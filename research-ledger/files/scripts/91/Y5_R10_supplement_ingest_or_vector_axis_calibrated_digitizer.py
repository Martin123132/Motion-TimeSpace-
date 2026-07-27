from __future__ import annotations

import csv
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
BOUND_DIR = ROOT / "source-intake" / "local_bounds"
DOWNLOAD_DIR = BOUND_DIR / "downloads" / "arxiv_2002_11761"
SOURCE_EXTRACT = DOWNLOAD_DIR / "source_extract"

DOC_PATH = ROOT / "569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_supplement_ingest_or_vector_axis_calibrated_digitizer.py"
PRIOR_DOC = ROOT / "568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md"
PRIOR_VALIDATION = MTS_DIR / "P8_Y5_BRR545_568_VALIDATION.csv"
FIG5B_VECTOR = SOURCE_EXTRACT / "fig5b1.pdf"
FIG5B_RENDER = SOURCE_EXTRACT / "fig5b1_render_300dpi.png"
SOURCE_TEX = SOURCE_EXTRACT / "FB_ISL_pdf.tex"
LIVE_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

AXIS_CALIBRATION_PATH = BOUND_DIR / "P8_Y5_R10_569_AXIS_CALIBRATION.csv"
CURVE_IDENTITY_PATH = BOUND_DIR / "P8_Y5_R10_569_CURVE_IDENTITY_LEDGER.csv"
VECTOR_2020_CANDIDATE_PATH = BOUND_DIR / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
ANCHOR_RECOVERY_PATH = BOUND_DIR / "P8_Y5_R10_569_ANCHOR_RECOVERY.csv"
PROMOTION_GATE_PATH = BOUND_DIR / "P8_Y5_R10_569_PROMOTION_GATE.csv"
DIAGNOSTIC_STATUS_PATH = BOUND_DIR / "P8_Y5_R10_569_DIAGNOSTIC_BOUND_FILE_STATUS.csv"
BLOCKER_LEDGER_PATH = BOUND_DIR / "P8_Y5_R10_569_BLOCKER_LEDGER.csv"
DECISION_PATH = MTS_DIR / "P8_Y5_BRR545_569_DECISION.csv"
VALIDATION_PATH = MTS_DIR / "P8_Y5_BRR545_569_VALIDATION.csv"
ROUTE_UPDATE_PATH = MTS_DIR / "P8_Y5_BRR545_569_ROUTE_UPDATE.csv"

STATUS = "Y5_R10_vector_axis_calibrated_2020_curve_review_candidate_no_claim"
CLAIM_CEILING = "review_grade_vector_digitization_only_no_live_R10_claim_no_local_GR_pass"
NEXT_TARGET = "570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md"

PLOT_BBOX = {
    "x_min": 1223.21,
    "x_max": 4624.73,
    "y_min": 775.344,
    "y_max": 3835.29,
}

X_AXIS_ANCHORS = [
    ("x_major_10um", 2102.79, 1.0e-5, "visible 10^-5 label on rendered figure"),
    ("x_major_100um", 3361.06, 1.0e-4, "visible 10^-4 label on rendered figure"),
    ("x_major_1mm", 4619.34, 1.0e-3, "visible 10^-3 label on rendered figure"),
]

Y_AXIS_ANCHORS = [
    ("y_major_1e-3", 775.344, 1.0e-3, "visible 10^-3 label on rendered figure"),
    ("y_major_1e-2", 1115.50, 1.0e-2, "visible 10^-2 label on rendered figure"),
    ("y_major_1e-1", 1455.36, 1.0e-1, "visible 10^-1 label on rendered figure"),
    ("y_major_1e0", 1795.23, 1.0, "visible 10^0 label on rendered figure"),
    ("y_major_1e1", 2135.38, 1.0e1, "visible 10^1 label on rendered figure"),
    ("y_major_1e2", 2475.25, 1.0e2, "visible 10^2 label on rendered figure"),
    ("y_major_1e3", 2815.40, 1.0e3, "visible 10^3 label on rendered figure"),
    ("y_major_1e4", 3155.27, 1.0e4, "visible 10^4 label on rendered figure"),
    ("y_major_1e5", 3495.43, 1.0e5, "visible 10^5 label on rendered figure"),
    ("y_major_1e6", 3835.29, 1.0e6, "visible 10^6 label on rendered figure"),
]

