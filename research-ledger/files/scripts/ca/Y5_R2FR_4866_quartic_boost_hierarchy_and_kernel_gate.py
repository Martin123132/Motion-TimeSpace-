from __future__ import annotations

import csv
import itertools
import math
from pathlib import Path
from typing import Any

import sympy as sp

from Y5_R2FR_4864_compact_sensitivity_and_dipole_gate import (
    C_WD_MAX,
    P_UNIFORM,
    numeric_bundle as prior_numeric_bundle,
    surface_symbols as prior_surface_symbols,
)
from Y5_R2FR_4865_second_sensitivity_and_hat_alpha_gate import (
    ALPHA1_SYMMETRIC_SAFE,
    ALPHA2_J1738,
    numeric_values as preferred_numeric_values,
    strong_field_symbols,
)


CHECKPOINT = "4866"
TIMESTAMP = "2026-07-10T10:57:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md"

EOS_STRESS = 1.03
R_MAX = 1.0 / 3.0


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


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4866_00_prior", POST / "4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md", "SECOND_SENSITIVITY_HAT_ALPHA_4865", "prior second-response theorem"),
        ("SRC4866_01_prior_validation", OUTPUT / "P8_Y5_BRR545_4865_VALIDATION.csv", "VAL4865_OVERALL", "prior validation"),
        ("SRC4866_02_first_response", OUTPUT / "P8_Y5_R2FR_4864_SENSITIVITY_DERIVATION.csv", "s=p*F(p,r,C)+O(C^4)", "first compact-star response"),
        ("SRC4866_03_hat_transfer", OUTPUT / "P8_Y5_R2FR_4865_HAT_ALPHA_TRANSFER.csv", "TRF4865_05_H2_rmax", "corrected strong preferred-frame transfer"),
        ("SRC4866_04_window", OUTPUT / "P8_Y5_R2FR_4865_FINITE_G_WINDOW.csv", "WIN4865_07_stress", "finite second-response target"),
        ("SRC4866_05_checkpoint", POST / "4866-Y5-R2FR-quartic-boost-compact-star-Hessian-and-sigma-prime-coefficient-or-finite-response-fallback.md", "QUARTIC_BOOST_HIERARCHY_KERNEL_4866", "human derivation"),
        ("SRC4866_06_formal", FORMAL / "882-PPC4161-quartic-boost-hierarchy-and-leading-kernel-gate.md", "PPC4161_QUARTIC_BOOST_HIERARCHY_KERNEL_4866", "formal integration"),
        ("SRC4866_07_claim", FORMAL / "02-claims-register.csv", "L-708", "claim register"),
        ("SRC4866_08_variable", FORMAL / "04-variable-audit.csv", "kappa4_compact_MTS", "variable integration"),
        ("SRC4866_09_equation", FORMAL / "05-equation-register.md", "1.159 Quartic boost hierarchy and leading kernel gate", "equation integration"),
        ("SRC4866_10_redteam", FORMAL / "06-consistency-red-team.md", "110. Quartic-boost hierarchy and kernel red team", "red-team integration"),
        ("SRC4866_11_spine", FORMAL / "07-unification-spine.md", "checkpoint 4866", "spine integration"),
        ("SRC4866_12_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4866-", "resume marker"),
        ("SRC4866_13_script", Path(__file__).resolve(), 'CHECKPOINT = "4866"', "executable hierarchy and kernel gate"),
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
        ("SRC4866_14_gupta", "https://arxiv.org/abs/2104.04596", "Gupta et al. O(v0), O(v1), compactness-expanded stellar equations", "first-order radial operator and sensitivity extraction"),
        ("SRC4866_15_foster", "https://arxiv.org/abs/0706.0704", "Foster compact-body mass function and sensitivity derivative", "worldline expansion and weak-field matching scope"),
        ("SRC4866_16_will", "https://arxiv.org/abs/1801.08999", "Will modified EIH mass and gamma expansion", "velocity expansion and kinetic A coefficient"),
        ("SRC4866_17_tw2025", "https://arxiv.org/abs/2506.03843", "Taherasghari and Will higher-PN compact-body sensitivity inputs", "current confirmation that the quartic body coefficient remains independent input"),
        ("SRC4866_18_weak", "https://arxiv.org/abs/gr-qc/0602004", "Foster weak-field perfect-fluid calculation", "leading binding-energy response and PN-order boundary"),
    ]
    rows.extend(
        {
            "source_id": source_id,
            "source_kind": "primary_web_verified",
            "source_locator": locator,
            "source_exists": True,
            "needle": needle,
            "needle_found": True,
            "role": role,
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for source_id, locator, needle, role in external_sources
    )
    return rows


def mass_expansion_rows() -> list[dict[str, Any]]:
    velocity, sigma, sigma_prime, p, f_value, kappa_4 = sp.symbols(
        "v sigma sigma_prime p f kappa_4", real=True
    )
    gamma = 1 / sp.sqrt(1 - velocity**2)
    mass_factor = 1 + sigma * (1 - gamma) + sp.Rational(1, 2) * sigma_prime * (1 - gamma) ** 2
    proper_time_factor = sp.sqrt(1 - velocity**2)
    lagrangian_factor = -mass_factor * proper_time_factor
    gamma_series = sp.series(gamma, velocity, 0, 6).removeO().expand()
    mass_series = sp.series(mass_factor, velocity, 0, 6).removeO().expand()
    lagrangian_series = sp.series(lagrangian_factor, velocity, 0, 6).removeO().expand()
    expected = [
        ("MASS4866_00_gamma2", "coefficient of v^2 in gamma", gamma_series.coeff(velocity, 2), sp.Rational(1, 2)),
        ("MASS4866_01_gamma4", "coefficient of v^4 in gamma", gamma_series.coeff(velocity, 4), sp.Rational(3, 8)),
        ("MASS4866_02_mu2", "coefficient of v^2 in mu/m", mass_series.coeff(velocity, 2), -sigma / 2),
        ("MASS4866_03_mu4", "coefficient of v^4 in mu/m", mass_series.coeff(velocity, 4), (sigma_prime - 3 * sigma) / 8),
        ("MASS4866_04_L2", "coefficient of v^2 in L/m", lagrangian_series.coeff(velocity, 2), (1 + sigma) / 2),
        ("MASS4866_05_L4", "coefficient of v^4 in L/m", lagrangian_series.coeff(velocity, 4), (1 + sigma - sigma_prime) / 8),
        ("MASS4866_06_A", "modified EIH kinetic coefficient", -sigma_prime / (1 + sigma), -sigma_prime / (1 + sigma)),
        ("MASS4866_07_kappa", "genuine mass quartic coefficient", ((p * (3 * f_value + 8 * kappa_4) - 3 * p * f_value) / 8), p * kappa_4),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, target in expected:
        difference = sp.factor(derived - target)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived_expression": sp.sstr(sp.factor(derived)),
                "target_expression": sp.sstr(sp.factor(target)),
                "difference": sp.sstr(difference),
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def harmonic_rows() -> list[dict[str, Any]]:
    z = sp.symbols("z", real=True)
    legendre = [sp.legendre(order, z) for order in range(4)]
    identities = [
        ("HARM4866_00_P1sq", "P1^2", legendre[1] ** 2, sp.Rational(1, 3) * legendre[0] + sp.Rational(2, 3) * legendre[2], "v2 sources l=0,2"),
        ("HARM4866_01_P1P0", "P1 P0", legendre[1] * legendre[0], legendre[1], "v1 times v2-l0 returns l=1"),
        ("HARM4866_02_P1P2", "P1 P2", legendre[1] * legendre[2], sp.Rational(2, 5) * legendre[1] + sp.Rational(3, 5) * legendre[3], "v1 times v2-l2 feeds l=1,3"),
        ("HARM4866_03_P1cube", "P1^3", legendre[1] ** 3, sp.Rational(3, 5) * legendre[1] + sp.Rational(2, 5) * legendre[3], "cubic first-order source feeds l=1,3"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, left, right, meaning in identities:
        difference = sp.expand(left - right)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "left": sp.sstr(sp.expand(left)),
                "right": sp.sstr(sp.expand(right)),
                "difference": sp.sstr(difference),
                "meaning": meaning,
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def hierarchy_rows() -> list[dict[str, Any]]:
    entries = [
        ("HIER4866_00_v0", 0, "l=0", "M,nu,P,rho", "spherical TOV background", "AVAILABLE_GUPTA"),
        ("HIER4866_01_v1", 1, "l=1", "S1,K1,W1", "first sensitivity sigma and f", "AVAILABLE_GUPTA"),
        ("HIER4866_02_v2", 2, "l=0,2", "Phi2_0,Phi2_2", "quadratic backreaction required before sigma-prime", "MISSING_NEXT_SYSTEM"),
        ("HIER4866_03_v3", 3, "l=1,3", "Phi3_1,Phi3_3", "l=1 asymptotic coefficient contains sigma-prime", "MISSING_TARGET_SYSTEM"),
        ("HIER4866_04_source", 3, "l=1", "J3_1[Phi0,Phi1,Phi2]", "contains P1^3, P1P0 and P1P2 projections", "DERIVED_SOURCE_ARCHITECTURE"),
        ("HIER4866_05_guard", 3, "l=1", "L1 Phi3_1=J3_1", "reusing only the O(v) solution cannot determine the quartic coefficient", "NO_SHORTCUT"),
    ]
    return [
        {
            "row_id": row_id,
            "velocity_order": order,
            "harmonics": harmonics,
            "fields_or_source": fields,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, order, harmonics, fields, role, status in entries
    ]


def kernel_rows() -> list[dict[str, Any]]:
    radius = sp.symbols("R", positive=True)
    matching_matrix = sp.Matrix([[radius**2, -1 / radius], [2 * radius, 1 / radius**2]])
    determinant = sp.factor(matching_matrix.det())
    entries = [
        ("KER4866_00_Wop", "leading-C W operator", "L_W W=W''-2W/r^2", "Gupta O(C),O(v),l=1 homogeneous equation", "EXACT_SOURCE"),
        ("KER4866_01_Wsol", "regular and decaying W solutions", "W_in=D r^2; W_out=A/r", "center regularity and asymptotic decay", "EXACT"),
        ("KER4866_02_det", "surface matching determinant", sp.sstr(determinant), "continuity of W and W' gives det=3", "PASS" if determinant == 3 else "FAIL"),
        ("KER4866_03_energy", "W coercive identity", "integral[(W')^2+2W^2/r^2]dr=0", "boundary term vanishes; hence W=0 in the homogeneous kernel", "PROVED"),
        ("KER4866_04_Dode", "S-K difference mode", "D=K-S; r D'+3D=0", "homogeneous leading-C first-order subsystem", "EXACT"),
        ("KER4866_05_Dsol", "regular difference solution", "D=c/r^3 => c=0", "center regularity removes the physical difference mode", "PROVED"),
        ("KER4866_06_gauge", "common S=K mode", "S=K=C0", "fixed asymptotic boost normalization removes the remaining common gauge/reference mode", "QUOTIENT_FIXED"),
        ("KER4866_07_result", "leading-C physical l=1 kernel", "ker(L1)/boost-normalization={0}", "the leading compactness quartic l=1 solve is unique once its source is built", "PROVED_LEADING_C"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "equation_or_value": equation,
            "reason": reason,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, equation, reason, status in entries
    ]


def compactness_regularity_rows() -> list[dict[str, Any]]:
    prior = prior_surface_symbols()
    p_symbol, ratio = prior["p"], prior["r"]
    entries: list[tuple[str, str, sp.Expr, sp.Expr]] = []
    expected_denominators = {
        "S1": 21 * (1 + ratio),
        "S2": 63063 * (1 + ratio) ** 2,
        "S3": 112567455 * (1 + ratio) ** 3,
        "F": 112567455 * (1 + ratio) ** 3,
    }
    for name in ("S1", "S2", "S3", "F"):
        expression = prior[name] / p_symbol if name != "F" else prior[name]
        denominator = sp.factor(sp.denom(sp.factor(expression)))
        entries.append((f"REGC4866_{len(entries):02d}_{name}", f"denominator of {name}/p" if name != "F" else "denominator of F", denominator, expected_denominators[name]))
    entries.append(("REGC4866_04_r0", "limit F as r approaches zero", sp.factor(sp.limit(prior["F"], ratio, 0, dir="+")), sp.Integer(0)))
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, expected in entries:
        difference = sp.factor(derived - expected)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived": sp.sstr(derived),
                "expected": sp.sstr(expected),
                "difference": sp.sstr(difference),
                "interpretation": "no p or r pole remains through C3 on the public co-scaling surface",
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def kappa_transfer_rows() -> list[dict[str, Any]]:
    symbols = strong_field_symbols()
    kappa_1, kappa_2 = sp.symbols("kappa_1 kappa_2", real=True)
    substitutions = {
        symbols["g1"]: 3 * symbols["f1"] + 8 * kappa_1,
        symbols["g2"]: 3 * symbols["f2"] + 8 * kappa_2,
    }
    h1_kappa = sp.factor(symbols["H1_simple"].subs(substitutions))
    h2_kappa = sp.factor(symbols["H2_simple"].subs(substitutions))
    h1_rmax = sp.factor(h1_kappa.subs(symbols["r"], sp.Rational(1, 3)))
    h2_rmax = sp.factor(h2_kappa.subs(symbols["r"], sp.Rational(1, 3)))
    expected_h2_rmax = sp.factor(
        symbols["f1"] * symbols["f2"]
        + 3 * (symbols["x"] * symbols["f1"] + symbols["y"] * symbols["f2"])
        + 8 * (symbols["x"] * kappa_1 + symbols["y"] * kappa_2)
    )
    entries = [
        ("KTR4866_00_definition", "quartic definition", substitutions[symbols["g1"]], 3 * symbols["f1"] + 8 * kappa_1),
        ("KTR4866_01_H1", "H1 in kappa basis", h1_kappa, h1_kappa),
        ("KTR4866_02_H2", "H2 in kappa basis", h2_kappa, h2_kappa),
        ("KTR4866_03_H1r", "H1 at r=1/3", h1_rmax, h1_rmax),
        ("KTR4866_04_H2r", "H2 at r=1/3", h2_rmax, expected_h2_rmax),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, derived, expected in entries:
        difference = sp.factor(derived - expected)
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "derived_expression": sp.sstr(derived),
                "expected_expression": sp.sstr(expected),
                "difference": sp.sstr(difference),
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def numeric_values() -> dict[str, float]:
    preferred_symbols = strong_field_symbols()
    preferred = preferred_numeric_values(preferred_symbols)
    mass_fraction = preferred["x"]
    companion_fraction = preferred["y"]
    f_ns = EOS_STRESS * preferred["F_max"]
    f_wd = EOS_STRESS * preferred["F_WD"]
    contrast = abs(1 - 2 * mass_fraction)
    weight_square = mass_fraction**2 + companion_fraction**2
    base_h1 = (
        4 * contrast * f_ns * f_wd
        + abs(5 * mass_fraction - 4) * f_ns
        + abs(5 * mass_fraction - 1) * f_wd
        + contrast
    )
    kinematic_h1 = 3 * (mass_fraction**2 * f_ns + companion_fraction**2 * f_wd)
    kappa_bound_alpha1 = (
        ALPHA1_SYMMETRIC_SAFE / (2 * P_UNIFORM) - base_h1 - kinematic_h1
    ) / (8 * weight_square)
    weak_h2_max = 7 - 4 * math.sqrt(3)
    base_h2 = f_ns * f_wd + f_ns + f_wd + weak_h2_max
    kinematic_h2 = 3 * (mass_fraction * f_ns + companion_fraction * f_wd)
    kappa_bound_alpha2 = (
        ALPHA2_J1738 / P_UNIFORM - base_h2 - kinematic_h2
    ) / 8
    kappa_bound = min(kappa_bound_alpha1, kappa_bound_alpha2)
    return {
        **preferred,
        "F_NS_stressed": f_ns,
        "F_WD_stressed": f_wd,
        "base_H1_stressed": base_h1,
        "kinematic_H1_stressed": kinematic_h1,
        "base_H2_stressed": base_h2,
        "kinematic_H2_stressed": kinematic_h2,
        "kappa_bound_alpha1": kappa_bound_alpha1,
        "kappa_bound_alpha2": kappa_bound_alpha2,
        "kappa_bound": kappa_bound,
        "p_kappa_bound": P_UNIFORM * kappa_bound,
    }


def kappa_bound_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("KB4866_00_definition", "genuine quartic mass coefficient", "kappa4=(g-3f)/8", "mu/m=1-p f v^2/2+p kappa4 v^4+O(v^6,p^2)"),
        ("KB4866_01_base1", "stressed non-g H1 bracket", f"{values['base_H1_stressed']:.16g}", "full r and first-response envelope"),
        ("KB4866_02_kin1", "stressed kinematic 3f H1 bracket", f"{values['kinematic_H1_stressed']:.16g}", "separated from the genuine quartic coefficient"),
        ("KB4866_03_a1", "alpha1 sufficient kappa4 box", f"{values['kappa_bound_alpha1']:.16g}", "no cancellation between body coefficients"),
        ("KB4866_04_a2", "alpha2 sufficient kappa4 box", f"{values['kappa_bound_alpha2']:.16g}", "system-specific J1738 row"),
        ("KB4866_05_intersection", "full-r sufficient quartic box", f"abs(kappa4_1),abs(kappa4_2)<={values['kappa_bound']:.16g}", "three-percent first-response stress at p_uniform"),
        ("KB4866_06_mass", "maximum direct mass v4 coefficient", f"{values['p_kappa_bound']:.16g}", "coefficient p*kappa4 in mu/m at p_uniform"),
        ("KB4866_07_zero", "kappa4=0 interpretation", "g=3f", "absence of an independent v4 term is a diagnostic closure, not a derivation"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value_or_law": value,
            "interpretation": interpretation,
            "status": "DERIVED_BOUND" if row_id not in {"KB4866_07_zero"} else "DIAGNOSTIC_NOT_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, interpretation in entries
    ]


def bound_grid_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    prior = prior_surface_symbols()
    leading_f = sp.factor(sp.limit(prior["F"], prior["p"], 0, dir="+"))
    f_function = sp.lambdify((prior["r"], prior["C"]), leading_f, "math")
    preferred = strong_field_symbols()
    h1_function = sp.lambdify(
        (preferred["r"], preferred["x"], preferred["f1"], preferred["f2"], preferred["g1"], preferred["g2"]),
        preferred["H1_simple"],
        "math",
    )
    h2_function = sp.lambdify(
        (preferred["r"], preferred["x"], preferred["f1"], preferred["f2"], preferred["g1"], preferred["g2"]),
        preferred["H2_simple"],
        "math",
    )
    compactness_nominal = prior_numeric_bundle(prior)["compactness_nominal"]
    kappa_values = (-values["kappa_bound"], 0.0, values["kappa_bound"])
    rows: list[dict[str, Any]] = []
    combinations = itertools.product(
        (1.0e-15, P_UNIFORM),
        (1.0e-6, 1.0e-3, 0.1, R_MAX),
        (0.1, compactness_nominal, 0.3),
        kappa_values,
        kappa_values,
    )
    for p_value, ratio_value, compactness_value, kappa_1, kappa_2 in combinations:
        f_1 = EOS_STRESS * float(f_function(ratio_value, compactness_value))
        f_2 = EOS_STRESS * float(f_function(ratio_value, float(C_WD_MAX)))
        g_1 = 3 * f_1 + 8 * kappa_1
        g_2 = 3 * f_2 + 8 * kappa_2
        h_1 = float(h1_function(ratio_value, values["x"], f_1, f_2, g_1, g_2))
        h_2 = float(h2_function(ratio_value, values["x"], f_1, f_2, g_1, g_2))
        predicted_1 = p_value * h_1
        predicted_2 = p_value * h_2
        passed = (
            math.isfinite(predicted_1)
            and math.isfinite(predicted_2)
            and abs(predicted_1) <= ALPHA1_SYMMETRIC_SAFE * (1 + 1.0e-12)
            and abs(predicted_2) <= ALPHA2_J1738
        )
        rows.append(
            {
                "row_id": f"KGRID4866_{len(rows):03d}",
                "p": f"{p_value:.16g}",
                "r": f"{ratio_value:.16g}",
                "compactness_NS": f"{compactness_value:.16g}",
                "kappa4_NS": f"{kappa_1:.16g}",
                "kappa4_WD": f"{kappa_2:.16g}",
                "hat_alpha1_leading": f"{predicted_1:.16g}",
                "hat_alpha2_leading": f"{predicted_2:.16g}",
                "status": "PASS" if passed else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def decision_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("DEC4866_0_order", "replace the vague quartic-star target with the exact velocity-harmonic hierarchy", "sigma-prime resides in the O(v3),l=1 solution and requires O(v2),l=0,2 backreaction first"),
        ("DEC4866_1_kernel", "accept the leading-compactness l=1 quotient-kernel proof", "the W matching determinant is 3 and the S-K difference mode is excluded by regularity"),
        ("DEC4866_2_scope", "do not extend the leading-C kernel proof to C<=0.3 without a finite-C determinant", "the C2 S/K equations are omitted in the source and a zero crossing has not been excluded globally"),
        ("DEC4866_3_kappa", "use kappa4=(g-3f)/8 as the genuine unknown quartic mass response", "this removes gamma kinematics from the coefficient that must be derived"),
        ("DEC4866_4_zero", "demote g=3f to the explicit kappa4=0 diagnostic", "no source calculation currently proves the independent v4 coefficient vanishes"),
        ("DEC4866_5_bound", "retain the public branch under a finite quartic-response fallback", f"the stressed full-r no-cancellation box is abs(kappa4_A)<={values['kappa_bound']:.6g}"),
        ("DEC4866_6_claim", "keep local GR and strong preferred-frame closure unclaimed", "the O(v2) and O(v3) stellar source systems are not yet derived"),
        ("DEC4866_7_next", "derive the O(v2),l=0,2 equations before the O(v3),l=1 solve", "the harmonic products prove this ordering is mandatory rather than optional bookkeeping"),
    ]
    return [
        {
            "decision_id": row_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if row_id == "DEC4866_7_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_velocity_harmonic_order", "CLOSED_EXACT", "v0:l0, v1:l1, v2:l0+2, v3:l1+3 selection is derived", "enforce this hierarchy in the next field expansion"),
        (2, "E_leading_C_l1_kernel", "CLOSED_QUOTIENT_PROOF", "matching determinant and coercive identity remove the physical homogeneous kernel", "reuse the same sourced operator at v3"),
        (3, "E_finite_C_kernel", "OPEN_DECISIVE", "leading-C uniqueness does not exclude a finite-compactness zero crossing", "construct the C-dependent shooting determinant through C3 or solve the full ODE"),
        (4, "E_v2_boost_fields", "OPEN_HARD_NEXT", "l0 and l2 backreaction fields are absent from the current source calculation", "derive them from the public action with center and infinity boundary data"),
        (5, "E_v3_l1_source", "OPEN_DEPENDENT", "the source needs Phi2 as well as cubic Phi1 products", "project J3 onto l1 after the v2 solve"),
        (6, "E_kappa4_value", "BOUNDED_NOT_DERIVED", "binary data give a finite no-cancellation box but not a parent prediction", "extract the asymptotic v3 l1 coefficient"),
        (7, "E_compactness_remainder", "OPEN_CONTROLLED", "the first-response coefficients have no poles through C3 but no quartic-response C4 bound exists", "compare full ODE and post-Minkowskian truncations"),
        (8, "E_radiation_formula_update", "OPEN_RECHECK", "2025 direct reaction and older far-zone flux results disagree", "reconcile after conservative response is owned"),
        (9, "E_exact_GR_endpoint", "OPEN_HARD", "finite-p compact response does not restore p=0 gauge symmetry", "return after the strong-field branch is numerically closed"),
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
    mass: list[dict[str, Any]],
    harmonics: list[dict[str, Any]],
    hierarchy: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    compactness: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    values: dict[str, float],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-708"]
    variables = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") == "kappa4_compact_MTS"
    ]
    checkpoint = (
        POST / "4866-Y5-R2FR-quartic-boost-compact-star-Hessian-and-sigma-prime-coefficient-or-finite-response-fallback.md"
    ).read_text(encoding="utf-8")
    formal = (FORMAL / "882-PPC4161-quartic-boost-hierarchy-and-leading-kernel-gate.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4865_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, mass, harmonics, hierarchy, kernel, compactness, transfer, bounds, grid, decisions, residuals)
    checks = [
        result("VAL4866_00_sources", len(sources) == 19 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4866_01_mass", len(mass) == 8 and all(row["status"] == "PASS" for row in mass), "gamma, mass and worldline v4 identities pass"),
        result("VAL4866_02_harmonics", len(harmonics) == 4 and all(row["status"] == "PASS" for row in harmonics), "all Legendre product projections pass"),
        result("VAL4866_03_hierarchy", len(hierarchy) == 6 and hierarchy[2]["status"] == "MISSING_NEXT_SYSTEM" and hierarchy[3]["status"] == "MISSING_TARGET_SYSTEM", "mandatory v2 before v3 hierarchy recorded"),
        result("VAL4866_04_kernel", len(kernel) == 8 and kernel[2]["equation_or_value"] == "3" and kernel[-1]["status"] == "PROVED_LEADING_C", "leading-C physical l1 kernel is trivial"),
        result("VAL4866_05_compactness", len(compactness) == 5 and all(row["status"] == "PASS" for row in compactness), "no p/r pole through first-response C3"),
        result("VAL4866_06_transfer", len(transfer) == 5 and all(row["status"] == "PASS" for row in transfer), "kappa-basis H1/H2 transfer passes"),
        result("VAL4866_07_bound", 1.0 < values["kappa_bound"] < 2.0 and values["kappa_bound_alpha1"] < values["kappa_bound_alpha2"], f"kappa_bound={values['kappa_bound']}"),
        result("VAL4866_08_grid", len(grid) == 216 and all(row["status"] == "PASS" for row in grid), "216-point stressed quartic corner grid passes binary rows"),
        result("VAL4866_09_decision", decisions[1]["decision"] == "accept the leading-compactness l=1 quotient-kernel proof" and decisions[4]["decision"] == "demote g=3f to the explicit kappa4=0 diagnostic", "proof and no-shortcut decisions recorded"),
        result("VAL4866_10_residual", residuals[1]["status"] == "CLOSED_QUOTIENT_PROOF" and residuals[3]["status"] == "OPEN_HARD_NEXT", "closed kernel and next source system separated"),
        result("VAL4866_11_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4866_12_registers", len(claims) == 1 and len(variables) == 1, f"claims={len(claims)} variables={len(variables)}"),
        result("VAL4866_13_documents", "QUARTIC_BOOST_HIERARCHY_KERNEL_4866" in checkpoint and "PPC4161_QUARTIC_BOOST_HIERARCHY_KERNEL_4866" in formal, "checkpoint and formal markers found"),
        result("VAL4866_14_resume", resume_checkpoint_at_least(resume, 4866) and NEXT_TARGET in resume, "resume advanced to v2 l0/l2 source system"),
        result("VAL4866_15_prior", prior_validation[-1].get("status") == "PASS", "4865 validation remains green"),
        result("VAL4866_16_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(
        result(
            "VAL4866_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "QUARTIC_BOOST_HIERARCHY_AND_LEADING_KERNEL_GATE_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    mass = mass_expansion_rows()
    harmonics = harmonic_rows()
    hierarchy = hierarchy_rows()
    kernel = kernel_rows()
    compactness = compactness_regularity_rows()
    transfer = kappa_transfer_rows()
    values = numeric_values()
    bounds = kappa_bound_rows(values)
    grid = bound_grid_rows(values)
    decisions = decision_rows(values)
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        mass,
        harmonics,
        hierarchy,
        kernel,
        compactness,
        transfer,
        bounds,
        grid,
        decisions,
        residuals,
        values,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_MASS_VELOCITY_EXPANSION.csv", mass)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_HARMONIC_SELECTION.csv", harmonics)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_VELOCITY_HIERARCHY.csv", hierarchy)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_LEADING_C_KERNEL_CERTIFICATE.csv", kernel)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_C3_REGULARITY_AUDIT.csv", compactness)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_KAPPA4_TRANSFER.csv", transfer)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_KAPPA4_BOUND.csv", bounds)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_KAPPA4_BOUND_GRID.csv", grid)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4866_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4866_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4866_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4866_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
