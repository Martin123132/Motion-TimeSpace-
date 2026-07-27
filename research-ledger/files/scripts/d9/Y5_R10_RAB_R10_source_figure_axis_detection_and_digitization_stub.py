from __future__ import annotations

import csv
import hashlib
import re
import shutil
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
DOC = ROOT / "1496-Y5-R10-RAB-R10-source-figure-axis-detection-and-digitization-stub.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1495_validation": OUT / "P8_Y5_BRR545_1495_VALIDATION.csv",
    "1495_manifest": OUT / "P8_Y5_R10_1495_R10_SOURCE_ARCHIVE_FILE_MANIFEST.csv",
    "1495_figures": OUT / "P8_Y5_R10_1495_R10_FIGURE_DIGITIZATION_TARGETS.csv",
    "1495_curve_status": OUT / "P8_Y5_R10_1495_R10_ALPHA_LAMBDA_CURVE_STATUS.csv",
    "1495_kernel_contract": OUT / "P8_Y5_R10_1495_DELTA_W_KERNEL_INPUT_CONTRACT.csv",
    "1495_next": OUT / "P8_Y5_R10_1495_NEXT_TARGET.csv",
}

SOURCE_TEX = R10 / "raw" / "Lee_2020_PRL_2002.11761_source_1495" / "FB_ISL_pdf.tex"
SOURCE_DIR = SOURCE_TEX.parent
CURVE_FIGURE = SOURCE_DIR / "fig5b1.pdf"
TORQUE_FIGURE = SOURCE_DIR / "fig5a.pdf"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
STAGING_DIR = R10 / "derived" / "staging"
TEMPLATE_PATH = STAGING_DIR / "R10_alpha_lambda_bound_curve_DIGITIZATION_TEMPLATE_1496.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

FIGURE_CAPTION_MAP = OUT / "P8_Y5_R10_1496_FIGURE_CAPTION_MAP.csv"
CURVE_TARGET_SELECTION = OUT / "P8_Y5_R10_1496_R10_CURVE_TARGET_SELECTION.csv"
AXIS_DETECTION_GATE = OUT / "P8_Y5_R10_1496_AXIS_DETECTION_GATE.csv"
DIGITIZATION_TEMPLATE_STATUS = OUT / "P8_Y5_R10_1496_DIGITIZATION_TEMPLATE_STATUS.csv"
KERNEL_CONTRACT_REFRESH = OUT / "P8_Y5_R10_1496_KERNEL_CONTRACT_REFRESH.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1496_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1496_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1496_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1496_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1496_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1496_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1496_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1496_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1496"
QUAR_CAPTIONS = QUARANTINE / "FIGURE_CAPTION_MAP_NONCLAIM.csv"
QUAR_SELECTION = QUARANTINE / "R10_CURVE_TARGET_SELECTION_NONCLAIM.csv"
QUAR_AXIS = QUARANTINE / "AXIS_DETECTION_GATE_NONCLAIM.csv"
QUAR_TEMPLATE = QUARANTINE / "DIGITIZATION_TEMPLATE_STATUS_NONCLAIM.csv"
BRANCH_CAPTIONS = BRANCH_RESIDUALS / "r10_figure_caption_map_nonclaim_1496.csv"
BRANCH_SELECTION = BRANCH_RESIDUALS / "r10_curve_target_selection_nonclaim_1496.csv"
BRANCH_AXIS = BRANCH_RESIDUALS / "r10_axis_detection_gate_nonclaim_1496.csv"
BRANCH_TEMPLATE = BRANCH_RESIDUALS / "r10_digitization_template_status_nonclaim_1496.csv"


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


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def balanced_brace_content(text: str, command: str) -> str:
    start = text.find(command)
    if start < 0:
        return ""
    brace_start = text.find("{", start)
    if brace_start < 0:
        return ""
    depth = 0
    for index in range(brace_start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start + 1 : index]
    return ""


