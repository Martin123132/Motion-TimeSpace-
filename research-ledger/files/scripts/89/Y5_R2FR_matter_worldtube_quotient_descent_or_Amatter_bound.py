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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1760"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1760_0_1759_handoff",
        "source_key": "1759_matter_worldtube_next",
        "source_path": ROOT / "1759-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
        "needles": ["NEXT1759_0_primary", "matter/worldtube"],
    },
    {
        "source_id": "SRC1760_1_1756_doc",
        "source_key": "1756_hidden_source_doc",
        "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
        "needles": ["HSC1756_2_matter_worldtube_vertex", "A_matter"],
    },
    {
        "source_id": "SRC1760_2_1756_two_slot",
        "source_key": "1756_quotient_matter_clause",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_TWO_SLOT_SOURCE_FREE_OWNER_PROOF_ATTEMPT.csv",
        "needles": ["OP1756_4_quotient_matter", "CONDITIONAL_ONLY"],
    },
    {
        "source_id": "SRC1760_3_1756_counterexample",
        "source_key": "1756_matter_worldtube_counterexample",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["HSC1756_2_matter_worldtube_vertex", "J_matter"],
    },
    {
        "source_id": "SRC1760_4_1756_residual",
        "source_key": "1756_A_matter_residual",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv",
        "needles": ["HSR1756_2_matter", "A_matter"],
    },
    {
        "source_id": "SRC1760_5_1575_doc",
        "source_key": "1575_matter_descent_signature_doc",
        "source_path": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
        "needles": ["MDS1575_0_action_form", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1760_6_1575_signature",
        "source_key": "1575_matter_descent_signature_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
        "needles": ["MDS1575_0_action_form", "MDS1575_5_verdict"],
    },
    {
        "source_id": "SRC1760_7_1044_pullback",
        "source_key": "1044_matter_pullback_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "needles": ["MPD1044_7_exact_theorem_if_signed", "J_matter=0"],
    },
    {
        "source_id": "SRC1760_8_1044_gate",
        "source_key": "1044_matter_pullback_premise_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv",
        "needles": ["MPG1044_6_verdict", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1760_9_1714_doc",
        "source_key": "1714_worldtube_hilbert_equality_doc",
        "source_path": ROOT / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "needles": ["WHE1714_4_same_object_equality", "EQUALITY_THEOREM_NOT_PROVED"],
    },
    {
        "source_id": "SRC1760_10_1714_worldtube",
        "source_key": "1714_worldtube_hilbert_equality_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1714_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv",
        "needles": ["WHE1714_4_same_object_equality", "Pi_M J_H"],
    },
    {
        "source_id": "SRC1760_11_1718_doc",
        "source_key": "1718_worldtube_support_doc",
        "source_path": ROOT / "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md",
        "needles": ["WTO1718_7_coupling_descent", "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED"],
    },
    {
        "source_id": "SRC1760_12_1718_support",
        "source_key": "1718_worldtube_support_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv",
        "needles": ["WTO1718_7_coupling_descent", "WTO1718_8_verdict"],
    },
    {
        "source_id": "SRC1760_13_1720_functor",
        "source_key": "1720_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_6_no_shadow_or_source_prefactor", "MFS1720_8_verdict"],
    },
    {
        "source_id": "SRC1760_14_1733_current",
        "source_key": "1733_descent_current_lemma",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv",
        "needles": ["DCL1733_6_matter_source_descent", "DCL1733_7_verdict"],
    },
    {
        "source_id": "SRC1760_15_1734_doc",
        "source_key": "1734_projectability_blocker",
        "source_path": ROOT / "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
        "needles": ["DTP1734_5_matter_coupling", "PROJECTABILITY_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1760_16_977_constant_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_7_verdict", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1760_17_977_superselection",
        "source_key": "977_superselection_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_SUPERSELECTION_GATE.csv",
        "needles": ["SSG977_7_verdict", "MISSING_CONSTANT_SOURCE_PARENT_CERTIFICATE"],
    },
    {
        "source_id": "SRC1760_18_1758_constants",
        "source_key": "1758_constant_source_universality",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
        "needles": ["CS1758_6_verdict", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_SOURCE_REGISTER.csv",
    "matter_descent_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
    "chain_rule": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_CHAIN_RULE_DECOMPOSITION.csv",
    "premise_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_DESCENT_PREMISE_AUDIT.csv",
    "worldtube_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
    "amatter_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_AMATTER_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1760_VALIDATION.csv",
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
                "role": "matter/worldtube quotient descent or A_matter residual audit",
                "valid_for_claim": False,
            }
        )
    return rows


def matter_descent_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MWD1760_0_target",
            "claim_piece": "matter/worldtube X-source zero",
            "mathematical_form": "J_matter := delta_X V_m|_{X=0}=0, or equivalently delta_v S_matter=0 for every local vertical v in ker(Dq)",
            "status": "TARGET_EXACT",
            "proof_status": "ZERO_IF_FULL_DESCENT_CONTRACT_SIGNED",
            "gap": "parent q, observed coframe, constants, no-marker, worldtube support and boundary/source-current clauses are not simultaneously signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MWD1760_1_conditional_theorem",
            "claim_piece": "ordinary matter quotient pullback",
            "mathematical_form": "S_matter=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]+dB_A, with Dq[v]=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_status": "CHAIN_RULE_KILLS_BULK_SOURCE_IF_CLAUSES_HOLD",
            "gap": "the theorem is mathematical, but current corpus supplies a contract rather than parent-action ownership",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MWD1760_2_direct_vertex_exclusion",
            "claim_piece": "no independent V_m[X,rho_A,W_source]",
            "mathematical_form": "partial_X V_m|_{0}=0 because no direct matter/source/worldtube slot may depend on X outside q",
            "status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "proof_status": "NOT_SIGNED",
            "gap": "ordinary matter functor and no source-only prefactor/no marker grammar are still policy/contract rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MWD1760_3_worldtube_support",
            "claim_piece": "source worldtube descends through Hilbert support",
            "mathematical_form": "W_source=closure(supp J_H[tau]) and delta_v W_source=0 when J_H and tau descend through q",
            "status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "proof_status": "WORLDTUBE_OWNER_OPEN",
            "gap": "1718 keeps parent action, same-frame J_H, tau lock, compactness, charge map and coupling descent unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MWD1760_4_current_verdict",
            "claim_piece": "J_matter=0 for current MTS",
            "mathematical_form": "delta_v S_matter=0 for local vertical v",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_status": "A_MATTER_RETAINED",
            "gap": "matter descent is exact as a sufficient theorem but cannot be promoted without parent-signing the descent stack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def chain_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_0_variation_identity",
            "term": "matter action vertical variation",
            "mathematical_form": "delta_v S_matter = G_e[v] + G_theta[v] + G_Psi[v] + G_W[v] + G_B[v] + G_V[v]",
            "zero_condition": "all six terms vanish or are separately source-bounded",
            "current_status": "EXACT_DECOMPOSITION",
            "source_channel_if_open": "A_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_1_geometry",
            "term": "observed geometry/coframe pullback",
            "mathematical_form": "G_e[v]=1/2 int sqrt(-g_obs) T^{mu nu} Lie_v g_obs_{mu nu}",
            "zero_condition": "g_obs=Obs_g(q(Phi)) and Dq[v]=0, up to owned gauge/Lorentz lift",
            "current_status": "MISSING_PARENT_Q_AND_OBSERVED_COFAME_DESCENT",
            "source_channel_if_open": "A_geom_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_2_constants",
            "term": "matter constants/material standards",
            "mathematical_form": "G_theta[v]=sum_a int J_theta^a Lie_v theta_a",
            "zero_condition": "theta_A are representation/superselection labels and Lie_v theta_A=0",
            "current_status": "MISSING_PARENT_CONSTANT_SUPERSELECTION_AND_TRIVIAL_MTS_ACTION",
            "source_channel_if_open": "A_theta_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_3_matter_lift",
            "term": "matter-field vertical lift",
            "mathematical_form": "G_Psi[v]=int E_Psi delta_v Psi plus gauge/Lorentz/diffeomorphism boundary terms",
            "zero_condition": "delta_v Psi is zero, on-shell, or an owned gauge/local-Lorentz/diffeomorphism lift with proper boundary",
            "current_status": "MISSING_PARENT_MATTER_LIFT_SIGNATURE",
            "source_channel_if_open": "A_lift_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_4_worldtube",
            "term": "source support/worldtube selector",
            "mathematical_form": "G_W[v]=delta_v W_source contributions from support, source measure or fitted source domain",
            "zero_condition": "W_source=closure(supp J_H[tau]) before readout and tau/J_H descend through q",
            "current_status": "MISSING_PARENT_WORLDTUBE_SUPPORT_OWNER",
            "source_channel_if_open": "A_worldtube_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_5_boundary",
            "term": "matter/worldtube boundary and exact terms",
            "mathematical_form": "G_B[v]=delta_v dB_A plus local projection/boundary flux",
            "zero_condition": "B_A[v] is zero, exact/proper, compact-support silent, or retained in an absolute tail envelope",
            "current_status": "MISSING_BOUNDARY_NOFLUX_OR_ABSOLUTE_TAIL_BOUND",
            "source_channel_if_open": "A_boundary_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "CR1760_6_direct_vertex",
            "term": "independent direct matter/source vertex",
            "mathematical_form": "G_V[v]=delta_v V_m[X,rho_A,W_source]|_{X=0}",
            "zero_condition": "parent grammar forbids any X-dependent matter/source/worldtube slot outside q",
            "current_status": "MISSING_NO_DIRECT_MATTER_X_VERTEX_THEOREM",
            "source_channel_if_open": "A_direct_matter",
            "valid_for_claim": False,
        },
    ]


