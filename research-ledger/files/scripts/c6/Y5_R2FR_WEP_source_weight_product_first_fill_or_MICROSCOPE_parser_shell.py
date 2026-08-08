from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1703"
INPUT = QUARANTINE / "input"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1703-Y5-R2FR-WEP-source-weight-product-first-fill-or-MICROSCOPE-parser-shell.md"

SOURCE_FILES = {
    "1702_doc": ROOT / "1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md",
    "1702_validation": OUT / "P8_Y5_BRR545_1702_VALIDATION.csv",
    "1702_wep_row": OUT / "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
    "1702_product_runner": OUT / "P8_Y5_PARENT_QLOC_1702_FIRST_ARENA_PRODUCT_RUNNER.csv",
    "1067_tau_schema": OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "1476_delta_w": MICROSCOPE / "branch_locked_wep" / "coefficients" / "Ci_source_weight_delta_w_input_nonclaim_1476.csv",
    "1482_status": MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_R_source_status_1482.csv",
    "1482_doc": ROOT / "1482-Y5-R10-RAB-MICROSCOPE-official-readout-source-intake-runner-or-Hom-generator-closure.md",
    "1596_contraction": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv",
    "1608_tau_contract": OUT / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
    "1699_request_template": MICROSCOPE / "branch_locked_wep" / "source" / "MICROSCOPE_WEP_data_request_template_1699.md",
    "1699_doc": ROOT / "1699-Y5-R2FR-parent-source-owner-grammar-or-finite-WEP-request-pack.md",
}

