from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
R10_SOURCES = ROOT / "source-intake" / "r10-sources" / "3012"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3012"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3012-Y5-R2FR-R10-first-source-backed-bound-rows-and-dryrun-schema-under-AX1090.md"

ARXIV_ABS_URL = "https://arxiv.org/abs/2002.11761"
ARXIV_PDF_URL = "https://arxiv.org/pdf/2002.11761"
ARXIV_SOURCE_URL = "https://arxiv.org/e-print/2002.11761"
APS_SUPPLEMENTAL_URL = "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101"
APS_DOI_URL = "https://doi.org/10.1103/PhysRevLett.124.101101"

PDF = R10_SOURCES / "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124_101101_arxiv_2002_11761.pdf"
SOURCE_TAR = R10_SOURCES / "arxiv_2002_11761_source.tar"
EXTRACTED = R10_SOURCES / "source_extracted"
TEX = EXTRACTED / "FB_ISL_pdf.tex"
FIG5B = EXTRACTED / "fig5b1.pdf"
APS_LOG = R10_SOURCES / "aps_supplemental_fetch_attempt_3012.log"
LIVE_CURVE_TARGET = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3012_SOURCE_ACQUISITION_LEDGER.csv",
    "source_facts": RESIDUALS / "P8_Y5_R2FR_3012_SOURCE_FACTS.csv",
    "figure_audit": RESIDUALS / "P8_Y5_R2FR_3012_FIGURE_VECTOR_AUDIT.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv",
    "dryrun_schema": RESIDUALS / "P8_Y5_R2FR_3012_QLOC_TO_ALPHA_DRYRUN_SCHEMA.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_3012_R10_DRYRUN_RESULTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3012_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3012_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3012_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3012_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3012_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "bound_rows_copy": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_3012_NONCLAIM.csv",
    "dryrun_schema_copy": LOCAL_BOUNDS / "q_loc_to_alpha_R10_dryrun_schema_3012_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3012_R10_QLOC_TO_YUKAWA_KERNEL_OR_SUPPLEMENT_IMPORT_NEXT.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_size(path: Path) -> int:
    return path.stat().st_size if path.exists() and path.is_file() else 0


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        read_rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def find_tex_fact(fact_id: str, needle: str, description: str) -> dict[str, Any]:
    lines = text(TEX).splitlines()
    for index, line in enumerate(lines, start=1):
        if needle in line:
            return base(
                {
                    "fact_id": fact_id,
                    "source_path": str(TEX),
                    "line_number": index,
                    "description": description,
                    "matched_text": line.strip(),
                    "status": "FOUND",
                }
            )
    return base(
        {
            "fact_id": fact_id,
            "source_path": str(TEX),
            "line_number": "MISSING",
            "description": description,
            "matched_text": needle,
            "status": "MISSING_TEXT_ANCHOR",
        }
    )


def figure_vector_stats(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "figure_exists": False,
            "pypdf_available": False,
            "page_count": 0,
            "operation_count": 0,
            "stroke_path_count": 0,
            "stroke_color_count": 0,
            "extractable_text_chars": 0,
            "axis_calibrated": False,
            "status": "MISSING_FIGURE",
        }
    try:
        from pypdf import PdfReader
        from pypdf.generic import ContentStream
    except Exception:
        return {
            "figure_exists": True,
            "pypdf_available": False,
            "page_count": "UNKNOWN",
            "operation_count": "UNKNOWN",
            "stroke_path_count": "UNKNOWN",
            "stroke_color_count": "UNKNOWN",
            "extractable_text_chars": "UNKNOWN",
            "axis_calibrated": False,
            "status": "PYPDF_NOT_AVAILABLE_VECTOR_AUDIT_SKIPPED",
        }
    reader = PdfReader(str(path))
    page = reader.pages[0]
    extracted_text = page.extract_text() or ""
    content = ContentStream(page.get_contents(), reader)
    color = (0.0, 0.0, 0.0)
    current: list[tuple[Any, ...]] = []
    path_count = 0
    colors: set[tuple[float, float, float]] = set()
    for operands, operator in content.operations:
        op = operator.decode("latin1") if isinstance(operator, bytes) else operator
        if op == "RG":
            color = tuple(float(value) for value in operands)
        elif op in {"m", "l", "c"}:
            current.append((op, *operands))
        elif op == "S":
            if current:
                path_count += 1
                colors.add(color)
            current = []
        elif op in {"f", "q", "Q"}:
            current = []
    return {
        "figure_exists": True,
        "pypdf_available": True,
        "page_count": len(reader.pages),
        "operation_count": len(content.operations),
        "stroke_path_count": path_count,
        "stroke_color_count": len(colors),
        "extractable_text_chars": len(extracted_text.strip()),
        "axis_calibrated": False,
        "status": "VECTOR_PATHS_PRESENT_AXIS_LABELS_NOT_TEXT_EXTRACTABLE",
    }


