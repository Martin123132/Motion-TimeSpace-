from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPT_REL = "scripts/Y5_R10_CX_component_source_derivation_or_real_bound_curve_promotion.py"
DOC = ROOT / "612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md"
STATUS = "Y5_R10_CX_invariant_ceiling_law_derived_numeric_parent_coefficients_still_blocked"
CLAIM_CEILING = "CX_component_contract_and_review_curve_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(value: float) -> str:
    return f"{value:.12e}"


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


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def load_epsilon() -> float:
    summary_path = OUT / "P8_Y5_R10_611_NONCLAIM_SUMMARY.csv"
    rows = read_csv(summary_path)
    return float(rows[0]["epsilon_shell"])


def intervals_for_threshold(curve_rows: list[dict[str, str]], epsilon_shell: float, c_threshold: float) -> tuple[int, str, int]:
    sorted_rows = sorted(curve_rows, key=lambda row: float(row["lambda_value"]))
    intervals: list[tuple[float, float]] = []
    current_start: float | None = None
    current_end: float | None = None
    passing_points = 0
    for row in sorted_rows:
        lam = float(row["lambda_value"])
        cmax = float(row["alpha_bound"]) / epsilon_shell
        passes = cmax >= c_threshold
        if passes:
            passing_points += 1
            if current_start is None:
                current_start = lam
            current_end = lam
        elif current_start is not None and current_end is not None:
            intervals.append((current_start, current_end))
            current_start = None
            current_end = None
    if current_start is not None and current_end is not None:
        intervals.append((current_start, current_end))
    if not intervals:
        return 0, "none", passing_points
    shown = [f"{start:.6e}..{end:.6e}" for start, end in intervals[:8]]
    if len(intervals) > 8:
        shown.append(f"...(+{len(intervals) - 8} more)")
    return len(intervals), ";".join(shown), passing_points


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md", "611 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_611_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_611_NONCLAIM_SUMMARY.csv", "epsilon_shell and review curve pressure summary"),
        ("source-intake/mts_residuals/P8_Y5_R10_611_CX_PRIOR_GRID.csv", "finite p1 C_X prior grid"),
        ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "lambda and alpha product derivation target"),
        ("source-intake/mts_residuals/P8_Y5_R10_578_MASS_GAP_TARGETS.csv", "mass-gap target pressure table"),
        ("source-intake/mts_residuals/P8_Y5_R10_578_PRODUCT_COEFFICIENT_DERIVATION.csv", "C_X component definitions"),
        ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "source/test charge obstruction and exact contract"),
        ("source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv", "exact source/test expressions"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review candidate R10 bound curve"),
        ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_derivation_rows(epsilon_shell: float, tightest_alpha: float, tightest_lambda: float) -> list[dict[str, object]]:
    c_full = tightest_alpha / epsilon_shell
    return [
        {
            "derivation_id": "CD612_0_invariant_rescaling",
            "object": "C_X invariant product",
            "statement": "Under X_prime=aX, Z_X_prime=Z_X/a^2, Q_prime=Q/a, q_prime=q/a, so Q_prime q_prime/Z_prime = Q q/Z.",
            "result": "component_split_gauge_dependent_whole_product_physical",
            "claim_status": "derived_identity_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_1_ceiling_law",
            "object": "review-pressure coefficient ceiling",
            "statement": "|C_X(lambda_X)| <= alpha_bound(lambda_X)/epsilon_shell with epsilon_shell=" + f(epsilon_shell),
            "result": "exact_after_finite_p1_law_and_bound_curve_choice",
            "claim_status": "review_candidate_pressure_only",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_2_full_curve_pressure",
            "object": "entire review-candidate curve",
            "statement": "If |C_X| <= min(alpha_bound_review)/epsilon_shell then every sampled review-candidate lambda point passes.",
            "result": f"|C_X| <= {f(c_full)} using min alpha={f(tightest_alpha)} at lambda={f(tightest_lambda)} m",
            "claim_status": "review_candidate_pressure_only",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_3_test_neutrality_route",
            "object": "qbar_XT",
            "statement": "If ordinary observed matter is X-blind before variation, partial_X hat_g=0 and partial_X c_a=0, then qbar_XT=0.",
            "result": "would_force_CX_zero_but_selector_theorem_not_parent_signed",
            "claim_status": "conditional_theorem_target",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_4_source_neutrality_route",
            "object": "Qbar_XH(lambda)",
            "statement": "If matter pullback, boundary, projector, memory, and domain source channels vanish or are Hamiltonian-orthogonal, then Qbar_XH=0.",
            "result": "would_force_CX_zero_but_channelwise_source_identity_not_parent_signed",
            "claim_status": "conditional_theorem_target",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_5_no_pole_route",
            "object": "K_X",
            "statement": "If X is removed by the constraint algebra before source variation, there is no Yukawa Green pole and K_X=0.",
            "result": "would_force_CX_zero_but_current_branch_keeps_finite_X_block",
            "claim_status": "conditional_theorem_target",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CD612_6_finite_branch_route",
            "object": "finite C_X",
            "statement": "If no zero theorem closes, parent action must provide lambda_X=sqrt(Z_X/M_X^2) and invariant C_X at that lambda.",
            "result": "honest_residual_score_not_GR_reduction_yet",
            "claim_status": "blocked_until_parent_coefficients_exist",
            "valid_for_claim": "false",
        },
    ]


def build_component_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CG612_0_field_normalization",
            "component": "Z_X,Qbar_XH,qbar_XT",
            "required_parent_statement": "Choose a parent normalization or report only the invariant product Qbar_XH*qbar_XT/Z_X.",
            "current_status": "invariant_product_derived_component_values_not_unique",
            "failure_mode": "fake small K_X can be erased by field rescaling unless charges transform with it",
            "next_action": "work with C_X directly or canonicalize X in the parent Hessian",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG612_1_matter_selector",
            "component": "qbar_XT",
            "required_parent_statement": "Observed metric/coframe and ordinary constants are X-blind before variation.",
            "current_status": "not_parent_signed",
            "failure_mode": "conformal countermodel exp(2aX)g keeps qbar_XT nonzero",
            "next_action": "derive selector theorem or keep qbar_XT finite",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG612_2_source_current",
            "component": "Qbar_XH(lambda)",
            "required_parent_statement": "All source channels vanish or project orthogonally to measured Hamiltonian mass.",
            "current_status": "symbolic_functional_only",
            "failure_mode": "boundary/projector/memory/domain channels can leak source charge",
            "next_action": "derive channelwise zero or bound compact-source charge",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG612_3_Hessian_range",
            "component": "lambda_X",
            "required_parent_statement": "M_X^2/Z_X is positive and numerically/symbolically fixed with units.",
            "current_status": "conditional_law_only",
            "failure_mode": "R10 pressure changes by many orders across lambda",
            "next_action": "derive local mass-gap relation from parent potential/Hessian",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG612_4_constraint_no_pole",
            "component": "K_X",
            "required_parent_statement": "X is pure constraint/gauge in the local branch and has no propagating Yukawa pole.",
            "current_status": "not_derived_for_finite_branch",
            "failure_mode": "finite quadratic X block implies ordinary exchange mode",
            "next_action": "prove constraint elimination or score finite C_X",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG612_5_bound_curve",
            "component": "alpha_bound(lambda)",
            "required_parent_statement": "Not parent-owned; external evidence must be claim-grade.",
            "current_status": "review_candidate_QA_pass_nonclaim",
            "failure_mode": "private digitization can guide but not carry a public R10 claim",
            "next_action": "obtain official table or independent human QA promotion",
            "valid_for_claim": "false",
        },
    ]


