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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1731"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1731 - Aext Surface Pair Support Certificate Or Boundary Flux Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1731_0_1730_doc",
        "source_key": "1730_doc",
        "source_path": ROOT / "1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md",
        "needles": ["NEXT1730_0_primary", "boundary-flux handoff"],
    },
    {
        "source_id": "SRC1731_1_1730_next",
        "source_key": "1730_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_NEXT_TARGET.csv",
        "needles": ["1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md", "selected"],
    },
    {
        "source_id": "SRC1731_2_1730_annulus_audit",
        "source_key": "1730_annulus_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_ANNULUS_SUPPORT_AUDIT.csv",
        "needles": ["ASA1730_7_verdict", "VACUUM_ANNULUS_ZERO_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1731_3_1730_norm_rows",
        "source_key": "1730_norm_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_TOBS_NORM_SOURCE_ROWS.csv",
        "needles": ["TNS1730_3_boundary_flux_guard", "MISSING_M_H_REF"],
    },
    {
        "source_id": "SRC1731_4_1724_annulus_owner",
        "source_key": "1724_annulus_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv",
        "needles": ["ANT1724_2_compact_annulus", "COMPACT_ANNULUS_NOT_PARENT_OWNED"],
    },
    {
        "source_id": "SRC1731_5_1718_worldtube_audit",
        "source_key": "1718_worldtube_support_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv",
        "needles": ["WTO1718_8_verdict", "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED"],
    },
    {
        "source_id": "SRC1731_6_1718_domain_contract",
        "source_key": "1718_domain_numerator_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv",
        "needles": ["NDB1718_0_domain_numerator_contract", "MISSING_ANNULUS_MEASURE"],
    },
    {
        "source_id": "SRC1731_7_1359_intake",
        "source_key": "1359_surface_intake",
        "source_path": RESIDUALS / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
        "needles": ["ISI1359_0_surface_inner", "MISSING_INNER_RADIUS_OR_SURFACE"],
    },
    {
        "source_id": "SRC1731_8_1360_surface_rows",
        "source_key": "1360_surface_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv",
        "needles": ["MSI1360_3_annulus_homology", "MISSING_ANNULUS_HOMOLOGY_SOURCE"],
    },
    {
        "source_id": "SRC1731_9_662_bound_template",
        "source_key": "662_boundary_flux_template",
        "source_path": RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv",
        "needles": ["BI662_3_boundary_reference_flux", "MISSING_BOUNDARY_REFERENCE_INPUT"],
    },
    {
        "source_id": "SRC1731_10_1013_obstructions",
        "source_key": "1013_flux_obstructions_doc",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["OBS1013_4_boundary_zero_flux", "MISSING_B_ZERO_FLUX"],
    },
    {
        "source_id": "SRC1731_11_mass_current_contract",
        "source_key": "mass_current_Hamiltonian_contract",
        "source_path": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needles": ["HC4_charge_equals_PiM_Hilbert_mass", "not_parent_derived"],
    },
    {
        "source_id": "SRC1731_12_683_same_frame",
        "source_key": "683_same_frame_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
        "needles": ["SFG683_6_final", "six blocking gates remain open"],
    },
    {
        "source_id": "SRC1731_13_1730_validation",
        "source_key": "1730_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1730_VALIDATION.csv",
        "needles": ["VAL1730_OVERALL", "PASS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_SOURCE_REGISTER.csv",
    "certificate_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_AEXT_CERTIFICATE_AUDIT.csv",
    "geometry_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_AEXT_GEOMETRY_SUPPORT_ROWS.csv",
    "boundary_flux_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_BOUNDARY_FLUX_HANDOFF_ROWS.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_AEXT_SUPPORT_THEOREM_ATTEMPT.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1731_VALIDATION.csv",
}


COPY_MAP = {
    "certificate_audit": "R2FR_1731_AEXT_CERTIFICATE_AUDIT.csv",
    "geometry_rows": "R2FR_1731_AEXT_GEOMETRY_SUPPORT_ROWS.csv",
    "boundary_flux_rows": "R2FR_1731_BOUNDARY_FLUX_HANDOFF_ROWS.csv",
    "theorem_attempt": "R2FR_1731_AEXT_SUPPORT_THEOREM_ATTEMPT.csv",
    "runner_refusal": "R2FR_1731_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1731_DECISION_LEDGER.csv",
    "next_target": "R2FR_1731_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1731_CLAIM_GATE.csv",
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


def certificate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_0_parent_worldtube",
            "certificate_clause": "parent-owned W_source",
            "required_statement": "W_source=closure(supp J_H[tau_obs]) is fixed before readout and has compact regular support.",
            "current_status": "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED",
            "blocking_gap": "1718 keeps parent action, same frame, tau lock, compactness and coupling descent unsigned",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_1_surface_inner",
            "certificate_clause": "inner linked surface S1",
            "required_statement": "S1 links W_source, is fixed before readout, and is not chosen from fitted orbital or R10 success.",
            "current_status": "MISSING_INNER_SURFACE",
            "blocking_gap": "1359/1360 record MISSING_INNER_RADIUS_OR_SURFACE",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_2_surface_outer",
            "certificate_clause": "outer linked surface S2",
            "required_statement": "S2 is homologous to S1 in the source-free exterior and fixed before readout.",
            "current_status": "MISSING_OUTER_SURFACE",
            "blocking_gap": "1359/1360 record MISSING_OUTER_RADIUS_OR_SURFACE",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_3_annulus_homology",
            "certificate_clause": "A_ext compact annulus and homology",
            "required_statement": "A_ext is the compact region between S1 and S2 with boundary S2-S1 and fixed exterior homology class.",
            "current_status": "MISSING_ANNULUS_HOMOLOGY_SOURCE",
            "blocking_gap": "1360 lacks annulus_A, boundary_relation, S1/S2 homology and source-free proof",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_4_support_exclusion",
            "certificate_clause": "A_ext cap W_source empty",
            "required_statement": "A_ext intersects no ordinary matter support and any shell/corner support is retained separately.",
            "current_status": "SUPPORT_EXCLUSION_NOT_SOURCED",
            "blocking_gap": "no local row proves A_ext cap W_source empty or handles distributional boundary stress",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_5_boundary_flux_handoff",
            "certificate_clause": "boundary flux handoff",
            "required_statement": "mass/source information excluded from bulk T_obs is carried by H_tau, M_H_ref, Pi_M J_H, B_zero_flux, Delta_symp, or R_glue rows.",
            "current_status": "BOUNDARY_FLUX_HANDOFF_MISSING",
            "blocking_gap": "662, 1013 and Hamiltonian charge contracts keep M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM chain map unfilled",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_6_same_frame_tau",
            "certificate_clause": "same frame and tau lock",
            "required_statement": "the source support, surface charge, clock normalization and orbit readout use the same e_obs and tau_obs.",
            "current_status": "SAME_FRAME_TAU_LOCK_UNSIGNED",
            "blocking_gap": "683 final gate remains blocked and tau/source-normal lock is still not parent-signed",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AEX1731_7_verdict",
            "certificate_clause": "A_ext source-free certificate verdict",
            "required_statement": "AEX1731_0 through AEX1731_6 all pass before bulk T_obs zero can become evidence.",
            "current_status": "AEXT_SOURCE_FREE_CERTIFICATE_NOT_SIGNED",
            "blocking_gap": "geometry/support and boundary-flux handoff both remain nonclaim ledgers",
            "certificate_signed": no(),
            "valid_for_claim": no(),
        },
    ]


def geometry_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["certificate_audit"]),
        str(RESIDUALS / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv"),
        str(RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "AGS1731_0_W_source",
            "quantity": "W_source",
            "definition": "parent-owned compact source worldtube selected by Hilbert source support",
            "formula": "W_source := closure(supp J_H[tau_obs])",
            "required_inputs": "parent_action;J_H_definition;tau_obs;compact_support;regularity;no_readout_mask;source_path",
            "current_status": "GEOMETRY_SOURCE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_PARENT_ACTION;MISSING_PARENT_SIGNED_JH;MISSING_PARENT_SIGNED_TAU_OBS;MISSING_COMPACT_SUPPORT;MISSING_NO_READOUT_MASK",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_W_SOURCE",
            "units": "worldtube_or_support_identifier_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AGS1731_1_S1_inner_surface",
            "quantity": "S1_or_r1",
            "definition": "inner surface or radius linking W_source",
            "formula": "S1 links W_source and is fixed before readout",
            "required_inputs": "system_id;surface_inner_id;r1;surface_definition;links_W_source;fixed_before_readout;source_path",
            "current_status": "GEOMETRY_SOURCE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_INNER_SURFACE;MISSING_R1;MISSING_LINKS_W_SOURCE;MISSING_FIXED_BEFORE_READOUT;MISSING_SOURCE_PATH",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_INNER_RADIUS_OR_SURFACE",
            "units": "length_or_surface_identifier_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AGS1731_2_S2_outer_surface",
            "quantity": "S2_or_r2",
            "definition": "outer surface or radius homologous to S1 in exterior annulus",
            "formula": "S2 homologous to S1 in Sigma\\W_source and fixed before readout",
            "required_inputs": "system_id;surface_outer_id;r2;surface_definition;homology_class;fixed_before_readout;source_path",
            "current_status": "GEOMETRY_SOURCE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_OUTER_SURFACE;MISSING_R2;MISSING_HOMOLOGY_CLASS;MISSING_FIXED_BEFORE_READOUT;MISSING_SOURCE_PATH",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_OUTER_RADIUS_OR_SURFACE",
            "units": "length_or_surface_identifier_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AGS1731_3_Aext_homology",
            "quantity": "A_ext_and_homology_class",
            "definition": "compact exterior annulus between S1 and S2",
            "formula": "partial A_ext = S2 - S1; A_ext cap W_source = empty; [S1]=[S2] in exterior homology",
            "required_inputs": "system_id;annulus_A;boundary_relation;S1_homology;S2_homology;source_free_certificate;annulus_measure;source_path",
            "current_status": "GEOMETRY_SOURCE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_ANNULUS_A;MISSING_BOUNDARY_RELATION;MISSING_S1_HOMOLOGY;MISSING_S2_HOMOLOGY;MISSING_SOURCE_FREE_CERTIFICATE;MISSING_ANNULUS_MEASURE",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_ANNULUS_HOMOLOGY_SOURCE",
            "units": "topological_class_plus_domain_metadata_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AGS1731_4_support_exclusion",
            "quantity": "A_ext_cap_W_source_empty",
            "definition": "source-free certificate for ordinary matter support in the exterior annulus",
            "formula": "supp(T_obs) cap A_ext = empty in the bulk, with shell/corner terms retained separately",
            "required_inputs": "T_obs_support;A_ext;W_source;regularity_class;surface_distribution_policy;source_path",
            "current_status": "SUPPORT_CERTIFICATE_ROW_TEMPLATE",
            "missing_inputs": "MISSING_TOBS_SUPPORT;MISSING_A_EXT;MISSING_W_SOURCE;MISSING_REGULARITY_CLASS;MISSING_SURFACE_DISTRIBUTION_POLICY;MISSING_SOURCE_PATH",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_SOURCE_FREE_CERTIFICATE",
            "units": "boolean_theorem_or_support_metadata_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def boundary_flux_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["certificate_audit"]),
        str(RESIDUALS / "P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv"),
        str(ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"),
        str(RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
        str(RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "same-frame positive Hamiltonian/source denominator carrying mass outside the vacuum bulk annulus",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref, with fixed reference and tau",
            "required_inputs": "tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path",
            "current_status": "BOUNDARY_HANDOFF_ROW_TEMPLATE",
            "missing_inputs": "MISSING_TAU_ID;MISSING_SURFACE_OUTER;MISSING_Q_TAU_INTEGRAL;MISSING_G_REF;MISSING_H_REF;MISSING_M_H_REF;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_M_H_REF",
            "units": "mass_or_energy_source_charge_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_1_B_zero_flux",
            "quantity": "B_zero_flux",
            "definition": "reference/exact-boundary flux through the linked annulus boundary",
            "formula": "int_boundary dB_zero = 0, or finite source-backed boundary flux coefficient",
            "required_inputs": "boundary_rule;B_zero_flux;surface_pair;corner_terms;M_H_ref;source_path",
            "current_status": "BOUNDARY_HANDOFF_ROW_TEMPLATE",
            "missing_inputs": "MISSING_BOUNDARY_RULE;MISSING_B_ZERO_FLUX;MISSING_SURFACE_PAIR;MISSING_CORNER_TERMS;MISSING_M_H_REF;MISSING_SOURCE_PATH",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_B_ZERO_FLUX",
            "units": "GM_flux_or_dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_2_Delta_symp",
            "quantity": "Delta_symp",
            "definition": "symplectic/reference nonintegrability contribution in the boundary handoff",
            "formula": "Delta_symp = curl_phase_space(delta H_tau) or theorem-zero with fixed boundary conditions",
            "required_inputs": "symplectic_current;boundary_conditions;integrability_certificate;M_H_ref;units;source_path",
            "current_status": "BOUNDARY_HANDOFF_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYMPLECTIC_CURRENT;MISSING_BOUNDARY_CONDITIONS;MISSING_INTEGRABILITY_CERTIFICATE;MISSING_M_H_REF;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DELTA_SYMP",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_3_R_glue",
            "quantity": "R_glue",
            "definition": "residual between Pi_M J_H, topological worldtube current and exact boundary term",
            "formula": "R_glue := Pi_M J_H - J_M_top - dB_zero",
            "required_inputs": "PiM_chain_map;J_H;J_M_top;B_zero;surface_pair;M_H_ref;source_path",
            "current_status": "BOUNDARY_HANDOFF_ROW_TEMPLATE",
            "missing_inputs": "MISSING_PIM_CHAIN_MAP;MISSING_J_H;MISSING_J_M_TOP;MISSING_B_ZERO;MISSING_SURFACE_PAIR;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_R_GLUE",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_4_PiM_chain_map",
            "quantity": "PiM_H_chain_map",
            "definition": "parent-owned Hamiltonian mass-charge projector map for the linked surfaces",
            "formula": "int_S Pi_M J_H = 4*pi*G_ref(H_tau[S]-H_ref), with [d,Pi_M]J_H=0 or retained",
            "required_inputs": "PiM_definition;Q_tau;surface_pair;commutator_zero_or_bound;M_H_ref;source_path",
            "current_status": "BOUNDARY_HANDOFF_ROW_TEMPLATE",
            "missing_inputs": "MISSING_PIM_DEFINITION;MISSING_Q_TAU;MISSING_SURFACE_PAIR;MISSING_ICOMMUTATOR_ZERO_OR_BOUND;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_PIM_H_CHAIN_MAP",
            "units": "operator_or_charge_map_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFH1731_5_handoff_acceptance",
            "quantity": "boundary_flux_handoff_acceptance",
            "definition": "acceptance gate for using bulk T_obs zero without erasing source mass",
            "formula": "pass iff M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM_H_chain_map are source-backed or theorem-zero",
            "required_inputs": "BFH1731_0 through BFH1731_4 all nonmissing and same-frame",
            "current_status": "CLAIM_BLOCKED",
            "missing_inputs": "MISSING_BOUNDARY_FLUX_HANDOFF_STACK",
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
            "attempt_id": "AST1731_0_geometry_antecedent",
            "statement": "If W_source is parent-owned, S1/S2 are fixed linked surfaces, and A_ext cap W_source is empty, the bulk annulus is source-free.",
            "current_status": "CONDITIONAL_THEOREM_SHAPE",
            "current_blocker": "geometry/source rows AGS1731_0 through AGS1731_4 are all missing or conditional",
            "would_close": "bulk T_obs zero antecedent",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "AST1731_1_bulk_Tobs_zero",
            "statement": "If the geometry antecedent and same-frame ordinary T_obs definition are signed, T_obs|A_ext=0 in the bulk.",
            "current_status": "CONDITIONAL_EFFECT_ONLY",
            "current_blocker": "same-frame T_obs/J_H and tau lock remain unsigned",
            "would_close": "bulk C_Tobs_tau zero",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "AST1731_2_boundary_handoff",
            "statement": "Bulk T_obs zero is legal only when H_tau/M_H_ref/PiM/boundary flux rows carry the excluded mass information.",
            "current_status": "HANDOFF_NOT_FILLED",
            "current_blocker": "boundary flux rows BFH1731_0 through BFH1731_5 are nonclaim templates",
            "would_close": "mass preservation guard for vacuum exterior route",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "AST1731_3_current_verdict",
            "statement": "Current MTS cannot yet claim A_ext source-free or bulk C_Tobs_tau=0.",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "A_ext certificate and boundary-flux handoff are both unsigned",
            "would_close": "no local-GR promotion; retain finite/nonclaim Tobs norm path",
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1731_0_Aext_certificate",
            "quantity": "A_ext source-free certificate",
            "runner_decision": "REFUSE_CLAIM",
            "refusal_reasons": "MISSING_W_SOURCE;MISSING_S1;MISSING_S2;MISSING_AEXT_HOMOLOGY;MISSING_SUPPORT_EXCLUSION;MISSING_SAME_FRAME_TAU_LOCK",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1731_1_boundary_handoff",
            "quantity": "boundary flux handoff",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "MISSING_M_H_REF;MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_PIM_CHAIN_MAP",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1731_2_C_Tobs_tau_zero",
            "quantity": "bulk C_Tobs_tau theorem-zero",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "AEXT_SOURCE_FREE_CERTIFICATE_NOT_SIGNED;BOUNDARY_FLUX_HANDOFF_MISSING",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1731_3_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_AEXT_CERTIFICATE;NO_BOUNDARY_HANDOFF;NO_MHREF;NO_SOURCE_NORMALIZATION;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1731_0_certificate_status",
            "decision": "do not sign A_ext source-free certificate",
            "because": "W_source, S1, S2, homology, support exclusion, same-frame tau and boundary flux are all unsigned",
            "next_action": "use geometry/support rows as the exact certificate checklist",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1731_1_boundary_handoff_priority",
            "decision": "boundary flux handoff is the next derivation bottleneck",
            "because": "even if the exterior bulk is vacuum, GR recovers mass through a surface/Hamiltonian charge rather than local matter stress",
            "next_action": "derive or source M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM_H_chain_map",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1731_2_geometry_parallel",
            "decision": "keep S1/S2/A_ext geometry intake parallel",
            "because": "surface data are necessary, but without boundary handoff they can only prove empty exterior, not measured mass or local GR",
            "next_action": "parallel row can fill surface identifiers and support metadata without scoring",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1731_0_primary",
            "next_target": "1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md",
            "script": "scripts/Y5_R2FR_boundary_flux_handoff_to_Htau_or_MHref_source_row.py",
            "objective": "derive the boundary/Hamiltonian handoff that carries source mass when bulk T_obs vanishes, or fill nonclaim M_H_ref/B_zero_flux/Delta_symp/R_glue/PiM rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1731_1_parallel_geometry_intake",
            "next_target": "1732b-Y5-R2FR-Aext-geometry-support-intake-row.md",
            "script": "scripts/Y5_R2FR_Aext_geometry_support_intake_row.py",
            "objective": "fill W_source, S1, S2, A_ext support-exclusion and homology metadata as nonclaim geometry rows",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1731_2_later_CdeltaTau",
            "next_target": "1733-Y5-R2FR-CdeltaTau-source-piece-stack-runner.md",
            "script": "scripts/Y5_R2FR_CdeltaTau_source_piece_stack_runner.py",
            "objective": "combine Z_Tobs_Aext or sup_A_Tobs with C_Tobs_tau only after geometry and boundary handoff close",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1731_0_Aext_source_free",
            "claim": "A_ext is parent-certified source-free",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "AEX1731_7 says the A_ext source-free certificate is not signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1731_1_boundary_handoff",
            "claim": "boundary/Hamiltonian handoff carries the excluded source mass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "BFH1731 rows have missing M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM chain map",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1731_2_bulk_C_Tobs_zero",
            "claim": "bulk C_Tobs_tau is theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "geometry and boundary handoff certificates are both missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1731_3_Tobs_finite_source",
            "claim": "sup_A ||T_obs||_op finite row can score",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "A_ext geometry, norm units and stress bound remain unfilled",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1731_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no A_ext certificate, no boundary handoff, no source-normalization denominator, PPN vector open",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "certificate_audit": certificate_audit_rows(),
        "geometry_rows": geometry_rows(),
        "boundary_flux_rows": boundary_flux_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1731_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1731_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "certificate_signed"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def rows_missing_and_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text and row.get("current_status") != "CLAIM_BLOCKED":
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1731_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1731_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1731*"):
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
    certificate = rows_map["certificate_audit"]
    geometry = rows_map["geometry_rows"]
    boundary = rows_map["boundary_flux_rows"]
    theorem = rows_map["theorem_attempt"]
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
        check("VAL1731_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1731_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1731_2_1730_handoff_preserved",
            any(row["source_key"] == "1730_next_target" and row["needles_present"] == "True" for row in source_register),
            "1730 selected Aext support/boundary handoff route",
            "1730 handoff missing",
        ),
        check(
            "VAL1731_3_certificate_audit_complete",
            {row["certificate_clause"] for row in certificate}
            >= {
                "parent-owned W_source",
                "inner linked surface S1",
                "outer linked surface S2",
                "A_ext compact annulus and homology",
                "A_ext cap W_source empty",
                "boundary flux handoff",
                "same frame and tau lock",
                "A_ext source-free certificate verdict",
            },
            "certificate audit covers worldtube, surfaces, annulus, support, boundary handoff, frame/tau and verdict",
            "certificate audit missing required clause",
        ),
        check(
            "VAL1731_4_certificate_blocked",
            any(row["audit_id"] == "AEX1731_7_verdict" and row["current_status"] == "AEXT_SOURCE_FREE_CERTIFICATE_NOT_SIGNED" for row in certificate),
            "Aext source-free certificate remains unsigned",
            "Aext verdict missing or claim-enabled",
        ),
        check(
            "VAL1731_5_geometry_rows_nonclaim",
            len(geometry) == 5 and rows_missing_and_nonclaim(geometry),
            "geometry/support rows carry missing markers and remain nonclaim",
            "geometry/support rows malformed or claim-enabled",
        ),
        check(
            "VAL1731_6_boundary_rows_nonclaim",
            len(boundary) == 6 and rows_missing_and_nonclaim(boundary),
            "boundary flux handoff rows carry missing markers and remain nonclaim",
            "boundary flux rows malformed or claim-enabled",
        ),
        check(
            "VAL1731_7_theorem_fails_current_claim",
            any(row["attempt_id"] == "AST1731_3_current_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt explicitly fails current claim",
            "theorem attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1731_8_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals}
            >= {"A_ext source-free certificate", "boundary flux handoff", "bulk C_Tobs_tau theorem-zero", "Newton/local-GR reduction"},
            "runner refusals cover Aext, handoff, C_Tobs and local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1731_9_decision_next",
            any(row["decision_id"] == "DEC1731_1_boundary_handoff_priority" for row in decisions),
            "decision selects boundary handoff priority",
            "boundary handoff priority decision missing",
        ),
        check(
            "VAL1731_10_next_selected",
            any(row["route_id"] == "NEXT1731_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1732 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1731_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1731_12_csv_parse", parsed_ok, "all generated 1731 CSVs parse", "one or more generated 1731 CSVs failed to parse"),
        check("VAL1731_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1731_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1731_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1731_16_formalization_untouched", formalization_untouched(), "no 1731 outputs found under formalization-workbench", "1731 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1731_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1731 Aext/boundary flux validation" if overall else "one or more 1731 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1731 tries to sign the full `A_ext` source-free certificate needed by the vacuum-annulus route.",
        "- Current result: the certificate is **not signed**. `W_source`, `S1`, `S2`, `A_ext cap W_source`, same-frame/tau lock, and boundary-flux handoff are all still missing or conditional.",
        "- Useful progress: the missing object is now split into two precise nonclaim ledgers: geometry/support rows and boundary/Hamiltonian handoff rows.",
        "- This protects the good GR-like idea: exterior bulk `T_obs=0` is allowed only if source mass reappears through `H_tau/M_H_ref/PiM/boundary` data.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Conditional Logic",
        "The route is still alive: a source-free exterior annulus can kill the bulk `T_obs` contribution to `C_Tobs_tau`. But this does not by itself derive Newton/GR. The source mass must be carried by a parent-owned boundary or Hamiltonian charge. So the next bottleneck is not just drawing `S1` and `S2`; it is proving the boundary-flux handoff.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Aext Certificate Audit",
        markdown_table(rows_map["certificate_audit"], ["audit_id", "certificate_clause", "current_status", "blocking_gap", "certificate_signed", "valid_for_claim"]),
        "",
        "## Geometry Support Rows",
        markdown_table(rows_map["geometry_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Boundary Flux Handoff Rows",
        markdown_table(rows_map["boundary_flux_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
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
        "1731 keeps the good route alive and blocks the bad shortcut. If we can derive the boundary/Hamiltonian handoff, then a vacuum exterior annulus becomes a strength rather than a loophole: no bulk matter stress outside the source, but a nonzero mass charge on the boundary. If we cannot derive it, `C_Tobs_tau` stays finite/nonclaim and local GR remains blocked. Next shot: derive or source the boundary handoff stack.",
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
    doc_path = ROOT / "1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1731_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1731 validation FAIL")
    print("1731 validation PASS")


if __name__ == "__main__":
    main()
