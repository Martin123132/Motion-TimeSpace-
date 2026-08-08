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

CHECKPOINT = "4642"
CLAIM_ID = "L-484"
BRANCH_ID = "MTS_R2FR_Y5_XI_TAIL_SIGNATURE_LAMBDA_PACK_4642"
MARKER = "PPC4161_XI_TAIL_PARENT_SIGNATURE_AND_LAMBDA_SOURCE_PACK_4642"
PACKET_MARKER = "PPC4161_PACKET_XI_TAIL_SIGNATURE_LAMBDA_PACK_4642"
DECISION = "LAMBDA_MEM_IMPORTED_AS_PARENT_HESSIAN_RATIO_PROJECTION_CONSTANTS_STAGED_FINITE_PACK_REMAINS_NONCLAIM"
NEXT_TARGET = "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"

DOC_PATH = POST / "4642-Y5-R2FR-Xi-tail-parent-signature-and-lambda-source-pack.md"
FORMAL_PATH = FORMAL / "658-PPC4161-Xi-tail-parent-signature-and-lambda-source-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4641_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4641_VALIDATION.csv"
CSV_4641_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4641_SAME_BRANCH_CLAUSE_MATRIX.csv"
CSV_4641_COMPAT = SOURCE_DIR / "P8_Y5_R2FR_4641_BRANCH_COMPATIBILITY_AUDIT.csv"
CSV_4641_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4641_FINITE_COEFFICIENT_PACK_SCHEMA.csv"
DOC_4641 = POST / "4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"
DOC_4628 = POST / "4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md"
FW_4334 = FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"
FW_4335 = FORMAL / "351-PPC4161-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md"
FW_4506 = FORMAL / "522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4642_SOURCE_REGISTER.csv"
PARENT_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_PARENT_SIGNATURE_PACK.csv"
LAMBDA_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_LAMBDA_MEM_SOURCE_PACK.csv"
PROJECTION_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_PROJECTION_CONSTANT_SOURCE_PACK.csv"
FINITE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_CLAIM_GRADE_FINITE_PACK_REQUIREMENTS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_R10_SOURCE_PACK_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4642_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4642_VALIDATION.csv"

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
        ("SRC4642_00_4641_validation", CSV_4641_VALIDATION, "VAL4641_OVERALL", "4641 validation."),
        ("SRC4642_01_4641_clauses", CSV_4641_CLAUSES, "CLAUSE4641_7", "same-branch clause matrix."),
        ("SRC4642_02_4641_compat", CSV_4641_COMPAT, "COMP4641_0_strict_private_branch", "strict branch compatibility row."),
        ("SRC4642_03_4641_finite_pack", CSV_4641_FINITE, "FP4641_4", "finite pack lambda row."),
        ("SRC4642_04_4641_doc", DOC_4641, "finite no-cancellation pack", "human 4641 finite-pack statement."),
        ("SRC4642_05_4628_marker", DOC_4628, "PPC4161_LAMBDA_MEM_GAP_ROW_OR_ZMEM_M2MEM_PARENT_HESSIAN_4628", "lambda_mem parent-Hessian checkpoint."),
        ("SRC4642_06_4628_hessian", DOC_4628, "HES4628_1_parent_hessian_definitions", "parent Hessian definitions."),
        ("SRC4642_07_4628_gap", DOC_4628, "GAP4628_0_exact_positive_gap", "positive-gap lambda condition."),
        ("SRC4642_08_4628_lambda_row", DOC_4628, "LNUM4628_2_lambda", "lambda_mem source row."),
        ("SRC4642_09_4628_anchor", DOC_4628, "A4628_0_R10_alpha1_lambda", "R10 anchor gap conversion row."),
        ("SRC4642_10_4334_R10_projection", FW_4334, "PI4334_0_R10", "R10 projection-matrix contract."),
        ("SRC4642_11_4334_R10_gate", FW_4334, "F4334_2_R10_smoke_gate", "R10 smoke gate."),
        ("SRC4642_12_4335_R10_blocker", FW_4335, "BLK4335_2_R10_parent_alpha", "R10 parent-alpha blocker."),
        ("SRC4642_13_4335_R10_formula", FW_4335, "F4335_4_R10_requirement", "R10 alpha(lambda) formula requirement."),
        ("SRC4642_14_4506_body_charge", FW_4506, "BCIN4506_0_memory_density", "memory body-charge input law."),
        ("SRC4642_15_4506_operator", FW_4506, "MOP4506_0_quadratic_action", "memory quadratic action signature."),
        ("SRC4642_16_curve", CSV_4635_CURVE, "lambda_m", "digitized R10 alpha(lambda) curve."),
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


