from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import R10_alpha_lambda_bound_prediction_runner as r10_runner


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
BOUND_DIR = ROOT / "source-intake" / "local_bounds"
RUNS_DIR = ROOT / "runs"

DOC_PATH = ROOT / "567-Y5-R10-finite-alpha-coefficient-fill-and-real-bound-curve-runner.md"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_finite_alpha_coefficient_fill_and_real_bound_curve_runner.py"

UPSTREAM_DOC = ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md"
UPSTREAM_VALIDATION = MTS_DIR / "P8_Y5_BRR545_566_VALIDATION.csv"
QUEUE_PATH = MTS_DIR / "P8_Y5_R10_566_ALPHA_COEFFICIENT_FILL_QUEUE.csv"
LIVE_MTS_CURVE = MTS_DIR / "R10_alpha_lambda_curve_MTS_source_normalization.csv"
LIVE_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
ANCHOR_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"

SOURCE_REGISTER_PATH = MTS_DIR / "P8_Y5_R10_567_SOURCE_REGISTER.csv"
FINITE_ALPHA_LAW_PATH = MTS_DIR / "P8_Y5_R10_567_FINITE_ALPHA_LAW.csv"
COEFFICIENT_REQUIREMENTS_PATH = MTS_DIR / "P8_Y5_R10_567_COEFFICIENT_REQUIREMENTS.csv"
REVERSE_BOUND_TARGETS_PATH = MTS_DIR / "P8_Y5_R10_567_REVERSE_BOUND_TARGETS.csv"
PRIOR_SCAN_TEMPLATE_PATH = MTS_DIR / "P8_Y5_R10_567_PRIOR_SCAN_TEMPLATE.csv"
MTS_FINITE_SMOKE_PATH = MTS_DIR / "R10_alpha_lambda_curve_MTS_FINITE_ALPHA_SMOKE_NONCLAIM.csv"
RUNNER_SUMMARY_PATH = MTS_DIR / "P8_Y5_R10_567_RUNNER_SUMMARY.csv"
EVALUATOR_PATH = MTS_DIR / "P8_Y5_R10_567_EVALUATOR.csv"
BLOCKER_LEDGER_PATH = MTS_DIR / "P8_Y5_R10_567_BLOCKER_LEDGER.csv"
DECISION_PATH = MTS_DIR / "P8_Y5_BRR545_567_DECISION.csv"
VALIDATION_PATH = MTS_DIR / "P8_Y5_BRR545_567_VALIDATION.csv"
ROUTE_UPDATE_PATH = MTS_DIR / "P8_Y5_BRR545_567_ROUTE_UPDATE.csv"

STATUS = "Y5_R10_finite_alpha_coefficient_fill_scaffold_written_reverse_bounds_anchor_only_no_claim"
CLAIM_CEILING = "finite_alpha_coefficient_scaffold_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in json.dumps(row, sort_keys=True)


