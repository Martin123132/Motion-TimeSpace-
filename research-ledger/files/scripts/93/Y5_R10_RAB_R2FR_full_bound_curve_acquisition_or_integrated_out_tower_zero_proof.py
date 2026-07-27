from __future__ import annotations

import csv
import math
from pathlib import Path


PACK_ID = "P8_Y5_R10_1342"
TITLE = "1342-Y5-R10-RAB-R2FR-full-bound-curve-acquisition-or-integrated-out-tower-zero-proof"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CURVE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_EXISTING_BOUND_CURVE_AUDIT.csv"
TOWER_ZERO_PATH = OUT_DIR / f"{PACK_ID}_INTEGRATED_OUT_TOWER_ZERO_ATTEMPT.csv"
ACQUISITION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_FULL_CURVE_ACQUISITION_LEDGER.csv"
INTERPOLATION_SMOKE_PATH = OUT_DIR / f"{PACK_ID}_INTERPOLATION_SMOKE.csv"
PROMOTION_GATE_PATH = OUT_DIR / f"{PACK_ID}_BOUND_CURVE_PROMOTION_GATE.csv"
RUNNER_STATUS_PATH = OUT_DIR / f"{PACK_ID}_R2FR_RUNNER_STATUS.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1342_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def as_float(value: object) -> float | None:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def falsey(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "n", ""}


def row_has_missing_marker(row: dict[str, object]) -> bool:
    for value in row.values():
        text = str(value).strip().upper()
        if "MISSING" in text or "PLACEHOLDER" in text or text in {"TBD", "TODO"}:
            return True
    return False


def local_artifact_exists(value: object) -> bool:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return False
    if text.startswith("http://") or text.startswith("https://"):
        return True
    return source_path(text).exists()


def numeric_curve_counts(rows: list[dict[str, str]]) -> tuple[int, int]:
    numeric = 0
    positive = 0
    for row in rows:
        lambda_value = as_float(row.get("lambda_value"))
        alpha_bound = as_float(row.get("alpha_bound"))
        if lambda_value is not None and alpha_bound is not None:
            numeric += 1
            if lambda_value > 0 and alpha_bound > 0:
                positive += 1
    return numeric, positive


