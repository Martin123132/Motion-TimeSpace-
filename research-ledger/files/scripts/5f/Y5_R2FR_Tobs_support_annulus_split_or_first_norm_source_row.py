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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1730"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1730 - Tobs Support Annulus Split Or First Norm Source Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1730_0_1729_doc",
        "source_key": "1729_doc",
        "source_path": ROOT / "1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md",
        "needles": ["NEXT1729_0_primary", "support-annulus"],
    },
    {
        "source_id": "SRC1730_1_1729_next",
        "source_key": "1729_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_NEXT_TARGET.csv",
        "needles": ["1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md", "selected"],
    },
    {
        "source_id": "SRC1730_2_1729_C_Tobs",
        "source_key": "1729_C_Tobs_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv",
        "needles": ["CTT1729_3_vacuum_annulus_zero_candidate", "MISSING_A_EXT_SUPPORT_SPLIT"],
    },
    {
        "source_id": "SRC1730_3_1724_annulus_audit",
        "source_key": "1724_annulus_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv",
        "needles": ["ANT1724_2_compact_annulus", "COMPACT_ANNULUS_NOT_PARENT_OWNED"],
    },
    {
        "source_id": "SRC1730_4_1016_selector_contract",
        "source_key": "1016_selector_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv",
        "needles": ["PSC1016_3_support_selector", "formal_selector_definition_available_conditional"],
    },
    {
        "source_id": "SRC1730_5_1016_selector_attempt",
        "source_key": "1016_selector_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["PST1016_0_selector_lemma", "conditional_lemma_pass"],
    },
    {
        "source_id": "SRC1730_6_1016_claim_gate",
        "source_key": "1016_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1016_CLAIM_GATE.csv",
        "needles": ["CG1016_1_selector_lemma_claim", "parent action"],
    },
    {
        "source_id": "SRC1730_7_662_parent_clauses",
        "source_key": "662_parent_clause_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
        "needles": ["CL662_2_parent_fixed_worldtube", "not_yet_derived"],
    },
    {
        "source_id": "SRC1730_8_662_bound_template",
        "source_key": "662_bound_input_template",
        "source_path": RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
        "needles": ["BI662_3_boundary_reference_flux", "MISSING_BOUNDARY_REFERENCE_INPUT"],
    },
    {
        "source_id": "SRC1730_9_1720_JH_row",
        "source_key": "1720_JH_norm_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_COMPACT_EXTERIOR_ANNULUS"],
    },
    {
        "source_id": "SRC1730_10_1719_ingredients",
        "source_key": "1719_JH_ingredient",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
        "needles": ["ING1719_0_JH_norm_candidate", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1730_11_683_same_frame",
        "source_key": "683_same_frame_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
        "needles": ["SFG683_1_coframe_lock", "MISSING_SAME_FRAME_MEASURE_PROOF"],
    },
    {
        "source_id": "SRC1730_12_1729_validation",
        "source_key": "1729_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1729_VALIDATION.csv",
        "needles": ["VAL1729_OVERALL", "PASS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_SOURCE_REGISTER.csv",
    "annulus_support_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_ANNULUS_SUPPORT_AUDIT.csv",
    "conditional_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_TOBS_VACUUM_ANNULUS_THEOREM.csv",
    "norm_source_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_TOBS_NORM_SOURCE_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1730_VALIDATION.csv",
}


COPY_MAP = {
    "annulus_support_audit": "R2FR_1730_ANNULUS_SUPPORT_AUDIT.csv",
    "conditional_theorem": "R2FR_1730_TOBS_VACUUM_ANNULUS_THEOREM.csv",
    "norm_source_rows": "R2FR_1730_TOBS_NORM_SOURCE_ROWS.csv",
    "runner_refusal": "R2FR_1730_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1730_DECISION_LEDGER.csv",
    "next_target": "R2FR_1730_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1730_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        text = source_path.read_text(encoding="utf-8", errors="replace") if source_path.exists() else ""
        needles_present = all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(source_path),
                "exists": yesno(source_path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": yesno(needles_present),
                "checked_utc": UTC,
            }
        )
    return rows


def annulus_support_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_0_worldtube_selector",
            "support_clause": "parent Hilbert worldtube selector",
            "candidate_statement": "W_source := closure(supp J_H[tau_obs]) is chosen before fitted mass, orbital GM, or radius readout.",
            "required_inputs": "parent action;same observed coframe;fixed tau_obs;compact Hilbert support;no readout mask",
            "current_status": "CONDITIONAL_SELECTOR_ONLY",
            "blocking_gap": "1016 gives the exact selector contract, but current MTS does not parent-sign J_H, tau_obs, or compact support",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_1_surface_pair",
            "support_clause": "linked surface pair",
            "candidate_statement": "S1 and S2 link the same W_source and define a compact exterior annulus A_ext with fixed orientation.",
            "required_inputs": "S1;S2;homology_class;orientation;source_path;units",
            "current_status": "SURFACE_PAIR_NOT_SOURCED",
            "blocking_gap": "1724 records missing S1/S2, homology, orientation and annulus measure inputs",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_2_source_free_annulus",
            "support_clause": "A_ext excludes ordinary matter support",
            "candidate_statement": "A_ext cap W_source is empty, so ordinary Hilbert stress has no bulk support in A_ext.",
            "required_inputs": "W_source;A_ext;support_proof;regularity_class;distributional_surface_policy",
            "current_status": "SOURCE_FREE_ANNULUS_NOT_PARENT_SIGNED",
            "blocking_gap": "A_ext is still a template and no support certificate proves supp(T_obs) cap A_ext is empty",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_3_Tobs_bulk_zero",
            "support_clause": "bulk T_obs vanishes on A_ext",
            "candidate_statement": "If T_obs is the ordinary-matter Hilbert stress and A_ext excludes W_source, then T_obs|A_ext=0 in the bulk.",
            "required_inputs": "ordinary matter functor;T_obs definition;same-frame source measure;A_ext support split",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "blocking_gap": "1720 keeps T_obs/J_H conditional and 683 keeps same-frame measure unsigned",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_4_boundary_flux_accounting",
            "support_clause": "boundary/source charge is retained outside bulk T_obs zero",
            "candidate_statement": "Bulk T_obs|A_ext=0 may not delete the mass source; the source charge must live in H_tau, Pi_M J_H, boundary/reference, or retained flux rows.",
            "required_inputs": "M_H_ref;B_zero_flux;Delta_symp;Pi_M chain map;R_glue;source-normalization ledger",
            "current_status": "BOUNDARY_FLUX_ACCOUNTING_MISSING",
            "blocking_gap": "662 and Hamiltonian charge contracts keep boundary/reference/PiM/source-normalization flux rows unsigned",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_5_surface_distribution_policy",
            "support_clause": "distributional shell and corner policy",
            "candidate_statement": "If matter or effective stress is distributional on S1/S2/corners, it is not counted as vanished bulk T_obs unless a boundary row carries it.",
            "required_inputs": "surface stress policy;corner terms;regularization;boundary source row",
            "current_status": "SURFACE_DISTRIBUTION_POLICY_MISSING",
            "blocking_gap": "no current row certifies that shell/corner terms vanish or are moved into a sourced boundary coefficient",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_6_norm_pair_and_units",
            "support_clause": "Tobs operator norm convention",
            "candidate_statement": "If the zero route fails, sup_A ||T_obs||_op needs a norm pair, volume form, Hodge factor and units.",
            "required_inputs": "norm_type;volume_form;Hodge_star_factor;tau_norm;current_norm;units",
            "current_status": "NORM_PAIR_AND_UNITS_MISSING",
            "blocking_gap": "1720/1724 source rows have not declared the common annulus norm owner",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ASA1730_7_verdict",
            "support_clause": "T_obs vacuum-annulus verdict",
            "candidate_statement": "Current MTS does not yet prove T_obs|A_ext=0 or source a nonzero T_obs norm value.",
            "required_inputs": "ASA1730_0 through ASA1730_6 all parent-signed or source-backed",
            "current_status": "VACUUM_ANNULUS_ZERO_NOT_SIGNED",
            "blocking_gap": "worldtube selector, surfaces, support split, same-frame T_obs, boundary flux and norm units remain open",
            "zero_route_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VAT1730_0_setup",
            "theorem_step": "define support-owned exterior annulus",
            "statement": "Let W_source=closure(supp J_H[tau_obs]) and A_ext be the compact region between fixed linked surfaces S1,S2 with A_ext cap W_source empty.",
            "current_status": "CONDITIONAL_SETUP_NOT_PARENT_SIGNED",
            "would_close": "makes source-free exterior a geometric fact rather than a fitted mask",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VAT1730_1_bulk_zero",
            "theorem_step": "ordinary Hilbert stress support",
            "statement": "If T_obs is sourced only by ordinary matter support and the support split is regular, then T_obs|A_ext=0 in the bulk.",
            "current_status": "CONDITIONAL_BULK_ZERO_THEOREM",
            "would_close": "sets sup_A ||T_obs||_op=0 for the bulk ordinary-matter source-current piece",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VAT1730_2_delta_tau_map_zero",
            "theorem_step": "moving tau source-current silence in the bulk",
            "statement": "If T_obs|A_ext=0, then L_Tobs^A[delta tau]=star_A(T_obs(delta tau,.))=0 and C_Tobs_tau^bulk=0.",
            "current_status": "CONDITIONAL_EFFECT_ONLY",
            "would_close": "kills only the bulk T_obs moving-tau contribution, not Hamiltonian/boundary/source-normalization charge",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VAT1730_3_boundary_guard",
            "theorem_step": "mass source is not deleted",
            "statement": "The theorem is legal only if boundary charge, Pi_M flux, reference subtraction, and source-normalization rows retain the mass information excluded from the bulk annulus.",
            "current_status": "BOUNDARY_GUARD_REQUIRED_NOT_FILLED",
            "would_close": "prevents a fake local-GR pass where vacuum T_obs zero erases the source rather than moves it to a conserved charge",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VAT1730_4_current_branch_verdict",
            "theorem_step": "current MTS theorem status",
            "statement": "The vacuum-annulus route is mathematically clean but not a current-MTS theorem because the antecedents are unsigned.",
            "current_status": "FAIL_CURRENT_CLAIM",
            "would_close": "if antecedents close, C_Tobs_tau bulk can become theorem-zero while boundary/source-normalization gates remain active",
            "valid_for_claim": no(),
        },
    ]


