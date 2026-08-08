from __future__ import annotations

import csv
import hashlib
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1498-Y5-R10-RAB-R10-rendered-axis-label-recovery-or-manual-calibration-packet.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1497_validation": OUT / "P8_Y5_BRR545_1497_VALIDATION.csv",
    "1497_axes": OUT / "P8_Y5_R10_1497_FIG5B1_AXIS_CANDIDATES.csv",
    "1497_curves": OUT / "P8_Y5_R10_1497_FIG5B1_CURVE_PATH_CANDIDATES.csv",
    "1497_points": OUT / "P8_Y5_R10_1497_NONCLAIM_POINT_DIGITIZATION_STATUS.csv",
    "1497_next": OUT / "P8_Y5_R10_1497_NEXT_TARGET.csv",
}

CURVE_FIGURE = R10 / "raw" / "Lee_2020_PRL_2002.11761_source_1495" / "fig5b1.pdf"
STAGING_DIR = R10 / "derived" / "staging"
RENDER_PNG = STAGING_DIR / "fig5b1_vector_render_1498.png"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

RENDER_PACKET = OUT / "P8_Y5_R10_1498_FIG5B1_RENDER_PACKET.csv"
AXIS_CALIBRATION = OUT / "P8_Y5_R10_1498_AXIS_VISUAL_CALIBRATION.csv"
CALIBRATED_BBOX = OUT / "P8_Y5_R10_1498_VECTOR_CANDIDATE_CALIBRATED_BBOX.csv"
POINT_STATUS = OUT / "P8_Y5_R10_1498_NONCLAIM_POINT_STATUS.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1498_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1498_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1498_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1498_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1498_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1498_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1498_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1498_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1498"
QUAR_RENDER = QUARANTINE / "FIG5B1_RENDER_PACKET_NONCLAIM.csv"
QUAR_AXIS = QUARANTINE / "AXIS_VISUAL_CALIBRATION_NONCLAIM.csv"
QUAR_BBOX = QUARANTINE / "VECTOR_CANDIDATE_CALIBRATED_BBOX_NONCLAIM.csv"
QUAR_POINTS = QUARANTINE / "NONCLAIM_POINT_STATUS.csv"
BRANCH_RENDER = BRANCH_RESIDUALS / "r10_fig5b1_render_packet_nonclaim_1498.csv"
BRANCH_AXIS = BRANCH_RESIDUALS / "r10_axis_visual_calibration_nonclaim_1498.csv"
BRANCH_BBOX = BRANCH_RESIDUALS / "r10_vector_candidate_calibrated_bbox_nonclaim_1498.csv"
BRANCH_POINTS = BRANCH_RESIDUALS / "r10_nonclaim_point_status_1498.csv"

X_AXIS_LEFT = 1223.21
X_AXIS_RIGHT = 4624.73
Y_AXIS_BOTTOM = 775.344
Y_AXIS_TOP = 3836.71
X_LOG_ANCHOR = 2102.79
X_LOG_ANCHOR_LOG10_LAMBDA_M = -5.0
X_UNITS_PER_DECADE = (4619.34 - 2102.79) / 2.0
Y_LOG_ALPHA_MIN = -3.0
Y_LOG_ALPHA_MAX = 6.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_content_stream() -> str:
    from pypdf import PdfReader

    page = PdfReader(str(CURVE_FIGURE)).pages[0]
    contents = page.get_contents()
    if isinstance(contents, list):
        data = b"".join(content.get_data() for content in contents)
    else:
        data = contents.get_data()
    return data.decode("latin-1", errors="ignore")


def rgb(vals: list[str]) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(round(float(value) * 255)))) for value in vals)