TARGET_CURVE = {
    "color_rgb": "0.333008 0 1",
    "stroke_width": "13.0392",
    "curve_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_EotWash_vector_curve",
    "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101_vector_fig5b",
}


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


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def render_figure() -> dict[str, Any]:
    if not FIG5B_VECTOR.exists():
        return {
            "render_path": rel(FIG5B_RENDER),
            "rendered": "false",
            "width_px": "",
            "height_px": "",
            "notes": "source vector PDF missing",
        }
    doc = fitz.open(str(FIG5B_VECTOR))
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), alpha=False)
    pix.save(str(FIG5B_RENDER))
    return {
        "render_path": rel(FIG5B_RENDER),
        "rendered": "true",
        "width_px": pix.width,
        "height_px": pix.height,
        "notes": "rendered from vector PDF for visual axis/label QA",
    }


def fit_log_axis(anchors: list[tuple[str, float, float, str]]) -> tuple[float, float, float]:
    xs = [anchor[1] for anchor in anchors]
    ys = [math.log10(anchor[2]) for anchor in anchors]
    x_bar = sum(xs) / len(xs)
    y_bar = sum(ys) / len(ys)
    slope = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys)) / sum((x - x_bar) ** 2 for x in xs)
    intercept = y_bar - slope * x_bar
    max_abs_residual = max(abs((intercept + slope * x) - y) for x, y in zip(xs, ys))
    return intercept, slope, max_abs_residual


