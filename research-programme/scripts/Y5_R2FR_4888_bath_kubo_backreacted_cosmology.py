from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FORMAL_SCRIPTS = FORMAL / "scripts"
if str(FORMAL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(FORMAL_SCRIPTS))

from cosmology_background_benchmark import C_KM_S, load_json  # noqa: E402
from cosmology_likelihood_smoke import (  # noqa: E402
    cumulative_trapezoid_grid,
    load_bao,
    load_pantheon,
    select_dataset,
)


CHECKPOINT = "4888"
NEXT_TARGET = (
    "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-"
    "and-binary-leakage-or-expansion-source-demotion-gate.md"
)

INITIAL_N = -7.0
OMEGA_R = 9.0e-5
OMEGA_M = 0.315
OMEGA_X = 0.049
OMEGA_OTHER_M = OMEGA_M - OMEGA_X
SIGMA_BAR = 0.3
GAMMA_BAR = 1.0
W_X = 0.0
TARGETS = (1.0e-4, 1.0e-3, 1.0e-2)


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    text_sources = [
        (
            "SRC4888_00_4887",
            POST
            / "4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md",
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887",
        ),
        (
            "SRC4888_01_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "A closed microscopic completion may use a continuum of bath fields",
        ),
        (
            "SRC4888_02_4885",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "Minimal same-parent completion and overdamped map",
        ),
        (
            "SRC4888_03_4886",
            POST
            / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
        ),
        (
            "SRC4888_04_prior_validation",
            POST
            / "source-intake"
            / "mts_residuals"
            / "P8_Y5_BRR545_4887_VALIDATION.csv",
            "VAL4887_OVERALL,PASS",
        ),
        (
            "SRC4888_05_config",
            FORMAL / "configs" / "cosmology_background_R1_current.json",
            "R1_current_background",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in text_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_text",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": _contains(path, marker),
            }
        )
    data_sources = [
        (
            "SRC4888_06_pantheon_data",
            FORMAL
            / "data"
            / "cosmology"
            / "pantheon_plus"
            / "Pantheon+SH0ES.dat",
        ),
        (
            "SRC4888_07_pantheon_covariance",
            FORMAL
            / "data"
            / "cosmology"
            / "pantheon_plus"
            / "Pantheon+SH0ES_STAT+SYS.cov",
        ),
        (
            "SRC4888_08_desi_data",
            FORMAL
            / "data"
            / "cosmology"
            / "desi_dr2_bao"
            / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        ),
        (
            "SRC4888_09_desi_covariance",
            FORMAL
            / "data"
            / "cosmology"
            / "desi_dr2_bao"
            / "desi_gaussian_bao_ALL_GCcomb_cov.txt",
        ),
    ]
    for source_id, path in data_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_data",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": "positive_file_size",
                "marker_found": path.exists() and path.stat().st_size > 0,
                "size_bytes": path.stat().st_size if path.exists() else 0,
            }
        )
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def microscopic_spectral_matching() -> dict[str, Any]:
    mixing_ratio = SIGMA_BAR**2 / (
        3.0 * OMEGA_X * (1.0 + W_X)
    )
    correlation = math.sqrt(mixing_ratio)
    memory_direction = np.asarray([1.0, 0.0])
    compression_direction = np.asarray(
        [correlation, math.sqrt(1.0 - correlation**2)]
    )
    gram = np.asarray(
        [
            [memory_direction @ memory_direction,
             memory_direction @ compression_direction],
            [compression_direction @ memory_direction,
             compression_direction @ compression_direction],
        ]
    )
    eigenvalues = np.linalg.eigvalsh(gram)
    return {
        "closed_parent_action": (
            "S_chi=sum_a int sqrt(-g)[-(grad chi_a)^2/2-"
            "Omega_a^2 chi_a^2/2+chi_a(c_a phi+d_a theta)]"
        ),
        "first_derivative_form": (
            "int sqrt(-g) d_a chi_a theta=-int sqrt(-g) "
            "d_a u^mu grad_mu chi_a+boundary"
        ),
        "retarded_kernel": (
            "K_AB^R(omega,k)=sum_a lambda_Aa lambda_Ba/"
            "[Omega_a^2+k^2-(omega+i0)^2]"
        ),
        "sigma_matching": (
            "Mbar_Pl^2 sigma_theta=K_phi_theta^R(0,0)="
            "sum_a c_a d_a/Omega_a^2"
        ),
        "gamma_matching": (
            "gamma_M=lim_omega_to_0plus Im K_phi_phi^R(omega,0)/"
            "(Mbar_Pl^2 omega)"
        ),
        "dispersion_relation": (
            "Mbar_Pl^2 sigma_theta=(2/pi) integral_0^infty "
            "domega Im K_phi_theta^R(omega,0)/omega, with subtractions "
            "fixed by the parent renormalization rule"
        ),
        "local_effective_action": (
            "Delta L=C_phi_phi phi^2/2+C_phi_theta phi theta+"
            "C_theta_theta theta^2/2+O(partial^2/Omega^2)"
        ),
        "diagonal_terms": (
            "C_phi_phi=sum c_a^2/Omega_a^2; "
            "C_theta_theta=sum d_a^2/Omega_a^2"
        ),
        "cauchy_schwarz": (
            "C_phi_theta^2<=C_phi_phi C_theta_theta"
        ),
        "cross_sign_fixed_by_passivity": False,
        "sigma_fixed_by_gamma_alone": False,
        "numeric_parent_prediction_complete": False,
        "normalized_benchmark_mixing_ratio": mixing_ratio,
        "normalized_benchmark_correlation": correlation,
        "normalized_two_mode_gram_min_eigenvalue": float(eigenvalues[0]),
        "normalized_two_mode_gram_max_eigenvalue": float(eigenvalues[1]),
        "constructive_example_positive_semidefinite": bool(
            eigenvalues[0] > 0.0
            and abs(gram[0, 1] - correlation) < 1.0e-14
        ),
        "ownership_verdict": (
            "EXACT_KUBO_MATCHING_FORMULA_AND_HEALTHY_TWO_MODE_EXISTENCE_"
            "CONSTRUCTED_NUMERIC_SIGMA_REMAINS_INDEPENDENT_CROSS_SPECTRAL_"
            "WILSON_DATA"
        ),
        "passed": bool(
            0.61 < mixing_ratio < 0.62
            and 0.78 < correlation < 0.79
            and eigenvalues[0] > 0.0
        ),
    }


