from __future__ import annotations

import csv
import hashlib
import shutil
import urllib.error
import urllib.request
from dataclasses import dataclass
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
DOC = ROOT / "1493-Y5-R10-RAB-download-or-extract-delta-w-source-files-R10-EotWash-MICROSCOPE.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1492_external": OUT / "P8_Y5_R10_1492_EXTERNAL_SOURCE_LEDGER.csv",
    "1492_targets": OUT / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv",
    "1492_status": OUT / "P8_Y5_R10_1492_ACQUISITION_STATUS.csv",
    "1492_requirements": OUT / "P8_Y5_R10_1492_EXTRACTION_REQUIREMENTS.csv",
    "1492_validation": OUT / "P8_Y5_BRR545_1492_VALIDATION.csv",
    "1492_next": OUT / "P8_Y5_R10_1492_NEXT_TARGET.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

DOWNLOAD_ATTEMPTS = OUT / "P8_Y5_R10_1493_DOWNLOAD_ATTEMPT_LEDGER.csv"
FILE_PROVENANCE = OUT / "P8_Y5_R10_1493_FILE_PROVENANCE_HASHES.csv"
EXTRACTION_BLOCKERS = OUT / "P8_Y5_R10_1493_EXTRACTION_BLOCKERS.csv"
R10_DIGITIZATION = OUT / "P8_Y5_R10_1493_R10_CURVE_DIGITIZATION_SKELETON.csv"
EOTWASH_SKELETON = OUT / "P8_Y5_R10_1493_EOTWASH_TABLE_EXTRACTION_SKELETON.csv"
MICROSCOPE_STATUS = OUT / "P8_Y5_R10_1493_MICROSCOPE_PORTAL_PARSE_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1493_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1493_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1493_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1493_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1493_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1493_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1493_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1493"
QUAR_DOWNLOADS = QUARANTINE / "DOWNLOAD_ATTEMPT_LEDGER_NONCLAIM.csv"
QUAR_HASHES = QUARANTINE / "FILE_PROVENANCE_HASHES_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "EXTRACTION_BLOCKERS_NONCLAIM.csv"
QUAR_READINESS = QUARANTINE / "DELTA_W_SCORE_READINESS_NONCLAIM.csv"
BRANCH_DOWNLOADS = BRANCH_RESIDUALS / "download_attempt_ledger_nonclaim_1493.csv"
BRANCH_HASHES = BRANCH_RESIDUALS / "file_provenance_hashes_nonclaim_1493.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "extraction_blockers_nonclaim_1493.csv"
BRANCH_READINESS = BRANCH_RESIDUALS / "delta_w_score_readiness_nonclaim_1493.csv"


@dataclass(frozen=True)
class DownloadSpec:
    external_id: str
    arena: str
    title: str
    source_url: str
    download_url: str
    local_path: Path
    expected_kind: str
    minimum_bytes: int
    acquisition_role: str


