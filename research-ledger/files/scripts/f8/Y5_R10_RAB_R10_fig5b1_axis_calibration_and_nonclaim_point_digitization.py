from __future__ import annotations

import csv
import hashlib
import shutil
import subprocess
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
DOC = ROOT / "1497-Y5-R10-RAB-R10-fig5b1-axis-calibration-and-nonclaim-point-digitization.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1496_validation": OUT / "P8_Y5_BRR545_1496_VALIDATION.csv",
    "1496_selection": OUT / "P8_Y5_R10_1496_R10_CURVE_TARGET_SELECTION.csv",
    "1496_axis": OUT / "P8_Y5_R10_1496_AXIS_DETECTION_GATE.csv",
    "1496_template_status": OUT / "P8_Y5_R10_1496_DIGITIZATION_TEMPLATE_STATUS.csv",
    "1496_kernel": OUT / "P8_Y5_R10_1496_KERNEL_CONTRACT_REFRESH.csv",
    "1496_next": OUT / "P8_Y5_R10_1496_NEXT_TARGET.csv",
}

CURVE_FIGURE = R10 / "raw" / "Lee_2020_PRL_2002.11761_source_1495" / "fig5b1.pdf"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
STAGING_DIR = R10 / "derived" / "staging"
VECTOR_SKELETON = STAGING_DIR / "R10_fig5b1_vector_curve_skeleton_1497.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

RENDERER_CAPABILITY = OUT / "P8_Y5_R10_1497_RENDERER_CAPABILITY.csv"
VECTOR_PARSE_SUMMARY = OUT / "P8_Y5_R10_1497_FIG5B1_VECTOR_PATHS_SUMMARY.csv"
AXIS_CANDIDATES = OUT / "P8_Y5_R10_1497_FIG5B1_AXIS_CANDIDATES.csv"
CURVE_PATH_CANDIDATES = OUT / "P8_Y5_R10_1497_FIG5B1_CURVE_PATH_CANDIDATES.csv"
POINT_STATUS = OUT / "P8_Y5_R10_1497_NONCLAIM_POINT_DIGITIZATION_STATUS.csv"
AXIS_CONTRACT = OUT / "P8_Y5_R10_1497_AXIS_CALIBRATION_CONTRACT.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1497_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1497_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1497_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1497_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1497_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1497_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1497_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1497_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1497"
QUAR_AXIS = QUARANTINE / "FIG5B1_AXIS_CANDIDATES_NONCLAIM.csv"
QUAR_CURVES = QUARANTINE / "FIG5B1_CURVE_PATH_CANDIDATES_NONCLAIM.csv"
QUAR_POINTS = QUARANTINE / "NONCLAIM_POINT_DIGITIZATION_STATUS.csv"
QUAR_CONTRACT = QUARANTINE / "AXIS_CALIBRATION_CONTRACT_NONCLAIM.csv"
BRANCH_AXIS = BRANCH_RESIDUALS / "r10_fig5b1_axis_candidates_nonclaim_1497.csv"
BRANCH_CURVES = BRANCH_RESIDUALS / "r10_fig5b1_curve_path_candidates_nonclaim_1497.csv"
BRANCH_POINTS = BRANCH_RESIDUALS / "r10_nonclaim_point_digitization_status_1497.csv"
BRANCH_CONTRACT = BRANCH_RESIDUALS / "r10_axis_calibration_contract_nonclaim_1497.csv"


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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def renderer_rows() -> list[dict[str, Any]]:
    commands = ["magick", "gswin64c", "gswin32c", "mutool", "pdftoppm", "pdftocairo"]
    rows = []
    for command in commands:
        found = shutil.which(command) is not None
        version = ""
        if found:
            try:
                result = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5)
                version = (result.stdout or result.stderr).splitlines()[0] if (result.stdout or result.stderr) else ""
            except Exception:
                version = "found_version_probe_failed"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "renderer_id": f"REN1497_{command}",
                "command": command,
                "available": found,
                "version_probe": version,
                "render_effect": "can_attempt_image_digitization" if found and command != "magick" else "not_used_or_not_available",
                **flags(),
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "renderer_id": "REN1497_vector_parse",
            "command": "pypdf_content_stream_parse",
            "available": True,
            "version_probe": "local_vector_stream",
            "render_effect": "used_for_nonclaim_geometry_skeleton",
            **flags(),
        }
    )
    return rows


