from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1791"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1791_0_1790_doc",
        "source_key": "1790_handoff",
        "source_path": ROOT / "1790-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-input-pack-smoke-runner.md",
        "needles": ["DEC1790_3_next", "NEXT1790_0_primary"],
        "role": "selects response-displacement conjugacy refresh or q_loc profile pack as 1791 target",
    },
    {
        "source_id": "SRC1791_1_1790_validation",
        "source_key": "1790_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1790_VALIDATION.csv",
        "needles": ["VAL1790_OVERALL", "PASS"],
        "role": "confirms 1790 passed before 1791 continues the same branch",
    },
    {
        "source_id": "SRC1791_2_1790_owner_bundle",
        "source_key": "1790_owner_bundle",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_OWNER_BUNDLE_GATE.csv",
        "needles": ["OBG1790_1_Khat_response", "OBG1790_6_verdict"],
        "role": "records Gamma/Khat/Ploc owner bundle blockers",
    },
    {
        "source_id": "SRC1791_3_1790_response_link",
        "source_key": "1790_response_to_cr2",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_RESPONSE_TO_CR2_LINK.csv",
        "needles": ["RCL1790_0_effective_law", "RCL1790_5_verdict"],
        "role": "ties the local response owner to c_R2_eff and q_loc gates",
    },
    {
        "source_id": "SRC1791_4_1790_q_loc_pack",
        "source_key": "1790_q_loc_fallback",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv",
        "needles": ["QLP1790_0_formula", "QLP1790_4_verdict"],
        "role": "records q_loc profile as formula-only before 1791",
    },
    {
        "source_id": "SRC1791_5_1789_effective_pack",
        "source_key": "1789_effective_cr2",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_EFFECTIVE_CR2_COEFFICIENT_PACK.csv",
        "needles": ["CEC1789_0_effective_law", "CEC1789_4_verdict"],
        "role": "provides effective coefficient law and missing executable coefficient verdict",
    },
    {
        "source_id": "SRC1791_6_1712_conjugacy",
        "source_key": "1712_conjugacy_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv",
        "needles": ["CJA1712_1_even_density", "CJA1712_6_verdict"],
        "role": "base response-displacement conjugacy attempt",
    },
    {
        "source_id": "SRC1791_7_1712_metric_identity",
        "source_key": "1712_metric_identity",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
        "needles": ["MRI1712_2_projected_Ward", "MRI1712_4_verdict"],
        "role": "Ward/metric-response identity audit",
    },
    {
        "source_id": "SRC1791_8_1712_blockers",
        "source_key": "1712_conjugacy_blockers",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_CONJUGACY_BLOCKER_AUDIT.csv",
        "needles": ["BLK1712_0_component_lock", "BLK1712_6_verdict"],
        "role": "component, source, metric, operator, projector and boundary blockers",
    },
    {
        "source_id": "SRC1791_9_1712_profile",
        "source_key": "1712_first_q_loc_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
        "needles": ["QPROF1712_0_parent_residual_vector", "QPROF1712_4_theorem_zero_certificate"],
        "role": "first q_loc profile row remains template-only",
    },
    {
        "source_id": "SRC1791_10_1353_z_lock",
        "source_key": "1353_z_component_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1353_Z_COMPONENT_LOCK_ATTEMPT.csv",
        "needles": ["ZLOCK1353_2_observable_lock", "ZLOCK1353_4_verdict"],
        "role": "formal Z doublet does not yet equal the physical q_loc/PPN/source-normalization vector",
    },
    {
        "source_id": "SRC1791_11_1353_no_linear_source",
        "source_key": "1353_no_linear_source",
        "source_path": RESIDUALS / "P8_Y5_R10_1353_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv",
        "needles": ["NLS1353_0_exchange_symmetry", "NLS1353_5_verdict"],
        "role": "no-linear-source theorem is the key coupling lock",
    },
    {
        "source_id": "SRC1791_12_1353_jz_bz",
        "source_key": "1353_jz_bz_source_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1353_JZ_BZ_SOURCE_PACK.csv",
        "needles": ["JZ1353_0_bulk_JZ", "JZ1353_3_Y6_extra_stress"],
        "role": "names the missing J_Z/B_Z/Y5/Y6 source coefficients",
    },
    {
        "source_id": "SRC1791_13_1712_next",
        "source_key": "1712_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_NEXT_TARGET.csv",
        "needles": ["NEXT1712_0_primary", "source-functional evenness"],
        "role": "prior next target already selected the coupling lock route",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_SOURCE_REGISTER.csv",
    "conjugacy_theorem_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_CONJUGACY_THEOREM_CONTRACT.csv",
    "ward_identity_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_WARD_IDENTITY_DERIVATION.csv",
    "amplitude_and_cr2_law": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_AMPLITUDE_AND_CR2_LAW.csv",
    "activation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_ACTIVATION_AUDIT.csv",
    "q_loc_cr2_profile_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_QLOC_CR2_PROFILE_PACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1791_VALIDATION.csv",
}

