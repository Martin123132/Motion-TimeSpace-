from __future__ import annotations

import csv
import hashlib
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_INTAKE = ROOT / "source-intake"
EOTWASH = SOURCE_INTAKE / "eotwash"
R10 = SOURCE_INTAKE / "r10"
MICROSCOPE = SOURCE_INTAKE / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1494-Y5-R10-RAB-PDF-table-text-extraction-for-EotWash-and-R10-curve-digitization.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1493_downloads": OUT / "P8_Y5_R10_1493_DOWNLOAD_ATTEMPT_LEDGER.csv",
    "1493_hashes": OUT / "P8_Y5_R10_1493_FILE_PROVENANCE_HASHES.csv",
    "1493_r10": OUT / "P8_Y5_R10_1493_R10_CURVE_DIGITIZATION_SKELETON.csv",
    "1493_eotwash": OUT / "P8_Y5_R10_1493_EOTWASH_TABLE_EXTRACTION_SKELETON.csv",
    "1493_microscope": OUT / "P8_Y5_R10_1493_MICROSCOPE_PORTAL_PARSE_STATUS.csv",
    "1493_readiness": OUT / "P8_Y5_R10_1493_DELTA_W_SCORE_READINESS.csv",
    "1493_validation": OUT / "P8_Y5_BRR545_1493_VALIDATION.csv",
    "1493_next": OUT / "P8_Y5_R10_1493_NEXT_TARGET.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

PDF_EXTRACTION_LEDGER = OUT / "P8_Y5_R10_1494_PDF_TEXT_EXTRACTION_LEDGER.csv"
TEXT_ANCHORS = OUT / "P8_Y5_R10_1494_TEXT_ANCHOR_CANDIDATES.csv"
R10_DIGITIZATION_QUEUE = OUT / "P8_Y5_R10_1494_R10_MANUAL_DIGITIZATION_QUEUE.csv"
EOTWASH_PROMOTION_QUEUE = OUT / "P8_Y5_R10_1494_EOTWASH_PROMOTION_QUEUE.csv"
MICROSCOPE_PROMOTION_QUEUE = OUT / "P8_Y5_R10_1494_MICROSCOPE_PROMOTION_QUEUE.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1494_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1494_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1494_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1494_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1494_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1494_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1494_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1494_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1494"
QUAR_EXTRACTION = QUARANTINE / "PDF_TEXT_EXTRACTION_LEDGER_NONCLAIM.csv"
QUAR_ANCHORS = QUARANTINE / "TEXT_ANCHOR_CANDIDATES_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "TARGET_PROMOTION_BLOCKERS_NONCLAIM.csv"
QUAR_READINESS = QUARANTINE / "DELTA_W_SCORE_READINESS_NONCLAIM.csv"
BRANCH_EXTRACTION = BRANCH_RESIDUALS / "pdf_text_extraction_ledger_nonclaim_1494.csv"
BRANCH_ANCHORS = BRANCH_RESIDUALS / "text_anchor_candidates_nonclaim_1494.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "target_promotion_blockers_nonclaim_1494.csv"
BRANCH_READINESS = BRANCH_RESIDUALS / "delta_w_score_readiness_nonclaim_1494.csv"


PDF_OUTPUT_DIRS = {
    "WEP_EotWash_material_pairs": EOTWASH / "extracted_text",
    "R10_short_range_inverse_square": R10 / "extracted_text",
    "WEP_MICROSCOPE_TiPt": MICROSCOPE / "extracted_text",
}

