from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_real_bound_anchor_staged_nonclaim_smoke_runner_blocks_claim"
CLAIM_CEILING = "R10_real_source_anchor_and_smoke_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "564-Y5-R10-full-curve-digitization-or-parent-coefficient-fill.md"

DOC_PATH = Path("563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_563_SOURCE_REGISTER.csv")
PROVENANCE_PATH = Path("source-intake/local_bounds/P8_Y5_R10_BOUND_SOURCE_PROVENANCE.csv")
ACQUISITION_LEDGER_PATH = Path("source-intake/local_bounds/P8_Y5_R10_563_ACQUISITION_LEDGER.csv")
ANCHOR_BOUND_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv")
MTS_SMOKE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv")
RUNNER_SUMMARY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_563_RUNNER_SUMMARY.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_563_EVALUATOR.csv")
BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_563_BLOCKER_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_563_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_563_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_563_ROUTE_UPDATE.csv")

LIVE_MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
LIVE_BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")
PRIOR_VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_562_VALIDATION.csv")


SOURCE_REGISTER = [
    {
        "source_file": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "role": "immediate upstream R10 lambda/prefactor gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_562_VALIDATION.csv",
        "role": "upstream validation confirming placeholder claim remains blocked",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
        "role": "accepted contract for real bound curve rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "role": "conditional alpha(lambda) prefactor relation from 562",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "live MTS placeholder curve kept unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live bound placeholder file kept unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "symbolic local-bound source hierarchy manifest",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "existing R10 comparator reused without changing claim logic",
    },
    {
        "source_file": "scripts/Y5_R10_real_bound_curve_acquisition_and_alpha_row_smoke_runner.py",
        "role": "this private checkpoint generator",
    },
]


PROVENANCE_ROWS = [
    {
        "source_id": "EOTWASH_2020_PRL124101101",
        "title": "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
        "year": "2020",
        "source_kind": "modern_anchor",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761",
        "doi": "10.1103/PhysRevLett.124.101101",
        "extraction_method": "anchor_only_from_abstract_statement_alpha_equals_1_range_less_than_38.6_um",
        "confidence_level": "95_percent",
        "data_status": "anchor_only_non_curve",
        "confidence": "high_for_threshold_anchor_low_for_curve",
        "valid_for_claim": "false",
        "notes": "Used only as a source-backed gravitational-strength Yukawa threshold anchor; no figure digitization or machine-readable curve was acquired here.",
    },
    {
        "source_id": "EOTWASH_2007_PRL98021101",
        "title": "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale",
        "year": "2007",
        "source_kind": "continuity_anchor",
        "source_url": "https://arxiv.org/abs/hep-ph/0611184",
        "doi": "10.1103/PhysRevLett.98.021101",
        "extraction_method": "anchor_only_from_abstract_statement_abs_alpha_le_1_down_to_lambda_56_um",
        "confidence_level": "95_percent",
        "data_status": "anchor_only_non_curve",
        "confidence": "high_for_threshold_anchor_low_for_curve",
        "valid_for_claim": "false",
        "notes": "Used only as an older Eot-Wash threshold continuity anchor; not a digitized alpha(lambda) curve.",
    },
    {
        "source_id": "ADELBERGER_HECKEL_NELSON_2003_REVIEW",
        "title": "Tests of the Gravitational Inverse-Square Law",
        "year": "2003",
        "source_kind": "review_context",
        "source_url": "https://arxiv.org/abs/hep-ph/0307284",
        "doi": "10.1146/annurev.nucl.53.041002.110503",
        "extraction_method": "review_context_only_no_numeric_rows_extracted",
        "confidence_level": "not_a_new_threshold_row",
        "data_status": "review_context_no_curve",
        "confidence": "high_for_source_hierarchy_low_for_numeric_curve",
        "valid_for_claim": "false",
        "notes": "Recorded for continuity with the existing placeholder source hierarchy; no numeric bound row is created from this review in checkpoint 563.",
    },
]


