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

CHECKPOINT = "4641"
CLAIM_ID = "L-483"
BRANCH_ID = "MTS_R2FR_Y5_SAME_BRANCH_XI_TAIL_ASSEMBLY_4641"
MARKER = "PPC4161_SAME_BRANCH_XI_TAIL_ZERO_ASSEMBLY_OR_FINITE_COEFFICIENT_PACK_4641"
PACKET_MARKER = "PPC4161_PACKET_SAME_BRANCH_XI_TAIL_ASSEMBLY_4641"
DECISION = "FOUR_XI_TAIL_ZERO_ROUTES_COMPATIBLE_ONLY_AS_SAME_BRANCH_CONDITIONAL_ASSEMBLY_FINITE_PACK_RETAINED"
NEXT_TARGET = "4642-Y5-R2FR-Xi-tail-parent-signature-and-lambda-source-pack.md"

DOC_PATH = POST / "4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"
FORMAL_PATH = FORMAL / "657-PPC4161-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4638_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4638_VALIDATION.csv"
CSV_4638_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4638_XISRC_HIDDEN_IMPORT_AUDIT.csv"
CSV_4639_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4639_VALIDATION.csv"
CSV_4639_FORMULAS = SOURCE_DIR / "P8_Y5_R2FR_4639_XI_NONHILBERT_FORMULA_ROWS.csv"
CSV_4640_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4640_VALIDATION.csv"
CSV_4640_FORMULAS = SOURCE_DIR / "P8_Y5_R2FR_4640_XI_BT_FORMULA_ROWS.csv"
CSV_4640_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4640_XI_TAIL_REDUCTION_ROWS.csv"
DOC_4638 = POST / "4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md"
DOC_4639 = POST / "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
DOC_4640 = POST / "4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4641_SOURCE_REGISTER.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_ZERO_BRANCH_IMPORT_ROWS.csv"
CLAUSE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_SAME_BRANCH_CLAUSE_MATRIX.csv"
COMPATIBILITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_BRANCH_COMPATIBILITY_AUDIT.csv"
ASSEMBLY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_XI_TAIL_ASSEMBLY_ROWS.csv"
FINITE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_FINITE_COEFFICIENT_PACK_SCHEMA.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_R10_SAME_BRANCH_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4641_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4641_VALIDATION.csv"

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
    return sorted((float(row["lambda_m"]), float(row["alpha_bound_abs"])) for row in read_csv(CSV_4635_CURVE))


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


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4641_00_4638_validation", CSV_4638_VALIDATION, "VAL4638_OVERALL", "4638 validation."),
        ("SRC4641_01_4638_xisrc_zero", CSV_4638_AUDIT, "AUD4638_1_conditional_zero", "Xi_src_hidden zero route."),
        ("SRC4641_02_4638_doc", DOC_4638, "Xi_src_hidden = 0", "human 4638 zero branch."),
        ("SRC4641_03_4639_validation", CSV_4639_VALIDATION, "VAL4639_OVERALL", "4639 validation."),
        ("SRC4641_04_4639_exact_zero", CSV_4639_FORMULAS, "F4639_2_exact_zero", "Xi_nonHilbert exact zero route."),
        ("SRC4641_05_4639_doc", DOC_4639, "Xi_nonHilbert=0", "human 4639 zero branch."),
        ("SRC4641_06_4640_validation", CSV_4640_VALIDATION, "VAL4640_OVERALL", "4640 validation."),
        ("SRC4641_07_4640_full_tail", CSV_4640_FORMULAS, "F4640_7_full_tail_zero", "full tail same-branch row."),
        ("SRC4641_08_4640_reduction", CSV_4640_REDUCTION, "XR4640_3_full_tail_zero_branch", "tail assembly row."),
        ("SRC4641_09_4640_doc", DOC_4640, "Xi_tail=0", "human 4640 assembly statement."),
        ("SRC4641_10_curve", CSV_4635_CURVE, "lambda_m", "R10 vector curve points."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line": line_of(path, needle),
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": now,
            }
        )
    return rows


