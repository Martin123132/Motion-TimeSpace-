from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
ACQ_SOURCE = POST / "source-intake" / "r10_curve_acquisition" / "4635" / "source"

CHECKPOINT = "4636"
CLAIM_ID = "L-478"
BRANCH_ID = "MTS_R2FR_Y5_R10_VECTOR_QA_EPSILON_ENVELOPE_4636"
MARKER = "PPC4161_R10_VECTOR_CURVE_QA_AND_EPSILON_COEFFICIENT_FILL_4636"
PACKET_MARKER = "PPC4161_PACKET_R10_VECTOR_QA_EPSILON_ENVELOPE_4636"
DECISION = "R10_REDUCES_TO_OBSERVABLE_XI_ENVELOPE_PARENT_COEFFICIENT_TARGET_DEFINED_NONCLAIM"
NEXT_TARGET = "4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md"

DOC_PATH = POST / "4636-Y5-R2FR-R10-vector-curve-QA-and-epsilon-coefficient-fill.md"
FORMAL_PATH = FORMAL / "652-PPC4161-R10-vector-curve-QA-and-epsilon-coefficient-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4635_VALIDATION.csv"
CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4635_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_CURVE_STATUS_ROWS.csv"
CSV_4635_PROJECTION = SOURCE_DIR / "P8_Y5_R2FR_4635_PROJECTION_INPUT_REQUIREMENTS.csv"
CSV_4635_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4635_VECTOR_CURVE_RUNNER_RESULTS.csv"
CSV_4635_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4635_NEXT_TARGET.csv"
TEX_PATH = ACQ_SOURCE / "FB_ISL_pdf.tex"
FIG5B_PDF = ACQ_SOURCE / "fig5b1.pdf"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4636_SOURCE_REGISTER.csv"
QA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_R10_VECTOR_CURVE_QA.csv"
OBSERVABLE_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_OBSERVABLE_XI_REDUCTION_ROWS.csv"
ENVELOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_R10_EPSILON_ENVELOPE_ROWS.csv"
INVERSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_XI_TO_LAMBDA_MAX_ROWS.csv"
COEFFICIENT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_PARENT_COEFFICIENT_TARGET_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_XI_ENVELOPE_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4636_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4636_VALIDATION.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")

SOURCE_ALPHA_ONE_ANCHOR_M = 38.6e-6


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


def load_curve() -> list[tuple[float, float]]:
    rows = read_csv(CSV_4635_CURVE)
    points = [(float(row["lambda_m"]), float(row["alpha_bound_abs"])) for row in rows]
    return sorted(points)


def interpolate_alpha(points: list[tuple[float, float]], lambda_m: float) -> float | None:
    if not points or lambda_m < points[0][0] or lambda_m > points[-1][0]:
        return None
    log_lambda = math.log10(lambda_m)
    for (left_lambda, left_alpha), (right_lambda, right_alpha) in zip(points, points[1:]):
        if left_lambda <= lambda_m <= right_lambda:
            left_log_lambda = math.log10(left_lambda)
            right_log_lambda = math.log10(right_lambda)
            if abs(right_log_lambda - left_log_lambda) < 1.0e-15:
                return left_alpha
            fraction = (log_lambda - left_log_lambda) / (right_log_lambda - left_log_lambda)
            log_alpha = math.log10(left_alpha) + fraction * (math.log10(right_alpha) - math.log10(left_alpha))
            return 10.0**log_alpha
    return points[-1][1]


