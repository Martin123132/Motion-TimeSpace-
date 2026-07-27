from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2877-Y5-R2FR-first-finite-row-fill-under-two-sign-interface-under-AX1090.md"

SRC_2876_DOC = ROOT / "2876-Y5-R2FR-shared-green-sign-convention-source-or-two-branch-nonclaim-interface-under-AX1090.md"
SRC_2876_NEXT = RESIDUALS / "P8_Y5_R2FR_2876_NEXT_TARGET.csv"
SRC_2876_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2876_VALIDATION.csv"
SRC_2876_INTERFACE = RESIDUALS / "P8_Y5_R2FR_2876_TWO_BRANCH_NONCLAIM_INTERFACE.csv"
SRC_2876_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2876_PROMOTION_REQUIREMENTS.csv"
SRC_2876_RUNNER = RESIDUALS / "P8_Y5_R2FR_2876_RUNNER_STATUS.csv"

SRC_2872_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_2872_REQUEST = RESIDUALS / "P8_Y5_R2FR_2872_NARROW_SOURCE_REQUEST.csv"
SRC_2872_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2872_VALIDATION.csv"
SRC_2871_LAW = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_SOURCE_EQUATION_AUDIT.csv"
SRC_2871_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_2871_REQUEST = RESIDUALS / "P8_Y5_R2FR_2871_NARROW_SOURCE_REQUEST.csv"
SRC_2870_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2870_DEEP_EXTRACTION_RESULTS.csv"
SRC_2870_CANDIDATES = RESIDUALS / "P8_Y5_R2FR_2870_FIRST_TRIPLET_CANDIDATE_REVIEW.csv"

SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2840_ZERO = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"

