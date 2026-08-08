from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1805"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1805_0_1804_doc",
        "source_key": "1804_doc",
        "source_path": ROOT / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md",
        "needles": ["NEXT1804_0_primary", "CPR1804_5_qbar_constants_abs"],
        "role": "1804 handoff selecting no-extra-F2/no-mass-vertex signature or bound matrix.",
    },
    {
        "source_id": "SRC1805_1_1804_validation",
        "source_key": "1804_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1804_VALIDATION.csv",
        "needles": ["VAL1804_OVERALL", "PASS"],
        "role": "confirms the current constant-superselection checkpoint passed.",
    },
    {
        "source_id": "SRC1805_2_1804_coefficients",
        "source_key": "1804_coefficients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_COEFFICIENT_PROVENANCE_ROWS.csv",
        "needles": ["CPR1804_0_b_alpha", "CPR1804_5_qbar_constants_abs"],
        "role": "current branch alpha/mass/clock coefficient provenance rows.",
    },
    {
        "source_id": "SRC1805_3_1804_alpha",
        "source_key": "1804_alpha",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_ALPHA_GAUGE_AUDIT.csv",
        "needles": ["AGA1804_1_unique_F2", "AGA1804_4_verdict"],
        "role": "current branch alpha gauge audit retaining b_alpha.",
    },
    {
        "source_id": "SRC1805_4_1804_mass",
        "source_key": "1804_mass",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_MASS_RATIO_AUDIT.csv",
        "needles": ["MRA1804_1_mass_ratios", "MRA1804_4_verdict"],
        "role": "current branch mass-ratio audit retaining b_mA/b_mu/b_nuc.",
    },
    {
        "source_id": "SRC1805_5_1804_clock",
        "source_key": "1804_clock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_CLOCK_PROJECTION_ROWS.csv",
        "needles": ["CLK1804_0_CAS646_0_AlHg", "CLK1804_1_CAS646_1_YbE3E2"],
        "role": "current branch clock alpha sensitivity projection rows.",
    },
    {
        "source_id": "SRC1805_6_1804_bounds",
        "source_key": "1804_bounds",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1804_BOUND_LINKS.csv",
        "needles": ["BL1804_2_WEP", "BL1804_3_R10"],
        "role": "current branch bound-link ledger for WEP/R10/clock anchors.",
    },
    {
        "source_id": "SRC1805_7_1048_doc",
        "source_key": "1048_doc",
        "source_path": ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
        "needles": ["PVS1048_5_verdict", "DEC1048_3_best_next"],
        "role": "older no-extra-F2/no-mass-vertex signature attempt and bound matrix.",
    },
    {
        "source_id": "SRC1805_8_1048_parent_signature",
        "source_key": "1048_parent_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv",
        "needles": ["PVS1048_1_no_extra_F2", "PVS1048_5_verdict"],
        "role": "older parent vertex signature audit.",
    },
    {
        "source_id": "SRC1805_9_1048_f2",
        "source_key": "1048_f2",
        "source_path": RESIDUALS / "P8_Y5_R10_1048_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
        "needles": ["F2T1048_1_no_scalar_counterterm", "F2T1048_3_verdict"],
        "role": "older no-extra-F2 theorem attempt.",
    },
    {
        "source_id": "SRC1805_10_1048_mass",
        "source_key": "1048_mass",
        "source_path": RESIDUALS / "P8_Y5_R10_1048_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv",
        "needles": ["MVT1048_1_no_yukawa_or_mass_X", "MVT1048_3_verdict"],
        "role": "older no-mass-vertex theorem attempt.",
    },
    {
        "source_id": "SRC1805_11_1048_vertices",
        "source_key": "1048_vertices",
        "source_path": RESIDUALS / "P8_Y5_R10_1048_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv",
        "needles": ["VT1048_1_scalar_F2", "VT1048_6_clock_readout_X"],
        "role": "older allowed/forbidden vertex catalog.",
    },
    {
        "source_id": "SRC1805_12_1048_matrix",
        "source_key": "1048_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
        "needles": ["BM1048_0_alpha_clock", "BM1048_4_PPN_source"],
        "role": "older alpha/mass/clock bound matrix.",
    },
    {
        "source_id": "SRC1805_13_1049_doc",
        "source_key": "1049_doc",
        "source_path": ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
        "needles": ["OCR1049_5_verdict", "SBT1049_4_product_functor"],
        "role": "older operator-classification/symmetry-ban target after 1048.",
    },
    {
        "source_id": "SRC1805_14_1049_operator",
        "source_key": "1049_operator",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
        "needles": ["OCR1049_2_product_sequestration", "OCR1049_5_verdict"],
        "role": "operator-classification rule attempt used to choose the next current-branch target.",
    },
    {
        "source_id": "SRC1805_15_1049_symmetry",
        "source_key": "1049_symmetry",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
        "needles": ["SBT1049_0_diffeomorphism_covariance", "SBT1049_4_product_functor"],
        "role": "symmetry tests showing covariance/gauge invariance do not forbid the dangerous vertices.",
    },
    {
        "source_id": "SRC1805_16_646_clock_sensitivity",
        "source_key": "646_clock_sensitivity",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock alpha sensitivity values.",
    },
    {
        "source_id": "SRC1805_17_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R3_gamma"],
        "role": "local WEP, clock, PPN and Gdot bound anchors.",
    },
    {
        "source_id": "SRC1805_18_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate bound curve, not claim grade.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_SOURCE_REGISTER.csv",
    "parent_vertex_signature_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_PARENT_VERTEX_SIGNATURE_AUDIT.csv",
    "no_extra_f2_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
    "no_mass_vertex_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv",
    "allowed_forbidden_vertex_table": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv",
    "alpha_mass_clock_bound_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
    "arena_projection_requirements": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ARENA_PROJECTION_REQUIREMENTS.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1805_ALPHA_MASS_CLOCK_MATRIX_TEMPLATE_NONCLAIM.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1805_VALIDATION.csv",
}