source_ledger = [
    base(
        {
            "source_id": "SRC3012_0_arxiv_abs",
            "source_url": ARXIV_ABS_URL,
            "local_path": "web-only",
            "exists": True,
            "bytes": "not_applicable",
            "sha256": "not_applicable",
            "status": "BROWSED_METADATA_CONFIRMED",
            "notes": "arXiv abstract page provides title, submission date, PDF/source links, abstract range statement and DOI links",
        }
    ),
    base(
        {
            "source_id": "SRC3012_1_arxiv_pdf",
            "source_url": ARXIV_PDF_URL,
            "local_path": str(PDF),
            "exists": PDF.exists(),
            "bytes": file_size(PDF),
            "sha256": sha256(PDF),
            "status": "CACHED" if PDF.exists() else "MISSING_LOCAL_CACHE",
            "notes": "primary arXiv PDF cache",
        }
    ),
    base(
        {
            "source_id": "SRC3012_2_arxiv_source_tar",
            "source_url": ARXIV_SOURCE_URL,
            "local_path": str(SOURCE_TAR),
            "exists": SOURCE_TAR.exists(),
            "bytes": file_size(SOURCE_TAR),
            "sha256": sha256(SOURCE_TAR),
            "status": "CACHED" if SOURCE_TAR.exists() else "MISSING_LOCAL_CACHE",
            "notes": "arXiv TeX source tar cache",
        }
    ),
    base(
        {
            "source_id": "SRC3012_3_extracted_tex",
            "source_url": ARXIV_SOURCE_URL,
            "local_path": str(TEX),
            "exists": TEX.exists(),
            "bytes": file_size(TEX),
            "sha256": sha256(TEX),
            "status": "EXTRACTED" if TEX.exists() else "MISSING_EXTRACTED_TEX",
            "notes": "TeX contains figure captions, Yukawa definition and supplement statement",
        }
    ),
    base(
        {
            "source_id": "SRC3012_4_fig5b1_vector_pdf",
            "source_url": ARXIV_SOURCE_URL,
            "local_path": str(FIG5B),
            "exists": FIG5B.exists(),
            "bytes": file_size(FIG5B),
            "sha256": sha256(FIG5B),
            "status": "EXTRACTED_VECTOR_FIGURE" if FIG5B.exists() else "MISSING_FIGURE",
            "notes": "bottom panel of Fig. 5 bound curve figure, vector paths but axis labels not text-extractable",
        }
    ),
    base(
        {
            "source_id": "SRC3012_5_aps_supplement_attempt",
            "source_url": APS_SUPPLEMENTAL_URL,
            "local_path": str(APS_LOG),
            "exists": APS_LOG.exists(),
            "bytes": file_size(APS_LOG),
            "sha256": sha256(APS_LOG),
            "status": "FETCH_ATTEMPT_403_FORBIDDEN" if "403" in text(APS_LOG) else "FETCH_STATUS_NOT_CONFIRMED",
            "notes": "supplement is the preferred numerical alpha-constraint source, but direct unauthenticated fetch failed",
        }
    ),
]

