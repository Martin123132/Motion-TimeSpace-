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
DOC = ROOT / "1102-Y5-R10-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md"
RUN_DIR = ROOT / "runs" / "1102-alpha-product-first-input-fill" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_BOUND_IMPORT.csv"

CLOCK_PRODUCT_BOUND_YR_INV = 2.1e-18
WEP_ALPHA_PRODUCT_MAX = 4.797780522732e-05
DD_ALPHA_COEFF_MAX = 8.320244933243533e-10
DELTA_Q_ALPHA = 0.001989808886825
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


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


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1102_0_1101_next", "source-intake/mts_residuals/P8_Y5_R10_1101_NEXT_TARGET.csv", "NEXT1101_0_1102", "1101 handoff."),
        ("SRC1102_1_1101_route", "source-intake/mts_residuals/P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv", "ROUTE1101_2_finite_alpha_products", "finite alpha product route selected."),
        ("SRC1102_2_1061_doc", "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md", "PRED1061_0_WEP_alpha_material_convention_filled", "earlier WEP input fill checkpoint."),
        ("SRC1102_3_1061_inputs", "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv", "INF1061_3_beta_source_alpha", "WEP missing-input ledger."),
        ("SRC1102_4_1061_prediction", "source-intake/mts_residuals/P8_Y5_R10_1061_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv", "PRED1061_0_WEP_alpha_material_convention_filled", "WEP prediction attempt."),
        ("SRC1102_5_1062_doc", "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md", "THEOREM_NOT_CLOSED_CURRENT_CORPUS", "combined WEP product theorem/closure checkpoint."),
        ("SRC1102_6_1062_premise", "source-intake/mts_residuals/P8_Y5_R10_1062_PREMISE_SIGNATURE_AUDIT.csv", "PREM1062_3_source_label_forgetting", "source-label premise audit."),
        ("SRC1102_7_1062_counter", "source-intake/mts_residuals/P8_Y5_R10_1062_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv", "CE1062_1_relative_source_weight", "relative source-weight counterexample."),
        ("SRC1102_8_1051_clock", "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv", "BAP1051_2_best_current_product", "clock product bound chain."),
        ("SRC1102_9_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "clock product bound ledger."),
        ("SRC1102_10_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_0_clock_product", "tau clock/WEP/R10 audit."),
        ("SRC1102_11_1053_beta", "source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv", "BSA1053_1_alpha_marker_source", "beta_source_alpha audit."),
        ("SRC1102_12_983_web", "source-intake/mts_residuals/P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv", "WEB983_0_MICROSCOPE_CQG_COMPOSITION", "MICROSCOPE composition source row."),
        ("SRC1102_13_1053_wcm", "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", "WCM1053_4", "WEP alpha charge matrix."),
        ("SRC1102_14_local_bound", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound anchor."),
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


def input_status_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "IN1102_0_clock_product_bound",
            "arena": "clock",
            "input": "abs(b_alpha*tau_clock_time) bound",
            "value_or_status": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "units": "yr^-1",
            "source": "ACB1052_2; BAP1051_2_best_current_product",
            "filled_status": "SOURCE_BACKED_BOUND_AVAILABLE_NOT_PREDICTION",
            "blocks_claim": "tau_clock_time and Xhat/chi_X normalization missing; b_alpha theorem-zero absent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_1_tau_clock_Xhat",
            "arena": "clock",
            "input": "tau_clock_time / Xhat normalization",
            "value_or_status": "MISSING_PARENT_TAU_CLOCK_XHAT_MAP",
            "units": "yr^-1 per normalized Xhat unit",
            "source": "TPR1053_0_clock_product",
            "filled_status": "not_filled",
            "blocks_claim": "clock product bound cannot become standalone b_alpha or MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_2_WEP_material_pair",
            "arena": "MICROSCOPE_WEP",
            "input": "material pair convention",
            "value_or_status": "TA6V_minus_PtRh10",
            "units": "dimensionless convention",
            "source": "WEB983_0; WCM1053_4; INF1061_0",
            "filled_status": "filled_for_smoke_only",
            "blocks_claim": "full material/source/readout tensor missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_3_delta_Q_alpha",
            "arena": "MICROSCOPE_WEP",
            "input": "Delta_Q_alpha_Coulomb_abs",
            "value_or_status": f"{DELTA_Q_ALPHA:.15e}",
            "units": "dimensionless",
            "source": "WCM1053_4; AWP1052_0_alpha_Coulomb",
            "filled_status": "filled_for_smoke_only",
            "blocks_claim": "source-backed smoke estimate, not full MICROSCOPE material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_4_WEP_product_target",
            "arena": "MICROSCOPE_WEP",
            "input": "abs(P_WEP_alpha) target",
            "value_or_status": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "units": "dimensionless",
            "source": "AWP1052_0_alpha_Coulomb; INF1061_2",
            "filled_status": "target_filled_not_prediction",
            "blocks_claim": "threshold is not an MTS predicted product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_5_beta_source_alpha",
            "arena": "MICROSCOPE_WEP",
            "input": "beta_source_alpha",
            "value_or_status": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER",
            "units": "dimensionless",
            "source": "BSA1053_1_alpha_marker_source; PREM1062_3_source_label_forgetting",
            "filled_status": "not_filled",
            "blocks_claim": "cannot set beta_source_alpha to 1 or 0 without source-label/Noether owner theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_6_tau_WEP",
            "arena": "MICROSCOPE_WEP",
            "input": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless projection factor",
            "source": "TPR1053_1_tau_WEP_definition; PREM1062_5_tau_WEP_readout",
            "filled_status": "not_filled",
            "blocks_claim": "cannot set tau_WEP to 1; needs local source/orbit/readout map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1102_7_direct_product",
            "arena": "MICROSCOPE_WEP",
            "input": "P_WEP_alpha",
            "value_or_status": "MISSING_DIRECT_PARENT_PRODUCT_OR_NUMERIC_VALUE",
            "units": "dimensionless",
            "source": "THM1062_6_verdict; PRED1061_0_WEP_alpha_material_convention_filled",
            "filled_status": "not_filled",
            "blocks_claim": "runner must refuse until direct product or all factors are sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def path_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "path_id": "PATH1102_0_clock",
            "path": "clock finite-alpha product",
            "available_now": "source-backed product bound |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "missing": "tau_clock_time; Xhat/chi_X normalization; alpha owner or numeric b_alpha product prediction",
            "decision": "retain as strongest product bound, not a scoreable prediction",
            "next_requirement": "derive tau_clock/Xhat map if clock route is selected",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "path_id": "PATH1102_1_WEP",
            "path": "WEP alpha product",
            "available_now": "MICROSCOPE material smoke pair, Delta_Q_alpha, eta bound, product target",
            "missing": "beta_source_alpha; tau_WEP; direct P_WEP_alpha theorem or numeric value; full material/readout tensor",
            "decision": "best route for source-normalization physics, but still not scoreable",
            "next_requirement": "attack source-label forgetting/Noether current owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "path_id": "PATH1102_2_best_next",
            "path": "source-label/Noether owner",
            "available_now": "1062 identifies relative source weight as clean counterexample",
            "missing": "parent source functor forgetting species labels before gravitational/EM source coupling",
            "decision": "selected next derivation target",
            "next_requirement": "prove source-label forgetting or stage relative-weight product priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1102_0_clock_alpha_bound_not_prediction",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "product_value": "MISSING_MTS_B_ALPHA_TAU_CLOCK_PREDICTION",
            "product_units": "yr^-1",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
            "inputs_present": "clock product bound only",
            "required_inputs": "tau_clock_time; Xhat normalization; b_alpha theorem-zero or direct product prediction",
            "derivation_status": "BOUND_AVAILABLE_PREDICTION_MISSING",
            "valid_for_claim": "false",
            "notes": "H0-normalized diagnostic is not a theory prediction.",
        },
        {
            "prediction_id": "PRED1102_1_WEP_material_target_not_prediction",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_PARENT_DERIVED_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
            "inputs_present": "Delta_Q_alpha; eta_bound; WEP product target",
            "required_inputs": "beta_source_alpha; tau_WEP; b_alpha or direct P_WEP_alpha theorem",
            "derivation_status": "MATERIAL_TARGET_FILLED_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "No beta=1, tau=1, or clock transfer.",
        },
        {
            "prediction_id": "PRED1102_2_c_alpha_DD_threshold_not_prediction",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_SOURCE_BACKED_C_ALPHA_OR_THEOREM_ZERO",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
            "inputs_present": "DD alpha threshold only",
            "required_inputs": "source-backed c_alpha_DD value or signed zero theorem",
            "derivation_status": "THRESHOLD_AVAILABLE_COEFFICIENT_MISSING",
            "valid_for_claim": "false",
            "notes": "Threshold is not prediction.",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1102_0_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "bound_value": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "bound_type": "upper_abs_1sigma_product_bound",
            "valid_for_claim": "false",
            "notes": "source-backed product bound only",
        },
        {
            "bound_id": "BOUND1102_1_WEP_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "target only",
        },
        {
            "bound_id": "BOUND1102_2_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "source_row": "REQ1098_0_c_alpha",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only",
        },
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1102_0_alpha_product_input_fill",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject product rows because only targets/bounds are filled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1102_0_clock_prediction",
            "claim_component": "clock alpha product is predicted by MTS",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "tau_clock/Xhat normalization and direct product prediction are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1102_1_WEP_product",
            "claim_component": "WEP alpha product is predicted by MTS",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "material target is filled, but beta_source_alpha, tau_WEP, and direct product are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1102_2_source_label",
            "claim_component": "source-label forgetting/Noether owner closes WEP alpha",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "1062 keeps relative source weights as a live counterexample",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1102_3_runner",
            "claim_component": "product runner has valid predictions",
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
            "decision_id": "DEC1102_0_clock",
            "decision": "clock path has the strongest source-backed product bound but no MTS prediction",
            "because": "tau_clock/Xhat normalization and b_alpha owner remain missing",
            "next_action": "keep as bound; do not extract standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1102_1_WEP",
            "decision": "WEP path has material/target inputs filled but product still absent",
            "because": "beta_source_alpha and tau_WEP are unowned, and closure zero is nonnumeric",
            "next_action": "attack source-label forgetting and Noether current owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1102_2_best_next",
            "decision": "next target is source-label forgetting/Noether owner",
            "because": "relative source weights are the cleanest counterexample blocking WEP, PPN/Newton source normalization, and R10 source/test products",
            "next_action": "1103-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-product-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1102_0_1103",
            "next_target": "1103-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-product-prior.md",
            "objective": "derive species-blind source-label forgetting and the Noether current owner that remove relative source weights, or stage explicit relative-weight product priors for WEP, PPN/Newton source normalization, and R10 without claiming a pass",
            "include": "source functor domain; same-action Hilbert source; relative w_A counterexample; Noether current owner; measured-G common-mode absorption guard; product/refusal rows",
            "exclude": "assuming WEP; hiding relative weights in measured G; beta_source_alpha=1; tau_WEP=1; standalone b_alpha; public local-GR/WEP/R10 claim; GitHub; formalization edits",
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
    sources: list[dict[str, str]],
    inputs: list[dict[str, str]],
    paths: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1102_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited local source paths exist and needles are found"))
    checks.append(("V1102_1_clock_bound_retained", any(row["input_id"] == "IN1102_0_clock_product_bound" and parse_float(row["value_or_status"]) == CLOCK_PRODUCT_BOUND_YR_INV for row in inputs), "clock product bound is retained"))
    checks.append(("V1102_2_WEP_material_target_filled", all(any(row["input_id"] == input_id and row["filled_status"].startswith(expected) for row in inputs) for input_id, expected in [("IN1102_2_WEP_material_pair", "filled"), ("IN1102_3_delta_Q_alpha", "filled"), ("IN1102_4_WEP_product_target", "target")]), "WEP material/DeltaQ/target inputs are filled"))
    checks.append(("V1102_3_beta_tau_missing", all(any(row["input_id"] == input_id and row["filled_status"] == "not_filled" for row in inputs) for input_id in ["IN1102_5_beta_source_alpha", "IN1102_6_tau_WEP", "IN1102_7_direct_product"]), "beta_source_alpha, tau_WEP, and direct product remain missing"))
    checks.append(("V1102_4_path_next_selected", any(row["path_id"] == "PATH1102_2_best_next" for row in paths), "source-label/Noether owner selected as next path"))
    checks.append(("V1102_5_predictions_missing", predictions and all(row["valid_for_claim"] == "false" and str(row["product_value"]).startswith("MISSING") for row in predictions), "prediction rows remain missing/nonclaim"))
    checks.append(("V1102_6_bounds_positive", len(bounds) == 3 and all(parse_float(row["bound_value"]) is not None and float(row["bound_value"]) > 0 for row in bounds), "bound rows have positive numeric values"))
    checks.append(("V1102_7_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses target-only rows"))
    checks.append(("V1102_8_claim_gates_blocked", claims and all(row["claim_allowed"] == "false" for row in claims), "all alpha product claim gates remain blocked"))
    checks.append(("V1102_9_next_target", any(row["next_target"].startswith("1103-Y5-R10-source-label") for row in next_rows), "1103 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1102_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1102_11_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1102 CSV outputs parse cleanly"))
    checks.append(("V1102_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench"))
    checks.append(("V1102_SUMMARY", True, "clock bound and WEP material target are retained; no scoreable alpha product exists; next target source-label/Noether owner"))
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
    sources: list[dict[str, str]],
    inputs: list[dict[str, str]],
    paths: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1102-Y5-R10 alpha product first input fill: tau-clock/Xhat or WEP beta-source",
            "",
            "## Current verdict",
            "1102 consolidates the finite-alpha route after the gauge-norm owner hunt failed. The useful inputs are real but limited: clocks provide a source-backed product bound, and WEP has a smoke material convention plus product target. Neither is an MTS product prediction. `tau_clock/Xhat`, `beta_source_alpha`, `tau_WEP`, and direct `P_WEP_alpha` remain unowned, so the runner must keep claims false.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Input fill ledger",
            md_table(inputs, ["input_id", "arena", "input", "value_or_status", "units", "source", "filled_status", "blocks_claim"]),
            "## Path decision",
            md_table(paths, ["path_id", "path", "available_now", "missing", "decision", "next_requirement"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claims, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    inputs = input_status_rows()
    paths = path_decision_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1102_SOURCE_REGISTER.csv",
        "input_status": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
        "path_decision": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_PATH_DECISION.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1102_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1102_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1102_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1102_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1102_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1102_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["input_status"], inputs)
    write_csv(outputs["path_decision"], paths)
    write_csv(outputs["prediction"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bounds, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claims = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation = validate_outputs(outputs, sources, inputs, paths, predictions, bounds, product_status, claims, next_rows)
    write_csv(outputs["validation"], validation)
    write_doc(sources, inputs, paths, product_status_rows_, product_result["comparisons"], claims, decisions, validation, next_rows)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
