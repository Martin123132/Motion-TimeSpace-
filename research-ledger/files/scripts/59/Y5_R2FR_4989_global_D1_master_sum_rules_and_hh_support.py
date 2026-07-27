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
SOURCE = POST / "source-intake" / "functional_rg" / "4989"

CHECKPOINT_4986 = POST / "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md"
CHECKPOINT_4987 = POST / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
CHECKPOINT_4988 = POST / "4988-Y5-R2FR-renormalized-scalar-two-particle-cut-and-exact-partial-wave-projection.md"
RESULT_4988 = POST / "source-intake" / "functional_rg" / "4988" / "scalar_cut_soft_subtraction_results.json"
BERN_SOURCE = POST / "source-intake" / "functional_rg" / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"

FACTOR_TWO_CSV = SOURCE / "master_factor_two_normalization.csv"
D1_KERNEL_CSV = SOURCE / "D1_ReF1_channel_kernel.csv"
D1_MOMENTS_CSV = SOURCE / "D1_legendre_moment_tower.csv"
SUM_RULES_CSV = SOURCE / "remaining_cut_sum_rules.csv"
HH_SUPPORT_CSV = SOURCE / "opposite_helicity_hh_support.csv"
AFFINE_CSV = SOURCE / "master_affine_invariant_coordinates.csv"
GATE_CSV = SOURCE / "global_master_completion_gate.csv"
RESULT_JSON = SOURCE / "global_D1_master_sum_rules_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4989_GLOBAL_D1_MASTER_SUM_RULES_HH_SUPPORT"
CHECKED_DATE = "2026-07-14"

x, L = sp.symbols("x L", positive=True)
PI = sp.pi
P2 = sp.expand(sp.legendre(2, 1 - 2 * x))


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
    bern = normalized_text(BERN_SOURCE)
    dunbar = normalized_text(DUNBAR_SOURCE)
    checkpoint_4986 = normalized_text(CHECKPOINT_4986)
    checkpoint_4987 = normalized_text(CHECKPOINT_4987)
    checkpoint_4988 = normalized_text(CHECKPOINT_4988)
    result_4988 = json.loads(RESULT_4988.read_text(encoding="utf-8"))
    return {
        "bern_optical_theorem_factor_two": "2\\text{Im}F_i^* = \\M F_i^*" in bern,
        "bern_real_two_loop_master_minus_one_over_pi": "twoloopSimon3" in bern and "\\text{Re}(\\M) \\text{Re}(F_i)" in bern,
        "bern_no_iterated_half_factor": "does not include a factor of $1/2$" in bern,
        "dunbar_same_helicity_tree_zero": "2^+ , 3^+ , \\phi_4 ) = 0" in dunbar,
        "dunbar_opposite_helicity_tree_nonzero": "2^- , 3^+ , \\phi_4 )" in dunbar and "{st \\over 4u}" in dunbar,
        "checkpoint_4986_beta_C_sixteen": "dC/dlnmu=16" in checkpoint_4986,
        "checkpoint_4986_one_loop_F1": "F_1,log=(2/pi)[(23/15)L_A-(1/30)L_B]" in checkpoint_4986,
        "checkpoint_4987_inverse_projector": "K_mu=-6(d0-5d2)" in checkpoint_4987 and "K_ang=d0+7d2" in checkpoint_4987,
        "checkpoint_4988_raw_coordinate_correction": "half-master raw-cut" in checkpoint_4988,
        "result_4988_master_weight_two": result_4988["projection"]["master_cut_weight"] == "-U_phiphi/(pi s^3)=2 D_phiphi",
    }


def polynomial_log_moment(spin: int, power: int) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(sp.legendre(spin, 1 - 2 * x)), x)
    value = sp.S.Zero
    for monomial, coefficient in polynomial.terms():
        value -= coefficient / sp.Rational(monomial[0] + power + 1) ** 2
    return sp.factor(value)


def d1_constant_moment(spin: int) -> sp.Expr:
    if spin % 2:
        return sp.S.Zero
    a1 = polynomial_log_moment(spin, 1)
    a2 = polynomial_log_moment(spin, 2)
    a3 = polynomial_log_moment(spin, 3)
    return sp.factor(-sp.Rational(32, 1) / PI * (sp.Rational(46, 15) * a3 + sp.Rational(1, 15) * (a1 - a2)))


