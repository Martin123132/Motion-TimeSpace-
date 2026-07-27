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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1732"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1732 - Boundary Flux Handoff To Htau Or MHref Source Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1732_0_1731_doc",
        "source_key": "1731_doc",
        "source_path": ROOT / "1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md",
        "needles": ["NEXT1731_0_primary", "boundary/Hamiltonian handoff"],
    },
    {
        "source_id": "SRC1732_1_1731_next",
        "source_key": "1731_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_NEXT_TARGET.csv",
        "needles": ["1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md", "selected"],
    },
    {
        "source_id": "SRC1732_2_1731_handoff_rows",
        "source_key": "1731_boundary_handoff_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_BOUNDARY_FLUX_HANDOFF_ROWS.csv",
        "needles": ["BFH1731_0_M_H_ref", "MISSING_M_H_REF"],
    },
    {
        "source_id": "SRC1732_3_457_doc",
        "source_key": "457_hamiltonian_boundary_charge_doc",
        "source_path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needles": ["conditional_Hamiltonian_boundary_charge_theorem", "not_parent_derived"],
    },
    {
        "source_id": "SRC1732_4_hamiltonian_contract",
        "source_key": "hamiltonian_boundary_charge_contract",
        "source_path": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needles": ["HC4_charge_equals_PiM_Hilbert_mass", "not_parent_derived"],
    },
    {
        "source_id": "SRC1732_5_664_integrability",
        "source_key": "664_integrability_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        "needles": ["HCI664_6_integrability_verdict", "fail_current_claim"],
    },
    {
        "source_id": "SRC1732_6_1017_reference_lock",
        "source_key": "1017_reference_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
        "needles": ["HRL1017_6_FB5540_zero_law", "fail_current_claim"],
    },
    {
        "source_id": "SRC1732_7_1017_mhref_schema",
        "source_key": "1017_mhref_first_row_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
        "needles": ["MHR1017_0_M_H_ref_denominator", "MISSING_STABLE_MH_REF"],
    },
    {
        "source_id": "SRC1732_8_1017_claim_gate",
        "source_key": "1017_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1017_CLAIM_GATE.csv",
        "needles": ["CG1017_6_Newton_local_GR", "stable Hamiltonian source charge is not derived"],
    },
    {
        "source_id": "SRC1732_9_boundary_reference_status",
        "source_key": "boundary_reference_first_row_status",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["B_zero_flux", "missing_claim_valid_source_or_zero_theorem"],
    },
    {
        "source_id": "SRC1732_10_1013_obstruction_doc",
        "source_key": "1013_PiM_JH_flux_obstructions",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["OBS1013_4_boundary_zero_flux", "MISSING_B_ZERO_FLUX"],
    },
    {
        "source_id": "SRC1732_11_1646_theta_Qtau_owner",
        "source_key": "1646_theta_Qtau_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "needles": ["TQ1646_5_owner_verdict", "FAIL_CURRENT_CLAIM"],
    },
    {
        "source_id": "SRC1732_12_1731_validation",
        "source_key": "1731_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1731_VALIDATION.csv",
        "needles": ["VAL1731_OVERALL", "PASS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_SOURCE_REGISTER.csv",
    "handoff_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_HANDOFF_THEOREM_AUDIT.csv",
    "htau_mhref_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
    "boundary_component_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_BOUNDARY_FLUX_COMPONENT_ROWS.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_HANDOFF_THEOREM_ATTEMPT.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1732_VALIDATION.csv",
}


COPY_MAP = {
    "handoff_audit": "R2FR_1732_HANDOFF_THEOREM_AUDIT.csv",
    "htau_mhref_rows": "R2FR_1732_HTAU_MHREF_SOURCE_ROWS.csv",
    "boundary_component_rows": "R2FR_1732_BOUNDARY_FLUX_COMPONENT_ROWS.csv",
    "theorem_attempt": "R2FR_1732_HANDOFF_THEOREM_ATTEMPT.csv",
    "runner_refusal": "R2FR_1732_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1732_DECISION_LEDGER.csv",
    "next_target": "R2FR_1732_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1732_CLAIM_GATE.csv",
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


def handoff_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_0_EH_exterior",
            "handoff_clause": "same-frame EH exterior constraint algebra",
            "required_statement": "The compact observed local exterior reduces to EH constraints plus boundary terms in the same frame.",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "blocking_gap": "HC0 is conditional; no parent action proof has signed the EH-only exterior ladder for this local branch.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_1_tau_generator",
            "handoff_clause": "observed time generator",
            "required_statement": "One tau/xi generates source variation, Hamiltonian charge, clocks and readout with fixed normalization.",
            "current_status": "NOT_PARENT_DERIVED",
            "blocking_gap": "HC1, HRL1017_4 and TQ1646 keep observed tau split across source, charge and readout branches.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_2_theta_Qtau",
            "handoff_clause": "parent symplectic potential and Noether charge",
            "required_statement": "Current MTS supplies L_parent, Theta_total and Q_tau^MTS before any surface charge is scored.",
            "current_status": "THETA_QTAU_OWNER_FAIL_CURRENT_CLAIM",
            "blocking_gap": "TQ1646_5 says the current owner remains a scaffold; Q_tau and C_tau are not extracted for retained sectors.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_3_integrability_reference",
            "handoff_clause": "integrable H_tau and fixed reference",
            "required_statement": "delta H_tau = int_S(delta Q_tau - i_tau Theta_total) - delta H_ref is finite, curl-free, and reference-silent.",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocking_gap": "HCI664_6 and HRL1017_1/2 keep integrability curl and reference lock open.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_4_boundary_flux_zero",
            "handoff_clause": "boundary and symplectic leakage controlled",
            "required_statement": "B_zero_flux, Delta_symp, corner, class and projector-boundary leakage are theorem-zero or retained as sourced residuals.",
            "current_status": "MISSING_CLAIM_VALID_SOURCE_OR_ZERO_THEOREM",
            "blocking_gap": "1013, 1017 and the boundary first-row status keep B_zero_flux and Delta_symp nonclaim.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_5_PiM_Hilbert_equality",
            "handoff_clause": "PiM Hilbert source equals Hamiltonian charge",
            "required_statement": "The surface Hamiltonian charge equals the parent-defined projected Hilbert mass current.",
            "current_status": "NOT_PARENT_DERIVED",
            "blocking_gap": "HC4 is not parent-derived; Pi_M variation ownership and source-current Ward identity are not signed.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_6_no_extra_charge",
            "handoff_clause": "no extra hidden charge",
            "required_statement": "Non-EH, projector, boundary, domain, memory, range and coupling sectors carry no unowned mass charge or are retained.",
            "current_status": "FAIL_OPEN",
            "blocking_gap": "HC5 remains fail-open; mu_extra and source hair remain active.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_7_constant_Geff_Gauss",
            "handoff_clause": "constant coupling and Poisson/Gauss/orbital calibration",
            "required_statement": "The charge normalization uses constant G_eff and reduces to measured Newtonian GM.",
            "current_status": "NOT_PARENT_DERIVED",
            "blocking_gap": "HC7-HC8 remain conditional/not-derived; measured-GM calibration is downstream.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BHA1732_8_verdict",
            "handoff_clause": "boundary/Hamiltonian handoff verdict",
            "required_statement": "BHA1732_0 through BHA1732_7 all pass before exterior bulk-vacuum can be promoted to local GR.",
            "current_status": "HANDOFF_NOT_SIGNED",
            "blocking_gap": "the route is GR-like and mathematically clean, but every current-MTS ownership piece is still downstream or nonclaim.",
            "handoff_signed": no(),
            "valid_for_claim": no(),
        },
    ]