DOC_PATH = ROOT / "1791-Y5-R2FR-response-displacement-conjugacy-owner-refresh-or-q_loc-profile-pack.md"


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


def conjugacy_theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_0_parent_action_candidate",
            "statement": "candidate response-displacement parent action",
            "mathematical_form": "S_RD = integral sqrt(-g)[Gamma_0(E,g) + 1/2 Z^A M_AB(E,g,nabla) Z^B + O(Z^4)] with E^A=(R_+^A+R_-^A)/2 and Z^A=(R_+^A-R_-^A)/2",
            "derived_result": "EXACT_CONDITIONAL_TEMPLATE",
            "activation_gap": "physical Y0-Y6 component coverage, operator domain, units and source coupling are not parent-locked",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_1_F1_zero",
            "statement": "exchange-even action gives formal local extremum",
            "mathematical_form": "Z -> -Z invariance implies delta Gamma_eff/delta Z^A |_{Z=0}=0, so F_1=0 for the shadow doublet variable",
            "derived_result": "FORMAL_F1_ZERO_DERIVED_CONDITIONALLY",
            "activation_gap": "formal Z=0 is not yet proved to be the physical q_loc/PPN/source-normalization residual zero",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_2_Khat_metric_owner",
            "statement": "K_hat must be the metric response of the same Gamma_eff density",
            "mathematical_form": "K_metric^{mu nu} = 2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu}; require K_hat^{mu nu}=K_metric^{mu nu} term by term",
            "derived_result": "IDENTITY_WRITTEN_NOT_SYMBOL_MATCHED",
            "activation_gap": "live K_hat tensor, sign convention, derivative terms and boundary terms are not matched",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_3_no_odd_coupling",
            "statement": "source, matter, boundary and readout functionals must have no odd Z coupling",
            "mathematical_form": "J_Z^A = delta S_source/delta Z_A|_0 = 0; B_Z^A=0; B_R^A=0 unless finite source-backed coefficient rows are supplied",
            "derived_result": "COUPLING_LOCK_NOT_DERIVED",
            "activation_gap": "Y5 source-normalization, Y6 extra-stress, material/species and readout source channels remain open",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_4_exact_conditional_theorem",
            "statement": "local vacuum plateau follows only under the full parent action contract",
            "mathematical_form": "if CTC1791_0..3 plus P_loc owner, no-flux boundary and on-shell conditions hold, then q_loc^nu=0 and no c_R2_eff tail is generated by the response doublet",
            "derived_result": "EXACT_CONDITIONAL_THEOREM",
            "activation_gap": "premises are stronger than current corpus evidence",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "CTC1791_5_verdict",
            "statement": "response-displacement conjugacy owner refresh",
            "mathematical_form": "conditional theorem retained; MTS activation requires component lock, no-linear-source lock, Khat match, P_loc owner, boundary no-flux, and arena maps",
            "derived_result": "CONDITIONAL_THEOREM_NOT_MTS_ACTIVATED",
            "activation_gap": "cannot promote local GR, q_loc zero, c_R2 zero, R10, or PPN from this checkpoint",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ward_identity_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "ward_id": "WID1791_0_diffeomorphism_variation",
            "identity_step": "vary the parent response-displacement action under infinitesimal diffeomorphism",
            "mathematical_form": "delta_xi S_RD = integral sqrt(-g) xi_nu[ nabla_mu K_metric^{mu nu} - nabla^nu Gamma_eff + E_A nabla^nu Z^A + J_Z^nu + B_Z^nu + C_readout^nu + boundary^nu ]",
            "result": "FORMAL_NOETHER_IDENTITY",
            "zero_condition": "K_hat=K_metric and all Euler/source/boundary/readout terms vanish",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ward_id": "WID1791_1_projected_residual",
            "identity_step": "apply the local projector fixed before readout",
            "mathematical_form": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "result": "PROJECTED_RESIDUAL_FORM",
            "zero_condition": "P_loc is parent-owned and commutes with the compact local limit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ward_id": "WID1791_2_zero_branch",
            "identity_step": "on-shell exchange-even source-free branch",
            "mathematical_form": "E_A=0, J_Z=B_Z=C_readout=boundary=0, K_hat=K_metric => q_loc^nu=0",
            "result": "EXACT_CONDITIONAL_ZERO",
            "zero_condition": "requires parent-signed source-functional evenness and no-flux theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ward_id": "WID1791_3_finite_residual_branch",
            "identity_step": "if any source or boundary term survives",
            "mathematical_form": "q_loc^nu = -P_loc(E_A nabla^nu Z^A + J_Z^nu + B_Z^nu + C_readout^nu + boundary^nu + Delta_K^{nu})",
            "result": "FINITE_PROFILE_REQUIRED",
            "zero_condition": "numeric/theorem-zero rows required for every surviving source term",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ward_id": "WID1791_4_verdict",
            "identity_step": "Ward route status",
            "mathematical_form": "the identity explains exactly what must vanish; it does not prove those terms vanish in current MTS",
            "result": "WARD_ROUTE_CONDITIONAL_NOT_CLAIM",
            "zero_condition": "next target must attack J_Z/B_Z/Y5/Y6 coupling lock",
            "valid_for_claim": False,
        },
    ]


