from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "614-Y5-R10-lambda-X-parent-Hessian-window-or-CX-envelope-scorecard.md"
SCRIPT_REL = "scripts/Y5_R10_lambda_X_parent_Hessian_window_or_CX_envelope_scorecard.py"
STATUS = "Y5_R10_lambda_X_parent_Hessian_law_scored_numeric_parent_ratio_still_missing"
CLAIM_CEILING = "lambda_Hessian_scorecard_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "615-Y5-R10-explicit-parent-X-block-short-range-origin-or-range-closure.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(value: float) -> str:
    return f"{value:.12e}"


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "613 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_613_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_613_NONCLAIM_SUMMARY.csv", "finite C_X lock summary"),
        ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "lambda law and mass-gap targets"),
        ("source-intake/mts_residuals/P8_Y5_R10_578_MASS_GAP_TARGETS.csv", "existing lambda/Hessian target grid"),
        ("source-intake/mts_residuals/P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv", "Hessian extraction formula"),
        ("564-Y5-R10-parent-hessian-source-zero-attempt.md", "parent Hessian source-zero attempt"),
        ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "Hessian/source obstruction"),
        ("source-intake/mts_residuals/P8_Y5_R10_612_LAMBDA_CX_CEILING_TABLE.csv", "C_X ceilings by lambda"),
        ("source-intake/mts_residuals/P8_Y5_R10_612_CX_SURVIVAL_WINDOWS.csv", "C_X survival windows"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review-candidate R10 pressure curve"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_hessian_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "HA614_0_second_variation",
            "target": "derive parent quadratic X block",
            "derived_form": "S_X^(2)=1/2 int sqrt(h)[Z_X |grad X|^2 + M_X^2 X^2] - int sqrt(h) X J_X",
            "result": "formal_Hessian_definition_recovered",
            "missing": "explicit parent Lagrangian residues that evaluate Z_X and M_X^2",
            "claim_status": "conditional_law_only",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "HA614_1_range_law",
            "target": "derive local range",
            "derived_form": "lambda_X=sqrt(Z_X/M_X^2), mu_X^2=M_X^2/Z_X",
            "result": "range_law_derived_conditionally",
            "missing": "positive parent-owned numeric or symbolic ratio M_X^2/Z_X",
            "claim_status": "law_derived_ratio_missing",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "HA614_2_positive_branch",
            "target": "local elliptic/stable finite mode",
            "derived_form": "Z_X>0 and M_X^2>0 in the same normalization convention",
            "result": "necessary_sign_gate_written",
            "missing": "same-branch second variation with sign convention fixed",
            "claim_status": "sign_gate_unfilled",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "HA614_3_numeric_ratio",
            "target": "derive numeric M_X^2/Z_X from current corpus",
            "derived_form": "not available from covariance/universality alone",
            "result": "numeric_derivation_rejected_for_now",
            "missing": "explicit parent X block or primitive curvature scale",
            "claim_status": "blocked_for_claim",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "HA614_4_scorecard_response",
            "target": "use range pressure without pretending it is a fit",
            "derived_form": "evaluate required M_X^2/Z_X and allowed |C_X| for candidate lambda windows",
            "result": "scorecard_built_not_claim",
            "missing": "parent reason for selecting a window",
            "claim_status": "private_pressure_only",
            "valid_for_claim": "false",
        },
    ]


def classify_window(lambda_um: float, max_cx: float) -> tuple[str, str, str]:
    if lambda_um <= 50:
        return (
            "short_range_forgiving",
            "R10 pressure is forgiving if the parent Hessian naturally lands here.",
            "derive short-range parent curvature or keep as nonclaim window",
        )
    if lambda_um <= 100:
        return (
            "transition_moderate",
            "finite branch can survive but large C_X needs care.",
            "derive parent ratio and C_X size together",
        )
    if max_cx <= 500:
        return (
            "trough_tight",
            "this is the dangerous R10 trough; C_X must be genuinely small.",
            "avoid by parent range derivation or prove suppression/zero",
        )
    if lambda_um >= 500:
        return (
            "longer_range_moderate_to_tight",
            "not instantly fatal, but no longer forgiving for large C_X.",
            "derive C_X below the local ceiling or move range shorter",
        )
    return (
        "mid_range_moderate",
        "C_X around hundreds is easy; thousands start to matter.",
        "derive range and finite coefficient together",
    )


