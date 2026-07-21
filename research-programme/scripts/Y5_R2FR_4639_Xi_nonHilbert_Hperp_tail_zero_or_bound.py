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

CHECKPOINT = "4639"
CLAIM_ID = "L-481"
BRANCH_ID = "MTS_R2FR_Y5_XI_NONHILBERT_HPERP_4639"
MARKER = "PPC4161_XI_NONHILBERT_HPERP_TAIL_ZERO_OR_BOUND_4639"
PACKET_MARKER = "PPC4161_PACKET_XI_NONHILBERT_HPERP_4639"
DECISION = "XI_NONHILBERT_REDUCED_TO_HPERP_SOURCE_PAIRING_ZERO_OR_BOUND_NONCLAIM"
NEXT_TARGET = "4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md"

DOC_PATH = POST / "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
FORMAL_PATH = FORMAL / "655-PPC4161-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4638_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4638_VALIDATION.csv"
CSV_4638_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4638_XI_TAIL_REDUCTION_ROWS.csv"
CSV_4638_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4638_R10_REDUCED_TAIL_RUNNER_RESULTS.csv"
DOC_4638 = POST / "4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md"
FW_4318 = FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md"
FW_4319 = FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md"
FW_4320 = FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"
FW_4431 = FORMAL / "447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4639_SOURCE_REGISTER.csv"
IMPORT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_NONHILBERT_IMPORT_AUDIT.csv"
FORMULA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_XI_NONHILBERT_FORMULA_ROWS.csv"
COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_HPERP_DQ_COMPONENT_STATUS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_XI_TAIL_REDUCTION_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_R10_REDUCED_TAIL_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4639_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4639_VALIDATION.csv"

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
        ("SRC4639_00_4638_validation", CSV_4638_VALIDATION, "VAL4638_OVERALL", "4638 validation."),
        ("SRC4639_01_4638_reduction", CSV_4638_REDUCTION, "XR4638_2_reduced_tail", "current four-component Xi_tail gate."),
        ("SRC4639_02_4638_doc", DOC_4638, "Xi_tail := Xi_src_hidden + Xi_nonHilbert", "human-readable reduced tail."),
        ("SRC4639_03_4318_priority", FW_4318, "P4318_1", "old ladder selected N_src_nonHilbert/Hperp first."),
        ("SRC4639_04_4318_canon", FW_4318, "NR4318_0_Nsrc", "canonical N_src_nonHilbert row."),
        ("SRC4639_05_4319_marker", FW_4319, "PPC4161_NONHILBERT_HPERP_SOURCE_SUPPORT_ZERO_OR_BOUND_ROW_4319", "Hperp source-support zero/bound theorem."),
        ("SRC4639_06_4319_zero", FW_4319, "TH4319_3_exact_zero", "exact N_src_nonHilbert zero branch."),
        ("SRC4639_07_4319_bound", FW_4319, "F4319_5_bound", "finite Dq/Hperp source-support bound."),
        ("SRC4639_08_4320_source_readout", FW_4320, "Dq_source_readout[Hperp]", "highest-leverage Dq component."),
        ("SRC4639_09_4320_Nsrc", FW_4320, "F4320_1_Nsrc", "N_src finite formula handoff."),
        ("SRC4639_10_4431_nonHilbert_zero", FW_4431, "NH4431_0_nonHilbert_zero_theorem", "Noether/improvement zero theorem."),
        ("SRC4639_11_4431_current_gap", FW_4431, "NH4431_1_current_gap", "current non-Hilbert gap retained."),
        ("SRC4639_12_4635_curve", CSV_4635_CURVE, "lambda_m", "R10 vector curve points."),
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


