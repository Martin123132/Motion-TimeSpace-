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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1803"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1803_0_1802_doc",
        "source_key": "1802_handoff",
        "source_path": ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
        "needles": ["DEC1802_2_best_next", "NEXT1802_0_primary"],
        "role": "selects no-shadow/constant/marker or qbar coefficient pack as 1803 target",
    },
    {
        "source_id": "SRC1803_1_1802_validation",
        "source_key": "1802_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1802_VALIDATION.csv",
        "needles": ["VAL1802_OVERALL", "PASS"],
        "role": "confirms 1802 passed before 1803 starts",
    },
    {
        "source_id": "SRC1803_2_1802_components",
        "source_key": "1802_qbar_readout_components",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_QBAR_READOUT_COMPONENT_ROWS.csv",
        "needles": ["QRC1802_1_qbar_marker_constants", "QRC1802_5_total_abs_guard"],
        "role": "defines qbar marker/constants/readout component debt",
    },
    {
        "source_id": "SRC1803_3_1046_doc",
        "source_key": "1046_doc",
        "source_path": ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
        "needles": ["NSF1046_5_verdict", "DEC1046_3_best_next"],
        "role": "older no-shadow/constant/marker theorem attempt and next target",
    },
    {
        "source_id": "SRC1803_4_1046_shadow",
        "source_key": "1046_shadow_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv",
        "needles": ["NSF1046_0_define_shadow_frame", "NSF1046_5_verdict"],
        "role": "no-shadow-frame theorem shape",
    },
    {
        "source_id": "SRC1803_5_1046_constants",
        "source_key": "1046_constant_marker",
        "source_path": RESIDUALS / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
        "needles": ["CMA1046_0_alpha_EM", "CMA1046_5_verdict"],
        "role": "constant/marker split audit",
    },
    {
        "source_id": "SRC1803_6_1046_vertices",
        "source_key": "1046_forbidden_vertices",
        "source_path": RESIDUALS / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv",
        "needles": ["FV1046_0_conformal_frame", "FV1046_6_source_only_weight"],
        "role": "forbidden vertex catalog for hidden couplings",
    },
    {
        "source_id": "SRC1803_7_1046_marker_rows",
        "source_key": "1046_marker_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv",
        "needles": ["QMC1046_0_b_conf", "QMC1046_3_qbar_marker_abs"],
        "role": "nonclaim marker/frame coefficient rows",
    },
    {
        "source_id": "SRC1803_8_1046_constant_rows",
        "source_key": "1046_constant_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
        "needles": ["QCC1046_0_b_alpha", "QCC1046_3_qbar_constants_abs"],
        "role": "nonclaim constant coefficient rows",
    },
    {
        "source_id": "SRC1803_9_1740_shadow_gate",
        "source_key": "1740_shadow_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
        "needles": ["NSF1740_0_parent_matter_domain", "NSF1740_6_verdict"],
        "role": "current branch no-shadow-frame clause gate",
    },
    {
        "source_id": "SRC1803_10_1740_shadow_theorem",
        "source_key": "1740_shadow_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["NSF1740_THM0_exact_contract", "NSF1740_THM2_bound_fallback"],
        "role": "current branch no-shadow theorem and finite fallback",
    },
    {
        "source_id": "SRC1803_11_1758_constant_source",
        "source_key": "1758_constant_source",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
        "needles": ["CS1758_0_representation_data", "CS1758_6_verdict"],
        "role": "current branch constant/source universality audit",
    },
    {
        "source_id": "SRC1803_12_1761_vertex_marker",
        "source_key": "1761_vertex_marker",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv",
        "needles": ["valid_for_claim"],
        "role": "current direct-vertex/no-marker audit",
    },
    {
        "source_id": "SRC1803_13_1765_source_prefactor",
        "source_key": "1765_source_prefactor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
        "needles": ["NSP1765_0_target", "NSP1765_4_current_verdict"],
        "role": "source-only species prefactor proof attempt",
    },
    {
        "source_id": "SRC1803_14_1767_source_shadow",
        "source_key": "1767_source_shadow",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
        "needles": ["SSZ1767_0_target", "SSZ1767_4_current_verdict"],
        "role": "source-shadow zero attempt and action-normal-form classification",
    },
    {
        "source_id": "SRC1803_15_1768_shadow_classification",
        "source_key": "1768_shadow_classification",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SHADOW_TERM_CLASSIFICATION_LEDGER.csv",
        "needles": ["SCL1768_0_hilbert_matter", "SCL1768_7_verdict"],
        "role": "shadow term normal-form classification ledger",
    },
    {
        "source_id": "SRC1803_16_1768_coefficients",
        "source_key": "1768_shadow_coefficients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SHADOW_COEFFICIENT_PACK.csv",
        "needles": ["SCP1768_0_delta_w_shadow", "SCP1768_4_nonclaim_lock"],
        "role": "current branch shadow coefficient pack",
    },
    {
        "source_id": "SRC1803_17_1676_no_marker",
        "source_key": "1676_no_marker",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv",
        "needles": ["NSS1676_0_parent_constructor_list", "NSS1676_5_verdict"],
        "role": "object-language no-marker theorem attempt",
    },
    {
        "source_id": "SRC1803_18_637_constants",
        "source_key": "637_constant_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv",
        "needles": ["CO637_0_descent_criterion", "CO637_3_universal_unit_rescaling"],
        "role": "constant ownership theorem and unit-rescaling guard",
    },
    {
        "source_id": "SRC1803_19_638_constant_zero",
        "source_key": "638_constant_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv",
        "needles": ["ZR638_1_alpha_EM", "ZR638_5_measured_GM"],
        "role": "constant zero route for alpha, masses, clocks and GM guard",
    },
    {
        "source_id": "SRC1803_20_646_clock_alpha",
        "source_key": "646_clock_alpha",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock alpha sensitivities",
    },
    {
        "source_id": "SRC1803_21_1028_marker",
        "source_key": "1028_marker_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv",
        "needles": ["NM1028_0_parent_q_kernel", "NM1028_6_verdict"],
        "role": "no-marker theorem audit and remaining frame/constant blockers",
    },
    {
        "source_id": "SRC1803_22_1028_bound_pack",
        "source_key": "1028_bound_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv",
        "needles": ["FMB1028_0_cg", "FMB1028_11_claim_gate"],
        "role": "frame/marker bound input schema",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_SOURCE_REGISTER.csv",
    "shadow_constant_theorem_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_SHADOW_CONSTANT_THEOREM_GATE.csv",
    "forbidden_vertex_catalog": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_FORBIDDEN_VERTEX_CATALOG.csv",
    "qbar_coefficient_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_QBAR_COEFFICIENT_PACK.csv",
    "arena_projection_interface": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_ARENA_PROJECTION_INTERFACE.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1803_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1803_VALIDATION.csv",
}

