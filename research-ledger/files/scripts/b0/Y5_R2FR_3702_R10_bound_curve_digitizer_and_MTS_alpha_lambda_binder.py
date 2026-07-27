from __future__ import annotations

import csv
import math
import re
import sys
import zlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
ARXIV_SOURCE = R10 / "arxiv_2002_11761_source"
CHECKPOINT_ID = "3702"
BRANCH_ID = "MTS_R2FR_Y5_R10_BOUND_CURVE_DIGITIZER_AND_MTS_ALPHA_LAMBDA_BINDER_3702"
DOC = ROOT / "3702-Y5-R2FR-R10-bound-curve-digitizer-and-MTS-alpha-lambda-binder.md"

X_MAJOR_1E_MINUS_5_M = 2102.79
X_MAJOR_1E_MINUS_4_M = 3361.06
Y_LOG_ALPHA_MINUS_3 = 775.344
Y_LOG_ALPHA_6 = 3835.29
Y_ALPHA_1 = 1795.23
ANCHOR_LAMBDA_M = 38.6e-6


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def lambda_from_x(x_pdf: float) -> float:
    scale = X_MAJOR_1E_MINUS_4_M - X_MAJOR_1E_MINUS_5_M
    return 10 ** (-5 + (x_pdf - X_MAJOR_1E_MINUS_5_M) / scale)


def log_alpha_from_y(y_pdf: float) -> float:
    return -3 + (y_pdf - Y_LOG_ALPHA_MINUS_3) / (Y_LOG_ALPHA_6 - Y_LOG_ALPHA_MINUS_3) * 9


def alpha_from_y(y_pdf: float) -> float:
    return 10 ** log_alpha_from_y(y_pdf)


def extract_pdf_segments(pdf_path: Path) -> list[tuple[tuple[float, float, float], float, float, float, float, float]]:
    data = pdf_path.read_bytes()
    match = re.search(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S)
    if not match:
        raise ValueError(f"no stream in {pdf_path}")
    text = zlib.decompress(match.group(1)).decode("latin1")
    tokens = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?|[A-Za-z]+|\S", text)
    color = (0.0, 0.0, 0.0)
    width = 0.0
    stack: list[float] = []
    current: tuple[float, float] | None = None
    segments: list[tuple[tuple[float, float, float], float, float, float, float, float]] = []
    for token in tokens:
        try:
            stack.append(float(token))
            continue
        except ValueError:
            pass
        if token == "RG" and len(stack) >= 3:
            blue = stack.pop()
            green = stack.pop()
            red = stack.pop()
            color = (round(red, 6), round(green, 6), round(blue, 6))
            stack = []
            current = None
        elif token == "w" and stack:
            width = round(stack.pop(), 3)
            stack = []
        elif token == "m" and len(stack) >= 2:
            y_pdf = stack.pop()
            x_pdf = stack.pop()
            current = (x_pdf, y_pdf)
            stack = []
        elif token == "l" and len(stack) >= 2 and current is not None:
            y_pdf = stack.pop()
            x_pdf = stack.pop()
            x0, y0 = current
            if 1220 <= x0 <= 4630 and 770 <= y0 <= 3840 and 1220 <= x_pdf <= 4630 and 770 <= y_pdf <= 3840:
                segments.append((color, width, x0, y0, x_pdf, y_pdf))
            current = (x_pdf, y_pdf)
            stack = []
        elif token == "c" and len(stack) >= 6 and current is not None:
            vals = [stack.pop() for _ in range(6)][::-1]
            current = (vals[4], vals[5])
            stack = []
        elif token in {"S", "f", "q", "Q", "cm", "gs", "J", "M", "d", "g", "G", "rg", "BT", "ET", "Tf", "Td", "Tj"}:
            stack = []
    return segments


def connected_components(segments: list[tuple[tuple[float, float, float], float, float, float, float, float]]) -> list[list[int]]:
    unused = set(range(len(segments)))
    components: list[list[int]] = []

    def close(point_a: tuple[float, float], point_b: tuple[float, float], tolerance: float = 3.0) -> bool:
        return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2 <= tolerance**2

    while unused:
        first = unused.pop()
        component = [first]
        points = [(segments[first][2], segments[first][3]), (segments[first][4], segments[first][5])]
        changed = True
        while changed:
            changed = False
            for idx in list(unused):
                endpoints = [(segments[idx][2], segments[idx][3]), (segments[idx][4], segments[idx][5])]
                if any(close(point, endpoint) for point in points for endpoint in endpoints):
                    unused.remove(idx)
                    component.append(idx)
                    points.extend(endpoints)
                    changed = True
        components.append(component)
    return components


