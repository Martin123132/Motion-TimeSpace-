from __future__ import annotations

import csv
import gzip
import hashlib
import io
import re
import shutil
import tarfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_INTAKE = ROOT / "source-intake"
R10 = SOURCE_INTAKE / "r10"
MICROSCOPE = SOURCE_INTAKE / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1495-Y5-R10-RAB-R10-alpha-lambda-curve-digitization-or-machine-readable-table-hunt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1494_r10_queue": OUT / "P8_Y5_R10_1494_R10_MANUAL_DIGITIZATION_QUEUE.csv",
    "1494_anchors": OUT / "P8_Y5_R10_1494_TEXT_ANCHOR_CANDIDATES.csv",
    "1494_blockers": OUT / "P8_Y5_R10_1494_TARGET_PROMOTION_BLOCKERS.csv",
    "1494_readiness": OUT / "P8_Y5_R10_1494_DELTA_W_SCORE_READINESS.csv",
    "1494_validation": OUT / "P8_Y5_BRR545_1494_VALIDATION.csv",
    "1494_next": OUT / "P8_Y5_R10_1494_NEXT_TARGET.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"
ARCHIVE_URL = "https://arxiv.org/e-print/2002.11761"
ARCHIVE_FILE = R10 / "raw" / "Lee_2020_PRL_2002.11761_source.tar.gz"
ARCHIVE_EXTRACT_DIR = R10 / "raw" / "Lee_2020_PRL_2002.11761_source_1495"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"

ARCHIVE_ACQUISITION = OUT / "P8_Y5_R10_1495_R10_SOURCE_ARCHIVE_ACQUISITION.csv"
ARCHIVE_MANIFEST = OUT / "P8_Y5_R10_1495_R10_SOURCE_ARCHIVE_FILE_MANIFEST.csv"
TEX_ANCHOR_SCAN = OUT / "P8_Y5_R10_1495_R10_TEX_ANCHOR_SCAN.csv"
FIGURE_TARGETS = OUT / "P8_Y5_R10_1495_R10_FIGURE_DIGITIZATION_TARGETS.csv"
MACHINE_TABLE_HUNT = OUT / "P8_Y5_R10_1495_R10_MACHINE_TABLE_HUNT.csv"
CURVE_STATUS = OUT / "P8_Y5_R10_1495_R10_ALPHA_LAMBDA_CURVE_STATUS.csv"
KERNEL_CONTRACT = OUT / "P8_Y5_R10_1495_DELTA_W_KERNEL_INPUT_CONTRACT.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1495_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1495_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1495_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1495_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1495_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1495_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1495_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1495_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1495"
QUAR_ARCHIVE = QUARANTINE / "R10_SOURCE_ARCHIVE_ACQUISITION_NONCLAIM.csv"
QUAR_FIGURES = QUARANTINE / "R10_FIGURE_DIGITIZATION_TARGETS_NONCLAIM.csv"
QUAR_CURVE = QUARANTINE / "R10_ALPHA_LAMBDA_CURVE_STATUS_NONCLAIM.csv"
QUAR_KERNEL = QUARANTINE / "DELTA_W_KERNEL_INPUT_CONTRACT_NONCLAIM.csv"
BRANCH_ARCHIVE = BRANCH_RESIDUALS / "r10_source_archive_acquisition_nonclaim_1495.csv"
BRANCH_FIGURES = BRANCH_RESIDUALS / "r10_figure_digitization_targets_nonclaim_1495.csv"
BRANCH_CURVE = BRANCH_RESIDUALS / "r10_alpha_lambda_curve_status_nonclaim_1495.csv"
BRANCH_KERNEL = BRANCH_RESIDUALS / "delta_w_kernel_input_contract_nonclaim_1495.csv"


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


def normalize_text(text: str) -> str:
    text = text.replace("\u2212", "-").replace("\u00d7", "x").replace("\u03bc", "um").replace("\u00b5", "um")
    return re.sub(r"\s+", " ", text).strip()