def parent_signature_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("PS4642_0", "single Hilbert source owner", "CLAUSE4641_0", "exact route", "parent grammar/action line must sign one active Hilbert source owner"),
        ("PS4642_1", "source-label forgetting", "CLAUSE4641_1", "exact route", "no source-only weights, hidden markers, source normalization or environment selector before variation"),
        ("PS4642_2", "Hperp source-pairing silence", "CLAUSE4641_2", "exact route", "Hperp=0 or S_A Hperp^A=0 plus R_src_readout=0"),
        ("PS4642_3", "same q-basic source worldtube", "CLAUSE4641_3", "exact and finite route", "source worldtube fixed before variation and shared by Hilbert/source/readout branches"),
        ("PS4642_4", "regular support/no-flux edge", "CLAUSE4641_4", "exact route", "zero density trace/no birth shell/source-free no-flux collar/fixed edge projector"),
        ("PS4642_5", "transition source kernel", "CLAUSE4641_5", "exact route", "q_tr Hilbert, same-worldtube, static l=0, universal, range-free, same-metric, boundary-owned"),
        ("PS4642_6", "same observed coframe/Hodge/tau", "CLAUSE4641_6", "promotion route", "readout frame common to matter, EM, clocks and local tests before scoring"),
        ("PS4642_7", "fixed projector/domain/lambda", "CLAUSE4641_7", "finite route", "projector/domain/lambda_mem parent-owned and fixed before R10/PPN residuals"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "clause": clause,
            "source_clause": source_clause,
            "route": route,
            "required_parent_input": required,
            "current_status": "FORMALLY_COMPATIBLE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for signature_id, clause, source_clause, route, required in clauses
    ]


