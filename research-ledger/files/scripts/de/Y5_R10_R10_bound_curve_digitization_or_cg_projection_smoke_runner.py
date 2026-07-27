from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
BOUND_DIR = ROOT / "source-intake" / "local_bounds"
RUN_DIR = ROOT / "runs" / "20260606-032900-Y5-R10-629-cg-projection-smoke-runner" / "results"

DOC = ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_R10_bound_curve_digitization_or_cg_projection_smoke_runner.py"

STATUS = "Y5_R10_review_curve_and_cg_projection_smoke_runner_built_claim_still_blocked"
CLAIM_CEILING = "nonclaim_smoke_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md"

PRIOR_628_DOC = ROOT / "628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md"
PRIOR_628_VALIDATION = MTS_DIR / "P8_Y5_BRR545_628_VALIDATION.csv"
PRIOR_628_SOURCES = MTS_DIR / "P8_Y5_R10_628_EXTERNAL_SOURCE_CANDIDATES.csv"
PRIOR_628_ANCHORS = MTS_DIR / "P8_Y5_R10_628_NONCLAIM_NUMERIC_ANCHORS.csv"
PRIOR_570_DOC = ROOT / "570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md"
PRIOR_570_VALIDATION = MTS_DIR / "P8_Y5_BRR545_570_VALIDATION.csv"
PRIOR_570_QA = BOUND_DIR / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv"
PRIOR_569_PROMOTION_GATE = BOUND_DIR / "P8_Y5_R10_569_PROMOTION_GATE.csv"

REVIEW_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
LIVE_DIGITIZED_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
MTS_CG_SMOKE = MTS_DIR / "R10_alpha_lambda_curve_MTS_CG_PROJECTION_SMOKE_NONCLAIM.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_629_SOURCE_REGISTER.csv"
SOURCE_SEARCH_STATUS = MTS_DIR / "P8_Y5_R10_629_SOURCE_SEARCH_STATUS.csv"
PROMOTION_AUDIT = MTS_DIR / "P8_Y5_R10_629_R10_CURVE_PROMOTION_AUDIT.csv"
PRESSURE_SAMPLES = MTS_DIR / "P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv"
CG_CONTRACT = MTS_DIR / "P8_Y5_R10_629_CG_PROJECTION_CONTRACT.csv"
RUNNER_BLOCK_REPORT = MTS_DIR / "P8_Y5_R10_629_RUNNER_BLOCK_REPORT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_629_NONCLAIM_SUMMARY.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_629_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_629_ROUTE_UPDATE.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_629_VALIDATION.csv"

