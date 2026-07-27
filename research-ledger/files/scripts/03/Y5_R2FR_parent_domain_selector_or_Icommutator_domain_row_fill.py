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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1717"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1717 - Parent Domain Selector Or I_commutator Domain Row Fill"
UTC = datetime.now(timezone.utc).isoformat()


def f() -> str:
    return "False"


def t(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1717_0_1716_doc",
        "source_key": "1716_doc",
        "source_path": ROOT / "1716-Y5-R2FR-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md",
        "needles": ["NEXT1716_0_primary", "FPR1716_0_Icommutator_domain_row"],
    },
    {
        "source_id": "SRC1717_1_1716_validation",
        "source_key": "1716_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1716_VALIDATION.csv",
        "needles": ["VAL1716_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1717_2_1716_domain_template",
        "source_key": "1716_domain_template",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1716_ICOMMUTATOR_DOMAIN_INPUT_TEMPLATE.csv",
        "needles": ["IDR1716_0_lab_or_compact_source_placeholder", "MISSING_SOURCE_WORLDTUBE"],
    },
    {
        "source_id": "SRC1717_3_61_bound_domain",
        "source_key": "61_bound_domain",
        "source_path": ROOT / "61-bound-domain-boundary-theorem-attempt.md",
        "needles": ["parent action still has to derive the boundary/domain selector", "bound_domain_boundary_theorem_partial_volume_extremum_not_parent_action"],
    },
    {
        "source_id": "SRC1717_4_62_chiD_contract",
        "source_key": "62_chiD_contract",
        "source_path": ROOT / "62-domain-field-chiD-action-contract.md",
        "needles": ["chi_D makes the missing obligation precise", "The parent action must provide"],
    },
    {
        "source_id": "SRC1717_5_63_chiD_variation",
        "source_key": "63_chiD_variation",
        "source_path": ROOT / "63-chiD-variation-to-boundary-equation-attempt.md",
        "needles": ["minimal chi_D variations do not yet derive the local boundary", "parent-derived binding/coherence invariant"],
    },
    {
        "source_id": "SRC1717_6_64_binding_invariant",
        "source_key": "64_binding_invariant",
        "source_path": ROOT / "64-binding-invariant-domain-selector-attempt.md",
        "needles": ["not a full binding derivation", "coherent_expansion_invariant_found_not_binding_derivation"],
    },
    {
        "source_id": "SRC1717_7_602_bound_domain",
        "source_key": "602_bound_domain",
        "source_path": ROOT / "602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md",
        "needles": ["real conditional selector theorem can be written", "The derivation is not complete"],
    },
    {
        "source_id": "SRC1717_8_1009_parent_action",
        "source_key": "1009_parent_action",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_5_domain_projector_selector", "partial_clause_not_parent_closed"],
    },
    {
        "source_id": "SRC1717_9_domain_variation_chain",
        "source_key": "domain_variation_chain",
        "source_path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "needles": ["V3_Ward_force", "conditional_pass_if_local_boundary_terms_zero"],
    },
    {
        "source_id": "SRC1717_10_worldtube_clauses",
        "source_key": "worldtube_clauses",
        "source_path": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "needles": ["W504_0_worldtube_setup", "setup_allowed"],
    },
    {
        "source_id": "SRC1717_11_hilbert_worldtube_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_0_parent_worldtube_fixed", "not_derived_for_current_MTS"],
    },
    {
        "source_id": "SRC1717_12_hilbert_worldtube_certificate",
        "source_key": "hilbert_worldtube_certificate",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "needles": ["HWG535_0_worldtube_fixed_before_readout", "missing_certificate"],
    },
    {
        "source_id": "SRC1717_13_worldtube_measure_theorem",
        "source_key": "worldtube_measure_theorem",
        "source_path": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_0_EH_reference_glue", "known_GR_style_conditional_reference"],
    },
    {
        "source_id": "SRC1717_14_ppn_domain_vector",
        "source_key": "ppn_domain_vector",
        "source_path": RESIDUALS / "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
        "needles": ["RPV908_3_domain_homology_drift", "MISSING_DOMAIN_SELECTOR_THEOREM_OR_VECTOR"],
    },
    {
        "source_id": "SRC1717_15_1015_same_object",
        "source_key": "1015_same_object",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_0_domain", "conditional_reference_lemma"],
    },
]