LIVE_TARGETS = {
    "EOTWASH_bounds": EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv",
    "EOTWASH_vectors": EOTWASH / "derived" / "P_WEP_EotWash_material_response_vectors.csv",
    "R10_curve": R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "R10_kernel": R10 / "derived" / "R10_delta_w_kernel_lambda.csv",
    "MICROSCOPE_readout": MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv",
    "MICROSCOPE_source": MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv",
    "MICROSCOPE_product": MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv",
    "MICROSCOPE_tensor": MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def sha256_text(text: str) -> str:
    digest = hashlib.sha256()
    digest.update(text.encode("utf-8"))
    return digest.hexdigest()


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    replacements = {
        "\u2212": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u00d7": "x",
        "\u03bc": "um",
        "\u00b5": "um",
        "\ufb00": "ff",
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\u0308": "",
    }
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def load_pdf_reader() -> tuple[str, Any | None]:
    try:
        from pypdf import PdfReader

        return "pypdf", PdfReader
    except Exception:
        return "missing_pdf_extractor", None


def local_path(row: dict[str, str]) -> Path:
    return ROOT / row["local_path"]


def downloaded_pdf_rows() -> list[dict[str, str]]:
    rows = read_csv(SOURCE_FILES["1493_downloads"])
    return [row for row in rows if row["download_status"] == "DOWNLOADED_PDF_PROVENANCE_ONLY"]


def extract_pdf_text() -> tuple[list[dict[str, Any]], dict[str, str]]:
    extractor_name, reader_cls = load_pdf_reader()
    ledger: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    for row in downloaded_pdf_rows():
        pdf_path = local_path(row)
        output_dir = PDF_OUTPUT_DIRS.get(row["arena"], SOURCE_INTAKE / "extracted_text")
        output_dir.mkdir(parents=True, exist_ok=True)
        text_path = output_dir / f"{pdf_path.stem}.txt"
        status = "PDF_EXTRACTOR_MISSING_BLOCKED"
        page_count = 0
        text_char_count = 0
        normalized_char_count = 0
        text_hash = ""
        error = ""
        extracted = ""

        if reader_cls is not None and pdf_path.exists():
            try:
                reader = reader_cls(str(pdf_path))
                page_count = len(reader.pages)
                page_texts = []
                for page in reader.pages:
                    page_texts.append(page.extract_text() or "")
                extracted = "\n\n".join(page_texts)
                normalized = normalize_text(extracted)
                text_path.write_text(extracted, encoding="utf-8")
                text_char_count = len(extracted)
                normalized_char_count = len(normalized)
                text_hash = sha256_text(extracted)
                status = "TEXT_EXTRACTED_NONCLAIM" if normalized_char_count > 1000 else "TEXT_TOO_SHORT_BLOCKED"
                texts[row["external_id"]] = normalized
            except Exception as exc:
                error = repr(exc)
                status = "TEXT_EXTRACTION_FAILED_BLOCKED"
        elif not pdf_path.exists():
            status = "PDF_SOURCE_MISSING_BLOCKED"

        ledger.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "extract_id": f"TXT1494_{row['external_id']}",
                "external_id": row["external_id"],
                "arena": row["arena"],
                "pdf_path": rel(pdf_path),
                "text_path": rel(text_path),
                "extractor": extractor_name,
                "extraction_status": status,
                "page_count": page_count,
                "text_char_count": text_char_count,
                "normalized_char_count": normalized_char_count,
                "text_sha256": text_hash,
                "error": error,
                "timestamp_utc": utc_now(),
                **flags(),
            }
        )
    return ledger, texts


