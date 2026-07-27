from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1419-Y5-R10-RAB-direct-source-variation-product-or-qbar-projection-matrix.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1419_SOURCE_REGISTER.csv"
DIRECT_PRODUCT_PATH = SRC_DIR / "P8_Y5_R10_1419_DIRECT_SOURCE_VARIATION_PRODUCT_ATTEMPT.csv"
PROJECTION_MATRIX_PATH = SRC_DIR / "P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv"
COEFFICIENT_VECTOR_PATH = SRC_DIR / "P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv"
SCORING_GATE_PATH = SRC_DIR / "P8_Y5_R10_1419_SCORING_ACCEPTANCE_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1419_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1419_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1419_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1419_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1419_direct_source_variation_product_not_derived_qbar_projection_matrix_written_nonclaim"
CLAIM_CEILING = (
    "direct_source_variation_product_attempt_and_qbar_projection_matrix_only_"
    "no_WEP_pass_no_R10_pass_no_PPN_pass_no_local_GR_pass_no_tau_shortcut"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


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
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1419_0_1418_doc",
            "source_path": "1418-Y5-R10-RAB-action-scale-current-owner-lock-or-qbar-source-weight-acquisition-ledger.md",
            "anchor": "NEXT1418_0_1419",
            "role": "prior checkpoint selecting direct source-variation product or projection matrix",
        },
        {
            "source_id": "SRC1419_1_1418_arena",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv",
            "anchor": "QAA1418_6_verdict",
            "role": "qbar_source_weight arena acquisition ledger",
        },
        {
            "source_id": "SRC1419_2_1068_direct",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv",
            "anchor": "DPF1068_0_preferred_route",
            "role": "direct parent product preferred but missing",
        },
        {
            "source_id": "SRC1419_3_1068_tau",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
            "anchor": "TAP1068_6_direct_product_fallback",
            "role": "WEP projection ingredients and direct product fallback",
        },
        {
            "source_id": "SRC1419_4_1068_worldtube",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
            "anchor": "SWT1068_5_verdict",
            "role": "source-worldtube missing requirements",
        },
        {
            "source_id": "SRC1419_5_1068_orbit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv",
            "anchor": "ORB1068_5_verdict",
            "role": "MICROSCOPE orbit/readout missing requirements",
        },
        {
            "source_id": "SRC1419_6_1068_force",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "anchor": "FRM1068_5_verdict",
            "role": "observed-frame force/readout map not derived",
        },
        {
            "source_id": "SRC1419_7_1044_qbar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "anchor": "QBC1044_3_qbar_source_weight",
            "role": "qbar_source_weight component and no-cancellation envelope",
        },
        {
            "source_id": "SRC1419_8_1417_qbar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
            "anchor": "QSA1417_0_qbar_source_weight",
            "role": "qbar_source_weight finite coefficient row",
        },
        {
            "source_id": "SRC1419_9_1418_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv",
            "anchor": "ACL1418_6_verdict",
            "role": "action-scale/current-owner lock not proved",
        },
        {
            "source_id": "SRC1419_10_WEP_bound",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R1_WEP_source_charge",
            "role": "WEP source-charge empirical anchor",
        },
        {
            "source_id": "SRC1419_11_clock_bound",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R2_clock_redshift",
            "role": "clock/readout guard empirical anchor",
        },
        {
            "source_id": "SRC1419_12_PPN_gamma",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R3_gamma",
            "role": "PPN gamma empirical anchor",
        },
        {
            "source_id": "SRC1419_13_PPN_beta",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R4_beta",
            "role": "PPN beta empirical anchor",
        },
        {
            "source_id": "SRC1419_14_Gdot",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R9_Gdot",
            "role": "orbital/Newton Gdot anchor",
        },
        {
            "source_id": "SRC1419_15_R10",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R10_fifth_force",
            "role": "R10 inverse-square symbolic anchor",
        },
        {
            "source_id": "SRC1419_16_R11",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "anchor": "R11_EH_operator_ledger",
            "role": "local-GR operator ledger anchor",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def direct_product_rows() -> list[dict[str, Any]]:
    return [
        {
            "product_id": "DSP1419_0_target",
            "arena": "all local/source arenas",
            "direct_product_statement": "derive P_arena directly from parent variation/readout instead of choosing tau factors",
            "required_evidence": "parent variation of S_parent gives observable residual with units, sign, source path, and readout convention",
            "current_result": "TARGET_EXACT",
            "missing_for_claim": "parent variation source-current owner and readout maps",
            "fallback_if_missing": "projection matrix with explicit missing coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_1_WEP_eta",
            "arena": "WEP_source_charge",
            "direct_product_statement": "P_WEP := |eta_AB^MTS[parent variation]|",
            "required_evidence": "delta a_AB or eta_AB from parent action in MICROSCOPE convention",
            "current_result": "MISSING_DIRECT_PARENT_PRODUCT",
            "missing_for_claim": "source worldtube, material tensor, orbit/readout kernel, eta sign/normalization",
            "fallback_if_missing": "PMX1419_0_WEP_source_charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_2_Newton_GM",
            "arena": "Newton_GM_orbital",
            "direct_product_statement": "P_GM := relative source-normalization residual after universal GM calibration",
            "required_evidence": "parent split of common source normalization vs relative kappa_A/source weight",
            "current_result": "MISSING_COMMON_RELATIVE_SPLIT",
            "missing_for_claim": "source composition/profile, calibration convention, orbital projection",
            "fallback_if_missing": "PMX1419_1_Newton_GM_orbital",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_3_R10_alpha",
            "arena": "R10_fifth_force",
            "direct_product_statement": "alpha_MTS(lambda) := parent short-range source/test residual",
            "required_evidence": "range-dependent kernel and alpha(lambda) mapping from parent variation",
            "current_result": "MISSING_RANGE_KERNEL_AND_QBAR_COEFFICIENT",
            "missing_for_claim": "real bound curve, lambda convention, K_X kernel, source/test material map",
            "fallback_if_missing": "PMX1419_2_R10_fifth_force",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_4_PPN_vector",
            "arena": "PPN",
            "direct_product_statement": "P_PPN := (delta gamma, delta beta, alpha_1, alpha_2, alpha_3, xi)_MTS",
            "required_evidence": "weak-field metric solution from parent equations with source residuals included",
            "current_result": "MISSING_WEAK_FIELD_PROJECTION",
            "missing_for_claim": "linearized field equations, source-current map, gauge convention, PPN readout",
            "fallback_if_missing": "PMX1419_3_PPN_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_5_local_GR",
            "arena": "local_GR_limit",
            "direct_product_statement": "P_local := norm of source/current residual in EH/Newton reduction",
            "required_evidence": "Bianchi-safe local reduction showing residual zero or bounded retained vector",
            "current_result": "MISSING_EH_SOURCE_REDUCTION",
            "missing_for_claim": "source-current theorem, conservation check, retained residual norm",
            "fallback_if_missing": "PMX1419_4_local_GR_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_6_clock_guard",
            "arena": "clock_readout_guard",
            "direct_product_statement": "P_clock := readout-normalization residual, not a WEP source pass",
            "required_evidence": "hbar*c/clock normalization from same parent owner or separate finite coefficient",
            "current_result": "GUARD_ONLY_NOT_SOURCE_PRODUCT",
            "missing_for_claim": "clock/readout transfer owner",
            "fallback_if_missing": "PMX1419_5_clock_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "DSP1419_7_verdict",
            "arena": "all local/source arenas",
            "direct_product_statement": "direct source-variation product route",
            "required_evidence": "DSP1419_1 through DSP1419_6 supply direct theorem-zero or numeric products",
            "current_result": "DIRECT_PRODUCT_NOT_DERIVED",
            "missing_for_claim": "all arenas require source-current/readout/projection inputs",
            "fallback_if_missing": "write projection matrix rows and keep claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "matrix_id": "PMX1419_0_WEP_source_charge",
            "arena": "WEP_source_charge",
            "observable": "eta_AB_source",
            "prediction_form": "P_WEP = |M_WEP,q qbar_source_weight + M_WEP,J current_rescaling + M_WEP,m marker_source + ...|",
            "coefficient_requirements": "M_WEP,q from source worldtube, material tensor, orbit/readout kernel, eta convention",
            "residual_inputs": "qbar_source_weight;current_rescaling_residual;source_marker_guard",
            "units": "dimensionless",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R1_WEP_source_charge",
            "acceptance_rule": "P_WEP <= 2.8e-15 only if all M entries and residuals are sourced/theorem-zero",
            "current_status": "MATRIX_ROW_SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_1_Newton_GM_orbital",
            "arena": "Newton_GM_orbital",
            "observable": "Gdot/G or relative source-normalization drift",
            "prediction_form": "P_GM = |M_GM,q(t,r) qbar_source_weight + M_GM,J current_rescaling| after common-mode GM calibration",
            "coefficient_requirements": "source composition/profile, common-vs-relative calibration map, time/range dependence, orbital observable kernel",
            "residual_inputs": "qbar_source_weight;current_rescaling_residual",
            "units": "yr^-1 or dimensionless after declared projection",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R9_Gdot",
            "acceptance_rule": "do not absorb relative source weights into measured G; compare only after units/projection declared",
            "current_status": "MATRIX_ROW_SCHEMA_READY_CALIBRATION_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_2_R10_fifth_force",
            "arena": "R10_fifth_force",
            "observable": "alpha_MTS(lambda)",
            "prediction_form": "alpha_qbar(lambda) = |M_R10,q(lambda) qbar_source_weight + M_R10,J(lambda) current_rescaling + M_R10,nonH(lambda) qbar_nonH|",
            "coefficient_requirements": "real alpha(lambda) curve, lambda convention, K_X Green/kernel normalization, source/test material map",
            "residual_inputs": "qbar_source_weight;current_rescaling_residual;qbar_nonH",
            "units": "dimensionless alpha at declared lambda",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R10_fifth_force",
            "acceptance_rule": "alpha_qbar(lambda) <= alpha_bound(lambda) only with real bound curve and no tau=1 shortcut",
            "current_status": "MATRIX_ROW_SCHEMA_READY_BOUND_CURVE_AND_KERNEL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_3_PPN_vector",
            "arena": "PPN",
            "observable": "delta_gamma;delta_beta;alpha1;alpha2;alpha3;xi",
            "prediction_form": "v_PPN = M_PPN r_source with r_source=(qbar_source_weight,current_rescaling,qbar_nonH,frame_leak,...)",
            "coefficient_requirements": "linearized field equations, gauge convention, source-current map, PPN readout basis",
            "residual_inputs": "qbar_source_weight;current_rescaling_residual;qbar_nonH;qbar_geom",
            "units": "dimensionless PPN vector",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R3_gamma;R4_beta",
            "acceptance_rule": "componentwise absolute comparison to PPN bounds after matrix coefficients are sourced",
            "current_status": "MATRIX_ROW_SCHEMA_READY_WEAK_FIELD_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_4_local_GR_vector",
            "arena": "local_GR_limit",
            "observable": "retained local source-current residual norm",
            "prediction_form": "||r_local|| <= ||qbar_source_weight|| + ||current_rescaling|| + ||qbar_nonH|| + conservation/Bianchi residuals",
            "coefficient_requirements": "EH/Newton reduction, Bianchi/conservation compatibility, residual norm and operator basis",
            "residual_inputs": "qbar_source_weight;current_rescaling_residual;qbar_nonH;Bianchi_residual",
            "units": "declared operator/residual norm",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R11_EH_operator_ledger",
            "acceptance_rule": "not an empirical pass; opens local-GR route only if residual vector theorem-zero or bounded",
            "current_status": "MATRIX_ROW_SCHEMA_READY_LOCAL_REDUCTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_5_clock_guard",
            "arena": "clock_readout_guard",
            "observable": "clock/readout residual",
            "prediction_form": "P_clock = |M_clock qbar_source_weight + M_clock,hbar hbar_readout_residual + ...|",
            "coefficient_requirements": "hbar*c/clock normalization and readout transfer from same parent owner",
            "residual_inputs": "qbar_source_weight;hbar_readout_residual;clock_coefficient_residual",
            "units": "dimensionless",
            "empirical_anchor": "source-intake/local_bounds/local_bound_claims.csv::R2_clock_redshift",
            "acceptance_rule": "clock agreement cannot screen WEP/source residual; use only as consistency guard",
            "current_status": "GUARD_ROW_SCHEMA_READY_READOUT_OWNER_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_6_total_abs_guard",
            "arena": "cross_arena",
            "observable": "no-cancellation source residual envelope",
            "prediction_form": "P_arena <= sum_i |M_arena,i r_i| with no cancellation credit unless parent-signed",
            "coefficient_requirements": "all matrix entries, residual values, units, signs, and source paths",
            "residual_inputs": "all declared source/qbar residual vector entries",
            "units": "arena-specific",
            "empirical_anchor": "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv::QBC1044_5_total_abs_guard",
            "acceptance_rule": "score only after every retained term is theorem-zero or source-backed numeric",
            "current_status": "NO_CANCELLATION_GUARD_ACTIVE_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "PMX1419_7_verdict",
            "arena": "all local/source arenas",
            "observable": "qbar_source_weight projection matrix",
            "prediction_form": "P = M r_source",
            "coefficient_requirements": "PMX1419_0 through PMX1419_6 all filled or theorem-zero",
            "residual_inputs": "source residual vector",
            "units": "arena-specific",
            "empirical_anchor": "PMX1419_0 through PMX1419_6",
            "acceptance_rule": "matrix is source-ready but unscored until coefficients/residuals are filled",
            "current_status": "PROJECTION_MATRIX_WRITTEN_UNSCORED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coefficient_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "coeff_id": "SRCV1419_0_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "relative source-only active gravitational prefactor sensitivity",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
            "source_anchor": "QSA1417_0_qbar_source_weight",
            "matrix_roles": "WEP;Newton_GM;R10;PPN;local_GR;clock_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "SRCV1419_1_current_rescaling",
            "symbol": "current_rescaling_residual",
            "definition": "source/test current normalization residual from J_A -> c_A J_A or beta_source,A",
            "current_value": "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "units": "dimensionless_or_declared_current_units",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
            "source_anchor": "QSA1417_1_current_rescaling_link",
            "matrix_roles": "WEP;Newton_GM;R10;PPN;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "SRCV1419_2_qbar_nonH",
            "symbol": "qbar_nonH",
            "definition": "non-Hilbert/boundary/domain/support-shift source residual",
            "current_value": "MISSING_NONHILBERT_BOUND",
            "units": "dimensionless_or_operator_norm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "source_anchor": "QBC1044_4_qbar_nonH",
            "matrix_roles": "R10;PPN;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "SRCV1419_3_qbar_geom",
            "symbol": "qbar_geom",
            "definition": "observed metric/coframe leakage contribution",
            "current_value": "MISSING_LIE_V_GHAT",
            "units": "dimensionless_after_normalization",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "source_anchor": "QBC1044_0_qbar_geom",
            "matrix_roles": "PPN;local_GR;WEP_direct_geometry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "SRCV1419_4_readout_clock",
            "symbol": "hbar_readout_residual",
            "definition": "clock/action-scale/readout normalization residual guard",
            "current_value": "MISSING_READOUT_OWNER_OR_COEFFICIENT",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv",
            "source_anchor": "ACL1418_5_readout_transfer",
            "matrix_roles": "clock_guard;WEP_readout_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "SRCV1419_5_verdict",
            "symbol": "r_source",
            "definition": "source residual vector for qbar projection matrix",
            "current_value": "VECTOR_DECLARED_VALUES_MISSING",
            "units": "mixed_requires_matrix_units",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv",
            "source_anchor": "PMX1419_7_verdict",
            "matrix_roles": "all",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def scoring_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SAG1419_0_direct_product",
            "gate": "direct product scoring",
            "opens_if": "DSP1419 arena row has theorem-zero or numeric observable residual with units/source/readout path",
            "current_status": "CLOSED_DIRECT_PRODUCT_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SAG1419_1_matrix_coefficients",
            "gate": "projection matrix scoring",
            "opens_if": "PMX1419 matrix coefficients have values/bounds, units, signs, source paths, and arena kernels",
            "current_status": "CLOSED_MATRIX_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SAG1419_2_residual_vector",
            "gate": "source residual vector scoring",
            "opens_if": "SRCV1419 residual coefficients are theorem-zero or source-backed numeric in the same parent basis",
            "current_status": "CLOSED_RESIDUAL_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SAG1419_3_empirical_bounds",
            "gate": "empirical comparison",
            "opens_if": "arena bounds are numeric or curve-backed and matched to the prediction variable",
            "current_status": "PARTIAL_ANCHORS_EXIST_R10_CURVE_SYMBOLIC",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SAG1419_4_refusal_guards",
            "gate": "no shortcut guard",
            "opens_if": "no tau=1, no Delta=0 by taste, no measured-G absorption, no cancellation credit",
            "current_status": "GUARDS_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SAG1419_5_overall",
            "gate": "local/source projection matrix claim gate",
            "opens_if": "SAG1419_0 or SAG1419_1+2+3 open and SAG1419_4 remains satisfied",
            "current_status": "ALL_SOURCE_PROJECTION_CLAIMS_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1419_0_direct_product",
            "decision": "do not claim direct source-variation product",
            "reason": "parent variation/readout products are missing in WEP, Newton, R10, PPN, and local-GR arenas",
            "next_action": "use projection matrix as the finite branch scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1419_1_projection_matrix",
            "decision": "projection matrix is now explicit but unscored",
            "reason": "matrix rows name coefficient, unit, source, and arena-kernel requirements without numeric shortcuts",
            "next_action": "fill the first executable matrix row, prioritizing WEP because its empirical bound anchor and missing projection pack are clearest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1419_2_best_next",
            "decision": "target first executable WEP projection row next",
            "reason": "WEP has the tightest source-charge anchor and forces source worldtube/material/orbit/readout discipline before other arenas borrow it",
            "next_action": "derive or build PMX1419_0_WEP_source_charge inputs; if unavailable, write a source acquisition checklist with no pass claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1419_0_direct_product_claim",
            "claim": "direct parent source-variation product is derived",
            "allowed": False,
            "reason": "DSP1419_7 is DIRECT_PRODUCT_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1419_1_projection_score_claim",
            "claim": "qbar projection matrix scores against local bounds",
            "allowed": False,
            "reason": "matrix coefficients and residual vector values are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1419_2_WEP_R10_claim",
            "claim": "WEP or R10 pass",
            "allowed": False,
            "reason": "WEP projection missing and R10 bound curve/kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1419_3_local_GR_claim",
            "claim": "local GR/Newton source-side reduction pass",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1419_0_1420",
            "target_doc": "1420-Y5-R10-RAB-first-executable-WEP-source-projection-row-or-acquisition-checklist.md",
            "target_script": "scripts/Y5_R10_RAB_first_executable_WEP_source_projection_row_or_acquisition_checklist.py",
            "task": "try to fill PMX1419_0_WEP_source_charge directly from parent variation or sourced WEP projection inputs; if it fails, write the exact source-worldtube/material/orbit/readout acquisition checklist",
            "success_condition": "WEP projection row becomes theorem-zero/numeric-source-backed, or every missing WEP input is acquisition-ready with path/unit/sign requirements and claim gates",
            "do_not_claim": "WEP pass; tau=1; measured-G absorption; cancellation; qbar_source_weight=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1419_1_parallel_R10",
            "target_doc": "future-R10-qbar-projection-bound-curve-and-kernel-fill.md",
            "target_script": "future_source_row_route",
            "task": "after WEP projection structure is clear, fill R10 alpha(lambda) curve and qbar kernel inputs",
            "success_condition": "R10 row has real bound curve, lambda convention, K_X kernel, source/test map, and qbar coefficient status",
            "do_not_claim": "symbolic alpha(lambda) as scored evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    direct_products: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    scoring_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        DIRECT_PRODUCT_PATH,
        PROJECTION_MATRIX_PATH,
        COEFFICIENT_VECTOR_PATH,
        SCORING_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    add(
        "VAL1419_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1419_1_direct_product",
        any(row["product_id"] == "DSP1419_7_verdict" and row["current_result"] == "DIRECT_PRODUCT_NOT_DERIVED" for row in direct_products),
        "direct source-variation product attempt fails honestly",
    )
    add(
        "VAL1419_2_projection_matrix",
        {"PMX1419_0_WEP_source_charge", "PMX1419_1_Newton_GM_orbital", "PMX1419_2_R10_fifth_force", "PMX1419_3_PPN_vector", "PMX1419_4_local_GR_vector", "PMX1419_7_verdict"}.issubset({row["matrix_id"] for row in matrix_rows})
        and all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in matrix_rows),
        "qbar projection matrix rows exist and remain nonclaim",
    )
    add(
        "VAL1419_3_coeff_vector",
        {"SRCV1419_0_qbar_source_weight", "SRCV1419_1_current_rescaling", "SRCV1419_5_verdict"}.issubset({row["coeff_id"] for row in coeff_rows})
        and all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in coeff_rows),
        "source residual coefficient vector exists and remains value-missing/nonclaim",
    )
    add(
        "VAL1419_4_scoring_gates",
        any(row["gate_id"] == "SAG1419_5_overall" and row["current_status"] == "ALL_SOURCE_PROJECTION_CLAIMS_BLOCKED" for row in scoring_gates),
        "scoring gates keep all source projection claims blocked",
    )
    add(
        "VAL1419_5_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_gates),
        "direct product, projection score, WEP/R10, and local-GR claims are refused",
    )
    add(
        "VAL1419_6_decision",
        any(row["decision_id"] == "DEC1419_2_best_next" and "WEP projection row" in row["decision"] for row in decisions),
        "decision ledger selects first executable WEP projection row next",
    )
    add(
        "VAL1419_7_next_target",
        any(row["next_id"] == "NEXT1419_0_1420" for row in next_targets),
        "next target 1420 is staged",
    )
    add(
        "VAL1419_8_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1419_9_overall",
        True,
        "1419 fails direct product and writes qbar projection matrix as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1419_9_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1419 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    direct_products: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    scoring_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1419 - Direct Source-Variation Product Or qbar Projection Matrix

**Current verdict:** the direct parent source-variation product is not derived. This keeps us from declaring WEP, Newton/GM, R10, PPN, or local-GR source-side passes. The useful advance is that the fallback is now a real projection matrix `P = M r_source`, not a vague tau split.

**Discipline move:** every matrix row is nonclaim. A row becomes score-ready only when the residual coefficient vector, projection coefficients, units, signs, source paths, and empirical bound/curve are all real. No `tau=1`, no measured-`G` absorption, and no cancellation credit are allowed.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## Direct Source-Variation Product Attempt

{md_table(direct_products)}

## qbar_source_weight Projection Matrix

{md_table(matrix_rows)}

## Source Residual Coefficient Vector

{md_table(coeff_rows)}

## Scoring Acceptance Gate

{md_table(scoring_gates)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(claim_gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    direct_products = direct_product_rows()
    matrix_rows = projection_matrix_rows()
    coeff_rows = coefficient_vector_rows()
    scoring_gates = scoring_gate_rows()
    decisions = decision_rows()
    claim_gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(
        sources,
        direct_products,
        matrix_rows,
        coeff_rows,
        scoring_gates,
        decisions,
        claim_gates,
        next_targets,
    )

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(DIRECT_PRODUCT_PATH, direct_products)
    write_csv(PROJECTION_MATRIX_PATH, matrix_rows)
    write_csv(COEFFICIENT_VECTOR_PATH, coeff_rows)
    write_csv(SCORING_GATE_PATH, scoring_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, claim_gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, direct_products, matrix_rows, coeff_rows, scoring_gates, decisions, claim_gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1419 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
