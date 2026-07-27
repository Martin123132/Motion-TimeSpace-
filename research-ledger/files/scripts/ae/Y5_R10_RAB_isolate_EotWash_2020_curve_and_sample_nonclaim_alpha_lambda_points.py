from __future__ import annotations

import csv
import hashlib
import math
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
DOC = ROOT / "1499-Y5-R10-RAB-isolate-EotWash-2020-curve-and-sample-nonclaim-alpha-lambda-points.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1498_validation": OUT / "P8_Y5_BRR545_1498_VALIDATION.csv",
    "1498_render": OUT / "P8_Y5_R10_1498_FIG5B1_RENDER_PACKET.csv",
    "1498_axis": OUT / "P8_Y5_R10_1498_AXIS_VISUAL_CALIBRATION.csv",
    "1498_bbox": OUT / "P8_Y5_R10_1498_VECTOR_CANDIDATE_CALIBRATED_BBOX.csv",
    "1498_next": OUT / "P8_Y5_R10_1498_NEXT_TARGET.csv",
}

CURVE_FIGURE = R10 / "raw" / "Lee_2020_PRL_2002.11761_source_1495" / "fig5b1.pdf"
RENDER_PNG = R10 / "derived" / "staging" / "fig5b1_vector_render_1498.png"
OVERLAY_PNG = R10 / "derived" / "staging" / "fig5b1_EotWash2020_nonclaim_sample_overlay_1499.png"
VISUAL_POINTS = R10 / "derived" / "staging" / "R10_EotWash2020_alpha_lambda_VISUAL_NONCLAIM_1499.csv"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

CURVE_SELECTION = OUT / "P8_Y5_R10_1499_EOTWASH2020_CURVE_SELECTION.csv"
NONCLAIM_POINTS = OUT / "P8_Y5_R10_1499_EOTWASH2020_ALPHA_LAMBDA_POINTS_NONCLAIM.csv"
OVERLAY_LEDGER = OUT / "P8_Y5_R10_1499_SAMPLE_OVERLAY_LEDGER.csv"
POINT_QUALITY = OUT / "P8_Y5_R10_1499_POINT_QUALITY_LEDGER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1499_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1499_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1499_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1499_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1499_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1499_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1499_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1499_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1499"
QUAR_SELECTION = QUARANTINE / "EOTWASH2020_CURVE_SELECTION_NONCLAIM.csv"
QUAR_POINTS = QUARANTINE / "EOTWASH2020_ALPHA_LAMBDA_POINTS_NONCLAIM.csv"
QUAR_QUALITY = QUARANTINE / "POINT_QUALITY_LEDGER_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "TARGET_PROMOTION_BLOCKERS_NONCLAIM.csv"
BRANCH_SELECTION = BRANCH_RESIDUALS / "r10_eotwash2020_curve_selection_nonclaim_1499.csv"
BRANCH_POINTS = BRANCH_RESIDUALS / "r10_eotwash2020_alpha_lambda_points_nonclaim_1499.csv"
BRANCH_QUALITY = BRANCH_RESIDUALS / "r10_point_quality_ledger_nonclaim_1499.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "r10_target_promotion_blockers_nonclaim_1499.csv"

X_AXIS_LEFT = 1223.21
X_AXIS_RIGHT = 4624.73
Y_AXIS_BOTTOM = 775.344
Y_AXIS_TOP = 3836.71
X_LOG_ANCHOR = 2102.79
X_LOG_ANCHOR_LOG10_LAMBDA_M = -5.0
X_UNITS_PER_DECADE = (4619.34 - 2102.79) / 2.0
Y_LOG_ALPHA_MIN = -3.0
Y_LOG_ALPHA_MAX = 6.0