NEEDLES = {
    "1702_doc": ["WEP Source-Weight Product Row", "NEXT1702_0_primary"],
    "1702_validation": ["VAL1702_OVERALL", "PASS"],
    "1702_wep_row": ["WEP1702_0_delta_w", "WEP1702_3_direct_product"],
    "1702_product_runner": ["PR1702_0_WEP_source_weight", "BLOCKED_MISSING_INPUTS"],
    "1067_tau_schema": ["TAQ1067_3_direct_product_option", "REFUSAL_ACTIVE"],
    "1476_delta_w": ["DW1476_0_delta_w_A", "MISSING_TAU_WEP"],
    "1482_status": ["ACCEPT1482_5_overall_parser_permission", "parser cannot evaluate tau_WEP"],
    "1482_doc": ["TAU1482_7_numeric_tau", "NOT_EVALUATED"],
    "1596_contraction": ["TCL1596_2_delta_w_amplitude_law", "EXACT_CONDITIONAL_AMPLITUDE_LAW"],
    "1608_tau_contract": ["TAU1608_0_definition", "FORMAL_DEFINITION_ONLY"],
    "1699_request_template": ["Requested Items", "Non-Claim Guardrail"],
    "1699_doc": ["MICROSCOPE Request Pack", "REQUEST_PACK_READY_DATA_NOT_ACQUIRED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1703_SOURCE_REGISTER.csv"
WEP_FILL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1703_WEP_SOURCE_WEIGHT_FILL_AUDIT.csv"
DELTA_W_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1703_DELTA_W_ROUTE.csv"
TAU_WEP_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1703_TAU_WEP_ROUTE.csv"
DIRECT_PRODUCT_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1703_DIRECT_PRODUCT_ROUTE.csv"
PARSER_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_SHELL_REQUIREMENTS.csv"
PARSER_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_DRY_RUN.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1703_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1703_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1703_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1703_VALIDATION.csv"
MANIFEST_TEMPLATE = INPUT / "P_WEP_tau_parser_manifest_TEMPLATE.json"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    WEP_FILL_AUDIT,
    DELTA_W_ROUTE,
    TAU_WEP_ROUTE,
    DIRECT_PRODUCT_ROUTE,
    PARSER_REQUIREMENTS,
    PARSER_DRY_RUN,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    WEP_FILL_AUDIT,
    DELTA_W_ROUTE,
    TAU_WEP_ROUTE,
    DIRECT_PRODUCT_ROUTE,
    PARSER_REQUIREMENTS,
    PARSER_DRY_RUN,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    WEP_FILL_AUDIT: [
        QUARANTINE / "WEP_SOURCE_WEIGHT_FILL_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_source_weight_fill_audit_1703.csv",
        QUEUE / "JR1703_WEP_SOURCE_WEIGHT_FILL_AUDIT.csv",
    ],
    DELTA_W_ROUTE: [
        QUARANTINE / "DELTA_W_ROUTE.csv",
        BRANCH_RESIDUALS / "R2FR_delta_w_route_1703.csv",
        QUEUE / "JR1703_DELTA_W_ROUTE.csv",
    ],
    TAU_WEP_ROUTE: [
        QUARANTINE / "TAU_WEP_ROUTE.csv",
        BRANCH_RESIDUALS / "R2FR_tau_WEP_route_1703.csv",
        QUEUE / "JR1703_TAU_WEP_ROUTE.csv",
    ],
    DIRECT_PRODUCT_ROUTE: [
        QUARANTINE / "DIRECT_PRODUCT_ROUTE.csv",
        BRANCH_RESIDUALS / "R2FR_direct_product_route_1703.csv",
        QUEUE / "JR1703_DIRECT_PRODUCT_ROUTE.csv",
    ],
    PARSER_REQUIREMENTS: [
        QUARANTINE / "MICROSCOPE_PARSER_SHELL_REQUIREMENTS.csv",
        BRANCH_RESIDUALS / "R2FR_MICROSCOPE_parser_shell_requirements_1703.csv",
        QUEUE / "JR1703_MICROSCOPE_PARSER_SHELL_REQUIREMENTS.csv",
    ],
    PARSER_DRY_RUN: [
        QUARANTINE / "MICROSCOPE_PARSER_DRY_RUN.csv",
        BRANCH_RESIDUALS / "R2FR_MICROSCOPE_parser_dry_run_1703.csv",
        QUEUE / "JR1703_MICROSCOPE_PARSER_DRY_RUN.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1703.csv",
        QUEUE / "JR1703_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1703.csv",
        QUEUE / "JR1703_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def has_missing(value: Any) -> bool:
    return "MISSING" in str(value).upper()


def source_path(path: Path) -> str:
    return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1703_{index}_{source_key}",
                "source_key": source_key,
                "source_path": source_path(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1703": "WEP source-weight first fill or MICROSCOPE parser-shell hard block",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def wep_fill_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_0_product_anchor",
            "object": "abs(Delta_w_TiPt*tau_WEP)",
            "route": "existing bound anchor",
            "current_evidence": "1596 records the exact conditional amplitude law and product-bound-only status",
            "status": "AVAILABLE_NONCLAIM_PRODUCT_ANCHOR",
            "blocker": "not an MTS prediction and not a Delta_w bound without tau_min",
            "next_action": "keep as comparator input only",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_1_delta_w_zero",
            "object": "Delta_w_TiPt=0",
            "route": "parent theorem-zero",
            "current_evidence": "1699/1702 keep source-owner grammar and readout no-reentry unsigned",
            "status": "BLOCKED_PARENT_ZERO_NOT_DERIVED",
            "blocker": "parent action has not signed source-owner exhaustiveness plus readout preservation",
            "next_action": "do not set Delta_w to zero in the runner",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_2_delta_w_numeric",
            "object": "Delta_w_TiPt numeric row",
            "route": "finite source-weight input",
            "current_evidence": "1476 records MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "status": "MISSING_NUMERIC_DELTA_W",
            "blocker": "no source-backed relative weight vector with units/sign/source anchor/no-cancellation rule",
            "next_action": "prefer direct product route unless parent theory supplies a real Delta_w vector",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_3_tau_wep",
            "object": "tau_WEP",
            "route": "readout/source/material projection",
            "current_evidence": "1482/1608 keep tau_WEP symbolic and not evaluated",
            "status": "MISSING_TAU_WEP",
            "blocker": "K_CMSM, source worldtube, material tensor, product convention, C_parent and tau_min are not live claim-grade inputs",
            "next_action": "build strict parser shell and request/import artifacts",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_4_direct_product",
            "object": "P_WEP_source_weight",
            "route": "direct product without Delta_w/tau split",
            "current_evidence": "1067 and 1702 allow direct product in principle but current value is MISSING_DIRECT_PRODUCT",
            "status": "MISSING_DIRECT_PRODUCT",
            "blocker": "no parent product theorem or official data product exists",
            "next_action": "make direct product the clean empirical target for a future parser",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "WFA1703_5_verdict",
            "object": "WEP source-weight score",
            "route": "first-fill attempt",
            "current_evidence": "all route gates checked against 1702 handoff and MICROSCOPE intake status",
            "status": "HARD_BLOCKED_TO_PARSER_SHELL",
            "blocker": "no theorem-zero, no numeric Delta_w, no tau_WEP, no direct product",
            "next_action": "1704 should build a drop-folder parser dry run/manual data request update",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_w_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "DWR1703_0_parent_zero",
            "quantity": "Delta_w_TiPt",
            "candidate_statement": "Delta_w_TiPt=0 from parent ordinary-matter source-owner grammar plus readout preservation",
            "required_evidence": "parent-signed grammar exhaustiveness; no source-only prefactor; readout/effective no-reentry",
            "current_status": "BLOCKED_UNSIGNED_PARENT_GRAMMAR_AND_READOUT",
            "source_anchor": "1699 Hom conditional; 1701/1702 readout commutator ledger",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "DWR1703_1_numeric_vector",
            "quantity": "Delta_w_TiPt",
            "candidate_statement": "source-backed relative weight vector with sign, units, no-cancellation convention and source path",
            "required_evidence": "numeric Delta_w_TiPt or component vector projected into Ti/Pt channel",
            "current_status": "MISSING_NUMERIC_SOURCE_WEIGHT",
            "source_anchor": "1476 DW1476_0_delta_w_A",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "DWR1703_2_product_bound_conversion",
            "quantity": "abs(Delta_w_TiPt)",
            "candidate_statement": "abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "required_evidence": "sourced tau_min with abs(tau_WEP)>=tau_min>0",
            "current_status": "BLOCKED_NO_TAU_MIN",
            "source_anchor": "1596 TCL1596_2_delta_w_amplitude_law",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "DWR1703_3_refusal",
            "quantity": "Delta_w_TiPt score",
            "candidate_statement": "do not score Delta_w from product anchor alone",
            "required_evidence": "zero theorem, numeric Delta_w, or tau_min conversion",
            "current_status": "REFUSAL_ACTIVE",
            "source_anchor": "1067 TAQ1067_4_refusal_rule",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def tau_wep_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_0_definition",
            "quantity": "tau_WEP",
            "definition_or_requirement": "tau_WEP := N_eta^-1 <K_CMSM, S_Earth x M_TiPt> in one branch-locked convention",
            "current_status": "FORMAL_DEFINITION_ONLY",
            "source_anchor": "1608 TAU1608_0_definition",
            "blocks": "numeric tau and tau_min cannot be evaluated",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_1_readout",
            "quantity": "K_CMSM/P_WEP_readout",
            "definition_or_requirement": "official MICROSCOPE readout/design matrix with masks, segment timing, units and sign convention",
            "current_status": "MISSING_OFFICIAL_MICROSCOPE_READOUT",
            "source_anchor": "1482 ACCEPT1482_0_official_arrays",
            "blocks": "parser cannot evaluate tau_WEP",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_2_source_worldtube",
            "quantity": "R_source/S_Earth",
            "definition_or_requirement": "Earth/source worldtube in observed local frame with orbit/source weighting",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "source_anchor": "1482 ACCEPT1482_1_source_worldtube",
            "blocks": "source leg of tau_WEP absent",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_3_material",
            "quantity": "M_TiPt",
            "definition_or_requirement": "Ti/Pt material response tensor in same parent source-weight basis",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source_anchor": "1482 TAU1482_6_material_tensor",
            "blocks": "Ti/Pt projection cannot be trusted from alloy label only",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_4_product_convention",
            "quantity": "N_eta/sign/eta convention",
            "definition_or_requirement": "reported Eotvos product convention with sign, absolute-value rule, and orbit average",
            "current_status": "PARTIAL_PENDING_NONCLAIM",
            "source_anchor": "1482 ACCEPT1482_2_product_convention",
            "blocks": "product route cannot promote without sign/units/orbit/source fields",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_5_c_parent",
            "quantity": "C_parent or zero certificate",
            "definition_or_requirement": "theorem-zero or source-backed finite parent coefficient in same branch",
            "current_status": "MISSING_C_PARENT_OR_ZERO_CERTIFICATE",
            "source_anchor": "1482 ACCEPT1482_4_C_parent",
            "blocks": "finite WEP branch cannot be promoted to parent-derived local GR",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_6_tau_min",
            "quantity": "tau_min",
            "definition_or_requirement": "strictly positive lower bound abs(tau_WEP)>=tau_min>0",
            "current_status": "NO_TAU_MIN_SOURCE",
            "source_anchor": "1596 DWB1596_2_tau_lower_bound; 1608 TLS1608_5_tau_min",
            "blocks": "cannot convert product anchor into Delta_w bound",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_route_id": "TWR1703_7_verdict",
            "quantity": "tau_WEP runner input",
            "definition_or_requirement": "all factors in one basis with hashes/source paths and no tau=1 shortcut",
            "current_status": "BLOCKED_MISSING_INPUTS",
            "source_anchor": "1482 ACCEPT1482_5_overall_parser_permission",
            "blocks": "WEP source-weight score",
            "accepted_for_runner": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def direct_product_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "direct_route_id": "DPR1703_0_allowed_shape",
            "quantity": "P_WEP_source_weight",
            "formula": "P_WEP_source_weight = direct parent product in reported MICROSCOPE Ti/Pt channel",
            "why_preferred": "avoids pretending Delta_w and tau_WEP are separately known",
            "required_evidence": "source-backed product theorem or official readout/source/material/product parser output",
            "current_status": "ALLOWED_IN_PRINCIPLE_NONCLAIM",
            "blocks": "no direct product row exists",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direct_route_id": "DPR1703_1_missing_data",
            "quantity": "P_WEP_source_weight",
            "formula": "P = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]>",
            "why_preferred": "keeps the physical observable as one product rather than splitting unowned factors",
            "required_evidence": "K_CMSM; S_Earth; M_TiPt; C_parent/zero; eta convention; parser manifest",
            "current_status": "MISSING_DIRECT_PRODUCT_INPUTS",
            "blocks": "parser shell can only refuse at present",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direct_route_id": "DPR1703_2_no_inversion",
            "quantity": "P_WEP_source_weight",
            "formula": "do not infer P from the experimental bound alone",
            "why_preferred": "prevents circularly choosing a product because MICROSCOPE allows it",
            "required_evidence": "forward MTS prediction before bound comparison",
            "current_status": "BOUND_INVERSION_REFUSED",
            "blocks": "2.8e-15 remains a comparator, not a prediction",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direct_route_id": "DPR1703_3_verdict",
            "quantity": "direct WEP product route",
            "formula": "direct product is the cleanest empirical branch once data exist",
            "why_preferred": "least smuggled route and easiest to audit",
            "required_evidence": "all live parser artifacts or parent product theorem",
            "current_status": "SELECTED_FOR_1704_PARSER_SHELL",
            "blocks": "not score-ready now",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parser_requirement_definitions() -> list[tuple[str, str, Path, str, str, str]]:
    return [
        (
            "PSR1703_0_readout_matrix",
            "P_WEP_K_CMSM_readout.csv",
            MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv",
            "time/session/orbit/masks/gx/gz/readout components/calibration flags/units/sign",
            "official MICROSCOPE/CMSM export or exact source-backed equivalent",
            "required_live_file_missing",
        ),
        (
            "PSR1703_1_source_worldtube",
            "P_WEP_R_source_Earth_worldtube.csv",
            MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
            "source shell/profile/orbit kernel/source response/units/source anchor",
            "Earth/source profile in observed local frame",
            "required_live_file_missing",
        ),
        (
            "PSR1703_2_material_tensor",
            "P_WEP_TiPt_material_response_tensor.csv",
            MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_TiPt_material_response_tensor.csv",
            "TA6V response/PtRh10 response/basis/uncertainty/sign/source anchor",
            "parent matter action derivation or source-backed material model",
            "required_live_file_missing",
        ),
        (
            "PSR1703_3_product_convention",
            "P_WEP_eta_product_convention.csv",
            MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
            "N_eta/eta sign/absolute convention/orbit average/units/source anchor",
            "MICROSCOPE product convention and MTS branch sign convention",
            "exists_but_partial_nonclaim_if_present",
        ),
        (
            "PSR1703_4_branch_lock",
            "P_WEP_same_parent_branch_lock.csv",
            MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv",
            "branch id/domain/source/readout/product basis/no branch mixing",
            "same-parent branch classifier",
            "guard_only_nonclaim_if_present",
        ),
        (
            "PSR1703_5_c_parent",
            "P_WEP_C_parent_or_zero_certificate.csv",
            MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_C_parent_or_zero_certificate.csv",
            "finite coefficient with units/source path or parent theorem-zero certificate",
            "same branch C_parent route",
            "required_live_file_missing",
        ),
        (
            "PSR1703_6_tau_min",
            "P_WEP_tau_min_lower_bound.csv",
            MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_tau_min_lower_bound.csv",
            "tau_min/confidence/sign/absolute convention/derivation/source path/assumptions",
            "positive lower-bound theorem or official-data computation",
            "required_live_file_missing",
        ),
        (
            "PSR1703_7_parser_manifest",
            "P_WEP_tau_parser_manifest.json",
            MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_tau_parser_manifest.json",
            "file hashes/schema versions/units/sign/no-shortcut gates/citation/license",
            "parser manifest for score-ready import",
            "required_live_file_missing_template_written",
        ),
    ]


def parser_requirement_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for requirement_id, artifact, target_path, required_fields, source_route, missing_status in parser_requirement_definitions():
        target_exists = target_path.exists()
        if target_exists and "partial" in missing_status:
            status = "EXISTS_PARTIAL_PENDING_NONCLAIM"
        elif target_exists and "guard" in missing_status:
            status = "EXISTS_GUARD_NONCLAIM"
        elif target_exists:
            status = "PRESENT_REQUIRES_VALIDATION_NONCLAIM"
        else:
            status = "MISSING_REQUIRED_LIVE_FILE"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "requirement_id": requirement_id,
                "artifact": artifact,
                "target_path": source_path(target_path),
                "target_exists": target_exists,
                "required_fields": required_fields,
                "source_or_derivation_route": source_route,
                "current_status": status,
                "acceptance_gate": "must be live source-backed artifact, not requirements-only; no MISSING markers; units/sign/hash/source path required",
                "parser_ready": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parser_dry_run_rows(requirement_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, requirement in enumerate(requirement_rows):
        target_exists = truthy(requirement["target_exists"])
        status = str(requirement["current_status"])
        if not target_exists:
            parse_status = "REFUSED_TARGET_ABSENT"
            reason = "required live artifact does not exist"
        elif "NONCLAIM" in status:
            parse_status = "REFUSED_NONCLAIM_OR_PARTIAL"
            reason = "artifact exists only as guard/partial/nonclaim input"
        else:
            parse_status = "REFUSED_UNVALIDATED"
            reason = "artifact is not validated with schema/hash/no-missing checks"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "dryrun_id": f"PDR1703_{index}_{requirement['artifact']}",
                "artifact": requirement["artifact"],
                "target_path": requirement["target_path"],
                "target_exists": target_exists,
                "parser_status": parse_status,
                "refusal_reason": reason,
                "can_parse_for_score": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "PDR1703_8_overall",
            "artifact": "WEP source-weight parser",
            "target_path": "all_required_artifacts",
            "target_exists": False,
            "parser_status": "REFUSED_MISSING_REQUIRED_INPUTS",
            "refusal_reason": "readout, source worldtube, material tensor, C_parent/zero, tau_min, and live manifest are not all present",
            "can_parse_for_score": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_0_delta_w_zero",
            "case": "set Delta_w_TiPt=0",
            "status": "REJECT_ZERO_THEOREM_CLAIM",
            "reason": "parent source-owner grammar/readout preservation remain unsigned",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_1_delta_w_numeric",
            "case": "score numeric Delta_w_TiPt",
            "status": "REJECT_DELTA_W_SCORE",
            "reason": "numeric source-weight vector and tau_min are missing",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_2_tau_wep",
            "case": "score tau_WEP projection",
            "status": "REJECT_TAU_WEP_SCORE",
            "reason": "official readout/source/material/product/C_parent/tau_min inputs are missing or nonclaim",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_3_direct_product",
            "case": "score direct P_WEP_source_weight",
            "status": "REJECT_DIRECT_PRODUCT_SCORE",
            "reason": "direct product route is allowed in shape but has no source-backed product row",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_4_parser",
            "case": "run MICROSCOPE WEP parser",
            "status": "REFUSE_PARSER_UNTIL_ARTIFACTS_EXIST",
            "reason": "parser dry-run refuses missing live artifacts and nonclaim guard rows",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1703_5_local_gr",
            "case": "claim local GR/Newton",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "WEP source-weight product is hard-blocked to parser shell; local coupling remains unresolved",
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1703_0_primary",
            "next_target": "1704-Y5-R2FR-MICROSCOPE-parser-shell-dry-run-or-manual-data-request.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_parser_shell_dry_run_or_manual_data_request.py",
            "objective": "turn the 1703 parser requirements into an executable drop-folder dry run and refreshed manual data request without scoring WEP",
            "selection_status": "selected",
            "success_condition": "parser refuses cleanly until live readout/source/material/C_parent/tau_min/manifest artifacts exist, or data-request pack is ready to send",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1703_1_theory_fallback",
            "next_target": "1704a-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
            "script": "scripts/Y5_R2FR_Delta_w_parent_zero_final_route_or_direct_product_only.py",
            "objective": "make one final parent-signature attempt for Delta_w=0; if it fails, demote split Delta_w route and use direct product only",
            "selection_status": "held_fallback",
            "success_condition": "parent-signed theorem-zero or explicit demotion of separate Delta_w route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1703_2_r10_fallback",
            "next_target": "1704b-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "script": "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "objective": "return to R10 alpha(lambda) projection after WEP parser shell is staged",
            "selection_status": "held_fallback",
            "success_condition": "lambda/Z/K/Qbar/tau and bound curve rows ready as nonclaim inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1703_0_wep_product",
            "claim": "WEP source-weight product score",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Delta_w, tau_WEP and direct product routes are all missing required evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1703_1_delta_w_zero",
            "claim": "Delta_w_TiPt=0 parent theorem",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source-owner grammar/readout no-reentry are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1703_2_tau_min",
            "claim": "positive tau_WEP lower bound",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "official readout/source/material/alignment inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1703_3_parser",
            "claim": "MICROSCOPE parser can evaluate WEP branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "parser dry-run refuses absent live artifacts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1703_4_local_GR_Newton",
            "claim": "derived local GR/Newton from WEP source branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "local coupling/source-weight branch remains unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def write_manifest_template(requirement_rows: list[dict[str, Any]]) -> None:
    INPUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "branch_id": BRANCH_ID,
        "manifest_status": "template_only_not_live",
        "valid_for_claim": False,
        "claim_allowed": False,
        "required_artifacts": [
            {
                "artifact": row["artifact"],
                "target_path": row["target_path"],
                "required_fields": row["required_fields"],
                "current_status": row["current_status"],
            }
            for row in requirement_rows
        ],
        "acceptance_gates": [
            "all target paths exist",
            "all rows parse with declared schema",
            "units and sign conventions are declared",
            "hashes/source paths/licenses/citations are recorded",
            "no MISSING markers remain",
            "score_ready remains false until separate validation promotes the row",
        ],
    }
    MANIFEST_TEMPLATE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    manifest_targets = [
        BRANCH_RESIDUALS / "R2FR_tau_parser_manifest_TEMPLATE_1703.json",
        QUEUE / "JR1703_P_WEP_tau_parser_manifest_TEMPLATE.json",
    ]
    for target in manifest_targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MANIFEST_TEMPLATE, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    fields = (
        "accepted_for_runner",
        "accepted_for_scoring",
        "can_score",
        "can_parse_for_score",
        "parser_ready",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    )
    for path in paths:
        for row in read_csv(path):
            for field in fields:
                if field in row and truthy(row[field]):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = (
        "1703-Y5",
        "P8_Y5_PARENT_QLOC_1703",
        "P8_Y5_BRR545_1703",
        "Y5_R2FR_WEP_source_weight_product_first_fill_or_MICROSCOPE_parser_shell",
    )
    for path in FORMALIZATION.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if any(marker in path.name for marker in markers):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    audit = read_csv(WEP_FILL_AUDIT)
    delta = read_csv(DELTA_W_ROUTE)
    tau = read_csv(TAU_WEP_ROUTE)
    direct = read_csv(DIRECT_PRODUCT_ROUTE)
    requirements = read_csv(PARSER_REQUIREMENTS)
    dryrun = read_csv(PARSER_DRY_RUN)
    runner = read_csv(RUNNER_REFUSAL)
    next_rows = read_csv(NEXT_TARGET)
    gates = read_csv(CLAIM_GATE)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    required_artifacts = {
        "P_WEP_K_CMSM_readout.csv",
        "P_WEP_R_source_Earth_worldtube.csv",
        "P_WEP_TiPt_material_response_tensor.csv",
        "P_WEP_eta_product_convention.csv",
        "P_WEP_same_parent_branch_lock.csv",
        "P_WEP_C_parent_or_zero_certificate.csv",
        "P_WEP_tau_min_lower_bound.csv",
        "P_WEP_tau_parser_manifest.json",
    }
    checks = [
        ("VAL1703_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1703_1_needles_present", all(truthy(row["needles_present"]) for row in sources), "all required source needles are present"),
        ("VAL1703_2_fill_audit_complete", {"WFA1703_1_delta_w_zero", "WFA1703_3_tau_wep", "WFA1703_4_direct_product", "WFA1703_5_verdict"}.issubset({row["audit_id"] for row in audit}), "fill audit covers zero, tau, direct product, and verdict rows"),
        ("VAL1703_3_fill_hard_blocked", any(row["audit_id"] == "WFA1703_5_verdict" and row["status"] == "HARD_BLOCKED_TO_PARSER_SHELL" for row in audit), "first-fill attempt hard-blocks to parser shell"),
        ("VAL1703_4_delta_routes_blocked", all(not truthy(row["accepted_for_runner"]) and (has_missing(row["current_status"]) or "BLOCKED" in row["current_status"] or "REFUSAL" in row["current_status"]) for row in delta), "Delta_w theorem/numeric/conversion routes remain blocked"),
        ("VAL1703_5_tau_routes_blocked", any(row["tau_route_id"] == "TWR1703_7_verdict" and row["current_status"] == "BLOCKED_MISSING_INPUTS" for row in tau), "tau_WEP route remains blocked by missing inputs"),
        ("VAL1703_6_direct_route_nonclaim", any(row["direct_route_id"] == "DPR1703_3_verdict" and row["current_status"] == "SELECTED_FOR_1704_PARSER_SHELL" for row in direct), "direct product route is selected only as future nonclaim parser target"),
        ("VAL1703_7_parser_requirements_complete", required_artifacts.issubset({row["artifact"] for row in requirements}), "parser shell lists every required live artifact"),
        ("VAL1703_8_parser_not_ready", all(not truthy(row["parser_ready"]) and not truthy(row["score_ready"]) for row in requirements), "parser requirements remain non-ready"),
        ("VAL1703_9_parser_dryrun_refuses", any(row["dryrun_id"] == "PDR1703_8_overall" and row["parser_status"] == "REFUSED_MISSING_REQUIRED_INPUTS" for row in dryrun), "parser dry-run refuses missing required inputs"),
        ("VAL1703_10_runner_blocks", runner and all(not truthy(row["can_score"]) and not truthy(row["accepted_for_scoring"]) for row in runner), "runner blocks all score paths"),
        ("VAL1703_11_claim_gates_blocked", gates and all(row["status"] == "BLOCKED_NO_CLAIM" and not truthy(row["claim_allowed"]) for row in gates), "all claim gates remain blocked"),
        ("VAL1703_12_next_selected", any(row["route_id"] == "NEXT1703_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects 1704 parser shell/data request route"),
        ("VAL1703_13_manifest_template", MANIFEST_TEMPLATE.exists() and "template_only_not_live" in read_text(MANIFEST_TEMPLATE), "parser manifest template written as non-live quarantine artifact"),
        ("VAL1703_14_csv_parse", csv_parses(GENERATED_CSVS), "all generated 1703 CSVs parse"),
        ("VAL1703_15_no_claim_flags", no_claim_flags(CLAIM_CHECKED_CSVS), "all generated score/prediction/claim flags remain false"),
        ("VAL1703_16_branch_copies", all(path.exists() for path in copies), "branch/quarantine/queue copies exist"),
        ("VAL1703_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1703_18_formalization_untouched", formalization_untouched(), "no 1703 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1703_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1703 WEP source-weight first-fill or MICROSCOPE parser-shell validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    delta: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    direct: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1703 - WEP Source-Weight Product First Fill Or MICROSCOPE Parser Shell",
                "## Verdict\n"
                "- 1703 tries the WEP source-weight first-fill honestly and does not get a score.\n"
                "- `Delta_w_TiPt=0` is still not parent-derived: source-owner grammar and readout no-reentry remain unsigned.\n"
                "- `tau_WEP` is still a formal projection, not a number: official readout, source worldtube, material tensor, product convention, `C_parent`, and `tau_min` are missing or nonclaim.\n"
                "- The clean route is now the direct product/parser shell: predict or import `P_WEP_source_weight` as one audited product rather than splitting two unowned factors.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, coupling, or public claim is made.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
                "## WEP Source-Weight Fill Audit",
                markdown_table(audit, ["audit_id", "object", "route", "status", "blocker", "next_action"]),
                "## Delta_w Route",
                markdown_table(delta, ["route_id", "quantity", "current_status", "required_evidence", "source_anchor"]),
                "## tau_WEP Route",
                markdown_table(tau, ["tau_route_id", "quantity", "current_status", "blocks", "source_anchor"]),
                "## Direct Product Route",
                markdown_table(direct, ["direct_route_id", "quantity", "current_status", "why_preferred", "blocks"]),
                "## MICROSCOPE Parser Shell Requirements",
                markdown_table(requirements, ["requirement_id", "artifact", "target_exists", "current_status", "required_fields"]),
                "## Parser Dry Run",
                markdown_table(dryrun, ["dryrun_id", "artifact", "parser_status", "refusal_reason"]),
                "## Runner Refusal",
                markdown_table(runner, ["runner_id", "case", "status", "reason"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"]),
                "## Claim Gates",
                markdown_table(gates, ["claim_id", "claim", "status", "reason"]),
                "## Validation",
                markdown_table(validation, ["check_id", "result", "detail"]),
                "## Working Interpretation\n"
                "This is not a loss; it is the useful kind of block. The WEP/coupling branch has stopped being foggy. Either the parent theory eventually kills `Delta_w_TiPt`, or the empirical route must produce a forward direct product `P_WEP_source_weight` from live MICROSCOPE/source/material/readout artifacts. The next best move is a parser shell that refuses cleanly until real files are dropped in.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    audit_rows = wep_fill_audit_rows()
    delta_rows = delta_w_route_rows()
    tau_rows = tau_wep_route_rows()
    direct_rows = direct_product_route_rows()
    requirement_rows = parser_requirement_rows()
    dryrun_rows = parser_dry_run_rows(requirement_rows)
    runner_rows = runner_refusal_rows()
    next_rows = next_target_rows()
    gate_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(WEP_FILL_AUDIT, audit_rows)
    write_csv(DELTA_W_ROUTE, delta_rows)
    write_csv(TAU_WEP_ROUTE, tau_rows)
    write_csv(DIRECT_PRODUCT_ROUTE, direct_rows)
    write_csv(PARSER_REQUIREMENTS, requirement_rows)
    write_csv(PARSER_DRY_RUN, dryrun_rows)
    write_csv(RUNNER_REFUSAL, runner_rows)
    write_csv(NEXT_TARGET, next_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_manifest_template(requirement_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows()
    write_csv(VALIDATION, validation)
    write_doc(source_rows, audit_rows, delta_rows, tau_rows, direct_rows, requirement_rows, dryrun_rows, runner_rows, next_rows, gate_rows, validation)

    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1703 validation PASS")


if __name__ == "__main__":
    main()
