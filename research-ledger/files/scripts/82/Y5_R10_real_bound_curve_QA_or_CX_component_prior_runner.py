from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner"
DOC_PATH = ROOT / "611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_611_SOURCE_REGISTER.csv"
BOUND_QA_PATH = RESIDUALS / "P8_Y5_R10_611_BOUND_CURVE_QA.csv"
CURVE_STATS_PATH = RESIDUALS / "P8_Y5_R10_611_REVIEW_CURVE_STATS.csv"
CX_PRIOR_GRID_PATH = RESIDUALS / "P8_Y5_R10_611_CX_PRIOR_GRID.csv"
COMPONENT_PRIOR_PATH = RESIDUALS / "P8_Y5_R10_611_CX_COMPONENT_PRIOR_RUNNER.csv"
LAMBDA_WINDOWS_PATH = RESIDUALS / "P8_Y5_R10_611_ALLOWED_LAMBDA_WINDOWS.csv"
MTS_PRIOR_CURVE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_611_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_611_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_611_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_611_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_611_VALIDATION.csv"

PRIOR_610_VALIDATION = RESIDUALS / "P8_Y5_BRR545_610_VALIDATION.csv"
VECTOR_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
LIVE_MTS = RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv"
LIVE_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
QA570 = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv"
SUMMARY570 = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"

STATUS = "Y5_R10_review_curve_QA_and_CX_prior_runner_built_nonclaim_real_claim_still_blocked"
CLAIM_CEILING = "review_candidate_curve_and_CX_prior_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md"
EPSILON_SHELL = 7.432631961576971e-06

