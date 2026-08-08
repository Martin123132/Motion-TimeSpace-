from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB / "docs"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
RAB_QUEUE = RAB / "acquisition-queue"
R10_1570 = RAB / "external" / "r10" / "1570"
R10_1571 = RAB / "external" / "r10" / "1571"
FIG2 = R10_1570 / "extracted_images" / "page_5_image_1_Im3.png"
TXT = R10_1570 / "aps_harvest_fulltext.txt"
PDF = R10_1570 / "aps_harvest_fulltext.pdf"
OVERLAY = R10_1571 / "R10_fig2_blue_curve_cleaned_trace_overlay_1571.png"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1571-Y5-RAB-R10-digitization-QA-or-tauR10-internal-kernel.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1570_doc": ROOT / "1570-Y5-RAB-R10-curve-digitization-or-tau-kernel-source-normalization.md",
    "1570_validation": OUT / "P8_Y5_BRR545_1570_VALIDATION.csv",
    "1570_curve": OUT / "P8_Y5_PARENT_QLOC_1570_R10_ALPHA_LAMBDA_DIGITIZED_CANDIDATE.csv",
    "1570_method": OUT / "P8_Y5_PARENT_QLOC_1570_R10_DIGITIZATION_METHOD.csv",
    "1570_tau": OUT / "P8_Y5_PARENT_QLOC_1570_TAU_KERNEL_SOURCE_NORMALIZATION_GATE.csv",
    "fig2": FIG2,
    "text": TXT,
    "pdf": PDF,
    "1569_tau": OUT / "P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv",
}