SOURCE_PATHS_FOR_DOMAIN_ROW = ";".join(
    str(item["source_path"])
    for item in SOURCES
    if item["source_key"]
    in {
        "1716_doc",
        "domain_variation_chain",
        "worldtube_clauses",
        "hilbert_worldtube_attempt",
        "hilbert_worldtube_certificate",
        "worldtube_measure_theorem",
        "ppn_domain_vector",
        "1015_same_object",
    }
)


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
    rows = []
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
                "exists": t(exists),
                "needles_present": t(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


DOMAIN_SELECTOR_AUDIT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_0_worldtube_setup_allowed",
        "selector_clause": "compact source worldtube and exterior annulus can be named",
        "mathematical_form": "A_ext = exterior(W_M) between linked S1,S2 with no source support in A_ext",
        "evidence_anchor": "W504_0_worldtube_setup",
        "current_status": "SETUP_ALLOWED_NOT_SELECTOR",
        "derivation_status": "conditional_setup_only",
        "failure_if_missing": "inside/outside split can be chosen after readout",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_1_parent_worldtube_fixed",
        "selector_clause": "parent fixes W_M before readout",
        "mathematical_form": "W_M = supp(delta S_matter/delta e_obs) or parent source-support current before orbital/R10/PPN fitting",
        "evidence_anchor": "HWT536_0;HWG535_0;SOL1015_0",
        "current_status": "NOT_DERIVED_FOR_CURRENT_MTS",
        "derivation_status": "missing_certificate",
        "failure_if_missing": "mass charge can be selected to fit observed source normalization",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_2_chiD_contract",
        "selector_clause": "chi_D/domain field can encode the selector obligation",
        "mathematical_form": "V_D=int chi_D dSigma, Sigma_D=boundary/level set of chi_D, E_chi=delta S_D/delta chi_D=0",
        "evidence_anchor": "62-domain-field-chiD-action-contract.md",
        "current_status": "CONTRACT_WRITTEN_NOT_VARIATION_DERIVED",
        "derivation_status": "contract_only",
        "failure_if_missing": "chi_D is a rescue knob rather than a parent field",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_3_chiD_variation_failure",
        "selector_clause": "minimal chi_D advection/variation does not select the physical boundary",
        "mathematical_form": "material/advection law transports chi_D but does not choose W_M,A_ext,[S2]_M",
        "evidence_anchor": "63-chiD-variation-to-boundary-equation-attempt.md",
        "current_status": "VARIATION_INSUFFICIENT",
        "derivation_status": "failed_as_full_derivation",
        "failure_if_missing": "domain remains imposed rather than derived",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_4_binding_invariant_partial",
        "selector_clause": "binding/coherence invariant can separate local/cosmological behavior only partially",
        "mathematical_form": "coherent expansion invariant C_exp gives a kinematic separator but not a full binding/domain owner",
        "evidence_anchor": "64-binding-invariant-domain-selector-attempt.md;602-Y5-R10-bound-domain-selector",
        "current_status": "USEFUL_INVARIANT_NOT_DOMAIN_DERIVATION",
        "derivation_status": "partial_support_only",
        "failure_if_missing": "local quiet domain can still be a hand-selected closure",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_5_parent_action_clause",
        "selector_clause": "parent action sector for domain/projector selector exists as a partial clause",
        "mathematical_form": "S_selector[u,h,X,Qcoh,chi_D] must vary to Euler/topological domain selection with stress accounting",
        "evidence_anchor": "PCS1009_5_domain_projector_selector",
        "current_status": "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
        "derivation_status": "not_promoted",
        "failure_if_missing": "domain/projector stress can leak into PPN and source normalization",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_6_boundary_flux_identity",
        "selector_clause": "if local boundary terms vanish, Ward/domain force vanishes",
        "mathematical_form": "F_domain^nu = E_chi nabla^nu chi_D + E_lambda nabla^nu lambda_D + div(T_D); on shell plus no boundary flux gives F_domain^nu=0",
        "evidence_anchor": "V3_Ward_force",
        "current_status": "CONDITIONAL_PASS_IF_BOUNDARY_ZERO",
        "derivation_status": "conditional_only",
        "failure_if_missing": "domain force/source term survives as finite residual",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_7_domain_homology_observable_vector",
        "selector_clause": "domain/homology drift is already a retained local observable-source vector",
        "mathematical_form": "c_domain maps S2/domain/normal/homology variation into PPN/source-normalization residuals",
        "evidence_anchor": "RPV908_3_domain_homology_drift",
        "current_status": "MISSING_DOMAIN_SELECTOR_THEOREM_OR_VECTOR",
        "derivation_status": "retained_finite_source_channel",
        "failure_if_missing": "PPN/source-normalization claims remain blocked",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "PDS1717_8_verdict",
        "selector_clause": "parent-domain selector for W_M/A_ext/[S2]_M",
        "mathematical_form": "S_parent selects W_M,A_ext,[S2]_M before readout and makes delta W_M=delta A_ext=delta[S2]_M=0 under allowed variations",
        "evidence_anchor": "1716;61-64;602;1009;HWT536;HWG535;RPV908_3",
        "current_status": "PARENT_DOMAIN_SELECTOR_NOT_PROVED",
        "derivation_status": "fallback_to_first_Icommutator_domain_row",
        "failure_if_missing": "I_commutator_domain remains the first live source-normalization residual",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
]