ANCHOR_PATTERNS: dict[str, list[tuple[str, str]]] = {
    "EXT1492_0_EOTWASH_PRL_2008": [
        ("Be_Ti_eta_Earth", r"eta\s*Earth[^=]{0,40}=\s*\(?\s*[+-]?\d+(?:\.\d+)?\s*[+-]?\s*\d*(?:\.\d+)?\)?\s*x?\s*10\s*-\s*13"),
        ("Be_Ti_delta_a", r"aN[^=]{0,50}=\s*\(?\s*[+-]?\d+(?:\.\d+)?\s*[+-]?\s*\d*(?:\.\d+)?\)?\s*x?\s*10\s*-\s*15"),
        ("Milky_Way_DM_eta", r"eta\s*DM[^=]{0,50}=\s*\(?\s*[+-]?\d+(?:\.\d+)?\s*[+-]?\s*\d+(?:\.\d+)?\)?\s*x?\s*10\s*-\s*5"),
        ("Yukawa_charge_formula", r"Yukawa potential[^.]{0,220}"),
    ],
    "EXT1492_1_EOTWASH_CQG_2012": [
        ("Be_Al_or_Be_Ti_context", r"Be[- ]?(?:Al|Ti)[^.]{0,220}"),
        ("torsion_balance_context", r"torsion[- ]balance[^.]{0,220}"),
        ("WEP_precision_context", r"10\s*-\s*13[^.]{0,160}"),
    ],
    "EXT1492_2_R10_ARXIV_2020": [
        ("R10_separation_range", r"separations? between 52 um and 3\.0 mm"),
        ("R10_gravity_strength_threshold", r"gravitational-strength Yukawa interactions? to ranges < 38\.6 um"),
        ("R10_Yukawa_potential", r"V\s*\(r\)\s*=\s*VN\s*\(r\)\s*\[\s*1\s*\+\s*alpha[^]]{0,120}\]"),
        ("R10_curve_language", r"95% confidence[^.]{0,220}"),
    ],
    "EXT1492_5_MICROSCOPE_PRL_FINAL": [
        ("SUEP_materials", r"SUEP[^.]{0,220}(?:Pt/Rh|PtRh|Ti/Al/V|TiAlV)[^.]{0,220}"),
        ("EP_plot_units", r"EP\s*\[\s*x\s*10\s*15\s*\][^.]{0,220}"),
        ("Eotvos_parameter_definition", r"2aA-aB[^.]{0,220}"),
        ("MICROSCOPE_final_bound_context", r"(?:10\s*15|10-15|10\^15)[^.]{0,220}"),
    ],
    "EXT1492_6_MICROSCOPE_CQG_READOUT": [
        ("SUEP_SUREF_materials", r"(?:SUREF|SUEP)[^.]{0,220}(?:PtRh10|Ti alloy)[^.]{0,220}"),
        ("PtRh10_composition", r"PtRh10[^.]{0,220}"),
        ("session_table_context", r"Spin Beginning Beginning End Duration[^.]{0,220}"),
        ("EP_units_context", r"EP\s*\[\s*x\s*10\s*15\s*\][^.]{0,220}"),
    ],
}


def concise_excerpt(text: str, start: int, end: int, max_words: int = 24) -> str:
    window = text[max(0, start - 90) : min(len(text), end + 90)]
    words = window.split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words])


def anchor_rows(texts: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for external_id, patterns in ANCHOR_PATTERNS.items():
        text = texts.get(external_id, "")
        for index, (anchor_name, pattern) in enumerate(patterns):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                status = "CANDIDATE_ANCHOR_FOUND_NONCLAIM"
                excerpt = concise_excerpt(text, match.start(), match.end())
                char_start = match.start()
            else:
                status = "ANCHOR_NOT_FOUND_OR_NEEDS_MANUAL_REVIEW"
                excerpt = ""
                char_start = ""
            rows.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "anchor_id": f"ANC1494_{external_id}_{index}",
                    "external_id": external_id,
                    "anchor_name": anchor_name,
                    "pattern": pattern,
                    "anchor_status": status,
                    "char_start": char_start,
                    "short_excerpt_for_manual_review": excerpt,
                    "promotion_rule": "manual verify against PDF page/figure/table before any live target row",
                    **flags(),
                }
            )
    return rows