DOC_PATH = ROOT / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": source["role"],
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(str(by_key[key]) for key in keys)


def parent_vertex_signature_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_0_declared_parent_domain",
            "signature_clause": "parent action has a declared field domain and allowed local-operator list before fitting local tests",
            "minimal_form": "S_parent[Phi,Psi]=S_grav[q(Phi)] + S_gauge[A^Q T_Q,q(Phi)] + S_matter[Psi,e_obs(q),omega(e_obs),theta_rep] + S_hidden[Xhat,...]",
            "would_buy": "prevents changing the theory per arena by inserting hidden alpha/mass/clock vertices after data pressure appears",
            "current_status": "CONTRACT_SHAPE_EXACT_NOT_PARENT_SIGNED",
            "blocks_if_missing": "post-hoc coefficient functions can be added to visible EM/matter/readout sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_1_no_extra_F2",
            "signature_clause": "no independent gauge kinetic operator or scalar gauge-kinetic function",
            "minimal_form": "Allowed: -(C_P/4) int mu_obs <F_Q T_Q,F_Q T_Q>_P; Forbidden: -(1/4) int mu_obs f_X(Xhat) F_Q^2 or lambda_A F_Q^2",
            "would_buy": "b_alpha=0 from fixed parent gauge norm instead of phenomenological alpha fitting",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "blocks_if_missing": "alpha_EM remains a retained b_alpha coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_2_no_mass_vertex",
            "signature_clause": "no explicit Xhat-dependent masses, Yukawas, QCD scales, nuclear binding, or material-response functions",
            "minimal_form": "Allowed: theta_rep fixed or theta_bar(q); Forbidden: m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat), beta_A(Xhat)",
            "would_buy": "b_mu, b_mA and b_nuc can be theorem-zero rather than fitted or bounded",
            "current_status": "NOT_DERIVED",
            "blocks_if_missing": "mass ratios, composition sensitivities and nuclear binding remain physical channels",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_3_no_clock_readout_vertex",
            "signature_clause": "clock and spectral readout descend from quotient-owned coframe/Hodge/matter constants",
            "minimal_form": "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) with no nu_i(Xhat), shadow coframe, or detector-frame normalization slot",
            "would_buy": "b_clock_i is inherited from zero upstream coefficients and no separate local clock residual survives",
            "current_status": "UNSIGNED",
            "blocks_if_missing": "clocks remain a separate local readout residual even if WEP is quiet",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_4_no_material_marker_vertex",
            "signature_clause": "source/test material labels are discrete representation data or quotient-owned densities, not smooth Xhat markers",
            "minimal_form": "material_A in Rep(P), rho_A=rho_bar_A(q,Psi_A); Forbidden: s_A(Xhat), preparation_A(Xhat), kappa_A(Xhat)",
            "would_buy": "prevents composition-dependent leakage from sneaking through source definitions",
            "current_status": "UNSIGNED",
            "blocks_if_missing": "WEP/R10 source-test channels stay retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_5_no_radiative_readout_reentry",
            "signature_clause": "tree-level bans survive effective/radiative/readout reduction",
            "minimal_form": "renormalized alpha_eff, mass ratios, binding functions and clock readout must factor through q or fixed representation data under the same parent rule",
            "would_buy": "prevents a clean bare action from reopening b_alpha/b_clock_i through effective observables",
            "current_status": "UNSIGNED",
            "blocks_if_missing": "loop/readout normalizations can reintroduce the very constants being zeroed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVS1805_6_verdict",
            "signature_clause": "parent action forbids all alpha/mass/clock hidden vertices",
            "minimal_form": "PVS1805_0 through PVS1805_5 parent-signed with no EFT/post-readout re-entry",
            "would_buy": "qbar_constants_abs=0 and the local constant sector closes structurally",
            "current_status": "FAIL_CURRENT_CLAIM_BOUND_MATRIX_REQUIRED",
            "blocks_if_missing": "build alpha/mass/clock projection matrix; no local-GR/R10/WEP/clock claim",
            "valid_for_claim": False,
        },
    ]


