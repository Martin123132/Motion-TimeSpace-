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
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
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


def bisect_positive_root(function: Callable[[float], float], lower: float, upper: float) -> float:
    lower_value = function(lower)
    upper_value = function(upper)
    while lower_value * upper_value > 0.0:
        upper *= 2.0
        upper_value = function(upper)
        if upper > 256.0:
            raise RuntimeError("failed to bracket positive root")
    for _ in range(180):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = function(midpoint)
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
    return 0.5 * (lower + upper)


def density_root(kernel: Callable[[float], tuple[float, float, float]]) -> float:
    return bisect_positive_root(
        lambda value: kernel(value)[0] - 3.0 * value * kernel(value)[1],
        1.0e-9,
        1.0,
    )


def hessian_root(kernel: Callable[[float], tuple[float, float, float]]) -> float:
    return bisect_positive_root(
        lambda value: 2.0 * kernel(value)[1] + 3.0 * value * kernel(value)[2],
        1.0e-9,
        1.0,
    )


def source_rows(timestamp: str) -> list[dict[str, object]]:
    sources = [
        (
            "SRC4847_00_4846",
            POST / "4846-Y5-R2FR-response-doublet-cosmology-local-source-split-or-first-real-SigmaGamma-arena-row.md",
            "Auxiliary coherent-load action",
            "Q/Lambda action and FLRW reduction",
        ),
        (
            "SRC4847_01_4845",
            POST / "4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md",
            "Local zero theorem",
            "positive Z-sector stationary theorem",
        ),
        (
            "SRC4847_02_tau",
            ROOT / "formalization-workbench" / "407-PPC4161-transition-electric-U-parent-sector-or-static-time-silence-proof.md",
            "u^mu = tau_obs^mu",
            "observed-time flow candidate",
        ),
        (
            "SRC4847_03_runner",
            Path(__file__).resolve(),
            "def stress_rows",
            "covariant stress and viability calculations",
        ),
        (
            "SRC4847_04_checkpoint",
            POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md",
            "COVARIANT_COHERENT_LOAD_HILBERT_STRESS_DERIVED",
            "human-readable covariant derivation",
        ),
        (
            "SRC4847_05_formal",
            ROOT / "formalization-workbench" / "863-PPC4161-coherent-load-covariant-Hilbert-stress-tau-Euler-and-stability-window.md",
            "COHERENT_LOAD_COVARIANT_STRESS_AND_STABILITY_WINDOW",
            "formal-workbench integration",
        ),
        (
            "SRC4847_06_validator",
            POST / "scripts" / "Y5_R2FR_4847_coherent_load_covariant_Hilbert_stress_and_tau_Euler_equation.py",
            'CHECKPOINT = "4847"',
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


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "CHS4847_0_action",
            "unit-flow reduced action",
            "S_mem=-(1/kappa) int sqrt(-g)[G(theta)+lambda_u(u.u+1)]",
            "G(theta)=Gamma_* F[(ell_Q theta/3)^3]",
        ),
        (
            "CHS4847_1_u_euler",
            "unit-flow Euler equation",
            "nabla_mu G_theta=2 lambda_u u_mu; lambda_u=-dot(G_theta)/2",
            "spatial projection D_mu G_theta=0",
        ),
        (
            "CHS4847_2_stress",
            "covariant Hilbert stress",
            "kappa T_mn=[nabla_a(G_theta u^a)-G]g_mn+dot(G_theta)u_m u_n",
            "includes normalization multiplier and agrees with lapse/scale variation",
        ),
        (
            "CHS4847_3_fluid",
            "perfect-fluid decomposition",
            "kappa rho=G-theta G_theta; kappa p=-G+theta G_theta+dot(G_theta)",
            "heat flux and anisotropic stress vanish in the minimal theta-only sector",
        ),
        (
            "CHS4847_4_auxiliary_equivalence",
            "Q/Lambda elimination",
            "delta_Q S=delta_Lambda S=0 => Hilbert variation of reduced G(theta) equals full auxiliary action on shell",
            "no multiplier stress is lost by on-shell algebraic elimination",
        ),
        (
            "CHS4847_5_tau_pullback",
            "observed-time pullback",
            "u=tau_obs/|tau_obs| => delta u=h.delta tau/|tau_obs|",
            "tau Euler receives the projected memory force D_mu G_theta",
        ),
        (
            "CHS4847_6_local",
            "stationary local theorem",
            "theta=0 => G=G_theta=dot(G_theta)=0 => T_mem=0 and E_tau_mem=0",
            "Gamma0 remains a separate vacuum background",
        ),
        (
            "CHS4847_7_degeneracy",
            "quadratic-origin warning",
            "G_theta_theta proportional s at s=0 and vanishes exactly",
            "this memory term cannot be the sole healthy kinetic owner of tau/u",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "object": obj,
            "formula": formula,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, obj, formula, consequence in rows
    ]


def stress_rows(timestamp: str, epsilon_h: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for kernel_name, kernel in KERNELS.items():
        rho_zero = density_root(kernel)
        hessian_zero = hessian_root(kernel)
        midpoint = 0.5 * (rho_zero + hessian_zero)
        for value in (0.0, 0.1, hessian_zero, midpoint, 1.0, rho_zero, 3.0):
            scalar = value ** (1.0 / 3.0) if value > 0.0 else 0.0
            function, derivative, second = kernel(value)
            g_theta_over_gamma_ell = scalar**2 * derivative
            g_theta_theta_over_gamma_ell2 = (
                2.0 * scalar * derivative + 3.0 * scalar**4 * second
            ) / 3.0
            dot_theta_ell2 = 3.0 * scalar**2 * epsilon_h
            dot_g_theta_over_gamma = (
                dot_theta_ell2
                * (2.0 * scalar * derivative + 3.0 * scalar**4 * second)
                / 3.0
            )
            rho_factor = function - 3.0 * value * derivative
            pressure_factor = -function + 3.0 * value * derivative + dot_g_theta_over_gamma
            identity_residual = rho_factor + pressure_factor - dot_g_theta_over_gamma
            rows.append(
                {
                    "row_id": f"STR4847_{kernel_name}_{value:.8e}",
                    "kernel": kernel_name,
                    "y": f"{value:.16e}",
                    "s_ell_theta_over_3": f"{scalar:.16e}",
                    "epsilon_H": f"{epsilon_h:.16e}",
                    "G_over_Gamma_star": f"{function:.16e}",
                    "G_theta_over_Gamma_star_ell": f"{g_theta_over_gamma_ell:.16e}",
                    "G_theta_theta_over_Gamma_star_ell2": f"{g_theta_theta_over_gamma_ell2:.16e}",
                    "dot_G_theta_over_Gamma_star": f"{dot_g_theta_over_gamma:.16e}",
                    "kappa_rho_over_Gamma_star": f"{rho_factor:.16e}",
                    "kappa_p_over_Gamma_star": f"{pressure_factor:.16e}",
                    "rho_plus_p_identity_residual": f"{identity_residual:.16e}",
                    "unit_lambda_over_Gamma_star": f"{-0.5 * dot_g_theta_over_gamma:.16e}",
                    "heat_flux": "0",
                    "anisotropic_stress": "0",
                    "rho_zero_y": f"{rho_zero:.16e}",
                    "hessian_zero_y": f"{hessian_zero:.16e}",
                    "status": "EXACT_STATIC_STRESS_ZERO" if value == 0.0 else "COVARIANT_STRESS_COMPUTED_NONCLAIM",
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                }
            )
    return rows


def viability_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for kernel_name, kernel in KERNELS.items():
        rho_zero = density_root(kernel)
        hessian_zero = hessian_root(kernel)
        midpoint = 0.5 * (rho_zero + hessian_zero)
        function, derivative, second = kernel(midpoint)
        scalar = midpoint ** (1.0 / 3.0)
        rho_factor = function - 3.0 * midpoint * derivative
        hessian_factor = (2.0 * scalar * derivative + 3.0 * scalar**4 * second) / 3.0
        rows.extend(
            [
                {
                    "window_id": f"WIN4847_{kernel_name}_negative_amplitude",
                    "kernel": kernel_name,
                    "Gamma_star_sign": "negative",
                    "lower_y": f"{hessian_zero:.16e}",
                    "upper_y": f"{rho_zero:.16e}",
                    "sample_y": f"{midpoint:.16e}",
                    "rho_factor_before_amplitude": f"{rho_factor:.16e}",
                    "hessian_factor_before_amplitude": f"{hessian_factor:.16e}",
                    "positive_density": (-rho_factor) > 0.0,
                    "positive_G_theta_theta": (-hessian_factor) > 0.0,
                    "positive_density_and_G_convexity_window": hessian_zero < rho_zero and rho_factor < 0.0 and hessian_factor < 0.0,
                    "homogeneous_kinetic_bracket": "6+9*Gamma_star*ell_Q^2*hessian_factor > 6 in this sign window",
                    "status": "NEGATIVE_AMPLITUDE_POSITIVE_RHO_AND_G_CONVEXITY_WINDOW_FOUND",
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                },
                {
                    "window_id": f"WIN4847_{kernel_name}_positive_amplitude_above_rho_root",
                    "kernel": kernel_name,
                    "Gamma_star_sign": "positive",
                    "lower_y": f"{rho_zero:.16e}",
                    "upper_y": "infinity",
                    "sample_y": "3.0000000000000000e+00",
                    "rho_factor_before_amplitude": f"{kernel(3.0)[0] - 9.0 * kernel(3.0)[1]:.16e}",
                    "hessian_factor_before_amplitude": f"{((2.0 * (3.0 ** (1.0 / 3.0)) * kernel(3.0)[1] + 3.0 * (3.0 ** (4.0 / 3.0)) * kernel(3.0)[2]) / 3.0):.16e}",
                    "positive_density": True,
                    "positive_G_theta_theta": False,
                    "positive_density_and_G_convexity_window": False,
                    "homogeneous_kinetic_bracket": "requires 6+9*Gamma_star*ell_Q^2*hessian_factor > 0",
                    "status": "POSITIVE_DENSITY_BUT_NEGATIVE_G_CURVATURE_TOTAL_KINETIC_BOUND_REQUIRED",
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                },
            ]
        )
    return rows


def ward_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "ward_id": "WARD4847_0_independent_u",
            "branch": "memory sector owns independent unit u",
            "Euler_condition": "D_mu G_theta=0",
            "stress_divergence": "0 on u and metric equations",
            "exchange": "none for separately on-shell memory sector",
            "status": "COVARIANT_WARD_CLOSURE_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ward_id": "WARD4847_1_shared_tau",
            "branch": "u is normalized parent tau_obs",
            "Euler_condition": "E_tau_parent + |tau|^-1 h.D G_theta/kappa = 0",
            "stress_divergence": "memory divergence balanced by parent tau-sector force",
            "exchange": "explicit same-action tau exchange",
            "status": "SHARED_TAU_EXCHANGE_IDENTITY_READY_PARENT_EULER_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ward_id": "WARD4847_2_external_u_forbidden",
            "branch": "u fixed externally while memory stress retained",
            "Euler_condition": "not varied",
            "stress_divergence": "generically nonzero",
            "exchange": "hidden external force",
            "status": "FAILED_EXTERNAL_FLOW_CONTROL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ward_id": "WARD4847_3_stationary_local",
            "branch": "parent normalized Killing tau",
            "Euler_condition": "theta=0 => G_theta=0",
            "stress_divergence": "0",
            "exchange": "0 in active memory sector",
            "status": "EXACT_LOCAL_MEMORY_STRESS_AND_EULER_ZERO_PRIVATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4847_0_stress",
            "decision": "covariant_memory_stress_closed_for_independent_unit_flow",
            "reason": "metric variation plus the unit constraint exactly reproduces the 4846 FLRW stress and gives zero heat/aniso",
            "next_action": "pull the result through the parent tau/coframe action and calculate preferred-frame residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4847_1_amplitude",
            "decision": "negative_Gamma_star_survives_density_and_homogeneous_kinetic_precheck",
            "reason": "both kernels have a finite interval where negative amplitude gives positive density and positive G_theta_theta; this preserves the GR-sign homogeneous kinetic bracket but is not a full perturbative stability proof",
            "next_action": "constrain ell_Q H0 to the derived interval, retain the full scalar/vector kinetic-matrix gate, and run cosmology likelihood",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4847_2_tau",
            "decision": "do_not_treat_u_as_external",
            "reason": "external u leaves an unbalanced Ward force; independent unit u or normalized parent tau must be varied",
            "next_action": "derive parent tau kinetic/current term or retain its response as a bounded preferred-frame channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4847_3_next",
            "decision": "run_H_load_cosmology_only_after_tau_stress_gate_is_recorded",
            "reason": "background fit without the covariant stress and stability window would score the wrong density",
            "next_action": "4848 H-load background equation and nonclaim cosmology smoke runner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timestamp", default="2026-07-09T21:30:00+00:00")
    parser.add_argument("--epsilon-h", type=float, default=-0.45)
    arguments = parser.parse_args()
    datasets = {
        "P8_Y5_R2FR_4847_SOURCE_REGISTER.csv": source_rows(arguments.timestamp),
        "P8_Y5_R2FR_4847_COVARIANT_STRESS_THEOREM.csv": theorem_rows(arguments.timestamp),
        "P8_Y5_R2FR_4847_STRESS_OUTPUT.csv": stress_rows(arguments.timestamp, arguments.epsilon_h),
        "P8_Y5_R2FR_4847_STABILITY_WINDOW.csv": viability_rows(arguments.timestamp),
        "P8_Y5_R2FR_4847_WARD_TAU_OUTPUT.csv": ward_rows(arguments.timestamp),
        "P8_Y5_R2FR_4847_DECISION.csv": decision_rows(arguments.timestamp),
    }
    for name, rows in datasets.items():
        write_csv(arguments.output_dir / name, rows)
    print("COHERENT_LOAD_COVARIANT_STRESS_RUNNER_PASS")
    for name, rows in datasets.items():
        print(f"{name}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