def r10_queue_rows(anchor_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    threshold_found = any(row["anchor_name"] == "R10_gravity_strength_threshold" and row["anchor_status"] == "CANDIDATE_ANCHOR_FOUND_NONCLAIM" for row in anchor_candidates)
    curve_target = LIVE_TARGETS["R10_curve"]
    kernel_target = LIVE_TARGETS["R10_kernel"]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "R10Q1494_0_pdf_text",
            "object": "R10 PDF text",
            "current_status": "TEXT_ANCHOR_FOUND_NONCLAIM" if threshold_found else "TEXT_ANCHOR_NEEDS_MANUAL_REVIEW",
            "required_output": rel(curve_target),
            "work_instruction": "use PDF figure/table, not abstract threshold, to digitize alpha(lambda) bound curve",
            "promotion_blocker": "FULL_CURVE_NOT_DIGITIZED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "R10Q1494_1_curve_digitization",
            "object": "alpha(lambda) curve",
            "current_status": "NOT_DIGITIZED",
            "required_output": rel(curve_target),
            "work_instruction": "extract ordered positive lambda_value/lambda_units/alpha_bound/confidence rows with method/provenance",
            "promotion_blocker": "DIGITIZED_CURVE_REQUIRED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "R10Q1494_2_delta_w_kernel",
            "object": "delta_w to alpha(lambda) projection kernel",
            "current_status": "MISSING",
            "required_output": rel(kernel_target),
            "work_instruction": "derive/source same-branch kernel mapping delta_w components into Yukawa alpha prediction",
            "promotion_blocker": "PARENT_PROJECTION_KERNEL_REQUIRED",
            **flags(),
        },
    ]


def eotwash_queue_rows(anchor_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eta_found = any(row["anchor_name"] == "Be_Ti_eta_Earth" and row["anchor_status"] == "CANDIDATE_ANCHOR_FOUND_NONCLAIM" for row in anchor_candidates)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "EOTQ1494_0_eta_bound",
            "object": "EotWash Be-Ti eta bound",
            "current_status": "TEXT_ANCHOR_FOUND_NONCLAIM" if eta_found else "TEXT_ANCHOR_NEEDS_MANUAL_REVIEW",
            "required_output": rel(LIVE_TARGETS["EOTWASH_bounds"]),
            "work_instruction": "extract eta, sigma/confidence, source-attractor direction, material pair, and page/source path",
            "promotion_blocker": "ETA_TABLE_ROW_NOT_PROMOTED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "EOTQ1494_1_material_vectors",
            "object": "EotWash material response vectors",
            "current_status": "MISSING",
            "required_output": rel(LIVE_TARGETS["EOTWASH_vectors"]),
            "work_instruction": "construct material response vectors in same component basis as delta_w; record composition and double-count rule",
            "promotion_blocker": "MATERIAL_RESPONSE_BASIS_MISSING",
            **flags(),
        },
    ]


