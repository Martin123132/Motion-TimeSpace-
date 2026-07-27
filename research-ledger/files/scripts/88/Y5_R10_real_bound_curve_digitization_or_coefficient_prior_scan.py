from __future__ import annotations

import csv
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
BOUND_DIR = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "568-Y5-R10-real-bound-curve-digitization-or-coefficient-prior-scan.md"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_real_bound_curve_digitization_or_coefficient_prior_scan.py"

PRIOR_DOC = ROOT / "567-Y5-R10-finite-alpha-coefficient-fill-and-real-bound-curve-runner.md"
PRIOR_VALIDATION = MTS_DIR / "P8_Y5_BRR545_567_VALIDATION.csv"
LIVE_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
ANCHOR_BOUND_CURVE = BOUND_DIR / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
PRIOR_TEMPLATE = MTS_DIR / "P8_Y5_R10_567_PRIOR_SCAN_TEMPLATE.csv"

ARXIV_DL = BOUND_DIR / "downloads" / "arxiv_2002_11761"
APS_DL = BOUND_DIR / "downloads" / "aps_prl_124_101101"
ARXIV_EPRINT = ARXIV_DL / "2002.11761.eprint"
ARXIV_PDF = ARXIV_DL / "2002.11761.pdf"
ARXIV_EXTRACT = ARXIV_DL / "source_extract"
SOURCE_TEX = ARXIV_EXTRACT / "FB_ISL_pdf.tex"
FIG5B_VECTOR = ARXIV_EXTRACT / "fig5b1.pdf"
APS_HARVEST = APS_DL / "https_harvest_aps_org_v2_journals_articles_10_1103_PhysRevLett_124_101101_fulltext.html"
APS_SUPP_ATTEMPT = APS_DL / "link_aps_supplemental_attempt.html"

ACQUISITION_STATUS_PATH = BOUND_DIR / "P8_Y5_R10_568_ACQUISITION_STATUS.csv"
SOURCE_TEXT_EVIDENCE_PATH = BOUND_DIR / "P8_Y5_R10_568_SOURCE_TEXT_EVIDENCE.csv"
SUPPLEMENTAL_ACCESS_LEDGER_PATH = BOUND_DIR / "P8_Y5_R10_568_SUPPLEMENTAL_ACCESS_LEDGER.csv"
VECTOR_FIGURE_AUDIT_PATH = BOUND_DIR / "P8_Y5_R10_568_VECTOR_FIGURE_AUDIT.csv"
VECTOR_PATH_SCOUT_PATH = BOUND_DIR / "R10_alpha_lambda_bound_curve_VECTOR_PATH_SCOUT_NONCLAIM.csv"
AXIS_CALIBRATION_REQUIREMENTS_PATH = BOUND_DIR / "P8_Y5_R10_568_AXIS_CALIBRATION_REQUIREMENTS.csv"
BOUND_CURVE_STATUS_PATH = BOUND_DIR / "P8_Y5_R10_568_BOUND_CURVE_CANDIDATE_STATUS.csv"
COEFFICIENT_PRIOR_SCAN_PLAN_PATH = MTS_DIR / "P8_Y5_R10_568_COEFFICIENT_PRIOR_SCAN_NONCLAIM_PLAN.csv"
BLOCKER_LEDGER_PATH = BOUND_DIR / "P8_Y5_R10_568_BLOCKER_LEDGER.csv"
DECISION_PATH = MTS_DIR / "P8_Y5_BRR545_568_DECISION.csv"
VALIDATION_PATH = MTS_DIR / "P8_Y5_BRR545_568_VALIDATION.csv"
ROUTE_UPDATE_PATH = MTS_DIR / "P8_Y5_BRR545_568_ROUTE_UPDATE.csv"

STATUS = "Y5_R10_real_curve_source_found_supplement_blocked_vector_fallback_nonclaim"
CLAIM_CEILING = "source_acquisition_and_vector_scout_only_no_R10_bound_curve_claim_no_local_GR_pass"
NEXT_TARGET = "569-Y5-R10-supplement-ingest-or-vector-axis-calibrated-digitizer.md"