def lambda_crossing_for_xi(points: list[tuple[float, float]], xi_value: float) -> tuple[str, str]:
    if not points:
        return ("MISSING_CURVE", "")
    min_lambda, max_alpha = points[0]
    max_lambda, min_alpha = points[-1]
    if xi_value > max_alpha:
        return ("NO_ALLOWED_RANGE_INSIDE_EXTRACTED_CURVE", f"<{min_lambda:.12g}")
    if xi_value <= min_alpha:
        return ("ALLOWED_THROUGH_FULL_EXTRACTED_RANGE", f">={max_lambda:.12g}")
    for (left_lambda, left_alpha), (right_lambda, right_alpha) in zip(points, points[1:]):
        if (left_alpha - xi_value) * (right_alpha - xi_value) <= 0.0:
            left_log_alpha = math.log10(left_alpha)
            right_log_alpha = math.log10(right_alpha)
            if abs(right_log_alpha - left_log_alpha) < 1.0e-15:
                return ("CROSSING_FOUND", f"{left_lambda:.12g}")
            fraction = (math.log10(xi_value) - left_log_alpha) / (right_log_alpha - left_log_alpha)
            log_lambda = math.log10(left_lambda) + fraction * (math.log10(right_lambda) - math.log10(left_lambda))
            return ("CROSSING_FOUND", f"{10.0**log_lambda:.12g}")
    return ("NO_CROSSING_FOUND", "")


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4636_00_4635_validation", CSV_4635_VALIDATION, "VAL4635_OVERALL", "4635 validation."),
        ("SRC4636_01_4635_curve", CSV_4635_CURVE, "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1", "4635 vector curve."),
        ("SRC4636_02_4635_status", CSV_4635_STATUS, "FULL_VECTOR_CURVE_EXTRACTED_FROM_FIG5B1_NONCLAIM", "4635 curve status."),
        ("SRC4636_03_4635_projection", CSV_4635_PROJECTION, "alpha_bound(lambda)", "projection inputs."),
        ("SRC4636_04_4635_runner", CSV_4635_RUNNER, "RUN4635_0_current_live_R10", "live fail-closed runner."),
        ("SRC4636_05_4635_next", CSV_4635_NEXT, "4636-Y5-R2FR-R10-vector-curve-QA-and-epsilon-coefficient-fill.md", "4635 selected 4636."),
        ("SRC4636_06_yukawa_convention", TEX_PATH, "V(r)=V_N(r) [1+\\alpha \\exp({-r/\\lambda})]", "Yukawa convention in paper."),
        ("SRC4636_07_alpha1_anchor", TEX_PATH, "lambda<38.6\\,\\mu$m", "published alpha=1 threshold."),
        ("SRC4636_08_fig5b1", FIG5B_PDF, "", "source vector figure."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path) if path.suffix.lower() in {".csv", ".md", ".tex", ".txt"} else ""
        path_exists = path.exists()
        needle_found = path_exists if not needle else needle in text
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path_exists,
                "needle": needle,
                "needle_found": needle_found,
                "line": line_of(path, needle) if needle else 0,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": now,
            }
        )
    return rows