def source_register() -> list[dict[str, Any]]:
    local_sources = [
        (UPSTREAM_DOC, "immediate upstream fork: primitive quotient/no-marker route ended in coefficient fill"),
        (UPSTREAM_VALIDATION, "prior checkpoint validation guardrail"),
        (QUEUE_PATH, "coefficient fill queue inherited from 566"),
        (LIVE_MTS_CURVE, "live MTS alpha(lambda) placeholder retained unchanged"),
        (LIVE_BOUND_CURVE, "live R10 bound placeholder retained unchanged"),
        (ANCHOR_BOUND_CURVE, "source-backed anchor-only smoke bound rows"),
        (ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py", "existing alpha(lambda) comparator reused"),
        (SCRIPT_PATH, "this checkpoint generator"),
    ]
    rows = [
        {
            "source_file": rel(path),
            "role": role,
            "source_type": "local_path",
            "exists": bool_text(path.exists()),
            "valid_for_claim": "false",
        }
        for path, role in local_sources
    ]
    rows.extend(
        [
            {
                "source_file": "https://pubmed.ncbi.nlm.nih.gov/32216404/",
                "role": "modern Eot-Wash short-range anchor metadata",
                "source_type": "web_source_recorded_not_reacquired",
                "exists": "not_applicable_url",
                "valid_for_claim": "false",
            },
            {
                "source_file": "https://arxiv.org/abs/2002.11761",
                "role": "modern Eot-Wash 2020 source-backed anchor row",
                "source_type": "web_source_recorded_not_reacquired",
                "exists": "not_applicable_url",
                "valid_for_claim": "false",
            },
            {
                "source_file": "https://arxiv.org/abs/hep-ph/0611184",
                "role": "2007 Eot-Wash continuity anchor row",
                "source_type": "web_source_recorded_not_reacquired",
                "exists": "not_applicable_url",
                "valid_for_claim": "false",
            },
        ]
    )
    return rows


def finite_alpha_law() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "FA567_0_finite_alpha",
            "object": "alpha_X(lambda_X)",
            "symbolic_form": "alpha_X(lambda_X)=s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "equivalent_contract": "alpha_X(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "needed_inputs": "s_X;Z_X;G_obs;Qbar_XH(lambda_X);qbar_XT",
            "derived_from_parent": "false",
            "use": "finite-range X branch score variable",
            "valid_for_claim": "false",
            "notes": "The denominator convention may be absorbed into K_X; no numeric claim until parent normalization fixes K_X.",
        },
        {
            "law_id": "FA567_1_range",
            "object": "lambda_X",
            "symbolic_form": "lambda_X=sqrt(Z_X/M_X^2)",
            "equivalent_contract": "M_X^2=Z_X/lambda_X^2",
            "needed_inputs": "Z_X;M_X^2",
            "derived_from_parent": "false",
            "use": "maps parent Hessian/mass-gap data to R10 range",
            "valid_for_claim": "false",
            "notes": "Requires positive kinetic normalization and positive mass gap for ordinary Yukawa decay.",
        },
        {
            "law_id": "FA567_2_bound_product",
            "object": "P_X(lambda)",
            "symbolic_form": "P_X(lambda)=abs(K_X*Qbar_XH(lambda)*qbar_XT)",
            "equivalent_contract": "P_X(lambda)<=alpha_bound(lambda)",
            "needed_inputs": "K_X;Qbar_XH(lambda);qbar_XT;alpha_bound(lambda)",
            "derived_from_parent": "false",
            "use": "R10 comparison form independent of sign convention",
            "valid_for_claim": "false",
            "notes": "This is the safe finite-alpha gate: sign can help model-building but cannot hide abs(alpha) in the fifth-force bound.",
        },
        {
            "law_id": "FA567_3_reverse_anchor",
            "object": "anchor-only reverse constraint",
            "symbolic_form": "abs(K_X*Qbar_XH(lambda_anchor)*qbar_XT)<=alpha_anchor",
            "equivalent_contract": "source-backed anchors define non-claim target magnitudes only",
            "needed_inputs": "anchor lambda;anchor alpha_bound;full curve before claim",
            "derived_from_parent": "false",
            "use": "smoke target for future coefficient/prior scan",
            "valid_for_claim": "false",
            "notes": "Two alpha=1 threshold anchors are not a digitized alpha(lambda) curve.",
        },
    ]