ANCHOR_BOUND_ROWS = [
    {
        "bound_id": "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101",
        "lambda_value": "3.86e-5",
        "lambda_units": "m",
        "alpha_bound": "1.0",
        "alpha_bound_source": "https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
        "digitization_method": "anchor_only_non_curve_from_alpha_equals_1_threshold_statement",
        "source_file": "https://arxiv.org/abs/2002.11761",
        "valid_for_claim": "false",
        "notes": "Modern source-backed anchor only: gravitational-strength Yukawa interactions limited to ranges below 38.6 um at 95 percent confidence; not a full alpha(lambda) curve.",
    },
    {
        "bound_id": "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM",
        "dataset_id": "Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_2007_PRL98021101",
        "lambda_value": "5.6e-5",
        "lambda_units": "m",
        "alpha_bound": "1.0",
        "alpha_bound_source": "https://arxiv.org/abs/hep-ph/0611184; doi:10.1103/PhysRevLett.98.021101",
        "digitization_method": "anchor_only_non_curve_from_abs_alpha_le_1_threshold_statement",
        "source_file": "https://arxiv.org/abs/hep-ph/0611184",
        "valid_for_claim": "false",
        "notes": "Continuity anchor only: inverse-square law holds with abs(alpha)<=1 down to lambda=56 um at 95 percent confidence; not a full alpha(lambda) curve.",
    },
]


MTS_SMOKE_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "R10_symbolic_parent_prefactor_smoke",
        "curve_id": "R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM",
        "lambda_value": "3.86e-5",
        "lambda_units": "m",
        "alpha_predicted": "K_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
        "alpha_bound": "1.0",
        "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "force_law_form": "Yukawa_potential_and_acceleration_ratio",
        "derivation_status": "symbolic_prefactor_nonclaim_smoke_parent_coefficients_absent",
        "formula_reference": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md::alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT",
        "source_file": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "assumptions": "Z_X,M_X_squared,numerator_coefficients,source_paths_not_numeric_or_parent_derived",
        "valid_for_claim": "false",
        "notes": "Schema and unit smoke row only; alpha is intentionally symbolic and must remain invalid for claim scoring.",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "R10_symbolic_parent_prefactor_smoke",
        "curve_id": "R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM",
        "lambda_value": "5.6e-5",
        "lambda_units": "m",
        "alpha_predicted": "K_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
        "alpha_bound": "1.0",
        "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM",
        "force_law_form": "Yukawa_potential_and_acceleration_ratio",
        "derivation_status": "symbolic_prefactor_nonclaim_smoke_parent_coefficients_absent",
        "formula_reference": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md::lambda_X=sqrt(Z_X/M_X^2)",
        "source_file": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "assumptions": "Z_X,M_X_squared,numerator_coefficients,source_paths_not_numeric_or_parent_derived",
        "valid_for_claim": "false",
        "notes": "Second anchor-aligned smoke row; remains non-claim because parent coefficients are not sourced.",
    },
]


ACQUISITION_ROWS = [
    {
        "item": "full_2020_Eot_Wash_alpha_lambda_curve",
        "requested": "true",
        "method": "web_metadata_and_abstract_anchor_review",
        "status": "not_acquired",
        "result": "threshold anchor found; no full digitized curve extracted",
        "next_action": "digitize PRL 2020 bound figure or locate machine-readable supplementary table",
    },
    {
        "item": "older_2007_Eot_Wash_alpha_lambda_anchor",
        "requested": "true",
        "method": "arxiv_metadata_and_abstract_anchor_review",
        "status": "anchor_acquired_noncurve",
        "result": "abs(alpha)<=1 down to lambda=56um recorded as anchor-only row",
        "next_action": "use only for continuity unless full curve points are digitized",
    },
    {
        "item": "2003_Adelberger_review_continuity",
        "requested": "true",
        "method": "arxiv_metadata_review",
        "status": "recorded_no_numeric_row",
        "result": "review source recorded in provenance, no bound row created",
        "next_action": "digitize review plots only if needed for historical comparison, not modern claim",
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    columns = fieldnames or list(rows[0].keys()) if rows else fieldnames or []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, str]) -> bool:
    serialized = json.dumps(row, sort_keys=True)
    return "MISSING_" in serialized or "template_invalid" in serialized or "fill_" in serialized


