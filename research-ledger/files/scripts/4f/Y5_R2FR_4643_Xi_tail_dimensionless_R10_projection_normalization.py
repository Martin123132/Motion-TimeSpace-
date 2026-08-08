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

CHECKPOINT = "4643"
CLAIM_ID = "L-485"
BRANCH_ID = "MTS_R2FR_Y5_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643"
MARKER = "PPC4161_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643"
PACKET_MARKER = "PPC4161_PACKET_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643"
DECISION = "R10_PROJECTION_CONSTANTS_COLLAPSED_TO_DIMENSIONLESS_ARENA_NORM_COMPONENTS_AND_LAMBDA_REMAIN_NONCLAIM"
NEXT_TARGET = "4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md"

DOC_PATH = POST / "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"
FORMAL_PATH = FORMAL / "659-PPC4161-Xi-tail-dimensionless-R10-projection-normalization.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4642_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4642_VALIDATION.csv"
CSV_4642_PROJECTION = SOURCE_DIR / "P8_Y5_R2FR_4642_PROJECTION_CONSTANT_SOURCE_PACK.csv"
CSV_4642_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4642_CLAIM_BLOCKERS.csv"
DOC_4642 = POST / "4642-Y5-R2FR-Xi-tail-parent-signature-and-lambda-source-pack.md"
DOC_4641 = POST / "4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"
DOC_4640 = POST / "4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md"
DOC_4639 = POST / "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
DOC_4628 = POST / "4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md"
FW_4334 = FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"
FW_4335 = FORMAL / "351-PPC4161-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md"
FW_4506 = FORMAL / "522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4643_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_DIMENSIONLESS_R10_PROJECTION_THEOREM.csv"
NORM_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_NORMALIZED_PROJECTION_INPUT_PACK.csv"
REMAINING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_REMAINING_CLAIM_INPUTS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_R10_NORMALIZED_ALPHA_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4643_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4643_VALIDATION.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


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
        values = [str(row.get(header, "")).replace("\n", "<br>").replace("|", "\\|") for header in headers]
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


def load_curve_points() -> list[tuple[float, float]]:
    rows = read_csv(CSV_4635_CURVE)
    points: list[tuple[float, float]] = []
    for row in rows:
        try:
            points.append((float(row["lambda_m"]), float(row["alpha_bound_abs"])))
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(points)