def qa_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    if not points:
        return [
            {
                "checkpoint": CHECKPOINT,
                "qa_id": "QA4636_0_curve_present",
                "status": "FAIL",
                "detail": "no curve points loaded",
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        ]
    lambda_monotone = all(right_lambda > left_lambda for (left_lambda, _), (right_lambda, _) in zip(points, points[1:]))
    alpha_nonincreasing = all(right_alpha <= left_alpha for (_, left_alpha), (_, right_alpha) in zip(points, points[1:]))
    crossing_status, crossing_value = lambda_crossing_for_xi(points, 1.0)
    crossing_m = float(crossing_value) if crossing_value and not crossing_value.startswith((">", "<")) else math.nan
    anchor_error = (crossing_m - SOURCE_ALPHA_ONE_ANCHOR_M) / SOURCE_ALPHA_ONE_ANCHOR_M if math.isfinite(crossing_m) else math.nan
    return [
        {
            "checkpoint": CHECKPOINT,
            "qa_id": "QA4636_0_curve_present",
            "status": "PASS",
            "detail": f"{len(points)} vector points loaded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "qa_id": "QA4636_1_lambda_monotone",
            "status": "PASS" if lambda_monotone else "FAIL",
            "detail": "lambda values are strictly increasing" if lambda_monotone else "lambda ordering violation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "qa_id": "QA4636_2_alpha_nonincreasing",
            "status": "PASS" if alpha_nonincreasing else "FAIL",
            "detail": "alpha bound decreases with lambda" if alpha_nonincreasing else "alpha bound ordering violation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "qa_id": "QA4636_3_alpha1_anchor_crossing",
            "status": "PASS_FOR_SMOKE_QA" if crossing_status == "CROSSING_FOUND" and abs(anchor_error) < 0.02 else "FAIL",
            "detail": f"vector alpha=1 crossing={crossing_m:.12g} m; source anchor={SOURCE_ALPHA_ONE_ANCHOR_M:.12g} m; fractional error={anchor_error:.6g}",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "qa_id": "QA4636_4_claim_grade",
            "status": "BLOCKED_NONCLAIM",
            "detail": "official supplemental +/- alpha numeric rows or manual digitization QA still required before promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def observable_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XI4636_0_define_observable_combo",
            "statement": "Define Xi_AB(lambda_mem) := C_N epsilon_A epsilon_B / Z_min.",
            "derivation_role": "R10 observes this product combination, not the individual split into epsilon_A, epsilon_B, Z_min and C_N.",
            "result": "R10 coefficient target reduced to one observable parent-owned Xi_AB row.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XI4636_1_R10_gate",
            "statement": "For the Yukawa convention V=V_N[1+alpha exp(-r/lambda)], R10 requires |Xi_AB| <= alpha_bound(lambda_mem).",
            "derivation_role": "Direct comparison of MTS scalar/Yukawa residual with Eot-Wash alpha(lambda).",
            "result": "The extracted curve can bound Xi_AB as a function of lambda_mem.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XI4636_2_epsilon_product",
            "statement": "epsilon_A epsilon_B <= (Z_min/C_N) alpha_bound(lambda_mem).",
            "derivation_role": "Product envelope if the parent action supplies Z_min/C_N.",
            "result": "R10 gives a hard product ceiling once lambda_mem is known.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XI4636_3_symmetric_epsilon",
            "statement": "If epsilon_A=epsilon_B=epsilon, then epsilon <= sqrt((Z_min/C_N) alpha_bound(lambda_mem)).",
            "derivation_role": "Readable symmetric-coupling envelope.",
            "result": "The local branch can now say how small symmetric coupling must be at each range.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XI4636_4_exact_zero",
            "statement": "If no-slot/branch-extremum gives epsilon_A=0 or epsilon_B=0, then Xi_AB=0 and R10 is silent for this channel.",
            "derivation_role": "Exact local-GR route preserved.",
            "result": "Still conditional because the parent zero theorem is unsigned.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def envelope_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    sample_um = [6.0, 10.0, 20.0, 30.0, 38.6, 50.0, 70.0, 85.0, 100.0, 200.0, 500.0, 1000.0]
    rows: list[dict[str, Any]] = []
    for index, lambda_um in enumerate(sample_um):
        lambda_m = lambda_um * 1.0e-6
        alpha_bound = interpolate_alpha(points, lambda_m)
        if alpha_bound is None:
            status = "OUTSIDE_EXTRACTED_RANGE"
            xi_bound = ""
            epsilon_bound = ""
        else:
            xi_bound = alpha_bound
            epsilon_bound = math.sqrt(alpha_bound)
            if alpha_bound >= 1.0:
                status = "CANONICAL_ORDER_ONE_PRODUCT_ALLOWED_BY_VECTOR_SMOKE"
            elif alpha_bound >= 0.1:
                status = "SUB_ORDER_PRODUCT_REQUIRED"
            else:
                status = "SMALL_PRODUCT_REQUIRED"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "envelope_id": f"ENV4636_{index}",
                "lambda_um": f"{lambda_um:.12g}",
                "lambda_m": f"{lambda_m:.12g}",
                "alpha_bound_abs": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "Xi_AB_max": "" if xi_bound == "" else f"{xi_bound:.12g}",
                "epsilon_product_bound": "" if alpha_bound is None else "(epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound",
                "symmetric_epsilon_max_if_Z_over_CN_1": "" if epsilon_bound == "" else f"{epsilon_bound:.12g}",
                "status": status,
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def inverse_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    xi_samples = [1.0e4, 1.0e3, 1.0e2, 10.0, 1.0, 0.1, 0.03, 0.02, 0.01]
    rows: list[dict[str, Any]] = []
    for index, xi_value in enumerate(xi_samples):
        status, lambda_limit = lambda_crossing_for_xi(points, xi_value)
        if lambda_limit.startswith(">="):
            lambda_um = ">=" + f"{float(lambda_limit[2:]) * 1.0e6:.12g}"
        elif lambda_limit.startswith("<"):
            lambda_um = "<" + f"{float(lambda_limit[1:]) * 1.0e6:.12g}"
        elif lambda_limit:
            lambda_um = f"{float(lambda_limit) * 1.0e6:.12g}"
        else:
            lambda_um = ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "inverse_id": f"INV4636_{index}",
                "Xi_AB_assumed": f"{xi_value:.12g}",
                "lambda_max_for_pass_um": lambda_um,
                "status": status,
                "interpretation": "larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed",
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": now,
            }
        )
    return rows


def coefficient_target_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "target_id": "TGT4636_0_XiAB_direct",
            "target": "Xi_AB := C_N epsilon_A epsilon_B/Z_min",
            "why_this_is_better_than_circling": "R10 only needs this product; deriving Xi_AB directly avoids demanding separately numeric epsilon_A, epsilon_B, Z_min and C_N before any progress.",
            "needed_parent_input": "same-branch quadratic/source action giving the observable Yukawa normalization",
            "current_status": "FORMULA_FILLED_NUMERIC_PARENT_ROW_MISSING",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "target_id": "TGT4636_1_lambda_mem",
            "target": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "why_this_is_better_than_circling": "the R10 curve now converts a parent Hessian ratio into a concrete allowed coupling ceiling",
            "needed_parent_input": "positive gap ratio M2_mem/Z_mem or exact-zero source",
            "current_status": "FORMULA_FILLED_NUMERIC_PARENT_ROW_MISSING",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "target_id": "TGT4636_2_exact_zero_factor",
            "target": "epsilon_A=0 or epsilon_B=0",
            "why_this_is_better_than_circling": "a single parent zero factor makes Xi_AB vanish without tuning the curve",
            "needed_parent_input": "signed no-source-slot/q-basic A_m, branch extremum, or parent involution",
            "current_status": "CONDITIONAL_UNSIGNED",
            "next_action": "try to sign the parent Xi zero theorem while retaining finite envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "target_id": "TGT4636_3_WEP_split_caveat",
            "target": "epsilon_A versus epsilon_B split and composition dependence",
            "why_this_is_better_than_circling": "R10 can use Xi_AB, but WEP/PPN cannot; this separates what is genuinely needed for each arena",
            "needed_parent_input": "composition/source projection maps",
            "current_status": "STILL_REQUIRED_AFTER_R10",
            "next_action": "do not use R10 Xi success as WEP/PPN success",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def runner_rows(now: str, points: list[tuple[float, float]]) -> list[dict[str, Any]]:
    scenarios = [
        ("RUN4636_0_current_live", None, None, "FAIL_CLOSED_MISSING_XI_AND_LAMBDA", "live branch has no parent Xi_AB/lambda row"),
        ("RUN4636_1_exact_zero", 0.0, 1000.0e-6, "CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY", "Xi_AB=0 if parent zero theorem is signed"),
        ("RUN4636_2_order_one_at_vector_crossing", 1.0, 38.3693961472e-6, "EVALUATE", "order-one Xi at extracted alpha=1 crossing"),
        ("RUN4636_3_order_one_at_source_anchor", 1.0, 38.6e-6, "EVALUATE", "source anchor is slightly to the right of vector crossing; this is QA-sensitive"),
        ("RUN4636_4_order_one_at_50um", 1.0, 50.0e-6, "EVALUATE", "order-one Xi at 50 um"),
        ("RUN4636_5_point075_at_100um", 0.075, 100.0e-6, "EVALUATE", "near-bound small Xi at 100 um"),
        ("RUN4636_6_point1_at_100um", 0.1, 100.0e-6, "EVALUATE", "slightly too-large Xi at 100 um"),
        ("RUN4636_7_point01_at_1mm", 0.01, 1000.0e-6, "EVALUATE", "small Xi at 1 mm"),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, xi_value, lambda_m, preset, reason in scenarios:
        alpha_bound = interpolate_alpha(points, lambda_m) if lambda_m is not None else None
        if preset != "EVALUATE":
            result = preset
        elif alpha_bound is None:
            result = "FAIL_CLOSED_LAMBDA_OUTSIDE_CURVE"
        elif xi_value is not None and abs(xi_value - alpha_bound) / max(alpha_bound, 1.0e-30) < 0.02:
            result = "PASS_WITHIN_VECTOR_QA_TOLERANCE_NONCLAIM"
        elif xi_value is not None and xi_value <= alpha_bound:
            result = "PASS_VECTOR_ENVELOPE_SMOKE_ONLY_NONCLAIM"
        else:
            result = "FAIL_VECTOR_ENVELOPE_XI_ABOVE_BOUND"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "Xi_AB": "MISSING_PARENT_COEFFICIENT" if xi_value is None else f"{xi_value:.12g}",
                "lambda_mem_m": "MISSING_PARENT_HESSIAN_RATIO" if lambda_m is None else f"{lambda_m:.12g}",
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
            "control_id": "CTL4636_0_no_Xi_fitting_from_bound",
            "rule": "Do not choose Xi_AB from the R10 bound; Xi_AB must come from a parent coefficient row or exact-zero theorem.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4636_1_curve_is_nonclaim",
            "rule": "The vector-extracted curve is an internal smoke gate until official supplement/manual QA promotes it.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4636_2_R10_not_WEP",
            "rule": "A product Xi_AB bound does not replace composition-dependent WEP/PPN projections.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4636_0_parent_Xi",
            "blocks": "R10/local-G finite branch",
            "missing": "parent-owned Xi_AB and lambda_mem, or exact-zero factor",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4636_1_curve_promotion",
            "blocks": "claim-grade R10 comparison",
            "missing": "official supplemental numeric +/- alpha rows or independent manual QA of vector extraction",
            "next_action": "keep vector curve as smoke until promoted",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4636_2_other_arenas",
            "blocks": "WEP/PPN/clock/orbital use",
            "missing": "source/test composition projection and metric-sector residual maps",
            "next_action": "after Xi_AB row exists, propagate to WEP/PPN with separate projections",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4636_0",
            "decision": DECISION,
            "meaning": "The R10 problem now has a concrete derived target: parent theory must supply Xi_AB and lambda_mem, or prove one factor is zero. The vector curve turns those into numeric pass/fail envelopes.",
            "status": "NONCLAIM_ENVELOPE_READY_PARENT_XI_TARGET_NEXT",
            "best_route": "derive or sign Xi_AB=0; if not, derive Xi_AB and lambda_mem and compare to the envelope.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "status": "PASS_NONCLAIM_ARTIFACTS_WRITTEN",
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
            "reason": "R10 now wants a parent-owned Xi_AB/lambda_mem row or an exact-zero proof.",
            "timestamp_utc": now,
        }
    ]


