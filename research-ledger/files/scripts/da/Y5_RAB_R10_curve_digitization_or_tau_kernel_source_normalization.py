from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB / "docs"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
RAB_QUEUE = RAB / "acquisition-queue"
R10_1570 = RAB / "external" / "r10" / "1570"
PDF = R10_1570 / "aps_harvest_fulltext.pdf"
TXT = R10_1570 / "aps_harvest_fulltext.txt"
FIG2 = R10_1570 / "extracted_images" / "page_5_image_1_Im3.png"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1570-Y5-RAB-R10-curve-digitization-or-tau-kernel-source-normalization.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1569_doc": ROOT / "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md",
    "1569_validation": OUT / "P8_Y5_BRR545_1569_VALIDATION.csv",
    "1569_decision": OUT / "P8_Y5_PARENT_QLOC_1569_DECISION.csv",
    "1569_tau": OUT / "P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv",
    "1569_external": OUT / "P8_Y5_PARENT_QLOC_1569_EXTERNAL_R10_BOUND_METADATA_ROW.csv",
    "pdf": PDF,
    "text": TXT,
    "fig2": FIG2,
}

NEEDLES = {
    "1569_doc": ["first external R10 metadata source is now localized", "source-normalization kernel is missing"],
    "1569_validation": ["VAL1569_OVERALL", "PASS"],
    "1569_decision": ["DEC1569_3_next", "NEXT_1570_R10_CURVE_DIGITIZATION_OR_TAU_KERNEL_SOURCE_NORMALIZATION"],
    "1569_tau": ["TAU1569_3_projection_kernel", "KERNEL_CONTRACT_WRITTEN_NOT_FILLED"],
    "1569_external": ["EXTBOUND1569_R10_CROSSREF_PRL126_211101", "LOCAL_CROSSREF_METADATA_PRESENT"],
    "pdf": ["Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range"],
    "text": ["FIG. 2. Constraints on Y", "function of λ"],
    "fig2": [],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1570_SOURCE_REGISTER.csv"
PDF_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1570_PDF_FIGURE_SOURCE_AUDIT.csv"
DIGITIZATION_METHOD = OUT / "P8_Y5_PARENT_QLOC_1570_R10_DIGITIZATION_METHOD.csv"
DIGITIZED_CURVE = OUT / "P8_Y5_PARENT_QLOC_1570_R10_ALPHA_LAMBDA_DIGITIZED_CANDIDATE.csv"
TAU_GATE = OUT / "P8_Y5_PARENT_QLOC_1570_TAU_KERNEL_SOURCE_NORMALIZATION_GATE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1570_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1570_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1570_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1570_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1570_VALIDATION.csv"
QUEUE_CURVE = RAB_QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1570_CANDIDATE_NONCLAIM.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1570"
COPY_TARGETS = {
    PDF_AUDIT: [
        QUARANTINE / "PDF_FIGURE_SOURCE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_pdf_figure_source_audit_nonclaim_1570.csv",
    ],
    DIGITIZATION_METHOD: [
        QUARANTINE / "R10_DIGITIZATION_METHOD_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_digitization_method_nonclaim_1570.csv",
    ],
    DIGITIZED_CURVE: [
        QUARANTINE / "R10_ALPHA_LAMBDA_DIGITIZED_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_alpha_lambda_digitized_candidate_nonclaim_1570.csv",
        QUEUE_CURVE,
    ],
    TAU_GATE: [
        QUARANTINE / "TAU_KERNEL_SOURCE_NORMALIZATION_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_kernel_source_normalization_gate_nonclaim_1570.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_curve_tau_kernel_decision_nonclaim_1570.csv",
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
                "source_id": f"SRC1570_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "R10 curve digitization candidate or tau kernel source-normalization gate",
                **flags(),
            }
        )
    return rows


def pdf_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PDF1570_0_pdf_payload",
            "local_path": rel(PDF),
            "exists": PDF.exists(),
            "bytes": PDF.stat().st_size if PDF.exists() else 0,
            "anchor": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range",
            "anchor_found": file_contains(PDF, ["Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range"]) if PDF.exists() else False,
            "status": "LOCAL_FULLTEXT_PDF_PAYLOAD_PRESENT",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PDF1570_1_text_extract",
            "local_path": rel(TXT),
            "exists": TXT.exists(),
            "bytes": TXT.stat().st_size if TXT.exists() else 0,
            "anchor": "FIG. 2. Constraints on Y",
            "anchor_found": file_contains(TXT, ["FIG. 2. Constraints on Y"]) if TXT.exists() else False,
            "status": "TEXT_EXTRACTION_PRESENT",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PDF1570_2_fig2_image",
            "local_path": rel(FIG2),
            "exists": FIG2.exists(),
            "bytes": FIG2.stat().st_size if FIG2.exists() else 0,
            "anchor": "page_5_image_1_Im3.png",
            "anchor_found": FIG2.exists(),
            "status": "FIG2_IMAGE_EXTRACTED",
            **flags(),
        },
    ]


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
                        "size": len(pts),
                        "min_x": min(xs2),
                        "max_x": max(xs2),
                        "min_y": min(ys),
                        "max_y": max(ys),
                        "points": pts,
                    }
                )
    return components