CONDITIONAL_THEOREM_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "CDT1717_0_parent_selector_axiom_contract",
        "theorem_piece": "parent selector data",
        "conditional_statement": "Assume S_parent supplies D_M=(W_M,A_ext,[S2]_M,chi_D or source-support current) before readout.",
        "status": "CONDITIONAL_CONTRACT",
        "current_MTS_result": "selector data not parent-signed",
        "effect_if_signed": "domain variations become controlled objects rather than fitted choices",
        "valid_for_claim": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "CDT1717_1_fixed_domain_variation",
        "theorem_piece": "fixed domain condition",
        "conditional_statement": "If delta W_M=delta A_ext=delta[S2]_M=0 for allowed metric/readout/orbit variations, then (dPi_M)_domain=0.",
        "status": "MATHEMATICAL_CONDITIONAL",
        "current_MTS_result": "fixed-domain condition not derived",
        "effect_if_signed": "the first I_commutator_domain contribution collapses to zero",
        "valid_for_claim": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "CDT1717_2_no_defect_crossing",
        "theorem_piece": "topological stability",
        "conditional_statement": "If no defect/source support crosses A_ext and linked surfaces remain homologous, the Poincare-dual class is invariant.",
        "status": "MATHEMATICAL_CONDITIONAL",
        "current_MTS_result": "no-crossing/support theorem not parent-signed",
        "effect_if_signed": "S2/homology drift row can be theorem-zeroed",
        "valid_for_claim": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "CDT1717_3_boundary_flux_silence",
        "theorem_piece": "boundary/Ward silence",
        "conditional_statement": "If E_chi=E_lambda=0 and boundary flux vanishes, F_domain^nu=0 by the domain Ward identity.",
        "status": "CONDITIONAL_FROM_VARIATION_CHAIN",
        "current_MTS_result": "boundary no-flux and parent selector stress are unsigned",
        "effect_if_signed": "domain vector/flux/STF leakage can be removed from local source rows",
        "valid_for_claim": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "CDT1717_4_zero_law",
        "theorem_piece": "domain contribution zero law",
        "conditional_statement": "If CDT1717_0 through CDT1717_3 hold, I_commutator_domain=M_H_ref^-1 int_A (dPi_M)_domain J_H=0.",
        "status": "CONDITIONAL_ONLY_NO_CURRENT_CLAIM",
        "current_MTS_result": "antecedents missing",
        "effect_if_signed": "one source-normalization residual would close without empirical fitting",
        "valid_for_claim": f(),
    },
]


