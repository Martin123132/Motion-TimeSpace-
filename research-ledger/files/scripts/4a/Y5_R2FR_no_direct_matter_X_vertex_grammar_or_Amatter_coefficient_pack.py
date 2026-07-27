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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1761"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1761_0_1760_handoff",
        "source_key": "1760_no_direct_vertex_next",
        "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
        "needles": ["NEXT1760_0_primary", "V_m[X,rho_A,W_source]"],
    },
    {
        "source_id": "SRC1761_1_1488_doc",
        "source_key": "1488_wA_handoff_doc",
        "source_path": ROOT / "1488-Y5-R10-RAB-ordinary-matter-subaction-current-chain-owner-or-explicit-wA-residual-lock.md",
        "needles": ["NEXT1488_0_1489", "w_A"],
    },
    {
        "source_id": "SRC1761_2_1488_hom",
        "source_key": "1488_no_source_only_hom_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_NO_SOURCE_ONLY_HOM_GATE.csv",
        "needles": ["HOMG1488_0_target", "HOMG1488_5_verdict"],
    },
    {
        "source_id": "SRC1761_3_1488_wA",
        "source_key": "1488_wA_deltaW_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_1_component_vector", "NONCLAIM_LOCK"],
    },
    {
        "source_id": "SRC1761_4_1488_current",
        "source_key": "1488_current_chain_countermodel",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
        "needles": ["OMSCC1488_3_prefactor_countermodel", "w_A"],
    },
    {
        "source_id": "SRC1761_5_1720_functor",
        "source_key": "1720_source_prefactor_countermodel",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_6_no_shadow_or_source_prefactor", "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1761_6_1720_JH",
        "source_key": "1720_hilbert_current_prefactor_countermodel",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
        "needles": ["JHT1720_3_source_prefactor_countermodel", "COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1761_7_954_parent_clause",
        "source_key": "954_parent_no_prefactor_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"],
    },
    {
        "source_id": "SRC1761_8_954_label_forgetting",
        "source_key": "954_label_forgetting_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
        "needles": ["PLF954_2_prefactor_obstruction", "PLF954_5_verdict"],
    },
    {
        "source_id": "SRC1761_9_953_source_functor",
        "source_key": "953_source_functor_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NSF953_2_conditional_uniqueness", "NSF953_5_verdict"],
    },
    {
        "source_id": "SRC1761_10_955_minimal",
        "source_key": "955_minimal_matter_action_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    },
    {
        "source_id": "SRC1761_11_955_classification",
        "source_key": "955_source_prefactor_classification",
        "source_path": RESIDUALS / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "needles": ["SPC955_2_relative_species_weight", "SPC955_3_hidden_marker_weight"],
    },
    {
        "source_id": "SRC1761_12_736_no_marker",
        "source_key": "736_no_marker_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
        "needles": ["NMC736_3_shadow_frame_forbidden", "NMC736_5_limit"],
    },
    {
        "source_id": "SRC1761_13_767_reaudit",
        "source_key": "767_no_alpha_mass_vertex_reaudit",
        "source_path": RESIDUALS / "P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
        "needles": ["PMR767_3_no_alpha_mass_vertex", "hard_blocker_still_unsigned"],
    },
    {
        "source_id": "SRC1761_14_977_constants",
        "source_key": "977_no_constant_vertices",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_2_no_constant_vertices", "CONTRACT_CLEAR_NOT_PARENT_DERIVED"],
    },
    {
        "source_id": "SRC1761_15_1758_invariant_debt",
        "source_key": "1758_invariant_generator_debt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_INVARIANT_ALGEBRA_AUDIT.csv",
        "needles": ["IA1758_5_species_constants", "MISSING_CONSTANT_SOURCE_UNIVERSALITY"],
    },
    {
        "source_id": "SRC1761_16_1758_minimality",
        "source_key": "1758_material_marker_extension",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
        "needles": ["PM1758_2_material_marker_no_extension", "NOT_DERIVED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_SOURCE_REGISTER.csv",
    "grammar_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
    "prefactor_classification": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "hom_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NO_SOURCE_ONLY_HOM_AUDIT.csv",
    "direct_vertex_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv",
    "coefficient_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_AMATTER_COEFFICIENT_PACK.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1761_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "no direct matter X vertex grammar or A_matter coefficient pack",
                "valid_for_claim": False,
            }
        )
    return rows


def grammar_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NDV1761_0_target",
            "claim_piece": "no direct matter X vertex",
            "mathematical_form": "Allowed[S_ord] excludes V_m[X,rho_A,W_source], w_A(X,m,D,W), hidden frames g_A(X), and post-readout source masks outside q",
            "status": "TARGET_EXACT",
            "proof_status": "ZERO_IF_PARENT_GRAMMAR_SIGNED",
            "gap": "absence of a slot is a parent object-language theorem, not a consequence of covariance or Ward identities alone",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NDV1761_1_allowed_syntax",
            "claim_piece": "minimal ordinary matter syntax",
            "mathematical_form": "S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A] with one common action measure and no active-source prefactor argument",
            "status": "EXACT_CONDITIONAL_SCHEMA",
            "proof_status": "IF_SIGNED_THEN_A_DIRECT_MATTER_ZERO",
            "gap": "955 gives the lemma shape, but the current parent action does not derive the syntax",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NDV1761_2_common_mode",
            "claim_piece": "common source prefactor",
            "mathematical_form": "S_ord -> w_* S_ord and kappa_univ w_* -> kappa_measured",
            "status": "CALIBRATION_NUISANCE_ONLY",
            "proof_status": "NOT_A_WEP_OR_LOCAL_FORCE_RESIDUAL_BY_ITSELF",
            "gap": "does not remove relative or hidden-marker source weights",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NDV1761_3_relative_countermodel",
            "claim_piece": "relative source prefactor survives",
            "mathematical_form": "S_ord=sum_A w_A S_A gives T_source=sum_A w_A T_A while ordinary equations can still look acceptable",
            "status": "COUNTERMODEL_SURVIVES",
            "proof_status": "NO_SOURCE_ONLY_HOM_NOT_DERIVED",
            "gap": "relative w_A is not killed by covariance, additivity, Ward identities, or a common measured-G calibration",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NDV1761_4_current_verdict",
            "claim_piece": "current MTS no-direct-vertex theorem",
            "mathematical_form": "partial_X V_m|0=0 and delta_w_A=0 for ordinary matter/source sectors",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_status": "A_DIRECT_AND_DELTA_W_RETAINED",
            "gap": "HOM exclusion, no-marker minimality, no hidden frame, no alpha/mass vertex, and readout/worldtube silence remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def prefactor_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_0_absent_slot",
            "prefactor_type": "absent parent slot",
            "mathematical_form": "partial S_ord / partial w_A is undefined because w_A is not an argument",
            "status": "DESIRED_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "effect_on_source": "T_source=T_total once other Hilbert/current clauses close",
            "action": "derive from parent object language or keep nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_1_common_mode",
            "prefactor_type": "common universal prefactor",
            "mathematical_form": "w_A=w_* for every ordinary species",
            "status": "CALIBRATION_MODE",
            "effect_on_source": "absorbed into kappa/G calibration, not a relative WEP/source residual by itself",
            "action": "track separately from relative delta_w_A",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_2_relative_species",
            "prefactor_type": "relative species/source weight",
            "mathematical_form": "w_A=w_*(1+epsilon_A), epsilon_A != epsilon_B",
            "status": "LIVE_COUNTERMODEL",
            "effect_on_source": "composition/source-normalization residual",
            "action": "parent-forbid or source beta/delta_w bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_3_hidden_marker",
            "prefactor_type": "hidden invariant/material/domain marker",
            "mathematical_form": "w_A=w(I_hid,m,D,boundary,A)",
            "status": "LIVE_COUNTERMODEL",
            "effect_on_source": "source charge reopens under marker/domain/readout labels",
            "action": "requires primitive minimality and invariant-algebra triviality or explicit A_marker/A_direct rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_4_hidden_frame",
            "prefactor_type": "universal or species hidden conformal/disformal frame",
            "mathematical_form": "g_A = A_A(X)^2 g_obs + disformal terms",
            "status": "LIVE_UNLESS_DECLARED_EXTENSION",
            "effect_on_source": "can be WEP-safe in a narrow sense but still affect clocks, PPN, R10 or source normalization",
            "action": "forbid as parent grammar or bound as c_g/disformal-like residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_5_alpha_mass_vertex",
            "prefactor_type": "direct alpha/mass/charge vertex",
            "mathematical_form": "alpha_EM(X)F^2, m_A(X), q_A X_mu J_A^mu, theta_A(I_Q,m)",
            "status": "FORBIDDEN_BY_POLICY_NOT_PARENT_THEOREM",
            "effect_on_source": "clock, WEP, fine-structure and fifth-force residuals return",
            "action": "derive no-constant-vertex theorem or keep alpha/mass coefficient rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "class_id": "SP1761_6_readout_worldtube",
            "prefactor_type": "post-readout/source-worldtube source mask",
            "mathematical_form": "w=w(W_source,Pi_M,readout,domain) selected after variation",
            "status": "LIVE_COUNTERMODEL",
            "effect_on_source": "active source can be changed without visibly changing matter equations",
            "action": "requires before-readout source/worldtube owner theorem or explicit A_worldtube coefficient",
            "valid_for_claim": False,
        },
    ]