def build_lambda_window_rows(target_rows: list[dict[str, str]], epsilon_shell: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in target_rows:
        lam_m = float(target["lambda_X_m"])
        lam_um = float(target["lambda_X_um"])
        alpha = float(target["alpha_bound_review_candidate"])
        max_cx = alpha / epsilon_shell
        label, interpretation, next_action = classify_window(lam_um, max_cx)
        rows.append(
            {
                "window_id": "LW614_" + target["target_id"].split("_")[-1],
                "lambda_X_m": f(lam_m),
                "lambda_X_um": target["lambda_X_um"],
                "M_X2_over_Z_X_m_minus2": target["M_X2_over_Z_X_m_minus2"],
                "canonical_m_X_eV": target["canonical_m_X_eV"],
                "alpha_bound_review_candidate": f(alpha),
                "epsilon_shell": f(epsilon_shell),
                "max_abs_CX_review_pressure": f(max_cx),
                "window_class": label,
                "interpretation": interpretation,
                "parent_relation_needed": f"M_X^2/Z_X={target['M_X2_over_Z_X_m_minus2']} m^-2",
                "next_action": next_action,
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_cx_scorecard_rows(lambda_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    scenarios = [
        ("CX614_1", 1.0, "order_one"),
        ("CX614_100", 100.0, "full_curve_safe_scale"),
        ("CX614_315", 315.4554554349, "full_curve_ceiling_scale"),
        ("CX614_1000", 1000.0, "range_window_sensitive"),
        ("CX614_10000", 10000.0, "large_finite_coefficient"),
        ("CX614_100000", 100000.0, "very_large_finite_coefficient"),
    ]
    rows: list[dict[str, object]] = []
    for scenario_id, cx_value, scenario_label in scenarios:
        pass_count = 0
        margins: list[float] = []
        passing_lambdas: list[str] = []
        failing_lambdas: list[str] = []
        worst_margin = float("inf")
        worst_lambda = ""
        for row in lambda_rows:
            max_cx = float(row["max_abs_CX_review_pressure"])
            margin = max_cx / cx_value
            margins.append(margin)
            if margin < worst_margin:
                worst_margin = margin
                worst_lambda = str(row["lambda_X_um"])
            if margin >= 1.0:
                pass_count += 1
                passing_lambdas.append(str(row["lambda_X_um"]))
            else:
                failing_lambdas.append(str(row["lambda_X_um"]))
        if pass_count == len(lambda_rows):
            verdict = "passes_all_sampled_target_windows"
        elif pass_count == 0:
            verdict = "fails_all_sampled_target_windows"
        elif cx_value <= 1000:
            verdict = "mostly_safe_except_tight_trough"
        else:
            verdict = "range_sensitive_requires_short_or_suppressed_branch"
        rows.append(
            {
                "scenario_id": scenario_id,
                "abs_CX_assumed": f(cx_value),
                "scenario_label": scenario_label,
                "sampled_windows": len(lambda_rows),
                "passing_windows": pass_count,
                "failing_windows": len(lambda_rows) - pass_count,
                "passing_lambda_um": ";".join(passing_lambdas) if passing_lambdas else "none",
                "failing_lambda_um": ";".join(failing_lambdas) if failing_lambdas else "none",
                "worst_margin_CXmax_over_CX": f(worst_margin),
                "worst_lambda_um": worst_lambda,
                "scorecard_verdict": verdict,
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_parent_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "HC614_0_same_branch_Hessian",
            "required_parent_input": "second variation of the same local branch used for matter/source analysis",
            "mathematical_form": "delta^2 S_parent -> Z_X, M_X^2, J_X",
            "acceptance_gate": "Z_X and M_X^2 come from one parent normalization, not separate fits",
            "current_status": "formula_only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "HC614_1_positive_elliptic_mode",
            "required_parent_input": "positive kinetic residue and positive mass curvature",
            "mathematical_form": "Z_X>0, M_X^2>0",
            "acceptance_gate": "no ghost/anti-elliptic local finite mode",
            "current_status": "not_evaluated",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "HC614_2_range_selection",
            "required_parent_input": "numeric or symbolic Hessian ratio with units",
            "mathematical_form": "M_X^2/Z_X = 1/lambda_X^2",
            "acceptance_gate": "selects a specific R10 bound ordinate before comparison",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "HC614_3_natural_short_range_origin",
            "required_parent_input": "reason for tens-of-microns scale if that is the surviving window",
            "mathematical_form": "M_X^2/Z_X ~ 4e8 to 3e10 m^-2",
            "acceptance_gate": "scale is derived from parent curvature/regularity, not chosen after seeing R10",
            "current_status": "open_next_target",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "HC614_4_product_pairing",
            "required_parent_input": "C_X and lambda_X from the same parent X normalization",
            "mathematical_form": "alpha_X=lambda branch = epsilon_shell*C_X(lambda_X)",
            "acceptance_gate": "field rescaling does not create fake suppression",
            "current_status": "invariant_CX_law_available_but_parent_value_missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "HC614_5_claim_wall",
            "required_parent_input": "claim-grade alpha_bound(lambda) plus parent-signed C_X and lambda_X",
            "mathematical_form": "|epsilon_shell*C_X(lambda_X)| <= alpha_bound(lambda_X)",
            "acceptance_gate": "all rows valid_for_claim=true only after data and theory provenance exist",
            "current_status": "blocked",
            "valid_for_claim": "false",
        },
    ]


def build_route_matrix_rows(lambda_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    short_rows = [row for row in lambda_rows if float(row["lambda_X_um"]) <= 50.0]
    trough_rows = [row for row in lambda_rows if row["window_class"] == "trough_tight"]
    return [
        {
            "route_id": "RM614_0_short_range_parent_origin",
            "route": "derive lambda_X in the 5.9-50 um band",
            "pressure_read": f"min_CX_ceiling_in_band={f(min(float(row['max_abs_CX_review_pressure']) for row in short_rows))}",
            "best_use": "least painful finite branch route if parent scale is natural",
            "risk": "post-hoc if no parent scale explains it",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "RM614_1_mid_long_range_suppression",
            "route": "allow lambda_X around 75-1000 um but derive small C_X",
            "pressure_read": "C_X must be below local ceiling, as low as few hundred near the trough",
            "best_use": "honest if source/test/projector suppression is parent-owned",
            "risk": "starts to look tuned if C_X is chosen only for R10",
            "next_action": "derive_CX_component_suppression_or_source_neutrality",
            "valid_for_claim": "false",
        },
        {
            "route_id": "RM614_2_trough_avoidance",
            "route": "derive parent Hessian away from lambda about 608 um",
            "pressure_read": f"trough_CX_ceiling={f(float(trough_rows[0]['max_abs_CX_review_pressure'])) if trough_rows else 'missing'}",
            "best_use": "diagnostic guardrail, not an allowed fit choice",
            "risk": "range avoidance without derivation is not evidence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "route_id": "RM614_3_theorem_zero_return",
            "route": "prove no pole, qbar_XT=0, or Qbar_XH=0",
            "pressure_read": "R10 then becomes theorem-zero, not a range score",
            "best_use": "strongest local-GR route if parent identities close",
            "risk": "previous selector/source attempts remain conditional",
            "next_action": "return_only_with_new_parent_certificate",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D614_0_range_law",
            "status": "lambda_law_derived_conditionally",
            "decision": "keep lambda_X=sqrt(Z_X/M_X^2) as the parent-Hessian range law",
            "meaning": "range is a Hessian ratio, not a free curve-fit knob",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D614_1_numeric_ratio",
            "status": STATUS,
            "decision": "do not claim a numeric M_X^2/Z_X derivation from current corpus",
            "meaning": "current parent materials give the extraction formula but not the evaluated residues",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D614_2_best_next_route",
            "status": "explicit_parent_X_block_next",
            "decision": "try to construct a parent X block with natural short-range Hessian scale",
            "meaning": "if the scale lands at tens of microns naturally, R10 becomes much less grim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D614_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "this is a range/C_X scorecard for private derivation pressure only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU614_0_allowed",
            "allowed_after_614": "use lambda/C_X scorecard to guide parent Hessian derivation",
            "forbidden_after_614": "choose lambda_X after looking at the R10 curve and call it derived",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU614_1_allowed",
            "allowed_after_614": "say tens-of-microns range is forgiving only if parent-owned",
            "forbidden_after_614": "claim R10 survival from review-candidate pressure rows",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU614_2_allowed",
            "allowed_after_614": "return to zero theorem only with new no-pole/source/test certificate",
            "forbidden_after_614": "erase finite C_X envelope because the trough is uncomfortable",
            "next_action": "keep_finite_branch_locked_until_certificate",
        },
    ]


def build_summary_rows(lambda_rows: list[dict[str, object]], cx_rows: list[dict[str, object]], summary_613: dict[str, str]) -> list[dict[str, object]]:
    short_rows = [row for row in lambda_rows if float(row["lambda_X_um"]) <= 50.0]
    tightest = min(lambda_rows, key=lambda row: float(row["max_abs_CX_review_pressure"]))
    cx1000 = next(row for row in cx_rows if row["scenario_id"] == "CX614_1000")
    cx1e5 = next(row for row in cx_rows if row["scenario_id"] == "CX614_100000")
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lambda_law": "lambda_X=sqrt(Z_X/M_X^2)",
            "numeric_parent_ratio_ready": "false",
            "short_range_min_CX_ceiling": f(min(float(row["max_abs_CX_review_pressure"]) for row in short_rows)),
            "tightest_sampled_lambda_um": tightest["lambda_X_um"],
            "tightest_sampled_CX_ceiling": tightest["max_abs_CX_review_pressure"],
            "CX1000_passing_windows": cx1000["passing_windows"],
            "CX1e5_passing_windows": cx1e5["passing_windows"],
            "finite_CX_envelope_locked": summary_613["finite_CX_envelope_locked"],
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    hessian_rows: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    cx_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    route_matrix_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    no_claim_rows = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for table in [hessian_rows, lambda_rows, cx_rows, contract_rows, route_matrix_rows, decision_rows, summary_rows]
        for row in table
    )
    numeric_lambda = all(float(row["lambda_X_m"]) > 0 and float(row["M_X2_over_Z_X_m_minus2"]) > 0 for row in lambda_rows)
    cx100 = next(row for row in cx_rows if row["scenario_id"] == "CX614_100")
    cx1000 = next(row for row in cx_rows if row["scenario_id"] == "CX614_1000")
    cx100_passes = int(cx100["passing_windows"]) == len(lambda_rows)
    cx1000_has_failures = int(cx1000["failing_windows"]) >= 1
    return [
        {"check_id": "V614_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V614_1_prior_613_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V614_2_hessian_law_retained_not_promoted", "result": "pass" if hessian_rows[3]["result"] == "numeric_derivation_rejected_for_now" else "fail", "detail": f"hessian_rows={len(hessian_rows)}"},
        {"check_id": "V614_3_lambda_scorecard_numeric", "result": "pass" if numeric_lambda and len(lambda_rows) == 11 else "fail", "detail": f"lambda_rows={len(lambda_rows)}"},
        {"check_id": "V614_4_CX_scorecard_sane", "result": "pass" if cx100_passes and cx1000_has_failures else "fail", "detail": f"cx_rows={len(cx_rows)};CX100_passes_all={cx100_passes};CX1000_has_failures={cx1000_has_failures}"},
        {"check_id": "V614_5_parent_contract_blocks_claim", "result": "pass" if contract_rows[-1]["current_status"] == "blocked" else "fail", "detail": f"contract_rows={len(contract_rows)}"},
        {"check_id": "V614_6_route_matrix_written", "result": "pass" if len(route_matrix_rows) == 4 else "fail", "detail": f"route_rows={len(route_matrix_rows)}"},
        {"check_id": "V614_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V614_8_next_target_set", "result": "pass" if decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V614_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    hessian_rows: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    cx_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    route_matrix_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_update_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 614 Y5 R10 lambda-X parent-Hessian window or C_X envelope scorecard

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The range law remains derived only conditionally: `lambda_X=sqrt(Z_X/M_X^2)`.
- The current corpus still does not evaluate the parent Hessian ratio `M_X^2/Z_X`; treating `lambda_X` as a fitted knob is forbidden.
- The scorecard says short ranges up to about `50 um` are forgiving for the locked finite `C_X` branch, while the tight sampled trough is near `{summary_rows[0]['tightest_sampled_lambda_um']} um` with `|C_X| <= {summary_rows[0]['tightest_sampled_CX_ceiling']}`.
- No R10/local-GR claim is made. This is private derivation pressure for the next parent-X-block attempt.

## Source Register
{md_table(source_register)}

## Hessian Derivation Attempt
{md_table(hessian_rows)}

## Lambda Window Scorecard
{md_table(lambda_rows)}

## C_X Scenario Scorecard
{md_table(cx_rows)}

## Parent Hessian Contract
{md_table(contract_rows)}

## Route Decision Matrix
{md_table(route_matrix_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_update_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is actually a nice tactical map. The local finite branch does not need a miracle if the parent Hessian naturally gives a short range: at `38.6 um`, the review-pressure ceiling is about `1.53e5` for `C_X`; at the trough near `608 um`, it collapses to about `315`. So the next honest move is to try to build or reject a parent `X` block whose Hessian scale is naturally tens of microns. If that cannot be derived, we need genuine `C_X` suppression or a zero theorem. No haymakers, no panic - just footwork and range control.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_613_VALIDATION.csv")
    summary_613 = read_csv(OUT / "P8_Y5_R10_613_NONCLAIM_SUMMARY.csv")[0]
    target_rows = read_csv(OUT / "P8_Y5_R10_578_MASS_GAP_TARGETS.csv")
    epsilon_shell = float(summary_613["epsilon_shell"])

    hessian_rows = build_hessian_attempt_rows()
    lambda_rows = build_lambda_window_rows(target_rows, epsilon_shell)
    cx_rows = build_cx_scorecard_rows(lambda_rows)
    contract_rows = build_parent_contract_rows()
    route_matrix_rows = build_route_matrix_rows(lambda_rows)
    decision_rows = build_decision_rows()
    route_update_rows = build_route_update_rows()
    summary_rows = build_summary_rows(lambda_rows, cx_rows, summary_613)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        hessian_rows,
        lambda_rows,
        cx_rows,
        contract_rows,
        route_matrix_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_614_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_614_HESSIAN_DERIVATION_ATTEMPT.csv", hessian_rows)
    write_csv(OUT / "P8_Y5_R10_614_LAMBDA_WINDOW_SCORECARD.csv", lambda_rows)
    write_csv(OUT / "P8_Y5_R10_614_CX_SCENARIO_SCORECARD.csv", cx_rows)
    write_csv(OUT / "P8_Y5_R10_614_PARENT_HESSIAN_CONTRACT.csv", contract_rows)
    write_csv(OUT / "P8_Y5_R10_614_ROUTE_DECISION_MATRIX.csv", route_matrix_rows)
    write_csv(OUT / "P8_Y5_BRR545_614_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_614_ROUTE_UPDATE.csv", route_update_rows)
    write_csv(OUT / "P8_Y5_R10_614_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_614_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        hessian_rows,
        lambda_rows,
        cx_rows,
        contract_rows,
        route_matrix_rows,
        decision_rows,
        route_update_rows,
        summary_rows,
        validation_rows,
    )

    payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC),
        "validation": rel(OUT / "P8_Y5_BRR545_614_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