def render_vector_png() -> dict[str, Any]:
    text = pdf_content_stream()
    width, height = 1400, 1220
    sx, sy = width / 4950.0, height / 4310.0
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    line_width = 1.0
    stroke = (0, 0, 0)
    fill = (0, 0, 0)
    current: list[tuple[float, float]] = []

    def tr(point: tuple[float, float]) -> tuple[float, float]:
        return point[0] * sx, height - point[1] * sy

    def cubic(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], steps: int = 12) -> list[tuple[float, float]]:
        points = []
        for step in range(steps + 1):
            t = step / steps
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t**3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t**3 * p3[1]
            points.append((x, y))
        return points

    def flush(op: str) -> None:
        if len(current) >= 2:
            pts = [tr(point) for point in current]
            color = fill if op in {"f", "F"} else stroke
            draw.line(pts, fill=color, width=max(1, int(round(line_width * sx))))

    for raw in text.splitlines():
        parts = raw.strip().split()
        if not parts:
            continue
        op = parts[-1]
        try:
            if op == "w":
                line_width = float(parts[-2])
            elif op == "RG":
                stroke = rgb(parts[-4:-1])
            elif op == "rg":
                fill = rgb(parts[-4:-1])
            elif op == "m":
                if current:
                    flush("S")
                current = [(float(parts[-3]), float(parts[-2]))]
            elif op == "l":
                current.append((float(parts[-3]), float(parts[-2])))
            elif op == "c" and current:
                p0 = current[-1]
                p1 = (float(parts[-7]), float(parts[-6]))
                p2 = (float(parts[-5]), float(parts[-4]))
                p3 = (float(parts[-3]), float(parts[-2]))
                current.extend(cubic(p0, p1, p2, p3)[1:])
            elif op in {"S", "s", "f", "F", "B", "b", "n"}:
                flush(op)
                current = []
        except Exception:
            continue
    if current:
        flush("S")
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    image.save(RENDER_PNG)
    return {
        "same_parent_branch_id": BRANCH_ID,
        "render_id": "RENDER1498_0_fig5b1_vector",
        "source_pdf": rel(CURVE_FIGURE),
        "render_png": rel(RENDER_PNG),
        "render_exists": RENDER_PNG.exists(),
        "render_byte_count": RENDER_PNG.stat().st_size if RENDER_PNG.exists() else 0,
        "render_sha256": file_sha256(RENDER_PNG) if RENDER_PNG.exists() else "",
        "render_method": "PIL drawing of pypdf content stream paths",
        "visual_status": "READABLE_FOR_MANUAL_AXIS_CALIBRATION_NONCLAIM",
        "timestamp_utc": utc_now(),
        **flags(),
    }


def axis_calibration_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_0_x_left",
            "axis": "x_lambda",
            "vector_coord": X_AXIS_LEFT,
            "physical_value": "2e-6",
            "physical_units": "m",
            "calibration_basis": "visible rendered left tick label 2 with decade context before 10^-5",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_1_x_major_1e5",
            "axis": "x_lambda",
            "vector_coord": X_LOG_ANCHOR,
            "physical_value": "1e-5",
            "physical_units": "m",
            "calibration_basis": "visible rendered major tick 10^-5",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_2_x_major_1e4",
            "axis": "x_lambda",
            "vector_coord": 3361.06,
            "physical_value": "1e-4",
            "physical_units": "m",
            "calibration_basis": "visible rendered major tick 10^-4",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_3_x_major_1e3",
            "axis": "x_lambda",
            "vector_coord": 4619.34,
            "physical_value": "1e-3",
            "physical_units": "m",
            "calibration_basis": "visible rendered major tick 10^-3",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_4_y_bottom",
            "axis": "y_abs_alpha",
            "vector_coord": Y_AXIS_BOTTOM,
            "physical_value": "1e-3",
            "physical_units": "dimensionless",
            "calibration_basis": "visible rendered bottom major tick 10^-3",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_calibration_id": "AXCAL1498_5_y_top",
            "axis": "y_abs_alpha",
            "vector_coord": Y_AXIS_TOP,
            "physical_value": "1e6",
            "physical_units": "dimensionless",
            "calibration_basis": "visible rendered top major tick 10^6",
            "calibration_status": "VISUAL_CALIBRATION_NONCLAIM_REQUIRES_REVIEW",
            **flags(),
        },
    ]


def vector_x_to_lambda(x: float) -> float:
    log_lambda = X_LOG_ANCHOR_LOG10_LAMBDA_M + (x - X_LOG_ANCHOR) / X_UNITS_PER_DECADE
    return 10**log_lambda


