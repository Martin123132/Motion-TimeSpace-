from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw
from pypdf import PdfReader


CHECKPOINT = "2704"
BRANCH_ID = "Y5_R2FR_APS_SUPPLEMENT_RETRIEVAL_OR_QLOC_PARENT_PROFILE_DERIVATION_2704"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
CACHE_2703 = LOCAL_BOUNDS / "r10_source_cache_2703"
CACHE_2704 = LOCAL_BOUNDS / "r10_source_cache_2704"

DOC_PATH = ROOT / "2704-Y5-R2FR-APS-supplement-retrieval-or-q-loc-parent-profile-derivation.md"
FIG5_PATH = CACHE_2703 / "arxiv_eprint_2002_11761_unpacked" / "fig5b1.pdf"
SUPPLEMENT_ATTEMPTS_PATH = CACHE_2704 / "supplement_retrieval_attempts_2704.json"
VECTOR_RENDER_PATH = CACHE_2704 / "fig5b1_vector_render_probe_2704.png"
VECTOR_PROBE_PATH = CACHE_2704 / "fig5b1_vector_probe_2704.json"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2704_SOURCE_REGISTER.csv",
    "supplement_retrieval": RESIDUALS / "P8_Y5_R2FR_2704_SUPPLEMENT_RETRIEVAL_ATTEMPTS.csv",
    "axis_calibration": RESIDUALS / "P8_Y5_R2FR_2704_FIG5_AXIS_CALIBRATION_NONCLAIM.csv",
    "vector_probe": RESIDUALS / "P8_Y5_R2FR_2704_FIG5_VECTOR_PROBE.csv",
    "curve_candidates": RESIDUALS / "P8_Y5_R2FR_2704_VECTOR_CURVE_CANDIDATES.csv",
    "candidate_samples": RESIDUALS / "P8_Y5_R2FR_2704_EOTWASH2020_VECTOR_CANDIDATE_SAMPLES_NONCLAIM.csv",
    "qloc_derivation": RESIDUALS / "P8_Y5_R2FR_2704_QLOC_PARENT_PROFILE_DERIVATION_CONTRACT.csv",
    "blocker_ledger": RESIDUALS / "P8_Y5_R2FR_2704_BLOCKER_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2704_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2704_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2704_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2704_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2704_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_supplement_attempts": LOCAL_BOUNDS / "R10_APS_SUPPLEMENT_RETRIEVAL_ATTEMPTS_2704.csv",
    "local_axis_calibration": LOCAL_BOUNDS / "R10_FIG5_AXIS_CALIBRATION_2704_NONCLAIM.csv",
    "local_vector_candidates": LOCAL_BOUNDS / "R10_FIG5_VECTOR_CURVE_CANDIDATES_2704_NONCLAIM.csv",
    "local_candidate_samples": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_CANDIDATE_2704_NONCLAIM.csv",
    "wep_qloc_derivation": WEP_RESIDUALS / "q_loc_parent_profile_derivation_contract_2704_NONCLAIM.csv",
    "source_weight_qloc_derivation": SOURCE_WEIGHT / "QLOC_PARENT_PROFILE_DERIVATION_CONTRACT_2704_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2704_QLOC_KERNEL_COEFFICIENTS_OR_SUPPLEMENT_INGEST_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2704_2703_NEXT",
        "relative_path": "2703-Y5-R2FR-R10-bound-curve-digitization-dryrun-or-q-loc-profile-source-hunt.md",
        "required_needles": ["NEXT2703_0_selected", "BDRY2703_3_aps_supplement", "QH2703_5_verdict", "VAL2703_OVERALL"],
        "purpose": "imports the selected 2704 supplement/profile target",
    },
    {
        "source_id": "SRC2704_2699_WARD",
        "relative_path": "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
        "required_needles": ["WID2699_0_definition", "QLOC2699_0_q_loc_vector", "APQ2699_1_R10", "VAL2699_OVERALL"],
        "purpose": "imports exact q_loc Ward-divergence contract",
    },
    {
        "source_id": "SRC2704_2701_ALPHA_OPERATOR",
        "relative_path": "2701-Y5-R2FR-q-loc-PPN-kernel-or-R10-alpha-response-operator-fill.md",
        "required_needles": ["R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE", "MISS2701_0_q_loc_profile", "VAL2701_OVERALL"],
        "purpose": "imports q_loc-to-alpha(lambda) response operator",
    },
    {
        "source_id": "SRC2704_2702_PROFILE_SCHEMA",
        "relative_path": "2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md",
        "required_needles": ["QPROF2702_0_required_prediction_row", "NEXT2702_0_selected", "VAL2702_OVERALL"],
        "purpose": "imports q_loc R10 profile schema",
    },
    {
        "source_id": "SRC2704_SUPPLEMENT_ATTEMPTS",
        "relative_path": "source-intake/local_bounds/r10_source_cache_2704/supplement_retrieval_attempts_2704.json",
        "required_needles": ["link_aps_supplement", "journals_aps_supp_pdf_guess_1", "HTTP Error 403"],
        "purpose": "imports 2704 APS supplement retrieval attempts",
    },
    {
        "source_id": "SRC2704_FIG5_PDF",
        "relative_path": "source-intake/local_bounds/r10_source_cache_2703/arxiv_eprint_2002_11761_unpacked/fig5b1.pdf",
        "required_needles": ["%PDF"],
        "purpose": "imports cached arXiv Fig. 5 bottom plot vector PDF",
        "binary_prefix": True,
    },
]

