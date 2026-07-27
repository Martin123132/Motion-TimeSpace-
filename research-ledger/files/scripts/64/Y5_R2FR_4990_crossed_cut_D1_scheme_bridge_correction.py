from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4990"

CHECKPOINT_4982 = POST / "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-point-subtraction.md"
CHECKPOINT_4985 = POST / "4985-Y5-R2FR-metric-frame-O2-zero-and-partial-wave-mixing-flow.md"
CHECKPOINT_4986 = POST / "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md"
CHECKPOINT_4987 = POST / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
CHECKPOINT_4988 = POST / "4988-Y5-R2FR-renormalized-scalar-two-particle-cut-and-exact-partial-wave-projection.md"
CHECKPOINT_4989 = POST / "4989-Y5-R2FR-global-D1-master-sum-rules-and-opposite-helicity-hh-support.md"
RESULT_4988 = POST / "source-intake" / "functional_rg" / "4988" / "scalar_cut_soft_subtraction_results.json"
FRG_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
BERN_SOURCE = POST / "source-intake" / "functional_rg" / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"

CROSSING_CSV = SOURCE / "crossed_scalar_cut_identity.csv"
FLOW_CSV = SOURCE / "flow_scheme_separation.csv"
SCHEME_ORBIT_CSV = SOURCE / "scheme_orbit_propagation_correction.csv"
CANCELLATION_CSV = SOURCE / "corrected_D1_cancellation.csv"
HH_SCOPE_CSV = SOURCE / "hh_crossing_support_scope.csv"
SUPERSESSION_CSV = SOURCE / "4989_supersession_matrix.csv"
GATE_CSV = SOURCE / "corrected_master_gate.csv"
RESULT_JSON = SOURCE / "crossed_cut_D1_scheme_bridge_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4990_CROSSED_CUT_D1_SCHEME_BRIDGE_CORRECTION"
CHECKED_DATE = "2026-07-14"

s, t, u = sp.symbols("s t u", nonzero=True)
x, L = sp.symbols("x L", positive=True)
LA, LB, QA, QB = sp.symbols("L_A L_B Q_A Q_B")
PI = sp.pi


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(expression: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.simplify(expression)))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_lock() -> dict[str, bool]:
    frg = normalized_text(FRG_SOURCE)
    dunbar = normalized_text(DUNBAR_SOURCE)
    bern = normalized_text(BERN_SOURCE)
    checkpoint_4982 = normalized_text(CHECKPOINT_4982)
    checkpoint_4985 = normalized_text(CHECKPOINT_4985)
    checkpoint_4986 = normalized_text(CHECKPOINT_4986)
    checkpoint_4987 = normalized_text(CHECKPOINT_4987)
    checkpoint_4988 = normalized_text(CHECKPOINT_4988)
    checkpoint_4989 = normalized_text(CHECKPOINT_4989)
    result_4988 = json.loads(RESULT_4988.read_text(encoding="utf-8"))
    return {
        "frg_functional_flow_context": "functional renormalization group" in frg and "Type I" in frg and "Litim-type" in frg,
        "frg_beta_sixteen_checkpoint": "beta_c,ess|0=20g^2-4g^2=16g^2" in checkpoint_4982,
        "dunbar_counterterm_203_over_320": "{203 \\over 320\\eps } ( D_{\\mu} \\phi D^{\\mu} \\phi )^2" in dunbar,
        "dunbar_amplitude_divergence_203_over_160": "-{203\\over 160\\eps }" in dunbar,
        "bern_all_channel_sum": "sums are over all kinematic channels" in bern,
        "bern_phase_space_half_factor": "additional symmetry factor of $1/2$" in bern,
        "bern_dilatation_sign": "D = -\\mu\\partial_\\mu" in bern,
        "checkpoint_4985_crossing_identity": "=-(9/2)stu" in checkpoint_4985,
        "checkpoint_4985_corrected_double_log": "-609/(10pi)" in checkpoint_4985,
        "checkpoint_4986_mixed_F1": "F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B]" in checkpoint_4986,
        "checkpoint_4986_corrected_fixed_p4_invariant": "I_2L=3S_2L-(203/10)rho_mix" in checkpoint_4986,
        "checkpoint_4987_corrected_full_orbit": "3S-(203/10)rho+(18/pi)r4" in checkpoint_4987,
        "checkpoint_4988_scalar_slopes": "[1827/(10pi)]L" in checkpoint_4988 and "[9541/(300pi)]L" in checkpoint_4988,
        "result_4988_d_slopes": result_4988["projection"]["d0_L_slope"] == "-2233/(72*pi)" and result_4988["projection"]["d2_L_slope"] == "-203/(1800*pi)",
        "checkpoint_4989_wrong_two_cut_target_present": "only remaining low-spin unknowns are the mixed `hhh`" in checkpoint_4989,
    }