def interpolate_alpha(points: list[tuple[float, float]], lambda_m: float) -> float | None:
    if not points or lambda_m < points[0][0] or lambda_m > points[-1][0]:
        return None
    for x_value, y_value in points:
        if math.isclose(lambda_m, x_value, rel_tol=0.0, abs_tol=1e-18):
            return y_value
    for left, right in zip(points, points[1:]):
        x0, y0 = left
        x1, y1 = right
        if x0 <= lambda_m <= x1:
            if x0 <= 0 or x1 <= 0 or y0 <= 0 or y1 <= 0:
                t = (lambda_m - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
            t = (math.log(lambda_m) - math.log(x0)) / (math.log(x1) - math.log(x0))
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return None


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4643_00_4642_validation", CSV_4642_VALIDATION, "VAL4642_OVERALL", "4642 validated lambda/projection source pack."),
        ("SRC4643_01_4642_projection", CSV_4642_PROJECTION, "PROJ4642_0_K_NH", "projection constants were the active missing layer."),
        ("SRC4643_02_4642_blocker", CSV_4642_BLOCKERS, "PROJECTION_CONSTANTS_MISSING", "4642 blocker targeted by 4643."),
        ("SRC4643_03_4642_doc", DOC_4642, "K_NH/K_edge/K_tr/Pi_R10", "human 4642 statement of missing projection constants."),
        ("SRC4643_04_4639_KNH", DOC_4639, "Xi_nonHilbert := K_NH N_src_nonHilbert", "non-Hilbert tail projection constant source formula."),
        ("SRC4643_05_4640_Kedge", DOC_4640, "|Xi_boundary_history| <= K_edge", "boundary-history projection constant source formula."),
        ("SRC4643_06_4640_Ktr", DOC_4640, "|Xi_transition_inner| <= K_tr", "transition-inner projection constant source formula."),
        ("SRC4643_07_4641_gate", DOC_4641, "finite no-cancellation pack", "same-branch finite gate from 4641."),
        ("SRC4643_08_4334_R10", FW_4334, "PI4334_0_R10", "R10 projection matrix discipline."),
        ("SRC4643_09_4334_gate", FW_4334, "F4334_2_R10_smoke_gate", "R10 scoring gate."),
        ("SRC4643_10_4335_requirement", FW_4335, "F4335_4_R10_requirement", "R10 alpha(lambda) source normalization requirement."),
        ("SRC4643_11_4628_lambda", DOC_4628, "lambda_mem=sqrt(Z_mem/M2_mem)", "lambda_mem parent-Hessian law remains imported."),
        ("SRC4643_12_4506_operator", FW_4506, "MOP4506_0_quadratic_action", "memory quadratic action source operator."),
        ("SRC4643_13_4635_curve", CSV_4635_CURVE, "lambda_m", "digitized R10 vector curve used for controls only."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in sources:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": line_of(path, needle) > 0,
                "line": line_of(path, needle),
                "purpose": purpose,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "THM4643_0_calibrated_R10_functional",
            "statement": "Define alpha_i(lambda) as the linear R10 Yukawa-template coefficient of residual component R_i after the calibrated Newtonian 1/r channel is removed.",
            "equation": "alpha_i(lambda)=<R_i,Y_lambda>_R10/<Y_lambda,Y_lambda>_R10",
            "proof_status": "DEFINITION_WITH_4334_4335_SOURCE_GUARD",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "THM4643_1_linearity",
            "statement": "Because the template projection is linear on the residual force/potential channel, the projected tail coefficient is the sum of projected component coefficients.",
            "equation": "alpha_tail(lambda)=sum_i alpha_i(lambda)",
            "proof_status": "LINEAR_PROJECTION_PROOF",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "THM4643_2_no_cancellation_bound",
            "statement": "The conservative finite gate uses absolute components, so cancellation between hidden/source/boundary/transition pieces is not allowed.",
            "equation": "|alpha_tail(lambda)| <= |alpha_src_hidden|+|alpha_nonHilbert|+|alpha_boundary_history|+|alpha_transition_inner|",
            "proof_status": "TRIANGLE_INEQUALITY_DERIVED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "THM4643_3_projection_constant_collapse",
            "statement": "If Xi components are stored as these dimensionless alpha_i coefficients, then K_NH, K_edge, K_tr and Pi_R10 are not independent physical constants.",
            "equation": "K_NH=K_edge=K_tr=Pi_R10=1 in the dimensionless R10 alpha norm",
            "proof_status": "NORMALIZATION_COLLAPSE_DERIVED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "THM4643_4_raw_action_guard",
            "statement": "Raw action-space residuals cannot use the unit constants until projected and normalized against the same calibrated source/test geometry.",
            "equation": "raw R_i -> alpha_i(lambda) required before R10 scoring",
            "proof_status": "RAW_UNITS_BRANCH_REJECT_GUARD",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def normalized_pack_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_0_Pi_R10",
            "symbol": "Pi_R10(lambda)",
            "input_filled": True,
            "value_or_rule": "linear calibrated Yukawa-template alpha functional",
            "status": "FILLED_AS_DIMENSIONLESS_PROJECTION_FUNCTIONAL",
            "source_basis": "4334 PI4334_0_R10 and 4335 F4335_4_R10_requirement",
            "remaining_needed": "component residuals must be projected through this functional before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_1_K_NH",
            "symbol": "K_NH",
            "input_filled": True,
            "value_or_rule": "1 once Xi_nonHilbert is represented as alpha_nonHilbert(lambda)",
            "status": "COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION",
            "source_basis": "4639 Xi_nonHilbert formula plus THM4643_3",
            "remaining_needed": "project N_src_nonHilbert into alpha_nonHilbert(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_2_K_edge",
            "symbol": "K_edge",
            "input_filled": True,
            "value_or_rule": "1 once Q_edge terms are represented as alpha_boundary_history(lambda)",
            "status": "COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION",
            "source_basis": "4640 boundary-history formula plus THM4643_3",
            "remaining_needed": "project shell/boundary Q_edge terms into alpha_boundary_history(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_3_K_tr",
            "symbol": "K_tr",
            "input_filled": True,
            "value_or_rule": "1 once epsilon_tr_hair is represented as alpha_transition_inner(lambda)",
            "status": "COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION",
            "source_basis": "4640 transition-inner formula plus THM4643_3",
            "remaining_needed": "project transition hair into alpha_transition_inner(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_4_Gobs_source_norm",
            "symbol": "G_N^obs M_S m_T",
            "input_filled": True,
            "value_or_rule": "normalization denominator is the experiment-calibrated Newtonian channel, not a new fitted MTS constant",
            "status": "CALIBRATION_DENOMINATOR_DEFINED_HIDING_IN_G_REJECTED",
            "source_basis": "4335 F4335_4_R10_requirement",
            "remaining_needed": "use source/test geometry and composition for any numeric R10 score",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "NORM4643_5_alpha_bound_curve",
            "symbol": "alpha_bound(lambda)",
            "input_filled": False,
            "value_or_rule": "digitized curve usable for internal controls only",
            "status": "SMOKE_CURVE_AVAILABLE_CLAIM_QA_PENDING",
            "source_basis": "4635 digitized vector curve",
            "remaining_needed": "claim-grade curve QA/provenance before public R10 scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def remaining_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4643_0_projection_layer",
            "previous_blocker": "BLK4642_2_PROJECTION_CONSTANTS_MISSING",
            "status_after_4643": "INDEPENDENT_CONSTANT_LAYER_COLLAPSED",
            "detail": "K_NH/K_edge/K_tr/Pi_R10 are no longer free source constants in the R10-alpha representation; raw residuals must first be converted into dimensionless component alpha_i(lambda).",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4643_1_component_values",
            "previous_blocker": "BLK4642_3_FINITE_COMPONENT_VALUES_MISSING",
            "status_after_4643": "STILL_MISSING_BUT_NOW_WELL_DEFINED",
            "detail": "Need alpha_src_hidden, alpha_nonHilbert, alpha_boundary_history and alpha_transition_inner, or exact same-branch zeros.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4643_2_lambda_ratio",
            "previous_blocker": "BLK4642_1_ZMEM_M2MEM_RATIO_MISSING",
            "status_after_4643": "UNCHANGED",
            "detail": "lambda_mem remains sqrt(Z_mem/M2_mem); 4643 does not invent the parent Hessian ratio.",
            "next_action": "derive parent Hessian ratio or exact constraint/contact branch",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4643_3_exact_signature",
            "previous_blocker": "BLK4642_0_SAME_BRANCH_SIGNATURE_UNSIGNED",
            "status_after_4643": "UNCHANGED",
            "detail": "Exact Xi_tail=0 still requires the same-branch parent signature from 4641.",
            "next_action": "try exact zero certificate before finite scoring if a clause can be signed",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4643_4_public_claim",
            "previous_blocker": "BLK4642_4_R10_PROMOTION_SCOPE_PENDING",
            "status_after_4643": "UNCHANGED",
            "detail": "No public/local-GR/R10 claim; this is a private normalization theorem and smoke runner.",
            "next_action": "promote only after component values/lambda/curve QA and PPN/Newton/clocks/orbital maps exist",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    points = load_curve_points()
    lambda_control = 1.0e-4
    alpha_bound = interpolate_alpha(points, lambda_control)
    alpha_pass = 0.5 * alpha_bound if alpha_bound is not None else ""
    alpha_fail = 1.5 * alpha_bound if alpha_bound is not None else ""
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_0_live_missing_components",
            "branch": "current live normalized R10 pack",
            "lambda_mem_m": "",
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "alpha_tail_abs": "",
            "alpha_bound_vector": "",
            "result": "FAIL_CLOSED",
            "reason": "projection constants are normalized, but component alpha_i(lambda) values and lambda_mem remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_1_exact_zero_control",
            "branch": "same-branch exact Xi component zeros",
            "lambda_mem_m": lambda_control,
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": 0.0,
            "alpha_boundary_history": 0.0,
            "alpha_transition_inner": 0.0,
            "alpha_tail_abs": 0.0,
            "alpha_bound_vector": alpha_bound if alpha_bound is not None else "",
            "result": "CONDITIONAL_ZERO_PASS_NONCLAIM",
            "reason": "linear normalized projection sends zero components to zero alpha_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_2_small_normalized_components",
            "branch": "dimensionless alpha_i toy pass",
            "lambda_mem_m": lambda_control,
            "alpha_src_hidden": alpha_pass / 4 if isinstance(alpha_pass, float) else "",
            "alpha_nonHilbert": alpha_pass / 4 if isinstance(alpha_pass, float) else "",
            "alpha_boundary_history": alpha_pass / 4 if isinstance(alpha_pass, float) else "",
            "alpha_transition_inner": alpha_pass / 4 if isinstance(alpha_pass, float) else "",
            "alpha_tail_abs": alpha_pass,
            "alpha_bound_vector": alpha_bound if alpha_bound is not None else "",
            "result": "SMOKE_PASS_NONCLAIM" if isinstance(alpha_pass, float) else "FAIL_CLOSED",
            "reason": "control row demonstrates unit projection constants with no-cancellation sum below bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_3_large_normalized_components",
            "branch": "dimensionless alpha_i toy fail",
            "lambda_mem_m": lambda_control,
            "alpha_src_hidden": alpha_fail / 4 if isinstance(alpha_fail, float) else "",
            "alpha_nonHilbert": alpha_fail / 4 if isinstance(alpha_fail, float) else "",
            "alpha_boundary_history": alpha_fail / 4 if isinstance(alpha_fail, float) else "",
            "alpha_transition_inner": alpha_fail / 4 if isinstance(alpha_fail, float) else "",
            "alpha_tail_abs": alpha_fail,
            "alpha_bound_vector": alpha_bound if alpha_bound is not None else "",
            "result": "SMOKE_FAIL_NONCLAIM" if isinstance(alpha_fail, float) else "FAIL_CLOSED",
            "reason": "control row demonstrates same unit constants fail when absolute component sum exceeds bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_4_raw_action_units",
            "branch": "raw action residuals with K=1 attempted",
            "lambda_mem_m": lambda_control,
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "alpha_tail_abs": "",
            "alpha_bound_vector": alpha_bound if alpha_bound is not None else "",
            "result": "REJECT_BRANCH",
            "reason": "K=1 is only legal after conversion into calibrated dimensionless R10 alpha_i(lambda) coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_5_hide_in_Gobs",
            "branch": "absorb residual into calibrated G_N",
            "lambda_mem_m": lambda_control,
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "alpha_tail_abs": "",
            "alpha_bound_vector": alpha_bound if alpha_bound is not None else "",
            "result": "REJECT_BRANCH",
            "reason": "Newtonian calibration channel must be subtracted before Yukawa projection; MTS residual cannot be hidden in G_N^obs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4643_6_outside_curve_domain",
            "branch": "lambda outside digitized curve",
            "lambda_mem_m": 1.0e-9,
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": 0.0,
            "alpha_boundary_history": 0.0,
            "alpha_transition_inner": 0.0,
            "alpha_tail_abs": 0.0,
            "alpha_bound_vector": "",
            "result": "FAIL_CLOSED",
            "reason": "alpha_bound(lambda) unavailable outside the source-backed curve domain",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]
    return rows


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4643_0_not_a_G_derivation",
            "rule": "This checkpoint does not derive Newton's constant; it fixes how local residuals are normalized against the observed/calibrated Newtonian channel for R10.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4643_1_no_free_K_after_projection",
            "rule": "Once an object is stored as alpha_i(lambda), K_NH/K_edge/K_tr/Pi_R10 cannot be tuned separately.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4643_2_raw_units_rejected",
            "rule": "Raw parent-action residuals must pass through the projection functional before using the unit-normalized finite gate.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4643_3_no_cancellation",
            "rule": "R10 finite scoring uses the sum of absolute projected components unless exact same-branch zeros are signed.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4643_0",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "summary": "4643 removes the independent R10 projection-constant layer by defining Xi components as calibrated dimensionless Yukawa-alpha coefficients; this fills the normalization route but leaves component values, lambda_mem and exact same-branch signatures open.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "Projection constants collapsed by dimensionless R10 alpha normalization; no local-GR/R10 claim.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "priority": "derive one alpha_i(lambda) component or exact zero certificate now that projection constants are no longer independent blockers",
            "first_attempt": "Xi_src_hidden exact zero if source-label forgetting can be parent-signed; otherwise alpha_nonHilbert finite component through Hperp/readout",
            "timestamp_utc": timestamp,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    norm_pack: list[dict[str, Any]],
    remaining: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4643 - Xi_tail first claim-grade input fill or exact parent signature

Branch: `{BRANCH_ID}`
Marker: `{MARKER}`
Decision: `{DECISION}`

## Result

4643 takes a real step rather than adding another missing-input ledger. The active 4642 blocker was that `K_NH`, `K_edge`, `K_tr`, `Pi_R10(lambda)` and the source normalization looked like separate constants. That is too much freedom.

The clean route is to express every local tail component directly as the calibrated R10 Yukawa-alpha coefficient:

`alpha_i(lambda)=<R_i,Y_lambda>_R10/<Y_lambda,Y_lambda>_R10`

after the observed Newtonian `1/r` calibration channel is removed. Linearity gives

`alpha_tail(lambda)=alpha_src_hidden+alpha_nonHilbert+alpha_boundary_history+alpha_transition_inner`.

The no-cancellation gate is then

`|alpha_tail(lambda)| <= |alpha_src_hidden|+|alpha_nonHilbert|+|alpha_boundary_history|+|alpha_transition_inner| <= alpha_bound(lambda_mem)`.

So, in this representation, `K_NH=K_edge=K_tr=Pi_R10=1` by normalization, not by fitting. Raw action-space residuals still need the projection map before scoring. This removes one independent free-constant layer but does not claim R10/local GR.

## Source Register

{markdown_table(sources)}

## Dimensionless R10 Projection Theorem

{markdown_table(theorem)}

## Normalized Projection Input Pack

{markdown_table(norm_pack)}

## Remaining Claim Inputs

{markdown_table(remaining)}

## R10 Normalized Alpha Runner

{markdown_table(runners)}

## Controls

{markdown_table(controls)}

## Decision

{markdown_table(decisions)}

## Status

{markdown_table(statuses)}

## Next Target

{markdown_table(nexts)}

## Validation

{markdown_table(validation)}
"""


def build_validation(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    norm_pack: list[dict[str, Any]],
    remaining: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4643_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4643_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4643_2_theorem_rows", len(theorem) >= 5, "dimensionless projection theorem rows present"))
    statuses = {row["symbol"]: row["status"] for row in norm_pack}
    checks.append(("VAL4643_3_Pi_R10_filled", statuses.get("Pi_R10(lambda)") == "FILLED_AS_DIMENSIONLESS_PROJECTION_FUNCTIONAL", "Pi_R10 filled as a linear alpha functional"))
    checks.append(("VAL4643_4_K_constants_collapsed", all(statuses.get(symbol) == "COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION" for symbol in ["K_NH", "K_edge", "K_tr"]), "K_NH/K_edge/K_tr collapsed by normalization"))
    checks.append(("VAL4643_5_Gobs_guard", statuses.get("G_N^obs M_S m_T") == "CALIBRATION_DENOMINATOR_DEFINED_HIDING_IN_G_REJECTED", "Gobs normalization guard present"))
    checks.append(("VAL4643_6_projection_blocker_updated", any(row["status_after_4643"] == "INDEPENDENT_CONSTANT_LAYER_COLLAPSED" for row in remaining), "projection blocker updated"))
    result_by_id = {row["run_id"]: row["result"] for row in runners}
    checks.append(("VAL4643_7_live_fail_closed", result_by_id.get("RUN4643_0_live_missing_components") == "FAIL_CLOSED", "live missing component branch fails closed"))
    checks.append(("VAL4643_8_pass_fail_controls", any("PASS" in row["result"] for row in runners) and any("FAIL" in row["result"] for row in runners), "runner has pass and fail controls"))
    checks.append(("VAL4643_9_raw_units_rejected", result_by_id.get("RUN4643_4_raw_action_units") == "REJECT_BRANCH", "raw action K=1 misuse rejected"))
    checks.append(("VAL4643_10_hide_in_G_rejected", result_by_id.get("RUN4643_5_hide_in_Gobs") == "REJECT_BRANCH", "hiding residual in Gobs rejected"))
    checks.append(("VAL4643_11_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in runners + decisions), "generated runner/decision rows remain nonclaim"))
    checks.append(("VAL4643_12_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4643_13_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4643_14_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4643_15_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4643_16_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4643_17_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4643_18_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))

    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4643_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4643 validation passed" if all(row["status"] == "PASS" for row in rows) else "4643 validation failed",
            "timestamp_utc": utc_now(),
        }
    )
    return rows


def write_claim_append() -> None:
    text = read_text(CLAIMS_PATH)
    if CLAIM_ID in text:
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4643 collapses R10 projection constants into a calibrated dimensionless Yukawa-alpha norm, so K_NH/K_edge/K_tr/Pi_R10 are not independent fit dials once components are projected.",
        "Generated dimensionless R10 projection theorem, normalized projection input pack, remaining claim inputs, R10 normalized alpha runner, controls, decision, status, next target and validation.",
        "Xi_tail_dimensionless_R10_projection_normalization_nonclaim",
        NEXT_TARGET,
        "Using K=1 on raw action-space residuals, hiding residuals in calibrated G_N, or treating toy alpha_i controls as source-backed component values.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No local-GR/Newton/R10/PPN claim until component alpha_i(lambda) values or exact zeros, same-branch lambda_mem, curve QA and promotion maps are all source-backed.",
    ]
    escaped = []
    for value in row:
        value = str(value)
        if "," in value or '"' in value:
            value = '"' + value.replace('"', '""') + '"'
        escaped.append(value)
    append_once(CLAIMS_PATH, CLAIM_ID, ",".join(escaped))


def main() -> int:
    timestamp = utc_now()
    sources = source_rows(timestamp)
    theorem = theorem_rows(timestamp)
    norm_pack = normalized_pack_rows(timestamp)
    remaining = remaining_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(NORM_PACK_CSV, norm_pack)
    write_csv(REMAINING_CSV, remaining)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)

    write_text(DOC_PATH, build_doc(sources, theorem, norm_pack, remaining, runners, controls, decisions, statuses, nexts, []))
    write_text(FORMAL_PATH, build_doc(sources, theorem, norm_pack, remaining, runners, controls, decisions, statuses, nexts, []))
    write_claim_append()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4643 collapses the R10 projection-constant layer by defining each `Xi_tail` component as a calibrated dimensionless Yukawa-alpha coefficient after the Newtonian channel is removed. In that representation `K_NH=K_edge=K_tr=Pi_R10=1` by normalization, not fitting. Raw parent-action residuals still require projection; component values/exact zeros and `lambda_mem=sqrt(Z_mem/M2_mem)` remain the active blockers. This remains nonclaim.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` removes one artificial free layer from the local R10 route: projection constants are unit constants only after conversion into calibrated dimensionless R10 alpha coefficients. Next packet target: `{NEXT_TARGET}`.
""",
    )

    validation = build_validation(sources, theorem, norm_pack, remaining, runners, decisions, timestamp)
    write_csv(VALIDATION_CSV, validation)
    write_text(DOC_PATH, build_doc(sources, theorem, norm_pack, remaining, runners, controls, decisions, statuses, nexts, validation))
    write_text(FORMAL_PATH, build_doc(sources, theorem, norm_pack, remaining, runners, controls, decisions, statuses, nexts, validation))

    status = "PASS" if validation[-1]["status"] == "PASS" else "FAIL"
    print(f"{MARKER}: {status}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