def no_extra_f2_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "F2T1805_0_unique_norm",
            "claim_piece": "unique Maxwell kinetic normalization",
            "mathematical_form": "S_Q=-(C_P/4) int mu_obs <F_Q T_Q,F_Q T_Q>_P and Lie_v(C_P<T_Q,T_Q>_P)=0",
            "proof_step": "If the charge generator, inner product and curvature norm are parent-owned representation data, the gauge kinetic coefficient has no vertical derivative.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "MISSING_PARENT_SIGNED_TQ_OWNER_AND_FIXED_INNER_PRODUCT",
            "if_missing": "b_alpha retains a normalization term",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "F2T1805_1_no_scalar_counterterm",
            "claim_piece": "forbid f_X(Xhat) F_Q^2 and lambda_A F_Q^2",
            "mathematical_form": "delta S_forbidden=-(1/4) int mu_obs f_X(Xhat)F_Q^2; require f_X constant, quotient-descended, or absent",
            "proof_step": "A local scalar gauge-kinetic function is covariant, gauge invariant and dimensionless; it is not eliminated by unit choice.",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_NOT_FORBIDDEN",
            "missing_for_claim": "MISSING_OPERATOR_CLASSIFICATION_OR_SYMMETRY_EXCLUDING_FX_F2",
            "if_missing": "b_alpha = Lie_v ln(g_EM^-2) can be finite",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "F2T1805_2_no_current_rescaling",
            "claim_piece": "charge current and source normalization owner",
            "mathematical_form": "S_int=sum_A n_A int A_Q J_A with n_A representation data and no beta_source_alpha(Xhat)",
            "proof_step": "Even fixed alpha does not close the local source branch unless current/source normalization is owned by the same parent charge generator.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "MISSING_CURRENT_OWNER;MISSING_SOURCE_CHARGE_NORMALIZATION",
            "if_missing": "WEP/R10 source-test strength can float independently",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "F2T1805_3_no_radiative_reentry",
            "claim_piece": "no EFT/readout re-entry of alpha",
            "mathematical_form": "alpha_eff(q,Xhat) must factor through q or be fixed by the same parent owner under renormalization/readout",
            "proof_step": "A tree-level ban cannot be credited if the effective clock/spectral readout regenerates Xhat-dependent alpha.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "MISSING_RENORMALIZATION_AND_READOUT_CLOSURE",
            "if_missing": "clock and EM spectra rows reopen b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "F2T1805_4_verdict",
            "claim_piece": "no-extra-F2 theorem promotion",
            "mathematical_form": "F2T1805_0 + F2T1805_1 + F2T1805_2 + F2T1805_3 => b_alpha=0",
            "proof_step": "The conditional theorem is clean, but the current branch still permits the scalar/counterterm F2 route.",
            "current_status": "FAIL_CURRENT_CLAIM_RETAIN_B_ALPHA",
            "missing_for_claim": "MISSING_NO_FX_F2_THEOREM_OR_NUMERIC_SOURCE_BACKED_B_ALPHA_BOUND",
            "if_missing": "alpha/mass/clock bound matrix remains required",
            "valid_for_claim": False,
        },
    ]