def hom_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HOM1761_0_target",
            "hom_statement": "Hom_parent(species_label or hidden_marker or readout_selector, R_+ active-source-prefactor) is empty or common-constant only",
            "current_status": "TARGET_EXACT",
            "why_needed": "this is the exact grammar theorem that would remove source-only w_A and direct V_m slots",
            "blocker": "MISSING_PARENT_OBJECT_LANGUAGE_EXCLUSION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HOM1761_1_species",
            "hom_statement": "Hom(species label, R_+ active-source-prefactor)=common constants only",
            "current_status": "NOT_DERIVED",
            "why_needed": "removes relative species source weights",
            "blocker": "MISSING_LABEL_FORGETTING_PARENT_CATEGORY_THEOREM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HOM1761_2_hidden_invariant",
            "hom_statement": "Hom(I_hid or invariant generator, R_+ source coefficient)=empty",
            "current_status": "NOT_DERIVED",
            "why_needed": "removes hidden marker/domain/source coefficients",
            "blocker": "MISSING_INVARIANT_ALGEBRA_TRIVIALITY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HOM1761_3_readout_worldtube",
            "hom_statement": "Hom(readout/worldtube/domain selector, R_+ source weight)=empty before variation",
            "current_status": "NOT_DERIVED",
            "why_needed": "prevents post-readout source masks and fitted active-source weights",
            "blocker": "MISSING_BEFORE_READOUT_WORLDTUBE_SOURCE_OWNER",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HOM1761_4_verdict",
            "hom_statement": "no-source-only Hom exclusion is signed for current MTS",
            "current_status": "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED",
            "why_needed": "would set delta_w_A=0 and remove A_direct_matter's prefactor branch",
            "blocker": "retain delta_w and A_direct coefficient pack",
            "valid_for_claim": False,
        },
    ]


