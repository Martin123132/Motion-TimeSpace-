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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1716"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1716 - PiM Fixed Chainmap Parent Signature Or I_commutator First Profile Row"
UTC = datetime.now(timezone.utc).isoformat()


SOURCES = [
    {
        "source_id": "SRC1716_0_1715_doc",
        "source_key": "1715_doc",
        "source_path": ROOT / "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
        "needles": ["Current MTS does not sign the parent prerequisites", "NEXT1715_0_primary"],
    },
    {
        "source_id": "SRC1716_1_1715_validation",
        "source_key": "1715_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1715_VALIDATION.csv",
        "needles": ["VAL1715_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1716_2_1715_signature_requirements",
        "source_key": "1715_signature_requirements",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1715_PARENT_SIGNATURE_REQUIREMENTS.csv",
        "needles": ["SIG1715_0_parent_selector", "SIG1715_6_tau_MHref_lock"],
    },
    {
        "source_id": "SRC1716_3_1715_profile_rows",
        "source_key": "1715_profile_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1715_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
        "needles": ["ICP1715_0_fixed_domain_derivative", "RETAINED_NONCLAIM"],
    },
    {
        "source_id": "SRC1716_4_1715_claim_gate",
        "source_key": "1715_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1715_CLAIM_GATE.csv",
        "needles": ["CG1715_1_parent_chainmap_signed", "BLOCKED_NO_CLAIM"],
    },
    {
        "source_id": "SRC1716_5_1017_doc",
        "source_key": "1017_doc",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HRL1017_4_tau_lock", "HRL1017_5_MHref_denominator"],
    },
    {
        "source_id": "SRC1716_6_1017_reference_lock",
        "source_key": "1017_reference_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
        "needles": ["HRL1017_4_tau_lock", "fail_current_claim"],
    },
    {
        "source_id": "SRC1716_7_1652_MHref_refusal",
        "source_key": "1652_MHref_refusal",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_MHref_source_measure_refusal_runner_nonclaim_1652.csv",
        "needles": ["RUN1652_0_MHref", "NO_ORBITAL_GM_IMPORT"],
    },
    {
        "source_id": "SRC1716_8_1653_source_owner_gate",
        "source_key": "1653_source_owner_gate",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_source_measure_owner_gate_nonclaim_1653.csv",
        "needles": ["SMO1653_1_PiM_owner", "MISSING_PIM_OWNER"],
    },
    {
        "source_id": "SRC1716_9_1654_projector_owner_gate",
        "source_key": "1654_projector_owner_gate",
        "source_path": MICROSCOPE_RESIDUALS / "R2FR_PiM_Ploc_owner_gate_nonclaim_1654.csv",
        "needles": ["POG1654_1_PiM_chain_map", "NOT_PARENT_DERIVED"],
    },
]


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def false_text() -> str:
    return "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


SIGNATURE_AUDIT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_0_parent_selector",
        "parent_clause": "parent selects the topological mass channel before readout",
        "minimal_condition": "S_parent supplies chi_M or ell_M and compact source support W_M before any orbit/R10/PPN scoring",
        "source_anchor": "SIG1715_0_parent_selector;SMO1653_1_PiM_owner",
        "current_status": "MISSING_PARENT_SELECTOR",
        "can_sign_now": false_text(),
        "missing_inputs": "parent selector equation; topological channel definition; no post-readout mask certificate",
        "effect": "Pi_M ownership remains adjustable and cannot zero I_commutator",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_1_fixed_domain",
        "parent_clause": "source worldtube, exterior annulus and linking surface are fixed by the parent branch",
        "minimal_condition": "delta W_M=0, delta A_ext=0, delta[S2]_M=0 under metric/readout/orbit variations",
        "source_anchor": "SIG1715_1_fixed_domain;POG1654_0_parent_domain",
        "current_status": "MISSING_FIXED_DOMAIN_OWNER",
        "can_sign_now": false_text(),
        "missing_inputs": "domain selector; boundary class; radial/deformation silence theorem",
        "effect": "domain derivative term is the first concrete I_commutator row",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_2_metric_independent_representative",
        "parent_clause": "Pi_M representative is topological and metric-independent",
        "minimal_condition": "Pi_M J=ell_M(J) omega_M_top, d omega_M_top=0, integral_link omega_M_top=1, delta_g omega_M_top=0",
        "source_anchor": "SIG1715_2_metric_independent_representative",
        "current_status": "CONDITIONAL_TEMPLATE_ONLY",
        "can_sign_now": false_text(),
        "missing_inputs": "parent-normalized representative; metric-variation silence certificate",
        "effect": "Hodge/projector-stress row remains live",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_3_chainmap_on_current_complex",
        "parent_clause": "Pi_M is a chain-map on the physical Hilbert-current complex",
        "minimal_condition": "d(Pi_M J)=Pi_M dJ for every physical J in C_H(W_M,A_ext)",
        "source_anchor": "SIG1715_3_chainmap_proof;POG1654_1_PiM_chain_map",
        "current_status": "CONDITIONAL_MATH_ONLY",
        "can_sign_now": false_text(),
        "missing_inputs": "physical current complex; parent ownership of Pi_M; allowed-current theorem",
        "effect": "conditional lemma is retained but cannot be applied to live source rows",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_4_physical_current_membership",
        "parent_clause": "J_H and all source/frame/species channels lie in the fixed complex or theorem-zero outside it",
        "minimal_condition": "J_H[e_obs,tau] plus extra/source/species/frame pieces belong to C_H(W_M,A_ext)",
        "source_anchor": "SIG1715_4_physical_current_lock;SMO1653_3_commutator_closure",
        "current_status": "MISSING_CURRENT_DOMAIN_LOCK",
        "can_sign_now": false_text(),
        "missing_inputs": "Hilbert-current decomposition; species/material inclusion; frame-source theorem",
        "effect": "current-domain escape row remains live",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_5_exterior_silence",
        "parent_clause": "compact exterior annulus has no hidden source, anomaly, boundary or projector support",
        "minimal_condition": "support(dPi_M), support(A_parent), support(B_flux), support(J_extra) absent from A_ext or theorem-zero",
        "source_anchor": "SIG1715_5_exterior_silence",
        "current_status": "MISSING_EXTERIOR_SILENCE_THEOREM",
        "can_sign_now": false_text(),
        "missing_inputs": "no-hair/boundary theorem; anomaly operator silence; exterior support certificate",
        "effect": "boundary/anomaly source-profile rows remain live",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_6_tau_MHref_lock",
        "parent_clause": "same time generator and same-frame positive denominator normalize the projected source",
        "minimal_condition": "tau_source=tau_charge=tau_clock=tau_readout and M_H_ref>0 in the same observed frame",
        "source_anchor": "SIG1715_6_tau_MHref_lock;HRL1017_4_tau_lock;HRL1017_5_MHref_denominator;RUN1652_0_MHref",
        "current_status": "MISSING_TAU_MHREF_DENOMINATOR",
        "can_sign_now": false_text(),
        "missing_inputs": "tau lock; Hamiltonian integrability; positive source denominator; no orbital-GM import",
        "effect": "even a finite numerator cannot be score-ready yet",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "clause_id": "FCS1716_7_verdict",
        "parent_clause": "current MTS parent-signs the fixed chain-map theorem for Pi_M",
        "minimal_condition": "all FCS1716_0 through FCS1716_6 are parent-signed or source-backed",
        "source_anchor": "1715 claim gate and 1652-1654 owner gates",
        "current_status": "PARENT_CHAINMAP_NOT_SIGNED",
        "can_sign_now": false_text(),
        "missing_inputs": "selector; fixed domain; metric-independent representative; current complex; exterior silence; tau/M_H_ref",
        "effect": "route demotes to first I_commutator_domain profile row without scoring",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
]