def microscope_queue_rows(anchor_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    material_found = any("material" in row["anchor_name"].lower() and row["anchor_status"] == "CANDIDATE_ANCHOR_FOUND_NONCLAIM" for row in anchor_candidates)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "MICQ1494_0_material_convention",
            "object": "MICROSCOPE material convention",
            "current_status": "TEXT_ANCHOR_FOUND_NONCLAIM" if material_found else "TEXT_ANCHOR_NEEDS_MANUAL_REVIEW",
            "required_output": rel(LIVE_TARGETS["MICROSCOPE_tensor"]),
            "work_instruction": "confirm PtRh10/Ti alloy convention and build sourced material tensor only if same-basis mapping exists",
            "promotion_blocker": "MATERIAL_TENSOR_NOT_PROMOTED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "MICQ1494_1_official_readout",
            "object": "CMSM official readout/design matrix",
            "current_status": "MISSING_PORTAL_FETCH_BLOCKED",
            "required_output": rel(LIVE_TARGETS["MICROSCOPE_readout"]),
            "work_instruction": "obtain CMSM export/package or manually document access route; papers alone do not replace arrays",
            "promotion_blocker": "OFFICIAL_ARRAYS_MISSING",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "queue_id": "MICQ1494_2_source_worldtube",
            "object": "Earth/source worldtube",
            "current_status": "MISSING",
            "required_output": rel(LIVE_TARGETS["MICROSCOPE_source"]),
            "work_instruction": "build/source Earth/source profile and orbit projection in the same readout convention",
            "promotion_blocker": "SOURCE_WORLDTUBE_MISSING",
            **flags(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (name, path) in enumerate(LIVE_TARGETS.items()):
        exists = path.exists()
        if name == "MICROSCOPE_product" and exists:
            status = "EXISTS_REQUIRES_CONTENT_VALIDATION"
            blocker = "PRODUCT_CONVENTION_CONTENT_NOT_VALIDATED"
        elif exists:
            status = "EXISTS_BUT_NOT_VALIDATED_FOR_CLAIM"
            blocker = "TARGET_CONTENT_NOT_VALIDATED"
        else:
            status = "MISSING_OR_UNPROMOTED"
            blocker = "TARGET_FILE_MISSING"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "blocker_id": f"TBLK1494_{index}_{name}",
                "target_name": name,
                "target_path": rel(path),
                "target_exists": exists,
                "target_status": status,
                "blocking_marker": blocker,
                "reason": "1494 extracts text only; live target promotion requires numeric rows, units, provenance, and same-branch projection",
                **flags(),
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "TBLK1494_overall",
            "target_name": "delta_w_cross_arena_score",
            "target_path": "not_applicable",
            "target_exists": False,
            "target_status": "NOT_SCORE_READY",
            "blocking_marker": "EXTRACTED_TEXT_IS_NOT_A_SCORE",
            "reason": "text anchors reduce manual search debt but do not supply C_parent, tau maps, kernels, or validated bound tables",
            **flags(),
        }
    )
    return rows


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(blockers):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "readiness_id": f"READY1494_{index}_{row['target_name']}",
                "object": row["target_name"],
                "path": row["target_path"],
                "content_status": row["target_status"],
                "score_effect": "BLOCKS_SCORE_OR_CLAIM",
                "required_before_claim": True,
                **flags(),
            }
        )
    return rows


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1494_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "PDF text extraction cannot derive or import parent coupling coefficients",
            "claim_effect": "universal coupling and local-GR/Newton claims remain blocked",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1494_0_text",
            "target": "PDF text extraction",
            "current_status": "TEXT_EXTRACTED_WHERE_AVAILABLE_NONCLAIM",
            "claim_effect": "evidence search improved; no physics claim changes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1494_1_delta_w",
            "target": "delta_w empirical score",
            "current_status": "TEXT_ANCHORS_ONLY_TARGETS_AND_KERNELS_MISSING",
            "claim_effect": "WEP/R10 score blocked",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1494_2_local_GR",
            "target": "local GR/Newton reduction",
            "current_status": "NOT_CLOSED",
            "claim_effect": "no local-GR/Newton claim from text extraction",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1494_3_next",
            "target": "next work",
            "current_status": "R10_CURVE_DIGITIZATION_OR_SOURCE_TABLE_HUNT",
            "claim_effect": "best leverage is a real alpha(lambda) curve plus projection kernel",
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    reasons = [
        ("REJ1494_0_text", "TEXT_ANCHORS_NOT_TARGET_DATA", "extracted text is search evidence, not a promoted numeric bound file"),
        ("REJ1494_1_R10", "R10_FULL_CURVE_MISSING", "R10 abstract threshold is anchor-only; full alpha(lambda) curve still missing"),
        ("REJ1494_2_kernel", "DELTA_W_TO_ALPHA_KERNEL_MISSING", "the short-range score still needs a same-branch projection kernel"),
        ("REJ1494_3_EotWash", "EOTWASH_MATERIAL_VECTOR_MISSING", "EotWash eta anchor lacks response-vector basis"),
        ("REJ1494_4_MICROSCOPE", "MICROSCOPE_OFFICIAL_ARRAYS_MISSING", "MICROSCOPE papers do not replace CMSM readout arrays"),
        ("REJ1494_5_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "no parent coupling coefficient imported or inferred from PDFs"),
        ("REJ1494_6_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/R10/local-GR/Newton pass may be claimed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            **flags(),
        }
        for rejection_id, marker, reason in reasons
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1494_0_extraction_not_claim",
            "decision": "use extracted PDF text only as manual-review evidence",
            "rationale": "text anchors are lossy and can misread tables/figures",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1494_1_R10_priority",
            "decision": "prioritize R10 alpha(lambda) curve digitization or machine-readable source hunt",
            "rationale": "R10 is the shortest route to a concrete local residual bound if the kernel can be derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1494_2_MICROSCOPE",
            "decision": "keep MICROSCOPE blocked until official arrays or a reproducible CMSM export exists",
            "rationale": "paper-level anchors are not enough for same-branch WEP projection",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1494_0_1495",
            "next_target": "1495-Y5-R10-RAB-R10-alpha-lambda-curve-digitization-or-machine-readable-table-hunt.md",
            "script": "scripts/Y5_R10_RAB_R10_alpha_lambda_curve_digitization_or_machine_readable_table_hunt.py",
            "objective": (
                "extract or source a real R10 alpha(lambda) bound curve, keep anchor-only rows invalid for claim, "
                "and specify the delta_w-to-alpha kernel inputs still needed"
            ),
            **flags(),
        }
    ]