def no_mass_vertex_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "MVT1805_0_fixed_rep_spectrum",
            "claim_piece": "fixed matter representation spectrum",
            "mathematical_form": "theta_mass(Phi)=theta_rep or theta_bar(q(Phi)); Dq[v_X]=0 => Lie_v ln(m_A/m_B)=0",
            "proof_step": "Mass-ratio silence follows if the entire dimensionless matter spectrum is representation/quotient data.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "MISSING_PARENT_DERIVATION_OF_ELECTRON_PROTON_NUCLEAR_MASS_RATIO_DATA",
            "if_missing": "b_mu and b_mA retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "MVT1805_1_no_yukawa_or_mass_X",
            "claim_piece": "forbid Xhat-dependent masses and Yukawas",
            "mathematical_form": "Forbidden: m_A(Xhat) psi_bar_A psi_A, y_A(Xhat) psi_A H psi_B, Lambda_QCD(Xhat)",
            "proof_step": "These vertices are local and covariant; without a parent symmetry/operator rule they are legal finite couplings.",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_ALLOWED_OPERATOR_LIST_OR_SYMMETRY_EXCLUDING_MASS_VERTICES",
            "if_missing": "composition-dependent WEP/R10 and clock mass channels stay live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "MVT1805_2_binding_response",
            "claim_piece": "forbid hidden binding/nuclear response functions",
            "mathematical_form": "B_A(Phi)=Bbar_A(q(Phi),theta_rep) and no B_A(Xhat), beta_A(Xhat), or material response marker",
            "proof_step": "Even fixed point-particle masses are not enough because observable bodies carry EM/nuclear binding fractions.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "MISSING_COMPOSITION_SENSITIVITY_MATRIX_OR_THEOREM_ZERO_BINDING_RESPONSE",
            "if_missing": "b_mA, b_nuc and beta_A rows required for WEP/R10",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "MVT1805_3_no_clock_readout_X",
            "claim_piece": "forbid direct clock-readout Xhat vertex",
            "mathematical_form": "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) and no independent clock frame/readout coefficient c_i(Xhat)",
            "proof_step": "A clock theorem must cover the actual measured dimensionless transition ratio, not just the metric coframe.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "MISSING_CLOCK_READOUT_DESCENT;MISSING_TAU_CLOCK_LOCAL_DXHAT_MAP",
            "if_missing": "b_clock_i remains a retained residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "MVT1805_4_verdict",
            "claim_piece": "no-mass-vertex theorem promotion",
            "mathematical_form": "MVT1805_0 + MVT1805_1 + MVT1805_2 + MVT1805_3 => b_mu=b_mA=b_nuc=b_clock_i=0",
            "proof_step": "The conditional proof is clear, but the current corpus does not derive the matter spectrum or forbid all Xhat mass/readout vertices.",
            "current_status": "FAIL_CURRENT_CLAIM_RETAIN_MASS_CLOCK_MATRIX",
            "missing_for_claim": "MISSING_PARENT_MATTER_SPECTRUM_THEOREM_OR_NUMERIC_SOURCE_BACKED_MASS_COMPOSITION_CLOCK_COEFFICIENTS",
            "if_missing": "alpha/mass/clock bound matrix remains required",
            "valid_for_claim": False,
        },
    ]