THEOREM_CONTRACT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_0_parent_data",
        "contract_piece": "parent data package",
        "formal_requirement": "D_M=(W_M,A_ext,[S2]_M,ell_M,omega_M_top,tau,M_H_ref) is selected by S_parent before readout",
        "proof_status": "OPEN",
        "current_use": "contract only",
        "why_not_enough": "no parent selector equation or tau/M_H_ref denominator proof exists",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_1_fixed_complex",
        "contract_piece": "fixed source-current complex",
        "formal_requirement": "C_H(W_M,A_ext) is invariant under the variations used in source/orbit/readout comparisons",
        "proof_status": "OPEN",
        "current_use": "contract only",
        "why_not_enough": "domain and physical-current membership remain unsigned",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_2_topological_projector",
        "contract_piece": "metric-silent Pi_M",
        "formal_requirement": "Pi_M J = ell_M(J) omega_M_top with d omega_M_top=0 and delta_g Pi_M=0",
        "proof_status": "CONDITIONAL_TEMPLATE",
        "current_use": "allowed mathematical form",
        "why_not_enough": "template is not parent-owned or tied to physical J_H",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_3_chainmap_identity",
        "contract_piece": "chain-map identity",
        "formal_requirement": "d(Pi_M J)=Pi_M dJ for every allowed physical current J",
        "proof_status": "CONDITIONAL_LEMMA",
        "current_use": "derivation target",
        "why_not_enough": "allowed-current domain is not yet the live Hilbert current domain",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_4_exterior_closure",
        "contract_piece": "source-free exterior annulus",
        "formal_requirement": "dJ_H=0 and no anomaly/boundary/operator support in A_ext except theorem-zero exact pieces",
        "proof_status": "OPEN",
        "current_use": "contract only",
        "why_not_enough": "boundary/anomaly/source-measure channels remain live",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_5_conditional_zero_theorem",
        "contract_piece": "conditional commutator zero",
        "formal_requirement": "If TCC1716_0 through TCC1716_4 hold, then I_commutator = M_H_ref^-1 int_A [d,Pi_M]J_H = 0",
        "proof_status": "CONDITIONAL_ONLY",
        "current_use": "clean target theorem",
        "why_not_enough": "antecedents are not signed by current MTS",
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "TCC1716_6_current_verdict",
        "contract_piece": "live branch status",
        "formal_requirement": "Apply conditional theorem to physical source rows",
        "proof_status": "NOT_PROVED_FOR_CURRENT_MTS",
        "current_use": "fall back to source-profile acquisition",
        "why_not_enough": "FCS1716_7 remains false",
        "valid_for_claim": false_text(),
    },
]