def pdf_content_stream() -> str:
    from pypdf import PdfReader

    page = PdfReader(str(CURVE_FIGURE)).pages[0]
    contents = page.get_contents()
    if isinstance(contents, list):
        data = b"".join(content.get_data() for content in contents)
    else:
        data = contents.get_data()
    return data.decode("latin-1", errors="ignore")


def as_float(value: str) -> float:
    return float(value)


def flush_path(
    rows: list[dict[str, Any]],
    path_id: int,
    path_points: list[tuple[float, float]],
    operators: list[str],
    line_width: float,
    stroke_color: tuple[float, float, float],
    fill_color: tuple[float, float, float],
    paint_op: str,
) -> int:
    if not path_points:
        return path_id
    xs = [point[0] for point in path_points]
    ys = [point[1] for point in path_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x, span_y = max_x - min_x, max_y - min_y
    color_name = "black" if stroke_color == (0.0, 0.0, 0.0) else f"rgb({stroke_color[0]:.3g},{stroke_color[1]:.3g},{stroke_color[2]:.3g})"
    if len(path_points) == 2 and span_x > 500 and span_y < 1:
        role = "long_horizontal_axis_or_grid_candidate"
    elif len(path_points) == 2 and span_y > 500 and span_x < 1:
        role = "long_vertical_axis_or_grid_candidate"
    elif stroke_color != (0.0, 0.0, 0.0) and span_x > 100 and span_y > 20:
        role = "colored_curve_or_band_candidate"
    elif line_width == 0:
        role = "fill_or_text_outline_candidate"
    else:
        role = "tick_text_or_minor_path"
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "path_id": f"PATH1497_{path_id}",
            "paint_op": paint_op,
            "operator_sequence": "".join(operators),
            "point_count": len(path_points),
            "line_width": line_width,
            "stroke_color": color_name,
            "fill_color": f"rgb({fill_color[0]:.3g},{fill_color[1]:.3g},{fill_color[2]:.3g})",
            "min_x": round(min_x, 6),
            "max_x": round(max_x, 6),
            "min_y": round(min_y, 6),
            "max_y": round(max_y, 6),
            "span_x": round(span_x, 6),
            "span_y": round(span_y, 6),
            "role_guess": role,
            **flags(),
        }
    )
    return path_id + 1


def vector_path_rows() -> list[dict[str, Any]]:
    text = pdf_content_stream()
    rows: list[dict[str, Any]] = []
    line_width = 1.0
    stroke_color = (0.0, 0.0, 0.0)
    fill_color = (0.0, 0.0, 0.0)
    path_points: list[tuple[float, float]] = []
    operators: list[str] = []
    path_id = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[-1]
        try:
            if op == "w" and len(parts) >= 2:
                line_width = as_float(parts[-2])
            elif op == "RG" and len(parts) >= 4:
                stroke_color = (as_float(parts[-4]), as_float(parts[-3]), as_float(parts[-2]))
            elif op == "rg" and len(parts) >= 4:
                fill_color = (as_float(parts[-4]), as_float(parts[-3]), as_float(parts[-2]))
            elif op == "m" and len(parts) >= 3:
                if path_points:
                    path_id = flush_path(rows, path_id, path_points, operators, line_width, stroke_color, fill_color, "implicit_new_move")
                path_points = [(as_float(parts[-3]), as_float(parts[-2]))]
                operators = ["m"]
            elif op == "l" and len(parts) >= 3:
                path_points.append((as_float(parts[-3]), as_float(parts[-2])))
                operators.append("l")
            elif op == "c" and len(parts) >= 7:
                path_points.extend(
                    [
                        (as_float(parts[-7]), as_float(parts[-6])),
                        (as_float(parts[-5]), as_float(parts[-4])),
                        (as_float(parts[-3]), as_float(parts[-2])),
                    ]
                )
                operators.append("c")
            elif op in {"S", "s", "f", "F", "B", "b", "n"}:
                path_id = flush_path(rows, path_id, path_points, operators, line_width, stroke_color, fill_color, op)
                path_points = []
                operators = []
        except Exception:
            continue
    if path_points:
        flush_path(rows, path_id, path_points, operators, line_width, stroke_color, fill_color, "eof")
    return rows