def vector_y_to_alpha(y: float) -> float:
    frac = (y - Y_AXIS_BOTTOM) / (Y_AXIS_TOP - Y_AXIS_BOTTOM)
    log_alpha = Y_LOG_ALPHA_MIN + frac * (Y_LOG_ALPHA_MAX - Y_LOG_ALPHA_MIN)
    return 10**log_alpha


def calibrated_bbox_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCE_FILES["1497_curves"]):
        if row["candidate_status"] != "VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM":
            continue
        x0 = X_AXIS_LEFT + float(row["normalized_bbox_x0"]) * (X_AXIS_RIGHT - X_AXIS_LEFT)
        x1 = X_AXIS_LEFT + float(row["normalized_bbox_x1"]) * (X_AXIS_RIGHT - X_AXIS_LEFT)
        y0 = Y_AXIS_BOTTOM + float(row["normalized_bbox_y0"]) * (Y_AXIS_TOP - Y_AXIS_BOTTOM)
        y1 = Y_AXIS_BOTTOM + float(row["normalized_bbox_y1"]) * (Y_AXIS_TOP - Y_AXIS_BOTTOM)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "bbox_id": f"BBOX1498_{row['candidate_id']}",
                "source_candidate_id": row["candidate_id"],
                "source_path_id": row["source_path_id"],
                "stroke_color": row["stroke_color"],
                "lambda_min_m_approx": f"{min(vector_x_to_lambda(x0), vector_x_to_lambda(x1)):.6e}",
                "lambda_max_m_approx": f"{max(vector_x_to_lambda(x0), vector_x_to_lambda(x1)):.6e}",
                "alpha_min_approx": f"{min(vector_y_to_alpha(y0), vector_y_to_alpha(y1)):.6e}",
                "alpha_max_approx": f"{max(vector_y_to_alpha(y0), vector_y_to_alpha(y1)):.6e}",
                "bbox_status": "CALIBRATED_BBOX_ONLY_NOT_CURVE_POINTS",
                "promotion_blocker": "candidate identity and sampled curve points still require manual/render verification",
                **flags(),
            }
        )
    return rows