def clean_tex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(?:bf|textbf|em|ref|cite|label)\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("$", "").replace("~", " ")
    text = text.replace("\\%", "%").replace("\\alpha", "alpha").replace("\\lambda", "lambda")
    return re.sub(r"\s+", " ", text).strip()


def figure_blocks() -> list[str]:
    text = read_text(SOURCE_TEX)
    return re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", text, flags=re.DOTALL)


def caption_map_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for block_index, block in enumerate(figure_blocks()):
        includes = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}", block)
        caption_raw = balanced_brace_content(block, r"\caption")
        caption = clean_tex(caption_raw)
        label = balanced_brace_content(block, r"\label")
        for include_index, include in enumerate(includes):
            graphic_path = SOURCE_DIR / include
            name = graphic_path.name
            if label == "fig5" and name == "fig5b1.pdf":
                role = "R10_ALPHA_LAMBDA_LIMIT_CURVE_TARGET"
                selection = "SELECTED_CURVE_DIGITIZATION_TARGET_NONCLAIM"
            elif label == "fig5" and name == "fig5a.pdf":
                role = "R10_TORQUE_DATA_CONTEXT"
                selection = "CONTEXT_NOT_BOUND_CURVE"
            elif "upper limits" in caption.lower() and "alpha" in caption.lower():
                role = "R10_LIMIT_FIGURE_REVIEW_REQUIRED"
                selection = "POSSIBLE_CURVE_CONTEXT_REVIEW"
            else:
                role = "NON_CURVE_SUPPORT_FIGURE"
                selection = "NOT_SELECTED_FOR_ALPHA_LAMBDA_CURVE"
            rows.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "figure_map_id": f"FCM1496_{block_index}_{include_index}",
                    "figure_label": label,
                    "include_order": include_index,
                    "graphic_path": rel(graphic_path),
                    "graphic_exists": graphic_path.exists(),
                    "graphic_sha256": file_sha256(graphic_path) if graphic_path.exists() else "",
                    "caption_role": role,
                    "selection_status": selection,
                    "caption_excerpt_for_review": caption[:220],
                    **flags(),
                }
            )
    return rows


def selected_curve_rows(caption_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [row for row in caption_rows if row["selection_status"] == "SELECTED_CURVE_DIGITIZATION_TARGET_NONCLAIM"]
    if not selected:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "selection_id": "SEL1496_no_curve_target",
                "curve_figure_path": rel(CURVE_FIGURE),
                "selection_status": "CURVE_TARGET_NOT_IDENTIFIED_BLOCKED",
                "curve_target_path": rel(CURVE_TARGET),
                "reason": "no caption-mapped figure matched fig5 bottom alpha limit curve",
                **flags(),
            }
        ]
    row = selected[0]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "selection_id": "SEL1496_0_fig5b1",
            "curve_figure_path": row["graphic_path"],
            "selection_status": "CURVE_TARGET_IDENTIFIED_NONCLAIM",
            "curve_target_path": rel(CURVE_TARGET),
            "reason": "TeX caption maps fig5b1.pdf to the bottom plot: 95% confidence upper limits on |alpha|",
            **flags(),
        }
    ]


def figure_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return " ".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return ""