def axis_rows(paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    horizontals = [row for row in paths if row["role_guess"] == "long_horizontal_axis_or_grid_candidate"]
    verticals = [row for row in paths if row["role_guess"] == "long_vertical_axis_or_grid_candidate"]
    bottom = max(horizontals, key=lambda row: float(row["span_x"])) if horizontals else None
    left_or_tallest = max(verticals, key=lambda row: float(row["span_y"])) if verticals else None
    rows = []
    if bottom:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "axis_id": "AXIS1497_0_horizontal",
                "source_path_id": bottom["path_id"],
                "axis_role": "horizontal_plot_axis_candidate",
                "min_coord": bottom["min_x"],
                "max_coord": bottom["max_x"],
                "fixed_coord": bottom["min_y"],
                "coord_units": "pdf_vector_units_pre_cm_scale",
                "calibration_status": "GEOMETRY_FOUND_LABEL_VALUES_MISSING",
                "manual_requirement": "assign lambda tick labels from rendered figure before converting to physical units",
                **flags(),
            }
        )
    if left_or_tallest:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "axis_id": "AXIS1497_1_vertical",
                "source_path_id": left_or_tallest["path_id"],
                "axis_role": "vertical_plot_axis_candidate",
                "min_coord": left_or_tallest["min_y"],
                "max_coord": left_or_tallest["max_y"],
                "fixed_coord": left_or_tallest["min_x"],
                "coord_units": "pdf_vector_units_pre_cm_scale",
                "calibration_status": "GEOMETRY_FOUND_LABEL_VALUES_MISSING",
                "manual_requirement": "assign |alpha| tick labels from rendered figure before converting to physical units",
                **flags(),
            }
        )
    if not rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "axis_id": "AXIS1497_no_axis",
                "source_path_id": "",
                "axis_role": "axis_detection_failed",
                "min_coord": "",
                "max_coord": "",
                "fixed_coord": "",
                "coord_units": "pdf_vector_units_pre_cm_scale",
                "calibration_status": "AXIS_GEOMETRY_NOT_FOUND",
                "manual_requirement": "use rendered figure/manual calibration",
                **flags(),
            }
        )
    return rows


def plot_box(axis_candidates: list[dict[str, Any]]) -> dict[str, float] | None:
    horizontal = next((row for row in axis_candidates if row["axis_role"] == "horizontal_plot_axis_candidate"), None)
    vertical = next((row for row in axis_candidates if row["axis_role"] == "vertical_plot_axis_candidate"), None)
    if not horizontal or not vertical:
        return None
    return {
        "x_min": float(horizontal["min_coord"]),
        "x_max": float(horizontal["max_coord"]),
        "y_min": float(horizontal["fixed_coord"]),
        "y_max": float(vertical["max_coord"]),
    }


def inside_plot(row: dict[str, Any], box: dict[str, float]) -> bool:
    return (
        float(row["max_x"]) >= box["x_min"]
        and float(row["min_x"]) <= box["x_max"]
        and float(row["max_y"]) >= min(box["y_min"], box["y_max"])
        and float(row["min_y"]) <= max(box["y_min"], box["y_max"])
    )