SOURCE_FILES = [
    ("610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md", "immediate 610 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_610_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_610_FINITE_P1_COEFFICIENT_ENVELOPE.csv", "finite p1 law"),
    ("source-intake/mts_residuals/P8_Y5_R10_610_ALPHA_PRESSURE_ENVELOPE.csv", "anchor-only pressure grid"),
    ("source-intake/mts_residuals/P8_Y5_R10_610_COMPONENT_BUDGET_SCENARIOS.csv", "component budget seed"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review candidate curve"),
    ("source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv", "prior candidate QA"),
    ("source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv", "prior candidate curve summary"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor-only nonclaim rows"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
    ("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv", "live MTS placeholder kept unchanged"),
    ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "lambda target lineage"),
    ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "C_X source/test factorization"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_real_bound_curve_QA_or_CX_component_prior_runner.py", "this checkpoint generator"),
]

MTS_REQUIRED_FIELDS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def vector_points() -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for row in read_csv(VECTOR_CURVE):
        lam = parse_float(row.get("lambda_value", ""))
        alpha = parse_float(row.get("alpha_bound", ""))
        if lam is None or alpha is None:
            continue
        points.append({**row, "lambda_m": lam, "alpha_bound_float": alpha})
    return sorted(points, key=lambda item: item["lambda_m"])


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_bound_qa_rows(points: list[dict[str, Any]]) -> list[dict[str, str]]:
    all_rows = read_csv(VECTOR_CURVE)
    claim_rows = [row for row in all_rows if is_true(row.get("valid_for_claim", ""))]
    missing_markers = [
        row.get("bound_id", f"row_{idx}")
        for idx, row in enumerate(all_rows)
        if "MISSING" in json.dumps(row, sort_keys=True)
    ]
    source_paths = sorted({row.get("source_file", "") for row in all_rows if row.get("source_file", "")})
    render_paths = sorted({row.get("render_file", "") for row in all_rows if row.get("render_file", "")})
    source_missing = [path for path in source_paths if path and not (ROOT / path).exists()]
    render_missing = [path for path in render_paths if path and not (ROOT / path).exists()]
    positive_numeric = all(point["lambda_m"] > 0 and point["alpha_bound_float"] > 0 for point in points)
    monotonic_lambda = all(points[i]["lambda_m"] <= points[i + 1]["lambda_m"] for i in range(len(points) - 1))
    anchor_target = 3.86e-5
    nearest = min(points, key=lambda point: abs(math.log(point["lambda_m"]) - math.log(anchor_target))) if points else {}
    anchor_alpha = nearest.get("alpha_bound_float", math.nan)
    anchor_lambda = nearest.get("lambda_m", math.nan)
    anchor_log_error = abs(math.log10(anchor_alpha) - math.log10(1.0)) if anchor_alpha > 0 else math.inf
    anchor_rel_error = abs(anchor_lambda - anchor_target) / anchor_target if anchor_lambda else math.inf
    prior_qa = read_csv(QA570)
    prior_anchor_pass = any(row.get("qa_id") == "QA570_1_anchor_recovery" and "pass" in row.get("result", "") for row in prior_qa)
    return [
        {
            "qa_id": "QA611_0_schema_rows",
            "check": "review candidate file has parseable rows",
            "result": "pass" if len(all_rows) == len(points) and len(points) > 0 else "fail",
            "detail": f"raw_rows={len(all_rows)};numeric_points={len(points)}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_1_positive_numeric",
            "check": "lambda and alpha are positive numeric",
            "result": "pass" if positive_numeric else "fail",
            "detail": f"positive_numeric={positive_numeric}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_2_lambda_order",
            "check": "lambda values can be sorted into a monotonic curve",
            "result": "pass" if monotonic_lambda else "fail",
            "detail": f"lambda_min={points[0]['lambda_m'] if points else ''};lambda_max={points[-1]['lambda_m'] if points else ''}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_3_no_missing_markers",
            "check": "review rows contain no MISSING markers",
            "result": "pass" if not missing_markers else "fail",
            "detail": f"missing_marker_rows={len(missing_markers)}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_4_source_assets_exist",
            "check": "local figure source and render assets exist",
            "result": "pass" if not source_missing and not render_missing else "fail",
            "detail": f"source_missing={len(source_missing)};render_missing={len(render_missing)}",
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_5_anchor_recovery",
            "check": "nearest review point recovers alpha~1 at 38.6um",
            "result": "pass_review_candidate" if anchor_log_error < 0.01 and anchor_rel_error < 0.01 and prior_anchor_pass else "fail",
            "detail": (
                f"nearest_bound_id={nearest.get('bound_id','')};lambda={anchor_lambda:.12e};"
                f"alpha={anchor_alpha:.12e};lambda_rel_error={anchor_rel_error:.12e};alpha_log10_error={anchor_log_error:.12e};prior_570={prior_anchor_pass}"
            ),
            "valid_for_claim": "false",
        },
        {
            "qa_id": "QA611_6_nonclaim_guard",
            "check": "review candidate remains nonclaim",
            "result": "pass" if len(claim_rows) == 0 else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
            "valid_for_claim": "false",
        },
    ]


def make_curve_stats_rows(points: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not points:
        return []
    min_alpha_point = min(points, key=lambda point: point["alpha_bound_float"])
    max_alpha_point = max(points, key=lambda point: point["alpha_bound_float"])
    return [
        {
            "stat_id": "CS611_0_rows",
            "metric": "review_candidate_rows",
            "value": str(len(points)),
            "units": "rows",
            "valid_for_claim": "false",
            "notes": "review-candidate curve only; not live claim curve",
        },
        {
            "stat_id": "CS611_1_lambda_range",
            "metric": "lambda_min_to_max",
            "value": f"{points[0]['lambda_m']:.15g}..{points[-1]['lambda_m']:.15g}",
            "units": "m",
            "valid_for_claim": "false",
            "notes": f"source rows {points[0].get('bound_id','')} to {points[-1].get('bound_id','')}",
        },
        {
            "stat_id": "CS611_2_alpha_range",
            "metric": "alpha_bound_min_to_max",
            "value": f"{min_alpha_point['alpha_bound_float']:.15g}..{max_alpha_point['alpha_bound_float']:.15g}",
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": f"min at lambda={min_alpha_point['lambda_m']:.15g}; max at lambda={max_alpha_point['lambda_m']:.15g}",
        },
        {
            "stat_id": "CS611_3_tightest_candidate_bound",
            "metric": "tightest_candidate_bound",
            "value": f"{min_alpha_point['alpha_bound_float']:.15g}",
            "units": "dimensionless",
            "valid_for_claim": "false",
            "notes": f"lambda={min_alpha_point['lambda_m']:.15g}; diagnostic only",
        },
    ]


def allowed_intervals(points: list[dict[str, Any]], alpha_predicted: float) -> list[tuple[float, float]]:
    intervals: list[tuple[float, float]] = []
    start: float | None = None
    previous: float | None = None
    for point in points:
        ok = alpha_predicted <= point["alpha_bound_float"]
        lam = point["lambda_m"]
        if ok and start is None:
            start = lam
        if not ok and start is not None and previous is not None:
            intervals.append((start, previous))
            start = None
        previous = lam
    if start is not None and previous is not None:
        intervals.append((start, previous))
    return intervals


def format_intervals(intervals: list[tuple[float, float]], limit: int = 8) -> str:
    if not intervals:
        return ""
    shown = [f"{left:.6e}..{right:.6e}" for left, right in intervals[:limit]]
    extra = len(intervals) - limit
    if extra > 0:
        shown.append(f"...(+{extra} more)")
    return ";".join(shown)


def make_cx_prior_grid_rows(points: list[dict[str, Any]]) -> list[dict[str, str]]:
    c_values = [1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 1e5, 1.345418426702e5, 1e6]
    rows: list[dict[str, str]] = []
    total = len(points)
    for c_value in c_values:
        alpha_predicted = EPSILON_SHELL * c_value
        passing_points = [point for point in points if alpha_predicted <= point["alpha_bound_float"]]
        intervals = allowed_intervals(points, alpha_predicted)
        rows.append(
            {
                "grid_id": f"CX611_C{c_value:.6g}".replace("+", ""),
                "abs_CX_trial": f"{c_value:.12e}",
                "epsilon_shell": f"{EPSILON_SHELL:.12e}",
                "alpha_predicted_p1": f"{alpha_predicted:.12e}",
                "review_candidate_points": str(total),
                "passing_points": str(len(passing_points)),
                "passing_fraction": f"{(len(passing_points) / total if total else 0):.12e}",
                "allowed_lambda_intervals_m_review_candidate": format_intervals(intervals),
                "number_of_intervals": str(len(intervals)),
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_component_prior_rows(points: list[dict[str, Any]]) -> list[dict[str, str]]:
    min_alpha = min((point["alpha_bound_float"] for point in points), default=1.0)
    scenarios = [
        ("unit_source_unit_test", 1.0, 1.0),
        ("weak_test_1e_minus_2", 1.0, 1e-2),
        ("weak_source_1e_minus_2", 1e-2, 1.0),
        ("both_1e_minus_2", 1e-2, 1e-2),
        ("both_1e_minus_3", 1e-3, 1e-3),
        ("source_screened_1e_minus_4_test_unit", 1e-4, 1.0),
        ("test_screened_1e_minus_4_source_unit", 1.0, 1e-4),
    ]
    rows: list[dict[str, str]] = []
    for scenario_id, q_source, q_test in scenarios:
        product = q_source * q_test
        max_norm = min_alpha / (EPSILON_SHELL * product) if product > 0 else math.inf
        rows.append(
            {
                "scenario_id": f"CPR611_{scenario_id}",
                "Qbar_XH_trial": f"{q_source:.12e}",
                "qbar_XT_trial": f"{q_test:.12e}",
                "source_test_product": f"{product:.12e}",
                "tightest_review_alpha_bound": f"{min_alpha:.12e}",
                "max_abs_normalization_factor_review_candidate": f"{max_norm:.12e}",
                "formula": "abs(kappa_norm)*Qbar_XH*qbar_XT*epsilon_shell <= min(alpha_bound_review)",
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_lambda_window_rows(cx_grid_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in cx_grid_rows:
        rows.append(
            {
                "window_id": row["grid_id"].replace("CX611", "LW611"),
                "abs_CX_trial": row["abs_CX_trial"],
                "alpha_predicted_p1": row["alpha_predicted_p1"],
                "passing_fraction": row["passing_fraction"],
                "number_of_intervals": row["number_of_intervals"],
                "allowed_lambda_intervals_m_review_candidate": row["allowed_lambda_intervals_m_review_candidate"],
                "claim_status": "review_candidate_nonclaim_pressure",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_mts_prior_rows(cx_grid_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    anchors = read_csv(ANCHOR_BOUND)
    cx_subset = [row for row in cx_grid_rows if row["abs_CX_trial"] in {"1.000000000000e+00", "1.000000000000e+03", "1.000000000000e+05"}]
    rows: list[dict[str, str]] = []
    for anchor in anchors:
        for grid in cx_subset:
            rows.append(
                {
                    "model_id": "MTS_finite_p1_prior_nonclaim",
                    "branch_id": f"R10_finite_p1_CX_{grid['abs_CX_trial']}",
                    "curve_id": "R10_alpha_lambda_curve_MTS_FINITE_P1_NUMERIC_PRIOR_NONCLAIM",
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", "m"),
                    "alpha_predicted": grid["alpha_predicted_p1"],
                    "alpha_bound": anchor.get("alpha_bound", "1.0"),
                    "alpha_bound_source": f"source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::{anchor.get('bound_id', '')}",
                    "force_law_form": "Yukawa_potential_alpha",
                    "derivation_status": "numeric_prior_nonclaim_not_parent_sourced",
                    "formula_reference": "611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md::CX611",
                    "source_file": "611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md",
                    "assumptions": "C_X_trial_grid_not_parent_sourced;anchor_bound_only;valid_for_claim_false",
                    "valid_for_claim": "false",
                    "notes": "Diagnostic numeric prior only; runner must reject because rows are not parent-sourced claim rows.",
                }
            )
    return rows


def make_runner_summary(run_result: dict[str, Any]) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_611_NUMERIC_PRIOR_RECHECK",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "mts_rows": str(status["mts_rows"]),
            "valid_mts_rows": str(status["valid_mts_rows"]),
            "bound_rows": str(status["bound_rows"]),
            "valid_bound_rows": str(status["valid_bound_rows"]),
            "comparison_rows": str(status["comparison_rows"]),
            "passed_rows": str(status["passed_rows"]),
            "blocked_or_failed_rows": str(status["blocked_or_failed_rows"]),
            "R10_pass_for_claim": str(status["R10_pass_for_claim"]),
            "claim_allowed": str(status["claim_allowed"]),
            "notes": "required blocked result: numeric priors and review/anchor bounds are nonclaim",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D611_0_review_curve",
            "status": "review_candidate_QA_pass_nonclaim",
            "decision": "use vector curve only as private pressure data",
            "meaning": "good enough for internal C_X pressure, not enough for public R10 claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D611_1_CX_prior",
            "status": "component_prior_runner_built",
            "decision": "use C_X prior grid to size finite p1 branch",
            "meaning": "the branch is now executable as pressure before parent coefficients exist",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D611_2_next_gate",
            "status": "data_or_theory_fork",
            "decision": "next choose real bound-curve promotion or C_X component derivation",
            "meaning": "both are now explicit; neither is claim-ready",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D611_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "review candidates and priors are not evidence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU611_0_data_route",
            "allowed_after_611": "promote real bound curve only after human/independent QA or official table",
            "forbidden_after_611": "copy review candidate into live claim curve",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU611_1_theory_route",
            "allowed_after_611": "derive C_X components or set source/test zero factors",
            "forbidden_after_611": "treat C_X priors as parent coefficients",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU611_2_runner_route",
            "allowed_after_611": "use nonclaim runner rows for schema/failure-mode checks",
            "forbidden_after_611": "declare R10 pass from any valid_for_claim=false row",
            "next_action": "keep all diagnostics private until claim rows are real",
        },
    ]


def make_summary_rows(points: list[dict[str, Any]], cx_grid_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    strongest_pass = [
        row for row in cx_grid_rows if row["passing_fraction"] == "1.000000000000e+00"
    ]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": f"{EPSILON_SHELL:.15g}",
            "review_candidate_rows": str(len(points)),
            "largest_CX_full_candidate_pass": strongest_pass[-1]["abs_CX_trial"] if strongest_pass else "",
            "real_bound_curve_claim_ready": "false",
            "CX_parent_coefficients_ready": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def count_claim_rows(row_sets: list[list[dict[str, Any]]]) -> int:
    return sum(1 for rows in row_sets for row in rows if is_true(str(row.get("valid_for_claim", ""))))


def make_validation_rows(
    sources: list[dict[str, str]],
    qa_rows: list[dict[str, str]],
    stats_rows: list[dict[str, str]],
    cx_grid_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    window_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_610_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    qa_failures = [row for row in qa_rows if not row["result"].startswith("pass")]
    stats_ok = len(stats_rows) >= 4
    cx_numeric = all(parse_float(row["alpha_predicted_p1"]) is not None for row in cx_grid_rows)
    component_numeric = all(parse_float(row["max_abs_normalization_factor_review_candidate"]) is not None for row in component_rows)
    windows_ok = len(window_rows) == len(cx_grid_rows) and all(row["valid_for_claim"] == "false" for row in window_rows)
    template_numeric = all(parse_float(row["alpha_predicted"]) is not None for row in mts_rows)
    template_nonclaim = all(row["valid_for_claim"] == "false" for row in mts_rows)
    live_mts_rows = read_csv(LIVE_MTS)
    live_bound_rows = read_csv(LIVE_BOUND)
    runner = runner_rows[0]
    claim_rows = count_claim_rows(
        [
            qa_rows,
            stats_rows,
            cx_grid_rows,
            component_rows,
            window_rows,
            mts_rows,
            decision_rows,
            summary_rows,
        ]
    )
    return [
        {
            "check_id": "V611_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V611_1_prior_610_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V611_2_review_curve_QA_passes_nonclaim",
            "result": "pass" if qa_rows and not qa_failures else "fail",
            "detail": f"qa_rows={len(qa_rows)};qa_failures={len(qa_failures)}",
        },
        {
            "check_id": "V611_3_curve_stats_written",
            "result": "pass" if stats_ok else "fail",
            "detail": f"stats_rows={len(stats_rows)}",
        },
        {
            "check_id": "V611_4_CX_grid_numeric_nonclaim",
            "result": "pass" if cx_grid_rows and cx_numeric and all(row["valid_for_claim"] == "false" for row in cx_grid_rows) else "fail",
            "detail": f"grid_rows={len(cx_grid_rows)};numeric={cx_numeric}",
        },
        {
            "check_id": "V611_5_component_prior_numeric_nonclaim",
            "result": "pass" if component_rows and component_numeric and all(row["valid_for_claim"] == "false" for row in component_rows) else "fail",
            "detail": f"component_rows={len(component_rows)};numeric={component_numeric}",
        },
        {
            "check_id": "V611_6_lambda_windows_written",
            "result": "pass" if windows_ok else "fail",
            "detail": f"window_rows={len(window_rows)};grid_rows={len(cx_grid_rows)}",
        },
        {
            "check_id": "V611_7_numeric_prior_template_nonclaim",
            "result": "pass" if mts_rows and template_numeric and template_nonclaim else "fail",
            "detail": f"template_rows={len(mts_rows)};numeric={template_numeric};nonclaim={template_nonclaim}",
        },
        {
            "check_id": "V611_8_runner_blocks_nonclaim_rows",
            "result": "pass"
            if runner["R10_pass_for_claim"] == "False"
            and runner["claim_allowed"] == "False"
            and runner["valid_mts_rows"] == "0"
            and runner["valid_bound_rows"] == "0"
            else "fail",
            "detail": (
                f"valid_mts={runner['valid_mts_rows']};valid_bound={runner['valid_bound_rows']};"
                f"R10_pass={runner['R10_pass_for_claim']};claim_allowed={runner['claim_allowed']}"
            ),
        },
        {
            "check_id": "V611_9_live_files_not_overwritten",
            "result": "pass" if len(live_mts_rows) == 2 and len(live_bound_rows) == 2 else "fail",
            "detail": f"live_mts_rows={len(live_mts_rows)};live_bound_rows={len(live_bound_rows)}",
        },
        {
            "check_id": "V611_10_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V611_11_no_R10_or_local_GR_claim",
            "result": "pass"
            if summary_rows[0]["R10_pass"] == "false"
            and summary_rows[0]["WEP_pass"] == "false"
            and summary_rows[0]["PPN_pass"] == "false"
            and summary_rows[0]["local_GR_pass"] == "false"
            else "fail",
            "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    qa_rows: list[dict[str, str]],
    stats_rows: list[dict[str, str]],
    cx_grid_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    window_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 611 Y5 R10 real-bound-curve QA or C_X component-prior runner

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The existing vector-extracted 2020 R10 curve passes internal review-candidate QA, including source/render assets and alpha=1 anchor recovery.
- It remains non-claim. It is useful pressure data, not a promoted bound curve.
- A finite `p=1` `C_X` prior runner is now wired: `alpha_X=epsilon_shell*C_X`.
- The next real wall is either promote/acquire a claim-grade bound curve or derive numeric/source-backed `C_X` components.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Bound Curve QA
{markdown_table(qa_rows, ["qa_id", "check", "result", "detail", "valid_for_claim"])}

## Review Curve Stats
{markdown_table(stats_rows, ["stat_id", "metric", "value", "units", "valid_for_claim", "notes"])}

## C_X Prior Grid
{markdown_table(cx_grid_rows, ["grid_id", "abs_CX_trial", "epsilon_shell", "alpha_predicted_p1", "review_candidate_points", "passing_points", "passing_fraction", "allowed_lambda_intervals_m_review_candidate", "number_of_intervals", "claim_status", "valid_for_claim"])}

## C_X Component Prior Runner
{markdown_table(component_rows, ["scenario_id", "Qbar_XH_trial", "qbar_XT_trial", "source_test_product", "tightest_review_alpha_bound", "max_abs_normalization_factor_review_candidate", "formula", "claim_status", "valid_for_claim"])}

## Allowed Lambda Windows
{markdown_table(window_rows, ["window_id", "abs_CX_trial", "alpha_predicted_p1", "passing_fraction", "number_of_intervals", "allowed_lambda_intervals_m_review_candidate", "claim_status", "valid_for_claim"])}

## MTS Numeric Prior Template
{markdown_table(mts_rows, MTS_REQUIRED_FIELDS)}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_611", "forbidden_after_611", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is exactly where the project becomes test-shaped. We have not won R10, but we now have a review-grade pressure curve and a finite-branch coefficient dial that can be attacked from either side. If `C_X` derives small or the range lands in a forgiving window, the branch survives a round. If it lands near the tight part of the curve with a huge `C_X`, it gets punished and we know where to repair.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"

    points = vector_points()
    sources = make_sources()
    qa_rows = make_bound_qa_rows(points)
    stats_rows = make_curve_stats_rows(points)
    cx_grid_rows = make_cx_prior_grid_rows(points)
    component_rows = make_component_prior_rows(points)
    window_rows = make_lambda_window_rows(cx_grid_rows)
    mts_rows = make_mts_prior_rows(cx_grid_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(BOUND_QA_PATH, qa_rows, ["qa_id", "check", "result", "detail", "valid_for_claim"])
    write_csv(CURVE_STATS_PATH, stats_rows, ["stat_id", "metric", "value", "units", "valid_for_claim", "notes"])
    write_csv(CX_PRIOR_GRID_PATH, cx_grid_rows, ["grid_id", "abs_CX_trial", "epsilon_shell", "alpha_predicted_p1", "review_candidate_points", "passing_points", "passing_fraction", "allowed_lambda_intervals_m_review_candidate", "number_of_intervals", "claim_status", "valid_for_claim"])
    write_csv(COMPONENT_PRIOR_PATH, component_rows, ["scenario_id", "Qbar_XH_trial", "qbar_XT_trial", "source_test_product", "tightest_review_alpha_bound", "max_abs_normalization_factor_review_candidate", "formula", "claim_status", "valid_for_claim"])
    write_csv(LAMBDA_WINDOWS_PATH, window_rows, ["window_id", "abs_CX_trial", "alpha_predicted_p1", "passing_fraction", "number_of_intervals", "allowed_lambda_intervals_m_review_candidate", "claim_status", "valid_for_claim"])
    write_csv(MTS_PRIOR_CURVE_PATH, mts_rows, MTS_REQUIRED_FIELDS)

    runner_result = run_runner(MTS_PRIOR_CURVE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result)
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    summary_rows = make_summary_rows(points, cx_grid_rows)
    validation_rows = make_validation_rows(
        sources,
        qa_rows,
        stats_rows,
        cx_grid_rows,
        component_rows,
        window_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_611", "forbidden_after_611", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "epsilon_shell", "review_candidate_rows", "largest_CX_full_candidate_pass", "real_bound_curve_claim_ready", "CX_parent_coefficients_ready", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_doc(
        generated,
        run_root,
        sources,
        qa_rows,
        stats_rows,
        cx_grid_rows,
        component_rows,
        window_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        route_rows,
        validation_rows,
    )

    status = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_status": rel(result_dir / "R10_runner_status.json"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