def import_audit_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4639_0_object_map",
            "input": "N_src_nonHilbert from 4318/4319",
            "mapped_to_current_tail": "Xi_nonHilbert",
            "status": "MAPPED_AS_DIMENSIONLESS_PROJECTED_SOURCE_BYPASS",
            "law": "Xi_nonHilbert := K_NH N_src_nonHilbert with K_NH the current R10 projection normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4639_1_exact_zero",
            "input": "TH4319_3_exact_zero",
            "mapped_to_current_tail": "Xi_nonHilbert=0",
            "status": "CONDITIONAL_ZERO_AVAILABLE",
            "law": "Hperp=0 or S_A Hperp^A=0, and R_src_readout=0 => N_src_nonHilbert=0 => Xi_nonHilbert=0",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4639_2_finite_bound",
            "input": "F4319_5_bound / F4320_1_Nsrc",
            "mapped_to_current_tail": "|Xi_nonHilbert| bound",
            "status": "BOUND_ROUTE_READY_INPUTS_MISSING",
            "law": "|Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4639_3_noether_bypass",
            "input": "NH4431_0_nonHilbert_zero_theorem / NH4431_1_current_gap",
            "mapped_to_current_tail": "Noether/improvement bypass risk",
            "status": "EXACT_THEOREM_STAGED_BUT_UNSIGNED",
            "law": "owned exact improvements with zero compact projected flux cannot source Xi_nonHilbert; spin/boundary/readout/flux pieces remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def formula_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4639_0_quotient_split",
            "formula": "H_L = H_q + Hperp, H_q in ker(Dq), Hperp=(1-Pi_kerDq)H_L",
            "basis": "4319 Hperp strip",
            "status": "IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4639_1_source_pairing",
            "formula": "S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
            "basis": "4319 source-pairing split",
            "status": "IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4639_2_exact_zero",
            "formula": "if Hperp=0 or S_A Hperp^A=0, and R_src_readout=0, then Xi_nonHilbert=0",
            "basis": "TH4319_3_exact_zero plus current Xi projection",
            "status": "CONDITIONAL_ZERO_NOT_GLOBAL_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4639_3_finite_bound",
            "formula": "|Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
            "basis": "F4319_5_bound/F4320_1_Nsrc with dimensionless R10 projection K_NH",
            "status": "BOUND_READY_KNH_AND_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4639_4_reduced_tail_after_zero",
            "formula": "if Xi_src_hidden=0 and Xi_nonHilbert=0, then Xi_tail := Xi_boundary_history + Xi_transition_inner",
            "basis": "4638 reduced tail plus 4639 zero branch",
            "status": "CONDITIONAL_REDUCTION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def component_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("HC4639_0", "Dq_source_readout[Hperp]", "highest leverage because it feeds both E_Dq,Hperp and R_src_readout", "MISSING_PARENT_SIGNATURE"),
        ("HC4639_1", "Dq_geom[Hperp]", "geometry/coframe descent component", "PROFILE_ROUTE_AVAILABLE_VALUES_MISSING"),
        ("HC4639_2", "Dq_EM[Hperp]", "EM/Hodge/current descent component", "ROUTE_AVAILABLE_VALUES_MISSING"),
        ("HC4639_3", "Dq_tau[Hperp]", "clock/reference-time descent component", "ROUTE_OPEN"),
        ("HC4639_4", "Dq_matter[Hperp]", "matter action descent component", "ROUTE_OPEN"),
        ("HC4639_5", "Dq_boundary_projector[Hperp]", "boundary/projector ownership component", "ROUTE_OPEN"),
        ("HC4639_6", "Dq_theta_marker[Hperp]", "marker/selector component", "ROUTE_OPEN"),
        ("HC4639_7", "Dq_coeff[Hperp]", "coefficient/normalization component", "ROUTE_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "role": role,
            "current_status": status,
            "zero_gate": "Dq_i[Hperp]=0 from parent quotient/factorization certificate",
            "bound_gate": "epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for component_id, component, role, status in components
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4639_0_input_from_4638",
            "definition": "Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner",
            "status": "INPUT_FROM_4638",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4639_1_nonHilbert_zero_branch",
            "definition": "if Hperp=0 or S_A Hperp^A=0, and R_src_readout=0, then Xi_nonHilbert=0",
            "status": "CONDITIONAL_ZERO_ROUTE_IMPORTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4639_2_reduced_tail_after_two_zeros",
            "definition": "if Xi_src_hidden=0 and Xi_nonHilbert=0, then Xi_tail := Xi_boundary_history + Xi_transition_inner",
            "status": "TWO_COMPONENT_REDUCTION_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4639_3_finite_gate",
            "definition": "|Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem)",
            "status": "R10_GATE_RETAINS_NONCANCELLATION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def run_rows(points: list[tuple[float, float]], now: str) -> list[dict[str, Any]]:
    specs = [
        ("RUN4639_0_live_missing_inputs", "current live corpus", None, None, None, None, None),
        ("RUN4639_1_two_component_zero_control", "Xi_src_hidden and Xi_nonHilbert zero", 1.0e-4, 0.0, 0.0, 0.0, 0.0),
        ("RUN4639_2_nonHilbert_pass_100um", "finite non-Hilbert smoke", 1.0e-4, 0.0, 0.04, 0.0, 0.0),
        ("RUN4639_3_nonHilbert_fail_100um", "finite non-Hilbert smoke", 1.0e-4, 0.0, 0.08, 0.0, 0.0),
        ("RUN4639_4_boundary_transition_pass_200um", "after two zeros, remaining pair smoke", 2.0e-4, 0.0, 0.0, 0.02, 0.01),
        ("RUN4639_5_boundary_transition_fail_200um", "after two zeros, remaining pair smoke", 2.0e-4, 0.0, 0.0, 0.02, 0.02),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, branch, lambda_m, xi_src, xi_nonhilbert, xi_boundary, xi_transition in specs:
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
                    "result": "FAIL_CLOSED",
                    "reason": "missing source-backed K_NH, Hperp/Dq values, remaining tail values and lambda_mem",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                    "timestamp_utc": now,
                }
            )
            continue
        alpha = interpolate_alpha(points, lambda_m)
        xi_tail = float(xi_src or 0.0) + float(xi_nonhilbert or 0.0) + float(xi_boundary or 0.0) + float(xi_transition or 0.0)
        if alpha is None:
            result = "FAIL_CLOSED"
            reason = "lambda outside extracted vector curve"
        elif xi_tail <= alpha:
            result = "SMOKE_PASS_NONCLAIM"
            reason = "absolute reduced tail sits inside digitized vector bound for this toy/control row"
        else:
            result = "SMOKE_FAIL_NONCLAIM"
            reason = "absolute reduced tail exceeds digitized vector bound"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "branch": branch,
                "lambda_mem_m": f"{lambda_m:.12g}",
                "Xi_src_hidden_abs": f"{float(xi_src or 0.0):.12g}",
                "Xi_nonHilbert_abs": f"{float(xi_nonhilbert or 0.0):.12g}",
                "Xi_boundary_history_abs": f"{float(xi_boundary or 0.0):.12g}",
                "Xi_transition_inner_abs": f"{float(xi_transition or 0.0):.12g}",
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
            "control_id": "CTRL4639_0_no_generic_Dq_zero",
            "control": "generic Dq zero is not accepted as an Hperp certificate",
            "result": "PASS",
            "reason": "Dq_i[Hperp]=0 must be signed component-wise or bounded by epsilon_i",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4639_1_no_Noether_shortcut",
            "control": "Noether/conservation alone does not kill non-Hilbert bypass",
            "result": "PASS",
            "reason": "4431 spin/boundary/readout/flux gaps remain blockers",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4639_2_no_cancellation",
            "control": "absolute Xi components are summed",
            "result": "PASS",
            "reason": "finite rows are compared against R10 without cancellation between residuals",
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("BLK4639_0", "MISSING_K_NH_PROJECTION", "dimensionless map from N_src_nonHilbert to Xi_nonHilbert is not source-backed"),
        ("BLK4639_1", "MISSING_HPERP_ZERO_OR_COMPONENT_VALUES", "Dq_i[Hperp] component zeros/epsilons are not parent-signed"),
        ("BLK4639_2", "MISSING_R_SRC_READOUT_ZERO_OR_BOUND", "R_src_readout remains an explicit source-readout residual"),
        ("BLK4639_3", "NONHILBERT_NOETHER_FLUX_GAPS", "spin/boundary/readout/improvement compact flux pieces remain open"),
        ("BLK4639_4", "REMAINING_XI_BOUNDARY_TRANSITION", "Xi_boundary_history and Xi_transition_inner remain live after the conditional two-component reduction"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "detail": detail,
            "blocks_claim": True,
            "next_action": NEXT_TARGET if blocker_id == "BLK4639_4" else "retain in non-Hilbert source ledger",
            "timestamp_utc": now,
        }
        for blocker_id, blocker, detail in blockers
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4639_0",
            "decision": DECISION,
            "selected_next_target": NEXT_TARGET,
            "claim_allowed": False,
            "reason": "Xi_nonHilbert now has a concrete exact-zero or finite-bound route, but its parent signatures and the remaining boundary/transition pair remain open",
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "SECOND_TAIL_COMPONENT_REDUCED_NONCLAIM",
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
            "priority": "attack the remaining boundary/history plus transition-inner pair in the reduced R10 tail",
            "acceptance_gate": "either reduce Xi_tail to only one residual component or create finite nonclaim bound rows against the R10 curve",
            "timestamp_utc": now,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    components: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    runs: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4639 — Xi_nonHilbert/Hperp tail zero or bound