def allowed_forbidden_vertex_table_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_0_parent_curvature_F2",
            "sector": "EM",
            "operator_or_slot": "<F_Q T_Q,F_Q T_Q>_P",
            "classification": "allowed_if_parent_owned",
            "coefficient": "C_P<T_Q,T_Q>_P",
            "claim_effect": "can support b_alpha=0 only if no extra F2/current/readout re-entry",
            "current_status": "conditional",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_1_scalar_F2",
            "sector": "EM",
            "operator_or_slot": "f_X(Xhat)F_Q^2 or lambda_A F_Q^2",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_alpha",
            "claim_effect": "finite alpha drift and Coulomb/source pressure",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_2_current_rescaling",
            "sector": "EM/source",
            "operator_or_slot": "beta_source_alpha(Xhat) A_Q J_A or current/source normalization marker",
            "classification": "forbidden_required_or_bounded",
            "coefficient": "beta_source_alpha",
            "claim_effect": "WEP/R10 source charge can float even if alpha clock row is small",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_3_mass_X",
            "sector": "matter",
            "operator_or_slot": "m_A(Xhat) psi_bar_A psi_A",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_mA",
            "claim_effect": "composition, clocks and source mass drift",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_4_yukawa_X",
            "sector": "matter",
            "operator_or_slot": "y_A(Xhat) psi_A H psi_B",
            "classification": "forbidden_required_but_currently_legal",
            "coefficient": "b_mu;b_mA",
            "claim_effect": "dimensionless mass-ratio drift",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_5_binding_X",
            "sector": "composite_matter",
            "operator_or_slot": "B_A(Xhat), Lambda_QCD(Xhat), nuclear/EM binding response",
            "classification": "forbidden_required_or_bounded",
            "coefficient": "b_nuc;beta_A;b_mA",
            "claim_effect": "WEP/R10 composition pressure even if point-particle masses are fixed",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "VT1805_6_clock_readout_X",
            "sector": "readout",
            "operator_or_slot": "nu_i(Xhat), clock-frame normalization, or detector readout map",
            "classification": "forbidden_required_or_bounded",
            "coefficient": "b_clock_i;tau_clock",
            "claim_effect": "clock/redshift residual independent of WEP silence",
            "current_status": "blocks_claim",
            "valid_for_claim": False,
        },
    ]