def web_parts_are_recorded(source_url: str) -> bool:
    parts = [part.strip() for part in source_url.split(";") if part.strip()]
    return bool(parts) and all(part.startswith(("http://", "https://")) for part in parts)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in SOURCE_REGISTER:
        source_file = item["source_file"]
        exists = (ROOT / source_file).exists()
        rows.append(
            {
                "source_file": source_file,
                "role": item["role"],
                "exists": str(exists),
            }
        )
    return rows


def anchor_numeric_checks(rows: list[dict[str, str]]) -> tuple[bool, str]:
    issues: list[str] = []
    for row in rows:
        lambda_value = parse_float(row.get("lambda_value", ""))
        alpha_bound = parse_float(row.get("alpha_bound", ""))
        if lambda_value is None or lambda_value <= 0:
            issues.append(f"{row.get('bound_id', '')}:lambda_not_positive_numeric")
        if alpha_bound is None or alpha_bound <= 0:
            issues.append(f"{row.get('bound_id', '')}:alpha_not_positive_numeric")
        if row.get("lambda_units") not in {"m", "um", "micron", "microns"}:
            issues.append(f"{row.get('bound_id', '')}:unrecognized_units")
        if has_missing_marker(row):
            issues.append(f"{row.get('bound_id', '')}:missing_marker")
        if is_true(row.get("valid_for_claim", "")):
            issues.append(f"{row.get('bound_id', '')}:claim_flag_true")
    return not issues, ";".join(issues)


def smoke_row_checks(rows: list[dict[str, str]]) -> tuple[bool, str]:
    issues: list[str] = []
    for row in rows:
        lambda_value = parse_float(row.get("lambda_value", ""))
        if lambda_value is None or lambda_value <= 0:
            issues.append(f"{row.get('branch_id', '')}:lambda_not_positive_numeric")
        if is_true(row.get("valid_for_claim", "")):
            issues.append(f"{row.get('branch_id', '')}:claim_flag_true")
        if not str(row.get("alpha_predicted", "")).startswith("K_X*"):
            issues.append(f"{row.get('branch_id', '')}:not_symbolic_prefactor")
    return not issues, ";".join(issues)


def nonclaim_interpolation_dry_check(rows: list[dict[str, str]]) -> tuple[str, str]:
    points = sorted(
        (
            (float(row["lambda_value"]), float(row["alpha_bound"]), row["bound_id"])
            for row in rows
            if parse_float(row.get("lambda_value", "")) is not None and parse_float(row.get("alpha_bound", "")) is not None
        ),
        key=lambda item: item[0],
    )
    if len(points) < 2:
        return "blocked", "need at least two positive numeric anchors for log-interpolation smoke"
    left_lambda, left_alpha, left_id = points[0]
    right_lambda, right_alpha, right_id = points[-1]
    if left_alpha <= 0 or right_alpha <= 0 or left_lambda <= 0 or right_lambda <= 0:
        return "blocked", "nonpositive anchor blocks log interpolation"
    midpoint_lambda = math.sqrt(left_lambda * right_lambda)
    interpolation_weight = (math.log(midpoint_lambda) - math.log(left_lambda)) / (math.log(right_lambda) - math.log(left_lambda))
    log_alpha = math.log(left_alpha) + interpolation_weight * (math.log(right_alpha) - math.log(left_alpha))
    midpoint_alpha = math.exp(log_alpha)
    return "pass_nonclaim", f"{left_id}->{right_id};lambda_mid={midpoint_lambda:.6e};alpha_mid={midpoint_alpha:.6e}"