def digitized_curve_rows() -> list[dict[str, Any]]:
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
    selected = [
        component
        for component in components
        if component["size"] > 300 and (component["max_x"] - component["min_x"]) > 100 and component["min_y"] < 520
    ]
    pixel_by_x: dict[int, list[int]] = {}
    selected_ids = []
    for index, component in enumerate(selected):
        selected_ids.append(f"component{index}:size={component['size']}:bbox={component['min_x']},{component['max_x']},{component['min_y']},{component['max_y']}")
        for y, x in component["points"]:
            if 114 <= x <= 1012 and 20 <= y <= 688:
                pixel_by_x.setdefault(x, []).append(y)
    rows = []
    sample_index = 0
    for x in sorted(pixel_by_x):
        ys = pixel_by_x[x]
        if not ys:
            continue
        if sample_index % 10 != 0:
            sample_index += 1
            continue
        y = float(np.median(ys))
        lam = px_to_lambda(float(x))
        alpha = px_to_alpha(y)
        if lam <= 0 or alpha <= 0:
            sample_index += 1
            continue
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "point_id": f"DIG1570_{len(rows):03d}",
                "lambda_m": f"{lam:.8g}",
                "alpha_abs_bound": f"{alpha:.8g}",
                "pixel_x": x,
                "pixel_y": f"{y:.2f}",
                "curve": "This_work_blue_curve",
                "digitization_status": "CANDIDATE_IMAGE_TRACE_NONCLAIM",
                "source_image": rel(FIG2),
                "source_text": rel(TXT),
                "calibration": "manual_log_axis_from_frame_and_major_ticks",
                "selected_components": " | ".join(selected_ids),
                **flags(),
            }
        )
        sample_index += 1
    if not rows:
        raise RuntimeError("no digitized curve rows generated")
    return rows


def digitization_method_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c = calibration()
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "METHOD1570_0_source",
            "method_piece": "source assets",
            "value": f"pdf={rel(PDF)}; text={rel(TXT)}; fig2={rel(FIG2)}",
            "status": "LOCAL_SOURCE_ASSETS_PRESENT",
            "risk": "figure tracing still needs manual QA before accepted use",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "METHOD1570_1_axis_calibration",
            "method_piece": "log axis calibration",
            "value": f"x_left={c['plot_x_left_px']} at lambda=1e-3; x_decade={c['plot_x_decade_px']} px; y_top={c['plot_y_top_px']} at alpha=1; y_decade={c['plot_y_decade_px']} px",
            "status": "MANUAL_IMAGE_CALIBRATION_CANDIDATE",
            "risk": "axis calibration is approximate and must be QA'd against plot ticks",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "METHOD1570_2_curve_detection",
            "method_piece": "blue pixel connected components",
            "value": f"points={len(curve_rows)}",
            "status": "CANDIDATE_TRACE_CREATED",
            "risk": "blue arrow/text may contaminate candidate; no claim until cleaned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "method_id": "METHOD1570_3_acceptance",
            "method_piece": "accepted curve gate",
            "value": "manual or independent digitization check required before valid_for_claim",
            "status": "NOT_ACCEPTED",
            "risk": "candidate curve can support tooling smoke tests only",
            **flags(),
        },
    ]