DOMAIN_ROW = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "IDR1717_0_parent_worldtube_exterior_annulus_candidate",
        "profile_id": "ICP1715_0_fixed_domain_derivative",
        "quantity": "I_commutator_domain",
        "system_id": "local_compact_source_branch_R2FR",
        "domain_id": "parent_worldtube_exterior_annulus_candidate",
        "W_M": "W_source = supp(delta S_matter/delta e_obs) or parent Hilbert source-support current; HWT536_0 says not_derived_for_current_MTS",
        "A_ext": "exterior(W_M) between linked S1,S2 with no source support; W504_0 setup_allowed",
        "S2_class": "linked homology class around W_M; Poincare-dual same-object route conditional via SOL1015_0/SOL1015_2",
        "domain_variation_parameter": "delta_D=(delta W_M, delta A_ext, delta[S2]_M) under metric/readout/orbit variations",
        "dPiM_domain_operator": "(dPi_M)_domain induced by domain/linking-surface motion; MISSING_OPERATOR_OR_ZERO_THEOREM",
        "J_H_source_current": "J_H[tau]=delta S_matter/delta e_obs contracted with tau; same-frame source measure not yet locked",
        "numerator_value": "MISSING_NUMERIC_OR_PARENT_ZERO_THEOREM",
        "numerator_units": "same_units_as_projected_source_current_integral; dimensionless after division by M_H_ref",
        "M_H_ref": "MISSING_SAME_FRAME_POSITIVE_MHREF",
        "M_H_ref_units": "MISSING_MHREF_UNITS",
        "source_path": SOURCE_PATHS_FOR_DOMAIN_ROW,
        "equation_ref": "FPR1716_0;W504_0;HWT536_0;HWG535_0;SOL1015_0;RPV908_3;V3_Ward_force",
        "no_cancellation_guard": "ABS_SUM_DOMAIN_NO_CANCELLATION_REQUIRED",
        "row_status": "SOURCE_READY_STRUCTURE_VALUE_MISSING",
        "score_ready": f(),
        "valid_for_claim": f(),
        "claim_allowed": f(),
        "generated_utc": UTC,
    }
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1717_0_parent_domain_selector",
        "quantity": "parent-domain selector W_M/A_ext/[S2]_M",
        "runner_decision": "REFUSE_CLAIM",
        "refusal_reasons": "WORLD_TUBE_SUPPORT_NOT_PARENT_SIGNED;CHI_D_CONTRACT_ONLY;BINDING_INVARIANT_PARTIAL;BOUNDARY_FLUX_UNSIGNED",
        "accepted_for_scoring": f(),
        "score_ready": f(),
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1717_1_Icommutator_domain_zero",
        "quantity": "I_commutator_domain theorem-zero",
        "runner_decision": "REFUSE_ZERO_THEOREM",
        "refusal_reasons": "CDT1717_0_TO_3_ANTECEDENTS_UNSIGNED",
        "accepted_for_scoring": f(),
        "score_ready": f(),
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1717_2_Icommutator_domain_score",
        "quantity": "source-ready I_commutator_domain row",
        "runner_decision": "REFUSE_SCORING_VALUE_MISSING",
        "refusal_reasons": "MISSING_OPERATOR_OR_ZERO_THEOREM;MISSING_NUMERIC_NUMERATOR;MISSING_MHREF;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": f(),
        "score_ready": f(),
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1717_3_Newton_GR_reopen",
        "quantity": "Newton/local-GR source normalization",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "DOMAIN_SELECTOR_UNSIGNED;I_COMMUTATOR_DOMAIN_UNSCORED;R_EQ_MISSING;M_H_REF_MISSING;PPN_DOMAIN_VECTOR_OPEN",
        "accepted_for_scoring": f(),
        "score_ready": f(),
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1717_0_primary",
        "next_target": "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md",
        "script": "scripts/Y5_R2FR_worldtube_support_owner_or_Icommutator_domain_numerator_bound.py",
        "objective": "try to parent-sign W_M as the Hilbert/source-support worldtube before readout; if not, fill a finite numerator-bound contract for I_commutator_domain",
        "selection_status": "selected",
        "success_condition": "worldtube support owner theorem or a nonclaim numerator-bound row with operator norm, J_H norm, units, and source paths",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1717_1_parallel_MHref",
        "next_target": "1718b-Y5-R2FR-MHref-same-frame-denominator-fill.md",
        "script": "scripts/Y5_R2FR_MHref_same_frame_denominator_fill.py",
        "objective": "parallel denominator route once a numerator row exists",
        "selection_status": "held_until_numerator_exists",
        "success_condition": "positive same-frame M_H_ref with no orbital-GM import",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1717_0_parent_domain_selector",
        "claim": "parent action fixes W_M/A_ext/[S2]_M before readout",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "worldtube support, chi_D selector, binding invariant, and boundary/no-flux clauses remain conditional",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1717_1_Icommutator_domain_zero",
        "claim": "I_commutator_domain = 0",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "conditional zero law has unsigned antecedents",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1717_2_Icommutator_domain_score",
        "claim": "first I_commutator_domain row is score-ready",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "source-ready structure exists but numerator/operator/M_H_ref values are missing",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1717_3_Newton_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "domain selector, I_commutator_domain, R_eq, M_H_ref and PPN domain vector remain open",
        "valid_for_claim": f(),
        "claim_allowed": f(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_SOURCE_REGISTER.csv",
    "selector_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_PARENT_DOMAIN_SELECTOR_AUDIT.csv",
    "conditional_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_CONDITIONAL_DOMAIN_ZERO_THEOREM.csv",
    "domain_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_ICOMMUTATOR_DOMAIN_FIRST_SOURCE_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_RUNNER_REFUSAL.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1717_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1717_VALIDATION.csv",
}