AXIS_CALIBRATION = {
    "x_plot_min": 122.321,
    "x_plot_max": 462.473,
    "y_plot_min": 77.5344,
    "y_plot_max": 383.671,
    "lambda_min_m": 2.0e-6,
    "lambda_max_m": 1.0e-3,
    "alpha_min": 1.0e-3,
    "alpha_max": 1.0e6,
}

PROBABLE_2020_STYLE = ((0.333008, 0.0, 1.0), 1.304)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path, binary_prefix: bool = False) -> str:
    if not path.exists():
        return ""
    if binary_prefix:
        return path.read_bytes()[:64].decode("latin1", errors="replace")
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path, bool(spec.get("binary_prefix")))
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def supplement_retrieval_rows() -> list[dict[str, Any]]:
    attempts = read_json(SUPPLEMENT_ATTEMPTS_PATH, [])
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_id": attempt.get("attempt_id", f"ATT2704_{len(rows)}"),
                "source_key": attempt.get("key", ""),
                "url": attempt.get("url", ""),
                "headers_profile": attempt.get("headers_profile", ""),
                "status": attempt.get("status", ""),
                "http_status": attempt.get("http_status", ""),
                "content_type": attempt.get("content_type", ""),
                "bytes_saved": attempt.get("bytes_saved", 0),
                "local_file": attempt.get("local_file", ""),
                "notes": attempt.get("notes", ""),
                "claim_usable_now": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows or [
        {
            "attempt_id": "ATT2704_0_missing_attempt_json",
            "source_key": "MISSING_SUPPLEMENT_ATTEMPT_JSON",
            "url": "",
            "headers_profile": "",
            "status": "not_run",
            "http_status": "",
            "content_type": "",
            "bytes_saved": 0,
            "local_file": "",
            "notes": "supplement retrieval attempts file is missing",
            "claim_usable_now": "false",
            "timestamp_utc": stamp(),
        }
    ]


def parse_pdf_paths(pdf_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[float]]:
    page = PdfReader(str(pdf_path)).pages[0]
    media_box = [float(page.mediabox.width), float(page.mediabox.height)]
    raw = page.get_contents().get_data().decode("latin1")
    pattern = re.compile(r"/[A-Za-z0-9_.]+|[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][-+]?\d+)?|[A-Za-z*]+|\[|\]|<<|>>")
    num_re = re.compile(r"^[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][-+]?\d+)?$")
    tokens = pattern.findall(raw)
    stack: list[str] = []
    path: list[tuple[Any, ...]] = []
    stroke = (0.0, 0.0, 0.0)
    fill = (0.0, 0.0, 0.0)
    width = 1.0
    paths: list[dict[str, Any]] = []
    for token in tokens:
        if num_re.match(token) or token.startswith("/") or token in {"[", "]", "<<", ">>"}:
            stack.append(token)
            continue

        def nums(count: int) -> list[float]:
            values = [float(item) for item in stack[-count:]]
            del stack[-count:]
            return values

        op = token
        if op == "w" and len(stack) >= 1:
            width = nums(1)[0] * 0.1
        elif op == "RG" and len(stack) >= 3:
            stroke = tuple(nums(3))  # type: ignore[assignment]
        elif op == "rg" and len(stack) >= 3:
            fill = tuple(nums(3))  # type: ignore[assignment]
        elif op == "m" and len(stack) >= 2:
            x_value, y_value = nums(2)
            path.append(("m", x_value * 0.1, y_value * 0.1))
        elif op == "l" and len(stack) >= 2:
            x_value, y_value = nums(2)
            path.append(("l", x_value * 0.1, y_value * 0.1))
        elif op == "c" and len(stack) >= 6:
            x1, y1, x2, y2, x3, y3 = nums(6)
            path.append(("c", x1 * 0.1, y1 * 0.1, x2 * 0.1, y2 * 0.1, x3 * 0.1, y3 * 0.1))
        elif op == "h":
            path.append(("h",))
        elif op in {"S", "s", "f", "F", "f*", "B", "b", "B*", "b*"}:
            if path:
                paths.append({"paint": op, "stroke": stroke, "fill": fill, "width": round(width, 3), "path": path})
            path = []

    x0 = AXIS_CALIBRATION["x_plot_min"]
    x1 = AXIS_CALIBRATION["x_plot_max"]
    y0 = AXIS_CALIBRATION["y_plot_min"]
    y1 = AXIS_CALIBRATION["y_plot_max"]
    segments: list[dict[str, Any]] = []
    for pdf_path_row in paths:
        if pdf_path_row["paint"] not in {"S", "s", "B", "b", "B*", "b*"}:
            continue
        current: tuple[float, float] | None = None
        for segment in pdf_path_row["path"]:
            if segment[0] == "m":
                current = (float(segment[1]), float(segment[2]))
            elif segment[0] == "l" and current is not None:
                p1 = current
                p2 = (float(segment[1]), float(segment[2]))
                current = p2
                mx = (p1[0] + p2[0]) / 2.0
                my = (p1[1] + p2[1]) / 2.0
                if x0 - 2 <= mx <= x1 + 2 and y0 - 2 <= my <= y1 + 2:
                    segments.append(
                        {
                            "style": (tuple(pdf_path_row["stroke"]), pdf_path_row["width"]),
                            "stroke": tuple(pdf_path_row["stroke"]),
                            "width": pdf_path_row["width"],
                            "p1": p1,
                            "p2": p2,
                        }
                    )
            elif segment[0] == "c":
                current = (float(segment[5]), float(segment[6]))
    return paths, segments, media_box


