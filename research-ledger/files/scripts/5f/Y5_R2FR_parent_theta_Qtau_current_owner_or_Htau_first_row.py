from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1733"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1733 - Parent Theta Qtau Current Owner Or Htau First Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1733_0_1732_doc",
        "source_key": "1732_doc",
        "source_path": ROOT / "1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md",
        "needles": ["NEXT1732_0_primary", "Theta_total"],
    },
    {
        "source_id": "SRC1733_1_1732_next",
        "source_key": "1732_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_NEXT_TARGET.csv",
        "needles": ["1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md", "selected"],
    },
    {
        "source_id": "SRC1733_2_1732_validation",
        "source_key": "1732_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1732_VALIDATION.csv",
        "needles": ["VAL1732_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1733_3_1646_owner_audit",
        "source_key": "1646_theta_Qtau_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "needles": ["TQ1646_5_owner_verdict", "FAIL_CURRENT_CLAIM"],
    },
    {
        "source_id": "SRC1733_4_771_doc",
        "source_key": "771_theta_Qtau_doc",
        "source_path": ROOT / "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
        "needles": ["TQ771_6_owner_verdict", "not_accepted_current_corpus"],
    },
    {
        "source_id": "SRC1733_5_667_doc",
        "source_key": "667_parent_boundary_action_doc",
        "source_path": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
        "needles": ["PBA667_3_charge_definition", "formal_Noether_shape_available"],
    },
    {
        "source_id": "SRC1733_6_667_variation",
        "source_key": "667_variation_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
        "needles": ["VL667_3_Hamiltonian_variation", "candidate_not_integrability_proof"],
    },
    {
        "source_id": "SRC1733_7_993_Qtau_decomp",
        "source_key": "993_Qtau_decomposition",
        "source_path": RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        "needles": ["QDEC993_5_total", "not_promoted"],
    },
    {
        "source_id": "SRC1733_8_1645_Htau",
        "source_key": "1645_Htau_integrability",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv",
        "needles": ["HTM1645_5_verdict", "FAIL_CURRENT_CLAIM"],
    },
    {
        "source_id": "SRC1733_9_772_hybrid_doc",
        "source_key": "772_hybrid_current_owner",
        "source_path": ROOT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
        "needles": ["HCO772_7_owner_verdict", "fail_current_corpus"],
    },
    {
        "source_id": "SRC1733_10_668_sector_doc",
        "source_key": "668_sector_owner",
        "source_path": ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
        "needles": ["LOG668_2_LX_owner", "fail_current_claim"],
    },
    {
        "source_id": "SRC1733_11_1487_owner_audit",
        "source_key": "1487_theta_Qtau_ownership",
        "source_path": RESIDUALS / "P8_Y5_R10_1487_THETA_QTAU_OWNERSHIP_AUDIT.csv",
        "needles": ["TQO1487_6_verdict", "NOT_EXTRACTED"],
    },
    {
        "source_id": "SRC1733_12_1667_Dq_doc",
        "source_key": "1667_q_Dq_doc",
        "source_path": ROOT / "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md",
        "needles": ["Q_NOT_COMPUTABLE_CURRENT_CORPUS", "Dq"],
    },
    {
        "source_id": "SRC1733_13_1668_constraint_doc",
        "source_key": "1668_constraint_first_doc",
        "source_path": ROOT / "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md",
        "needles": ["CFA1668_8_verdict", "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CORPUS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_SOURCE_REGISTER.csv",
    "current_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "descent_lemma": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv",
    "component_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
    "htau_first_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_HTAU_FIRST_ROW_SCHEMA.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THEOREM_ATTEMPT.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1733_VALIDATION.csv",
}


COPY_MAP = {
    "current_owner_audit": "R2FR_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "descent_lemma": "R2FR_1733_DESCENT_CURRENT_LEMMA.csv",
    "component_rows": "R2FR_1733_THETA_QTAU_COMPONENT_ROWS.csv",
    "htau_first_rows": "R2FR_1733_HTAU_FIRST_ROW_SCHEMA.csv",
    "theorem_attempt": "R2FR_1733_THEOREM_ATTEMPT.csv",
    "runner_refusal": "R2FR_1733_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1733_DECISION_LEDGER.csv",
    "next_target": "R2FR_1733_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1733_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles_present = all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": yesno(needles_present),
                "checked_utc": UTC,
            }
        )
    return rows


def current_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_0_L_parent",
            "needed_object": "one explicit current-chain L_parent",
            "owner_test": "delta L_parent = E_A delta Phi^A + d Theta_total with EH, matter, extra, boundary, tau, reference and coupling sectors included",
            "current_result": "TEMPLATE_AVAILABLE_NOT_CURRENT_OWNER",
            "blocker": "no single local parent action has all retained sectors varied before readout",
            "claim_effect_if_closed": "Theta_total becomes an extracted object rather than a named placeholder",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_1_Theta_total",
            "needed_object": "Theta_total sector split",
            "owner_test": "Theta_total = Theta_EH + Theta_matter + Theta_X + Theta_projector + delta B_ref + Theta_boundary",
            "current_result": "TEMPLATE_AVAILABLE_NOT_EXTRACTED",
            "blocker": "only EH/reference formal pieces are stable; X/projector/boundary/coupling pieces are not extracted from one variation",
            "claim_effect_if_closed": "delta_H_tau one-form can be evaluated componentwise",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_2_Noether_current",
            "needed_object": "J_tau and Q_tau^MTS",
            "owner_test": "J_tau = Theta_total(Phi,L_tau Phi) - i_tau L_parent = d Q_tau^MTS + C_tau",
            "current_result": "FORMAL_SHAPE_AVAILABLE_NOT_CERTIFICATE",
            "blocker": "Q_X, C_tau, C_extra, C_projector, C_boundary and C_ref are not extracted for retained sectors",
            "claim_effect_if_closed": "Q_tau^MTS becomes a candidate Hamiltonian source charge",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_3_tau_projectability",
            "needed_object": "tau action on all parent fields",
            "owner_test": "L_tau Phi is projectable through q and fixed across source, charge, clock, boundary and orbit readout",
            "current_result": "NOT_PARENT_OWNED",
            "blocker": "observed tau, source tau, charge tau, boundary tau and clock/readout tau remain split",
            "claim_effect_if_closed": "removes time-generator ambiguity from H_tau",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_4_boundary_reference",
            "needed_object": "B_ref and boundary representative",
            "owner_test": "boundary improvement and reference subtraction are fixed before readout and derivative-silent",
            "current_result": "NOT_PARENT_OWNED",
            "blocker": "reference branch, edge charge, relative boundary class and no-hair terms remain residual branches",
            "claim_effect_if_closed": "prevents Q_tau shifts under counterterm/reference choices",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_5_matter_coupling_descent",
            "needed_object": "ordinary matter/coupling descent in same current",
            "owner_test": "matter, constants, charge normalization, measure, coframe and connection descend through q(Phi)",
            "current_result": "BLOCKED_BY_COUPLING_DESCENT",
            "blocker": "common geometry/WEP/no-marker/source-normalization route remains closure-level rather than parent-signed",
            "claim_effect_if_closed": "prevents Hamiltonian proof from hiding WEP/source-normalization leaks",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_6_q_Dq_descent",
            "needed_object": "computable quotient map q and kernel Dq",
            "owner_test": "q(Phi) and ker(Dq) are explicit before matter/readout; vertical directions are either killed or residualized",
            "current_result": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
            "blocker": "1667/1668 keep Z/phi/R_AB Dq leaks and constraint-first route unsigned",
            "claim_effect_if_closed": "extra representative directions can be proved silent without smuggling",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1733_7_owner_verdict",
            "needed_object": "Theta_total/Q_tau current owner",
            "owner_test": "COA1733_0 through COA1733_6 pass together",
            "current_result": "OWNER_NOT_SIGNED",
            "blocker": "current owner remains a scaffold; H_tau first rows and descent-current clauses are required",
            "claim_effect_if_closed": "would reactivate the Hamiltonian local-GR bridge",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def descent_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_0_contract",
            "lemma_clause": "descent-current lemma contract",
            "mathematical_statement": "If L_parent = q^*L_red + L_vert_alg + dB, tau is q-projectable, Dq[v]=0 on vertical fibres, Theta_vert(v)=0/exact, and B is fixed before readout, then Theta_parent = q^*Theta_red + delta B + exact and Q_tau^parent = q^*Q_tau^red + i_tau B + proper corner terms.",
            "current_status": "CONDITIONAL_LEMMA_WRITTEN",
            "missing_for_claim": "all antecedents must be parent-signed; current row is a contract, not evidence",
            "would_close": "legitimate route for Q_tau^MTS to reduce to EH/reduced charge without inserting silence",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_1_q_map",
            "lemma_clause": "q and Dq are explicit",
            "mathematical_statement": "q: Phi_parent -> Q_obs is defined with tangent map Dq and visible variables declared before readout",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "q is not computable in 1667; Dq_Z, Dq_phi and Dq_RAB/Jq leaks are retained",
            "would_close": "vertical/silent clauses become runnable instead of verbal",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_2_action_factorization",
            "lemma_clause": "action factors through q plus silent vertical block",
            "mathematical_statement": "L_parent(Phi) = q^*L_red(q(Phi)) + L_vert_alg(Phi_v) + dB with no hidden matter/readout dependence on Phi_v",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "constraint-first Z/phi/R_AB removal is not derived and L_X sector owner is missing",
            "would_close": "extra-sector current either descends or becomes an explicit residual",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_3_tau_projectable",
            "lemma_clause": "tau is projectable through q",
            "mathematical_statement": "Dq(L_tau Phi) = L_tau_red q(Phi), and tau_source=tau_charge=tau_clock=tau_readout",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "tau action is not owned across source, charge, clock, boundary and orbit readout",
            "would_close": "H_tau charge refers to one physical observed time flow",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_4_vertical_symplectic_silence",
            "lemma_clause": "vertical symplectic current is zero/exact/proper",
            "mathematical_statement": "Theta_vert(delta Phi_v)=0 or exact on allowed variations, so int_S(delta Q_X - i_tau Theta_X) is zero/proper or retained",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "Theta_X, Q_X, omega_X and boundary conditions are not sector-owned",
            "would_close": "delta_H_tau extra-sector curl becomes zero or an explicit finite component",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_5_boundary_reference_fixed",
            "lemma_clause": "boundary/reference improvement fixed",
            "mathematical_statement": "B_ref and B_class are selected by parent branch/topology and cannot absorb source/radius/time/frame/readout changes",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "reference derivative silence and boundary no-hair remain nonclaim",
            "would_close": "Q_tau improvement ambiguity stops leaking into M_H_ref",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_6_matter_source_descent",
            "lemma_clause": "matter/source/coupling descent",
            "mathematical_statement": "ordinary matter, constants, coframe, connection, source measure and test-body readout depend only on q(Phi)",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "coupling descent, common geometry, WEP and source-normalization are not parent-signed",
            "would_close": "Hamiltonian charge can be compared to measured source mass without hidden marker charge",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "DCL1733_7_verdict",
            "lemma_clause": "descent-current lemma accepted for current MTS",
            "mathematical_statement": "DCL1733_1 through DCL1733_6 all pass",
            "current_status": "DESCENT_CURRENT_NOT_SIGNED",
            "missing_for_claim": "q/Dq, action factorization, tau, vertical silence, boundary/reference and matter/source descent all remain unsigned",
            "would_close": "Theta_total/Q_tau owner could be promoted from contract to theorem",
            "valid_for_claim": no(),
        },
    ]