def axis_gate_rows(selection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = selection_rows[0]["selection_status"] == "CURVE_TARGET_IDENTIFIED_NONCLAIM"
    text = figure_pdf_text(CURVE_FIGURE) if selected and CURVE_FIGURE.exists() else ""
    text_norm = re.sub(r"\s+", " ", text.replace("\u03bc", "um").replace("\u00b5", "um")).strip()
    axis_text_status = "FIGURE_TEXT_EXTRACTED_REVIEW_REQUIRED" if text_norm else "FIGURE_AXIS_TEXT_NOT_EXTRACTABLE_MANUAL_CALIBRATION_REQUIRED"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_gate_id": "AXIS1496_0_x",
            "curve_figure_path": rel(CURVE_FIGURE),
            "axis": "x",
            "expected_quantity": "lambda",
            "expected_units": "length, preferably um or m with conversion recorded",
            "scale_requirement": "verify whether log scale before digitization",
            "auto_axis_text_status": axis_text_status,
            "extracted_text_preview": text_norm[:120],
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_gate_id": "AXIS1496_1_y",
            "curve_figure_path": rel(CURVE_FIGURE),
            "axis": "y",
            "expected_quantity": "absolute Yukawa strength |alpha|",
            "expected_units": "dimensionless",
            "scale_requirement": "verify whether log scale before digitization",
            "auto_axis_text_status": axis_text_status,
            "extracted_text_preview": text_norm[:120],
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "axis_gate_id": "AXIS1496_2_confidence",
            "curve_figure_path": rel(CURVE_FIGURE),
            "axis": "curve",
            "expected_quantity": "95 percent upper limit",
            "expected_units": "confidence convention/source caption",
            "scale_requirement": "record whether curve is |alpha|, +alpha, or -alpha; 1496 only selects |alpha| caption target",
            "auto_axis_text_status": axis_text_status,
            "extracted_text_preview": text_norm[:120],
            **flags(),
        },
    ]


def write_digitization_template() -> list[dict[str, Any]]:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "template_row_id": "TEMPLATE1496_placeholder",
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound_abs": "",
            "alpha_sign_convention": "abs_alpha_from_fig5_bottom_caption",
            "confidence": "95_percent",
            "curve_source": "R10_2020_PRL_fig5b1",
            "figure_file": rel(CURVE_FIGURE),
            "source_caption_label": "fig5",
            "digitization_method": "MISSING_MANUAL_OR_RENDERED_DIGITIZATION",
            "axis_x_scale": "MISSING_VERIFY_LOG_OR_LINEAR",
            "axis_y_scale": "MISSING_VERIFY_LOG_OR_LINEAR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "template only; no curve points supplied in 1496",
        }
    ]
    write_csv(TEMPLATE_PATH, rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": "DT1496_0_template",
            "template_path": rel(TEMPLATE_PATH),
            "template_exists": TEMPLATE_PATH.exists(),
            "curve_target_path": rel(CURVE_TARGET),
            "live_curve_target_exists": CURVE_TARGET.exists(),
            "template_status": "NONCLAIM_TEMPLATE_WRITTEN_NO_POINTS",
            "required_before_promotion": "replace placeholder with digitized positive numeric lambda/alpha rows, source figure, method, units, and validation",
            **flags(),
        }
    ]