FIRST_PROFILE_SCHEMA_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "schema_id": "FPR1716_0_Icommutator_domain_row",
        "profile_id": "ICP1715_0_fixed_domain_derivative",
        "quantity": "I_commutator_domain",
        "arena": "local_source_exterior_annulus",
        "formula": "I_commutator_domain = M_H_ref^-1 int_{A_ext} (dPi_M)_domain J_H",
        "required_fields": "system_id;domain_id;W_M;A_ext;S2_class;domain_variation_parameter;dPiM_domain_operator;J_H_source_current;numerator_value;numerator_units;M_H_ref;M_H_ref_units;source_path;equation_ref;no_cancellation_guard;valid_for_claim",
        "current_row_status": "TEMPLATE_ONLY_ALL_PHYSICAL_VALUES_MISSING",
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
        "next_fill_action": "either parent-prove delta W_M=delta A_ext=delta[S2]_M=0 or fill a finite source-backed numerator row with units and same-frame M_H_ref",
    },
    {
        "branch_id": BRANCH_ID,
        "schema_id": "FPR1716_1_zero_route",
        "profile_id": "ICP1715_0_fixed_domain_derivative",
        "quantity": "domain_zero_theorem",
        "arena": "parent_fixed_domain",
        "formula": "delta W_M=0 and delta A_ext=0 and delta[S2]_M=0 implies (dPi_M)_domain=0",
        "required_fields": "parent_domain_selector;boundary_class_certificate;radial_deformation_silence;source_path;equation_ref",
        "current_row_status": "MISSING_PARENT_DOMAIN_SELECTOR",
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
        "next_fill_action": "hunt for parent domain selector before any numeric scoring",
    },
    {
        "branch_id": BRANCH_ID,
        "schema_id": "FPR1716_2_finite_bound_route",
        "profile_id": "ICP1715_0_fixed_domain_derivative",
        "quantity": "finite_domain_bound",
        "arena": "empirical_or_constructive_bound",
        "formula": "abs(I_commutator_domain) <= abs(int_A (dPi_M)_domain J_H)/M_H_ref",
        "required_fields": "operator_norm_bound;source_current_norm;annulus_measure;M_H_ref;units;source_path;no_cancellation_guard",
        "current_row_status": "MISSING_NUMERIC_BOUND_AND_DENOMINATOR",
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
        "next_fill_action": "only use if zero theorem fails and all numerator/denominator units become source-backed",
    },
]