def fetch_archive() -> dict[str, Any]:
    ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        ARCHIVE_URL,
        headers={
            "User-Agent": "MTS-private-R10-source-hunt/1495 (+nonclaim provenance audit)",
            "Accept": "application/x-eprint-tar,application/gzip,application/octet-stream,*/*",
        },
    )
    base = {
        "same_parent_branch_id": BRANCH_ID,
        "archive_id": "ARCH1495_R10_ARXIV_SOURCE",
        "source_url": ARCHIVE_URL,
        "local_path": rel(ARCHIVE_FILE),
        "timestamp_utc": utc_now(),
        **flags(),
    }
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            status = getattr(response, "status", "unknown")
            content_type = response.headers.get("content-type", "unknown")
    except urllib.error.HTTPError as exc:
        return {
            **base,
            "download_status": "FETCH_FAILED_BLOCKED",
            "http_status": exc.code,
            "content_type": exc.headers.get("content-type", "unknown") if exc.headers else "unknown",
            "byte_count": 0,
            "sha256": "",
            "error": f"HTTPError: {exc.reason}",
        }
    except urllib.error.URLError as exc:
        return {
            **base,
            "download_status": "FETCH_FAILED_BLOCKED",
            "http_status": "unavailable",
            "content_type": "unknown",
            "byte_count": 0,
            "sha256": "",
            "error": f"URLError: {exc.reason}",
        }

    ARCHIVE_FILE.write_bytes(data)
    return {
        **base,
        "download_status": "DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM" if len(data) > 1000 else "DOWNLOADED_TOO_SMALL_BLOCKED",
        "http_status": status,
        "content_type": content_type,
        "byte_count": len(data),
        "sha256": sha256_bytes(data),
        "error": "",
    }


def archive_bytes_for_tar(path: Path) -> bytes:
    data = path.read_bytes()
    if tarfile.is_tarfile(path):
        return data
    try:
        unpacked = gzip.decompress(data)
        return unpacked
    except Exception:
        return data


def safe_extract_archive(archive_path: Path, extract_dir: Path) -> tuple[str, str]:
    extract_dir.mkdir(parents=True, exist_ok=True)
    root_resolved = extract_dir.resolve()
    data = archive_bytes_for_tar(archive_path)
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tar:
            for member in tar.getmembers():
                target = (extract_dir / member.name).resolve()
                if not str(target).startswith(str(root_resolved)):
                    return "EXTRACTION_BLOCKED_PATH_TRAVERSAL", f"unsafe member path: {member.name}"
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    source = tar.extractfile(member)
                    if source is not None:
                        target.write_bytes(source.read())
        return "EXTRACTED_SOURCE_ARCHIVE_NONCLAIM", ""
    except Exception as exc:
        return "EXTRACTION_FAILED_BLOCKED", repr(exc)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_rows(extraction_status: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not ARCHIVE_EXTRACT_DIR.exists() or not extraction_status.startswith("EXTRACTED"):
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "manifest_id": "MAN1495_no_extracted_archive",
                "file_path": rel(ARCHIVE_EXTRACT_DIR),
                "suffix": "",
                "byte_count": 0,
                "sha256": "",
                "file_role_guess": "archive_not_extracted",
                **flags(),
            }
        ]
    for index, path in enumerate(sorted(p for p in ARCHIVE_EXTRACT_DIR.rglob("*") if p.is_file())):
        suffix = path.suffix.lower()
        if suffix in [".tex", ".bbl", ".bib", ".sty", ".cls", ".txt", ".aux"]:
            role = "source_text"
        elif suffix in [".dat", ".csv", ".tsv"]:
            role = "machine_table_candidate"
        elif suffix in [".eps", ".pdf", ".png", ".jpg", ".jpeg"]:
            role = "figure_or_graphic_asset"
        else:
            role = "other_source_asset"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "manifest_id": f"MAN1495_{index}",
                "file_path": rel(path),
                "suffix": suffix,
                "byte_count": path.stat().st_size,
                "sha256": file_sha256(path),
                "file_role_guess": role,
                **flags(),
            }
        )
    return rows


SCAN_PATTERNS = [
    ("alpha_lambda_yukawa", r"(?:alpha|\\alpha).{0,160}(?:lambda|\\lambda|Yukawa)"),
    ("lambda_threshold_38p6", r"38\.6.{0,80}(?:um|\\mu|micron|micrometer)"),
    ("confidence_95", r"95\\?%|95%|95\\s*percent|confidence"),
    ("figure_reference", r"(?:Fig\\.|Figure|figure).{0,160}(?:limit|Yukawa|alpha|lambda|exclusion|constraint)"),
    ("separation_range", r"52.{0,40}(?:um|\\mu|micron).{0,80}3\.0.{0,20}mm"),
]