def audit_curve_file(artifact_id: str, relative_path: str, intended_role: str) -> dict[str, object]:
    path = source_path(relative_path)
    rows = read_csv(path)
    numeric_rows, positive_numeric_rows = numeric_curve_counts(rows)
    claim_true_rows = sum(1 for row in rows if truthy(row.get("valid_for_claim", False)))
    missing_marker_rows = sum(1 for row in rows if row_has_missing_marker(row))
    source_asset_missing_rows = 0
    for row in rows:
        for field in ("source_file", "render_file"):
            if field in row and str(row.get(field, "")).strip():
                if not local_artifact_exists(row.get(field)):
                    source_asset_missing_rows += 1

    if not path.exists():
        status = "MISSING_ARTIFACT"
        promotion_effect = "cannot use"
    elif rows and numeric_rows == positive_numeric_rows == len(rows) and claim_true_rows == len(rows) and missing_marker_rows == 0:
        status = "CLAIM_READY_CANDIDATE_REQUIRES_EXTERNAL_POLICY_REVIEW"
        promotion_effect = "would still need MTS coefficient before scoring"
    elif rows and positive_numeric_rows > 0 and claim_true_rows == 0 and missing_marker_rows == 0:
        status = "PRIVATE_PRESSURE_CURVE_NONCLAIM"
        promotion_effect = "usable for internal interpolation smoke only"
    elif rows and missing_marker_rows > 0:
        status = "PLACEHOLDER_OR_TEMPLATE_NONCLAIM"
        promotion_effect = "cannot score"
    else:
        status = "EMPTY_OR_UNPARSEABLE_NONCLAIM"
        promotion_effect = "cannot score"

    return {
        "artifact_id": artifact_id,
        "relative_path": relative_path,
        "exists": path.exists(),
        "intended_role": intended_role,
        "row_count": len(rows),
        "numeric_rows": numeric_rows,
        "positive_numeric_rows": positive_numeric_rows,
        "claim_true_rows": claim_true_rows,
        "missing_marker_rows": missing_marker_rows,
        "source_asset_missing_rows": source_asset_missing_rows,
        "status": status,
        "promotion_effect": promotion_effect,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def loglog_interpolate_alpha(rows: list[dict[str, str]], lambda_value_m: float) -> float | None:
    points: list[tuple[float, float]] = []
    for row in rows:
        lambda_value = as_float(row.get("lambda_value"))
        alpha_bound = as_float(row.get("alpha_bound"))
        if lambda_value is not None and alpha_bound is not None and lambda_value > 0 and alpha_bound > 0:
            points.append((lambda_value, alpha_bound))
    points.sort()
    if len(points) < 2 or lambda_value_m < points[0][0] or lambda_value_m > points[-1][0]:
        return None
    for (left_lambda, left_alpha), (right_lambda, right_alpha) in zip(points, points[1:]):
        if left_lambda <= lambda_value_m <= right_lambda:
            if left_lambda == right_lambda:
                return left_alpha
            left_x = math.log10(left_lambda)
            right_x = math.log10(right_lambda)
            frac = (math.log10(lambda_value_m) - left_x) / (right_x - left_x)
            left_y = math.log10(left_alpha)
            right_y = math.log10(right_alpha)
            return 10 ** (left_y + frac * (right_y - left_y))
    return None


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not falsey(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not falsey(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1342*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1342_0_1341_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1341_NEXT_TARGET.csv",
            "needle": "NEXT1341_0_1342",
            "role": "selected 1342 target",
        },
        {
            "source_id": "SRC1342_1_1341_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1341_R2FR_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "R2ZERO1341_3_integrated_out_tower",
            "role": "integrated-out tower gap inherited from 1341",
        },
        {
            "source_id": "SRC1342_2_1341_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1341_SOURCE_BACKED_BOUND_ROWS_NONCLAIM.csv",
            "needle": "BOUND1341_1_R10_full_curve_required",
            "role": "full curve required gate inherited from 1341",
        },
        {
            "source_id": "SRC1342_3_1341_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1341_VALIDATION.csv",
            "needle": "VAL1341_11_overall",
            "role": "1341 pass gate",
        },
        {
            "source_id": "SRC1342_4_611_curve_QA",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_611_BOUND_CURVE_QA.csv",
            "needle": "QA611_5_anchor_recovery",
            "role": "existing Lee 2020 review-candidate curve QA",
        },
        {
            "source_id": "SRC1342_5_612_promotion_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_612_BOUND_CURVE_PROMOTION_GATE.csv",
            "needle": "PG612_1_claim_grade_bound_curve",
            "role": "claim-grade promotion block for review candidate",
        },
        {
            "source_id": "SRC1342_6_674_curve_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_674_BOUND_CURVE_STATUS_GATE.csv",
            "needle": "BCG674_1_review_candidate_curve",
            "role": "current live/review curve status",
        },
        {
            "source_id": "SRC1342_7_965_curve_manifest",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv",
            "needle": "R2FC965_0_Lee2020_full_curve_required",
            "role": "R2/fR full curve intake manifest",
        },
        {
            "source_id": "SRC1342_8_966_digitizer_decision",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_R2FR_CURVE_DIGITIZER_DECISION.csv",
            "needle": "R2DIG966_0_selected_route",
            "role": "R2/fR digitizer defer decision",
        },
        {
            "source_id": "SRC1342_9_R10_runner",
            "local_path": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "needle": "alpha",
            "role": "existing strict alpha-lambda runner",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    curve_artifacts = [
        (
            "CURVE1342_0_live_digitized_placeholder",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "live claim-facing bound curve file",
        ),
        (
            "CURVE1342_1_Lee2020_vector_review_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            "private pressure curve from Lee 2020 figure extraction",
        ),
        (
            "CURVE1342_2_anchor_smoke",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            "source-backed anchor-only smoke data",
        ),
        (
            "CURVE1342_3_old_run_live_result",
            "runs/20260605-144500-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner/results/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "old runner result mirror of live placeholder",
        ),
    ]
    curve_audit = [audit_curve_file(*artifact) for artifact in curve_artifacts]

    tower_zero = [
        {
            "attempt_id": "TOWER1342_0_target",
            "clause": "integrated-out R2/fR tower zero",
            "needed_statement": "eliminating hidden/projector/memory/scalar sectors cannot generate R^2, f(R), Yukawa, or nonlocal scalar curvature terms in S_eff[g]",
            "current_result": "TARGET_EXACT",
            "gap_or_countermodel": "must be proved before EH/local-GR left-hand side can be promoted",
            "zero_proof_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_1_visible_second_order",
            "clause": "visible Euler-Lagrange order",
            "needed_statement": "local observed metric equations are strictly second order after all reductions",
            "current_result": "CONDITIONAL_FILTER_SURVIVES",
            "gap_or_countermodel": "second-order output rejects finite R2/fR but does not prove parent coefficients are zero",
            "zero_proof_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_2_auxiliary_solution",
            "clause": "auxiliary/projector elimination",
            "needed_statement": "all eliminated sectors solve algebraically or by pure constraints with no curvature-dependent Green operator",
            "current_result": "UNSIGNED",
            "gap_or_countermodel": "a massive eliminated scalar or projector response can generate R F(□) R, R^2, or Yukawa residuals",
            "zero_proof_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_3_functional_measure",
            "clause": "measure/Jacobian/determinant silence",
            "needed_statement": "reduction measure and determinant terms do not add curvature-squared local counterterms",
            "current_result": "UNSIGNED",
            "gap_or_countermodel": "integrating out a nontrivial sector can shift the effective local curvature expansion even when the classical equation is quiet",
            "zero_proof_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_4_memory_kernel",
            "clause": "memory/nonlocal kernel silence",
            "needed_statement": "history kernels collapse to EH plus harmless boundary terms in the local exterior branch",
            "current_result": "UNSIGNED",
            "gap_or_countermodel": "R F(□) R or finite-range scalar response remains allowed without an explicit kernel theorem",
            "zero_proof_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_5_boundary_flux",
            "clause": "boundary/local projection harmlessness",
            "needed_statement": "projection and boundary terms do not leak an effective scalar mode into the local PPN branch",
            "current_result": "UNSIGNED",
            "gap_or_countermodel": "boundary data can mimic a retained scalar amplitude unless source-normalized flux is killed",
            "zero_proof_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_6_primitive_no_marker",
            "clause": "no natural curvature-tower marker",
            "needed_statement": "motion/time/space primitives admit EH but no independent scalar curvature-tower marker",
            "current_result": "UNSIGNED",
            "gap_or_countermodel": "previous primitive-minimality audits did not forbid a local curvature scalar marker",
            "zero_proof_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TOWER1342_7_verdict",
            "clause": "c_R2/c_fRR parent-zero signature",
            "needed_statement": "all routes that generate finite scalar R2/fR residuals are parent-zeroed",
            "current_result": "ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "gap_or_countermodel": "integrated-out tower, measure, memory, boundary, and primitive-marker clauses remain unsigned",
            "zero_proof_status": "BOUND_OR_CLOSURE_ROUTE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    vector_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv")
    alpha_at_anchor = loglog_interpolate_alpha(vector_rows, 38.6e-6)
    if alpha_at_anchor is None:
        anchor_status = "NO_INTERPOLATION_AVAILABLE"
        anchor_detail = "Lee 2020 review candidate missing or probe outside domain"
    else:
        log_error = abs(math.log10(alpha_at_anchor))
        anchor_status = "PRIVATE_PRESSURE_ANCHOR_RECOVERY_PASS" if log_error < 0.02 else "PRIVATE_PRESSURE_ANCHOR_RECOVERY_WARN"
        anchor_detail = f"alpha_interp={alpha_at_anchor:.12g}; log10_error_to_alpha1={log_error:.6g}"

    interpolation_smoke = [
        {
            "interp_id": "INT1342_0_Lee2020_anchor_probe",
            "curve_artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            "lambda_probe_m": 38.6e-6,
            "lambda_probe_um": 38.6,
            "alpha_interpolated": "" if alpha_at_anchor is None else f"{alpha_at_anchor:.12g}",
            "method": "log_log_linear_interpolation_private_smoke",
            "status": anchor_status,
            "detail": anchor_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "interp_id": "INT1342_1_policy",
            "curve_artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            "lambda_probe_m": "not_applicable",
            "lambda_probe_um": "not_applicable",
            "alpha_interpolated": "not_claim_value",
            "method": "policy_gate",
            "status": "INTERPOLATOR_READY_FOR_PRIVATE_PRESSURE_ONLY",
            "detail": "review-candidate curve has numeric support but valid_for_claim=false and cannot score a public/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acquisition_ledger = [
        {
            "acq_id": "ACQ1342_0_live_curve",
            "artifact_or_target": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "current_status": "placeholder_live_file",
            "evidence_quality": "none",
            "action": "leave unchanged until claim-grade curve is independently sourced",
            "claim_effect": "blocks finite R2/fR scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "ACQ1342_1_Lee2020_review_candidate",
            "artifact_or_target": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            "current_status": "390_positive_numeric_rows_private_review_candidate",
            "evidence_quality": "source-backed figure extraction with local assets and anchor recovery, but no human/official promotion",
            "action": "retain as private pressure wall and interpolation smoke data",
            "claim_effect": "cannot promote because every row has valid_for_claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "ACQ1342_2_claim_grade_route",
            "artifact_or_target": "Lee2020_or_official_short_range_alpha_lambda_curve",
            "current_status": "claim_grade_full_curve_still_required",
            "evidence_quality": "requires official machine-readable table or independent digitization QA/promotion",
            "action": "only promote after provenance, axis, curve identity, units, monotonic/domain, and source-asset checks pass",
            "claim_effect": "still cannot score without MTS alpha/lambda prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "ACQ1342_3_MTS_prediction_route",
            "artifact_or_target": "MTS_R2FR_scalar_prediction_row",
            "current_status": "missing_parent_coefficient",
            "evidence_quality": "no numeric c_R2/c_fRR, scalar mass, alpha, screening, or source map",
            "action": "derive parent coefficient zero or fill finite scalar map before any curve comparison matters",
            "claim_effect": "blocks runner even if a claim-grade curve later exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_gate = [
        {
            "gate_id": "GATE1342_0_parent_zero",
            "requirement": "parent-signed zero proof for c_R2/c_fRR",
            "current_status": "BLOCKED",
            "detail": "TOWER1342_7_verdict is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1342_1_full_curve",
            "requirement": "full positive numeric alpha(lambda) curve with source provenance and valid_for_claim=true",
            "current_status": "BLOCKED",
            "detail": "live file is placeholder; Lee 2020 vector candidate is private nonclaim only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1342_2_MTS_prediction",
            "requirement": "numeric parent-sourced alpha_predicted and lambda_predicted for finite scalar branch",
            "current_status": "BLOCKED",
            "detail": "MTS scalar coefficient/mass/coupling/screening map absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1342_3_interpolation",
            "requirement": "prediction lambda lies inside the sourced curve domain and uses declared interpolation",
            "current_status": "PRIVATE_ONLY",
            "detail": "log-log interpolator works on the review candidate, but no claim row may use it yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1342_4_local_GR",
            "requirement": "R2/fR family zeroed or bounded before EH/local-GR promotion",
            "current_status": "BLOCKED",
            "detail": "R11 residual family remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_status = [
        {
            "run_id": "RUN1342_0_zero_branch",
            "input_branch": "c_R2/c_fRR_zero_switch",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "reason": "integrated-out tower and primitive-marker clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1342_1_live_curve_branch",
            "input_branch": "live_R10_alpha_lambda_bound_curve_DIGITIZED",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_BOUND_CURVE_PLACEHOLDER",
            "reason": "live file has no positive numeric claim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1342_2_review_curve_branch",
            "input_branch": "Lee2020_vector_review_candidate",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_NONCLAIM_REVIEW_CANDIDATE",
            "reason": "numeric interpolation works for private pressure only; valid_for_claim=false for every row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1342_3_MTS_prediction_branch",
            "input_branch": "finite_R2FR_scalar_prediction",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_MISSING_MTS_PARENT_COEFFICIENT",
            "reason": "no parent-sourced c_R2/c_fRR, alpha, lambda, mass, source-coupling, or screening row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1342_VERDICT",
            "input_branch": "all_R2FR_routes",
            "accepted_for_scoring": False,
            "verdict": "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "reason": "neither zero theorem nor finite scalar comparison is claim-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1342_0_zero_route",
            "decision": "integrated-out tower zero proof is not derived",
            "because": "auxiliary, measure, memory, boundary, and primitive-marker clauses remain unsigned",
            "effect": "finite scalar branch cannot be killed by theorem yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1342_1_curve_route",
            "decision": "existing Lee 2020 vector curve is useful but private-only",
            "because": "it has numeric rows and anchor recovery, but no claim-grade promotion and every row remains valid_for_claim=false",
            "effect": "it can pressure-test future coefficients but cannot support a local-GR/R10 claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1342_2_best_next",
            "decision": "next work should attack the parent scalar coefficient before more curve work",
            "because": "without c_R2/c_fRR or a signed zero theorem, a perfect bound curve still cannot score MTS",
            "effect": "1343 should target parent coefficient zero signature or finite scalar map fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1342_0_1343",
            "target_file": "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
            "target_script": "scripts/Y5_R10_RAB_R2FR_parent_coefficient_zero_signature_or_finite_scalar_map_fill.py",
            "task": "derive c_R2/c_fRR=0 from the parent action/object language, or fill the finite scalar alpha/lambda/mass/source map as a nonclaim runner input",
            "success_condition": "parent-signed zero coefficient, or a complete nonclaim finite scalar prediction row that can be compared to the private pressure curve and later claim-grade bounds",
            "do_not": "do not claim local GR, do not use the review candidate as public bound evidence, do not invent coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        curve_audit,
        tower_zero,
        acquisition_ledger,
        interpolation_smoke,
        promotion_gate,
        runner_status,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CURVE_AUDIT_PATH, curve_audit)
    write_csv(TOWER_ZERO_PATH, tower_zero)
    write_csv(ACQUISITION_LEDGER_PATH, acquisition_ledger)
    write_csv(INTERPOLATION_SMOKE_PATH, interpolation_smoke)
    write_csv(PROMOTION_GATE_PATH, promotion_gate)
    write_csv(RUNNER_STATUS_PATH, runner_status)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    live_curve = next(row for row in curve_audit if row["artifact_id"] == "CURVE1342_0_live_digitized_placeholder")
    review_curve = next(row for row in curve_audit if row["artifact_id"] == "CURVE1342_1_Lee2020_vector_review_candidate")
    formalization_hits = generated_inside_formalization()
    overall_inputs_ok = (
        sources_ok
        and live_curve["positive_numeric_rows"] == 0
        and review_curve["positive_numeric_rows"] == 390
        and review_curve["claim_true_rows"] == 0
        and tower_zero[-1]["current_result"] == "ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS"
        and runner_status[-1]["verdict"] == "R2FR_BRANCH_BLOCKED_NONCLAIM"
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )
    validation = [
        validation_row(
            "VAL1342_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1342_1_live_curve_placeholder",
            "live claim-facing curve remains placeholder-only",
            live_curve["positive_numeric_rows"] == 0 and live_curve["claim_true_rows"] == 0,
            f"positive_numeric_rows={live_curve['positive_numeric_rows']};claim_true_rows={live_curve['claim_true_rows']}",
        ),
        validation_row(
            "VAL1342_2_review_candidate_private_curve",
            "Lee 2020 review candidate is numeric but nonclaim",
            review_curve["positive_numeric_rows"] == 390 and review_curve["claim_true_rows"] == 0,
            f"positive_numeric_rows={review_curve['positive_numeric_rows']};claim_true_rows={review_curve['claim_true_rows']};status={review_curve['status']}",
        ),
        validation_row(
            "VAL1342_3_interpolation_private_smoke",
            "log-log interpolation smoke runs on private review curve",
            anchor_status.startswith("PRIVATE_PRESSURE_ANCHOR_RECOVERY"),
            anchor_detail,
        ),
        validation_row(
            "VAL1342_4_tower_zero_not_derived",
            "integrated-out tower zero theorem is not promoted",
            tower_zero[-1]["current_result"] == "ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            tower_zero[-1]["gap_or_countermodel"],
        ),
        validation_row(
            "VAL1342_5_promotion_blocked",
            "claim promotion gates remain blocked/nonclaim",
            all(row["claim_allowed"] is False for row in promotion_gate),
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in promotion_gate),
        ),
        validation_row(
            "VAL1342_6_runner_rejects",
            "strict runner status rejects every R2/fR branch",
            runner_status[-1]["verdict"] == "R2FR_BRANCH_BLOCKED_NONCLAIM",
            ";".join(f"{row['run_id']}={row['verdict']}" for row in runner_status),
        ),
        validation_row(
            "VAL1342_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1342_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1342_9_next_target_1343",
            "next target routes to parent scalar coefficient zero or finite scalar map fill",
            next_target[0]["next_id"] == "NEXT1342_0_1343",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1342_10_overall",
            "overall 1342 validation",
            overall_inputs_ok,
            "1342 keeps R2/fR blocked, preserves Lee 2020 curve as private pressure data, and selects parent coefficient route",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1342 does not derive the integrated-out `R2/fR` tower zero theorem. The local second-order filter is still useful, but it does not by itself prove `c_R2 = 0` or `c_fRR = 0`.

**Main progress:** the old bound-curve material has been audited. The live claim-facing curve is still a placeholder, while the Lee 2020 vector candidate has 390 positive numeric rows and passes an internal anchor interpolation smoke check. It remains private pressure data only: every row is `valid_for_claim=false`.

**Decision:** do not spend the next move polishing the curve unless a coefficient exists. Next target is `1343`: derive the parent scalar coefficient zero signature, or fill the finite scalar alpha/lambda/mass/source map as nonclaim input.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Existing Bound Curve Audit
{markdown_table(curve_audit, ["artifact_id", "relative_path", "exists", "row_count", "positive_numeric_rows", "claim_true_rows", "missing_marker_rows", "source_asset_missing_rows", "status", "promotion_effect", "valid_for_claim", "claim_allowed"])}

## Integrated-Out Tower Zero Attempt
{markdown_table(tower_zero, ["attempt_id", "clause", "needed_statement", "current_result", "gap_or_countermodel", "zero_proof_status", "valid_for_claim", "claim_allowed"])}

## Full Curve Acquisition Ledger
{markdown_table(acquisition_ledger, ["acq_id", "artifact_or_target", "current_status", "evidence_quality", "action", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Interpolation Smoke
{markdown_table(interpolation_smoke, ["interp_id", "curve_artifact", "lambda_probe_um", "alpha_interpolated", "method", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Bound Curve Promotion Gate
{markdown_table(promotion_gate, ["gate_id", "requirement", "current_status", "detail", "valid_for_claim", "claim_allowed"])}

## R2FR Runner Status
{markdown_table(runner_status, ["run_id", "input_branch", "accepted_for_scoring", "verdict", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