SRC_1625_BUILDER = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"
SRC_1625_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_LIVE_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_1625_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1625_VALIDATION.csv"
SRC_1869_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv"
SRC_1869_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_1869_DECISION_LEDGER.csv"
SRC_1869_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1869_VALIDATION.csv"
SRC_2169_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2169_FINITE_LOCAL_COMPONENT_SCHEMA.csv"
SRC_2169_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_2169_DECISION_LEDGER.csv"
SRC_2169_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2169_VALIDATION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2877_SOURCE_REGISTER.csv",
    "target": RESIDUALS / "P8_Y5_R2FR_2877_FIRST_FILL_TARGET_SELECTION.csv",
    "qreff_review": RESIDUALS / "P8_Y5_R2FR_2877_QREFF_ELLR_CANDIDATE_REVIEW.csv",
    "fill_attempt": RESIDUALS / "P8_Y5_R2FR_2877_QREFF_ELLR_FILL_ATTEMPT.csv",
    "qcab_fallback": RESIDUALS / "P8_Y5_R2FR_2877_QCAB_FALLBACK_REVIEW.csv",
    "interface_update": RESIDUALS / "P8_Y5_R2FR_2877_TWO_SIGN_INTERFACE_UPDATE.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2877_NORMALIZATION_PACK_SOURCE_REQUESTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2877_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2877_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2877_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2877_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2877_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2877_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "fill_copy": LOCAL_BOUNDS / "RAB_QREFF_ELLR_FIRST_FILL_ATTEMPT_2877_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_QREFF_NORMALIZATION_PACK_REQUESTS_2877_NONCLAIM.csv",
    "interface_copy": BETA_DOCS / "RAB_TWO_SIGN_INTERFACE_UPDATE_2877_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2877_qReff_normalization_pack_derivation_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2877_0_2876_doc", SRC_2876_DOC, "Status: `Y5_R2FR_2876_shared_radial_formula_recorded_sign_not_chosen_two_branch_nonclaim_interface_2877_next`;first finite row fill", "2876 selected first finite row fill"),
        ("SRC2877_1_2876_next", SRC_2876_NEXT, "NEXT2876_0_2877", "handoff to 2877"),
        ("SRC2877_2_2876_validation", SRC_2876_VALIDATION, "VAL2876_OVERALL", "2876 validation"),
        ("SRC2877_3_2876_interface", SRC_2876_INTERFACE, "SIGBR2876_PLUS;SIGBR2876_MINUS;SIGBR2876_SYMBOLIC", "two-sign interface"),
        ("SRC2877_4_2876_promotion", SRC_2876_PROMOTION, "PROM2876_2_q_R_eff;PROM2876_3_common_green", "promotion blockers"),
        ("SRC2877_5_2876_runner", SRC_2876_RUNNER, "RUN2876_0_two_branch_interface", "runner refusal"),
        ("SRC2877_6_2872_law", SRC_2872_LAW, "LAW2872_1_compact_source_charge;LAW2872_6_verdict", "q_R_eff conditional source law"),
        ("SRC2877_7_2872_template", SRC_2872_TEMPLATE, "TPL2872_0_qReff_parent_source_row;TPL2872_1_ellR_range;TPL2872_4_tau_arena", "q_R_eff finite row template"),
        ("SRC2877_8_2872_request", SRC_2872_REQUEST, "REQ2872_QREFF_PARENT_SOURCE_ROW", "q_R_eff narrow request"),
        ("SRC2877_9_2872_validation", SRC_2872_VALIDATION, "VAL2872_5_zero_not_proven;VAL2872_OVERALL", "q_R_eff validation"),
        ("SRC2877_10_2871_law", SRC_2871_LAW, "LAW2871_1_operator_source_contract;LAW2871_6_verdict", "Q_CAB conditional law"),
        ("SRC2877_11_2871_template", SRC_2871_TEMPLATE, "TPL2871_0_QCAB_parent_source_row;TPL2871_3_BCAB_boundary", "Q_CAB template"),
        ("SRC2877_12_2871_request", SRC_2871_REQUEST, "REQ2871_QCAB_PARENT_SOURCE_ROW", "Q_CAB narrow request"),
        ("SRC2877_13_2870_extraction", SRC_2870_EXTRACTION, "EXT2870_CAB;EXT2870_eff;EXT2870_Green", "deep extraction no accepted rows"),
        ("SRC2877_14_2870_candidates", SRC_2870_CANDIDATES, "REV2870_CAND2869_eff_15", "possible q_R_eff-looking row rejected"),
        ("SRC2877_15_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_4_compact_body", "symbolic q_R_eff + ell_R kernel"),
        ("SRC2877_16_2839_selector", SRC_2839_SELECTOR, "SEL2839_0_minimal_pair;SEL2839_4_projection", "minimal q_R_eff/ell_R row selector"),
        ("SRC2877_17_2840_contract", SRC_2840_CONTRACT, "PACK2840_0_range;PACK2840_1_amplitude;PACK2840_5_source", "normalization pack contract"),
        ("SRC2877_18_2840_zero", SRC_2840_ZERO, "PZ2840_1_operator_zero;PZ2840_5_joint_certificate", "parent-zero certificate remains open"),
        ("SRC2877_19_2844_flux", SRC_2844_FLUX, "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "A_total target"),
        ("SRC2877_20_1625_builder", SRC_1625_BUILDER, "PB1625_0_ZR;PB1625_1_MR2;PB1625_2_JR", "older finite coefficient builder"),
        ("SRC2877_21_1625_template", SRC_1625_TEMPLATE, "TEMPLATE1625_0_ZR;TEMPLATE1625_1_MR2;TEMPLATE1625_2_JR", "older nonclaim templates"),
        ("SRC2877_22_1625_validation", SRC_1625_VALIDATION, "VAL1625_5_template_rejected;VAL1625_OVERALL", "1625 validation"),
        ("SRC2877_23_1869_schema", SRC_1869_SCHEMA, "FLC1869_1_ZR;FLC1869_2_MR2;FLC1869_6_JR", "finite component schema"),
        ("SRC2877_24_1869_decision", SRC_1869_DECISION, "DEC1869_2_next", "1869 source chain decision"),
        ("SRC2877_25_1869_validation", SRC_1869_VALIDATION, "VAL1869_9_missing_not_ready;VAL1869_OVERALL", "1869 validation"),
        ("SRC2877_26_2169_schema", SRC_2169_SCHEMA, "FLC2169_1_ZR;FLC2169_3_lambdaR;FLC2169_6_JR", "2169 finite local schema"),
        ("SRC2877_27_2169_decision", SRC_2169_DECISION, "DEC2169_2_next", "2169 source chain decision"),
        ("SRC2877_28_2169_validation", SRC_2169_VALIDATION, "VAL2169_05_claim_gates;VAL2169_OVERALL", "2169 validation"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "target_id": "TGT2877_0_qReff_ellR",
            "rank": 1,
            "quantity_group": "q_R_eff + ell_R",
            "why_first": "the symbolic kernel already says amplitude and range must be paired before any local/R10/PPN projection",
            "source_basis": "KER2839_4_compact_body;SEL2839_0_minimal_pair;LAW2872_1_compact_source_charge",
            "attempted": True,
            "selected": True,
        },
        {
            "target_id": "TGT2877_1_Q_CAB",
            "rank": 2,
            "quantity_group": "Q_CAB",
            "why_first": "fallback numerator leg if q_R_eff/range has no live row",
            "source_basis": "LAW2871_1_operator_source_contract;TPL2871_0_QCAB_parent_source_row",
            "attempted": True,
            "selected": False,
        },
        {
            "target_id": "TGT2877_2_sigma_common_green",
            "rank": 3,
            "quantity_group": "sigma_R_source_sign + common Green",
            "why_first": "needed to compare Q_CAB and q_R_eff, but not a finite row by itself",
            "source_basis": "SIGBR2876_SYMBOLIC;PROM2876_0_sign_owner",
            "attempted": False,
            "selected": False,
        },
    ]
    return [add_common(row) for row in rows]