DOWNLOAD_SPECS = [
    DownloadSpec(
        external_id="EXT1492_0_EOTWASH_PRL_2008",
        arena="WEP_EotWash_material_pairs",
        title="Test of the Equivalence Principle Using a Rotating Torsion Balance",
        source_url="https://arxiv.org/abs/0712.0607",
        download_url="https://arxiv.org/pdf/0712.0607",
        local_path=EOTWASH / "raw" / "Schlamminger_2008_PRL_0712.0607.pdf",
        expected_kind="pdf",
        minimum_bytes=1000,
        acquisition_role="provenance PDF for EotWash WEP eta/material extraction",
    ),
    DownloadSpec(
        external_id="EXT1492_1_EOTWASH_CQG_2012",
        arena="WEP_EotWash_material_pairs",
        title="Torsion-balance tests of the weak equivalence principle",
        source_url="https://arxiv.org/abs/1207.2442",
        download_url="https://arxiv.org/pdf/1207.2442",
        local_path=EOTWASH / "docs" / "Wagner_2012_CQG_1207.2442.pdf",
        expected_kind="pdf",
        minimum_bytes=1000,
        acquisition_role="provenance PDF for EotWash material-pair review extraction",
    ),
    DownloadSpec(
        external_id="EXT1492_2_R10_ARXIV_2020",
        arena="R10_short_range_inverse_square",
        title="New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
        source_url="https://arxiv.org/abs/2002.11761",
        download_url="https://arxiv.org/pdf/2002.11761",
        local_path=R10 / "raw" / "Lee_2020_PRL_2002.11761.pdf",
        expected_kind="pdf",
        minimum_bytes=1000,
        acquisition_role="provenance PDF for R10 alpha(lambda) curve digitization",
    ),
    DownloadSpec(
        external_id="EXT1492_3_R10_PUBMED_2020",
        arena="R10_short_range_inverse_square",
        title="PubMed record for PRL 124 101101",
        source_url="https://pubmed.ncbi.nlm.nih.gov/32216404/",
        download_url="https://pubmed.ncbi.nlm.nih.gov/32216404/",
        local_path=R10 / "docs" / "Lee_2020_PRL_pubmed_record.html",
        expected_kind="html",
        minimum_bytes=100,
        acquisition_role="bibliographic metadata cross-check, not a bound curve",
    ),
    DownloadSpec(
        external_id="EXT1492_4_MICROSCOPE_CMSM_PORTAL",
        arena="WEP_MICROSCOPE_TiPt",
        title="MICROSCOPE science data portal",
        source_url="https://cmsm-ds.onera.fr/user/microscope",
        download_url="https://cmsm-ds.onera.fr/user/microscope",
        local_path=MICROSCOPE / "raw" / "CMSM_portal_landing.html",
        expected_kind="html",
        minimum_bytes=100,
        acquisition_role="portal landing/metadata probe only; official arrays still require package export",
    ),
    DownloadSpec(
        external_id="EXT1492_5_MICROSCOPE_PRL_FINAL",
        arena="WEP_MICROSCOPE_TiPt",
        title="MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
        source_url="https://arxiv.org/abs/2209.15487",
        download_url="https://arxiv.org/pdf/2209.15487",
        local_path=MICROSCOPE / "docs" / "Touboul_2022_PRL_final_results.pdf",
        expected_kind="pdf",
        minimum_bytes=1000,
        acquisition_role="provenance PDF for final MICROSCOPE eta bound",
    ),
    DownloadSpec(
        external_id="EXT1492_6_MICROSCOPE_CQG_READOUT",
        arena="WEP_MICROSCOPE_TiPt",
        title="Result of the MICROSCOPE Weak Equivalence Principle test",
        source_url="https://arxiv.org/abs/2209.15488",
        download_url="https://arxiv.org/pdf/2209.15488",
        local_path=MICROSCOPE / "docs" / "Touboul_2022_CQG_readout.pdf",
        expected_kind="pdf",
        minimum_bytes=1000,
        acquisition_role="provenance PDF for readout convention and CMSM route",
    ),
]


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