source_facts = [
    find_tex_fact(
        "FACT3012_0_yukawa_potential",
        "V(r)=V_N(r) [1+\\alpha \\exp({-r/\\lambda})]",
        "Yukawa parameterization defines alpha and lambda against Newtonian potential",
    ),
    find_tex_fact(
        "FACT3012_1_fig5_bottom_limits",
        "corresponding 95\\% confidence upper limits on $|\\alpha|$",
        "Fig. 5 bottom panel is the alpha(lambda) upper-limit plot",
    ),
    find_tex_fact(
        "FACT3012_2_66_lambda_scan",
        "66 assumed values of  $\\lambda$ between $5\\,\\mu$m and $9\\,$mm",
        "analysis scanned 66 lambda values",
    ),
    find_tex_fact(
        "FACT3012_3_grav_strength_threshold",
        "gravitational-strength Yukawa interaction must have $\\lambda<38.6\\,\\mu$m",
        "alpha=1 threshold anchor in the paper text",
    ),
    find_tex_fact(
        "FACT3012_4_supplement_numerical_values",
        "constraints on $+\\alpha$ and $-\\alpha$ are given in Supplemental Material",
        "supplement is the proper numerical source for signed alpha constraints",
    ),
    find_tex_fact(
        "FACT3012_5_supplement_torque_values",
        "See Supplemental Material at XXXX for numerical values of the gravitational torques",
        "TeX reference confirms supplemental numerical values exist, but publisher URL is required",
    ),
]

fig_stats = figure_vector_stats(FIG5B)
figure_audit = [
    base(
        {
            "figure_id": "FIG3012_0_fig5b1",
            "figure_path": str(FIG5B),
            "figure_exists": fig_stats["figure_exists"],
            "pypdf_available": fig_stats["pypdf_available"],
            "page_count": fig_stats["page_count"],
            "operation_count": fig_stats["operation_count"],
            "stroke_path_count": fig_stats["stroke_path_count"],
            "stroke_color_count": fig_stats["stroke_color_count"],
            "extractable_text_chars": fig_stats["extractable_text_chars"],
            "axis_calibrated": fig_stats["axis_calibrated"],
            "status": fig_stats["status"],
            "claim_policy": "vector paths alone do not become data rows without calibrated axes and curve identity",
        }
    )
]

bound_rows = [
    base(
        {
            "curve_row_id": "R10B3012_0_EotWash_2020_alpha1_anchor",
            "row_kind": "source_text_anchor",
            "source_url": ARXIV_ABS_URL,
            "source_path": str(TEX),
            "lambda_value": "3.86e-5",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "alpha_units": "dimensionless",
            "confidence": "95%",
            "extraction_method": "paper text alpha=1 gravitational-strength threshold from 38.6 microm",
            "full_curve_row": False,
            "valid_bound_curve_row": False,
            "status": "ANCHOR_ONLY_NON_CURVE",
            "blocker": "one alpha=1 threshold does not provide interpolation over arbitrary lambda/support",
        }
    ),
    base(
        {
            "curve_row_id": "R10B3012_1_EotWash_2007_alpha1_anchor",
            "row_kind": "continuity_anchor_from_2410",
            "source_url": "https://arxiv.org/abs/hep-ph/0611184",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2410_BOUND_CURVE_ADMISSION_GATE.csv"),
            "lambda_value": "5.6e-5",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "alpha_units": "dimensionless",
            "confidence": "95%",
            "extraction_method": "prior local 2410 anchor ledger, not re-promoted",
            "full_curve_row": False,
            "valid_bound_curve_row": False,
            "status": "ANCHOR_ONLY_NON_CURVE",
            "blocker": "older continuity anchor is not a dense modern curve",
        }
    ),
    base(
        {
            "curve_row_id": "R10B3012_2_APS_supplement_full_curve",
            "row_kind": "preferred_numerical_source",
            "source_url": APS_SUPPLEMENTAL_URL,
            "source_path": str(APS_LOG),
            "lambda_value": "MISSING_66_LAMBDA_VALUES",
            "lambda_units": "m",
            "alpha_bound": "MISSING_SIGNED_ALPHA_CONSTRAINTS",
            "alpha_units": "dimensionless",
            "confidence": "95%",
            "extraction_method": "direct APS supplemental fetch attempted; received 403",
            "full_curve_row": False,
            "valid_bound_curve_row": False,
            "status": "SUPPLEMENTAL_ACCESS_BLOCKED",
            "blocker": "numerical signed constraints live in APS supplement, but unauthenticated fetch failed",
        }
    ),
    base(
        {
            "curve_row_id": "R10B3012_3_fig5_vector_digitization_candidate",
            "row_kind": "figure_vector_candidate",
            "source_url": ARXIV_SOURCE_URL,
            "source_path": str(FIG5B),
            "lambda_value": "MISSING_AXIS_CALIBRATION",
            "lambda_units": "m",
            "alpha_bound": "MISSING_CURVE_IDENTITY",
            "alpha_units": "dimensionless",
            "confidence": "95%",
            "extraction_method": "vector path audit only; no calibrated digitization performed",
            "full_curve_row": False,
            "valid_bound_curve_row": False,
            "status": "VECTOR_PRESENT_NOT_DIGITIZED",
            "blocker": "axis labels are not text-extractable and multiple colored curves require calibrated extraction",
        }
    ),
]