def qreff_review_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "review_id": "QR2877_0_kernel_pair",
            "candidate": "q_R_eff=-int_body S_R/Z_R d^3x with ell_R^2=Z_R/M_R^2",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_4_compact_body",
            "evidence_class": "SYMBOLIC_KERNEL_CONTRACT",
            "accepted_live_row": False,
            "reason_not_accepted": "no finite S_R/Z_R integral, no ell_R value, no source path/equation anchor, no boundary homogeneous policy",
        },
        {
            "review_id": "QR2877_1_selector",
            "candidate": "first finite row must pair ell_R plus q_R_eff",
            "source_path": str(SRC_2839_SELECTOR),
            "source_anchor": "SEL2839_0_minimal_pair",
            "evidence_class": "ROW_SELECTOR_ONLY",
            "accepted_live_row": False,
            "reason_not_accepted": "selector names the row shape but supplies no value or theorem-zero",
        },
        {
            "review_id": "QR2877_2_pack_contract",
            "candidate": "normalization pack: ell_R, q_R_eff, sign, boundary, tau, source",
            "source_path": str(SRC_2840_CONTRACT),
            "source_anchor": "PACK2840_0_range;PACK2840_1_amplitude",
            "evidence_class": "CONTRACT_MISSING_FIELDS",
            "accepted_live_row": False,
            "reason_not_accepted": "all required pack fields are marked missing",
        },
        {
            "review_id": "QR2877_3_2872_template",
            "candidate": "q_R_eff finite row template",
            "source_path": str(SRC_2872_TEMPLATE),
            "source_anchor": "TPL2872_0_qReff_parent_source_row",
            "evidence_class": "TEMPLATE_ONLY",
            "accepted_live_row": False,
            "reason_not_accepted": "contains MISSING_q_R_eff, MISSING_ELL_R, MISSING_PARENT_SOURCE_PATH and MISSING_EQUATION_ANCHOR",
        },
        {
            "review_id": "QR2877_4_ZR_MR2_builder",
            "candidate": "older Z_R/M_R^2/J_R builder rows",
            "source_path": str(SRC_1625_BUILDER),
            "source_anchor": "PB1625_0_ZR;PB1625_1_MR2;PB1625_2_JR",
            "evidence_class": "BUILDER_SCHEMA_ONLY",
            "accepted_live_row": False,
            "reason_not_accepted": "builder rows require source-backed input but current_status is MISSING_SOURCE_BACKED_INPUT",
        },
        {
            "review_id": "QR2877_5_component_schema",
            "candidate": "finite local component schema for Z_R, M_R^2, lambda_R, J_R",
            "source_path": str(SRC_1869_SCHEMA),
            "source_anchor": "FLC1869_1_ZR;FLC1869_2_MR2;FLC1869_6_JR",
            "evidence_class": "COMPONENT_SCHEMA_ONLY",
            "accepted_live_row": False,
            "reason_not_accepted": "numeric_value and source_path columns are MISSING_* and parent_signed=false",
        },
        {
            "review_id": "QR2877_6_deep_extraction_possible_hit",
            "candidate": "one possible q_R_eff-looking candidate from 2870",
            "source_path": str(SRC_2870_CANDIDATES),
            "source_anchor": "REV2870_CAND2869_eff_15",
            "evidence_class": "POSSIBLE_TEXT_HIT_REJECTED",
            "accepted_live_row": False,
            "reason_not_accepted": "matched target terms but was rejected for manual provenance and wrong finite q_R_eff/ell_R row requirements",
        },
        {
            "review_id": "QR2877_7_zero_certificate",
            "candidate": "parent-zero q_R_eff route",
            "source_path": str(SRC_2840_ZERO),
            "source_anchor": "PZ2840_5_joint_certificate",
            "evidence_class": "ZERO_CERTIFICATE_NOT_CLOSED",
            "accepted_live_row": False,
            "reason_not_accepted": "operator/source/boundary/readout zero clauses are not parent-signed",
        },
    ]
    return [add_common(row) for row in rows]