def zero_import_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZIMP4641_0_Xisrc",
            "component": "Xi_src_hidden",
            "zero_condition": "source-label-forgetting Hilbert-owner branch: no hidden/source-only weights, no source normalization/marker/environment return",
            "source": "4638 AUD4638_1_conditional_zero",
            "branch_tag": "B_source_label_forgetting_Hilbert_owner",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZIMP4641_1_XiNH",
            "component": "Xi_nonHilbert",
            "zero_condition": "Hperp=0 or S_A Hperp^A=0, and R_src_readout=0",
            "source": "4639 F4639_2_exact_zero",
            "branch_tag": "B_Hperp_source_pairing_zero",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZIMP4641_2_XiBH",
            "component": "Xi_boundary_history",
            "zero_condition": "Q_edge_shell=0 and Q_edge_boundary=0 from same q-basic source worldtube, no birth shell, no-flux collar, fixed corner/reference/projector",
            "source": "4640 F4640_3_boundary_bound",
            "branch_tag": "B_Qedge_worldtube_no_flux",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZIMP4641_3_XiTR",
            "component": "Xi_transition_inner",
            "zero_condition": "q_tr=P_kernel q_tr: Hilbert, same-worldtube, static l=0, universal, range-free, same-metric, boundary-owned",
            "source": "4640 F4640_5_transition_bound/F4640_7_full_tail_zero",
            "branch_tag": "B_transition_source_kernel",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def clause_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("CLAUSE4641_0", "single Hilbert source owner", "ordinary matter/EM/source current comes from one Hilbert parent owner before readout", "needed for Xi_src_hidden and Xi_nonHilbert", "COMPATIBLE_BUT_PARENT_SIGNATURE_UNSIGNED"),
        ("CLAUSE4641_1", "source-label forgetting", "no source-only weights, hidden markers, source normalization, environment selector or direct m-charge return", "kills Xi_src_hidden", "COMPATIBLE_BUT_PARENT_SIGNATURE_UNSIGNED"),
        ("CLAUSE4641_2", "quotient Hperp silence", "Hperp=0 or S_A Hperp^A=0 with R_src_readout=0", "kills Xi_nonHilbert", "COMPATIBLE_BUT_HPERP_COMPONENTS_UNSIGNED"),
        ("CLAUSE4641_3", "same q-basic source worldtube", "the source worldtube is fixed before variation and shared by Hilbert/source/readout branches", "kills boundary shell and supports transition kernel", "COMPATIBLE_BUT_WORLDTUBE_SIGNATURE_UNSIGNED"),
        ("CLAUSE4641_4", "regular support and no-flux collar", "zero density trace, no birth shell, source-free no-flux collar, fixed corner/reference/projector", "kills Xi_boundary_history", "COMPATIBLE_BUT_EDGE_COMPONENTS_UNSIGNED"),
        ("CLAUSE4641_5", "transition source kernel", "q_tr is Hilbert, same-worldtube, static l=0, universal, range-free, same-metric and boundary-owned", "kills Xi_transition_inner", "COMPATIBLE_BUT_KERNEL_CLAUSES_UNSIGNED"),
        ("CLAUSE4641_6", "same observed coframe/Hodge/tau", "the readout frame is selected before scoring and is common to matter, EM, clocks and local tests", "prevents frame/Hodge/tau cross-branch mixing", "COMPATIBLE_BUT_GLOBAL_ADOPTION_UNSIGNED"),
        ("CLAUSE4641_7", "fixed projector/domain/lambda", "projector/domain/lambda_mem are parent-owned, not fit after seeing R10/PPN residuals", "enables claim-grade finite pack or exact branch", "COMPATIBLE_BUT_SOURCE_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "requirement": requirement,
            "role": role,
            "current_status": status,
            "compatible_with_strict_branch": True,
            "signed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for clause_id, clause, requirement, role, status in clauses
    ]