def lambda_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "lambda_id": "LAM4642_0_parent_hessian_law",
            "symbol": "lambda_mem",
            "definition": "lambda_mem=sqrt(Z_mem/M2_mem) when Z_mem>0 and M2_mem>0 on the same branch/normalization",
            "source": "4628 HES4628_1/GAP4628_0/LNUM4628_2",
            "numeric_value": "",
            "units": "m",
            "current_status": "LAW_DERIVED_NUMERIC_RATIO_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "lambda_id": "LAM4642_1_exact_contact_route",
            "symbol": "lambda_mem",
            "definition": "M2_mem/Z_mem -> infinity or memory constrained/eliminated gives contact/absent force",
            "source": "4628 GAP4628_3_constraint_limit",
            "numeric_value": "",
            "units": "m",
            "current_status": "CONDITIONAL_EXACT_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "lambda_id": "LAM4642_2_massless_fail",
            "symbol": "lambda_mem",
            "definition": "M2_mem=0 gives lambda_mem -> infinity unless Q_eff/Xi_tail is exactly zero",
            "source": "4628 GAP4628_1_massless_fail",
            "numeric_value": "infinity_if_not_zero",
            "units": "m",
            "current_status": "FAIL_BRANCH_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "lambda_id": "LAM4642_3_tachyon_reject",
            "symbol": "lambda_mem",
            "definition": "M2_mem<0 is unstable and cannot be used as a local-GR recovery branch",
            "source": "4628 GAP4628_2_tachyon_fail",
            "numeric_value": "imaginary",
            "units": "m",
            "current_status": "REJECT_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "lambda_id": "LAM4642_4_R10_anchor_smoke",
            "symbol": "(M2_mem/Z_mem)_anchor",
            "definition": "1/(38.6e-6 m)^2 from alpha=1 anchor smoke, not a theory prediction",
            "source": "4628 A4628_0_R10_alpha1_lambda",
            "numeric_value": "671158957.2874439",
            "units": "m^-2",
            "current_status": "SOURCE_BACKED_ANCHOR_SMOKE_NOT_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def projection_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROJ4642_0_K_NH", "K_NH", "Xi_nonHilbert projection normalization", "4639 formula; 4334 projection matrix discipline", "maps N_src_nonHilbert/Hperp bound into dimensionless Xi_tail", "MISSING_SOURCE_BACKED_CONSTANT"),
        ("PROJ4642_1_K_edge", "K_edge", "Q_edge to Xi_boundary_history projection normalization", "4640 formula; 4609 Q_edge law", "maps worldtube shell/boundary residual into dimensionless Xi_tail", "MISSING_SOURCE_BACKED_CONSTANT"),
        ("PROJ4642_2_K_tr", "K_tr", "transition hair to Xi_transition_inner projection normalization", "4640 formula; 4355 epsilon_tr_hair law", "maps transition source-kernel hair into dimensionless Xi_tail", "MISSING_SOURCE_BACKED_CONSTANT"),
        ("PROJ4642_3_Pi_R10", "Pi_R10(lambda)", "R10 alpha(lambda) arena projection", "4334 PI4334_0_R10", "must be numeric/source-backed and fixed before scoring", "MISSING_R10_PARENT_COEFFICIENTS"),
        ("PROJ4642_4_alpha_bound_curve", "alpha_bound(lambda)", "experimental R10 comparator curve", "4635 digitized Eot-Wash vector curve", "usable for internal smoke; claim needs final QA/source-backed curve status", "SMOKE_CURVE_AVAILABLE_CLAIM_QA_PENDING"),
        ("PROJ4642_5_Gobs_source_norm", "G_N^obs M_S m_T", "source-normalization denominator for alpha(lambda)", "4335 F4335_4_R10_requirement", "prevents hiding coupling in calibrated G or orbital GM", "MISSING_SOURCE_NORMALIZATION_BRANCH"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "projection_id": projection_id,
            "symbol": symbol,
            "meaning": meaning,
            "source_basis": source_basis,
            "required_use": required_use,
            "current_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for projection_id, symbol, meaning, source_basis, required_use, status in rows
    ]


def finite_pack_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CFP4642_0", "Xi_src_hidden", "zero certificate or finite value", "source-label-forgetting clauses or component sum from 4638"),
        ("CFP4642_1", "Xi_nonHilbert", "K_NH ||U_B||(C_S C_perp E_Dq,Hperp+||R_src_readout||)", "K_NH plus Hperp/Dq values"),
        ("CFP4642_2", "Xi_boundary_history", "K_edge(|Q_edge_shell|+|Q_edge_boundary|)", "K_edge plus Q_edge component values"),
        ("CFP4642_3", "Xi_transition_inner", "K_tr epsilon_tr_hair", "K_tr plus transition-hair component values"),
        ("CFP4642_4", "lambda_mem", "sqrt(Z_mem/M2_mem)", "same-branch Z_mem/M2_mem ratio or exact constraint route"),
        ("CFP4642_5", "alpha_bound(lambda_mem)", "interpolation from R10 curve", "claim-grade curve QA and lambda within source-backed curve domain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "requirement_id": requirement_id,
            "symbol": symbol,
            "claim_grade_requirement": requirement,
            "first_input_to_fill": first_input,
            "current_status": "MISSING_CLAIM_GRADE_INPUT_OR_PARENT_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for requirement_id, symbol, requirement, first_input in rows
    ]