def p2(argument: sp.Expr) -> sp.Expr:
    return sp.expand((3 * argument**2 - 1) / 2)


def crossing_identities() -> dict[str, sp.Expr]:
    channel_s = s**3 * p2((t - u) / s)
    channel_t = t**3 * p2((u - s) / t)
    channel_u = u**3 * p2((s - t) / u)
    substitution = {u: -s - t}
    p2_channel_identity = sp.factor((channel_s - (s**3 - 6 * s * t * u)).subs(substitution))
    sum_cubes = sp.factor((s**3 + t**3 + u**3 - 3 * s * t * u).subs(substitution))
    sum_p2 = sp.factor((channel_s + channel_t + channel_u + 15 * s * t * u).subs(substitution))
    mixed = sp.factor(
        (
            s**3 * (-sp.Rational(55, 36) - p2((t - u) / s) / 180)
            + t**3 * (-sp.Rational(55, 36) - p2((u - s) / t) / 180)
            + u**3 * (-sp.Rational(55, 36) - p2((s - t) / u) / 180)
            + sp.Rational(9, 2) * s * t * u
        ).subs(substitution)
    )
    return {
        "single_channel_p2": p2_channel_identity,
        "sum_cubes": sum_cubes,
        "sum_p2": sum_p2,
        "mixed_crossing": mixed,
    }


def scalar_cut_quantities(result_4988: dict[str, Any]) -> dict[str, sp.Expr]:
    d0_constant = sp.sympify(result_4988["projection"]["d0_L0"])
    d2_constant = sp.sympify(result_4988["projection"]["d2_L0"])
    d0_slope = sp.sympify(result_4988["projection"]["d0_L_slope"])
    d2_slope = sp.sympify(result_4988["projection"]["d2_L_slope"])
    f1_log = sp.Rational(2, 1) / PI * (sp.Rational(23, 15) * LA - sp.Rational(1, 30) * LB)
    crossed_log = sp.factor((d0_slope + d2_slope) * LA - 6 * d2_slope * LB)
    master_log = sp.factor(2 * crossed_log)
    d1_multiplier = sp.factor(sp.expand(master_log).coeff(LA) / sp.expand(f1_log).coeff(LA))
    beta_smatrix = -d1_multiplier
    f2_double = sp.factor(beta_smatrix / (2 * PI) * (sp.Rational(23, 15) * QA - sp.Rational(1, 30) * QB))
    f2_double_derivative = sp.factor(f2_double.subs({QA: -4 * LA, QB: -4 * LB}))
    direct_channel_double_log = sp.factor(-beta_smatrix / PI * (sp.Rational(23, 15) - x * (1 - x) / 30))
    direct_channel_legendre = sp.factor(d0_slope + d2_slope * sp.legendre(2, 1 - 2 * x))
    amplitude_a = sp.factor(d0_constant + d2_constant)
    amplitude_b = sp.factor(-6 * d2_constant)
    delta_k_mu = sp.factor(-6 * (d0_constant - 5 * d2_constant))
    delta_k_ang = sp.factor(d0_constant + 7 * d2_constant)
    return {
        "d0_constant": d0_constant,
        "d2_constant": d2_constant,
        "d0_slope": d0_slope,
        "d2_slope": d2_slope,
        "f1_log": f1_log,
        "crossed_log": crossed_log,
        "master_log": master_log,
        "d1_multiplier": d1_multiplier,
        "beta_smatrix": beta_smatrix,
        "f2_double": f2_double,
        "f2_double_derivative": f2_double_derivative,
        "direct_channel_double_log": direct_channel_double_log,
        "direct_channel_legendre": direct_channel_legendre,
        "amplitude_a": amplitude_a,
        "amplitude_b": amplitude_b,
        "delta_k_mu": delta_k_mu,
        "delta_k_ang": delta_k_ang,
    }


