from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4965"

RESULT_JSON = SOURCE / "p8_basis_projector_and_partial_flow_results.json"
BASIS_CSV = SOURCE / "p8_on_shell_basis.csv"
PROJECTOR_CSV = SOURCE / "p8_helicity_projector.csv"
MOTION_SOURCE_CSV = SOURCE / "p8_minimal_motion_scalar_source.csv"
POWER_COUNT_CSV = SOURCE / "p8_parent_source_power_count.csv"
DISPERSIVE_CSV = SOURCE / "p8_C3_dispersive_cone.csv"
COMPACT_CSV = SOURCE / "p8_two_coordinate_compact_domain.csv"
DECISION_CSV = SOURCE / "p8_flow_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4965_P8_BASIS_HELICITY_PARTIAL_FLOW"
CHECKED_DATE = "2026-07-13"

SOURCE_PATHS = {
    "ruh1908_tex": SOURCE / "src-1908.08050" / "GravityEFTv2_final.tex",
    "li2305_tex": SOURCE / "src-2305.10481" / "main.tex",
    "bern2103_tex": SOURCE / "src-2103.12728" / "GravScatt.tex",
    "ruh1908_pdf": SOURCE / "1908.08050.pdf",
    "li2305_pdf": SOURCE / "2305.10481.pdf",
    "bern2103_pdf": SOURCE / "2103.12728.pdf",
    "motion_4935": POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "motion_sector_entry_results.json",
    "trajectory_4935": POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "completed_fixed_point_trajectory_results.json",
    "trajectory_script_4935": POST
    / "scripts"
    / "Y5_R2FR_4935_completed_fixed_point_trajectory.py",
    "C3_4963": POST
    / "source-intake"
    / "functional_rg"
    / "4963"
    / "strong_field_C3_and_scalar_branch_results.json",
    "p8_tail_4964": POST
    / "source-intake"
    / "functional_rg"
    / "4964"
    / "p8plus_tail_norm_gate.csv",
    "p4_quotient_4964": POST
    / "source-intake"
    / "functional_rg"
    / "4964"
    / "four_derivative_quotient_CFF_p8_results.json",
}