dryrun_schema = [
    base(
        {
            "schema_id": "DRY3012_0_required_prediction_row",
            "artifact": "R10_q_loc_to_alpha_prediction_row",
            "required_fields": "prediction_id; lambda_X_m; alpha_predicted; alpha_units; K_R10_source_path; q_loc_profile_path; C_q_to_alpha; coupling_coefficients; source_normalization; uncertainty; valid_prediction_row",
            "current_values": "MISSING_K_R10; MISSING_lambda_X; MISSING_C_q_to_alpha; MISSING_q_loc_profile; MISSING_COUPLING_COEFFICIENTS",
            "units_policy": "lambda_X in m; alpha_predicted dimensionless; all source-normalization factors declared",
            "failure_mode": "prediction row is invalid until parent projection coefficients are real",
        }
    ),
    base(
        {
            "schema_id": "DRY3012_1_required_bound_row",
            "artifact": "R10_alpha_lambda_bound_curve_DIGITIZED",
            "required_fields": "bound_id; lambda_value; lambda_units; alpha_bound; alpha_units; source_url; source_path; extraction_method; confidence; full_curve_row; valid_bound_curve_row",
            "current_values": "anchors present; full curve missing; supplement blocked; vector figure not calibrated",
            "units_policy": "lambda_value > 0 m; alpha_bound > 0 dimensionless; no MISSING markers for valid rows",
            "failure_mode": "bound row is invalid for claim unless full_curve_row=true and valid_bound_curve_row=true",
        }
    ),
    base(
        {
            "schema_id": "DRY3012_2_comparison_rule",
            "artifact": "R10_alpha_comparator",
            "required_fields": "matching lambda interpolation range; no extrapolation; alpha_predicted_abs <= alpha_bound; uncertainty policy; no cancellation",
            "current_values": "not runnable because both full curve and prediction row are missing",
            "units_policy": "compare dimensionless alpha at matched lambda support only",
            "failure_mode": "runner returns BLOCKED_NONCLAIM, not pass/fail physics",
        }
    ),
]