def fill_attempt_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "fill_id": "FILL2877_0_qReff_ellR_live_row_attempt",
                "branch_family": "two_sign_interface_2876",
                "target": "q_R_eff + ell_R",
                "q_R_eff_value": "MISSING_q_R_eff",
                "q_R_eff_units": "MISSING_q_R_eff_UNITS",
                "ell_R_value": "MISSING_ELL_R",
                "ell_R_units": "length",
                "S_R_over_Z_R": "MISSING_S_R_OVER_Z_R",
                "Z_R": "MISSING_Z_R",
                "M_R2": "MISSING_M_R2",
                "H_R_boundary": "MISSING_H_R_BOUNDARY_CLASS",
                "source_path": "MISSING_PARENT_SOURCE_PATH",
                "equation_anchor": "MISSING_EQUATION_ANCHOR",
                "source_support": "MISSING_COMPACT_SOURCE_SUPPORT",
                "arena_projection": "MISSING_TAU_ARENA",
                "sigma_branch_policy": "retain +1/-1/symbolic nonclaim branches; no physical sign chosen",
                "fill_status": "REFUSED_NO_LIVE_SOURCE_ROW",
                "numeric_value_present": False,
                "parent_zero_theorem_present": False,
                "accepted_live_row": False,
                "runner_ready": False,
            }
        )
    ]


def qcab_fallback_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fallback_id": "QCF2877_0_QCAB_law",
            "candidate": "Q_CAB=int_W J_CAB dV + boundary term",
            "source_path": str(SRC_2871_LAW),
            "source_anchor": "LAW2871_1_operator_source_contract",
            "fallback_status": "CONTRACT_ONLY_VALUE_MISSING",
            "reason_not_filled": "L_CAB,J_CAB/rho_CAB,boundary,units,branch and source anchor remain missing",
            "accepted_live_row": False,
        },
        {
            "fallback_id": "QCF2877_1_QCAB_template",
            "candidate": "Q_CAB finite row template",
            "source_path": str(SRC_2871_TEMPLATE),
            "source_anchor": "TPL2871_0_QCAB_parent_source_row",
            "fallback_status": "TEMPLATE_ONLY",
            "reason_not_filled": "contains MISSING_Q_CAB and MISSING_PARENT_SOURCE_PATH",
            "accepted_live_row": False,
        },
        {
            "fallback_id": "QCF2877_2_QCAB_deep_extraction",
            "candidate": "2870 deep extraction Q_CAB result",
            "source_path": str(SRC_2870_EXTRACTION),
            "source_anchor": "EXT2870_CAB",
            "fallback_status": "NO_ACCEPTED_SOURCE_ROW",
            "reason_not_filled": "reviewed candidates were blocker/request/schema/placeholder rows",
            "accepted_live_row": False,
        },
    ]
    return [add_common(row) for row in rows]