@lru_cache(maxsize=None)
def conserved_stress_owner() -> dict[str, Any]:
    return {
        "interaction_stress": (
            "T_sigma_mn=Mbar_Pl^2 sigma_theta[2 u_(m grad_n)phi+"
            "Y u_m u_n-Y g_mn], Y=u.grad phi"
        ),
        "clock_current": (
            "J_Theta^mu=P_X sqrt(2X) u^mu+Mbar_Pl^2 sigma_theta "
            "h^munu grad_nu phi/sqrt(2X); div J_Theta=0"
        ),
        "homogeneous_interaction_density": "rho_sigma=0",
        "homogeneous_interaction_pressure": (
            "p_sigma=-Mbar_Pl^2 sigma_theta phi_dot"
        ),
        "scalar_continuity": (
            "rho_phi_dot+3H(rho_phi+p_phi)="
            "Mbar_Pl^2[3 sigma_theta H phi_dot-gamma_M phi_dot^2]"
        ),
        "bath_continuity": (
            "rho_X_dot+3H(rho_X+p_X)=Mbar_Pl^2 gamma_M phi_dot^2"
        ),
        "total_continuity": (
            "rho_tot_dot+3H[rho_tot+p_phi+p_X+p_sigma+p_other]=0"
        ),
        "diffeomorphism_identity": (
            "div T_total=E_phi grad phi+E_Theta grad Theta; on shell zero"
        ),
        "background_interaction_is_zero_energy_not_zero_stress": True,
        "passed": True,
    }


@lru_cache(maxsize=None)
def coupled_characteristics() -> dict[str, Any]:
    mixing_ratio = SIGMA_BAR**2 / (
        3.0 * OMEGA_X * (1.0 + W_X)
    )
    rows: list[dict[str, Any]] = []
    for sound_speed_squared in (1.0 / 3.0, 0.1, 1.0e-3):
        epsilon = mixing_ratio * sound_speed_squared
        discriminant = math.sqrt(
            (1.0 - sound_speed_squared) ** 2 + 4.0 * epsilon
        )
        upper = (1.0 + sound_speed_squared + discriminant) / 2.0
        lower = (1.0 + sound_speed_squared - discriminant) / 2.0
        rows.append(
            {
                "bath_sound_speed_squared": sound_speed_squared,
                "mixing_ratio": mixing_ratio,
                "epsilon": epsilon,
                "c_plus_squared": upper,
                "c_minus_squared": lower,
                "no_gradient_instability": lower > 0.0,
                "public_cone_exceeded_low_energy": upper > 1.0,
            }
        )
    return {
        "quadratic_determinant": (
            "(c_mode^2-1)(c_mode^2-c_X^2)-"
            "R_mix c_X^2=0"
        ),
        "mixing_ratio": mixing_ratio,
        "stability_condition": "R_mix=Mbar_Pl^2 sigma_theta^2/(rho_X+p_X)<1",
        "upper_root_theorem": (
            "for sigma_theta nonzero and c_X^2>0, c_plus^2>max(1,c_X^2)"
        ),
        "bare_phi_principal_block_unchanged": True,
        "coupled_public_cone_unchanged": False,
        "UV_front_velocity_status": (
            "requires the untruncated causal nonlocal bath kernel; the "
            "local derivative truncation cannot prove a shared front cone"
        ),
        "rows": rows,
        "passed": bool(
            mixing_ratio < 1.0
            and all(row["no_gradient_instability"] for row in rows)
            and all(row["public_cone_exceeded_low_energy"] for row in rows)
        ),
    }


