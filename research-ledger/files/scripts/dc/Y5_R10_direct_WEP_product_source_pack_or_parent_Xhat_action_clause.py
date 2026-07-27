from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1094-Y5-R10-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1094-direct-WEP-product-source-pack" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15
DELTA_Q_ALPHA = 1.989808886825e-03
UNIT_SOURCE_ETA_PREDICTION = 5.836031862511e-11
DIRECT_PRODUCT_BOUND = ETA_BOUND / UNIT_SOURCE_ETA_PREDICTION


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1094_0_1093_next", "source-intake/mts_residuals/P8_Y5_R10_1093_NEXT_TARGET.csv", "NEXT1093_0_1094", "1093 handoff."),
        ("SRC1094_1_1093_projection", "source-intake/mts_residuals/P8_Y5_R10_1093_BALPHA_TAU_PROJECTION_SOURCE_LEDGER.csv", "PS1093_1_tau_WEP", "projection source status."),
        ("SRC1094_2_1061_product", "source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_0_product_definition", "direct P_WEP product definition."),
        ("SRC1094_3_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_3_screened_product_target", "WEP alpha material convention and product threshold."),
        ("SRC1094_4_1067_tau_functional", "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv", "TWF1067_6_verdict", "tau_WEP functional decomposition."),
        ("SRC1094_5_1068_pack", "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv", "TAP1068_6_direct_product_fallback", "direct product acquisition pack."),
        ("SRC1094_6_1069_real_source", "source-intake/mts_residuals/P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv", "WTS1069_0_MICROSCOPE_eta_source_charge_proxy", "first real WEP source/readout row."),
        ("SRC1094_7_1072_tau_status", "source-intake/mts_residuals/P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv", "NTS1072_2_tau_WEP", "numeric tau status."),
        ("SRC1094_8_1052_alpha_wep", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "alpha WEP pressure ledger."),
        ("SRC1094_9_988_wep_alpha", "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "unit source eta prediction and threshold."),
        ("SRC1094_10_651_DD", "source-intake/mts_residuals/P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv", "Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb", "Damour-Donoghue smoke material charge estimate."),
        ("SRC1094_11_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE bound anchor."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def direct_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "DWP1094_0_observable",
            "object": "MICROSCOPE eta_AB",
            "definition": "eta_AB is the observed differential acceleration bound for Ti/Pt in the selected frame",
            "numeric_value": f"{ETA_BOUND:.12e}",
            "units": "dimensionless",
            "status": "SOURCE_BACKED_BOUND_ANCHOR",
            "claim_policy": "bound anchor only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "DWP1094_1_material_delta",
            "object": "Delta_Q_alpha_Coulomb_abs",
            "definition": "absolute TA6V minus PtRh10 alpha/Coulomb material charge in the smoke Damour-Donoghue convention",
            "numeric_value": f"{DELTA_Q_ALPHA:.12e}",
            "units": "dimensionless",
            "status": "SOURCE_BACKED_SMOKE_CONVENTION",
            "claim_policy": "not full material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "DWP1094_2_unit_source",
            "object": "unit_source_eta_prediction",
            "definition": "eta predicted by unit alpha/source normalization in the 1052/988 alpha-Coulomb convention",
            "numeric_value": f"{UNIT_SOURCE_ETA_PREDICTION:.12e}",
            "units": "dimensionless",
            "status": "SOURCE_BACKED_SMOKE_CONVENTION",
            "claim_policy": "threshold only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "DWP1094_3_direct_product_bound",
            "object": "P_WEP_alpha_direct",
            "definition": "abs(P_WEP_alpha_direct) <= eta_bound / unit_source_eta_prediction",
            "numeric_value": f"{DIRECT_PRODUCT_BOUND:.12e}",
            "units": "dimensionless",
            "status": "NUMERIC_SCORE_THRESHOLD_NONCLAIM",
            "claim_policy": "usable as private product threshold; no MTS prediction yet",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "DWP1094_4_required_prediction",
            "object": "MTS P_WEP_alpha_direct",
            "definition": "single parent-projected alpha/source product mapping MTS local scalar response to the MICROSCOPE observable",
            "numeric_value": "MISSING_MTS_DIRECT_PRODUCT",
            "units": "dimensionless",
            "status": "MISSING_DIRECT_PRODUCT",
            "claim_policy": "runner must refuse until sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_context_rows() -> list[dict[str, str]]:
    return [
        {
            "context_id": "CTX1094_0_bound_readout",
            "component": "eta_AB readout",
            "current_evidence": "WTS1069_0 and R1_WEP_source_charge give eta upper bound 2.8e-15",
            "current_status": "BOUND_ANCHOR_PRESENT",
            "blocks_score": "false",
            "needed_to_promote": "full sign/frame/readout convention if public claim is attempted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "context_id": "CTX1094_1_material_response",
            "component": "Ti/Pt alpha material delta",
            "current_evidence": "MCON1061_1 and Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb",
            "current_status": "SMOKE_DELTA_PRESENT",
            "blocks_score": "partly",
            "needed_to_promote": "full material tensor or theorem reducing to the DD smoke convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "context_id": "CTX1094_2_source_worldtube",
            "component": "Earth/source worldtube",
            "current_evidence": "TAP1068_0 and TWF1067_1",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "blocks_score": "true",
            "needed_to_promote": "source stress/profile/composition convention in observed local frame",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "context_id": "CTX1094_3_orbit_readout",
            "component": "MICROSCOPE orbit/readout map",
            "current_evidence": "TAP1068_1, TAP1068_4, and NTS1072_2",
            "current_status": "MISSING_NUMERIC_KERNEL",
            "blocks_score": "true",
            "needed_to_promote": "orbit/attitude/readout averaging kernel or direct observable theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "context_id": "CTX1094_4_Xhat_normalization",
            "component": "parent Xhat normalization",
            "current_evidence": "TWF1067_5 and TAP1068_5",
            "current_status": "MISSING_XHAT_NORMALIZATION",
            "blocks_score": "true",
            "needed_to_promote": "shared parent normalization or explicitly separate finite-branch convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_action_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PX1094_0_field_owner",
            "future_parent_action_clause": "S_parent contains a normalized scalar/vertical mode Xhat with a declared quotient role",
            "must_satisfy": "Xhat is not merely chi_X closure notation; it is the field varied in the parent action",
            "current_status": "NOT_SIGNED",
            "if_signed": "connects nohair operator and WEP product to one owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PX1094_1_matter_response",
            "future_parent_action_clause": "ordinary matter response gives either delta_X S_matter=0 or a finite observable product P_WEP_alpha_direct",
            "must_satisfy": "no hidden split into beta_source_alpha, tau_WEP, or material tensor unless each factor is sourced",
            "current_status": "NOT_SIGNED",
            "if_signed": "turns WEP branch into theorem-zero or scoreable finite product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PX1094_2_no_rescale_cheat",
            "future_parent_action_clause": "measured G/calibration cannot absorb relative source-weight or material-dependent residuals",
            "must_satisfy": "same observed-frame force map is used for GR baseline and MTS residual",
            "current_status": "POLICY_WRITTEN_NOT_PARENT_SIGNED",
            "if_signed": "protects WEP comparison from cancellation/rescaling objections",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PX1094_3_verdict",
            "future_parent_action_clause": "parent Xhat action clause sufficient for WEP scoring",
            "must_satisfy": "field owner + matter response + readout/frame + no-rescale rule",
            "current_status": "PARENT_ACTION_CLAUSE_NOT_DERIVED",
            "if_signed": "1094 direct product can become a real prediction row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1094_0_missing_direct_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha_direct",
            "product_value": "MISSING_MTS_DIRECT_PRODUCT_FROM_PARENT_ACTION",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
            "inputs_present": "eta bound; DD smoke material delta; unit-source threshold",
            "required_inputs": "parent Xhat action clause or source-backed numeric direct P_WEP_alpha_direct row",
            "derivation_status": "MISSING_SCOREABLE_MTS_PRODUCT",
            "valid_for_claim": "false",
            "notes": "do not divide clock product by guessed tau; do not set tau_WEP to one",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1094_0_direct_WEP_alpha_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha_direct",
            "bound_value": f"{DIRECT_PRODUCT_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "source_row": "MCON1061_3_screened_product_target",
            "bound_type": "absolute_direct_product_upper_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "private score threshold from eta bound divided by unit-source smoke convention; not a full material-tensor public claim",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1094_0_direct_WEP_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "threshold is numeric but MTS direct product is missing, so claim remains false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1094_0_threshold",
            "claim_component": "direct WEP threshold exists",
            "gate_pass": "true_nonclaim_only",
            "claim_allowed": "false",
            "reason": f"P_WEP_alpha_direct threshold is {DIRECT_PRODUCT_BOUND:.12e} but is smoke-threshold only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1094_1_prediction",
            "claim_component": "MTS direct WEP product exists",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PRED1094_0_missing_direct_WEP_product has no numeric product_value",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1094_2_parent_clause",
            "claim_component": "parent Xhat action clause signs the WEP product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PX1094_3_verdict=PARENT_ACTION_CLAUSE_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1094_3_product_runner",
            "claim_component": "direct WEP product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1094_0_scoreboard_improved",
            "decision": "direct WEP alpha threshold is now explicit",
            "because": "eta bound and unit-source smoke convention give P_WEP_alpha_direct <= 4.7978e-05",
            "next_action": "do not claim; use threshold only when a real MTS product row exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1094_1_prediction_missing",
            "decision": "MTS still lacks the direct WEP product prediction",
            "because": "parent Xhat action/matter response clause is not derived and numeric tau/source kernel is not acquired",
            "next_action": "derive parent action clause or source a direct numeric product row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1094_2_best_next",
            "decision": "attempt the parent action clause before more data scraping",
            "because": "without a product owner, extra MICROSCOPE files only improve the bound side, not the MTS prediction side",
            "next_action": "1095-Y5-R10-parent-Xhat-WEP-product-action-clause-or-direct-product-numeric-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1094_0_1095",
            "next_target": "1095-Y5-R10-parent-Xhat-WEP-product-action-clause-or-direct-product-numeric-row.md",
            "objective": "derive the parent Xhat matter-response clause that yields theorem-zero or a numeric direct P_WEP_alpha product; if it fails, stage the exact source fields needed for a numeric direct row",
            "include": "parent variation of matter/source action; direct P_WEP_alpha formula; observed-frame force/readout map; material convention owner; no measured-G absorption; numeric row refusal gates",
            "exclude": "standalone beta/tau division; tau_WEP=1; clock transfer; cancellation; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1094_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1094_1_threshold_numeric", abs(DIRECT_PRODUCT_BOUND - 4.797780522731929e-05) < 1e-16, "direct WEP threshold computed from eta/unit-source rows"))
    checks.append(("V1094_2_contract_missing_prediction", any(row["contract_id"] == "DWP1094_4_required_prediction" and row["status"] == "MISSING_DIRECT_PRODUCT" for row in contract_rows), "required MTS direct product remains missing"))
    checks.append(("V1094_3_source_context_blocks_score", any(row["blocks_score"] == "true" for row in context_rows), "source context still has score-blocking gaps"))
    checks.append(("V1094_4_parent_clause_not_derived", any(row["clause_id"] == "PX1094_3_verdict" and row["current_status"] == "PARENT_ACTION_CLAUSE_NOT_DERIVED" for row in action_rows), "parent Xhat action clause remains unsigned"))
    checks.append(("V1094_5_prediction_missing_nonclaim", any("MISSING_MTS_DIRECT_PRODUCT" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing and nonclaim"))
    checks.append(("V1094_6_bound_threshold_positive", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0, "direct product bound threshold is positive numeric"))
    checks.append(("V1094_7_bound_nonclaim", bool(bound_rows_) and bound_rows_[0]["valid_for_claim"] == "false", "direct product threshold is explicitly nonclaim"))
    checks.append(("V1094_8_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1094_9_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local claim"))
    checks.append(("V1094_10_next_target", any(row["next_target"].startswith("1095-Y5-R10-parent-Xhat-WEP-product") for row in next_rows), "1095 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1094_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1094_12_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1094 CSV outputs parse cleanly"))
    checks.append(("V1094_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1094_SUMMARY", True, "direct WEP threshold exists; MTS direct product and parent action clause remain missing; claim blocked"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1094-Y5-R10 direct WEP product source pack or parent Xhat action clause",
            "",
            "## Current verdict",
            "1094 improves the WEP scoreboard but does not create a claim. The direct alpha/WEP product threshold is now explicit: in the current smoke material convention, `|P_WEP_alpha_direct| <= 4.797780522732e-05`. That avoids fake factor splitting into standalone `beta_source_alpha` and `tau_WEP`. However, the MTS prediction side is still missing: no parent Xhat action clause yet gives a numeric direct product or theorem-zero. Product runner refusal is therefore the correct result.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Direct WEP product contract",
            md_table(contract_rows, ["contract_id", "object", "definition", "numeric_value", "units", "status", "claim_policy"]),
            "## WEP source context ledger",
            md_table(context_rows, ["context_id", "component", "current_evidence", "current_status", "blocks_score", "needed_to_promote"]),
            "## Parent Xhat action clause attempt",
            md_table(action_rows, ["clause_id", "future_parent_action_clause", "must_satisfy", "current_status", "if_signed"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    contract_rows = direct_contract_rows()
    context_rows = source_context_rows()
    action_rows = parent_action_clause_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1094_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
        "context": OUT / "P8_Y5_R10_1094_WEP_SOURCE_CONTEXT_LEDGER.csv",
        "parent_action": OUT / "P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1094_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1094_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1094_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1094_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1094_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1094_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["contract"], contract_rows)
    write_csv(outputs["context"], context_rows)
    write_csv(outputs["parent_action"], action_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        contract_rows,
        context_rows,
        action_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        contract_rows,
        context_rows,
        action_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
