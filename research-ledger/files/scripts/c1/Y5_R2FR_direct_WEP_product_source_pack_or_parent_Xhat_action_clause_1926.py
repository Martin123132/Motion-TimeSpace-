from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1926"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1926-Y5-R2FR-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1925_next": OUT / "P8_Y5_PARENT_QLOC_1925_NEXT_TARGET.csv",
    "1925_doc": ROOT / "1925-Y5-R2FR-parent-scalar-nohair-input-pack-or-finite-profile-rows.md",
    "1925_validation": OUT / "P8_Y5_BRR545_1925_VALIDATION.csv",
    "1094_parent_clause": OUT / "P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
    "1094_direct_contract": OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
    "1094_candidate": OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "1094_context": OUT / "P8_Y5_R10_1094_WEP_SOURCE_CONTEXT_LEDGER.csv",
    "1094_runner": OUT / "P8_Y5_R10_1094_PRODUCT_RUNNER_STATUS.csv",
    "1095_parent_clause": OUT / "P8_Y5_R10_1095_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
    "1095_formula": OUT / "P8_Y5_R10_1095_DIRECT_WEP_FORMULA_LEDGER.csv",
    "1095_numeric_requirements": OUT / "P8_Y5_R10_1095_NUMERIC_ROW_REQUIREMENTS.csv",
    "1095_thresholds": OUT / "P8_Y5_R10_1095_DD_COEFFICIENT_THRESHOLDS.csv",
    "1096_zero": OUT / "P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
    "1096_priors": OUT / "P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv",
    "1096_validation": OUT / "P8_Y5_BRR545_1096_VALIDATION.csv",
}

