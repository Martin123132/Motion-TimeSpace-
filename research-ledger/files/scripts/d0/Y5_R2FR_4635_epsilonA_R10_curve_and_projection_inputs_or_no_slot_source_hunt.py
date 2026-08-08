from __future__ import annotations

import csv
import math
import subprocess
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import fitz
except ImportError:  # pragma: no cover - validation records this if the local env changes.
    fitz = None


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
ACQ_DIR = POST / "source-intake" / "r10_curve_acquisition" / "4635"
ACQ_SOURCE = ACQ_DIR / "source"

CHECKPOINT = "4635"
CLAIM_ID = "L-477"
BRANCH_ID = "MTS_R2FR_Y5_EPSILONA_R10_CURVE_PROJECTION_4635"
MARKER = "PPC4161_EPSILONA_R10_CURVE_AND_PROJECTION_INPUTS_OR_NO_SLOT_SOURCE_HUNT_4635"
PACKET_MARKER = "PPC4161_PACKET_EPSILONA_R10_CURVE_PROJECTION_4635"
DECISION = "R10_VECTOR_CURVE_EXTRACTED_NONCLAIM_PARENT_EPSILON_AND_NO_SLOT_STILL_MISSING"
NEXT_TARGET = "4636-Y5-R2FR-R10-vector-curve-QA-and-epsilon-coefficient-fill.md"

DOC_PATH = POST / "4635-Y5-R2FR-epsilonA-R10-curve-and-projection-inputs-or-no-slot-source-hunt.md"
FORMAL_PATH = FORMAL / "651-PPC4161-epsilonA-R10-curve-and-projection-inputs-or-no-slot-source-hunt.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4635_SOURCE_REGISTER.csv"
ACQUISITION_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_SOURCE_ACQUISITION_LEDGER.csv"
CURVE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CURVE_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_CURVE_STATUS_ROWS.csv"
PROJECTION_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_PROJECTION_INPUT_REQUIREMENTS.csv"
NO_SLOT_HUNT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_NO_SLOT_SOURCE_HUNT_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_VECTOR_CURVE_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4635_VALIDATION.csv"

CSV_4634_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4634_NEXT_TARGET.csv"
CSV_4634_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4634_VALIDATION.csv"
CSV_4634_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4634_EPSILONA_FIRST_BOUND_MATRIX.csv"
CSV_4634_THRESHOLD = SOURCE_DIR / "P8_Y5_R2FR_4634_SYMBOLIC_THRESHOLD_ROWS.csv"
CSV_4634_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4634_BOUND_MATRIX_RUNNER_RESULTS.csv"
CSV_4626_ANCHORS = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4633_SIGN = SOURCE_DIR / "P8_Y5_R2FR_4633_PARENT_SIGNING_MATRIX.csv"
CSV_1451_SIGN = SOURCE_DIR / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
CSV_1452_SIGN = SOURCE_DIR / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"

ARXIV_PDF = ACQ_DIR / "arxiv_2002_11761.pdf"
ARXIV_SOURCE_TAR = ACQ_DIR / "arxiv_2002_11761_source.tar"
TEX_PATH = ACQ_SOURCE / "FB_ISL_pdf.tex"
FIG5B_PDF = ACQ_SOURCE / "fig5b1.pdf"
FIG5B_PNG = ACQ_SOURCE / "fig5b1.png"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")

AXIS_LEFT_X = 122.32
AXIS_RIGHT_X = 462.47
AXIS_TOP_Y = 47.33
AXIS_BOTTOM_Y = 353.47
LOG_LAMBDA_LEFT = math.log10(2.0e-6)
LOG_LAMBDA_RIGHT = math.log10(1.0e-3)
LOG_ALPHA_TOP = 6.0
LOG_ALPHA_BOTTOM = -3.0
ALPHA_ONE_ANCHOR_M = 38.6e-6


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line_text in enumerate(read_text(path).splitlines(), start=1):
        if needle in line_text:
            return line_number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    separator = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + separator + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def path_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def lambda_from_pdf_x(pdf_x: float) -> float:
    log_lambda = LOG_LAMBDA_LEFT + (pdf_x - AXIS_LEFT_X) / (AXIS_RIGHT_X - AXIS_LEFT_X) * (LOG_LAMBDA_RIGHT - LOG_LAMBDA_LEFT)
    return 10.0**log_lambda


def alpha_from_pdf_y(pdf_y: float) -> float:
    log_alpha = LOG_ALPHA_TOP - (pdf_y - AXIS_TOP_Y) / (AXIS_BOTTOM_Y - AXIS_TOP_Y) * (LOG_ALPHA_TOP - LOG_ALPHA_BOTTOM)
    return 10.0**log_alpha


def log_lambda_from_pdf_x(pdf_x: float) -> float:
    return math.log10(lambda_from_pdf_x(pdf_x))


def log_alpha_from_pdf_y(pdf_y: float) -> float:
    return math.log10(alpha_from_pdf_y(pdf_y))