def build_runner_summary(
    live_result: dict[str, Any],
    smoke_result: dict[str, Any],
    interpolation_status: str,
    interpolation_detail: str,
) -> list[dict[str, Any]]:
    rows = []
    for runner_id, result in [
        ("R10_RUNNER_563_LIVE_PLACEHOLDER_RECHECK", live_result),
        ("R10_RUNNER_563_ANCHOR_SMOKE_RECHECK", smoke_result),
    ]:
        status = result["status"]
        rows.append(
            {
                "runner_id": runner_id,
                "mts_curve": status["mts_curve"],
                "bound_curve": status["bound_curve"],
                "mts_rows": status["mts_rows"],
                "valid_mts_rows": status["valid_mts_rows"],
                "bound_rows": status["bound_rows"],
                "valid_bound_rows": status["valid_bound_rows"],
                "comparison_rows": status["comparison_rows"],
                "passed_rows": status["passed_rows"],
                "blocked_or_failed_rows": status["blocked_or_failed_rows"],
                "R10_pass_for_claim": status["R10_pass_for_claim"],
                "claim_allowed": status["claim_allowed"],
                "notes": "existing runner result; false is required at checkpoint 563",
            }
        )
    rows.append(
        {
            "runner_id": "R10_NONCLAIM_ANCHOR_INTERPOLATION_DRY_CHECK",
            "mts_curve": rel(ROOT / MTS_SMOKE_PATH),
            "bound_curve": rel(ROOT / ANCHOR_BOUND_PATH),
            "mts_rows": len(MTS_SMOKE_ROWS),
            "valid_mts_rows": 0,
            "bound_rows": len(ANCHOR_BOUND_ROWS),
            "valid_bound_rows": 0,
            "comparison_rows": 0,
            "passed_rows": 0,
            "blocked_or_failed_rows": 1 if interpolation_status != "pass_nonclaim" else 0,
            "R10_pass_for_claim": "False",
            "claim_allowed": "False",
            "notes": f"{interpolation_status}: {interpolation_detail}",
        }
    )
    return rows


def build_evaluator(
    live_result: dict[str, Any],
    smoke_result: dict[str, Any],
    interpolation_status: str,
) -> list[dict[str, str]]:
    return [
        {
            "criterion_id": "E563_0_real_source_anchor_started",
            "criterion": "Real Eot-Wash source hierarchy is recorded with DOI/URL/year/provenance.",
            "result": "pass",
            "claim_impact": "source plumbing improved; no R10 claim",
        },
        {
            "criterion_id": "E563_1_full_curve_missing",
            "criterion": "Full alpha(lambda) curve must be digitized or table-sourced before claim scoring.",
            "result": "blocked",
            "claim_impact": "anchor-only rows are not enough for R10/local-GR pass",
        },
        {
            "criterion_id": "E563_2_mts_parent_coefficients_missing",
            "criterion": "MTS alpha rows require Z_X, M_X^2, numerator coefficients, and source-backed formula paths.",
            "result": "blocked",
            "claim_impact": "symbolic smoke rows remain non-claim",
        },
        {
            "criterion_id": "E563_3_live_runner_blocks",
            "criterion": "Existing comparator must keep live placeholder files blocked.",
            "result": "pass" if not live_result["status"]["R10_pass_for_claim"] else "fail",
            "claim_impact": "guardrail intact",
        },
        {
            "criterion_id": "E563_4_smoke_runner_blocks",
            "criterion": "Candidate/smoke files must validate failure modes and still block claims.",
            "result": "pass" if not smoke_result["status"]["R10_pass_for_claim"] else "fail",
            "claim_impact": "guardrail intact",
        },
        {
            "criterion_id": "E563_5_nonclaim_interpolation_smoke",
            "criterion": "Positive numeric anchors can be log-interpolated only as a non-claim plumbing dry check.",
            "result": "pass" if interpolation_status == "pass_nonclaim" else "blocked",
            "claim_impact": "interpolation plumbing checked without promoting anchors",
        },
    ]


def build_blocker_ledger() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "B563_0_no_full_bound_curve",
            "blocker": "Only alpha=1 threshold anchors were staged; there is no dense alpha(lambda) curve.",
            "why_it_matters": "R10 scoring needs bound strength at the MTS predicted lambda, not a single threshold sentence.",
            "next_action": "digitize 2020 PRL figure points or locate official machine-readable curve data",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B563_1_no_numeric_MTS_alpha",
            "blocker": "MTS alpha rows remain symbolic because Z_X, M_X^2, K_X, Qbar_XH, and qbar_XT are not numerically parent-sourced.",
            "why_it_matters": "The comparator cannot test abs(alpha_predicted)<=alpha_bound without numeric alpha(lambda).",
            "next_action": "derive theorem-zero source silence or fill source-backed parent coefficients",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B563_2_anchor_rows_nonclaim_by_design",
            "blocker": "Anchor rows are valid evidence provenance but invalid claim rows.",
            "why_it_matters": "A threshold anchor can guide the next data pass but cannot replace a conservative bound curve.",
            "next_action": "promote only after full-curve extraction and independent validation",
            "claim_blocked": "true",
        },
    ]