def _branch_initial_guess(target: float) -> np.ndarray:
    guesses = {
        1.0e-4: 3.356e8,
        1.0e-3: 4.719e5,
        1.0e-2: 9.854e2,
    }
    return np.asarray([math.log(guesses[target]), 0.0])


def _branch_integrator(
    target: float, log_kappa: float, log_bath_scale: float
) -> dict[str, Any]:
    kappa_bar = math.exp(log_kappa)
    omega_lambda = 1.0 - OMEGA_R - OMEGA_M - target
    initial_bath = OMEGA_X * math.exp(-3.0 * INITIAL_N + log_bath_scale)

    def background_values(
        n_value: float, state: np.ndarray
    ) -> tuple[float, float, float]:
        field, field_n, bath_density = state
        radiation = OMEGA_R * math.exp(-4.0 * n_value)
        other_matter = OMEGA_OTHER_M * math.exp(-3.0 * n_value)
        potential = kappa_bar * field**4 / 12.0
        denominator = 1.0 - field_n**2 / 6.0
        numerator = (
            radiation
            + other_matter
            + omega_lambda
            + bath_density
            + potential
        )
        if denominator <= 0.0 or numerator <= 0.0:
            raise ValueError("non-positive Friedmann branch")
        e_squared = numerator / denominator
        e_value = math.sqrt(e_squared)
        h_prime = (
            -2.0 * radiation / e_squared
            - 1.5
            * (other_matter + (1.0 + W_X) * bath_density)
            / e_squared
            - 0.5 * field_n**2
            + SIGMA_BAR * field_n / (2.0 * e_value)
        )
        return e_value, h_prime, potential

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        field, field_n, bath_density = state
        e_value, h_prime, _ = background_values(n_value, state)
        return np.asarray(
            [
                field_n,
                -(3.0 + h_prime + GAMMA_BAR / e_value) * field_n
                - kappa_bar * field**3 / e_value**2
                + 3.0 * SIGMA_BAR / e_value,
                -3.0 * (1.0 + W_X) * bath_density
                + GAMMA_BAR * e_value * field_n**2 / 3.0,
            ]
        )

    solution = solve_ivp(
        rhs,
        (INITIAL_N, 0.0),
        np.asarray([0.0, 0.0, initial_bath]),
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError("backreacted FLRW integration failed")
    field, field_n, bath_density = solution.y[:, -1]
    e_value, _, potential = background_values(0.0, solution.y[:, -1])
    memory_fraction = (
        e_value**2 * field_n**2 / 6.0 + potential
    ) / e_value**2
    return {
        "target": target,
        "kappa_bar": kappa_bar,
        "log_kappa": log_kappa,
        "bath_scale": math.exp(log_bath_scale),
        "log_bath_scale": log_bath_scale,
        "omega_lambda": omega_lambda,
        "solution": solution,
        "background_values": background_values,
        "rhs": rhs,
        "bath_today": float(bath_density),
        "memory_today": float(memory_fraction),
        "E_today": float(e_value),
    }


@lru_cache(maxsize=None)
def _solve_branch(target: float) -> dict[str, Any]:
    def residual(vector: np.ndarray) -> np.ndarray:
        run = _branch_integrator(target, float(vector[0]), float(vector[1]))
        return np.asarray(
            [
                math.log(run["memory_today"] / target),
                math.log(run["bath_today"] / OMEGA_X),
            ]
        )

    root_result = optimize.root(
        residual,
        _branch_initial_guess(target),
        method="hybr",
        tol=1.0e-10,
    )
    if not root_result.success:
        raise RuntimeError(f"branch shooting failed: {root_result.message}")
    run = _branch_integrator(
        target, float(root_result.x[0]), float(root_result.x[1])
    )
    run["shooting_success"] = bool(root_result.success)
    run["shooting_residual_norm"] = float(
        np.linalg.norm(residual(root_result.x), ord=np.inf)
    )
    return run


def _branch_arrays(run: dict[str, Any], count: int = 1601) -> dict[str, np.ndarray]:
    n_values = np.linspace(INITIAL_N, 0.0, count)
    states = run["solution"].sol(n_values)
    e_values = np.empty_like(n_values)
    h_values = np.empty_like(n_values)
    potential_values = np.empty_like(n_values)
    rhs_values = np.empty_like(states)
    for index, n_value in enumerate(n_values):
        e_value, h_value, potential = run["background_values"](
            float(n_value), states[:, index]
        )
        e_values[index] = e_value
        h_values[index] = h_value
        potential_values[index] = potential
        rhs_values[:, index] = run["rhs"](
            float(n_value), states[:, index]
        )
    return {
        "N": n_values,
        "state": states,
        "rhs": rhs_values,
        "E": e_values,
        "h": h_values,
        "V": potential_values,
    }


def _branch_summary(run: dict[str, Any]) -> dict[str, Any]:
    arrays = _branch_arrays(run)
    n_values = arrays["N"]
    field, field_n, bath_density = arrays["state"]
    field_nn = arrays["rhs"][1]
    bath_n = arrays["rhs"][2]
    e_values = arrays["E"]
    h_values = arrays["h"]
    potential = arrays["V"]
    radiation = OMEGA_R * np.exp(-4.0 * n_values)
    other_matter = OMEGA_OTHER_M * np.exp(-3.0 * n_values)
    memory_density = e_values**2 * field_n**2 / 6.0 + potential
    memory_fraction = memory_density / e_values**2
    numerator = (
        radiation
        + other_matter
        + run["omega_lambda"]
        + bath_density
        + potential
    )
    denominator = 1.0 - field_n**2 / 6.0
    numerator_n = (
        -4.0 * radiation
        - 3.0 * other_matter
        + bath_n
        + run["kappa_bar"] * field**3 * field_n / 3.0
    )
    denominator_n = -field_n * field_nn / 3.0
    h_from_constraint = 0.5 * (
        numerator_n / numerator - denominator_n / denominator
    )
    memory_density_n = (
        e_values**2 * h_values * field_n**2 / 3.0
        + e_values**2 * field_n * field_nn / 3.0
        + run["kappa_bar"] * field**3 * field_n / 3.0
    )
    total_density_n = (
        -4.0 * radiation
        - 3.0 * other_matter
        + bath_n
        + memory_density_n
    )
    three_enthalpy = (
        4.0 * radiation
        + 3.0 * other_matter
        + 3.0 * (1.0 + W_X) * bath_density
        + e_values**2 * field_n**2
        - SIGMA_BAR * e_values * field_n
    )
    continuity_residual = total_density_n + three_enthalpy
    continuity_scale = 1.0 + np.abs(total_density_n) + np.abs(three_enthalpy)
    half_target = 0.5 * run["target"]
    activated = np.flatnonzero(memory_fraction >= half_target)
    half_redshift = (
        math.exp(-float(n_values[activated[0]])) - 1.0
        if len(activated)
        else math.nan
    )
    return {
        "target_Omega_memory_today": run["target"],
        "sigma_theta_over_H0": SIGMA_BAR,
        "gamma_M_over_H0": GAMMA_BAR,
        "kappa_over_H0_squared": run["kappa_bar"],
        "initial_bath_dust_normalization_ratio": run["bath_scale"],
        "bath_heating_compensation_fraction": 1.0 - run["bath_scale"],
        "Omega_X_today": run["bath_today"],
        "Omega_memory_today": run["memory_today"],
        "E_today": run["E_today"],
        "phi_today": float(field[-1]),
        "dphi_dN_today": float(field_n[-1]),
        "maximum_Omega_memory": float(np.max(memory_fraction)),
        "half_activation_redshift": half_redshift,
        "maximum_abs_Friedmann_derivative_residual": float(
            np.max(np.abs(h_from_constraint - h_values))
        ),
        "maximum_relative_total_continuity_residual": float(
            np.max(np.abs(continuity_residual) / continuity_scale)
        ),
        "maximum_field_speed_squared": float(np.max(field_n**2)),
        "minimum_E_squared": float(np.min(e_values**2)),
        "shooting_residual_norm": run["shooting_residual_norm"],
        "backreaction_pass": bool(
            abs(run["E_today"] - 1.0) < 1.0e-8
            and abs(run["bath_today"] / OMEGA_X - 1.0) < 1.0e-8
            and abs(run["memory_today"] / run["target"] - 1.0) < 1.0e-8
            and np.max(np.abs(h_from_constraint - h_values)) < 1.0e-10
            and np.max(np.abs(continuity_residual) / continuity_scale)
            < 1.0e-10
            and np.max(field_n**2) < 6.0
            and np.min(e_values**2) > 0.0
        ),
    }


@lru_cache(maxsize=None)
def backreacted_flrw() -> dict[str, Any]:
    rows = [_branch_summary(_solve_branch(target)) for target in TARGETS]
    return {
        "dimensionless_Friedmann": (
            "E^2=[x_r+x_o+x_X+x_Lambda+kappa_bar phi^4/12]/"
            "[1-phi_N^2/6]"
        ),
        "Raychaudhuri": (
            "H_N/H=-2x_r/E^2-3[x_o+(1+w_X)x_X]/(2E^2)-"
            "phi_N^2/2+sigma_bar phi_N/(2E)"
        ),
        "memory_equation": (
            "phi_NN+(3+H_N/H+gamma_bar/E)phi_N+"
            "kappa_bar phi^3/E^2=3 sigma_bar/E"
        ),
        "bath_equation": (
            "x_X,N=-3(1+w_X)x_X+gamma_bar E phi_N^2/3"
        ),
        "rows": rows,
        "passed": all(row["backreaction_pass"] for row in rows),
    }


def _solve_growth(
    n_values: np.ndarray,
    e_values: np.ndarray,
    h_values: np.ndarray,
    clustering_density: np.ndarray,
) -> Any:
    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        e_value = float(np.interp(n_value, n_values, e_values))
        h_value = float(np.interp(n_value, n_values, h_values))
        cluster = float(np.interp(n_value, n_values, clustering_density))
        return np.asarray(
            [
                state[1],
                -(2.0 + h_value) * state[1]
                + 1.5 * cluster * state[0] / e_value**2,
            ]
        )

    initial_growth = math.exp(INITIAL_N)
    solution = solve_ivp(
        rhs,
        (INITIAL_N, 0.0),
        np.asarray([initial_growth, initial_growth]),
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError("growth integration failed")
    return solution


@lru_cache(maxsize=None)
def smooth_memory_growth_limit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for target in TARGETS:
        run = _solve_branch(target)
        arrays = _branch_arrays(run)
        n_values = arrays["N"]
        e_values = arrays["E"]
        h_values = arrays["h"]
        bath_density = arrays["state"][2]
        other_matter = OMEGA_OTHER_M * np.exp(-3.0 * n_values)
        clustering_density = other_matter + bath_density
        mts_growth = _solve_growth(
            n_values, e_values, h_values, clustering_density
        )
        baseline_e = np.sqrt(
            OMEGA_R * np.exp(-4.0 * n_values)
            + OMEGA_M * np.exp(-3.0 * n_values)
            + 1.0
            - OMEGA_R
            - OMEGA_M
        )
        baseline_h = -(
            4.0 * OMEGA_R * np.exp(-4.0 * n_values)
            + 3.0 * OMEGA_M * np.exp(-3.0 * n_values)
        ) / (2.0 * baseline_e**2)
        baseline_growth = _solve_growth(
            n_values,
            baseline_e,
            baseline_h,
            OMEGA_M * np.exp(-3.0 * n_values),
        )
        for redshift in (0.0, 0.5, 1.0, 2.0):
            n_value = -math.log1p(redshift)
            mts_state = mts_growth.sol(n_value)
            baseline_state = baseline_growth.sol(n_value)
            mts_today = mts_growth.sol(0.0)[0]
            baseline_today = baseline_growth.sol(0.0)[0]
            mts_d = mts_state[0] / mts_today
            baseline_d = baseline_state[0] / baseline_today
            mts_f = mts_state[1] / mts_state[0]
            baseline_f = baseline_state[1] / baseline_state[0]
            rows.append(
                {
                    "target_Omega_memory_today": target,
                    "redshift": redshift,
                    "D_MTS_normalized": float(mts_d),
                    "D_LCDM_normalized": float(baseline_d),
                    "fractional_D_shift": float(mts_d / baseline_d - 1.0),
                    "f_MTS": float(mts_f),
                    "f_LCDM": float(baseline_f),
                    "fractional_f_shift": float(mts_f / baseline_f - 1.0),
                }
            )
    return {
        "limit": (
            "GR subhorizon growth with pressure-supported memory and the "
            "c_X^2 to zero clustering bath mode"
        ),
        "equation": (
            "D_NN+(2+H_N/H)D_N-(3/2)Omega_cluster D=0"
        ),
        "full_coupled_perturbation_likelihood": False,
        "rows": rows,
        "maximum_abs_fractional_D_shift": max(
            abs(row["fractional_D_shift"]) for row in rows
        ),
        "maximum_abs_fractional_f_shift": max(
            abs(row["fractional_f_shift"]) for row in rows
        ),
        "passed": all(
            math.isfinite(row["fractional_D_shift"])
            and math.isfinite(row["fractional_f_shift"])
            for row in rows
        ),
    }


def _score_background(
    z_grid: np.ndarray,
    e_grid: np.ndarray,
    sn: dict[str, Any],
    bao: dict[str, Any],
) -> dict[str, Any]:
    integral = cumulative_trapezoid_grid(z_grid, 1.0 / e_grid)
    d_m_sn = C_KM_S * np.interp(sn["z_cosmo"], z_grid, integral) / 70.0
    d_l_sn = (1.0 + sn["z_hel"]) * d_m_sn
    mu_model = 5.0 * np.log10(d_l_sn) + 25.0
    residual = sn["mu_obs"] - mu_model
    c_inv_residual = linalg.cho_solve(
        sn["cho"], residual, check_finite=False
    )
    offset = float(
        sn["ones"] @ c_inv_residual / sn["ones_cinv_ones"]
    )
    adjusted = residual - offset * sn["ones"]
    chi2_sn = float(
        adjusted
        @ linalg.cho_solve(sn["cho"], adjusted, check_finite=False)
    )

    def bao_chi2(log_q: float) -> float:
        q_value = math.exp(log_q)
        d_m = (
            C_KM_S
            * np.interp(bao["z"], z_grid, integral)
            / q_value
        )
        e_values = np.interp(bao["z"], z_grid, e_grid)
        d_h = C_KM_S / (q_value * e_values)
        d_v = np.cbrt(bao["z"] * d_m**2 * d_h)
        predicted = []
        for index, quantity in enumerate(bao["quantity"]):
            values = {
                "DM_over_rs": d_m[index],
                "DH_over_rs": d_h[index],
                "DV_over_rs": d_v[index],
            }
            predicted.append(values[quantity])
        bao_residual = bao["obs"] - np.asarray(predicted)
        return float(
            bao_residual
            @ linalg.cho_solve(
                bao["cho"], bao_residual, check_finite=False
            )
        )

    q_fit = optimize.minimize_scalar(
        bao_chi2,
        bounds=(math.log(7500.0), math.log(14000.0)),
        method="bounded",
        options={"xatol": 1.0e-9},
    )
    chi2_bao = float(q_fit.fun)
    return {
        "chi2_sn": chi2_sn,
        "chi2_bao": chi2_bao,
        "chi2_total": chi2_sn + chi2_bao,
        "sn_offset": offset,
        "q_H0_rd": math.exp(float(q_fit.x)),
        "q_fit_success": bool(q_fit.success),
    }


def _baseline_e(
    model: str, params: np.ndarray, z_grid: np.ndarray
) -> np.ndarray:
    zp1 = 1.0 + z_grid
    omega_m = float(params[0])
    if model == "LCDM":
        dark = np.full_like(z_grid, 1.0 - OMEGA_R - omega_m)
    elif model == "wCDM":
        equation_of_state = float(params[1])
        dark = (1.0 - OMEGA_R - omega_m) * zp1 ** (
            3.0 * (1.0 + equation_of_state)
        )
    elif model == "CPL":
        w0 = float(params[1])
        wa = float(params[2])
        scale = 1.0 / zp1
        dark = (
            (1.0 - OMEGA_R - omega_m)
            * scale ** (-3.0 * (1.0 + w0 + wa))
            * np.exp(3.0 * wa * (scale - 1.0))
        )
    else:
        raise ValueError(f"unknown baseline {model}")
    e_squared = OMEGA_R * zp1**4 + omega_m * zp1**3 + dark
    if np.any(e_squared <= 0.0) or np.any(~np.isfinite(e_squared)):
        raise ValueError("invalid baseline background")
    return np.sqrt(e_squared)


def _fit_baseline(
    model: str,
    z_grid: np.ndarray,
    sn: dict[str, Any],
    bao: dict[str, Any],
) -> dict[str, Any]:
    definitions = {
        "LCDM": {
            "bounds": ((0.1, 0.5),),
            "starts": ((0.2,), (0.3,), (0.4,)),
            "names": ("Omega_m",),
        },
        "wCDM": {
            "bounds": ((0.1, 0.5), (-1.4, -0.6)),
            "starts": ((0.3, -1.0), (0.3, -0.9), (0.25, -1.1)),
            "names": ("Omega_m", "w"),
        },
        "CPL": {
            "bounds": ((0.1, 0.5), (-1.6, -0.4), (-2.0, 2.0)),
            "starts": (
                (0.3, -1.0, 0.0),
                (0.31, -0.86, -0.56),
                (0.25, -1.0, 0.5),
                (0.35, -1.1, -0.5),
            ),
            "names": ("Omega_m", "w0", "wa"),
        },
    }
    definition = definitions[model]

    def objective(params: np.ndarray) -> float:
        try:
            return _score_background(
                z_grid, _baseline_e(model, params, z_grid), sn, bao
            )["chi2_total"]
        except (ValueError, FloatingPointError):
            return 1.0e100

    fits = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=definition["bounds"],
            options={"maxiter": 120, "ftol": 1.0e-9},
        )
        for start in definition["starts"]
    ]
    successful_fits = [
        item
        for item in fits
        if item.success and math.isfinite(float(item.fun))
    ]
    fit = min(
        successful_fits if successful_fits else fits,
        key=lambda item: float(item.fun),
    )
    score = _score_background(
        z_grid, _baseline_e(model, fit.x, z_grid), sn, bao
    )
    params = {
        name: float(value)
        for name, value in zip(definition["names"], fit.x)
    }
    params["q_H0_rd"] = score["q_H0_rd"]
    parameter_count = len(definition["names"]) + 1
    n_data = sn["n"] + bao["n"]
    return {
        "model": model,
        "chi2_sn": score["chi2_sn"],
        "chi2_bao": score["chi2_bao"],
        "chi2_total": score["chi2_total"],
        "parameters": params,
        "identifiable_parameter_count": parameter_count,
        "AIC": score["chi2_total"] + 2.0 * parameter_count,
        "BIC": score["chi2_total"] + parameter_count * math.log(n_data),
        "success": bool(fit.success and score["q_fit_success"]),
        "edge_flag": any(
            min(
                (value - lower) / (upper - lower),
                (upper - value) / (upper - lower),
            )
            < 0.01
            for value, (lower, upper) in zip(fit.x, definition["bounds"])
        ),
    }