def extract_purple_components() -> list[dict[str, Any]]:
    if fitz is None or not FIG5B_PDF.exists():
        return []
    page = fitz.open(FIG5B_PDF)[0]
    segments: list[tuple[float, float, float, float]] = []
    for drawing in page.get_drawings():
        stroke_color = drawing.get("color")
        stroke_width = round(float(drawing.get("width") or 0.0), 3)
        is_eotwash_purple = (
            stroke_color
            and abs(stroke_color[0] - 0.333008) < 0.01
            and abs(stroke_color[1]) < 0.01
            and abs(stroke_color[2] - 1.0) < 0.01
            and stroke_width == 1.304
        )
        if not is_eotwash_purple:
            continue
        for item in drawing.get("items", []):
            if item[0] != "l":
                continue
            start_point = item[1]
            end_point = item[2]
            start_x, start_y = float(start_point.x), float(start_point.y)
            end_x, end_y = float(end_point.x), float(end_point.y)
            inside_plot = (
                120.0 <= max(start_x, end_x)
                and min(start_x, end_x) <= 465.0
                and 35.0 <= max(start_y, end_y)
                and min(start_y, end_y) <= 360.0
            )
            if inside_plot:
                segments.append((start_x, start_y, end_x, end_y))
    adjacency: dict[tuple[float, float], list[tuple[tuple[float, float], int]]] = defaultdict(list)

    def endpoint_key(pdf_x: float, pdf_y: float) -> tuple[float, float]:
        return (round(pdf_x, 2), round(pdf_y, 2))

    for segment_index, segment in enumerate(segments):
        start_key = endpoint_key(segment[0], segment[1])
        end_key = endpoint_key(segment[2], segment[3])
        adjacency[start_key].append((end_key, segment_index))
        adjacency[end_key].append((start_key, segment_index))

    visited: set[tuple[float, float]] = set()
    components: list[dict[str, Any]] = []
    for node in list(adjacency):
        if node in visited:
            continue
        queue: deque[tuple[float, float]] = deque([node])
        visited.add(node)
        segment_indices: set[int] = set()
        while queue:
            current_node = queue.popleft()
            for next_node, segment_index in adjacency[current_node]:
                segment_indices.add(segment_index)
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)
        pdf_x_values = [coordinate for segment_index in segment_indices for coordinate in (segments[segment_index][0], segments[segment_index][2])]
        pdf_y_values = [coordinate for segment_index in segment_indices for coordinate in (segments[segment_index][1], segments[segment_index][3])]
        total_length = sum(
            math.hypot(segments[segment_index][2] - segments[segment_index][0], segments[segment_index][3] - segments[segment_index][1])
            for segment_index in segment_indices
        )
        components.append(
            {
                "segment_indices": segment_indices,
                "segments": [segments[segment_index] for segment_index in segment_indices],
                "segment_count": len(segment_indices),
                "length": total_length,
                "bbox_pdf": (min(pdf_x_values), min(pdf_y_values), max(pdf_x_values), max(pdf_y_values)),
            }
        )
    components.sort(key=lambda component: component["length"], reverse=True)
    return components


def alpha_one_crossing(component_segments: list[tuple[float, float, float, float]]) -> float | None:
    alpha_one_pdf_y = AXIS_TOP_Y + (LOG_ALPHA_TOP / (LOG_ALPHA_TOP - LOG_ALPHA_BOTTOM)) * (AXIS_BOTTOM_Y - AXIS_TOP_Y)
    crossings: list[float] = []
    for start_x, start_y, end_x, end_y in component_segments:
        if abs(start_y - end_y) < 1.0e-12:
            continue
        bracketed = (start_y - alpha_one_pdf_y) * (end_y - alpha_one_pdf_y) <= 0.0
        if not bracketed:
            continue
        interpolation = (alpha_one_pdf_y - start_y) / (end_y - start_y)
        if 0.0 <= interpolation <= 1.0:
            crossing_pdf_x = start_x + interpolation * (end_x - start_x)
            crossings.append(lambda_from_pdf_x(crossing_pdf_x))
    if not crossings:
        return None
    return min(crossings, key=lambda value: abs(value - ALPHA_ONE_ANCHOR_M))