def alpha_mass_clock_bound_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BM1805_0_alpha_clock",
            "arena": "clock_frequency_ratios",
            "observable": "d ln(nu_a/nu_b)",
            "bound_or_sensitivity_source": str(RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"),
            "projection_formula": "d ln R_ab = DeltaK_alpha_ab*b_alpha*dXhat + DeltaK_mu_ab*b_mu*dXhat + DeltaK_nuc_ab*b_nuc*dXhat + ...",
            "required_mts_inputs": "b_alpha or theorem-zero; b_mu/b_nuc; tau_clock/local dXhat; K_mu/K_nuc sources",
            "current_status": "SOURCE_SENSITIVITY_PARTIAL_MTS_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BM1805_1_clock_redshift",
            "arena": "redshift_LPI_clocks",
            "observable": "alpha_clock_redshift",
            "bound_or_sensitivity_source": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R2_clock_redshift",
            "projection_formula": "alpha_clock_redshift = P_clock[b_clock_i, metric_readout_residual, source potential map]",
            "required_mts_inputs": "clock readout map; local potential/source normalization; b_clock_i or theorem-zero",
            "current_status": "BOUND_ANCHOR_READY_PROJECTION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BM1805_2_WEP_alpha_mass",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_AB",
            "bound_or_sensitivity_source": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R1_WEP_source_charge",
            "projection_formula": "eta_AB = DeltaQ_alpha_AB*beta_source_alpha*b_alpha*tau_WEP + DeltaQ_mass_AB*b_mA*tau_WEP + DeltaQ_nuc_AB*b_nuc*tau_WEP + ...",
            "required_mts_inputs": "composition charge matrix; source/test beta vectors; tau_WEP; b_alpha/b_mA/b_nuc or theorem-zero",
            "current_status": "BOUND_ANCHOR_READY_COMPOSITION_MATRIX_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BM1805_3_R10_yukawa",
            "arena": "R10_short_range_fifth_force",
            "observable": "alpha_X(lambda_X)",
            "bound_or_sensitivity_source": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"),
            "projection_formula": "alpha_X(lambda_X) ~ K_X Qbar_source(lambda_X) Qbar_test(lambda_X)/(4*pi*Z_X*G_obs), with Qbar containing alpha/mass/nuclear/clock terms",
            "required_mts_inputs": "lambda_X; Z_X; K_X; Qbar_source/test; b_alpha/b_mA/b_nuc; promoted bound curve",
            "current_status": "BOUND_REVIEW_CANDIDATE_AND_MTS_COMPONENTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BM1805_4_PPN_source",
            "arena": "local_GR_PPN",
            "observable": "gamma,beta,alpha_i,xi,Gdot",
            "bound_or_sensitivity_source": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R3_gamma_through_R9_Gdot",
            "projection_formula": "PPN vector receives metric/source/readout residuals plus constant-sector source-normalization leakage",
            "required_mts_inputs": "weak-field solution; source Hamiltonian owner; constant leakage theorem-zero or bound vector",
            "current_status": "LOCAL_GR_NOT_SCORE_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def arena_projection_requirements_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "APR1805_0_no_cancellation_policy",
            "requirement": "alpha, mass, clock, marker and source residuals must be bounded as an absolute envelope unless a theorem forces cancellation",
            "why": "otherwise a tuned cancellation can fake local silence",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "APR1805_1_shared_domain",
            "requirement": "same local domain, screen/projection rule and Xhat normalization must be used for WEP, R10, clocks and PPN",
            "why": "arena-specific screening would be a hidden patch, not a unified field-theory derivation",
            "status": "MISSING_PARENT_RULE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "APR1805_2_dimensionless_guard",
            "requirement": "dimensionless alpha, mass ratios and clock ratios cannot be removed by unit conventions",
            "why": "unit choices only fix dimensionful coordinates/scales",
            "status": "PASSED_GUARD",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "APR1805_3_source_paths",
            "requirement": "every promoted bound row must cite source paths and contain no MISSING markers",
            "why": "keeps private smoke rows separate from claim rows",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "APR1805_4_radiative_readout_closure",
            "requirement": "a tree-level operator ban must also close effective/radiative/readout re-entry",
            "why": "otherwise the parent action can look clean while observed alpha/mass/clock rows still vary",
            "status": "MISSING_PARENT_RULE",
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "alpha_mass_clock_bound_matrix_template_1805",
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_K_X_QSOURCE_QTEST_FROM_B_ALPHA_B_MASS_B_CLOCK_OVER_4PI_ZX_G",
            "force_law_form": "alpha_X(lambda_X) projects the no-cancellation alpha/mass/clock source-test charge envelope into R10",
            "derivation_status": "template_invalid_no_extra_F2_no_mass_vertex_signature_or_bound_matrix_inputs_missing",
            "valid_for_claim": False,
        }
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1805_0_parent_signature",
            "gate": "parent vertex signature forbids dangerous alpha/mass/clock vertices",
            "current_status": "BLOCKED",
            "reason": "independent F2, mass, Yukawa, binding and readout vertices are not ruled out by current parent action",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1805_1_bound_matrix",
            "gate": "fallback alpha/mass/clock bound matrix score-ready",
            "current_status": "BLOCKED",
            "reason": "matrix has anchors/sensitivities but lacks MTS coefficient values, composition/source charges and local projections",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1805_2_no_public_claim",
            "gate": "no local-GR/R10/WEP/clock claim from this checkpoint",
            "current_status": "ACTIVE_GUARD",
            "reason": "all theorem and bound routes remain nonclaim",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1805_3_verdict",
            "gate": "constant-sector local branch closed by signature or bound matrix",
            "current_status": "SIGNATURE_NOT_SIGNED_BOUND_MATRIX_NOT_SCORE_READY",
            "reason": "the exact operator throat exists, but current evidence requires residual machinery rather than a theorem-zero claim",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1805_0_no_extra_F2",
            "claim": "independent f_X F^2 and lambda_A F^2 are forbidden by parent action",
            "status": "BLOCKED",
            "reason": "scalar gauge-kinetic counterterm remains covariant/gauge-invariant and not parent-forbidden",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1805_1_no_mass_vertex",
            "claim": "m_A(Xhat), y_A(Xhat), QCD/binding and material-response vertices are forbidden",
            "status": "BLOCKED",
            "reason": "matter spectrum and binding-response ownership are not derived",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1805_2_bound_matrix_score",
            "claim": "alpha/mass/clock bound matrix can score WEP/R10/clocks",
            "status": "BLOCKED",
            "reason": "source sensitivities and bounds are staged, but MTS-side local projections and coefficients are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1805_3_local_GR_Newton",
            "claim": "local-GR/Newton branch is closed by 1805",
            "status": "BLOCKED",
            "reason": "constant-sector closure is only one upstream prerequisite; PPN/source Hamiltonian gates remain separate",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1805_0_parent_signature",
            "decision": "NO_EXTRA_F2_NO_MASS_VERTEX_ROUTE_IS_CORRECT_THROAT_BUT_NOT_SIGNED",
            "reason": "the theorem would zero alpha/mass/clock leakage, but current corpus still allows the key countervertices",
            "next_action": "derive a symmetry/operator-classification ban or use the bound matrix as retained residual machinery",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1805_1_alpha_status",
            "decision": "B_ALPHA_REMAINS_LIVE",
            "reason": "f_X F^2 is covariant, gauge invariant and dimensionless, so unit choices cannot remove it",
            "next_action": "target parent gauge symmetry/connection-norm uniqueness or numeric b_alpha projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1805_2_mass_clock_status",
            "decision": "B_MU_B_MA_B_NUC_B_CLOCK_REMAIN_LIVE",
            "reason": "mass ratios, binding fractions and clock ratios are observable and not supplied by the parent action",
            "next_action": "target matter-spectrum ownership or source composition sensitivity matrix",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1805_3_best_next",
            "decision": "PARENT_OPERATOR_CLASSIFICATION_SYMMETRY_BAN_OR_RESIDUAL_PRIOR_NEXT",
            "reason": "we now know exactly which vertices must be absent for the derivation path to win",
            "next_action": "build 1806 to test operator classification/sequestration before sourcing residual prior widths",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1805_0_primary",
            "next_target": "1806-Y5-R2FR-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
            "script": "scripts/Y5_R2FR_parent_operator_classification_symmetry_ban_or_residual_coefficient_prior.py",
            "objective": "try to derive a parent symmetry/operator-classification rule that forbids f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), and clock-readout Xhat vertices; if it fails, assign nonclaim residual-prior slots for the alpha/mass/clock bound matrix",
            "selection_status": "selected",
            "success_condition": "derived visible/hidden operator separation or source-ready residual-prior slots with no claim promotion",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1805_1_parallel_projection",
            "next_target": "1806b-Y5-R2FR-alpha-mass-clock-composition-projection-sourcing.md",
            "script": "scripts/Y5_R2FR_alpha_mass_clock_composition_projection_sourcing.py",
            "objective": "source composition and clock sensitivity matrices for the fallback bound route",
            "selection_status": "held_parallel",
            "success_condition": "nonclaim projection rows with source-backed sensitivities and explicit missing MTS coefficients",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_vertex_signature_audit": parent_vertex_signature_audit_rows(),
        "no_extra_f2_theorem_attempt": no_extra_f2_theorem_attempt_rows(),
        "no_mass_vertex_theorem_attempt": no_mass_vertex_theorem_attempt_rows(),
        "allowed_forbidden_vertex_table": allowed_forbidden_vertex_table_rows(),
        "alpha_mass_clock_bound_matrix": alpha_mass_clock_bound_matrix_rows(),
        "arena_projection_requirements": arena_projection_requirements_rows(),
        "mts_r10_template": mts_r10_template_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1805_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "score_ready",
        "numeric_score_ready",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            for flag in claim_flags:
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ready_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "score_ready",
        "numeric_score_ready",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in ready_flags:
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1805_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1805_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1805_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1805_2_parent_signature_blocked",
            any(
                row["clause_id"] == "PVS1805_6_verdict"
                and row["current_status"] == "FAIL_CURRENT_CLAIM_BOUND_MATRIX_REQUIRED"
                for row in rows_map["parent_vertex_signature_audit"]
            ),
            "parent vertex signature attempt remains blocked",
        ),
        (
            "VAL1805_3_no_extra_F2_blocked",
            any(
                row["theorem_id"] == "F2T1805_4_verdict"
                and row["current_status"] == "FAIL_CURRENT_CLAIM_RETAIN_B_ALPHA"
                for row in rows_map["no_extra_f2_theorem_attempt"]
            ),
            "no-extra-F2 theorem fails current corpus because scalar/counterterm F2 is not forbidden",
        ),
        (
            "VAL1805_4_no_mass_vertex_blocked",
            any(
                row["theorem_id"] == "MVT1805_4_verdict"
                and row["current_status"] == "FAIL_CURRENT_CLAIM_RETAIN_MASS_CLOCK_MATRIX"
                for row in rows_map["no_mass_vertex_theorem_attempt"]
            ),
            "no-mass-vertex theorem fails current corpus because matter spectrum/readout are not parent-derived",
        ),
        (
            "VAL1805_5_forbidden_vertices_catalogued",
            len(rows_map["allowed_forbidden_vertex_table"]) >= 7
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["allowed_forbidden_vertex_table"]),
            "key alpha/mass/clock hidden vertices are catalogued",
        ),
        (
            "VAL1805_6_bound_matrix_nonclaim",
            len(rows_map["alpha_mass_clock_bound_matrix"]) >= 5
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_mass_clock_bound_matrix"]),
            "alpha/mass/clock bound matrix is staged as nonclaim",
        ),
        (
            "VAL1805_7_arena_guards_present",
            any(row["requirement_id"] == "APR1805_0_no_cancellation_policy" for row in rows_map["arena_projection_requirements"])
            and any(row["requirement_id"] == "APR1805_2_dimensionless_guard" for row in rows_map["arena_projection_requirements"]),
            "dimensionless guard and arena policies are present",
        ),
        (
            "VAL1805_8_mts_template_schema_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1805_9_acceptance_blocks",
            any(
                row["gate_id"] == "AC1805_3_verdict"
                and row["current_status"] == "SIGNATURE_NOT_SIGNED_BOUND_MATRIX_NOT_SCORE_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks 1805 closure",
        ),
        (
            "VAL1805_10_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all no-extra-F2/no-mass/local claim gates remain blocked",
        ),
        ("VAL1805_11_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1805_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1805_13_decision_next",
            any(
                row["decision_id"] == "DEC1805_3_best_next"
                and row["decision"] == "PARENT_OPERATOR_CLASSIFICATION_SYMMETRY_BAN_OR_RESIDUAL_PRIOR_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects operator classification/symmetry ban next",
        ),
        (
            "VAL1805_14_next_selected",
            any(row["route_id"] == "NEXT1805_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1805_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1805 CSVs parse"),
        ("VAL1805_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1805_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1805_18_formalization_untouched", formalization_untouched(), "no 1805 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1805_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1805 no-extra-F2 no-mass-vertex signature or alpha/mass/clock bound matrix checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1805 - Y5/R2FR No-Extra-F2, No-Mass-Vertex Signature or Alpha/Mass/Clock Bound Matrix",
            "",
            "## Verdict",
            "",
            "1805 identifies the correct parent-action throat for the constant/coupling problem. If the parent action signs one unique EM curvature norm, forbids independent `f_X(Xhat)F_Q^2`, forbids `m_A(Xhat)`, `y_A(Xhat)`, QCD/binding/material-response vertices, and closes clock/readout re-entry, then the constant sector can be zeroed by derivation rather than fitted.",
            "",
            "That route is mathematically clean but not currently signed. Diffeomorphism covariance and gauge invariance do not forbid the dangerous vertices; a scalar gauge-kinetic term and mass/binding response functions remain legal unless a stronger parent operator-classification or visible/hidden product rule is derived.",
            "",
            "So this checkpoint does not claim `b_alpha=0`, `b_mu=0`, `b_mA=0`, `b_nuc=0`, `b_clock_i=0`, or `qbar_constants_abs=0`. It stages the fallback alpha/mass/clock bound matrix for clocks, WEP, R10, and PPN/source arenas, while keeping every row nonclaim.",
            "",
            "**Claim ceiling:** no no-extra-F2 theorem, no no-mass-vertex theorem, no clock-readout theorem, no alpha/mass/clock bound-matrix score, no local-GR/Newton claim, no R10/WEP/clock claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1805.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Parent Vertex Signature Audit",
            markdown_table(rows_map["parent_vertex_signature_audit"], ["clause_id", "signature_clause", "minimal_form", "current_status", "blocks_if_missing", "valid_for_claim"]),
            "",
            "## No-Extra-F2 Theorem Attempt",
            markdown_table(rows_map["no_extra_f2_theorem_attempt"], ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "",
            "## No-Mass-Vertex Theorem Attempt",
            markdown_table(rows_map["no_mass_vertex_theorem_attempt"], ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "",
            "## Allowed/Forbidden Vertex Table",
            markdown_table(rows_map["allowed_forbidden_vertex_table"], ["vertex_id", "sector", "operator_or_slot", "classification", "coefficient", "claim_effect", "current_status", "valid_for_claim"]),
            "",
            "## Alpha/Mass/Clock Bound Matrix",
            markdown_table(rows_map["alpha_mass_clock_bound_matrix"], ["matrix_id", "arena", "observable", "projection_formula", "required_mts_inputs", "current_status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Arena Projection Requirements",
            markdown_table(rows_map["arena_projection_requirements"], ["requirement_id", "requirement", "why", "status", "valid_for_claim"]),
            "",
            "## MTS R10 Smoke Template",
            markdown_table(rows_map["mts_r10_template"], ["model_id", "branch_id", "lambda_value", "alpha_predicted", "derivation_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "The path is now clear rather than vague. The coupling does look like the right bottleneck: not because it kills MTS, but because it is where the parent action has to stop being a flexible story and become a strict operator grammar. The best next move is to test whether a visible/hidden operator-classification rule can be derived rather than merely adopted.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1805 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