DOMAIN_INPUT_TEMPLATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "IDR1716_0_lab_or_compact_source_placeholder",
        "system_id": "MISSING_SYSTEM_ID",
        "domain_id": "MISSING_DOMAIN_ID",
        "W_M": "MISSING_SOURCE_WORLDTUBE",
        "A_ext": "MISSING_EXTERIOR_ANNULUS",
        "S2_class": "MISSING_LINKING_SURFACE_CLASS",
        "domain_variation_parameter": "MISSING_VARIATION_PARAMETER",
        "dPiM_domain_operator": "MISSING_OPERATOR_OR_ZERO_THEOREM",
        "J_H_source_current": "MISSING_HILBERT_CURRENT_SOURCE",
        "numerator_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "numerator_units": "MISSING_UNITS",
        "M_H_ref": "MISSING_SAME_FRAME_POSITIVE_MHREF",
        "M_H_ref_units": "MISSING_MHREF_UNITS",
        "source_path": "MISSING_EXISTING_SOURCE_PATH",
        "equation_ref": "MISSING_EQUATION_REF",
        "no_cancellation_guard": "MISSING_ABS_SUM_GUARD",
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
        "generated_utc": UTC,
    }
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1716_0_parent_chainmap",
        "quantity": "parent-signed Pi_M fixed chain-map theorem",
        "runner_decision": "REFUSE_CLAIM",
        "refusal_reasons": "MISSING_PARENT_SELECTOR;MISSING_FIXED_DOMAIN_OWNER;MISSING_CURRENT_DOMAIN_LOCK;MISSING_EXTERIOR_SILENCE;MISSING_TAU_MHREF_DENOMINATOR",
        "accepted_for_scoring": false_text(),
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1716_1_Icommutator_domain_zero",
        "quantity": "I_commutator_domain zero theorem",
        "runner_decision": "REFUSE_ZERO_THEOREM",
        "refusal_reasons": "DOMAIN_SELECTOR_UNSIGNED;BOUNDARY_CLASS_UNSIGNED;RADIAL_DEFORMATION_SILENCE_UNSIGNED",
        "accepted_for_scoring": false_text(),
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1716_2_Icommutator_domain_finite_score",
        "quantity": "I_commutator_domain finite bound row",
        "runner_decision": "REFUSE_SCORING_TEMPLATE_ONLY",
        "refusal_reasons": "MISSING_NUMERATOR;MISSING_OPERATOR_NORM;MISSING_JH_SOURCE;MISSING_UNITS;MISSING_MHREF;MISSING_SOURCE_PATH;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": false_text(),
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1716_3_Newton_GR_reopen",
        "quantity": "Newton/local-GR source normalization from Pi_M route",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "PARENT_CHAINMAP_UNSIGNED;I_COMMUTATOR_DOMAIN_UNFILLED;R_EQ_MISSING;M_H_REF_MISSING;CALIBRATION_TAIL_OPEN",
        "accepted_for_scoring": false_text(),
        "score_ready": false_text(),
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1716_0_primary",
        "next_target": "1717-Y5-R2FR-parent-domain-selector-or-Icommutator-domain-row-fill.md",
        "script": "scripts/Y5_R2FR_parent_domain_selector_or_Icommutator_domain_row_fill.py",
        "objective": "try to prove the parent fixed-domain selector for W_M/A_ext/[S2]_M; if not, fill the first source-ready I_commutator_domain row without scoring",
        "selection_status": "selected",
        "success_condition": "either delta-domain theorem is parent-signed, or the domain profile row has explicit numerator, units, source path and same-frame M_H_ref requirements still marked nonclaim",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1716_1_parallel_MHref",
        "next_target": "1716c-Y5-R2FR-MHref-denominator-source-intake.md",
        "script": "scripts/Y5_R2FR_MHref_denominator_source_intake.py",
        "objective": "parallel denominator route if finite I_commutator scoring becomes unavoidable",
        "selection_status": "held_until_domain_row_needs_denominator",
        "success_condition": "same-frame positive M_H_ref row with no orbital-GM import",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1716_2_parallel_Req",
        "next_target": "1716b-Y5-R2FR-R_eq-bound-input-row-or-topological-Hilbert-equality-contract.md",
        "script": "scripts/Y5_R2FR_R_eq_bound_input_row_or_topological_Hilbert_equality_contract.py",
        "objective": "parallel source equality route remains secondary until Pi_M domain ownership is clearer",
        "selection_status": "held_parallel",
        "success_condition": "R_eq theorem-zero or finite source-backed bound row",
        "valid_for_claim": false_text(),
        "claim_allowed": false_text(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1716_0_parent_chainmap_signed",
        "claim": "current MTS parent-signs fixed-domain metric-independent Pi_M as a chain-map on physical J_H",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "FCS1716_7 is false; selector/domain/current/exterior/tau-MHref locks remain missing",
        "claim_allowed": false_text(),
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1716_1_Icommutator_domain_zero",
        "claim": "domain contribution to I_commutator is theorem-zero",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "fixed-domain selector and boundary/radial silence theorem are unsigned",
        "claim_allowed": false_text(),
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1716_2_Icommutator_domain_score",
        "claim": "first I_commutator_domain profile row is numeric/source-backed and score-ready",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "template has MISSING numerator, units, source path and same-frame M_H_ref",
        "claim_allowed": false_text(),
        "valid_for_claim": false_text(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1716_3_Newton_GR",
        "claim": "Newton/local-GR source-normalization gates can reopen from Pi_M chainmap route",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "Pi_M ownership, I_commutator_domain, R_eq, M_H_ref and calibration tail remain open",
        "claim_allowed": false_text(),
        "valid_for_claim": false_text(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_SOURCE_REGISTER.csv",
    "signature_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_FIXED_CHAINMAP_PARENT_SIGNATURE_AUDIT.csv",
    "theorem_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_FIXED_CHAINMAP_THEOREM_CONTRACT.csv",
    "profile_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_ICOMMUTATOR_DOMAIN_FIRST_PROFILE_SCHEMA.csv",
    "domain_template": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_ICOMMUTATOR_DOMAIN_INPUT_TEMPLATE.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_RUNNER_REFUSAL.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1716_VALIDATION.csv",
}


COPY_MAP = {
    "signature_audit": "R2FR_fixed_chainmap_parent_signature_audit_1716.csv",
    "theorem_contract": "R2FR_fixed_chainmap_theorem_contract_1716.csv",
    "profile_schema": "R2FR_Icommutator_domain_first_profile_schema_1716.csv",
    "domain_template": "R2FR_Icommutator_domain_input_template_1716.csv",
    "runner_refusal": "R2FR_runner_refusal_1716.csv",
    "next_target": "R2FR_next_target_1716.csv",
    "claim_gate": "R2FR_claim_gate_1716.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "signature_audit": SIGNATURE_AUDIT_ROWS,
        "theorem_contract": THEOREM_CONTRACT_ROWS,
        "profile_schema": FIRST_PROFILE_SCHEMA_ROWS,
        "domain_template": DOMAIN_INPUT_TEMPLATE_ROWS,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, filename in COPY_MAP.items():
        source = OUTPUTS[key]
        shutil.copy2(source, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(source, RAB_QUEUE / f"JR1716_{key.upper()}.csv")
        shutil.copy2(source, QUARANTINE / filename)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1716_SOURCE_REGISTER.csv")


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    false_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "can_sign_now",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in false_fields and str(value).lower() != "false":
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1716*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def branch_copies_exist() -> bool:
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1716_{key.upper()}.csv").exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
    return (QUARANTINE / "P8_Y5_PARENT_QLOC_1716_SOURCE_REGISTER.csv").exists()


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_rows = rows_map["source_register"]
    signature_rows = rows_map["signature_audit"]
    contract_rows = rows_map["theorem_contract"]
    schema_rows = rows_map["profile_schema"]
    template_rows = rows_map["domain_template"]
    runner_rows = rows_map["runner_refusal"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check(
            "VAL1716_0_sources_exist",
            all(row["exists"] == "True" for row in source_rows),
            "all cited source paths exist",
            "one or more cited source paths missing",
        ),
        check(
            "VAL1716_1_needles_present",
            all(row["needles_present"] == "True" for row in source_rows),
            "required source needles are present",
            "one or more required source needles missing",
        ),
        check(
            "VAL1716_2_parent_chainmap_not_signed",
            any(row["clause_id"] == "FCS1716_7_verdict" and row["current_status"] == "PARENT_CHAINMAP_NOT_SIGNED" and row["can_sign_now"] == "False" for row in signature_rows),
            "parent chain-map theorem remains unclaimed for current MTS",
            "parent chain-map theorem was promoted or verdict row missing",
        ),
        check(
            "VAL1716_3_all_signature_clauses_nonclaim",
            all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in signature_rows),
            "all parent-signature audit rows remain nonclaim",
            "signature audit contains a claim-enabled row",
        ),
        check(
            "VAL1716_4_conditional_theorem_retained",
            any(row["contract_id"] == "TCC1716_5_conditional_zero_theorem" and row["proof_status"] == "CONDITIONAL_ONLY" for row in contract_rows),
            "conditional fixed-chainmap theorem is retained without promotion",
            "conditional theorem row missing or promoted",
        ),
        check(
            "VAL1716_5_domain_profile_schema_present",
            any(row["schema_id"] == "FPR1716_0_Icommutator_domain_row" and row["score_ready"] == "False" for row in schema_rows),
            "first I_commutator_domain profile schema is present and unscored",
            "first domain profile schema missing or score-ready",
        ),
        check(
            "VAL1716_6_domain_template_nonclaim",
            all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" and "MISSING" in row["source_path"] for row in template_rows),
            "domain input template keeps missing values and valid_for_claim=false",
            "domain input template contains claim-ready or sourced-looking row",
        ),
        check(
            "VAL1716_7_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses chainmap, zero, scoring and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1716_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check(
            "VAL1716_9_next_selected",
            any(row["route_id"] == "NEXT1716_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects parent-domain selector or I_commutator_domain row fill",
            "next target missing selected primary route",
        ),
        check(
            "VAL1716_10_csv_parse",
            parsed_ok,
            "all generated 1716 CSVs parse",
            "one or more generated 1716 CSVs failed to parse",
        ),
        check(
            "VAL1716_11_no_claim_flags",
            no_claim_flags(rows_map),
            "all generated scoring and claim flags remain false",
            "one or more generated flags enabled a claim",
        ),
        check(
            "VAL1716_12_branch_copies",
            branch_copies_exist(),
            "branch/quarantine/queue copies exist",
            "one or more branch/quarantine/queue copies missing",
        ),
        check(
            "VAL1716_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
            "scripts __pycache__ still exists",
        ),
        check(
            "VAL1716_14_formalization_untouched",
            formalization_untouched(),
            "no 1716 outputs found under formalization-workbench",
            "1716 output leaked into formalization-workbench",
        ),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1716_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1716 fixed-chainmap parent signature and I_commutator_domain first-profile validation"
            if overall
            else "one or more 1716 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1716 tries the derivation path first: parent-sign the fixed-domain, metric-independent `Pi_M` chain-map theorem.",
        "- The clean theorem survives as a conditional contract, but current MTS still does not sign the selector, fixed domain, physical-current complex, exterior silence, or tau/`M_H_ref` denominator.",
        "- Therefore `[d,Pi_M]J_H=0` is not claimed for the physical source current.",
        "- The honest fallback is now explicit: fill the first `I_commutator_domain` profile row, starting with the domain/linking-surface derivative.",
        "- No Newton, local-GR, R10, PPN, clock, orbital, source-normalization or `q_loc`-zero claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Fixed Chainmap Parent-Signature Audit",
        markdown_table(
            rows_map["signature_audit"],
            ["clause_id", "parent_clause", "minimal_condition", "current_status", "can_sign_now", "effect"],
        ),
        "",
        "## Fixed Chainmap Theorem Contract",
        markdown_table(
            rows_map["theorem_contract"],
            ["contract_id", "contract_piece", "formal_requirement", "proof_status", "current_use", "why_not_enough"],
        ),
        "",
        "## First I_commutator Domain Profile Schema",
        markdown_table(
            rows_map["profile_schema"],
            ["schema_id", "profile_id", "quantity", "formula", "current_row_status", "score_ready", "next_fill_action"],
        ),
        "",
        "## I_commutator Domain Input Template",
        markdown_table(
            rows_map["domain_template"],
            [
                "row_id",
                "system_id",
                "domain_id",
                "W_M",
                "A_ext",
                "S2_class",
                "dPiM_domain_operator",
                "J_H_source_current",
                "M_H_ref",
                "source_path",
                "valid_for_claim",
            ],
        ),
        "",
        "## Runner Refusal",
        markdown_table(
            rows_map["runner_refusal"],
            ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"],
        ),
        "",
        "## Next Target",
        markdown_table(
            rows_map["next_target"],
            ["route_id", "next_target", "script", "objective", "selection_status"],
        ),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1716 is not a failure; it narrows the fight. The fixed-chainmap route is mathematically respectable, but it demands parent ownership of the topological selector and source domain. The next useful derivation target is the domain selector itself: if the parent action fixes `W_M`, `A_ext`, and `[S2]_M`, the first commutator profile row can collapse to zero. If not, the same row becomes the first finite residual we must source and bound.",
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
    doc_path = ROOT / "1716-Y5-R2FR-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1716_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1716 validation FAIL")
    print("1716 validation PASS")


if __name__ == "__main__":
    main()