def sha256_bytes(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def looks_like_pdf(data: bytes, content_type: str) -> bool:
    return data.startswith(b"%PDF") or "pdf" in content_type.lower()


def looks_like_html_or_text(data: bytes, content_type: str) -> bool:
    lowered = content_type.lower()
    prefix = data[:300].lower()
    return (
        "html" in lowered
        or "text" in lowered
        or b"<html" in prefix
        or b"<!doctype html" in prefix
        or b"<body" in prefix
    )


def payload_valid(data: bytes, content_type: str, spec: DownloadSpec) -> bool:
    if len(data) < spec.minimum_bytes:
        return False
    if spec.expected_kind == "pdf":
        return looks_like_pdf(data, content_type)
    if spec.expected_kind == "html":
        return looks_like_html_or_text(data, content_type)
    return True


def blocker_payload_path(spec: DownloadSpec) -> Path:
    suffix = ".fetch_blocker"
    if spec.expected_kind == "pdf":
        return spec.local_path.with_name(f"{spec.local_path.name}{suffix}.html")
    return spec.local_path.with_name(f"{spec.local_path.name}{suffix}.txt")


def fetch(spec: DownloadSpec) -> tuple[dict[str, Any], dict[str, Any] | None]:
    spec.local_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        spec.download_url,
        headers={
            "User-Agent": "MTS-private-source-acquisition/1493 (+nonclaim provenance audit)",
            "Accept": "application/pdf,text/html,text/plain,*/*",
        },
    )

    base = {
        "same_parent_branch_id": BRANCH_ID,
        "attempt_id": f"DLA1493_{spec.external_id}",
        "external_id": spec.external_id,
        "arena": spec.arena,
        "title": spec.title,
        "source_url": spec.source_url,
        "download_url": spec.download_url,
        "expected_kind": spec.expected_kind,
        "minimum_bytes": spec.minimum_bytes,
        "acquisition_role": spec.acquisition_role,
        "timestamp_utc": utc_now(),
        **flags(),
    }

    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            http_status = getattr(response, "status", "unknown")
            content_type = response.headers.get("content-type", "unknown")
    except urllib.error.HTTPError as exc:
        return (
            {
                **base,
                "local_path": rel(spec.local_path),
                "download_status": "FETCH_FAILED_BLOCKED",
                "http_status": exc.code,
                "content_type": exc.headers.get("content-type", "unknown") if exc.headers else "unknown",
                "byte_count": 0,
                "sha256": "",
                "error": f"HTTPError: {exc.reason}",
            },
            None,
        )
    except urllib.error.URLError as exc:
        return (
            {
                **base,
                "local_path": rel(spec.local_path),
                "download_status": "FETCH_FAILED_BLOCKED",
                "http_status": "unavailable",
                "content_type": "unknown",
                "byte_count": 0,
                "sha256": "",
                "error": f"URLError: {exc.reason}",
            },
            None,
        )
    except TimeoutError as exc:
        return (
            {
                **base,
                "local_path": rel(spec.local_path),
                "download_status": "FETCH_FAILED_BLOCKED",
                "http_status": "timeout",
                "content_type": "unknown",
                "byte_count": 0,
                "sha256": "",
                "error": f"TimeoutError: {exc}",
            },
            None,
        )

    digest = sha256_bytes(data)
    is_valid_payload = payload_valid(data, content_type, spec)
    saved_path = spec.local_path if is_valid_payload else blocker_payload_path(spec)
    saved_path.parent.mkdir(parents=True, exist_ok=True)
    saved_path.write_bytes(data)

    if spec.external_id == "EXT1492_4_MICROSCOPE_CMSM_PORTAL" and is_valid_payload:
        status = "LANDING_PAGE_ONLY_BLOCKED"
    elif is_valid_payload and spec.expected_kind == "pdf":
        status = "DOWNLOADED_PDF_PROVENANCE_ONLY"
    elif is_valid_payload:
        status = "DOWNLOADED_METADATA_PROVENANCE_ONLY"
    else:
        status = "FETCHED_INVALID_PAYLOAD_BLOCKED"

    attempt_row = {
        **base,
        "local_path": rel(saved_path),
        "download_status": status,
        "http_status": http_status,
        "content_type": content_type,
        "byte_count": len(data),
        "sha256": digest,
        "error": "" if is_valid_payload else "payload did not match expected kind/size; saved as blocker evidence",
    }
    provenance_row = {
        "same_parent_branch_id": BRANCH_ID,
        "provenance_id": f"HASH1493_{spec.external_id}",
        "external_id": spec.external_id,
        "arena": spec.arena,
        "file_path": rel(saved_path),
        "source_url": spec.source_url,
        "download_url": spec.download_url,
        "content_type": content_type,
        "byte_count": len(data),
        "sha256": digest,
        "payload_kind": spec.expected_kind if is_valid_payload else "invalid_or_blocker_payload",
        "provenance_status": "SOURCE_FILE_ACQUIRED_NONCLAIM" if is_valid_payload else "BLOCKER_PAYLOAD_SAVED_NONCLAIM",
        "timestamp_utc": utc_now(),
        **flags(),
    }
    return attempt_row, provenance_row