def direct_vertex_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_0_Vm",
            "vertex": "V_m[X,rho_A,W_source]",
            "forbidden_if": "matter functor has only q-owned observed geometry, fixed constants, and parent-owned Hilbert worldtube support",
            "current_status": "CONTRACT_ONLY",
            "residual_if_open": "A_direct_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_1_wA",
            "vertex": "source-only species/action prefactor w_A",
            "forbidden_if": "no-source-only Hom exclusion and single matter density line are parent-signed",
            "current_status": "COUNTERMODEL_SURVIVES",
            "residual_if_open": "delta_w_A",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_2_marker",
            "vertex": "theta_A(m), kappa_A(m), material/domain marker",
            "forbidden_if": "primitive minimality forbids co-moving marker quotient extensions and invariant algebra has no marker generators",
            "current_status": "NOT_DERIVED",
            "residual_if_open": "delta_w_marker or A_theta_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_3_shadow_frame",
            "vertex": "hidden conformal/disformal matter/source frame",
            "forbidden_if": "one observed coframe is parent-owned before matter/readout and no shadow frame map is allowed",
            "current_status": "NOT_PARENT_SIGNED",
            "residual_if_open": "A_shadow_frame or c_g-like disformal residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_4_alpha_mass",
            "vertex": "alpha_EM(X), m_A(X), q_A X_mu J_A^mu",
            "forbidden_if": "constants are representation data and no direct constant vertices are parent-derived",
            "current_status": "POLICY_ONLY",
            "residual_if_open": "A_alpha_mass or b_theta",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vertex_id": "DV1761_5_verdict",
            "vertex": "all direct matter/source vertices",
            "forbidden_if": "DV1761_0 through DV1761_4 are all signed in one parent branch",
            "current_status": "FAIL_CURRENT_CLAIM_DIRECT_VERTEX_NOT_EXCLUDED",
            "residual_if_open": "A_direct_matter remains",
            "valid_for_claim": False,
        },
    ]