def interface_update_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "update_id": "INT2877_0_plus",
            "source_branch": "SIGBR2876_PLUS",
            "sigma_candidate": "+1",
            "q_R_eff_status": "MISSING_q_R_eff",
            "ell_R_status": "MISSING_ELL_R",
            "Q_CAB_status": "MISSING_Q_CAB",
            "runner_status": "STILL_BLOCKED",
            "score_allowed": False,
        },
        {
            "update_id": "INT2877_1_minus",
            "source_branch": "SIGBR2876_MINUS",
            "sigma_candidate": "-1",
            "q_R_eff_status": "MISSING_q_R_eff",
            "ell_R_status": "MISSING_ELL_R",
            "Q_CAB_status": "MISSING_Q_CAB",
            "runner_status": "STILL_BLOCKED",
            "score_allowed": False,
        },
        {
            "update_id": "INT2877_2_symbolic",
            "source_branch": "SIGBR2876_SYMBOLIC",
            "sigma_candidate": "sigma_R_source_sign",
            "q_R_eff_status": "MISSING_q_R_eff",
            "ell_R_status": "MISSING_ELL_R",
            "Q_CAB_status": "MISSING_Q_CAB",
            "runner_status": "ONLY_CLAIM_COMPATIBLE_FORM_BUT_STILL_BLOCKED",
            "score_allowed": False,
        },
    ]
    return [add_common(row) for row in rows]