SAMPLE_LAMBDAS_M = [
    5.9e-6,
    1.0e-5,
    2.0e-5,
    3.86e-5,
    5.6e-5,
    1.0e-4,
    3.0e-4,
    6.08e-4,
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
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def load_review_curve() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(REVIEW_CURVE):
        lambda_value = parse_float(row.get("lambda_value"))
        alpha_bound = parse_float(row.get("alpha_bound"))
        if lambda_value is None or alpha_bound is None or lambda_value <= 0 or alpha_bound <= 0:
            continue
        rows.append(
            {
                **row,
                "lambda_value_float": lambda_value,
                "alpha_bound_float": alpha_bound,
                "log10_lambda": math.log10(lambda_value),
                "log10_alpha": math.log10(alpha_bound),
            }
        )
    rows.sort(key=lambda item: item["lambda_value_float"])
    return rows


def interpolate_loglog(curve_rows: list[dict[str, Any]], lambda_value: float) -> tuple[float | None, str]:
    if not curve_rows:
        return None, "missing_review_curve"
    if lambda_value < curve_rows[0]["lambda_value_float"] or lambda_value > curve_rows[-1]["lambda_value_float"]:
        return None, "lambda_outside_review_curve_range"
    for row in curve_rows:
        if math.isclose(lambda_value, row["lambda_value_float"], rel_tol=1e-12, abs_tol=0.0):
            return row["alpha_bound_float"], f"exact:{row.get('bound_id', '')}"
    for left, right in zip(curve_rows, curve_rows[1:]):
        if left["lambda_value_float"] <= lambda_value <= right["lambda_value_float"]:
            x0 = left["log10_lambda"]
            x1 = right["log10_lambda"]
            y0 = left["log10_alpha"]
            y1 = right["log10_alpha"]
            t = (math.log10(lambda_value) - x0) / (x1 - x0)
            return 10 ** (y0 + t * (y1 - y0)), f"log_interp:{left.get('bound_id', '')}->{right.get('bound_id', '')}"
    return None, "interpolation_failed"


def nearest_curve_point(curve_rows: list[dict[str, Any]], lambda_value: float) -> tuple[dict[str, Any] | None, float | None]:
    if not curve_rows:
        return None, None
    nearest = min(curve_rows, key=lambda row: abs(row["lambda_value_float"] - lambda_value))
    relative_error = abs(nearest["lambda_value_float"] - lambda_value) / lambda_value
    return nearest, relative_error


def pressure_class(alpha_bound: float | None) -> str:
    if alpha_bound is None:
        return "not_comparable"
    if alpha_bound >= 100:
        return "weak_pressure_alpha_bound_above_100"
    if alpha_bound >= 1:
        return "moderate_pressure_alpha_bound_1_to_100"
    if alpha_bound >= 0.1:
        return "strong_pressure_alpha_bound_0p1_to_1"
    if alpha_bound >= 0.01:
        return "very_strong_pressure_alpha_bound_0p01_to_0p1"
    return "knife_edge_pressure_alpha_bound_below_0p01"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_628_DOC, "immediate 628 source-acquisition checkpoint"),
        (PRIOR_628_VALIDATION, "628 validation gate"),
        (PRIOR_628_SOURCES, "external local-bound source candidates"),
        (PRIOR_628_ANCHORS, "nonclaim numeric anchors"),
        (PRIOR_570_DOC, "review-candidate R10 pressure wall"),
        (PRIOR_570_VALIDATION, "570 validation gate"),
        (PRIOR_570_QA, "review-candidate curve QA"),
        (PRIOR_569_PROMOTION_GATE, "promotion blocker gate"),
        (REVIEW_CURVE, "axis-calibrated review-candidate R10 curve"),
        (LIVE_DIGITIZED_CURVE, "live claim curve that must remain placeholder"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC629_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def source_search_status_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "search_id": "SS629_0_primary_paper",
            "target": "R10_alpha_bound_lambda",
            "status": "primary_source_located",
            "evidence": "Eot-Wash 2020 PRL/arXiv gives alpha=1 threshold and figure source for bound curve",
            "source_path_or_url": "https://arxiv.org/abs/2002.11761; https://doi.org/10.1103/PhysRevLett.124.101101",
            "consequence": "source usable for anchor and review-candidate curve, not alone a machine-ready claim curve",
            "valid_for_claim": "false",
        },
        {
            "search_id": "SS629_1_machine_table",
            "target": "full_alpha_lambda_machine_table",
            "status": "not_found_in_checkpoint",
            "evidence": "no source-backed supplemental table was promoted; existing vector extraction remains review-candidate",
            "source_path_or_url": rel(REVIEW_CURVE),
            "consequence": "do not overwrite live digitized bound file",
            "valid_for_claim": "false",
        },
        {
            "search_id": "SS629_2_review_candidate",
            "target": "axis_calibrated_vector_curve",
            "status": "available_as_private_pressure_wall",
            "evidence": f"numeric review rows={len(curve_rows)}; all rows valid_for_claim=false",
            "source_path_or_url": rel(REVIEW_CURVE),
            "consequence": "may compute private coefficient pressure samples only",
            "valid_for_claim": "false",
        },
        {
            "search_id": "SS629_3_cg_projection",
            "target": "c_g_tau_R10_projection",
            "status": "not_sourced",
            "evidence": "628 c_g/tau_R10 rows remain MISSING_PARENT_INPUT or MISSING_ARENA_PROJECTION",
            "source_path_or_url": rel(PRIOR_628_DOC),
            "consequence": "R10 runner must block any MTS claim row",
            "valid_for_claim": "false",
        },
    ]