def premise_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_0_q_map",
            "required_clause": "parent quotient q and Dq exist before readout",
            "mathematical_form": "q: Phi_parent -> Q_obs with Dq[v_X]=0 for local vertical representative directions",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "geometry pullback and matter descent cannot be promoted",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_1_observed_geometry",
            "required_clause": "observed coframe/metric descends through q",
            "mathematical_form": "e_obs=Obs_e(q(Phi)), g_obs=Obs_g(q(Phi)), omega=omega[e_obs]",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "T^{mu nu} Lie_v g_obs term becomes a physical local source",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_2_matter_functor",
            "required_clause": "ordinary matter action is a functor of observed geometry and fixed representation data",
            "mathematical_form": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "if_missing": "direct X/source/worldtube vertices remain legal",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_3_constants",
            "required_clause": "masses, charges, alpha_EM, clocks and material standards are X-blind",
            "mathematical_form": "Lie_v theta_A=0 and no theta_A(X,I_Q,m,h)",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "if_missing": "clock, WEP, fine-structure and source-normalization channels remain",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_4_no_shadow_prefactor",
            "required_clause": "no hidden conformal/disformal frame, source-only weight, marker or post-readout EFT counterterm",
            "mathematical_form": "forbid S_ord=sum_A w_A(X,m,W) S_A or g_A=A_A(X)^2 g_obs",
            "current_status": "POLICY_CONTRACT_NOT_THEOREM",
            "if_missing": "relative source/test charge can hide while ordinary-looking matter remains",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_5_worldtube_support",
            "required_clause": "source worldtube is parent-owned Hilbert support",
            "mathematical_form": "W_source=closure(supp J_H[tau]) before source/readout fitting",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_missing": "source domain and material support can inject J_matter or source-normalization hair",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_6_boundary",
            "required_clause": "matter boundary/worldtube terms are zero, exact/proper, or explicitly bounded",
            "mathematical_form": "Pi_local delta_v B_A=0 or ||Pi_local delta_v B_A|| is source-backed",
            "current_status": "OPEN",
            "if_missing": "boundary/local projection flux re-enters the X Euler-Lagrange equation",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_7_hilbert_source_owner",
            "required_clause": "ordinary active source is the same Hilbert/coframe current",
            "mathematical_form": "tau_a^mu=det(e)^-1 delta S_matter/delta e_mu^a and one global kappa multiplies sum_A T_A",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "if_missing": "non-Hilbert or species-weighted source current remains live",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PRE1760_8_verdict",
            "required_clause": "all descent premises hold in one parent branch",
            "mathematical_form": "PRE1760_0 through PRE1760_7 all signed",
            "current_status": "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED",
            "if_missing": "A_matter remains mandatory",
            "claim_allowed": False,
        },
    ]


