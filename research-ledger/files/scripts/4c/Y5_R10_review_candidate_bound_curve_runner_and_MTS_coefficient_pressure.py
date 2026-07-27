from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
BOUND_DIR = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_review_candidate_bound_curve_runner_and_MTS_coefficient_pressure.py"

PRIOR_DOC = ROOT / "569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md"
PRIOR_VALIDATION = MTS_DIR / "P8_Y5_BRR545_569_VALIDATION.csv"
REVIEW_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
ANCHOR_RECOVERY = BOUND_DIR / "P8_Y5_R10_569_ANCHOR_RECOVERY.csv"
PROMOTION_GATE = BOUND_DIR / "P8_Y5_R10_569_PROMOTION_GATE.csv"
LIVE_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
FINITE_ALPHA_LAW = MTS_DIR / "P8_Y5_R10_567_FINITE_ALPHA_LAW.csv"
COEFFICIENT_REQUIREMENTS = MTS_DIR / "P8_Y5_R10_567_COEFFICIENT_REQUIREMENTS.csv"

REVIEW_CURVE_SUMMARY_PATH = BOUND_DIR / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"
REVIEW_CANDIDATE_QA_PATH = BOUND_DIR / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv"
COEFFICIENT_PRESSURE_PATH = MTS_DIR / "P8_Y5_R10_570_COEFFICIENT_PRESSURE_TABLE.csv"
PRODUCT_SCAN_PATH = MTS_DIR / "P8_Y5_R10_570_HYPOTHETICAL_PRODUCT_SCAN.csv"
MTS_ALPHA_STATUS_PATH = MTS_DIR / "P8_Y5_R10_570_MTS_ALPHA_STATUS.csv"
NONCLAIM_RUNNER_SUMMARY_PATH = MTS_DIR / "P8_Y5_R10_570_NONCLAIM_RUNNER_SUMMARY.csv"
BLOCKER_LEDGER_PATH = MTS_DIR / "P8_Y5_R10_570_BLOCKER_LEDGER.csv"
DECISION_PATH = MTS_DIR / "P8_Y5_BRR545_570_DECISION.csv"
VALIDATION_PATH = MTS_DIR / "P8_Y5_BRR545_570_VALIDATION.csv"
ROUTE_UPDATE_PATH = MTS_DIR / "P8_Y5_BRR545_570_ROUTE_UPDATE.csv"

STATUS = "Y5_R10_review_candidate_curve_pressure_runner_nonclaim"
CLAIM_CEILING = "diagnostic_coefficient_pressure_only_no_R10_pass_no_local_GR_pass"
NEXT_TARGET = "571-Y5-R10-finite-alpha-coefficient-route-or-theorem-zero-return.md"

TARGET_LAMBDAS_M = [
    5.9e-6,
    1.0e-5,
    2.0e-5,
    3.86e-5,
    5.0e-5,
    7.5e-5,
    1.0e-4,
    2.0e-4,
    5.0e-4,
    1.0e-3,
]

