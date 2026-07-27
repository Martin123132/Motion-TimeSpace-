from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
DEFAULT_OUTPUT = POST / "source-intake" / "mts_residuals"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def exponential_kernel(value: float) -> tuple[float, float, float]:
    exponential = math.exp(-value)
    return -math.expm1(-value), exponential, -exponential


def tanh_kernel(value: float) -> tuple[float, float, float]:
    function = math.tanh(value)
    derivative = 1.0 / math.cosh(value) ** 2
    return function, derivative, -2.0 * function * derivative


KERNELS: dict[str, Callable[[float], tuple[float, float, float]]] = {
    "positive_branch_exponential": exponential_kernel,
    "global_tanh": tanh_kernel,
}


def density_factor(kernel: Callable[[float], tuple[float, float, float]], value: float) -> float:
    function, derivative, _ = kernel(value)
    return function - 3.0 * value * derivative


def positive_density_root(kernel: Callable[[float], tuple[float, float, float]]) -> float:
    lower = 1.0e-8
    upper = 1.0
    while density_factor(kernel, upper) <= 0.0:
        upper *= 2.0
        if upper > 128.0:
            raise RuntimeError("positive density root was not bracketed")
    for _ in range(160):
        midpoint = 0.5 * (lower + upper)
        if density_factor(kernel, midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    return 0.5 * (lower + upper)


def source_rows(timestamp: str) -> list[dict[str, object]]:
    sources = [
        (
            "SRC4846_00_4845",
            POST / "4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md",
            "LST4845_7_cosmology",
            "response-doublet local theorem and cosmology handoff",
        ),
        (
            "SRC4846_01_275",
            POST / "275-JC-three-form-memory-current-from-Q.md",
            "det(X I + S)",
            "three-dimensional determinant origin and shear counterexample",
        ),
        (
            "SRC4846_02_53",
            POST / "53-coherent-projection-local-silence-gate.md",
            "P_coh[Theta]",
            "coherent volume-load projection",
        ),
        (
            "SRC4846_03_316",
            POST / "316-FLRW-memory-projection-amplitude-contract.md",
            "F(N) = 1 - exp",
            "existing cubic FLRW endpoint contract",
        ),
        (
            "SRC4846_04_407",
            ROOT / "formalization-workbench" / "407-PPC4161-transition-electric-U-parent-sector-or-static-time-silence-proof.md",
            "u^mu = tau_obs^mu",
            "MTS-native observed-time flow candidate",
        ),
        (
            "SRC4846_05_4844",
            POST / "4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md",
            "Sigma_Gamma",
            "correct Gamma metric variation and Newton source",
        ),
        (
            "SRC4846_06_runner",
            Path(__file__).resolve(),
            "def flrw_rows",
            "executable endpoint, local and FLRW calculations",
        ),
        (
            "SRC4846_07_checkpoint",
            POST / "4846-Y5-R2FR-response-doublet-cosmology-local-source-split-or-first-real-SigmaGamma-arena-row.md",
            "ANALYTIC_ODD_RESPONSE_CUBIC_NO_GO_PROVED",
            "human-readable derivation checkpoint",
        ),
        (
            "SRC4846_08_formal",
            ROOT / "formalization-workbench" / "862-PPC4161-response-doublet-cosmology-local-source-split-and-coherent-load-action.md",
            "PRIVATE_SAME_ACTION_LOCAL_ZERO_FLRW_ACTIVE",
            "formal-workbench integration",
        ),
        (
            "SRC4846_09_generator",
            POST / "scripts" / "Y5_R2FR_4846_response_doublet_cosmology_local_source_split_or_first_real_SigmaGamma_arena_row.py",
            'CHECKPOINT = "4846"',
            "checkpoint validator",
        ),
    ]
    rows = []
    for source_id, path, needle, role in sources:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def obstruction_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "EPO4846_0_analytic_odd_linear",
            "carrier": "exchange-odd Z(s)",
            "carrier_leading_power": 1,
            "density_symmetry": "analytic exchange-even Gamma_Z",
            "density_leading_power": 2,
            "target_power": 3,
            "cubic_endpoint_possible": False,
            "status": "PROVED_ANALYTIC_PARITY_OBSTRUCTION",
            "reason": "an even analytic density contains Z^(2n), so a linear odd carrier starts at s^2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "EPO4846_1_analytic_odd_cubic",
            "carrier": "exchange-odd Z(s)",
            "carrier_leading_power": 3,
            "density_symmetry": "analytic exchange-even Gamma_Z",
            "density_leading_power": 6,
            "target_power": 3,
            "cubic_endpoint_possible": False,
            "status": "PROVED_ANALYTIC_PARITY_OBSTRUCTION",
            "reason": "raising the analytic odd carrier order moves the even density to s^6, not s^3",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "EPO4846_2_nonanalytic_escape",
            "carrier": "Z proportional s^(3/2)",
            "carrier_leading_power": 1.5,
            "density_symmetry": "quadratic Gamma_Z",
            "density_leading_power": 3,
            "target_power": 3,
            "cubic_endpoint_possible": True,
            "status": "REJECTED_NONANALYTIC_ORIGIN_ESCAPE",
            "reason": "it obtains the target only by losing an analytic regular expansion at the local origin",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "EPO4846_3_even_load_determinant",
            "carrier": "exchange-even spatial Q",
            "carrier_leading_power": 1,
            "density_symmetry": "I_Q=det_3(Q)",
            "density_leading_power": 3,
            "target_power": 3,
            "cubic_endpoint_possible": True,
            "status": "CUBIC_ENDPOINT_DERIVED_FROM_SPATIAL_DETERMINANT",
            "reason": "Q is unchanged by response exchange, while a three-dimensional determinant is cubic algebraically",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "action_id": "CLA4846_0_fields",
            "object": "response decomposition",
            "formula": "R_+=Q+Z; R_-=Q-Z; Q exchange-even; Z exchange-odd",
            "derivation_status": "ALGEBRAIC_DECOMPOSITION",
            "meaning": "cosmological volume load and local odd response are no longer forced into one parity channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CLA4846_1_spatial_geometry",
            "object": "observed-time spatial bundle",
            "formula": "u=tau_obs/sqrt(-g(tau_obs,tau_obs)); h=delta+u tensor u; theta=nabla.u; hQh=Q",
            "derivation_status": "CONDITIONAL_ON_PARENT_TAU_LOCK",
            "meaning": "uses the same source/clock/orbit coframe candidate rather than a fitted cosmology frame",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CLA4846_2_determinant",
            "object": "covariant spatial determinant",
            "formula": "I_Q=((Tr_h Q)^3-3 Tr_h Q Tr_h(Q^2)+2 Tr_h(Q^3))/6",
            "derivation_status": "EXACT_THREE_DIMENSIONAL_IDENTITY",
            "meaning": "on Q=s h, I_Q=s^3",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CLA4846_3_constraint",
            "object": "local coherent-load constraint",
            "formula": "C_Q=Q-(ell_Q theta/3)h; Gamma_mem=Gamma_* F(I_Q)+Lambda:C_Q",
            "derivation_status": "PRIVATE_PARENT_ACTION_CANDIDATE",
            "meaning": "the isotropic volume projector is imposed variationally and its multiplier stress is retained",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CLA4846_4_auxiliary_equations",
            "object": "Q and Lambda Euler equations",
            "formula": "Q=(ell_Q theta/3)h; Lambda=-Gamma_* F'(I_Q) Cof_h(Q)",
            "derivation_status": "EXACT_AUXILIARY_VARIATION",
            "meaning": "Lambda is O(theta^2), so it cannot be dropped from the metric/flow variation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CLA4846_5_combined_density",
            "object": "same-action Gamma carrier",
            "formula": "Gamma_eff=Gamma0+Gamma_mem[Q,Lambda,u]+Gamma_Z[Z]",
            "derivation_status": "PRIVATE_COMBINED_ACTION_CANDIDATE",
            "meaning": "Q carries coherent cosmology; the positive Z action from 4845 carries odd local deviations",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def branch_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BR4846_0_live_parent_unsigned",
            "branch": "global MTS parent adoption",
            "u_tau_parent_owned": False,
            "same_action_local_flrw": False,
            "stationary_killing_theta_zero": False,
            "Q_constraint_varied": False,
            "multiplier_stress_retained": False,
            "Z_local_theorem_available": True,
            "local_active_zero": False,
            "flrw_active": False,
            "status": "BLOCKED_GLOBAL_PARENT_ADOPTION",
            "remaining": "tau/coframe parent lock; ell_Q and Gamma_* origin; full covariant stress; cosmology refit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "branch_id": "BR4846_1_private_stationary_local",
            "branch": "normalized stationary Killing flow with auxiliary Q and positive Z",
            "u_tau_parent_owned": "conditional",
            "same_action_local_flrw": True,
            "stationary_killing_theta_zero": True,
            "Q_constraint_varied": True,
            "multiplier_stress_retained": True,
            "Z_local_theorem_available": True,
            "local_active_zero": True,
            "flrw_active": True,
            "status": "SAME_ACTION_LOCAL_ZERO_FLRW_ACTIVE_PRIVATE_THEOREM",
            "remaining": "parent tau lock and coefficient origin prevent promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "branch_id": "BR4846_2_nonstationary_local",
            "branch": "finite local expansion or tau non-Killing residual",
            "u_tau_parent_owned": "conditional",
            "same_action_local_flrw": True,
            "stationary_killing_theta_zero": False,
            "Q_constraint_varied": True,
            "multiplier_stress_retained": True,
            "Z_local_theorem_available": True,
            "local_active_zero": False,
            "flrw_active": True,
            "status": "FINITE_THETA_RESIDUAL_REQUIRES_PPN_CLOCK_ORBITAL_BOUND",
            "remaining": "source theta profile and ell_Q/Gamma_* response projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "branch_id": "BR4846_3_forbidden_hand_switch",
            "branch": "set Q=0 locally and Q nonzero in FLRW without one constraint",
            "u_tau_parent_owned": False,
            "same_action_local_flrw": False,
            "stationary_killing_theta_zero": False,
            "Q_constraint_varied": False,
            "multiplier_stress_retained": False,
            "Z_local_theorem_available": False,
            "local_active_zero": False,
            "flrw_active": False,
            "status": "FAILED_ENVIRONMENT_SWITCH_CONTROL",
            "remaining": "forbidden route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def local_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for kernel_name, kernel in KERNELS.items():
        for scalar in (0.0, 1.0e-6, 1.0e-3, 0.1):
            invariant = scalar**3
            function, derivative, _ = kernel(invariant)
            response_s = 3.0 * scalar**2 * derivative
            rows.append(
                {
                    "row_id": f"LOC4846_{kernel_name}_{scalar:.0e}",
                    "kernel": kernel_name,
                    "s_ell_theta_over_3": f"{scalar:.16e}",
                    "I_Q": f"{invariant:.16e}",
                    "Gamma_mem_over_Gamma_star": f"{function:.16e}",
                    "dGamma_ds_over_Gamma_star": f"{response_s:.16e}",
                    "local_action_order": 3,
                    "local_field_response_order": 2,
                    "exact_static_zero": scalar == 0.0 and function == 0.0 and response_s == 0.0,
                    "status": "EXACT_STATIC_ZERO" if scalar == 0.0 else "FINITE_CUBIC_ACTION_QUADRATIC_RESPONSE_SMOKE",
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                }
            )
    return rows


def flrw_rows(timestamp: str, epsilon_h: float) -> list[dict[str, object]]:
    rows = []
    for kernel_name, kernel in KERNELS.items():
        root = positive_density_root(kernel)
        sample_values = (1.0e-6, 0.1, 1.0, root, 3.0)
        for value in sample_values:
            function, derivative, second = kernel(value)
            rho_factor = function - 3.0 * value * derivative
            pressure_factor = (
                -function
                + 3.0 * value * derivative
                + value * epsilon_h * (2.0 * derivative + 3.0 * value * second)
            )
            rho_time_derivative_over_Gamma_star_H = (
                3.0 * value * epsilon_h * (-2.0 * derivative - 3.0 * value * second)
            )
            continuity_residual = (
                rho_time_derivative_over_Gamma_star_H
                + 3.0 * (rho_factor + pressure_factor)
            )
            equation_of_state = pressure_factor / rho_factor if abs(rho_factor) > 1.0e-13 else math.nan
            rows.append(
                {
                    "row_id": f"FLRW4846_{kernel_name}_{value:.8e}",
                    "kernel": kernel_name,
                    "y_ellH_cubed": f"{value:.16e}",
                    "ellH": f"{value ** (1.0 / 3.0):.16e}",
                    "epsilon_H_dotH_over_H2": f"{epsilon_h:.16e}",
                    "F": f"{function:.16e}",
                    "F_prime": f"{derivative:.16e}",
                    "kappa_rho_over_Gamma_star": f"{rho_factor:.16e}",
                    "kappa_p_over_Gamma_star": f"{pressure_factor:.16e}",
                    "continuity_residual_over_Gamma_star_H": f"{continuity_residual:.16e}",
                    "w_effective": "UNDEFINED_AT_RHO_ZERO" if math.isnan(equation_of_state) else f"{equation_of_state:.16e}",
                    "positive_density_root_y": f"{root:.16e}",
                    "rho_sign_for_positive_Gamma_star": "positive" if rho_factor > 1.0e-12 else "negative" if rho_factor < -1.0e-12 else "zero_crossing",
                    "status": "FLRW_MINISUPERSPACE_STRESS_COMPUTED_NONCLAIM",
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                }
            )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4846_0_parity",
            "decision": "do_not_drive_cubic_memory_with_exchange_odd_Z_alone",
            "reason": "analytic exchange-even Z density has even endpoint order",
            "next_action": "retain Z for local response and use exchange-even spatial load Q for cosmology",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4846_1_parent_candidate",
            "decision": "promote_local_auxiliary_volume_load_action_to_lead_private_candidate",
            "reason": "one variational constraint yields Q=0 on stationary Killing flow and Q=ell_Q H h on FLRW",
            "next_action": "derive full covariant Hilbert stress and preferred-frame residual from u/tau variation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4846_2_kernel",
            "decision": "retain_exponential_only_on_expanding_branch_and_test_tanh_global_completion",
            "reason": "1-exp(-I) is unbounded for large negative determinant, while tanh(I) is globally bounded and preserves the cubic endpoint",
            "next_action": "score both H-load kernels against cosmology before selecting one",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4846_3_old_memory",
            "decision": "do_not_claim_existing_N_over_u3_shape_from_new_action",
            "reason": "the local action predicts I_Q=(ell_Q H)^3, not I_M=(N/u3)^3",
            "next_action": "run a nonclaim H-load cosmology fit and compare it directly with the old N-memory branch and LCDM/wCDM/CPL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timestamp", default="2026-07-09T20:30:00+00:00")
    parser.add_argument("--epsilon-h", type=float, default=-0.45)
    arguments = parser.parse_args()

    output = arguments.output_dir
    datasets = {
        "P8_Y5_R2FR_4846_SOURCE_REGISTER.csv": source_rows(arguments.timestamp),
        "P8_Y5_R2FR_4846_ENDPOINT_OBSTRUCTION.csv": obstruction_rows(arguments.timestamp),
        "P8_Y5_R2FR_4846_ACTION_CONSTRUCTION.csv": action_rows(arguments.timestamp),
        "P8_Y5_R2FR_4846_BRANCH_OUTPUT.csv": branch_rows(arguments.timestamp),
        "P8_Y5_R2FR_4846_LOCAL_ENDPOINT_OUTPUT.csv": local_rows(arguments.timestamp),
        "P8_Y5_R2FR_4846_FLRW_STRESS_OUTPUT.csv": flrw_rows(arguments.timestamp, arguments.epsilon_h),
        "P8_Y5_R2FR_4846_DECISION.csv": decision_rows(arguments.timestamp),
    }
    for name, rows in datasets.items():
        write_csv(output / name, rows)

    print("COHERENT_LOAD_AUXILIARY_ACTION_RUNNER_PASS")
    for name, rows in datasets.items():
        print(f"{name}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