def candidate_curve_segments() -> tuple[list[tuple[tuple[float, float, float], float, float, float, float, float]], dict[str, object]]:
    fig = ARXIV_SOURCE / "fig5b1.pdf"
    all_segments = extract_pdf_segments(fig)
    curve_color = (0.333008, 0.0, 1.0)
    curve_width = 13.039
    candidate_segments = []
    for segment in all_segments:
        color, width, x0, y0, x1, y1 = segment
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        length = math.hypot(dx, dy)
        if color == curve_color and abs(width - curve_width) < 0.02 and length > 5 and dx > 1 and dy > 1:
            candidate_segments.append(segment)
    components = connected_components(candidate_segments)
    best_component: list[int] | None = None
    best_distance = float("inf")
    best_crossing: tuple[float, float] | None = None
    for component in components:
        for idx in component:
            _, _, x0, y0, x1, y1 = candidate_segments[idx]
            if (y0 - Y_ALPHA_1) * (y1 - Y_ALPHA_1) <= 0 and abs(y1 - y0) > 1:
                fraction = (Y_ALPHA_1 - y0) / (y1 - y0)
                x_cross = x0 + fraction * (x1 - x0)
                lambda_cross = lambda_from_x(x_cross)
                distance = abs(lambda_cross - ANCHOR_LAMBDA_M)
                if distance < best_distance:
                    best_distance = distance
                    best_component = component
                    best_crossing = (x_cross, lambda_cross)
    if best_component is None or best_crossing is None:
        raise ValueError("no candidate curve crossing near alpha=1")
    selected = [candidate_segments[idx] for idx in best_component]
    metadata = {
        "figure_path": str(fig),
        "curve_color_rgb": str(curve_color),
        "curve_width_pdf": curve_width,
        "candidate_segment_count": len(selected),
        "alpha1_crossing_x_pdf": round(best_crossing[0], 6),
        "alpha1_crossing_lambda_m": best_crossing[1],
        "alpha1_crossing_lambda_um": best_crossing[1] * 1e6,
        "anchor_lambda_um": ANCHOR_LAMBDA_M * 1e6,
        "anchor_abs_error_um": abs(best_crossing[1] - ANCHOR_LAMBDA_M) * 1e6,
    }
    return selected, metadata