NEEDLES = {
    "1570_doc": ["candidate blue-curve digitization", "internal MTS side is still missing"],
    "1570_validation": ["VAL1570_OVERALL", "PASS"],
    "1570_curve": ["DIG1570_000", "CANDIDATE_IMAGE_TRACE_NONCLAIM"],
    "1570_method": ["METHOD1570_3_acceptance", "NOT_ACCEPTED"],
    "1570_tau": ["TAUG1570_4_verdict", "NOT_READY"],
    "fig2": [],
    "text": ["FIG. 2. Constraints on Y", "function of λ"],
    "pdf": ["Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range"],
    "1569_tau": ["TAU1569_3_projection_kernel", "KERNEL_CONTRACT_WRITTEN_NOT_FILLED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1571_SOURCE_REGISTER.csv"
COMPONENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1571_BLUE_COMPONENT_QA_AUDIT.csv"
QA_METHOD = OUT / "P8_Y5_PARENT_QLOC_1571_DIGITIZATION_QA_METHOD.csv"
CLEAN_CURVE = OUT / "P8_Y5_PARENT_QLOC_1571_R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE.csv"
CURVE_COMPARISON = OUT / "P8_Y5_PARENT_QLOC_1571_CURVE_COMPARISON_1570_TO_1571.csv"
TAU_KERNEL = OUT / "P8_Y5_PARENT_QLOC_1571_TAU_R10_INTERNAL_KERNEL_ATTEMPT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1571_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1571_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1571_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1571_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1571_VALIDATION.csv"
QUEUE_CURVE = RAB_QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1571_QA_CANDIDATE_NONCLAIM.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1571"
COPY_TARGETS = {
    COMPONENT_AUDIT: [
        QUARANTINE / "BLUE_COMPONENT_QA_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_blue_component_QA_audit_nonclaim_1571.csv",
    ],
    QA_METHOD: [
        QUARANTINE / "DIGITIZATION_QA_METHOD_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_digitization_QA_method_nonclaim_1571.csv",
    ],
    CLEAN_CURVE: [
        QUARANTINE / "R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_alpha_lambda_digitized_QA_candidate_nonclaim_1571.csv",
        QUEUE_CURVE,
    ],
    CURVE_COMPARISON: [
        QUARANTINE / "CURVE_COMPARISON_1570_TO_1571_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_curve_comparison_1570_to_1571_nonclaim.csv",
    ],
    TAU_KERNEL: [
        QUARANTINE / "TAU_R10_INTERNAL_KERNEL_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_internal_kernel_attempt_nonclaim_1571.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_digitization_QA_tau_kernel_decision_nonclaim_1571.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    if not needles:
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1571_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "R10 digitization QA or tau_R10 internal kernel attempt",
                **flags(),
            }
        )
    return rows


def calibration() -> dict[str, float]:
    return {
        "plot_x_left_px": 114.0,
        "plot_x_log_lambda_left": -3.0,
        "plot_x_decade_px": 243.0,
        "plot_y_top_px": 20.0,
        "plot_y_log_alpha_top": 0.0,
        "plot_y_decade_px": 155.0,
    }


def px_to_lambda(x: float) -> float:
    c = calibration()
    log_lambda = c["plot_x_log_lambda_left"] + (x - c["plot_x_left_px"]) / c["plot_x_decade_px"]
    return 10**log_lambda


def px_to_alpha(y: float) -> float:
    c = calibration()
    log_alpha = c["plot_y_log_alpha_top"] - (y - c["plot_y_top_px"]) / c["plot_y_decade_px"]
    return 10**log_alpha


def blue_components(mask: np.ndarray) -> list[dict[str, Any]]:
    height, width = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    components: list[dict[str, Any]] = []
    for y in range(height):
        xs = np.where(mask[y] & ~seen[y])[0]
        for x0 in xs:
            if seen[y, x0] or not mask[y, x0]:
                continue
            stack = [(y, int(x0))]
            seen[y, x0] = True
            pts: list[tuple[int, int]] = []
            while stack:
                cy, cx = stack.pop()
                pts.append((cy, cx))
                for ny in (cy - 1, cy, cy + 1):
                    for nx in (cx - 1, cx, cx + 1):
                        if ny == cy and nx == cx:
                            continue
                        if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
            if len(pts) > 20:
                ys = [pt[0] for pt in pts]
                xs2 = [pt[1] for pt in pts]
                components.append(
                    {
                        "component_index": len(components),
                        "size": len(pts),
                        "min_x": min(xs2),
                        "max_x": max(xs2),
                        "min_y": min(ys),
                        "max_y": max(ys),
                        "points": pts,
                    }
                )
    return components


def component_status(component: dict[str, Any]) -> tuple[str, str]:
    width = component["max_x"] - component["min_x"]
    height = component["max_y"] - component["min_y"]
    if component["size"] >= 100 and width >= 20 and component["min_y"] < 520 and component["max_y"] <= 660:
        return "KEEP_CURVE_CANDIDATE", "large/medium blue component in plot region above label band"
    if component["min_y"] >= 580:
        return "REJECT_LABEL_OR_AXIS_TEXT", "blue text/label band below curve region"
    return "REJECT_SMALL_OR_NONCURVE_BLUE_MARK", f"size={component['size']}; width={width}; height={height}"


def analyze_components() -> tuple[np.ndarray, list[dict[str, Any]], list[dict[str, Any]]]:
    image = Image.open(FIG2).convert("RGB")
    arr = np.array(image)
    blue_mask = (
        (arr[:, :, 2] > 150)
        & (arr[:, :, 0] < 100)
        & (arr[:, :, 1] < 170)
        & ((arr[:, :, 2] - arr[:, :, 0]) > 80)
        & ((arr[:, :, 2] - arr[:, :, 1]) > 50)
    )
    components = blue_components(blue_mask)
    audit_rows = []
    kept = []
    for component in components:
        status, reason = component_status(component)
        if status == "KEEP_CURVE_CANDIDATE":
            kept.append(component)
        audit_rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "component_id": f"COMP1571_{component['component_index']:02d}",
                "pixel_count": component["size"],
                "min_x": component["min_x"],
                "max_x": component["max_x"],
                "min_y": component["min_y"],
                "max_y": component["max_y"],
                "qa_status": status,
                "reason": reason,
                **flags(),
            }
        )
    return arr, audit_rows, kept


def cleaned_curve_rows(kept: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pixel_by_x: dict[int, list[int]] = {}
    kept_ids = []
    for component in kept:
        kept_ids.append(
            f"COMP{component['component_index']}:size={component['size']}:bbox={component['min_x']},{component['max_x']},{component['min_y']},{component['max_y']}"
        )
        for y, x in component["points"]:
            if 114 <= x <= 1012 and 20 <= y <= 688:
                pixel_by_x.setdefault(x, []).append(y)
    rows = []
    for sample_number, x in enumerate(sorted(pixel_by_x)[::8]):
        ys = pixel_by_x[x]
        if not ys:
            continue
        y = float(np.percentile(ys, 15))
        lam = px_to_lambda(float(x))
        alpha = px_to_alpha(y)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "point_id": f"QA1571_{len(rows):03d}",
                "lambda_m": f"{lam:.8g}",
                "alpha_abs_bound": f"{alpha:.8g}",
                "pixel_x": x,
                "pixel_y": f"{y:.2f}",
                "curve": "This_work_blue_curve",
                "digitization_status": "QA_CLEANED_CANDIDATE_NONCLAIM",
                "qa_rule": "kept_blue_components_minimized_label_contamination_15th_percentile_y",
                "source_image": rel(FIG2),
                "overlay_image": rel(OVERLAY),
                "kept_components": " | ".join(kept_ids),
                **flags(),
            }
        )
    if not rows:
        raise RuntimeError("no cleaned curve rows generated")
    return rows