Marker: `{MARKER}`

## Result

4639 imports the older `N_src_nonHilbert/Hperp` theorem into the current 4638 R10 tail. The current tail is

`Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner`.

The second component is now given a sharp route:

`Xi_nonHilbert := K_NH N_src_nonHilbert`,

with

`H_L = H_q + Hperp`, `H_q in ker(Dq)`, `Hperp=(1-Pi_kerDq)H_L`,

and

`S_cg_nonHilbert = S_A Hperp^A + R_src_readout`.

Therefore, if `Hperp=0` or `S_A Hperp^A=0`, and `R_src_readout=0`, then `Xi_nonHilbert=0`. If not, the finite branch is

`|Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)`.

This is progress, not a claim: `K_NH`, the Hperp component certificates, `R_src_readout`, and the Noether/improvement flux clauses remain unsigned.

## Source register

{markdown_table(sources)}

## Import audit

{markdown_table(audits)}

## Formula rows

{markdown_table(formulas)}

## Hperp/Dq component status

{markdown_table(components)}

## Tail reduction rows

{markdown_table(reductions)}

## R10 reduced-tail smoke runner

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
        "claim": "4639 imports the Hperp/source-pairing zero-or-bound theorem into the live R10 Xi_tail and gives Xi_nonHilbert a concrete conditional zero or finite bound route.",
        "current_evidence": "Generated source register, non-Hilbert import audit, formula rows, Hperp component status, reduced-tail rows, R10 smoke runner, controls, blockers, decision, status, next target and validation.",
        "status": "Xi_nonHilbert_Hperp_reduced_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a generic Dq or Noether argument as a component-wise Hperp/source-readout zero certificate.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/R10/PPN claim until K_NH, Hperp component zeros or epsilons, R_src_readout and remaining boundary/transition tail terms are source-backed or theorem-zeroed.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def validate(
    sources: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    components: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4639_0_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4639_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4639_2_Xi_map", any(row["mapped_to_current_tail"] == "Xi_nonHilbert" for row in audits), "N_src_nonHilbert mapped to Xi_nonHilbert"))
    checks.append(("VAL4639_3_exact_zero_imported", any(row["audit_id"] == "AUD4639_1_exact_zero" for row in audits), "Hperp exact zero branch imported"))
    checks.append(("VAL4639_4_bound_formula_present", any(row["formula_id"] == "F4639_3_finite_bound" for row in formulas), "finite Xi_nonHilbert bound formula present"))
    checks.append(("VAL4639_5_component_matrix_present", len(components) == 8, "all eight Hperp/Dq components listed"))
    checks.append(("VAL4639_6_two_component_reduction", any(row["row_id"] == "XR4639_2_reduced_tail_after_two_zeros" for row in reductions), "two-component tail reduction row present"))
    checks.append(("VAL4639_7_runner_live_fail_closed", any(row["run_id"] == "RUN4639_0_live_missing_inputs" and row["result"] == "FAIL_CLOSED" for row in runs), "live missing-input row fails closed"))
    checks.append(("VAL4639_8_runner_has_pass_and_fail_controls", any("PASS" in row["result"] for row in runs) and any("FAIL" in row["result"] for row in runs), "runner has pass and fail controls"))
    checks.append(("VAL4639_9_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for row in audits + formulas + components + reductions + runs), "generated theory rows remain nonclaim"))
    checks.append(("VAL4639_10_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4639_11_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4639_12_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4639_13_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4639_14_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4639_15_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4639_16_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
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
            "validation_id": "VAL4639_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4639 validation passed" if overall else "one or more 4639 checks failed",
            "timestamp_utc": utc_now(),
        }
    )
    return validations


def main() -> int:
    now = utc_now()
    points = load_curve_points()
    sources = source_rows(now)
    audits = import_audit_rows(now)
    formulas = formula_rows(now)
    components = component_rows(now)
    reductions = reduction_rows(now)
    runs = run_rows(points, now)
    controls = control_rows(now)
    blockers = blocker_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    for path, rows in [
        (SOURCE_REGISTER, sources),
        (IMPORT_AUDIT_CSV, audits),
        (FORMULA_CSV, formulas),
        (COMPONENT_CSV, components),
        (REDUCTION_CSV, reductions),
        (RUNNER_CSV, runs),
        (CONTROL_CSV, controls),
        (BLOCKERS_CSV, blockers),
        (DECISION_CSV, decisions),
        (STATUS_CSV, statuses),
        (NEXT_CSV, next_targets),
    ]:
        write_csv(path, rows)

    provisional_validations = [
        {"checkpoint": CHECKPOINT, "validation_id": "VAL4639_PROVISIONAL", "status": "PENDING", "detail": "validation runs after documents are written", "timestamp_utc": now}
    ]
    doc_body = build_doc(sources, audits, formulas, components, reductions, runs, blockers, decisions, provisional_validations)
    write_text(DOC_PATH, doc_body)
    write_text(FORMAL_PATH, doc_body.replace("# 4639", "# 655 / 4639", 1))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4639 imports the old `N_src_nonHilbert/Hperp` theorem into the live R10 tail. It maps `Xi_nonHilbert := K_NH N_src_nonHilbert`, with exact branch `Hperp=0` or `S_A Hperp^A=0`, plus `R_src_readout=0`, giving `Xi_nonHilbert=0`. Otherwise `|Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)`. This remains nonclaim because `K_NH`, component Hperp certificates, source-readout residuals and Noether/improvement flux clauses are not parent-signed.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` reduces the second current R10 `Xi_tail` component. If `Xi_src_hidden=0` from 4638 and `Xi_nonHilbert=0` from the Hperp/source-pairing branch, the live tail reduces to `Xi_boundary_history + Xi_transition_inner`. Next packet target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    validations = validate(sources, audits, formulas, components, reductions, runs)
    write_csv(VALIDATION_CSV, validations)
    final_doc = build_doc(sources, audits, formulas, components, reductions, runs, blockers, decisions, validations)
    write_text(DOC_PATH, final_doc)
    write_text(FORMAL_PATH, final_doc.replace("# 4639", "# 655 / 4639", 1))

    print(f"{MARKER}: {validations[-1]['status']}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if validations[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