def curve_candidate_rows(paths: list[dict[str, Any]], axes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    box = plot_box(axes)
    candidates = [
        row
        for row in paths
        if row["role_guess"] == "colored_curve_or_band_candidate" and (box is None or inside_plot(row, box))
    ]
    candidates = sorted(candidates, key=lambda row: (float(row["span_x"]) * float(row["span_y"]), int(row["point_count"])), reverse=True)
    if not candidates:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "candidate_id": "CURVE1497_no_vector_curve",
                "source_path_id": "",
                "stroke_color": "",
                "point_count": 0,
                "normalized_bbox_x0": "",
                "normalized_bbox_x1": "",
                "normalized_bbox_y0": "",
                "normalized_bbox_y1": "",
                "candidate_status": "NO_COLORED_CURVE_CANDIDATE_FOUND",
                "promotion_blocker": "manual/rendered digitization required",
                **flags(),
            }
        ]
    rows = []
    for index, row in enumerate(candidates[:20]):
        if box:
            nx0 = (float(row["min_x"]) - box["x_min"]) / (box["x_max"] - box["x_min"])
            nx1 = (float(row["max_x"]) - box["x_min"]) / (box["x_max"] - box["x_min"])
            ny0 = (float(row["min_y"]) - box["y_min"]) / (box["y_max"] - box["y_min"]) if box["y_max"] != box["y_min"] else ""
            ny1 = (float(row["max_y"]) - box["y_min"]) / (box["y_max"] - box["y_min"]) if box["y_max"] != box["y_min"] else ""
        else:
            nx0 = nx1 = ny0 = ny1 = ""
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "candidate_id": f"CURVE1497_{index}",
                "source_path_id": row["path_id"],
                "stroke_color": row["stroke_color"],
                "point_count": row["point_count"],
                "normalized_bbox_x0": round(nx0, 6) if nx0 != "" else "",
                "normalized_bbox_x1": round(nx1, 6) if nx1 != "" else "",
                "normalized_bbox_y0": round(ny0, 6) if ny0 != "" else "",
                "normalized_bbox_y1": round(ny1, 6) if ny1 != "" else "",
                "candidate_status": "VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM",
                "promotion_blocker": "axis labels and curve identity must be manually verified before numeric points",
                **flags(),
            }
        )
    return rows


def write_vector_skeleton(curves: list[dict[str, Any]]) -> list[dict[str, Any]]:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "skeleton_id": row["candidate_id"],
            "source_path_id": row["source_path_id"],
            "stroke_color": row["stroke_color"],
            "normalized_bbox_x0": row["normalized_bbox_x0"],
            "normalized_bbox_x1": row["normalized_bbox_x1"],
            "normalized_bbox_y0": row["normalized_bbox_y0"],
            "normalized_bbox_y1": row["normalized_bbox_y1"],
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound_abs": "",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "vector skeleton only; not a digitized curve point",
        }
        for row in curves
    ]
    write_csv(VECTOR_SKELETON, rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "point_status_id": "PTS1497_0_vector_skeleton",
            "skeleton_path": rel(VECTOR_SKELETON),
            "skeleton_rows": len(rows),
            "live_curve_target": rel(CURVE_TARGET),
            "live_curve_target_exists": CURVE_TARGET.exists(),
            "point_status": "VECTOR_SKELETON_WRITTEN_NO_NUMERIC_ALPHA_LAMBDA_POINTS",
            "reason": "axis labels/scale and curve identity not yet verified",
            **flags(),
        }
    ]


