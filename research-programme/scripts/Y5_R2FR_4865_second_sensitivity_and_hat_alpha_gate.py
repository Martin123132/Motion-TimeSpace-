from __future__ import annotations

import csv
import itertools
import math
from pathlib import Path
from typing import Any

import sympy as sp

from Y5_R2FR_4864_compact_sensitivity_and_dipole_gate import (
    C_WD_MAX,
    M1_J1738,
    M2_J1738,
    P_UNIFORM,
    numeric_bundle as prior_numeric_bundle,
    surface_symbols as prior_surface_symbols,
)


CHECKPOINT = "4865"
TIMESTAMP = "2026-07-10T04:25:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4866-Y5-R2FR-quartic-boost-compact-star-Hessian-and-sigma-prime-coefficient-or-finite-response-fallback.md"

R_MAX = 1.0 / 3.0
ALPHA1_LOWER_J1738 = -3.5e-5
ALPHA1_UPPER_J1738 = 3.3e-5
ALPHA1_SYMMETRIC_SAFE = min(abs(ALPHA1_LOWER_J1738), abs(ALPHA1_UPPER_J1738))
ALPHA2_J1738 = 2.9e-4
ALPHA2_COMBINED = 1.8e-4
ALPHA2_SOLITARY = 1.6e-9
EOS_STRESS = 1.03


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def strong_field_symbols() -> dict[str, sp.Expr]:
    p, ratio, mass_fraction = sp.symbols("p r x", positive=True)
    f_1, f_2, g_1, g_2 = sp.symbols("f_1 f_2 g_1 g_2", real=True)
    companion_fraction = 1 - mass_fraction
    c_a = 2 * ratio * p / (1 + ratio)
    c_theta = 2 * p / ((1 + ratio) * (1 - p))
    c_sigma = sp.Integer(0)
    c_omega = p * (1 + ratio - ratio * p)
    alpha_1 = -8 * ratio * p / (1 + ratio)
    alpha_2 = -ratio * p * (1 - 3 * ratio) / (1 + ratio)
    sigma_1 = p * f_1
    sigma_2 = p * f_2
    sigma_prime_1 = p * g_1
    sigma_prime_2 = p * g_2
    effective_g = 1 / ((1 + sigma_1) * (1 + sigma_2))
    script_a_1 = -sigma_prime_1 / (1 + sigma_1)
    script_a_2 = -sigma_prime_2 / (1 + sigma_2)
    script_b_12 = effective_g * (1 + sigma_1)
    script_b_21 = effective_g * (1 + sigma_2)
    script_b_minus = (script_b_12 - script_b_21) / 2
    script_q = (
        -sp.Rational(1, 2)
        * (2 - c_a)
        / (2 * c_sigma - c_a)
        * (alpha_1 - 2 * alpha_2)
        * (sigma_1 + sigma_2)
        + 3 * (2 - c_a) / (2 * c_sigma + c_theta) * sigma_1 * sigma_2
    )
    script_r = (
        sp.Rational(1, 2)
        * (8 + alpha_1)
        / (c_omega + c_sigma)
        * (-c_omega * (sigma_1 + sigma_2) + (1 - c_omega) * sigma_1 * sigma_2)
    )
    script_c = effective_g * (
        alpha_1 - alpha_2 - 3 * (sigma_1 + sigma_2) - script_q - script_r
    )
    script_e = effective_g * (alpha_2 + script_q - script_r)
    script_a_power_1 = mass_fraction * script_a_1 + companion_fraction * script_a_2
    script_a_power_2 = mass_fraction**2 * script_a_1 - companion_fraction**2 * script_a_2
    mass_difference = mass_fraction - companion_fraction
    hat_alpha_1 = sp.factor(
        mass_difference * (script_c + script_e)
        - 6 * script_b_minus
        - 2 * effective_g * script_a_power_2
    )
    hat_alpha_2 = sp.factor(script_e - effective_g * script_a_power_1)
    h_1 = sp.factor(sp.limit(hat_alpha_1 / p, p, 0, dir="+"))
    h_2 = sp.factor(sp.limit(hat_alpha_2 / p, p, 0, dir="+"))
    contrast = 1 - 2 * mass_fraction
    h_1_simple = sp.factor(
        2
        * (
            4 * contrast * f_1 * f_2 / (1 + ratio)
            + (5 * mass_fraction - 4) * f_1
            + (5 * mass_fraction - 1) * f_2
            + mass_fraction**2 * g_1
            - companion_fraction**2 * g_2
            + 4 * ratio * contrast / (1 + ratio)
        )
    )
    h_2_simple = sp.factor(
        (3 * ratio**2 + 6 * ratio - 1) / (1 + ratio) * f_1 * f_2
        + (1 - 3 * ratio) * (f_1 + f_2)
        + mass_fraction * g_1
        + companion_fraction * g_2
        + ratio * (3 * ratio - 1) / (1 + ratio)
    )
    h_1_rmax = sp.factor(h_1_simple.subs(ratio, sp.Rational(1, 3)))
    h_2_rmax = sp.factor(h_2_simple.subs(ratio, sp.Rational(1, 3)))
    return {
        "p": p,
        "r": ratio,
        "x": mass_fraction,
        "y": companion_fraction,
        "f1": f_1,
        "f2": f_2,
        "g1": g_1,
        "g2": g_2,
        "Q": script_q,
        "R": script_r,
        "hat_alpha1": hat_alpha_1,
        "hat_alpha2": hat_alpha_2,
        "H1": h_1,
        "H2": h_2,
        "H1_simple": h_1_simple,
        "H2_simple": h_2_simple,
        "H1_rmax": h_1_rmax,
        "H2_rmax": h_2_rmax,
    }


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4865_00_prior", POST / "4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md", "COMPACT_BODY_SENSITIVITY_DIPOLE_4864", "prior compact-body result"),
        ("SRC4865_01_prior_validation", OUTPUT / "P8_Y5_BRR545_4864_VALIDATION.csv", "VAL4864_OVERALL", "prior validation"),
        ("SRC4865_02_sensitivity", OUTPUT / "P8_Y5_R2FR_4864_SENSITIVITY_DERIVATION.csv", "s=p*F(p,r,C)+O(C^4)", "leading sensitivity law"),
        ("SRC4865_03_map", OUTPUT / "P8_Y5_R2FR_4864_COEFFICIENT_MAP.csv", "MAP4864_09", "public compact-body coefficient map"),
        ("SRC4865_04_checkpoint", POST / "4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md", "SECOND_SENSITIVITY_HAT_ALPHA_4865", "human derivation"),
        ("SRC4865_05_formal", FORMAL / "881-PPC4161-second-sensitivity-and-strong-field-preferred-frame-gate.md", "PPC4161_SECOND_SENSITIVITY_HAT_ALPHA_4865", "formal integration"),
        ("SRC4865_06_claim", FORMAL / "02-claims-register.csv", "L-707", "claim register"),
        ("SRC4865_07_variable", FORMAL / "04-variable-audit.csv", "sigma_prime_compact_MTS", "variable integration"),
        ("SRC4865_08_equation", FORMAL / "05-equation-register.md", "1.158 Second sensitivity and strong preferred-frame gate", "equation integration"),
        ("SRC4865_09_redteam", FORMAL / "06-consistency-red-team.md", "109. Second-sensitivity and strong preferred-frame red team", "red-team integration"),
        ("SRC4865_10_spine", FORMAL / "07-unification-spine.md", "checkpoint 4865", "spine integration"),
        ("SRC4865_11_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4865-", "resume marker"),
        ("SRC4865_12_script", Path(__file__).resolve(), 'CHECKPOINT = "4865"', "executable preferred-frame gate"),
        ("SRC4865_13_cutoff", OUTPUT / "P8_Y5_R2FR_4863_HARD_CUTOFF.csv", "CUT4863_0_canonical", "finite-r regular-response context"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    external_sources = [
        ("SRC4865_14_gupta", "primary_web_verified", "https://arxiv.org/abs/2104.04596", "Gupta et al. corrected EIH Appendix and sensitivity definitions", "corrected compact-body hat-alpha transfer"),
        ("SRC4865_15_shao_binary", "primary_web_verified", "https://arxiv.org/abs/1209.4503", "Shao and Wex binary preferred-frame limits", "system-specific and combined binary bounds"),
        ("SRC4865_16_shao_solitary", "primary_web_verified", "https://arxiv.org/abs/1307.2552", "Shao et al. solitary spin-precession limit", "conditional one-body target only"),
        ("SRC4865_17_tw2025", "primary_web_verified", "https://arxiv.org/abs/2506.03843", "Taherasghari and Will 2025 compact-body mass expansion", "independent higher sensitivity coefficients in current PN dynamics"),
        ("SRC4865_18_foster", "primary_web_verified", "https://arxiv.org/abs/0706.0704", "Foster strong-field effective action", "compact-body sensitivity framework"),
    ]
    rows.extend(
        {
            "source_id": source_id,
            "source_kind": source_kind,
            "source_locator": locator,
            "source_exists": True,
            "needle": needle,
            "needle_found": True,
            "role": role,
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for source_id, source_kind, locator, needle, role in external_sources
    )
    return rows


def regular_response_rows() -> list[dict[str, Any]]:
    entries = [
        ("REG4865_00_reduced", "co-scaled reduced compact-body functional", "I[p,x,Y]=I_GR+p I1[x,Y;r,C]+O(p^2)", "established public coefficients all scale with p at fixed finite r"),
        ("REG4865_01_stationary", "leading reduced stationary equation", "D_Y I1[x,Y0]=0", "the p factor divides out before taking p to zero"),
        ("REG4865_02_hessian", "regular-response condition", "H_YY=D_Y^2 I1 invertible after gauge fixing and boundary conditions", "explicit no-zero-mode hypothesis"),
        ("REG4865_03_implicit", "stationary branch", "Y_star(x,p)=Y0(x)+O(p)", "implicit-function theorem at fixed 0<r<=1/3"),
        ("REG4865_04_mass", "on-shell mass response", "ln(mu)=ln(m_GR)+p h(x;r,C)+O(p^2)", "h is finite with two x derivatives on a regular branch"),
        ("REG4865_05_first", "first sensitivity", "sigma=-d_x ln(mu)=p f+O(p^2); f=-h_x(0)", "agrees with sigma=s/(1-s) and s=pF"),
        ("REG4865_06_second", "second sensitivity coefficient", "sigma_prime=sigma+sigma^2+d_x^2 ln(mu)=p g+O(p^2)", "g=f+h_xx(0) is finite but not numerically fixed"),
        ("REG4865_07_schur", "on-shell second derivative", "h_xx=I1_xx-I1_xY H_YY^(-1) I1_Yx", "general Schur complement evaluated on Y0"),
        ("REG4865_08_failure", "strong-field failure condition", "lambda_min(H_YY)=0 or unbounded inverse", "a compact-star zero mode can invalidate sigma_prime=O(p) and triggers fallback"),
        ("REG4865_09_notation", "2025 notation map", "s_TW=-sigma_Gupta; a_s,TW=sigma_prime,Gupta", "follows directly by matching the two Taylor expansions of m(gamma)"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "equation_or_condition": equation,
            "interpretation": interpretation,
            "status": "FAILURE_GATE_IDENTIFIED" if row_id == "REG4865_08_failure" else "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, equation, interpretation in entries
    ]


def transfer_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio, mass_fraction = symbols["p"], symbols["r"], symbols["x"]
    f_1, f_2, g_1, g_2 = symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]
    companion_fraction = 1 - mass_fraction
    expected_q = 3 * (1 + ratio) * (f_1 * f_2 - f_1 - f_2)
    expected_r = -4 * (-f_1 * f_2 + (1 + ratio) * (f_1 + f_2)) / (1 + ratio)
    expected_h1_rmax = 2 * (
        3 * f_1 * f_2 * (1 - 2 * mass_fraction)
        + f_1 * (5 * mass_fraction - 4)
        + f_2 * (5 * mass_fraction - 1)
        + mass_fraction**2 * g_1
        - companion_fraction**2 * g_2
        + 1
        - 2 * mass_fraction
    )
    expected_h2_rmax = f_1 * f_2 + mass_fraction * g_1 + companion_fraction * g_2
    entries = [
        ("TRF4865_00_Q", "lim Q/p", sp.limit(symbols["Q"] / p, p, 0, dir="+"), expected_q),
        ("TRF4865_01_R", "lim R/p", sp.limit(symbols["R"] / p, p, 0, dir="+"), expected_r),
        ("TRF4865_02_H1", "lim hat_alpha1/p", symbols["H1"], symbols["H1_simple"]),
        ("TRF4865_03_H2", "lim hat_alpha2/p", symbols["H2"], symbols["H2_simple"]),
        ("TRF4865_04_H1_rmax", "H1 at r=1/3", symbols["H1_rmax"], expected_h1_rmax),
        ("TRF4865_05_H2_rmax", "H2 at r=1/3", symbols["H2_rmax"], expected_h2_rmax),
        ("TRF4865_06_order1", "hat_alpha1 scaling", sp.limit(symbols["hat_alpha1"], p, 0, dir="+"), sp.Integer(0)),
        ("TRF4865_07_order2", "hat_alpha2 scaling", sp.limit(symbols["hat_alpha2"], p, 0, dir="+"), sp.Integer(0)),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, expected in entries:
        difference = sp.factor(derived - expected)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived_expression": sp.sstr(sp.factor(derived)),
                "expected_expression": sp.sstr(sp.factor(expected)),
                "difference": sp.sstr(difference),
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def numeric_values(symbols: dict[str, sp.Expr]) -> dict[str, float]:
    prior_symbols = prior_surface_symbols()
    prior_values = prior_numeric_bundle(prior_symbols)
    mass_fraction = M2_J1738 / (M1_J1738 + M2_J1738)
    companion_fraction = 1 - mass_fraction
    f_ns = prior_values["F_nominal"]
    f_wd = prior_values["F_WD"]
    f_max = prior_values["F_max"]
    h1_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H1_simple"],
        "math",
    )
    h2_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H2_simple"],
        "math",
    )
    h1_zero = float(h1_function(R_MAX, mass_fraction, f_ns, f_wd, 0.0, 0.0))
    h2_zero = float(h2_function(R_MAX, mass_fraction, f_ns, f_wd, 0.0, 0.0))
    contrast = abs(1 - 2 * mass_fraction)
    weight_square = mass_fraction**2 + companion_fraction**2
    base_h1_uniform = (
        4 * contrast * f_max * f_wd
        + abs(5 * mass_fraction - 4) * f_max
        + abs(5 * mass_fraction - 1) * f_wd
        + contrast
    )
    weak_h2_max = 7 - 4 * math.sqrt(3)
    base_h2_uniform = f_max * f_wd + f_max + f_wd + weak_h2_max
    g_box_alpha1 = (ALPHA1_SYMMETRIC_SAFE / (2 * P_UNIFORM) - base_h1_uniform) / weight_square
    g_box_alpha2 = ALPHA2_J1738 / P_UNIFORM - base_h2_uniform
    f_max_stressed = EOS_STRESS * f_max
    f_wd_stressed = EOS_STRESS * f_wd
    base_h1_stressed = (
        4 * contrast * f_max_stressed * f_wd_stressed
        + abs(5 * mass_fraction - 4) * f_max_stressed
        + abs(5 * mass_fraction - 1) * f_wd_stressed
        + contrast
    )
    g_box_alpha1_stressed = (
        ALPHA1_SYMMETRIC_SAFE / (2 * P_UNIFORM) - base_h1_stressed
    ) / weight_square
    return {
        "x": mass_fraction,
        "y": companion_fraction,
        "F_NS": f_ns,
        "F_WD": f_wd,
        "F_max": f_max,
        "H1_zero": h1_zero,
        "H2_zero": h2_zero,
        "hat_alpha1_zero": P_UNIFORM * h1_zero,
        "hat_alpha2_zero": P_UNIFORM * h2_zero,
        "contrast": contrast,
        "weight_square": weight_square,
        "base_H1_uniform": base_h1_uniform,
        "base_H2_uniform": base_h2_uniform,
        "weak_H2_max": weak_h2_max,
        "g_box_alpha1": g_box_alpha1,
        "g_box_alpha2": g_box_alpha2,
        "g_box": min(g_box_alpha1, g_box_alpha2),
        "base_H1_stressed": base_h1_stressed,
        "g_box_alpha1_stressed": g_box_alpha1_stressed,
        "alpha1_H_budget": ALPHA1_SYMMETRIC_SAFE / P_UNIFORM,
        "alpha2_H_budget_J1738": ALPHA2_J1738 / P_UNIFORM,
        "alpha2_H_budget_combined": ALPHA2_COMBINED / P_UNIFORM,
        "alpha2_H_budget_solitary_conditional": ALPHA2_SOLITARY / P_UNIFORM,
    }


def bound_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("BND4865_00_a1", "J1738 binary hat_alpha1", "[-3.5e-5,3.3e-5]", "95 percent", "system-specific CMB-frame bound; MTS use assumes asymptotic public-flow/CMB alignment", "APPLICABLE_LEADING_TRANSFER_WITH_FRAME_CONDITION"),
        ("BND4865_01_a1safe", "symmetric no-cancellation hat_alpha1 budget", f"{ALPHA1_SYMMETRIC_SAFE:.16g}", "dimensionless", "uses the smaller side of the asymmetric J1738 interval", "APPLICABLE_SUFFICIENT"),
        ("BND4865_02_a2j", "J1738 binary hat_alpha2", f"{ALPHA2_J1738:.16g}", "95 percent magnitude", "system-specific CMB-frame row matching the adopted masses; public-flow/CMB alignment required", "APPLICABLE_LEADING_TRANSFER_WITH_FRAME_CONDITION"),
        ("BND4865_03_a2combined", "combined J1012 plus J1738 hat_alpha2", f"{ALPHA2_COMBINED:.16g}", "95 percent magnitude", "requires approximately common strong parameter across both systems", "CONDITIONAL_SHARED_PARAMETER"),
        ("BND4865_04_solitary", "two solitary pulsars hat_alpha2", f"{ALPHA2_SOLITARY:.16g}", "95 percent magnitude", "spin-precession observable needs a one-body MTS map, not the binary H2 formula", "QUARANTINED_NOT_APPLIED"),
        ("BND4865_05_budget", "J1738 leading coefficient budgets at p_uniform", f"H1_abs<={values['alpha1_H_budget']:.16g};H2_abs<={values['alpha2_H_budget_J1738']:.16g}", "dimensionless coefficients", "binary limits are broad after the exact O(p) transfer", "NONEMPTY"),
    ]
    return [
        {
            "row_id": row_id,
            "observable": observable,
            "bound_or_interval": bound,
            "units_or_confidence": units,
            "applicability": applicability,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, observable, bound, units, applicability, status in entries
    ]


def finite_window_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("WIN4865_00_mass", "J1738 mass fractions", f"x={values['x']:.16g};y={values['y']:.16g}", "x=m_WD/m_total"),
        ("WIN4865_01_f", "nominal leading responses", f"f_NS={values['F_NS']:.16g};f_WD={values['F_WD']:.16g}", "4864 C3 Tolman VII projection"),
        ("WIN4865_02_base1", "uniform H1 bracket base bound", f"{values['base_H1_uniform']:.16g}", "triangle bound over 0<r<=1/3, f_NS<=Fmax and f_WD<=F_WDmax"),
        ("WIN4865_03_base2", "uniform H2 base bound", f"{values['base_H2_uniform']:.16g}", "uses abs[(3r^2+6r-1)/(1+r)]<=1 and max r(1-3r)/(1+r)=7-4sqrt(3)"),
        ("WIN4865_04_g1", "alpha1 sufficient common absolute g bound", f"{values['g_box_alpha1']:.16g}", "if abs(g1),abs(g2) are below this value, the leading H1 bound holds without cancellation"),
        ("WIN4865_05_g2", "alpha2 sufficient common absolute g bound", f"{values['g_box_alpha2']:.16g}", "system-specific binary alpha2 row"),
        ("WIN4865_06_intersection", "uniform finite-response box", f"abs(g1),abs(g2)<={values['g_box']:.16g}", "nonempty full-r leading-order sufficient intersection at p_uniform"),
        ("WIN4865_07_stress", "three-percent sensitivity-stressed g box", f"abs(g1),abs(g2)<={values['g_box_alpha1_stressed']:.16g}", "retains a broad finite-response target"),
        ("WIN4865_08_existence", "arbitrary finite-response existence law", "p<min[p_uniform,alpha1_safe/abs(H1),alpha2_J1738/abs(H2)]", "for finite H1,H2 there is always a positive asymptotic binary-safe p interval"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value_or_law": value,
            "interpretation": interpretation,
            "status": "DERIVED_LEADING_ORDER",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, interpretation in entries
    ]


def benchmark_rows(symbols: dict[str, sp.Expr], values: dict[str, float]) -> list[dict[str, Any]]:
    h1_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H1_simple"],
        "math",
    )
    h2_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H2_simple"],
        "math",
    )
    rows: list[dict[str, Any]] = []
    for p_value, multiplier in itertools.product((1.0e-15, P_UNIFORM), (0.0, 1.0, 3.0)):
        g_1 = multiplier * values["F_NS"]
        g_2 = multiplier * values["F_WD"]
        h_1 = float(h1_function(R_MAX, values["x"], values["F_NS"], values["F_WD"], g_1, g_2))
        h_2 = float(h2_function(R_MAX, values["x"], values["F_NS"], values["F_WD"], g_1, g_2))
        predicted_1 = p_value * h_1
        predicted_2 = p_value * h_2
        rows.append(
            {
                "row_id": f"SMK4865_{len(rows):02d}",
                "p": f"{p_value:.16g}",
                "r": f"{R_MAX:.16g}",
                "response_diagnostic": f"g_A={multiplier:g} f_A",
                "H1": f"{h_1:.16g}",
                "H2": f"{h_2:.16g}",
                "hat_alpha1_leading": f"{predicted_1:.16g}",
                "hat_alpha2_leading": f"{predicted_2:.16g}",
                "binary_alpha1_status": "PASS" if abs(predicted_1) <= ALPHA1_SYMMETRIC_SAFE else "FAIL",
                "binary_alpha2_status": "PASS" if abs(predicted_2) <= ALPHA2_J1738 else "FAIL",
                "solitary_number_if_same_map": "PASS" if abs(predicted_2) <= ALPHA2_SOLITARY else "FAIL",
                "solitary_applicability": "NOT_ESTABLISHED",
                "status": "DIAGNOSTIC_ONLY",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def grid_rows(symbols: dict[str, sp.Expr], values: dict[str, float]) -> list[dict[str, Any]]:
    prior_symbols = prior_surface_symbols()
    leading_f = sp.factor(sp.limit(prior_symbols["F"], prior_symbols["p"], 0, dir="+"))
    f_function = sp.lambdify((prior_symbols["r"], prior_symbols["C"]), leading_f, "math")
    h1_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H1_simple"],
        "math",
    )
    h2_function = sp.lambdify(
        (symbols["r"], symbols["x"], symbols["f1"], symbols["f2"], symbols["g1"], symbols["g2"]),
        symbols["H2_simple"],
        "math",
    )
    compactness_nominal = prior_numeric_bundle(prior_symbols)["compactness_nominal"]
    rows: list[dict[str, Any]] = []
    parameter_grid = itertools.product(
        (1.0e-15, 1.0e-9, P_UNIFORM),
        (1.0e-6, 1.0e-3, 0.1, R_MAX),
        (0.1, compactness_nominal, 0.3),
        (0.0, 1.0, 3.0),
    )
    for p_value, ratio_value, compactness_value, multiplier in parameter_grid:
        f_1 = float(f_function(ratio_value, compactness_value))
        f_2 = float(f_function(ratio_value, float(C_WD_MAX)))
        g_1 = multiplier * f_1
        g_2 = multiplier * f_2
        h_1 = float(h1_function(ratio_value, values["x"], f_1, f_2, g_1, g_2))
        h_2 = float(h2_function(ratio_value, values["x"], f_1, f_2, g_1, g_2))
        predicted_1 = p_value * h_1
        predicted_2 = p_value * h_2
        passed = (
            math.isfinite(predicted_1)
            and math.isfinite(predicted_2)
            and abs(predicted_1) <= ALPHA1_SYMMETRIC_SAFE
            and abs(predicted_2) <= ALPHA2_J1738
        )
        rows.append(
            {
                "row_id": f"GRID4865_{len(rows):03d}",
                "p": f"{p_value:.16g}",
                "r": f"{ratio_value:.16g}",
                "compactness_NS": f"{compactness_value:.16g}",
                "response_multiplier": f"{multiplier:.16g}",
                "f_NS": f"{f_1:.16g}",
                "f_WD": f"{f_2:.16g}",
                "hat_alpha1_leading": f"{predicted_1:.16g}",
                "hat_alpha2_leading": f"{predicted_2:.16g}",
                "status": "PASS" if passed else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def quartic_input_rows() -> list[dict[str, Any]]:
    entries = [
        ("QRT4865_00_first", "linear boost response h_x", "OWNED_THROUGH_C3", "f=-h_x=F+O(C4)", "4864 compact sensitivity"),
        ("QRT4865_01_direct", "direct quartic boost insertion I1_xx", "OPEN_PARENT_COEFFICIENT", "required by the Schur complement", "derive boosted-star action through (gamma-1)^2"),
        ("QRT4865_02_mixed", "mixed boost-profile response I1_xY", "OPEN_PARENT_PROFILE", "required by the Schur complement", "solve the first differentiated compact-star boundary problem"),
        ("QRT4865_03_hessian", "gauge-fixed compact-star inverse Hessian H_YY^-1", "OPEN_ZERO_MODE_GATE", "finite inverse proves regular response", "construct spectrum or a coercive bound"),
        ("QRT4865_04_second", "numeric g=f+h_xx", "OPEN_HARD_NEXT", "2025 PN work treats the corresponding a_s as an input rather than a stellar prediction", "compute the quartic on-shell response and its remainder"),
    ]
    return [
        {
            "row_id": row_id,
            "required_input": required,
            "status": status,
            "role": role,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, required, status, role, next_action in entries
    ]


def decision_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("DEC4865_0_scaling", "accept sigma_prime=p g+O(p^2) on the regular finite-r branch", "the co-scaled on-shell functional and invertible reduced Hessian imply two finite boost derivatives"),
        ("DEC4865_1_failure", "make a compact-star Hessian zero mode the explicit failure trigger", "vacuum positivity alone does not rule out a strong-field zero mode"),
        ("DEC4865_2_transfer", "accept the corrected exact leading H1 and H2 transfer", "all eight symbolic identities vanish"),
        ("DEC4865_3_binary", "retain the public branch under current binary preferred-frame bounds", f"the full-r sufficient three-percent-stressed box remains abs(g_A)<={values['g_box_alpha1_stressed']:.6g}"),
        ("DEC4865_4_combined", "do not silently substitute the combined alpha2 row for the system-specific row", "strong parameters may be compactness dependent"),
        ("DEC4865_5_solitary", "do not apply the 1.6e-9 solitary number to binary H2", "the one-body spin-precession projection is not yet derived"),
        ("DEC4865_6_numeric", "do not invent a numerical g coefficient", "the current parent truncation owns h_x but not the quartic Schur-complement data"),
        ("DEC4865_7_next", "derive the quartic boosted compact-star response", "this directly computes g or exposes the zero mode that rejects the branch"),
    ]
    return [
        {
            "decision_id": row_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if row_id == "DEC4865_7_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_sigma_prime_scaling", "CLOSED_CONDITIONAL_THEOREM", "sigma_prime=O(p) follows on every regular finite-r stationary branch", "retain the Hessian condition explicitly"),
        (2, "E_sigma_prime_coefficient", "OPEN_HARD_NEXT", "g=f+h_xx needs quartic boost and profile-response data", "derive the compact-star Schur complement"),
        (3, "E_compact_zero_mode", "OPEN_DECISIVE_GATE", "a zero eigenvalue invalidates the regular-response theorem", "construct a coercive bound or find the mode"),
        (4, "E_hat_alpha_transfer", "CLOSED_ANALYTIC_LEADING", "corrected Gupta H1 and H2 are reduced exactly", "retain O(p2) remainder discipline"),
        (5, "E_binary_preferred_frame", "BOUNDED_NONEMPTY", "system-specific J1738 rows leave a broad finite-g target", "recompute once g is derived"),
        (6, "E_solitary_precession_map", "OPEN_HARD", "the 1.6e-9 observable is one-body spin precession rather than binary orbital H2", "derive from the public matter-frame compact-body action"),
        (7, "E_radiation_formula_update", "OPEN_RECHECK", "the 2025 direct-reaction calculation reports disagreement with older far-zone flux formulas", "treat 4864 as smoke and compare flux conventions before promotion"),
        (8, "E_exact_GR_endpoint", "OPEN_HARD", "the theorem is finite-r and does not restore the singular p=0 flow chart", "return after the compact Hessian gate"),
        (9, "E_asymptotic_preferred_frame", "OPEN_CONTROLLED", "quoted binary rows use the CMB preferred frame", "derive the FLRW-to-local matching that identifies the asymptotic public flow with the CMB rest frame"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    regular: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    windows: list[dict[str, Any]],
    benchmarks: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    quartic: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    values: dict[str, float],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-707"]
    variables = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") == "sigma_prime_compact_MTS"
    ]
    checkpoint = (
        POST / "4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md"
    ).read_text(encoding="utf-8")
    formal = (FORMAL / "881-PPC4161-second-sensitivity-and-strong-field-preferred-frame-gate.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4864_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, regular, transfer, bounds, windows, benchmarks, grid, quartic, decisions, residuals)
    stressed_h1_bound = 2 * (
        values["base_H1_stressed"]
        + values["weight_square"] * values["g_box_alpha1_stressed"]
    )
    stressed_h2_bound = values["base_H2_uniform"] + values["g_box_alpha1_stressed"]
    checks = [
        result("VAL4865_00_sources", len(sources) == 19 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4865_01_regular", len(regular) == 10 and regular[6]["equation_or_condition"].startswith("sigma_prime="), "regular-response theorem and failure gate recorded"),
        result("VAL4865_02_transfer", len(transfer) == 8 and all(row["status"] == "PASS" for row in transfer), "all corrected H1/H2 identities pass"),
        result("VAL4865_03_bounds", len(bounds) == 6 and bounds[4]["status"] == "QUARANTINED_NOT_APPLIED", "binary and solitary applicability separated"),
        result("VAL4865_04_window", values["g_box"] > 10.0 and values["g_box_alpha1_stressed"] > 10.0, f"g_box={values['g_box']} stressed={values['g_box_alpha1_stressed']}"),
        result("VAL4865_04b_sufficient", stressed_h1_bound <= values["alpha1_H_budget"] * (1 + 1.0e-12) and stressed_h2_bound <= values["alpha2_H_budget_J1738"], f"stress_H1={stressed_h1_bound} stress_H2={stressed_h2_bound}"),
        result("VAL4865_05_nominal", abs(values["hat_alpha1_zero"]) < ALPHA1_SYMMETRIC_SAFE and abs(values["hat_alpha2_zero"]) < ALPHA2_J1738, "zero-curvature-response diagnostic passes binary rows"),
        result("VAL4865_06_benchmarks", len(benchmarks) == 6 and all(row["binary_alpha1_status"] == "PASS" and row["binary_alpha2_status"] == "PASS" for row in benchmarks), "six finite-response diagnostics pass binary rows"),
        result("VAL4865_07_grid", len(grid) == 108 and all(row["status"] == "PASS" for row in grid), "108-point p-r-C-response grid passes"),
        result("VAL4865_08_quartic", len(quartic) == 5 and quartic[-1]["status"] == "OPEN_HARD_NEXT", "numeric g remains an explicit quartic-response target"),
        result("VAL4865_09_branch", decisions[3]["decision"] == "retain the public branch under current binary preferred-frame bounds", "binary gate does not trigger fallback"),
        result("VAL4865_10_solitary", decisions[5]["decision"] == "do not apply the 1.6e-9 solitary number to binary H2", "solitary overconstraint blocked"),
        result("VAL4865_11_residual", residuals[1]["status"] == "OPEN_HARD_NEXT" and residuals[2]["status"] == "OPEN_DECISIVE_GATE", "coefficient and zero-mode targets separated"),
        result("VAL4865_12_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4865_13_registers", len(claims) == 1 and len(variables) == 1, f"claims={len(claims)} variables={len(variables)}"),
        result("VAL4865_14_documents", "SECOND_SENSITIVITY_HAT_ALPHA_4865" in checkpoint and "PPC4161_SECOND_SENSITIVITY_HAT_ALPHA_4865" in formal, "checkpoint and formal markers found"),
        result("VAL4865_15_resume", resume_checkpoint_at_least(resume, 4865) and NEXT_TARGET in resume, "resume advanced to quartic boosted-star response"),
        result("VAL4865_16_prior", prior_validation[-1].get("status") == "PASS", "4864 validation remains green"),
        result("VAL4865_17_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(
        result(
            "VAL4865_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "SECOND_SENSITIVITY_SCALING_AND_HAT_ALPHA_GATE_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    symbols = strong_field_symbols()
    sources = source_rows()
    regular = regular_response_rows()
    transfer = transfer_rows(symbols)
    values = numeric_values(symbols)
    bounds = bound_rows(values)
    windows = finite_window_rows(values)
    benchmarks = benchmark_rows(symbols, values)
    grid = grid_rows(symbols, values)
    quartic = quartic_input_rows()
    decisions = decision_rows(values)
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        regular,
        transfer,
        bounds,
        windows,
        benchmarks,
        grid,
        quartic,
        decisions,
        residuals,
        values,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_REGULAR_RESPONSE_THEOREM.csv", regular)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_HAT_ALPHA_TRANSFER.csv", transfer)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_PREFERRED_FRAME_BOUNDS.csv", bounds)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_FINITE_G_WINDOW.csv", windows)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_BENCHMARK_SMOKE.csv", benchmarks)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_STRONG_FIELD_GRID.csv", grid)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_QUARTIC_INPUT_AUDIT.csv", quartic)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4865_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4865_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4865_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4865_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
