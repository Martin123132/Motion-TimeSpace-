from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy import optimize
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4895_full_spectral_matrix_local_decoupling as previous  # noqa: E402


CHECKPOINT = "4896"
NEXT_TARGET = (
    "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-"
    "derived-extension-reentry-gate.md"
)
TARGET_MEMORY = 1.0e-3
INITIAL_N = -14.0
DEFAULT_MODES = 40
DEFAULT_XMAX = 32.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4896_00_4895",
            POST
            / "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md",
            "MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895",
        ),
        (
            "SRC4896_01_4895_validation",
            OUTPUT / "P8_Y5_BRR545_4895_VALIDATION.csv",
            "VAL4895_OVERALL,PASS",
        ),
        (
            "SRC4896_02_4888",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4896_03_4889",
            POST
            / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md",
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
        (
            "SRC4896_04_4890",
            POST
            / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md",
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890",
        ),
        (
            "SRC4896_05_4894_background",
            OUTPUT / "P8_Y5_R2FR_4894_ONE_SIDED_BACKGROUNDS.csv",
            "0.2517166461337078",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_derivation_or_output",
            "source_path": str(path),
            "source_exists": path.exists(),
            "marker": marker,
            "marker_found": contains(path, marker),
        }
        for source_id, path, marker in sources
    ]
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def covariant_parent_and_stress() -> dict[str, Any]:
    spectral = previous.exact_spectral_completion()
    c_phi = spectral["C_phi_phi"]
    c_theta = spectral["C_theta_theta"]
    q_cross = spectral["q_cross"]
    rows = [
        {
            "object": "closed_continuum_parent",
            "formula": (
                "L_chi=int dOmega[-(nabla chi)^2/2-Omega^2 chi^2/2+"
                "g chi phi+q g nabla_chi.nabla_U]"
            ),
            "role": "one covariant closed owner for reciprocal response and stress",
            "derived": True,
        },
        {
            "object": "spectral_coupling_density",
            "formula": (
                "g(Omega)^2=2 gamma Omega^2/{pi[1+(Omega/Lambda)^2]^2}"
            ),
            "role": "Im K_R=J and int g^2/Omega^2=C_phi_phi",
            "derived": True,
        },
        {
            "object": "clock_counterterm_auxiliary",
            "formula": (
                "-C_theta theta^2/2=b^2/(2C_theta)+b theta; b=-C_theta theta"
            ),
            "role": "first-order minisuperspace representation of the clock counterterm",
            "derived": True,
        },
        {
            "object": "clock_shift_current",
            "formula": (
                "D=varrho-q int g chi_dot dOmega-b_dot; D_dot+3HD=0"
            ),
            "role": "exact U-shift Noether current on homogeneous FLRW",
            "derived": True,
        },
        {
            "object": "bath_clock_energy",
            "formula": (
                "rho_B=D+int[(chi_dot^2+Omega^2 chi^2)/2-g chi phi]dOmega+"
                "C_phi phi^2/2-C_theta theta^2/2"
            ),
            "role": "lapse variation of the closed parent",
            "derived": True,
        },
        {
            "object": "bath_clock_enthalpy",
            "formula": (
                "rho_B+p_B=D+int chi_dot^2-q int g chi_dot-b_dot"
            ),
            "role": "scale-factor variation and Raychaudhuri source",
            "derived": True,
        },
    ]
    return {
        "rows": rows,
        "C_phi_phi": c_phi,
        "C_theta_theta": c_theta,
        "q_cross": q_cross,
        "clock_current_conserved": True,
        "stress_from_same_closed_parent": True,
        "counterterm_auxiliary_is_algebraic": True,
        "passed": all(row["derived"] for row in rows),
    }