def build_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D563_0_checkpoint_status",
            "status": STATUS,
            "decision": "stage source-backed anchors and smoke alpha rows only",
            "rationale": "real sources improve plumbing, but every claim gate remains deliberately closed",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D563_1_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "do not claim R10/local-GR pass",
            "rationale": "full bound curve and parent-derived MTS alpha are both absent",
            "next_target": NEXT_TARGET,
        },
    ]


def build_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU563_0_data_route",
            "current_state": "anchor_only_noncurve_source_backed",
            "next_gate": "full_curve_digitization",
            "success_condition": "dense positive numeric lambda_value and alpha_bound rows with valid_for_claim=true only after provenance and extraction checks",
        },
        {
            "route_id": "RU563_1_theory_route",
            "current_state": "symbolic_MTS_alpha_nonclaim",
            "next_gate": "parent_coefficient_or_theorem_zero",
            "success_condition": "derive/source Z_X, M_X^2, numerator coefficients, and formula source paths, or prove no-range theorem-zero",
        },
    ]


def build_validation_rows(
    source_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    live_result: dict[str, Any],
    smoke_result: dict[str, Any],
    interpolation_status: str,
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    provenance_urls_ok = all(web_parts_are_recorded(row["source_url"]) for row in PROVENANCE_ROWS)
    anchor_ok, anchor_detail = anchor_numeric_checks(ANCHOR_BOUND_ROWS)
    smoke_ok, smoke_detail = smoke_row_checks(MTS_SMOKE_ROWS)
    live_bound_rows = read_csv(ROOT / LIVE_BOUND_CURVE_PATH)
    live_mts_rows = read_csv(ROOT / LIVE_MTS_CURVE_PATH)
    claim_rows = [
        row for row in ANCHOR_BOUND_ROWS + MTS_SMOKE_ROWS if is_true(row.get("valid_for_claim", ""))
    ]
    no_overclaim = (
        not live_result["status"]["R10_pass_for_claim"]
        and not smoke_result["status"]["R10_pass_for_claim"]
        and not claim_rows
    )
    return [
        {
            "check_id": "V563_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V563_1_prior_562_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V563_2_provenance_sources_recorded",
            "result": "pass" if len(PROVENANCE_ROWS) == 3 and provenance_urls_ok else "fail",
            "detail": f"provenance_rows={len(PROVENANCE_ROWS)};urls_recorded={provenance_urls_ok}",
        },
        {
            "check_id": "V563_3_anchor_bound_rows_numeric_nonclaim",
            "result": "pass" if anchor_ok else "fail",
            "detail": f"anchor_rows={len(ANCHOR_BOUND_ROWS)};issues={anchor_detail or 'none'}",
        },
        {
            "check_id": "V563_4_mts_smoke_rows_symbolic_nonclaim",
            "result": "pass" if smoke_ok else "fail",
            "detail": f"smoke_rows={len(MTS_SMOKE_ROWS)};issues={smoke_detail or 'none'}",
        },
        {
            "check_id": "V563_5_live_runner_blocks_placeholders",
            "result": "pass" if not live_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={live_result['status']['valid_mts_rows']};valid_bound={live_result['status']['valid_bound_rows']};R10_pass={live_result['status']['R10_pass_for_claim']}",
        },
        {
            "check_id": "V563_6_smoke_runner_blocks_nonclaim",
            "result": "pass" if not smoke_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={smoke_result['status']['valid_mts_rows']};valid_bound={smoke_result['status']['valid_bound_rows']};R10_pass={smoke_result['status']['R10_pass_for_claim']}",
        },
        {
            "check_id": "V563_7_nonclaim_interpolation_dry_check",
            "result": "pass" if interpolation_status == "pass_nonclaim" else "fail",
            "detail": f"status={interpolation_status}",
        },
        {
            "check_id": "V563_8_live_files_not_overwritten",
            "result": "pass" if len(live_bound_rows) == 2 and len(live_mts_rows) == 2 else "fail",
            "detail": f"live_bound_rows={len(live_bound_rows)};live_mts_rows={len(live_mts_rows)}",
        },
        {
            "check_id": "V563_9_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V563_10_no_overclaim",
            "result": "pass" if no_overclaim else "fail",
            "detail": "R10_pass=false;Newton=false;PPN=false;local_GR=false;anchor_only=true;parent_alpha_numeric=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    runner_summary: list[dict[str, Any]],
    evaluator_rows: list[dict[str, str]],
    blocker_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> None:
    body = f"""# 563 Y5 R10 real bound curve acquisition and alpha-row smoke runner

Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- Real Eot-Wash source-backed anchor points are now staged in a separate non-claim bound file.
- The live claim files are intentionally unchanged and still blocked by the existing runner.
- MTS alpha rows are smoke-only because the parent coefficients are still symbolic.
- This is data plumbing, not a local-GR/R10 pass.

## Bound Source Provenance
{markdown_table(PROVENANCE_ROWS)}

## Anchor Bound Rows
{markdown_table(ANCHOR_BOUND_ROWS)}

## MTS Smoke Rows
{markdown_table(MTS_SMOKE_ROWS)}

## Acquisition Ledger
{markdown_table(ACQUISITION_ROWS)}

## Runner Summary
{markdown_table(runner_summary)}

## Evaluator
{markdown_table(evaluator_rows)}

## Blocker Ledger
{markdown_table(blocker_rows)}

## Decision
{markdown_table(decision_rows)}

## Source Register
{markdown_table(source_rows)}

## Validation
{markdown_table(validation_rows)}

## Route Update
{markdown_table(route_rows)}

## Private Readout
This checkpoint improves the R10 evidence plumbing but keeps the physics gate shut. The right next move is either a real digitized bound curve or a parent-derived/theorem-zero MTS alpha row; anything weaker would be dressing a placeholder up as evidence, and we are not doing that.
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    write_csv(PROVENANCE_PATH, PROVENANCE_ROWS)
    write_csv(ACQUISITION_LEDGER_PATH, ACQUISITION_ROWS)
    write_csv(ANCHOR_BOUND_PATH, ANCHOR_BOUND_ROWS)
    write_csv(MTS_SMOKE_PATH, MTS_SMOKE_ROWS)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = ROOT / "runs" / f"{timestamp}-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner" / "results"
    live_result = run_runner(ROOT / LIVE_MTS_CURVE_PATH, ROOT / LIVE_BOUND_CURVE_PATH, run_root / "live_placeholder_runner")
    smoke_result = run_runner(ROOT / MTS_SMOKE_PATH, ROOT / ANCHOR_BOUND_PATH, run_root / "anchor_smoke_runner")
    interpolation_status, interpolation_detail = nonclaim_interpolation_dry_check(ANCHOR_BOUND_ROWS)

    source_rows = source_register_rows()
    prior_rows = read_csv(ROOT / PRIOR_VALIDATION_PATH)
    runner_summary = build_runner_summary(live_result, smoke_result, interpolation_status, interpolation_detail)
    evaluator_rows = build_evaluator(live_result, smoke_result, interpolation_status)
    blocker_rows = build_blocker_ledger()
    decision_rows = build_decision_rows()
    route_rows = build_route_update_rows()
    validation_rows = build_validation_rows(source_rows, prior_rows, live_result, smoke_result, interpolation_status)

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(RUNNER_SUMMARY_PATH, runner_summary)
    write_csv(EVALUATOR_PATH, evaluator_rows)
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows)
    write_csv(DECISION_PATH, decision_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(ROUTE_UPDATE_PATH, route_rows)
    write_doc(source_rows, runner_summary, evaluator_rows, blocker_rows, decision_rows, validation_rows, route_rows)

    summary = {
        "status": STATUS,
        "doc": rel(ROOT / DOC_PATH),
        "anchor_bound_file": rel(ROOT / ANCHOR_BOUND_PATH),
        "mts_smoke_file": rel(ROOT / MTS_SMOKE_PATH),
        "runner_summary": rel(ROOT / RUNNER_SUMMARY_PATH),
        "validation": rel(ROOT / VALIDATION_PATH),
        "validation_failed": [row for row in validation_rows if row["result"] != "pass"],
        "claim_ceiling": CLAIM_CEILING,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