NEEDLES = {
    "1925_next": ["NEXT1925_0_primary", "direct WEP"],
    "1925_doc": ["STAT1925_2_best_route", "VAL1925_OVERALL"],
    "1925_validation": ["VAL1925_OVERALL", "PASS"],
    "1094_parent_clause": ["PX1094_3_verdict", "PARENT_ACTION_CLAUSE_NOT_DERIVED"],
    "1094_direct_contract": ["DWP1094_3_direct_product_bound", "MISSING_MTS_DIRECT_PRODUCT"],
    "1094_candidate": ["PRED1094_0_missing_direct_WEP_product", "MISSING_SCOREABLE_MTS_PRODUCT"],
    "1094_context": ["CTX1094_2_source_worldtube", "MISSING_XHAT_NORMALIZATION"],
    "1094_runner": ["valid_prediction_rows", "claim remains false"],
    "1095_parent_clause": ["PAC1095_4_verdict", "ACTION_CLAUSE_NOT_DERIVED"],
    "1095_formula": ["DPF1095_0_direct_observable", "FORMULA_CONTRACT_ONLY"],
    "1095_numeric_requirements": ["NR1095_0_coefficient_owner", "MISSING_READOUT_KERNEL"],
    "1095_thresholds": ["THR1095_0_alpha", "THR1095_2_combined_abs"],
    "1096_zero": ["CZ1096_4_verdict", "COEFFICIENT_ZERO_NOT_DERIVED"],
    "1096_priors": ["PRI1096_0_alpha", "PRI1096_2_common_abs"],
    "1096_validation": ["V1096_SUMMARY", "pass"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1926_SOURCE_REGISTER.csv",
    "parent_response": OUT / "P8_Y5_PARENT_QLOC_1926_PARENT_RESPONSE_AUDIT.csv",
    "direct_source_pack": OUT / "P8_Y5_PARENT_QLOC_1926_DIRECT_WEP_SOURCE_PACK_NONCLAIM.csv",
    "observed_frame": OUT / "P8_Y5_PARENT_QLOC_1926_OBSERVED_FRAME_READOUT_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1926_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1926_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1926_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1926_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1926_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["parent_response"], SOURCE_WEIGHT_DOCS / "DIRECT_WEP_PARENT_RESPONSE_AUDIT_1926_NONCLAIM.csv"),
    (OUTPUTS["direct_source_pack"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1926_DIRECT_WEP_SOURCE_PACK_NONCLAIM.csv"),
    (OUTPUTS["direct_source_pack"], QUEUE / "JR1926_DIRECT_WEP_SOURCE_PACK_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1926_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1926 direct WEP product source pack or parent Xhat action clause",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def parent_response_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_0_target",
            "clause": "parent Xhat matter-response target",
            "mathematical_statement": "delta_X S_matter is either zero by quotient invariance or gives a parent-owned coefficient vector c_I feeding one observed-frame WEP product.",
            "source_anchor": "NEXT1925_0_primary; PAC1095_1_matter_response",
            "current_status": "TARGET_SHARP",
            "missing_for_claim": "field owner, matter response, coefficient owner, source/readout kernel, and no-rescale theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_1_field_owner",
            "clause": "Xhat field owner",
            "mathematical_statement": "Xhat must be the varied parent field with fixed units, not chi_X closure notation or a fitted projection coordinate.",
            "source_anchor": "PX1094_0_field_owner; PAC1095_0_field_owner",
            "current_status": "NOT_DERIVED",
            "missing_for_claim": "parent action term, units, normalization, and quotient role",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_2_matter_response",
            "clause": "ordinary matter response",
            "mathematical_statement": "delta_X ln m_A^eff = sum_I c_I Q_A^I delta Xhat, or delta_X S_matter=0 exactly.",
            "source_anchor": "PX1094_1_matter_response; PAC1095_1_matter_response",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "missing_for_claim": "MOMS/WEP coupling-owner clauses and constant-sector universality",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_3_source_readout",
            "clause": "same observed-frame source/readout map",
            "mathematical_statement": "P_WEP = K_MICROSCOPE[e_obs,orbit,readout] * sum_I c_I Q_source^I DeltaQ_TiPt^I.",
            "source_anchor": "PAC1095_2_source_readout; CTX1094_2_source_worldtube; CTX1094_3_orbit_readout",
            "current_status": "SOURCE_READOUT_NOT_DERIVED",
            "missing_for_claim": "Earth source worldtube, orbit/readout averaging kernel, and no measured-G absorption proof",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_4_coefficient_zero",
            "clause": "coefficient vector zero or numeric owner",
            "mathematical_statement": "c_I=0 for all ordinary matter response coefficients, or c_I is numeric/source-backed before material-pair choice.",
            "source_anchor": "CZ1096_4_verdict; NR1095_0_coefficient_owner",
            "current_status": "COEFFICIENT_ZERO_NOT_DERIVED",
            "missing_for_claim": "constant-sector universality, no hidden-visible hom, basis owner, and readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_5_formula_contract",
            "clause": "direct WEP formula contract",
            "mathematical_statement": "P_WEP_alpha_direct is scoreable only when all legs are parent-owned or explicitly source-backed in the same convention.",
            "source_anchor": "DWP1094_3_direct_product_bound; DPF1095_0_direct_observable",
            "current_status": "FORMULA_CONTRACT_ONLY",
            "missing_for_claim": "MTS direct product value is still missing",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DWP1926_6_verdict",
            "clause": "1926 direct WEP product verdict",
            "mathematical_statement": "The direct WEP product source pack is now explicit, but the parent response/action clause is not derived and no MTS prediction row exists.",
            "source_anchor": "DWP1926_1_field_owner through DWP1926_5_formula_contract",
            "current_status": "PARENT_RESPONSE_NOT_DERIVED_SOURCE_PACK_STAGED",
            "missing_for_claim": "parent coefficient vector or exact theorem-zero plus observed-frame source/readout map",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def direct_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_0_P_WEP_alpha_direct_threshold",
            "object": "P_WEP_alpha_direct threshold",
            "numeric_value": "4.797780522732e-05",
            "units": "dimensionless",
            "source_anchor": "DWP1094_3_direct_product_bound",
            "status": "NUMERIC_THRESHOLD_NONCLAIM",
            "missing_for_prediction": "MTS direct product value from parent action",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_1_c_alpha_DD_threshold",
            "object": "c_alpha_DD coefficient threshold",
            "numeric_value": "8.3202449332435330e-10",
            "units": "dimensionless",
            "source_anchor": "THR1095_0_alpha; PRI1096_0_alpha",
            "status": "NUMERIC_THRESHOLD_NONCLAIM",
            "missing_for_prediction": "parent c_alpha_DD value or zero theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_2_c_surface_DD_threshold",
            "object": "c_surface_DD coefficient threshold",
            "numeric_value": "6.9875016461438634e-11",
            "units": "dimensionless",
            "source_anchor": "THR1095_1_surface; PRI1096_1_surface",
            "status": "NUMERIC_THRESHOLD_NONCLAIM",
            "missing_for_prediction": "parent c_surface_DD value or zero theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_3_c_common_abs_threshold",
            "object": "combined absolute coefficient threshold",
            "numeric_value": "6.4461422294339073e-11",
            "units": "dimensionless",
            "source_anchor": "THR1095_2_combined_abs; PRI1096_2_common_abs",
            "status": "NUMERIC_THRESHOLD_NONCLAIM",
            "missing_for_prediction": "parent common coefficient or coefficient vector norm",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_4_parent_coefficient_vector",
            "object": "parent coefficient vector c_I",
            "numeric_value": "MISSING_PARENT_COEFFICIENT_VECTOR",
            "units": "basis-dependent dimensionless response",
            "source_anchor": "NR1095_0_coefficient_owner; CZ1096_4_verdict",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "missing_for_prediction": "numeric c_I or exact c_I=0 theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_5_source_vector",
            "object": "Earth/source vector Q_source^I",
            "numeric_value": "SMOKE_DD_VECTOR_ONLY",
            "units": "DD/material basis",
            "source_anchor": "NR1095_1_source_vector; CTX1094_2_source_worldtube",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "missing_for_prediction": "observed-frame source worldtube in same basis",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_6_material_delta_vector",
            "object": "Ti/Pt material response DeltaQ^I",
            "numeric_value": "SMOKE_DELTA_PRESENT_NOT_FULL_TENSOR",
            "units": "DD/material basis",
            "source_anchor": "NR1095_2_material_delta; CTX1094_1_material_response",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "missing_for_prediction": "full material tensor or theorem reducing to DD smoke convention",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_7_readout_kernel",
            "object": "K_MICROSCOPE observed-frame kernel",
            "numeric_value": "MISSING_READOUT_KERNEL",
            "units": "observable eta map",
            "source_anchor": "NR1095_3_readout_kernel; CTX1094_3_orbit_readout",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "missing_for_prediction": "orbit/readout/attitude kernel or direct observable theorem",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_8_no_rescale_proof",
            "object": "no measured-G/source-weight absorption proof",
            "numeric_value": "POLICY_ONLY",
            "units": "theorem/policy",
            "source_anchor": "NR1095_4_no_rescale; PX1094_2_no_rescale_cheat",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "missing_for_prediction": "parent-signed no-rescale theorem in same observed frame",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSP1926_9_MTS_direct_product_prediction",
            "object": "MTS P_WEP_alpha_direct prediction",
            "numeric_value": "MISSING_MTS_DIRECT_PRODUCT",
            "units": "dimensionless",
            "source_anchor": "PRED1094_0_missing_direct_WEP_product",
            "status": "MISSING_SCOREABLE_MTS_PRODUCT",
            "missing_for_prediction": "parent response clause or source-backed numeric product",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def observed_frame_rows() -> list[dict[str, Any]]:
    specs = [
        ("OFR1926_0_same_frame", "same observed-frame force/readout map as GR baseline", "POLICY_WRITTEN_NOT_PARENT_SIGNED", "PX1094_2_no_rescale_cheat", "prevents hiding relative residuals in calibration"),
        ("OFR1926_1_source_worldtube", "Earth/source stress and composition in the same basis", "MISSING_SOURCE_WORLDTUBE", "CTX1094_2_source_worldtube", "sets source leg of WEP product"),
        ("OFR1926_2_orbit_readout", "MICROSCOPE orbit/readout averaging kernel", "MISSING_NUMERIC_KERNEL", "CTX1094_3_orbit_readout; NR1095_3_readout_kernel", "maps theory force into eta_AB"),
        ("OFR1926_3_material_basis", "full material tensor or declared DD reduction theorem", "SMOKE_DELTA_PRESENT_NOT_FULL_TENSOR", "NR1095_2_material_delta", "prevents one-pair cancellation games"),
        ("OFR1926_4_coefficient_policy", "coefficient vector fixed before material choice", "POLICY_ONLY_NOT_PARENT_DERIVED", "PAC1095_3_no_cancellation", "keeps product predictive rather than fitted"),
        ("OFR1926_5_runner_refusal", "runner refuses claim until valid MTS prediction exists", "RUNNER_REFUSES_AS_EXPECTED", "APR1094_0_direct_WEP_product_stub", "current claim remains false"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "requirement": requirement,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "why_needed": why_needed,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for contract_id, requirement, current_status, source_anchor, why_needed in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_0_thresholds",
            "requirement": "numeric WEP/DD thresholds are present",
            "status": "PASS_NONCLAIM_THRESHOLD_ONLY",
            "evidence": "DSP1926_0 through DSP1926_3",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_1_parent_response",
            "requirement": "parent Xhat action clause signs field owner and matter response",
            "status": "FAIL_PARENT_RESPONSE_NOT_DERIVED",
            "evidence": "DWP1926_1_field_owner; DWP1926_2_matter_response",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_2_coefficient_zero",
            "requirement": "c_I=0 theorem or numeric source-backed c_I",
            "status": "FAIL_COEFFICIENT_OWNER_MISSING",
            "evidence": "DWP1926_4_coefficient_zero; DSP1926_4_parent_coefficient_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_3_observed_frame",
            "requirement": "source worldtube, readout kernel, material basis, and no-rescale theorem",
            "status": "FAIL_OBSERVED_FRAME_CONTRACT_INCOMPLETE",
            "evidence": "OFR1926_1_source_worldtube through OFR1926_4_coefficient_policy",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_4_MTS_prediction",
            "requirement": "numeric MTS direct WEP product row",
            "status": "FAIL_MISSING_SCOREABLE_MTS_PRODUCT",
            "evidence": "DSP1926_9_MTS_direct_product_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1926_5_local_WEP_claim",
            "requirement": "local WEP/local-GR claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1926_1_parent_response; CG1926_2_coefficient_zero; CG1926_3_observed_frame; CG1926_4_MTS_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1926_0_parent_response_result",
            "decision": "PARENT_RESPONSE_ACTION_CLAUSE_NOT_DERIVED",
            "why": "field owner, matter response, source/readout kernel, no-rescale theorem, and coefficient vector owner do not close together",
            "next_action": "move the unresolved weight into coefficient-vector/constant-sector derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1926_1_source_pack_result",
            "decision": "DIRECT_WEP_SOURCE_PACK_STAGED_NONCLAIM",
            "why": "MICROSCOPE/DD thresholds are numeric, but the MTS direct product and coefficient vector are missing",
            "next_action": "use thresholds only as private acceptance gates until parent coefficients are derived or externally sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1926_2_next_route",
            "decision": "MOVE_TO_CONSTANT_SECTOR_UNIVERSALITY",
            "why": "if ordinary constants are parent superselection data, the DD coefficient vector can theorem-zero cleanly; otherwise finite coefficient priors are required",
            "next_action": "1927 should attack constant-sector universality or stage finite coefficient source priors",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1926_0_primary",
            "selection_status": "selected",
            "target_doc": "1927-Y5-R2FR-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
            "target_script": "scripts/Y5_R2FR_constant_sector_universality_theorem_or_finite_coefficient_source_prior_1927.py",
            "objective": "derive ordinary constants and response coefficients as parent superselection data independent of hidden invariants; otherwise stage finite DD/source coefficient priors",
            "success_condition": "c_I=0 theorem for ordinary matter response, or source-backed finite coefficient rows with no pair-cancellation loophole",
            "do_not": "do not use unsourced coefficient priors, one-pair cancellations, tau_WEP=1, clock transfer, or WEP/local-GR claims",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1926_0_gain",
            "area": "direct WEP scoring",
            "summary": "1926 separates bound-side thresholds from theory-side predictions: thresholds are real private gates, but MTS still lacks P_WEP_alpha_direct.",
            "status": "THRESHOLDS_READY_PREDICTION_MISSING",
            "what_it_means": "the WEP branch is testable in shape, not claimable in value",
            "next": "coefficient-vector/constant-sector derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1926_1_missing",
            "area": "parent matter response",
            "summary": "The missing centre is no longer vague coupling; it is the parent-owned coefficient vector c_I or an exact c_I=0 theorem.",
            "status": "COUPLING_OWNER_EXPOSED",
            "what_it_means": "this is the coupling bottleneck in a clean form",
            "next": "constant-sector universality theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_response": parent_response_rows(),
        "direct_source_pack": direct_source_pack_rows(),
        "observed_frame": observed_frame_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append({"validation_id": "VAL1926_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    parent = parse_csv(OUTPUTS["parent_response"])
    verdict = next(row for row in parent if row["audit_id"] == "DWP1926_6_verdict")
    rows.append({"validation_id": "VAL1926_01_parent_response", "status": "PASS" if verdict["current_status"] == "PARENT_RESPONSE_NOT_DERIVED_SOURCE_PACK_STAGED" and all(row["proof_pass"] == "False" for row in parent) else "FAIL", "detail": "parent response action clause not derived", "valid_for_claim": False, "claim_allowed": False})
    pack = parse_csv(OUTPUTS["direct_source_pack"])
    threshold_rows = [row for row in pack if row["status"] == "NUMERIC_THRESHOLD_NONCLAIM"]
    thresholds_positive = all(float(row["numeric_value"]) > 0 for row in threshold_rows)
    rows.append({"validation_id": "VAL1926_02_thresholds", "status": "PASS" if len(threshold_rows) == 4 and thresholds_positive else "FAIL", "detail": "numeric threshold rows are positive and nonclaim", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1926_03_missing_prediction", "status": "PASS" if any(row["numeric_value"] == "MISSING_MTS_DIRECT_PRODUCT" for row in pack) and any(row["numeric_value"] == "MISSING_PARENT_COEFFICIENT_VECTOR" for row in pack) else "FAIL", "detail": "MTS direct product and parent coefficient vector remain missing", "valid_for_claim": False, "claim_allowed": False})
    observed = parse_csv(OUTPUTS["observed_frame"])
    rows.append({"validation_id": "VAL1926_04_observed_frame", "status": "PASS" if any(row["current_status"] == "MISSING_SOURCE_WORLDTUBE" for row in observed) and any(row["current_status"] == "MISSING_NUMERIC_KERNEL" for row in observed) else "FAIL", "detail": "source/readout observed-frame contract remains incomplete", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1926_5_local_WEP_claim")
    rows.append({"validation_id": "VAL1926_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "local WEP/local-GR claim remains blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1926_06_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_CONSTANT_SECTOR_UNIVERSALITY" for row in decisions) else "FAIL", "detail": "constant-sector route selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1926_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1927-Y5-R2FR-constant-sector") else "FAIL", "detail": "1927 constant-sector target selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = True
    claim_safe = True
    for path in generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    claim_safe = False
        except Exception:
            csv_ok = False
    rows.append({"validation_id": "VAL1926_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1926_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1926_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1926_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1926-") or "_1926" in path.name or "1926_" in path.name or "Y5_R2FR_direct_WEP" in path.name)
    rows.append({"validation_id": "VAL1926_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1926_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1926_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1926 direct WEP product source pack or parent Xhat action clause", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1926 - Direct WEP Product Source Pack Or Parent Xhat Action Clause

## Purpose

This checkpoint tries to turn the local scalar branch into a direct, observed-frame WEP product instead of splitting the problem into unsourced beta/tau placeholders. It attempts the parent Xhat matter-response derivation first; if that fails, it stages the exact source-pack rows needed for a future numeric product.

## Result

- Bound-side thresholds are numeric and useful as private acceptance gates.
- The parent Xhat matter-response/action clause is not derived.
- The theory-side product is still missing: no parent coefficient vector `c_I`, no exact `c_I=0` theorem, and no full observed-frame source/readout kernel.
- Direct WEP source-pack rows are staged as nonclaim.
- The next target is constant-sector universality: either derive ordinary response coefficients as parent superselection data, or keep finite coefficient priors nonclaim.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Response Audit

{markdown_table(rows_by_name["parent_response"])}

## Direct WEP Source Pack

{markdown_table(rows_by_name["direct_source_pack"])}

## Observed-Frame Readout Contract

{markdown_table(rows_by_name["observed_frame"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