def coefficient_pack_rows() -> list[dict[str, Any]]:
    source_path = str(RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv")
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_0_w_star",
            "symbol": "w_star",
            "definition": "common universal source/action prefactor",
            "status": "CALIBRATION_NUISANCE_NONCLAIM",
            "required_input": "common calibration owner if used; not a relative WEP/local-force proof",
            "feeds": "kappa/G calibration only",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_1_delta_w_A",
            "symbol": "delta_w_A",
            "definition": "finite ordinary source/action weight residual vector over source-relevant matter components",
            "status": "RETAINED_RESIDUAL_SYMBOLIC",
            "required_input": "parent Hom zero theorem or component basis with numeric/source-backed bounds",
            "feeds": "A_direct_matter, WEP/source-normalization/PPN/R10 local source channels",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_2_delta_w_species",
            "symbol": "delta_w_species",
            "definition": "species-label to active-source prefactor leakage",
            "status": "MISSING_HOM_SPECIES_EXCLUSION_OR_BOUND",
            "required_input": "label-forgetting parent category proof or source-specific beta/delta_w bound",
            "feeds": "composition and source/test residuals",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_3_delta_w_hidden",
            "symbol": "delta_w_hidden",
            "definition": "hidden invariant to source coefficient leakage",
            "status": "MISSING_INVARIANT_ALGEBRA_TRIVIALITY_OR_BOUND",
            "required_input": "hidden invariant no-Hom proof or coefficient target",
            "feeds": "hidden-source A_direct/A_marker residuals",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_4_delta_w_marker",
            "symbol": "delta_w_marker",
            "definition": "material/domain/boundary marker to source coefficient leakage",
            "status": "MISSING_NO_MARKER_EXTENSION_THEOREM_OR_BOUND",
            "required_input": "primitive minimality/no-marker proof or marker coefficient row",
            "feeds": "A_theta_matter and A_direct_matter",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_5_delta_w_readout",
            "symbol": "delta_w_readout",
            "definition": "post-variation source/readout/worldtube transfer leakage",
            "status": "MISSING_BEFORE_READOUT_OWNER_OR_BOUND",
            "required_input": "source/worldtube owner theorem or readout coefficient bound",
            "feeds": "A_worldtube_matter and source-normalization rows",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CP1761_6_A_direct_matter",
            "symbol": "A_direct_matter",
            "definition": "direct matter/source vertex component of A_matter",
            "status": "MISSING_ZERO_THEOREM_OR_COMPONENT_VALUES",
            "required_input": "||delta_v V_m||_{E*} or theorem-zero from no-direct-vertex grammar",
            "feeds": "A_matter <= ... + A_direct_matter + ...",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1760_AMATTER_BOUND_INTERFACE.csv"),
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1761_0_no_direct_vertex",
            "quantity": "partial_X V_m|0",
            "current_status": "NOT_ZEROED",
            "evidence": "no-source-only Hom exclusion and no-marker/no-shadow-frame grammar remain unsigned",
            "remaining_gap": "parent object language must forbid w_A, hidden frame, marker, alpha/mass and readout/worldtube source slots",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1761_1_delta_w",
            "quantity": "delta_w_A",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "1488/955 show relative w_A survives Ward/additivity/common-calibration arguments",
            "remaining_gap": "parent Hom theorem or source-backed component bounds",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1761_2_A_matter",
            "quantity": "A_matter",
            "current_status": "NOT_ZEROED",
            "evidence": "1761 narrows A_direct_matter but does not close it",
            "remaining_gap": "A_geom, A_theta, A_lift, A_direct, A_worldtube, A_boundary and A_nonHilbert remain missing or unsigned",
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1761_0_common_mode",
            "decision": "COMMON_SOURCE_PREFACTOR_IS_CALIBRATION_ONLY",
            "reason": "a single w_star can be absorbed into kappa/G calibration and is not the dangerous relative source charge",
            "next_action": "keep w_star separate from delta_w_A",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1761_1_relative_mode",
            "decision": "RELATIVE_SOURCE_PREFACTOR_SURVIVES",
            "reason": "Ward symmetry, covariance, additivity and common measured-G calibration do not remove w_A/w_B",
            "next_action": "do not claim local-GR matter source closure from Hilbert-current prose alone",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1761_2_no_hom",
            "decision": "NO_SOURCE_ONLY_HOM_NOT_PARENT_DERIVED",
            "reason": "the exact grammar theorem is known but current parent object language does not derive it",
            "next_action": "retain delta_w_A and A_direct_matter",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1761_3_best_next",
            "decision": "MINIMAL_PARENT_OBJECT_LANGUAGE_OR_DELTAW_BOUND_IS_NEXT",
            "reason": "the derivation route now reduces to a typed parent grammar/minimality theorem; otherwise the honest path is finite delta_w bounds",
            "next_action": "build 1762 parent object-language Hom exclusion from minimality/invariant algebra or delta_w bound runner",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1761_0_no_direct_vertex",
            "claim": "parent grammar forbids all direct matter X/source slots",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_OBJECT_LANGUAGE_HOM_EXCLUSION_MISSING",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1761_1_delta_w_zero",
            "claim": "delta_w_A=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_RELATIVE_SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1761_2_A_direct_zero",
            "claim": "A_direct_matter=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_MARKER_NO_SHADOW_NO_ALPHA_READOUT_SLOTS_UNSIGNED",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1761_3_A_matter_zero",
            "claim": "A_matter=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DIRECT_VERTEX_AND_OTHER_AMATTER_COMPONENTS_ACTIVE",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1761_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTAW_AND_AMATTER_SOURCE_ENVELOPE_NOT_ZERO_OR_SOURCED",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1761_0_primary",
            "next_target": "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
            "script": "scripts/Y5_R2FR_parent_object_language_Hom_exclusion_from_minimality_or_deltaw_bound.py",
            "objective": "try to derive the no-source-only Hom theorem from primitive minimality, invariant-algebra triviality and fixed representation data; otherwise build source-ready delta_w/A_direct bound rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1761_1_fallback",
            "next_target": "1762b-Y5-R2FR-deltaw-Amatter-bound-runner.md",
            "script": "scripts/Y5_R2FR_deltaw_Amatter_bound_runner.py",
            "objective": "turn delta_w_A, delta_w_species, delta_w_hidden, delta_w_marker and delta_w_readout into nonclaim source-envelope inputs with units and source paths",
            "selection_status": "held_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "grammar_attempt": grammar_attempt_rows(),
        "prefactor_classification": prefactor_classification_rows(),
        "hom_audit": hom_audit_rows(),
        "direct_vertex_audit": direct_vertex_audit_rows(),
        "coefficient_pack": coefficient_pack_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return bool(list(csv.DictReader(handle)))
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1761_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1761_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
    }