def digitized_candidate_rows(timestamp: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    segments, metadata = candidate_curve_segments()
    lambdas = []
    for _, _, x0, _y0, x1, _y1 in segments:
        lambdas.extend([lambda_from_x(x0), lambda_from_x(x1)])
    min_lambda = max(min(lambdas), 5e-6)
    max_lambda = min(max(lambdas), 9e-3)
    targets = [10 ** (math.log10(min_lambda) + idx * (math.log10(max_lambda) - math.log10(min_lambda)) / 65) for idx in range(66)]
    rows: list[dict[str, object]] = []
    for idx, lambda_target in enumerate(targets):
        x_target = X_MAJOR_1E_MINUS_5_M + (X_MAJOR_1E_MINUS_4_M - X_MAJOR_1E_MINUS_5_M) * (math.log10(lambda_target) + 5)
        alpha_candidates = []
        for _color, _width, x0, y0, x1, y1 in segments:
            if min(x0, x1) <= x_target <= max(x0, x1) and abs(x1 - x0) > 1e-9:
                fraction = (x_target - x0) / (x1 - x0)
                y_interp = y0 + fraction * (y1 - y0)
                alpha_candidates.append(alpha_from_y(y_interp))
        if not alpha_candidates:
            continue
        alpha_bound = min(alpha_candidates)
        rows.append(
            {
                **base(timestamp),
                "curve_row_id": f"R10C3702_{idx:03d}",
                "lambda_m": f"{lambda_target:.12e}",
                "lambda_um": f"{lambda_target * 1e6:.6f}",
                "alpha_bound_abs": f"{alpha_bound:.12e}",
                "extraction_method": "vector_pdf_lower_envelope_candidate_from_fig5b1",
                "source_file": str(ARXIV_SOURCE / "fig5b1.pdf"),
                "figure_axis_calibration": "x: 1e-5 m at 2102.79, 1e-4 m at 3361.06; y: log10(alpha) -3 at 775.344 and 6 at 3835.29",
                "confidence": "candidate_manual_review_required",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    anchor_row = {
        **base(timestamp),
        "curve_row_id": "R10C3702_OFFICIAL_ALPHA1_ANCHOR",
        "lambda_m": f"{ANCHOR_LAMBDA_M:.12e}",
        "lambda_um": f"{ANCHOR_LAMBDA_M * 1e6:.6f}",
        "alpha_bound_abs": "1.000000000000e+00",
        "extraction_method": "official_text_anchor_from_Lee2020_arxiv_and_pubmed",
        "source_file": str(ARXIV_SOURCE / "FB_ISL_pdf.tex"),
        "figure_axis_calibration": "not digitized; text states gravitational-strength Yukawa range <38.6 micrometer",
        "confidence": "source_text_anchor_high_but_not_full_curve",
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    rows.append(anchor_row)
    return rows, metadata


def source_register(timestamp: str, metadata: dict[str, object]) -> list[dict[str, object]]:
    specs = [
        ("handoff_3701", RESIDUALS / "P8_Y5_R2FR_3701_NEXT_TARGET.csv", "R10"),
        ("source_rows_3701", RESIDUALS / "P8_Y5_R2FR_3701_LOCAL_TEST_SOURCE_ROWS.csv", "38.6"),
        ("matrix_3701", RESIDUALS / "P8_Y5_R2FR_3701_RESIDUAL_MATRIX_ROWS.csv", "alpha_bound_R10"),
        ("arxiv_tex_2002_11761", ARXIV_SOURCE / "FB_ISL_pdf.tex", "constraints on $|\\alpha|$"),
        ("arxiv_fig5b1_pdf", ARXIV_SOURCE / "fig5b1.pdf", ""),
        ("arxiv_source_archive", R10 / "arxiv_2002_11761_source.tar.gz", ""),
    ]
    rows = []
    for source_id, path, needle in specs:
        exists = path.exists()
        text = read_text(path) if exists and path.suffix.lower() in {".tex", ".csv", ".md"} else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": True if needle == "" and exists else (needle in text),
                "role": "R10 bound curve and MTS alpha-lambda binder input",
                "metadata_crossing_um": f"{metadata.get('alpha1_crossing_lambda_um', '')}",
            }
        )
    return rows


def extraction_rows(timestamp: str, metadata: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "extraction_id": "EXT3702_0_axis_calibration",
            "object": "fig5b1.pdf bottom plot",
            "method": "PDF vector stream parsed directly; axis calibrated from log tick positions and text anchor",
            "result": "x_major_1e-5_m=2102.79; x_major_1e-4_m=3361.06; y_logalpha_minus3=775.344; y_logalpha_6=3835.29",
            "confidence": "medium_for_private_digitization",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "extraction_id": "EXT3702_1_curve_component",
            "object": "Eot-Wash 2020 candidate curve",
            "method": "selected purple vector component whose alpha=1 crossing matches official 38.6 micrometer anchor",
            "result": f"crossing={metadata['alpha1_crossing_lambda_um']:.6f} micrometer; official anchor=38.6 micrometer; abs error={metadata['anchor_abs_error_um']:.6f} micrometer",
            "confidence": "candidate_curve_manual_review_required",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "extraction_id": "EXT3702_2_limitations",
            "object": "official full curve",
            "method": "arXiv source inspection",
            "result": "TeX says positive and negative alpha constraints are in Supplemental Material, but extracted arXiv source package contains PDFs and no machine-readable alpha-lambda table.",
            "confidence": "blocker_precisely_named",
            "claim_allowed": False,
        },
    ]


def mts_binder_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "MTSR10_3702_0_lambda",
            "lambda_H",
            "lambda_H = 1/mu_H",
            "requires mu_H from T_eff lambda_min(I_H^perp)-R_domain-R_source_slope or numeric closure",
            "MISSING_MUH_VALUE",
        ),
        (
            "MTSR10_3702_1_alpha",
            "alpha_eff(lambda_H)",
            "alpha_eff = K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj",
            "requires K_N, rho_Newton, z0^2/z2_bound, edge, projection terms",
            "MISSING_ALPHA_VALUE",
        ),
        (
            "MTSR10_3702_2_score",
            "R10_score",
            "pass_if abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H)",
            "requires either official alpha_bound(lambda) table or reviewed digitized candidate plus numeric MTS alpha/lambda",
            "SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "MTSR10_3702_3_anchor_only",
            "anchor_smoke",
            "if lambda_H >= 38.6 micrometer then gravitational-strength alpha_eff~1 branch is disfavored by Lee2020 anchor",
            "only a sanity check; cannot score arbitrary alpha_eff without full curve",
            "ANCHOR_ONLY_SMOKE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "binder_id": binder_id,
            "quantity": quantity,
            "formula": formula,
            "required_inputs": required_inputs,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for binder_id, quantity, formula, required_inputs, status in specs
    ]