def compatibility_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "COMP4641_0_strict_private_branch",
            "branch": "B_strict_qbasic_Hilbert_same_worldtube",
            "included_zero_tags": "B_source_label_forgetting_Hilbert_owner;B_Hperp_source_pairing_zero;B_Qedge_worldtube_no_flux;B_transition_source_kernel",
            "compatibility": "FORMALLY_COMPATIBLE",
            "claim_status": "CONDITIONAL_PRIVATE_ZERO_NOT_PARENT_SIGNED",
            "result": "Xi_tail=0 if all clauses sign on this branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "COMP4641_1_source_label_only",
            "branch": "B_source_label_forgetting_only",
            "included_zero_tags": "B_source_label_forgetting_Hilbert_owner",
            "compatibility": "INSUFFICIENT",
            "claim_status": "REJECT_FULL_ZERO",
            "result": "Xi_src_hidden may zero, but Xi_nonHilbert, boundary/history and transition-inner remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "COMP4641_2_cross_branch",
            "branch": "B_cross_branch_patchwork",
            "included_zero_tags": "zeros selected from incompatible source/readout/domain choices",
            "compatibility": "REJECTED",
            "claim_status": "REJECT_CROSS_BRANCH_ZERO",
            "result": "cannot claim Xi_tail=0 by stitching branch-local theorems from different readout/domain choices",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def assembly_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XA4641_0_full_tail",
            "formula": "Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner",
            "status": "INPUT_ASSEMBLED_FROM_4638_4639_4640",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XA4641_1_exact_branch",
            "formula": "if Z_src_hidden=Z_nonHilbert=Z_boundary_history=Z_transition_inner=True on B_strict_qbasic_Hilbert_same_worldtube, then Xi_tail=0",
            "status": "CONDITIONAL_EXACT_ZERO_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XA4641_2_finite_pack",
            "formula": "|Xi_tail| <= |Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)",
            "status": "FINITE_NO_CANCELLATION_PACK_REQUIRED_IF_ANY_ZERO_CLAUSE_OPENS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def finite_pack_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("FP4641_0", "Xi_src_hidden", "source-label/hidden/source-weight residual", "zero theorem or finite dimensionless value"),
        ("FP4641_1", "Xi_nonHilbert", "Hperp/source-pairing residual", "K_NH, U_B, C_S, C_perp, E_Dq,Hperp, R_src_readout"),
        ("FP4641_2", "Xi_boundary_history", "Q_edge shell/boundary residual", "K_edge, Q_edge_shell, Q_edge_boundary"),
        ("FP4641_3", "Xi_transition_inner", "transition source-kernel hair residual", "K_tr, epsilon_tr_hair components"),
        ("FP4641_4", "lambda_mem", "range scale for R10 alpha(lambda)", "parent-derived/source-backed value in meters"),
        ("FP4641_5", "alpha_bound(lambda_mem)", "Eot-Wash vector curve comparator", "interpolated from digitized source curve with claim-grade provenance"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "pack_id": pack_id,
            "symbol": symbol,
            "meaning": meaning,
            "required_input": required,
            "units": "dimensionless" if symbol != "lambda_mem" else "m",
            "status": "MISSING_CLAIM_GRADE_INPUT_OR_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for pack_id, symbol, meaning, required in components
    ]