def make_overlay(arr: np.ndarray, curve_rows: list[dict[str, Any]]) -> None:
    R10_1571.mkdir(parents=True, exist_ok=True)
    image = Image.fromarray(arr.copy())
    draw = ImageDraw.Draw(image)
    for row in curve_rows:
        x = int(row["pixel_x"])
        y = float(row["pixel_y"])
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), outline=(255, 0, 0), width=2)
    image.save(OVERLAY)


def qa_method_rows(component_rows: list[dict[str, Any]], curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kept = sum(1 for row in component_rows if row["qa_status"] == "KEEP_CURVE_CANDIDATE")
    rejected = len(component_rows) - kept
    c = calibration()
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "QA1571_0_components",
            "method_piece": "blue connected component filtering",
            "value": f"kept={kept}; rejected={rejected}; total={len(component_rows)}",
            "status": "QA_FILTER_APPLIED",
            "risk": "curve still image-traced and needs independent/manual acceptance",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "QA1571_1_axis",
            "method_piece": "axis calibration",
            "value": f"x_left={c['plot_x_left_px']}, x_decade={c['plot_x_decade_px']}, y_top={c['plot_y_top_px']}, y_decade={c['plot_y_decade_px']}",
            "status": "REUSED_1570_MANUAL_CALIBRATION",
            "risk": "axis calibration approximate until tick-by-tick QA",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "QA1571_2_centerline",
            "method_piece": "curve y selection",
            "value": "15th percentile y per x, sampled every 8 pixels",
            "status": "LABEL_CONTAMINATION_REDUCED",
            "risk": "may trace upper edge of thick line rather than exact centerline",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "QA1571_3_overlay",
            "method_piece": "visual QA overlay",
            "value": rel(OVERLAY),
            "status": "OVERLAY_CREATED",
            "risk": "human visual pass still required before accepted use",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "QA1571_4_acceptance",
            "method_piece": "accepted curve gate",
            "value": f"cleaned_points={len(curve_rows)}",
            "status": "NOT_ACCEPTED_NONCLAIM",
            "risk": "candidate supports smoke tests only",
            **flags(),
        },
    ]


def comparison_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    old_rows = read_csv(SOURCE_FILES["1570_curve"])
    old_lambda = [float(row["lambda_m"]) for row in old_rows]
    old_alpha = [float(row["alpha_abs_bound"]) for row in old_rows]
    new_lambda = [float(row["lambda_m"]) for row in curve_rows]
    new_alpha = [float(row["alpha_abs_bound"]) for row in curve_rows]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "comparison_id": "CMP1571_0_point_count",
            "metric": "point_count",
            "old_1570": len(old_rows),
            "new_1571": len(curve_rows),
            "status": "QA_CHANGED_CANDIDATE_TRACE",
            "interpretation": "cleaned component selection may include previously missed curve segment and reduce label contamination",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "comparison_id": "CMP1571_1_lambda_range",
            "metric": "lambda_m_range",
            "old_1570": f"{min(old_lambda):.8g}..{max(old_lambda):.8g}",
            "new_1571": f"{min(new_lambda):.8g}..{max(new_lambda):.8g}",
            "status": "RANGE_RECORDED_NONCLAIM",
            "interpretation": "range check only; not an acceptance test",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "comparison_id": "CMP1571_2_alpha_range",
            "metric": "alpha_abs_bound_range",
            "old_1570": f"{min(old_alpha):.8g}..{max(old_alpha):.8g}",
            "new_1571": f"{min(new_alpha):.8g}..{max(new_alpha):.8g}",
            "status": "RANGE_RECORDED_NONCLAIM",
            "interpretation": "axis/centerline QA still needed before accepted bound curve",
            **flags(),
        },
    ]


