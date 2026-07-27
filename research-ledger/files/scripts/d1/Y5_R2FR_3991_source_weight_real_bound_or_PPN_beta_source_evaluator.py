from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3991"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3991-Y5-R2FR-source-weight-real-bound-or-PPN-beta-source-evaluator.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3991_SOURCE_REGISTER.csv",
    "anchors": SRC / "P8_Y5_R2FR_3991_REAL_SOURCE_WEIGHT_BOUND_ANCHORS.csv",
    "schema": SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_SCHEMA.csv",
    "cases": SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_RESULTS.csv",
    "transfer": SRC / "P8_Y5_R2FR_3991_WEP_TO_PPN_TRANSFER_LEDGER.csv",
    "decision": SRC / "P8_Y5_R2FR_3991_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3991_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3991_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3991_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3991_VALIDATION.csv",
}

NEXT_DOC = "3992-Y5-R2FR-parent-source-weight-projection-or-WEP-tau-denominator.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3992_parent_source_weight_projection_or_WEP_tau_denominator.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC3991_00_3990_next", SRC / "P8_Y5_R2FR_3990_NEXT_TARGET.csv", "NEXT3990_0", "3990 handoff"),
        ("SRC3991_01_3990_bound", SRC / "P8_Y5_R2FR_3990_SOURCE_WEIGHT_BOUND_ROWS.csv", "SWB3990_6_beta", "3990 beta feed bound"),
        ("SRC3991_02_3990_schema", SRC / "P8_Y5_R2FR_3990_FIRST_REAL_SOURCE_WEIGHT_BOUND_SCHEMA.csv", "SWS3990_1", "3990 source-weight schema"),
        ("SRC3991_03_WEP_real_bound", SRC / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_BOUND_ROW.csv", "WEP1934_0_MICROSCOPE_TiPt_eta", "real MICROSCOPE WEP bound"),
        ("SRC3991_04_WEP_smoke", SRC / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_NONCLAIM_SMOKE_ROW.csv", "SMOKE1934_0_MTS_WEP_source_weight_placeholder", "WEP smoke placeholder"),
        ("SRC3991_05_R10_deltaW", SRC / "P8_Y5_R10_1476_DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv", "DW1476_0_delta_w_A", "R10 delta-w source-weight input"),
        ("SRC3991_06_1887_template", SRC / "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv", "FSV1887_PPN_BETA_SOURCE_NONCLAIM", "finite source-weight vector template"),
        ("SRC3991_07_2514_beta", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_0_source", "finite beta source vector"),
        ("SRC3991_08_2631_ppn", SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv", "PPNV2631_4_wR", "full PPN source-weight slot"),
        ("SRC3991_09_3917_beta", SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv", "BET3917_2_fallback", "beta-source fallback pass rule"),
        ("SRC3991_10_3919_lock", SRC / "P8_Y5_R2FR_3919_BETA_SOURCE_LOCK_DERIVATION.csv", "BETA3919_4_source_zero", "conditional beta-source theorem zero"),
        ("SRC3991_11_1224_product", SRC / "P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv", "PROD1224_0_source_weight", "WEP product law"),
        ("SRC3991_12_1477_rules", SRC / "P8_Y5_R10_1477_CI_SOURCE_WEIGHT_EVALUATOR_RULES_V2.csv", "EVR1477_2_no_bound_inversion", "bound inversion refusal guard"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def get_wep_bound_row() -> dict[str, str]:
    rows = read_csv(SRC / "P8_Y5_PARENT_QLOC_1934_WEP_SOURCE_WEIGHT_BOUND_ROW.csv")
    for row in rows:
        if row.get("bound_id") == "WEP1934_0_MICROSCOPE_TiPt_eta":
            return row
    raise RuntimeError("WEP1934_0_MICROSCOPE_TiPt_eta row missing")


def beta_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv")
    for row in rows:
        if row.get("component_id") == "DBETA2514_0_source":
            return float(row["beta_bound"])
    raise RuntimeError("DBETA2514_0_source beta bound missing")


def anchor_rows(timestamp: str) -> list[dict[str, Any]]:
    wep = get_wep_bound_row()
    eta_bound = float(wep["reported_no_violation_level_abs_eta"])
    sigma_quad = float(wep["combined_sigma_quadrature"])
    return [
        {
            "anchor_id": "ANCH3991_0_WEP_MICROSCOPE_product",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_Ti_Pt",
            "real_observable_bound": eta_bound,
            "units": wep["units"],
            "source_url": wep["source_url"],
            "source_doi": wep["source_doi"],
            "crosscheck_url": wep["crosscheck_url"],
            "crosscheck_doi": wep["crosscheck_doi"],
            "extraction": "imported from existing source-backed WEP1934 row",
            "usable_bound_statement": "|P_WEP_source_weight|=|Delta_w_TiPt * tau_WEP| <= eta_bound_abs",
            "combined_sigma_quadrature": sigma_quad,
            "projection_needed": "tau_WEP and material/source contrast denominator",
            "claim_status": "REAL_OBSERVABLE_BOUND_ANCHOR_PROJECTION_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "anchor_id": "ANCH3991_1_PPN_beta_threshold",
            "arena": "PPN_beta",
            "observable": "beta_minus_1_source_component",
            "real_observable_bound": beta_bound(),
            "units": "dimensionless",
            "source_url": str(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv"),
            "source_doi": "local_internal_bound_row",
            "crosscheck_url": str(SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv"),
            "crosscheck_doi": "local_internal_beta_rule",
            "extraction": "imported from 2514 beta_bound row and 3917 fallback rule",
            "usable_bound_statement": "delta_beta_source_abs <= beta_bound only after source/theorem/numeric rows close",
            "combined_sigma_quadrature": "",
            "projection_needed": "A_source/B_source theorem-zero or numeric PPN source-weight projection",
            "claim_status": "BETA_THRESHOLD_AVAILABLE_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "BSE3991_0_direct_beta",
            "route": "direct_PPN_source_beta",
            "required_inputs": "A_source;B_source;epsilon_SN OR theorem-zero certificate B_source=A_source^2",
            "formula": "delta_beta_source_abs=abs(B_source/A_source^2-1)+abs(epsilon_SN)",
            "pass_rule": "delta_beta_source_abs <= 7.8e-05",
            "refusal_rule": "missing A_source/B_source/theorem-zero blocks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "schema_id": "BSE3991_1_3990_envelope",
            "route": "3990_no_Hom_envelope",
            "required_inputs": "R_matter_descent;epsilon_no_hom_species_source;epsilon_action_line_universality;epsilon_readout_reentry;epsilon_SN",
            "formula": "delta_beta_source_abs <= abs(R_matter_descent)+epsilon_no_hom_species_source+epsilon_action_line_universality+epsilon_readout_reentry+abs(epsilon_SN)",
            "pass_rule": "no-cancellation sum below beta bound",
            "refusal_rule": "any missing parent coefficient blocks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "schema_id": "BSE3991_2_WEP_transfer",
            "route": "WEP_product_bound_transfer",
            "required_inputs": "eta_bound_abs;tau_WEP;material/source contrast;K_beta_from_WEP;epsilon_SN",
            "formula": "delta_beta_source_abs <= abs(K_beta_from_WEP)*eta_bound_abs/abs(tau_WEP*material_contrast)+abs(epsilon_SN)",
            "pass_rule": "transfer is only valid when denominator and K_beta projection are numeric and source-backed",
            "refusal_rule": "do not invert the WEP bound into MTS coupling without tau/material/K projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    eta_bound = float(get_wep_bound_row()["reported_no_violation_level_abs_eta"])
    return [
        {
            "case_id": "CASE3991_0_parent_theorem_zero",
            "route": "direct_PPN_source_beta",
            "theorem_zero": True,
            "A_source": "",
            "B_source": "",
            "R_matter_descent": "",
            "epsilon_no_hom_species_source": "",
            "epsilon_action_line_universality": "",
            "epsilon_readout_reentry": "",
            "epsilon_SN": 0.0,
            "eta_bound_abs": "",
            "tau_WEP": "",
            "material_contrast": "",
            "K_beta_from_WEP": "",
            "parent_inputs_status": "THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3991_1_real_WEP_anchor_projection_blocked",
            "route": "WEP_product_bound_transfer",
            "theorem_zero": False,
            "A_source": "",
            "B_source": "",
            "R_matter_descent": "",
            "epsilon_no_hom_species_source": "",
            "epsilon_action_line_universality": "",
            "epsilon_readout_reentry": "",
            "epsilon_SN": "",
            "eta_bound_abs": eta_bound,
            "tau_WEP": "",
            "material_contrast": "",
            "K_beta_from_WEP": "",
            "parent_inputs_status": "REAL_WEP_BOUND_PRESENT_TAU_MATERIAL_K_MISSING",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3991_2_WEP_transfer_toy_projection",
            "route": "WEP_product_bound_transfer",
            "theorem_zero": False,
            "A_source": "",
            "B_source": "",
            "R_matter_descent": "",
            "epsilon_no_hom_species_source": "",
            "epsilon_action_line_universality": "",
            "epsilon_readout_reentry": "",
            "epsilon_SN": 0.0,
            "eta_bound_abs": eta_bound,
            "tau_WEP": 1.0,
            "material_contrast": 1.0,
            "K_beta_from_WEP": 1.0,
            "parent_inputs_status": "TOY_PROJECTION_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3991_3_3990_small_envelope_smoke",
            "route": "3990_no_Hom_envelope",
            "theorem_zero": False,
            "A_source": "",
            "B_source": "",
            "R_matter_descent": 0.0,
            "epsilon_no_hom_species_source": 8.33333041598e-07,
            "epsilon_action_line_universality": 2.0e-06,
            "epsilon_readout_reentry": 3.0e-06,
            "epsilon_SN": 4.0e-06,
            "eta_bound_abs": "",
            "tau_WEP": "",
            "material_contrast": "",
            "K_beta_from_WEP": "",
            "parent_inputs_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3991_4_missing_parent_rows",
            "route": "3990_no_Hom_envelope",
            "theorem_zero": False,
            "A_source": "",
            "B_source": "",
            "R_matter_descent": "",
            "epsilon_no_hom_species_source": "",
            "epsilon_action_line_universality": "",
            "epsilon_readout_reentry": "",
            "epsilon_SN": "",
            "eta_bound_abs": "",
            "tau_WEP": "",
            "material_contrast": "",
            "K_beta_from_WEP": "",
            "parent_inputs_status": "MISSING_PARENT_INPUT",
            "timestamp_utc": timestamp,
        },
    ]


def optional_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def evaluate_case(row: dict[str, Any], beta_limit: float) -> dict[str, Any]:
    case_id = row["case_id"]
    route = row["route"]
    theorem_zero = str(row.get("theorem_zero", "")).lower() == "true"
    status = row.get("parent_inputs_status", "")

    result: dict[str, Any] = {
        "case_id": case_id,
        "route": route,
        "input_status": status,
        "beta_bound": beta_limit,
        "delta_beta_source_abs": "MISSING",
        "passes_beta_bound": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }

    if theorem_zero:
        epsilon_sn = optional_float(row.get("epsilon_SN")) or 0.0
        delta_beta = abs(epsilon_sn)
        result.update(
            {
                "delta_beta_source_abs": f"{delta_beta:.12g}",
                "passes_beta_bound": delta_beta <= beta_limit,
                "score_ready": False,
                "input_status": "CONDITIONAL_THEOREM_ZERO_PARENT_UNSIGNED",
            }
        )
        return result

    if route == "direct_PPN_source_beta":
        a_source = optional_float(row.get("A_source"))
        b_source = optional_float(row.get("B_source"))
        epsilon_sn = optional_float(row.get("epsilon_SN"))
        if a_source is None or b_source is None or epsilon_sn is None or a_source == 0.0:
            result["input_status"] = "MISSING_A_SOURCE_B_SOURCE_OR_EPSILON_SN"
            return result
        delta_beta = abs(b_source / (a_source * a_source) - 1.0) + abs(epsilon_sn)
    elif route == "3990_no_Hom_envelope":
        values = [
            optional_float(row.get("R_matter_descent")),
            optional_float(row.get("epsilon_no_hom_species_source")),
            optional_float(row.get("epsilon_action_line_universality")),
            optional_float(row.get("epsilon_readout_reentry")),
            optional_float(row.get("epsilon_SN")),
        ]
        if any(value is None for value in values):
            result["input_status"] = "MISSING_3990_ENVELOPE_INPUT"
            return result
        delta_beta = sum(abs(value) for value in values if value is not None)
    elif route == "WEP_product_bound_transfer":
        eta_bound = optional_float(row.get("eta_bound_abs"))
        tau_wep = optional_float(row.get("tau_WEP"))
        material_contrast = optional_float(row.get("material_contrast"))
        k_beta = optional_float(row.get("K_beta_from_WEP"))
        epsilon_sn = optional_float(row.get("epsilon_SN"))
        if eta_bound is None:
            result["input_status"] = "MISSING_WEP_ETA_BOUND"
            return result
        if tau_wep is None or material_contrast is None or k_beta is None or epsilon_sn is None:
            result["input_status"] = "REAL_WEP_BOUND_PRESENT_TRANSFER_DENOMINATOR_MISSING"
            return result
        denominator = abs(tau_wep * material_contrast)
        if denominator == 0.0:
            result["input_status"] = "ZERO_WEP_TRANSFER_DENOMINATOR"
            return result
        delta_beta = abs(k_beta) * eta_bound / denominator + abs(epsilon_sn)
    else:
        result["input_status"] = f"UNKNOWN_ROUTE_{route}"
        return result

    result.update(
        {
            "delta_beta_source_abs": f"{delta_beta:.12g}",
            "passes_beta_bound": delta_beta <= beta_limit,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    limit = beta_bound()
    rows = [evaluate_case(row, limit) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def transfer_rows(timestamp: str) -> list[dict[str, Any]]:
    eta_bound = float(get_wep_bound_row()["reported_no_violation_level_abs_eta"])
    return [
        {
            "transfer_id": "WTP3991_0_real_product_bound",
            "source_arena": "WEP_MICROSCOPE_TiPt",
            "target_arena": "source_weight_product",
            "known": f"|Delta_w_TiPt * tau_WEP| <= {eta_bound}",
            "needed_to_invert": "numeric tau_WEP; material/source contrast; sign/no-cancellation convention",
            "status": "REAL_BOUND_ANCHOR_NOT_COUPLING_VALUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "transfer_id": "WTP3991_1_ppn_transfer",
            "source_arena": "WEP_MICROSCOPE_TiPt",
            "target_arena": "PPN_beta_source",
            "known": "eta bound can limit beta source only after K_beta_from_WEP maps the same source-weight basis into the PPN beta slot",
            "needed_to_invert": "same delta_w basis; K_beta_from_WEP; epsilon_SN; PPN source normalization",
            "status": "TRANSFER_BLOCKED_BY_PARENT_PROJECTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "transfer_id": "WTP3991_2_refusal_guard",
            "source_arena": "all",
            "target_arena": "local_GR_claim",
            "known": "an observational small number is not a derivation of source universality",
            "needed_to_invert": "parent no-Hom theorem or complete projection denominator",
            "status": "NO_BOUND_INVERSION_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3991_0",
            "finding": "first real source-weight observable bound anchor exists",
            "evidence": "MICROSCOPE Ti/Pt eta bound imports as |Delta_w_TiPt*tau_WEP| <= eta_bound",
            "limitation": "tau_WEP/material/K projection is missing, so it is not yet an MTS coupling bound",
            "next_action": "derive/source WEP tau denominator and material/source contrast, or parent-sign no-Hom zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3991_1",
            "finding": "PPN beta-source evaluator is executable",
            "evidence": "theorem-zero, WEP-transfer, 3990-envelope, toy numeric, and missing-input branches all run",
            "limitation": "all score-ready branches remain blocked until parent/source rows are real",
            "next_action": "3992 should attack the projection denominator rather than write another abstract target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3991_0_no_WEP_source_weight_claim",
            "claim": "MTS relative source-weight is bounded by MICROSCOPE",
            "allowed": False,
            "reason": "real eta bound exists, but tau_WEP/material/source contrast projection is not derived or sourced",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3991_1_no_PPN_beta_claim",
            "claim": "PPN beta source component passes",
            "allowed": False,
            "reason": "evaluator exists, but score-ready parent inputs/theorem-zero certificate are not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3991_2_no_local_GR_claim",
            "claim": "local GR/Newton calibrated source coupling closes",
            "allowed": False,
            "reason": "product lock, extra monopole, PPN rest, and source-weight projection gates remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3991_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive/source the WEP tau/material/source denominator or parent-sign the no-Hom source-weight zero",
            "success_condition": "MICROSCOPE eta bound becomes a real Delta_w/tau projection row, or no-Hom theorem-zero closes source weights without projection inversion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "REAL_WEP_BOUND_ANCHOR_AND_PPN_BETA_SOURCE_EVALUATOR_READY_NONCLAIM",
            "headline": "the first real source-weight observable bound is imported, and the PPN beta-source evaluator now blocks/pass-tests the correct branches",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    wep = get_wep_bound_row()
    eta_bound = float(wep["reported_no_violation_level_abs_eta"])
    lines = [
        "# 3991 - Source-Weight Real Bound Or PPN Beta-Source Evaluator",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint imports a real observable bound without pretending it is already an MTS coupling bound.",
        "",
        f"The source-backed MICROSCOPE Ti/Pt row gives `|eta_TiPt| <= {eta_bound}`.",
        "",
        "For the source-weight branch the honest statement is:",
        "",
        "`|P_WEP_source_weight| = |Delta_w_TiPt * tau_WEP| <= eta_bound_abs`.",
        "",
        "That is real evidence, but it is only a product anchor until the parent `tau_WEP`, material/source contrast, and readout kernel are derived or sourced.",
        "",
        "## PPN Beta Evaluator",
        "",
        "The evaluator now covers three branches:",
        "",
        "- theorem-zero branch: `B_source=A_source^2` gives `delta_beta_source=0` conditionally;",
        "- 3990 envelope branch: `delta_beta_source_abs <= |R_matter_descent| + epsilon_no_hom + epsilon_action_line + epsilon_readout + |epsilon_SN|`;",
        "- WEP transfer branch: `delta_beta_source_abs <= |K_beta_from_WEP| eta_bound / |tau_WEP material_contrast| + |epsilon_SN|`.",
        "",
        "The real WEP branch correctly blocks because the transfer denominator is missing. The toy WEP projection passes only as a unit test, not as evidence.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, delta_beta `{row['delta_beta_source_abs']}`, passes={row['passes_beta_bound']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Current Residual Meaning",
            "",
            "The source-coupling gap has been narrowed again: it is now specifically the projection denominator from a real WEP observable into the MTS source-weight basis, or else the parent no-Hom theorem-zero.",
            "",
            "## Source Register",
            "",
            f"`{found}/{len(sources)}` source needles found.",
        ]
    )
    for row in sources:
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        )
    lines.extend(
        [
            "",
            "## Next Target",
            "",
            f"`{NEXT_DOC}`",
            "",
            "Derive/source the `tau_WEP` denominator and material/source contrast, or parent-sign the no-Hom zero directly.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def update_spine(timestamp: str) -> None:
    header = "## 3991 - Real WEP Anchor And Beta-Source Evaluator"
    block = "\n".join(
        [
            "",
            header,
            "",
            f"- Timestamp: `{timestamp}`",
            "- Status: `REAL_WEP_BOUND_ANCHOR_AND_PPN_BETA_SOURCE_EVALUATOR_READY_NONCLAIM`",
            "- Main progress:",
            "  the MICROSCOPE Ti/Pt bound is now imported as a real source-weight product anchor: `|Delta_w_TiPt * tau_WEP| <= eta_bound_abs`.",
            "- Important refusal:",
            "  this is not yet an MTS coupling bound because `tau_WEP`, material/source contrast, and `K_beta_from_WEP` are not derived/sourced.",
            "- PPN evaluator:",
            "  supports theorem-zero, 3990 no-Hom envelope, WEP-transfer, toy projection, and missing-parent block branches.",
            "- Current bottleneck:",
            "  derive/source the WEP projection denominator or parent-sign the no-Hom source-weight zero.",
            f"- Next: `{NEXT_DOC}`.",
            "",
        ]
    )
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if header not in existing:
        SPINE_PATH.write_text(existing.rstrip() + block, encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL3991_00_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3991_01_needles_found", all(row["needle_found"] for row in sources), "every cited source needle found")
    wep_anchor = next(row for row in anchors if row["anchor_id"] == "ANCH3991_0_WEP_MICROSCOPE_product")
    add("VAL3991_02_wep_anchor_positive", float(wep_anchor["real_observable_bound"]) > 0.0, "WEP anchor bound is positive numeric")
    add("VAL3991_03_wep_source_recorded", bool(wep_anchor["source_url"]) and bool(wep_anchor["source_doi"]), "WEP source URL/DOI recorded")
    add("VAL3991_04_anchor_nonclaim", not any(str(row["valid_for_claim"]).lower() == "true" for row in anchors), "anchors remain nonclaim")
    add("VAL3991_05_cases_written", len(cases) >= 5, "evaluator cases written")
    theorem = next(row for row in results if row["case_id"] == "CASE3991_0_parent_theorem_zero")
    real_wep = next(row for row in results if row["case_id"] == "CASE3991_1_real_WEP_anchor_projection_blocked")
    toy = next(row for row in results if row["case_id"] == "CASE3991_2_WEP_transfer_toy_projection")
    envelope = next(row for row in results if row["case_id"] == "CASE3991_3_3990_small_envelope_smoke")
    missing = next(row for row in results if row["case_id"] == "CASE3991_4_missing_parent_rows")
    add("VAL3991_06_theorem_zero_passes", float(theorem["delta_beta_source_abs"]) == 0.0 and str(theorem["passes_beta_bound"]).lower() == "true", "conditional theorem-zero branch passes smoke")
    add("VAL3991_07_real_wep_blocks", real_wep["input_status"] == "REAL_WEP_BOUND_PRESENT_TRANSFER_DENOMINATOR_MISSING", "real WEP anchor blocks without projection denominator")
    add("VAL3991_08_toy_wep_passes_nonclaim", str(toy["passes_beta_bound"]).lower() == "true" and str(toy["valid_for_claim"]).lower() == "false", "toy WEP projection passes only as nonclaim")
    add("VAL3991_09_envelope_passes_nonclaim", str(envelope["passes_beta_bound"]).lower() == "true" and str(envelope["valid_for_claim"]).lower() == "false", "3990 envelope smoke passes only as nonclaim")
    add("VAL3991_10_missing_blocks", missing["input_status"] == "MISSING_3990_ENVELOPE_INPUT" and str(missing["passes_beta_bound"]).lower() == "false", "missing parent rows block")
    add("VAL3991_11_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3991_12_transfer_guard", "NO_BOUND_INVERSION_GUARD_ACTIVE" in read_text(OUTPUTS["transfer"]), "bound inversion guard active")
    add("VAL3991_13_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3991_14_doc_exists", DOC_PATH.exists() and "Delta_w_TiPt * tau_WEP" in read_text(DOC_PATH), "document written")
    add("VAL3991_15_spine_updated", SPINE_PATH.exists() and "## 3991 - Real WEP Anchor And Beta-Source Evaluator" in read_text(SPINE_PATH), "spine updated")
    add("VAL3991_16_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3991_17_compile", compile_ok, "script compiles")
    add("VAL3991_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3991_19_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3991_20_results_nonclaim", not any(str(row["valid_for_claim"]).lower() == "true" for row in results), "all evaluator results remain nonclaim")
    return rows


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    anchors = anchor_rows(timestamp)
    schema = schema_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    transfer = transfer_rows(timestamp)
    decision = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["anchors"], anchors)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["transfer"], transfer)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    update_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validation = build_validation_rows(timestamp, sources, anchors, cases, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if str(row["passed"]).lower() != "true"]
    print(f"3991 validation: {len(validation) - len(failed)}/{len(validation)} passed")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