EXPECTED_HASHES = {
    "ruh1908_tex": "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
    "li2305_tex": "9a6dfbd91dd9531c5482353adb23c241cc34f4461178f79c71bf8d818923c984",
    "bern2103_tex": "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963",
    "ruh1908_pdf": "0a7488198a3d164e33461bd149a83117be0f005b34363f77d2f8667d04f321b3",
    "li2305_pdf": "3907d2ebad4d563623db777449e5eaec26f44af8de1e4dfdeedf5e9e2e7c2241",
    "bern2103_pdf": "6e6886c133700117d76eefc4d5f0f3fdfa28cb08f3140b24718eea25313ca3ff",
    "motion_4935": "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    "trajectory_4935": "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    "trajectory_script_4935": "ad3199770b67210d14748c5b88c4b9c1cee0796318281adcfe8adb16f1c80f48",
    "C3_4963": "059b52fe849ea13082f5ad86221c85009a7595637e0ad0415b3ea59cbb37a791",
    "p8_tail_4964": "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    "p4_quotient_4964": "752b62cf5f236860739d4200c3c3fbaa52952187a8db06e71fa98051b2fa2b04",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("/", "\\")


def source_checks() -> dict[str, Any]:
    missing = [name for name, path in SOURCE_PATHS.items() if not path.exists()]
    bad_hashes = {
        name: {"expected": EXPECTED_HASHES[name], "actual": digest(path)}
        for name, path in SOURCE_PATHS.items()
        if path.exists() and digest(path) != EXPECTED_HASHES[name]
    }
    texts = {
        name: path.read_text(encoding="utf-8-sig", errors="replace")
        for name, path in SOURCE_PATHS.items()
        if name.endswith("_tex") and path.exists()
    }
    clauses = {
        "ruh_dim8_hilbert": "C_L^4 + C_L^2 C_R^2 + C_R^4" in texts.get("ruh1908_tex", ""),
        "ruh_chiral_definition": "C_{L/R}^{\\mu\\nu\\rho\\sigma} = \\frac{1}{2}" in texts.get("ruh1908_tex", ""),
        "li_dim8_CL4": "C_{\\rm L}^4" in texts.get("li2305_tex", ""),
        "li_dim8_mixed": "C_{\\rm L}^2C_{\\rm R}^2" in texts.get("li2305_tex", ""),
        "bern_helicity_minus": "\\beta_{R^4}^-" in texts.get("bern2103_tex", ""),
        "bern_helicity_plus": "\\beta_{R^4}^+" in texts.get("bern2103_tex", ""),
        "bern_scalar_7560": "1}{7560}" in texts.get("bern2103_tex", ""),
        "bern_scalar_6300": "1}{6300}" in texts.get("bern2103_tex", ""),
        "bern_bound": "| \\beta_{R^3} |^2 \\leq {\\beta_{R^4}^+ \\over m_{\\rm gap}^2}" in texts.get("bern2103_tex", ""),
    }
    if missing or bad_hashes or not all(clauses.values()):
        raise RuntimeError(
            f"source lock failed: missing={missing}; bad_hashes={bad_hashes}; clauses={clauses}"
        )
    return {
        "missing": missing,
        "bad_hashes": bad_hashes,
        "clauses": clauses,
        "hashes": {name: digest(path) for name, path in SOURCE_PATHS.items()},
    }


def derive_p8_basis() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    C_L2, C_R2 = sp.symbols("C_L2 C_R2")
    curvature_even = C_L2 + C_R2
    curvature_odd = -sp.I * (C_L2 - C_R2)
    same = C_L2**2 + C_R2**2
    mixed = C_L2 * C_R2

    O_CC = sp.expand(curvature_even**2)
    O_TT = sp.expand(curvature_odd**2)
    O_CT = sp.expand(curvature_even * curvature_odd)
    checks = {
        "O_CC_map": sp.simplify(O_CC - (same + 2 * mixed)) == 0,
        "O_TT_map": sp.simplify(O_TT - (-same + 2 * mixed)) == 0,
        "O_CT_map": sp.simplify(O_CT + sp.I * (C_L2**2 - C_R2**2)) == 0,
    }

    rows = tagged(
        [
            {
                "basis_id": "B4965_00_raw_CL4",
                "quotient_stage": "4D_on_shell_EOM_IBP_Hilbert",
                "representative": "(C_L^2)^2",
                "helicity_support": "all-minus; conjugate all-plus",
                "reality_action": "paired_with_C_R4",
                "parity": "paired_even_or_odd",
                "independent_parity_even_coordinate": False,
                "status": "RAW_CHIRAL_MONOMIAL",
                "source": "arXiv:1908.08050 Eq.(GravityHilbert); arXiv:2305.10481 pure-gravity table",
            },
            {
                "basis_id": "B4965_01_raw_mixed",
                "quotient_stage": "4D_on_shell_EOM_IBP_Hilbert",
                "representative": "C_L^2 C_R^2",
                "helicity_support": "two-plus_two-minus",
                "reality_action": "self_conjugate",
                "parity": "even",
                "independent_parity_even_coordinate": True,
                "status": "PARITY_EVEN_MIXED_COORDINATE",
                "source": "arXiv:1908.08050 Eq.(GravityHilbert); arXiv:2305.10481 pure-gravity table",
            },
            {
                "basis_id": "B4965_02_raw_CR4",
                "quotient_stage": "4D_on_shell_EOM_IBP_Hilbert",
                "representative": "(C_R^2)^2",
                "helicity_support": "all-plus; conjugate all-minus",
                "reality_action": "paired_with_C_L4",
                "parity": "paired_even_or_odd",
                "independent_parity_even_coordinate": False,
                "status": "RAW_CHIRAL_MONOMIAL",
                "source": "arXiv:1908.08050 Eq.(GravityHilbert)",
            },
            {
                "basis_id": "B4965_03_even_same",
                "quotient_stage": "reality_plus_parity",
                "representative": "(C_L^2)^2+(C_R^2)^2",
                "helicity_support": "all-plus plus all-minus",
                "reality_action": "real",
                "parity": "even",
                "independent_parity_even_coordinate": True,
                "status": "PARITY_EVEN_SAME_CHIRALITY_COORDINATE",
                "source": "derived from the source-locked three-monomial Hilbert coefficient",
            },
            {
                "basis_id": "B4965_04_odd_same",
                "quotient_stage": "selected_parent_parity",
                "representative": "i[(C_L^2)^2-(C_R^2)^2] proportional (C.C)(C.Ctilde)",
                "helicity_support": "parity-odd all-plus/all-minus difference",
                "reality_action": "real_after_i_factor",
                "parity": "odd",
                "independent_parity_even_coordinate": False,
                "status": "EXCLUDED_BY_SELECTED_PARITY_EVEN_BRANCH",
                "source": "arXiv:1908.08050 dimension-8 GRSMEFT basis",
            },
            {
                "basis_id": "B4965_05_real_OCC",
                "quotient_stage": "real_invariant_basis",
                "representative": "O_CC=(C_mnrs C^mnrs)^2",
                "helicity_support": "same plus mixed",
                "reality_action": "real",
                "parity": "even",
                "independent_parity_even_coordinate": True,
                "status": "FIRST_REAL_BASIS_COORDINATE",
                "source": "arXiv:1908.08050 Eq.(GravityVacuumAction) and dimension-8 table",
            },
            {
                "basis_id": "B4965_06_real_Ott",
                "quotient_stage": "real_invariant_basis",
                "representative": "O_tt=(C_mnrs Ctilde^mnrs)^2",
                "helicity_support": "same plus mixed",
                "reality_action": "real",
                "parity": "even",
                "independent_parity_even_coordinate": True,
                "status": "SECOND_REAL_BASIS_COORDINATE",
                "source": "arXiv:1908.08050 Eq.(GravityVacuumAction) and dimension-8 table",
            },
            {
                "basis_id": "B4965_07_no_D_at_p8",
                "quotient_stage": "complete_dimension_count",
                "representative": "no independent D^2 C^3 or derivative quartic at dimension 8",
                "helicity_support": "not_applicable",
                "reality_action": "not_applicable",
                "parity": "not_applicable",
                "independent_parity_even_coordinate": False,
                "status": "DERIVATIVE_OPERATORS_BEGIN_AT_DIMENSION_10",
                "source": "arXiv:1908.08050 Eq.(GravityHilbert); arXiv:2305.10481 pure-gravity table",
            },
        ]
    )
    summary = {
        "raw_chiral_monomial_count": 3,
        "real_parity_even_rank": 2,
        "real_parity_odd_rank_excluded": 1,
        "derivative_p8_rank": 0,
        "O_CC_chiral_expansion": str(O_CC),
        "O_tildetilde_chiral_expansion": str(O_TT),
        "O_Ctilde_chiral_expansion": str(O_CT),
        "checks": checks,
    }
    if not all(checks.values()):
        raise RuntimeError(f"p8 invariant map failed: {checks}")
    return rows, summary


def derive_helicity_projector() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    projector = sp.Matrix([[1, -1], [1, 1]])
    inverse = projector.inv()
    identity = sp.simplify(inverse * projector)
    rows = tagged(
        [
            {
                "channel_id": "H4965_00_all_plus",
                "external_helicity": "++++",
                "reduced_amplitude": "A_pppp/K_pppp=beta_minus",
                "kinematic_factor": "K_pppp=(s^2+t^2+u^2)^2/2*([12][34]/<12><34>)^2",
                "coefficient_beta_C": 1,
                "coefficient_beta_tildeC": -1,
                "projected_coordinate": "beta_minus=beta_C-beta_tildeC",
                "status": "FIRST_INDEPENDENT_P8_PROJECTOR",
                "source": "arXiv:2103.12728 Eqs.(R4 amplitudes,R4definition)",
            },
            {
                "channel_id": "H4965_01_double_minus",
                "external_helicity": "+--+",
                "reduced_amplitude": "A_pmmP/K_pmmP=beta_plus",
                "kinematic_factor": "K_pmmP=(<23>[14])^4",
                "coefficient_beta_C": 1,
                "coefficient_beta_tildeC": 1,
                "projected_coordinate": "beta_plus=beta_C+beta_tildeC",
                "status": "SECOND_INDEPENDENT_P8_PROJECTOR",
                "source": "arXiv:2103.12728 Eqs.(R4 amplitudes,R4definition)",
            },
            {
                "channel_id": "H4965_02_inverse_beta_C",
                "external_helicity": "inverse_map",
                "reduced_amplitude": "beta_C=(beta_minus+beta_plus)/2",
                "kinematic_factor": "reduced amplitudes evaluated away from kinematic zeros",
                "coefficient_beta_C": "1/2 on each reduced channel",
                "coefficient_beta_tildeC": "not_applicable",
                "projected_coordinate": "beta_C",
                "status": "EXACT_INVERSE_PROJECTOR",
                "source": "symbolic inverse of the two source-locked helicity rows",
            },
            {
                "channel_id": "H4965_03_inverse_beta_tildeC",
                "external_helicity": "inverse_map",
                "reduced_amplitude": "beta_tildeC=(beta_plus-beta_minus)/2",
                "kinematic_factor": "reduced amplitudes evaluated away from kinematic zeros",
                "coefficient_beta_C": "-1/2 on beta_minus; +1/2 on beta_plus",
                "coefficient_beta_tildeC": "not_applicable",
                "projected_coordinate": "beta_tildeC",
                "status": "EXACT_INVERSE_PROJECTOR",
                "source": "symbolic inverse of the two source-locked helicity rows",
            },
        ]
    )
    summary = {
        "matrix": [[int(value) for value in row] for row in projector.tolist()],
        "determinant": int(projector.det()),
        "rank": int(projector.rank()),
        "inverse": [[str(value) for value in row] for row in inverse.tolist()],
        "inverse_times_projector": [[str(value) for value in row] for row in identity.tolist()],
    }
    if projector.rank() != 2 or projector.det() == 0 or identity != sp.eye(2):
        raise RuntimeError(f"helicity projector is not invertible: {summary}")
    return rows, summary


def derive_minimal_motion_scalar_source(
    motion_result: dict[str, Any], C3_result: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mu = sp.symbols("mu_psi", positive=True)
    B_minus = 1 / (60480 * sp.pi * mu**4)
    B_plus = 1 / (50400 * sp.pi * mu**4)
    B_C = sp.simplify((B_minus + B_plus) / 2)
    B_tilde = sp.simplify((B_plus - B_minus) / 2)
    A_C3_scalar = 1 / (483840 * sp.pi**2 * mu**2)
    B_minus_from_A = sp.simplify(B_minus / A_C3_scalar**2)
    B_plus_from_A = sp.simplify(B_plus / A_C3_scalar**2)
    B_C_from_A = sp.simplify(B_C / A_C3_scalar**2)
    B_tilde_from_A = sp.simplify(B_tilde / A_C3_scalar**2)
    inherited_c6 = sp.sympify(
        motion_result["minimal_optimized_trace"]["scalar_c6"].replace("pi", "pi")
    )
    c6_match = sp.simplify(A_C3_scalar * mu**2 - inherited_c6) == 0
    selected_negative = C3_result["C3_selection"]["selected_sign_negative_in_source_scheme"]

    rows = tagged(
        [
            {
                "source_id": "S4965_00_normalization_map",
                "quantity": "Bern_to_MTS_action_coordinates",
                "exact_formula": "beta_R3=(3/2)kappa*a_plus; beta_C=kappa^2*b_C; beta_tildeC=kappa^2*b_tildeC",
                "dimensionless_formula": "A_C3=a_plus/(16pi lP^4); B_C=b_C/lP^6; B_tildeC=b_tildeC/lP^6",
                "numeric_prefactor": "not_applicable",
                "sign_or_ratio": "invertible_coordinate_map",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "ACTION_NORMALIZATION_MAP_DERIVED",
                "source": "arXiv:2103.12728 EFT action plus MTS 4922/4963 action normalization",
            },
            {
                "source_id": "S4965_01_scalar_C3",
                "quantity": "A_C3_minimal_scalar",
                "exact_formula": "1/(483840*pi^2*mu_psi^2)",
                "dimensionless_formula": "mu_psi=m_psi*lP",
                "numeric_prefactor": float(1 / (483840 * sp.pi**2)),
                "sign_or_ratio": "positive",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "MINIMAL_SCALAR_C3_THRESHOLD_SOURCE_DERIVED",
                "source": "arXiv:2103.12728 scalar beta_R3 matching",
            },
            {
                "source_id": "S4965_02_scalar_Bminus",
                "quantity": "B_minus_minimal_scalar",
                "exact_formula": "1/(60480*pi*mu_psi^4)",
                "dimensionless_formula": "B_minus=(b_C-b_tildeC)/lP^6",
                "numeric_prefactor": float(1 / (60480 * sp.pi)),
                "sign_or_ratio": "positive",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "ALL_PLUS_P8_SOURCE_DERIVED",
                "source": "arXiv:2103.12728 scalar beta_R4_minus matching",
            },
            {
                "source_id": "S4965_03_scalar_Bplus",
                "quantity": "B_plus_minimal_scalar",
                "exact_formula": "1/(50400*pi*mu_psi^4)",
                "dimensionless_formula": "B_plus=(b_C+b_tildeC)/lP^6",
                "numeric_prefactor": float(1 / (50400 * sp.pi)),
                "sign_or_ratio": "positive; B_plus/B_minus=6/5",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "DOUBLE_MINUS_P8_SOURCE_DERIVED",
                "source": "arXiv:2103.12728 scalar beta_R4_plus matching",
            },
            {
                "source_id": "S4965_04_scalar_BC",
                "quantity": "B_C_minimal_scalar",
                "exact_formula": str(B_C),
                "dimensionless_formula": "B_C=(B_minus+B_plus)/2",
                "numeric_prefactor": float(B_C * mu**4),
                "sign_or_ratio": "positive; real-basis ratio B_C:B_tildeC=11:1",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "REAL_EVEN_P8_SOURCE_DERIVED",
                "source": "inverse helicity projector",
            },
            {
                "source_id": "S4965_05_scalar_Btilde",
                "quantity": "B_tildeC_minimal_scalar",
                "exact_formula": str(B_tilde),
                "dimensionless_formula": "B_tildeC=(B_plus-B_minus)/2",
                "numeric_prefactor": float(B_tilde * mu**4),
                "sign_or_ratio": "positive; real-basis ratio B_C:B_tildeC=11:1",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "REAL_PSEUDOSCALAR_SQUARED_P8_SOURCE_DERIVED",
                "source": "inverse helicity projector",
            },
            {
                "source_id": "S4965_06_c6_crosscheck",
                "quantity": "stripped_C3_prefactor",
                "exact_formula": "mu_psi^2*A_C3_minimal_scalar=1/(483840*pi^2)",
                "dimensionless_formula": motion_result["minimal_optimized_trace"]["scalar_c6"],
                "numeric_prefactor": float(inherited_c6),
                "sign_or_ratio": f"exact_match={c6_match}",
                "valid_for_partial_parent_source": c6_match,
                "valid_for_total_parent_prediction": False,
                "status": "INDEPENDENT_AMPLITUDE_TO_HEAT_KERNEL_NORMALIZATION_MATCH",
                "source": "4935 minimal motion trace and arXiv:2103.12728 scalar matching",
            },
            {
                "source_id": "S4965_07_scalar_only_test",
                "quantity": "direct_identification_of_selected_A_C3_S_with_isolated_scalar_threshold",
                "exact_formula": "A_C3_minimal_scalar>0 while selected local A_C3^S<0 in their displayed source schemes",
                "dimensionless_formula": f"selected=[{C3_result['C3_selection']['selected_A_C3_min']},{C3_result['C3_selection']['selected_A_C3_max']}]",
                "numeric_prefactor": "not_applicable",
                "sign_or_ratio": "direct_identification_fails; physical-origin_no_go_not_implied",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "DIRECT_SCALAR_THRESHOLD_IDENTIFICATION_REJECTED_SCHEME_INVARIANT_ORIGIN_OPEN",
                "source": "4963 selected source-scheme C3 envelope and scalar-loop matching",
            },
            {
                "source_id": "S4965_08_scalar_internal_consistency_curve",
                "quantity": "minimal_scalar_p8_vector_as_function_of_its_own_C3_source",
                "exact_formula": "B_minus=3870720*pi^3*A_psi^2; B_plus=4644864*pi^3*A_psi^2",
                "dimensionless_formula": "B_C=4257792*pi^3*A_psi^2; B_tildeC=387072*pi^3*A_psi^2",
                "numeric_prefactor": "mass_gap_eliminated_exactly",
                "sign_or_ratio": "one-dimensional positive curve; B_plus/B_minus=6/5",
                "valid_for_partial_parent_source": True,
                "valid_for_total_parent_prediction": False,
                "status": "MINIMAL_SCALAR_C3_P8_SOURCE_RELATION_DERIVED",
                "source": "common scalar mass eliminated between the source-locked C3 and p8 threshold coefficients",
            },
        ]
    )
    checks = {
        "Bplus_over_Bminus": sp.simplify(B_plus / B_minus) == sp.Rational(6, 5),
        "BC_exact": sp.simplify(B_C - 11 / (604800 * sp.pi * mu**4)) == 0,
        "Btilde_exact": sp.simplify(B_tilde - 1 / (604800 * sp.pi * mu**4)) == 0,
        "real_basis_ratio": sp.simplify(B_C / B_tilde) == 11,
        "c6_prefactor_match": c6_match,
        "Bminus_from_A": B_minus_from_A == 3870720 * sp.pi**3,
        "Bplus_from_A": B_plus_from_A == 4644864 * sp.pi**3,
        "BC_from_A": B_C_from_A == 4257792 * sp.pi**3,
        "Btilde_from_A": B_tilde_from_A == 387072 * sp.pi**3,
        "selected_total_negative": selected_negative,
        "minimal_scalar_positive": sp.ask(sp.Q.positive(A_C3_scalar)) is True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"minimal scalar source derivation failed: {checks}")
    return rows, {
        "B_minus": str(B_minus),
        "B_plus": str(B_plus),
        "B_C": str(B_C),
        "B_tildeC": str(B_tilde),
        "A_C3_scalar": str(A_C3_scalar),
        "B_minus_from_A_C3_scalar": str(B_minus_from_A),
        "B_plus_from_A_C3_scalar": str(B_plus_from_A),
        "B_C_from_A_C3_scalar": str(B_C_from_A),
        "B_tildeC_from_A_C3_scalar": str(B_tilde_from_A),
        "minimal_scalar_source_rank_in_p8_space": 1,
        "minimal_scalar_direct_identification_with_selected_A_C3_S": False,
        "minimal_scalar_only_physical_origin_rejected": False,
        "checks": checks,
    }


def derive_power_count_and_flow_gate(
    trajectory: dict[str, Any], p4_result: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    entries = [
        ("PC4965_00_tree_p8", 0, {8: 1}, "independent_p8_boundary_or_UV_matching"),
        ("PC4965_01_tree_p6_p4", 0, {6: 1, 4: 1}, "p4_redefinition_relocation"),
        ("PC4965_02_tree_3p4", 0, {4: 3}, "p4_redefinition_relocation"),
        ("PC4965_03_one_loop_p6", 1, {6: 1}, "C3_or_O4_insertion"),
        ("PC4965_04_one_loop_2p4", 1, {4: 2}, "p4_redefinition_relocation"),
        ("PC4965_05_two_loop_p4", 2, {4: 1}, "p4_redefinition_relocation"),
        ("PC4965_06_three_loop_EH", 3, {}, "pure_EH_quantum_source"),
    ]
    p4_rank = p4_result["four_derivative_quotient"][
        "independent_neutral_vacuum_p4_parameters"
    ]
    rows: list[dict[str, Any]] = []
    all_power_counts_pass = True
    for source_id, loops, vertices, source_role in entries:
        derivative_order = 2 + 2 * loops + sum(
            multiplicity * (dimension - 2)
            for dimension, multiplicity in vertices.items()
        )
        independent_in_p4_quotient = 4 not in vertices
        passed = derivative_order == 8
        all_power_counts_pass &= passed
        rows.append(
            {
                "source_id": source_id,
                "loop_order": loops,
                "higher_derivative_vertices": ";".join(
                    f"p{dimension}x{multiplicity}"
                    for dimension, multiplicity in sorted(vertices.items())
                )
                or "EH_only",
                "power_count_formula": "D=2+2L+sum V_i(d_i-2)",
                "computed_D": derivative_order,
                "p8_power_count_pass": passed,
                "independent_in_selected_vacuum_p4_quotient": independent_in_p4_quotient,
                "source_role": source_role,
                "current_4935_projection_available": False,
                "status": (
                    "ACTIVE_INDEPENDENT_P8_SOURCE_CLASS"
                    if independent_in_p4_quotient
                    else "P4_DEPENDENT_CLASS_RELOCATED_BY_EQUIVALENCE_QUOTIENT"
                ),
            }
        )
    rows.append(
        {
            "source_id": "PC4965_07_massive_motion_threshold",
            "loop_order": 1,
            "higher_derivative_vertices": "minimal_p2_motion_Hessian_large_mass_expansion",
            "power_count_formula": "one massive determinant generates local p8/m_psi^4 matching",
            "computed_D": 8,
            "p8_power_count_pass": True,
            "independent_in_selected_vacuum_p4_quotient": True,
            "source_role": "explicit_rank1_p8_source_vector_derived_in_4965",
            "current_4935_projection_available": "partial_analytic_threshold_match_only",
            "status": "MOTION_SCALAR_MINIMAL_SOURCE_VECTOR_DERIVED",
        }
    )

    coordinates = trajectory["flow_contract"]["coordinates"]
    p8_coordinates = {"B_minus", "B_plus", "b_C", "b_tildeC"}
    current_p8_coordinates = sorted(set(coordinates) & p8_coordinates)
    summary = {
        "power_count_identity_passed_for_all_partitions": all_power_counts_pass,
        "p4_quotient_rank": p4_rank,
        "current_4935_coordinates": coordinates,
        "current_4935_p8_coordinates": current_p8_coordinates,
        "current_4935_p8_projection_rank": 0 if not current_p8_coordinates else None,
        "target_p8_rank": 2,
        "minimal_motion_scalar_source_rank": 1,
        "total_parent_p8_values_identified": False,
        "required_extension": "append B_minus,B_plus and project d_t Gamma_TTTT on ++++ and +--+ channels; include O4, graviton, photon and boundary sources",
    }
    if not all_power_counts_pass or p4_rank != 0 or current_p8_coordinates:
        raise RuntimeError(f"p8 parent source audit changed: {summary}")
    return tagged(rows), summary


def derive_dispersive_cone(
    C3_result: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    selected_min = float(C3_result["C3_selection"]["selected_A_C3_min"])
    selected_max = float(C3_result["C3_selection"]["selected_A_C3_max"])
    factors = [576 * math.pi**2 * selected_min**2, 576 * math.pi**2 * selected_max**2]
    factor_min = min(factors)
    factor_max = max(factors)
    rows = tagged(
        [
            {
                "cone_id": "D4965_00_primary_bound",
                "statement": "|beta_R3|^2 <= beta_R4_plus/M_gap^2",
                "MTS_coordinate_form": "B_plus >= 576*pi^2*A_C3_phys^2*mu_gap^2",
                "coefficient_min": "not_applicable",
                "coefficient_max": "not_applicable",
                "assumptions": "infrared-finite massive contribution; perturbative unitarity; crossing; dispersive/Regge conditions of arXiv:2103.12728",
                "valid_for_physical_bound": True,
                "valid_for_current_MTS_numeric_bound": False,
                "status": "CONDITIONAL_PHYSICAL_DISPERSIVE_CONE_DERIVED",
            },
            {
                "cone_id": "D4965_01_source_scheme_transfer",
                "statement": "insert the 4963 A_C3^S interval only as an algebraic illustration",
                "MTS_coordinate_form": "B_plus >= coefficient*mu_gap^2",
                "coefficient_min": factor_min,
                "coefficient_max": factor_max,
                "assumptions": "would additionally require A_C3^S to be replaced by a scheme-independent local-plus-nonlocal three-graviton amplitude coefficient",
                "valid_for_physical_bound": False,
                "valid_for_current_MTS_numeric_bound": False,
                "status": "SOURCE_SCHEME_NUMBER_QUARANTINED",
            },
            {
                "cone_id": "D4965_02_threshold_guardrail",
                "statement": "for one particle of mass m_psi the dispersive pair threshold is M_gap=2m_psi",
                "MTS_coordinate_form": "mu_gap=2*mu_psi",
                "coefficient_min": "not_applicable",
                "coefficient_max": "not_applicable",
                "assumptions": "single stable massive threshold",
                "valid_for_physical_bound": True,
                "valid_for_current_MTS_numeric_bound": False,
                "status": "PARTICLE_MASS_AND_DISPERSIVE_GAP_SEPARATED",
            },
            {
                "cone_id": "D4965_03_four_dimensional_guardrail",
                "statement": "do not promote the perturbative infrared-finite bound to an unrestricted nonperturbative four-dimensional quantum-gravity theorem",
                "MTS_coordinate_form": "no_numeric_total_B_plus_claim",
                "coefficient_min": "not_applicable",
                "coefficient_max": "not_applicable",
                "assumptions": "the source explicitly notes four-dimensional IR and nonperturbative limitations",
                "valid_for_physical_bound": True,
                "valid_for_current_MTS_numeric_bound": False,
                "status": "SCOPE_GUARDRAIL_RETAINED",
            },
        ]
    )
    return rows, {
        "MTS_cone": "B_plus >= 576*pi^2*A_C3_phys^2*mu_gap^2",
        "source_scheme_factor_min": factor_min,
        "source_scheme_factor_max": factor_max,
        "current_numeric_cone_claim": False,
    }


def derive_compact_domain(
    p8_tail_rows: list[dict[str, str]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    object_rows = [row for row in p8_tail_rows if row["row_type"] == "compact_object_gate"]
    rows: list[dict[str, Any]] = []
    for row in object_rows:
        budget = float(row["C8_max_if_R_equals_1"])
        rows.append(
            {
                "object_id": row["object_id"],
                "source_class": row["source_class"],
                "chi_lP2_curvature": row["chi_lP2_curvature"],
                "epsilon_gate": row["epsilon_gate"],
                "exact_two_coordinate_gate": "rho_minus*abs(B_minus)+rho_plus*abs(B_plus)<=C8_max",
                "unit_response_l1_budget": budget,
                "single_coordinate_intercept_if_other_zero": budget,
                "rho_minus_status": "STATIC_RESPONSE_PROJECTOR_NOT_YET_CALCULATED",
                "rho_plus_status": "STATIC_RESPONSE_PROJECTOR_NOT_YET_CALCULATED",
                "minimal_scalar_direction": "B_plus=(6/5)B_minus",
                "valid_for_conditional_coefficient_domain": True,
                "valid_for_compact_p8_claim": False,
                "status": "EXACT_2D_RESPONSE_GATE_UNIT_WEIGHT_BENCHMARK_ONLY",
                "source": row["source_path"],
            }
        )
    tightest = min(rows, key=lambda item: item["unit_response_l1_budget"])
    return tagged(rows), {
        "object_count": len(rows),
        "tightest_object": tightest["object_id"],
        "tightest_unit_response_l1_budget": tightest["unit_response_l1_budget"],
        "static_response_projector_calculated": False,
        "minimal_scalar_direction": "B_plus/B_minus=6/5",
    }


def decision_rows(
    basis: dict[str, Any],
    projector: dict[str, Any],
    motion: dict[str, Any],
    flow: dict[str, Any],
    compact: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision_id": "DEC4965_00_p8_basis",
                "question": "What is the complete selected Ricci-flat parity-even local p8 pure-gravity rank?",
                "answer": basis["real_parity_even_rank"],
                "evidence": "two independent primary-source basis constructions plus exact chiral-real map",
                "status": "RANK_TWO_PROVED",
            },
            {
                "decision_id": "DEC4965_01_helicity_projector",
                "question": "Can the two p8 coordinates be separated by on-shell data?",
                "answer": f"yes; rank={projector['rank']}; determinant={projector['determinant']}",
                "evidence": "++++ gives beta_minus and +--+ gives beta_plus",
                "status": "FULL_RANK_PROJECTOR_DERIVED",
            },
            {
                "decision_id": "DEC4965_02_motion_source",
                "question": "Does the current motion sector supply any calculated p8 source?",
                "answer": "yes; one conditional minimal massive-scalar source vector",
                "evidence": "B_minus=1/(60480 pi mu_psi^4); B_plus=1/(50400 pi mu_psi^4)",
                "status": "PARTIAL_PARENT_SOURCE_RANK_ONE_DERIVED",
            },
            {
                "decision_id": "DEC4965_03_scalar_only",
                "question": "Can the selected local A_C3^S be directly identified with the isolated minimal-scalar threshold term?",
                "answer": motion["minimal_scalar_direct_identification_with_selected_A_C3_S"],
                "evidence": "the displayed source-scheme signs differ; because A_C3^S is not scheme invariant this rejects direct identification, not every scalar-origin completion",
                "status": "DIRECT_IDENTIFICATION_REJECTED_PHYSICAL_ORIGIN_OPEN",
            },
            {
                "decision_id": "DEC4965_04_total_parent_flow",
                "question": "Are both total p8 Wilson coordinates fixed by the present 4935 trajectory?",
                "answer": flow["total_parent_p8_values_identified"],
                "evidence": f"target rank={flow['target_p8_rank']}; current p8 rank={flow['current_4935_p8_projection_rank']}; scalar partial rank={flow['minimal_motion_scalar_source_rank']}",
                "status": "TOTAL_P8_FLOW_NOT_YET_IDENTIFIED",
            },
            {
                "decision_id": "DEC4965_05_compact_GR",
                "question": "Does 4965 establish exact all-operator compact GR?",
                "answer": False,
                "evidence": f"static p8 response weights remain open across {compact['object_count']} retained compact rows",
                "status": "ALL_OPERATOR_COMPACT_GR_FALSE",
            },
            {
                "decision_id": "DEC4965_06_next",
                "question": "What is the next noncircular derivation target?",
                "answer": "derive the O4-modified p8 four-graviton source and the two static response weights in the same helicity basis",
                "evidence": "the minimal scalar source is now known; O4 plus boundary/gravity terms and compact transfer are the first missing total-source pieces",
                "status": "O4_P8_SOURCE_AND_STATIC_RESPONSE_NEXT",
            },
        ]
    )


def write_provenance(source_state: dict[str, Any]) -> None:
    lines = [
        "# Checkpoint 4965 source provenance",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        f"Marker: `{MARKER}`.",
        "",
        "This packet proves the complete selected four-dimensional Ricci-flat",
        "parity-even local p8 basis, constructs its rank-two helicity projector",
        "and derives the rank-one minimally coupled massive motion-scalar source",
        "vector. It does not determine the total parent p8 boundary or claim",
        "all-operator compact GR.",
        "",
        "## Primary records",
        "",
        "- Ruhdorfer, Serra and Weiler, *Effective Field Theory of Gravity to All Orders*, arXiv:1908.08050. Basis evidence: source lines 583-630 and 1115-1139.",
        "- Li, Ren, Xiao, Yu and Zheng, *On-shell Operator Construction in the Effective Field Theory of Gravity*, arXiv:2305.10481, JHEP 10 (2023) 019. Basis evidence: source lines 754-779.",
        "- Bern, Kosmopoulos and Zhiboedov, *Gravitational Effective Field Theory Islands, Low-Spin Dominance, and the Four-Graviton Amplitude*, arXiv:2103.12728. Action/amplitudes: lines 1726-1764 and 1884-1900; scalar matching: 2033-2058; conditional dispersive bound: 3394-3448.",
        "",
        "## Locked files",
        "",
        "| id | local path | SHA-256 |",
        "|---|---|---|",
    ]
    for name, path in SOURCE_PATHS.items():
        lines.append(f"| `{name}` | `{relative(path)}` | `{source_state['hashes'][name]}` |")
    lines.extend(
        [
            "",
            "## Scope firewall",
            "",
            "- The primary basis rank and helicity projector are exact within the declared four-dimensional on-shell parity-even local pure-gravity sector.",
            "- The motion source vector assumes the renormalized 4935 Hessian is a canonically normalized minimally coupled massive scalar at threshold matching.",
            "- The O4 portal, pure-gravity contribution, photons, nonlocal pieces and an independent p8 boundary can shift the total two-vector.",
            "- The 4963 finite C3 coordinate is scheme dependent by itself, so its insertion into the dispersive cone is quarantined from numeric claim status.",
            "- No GitHub action is performed.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_state = source_checks()
    motion_result = json.loads(SOURCE_PATHS["motion_4935"].read_text(encoding="utf-8"))
    trajectory = json.loads(SOURCE_PATHS["trajectory_4935"].read_text(encoding="utf-8"))
    C3_result = json.loads(SOURCE_PATHS["C3_4963"].read_text(encoding="utf-8"))
    p4_result = json.loads(SOURCE_PATHS["p4_quotient_4964"].read_text(encoding="utf-8"))
    p8_tail_rows = read_csv(SOURCE_PATHS["p8_tail_4964"])

    basis_rows, basis_summary = derive_p8_basis()
    projector_rows, projector_summary = derive_helicity_projector()
    motion_rows, motion_summary = derive_minimal_motion_scalar_source(
        motion_result, C3_result
    )
    power_rows, power_summary = derive_power_count_and_flow_gate(
        trajectory, p4_result
    )
    dispersive_rows, dispersive_summary = derive_dispersive_cone(C3_result)
    compact_rows, compact_summary = derive_compact_domain(p8_tail_rows)
    decisions = decision_rows(
        basis_summary,
        projector_summary,
        motion_summary,
        power_summary,
        compact_summary,
    )

    write_csv(BASIS_CSV, basis_rows)
    write_csv(PROJECTOR_CSV, projector_rows)
    write_csv(MOTION_SOURCE_CSV, motion_rows)
    write_csv(POWER_COUNT_CSV, power_rows)
    write_csv(DISPERSIVE_CSV, dispersive_rows)
    write_csv(COMPACT_CSV, compact_rows)
    write_csv(DECISION_CSV, decisions)
    write_provenance(source_state)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_state": source_state,
        "p8_basis": basis_summary,
        "helicity_projector": projector_summary,
        "minimal_motion_scalar_source": motion_summary,
        "parent_power_count_and_flow_gate": power_summary,
        "C3_dispersive_cone": dispersive_summary,
        "compact_two_coordinate_domain": compact_summary,
        "decisions": {row["decision_id"]: row["answer"] for row in decisions},
        "checks": {
            "all_sources_locked": not source_state["missing"] and not source_state["bad_hashes"],
            "all_source_clauses_found": all(source_state["clauses"].values()),
            "p8_parity_even_rank_two": basis_summary["real_parity_even_rank"] == 2,
            "no_derivative_p8_coordinate": basis_summary["derivative_p8_rank"] == 0,
            "helicity_projector_rank_two": projector_summary["rank"] == 2,
            "helicity_projector_determinant_two": projector_summary["determinant"] == 2,
            "minimal_scalar_source_rank_one": motion_summary["minimal_scalar_source_rank_in_p8_space"] == 1,
            "minimal_scalar_C3_normalization_crosscheck": motion_summary["checks"]["c6_prefactor_match"],
            "minimal_scalar_direct_C3_identification_rejected": not motion_summary["minimal_scalar_direct_identification_with_selected_A_C3_S"],
            "minimal_scalar_physical_origin_not_overclaimed": not motion_summary["minimal_scalar_only_physical_origin_rejected"],
            "p4_vacuum_quotient_rank_zero": power_summary["p4_quotient_rank"] == 0,
            "current_4935_p8_projection_rank_zero": power_summary["current_4935_p8_projection_rank"] == 0,
            "total_parent_p8_not_claimed": not power_summary["total_parent_p8_values_identified"],
            "dispersive_numeric_MTS_cone_not_claimed": not dispersive_summary["current_numeric_cone_claim"],
            "eleven_compact_rows_retained": compact_summary["object_count"] == 11,
            "static_response_projector_not_claimed": not compact_summary["static_response_projector_calculated"],
            "all_operator_compact_GR_false": decisions[5]["answer"] is False,
            "full_MTS_false": True,
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(result["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