def axis_contract_rows(axis_candidates: list[dict[str, Any]], point_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    box = plot_box(axis_candidates)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "AXCON1497_0_plot_box",
            "required_object": "fig5b1 plot box",
            "current_status": "VECTOR_GEOMETRY_FOUND" if box else "MISSING",
            "value_or_path": str(box) if box else "",
            "promotion_requirement": "manual/rendered verification of axis tick labels",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "AXCON1497_1_x_axis",
            "required_object": "lambda axis calibration",
            "current_status": "LABEL_VALUES_MISSING",
            "value_or_path": rel(CURVE_FIGURE),
            "promotion_requirement": "map vector x coordinate to lambda units and record log/linear scale",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "AXCON1497_2_y_axis",
            "required_object": "|alpha| axis calibration",
            "current_status": "LABEL_VALUES_MISSING",
            "value_or_path": rel(CURVE_FIGURE),
            "promotion_requirement": "map vector y coordinate to dimensionless |alpha| and record log/linear scale",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "AXCON1497_3_points",
            "required_object": "digitized curve points",
            "current_status": point_rows[0]["point_status"],
            "value_or_path": point_rows[0]["skeleton_path"],
            "promotion_requirement": "replace vector skeleton with numeric positive lambda/alpha rows",
            **flags(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1497_0_axis_labels",
            "blocking_marker": "AXIS_LABEL_VALUES_MISSING",
            "reason": "vector geometry is found, but physical lambda/alpha tick labels are not machine-readable",
            "target_path": rel(CURVE_FIGURE),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1497_1_numeric_points",
            "blocking_marker": "NUMERIC_CURVE_POINTS_MISSING",
            "reason": "vector skeleton is not a physical alpha(lambda) bound curve",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1497_2_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "even validated curve points need a same-branch MTS projection kernel",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": f"READY1497_{index}_{row['blocker_id']}",
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
            "refusal_id": "CP1497_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "vector geometry parsing cannot derive parent coupling normalization",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1497_0_vector",
            "target": "R10 fig5b1 vector geometry",
            "current_status": "VECTOR_SKELETON_AVAILABLE_NONCLAIM",
            "claim_effect": "digitization route improved; no score/pass claim",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1497_1_local_GR",
            "target": "local GR/Newton reduction",
            "current_status": "NOT_CLOSED",
            "claim_effect": "no local-GR/Newton claim from vector parsing",
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    reasons = [
        ("REJ1497_0_axis", "AXIS_LABEL_VALUES_MISSING", "vector geometry lacks physical tick-label calibration"),
        ("REJ1497_1_points", "PHYSICAL_POINTS_MISSING", "candidate paths are not numeric alpha(lambda) rows"),
        ("REJ1497_2_kernel", "PROJECTION_KERNEL_MISSING", "delta_w-to-alpha kernel is still absent"),
        ("REJ1497_3_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "no parent coupling coefficient imported"),
        ("REJ1497_4_claim", "CLAIM_PROMOTION_FORBIDDEN", "no R10/local-GR/Newton pass may be claimed"),
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
            "decision_id": "DEC1497_0_vector_parse",
            "decision": "use fig5b1 PDF vector stream as the local digitization scaffold",
            "rationale": "no ordinary renderer is installed, but the vector content exposes geometry candidates",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1497_1_no_promotion",
            "decision": "write a vector skeleton but no physical alpha(lambda) points",
            "rationale": "axis labels and curve identity still require manual/rendered verification",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1497_0_1498",
            "next_target": "1498-Y5-R10-RAB-R10-rendered-axis-label-recovery-or-manual-calibration-packet.md",
            "script": "scripts/Y5_R10_RAB_R10_rendered_axis_label_recovery_or_manual_calibration_packet.py",
            "objective": "recover physical axis labels for fig5b1 via rendering/manual calibration, then convert vector skeleton candidates into nonclaim alpha(lambda) rows",
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


def skeleton_flags_false() -> bool:
    for row in read_csv(VECTOR_SKELETON):
        if row.get("valid_for_claim") not in ("False", "false", False) or row.get("claim_allowed") not in ("False", "false", False):
            return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (AXIS_CANDIDATES, QUAR_AXIS),
        (CURVE_PATH_CANDIDATES, QUAR_CURVES),
        (POINT_STATUS, QUAR_POINTS),
        (AXIS_CONTRACT, QUAR_CONTRACT),
        (AXIS_CANDIDATES, BRANCH_AXIS),
        (CURVE_PATH_CANDIDATES, BRANCH_CURVES),
        (POINT_STATUS, BRANCH_POINTS),
        (AXIS_CONTRACT, BRANCH_CONTRACT),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], path_rows: list[dict[str, Any]], axes: list[dict[str, Any]], curves: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values()) and CURVE_FIGURE.exists()
    vector_parsed = len(path_rows) > 100
    axis_found = any(row["calibration_status"] == "GEOMETRY_FOUND_LABEL_VALUES_MISSING" for row in axes)
    curve_candidates = any(row["candidate_status"] == "VECTOR_CURVE_OR_BAND_CANDIDATE_NONCLAIM" for row in curves)
    skeleton_ok = VECTOR_SKELETON.exists() and skeleton_flags_false()
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_AXIS, QUAR_CURVES, QUAR_POINTS, QUAR_CONTRACT, BRANCH_AXIS, BRANCH_CURVES, BRANCH_POINTS, BRANCH_CONTRACT])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    readiness_nonclaim = all(row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in read_csv(SCORE_READINESS))
    checks = [
        ("VAL1497_0_local_sources", source_paths_exist, "all cited 1496/source figure paths exist"),
        ("VAL1497_1_vector_parse", vector_parsed, f"vector path rows={len(path_rows)}"),
        ("VAL1497_2_axis_candidates", axis_found, "plot-axis geometry candidates found"),
        ("VAL1497_3_curve_candidates", curve_candidates, f"curve candidate rows={len(curves)}"),
        ("VAL1497_4_skeleton", skeleton_ok, "vector skeleton exists and remains nonclaim"),
        ("VAL1497_5_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1497_6_readiness_blocked", readiness_nonclaim, "delta_w/R10 readiness remains false"),
        ("VAL1497_7_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1497_8_csv_parse", csv_parse_ok, "all generated 1497 CSVs parse cleanly"),
        ("VAL1497_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1497_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1497_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1497_12_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
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
            "check_id": "VAL1497_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1497 parsed fig5b1 vector geometry and wrote a nonclaim curve skeleton"
            if overall
            else "1497 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(renderer: list[dict[str, Any]], axes: list[dict[str, Any]], curves: list[dict[str, Any]], point_rows: list[dict[str, Any]], contract: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    renderer_summary = [row for row in renderer if row["available"] in (True, "True") or row["renderer_id"] == "REN1497_vector_parse"]
    DOC.write_text(
        "\n".join(
            [
                "# 1497 - R10 fig5b1 Axis Calibration and Nonclaim Point Digitization",
                "",
                "## Verdict",
                "- No normal PDF renderer was available, but the `fig5b1.pdf` vector stream was parseable.",
                "- Plot-axis geometry and colored curve/band candidates were extracted into a nonclaim vector skeleton.",
                "- No physical `alpha(lambda)` points are promoted because axis tick labels and curve identity still require rendered/manual calibration.",
                "",
                "## Renderer Capability",
                md_table(renderer_summary, ["renderer_id", "command", "available", "render_effect"]),
                "",
                "## Axis Candidates",
                md_table(axes, ["axis_id", "axis_role", "min_coord", "max_coord", "fixed_coord", "calibration_status"]),
                "",
                "## Curve Path Candidates",
                md_table(curves[:10], ["candidate_id", "source_path_id", "stroke_color", "point_count", "candidate_status"]),
                "",
                "## Point Digitization Status",
                md_table(point_rows, ["point_status_id", "skeleton_path", "skeleton_rows", "point_status", "reason"]),
                "",
                "## Axis Calibration Contract",
                md_table(contract, ["contract_id", "required_object", "current_status", "promotion_requirement"]),
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
    renderer = renderer_rows()
    paths = vector_path_rows()
    axes = axis_rows(paths)
    curves = curve_candidate_rows(paths, axes)
    point_rows = write_vector_skeleton(curves)
    contract = axis_contract_rows(axes, point_rows)
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    c_parent_rows = c_parent_refusal_rows()
    local_rows = local_status_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(RENDERER_CAPABILITY, renderer)
    write_csv(VECTOR_PARSE_SUMMARY, paths)
    write_csv(AXIS_CANDIDATES, axes)
    write_csv(CURVE_PATH_CANDIDATES, curves)
    write_csv(POINT_STATUS, point_rows)
    write_csv(AXIS_CONTRACT, contract)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        RENDERER_CAPABILITY,
        VECTOR_PARSE_SUMMARY,
        AXIS_CANDIDATES,
        CURVE_PATH_CANDIDATES,
        POINT_STATUS,
        AXIS_CONTRACT,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, paths, axes, curves)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(renderer, axes, curves, point_rows, contract, validation, next_rows)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