SAMPLE_POINTS = [
    ("R10EW2020_0_visual_left_high", 7.0e-6, 2.0e5, "visual_curve_candidate"),
    ("R10EW2020_1_visual_knee_high", 1.0e-5, 2.5e4, "visual_curve_candidate"),
    ("R10EW2020_2_arrow_endpoint", 1.9e-5, 9.0e1, "blue_label_arrow_endpoint_candidate"),
    ("R10EW2020_3_text_threshold_anchor", 3.86e-5, 1.0, "source_text_alpha1_threshold_anchor"),
    ("R10EW2020_4_visual_post_threshold", 5.0e-5, 1.6e-1, "visual_curve_candidate"),
    ("R10EW2020_5_visual_minimum_left", 8.0e-5, 3.0e-2, "visual_curve_candidate"),
    ("R10EW2020_6_visual_floor", 1.2e-4, 1.2e-2, "visual_curve_candidate"),
    ("R10EW2020_7_visual_right_tail", 2.5e-4, 5.0e-3, "visual_curve_candidate"),
    ("R10EW2020_8_visual_far_right", 5.0e-4, 3.0e-3, "visual_curve_candidate"),
]


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


def lambda_to_vector_x(lambda_m: float) -> float:
    return X_LOG_ANCHOR + X_UNITS_PER_DECADE * (math.log10(lambda_m) - X_LOG_ANCHOR_LOG10_LAMBDA_M)


def alpha_to_vector_y(alpha_abs: float) -> float:
    frac = (math.log10(alpha_abs) - Y_LOG_ALPHA_MIN) / (Y_LOG_ALPHA_MAX - Y_LOG_ALPHA_MIN)
    return Y_AXIS_BOTTOM + frac * (Y_AXIS_TOP - Y_AXIS_BOTTOM)


def vector_to_pixel(x: float, y: float, width: int, height: int) -> tuple[float, float]:
    return x * width / 4950.0, height - y * height / 4310.0


def point_rows() -> list[dict[str, Any]]:
    rows = []
    for sample_id, lambda_m, alpha_abs, sample_role in SAMPLE_POINTS:
        vx = lambda_to_vector_x(lambda_m)
        vy = alpha_to_vector_y(alpha_abs)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "point_id": sample_id,
                "curve_identity": "EotWash_2020_fig5b1_candidate",
                "lambda_value": f"{lambda_m:.8e}",
                "lambda_units": "m",
                "alpha_bound_abs": f"{alpha_abs:.8e}",
                "alpha_sign_convention": "absolute_upper_limit_abs_alpha",
                "confidence": "95_percent_from_fig5_caption",
                "point_source": sample_role,
                "figure_file": rel(CURVE_FIGURE),
                "render_file": rel(RENDER_PNG),
                "vector_x_approx": f"{vx:.6f}",
                "vector_y_approx": f"{vy:.6f}",
                "digitization_method": "manual_visual_estimate_from_1498_render_plus_38p6um_text_anchor",
                "promotion_status": "NONCLAIM_APPROXIMATE_VISUAL_POINT_REQUIRES_REVIEW",
                **flags(),
            }
        )
    return rows


def selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "selection_id": "SEL1499_0_EotWash2020_candidate",
            "curve_identity": "EotWash_2020_fig5b1_candidate",
            "selection_basis": "fig5b1 caption identifies bottom panel as 95 percent |alpha| limits; blue Eot-Wash 2020 label/arrow plus text alpha=1 at lambda<38.6um anchors the candidate",
            "source_figure": rel(CURVE_FIGURE),
            "render_figure": rel(RENDER_PNG),
            "live_curve_target": rel(CURVE_TARGET),
            "selection_status": "SELECTED_FOR_NONCLAIM_VISUAL_SAMPLING_ONLY",
            "review_requirement": "human/render verification required before any live curve promotion",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "selection_id": "SEL1499_1_live_refusal",
            "curve_identity": "R10_alpha_lambda_bound_curve_DIGITIZED",
            "selection_basis": "1499 points are approximate and not a digitized primary curve table",
            "source_figure": rel(CURVE_FIGURE),
            "render_figure": rel(RENDER_PNG),
            "live_curve_target": rel(CURVE_TARGET),
            "selection_status": "LIVE_TARGET_NOT_WRITTEN",
            "review_requirement": "write live target only after reviewed digitization and projection-kernel separation",
            **flags(),
        },
    ]