dryrun_results = [
    base(
        {
            "dryrun_id": "RUN3012_0_bound_curve_gate",
            "check": "any valid full-curve bound rows present",
            "passed": False,
            "observed": "0 valid full-curve rows; anchors are noncurve",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "RUN3012_1_prediction_gate",
            "check": "valid q_loc-to-alpha prediction row present",
            "passed": False,
            "observed": "K_R10, lambda_X and C_q_to_alpha missing",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "RUN3012_2_supplement_gate",
            "check": "APS supplemental numerical constraints acquired",
            "passed": False,
            "observed": "direct APS fetch returned 403",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "RUN3012_3_vector_digitization_gate",
            "check": "Fig. 5 vector paths calibrated into data rows",
            "passed": False,
            "observed": "vector paths present but axis labels/curve identities not calibrated",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "RUN3012_4_claim_gate",
            "check": "R10 claim allowed",
            "passed": False,
            "observed": "bound curve and MTS prediction are both incomplete",
            "result_status": "CLAIM_FORBIDDEN",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3012_0_source_cache",
            "gate": "arXiv PDF/source and Fig. 5 vector source are cached locally",
            "result": PDF.exists() and SOURCE_TAR.exists() and TEX.exists() and FIG5B.exists(),
            "notes": "source cache exists under source-intake/r10-sources/3012",
        }
    ),
    base(
        {
            "gate_id": "GATE3012_1_text_facts",
            "gate": "TeX source anchors are found",
            "result": all(row["status"] == "FOUND" for row in source_facts),
            "notes": "Yukawa definition, Fig. 5 limit role, 66 lambda scan, threshold and supplement facts are anchored",
        }
    ),
    base(
        {
            "gate_id": "GATE3012_2_no_live_curve_write",
            "gate": "live R10_alpha_lambda_bound_curve_DIGITIZED.csv is not written by 3012",
            "result": LIVE_CURVE_TARGET not in OUTPUTS.values() and LIVE_CURVE_TARGET not in BRANCH_OUTPUTS.values(),
            "notes": "3012 writes only NONCLAIM curve rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3012_3_anchors_nonclaim",
            "gate": "alpha=1 anchors remain nonclaim noncurve",
            "result": all(row["status"] == "ANCHOR_ONLY_NON_CURVE" and not boolish(row["valid_for_claim"]) for row in bound_rows[:2]),
            "notes": "anchors are useful for plumbing but not sufficient for alpha(lambda) scoring",
        }
    ),
    base(
        {
            "gate_id": "GATE3012_4_vector_not_promoted",
            "gate": "vector figure paths are not promoted without calibration",
            "result": figure_audit[0]["axis_calibrated"] is False and not boolish(bound_rows[3]["valid_for_claim"]),
            "notes": "no screen/pixel curve fabrication",
        }
    ),
    base(
        {
            "gate_id": "GATE3012_5_R10_claim",
            "gate": "R10 pass claim allowed",
            "result": False,
            "notes": "full curve, q_loc projection and source normalization are missing",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3012_0_status",
            "decision": "3012 acquires and caches the arXiv R10 source package, but does not obtain the publisher supplemental numerical curve.",
            "rationale": "The proper numerical source is the APS supplement; direct unauthenticated access returned 403, and Fig. 5 vector paths are not axis-calibrated data rows.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3012_1_bound_rows",
            "decision": "Only two alpha=1 anchors are staged, both valid_for_claim=false.",
            "rationale": "The 38.6 microm statement is useful as a threshold check but cannot replace the 66-lambda alpha(lambda) constraint table.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3012_2_next_route",
            "decision": "Move to q_loc-to-Yukawa projection derivation while leaving a parallel supplement/manual-digitization import route open.",
            "rationale": "Even with the curve, R10 cannot score MTS until K_R10, lambda_X and C_q_to_alpha are derived.",
            "claim_allowed_after_decision": False,
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3012_0_3013",
            "priority": "selected_primary",
            "target_doc": "3013-Y5-R2FR-R10-q_loc-to-Yukawa-projection-kernel-or-calibrated-curve-import-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_R10_q_loc_to_Yukawa_projection_kernel_or_calibrated_curve_import_under_AX1090_3013.py",
            "mission": "Derive the q_loc/Delta_K/coupling-vector to Yukawa alpha(lambda) projection kernel, while preserving a side route for APS supplemental import or calibrated Fig. 5 digitization.",
            "success_condition": "a fail-closed R10 prediction row exists with explicit K_R10, lambda_X, source normalization and units, or a theorem/blocker states exactly which parent coefficient is missing.",
            "fallback_if_fail": "write the exact missing parent coefficient/projection map as a blocker and keep R10 nonclaim",
            "guardrails": "no R10 pass claim; no alpha curve from uncalibrated vector paths; no anchor-only curve; no hidden coupling; no formalization-workbench edits; no GitHub action",
        }
    )
]

