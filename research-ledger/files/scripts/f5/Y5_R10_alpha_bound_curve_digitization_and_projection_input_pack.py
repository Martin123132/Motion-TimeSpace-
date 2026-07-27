from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOWNLOADS = LOCAL_BOUNDS / "downloads"
DOC = ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def as_float(value: object) -> float | None:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1034_0_1033_next",
            "source-intake/mts_residuals/P8_Y5_R10_1033_NEXT_TARGET.csv",
            "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "1033 handoff naming the 1034 bound-curve and projection-pack target.",
        ),
        (
            "SRC1034_1_1033_acquisition",
            "source-intake/mts_residuals/P8_Y5_R10_1033_R10_ACQUISITION_TEMPLATE.csv",
            "R10ACQ1033_0_alpha_bound_curve",
            "1033 missing-input ledger for alpha_bound(lambda), K_X, Qbar_XH, tau_R10, c_g, and alpha_predicted.",
        ),
        (
            "SRC1034_2_1033_profile_contract",
            "source-intake/mts_residuals/P8_Y5_R10_1033_R10_PROFILE_NORMALIZATION_CONTRACT.csv",
            "R10PC1033_6_score_gate",
            "1033 score-gate contract requiring numeric sourced prediction and bound rows.",
        ),
        (
            "SRC1034_3_live_bound_placeholder",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "R10_BOUND_PLACEHOLDER_0",
            "Live bound file deliberately remains a placeholder, not a claim curve.",
        ),
        (
            "SRC1034_4_vector_review_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "Existing axis-calibrated vector extraction from the 2020 Fig. 5b bound curve.",
        ),
        (
            "SRC1034_5_vector_candidate_qa",
            "source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
            "QA570_1_anchor_recovery",
            "QA ledger showing anchor recovery but blocked promotion.",
        ),
        (
            "SRC1034_6_axis_calibration",
            "source-intake/local_bounds/P8_Y5_R10_569_AXIS_CALIBRATION.csv",
            "x_major_10um",
            "Axis calibration used by the vector review candidate.",
        ),
        (
            "SRC1034_7_supplement_attempts",
            "source-intake/local_bounds/P8_Y5_R10_568_SUPPLEMENTAL_ACCESS_LEDGER.csv",
            "blocked_cloudflare_403_js_challenge",
            "Official APS supplemental access attempt ledger.",
        ),
        (
            "SRC1034_8_arxiv_eprint",
            "source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.eprint",
            "",
            "Downloaded arXiv source package.",
        ),
        (
            "SRC1034_9_arxiv_pdf",
            "source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf",
            "",
            "Downloaded arXiv PDF.",
        ),
        (
            "SRC1034_10_fig5b_vector_pdf",
            "source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/fig5b1.pdf",
            "",
            "Vector figure containing the R10 alpha(lambda) constraint curve.",
        ),
        (
            "SRC1034_11_tex_source",
            "source-intake/local_bounds/downloads/arxiv_2002_11761/source_extract/FB_ISL_pdf.tex",
            "Supplemental Material",
            "TeX source confirms the paper points to supplemental numerical values but does not include them.",
        ),
        (
            "SRC1034_12_mts_prediction_placeholder",
            "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
            "MTS-side alpha prediction remains placeholder-only.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists and needle else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str((not needle and exists) or (needle in text)).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def external_source_rows() -> list[dict[str, str]]:
    return [
        {
            "external_id": "EXT1034_0_arxiv_abs",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "source_role": "modern Eot-Wash 2020 source anchor",
            "evidence_summary": "Abstract gives separations 52 micrometers to 3.0 mm and gravitational-strength Yukawa range limit lambda < 38.6 micrometers.",
            "machine_readable_curve": "false",
            "local_artifact": relative(DOWNLOADS / "arxiv_2002_11761" / "2002.11761.eprint"),
            "acquisition_status": "source_package_present_no_numeric_supplement_table",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1034_1_arxiv_pdf",
            "source_url": "https://arxiv.org/pdf/2002.11761",
            "source_role": "force-law, scan-range, and Fig. 5b bound-curve convention",
            "evidence_summary": "Paper defines V=VN[1+alpha exp(-r/lambda)], scans 66 lambda values between 5 micrometers and 9 mm, and plots 95 percent CL |alpha| limits.",
            "machine_readable_curve": "false",
            "local_artifact": relative(DOWNLOADS / "arxiv_2002_11761" / "2002.11761.pdf"),
            "acquisition_status": "pdf_present_text_and_vector_figure_available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1034_2_arxiv_source_fig5b",
            "source_url": "https://arxiv.org/e-print/2002.11761",
            "source_role": "source package containing vector Fig. 5b file",
            "evidence_summary": "Source package contains fig5b1.pdf and TeX, but no official numeric alpha(lambda) table.",
            "machine_readable_curve": "false",
            "local_artifact": relative(DOWNLOADS / "arxiv_2002_11761" / "source_extract" / "fig5b1.pdf"),
            "acquisition_status": "vector_curve_candidate_extractable_but_review_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1034_3_aps_supplement_attempt",
            "source_url": "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101",
            "source_role": "official supplemental numerical values if accessible",
            "evidence_summary": "Direct access attempt is recorded locally as a Cloudflare/JavaScript challenge, so no official table is acquired in this pass.",
            "machine_readable_curve": "false",
            "local_artifact": relative(DOWNLOADS / "aps_prl_124_101101" / "link_aps_supplemental_attempt.html"),
            "acquisition_status": "blocked_cloudflare_or_js_challenge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1034_4_eotwash_results_page",
            "source_url": "https://www.npl.washington.edu/eotwash/results",
            "source_role": "Eot-Wash public constraint-page provenance",
            "evidence_summary": "Public page describes 95 percent CL Yukawa ISL constraints relative to gravity and range, but does not expose a machine-readable table in this pack.",
            "machine_readable_curve": "false",
            "local_artifact": "MISSING_LOCAL_MACHINE_READABLE_TABLE",
            "acquisition_status": "web_provenance_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def vector_candidate_stats(vector_rows: list[dict[str, str]]) -> dict[str, object]:
    numeric_rows = []
    for row in vector_rows:
        lam = as_float(row.get("lambda_value"))
        alpha = as_float(row.get("alpha_bound"))
        if lam is not None and alpha is not None and lam > 0 and alpha > 0:
            numeric_rows.append((lam, alpha, row))
    if not numeric_rows:
        return {
            "rows": 0,
            "lambda_min": "",
            "lambda_max": "",
            "alpha_min": "",
            "alpha_max": "",
            "tightest_lambda": "",
            "all_nonclaim": "false",
        }
    tightest = min(numeric_rows, key=lambda item: item[1])
    return {
        "rows": len(numeric_rows),
        "lambda_min": min(item[0] for item in numeric_rows),
        "lambda_max": max(item[0] for item in numeric_rows),
        "alpha_min": min(item[1] for item in numeric_rows),
        "alpha_max": max(item[1] for item in numeric_rows),
        "tightest_lambda": tightest[0],
        "all_nonclaim": str(all(not flag(row.get("valid_for_claim")) for row in vector_rows)).lower(),
    }


def write_1034_curve_candidate(vector_rows: list[dict[str, str]]) -> Path:
    candidate_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
    fieldnames = []
    for row in vector_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    for extra in ["pack_id", "promotion_policy", "generated_utc"]:
        if extra not in fieldnames:
            fieldnames.append(extra)
    rows: list[dict[str, object]] = []
    for row in vector_rows:
        copy = dict(row)
        copy["valid_for_claim"] = "false"
        copy["pack_id"] = "P8_Y5_R10_1034"
        copy["promotion_policy"] = "review_candidate_only_requires_official_supplement_or_human_visual_QA_before_live_claim_file_update"
        copy["generated_utc"] = stamp()
        rows.append(copy)
    write_csv(candidate_path, rows, fieldnames)
    return candidate_path


def alpha_bound_rows(stats: dict[str, object], candidate_path: Path) -> list[dict[str, str]]:
    return [
        {
            "bound_id": "R10B1034_0_2020_alpha1_38p6um_anchor",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101",
            "lambda_value": "3.86e-05",
            "lambda_units": "m",
            "alpha_bound": "1.0",
            "alpha_bound_source": "https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
            "extraction_method": "paper_text_gravitational_strength_threshold_anchor",
            "row_type": "anchor_only_non_curve",
            "confidence": "high_for_anchor_not_curve",
            "source_file": relative(DOWNLOADS / "arxiv_2002_11761" / "2002.11761.pdf"),
            "valid_for_claim": "false",
            "notes": "This is the alpha=1 threshold anchor only, not a full alpha_bound(lambda) curve.",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R10B1034_1_2020_scan_range_min",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101",
            "lambda_value": "5e-06",
            "lambda_units": "m",
            "alpha_bound": "MISSING_CURVE_VALUE",
            "alpha_bound_source": "https://arxiv.org/pdf/2002.11761",
            "extraction_method": "paper_text_lambda_scan_range",
            "row_type": "scan_range_anchor_only",
            "confidence": "high_for_lambda_range_not_alpha_bound",
            "source_file": relative(DOWNLOADS / "arxiv_2002_11761" / "2002.11761.pdf"),
            "valid_for_claim": "false",
            "notes": "Paper states 66 lambda values were tested between 5 micrometers and 9 mm, but this row has no alpha bound.",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R10B1034_2_2020_scan_range_max",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101",
            "lambda_value": "9e-03",
            "lambda_units": "m",
            "alpha_bound": "MISSING_CURVE_VALUE",
            "alpha_bound_source": "https://arxiv.org/pdf/2002.11761",
            "extraction_method": "paper_text_lambda_scan_range",
            "row_type": "scan_range_anchor_only",
            "confidence": "high_for_lambda_range_not_alpha_bound",
            "source_file": relative(DOWNLOADS / "arxiv_2002_11761" / "2002.11761.pdf"),
            "valid_for_claim": "false",
            "notes": "Paper states 66 lambda values were tested between 5 micrometers and 9 mm, but this row has no alpha bound.",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R10B1034_3_vector_review_candidate_summary",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101_vector_fig5b",
            "lambda_value": f"{stats['lambda_min']}..{stats['lambda_max']}",
            "lambda_units": "m",
            "alpha_bound": f"{stats['alpha_min']}..{stats['alpha_max']}",
            "alpha_bound_source": "https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
            "extraction_method": "axis_calibrated_vector_path_extraction_from_fig5b1_pdf_review_candidate",
            "row_type": "full_curve_review_candidate_nonclaim",
            "confidence": "medium_internal_QA_not_promotion_ready",
            "source_file": relative(candidate_path),
            "valid_for_claim": "false",
            "notes": f"{stats['rows']} numeric review-candidate rows; tightest candidate alpha at lambda={stats['tightest_lambda']} m; requires official supplement or human QA before use as claim curve.",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "R10B1034_4_official_supplement_table_status",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101_supplement",
            "lambda_value": "MISSING_OFFICIAL_TABLE",
            "lambda_units": "m",
            "alpha_bound": "MISSING_OFFICIAL_TABLE",
            "alpha_bound_source": "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101",
            "extraction_method": "direct_web_access_attempt",
            "row_type": "blocker_status",
            "confidence": "not_acquired",
            "source_file": relative(DOWNLOADS / "aps_prl_124_101101" / "link_aps_supplemental_attempt.html"),
            "valid_for_claim": "false",
            "notes": "Official numerical supplement remains blocked in current local/web pass; do not fabricate curve rows.",
            "generated_utc": stamp(),
        },
    ]


def curve_summary_rows(stats: dict[str, object], candidate_path: Path) -> list[dict[str, str]]:
    return [
        {
            "summary_id": "CS1034_0_candidate_file",
            "metric": "candidate_file",
            "value": relative(candidate_path),
            "units": "path",
            "promotion_status": "review_candidate_nonclaim",
            "valid_for_claim": "false",
            "notes": "Separate 1034 candidate file created; live DIGITIZED claim file left untouched.",
            "generated_utc": stamp(),
        },
        {
            "summary_id": "CS1034_1_rows",
            "metric": "numeric_rows",
            "value": str(stats["rows"]),
            "units": "rows",
            "promotion_status": "review_candidate_nonclaim",
            "valid_for_claim": "false",
            "notes": "Rows copied from the prior vector review candidate with valid_for_claim forced false.",
            "generated_utc": stamp(),
        },
        {
            "summary_id": "CS1034_2_lambda_range",
            "metric": "lambda_min_to_max",
            "value": f"{stats['lambda_min']}..{stats['lambda_max']}",
            "units": "m",
            "promotion_status": "review_candidate_nonclaim",
            "valid_for_claim": "false",
            "notes": "Internal plotting/smoke range only.",
            "generated_utc": stamp(),
        },
        {
            "summary_id": "CS1034_3_alpha_range",
            "metric": "alpha_bound_min_to_max",
            "value": f"{stats['alpha_min']}..{stats['alpha_max']}",
            "units": "dimensionless",
            "promotion_status": "review_candidate_nonclaim",
            "valid_for_claim": "false",
            "notes": "Internal plotting/smoke range only.",
            "generated_utc": stamp(),
        },
        {
            "summary_id": "CS1034_4_tightest_candidate",
            "metric": "min_alpha_lambda",
            "value": str(stats["tightest_lambda"]),
            "units": "m",
            "promotion_status": "review_candidate_nonclaim",
            "valid_for_claim": "false",
            "notes": f"Minimum review-candidate alpha={stats['alpha_min']}; not a public or claim bound.",
            "generated_utc": stamp(),
        },
    ]


def profile_convention_rows() -> list[dict[str, str]]:
    return [
        {
            "convention_id": "R10C1034_0_yukawa_potential",
            "quantity": "observable convention",
            "mathematical_form": "V(r)=V_N(r)[1+alpha exp(-r/lambda)]",
            "source_status": "SOURCE_TEXT_ANCHOR_PRESENT",
            "needed_for_claim": "unit-matched alpha_predicted(lambda) rows",
            "valid_for_claim": "false",
            "notes": "Convention is source-backed; MTS prediction is not.",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "R10C1034_1_lambda_grid",
            "quantity": "external lambda scan",
            "mathematical_form": "66 assumed lambda values from 5 micrometers to 9 mm",
            "source_status": "SOURCE_TEXT_ANCHOR_PRESENT",
            "needed_for_claim": "official numerical grid or QA-approved digitized curve",
            "valid_for_claim": "false",
            "notes": "Scan endpoints are not enough for curve scoring.",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "R10C1034_2_source_profile",
            "quantity": "source-body profile",
            "mathematical_form": "Qbar_XH[source,lambda] = normalized source support integral under the R10 geometry",
            "source_status": "MISSING_MTS_SOURCE_PROFILE",
            "needed_for_claim": "same-worldtube Hilbert/source charge and measured-GM calibration convention",
            "valid_for_claim": "false",
            "notes": "Cannot absorb this into tau_R10 or c_g without losing units.",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "R10C1034_3_test_profile",
            "quantity": "test-leg projection",
            "mathematical_form": "tau_R10[test,lambda] = normalized readout/material projection of the finite X leg",
            "source_status": "MISSING_MTS_TEST_PROFILE",
            "needed_for_claim": "trace/readout convention and finite-size material correction",
            "valid_for_claim": "false",
            "notes": "The unity shortcut remains rejected.",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "R10C1034_4_no_cancellation",
            "quantity": "retained-tail envelope",
            "mathematical_form": "alpha_pred = K_X Qbar_XH [tau_R10 c_g + absolute_tail_envelope]",
            "source_status": "MISSING_ABSOLUTE_ENVELOPE",
            "needed_for_claim": "zero theorem or numeric rows for every retained component",
            "valid_for_claim": "false",
            "notes": "No cancellation can be used to sneak through R10.",
            "generated_utc": stamp(),
        },
    ]


def projection_input_rows(candidate_path: Path) -> list[dict[str, str]]:
    return [
        {
            "input_id": "R10P1034_0_alpha_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "candidate_value": "REVIEW_CANDIDATE_CURVE_PRESENT_NONCLAIM",
            "units": "dimensionless over lambda in m",
            "source_path": relative(candidate_path),
            "source_row_id": "R10_VECTOR_2020_REVIEW_*",
            "status": "BLOCKED_REVIEW_CANDIDATE_NOT_PROMOTED",
            "needed_for_score": "official supplement table or human visual QA plus promotion gate",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_1_KX_lambda",
            "quantity": "K_X(lambda)",
            "candidate_value": "MISSING_KERNEL_NORMALIZATION",
            "units": "model_dependent",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "MISSING_GREEN_FUNCTION_DERIVATION",
            "needed_for_score": "derive static X Green kernel and Newton-normalized alpha conversion",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_2_Qbar_XH",
            "quantity": "Qbar_XH(source,lambda)",
            "candidate_value": "MISSING_SOURCE_CHARGE",
            "units": "dimensionless_or_declared",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "MISSING_SOURCE_NORMALIZATION",
            "needed_for_score": "same-worldtube source charge, support rule, and measured-GM calibration",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_3_tau_R10",
            "quantity": "tau_R10(test,lambda)",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "source_path": "MISSING_PROJECTION_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "MISSING_R10_PROJECTION_DERIVATION",
            "needed_for_score": "test material/readout projection and profile integral",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_4_cg",
            "quantity": "c_g",
            "candidate_value": "MISSING_PARENT_INPUT_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "MISSING_PARENT_CG_OR_SIGNED_ZERO_PROOF",
            "needed_for_score": "parent-signed c_g value or closed zero theorem",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_5_tail_envelope",
            "quantity": "retained tails",
            "candidate_value": "MISSING_ABSOLUTE_NO_CANCELLATION_ENVELOPE",
            "units": "dimensionless alpha-equivalent",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "ABSOLUTE_ENVELOPE_REQUIRED",
            "needed_for_score": "individual bound/zero rows for b_A, b_alpha, b_dis, q_nonH, Delta_W_support, hidden components",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R10P1034_6_alpha_predicted",
            "quantity": "alpha_predicted(lambda)",
            "candidate_value": "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
            "units": "dimensionless over lambda in m",
            "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "source_row_id": "bulk_memory_range_template",
            "status": "MISSING_JOIN_OF_KX_QBAR_TAU_CG_TAILS",
            "needed_for_score": "numeric prediction rows after all companion factors exist",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def placeholder_refusal_rows(projection_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(projection_rows):
        failure_reasons = []
        if "MISSING" in row["candidate_value"]:
            failure_reasons.append("MISSING_VALUE")
        if "MISSING" in row["source_path"]:
            failure_reasons.append("MISSING_SOURCE_PATH")
        if "MISSING" in row["source_row_id"]:
            failure_reasons.append("MISSING_SOURCE_ROW_ID")
        if not flag(row["score_ready"]):
            failure_reasons.append("NOT_READY_FOR_SCORE")
        if not flag(row["valid_for_claim"]):
            failure_reasons.append("CLAIM_POLICY_FALSE")
        if row["status"].startswith("BLOCKED"):
            failure_reasons.append(row["status"])
        rows.append(
            {
                "run_id": f"R10REF1034_{index}_{row['quantity'].replace('(', '').replace(')', '').replace(',', '').replace(' ', '_')}",
                "input_id": row["input_id"],
                "quantity": row["quantity"],
                "candidate_value": row["candidate_value"],
                "refusal_status": "rejected_missing_or_nonclaim_R10_inputs",
                "failure_reasons": ";".join(failure_reasons),
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1034_0_sources",
            "claim": "all 1034 local sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1034_1_external_curve",
            "claim": "R10 external alpha_bound(lambda) is usable for claim scoring",
            "gate_pass": "false",
            "reason": "vector curve is only a review candidate and official supplement table is not acquired",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1034_2_mts_projection",
            "claim": "MTS alpha_predicted(lambda) is source-normalized",
            "gate_pass": "false",
            "reason": "K_X, Qbar_XH, tau_R10, c_g, and tail envelope are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1034_3_no_unity_shortcut",
            "claim": "tau_R10 can be set to one",
            "gate_pass": "false",
            "reason": "1033 rejected the unity shortcut; 1034 preserves this block",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1034_4_no_cancellation",
            "claim": "tail terms can cancel without explicit envelope",
            "gate_pass": "false",
            "reason": "absolute retained-tail envelope remains required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1034_5_R10_score",
            "claim": "R10 finite branch can be scored",
            "gate_pass": "false",
            "reason": "external curve is nonclaim and theory-side projection pack is incomplete",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows(candidate_path: Path) -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1034_0_bound_status",
            "decision": "Use the 2020 vector-extracted curve only as a private review candidate.",
            "because": "it is source-backed by the arXiv vector figure and passes internal axis/anchor checks, but lacks official supplement or human visual QA promotion.",
            "next_action": "keep live DIGITIZED claim file unchanged and use the 1034 candidate only for nonclaim smoke plots/joins",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1034_1_anchor_status",
            "decision": "Keep alpha=1 at lambda=38.6 micrometers as an anchor, not a curve.",
            "because": "a single threshold sentence cannot substitute for alpha_bound(lambda) over the tested range.",
            "next_action": "record anchor provenance but refuse full-curve scoring from anchors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1034_2_projection_status",
            "decision": "R10 projection remains missing on the MTS side.",
            "because": "K_X(lambda), Qbar_XH, tau_R10, c_g, and retained-tail envelope are still unsourced.",
            "next_action": "derive K_X(lambda) as the next lowest-ambiguity parent-normalization target",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1034_3_next_target",
            "decision": "Next target is K_X Green-kernel normalization plus source/test profile convention.",
            "because": f"external bound evidence has a nonclaim review candidate at {relative(candidate_path)}, while the theory-side alpha prediction is still empty.",
            "next_action": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "objective": "derive or source the static X Green-kernel normalization K_X(lambda) and the minimal source/test profile integral needed to turn c_g/tau_R10 into alpha_predicted(lambda)",
            "include": "parent kinetic normalization, range relation lambda_X, Newtonian comparison convention, source support, test readout profile, finite-size integral, retained-tail envelope slot",
            "exclude": "unity tau shortcut, invented K_X values, invented Qbar/tau/c_g rows, R10 pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    external_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    vector_rows: list[dict[str, str]],
    candidate_path: Path,
    projection_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1034_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all cited local source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1034_1_web_sources_recorded",
            all(row["source_url"].startswith("http") for row in external_rows),
            "external source URLs recorded without empty web-source rows",
        )
    )
    checks.append(
        (
            "V1034_2_candidate_file_written",
            candidate_path.exists() and candidate_path.stat().st_size > 0,
            f"candidate file written at {candidate_path}",
        )
    )
    numeric_candidate_ok = True
    for row in vector_rows:
        lam = as_float(row.get("lambda_value"))
        alpha = as_float(row.get("alpha_bound"))
        numeric_candidate_ok = numeric_candidate_ok and lam is not None and alpha is not None and lam > 0 and alpha > 0
    checks.append(
        (
            "V1034_3_vector_candidate_numeric",
            bool(vector_rows) and numeric_candidate_ok,
            "vector review candidate rows have positive numeric lambda and alpha values",
        )
    )
    checks.append(
        (
            "V1034_4_vector_candidate_nonclaim",
            bool(vector_rows) and all(not flag(row.get("valid_for_claim")) for row in vector_rows),
            "all vector review candidate rows remain valid_for_claim=false",
        )
    )
    anchor = next((row for row in alpha_rows if row["bound_id"] == "R10B1034_0_2020_alpha1_38p6um_anchor"), None)
    checks.append(
        (
            "V1034_5_anchor_positive_nonclaim",
            bool(anchor)
            and as_float(anchor["lambda_value"]) is not None
            and as_float(anchor["lambda_value"]) > 0
            and as_float(anchor["alpha_bound"]) == 1.0
            and not flag(anchor["valid_for_claim"]),
            "alpha=1 at 38.6 micrometers anchor is positive numeric and nonclaim",
        )
    )
    checks.append(
        (
            "V1034_6_no_anchor_promoted",
            all(not flag(row["valid_for_claim"]) for row in alpha_rows if "anchor" in row["row_type"]),
            "anchor-only rows are not promoted to claim rows",
        )
    )
    checks.append(
        (
            "V1034_7_projection_blocked",
            all(not flag(row["score_ready"]) and not flag(row["valid_for_claim"]) for row in projection_rows),
            "all projection input rows refuse scoring",
        )
    )
    checks.append(
        (
            "V1034_8_mts_side_missing_explicit",
            any("MISSING_KERNEL_NORMALIZATION" in row["candidate_value"] for row in projection_rows)
            and any("MISSING_SOURCE_CHARGE" in row["candidate_value"] for row in projection_rows)
            and any("MISSING_ARENA_PROJECTION" in row["candidate_value"] for row in projection_rows),
            "K_X, Qbar_XH, and tau_R10 missing statuses are explicit",
        )
    )
    checks.append(
        (
            "V1034_9_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claim_rows),
            "claim gates refuse R10 scoring and promotion",
        )
    )
    checks.append(
        (
            "V1034_10_decision_next",
            any("1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md" in row["next_action"] for row in decision),
            "decision ledger selects 1035 K_X/profile target",
        )
    )
    checks.append(
        (
            "V1034_11_next_target_written",
            bool(next_target)
            and next_target[0]["next_target"] == "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1034_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1034_EXTERNAL_SOURCE_ACQUISITION_LEDGER.csv",
        OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv",
        OUT / "P8_Y5_R10_1034_CURVE_CANDIDATE_SUMMARY.csv",
        OUT / "P8_Y5_R10_1034_SOURCE_TEST_PROFILE_CONVENTION.csv",
        OUT / "P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv",
        OUT / "P8_Y5_R10_1034_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1034_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1034_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1034_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1034_VALIDATION.csv",
        candidate_path,
    ]
    checks.append(
        (
            "V1034_12_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1034_13_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1034_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1034 R10 alpha-bound curve and projection-pack validation summary",
            "generated_utc": stamp(),
        }
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    return rows


def write_doc(
    source_rows: list[dict[str, str]],
    external_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    curve_summary: list[dict[str, str]],
    convention_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    sections = [
        "# 1034 Y5 R10 alpha-bound curve digitization and projection input pack",
        "",
        "**Status:** The R10 external side now has a source-backed, axis-calibrated **review candidate** curve from the 2020 Eot-Wash arXiv vector figure plus a paper-text `alpha=1`, `lambda=38.6 micrometers` anchor. It is deliberately **not** promoted to the live claim curve because the official supplemental numerical table is still not acquired and human visual QA/promotion has not signed it.",
        "",
        "**Claim ceiling:** no R10 pass, no local-GR pass, no finite-`c_g` score, no `tau_R10=1` shortcut, no invented `K_X/Qbar/tau/c_g` row, and no live bound-curve promotion is allowed from 1034.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## External source acquisition ledger",
        md_table(external_rows, ["external_id", "source_url", "source_role", "machine_readable_curve", "acquisition_status", "local_artifact"]),
        "## Alpha-bound candidate rows",
        md_table(alpha_rows, ["bound_id", "lambda_value", "lambda_units", "alpha_bound", "row_type", "confidence", "valid_for_claim", "notes"]),
        "## Curve candidate summary",
        md_table(curve_summary, ["summary_id", "metric", "value", "units", "promotion_status", "valid_for_claim", "notes"]),
        "## Source/test profile convention",
        md_table(convention_rows, ["convention_id", "quantity", "mathematical_form", "source_status", "needed_for_claim", "valid_for_claim"]),
        "## Projection input pack",
        md_table(projection_rows, ["input_id", "quantity", "candidate_value", "units", "source_path", "status", "needed_for_score", "score_ready", "valid_for_claim"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["run_id", "input_id", "quantity", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "## Next target",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    vector_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
    vector_rows = read_csv(vector_path)
    candidate_path = write_1034_curve_candidate(vector_rows)
    copied_rows = read_csv(candidate_path)
    stats = vector_candidate_stats(copied_rows)

    external_rows = external_source_rows()
    alpha_rows = alpha_bound_rows(stats, candidate_path)
    curve_summary = curve_summary_rows(stats, candidate_path)
    convention_rows = profile_convention_rows()
    projection_rows = projection_input_rows(candidate_path)
    refusal_rows = placeholder_refusal_rows(projection_rows)
    claim_rows = claim_gate_rows()
    decision = decision_rows(candidate_path)
    next_target = next_target_rows()
    validation = validation_rows(
        source_rows,
        external_rows,
        alpha_rows,
        copied_rows,
        candidate_path,
        projection_rows,
        claim_rows,
        decision,
        next_target,
    )

    write_csv(OUT / "P8_Y5_R10_1034_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1034_EXTERNAL_SOURCE_ACQUISITION_LEDGER.csv", external_rows)
    write_csv(OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv", alpha_rows)
    write_csv(OUT / "P8_Y5_R10_1034_CURVE_CANDIDATE_SUMMARY.csv", curve_summary)
    write_csv(OUT / "P8_Y5_R10_1034_SOURCE_TEST_PROFILE_CONVENTION.csv", convention_rows)
    write_csv(OUT / "P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_1034_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1034_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1034_DECISION_LEDGER.csv", decision)
    write_csv(OUT / "P8_Y5_R10_1034_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1034_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        external_rows,
        alpha_rows,
        curve_summary,
        convention_rows,
        projection_rows,
        refusal_rows,
        claim_rows,
        decision,
        validation,
        next_target,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1034 validation failed: {failed}")


if __name__ == "__main__":
    main()