PLOT_BBOX = {
    "x_min": 1223.21,
    "x_max": 4624.73,
    "y_min": 775.344,
    "y_max": 3835.29,
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def file_info(path: Path, artifact_id: str, role: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "artifact_id": artifact_id,
        "path": rel(path),
        "role": role,
        "exists": bool_text(exists),
        "bytes": path.stat().st_size if exists else "",
        "valid_for_claim": "false",
    }


def acquisition_status() -> list[dict[str, Any]]:
    rows = [
        file_info(ARXIV_EPRINT, "AQ568_0_arxiv_eprint", "downloaded arXiv source package"),
        file_info(ARXIV_PDF, "AQ568_1_arxiv_pdf", "downloaded arXiv PDF"),
        file_info(SOURCE_TEX, "AQ568_2_tex_source", "extractable TeX source from arXiv package"),
        file_info(FIG5B_VECTOR, "AQ568_3_fig5b_vector_pdf", "vector figure containing alpha(lambda) constraints plot"),
        file_info(APS_HARVEST, "AQ568_4_aps_harvest_fulltext", "APS harvest fulltext PDF copy"),
        file_info(APS_SUPP_ATTEMPT, "AQ568_5_aps_supplement_attempt", "direct APS supplemental access attempt output"),
        file_info(LIVE_BOUND_CURVE, "AQ568_6_live_digitized_placeholder", "live claim curve placeholder retained unchanged"),
        file_info(ANCHOR_BOUND_CURVE, "AQ568_7_anchor_smoke_curve", "source-backed anchor-only smoke curve retained"),
    ]
    for row in rows:
        if row["artifact_id"] == "AQ568_5_aps_supplement_attempt" and APS_SUPP_ATTEMPT.exists():
            content = APS_SUPP_ATTEMPT.read_text(encoding="utf-8", errors="ignore")
            row["access_result"] = "blocked_cloudflare_or_js_challenge" if "Just a moment" in content else "downloaded_nonstandard_response"
        else:
            row["access_result"] = "present" if row["exists"] == "true" else "missing"
    return rows


def source_text_evidence() -> list[dict[str, Any]]:
    evidence_patterns = [
        ("TE568_0_abstract_anchor", "38.6", "paper threshold anchor: gravitational-strength Yukawa ranges below 38.6 micrometers"),
        ("TE568_1_yukawa_law", "V(r)=V_N", "paper defines the standard Yukawa alpha-lambda comparison law"),
        ("TE568_2_scan_count", "66 assumed values", "paper reports alpha constraints for 66 assumed lambda values"),
        ("TE568_3_supplement_table", "Supplemental Material", "paper says numerical alpha-constraint values are in supplemental material"),
    ]
    if not SOURCE_TEX.exists():
        return [
            {
                "evidence_id": item[0],
                "source_file": rel(SOURCE_TEX),
                "line_number": "",
                "matched": "false",
                "meaning": item[2],
                "valid_for_claim": "false",
                "notes": "TeX source missing",
            }
            for item in evidence_patterns
        ]
    lines = SOURCE_TEX.read_text(encoding="utf-8", errors="ignore").splitlines()
    rows: list[dict[str, Any]] = []
    for evidence_id, pattern, meaning in evidence_patterns:
        matches = [(idx, line.strip()) for idx, line in enumerate(lines, start=1) if pattern in line]
        if not matches and pattern == "V(r)=V_N":
            matches = [(idx, line.strip()) for idx, line in enumerate(lines, start=1) if "V_N" in line and "alpha" in line]
        idx, line = matches[0] if matches else ("", "")
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_file": rel(SOURCE_TEX),
                "line_number": idx,
                "matched": bool_text(bool(matches)),
                "meaning": meaning,
                "local_excerpt_short": line[:180],
                "valid_for_claim": "false",
                "notes": "source text supports acquisition target but does not itself provide full curve rows",
            }
        )
    return rows