write_csv(OUTPUTS["sources"], source_ledger)
write_csv(OUTPUTS["source_facts"], source_facts)
write_csv(OUTPUTS["figure_audit"], figure_audit)
write_csv(OUTPUTS["bound_rows"], bound_rows)
write_csv(OUTPUTS["dryrun_schema"], dryrun_schema)
write_csv(OUTPUTS["dryrun_results"], dryrun_results)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("bound_rows_copy", "bound_rows"),
    ("dryrun_schema_copy", "dryrun_schema"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3012_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_ledger
    + source_facts
    + figure_audit
    + bound_rows
    + dryrun_schema
    + dryrun_results
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3012_00_source_cache",
        "passed": PDF.exists() and SOURCE_TAR.exists() and TEX.exists() and FIG5B.exists(),
        "requirement": "arXiv PDF/source, TeX and Fig. 5 vector PDF are cached locally",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3012_01_source_hashes",
        "passed": all(row["sha256"] != "MISSING" for row in source_ledger if row["local_path"] not in {"web-only"}),
        "requirement": "cached local sources have SHA256 hashes",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3012_02_text_facts",
        "passed": all(row["status"] == "FOUND" for row in source_facts),
        "requirement": "required TeX source facts are found",
        "evidence": OUTPUTS["source_facts"].name,
    },
    {
        "validation_id": "VAL3012_03_aps_blocker_recorded",
        "passed": "403" in text(APS_LOG) and not (R10_SOURCES / "aps_supplemental_fetch_attempt_3012.tmp").exists(),
        "requirement": "APS supplement access failure is recorded and no partial download is used",
        "evidence": str(APS_LOG),
    },
    {
        "validation_id": "VAL3012_04_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3012_05_anchors_positive_nonclaim",
        "passed": all(
            float(row["lambda_value"]) > 0
            and float(row["alpha_bound"]) > 0
            and not boolish(row["valid_for_claim"])
            and not boolish(row["valid_bound_curve_row"])
            for row in bound_rows[:2]
        ),
        "requirement": "anchor rows have positive numbers but remain nonclaim noncurve",
        "evidence": "R10B3012_0 and R10B3012_1",
    },
    {
        "validation_id": "VAL3012_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in bound_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are not valid_for_claim",
        "evidence": OUTPUTS["bound_rows"].name,
    },
    {
        "validation_id": "VAL3012_07_no_claim_rows",
        "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in claim_rows),
        "requirement": "no 3012 row is valid for claim or claim allowed",
        "evidence": "base() claim fields",
    },
    {
        "validation_id": "VAL3012_08_live_curve_not_written",
        "passed": LIVE_CURVE_TARGET not in all_generated,
        "requirement": "live R10_alpha_lambda_bound_curve_DIGITIZED.csv is not modified by this checkpoint",
        "evidence": "output target list",
    },
    {
        "validation_id": "VAL3012_09_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3012_10_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3012_11_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3013-Y5_R2FR") is False
        and next_target[0]["target_doc"].startswith("3013-Y5-R2FR-R10"),
        "requirement": "next target selects R10 projection-kernel derivation or calibrated curve import",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3012_99_overall",
        "passed": overall_pass,
        "requirement": "all 3012 validation checks pass",
        "evidence": "aggregate of VAL3012_00 through VAL3012_11",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3012 — R10 First Source-Backed Bound Rows and Dry-Run Schema under AX1090

Status: `Y5_R2FR_3012_R10_sources_cached_supplement_blocked_nonclaim_dryrun_schema_staged_3013_next`

## Verdict

3012 makes real progress but **does not** unlock an R10 claim.

The good part: the arXiv PDF/source package for Lee et al. 2020 is cached locally, the TeX source anchors the Yukawa definition, the 66-lambda scan, the Fig. 5 alpha-limit role, and the alpha=1 threshold at `38.6 microm`.

The hard blocker: the paper says the numerical signed alpha constraints live in the APS Supplemental Material. Direct unauthenticated fetch of that supplement returned `403`, so 3012 refuses to fabricate a curve. The extracted Fig. 5 bottom-panel PDF contains vector paths, but the axis labels are not text-extractable and the curves are not calibrated into physical `lambda, alpha` rows.

## Source Acquisition Ledger

{md_table(source_ledger, ["source_id", "exists", "bytes", "status", "notes"])}

## Source Facts

{md_table(source_facts, ["fact_id", "line_number", "description", "status"])}

## Figure Vector Audit

{md_table(figure_audit, ["figure_id", "operation_count", "stroke_path_count", "stroke_color_count", "extractable_text_chars", "axis_calibrated", "status"])}

## R10 Bound Rows

{md_table(bound_rows, ["curve_row_id", "row_kind", "lambda_value", "alpha_bound", "status", "valid_bound_curve_row"])}

## Dry-Run Schema

{md_table(dryrun_schema, ["schema_id", "artifact", "current_values", "failure_mode"])}

## Dry-Run Results

{md_table(dryrun_results, ["dryrun_id", "check", "passed", "observed", "result_status"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["source_facts"]}`
- `{OUTPUTS["figure_audit"]}`
- `{OUTPUTS["bound_rows"]}`
- `{OUTPUTS["dryrun_schema"]}`
- `{OUTPUTS["dryrun_results"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["bound_rows_copy"]}`
- `{BRANCH_OUTPUTS["dryrun_schema_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No R10 pass claim.
- No live `R10_alpha_lambda_bound_curve_DIGITIZED.csv` overwrite.
- No anchor-only curve claim.
- No uncalibrated vector-figure digitization claim.
- No hidden-coupling or bound-inversion shortcut.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
