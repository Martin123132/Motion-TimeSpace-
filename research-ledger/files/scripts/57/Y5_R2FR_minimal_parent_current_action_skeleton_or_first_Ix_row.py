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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1799"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1799_0_1798_doc",
        "source_key": "1798_handoff",
        "source_path": ROOT / "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md",
        "needles": ["DEC1798_3_next", "NEXT1798_0_primary"],
        "role": "selects minimal parent-current action skeleton or first I_X row as 1799 target",
    },
    {
        "source_id": "SRC1799_1_1798_validation",
        "source_key": "1798_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1798_VALIDATION.csv",
        "needles": ["VAL1798_OVERALL", "PASS"],
        "role": "confirms 1798 passed before 1799 starts",
    },
    {
        "source_id": "SRC1799_2_1798_component_pack",
        "source_key": "1798_curl_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv",
        "needles": ["DCC1798_1_I_X", "REJECT_CURRENT_DELTAH_CURL_PACK"],
        "role": "defines I_X as first non-EH curl component",
    },
    {
        "source_id": "SRC1799_3_extra_silence_identity",
        "source_key": "extra_silence_identity",
        "source_path": RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
        "needles": ["E506_scalar_positive_operator", "E506_memory_kernel_silence"],
        "role": "conditional extra-sector positive/nohair energy identities",
    },
    {
        "source_id": "SRC1799_4_sector_silence_status",
        "source_key": "sector_silence_status",
        "source_path": RESIDUALS / "P8_MTS_SECTOR_SILENCE_STATUS.csv",
        "needles": ["motion_time_flow_modes", "memory_kernel"],
        "role": "sector silence status keeps motion/time/memory open",
    },
    {
        "source_id": "SRC1799_5_extra_charge_attempt",
        "source_key": "extra_charge_attempt",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_SILENCE_ATTEMPT.csv",
        "needles": ["HEC556_2_positive_operator_route", "HEC556_7_verdict"],
        "role": "Hamiltonian extra-charge silence attempt fails current claim",
    },
    {
        "source_id": "SRC1799_6_extra_charge_map",
        "source_key": "extra_charge_channel_map",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv",
        "needles": ["HECM556_2_bulk_memory_range", "HECM556_7_parent_anomaly_multiplier"],
        "role": "maps bulk/memory/range and anomaly channels into Cextra/I_X risk",
    },
    {
        "source_id": "SRC1799_7_extra_charge_fill",
        "source_key": "extra_charge_fill_row",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv",
        "needles": ["FB556_0_HPiM_Cextra_core_channel_bound", "MISSING_BULK_MEMORY_RANGE_ZERO_OR_YUKAWA_BOUND"],
        "role": "unfilled extra-charge bound row",
    },
    {
        "source_id": "SRC1799_8_bulk_memory_positive",
        "source_key": "bulk_memory_positive_operator",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
        "needles": ["BMR557_1_massive_positive_operator", "BMR557_7_verdict"],
        "role": "bulk/memory/range positive operator attempt",
    },
    {
        "source_id": "SRC1799_9_bulk_memory_force_map",
        "source_key": "bulk_memory_force_map",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
        "needles": ["BMRF557_0_static_bulk_operator", "BMRF557_3_Hamiltonian_projection"],
        "role": "Yukawa/R10 fallback map and Hamiltonian projection gap",
    },
    {
        "source_id": "SRC1799_10_bulk_memory_yukawa",
        "source_key": "bulk_memory_yukawa_row",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
        "needles": ["FB557_0_bulk_memory_range_zero_or_Yukawa_bound", "MISSING_SOURCE_NORMALIZED_ALPHA_LAMBDA_CURVE"],
        "role": "unfilled bulk/memory/range Yukawa row",
    },
    {
        "source_id": "SRC1799_11_thetaX_gate",
        "source_key": "thetaX_owner_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv",
        "needles": ["TOG1041_0_parent_route", "TOG1041_5_verdict"],
        "role": "Theta_X/P_X owner gate fails current claim",
    },
    {
        "source_id": "SRC1799_12_thetaX_contract",
        "source_key": "thetaX_template_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1041_THETAX_PX_TEMPLATE_CONTRACT.csv",
        "needles": ["TPX1041_0_general_variation", "TPX1041_5_verdict"],
        "role": "finite-order X-sector variation template",
    },
    {
        "source_id": "SRC1799_13_thetaX_r10_template",
        "source_key": "thetaX_r10_nonclaim",
        "source_path": RESIDUALS / "R10_alpha_lambda_curve_MTS_1041_THETAX_PX_TEMPLATE_NONCLAIM.csv",
        "needles": ["MTS_1041_POSITIVE_NOHAIR_TEMPLATE", "MISSING_POSITIVE_OPERATOR_SOURCE_FILE"],
        "role": "nonclaim R10/nohair template for X sector",
    },
    {
        "source_id": "SRC1799_14_memory_operator_lemma",
        "source_key": "memory_operator_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict"],
        "role": "relative positive-operator lemma with unsigned parent inputs",
    },
    {
        "source_id": "SRC1799_15_memory_input_audit",
        "source_key": "memory_input_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        "needles": ["MOI968_2_operator_L", "MOI968_8_verdict"],
        "role": "memory operator activation inputs are missing",
    },
    {
        "source_id": "SRC1799_16_memory_owner_hunt",
        "source_key": "memory_owner_hunt",
        "source_path": RESIDUALS / "P8_Y5_R10_969_MEMORY_OPERATOR_OWNER_HUNT.csv",
        "needles": ["MOO969_0_557_positive_bulk_operator", "MOO969_7_verdict"],
        "role": "no parent memory operator owner found in current corpus",
    },
    {
        "source_id": "SRC1799_17_quadratic_memory_action",
        "source_key": "quadratic_memory_action",
        "source_path": RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "needles": ["QMA970_0_action", "QMA970_7_verdict"],
        "role": "relative minimal quadratic X/memory action skeleton",
    },
    {
        "source_id": "SRC1799_18_two_slot_contract",
        "source_key": "two_slot_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_972_TWO_SLOT_ACTION_CONTRACT.csv",
        "needles": ["TSC972_2_active_X_kinetic", "TSC972_7_verdict"],
        "role": "two-slot active X kinetic plus observed coupling contract",
    },
    {
        "source_id": "SRC1799_19_JX_gate",
        "source_key": "JX_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv",
        "needles": ["JXD973_0_kinetic_affine", "JXD973_6_verdict"],
        "role": "J_X decomposition gate keeps source silence unproved",
    },
    {
        "source_id": "SRC1799_20_extra_omega",
        "source_key": "extra_omega_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv",
        "needles": ["ESO912_3_bulk_X_memory", "ESO912_4_source_normalization"],
        "role": "extra-sector omega remains missing for X/memory",
    },
    {
        "source_id": "SRC1799_21_delta_symp_extra",
        "source_key": "delta_symp_extra_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv",
        "needles": ["DSE912_3_bulk_X", "MISSING_X_OMEGA_OR_FORCE_LAW"],
        "role": "Delta_symp_X row is unfilled",
    },
    {
        "source_id": "SRC1799_22_normal_form",
        "source_key": "normal_form_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_0_parent_action_partition", "ANF1768_6_current_verdict"],
        "role": "parent action normal-form signature remains unsigned",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_SOURCE_REGISTER.csv",
    "minimal_x_action_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_MINIMAL_X_ACTION_ATTEMPT.csv",
    "ix_source_bound_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_FIRST_IX_SOURCE_BOUND_ROW.csv",
    "activation_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_ACTIVATION_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1799_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1799_VALIDATION.csv",
}