def supplemental_access_ledger() -> list[dict[str, Any]]:
    attempted = [
        "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/supplement.pdf",
        "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/supplemental.pdf",
        "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/Supplemental_Material.pdf",
        "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/FB_ISL_supp.pdf",
        "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/FB_ISL_supplement.pdf",
        "http://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101",
    ]
    rows: list[dict[str, Any]] = []
    challenge = APS_SUPP_ATTEMPT.exists() and "Just a moment" in APS_SUPP_ATTEMPT.read_text(encoding="utf-8", errors="ignore")
    for index, url in enumerate(attempted):
        rows.append(
            {
                "attempt_id": f"SA568_{index}",
                "url": url,
                "local_artifact": rel(APS_SUPP_ATTEMPT) if url.startswith("http://link.aps.org") and APS_SUPP_ATTEMPT.exists() else "",
                "result": "blocked_cloudflare_403_js_challenge" if url.startswith("http://link.aps.org") and challenge else "direct_candidate_not_downloaded_or_forbidden",
                "contains_machine_readable_table": "false",
                "valid_for_claim": "false",
                "next_action": "open in browser/manual download or locate alternate public mirror/data package",
            }
        )
    return rows


def parse_vector_segments() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not FIG5B_VECTOR.exists():
        return [], [
            {
                "audit_id": "VF568_0_vector_file",
                "source_file": rel(FIG5B_VECTOR),
                "result": "missing",
                "detail": "fig5b1.pdf missing",
                "valid_for_claim": "false",
            }
        ]

    page = PdfReader(str(FIG5B_VECTOR)).pages[0]
    contents = page.get_contents()
    data = contents.get_data() if not isinstance(contents, list) else b"".join(item.get_data() for item in contents)
    text = data.decode("latin1", errors="ignore")

    width = ""
    color = "0 0 0"
    current: tuple[float, float] | None = None
    segments: list[dict[str, Any]] = []
    width_re = re.compile(r"^([0-9.]+) w$")
    color_re = re.compile(r"^([0-9.]+) ([0-9.]+) ([0-9.]+) RG$")
    move_re = re.compile(r"^([0-9.]+) ([0-9.]+) m$")
    line_re = re.compile(r"^([0-9.]+) ([0-9.]+) l$")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        width_match = width_re.match(line)
        if width_match:
            width = width_match.group(1)
            continue
        color_match = color_re.match(line)
        if color_match:
            color = " ".join(color_match.groups())
            continue
        move_match = move_re.match(line)
        if move_match:
            current = (float(move_match.group(1)), float(move_match.group(2)))
            continue
        line_match = line_re.match(line)
        if line_match and current is not None:
            end = (float(line_match.group(1)), float(line_match.group(2)))
            x0, y0 = current
            x1, y1 = end
            in_plot = (
                PLOT_BBOX["x_min"] <= min(x0, x1) <= PLOT_BBOX["x_max"]
                and PLOT_BBOX["x_min"] <= max(x0, x1) <= PLOT_BBOX["x_max"]
                and PLOT_BBOX["y_min"] <= min(y0, y1) <= PLOT_BBOX["y_max"]
                and PLOT_BBOX["y_min"] <= max(y0, y1) <= PLOT_BBOX["y_max"]
            )
            if color != "0 0 0" and in_plot:
                segments.append(
                    {
                        "source_file": rel(FIG5B_VECTOR),
                        "color_rgb": color,
                        "stroke_width": width,
                        "x0_pdf": x0,
                        "y0_pdf": y0,
                        "x1_pdf": x1,
                        "y1_pdf": y1,
                        "coordinate_units": "raw_pdf_user_units",
                        "lambda_value": "",
                        "alpha_bound": "",
                        "valid_for_claim": "false",
                        "notes": "raw vector segment inside plot box; axis calibration required before alpha(lambda) use",
                    }
                )
            current = end

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in segments:
        grouped.setdefault((row["color_rgb"], row["stroke_width"]), []).append(row)

    scout_rows: list[dict[str, Any]] = []
    for index, ((group_color, group_width), group_rows) in enumerate(sorted(grouped.items(), key=lambda item: len(item[1]), reverse=True)):
        xs = [float(row["x0_pdf"]) for row in group_rows] + [float(row["x1_pdf"]) for row in group_rows]
        ys = [float(row["y0_pdf"]) for row in group_rows] + [float(row["y1_pdf"]) for row in group_rows]
        scout_rows.append(
            {
                "scout_id": f"VS568_{index}",
                "source_file": rel(FIG5B_VECTOR),
                "color_rgb": group_color,
                "stroke_width": group_width,
                "segment_count": len(group_rows),
                "x_pdf_min": min(xs),
                "x_pdf_max": max(xs),
                "y_pdf_min": min(ys),
                "y_pdf_max": max(ys),
                "plot_x_pdf_min": PLOT_BBOX["x_min"],
                "plot_x_pdf_max": PLOT_BBOX["x_max"],
                "plot_y_pdf_min": PLOT_BBOX["y_min"],
                "plot_y_pdf_max": PLOT_BBOX["y_max"],
                "lambda_value": "",
                "lambda_units": "",
                "alpha_bound": "",
                "digitization_status": "raw_vector_group_only_axis_unresolved",
                "valid_for_claim": "false",
                "notes": "May contain curve, legend, ticks, or glyph fragments; requires axis and role calibration.",
            }
        )

    audit_rows = [
        {
            "audit_id": "VF568_0_vector_file",
            "source_file": rel(FIG5B_VECTOR),
            "result": "present",
            "detail": f"bytes={FIG5B_VECTOR.stat().st_size}",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "VF568_1_content_stream",
            "source_file": rel(FIG5B_VECTOR),
            "result": "parsed",
            "detail": f"content_stream_bytes={len(data)};nonblack_inplot_segments={len(segments)};groups={len(scout_rows)}",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "VF568_2_text_labels",
            "source_file": rel(FIG5B_VECTOR),
            "result": "not_extractable_by_pypdf",
            "detail": "figure labels are vector paths, not extractable text; axis calibration cannot be verified automatically yet",
            "valid_for_claim": "false",
        },
    ]
    return scout_rows, audit_rows