def connected_components(segments: list[dict[str, Any]], style: tuple[tuple[float, float, float], float], tolerance: float = 0.8) -> list[list[dict[str, Any]]]:
    selected = [segment for segment in segments if segment["style"] == style]
    parent = list(range(len(selected)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(a_index: int, b_index: int) -> None:
        a_root = find(a_index)
        b_root = find(b_index)
        if a_root != b_root:
            parent[b_root] = a_root

    buckets: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for index, segment in enumerate(selected):
        for point in [segment["p1"], segment["p2"]]:
            key = (round(point[0] / tolerance), round(point[1] / tolerance))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for other_index in buckets.get((key[0] + dx, key[1] + dy), []):
                        other = selected[other_index]
                        distances = [
                            math.hypot(point[0] - other["p1"][0], point[1] - other["p1"][1]),
                            math.hypot(point[0] - other["p2"][0], point[1] - other["p2"][1]),
                        ]
                        if min(distances) <= tolerance:
                            union(index, other_index)
            buckets[key].append(index)

    components: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, segment in enumerate(selected):
        components[find(index)].append(segment)
    return sorted(components.values(), key=len, reverse=True)


def component_bbox(component: list[dict[str, Any]]) -> list[float]:
    points = [point for segment in component for point in [segment["p1"], segment["p2"]]]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def x_to_lambda(x_plot: float) -> float:
    log_min = math.log10(AXIS_CALIBRATION["lambda_min_m"])
    log_max = math.log10(AXIS_CALIBRATION["lambda_max_m"])
    frac = (x_plot - AXIS_CALIBRATION["x_plot_min"]) / (AXIS_CALIBRATION["x_plot_max"] - AXIS_CALIBRATION["x_plot_min"])
    return 10 ** (log_min + frac * (log_max - log_min))


def y_to_alpha(y_plot: float) -> float:
    log_min = math.log10(AXIS_CALIBRATION["alpha_min"])
    log_max = math.log10(AXIS_CALIBRATION["alpha_max"])
    frac = (y_plot - AXIS_CALIBRATION["y_plot_min"]) / (AXIS_CALIBRATION["y_plot_max"] - AXIS_CALIBRATION["y_plot_min"])
    return 10 ** (log_min + frac * (log_max - log_min))


def render_vector_probe(paths: list[dict[str, Any]], media_box: list[float]) -> None:
    CACHE_2704.mkdir(parents=True, exist_ok=True)
    width, height = media_box
    scale = 3
    image = Image.new("RGB", (int(width * scale), int(height * scale)), "white")
    draw = ImageDraw.Draw(image)

    def color(rgb: tuple[float, float, float]) -> tuple[int, int, int]:
        return tuple(max(0, min(255, int(round(channel * 255)))) for channel in rgb)

    def point(x_value: float, y_value: float) -> tuple[float, float]:
        return (x_value * scale, (height - y_value) * scale)

    for path_row in paths:
        points: list[tuple[float, float]] = []
        start: tuple[float, float] | None = None
        for segment in path_row["path"]:
            if segment[0] == "m":
                if points and path_row["paint"] in {"S", "s", "B", "b", "B*", "b*"}:
                    draw.line([point(x, y) for x, y in points], fill=color(tuple(path_row["stroke"])), width=max(1, int(path_row["width"] * scale)))
                points = [(float(segment[1]), float(segment[2]))]
                start = points[0]
            elif segment[0] == "l":
                points.append((float(segment[1]), float(segment[2])))
            elif segment[0] == "c":
                points.extend([(float(segment[1]), float(segment[2])), (float(segment[3]), float(segment[4])), (float(segment[5]), float(segment[6]))])
            elif segment[0] == "h" and start is not None:
                points.append(start)
        if points:
            if path_row["paint"] in {"f", "F", "f*", "B", "b", "B*", "b*"} and len(points) > 2:
                draw.polygon([point(x, y) for x, y in points], fill=color(tuple(path_row["fill"])))
            if path_row["paint"] in {"S", "s", "B", "b", "B*", "b*"} and len(points) > 1:
                draw.line([point(x, y) for x, y in points], fill=color(tuple(path_row["stroke"])), width=max(1, int(path_row["width"] * scale)))

    x0 = AXIS_CALIBRATION["x_plot_min"]
    x1 = AXIS_CALIBRATION["x_plot_max"]
    y0 = AXIS_CALIBRATION["y_plot_min"]
    y1 = AXIS_CALIBRATION["y_plot_max"]
    draw.rectangle([point(x0, y1), point(x1, y0)], outline=(255, 0, 0), width=3)
    image.save(VECTOR_RENDER_PATH)


def vector_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    paths, segments, media_box = parse_pdf_paths(FIG5_PATH)
    render_vector_probe(paths, media_box)
    components = connected_components(segments, PROBABLE_2020_STYLE)
    style_summaries: defaultdict[tuple[Any, ...], dict[str, Any]] = defaultdict(lambda: {"segments": 0, "length": 0.0, "points": []})
    for segment in segments:
        key = (segment["stroke"], segment["width"])
        length = math.hypot(segment["p2"][0] - segment["p1"][0], segment["p2"][1] - segment["p1"][1])
        style_summaries[key]["segments"] += 1
        style_summaries[key]["length"] += length
        style_summaries[key]["points"].extend([segment["p1"], segment["p2"]])

    vector_probe_rows: list[dict[str, Any]] = [
        {
            "probe_id": "FIG5PROBE2704_0_pdf",
            "object": "fig5b1.pdf",
            "status": "VECTOR_READABLE",
            "path_count": len(paths),
            "segment_count_in_axis_region": len(segments),
            "media_box": ";".join(f"{value:.6g}" for value in media_box),
            "render_png": str(VECTOR_RENDER_PATH),
            "probe_json": str(VECTOR_PROBE_PATH),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "probe_id": "FIG5PROBE2704_1_probable_2020_style",
            "object": "violet stroke width 1.304",
            "status": "CONNECTED_COMPONENTS_FOUND" if components else "MISSING_COMPONENT",
            "path_count": len(components),
            "segment_count_in_axis_region": sum(len(component) for component in components),
            "media_box": f"style={PROBABLE_2020_STYLE}",
            "render_png": str(VECTOR_RENDER_PATH),
            "probe_json": str(VECTOR_PROBE_PATH),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]

    curve_rows: list[dict[str, Any]] = []
    for index, component in enumerate(components[:4]):
        bbox = component_bbox(component)
        curve_rows.append(
            {
                "candidate_id": f"CURVE2704_violet_width1304_component_{index}",
                "source_pdf": str(FIG5_PATH),
                "probable_label": "Eot-Wash_2020_candidate" if index == 0 else "other_violet_curve_or_label_candidate",
                "component_rank": index,
                "stroke_rgb": ";".join(str(value) for value in PROBABLE_2020_STYLE[0]),
                "stroke_width_plot": PROBABLE_2020_STYLE[1],
                "segment_count": len(component),
                "x_plot_min": f"{bbox[0]:.8g}",
                "x_plot_max": f"{bbox[2]:.8g}",
                "y_plot_min": f"{bbox[1]:.8g}",
                "y_plot_max": f"{bbox[3]:.8g}",
                "lambda_min_m_est": f"{x_to_lambda(bbox[0]):.8e}",
                "lambda_max_m_est": f"{x_to_lambda(bbox[2]):.8e}",
                "alpha_min_est": f"{y_to_alpha(bbox[1]):.8e}",
                "alpha_max_est": f"{y_to_alpha(bbox[3]):.8e}",
                "qa_status": "CURVE_ID_PROBABLE_NOT_CONFIRMED;AXIS_CALIBRATION_INFERRED;OFFICIAL_SUPPLEMENT_NOT_ACQUIRED",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )

    samples: list[dict[str, Any]] = []
    if components:
        component = components[0]
        points = [point for segment in component for point in [segment["p1"], segment["p2"]]]
        points = [point for point in points if AXIS_CALIBRATION["x_plot_min"] <= point[0] <= AXIS_CALIBRATION["x_plot_max"] and AXIS_CALIBRATION["y_plot_min"] <= point[1] <= AXIS_CALIBRATION["y_plot_max"]]
        points = sorted(points, key=lambda point: point[0])
        deduped: list[tuple[float, float]] = []
        for point in points:
            if not deduped or abs(point[0] - deduped[-1][0]) > 0.35:
                deduped.append(point)
            else:
                previous = deduped[-1]
                deduped[-1] = ((previous[0] + point[0]) / 2.0, (previous[1] + point[1]) / 2.0)
        if len(deduped) > 32:
            step = (len(deduped) - 1) / 31
            sampled_points = [deduped[round(i * step)] for i in range(32)]
        else:
            sampled_points = deduped
        for index, point in enumerate(sampled_points):
            samples.append(
                {
                    "sample_id": f"EOTWASH2020_VEC2704_{index:03d}",
                    "candidate_id": "CURVE2704_violet_width1304_component_0",
                    "source_pdf": str(FIG5_PATH),
                    "lambda_value_m": f"{x_to_lambda(point[0]):.10e}",
                    "lambda_units": "m",
                    "alpha_bound_abs": f"{y_to_alpha(point[1]):.10e}",
                    "alpha_units": "dimensionless_abs_alpha",
                    "x_plot": f"{point[0]:.8g}",
                    "y_plot": f"{point[1]:.8g}",
                    "extraction_method": "vector_endpoint_decimation_from_cached_fig5b1_pdf",
                    "qa_flags": "NONCLAIM;CURVE_ID_PROBABLE_NOT_CONFIRMED;AXIS_CALIBRATION_INFERRED_FROM_FIGURE_LABELS;APS_SUPPLEMENT_BLOCKED",
                    "valid_for_claim": "false",
                    "timestamp_utc": stamp(),
                }
            )

    VECTOR_PROBE_PATH.write_text(
        json.dumps(
            {
                "source_pdf": str(FIG5_PATH),
                "axis_calibration": AXIS_CALIBRATION,
                "probable_style": {"stroke": PROBABLE_2020_STYLE[0], "width": PROBABLE_2020_STYLE[1]},
                "vector_probe_rows": vector_probe_rows,
                "curve_candidates": curve_rows,
                "sample_count": len(samples),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return vector_probe_rows, curve_rows, samples


def axis_calibration_rows() -> list[dict[str, Any]]:
    return [
        {
            "axis_id": "AXIS2704_0_x_lambda",
            "figure": "fig5b1.pdf",
            "axis": "x",
            "plot_min": AXIS_CALIBRATION["x_plot_min"],
            "plot_max": AXIS_CALIBRATION["x_plot_max"],
            "data_min": AXIS_CALIBRATION["lambda_min_m"],
            "data_max": AXIS_CALIBRATION["lambda_max_m"],
            "data_units": "m",
            "scale": "log10",
            "source_basis": "vector axis box plus visible tick labels 2e-6 to 1e-3 in diagnostic render",
            "qa_status": "INFERRED_NEEDS_HUMAN_OR_SUPPLEMENT_CONFIRMATION",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axis_id": "AXIS2704_1_y_abs_alpha",
            "figure": "fig5b1.pdf",
            "axis": "y",
            "plot_min": AXIS_CALIBRATION["y_plot_min"],
            "plot_max": AXIS_CALIBRATION["y_plot_max"],
            "data_min": AXIS_CALIBRATION["alpha_min"],
            "data_max": AXIS_CALIBRATION["alpha_max"],
            "data_units": "dimensionless_abs_alpha",
            "scale": "log10",
            "source_basis": "vector axis box plus visible tick labels 1e-3 to 1e6 in diagnostic render",
            "qa_status": "INFERRED_NEEDS_HUMAN_OR_SUPPLEMENT_CONFIRMATION",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def qloc_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "QD2704_0_exact_identity",
            "stage": "algebraic identity",
            "statement": "T_GK^{mu nu}=K_hat^{mu nu}-Gamma_eff g^{mu nu}; q_loc^nu=-P_loc nabla_mu T_GK^{mu nu}",
            "derived_status": "DERIVED_FROM_2699",
            "missing_for_live_claim": "none for identity; physical zero still unsigned",
            "consequence": "q_loc must be zero-proved or bounded as an actual residual, not hidden by plateau language",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "derivation_id": "QD2704_1_zero_theorem",
            "stage": "local GR zero route",
            "statement": "q_loc^nu=0 follows if T_GK is a single parent Hilbert stress, Euler/source/boundary/readout/projector terms vanish, and the local fixed point is a stress double zero",
            "derived_status": "CONDITIONAL_THEOREM_NOT_LIVE",
            "missing_for_live_claim": "MISSING_PARENT_SIGNED_ACTION;MISSING_HELMHOLTZ_CERTIFICATE;MISSING_BOUNDARY_NO_FLUX;MISSING_PLOC_OWNER;MISSING_PHYSICAL_DOUBLE_ZERO",
            "consequence": "local GR/Newton reduction remains blocked unless these clauses close together",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "derivation_id": "QD2704_2_finite_yukawa_shape",
            "stage": "finite profile route",
            "statement": "If a parent local quadratic mode X obeys (nabla^2-lambda_X^{-2}) chi_X = -Q_X rho and T_GK couples through C_X, then q_loc^r carries the Yukawa radial kernel proportional to C_X Q_X^S Q_X^T (1+r/lambda_X) exp(-r/lambda_X)/r^2",
            "derived_status": "CONDITIONAL_GREEN_FUNCTION_SHAPE_DERIVED",
            "missing_for_live_claim": "MISSING_PARENT_MODE_X;MISSING_C_X;MISSING_Q_X_SOURCE_TEST_CHARGES;MISSING_LAMBDA_X;MISSING_SOURCE_NORMALIZATION",
            "consequence": "the shape can be derived under a standard local massive kernel, but the MTS coefficients/ranges are not signed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "derivation_id": "QD2704_3_alpha_projection",
            "stage": "R10 projection",
            "statement": "alpha_q(lambda;r)=a_q(r,lambda)/a_N(r)*exp(r/lambda)/(1+r/lambda), with abs-alpha envelope over the experiment window",
            "derived_status": "OPERATOR_IMPORTED_FROM_2701",
            "missing_for_live_claim": "MISSING_A_Q_PROFILE;MISSING_A_N_SAME_FRAME;MISSING_FULL_CLAIM_GRADE_BOUND_CURVE",
            "consequence": "vector candidate data can test plumbing, not physics preference, until q_loc coefficients exist",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "derivation_id": "QD2704_4_live_branch_choice",
            "stage": "next derivation hinge",
            "statement": "Either prove QD2704_1 zero theorem, or derive numerical C_X,Q_X,lambda_X for QD2704_2 and compare to R10/PPN/clock/orbital bounds",
            "derived_status": "EXACT_CONTRACT_WRITTEN",
            "missing_for_live_claim": "MISSING_ZERO_PROOF_OR_FINITE_COEFFICIENTS",
            "consequence": "2705 should hunt coefficients, not circle the old q_loc blocker",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2704_0_supplement",
            "blocker": "official APS supplemental numerical values not acquired",
            "evidence": "all local APS/link.aps attempts returned 401/403",
            "effect": "vector candidate rows remain nonclaim",
            "next_action": "manual browser download or alternate official access; then ingest as source-backed table",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2704_1_curve_QA",
            "blocker": "Fig. 5 curve identity and axis calibration not independently confirmed",
            "evidence": "vector extraction found probable Eot-Wash 2020 component but relies on figure-label inference",
            "effect": "numeric candidate samples cannot update live claim curve",
            "next_action": "human/second-tool QA against visible figure or official supplement",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2704_2_q_loc_coefficients",
            "blocker": "q_loc finite Yukawa coefficients absent",
            "evidence": "conditional kernel shape exists, but C_X, Q_X and lambda_X are not parent-signed",
            "effect": "MTS alpha(lambda) prediction still absent",
            "next_action": "derive or source parent mode/coefficient/range law",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2704_3_local_GR",
            "blocker": "zero theorem still unsigned",
            "evidence": "parent action, Helmholtz, boundary, projector and double-zero clauses remain missing",
            "effect": "no local GR/Newton recovery claim",
            "next_action": "attack zero theorem or bound finite residuals arena-by-arena",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2704_0_vector_readable",
            "gate": "Fig. 5 vector extraction route exists",
            "status": "PASS_NONCLAIM_TOOLING",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "vector candidate rows are useful plumbing but not official/QA-locked data",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2704_1_official_curve",
            "gate": "official or QA-locked full alpha(lambda) curve",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "APS supplement blocked and figure extraction not QA-confirmed",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2704_2_mts_prediction",
            "gate": "MTS q_loc alpha(lambda) prediction",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "C_X/Q_X/lambda_X or zero theorem are missing",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2704_3_R10_score",
            "gate": "R10 local bound comparison can support evidence",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "bound curve candidate and q_loc prediction are both nonclaim",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2704_4_local_GR",
            "gate": "local GR/Newton recovery",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "q_loc is neither zero-proved nor bounded below all local arenas",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2704_5_private",
            "gate": "public/GitHub action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2704_0_data",
            "decision": "VECTOR_CANDIDATE_DATA_STAGED_NOT_CLAIMED",
            "rationale": "Fig. 5 bottom plot is vector-readable and yields a plausible Eot-Wash 2020 bound component, but official supplement/QA is still missing",
            "next_action": "use candidate samples only for pipeline smoke; do not update live claim curve",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2704_1_theory",
            "decision": "FINITE_PROFILE_REDUCED_TO_KERNEL_COEFFICIENTS",
            "rationale": "under a standard local massive Green-function route, the Yukawa radial shape is conditional; the missing physics is C_X, Q_X and lambda_X or a zero theorem",
            "next_action": "2705 should hunt parent mode coefficients/ranges",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2704_2_priority",
            "decision": "THEORY_COEFFICIENTS_ARE_NOW_HIGHER_VALUE_THAN_MORE_PLACEHOLDER_SCORING",
            "rationale": "the data side has a nonclaim candidate; without MTS alpha(lambda), more runner work is performative",
            "next_action": "derive q_loc kernel coefficients or prove q_loc zero",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2704_0_selected",
            "selection": "selected_primary",
            "target_doc": "2705-Y5-R2FR-q-loc-Yukawa-kernel-coefficients-or-zero-theorem.md",
            "target_script": "scripts/Y5_R2FR_q_loc_Yukawa_kernel_coefficients_or_zero_theorem_2705.py",
            "task": "try to derive the parent mode/range/coefficient law C_X,Q_X,lambda_X that turns q_loc into a real finite alpha(lambda) prediction; if that fails, sharpen the zero-theorem premises and keep the vector R10 curve candidate as nonclaim plumbing",
            "success_condition": "either a parent-signed finite q_loc coefficient/range row is produced, or the exact missing theorem clauses are reduced further without inventing a profile",
            "forbidden_shortcuts": "treat vector samples as official; score symbolic alpha; choose coefficients by fitting R10; claim local GR; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2704_0_R10_data",
            "topic": "R10 bound curve",
            "status": "VECTOR_CANDIDATE_STAGED_NONCLAIM",
            "meaning": "we have a likely Eot-Wash 2020 Fig. 5 candidate curve in numeric form for smoke plumbing, not evidence",
            "next_action": "QA/official supplement ingest",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2704_1_q_loc",
            "topic": "q_loc profile",
            "status": "SHAPE_CONDITIONAL_COEFFICIENTS_MISSING",
            "meaning": "the finite Yukawa profile shape can be written under a local massive kernel, but MTS parent coefficients/ranges are still absent",
            "next_action": "derive C_X,Q_X,lambda_X or zero theorem",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2704_2_local_GR",
            "topic": "local GR/Newton",
            "status": "NOT_CLAIMED_BUT_MORE_LOCALIZED",
            "meaning": "the gap is no longer vague coupling talk; it is zero theorem or finite kernel coefficients",
            "next_action": "2705 coefficient/zero theorem attack",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2704_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all artifacts remain private in post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validate(generated_paths: dict[str, Path], generated_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = generated_rows["source_register"]
    add("VAL2704_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2704_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    supplements = generated_rows["supplement_retrieval"]
    add("VAL2704_2_supplement_attempted", len(supplements) >= 8, "multiple APS/link.aps supplement retrieval attempts are recorded")
    add("VAL2704_3_no_official_supplement_cached", all(int(row.get("bytes_saved", 0) or 0) == 0 for row in supplements), "no official supplement file was cached and treated as data")
    add("VAL2704_4_supplement_blocked", any(str(row.get("http_status")) in {"401", "403"} for row in supplements), "APS/link.aps blocking is recorded")

    vector = generated_rows["vector_probe"]
    add("VAL2704_5_vector_readable", any(row["probe_id"] == "FIG5PROBE2704_0_pdf" and row["status"] == "VECTOR_READABLE" for row in vector), "fig5b1.pdf is vector-readable")
    add("VAL2704_6_render_created", VECTOR_RENDER_PATH.exists(), f"diagnostic render exists: {VECTOR_RENDER_PATH}")

    candidates = generated_rows["curve_candidates"]
    add("VAL2704_7_curve_candidate_exists", any(row["probable_label"] == "Eot-Wash_2020_candidate" for row in candidates), "probable Eot-Wash 2020 vector component staged")

    samples = generated_rows["candidate_samples"]
    positive_samples = True
    for row in samples:
        try:
            positive_samples = positive_samples and float(row["lambda_value_m"]) > 0 and float(row["alpha_bound_abs"]) > 0
        except ValueError:
            positive_samples = False
    add("VAL2704_8_candidate_samples_positive", positive_samples and len(samples) >= 10, "candidate vector samples have positive numeric lambda/alpha values")
    add("VAL2704_9_candidate_samples_nonclaim", all(row["valid_for_claim"] == "false" for row in samples), "all candidate vector samples remain nonclaim")

    derivation = generated_rows["qloc_derivation"]
    add("VAL2704_10_kernel_shape_written", any(row["derivation_id"] == "QD2704_2_finite_yukawa_shape" for row in derivation), "conditional finite Yukawa q_loc shape law is recorded")
    add("VAL2704_11_coefficients_missing", any("MISSING_C_X" in row["missing_for_live_claim"] for row in derivation), "parent coefficients/ranges remain explicitly missing")

    gates = generated_rows["claim_gates"]
    add("VAL2704_12_no_claims", all(row["claim_allowed"] == "false" for row in gates), "all claim gates keep claim_allowed=false")
    add("VAL2704_13_next_2705", any(row["next_id"] == "NEXT2704_0_selected" and "2705" in row["target_doc"] for row in generated_rows["next_target"]), "2705 target selected")
    add("VAL2704_14_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2704_15_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2704_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in validation if not row["check_id"].startswith("VAL2704_PARSE_validation")]
    overall = all(row["passed"] == "true" for row in core)
    add(
        "VAL2704_OVERALL",
        overall,
        "2704 stages a nonclaim vector-digitized R10 candidate curve, records APS supplement blocking, derives the conditional q_loc Yukawa shape contract, and selects coefficient/zero-theorem work next",
    )
    return validation


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Supplement Retrieval Attempts", rows_by_name["supplement_retrieval"]),
        ("Axis Calibration", rows_by_name["axis_calibration"]),
        ("Vector Probe", rows_by_name["vector_probe"]),
        ("Curve Candidates", rows_by_name["curve_candidates"]),
        ("Candidate Samples", rows_by_name["candidate_samples"][:12]),
        ("q_loc Parent-Profile Derivation", rows_by_name["qloc_derivation"]),
        ("Blocker Ledger", rows_by_name["blocker_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2704: APS Supplement Retrieval Or q_loc Parent-Profile Derivation",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2704 makes the data route sharper and then hands the baton back to derivation. APS/link.aps is still blocking the official supplement locally, so no official curve was acquired. But cached `fig5b1.pdf` is vector-readable, the axis box can be inferred from the visible log labels, and a probable Eot-Wash 2020 bound component has been sampled into a strictly nonclaim candidate table for pipeline smoke only. On the theory side, the finite q_loc profile route is now narrowed: under a local massive parent mode the Yukawa radial shape follows, but MTS still needs parent-signed `C_X`, `Q_X`, and `lambda_X`, or the full zero theorem.",
        "",
        "## Bottom Line",
        "",
        "- Data side: no official supplement yet, but vector candidate curve plumbing exists.",
        "- Theory side: the missing thing is now kernel coefficients/range, not vague coupling language.",
        "- Claim posture: no R10 pass, no local-GR pass, no live bound file update.",
        "- Best next move: derive `C_X,Q_X,lambda_X` or prove q_loc zero.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CACHE_2704.mkdir(parents=True, exist_ok=True)
    vector_probe_rows, curve_candidate_rows, candidate_sample_rows = vector_outputs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "supplement_retrieval": supplement_retrieval_rows(),
        "axis_calibration": axis_calibration_rows(),
        "vector_probe": vector_probe_rows,
        "curve_candidates": curve_candidate_rows,
        "candidate_samples": candidate_sample_rows,
        "qloc_derivation": qloc_derivation_rows(),
        "blocker_ledger": blocker_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_supplement_attempts"], rows_by_name["supplement_retrieval"])
    write_csv(BRANCH_OUTPUTS["local_axis_calibration"], rows_by_name["axis_calibration"])
    write_csv(BRANCH_OUTPUTS["local_vector_candidates"], rows_by_name["curve_candidates"])
    write_csv(BRANCH_OUTPUTS["local_candidate_samples"], rows_by_name["candidate_samples"])
    write_csv(BRANCH_OUTPUTS["wep_qloc_derivation"], rows_by_name["qloc_derivation"])
    write_csv(BRANCH_OUTPUTS["source_weight_qloc_derivation"], rows_by_name["qloc_derivation"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation_rows = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation_rows
    write_csv(OUTPUTS["validation"], validation_rows)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