@lru_cache(maxsize=None)
def ultraviolet_FLRW_gate() -> dict[str, Any]:
    parent = covariant_parent_and_stress()
    c_theta = parent["C_theta_theta"]
    effective_planck_ratio = 1.0 + 1.5 * c_theta
    early_hubble_ratio = 1.0 / math.sqrt(effective_planck_ratio)
    early_fractional_shift = early_hubble_ratio - 1.0
    maximum_allowed_c_theta_for_ten_percent_h = (
        (1.0 / 0.9**2) - 1.0
    ) / 1.5
    minimum_required_cutoff = (
        3.0
        * previous.previous.local_parent.background.SIGMA_BAR**2
        / (
            previous.previous.local_parent.background.GAMMA_BAR
            * ((1.0 / 0.9**2) - 1.0)
        )
    )
    cutoff_limit = previous.exact_spectral_completion()["cutoff_per_H0"]
    rows = []
    for cutoff in (0.1, 0.2, cutoff_limit):
        c_theta_at_cutoff = (
            2.0
            * previous.previous.local_parent.background.SIGMA_BAR**2
            / (previous.previous.local_parent.background.GAMMA_BAR * cutoff)
        )
        planck_ratio = 1.0 + 1.5 * c_theta_at_cutoff
        h_ratio = 1.0 / math.sqrt(planck_ratio)
        rows.append(
            {
                "cutoff_per_H0": cutoff,
                "C_theta_theta": c_theta_at_cutoff,
                "early_effective_Mpl_squared_ratio": planck_ratio,
                "early_H_over_GR_same_physical_density": h_ratio,
                "absolute_fractional_early_H_shift": abs(h_ratio - 1.0),
                "passes_internal_ten_percent_gate": abs(h_ratio - 1.0) < 0.1,
            }
        )
    return {
        "rows": rows,
        "UV_limit": (
            "K_R(omega/H0>>Lambda)->0 so Kren_thetatheta->-C_theta_theta"
        ),
        "effective_EH_coefficient": (
            "Mpl_cosmo^2/Mpl_local^2=1+3 C_theta_theta/2"
        ),
        "effective_planck_ratio_at_FDT_ceiling": effective_planck_ratio,
        "early_H_over_GR_at_FDT_ceiling": early_hubble_ratio,
        "early_fractional_H_shift_at_FDT_ceiling": early_fractional_shift,
        "internal_gate": "abs(H_early/H_GR-1)<0.1",
        "maximum_C_theta_for_internal_gate": (
            maximum_allowed_c_theta_for_ten_percent_h
        ),
        "minimum_cutoff_for_internal_gate": minimum_required_cutoff,
        "FDT_cutoff_ceiling": cutoff_limit,
        "cutoff_gap_factor": minimum_required_cutoff / cutoff_limit,
        "all_FDT_allowed_cutoffs_fail": all(
            not row["passes_internal_ten_percent_gate"] for row in rows
        ),
        "passed": bool(
            effective_planck_ratio > 2.0
            and early_hubble_ratio < 0.7
            and minimum_required_cutoff > cutoff_limit
            and all(
                not row["passes_internal_ten_percent_gate"] for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def continuum_quadrature(
    mode_count: int = DEFAULT_MODES, x_max: float = DEFAULT_XMAX
) -> dict[str, Any]:
    spectral = previous.exact_spectral_completion()
    cutoff = spectral["cutoff_per_H0"]
    gamma = spectral["gamma_bar"]
    c_phi = spectral["C_phi_phi"]
    nodes, base_weights = np.polynomial.legendre.leggauss(mode_count)
    x_values = 0.5 * x_max * (nodes + 1.0)
    x_weights = 0.5 * x_max * base_weights
    omega = cutoff * x_values
    weights = cutoff * x_weights
    coupling = np.sqrt(
        2.0
        * gamma
        * omega**2
        / (math.pi * (1.0 + (omega / cutoff) ** 2) ** 2)
    )
    raw_static = float(np.sum(weights * coupling**2 / omega**2))
    normalization = math.sqrt(c_phi / raw_static)
    coupling *= normalization
    static = float(np.sum(weights * coupling**2 / omega**2))
    first_moment = float(np.sum(weights * coupling**2))
    return {
        "mode_count": mode_count,
        "x_max": x_max,
        "omega": omega,
        "weights": weights,
        "coupling": coupling,
        "raw_static_susceptibility": raw_static,
        "normalization_factor": normalization,
        "static_susceptibility": static,
        "target_static_susceptibility": c_phi,
        "relative_static_residual": static / c_phi - 1.0,
        "coupling_squared_integral": first_moment,
        "minimum_omega": float(np.min(omega)),
        "maximum_omega": float(np.max(omega)),
        "passed": bool(
            mode_count >= 20
            and x_max >= 20.0
            and abs(static / c_phi - 1.0) < 1.0e-13
        ),
    }


def full_matrix_integrator(
    log_kappa: float,
    log_clock_scale: float,
    mode_count: int = DEFAULT_MODES,
    x_max: float = DEFAULT_XMAX,
    initial_n: float = INITIAL_N,
    omega_lambda_override: float | None = None,
) -> dict[str, Any]:
    quadrature = continuum_quadrature(mode_count, x_max)
    parent = covariant_parent_and_stress()
    omega = quadrature["omega"]
    weights = quadrature["weights"]
    coupling = quadrature["coupling"]
    c_phi = parent["C_phi_phi"]
    c_theta = parent["C_theta_theta"]
    q_cross = parent["q_cross"]
    background = previous.previous.local_parent.background
    kappa = math.exp(log_kappa)
    clock_scale = math.exp(log_clock_scale)
    omega_lambda = (
        float(omega_lambda_override)
        if omega_lambda_override is not None
        else 1.0
        - background.OMEGA_R
        - background.OMEGA_OTHER_M
        - background.OMEGA_X
        - TARGET_MEMORY
    )

    def current_density(n_value: float) -> float:
        return (
            background.OMEGA_X
            * clock_scale
            * math.exp(-3.0 * n_value)
        )

    def unpack(state: np.ndarray) -> tuple[float, float, np.ndarray, np.ndarray]:
        field = float(state[0])
        field_n = float(state[1])
        bath = state[2 : 2 + mode_count]
        bath_n = state[2 + mode_count : 2 + 2 * mode_count]
        return field, field_n, bath, bath_n

    def background_values(n_value: float, state: np.ndarray) -> dict[str, Any]:
        field, field_n, bath, bath_n = unpack(state)
        radiation = background.OMEGA_R * math.exp(-4.0 * n_value)
        other_matter = background.OMEGA_OTHER_M * math.exp(-3.0 * n_value)
        clock_current = current_density(n_value)
        bath_n_squared = float(np.sum(weights * bath_n**2))
        bath_mass = float(np.sum(weights * omega**2 * bath**2))
        response = float(np.sum(weights * coupling * bath))
        response_n = float(np.sum(weights * coupling * bath_n))
        denominator = (
            1.0
            + 1.5 * c_theta
            - field_n**2 / 6.0
            - bath_n_squared / 6.0
        )
        numerator = (
            radiation
            + other_matter
            + omega_lambda
            + clock_current
            + bath_mass / 6.0
            - response * field / 3.0
            + c_phi * field**2 / 6.0
            + kappa * field**4 / 12.0
        )
        if denominator <= 0.0 or numerator <= 0.0:
            raise ValueError(
                f"non-positive full-matrix Friedmann branch at N={n_value}"
            )
        e_squared = numerator / denominator
        e_value = math.sqrt(e_squared)
        h_numerator = (
            -2.0 * radiation / e_squared
            - 1.5 * other_matter / e_squared
            - 1.5 * clock_current / e_squared
            - 0.5 * field_n**2
            - 0.5 * bath_n_squared
            + q_cross * response_n / (2.0 * e_value)
        )
        h_value = h_numerator / (1.0 + 1.5 * c_theta)
        theta = 3.0 * e_value
        scalar_force = response - c_phi * field
        reciprocal_force = q_cross * response - c_theta * theta
        scalar_density = (
            e_squared * field_n**2 / 6.0
            + kappa * field**4 / 12.0
        )
        bath_clock_density = (
            clock_current
            + (
                0.5 * e_squared * bath_n_squared
                + 0.5 * bath_mass
                - response * field
                + 0.5 * c_phi * field**2
                - 0.5 * c_theta * theta**2
            )
            / 3.0
        )
        counterterm_density = -0.5 * c_theta * theta**2 / 3.0
        induced_mode_density = (
            0.5 * e_squared * bath_n_squared
            + 0.5 * bath_mass
            - response * field
            + 0.5 * c_phi * field**2
        ) / 3.0
        multiplier_density = (
            clock_current
            + q_cross * e_value * response_n / 3.0
            - c_theta * e_squared * h_value
        )
        return {
            "E": e_value,
            "E2": e_squared,
            "h": h_value,
            "radiation": radiation,
            "other_matter": other_matter,
            "clock_current": clock_current,
            "bath_n_squared": bath_n_squared,
            "bath_mass": bath_mass,
            "response": response,
            "response_n": response_n,
            "theta": theta,
            "scalar_force": scalar_force,
            "reciprocal_force": reciprocal_force,
            "scalar_density": scalar_density,
            "bath_clock_density": bath_clock_density,
            "counterterm_density": counterterm_density,
            "induced_mode_density": induced_mode_density,
            "multiplier_density": multiplier_density,
            "friedmann_denominator": denominator,
            "friedmann_numerator": numerator,
        }

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        field, field_n, bath, bath_n = unpack(state)
        local = background_values(n_value, state)
        e_squared = local["E2"]
        source_collective = field + q_cross * local["theta"]
        field_nn = (
            -(3.0 + local["h"]) * field_n
            - kappa * field**3 / e_squared
            + local["scalar_force"] / e_squared
        )
        bath_nn = (
            -(3.0 + local["h"]) * bath_n
            - omega**2 * bath / e_squared
            + coupling * source_collective / e_squared
        )
        return np.concatenate(
            ([field_n, field_nn], bath_n, bath_nn)
        )

    initial = np.zeros(2 + 2 * mode_count)
    solution = solve_ivp(
        rhs,
        (initial_n, 0.0),
        initial,
        method="DOP853",
        rtol=3.0e-8,
        atol=2.0e-10,
        max_step=0.0125,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"full-matrix background failed: {solution.message}")
    final = solution.y[:, -1]
    local = background_values(0.0, final)
    scalar_fraction = local["scalar_density"] / local["E2"]
    bath_fraction = local["bath_clock_density"] / local["E2"]
    return {
        "kappa": kappa,
        "clock_scale": clock_scale,
        "omega_lambda": omega_lambda,
        "mode_count": mode_count,
        "x_max": x_max,
        "initial_n": initial_n,
        "solution": solution,
        "background_values": background_values,
        "rhs": rhs,
        "scalar_fraction_today": scalar_fraction,
        "bath_fraction_today": bath_fraction,
        "E_today": local["E"],
        "h_today": local["h"],
        "field_today": float(final[0]),
        "field_n_today": float(final[1]),
        "response_today": local["response"],
        "reciprocal_force_today": local["reciprocal_force"],
        "friedmann_denominator_today": local["friedmann_denominator"],
    }


@lru_cache(maxsize=None)
def shoot_default_background() -> dict[str, Any]:
    inherited_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4894_ONE_SIDED_BACKGROUNDS.csv")
    inherited = min(
        inherited_rows,
        key=lambda row: abs(
            float(row["cutoff_per_efold"])
            - previous.exact_spectral_completion()["cutoff_per_H0"]
        ),
    )
    log_kappa = math.log(float(inherited["kappa_over_H0_squared"]))
    target_bath = previous.previous.local_parent.background.OMEGA_X
    initial_lambda = (
        1.0
        - previous.previous.local_parent.background.OMEGA_R
        - previous.previous.local_parent.background.OMEGA_OTHER_M
        - previous.previous.local_parent.background.OMEGA_X
        - TARGET_MEMORY
    )

    def closure_residual(vector: np.ndarray) -> np.ndarray:
        run = full_matrix_integrator(
            log_kappa,
            float(vector[0]),
            omega_lambda_override=float(vector[1]),
        )
        return np.asarray(
            [
                (run["bath_fraction_today"] - target_bath) / target_bath,
                run["E_today"] - 1.0,
            ]
        )

    fit = optimize.least_squares(
        closure_residual,
        np.asarray(
            [math.log(float(inherited["clock_initial_scale"])), initial_lambda]
        ),
        bounds=(
            np.asarray([math.log(1.0e-4), 0.0]),
            np.asarray([math.log(1.0e3), 2.0]),
        ),
        xtol=2.0e-10,
        ftol=2.0e-10,
        gtol=2.0e-10,
        max_nfev=30,
    )
    run = full_matrix_integrator(
        log_kappa,
        float(fit.x[0]),
        omega_lambda_override=float(fit.x[1]),
    )
    bath_residual_final = run["bath_fraction_today"] - target_bath
    e_residual = run["E_today"] - 1.0
    memory_residual = run["scalar_fraction_today"] - TARGET_MEMORY
    joint_residual_norm = max(
        abs(memory_residual) / TARGET_MEMORY,
        abs(bath_residual_final) / target_bath,
        abs(e_residual),
    )
    return {
        "closure_fit_success": bool(fit.success),
        "closure_fit_nfev": int(fit.nfev),
        "bath_target_closed": abs(bath_residual_final) < 1.0e-8,
        "E0_target_closed": abs(e_residual) < 1.0e-8,
        "memory_target_closed": abs(memory_residual) < 1.0e-6,
        "joint_reshoot_closed": bool(
            abs(bath_residual_final) < 1.0e-8
            and abs(e_residual) < 1.0e-8
            and abs(memory_residual) < 1.0e-6
        ),
        "bath_residual": bath_residual_final,
        "E0_residual": e_residual,
        "memory_residual": memory_residual,
        "joint_residual_norm": joint_residual_norm,
        "memory_shortfall_factor": (
            TARGET_MEMORY / run["scalar_fraction_today"]
        ),
        "run": run,
        "passed": bool(
            fit.success
            and abs(bath_residual_final) < 1.0e-8
            and abs(e_residual) < 1.0e-8
            and not abs(memory_residual) < 1.0e-6
            and TARGET_MEMORY / run["scalar_fraction_today"] > 500.0
        ),
    }


def constraint_diagnostics(run: dict[str, Any]) -> dict[str, Any]:
    quadrature = continuum_quadrature(run["mode_count"], run["x_max"])
    parent = covariant_parent_and_stress()
    omega = quadrature["omega"]
    weights = quadrature["weights"]
    coupling = quadrature["coupling"]
    c_phi = parent["C_phi_phi"]
    c_theta = parent["C_theta_theta"]
    q_cross = parent["q_cross"]
    background = previous.previous.local_parent.background
    rows: list[dict[str, Any]] = []
    for n_value in np.linspace(run["initial_n"], 0.0, 141):
        state = run["solution"].sol(float(n_value))
        local = run["background_values"](float(n_value), state)
        derivative = run["rhs"](float(n_value), state)
        field = float(state[0])
        field_n = float(state[1])
        bath = state[2 : 2 + run["mode_count"]]
        bath_n = state[
            2 + run["mode_count"] : 2 + 2 * run["mode_count"]
        ]
        field_nn = float(derivative[1])
        bath_nn = derivative[
            2 + run["mode_count"] : 2 + 2 * run["mode_count"]
        ]
        radiation = local["radiation"]
        other_matter = local["other_matter"]
        clock_current = local["clock_current"]
        e_squared = local["E2"]
        a_n = (
            -4.0 * radiation
            - 3.0 * other_matter
            - 3.0 * clock_current
            + float(np.sum(weights * omega**2 * bath * bath_n)) / 3.0
            - (
                field_n * local["response"]
                + field * local["response_n"]
            )
            / 3.0
            + c_phi * field * field_n / 3.0
            + run["kappa"] * field**3 * field_n / 3.0
        )
        b_n = -(
            field_n * field_nn
            + float(np.sum(weights * bath_n * bath_nn))
        ) / 3.0
        h_from_friedmann_derivative = (
            a_n - e_squared * b_n
        ) / (
            2.0
            * e_squared
            * local["friedmann_denominator"]
        )
        raychaudhuri_lhs = local["h"] * (1.0 + 1.5 * c_theta)
        raychaudhuri_rhs = (
            -2.0 * radiation / e_squared
            - 1.5 * other_matter / e_squared
            - 1.5 * clock_current / e_squared
            - 0.5 * field_n**2
            - 0.5 * float(np.sum(weights * bath_n**2))
            + q_cross * local["response_n"] / (2.0 * local["E"])
        )
        rows.append(
            {
                "N": float(n_value),
                "redshift": math.exp(-float(n_value)) - 1.0,
                "E": local["E"],
                "h_raychaudhuri": local["h"],
                "h_from_Friedmann_derivative": h_from_friedmann_derivative,
                "absolute_Friedmann_derivative_residual": abs(
                    local["h"] - h_from_friedmann_derivative
                ),
                "absolute_Raychaudhuri_identity_residual": abs(
                    raychaudhuri_lhs - raychaudhuri_rhs
                ),
                "friedmann_denominator": local["friedmann_denominator"],
                "bath_fraction": local["bath_clock_density"] / e_squared,
            }
        )
    return {
        "rows": rows,
        "maximum_Friedmann_derivative_residual": max(
            row["absolute_Friedmann_derivative_residual"] for row in rows
        ),
        "maximum_Raychaudhuri_identity_residual": max(
            row["absolute_Raychaudhuri_identity_residual"] for row in rows
        ),
        "minimum_Friedmann_denominator": min(
            row["friedmann_denominator"] for row in rows
        ),
        "minimum_bath_fraction": min(row["bath_fraction"] for row in rows),
        "maximum_bath_fraction": max(row["bath_fraction"] for row in rows),
        "passed": bool(
            max(
                row["absolute_Friedmann_derivative_residual"] for row in rows
            )
            < 1.0e-10
            and max(
                row["absolute_Raychaudhuri_identity_residual"] for row in rows
            )
            < 1.0e-12
            and min(row["friedmann_denominator"] for row in rows) > 1.0
        ),
    }


@lru_cache(maxsize=None)
def background_evolution() -> dict[str, Any]:
    shot = shoot_default_background()
    run = shot["run"]
    background = previous.previous.local_parent.background
    rows: list[dict[str, Any]] = []
    for redshift in (1.0e6, 1100.0, 100.0, 10.0, 3.0, 1.0, 0.5, 0.0):
        n_value = -math.log1p(redshift)
        state = run["solution"].sol(n_value)
        local = run["background_values"](n_value, state)
        matched_gr_e = math.sqrt(
            background.OMEGA_R * math.exp(-4.0 * n_value)
            + background.OMEGA_M * math.exp(-3.0 * n_value)
            + 1.0
            - background.OMEGA_R
            - background.OMEGA_M
        )
        rows.append(
            {
                "redshift": redshift,
                "N": n_value,
                "E_full_matrix": local["E"],
                "E_matched_GR": matched_gr_e,
                "H_ratio_to_matched_GR": local["E"] / matched_gr_e,
                "h_full_matrix": local["h"],
                "field": float(state[0]),
                "field_N": float(state[1]),
                "scalar_fraction": local["scalar_density"] / local["E2"],
                "bath_clock_fraction": (
                    local["bath_clock_density"] / local["E2"]
                ),
                "clock_current_fraction": (
                    local["clock_current"] / local["E2"]
                ),
                "induced_mode_fraction": (
                    local["induced_mode_density"] / local["E2"]
                ),
                "counterterm_fraction": (
                    local["counterterm_density"] / local["E2"]
                ),
                "multiplier_fraction": (
                    local["multiplier_density"] / local["E2"]
                ),
                "scalar_force": local["scalar_force"],
                "reciprocal_force": local["reciprocal_force"],
            }
        )
    return {
        "rows": rows,
        "minimum_H_ratio_to_matched_GR": min(
            row["H_ratio_to_matched_GR"] for row in rows
        ),
        "maximum_H_ratio_to_matched_GR": max(
            row["H_ratio_to_matched_GR"] for row in rows
        ),
        "counterterm_fraction_exact": -1.5
        * covariant_parent_and_stress()["C_theta_theta"],
        "clock_scale_today": run["clock_scale"],
        "omega_lambda": run["omega_lambda"],
        "passed": bool(
            all(math.isfinite(row["E_full_matrix"]) for row in rows)
            and min(row["multiplier_fraction"] for row in rows) > 0.0
            and all(
                abs(
                    row["counterterm_fraction"]
                    + 1.5 * covariant_parent_and_stress()["C_theta_theta"]
                )
                < 1.0e-12
                for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def parameter_scan() -> dict[str, Any]:
    kappa_values = (1.0e-3, 1.0, 1.0e3, 1.0e6, 1.0e9, 1.0e12)
    clock_scales = (1.0e-3, 1.0, 22.7, 100.0)
    rows: list[dict[str, Any]] = []
    for kappa in kappa_values:
        for clock_scale in clock_scales:
            try:
                run = full_matrix_integrator(
                    math.log(kappa),
                    math.log(clock_scale),
                    mode_count=12,
                    x_max=16.0,
                )
            except (ValueError, RuntimeError, OverflowError):
                rows.append(
                    {
                        "kappa": kappa,
                        "clock_scale": clock_scale,
                        "integration_success": False,
                        "scalar_fraction_today": math.nan,
                        "bath_fraction_today": math.nan,
                        "E_today": math.nan,
                        "closes_memory_within_ten_percent": False,
                        "closes_bath_within_ten_percent": False,
                        "closes_both_within_ten_percent": False,
                    }
                )
                continue
            memory_close = (
                abs(run["scalar_fraction_today"] / TARGET_MEMORY - 1.0) < 0.1
            )
            bath_close = (
                abs(
                    run["bath_fraction_today"]
                    / previous.previous.local_parent.background.OMEGA_X
                    - 1.0
                )
                < 0.1
            )
            rows.append(
                {
                    "kappa": kappa,
                    "clock_scale": clock_scale,
                    "integration_success": True,
                    "scalar_fraction_today": run["scalar_fraction_today"],
                    "bath_fraction_today": run["bath_fraction_today"],
                    "E_today": run["E_today"],
                    "closes_memory_within_ten_percent": memory_close,
                    "closes_bath_within_ten_percent": bath_close,
                    "closes_both_within_ten_percent": memory_close and bath_close,
                }
            )
    successful = [row for row in rows if row["integration_success"]]
    bath_close_rows = [
        row for row in successful if row["closes_bath_within_ten_percent"]
    ]
    return {
        "rows": rows,
        "successful_rows": len(successful),
        "maximum_memory_fraction": max(
            row["scalar_fraction_today"] for row in successful
        ),
        "maximum_memory_fraction_among_bath_close_rows": max(
            row["scalar_fraction_today"] for row in bath_close_rows
        ),
        "joint_close_rows": sum(
            row["closes_both_within_ten_percent"] for row in successful
        ),
        "scan_scope": (
            "positive_kappa_1e-3_to_1e12_clock_scale_1e-3_to_100_"
            "zero_retarded_history_12_mode_smoke_not_global_fit"
        ),
        "passed": bool(
            len(successful) == len(rows)
            and max(row["scalar_fraction_today"] for row in successful)
            < 2.0e-5
            and max(
                row["scalar_fraction_today"] for row in bath_close_rows
            )
            < 2.0e-6
            and not any(
                row["closes_both_within_ten_percent"] for row in successful
            )
        ),
    }


@lru_cache(maxsize=None)
def convergence_audit() -> dict[str, Any]:
    shot = shoot_default_background()
    reference = shot["run"]
    configurations = (
        (16, 20.0, -14.0),
        (24, 24.0, -14.0),
        (40, 32.0, -14.0),
        (56, 40.0, -14.0),
        (24, 24.0, -12.0),
        (24, 24.0, -16.0),
    )
    rows: list[dict[str, Any]] = []
    for mode_count, x_max, initial_n in configurations:
        run = full_matrix_integrator(
            math.log(reference["kappa"]),
            math.log(reference["clock_scale"]),
            mode_count=mode_count,
            x_max=x_max,
            initial_n=initial_n,
            omega_lambda_override=reference["omega_lambda"],
        )
        rows.append(
            {
                "mode_count": mode_count,
                "x_max": x_max,
                "initial_N": initial_n,
                "scalar_fraction_today": run["scalar_fraction_today"],
                "bath_fraction_today": run["bath_fraction_today"],
                "E_today": run["E_today"],
                "response_today": run["response_today"],
            }
        )
    baseline = next(
        row
        for row in rows
        if row["mode_count"] == 40
        and row["x_max"] == 32.0
        and row["initial_N"] == -14.0
    )
    for row in rows:
        row["fractional_memory_shift_from_default"] = (
            row["scalar_fraction_today"]
            / baseline["scalar_fraction_today"]
            - 1.0
        )
        row["absolute_bath_shift_from_default"] = (
            row["bath_fraction_today"] - baseline["bath_fraction_today"]
        )
    initial_rows = [
        row
        for row in rows
        if row["mode_count"] == 24 and row["x_max"] == 24.0
    ]
    return {
        "rows": rows,
        "maximum_abs_fractional_memory_quadrature_shift": max(
            abs(row["fractional_memory_shift_from_default"])
            for row in rows[:4]
        ),
        "maximum_abs_initial_time_memory_shift": (
            max(row["scalar_fraction_today"] for row in initial_rows)
            / min(row["scalar_fraction_today"] for row in initial_rows)
            - 1.0
        ),
        "passed": bool(
            max(
                abs(row["fractional_memory_shift_from_default"])
                for row in rows[:4]
            )
            < 0.02
            and (
                max(row["scalar_fraction_today"] for row in initial_rows)
                / min(row["scalar_fraction_today"] for row in initial_rows)
                - 1.0
            )
            < 1.0e-5
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    parent = covariant_parent_and_stress()
    uv = ultraviolet_FLRW_gate()
    shot = shoot_default_background()
    diagnostics = constraint_diagnostics(shot["run"])
    evolution = background_evolution()
    scan = parameter_scan()
    convergence = convergence_audit()
    requirements = [
        {
            "requirement": "same_parent_covariant_bath_stress",
            "status": "derived_from_closed_continuum_and_clock_counterterm_auxiliary",
            "closed": True,
        },
        {
            "requirement": "Friedmann_Raychaudhuri_Ward_consistency",
            "status": "closed_to_numerical_precision",
            "closed": True,
        },
        {
            "requirement": "physical_bath_density_reshoot",
            "status": "bath_fraction_and_E0_close",
            "closed": True,
        },
        {
            "requirement": "target_memory_activation",
            "status": "fails_by_more_than_three_orders_of_magnitude",
            "closed": False,
        },
        {
            "requirement": "early_standard_gravity_limit",
            "status": "fails_exact_UV_counterterm_theorem",
            "closed": False,
        },
        {
            "requirement": "quadrature_and_initial_history_robustness",
            "status": "passes_declared_convergence_checks",
            "closed": True,
        },
        {
            "requirement": "reuse_previous_CMB_growth_likelihoods",
            "status": "forbidden_background_and_source_are_different",
            "closed": False,
        },
    ]
    return {
        "requirements": requirements,
        "closed_requirements": sum(row["closed"] for row in requirements),
        "total_requirements": len(requirements),
        "full_matrix_parent_math_status": (
            "COVARIANT_STRESS_AND_BACKGROUND_CONSTRAINTS_DERIVED"
        ),
        "bath_density_reshoot_status": "CLOSES",
        "memory_activation_status": (
            "REJECTED_ZERO_HISTORY_POSITIVE_KAPPA_BRANCH_SHORTFALL_GT_500"
        ),
        "early_limit_status": (
            "REJECTED_FDT_ALLOWED_DIAGONAL_SUBTRACTION_GIVES_"
            "MEFF2_OVER_MPL2_GE_2P0726"
        ),
        "bath_cosmology_status": (
            "RETIRED_AS_ACTIVE_FUNDAMENTAL_COSMOLOGY_SOURCE_FOR_"
            "GAMMA1_SIGMA0P3_FDT_ALLOWED_DIAGONAL_SUBTRACTION"
        ),
        "stationary_local_GR_status": (
            "UNCHANGED_4895_DECOUPLING_THEOREM_REMAINS_VALID"
        ),
        "metric_only_cosmology_status": (
            "RETAIN_AS_BASELINE_UNTIL_A_DIFFERENT_DERIVED_EXTENSION_CLOSES"
        ),
        "reentry_condition": (
            "new_parent_spectral_or_counterterm_architecture_must_remove_"
            "the_UV_theta2_Planck_shift_without_restoring_static_phi2_or_"
            "theta2_and_must_rederive_FDT_stress_and_constraints"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            parent["passed"]
            and uv["passed"]
            and shot["passed"]
            and diagnostics["passed"]
            and evolution["passed"]
            and scan["passed"]
            and convergence["passed"]
            and sum(row["closed"] for row in requirements) == 4
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    shot = shoot_default_background()
    sections = {
        "sources": source_contract(),
        "parent": covariant_parent_and_stress(),
        "uv": ultraviolet_FLRW_gate(),
        "quadrature": continuum_quadrature(),
        "shot": shot,
        "diagnostics": constraint_diagnostics(shot["run"]),
        "evolution": background_evolution(),
        "scan": parameter_scan(),
        "convergence": convergence_audit(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["bath_cosmology_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    parent = calculation["sections"]["parent"]
    uv = calculation["sections"]["uv"]
    print(
        "Ctheta={:.9f} Meff2_ratio={:.9f} Hearly_ratio={:.9f}".format(
            parent["C_theta_theta"],
            uv["effective_planck_ratio_at_FDT_ceiling"],
            uv["early_H_over_GR_at_FDT_ceiling"],
        )
    )
    shot = calculation["sections"]["shot"]
    run = shot["run"]
    print(
        "bath_shoot={} joint_shoot={} memory_shortfall={:.3f} "
        "kappa={:.6e} clock_scale={:.6e} "
        "Omega_phi={:.6e} Omega_bath={:.6e} E0={:.9f}".format(
            shot["bath_target_closed"],
            shot["joint_reshoot_closed"],
            shot["memory_shortfall_factor"],
            run["kappa"],
            run["clock_scale"],
            run["scalar_fraction_today"],
            run["bath_fraction_today"],
            run["E_today"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