def worldtube_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WTA1760_0_support_selector",
            "claim": "worldtube source support is not fitted",
            "mathematical_form": "W_source=closure(supp J_H[tau]) with compact regular support and linked exterior surfaces",
            "current_status": "CONDITIONAL_LEMMA_ONLY",
            "remaining_gap": "parent action, same-frame J_H, tau lock, compactness and coupling descent are unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WTA1760_1_same_charge",
            "claim": "Hilbert source equals exterior/topological mass source before orbital calibration",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero and int_W Pi_M J_H = int_S Q_M[tau]",
            "current_status": "NOT_DERIVED_KEY_BLOCKER",
            "remaining_gap": "R_eq, I_commutator, B_zero_flux and parent Q_M remain nonclaim residuals",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WTA1760_2_no_readout_domain_mask",
            "claim": "source domain/projector is parent-owned before readout",
            "mathematical_form": "Pi_M and W_source are fixed by the parent branch/topology, not selected after seeing orbital data",
            "current_status": "GUARDRAIL_INSTALLED_NOT_THEOREM",
            "remaining_gap": "projector/domain mismatch can still source N_domain or A_worldtube_matter",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WTA1760_3_matter_worldtube_verdict",
            "claim": "worldtube terms do not source X",
            "mathematical_form": "delta_v W_source=0 and delta_v M_source[W]=0 for vertical v",
            "current_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "remaining_gap": "retain A_worldtube_matter inside A_matter until support/charge equality closes",
            "valid_for_claim": False,
        },
    ]