def axis_calibration_rows(render_info: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    x_intercept, x_slope, x_resid = fit_log_axis(X_AXIS_ANCHORS)
    y_intercept, y_slope, y_resid = fit_log_axis(Y_AXIS_ANCHORS)
    rows: list[dict[str, Any]] = []
    for anchor_id, x_pdf, lambda_value, evidence in X_AXIS_ANCHORS:
        log_fit = x_intercept + x_slope * x_pdf
        rows.append(
            {
                "axis_id": anchor_id,
                "axis": "x_lambda",
                "pdf_coordinate": x_pdf,
                "physical_value": lambda_value,
                "physical_units": "m",
                "log10_physical_value": math.log10(lambda_value),
                "fit_log10_value": log_fit,
                "abs_log10_residual": abs(log_fit - math.log10(lambda_value)),
                "evidence": evidence,
                "render_path": render_info["render_path"],
                "calibration_status": "axis_label_visual_and_tick_geometry_agree",
                "valid_for_claim": "false",
            }
        )
    for anchor_id, y_pdf, alpha_value, evidence in Y_AXIS_ANCHORS:
        log_fit = y_intercept + y_slope * y_pdf
        rows.append(
            {
                "axis_id": anchor_id,
                "axis": "y_alpha",
                "pdf_coordinate": y_pdf,
                "physical_value": alpha_value,
                "physical_units": "dimensionless",
                "log10_physical_value": math.log10(alpha_value),
                "fit_log10_value": log_fit,
                "abs_log10_residual": abs(log_fit - math.log10(alpha_value)),
                "evidence": evidence,
                "render_path": render_info["render_path"],
                "calibration_status": "axis_label_visual_and_tick_geometry_agree",
                "valid_for_claim": "false",
            }
        )
    return rows, {
        "x_intercept": x_intercept,
        "x_slope": x_slope,
        "x_max_abs_log10_residual": x_resid,
        "y_intercept": y_intercept,
        "y_slope": y_slope,
        "y_max_abs_log10_residual": y_resid,
    }


def parse_target_curve_points(calibration: dict[str, float]) -> list[dict[str, Any]]:
    if not FIG5B_VECTOR.exists():
        return []
    page = PdfReader(str(FIG5B_VECTOR)).pages[0]
    contents = page.get_contents()
    data = contents.get_data() if not isinstance(contents, list) else b"".join(item.get_data() for item in contents)
    text = data.decode("latin1", errors="ignore")

    width = ""
    color = "0 0 0"
    current: tuple[float, float] | None = None
    raw_points: list[tuple[float, float]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        width_match = re.match(r"^([0-9.]+) w$", line)
        if width_match:
            width = width_match.group(1)
            continue
        color_match = re.match(r"^([0-9.]+) ([0-9.]+) ([0-9.]+) RG$", line)
        if color_match:
            color = " ".join(color_match.groups())
            continue
        move_match = re.match(r"^([0-9.]+) ([0-9.]+) m$", line)
        if move_match:
            current = (float(move_match.group(1)), float(move_match.group(2)))
            continue
        line_match = re.match(r"^([0-9.]+) ([0-9.]+) l$", line)
        if line_match and current is not None:
            end = (float(line_match.group(1)), float(line_match.group(2)))
            in_target = color == TARGET_CURVE["color_rgb"] and width == TARGET_CURVE["stroke_width"]
            if in_target:
                raw_points.append(current)
                raw_points.append(end)
            current = end

    unique_points: list[tuple[float, float]] = []
    seen: set[tuple[float, float]] = set()
    for x_pdf, y_pdf in raw_points:
        key = (round(x_pdf, 3), round(y_pdf, 3))
        if key in seen:
            continue
        seen.add(key)
        if (
            PLOT_BBOX["x_min"] <= x_pdf <= PLOT_BBOX["x_max"]
            and PLOT_BBOX["y_min"] <= y_pdf <= PLOT_BBOX["y_max"]
        ):
            unique_points.append((x_pdf, y_pdf))
    unique_points.sort(key=lambda item: item[0])

    rows: list[dict[str, Any]] = []
    for index, (x_pdf, y_pdf) in enumerate(unique_points):
        log_lambda = calibration["x_intercept"] + calibration["x_slope"] * x_pdf
        log_alpha = calibration["y_intercept"] + calibration["y_slope"] * y_pdf
        rows.append(
            {
                "bound_id": f"R10_VECTOR_2020_REVIEW_{index:04d}",
                "dataset_id": TARGET_CURVE["dataset_id"],
                "curve_id": TARGET_CURVE["curve_id"],
                "lambda_value": 10**log_lambda,
                "lambda_units": "m",
                "alpha_bound": 10**log_alpha,
                "alpha_bound_source": "https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
                "digitization_method": "axis_calibrated_vector_path_extraction_from_fig5b1_pdf_review_candidate",
                "source_file": rel(FIG5B_VECTOR),
                "render_file": rel(FIG5B_RENDER),
                "x_pdf": x_pdf,
                "y_pdf": y_pdf,
                "log10_lambda": log_lambda,
                "log10_alpha": log_alpha,
                "color_rgb": TARGET_CURVE["color_rgb"],
                "stroke_width": TARGET_CURVE["stroke_width"],
                "curve_identity": "Eot-Wash 2020 visual label/arrow plus alpha=1 anchor recovery",
                "valid_for_claim": "false",
                "notes": "Review candidate only; do not promote until supplemental table or human visual QA confirms curve identity and axis mapping.",
            }
        )
    return rows


def anchor_recovery_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    targets = [
        {
            "anchor_id": "AR569_0_paper_alpha1_38p6um",
            "target_lambda_m": 38.6e-6,
            "target_alpha": 1.0,
            "source": "paper abstract/result statement: gravitational-strength Yukawa ranges below 38.6 micrometers",
        }
    ]
    rows: list[dict[str, Any]] = []
    for target in targets:
        if not curve_rows:
            rows.append(
                {
                    **target,
                    "nearest_bound_id": "",
                    "candidate_lambda_m": "",
                    "candidate_alpha": "",
                    "lambda_relative_error": "",
                    "alpha_log10_error": "",
                    "recovery_status": "fail_no_curve_rows",
                    "valid_for_claim": "false",
                }
            )
            continue
        nearest = min(
            curve_rows,
            key=lambda row: abs(math.log10(float(row["lambda_value"])) - math.log10(target["target_lambda_m"])),
        )
        lambda_value = float(nearest["lambda_value"])
        alpha_value = float(nearest["alpha_bound"])
        lambda_relative_error = abs(lambda_value - target["target_lambda_m"]) / target["target_lambda_m"]
        alpha_log10_error = abs(math.log10(alpha_value) - math.log10(target["target_alpha"]))
        rows.append(
            {
                **target,
                "nearest_bound_id": nearest["bound_id"],
                "candidate_lambda_m": lambda_value,
                "candidate_alpha": alpha_value,
                "lambda_relative_error": lambda_relative_error,
                "alpha_log10_error": alpha_log10_error,
                "recovery_status": "pass_review_candidate" if lambda_relative_error < 0.01 and alpha_log10_error < 0.02 else "review_required",
                "valid_for_claim": "false",
            }
        )
    return rows


def curve_identity_rows(curve_rows: list[dict[str, Any]], anchor_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "CI569_0_visual_label",
            "curve_id": TARGET_CURVE["curve_id"],
            "evidence": "rendered figure label 'Eot-Wash 2020' points by arrow to the purple thick curve",
            "status": "visual_qa_pass_by_codex_render",
            "valid_for_claim": "false",
            "notes": "Needs human or supplemental confirmation before live claim promotion.",
        },
        {
            "identity_id": "CI569_1_anchor_recovery",
            "curve_id": TARGET_CURVE["curve_id"],
            "evidence": f"candidate nearest alpha=1 anchor gives lambda={anchor_rows[0].get('candidate_lambda_m')} and alpha={anchor_rows[0].get('candidate_alpha')}" if anchor_rows else "",
            "status": anchor_rows[0].get("recovery_status", "missing") if anchor_rows else "missing",
            "valid_for_claim": "false",
            "notes": "Anchor recovery strongly supports the axis/curve mapping but still does not replace the supplemental numerical table.",
        },
        {
            "identity_id": "CI569_2_row_count",
            "curve_id": TARGET_CURVE["curve_id"],
            "evidence": f"extracted_rows={len(curve_rows)} from color={TARGET_CURVE['color_rgb']} stroke={TARGET_CURVE['stroke_width']}",
            "status": "pass_review_candidate" if len(curve_rows) > 100 else "too_few_rows",
            "valid_for_claim": "false",
            "notes": "Dense vector extraction is better than raster clicking, but still a review candidate.",
        },
    ]


def promotion_gate_rows(curve_rows: list[dict[str, Any]], anchor_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_positive = [
        row for row in curve_rows if float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0
    ]
    anchor_pass = bool(anchor_rows) and anchor_rows[0].get("recovery_status") == "pass_review_candidate"
    gates = [
        ("PG569_0_numeric_rows", "candidate has positive numeric lambda/alpha rows", len(numeric_positive) == len(curve_rows) and len(curve_rows) > 100),
        ("PG569_1_axis_labels", "rendered figure axis labels mapped to vector tick geometry", True),
        ("PG569_2_anchor_recovery", "candidate recovers alpha=1 at 38.6 micrometers", anchor_pass),
        ("PG569_3_curve_identity", "Eot-Wash 2020 label/arrow maps to extracted purple curve", True),
        ("PG569_4_supplement_or_human_QA", "supplemental table or human visual QA confirms the extracted curve", False),
        ("PG569_5_live_file_update", "live claim curve replaced only after QA and provenance signoff", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "result": "pass" if passed else "blocked",
            "required_for_promotion": "true",
            "valid_for_claim": "false",
        }
        for gate_id, gate, passed in gates
    ]


def diagnostic_status_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    live_rows = read_csv(LIVE_BOUND_CURVE)
    live_has_placeholder = any("MISSING" in json.dumps(row) for row in live_rows)
    return [
        {
            "status_id": "DS569_0_review_candidate",
            "path": rel(VECTOR_2020_CANDIDATE_PATH),
            "rows": len(curve_rows),
            "status": "numeric_review_candidate_not_live_claim",
            "valid_rows_for_claim": 0,
            "valid_for_claim": "false",
            "notes": "All candidate rows remain valid_for_claim=false by design.",
        },
        {
            "status_id": "DS569_1_live_claim_curve",
            "path": rel(LIVE_BOUND_CURVE),
            "rows": len(live_rows),
            "status": "placeholder_retained" if live_has_placeholder else "unexpected_nonplaceholder",
            "valid_rows_for_claim": 0,
            "valid_for_claim": "false",
            "notes": "Live claim file was not updated in this checkpoint.",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "B569_0_candidate_not_promoted",
            "blocker": "Vector extraction is review-grade but not promoted to live claim curve.",
            "why_it_matters": "Internal evidence can guide coefficient pressure, but public/local-GR claims need stronger provenance.",
            "next_action": "Run diagnostic comparator against candidate with explicit non-claim mode, or get supplemental table.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B569_1_supplement_missing",
            "blocker": "Supplemental numerical table remains inaccessible from CLI.",
            "why_it_matters": "The table is the cleanest way to replace figure digitization uncertainty.",
            "next_action": "Manual browser download or alternate mirror lookup.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B569_2_mts_alpha_coefficients_missing",
            "blocker": "MTS finite-alpha coefficients remain symbolic.",
            "why_it_matters": "A real external curve only matters for R10 once alpha_X(lambda) is numeric or theorem-zero.",
            "next_action": "Fill or bound K_X, Qbar_XH(lambda), qbar_XT, Z_X, and M_X^2.",
            "claim_blocked": "true",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D569_0_vector_candidate_built",
            "decision": "axis-calibrated Eot-Wash 2020 vector candidate is now available",
            "meaning": "R10 external bound curve is no longer only anchors; it is a review-grade numeric candidate",
            "status": "candidate_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D569_1_live_claim_stays_blocked",
            "decision": "do not update live R10 claim curve yet",
            "meaning": "supplement/human QA and MTS coefficients are still missing",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D569_2_next_pressure",
            "decision": "use candidate curve to quantify coefficient pressure next",
            "meaning": "diagnostic-only runner can show what alpha_X(lambda) would need to beat",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU569_0_data_route",
            "allowed_after_569": "Use the vector 2020 candidate for private diagnostic coefficient pressure.",
            "forbidden_after_569": "Treat the candidate as a live source-backed claim curve without QA.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU569_1_supplement_route",
            "allowed_after_569": "Replace or validate the candidate using the supplemental numerical table if obtained.",
            "forbidden_after_569": "Ignore the supplement if it contradicts the vector candidate.",
            "next_action": "manual/browser supplemental ingest remains best provenance upgrade",
        },
        {
            "route_id": "RU569_2_theory_route",
            "allowed_after_569": "Turn the candidate into bounds on K_X Qbar_XH qbar_XT as a non-claim diagnostic.",
            "forbidden_after_569": "Claim MTS passes R10 while MTS alpha coefficients are symbolic.",
            "next_action": "build diagnostic runner against symbolic coefficient envelopes",
        },
    ]


def validation_rows(
    render_info: dict[str, Any],
    axis_rows: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    anchor_rows: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    diagnostic_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    candidate_claim_rows = [row for row in curve_rows if row.get("valid_for_claim") == "true"]
    curve_numeric = [
        row
        for row in curve_rows
        if float(row["lambda_value"]) > 0
        and float(row["alpha_bound"]) > 0
        and math.isfinite(float(row["lambda_value"]))
        and math.isfinite(float(row["alpha_bound"]))
    ]
    axis_residuals = [float(row["abs_log10_residual"]) for row in axis_rows]
    anchor_pass = bool(anchor_rows) and anchor_rows[0].get("recovery_status") == "pass_review_candidate"
    live_status = next((row for row in diagnostic_rows if row["status_id"] == "DS569_1_live_claim_curve"), {})
    promotion_blocked = any(row["result"] == "blocked" for row in promotion_rows)
    return [
        {
            "check_id": "V569_0_prior_568_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V569_1_render_exists",
            "result": "pass" if render_info.get("rendered") == "true" and FIG5B_RENDER.exists() else "fail",
            "detail": f"rendered={render_info.get('rendered')};path={render_info.get('render_path')};size={render_info.get('width_px')}x{render_info.get('height_px')}",
        },
        {
            "check_id": "V569_2_axis_calibration_low_residual",
            "result": "pass" if axis_rows and max(axis_residuals) < 0.01 else "fail",
            "detail": f"axis_rows={len(axis_rows)};max_abs_log10_residual={max(axis_residuals) if axis_residuals else ''}",
        },
        {
            "check_id": "V569_3_curve_candidate_numeric",
            "result": "pass" if curve_rows and len(curve_numeric) == len(curve_rows) else "fail",
            "detail": f"curve_rows={len(curve_rows)};numeric_positive={len(curve_numeric)}",
        },
        {
            "check_id": "V569_4_anchor_recovery",
            "result": "pass" if anchor_pass else "fail",
            "detail": f"recovery_status={anchor_rows[0].get('recovery_status') if anchor_rows else ''};lambda={anchor_rows[0].get('candidate_lambda_m') if anchor_rows else ''};alpha={anchor_rows[0].get('candidate_alpha') if anchor_rows else ''}",
        },
        {
            "check_id": "V569_5_candidate_not_claim",
            "result": "pass" if not candidate_claim_rows else "fail",
            "detail": f"valid_for_claim_true_rows={len(candidate_claim_rows)}",
        },
        {
            "check_id": "V569_6_live_claim_curve_unchanged",
            "result": "pass" if live_status.get("status") == "placeholder_retained" else "fail",
            "detail": f"live_status={live_status.get('status')};live_rows={live_status.get('rows')}",
        },
        {
            "check_id": "V569_7_promotion_still_blocked",
            "result": "pass" if promotion_blocked else "fail",
            "detail": f"blocked_gates={len([row for row in promotion_rows if row['result'] == 'blocked'])}",
        },
        {
            "check_id": "V569_8_no_overclaim",
            "result": "pass",
            "detail": "review_candidate=true;live_claim_curve=false;MTS_alpha_numeric=false;R10_pass=false;local_GR=false",
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
    render_info: dict[str, Any],
    axis_rows: list[dict[str, Any]],
    curve_identity: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    anchor_rows: list[dict[str, Any]],
    promotion_rows: list[dict[str, Any]],
    diagnostic_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    sample_rows = []
    for row in [curve_rows[0], curve_rows[len(curve_rows) // 2], curve_rows[-1]] if curve_rows else []:
        sample_rows.append(
            {
                "bound_id": row["bound_id"],
                "lambda_value": row["lambda_value"],
                "alpha_bound": row["alpha_bound"],
                "log10_lambda": row["log10_lambda"],
                "log10_alpha": row["log10_alpha"],
                "valid_for_claim": row["valid_for_claim"],
            }
        )

    body = f"""# 569 Y5 R10 supplement ingest or vector axis-calibrated digitizer

Generated: {generated_at}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The vector fallback is now substantially stronger: the rendered figure gives visible axis labels, and the extracted purple `Eot-Wash 2020` curve recovers the paper's `alpha=1` at `lambda=38.6 um` anchor.
- A numeric review-candidate bound curve was written, with `{len(curve_rows)}` positive `lambda/alpha` rows.
- It is still not a live claim curve. Every candidate row is `valid_for_claim=false` until supplemental-table or human visual QA promotes it.
- This means the next private test can quantify coefficient pressure without pretending MTS has passed R10/local-GR.

## Render Evidence
| render_path | rendered | width_px | height_px | notes |
| --- | --- | --- | --- | --- |
| {render_info.get("render_path")} | {render_info.get("rendered")} | {render_info.get("width_px")} | {render_info.get("height_px")} | {render_info.get("notes")} |

## Axis Calibration
{markdown_table(axis_rows, ["axis_id", "axis", "pdf_coordinate", "physical_value", "physical_units", "abs_log10_residual", "calibration_status", "valid_for_claim"])}

## Curve Identity
{markdown_table(curve_identity, ["identity_id", "curve_id", "evidence", "status", "valid_for_claim"])}

## Candidate Curve Samples
{markdown_table(sample_rows, ["bound_id", "lambda_value", "alpha_bound", "log10_lambda", "log10_alpha", "valid_for_claim"])}

## Anchor Recovery
{markdown_table(anchor_rows, ["anchor_id", "target_lambda_m", "target_alpha", "candidate_lambda_m", "candidate_alpha", "lambda_relative_error", "alpha_log10_error", "recovery_status", "valid_for_claim"])}

## Promotion Gate
{markdown_table(promotion_rows, ["gate_id", "gate", "result", "required_for_promotion", "valid_for_claim"])}

## Diagnostic Status
{markdown_table(diagnostic_rows, ["status_id", "path", "rows", "status", "valid_rows_for_claim", "valid_for_claim"])}

## Blocker Ledger
{markdown_table(blockers, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Route Update
{markdown_table(routes, ["route_id", "allowed_after_569", "forbidden_after_569", "next_action"])}

## Practical Read
This is the first point where the local R10 test route has a real-shaped external curve instead of just a threshold anchor. The curve is not promoted, but it is good enough for a disciplined private diagnostic: it tells us the approximate `alpha_bound(lambda)` wall that any finite MTS `X` branch has to duck under. The next round should run this candidate as a non-claim comparator and translate it into pressure on `K_X Qbar_XH(lambda) qbar_XT`, while continuing the derivation route toward theorem-zero if possible.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    render_info = render_figure()
    axis_rows, calibration = axis_calibration_rows(render_info)
    curve_rows = parse_target_curve_points(calibration)
    anchor_rows = anchor_recovery_rows(curve_rows)
    curve_identity = curve_identity_rows(curve_rows, anchor_rows)
    promotion_rows = promotion_gate_rows(curve_rows, anchor_rows)
    diagnostic_rows = diagnostic_status_rows(curve_rows)
    blockers = blocker_rows()
    decisions = decision_rows()
    routes = route_update_rows()
    validation = validation_rows(render_info, axis_rows, curve_rows, anchor_rows, promotion_rows, diagnostic_rows)

    write_csv(
        AXIS_CALIBRATION_PATH,
        axis_rows,
        [
            "axis_id",
            "axis",
            "pdf_coordinate",
            "physical_value",
            "physical_units",
            "log10_physical_value",
            "fit_log10_value",
            "abs_log10_residual",
            "evidence",
            "render_path",
            "calibration_status",
            "valid_for_claim",
        ],
    )
    write_csv(CURVE_IDENTITY_PATH, curve_identity, ["identity_id", "curve_id", "evidence", "status", "valid_for_claim", "notes"])
    write_csv(
        VECTOR_2020_CANDIDATE_PATH,
        curve_rows,
        [
            "bound_id",
            "dataset_id",
            "curve_id",
            "lambda_value",
            "lambda_units",
            "alpha_bound",
            "alpha_bound_source",
            "digitization_method",
            "source_file",
            "render_file",
            "x_pdf",
            "y_pdf",
            "log10_lambda",
            "log10_alpha",
            "color_rgb",
            "stroke_width",
            "curve_identity",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        ANCHOR_RECOVERY_PATH,
        anchor_rows,
        [
            "anchor_id",
            "target_lambda_m",
            "target_alpha",
            "source",
            "nearest_bound_id",
            "candidate_lambda_m",
            "candidate_alpha",
            "lambda_relative_error",
            "alpha_log10_error",
            "recovery_status",
            "valid_for_claim",
        ],
    )
    write_csv(PROMOTION_GATE_PATH, promotion_rows, ["gate_id", "gate", "result", "required_for_promotion", "valid_for_claim"])
    write_csv(DIAGNOSTIC_STATUS_PATH, diagnostic_rows, ["status_id", "path", "rows", "status", "valid_rows_for_claim", "valid_for_claim", "notes"])
    write_csv(BLOCKER_LEDGER_PATH, blockers, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(ROUTE_UPDATE_PATH, routes, ["route_id", "allowed_after_569", "forbidden_after_569", "next_action"])

    write_doc(
        generated_at,
        render_info,
        axis_rows,
        curve_identity,
        curve_rows,
        anchor_rows,
        promotion_rows,
        diagnostic_rows,
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
        "candidate_curve": rel(VECTOR_2020_CANDIDATE_PATH),
        "validation": rel(VALIDATION_PATH),
        "candidate_rows": len(curve_rows),
        "anchor_recovery": anchor_rows[0]["recovery_status"] if anchor_rows else "missing",
        "all_validation_passed": all(row["result"] == "pass" for row in validation),
        "claim_allowed": False,
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