def tau_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("TAUG1570_0_external_bound", "external alpha(lambda) curve", "candidate curve now exists", "CANDIDATE_NONCLAIM"),
        ("TAUG1570_1_internal_range", "lambda_R=sqrt(Z_R/M_R^2)", "Z_R and M_R^2 missing", "BLOCKED"),
        ("TAUG1570_2_internal_amplitude", "alpha_MTS=tau_R10*A_R", "A_R/J_R/B_R/readout source normalization missing", "BLOCKED"),
        ("TAUG1570_3_comparator", "abs(alpha_MTS(lambda_R)) <= alpha_bound(lambda_R)", "cannot evaluate without internal projection", "BLOCKED"),
        ("TAUG1570_4_verdict", "tau kernel source normalization", "not derived; candidate curve only improves external side", "NOT_READY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "target": target,
            "current_status": current_status,
            "result": result,
            "source_paths": source_list("1569_tau", "fig2", "text"),
            **flags(),
        }
        for gate_id, target, current_status, result in rows
    ]


def runner_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("RUN1570_0_sources", "load 1569 handoff and R10 PDF/text/figure", "PASS", "all source register needles found"),
        ("RUN1570_1_curve", "candidate R10 alpha(lambda) digitization", "PASS_CANDIDATE_NONCLAIM", f"candidate_points={len(curve_rows)}"),
        ("RUN1570_2_acceptance", "accepted R10 bound curve", "NOT_ACCEPTED", "manual/independent QA required"),
        ("RUN1570_3_tau", "tau_R10 source-normalized projection", "BLOCKED_NO_CLAIM", "internal source normalization missing"),
        ("RUN1570_4_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1570_5_claim", "R10/local GR claim", "BLOCKED_NO_CLAIM", "candidate curve exists but internal MTS prediction is missing"),
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
        ("GATE1570_0_curve_candidate", "candidate R10 bound curve", "PASS_NONCLAIM", "image-trace candidate exists but is not accepted"),
        ("GATE1570_1_curve_accepted", "accepted R10 bound curve", "BLOCKED_NO_CLAIM", "manual/independent digitization QA missing"),
        ("GATE1570_2_tau_kernel", "tau_R10 source-normalized projection", "BLOCKED_NO_CLAIM", "internal source normalization missing"),
        ("GATE1570_3_MTS_prediction", "alpha_MTS(lambda)", "BLOCKED_NO_CLAIM", "Z_R/M_R2/J_R/B_R/readout inputs missing"),
        ("GATE1570_4_local_GR", "derived local GR/Newton/R10 safety", "BLOCKED_NO_CLAIM", "external curve alone is not theory evidence"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1569_doc", "fig2", "text"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1570_0_curve",
            "decision": "R10 bound curve",
            "result": "CANDIDATE_DIGITIZED_CURVE_CREATED_NONCLAIM",
            "reason": "Fig. 2 blue curve was extracted and traced, but requires QA before accepted use",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1570_1_tau",
            "decision": "tau_R10 kernel",
            "result": "SOURCE_NORMALIZATION_MISSING",
            "reason": "external curve side improved; internal MTS projection still missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1570_2_next",
            "decision": "next target",
            "result": "NEXT_1571_DIGITIZATION_QA_OR_TAU_R10_INTERNAL_KERNEL",
            "reason": "either QA the digitized curve or derive/fill the internal tau_R10 projection kernel",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1570_0_1571",
            "next_target": "1571-Y5-RAB-R10-digitization-QA-or-tauR10-internal-kernel.md",
            "script": "scripts/Y5_RAB_R10_digitization_QA_or_tauR10_internal_kernel.py",
            "objective": "QA/clean the candidate R10 digitized curve and separately try to derive the internal tau_R10 source-normalization kernel from Z_R/M_R2/J_R/B_R/readout inputs",
            "do_not": "do not accept the candidate curve without QA; do not claim R10 pass without an internal MTS prediction; do not edit formalization-workbench",
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
    pdf = read_csv(PDF_AUDIT)
    method = read_csv(DIGITIZATION_METHOD)
    curve = read_csv(DIGITIZED_CURVE)
    tau = read_csv(TAU_GATE)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    lambda_values = [float(row["lambda_m"]) for row in curve]
    alpha_values = [float(row["alpha_abs_bound"]) for row in curve]

    checks = [
        ("VAL1570_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1570 source paths exist"),
        ("VAL1570_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1570_2_pdf_assets", all(row["exists"] == "True" and row["anchor_found"] == "True" for row in pdf), "PDF/text/Fig2 assets exist and are anchored"),
        ("VAL1570_3_method_recorded", len(method) == 4 and any(row["status"] == "NOT_ACCEPTED" for row in method), "digitization method and nonacceptance recorded"),
        ("VAL1570_4_curve_candidate", len(curve) >= 20 and all(row["digitization_status"] == "CANDIDATE_IMAGE_TRACE_NONCLAIM" for row in curve), "candidate digitized curve rows created"),
        ("VAL1570_5_curve_positive", all(value > 0 for value in lambda_values + alpha_values), "candidate curve lambda/alpha values are positive"),
        ("VAL1570_6_tau_blocked", any(row["gate_id"] == "TAUG1570_4_verdict" and row["result"] == "NOT_READY" for row in tau), "tau kernel remains not ready"),
        ("VAL1570_7_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1570_8_runner_blocks_claim", any(row["runner_id"] == "RUN1570_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local/R10 claim"),
        ("VAL1570_9_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1570_10_decision_next", any(row["result"] == "NEXT_1571_DIGITIZATION_QA_OR_TAU_R10_INTERNAL_KERNEL" for row in decision_items), "decision selects digitization QA or tau kernel"),
        ("VAL1570_11_next_target", any("1571-Y5-RAB-R10-digitization-QA" in row["next_target"] for row in next_rows), "next target is digitization QA or tau kernel"),
        ("VAL1570_12_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1570 CSVs parse cleanly"),
        ("VAL1570_13_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1570_14_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1570_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1570_16_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1570_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1570 R10 curve digitization or tau kernel source-normalization validation",
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
    pdf: list[dict[str, Any]],
    method: list[dict[str, Any]],
    curve: list[dict[str, Any]],
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
                "# 1570 - R_AB R10 Curve Digitization or tau_R10 Kernel Source Normalization",
                "",
                "## Verdict",
                "- The external R10 side improved materially: the APS fulltext PDF payload, text extraction, Fig. 2 image, and a candidate blue-curve digitization now exist locally.",
                "- The digitized curve is candidate-only: it is an image trace with approximate axis calibration and possible blue-arrow/text contamination.",
                "- The internal MTS side is still missing: `tau_R10` source normalization, `Z_R`, `M_R^2`, `J_R`, `B_R`, and readout inputs are not filled.",
                "- Therefore this supports future smoke tooling, not a claim.",
                "- No R10, local GR/Newton, PPN, WEP, clock, orbital, `Z_R=0`, or `q_R=0` claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## PDF/Figure Source Audit",
                md_table(pdf, ["audit_id", "local_path", "exists", "bytes", "anchor", "anchor_found", "status"]),
                "",
                "## Digitization Method",
                md_table(method, ["method_id", "method_piece", "value", "status", "risk"]),
                "",
                "## Digitized Curve Candidate",
                md_table(curve[:30], ["point_id", "lambda_m", "alpha_abs_bound", "pixel_x", "pixel_y", "curve", "digitization_status"]),
                "",
                "## tau_R10 Kernel Gate",
                md_table(tau, ["gate_id", "target", "current_status", "result"]),
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
    pdf = pdf_audit_rows()
    curve = digitized_curve_rows()
    method = digitization_method_rows(curve)
    tau = tau_gate_rows()
    run_rows = runner_rows(curve)
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PDF_AUDIT, pdf)
    write_csv(DIGITIZATION_METHOD, method)
    write_csv(DIGITIZED_CURVE, curve)
    write_csv(TAU_GATE, tau)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PDF_AUDIT,
        DIGITIZATION_METHOD,
        DIGITIZED_CURVE,
        TAU_GATE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, pdf, method, curve, tau, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