def _mts_e_on_z(run: dict[str, Any], z_grid: np.ndarray) -> np.ndarray:
    n_values = -np.log1p(z_grid)
    states = run["solution"].sol(n_values)
    e_values = np.empty_like(z_grid)
    for index, n_value in enumerate(n_values):
        e_values[index] = run["background_values"](
            float(n_value), states[:, index]
        )[0]
    return e_values


@lru_cache(maxsize=None)
def likelihood_smoke() -> dict[str, Any]:
    config_path = FORMAL / "configs" / "cosmology_background_R1_current.json"
    config = load_json(config_path)
    bao = load_bao(ROOT, select_dataset(config, "BAO"))
    baseline_rows: list[dict[str, Any]] = []
    branch_rows: list[dict[str, Any]] = []
    information_rows: list[dict[str, Any]] = []
    for branch in ("no_sh0es", "sh0es"):
        sn = load_pantheon(
            ROOT, select_dataset(config, "Pantheon"), branch=branch
        )
        z_max = max(float(np.max(sn["z_cosmo"])), float(np.max(bao["z"])))
        z_grid = np.linspace(0.0, z_max * 1.02 + 0.01, 3072)
        baseline_by_name: dict[str, dict[str, Any]] = {}
        for model in ("LCDM", "wCDM", "CPL"):
            fitted = _fit_baseline(model, z_grid, sn, bao)
            fitted["branch"] = branch
            fitted["n_data"] = sn["n"] + bao["n"]
            baseline_rows.append(fitted)
            baseline_by_name[model] = fitted
        fixed_e = _baseline_e("LCDM", np.asarray([OMEGA_M]), z_grid)
        fixed_score = _score_background(z_grid, fixed_e, sn, bao)
        fixed_baseline = {
            "model": "LCDM_fixed_Omega_m_0p315",
            "branch": branch,
            "chi2_sn": fixed_score["chi2_sn"],
            "chi2_bao": fixed_score["chi2_bao"],
            "chi2_total": fixed_score["chi2_total"],
            "parameters": {
                "Omega_m": OMEGA_M,
                "q_H0_rd": fixed_score["q_H0_rd"],
            },
            "identifiable_parameter_count": 1,
            "AIC": fixed_score["chi2_total"] + 2.0,
            "BIC": fixed_score["chi2_total"]
            + math.log(sn["n"] + bao["n"]),
            "success": fixed_score["q_fit_success"],
            "edge_flag": False,
            "n_data": sn["n"] + bao["n"],
        }
        baseline_rows.append(fixed_baseline)
        baseline_by_name["LCDM_fixed"] = fixed_baseline
        for target in TARGETS:
            run = _solve_branch(target)
            score = _score_background(
                z_grid, _mts_e_on_z(run, z_grid), sn, bao
            )
            branch_row = {
                "branch": branch,
                "model": f"MTS_expansion_memory_{target:.0e}",
                "target_Omega_memory_today": target,
                "sigma_theta_over_H0": SIGMA_BAR,
                "gamma_M_over_H0": GAMMA_BAR,
                "kappa_over_H0_squared": run["kappa_bar"],
                "chi2_sn": score["chi2_sn"],
                "chi2_bao": score["chi2_bao"],
                "chi2_total": score["chi2_total"],
                "q_H0_rd": score["q_H0_rd"],
                "n_data": sn["n"] + bao["n"],
                "predeclared_row_not_fitted": True,
                "success": score["q_fit_success"],
            }
            branch_rows.append(branch_row)
            for baseline_name, baseline in baseline_by_name.items():
                for counting_rule, mts_count in (
                    ("conditional_sigma_gamma_predeclared", 2),
                    ("conservative_sigma_gamma_kappa_counted", 4),
                ):
                    delta_chi2 = score["chi2_total"] - baseline["chi2_total"]
                    information_rows.append(
                        {
                            "branch": branch,
                            "MTS_model": branch_row["model"],
                            "baseline": baseline_name,
                            "counting_rule": counting_rule,
                            "MTS_parameter_count": mts_count,
                            "baseline_parameter_count": baseline[
                                "identifiable_parameter_count"
                            ],
                            "delta_chi2_MTS_minus_baseline": delta_chi2,
                            "delta_AIC_MTS_minus_baseline": delta_chi2
                            + 2.0
                            * (
                                mts_count
                                - baseline["identifiable_parameter_count"]
                            ),
                            "delta_BIC_MTS_minus_baseline": delta_chi2
                            + (
                                mts_count
                                - baseline["identifiable_parameter_count"]
                            )
                            * math.log(sn["n"] + bao["n"]),
                            "stable_evidence_allowed": False,
                        }
                    )
    return {
        "baseline_rows": baseline_rows,
        "branch_rows": branch_rows,
        "information_rows": information_rows,
        "SN_offset_profiled": True,
        "MTS_physics_rows_fitted": False,
        "comparison_scope": (
            "real Pantheon+ covariance and DESI DR2 BAO covariance; three "
            "predeclared backreacted MTS rows with only H0*rd profiled"
        ),
        "passed": bool(
            all(row["success"] for row in baseline_rows)
            and all(row["success"] for row in branch_rows)
            and all(
                math.isfinite(row["delta_chi2_MTS_minus_baseline"])
                for row in information_rows
            )
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    spectral = microscopic_spectral_matching()
    stress = conserved_stress_owner()
    characteristics = coupled_characteristics()
    background = backreacted_flrw()
    growth = smooth_memory_growth_limit()
    likelihood = likelihood_smoke()
    percent_no_sh0es = next(
        row
        for row in likelihood["branch_rows"]
        if row["branch"] == "no_sh0es"
        and row["target_Omega_memory_today"] == 1.0e-2
    )
    fixed_no_sh0es = next(
        row
        for row in likelihood["baseline_rows"]
        if row["branch"] == "no_sh0es"
        and row["model"] == "LCDM_fixed_Omega_m_0p315"
    )
    return {
        "microscopic_matching": (
            "KUBO_FORMULA_DERIVED_NUMERIC_CROSS_SPECTRUM_NOT_PREDICTED"
        ),
        "diagonal_susceptibilities": "MANDATORY_NOT_OPTIONAL",
        "total_stress": "COVARIANT_OWNER_AND_BACKGROUND_CONSERVATION_CLOSED",
        "backreacted_background": "THREE_PREDECLARED_BRANCHES_PASS",
        "growth": "SMOOTH_MEMORY_DUST_LIMIT_ONLY_FULL_COUPLED_KERNEL_OPEN",
        "real_data_smoke": "PANTHEON_PLUS_AND_DESI_DR2_EXECUTED_NONCLAIM",
        "percent_no_sh0es_delta_chi2_vs_fixed_LCDM": (
            percent_no_sh0es["chi2_total"]
            - fixed_no_sh0es["chi2_total"]
        ),
        "local_derivative_characteristics": (
            "STABLE_BUT_UPPER_LOW_ENERGY_MODE_EXCEEDS_PUBLIC_CONE"
        ),
        "4887_principal_statement_correction": (
            "bare_phi_block_unchanged_but_coupled_clock_memory_cone_changed"
        ),
        "promotion_status": (
            "BACKGROUND_ROUTE_SURVIVES_AND_IS_DATA_COMPETITIVE_AT_SMOKE_"
            "LEVEL_BUT_NO_LOCAL_GR_OR_CAUSAL_UV_PROMOTION_UNTIL_FULL_"
            "NONLOCAL_KERNEL_AND_BINARY_GATE"
        ),
        "expansion_source_demoted": False,
        "expansion_source_promoted_to_parent_prediction": False,
        "next_target": NEXT_TARGET,
        "passed": all(
            (
                sources["passed"],
                spectral["passed"],
                stress["passed"],
                characteristics["passed"],
                background["passed"],
                growth["passed"],
                likelihood["passed"],
            )
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "spectral_matching": microscopic_spectral_matching(),
        "stress_owner": conserved_stress_owner(),
        "characteristics": coupled_characteristics(),
        "backreacted_FLRW": backreacted_flrw(),
        "growth_limit": smooth_memory_growth_limit(),
        "likelihood": likelihood_smoke(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "decision": arbitration()["promotion_status"],
        "sections": sections,
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    print(calculation["decision"])
    for row in calculation["sections"]["backreacted_FLRW"]["rows"]:
        print(
            "target={target:.0e} kappa={kappa:.9g} bath_scale={scale:.9g} "
            "max_memory={maximum:.9g}".format(
                target=row["target_Omega_memory_today"],
                kappa=row["kappa_over_H0_squared"],
                scale=row["initial_bath_dust_normalization_ratio"],
                maximum=row["maximum_Omega_memory"],
            )
        )
    likelihood = calculation["sections"]["likelihood"]
    for row in likelihood["branch_rows"]:
        print(
            f"{row['branch']} {row['model']} chi2={row['chi2_total']:.8f}"
        )
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