def promotion_audit_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    promotion_rows = read_csv(PRIOR_569_PROMOTION_GATE)
    qa_rows = read_csv(PRIOR_570_QA)
    live_rows = read_csv(LIVE_DIGITIZED_CURVE)
    live_has_missing = any("MISSING" in json.dumps(row) for row in live_rows)
    candidate_claim_rows = [row for row in curve_rows if is_true(row.get("valid_for_claim"))]
    blocked_promotion = [row for row in promotion_rows if row.get("result") == "blocked"]
    return [
        {
            "audit_id": "PA629_0_candidate_numeric",
            "check": "review candidate has positive numeric lambda/alpha rows",
            "result": "pass" if len(curve_rows) >= 300 else "fail",
            "detail": f"numeric_rows={len(curve_rows)}",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PA629_1_candidate_nonclaim",
            "check": "review candidate has no claim rows",
            "result": "pass" if not candidate_claim_rows else "fail",
            "detail": f"claim_rows={len(candidate_claim_rows)}",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PA629_2_anchor_qa",
            "check": "570 anchor QA remains review-only",
            "result": "pass" if any(row.get("qa_id") == "QA570_1_anchor_recovery" for row in qa_rows) else "fail",
            "detail": ";".join(f"{row.get('qa_id')}={row.get('result')}" for row in qa_rows),
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PA629_3_promotion_blocker",
            "check": "supplement/human QA and live-file promotion remain blocked",
            "result": "pass" if len(blocked_promotion) >= 2 else "fail",
            "detail": f"blocked_rows={len(blocked_promotion)}",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PA629_4_live_claim_file",
            "check": "live digitized bound file remains placeholder",
            "result": "pass" if live_has_missing else "fail",
            "detail": f"live_rows={len(live_rows)};contains_missing_marker={bool_text(live_has_missing)}",
            "valid_for_claim": "false",
        },
    ]


def pressure_sample_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lambda_value in enumerate(SAMPLE_LAMBDAS_M):
        nearest, relative_error = nearest_curve_point(curve_rows, lambda_value)
        if nearest is not None and relative_error is not None and relative_error < 0.005:
            alpha_bound = nearest["alpha_bound_float"]
            method = f"nearest_review_point:{nearest.get('bound_id', '')};lambda_relative_error={relative_error:.6g}"
        else:
            alpha_bound, method = interpolate_loglog(curve_rows, lambda_value)
        rows.append(
            {
                "sample_id": f"PS629_{index}",
                "lambda_value": f"{lambda_value:.12g}",
                "lambda_units": "m",
                "alpha_bound_review_candidate": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "interpolation_method": method,
                "pressure_class": pressure_class(alpha_bound),
                "future_pass_condition": "abs(alpha_MTS_R10(lambda))<=alpha_bound(lambda)",
                "max_abs_effective_product": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "promotion_status": "review_candidate_private_pressure_only",
                "valid_for_claim": "false",
                "notes": "Nonclaim sample from review-candidate vector curve; do not treat as live R10 evidence.",
            }
        )
    return rows


def cg_projection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CG629_0_effective_alpha",
            "object": "alpha_MTS_R10(lambda)",
            "required_value": "numeric_or_theorem_zero",
            "status": "blocked_symbolic",
            "formula_or_condition": "alpha_MTS_R10(lambda)=abs(c_g*tau_R10(lambda)*K_X*Qbar_XH(lambda;lambda_X)*qbar_XT/Z_eff)",
            "source_requirement": "parent action must define c_g, Z_eff, source/test charges, and R10 projection map",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CG629_1_zero_route",
            "object": "Z_cg or c_g",
            "required_value": "Z_cg=true with c_g=0, or sourced numeric c_g",
            "status": "not_signed",
            "formula_or_condition": "if c_g=0 by parent geometry, alpha_MTS_R10(lambda)=0 for all lambda",
            "source_requirement": "quotient-invariant matter action plus no representative Weyl/disformal residue",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CG629_2_projection",
            "object": "tau_R10(lambda)",
            "required_value": "dimensionless apparatus projection",
            "status": "missing_arena_projection",
            "formula_or_condition": "tau_R10 must map parent local mode into Yukawa-alpha observable for the Eot-Wash source/detector geometry",
            "source_requirement": "derive from local profile, material coupling, and experimental source geometry",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CG629_3_range",
            "object": "lambda_X",
            "required_value": "positive numeric meters or no-range theorem",
            "status": "missing_parent_hessian",
            "formula_or_condition": "lambda_X=sqrt(Z_X/M_X^2)",
            "source_requirement": "parent Hessian/eigenvalue block for the local residual mode",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CG629_4_profile",
            "object": "Qbar_XH(lambda;lambda_X)",
            "required_value": "source/profile response",
            "status": "missing_profile_map",
            "formula_or_condition": "Qbar_XH must be evaluated on the R10 source geometry and local transition profile",
            "source_requirement": "derive from local compact-shell/profile solution or demote to explicit empirical closure",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CG629_5_claim_gate",
            "object": "R10 pass",
            "required_value": "all valid physical rows satisfy bound",
            "status": "blocked",
            "formula_or_condition": "abs(alpha_MTS_R10(lambda_i))<=alpha_bound(lambda_i) for all source-backed curve rows",
            "source_requirement": "valid physical MTS alpha rows plus promoted source-backed bound curve",
            "valid_for_claim": "false",
        },
    ]