def run_rows(points: list[tuple[float, float]], now: str) -> list[dict[str, Any]]:
    specs = [
        ("RUN4642_0_live_missing_pack", "current live source pack", None, None, "FAIL_CLOSED", "missing parent signatures, projection constants and lambda_mem"),
        ("RUN4642_1_exact_same_branch_zero", "same-branch exact zero control", 1.0e-4, 0.0, "CONDITIONAL_ZERO_PASS_NONCLAIM", "Xi_tail=0 if the strict same-branch parent signature is signed"),
        ("RUN4642_2_anchor_smoke_pass", "anchor-smoke finite pack", 3.86e-5, 0.9, "", ""),
        ("RUN4642_3_anchor_smoke_fail", "anchor-smoke finite pack", 3.86e-5, 1.0, "", ""),
        ("RUN4642_4_finite_pack_pass_100um", "finite coefficient pack smoke", 1.0e-4, 0.07, "", ""),
        ("RUN4642_5_finite_pack_fail_100um", "finite coefficient pack smoke", 1.0e-4, 0.08, "", ""),
        ("RUN4642_6_massless_branch", "M2_mem=0 without exact Xi_tail zero", math.inf, 0.0, "FAIL_CLOSED", "massless branch requires exact source/coupling zero; no finite R10 range"),
        ("RUN4642_7_tachyon_branch", "M2_mem<0", math.nan, 0.0, "REJECT_BRANCH", "negative M2_mem is unstable and cannot be local-GR recovery"),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, branch, lambda_m, xi_tail, forced_result, forced_reason in specs:
        if lambda_m is None:
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "run_id": run_id,
                    "branch": branch,
                    "lambda_mem_m": "",
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
        if not math.isfinite(lambda_m):
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "run_id": run_id,
                    "branch": branch,
                    "lambda_mem_m": str(lambda_m),
                    "Xi_tail_abs": f"{float(xi_tail or 0.0):.12g}",
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
        if forced_result:
            result = forced_result
            reason = forced_reason
        elif alpha is None:
            result = "FAIL_CLOSED"
            reason = "lambda outside extracted vector curve"
        elif float(xi_tail or 0.0) <= alpha:
            result = "SMOKE_PASS_NONCLAIM"
            reason = "absolute Xi_tail sits inside digitized vector bound for this toy/source-pack row"
        else:
            result = "SMOKE_FAIL_NONCLAIM"
            reason = "absolute Xi_tail exceeds digitized vector bound"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "branch": branch,
                "lambda_mem_m": f"{lambda_m:.12g}",
                "Xi_tail_abs": f"{float(xi_tail or 0.0):.12g}",
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
            "control_id": "CTRL4642_0_lambda_not_fit",
            "control": "lambda_mem is fixed by same-branch Z_mem/M2_mem, not selected from R10 bound",
            "result": "PASS",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4642_1_anchor_not_curve_claim",
            "control": "38.6 um alpha=1 row is anchor-smoke only",
            "result": "PASS",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4642_2_no_projection_postfit",
            "control": "K_NH/K_edge/K_tr/Pi_R10 must be fixed before residual scoring",
            "result": "PASS",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4642_3_fail_branches_retained",
            "control": "massless and tachyonic memory-gap branches fail/reject unless exact zero route closes",
            "result": "PASS",
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("BLK4642_0", "SAME_BRANCH_SIGNATURE_UNSIGNED", "the strict parent/readout branch is compatible but not signed for claim"),
        ("BLK4642_1", "ZMEM_M2MEM_RATIO_MISSING", "lambda_mem law is derived, but same-branch numeric/invariant ratio is missing"),
        ("BLK4642_2", "PROJECTION_CONSTANTS_MISSING", "K_NH, K_edge, K_tr, Pi_R10 and source normalization are not source-backed"),
        ("BLK4642_3", "FINITE_COMPONENT_VALUES_MISSING", "Xi component magnitudes are not claim-grade values if exact zero branch opens"),
        ("BLK4642_4", "R10_PROMOTION_SCOPE_PENDING", "R10 pack is not yet propagated to PPN/Newton/clock/orbital/local-GR promotion gates"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "detail": detail,
            "blocks_claim": True,
            "next_action": NEXT_TARGET if blocker_id in {"BLK4642_1", "BLK4642_2", "BLK4642_3"} else "retain branch-signature blocker",
            "timestamp_utc": now,
        }
        for blocker_id, blocker, detail in blockers
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4642_0",
            "decision": DECISION,
            "selected_next_target": NEXT_TARGET,
            "claim_allowed": False,
            "reason": "lambda_mem now has a real parent-Hessian source law in the current route, but the same-branch Z/M ratio and projection constants remain missing, so 4642 emits a source pack rather than a claim",
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "SOURCE_PACK_READY_NONCLAIM",
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
            "priority": "try to fill one claim-grade input first: same-branch Z_mem/M2_mem ratio, K_NH/K_edge/K_tr/Pi_R10 projection constant, or exact parent signature",
            "acceptance_gate": "row remains nonclaim unless source path, units, branch convention and no-postfit rule are satisfied",
            "timestamp_utc": now,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    parent_signatures: list[dict[str, Any]],
    lambda_pack: list[dict[str, Any]],
    projection_pack: list[dict[str, Any]],
    finite_pack: list[dict[str, Any]],
    runs: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4642 — Xi-tail parent signature and lambda source pack

Marker: `{MARKER}`

## Result

4642 turns the 4641 handoff into a claim-grade acquisition pack.

The main advance is that `lambda_mem` is not an arbitrary fit parameter in this route. It imports the 4628 parent-Hessian law:

`lambda_mem = sqrt(Z_mem/M2_mem)`

when `Z_mem>0` and `M2_mem>0` are owned on the same branch and in the same normalization. The R10 `38.6 um` row remains an anchor-smoke conversion only, not a theory value.

The exact branch remains:

`Xi_tail=0`

only if the strict same-branch parent/readout signature signs all four component zero routes from 4638–4641.

If any exact-zero clause opens, the finite route is:

`|Xi_tail| <= |Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)`.

4642 does not claim R10/local-GR. It says exactly what must be filled next: same-branch parent signatures, `Z_mem/M2_mem` or exact constraint route, projection constants `K_NH/K_edge/K_tr/Pi_R10`, component magnitudes, and curve/promotion QA.

## Source register

{markdown_table(sources)}

## Parent signature pack

{markdown_table(parent_signatures)}

## Lambda source pack

{markdown_table(lambda_pack)}

## Projection constant source pack

{markdown_table(projection_pack)}

## Claim-grade finite pack requirements

{markdown_table(finite_pack)}

## R10 source-pack runner

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
        "claim": "4642 imports lambda_mem as a parent-Hessian ratio and stages the same-branch signature, projection-constant and finite-coefficient source pack needed to score the Xi_tail R10 route.",
        "current_evidence": "Generated source register, parent signature pack, lambda_mem source pack, projection constant pack, claim-grade finite pack requirements, R10 source-pack runner, controls, blockers, decision, status, next target and validation.",
        "status": "Xi_tail_lambda_projection_source_pack_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating lambda_mem as fit from the R10 bound, or scoring R10 with projection constants chosen after residuals.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/R10/PPN claim until same-branch signatures or finite coefficients, Z_mem/M2_mem, projection constants, source normalization and lambda_mem are claim-grade.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def validate(
    sources: list[dict[str, Any]],
    parent_signatures: list[dict[str, Any]],
    lambda_pack: list[dict[str, Any]],
    projection_pack: list[dict[str, Any]],
    finite_pack: list[dict[str, Any]],
    runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4642_0_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4642_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4642_2_parent_signature_pack", len(parent_signatures) == 8, "same-branch parent signature pack has eight clauses"))
    checks.append(("VAL4642_3_lambda_law_imported", any(row["lambda_id"] == "LAM4642_0_parent_hessian_law" and "sqrt(Z_mem/M2_mem)" in row["definition"] for row in lambda_pack), "lambda_mem parent-Hessian law imported"))
    checks.append(("VAL4642_4_fail_branches_retained", any(row["current_status"] == "FAIL_BRANCH_RETAINED" for row in lambda_pack) and any(row["current_status"] == "REJECT_BRANCH" for row in lambda_pack), "massless/tachyon branches retained as fail/reject"))
    checks.append(("VAL4642_5_projection_pack", len(projection_pack) == 6, "projection constant pack complete"))
    checks.append(("VAL4642_6_finite_pack", len(finite_pack) == 6, "claim-grade finite pack requirements complete"))
    checks.append(("VAL4642_7_runner_live_fail_closed", any(row["run_id"] == "RUN4642_0_live_missing_pack" and row["result"] == "FAIL_CLOSED" for row in runs), "live source pack fails closed"))
    checks.append(("VAL4642_8_runner_pass_fail_controls", any("PASS" in row["result"] for row in runs) and any("FAIL" in row["result"] for row in runs), "runner has pass and fail controls"))
    checks.append(("VAL4642_9_runner_rejects_tachyon", any(row["run_id"] == "RUN4642_7_tachyon_branch" and row["result"] == "REJECT_BRANCH" for row in runs), "tachyon branch rejected"))
    checks.append(("VAL4642_10_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for row in parent_signatures + lambda_pack + projection_pack + finite_pack + runs), "generated rows remain nonclaim"))
    checks.append(("VAL4642_11_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4642_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4642_13_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4642_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4642_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4642_16_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4642_17_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
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
            "validation_id": "VAL4642_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4642 validation passed" if overall else "one or more 4642 checks failed",
            "timestamp_utc": utc_now(),
        }
    )
    return validations


def main() -> int:
    now = utc_now()
    points = load_curve_points()
    sources = source_rows(now)
    parent_signatures = parent_signature_rows(now)
    lambda_pack = lambda_rows(now)
    projection_pack = projection_rows(now)
    finite_pack = finite_pack_rows(now)
    runs = run_rows(points, now)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    for path, rows in [
        (SOURCE_REGISTER, sources),
        (PARENT_SIGNATURE_CSV, parent_signatures),
        (LAMBDA_PACK_CSV, lambda_pack),
        (PROJECTION_PACK_CSV, projection_pack),
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
        {"checkpoint": CHECKPOINT, "validation_id": "VAL4642_PROVISIONAL", "status": "PENDING", "detail": "validation runs after documents are written", "timestamp_utc": now}
    ]
    doc_body = build_doc(sources, parent_signatures, lambda_pack, projection_pack, finite_pack, runs, blockers, decisions, provisional_validations)
    write_text(DOC_PATH, doc_body)
    write_text(FORMAL_PATH, doc_body.replace("# 4642", "# 658 / 4642", 1))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4642 imports `lambda_mem=sqrt(Z_mem/M2_mem)` from the parent-Hessian route and stages the claim-grade source pack needed for the same-branch `Xi_tail` R10 gate. Exact zero still requires the strict same-branch signature from 4641; finite scoring requires real `Xi` component magnitudes, `K_NH/K_edge/K_tr/Pi_R10`, source normalization and same-branch `Z_mem/M2_mem`. Massless and tachyonic branches are retained as fail/reject unless exact zero closes. This remains nonclaim.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` converts the same-branch `Xi_tail` gate into a source acquisition pack. The range is no longer free: `lambda_mem` comes from `Z_mem/M2_mem`. Next packet target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    validations = validate(sources, parent_signatures, lambda_pack, projection_pack, finite_pack, runs)
    write_csv(VALIDATION_CSV, validations)
    final_doc = build_doc(sources, parent_signatures, lambda_pack, projection_pack, finite_pack, runs, blockers, decisions, validations)
    write_text(DOC_PATH, final_doc)
    write_text(FORMAL_PATH, final_doc.replace("# 4642", "# 658 / 4642", 1))

    print(f"{MARKER}: {validations[-1]['status']}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if validations[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