def point_status_rows(bbox_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "point_status_id": "PTS1498_0_bbox_ranges",
            "bbox_rows": len(bbox_rows),
            "live_curve_target": rel(CURVE_TARGET),
            "live_curve_target_exists": CURVE_TARGET.exists(),
            "point_status": "APPROX_BBOX_RANGES_ONLY_NO_DIGITIZED_POINTS",
            "reason": "1498 preserves axis calibration and candidate ranges, but does not sample the correct curve into alpha(lambda) rows",
            **flags(),
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1498_0_identity",
            "blocking_marker": "CURVE_IDENTITY_NOT_VERIFIED",
            "reason": "multiple colored candidates exist; the Eot-Wash 2020 curve must be isolated before point rows",
            "target_path": rel(RENDER_PNG),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1498_1_points",
            "blocking_marker": "DIGITIZED_POINT_ROWS_MISSING",
            "reason": "calibrated bounding boxes are not alpha(lambda) curve samples",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1498_2_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "R10 bound curve still needs same-branch MTS projection kernel",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1498_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1498_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "axis calibration cannot derive parent coupling normalization",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1498_0_1499",
            "next_target": "1499-Y5-R10-RAB-isolate-EotWash-2020-curve-and-sample-nonclaim-alpha-lambda-points.md",
            "script": "scripts/Y5_R10_RAB_isolate_EotWash_2020_curve_and_sample_nonclaim_alpha_lambda_points.py",
            "objective": "isolate the Eot-Wash 2020 curve in fig5b1, sample approximate nonclaim alpha(lambda) points, and keep R10 scoring blocked until the projection kernel exists",
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
        (RENDER_PACKET, QUAR_RENDER),
        (AXIS_CALIBRATION, QUAR_AXIS),
        (CALIBRATED_BBOX, QUAR_BBOX),
        (POINT_STATUS, QUAR_POINTS),
        (RENDER_PACKET, BRANCH_RENDER),
        (AXIS_CALIBRATION, BRANCH_AXIS),
        (CALIBRATED_BBOX, BRANCH_BBOX),
        (POINT_STATUS, BRANCH_POINTS),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], render: dict[str, Any], bbox_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values()) and CURVE_FIGURE.exists()
    render_ok = RENDER_PNG.exists() and RENDER_PNG.stat().st_size > 10_000
    axis_rows_ok = len(read_csv(AXIS_CALIBRATION)) >= 6
    bbox_ok = len(bbox_rows) >= 10
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_RENDER, QUAR_AXIS, QUAR_BBOX, QUAR_POINTS, BRANCH_RENDER, BRANCH_AXIS, BRANCH_BBOX, BRANCH_POINTS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1498_0_local_sources", source_paths_exist, "all cited 1497/source figure paths exist"),
        ("VAL1498_1_render", render_ok, f"render path={render['render_png']}"),
        ("VAL1498_2_axis_calibration", axis_rows_ok, "visual axis calibration rows written"),
        ("VAL1498_3_bbox_ranges", bbox_ok, f"calibrated bbox rows={len(bbox_rows)}"),
        ("VAL1498_4_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1498_5_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1498_6_csv_parse", csv_parse_ok, "all generated 1498 CSVs parse cleanly"),
        ("VAL1498_7_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1498_8_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1498_9_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1498_10_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1498_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1498 rendered fig5b1 and wrote nonclaim visual axis calibration/bbox ranges"
            if overall
            else "1498 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(render: dict[str, Any], axis_rows: list[dict[str, Any]], bbox_rows: list[dict[str, Any]], point_rows: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1498 - R10 Rendered Axis Label Recovery or Manual Calibration Packet",
                "",
                "## Verdict",
                "- `fig5b1.pdf` was rendered locally from its vector stream into a readable PNG.",
                "- Visible axis calibration anchors were recorded as nonclaim review assumptions.",
                "- Candidate vector bboxes were converted into approximate physical ranges, but no live `alpha(lambda)` point rows were promoted.",
                "",
                "## Render Packet",
                md_table([render], ["render_id", "render_png", "render_byte_count", "visual_status"]),
                "",
                "## Axis Visual Calibration",
                md_table(axis_rows, ["axis_calibration_id", "axis", "vector_coord", "physical_value", "physical_units", "calibration_status"]),
                "",
                "## Calibrated Candidate BBox Preview",
                md_table(bbox_rows[:10], ["bbox_id", "stroke_color", "lambda_min_m_approx", "lambda_max_m_approx", "alpha_min_approx", "alpha_max_approx", "bbox_status"]),
                "",
                "## Point Status",
                md_table(point_rows, ["point_status_id", "bbox_rows", "point_status", "reason"]),
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
    render = render_vector_png()
    axis_rows = axis_calibration_rows()
    bbox_rows = calibrated_bbox_rows()
    point_rows = point_status_rows(bbox_rows)
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent_rows = c_parent_refusal_rows()
    local_rows = [
        {"same_parent_branch_id": BRANCH_ID, "local_status_id": "LRS1498_0", "object": "R10 fig5b1 calibration", "status": "RENDERED_AXIS_PACKET_NONCLAIM", "effect": "digitization route improved, no R10/local claim", **flags()}
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = [
        {"same_parent_branch_id": BRANCH_ID, "decision_id": "DEC1498_0", "decision": "use local vector render for manual axis calibration", "rationale": "render is readable but still needs review before live curve promotion", **flags()}
    ]
    next_rows = next_target_rows()

    write_csv(RENDER_PACKET, [render])
    write_csv(AXIS_CALIBRATION, axis_rows)
    write_csv(CALIBRATED_BBOX, bbox_rows)
    write_csv(POINT_STATUS, point_rows)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        RENDER_PACKET,
        AXIS_CALIBRATION,
        CALIBRATED_BBOX,
        POINT_STATUS,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, render, bbox_rows)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(render, axis_rows, bbox_rows, point_rows, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