def has_any_claim(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def validation_rows(
    sources: list[dict[str, Any]],
    qa: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    inverse: list[dict[str, Any]],
    targets: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_groups = [sources, qa, reduction, envelope, inverse, targets, runner, controls, blockers, decisions, status, next_target]
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

    add("VAL4636_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in sources), "all cited local source paths/needles found")
    csv_paths = [
        SOURCE_REGISTER,
        QA_CSV,
        OBSERVABLE_REDUCTION_CSV,
        ENVELOPE_CSV,
        INVERSE_CSV,
        COEFFICIENT_TARGET_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_details = []
    csv_ok = True
    for csv_path in csv_paths:
        try:
            csv_details.append(f"{csv_path.name}:{len(read_csv(csv_path))}")
        except csv.Error as exc:
            csv_ok = False
            csv_details.append(f"{csv_path.name}:CSV_ERROR:{exc}")
    add("VAL4636_01_csv_parse", csv_ok, ";".join(csv_details))
    add("VAL4636_02_curve_qa_passes", all(row["status"].startswith("PASS") or row["status"] == "BLOCKED_NONCLAIM" for row in qa), "curve monotonicity and alpha=1 smoke QA pass")
    add("VAL4636_03_Xi_reduction_present", any("Xi_AB" in row["statement"] for row in reduction), "observable Xi_AB reduction row present")
    add("VAL4636_04_envelope_has_key_lambdas", {"38.6", "100"}.issubset({row["lambda_um"] for row in envelope}), "38.6um and 100um envelope rows present")
    add("VAL4636_05_inverse_has_alpha1_crossing", any(row["Xi_AB_assumed"] == "1" and row["status"] == "CROSSING_FOUND" for row in inverse), "Xi=1 crossing present")
    add("VAL4636_06_runner_live_fail_and_controls", any(row["result"] == "FAIL_CLOSED_MISSING_XI_AND_LAMBDA" for row in runner) and any(row["result"].startswith("PASS") for row in runner) and any(row["result"].startswith("FAIL_VECTOR") for row in runner), "live fail plus pass/fail controls")
    add("VAL4636_07_targets_define_next_parent_row", any(row["target_id"] == "TGT4636_0_XiAB_direct" for row in targets), "parent Xi_AB target present")
    add("VAL4636_08_all_rows_nonclaim", not any(has_any_claim(group) for group in generated_groups), "no generated row promotes a claim")
    add("VAL4636_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4636_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4636_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4636_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4636_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4636_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4636_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4636_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4636_OVERALL", all(row["status"] == "PASS" for row in checks), "4636 R10 Xi envelope checkpoint")
    return checks


def write_docs(
    now: str,
    sources: list[dict[str, Any]],
    qa: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    inverse: list[dict[str, Any]],
    targets: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> None:
    body = f"""# 4636 - R10 Vector Curve QA And Epsilon Coefficient Fill

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

4636 converts the 4635 R10 vector curve into a hard envelope for the observable source-coupling product.

The useful reduction is:

`Xi_AB(lambda_mem) := C_N epsilon_A epsilon_B / Z_min`

and the R10 gate is:

`|Xi_AB| <= alpha_bound(lambda_mem)`.

This is progress because R10 does not need us to separately know `epsilon_A`, `epsilon_B`, `Z_min`, and `C_N` before doing anything. It needs the parent-owned observable product `Xi_AB` plus `lambda_mem`. WEP/PPN still need the split and composition maps, so this does not overclaim.

## Source Register

{markdown_table(sources)}

## Curve QA

{markdown_table(qa)}

## Observable Xi Reduction

{markdown_table(reduction)}

## R10 Epsilon/Xi Envelope

{markdown_table(envelope)}

## Xi To Lambda Max

{markdown_table(inverse)}

## Parent Coefficient Targets

{markdown_table(targets)}

## Runner Results

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
    formal_body = f"""# 652 - PPC4161 R10 Vector Curve QA And Epsilon Coefficient Fill

Marker: `{MARKER}`

Source checkpoint: `{DOC_PATH}`

4636 reduces the R10 local-gravity comparison to the observable product `Xi_AB=C_N epsilon_A epsilon_B/Z_min` and writes the envelope `|Xi_AB| <= alpha_bound(lambda_mem)` using the 4635 vector-extracted Eot-Wash 2020 curve. This is the first concrete numeric map from parent local-branch coefficients to allowed short-range residual strength.

Key read: order-one canonical `Xi_AB` only survives around or below the `~38 um` crossing; by `100 um`, the canonical product must be about `< 0.076`, and by `1 mm` it must be about `< 0.019`, unless the parent zero route gives `Xi_AB=0`.

Decision: `{DECISION}`.

Next: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, formal_body)


def append_integrations() -> None:
    spine_block = f"""
## PPC4161 R10 Vector Curve QA And Epsilon Coefficient Fill 4636

Marker: `{MARKER}`

4636 converts R10 into a concrete parent-coefficient target. The comparison no longer needs to float as separate missing symbols: define `Xi_AB=C_N epsilon_A epsilon_B/Z_min`, then require `|Xi_AB| <= alpha_bound(lambda_mem)`. The extracted curve says order-one `Xi_AB` is only viable near/below the `~38 um` crossing; longer ranges need smaller product coupling or an exact parent zero.

Next: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)
    packet_block = f"""
## PPC4161 Packet - R10 Vector QA Epsilon Envelope 4636

Marker: `{PACKET_MARKER}`

Local packet update: R10 now has a usable envelope. The next proof target is not another broad missing list; it is parent ownership of `Xi_AB` and `lambda_mem`, or a signed exact-zero factor.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def append_claim_register() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "area": "local_gr_empirical_interface",
        "claim": "4636 reduces the R10 bound route to a concrete observable Xi_AB envelope and identifies the next parent coefficient target.",
        "support": "Generated source register, curve QA, Xi reduction, epsilon envelope, inverse lambda rows, parent coefficient targets, runner results, controls, blockers, decision, status, next target and validation.",
        "status": "r10_Xi_envelope_nonclaim",
        "next": NEXT_TARGET,
        "risk": "Fitting Xi_AB from the R10 bound or treating a product R10 gate as WEP/PPN/local-GR completion.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "notes": "No local-GR/Newton/PPN/R10 pass until parent Xi_AB and lambda_mem are derived or exact-zero is signed, and curve QA is promoted.",
    }
    file_exists = CLAIMS_PATH.exists()
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists or CLAIMS_PATH.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    now = utc_now()
    points = load_curve()
    sources = source_rows(now)
    qa = qa_rows(now, points)
    reduction = observable_reduction_rows(now)
    envelope = envelope_rows(now, points)
    inverse = inverse_rows(now, points)
    targets = coefficient_target_rows(now)
    runner = runner_rows(now, points)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    status = status_rows(now)
    next_target = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QA_CSV, qa)
    write_csv(OBSERVABLE_REDUCTION_CSV, reduction)
    write_csv(ENVELOPE_CSV, envelope)
    write_csv(INVERSE_CSV, inverse)
    write_csv(COEFFICIENT_TARGET_CSV, targets)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_docs(now, sources, qa, reduction, envelope, inverse, targets, runner, controls, blockers, decisions)
    append_integrations()
    append_claim_register()

    validation = validation_rows(sources, qa, reduction, envelope, inverse, targets, runner, controls, blockers, decisions, status, next_target)
    write_csv(VALIDATION_CSV, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {VALIDATION_CSV}")
    print(f"next {NEXT_TARGET}")


if __name__ == "__main__":
    main()
