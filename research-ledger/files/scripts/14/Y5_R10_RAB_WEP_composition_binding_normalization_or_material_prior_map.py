from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1404-Y5-R10-RAB-WEP-composition-binding-normalization-or-material-prior-map.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1404_SOURCE_REGISTER.csv"
NORMALIZATION_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1404_COMPOSITION_BINDING_NORMALIZATION_AUDIT.csv"
MATERIAL_PRIOR_MAP_PATH = SRC_DIR / "P8_Y5_R10_1404_MATERIAL_PRIOR_MAP.csv"
CANCELLATION_GUARD_PATH = SRC_DIR / "P8_Y5_R10_1404_ONE_PAIR_CANCELLATION_GUARD.csv"
VECTOR_PRESSURE_GATE_PATH = SRC_DIR / "P8_Y5_R10_1404_WEP_VECTOR_PRESSURE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1404_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1404_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1404_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1404_VALIDATION.csv"

STATUS = (
    "Y5_R10_1404_WEP_composition_binding_normalization_not_derived_"
    "material_vector_prior_map_written_nonclaim"
)
CLAIM_CEILING = (
    "WEP_material_normalization_or_vector_prior_only_no_WEP_pass_no_clock_transfer_"
    "no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)

ETA_BOUND = "2.800000e-15"
DELTA_Q_ALPHA = "-1.989808886825000e-03"
DELTA_Q_SURFACE = "-3.306456347405000e-03"
ALPHA_TARGET = "4.797780522732e-05"
ROBUST_TARGET = "2.887280314062e-05"
CANCELLATION_RATIO = "-6.017949967452794e-01"


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1404_0_1403_doc",
            "source_path": "1403-Y5-R10-RAB-WEP-source-normalization-owner-or-finite-beta-source-prior.md",
            "anchor": "NEXT1403_0_1404",
            "role": "prior checkpoint selecting composition/binding normalization as next WEP target",
        },
        {
            "source_id": "SRC1404_1_1403_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1403_WEP_SOURCE_OWNER_AUDIT.csv",
            "anchor": "WSO1403_2_composition_charge_normalization",
            "role": "declares common WEP composition convention unsigned",
        },
        {
            "source_id": "SRC1404_2_1403_prior",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1403_BETA_SOURCE_TAU_WEP_PRIOR.csv",
            "anchor": "BWP1403_4_binding_guard",
            "role": "requires robust binding guard if surface/binding channel remains active",
        },
        {
            "source_id": "SRC1404_3_1403_pressure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1403_WEP_PRESSURE_GATE.csv",
            "anchor": "WPG1403_1_robust_surface",
            "role": "imports alpha-only and robust WEP pressure targets",
        },
        {
            "source_id": "SRC1404_4_1053_material_matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
            "anchor": "WCM1053_5",
            "role": "existing Ti/Pt alpha and surface/binding smoke charge rows",
        },
        {
            "source_id": "SRC1404_5_1061_convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "anchor": "MCON1061_1_delta_Q_alpha",
            "role": "records MICROSCOPE Ti/Pt sign and alpha charge convention",
        },
        {
            "source_id": "SRC1404_6_1068_requirements",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv",
            "anchor": "MAT1068_2_full_tensor",
            "role": "states full material response tensor is missing",
        },
        {
            "source_id": "SRC1404_7_1079_tensor_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv",
            "anchor": "MTC1079_0_basis",
            "role": "contract for a common response basis",
        },
        {
            "source_id": "SRC1404_8_1080_candidates",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "anchor": "MAT1080_3_delta_surface_smoke",
            "role": "candidate Ti/Pt material composition and surface smoke rows",
        },
        {
            "source_id": "SRC1404_9_1081_parent_basis",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv",
            "anchor": "PB1081_4_verdict",
            "role": "prior failed parent WEP basis derivation attempt",
        },
        {
            "source_id": "SRC1404_10_1086_obstruction",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv",
            "anchor": "CDO1086_2_cancellation_line",
            "role": "one-pair cancellation line obstruction",
        },
        {
            "source_id": "SRC1404_11_1087_no_cancel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
            "anchor": "AMC1087_0_pair_line_forbidden",
            "role": "forbids using one Ti/Pt cancellation as theory result",
        },
        {
            "source_id": "SRC1404_12_1394_composition_map",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv",
            "anchor": "MCM1394_6_composition_verdict",
            "role": "recent bulk material composition map with sector fractions and beta_i",
        },
        {
            "source_id": "SRC1404_13_1395_sector_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "anchor": "SBP1395_5_pack_verdict",
            "role": "binding sector beta source pack remains unfilled",
        },
        {
            "source_id": "SRC1404_14_this_script",
            "source_path": "scripts/Y5_R10_RAB_WEP_composition_binding_normalization_or_material_prior_map.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def normalization_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CBN1404_0_common_basis",
            "required_clause": "one common material response basis for alpha/Coulomb, surface/binding, electronic, nuclear, EM, and other sectors",
            "current_evidence": "1079 states the basis contract; 1081 did not derive the MTS parent basis",
            "missing_or_failure": "MISSING_PARENT_WEP_BASIS",
            "status": "UNSIGNED",
            "consequence": "alpha-only and surface/binding rows are comparable only as smoke/proxy rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_1_pair_charge_convention",
            "required_clause": "TA6V-minus-PtRh10 sign and charge convention is explicit",
            "current_evidence": "1053/1061/1086 provide DeltaQ_alpha and DeltaQ_surface for the same Ti/Pt pair",
            "missing_or_failure": "PAIR_ONLY_NOT_PARENT_COMPLETE",
            "status": "SMOKE_PAIR_CONVENTION_AVAILABLE_NONCLAIM",
            "consequence": "can write a finite material prior map but cannot prove universal WEP normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_2_parent_coefficients",
            "required_clause": "MTS vertical/current coefficients project into each material response component",
            "current_evidence": "1394/1395 name beta_e, beta_nuc, beta_EM, beta_other but do not value-fill or theorem-zero them",
            "missing_or_failure": "MISSING_P_I_PARENT_COEFFICIENT_VECTOR",
            "status": "UNSIGNED",
            "consequence": "eta_AB = DeltaQ^I P_I cannot be scored as a prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_3_source_tau_kernel",
            "required_clause": "same tau_WEP/source kernel multiplies the material vector in a parent-derived way",
            "current_evidence": "1403 retains B_WEP := beta_source_alpha*tau_WEP as finite prior",
            "missing_or_failure": "MISSING_TAU_WEP_AND_SOURCE_KERNEL_OWNER",
            "status": "UNSIGNED",
            "consequence": "no clock/R10/PPN transfer and no WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_4_binding_inheritance",
            "required_clause": "surface/binding response is theorem-zero, inherited from common owner, or source-backed",
            "current_evidence": "1394 binding inheritance attempt leaves binding rows open; 1395 sector beta pack is unfilled",
            "missing_or_failure": "MISSING_BINDING_SECTOR_ZERO_OR_SOURCE_VALUES",
            "status": "UNSIGNED",
            "consequence": "robust surface/binding pressure target remains the conservative lane",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_5_no_one_pair_cancellation",
            "required_clause": "do not tune c_surface/c_alpha to cancel only TA6V-PtRh10",
            "current_evidence": "1086 exposes the cancellation line; 1087 forbids treating it as theory",
            "missing_or_failure": "ONE_PAIR_CANCELLATION_FORBIDDEN",
            "status": "DISCIPLINE_SIGNED",
            "consequence": "small WEP score must come from parent theorem or all-material fit, not pair-line tuning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_6_conditional_normalization_theorem",
            "required_clause": "if CBN1404_0..4 close, DeltaQ^I and P_I form a parent-normalized WEP vector",
            "current_evidence": "clauses are named but parent coefficients and source kernel are missing",
            "missing_or_failure": "EXACT_CONDITIONAL_ONLY",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "consequence": "future WEP prediction can be upgraded without changing the pressure ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CBN1404_7_current_verdict",
            "required_clause": "current composition/binding normalization status",
            "current_evidence": "pair smoke convention exists; parent material vector and source kernel do not",
            "missing_or_failure": "NORMALIZATION_NOT_DERIVED_MATERIAL_PRIOR_REQUIRED",
            "status": "NORMALIZATION_NOT_DERIVED_MATERIAL_PRIOR_REQUIRED",
            "consequence": "write vector prior rows and keep WEP/local claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def material_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "prior_id": "MPM1404_0_vector_definition",
            "object": "P_WEP^I := tau_WEP * beta_source^I * b_I",
            "formula_or_value": "eta_AB = sum_I DeltaQ_AB^I P_WEP^I",
            "basis_status": "MISSING_PARENT_COMPLETE_BASIS",
            "source": "1403 plus 1079/1081/1394/1395",
            "status": "VECTOR_PRIOR_DEFINITION_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_1_pair",
            "object": "MICROSCOPE-like smoke pair",
            "formula_or_value": "TA6V_minus_PtRh10",
            "basis_status": "PAIR_CONVENTION_AVAILABLE",
            "source": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv::MCON1061_0_test_pair",
            "status": "PAIR_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_2_delta_alpha",
            "object": "DeltaQ_alpha_Coulomb",
            "formula_or_value": DELTA_Q_ALPHA,
            "basis_status": "SMOKE_COMPONENT",
            "source": "P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv::CDO1086_0_alpha_delta",
            "status": "NUMERIC_PROXY_NOT_PARENT_BASIS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_3_delta_surface",
            "object": "DeltaQ_surface_binding",
            "formula_or_value": DELTA_Q_SURFACE,
            "basis_status": "SMOKE_COMPONENT",
            "source": "P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv::CDO1086_1_surface_delta",
            "status": "NUMERIC_PROXY_NOT_PARENT_BASIS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_4_alpha_only_pressure",
            "object": "|P_alpha| max if only alpha/Coulomb channel is active",
            "formula_or_value": ALPHA_TARGET,
            "basis_status": "ONE_COMPONENT_PROJECTION_ONLY",
            "source": "P8_Y5_R10_1403_WEP_PRESSURE_GATE.csv::WPG1403_0_alpha_only",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_5_surface_pressure",
            "object": "|P_surface| max if surface/binding channel is retained as unit stress",
            "formula_or_value": ROBUST_TARGET,
            "basis_status": "ONE_COMPONENT_SURFACE_PROJECTION_ONLY",
            "source": "P8_Y5_R10_1403_WEP_PRESSURE_GATE.csv::WPG1403_1_robust_surface",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_6_full_material_tensor",
            "object": "DeltaQ_AB^I for all relevant ordinary-matter sectors",
            "formula_or_value": "MISSING_FULL_MATERIAL_TENSOR",
            "basis_status": "MISSING",
            "source": "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv::MAT1068_2_full_tensor",
            "status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_7_parent_coefficient_vector",
            "object": "P_WEP^I parent coefficient vector",
            "formula_or_value": "MISSING_P_alpha;MISSING_P_surface;MISSING_P_e;MISSING_P_nuc;MISSING_P_EM;MISSING_P_other",
            "basis_status": "MISSING",
            "source": "P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv::SBP1395_5_pack_verdict",
            "status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_8_vector_bound_inequality",
            "object": "finite material prior pressure inequality",
            "formula_or_value": f"|({DELTA_Q_ALPHA})P_alpha + ({DELTA_Q_SURFACE})P_surface + ...| <= {ETA_BOUND}",
            "basis_status": "INEQUALITY_ONLY",
            "source": "1404 checkpoint",
            "status": "MATERIAL_PRIOR_MAP_WRITTEN_NO_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "MPM1404_9_verdict",
            "object": "composition/binding normalization status",
            "formula_or_value": "material vector prior exists; parent normalization does not",
            "basis_status": "NONCLAIM_PRIOR_MAP",
            "source": "1404 checkpoint",
            "status": "READY_AS_MATERIAL_PRIOR_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cancellation_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "OCG1404_0_pair_line",
            "object": "TA6V_minus_PtRh10 alpha/surface cancellation line",
            "value_or_formula": f"c_surface/c_alpha = {CANCELLATION_RATIO}",
            "why_not_allowed": "one-pair cancellation is not invariant under changing material pair",
            "source": "P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv::CDO1086_2_cancellation_line",
            "status": "FORBIDDEN_AS_THEORY_RESULT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "OCG1404_1_two_component_incomplete_basis",
            "object": "alpha/surface-only material plane",
            "value_or_formula": "span{Q_alpha,Q_surface}",
            "why_not_allowed": "DD alpha/surface rows are useful pressure channels but not proven parent-complete basis",
            "source": "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv::AMC1087_1_basis_completeness",
            "status": "INCOMPLETE_BASIS_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "OCG1404_2_branch_mixing",
            "object": "mix coefficient from one branch with range/readout from another",
            "value_or_formula": "FORBIDDEN",
            "why_not_allowed": "would make range and amplitude independently tuneable",
            "source": "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv::AMC1087_2_same_branch_requirement",
            "status": "SAME_BRANCH_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "OCG1404_3_current_verdict",
            "object": "WEP material cancellation policy",
            "value_or_formula": "no cancellation claim permitted",
            "why_not_allowed": "parent all-material theorem or multi-material source-backed fit is absent",
            "source": "1404 checkpoint",
            "status": "NO_CANCELLATION_ROUTE_TO_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def vector_pressure_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "VPG1404_0_alpha_projection",
            "channel": "alpha/Coulomb one-component projection",
            "bound_or_target": ALPHA_TARGET,
            "required_input": "P_alpha parent coefficient and tau_WEP source kernel",
            "current_status": "MISSING_PARENT_INPUTS",
            "verdict": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "VPG1404_1_surface_projection",
            "channel": "surface/binding one-component projection",
            "bound_or_target": ROBUST_TARGET,
            "required_input": "P_surface parent coefficient and binding normalization",
            "current_status": "MISSING_BINDING_INPUTS",
            "verdict": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "VPG1404_2_vector_inequality",
            "channel": "full WEP material vector",
            "bound_or_target": f"|DeltaQ^I P_I| <= {ETA_BOUND}",
            "required_input": "DeltaQ_AB^I full material tensor and P_I parent vector",
            "current_status": "MISSING_FULL_TENSOR_AND_PARENT_VECTOR",
            "verdict": "BLOCKED_VECTOR_NOT_SCORED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "VPG1404_3_cancellation_guard",
            "channel": "one-pair alpha/surface cancellation",
            "bound_or_target": CANCELLATION_RATIO,
            "required_input": "all-material invariant theorem or multi-material evidence",
            "current_status": "FORBIDDEN_BY_POLICY",
            "verdict": "CANNOT_USE_PAIR_CANCELLATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "VPG1404_4_local_transfer",
            "channel": "WEP to PPN/Newton/local GR",
            "bound_or_target": "not_applicable",
            "required_input": "local projection coefficients A_i plus EM/local residual closure",
            "current_status": "MISSING_LOCAL_PROJECTION",
            "verdict": "LOCAL_TRANSFER_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "VPG1404_5_verdict",
            "channel": "WEP composition/binding branch",
            "bound_or_target": "pressure ledger only",
            "required_input": "CBN1404_0..4 closure",
            "current_status": "NORMALIZATION_NOT_DERIVED",
            "verdict": "WEP_VECTOR_GATE_WRITTEN_NO_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1404_0_normalization",
            "claim": "WEP composition/binding normalization is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "common parent basis, P_I vector, and source kernel are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1404_1_WEP_pass",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "alpha and surface rows are pressure targets only, not predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1404_2_cancellation",
            "claim": "TA6V-PtRh10 cancellation line rescues WEP",
            "status": "FORBIDDEN_NO_CLAIM",
            "reason": "one-pair tuning is not theory and violates all-material policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1404_3_transfer",
            "claim": "WEP material pressure transfers to clocks, R10, PPN, or orbital tests",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 arena isolation remains in force",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1404_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "WEP vector prior does not close q_loc, lambda_A, EM residuals, or PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1404_0_verdict",
            "decision": "do not promote WEP composition/binding normalization",
            "basis": "pair convention exists but parent material basis/vector/source kernel are missing",
            "action": "keep material prior map nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1404_1_vector_form",
            "decision": "treat WEP as vector pressure problem",
            "basis": "eta_AB = sum_I DeltaQ_AB^I P_I is the least-cheatable form",
            "action": "future rows must fill P_I and DeltaQ_AB^I, not hide channels in one scalar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1404_2_robust_policy",
            "decision": "retain robust surface/binding lane",
            "basis": "binding sector has not been theorem-zeroed or source-valued",
            "action": "alpha-only lane can be used only as diagnostic, not as final WEP evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1404_3_next_route",
            "decision": "next target is parent WEP material response current",
            "basis": "the missing object is P_I, not another scalar pressure target",
            "action": "derive P_I from parent action/current or write explicit vector prior bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1404_0_1405",
            "target_doc": "1405-Y5-R10-RAB-parent-WEP-material-response-current-or-vector-prior-bound.md",
            "target_script": "scripts/Y5_R10_RAB_parent_WEP_material_response_current_or_vector_prior_bound.py",
            "task": "derive the parent WEP material response vector P_I from the local matter action/current, or write explicit nonclaim vector-prior bound rows",
            "success_condition": "P_alpha, P_surface, P_e, P_nuc, P_EM, and P_other are theorem-zero/source-owned or explicitly finite-prior bounded with no one-pair cancellation",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    material: list[dict[str, Any]],
    cancellation: list[dict[str, Any]],
    pressure: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()

    def row(check_id: str, status: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "timestamp_utc": now,
        }

    all_sources_ok = all(r["path_exists"] and r["anchor_found"] for r in sources)
    audit_ok = (
        any(r["audit_id"] == "CBN1404_6_conditional_normalization_theorem" for r in audit)
        and any(
            r["audit_id"] == "CBN1404_7_current_verdict"
            and r["status"] == "NORMALIZATION_NOT_DERIVED_MATERIAL_PRIOR_REQUIRED"
            for r in audit
        )
        and all(str(r["claim_allowed"]) == "False" for r in audit)
    )
    material_ok = (
        any(r["prior_id"] == "MPM1404_2_delta_alpha" and r["formula_or_value"] == DELTA_Q_ALPHA for r in material)
        and any(r["prior_id"] == "MPM1404_3_delta_surface" and r["formula_or_value"] == DELTA_Q_SURFACE for r in material)
        and any(r["prior_id"] == "MPM1404_8_vector_bound_inequality" for r in material)
        and all(str(r["valid_for_claim"]) == "False" for r in material)
    )
    cancellation_ok = (
        any(r["guard_id"] == "OCG1404_0_pair_line" and r["value_or_formula"] == f"c_surface/c_alpha = {CANCELLATION_RATIO}" for r in cancellation)
        and any(r["status"] == "NO_CANCELLATION_ROUTE_TO_CLAIM" for r in cancellation)
        and all(str(r["claim_allowed"]) == "False" for r in cancellation)
    )
    pressure_ok = (
        any(r["gate_id"] == "VPG1404_5_verdict" and r["verdict"] == "WEP_VECTOR_GATE_WRITTEN_NO_PASS" for r in pressure)
        and any(r["gate_id"] == "VPG1404_4_local_transfer" and r["verdict"] == "LOCAL_TRANSFER_BLOCKED" for r in pressure)
        and all(str(r["valid_for_claim"]) == "False" for r in pressure)
    )
    claims_ok = all(str(r["claim_allowed"]) == "False" and "NO_CLAIM" in r["status"] for r in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        NORMALIZATION_AUDIT_PATH,
        MATERIAL_PRIOR_MAP_PATH,
        CANCELLATION_GUARD_PATH,
        VECTOR_PRESSURE_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all(str((ROOT / path).resolve()).startswith(str(ROOT.resolve())) for path in output_paths)

    checks = [
        row("VAL1404_0_sources", all_sources_ok, "all cited local source paths exist and anchors are present"),
        row("VAL1404_1_normalization_audit", audit_ok, "composition/binding normalization remains exact conditional only"),
        row("VAL1404_2_material_prior", material_ok, "material vector prior map includes alpha/surface deltas and vector inequality as nonclaim"),
        row("VAL1404_3_cancellation_guard", cancellation_ok, "one-pair cancellation line is recorded and forbidden as a claim"),
        row("VAL1404_4_pressure_gate", pressure_ok, "WEP vector pressure gate blocks WEP and local-transfer claims"),
        row("VAL1404_5_claim_refusal", claims_ok, "WEP, cancellation, transfer, and local-GR claims are refused"),
        row("VAL1404_6_scope", scope_ok, "outputs are confined to post-checkpoint-work paths"),
    ]
    overall = all(check["status"] == "PASS" for check in checks)
    checks.append(
        row(
            "VAL1404_7_overall",
            overall,
            "1404 writes a nonclaim WEP material vector prior and leaves normalization/local-GR unclaimed",
        )
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    material: list[dict[str, Any]],
    cancellation: list[dict[str, Any]],
    pressure: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 1404 — WEP Composition/Binding Normalization Or Material Prior Map

**Status:** `{STATUS}`

**Current verdict:** WEP composition/binding normalization is not derived. The honest object is a material vector, `eta_AB = sum_I DeltaQ_AB^I P_WEP^I`, not a single scalar alpha rescue.

**Discipline move:** keep the Ti/Pt alpha and surface/binding rows as pressure/proxy rows only. The one-pair cancellation line `c_surface/c_alpha = {CANCELLATION_RATIO}` is explicitly forbidden as a theory result.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Composition/Binding Normalization Audit

{md_table(audit)}

## Material Prior Map

{md_table(material)}

## One-Pair Cancellation Guard

{md_table(cancellation)}

## WEP Vector Pressure Gate

{md_table(pressure)}

## Claim Gate

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    audit = normalization_audit_rows()
    material = material_prior_rows()
    cancellation = cancellation_guard_rows()
    pressure = vector_pressure_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, audit, material, cancellation, pressure, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(NORMALIZATION_AUDIT_PATH, audit)
    write_csv(MATERIAL_PRIOR_MAP_PATH, material)
    write_csv(CANCELLATION_GUARD_PATH, cancellation)
    write_csv(VECTOR_PRESSURE_GATE_PATH, pressure)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, audit, material, cancellation, pressure, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1404 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
