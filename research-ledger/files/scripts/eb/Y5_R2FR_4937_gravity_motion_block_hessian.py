from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4937"
OUTPUT = SOURCE_DIR / "gravity_motion_block_hessian_results.json"
SERIES_OUTPUT = SOURCE_DIR / "fractional_mixing_power_series.csv"

PARENT_ACTION = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
CHECKPOINT_4936 = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
FRACTIONAL_4936 = POST / "source-intake" / "functional_rg" / "4936" / "fractional_potential_LPA_closure_results.json"
WETTERICH_SOURCE = SOURCE_DIR / "src-1911.06100v3" / "Eff_Scalar_Pot_ASQG.tex"
PHYSICAL_HESSIAN_SOURCE = SOURCE_DIR / "src-2111.04696v2" / "Rsquared.tex"

MARKER = "MTS_4937_GRAVITY_MOTION_BLOCK_HESSIAN"
EXPECTED_HASHES = {
    PARENT_ACTION: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    CHECKPOINT_4936: "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971",
    FRACTIONAL_4936: "8af1d8bf764372917991126c86de63847714f1a48ca4f5eb0925d1b91a4fdf96",
    WETTERICH_SOURCE: "5d742ca63e93e1715adfba01f83c6c6cf2fcbbdb57407cb472eee5133914b9b9",
    PHYSICAL_HESSIAN_SOURCE: "7c857e1ccdd7569874ca8a439f62afee24994d4389c2c4bec772b4620b949bb0",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("refusing to write an empty Hessian power series")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def coefficient(expression: sp.Expr, variable: sp.Symbol, power: int) -> sp.Expr:
    return sp.simplify(sp.expand(expression).coeff(variable, power))


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path) if path.exists() else "MISSING"}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"gravity-motion Hessian source hash mismatch: {hash_failures}")

    sigma, delta_psi = sp.symbols("sigma delta_psi", real=True)
    momentum_sq, scale = sp.symbols("p2 k", positive=True)
    planck_function, potential_value = sp.symbols("F U", positive=True)
    potential_prime, potential_second = sp.symbols("Uprime Usecond", real=True)

    physical_trace_norm = sp.Rational(1, 3)
    sqrt_metric = 1 + sigma / 2 + sigma**2 * (
        sp.Rational(1, 8) - physical_trace_norm / 4
    )
    potential_expansion = (
        potential_value
        + potential_prime * delta_psi
        + potential_second * delta_psi**2 / 2
    )
    quadratic_potential = sp.expand(sqrt_metric * potential_expansion)
    hessian_sigma_sigma_potential = sp.diff(
        quadratic_potential, sigma, sigma
    ).subs({sigma: 0, delta_psi: 0})
    hessian_sigma_psi_potential = sp.diff(
        quadratic_potential, sigma, delta_psi
    ).subs({sigma: 0, delta_psi: 0})
    hessian_psi_psi_potential = sp.diff(
        quadratic_potential, delta_psi, delta_psi
    ).subs({sigma: 0, delta_psi: 0})

    source_sigma_kernel = planck_function * momentum_sq / 2 - potential_value / 4
    hessian_sigma_sigma = -source_sigma_kernel / 3
    hessian_sigma_psi = hessian_sigma_psi_potential
    hessian_psi_psi = momentum_sq + potential_second
    unnormalized_hessian = sp.Matrix(
        [
            [hessian_sigma_sigma, hessian_sigma_psi],
            [hessian_sigma_psi, hessian_psi_psi],
        ]
    )

    canonical_sigma_factor = sp.sqrt(planck_function / 6)
    canonical_hessian = sp.simplify(
        sp.diag(sp.sqrt(6 / planck_function), 1)
        * unnormalized_hessian
        * sp.diag(sp.sqrt(6 / planck_function), 1)
    )
    expected_canonical_hessian = sp.Matrix(
        [
            [-(momentum_sq - potential_value / (2 * planck_function)), sp.sqrt(3 / (2 * planck_function)) * potential_prime],
            [sp.sqrt(3 / (2 * planck_function)) * potential_prime, momentum_sq + potential_second],
        ]
    )

    dimensionless_u, dimensionless_w = sp.symbols("u w", positive=True)
    dimensionless_u_prime, dimensionless_u_second = sp.symbols(
        "uprime usecond", real=True
    )
    a = sp.simplify(1 - dimensionless_u / (4 * dimensionless_w))
    b = 1 + dimensionless_u_second
    mu_sq = sp.simplify(3 * dimensionless_u_prime**2 / (4 * dimensionless_w))
    mu = sp.symbols("mu", real=True)
    dimensionless_block = sp.Matrix([[-a, mu], [mu, b]])
    block_determinant = sp.factor(dimensionless_block.det())

    regulator_weight = sp.symbols("r_sigma", positive=True)
    signed_regulator_kernel = sp.diag(-regulator_weight, 1)
    inverse_trace = sp.factor(
        sp.trace(dimensionless_block.inv() * signed_regulator_kernel)
    )
    inverse_trace_mu_sq = sp.factor(inverse_trace.subs(mu**2, mu_sq))
    expected_inverse_trace = sp.factor(
        (a + regulator_weight * b) / (a * b + mu_sq)
    )
    diagonal_trace = sp.factor(1 / b + regulator_weight / a)

    q, g_tilde = sp.symbols("q g_tilde", positive=True)
    fractional_substitutions = {
        dimensionless_u: sp.Rational(3, 4) * g_tilde * q**2,
        dimensionless_u_prime: g_tilde * sp.sqrt(q),
        dimensionless_u_second: g_tilde / (3 * q),
    }
    fractional_a = sp.factor(a.subs(fractional_substitutions))
    fractional_b = sp.factor(b.subs(fractional_substitutions))
    fractional_mu_sq = sp.factor(mu_sq.subs(fractional_substitutions))
    loop_factor = 1 / (32 * sp.pi**2)
    pair_trace = sp.factor(
        loop_factor * expected_inverse_trace.subs(fractional_substitutions)
    )
    pair_diagonal = sp.factor(
        loop_factor * diagonal_trace.subs(fractional_substitutions)
    )
    mixed_correction = sp.factor(pair_trace - pair_diagonal)

    pair_series = sp.series(pair_trace, q, 0, 5).removeO().expand()
    diagonal_series = sp.series(pair_diagonal, q, 0, 5).removeO().expand()
    mixed_series = sp.series(mixed_correction, q, 0, 5).removeO().expand()

    dimensionless_v = sp.factor(
        fractional_substitutions[dimensionless_u] / dimensionless_w
    )
    tt_trace = sp.factor(5 / (24 * sp.pi**2 * (1 - dimensionless_v)))
    measure_trace = -1 / (8 * sp.pi**2)
    canonical_fractional_flow = -2 * g_tilde * q**2
    full_flow = sp.factor(
        canonical_fractional_flow + tt_trace + measure_trace + pair_trace
    )
    full_flow_series = sp.series(full_flow, q, 0, 4).removeO().expand()

    weights = {
        "canonical_signed_block": sp.Integer(1),
        "source_diagonal_calibrated": sp.Rational(4, 3),
    }
    rows: list[dict[str, Any]] = []
    for scheme_name, weight in weights.items():
        scheme_pair = sp.expand(pair_series.subs(regulator_weight, weight))
        scheme_diagonal = sp.expand(diagonal_series.subs(regulator_weight, weight))
        scheme_mixed = sp.expand(mixed_series.subs(regulator_weight, weight))
        scheme_full = sp.expand(full_flow_series.subs(regulator_weight, weight))
        for power in range(0, 4):
            rows.append(
                {
                    "scheme": scheme_name,
                    "r_sigma": str(weight),
                    "q_power": power,
                    "varphi_power": str(sp.Rational(2 * power, 3)),
                    "pair_coefficient": str(coefficient(scheme_pair, q, power)),
                    "diagonal_pair_coefficient": str(coefficient(scheme_diagonal, q, power)),
                    "mixing_only_coefficient": str(coefficient(scheme_mixed, q, power)),
                    "full_flow_coefficient": str(coefficient(scheme_full, q, power)),
                    "can_cancel_scalar_q_channel": power != 1 or coefficient(scheme_mixed, q, power) != 0,
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    q_pair_coefficient = sp.simplify(coefficient(pair_series, q, 1))
    q_mixed_coefficient = sp.simplify(coefficient(mixed_series, q, 1))
    q_full_coefficient = sp.simplify(coefficient(full_flow_series, q, 1))
    q2_mixed_coefficient = sp.simplify(coefficient(mixed_series, q, 2))

    checks = {
        "physical_trace_norm_is_one_third": physical_trace_norm == sp.Rational(1, 3),
        "sqrt_metric_quadratic_coefficient_is_one_twenty_four": coefficient(sqrt_metric, sigma, 2) == sp.Rational(1, 24),
        "potential_sigma_Hessian_is_U_over_twelve": hessian_sigma_sigma_potential == potential_value / 12,
        "potential_cross_Hessian_is_Uprime_over_two": hessian_sigma_psi_potential == potential_prime / 2,
        "potential_scalar_Hessian_is_Usecond": hessian_psi_psi_potential == potential_second,
        "canonical_Hessian_exact": sp.simplify(canonical_hessian - expected_canonical_hessian) == sp.zeros(2),
        "block_determinant_exact": sp.simplify(block_determinant + a * b + mu**2) == 0,
        "signed_inverse_trace_exact": sp.simplify(inverse_trace_mu_sq - expected_inverse_trace) == 0,
        "diagonal_limit_exact": sp.simplify(expected_inverse_trace.subs(dimensionless_u_prime, 0) - diagonal_trace) == 0,
        "source_weight_reproduces_sigma_coefficient": sp.simplify(loop_factor * sp.Rational(4, 3) - 1 / (24 * sp.pi**2)) == 0,
        "fractional_a_exact": sp.simplify(fractional_a - (1 - 3 * g_tilde * q**2 / (16 * dimensionless_w))) == 0,
        "fractional_b_exact": fractional_b == (g_tilde + 3 * q) / (3 * q),
        "fractional_mu_squared_exact": fractional_mu_sq == 3 * g_tilde**2 * q / (4 * dimensionless_w),
        "pair_q_source_is_scalar_and_nonzero": q_pair_coefficient == 3 / (32 * sp.pi**2 * g_tilde),
        "mixing_has_no_q_term": q_mixed_coefficient == 0,
        "mixing_starts_at_q_squared": q2_mixed_coefficient == -9 * regulator_weight * g_tilde / (128 * sp.pi**2 * dimensionless_w),
        "full_flow_retains_q_source": q_full_coefficient == 3 / (32 * sp.pi**2 * g_tilde),
        "no_fractional_q_cancellation_in_either_scheme": all(
            coefficient(mixed_series.subs(regulator_weight, weight), q, 1) == 0
            and coefficient(full_flow_series.subs(regulator_weight, weight), q, 1) != 0
            for weight in weights.values()
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(f"gravity-motion Hessian checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "background_action": {
            "Euclidean_form": "Gamma_k=integral sqrt(g)[-F_k R/2+U_k(psi)+(nabla psi)^2/2]",
            "background": "flat metric and arbitrary constant off-shell psi; Z_psi=1 in this checkpoint",
            "physical_metric_decomposition": "f_mn=t_mn+S_hat_mn sigma with tr(S_hat)=1 and S_hat_mn S_hat^mn=1/3 on flat space",
        },
        "direct_second_variation": {
            "sqrt_g": "1+sigma/2+sigma^2/24+O(f^3)",
            "quadratic_potential_action": "U sigma^2/24+(U'/2)sigma delta_psi+(U''/2)delta_psi^2",
            "source_sigma_kernel": "K_sigma=(F/2)p^2-U/4",
            "unnormalized_Hessian_sigma_delta_psi": [["-K_sigma/3", "U'/2"], ["U'/2", "p^2+U''"]],
            "canonical_trace_coordinate": "s=sqrt(F/6)sigma",
            "canonical_Hessian_s_delta_psi": [["-(p^2-U/(2F))", "sqrt(3/(2F))U'"], ["sqrt(3/(2F))U'", "p^2+U''"]],
            "mixing_silence_condition": "U'=0; constant scalar position alone is insufficient off shell",
        },
        "optimized_dimensionless_block": {
            "definitions": {
                "w": "F/(2k^2)",
                "u": "U/k^4",
                "v": "u/w",
                "a": "1-v/4",
                "b": "1+u''",
                "mu_squared": "3(u')^2/(4w)",
            },
            "block_over_k_squared": [["-a", "mu"], ["mu", "b"]],
            "determinant_over_k_four": "-(a b+mu^2)",
            "pole_condition": "a b+mu^2=0",
            "signed_diagonal_regulator_trace": "(a+r_sigma b)/(a b+mu^2)",
            "r_sigma_1": "canonical signed-block robustness convention",
            "r_sigma_4_over_3": "calibrates the diagonal sigma term to 1/[24pi^2(1-v/4)] in arXiv:1911.06100",
            "scheme_boundary": "the r_sigma calibration is a declared optimized physical-gauge flow convention, not a regulator-independent observable",
        },
        "fractional_parent_projection": {
            "q": "|varphi|^(2/3)",
            "u": "(3/4)g_tilde q^2",
            "u_prime": "g_tilde sqrt(q)",
            "u_second": "g_tilde/(3q)",
            "a": str(fractional_a),
            "b": str(fractional_b),
            "mu_squared": str(fractional_mu_sq),
            "pair_trace_exact": str(pair_trace),
            "pair_trace_series": str(pair_series),
            "diagonal_pair_series": str(diagonal_series),
            "mixing_only_series": str(mixed_series),
            "full_flow_series_eta_zero": str(full_flow_series),
            "leading_generated_q_coefficient": str(q_full_coefficient),
            "leading_mixing_correction": str(q2_mixed_coefficient) + " q^2",
            "cancellation_result": "REJECTED_WITHIN_UNCHANGED_MINIMAL_PARENT_AND_DECLARED_OPTIMIZED_BLOCK",
            "reason": "the scalar threshold generates q while TT, sigma-potential and sigma-motion mixing first depend on the fractional field at q^2",
        },
        "route_decision": {
            "exact_mixed_trace_cancellation_escape": False,
            "full_functional_potential_required": True,
            "next_calculation": "solve the declared gravity-motion fixed-functional equation and count its linear eigenoperators",
        },
        "checks": checks,
        "claim_boundary": {
            "off_shell_gravity_motion_Hessian_derived": True,
            "optimized_mixed_potential_trace_derived": True,
            "fractional_q_cancellation_found": False,
            "regulator_independent_no_go_claimed": False,
            "full_MTS_fixed_function_derived": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(SERIES_OUTPUT, rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_SERIES_SHA256={digest(SERIES_OUTPUT)}", flush=True)
    print(f"{MARKER}_Q_SOURCE={q_full_coefficient}", flush=True)
    print(f"{MARKER}_MIXING_Q={q_mixed_coefficient}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