def read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def concise_excerpt(text: str, start: int, end: int, max_words: int = 24) -> str:
    window = text[max(0, start - 90) : min(len(text), end + 90)]
    words = window.split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words])


def tex_anchor_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_files = [ROOT / row["file_path"] for row in manifest if row["file_role_guess"] == "source_text"]
    if not source_files:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "scan_id": "SCAN1495_no_source_text",
                "file_path": rel(ARCHIVE_EXTRACT_DIR),
                "pattern_name": "source_text_missing",
                "scan_status": "NO_TEX_OR_TEXT_SOURCE_FOUND",
                "char_start": "",
                "short_excerpt_for_manual_review": "",
                **flags(),
            }
        ]
    for path in source_files:
        text = normalize_text(read_text_file(path))
        for pattern_index, (name, pattern) in enumerate(SCAN_PATTERNS):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            rows.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "scan_id": f"SCAN1495_{path.name}_{pattern_index}",
                    "file_path": rel(path),
                    "pattern_name": name,
                    "scan_status": "SOURCE_PATTERN_FOUND_NONCLAIM" if match else "PATTERN_NOT_FOUND",
                    "char_start": match.start() if match else "",
                    "short_excerpt_for_manual_review": concise_excerpt(text, match.start(), match.end()) if match else "",
                    **flags(),
                }
            )
    return rows


def table_hunt_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in manifest if row["file_role_guess"] == "machine_table_candidate"]
    if not candidates:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "table_id": "TAB1495_no_machine_table",
                "file_path": "not_found_in_arxiv_source_archive",
                "table_status": "NO_MACHINE_READABLE_TABLE_FOUND",
                "byte_count": 0,
                "required_validation": "manual figure digitization or external primary-source table required",
                **flags(),
            }
        ]
    rows = []
    for index, row in enumerate(candidates):
        path = ROOT / row["file_path"]
        text = normalize_text(read_text_file(path))[:2000]
        numeric_lines = sum(1 for line in text.splitlines() if re.search(r"\d", line))
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "table_id": f"TAB1495_{index}",
                "file_path": row["file_path"],
                "table_status": "MACHINE_TABLE_CANDIDATE_NEEDS_REVIEW",
                "byte_count": row["byte_count"],
                "required_validation": f"inspect columns/units; numeric_lines_preview={numeric_lines}",
                **flags(),
            }
        )
    return rows


def figure_target_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    figures = [row for row in manifest if row["file_role_guess"] == "figure_or_graphic_asset"]
    if not figures:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "figure_id": "FIG1495_no_figure_asset",
                "file_path": "not_found_in_arxiv_source_archive",
                "figure_status": "NO_FIGURE_ASSET_FOUND",
                "priority": "high",
                "digitization_instruction": "digitize from PDF page manually or use alternate primary source",
                "required_output": rel(CURVE_TARGET),
                **flags(),
            }
        ]
    rows = []
    for index, row in enumerate(figures):
        name = Path(row["file_path"]).name.lower()
        likely_curve = any(token in name for token in ["limit", "alpha", "yuk", "excl", "fig", "lambda"])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "figure_id": f"FIG1495_{index}",
                "file_path": row["file_path"],
                "figure_status": "FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED",
                "priority": "high" if likely_curve else "medium",
                "digitization_instruction": (
                    "inspect this figure for alpha(lambda) exclusion curve; extract axes, confidence level, and ordered points"
                    if likely_curve
                    else "inspect figure role before using; do not promote without axis/curve verification"
                ),
                "required_output": rel(CURVE_TARGET),
                **flags(),
            }
        )
    return rows