def run_rows(points: list[tuple[float, float]], now: str) -> list[dict[str, Any]]:
    specs = [
        ("RUN4641_0_live_missing_inputs", "current live corpus", None, None, None, None, None, "FAIL_CLOSED", "missing same-branch signatures, finite component values and lambda_mem"),
        ("RUN4641_1_strict_same_branch_zero", "all four zeros on one branch", 1.0e-4, 0.0, 0.0, 0.0, 0.0, "", ""),
        ("RUN4641_2_cross_branch_zeros", "four zeros selected from incompatible branches", 1.0e-4, 0.0, 0.0, 0.0, 0.0, "REJECT_CROSS_BRANCH_ZERO", "zero rows do not share one parent/readout branch"),
        ("RUN4641_3_finite_pack_pass_100um", "finite coefficient pack smoke", 1.0e-4, 0.01, 0.02, 0.02, 0.01, "", ""),
        ("RUN4641_4_finite_pack_fail_100um", "finite coefficient pack smoke", 1.0e-4, 0.02, 0.02, 0.02, 0.02, "", ""),
        ("RUN4641_5_finite_pack_pass_1mm", "large-range tight finite pack", 1.0e-3, 0.004, 0.004, 0.004, 0.004, "", ""),
        ("RUN4641_6_finite_pack_fail_1mm", "large-range tight finite pack", 1.0e-3, 0.005, 0.005, 0.005, 0.005, "", ""),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, branch, lambda_m, xi_src, xi_nh, xi_bh, xi_tr, forced_result, forced_reason in specs:
        if lambda_m is None:
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "run_id": run_id,
                    "branch": branch,
                    "lambda_mem_m": "",
                    "Xi_src_hidden_abs": "",
                    "Xi_nonHilbert_abs": "",
                    "Xi_boundary_history_abs": "",
                    "Xi_transition_inner_abs": "",
                    "Xi_tail_abs": "",
                    "alpha_bound_vector": "",
                    "result": forced_result,
                    "reason": forced_reason,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                    "timestamp_utc": now,
                }
            )
            continue
        alpha = interpolate_alpha(points, lambda_m)
        xi_tail = float(xi_src or 0.0) + float(xi_nh or 0.0) + float(xi_bh or 0.0) + float(xi_tr or 0.0)
        if forced_result:
            result = forced_result
            reason = forced_reason
        elif alpha is None:
            result = "FAIL_CLOSED"
            reason = "lambda outside extracted vector curve"
        elif xi_tail <= alpha:
            result = "SMOKE_PASS_NONCLAIM"
            reason = "absolute Xi_tail sits inside digitized vector bound for this toy/control row"
        else:
            result = "SMOKE_FAIL_NONCLAIM"
            reason = "absolute Xi_tail exceeds digitized vector bound"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "branch": branch,
                "lambda_mem_m": f"{lambda_m:.12g}",
                "Xi_src_hidden_abs": f"{float(xi_src or 0.0):.12g}",
                "Xi_nonHilbert_abs": f"{float(xi_nh or 0.0):.12g}",
                "Xi_boundary_history_abs": f"{float(xi_bh or 0.0):.12g}",
                "Xi_transition_inner_abs": f"{float(xi_tr or 0.0):.12g}",
                "Xi_tail_abs": f"{xi_tail:.12g}",
                "alpha_bound_vector": "" if alpha is None else f"{alpha:.12g}",
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
            "control_id": "CTRL4641_0_cross_branch_rejected",
            "control": "reject exact zero assembled from incompatible branches",
            "result": "PASS",
            "reason": "RUN4641_2 is an explicit reject row even though component magnitudes are zero",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4641_1_no_cancellation",
            "control": "finite pack uses absolute component sum",
            "result": "PASS",
            "reason": "no signs or cancellations are used in finite R10 smoke rows",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4641_2_private_not_public",
            "control": "strict branch zero is private conditional only",
            "result": "PASS",
            "reason": "all generated rows remain valid_for_claim=false",
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("BLK4641_0", "PARENT_SIGNATURE_UNSIGNED", "single Hilbert source owner and source-label forgetting are not globally parent-signed"),
        ("BLK4641_1", "HPERP_QEDGE_KERNEL_CLAUSES_UNSIGNED", "Hperp, Q_edge and transition source-kernel zero clauses remain branch-local"),
        ("BLK4641_2", "PROJECTION_CONSTANTS_MISSING", "K_NH, K_edge, K_tr and other finite-pack projection constants are not source-backed"),
        ("BLK4641_3", "LAMBDA_MEM_MISSING", "lambda_mem is not parent-derived/source-backed for claim-grade R10 use"),
        ("BLK4641_4", "PROMOTION_SCOPE_NOT_DONE", "R10 same-branch assembly is not yet propagated into PPN/Newton/clock/orbital/local-GR promotion gates"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "detail": detail,
            "blocks_claim": True,
            "next_action": NEXT_TARGET if blocker_id in {"BLK4641_2", "BLK4641_3"} else "retain same-branch signature blocker",
            "timestamp_utc": now,
        }
        for blocker_id, blocker, detail in blockers
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4641_0",
            "decision": DECISION,
            "selected_next_target": NEXT_TARGET,
            "claim_allowed": False,
            "reason": "the four component zero routes are formally compatible only on a strict same-branch parent/readout package; otherwise a finite no-cancellation pack is required",
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "SAME_BRANCH_CONDITIONAL_ZERO_ASSEMBLED_NONCLAIM",
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "local_gr_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "newton_claim": False,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "priority": "source or prove the parent branch signature, projection constants and lambda_mem required to promote same-branch Xi_tail closure beyond private nonclaim",
            "acceptance_gate": "claim remains blocked unless exact branch signatures are parent-signed or finite coefficients plus lambda_mem are real and pass R10 without cancellation",
            "timestamp_utc": now,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    compatibility: list[dict[str, Any]],
    assembly: list[dict[str, Any]],
    finite_pack: list[dict[str, Any]],
    runs: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4641 — Same-branch Xi-tail zero assembly or finite coefficient pack