def mts_cg_smoke_rows(pressure_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(pressure_rows):
        rows.append(
            {
                "model_id": "MTS_local_cg_projection_smoke_nonclaim",
                "branch_id": f"MTS_CG_SMOKE_629_{index}",
                "curve_id": "R10_alpha_lambda_curve_MTS_CG_PROJECTION_SMOKE_NONCLAIM",
                "lambda_value": row["lambda_value"],
                "lambda_units": "m",
                "alpha_predicted": "abs(c_g*tau_R10(lambda)*K_X*Qbar_XH(lambda;lambda_X)*qbar_XT/Z_eff)",
                "alpha_bound": row["alpha_bound_review_candidate"],
                "alpha_bound_source": f"{rel(REVIEW_CURVE)}::{row['sample_id']}",
                "force_law_form": "Yukawa_alpha_nonclaim_projection_smoke",
                "derivation_status": "symbolic_missing_c_g_tau_R10_K_X_Qbar_XH_qbar_XT_Z_eff",
                "formula_reference": f"{rel(DOC)}::CG629_0_effective_alpha",
                "source_file": rel(DOC),
                "assumptions": "review-candidate pressure sample only; no parent projection inputs are sourced",
                "valid_for_claim": "false",
                "notes": "Runner smoke row deliberately symbolic and invalid for claim scoring.",
            }
        )
    return rows


def runner_block_report_rows(runner_result: dict[str, Any]) -> list[dict[str, Any]]:
    status = runner_result["status"]
    mts_issues: dict[str, int] = {}
    for row in runner_result["mts_validation"]:
        for issue in str(row.get("issues", "")).split(";"):
            if issue:
                mts_issues[issue] = mts_issues.get(issue, 0) + 1
    bound_issues: dict[str, int] = {}
    for row in runner_result["bound_validation"]:
        for issue in str(row.get("issues", "")).split(";"):
            if issue:
                bound_issues[issue] = bound_issues.get(issue, 0) + 1
    return [
        {
            "report_id": "RB629_0_runner_status",
            "item": "R10_alpha_lambda_bound_prediction_runner",
            "status": "blocked_as_expected" if not status["claim_allowed"] else "unexpected_claim_allowed",
            "detail": json.dumps(status, sort_keys=True),
            "valid_for_claim": "false",
        },
        {
            "report_id": "RB629_1_MTS_validation",
            "item": "MTS cg smoke rows",
            "status": "invalid_as_expected" if status["valid_mts_rows"] == 0 else "unexpected_valid_mts_rows",
            "detail": json.dumps(mts_issues, sort_keys=True),
            "valid_for_claim": "false",
        },
        {
            "report_id": "RB629_2_bound_validation",
            "item": "review candidate bound rows",
            "status": "invalid_for_claim_as_expected" if status["valid_bound_rows"] == 0 else "unexpected_valid_bound_rows",
            "detail": json.dumps(bound_issues, sort_keys=True),
            "valid_for_claim": "false",
        },
        {
            "report_id": "RB629_3_comparison",
            "item": "comparison rows",
            "status": "no_claim_comparison" if status["comparison_rows"] == 1 and status["passed_rows"] == 0 else "check_runner_output",
            "detail": f"comparison_rows={status['comparison_rows']};passed_rows={status['passed_rows']};blocked_or_failed_rows={status['blocked_or_failed_rows']}",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D629_0_smoke_runner_built",
            "decision": STATUS,
            "meaning": "R10 review curve can now be sampled against a formal c_g projection contract",
            "status": "diagnostic_progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D629_1_no_curve_promotion",
            "decision": "do_not_promote_review_curve_to_live_claim_file",
            "meaning": "supplemental table or human visual QA signoff is still missing",
            "status": "blocked_for_claim",
            "next_target": "supplement_or_manual_QA_only_if_public_R10_claim_needed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D629_2_projection_gap",
            "decision": "derive_or_bound_c_g_tau_R10_next",
            "meaning": "data side is good enough for pressure; theory side still lacks physical alpha rows",
            "status": "next_required",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D629_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no R10, local-GR, WEP, PPN, clock, or orbital pass follows from this checkpoint",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU629_0_allowed",
            "allowed_after_629": "Use review-candidate pressure samples as private coefficient targets.",
            "forbidden_after_629": "Claim R10/local-GR pass from review curve or symbolic c_g rows.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU629_1_allowed",
            "allowed_after_629": "Try to derive c_g=0 or a sourced c_g*tau_R10 projection.",
            "forbidden_after_629": "Fit c_g post hoc without a parent coefficient/projection contract.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU629_2_data_route",
            "allowed_after_629": "Promote the Eot-Wash curve only after supplement/manual QA signoff.",
            "forbidden_after_629": "Overwrite R10_alpha_lambda_bound_curve_DIGITIZED.csv with review-candidate rows.",
            "next_action": "curve promotion remains separate provenance work",
        },
    ]


def validation_rows(
    curve_rows: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    runner_result: dict[str, Any],
) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_missing = [row for row in source_rows if row["exists"] != "true"]
    prior_628_rows = read_csv(PRIOR_628_VALIDATION)
    prior_628_fail = [row for row in prior_628_rows if row.get("result") != "pass"]
    live_rows = read_csv(LIVE_DIGITIZED_CURVE)
    live_has_missing = any("MISSING" in json.dumps(row) for row in live_rows)
    anchor_nearest, anchor_relative_error = nearest_curve_point(curve_rows, 3.86e-5)
    anchor_alpha = anchor_nearest["alpha_bound_float"] if anchor_nearest else None
    anchor_ok = anchor_alpha is not None and anchor_relative_error is not None and anchor_relative_error < 0.005 and abs(math.log10(anchor_alpha)) < 0.05
    runner_status = runner_result["status"]
    return [
        {
            "check_id": "V629_0_source_paths_exist",
            "result": "pass" if not source_missing else "fail",
            "detail": f"missing={len(source_missing)}",
        },
        {
            "check_id": "V629_1_prior_628_clean",
            "result": "pass" if prior_628_rows and not prior_628_fail else "fail",
            "detail": f"prior_rows={len(prior_628_rows)};prior_fails={len(prior_628_fail)}",
        },
        {
            "check_id": "V629_2_review_curve_private_only",
            "result": "pass" if len(curve_rows) >= 300 and not [row for row in curve_rows if is_true(row.get("valid_for_claim"))] else "fail",
            "detail": f"numeric_rows={len(curve_rows)};claim_rows={len([row for row in curve_rows if is_true(row.get('valid_for_claim'))])}",
        },
        {
            "check_id": "V629_3_anchor_sample_recovers_alpha1",
            "result": "pass" if anchor_ok else "fail",
            "detail": f"lambda=3.86e-5m;nearest_candidate_alpha={anchor_alpha};relative_lambda_error={anchor_relative_error}",
        },
        {
            "check_id": "V629_4_promotion_remains_blocked",
            "result": "pass" if any(row["result"] == "pass" and row["audit_id"] == "PA629_3_promotion_blocker" for row in promotion_rows) else "fail",
            "detail": ";".join(f"{row['audit_id']}={row['result']}" for row in promotion_rows),
        },
        {
            "check_id": "V629_5_contract_blocks_claim",
            "result": "pass" if len(contract_rows) == 6 and all(row["valid_for_claim"] == "false" for row in contract_rows) else "fail",
            "detail": f"contract_rows={len(contract_rows)};claim_rows={len([row for row in contract_rows if row['valid_for_claim'] == 'true'])}",
        },
        {
            "check_id": "V629_6_smoke_runner_blocks_claim",
            "result": "pass"
            if len(smoke_rows) == len(pressure_rows)
            and runner_status["valid_mts_rows"] == 0
            and runner_status["valid_bound_rows"] == 0
            and not runner_status["claim_allowed"]
            else "fail",
            "detail": f"smoke_rows={len(smoke_rows)};valid_mts={runner_status['valid_mts_rows']};valid_bound={runner_status['valid_bound_rows']};claim_allowed={runner_status['claim_allowed']}",
        },
        {
            "check_id": "V629_7_live_claim_file_not_modified_into_claim",
            "result": "pass" if live_has_missing and not [row for row in live_rows if is_true(row.get("valid_for_claim"))] else "fail",
            "detail": f"live_rows={len(live_rows)};contains_missing={bool_text(live_has_missing)};claim_rows={len([row for row in live_rows if is_true(row.get('valid_for_claim'))])}",
        },
        {
            "check_id": "V629_8_no_local_claim",
            "result": "pass",
            "detail": "Z_cg=false;c_g=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def nonclaim_summary_rows(
    curve_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    runner_result: dict[str, Any],
) -> list[dict[str, Any]]:
    alpha_values = [parse_float(row["alpha_bound_review_candidate"]) for row in pressure_rows]
    numeric_alpha = [value for value in alpha_values if value is not None]
    tightest = min(numeric_alpha) if numeric_alpha else ""
    tightest_row = ""
    if numeric_alpha:
        tightest_index = min(range(len(pressure_rows)), key=lambda index: numeric_alpha[index] if numeric_alpha[index] is not None else float("inf"))
        tightest_row = pressure_rows[tightest_index]["lambda_value"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "review_curve_rows": len(curve_rows),
            "pressure_sample_rows": len(pressure_rows),
            "tightest_sample_alpha_bound": tightest,
            "tightest_sample_lambda_m": tightest_row,
            "runner_claim_allowed": bool_text(bool(runner_result["status"]["claim_allowed"])),
            "cg_projection_ready": "false",
            "r10_curve_promoted": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def build_doc(
    source_rows: list[dict[str, Any]],
    search_rows: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 629 Y5 R10 bound curve digitization or cg projection smoke runner",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- 629 did not promote the R10 bound curve and did not claim a local pass.\n"
            "- It built the missing bridge between the review-candidate Eot-Wash curve and the `c_g` projection contract.\n"
            "- The smoke runner correctly blocks all MTS rows because `c_g`, `tau_R10`, `K_X`, `Qbar_XH`, `qbar_XT`, `Z_eff`, and curve-promotion provenance are still not sourced.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Source Search Status\n" + markdown_table(search_rows),
            "## R10 Curve Promotion Audit\n" + markdown_table(promotion_rows),
            "## Review-Candidate Pressure Samples\n" + markdown_table(pressure_rows),
            "## c_g Projection Contract\n" + markdown_table(contract_rows),
            "## Runner Block Report\n" + markdown_table(runner_rows),
            "## Nonclaim Summary\n" + markdown_table(summary_rows),
            "## Decision\n" + markdown_table(decision_rows_),
            "## Route Update\n" + markdown_table(route_rows),
            "## Validation\n" + markdown_table(validation_rows_),
        ]
    )


def main() -> None:
    curve_rows = load_review_curve()
    source_rows = source_register_rows()
    search_rows = source_search_status_rows(curve_rows)
    promotion_rows = promotion_audit_rows(curve_rows)
    pressure_rows = pressure_sample_rows(curve_rows)
    contract_rows = cg_projection_contract_rows()
    smoke_rows = mts_cg_smoke_rows(pressure_rows)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(SOURCE_SEARCH_STATUS, search_rows)
    write_csv(PROMOTION_AUDIT, promotion_rows)
    write_csv(PRESSURE_SAMPLES, pressure_rows)
    write_csv(CG_CONTRACT, contract_rows)
    write_csv(MTS_CG_SMOKE, smoke_rows)

    runner_result = run_runner(MTS_CG_SMOKE, REVIEW_CURVE, RUN_DIR)
    runner_rows = runner_block_report_rows(runner_result)
    summary_rows = nonclaim_summary_rows(curve_rows, pressure_rows, runner_result)
    decisions = decision_rows()
    route_rows = route_update_rows()
    validations = validation_rows(curve_rows, promotion_rows, pressure_rows, contract_rows, smoke_rows, runner_result)

    write_csv(RUNNER_BLOCK_REPORT, runner_rows)
    write_csv(NONCLAIM_SUMMARY, summary_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, route_rows)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            search_rows,
            promotion_rows,
            pressure_rows,
            contract_rows,
            runner_rows,
            summary_rows,
            decisions,
            route_rows,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )

    failed = [row for row in validations if row["result"] != "pass"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "doc": str(DOC),
                "runner_output_dir": str(RUN_DIR),
                "failed_checks": failed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