def curve_status_rows(table_rows: list[dict[str, Any]], figure_rows: list[dict[str, Any]], scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    has_table_candidate = any(row["table_status"] == "MACHINE_TABLE_CANDIDATE_NEEDS_REVIEW" for row in table_rows)
    has_figure_asset = any(row["figure_status"] == "FIGURE_ASSET_FOUND_MANUAL_DIGITIZATION_REQUIRED" for row in figure_rows)
    has_tex_threshold = any(row["pattern_name"] == "lambda_threshold_38p6" and row["scan_status"] == "SOURCE_PATTERN_FOUND_NONCLAIM" for row in scan_rows)
    if has_table_candidate:
        status = "MACHINE_TABLE_CANDIDATE_FOUND_NOT_VALIDATED"
        next_action = "validate candidate table columns/units against PDF curve before promotion"
    elif has_figure_asset:
        status = "FIGURE_ASSET_FOUND_DIGITIZATION_REQUIRED"
        next_action = "digitize alpha(lambda) curve from source figure asset"
    elif has_tex_threshold:
        status = "ONLY_TEXT_THRESHOLD_FOUND_NON_CURVE"
        next_action = "manual PDF curve digitization or primary data-table hunt required"
    else:
        status = "CURVE_SOURCE_NOT_FOUND_BLOCKED"
        next_action = "manual PDF inspection or external primary source search required"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "curve_status_id": "CURVE1495_0_R10_alpha_lambda",
            "curve_target_path": rel(CURVE_TARGET),
            "curve_target_exists": CURVE_TARGET.exists(),
            "machine_table_candidate": has_table_candidate,
            "figure_asset_candidate": has_figure_asset,
            "text_threshold_anchor": has_tex_threshold,
            "curve_status": status,
            "next_action": next_action,
            **flags(),
        }
    ]


def kernel_contract_rows() -> list[dict[str, Any]]:
    inputs = [
        ("KERN1495_0_curve", "R10 alpha(lambda) bound curve", rel(CURVE_TARGET), "empirical_input", "MISSING_OR_UNPROMOTED"),
        ("KERN1495_1_geometry", "R10 test/source geometry response function", "source-intake/r10/derived/R10_geometry_response_kernel.csv", "experimental_projection", "MISSING"),
        ("KERN1495_2_basis", "delta_w component basis and units", "source-intake/mts_residuals/P8_Y5_R10_delta_w_basis_contract.csv", "theory_projection", "MISSING"),
        ("KERN1495_3_parent", "parent coupling normalization or explicit residual prior", rel(C_PARENT_IMPORT), "parent_action_input", "FORBIDDEN_TO_IMPORT_UNDER_1495"),
        ("KERN1495_4_mapping", "map from delta_w residual to Yukawa alpha convention", rel(KERNEL_TARGET), "same_branch_kernel", "MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_input_id": input_id,
            "required_input": required_input,
            "target_path": path,
            "input_owner": owner,
            "current_status": status,
            "failure_effect": "R10 delta_w score remains blocked",
            **flags(),
        }
        for input_id, required_input, path, owner, status in inputs
    ]


def blocker_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    curve_status = curve_rows[0]["curve_status"]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1495_0_curve",
            "blocking_marker": "R10_ALPHA_LAMBDA_CURVE_NOT_PROMOTED",
            "reason": f"curve status={curve_status}; live target remains absent",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1495_1_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "even a digitized bound curve is not an MTS prediction without the same-branch projection kernel",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1495_2_claim",
            "blocking_marker": "CLAIM_PROMOTION_FORBIDDEN",
            "reason": "source archive hunt does not prove local GR/Newton or pass R10",
            "target_path": "not_applicable",
            **flags(),
        },
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": f"READY1495_{index}_{row['blocker_id']}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "content_status": "BLOCKED",
            "score_effect": row["reason"],
            "required_before_claim": True,
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1495_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "R10 source archive cannot derive parent coupling normalization",
            "claim_effect": "R10 empirical branch remains residual/kernel blocked",
            **flags(),
        }
    ]


def local_status_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1495_0_archive",
            "target": "R10 arXiv source archive",
            "current_status": curve_rows[0]["curve_status"],
            "claim_effect": "improves digitization route only; no R10 pass",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1495_1_local_GR",
            "target": "local GR/Newton reduction",
            "current_status": "NOT_CLOSED",
            "claim_effect": "no local-GR/Newton claim from R10 source archive",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1495_2_next",
            "target": "next work",
            "current_status": "DIGITIZE_CURVE_OR_BUILD_KERNEL_CONTRACT",
            "claim_effect": "best next step is curve extraction plus explicit kernel law",
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    reasons = [
        ("REJ1495_0_curve", "CURVE_NOT_PROMOTED", "R10 alpha(lambda) live target remains absent or unvalidated"),
        ("REJ1495_1_kernel", "PROJECTION_KERNEL_MISSING", "delta_w-to-alpha kernel remains absent"),
        ("REJ1495_2_anchor", "ANCHOR_ONLY_NOT_CURVE", "38.6 um alpha=1 threshold cannot replace full curve"),
        ("REJ1495_3_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "source archive does not derive coupling coefficients"),
        ("REJ1495_4_claim", "CLAIM_PROMOTION_FORBIDDEN", "no R10/local-GR/Newton pass may be claimed"),
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


def decision_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1495_0_source_archive",
            "decision": "use arXiv source archive as the primary local route for R10 curve assets",
            "rationale": "source assets are cleaner than eyeballing the rendered PDF",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1495_1_curve_status",
            "decision": f"keep curve nonclaim with status {curve_rows[0]['curve_status']}",
            "rationale": "the live curve file is still absent and requires unit/axis validation",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1495_2_kernel",
            "decision": "write the kernel input contract before any score run",
            "rationale": "R10 bound data alone is not an MTS prediction",
            **flags(),
        },
    ]