def boolish_true(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_true(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "row_status", "proof_status"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_true(value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1761_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1761_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1761() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1761*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def grammar_contract_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "NDV1761_1_allowed_syntax"
        and row["status"] == "EXACT_CONDITIONAL_SCHEMA"
        and row["valid_for_claim"] is False
        for row in rows_map["grammar_attempt"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "NDV1761_3_relative_countermodel"
        and row["status"] == "COUNTERMODEL_SURVIVES"
        and row["valid_for_claim"] is False
        for row in rows_map["grammar_attempt"]
    )


def deltaw_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["coefficient_pack"]
    return any(row["symbol"] == "delta_w_A" and row["valid_for_claim"] is False for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def no_direct_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "NDV1761_4_current_verdict"
        and row["proof_status"] == "A_DIRECT_AND_DELTA_W_RETAINED"
        and row["valid_for_claim"] is False
        for row in rows_map["grammar_attempt"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1761_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1761_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1761_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1761_2_grammar_contract", grammar_contract_present(rows_map), "minimal matter grammar contract recorded", "minimal grammar contract missing or promoted"),
        check_row("VAL1761_3_countermodel_retained", countermodel_retained(rows_map), "relative source-prefactor countermodel retained", "relative countermodel missing or promoted"),
        check_row("VAL1761_4_no_direct_not_promoted", no_direct_not_promoted(rows_map), "no-direct-vertex theorem remains unpromoted", "direct-vertex theorem promoted or verdict missing"),
        check_row("VAL1761_5_deltaw_nonclaim", deltaw_nonclaim(rows_map), "delta_w coefficient pack remains nonclaim", "delta_w pack missing or promoted"),
        check_row("VAL1761_6_claim_gates_safe", all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates), "all claim gates remain blocked", "one or more claim gates opened"),
        check_row("VAL1761_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1761_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1761_9_decision_next",
            any(row["decision_id"] == "DEC1761_3_best_next" and row["decision"] == "MINIMAL_PARENT_OBJECT_LANGUAGE_OR_DELTAW_BOUND_IS_NEXT" for row in rows_map["decision"]),
            "decision selects parent object-language Hom or delta_w route",
            "best-next decision missing",
        ),
        check_row("VAL1761_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1761_11_csv_parse", csv_parse_all(), "all generated 1761 CSVs parse", "one or more generated 1761 CSVs fail to parse"),
        check_row("VAL1761_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1761_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1761_14_formalization_untouched", formalization_untouched_for_1761(), "no 1761 outputs found under formalization-workbench", "1761 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1761_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1761 no direct matter X vertex grammar or A_matter coefficient pack",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1761 - No Direct Matter X Vertex Grammar Or A_matter Coefficient Pack",
        "",
        "## Verdict",
        "- 1761 attacks the sharp matter-specific leak from 1760: direct `V_m[X,rho_A,W_source]`, source-only prefactors, hidden matter frames, and marker/source weights.",
        "- The clean theorem is exact but conditional: if the parent object language admits only `S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]` plus one common calibration mode, then `A_direct_matter=0` for ordinary matter.",
        "- The current corpus does not derive that object language. Relative `w_A`, hidden-marker weights, shadow frames, alpha/mass vertices, and readout/worldtube masks remain legal countermodels.",
        "- `w_star` is classified as common calibration only; `delta_w_A` is the dangerous residual vector.",
        "- Therefore `A_direct_matter`, `delta_w_A`, and the wider `A_matter` interface remain explicit nonclaim residuals.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Grammar Theorem Attempt",
        markdown_table(rows_map["grammar_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap"]),
        "",
        "## Source-Prefactor Classification",
        markdown_table(rows_map["prefactor_classification"], ["class_id", "prefactor_type", "mathematical_form", "status", "effect_on_source", "action"]),
        "",
        "## No-Source-Only Hom Audit",
        markdown_table(rows_map["hom_audit"], ["audit_id", "hom_statement", "current_status", "why_needed", "blocker"]),
        "",
        "## Direct Vertex And No-Marker Audit",
        markdown_table(rows_map["direct_vertex_audit"], ["vertex_id", "vertex", "forbidden_if", "current_status", "residual_if_open"]),
        "",
        "## A-matter Coefficient Pack",
        markdown_table(rows_map["coefficient_pack"], ["coefficient_id", "symbol", "definition", "status", "required_input", "feeds"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1761 is not grim; it is clarifying. The matter branch now has a precise fork. If the parent action really has a minimal typed grammar, then direct ordinary-matter `X` vertices vanish cleanly. If not, the surviving danger is not mystical: it is a finite source-weight vector `delta_w_A` plus hidden-marker, shadow-frame, alpha/mass and readout/worldtube slots. The next derivation-first move is to try to derive the no-source-only Hom theorem from primitive minimality and invariant-algebra triviality; if that fails again, the honest route is a nonclaim `delta_w`/`A_direct_matter` bound runner.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1761 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