def amatter_bound_rows() -> list[dict[str, Any]]:
    source_path = str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv")
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_0_zero_condition",
            "quantity": "Z_matter",
            "required_form": "Z_matter=True only if q/coframe descent, constants, matter lift, no direct V_m, worldtube support and boundary clauses all pass",
            "current_status": "FALSE_PARENT_UNSIGNED",
            "formula": "J_matter=0 condition",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_1_A_geom",
            "quantity": "A_geom_matter",
            "required_form": "||1/2 int sqrt(-g_obs) T^{mu nu} Lie_v g_obs_{mu nu}||_{E*}",
            "current_status": "MISSING_Q_COFAME_DESCENT_OR_A_GEOM",
            "formula": "geometry/coframe pullback leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_2_A_theta",
            "quantity": "A_theta_matter",
            "required_form": "||sum_a int J_theta^a Lie_v theta_a||_{E*}",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_A_THETA",
            "formula": "matter constants/material standards leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_3_A_lift",
            "quantity": "A_lift_matter",
            "required_form": "||int E_Psi delta_v Psi + proper-boundary lift terms||_{E*}",
            "current_status": "MISSING_MATTER_LIFT_OR_A_LIFT",
            "formula": "matter field vertical lift leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_4_A_direct",
            "quantity": "A_direct_matter",
            "required_form": "||delta_v V_m[X,rho_A,W_source]|_{X=0}||_{E*}",
            "current_status": "MISSING_NO_DIRECT_MATTER_X_VERTEX_OR_A_DIRECT",
            "formula": "direct matter/worldtube X vertex",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_5_A_worldtube",
            "quantity": "A_worldtube_matter",
            "required_form": "||delta_v W_source or source-measure support terms||_{E*}",
            "current_status": "MISSING_WORLDTUBE_SUPPORT_OWNER_OR_A_WORLDTUBE",
            "formula": "source support/worldtube selector leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_6_A_boundary",
            "quantity": "A_boundary_matter",
            "required_form": "||Pi_local delta_v B_A||_{E*}",
            "current_status": "MISSING_MATTER_BOUNDARY_NOFLUX_OR_A_BOUNDARY_MATTER",
            "formula": "matter/worldtube boundary projection leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_7_A_nonHilbert",
            "quantity": "A_nonHilbert_matter",
            "required_form": "||J_nonHilbert||_{E*} or theorem-zero from source-owner certificate",
            "current_status": "MISSING_NONHILBERT_SOURCE_ZERO_OR_A_NONHILBERT",
            "formula": "non-Hilbert/source-current leak",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AM1760_8_A_matter",
            "quantity": "A_matter",
            "required_form": "A_matter <= A_geom_matter + A_theta_matter + A_lift_matter + A_direct_matter + A_worldtube_matter + A_boundary_matter + A_nonHilbert_matter in one E* norm",
            "current_status": "MISSING_COMMON_ESTAR_NORM_AND_COMPONENT_VALUES",
            "formula": "||J_matter||_{E*} <= A_matter",
            "source_path": source_path,
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1760_0_matter",
            "quantity": "J_matter",
            "current_status": "NOT_ZEROED",
            "evidence": "1044/1575 give an exact conditional pullback theorem, but all premise gates are not signed",
            "remaining_gap": "parent matter functor, q/coframe descent, constants, no-marker/source-prefactor, worldtube support, boundary and source-current owner",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1760_1_Amatter",
            "quantity": "A_matter",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "1756 already carries A_matter=||delta_X V_m||_{E*}; 1760 expands its component interface",
            "remaining_gap": "component values, common E* norm, operator/projection response and source paths for numeric inputs",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1760_2_source_silence",
            "quantity": "S_cg(D_L=0,Y)",
            "current_status": "NOT_DERIVED",
            "evidence": "affine, coupling-chain and matter hidden sources are nonzero/nonclaim; boundary/history/tower/mu/kernel channels remain",
            "remaining_gap": "J_hidden still includes A_shift, A_marker, A_matter, A_chain, A_boundary, A_hist, A_tower, A_mu_even and A_kernel",
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1760_0_conditional_theorem",
            "decision": "MATTER_DESCENT_CHAIN_RULE_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "if S_matter factors through q and the matter/constants/worldtube/boundary clauses hold, the vertical variation vanishes",
            "next_action": "keep the theorem as a parent-action contract, not a claim",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1760_1_parent_signature",
            "decision": "PARENT_SIGNATURE_NOT_SIGNED",
            "reason": "current evidence still has q/coframe, constants, no-marker/source-prefactor, worldtube support and boundary/source-owner gaps",
            "next_action": "retain A_matter and expose its components rather than smuggling local GR",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1760_2_A_matter",
            "decision": "A_MATTER_INTERFACE_WRITTEN_NONCLAIM",
            "reason": "the zero theorem failed for current MTS, so the matter/worldtube hidden source must be bounded or derived later",
            "next_action": "do not set A_matter=0; use component rows only as nonclaim plumbing",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1760_3_best_next",
            "decision": "NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_IS_NEXT_BEST_DERIVATION_ROUTE",
            "reason": "the sharpest remaining matter-specific obstruction is the legal possibility of V_m[X,rho_A,W_source] or a source-only prefactor",
            "next_action": "build 1761 no-direct matter X vertex grammar proof or A_direct/A_worldtube coefficient pack",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1760_0_matter_descent_parent",
            "claim": "ordinary matter descends through q in the parent action",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_Q_COFAME_MATTER_FUNCTOR_CONSTANTS_NO_MARKER_BOUNDARY_WORLDTUBE",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1760_1_no_direct_vertex",
            "claim": "no V_m[X,rho_A,W_source] direct matter/worldtube vertex exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_DIRECT_MATTER_X_VERTEX_THEOREM",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1760_2_Amatter_zero",
            "claim": "A_matter=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_MATTER_DESCENT_NOT_PARENT_SIGNED",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1760_3_Amatter_bound",
            "claim": "A_matter is finite and sourced in a declared E* norm",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_COMPONENT_VALUES_COMMON_NORM_AND_PROJECTION_RESPONSE_MISSING",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1760_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_MATTER_AND_OTHER_HIDDEN_SOURCE_CHANNELS_ACTIVE",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1760_0_primary",
            "next_target": "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_no_direct_matter_X_vertex_grammar_or_Amatter_coefficient_pack.py",
            "objective": "try to prove the parent grammar forbids V_m[X,rho_A,W_source], source-only prefactors, hidden matter frames and material markers; otherwise stage A_direct/A_worldtube/A_theta coefficients",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1760_1_fallback",
            "next_target": "1761b-Y5-R2FR-Amatter-E-star-bound-runner.md",
            "script": "scripts/Y5_R2FR_Amatter_E_star_bound_runner.py",
            "objective": "turn A_geom/A_theta/A_direct/A_worldtube/A_boundary into a runnable nonclaim source-envelope interface with units and operator/projection norms",
            "selection_status": "held_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "matter_descent_attempt": matter_descent_attempt_rows(),
        "chain_rule": chain_rule_rows(),
        "premise_audit": premise_audit_rows(),
        "worldtube_audit": worldtube_audit_rows(),
        "amatter_bound": amatter_bound_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1760_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1760_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    lower = key.lower()
    return lower in {
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
    status_keys = {"current_status", "status", "row_status", "proof_status", "attempt_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_true(value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1760_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1760_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1760() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1760*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def matter_theorem_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "MWD1760_1_conditional_theorem"
        and row["status"] == "EXACT_CONDITIONAL_THEOREM"
        and row["claim_allowed"] is False
        for row in rows_map["matter_descent_attempt"]
    )


def matter_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "MWD1760_4_current_verdict"
        and row["proof_status"] == "A_MATTER_RETAINED"
        and row["valid_for_claim"] is False
        for row in rows_map["matter_descent_attempt"]
    )