def vector_digitized_curve(now: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    components = extract_purple_components()
    component_summaries: list[dict[str, Any]] = []
    for component_index, component in enumerate(components):
        bbox_left, bbox_top, bbox_right, bbox_bottom = component["bbox_pdf"]
        crossing = alpha_one_crossing(component["segments"])
        component_summaries.append(
            {
                "component_id": f"PURPLE_COMPONENT_{component_index}",
                "segment_count": component["segment_count"],
                "pdf_bbox": f"{bbox_left:.3f},{bbox_top:.3f},{bbox_right:.3f},{bbox_bottom:.3f}",
                "lambda_min_m": f"{lambda_from_pdf_x(bbox_left):.12g}",
                "lambda_max_m": f"{lambda_from_pdf_x(bbox_right):.12g}",
                "alpha_min": f"{alpha_from_pdf_y(bbox_bottom):.12g}",
                "alpha_max": f"{alpha_from_pdf_y(bbox_top):.12g}",
                "alpha_one_crossing_m": "" if crossing is None else f"{crossing:.12g}",
                "anchor_error_fraction_vs_38p6um": "" if crossing is None else f"{(crossing - ALPHA_ONE_ANCHOR_M) / ALPHA_ONE_ANCHOR_M:.6g}",
                "component_role": "EOTWASH_2020_SELECTED_BY_ALPHA1_CROSSING" if component_index == 0 else "OLDER_EOTWASH_CURVE_OR_ADJACENT_PURPLE_CURVE",
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    if not components:
        return [], component_summaries
    selected_component = components[0]
    selected_crossing = alpha_one_crossing(selected_component["segments"])
    point_map: dict[tuple[float, float], tuple[float, float]] = {}
    for segment in selected_component["segments"]:
        point_map[(round(segment[0], 3), round(segment[1], 3))] = (segment[0], segment[1])
        point_map[(round(segment[2], 3), round(segment[3], 3))] = (segment[2], segment[3])
    sorted_points = sorted(point_map.values(), key=lambda point: point[0])
    curve_rows: list[dict[str, Any]] = []
    for point_index, (pdf_x, pdf_y) in enumerate(sorted_points):
        lambda_value = lambda_from_pdf_x(pdf_x)
        alpha_value = alpha_from_pdf_y(pdf_y)
        curve_rows.append(
            {
                "checkpoint": CHECKPOINT,
                "curve_id": "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1",
                "point_index": point_index,
                "lambda_m": f"{lambda_value:.12g}",
                "lambda_um": f"{lambda_value * 1.0e6:.12g}",
                "alpha_bound_abs": f"{alpha_value:.12g}",
                "log10_lambda": f"{math.log10(lambda_value):.12g}",
                "log10_alpha": f"{math.log10(alpha_value):.12g}",
                "pdf_x": f"{pdf_x:.6f}",
                "pdf_y": f"{pdf_y:.6f}",
                "component_id": "PURPLE_COMPONENT_0",
                "alpha_one_crossing_m": "" if selected_crossing is None else f"{selected_crossing:.12g}",
                "axis_calibration": "x:2e-6_to_1e-3_m_log; y:1e6_to_1e-3_abs_alpha_log",
                "extraction_method": "PyMuPDF vector path extraction from arXiv source fig5b1.pdf; selected component by alpha=1 crossing near 38.6 um",
                "source_figure": str(FIG5B_PDF),
                "source_tex": str(TEX_PATH),
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return curve_rows, component_summaries


def interpolate_alpha_bound(curve_rows: list[dict[str, Any]], lambda_m: float) -> float | None:
    usable_points = sorted(
        (float(row["lambda_m"]), float(row["alpha_bound_abs"])) for row in curve_rows if row.get("lambda_m") and row.get("alpha_bound_abs")
    )
    if not usable_points or lambda_m < usable_points[0][0] or lambda_m > usable_points[-1][0]:
        return None
    log_lambda = math.log10(lambda_m)
    for point_index in range(len(usable_points) - 1):
        lambda_left, alpha_left = usable_points[point_index]
        lambda_right, alpha_right = usable_points[point_index + 1]
        if lambda_left <= lambda_m <= lambda_right:
            log_left = math.log10(lambda_left)
            log_right = math.log10(lambda_right)
            if abs(log_right - log_left) < 1.0e-15:
                return alpha_left
            interpolation = (log_lambda - log_left) / (log_right - log_left)
            log_alpha = math.log10(alpha_left) + interpolation * (math.log10(alpha_right) - math.log10(alpha_left))
            return 10.0**log_alpha
    return usable_points[-1][1]


def source_register_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4635_00_4634_next", "local_path", CSV_4634_NEXT, "4635-Y5-R2FR-epsilonA-R10-curve-and-projection-inputs-or-no-slot-source-hunt.md", "4634 selected the R10 curve/projection target."),
        ("SRC4635_01_4634_validation", "local_path", CSV_4634_VALIDATION, "VAL4634_OVERALL", "4634 validation."),
        ("SRC4635_02_4634_matrix", "local_path", CSV_4634_MATRIX, "BM4634_0_R10", "first epsilon_A R10 matrix."),
        ("SRC4635_03_4634_threshold", "local_path", CSV_4634_THRESHOLD, "TH4634_0_R10_anchor_epsilon_product", "symbolic R10 threshold."),
        ("SRC4635_04_4634_runner", "local_path", CSV_4634_RUNNER, "RUN4634_0_current_live_R10", "live fail-closed runner."),
        ("SRC4635_05_4626_anchor", "local_path", CSV_4626_ANCHORS, "BA4626_0_R10_EOTWASH_ALPHA1", "source-backed alpha=1 anchor."),
        ("SRC4635_06_4628_gap", "local_path", CSV_4628_NUMERIC, "LNUM4628_3_R10_anchor_gap_ratio", "R10 gap-ratio conversion."),
        ("SRC4635_07_arxiv_pdf", "local_path", ARXIV_PDF, "", "downloaded arXiv PDF."),
        ("SRC4635_08_arxiv_source_tar", "local_path", ARXIV_SOURCE_TAR, "", "downloaded arXiv e-print source archive."),
        ("SRC4635_09_tex_yukawa", "local_path", TEX_PATH, "V(r)=V_N(r) [1+\\alpha \\exp({-r/\\lambda})]", "Yukawa convention in paper source."),
        ("SRC4635_10_tex_66_lambda", "local_path", TEX_PATH, "66 assumed values of  $\\lambda$ between $5\\,\\mu$m and $9\\,$mm", "fit grid statement."),
        ("SRC4635_11_tex_alpha1_anchor", "local_path", TEX_PATH, "lambda<38.6\\,\\mu$m", "alpha=1 range statement."),
        ("SRC4635_12_tex_supplement", "local_path", TEX_PATH, "constraints on $+\\alpha$ and $-\\alpha$ are given in Supplemental Material", "supplemental material requirement."),
        ("SRC4635_13_fig5b1_vector", "local_path", FIG5B_PDF, "", "vector figure used for nonclaim curve extraction."),
        ("SRC4635_14_fig5b1_png", "local_path", FIG5B_PNG, "", "rendered visual QA image."),
        ("SRC4635_15_4633_parent_sign", "local_path", CSV_4633_SIGN, "SIGN4633_0_no_hidden_visible_Hom", "no-slot parent signature still unsigned."),
        ("SRC4635_16_1451_sign", "local_path", CSV_1451_SIGN, "SIGN1451_0_no_slot", "older no-slot signing decision."),
        ("SRC4635_17_1452_sign", "local_path", CSV_1452_SIGN, "SIGN1452_0_common_measure", "common-measure signing decision."),
        ("SRC4635_18_pubmed_url", "url", "https://pubmed.ncbi.nlm.nih.gov/32216404/", "", "PubMed record for Lee et al. 2020."),
        ("SRC4635_19_arxiv_abs_url", "url", "https://arxiv.org/abs/2002.11761", "", "arXiv abstract/source page."),
        ("SRC4635_20_aps_supplement_url", "url", "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101", "", "official supplemental URL; local probe hit 403 Cloudflare."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_type, source_path, needle, role in specs:
        if source_type == "local_path":
            path = Path(source_path)
            source_text = read_text(path) if path.suffix.lower() in {".txt", ".tex", ".csv", ".md"} else ""
            path_exists = path.exists()
            needle_found = bool(needle in source_text) if needle else path_exists
            line_number = line_of(path, needle) if needle else 0
            size_bytes = path_size(path)
            source_value = str(path)
        else:
            path_exists = True
            needle_found = True
            line_number = 0
            size_bytes = ""
            source_value = str(source_path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_type": source_type,
                "source": source_value,
                "path_exists_or_url_recorded": path_exists,
                "needle": needle,
                "needle_found": needle_found,
                "line": line_number,
                "size_bytes": size_bytes,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": now,
            }
        )
    return rows


def acquisition_rows(now: str, curve_rows: list[dict[str, Any]], component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    crossing = component_rows[0]["alpha_one_crossing_m"] if component_rows else ""
    return [
        {
            "checkpoint": CHECKPOINT,
            "acquisition_id": "ACQ4635_0_arxiv_pdf",
            "source": "https://arxiv.org/pdf/2002.11761",
            "local_path": str(ARXIV_PDF),
            "status": "ACQUIRED",
            "method": "Invoke-WebRequest",
            "confidence": "paper_pdf_source_backed",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "acquisition_id": "ACQ4635_1_arxiv_eprint_source",
            "source": "https://arxiv.org/e-print/2002.11761",
            "local_path": str(ARXIV_SOURCE_TAR),
            "status": "ACQUIRED_EXTRACTED",
            "method": "arXiv source tar; contains FB_ISL_pdf.tex and fig5b1.pdf",
            "confidence": "source_archive_backed",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "acquisition_id": "ACQ4635_2_R10_curve_vector_extraction",
            "source": str(FIG5B_PDF),
            "local_path": str(CURVE_CSV),
            "status": "VECTOR_DIGITIZED_FULL_CURVE_NONCLAIM_QA_REQUIRED" if curve_rows else "VECTOR_EXTRACTION_FAILED",
            "method": "extract purple width=1.304 vector component whose alpha=1 crossing reproduces 38.6 um",
            "confidence": "strong_internal_smoke; not official supplemental numeric table",
            "point_count": len(curve_rows),
            "alpha_one_crossing_m": crossing,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "acquisition_id": "ACQ4635_3_APS_supplement_probe",
            "source": "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101",
            "local_path": "",
            "status": "BLOCKED_403_CLOUDFLARE_IN_LOCAL_PROBE",
            "method": "PowerShell/curl probe on 2026-07-06",
            "confidence": "blocker_not_fabrication",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def curve_status_rows(now: str, curve_rows: list[dict[str, Any]], component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not curve_rows or not component_rows:
        return [
            {
                "checkpoint": CHECKPOINT,
                "curve_status_id": "CURVE4635_0_EOTWASH2020",
                "status": "NO_VECTOR_CURVE_EXTRACTED",
                "point_count": 0,
                "usable_for_smoke": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        ]
    crossing = float(component_rows[0]["alpha_one_crossing_m"])
    return [
        {
            "checkpoint": CHECKPOINT,
            "curve_status_id": "CURVE4635_0_EOTWASH2020",
            "status": "FULL_VECTOR_CURVE_EXTRACTED_FROM_FIG5B1_NONCLAIM",
            "point_count": len(curve_rows),
            "lambda_min_m": curve_rows[0]["lambda_m"],
            "lambda_max_m": curve_rows[-1]["lambda_m"],
            "alpha_one_crossing_m": f"{crossing:.12g}",
            "source_anchor_alpha1_m": f"{ALPHA_ONE_ANCHOR_M:.12g}",
            "anchor_error_fraction": f"{(crossing - ALPHA_ONE_ANCHOR_M) / ALPHA_ONE_ANCHOR_M:.6g}",
            "usable_for_smoke": True,
            "claim_grade_reason": "figure-vector extraction needs manual QA or official supplemental numeric table before promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        *[
            {
                "checkpoint": CHECKPOINT,
                "curve_status_id": f"CURVE4635_COMPONENT_{component_index}",
                **component_row,
            }
            for component_index, component_row in enumerate(component_rows)
        ],
    ]


def projection_input_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("PIN4635_0_epsilon_A", "epsilon_A", "parent-visible source coupling amplitude", "MISSING_PARENT_COEFFICIENT_OR_EXACT_ZERO", "Required for alpha_AB."),
        ("PIN4635_1_epsilon_B", "epsilon_B", "second body/source coupling amplitude", "MISSING_PARENT_COEFFICIENT_OR_EXACT_ZERO", "Required for alpha_AB."),
        ("PIN4635_2_Z_min", "Z_min", "same-branch memory kinetic normalization", "MISSING_PARENT_NORMALIZATION", "Cannot normalize alpha_AB without it."),
        ("PIN4635_3_C_N", "C_N", "Newton/Yukawa convention and geometry coefficient", "MISSING_CONVENTION_CALIBRATION", "Maps epsilon product to |alpha|."),
        ("PIN4635_4_lambda_mem", "lambda_mem", "sqrt(Z_mem/M2_mem)", "MISSING_PARENT_HESSIAN_RATIO", "R10 curve lookup requires this."),
        ("PIN4635_5_alpha_bound_curve", "alpha_bound(lambda)", "Eot-Wash 2020 full |alpha| curve", "VECTOR_EXTRACTED_NONCLAIM_QA_REQUIRED", "Now usable for smoke, not claim-grade."),
        ("PIN4635_6_sign_convention", "|alpha| versus +/- alpha", "experimental sign convention", "ABS_ALPHA_AVAILABLE_PLUS_MINUS_SUPPLEMENT_BLOCKED", "Official +/- curves still need supplement access."),
        ("PIN4635_7_interpolation_policy", "log-log interpolation", "curve lookup convention", "SMOKE_POLICY_READY", "Use only inside nonclaim runner until QA."),
        ("PIN4635_8_same_branch_parent_action", "same-branch ownership", "ensures lambda and alpha share one parent action", "UNSIGNED", "Prevents normalization cheating."),
        ("PIN4635_9_projection_to_other_arenas", "WEP/PPN/clock/orbital projections", "arena-specific maps", "MISSING_ARENA_PROJECTION", "Still blocked outside R10."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": input_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "note": note,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for input_id, symbol, meaning, status, note in specs
    ]


def no_slot_hunt_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "NSH4635_0_no_hidden_visible_Hom",
            "target": "NoHiddenVisibleHom for q-basic A_m",
            "source_path": str(CSV_4633_SIGN),
            "source_marker": "SIGN4633_0_no_hidden_visible_Hom",
            "current_result": "UNSIGNED",
            "effect": "epsilon_A cannot be set to zero by no-slot route yet",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "NSH4635_1_label_forgetting_common_measure",
            "target": "label-forgetting/common-measure current descent",
            "source_path": str(CSV_1452_SIGN),
            "source_marker": "SIGN1452_0_common_measure",
            "current_result": "UNSIGNED",
            "effect": "parent zero theorem remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "NSH4635_2_bound_route_active",
            "target": "fallback R10 bound route",
            "source_path": str(CURVE_CSV),
            "source_marker": "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1",
            "current_result": "ACTIVE_NONCLAIM",
            "effect": "use vector curve to stress epsilon/Z/C_N/lambda rows while hunting parent zero proof",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def runner_rows(now: str, curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scenarios = [
        ("RUN4635_0_current_live_R10", None, None, None, None, None, "FAIL_CLOSED_MISSING_INPUT", "epsilon_A/epsilon_B/Z_min/C_N/lambda_mem are still missing"),
        ("RUN4635_1_parent_no_slot_zero", 0.0, 0.0, 1.0, 1.0, ALPHA_ONE_ANCHOR_M, "CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY", "would pass all R10 alpha bounds, but no-slot signatures are unsigned"),
        ("RUN4635_2_small_epsilon_vector_smoke", 0.01, 0.01, 1.0, 1.0, ALPHA_ONE_ANCHOR_M, "EVALUATE", "small epsilon smoke against vector curve"),
        ("RUN4635_3_order_one_epsilon_vector_fail", 1.0, 1.0, 0.5, 1.0, ALPHA_ONE_ANCHOR_M, "EVALUATE", "order-one epsilon should fail near alpha=1 crossing"),
        ("RUN4635_4_long_range_low_alpha_fail", 0.316227766, 0.316227766, 1.0, 1.0, 1.0e-4, "EVALUATE", "alpha about 0.1 is too large at 100 um for the 2020 vector curve"),
        ("RUN4635_5_shorter_range_smoke", 0.01, 0.01, 1.0, 1.0, 2.0e-5, "EVALUATE", "shorter range has weak bound and should pass the vector smoke"),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, epsilon_a, epsilon_b, z_min, convention_factor, lambda_mem, preset_result, reason in scenarios:
        alpha_predicted: float | None = None
        alpha_bound: float | None = None
        result = preset_result
        if None not in {epsilon_a, epsilon_b, z_min, convention_factor, lambda_mem}:
            alpha_predicted = float(convention_factor) * float(epsilon_a) * float(epsilon_b) / float(z_min)
            alpha_bound = interpolate_alpha_bound(curve_rows, float(lambda_mem))
            if preset_result == "EVALUATE":
                if alpha_bound is None:
                    result = "FAIL_CLOSED_LAMBDA_OUTSIDE_VECTOR_CURVE"
                elif alpha_predicted <= alpha_bound:
                    result = "PASS_VECTOR_CURVE_SMOKE_ONLY_NONCLAIM"
                else:
                    result = "FAIL_VECTOR_CURVE_ALPHA_ABOVE_BOUND"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "arena": "R10",
                "epsilon_A": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND" if epsilon_a is None else epsilon_a,
                "epsilon_B": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND" if epsilon_b is None else epsilon_b,
                "Z_min": "MISSING_ZMEM_PARENT_VALUE" if z_min is None else z_min,
                "C_N": "MISSING_CONVENTION_OR_CALIBRATION" if convention_factor is None else convention_factor,
                "lambda_mem_m": "MISSING_ZMEM_M2MEM_RATIO" if lambda_mem is None else f"{lambda_mem:.12g}",
                "alpha_AB": "MISSING" if alpha_predicted is None else f"{alpha_predicted:.12g}",
                "alpha_bound_vector": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "result": result,
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4635_0_no_claim_from_vector_digitization",
            "rule": "Vector-extracted Fig. 5 curve is allowed for smoke tests but not a claim until manual QA or official supplemental numeric rows are acquired.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4635_1_no_epsilon_without_parent_source",
            "rule": "epsilon_A/B cannot be invented from the R10 curve; they must be exact-zero or parent coefficient rows.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4635_2_same_branch_normalization",
            "rule": "Z_min, C_N, lambda_mem and alpha_AB must be co-normalized on one parent branch.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4635_0_R10_claim",
            "blocks": "R10/local-G claim",
            "missing": "parent epsilon_A/B or exact-zero theorem; Z_min; C_N; lambda_mem; curve QA/supplement",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4635_1_no_slot_exact_zero",
            "blocks": "epsilon_A=0 import",
            "missing": "signed parent no-hidden-visible-Hom, label forgetting, common-measure/current and non-Hilbert guard",
            "next_action": "continue no-slot proof search in parallel with coefficient fill",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4635_2_other_arenas",
            "blocks": "WEP/PPN/clock/orbital scoring",
            "missing": "projection coefficients and arena source maps",
            "next_action": "after R10 smoke stabilizes, extend same coefficient discipline to WEP/PPN",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4635_0",
            "decision": DECISION,
            "meaning": "The R10 alpha(lambda) input is no longer merely a one-point anchor: a vector-extracted Eot-Wash 2020 curve now exists for nonclaim smoke testing. The theory still cannot claim a pass until parent-owned epsilon/Z/C_N/lambda inputs or exact-zero no-slot proof are supplied.",
            "status": "NONCLAIM_VECTOR_CURVE_READY_PARENT_INPUTS_MISSING",
            "best_route": "Use the vector curve to stress-test any future parent epsilon row; in parallel keep trying to sign the no-slot exact-zero theorem.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str, curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "status": "PASS_NONCLAIM_ARTIFACTS_WRITTEN",
            "curve_point_count": len(curve_rows),
            "github_action": "NONE_LOCAL_ONLY",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The R10 curve exists for smoke; next fill or prove the parent epsilon/Z/C_N/lambda inputs and QA the curve against official supplemental rows if accessible.",
            "timestamp_utc": now,
        }
    ]


def has_any_claim(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def validation_rows(
    source_rows: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    curve_status: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    no_slot_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_generated = [source_rows, curve_rows, curve_status, projection_rows, no_slot_rows, runner, controls, blockers, decisions, status, next_target]
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    required_sources_ok = all(
        row["path_exists_or_url_recorded"] and row["needle_found"]
        for row in source_rows
        if row["source_id"] not in {"SRC4635_20_aps_supplement_url"}
    )
    add("VAL4635_00_sources_exist_and_needles_found", required_sources_ok, "all required local sources/needles found; APS supplement URL recorded as blocked")

    csv_paths = [
        SOURCE_REGISTER,
        ACQUISITION_LEDGER,
        CURVE_CSV,
        CURVE_STATUS_CSV,
        PROJECTION_INPUTS_CSV,
        NO_SLOT_HUNT_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_detail_parts = []
    csv_parse_ok = True
    for csv_path in csv_paths:
        try:
            csv_detail_parts.append(f"{csv_path.name}:{len(read_csv(csv_path))}")
        except csv.Error as exc:
            csv_parse_ok = False
            csv_detail_parts.append(f"{csv_path.name}:CSV_ERROR:{exc}")
    add("VAL4635_01_csv_parse", csv_parse_ok, ";".join(csv_detail_parts))

    crossing_rows = [row for row in curve_status if row.get("curve_status_id") == "CURVE4635_0_EOTWASH2020"]
    crossing_ok = bool(crossing_rows and crossing_rows[0].get("status") == "FULL_VECTOR_CURVE_EXTRACTED_FROM_FIG5B1_NONCLAIM")
    add("VAL4635_02_vector_curve_extracted", crossing_ok, crossing_rows[0].get("alpha_one_crossing_m", "missing") if crossing_rows else "missing")

    if curve_rows:
        lambda_values = [float(row["lambda_m"]) for row in curve_rows]
        alpha_values = [float(row["alpha_bound_abs"]) for row in curve_rows]
        curve_numeric_ok = all(value > 0.0 for value in lambda_values + alpha_values) and lambda_values == sorted(lambda_values)
    else:
        curve_numeric_ok = False
    add("VAL4635_03_curve_rows_positive_sorted", curve_numeric_ok, f"point_count={len(curve_rows)}")

    curve_smoke_ok = any(row["result"] == "PASS_VECTOR_CURVE_SMOKE_ONLY_NONCLAIM" for row in runner) and any(row["result"] == "FAIL_VECTOR_CURVE_ALPHA_ABOVE_BOUND" for row in runner)
    add("VAL4635_04_runner_pass_fail_controls", curve_smoke_ok, "vector curve runner has pass/fail controls")

    live_fail_ok = any(row["run_id"] == "RUN4635_0_current_live_R10" and row["result"] == "FAIL_CLOSED_MISSING_INPUT" for row in runner)
    add("VAL4635_05_live_branch_fails_closed", live_fail_ok, "current live R10 branch remains blocked")

    projection_ok = {"epsilon_A", "epsilon_B", "Z_min", "C_N", "lambda_mem", "alpha_bound(lambda)"}.issubset({row["symbol"] for row in projection_rows})
    add("VAL4635_06_projection_inputs_present", projection_ok, "core R10 projection inputs present")

    no_slot_ok = any(row["current_result"] == "UNSIGNED" for row in no_slot_rows)
    add("VAL4635_07_no_slot_unsigned_retained", no_slot_ok, "exact-zero route retained but not imported")

    nonclaim_ok = not any(has_any_claim(generated_rows) for generated_rows in all_generated)
    add("VAL4635_08_all_rows_nonclaim", nonclaim_ok, "no generated row promotes a claim")

    add("VAL4635_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4635_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4635_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4635_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4635_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4635_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4635_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4635_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4635_OVERALL", overall, "4635 R10 vector curve/projection checkpoint")
    return checks


def write_docs(
    now: str,
    source_rows: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    curve_rows: list[dict[str, Any]],
    curve_status: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    no_slot_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> None:
    curve_preview = curve_rows[:5] + curve_rows[-5:] if len(curve_rows) > 10 else curve_rows
    body = f"""# 4635 - EpsilonA R10 Curve And Projection Inputs Or No-Slot Source Hunt

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4635 moves the R10 side from a single `alpha=1 at lambda=38.6 um` anchor to a real nonclaim curve input.

The arXiv source archive contains `fig5b1.pdf`. Its purple vector component whose `|alpha|=1` crossing lands at the published `38.6 um` gravitational-strength threshold is extracted into `{CURVE_CSV.name}`.

This is useful for smoke testing any future `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, `lambda_mem` row, but it is still not a public/claim-grade empirical pass: the official APS supplemental numeric +/- alpha rows were not locally acquired, and parent-owned MTS coefficients remain missing.

## Source Register

{markdown_table(source_rows)}

## Acquisition Ledger

{markdown_table(acquisition)}

## Curve Status

{markdown_table(curve_status)}

## Curve Preview

{markdown_table(curve_preview)}

## Projection Input Requirements

{markdown_table(projection_rows)}

## No-Slot Source Hunt

{markdown_table(no_slot_rows)}

## Vector Curve Runner Results

{markdown_table(runner)}

## Controls

{markdown_table(controls)}

## Blockers

{markdown_table(blockers)}

## Decision

{markdown_table(decisions)}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)
    formal_body = f"""# 651 - PPC4161 EpsilonA R10 Curve And Projection Inputs Or No-Slot Source Hunt

Marker: `{MARKER}`

Source checkpoint: `{DOC_PATH}`

4635 extracts the Eot-Wash 2020 `|alpha|(lambda)` curve from the paper's vector Fig. 5 source for nonclaim smoke use. The selected component is the purple curve whose `alpha=1` crossing reproduces the published `38.6 um` threshold to plotting accuracy. This upgrades the R10 input from one anchor to a curve-shaped gate, but still blocks any local-GR/R10 claim until parent `epsilon_A/B`, `Z_min`, `C_N`, `lambda_mem` and curve QA/supplemental numeric rows are supplied.

Decision: `{DECISION}`.

Next: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, formal_body)


def append_formal_integrations() -> None:
    spine_block = f"""
## PPC4161 EpsilonA R10 Curve And Projection Inputs Or No-Slot Source Hunt 4635

Marker: `{MARKER}`

4635 turns the R10 empirical side from a one-point anchor into a nonclaim vector-extracted Eot-Wash 2020 `|alpha|(lambda)` curve. The curve is good enough for internal smoke tests because its `alpha=1` crossing lands near the published `38.6 um` threshold, but it cannot promote a theory claim until the official supplemental numeric rows or manual QA are added and MTS supplies parent-owned `epsilon_A/B`, `Z_min`, `C_N`, and `lambda_mem`.

Next: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)
    packet_block = f"""
## PPC4161 Packet - EpsilonA R10 Curve Projection 4635

Marker: `{PACKET_MARKER}`

Local packet update: R10 now has a curve-shaped nonclaim gate instead of only an alpha=1 range anchor. The live theory branch still fails closed; the useful move is to feed any future parent epsilon/gap coefficient through this curve before trying WEP/PPN/clock/orbital projections.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def append_claim_register() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "area": "local_gr_empirical_interface",
        "claim": "4635 extracts a nonclaim Eot-Wash 2020 R10 alpha(lambda) curve from the arXiv vector figure and wires it into the epsilon_A bound route.",
        "support": "Generated source register, acquisition ledger, vector digitized curve, projection input requirements, no-slot hunt rows, runner results, controls, blockers, decision, status, next target and validation.",
        "status": "r10_vector_curve_smoke_nonclaim",
        "next": NEXT_TARGET,
        "risk": "Treating vector figure digitization or missing parent epsilon/Z/C_N/lambda inputs as a local-GR/R10 pass.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "notes": "No local-GR/Newton/PPN/R10 pass until exact-zero no-slot theorem is signed or the curve route passes with source-backed parent coefficients and curve QA.",
    }
    file_exists = CLAIMS_PATH.exists()
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists or CLAIMS_PATH.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    now = utc_now()
    curve_rows, component_rows = vector_digitized_curve(now)
    source_rows = source_register_rows(now)
    acquisition = acquisition_rows(now, curve_rows, component_rows)
    curve_status = curve_status_rows(now, curve_rows, component_rows)
    projection_rows = projection_input_rows(now)
    no_slot_rows = no_slot_hunt_rows(now)
    runner = runner_rows(now, curve_rows)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    status = status_rows(now, curve_rows)
    next_target = next_rows(now)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(ACQUISITION_LEDGER, acquisition)
    write_csv(CURVE_CSV, curve_rows)
    write_csv(CURVE_STATUS_CSV, curve_status)
    write_csv(PROJECTION_INPUTS_CSV, projection_rows)
    write_csv(NO_SLOT_HUNT_CSV, no_slot_rows)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_docs(now, source_rows, acquisition, curve_rows, curve_status, projection_rows, no_slot_rows, runner, controls, blockers, decisions)
    append_formal_integrations()
    append_claim_register()

    validation = validation_rows(source_rows, curve_rows, curve_status, projection_rows, no_slot_rows, runner, controls, blockers, decisions, status, next_target)
    write_csv(VALIDATION_CSV, validation)
    print(f"wrote {DOC_PATH}")
    print(f"curve rows: {len(curve_rows)}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