def htau_mhref_source_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["handoff_audit"]),
        str(ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md"),
        str(RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
        str(RESIDUALS / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HMS1732_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "positive same-frame Hamiltonian/source denominator carrying source mass outside the vacuum bulk annulus",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref with fixed tau, frame, surface and reference",
            "required_inputs": "system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path",
            "current_status": "MISSING_STABLE_MH_REF",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_TAU_ID;MISSING_SURFACE_OUTER;MISSING_Q_TAU_INTEGRAL;MISSING_G_REF;MISSING_H_REF;MISSING_M_H_REF;MISSING_UNITS;MISSING_REFERENCE_RULE",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_M_H_REF",
            "units": "mass_or_energy_source_charge_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HMS1732_1_delta_H_tau",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "field-space curl obstruction of the Hamiltonian source charge normalized by M_H_ref",
            "formula": "I_tau(delta1,delta2) := curl(delta H_tau) = int_S i_tau omega_total + curl(delta H_ref)",
            "required_inputs": "Theta_total;Q_tau;omega_total;field_variation_pair;boundary_conditions;M_H_ref;units;source_path",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_THETA_TOTAL;MISSING_Q_TAU;MISSING_OMEGA_TOTAL;MISSING_FIELD_VARIATION_PAIR;MISSING_BOUNDARY_CONDITIONS;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DELTA_H_TAU_NONINTEGRABLE",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HMS1732_2_PiM_H_chain_map",
            "quantity": "PiM_H_chain_map",
            "definition": "parent-owned map identifying the projected Hilbert source current with the Hamiltonian surface charge",
            "formula": "int_S Pi_M J_H = 4*pi*G_ref*(H_tau[S]-H_ref) with [d,Pi_M]J_H theorem-zero or retained",
            "required_inputs": "PiM_definition;J_H;Q_tau;surface_pair;G_ref;commutator_zero_or_bound;M_H_ref;source_path",
            "current_status": "MISSING_PIM_H_CHAIN_MAP",
            "missing_inputs": "MISSING_PIM_DEFINITION;MISSING_J_H;MISSING_Q_TAU;MISSING_SURFACE_PAIR;MISSING_G_REF;MISSING_ICOMMUTATOR_ZERO_OR_BOUND;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_PIM_H_CHAIN_MAP",
            "units": "operator_or_charge_map_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HMS1732_3_Poisson_Gauss_bridge",
            "quantity": "measured_GM_calibration",
            "definition": "weak-field bridge from Hamiltonian surface charge to the Newtonian source measured by orbits",
            "formula": "GM_obs = G_eff*(4*pi*G_eff)^-1*int_S grad Phi dot dS plus retained hidden-charge corrections",
            "required_inputs": "weak_field_EH_limit;constant_G_eff;no_hidden_charge_or_mu_extra;slow_particle_geodesic_limit;orbit_readout;source_path",
            "current_status": "MISSING_MEASURED_GM_CALIBRATION",
            "missing_inputs": "MISSING_WEAK_FIELD_EH_LIMIT;MISSING_CONSTANT_GEFF;MISSING_NO_HIDDEN_CHARGE_OR_MU_EXTRA;MISSING_GEODESIC_LIMIT;MISSING_ORBIT_READOUT",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_GM_CALIBRATION",
            "units": "GM_or_dimensionless_after_reference_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def boundary_component_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["handoff_audit"]),
        str(RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"),
        str(RESIDUALS / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv"),
        str(ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"),
        str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFC1732_0_B_zero_flux",
            "quantity": "B_zero_flux",
            "definition": "exact/reference/boundary improvement flux through compact linked surfaces",
            "formula": "int_boundary dB_zero = 0 or |B_zero_flux|/M_H_ref sourced as a retained residual",
            "required_inputs": "boundary_rule;surface_pair;corner_terms;B_zero_flux;M_H_ref;units;source_path",
            "current_status": "MISSING_CLAIM_VALID_SOURCE_OR_ZERO_THEOREM",
            "missing_inputs": "MISSING_BOUNDARY_RULE;MISSING_SURFACE_PAIR;MISSING_CORNER_TERMS;MISSING_B_ZERO_FLUX;MISSING_M_H_REF;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_B_ZERO_FLUX",
            "units": "GM_flux_or_dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFC1732_1_Delta_symp",
            "quantity": "Delta_symp",
            "definition": "symplectic/reference leakage in the Hamiltonian handoff",
            "formula": "Delta_symp := int_boundary(delta Q_tau^extra - i_tau Theta_extra) + delta B_class",
            "required_inputs": "Theta_extra;Q_tau_extra;boundary_conditions;B_class;M_H_ref;units;source_path",
            "current_status": "MISSING_CLAIM_VALID_SOURCE_OR_ZERO_THEOREM",
            "missing_inputs": "MISSING_THETA_EXTRA;MISSING_Q_TAU_EXTRA;MISSING_BOUNDARY_CONDITIONS;MISSING_B_CLASS;MISSING_DELTA_SYMP;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DELTA_SYMP",
            "units": "dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFC1732_2_R_glue",
            "quantity": "R_glue",
            "definition": "glue residual between Pi_M J_H, topological worldtube current and exact boundary term",
            "formula": "R_glue := Pi_M J_H - J_M_top - dB_zero",
            "required_inputs": "PiM_chain_map;J_H;J_M_top;B_zero;surface_pair;M_H_ref;source_path",
            "current_status": "MISSING_R_GLUE",
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
            "row_id": "BFC1732_3_delta_H_tau_nonintegrable",
            "quantity": "delta_H_tau_nonintegrable",
            "definition": "nonintegrable Hamiltonian variation numerator before M_H_ref normalization",
            "formula": "delta_H_tau_nonintegrable := curl_phase_space int_S(delta Q_tau - i_tau Theta_total - delta H_ref)",
            "required_inputs": "Theta_total;Q_tau;H_ref;field_variation_pair;surface_pair;M_H_ref;source_path",
            "current_status": "MISSING_DELTA_H_TAU_NONINTEGRABLE",
            "missing_inputs": "MISSING_THETA_TOTAL;MISSING_Q_TAU;MISSING_H_REF;MISSING_FIELD_VARIATION_PAIR;MISSING_SURFACE_PAIR;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DELTA_H_TAU_NONINTEGRABLE",
            "units": "energy_or_dimensionless_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFC1732_4_extra_charge_vector",
            "quantity": "mu_extra_boundary_charge_vector",
            "definition": "retained non-EH/projector/domain/memory/range/coupling charge channels that can mimic source mass",
            "formula": "mu_extra := Q_nonEH + Q_PiM + Q_boundary + Q_domain + Q_memory + Q_range + Q_delta_kappa",
            "required_inputs": "nonEH_charge;projector_charge;boundary_charge;domain_charge;memory_charge;range_charge;coupling_charge;M_H_ref;source_path",
            "current_status": "MISSING_EXTRA_CHARGE_VECTOR",
            "missing_inputs": "MISSING_NON_EH_CHARGE;MISSING_PROJECTOR_CHARGE;MISSING_BOUNDARY_CHARGE;MISSING_DOMAIN_CHARGE;MISSING_MEMORY_CHARGE;MISSING_RANGE_CHARGE;MISSING_COUPLING_CHARGE;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_MU_EXTRA_VECTOR",
            "units": "dimensionless_or_GM_flux_after_MHref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BFC1732_5_total_handoff_abs",
            "quantity": "epsilon_boundary_handoff_abs",
            "definition": "no-cancellation boundary handoff residual envelope",
            "formula": "(|B_zero_flux|+|Delta_symp|+|R_glue|+|delta_H_tau_nonintegrable|+|mu_extra|)/M_H_ref",
            "required_inputs": "BFC1732_0 through BFC1732_4;positive_M_H_ref;common_units;source_path",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "missing_inputs": "MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_DELTA_H_TAU_NONINTEGRABLE;MISSING_MU_EXTRA_VECTOR;MISSING_M_H_REF",
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
            "attempt_id": "BHT1732_0_conditional_route",
            "statement": "If the parent local branch supplies EH exterior constraints, fixed tau, Theta/Q_tau, integrable H_tau, no extra charge, constant G_eff and Poisson/Gauss calibration, then exterior bulk vacuum can coexist with nonzero measured mass through a boundary charge.",
            "mathematical_form": "H_tau[Omega]=int_Omega tau*C + int_boundary Q_tau - H_ref; C=0; H_tau-H_ref=G_eff*M_eff after calibration",
            "current_status": "VALID_CONDITIONAL_GR_LIKE_ROUTE",
            "current_blocker": "condition chain is not parent-signed for current MTS",
            "would_close": "boundary handoff route becomes a real local-GR/Newton bridge",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BHT1732_1_current_MTS_inputs",
            "statement": "Current MTS supplies enough parent current data to instantiate the conditional route.",
            "mathematical_form": "delta L_parent = E delta Phi + dTheta_total and J_tau=dQ_tau+C_tau with every retained sector included",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "TQ1646_5 keeps Theta_total/Q_tau current owner unsigned",
            "would_close": "H_tau variation becomes computable instead of a named placeholder",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BHT1732_2_mass_identity",
            "statement": "The boundary charge equals the projected Hilbert/Newton source mass.",
            "mathematical_form": "int_S Pi_M J_H = 4*pi*G_ref*(H_tau-H_ref) and GM_obs=G_eff*M_charge",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "HC4-HC8 remain not parent-derived or fail-open",
            "would_close": "measured GM would no longer be an inserted source-normalization closure",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BHT1732_3_no_leakage",
            "statement": "Extra boundary, projector, non-EH, domain, memory, range and coupling charges vanish or are retained in a finite residual vector.",
            "mathematical_form": "B_zero_flux=Delta_symp=R_glue=mu_extra=0 or epsilon_boundary_handoff_abs is sourced",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "B_zero_flux, Delta_symp, R_glue, mu_extra and M_H_ref are missing/nonclaim",
            "would_close": "bulk-vacuum route would preserve mass without hiding sector hair",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BHT1732_4_current_verdict",
            "statement": "The 1732 boundary/Hamiltonian handoff is signed for current MTS.",
            "mathematical_form": "BHA1732_0...BHA1732_7 all true and HMS/BFC rows nonmissing in common units",
            "current_status": "FAIL_CURRENT_CLAIM",
            "current_blocker": "the handoff is cleanly specified but not derived; source rows remain placeholders with explicit blockers",
            "would_close": "reactivate local-GR/Newton derivation gate",
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1732_0_bulk_vacuum_to_mass",
            "quantity": "bulk-vacuum exterior to nonzero source mass",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_PARENT_SIGNED_HTAU;NO_MHREF;NO_PIM_HILBERT_EQUALITY;NO_GAUSS_CALIBRATION",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1732_1_Htau_integrability",
            "quantity": "H_tau integrability and reference lock",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_THETA_TOTAL;MISSING_Q_TAU;MISSING_H_REF_LOCK;MISSING_INTEGRABILITY_CURL_ZERO",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1732_2_boundary_handoff_residual",
            "quantity": "epsilon_boundary_handoff_abs",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_MU_EXTRA_VECTOR;MISSING_M_H_REF",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1732_3_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "HANDOFF_NOT_SIGNED;SOURCE_CHARGE_NOT_MEASURED_GM;PPN_VECTOR_OPEN;R10_LOCAL_BRANCH_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1732_0_conditional_route_kept",
            "decision": "keep the boundary/Hamiltonian route as the cleanest GR-like handoff",
            "because": "it explains how exterior bulk vacuum can still carry source mass through a surface charge rather than local matter stress",
            "next_action": "derive the parent Theta/Q_tau owner before trying to score M_H_ref",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1732_1_no_claim",
            "decision": "do not claim local GR/Newton or source-normalization closure",
            "because": "H_tau, M_H_ref, PiM-Hilbert equality, boundary leakage and measured-GM calibration are all unsigned",
            "next_action": "keep HMS1732 and BFC1732 rows as nonclaim source-ready ledgers",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1732_2_next_bottleneck",
            "decision": "Theta_total/Q_tau current ownership is the next derivation bottleneck",
            "because": "without parent symplectic potential and Noether charge, H_tau cannot be computed or tested",
            "next_action": "attempt 1733 parent theta-Q_tau current-owner derivation or produce the first H_tau component row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1732_0_primary",
            "next_target": "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
            "script": "scripts/Y5_R2FR_parent_theta_Qtau_current_owner_or_Htau_first_row.py",
            "objective": "derive/extract the parent MTS Theta_total and Q_tau current owner for observed time, or fill first nonclaim H_tau component source rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1732_1_parallel_MHref_pack",
            "next_target": "1733b-Y5-R2FR-MHref-denominator-source-pack.md",
            "script": "scripts/Y5_R2FR_MHref_denominator_source_pack.py",
            "objective": "stage system_id, tau_id, surface_outer, Q_tau_integral, G_ref, H_ref, M_H_ref and units rows without claim promotion",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1732_2_later_residual_stack",
            "next_target": "1734-Y5-R2FR-CdeltaTau-source-piece-stack-runner.md",
            "script": "scripts/Y5_R2FR_CdeltaTau_source_piece_stack_runner.py",
            "objective": "combine C_Tobs_tau, C_delta_tau and boundary handoff terms only after parent current ownership improves",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1732_0_boundary_handoff",
            "claim": "boundary/Hamiltonian handoff carries excluded source mass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "BHA1732_8 verdict is HANDOFF_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1732_1_Htau_integrability",
            "claim": "H_tau is finite, integrable and reference-locked",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Theta_total, Q_tau, omega_total, H_ref lock and integrability curl are missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1732_2_MHref",
            "claim": "M_H_ref is a positive stable same-frame source denominator",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "HMS1732_0 keeps M_H_ref as MISSING_STABLE_MH_REF",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1732_3_boundary_residual_zero",
            "claim": "B_zero_flux, Delta_symp, R_glue and mu_extra vanish",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "BFC1732 rows are missing/nonclaim and no theorem-zero is signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1732_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived through the boundary charge",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source charge is not yet proved equal to measured GM and PPN/R10 local branches remain open",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "handoff_audit": handoff_audit_rows(),
        "htau_mhref_rows": htau_mhref_source_rows(),
        "boundary_component_rows": boundary_component_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1732_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1732_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "handoff_signed"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def rows_missing_and_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text and "BLOCKED" not in row_text:
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1732_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1732_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1732*"):
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
    handoff_audit = rows_map["handoff_audit"]
    htau_rows = rows_map["htau_mhref_rows"]
    boundary_rows = rows_map["boundary_component_rows"]
    theorem_rows = rows_map["theorem_attempt"]
    runner_rows = rows_map["runner_refusal"]
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
        check("VAL1732_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1732_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1732_2_1731_route_preserved",
            any(row["source_key"] == "1731_next_target" and row["needles_present"] == "True" for row in source_register),
            "1731 selected the boundary/Hamiltonian handoff route",
            "1731 handoff route missing",
        ),
        check(
            "VAL1732_3_handoff_audit_complete",
            {row["handoff_clause"] for row in handoff_audit}
            >= {
                "same-frame EH exterior constraint algebra",
                "observed time generator",
                "parent symplectic potential and Noether charge",
                "integrable H_tau and fixed reference",
                "boundary and symplectic leakage controlled",
                "PiM Hilbert source equals Hamiltonian charge",
                "no extra hidden charge",
                "constant coupling and Poisson/Gauss/orbital calibration",
                "boundary/Hamiltonian handoff verdict",
            },
            "handoff audit covers EH, tau, Theta/Q_tau, integrability, boundary leakage, PiM, hidden charge, coupling/Gauss and verdict",
            "handoff audit missing a required clause",
        ),
        check(
            "VAL1732_4_handoff_blocked",
            any(row["audit_id"] == "BHA1732_8_verdict" and row["current_status"] == "HANDOFF_NOT_SIGNED" for row in handoff_audit),
            "handoff verdict remains unsigned",
            "handoff verdict missing or claim-enabled",
        ),
        check(
            "VAL1732_5_htau_rows_nonclaim",
            len(htau_rows) == 4 and rows_missing_and_nonclaim(htau_rows),
            "H_tau/M_H_ref source rows carry missing markers and remain nonclaim",
            "H_tau/M_H_ref rows malformed or claim-enabled",
        ),
        check(
            "VAL1732_6_boundary_rows_nonclaim",
            len(boundary_rows) == 6 and rows_missing_and_nonclaim(boundary_rows),
            "boundary component rows carry missing markers and remain nonclaim",
            "boundary component rows malformed or claim-enabled",
        ),
        check(
            "VAL1732_7_theorem_fails_current_claim",
            any(row["attempt_id"] == "BHT1732_4_current_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem_rows),
            "theorem attempt explicitly fails current claim",
            "theorem attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1732_8_runner_refusals_cover_chain",
            {row["quantity"] for row in runner_rows}
            >= {"bulk-vacuum exterior to nonzero source mass", "H_tau integrability and reference lock", "epsilon_boundary_handoff_abs", "Newton/local-GR reduction"},
            "runner refusals cover mass handoff, H_tau, boundary residual and local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1732_9_decision_next",
            any(row["decision_id"] == "DEC1732_2_next_bottleneck" for row in decision),
            "decision selects Theta/Q_tau current ownership as next bottleneck",
            "next bottleneck decision missing",
        ),
        check(
            "VAL1732_10_next_selected",
            any(row["route_id"] == "NEXT1732_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1733 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1732_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1732_12_csv_parse", parsed_ok, "all generated 1732 CSVs parse", "one or more generated 1732 CSVs failed to parse"),
        check("VAL1732_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1732_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1732_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1732_16_formalization_untouched", formalization_untouched(), "no 1732 outputs found under formalization-workbench", "1732 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1732_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1732 boundary/Hamiltonian handoff validation" if overall else "one or more 1732 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1732 tries the clean GR-like route: source mass leaves the exterior bulk stress but reappears as a Hamiltonian/boundary surface charge.",
        "- Current result: the route is mathematically coherent as a conditional handoff, but it is **not signed for current MTS**.",
        "- The hard missing object is now sharper: parent-owned `Theta_total` and `Q_tau` for the observed time generator must be extracted before `H_tau` or `M_H_ref` can score.",
        "- `M_H_ref`, `B_zero_flux`, `Delta_symp`, `R_glue`, `delta_H_tau_nonintegrable`, and `mu_extra` are staged as source-ready nonclaim rows.",
        "- No R10, WEP, PPN, clock, orbital, Newton, local-GR, `q_loc=0`, `M_H_ref`, or measured-GM claim is made.",
        "",
        "## Derivation Read",
        "The handoff is the right boxing footwork: it prevents the theory from pretending that exterior bulk vacuum erases mass. In GR the mass is not a local exterior matter stress; it is carried by constraints and boundary charge. MTS can use the same style only if the parent action supplies the current machinery rather than naming the charge by hand.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Handoff Audit",
        markdown_table(rows_map["handoff_audit"], ["audit_id", "handoff_clause", "current_status", "blocking_gap", "handoff_signed", "valid_for_claim"]),
        "",
        "## Htau And MHref Source Rows",
        markdown_table(rows_map["htau_mhref_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Boundary Component Rows",
        markdown_table(rows_map["boundary_component_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
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
        "1732 does not solve local GR, but it improves the map. The old loophole was: if the exterior annulus is vacuum, where did the source mass go? The answer must be Hamiltonian/boundary charge. Current MTS has a credible conditional route, but not the parent-signed current owner. Therefore the best next shot is 1733: derive or reject the parent `Theta_total/Q_tau` owner. If that fails, the local branch stays finite-residual/closure-only rather than promoted.",
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
    doc_path = ROOT / "1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1732_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1732 validation FAIL")
    print("1732 validation PASS")


if __name__ == "__main__":
    main()