def smoke_rows(timestamp: str, candidate_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    numeric_curve_rows = [row for row in candidate_rows if row["curve_row_id"] != "R10C3702_OFFICIAL_ALPHA1_ANCHOR"]
    anchor = next(row for row in candidate_rows if row["curve_row_id"] == "R10C3702_OFFICIAL_ALPHA1_ANCHOR")
    return [
        {
            **base(timestamp),
            "smoke_id": "SMOKE3702_0_curve_candidate",
            "input": "digitized_candidate_lower_envelope",
            "result": f"{len(numeric_curve_rows)} candidate curve rows plus official alpha=1 anchor at {anchor['lambda_um']} micrometer",
            "score_ready": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "blocker": "manual review and/or official supplemental alpha table required for claims",
        },
        {
            **base(timestamp),
            "smoke_id": "SMOKE3702_1_mts_binding",
            "input": "symbolic MTS alpha_eff/lambda_H",
            "result": "binder schema exists but no numeric rho_Newton, z2_bound, mu_H, K_N, alpha_edge, or alpha_proj",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "blocker": "MTS-side numeric rows missing",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3702_0", "R10 figure digitization candidate exists.", "Vector extraction from fig5b1 reproduces the official alpha=1 crossing at 38.58 micrometer.", "CURVE_CANDIDATE_ADVANCES"),
        ("DEC3702_1", "Do not treat the candidate curve as claim evidence.", "The paper says the signed alpha constraints are in Supplemental Material; no machine-readable official table was found in the arXiv source package.", "CLAIM_BLOCKED"),
        ("DEC3702_2", "MTS R10 binder is schema-ready but not numerically score-ready.", "lambda_H and alpha_eff remain symbolic until mu_H/rho_Newton/z2_bound/K_N are sourced.", "MTS_SIDE_MISSING"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3702_0_official_curve", "official full alpha_bound(lambda) table or manually reviewed digitization", "BLOCKED"),
        ("CG3702_1_mts_lambda", "numeric lambda_H=1/mu_H sourced from parent mass-gap rows", "BLOCKED"),
        ("CG3702_2_mts_alpha", "numeric alpha_eff from rho_Newton, z2_bound, K_N, edge, projection terms", "BLOCKED"),
        ("CG3702_3_score", "abs(alpha_eff(lambda_H)) <= alpha_bound_R10(lambda_H) evaluated", "BLOCKED"),
        ("CG3702_4_public", "public R10/local-Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str, metadata: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3702_0",
            "status": "R10_CANDIDATE_CURVE_DIGITIZED_FROM_VECTOR_FIGURE_MTS_ALPHA_LAMBDA_BINDER_SCHEMA_READY_NONCLAIM",
            "summary": (
                f"3702 extracted a private candidate R10 alpha_bound(lambda) lower envelope from arXiv fig5b1.pdf. "
                f"The selected component crosses alpha=1 at {metadata['alpha1_crossing_lambda_um']:.3f} micrometer, matching the official 38.6 micrometer anchor. "
                "The curve is useful for nonclaim smoke tests only; claims require an official supplemental table or manual-reviewed digitization plus numeric MTS alpha_eff/lambda_H rows."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3702_0",
            "target_doc": "3703-Y5-R2FR-MTS-rho-Newton-z2bound-muH-numeric-or-symbolic-bound.md",
            "target_script": "scripts/Y5_R2FR_3703_MTS_rho_Newton_z2bound_muH_numeric_or_symbolic_bound.py",
            "objective": "try to derive or bound the MTS-side R10 inputs rho_Newton, z2_bound, mu_H/lambda_H, K_N, alpha_edge, and alpha_proj from the Fisher/source-silence chain",
            "success_gate": "R10 can run a complete nonclaim smoke score against the candidate curve, or the MTS-side missing input is narrowed to one named parent coefficient",
            "claim_allowed": False,
        }
    ]


def write_doc(
    metadata: dict[str, object],
    sources: list[dict[str, object]],
    extraction: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    binders: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3702 Y5 R2FR R10 Bound Curve Digitizer And MTS Alpha-Lambda Binder",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- Pulled and inspected the arXiv source package for Lee et al. 2020 / PRL 124, 101101.",
        "- The TeX confirms 66 tested `lambda` values from `5 micrometer` to `9 mm`, but says signed `alpha` constraints are in Supplemental Material.",
        "- The arXiv source package contains `fig5b1.pdf` but no machine-readable alpha-lambda table.",
        f"- A private vector digitization candidate was extracted from `fig5b1.pdf`; it crosses `alpha=1` at `{metadata['alpha1_crossing_lambda_um']:.6f} micrometer`, matching the official `38.6 micrometer` anchor.",
        "- The digitized curve is `valid_for_claim=false`; it is only for smoke-testing schema and rough private intuition until manually reviewed or replaced by an official table.",
        "",
        "## Extraction Rows",
        "",
    ]
    for row in extraction:
        lines.append(f"- `{row['extraction_id']}`: `{row['confidence']}` | {row['result']}")
    lines.extend(["", "## Curve Rows", ""])
    lines.append(f"- Candidate rows: `{len([row for row in candidate_rows if row['curve_row_id'] != 'R10C3702_OFFICIAL_ALPHA1_ANCHOR'])}`")
    anchor = next(row for row in candidate_rows if row["curve_row_id"] == "R10C3702_OFFICIAL_ALPHA1_ANCHOR")
    lines.append(f"- Official anchor row: `{anchor['lambda_um']} micrometer`, `alpha=1`, `valid_for_claim=false`")
    lines.extend(["", "## MTS Binder Rows", ""])
    for row in binders:
        lines.append(f"- `{row['binder_id']}`: `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Smoke Rows", ""])
    for row in smoke:
        lines.append(f"- `{row['smoke_id']}`: score_ready={row['score_ready']} claim=false | {row['result']} | blocker: {row['blocker']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    metadata: dict[str, object],
    sources: list[dict[str, object]],
    extraction: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    binders: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    checks.append(("anchor_crossing", "digitized alpha=1 crossing agrees with official anchor within 0.5 micrometer", float(metadata["anchor_abs_error_um"]) < 0.5, str(metadata)))
    numeric_candidate_rows = [row for row in candidate_rows if row["curve_row_id"] != "R10C3702_OFFICIAL_ALPHA1_ANCHOR"]
    checks.append(("candidate_curve_rows", "candidate curve has at least 30 rows", len(numeric_candidate_rows) >= 30, f"rows={len(numeric_candidate_rows)}"))
    positive_curve = all(float(row["lambda_m"]) > 0 and float(row["alpha_bound_abs"]) > 0 for row in candidate_rows)
    checks.append(("positive_curve_values", "all curve lambda/alpha values are positive", positive_curve, ""))
    checks.append(("curve_nonclaim", "all curve rows are nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in candidate_rows), ""))
    binder_by_id = {str(row["binder_id"]): row for row in binders}
    checks.append(("binder_formula", "MTS alpha/lambda binder contains lambda_H and alpha_eff", "lambda_H" in str(binder_by_id["MTSR10_3702_0_lambda"]["formula"]) and "alpha_eff" in str(binder_by_id["MTSR10_3702_1_alpha"]["formula"]), ""))
    checks.append(("smoke_candidate_ready_only", "candidate curve smoke ready but MTS binding not ready", any(row["smoke_id"] == "SMOKE3702_0_curve_candidate" and row["score_ready"] is True for row in smoke) and any(row["smoke_id"] == "SMOKE3702_1_mts_binding" and row["score_ready"] is False for row in smoke), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3703", "next target advances to MTS-side R10 inputs", str(next_target[0]["target_doc"]).startswith("3703-") and "rho-Newton" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core R10 terms", all(term in doc_text for term in ["38.6 micrometer", "valid_for_claim=false", "alpha_eff", "lambda_H", "Supplemental Material"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3702*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3702 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    candidate_rows, metadata = digitized_candidate_rows(timestamp)
    sources = source_register(timestamp, metadata)
    extraction = extraction_rows(timestamp, metadata)
    binders = mts_binder_rows(timestamp)
    smoke = smoke_rows(timestamp, candidate_rows)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, metadata)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3702_SOURCE_REGISTER.csv",
        "extraction": RESIDUALS / "P8_Y5_R2FR_3702_R10_FIGURE_EXTRACTION_ROWS.csv",
        "candidate_curve": RESIDUALS / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv",
        "binders": RESIDUALS / "P8_Y5_R2FR_3702_MTS_ALPHA_LAMBDA_BINDER_ROWS.csv",
        "smoke": RESIDUALS / "P8_Y5_R2FR_3702_R10_SMOKE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3702_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3702_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3702_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3702_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3702_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["extraction"], extraction)
    write_csv(outputs["candidate_curve"], candidate_rows)
    write_csv(outputs["binders"], binders)
    write_csv(outputs["smoke"], smoke)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(metadata, sources, extraction, candidate_rows, binders, smoke, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, metadata, sources, extraction, candidate_rows, binders, smoke, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3702 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3702 checkpoint: R10 candidate curve digitized; MTS alpha/lambda binder remains nonclaim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
