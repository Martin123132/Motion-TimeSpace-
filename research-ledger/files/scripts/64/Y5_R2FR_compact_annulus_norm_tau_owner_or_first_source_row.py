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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1724"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1724 - Compact Annulus Norm Tau Owner Or First Source Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1724_0_1723_doc",
        "source_key": "1723_doc",
        "source_path": ROOT / "1723-Y5-R2FR-guarded-JH-norm-stack-or-CwH-input-source.md",
        "needles": ["NEXT1723_0_primary", "compact annulus/norm/tau owner"],
    },
    {
        "source_id": "SRC1724_1_1723_guard",
        "source_key": "1723_guard_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_GUARD_REQUIREMENT_MATRIX.csv",
        "needles": ["GJH1723_2_tau_annulus_norm", "TAU_ANNULUS_NORM_MISSING"],
    },
    {
        "source_id": "SRC1724_2_1723_priority",
        "source_key": "1723_input_priority",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_INPUT_PRIORITY_LEDGER.csv",
        "needles": ["PRI1723_0_shared_norm_space", "A_ext + norm_type + volume form + units"],
    },
    {
        "source_id": "SRC1724_3_1720_jh_row",
        "source_key": "1720_jh_norm_first_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
    {
        "source_id": "SRC1724_4_1720_doc",
        "source_key": "1720_doc",
        "source_path": ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
        "needles": ["JHT1720_2_norm_convention", "compact exterior annulus"],
    },
    {
        "source_id": "SRC1724_5_1719_ingredients",
        "source_key": "1719_ingredients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
        "needles": ["ING1719_0_JH_norm_candidate", "A_ext;norm_type;volume_form"],
    },
    {
        "source_id": "SRC1724_6_1718_doc",
        "source_key": "1718_doc",
        "source_path": ROOT / "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md",
        "needles": ["closure(supp J_H[tau])", "linked exterior surfaces"],
    },
    {
        "source_id": "SRC1724_7_1718_domain_bound",
        "source_key": "1718_domain_bound",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv",
        "needles": ["NDB1718_0_domain_numerator_contract", "MISSING_ANNULUS_MEASURE"],
    },
    {
        "source_id": "SRC1724_8_1608_tau",
        "source_key": "1608_tau_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    },
    {
        "source_id": "SRC1724_9_1608_doc",
        "source_key": "1608_doc",
        "source_path": ROOT / "1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md",
        "needles": ["tau_eff=1 shortcut", "SHORTCUT_FORBIDDEN"],
    },
    {
        "source_id": "SRC1724_10_684_frame_lock",
        "source_key": "684_frame_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
        "needles": ["FLC684_6_verdict", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1724_11_685_tau_generator",
        "source_key": "685_tau_generator",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_6_verdict", "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs"],
    },
    {
        "source_id": "SRC1724_12_1359_surface_intake",
        "source_key": "1359_surface_intake",
        "source_path": RESIDUALS / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
        "needles": ["ISI1359_0_surface_inner", "MISSING_INNER_RADIUS_OR_SURFACE"],
    },
    {
        "source_id": "SRC1724_13_1360_surface_rows",
        "source_key": "1360_surface_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv",
        "needles": ["MSI1360_3_annulus_homology", "MISSING_ANNULUS_HOMOLOGY_SOURCE"],
    },
    {
        "source_id": "SRC1724_14_1722_cwh_rows",
        "source_key": "1722_cwh_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_CURRENT_NORM_BOUND_ROWS.csv",
        "needles": ["CWH1722_0_CwH_current_norm_bound_candidate", "MISSING_OPERATOR_NORM"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_SOURCE_REGISTER.csv",
    "owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv",
    "common_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_COMMON_NORM_SPACE_SCHEMA.csv",
    "first_source_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_FIRST_SOURCE_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1724_VALIDATION.csv",
}


COPY_MAP = {
    "owner_audit": "R2FR_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv",
    "common_schema": "R2FR_1724_COMMON_NORM_SPACE_SCHEMA.csv",
    "first_source_rows": "R2FR_1724_FIRST_SOURCE_ROWS.csv",
    "runner_refusal": "R2FR_1724_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1724_DECISION_LEDGER.csv",
    "next_target": "R2FR_1724_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1724_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows = []
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


def owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_0_parent_support_selector",
            "owner_clause": "W_source selector",
            "candidate_statement": "W_source := closure(supp J_H[tau_obs]) before readout, with no post-fit masking or measured-G absorption.",
            "required_parent_signature": "parent action + same observed coframe + fixed tau_obs + ordinary/full source-current definition",
            "current_status": "CONDITIONAL_SELECTOR_ONLY",
            "blocking_debt": "J_H[tau_obs] and tau_obs are not parent-signed in a common source frame",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_1_surface_pair",
            "owner_clause": "linked surface pair",
            "candidate_statement": "choose S1 and S2 in the source-free exterior with S1 homologous to S2 and boundaries fixed before source readout.",
            "required_parent_signature": "inner surface, outer surface, homology class, source-free certificate, orientation rule",
            "current_status": "SURFACE_PAIR_NOT_SOURCED",
            "blocking_debt": "1359/1360 rows still have missing S1/S2/radii/homology/source-free inputs",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_2_compact_annulus",
            "owner_clause": "compact exterior annulus",
            "candidate_statement": "A_ext is the compact region between S1 and S2 on a tau_obs slice, with A_ext cap W_source empty.",
            "required_parent_signature": "regular support, compactness, source-free exterior certificate, annulus measure",
            "current_status": "COMPACT_ANNULUS_NOT_PARENT_OWNED",
            "blocking_debt": "1718 compactness is a conditional topological step and annulus_measure is missing",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_3_volume_form",
            "owner_clause": "observed volume form",
            "candidate_statement": "mu_A := induced spatial volume form from e_obs on the tau_obs slice, with orientation inherited from (S2,-S1).",
            "required_parent_signature": "e_obs descent + tau_obs source-normal lock + orientation convention + units",
            "current_status": "VOLUME_FORM_NOT_SIGNED",
            "blocking_debt": "684/685 frame and tau generator locks remain blocked_nonclaim",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_4_current_norm",
            "owner_clause": "current norm type",
            "candidate_statement": "declare one current norm, e.g. ||J||_{A,1}=int_A |J|_{g_obs} mu_A or a declared dual norm, shared by J_H, C_wH and C_nonH.",
            "required_parent_signature": "norm functor, metric/coframe used in the pointwise norm, component-current projection compatibility",
            "current_status": "NORM_TYPE_NOT_SOURCED",
            "blocking_debt": "1720 J_H row and 1722 C_wH row both lack norm type/operator norm inputs",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_5_domain_operator_pair",
            "owner_clause": "dual operator norm pair",
            "candidate_statement": "C_DPiM := sup_{J != 0} |int_A (dPi_M)_domain J| / ||J||_A, using the same A_ext, tau_obs, volume form and units.",
            "required_parent_signature": "dPiM domain map, domain variation norm, annulus measure, compatible numerator units",
            "current_status": "OPERATOR_NORM_PAIR_NOT_SOURCED",
            "blocking_debt": "1719/1718 factorization exists but C_DPiM, delta_D and numerator units remain missing",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_6_tau_source_normal_lock",
            "owner_clause": "tau/source-normal lock",
            "candidate_statement": "tau_source = tau_charge = tau_clock = tau_boundary = tau_orbit = tau_obs, with no tau_eff=1 shortcut.",
            "required_parent_signature": "observed-frame lock, Hamiltonian generator, clock normalization, boundary reference, source-normal convention",
            "current_status": "TAU_SOURCE_NORMAL_LOCK_BLOCKED",
            "blocking_debt": "1608 tau_WEP, 684 frame lock and 685 tau generator rows remain not evaluated/blocked",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_7_units_and_orientation",
            "owner_clause": "units and signs",
            "candidate_statement": "all source-current, operator, numerator and normalized residual units must be declared before interpolation or comparison.",
            "required_parent_signature": "unit ledger, orientation convention, denominator normalization, no fitted-G absorption",
            "current_status": "UNITS_ORIENTATION_SCHEMA_ONLY",
            "blocking_debt": "1359 records unit normalization as schema-only and 1360 denominator/source rows remain missing",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "ANT1724_8_verdict",
            "owner_clause": "common norm owner verdict",
            "candidate_statement": "a common owner theorem is available only conditionally; current branch must use source-ready nonclaim rows, not a derived owner.",
            "required_parent_signature": "ANT1724_0 through ANT1724_7 all parent-signed",
            "current_status": "COMMON_NORM_SPACE_NOT_PARENT_OWNED",
            "blocking_debt": "support, surfaces, annulus, volume form, norm pair, tau/source-normal lock and units are all unsigned",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def common_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "schema_id": "CNS1724_0_common_owner_schema",
            "row_type": "required_columns",
            "system_id": "required",
            "branch_local_id": "required",
            "A_ext_id": "required",
            "W_source_rule": "required",
            "surface_inner_id": "required",
            "surface_outer_id": "required",
            "homology_class": "required",
            "source_free_certificate": "required",
            "volume_form": "required",
            "norm_type_current": "required",
            "norm_pair_domain": "required",
            "tau_id": "required",
            "source_normal_id": "required",
            "orientation": "required",
            "units_current": "required",
            "units_operator": "required",
            "units_numerator": "required",
            "source_path": "required",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "CNS1724_1_minimal_candidate_definition",
            "row_type": "conditional_definition",
            "system_id": "MISSING_SYSTEM_ID",
            "branch_local_id": BRANCH_ID,
            "A_ext_id": "A_ext[S1,S2,tau_obs]",
            "W_source_rule": "W_source=closure(supp J_H[tau_obs])",
            "surface_inner_id": "MISSING_SURFACE_INNER_S1",
            "surface_outer_id": "MISSING_SURFACE_OUTER_S2",
            "homology_class": "MISSING_EXTERIOR_HOMOLOGY_CLASS",
            "source_free_certificate": "MISSING_A_EXT_CAP_W_SOURCE_EMPTY_CERTIFICATE",
            "volume_form": "MISSING_MU_A_FROM_EOBS_TAUOBS",
            "norm_type_current": "MISSING_CURRENT_NORM_L1_L2_SUP_OR_DUAL",
            "norm_pair_domain": "MISSING_DUAL_OPERATOR_NORM_PAIR",
            "tau_id": "MISSING_PARENT_SIGNED_TAU_OBS",
            "source_normal_id": "MISSING_SOURCE_NORMAL_LOCK",
            "orientation": "MISSING_ORIENTATION_CONVENTION",
            "units_current": "MISSING_CURRENT_UNITS",
            "units_operator": "MISSING_OPERATOR_UNITS",
            "units_numerator": "MISSING_NUMERATOR_UNITS",
            "source_path": str(OUTPUTS["first_source_rows"]),
            "valid_for_claim": no(),
        },
    ]


def first_source_rows() -> list[dict[str, Any]]:
    source_bundle = ";".join(str(source["source_path"]) for source in SOURCES)
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "NORM1724_0_common_norm_space_candidate",
            "quantity": "common_A_ext_tau_norm_owner",
            "definition": "one shared A_ext, tau_obs, volume form, norm type and units for J_H, C_wH, C_nonH and N_domain",
            "status": "SOURCE_ROW_TEMPLATE_ONLY_NOT_SCORE_READY",
            "missing_parent_inputs": "MISSING_SYSTEM_ID;MISSING_SURFACE_PAIR;MISSING_HOMOLOGY;MISSING_SOURCE_FREE_CERTIFICATE;MISSING_VOLUME_FORM;MISSING_NORM_TYPE;MISSING_TAU_LOCK;MISSING_SOURCE_NORMAL;MISSING_UNITS",
            "source_paths": source_bundle,
            "source_anchor": "GJH1723_2;PRI1723_0;JHN1720_0;NDB1718_0;TAU1608_4;FLC684_6;TGC685_6;ISI1359_0..7;MSI1360_0..7",
            "numeric_value": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "units": "MISSING_COMMON_UNITS",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NORM1724_1_tau_source_normal_candidate",
            "quantity": "tau_obs_source_normal_lock",
            "definition": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs with one source-normal convention",
            "status": "TAU_SOURCE_NORMAL_LOCK_BLOCKED_NONCLAIM",
            "missing_parent_inputs": "MISSING_HAMILTONIAN_GENERATOR;MISSING_CLOCK_NORMALIZATION;MISSING_BOUNDARY_REFERENCE;MISSING_SOURCE_NORMAL;MISSING_TAU_WEP_EVALUATION",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv") + ";" + str(RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv"),
            "source_anchor": "FLC684_1;FLC684_6;TGC685_0;TGC685_4;TGC685_6;TAU1608_3;TAU1608_4",
            "numeric_value": "MISSING_PARENT_SIGNED_TAU_OBS",
            "units": "dimensionless_or_time_normalization_CERTIFICATE_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NORM1724_2_surface_pair_annulus_candidate",
            "quantity": "S1_S2_A_ext_homology",
            "definition": "S1 and S2 bound a compact source-free exterior annulus A_ext fixed before readout",
            "status": "SURFACE_PAIR_ANNULUS_SOURCE_ROW_TEMPLATE",
            "missing_parent_inputs": "MISSING_INNER_SURFACE;MISSING_OUTER_SURFACE;MISSING_ANNULUS_HOMOLOGY;MISSING_SOURCE_FREE_CERTIFICATE;MISSING_ANNULUS_MEASURE",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv") + ";" + str(RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv"),
            "source_anchor": "ISI1359_0;ISI1359_1;ISI1359_2;MSI1360_1;MSI1360_2;MSI1360_3;NDB1718_0",
            "numeric_value": "MISSING_SURFACE_RADII_OR_THEOREM_SURFACES",
            "units": "length_or_surface_identifier_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NORM1724_3_volume_form_orientation_candidate",
            "quantity": "mu_A_orientation",
            "definition": "observed induced volume form and orientation on A_ext from e_obs and tau_obs",
            "status": "VOLUME_FORM_ORIENTATION_TEMPLATE_ONLY",
            "missing_parent_inputs": "MISSING_PARENT_SIGNED_EOBS;MISSING_PARENT_SIGNED_TAU_OBS;MISSING_ORIENTATION_CONVENTION;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
            "source_anchor": "FLC684_6;JHN1720_0",
            "numeric_value": "MISSING_VOLUME_FORM_CERTIFICATE",
            "units": "MISSING_MEASURE_UNITS",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NORM1724_4_norm_pair_candidate",
            "quantity": "current_norm_and_dPiM_dual_norm_pair",
            "definition": "one norm for source currents and the corresponding dual operator norm for dPiM_domain",
            "status": "NORM_PAIR_TEMPLATE_ONLY",
            "missing_parent_inputs": "MISSING_CURRENT_NORM_TYPE;MISSING_COMPONENT_PROJECTION_NORM;MISSING_DPIM_OPERATOR_NORM;MISSING_DELTA_D_NORM;MISSING_NUMERATOR_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_CURRENT_NORM_BOUND_ROWS.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1723_GUARDED_JH_NORM_STACK.csv"),
            "source_anchor": "ING1719_0;ING1719_1;CWH1722_0;STACK1723_1",
            "numeric_value": "MISSING_OPERATOR_AND_CURRENT_NORM_VALUES",
            "units": "MISSING_COMPATIBLE_NORM_UNITS",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1724_0_owner_theorem",
            "quantity": "common annulus/norm/tau owner theorem",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_DERIVED_OWNER",
            "refusal_reasons": "UNSIGNED_SUPPORT_SELECTOR;UNSIGNED_SURFACE_PAIR;UNSIGNED_TAU_SOURCE_NORMAL_LOCK;UNSIGNED_VOLUME_FORM;UNSIGNED_NORM_PAIR;MISSING_UNITS",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1724_1_first_source_rows",
            "quantity": "common owner source-ready rows",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "ALL_ROWS_VALID_FOR_CLAIM_FALSE;MISSING_PARENT_INPUTS_REMAIN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1724_2_JH_total",
            "quantity": "J_H_total norm stack",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "COMMON_NORM_SPACE_NOT_PARENT_OWNED;BASE_JH_NORM_MISSING;CWH_INPUTS_MISSING;NONHILBERT_CURRENT_MISSING",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1724_3_Ndomain",
            "quantity": "N_domain guarded bound",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "A_EXT_MISSING;ANNULUS_MEASURE_MISSING;DPIM_OPERATOR_NORM_MISSING;DELTA_D_MISSING;JH_TOTAL_NORM_NOT_READY",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1724_4_Newton_local_GR",
            "quantity": "Newton/local-GR reopening",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_COMMON_OWNER;NO_FINITE_NDOMAIN;M_H_REF_MISSING;R_EQ_MISSING;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1724_0_owner_derivation",
            "decision": "common owner theorem not claimed",
            "because": "the theorem needs signed support, surfaces, annulus, tau/source-normal, volume form, norm-pair and unit clauses together",
            "next_action": "use the source-ready nonclaim rows as the checklist rather than smuggling in a plateau or norm axiom",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1724_1_best_next",
            "decision": "attack tau/source-normal lock first",
            "because": "tau_obs controls J_H, C_wH, C_nonH, clocks, Hamiltonian charge, orbit readout and WEP readout; without it no shared owner can score",
            "next_action": "1725 should try to derive tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs, or keep it as an explicit finite input row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1724_2_parallel_surface_fill",
            "decision": "surface-pair acquisition remains parallel",
            "because": "S1/S2/A_ext can be filled as data-geometry inputs, but scoring still fails if tau/source-normal lock is unsigned",
            "next_action": "prepare S1/S2/A_ext source rows after tau lock route or in a short parallel checkpoint",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1724_0_primary",
            "next_target": "1725-Y5-R2FR-tau-source-normal-lock-or-explicit-finite-input-row.md",
            "script": "scripts/Y5_R2FR_tau_source_normal_lock_or_explicit_finite_input_row.py",
            "objective": "derive the one-generator tau/source-normal lock needed by J_H, C_wH, C_nonH, clocks, boundary charge, orbital readout and WEP; if not, write the explicit nonclaim input row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1724_1_parallel_surface_annulus",
            "next_target": "1725b-Y5-R2FR-surface-pair-annulus-source-row-fill.md",
            "script": "scripts/Y5_R2FR_surface_pair_annulus_source_row_fill.py",
            "objective": "fill S1/S2/A_ext/homology/source-free certificate as geometry-data inputs without claiming local GR",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1724_2_later_nonHilbert",
            "next_target": "1726-Y5-R2FR-nonHilbert-current-silence-or-qnonH-source-row.md",
            "script": "scripts/Y5_R2FR_nonHilbert_current_silence_or_qnonH_source_row.py",
            "objective": "derive non-Hilbert/current/readout source silence or source a finite q_nonH correction after the common owner route is less ambiguous",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1724_0_common_owner",
            "claim": "A_ext/tau/norm/volume-form owner is parent-derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "ANT1724_0 through ANT1724_7 remain unsigned",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1724_1_JH_total_norm",
            "claim": "guarded J_H_total norm is score-ready",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "common owner row is template-only and source-current components remain missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1724_2_Ndomain",
            "claim": "N_domain guarded bound is finite",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "A_ext, annulus measure, C_DPiM, delta_D and J_H_total norm are not sourced",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1724_3_Newton_local_GR",
            "claim": "Newton/local-GR source-normalization gate can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "shared owner and finite source numerator chain are not closed",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "owner_audit": owner_audit_rows(),
        "common_schema": common_schema_rows(),
        "first_source_rows": first_source_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1724_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1724_{key.upper()}.csv")


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


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1724_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1724_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1724*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def first_source_rows_have_missing(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        combined = ";".join(str(value) for value in row.values())
        if "MISSING_" not in combined:
            return False
        if row.get("valid_for_claim") != "False":
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

    source_rows_map = rows_map["source_register"]
    owner_rows = rows_map["owner_audit"]
    schema_rows = rows_map["common_schema"]
    first_rows = rows_map["first_source_rows"]
    refusal_rows = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    next_target = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1724_0_sources_exist", all(row["exists"] == "True" for row in source_rows_map), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1724_1_needles_present", all(row["needles_present"] == "True" for row in source_rows_map), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1724_2_1723_handoff_preserved",
            any(row["source_key"] == "1723_doc" and row["needles_present"] == "True" for row in source_rows_map),
            "1723 selected compact annulus/norm/tau owner next",
            "1723 handoff missing",
        ),
        check(
            "VAL1724_3_owner_audit_complete",
            {row["owner_clause"] for row in owner_rows} >= {"W_source selector", "linked surface pair", "compact exterior annulus", "observed volume form", "current norm type", "dual operator norm pair", "tau/source-normal lock", "units and signs"},
            "owner audit covers support, surfaces, annulus, volume, norm, operator pair, tau lock and units",
            "owner audit missing required clause",
        ),
        check(
            "VAL1724_4_owner_verdict_blocked",
            any(row["audit_id"] == "ANT1724_8_verdict" and row["current_status"] == "COMMON_NORM_SPACE_NOT_PARENT_OWNED" for row in owner_rows),
            "common norm owner remains explicitly blocked",
            "common norm owner verdict missing or opened",
        ),
        check(
            "VAL1724_5_schema_required_columns",
            any(row["schema_id"] == "CNS1724_0_common_owner_schema" and row["system_id"] == "required" and row["source_path"] == "required" for row in schema_rows),
            "common norm space schema records required columns",
            "common norm space schema missing required row",
        ),
        check(
            "VAL1724_6_first_rows_nonclaim",
            len(first_rows) == 5 and first_source_rows_have_missing(first_rows),
            "all first source rows remain nonclaim and carry explicit missing markers",
            "first source rows are incomplete or claim-enabled",
        ),
        check(
            "VAL1724_7_refusals_cover_chain",
            {row["quantity"] for row in refusal_rows} >= {"common annulus/norm/tau owner theorem", "J_H_total norm stack", "N_domain guarded bound", "Newton/local-GR reopening"},
            "runner refusals cover owner, J_H_total, N_domain and Newton/local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1724_8_decision_tau_next",
            any(row["decision_id"] == "DEC1724_1_best_next" and "tau/source-normal lock" in row["decision"] for row in decision),
            "decision selects tau/source-normal lock as primary next target",
            "decision does not select tau/source-normal lock",
        ),
        check(
            "VAL1724_9_next_selected",
            any(row["route_id"] == "NEXT1724_0_primary" and row["selection_status"] == "selected" for row in next_target),
            "next target row selects 1725 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1724_10_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1724_11_csv_parse", parsed_ok, "all generated 1724 CSVs parse", "one or more generated 1724 CSVs failed to parse"),
        check("VAL1724_12_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1724_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1724_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1724_15_formalization_untouched", formalization_untouched(), "no 1724 outputs found under formalization-workbench", "1724 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1724_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1724 compact annulus/norm/tau owner validation" if overall else "one or more 1724 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1724 tries the derivation-first route for the shared `A_ext`/norm/`tau_obs` owner that 1723 made unavoidable.",
        "- The clean theorem exists only conditionally: if support, linked surfaces, compact exterior annulus, observed volume form, current norm, dual operator norm, `tau_obs`/source-normal lock, and units are all parent-signed, then the same measurement space can host `J_H`, `C_wH`, `C_nonH`, and `N_domain`.",
        "- Current branch does **not** have those signatures. The result is therefore a source-ready nonclaim schema, not a GR/Newton/local-source claim.",
        "- The most dangerous cheat is now visible: choosing `tau`, the annulus, or the norm after looking at the readout would silently tune the local branch. 1724 forbids that.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, source-normalization, `J_H_total`, or `N_domain` claim is made.",
        "",
        "## Conditional Owner Theorem",
        "If a parent action supplies a pre-readout support selector `W_source=closure(supp J_H[tau_obs])`, linked source-free surfaces `S1,S2`, a compact annulus `A_ext`, the observed volume form from `e_obs`, one declared source-current norm, the corresponding dual `dPi_M` operator norm, a single `tau_obs`/source-normal convention, and compatible units, then all active source-current pieces can be measured in one space. The present corpus has the form of this theorem, but not the signatures needed to use it as evidence.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Owner Audit",
        markdown_table(rows_map["owner_audit"], ["audit_id", "owner_clause", "current_status", "blocking_debt", "derivation_ready", "valid_for_claim"]),
        "",
        "## Common Norm Space Schema",
        markdown_table(rows_map["common_schema"], ["schema_id", "row_type", "A_ext_id", "W_source_rule", "surface_inner_id", "surface_outer_id", "volume_form", "norm_type_current", "norm_pair_domain", "tau_id", "valid_for_claim"]),
        "",
        "## First Source Rows",
        markdown_table(rows_map["first_source_rows"], ["input_id", "quantity", "status", "missing_parent_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "1724 is not flashy, but it is important: it turns a vague local-branch normalization problem into a hard checklist. The shared measurement space is now a named object with explicit missing teeth. The next best derivation attack is the `tau_obs`/source-normal lock, because that one generator touches the source current, Hamiltonian charge, clocks, orbit readout, and WEP readout. If that lock can be derived, the annulus/norm owner becomes much less arbitrary; if it cannot, the local branch remains an explicit finite-input closure rather than a GR reduction.",
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
    doc_path = ROOT / "1724-Y5-R2FR-compact-annulus-norm-tau-owner-or-first-source-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1724_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1724 validation FAIL")
    print("1724 validation PASS")


if __name__ == "__main__":
    main()
