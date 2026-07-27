from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


sys.dont_write_bytecode = True

from Y5_R2FR_4883_multi_eos_tov_love_response import (
    EOS_SPECS,
    EOS_TABLES,
    L_SUN_M,
    R0,
    SURFACE_FACTOR,
    _initial_state,
    _surface_q,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4886"
NEXT_TARGET = (
    "4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-"
    "silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md"
)

BETA_ANCHOR = -1.0 / 18.0
CASSINI_CENTRAL = 2.1e-5
CASSINI_SIGMA = 2.3e-5
CASSINI_TWO_SIGMA_ABS_CEILING = abs(CASSINI_CENTRAL) + 2 * CASSINI_SIGMA
OMEGA_B = 0.049
OMEGA_M = 0.315
H0_KM_S_MPC = 67.4
MPC_M = 3.085677581491367e22
C_M_S = 299792458.0
AU_M = 149597870700.0
HBAR_C_EV_M = 1.973269804e-7
Z_RECOMBINATION = 1100.0

TARGETS_PATH = OUTPUT / "P8_Y5_R2FR_4883_TARGET_LOCATIONS.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local = [
        (
            "SRC4886_00_previous_checkpoint",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        ),
        (
            "SRC4886_01_memory_action",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md",
            "b T M^2",
        ),
        (
            "SRC4886_02_memory_minimum",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md",
            "M_*^2 = 2",
        ),
        (
            "SRC4886_03_sign_branch",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "sign-of-the-coupling-b.md",
            "b < 0",
        ),
        (
            "SRC4886_04_EOS_targets",
            TARGETS_PATH,
            "canonical_1p4",
        ),
        (
            "SRC4886_05_EOS_validation",
            OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv",
            "VAL4883_OVERALL,PASS",
        ),
        (
            "SRC4886_06_Cassini_source_pack",
            POST
            / "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md",
            "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
        ),
        (
            "SRC4886_07_local_GR_certificate",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "gamma_{\\rm classical}=1",
        ),
        (
            "SRC4886_08_DEF_primary_pdf",
            POST
            / "source-intake"
            / "memory_uv"
            / "4886"
            / "Damour_Esposito_Farese_gr-qc_9602056.pdf",
            "binary-pulsar tensor-scalar primary PDF",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local:
        exists = path.exists()
        if path.suffix.lower() == ".pdf":
            marker_found = exists and path.stat().st_size == 395490
        else:
            marker_found = exists and marker in path.read_text(
                encoding="utf-8", errors="replace"
            )
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker_found,
            }
        )
    return {
        "rows": rows,
        "web_sources": {
            "Cassini_primary": "https://doi.org/10.1038/nature01997",
            "DEF_primary": "https://arxiv.org/abs/gr-qc/9602056",
        },
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def conformal_parent_completion() -> dict[str, Any]:
    beta, phi, trace = sp.symbols("beta phi T", real=True)
    log_a = beta * phi**2
    alpha_phi = sp.diff(log_a, phi)
    alpha_def = sp.sqrt(2) * alpha_phi
    leading_trace_term = sp.expand(log_a * trace)
    return {
        "dimensionless_field": "phi=M/Mbar_Pl",
        "dimensionless_coupling": "beta=b*Mbar_Pl^2",
        "matter_owner": "S_m[A(phi)^2 g_mn,Psi_m]",
        "conformal_factor": "A(phi)=exp(beta*phi^2)",
        "leading_expansion": "S_m[A^2 g]=S_m[g]+int sqrt(-g) beta*phi^2*T+O((beta*phi^2)^2)",
        "leading_trace_term": str(leading_trace_term),
        "alpha_phi": str(alpha_phi),
        "alpha_DEF": str(alpha_def),
        "normalization_relation": "varphi_DEF=phi/sqrt(2); alpha_DEF=sqrt(2)*d ln A/dphi",
        "scalar_equation": "Box phi=kappa*phi^3-8*pi*alpha_phi*T_geo",
        "matter_exchange": "nabla_mu T_m^(mu nu)=alpha_phi*T_m*nabla^nu phi",
        "dust_continuity": "rho_m_dot+3H*rho_m=alpha_phi*rho_m*phi_dot",
        "interpretation": (
            "this is the minimal diffeomorphism-invariant universal matter "
            "owner of the printed b*T*M^2 term; treating T as an external "
            "conserved source instead would leave the field theory open"
        ),
        "passed": bool(
            alpha_phi == 2 * beta * phi
            and alpha_def == 2 * sp.sqrt(2) * beta * phi
            and leading_trace_term == beta * phi**2 * trace
        ),
    }


def _target_rows() -> list[dict[str, Any]]:
    return [
        {
            "eos_id": row["eos_id"],
            "model_id": row["model_id"],
            "central_q": float(row["central_q"]),
            "reference_mass_Msun": float(row["mass_Msun"]),
            "reference_radius_km": float(row["radius_km"]),
        }
        for row in read_csv(TARGETS_PATH)
    ]


@lru_cache(maxsize=None)
def _background_profile(eos_id: str, central_q: float) -> dict[str, Any]:
    eos = EOS_TABLES[eos_id]
    surface_q = _surface_q(eos, SURFACE_FACTOR)
    initial = _initial_state(eos, central_q)[:2]

    def rhs(radius: float, state: np.ndarray) -> np.ndarray:
        mass, q_value = state
        energy, pressure, _, pressure_q, _, _ = eos.base_jet(q_value)
        metric_f = 1 - 2 * mass / radius
        mass_prime = 4 * math.pi * radius**2 * energy
        pressure_prime = -(
            (energy + pressure)
            * (mass + 4 * math.pi * radius**3 * pressure)
            / (radius**2 * metric_f)
        )
        return np.asarray([mass_prime, pressure_prime / pressure_q])

    def surface_event(radius: float, state: np.ndarray) -> float:
        return float(state[1] - surface_q)

    surface_event.terminal = True
    surface_event.direction = -1
    solution = solve_ivp(
        rhs,
        (R0, 100.0),
        initial,
        events=surface_event,
        rtol=3.0e-9,
        atol=np.asarray([1.0e-11, 2.0e-20]),
        max_step=0.02,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError(f"{eos_id}: scalar-background surface failure")
    radius_surface = float(solution.t_events[0][0])
    mass_surface = float(solution.y_events[0][0][0])
    radii = solution.t
    masses = solution.y[0]
    q_values = solution.y[1]

    friction: list[float] = []
    trace_source: list[float] = []
    traces: list[float] = []
    energies: list[float] = []
    pressures: list[float] = []
    for radius, mass, q_value in zip(radii, masses, q_values):
        energy, pressure, _, _, _, _ = eos.base_jet(q_value)
        metric_f = 1 - 2 * mass / radius
        mass_prime = 4 * math.pi * radius**2 * energy
        nu_prime = 2 * (
            mass + 4 * math.pi * radius**3 * pressure
        ) / (radius**2 * metric_f)
        lambda_prime = 2 * (
            mass_prime / radius - mass / radius**2
        ) / metric_f
        trace = float(energy - 3 * pressure)
        friction.append(2 / radius + (nu_prime - lambda_prime) / 2)
        trace_source.append(16 * math.pi * trace / metric_f)
        traces.append(trace)
        energies.append(float(energy))
        pressures.append(float(pressure))

    volume_weight = 4 * math.pi * radii**2
    positive_trace = np.maximum(np.asarray(traces), 0.0)
    absolute_trace = np.abs(np.asarray(traces))
    trace_positive_fraction = float(
        np.trapezoid(volume_weight * positive_trace, radii)
        / np.trapezoid(volume_weight * absolute_trace, radii)
    )
    return {
        "eos_id": eos_id,
        "central_q": central_q,
        "radii": np.asarray(radii),
        "friction": np.asarray(friction),
        "trace_source": np.asarray(trace_source),
        "mass": mass_surface,
        "radius": radius_surface,
        "radius_km": radius_surface * L_SUN_M / 1000,
        "compactness": mass_surface / radius_surface,
        "central_energy": energies[0],
        "central_pressure": pressures[0],
        "central_trace": traces[0],
        "minimum_trace": min(traces),
        "trace_positive_volume_fraction": trace_positive_fraction,
        "metric_f_surface": 1 - 2 * mass_surface / radius_surface,
    }


def _scalar_profile(
    background: dict[str, Any], beta: float, max_step: float = 0.03
) -> dict[str, float]:
    radii = background["radii"]
    friction = background["friction"]
    trace_source = background["trace_source"]
    radius_surface = background["radius"]
    mass = background["mass"]
    source_center = beta * trace_source[0]

    def rhs(radius: float, state: np.ndarray) -> np.ndarray:
        coefficient_p = np.interp(radius, radii, friction)
        coefficient_q = beta * np.interp(radius, radii, trace_source)
        field, gradient = state
        return np.asarray(
            [gradient, coefficient_q * field - coefficient_p * gradient]
        )

    solution = solve_ivp(
        rhs,
        (R0, radius_surface),
        np.asarray(
            [
                1 + source_center * R0**2 / 6,
                source_center * R0 / 3,
            ]
        ),
        rtol=1.0e-9,
        atol=1.0e-11,
        max_step=max_step,
    )
    if not solution.success:
        raise RuntimeError("scalar profile integration failed")
    field_surface, gradient_surface = solution.y[:, -1]
    metric_f = background["metric_f_surface"]
    flux_constant = radius_surface**2 * metric_f * gradient_surface
    field_infinity = field_surface - (
        flux_constant / (2 * mass)
    ) * math.log(metric_f)
    normalized_flux = flux_constant / field_infinity
    charge_ratio = normalized_flux / (4 * beta * mass)
    return {
        "field_center_over_infinity": 1 / field_infinity,
        "field_surface_over_infinity": field_surface / field_infinity,
        "gradient_surface_over_infinity": gradient_surface / field_infinity,
        "flux_Lsun": normalized_flux,
        "scalar_charge_ratio": charge_ratio,
        "unnormalized_field_infinity": field_infinity,
    }


def _first_scalarization_threshold(background: dict[str, Any]) -> float:
    samples = -np.geomspace(1.0e-4, 2.0, 18)
    previous_beta = float(samples[0])
    previous_value = _scalar_profile(background, previous_beta)[
        "unnormalized_field_infinity"
    ]
    for sample in samples[1:]:
        beta = float(sample)
        value = _scalar_profile(background, beta)[
            "unnormalized_field_infinity"
        ]
        if value * previous_value < 0:
            return float(
                brentq(
                    lambda trial: _scalar_profile(background, trial)[
                        "unnormalized_field_infinity"
                    ],
                    previous_beta,
                    beta,
                    xtol=1.0e-9,
                    rtol=1.0e-9,
                )
            )
        previous_beta = beta
        previous_value = value
    raise RuntimeError("first scalarization threshold not bracketed")


@lru_cache(maxsize=None)
def spherical_profiles() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    h0_inverse_lsun = (
        H0_KM_S_MPC * 1000 / MPC_M / C_M_S * L_SUN_M
    )
    ambient_baryon_density = (
        3 * OMEGA_B * h0_inverse_lsun**2 / (8 * math.pi)
    )
    for target in _target_rows():
        background = _background_profile(
            target["eos_id"], target["central_q"]
        )
        anchor = _scalar_profile(background, BETA_ANCHOR, 0.03)
        coarse = _scalar_profile(background, BETA_ANCHOR, 0.06)
        fine = _scalar_profile(background, BETA_ANCHOR, 0.015)
        beta_critical = _first_scalarization_threshold(background)
        rows.append(
            {
                **target,
                "computed_mass_Msun": background["mass"],
                "computed_radius_km": background["radius_km"],
                "compactness": background["compactness"],
                "central_pressure_over_energy": (
                    background["central_pressure"]
                    / background["central_energy"]
                ),
                "central_trace_Lsun_minus2": background["central_trace"],
                "minimum_trace_Lsun_minus2": background["minimum_trace"],
                "trace_positive_volume_fraction": background[
                    "trace_positive_volume_fraction"
                ],
                "beta_anchor": BETA_ANCHOR,
                "field_center_over_infinity": anchor[
                    "field_center_over_infinity"
                ],
                "field_surface_over_infinity": anchor[
                    "field_surface_over_infinity"
                ],
                "scalar_charge_ratio": anchor["scalar_charge_ratio"],
                "ambient_baryon_density_Lsun_minus2": (
                    ambient_baryon_density
                ),
                "ambient_quartic_to_central_trace_ratio": (
                    ambient_baryon_density
                    * anchor["field_center_over_infinity"] ** 2
                    / abs(background["central_trace"])
                ),
                "first_beta_scalarization": beta_critical,
                "first_beta_DEF_scalarization": 4 * beta_critical,
                "anchor_to_threshold_abs_ratio": (
                    abs(BETA_ANCHOR) / abs(beta_critical)
                ),
                "threshold_margin_factor": (
                    abs(beta_critical) / abs(BETA_ANCHOR)
                ),
                "coarse_fine_charge_fractional_difference": abs(
                    coarse["scalar_charge_ratio"]
                    / fine["scalar_charge_ratio"]
                    - 1
                ),
                "zero_branch_globally_stable_at_anchor": bool(
                    BETA_ANCHOR > beta_critical
                ),
            }
        )
    return {
        "equation": (
            "phi''+[2/r+(nu'-lambda')/2]phi'="
            "(1-2m/r)^-1[kappa*phi^3+16*pi*beta*(rho-3p)*phi]"
        ),
        "boundary_conditions": (
            "phi'(0)=0; regular center; exact Schwarzschild exterior "
            "phi=phi_inf+[C/(2M)]ln(1-2M/r)"
        ),
        "charge_definition": (
            "alpha_A/alpha_inf=C_normalized/(4*beta*M)"
        ),
        "rows": rows,
        "minimum_threshold_margin": min(
            row["threshold_margin_factor"] for row in rows
        ),
        "maximum_charge_convergence_error": max(
            row["coarse_fine_charge_fractional_difference"] for row in rows
        ),
        "interpretation": (
            "the pointwise negative M=0 Hessian found in 4885 is not a "
            "global instability at beta=-1/18; gradient energy keeps all "
            "nine stars below the first zero-mode threshold"
        ),
        "passed": bool(
            len(rows) == 9
            and all(row["zero_branch_globally_stable_at_anchor"] for row in rows)
            and all(
                0 < row["scalar_charge_ratio"] < 1 for row in rows
            )
            and min(row["threshold_margin_factor"] for row in rows) > 19
            and max(
                row["ambient_quartic_to_central_trace_ratio"]
                for row in rows
            )
            < 1.0e-40
            and max(
                row["coarse_fine_charge_fractional_difference"]
                for row in rows
            )
            < 3.0e-6
        ),
    }


@lru_cache(maxsize=None)
def weak_source_and_range() -> dict[str, Any]:
    solar_compactness = 1.4766250385 / 695700.0
    x_squared = 12 * abs(BETA_ANCHOR) * solar_compactness
    charge_ratio = 1 + 2 * x_squared / 5 + 17 * x_squared**2 / 105
    h0_per_second = H0_KM_S_MPC * 1000 / MPC_M
    h0_inverse_m = h0_per_second / C_M_S
    mass_over_h0 = math.sqrt(12 * abs(BETA_ANCHOR) * OMEGA_B)
    mass_inverse_m = mass_over_h0 * h0_inverse_m
    compton_m = 1 / mass_inverse_m
    bare_mass_AU_eV = HBAR_C_EV_M / AU_M
    cosmological_mass_eV = HBAR_C_EV_M * mass_inverse_m
    return {
        "uniform_density_equation": (
            "x^2=12*abs(beta)*compactness; "
            "charge_ratio=3*(tan(x)/x-1)/x^2"
        ),
        "solar_compactness": solar_compactness,
        "solar_x_squared": x_squared,
        "solar_charge_ratio": charge_ratio,
        "solar_screening_fraction": 1 - charge_ratio,
        "ambient_mass_over_H0": mass_over_h0,
        "ambient_compton_Mpc": compton_m / MPC_M,
        "ambient_mass_eV": cosmological_mass_eV,
        "ambient_mass_times_AU": mass_inverse_m * AU_M,
        "bare_mass_for_one_AU_range_eV": bare_mass_AU_eV,
        "AU_screening_to_cosmological_mass_ratio": (
            bare_mass_AU_eV / cosmological_mass_eV
        ),
        "interpretation": (
            "the density-minimum fluctuation is effectively massless on "
            "Solar-System scales and the Sun is unscreened at the anchor; "
            "a bare mass short enough to hide it within one AU is about "
            "10^15 times the cosmological mass scale"
        ),
        "passed": bool(
            abs(charge_ratio - 1) < 1.0e-6
            and compton_m / MPC_M > 2.0e4
            and mass_inverse_m * AU_M < 1.0e-14
            and bare_mass_AU_eV / cosmological_mass_eV > 1.0e14
        ),
    }


@lru_cache(maxsize=None)
def ppn_cosmology_link() -> dict[str, Any]:
    alpha_def_squared_max = CASSINI_TWO_SIGMA_ABS_CEILING / (
        2 - CASSINI_TWO_SIGMA_ABS_CEILING
    )
    b_max = alpha_def_squared_max / (8 * abs(BETA_ANCHOR))
    scenarios: list[dict[str, Any]] = []
    for b_value, label in (
        (b_max, "Cassini_two_sigma_ceiling"),
        (1.0e-3, "per_mille_growth_target"),
        (1.0e-2, "one_percent_growth_target"),
        (5.0e-2, "five_percent_growth_target"),
    ):
        alpha_squared = 8 * abs(BETA_ANCHOR) * b_value
        gamma_deviation = 2 * alpha_squared / (1 + alpha_squared)
        scenarios.append(
            {
                "scenario": label,
                "B0": b_value,
                "phi_infinity_squared": b_value / abs(BETA_ANCHOR),
                "ln_A_infinity": -b_value,
                "alpha_DEF_squared": alpha_squared,
                "abs_gamma_minus_one": gamma_deviation,
                "Cassini_ceiling_ratio": (
                    gamma_deviation / CASSINI_TWO_SIGMA_ABS_CEILING
                ),
                "large_scale_growth_modification": -b_value,
                "Cassini_allowed": bool(
                    gamma_deviation <= CASSINI_TWO_SIGMA_ABS_CEILING
                    * (1 + 1.0e-12)
                ),
            }
        )
    return {
        "minimum_branch": "phi_inf^2=B0/abs(beta)",
        "standard_scalar_coupling": (
            "alpha_DEF^2=8*abs(beta)*B0"
        ),
        "PPN_relation": (
            "gamma-1=-2*alpha_DEF^2/(1+alpha_DEF^2)"
        ),
        "Cassini_measurement": "gamma-1=(2.1+/-2.3)e-5",
        "conservative_two_sigma_abs_ceiling": (
            CASSINI_TWO_SIGMA_ABS_CEILING
        ),
        "alpha_DEF_squared_max": alpha_def_squared_max,
        "B0_max": b_max,
        "maximum_large_scale_growth_suppression": b_max,
        "scenarios": scenarios,
        "interpretation": (
            "the same amplitude B0 that produces the corpus large-scale "
            "growth suppression fixes the long-range scalar PPN coupling; "
            "at beta=-1/18 the conservative Cassini ceiling forces the "
            "effect below 7.6e-5"
        ),
        "passed": bool(
            b_max < 7.6e-5
            and scenarios[2]["Cassini_ceiling_ratio"] > 130
            and scenarios[3]["Cassini_ceiling_ratio"] > 600
        ),
    }


@lru_cache(maxsize=None)
def flrw_dynamics_gate() -> dict[str, Any]:
    scale_ratio = 1 + Z_RECOMBINATION
    mode_rows: list[dict[str, Any]] = []
    for coupled_fraction, label in (
        (OMEGA_B / OMEGA_M, "baryons_only"),
        (1.0, "all_nonrelativistic_matter"),
    ):
        discriminant = 2.25 - 24 * BETA_ANCHOR * coupled_fraction
        growing = (-1.5 + math.sqrt(discriminant)) / 2
        decaying = (-1.5 - math.sqrt(discriminant)) / 2
        mode_rows.append(
            {
                "coupled_sector": label,
                "coupled_matter_fraction": coupled_fraction,
                "matter_era_equation": (
                    "phi_NN+3*phi_N/2+6*beta*f_c*phi=0"
                ),
                "growing_exponent": growing,
                "decaying_exponent": decaying,
                "growth_recombination_to_today": scale_ratio**growing,
                "instantaneous_minimum_exponent": -1.5,
            }
        )
    ppn = ppn_cosmology_link()
    b0_max = ppn["B0_max"]
    b_recombination = b0_max * scale_ratio**3
    perturbative_b0_ceiling = 0.01 / scale_ratio**3
    return {
        "mode_rows": mode_rows,
        "minimum_scaling": "B(a)=B0*a^-3; phi_min proportional a^-3/2",
        "B0_Cassini_max": b0_max,
        "B_at_recombination_if_tracking": b_recombination,
        "A_at_recombination_if_tracking": (
            0.0 if b_recombination > 745 else math.exp(-b_recombination)
        ),
        "B0_for_abs_lnA_recombination_below_0p01": (
            perturbative_b0_ceiling
        ),
        "Cassini_B0_over_recombination_perturbative_ceiling": (
            b0_max / perturbative_b0_ceiling
        ),
        "dichotomy": (
            "tracking the printed minimum back to recombination makes the "
            "trace-coupling completion nonperturbative; remaining near the "
            "small-field branch avoids that but invalidates the minimum-"
            "branch growth formula and gives only slow matter-era evolution"
        ),
        "passed": bool(
            mode_rows[0]["growing_exponent"] < 0.04
            and mode_rows[1]["growing_exponent"] < 0.21
            and b_recombination > 1.0e4
            and perturbative_b0_ceiling < 1.0e-11
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    parent = conformal_parent_completion()
    stars = spherical_profiles()
    weak = weak_source_and_range()
    link = ppn_cosmology_link()
    flrw = flrw_dynamics_gate()
    return {
        "minimal_covariant_trace_owner": (
            "A(phi)=exp(beta*phi^2) universal conformal matter metric"
        ),
        "anchor_neutron_star_scalarization": False,
        "anchor_pointwise_tachyon_refined": (
            "NO_GLOBAL_ZERO_MODE_ON_NINE_TESTED_STARS"
        ),
        "anchor_solar_screening": False,
        "anchor_scalar_range": "COSMOLOGICAL_NOT_YUKAWA_SCREENED_LOCALLY",
        "maximum_same_branch_B0": link["B0_max"],
        "maximum_same_branch_large_scale_growth_effect": link[
            "maximum_large_scale_growth_suppression"
        ],
        "significant_active_M_growth_branch": (
            "REJECTED_UNDER_MINIMAL_COVARIANT_TRACE_OWNER"
        ),
        "canonical_M_UV_determinant": "RETAINED",
        "Gamma_overdamped_readout": "RETAINED",
        "bTM2_cosmology_status": (
            "PERTURBATIVE_NEGLIGIBLE_OR_PHENOMENOLOGICAL_CLOSURE_ONLY"
        ),
        "renormalized_EH_local_branch": "RETAINED",
        "next_route": (
            "derive a conserved derivative/curvature memory source whose "
            "stationary local PPN projection vanishes while FLRW activation "
            "does not, or demote active-M cosmology"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            sources["passed"]
            and parent["passed"]
            and stars["passed"]
            and weak["passed"]
            and link["passed"]
            and flrw["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "parent_completion": conformal_parent_completion(),
        "stellar_profiles": spherical_profiles(),
        "weak_source_range": weak_source_and_range(),
        "PPN_cosmology_link": ppn_cosmology_link(),
        "FLRW_dynamics": flrw_dynamics_gate(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(
        section.get("passed", True) for section in sections.values()
    )
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "all_checks_pass": all_checks_pass,
        "decision": (
            "close the static memory-scalar boundary problem on nine "
            "microphysical neutron-star backgrounds; refine the pointwise "
            "tachyon into a globally stable anchor below the first zero "
            "mode; prove the Sun is unscreened and the scalar cosmologically "
            "long ranged; map the corpus cosmological amplitude B0 directly "
            "to Cassini gamma; reject significant bTM2-driven growth under "
            "the minimal covariant matter owner while retaining canonical M, "
            "its overdamped Gamma readout, and the renormalized-EH branch"
        ),
    }


if __name__ == "__main__":
    calculation = result()
    print("MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886")
    print(f"all_checks_pass={calculation['all_checks_pass']}")
    print(calculation["decision"])
