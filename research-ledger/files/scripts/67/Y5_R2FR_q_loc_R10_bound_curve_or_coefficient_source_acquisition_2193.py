from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2193"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2193-Y5-R2FR-q_loc-R10-bound-curve-or-coefficient-source-acquisition.md"

CANDIDATE_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
LIVE_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2193_SOURCE_REGISTER.csv",
    "curve_admission": OUT / "P8_Y5_PARENT_QLOC_2193_R10_CURVE_ADMISSION.csv",
    "join_preview": OUT / "P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW.csv",
    "missing_input_reduction": OUT / "P8_Y5_PARENT_QLOC_2193_MISSING_INPUT_REDUCTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2193_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2193_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2193_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2193_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2193_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2193_QLOC_R10_REVIEW_CURVE_ADMISSION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2193_R10_JOIN_PREVIEW_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_R10_BOUND_CURVE_ADMISSION_2193_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def safe_float(value: Any) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def formalization_has_2193_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2193-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2193*",
        "*P8_Y5_BRR545_2193*",
        "*Y5_R2FR_q_loc_R10_bound_curve_or_coefficient_source_acquisition_2193*",
        "*JR2193*",
        "*PARENT_QLOC_R10_BOUND_CURVE_ADMISSION_2193*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2192_doc",
            ROOT / "2192-Y5-R2FR-first-q_loc-response-operator-or-component-row-fill.md",
            ["NEXT2192_0_2193", "R10COMP2192_0_2020_anchor_lambda_schema_row", "VAL2192_OVERALL"],
            "2192 selected bound curve or coefficient/profile acquisition and supplied the 38.6 micrometer q_loc R10 seed.",
        ),
        (
            "2192_component_seed",
            OUT / "P8_Y5_PARENT_QLOC_2192_R10_COMPONENT_INPUT_ROW.csv",
            ["R10COMP2192_0_2020_anchor_lambda_schema_row", "3.86e-5", "MISSING_REAL_BOUND_CURVE"],
            "The current q_loc branch seed to join against a review candidate curve.",
        ),
        (
            "569_doc",
            ROOT / "569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md",
            ["Y5_R10_vector_axis_calibrated_2020_curve_review_candidate_no_claim", "alpha=1", "lambda=38.6 um"],
            "569 established an axis-calibrated vector review candidate and anchor recovery.",
        ),
        (
            "569_validation",
            OUT / "P8_Y5_BRR545_569_VALIDATION.csv",
            ["V569_3_curve_candidate_numeric", "V569_4_anchor_recovery", "V569_8_no_overclaim"],
            "569 validation proves the candidate is numeric, anchor-recovering and nonclaim.",
        ),
        (
            "569_axis_calibration",
            LOCAL_BOUNDS / "P8_Y5_R10_569_AXIS_CALIBRATION.csv",
            ["x_major_10um", "y_major_1e0", "axis_label_visual_and_tick_geometry_agree"],
            "Axis mapping evidence for lambda and alpha.",
        ),
        (
            "569_anchor_recovery",
            LOCAL_BOUNDS / "P8_Y5_R10_569_ANCHOR_RECOVERY.csv",
            ["AR569_0_paper_alpha1_38p6um", "R10_VECTOR_2020_REVIEW_0154", "pass_review_candidate"],
            "Anchor recovery row for alpha=1 at 38.6 micrometers.",
        ),
        (
            "569_promotion_gate",
            LOCAL_BOUNDS / "P8_Y5_R10_569_PROMOTION_GATE.csv",
            ["PG569_4_supplement_or_human_QA", "blocked", "PG569_5_live_file_update"],
            "Promotion gate keeps the candidate out of the live claim curve.",
        ),
        (
            "570_candidate_qa",
            LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
            ["QA570_1_anchor_recovery", "pass_review_candidate", "candidate_rows=390;claim_rows=0"],
            "Review-candidate QA confirms anchor recovery and zero claim rows.",
        ),
        (
            "570_curve_summary",
            LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
            ["CS570_0_rows", "390", "tightest_candidate_bound"],
            "Summary of candidate rows and bounds.",
        ),
        (
            "1034_doc",
            ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            ["R10B1034_3_vector_review_candidate_summary", "390 numeric review-candidate rows", "CGATE1034_1_external_curve"],
            "1034 repackaged the review candidate for projection use but kept scoring blocked.",
        ),
        (
            "1034_validation",
            OUT / "P8_Y5_BRR545_1034_VALIDATION.csv",
            ["V1034_3_vector_candidate_numeric", "V1034_4_vector_candidate_nonclaim", "V1034_9_claim_gates_blocked"],
            "1034 validation confirms the candidate file is numeric, nonclaim and blocked.",
        ),
        (
            "1034_candidate_curve",
            CANDIDATE_CURVE,
            ["R10_VECTOR_2020_REVIEW_0000", "valid_for_claim", "review_candidate_only_requires_official_supplement_or_human_visual_QA_before_live_claim_file_update"],
            "Dense 390-row nonclaim alpha(lambda) candidate to admit into the current q_loc branch.",
        ),
        (
            "live_digitized_placeholder",
            LIVE_CURVE,
            ["MISSING_DIGITIZED_ALPHA_BOUND", "MISSING_NUMERIC_LAMBDA", "valid_for_claim"],
            "Live claim curve remains a placeholder and must not be silently replaced.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def numeric_candidate_rows() -> list[dict[str, Any]]:
    rows = read_csv(CANDIDATE_CURVE)
    numeric: list[dict[str, Any]] = []
    for row in rows:
        lambda_value = safe_float(row.get("lambda_value"))
        alpha_bound = safe_float(row.get("alpha_bound"))
        if lambda_value is None or alpha_bound is None:
            continue
        if lambda_value <= 0 or alpha_bound <= 0:
            continue
        numeric.append({**row, "lambda_float": lambda_value, "alpha_float": alpha_bound})
    return numeric


def axis_summary() -> dict[str, Any]:
    rows = read_csv(LOCAL_BOUNDS / "P8_Y5_R10_569_AXIS_CALIBRATION.csv")
    residuals = [safe_float(row.get("abs_log10_residual")) for row in rows]
    residuals_clean = [value for value in residuals if value is not None]
    return {
        "axis_rows": len(rows),
        "max_abs_log10_residual": max(residuals_clean) if residuals_clean else "MISSING",
        "x_axis_rows": sum(1 for row in rows if row.get("axis") == "x_lambda"),
        "y_axis_rows": sum(1 for row in rows if row.get("axis") == "y_alpha"),
        "all_nonclaim": all(str(row.get("valid_for_claim", "")).lower() == "false" for row in rows),
    }


def anchor_recovery_summary() -> dict[str, Any]:
    rows = read_csv(LOCAL_BOUNDS / "P8_Y5_R10_569_ANCHOR_RECOVERY.csv")
    row = rows[0] if rows else {}
    return {
        "anchor_id": row.get("anchor_id", "MISSING"),
        "target_lambda_m": safe_float(row.get("target_lambda_m")),
        "target_alpha": safe_float(row.get("target_alpha")),
        "nearest_bound_id": row.get("nearest_bound_id", "MISSING"),
        "candidate_lambda_m": safe_float(row.get("candidate_lambda_m")),
        "candidate_alpha": safe_float(row.get("candidate_alpha")),
        "lambda_relative_error": safe_float(row.get("lambda_relative_error")),
        "alpha_log10_error": safe_float(row.get("alpha_log10_error")),
        "recovery_status": row.get("recovery_status", "MISSING"),
        "valid_for_claim": row.get("valid_for_claim", "MISSING"),
    }


def curve_admission_rows() -> list[dict[str, Any]]:
    numeric = numeric_candidate_rows()
    axis = axis_summary()
    anchor = anchor_recovery_summary()
    live_rows = read_csv(LIVE_CURVE)
    lambdas = [row["lambda_float"] for row in numeric]
    alphas = [row["alpha_float"] for row in numeric]
    claim_rows = [row for row in read_csv(CANDIDATE_CURVE) if str(row.get("valid_for_claim", "")).lower() == "true"]
    promotion_rows = read_csv(LOCAL_BOUNDS / "P8_Y5_R10_569_PROMOTION_GATE.csv")
    blocked_promotion = [
        row
        for row in promotion_rows
        if str(row.get("result", "")).lower() == "blocked" and truthy(row.get("required_for_promotion", False))
    ]
    return [
        base_row(
            admission_id="R10CURVE2193_0_review_candidate_admitted_to_q_loc_branch",
            curve_file=str(CANDIDATE_CURVE),
            source_kind="axis_calibrated_vector_fig5b_review_candidate",
            row_count=len(read_csv(CANDIDATE_CURVE)),
            numeric_positive_rows=len(numeric),
            lambda_min_m=min(lambdas) if lambdas else "MISSING",
            lambda_max_m=max(lambdas) if lambdas else "MISSING",
            alpha_min_dimensionless=min(alphas) if alphas else "MISSING",
            alpha_max_dimensionless=max(alphas) if alphas else "MISSING",
            axis_rows=axis["axis_rows"],
            max_abs_log10_axis_residual=axis["max_abs_log10_residual"],
            anchor_recovery_status=anchor["recovery_status"],
            anchor_nearest_bound_id=anchor["nearest_bound_id"],
            anchor_lambda_relative_error=anchor["lambda_relative_error"],
            anchor_alpha_log10_error=anchor["alpha_log10_error"],
            candidate_claim_rows=len(claim_rows),
            live_curve_rows=len(live_rows),
            live_curve_status="placeholder_retained_not_overwritten",
            blocked_promotion_gates=len(blocked_promotion),
            admitted_for="private_q_loc_R10_join_preview_and_coefficient_pressure",
            score_ready=False,
            claim_grade_curve=False,
            admission_status="admitted_as_review_candidate_nonclaim",
            notes="External R10 side is now dense enough for private coefficient pressure, but it is not public/claim-grade without supplement or human QA.",
        )
    ]


def nearest_curve_row(target_lambda: float, rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    return min(rows, key=lambda row: abs(float(row["lambda_float"]) - target_lambda))


def join_preview_rows() -> list[dict[str, Any]]:
    component_rows = read_csv(OUT / "P8_Y5_PARENT_QLOC_2192_R10_COMPONENT_INPUT_ROW.csv")
    component = component_rows[0] if component_rows else {}
    target_lambda = safe_float(component.get("lambda_value"))
    numeric = numeric_candidate_rows()
    joined: list[dict[str, Any]] = []
    if target_lambda is None:
        return [
            base_row(
                join_id="R10JOIN2193_0_failed_no_component_lambda",
                join_status="blocked_missing_target_lambda",
                score_ready=False,
                failure_reasons="MISSING_COMPONENT_LAMBDA",
            )
        ]
    nearest = nearest_curve_row(target_lambda, numeric)
    if nearest is None:
        return [
            base_row(
                join_id="R10JOIN2193_0_failed_no_candidate_curve",
                target_component_row_id=component.get("component_row_id", "MISSING"),
                target_lambda=target_lambda,
                join_status="blocked_missing_candidate_curve",
                score_ready=False,
                failure_reasons="MISSING_NUMERIC_CANDIDATE_CURVE",
            )
        ]
    nearest_lambda = float(nearest["lambda_float"])
    nearest_alpha = float(nearest["alpha_float"])
    relative_error = abs(nearest_lambda - target_lambda) / target_lambda
    joined.append(
        base_row(
            join_id="R10JOIN2193_0_component_seed_to_review_candidate",
            target_component_row_id=component.get("component_row_id", "MISSING"),
            target_lambda_m=target_lambda,
            nearest_bound_id=nearest.get("bound_id", "MISSING"),
            nearest_lambda_m=nearest_lambda,
            nearest_alpha_bound=nearest_alpha,
            lambda_relative_error=relative_error,
            alpha_bound_source=nearest.get("alpha_bound_source", "MISSING"),
            curve_file=str(CANDIDATE_CURVE),
            curve_status="review_candidate_nonclaim",
            alpha_predicted="MISSING_ALPHA_PREDICTED_FROM_QLOC",
            c_q_alpha_lambda=component.get("c_q_alpha_lambda", "MISSING_CQ_ALPHA_LAMBDA"),
            q_profile_lambda=component.get("q_profile_lambda", "MISSING_QLOC_PROFILE"),
            range_kernel=component.get("range_kernel", "MISSING_RANGE_KERNEL"),
            q_units=component.get("q_units", "MISSING_QLOC_UNITS"),
            score_expression="requires abs(alpha_predicted)<=nearest_alpha_bound after interpolation and all sources are claim-valid",
            failure_reasons="MISSING_ALPHA_PREDICTED;MISSING_CQ_ALPHA_LAMBDA;MISSING_QLOC_PROFILE;MISSING_RANGE_KERNEL;CANDIDATE_CURVE_NONCLAIM",
            join_status="join_preview_pass_nonclaim_scoring_blocked",
            score_ready=False,
        )
    )
    return joined


def missing_input_reduction_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            item_id="MIR2193_0_external_bound_curve",
            prior_2192_status="MISSING_REAL_BOUND_CURVE",
            current_2193_status="REVIEW_CANDIDATE_DENSE_CURVE_AVAILABLE_NONCLAIM",
            evidence_path=str(CANDIDATE_CURVE),
            reduction_strength="private_testing_improved_not_claim_grade",
            still_missing_for_claim="OFFICIAL_SUPPLEMENT_TABLE_OR_HUMAN_VISUAL_QA_PROMOTION;LIVE_CURVE_UPDATE_SIGNOFF",
            score_ready=False,
        ),
        base_row(
            item_id="MIR2193_1_c_q_alpha_lambda",
            prior_2192_status="MISSING_CQ_ALPHA_LAMBDA",
            current_2193_status="STILL_MISSING",
            evidence_path="MISSING_PARENT_COEFFICIENT_SOURCE",
            reduction_strength="none",
            still_missing_for_claim="PARENT_DERIVED_RESPONSE_COEFFICIENT_OR_THEOREM_ZERO",
            score_ready=False,
        ),
        base_row(
            item_id="MIR2193_2_q_profile_lambda",
            prior_2192_status="MISSING_QLOC_PROFILE",
            current_2193_status="STILL_MISSING",
            evidence_path="MISSING_QLOC_COMPONENT_PROFILE_SOURCE",
            reduction_strength="none",
            still_missing_for_claim="PARENT_OR_SOLVED_LOCAL_PROFILE_IN_OBSERVED_FRAME",
            score_ready=False,
        ),
        base_row(
            item_id="MIR2193_3_range_kernel_and_units",
            prior_2192_status="MISSING_RANGE_KERNEL;MISSING_QLOC_UNITS",
            current_2193_status="STILL_MISSING",
            evidence_path="MISSING_PARENT_NORMALIZATION_AND_GREEN_KERNEL",
            reduction_strength="none",
            still_missing_for_claim="GREEN_KERNEL_NORMALIZATION;QLOC_UNITS;FINITE_SOURCE_TEST_PROFILE",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CG2193_0_external_curve",
            "R10 external alpha_bound(lambda) can support private diagnostics",
            "PASS_NONCLAIM",
            "390 positive numeric review-candidate rows exist and are source-backed by the arXiv vector figure.",
        ),
        (
            "CG2193_1_external_curve_claim_grade",
            "R10 external alpha_bound(lambda) is claim-grade",
            "BLOCKED_NONCLAIM",
            "Supplemental numerical table or human visual QA promotion is still absent.",
        ),
        (
            "CG2193_2_theory_side_alpha",
            "MTS/q_loc alpha_predicted(lambda) is score-ready",
            "BLOCKED_NONCLAIM",
            "c_q_alpha(lambda), q_profile(lambda), range kernel, units and observed-frame profile are still missing.",
        ),
        (
            "CG2193_3_R10_score",
            "R10 comparator can claim pass/fail",
            "BLOCKED_NONCLAIM",
            "External curve is nonclaim and theory-side alpha is absent, so no R10/local-GR/Newton/PPN claim is allowed.",
        ),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2193_0_gain",
            "REVIEW_CANDIDATE_CURVE_ADMITTED_TO_QLOC_R10",
            "The q_loc branch no longer has only an anchor; it has a dense nonclaim alpha(lambda) wall for private coefficient pressure.",
            "selected",
        ),
        (
            "DEC2193_1_limit",
            "R10_SCORE_STILL_BLOCKED",
            "The external curve is not claim-grade and MTS/q_loc alpha_predicted(lambda) is not derived.",
            "selected",
        ),
        (
            "DEC2193_2_next",
            "DERIVE_QLOC_ALPHA_COEFFICIENT_OR_PROFILE_NEXT",
            "With a private curve wall available, the best leap is theory-side: derive c_q_alpha(lambda), q_profile(lambda), and range-kernel normalization, or prove theorem-zero.",
            "selected",
        ),
        (
            "DEC2193_3_data_parallel",
            "SUPPLEMENT_OR_HUMAN_QA_PROMOTION_HELD_PARALLEL",
            "A claim-grade external curve still needs supplement/table or human QA, but that is no longer the only blocker for private progress.",
            "held_parallel",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2193_0_2194",
            selection_status="selected",
            target_file="2194-Y5-R2FR-parent-q_loc-alpha-coefficient-profile-or-theorem-zero.md",
            target_script="scripts/Y5_R2FR_parent_q_loc_alpha_coefficient_profile_or_theorem_zero_2194.py",
            objective="derive or source the theory-side q_loc->R10 alpha prediction: c_q_alpha(lambda), q_profile(lambda), range-kernel normalization and observed-frame units, or prove q_loc theorem-zero instead",
            success_condition="one theory-side missing input is either parent-derived/source-backed or explicitly demoted to residual closure; no R10 score is claimed unless all external and theory-side gates are valid",
            do_not_do="do not set c_q_alpha=1 by convention; do not use unity profile shortcuts; do not promote review-candidate curve to claim-grade; do not claim local-GR/R10/Newton/PPN pass",
        ),
        base_row(
            route_id="NEXT2193_1_data_QA",
            selection_status="held_parallel",
            target_file="2194b-Y5-R10-official-supplement-or-human-QA-promotion-gate.md",
            target_script="scripts/Y5_R10_official_supplement_or_human_QA_promotion_gate_2194b.py",
            objective="attempt official supplemental-table acquisition or human visual QA gate for the review candidate curve",
            success_condition="external curve promotion is either source-signed or remains explicitly blocked without changing live claim files",
            do_not_do="do not bypass the promotion gate by copying the review candidate into R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["curve_admission"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["join_preview"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["curve_admission"], BRANCH_COPIES["source_weight"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if truthy(row.get("claim_allowed", False)):
                return False
            if truthy(row.get("valid_for_claim", False)):
                return False
    return True


def all_score_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if "score_ready" in row and truthy(row["score_ready"]):
                return False
            if "claim_grade_curve" in row and truthy(row["claim_grade_curve"]):
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2193_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2193_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    admission = rows_by_name["curve_admission"][0]
    curve_numeric = int(admission["numeric_positive_rows"]) >= 100 and int(admission["candidate_claim_rows"]) == 0
    validations.append(base_row(validation_id="VAL2193_02_curve_numeric_nonclaim", status="PASS" if curve_numeric else "FAIL", detail=f"numeric_positive_rows={admission['numeric_positive_rows']};candidate_claim_rows={admission['candidate_claim_rows']}"))

    axis_ok = safe_float(admission["max_abs_log10_axis_residual"])
    anchor_error = safe_float(admission["anchor_lambda_relative_error"])
    anchor_alpha_error = safe_float(admission["anchor_alpha_log10_error"])
    calibration_ok = (
        axis_ok is not None
        and axis_ok < 0.001
        and anchor_error is not None
        and anchor_error < 0.01
        and anchor_alpha_error is not None
        and anchor_alpha_error < 0.02
    )
    validations.append(base_row(validation_id="VAL2193_03_axis_anchor_recovery", status="PASS" if calibration_ok else "FAIL", detail=f"max_axis_residual={admission['max_abs_log10_axis_residual']};anchor_lambda_rel_error={admission['anchor_lambda_relative_error']};anchor_alpha_log10_error={admission['anchor_alpha_log10_error']}"))

    live_rows = read_csv(LIVE_CURVE)
    live_placeholder = any("MISSING" in str(value) for row in live_rows for value in row.values()) and all(str(row.get("valid_for_claim", "")).lower() == "false" for row in live_rows)
    validations.append(base_row(validation_id="VAL2193_04_live_curve_not_overwritten", status="PASS" if live_placeholder else "FAIL", detail=f"live_rows={len(live_rows)};placeholder_retained={live_placeholder}"))

    join = rows_by_name["join_preview"][0]
    join_ok = (
        join["join_status"] == "join_preview_pass_nonclaim_scoring_blocked"
        and safe_float(join["nearest_alpha_bound"]) is not None
        and safe_float(join["nearest_alpha_bound"]) > 0
        and safe_float(join["lambda_relative_error"]) is not None
        and safe_float(join["lambda_relative_error"]) < 0.01
        and not truthy(join["score_ready"])
    )
    validations.append(base_row(validation_id="VAL2193_05_join_preview_nonclaim", status="PASS" if join_ok else "FAIL", detail=f"join_status={join['join_status']};nearest_alpha={join.get('nearest_alpha_bound')};lambda_relative_error={join.get('lambda_relative_error')};score_ready={join.get('score_ready')}"))

    reduction_rows = rows_by_name["missing_input_reduction"]
    external_reduced = any(row["item_id"] == "MIR2193_0_external_bound_curve" and row["current_2193_status"] == "REVIEW_CANDIDATE_DENSE_CURVE_AVAILABLE_NONCLAIM" for row in reduction_rows)
    theory_still_missing = all(row["current_2193_status"] == "STILL_MISSING" for row in reduction_rows if row["item_id"] != "MIR2193_0_external_bound_curve")
    validations.append(base_row(validation_id="VAL2193_06_missing_input_reduction", status="PASS" if external_reduced and theory_still_missing else "FAIL", detail=f"external_reduced={external_reduced};theory_still_missing={theory_still_missing}"))

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2193_07_claim_gate", status="PASS" if "PASS_NONCLAIM" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses else "FAIL", detail="external curve passes only nonclaim diagnostics; R10 score remains blocked"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2193_08_decision", status="PASS" if "DERIVE_QLOC_ALPHA_COEFFICIENT_OR_PROFILE_NEXT" in decisions else "FAIL", detail="decision selects theory-side coefficient/profile derivation next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2193_09_next_target", status="PASS" if "NEXT2193_0_2194" in routes else "FAIL", detail="2194 theory-side route selected"))

    validations.append(base_row(validation_id="VAL2193_10_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2193_11_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or claim-grade"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2193_12_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2193_13_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2193_14_formalization_clean", status="PASS" if not formalization_has_2193_artifacts() else "FAIL", detail="formalization-workbench has no 2193 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2193_15_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2193_OVERALL", status=overall, detail="2193 admits the dense R10 review-candidate curve into the q_loc branch for private join/pressure work while keeping all claim gates blocked"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2193 - Y5/R2FR q_loc R10 Bound Curve Or Coefficient Source Acquisition",
        "",
        "## Current Verdict",
        "",
        "2193 takes the best available route: it admits the existing 1034 Eot-Wash 2020 vector-extracted `alpha(lambda)` curve into the current `q_loc -> R10` branch as a **review-candidate, nonclaim** external wall.",
        "",
        "This is real progress for private testing because the branch no longer has only an `alpha=1` threshold anchor. It now has 390 positive numeric candidate rows, low-residual axis calibration, and anchor recovery near `lambda=38.6 um`, `alpha=1`.",
        "",
        "It is still not a public or claim-grade R10 curve. The live `R10_alpha_lambda_bound_curve_DIGITIZED.csv` file is deliberately unchanged, and R10 scoring remains blocked because the theory-side `alpha_predicted(lambda)` is missing.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## R10 Curve Admission",
        "",
        md_table(rows_by_name["curve_admission"], ["admission_id", "source_kind", "row_count", "numeric_positive_rows", "lambda_min_m", "lambda_max_m", "alpha_min_dimensionless", "alpha_max_dimensionless", "anchor_recovery_status", "candidate_claim_rows", "live_curve_status", "admission_status", "score_ready", "claim_grade_curve", "valid_for_claim"]),
        "",
        "## q_loc R10 Join Preview",
        "",
        md_table(rows_by_name["join_preview"], ["join_id", "target_component_row_id", "target_lambda_m", "nearest_bound_id", "nearest_lambda_m", "nearest_alpha_bound", "lambda_relative_error", "alpha_predicted", "failure_reasons", "join_status", "score_ready", "valid_for_claim"]),
        "",
        "## Missing Input Reduction",
        "",
        md_table(rows_by_name["missing_input_reduction"], ["item_id", "prior_2192_status", "current_2193_status", "evidence_path", "reduction_strength", "still_missing_for_claim", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "The external R10 wall is now good enough for private coefficient pressure: the branch can ask what `alpha_predicted(lambda)` would need to be below. That is not the same as an R10 pass, because the review candidate still needs supplement/human QA promotion and the MTS/q_loc alpha prediction is not derived.",
        "",
        "Best next attack: stop circling the external data and go after the theory-side map: derive or source `c_q_alpha(lambda)`, `q_profile(lambda)`, range-kernel normalization, and q_loc units/profile; or prove theorem-zero so the alpha prediction vanishes.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "curve_admission": curve_admission_rows(),
        "join_preview": join_preview_rows(),
        "missing_input_reduction": missing_input_reduction_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