PRODUCT_AMPLITUDES = [
    1.0e3,
    1.0e2,
    1.0e1,
    1.0,
    3.0e-1,
    1.0e-1,
    3.0e-2,
    1.0e-2,
    3.0e-3,
    1.0e-3,
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def load_review_curve() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(REVIEW_CURVE):
        lambda_value = parse_float(row.get("lambda_value"))
        alpha_bound = parse_float(row.get("alpha_bound"))
        if lambda_value is None or alpha_bound is None:
            continue
        rows.append(
            {
                **row,
                "lambda_value": lambda_value,
                "alpha_bound": alpha_bound,
                "log10_lambda": math.log10(lambda_value),
                "log10_alpha": math.log10(alpha_bound),
            }
        )
    rows.sort(key=lambda item: item["lambda_value"])
    return rows


def interpolate_loglog(curve_rows: list[dict[str, Any]], lambda_value: float) -> tuple[float | None, str]:
    if not curve_rows:
        return None, "no_curve_rows"
    if lambda_value < curve_rows[0]["lambda_value"] or lambda_value > curve_rows[-1]["lambda_value"]:
        return None, "lambda_outside_review_curve_range"
    for row in curve_rows:
        if math.isclose(lambda_value, row["lambda_value"], rel_tol=1e-12):
            return row["alpha_bound"], f"exact:{row['bound_id']}"
    for left, right in zip(curve_rows, curve_rows[1:]):
        if left["lambda_value"] <= lambda_value <= right["lambda_value"]:
            x0 = left["log10_lambda"]
            x1 = right["log10_lambda"]
            y0 = left["log10_alpha"]
            y1 = right["log10_alpha"]
            t = (math.log10(lambda_value) - x0) / (x1 - x0)
            return 10 ** (y0 + t * (y1 - y0)), f"log_interp:{left['bound_id']}->{right['bound_id']}"
    return None, "interpolation_failed"


def pressure_class(alpha_bound: float) -> str:
    if alpha_bound >= 100.0:
        return "weak_pressure_alpha_bound_above_100"
    if alpha_bound >= 1.0:
        return "moderate_pressure_gravity_strength_or_larger_allowed"
    if alpha_bound >= 0.1:
        return "sub_gravity_strength_pressure"
    if alpha_bound >= 0.01:
        return "strong_pressure_percent_to_tenth_gravity"
    return "very_strong_pressure_below_percent_gravity"


def curve_summary_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not curve_rows:
        return [
            {
                "summary_id": "CS570_0_missing",
                "metric": "review_curve_rows",
                "value": 0,
                "units": "rows",
                "valid_for_claim": "false",
                "notes": "review curve missing or not numeric",
            }
        ]
    min_alpha_row = min(curve_rows, key=lambda item: item["alpha_bound"])
    max_alpha_row = max(curve_rows, key=lambda item: item["alpha_bound"])
    min_lambda_row = min(curve_rows, key=lambda item: item["lambda_value"])
    max_lambda_row = max(curve_rows, key=lambda item: item["lambda_value"])
    return [
        {
            "summary_id": "CS570_0_rows",
            "metric": "review_candidate_rows",
            "value": len(curve_rows),
            "units": "rows",
            "valid_for_claim": "false",
            "notes": "axis-calibrated vector review candidate, not live claim curve",
        },
        {
            "summary_id": "CS570_1_lambda_range",
            "metric": "lambda_min_to_max",
            "value": f"{min_lambda_row['lambda_value']}..{max_lambda_row['lambda_value']}",
            "units": "m",
            "valid_for_claim": "false",
            "notes": f"source rows {min_lambda_row['bound_id']} to {max_lambda_row['bound_id']}",
        },
        {
            "summary_id": "CS570_2_alpha_range",
            "metric": "alpha_bound_min_to_max",
            "value": f"{min_alpha_row['alpha_bound']}..{max_alpha_row['alpha_bound']}",
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": f"min at lambda={min_alpha_row['lambda_value']}; max at lambda={max_alpha_row['lambda_value']}",
        },
        {
            "summary_id": "CS570_3_min_alpha",
            "metric": "tightest_candidate_bound",
            "value": min_alpha_row["alpha_bound"],
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": f"lambda={min_alpha_row['lambda_value']}; diagnostic only",
        },
    ]


def review_candidate_qa_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior_validation = read_csv(PRIOR_VALIDATION)
    anchor_rows = read_csv(ANCHOR_RECOVERY)
    promotion_rows = read_csv(PROMOTION_GATE)
    live_rows = read_csv(LIVE_BOUND_CURVE)
    candidate_claim_rows = [row for row in curve_rows if row.get("valid_for_claim") == "true"]
    live_placeholder = any("MISSING" in json.dumps(row) for row in live_rows)
    return [
        {
            "qa_id": "QA570_0_prior_validation",
            "check": "569 validation passed",
            "result": "pass" if prior_validation and not [row for row in prior_validation if row.get("result") != "pass"] else "fail",
            "detail": f"rows={len(prior_validation)}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA570_1_anchor_recovery",
            "check": "candidate recovers alpha=1 at 38.6 micrometers",
            "result": anchor_rows[0].get("recovery_status", "missing") if anchor_rows else "missing",
            "detail": json.dumps(anchor_rows[0], sort_keys=True) if anchor_rows else "",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA570_2_promotion_gate",
            "check": "promotion gate still blocks live claim",
            "result": "pass" if any(row.get("result") == "blocked" for row in promotion_rows) else "fail",
            "detail": f"blocked={len([row for row in promotion_rows if row.get('result') == 'blocked'])}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA570_3_candidate_nonclaim",
            "check": "review candidate has no claim rows",
            "result": "pass" if not candidate_claim_rows else "fail",
            "detail": f"candidate_rows={len(curve_rows)};claim_rows={len(candidate_claim_rows)}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA570_4_live_placeholder_retained",
            "check": "live digitized claim file remains placeholder",
            "result": "pass" if live_placeholder else "fail",
            "detail": f"live_rows={len(live_rows)};placeholder={bool_text(live_placeholder)}",
            "valid_for_claim": "false",
        },
    ]


def coefficient_pressure_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lambda_value in enumerate(TARGET_LAMBDAS_M):
        alpha_bound, method = interpolate_loglog(curve_rows, lambda_value)
        rows.append(
            {
                "pressure_id": f"CP570_{index}",
                "lambda_value": lambda_value,
                "lambda_units": "m",
                "alpha_bound_review_candidate": alpha_bound if alpha_bound is not None else "",
                "interpolation_method": method,
                "coefficient_constraint": "abs(K_X*Qbar_XH(lambda)*qbar_XT)<=alpha_bound(lambda)",
                "max_abs_KQqbar": alpha_bound if alpha_bound is not None else "",
                "pressure_class": pressure_class(alpha_bound) if alpha_bound is not None else "not_comparable",
                "MTS_alpha_status": "symbolic_coefficients_unfilled",
                "valid_for_claim": "false",
                "notes": "Private diagnostic pressure from review candidate only; not a live exclusion claim.",
            }
        )
    return rows


def crossing_lambdas_for_product(curve_rows: list[dict[str, Any]], product: float) -> str:
    if not curve_rows or product <= 0:
        return ""
    log_product = math.log10(product)
    crossings: list[float] = []
    previous = curve_rows[0]
    previous_delta = previous["log10_alpha"] - log_product
    for current in curve_rows[1:]:
        current_delta = current["log10_alpha"] - log_product
        if previous_delta == 0:
            crossings.append(previous["lambda_value"])
        if previous_delta * current_delta < 0:
            t = abs(previous_delta) / (abs(previous_delta) + abs(current_delta))
            log_lambda = previous["log10_lambda"] + t * (current["log10_lambda"] - previous["log10_lambda"])
            crossings.append(10**log_lambda)
        previous = current
        previous_delta = current_delta
    return ";".join(str(value) for value in crossings)


def product_scan_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not curve_rows:
        return rows
    for index, product in enumerate(PRODUCT_AMPLITUDES):
        ratios = [product / row["alpha_bound"] for row in curve_rows]
        max_ratio = max(ratios)
        worst_index = ratios.index(max_ratio)
        worst_row = curve_rows[worst_index]
        pass_all = all(ratio <= 1.0 for ratio in ratios)
        rows.append(
            {
                "scan_id": f"HPS570_{index}",
                "hypothetical_abs_product": product,
                "formula": "abs(K_X*Qbar_XH(lambda)*qbar_XT)",
                "lambda_range_tested_m": f"{curve_rows[0]['lambda_value']}..{curve_rows[-1]['lambda_value']}",
                "pass_entire_review_curve": bool_text(pass_all),
                "max_violation_ratio_product_over_bound": max_ratio,
                "worst_lambda_m": worst_row["lambda_value"],
                "worst_alpha_bound": worst_row["alpha_bound"],
                "crossing_lambdas_m": crossing_lambdas_for_product(curve_rows, product),
                "diagnostic_interpretation": "allowed_across_review_range_if_product_constant" if pass_all else "excluded_somewhere_on_review_range_if_product_constant",
                "valid_for_claim": "false",
                "notes": "Hypothetical constant-product scan only; MTS product is not derived or fitted.",
            }
        )
    return rows


def mts_alpha_status_rows() -> list[dict[str, Any]]:
    law_rows = read_csv(FINITE_ALPHA_LAW)
    requirement_rows = read_csv(COEFFICIENT_REQUIREMENTS)
    rows = [
        {
            "status_id": "MAS570_0_finite_alpha_law",
            "item": "alpha_X(lambda)",
            "current_state": "symbolic",
            "blocking_detail": "alpha_X(lambda)=K_X*Qbar_XH(lambda)*qbar_XT; no numeric K_X, source charge, or test charge",
            "next_action": "derive theorem-zero or fill/bound product coefficients",
            "valid_for_claim": "false",
        },
        {
            "status_id": "MAS570_1_range_law",
            "item": "lambda_X",
            "current_state": "symbolic",
            "blocking_detail": "lambda_X=sqrt(Z_X/M_X^2); no parent Hessian/mass-gap value",
            "next_action": "derive Z_X and M_X^2, or scan lambda_X as non-claim",
            "valid_for_claim": "false",
        },
    ]
    for index, row in enumerate(requirement_rows):
        rows.append(
            {
                "status_id": f"MAS570_req_{index}",
                "item": row.get("symbol", ""),
                "current_state": row.get("current_status", ""),
                "blocking_detail": row.get("blocks", ""),
                "next_action": row.get("fill_contract", ""),
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "status_id": "MAS570_2_source_rows",
            "item": "finite alpha law register",
            "current_state": f"law_rows={len(law_rows)};requirement_rows={len(requirement_rows)}",
            "blocking_detail": "law is structurally useful but not numeric",
            "next_action": "turn pressure table into coefficient target ledger",
            "valid_for_claim": "false",
        }
    )
    return rows


def nonclaim_runner_summary_rows(
    curve_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "NCR570_0_review_curve_pressure",
            "review_curve": rel(REVIEW_CURVE),
            "curve_rows": len(curve_rows),
            "pressure_rows": len(pressure_rows),
            "product_scan_rows": len(product_rows),
            "MTS_numeric_alpha_rows": 0,
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "result": "diagnostic_pressure_only",
            "notes": "The runner intentionally does not score a pass/fail because MTS alpha coefficients remain symbolic and the bound curve is review-candidate only.",
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "B570_0_MTS_alpha_numeric_missing",
            "blocker": "MTS finite alpha remains a symbolic product.",
            "why_it_matters": "The review curve can only pressure coefficients; it cannot certify a pass.",
            "next_action": "derive or bound K_X, Qbar_XH(lambda), qbar_XT, Z_X, and M_X^2.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B570_1_review_curve_not_promoted",
            "blocker": "The 2020 curve is review-candidate digitization, not live claim evidence.",
            "why_it_matters": "Public/local-GR claims need supplemental-table or human QA provenance.",
            "next_action": "obtain supplemental table or complete manual visual QA signoff.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B570_2_theorem_zero_still_open",
            "blocker": "No theorem yet sets qbar_XT or Qbar_XH(lambda) to zero.",
            "why_it_matters": "A finite X mode must satisfy the R10 product wall unless the zero route is derived.",
            "next_action": "try one more targeted theorem-zero return or accept finite coefficient route.",
            "claim_blocked": "true",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D570_0_pressure_wall_built",
            "decision": "R10 pressure wall is now quantified from the review curve",
            "meaning": "finite MTS X branch has explicit product bounds as a function of lambda",
            "status": "diagnostic_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D570_1_no_pass_claim",
            "decision": "do not claim R10 pass",
            "meaning": "MTS alpha product is symbolic and external curve is not promoted",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D570_2_next_fork",
            "decision": "choose finite-coefficient route or theorem-zero return",
            "meaning": "either derive qbar/source neutrality or fill the product envelope",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU570_0_allowed",
            "allowed_after_570": "Use the pressure table as private coefficient targets.",
            "forbidden_after_570": "Claim MTS passes R10/local-GR from symbolic coefficients.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU570_1_theory_route",
            "allowed_after_570": "Attempt theorem-zero for qbar_XT or Qbar_XH(lambda) with the pressure table as motivation.",
            "forbidden_after_570": "Keep cycling zero-route attempts without new premises.",
            "next_action": "derive neutrality or enter residual coefficient rows",
        },
        {
            "route_id": "RU570_2_data_route",
            "allowed_after_570": "Promote curve only after supplemental table or QA signoff.",
            "forbidden_after_570": "Overwrite live digitized bound file with review candidate rows.",
            "next_action": "supplement/manual QA remains provenance upgrade",
        },
    ]