def norm_source_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["annulus_support_audit"]),
        str(OUTPUTS["conditional_theorem"]),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv"),
        str(RESIDUALS / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNS1730_0_Z_Tobs_Aext_candidate",
            "quantity": "Z_Tobs_Aext_bulk",
            "definition": "candidate theorem-zero flag for ordinary-matter T_obs in the compact exterior annulus",
            "formula": "Z_Tobs_Aext_bulk=True only if W_source, S1/S2, A_ext cap W_source empty, T_obs support and boundary flux accounting are parent-signed",
            "required_inputs": "W_source;S1;S2;A_ext;support_proof;T_obs_definition;boundary_flux_row;surface_distribution_policy;source_path",
            "current_status": "ZERO_ROUTE_CONDITIONAL_ANTECEDENTS_MISSING",
            "missing_inputs": "MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_SURFACE_PAIR;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_TOBS_SUPPORT_PROOF;MISSING_BOUNDARY_FLUX_ACCOUNTING;MISSING_SURFACE_DISTRIBUTION_POLICY",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_Z_TOBS_AEXT_BULK",
            "units": "boolean_theorem_zero_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNS1730_1_sup_A_Tobs_op",
            "quantity": "sup_A_norm_Tobs_op",
            "definition": "first nonclaim source row for the observed stress-energy operator norm on A_ext",
            "formula": "sup_A ||T_obs||_op, or 0 if Z_Tobs_Aext_bulk is parent-signed",
            "required_inputs": "system_id;A_ext;norm_type;observed_metric_or_coframe;volume_form;stress_components_or_energy_density_bound;Hodge_star_factor;units;source_path",
            "current_status": "FIRST_NORM_SOURCE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_OBSERVED_METRIC_OR_COFRAME;MISSING_VOLUME_FORM;MISSING_STRESS_COMPONENTS_OR_ENERGY_DENSITY_BOUND;MISSING_HODGE_FACTOR;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_SUP_A_TOBS_OP",
            "units": "stress_energy_or_current_conversion_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNS1730_2_C_Tobs_tau_from_sup",
            "quantity": "C_Tobs_tau",
            "definition": "coefficient inherited from the stress operator norm and Hodge/current norm conversion",
            "formula": "C_Tobs_tau <= C_star_measure(A_ext,norm_pair) * sup_A ||T_obs||_op",
            "required_inputs": "sup_A_norm_Tobs_op;C_star_measure;norm_pair;tau_norm;current_norm;units;source_path",
            "current_status": "COEFFICIENT_UPDATE_TEMPLATE",
            "missing_inputs": "MISSING_SUP_A_TOBS_OP;MISSING_C_STAR_MEASURE;MISSING_NORM_PAIR;MISSING_TAU_NORM;MISSING_CURRENT_NORM;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_C_TOBS_TAU",
            "units": "current_norm_per_tau_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNS1730_3_boundary_flux_guard",
            "quantity": "B_flux_Tobs_support",
            "definition": "boundary/reference/PiM flux row required if bulk T_obs is set to zero in A_ext",
            "formula": "source_charge = H_tau/Pi_M/boundary ledger, not bulk T_obs in A_ext",
            "required_inputs": "M_H_ref;B_zero_flux;Delta_symp;R_glue;PiM_chain_map;units;source_path",
            "current_status": "BOUNDARY_FLUX_GUARD_ROW_TEMPLATE",
            "missing_inputs": "MISSING_M_H_REF;MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_PIM_CHAIN_MAP;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv"),
            "numeric_value": "MISSING_B_FLUX_TOBS_SUPPORT",
            "units": "charge_or_dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNS1730_4_surface_distribution_guard",
            "quantity": "S_surface_Tobs_Aext",
            "definition": "guard against hidden shell/corner stress on S1/S2 when declaring bulk T_obs support-free",
            "formula": "S_surface_Tobs_Aext=0 or retained in B_flux_Tobs_support",
            "required_inputs": "surface_stress_policy;corner_terms;regularization;boundary_flux_row;source_path",
            "current_status": "SURFACE_TERM_GUARD_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SURFACE_STRESS_POLICY;MISSING_CORNER_TERMS;MISSING_REGULARIZATION;MISSING_BOUNDARY_FLUX_ROW",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_SURFACE_TOBS_AEXT",
            "units": "stress_integral_or_boundary_charge_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1730_0_vacuum_annulus_zero",
            "quantity": "T_obs|A_ext=0",
            "runner_decision": "REFUSE_CLAIM",
            "refusal_reasons": "MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_SURFACE_PAIR;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_SAME_FRAME_TOBS;MISSING_BOUNDARY_FLUX_ACCOUNTING",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1730_1_Tobs_norm_source_row",
            "quantity": "sup_A_norm_Tobs_op",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_STRESS_BOUND;MISSING_HODGE_FACTOR;MISSING_UNITS",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1730_2_C_Tobs_tau",
            "quantity": "C_Tobs_tau",
            "runner_decision": "BOUND_FORM_ONLY_REFUSE_SCORING",
            "refusal_reasons": "MISSING_SUP_A_TOBS_OP_OR_ZERO_THEOREM;MISSING_C_STAR_MEASURE;MISSING_TAU_NORM;MISSING_CURRENT_NORM",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1730_3_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "VACUUM_ANNULUS_ZERO_NOT_SIGNED;BOUNDARY_FLUX_GUARD_UNFILLED;MHREF_JH_NDOMAIN_PPN_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1730_0_vacuum_annulus_route",
            "decision": "keep the vacuum-annulus zero theorem as the clean route",
            "because": "if A_ext is genuinely source-free, the bulk T_obs moving-tau source-current coefficient can vanish without a fitted cancellation",
            "next_action": "prove the worldtube/surface/support antecedents or keep the coefficient finite",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1730_1_no_mass_erasure",
            "decision": "do not let bulk T_obs zero erase the mass source",
            "because": "a vacuum exterior in GR still carries mass through boundary/Hamiltonian flux, not local matter stress in the annulus",
            "next_action": "require B_flux/M_H_ref/PiM/source-normalization accounting before any C_Tobs_tau zero promotion",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1730_2_best_next",
            "decision": "attack A_ext surface-pair and support certificate next",
            "because": "numeric T_obs stress values are premature until the branch knows whether the active annulus is source-free or not",
            "next_action": "1731 should parent-sign or explicitly source W_source, S1, S2, A_ext cap W_source, and the boundary-flux handoff",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1730_0_primary",
            "next_target": "1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md",
            "script": "scripts/Y5_R2FR_Aext_surface_pair_support_certificate_or_boundary_flux_row.py",
            "objective": "parent-sign or source W_source, S1, S2, A_ext cap W_source empty, and boundary-flux handoff; otherwise keep Tobs norm row finite and nonclaim",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1730_1_parallel_norm_units",
            "next_target": "1731b-Y5-R2FR-Tobs-norm-units-and-Hodge-factor-source-row.md",
            "script": "scripts/Y5_R2FR_Tobs_norm_units_and_Hodge_factor_source_row.py",
            "objective": "fill norm type, observed volume form, Hodge-star conversion and units for sup_A ||T_obs||_op without scoring it",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1730_2_later_CdeltaTau_stack",
            "next_target": "1732-Y5-R2FR-CdeltaTau-source-piece-stack-runner.md",
            "script": "scripts/Y5_R2FR_CdeltaTau_source_piece_stack_runner.py",
            "objective": "combine Z_Tobs_Aext or sup_A_Tobs with C_Tobs_tau only after the annulus and boundary guards are closed",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1730_0_vacuum_annulus_zero",
            "claim": "T_obs vanishes on the compact exterior annulus",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "ASA1730_7 says the vacuum-annulus zero theorem is not signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1730_1_C_Tobs_tau_zero",
            "claim": "C_Tobs_tau bulk is theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "support split, boundary flux handoff, and surface distribution policy are missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1730_2_Tobs_norm_source_backed",
            "claim": "sup_A ||T_obs||_op is source-backed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "first norm source row lacks A_ext, norm type, stress bound, Hodge factor and units",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1730_3_MHref_JH_Ndomain",
            "claim": "M_H_ref/J_H/N_domain can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "bulk source-current piece and boundary mass-flux handoff are both unclosed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1730_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "support geometry, fixed tau, Hamiltonian charge, source normalization and PPN vector remain open",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "annulus_support_audit": annulus_support_audit_rows(),
        "conditional_theorem": conditional_theorem_rows(),
        "norm_source_rows": norm_source_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1730_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1730_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "zero_route_ready"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1730_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1730_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1730*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def norm_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    if len(rows) != 5:
        return False
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text:
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
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
    audit = rows_map["annulus_support_audit"]
    theorem = rows_map["conditional_theorem"]
    norm_rows = rows_map["norm_source_rows"]
    refusals = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1730_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1730_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1730_2_1729_handoff_preserved",
            any(row["source_key"] == "1729_next_target" and row["needles_present"] == "True" for row in source_register),
            "1729 selected support-annulus route",
            "1729 handoff missing",
        ),
        check(
            "VAL1730_3_annulus_audit_complete",
            {row["support_clause"] for row in audit}
            >= {
                "parent Hilbert worldtube selector",
                "linked surface pair",
                "A_ext excludes ordinary matter support",
                "bulk T_obs vanishes on A_ext",
                "boundary/source charge is retained outside bulk T_obs zero",
                "distributional shell and corner policy",
                "Tobs operator norm convention",
                "T_obs vacuum-annulus verdict",
            },
            "annulus audit covers selector, surfaces, support, bulk zero, boundary flux, surface terms, norm and verdict",
            "annulus audit missing required clause",
        ),
        check(
            "VAL1730_4_vacuum_zero_blocked",
            any(row["audit_id"] == "ASA1730_7_verdict" and row["current_status"] == "VACUUM_ANNULUS_ZERO_NOT_SIGNED" for row in audit),
            "vacuum-annulus zero remains unsigned",
            "vacuum-annulus zero verdict missing or opened",
        ),
        check(
            "VAL1730_5_conditional_theorem_written",
            any(row["theorem_id"] == "VAT1730_2_delta_tau_map_zero" and "C_Tobs_tau" in row["statement"] for row in theorem),
            "conditional bulk C_Tobs_tau zero theorem is written",
            "conditional C_Tobs_tau zero theorem missing",
        ),
        check(
            "VAL1730_6_norm_rows_nonclaim",
            norm_rows_nonclaim(norm_rows),
            "all norm/source rows carry missing markers and remain nonclaim",
            "one or more norm/source rows are claim-enabled or malformed",
        ),
        check(
            "VAL1730_7_boundary_guard_present",
            any(row["row_id"] == "TNS1730_3_boundary_flux_guard" for row in norm_rows),
            "boundary flux guard row is present",
            "boundary flux guard row missing",
        ),
        check(
            "VAL1730_8_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals} >= {"T_obs|A_ext=0", "sup_A_norm_Tobs_op", "C_Tobs_tau", "Newton/local-GR reduction"},
            "runner refusals cover vacuum zero, norm row, C_Tobs_tau and local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1730_9_decision_next",
            any(row["decision_id"] == "DEC1730_2_best_next" and "surface-pair" in row["decision"] for row in decisions),
            "decision selects A_ext surface-pair/support certificate next",
            "decision does not select surface-pair/support certificate",
        ),
        check(
            "VAL1730_10_next_selected",
            any(row["route_id"] == "NEXT1730_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1731 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1730_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1730_12_csv_parse", parsed_ok, "all generated 1730 CSVs parse", "one or more generated 1730 CSVs failed to parse"),
        check("VAL1730_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1730_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1730_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1730_16_formalization_untouched", formalization_untouched(), "no 1730 outputs found under formalization-workbench", "1730 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1730_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1730 Tobs support-annulus validation" if overall else "one or more 1730 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1730 tests the cleanest way to silence the moving-`tau` source-current leak: make the active compact exterior annulus genuinely source-free.",
        "- The theorem shape is good: if `W_source=closure(supp J_H[tau_obs])`, `A_ext cap W_source=empty`, and boundary/source flux is retained elsewhere, then bulk `T_obs|A_ext=0` and the bulk `C_Tobs_tau` piece is zero.",
        "- Current result: this is **not signed** for current MTS. The worldtube selector, surface pair, support split, same-frame `T_obs`, boundary-flux handoff, surface/corner policy, and norm units are still open.",
        "- The fallback is now a first nonclaim `sup_A_norm_Tobs_op` row plus boundary-flux and surface-distribution guard rows.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Conditional Theorem",
        "If the source worldtube and linked exterior annulus are parent-owned, then a vacuum exterior works exactly the way the GR intuition wants: ordinary matter stress vanishes in the bulk annulus while mass is carried by boundary/Hamiltonian/source-normalization data. The forbidden move is to use `T_obs|A_ext=0` to delete the source rather than move it into the conserved charge ledger.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Annulus Support Audit",
        markdown_table(rows_map["annulus_support_audit"], ["audit_id", "support_clause", "current_status", "blocking_gap", "zero_route_ready", "valid_for_claim"]),
        "",
        "## Vacuum Annulus Theorem",
        markdown_table(rows_map["conditional_theorem"], ["theorem_id", "theorem_step", "statement", "current_status", "valid_for_claim"]),
        "",
        "## Tobs Norm Source Rows",
        markdown_table(rows_map["norm_source_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "This is one of the less grim local-branch moves. A vacuum exterior annulus is exactly how a GR-like theory can have no local matter stress in the exterior without losing the source mass. But the price is strict: the mass must reappear through a parent-owned boundary/Hamiltonian/source-normalization chain. So 1730 does not close local GR, but it gives us a cleaner fork: either prove the annulus/support/boundary handoff, or pay `C_Tobs_tau` as a finite source-current residual.",
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
    doc_path = ROOT / "1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1730_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1730 validation FAIL")
    print("1730 validation PASS")


if __name__ == "__main__":
    main()