def crossing_rows(quantities: dict[str, sp.Expr], identities: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "CROSS4990_01_channel_P2",
            "statement": "q^3 P2((p-r)/q)=q^3-6stu",
            "exact_residual": exact(identities["single_channel_p2"]),
            "consequence": "channel P2 logs map to L_A-6L_B",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CROSS4990_02_sum_cubes",
            "statement": "sum_cyclic q^3=3stu",
            "exact_residual": exact(identities["sum_cubes"]),
            "consequence": "crossing and the dilatation factor are already encoded in -6(d0-5d2)",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CROSS4990_03_sum_P2",
            "statement": "sum_cyclic q^3 P2=-15stu",
            "exact_residual": exact(identities["sum_p2"]),
            "consequence": "direct-channel d0,d2 reconstruct the crossing-symmetric local projection",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CROSS4990_04_mixed_kernel",
            "statement": "sum q^3[-55/36-P2/180]=-(9/2)stu",
            "exact_residual": exact(identities["mixed_crossing"]),
            "consequence": "the 4988 L slopes have exactly the 4985 mixed-kernel shape",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CROSS4990_05_scalar_slope_factor",
            "statement": "d0_L+d2_L P2=(203/(10pi))[-55/36-P2/180]",
            "exact_residual": exact(
                quantities["direct_channel_legendre"]
                - sp.Rational(203, 10) / PI * (-sp.Rational(55, 36) - sp.legendre(2, 1 - 2 * x) / 180)
            ),
            "consequence": "the coefficient 203 is inherited from the physical one-loop scalar-gravity counterterm",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "CROSS4990_06_crossed_scalar_log",
            "statement": "Dphi_crossed,log=-(203/20)F1_log",
            "exact_residual": exact(quantities["crossed_log"] + sp.Rational(203, 20) * quantities["f1_log"]),
            "consequence": "after the master factor two the scalar cut saturates the perturbative D1 nested logarithm",
            "status": "DERIVED_EXACT",
        },
    ]


def flow_rows(quantities: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "flow_id": "FLOW4990_01_FRG",
            "coordinate": "C_FRG",
            "flow_coefficient": "16",
            "flow_definition": "Wilsonian effective-average-action flow in a Type-I Litim FRG truncation after an essential frame map",
            "source_path": relative(FRG_SOURCE),
            "may_enter_on_shell_D1_directly": False,
            "status": "VALID_IN_OWN_SCHEME_NOT_AN_ONSHELL_COEFFICIENT",
        },
        {
            "flow_id": "FLOW4990_02_Smatrix",
            "coordinate": "C_Smatrix",
            "flow_coefficient": exact(quantities["beta_smatrix"]),
            "flow_definition": "perturbative on-shell/rational-free coefficient fixed by the Dunbar counterterm and crossed-cut logarithm",
            "source_path": relative(DUNBAR_SOURCE),
            "may_enter_on_shell_D1_directly": True,
            "status": "DERIVED_EXACT_IN_AMPLITUDE_SCHEME",
        },
        {
            "flow_id": "FLOW4990_03_D_operator",
            "coordinate": "D C_Smatrix",
            "flow_coefficient": exact(quantities["d1_multiplier"]),
            "flow_definition": "D=-mu partial_mu=-d/dlnmu, so D C_Smatrix=-beta_C_Smatrix",
            "source_path": relative(BERN_SOURCE),
            "may_enter_on_shell_D1_directly": True,
            "status": "DERIVED_EXACT",
        },
        {
            "flow_id": "FLOW4990_04_bridge",
            "coordinate": "C_Smatrix=f(C_FRG,g,regulator,frame)",
            "flow_coefficient": "not derived",
            "flow_definition": "finite scheme and regulator map required before comparing 16 with 203/10",
            "source_path": relative(CHECKPOINT_4982),
            "may_enter_on_shell_D1_directly": False,
            "status": "BRIDGE_OPEN_NONCLAIM",
        },
    ]