def kernel_rows() -> list[dict[str, Any]]:
    inputs = [
        ("KERN1496_0_curve", "digitized R10 |alpha|(lambda) upper-limit curve", rel(CURVE_TARGET), "MISSING_LIVE_TARGET"),
        ("KERN1496_1_axis", "axis calibration and log/linear convention for fig5b1", rel(AXIS_DETECTION_GATE), "MANUAL_CALIBRATION_REQUIRED"),
        ("KERN1496_2_geometry", "R10 geometry response kernel", "source-intake/r10/derived/R10_geometry_response_kernel.csv", "MISSING"),
        ("KERN1496_3_basis", "delta_w component basis and units", "source-intake/mts_residuals/P8_Y5_R10_delta_w_basis_contract.csv", "MISSING"),
        ("KERN1496_4_mapping", "delta_w to Yukawa alpha mapping", rel(KERNEL_TARGET), "MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_input_id": input_id,
            "required_input": required_input,
            "target_path": path,
            "current_status": status,
            "failure_effect": "R10 score remains blocked",
            **flags(),
        }
        for input_id, required_input, path, status in inputs
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1496_0_no_points",
            "blocking_marker": "DIGITIZED_POINTS_MISSING",
            "reason": "1496 identifies fig5b1 and writes a template but does not digitize curve points",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1496_1_axis",
            "blocking_marker": "AXIS_CALIBRATION_MANUAL",
            "reason": "figure axis text is not reliably extractable from fig5b1.pdf; scale must be manually/render-verified",
            "target_path": rel(CURVE_FIGURE),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1496_2_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "digitized bound curve still needs same-branch projection kernel before any MTS score",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": f"READY1496_{index}_{row['blocker_id']}",
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
            "refusal_id": "CP1496_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "figure target selection cannot derive parent coupling normalization",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1496_0_curve_target",
            "target": "R10 alpha(lambda) source figure",
            "current_status": "FIG5B1_IDENTIFIED_TEMPLATE_ONLY",
            "claim_effect": "digitization route sharpened; no score/pass claim",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "LRS1496_1_local_GR",
            "target": "local GR/Newton reduction",
            "current_status": "NOT_CLOSED",
            "claim_effect": "no local-GR/Newton claim from figure selection",
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    reasons = [
        ("REJ1496_0_points", "DIGITIZED_POINTS_MISSING", "curve target is identified but no numeric alpha(lambda) rows exist"),
        ("REJ1496_1_axis", "AXIS_CALIBRATION_MISSING", "manual/render axis calibration is required"),
        ("REJ1496_2_kernel", "PROJECTION_KERNEL_MISSING", "delta_w-to-alpha kernel is still absent"),
        ("REJ1496_3_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "source figure does not derive coupling coefficients"),
        ("REJ1496_4_claim", "CLAIM_PROMOTION_FORBIDDEN", "no R10/local-GR/Newton pass may be claimed"),
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
            "decision_id": "DEC1496_0_target",
            "decision": "select fig5b1.pdf as the R10 |alpha|(lambda) curve target",
            "rationale": "TeX caption maps fig5 bottom plot to 95 percent upper limits on |alpha|",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1496_1_no_points",
            "decision": "write a digitization template but no curve points",
            "rationale": "axis calibration is not machine-readable from the figure asset in this pass",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1496_0_1497",
            "next_target": "1497-Y5-R10-RAB-R10-fig5b1-axis-calibration-and-nonclaim-point-digitization.md",
            "script": "scripts/Y5_R10_RAB_R10_fig5b1_axis_calibration_and_nonclaim_point_digitization.py",
            "objective": "render or manually calibrate fig5b1 axes, fill nonclaim alpha(lambda) point rows, and keep the R10 score blocked until the projection kernel exists",
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


def template_flags_false() -> bool:
    for row in read_csv(TEMPLATE_PATH):
        if row.get("valid_for_claim") not in ("False", "false", False) or row.get("claim_allowed") not in ("False", "false", False):
            return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (FIGURE_CAPTION_MAP, QUAR_CAPTIONS),
        (CURVE_TARGET_SELECTION, QUAR_SELECTION),
        (AXIS_DETECTION_GATE, QUAR_AXIS),
        (DIGITIZATION_TEMPLATE_STATUS, QUAR_TEMPLATE),
        (FIGURE_CAPTION_MAP, BRANCH_CAPTIONS),
        (CURVE_TARGET_SELECTION, BRANCH_SELECTION),
        (AXIS_DETECTION_GATE, BRANCH_AXIS),
        (DIGITIZATION_TEMPLATE_STATUS, BRANCH_TEMPLATE),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], caption_rows: list[dict[str, Any]], selection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values()) and SOURCE_TEX.exists() and CURVE_FIGURE.exists()
    fig5b1_selected = any(row["graphic_path"].endswith("fig5b1.pdf") and row["selection_status"] == "SELECTED_CURVE_DIGITIZATION_TARGET_NONCLAIM" for row in caption_rows)
    selection_ok = selection_rows[0]["selection_status"] == "CURVE_TARGET_IDENTIFIED_NONCLAIM"
    template_ok = TEMPLATE_PATH.exists() and template_flags_false()
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_CAPTIONS, QUAR_SELECTION, QUAR_AXIS, QUAR_TEMPLATE, BRANCH_CAPTIONS, BRANCH_SELECTION, BRANCH_AXIS, BRANCH_TEMPLATE])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    readiness_nonclaim = all(row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in read_csv(SCORE_READINESS))
    checks = [
        ("VAL1496_0_local_sources", source_paths_exist, "all cited 1495/source figure paths exist"),
        ("VAL1496_1_fig5b1_selected", fig5b1_selected, "fig5b1 selected from TeX caption map"),
        ("VAL1496_2_selection_row", selection_ok, "curve target selection row is explicit"),
        ("VAL1496_3_template", template_ok, "digitization template exists and remains nonclaim"),
        ("VAL1496_4_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1496_5_readiness_blocked", readiness_nonclaim, "delta_w/R10 readiness remains false"),
        ("VAL1496_6_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1496_7_csv_parse", csv_parse_ok, "all generated 1496 CSVs parse cleanly"),
        ("VAL1496_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1496_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1496_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1496_11_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
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
            "check_id": "VAL1496_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1496 identified R10 fig5b1 curve target and wrote a nonclaim digitization template"
            if overall
            else "1496 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(caption_rows: list[dict[str, Any]], selection_rows: list[dict[str, Any]], axis_rows: list[dict[str, Any]], template_rows: list[dict[str, Any]], kernel: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    selected_or_fig5 = [row for row in caption_rows if row["figure_label"] == "fig5" or "CURVE" in row["caption_role"]]
    DOC.write_text(
        "\n".join(
            [
                "# 1496 - R10 Source Figure Axis Detection and Digitization Stub",
                "",
                "## Verdict",
                "- `fig5b1.pdf` is selected as the R10 `|alpha|(lambda)` source-figure target from the paper TeX caption map.",
                "- A nonclaim digitization template was written, but no numeric curve points were fabricated or promoted.",
                "- R10 remains blocked until axes are calibrated, curve points are digitized, and the `delta_w -> alpha(lambda)` kernel exists.",
                "",
                "## Figure Caption Map: Selected Context",
                md_table(selected_or_fig5, ["figure_map_id", "figure_label", "graphic_path", "caption_role", "selection_status"]),
                "",
                "## Curve Target Selection",
                md_table(selection_rows, ["selection_id", "curve_figure_path", "selection_status", "curve_target_path", "reason"]),
                "",
                "## Axis Detection Gate",
                md_table(axis_rows, ["axis_gate_id", "axis", "expected_quantity", "scale_requirement", "auto_axis_text_status"]),
                "",
                "## Digitization Template Status",
                md_table(template_rows, ["template_id", "template_path", "template_status", "required_before_promotion"]),
                "",
                "## Kernel Contract Refresh",
                md_table(kernel, ["kernel_input_id", "required_input", "current_status", "failure_effect"]),
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
    caption_rows = caption_map_rows()
    selection_rows = selected_curve_rows(caption_rows)
    axis_rows = axis_gate_rows(selection_rows)
    template_rows = write_digitization_template()
    kernel = kernel_rows()
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    c_parent_rows = c_parent_refusal_rows()
    local_rows = local_status_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(FIGURE_CAPTION_MAP, caption_rows)
    write_csv(CURVE_TARGET_SELECTION, selection_rows)
    write_csv(AXIS_DETECTION_GATE, axis_rows)
    write_csv(DIGITIZATION_TEMPLATE_STATUS, template_rows)
    write_csv(KERNEL_CONTRACT_REFRESH, kernel)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent_rows)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        FIGURE_CAPTION_MAP,
        CURVE_TARGET_SELECTION,
        AXIS_DETECTION_GATE,
        DIGITIZATION_TEMPLATE_STATUS,
        KERNEL_CONTRACT_REFRESH,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, caption_rows, selection_rows)
    write_csv(VALIDATION, validation)
    generated_csvs.append(VALIDATION)
    write_doc(caption_rows, selection_rows, axis_rows, template_rows, kernel, validation, next_rows)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