def next_target_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if curve_rows[0]["figure_asset_candidate"] == "True" or curve_rows[0]["figure_asset_candidate"] is True:
        target = "1496-Y5-R10-RAB-R10-source-figure-axis-detection-and-digitization-stub.md"
        script = "scripts/Y5_R10_RAB_R10_source_figure_axis_detection_and_digitization_stub.py"
        objective = "inspect source figure assets, identify alpha(lambda) axes, and produce a nonclaim digitization template with units/confidence gates"
    else:
        target = "1496-Y5-R10-RAB-R10-curve-manual-digitization-or-external-primary-table-search.md"
        script = "scripts/Y5_R10_RAB_R10_curve_manual_digitization_or_external_primary_table_search.py"
        objective = "build a manual digitization queue or locate a primary machine-readable R10 bound curve source"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1495_0_1496",
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


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (ARCHIVE_ACQUISITION, QUAR_ARCHIVE),
        (FIGURE_TARGETS, QUAR_FIGURES),
        (CURVE_STATUS, QUAR_CURVE),
        (KERNEL_CONTRACT, QUAR_KERNEL),
        (ARCHIVE_ACQUISITION, BRANCH_ARCHIVE),
        (FIGURE_TARGETS, BRANCH_FIGURES),
        (CURVE_STATUS, BRANCH_CURVE),
        (KERNEL_CONTRACT, BRANCH_KERNEL),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], acquisition: dict[str, Any], manifest: list[dict[str, Any]], scan_rows: list[dict[str, Any]], curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    download_recorded = acquisition["download_status"] in ["DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM", "DOWNLOADED_TOO_SMALL_BLOCKED", "FETCH_FAILED_BLOCKED"]
    archive_hash_ok = bool(acquisition["sha256"]) and int(acquisition["byte_count"]) > 1000 if acquisition["download_status"] == "DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM" else True
    manifest_present = len(manifest) > 0
    scan_present = len(scan_rows) > 0
    curve_not_promoted = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_ARCHIVE, QUAR_FIGURES, QUAR_CURVE, QUAR_KERNEL, BRANCH_ARCHIVE, BRANCH_FIGURES, BRANCH_CURVE, BRANCH_KERNEL])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    readiness_nonclaim = all(row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in read_csv(SCORE_READINESS))
    checks = [
        ("VAL1495_0_local_sources", source_paths_exist, "all cited 1494 local source paths exist"),
        ("VAL1495_1_archive_attempt", download_recorded, f"archive status={acquisition['download_status']}"),
        ("VAL1495_2_archive_hash", archive_hash_ok, "downloaded archive has sha256 and byte_count over threshold or failure is explicit"),
        ("VAL1495_3_manifest", manifest_present, "archive manifest/blocker row written"),
        ("VAL1495_4_scan", scan_present, "TeX/source scan rows written"),
        ("VAL1495_5_curve_not_promoted", curve_not_promoted, "R10 curve/kernel live targets remain absent"),
        ("VAL1495_6_readiness_blocked", readiness_nonclaim, "delta_w/R10 score readiness remains false"),
        ("VAL1495_7_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1495_8_csv_parse", csv_parse_ok, "all generated 1495 CSVs parse cleanly"),
        ("VAL1495_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1495_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1495_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1495_12_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
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
            "check_id": "VAL1495_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1495 hunted R10 source archive/table/figure route and kept curve/kernel nonclaim"
            if overall
            else "1495 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    acquisition: dict[str, Any],
    manifest: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    table_rows: list[dict[str, Any]],
    figure_rows: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    manifest_summary = []
    for role in sorted({row["file_role_guess"] for row in manifest}):
        role_rows = [row for row in manifest if row["file_role_guess"] == role]
        manifest_summary.append({"file_role_guess": role, "count": len(role_rows)})
    scan_summary = [
        {
            "pattern_name": row["pattern_name"],
            "scan_status": row["scan_status"],
            "file_path": row["file_path"],
        }
        for row in scan_rows[:12]
    ]
    DOC.write_text(
        "\n".join(
            [
                "# 1495 - R10 alpha(lambda) Curve Digitization or Machine-Readable Table Hunt",
                "",
                "## Verdict",
                "- The R10 source archive/table/figure route has been tested and ledgered.",
                "- Any source assets found remain nonclaim: the live `R10_alpha_lambda_bound_curve_DIGITIZED.csv` and `R10_delta_w_kernel_lambda.csv` are not promoted.",
                "- R10 can only become score-ready after a validated curve and the same-branch `delta_w -> alpha(lambda)` kernel both exist.",
                "",
                "## Archive Acquisition",
                md_table([acquisition], ["archive_id", "download_status", "http_status", "byte_count", "local_path"]),
                "",
                "## Archive Manifest Summary",
                md_table(manifest_summary, ["file_role_guess", "count"]),
                "",
                "## Source Anchor Scan Preview",
                md_table(scan_summary, ["pattern_name", "scan_status", "file_path"]),
                "",
                "## Machine Table Hunt",
                md_table(table_rows, ["table_id", "file_path", "table_status", "required_validation"]),
                "",
                "## Figure Digitization Targets",
                md_table(figure_rows, ["figure_id", "file_path", "figure_status", "priority", "required_output"]),
                "",
                "## Curve Status",
                md_table(curve_rows, ["curve_status_id", "curve_status", "machine_table_candidate", "figure_asset_candidate", "text_threshold_anchor", "next_action"]),
                "",
                "## Kernel Input Contract",
                md_table(kernel_rows, ["kernel_input_id", "required_input", "input_owner", "current_status", "failure_effect"]),
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
    R10.mkdir(parents=True, exist_ok=True)
    acquisition = fetch_archive()
    extraction_status = "NOT_ATTEMPTED"
    extraction_error = ""
    if acquisition["download_status"] == "DOWNLOADED_SOURCE_ARCHIVE_NONCLAIM":
        extraction_status, extraction_error = safe_extract_archive(ARCHIVE_FILE, ARCHIVE_EXTRACT_DIR)
    acquisition["extraction_status"] = extraction_status
    acquisition["extraction_error"] = extraction_error

    manifest = manifest_rows(extraction_status)
    scan_rows = tex_anchor_rows(manifest)
    table_rows = table_hunt_rows(manifest)
    figure_rows = figure_target_rows(manifest)
    curve_rows = curve_status_rows(table_rows, figure_rows, scan_rows)
    kernel_rows = kernel_contract_rows()
    blockers = blocker_rows(curve_rows)
    readiness = score_readiness_rows(blockers)
    c_parent_rows = c_parent_refusal_rows()
    local_rows = local_status_rows(curve_rows)
    rejections = rejection_rows()
    decisions = decision_rows(curve_rows)
    next_rows = next_target_rows(curve_rows)

    write_csv(ARCHIVE_ACQUISITION, [acquisition])
    write_csv(ARCHIVE_MANIFEST, manifest)
    write_csv(TEX_ANCHOR_SCAN, scan_rows)
    write_csv(FIGURE_TARGETS, figure_rows)
    write_csv(MACHINE_TABLE_HUNT, table_rows)
    write_csv(CURVE_STATUS, curve_rows)
    write_csv(KERNEL_CONTRACT, kernel_rows)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        ARCHIVE_ACQUISITION,
        ARCHIVE_MANIFEST,
        TEX_ANCHOR_SCAN,
        FIGURE_TARGETS,
        MACHINE_TABLE_HUNT,
        CURVE_STATUS,
        KERNEL_CONTRACT,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, acquisition, manifest, scan_rows, curve_rows)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(acquisition, manifest, scan_rows, table_rows, figure_rows, curve_rows, kernel_rows, validation, next_rows)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