def component_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["current_owner_audit"]),
        str(OUTPUTS["descent_lemma"]),
        str(RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv"),
        str(RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv"),
        str(ROOT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_0_EH",
            "quantity": "Theta_EH;Q_tau_EH",
            "definition": "standard EH covariant phase-space current for the observed metric sector",
            "formula": "Q_tau^EH[g_obs,tau] with EH boundary conditions and fixed normalization",
            "current_status": "CONDITIONAL_GR_REFERENCE_ONLY",
            "missing_inputs": "MISSING_PARENT_REDUCTION_TO_EH;MISSING_FIXED_TAU;MISSING_BOUNDARY_CONDITIONS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "CONDITIONAL_REFERENCE_NOT_FULL_OWNER",
            "units": "Hamiltonian_charge_units_conditional",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_1_X_extra",
            "quantity": "Theta_X;Q_tau_X;C_tau_X",
            "definition": "MTS extra-sector contribution to the observed-time Noether current",
            "formula": "delta L_X = E_X delta X + dTheta_X; J_tau^X = Theta_X(L_tau X)-i_tau L_X = dQ_tau^X+C_tau^X",
            "current_status": "MISSING_SECTOR_LAGRANGIAN_OWNER",
            "missing_inputs": "MISSING_L_X;MISSING_THETA_X;MISSING_Q_TAU_X;MISSING_C_TAU_X;MISSING_BOUNDARY_CONDITIONS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_THETA_QX_OWNER",
            "units": "charge_or_symplectic_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_2_projector_PiM",
            "quantity": "Theta_projector;Q_tau_projector;PiM_chain_map",
            "definition": "projector/source-current contribution to the Hamiltonian charge and mass projection",
            "formula": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H; int_S Pi_M J_H = 4*pi*G_ref(H_tau-H_ref)",
            "current_status": "MISSING_PROJECTOR_CURRENT_OWNER",
            "missing_inputs": "MISSING_PIM_DEFINITION;MISSING_DELTA_PIM;MISSING_J_H;MISSING_COMMUTATOR_ZERO_OR_BOUND;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_PROJECTOR_QTAU_PIECE",
            "units": "operator_or_charge_map_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_3_boundary_reference",
            "quantity": "Theta_boundary;Q_tau_boundary;delta B_ref",
            "definition": "boundary improvement, reference subtraction and class/no-hair contribution",
            "formula": "Theta_total includes delta B_ref + Theta_boundary; Q_tau shifts by i_tau B plus corner/class terms",
            "current_status": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "missing_inputs": "MISSING_B_REF;MISSING_B_CLASS;MISSING_CORNER_TERMS;MISSING_REFERENCE_LOCK;MISSING_BOUNDARY_NOHAIR",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_BOUNDARY_QTAU_PIECE",
            "units": "charge_or_boundary_flux_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_4_tau_surface",
            "quantity": "tau_surface_reference_piece",
            "definition": "observed-time generator, surface choice and reference branch contribution",
            "formula": "Delta_tau + Delta_S + Delta_ref normalized only after one tau and one surface pair are parent-selected",
            "current_status": "MISSING_TAU_SURFACE_REFERENCE_LOCK",
            "missing_inputs": "MISSING_TAU_ID;MISSING_SURFACE_PAIR;MISSING_H_REF_LOCK;MISSING_FRAME_LOCK;MISSING_SOURCE_READOUT_LOCK",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_TAU_REF_SURFACE_MISMATCH",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_5_Dq_leak",
            "quantity": "Dq_current_leak_piece",
            "definition": "failure of quotient descent to kill representative/residual variables before matter/readout",
            "formula": "Dq[v] and DObs_e[Dq[v]] source current leakage into Theta/Q_tau or source readout",
            "current_status": "MISSING_Q_DQ_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_Q_MAP;MISSING_DQ_Z;MISSING_DQ_PHI;MISSING_DQ_RAB_JQ;MISSING_OBSERVED_COFRAME_FUNCTOR",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DQ_CURRENT_LEAK",
            "units": "arena_dependent_leak_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQC1733_6_total_Qtau",
            "quantity": "Q_tau^MTS_total",
            "definition": "full observed-time Hamiltonian charge candidate",
            "formula": "Q_tau^MTS = Q_EH + Q_X + Q_projector + Q_boundary + Q_matter/source, with all silent pieces proved zero/exact or retained",
            "current_status": "NOT_PROMOTED_COMPONENTS_MISSING",
            "missing_inputs": "MISSING_Q_X;MISSING_Q_PROJECTOR;MISSING_Q_BOUNDARY;MISSING_SOURCE_GLUE;MISSING_DQ_DESCENT;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "BLOCKED",
            "units": "Hamiltonian_charge_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def htau_first_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["component_rows"]),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv"),
        str(RESIDUALS / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv"),
        str(ROOT / "772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HFR1733_0_alpha_tau",
            "quantity": "alpha_tau_one_form",
            "definition": "Hamiltonian one-form on local branch field space",
            "formula": "alpha_tau[delta Phi] = int_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref",
            "required_inputs": "Theta_total;Q_tau^MTS;tau_id;surface_pair;H_ref;field_variation;source_path",
            "current_status": "FORMAL_DEFINITION_ONLY",
            "missing_inputs": "MISSING_THETA_TOTAL;MISSING_Q_TAU_MTS;MISSING_TAU_ID;MISSING_SURFACE_PAIR;MISSING_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_ALPHA_TAU_SOURCE_ROW",
            "units": "energy_variation_or_charge_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HFR1733_1_curl_components",
            "quantity": "d_field_alpha_tau_components",
            "definition": "no-cancellation decomposition of the H_tau integrability curl",
            "formula": "d alpha_tau = I_EH + I_X + I_projector + I_boundary + I_ref + I_tau + I_surface + I_Dq",
            "required_inputs": "component_values_or_zero_theorems;common_units;M_H_ref;source_paths",
            "current_status": "MISSING_COMPONENTS",
            "missing_inputs": "MISSING_I_X;MISSING_I_PROJECTOR;MISSING_I_BOUNDARY;MISSING_I_REF;MISSING_I_TAU;MISSING_I_SURFACE;MISSING_I_DQ;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DELTA_H_TAU_CURL_COMPONENTS",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HFR1733_2_total_deltaH",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "absolute integrability residual normalized by positive same-frame M_H_ref",
            "formula": "(|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref",
            "required_inputs": "HFR1733_1 components;positive_M_H_ref;no_cancellation_flag;source_paths",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "missing_inputs": "MISSING_CURL_COMPONENTS;MISSING_M_H_REF;MISSING_COMMON_UNITS;MISSING_NO_CANCELLATION_LEDGER",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "BLOCKED",
            "units": "dimensionless_gate",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQT1733_0_covariant_current",
            "statement": "A covariant parent action supplies a Noether current and charge by variation.",
            "mathematical_form": "delta L = E_A delta Phi^A + dTheta; J_tau = Theta(Phi,L_tau Phi)-i_tau L = dQ_tau + C_tau",
            "current_status": "VALID_CONDITIONAL_FORM",
            "current_blocker": "conditional form does not identify current-MTS retained-sector owners",
            "would_close": "formal owner grammar for Theta_total and Q_tau",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQT1733_1_descent_current",
            "statement": "If the parent action descends through q, the reduced EH/current charge can be used without smuggling extra-sector silence.",
            "mathematical_form": "L_parent=q^*L_red+L_vert_alg+dB; Dq[v]=0; tau projectable; Q_parent=q^*Q_red+i_tau B+proper",
            "current_status": "CONDITIONAL_LEMMA_NOT_SIGNED",
            "current_blocker": "q/Dq, action factorization, tau, boundary/reference and matter descent are all unsigned",
            "would_close": "strict low-scrutiny route to Q_tau^MTS",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQT1733_2_current_MTS_owner",
            "statement": "Current MTS supplies the parent-signed Theta_total/Q_tau owner.",
            "mathematical_form": "COA1733_0..COA1733_7 all pass and TQC1733 rows contain no MISSING markers",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "owner audit remains unsigned and Q_tau total is not promoted",
            "would_close": "H_tau first row becomes computable",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TQT1733_3_current_verdict",
            "statement": "H_tau/M_H_ref/local-GR gates can reopen from 1733.",
            "mathematical_form": "alpha_tau closed, M_H_ref positive, Q_tau equals measured source charge, all retained curls zero/bounded",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "H_tau rows are schema-only and M_H_ref/source-GM calibration remains blocked",
            "would_close": "reactivate local-GR/Newton derivation branch",
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1733_0_theta_Qtau_owner",
            "quantity": "Theta_total/Q_tau current owner",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_L_PARENT_CURRENT_CHAIN;MISSING_THETA_X;MISSING_Q_X;MISSING_BOUNDARY_REFERENCE_OWNER;MISSING_TAU_PROJECTABILITY;MISSING_COUPLING_DESCENT",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1733_1_descent_current",
            "quantity": "descent-current lemma",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_Q_MAP;MISSING_DQ_KERNEL;MISSING_ACTION_FACTORIZATION;MISSING_VERTICAL_SYMPLECTIC_SILENCE;MISSING_MATTER_SOURCE_DESCENT",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1733_2_Htau_first_row",
            "quantity": "alpha_tau and delta_H_tau_nonintegrable_over_MH",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_Q_TAU_MTS;MISSING_THETA_TOTAL;MISSING_CURL_COMPONENTS;MISSING_M_H_REF",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1733_3_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_PARENT_CURRENT_OWNER;NO_HTAU_INTEGRABILITY;NO_MHREF;NO_MEASURED_GM_CALIBRATION;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1733_0_contract_kept",
            "decision": "keep the exact descent-current lemma as the derivation contract",
            "because": "it is the clean route that would let MTS inherit GR/EH current structure only after quotient and boundary premises are signed",
            "next_action": "attack q/Dq and tau projectability rather than inserting Q_tau by hand",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1733_1_no_owner_claim",
            "decision": "do not accept Theta_total/Q_tau owner yet",
            "because": "sector L_X, Q_X, boundary/reference, tau, coupling descent and q/Dq are still missing",
            "next_action": "keep TQC1733 and HFR1733 as nonclaim source rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1733_2_next_bottleneck",
            "decision": "q/Dq plus tau projectability is the next bottleneck",
            "because": "without a projectable observed time flow through a computable quotient, no current descent theorem can be signed",
            "next_action": "attempt the Dq/tau descent-current clause or emit a theta-leak source row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1733_0_primary",
            "next_target": "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
            "script": "scripts/Y5_R2FR_current_descent_lemma_Dq_tau_projectability_or_theta_leak_row.py",
            "objective": "prove q/Dq and tau projectability clauses needed by the descent-current lemma, or stage nonclaim theta/Qtau leak rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1733_1_parallel_Htau_pack",
            "next_target": "1734b-Y5-R2FR-Htau-first-row-component-source-pack.md",
            "script": "scripts/Y5_R2FR_Htau_first_row_component_source_pack.py",
            "objective": "turn alpha_tau and delta_H_tau curl components into source-ready nonclaim rows with unit conventions",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1733_2_later_MHref",
            "next_target": "1735-Y5-R2FR-MHref-denominator-source-pack.md",
            "script": "scripts/Y5_R2FR_MHref_denominator_source_pack.py",
            "objective": "only after current ownership improves, stage M_H_ref denominator inputs and measured-GM calibration checks",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1733_0_current_owner",
            "claim": "Theta_total/Q_tau current owner is parent-signed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "COA1733_7 owner verdict is OWNER_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1733_1_descent_current",
            "claim": "descent-current lemma is signed for current MTS",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "DCL1733_7 verdict is DESCENT_CURRENT_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1733_2_Htau_integrability",
            "claim": "H_tau is finite and integrable",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "HFR1733 rows are formal/schema-only and curl components are missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1733_3_MHref",
            "claim": "M_H_ref is a legal source denominator",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Q_tau total, H_tau and measured-GM calibration remain blocked",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1733_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no parent current owner, no H_tau integrability, no M_H_ref, no PPN/local branch pass",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "current_owner_audit": current_owner_audit_rows(),
        "descent_lemma": descent_lemma_rows(),
        "component_rows": component_rows(),
        "htau_first_rows": htau_first_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "claim_gate": claim_gate_rows(),
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1733_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1733_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def source_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text and "BLOCKED" not in row_text and "CONDITIONAL" not in row_text:
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1733_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1733_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1733*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_register = rows_map["source_register"]
    owner_rows = rows_map["current_owner_audit"]
    descent_rows = rows_map["descent_lemma"]
    component = rows_map["component_rows"]
    htau_rows = rows_map["htau_first_rows"]
    theorem = rows_map["theorem_attempt"]
    runner = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1733_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1733_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1733_2_1732_route_preserved",
            any(row["source_key"] == "1732_next_target" and row["needles_present"] == "True" for row in source_register),
            "1732 selected the Theta/Q_tau owner route",
            "1732 selected route missing",
        ),
        check(
            "VAL1733_3_owner_audit_complete",
            {row["needed_object"] for row in owner_rows}
            >= {
                "one explicit current-chain L_parent",
                "Theta_total sector split",
                "J_tau and Q_tau^MTS",
                "tau action on all parent fields",
                "B_ref and boundary representative",
                "ordinary matter/coupling descent in same current",
                "computable quotient map q and kernel Dq",
                "Theta_total/Q_tau current owner",
            },
            "owner audit covers L_parent, Theta, Noether current, tau, boundary, coupling, Dq and verdict",
            "owner audit missing required object",
        ),
        check(
            "VAL1733_4_owner_blocked",
            any(row["audit_id"] == "COA1733_7_owner_verdict" and row["current_result"] == "OWNER_NOT_SIGNED" for row in owner_rows),
            "Theta/Q_tau owner remains unsigned",
            "owner verdict missing or claim-enabled",
        ),
        check(
            "VAL1733_5_descent_lemma_contract",
            any(row["clause_id"] == "DCL1733_0_contract" and row["current_status"] == "CONDITIONAL_LEMMA_WRITTEN" for row in descent_rows)
            and any(row["clause_id"] == "DCL1733_7_verdict" and row["current_status"] == "DESCENT_CURRENT_NOT_SIGNED" for row in descent_rows),
            "descent-current lemma is written as a contract but not signed",
            "descent-current lemma contract/verdict missing",
        ),
        check(
            "VAL1733_6_component_rows_nonclaim",
            len(component) == 7 and source_rows_nonclaim(component),
            "Theta/Q_tau component rows carry blockers and remain nonclaim",
            "component rows malformed or claim-enabled",
        ),
        check(
            "VAL1733_7_htau_rows_nonclaim",
            len(htau_rows) == 3 and source_rows_nonclaim(htau_rows),
            "H_tau first rows carry blockers and remain nonclaim",
            "H_tau first rows malformed or claim-enabled",
        ),
        check(
            "VAL1733_8_theorem_fails_current_claim",
            any(row["attempt_id"] == "TQT1733_3_current_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt explicitly fails current claim",
            "theorem attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1733_9_runner_refusals_cover_chain",
            {row["quantity"] for row in runner}
            >= {"Theta_total/Q_tau current owner", "descent-current lemma", "alpha_tau and delta_H_tau_nonintegrable_over_MH", "Newton/local-GR reduction"},
            "runner refusals cover owner, descent, H_tau and local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1733_10_decision_next",
            any(row["decision_id"] == "DEC1733_2_next_bottleneck" for row in decision),
            "decision selects Dq/tau projectability as next bottleneck",
            "next bottleneck decision missing",
        ),
        check(
            "VAL1733_11_next_selected",
            any(row["route_id"] == "NEXT1733_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1734 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1733_12_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1733_13_csv_parse", parsed_ok, "all generated 1733 CSVs parse", "one or more generated 1733 CSVs failed to parse"),
        check("VAL1733_14_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1733_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1733_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1733_17_formalization_untouched", formalization_untouched(), "no 1733 outputs found under formalization-workbench", "1733 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1733_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1733 parent Theta/Q_tau current owner validation" if overall else "one or more 1733 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1733 tries to derive the parent `Theta_total/Q_tau` owner needed before `H_tau`, `M_H_ref`, or local GR can honestly score.",
        "- Current result: the exact descent-current route is now written as a crisp contract, but it is **not signed for current MTS**.",
        "- The clean law is: if `L_parent` factors through a computable quotient `q`, `tau` is projectable, vertical symplectic pieces are zero/exact, and boundary/reference data are fixed, then `Theta_total` and `Q_tau` descend without smuggling.",
        "- The current corpus still misses q/Dq, sector `L_X/Theta_X/Q_X`, boundary/reference ownership, tau projectability, and matter/coupling descent.",
        "- No `H_tau`, `M_H_ref`, R10, WEP, PPN, clock, orbital, Newton, local-GR, or `q_loc=0` claim is made.",
        "",
        "## Why This Helps",
        "This is not just another blocker ledger. It names the exact bridge we need: a parent current descent theorem. If that theorem closes, MTS can inherit the GR-style Hamiltonian charge in a disciplined way. If it does not close, the leakage becomes explicit source rows instead of being hidden in prose.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Current Owner Audit",
        markdown_table(rows_map["current_owner_audit"], ["audit_id", "needed_object", "current_result", "blocker", "valid_for_claim", "claim_allowed"]),
        "",
        "## Descent Current Lemma",
        markdown_table(rows_map["descent_lemma"], ["clause_id", "lemma_clause", "current_status", "missing_for_claim", "would_close", "valid_for_claim"]),
        "",
        "## Theta Qtau Component Rows",
        markdown_table(rows_map["component_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Htau First Rows",
        markdown_table(rows_map["htau_first_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Theorem Attempt",
        markdown_table(rows_map["theorem_attempt"], ["attempt_id", "statement", "current_status", "current_blocker", "would_close", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The route is sharper now. We are not asking 'what is Q_tau?' in the void; we are asking whether a parent current descends through `q` with a projectable observed time flow. That is exactly the Grossmann-style step: find the geometry that makes the formal current unavoidable. Next best shot is 1734: attack q/Dq plus tau projectability. If that fails, the correct fallback is a theta/Qtau leak row, not a claimed local-GR pass.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1733_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1733 validation FAIL")
    print("1733 validation PASS")


if __name__ == "__main__":
    main()