def amplitude_and_cr2_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_0_sourced_extremum",
            "object": "response displacement amplitude",
            "mathematical_form": "M_AB Z^B + N_A[Z^3] = J_A + B_A^R R + B_A^T T + B_A^bdy K_bdy + B_A^readout",
            "interpretation": "formal F1=0 becomes physical only if the right-hand source vector is zero or source-backed",
            "current_status": "SOURCE_VECTOR_NOT_OWNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_1_amplitude_bound",
            "object": "Delta amplitude / mass-gap bound",
            "mathematical_form": "if M is positive self-adjoint on the gauge-reduced local domain and ||M^{-1} N[Z^3]|| <= epsilon||Z||, then ||Z|| <= ||M^{-1}||||J_total||/(1-epsilon)",
            "interpretation": "this is the exact bound structure needed to replace a plateau axiom with a source-response estimate",
            "current_status": "MISSING_M_OPERATOR_DOMAIN_AND_J_TOTAL",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_2_transition_length",
            "object": "ell_tr/L_cg",
            "mathematical_form": "m_X^2 = lambda_min(M_AB/Z_inner_product); ell_tr = 1/m_X; ell_tr/L_cg = 1/(m_X L_cg)",
            "interpretation": "the local transition scale is derivable only after the operator normalization, inner product, and L_cg owner are fixed",
            "current_status": "MISSING_OPERATOR_NORMALIZATION_AND_LCG_OWNER",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_3_cR2_eff_law",
            "object": "c_R2_eff",
            "mathematical_form": "c_R2_eff = c_bare + 1/2 B_R^T M^{-1} B_R + c_measure + c_boundary + c_field_redef_remnant",
            "interpretation": "same response Hessian either gives a finite R2/fR coefficient or is zero only if all vertices and remnants vanish",
            "current_status": "MISSING_BR_M_INVERSE_MEASURE_BOUNDARY_VALUES",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_4_zero_conditions",
            "object": "theorem-zero route",
            "mathematical_form": "J_total=0, B_R=0, c_bare=0, c_measure=0, c_boundary=0, P_loc owner and no-flux boundary => q_loc=0 and c_R2_eff=0",
            "interpretation": "this is the exact contract a future parent action must satisfy",
            "current_status": "ZERO_CONDITIONS_NOT_PARENT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "ACL1791_5_verdict",
            "object": "amplitude/c_R2 derivation status",
            "mathematical_form": "derivation gives the shape of the law but no numeric or theorem-zero MTS row",
            "interpretation": "use the law as the next coupling hunt, not as a pass",
            "current_status": "LAW_DERIVED_CONDITIONALLY_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def activation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_0_parent_action",
            "required_activation": "source-checkable S_RD with Gamma_eff, M_AB, fields, dimensions and derivative order",
            "current_evidence": "CTC1791_0 is a conditional template only",
            "status": "OPEN",
            "next_attack": "write or source the actual parent action density",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_1_component_lock",
            "required_activation": "Z^A covers Y0-Y6 and equals q_loc/PPN/source-normalization residual vector",
            "current_evidence": "ZLOCK1353_4_verdict COMPONENT_LOCK_NOT_PROVED",
            "status": "OPEN_HARD_BLOCK",
            "next_attack": "map Z^A into R10, PPN, clock, orbital, R11 and source-normalization channels",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_2_no_linear_source",
            "required_activation": "J_Z=B_Z=0 or finite sourced values for matter, boundary, source-normalization, species and readout",
            "current_evidence": "NLS1353_5_verdict THEOREM_NOT_PROVED; JZ1353 rows missing",
            "status": "OPEN_HARD_BLOCK",
            "next_attack": "prove exchange-even source functional or fill J_Z/B_Z coefficient rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_3_Khat_match",
            "required_activation": "live K_hat equals metric response of the same Gamma_eff",
            "current_evidence": "MRI1712_4_verdict not_symbol_matched; OBG1790_1_Khat_response NOT_MATCHED",
            "status": "OPEN",
            "next_attack": "compute metric variation from chosen Gamma_eff and compare tensor components",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_4_operator_domain",
            "required_activation": "M_AB positive, self-adjoint, gauge-reduced and unit-normalized",
            "current_evidence": "BLK1712_4_operator_domain OPEN",
            "status": "OPEN",
            "next_attack": "declare inner product, gauge quotient, boundary domain and units",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_5_projector_boundary",
            "required_activation": "P_loc owner and boundary no-flux before readout",
            "current_evidence": "BLK1712_5_projector_boundary OPEN; OBG1790_2_Ploc_owner OPEN_PROJECTOR_OWNER",
            "status": "OPEN",
            "next_attack": "derive projection order and linked-sphere flux silence",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_6_cR2_source_normalization",
            "required_activation": "B_R, M^{-1}, c_bare, measure, boundary and field-redefinition terms zero or numeric/source-backed",
            "current_evidence": "RCL1790_5_verdict CANNOT_ZERO_OR_SCORE_CR2_QLOC",
            "status": "OPEN_HARD_BLOCK",
            "next_attack": "source or zero the response Hessian vertices",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ACT1791_7_verdict",
            "required_activation": "all activation clauses close together",
            "current_evidence": "multiple open hard blocks",
            "status": "CONJUGACY_NOT_ACTIVATED",
            "next_attack": "source-functional evenness and J_Z/B_Z coupling lock is the highest-leverage next route",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def q_loc_cr2_profile_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_0_identity",
            "row_type": "branch identity",
            "required_field": "model_id;operator_family",
            "current_value": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428;q_loc_cR2_response_pack",
            "units_required": "not applicable",
            "source_path_required": "this checkpoint",
            "row_status": "CONTRACT_ONLY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_1_q_loc_formula",
            "row_type": "q_loc theorem/profile slot",
            "required_field": "q_loc^nu expression or theorem-zero certificate",
            "current_value": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) plus source residual terms",
            "units_required": "force-density/stress-divergence units in SI or geometrized units with conversion",
            "source_path_required": "Gamma_eff/Khat/Ploc parent action and metric response files",
            "row_status": "FORMULA_ONLY_NOT_SCOREABLE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_2_source_vector",
            "row_type": "finite residual source vector",
            "required_field": "J_Z;B_Z;Y5;Y6;species;readout;boundary coefficients",
            "current_value": "MISSING_JZ_BZ_Y5_Y6_SOURCE_VECTOR",
            "units_required": "same inner-product-normalized units as M_AB Z^B",
            "source_path_required": "source-functional variation or coefficient extraction path for every nonzero term",
            "row_status": "REJECT_MISSING_SOURCE_VECTOR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_3_operator",
            "row_type": "response Hessian/operator",
            "required_field": "M_AB or L_X; inverse; positivity; boundary domain; mass gap",
            "current_value": "MISSING_M_OPERATOR_AND_INVERSE",
            "units_required": "operator units, inner product, eigenvalue/mass-gap convention, ell_tr/L_cg",
            "source_path_required": "parent action Hessian calculation",
            "row_status": "REJECT_MISSING_OPERATOR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_4_cR2_coefficient",
            "row_type": "R2/fR coefficient slot",
            "required_field": "c_R2_eff or theorem-zero certificate",
            "current_value": "MISSING_c_bare_B_R_M_inverse_measure_boundary_values",
            "units_required": "length^2 for c_R2 in action convention or explicit fRR normalization",
            "source_path_required": "response Hessian curvature vertex and normalization source",
            "row_status": "REJECT_MISSING_CR2_INPUTS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_5_R10_projection",
            "row_type": "R10 projection slot",
            "required_field": "alpha(lambda)=K_X(lambda) Qbar_XH(lambda) qbar_XT(lambda) from parent coefficients",
            "current_value": "MISSING_K_X_QBAR_XH_QBAR_XT_LAMBDA_X",
            "units_required": "dimensionless alpha and SI length lambda",
            "source_path_required": "parent q_loc/c_R2 coefficient file and source-backed bound curve",
            "row_status": "REJECT_MISSING_R10_PROJECTION",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_6_PPN_clock_orbital",
            "row_type": "local arena projection slots",
            "required_field": "PPN vector; clock shift; orbital residual; measured-GM/source-normalization map",
            "current_value": "MISSING_WEAK_FIELD_CLOCK_ORBITAL_SOURCE_MAPS",
            "units_required": "dimensionless PPN, fractional frequency, acceleration/precession, GM drift",
            "source_path_required": "weak-field gauge map, clock/orbital response, and source-normalization operator",
            "row_status": "REJECT_MISSING_ARENA_MAPS",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "QCP1791_7_acceptance",
            "row_type": "acceptance gate",
            "required_field": "theorem-zero bundle or complete finite numeric/source-backed pack",
            "current_value": "NEITHER_CONDITION_MET",
            "units_required": "all units explicit",
            "source_path_required": "all cited files must exist and parse",
            "row_status": "REJECT_CURRENT_PROFILE_PACK",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_0_shadow_zero",
            "countermodel": "formal Z double-zero exists but physical q_loc/PPN/source-normalization residual is outside Z",
            "survives_current_constraints": True,
            "why_survives": "component lock remains not proved",
            "what_kills_it": "source-backed Z^A map covering Y0-Y6 and all local arenas",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_1_odd_source",
            "countermodel": "matter, source-normalization, boundary, species or readout terms generate an odd linear J_Z",
            "survives_current_constraints": True,
            "why_survives": "no-linear-source theorem is not parent-signed",
            "what_kills_it": "exchange-even source-functional theorem or finite sourced J_Z rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_2_curvature_vertex",
            "countermodel": "response displacement couples linearly to curvature and regenerates c_R2_eff through B_R^T M^{-1} B_R",
            "survives_current_constraints": True,
            "why_survives": "B_R and M^{-1} are not sourced or zeroed",
            "what_kills_it": "B_R=0 theorem or complete finite c_R2 coefficient pack",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_3_uncontrolled_operator",
            "countermodel": "M_AB has wrong sign, zero modes, gauge modes, or undefined boundary domain",
            "survives_current_constraints": True,
            "why_survives": "operator positivity/domain is open",
            "what_kills_it": "positive self-adjoint gauge-reduced operator with mass gap and units",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_4_Khat_mismatch",
            "countermodel": "K_hat is not the metric response of Gamma_eff, so Ward cancellation is symbolic",
            "survives_current_constraints": True,
            "why_survives": "term-by-term metric response match is missing",
            "what_kills_it": "live Khat equals K_metric[Gamma_eff] including boundary terms",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1791_5_Ploc_tuning",
            "countermodel": "P_loc projection is tuned after readout to silence residuals",
            "survives_current_constraints": True,
            "why_survives": "projector owner is open",
            "what_kills_it": "parent-fixed covariant projector before readout",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_0_conjugacy_theorem",
            "claim": "response-displacement conjugacy is an activated MTS parent theorem",
            "status": "BLOCKED",
            "reason": "conditional theorem exists but activation clauses are not source-backed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_1_F1_zero_physical",
            "claim": "F1=0 proves physical q_loc/local-vacuum plateau",
            "status": "BLOCKED",
            "reason": "formal double-zero lacks component lock and no-linear-source theorem",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_2_q_loc_zero_or_profile",
            "claim": "q_loc is theorem-zero or finite score-ready",
            "status": "BLOCKED",
            "reason": "q_loc/c_R2 profile pack is rejected for missing source vector, operator, units and arena maps",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_3_cR2_zero_or_value",
            "claim": "c_R2_eff is theorem-zero or finite parent coefficient",
            "status": "BLOCKED",
            "reason": "B_R, M^{-1}, c_bare, measure and boundary terms are missing",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_4_R10_PPN_clock_orbital_score",
            "claim": "R10/PPN/clock/orbital scores can be run",
            "status": "BLOCKED",
            "reason": "profile pack has no numeric parent coefficients or projection maps",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1791_5_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "conjugacy, coupling, Khat, P_loc, boundary, c_R2 and PPN/source-normalization gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1791_0_conditional_theorem",
            "decision": "CONJUGACY_THEOREM_DERIVED_ONLY_CONDITIONALLY",
            "reason": "exchange-even response-displacement action does give formal F1=0 and a Ward route to q_loc=0",
            "next_action": "do not claim; activate by proving component lock and source-functional evenness",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1791_1_amplitude_law",
            "decision": "AMPLITUDE_AND_CR2_LAW_WRITTEN",
            "reason": "the same Hessian controls ||Z||, ell_tr/L_cg and c_R2_eff through M^{-1}, J_total and B_R",
            "next_action": "fill or theorem-zero M_AB, J_total, B_R, c_bare, measure and boundary rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1791_2_profile_pack",
            "decision": "STRICT_QLOC_CR2_PROFILE_PACK_EMITTED_NONCLAIM",
            "reason": "fallback pack now names exact missing source vector, operator, coefficient, units and arena-map fields",
            "next_action": "use it as the input contract for future tests, not as current evidence",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1791_3_next",
            "decision": "SOURCE_FUNCTIONAL_EVENNESS_AND_JZ_BZ_COUPLING_LOCK_NEXT",
            "reason": "the coupling is now the central hinge: if source functionals are exchange-even, F1=0 can become physical; if not, finite profiles must be acquired",
            "next_action": "build 1792 coupling-lock attempt or explicit J_Z/B_Z/Y5/Y6 acquisition ledger",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1791_0_primary",
            "next_target": "1792-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "script": "scripts/Y5_R2FR_source_functional_evenness_and_JZ_BZ_coupling_lock_or_profile_acquisition.py",
            "objective": "try to prove matter, source-normalization, species, boundary and readout functionals are exchange-even in Z; if not, emit explicit nonclaim J_Z/B_Z/Y5/Y6 coefficient acquisition rows",
            "selection_status": "selected",
            "success_condition": "parent-signed no-linear-source theorem, or source-backed finite coupling/profile rows with units and arena maps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1791_1_parallel_metric",
            "next_target": "1792b-Y5-R2FR-live-Khat-metric-variation-comparison.md",
            "script": "scripts/Y5_R2FR_live_Khat_metric_variation_comparison.py",
            "objective": "compute K_metric from any chosen Gamma_eff density and compare against live K_hat components",
            "selection_status": "held_parallel",
            "success_condition": "term-by-term metric response match or explicit mismatch ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1791_2_parallel_cR2",
            "next_target": "1792c-Y5-R2FR-response-Hessian-cR2-coefficient-input-pack.md",
            "script": "scripts/Y5_R2FR_response_Hessian_cR2_coefficient_input_pack.py",
            "objective": "source or theorem-zero B_R, M_inverse, c_bare, measure and boundary pieces for c_R2_eff",
            "selection_status": "held_until_coupling_lock",
            "success_condition": "complete c_R2/fRR coefficient pack or strict nonclaim blocker ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "conjugacy_theorem_contract": conjugacy_theorem_contract_rows(),
        "ward_identity_derivation": ward_identity_derivation_rows(),
        "amplitude_and_cr2_law": amplitude_and_cr2_law_rows(),
        "activation_audit": activation_audit_rows(),
        "q_loc_cr2_profile_pack": q_loc_cr2_profile_pack_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
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
        shutil.copy2(path, RAB_QUEUE / f"JR1791_{key.upper()}.csv")


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
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "score_emitted",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "score_emitted",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
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
        if not (RAB_QUEUE / f"JR1791_{key.upper()}.csv").exists():
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
        ("VAL1791_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1791_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1791_2_conditional_theorem_written",
            any(
                row["contract_id"] == "CTC1791_4_exact_conditional_theorem"
                and row["derived_result"] == "EXACT_CONDITIONAL_THEOREM"
                for row in rows_map["conjugacy_theorem_contract"]
            ),
            "response-displacement conditional theorem is written",
        ),
        (
            "VAL1791_3_theorem_not_activated",
            any(
                row["contract_id"] == "CTC1791_5_verdict"
                and row["derived_result"] == "CONDITIONAL_THEOREM_NOT_MTS_ACTIVATED"
                for row in rows_map["conjugacy_theorem_contract"]
            )
            and all(not boolish(row["theorem_closed_for_claim"]) and not boolish(row["valid_for_claim"]) for row in rows_map["conjugacy_theorem_contract"]),
            "conditional theorem is not promoted to an MTS claim",
        ),
        (
            "VAL1791_4_ward_zero_and_residual",
            any(row["ward_id"] == "WID1791_2_zero_branch" and row["result"] == "EXACT_CONDITIONAL_ZERO" for row in rows_map["ward_identity_derivation"])
            and any(row["ward_id"] == "WID1791_3_finite_residual_branch" and row["result"] == "FINITE_PROFILE_REQUIRED" for row in rows_map["ward_identity_derivation"]),
            "Ward identity records both zero and finite-residual branches",
        ),
        (
            "VAL1791_5_amplitude_and_cr2_laws",
            any(row["law_id"] == "ACL1791_1_amplitude_bound" for row in rows_map["amplitude_and_cr2_law"])
            and any(row["law_id"] == "ACL1791_3_cR2_eff_law" for row in rows_map["amplitude_and_cr2_law"])
            and any(row["law_id"] == "ACL1791_5_verdict" and row["current_status"] == "LAW_DERIVED_CONDITIONALLY_INPUTS_MISSING" for row in rows_map["amplitude_and_cr2_law"]),
            "amplitude bound and c_R2 law are written but input-missing",
        ),
        (
            "VAL1791_6_activation_audit_blocks",
            any(row["audit_id"] == "ACT1791_7_verdict" and row["status"] == "CONJUGACY_NOT_ACTIVATED" for row in rows_map["activation_audit"])
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["activation_audit"]),
            "activation audit blocks current theorem promotion",
        ),
        (
            "VAL1791_7_profile_pack_rejected",
            any(row["pack_id"] == "QCP1791_7_acceptance" and row["row_status"] == "REJECT_CURRENT_PROFILE_PACK" for row in rows_map["q_loc_cr2_profile_pack"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["q_loc_cr2_profile_pack"]),
            "q_loc/c_R2 profile pack is strict and rejected",
        ),
        (
            "VAL1791_8_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1791_9_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1791_10_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1791_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1791_12_decision_next",
            any(
                row["decision_id"] == "DEC1791_3_next"
                and row["decision"] == "SOURCE_FUNCTIONAL_EVENNESS_AND_JZ_BZ_COUPLING_LOCK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects coupling-lock next",
        ),
        (
            "VAL1791_13_next_selected",
            any(row["route_id"] == "NEXT1791_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1791_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1791 CSVs parse"),
        ("VAL1791_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1791_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1791_17_formalization_untouched", formalization_untouched(), "no 1791 outputs found under formalization-workbench"),
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
            "check_id": "VAL1791_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1791 response-displacement conjugacy owner refresh or q_loc/c_R2 profile pack checkpoint",
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
            "# 1791 - Y5/R2FR Response-Displacement Conjugacy Owner Refresh or q_loc Profile Pack",
            "",
            "## Verdict",
            "",
            "1791 derives the clean conditional structure, but refuses to smuggle it into a local-GR claim. If the parent action is exchange-even in the response displacement `Z^A`, then the formal first variation vanishes at `Z=0`: `F_1=0`. If `K_hat` is also the metric response of the same `Gamma_eff`, and if `P_loc`, source, boundary and readout terms are parent-owned, the diffeomorphism/Ward identity gives `q_loc^nu=0`.",
            "",
            "The catch is exactly the coupling. A surviving odd source vector gives",
            "",
            "`M_AB Z^B + N_A[Z^3] = J_A + B_A^R R + B_A^T T + B_A^bdy K_bdy + B_A^readout`,",
            "",
            "so the finite branch needs `M_AB`, `J_total`, `B_R`, units, boundary conditions and arena maps. The same Hessian controls the local amplitude bound, `ell_tr/L_cg`, and `c_R2_eff = c_bare + 1/2 B_R^T M^{-1}B_R + ...`. Those laws are now explicit, but their parent inputs are still missing.",
            "",
            "**Claim ceiling:** no activated conjugacy theorem, no physical `F_1=0` claim, no `q_loc=0`, no `c_R2=0`, no R10/PPN/clock/orbital score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1791.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Conjugacy Theorem Contract",
            markdown_table(rows_map["conjugacy_theorem_contract"], ["contract_id", "statement", "mathematical_form", "derived_result", "activation_gap", "valid_for_claim"]),
            "",
            "## Ward Identity Derivation",
            markdown_table(rows_map["ward_identity_derivation"], ["ward_id", "identity_step", "mathematical_form", "result", "zero_condition", "valid_for_claim"]),
            "",
            "## Amplitude and cR2 Law",
            markdown_table(rows_map["amplitude_and_cr2_law"], ["law_id", "object", "mathematical_form", "interpretation", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Activation Audit",
            markdown_table(rows_map["activation_audit"], ["audit_id", "required_activation", "current_evidence", "status", "next_attack", "valid_for_claim"]),
            "",
            "## q_loc / cR2 Profile Pack",
            markdown_table(rows_map["q_loc_cr2_profile_pack"], ["pack_id", "row_type", "required_field", "current_value", "units_required", "source_path_required", "row_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
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
            "This is a useful tightening. The local plateau can be a theorem only if the coupling lock closes. The next target is therefore not another broad GR paragraph; it is the source-functional evenness/J_Z/B_Z coupling hunt. Either the source functional is even in `Z` and the double-zero becomes physical, or the theory must own a finite residual profile with coefficients and units.",
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
    print(f"1791 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