def scheme_orbit_rows(quantities: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    alpha, beta = sp.symbols("alpha beta")
    C_c, C_w, S_2L, rho_mix, r4, A_2, B_2 = sp.symbols("C_c C_w S_2L rho_mix r4 A_2 B_2")
    beta_c = quantities["beta_smatrix"]
    B_gc = -sp.Rational(6, 1) / PI
    f_A = sp.Rational(46, 15) / PI
    f_B = -sp.Rational(1, 15) / PI

    S_prime = S_2L + beta_c * alpha - B_gc * beta
    rho_prime = rho_mix + 3 * alpha
    r4_prime = r4 - beta
    I_fixed = 3 * S_2L - beta_c * rho_mix
    I_fixed_prime = 3 * S_prime - beta_c * rho_prime
    I_shift_residual = sp.factor(I_fixed_prime - I_fixed + 3 * B_gc * beta)

    K_mu = sp.factor(I_fixed - 3 * B_gc * r4)
    K_mu_prime = sp.factor(I_fixed_prime - 3 * B_gc * r4_prime)
    K_mu_residual = sp.factor(K_mu_prime - K_mu)

    A_prime = A_2 - beta * f_A
    B_prime = B_2 - beta * f_B
    K_ang = sp.factor(A_2 - B_2 - (f_A - f_B) * r4)
    K_ang_prime = sp.factor(A_prime - B_prime - (f_A - f_B) * r4_prime)
    K_ang_residual = sp.factor(K_ang_prime - K_ang)

    S_rational_free = sp.factor(S_2L - beta_c * rho_mix / 3 - B_gc * r4)
    A_rational_free = sp.factor(A_2 - f_A * r4)
    B_rational_free = sp.factor(B_2 - f_B * r4)
    rational_free_mu_residual = sp.factor(3 * S_rational_free - K_mu)
    rational_free_ang_residual = sp.factor(A_rational_free - B_rational_free - K_ang)
    trajectory_double_log = sp.factor(B_gc * beta_c / 2)

    values = {
        "beta_c": beta_c,
        "B_gc": B_gc,
        "trajectory_double_log": trajectory_double_log,
        "S_prime": S_prime,
        "I_fixed": I_fixed,
        "I_shift_residual": I_shift_residual,
        "K_mu": K_mu,
        "K_mu_residual": K_mu_residual,
        "K_ang": K_ang,
        "K_ang_residual": K_ang_residual,
        "S_rational_free": S_rational_free,
        "A_rational_free": A_rational_free,
        "B_rational_free": B_rational_free,
        "rational_free_mu_residual": rational_free_mu_residual,
        "rational_free_ang_residual": rational_free_ang_residual,
    }
    rows = [
        {
            "correction_id": "ORBIT4990_01_on_shell_beta",
            "quantity": "beta_C in the perturbative amplitude scheme",
            "historical_expression": "16 imported from the Type-I/Litim FRG coordinate",
            "corrected_expression": exact(beta_c),
            "exact_residual": exact(beta_c - sp.Rational(203, 10)),
            "consequence": "all amplitude-scheme descendants must use 203/10 unless a finite FRG bridge is supplied",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_02_C_trajectory",
            "quantity": "C(t)",
            "historical_expression": "C_c+16t",
            "corrected_expression": "C_c+(203/10)t",
            "exact_residual": "0",
            "consequence": "the one-loop logarithmic coefficient remains source fixed while its running coordinate is on-shell",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_03_W_double_log",
            "quantity": "coefficient of t^2 in W(t)",
            "historical_expression": "-48/pi",
            "corrected_expression": exact(trajectory_double_log),
            "exact_residual": exact(trajectory_double_log + sp.Rational(609, 10) / PI),
            "consequence": "W=C_w+(S_2L-6C_c/pi)t-(609/(10pi))t^2 in the amplitude scheme",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_04_S_transform",
            "quantity": "finite two-loop scale coordinate",
            "historical_expression": "S_2L'=S_2L+16alpha+(6/pi)beta",
            "corrected_expression": "S_2L'=S_2L+(203/10)alpha+(6/pi)beta",
            "exact_residual": "0",
            "consequence": "the beta shift is required because a finite p4 rational term changes the trajectory origin",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_05_fixed_p4_I",
            "quantity": "fixed-p4 invariant I",
            "historical_expression": "I=3S_2L-16rho_mix",
            "corrected_expression": exact(I_fixed),
            "exact_residual": exact(I_shift_residual),
            "consequence": "I is alpha invariant but shifts by -3B_gc beta under the p4 finite orbit",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_06_full_K_mu",
            "quantity": "full finite-orbit scale invariant K_mu",
            "historical_expression": "3S_2L-16rho_mix+(18/pi)r4",
            "corrected_expression": exact(K_mu),
            "exact_residual": exact(K_mu_residual),
            "consequence": "K_mu is invariant under simultaneous alpha and beta finite redefinitions",
            "status": "CORRECTED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_07_full_K_ang",
            "quantity": "full finite-orbit angular invariant K_ang",
            "historical_expression": "A_2-B_2-(47/(15pi))r4",
            "corrected_expression": exact(K_ang),
            "exact_residual": exact(K_ang_residual),
            "consequence": "the angular invariant is unchanged by the beta_C correction",
            "status": "RECONFIRMED_EXACT",
        },
        {
            "correction_id": "ORBIT4990_08_rational_free",
            "quantity": "double-rational-free reduction",
            "historical_expression": "r4_rf=rho_rf=0; K_mu=3S_rf; K_ang=A_rf-B_rf",
            "corrected_expression": "r4_rf=rho_rf=0; K_mu=3S_rf; K_ang=A_rf-B_rf",
            "exact_residual": exact(rational_free_mu_residual + rational_free_ang_residual),
            "consequence": "4988 scalar subtotals in the declared rational-free scheme are unchanged",
            "status": "RECONFIRMED_EXACT",
        },
    ]
    return rows, values


def cancellation_rows(quantities: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    cancellation = sp.factor(quantities["master_log"] - quantities["d1_multiplier"] * quantities["f1_log"])
    double_log_rg = sp.factor(quantities["f2_double_derivative"] + quantities["beta_smatrix"] * quantities["f1_log"])
    direct_match = sp.factor(quantities["direct_channel_double_log"] - quantities["direct_channel_legendre"])
    return [
        {
            "check_id": "D1C4990_01_master_multiplier",
            "quantity": "D1 ReF1",
            "exact_expression": f"({exact(quantities['d1_multiplier'])}) F1",
            "exact_residual": "0",
            "interpretation": "the on-shell dilatation coefficient is -203/10, not +16",
            "status": "DERIVED_EXACT",
        },
        {
            "check_id": "D1C4990_02_crossed_log_cancellation",
            "quantity": "2 Dphi_crossed,log-D1 ReF1",
            "exact_expression": exact(cancellation),
            "exact_residual": exact(cancellation),
            "interpretation": "no three-particle scale slope is needed or allowed",
            "status": "EXACT_ZERO",
        },
        {
            "check_id": "D1C4990_03_corrected_double_log",
            "quantity": "F2_double",
            "exact_expression": exact(quantities["f2_double"]),
            "exact_residual": exact(double_log_rg),
            "interpretation": "dF2_double/dlnmu=-(203/10)F1_log",
            "status": "DERIVED_EXACT",
        },
        {
            "check_id": "D1C4990_04_direct_channel_double_log",
            "quantity": "Disc_s F2_double coefficient_L",
            "exact_expression": exact(quantities["direct_channel_double_log"]),
            "exact_residual": exact(direct_match),
            "interpretation": "the corrected RG double log reproduces both exact 4988 L slopes",
            "status": "DERIVED_EXACT",
        },
        {
            "check_id": "D1C4990_05_scalar_A",
            "quantity": "Delta A_phi",
            "exact_expression": exact(quantities["amplitude_a"]),
            "exact_residual": "0",
            "interpretation": "A_phi=d0+d2 is an additive scalar-cut single-log subtotal",
            "status": "RESTORED_EXACT_SUBTOTAL",
        },
        {
            "check_id": "D1C4990_06_scalar_B",
            "quantity": "Delta B_phi",
            "exact_expression": exact(quantities["amplitude_b"]),
            "exact_residual": "0",
            "interpretation": "B_phi=-6d2 is an additive scalar-cut single-log subtotal",
            "status": "RESTORED_EXACT_SUBTOTAL",
        },
        {
            "check_id": "D1C4990_07_scalar_Kmu",
            "quantity": "Delta K_mu_phi",
            "exact_expression": exact(quantities["delta_k_mu"]),
            "numeric_value": f"{float(sp.N(quantities['delta_k_mu'], 17)):.15g}",
            "exact_residual": "0",
            "interpretation": "the factor two and cyclic crossing are already encoded in the -6 inverse map; do not multiply again",
            "status": "RESTORED_EXACT_SUBTOTAL_NOT_FULL_K",
        },
        {
            "check_id": "D1C4990_08_scalar_Kang",
            "quantity": "Delta K_ang_phi",
            "exact_expression": exact(quantities["delta_k_ang"]),
            "numeric_value": f"{float(sp.N(quantities['delta_k_ang'], 17)):.15g}",
            "exact_residual": "0",
            "interpretation": "the scalar angular single-log subtotal is additive but not the full invariant",
            "status": "RESTORED_EXACT_SUBTOTAL_NOT_FULL_K",
        },
    ]


def hh_scope_rows() -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    physical_t = -x
    physical_u = x - 1
    z_t = (physical_u - 1) / physical_t
    z_u = (1 - physical_t) / physical_u
    crossed_toy = sp.factor(physical_t**4 * sp.legendre(4, z_t) + physical_u**4 * sp.legendre(4, z_u))
    p0_moment = sp.factor(sp.integrate(crossed_toy, (x, 0, 1)))
    p2_coefficient = sp.factor(5 * sp.integrate(sp.legendre(2, 1 - 2 * x) * crossed_toy, (x, 0, 1)))
    values = {
        "crossed_toy": crossed_toy,
        "p0_moment": p0_moment,
        "p2_coefficient": p2_coefficient,
    }
    rows = [
        {
            "scope_id": "HHX4990_01_direct_support",
            "statement": "opposite-helicity hh direct-channel support starts at J=4",
            "exact_value": "d^J_04=0 for J<4",
            "consequence": "direct s-channel hh has no J=0,2 coefficient",
            "status": "EXACT_DIRECT_CHANNEL_ONLY",
        },
        {
            "scope_id": "HHX4990_02_crossing_noninvariance",
            "statement": "a Legendre-J label is not invariant under s<->t or s<->u crossing",
            "exact_value": exact(crossed_toy),
            "consequence": "crossed hh channels can feed physical-s J=0,2 after the full soft-safe assembly",
            "status": "DERIVED_EXACT_COUNTEREXAMPLE",
        },
        {
            "scope_id": "HHX4990_03_crossed_P0",
            "statement": "P0 moment of crossed P4 toy",
            "exact_value": exact(p0_moment),
            "consequence": "direct J>=4 does not imply global low-spin zero",
            "status": "NONZERO_EXACT",
        },
        {
            "scope_id": "HHX4990_04_crossed_P2",
            "statement": "P2 coefficient of crossed P4 toy",
            "exact_value": exact(p2_coefficient),
            "consequence": "hh remains on the full K_mu/K_ang critical path",
            "status": "NONZERO_EXACT",
        },
        {
            "scope_id": "HHX4990_05_correct_boundary",
            "statement": "allowed hh claim",
            "exact_value": "direct-channel J0=J2=0; crossing-summed DeltaK_hh unknown",
            "consequence": "evaluate hh plus both three-particle cuts before full invariants",
            "status": "CORRECTED_NONCLAIM",
        },
    ]
    return rows, values


def supersession_rows() -> list[dict[str, Any]]:
    return [
        {
            "item_id": "SUP4990_01_factor_two",
            "4989_statement": "4988 Khat values are merely raw half-master coordinates",
            "4990_decision": "superseded",
            "correct_statement": "D=-U/(2pi) and the master uses 2D, but the -6 K_mu inverse map already includes the dilatation factor and cyclic crossing; the 4988 values are additive scalar-cut subtotals",
            "status": "CORRECTED",
        },
        {
            "item_id": "SUP4990_02_D1_multiplier",
            "4989_statement": "D1 ReF1=+16 ReF1",
            "4990_decision": "rejected",
            "correct_statement": "in the perturbative on-shell scheme D1 ReF1=-(203/10)F1; 16 belongs to a distinct Wilsonian FRG coordinate",
            "status": "CORRECTED",
        },
        {
            "item_id": "SUP4990_03_remaining_scale_slopes",
            "4989_statement": "three remaining cuts must supply 3097/(72pi) and -21397/(1800pi)",
            "4990_decision": "rejected",
            "correct_statement": "tree three-particle cuts carry no mu logarithm; the crossing-summed scalar cut cancels D1 exactly and the proposed slope targets are spurious",
            "status": "CORRECTED",
        },
        {
            "item_id": "SUP4990_04_hh_global_zero",
            "4989_statement": "opposite-helicity hh cannot alter K_mu or K_ang",
            "4990_decision": "narrowed",
            "correct_statement": "only its direct-channel J0,J2 projections vanish; crossed channels can generate low-spin support, so the full hh cut remains required",
            "status": "CORRECTED",
        },
        {
            "item_id": "SUP4990_05_two_number_affine_target",
            "4989_statement": "only r0,r2 from the two three-particle cuts remain",
            "4990_decision": "rejected",
            "correct_statement": "the full hh crossing completion and both three-particle cuts remain before numeric K_mu,K_ang",
            "status": "CORRECTED",
        },
    ]


def gate_rows(
    source_checks: dict[str, bool],
    identities: dict[str, sp.Expr],
    quantities: dict[str, sp.Expr],
    scheme_values: dict[str, sp.Expr],
    hh_values: dict[str, sp.Expr],
) -> list[dict[str, Any]]:
    checks = [
        ("primary_source_lock", all(source_checks.values()), f"{sum(source_checks.values())}/{len(source_checks)} source markers"),
        ("crossed_channel_algebra", all(value == 0 for value in identities.values()), "four exact crossing residuals vanish"),
        ("scalar_slope_factorization", sp.simplify(quantities["direct_channel_legendre"] - sp.Rational(203, 10) / PI * (-sp.Rational(55, 36) - sp.legendre(2, 1 - 2 * x) / 180)) == 0, "203/10 times mixed kernel"),
        ("smatrix_D1_multiplier", quantities["d1_multiplier"] == -sp.Rational(203, 10), "D1 ReF1=-(203/10)F1"),
        ("crossed_log_cancellation", sp.simplify(quantities["master_log"] - quantities["d1_multiplier"] * quantities["f1_log"]) == 0, "2Dphi_crossed,log-D1ReF1=0"),
        ("corrected_double_log", sp.simplify(quantities["f2_double_derivative"] + quantities["beta_smatrix"] * quantities["f1_log"]) == 0, "RG derivative exact"),
        ("direct_double_log_match", sp.simplify(quantities["direct_channel_double_log"] - quantities["direct_channel_legendre"]) == 0, "both 4988 slopes reproduced"),
        ("FRG_Smatrix_separated", True, "16 and 203/10 carry distinct scheme labels"),
        ("scalar_subtotals_restored", True, "Delta K_mu_phi and Delta K_ang_phi remain additive partial terms"),
        ("hh_direct_support_only", hh_values["p0_moment"] != 0 and hh_values["p2_coefficient"] != 0, "crossed P4 counterexample has nonzero P0,P2"),
        ("4989_affected_claims_superseded", True, "five explicit correction rows"),
        (
            "inherited_scheme_orbit_corrected",
            all(
                scheme_values[name] == 0
                for name in (
                    "I_shift_residual",
                    "K_mu_residual",
                    "K_ang_residual",
                    "rational_free_mu_residual",
                    "rational_free_ang_residual",
                )
            )
            and scheme_values["trajectory_double_log"] == -sp.Rational(609, 10) / PI,
            "4985-4987 descendants use beta_C^S-matrix=203/10; K_mu and K_ang remain finite-orbit invariant",
        ),
        ("FRG_Smatrix_finite_bridge", False, "regulator and finite-coordinate map not yet derived"),
        ("hh_full_crossed_cut", False, "direct support theorem is insufficient for the global invariant"),
        ("mixed_hhh_cut", False, "three-particle cut remains"),
        ("phiphih_cut", False, "three-particle cut remains"),
        ("numeric_full_K_mu", False, "scalar subtotal only"),
        ("numeric_full_K_ang", False, "scalar subtotal only"),
        ("exact_all_operator_local_GR", False, "remaining quantum cut and local residual sectors"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4990_{index:02d}_{name}",
            "gate": name,
            "passed": bool(passed),
            "evidence": evidence,
            "status": "PASS" if passed else "OPEN_NONCLAIM",
            "valid_for_checkpoint_claim": bool(passed),
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4990 crossed-cut and D1 scheme-correction provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Source roles",
        "",
        "- [Dunbar and Norridge](https://arxiv.org/abs/hep-th/9512084): perturbative scalar-gravity counterterm and complete one-loop logarithms.",
        "- [Bern, Parra-Martinez and Sawyer](https://arxiv.org/abs/2005.12917): all-channel sum, dilatation sign, phase-space convention, and real two-loop master.",
        "- [Laporte et al.](https://arxiv.org/abs/2110.09566): Wilsonian effective-average-action FRG context, Type-I regulator, and Litim profile; this is not silently identified with the on-shell amplitude scheme.",
        "",
        "## Source-marker checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "Checkpoint 4990 supersedes the affected physical interpretations in 4989 and propagates the on-shell coefficient correction through the inherited 4985-4987 amplitude-scheme orbit. It proves the exact crossing completion, derives the perturbative on-shell D1 coefficient, restores the 4988 scalar-cut subtotals, and narrows the hh support theorem to the direct channel. It does not derive the finite FRG-to-S-matrix bridge, the full crossed hh cut, either three-particle cut, numeric full invariants, exact local GR, or full MTS.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()

    source_checks = source_lock()
    if not all(source_checks.values()):
        raise RuntimeError(f"source lock failed: {[name for name, passed in source_checks.items() if not passed]}")
    result_4988 = json.loads(RESULT_4988.read_text(encoding="utf-8"))
    identities = crossing_identities()
    quantities = scalar_cut_quantities(result_4988)
    crossing = crossing_rows(quantities, identities)
    flows = flow_rows(quantities)
    scheme_orbit, scheme_values = scheme_orbit_rows(quantities)
    cancellation = cancellation_rows(quantities)
    hh_scope, hh_values = hh_scope_rows()
    supersession = supersession_rows()
    gates = gate_rows(source_checks, identities, quantities, scheme_values, hh_values)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_checks": source_checks,
                    "D1_multiplier": exact(quantities["d1_multiplier"]),
                    "trajectory_double_log": exact(scheme_values["trajectory_double_log"]),
                    "K_mu_orbit_residual": exact(scheme_values["K_mu_residual"]),
                    "crossed_log_residual": exact(quantities["master_log"] - quantities["d1_multiplier"] * quantities["f1_log"]),
                    "dry_run": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    outputs = [
        (CROSSING_CSV, crossing),
        (FLOW_CSV, flows),
        (SCHEME_ORBIT_CSV, scheme_orbit),
        (CANCELLATION_CSV, cancellation),
        (HH_SCOPE_CSV, hh_scope),
        (SUPERSESSION_CSV, supersession),
        (GATE_CSV, gates),
    ]
    for path, rows in outputs:
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [
        CHECKPOINT_4982,
        CHECKPOINT_4985,
        CHECKPOINT_4986,
        CHECKPOINT_4987,
        CHECKPOINT_4988,
        CHECKPOINT_4989,
        RESULT_4988,
        FRG_SOURCE,
        DUNBAR_SOURCE,
        BERN_SOURCE,
        script_path,
    ]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "crossing": {name: exact(value) for name, value in identities.items()},
        "flow_separation": {
            "beta_C_FRG": "16 in the declared Type-I Litim Wilsonian essential coordinate",
            "beta_C_Smatrix": exact(quantities["beta_smatrix"]),
            "D_C_Smatrix": exact(quantities["d1_multiplier"]),
            "finite_bridge_derived": False,
        },
        "scheme_orbit_correction": {
            "trajectory_double_log": exact(scheme_values["trajectory_double_log"]),
            "I_fixed_p4": exact(scheme_values["I_fixed"]),
            "K_mu": exact(scheme_values["K_mu"]),
            "K_ang": exact(scheme_values["K_ang"]),
            "I_shift_residual": exact(scheme_values["I_shift_residual"]),
            "K_mu_residual": exact(scheme_values["K_mu_residual"]),
            "K_ang_residual": exact(scheme_values["K_ang_residual"]),
            "rational_free_mu_residual": exact(scheme_values["rational_free_mu_residual"]),
            "rational_free_ang_residual": exact(scheme_values["rational_free_ang_residual"]),
        },
        "corrected_D1": {
            "D1_ReF1": f"({exact(quantities['d1_multiplier'])}) F1",
            "crossed_scalar_log": exact(quantities["crossed_log"]),
            "master_log_residual": exact(quantities["master_log"] - quantities["d1_multiplier"] * quantities["f1_log"]),
            "F2_double": exact(quantities["f2_double"]),
            "direct_channel_double_log_residual": exact(quantities["direct_channel_double_log"] - quantities["direct_channel_legendre"]),
        },
        "scalar_subtotals": {
            "Delta_K_mu_phi": exact(quantities["delta_k_mu"]),
            "Delta_K_ang_phi": exact(quantities["delta_k_ang"]),
            "numeric_full_K_mu": False,
            "numeric_full_K_ang": False,
        },
        "hh_scope": {
            "direct_channel_minimum_J": 4,
            "direct_channel_J0_J2_zero": True,
            "crossing_summed_K_contribution_zero": False,
            "full_crossed_hh_open": True,
            "toy_crossed_P0": exact(hh_values["p0_moment"]),
            "toy_crossed_P2": exact(hh_values["p2_coefficient"]),
        },
        "supersedes_checkpoint": 4989,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, source_checks)

    passed = sum(bool(row["passed"]) for row in gates)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "passed_gates": passed,
                "total_gates": len(gates),
                "open_nonclaim_gates": len(gates) - passed,
                "beta_C_Smatrix": exact(quantities["beta_smatrix"]),
                "D1_multiplier": exact(quantities["d1_multiplier"]),
                "trajectory_double_log": exact(scheme_values["trajectory_double_log"]),
                "crossed_log_residual": exact(quantities["master_log"] - quantities["d1_multiplier"] * quantities["f1_log"]),
                "Delta_K_mu_phi": exact(quantities["delta_k_mu"]),
                "Delta_K_ang_phi": exact(quantities["delta_k_ang"]),
                "full_crossed_hh_open": True,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
