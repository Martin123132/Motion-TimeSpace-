from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy import optimize
from scipy.integrate import quad, solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel as local_parent  # noqa: E402


CHECKPOINT = "4894"
TARGET = 1.0e-3
LAMBDA_VALUES = (0.1, 0.2, 0.2517166461337078)
NEXT_TARGET = (
    "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-"
    "GR-decoupling-or-bath-cosmology-retirement-gate.md"
)


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
            "SRC4894_00_4893",
            POST
            / "4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-cutoff-selection-or-CMB-likelihood-demotion-gate.md",
            "MTS_IR_CMB_UV_BATH_CUTOFF_GATE_4893",
        ),
        (
            "SRC4894_01_validation",
            OUTPUT / "P8_Y5_BRR545_4893_VALIDATION.csv",
            "VAL4893_OVERALL,PASS",
        ),
        (
            "SRC4894_02_FDT_summary",
            OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv",
            "today_exact_cutoff_limit_at_Theta0p1",
        ),
        (
            "SRC4894_03_spectral_parent",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "Passivity fixes the positivity of the full spectral Gram matrix.",
        ),
        (
            "SRC4894_04_composite_parent",
            POST
            / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md",
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890",
        ),
        (
            "SRC4894_05_local_background",
            OUTPUT / "P8_Y5_R2FR_4890_EARLY_BACKGROUND.csv",
            "kappa_over_H0_squared",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_output_or_parent_derivation",
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
def kernel_and_sum_rules() -> dict[str, Any]:
    gamma_bar = local_parent.background.GAMMA_BAR
    sigma_bar = local_parent.background.SIGMA_BAR
    omega_x = local_parent.background.OMEGA_X
    cutoff_limit = float(
        read_csv(OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv")[0][
            "today_exact_cutoff_limit_at_Theta0p1"
        ]
    )
    rows: list[dict[str, Any]] = []
    for cutoff in (*LAMBDA_VALUES, 0.6, 1.0):
        c_phi_phi = gamma_bar * cutoff / 2.0
        q_cross = sigma_bar / c_phi_phi
        c_theta_theta_min = sigma_bar**2 / c_phi_phi
        friction_at_h0 = 1.0 / (1.0 + (1.0 / cutoff) ** 2) ** 2
        rows.append(
            {
                "cutoff_per_efold": cutoff,
                "C_phi_phi": c_phi_phi,
                "cross_amplitude_q": q_cross,
                "C_phi_theta": sigma_bar,
                "minimum_C_theta_theta": c_theta_theta_min,
                "saturated_static_determinant": (
                    c_phi_phi * c_theta_theta_min - sigma_bar**2
                ),
                "current_parent_zero_C_theta_theta_determinant": -sigma_bar**2,
                "minimum_C_theta_theta_over_3OmegaX": (
                    c_theta_theta_min / (3.0 * omega_x)
                ),
                "friction_fraction_at_omega_H0": friction_at_h0,
                "local_Markov_fractional_error_at_omega_H0": (
                    1.0 - friction_at_h0
                ),
                "inside_exact_FDT_cutoff": cutoff <= cutoff_limit,
                "equal_coupling": abs(q_cross - 1.0) < 1.0e-12,
            }
        )

    def analytic_kernel(time_value: float, cutoff: float) -> float:
        return (
            gamma_bar
            * cutoff
            * (1.0 + cutoff * time_value)
            * math.exp(-cutoff * time_value)
            / 2.0
        )

    normalization_rows: list[dict[str, Any]] = []
    for cutoff in LAMBDA_VALUES:
        integral, _ = quad(
            lambda time_value: analytic_kernel(time_value, cutoff),
            0.0,
            math.inf,
            epsabs=1.0e-12,
            epsrel=1.0e-11,
        )
        for omega in (0.0, 0.1, 1.0, 10.0):
            if omega == 0.0:
                cosine_transform = integral
            else:
                cosine_transform, _ = quad(
                    lambda time_value: analytic_kernel(time_value, cutoff),
                    0.0,
                    math.inf,
                    epsabs=1.0e-11,
                    epsrel=1.0e-9,
                    weight="cos",
                    wvar=omega,
                    limlst=200,
                )
            expected = gamma_bar / (1.0 + (omega / cutoff) ** 2) ** 2
            normalization_rows.append(
                {
                    "cutoff_per_efold": cutoff,
                    "omega_per_efold": omega,
                    "kernel_time_integral": integral,
                    "cosine_transform": cosine_transform,
                    "expected_real_friction": expected,
                    "absolute_transform_residual": abs(
                        cosine_transform - expected
                    ),
                }
            )
    allowed_row = next(
        row
        for row in rows
        if abs(row["cutoff_per_efold"] - cutoff_limit) < 1.0e-12
    )
    equal_coupling_cutoff = 2.0 * sigma_bar / gamma_bar
    return {
        "rows": rows,
        "normalization_rows": normalization_rows,
        "spectral_density": (
            "J_phi_phi(omega)=gamma_bar omega/[1+(omega/Lambda)^2]^2"
        ),
        "causal_memory_kernel": (
            "Gamma_Lambda(t)=gamma_bar Lambda(1+Lambda t)exp(-Lambda t)/2"
        ),
        "auxiliary_localization": (
            "r1_dot=phi_dot-Lambda r1; r2_dot=Lambda(r1-r2); "
            "F_mem=gamma_bar Lambda(r1+r2)/2"
        ),
        "static_sum_rules": (
            "C_phi_phi=gamma_bar Lambda/2; C_phi_theta=sigma_bar; "
            "C_theta_theta>=2 sigma_bar^2/(gamma_bar Lambda)"
        ),
        "rank_one_saturation": (
            "J_AB=J_phi_phi (1,q)_A(1,q)_B with "
            "q=2 sigma_bar/(gamma_bar Lambda)"
        ),
        "cutoff_limit": cutoff_limit,
        "equal_coupling_cutoff": equal_coupling_cutoff,
        "allowed_cutoff_C_phi_phi": allowed_row["C_phi_phi"],
        "allowed_cutoff_q": allowed_row["cross_amplitude_q"],
        "allowed_cutoff_minimum_C_theta_theta": allowed_row[
            "minimum_C_theta_theta"
        ],
        "allowed_cutoff_minimum_C_theta_theta_over_3OmegaX": allowed_row[
            "minimum_C_theta_theta_over_3OmegaX"
        ],
        "allowed_cutoff_friction_fraction_at_H0": allowed_row[
            "friction_fraction_at_omega_H0"
        ],
        "current_parent_has_reciprocal_theta_theta_kernel": False,
        "current_parent_has_diagonal_counterterm_rule": False,
        "current_parent_is_full_positive_spectral_matrix": False,
        "current_parent_static_spectral_determinant_if_Ctheta_theta_zero": (
            -sigma_bar**2
        ),
        "completed_rank_one_spectral_eigenvalues_at_cutoff": (
            0.0,
            allowed_row["C_phi_phi"]
            + allowed_row["minimum_C_theta_theta"],
        ),
        "passed": bool(
            max(
                row["absolute_transform_residual"]
                for row in normalization_rows
            )
            < 1.0e-9
            and abs(equal_coupling_cutoff - 0.6) < 1.0e-12
            and allowed_row["minimum_C_theta_theta"] > 0.7
            and allowed_row["local_Markov_fractional_error_at_omega_H0"]
            > 0.99
            and abs(allowed_row["saturated_static_determinant"]) < 1.0e-14
            and -0.091
            < allowed_row["current_parent_zero_C_theta_theta_determinant"]
            < -0.089
        ),
    }


def one_sided_nonlocal_integrator(
    cutoff: float, log_kappa: float, log_clock_scale: float
) -> dict[str, Any]:
    kappa_bar = math.exp(log_kappa)
    clock_scale = math.exp(log_clock_scale)
    omega_lambda = (
        1.0
        - local_parent.background.OMEGA_R
        - local_parent.background.OMEGA_M
        - TARGET
    )
    initial_clock = local_parent.background.OMEGA_X * math.exp(
        -3.0 * local_parent.EARLY_INITIAL_N + log_clock_scale
    )

    def background_values(
        n_value: float, state: np.ndarray
    ) -> dict[str, float]:
        field, field_n, clock_density, memory_1, memory_2 = state
        radiation = local_parent.background.OMEGA_R * math.exp(-4.0 * n_value)
        other_matter = local_parent.background.OMEGA_OTHER_M * math.exp(
            -3.0 * n_value
        )
        potential = kappa_bar * field**4 / 12.0
        denominator = 1.0 - field_n**2 / 6.0
        numerator = (
            radiation
            + other_matter
            + omega_lambda
            + clock_density
            + potential
        )
        if denominator <= 0.0 or numerator <= 0.0:
            raise ValueError("non-positive one-sided nonlocal branch")
        e_squared = numerator / denominator
        e_value = math.sqrt(e_squared)
        h_value = (
            -2.0 * radiation / e_squared
            - 1.5 * (other_matter + clock_density) / e_squared
            - 0.5 * field_n**2
            + local_parent.background.SIGMA_BAR
            * field_n
            / (2.0 * e_value)
        )
        friction = (
            local_parent.background.GAMMA_BAR
            * cutoff
            * (memory_1 + memory_2)
            / 2.0
        )
        return {
            "E": e_value,
            "h": h_value,
            "radiation": radiation,
            "other_matter": other_matter,
            "potential": potential,
            "friction_over_H0_squared": friction,
        }

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        field, field_n, clock_density, memory_1, memory_2 = state
        local = background_values(n_value, state)
        e_value = local["E"]
        friction = local["friction_over_H0_squared"]
        return np.asarray(
            [
                field_n,
                -(3.0 + local["h"]) * field_n
                - kappa_bar * field**3 / e_value**2
                + 3.0 * local_parent.background.SIGMA_BAR / e_value
                - friction / e_value**2,
                -3.0 * clock_density + friction * field_n / 3.0,
                field_n - cutoff * memory_1 / e_value,
                cutoff * (memory_1 - memory_2) / e_value,
            ]
        )

    solution = solve_ivp(
        rhs,
        (local_parent.EARLY_INITIAL_N, 0.0),
        np.asarray([0.0, 0.0, initial_clock, 0.0, 0.0]),
        method="DOP853",
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"one-sided nonlocal background failed at {cutoff}")
    final = solution.y[:, -1]
    local = background_values(0.0, final)
    memory_fraction = (
        local["E"] ** 2 * final[1] ** 2 / 6.0 + local["potential"]
    ) / local["E"] ** 2
    return {
        "cutoff": cutoff,
        "kappa_bar": kappa_bar,
        "clock_scale": clock_scale,
        "omega_lambda": omega_lambda,
        "solution": solution,
        "background_values": background_values,
        "rhs": rhs,
        "memory_today": float(memory_fraction),
        "clock_today": float(final[2]),
        "E_today": float(local["E"]),
        "friction_today": float(local["friction_over_H0_squared"]),
        "memory_1_today": float(final[3]),
        "memory_2_today": float(final[4]),
    }


@lru_cache(maxsize=None)
def one_sided_background_diagnostic() -> dict[str, Any]:
    local_row = next(
        row
        for row in read_csv(OUTPUT / "P8_Y5_R2FR_4890_EARLY_BACKGROUND.csv")
        if float(row["target"]) == TARGET
    )
    local_kappa = float(local_row["kappa_over_H0_squared"])
    local_clock_scale = float(local_row["clock_initial_scale"])
    local_run = local_parent._early_branch_integrator(
        TARGET, math.log(local_kappa), math.log(local_clock_scale)
    )
    rows: list[dict[str, Any]] = []
    background_rows: list[dict[str, Any]] = []
    runs: dict[float, dict[str, Any]] = {}
    for cutoff in LAMBDA_VALUES:
        def residual(vector: np.ndarray) -> np.ndarray:
            run = one_sided_nonlocal_integrator(
                cutoff, float(vector[0]), float(vector[1])
            )
            return np.asarray(
                [
                    math.log(run["memory_today"] / TARGET),
                    math.log(
                        run["clock_today"] / local_parent.background.OMEGA_X
                    ),
                ]
            )

        root = optimize.root(
            residual,
            np.asarray([math.log(local_kappa), math.log(local_clock_scale)]),
            method="hybr",
            tol=1.0e-10,
        )
        if not root.success:
            raise RuntimeError(
                f"one-sided nonlocal shooting failed at {cutoff}: {root.message}"
            )
        run = one_sided_nonlocal_integrator(
            cutoff, float(root.x[0]), float(root.x[1])
        )
        runs[cutoff] = run
        n_values = np.linspace(-math.log(101.0), 0.0, 701)
        fractional_e_shifts: list[float] = []
        for n_value in n_values:
            state = run["solution"].sol(float(n_value))
            local_state = local_run["solution"].sol(float(n_value))
            e_nonlocal = run["background_values"](
                float(n_value), state
            )["E"]
            e_local = local_run["background_values"](
                float(n_value), local_state
            )[0]
            fractional_e_shifts.append(e_nonlocal / e_local - 1.0)
        rows.append(
            {
                "cutoff_per_efold": cutoff,
                "shooting_success": bool(root.success),
                "shooting_residual_norm": float(
                    np.linalg.norm(residual(root.x), ord=np.inf)
                ),
                "kappa_over_H0_squared": run["kappa_bar"],
                "kappa_ratio_to_local": run["kappa_bar"] / local_kappa,
                "clock_initial_scale": run["clock_scale"],
                "memory_today": run["memory_today"],
                "clock_today": run["clock_today"],
                "E_today": run["E_today"],
                "friction_today_over_H0_squared": run["friction_today"],
                "maximum_abs_fractional_E_shift_vs_local": max(
                    abs(value) for value in fractional_e_shifts
                ),
            }
        )
        for redshift in (100.0, 30.0, 10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.0):
            n_value = -math.log1p(redshift)
            state = run["solution"].sol(n_value)
            local = run["background_values"](n_value, state)
            background_rows.append(
                {
                    "cutoff_per_efold": cutoff,
                    "redshift": redshift,
                    "N": n_value,
                    "E": local["E"],
                    "field": float(state[0]),
                    "field_N": float(state[1]),
                    "clock_density": float(state[2]),
                    "memory_1": float(state[3]),
                    "memory_2": float(state[4]),
                    "friction_over_H0_squared": local[
                        "friction_over_H0_squared"
                    ],
                }
            )
    return {
        "rows": rows,
        "background_rows": background_rows,
        "runs": runs,
        "closure_label": (
            "one_sided_auto_memory_only_with_local_sigma_cross_source_and_no_"
            "reciprocal_theta_theta_kernel_or_bath_stress"
        ),
        "variationally_complete": False,
        "usable_for_parent_prediction": False,
        "passed": bool(
            all(
                row["shooting_success"]
                and row["shooting_residual_norm"] < 1.0e-8
                and abs(row["memory_today"] - TARGET) < 1.0e-10
                and abs(
                    row["clock_today"] - local_parent.background.OMEGA_X
                )
                < 1.0e-10
                and abs(row["E_today"] - 1.0) < 1.0e-9
                for row in rows
            )
            and not background_rows == []
        ),
    }


@lru_cache(maxsize=None)
def variational_completion_audit() -> dict[str, Any]:
    kernel = kernel_and_sum_rules()
    background = one_sided_background_diagnostic()
    requirements = [
        {
            "requirement": "causal_retarded_auto_kernel",
            "status": "derived_and_two_auxiliary_localization_verified",
            "closed": True,
        },
        {
            "requirement": "gamma_sigma_common_spectral_matrix",
            "status": "rank_one_positive_saturation_constructed_at_sum_rule_level",
            "closed": True,
        },
        {
            "requirement": "reciprocal_theta_theta_kernel",
            "status": "compulsory_minimum_derived_but_absent_from_current_parent",
            "closed": False,
        },
        {
            "requirement": "diagonal_counterterm_rule",
            "status": "absent_large_induced_compression_term_cannot_be_silently_subtracted",
            "closed": False,
        },
        {
            "requirement": "covariant_bath_stress_in_Einstein_equations",
            "status": "not_present_in_two_auxiliary_response_only_localization",
            "closed": False,
        },
        {
            "requirement": "nonlocal_background_smoke",
            "status": "three_one_sided_reshoots_run_but_not_parent_predictions",
            "closed": True,
        },
        {
            "requirement": "nonlocal_high_k_constraint_system",
            "status": "not_allowed_until_reciprocal_kernel_and_stress_are_varied",
            "closed": False,
        },
        {
            "requirement": "self_consistent_nonlocal_FDT_covariance",
            "status": "not_allowed_until_same_completed_kernel_defines_response_and_noise",
            "closed": False,
        },
    ]
    return {
        "requirements": requirements,
        "closed_requirements": sum(row["closed"] for row in requirements),
        "total_requirements": len(requirements),
        "exact_obstruction": (
            "FDT_cutoff_requires_Lambda<=0.2517166_while_positive_gamma_sigma_"
            "spectral_matching_requires_Ctheta_theta>=0.71508_and_the_current_"
            "parent_contains_neither_that_reciprocal_kernel_nor_a_counterterm_rule"
        ),
        "Markov_conflict": (
            "at_the_allowed_cutoff_only_about_0.355_percent_of_the_nominal_"
            "gamma_remains_at_omega_equals_H0"
        ),
        "one_sided_background_status": (
            "numerically_shootable_but_nonvariational_and_not_eligible_for_"
            "Einstein_Boltzmann_or_likelihood_use"
        ),
        "current_cosmology_source_status": (
            "DEMOTED_TO_PHENOMENOLOGICAL_CLOSURE_PENDING_FULL_2X2_KERNEL_"
            "COUNTERTERMS_AND_BATH_STRESS"
        ),
        "local_stationary_correspondence_status": (
            "UNCHANGED_THE_OBSTRUCTION_IS_IN_THE_COSMOLOGICAL_BATH_SOURCE"
        ),
        "same_kernel_response_and_noise_compilable": False,
        "FDT_covariance_status": (
            "BLOCKED_BY_ABSENT_RECIPROCAL_KERNEL_COUNTERTERM_RULE_AND_BATH_STRESS"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            kernel["passed"]
            and background["passed"]
            and sum(row["closed"] for row in requirements) == 3
            and not all(row["closed"] for row in requirements)
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "kernel": kernel_and_sum_rules(),
        "background": one_sided_background_diagnostic(),
        "audit": variational_completion_audit(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "decision": sections["audit"]["current_cosmology_source_status"],
        "sections": sections,
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    kernel = calculation["sections"]["kernel"]
    background = calculation["sections"]["background"]
    print(
        "Lambda_max={:.9f} q={:.6f} Ctheta_min={:.6f} friction_H0={:.6e}".format(
            kernel["cutoff_limit"],
            kernel["allowed_cutoff_q"],
            kernel["allowed_cutoff_minimum_C_theta_theta"],
            kernel["allowed_cutoff_friction_fraction_at_H0"],
        )
    )
    for row in background["rows"]:
        print(
            "Lambda={:.6f} kappa_ratio={:.6e} max_dE={:.6e}".format(
                row["cutoff_per_efold"],
                row["kappa_ratio_to_local"],
                row["maximum_abs_fractional_E_shift_vs_local"],
            )
        )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