def blocker_rows(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(attempts):
        status = str(row["download_status"])
        if status == "DOWNLOADED_PDF_PROVENANCE_ONLY":
            reason = "PDF is acquired, but tables/figures have not been extracted into scoreable target files"
            blocker = "PDF_TEXT_TABLE_OR_FIGURE_EXTRACTION_MISSING"
        elif status == "DOWNLOADED_METADATA_PROVENANCE_ONLY":
            reason = "metadata page is acquired, but it is not a bound curve or official data product"
            blocker = "METADATA_ONLY_NOT_SCOREABLE"
        elif status == "LANDING_PAGE_ONLY_BLOCKED":
            reason = "CMSM landing page is acquired, but official arrays/download package are still missing"
            blocker = "MICROSCOPE_PORTAL_LANDING_ONLY"
        else:
            reason = f"source acquisition did not produce a validated {row['expected_kind']} payload"
            blocker = "SOURCE_FETCH_FAILED_OR_INVALID"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "blocker_id": f"BLK1493_{index}_{row['external_id']}",
                "external_id": row["external_id"],
                "arena": row["arena"],
                "blocking_marker": blocker,
                "reason": reason,
                "local_evidence_path": row["local_path"],
                "download_status": status,
                "next_action": "extract and promote target data under explicit nonclaim gates",
                **flags(),
            }
        )
    rows.extend(
        [
            {
                "same_parent_branch_id": BRANCH_ID,
                "blocker_id": "BLK1493_same_branch_projection",
                "external_id": "all_delta_w_sources",
                "arena": "all_delta_w_arenas",
                "blocking_marker": "SAME_BRANCH_PROJECTION_PRODUCTS_MISSING",
                "reason": "source PDFs do not supply C_parent, tau maps, source kernels, or response vectors by themselves",
                "local_evidence_path": "not_applicable",
                "download_status": "BLOCKED_BY_THEORY_INPUTS",
                "next_action": "derive/source C_parent-free projection kernels or keep the residual branch explicit",
                **flags(),
            },
            {
                "same_parent_branch_id": BRANCH_ID,
                "blocker_id": "BLK1493_claim_gate",
                "external_id": "all_delta_w_sources",
                "arena": "local_GR_Newton",
                "blocking_marker": "CLAIM_PROMOTION_FORBIDDEN",
                "reason": "1493 is acquisition/provenance plumbing, not a local GR/Newton proof or empirical score",
                "local_evidence_path": "not_applicable",
                "download_status": "NONCLAIM_GATE_ACTIVE",
                "next_action": "only promote after extracted numeric rows and parent-owned kernels pass validation",
                **flags(),
            },
        ]
    )
    return rows


def r10_digitization_rows(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    r10_pdf = next(row for row in attempts if row["external_id"] == "EXT1492_2_R10_ARXIV_2020")
    r10_pdf_present = Path(ROOT / str(r10_pdf["local_path"])).exists()
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "digitization_id": "R10DIG1493_0_source_pdf",
            "object": "R10_2020_PRL_PDF",
            "source_path": r10_pdf["local_path"],
            "source_present": r10_pdf_present,
            "extraction_method": "PDF figure/table extraction not yet run",
            "digitization_status": "SOURCE_PDF_AVAILABLE_NONCLAIM" if r10_pdf_present else "SOURCE_PDF_MISSING_BLOCKED",
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound": "",
            "confidence": "",
            "curve_row_type": "source_file_only",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "digitization_id": "R10DIG1493_1_curve_target",
            "object": "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "source_path": rel(R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"),
            "source_present": (R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv").exists(),
            "extraction_method": "digitize alpha(lambda) curve or locate machine-readable table",
            "digitization_status": "NOT_DIGITIZED",
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound": "",
            "confidence": "",
            "curve_row_type": "required_full_curve_missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "digitization_id": "R10DIG1493_2_abstract_anchor",
            "object": "R10_gravity_strength_threshold_anchor",
            "source_path": r10_pdf["local_path"] if r10_pdf_present else "https://arxiv.org/abs/2002.11761",
            "source_present": r10_pdf_present,
            "extraction_method": "abstract threshold only; not a curve",
            "digitization_status": "ANCHOR_ONLY_NON_CURVE",
            "lambda_value": "38.6",
            "lambda_units": "um",
            "alpha_bound": "1",
            "confidence": "paper_claim_context_not_promoted",
            "curve_row_type": "anchor_only_non_curve",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "digitization_id": "R10DIG1493_3_claim_gate",
            "object": "R10_delta_w_score_gate",
            "source_path": rel(R10 / "derived" / "R10_delta_w_kernel_lambda.csv"),
            "source_present": (R10 / "derived" / "R10_delta_w_kernel_lambda.csv").exists(),
            "extraction_method": "parent-owned delta_w to alpha(lambda) projection kernel",
            "digitization_status": "KERNEL_MISSING_SCORE_BLOCKED",
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound": "",
            "confidence": "",
            "curve_row_type": "kernel_required",
            **flags(),
        },
    ]