DOC_PATH = ROOT / "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md"


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


def shadow_constant_theorem_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_0_define_shadow",
            "claim_piece": "shadow/frame/marker coupling definition",
            "required_statement": "any A(X)e_obs, disformal slot, alpha_EM(X), m_A(X), material marker, source-only w_A, or post-readout source map is classified as a residual unless parent-forbidden",
            "current_status": "DEFINITION_AND_CLASSIFICATION_READY",
            "missing_input": "none_at_definition_level",
            "source_paths": src("1046_shadow_theorem", "1046_forbidden_vertices", "1768_shadow_classification"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_1_chain_rule_zero",
            "claim_piece": "quotient-owned frame/constant derivative",
            "required_statement": "if F(Phi)=Fbar(q(Phi)) and Dq[v_X]=0, then Lie_v F=0 for frame, constant, marker, and source functions",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_input": "MISSING_PARENT_Q_DQ;MISSING_FACTORISATION_FOR_EACH_FUNCTION",
            "source_paths": src("1046_shadow_theorem", "637_constant_theorem", "1028_marker_audit"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_2_no_extra_frame_slot",
            "claim_piece": "no hidden Weyl/disformal frame",
            "required_statement": "ordinary matter/readout action admits no A_A(X)e_obs, D_A(X), source-only metric, endpoint frame, or post-readout detector frame",
            "current_status": "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED",
            "missing_input": "MISSING_PARENT_NO_EXTRA_FRAME_ACTION_CLAUSE;MISSING_OBSERVABLE_COMPLETENESS",
            "source_paths": src("1740_shadow_gate", "1740_shadow_theorem", "1046_shadow_theorem"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_3_constants",
            "claim_piece": "alpha/mass/clock constant superselection",
            "required_statement": "alpha_EM, mass ratios, charge/Yukawa/binding data, and clock transition ratios are quotient-owned or fixed representation data",
            "current_status": "CONSTANT_SUPERSELECTION_NOT_PARENT_SIGNED",
            "missing_input": "MISSING_ALPHA_EM_OWNER;MISSING_MASS_RATIO_OWNER;MISSING_CLOCK_PROJECTION_FROM_MTS_STATE",
            "source_paths": src("1758_constant_source", "637_constant_theorem", "638_constant_zero", "646_clock_alpha"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_4_markers",
            "claim_piece": "no material/source/preparation marker",
            "required_statement": "no smooth material, isotope/preparation, hidden coefficient, or readout label can alter ordinary source strength except as explicit residual",
            "current_status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "missing_input": "MISSING_PARENT_CONSTRUCTOR_LIST;MISSING_NO_SOURCE_ONLY_SPECIES_SLOT;MISSING_MARKER_COEFFICIENTS",
            "source_paths": src("1676_no_marker", "1028_marker_audit", "1761_vertex_marker"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_5_source_prefactor",
            "claim_piece": "no source-only prefactor/shadow source",
            "required_statement": "no w_A or kappa_A multiplies the active gravitational source independently of the ordinary matter action, except one common calibration",
            "current_status": "SOURCE_PREFactor_THEOREM_PARTIAL_PARENT_UNSIGNED",
            "missing_input": "MISSING_NO_HOM_SOURCE_SLOT;MISSING_CONNECTED_MATTER_GRAPH;MISSING_SOURCE_MAP_IDENTITY",
            "source_paths": src("1765_source_prefactor", "1767_source_shadow", "1768_shadow_coefficients"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_6_action_normal_form",
            "claim_piece": "shadow terms classified by parent normal form",
            "required_statement": "every hidden source term is owned as Hilbert matter, LHS geometry, nonminimal coupling, boundary/improvement, non-Hilbert current, projector, or decoupled block",
            "current_status": "CLASSIFICATION_READY_NORMAL_FORM_UNSIGNED",
            "missing_input": "MISSING_NORMAL_FORM_DECISION_FOR_NONMINIMAL_BOUNDARY_NONHILBERT_PROJECTOR_DECOUPLED_BLOCKS",
            "source_paths": src("1768_shadow_classification", "1768_shadow_coefficients"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SCT1803_7_verdict",
            "claim_piece": "current no-shadow/constant/marker theorem",
            "required_statement": "all frame, constant, marker, and source-shadow channels vanish by one parent action signature or become finite source-backed rows",
            "current_status": "NO_SHADOW_CONSTANT_MARKER_ZERO_NOT_PROVED_COEFFICIENT_PACK_REQUIRED",
            "missing_input": "MISSING_PARENT_NO_SHADOW_CONSTANT_MARKER_SOURCE_SIGNATURE",
            "source_paths": src("1802_qbar_readout_components", "1046_doc", "1768_shadow_classification"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def forbidden_vertex_catalog_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_0_conformal_frame",
            "forbidden_vertex": "S_A[Psi_A, exp(2 b_conf Xhat) g_obs]",
            "coefficient": "b_conf",
            "retention_reason": "universal conformal coupling can be WEP quiet but still source R10, clocks and source-normalization pressure",
            "zero_condition": "parent no-extra-frame theorem or b_conf=0 from quotient factorisation",
            "fallback_row": "QCP1803_0_b_conf",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_1_disformal_frame",
            "forbidden_vertex": "S_A[Psi_A, g_obs + b_dis Xhat U_mu U_nu + ...]",
            "coefficient": "b_dis",
            "retention_reason": "disformal slots feed PPN, preferred-frame, clocks and orbital/source rows",
            "zero_condition": "parent no-disformal-frame theorem or source-backed b_dis row",
            "fallback_row": "QCP1803_1_b_dis",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_2_alpha_EM",
            "forbidden_vertex": "alpha_EM(Xhat)F_munu F^munu or gauge kinetic f(Xhat)F^2",
            "coefficient": "b_alpha",
            "retention_reason": "dimensionless alpha cannot be unit-rescaled away and is directly clock/EM/composition observable",
            "zero_condition": "quotient-owned gauge coupling/topological representation theorem",
            "fallback_row": "QCP1803_2_b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_3_mass_ratio",
            "forbidden_vertex": "m_A(Xhat), y_A(Xhat), binding/nuclear ratio Xhat dependence",
            "coefficient": "b_mA",
            "retention_reason": "mass ratios and composition binding fractions feed WEP, clocks, source charge and R10",
            "zero_condition": "fixed representation/mass spectrum theorem",
            "fallback_row": "QCP1803_3_b_mA",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_4_clock_transition",
            "forbidden_vertex": "nu_i(Xhat), Rydberg/hyperfine/nuclear clock ratio dependence",
            "coefficient": "b_clock_i",
            "retention_reason": "clock ratios are dimensionless and inherit alpha/mass/nuclear sensitivity",
            "zero_condition": "alpha/mass/nuclear constant theorem plus tau_clock map",
            "fallback_row": "QCP1803_4_b_clock_i",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_5_material_marker",
            "forbidden_vertex": "material_marker_A(Xhat), isotope/preparation/source labels, or hidden post-readout marker",
            "coefficient": "b_marker",
            "retention_reason": "marker maps can preserve covariance while producing composition/source charge",
            "zero_condition": "no-marker object-language theorem",
            "fallback_row": "QCP1803_5_b_marker",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_6_source_prefactor",
            "forbidden_vertex": "S_source=sum_A kappa_A J_A or S_matter=sum_A w_A S_A with relative w_A",
            "coefficient": "delta_w_shadow",
            "retention_reason": "relative source-only weights can leave matter equations ordinary while changing gravitational source",
            "zero_condition": "no source-only slot theorem plus connected matter graph/source-map identity",
            "fallback_row": "QCP1803_6_delta_w_shadow",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "FVC1803_7_nonminimal_shadow",
            "forbidden_vertex": "DeltaS=c_nonminimal f(X,Phi,labels)L_m or post-Hilbert source-shadow projector",
            "coefficient": "c_nonminimal;C_R;delta_w_shadow",
            "retention_reason": "normal-form classification says nonminimal/projector terms must be owned or bounded, not hidden",
            "zero_condition": "parent action normal-form exhaustiveness plus identity source map",
            "fallback_row": "QCP1803_7_c_nonminimal",
            "valid_for_claim": False,
        },
    ]


def qbar_coefficient_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_0_b_conf",
            "symbol": "b_conf",
            "definition": "vertical derivative of hidden conformal matter/source frame",
            "formula_or_bound": "|qbar_marker| contains |tau_frame b_conf| plus source/test sensitivities",
            "required_inputs": "Xhat normalization; b_conf theorem-zero or numeric value; tau_R10/tau_clock/tau_PPN; source paths",
            "current_value": "MISSING_B_CONF_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "R10;WEP;clock;PPN;source_normalization",
            "source_paths": src("1046_marker_rows", "1028_bound_pack", "1740_shadow_gate"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_1_b_dis",
            "symbol": "b_dis",
            "definition": "vertical derivative of disformal/profile-normalized matter frame slot",
            "formula_or_bound": "|qbar_marker| contains |tau_dis b_dis| plus preferred-frame/orbital projections",
            "required_inputs": "disformal profile; normalization; b_dis theorem-zero or numeric value; arena projections",
            "current_value": "MISSING_B_DIS_OR_THEOREM_ZERO",
            "units": "model_dependent_declared",
            "observable_links": "PPN;preferred_frame;clock;orbital;R10",
            "source_paths": src("1046_marker_rows", "1028_bound_pack", "1740_shadow_gate"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_2_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative d ln alpha_EM/dXhat or EM/gauge kinetic marker",
            "formula_or_bound": "clock pair response d ln R_ab=DeltaK_alpha_ab b_alpha dXhat plus WEP/EM binding sensitivity terms",
            "required_inputs": "b_alpha theorem-zero or numeric source; Xhat normalization; clock/WEP sensitivities; source paths",
            "current_value": "MISSING_B_ALPHA_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "clock;EM_spectra;WEP;R10",
            "source_paths": src("1046_constant_rows", "638_constant_zero", "646_clock_alpha"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_3_b_mA",
            "symbol": "b_mA",
            "definition": "vertical derivative of particle masses, mass ratios, Yukawa/binding constants, or nuclear response",
            "formula_or_bound": "|qbar_constants| contains sum_A |s_mA b_mA| over material/clock/source sensitivities",
            "required_inputs": "mass-ratio owner theorem or b_mA values; material sensitivities; source paths",
            "current_value": "MISSING_B_MASS_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "WEP;composition;clock;source_charge;R10",
            "source_paths": src("1046_constant_rows", "638_constant_zero", "1758_constant_source"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_4_b_clock_i",
            "symbol": "b_clock_i",
            "definition": "vertical derivative of clock transition after alpha/mass/nuclear sensitivities are projected",
            "formula_or_bound": "b_clock_i=K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...",
            "required_inputs": "clock sensitivity matrix; b_alpha/b_mu/b_nuc; local dXhat projection; tau_clock",
            "current_value": "MISSING_CLOCK_CONSTANT_PROJECTION",
            "units": "dimensionless",
            "observable_links": "R2_clock_redshift;alpha_drift;clock_comparison",
            "source_paths": src("1046_constant_rows", "646_clock_alpha", "638_constant_zero"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_5_b_marker",
            "symbol": "b_marker",
            "definition": "vertical derivative of material/source/preparation marker",
            "formula_or_bound": "|qbar_marker| contains sum_A |s_A b_marker,A|",
            "required_inputs": "marker taxonomy; material pair; sensitivities; theorem-zero or coefficient values; source paths",
            "current_value": "MISSING_MARKER_COEFFICIENTS",
            "units": "dimensionless_after_sensitivity_normalization",
            "observable_links": "WEP_source_charge;composition;clock;R10",
            "source_paths": src("1046_marker_rows", "1676_no_marker", "1028_marker_audit"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_6_delta_w_shadow",
            "symbol": "delta_w_shadow",
            "definition": "relative source-only weight or post-Hilbert source-shadow/projector leakage",
            "formula_or_bound": "|qbar_source_weight| <= |delta_w_shadow| + disconnected_block_tail + projector/source-map tails",
            "required_inputs": "source-map identity theorem or source-backed delta_w rows; connected matter graph; arena projection",
            "current_value": "MISSING_DELTA_W_SHADOW_ZERO_OR_BOUND",
            "units": "dimensionless_or_arena_normalized",
            "observable_links": "WEP;Newton_GM;R10;PPN;local_GR",
            "source_paths": src("1765_source_prefactor", "1767_source_shadow", "1768_shadow_coefficients"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_7_c_nonminimal",
            "symbol": "c_nonminimal",
            "definition": "direct matter-MTS/geometric nonminimal source term coefficient",
            "formula_or_bound": "|DeltaJ_nonminimal| <= |c_nonminimal| ||f(X,Phi,labels)L_m|| projected by arena",
            "required_inputs": "operator basis; dimensions; source path; arena projection; zero theorem or numeric coefficient",
            "current_value": "MISSING_OPERATOR_BASIS_AND_BOUND",
            "units": "operator_dependent",
            "observable_links": "R10;WEP;PPN;clock;local_GR",
            "source_paths": src("1768_shadow_classification", "1768_shadow_coefficients"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCP1803_8_total_abs_guard",
            "symbol": "qbar_hidden_abs_envelope",
            "definition": "no-cancellation envelope over frame, constants, markers, source weights and nonminimal shadows",
            "formula_or_bound": "|qbar_hidden| <= |b_conf|+|tau_dis b_dis|+|s_alpha b_alpha|+sum|s_mA b_mA|+sum|s_marker b_marker|+|delta_w_shadow|+|c_nonminimal|",
            "required_inputs": "all coefficients theorem-zero or numeric/source-backed in one normalization; no MISSING markers",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_or_declared_profile_units",
            "observable_links": "all_local_arenas",
            "source_paths": src("1802_qbar_readout_components", "1046_marker_rows", "1046_constant_rows", "1768_shadow_coefficients"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_projection_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "API1803_0_R10",
            "arena": "R10 short-range force",
            "active_coefficients": "b_conf;b_dis;b_marker;b_alpha;b_mA;delta_w_shadow;c_nonminimal",
            "projection_rule": "alpha_X(lambda) needs K_X,Qbar_XH,qbar_hidden_abs,tau_R10,lambda_X and promoted alpha_bound(lambda)",
            "current_status": "NOT_SCOREABLE_COEFFICIENTS_AND_BOUND_CURVE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "API1803_1_WEP",
            "arena": "WEP/source charge",
            "active_coefficients": "b_marker;b_mA;b_alpha;delta_w_shadow",
            "projection_rule": "eta_AB needs material-pair sensitivities and source/test qbar coefficients in the same frame",
            "current_status": "NOT_SCOREABLE_MATERIAL_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "interface_id": "API1803_2_clock_EM",
            "arena": "clocks/EM/fine-structure",
            "active_coefficients": "b_alpha;b_mA;b_clock_i;b_conf;b_dis",
            "projection_rule": "d ln R_ab=DeltaK_alpha b_alpha dXhat plus mass/nuclear terms; requires tau_clock/local dXhat map",
            "current_status": "SENSITIVITIES_EXIST_MTS_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "API1803_3_PPN_orbital",
            "arena": "PPN/orbital/source normalization",
            "active_coefficients": "b_conf;b_dis;delta_w_shadow;c_nonminimal;boundary/support tails",
            "projection_rule": "PPN/Newton needs Pi_M source map, tau_PPN, orbital support and residual vector before scoring",
            "current_status": "NOT_SCOREABLE_SOURCE_MAP_AND_TAU_PPN_MISSING",
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1803_0_no_shadow_zero",
            "gate": "no-shadow/no-marker/constant theorem-zero",
            "current_status": "FAIL_PARENT_SIGNATURE_UNSIGNED",
            "reason": "chain-rule theorem is exact but parent no-extra-frame, constant superselection, no-marker and source-map signatures are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1803_1_coefficient_pack",
            "gate": "finite hidden-coupling coefficient envelope",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "reason": "qbar coefficient rows are explicit but contain MISSING theorem-zero/numeric inputs",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1803_2_no_cancellation",
            "gate": "no cancellation between hidden coupling channels",
            "current_status": "POLICY_ACTIVE_NOT_SCORE",
            "reason": "all hidden coefficients must be zero/bounded absolutely; opposite-sign frame/constant/source cancellation gets no credit",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1803_3_verdict",
            "gate": "hidden coupling closure readiness",
            "current_status": "HIDDEN_COUPLINGS_NOT_ZERO_AND_NOT_BOUNDED",
            "reason": "no claim-ready theorem-zero route and no source-backed coefficient values exist",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1803_0_universal_conformal",
            "countermodel": "universal A(X)^2 g_obs coupling is WEP quiet but nonzero in R10/source normalization",
            "survives_current_constraints": True,
            "why_survives": "no-extra-frame parent action clause is unsigned",
            "what_kills_it": "parent no-shadow theorem or source-backed b_conf bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1803_1_dimensionless_alpha",
            "countermodel": "alpha_EM(X) varies while metric/coframe descent looks clean",
            "survives_current_constraints": True,
            "why_survives": "alpha_EM is dimensionless and constant superselection is not parent-derived",
            "what_kills_it": "quotient-owned gauge coupling theorem or b_alpha coefficient provenance",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1803_2_mass_marker",
            "countermodel": "mass ratios/material markers carry X sensitivity into WEP and clock channels",
            "survives_current_constraints": True,
            "why_survives": "fixed representation/no-marker theorem is not parent-signed",
            "what_kills_it": "mass/marker superselection theorem or source-backed b_mA/b_marker rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1803_3_source_prefactor",
            "countermodel": "relative source-only weights alter active gravitational source without altering ordinary equations",
            "survives_current_constraints": True,
            "why_survives": "no-Hom source slot and connected matter graph are not parent-signed",
            "what_kills_it": "source-map identity theorem or finite delta_w_shadow bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1803_4_nonminimal_shadow",
            "countermodel": "nonminimal matter-MTS source term or post-Hilbert projector is a real hidden source",
            "survives_current_constraints": True,
            "why_survives": "parent action normal-form classification is incomplete",
            "what_kills_it": "normal-form exhaustiveness or finite c_nonminimal/projector coefficient rows",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1803_0_no_shadow",
            "claim": "hidden Weyl/disformal frame is theorem-zero",
            "status": "BLOCKED",
            "reason": "SCT1803_2 is not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1803_1_constants",
            "claim": "alpha/mass/clock constants are vertical-silent",
            "status": "BLOCKED",
            "reason": "SCT1803_3 constant superselection is unsigned and MTS clock projection is missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1803_2_markers_source",
            "claim": "material markers and source-only prefactors are absent",
            "status": "BLOCKED",
            "reason": "no-marker/no-source-prefactor theorems are conditional and parent unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1803_3_coefficients",
            "claim": "hidden qbar coefficient envelope is scoreable",
            "status": "BLOCKED",
            "reason": "QCP1803 rows contain missing theorem-zero or numeric coefficient inputs",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1803_4_local_GR_Newton",
            "claim": "hidden-coupling closure supports local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "hidden coupling source terms remain neither zero nor bounded, and source normalization remains open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1803_0_theorem_shape",
            "decision": "NO_SHADOW_CHAIN_RULE_EXACT_CONDITIONAL",
            "reason": "factor-through-q plus Dq[v_X]=0 would kill frame/constant/marker derivatives",
            "next_action": "do not claim until parent no-extra-frame, constants and no-marker clauses are signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1803_1_current_status",
            "decision": "HIDDEN_COUPLINGS_RETAINED",
            "reason": "universal conformal/disformal frame, alpha/mass/clock constants, markers, source prefactors and nonminimal shadows remain legal countermodels",
            "next_action": "retain the absolute qbar coefficient envelope",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1803_2_best_next",
            "decision": "CONSTANT_SUPERSELECTION_ALPHA_MASS_CLOCK_PROVENANCE_NEXT",
            "reason": "alpha_EM and mass/clock ratios are dimensionless or sensitivity-projected, so they are the hardest to hide by units and the easiest to test later",
            "next_action": "build 1804 to prove constant superselection or source b_alpha/b_mA/b_clock_i provenance rows",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1803_0_primary",
            "next_target": "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md",
            "script": "scripts/Y5_R2FR_constant_superselection_alpha_mass_clock_provenance.py",
            "objective": "try to prove alpha_EM, mass ratios and clock transition constants are quotient-owned/superselected and vertically silent; if not, emit source-ready b_alpha, b_mA and b_clock_i provenance rows",
            "selection_status": "selected",
            "success_condition": "constant-sector theorem-zero or source-backed alpha/mass/clock coefficient rows with units and projection requirements",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1803_1_parallel_source_prefactor",
            "next_target": "1804b-Y5-R2FR-source-prefactor-identity-or-deltaw-shadow-bound.md",
            "script": "scripts/Y5_R2FR_source_prefactor_identity_or_deltaw_shadow_bound.py",
            "objective": "prove no source-only prefactor/source-shadow route or emit finite delta_w_shadow rows",
            "selection_status": "held_parallel",
            "success_condition": "source-map identity theorem or source-backed delta_w_shadow coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1803_2_parallel_frame",
            "next_target": "1804c-Y5-R2FR-Weyl-disformal-frame-zero-or-bg-bdis-bound.md",
            "script": "scripts/Y5_R2FR_Weyl_disformal_frame_zero_or_bg_bdis_bound.py",
            "objective": "prove no Weyl/disformal matter/source frame or emit b_conf/b_dis rows with arena projections",
            "selection_status": "held_parallel",
            "success_condition": "no-shadow frame theorem or source-backed b_conf/b_dis coefficient rows",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "shadow_constant_theorem_gate": shadow_constant_theorem_gate_rows(),
        "forbidden_vertex_catalog": forbidden_vertex_catalog_rows(),
        "qbar_coefficient_pack": qbar_coefficient_pack_rows(),
        "arena_projection_interface": arena_projection_interface_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1803_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1803_{key.upper()}.csv").exists():
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
        ("VAL1803_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1803_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1803_2_theorem_not_promoted",
            any(
                row["gate_id"] == "SCT1803_7_verdict"
                and row["current_status"] == "NO_SHADOW_CONSTANT_MARKER_ZERO_NOT_PROVED_COEFFICIENT_PACK_REQUIRED"
                and not boolish(row["theorem_zero"])
                for row in rows_map["shadow_constant_theorem_gate"]
            ),
            "no-shadow/constant/marker theorem remains unpromoted",
        ),
        (
            "VAL1803_3_vertices_catalogued",
            len(rows_map["forbidden_vertex_catalog"]) >= 8
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["forbidden_vertex_catalog"]),
            "forbidden vertex catalog covers hidden frame/constant/marker/source routes",
        ),
        (
            "VAL1803_4_coefficient_pack_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in rows_map["qbar_coefficient_pack"])
            and any("MISSING" in row["current_value"] for row in rows_map["qbar_coefficient_pack"]),
            "qbar coefficient pack is nonclaim and value-missing",
        ),
        (
            "VAL1803_5_arena_interfaces_blocked",
            all(not boolish(row["valid_for_claim"]) and ("MISSING" in row["current_status"] or "NOT_SCOREABLE" in row["current_status"] or "SENSITIVITIES_EXIST" in row["current_status"]) for row in rows_map["arena_projection_interface"]),
            "arena interfaces remain blocked",
        ),
        (
            "VAL1803_6_acceptance_blocks",
            any(
                row["gate_id"] == "AC1803_3_verdict"
                and row["current_status"] == "HIDDEN_COUPLINGS_NOT_ZERO_AND_NOT_BOUNDED"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks hidden coupling closure",
        ),
        (
            "VAL1803_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1803_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1803_9_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1803_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1803_11_decision_next",
            any(
                row["decision_id"] == "DEC1803_2_best_next"
                and row["decision"] == "CONSTANT_SUPERSELECTION_ALPHA_MASS_CLOCK_PROVENANCE_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects constant superselection/alpha/mass/clock provenance next",
        ),
        (
            "VAL1803_12_next_selected",
            any(row["route_id"] == "NEXT1803_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1803_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1803 CSVs parse"),
        ("VAL1803_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1803_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1803_16_formalization_untouched", formalization_untouched(), "no 1803 outputs found under formalization-workbench"),
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
            "check_id": "VAL1803_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1803 no-shadow constant marker or qbar coefficient pack checkpoint",
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
            "# 1803 - Y5/R2FR No-Shadow, Constant Marker, or qbar Coefficient Pack",
            "",
            "## Verdict",
            "",
            "1803 sharpens the hidden-coupling problem. The no-shadow theorem is exact only as a conditional chain-rule statement: if every frame, constant, marker, and source function factors through `q` and `v_X in ker(Dq)`, its vertical derivative vanishes.",
            "",
            "That is not yet a parent-signed theorem. Universal Weyl/disformal frames, `alpha_EM(X)`, mass-ratio or clock dependence, material markers, source-only prefactors, and nonminimal shadow terms remain live unless the parent action forbids them.",
            "",
            "So this checkpoint does not claim `qbar_marker=0` or `qbar_constants=0`. It turns the loopholes into named coefficient rows with a no-cancellation absolute envelope.",
            "",
            "**Claim ceiling:** no no-shadow theorem, no constant superselection theorem, no marker/source-prefactor zero theorem, no scoreable qbar coefficient row, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1803.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Shadow/Constant Theorem Gate",
            markdown_table(rows_map["shadow_constant_theorem_gate"], ["gate_id", "claim_piece", "required_statement", "current_status", "missing_input", "theorem_zero", "valid_for_claim"]),
            "",
            "## Forbidden Vertex Catalog",
            markdown_table(rows_map["forbidden_vertex_catalog"], ["vertex_id", "forbidden_vertex", "coefficient", "retention_reason", "zero_condition", "fallback_row", "valid_for_claim"]),
            "",
            "## qbar Coefficient Pack",
            markdown_table(rows_map["qbar_coefficient_pack"], ["row_id", "symbol", "definition", "formula_or_bound", "current_value", "observable_links", "valid_for_claim"]),
            "",
            "## Arena Projection Interface",
            markdown_table(rows_map["arena_projection_interface"], ["interface_id", "arena", "active_coefficients", "projection_rule", "current_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This is not grim; it is a tightening. The theory is no longer allowed to wave at 'matter coupling' as a blob. Every hidden coupling must now either factor through the quotient, be parent-forbidden by action grammar, or become a coefficient with arena-specific projections. The next most testable subproblem is the dimensionless constant sector: `alpha_EM`, mass ratios, and clock transitions.",
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
    print(f"1803 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