COPY_MAP = {
    "selector_audit": "R2FR_parent_domain_selector_audit_1717.csv",
    "conditional_theorem": "R2FR_conditional_domain_zero_theorem_1717.csv",
    "domain_row": "R2FR_Icommutator_domain_first_source_row_1717.csv",
    "runner_refusal": "R2FR_runner_refusal_1717.csv",
    "next_target": "R2FR_next_target_1717.csv",
    "claim_gate": "R2FR_claim_gate_1717.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "selector_audit": DOMAIN_SELECTOR_AUDIT_ROWS,
        "conditional_theorem": CONDITIONAL_THEOREM_ROWS,
        "domain_row": DOMAIN_ROW,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1717_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1717_{key.upper()}.csv")


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


def domain_row_source_paths_exist() -> bool:
    row = DOMAIN_ROW[0]
    paths = [Path(item) for item in row["source_path"].split(";") if item]
    return bool(paths) and all(path.exists() for path in paths)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1717*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1717_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1717_{key.upper()}.csv").exists():
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

    source_rows = rows_map["source_register"]
    selector_rows = rows_map["selector_audit"]
    theorem_rows = rows_map["conditional_theorem"]
    domain_rows = rows_map["domain_row"]
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
            "VAL1717_0_sources_exist",
            all(row["exists"] == "True" for row in source_rows),
            "all cited source paths exist",
            "one or more cited source paths missing",
        ),
        check(
            "VAL1717_1_needles_present",
            all(row["needles_present"] == "True" for row in source_rows),
            "required source needles are present",
            "one or more required source needles missing",
        ),
        check(
            "VAL1717_2_selector_not_proved",
            any(row["audit_id"] == "PDS1717_8_verdict" and row["current_status"] == "PARENT_DOMAIN_SELECTOR_NOT_PROVED" for row in selector_rows),
            "parent-domain selector remains unproved",
            "selector verdict missing or promoted",
        ),
        check(
            "VAL1717_3_conditional_zero_law_only",
            any(row["theorem_id"] == "CDT1717_4_zero_law" and row["status"] == "CONDITIONAL_ONLY_NO_CURRENT_CLAIM" for row in theorem_rows),
            "domain zero law retained only as conditional theorem",
            "domain zero law missing or promoted",
        ),
        check(
            "VAL1717_4_first_domain_row_source_ready_nonclaim",
            any(row["row_id"] == "IDR1717_0_parent_worldtube_exterior_annulus_candidate" and row["row_status"] == "SOURCE_READY_STRUCTURE_VALUE_MISSING" and row["valid_for_claim"] == "False" for row in domain_rows),
            "first I_commutator_domain row has real source paths but remains nonclaim",
            "first I_commutator_domain source row missing or claim-enabled",
        ),
        check(
            "VAL1717_5_domain_row_source_paths_exist",
            domain_row_source_paths_exist(),
            "all source paths listed in the first domain row exist",
            "one or more source paths listed in the first domain row missing",
        ),
        check(
            "VAL1717_6_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses selector, zero, scoring and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1717_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check(
            "VAL1717_8_next_selected",
            any(row["route_id"] == "NEXT1717_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects worldtube-support owner or numerator-bound route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1717_9_csv_parse",
            parsed_ok,
            "all generated 1717 CSVs parse",
            "one or more generated 1717 CSVs failed to parse",
        ),
        check(
            "VAL1717_10_no_claim_flags",
            no_claim_flags(rows_map),
            "all generated scoring and claim flags remain false",
            "one or more generated flags enabled a claim",
        ),
        check(
            "VAL1717_11_branch_copies",
            branch_copies_exist(),
            "branch/quarantine/queue copies exist",
            "one or more branch/quarantine/queue copies missing",
        ),
        check(
            "VAL1717_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
            "scripts __pycache__ still exists",
        ),
        check(
            "VAL1717_13_formalization_untouched",
            formalization_untouched(),
            "no 1717 outputs found under formalization-workbench",
            "1717 output leaked into formalization-workbench",
        ),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1717_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1717 parent-domain selector and I_commutator_domain first-row validation"
            if overall
            else "one or more 1717 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1717 tries the derivation path first: derive the parent selector for `W_M`, `A_ext`, and `[S2]_M`.",
        "- The best available theorem is conditional: fixed parent worldtube/support plus no defect crossing and no boundary flux would make `(dPi_M)_domain=0`.",
        "- Current MTS still does not parent-sign that selector. `chi_D`, `N_D`, coherent expansion, and worldtube support are useful contracts, not a completed derivation.",
        "- The first `I_commutator_domain` row is now source-ready in structure: it names the candidate worldtube, annulus, linking class, operator, source current, units, source paths, and missing numerator/denominator.",
        "- No Newton, local-GR, R10, PPN, clock, orbital, source-normalization or `q_loc`-zero claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Parent Domain Selector Audit",
        markdown_table(
            rows_map["selector_audit"],
            ["audit_id", "selector_clause", "mathematical_form", "current_status", "derivation_status", "failure_if_missing"],
        ),
        "",
        "## Conditional Domain Zero Theorem",
        markdown_table(
            rows_map["conditional_theorem"],
            ["theorem_id", "theorem_piece", "conditional_statement", "status", "current_MTS_result", "effect_if_signed"],
        ),
        "",
        "## First I_commutator Domain Source Row",
        markdown_table(
            rows_map["domain_row"],
            [
                "row_id",
                "system_id",
                "domain_id",
                "W_M",
                "A_ext",
                "S2_class",
                "dPiM_domain_operator",
                "numerator_value",
                "M_H_ref",
                "row_status",
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
        "This moves the problem from a vague `domain selector missing` complaint to a concrete fork. The clean derivation route is now: prove the parent action owns the Hilbert/source-support worldtube before readout. If that proof fails, the first finite residual is no longer mysterious: it is the domain/linking-surface contribution to `I_commutator`, with numerator and same-frame `M_H_ref` still missing.",
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
    doc_path = ROOT / "1717-Y5-R2FR-parent-domain-selector-or-Icommutator-domain-row-fill.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1717_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1717 validation FAIL")
    print("1717 validation PASS")


if __name__ == "__main__":
    main()