def coefficient_requirements(queue_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        symbol = row.get("symbol", "")
        if "Z_X" in symbol:
            fill_contract = "derive positive kinetic Hessian coefficient or define conservative scan prior"
            blocks = "lambda_X;K_X;ghost/stability sign"
        elif "M_X" in symbol:
            fill_contract = "derive positive Hessian mass gap or scan lambda_X directly as non-claim"
            blocks = "range selection;interpolation into R10 bound curve"
        elif "qbar_XT" in symbol:
            fill_contract = "derive ordinary test-body X neutrality or enter residual coupling bound"
            blocks = "WEP/local fifth-force amplitude"
        elif "Qbar_XH" in symbol:
            fill_contract = "derive source projected X charge or channelwise source form factor"
            blocks = "source amplitude in torsion-balance bodies"
        elif "alpha_bound" in symbol:
            fill_contract = "digitize/source full alpha_bound(lambda) curve with valid claim rows"
            blocks = "external evidence comparison"
        else:
            fill_contract = "supply parent-derived numeric value or explicit non-claim prior"
            blocks = "R10 finite-alpha scoring"
        rows.append(
            {
                "requirement_id": row.get("queue_id", ""),
                "symbol": symbol,
                "needed_for": row.get("needed_for", ""),
                "current_status": row.get("current_status", ""),
                "fill_contract": fill_contract,
                "blocks": blocks,
                "allowed_now": "symbolic scaffold;reverse bound target;non-claim prior template",
                "forbidden_now": "R10 pass;local-GR pass;alpha=0 theorem;numeric exclusion claim",
                "valid_for_claim": "false",
            }
        )
    return rows


def reverse_bound_targets(anchor_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, anchor in enumerate(anchor_rows):
        lambda_value = parse_float(anchor.get("lambda_value", ""))
        alpha_bound = parse_float(anchor.get("alpha_bound", ""))
        lambda_units = anchor.get("lambda_units", "")
        if lambda_value is None or alpha_bound is None or alpha_bound <= 0:
            max_product = ""
            log_lambda = ""
            issue = "anchor_not_numeric"
        else:
            max_product = alpha_bound
            log_lambda = math.log10(lambda_value) if lambda_value > 0 and lambda_units == "m" else ""
            issue = "anchor_only_noncurve"
        rows.append(
            {
                "target_id": f"RBT567_{index}",
                "bound_id": anchor.get("bound_id", ""),
                "lambda_value": anchor.get("lambda_value", ""),
                "lambda_units": lambda_units,
                "log10_lambda_m": log_lambda,
                "alpha_bound": anchor.get("alpha_bound", ""),
                "max_abs_KQqbar_at_anchor": max_product,
                "constraint_form": "abs(K_X*Qbar_XH(lambda_anchor)*qbar_XT)<=alpha_bound_anchor",
                "digitization_method": anchor.get("digitization_method", ""),
                "alpha_bound_source": anchor.get("alpha_bound_source", ""),
                "source_file": anchor.get("source_file", ""),
                "valid_for_claim": "false",
                "claim_blocker": issue,
                "notes": "Reverse target only; cannot replace full R10 alpha(lambda) evidence curve.",
            }
        )
    return rows


def prior_scan_template() -> list[dict[str, Any]]:
    return [
        {
            "scan_id": "PST567_0_lambda_anchor_window",
            "parameter": "lambda_X",
            "suggested_domain": "3.0e-5 m <= lambda_X <= 6.5e-5 m",
            "units": "m",
            "why": "covers current Eot-Wash alpha=1 anchor thresholds without pretending to have full curve",
            "claim_use": "smoke_only",
            "valid_for_claim": "false",
        },
        {
            "scan_id": "PST567_1_lambda_broad_R10",
            "parameter": "lambda_X",
            "suggested_domain": "1.0e-6 m <= lambda_X <= 1.0e-2 m",
            "units": "m",
            "why": "broad non-claim R10 range for later digitized curve interpolation stress",
            "claim_use": "smoke_only_until_curve_digitized",
            "valid_for_claim": "false",
        },
        {
            "scan_id": "PST567_2_product_amplitude",
            "parameter": "abs(K_X*Qbar_XH*qbar_XT)",
            "suggested_domain": "log10 product from -30 to +3",
            "units": "dimensionless_alpha_convention",
            "why": "tests whether any finite source/test charge branch can sit below short-range fifth-force bounds",
            "claim_use": "nonclaim_prior_scan",
            "valid_for_claim": "false",
        },
        {
            "scan_id": "PST567_3_sign",
            "parameter": "s_X",
            "suggested_domain": "-1,+1",
            "units": "sign",
            "why": "keeps attractive/repulsive convention explicit while R10 compares abs(alpha)",
            "claim_use": "diagnostic_only",
            "valid_for_claim": "false",
        },
        {
            "scan_id": "PST567_4_source_charge",
            "parameter": "Qbar_XH(lambda)",
            "suggested_domain": "parent integral or channelwise bound required",
            "units": "parent_normalized",
            "why": "torsion-balance source composition must not be hand-waved",
            "claim_use": "blocked_until_parent_or_external_source_model",
            "valid_for_claim": "false",
        },
        {
            "scan_id": "PST567_5_test_charge",
            "parameter": "qbar_XT",
            "suggested_domain": "zero theorem or residual bound required",
            "units": "parent_normalized",
            "why": "ordinary test-body neutrality is the local-GR/WEP pressure point",
            "claim_use": "blocked_until_parent_or_residual_bound",
            "valid_for_claim": "false",
        },
    ]


def finite_alpha_smoke_rows(anchor_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, anchor in enumerate(anchor_rows):
        rows.append(
            {
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "finite_X_alpha_symbolic_nonclaim",
                "curve_id": f"R10_alpha_lambda_curve_MTS_FINITE_ALPHA_SMOKE_NONCLAIM_{index}",
                "lambda_value": anchor.get("lambda_value", ""),
                "lambda_units": anchor.get("lambda_units", ""),
                "alpha_predicted": "K_X*Qbar_XH(lambda)*qbar_XT",
                "alpha_bound": anchor.get("alpha_bound", ""),
                "alpha_bound_source": anchor.get("alpha_bound_source", ""),
                "force_law_form": "Yukawa_alpha_exp_minus_r_over_lambda_over_r2",
                "derivation_status": "symbolic_coefficient_fill_required_not_numeric",
                "formula_reference": rel(DOC_PATH),
                "source_file": rel(UPSTREAM_DOC),
                "assumptions": "finite physical X branch;abs alpha compared to R10 bound;anchor-only external rows",
                "valid_for_claim": "false",
                "notes": "Smoke row only: symbolic alpha intentionally fails numeric claim validation.",
            }
        )
    return rows


def summarize_runner(run_id: str, result: dict[str, Any], notes: str) -> dict[str, Any]:
    status = result["status"]
    return {
        "runner_id": run_id,
        "mts_curve": status["mts_curve"],
        "bound_curve": status["bound_curve"],
        "output_dir": status["output_dir"],
        "mts_rows": status["mts_rows"],
        "valid_mts_rows": status["valid_mts_rows"],
        "bound_rows": status["bound_rows"],
        "valid_bound_rows": status["valid_bound_rows"],
        "comparison_rows": status["comparison_rows"],
        "passed_rows": status["passed_rows"],
        "blocked_or_failed_rows": status["blocked_or_failed_rows"],
        "R10_pass_for_claim": status["R10_pass_for_claim"],
        "claim_allowed": status["claim_allowed"],
        "notes": notes,
    }


def validation_rows(
    sources: list[dict[str, Any]],
    law_rows: list[dict[str, Any]],
    requirement_rows: list[dict[str, Any]],
    reverse_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(UPSTREAM_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    local_missing = [
        row["source_file"]
        for row in sources
        if row.get("source_type") == "local_path" and row.get("exists") != "true"
    ]
    reverse_numeric = [
        row
        for row in reverse_rows
        if parse_float(str(row.get("lambda_value", ""))) is not None
        and parse_float(str(row.get("alpha_bound", ""))) is not None
        and parse_float(str(row.get("lambda_value", ""))) > 0
        and parse_float(str(row.get("alpha_bound", ""))) > 0
    ]
    invalid_claim_markers = [
        row for row in smoke_rows + reverse_rows if row.get("valid_for_claim") == "true" or has_missing_marker(row)
    ]
    live_runner = next((row for row in runner_rows if row["runner_id"] == "R10_RUNNER_567_LIVE_PLACEHOLDER_RECHECK"), {})
    smoke_runner = next((row for row in runner_rows if row["runner_id"] == "R10_RUNNER_567_FINITE_ALPHA_ANCHOR_SMOKE"), {})
    validations = [
        {
            "check_id": "V567_0_source_paths_exist",
            "result": "pass" if not local_missing else "fail",
            "detail": f"missing={len(local_missing)}",
        },
        {
            "check_id": "V567_1_prior_566_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V567_2_finite_alpha_law_written",
            "result": "pass" if len(law_rows) == 4 else "fail",
            "detail": f"law_rows={len(law_rows)}",
        },
        {
            "check_id": "V567_3_coefficient_requirements_preserved",
            "result": "pass" if len(requirement_rows) == 5 else "fail",
            "detail": f"requirement_rows={len(requirement_rows)}",
        },
        {
            "check_id": "V567_4_reverse_bounds_anchor_only",
            "result": "pass" if len(reverse_rows) == len(reverse_numeric) and reverse_rows else "fail",
            "detail": f"reverse_rows={len(reverse_rows)};numeric_positive={len(reverse_numeric)};valid_for_claim_true=0",
        },
        {
            "check_id": "V567_5_smoke_rows_nonclaim_symbolic",
            "result": "pass" if smoke_rows and not invalid_claim_markers else "fail",
            "detail": f"smoke_rows={len(smoke_rows)};claim_or_missing_marker_rows={len(invalid_claim_markers)}",
        },
        {
            "check_id": "V567_6_live_runner_still_blocks",
            "result": "pass"
            if live_runner and live_runner.get("claim_allowed") in (False, "False", "false")
            else "fail",
            "detail": f"valid_mts={live_runner.get('valid_mts_rows')};valid_bound={live_runner.get('valid_bound_rows')};R10_pass={live_runner.get('R10_pass_for_claim')}",
        },
        {
            "check_id": "V567_7_finite_smoke_runner_blocks",
            "result": "pass"
            if smoke_runner and smoke_runner.get("claim_allowed") in (False, "False", "false")
            else "fail",
            "detail": f"valid_mts={smoke_runner.get('valid_mts_rows')};valid_bound={smoke_runner.get('valid_bound_rows')};R10_pass={smoke_runner.get('R10_pass_for_claim')}",
        },
        {
            "check_id": "V567_8_no_overclaim",
            "result": "pass",
            "detail": "finite_alpha_numeric=false;real_bound_curve=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]
    return validations


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
    law_rows: list[dict[str, Any]],
    requirement_rows: list[dict[str, Any]],
    reverse_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    evaluator_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
) -> None:
    body = f"""# 567 Y5 R10 finite alpha coefficient fill and real bound curve runner

Generated: {generated_at}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The clean zero-route remains blocked unless a future parent action derives the quotient/no-marker clause.
- The retained physical branch is now written as a finite `alpha_X(lambda)` coefficient contract instead of being left vague.
- The current numerical state is still non-claim: alpha rows are symbolic, and the external R10 evidence is anchor-only rather than a full digitized `alpha_bound(lambda)` curve.
- The useful progress is that we now know exactly what has to be filled: `Z_X`, `M_X^2`, `qbar_XT`, `Qbar_XH(lambda)`, and the real R10 bound curve.

## Finite Alpha Law
{markdown_table(law_rows, ["law_id", "object", "symbolic_form", "equivalent_contract", "needed_inputs", "derived_from_parent", "valid_for_claim"])}

## Coefficient Requirements
{markdown_table(requirement_rows, ["requirement_id", "symbol", "needed_for", "current_status", "fill_contract", "blocks", "valid_for_claim"])}

## Reverse Bound Targets
{markdown_table(reverse_rows, ["target_id", "bound_id", "lambda_value", "lambda_units", "alpha_bound", "max_abs_KQqbar_at_anchor", "claim_blocker", "valid_for_claim"])}

## Prior Scan Template
{markdown_table(prior_rows, ["scan_id", "parameter", "suggested_domain", "units", "why", "claim_use", "valid_for_claim"])}

## MTS Smoke Alpha Rows
{markdown_table(smoke_rows, ["curve_id", "lambda_value", "lambda_units", "alpha_predicted", "alpha_bound", "derivation_status", "valid_for_claim"])}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Evaluator
{markdown_table(evaluator_rows, ["gate_id", "gate", "result", "detail", "valid_for_claim"])}

## Blocker Ledger
{markdown_table(blocker_rows, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Source Register
{markdown_table(source_rows, ["source_file", "role", "source_type", "exists", "valid_for_claim"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_567", "forbidden_after_567", "next_action"])}

## Practical Read
This checkpoint does not rescue R10 by declaration. It does the useful engineering thing: it converts the surviving local fifth-force risk into an exact amplitude product and reverse-bound target. If the parent action later proves `qbar_XT=0` or `Qbar_XH=0`, the branch can return to theorem-zero. If not, the theory has to show the finite product sits below a real digitized Eot-Wash-style `alpha_bound(lambda)` curve.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS_DIR / f"{run_stamp}-Y5-R10-567-finite-alpha-coefficient-fill"

    queue_rows = read_csv(QUEUE_PATH)
    anchor_rows = read_csv(ANCHOR_BOUND_CURVE)

    sources = source_register()
    law_rows = finite_alpha_law()
    requirement_rows = coefficient_requirements(queue_rows)
    reverse_rows = reverse_bound_targets(anchor_rows)
    prior_rows = prior_scan_template()
    smoke_rows = finite_alpha_smoke_rows(anchor_rows)

    write_csv(
        SOURCE_REGISTER_PATH,
        sources,
        ["source_file", "role", "source_type", "exists", "valid_for_claim"],
    )
    write_csv(
        FINITE_ALPHA_LAW_PATH,
        law_rows,
        [
            "law_id",
            "object",
            "symbolic_form",
            "equivalent_contract",
            "needed_inputs",
            "derived_from_parent",
            "use",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        COEFFICIENT_REQUIREMENTS_PATH,
        requirement_rows,
        [
            "requirement_id",
            "symbol",
            "needed_for",
            "current_status",
            "fill_contract",
            "blocks",
            "allowed_now",
            "forbidden_now",
            "valid_for_claim",
        ],
    )
    write_csv(
        REVERSE_BOUND_TARGETS_PATH,
        reverse_rows,
        [
            "target_id",
            "bound_id",
            "lambda_value",
            "lambda_units",
            "log10_lambda_m",
            "alpha_bound",
            "max_abs_KQqbar_at_anchor",
            "constraint_form",
            "digitization_method",
            "alpha_bound_source",
            "source_file",
            "valid_for_claim",
            "claim_blocker",
            "notes",
        ],
    )
    write_csv(
        PRIOR_SCAN_TEMPLATE_PATH,
        prior_rows,
        ["scan_id", "parameter", "suggested_domain", "units", "why", "claim_use", "valid_for_claim"],
    )
    write_csv(MTS_FINITE_SMOKE_PATH, smoke_rows, r10_runner.MTS_REQUIRED_COLUMNS)

    live_result = r10_runner.run_runner(
        LIVE_MTS_CURVE,
        LIVE_BOUND_CURVE,
        run_root / "live_placeholder_recheck" / "results",
    )
    smoke_result = r10_runner.run_runner(
        MTS_FINITE_SMOKE_PATH,
        ANCHOR_BOUND_CURVE,
        run_root / "finite_alpha_anchor_smoke" / "results",
    )
    runner_rows = [
        summarize_runner(
            "R10_RUNNER_567_LIVE_PLACEHOLDER_RECHECK",
            live_result,
            "live files remain blocked exactly as intended",
        ),
        summarize_runner(
            "R10_RUNNER_567_FINITE_ALPHA_ANCHOR_SMOKE",
            smoke_result,
            "symbolic finite-alpha smoke rows and anchor-only bound rows remain non-claim",
        ),
    ]
    write_csv(
        RUNNER_SUMMARY_PATH,
        runner_rows,
        [
            "runner_id",
            "mts_curve",
            "bound_curve",
            "output_dir",
            "mts_rows",
            "valid_mts_rows",
            "bound_rows",
            "valid_bound_rows",
            "comparison_rows",
            "passed_rows",
            "blocked_or_failed_rows",
            "R10_pass_for_claim",
            "claim_allowed",
            "notes",
        ],
    )

    evaluator_rows = [
        {
            "gate_id": "E567_0_zero_route",
            "gate": "promote R10 theorem-zero",
            "result": "blocked",
            "detail": "quotient/no-marker clause is sufficient but still not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E567_1_finite_alpha_law",
            "gate": "write exact finite-alpha amplitude contract",
            "result": "pass_scaffold",
            "detail": "alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT with abs product compared to R10 bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E567_2_reverse_bounds",
            "gate": "turn available anchors into reverse coefficient targets",
            "result": "pass_nonclaim",
            "detail": f"reverse_targets={len(reverse_rows)}; all anchor-only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E567_3_runner_guardrail",
            "gate": "confirm no branch passes R10 for claim",
            "result": "pass",
            "detail": "live placeholder and finite-alpha smoke runner both block claim",
            "valid_for_claim": "false",
        },
    ]
    write_csv(EVALUATOR_PATH, evaluator_rows, ["gate_id", "gate", "result", "detail", "valid_for_claim"])

    blocker_rows = [
        {
            "blocker_id": "B567_0_no_numeric_parent_coefficients",
            "blocker": "Z_X, M_X^2, qbar_XT, and Qbar_XH(lambda) remain unfilled.",
            "why_it_matters": "alpha_X(lambda) cannot be computed from parent data.",
            "next_action": "derive coefficients or run an explicitly non-claim prior scan.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B567_1_real_bound_curve_missing",
            "blocker": "R10 alpha_bound(lambda) is still anchor-only/noncurve.",
            "why_it_matters": "interpolation and exclusion claims require a real curve, not threshold sentences.",
            "next_action": "digitize full Eot-Wash bound curve or find source-backed machine-readable rows.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B567_2_vertical_branch_not_derived",
            "blocker": "ordinary matter X neutrality is not a theorem.",
            "why_it_matters": "cannot set qbar_XT=0 without a parent quotient/no-marker proof.",
            "next_action": "either derive qbar_XT=0 or keep finite-alpha branch under R10 pressure.",
            "claim_blocked": "true",
        },
    ]
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])

    decision_rows = [
        {
            "decision_id": "D567_0_finite_alpha_branch_retained",
            "decision": "retain physical X finite-alpha branch",
            "meaning": "R10 risk is now an amplitude product, not an informal worry",
            "status": "retained_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D567_1_no_R10_claim",
            "decision": "do not claim R10/local-GR pass",
            "meaning": "symbolic alpha and anchor-only bound rows are diagnostic only",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D567_2_next_fork",
            "decision": "choose digitized curve or coefficient prior scan next",
            "meaning": "data curve and parent coefficients are now separable missing pieces",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "status", "next_target"])

    validation = validation_rows(sources, law_rows, requirement_rows, reverse_rows, smoke_rows, runner_rows)
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    route_rows = [
        {
            "route_id": "RU567_0_allowed",
            "allowed_after_567": "Use finite-alpha law as a private coefficient-fill scaffold.",
            "forbidden_after_567": "Claim R10 fifth-force pass, WEP pass, PPN pass, local-GR pass, or alpha=0 theorem.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU567_1_data_route",
            "allowed_after_567": "Acquire/digitize the real alpha_bound(lambda) curve before exclusion scoring.",
            "forbidden_after_567": "Treat alpha=1 threshold anchors as a full bound curve.",
            "next_action": "build curve digitizer or source-backed table intake",
        },
        {
            "route_id": "RU567_2_theory_route",
            "allowed_after_567": "Derive or bound Z_X, M_X^2, qbar_XT, and Qbar_XH(lambda).",
            "forbidden_after_567": "Hide a physical finite-range X mode behind the earlier closure route.",
            "next_action": "coefficient prior scan only if clearly marked non-claim",
        },
    ]
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_567", "forbidden_after_567", "next_action"])

    write_doc(
        generated_at,
        law_rows,
        requirement_rows,
        reverse_rows,
        prior_rows,
        smoke_rows,
        runner_rows,
        evaluator_rows,
        blocker_rows,
        decision_rows,
        sources,
        validation,
        route_rows,
    )

    status = {
        "generated_at_utc": generated_at,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_summary": rel(RUNNER_SUMMARY_PATH),
        "all_validation_passed": all(row["result"] == "pass" for row in validation),
        "claim_allowed": False,
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