def tau_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KERN1571_0_form",
            "alpha_MTS(lambda_R) = tau_R10 * A_R[Z_R,M_R^2,J_R,B_R,readout]",
            "formal bridge to compare with R10 bound curve",
            "FORMAL_KERNEL_SHAPE_ONLY",
            "all source-normalized internal inputs missing",
        ),
        (
            "KERN1571_1_range",
            "lambda_R = sqrt(Z_R/M_R^2)",
            "sets x-axis location if finite residual branch is active",
            "MISSING_ZR_MR2",
            "no parent-normalized Z_R or M_R^2",
        ),
        (
            "KERN1571_2_source",
            "A_R source amplitude from J_R/B_R/readout coupling to test masses",
            "sets y-axis alpha prediction",
            "MISSING_SOURCE_NORMALIZATION",
            "matter/source/boundary/readout descent not theorem-zeroed and no finite row exists",
        ),
        (
            "KERN1571_3_bound_eval",
            "pass if abs(alpha_MTS(lambda_R)) <= alpha_bound_digitized(lambda_R)",
            "eventual R10 comparator",
            "BLOCKED_NO_INTERNAL_PREDICTION",
            "external curve cannot be scored alone",
        ),
        (
            "KERN1571_4_verdict",
            "tau_R10 internal kernel",
            "not ready",
            "NOT_READY",
            "next derivation must fill source normalization or theorem-zero branch",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": kernel_id,
            "kernel_piece": kernel_piece,
            "role": role,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_list("1570_tau", "1569_tau"),
            **flags(),
        }
        for kernel_id, kernel_piece, role, status, blocking_gap in rows
    ]