DOC_PATH = ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md"


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


def minimal_x_action_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_0_parent_route",
            "object": "selected parent X route",
            "mathematical_form": "choose absent/gauge, first-class vertical constraint, positive source-free field, or sourced residual before scoring I_X",
            "current_status": "ROUTE_NOT_PARENT_SELECTED",
            "relative_result": "routes exist as contracts, not as a signed parent branch",
            "blocking_gap": "MISSING_PARENT_ROUTE_SELECTION",
            "source_paths": src("thetaX_owner_gate", "memory_owner_hunt", "normal_form_signature"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_1_minimal_action_skeleton",
            "object": "minimal active X action",
            "mathematical_form": "S_X = 1/2 int_D sqrt(gamma)[A^ij nabla_i X nabla_j X + m_X^2 X^2 - 2 J_X X] + S_boundary[X]",
            "current_status": "FORMAL_SKELETON_WRITTEN_NOT_PARENT_SIGNED",
            "relative_result": "gives a lawful target for L_X, Theta_X, omega_X and no-hair tests",
            "blocking_gap": "MISSING_PARENT_X_FIELD;MISSING_AIJ_OWNER;MISSING_MX2_OWNER;MISSING_JX_SOURCE_MAP;MISSING_BOUNDARY_CLASS",
            "source_paths": src("quadratic_memory_action", "two_slot_contract", "thetaX_template_contract"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_2_variation",
            "object": "Euler variation and Theta_X",
            "mathematical_form": "delta S_X = int_D sqrt(gamma)(L_X X - J_X)delta X + int_partialD Pi_X delta X; Theta_X^i = Pi_X^i delta X",
            "current_status": "RELATIVE_VARIATION_OK_INPUTS_UNSIGNED",
            "relative_result": "if accepted, supplies the missing Theta_X/omega_X form for I_X",
            "blocking_gap": "MISSING_PARENT_DOMAIN;MISSING_BOUNDARY_CONDITION;MISSING_THETAX_NORMALIZATION",
            "source_paths": src("quadratic_memory_action", "thetaX_template_contract"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_3_symplectic_current",
            "object": "omega_X and I_X",
            "mathematical_form": "omega_X(delta1,delta2)=delta1 Pi_X^i delta2 X - delta2 Pi_X^i delta1 X; I_X = |int_S i_tau omega_X|/M_H_ref plus constraint/boundary terms",
            "current_status": "FORMULA_READY_COMPONENTS_MISSING",
            "relative_result": "identifies the exact symplectic object to zero or bound",
            "blocking_gap": "MISSING_OMEGA_X_SOURCE;MISSING_BOUNDARY_PULLBACK;MISSING_M_H_REF",
            "source_paths": src("extra_omega_ledger", "delta_symp_extra_rows", "thetaX_template_contract"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_4_positive_nohair_activation",
            "object": "X=0 local nohair theorem",
            "mathematical_form": "0=int_D X(L_X X-J_X)=int_D(A^ij nabla_iX nabla_jX + m_X^2 X^2) + boundary - int_D XJ_X",
            "current_status": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "relative_result": "would force X=0 only if A>=0, m_X^2>=0/zero-mode removed, J_X=0 and boundary flux=0",
            "blocking_gap": "MISSING_SIGN_CERTIFICATE;MISSING_ZERO_SOURCE_THEOREM;MISSING_BOUNDARY_DATA;MISSING_DOMAIN_SELECTOR",
            "source_paths": src("extra_silence_identity", "memory_operator_lemma", "memory_input_audit"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_5_source_boundary_projection",
            "object": "J_X, boundary flux and Hamiltonian projection",
            "mathematical_form": "J_X=J_matter+J_chiD_wall+J_boundary+J_readout+J_history; Pi_M^H dJ_X=0 or finite source-normalized Yukawa row",
            "current_status": "SOURCE_BOUNDARY_PROJECTION_NOT_DERIVED",
            "relative_result": "sets the split between zero theorem and empirical fallback",
            "blocking_gap": "MISSING_JX_ZERO;MISSING_BOUNDARY_FLUX_ZERO;MISSING_PIM_H_PROJECTION;MISSING_ALPHA_LAMBDA_CURVE",
            "source_paths": src("JX_gate", "bulk_memory_force_map", "bulk_memory_yukawa_row"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_6_double_zero_tension",
            "object": "double-zero gated memory branch",
            "mathematical_form": "S_mem = int sqrt(-g) f(chi_D)L_X[X] with f(0)=f'(0)=0",
            "current_status": "BRANCH_TENSION_RETAINED",
            "relative_result": "double-zero can silence local stress/exchange, but if it gates the kinetic operator it can also remove the operator needed to prove X=0",
            "blocking_gap": "MISSING_PARENT_ORIGIN_FOR_F;MISSING_ACTIVE_OPERATOR_BRANCH_SELECTION",
            "source_paths": src("quadratic_memory_action", "two_slot_contract", "JX_gate"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MXA1799_7_verdict",
            "object": "minimal parent current action skeleton for I_X",
            "mathematical_form": "MXA1799_0 through MXA1799_6 pass in one parent branch",
            "current_status": "RELATIVE_SKELETON_READY_PARENT_UNSIGNED",
            "relative_result": "skeleton is mathematically useful but not a local-GR proof",
            "blocking_gap": "MISSING_PARENT_SIGNED_X_ACTION_AND_ACTIVATION_INPUTS",
            "source_paths": src("quadratic_memory_action", "thetaX_owner_gate", "bulk_memory_positive_operator"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def ix_source_bound_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_0_identity",
            "component": "I_X_over_MH",
            "definition": "first non-EH curl component: extra motion/time/memory/range sector contribution to d_field alpha_tau",
            "formula": "|int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref",
            "required_input": "L_X;Theta_X;omega_X;C_tau_X;J_X;boundary_X;Pi_M^H projection;M_H_ref;source_path",
            "current_value": "MISSING_I_X_NUMERIC_OR_THEOREM_ZERO",
            "status": "STAGED_NONCLAIM_SCHEMA",
            "source_paths": src("1798_curl_pack", "thetaX_template_contract", "extra_charge_fill_row"),
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_1_operator_sign",
            "component": "operator_positive_or_absent",
            "definition": "parent X operator is absent/gauge/topological or positive with controlled kernel",
            "formula": "A^ij >= 0 and m_X^2 >= 0, with zero-mode removed or universal constant class",
            "required_input": "Z_X/A^ij;M_X^2;operator source;field normalization;domain D",
            "current_value": "MISSING_OPERATOR_SIGN_AND_GAP_CERTIFICATE",
            "status": "MISSING_PARENT_OPERATOR_INPUT",
            "source_paths": src("memory_operator_lemma", "memory_input_audit", "thetaX_owner_gate"),
            "units": "operator_certificate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_2_source_zero",
            "component": "J_X_source_silence",
            "definition": "ordinary matter/domain/readout/history do not source X in the local exterior",
            "formula": "J_X=J_matter+J_chiD_wall+J_boundary+J_readout+J_history=0",
            "required_input": "matter blindness;chi_D wall silence;boundary exchange silence;readout-after-variation;history kernel locality",
            "current_value": "MISSING_JX_ZERO_THEOREM_OR_COMPONENT_BOUNDS",
            "status": "MISSING_SOURCE_SILENCE_INPUT",
            "source_paths": src("JX_gate", "bulk_memory_positive_operator", "bulk_memory_force_map"),
            "units": "source_current_certificate_or_bound",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_3_boundary_zero",
            "component": "boundary_X_flux",
            "definition": "X boundary term has zero local flux or finite source-backed profile",
            "formula": "Pi_X delta X|partialD=0 or |boundary_X|/M_H_ref finite",
            "required_input": "boundary class;Dirichlet/Neumann/zero-mean rule;relative nohair;boundary coefficient source",
            "current_value": "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "status": "MISSING_BOUNDARY_INPUT",
            "source_paths": src("memory_operator_lemma", "two_slot_contract", "bulk_memory_yukawa_row"),
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_4_symplectic_flux",
            "component": "Delta_symp_X",
            "definition": "X-sector symplectic obstruction contribution",
            "formula": "|int_S i_tau omega_X|/M_H_ref",
            "required_input": "omega_X;boundary pullback;tau;surface;M_H_ref;source_path",
            "current_value": "MISSING_X_OMEGA_OR_FORCE_LAW",
            "status": "MISSING_SYMPLECTIC_INPUT",
            "source_paths": src("extra_omega_ledger", "delta_symp_extra_rows"),
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_5_yukawa_fallback",
            "component": "alpha_X_lambda_fallback",
            "definition": "if X survives, represent it as source-normalized fifth-force/range profile",
            "formula": "a_X/a_GR = alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X)",
            "required_input": "m_X;lambda_X;source/test charges;Pi_M^H projection;alpha_X(lambda);bound curve;normalization",
            "current_value": "MISSING_SOURCE_NORMALIZED_ALPHA_LAMBDA_CURVE",
            "status": "MISSING_R10_FALLBACK_INPUT",
            "source_paths": src("bulk_memory_force_map", "bulk_memory_yukawa_row", "thetaX_r10_nonclaim"),
            "units": "alpha_lambda_curve",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_6_Hamiltonian_projection",
            "component": "PiM_H_projection_of_X_charge",
            "definition": "surviving X charge projection into Hamiltonian mass current",
            "formula": "M_H_ref^-1 int_A Pi_M^H dJ_X or theorem-zero projection",
            "required_input": "Pi_M^H definition;J_X;chain map;projection coefficient;source_path",
            "current_value": "MISSING_HAMILTONIAN_PROJECTION_ZERO_OR_COEFFICIENT",
            "status": "MISSING_PIM_PROJECTION_INPUT",
            "source_paths": src("bulk_memory_force_map", "extra_charge_channel_map", "extra_charge_fill_row"),
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IXR1799_7_acceptance",
            "component": "I_X_row_acceptance",
            "definition": "acceptance gate for first I_X row",
            "formula": "IXR1799_1 through IXR1799_6 theorem-zero or source-backed finite rows with no MISSING markers",
            "required_input": "complete source-backed or theorem-zero I_X component pack",
            "current_value": "NOT_ACCEPTED",
            "status": "REJECT_CURRENT_IX_ROW",
            "source_paths": src("extra_charge_attempt", "bulk_memory_positive_operator", "thetaX_owner_gate"),
            "units": "gate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def activation_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACT1799_0_relative_skeleton",
            "gate": "minimal X action skeleton is mathematically lawful",
            "current_status": "PASS_RELATIVE_SKELETON_ONLY",
            "reason": "variation and positive-operator identity are available as conditional mathematics",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACT1799_1_parent_selection",
            "gate": "parent branch selects this X action before readout",
            "current_status": "FAIL_PARENT_UNSIGNED",
            "reason": "X field, operator and route are not parent selected",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACT1799_2_positive_nohair_inputs",
            "gate": "operator sign, source zero and boundary zero activate X=0",
            "current_status": "FAIL_INPUTS_MISSING",
            "reason": "sign/gap, J_X, boundary and domain inputs are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACT1799_3_fallback_curve",
            "gate": "surviving X has executable alpha(lambda) fallback",
            "current_status": "FAIL_R10_FALLBACK_MISSING",
            "reason": "alpha_X(lambda), lambda_X and Hamiltonian projection are not sourced",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACT1799_4_verdict",
            "gate": "I_X claim readiness",
            "current_status": "IX_ROW_NOT_READY",
            "reason": "skeleton helps, but no theorem-zero or finite row is accepted",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1799_0_source_driven_X",
            "countermodel": "ordinary matter, domain wall, boundary exchange, readout, or history tail sources X in the local exterior",
            "survives_current_constraints": True,
            "why_survives": "J_X decomposition is not zero-proved",
            "what_kills_it": "J_X=0 theorem or finite component source bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1799_1_boundary_hair_X",
            "countermodel": "X has finite boundary/zero-mode hair even when bulk source vanishes",
            "survives_current_constraints": True,
            "why_survives": "boundary class, zero-flux and zero-mode removal are not parent-derived",
            "what_kills_it": "boundary/nohair theorem or finite boundary flux row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1799_2_sign_indefinite_X",
            "countermodel": "X operator has wrong sign, zero mode, nonlocal memory tail, or no mass gap",
            "survives_current_constraints": True,
            "why_survives": "A^ij, Z_X, M_X^2 and locality are not sourced",
            "what_kills_it": "operator sign/gap/locality certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1799_3_fifth_force_X",
            "countermodel": "surviving X gives a finite-range fifth force rather than local silence",
            "survives_current_constraints": True,
            "why_survives": "alpha_X(lambda), q_source, q_test and Pi_M projection are missing",
            "what_kills_it": "R10 alpha(lambda) pass or source/test charge zero theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1799_4_degenerate_double_zero",
            "countermodel": "double-zero gate removes the X kinetic operator at the local branch, so it silences stress without proving X=0",
            "survives_current_constraints": True,
            "why_survives": "active operator branch and double-zero coupling branch are not parent-separated",
            "what_kills_it": "two-slot parent action with active X kinetic and double-zero observed coupling only",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1799_0_X_parent_action",
            "claim": "minimal X action is parent-selected",
            "status": "BLOCKED",
            "reason": "MXA1799_7 is relative skeleton ready but parent unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1799_1_I_X_zero",
            "claim": "I_X=0",
            "status": "BLOCKED",
            "reason": "operator sign, J_X zero, boundary zero and Pi_M projection are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1799_2_I_X_finite_score",
            "claim": "I_X finite source-backed row can be scored",
            "status": "BLOCKED",
            "reason": "IXR1799_7 rejects the current row due MISSING_* payloads",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1799_3_deltaH_integrability",
            "claim": "delta_H_tau_nonintegrable row is closed",
            "status": "BLOCKED",
            "reason": "first non-EH component I_X is not zero or bounded",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1799_4_local_GR_Newton",
            "claim": "local GR/Newton source-normalized reduction is derived",
            "status": "BLOCKED",
            "reason": "Hamiltonian integrability and extra-sector silence remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1799_0_skeleton",
            "decision": "MINIMAL_X_ACTION_SKELETON_WRITTEN_RELATIVE_ONLY",
            "reason": "the quadratic action/variation/omega route is mathematically valid but not parent selected",
            "next_action": "do not promote it as MTS action until activation inputs are real",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1799_1_ix_row",
            "decision": "FIRST_IX_ROW_EMITTED_NONCLAIM",
            "reason": "I_X now has explicit operator, source, boundary, symplectic, R10 and PiM projection slots",
            "next_action": "fill or derive those slots one by one",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1799_2_nohair_policy",
            "decision": "POSITIVE_OPERATOR_NOT_ENOUGH_WITHOUT_SOURCE_AND_BOUNDARY",
            "reason": "mass gap alone controls range but not coupling, source charge, boundary hair or Hamiltonian projection",
            "next_action": "require J_X=0, boundary zero, and PiM projection before theorem-zero",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1799_3_next",
            "decision": "X_POSITIVE_OPERATOR_ACTIVATION_OR_YUKAWA_FALLBACK_NEXT",
            "reason": "the next live fork is exact: activate nohair via operator/source/boundary/projection, or build source-normalized alpha(lambda) fallback",
            "next_action": "build 1800 to try the activation theorem; if it fails, emit alpha_X(lambda) fallback contract",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1799_0_primary",
            "next_target": "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
            "script": "scripts/Y5_R2FR_X_positive_operator_activation_or_Yukawa_fallback_row.py",
            "objective": "try to activate the X nohair theorem with operator sign, J_X=0, boundary zero and PiM projection; otherwise emit source-normalized alpha_X(lambda) fallback row",
            "selection_status": "selected",
            "success_condition": "I_X theorem-zero or executable finite-range fallback with lambda, alpha, source/test charges, PiM projection and bound source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1799_1_parallel_source",
            "next_target": "1800b-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
            "script": "scripts/Y5_R2FR_JX_source_zero_or_component_bound_pack.py",
            "objective": "prove J_X source silence or emit J_matter/J_chiD/J_boundary/J_readout/J_history component bounds",
            "selection_status": "held_parallel",
            "success_condition": "J_X=0 theorem or finite source component envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1799_2_parallel_boundary",
            "next_target": "1800c-Y5-R2FR-X-boundary-zero-mode-nohair-or-boundary-flux-row.md",
            "script": "scripts/Y5_R2FR_X_boundary_zero_mode_nohair_or_boundary_flux_row.py",
            "objective": "prove X boundary/zero-mode nohair or emit finite boundary flux profile",
            "selection_status": "held_parallel",
            "success_condition": "boundary_X theorem-zero or finite source-backed boundary row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "minimal_x_action_attempt": minimal_x_action_attempt_rows(),
        "ix_source_bound_row": ix_source_bound_row_rows(),
        "activation_gate": activation_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
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
        shutil.copy2(path, RAB_QUEUE / f"JR1799_{key.upper()}.csv")


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
        "score_ready",
        "score_emitted",
        "accepted_for_scoring",
        "parent_signed",
        "valid_prediction_row",
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
        "score_ready",
        "score_emitted",
        "accepted_for_scoring",
        "parent_signed",
        "valid_prediction_row",
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
        if not (RAB_QUEUE / f"JR1799_{key.upper()}.csv").exists():
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
        ("VAL1799_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1799_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1799_2_skeleton_relative_only",
            any(
                row["attempt_id"] == "MXA1799_7_verdict"
                and row["current_status"] == "RELATIVE_SKELETON_READY_PARENT_UNSIGNED"
                for row in rows_map["minimal_x_action_attempt"]
            )
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["minimal_x_action_attempt"]),
            "minimal X action skeleton is relative only",
        ),
        (
            "VAL1799_3_ix_row_rejected",
            any(
                row["row_id"] == "IXR1799_7_acceptance"
                and row["status"] == "REJECT_CURRENT_IX_ROW"
                for row in rows_map["ix_source_bound_row"]
            )
            and all(
                not boolish(row["accepted_for_scoring"])
                and not boolish(row["valid_prediction_row"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["ix_source_bound_row"]
            ),
            "first I_X row is rejected and non-scoreable",
        ),
        (
            "VAL1799_4_activation_gate_blocks",
            any(
                row["gate_id"] == "ACT1799_4_verdict"
                and row["current_status"] == "IX_ROW_NOT_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["activation_gate"]
            ),
            "activation gate blocks scoring",
        ),
        (
            "VAL1799_5_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1799_6_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1799_7_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1799_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1799_9_decision_next",
            any(
                row["decision_id"] == "DEC1799_3_next"
                and row["decision"] == "X_POSITIVE_OPERATOR_ACTIVATION_OR_YUKAWA_FALLBACK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects X activation or Yukawa fallback next",
        ),
        (
            "VAL1799_10_next_selected",
            any(row["route_id"] == "NEXT1799_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1799_11_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1799 CSVs parse"),
        ("VAL1799_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1799_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1799_14_formalization_untouched", formalization_untouched(), "no 1799 outputs found under formalization-workbench"),
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
            "check_id": "VAL1799_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1799 minimal parent current action skeleton or first I_X row checkpoint",
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
            "# 1799 - Y5/R2FR Minimal Parent Current Action Skeleton or First Ix Row",
            "",
            "## Verdict",
            "",
            "1799 writes the cleanest possible `X`-sector skeleton for the first non-EH curl obstruction. The skeleton is mathematically useful: it gives an action, variation, `Theta_X`, `omega_X`, and a positive-operator/nohair activation route.",
            "",
            "But it is not yet a parent-signed MTS action. The missing pieces are exactly the ones that matter: parent route selection, operator signs, `J_X=0`, boundary/zero-mode data, Hamiltonian projection, and a fallback source-normalized `alpha_X(lambda)` curve if the sector survives.",
            "",
            "The staged nonclaim row is:",
            "",
            "`I_X/M_H_ref = |int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref`.",
            "",
            "**Claim ceiling:** no parent-selected `X` action, no `I_X=0`, no finite `I_X` score, no `delta_H_tau` closure, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1799.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Minimal X Action Attempt",
            markdown_table(rows_map["minimal_x_action_attempt"], ["attempt_id", "object", "mathematical_form", "current_status", "blocking_gap", "parent_signed", "valid_for_claim"]),
            "",
            "## First Ix Source Bound Row",
            markdown_table(rows_map["ix_source_bound_row"], ["row_id", "component", "formula", "current_value", "status", "units", "accepted_for_scoring", "valid_for_claim"]),
            "",
            "## Activation Gate",
            markdown_table(rows_map["activation_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This is a useful tightening. We now know what would make the extra sector vanish without a plateau axiom: a parent-selected positive operator with no source, no boundary hair, and no Hamiltonian projection. If any of those fail, `X` becomes an empirical finite-range/source-normalization row instead of a GR-limit theorem.",
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
    print(f"1799 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