def amatter_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["amatter_bound"]
    return any(row["quantity"] == "A_matter" and row["valid_for_claim"] is False for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1760_2_source_silence"
        and row["current_status"] == "NOT_DERIVED"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1760_0_primary" and row["selection_status"] == "selected"
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
        check_row("VAL1760_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1760_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1760_2_conditional_theorem", matter_theorem_present(rows_map), "matter descent theorem recorded as exact conditional", "conditional theorem missing or promoted"),
        check_row("VAL1760_3_matter_not_promoted", matter_not_promoted(rows_map), "matter/worldtube source remains unpromoted", "matter source promoted or verdict missing"),
        check_row("VAL1760_4_Amatter_interface_nonclaim", amatter_interface_nonclaim(rows_map), "A_matter interface remains nonclaim", "A_matter interface missing or promoted"),
        check_row("VAL1760_5_source_zero_blocked", source_zero_blocked(rows_map), "source-zero status remains blocked", "source-zero status missing or promoted"),
        check_row("VAL1760_6_claim_gates_safe", all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates), "all claim gates remain blocked", "one or more claim gates opened"),
        check_row("VAL1760_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1760_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1760_9_decision_next",
            any(row["decision_id"] == "DEC1760_3_best_next" and row["decision"] == "NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_IS_NEXT_BEST_DERIVATION_ROUTE" for row in rows_map["decision"]),
            "decision selects no-direct-matter-X-vertex route",
            "best-next decision missing",
        ),
        check_row("VAL1760_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1760_11_csv_parse", csv_parse_all(), "all generated 1760 CSVs parse", "one or more generated 1760 CSVs fail to parse"),
        check_row("VAL1760_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1760_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1760_14_formalization_untouched", formalization_untouched_for_1760(), "no 1760 outputs found under formalization-workbench", "1760 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1760_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1760 matter/worldtube quotient descent or A_matter bound",
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
        "# 1760 - Matter/Worldtube Quotient Descent Or A_matter Bound",
        "",
        "## Verdict",
        "- 1760 tries the ordinary matter/worldtube route selected by 1759.",
        "- The chain-rule theorem is clean: if matter only sees `e_obs(q(Phi))`, fixed representation data, owned matter lifts, parent-owned Hilbert worldtubes, and silent boundaries, then `delta_v S_matter=0` for vertical `v` and `J_matter=0`.",
        "- Current MTS does not yet parent-sign those clauses. The theorem is therefore a contract, not a local-GR/Newton claim.",
        "- The live obstruction is the direct/legal possibility of `V_m[X,rho_A,W_source]`, hidden source prefactors, material markers, boundary tails, or worldtube/source-support terms outside `q`.",
        "- Therefore `A_matter` is retained as an explicit nonclaim residual interface.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Matter/Worldtube Descent Attempt",
        markdown_table(rows_map["matter_descent_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap"]),
        "",
        "## Chain-Rule Decomposition",
        markdown_table(rows_map["chain_rule"], ["term_id", "term", "mathematical_form", "zero_condition", "current_status", "source_channel_if_open"]),
        "",
        "## Descent Premise Audit",
        markdown_table(rows_map["premise_audit"], ["premise_id", "required_clause", "mathematical_form", "current_status", "if_missing"]),
        "",
        "## Worldtube Source Owner Audit",
        markdown_table(rows_map["worldtube_audit"], ["audit_id", "claim", "mathematical_form", "current_status", "remaining_gap"]),
        "",
        "## A-matter Bound Interface",
        markdown_table(rows_map["amatter_bound"], ["interface_id", "quantity", "required_form", "current_status", "formula"]),
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
        "This checkpoint does not close the GR/Newton bridge, but it removes a major fog bank. Ordinary matter can be made source-silent by a precise quotient-pullback theorem; that is the right shape. The reason it is not yet a claim is also precise: the parent language has not forbidden direct matter/worldtube `X` vertices, hidden source prefactors, material markers, unsupported worldtube selectors, boundary tails, or non-Hilbert currents. The next derivation-first target should therefore attack the grammar of `V_m[X,rho_A,W_source]` directly: prove that slot cannot exist in the parent action, or promote `A_direct_matter`/`A_worldtube_matter` into explicit nonclaim input rows.",
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
    doc_path = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1760 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