def eotwash_skeleton_rows(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prl = next(row for row in attempts if row["external_id"] == "EXT1492_0_EOTWASH_PRL_2008")
    review = next(row for row in attempts if row["external_id"] == "EXT1492_1_EOTWASH_CQG_2012")
    prl_present = Path(ROOT / str(prl["local_path"])).exists()
    review_present = Path(ROOT / str(review["local_path"])).exists()
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "extract_id": "EOT1493_0_PRL_source",
            "object": "EotWash_2008_PRL_source_pdf",
            "source_path": prl["local_path"],
            "source_present": prl_present,
            "required_target": rel(EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv"),
            "known_text_anchor": "eta_BeTi=(0.3 +/- 1.8)e-13 from source abstract; not promoted as table row here",
            "extraction_status": "PDF_AVAILABLE_TABLE_NOT_EXTRACTED" if prl_present else "PDF_MISSING_BLOCKED",
            "next_action": "extract material pair, source attractor, eta, sigma, confidence, units, and source path",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "extract_id": "EOT1493_1_review_source",
            "object": "EotWash_2012_CQG_review_pdf",
            "source_path": review["local_path"],
            "source_present": review_present,
            "required_target": rel(EOTWASH / "derived" / "P_WEP_EotWash_material_response_vectors.csv"),
            "known_text_anchor": "review context for Be-Al/Be-Ti torsion balance tests; not a response-vector table here",
            "extraction_status": "PDF_AVAILABLE_RESPONSE_VECTOR_NOT_EXTRACTED" if review_present else "PDF_MISSING_BLOCKED",
            "next_action": "build same-basis material response vector table with composition/source convention",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "extract_id": "EOT1493_2_claim_gate",
            "object": "EotWash_delta_w_score_gate",
            "source_path": rel(EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv"),
            "source_present": (EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv").exists(),
            "required_target": rel(EOTWASH / "derived" / "P_WEP_EotWash_material_response_vectors.csv"),
            "known_text_anchor": "none",
            "extraction_status": "TARGET_TABLES_MISSING_SCORE_BLOCKED",
            "next_action": "promote only after both eta bounds and material response vectors parse and remain sourced",
            **flags(),
        },
    ]


def microscope_status_rows(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    portal = next(row for row in attempts if row["external_id"] == "EXT1492_4_MICROSCOPE_CMSM_PORTAL")
    prl = next(row for row in attempts if row["external_id"] == "EXT1492_5_MICROSCOPE_PRL_FINAL")
    cqg = next(row for row in attempts if row["external_id"] == "EXT1492_6_MICROSCOPE_CQG_READOUT")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "microscope_id": "MIC1493_0_portal_probe",
            "object": "CMSM_portal_landing",
            "source_path": portal["local_path"],
            "source_present": Path(ROOT / str(portal["local_path"])).exists(),
            "parse_status": "LANDING_PAGE_ONLY_NOT_OFFICIAL_ARRAYS"
            if portal["download_status"] == "LANDING_PAGE_ONLY_BLOCKED"
            else "PORTAL_PROBE_FAILED_OR_INVALID",
            "required_target": rel(MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"),
            "next_action": "obtain official CMSM export/package or a reproducible parser for official arrays",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "microscope_id": "MIC1493_1_final_prl_pdf",
            "object": "MICROSCOPE_final_PRL_bound_source",
            "source_path": prl["local_path"],
            "source_present": Path(ROOT / str(prl["local_path"])).exists(),
            "parse_status": "PDF_AVAILABLE_BOUND_TEXT_NOT_TABLE_EXTRACTED"
            if Path(ROOT / str(prl["local_path"])).exists()
            else "PDF_MISSING_BLOCKED",
            "required_target": rel(MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"),
            "next_action": "extract/confirm eta result and material convention without replacing official arrays",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "microscope_id": "MIC1493_2_CQG_readout_pdf",
            "object": "MICROSCOPE_CQG_readout_convention_source",
            "source_path": cqg["local_path"],
            "source_present": Path(ROOT / str(cqg["local_path"])).exists(),
            "parse_status": "PDF_AVAILABLE_READOUT_CONVENTION_NOT_PARSED"
            if Path(ROOT / str(cqg["local_path"])).exists()
            else "PDF_MISSING_BLOCKED",
            "required_target": rel(MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"),
            "next_action": "validate product convention content against readout/source-kernel units",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "microscope_id": "MIC1493_3_official_arrays_gate",
            "object": "MICROSCOPE_score_gate",
            "source_path": rel(MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"),
            "source_present": (MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv").exists(),
            "parse_status": "OFFICIAL_ARRAYS_MISSING_SCORE_BLOCKED",
            "required_target": rel(MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"),
            "next_action": "do not score MICROSCOPE until official readout/source/product/material tensors are all populated",
            **flags(),
        },
    ]


def score_readiness_rows() -> list[dict[str, Any]]:
    required = [
        ("WEP_EotWash_material_pairs", EOTWASH / "derived" / "P_WEP_EotWash_material_pair_bounds.csv"),
        ("WEP_EotWash_material_vectors", EOTWASH / "derived" / "P_WEP_EotWash_material_response_vectors.csv"),
        ("R10_alpha_lambda_curve", R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"),
        ("R10_delta_w_kernel", R10 / "derived" / "R10_delta_w_kernel_lambda.csv"),
        ("MICROSCOPE_readout", MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"),
        ("MICROSCOPE_source_worldtube", MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"),
        ("MICROSCOPE_product_convention", MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"),
        ("MICROSCOPE_material_tensor", MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"),
    ]
    rows = []
    for index, (object_id, path) in enumerate(required):
        exists = path.exists()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "readiness_id": f"READY1493_{index}_{object_id}",
                "object": object_id,
                "path": rel(path),
                "path_exists": exists,
                "content_status": "EXISTS_REQUIRES_CONTENT_VALIDATION" if exists else "MISSING_OR_UNPROMOTED",
                "score_effect": "BLOCKS_SCORE_UNTIL_EXTRACTED_AND_PARENT_PROJECTED",
                "required_before_claim": True,
                **flags(),
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": "READY1493_overall",
            "object": "delta_w_cross_arena_score",
            "path": "not_applicable",
            "path_exists": False,
            "content_status": "NOT_SCORE_READY",
            "score_effect": "NO_WEP_R10_LOCAL_GR_OR_NEWTON_CLAIM_FROM_1493",
            "required_before_claim": True,
            **flags(),
        }
    )
    return rows


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1493_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "source acquisition cannot supply or infer parent coupling coefficients",
            "claim_effect": "universal coupling and local-GR/Newton claims remain blocked",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1493_0_downloads",
            "target": "source PDFs and metadata",
            "current_status": "ACQUIRED_IF_HASHED_BUT_NONCLAIM",
            "claim_effect": "provenance improves, no physics claim changes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1493_1_delta_w",
            "target": "delta_w empirical score",
            "current_status": "TARGET_DATA_AND_PROJECTION_KERNELS_MISSING",
            "claim_effect": "WEP/R10 score blocked",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1493_2_local_GR",
            "target": "local GR/Newton reduction",
            "current_status": "NOT_CLOSED",
            "claim_effect": "no local-GR/Newton claim from acquisition branch",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1493_3_next",
            "target": "next work",
            "current_status": "PDF_TEXT_TABLE_EXTRACTION_OR_MANUAL_DIGITIZATION_QUEUE",
            "claim_effect": "next pass can mine acquired files but must keep nonclaim until targets validate",
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    reasons = [
        ("REJ1493_0_extraction", "SOURCE_FILES_NOT_TARGET_DATA", "downloaded PDFs/HTML are provenance inputs, not scoreable bound rows"),
        ("REJ1493_1_R10", "R10_CURVE_NOT_DIGITIZED", "R10 alpha(lambda) curve and delta_w kernel still absent"),
        ("REJ1493_2_EotWash", "EOTWASH_TABLES_NOT_EXTRACTED", "EotWash eta/material response vectors remain missing"),
        ("REJ1493_3_MICROSCOPE", "MICROSCOPE_OFFICIAL_ARRAYS_MISSING", "portal landing/PDFs do not replace official CMSM arrays"),
        ("REJ1493_4_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "downloaded empirical sources do not derive coupling coefficients"),
        ("REJ1493_5_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/R10/local-GR/Newton pass may be claimed"),
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


def decision_rows(any_pdf: bool) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1493_0_provenance_not_claim",
            "decision": "download/hash source files where accessible, but keep all rows nonclaim",
            "rationale": "source acquisition is a prerequisite, not a result",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1493_1_R10",
            "decision": "treat R10 abstract threshold as anchor-only non-curve until full alpha(lambda) curve is digitized",
            "rationale": "an alpha=1 threshold sentence is not a usable bound curve for model comparison",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1493_2_MICROSCOPE",
            "decision": "treat CMSM landing page and papers as route/provenance only until official arrays are acquired",
            "rationale": "readout kernels and arrays are needed for same-branch delta_w projection",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1493_3_next",
            "decision": "move to PDF text/table extraction and manual digitization queue"
            if any_pdf
            else "repeat/acquire sources manually before extraction",
            "rationale": "at least one PDF exists for extraction" if any_pdf else "no valid PDF payload was acquired",
            **flags(),
        },
    ]


def next_target_rows(any_pdf: bool) -> list[dict[str, Any]]:
    if any_pdf:
        target = "1494-Y5-R10-RAB-PDF-table-text-extraction-for-EotWash-and-R10-curve-digitization.md"
        script = "scripts/Y5_R10_RAB_pdf_table_text_extraction_for_EotWash_and_R10_curve_digitization.py"
        objective = (
            "extract text/tables from acquired PDFs where possible, stage manual R10 curve digitization, "
            "and keep EotWash/MICROSCOPE/R10 rows nonclaim until numeric target files validate"
        )
    else:
        target = "1494-Y5-R10-RAB-source-acquisition-retry-or-user-assisted-download-queue.md"
        script = "scripts/Y5_R10_RAB_source_acquisition_retry_or_user_assisted_download_queue.py"
        objective = (
            "record manual download instructions or alternate mirrors because automated acquisition did not yield PDFs"
        )
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1493_0_1494",
            "next_target": target,
            "script": script,
            "objective": objective,
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


def validation_rows(
    attempts: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    generated_csvs: list[Path],
) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    attempts_complete = all(row["download_url"] and row["local_path"] and row["download_status"] for row in attempts)
    hashes_ok = all(
        row["sha256"] and int(row["byte_count"]) >= 0 and Path(ROOT / str(row["file_path"])).exists()
        for row in provenance
    )
    downloaded_ok = all(
        row["sha256"] and int(row["byte_count"]) >= int(row["minimum_bytes"])
        for row in attempts
        if str(row["download_status"]).startswith("DOWNLOADED") or row["download_status"] == "LANDING_PAGE_ONLY_BLOCKED"
    )
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_DOWNLOADS, QUAR_HASHES, QUAR_BLOCKERS, QUAR_READINESS, BRANCH_DOWNLOADS, BRANCH_HASHES, BRANCH_BLOCKERS, BRANCH_READINESS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    readiness_nonclaim = all(row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in read_csv(SCORE_READINESS))

    checks = [
        ("VAL1493_0_local_sources", source_paths_exist, "all cited 1492 local source paths exist"),
        ("VAL1493_1_attempt_rows", attempts_complete, "every download attempt records URL, local path, and status"),
        ("VAL1493_2_hash_rows", hashes_ok, "every saved payload has sha256, byte_count, and local file"),
        ("VAL1493_3_downloaded_thresholds", downloaded_ok, "downloaded/landing payload rows meet minimum byte thresholds"),
        ("VAL1493_4_extraction_blockers", len(read_csv(EXTRACTION_BLOCKERS)) >= len(attempts), "every acquisition route retains an extraction/claim blocker"),
        ("VAL1493_5_R10_noncurve_gate", all(row["valid_for_claim"] == "False" for row in read_csv(R10_DIGITIZATION)), "R10 anchor/curve skeleton remains nonclaim"),
        ("VAL1493_6_EotWash_nonclaim", all(row["valid_for_claim"] == "False" for row in read_csv(EOTWASH_SKELETON)), "EotWash extraction skeleton remains nonclaim"),
        ("VAL1493_7_MICROSCOPE_nonclaim", all(row["valid_for_claim"] == "False" for row in read_csv(MICROSCOPE_STATUS)), "MICROSCOPE portal/PDF rows remain nonclaim"),
        ("VAL1493_8_readiness_blocked", readiness_nonclaim, "delta_w score readiness remains false"),
        ("VAL1493_9_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1493_10_csv_parse", csv_parse_ok, "all generated 1493 CSVs parse cleanly"),
        ("VAL1493_11_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1493_12_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1493_13_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1493_14_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
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
            "check_id": "VAL1493_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1493 acquired/hashes accessible source files and keeps all delta_w/local claims blocked"
            if overall
            else "1493 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    attempts: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    r10_rows: list[dict[str, Any]],
    eot_rows: list[dict[str, Any]],
    mic_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1493 - Download or Extract delta_w Source Files: R10, EotWash, MICROSCOPE",
                "",
                "## Verdict",
                "- Automated source acquisition has been attempted for EotWash, R10, PubMed metadata, and MICROSCOPE paper/portal routes.",
                "- Any downloaded PDF/HTML is treated as provenance only; no curve, WEP table, CMSM array, or parent coupling row is promoted.",
                "- `delta_w`, WEP, R10, local-GR, and Newton-limit claims remain blocked until numeric target files and same-branch projection kernels exist.",
                "",
                "## Download Attempt Ledger",
                md_table(attempts, ["external_id", "arena", "download_status", "http_status", "byte_count", "local_path"]),
                "",
                "## Extraction Blockers",
                md_table(blockers, ["blocker_id", "arena", "blocking_marker", "download_status", "reason"]),
                "",
                "## R10 Curve Digitization Skeleton",
                md_table(r10_rows, ["digitization_id", "object", "source_present", "digitization_status", "curve_row_type"]),
                "",
                "## EotWash Extraction Skeleton",
                md_table(eot_rows, ["extract_id", "object", "source_present", "extraction_status", "next_action"]),
                "",
                "## MICROSCOPE Parse Status",
                md_table(mic_rows, ["microscope_id", "object", "source_present", "parse_status", "next_action"]),
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


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (DOWNLOAD_ATTEMPTS, QUAR_DOWNLOADS),
        (FILE_PROVENANCE, QUAR_HASHES),
        (EXTRACTION_BLOCKERS, QUAR_BLOCKERS),
        (SCORE_READINESS, QUAR_READINESS),
        (DOWNLOAD_ATTEMPTS, BRANCH_DOWNLOADS),
        (FILE_PROVENANCE, BRANCH_HASHES),
        (EXTRACTION_BLOCKERS, BRANCH_BLOCKERS),
        (SCORE_READINESS, BRANCH_READINESS),
    ]:
        shutil.copyfile(src, dst)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for directory in [
        EOTWASH / "raw",
        EOTWASH / "docs",
        EOTWASH / "derived",
        R10 / "raw",
        R10 / "docs",
        R10 / "derived",
        MICROSCOPE / "raw",
        MICROSCOPE / "docs",
        MICROSCOPE / "official_readout",
        MICROSCOPE / "source_worldtube",
        MICROSCOPE / "product_convention",
        MICROSCOPE / "derived",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    for spec in DOWNLOAD_SPECS:
        attempt_row, provenance_row = fetch(spec)
        attempts.append(attempt_row)
        if provenance_row is not None:
            provenance.append(provenance_row)

    blockers = blocker_rows(attempts)
    r10_rows = r10_digitization_rows(attempts)
    eot_rows = eotwash_skeleton_rows(attempts)
    mic_rows = microscope_status_rows(attempts)
    readiness = score_readiness_rows()
    c_parent_rows = c_parent_refusal_rows()
    local_rows = local_status_rows()
    rejections = rejection_rows()
    any_pdf = any(row["download_status"] == "DOWNLOADED_PDF_PROVENANCE_ONLY" for row in attempts)
    decisions = decision_rows(any_pdf)
    next_rows = next_target_rows(any_pdf)

    write_csv(DOWNLOAD_ATTEMPTS, attempts)
    write_csv(FILE_PROVENANCE, provenance)
    write_csv(EXTRACTION_BLOCKERS, blockers)
    write_csv(R10_DIGITIZATION, r10_rows)
    write_csv(EOTWASH_SKELETON, eot_rows)
    write_csv(MICROSCOPE_STATUS, mic_rows)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        DOWNLOAD_ATTEMPTS,
        FILE_PROVENANCE,
        EXTRACTION_BLOCKERS,
        R10_DIGITIZATION,
        EOTWASH_SKELETON,
        MICROSCOPE_STATUS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(attempts, provenance, generated_csvs)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(attempts, blockers, r10_rows, eot_rows, mic_rows, validation, next_rows)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