def csvs_parse(paths: list[Path]) -> bool:
    return all(parse_csv(path) for path in paths)


def generated_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for column in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
                value = row.get(column)
                if value not in (None, "", "False", "false", False):
                    return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (PDF_EXTRACTION_LEDGER, QUAR_EXTRACTION),
        (TEXT_ANCHORS, QUAR_ANCHORS),
        (TARGET_BLOCKERS, QUAR_BLOCKERS),
        (SCORE_READINESS, QUAR_READINESS),
        (PDF_EXTRACTION_LEDGER, BRANCH_EXTRACTION),
        (TEXT_ANCHORS, BRANCH_ANCHORS),
        (TARGET_BLOCKERS, BRANCH_BLOCKERS),
        (SCORE_READINESS, BRANCH_READINESS),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], extraction_rows: list[dict[str, Any]], anchor_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    extractor_name, reader_cls = load_pdf_reader()
    extractor_available = reader_cls is not None
    all_pdf_text_extracted = all(row["extraction_status"] == "TEXT_EXTRACTED_NONCLAIM" and Path(ROOT / str(row["text_path"])).exists() for row in extraction_rows)
    minimum_text = all(int(row["normalized_char_count"]) > 1000 for row in extraction_rows if row["extraction_status"] == "TEXT_EXTRACTED_NONCLAIM")
    anchor_count = sum(1 for row in anchor_candidates if row["anchor_status"] == "CANDIDATE_ANCHOR_FOUND_NONCLAIM")
    r10_curve_still_blocked = not LIVE_TARGETS["R10_curve"].exists() and not LIVE_TARGETS["R10_kernel"].exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_EXTRACTION, QUAR_ANCHORS, QUAR_BLOCKERS, QUAR_READINESS, BRANCH_EXTRACTION, BRANCH_ANCHORS, BRANCH_BLOCKERS, BRANCH_READINESS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    readiness_nonclaim = all(row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in read_csv(SCORE_READINESS))

    checks = [
        ("VAL1494_0_local_sources", source_paths_exist, "all cited 1493 local source paths exist"),
        ("VAL1494_1_pdf_extractor", extractor_available, f"PDF extractor available={extractor_name}"),
        ("VAL1494_2_text_extracted", all_pdf_text_extracted, "all downloaded PDFs produced text files"),
        ("VAL1494_3_text_minimum", minimum_text, "all extracted text rows exceed minimum normalized character threshold"),
        ("VAL1494_4_anchor_candidates", anchor_count >= 5, f"candidate anchors found={anchor_count}"),
        ("VAL1494_5_R10_curve_blocked", r10_curve_still_blocked, "R10 curve/kernel remain unpromoted"),
        ("VAL1494_6_readiness_blocked", readiness_nonclaim, "delta_w score readiness remains false"),
        ("VAL1494_7_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1494_8_csv_parse", csv_parse_ok, "all generated 1494 CSVs parse cleanly"),
        ("VAL1494_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1494_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1494_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1494_12_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1494_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1494 extracted PDF text/anchors and kept all delta_w/local claims blocked"
            if overall
            else "1494 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    extraction_rows: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    r10_rows: list[dict[str, Any]],
    eot_rows: list[dict[str, Any]],
    mic_rows: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    anchor_summary = [
        {
            "anchor_name": row["anchor_name"],
            "external_id": row["external_id"],
            "anchor_status": row["anchor_status"],
            "char_start": row["char_start"],
        }
        for row in anchors
    ]
    DOC.write_text(
        "\n".join(
            [
                "# 1494 - PDF Text/Table Extraction for EotWash and R10 Curve Digitization",
                "",
                "## Verdict",
                "- PDF text extraction succeeded where source PDFs were available, and candidate anchors were staged for manual review.",
                "- No extracted text anchor is promoted into a live bound curve, WEP table, MICROSCOPE array, or parent coupling coefficient.",
                "- The highest-leverage next step is the real R10 `alpha(lambda)` curve: digitize/source it, then derive the `delta_w -> alpha(lambda)` kernel.",
                "",
                "## PDF Text Extraction Ledger",
                md_table(extraction_rows, ["external_id", "arena", "extraction_status", "page_count", "normalized_char_count", "text_path"]),
                "",
                "## Anchor Candidate Summary",
                md_table(anchor_summary, ["external_id", "anchor_name", "anchor_status", "char_start"]),
                "",
                "## R10 Digitization Queue",
                md_table(r10_rows, ["queue_id", "object", "current_status", "required_output", "promotion_blocker"]),
                "",
                "## EotWash Promotion Queue",
                md_table(eot_rows, ["queue_id", "object", "current_status", "required_output", "promotion_blocker"]),
                "",
                "## MICROSCOPE Promotion Queue",
                md_table(mic_rows, ["queue_id", "object", "current_status", "required_output", "promotion_blocker"]),
                "",
                "## Target Promotion Blockers",
                md_table(blockers, ["blocker_id", "target_name", "target_status", "blocking_marker"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for directory in PDF_OUTPUT_DIRS.values():
        directory.mkdir(parents=True, exist_ok=True)

    extraction_rows, texts = extract_pdf_text()
    anchors = anchor_rows(texts)
    r10_rows = r10_queue_rows(anchors)
    eot_rows = eotwash_queue_rows(anchors)
    mic_rows = microscope_queue_rows(anchors)
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    c_parent_rows = c_parent_refusal_rows()
    local_rows = local_status_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(PDF_EXTRACTION_LEDGER, extraction_rows)
    write_csv(TEXT_ANCHORS, anchors)
    write_csv(R10_DIGITIZATION_QUEUE, r10_rows)
    write_csv(EOTWASH_PROMOTION_QUEUE, eot_rows)
    write_csv(MICROSCOPE_PROMOTION_QUEUE, mic_rows)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        PDF_EXTRACTION_LEDGER,
        TEXT_ANCHORS,
        R10_DIGITIZATION_QUEUE,
        EOTWASH_PROMOTION_QUEUE,
        MICROSCOPE_PROMOTION_QUEUE,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, extraction_rows, anchors)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(extraction_rows, anchors, r10_rows, eot_rows, mic_rows, blockers, validation, next_rows)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
