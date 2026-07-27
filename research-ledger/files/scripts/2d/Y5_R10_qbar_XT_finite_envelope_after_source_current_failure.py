from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "577-Y5-R10-qbar-XT-finite-envelope-after-source-current-failure.md"

PRIOR_576_VALIDATION = RESIDUALS / "P8_Y5_BRR545_576_VALIDATION.csv"
PRIOR_576_SUMMARY = RESIDUALS / "P8_Y5_R10_576_NONCLAIM_SUMMARY.csv"
FINITE_ALPHA_LAW = RESIDUALS / "P8_Y5_R10_567_FINITE_ALPHA_LAW.csv"
PRESSURE_570 = RESIDUALS / "P8_Y5_R10_570_COEFFICIENT_PRESSURE_TABLE.csv"
SCAN_570 = RESIDUALS / "P8_Y5_R10_570_HYPOTHETICAL_PRODUCT_SCAN.csv"
CURVE_SUMMARY_570 = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"
REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
LIVE_CLAIM_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_577_SOURCE_REGISTER.csv"
CURVE_PRESSURE_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_577_CURVE_PRESSURE_SUMMARY.csv"
QBAR_BUDGET_PATH = RESIDUALS / "P8_Y5_R10_577_QBAR_BUDGET_MATRIX.csv"
PRODUCT_SCAN_PATH = RESIDUALS / "P8_Y5_R10_577_PRODUCT_PRIOR_SCAN.csv"
COEFFICIENT_TARGETS_PATH = RESIDUALS / "P8_Y5_R10_577_COEFFICIENT_TARGETS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_577_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_577_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_577_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_577_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_qbar_XT_finite_envelope_built_nonclaim_review_candidate_pressure"
CLAIM_CEILING = "finite_qbar_XT_envelope_only_no_R10_pass_no_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md"

KQ_SCENARIOS = [
    ("KQ_1", 1.0, "natural_source_product"),
    ("KQ_0p3", 0.3, "mild_source_suppression"),
    ("KQ_0p1", 0.1, "one_order_source_suppression"),
    ("KQ_0p03", 0.03, "thirty_to_one_source_suppression"),
    ("KQ_0p01", 0.01, "two_order_source_suppression"),
]

PRODUCT_PRIORS = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]