def render_overlay(points: list[dict[str, Any]]) -> dict[str, Any]:
    image = Image.open(RENDER_PNG).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for row in points:
        x = float(row["vector_x_approx"])
        y = float(row["vector_y_approx"])
        px, py = vector_to_pixel(x, y, width, height)
        radius = 6 if row["point_source"] == "source_text_alpha1_threshold_anchor" else 4
        color = "red" if row["point_source"] != "source_text_alpha1_threshold_anchor" else "orange"
        draw.ellipse((px - radius, py - radius, px + radius, py + radius), outline=color, width=3)
    image.save(OVERLAY_PNG)
    return {
        "same_parent_branch_id": BRANCH_ID,
        "overlay_id": "OVERLAY1499_0_sample_points",
        "overlay_png": rel(OVERLAY_PNG),
        "overlay_exists": OVERLAY_PNG.exists(),
        "overlay_byte_count": OVERLAY_PNG.stat().st_size if OVERLAY_PNG.exists() else 0,
        "overlay_sha256": file_sha256(OVERLAY_PNG) if OVERLAY_PNG.exists() else "",
        "overlay_status": "NONCLAIM_REVIEW_OVERLAY_WRITTEN",
        **flags(),
    }


def quality_rows(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "quality_id": "QUAL1499_0_method",
            "object": "point_set_method",
            "status": "ROUGH_VISUAL_NONCLAIM",
            "detail": "points mix visual estimates with one source-text threshold anchor; they are not a digitized primary curve",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "quality_id": "QUAL1499_1_monotonic_lambda",
            "object": "lambda_order",
            "status": "PASS" if all(float(points[i]["lambda_value"]) < float(points[i + 1]["lambda_value"]) for i in range(len(points) - 1)) else "FAIL",
            "detail": "lambda values increase left-to-right",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "quality_id": "QUAL1499_2_alpha1_anchor",
            "object": "38p6um_alpha1_anchor",
            "status": "PRESENT_NONCLAIM",
            "detail": "source text says gravitational-strength Yukawa interactions limited to ranges <38.6um; stored as alpha=1 anchor only",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "quality_id": "QUAL1499_3_live_target",
            "object": "live_curve_target",
            "status": "ABSENT_BY_DESIGN",
            "detail": rel(CURVE_TARGET),
            **flags(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1499_0_visual_review",
            "blocking_marker": "VISUAL_POINTS_NEED_REVIEW",
            "reason": "1499 points are approximate visual samples, not a reviewed digitized curve",
            "target_path": rel(VISUAL_POINTS),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1499_1_live_curve",
            "blocking_marker": "LIVE_R10_CURVE_NOT_PROMOTED",
            "reason": "live target remains absent until points are reviewed and method documented",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1499_2_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "R10 comparison still needs same-branch MTS projection kernel",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1499_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "visual R10 points cannot derive parent coupling normalization",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1499_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1499_0_1500",
            "next_target": "1500-Y5-R10-RAB-reviewed-R10-curve-promotion-gate-or-kernel-derivation-contract.md",
            "script": "scripts/Y5_R10_RAB_reviewed_R10_curve_promotion_gate_or_kernel_derivation_contract.py",
            "objective": "either review/refine the visual R10 alpha(lambda) points into a live claim-eligible curve candidate, or keep the curve staged and derive the delta_w-to-alpha projection kernel contract",
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


def write_visual_points(points: list[dict[str, Any]]) -> None:
    rows = [
        {
            "lambda_value": row["lambda_value"],
            "lambda_units": row["lambda_units"],
            "alpha_bound_abs": row["alpha_bound_abs"],
            "confidence": row["confidence"],
            "curve_source": row["figure_file"],
            "digitization_method": row["digitization_method"],
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "visual nonclaim staging only",
        }
        for row in points
    ]
    write_csv(VISUAL_POINTS, rows)


def visual_points_flags_false() -> bool:
    for row in read_csv(VISUAL_POINTS):
        if row["valid_for_claim"] != "False" or row["claim_allowed"] != "False":
            return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (CURVE_SELECTION, QUAR_SELECTION),
        (NONCLAIM_POINTS, QUAR_POINTS),
        (POINT_QUALITY, QUAR_QUALITY),
        (TARGET_BLOCKERS, QUAR_BLOCKERS),
        (CURVE_SELECTION, BRANCH_SELECTION),
        (NONCLAIM_POINTS, BRANCH_POINTS),
        (POINT_QUALITY, BRANCH_QUALITY),
        (TARGET_BLOCKERS, BRANCH_BLOCKERS),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], points: list[dict[str, Any]], overlay: dict[str, Any]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values()) and CURVE_FIGURE.exists() and RENDER_PNG.exists()
    points_written = VISUAL_POINTS.exists() and len(read_csv(VISUAL_POINTS)) == len(points)
    points_nonclaim = visual_points_flags_false()
    alpha1_anchor = any(row["point_source"] == "source_text_alpha1_threshold_anchor" and abs(float(row["lambda_value"]) - 3.86e-5) < 1e-10 and abs(float(row["alpha_bound_abs"]) - 1.0) < 1e-12 for row in points)
    overlay_ok = OVERLAY_PNG.exists() and OVERLAY_PNG.stat().st_size > 10_000
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_SELECTION, QUAR_POINTS, QUAR_QUALITY, QUAR_BLOCKERS, BRANCH_SELECTION, BRANCH_POINTS, BRANCH_QUALITY, BRANCH_BLOCKERS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1499_0_local_sources", source_paths_exist, "all cited 1498/source render paths exist"),
        ("VAL1499_1_points_written", points_written, f"visual point rows={len(points)}"),
        ("VAL1499_2_points_nonclaim", points_nonclaim, "visual point file remains nonclaim"),
        ("VAL1499_3_alpha1_anchor", alpha1_anchor, "38.6um alpha=1 anchor present"),
        ("VAL1499_4_overlay", overlay_ok, f"overlay path={overlay['overlay_png']}"),
        ("VAL1499_5_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1499_6_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1499_7_csv_parse", csv_parse_ok, "all generated 1499 CSVs parse cleanly"),
        ("VAL1499_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1499_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1499_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1499_11_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1499_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1499 wrote approximate nonclaim EotWash 2020 alpha(lambda) samples and kept R10 scoring blocked"
            if overall
            else "1499 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(selection: list[dict[str, Any]], points: list[dict[str, Any]], overlay: dict[str, Any], quality: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1499 - Isolate EotWash 2020 Curve and Sample Nonclaim alpha(lambda) Points",
                "",
                "## Verdict",
                "- A rough Eot-Wash 2020 `|alpha|(lambda)` candidate was sampled from the 1498 rendered R10 figure.",
                "- The `38.6 um, alpha=1` source-text threshold is included as an anchor, but all rows remain nonclaim.",
                "- No live R10 curve or MTS/R10 score is promoted; the projection kernel is still missing.",
                "",
                "## Curve Selection",
                md_table(selection, ["selection_id", "curve_identity", "selection_status", "review_requirement"]),
                "",
                "## Nonclaim Point Preview",
                md_table(points, ["point_id", "lambda_value", "lambda_units", "alpha_bound_abs", "point_source", "promotion_status"]),
                "",
                "## Overlay",
                md_table([overlay], ["overlay_id", "overlay_png", "overlay_status"]),
                "",
                "## Quality Ledger",
                md_table(quality, ["quality_id", "object", "status", "detail"]),
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
    points = point_rows()
    selection = selection_rows()
    write_visual_points(points)
    overlay = render_overlay(points)
    quality = quality_rows(points)
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {"same_parent_branch_id": BRANCH_ID, "local_status_id": "LRS1499_0", "object": "R10 visual curve samples", "status": "NONCLAIM_APPROXIMATE_POINTS_STAGED", "effect": "empirical route improved, no R10/local claim", **flags()}
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = [
        {"same_parent_branch_id": BRANCH_ID, "decision_id": "DEC1499_0", "decision": "stage approximate Eot-Wash 2020 points as visual nonclaim only", "rationale": "useful for kernel development but not acceptable as live bound curve", **flags()}
    ]
    next_rows = next_target_rows()

    write_csv(CURVE_SELECTION, selection)
    write_csv(NONCLAIM_POINTS, points)
    write_csv(OVERLAY_LEDGER, [overlay])
    write_csv(POINT_QUALITY, quality)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        CURVE_SELECTION,
        NONCLAIM_POINTS,
        OVERLAY_LEDGER,
        POINT_QUALITY,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, points, overlay)
    write_csv(VALIDATION, validation)
    write_doc(selection, points, overlay, quality, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