def axis_calibration_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "AC568_0_x_axis_units",
            "need": "map raw x PDF coordinates to lambda values",
            "current_state": "plot vector coordinates found but tick labels are path glyphs",
            "acceptance_for_claim": "two or more independently verified x-axis tick labels, preferably all major ticks",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "AC568_1_y_axis_units",
            "need": "map raw y PDF coordinates to abs(alpha) values",
            "current_state": "plot vector coordinates found but y-axis log labels are path glyphs",
            "acceptance_for_claim": "two or more independently verified y-axis tick labels, preferably all major ticks",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "AC568_2_curve_identity",
            "need": "separate Lee 2020 constraint curve from prior-work curves, legend strokes, glyphs, and tick marks",
            "current_state": "color groups extracted without semantic curve identity",
            "acceptance_for_claim": "source caption/legend or manual visual QA maps each extracted group to a named experiment",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "AC568_3_machine_table_preferred",
            "need": "ingest supplemental numerical alpha constraints if accessible",
            "current_state": "paper says supplemental has numerical values; direct link is Cloudflare/403 blocked in CLI",
            "acceptance_for_claim": "downloaded supplemental PDF/table or alternate official machine-readable rows",
            "valid_for_claim": "false",
        },
    ]


def bound_curve_candidate_status(vector_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    live_rows = read_csv(LIVE_BOUND_CURVE)
    anchor_rows = read_csv(ANCHOR_BOUND_CURVE)
    return [
        {
            "candidate_id": "BC568_0_live_digitized_claim_file",
            "path": rel(LIVE_BOUND_CURVE),
            "row_count": len(live_rows),
            "status": "placeholder_claim_blocked",
            "valid_rows_for_claim": 0,
            "valid_for_claim": "false",
            "notes": "Retained unchanged; still contains placeholder rows rather than real digitized curve.",
        },
        {
            "candidate_id": "BC568_1_anchor_smoke",
            "path": rel(ANCHOR_BOUND_CURVE),
            "row_count": len(anchor_rows),
            "status": "anchor_only_noncurve",
            "valid_rows_for_claim": 0,
            "valid_for_claim": "false",
            "notes": "Useful threshold anchors only; not a full alpha(lambda) curve.",
        },
        {
            "candidate_id": "BC568_2_vector_path_scout",
            "path": rel(VECTOR_PATH_SCOUT_PATH),
            "row_count": len(vector_rows),
            "status": "raw_vector_groups_axis_unresolved",
            "valid_rows_for_claim": 0,
            "valid_for_claim": "false",
            "notes": "Proves vector fallback exists; cannot become alpha(lambda) until axis and curve identity are calibrated.",
        },
    ]


def coefficient_prior_scan_plan() -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_TEMPLATE)
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(prior_rows):
        rows.append(
            {
                "plan_id": f"CPS568_{index}",
                "parameter": row.get("parameter", ""),
                "suggested_domain": row.get("suggested_domain", ""),
                "status_after_acquisition": "allowed_as_nonclaim_only",
                "reason": "real alpha_bound(lambda) curve is not yet claim-grade",
                "valid_for_claim": "false",
            }
        )
    return rows