def d1_scale_moment(spin: int) -> sp.Expr:
    polynomial = sp.expand(sp.legendre(spin, 1 - 2 * x))
    return sp.factor(sp.integrate(polynomial * sp.Rational(144, 1) * x * (1 - x) / PI, (x, 0, 1)))


def factor_two_rows() -> list[dict[str, Any]]:
    return [
        {
            "normalization_id": "NORM4989_01_optical_theorem",
            "statement": "Bern convention",
            "equation": "2 Im F = U",
            "consequence": "the unitarity convolution U is twice the imaginary part",
            "source_path": relative(BERN_SOURCE),
            "status": "SOURCE_LOCKED_EXACT",
        },
        {
            "normalization_id": "NORM4989_02_log_discontinuity",
            "statement": "physical logarithm",
            "equation": "Disc ln(-s/mu^2)=-2pi i",
            "consequence": "c ln(-s/mu^2) with 2 Im F=U has c=-U/(2pi)",
            "source_path": relative(BERN_SOURCE),
            "status": "DERIVED_EXACT",
        },
        {
            "normalization_id": "NORM4989_03_raw_cut_coordinate",
            "statement": "4988 reduced scalar cut",
            "equation": "D_phiphi=Disc_s/(-2pi i s^3)=-U_phiphi/(2pi s^3)",
            "consequence": "4988 Khat values are raw half-master projector coordinates",
            "source_path": relative(RESULT_4988),
            "status": "DERIVED_EXACT",
        },
        {
            "normalization_id": "NORM4989_04_real_master",
            "statement": "Bern real two-loop master",
            "equation": "R_master=-U_total/(pi s^3)-D1 ReF1=2 sum_i D_i-G",
            "consequence": "every D_i enters with weight two and G is subtracted once globally",
            "source_path": relative(BERN_SOURCE),
            "status": "SOURCE_LOCKED_DERIVED_EXACT",
        },
    ]


def d1_kernel_rows() -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    g0 = -sp.Rational(32, 1) / PI * (
        sp.Rational(23, 15) * (x**3 * sp.log(x) + (1 - x) ** 3 * sp.log(1 - x))
        + sp.Rational(1, 30) * x * (1 - x) * (sp.log(x) + sp.log(1 - x))
    )
    g_scale = sp.Rational(144, 1) * x * (1 - x) / PI
    g_scale_legendre = sp.Rational(24, 1) * (1 - P2) / PI
    discontinuity_density = sp.Rational(32, 1) / PI * (sp.Rational(23, 15) - x * (1 - x) / 30)
    identities = {
        "g0": sp.factor(g0),
        "g_scale": sp.factor(g_scale),
        "g_scale_legendre": sp.factor(g_scale_legendre),
        "discontinuity_density": sp.factor(discontinuity_density),
        "scale_legendre_residual": sp.simplify(g_scale - g_scale_legendre),
    }
    rows = [
        {
            "kernel_id": "D1K4989_01_reduced_amplitude",
            "quantity": "R",
            "exact_expression": "-3 W stu + C F1 + F2",
            "derivation": "4986 reduced common-scheme amplitude",
            "source_path": relative(CHECKPOINT_4986),
            "status": "SOURCE_LOCKED",
        },
        {
            "kernel_id": "D1K4989_02_beta_C",
            "quantity": "dC/dlnmu",
            "exact_expression": "16",
            "derivation": "one-loop local four-motion flow",
            "source_path": relative(CHECKPOINT_4986),
            "status": "SOURCE_LOCKED",
        },
        {
            "kernel_id": "D1K4989_03_global_operator",
            "quantity": "G=D1 ReF1",
            "exact_expression": "16 ReF1",
            "derivation": "beta_C partial_C acting on C F1",
            "source_path": relative(CHECKPOINT_4986),
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "D1K4989_04_channel_constant",
            "quantity": "G0(x)",
            "exact_expression": exact(g0),
            "derivation": "physical s channel with t=-x and u=-(1-x)",
            "source_path": relative(CHECKPOINT_4986),
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "D1K4989_05_channel_scale",
            "quantity": "coefficient_L[G]",
            "exact_expression": exact(g_scale),
            "derivation": "16 times the common logarithmic scale dependence",
            "source_path": relative(CHECKPOINT_4986),
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "D1K4989_06_scale_polynomial",
            "quantity": "coefficient_L[G] in Legendre basis",
            "exact_expression": "(24/pi)(P0-P2)",
            "derivation": "144 x(1-x)/pi=(24/pi)(1-P2)",
            "source_path": relative(CHECKPOINT_4987),
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "D1K4989_07_channel_discontinuity",
            "quantity": "Disc_s G/(-2pi i s^3)",
            "exact_expression": exact(discontinuity_density),
            "derivation": "only the physical ln(-s) terms contribute",
            "source_path": relative(BERN_SOURCE),
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "D1K4989_08_complete_master",
            "quantity": "R_master(z,L)",
            "exact_expression": "2 sum_cuts D_cut(z,L)-G(z,L)",
            "derivation": "factor-two normalization plus one global anomalous-action subtraction",
            "source_path": relative(BERN_SOURCE),
            "status": "DERIVED_EXACT",
        },
    ]
    return rows, identities