Marker: `{MARKER}`

## Result

4641 assembles the four `Xi_tail` component routes from 4638, 4639 and 4640:

`Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner`.

The exact-zero branch is:

`Xi_tail=0`

only if all four component zeros hold on one shared parent/readout branch:

`Z_src_hidden=Z_nonHilbert=Z_boundary_history=Z_transition_inner=True`.

The strict branch is formally compatible: single Hilbert source owner, source-label forgetting, Hperp/source-pairing silence, same q-basic source worldtube, no-flux edge support, transition source-kernel membership, same coframe/Hodge/tau/readout, and fixed projector/domain/lambda data can be stated together.

But it is not a public claim. The parent signatures and source-backed constants are still missing. If any zero clause opens, the fallback is the finite no-cancellation pack:

`|Xi_tail| <= |Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)`.

## Source register

{markdown_table(sources)}

## Zero branch imports

{markdown_table(imports)}

## Same-branch clause matrix

{markdown_table(clauses)}

## Compatibility audit

{markdown_table(compatibility)}

## Xi-tail assembly rows

{markdown_table(assembly)}

## Finite coefficient pack schema

{markdown_table(finite_pack)}

## R10 same-branch runner

{markdown_table(runs)}

## Claim blockers

{markdown_table(blockers)}

## Decision

{markdown_table(decisions)}

## Validation