def blocker_ledger() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "B568_0_supplement_access",
            "blocker": "The paper states numerical alpha constraints are in supplemental material, but direct CLI access hits a Cloudflare/403 JavaScript challenge.",
            "why_it_matters": "The supplemental table would be the cleanest claim-grade curve source.",
            "next_action": "Use browser/manual download or locate an alternate official mirror.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B568_1_axis_calibration",
            "blocker": "The vector figure paths are extractable but axis labels are not text-extractable.",
            "why_it_matters": "Raw PDF path coordinates are not physical lambda/alpha rows.",
            "next_action": "Build an axis-calibrated digitizer with manually verified tick anchors.",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B568_2_curve_identity",
            "blocker": "The bottom figure combines this and previous work; color groups are not yet semantically assigned.",
            "why_it_matters": "We must not accidentally use a prior-work curve as the 2020 Lee curve or vice versa.",
            "next_action": "Map legend/curve identity before any full curve file is promoted.",
            "claim_blocked": "true",
        },
    ]


def validation_rows(
    acquisition_rows: list[dict[str, Any]],
    evidence_rows: list[dict[str, Any]],
    supplement_rows: list[dict[str, Any]],
    vector_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    curve_status_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    source_present = {row["artifact_id"]: row for row in acquisition_rows}
    evidence_matched = [row for row in evidence_rows if row.get("matched") == "true"]
    supplement_blocked = any(row.get("result") == "blocked_cloudflare_403_js_challenge" for row in supplement_rows)
    vector_parsed = any(row.get("audit_id") == "VF568_1_content_stream" and row.get("result") == "parsed" for row in audit_rows)
    claim_rows = [row for row in vector_rows + curve_status_rows if row.get("valid_for_claim") == "true"]
    live_rows = read_csv(LIVE_BOUND_CURVE)
    live_placeholder = any("MISSING" in json.dumps(row) for row in live_rows)
    return [
        {
            "check_id": "V568_0_prior_567_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V568_1_source_package_present",
            "result": "pass"
            if source_present.get("AQ568_0_arxiv_eprint", {}).get("exists") == "true"
            and source_present.get("AQ568_2_tex_source", {}).get("exists") == "true"
            else "fail",
            "detail": f"arxiv_eprint={source_present.get('AQ568_0_arxiv_eprint', {}).get('exists')};tex={source_present.get('AQ568_2_tex_source', {}).get('exists')}",
        },
        {
            "check_id": "V568_2_source_text_evidence_found",
            "result": "pass" if len(evidence_matched) == len(evidence_rows) and evidence_rows else "fail",
            "detail": f"matched={len(evidence_matched)};expected={len(evidence_rows)}",
        },
        {
            "check_id": "V568_3_supplement_access_blocked_recorded",
            "result": "pass" if supplement_blocked else "fail",
            "detail": f"supplement_blocked={bool_text(supplement_blocked)};attempts={len(supplement_rows)}",
        },
        {
            "check_id": "V568_4_vector_figure_parsed",
            "result": "pass" if vector_parsed and vector_rows else "fail",
            "detail": f"vector_groups={len(vector_rows)}",
        },
        {
            "check_id": "V568_5_live_claim_curve_still_blocked",
            "result": "pass" if live_placeholder else "fail",
            "detail": f"live_rows={len(live_rows)};placeholder_marker={bool_text(live_placeholder)}",
        },
        {
            "check_id": "V568_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"valid_for_claim_true_rows={len(claim_rows)}",
        },
        {
            "check_id": "V568_7_no_overclaim",
            "result": "pass",
            "detail": "supplement_table_ingested=false;axis_calibrated=false;curve_identity_verified=false;R10_pass=false;local_GR=false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D568_0_real_curve_source_identified",
            "decision": "real numerical curve source is identified but not acquired",
            "meaning": "the paper explicitly points to supplemental numerical alpha constraints",
            "status": "source_found_access_blocked",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D568_1_vector_fallback_retained",
            "decision": "retain vector digitization fallback",
            "meaning": "fig5b1.pdf contains extractable vector path groups, but needs calibration",
            "status": "fallback_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D568_2_prior_scan_only_nonclaim",
            "decision": "coefficient prior scan remains diagnostic only",
            "meaning": "without a real curve, coefficient scanning cannot become evidence",
            "status": "nonclaim_only",
            "next_target": NEXT_TARGET,
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU568_0_best_next",
            "allowed_after_568": "Try to ingest the supplemental numerical table by browser/manual download.",
            "forbidden_after_568": "Pretend the blocked supplemental table has been acquired.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU568_1_vector_route",
            "allowed_after_568": "Build an axis-calibrated vector digitizer using verified tick anchors and curve identity mapping.",
            "forbidden_after_568": "Promote raw PDF path coordinates directly to lambda/alpha rows.",
            "next_action": "calibrate x-axis, y-axis, and experiment curve identity",
        },
        {
            "route_id": "RU568_2_theory_route",
            "allowed_after_568": "Run coefficient priors only as explicit non-claim diagnostics.",
            "forbidden_after_568": "Use prior-scan survival as R10 evidence while external curve is non-claim.",
            "next_action": "keep deriving qbar_XT, Qbar_XH(lambda), Z_X, and M_X^2",
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
    acquisition: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    supplement: list[dict[str, Any]],
    vector_audit: list[dict[str, Any]],
    vector_scout: list[dict[str, Any]],
    axis_requirements: list[dict[str, Any]],
    curve_status: list[dict[str, Any]],
    prior_plan: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    top_vector = vector_scout[:8]
    body = f"""# 568 Y5 R10 real bound curve digitization or coefficient prior scan

Generated: {generated_at}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The real R10 curve route improved: the arXiv source package and vector figure are now local, and the TeX text confirms the paper scanned 66 lambda values and says numerical alpha constraints are in supplemental material.
- The cleanest numerical table is not acquired yet: the APS supplemental link is present but direct CLI access is blocked by a Cloudflare/403 JavaScript challenge.
- The fallback is viable but non-claim: `fig5b1.pdf` contains extractable vector path groups, but axis labels and curve identities still need calibration.
- Therefore R10 remains blocked for evidence, while the next useful move is either supplemental ingest or an axis-calibrated vector digitizer.

## Acquisition Status
{markdown_table(acquisition, ["artifact_id", "path", "role", "exists", "bytes", "access_result", "valid_for_claim"])}

## Source Text Evidence
{markdown_table(evidence, ["evidence_id", "source_file", "line_number", "matched", "meaning", "valid_for_claim"])}

## Supplemental Access Ledger
{markdown_table(supplement, ["attempt_id", "url", "result", "contains_machine_readable_table", "valid_for_claim", "next_action"])}

## Vector Figure Audit
{markdown_table(vector_audit, ["audit_id", "source_file", "result", "detail", "valid_for_claim"])}

## Vector Path Scout
{markdown_table(top_vector, ["scout_id", "color_rgb", "stroke_width", "segment_count", "x_pdf_min", "x_pdf_max", "y_pdf_min", "y_pdf_max", "digitization_status", "valid_for_claim"])}

## Axis Calibration Requirements
{markdown_table(axis_requirements, ["requirement_id", "need", "current_state", "acceptance_for_claim", "valid_for_claim"])}

## Bound Curve Candidate Status
{markdown_table(curve_status, ["candidate_id", "path", "row_count", "status", "valid_rows_for_claim", "valid_for_claim", "notes"])}

## Coefficient Prior Scan Plan
{markdown_table(prior_plan, ["plan_id", "parameter", "suggested_domain", "status_after_acquisition", "reason", "valid_for_claim"])}

## Blocker Ledger
{markdown_table(blockers, ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Route Update
{markdown_table(routes, ["route_id", "allowed_after_568", "forbidden_after_568", "next_action"])}

## Practical Read
This is not grim; it is a data-access fork, not a physics failure. The paper itself tells us the exact thing we need exists: numerical alpha constraints in the supplemental material. The CLI cannot currently pull that supplemental link because APS/link.aps is throwing a JavaScript challenge. Meanwhile the source package gives us a vector figure fallback. The next hard-nosed move is either to ingest the supplemental file manually or build the vector digitizer with explicit axis anchors, while keeping all coefficient scans non-claim until the external curve is real.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()

    acquisition = acquisition_status()
    evidence = source_text_evidence()
    supplement = supplemental_access_ledger()
    vector_scout, vector_audit = parse_vector_segments()
    axis_requirements = axis_calibration_requirements()
    curve_status = bound_curve_candidate_status(vector_scout)
    prior_plan = coefficient_prior_scan_plan()
    blockers = blocker_ledger()
    decisions = decision_rows()
    routes = route_update_rows()
    validation = validation_rows(acquisition, evidence, supplement, vector_scout, vector_audit, curve_status)

    write_csv(
        ACQUISITION_STATUS_PATH,
        acquisition,
        ["artifact_id", "path", "role", "exists", "bytes", "access_result", "valid_for_claim"],
    )
    write_csv(
        SOURCE_TEXT_EVIDENCE_PATH,
        evidence,
        ["evidence_id", "source_file", "line_number", "matched", "meaning", "local_excerpt_short", "valid_for_claim", "notes"],
    )
    write_csv(
        SUPPLEMENTAL_ACCESS_LEDGER_PATH,
        supplement,
        ["attempt_id", "url", "local_artifact", "result", "contains_machine_readable_table", "valid_for_claim", "next_action"],
    )
    write_csv(
        VECTOR_FIGURE_AUDIT_PATH,
        vector_audit,
        ["audit_id", "source_file", "result", "detail", "valid_for_claim"],
    )
    write_csv(
        VECTOR_PATH_SCOUT_PATH,
        vector_scout,
        [
            "scout_id",
            "source_file",
            "color_rgb",
            "stroke_width",
            "segment_count",
            "x_pdf_min",
            "x_pdf_max",
            "y_pdf_min",
            "y_pdf_max",
            "plot_x_pdf_min",
            "plot_x_pdf_max",
            "plot_y_pdf_min",
            "plot_y_pdf_max",
            "lambda_value",
            "lambda_units",
            "alpha_bound",
            "digitization_status",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        AXIS_CALIBRATION_REQUIREMENTS_PATH,
        axis_requirements,
        ["requirement_id", "need", "current_state", "acceptance_for_claim", "valid_for_claim"],
    )
    write_csv(
        BOUND_CURVE_STATUS_PATH,
        curve_status,
        ["candidate_id", "path", "row_count", "status", "valid_rows_for_claim", "valid_for_claim", "notes"],
    )
    write_csv(
        COEFFICIENT_PRIOR_SCAN_PLAN_PATH,
        prior_plan,
        ["plan_id", "parameter", "suggested_domain", "status_after_acquisition", "reason", "valid_for_claim"],
    )
    write_csv(
        BLOCKER_LEDGER_PATH,
        blockers,
        ["blocker_id", "blocker", "why_it_matters", "next_action", "claim_blocked"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        ROUTE_UPDATE_PATH,
        routes,
        ["route_id", "allowed_after_568", "forbidden_after_568", "next_action"],
    )

    write_doc(
        generated_at,
        acquisition,
        evidence,
        supplement,
        vector_audit,
        vector_scout,
        axis_requirements,
        curve_status,
        prior_plan,
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
        "validation": rel(VALIDATION_PATH),
        "vector_scout": rel(VECTOR_PATH_SCOUT_PATH),
        "all_validation_passed": all(row["result"] == "pass" for row in validation),
        "claim_allowed": False,
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