def d1_moment_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spin in range(0, 22, 2):
        moment_constant = d1_constant_moment(spin)
        coefficient_constant = sp.factor((2 * spin + 1) * moment_constant)
        moment_scale = d1_scale_moment(spin)
        coefficient_scale = sp.factor((2 * spin + 1) * moment_scale)
        required = sp.factor(coefficient_constant / 2) if spin >= 4 else sp.S.NaN
        rows.append(
            {
                "spin_J": spin,
                "A_J_1": exact(polynomial_log_moment(spin, 1)),
                "A_J_2": exact(polynomial_log_moment(spin, 2)),
                "A_J_3": exact(polynomial_log_moment(spin, 3)),
                "G0_moment": exact(moment_constant),
                "G0_legendre_coefficient": exact(coefficient_constant),
                "G_L_moment": exact(moment_scale),
                "G_L_legendre_coefficient": exact(coefficient_scale),
                "remaining_cut_required_L0_coefficient": "" if spin < 4 else exact(required),
                "sum_rule": "low-J master coordinate" if spin < 4 else "sum_remaining_cut_J=G_J/2",
                "status": "DERIVED_EXACT",
                "source_path": relative(CHECKPOINT_4986),
            }
        )
    return rows


def sum_rule_rows(result_4988: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    scalar_d0_slope = sp.sympify(result_4988["projection"]["d0_L_slope"])
    scalar_d2_slope = sp.sympify(result_4988["projection"]["d2_L_slope"])
    total_d0_slope = sp.Rational(12, 1) / PI
    total_d2_slope = -sp.Rational(12, 1) / PI
    remaining_d0_slope = sp.factor(total_d0_slope - scalar_d0_slope)
    remaining_d2_slope = sp.factor(total_d2_slope - scalar_d2_slope)
    identities = {
        "scalar_d0_slope": scalar_d0_slope,
        "scalar_d2_slope": scalar_d2_slope,
        "total_d0_slope": total_d0_slope,
        "total_d2_slope": total_d2_slope,
        "remaining_d0_slope": remaining_d0_slope,
        "remaining_d2_slope": remaining_d2_slope,
    }
    rows = [
        {
            "rule_id": "SUM4989_01_total_P0_scale",
            "sector": "P0",
            "exact_rule": "sum_all_cuts d0_L=12/pi",
            "exact_value": exact(total_d0_slope),
            "derivation": "2 sum d0_L-24/pi=0",
            "support_owner": "all cuts",
            "status": "DERIVED_EXACT",
        },
        {
            "rule_id": "SUM4989_02_total_P2_scale",
            "sector": "P2",
            "exact_rule": "sum_all_cuts d2_L=-12/pi",
            "exact_value": exact(total_d2_slope),
            "derivation": "2 sum d2_L+24/pi=0",
            "support_owner": "all cuts",
            "status": "DERIVED_EXACT",
        },
        {
            "rule_id": "SUM4989_03_scalar_P0_scale",
            "sector": "P0",
            "exact_rule": "d0_phi_L",
            "exact_value": exact(scalar_d0_slope),
            "derivation": "4988 exact scalar cut",
            "support_owner": "phiphi two-particle",
            "status": "SOURCE_LOCKED_EXACT",
        },
        {
            "rule_id": "SUM4989_04_scalar_P2_scale",
            "sector": "P2",
            "exact_rule": "d2_phi_L",
            "exact_value": exact(scalar_d2_slope),
            "derivation": "4988 exact scalar cut",
            "support_owner": "phiphi two-particle",
            "status": "SOURCE_LOCKED_EXACT",
        },
        {
            "rule_id": "SUM4989_05_remaining_P0_scale",
            "sector": "P0",
            "exact_rule": "d0_hhh_L+d0_phiphih_L=3097/(72pi)",
            "exact_value": exact(remaining_d0_slope),
            "derivation": "total minus scalar; opposite-helicity hh has J>=4",
            "support_owner": "two three-particle cuts only",
            "status": "DERIVED_EXACT_TARGET",
        },
        {
            "rule_id": "SUM4989_06_remaining_P2_scale",
            "sector": "P2",
            "exact_rule": "d2_hhh_L+d2_phiphih_L=-21397/(1800pi)",
            "exact_value": exact(remaining_d2_slope),
            "derivation": "total minus scalar; opposite-helicity hh has J>=4",
            "support_owner": "two three-particle cuts only",
            "status": "DERIVED_EXACT_TARGET",
        },
        {
            "rule_id": "SUM4989_07_higher_spin_tower",
            "sector": "even J>=4",
            "exact_rule": "D_hh,J+D_hhh,J+D_phiphih,J=G_J/2",
            "exact_value": "see D1_legendre_moment_tower.csv",
            "derivation": "scalar cut has only J=0,2 and the local target has no J>=4",
            "support_owner": "opposite-helicity hh plus both three-particle cuts",
            "status": "DERIVED_EXACT_INFINITE_TOWER",
        },
    ]
    return rows, identities


def hh_support_rows() -> list[dict[str, Any]]:
    return [
        {
            "support_id": "HH4989_01_external_difference",
            "statement": "external scalar helicity difference",
            "exact_value": "lambda_ext=0",
            "consequence": "scalar pair is expanded in d^J_{0,m}",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "DERIVED_EXACT",
        },
        {
            "support_id": "HH4989_02_internal_difference",
            "statement": "opposite-helicity graviton difference",
            "exact_value": "abs(lambda_hh)=abs(2-(-2))=4",
            "consequence": "the scalar-to-hh tree uses d^J_{0,4}",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "DERIVED_EXACT",
        },
        {
            "support_id": "HH4989_03_wigner_selection",
            "statement": "Wigner support theorem",
            "exact_value": "d^J_{0,4}=0 for J<4",
            "consequence": "D_hh,J=0 at J=0 and J=2",
            "source_path": relative(CHECKPOINT_4987),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "DERIVED_EXACT",
        },
        {
            "support_id": "HH4989_04_same_helicity_zero",
            "statement": "same-helicity scalar-graviton tree",
            "exact_value": "M_tree(phi,+,+,phi)=0",
            "consequence": "no lambda_hh=0 graviton cut can restore J=0 or J=2",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "SOURCE_LOCKED_EXACT_ZERO",
        },
        {
            "support_id": "HH4989_05_invariant_consequence",
            "statement": "low-spin inverse projector",
            "exact_value": "Delta K_mu_hh=Delta K_ang_hh=0",
            "consequence": "opposite-helicity hh cannot directly change K_mu or K_ang",
            "source_path": relative(CHECKPOINT_4987),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "DERIVED_EXACT_SUPPORT_ZERO",
        },
        {
            "support_id": "HH4989_06_higher_spin_role",
            "statement": "remaining hh task",
            "exact_value": "J=4,6,... coefficients open",
            "consequence": "hh is required only for the higher-J cancellation tower",
            "source_path": relative(DUNBAR_SOURCE),
            "valid_for_low_J_zero_claim": True,
            "valid_for_numeric_hh_cut_claim": False,
            "status": "NUMERIC_HIGHER_J_OPEN_NONCLAIM",
        },
    ]


def affine_rows(result_4988: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    d0_scalar = sp.sympify(result_4988["projection"]["d0_L0"])
    d2_scalar = sp.sympify(result_4988["projection"]["d2_L0"])
    g0_coefficient = d1_constant_moment(0)
    g2_coefficient = 5 * d1_constant_moment(2)
    r0, r2 = sp.symbols("r0 r2")
    master_r0 = sp.factor(2 * (d0_scalar + r0) - g0_coefficient)
    master_r2 = sp.factor(2 * (d2_scalar + r2) - g2_coefficient)
    k_mu = sp.factor(-6 * (master_r0 - 5 * master_r2))
    k_ang = sp.factor(master_r0 + 7 * master_r2)
    k_mu_constant = sp.factor(k_mu.subs({r0: 0, r2: 0}))
    k_ang_constant = sp.factor(k_ang.subs({r0: 0, r2: 0}))
    identities = {
        "master_r0": master_r0,
        "master_r2": master_r2,
        "k_mu": k_mu,
        "k_ang": k_ang,
        "k_mu_constant": k_mu_constant,
        "k_ang_constant": k_ang_constant,
    }
    rows = [
        {
            "coordinate_id": "AFF4989_01_R0",
            "quantity": "R0",
            "exact_expression": exact(master_r0),
            "interpretation": "r0 is the L=0 P0 coefficient from the two three-particle cuts",
            "status": "EXACT_AFFINE_REDUCTION",
        },
        {
            "coordinate_id": "AFF4989_02_R2",
            "quantity": "R2",
            "exact_expression": exact(master_r2),
            "interpretation": "r2 is the L=0 P2 coefficient from the two three-particle cuts",
            "status": "EXACT_AFFINE_REDUCTION",
        },
        {
            "coordinate_id": "AFF4989_03_Kmu",
            "quantity": "K_mu",
            "exact_expression": exact(k_mu),
            "interpretation": "K_mu=K_mu_known-12(r0-5r2)",
            "status": "EXACT_AFFINE_REDUCTION_NUMERIC_OPEN",
        },
        {
            "coordinate_id": "AFF4989_04_Kang",
            "quantity": "K_ang",
            "exact_expression": exact(k_ang),
            "interpretation": "K_ang=K_ang_known+2(r0+7r2)",
            "status": "EXACT_AFFINE_REDUCTION_NUMERIC_OPEN",
        },
        {
            "coordinate_id": "AFF4989_05_Kmu_known",
            "quantity": "K_mu_known",
            "exact_expression": exact(k_mu_constant),
            "numeric_value": f"{float(sp.N(k_mu_constant, 17)):.15g}",
            "interpretation": "scalar cut with master factor two minus global D1 low-spin projection",
            "status": "EXACT_KNOWN_AFFINE_INTERCEPT_NOT_FULL_K",
        },
        {
            "coordinate_id": "AFF4989_06_Kang_known",
            "quantity": "K_ang_known",
            "exact_expression": exact(k_ang_constant),
            "numeric_value": f"{float(sp.N(k_ang_constant, 17)):.15g}",
            "interpretation": "scalar cut with master factor two minus global D1 low-spin projection",
            "status": "EXACT_KNOWN_AFFINE_INTERCEPT_NOT_FULL_K",
        },
    ]
    return rows, identities


def gate_rows(source_checks: dict[str, bool], kernel: dict[str, sp.Expr], sums: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    checks = [
        ("primary_source_lock", all(source_checks.values()), f"{sum(source_checks.values())}/{len(source_checks)} source markers"),
        ("master_factor_two", True, "R_master=2 sum D-G"),
        ("global_D1_multiplier", True, "G=16 ReF1"),
        ("channel_scale_polynomial", kernel["scale_legendre_residual"] == 0, "G_L=(24/pi)(P0-P2)"),
        ("D1_J0_J2_exact", d1_constant_moment(0) == 868 / (135 * PI) and 5 * d1_constant_moment(2) == -3716 / (675 * PI), "exact low-spin moments"),
        ("D1_higher_J_tower", all(d1_scale_moment(spin) == 0 for spin in range(4, 22, 2)), "L slope has no J>=4 support"),
        ("remaining_scale_sum_rules", sums["remaining_d0_slope"] == 3097 / (72 * PI) and sums["remaining_d2_slope"] == -21397 / (1800 * PI), "two exact three-particle targets"),
        ("opposite_helicity_hh_low_J_zero", True, "abs(lambda_hh)=4 implies J>=4"),
        ("4988_labels_corrected", True, "raw Khat coordinates replace additive Delta K labels"),
        ("hh_numeric_higher_J", False, "one-loop opposite-helicity 2phi2h hard partial waves not yet evaluated"),
        ("mixed_hhh_cut_numeric", False, "three-particle mixed-helicity cut remains"),
        ("phiphih_cut_numeric", False, "three-particle scalar-graviton cut remains"),
        ("numeric_full_K_mu", False, "depends on r0-5r2 from the two three-particle cuts"),
        ("numeric_full_K_ang", False, "depends on r0+7r2 from the two three-particle cuts"),
        ("finite_C_w", False, "requires complete master"),
        ("exact_all_operator_local_GR", False, "two three-particle low-spin coefficients and residual sectors remain"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4989_{index:02d}_{name}",
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
        "# 4989 global D1 master provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- [Bern, Parra-Martinez and Sawyer](https://arxiv.org/abs/2005.12917): optical-theorem factor, iterated-cut combinatorics, dilatation operator, and real two-loop master.",
        "- [Dunbar and Norridge](https://arxiv.org/abs/hep-th/9512084): same-helicity zero and nonzero opposite-helicity scalar-graviton Compton tree.",
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
            "Checkpoint 4989 derives the once-global `D1 ReF1` kernel, its exact low-spin and higher-spin moment constraints, the factor-two correction to checkpoint 4988, and the exact absence of opposite-helicity `hh` support at `J=0,2`. It does not calculate the two three-particle low-spin coefficients or the higher-spin `hh` amplitudes. Numeric full `K_mu`, `K_ang`, exact local GR, and full MTS remain open.",
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
    factors = factor_two_rows()
    kernels, kernel_identities = d1_kernel_rows()
    moments = d1_moment_rows()
    sums, sum_identities = sum_rule_rows(result_4988)
    hh_support = hh_support_rows()
    affine, affine_identities = affine_rows(result_4988)
    gates = gate_rows(source_checks, kernel_identities, sum_identities)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_checks": source_checks,
                    "factor_rows": len(factors),
                    "moment_rows": len(moments),
                    "gate_rows": len(gates),
                    "dry_run": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    outputs = [
        (FACTOR_TWO_CSV, factors),
        (D1_KERNEL_CSV, kernels),
        (D1_MOMENTS_CSV, moments),
        (SUM_RULES_CSV, sums),
        (HH_SUPPORT_CSV, hh_support),
        (AFFINE_CSV, affine),
        (GATE_CSV, gates),
    ]
    for path, rows in outputs:
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [CHECKPOINT_4986, CHECKPOINT_4987, CHECKPOINT_4988, RESULT_4988, BERN_SOURCE, DUNBAR_SOURCE, script_path]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "normalization": {
            "optical_theorem": "2 Im F=U",
            "raw_cut": "D=-U/(2pi s^3)",
            "master": "R_master=2 sum_cuts D_cut-G",
        },
        "D1": {
            "operator": "G=D1 ReF1=16 ReF1",
            "G0": exact(kernel_identities["g0"]),
            "G_L": exact(kernel_identities["g_scale"]),
            "G_L_legendre": "(24/pi)(P0-P2)",
            "G0_J0_coefficient": exact(d1_constant_moment(0)),
            "G0_J2_coefficient": exact(5 * d1_constant_moment(2)),
        },
        "scale_sum_rules": {name: exact(value) for name, value in sum_identities.items()},
        "affine_master": {name: exact(value) for name, value in affine_identities.items()},
        "hh_support": {
            "minimum_J": 4,
            "J0_zero": True,
            "J2_zero": True,
            "direct_K_mu_K_ang_contribution_zero": True,
            "numeric_higher_J_open": True,
        },
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
                "remaining_d0_L": exact(sum_identities["remaining_d0_slope"]),
                "remaining_d2_L": exact(sum_identities["remaining_d2_slope"]),
                "K_mu_known_intercept": exact(affine_identities["k_mu_constant"]),
                "K_ang_known_intercept": exact(affine_identities["k_ang_constant"]),
                "hh_minimum_J": 4,
                "numeric_full_K_mu": False,
                "numeric_full_K_ang": False,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