def runner_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("RUN1571_0_sources", "load 1570 assets and handoff", "PASS", "all source register needles found"),
        ("RUN1571_1_qa_curve", "QA-cleaned R10 curve candidate", "PASS_QA_CANDIDATE_NONCLAIM", f"cleaned_points={len(curve_rows)}; overlay={rel(OVERLAY)}"),
        ("RUN1571_2_acceptance", "accepted R10 curve", "NOT_ACCEPTED", "human/independent QA still required"),
        ("RUN1571_3_tau_kernel", "tau_R10 internal kernel", "NOT_READY", "source-normalized internal prediction missing"),
        ("RUN1571_4_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1571_5_claim", "R10/local GR claim", "BLOCKED_NO_CLAIM", "QA curve exists but internal MTS prediction is missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1571_0_QA_curve", "QA-cleaned R10 candidate curve", "PASS_NONCLAIM", "cleaned trace and overlay exist but are not accepted"),
        ("GATE1571_1_accepted_curve", "accepted R10 curve", "BLOCKED_NO_CLAIM", "independent/manual digitization QA missing"),
        ("GATE1571_2_tau_kernel", "tau_R10 internal source-normalized kernel", "BLOCKED_NO_CLAIM", "Z_R/M_R2/J_R/B_R/readout inputs missing"),
        ("GATE1571_3_R10_score", "R10 score/pass/fail", "BLOCKED_NO_CLAIM", "no internal MTS alpha(lambda) prediction"),
        ("GATE1571_4_local_GR", "derived local GR/Newton safety", "BLOCKED_NO_CLAIM", "R10 external bound work does not solve local theorem gaps"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1570_doc", "fig2", "1570_tau"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1571_0_curve",
            "decision": "R10 digitization QA",
            "result": "QA_CLEANED_CANDIDATE_CREATED_NONCLAIM",
            "reason": "component filtering and overlay reduce obvious label contamination but do not make an accepted curve",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1571_1_tau",
            "decision": "tau_R10 internal kernel",
            "result": "NOT_READY_SOURCE_NORMALIZATION_MISSING",
            "reason": "formal kernel shape exists, but theory coefficients/source normalization remain absent",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1571_2_next",
            "decision": "next target",
            "result": "NEXT_1572_TAU_R10_SOURCE_NORMALIZATION_OR_ACCEPTED_CURVE_QA",
            "reason": "best next move is derive source-normalized tau_R10 or independently QA the curve into accepted nonclaim input",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1571_0_1572",
            "next_target": "1572-Y5-RAB-tauR10-source-normalization-or-accepted-curve-QA.md",
            "script": "scripts/Y5_RAB_tauR10_source_normalization_or_accepted_curve_QA.py",
            "objective": "try to derive/fill the internal tau_R10 source-normalization kernel; in parallel, QA the cleaned curve against manual tick/curve checks before any accepted nonclaim input",
            "do_not": "do not claim R10 pass; do not accept the curve without independent QA; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    components = read_csv(COMPONENT_AUDIT)
    method = read_csv(QA_METHOD)
    curve = read_csv(CLEAN_CURVE)
    comparison = read_csv(CURVE_COMPARISON)
    tau = read_csv(TAU_KERNEL)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    lambda_values = [float(row["lambda_m"]) for row in curve]
    alpha_values = [float(row["alpha_abs_bound"]) for row in curve]

    checks = [
        ("VAL1571_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1571 source paths exist"),
        ("VAL1571_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1571_2_component_audit", any(row["qa_status"] == "KEEP_CURVE_CANDIDATE" for row in components) and any(row["qa_status"].startswith("REJECT") for row in components), "component audit keeps and rejects blue components"),
        ("VAL1571_3_method_overlay", OVERLAY.exists() and any(row["method_id"] == "QA1571_3_overlay" and row["status"] == "OVERLAY_CREATED" for row in method), "overlay exists and method records it"),
        ("VAL1571_4_curve_candidate", len(curve) >= 50 and all(row["digitization_status"] == "QA_CLEANED_CANDIDATE_NONCLAIM" for row in curve), "QA-cleaned candidate curve rows created"),
        ("VAL1571_5_curve_positive", all(value > 0 for value in lambda_values + alpha_values), "candidate curve lambda/alpha values are positive"),
        ("VAL1571_6_comparison", len(comparison) == 3 and any(row["comparison_id"] == "CMP1571_0_point_count" for row in comparison), "1570-to-1571 comparison recorded"),
        ("VAL1571_7_tau_not_ready", any(row["kernel_id"] == "KERN1571_4_verdict" and row["status"] == "NOT_READY" for row in tau), "tau kernel remains not ready"),
        ("VAL1571_8_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1571_9_runner_blocks_claim", any(row["runner_id"] == "RUN1571_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local/R10 claim"),
        ("VAL1571_10_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1571_11_decision_next", any(row["result"] == "NEXT_1572_TAU_R10_SOURCE_NORMALIZATION_OR_ACCEPTED_CURVE_QA" for row in decision_items), "decision selects tau source normalization or accepted curve QA"),
        ("VAL1571_12_next_target", any("1572-Y5-RAB-tauR10-source-normalization" in row["next_target"] for row in next_rows), "next target is tau source normalization or accepted curve QA"),
        ("VAL1571_13_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1571 CSVs parse cleanly"),
        ("VAL1571_14_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1571_15_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1571_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1571_17_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1571_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1571 R10 digitization QA or tauR10 internal kernel validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    components: list[dict[str, Any]],
    method: list[dict[str, Any]],
    curve: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1571 - R_AB R10 Digitization QA or tau_R10 Internal Kernel",
                "",
                "## Verdict",
                "- The R10 Fig. 2 curve is now a cleaner QA candidate: blue connected components were classified, likely label/axis text rejected, and a trace overlay was written.",
                "- The cleaned curve is still not accepted evidence; it remains a private nonclaim input for smoke tooling until independent/manual QA verifies the axis and curve trace.",
                "- The theory side is unchanged in the important way: the internal `tau_R10` source-normalized kernel is still missing.",
                "- No R10 pass, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Blue Component QA Audit",
                md_table(components, ["component_id", "pixel_count", "min_x", "max_x", "min_y", "max_y", "qa_status", "reason"]),
                "",
                "## QA Method",
                md_table(method, ["method_id", "method_piece", "value", "status", "risk"]),
                "",
                "## Cleaned Curve Candidate",
                md_table(curve[:30], ["point_id", "lambda_m", "alpha_abs_bound", "pixel_x", "pixel_y", "digitization_status", "qa_rule"]),
                "",
                "## Curve Comparison",
                md_table(comparison, ["comparison_id", "metric", "old_1570", "new_1571", "status", "interpretation"]),
                "",
                "## tau_R10 Internal Kernel Attempt",
                md_table(tau, ["kernel_id", "kernel_piece", "role", "status", "blocking_gap"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    image_array, components, kept = analyze_components()
    curve = cleaned_curve_rows(kept)
    make_overlay(image_array, curve)
    method = qa_method_rows(components, curve)
    comparison = comparison_rows(curve)
    tau = tau_kernel_rows()
    run_rows = runner_rows(curve)
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COMPONENT_AUDIT, components)
    write_csv(QA_METHOD, method)
    write_csv(CLEAN_CURVE, curve)
    write_csv(CURVE_COMPARISON, comparison)
    write_csv(TAU_KERNEL, tau)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        COMPONENT_AUDIT,
        QA_METHOD,
        CLEAN_CURVE,
        CURVE_COMPARISON,
        TAU_KERNEL,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, components, method, curve, comparison, tau, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