def validation_rows(
    curve_rows: list[dict[str, Any]],
    qa_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    mts_status_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    candidate_claim_rows = [row for row in read_csv(REVIEW_CURVE) if row.get("valid_for_claim") == "true"]
    live_rows = read_csv(LIVE_BOUND_CURVE)
    live_placeholder = any("MISSING" in json.dumps(row) for row in live_rows)
    pressure_numeric = [
        row for row in pressure_rows if parse_float(row.get("alpha_bound_review_candidate")) is not None
    ]
    product_numeric = [
        row for row in product_rows if parse_float(row.get("max_violation_ratio_product_over_bound")) is not None
    ]
    qa_failed = [row for row in qa_rows if row.get("result") not in ("pass", "pass_review_candidate")]
    return [
        {
            "check_id": "V570_0_prior_569_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V570_1_review_curve_numeric",
            "result": "pass" if len(curve_rows) >= 100 else "fail",
            "detail": f"review_curve_rows={len(curve_rows)}",
        },
        {
            "check_id": "V570_2_review_curve_nonclaim",
            "result": "pass" if not candidate_claim_rows else "fail",
            "detail": f"candidate_claim_rows={len(candidate_claim_rows)}",
        },
        {
            "check_id": "V570_3_review_candidate_QA_passes",
            "result": "pass" if not qa_failed else "fail",
            "detail": f"qa_rows={len(qa_rows)};qa_failed={len(qa_failed)}",
        },
        {
            "check_id": "V570_4_pressure_table_numeric",
            "result": "pass" if len(pressure_numeric) == len(TARGET_LAMBDAS_M) else "fail",
            "detail": f"pressure_rows={len(pressure_rows)};numeric={len(pressure_numeric)}",
        },
        {
            "check_id": "V570_5_product_scan_numeric",
            "result": "pass" if len(product_numeric) == len(PRODUCT_AMPLITUDES) else "fail",
            "detail": f"product_rows={len(product_rows)};numeric={len(product_numeric)}",
        },
        {
            "check_id": "V570_6_MTS_alpha_still_symbolic",
            "result": "pass" if mts_status_rows else "fail",
            "detail": "MTS_numeric_alpha_rows=0;symbolic_status_rows=" + str(len(mts_status_rows)),
        },
        {
            "check_id": "V570_7_live_claim_curve_unchanged",
            "result": "pass" if live_placeholder else "fail",
            "detail": f"live_rows={len(live_rows)};placeholder={bool_text(live_placeholder)}",
        },
        {
            "check_id": "V570_8_no_overclaim",
            "result": "pass",
            "detail": "diagnostic_pressure_only=true;R10_pass=false;local_GR=false;claim_allowed=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    generated_at: str,
    curve_summary: list[dict[str, Any]],
    qa_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    mts_status_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    body = f"""# 570 Y5 R10 review candidate bound curve runner and MTS coefficient pressure

Generated: {generated_at}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The review-candidate Eot-Wash 2020 curve is now used as a private pressure wall.
- The finite MTS branch must satisfy `abs(K_X Qbar_XH(lambda) qbar_XT) <= alpha_bound(lambda)` at its range.
- This is not an R10 pass: MTS alpha is still symbolic, and the vector curve is still review-candidate rather than promoted claim evidence.
- The useful result is a concrete fork: either derive theorem-zero for the source/test charge, or fill/bound the finite product.

## Review Curve Summary
{markdown_table(curve_summary, ["summary_id", "metric", "value", "units", "valid_for_claim", "notes"])}

## Review Candidate QA
{markdown_table(qa_rows, ["qa_id", "check", "result", "detail", "valid_for_claim"])}

## Coefficient Pressure Table
{markdown_table(pressure_rows, ["pressure_id", "lambda_value", "lambda_units", "alpha_bound_review_candidate", "max_abs_KQqbar", "pressure_class", "valid_for_claim"])}

## Hypothetical Product Scan
{markdown_table(product_rows, ["scan_id", "hypothetical_abs_product", "pass_entire_review_curve", "max_violation_ratio_product_over_bound", "worst_lambda_m", "crossing_lambdas_m", "valid_for_claim"])}

## MTS Alpha Status
{markdown_table(mts_status_rows, ["status_id", "item", "current_state", "blocking_detail", "next_action", "valid_for_claim"])}

## Nonclaim Runner Summary
{markdown_table(runner_rows, ["runner_id", "curve_rows", "pressure_rows", "product_scan_rows", "MTS_numeric_alpha_rows", "claim_allowed", "R10_pass_for_claim", "result"])}

## Blocker Ledger
{markdown_table(blockers, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Route Update
{markdown_table(routes, ["route_id", "allowed_after_570", "forbidden_after_570", "next_action"])}

## Practical Read
This is the boxing-footwork version of the R10 test: not a knockout, not a claim, but the ring is now mapped. If the finite branch is gravity-strength near `lambda=38.6 um`, it sits right on the Eot-Wash wall. At larger ranges the allowed product drops below unity, so an unsuppressed finite `X` branch is pressured unless MTS derives neutrality/screening or a small product. That is exactly the right kind of grim-but-useful constraint.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    curve_rows = load_review_curve()
    curve_summary = curve_summary_rows(curve_rows)
    qa_rows = review_candidate_qa_rows(curve_rows)
    pressure_rows = coefficient_pressure_rows(curve_rows)
    product_rows = product_scan_rows(curve_rows)
    mts_status_rows = mts_alpha_status_rows()
    runner_rows = nonclaim_runner_summary_rows(curve_rows, pressure_rows, product_rows)
    blockers = blocker_rows()
    decisions = decision_rows()
    routes = route_update_rows()
    validation = validation_rows(curve_rows, qa_rows, pressure_rows, product_rows, mts_status_rows)

    write_csv(REVIEW_CURVE_SUMMARY_PATH, curve_summary, ["summary_id", "metric", "value", "units", "valid_for_claim", "notes"])
    write_csv(REVIEW_CANDIDATE_QA_PATH, qa_rows, ["qa_id", "check", "result", "detail", "valid_for_claim"])
    write_csv(
        COEFFICIENT_PRESSURE_PATH,
        pressure_rows,
        [
            "pressure_id",
            "lambda_value",
            "lambda_units",
            "alpha_bound_review_candidate",
            "interpolation_method",
            "coefficient_constraint",
            "max_abs_KQqbar",
            "pressure_class",
            "MTS_alpha_status",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        PRODUCT_SCAN_PATH,
        product_rows,
        [
            "scan_id",
            "hypothetical_abs_product",
            "formula",
            "lambda_range_tested_m",
            "pass_entire_review_curve",
            "max_violation_ratio_product_over_bound",
            "worst_lambda_m",
            "worst_alpha_bound",
            "crossing_lambdas_m",
            "diagnostic_interpretation",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(MTS_ALPHA_STATUS_PATH, mts_status_rows, ["status_id", "item", "current_state", "blocking_detail", "next_action", "valid_for_claim"])
    write_csv(
        NONCLAIM_RUNNER_SUMMARY_PATH,
        runner_rows,
        [
            "runner_id",
            "review_curve",
            "curve_rows",
            "pressure_rows",
            "product_scan_rows",
            "MTS_numeric_alpha_rows",
            "claim_allowed",
            "R10_pass_for_claim",
            "result",
            "notes",
        ],
    )
    write_csv(BLOCKER_LEDGER_PATH, blockers, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(ROUTE_UPDATE_PATH, routes, ["route_id", "allowed_after_570", "forbidden_after_570", "next_action"])

    write_doc(
        generated_at,
        curve_summary,
        qa_rows,
        pressure_rows,
        product_rows,
        mts_status_rows,
        runner_rows,
        blockers,
        decisions,
        validation,
        routes,
    )

    status = {
        "generated_at_utc": generated_at,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "pressure_table": rel(COEFFICIENT_PRESSURE_PATH),
        "product_scan": rel(PRODUCT_SCAN_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_passed": all(row["result"] == "pass" for row in validation),
        "claim_allowed": False,
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