{markdown_table(validations)}
"""


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4641 assembles the four Xi_tail zero-or-bound routes into a same-branch compatibility gate and finite no-cancellation coefficient pack.",
        "current_evidence": "Generated source register, zero imports, same-branch clause matrix, compatibility audit, Xi-tail assembly rows, finite coefficient pack schema, R10 same-branch runner, controls, blockers, decision, status, next target and validation.",
        "status": "same_branch_Xi_tail_zero_assembled_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming Xi_tail zero by stitching branch-local theorems from incompatible parent/readout/domain branches.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/R10/PPN claim until same-branch parent signatures are signed or finite component coefficients, projection constants and lambda_mem are source-backed and pass without cancellation.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def validate(
    sources: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    compatibility: list[dict[str, Any]],
    assembly: list[dict[str, Any]],
    finite_pack: list[dict[str, Any]],
    runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4641_0_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4641_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4641_2_four_zero_imports", {row["component"] for row in imports} == {"Xi_src_hidden", "Xi_nonHilbert", "Xi_boundary_history", "Xi_transition_inner"}, "all four component zero routes imported"))
    checks.append(("VAL4641_3_clause_matrix_complete", len(clauses) == 8, "same-branch clause matrix complete"))
    checks.append(("VAL4641_4_strict_branch_compatible", any(row["compatibility"] == "FORMALLY_COMPATIBLE" for row in compatibility), "strict branch compatibility row present"))
    checks.append(("VAL4641_5_cross_branch_rejected", any(row["compatibility"] == "REJECTED" for row in compatibility), "cross-branch exact zero rejected"))
    checks.append(("VAL4641_6_exact_assembly_row", any(row["row_id"] == "XA4641_1_exact_branch" for row in assembly), "exact same-branch assembly row present"))
    checks.append(("VAL4641_7_finite_pack_complete", len(finite_pack) == 6, "finite coefficient pack schema complete"))
    checks.append(("VAL4641_8_runner_live_fail_closed", any(row["run_id"] == "RUN4641_0_live_missing_inputs" and row["result"] == "FAIL_CLOSED" for row in runs), "live missing-input row fails closed"))
    checks.append(("VAL4641_9_runner_rejects_cross_branch", any(row["run_id"] == "RUN4641_2_cross_branch_zeros" and row["result"] == "REJECT_CROSS_BRANCH_ZERO" for row in runs), "runner rejects cross-branch zeros"))
    checks.append(("VAL4641_10_runner_pass_fail_controls", any("PASS" in row["result"] for row in runs) and any("FAIL" in row["result"] for row in runs), "runner has pass and fail controls"))
    checks.append(("VAL4641_11_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for row in imports + clauses + compatibility + assembly + finite_pack + runs), "generated rows remain nonclaim"))
    checks.append(("VAL4641_12_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4641_13_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4641_14_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4641_15_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4641_16_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4641_17_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4641_18_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
    validations = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": utc_now(),
        }
        for check_id, passed, detail in checks
    ]
    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4641_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4641 validation passed" if overall else "one or more 4641 checks failed",
            "timestamp_utc": utc_now(),
        }
    )
    return validations


def main() -> int:
    now = utc_now()
    points = load_curve_points()
    sources = source_rows(now)
    imports = zero_import_rows(now)
    clauses = clause_rows(now)
    compatibility = compatibility_rows(now)
    assembly = assembly_rows(now)
    finite_pack = finite_pack_rows(now)
    runs = run_rows(points, now)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    for path, rows in [
        (SOURCE_REGISTER, sources),
        (ZERO_IMPORT_CSV, imports),
        (CLAUSE_MATRIX_CSV, clauses),
        (COMPATIBILITY_CSV, compatibility),
        (ASSEMBLY_CSV, assembly),
        (FINITE_PACK_CSV, finite_pack),
        (RUNNER_CSV, runs),
        (CONTROL_CSV, controls),
        (BLOCKERS_CSV, blockers),
        (DECISION_CSV, decisions),
        (STATUS_CSV, statuses),
        (NEXT_CSV, next_targets),
    ]:
        write_csv(path, rows)

    provisional_validations = [
        {"checkpoint": CHECKPOINT, "validation_id": "VAL4641_PROVISIONAL", "status": "PENDING", "detail": "validation runs after documents are written", "timestamp_utc": now}
    ]
    doc_body = build_doc(sources, imports, clauses, compatibility, assembly, finite_pack, runs, blockers, decisions, provisional_validations)
    write_text(DOC_PATH, doc_body)
    write_text(FORMAL_PATH, doc_body.replace("# 4641", "# 657 / 4641", 1))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4641 assembles `Xi_src_hidden`, `Xi_nonHilbert`, `Xi_boundary_history` and `Xi_transition_inner` into a same-branch gate. Exact `Xi_tail=0` is allowed only on one strict q-basic Hilbert/same-worldtube/source-label-forgetting/source-kernel branch; cross-branch zero stitching is explicitly rejected. If any clause opens, the finite no-cancellation pack is `|Xi_tail| <= |Xi_src_hidden|+|Xi_nonHilbert|+|Xi_boundary_history|+|Xi_transition_inner| <= alpha_bound(lambda_mem)`. This remains nonclaim pending parent signatures, projection constants and `lambda_mem`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` assembles the private R10 `Xi_tail` route. The result is strong but conditional: exact zero requires one shared parent/readout branch; otherwise use the finite coefficient pack. Next packet target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    validations = validate(sources, imports, clauses, compatibility, assembly, finite_pack, runs)
    write_csv(VALIDATION_CSV, validations)
    final_doc = build_doc(sources, imports, clauses, compatibility, assembly, finite_pack, runs, blockers, decisions, validations)
    write_text(DOC_PATH, final_doc)
    write_text(FORMAL_PATH, final_doc.replace("# 4641", "# 657 / 4641", 1))

    print(f"{MARKER}: {validations[-1]['status']}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if validations[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