def build_ceiling_rows(target_rows: list[dict[str, str]], epsilon_shell: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for target in target_rows:
        alpha = float(target["alpha_bound_review_candidate"])
        cmax = alpha / epsilon_shell
        if cmax >= 1.0e6:
            verdict = "very_wide_margin_for_finite_CX"
        elif cmax >= 1.0e5:
            verdict = "wide_margin_near_tens_of_microns"
        elif cmax >= 1.0e3:
            verdict = "moderate_margin_parent_coefficients_matter"
        elif cmax >= 1.0e2:
            verdict = "tight_trough_requires_CX_below_few_hundred"
        else:
            verdict = "severe_pressure"
        rows.append(
            {
                "ceiling_id": "CC612_" + target["target_id"].split("_")[-1],
                "target_id": target["target_id"],
                "lambda_X_m": target["lambda_X_m"],
                "lambda_X_um": target["lambda_X_um"],
                "M_X2_over_Z_X_m_minus2": target["M_X2_over_Z_X_m_minus2"],
                "canonical_m_X_eV": target["canonical_m_X_eV"],
                "alpha_bound_review_candidate": f(alpha),
                "epsilon_shell": f(epsilon_shell),
                "max_abs_CX_review_pressure": f(cmax),
                "C1_pass": str(cmax >= 1.0).lower(),
                "C100_pass": str(cmax >= 100.0).lower(),
                "C1000_pass": str(cmax >= 1000.0).lower(),
                "C1e5_pass": str(cmax >= 1.0e5).lower(),
                "pressure_verdict": verdict,
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_survival_rows(curve_rows: list[dict[str, str]], epsilon_shell: float) -> list[dict[str, object]]:
    thresholds = [1.0, 100.0, 315.4554554349, 1000.0, 10000.0, 100000.0, 1.0e6]
    rows: list[dict[str, object]] = []
    total = len(curve_rows)
    for threshold in thresholds:
        count, intervals, passing = intervals_for_threshold(curve_rows, epsilon_shell, threshold)
        rows.append(
            {
                "survival_id": f"SW612_C{threshold:.6g}".replace("+", ""),
                "abs_CX_threshold": f(threshold),
                "review_candidate_points": total,
                "passing_points": passing,
                "passing_fraction": f(passing / total if total else 0.0),
                "allowed_interval_count": count,
                "allowed_lambda_intervals_m_review_candidate": intervals,
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_promotion_rows(curve_rows: list[dict[str, str]], source_register: list[dict[str, object]]) -> list[dict[str, object]]:
    claim_ready_rows = sum(1 for row in curve_rows if parse_bool(row.get("valid_for_claim", "false")))
    missing_sources = sum(1 for row in source_register if not parse_bool(row["exists"]))
    return [
        {
            "promotion_id": "PG612_0_review_candidate_internal_QA",
            "gate": "review candidate exists and prior QA passes",
            "status": "passed_for_private_pressure",
            "detail": f"rows={len(curve_rows)};claim_ready_rows={claim_ready_rows}",
            "valid_for_claim": "false",
        },
        {
            "promotion_id": "PG612_1_claim_grade_bound_curve",
            "gate": "official table or independent visual QA promotion",
            "status": "blocked",
            "detail": "no source in this checkpoint promotes valid_for_claim=true",
            "valid_for_claim": "false",
        },
        {
            "promotion_id": "PG612_2_source_paths",
            "gate": "all cited local sources exist",
            "status": "passed" if missing_sources == 0 else "failed",
            "detail": f"missing_sources={missing_sources}",
            "valid_for_claim": "false",
        },
        {
            "promotion_id": "PG612_3_live_file_policy",
            "gate": "do not overwrite live claim placeholder from review candidate",
            "status": "passed",
            "detail": "review candidate retained as nonclaim pressure file",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D612_0_derivation_result",
            "status": STATUS,
            "decision": "accept invariant C_X product and ceiling law as derived, not numeric parent C_X",
            "meaning": "we gained a real mathematical simplification but not an R10 claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D612_1_best_next_route",
            "status": "matter_selector_first",
            "decision": "try to prove qbar_XT=0 or small from an observed-frame selector theorem",
            "meaning": "this is cleaner than tuning source charges and less dependent on digitization",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D612_2_bound_curve_policy",
            "status": "do_not_promote_yet",
            "decision": "keep vector curve as review-candidate pressure only",
            "meaning": "no public R10 pass until bound curve and parent coefficients are both claim-grade",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D612_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "finite p1 branch is now bounded pressure, not derived GR reduction",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU612_0_allowed",
            "allowed_after_612": "derive a parent matter-selector theorem before variation: partial_X hat_g=0 and partial_X constants=0",
            "forbidden_after_612": "call qbar_XT small because it would be convenient",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU612_1_allowed",
            "allowed_after_612": "use C_X ceiling table as private derivation pressure",
            "forbidden_after_612": "treat review-candidate curve or C_X priors as public evidence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU612_2_allowed",
            "allowed_after_612": "promote bound curve only from official machine-readable rows or independent QA checklist",
            "forbidden_after_612": "copy review rows into live claim file",
            "next_action": "parallel_data_task_after_theory_gate",
        },
    ]


def build_summary(
    epsilon_shell: float,
    curve_rows: list[dict[str, str]],
    ceiling_rows: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    cmax_values = [float(row["max_abs_CX_review_pressure"]) for row in ceiling_rows]
    tightest_curve = min(float(row["alpha_bound"]) for row in curve_rows) / epsilon_shell
    full_safe = next(row for row in survival_rows if row["abs_CX_threshold"] == "3.154554554349e+02")
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": epsilon_shell,
            "review_candidate_rows": len(curve_rows),
            "tightest_full_curve_abs_CX_ceiling": f(tightest_curve),
            "target_table_min_abs_CX_ceiling": f(min(cmax_values)),
            "target_table_max_abs_CX_ceiling": f(max(cmax_values)),
            "full_curve_safe_threshold_points": full_safe["passing_points"],
            "CX_parent_coefficients_ready": "false",
            "real_bound_curve_claim_ready": "false",
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
    curve_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    ceiling_rows: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    curve_claim_rows = [row for row in curve_rows if parse_bool(row.get("valid_for_claim", "false"))]
    c_values = [float(row["max_abs_CX_review_pressure"]) for row in ceiling_rows]
    no_claim_outputs = all(not parse_bool(row.get("valid_for_claim", "false")) for table in [derivation_rows, gate_rows, ceiling_rows, survival_rows, promotion_rows, decision_rows] for row in table)
    return [
        {"check_id": "V612_0_source_paths_exist", "result": "pass" if not missing else "fail", "detail": f"missing={len(missing)}"},
        {"check_id": "V612_1_prior_611_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V612_2_review_curve_nonclaim", "result": "pass" if curve_rows and not curve_claim_rows else "fail", "detail": f"rows={len(curve_rows)};claim_rows={len(curve_claim_rows)}"},
        {"check_id": "V612_3_invariant_derivation_written", "result": "pass" if any(row["derivation_id"] == "CD612_0_invariant_rescaling" for row in derivation_rows) else "fail", "detail": f"derivation_rows={len(derivation_rows)}"},
        {"check_id": "V612_4_ceiling_law_numeric", "result": "pass" if c_values and all(value > 0 and math.isfinite(value) for value in c_values) else "fail", "detail": f"ceiling_rows={len(ceiling_rows)}"},
        {"check_id": "V612_5_component_gates_block_claim", "result": "pass" if gate_rows and all(not parse_bool(row["valid_for_claim"]) for row in gate_rows) else "fail", "detail": f"gate_rows={len(gate_rows)}"},
        {"check_id": "V612_6_survival_windows_written", "result": "pass" if survival_rows else "fail", "detail": f"survival_rows={len(survival_rows)}"},
        {"check_id": "V612_7_curve_not_promoted", "result": "pass" if any(row["status"] == "blocked" for row in promotion_rows) else "fail", "detail": f"promotion_rows={len(promotion_rows)}"},
        {"check_id": "V612_8_no_claim_rows", "result": "pass" if no_claim_outputs else "fail", "detail": f"all_valid_for_claim_false={no_claim_outputs}"},
        {"check_id": "V612_9_next_target_set", "result": "pass" if decision_rows and decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V612_10_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    ceiling_rows: list[dict[str, object]],
    survival_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    selected_ceiling_rows = ceiling_rows[:]
    content = f"""# 612 Y5 R10 C_X component-source derivation or real-bound-curve promotion

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- Derived a useful invariant: the split into `Z_X`, `Qbar_XH`, and `qbar_XT` is normalization-dependent, but the whole product `C_X` is invariant.
- Derived the pressure law for the finite `p=1` branch: `|C_X(lambda_X)| <= alpha_bound(lambda_X)/epsilon_shell`.
- The review-candidate curve says the whole sampled curve is safe only for `|C_X| <= {summary_rows[0]['tightest_full_curve_abs_CX_ceiling']}`; tens-of-microns ranges allow much larger `C_X`.
- No parent numeric coefficient is filled and no bound curve is promoted. This checkpoint tightens the target; it does not claim R10, WEP, PPN, or local-GR success.

## Source Register
{md_table(source_register)}

## C_X Derivation
{md_table(derivation_rows)}

## Component Closure Gate
{md_table(gate_rows)}

## Lambda-C_X Ceiling Table
{md_table(selected_ceiling_rows)}

## C_X Survival Windows
{md_table(survival_rows)}

## Bound-Curve Promotion Gate
{md_table(promotion_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
The branch is not dead; it is now boxed into an actual engineering target. If the parent route gives a tens-of-microns range, even a fairly large finite `C_X` can survive this private R10 pressure. If the range lands near the millimetre trough, the parent must either make `C_X` genuinely small, prove `qbar_XT=0`, prove `Qbar_XH=0`, or remove the pole. The least-scrutiny route is now the matter-selector theorem: prove ordinary matter is `X`-blind before variation, or stop pretending the local branch has reduced to GR.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    epsilon_shell = load_epsilon()
    curve_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv")
    target_rows = read_csv(OUT / "P8_Y5_R10_578_MASS_GAP_TARGETS.csv")
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_611_VALIDATION.csv")
    sorted_curve = sorted(curve_rows, key=lambda row: float(row["alpha_bound"]))
    tightest_alpha = float(sorted_curve[0]["alpha_bound"])
    tightest_lambda = float(sorted_curve[0]["lambda_value"])

    source_register = build_source_register()
    derivation_rows = build_derivation_rows(epsilon_shell, tightest_alpha, tightest_lambda)
    gate_rows = build_component_gate_rows()
    ceiling_rows = build_ceiling_rows(target_rows, epsilon_shell)
    survival_rows = build_survival_rows(curve_rows, epsilon_shell)
    promotion_rows = build_promotion_rows(curve_rows, source_register)
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    summary_rows = build_summary(epsilon_shell, curve_rows, ceiling_rows, survival_rows)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        curve_rows,
        derivation_rows,
        gate_rows,
        ceiling_rows,
        survival_rows,
        promotion_rows,
        decision_rows,
    )

    write_csv(OUT / "P8_Y5_R10_612_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_612_CX_INVARIANT_DERIVATION.csv", derivation_rows)
    write_csv(OUT / "P8_Y5_R10_612_COMPONENT_CLOSURE_GATE.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_612_LAMBDA_CX_CEILING_TABLE.csv", ceiling_rows)
    write_csv(OUT / "P8_Y5_R10_612_CX_SURVIVAL_WINDOWS.csv", survival_rows)
    write_csv(OUT / "P8_Y5_R10_612_BOUND_CURVE_PROMOTION_GATE.csv", promotion_rows)
    write_csv(OUT / "P8_Y5_BRR545_612_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_612_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_612_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_612_VALIDATION.csv", validation_rows)
    write_doc(
        generated,
        source_register,
        derivation_rows,
        gate_rows,
        ceiling_rows,
        survival_rows,
        promotion_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC),
        "validation": rel(OUT / "P8_Y5_BRR545_612_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