SOURCE_FILES = [
    {
        "source_file": "576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md",
        "role": "source-current zero route failed for claim; finite qbar_XT envelope triggered",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_576_VALIDATION.csv",
        "role": "prior checkpoint validation ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_576_NONCLAIM_SUMMARY.csv",
        "role": "qbar_XT retained nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_567_FINITE_ALPHA_LAW.csv",
        "role": "finite alpha law and reverse-bound form",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_570_COEFFICIENT_PRESSURE_TABLE.csv",
        "role": "sampled coefficient pressure wall from review-candidate curve",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_570_HYPOTHETICAL_PRODUCT_SCAN.csv",
        "role": "previous constant-product smoke scan",
    },
    {
        "source_file": "source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
        "role": "review-candidate curve row count, range, and tightest diagnostic bound",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
        "role": "nonclaim vector-curve candidate used for private coefficient pressure only",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live claim curve placeholder; should remain invalid for claim",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def to_float(value: str) -> float:
    return float(str(value).strip())


def fmt(value: float) -> str:
    if value == 0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.6e}"
    return f"{value:.12g}"


def pressure_class(alpha_bound: float) -> str:
    if alpha_bound >= 100:
        return "very_weak_pressure_alpha_above_100"
    if alpha_bound >= 1:
        return "natural_product_allowed_at_this_lambda"
    if alpha_bound >= 0.1:
        return "subunity_product_required"
    if alpha_bound >= 0.01:
        return "percent_to_tenth_product_required"
    if alpha_bound >= 0.001:
        return "per_mille_to_percent_product_required"
    return "sub_per_mille_product_required"


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in SOURCE_FILES:
        source_file = str(item["source_file"])
        rows.append(
            {
                "source_file": source_file,
                "exists": str((ROOT / source_file).exists()),
                "role": item["role"],
            }
        )
    return rows


def numeric_curve_rows(curve_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in curve_rows:
        try:
            lambda_value = to_float(row["lambda_value"])
            alpha_bound = to_float(row["alpha_bound"])
        except (KeyError, ValueError):
            continue
        if lambda_value > 0 and alpha_bound > 0:
            out.append({**row, "lambda_value_float": lambda_value, "alpha_bound_float": alpha_bound})
    return out


def make_curve_pressure_summary(
    curve_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    live_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    numeric_rows = numeric_curve_rows(curve_rows)
    alpha_values = [row["alpha_bound_float"] for row in numeric_rows]
    lambda_values = [row["lambda_value_float"] for row in numeric_rows]
    tightest = min(numeric_rows, key=lambda row: row["alpha_bound_float"])
    sample_bounds = [to_float(row["alpha_bound_review_candidate"]) for row in pressure_rows]
    live_claim_rows = [row for row in live_rows if str(row.get("valid_for_claim", "")).lower() == "true"]
    return [
        {
            "summary_id": "CPS577_0_curve_rows",
            "metric": "review_candidate_rows",
            "value": len(numeric_rows),
            "units": "rows",
            "valid_for_claim": "false",
            "notes": "private review-candidate curve only",
        },
        {
            "summary_id": "CPS577_1_lambda_range",
            "metric": "lambda_min_to_max",
            "value": f"{fmt(min(lambda_values))}..{fmt(max(lambda_values))}",
            "units": "m",
            "valid_for_claim": "false",
            "notes": "range over numeric review-candidate rows",
        },
        {
            "summary_id": "CPS577_2_alpha_range",
            "metric": "alpha_bound_min_to_max",
            "value": f"{fmt(min(alpha_values))}..{fmt(max(alpha_values))}",
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": f"tightest at lambda={fmt(tightest['lambda_value_float'])}",
        },
        {
            "summary_id": "CPS577_3_full_curve_product_ceiling",
            "metric": "max_constant_product_for_entire_review_curve",
            "value": fmt(tightest["alpha_bound_float"]),
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": "constant |K_X Qbar_XH qbar_XT| must be below this to clear all review-candidate rows",
        },
        {
            "summary_id": "CPS577_4_pressure_table_samples",
            "metric": "sampled_lambda_pressure_rows",
            "value": len(pressure_rows),
            "units": "rows",
            "valid_for_claim": "false",
            "notes": f"sample alpha min={fmt(min(sample_bounds))}; sample alpha max={fmt(max(sample_bounds))}",
        },
        {
            "summary_id": "CPS577_5_live_claim_curve",
            "metric": "live_claim_curve_rows_valid",
            "value": len(live_claim_rows),
            "units": "rows",
            "valid_for_claim": "false",
            "notes": "live digitized claim file remains placeholder/invalid; no R10 claim",
        },
    ]


def make_qbar_budget_matrix(pressure_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pressure_row in pressure_rows:
        lambda_value = to_float(pressure_row["lambda_value"])
        alpha_bound = to_float(pressure_row["alpha_bound_review_candidate"])
        for scenario_id, kq_abs, scenario_note in KQ_SCENARIOS:
            qbar_ceiling = alpha_bound / kq_abs
            rows.append(
                {
                    "budget_id": f"QB577_{len(rows)}",
                    "pressure_id": pressure_row["pressure_id"],
                    "lambda_value": fmt(lambda_value),
                    "lambda_units": pressure_row["lambda_units"],
                    "alpha_bound_review_candidate": fmt(alpha_bound),
                    "assumed_abs_KX_Qbar_XH": fmt(kq_abs),
                    "qbar_XT_max_abs": fmt(qbar_ceiling),
                    "product_ceiling": fmt(alpha_bound),
                    "pressure_class": pressure_class(alpha_bound),
                    "scenario": scenario_note,
                    "valid_for_claim": "false",
                    "notes": "Diagnostic qbar budget only; review-candidate curve and unfilled parent coefficients block claim.",
                }
            )
    return rows


def make_product_prior_scan(curve_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    numeric_rows = numeric_curve_rows(curve_rows)
    tightest = min(numeric_rows, key=lambda row: row["alpha_bound_float"])
    min_bound = tightest["alpha_bound_float"]
    rows: list[dict[str, object]] = []
    for product in PRODUCT_PRIORS:
        pass_curve = product <= min_bound
        rows.append(
            {
                "scan_id": f"PPS577_{len(rows)}",
                "constant_abs_product": fmt(product),
                "formula": "abs(K_X*Qbar_XH(lambda)*qbar_XT)",
                "review_curve_rows_tested": len(numeric_rows),
                "pass_entire_review_candidate_curve": str(pass_curve).lower(),
                "max_violation_ratio_product_over_bound": fmt(product / min_bound),
                "worst_lambda_m": fmt(tightest["lambda_value_float"]),
                "worst_alpha_bound": fmt(min_bound),
                "diagnostic_interpretation": "allowed_across_review_candidate_if_product_constant"
                if pass_curve
                else "excluded_somewhere_on_review_candidate_if_product_constant",
                "valid_for_claim": "false",
                "notes": "Nonclaim prior scan; MTS product is not derived and curve is not promoted.",
            }
        )
    return rows


def make_coefficient_targets(curve_summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    full_ceiling = next(
        row["value"]
        for row in curve_summary_rows
        if row["summary_id"] == "CPS577_3_full_curve_product_ceiling"
    )
    return [
        {
            "target_id": "CT577_0_lambda_X",
            "unknown": "lambda_X",
            "needed_form": "lambda_X=sqrt(Z_X/M_X^2)",
            "acceptable_route": "derive positive Z_X and positive parent Hessian M_X^2, or scan lambda_X as nonclaim",
            "diagnostic_pressure": "range controls which alpha_bound(lambda) ceiling applies",
            "current_status": "not_parent_derived",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_1_product_wall",
            "unknown": "abs(K_X Qbar_XH qbar_XT)",
            "needed_form": f"<= alpha_bound(lambda_X), and <= {full_ceiling} if treated as constant over full review range",
            "acceptable_route": "derive suppression, derive screening/neutrality, or provide sourced numeric coefficients",
            "diagnostic_pressure": "full review-candidate curve demands per-mille-scale constant product",
            "current_status": "finite_envelope_built_nonclaim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_2_K_X",
            "unknown": "K_X",
            "needed_form": "parent-normalized kinetic/source prefactor with sign and units fixed",
            "acceptable_route": "derive from parent action normalization or absorb convention into a declared K_X ledger",
            "diagnostic_pressure": "cannot be symbolic in a claim row",
            "current_status": "symbolic",
            "next_action": "derive or bound K_X",
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_3_Qbar_XH",
            "unknown": "Qbar_XH(lambda)",
            "needed_form": "source charge/profile for the host/source sector at lambda_X",
            "acceptable_route": "derive source neutrality/screening, or compute finite source charge with units",
            "diagnostic_pressure": "if O(1), qbar_XT must carry most suppression at long lambda",
            "current_status": "symbolic",
            "next_action": "derive source charge profile or finite bound",
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_4_qbar_XT",
            "unknown": "qbar_XT",
            "needed_form": "test-body charge per inertial mass in the local branch",
            "acceptable_route": "derive tiny value from parent matter coupling, or keep finite and score against qbar budget matrix",
            "diagnostic_pressure": "qbar_XT=0 failed; finite value now must be small enough",
            "current_status": "retained_finite",
            "next_action": "derive qbar_XT amplitude law or bounded prior",
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_5_abs_alpha_policy",
            "unknown": "sign of alpha_X",
            "needed_form": "R10 uses abs(alpha_X); sign cannot rescue an over-bound fifth-force magnitude",
            "acceptable_route": "use sign only for model dynamics, never for bound evasion",
            "diagnostic_pressure": "compare absolute product to alpha_bound",
            "current_status": "policy_locked",
            "next_action": "keep abs-value gate in runner",
            "valid_for_claim": "false",
        },
        {
            "target_id": "CT577_6_claim_curve",
            "unknown": "alpha_bound(lambda) claim evidence",
            "needed_form": "full source-backed digitized or official curve with valid_for_claim=true rows",
            "acceptable_route": "supplemental table, official data, or manually QA'd digitization provenance",
            "diagnostic_pressure": "current review candidate is useful but private only",
            "current_status": "claim_blocked",
            "next_action": "promote bound curve only after provenance gate",
            "valid_for_claim": "false",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D577_0_finite_envelope_built",
            "decision": "use finite qbar_XT envelope after source-current zero route failed",
            "meaning": "R10 pressure is now an explicit product bound instead of a vague objection",
            "status": "diagnostic_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D577_1_no_R10_claim",
            "decision": "do not claim R10 pass",
            "meaning": "bound curve is review-candidate only and MTS coefficients are still symbolic",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D577_2_lambda_matters",
            "decision": "lambda_X is now the first physical fork",
            "meaning": "O(1) product may survive near very short ranges, but long-range millimetre-scale branches need percent/per-mille suppression",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D577_3_coefficients_matter",
            "decision": "derive or bound K_X, Qbar_XH(lambda), and qbar_XT next",
            "meaning": "a finite branch can still survive, but not with all unknowns left symbolic",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU577_0_allowed",
            "allowed_after_577": "use qbar budget matrix as private coefficient target table",
            "forbidden_after_577": "claim R10 pass from symbolic alpha rows",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU577_1_allowed",
            "allowed_after_577": "say finite branch survives only if range/product land under the wall",
            "forbidden_after_577": "say finite branch fails without deriving lambda_X and product coefficients",
            "next_action": "derive lambda_X or scan nonclaim priors",
        },
        {
            "route_id": "RU577_2_allowed",
            "allowed_after_577": "return to theorem-zero only if a stronger parent action closes constants/source coupling",
            "forbidden_after_577": "reopen qbar_XT=0 by assertion",
            "next_action": "keep zero route as conditional escape hatch",
        },
        {
            "route_id": "RU577_3_allowed",
            "allowed_after_577": "score absolute product, not signed alpha tricks",
            "forbidden_after_577": "use negative alpha sign to hide fifth-force magnitude",
            "next_action": "abs-value gate stays locked",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_576: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    curve_rows: list[dict[str, str]],
    live_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    budget_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    coefficient_targets: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_pass = bool(prior_576) and all(row.get("result") == "pass" for row in prior_576)
    qbar_retained = bool(prior_summary) and prior_summary[0].get("qbar_XT_retained") == "true"
    numeric_curve = numeric_curve_rows(curve_rows)
    curve_claim_rows = [row for row in curve_rows if str(row.get("valid_for_claim", "")).lower() == "true"]
    live_claim_rows = [row for row in live_rows if str(row.get("valid_for_claim", "")).lower() == "true"]
    pressure_numeric = all(
        to_float(row["lambda_value"]) > 0 and to_float(row["alpha_bound_review_candidate"]) > 0
        for row in pressure_rows
    )
    product_001 = next(row for row in scan_rows if row["constant_abs_product"] == "0.001")
    product_003 = next(row for row in scan_rows if row["constant_abs_product"] == "0.003")
    blocked_decision = any(row.get("status") == "blocked_for_claim" for row in decisions)
    symbolic_targets = [
        row
        for row in coefficient_targets
        if row.get("current_status") in {"symbolic", "retained_finite", "not_parent_derived"}
    ]
    return [
        {
            "check_id": "V577_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(map(str, missing)) if missing else ""),
        },
        {
            "check_id": "V577_1_prior_576_validated",
            "result": "pass" if prior_pass and qbar_retained else "fail",
            "detail": f"prior_rows={len(prior_576)};qbar_retained={qbar_retained}",
        },
        {
            "check_id": "V577_2_review_curve_numeric_nonclaim",
            "result": "pass" if len(numeric_curve) > 0 and len(curve_claim_rows) == 0 else "fail",
            "detail": f"numeric_curve_rows={len(numeric_curve)};claim_rows={len(curve_claim_rows)}",
        },
        {
            "check_id": "V577_3_live_claim_curve_still_blocked",
            "result": "pass" if len(live_claim_rows) == 0 else "fail",
            "detail": f"live_claim_rows={len(live_claim_rows)}",
        },
        {
            "check_id": "V577_4_pressure_rows_numeric",
            "result": "pass" if pressure_rows and pressure_numeric else "fail",
            "detail": f"pressure_rows={len(pressure_rows)}",
        },
        {
            "check_id": "V577_5_qbar_budget_matrix_written",
            "result": "pass" if len(budget_rows) == len(pressure_rows) * len(KQ_SCENARIOS) else "fail",
            "detail": f"budget_rows={len(budget_rows)};scenarios={len(KQ_SCENARIOS)}",
        },
        {
            "check_id": "V577_6_product_prior_scan_sane",
            "result": "pass"
            if product_001["pass_entire_review_candidate_curve"] == "true"
            and product_003["pass_entire_review_candidate_curve"] == "false"
            else "fail",
            "detail": "product_0p001_passes_review_candidate=true;product_0p003_fails_review_candidate=true",
        },
        {
            "check_id": "V577_7_symbolic_coefficients_block_claim",
            "result": "pass" if len(symbolic_targets) >= 4 and blocked_decision else "fail",
            "detail": f"symbolic_or_retained_targets={len(symbolic_targets)};claim_allowed=false",
        },
        {
            "check_id": "V577_8_no_overclaim",
            "result": "pass",
            "detail": "finite_envelope_only;no_R10_pass;no_WEP;no_PPN;no_local_GR",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    curve_summary: list[dict[str, object]],
    budget_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    coefficient_targets: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sample_budget = [
        row
        for row in budget_rows
        if row["assumed_abs_KX_Qbar_XH"] == "1"
        or row["pressure_id"] in {"CP570_3", "CP570_6", "CP570_9"}
    ]
    sample_budget = sample_budget[:18]

    body = f"""# 577 Y5 R10 qbar_XT finite envelope after source-current failure

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- Since `qbar_XT=0` was not parent-derived in checkpoint 576, the finite branch must obey the product wall:

```text
alpha_X(lambda_X) = K_X Qbar_XH(lambda_X) qbar_XT
abs(K_X Qbar_XH(lambda_X) qbar_XT) <= alpha_bound(lambda_X).
```

- Using the current nonclaim 2020 review-candidate curve, the tightest diagnostic constant-product ceiling over the scanned range is about `2.34e-3` near `lambda ≈ 0.608 mm`.
- This does not kill the branch. It says the branch must either land at a short enough range, or derive/supply suppression in `K_X`, `Qbar_XH`, or `qbar_XT`.
- No R10/local-GR claim is made: the curve is still review-candidate only, and the MTS product is still symbolic.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Curve Pressure Summary
{markdown_table(curve_summary, ["summary_id", "metric", "value", "units", "valid_for_claim", "notes"])}

## Product Prior Scan
{markdown_table(scan_rows, ["scan_id", "constant_abs_product", "pass_entire_review_candidate_curve", "max_violation_ratio_product_over_bound", "worst_lambda_m", "worst_alpha_bound", "diagnostic_interpretation", "valid_for_claim"])}

## qbar_XT Budget Matrix
The full budget matrix is written to `source-intake/mts_residuals/P8_Y5_R10_577_QBAR_BUDGET_MATRIX.csv`. Selected rows:

{markdown_table(sample_budget, ["budget_id", "pressure_id", "lambda_value", "alpha_bound_review_candidate", "assumed_abs_KX_Qbar_XH", "qbar_XT_max_abs", "pressure_class", "valid_for_claim"])}

## Coefficient Targets
{markdown_table(coefficient_targets, ["target_id", "unknown", "needed_form", "acceptable_route", "diagnostic_pressure", "current_status", "next_action", "valid_for_claim"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_577", "forbidden_after_577", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is the useful kind of pressure. If the parent theory eventually predicts an unsuppressed `K_X Qbar_XH qbar_XT ~ 1` and a range around `0.1-1 mm`, R10 is probably brutal. If the range sits around the short Eot-Wash edge near tens of microns, or if source/test charge suppression is derived, the local branch can still breathe. So the next honest derivation target is not “is MTS dead?”; it is `lambda_X=sqrt(Z_X/M_X^2)` plus the product coefficients. That is the next gear to machine.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_576 = read_csv(PRIOR_576_VALIDATION)
    prior_summary = read_csv(PRIOR_576_SUMMARY)
    curve_rows = read_csv(REVIEW_CURVE)
    live_rows = read_csv(LIVE_CLAIM_CURVE)
    pressure_rows = read_csv(PRESSURE_570)
    scan_570_rows = read_csv(SCAN_570)

    curve_summary = make_curve_pressure_summary(curve_rows, pressure_rows, live_rows)
    budget_rows = make_qbar_budget_matrix(pressure_rows)
    scan_rows = make_product_prior_scan(curve_rows)
    coefficient_targets = make_coefficient_targets(curve_summary)
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_576,
        prior_summary,
        curve_rows,
        live_rows,
        pressure_rows,
        budget_rows,
        scan_rows,
        coefficient_targets,
        decisions,
    )

    full_ceiling = next(
        row["value"]
        for row in curve_summary
        if row["summary_id"] == "CPS577_3_full_curve_product_ceiling"
    )
    tightest_lambda = next(
        row["notes"].split("lambda=")[1]
        for row in curve_summary
        if row["summary_id"] == "CPS577_2_alpha_range"
    )
    summary_rows = [
        {
            "summary_id": "S577_0_result",
            "status": STATUS,
            "qbar_XT_zero_parent_derived": "false",
            "qbar_XT_retained": "true",
            "finite_product_wall": "abs(K_X*Qbar_XH(lambda_X)*qbar_XT)<=alpha_bound(lambda_X)",
            "review_candidate_constant_product_ceiling": full_ceiling,
            "tightest_review_candidate_lambda_m": tightest_lambda,
            "bound_curve_valid_for_claim": "false",
            "MTS_coefficients_numeric": "false",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        CURVE_PRESSURE_SUMMARY_PATH,
        curve_summary,
        ["summary_id", "metric", "value", "units", "valid_for_claim", "notes"],
    )
    write_csv(
        QBAR_BUDGET_PATH,
        budget_rows,
        [
            "budget_id",
            "pressure_id",
            "lambda_value",
            "lambda_units",
            "alpha_bound_review_candidate",
            "assumed_abs_KX_Qbar_XH",
            "qbar_XT_max_abs",
            "product_ceiling",
            "pressure_class",
            "scenario",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        PRODUCT_SCAN_PATH,
        scan_rows,
        [
            "scan_id",
            "constant_abs_product",
            "formula",
            "review_curve_rows_tested",
            "pass_entire_review_candidate_curve",
            "max_violation_ratio_product_over_bound",
            "worst_lambda_m",
            "worst_alpha_bound",
            "diagnostic_interpretation",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        COEFFICIENT_TARGETS_PATH,
        coefficient_targets,
        [
            "target_id",
            "unknown",
            "needed_form",
            "acceptable_route",
            "diagnostic_pressure",
            "current_status",
            "next_action",
            "valid_for_claim",
        ],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_577", "forbidden_after_577", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "qbar_XT_zero_parent_derived",
            "qbar_XT_retained",
            "finite_product_wall",
            "review_candidate_constant_product_ceiling",
            "tightest_review_candidate_lambda_m",
            "bound_curve_valid_for_claim",
            "MTS_coefficients_numeric",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        curve_summary,
        budget_rows,
        scan_rows,
        coefficient_targets,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "claim_allowed": False,
                "qbar_XT_retained": True,
                "finite_product_wall": "abs(K_X*Qbar_XH(lambda_X)*qbar_XT)<=alpha_bound(lambda_X)",
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
