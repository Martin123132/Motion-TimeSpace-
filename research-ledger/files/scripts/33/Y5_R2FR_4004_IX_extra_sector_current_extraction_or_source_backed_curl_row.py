from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4004"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4004-Y5-R2FR-IX-extra-sector-current-extraction-or-source-backed-curl-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4004_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4004_IX_AUXILIARY_KINETIC_FORK_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4004_IX_EXTRACTION_AUDIT.csv",
    "component_law": SRC / "P8_Y5_R2FR_4004_IX_COMPONENT_LAW.csv",
    "source_rows": SRC / "P8_Y5_R2FR_4004_IX_SOURCE_ROW_TEMPLATE.csv",
    "cases": SRC / "P8_Y5_R2FR_4004_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4004_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4004_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4004_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4004_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4004_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4004_VALIDATION.csv",
}

NEXT_DOC = "4005-Y5-R2FR-auxiliary-necessity-or-first-real-IX-source-coefficient.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4005_auxiliary_necessity_or_first_real_IX_source_coefficient.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4004_00_handoff", SRC / "P8_Y5_R2FR_4003_NEXT_TARGET.csv", "NEXT4003_0", "4003 I_X handoff"),
        ("SRC4004_01_ix_bound", SRC / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv", "PCB4003_2_I_X", "I_X component bound"),
        ("SRC4004_02_theta_qtau_x", SRC / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv", "TQC1733_1_X_extra", "Theta_X/Qtau_X missing row"),
        ("SRC4004_03_deltaH_ix", SRC / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv", "DCC1798_1_I_X", "deltaH curl I_X component"),
        ("SRC4004_04_aux_theta", SRC / "P8_Y5_R10_1264_THETA_OMEGA_VR_FILL_AUDIT.csv", "TVR1264_0_theta_candidate", "auxiliary theta zero candidate"),
        ("SRC4004_05_aux_on_shell", SRC / "P8_Y5_R10_1264_THETA_OMEGA_VR_FILL_AUDIT.csv", "TVR1264_3_on_shell_nullness", "auxiliary on-shell nullness guard"),
        ("SRC4004_06_aux_action", SRC / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv", "CAC1268_1_constraint_action", "second-class auxiliary action"),
        ("SRC4004_07_no_derivative", SRC / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv", "CAC1268_2_no_derivative_grammar", "no-derivative grammar"),
        ("SRC4004_08_aux_theorem", SRC / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv", "CAC1268_5_conditional_theorem", "auxiliary elimination theorem"),
        ("SRC4004_09_kinetic_variation", SRC / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv", "KIN2237_0_variation", "kinetic variation countermodel"),
        ("SRC4004_10_kinetic_contradiction", SRC / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv", "KIN2237_1_null_contradiction", "kinetic/null contradiction"),
        ("SRC4004_11_theta_fill", SRC / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv", "TO2238_0_theta_R", "theta/Omega fill"),
        ("SRC4004_12_operator_contradiction", SRC / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv", "TO2238_3_operator_contradiction", "derivative operator contradiction"),
        ("SRC4004_13_positive_identity", SRC / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv", "E506_vector_tensor_positive_operator", "positive operator silence identity"),
        ("SRC4004_14_lx_theorem", SRC / "P8_Y5_R10_1508_LX_THEOREM_LEDGER.csv", "THM1508_0_field_specific_positive_operator_zero", "field-specific L_X theorem"),
        ("SRC4004_15_template_guard", SRC / "P8_Y5_R10_1508_LX_THEOREM_LEDGER.csv", "THM1508_1_template_operator_no_instantiation", "template substitution guard"),
        ("SRC4004_16_lx_trial", SRC / "P8_Y5_R10_1508_LX_CERTIFICATE_TRIAL.csv", "TRIAL1508_8_acceptance", "L_X certificate acceptance"),
        ("SRC4004_17_lx_audit", SRC / "P8_Y5_R10_1508_FIELD_SPECIFIC_LX_OPERATOR_AUDIT.csv", "LXA1508_8_verdict", "field-specific L_X verdict"),
        ("SRC4004_18_alpha_pack", SRC / "P8_Y5_R10_1508_ALPHA_PRIOR_SOURCE_PACK.csv", "APACK1508_0_scalar_like", "source-backed alpha prior pack"),
        ("SRC4004_19_gk_candidate", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_B_positive_auxiliary_fields", "positive auxiliary stress candidate"),
        ("SRC4004_20_domain_aux", SRC / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv", "C0_parent_domain_sector", "domain auxiliary parent clause"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "IX4004_0_definition",
            "claim_piece": "I_X current obstruction",
            "mathematical_form": "I_X := |d_field alpha_tau^X|/M_H_ref, alpha_tau^X := int_S(delta Q_tau^X - i_tau Theta_X)",
            "derived_result": "The extra sector affects H_tau integrability only through its sector symplectic potential, charge, and retained bulk/source terms.",
            "status": "EXACT_DEFINITION_FROM_4003",
            "source_path": str(SRC / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_1_auxiliary_no_derivative_zero",
            "claim_piece": "auxiliary no-derivative zero route",
            "mathematical_form": "If L_X=L_aux(X,q(Phi),theta) epsilon with no D_mu X, no B_X[X], matter/readout independent of X, and no exterior on-shell source, then Theta_X=0, Q_tau^X=0/proper, and I_X=0.",
            "derived_result": "This is the clean route: an algebraic compatibility variable has no sector symplectic current or boundary momentum. Its remaining risk is bulk stress/constraint leakage, not I_X.",
            "status": "DERIVED_CONDITIONAL_ZERO_THEOREM",
            "source_path": str(SRC / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_2_RAB_auxiliary_candidate",
            "claim_piece": "R_AB second-class auxiliary candidate",
            "mathematical_form": "S_R=int mu_parent Lambda_R [R_AB-C_AB(q(Phi),theta,top)], with no D R_AB, no D Lambda_R, no vertical metric/connection, delta S_matter/delta R_AB=0, and delta B_R/delta R_AB=0.",
            "derived_result": "Under those candidate clauses, theta_R=Omega_R=Pi_R^n=0 and Lambda_R=0 on the protected branch; Z_R, J_R and B_R are zero only conditionally.",
            "status": "EXACT_WITHIN_CANDIDATE_NOT_PARENT_NECESSITY",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_3_kinetic_countermodel",
            "claim_piece": "derivative sector countermodel",
            "mathematical_form": "For L_X superset -1/2 Z_X nabla_mu X nabla^mu X -1/2 Z_X M_X^2 X^2, Theta_X^mu=-Z_X nabla^mu X delta X and Pi_X^n=-Z_X n_mu nabla^mu X.",
            "derived_result": "Any legal derivative term creates a real symplectic current/boundary momentum. It cannot be silently zeroed; it needs a positive-operator no-source theorem or finite coefficient rows.",
            "status": "EXACT_FORMAL_VARIATION_COUNTERMODEL",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_4_positive_operator_zero",
            "claim_piece": "field-specific positive operator zero route",
            "mathematical_form": "int_A <X,L_X X> = ||X||_positive^2 + boundary/history flux + source terms; if L_X is the actual parent Euler operator, positive, source-free, test-charge-free, PiM_H-silent and boundary/history silent, then X=0 and I_X=0.",
            "derived_result": "Positive energy can kill a derivative sector, but only after field identity, operator sign, domain, source/test charges, projection and boundary/history are field-specific.",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_INSTANTIATED",
            "source_path": str(SRC / "P8_Y5_R10_1508_LX_THEOREM_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_5_finite_row_fallback",
            "claim_piece": "source-backed finite I_X row",
            "mathematical_form": "If IX4004_1 or IX4004_4 fails, retain {field_id,Z_X,M_X^2,lambda_X,Q_X_source,q_test_X,PiM_H_projection,boundary_flux,tau_R10,source_path} and keep valid_for_claim=false until numeric/source-backed.",
            "derived_result": "The fallback is not another gap note: it is a schema for turning the extra-sector current into a tested finite-force coefficient.",
            "status": "SOURCE_ROW_TEMPLATE_READY",
            "source_path": str(SRC / "P8_Y5_R10_1508_ALPHA_PRIOR_SOURCE_PACK.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "IX4004_6_current_verdict",
            "claim_piece": "I_X current verdict",
            "mathematical_form": "Current corpus supports IX4004_1 as a promising conditional route and IX4004_3/4/5 as the honest fallback if derivatives or sources survive.",
            "derived_result": "I_X is not proven zero today, but it is now reduced to a sharp fork: prove auxiliary necessity/no-derivative protection, or fill the first real coefficient.",
            "status": "AUXILIARY_ROUTE_SELECTED_NOT_PROMOTED",
            "source_path": str(SRC / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "IXA4004_0_field_sort",
            "clause": "extra-sector field/sort identity",
            "required_signature": "name the parent field/component X and state whether it is algebraic auxiliary, positive operator field, memory kernel, boundary/topological class, or calibration.",
            "current_evidence": "R_AB and chi_D auxiliary candidates exist; generic X remains uninstantiated.",
            "status": "PARTIAL_CANDIDATE_NOT_GLOBAL_X_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_1_no_derivative_grammar",
            "clause": "no D_mu X grammar for auxiliary zero",
            "required_signature": "no D_mu X, no D_mu lambda_X, no vertical metric/connection, no derivative boundary term.",
            "current_evidence": "CAC1268_2 and TO2238_0 support the candidate for R_AB only.",
            "status": "CONDITIONAL_FOR_RAB_NOT_PARENT_NECESSITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_2_matter_source_descent",
            "clause": "ordinary matter/readout independent of auxiliary X",
            "required_signature": "delta S_matter/delta X=0 and no material-marker/source charge couples to X.",
            "current_evidence": "CAC1268_3 marks matter descent required but unsigned; 1508 keeps source/test charges missing.",
            "status": "OPEN_SOURCE_CHARGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_3_boundary_nohair",
            "clause": "no boundary/corner hair",
            "required_signature": "delta B_X/delta X=0 or fixed topological/proper corner term with zero linking-sphere flux.",
            "current_evidence": "CAC1268_4 and TO2238_2 mark boundary protection conditional.",
            "status": "OPEN_BOUNDARY_HAIR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_4_bulk_stress_guard",
            "clause": "Theta_X zero does not automatically remove bulk stress",
            "required_signature": "E_X and stress contribution vanish, become universal calibration, or are retained in C_tau_bulk/sector_gap.",
            "current_evidence": "TVR1264_3 says on-shell nullness needs Lambda_R=0 and no other R_AB source.",
            "status": "OPEN_BULK_STRESS_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_5_kinetic_derivative_escape",
            "clause": "derivative term escape hatch",
            "required_signature": "prove Z_X=0 by parent grammar/nullness, or if Z_X != 0 compute Theta_X, Pi_X^n, alpha_X(lambda).",
            "current_evidence": "KIN2237_0 and TO2238_3 prove a derivative term creates momentum/current.",
            "status": "FINITE_ROW_REQUIRED_IF_DERIVATIVE_TERM_ALLOWED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_6_positive_operator_certificate",
            "clause": "positive-operator nohair route",
            "required_signature": "field-specific L_X, positive sign/domain, zero source/test charges, zero PiM_H projection, zero boundary/history.",
            "current_evidence": "THM1508_0 is exact conditional; TRIAL1508_0..8 remain unaccepted.",
            "status": "OPEN_FIELD_SPECIFIC_CERTIFICATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IXA4004_7_verdict",
            "clause": "I_X theorem-zero verdict",
            "required_signature": "IXA4004_0 through IXA4004_6 pass together for the same X branch.",
            "current_evidence": "Auxiliary route is the best low-scrutiny path, but necessity/protection remains unsigned.",
            "status": "I_X_ZERO_NOT_CLAIMED_SOURCE_ROW_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_law_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "law_id": "IXL4004_0_auxiliary_symplectic_zero",
            "branch": "algebraic_auxiliary",
            "formula": "no D_mu X and no B_X[X] imply Theta_X=0, Pi_X^n=0, Q_tau^X=0/proper, alpha_tau^X=0, I_X=0",
            "required_inputs": "field_sort;no_derivative_grammar;matter_descent;boundary_nohair;bulk_stress_guard;M_H_ref",
            "current_value": "CONDITIONAL_ONLY",
            "status": "PROMISING_LOW_SCRUTINY_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "IXL4004_1_derivative_current",
            "branch": "kinetic_or_elastic_X",
            "formula": "Theta_X^mu=-Z_X nabla^mu X delta X; Pi_X^n=-Z_X n_mu nabla^mu X; alpha_tau^X=int_S(delta Q_tau^X-i_tau Theta_X)",
            "required_inputs": "Z_X;M_X2;field_id;domain;boundary_conditions;tau;Q_tau_X;M_H_ref",
            "current_value": "MISSING_PARENT_COEFFICIENTS",
            "status": "FINITE_CURRENT_IF_DERIVATIVE_TERM_ALLOWED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "IXL4004_2_positive_operator_bound",
            "branch": "source_free_positive_operator",
            "formula": "||X||_positive^2 <= |source_work|+|boundary_flux|+|history_flux|; I_X=0 only when RHS=0 and projection/test charge vanish",
            "required_inputs": "actual_L_X;positive_domain;source_charge;test_charge;PiM_H_projection;boundary_history_flux",
            "current_value": "MISSING_FIELD_SPECIFIC_CERTIFICATE",
            "status": "BOUND_ROUTE_NOT_ZERO_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "IXL4004_3_finite_force_template",
            "branch": "Yukawa_or_range_residual",
            "formula": "lambda_X=1/M_X and alpha_X(lambda) is proportional to Q_X_source*q_test_X/(G_ref M_source m_test Z_X), dressed by PiM_H and finite-source tau_R10 factors",
            "required_inputs": "lambda_X;Z_X;Q_X_source;q_test_X;PiM_H_projection;tau_R10;alpha_bound(lambda);units",
            "current_value": "SCHEMA_ONLY_NONCLAIM",
            "status": "SOURCE_ROW_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "IXL4004_4_no_free_zero_guard",
            "branch": "guardrail",
            "formula": "Theta_X=0 by algebra does not imply local GR unless C_tau_bulk, stress, matter/source, boundary and Dq leaks are also zero/bounded",
            "required_inputs": "C_tau_bulk;sector_gap;I_matter_EM;I_Dq;I_boundary",
            "current_value": "GUARD_ACTIVE",
            "status": "PREVENTS_AUXILIARY_OVERCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_row_template(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "IXSRC4004_0_RAB_auxiliary",
            "field_id": "R_AB_lambda_R_candidate",
            "branch": "second_class_auxiliary",
            "Z_X": "0_IF_NO_DERIVATIVE_GRAMMAR_PARENT_SIGNED_ELSE_MISSING",
            "M_X2": "not_applicable_auxiliary_constraint",
            "lambda_X": "not_applicable_if_auxiliary",
            "Q_X_source": "0_IF_MATTER_DESCENT_AND_Lambda_R_ZERO_ELSE_MISSING",
            "q_test_X": "0_IF_READOUT_DESCENT_ELSE_MISSING",
            "PiM_H_projection": "0_IF_PROJECTOR_DESCENT_ELSE_MISSING",
            "boundary_flux": "0_IF_DELTA_B_R_ZERO_ELSE_MISSING",
            "tau_R10": "not_applicable_if_theorem_zero",
            "alpha_predicted": "0_IF_ALL_AUXILIARY_CLAUSES_PARENT_SIGNED_ELSE_MISSING",
            "status": "CONDITIONAL_AUXILIARY_ZERO_CANDIDATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXSRC4004_1_scalar_positive_operator",
            "field_id": "X_scalar_candidate",
            "branch": "derivative_positive_operator",
            "Z_X": "MISSING_Z_X",
            "M_X2": "MISSING_M_X2",
            "lambda_X": "MISSING_1_over_M_X",
            "Q_X_source": "MISSING_Q_X_source",
            "q_test_X": "MISSING_q_test_X",
            "PiM_H_projection": "MISSING_PiM_H_projection",
            "boundary_flux": "MISSING_boundary_history_flux",
            "tau_R10": "MISSING_tau_R10",
            "alpha_predicted": "MISSING_alpha_from_parent_coefficients",
            "status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXSRC4004_2_vector_projector_positive_operator",
            "field_id": "X_projector_or_flow_candidate",
            "branch": "gauge_fixed_vector_tensor",
            "Z_X": "MISSING_Z_X_OR_PROJECTOR_NORM",
            "M_X2": "MISSING_M_X2_OR_CURVATURE_GAP",
            "lambda_X": "MISSING_effective_range",
            "Q_X_source": "MISSING_source_readout_charge",
            "q_test_X": "MISSING_test_readout_charge",
            "PiM_H_projection": "MISSING_PiM_H_projection",
            "boundary_flux": "MISSING_boundary_flux",
            "tau_R10": "MISSING_tau_R10",
            "alpha_predicted": "MISSING_alpha_from_parent_coefficients",
            "status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "IXSRC4004_3_memory_kernel",
            "field_id": "X_memory_candidate",
            "branch": "stable_memory_kernel",
            "Z_X": "MISSING_KERNEL_NORM",
            "M_X2": "MISSING_KERNEL_GAP",
            "lambda_X": "MISSING_effective_range_or_history_scale",
            "Q_X_source": "MISSING_history_source",
            "q_test_X": "MISSING_clock_or_force_readout",
            "PiM_H_projection": "MISSING_PiM_H_projection",
            "boundary_flux": "MISSING_history_boundary_flux",
            "tau_R10": "MISSING_tau_R10",
            "alpha_predicted": "MISSING_alpha_from_parent_coefficients",
            "status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4004_0_auxiliary_all_signed",
            "description": "algebraic auxiliary branch has no derivatives, matter descent, no boundary hair, bulk stress guard and M_H_ref",
            "auxiliary_branch": True,
            "no_derivative_grammar": True,
            "matter_descent": True,
            "boundary_nohair": True,
            "bulk_stress_guard": True,
            "positive_operator_certificate": False,
            "derivative_term_allowed": False,
            "source_row_numeric": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_1_auxiliary_matter_missing",
            "description": "Theta_X zero shape exists, but matter/source or bulk stress protection is missing",
            "auxiliary_branch": True,
            "no_derivative_grammar": True,
            "matter_descent": False,
            "boundary_nohair": True,
            "bulk_stress_guard": False,
            "positive_operator_certificate": False,
            "derivative_term_allowed": False,
            "source_row_numeric": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_2_derivative_term_present",
            "description": "kinetic/elastic term exists for X",
            "auxiliary_branch": False,
            "no_derivative_grammar": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "positive_operator_certificate": False,
            "derivative_term_allowed": True,
            "source_row_numeric": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_3_positive_operator_template_only",
            "description": "positive operator identity exists but field-specific source/test/projection/boundary data are missing",
            "auxiliary_branch": False,
            "no_derivative_grammar": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "positive_operator_certificate": False,
            "derivative_term_allowed": True,
            "source_row_numeric": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_4_positive_operator_all_signed",
            "description": "actual L_X positive operator is field-specific, source-free, test-charge-free, PiM silent and boundary/history silent",
            "auxiliary_branch": False,
            "no_derivative_grammar": False,
            "matter_descent": True,
            "boundary_nohair": True,
            "bulk_stress_guard": True,
            "positive_operator_certificate": True,
            "derivative_term_allowed": True,
            "source_row_numeric": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_5_source_backed_nonclaim_row",
            "description": "derivative branch has numeric/source-backed coefficient row but total local-GR bridge remains open",
            "auxiliary_branch": False,
            "no_derivative_grammar": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "positive_operator_certificate": False,
            "derivative_term_allowed": True,
            "source_row_numeric": True,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4004_6_missing_schema",
            "description": "required source/schema paths absent",
            "auxiliary_branch": False,
            "no_derivative_grammar": False,
            "matter_descent": False,
            "boundary_nohair": False,
            "bulk_stress_guard": False,
            "positive_operator_certificate": False,
            "derivative_term_allowed": False,
            "source_row_numeric": False,
            "schema_complete": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in cases:
        if not bool(case["schema_complete"]):
            status = "BLOCKED_MISSING_SCHEMA"
            ix_value = "MISSING"
            theta_zero = False
            qtau_zero = False
            action = "repair schema/source rows"
        elif bool(case["auxiliary_branch"]) and bool(case["no_derivative_grammar"]) and bool(case["matter_descent"]) and bool(case["boundary_nohair"]) and bool(case["bulk_stress_guard"]):
            status = "CONDITIONAL_AUXILIARY_ZERO"
            ix_value = 0.0
            theta_zero = True
            qtau_zero = True
            action = "promote only after parent necessity and remaining 4003 components close"
        elif bool(case["auxiliary_branch"]) and bool(case["no_derivative_grammar"]):
            status = "THETA_ZERO_BUT_BULK_SOURCE_OPEN"
            ix_value = "I_X_SYMPLECTIC_ZERO_CONDITIONAL_CTAU_OPEN"
            theta_zero = True
            qtau_zero = True
            action = "prove matter descent/bulk stress guard or retain C_tau_bulk/source row"
        elif bool(case["positive_operator_certificate"]):
            status = "CONDITIONAL_POSITIVE_OPERATOR_ZERO"
            ix_value = 0.0
            theta_zero = False
            qtau_zero = False
            action = "requires actual parent L_X certificate before any claim"
        elif bool(case["source_row_numeric"]):
            status = "NONCLAIM_NUMERIC_SOURCE_ROW_ACCEPTED"
            ix_value = "FINITE_ROW_AVAILABLE_TOTAL_CHAIN_OPEN"
            theta_zero = False
            qtau_zero = False
            action = "score as residual only, do not claim local GR"
        elif bool(case["derivative_term_allowed"]):
            status = "DERIVATIVE_CURRENT_REQUIRES_SOURCE_ROW"
            ix_value = "MISSING_Z_X_M_X_Q_SOURCE_Q_TEST_BOUNDARY"
            theta_zero = False
            qtau_zero = False
            action = "fill finite coefficient row or prove positive nohair"
        else:
            status = "IX_OPEN"
            ix_value = "SYMBOLIC_COMPONENT"
            theta_zero = False
            qtau_zero = False
            action = "choose auxiliary or derivative branch"
        results.append(
            {
                "case_id": case["case_id"],
                "input_status": status,
                "Theta_X_zero": theta_zero,
                "Q_tau_X_zero": qtau_zero,
                "I_X_value": ix_value,
                "claim_allowed": False,
                "next_action": action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return results


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DG4004_0_zero_proof",
            "question": "Can I_X be proved zero now?",
            "answer": "False",
            "reason": "The auxiliary/no-derivative theorem is derived but parent necessity, matter descent, boundary nohair and bulk stress guard are not all signed.",
            "action": "do not claim local-GR/Htau closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4004_1_best_route",
            "question": "Which route faces less scrutiny?",
            "answer": "auxiliary necessity/no-derivative protection",
            "reason": "It can make Theta_X and Q_tau_X vanish structurally; a derivative route needs source/test charges and R10/local bounds.",
            "action": "try to derive why the extra branch must be auxiliary rather than kinetic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4004_2_fallback",
            "question": "What if auxiliary necessity fails?",
            "answer": "finite source coefficient row",
            "reason": "A derivative term gives real current, so the honest fallback is Z_X/M_X/Q_source/q_test/PiM/boundary/tau_R10.",
            "action": "fill first real coefficient or keep nonclaim schema",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CG4004_0_I_X_zero", "I_X theorem zero", False, "auxiliary route conditional only"),
        ("CG4004_1_Htau_integrability", "H_tau integrability from extra sector", False, "other current-chain components remain open"),
        ("CG4004_2_local_GR", "local GR/Newton promotion", False, "I_X not enough and not parent-signed"),
        ("CG4004_3_R10_PPN", "R10/PPN/local arena pass", False, "source rows nonclaim and coefficient inputs missing"),
        ("CG4004_4_public_claim", "public claim", False, "private checkpoint only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4004_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove auxiliary necessity/no-derivative protection for the extra sector, or fill the first real I_X source coefficient row",
            "success_condition": "parent principle excludes D_mu X/vertical metric/source/boundary hair, giving I_X=0 conditionally promoted only after guards; otherwise a numeric/source-backed Z_X,M_X2,Q_X_source,q_test_X,PiM_H,boundary,tau_R10 row is created nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "I_X reduced to auxiliary/no-derivative zero theorem versus derivative-current finite source row; auxiliary route is best but not parent-signed",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4004 - I_X Extra-Sector Current Extraction Or Source-Backed Curl Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "`I_X` has been reduced to a clean fork, not a foggy missing variable.",
        "",
        "`I_X := |d_field alpha_tau^X|/M_H_ref`, where",
        "",
        "`alpha_tau^X := int_S(delta Q_tau^X - i_tau Theta_X)`.",
        "",
        "## Fork A: Auxiliary Zero",
        "",
        "If the extra sector is algebraic/auxiliary, with no `D_mu X`, no derivative boundary term, no matter/source/readout coupling to `X`, and no boundary hair, then:",
        "",
        "`Theta_X = 0`, `Q_tau^X = 0/proper`, `alpha_tau^X = 0`, so `I_X = 0`.",
        "",
        "This is the low-scrutiny route because it kills the symplectic current structurally rather than tuning it.",
        "",
        "The R_AB compatibility block is the clearest current candidate: `S_R=int mu_parent Lambda_R [R_AB-C_AB(q(Phi),theta,top)]`. Current evidence supports this as an exact conditional theorem, not yet a parent necessity theorem.",
        "",
        "## Fork B: Derivative Current",
        "",
        "If a kinetic/elastic term is legal, then the current is real:",
        "",
        "`Theta_X^mu = -Z_X nabla^mu X delta X`,",
        "",
        "`Pi_X^n = -Z_X n_mu nabla^mu X`.",
        "",
        "That branch needs either a field-specific positive-operator nohair proof or a finite source row with `Z_X`, `M_X^2`, `Q_X_source`, `q_test_X`, `PiM_H_projection`, `boundary_flux`, and `tau_R10`.",
        "",
        "## Guard",
        "",
        "Even if `Theta_X=0`, local GR is not won unless bulk stress, matter/source descent, boundary/reference, projector, and `Dq` leaks are also zero/bounded. This prevents an auxiliary shortcut from secretly hiding a force in `C_tau_bulk`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: `{row['input_status']}`, Theta_X_zero={row['Theta_X_zero']}, Q_tau_X_zero={row['Q_tau_X_zero']}, I_X=`{row['I_X_value']}`, claim={row['claim_allowed']}, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "Best route: prove auxiliary necessity/no-derivative protection. If that fails, stop trying to make `I_X` disappear and fill the first real coefficient row.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4004 - I_X Auxiliary/Kinetic Fork"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `I_X=|d_field alpha_tau^X|/M_H_ref`, with `alpha_tau^X=int_S(delta Q_tau^X-i_tau Theta_X)`, is now reduced to an auxiliary/no-derivative zero route versus a derivative-current finite-row route.
- Auxiliary route: no `D_mu X`, no `B_X[X]`, matter/readout descent, boundary nohair and bulk stress guard imply `Theta_X=Q_tau^X=I_X=0` conditionally.
- Derivative route: a term like `Z_X |nabla X|^2` gives `Theta_X^mu=-Z_X nabla^mu X delta X` and boundary momentum, so a positive-operator nohair theorem or source-backed coefficient row is required.
- Verdict: auxiliary route is best and least baroque, but not parent-signed; no local-GR/Newton/R10 claim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4004_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4004_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4004_02_definition", any(row["theorem_id"] == "IX4004_0_definition" for row in theorem), "I_X definition present")
    add("VAL4004_03_aux_zero", any(row["theorem_id"] == "IX4004_1_auxiliary_no_derivative_zero" for row in theorem), "auxiliary zero theorem present")
    add("VAL4004_04_rab_candidate", any(row["theorem_id"] == "IX4004_2_RAB_auxiliary_candidate" for row in theorem), "R_AB auxiliary candidate present")
    add("VAL4004_05_kinetic_countermodel", any(row["theorem_id"] == "IX4004_3_kinetic_countermodel" for row in theorem), "kinetic countermodel present")
    add("VAL4004_06_positive_operator", any(row["theorem_id"] == "IX4004_4_positive_operator_zero" for row in theorem), "positive operator theorem present")
    add("VAL4004_07_source_row_fallback", any(row["theorem_id"] == "IX4004_5_finite_row_fallback" for row in theorem), "source row fallback present")
    add("VAL4004_08_verdict", any(row["theorem_id"] == "IX4004_6_current_verdict" for row in theorem), "current verdict present")
    add("VAL4004_09_audit_verdict", any(row["audit_id"] == "IXA4004_7_verdict" for row in audit), "audit verdict present")
    add("VAL4004_10_boundary_guard", any(row["audit_id"] == "IXA4004_3_boundary_nohair" for row in audit), "boundary guard audit present")
    add("VAL4004_11_bulk_guard", any(row["audit_id"] == "IXA4004_4_bulk_stress_guard" for row in audit), "bulk stress guard audit present")
    add("VAL4004_12_aux_law", any(row["law_id"] == "IXL4004_0_auxiliary_symplectic_zero" for row in laws), "auxiliary symplectic zero law present")
    add("VAL4004_13_derivative_law", any(row["law_id"] == "IXL4004_1_derivative_current" for row in laws), "derivative current law present")
    add("VAL4004_14_no_free_zero", any(row["law_id"] == "IXL4004_4_no_free_zero_guard" for row in laws), "no-free-zero guard present")
    add("VAL4004_15_source_templates", len(source_rows) >= 4 and any(row["row_id"] == "IXSRC4004_0_RAB_auxiliary" for row in source_rows), "source row templates present")
    zero = next(row for row in results if row["case_id"] == "CASE4004_0_auxiliary_all_signed")
    missing_matter = next(row for row in results if row["case_id"] == "CASE4004_1_auxiliary_matter_missing")
    derivative = next(row for row in results if row["case_id"] == "CASE4004_2_derivative_term_present")
    positive = next(row for row in results if row["case_id"] == "CASE4004_4_positive_operator_all_signed")
    source = next(row for row in results if row["case_id"] == "CASE4004_5_source_backed_nonclaim_row")
    blocked = next(row for row in results if row["case_id"] == "CASE4004_6_missing_schema")
    add("VAL4004_16_aux_zero_case", float(zero["I_X_value"]) == 0.0 and str(zero["Theta_X_zero"]).lower() == "true", "auxiliary zero case clean")
    add("VAL4004_17_aux_guard_case", missing_matter["input_status"] == "THETA_ZERO_BUT_BULK_SOURCE_OPEN", "auxiliary overclaim guarded")
    add("VAL4004_18_derivative_case", derivative["input_status"] == "DERIVATIVE_CURRENT_REQUIRES_SOURCE_ROW", "derivative term routed to source row")
    add("VAL4004_19_positive_case", float(positive["I_X_value"]) == 0.0 and positive["input_status"] == "CONDITIONAL_POSITIVE_OPERATOR_ZERO", "positive operator zero case clean")
    add("VAL4004_20_source_nonclaim", source["input_status"] == "NONCLAIM_NUMERIC_SOURCE_ROW_ACCEPTED" and str(source["claim_allowed"]).lower() == "false", "source-backed row remains nonclaim")
    add("VAL4004_21_missing_blocks", blocked["I_X_value"] == "MISSING", "missing schema blocks")
    add("VAL4004_22_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4004_23_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4004_24_doc_exists", DOC_PATH.exists() and "Best route" in read_text(DOC_PATH), "document written")
    add("VAL4004_25_spine_updated", SPINE_PATH.exists() and "## 4004 - I_X Auxiliary/Kinetic Fork" in read_text(SPINE_PATH), "spine updated")
    add("VAL4004_26_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4004_27_compile", compile_ok, "script compiles")
    add("VAL4004_28_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4004_29_status_exists", OUTPUTS["status"].exists(), "status file exists")
    output_tables = [sources, theorem, audit, laws, source_rows, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4004_30_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4004_31_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4004_32_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    laws = component_law_rows(timestamp)
    source_rows = source_row_template(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["component_law"], laws)
    write_csv(OUTPUTS["source_rows"], source_rows)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, laws, source_rows, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4004 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