def request_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "request_id": "REQ2877_0_qReff_normalization_pack",
            "priority": 1,
            "object": "q_R_eff + ell_R normalization pack",
            "exact_request": "Derive/source one same-normalization pack containing Z_R, M_R^2 or direct ell_R, S_R/Z_R, q_R_eff=-int_W S_R/Z_R d^3x, H_R boundary policy, units, source path, equation anchor and arena projection.",
            "acceptance_rule": "all fields real or parent-zero theorem; no MISSING markers; source anchors must exist; no q_Rhat/Cassini backsolve; no closure-only authority",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_next": True,
        },
        {
            "request_id": "REQ2877_1_qReff_zero_certificate",
            "priority": 2,
            "object": "q_R_eff parent-zero theorem",
            "exact_request": "Prove source silence, operator/range decoupling, boundary homogeneous silence and readout projection silence as one parent theorem.",
            "acceptance_rule": "all zero clauses parent-signed together; no partial zero promotion",
            "status": "OPEN_THEOREM_REQUEST",
            "selected_next": False,
        },
        {
            "request_id": "REQ2877_2_QCAB_fallback",
            "priority": 3,
            "object": "Q_CAB finite row or zero theorem",
            "exact_request": "If q_R_eff pack cannot be filled, fill Q_CAB with L_CAB,J_CAB/rho_CAB,boundary,units,branch,source path/equation anchor and finite value or parent-zero theorem.",
            "acceptance_rule": "must share radial convention with q_R_eff once q_R_eff exists",
            "status": "OPEN_SOURCE_REQUEST",
            "selected_next": False,
        },
    ]
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2877_0_qReff_value", "finite q_R_eff value or zero theorem", "FAIL", "no live q_R_eff source row or parent-zero theorem found"),
        ("GATE2877_1_ellR_range", "ell_R or same-normalization Z_R/M_R^2 range", "FAIL", "range rows are schema/template only"),
        ("GATE2877_2_source_density", "S_R/Z_R compact source density", "FAIL", "source normalization and support missing"),
        ("GATE2877_3_boundary", "H_R boundary/no-hair class", "FAIL", "boundary homogeneous policy missing"),
        ("GATE2877_4_arena_projection", "tau_R10/tau_PPN/tau_clock/tau_orbital", "FAIL", "arena projection rows are templates only"),
        ("GATE2877_5_QCAB_fallback", "Q_CAB fallback live row", "FAIL", "Q_CAB remains contract/template only"),
        ("GATE2877_6_two_sign_interface", "two-sign interface remains nonclaim", "PASS_GUARD_ONLY", "plus/minus/symbolic branches stay score-blocked"),
        ("GATE2877_7_runner", "strict runner can score first finite row", "FAIL", "no accepted live row exists"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "guard_passed_nonclaim": result == "PASS_GUARD_ONLY",
                "claim_unlocked": False,
            }
        )
        for gate_id, criterion, result, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2877_0_first_finite_row_fill",
                "status": "REFUSED_NO_LIVE_SOURCE_ROW",
                "accepted_qreff_ellr_rows": 0,
                "required_qreff_ellr_rows": 1,
                "accepted_qcab_fallback_rows": 0,
                "required_qcab_fallback_rows": 1,
                "reason": "q_R_eff+ell_R and Q_CAB are still symbolic/template/schema rows; two-sign interface stays nonclaim",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2877_0_qreff_attempt",
            "decision": "Promote q_R_eff + ell_R as the first finite row.",
            "result": "REFUSED",
            "because": "only symbolic kernels, contracts, builder schemas and nonclaim templates exist",
        },
        {
            "decision_id": "DEC2877_1_qcab_fallback",
            "decision": "Use Q_CAB fallback as first finite row.",
            "result": "REFUSED",
            "because": "Q_CAB also lacks finite value, zero theorem, source density and boundary provenance",
        },
        {
            "decision_id": "DEC2877_2_interface",
            "decision": "Update the two-sign interface with first-fill outcome.",
            "result": "COMPLETE_NONCLAIM",
            "because": "all branches remain explicit and score-blocked",
        },
        {
            "decision_id": "DEC2877_3_next",
            "decision": "Move to q_R_eff normalization pack derivation/intake.",
            "result": "SELECTED_2878",
            "because": "the exact missing object is now Z_R/M_R^2/S_R-over-Z_R/H_R/tau in one same-normalization source pack",
        },
    ]
    return [add_common(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2877_0_2878",
                "status": "selected_primary",
                "target_doc": "2878-Y5-R2FR-qReff-normalization-pack-derivation-or-raw-coefficient-intake-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qReff_normalization_pack_derivation_or_raw_coefficient_intake_under_AX1090_2878.py",
                "mission": "derive or source the same-normalization q_R_eff pack: Z_R, M_R^2 or ell_R, S_R/Z_R, q_R_eff integral, H_R boundary policy and tau projections; if derivation fails, create a raw coefficient intake queue without promoting claims",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2877_0_fill", OUTPUTS["fill_attempt"], BRANCH_OUTPUTS["fill_copy"], "q_R_eff+ell_R first fill attempt nonclaim copy"),
        ("COPY2877_1_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "q_R_eff normalization pack source requests nonclaim copy"),
        ("COPY2877_2_interface", OUTPUTS["interface_update"], BRANCH_OUTPUTS["interface_copy"], "two-sign interface update nonclaim copy"),
        ("COPY2877_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to q_R_eff normalization pack target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_live_row",
        "numeric_value_present",
        "parent_zero_theorem_present",
        "runner_ready",
        "score_allowed",
        "gate_passed",
        "claim_unlocked",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    target = rows_by_name["target"]
    qreff = rows_by_name["qreff_review"]
    fill = rows_by_name["fill_attempt"]
    qcab = rows_by_name["qcab_fallback"]
    interface = rows_by_name["interface_update"]
    requests = rows_by_name["requests"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2877_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2877_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2877_2_qreff_selected_first", any(row["target_id"] == "TGT2877_0_qReff_ellR" and row["selected"] is True for row in target), "q_R_eff+ell_R selected as first fill target"),
        ("VAL2877_3_qreff_review_no_accepts", len(qreff) >= 8 and not any(row["accepted_live_row"] for row in qreff), "q_R_eff+ell_R review accepts no live row"),
        ("VAL2877_4_fill_attempt_refused", fill[0]["fill_status"] == "REFUSED_NO_LIVE_SOURCE_ROW" and fill[0]["runner_ready"] is False, "fill attempt remains refused"),
        ("VAL2877_5_qcab_fallback_refused", len(qcab) >= 3 and not any(row["accepted_live_row"] for row in qcab), "Q_CAB fallback also has no live row"),
        ("VAL2877_6_interface_still_blocked", all(row["score_allowed"] is False and row["runner_status"] != "READY" for row in interface), "two-sign interface remains score-blocked"),
        ("VAL2877_7_requests_select_2878", any(row["request_id"] == "REQ2877_0_qReff_normalization_pack" and row["selected_next"] is True for row in requests), "q_R_eff normalization pack request selected next"),
        ("VAL2877_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all claim gates fail closed"),
        ("VAL2877_9_runner_refused", runner[0]["status"] == "REFUSED_NO_LIVE_SOURCE_ROW" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2877_10_next_target_2878", next_target[0]["next_id"] == "NEXT2877_0_2878" and next_target[0]["selected"] is True, "2878 normalization pack target selected"),
        ("VAL2877_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2877_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2877_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2877_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2877_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2877_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2877_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2877_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2877 attempted the first finite row under the two-sign interface, refused q_R_eff+ell_R and Q_CAB promotion because only symbolic/template/schema rows exist, kept the interface score-blocked, and selected q_R_eff normalization-pack derivation/intake for 2878.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2877 - Y5 R2FR First Finite Row Fill Under Two Sign Interface Under AX1090

Status: `Y5_R2FR_2877_first_finite_row_fill_attempted_qReff_ellR_not_live_qcab_not_live_2878_next`

## Private Verdict

2877 tried to fill the first real finite row under the two-sign interface. The priority target was `q_R_eff + ell_R`, because the kernel chain says the amplitude and range must be sourced together:

`(-Laplace+ell_R^-2) delta_R = -S_R/Z_R`, `q_R_eff=-int_W S_R/Z_R d^3x`.

The attempt does **not** pass. The corpus has good symbolic contracts and strict templates, but no live source-backed row with finite `q_R_eff`, finite or derived `ell_R`, `S_R/Z_R`, boundary/no-hair class, units, source path, equation anchor, and arena projection. The older `Z_R/M_R^2/J_R` rows are builders/schemas/templates, not evidence rows.

The Q_CAB fallback also does not pass. So the two-sign interface remains useful but score-blocked. The next narrow target is the real missing gear: a same-normalization `q_R_eff` pack deriving or sourcing `Z_R`, `M_R^2` or `ell_R`, `S_R/Z_R`, `H_R`, and `tau` projections.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## First Fill Target Selection

{md_table(rows_by_name["target"], ["target_id", "rank", "quantity_group", "why_first", "attempted", "selected", "valid_for_claim"])}

## q_R_eff + ell_R Candidate Review

{md_table(rows_by_name["qreff_review"], ["review_id", "candidate", "evidence_class", "accepted_live_row", "reason_not_accepted", "valid_for_claim"])}

## q_R_eff + ell_R Fill Attempt

{md_table(rows_by_name["fill_attempt"], ["fill_id", "target", "q_R_eff_value", "ell_R_value", "S_R_over_Z_R", "source_path", "equation_anchor", "fill_status", "runner_ready", "valid_for_claim"])}

## Q_CAB Fallback Review

{md_table(rows_by_name["qcab_fallback"], ["fallback_id", "candidate", "fallback_status", "reason_not_filled", "accepted_live_row", "valid_for_claim"])}

## Two Sign Interface Update

{md_table(rows_by_name["interface_update"], ["update_id", "source_branch", "sigma_candidate", "q_R_eff_status", "ell_R_status", "Q_CAB_status", "runner_status", "score_allowed", "valid_for_claim"])}

## Normalization Pack Source Requests

{md_table(rows_by_name["requests"], ["request_id", "priority", "object", "exact_request", "status", "selected_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "guard_passed_nonclaim", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_qreff_ellr_rows", "accepted_qcab_fallback_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "target": target_rows(),
        "qreff_review": qreff_review_rows(),
        "fill_attempt": fill_attempt_rows(),
        "qcab_fallback": qcab_fallback_rows(),
        "interface_update": interface_update_rows(),
        "requests": request_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2877_OVERALL")
    print(f"VAL2877_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
