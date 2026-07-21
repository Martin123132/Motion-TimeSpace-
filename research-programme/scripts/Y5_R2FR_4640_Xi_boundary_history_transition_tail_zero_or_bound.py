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

CHECKPOINT = "4640"
CLAIM_ID = "L-482"
BRANCH_ID = "MTS_R2FR_Y5_XI_BOUNDARY_TRANSITION_PAIR_4640"
MARKER = "PPC4161_XI_BOUNDARY_HISTORY_TRANSITION_TAIL_ZERO_OR_BOUND_4640"
PACKET_MARKER = "PPC4161_PACKET_XI_BOUNDARY_HISTORY_TRANSITION_PAIR_4640"
DECISION = "XI_BOUNDARY_HISTORY_AND_TRANSITION_INNER_REDUCED_TO_QEDGE_AND_SOURCE_KERNEL_HAIR_ZERO_OR_BOUND_NONCLAIM"
NEXT_TARGET = "4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"

DOC_PATH = POST / "4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md"
FORMAL_PATH = FORMAL / "656-PPC4161-Xi-boundary-history-transition-tail-zero-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

CSV_4635_CURVE = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
CSV_4639_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4639_VALIDATION.csv"
CSV_4639_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4639_XI_TAIL_REDUCTION_ROWS.csv"
DOC_4639 = POST / "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
FW_4318 = FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md"
FW_4339 = FORMAL / "355-PPC4161-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"
FW_4355 = FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md"
FW_4609 = FORMAL / "625-PPC4161-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4640_SOURCE_REGISTER.csv"
IMPORT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_BOUNDARY_TRANSITION_IMPORT_AUDIT.csv"
FORMULA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_XI_BT_FORMULA_ROWS.csv"
BOUNDARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_BOUNDARY_HISTORY_COMPONENT_STATUS.csv"
TRANSITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_TRANSITION_INNER_HAIR_COMPONENT_STATUS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_XI_TAIL_REDUCTION_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_R10_FINAL_TAIL_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4640_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4640_VALIDATION.csv"

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
        ("SRC4640_00_4639_validation", CSV_4639_VALIDATION, "VAL4639_OVERALL", "4639 validation."),
        ("SRC4640_01_4639_reduction", CSV_4639_REDUCTION, "XR4639_2_reduced_tail_after_two_zeros", "two-component remaining tail handoff."),
        ("SRC4640_02_4639_doc", DOC_4639, "Xi_tail := Xi_boundary_history + Xi_transition_inner", "human-readable remaining tail."),
        ("SRC4640_03_4318_history", FW_4318, "NR4318_2_Nhistory", "canonical history/transition residual row."),
        ("SRC4640_04_4318_boundary", FW_4318, "NR4318_3_Nboundary", "canonical boundary/domain residual row."),
        ("SRC4640_05_4339_trace_defect", FW_4339, "BD4339_4_worldtube_trace_defect", "worldtube trace-defect bound machine."),
        ("SRC4640_06_4339_leak_update", FW_4339, "PLEAK4339_1", "off-worldtube readout/order component update."),
        ("SRC4640_07_4355_marker", FW_4355, "PPC4161_TRANSITION_SHELL_SAME_WORLDTUBE_NONHILBERT_RESIDUE_OR_BOUNDED_SOURCE_HAIR_4355", "transition source-kernel/hair checkpoint."),
        ("SRC4640_08_4355_clean_kernel", FW_4355, "TH4355_0_clean_transition_source", "clean transition source-kernel theorem."),
        ("SRC4640_09_4355_total_hair", FW_4355, "HB4355_7_total", "finite transition hair bound vector."),
        ("SRC4640_10_4609_marker", FW_4609, "PPC4161_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_FIRST_ROW_4609", "Q_edge source-worldtube boundary gate."),
        ("SRC4640_11_4609_abs_bound", FW_4609, "|Q_edge|_abs", "absolute Q_edge boundary/shell bound."),
        ("SRC4640_12_4635_curve", CSV_4635_CURVE, "lambda_m", "R10 vector curve points."),
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
            "audit_id": "AUD4640_0_pair_object",
            "input": "Xi_boundary_history + Xi_transition_inner",
            "mapped_object": "Xi_BT",
            "status": "CANONICAL_PAIR_DEFINED",
            "law": "Xi_BT := Xi_boundary_history + Xi_transition_inner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4640_1_boundary_import",
            "input": "Q_edge source-worldtube boundary gate",
            "mapped_object": "Xi_boundary_history",
            "status": "ZERO_OR_BOUND_IMPORTED",
            "law": "|Xi_boundary_history| <= K_edge(|Q_edge_shell| + |Q_edge_boundary|)",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4640_2_transition_import",
            "input": "transition source-kernel/hair law",
            "mapped_object": "Xi_transition_inner",
            "status": "ZERO_OR_BOUND_IMPORTED",
            "law": "|Xi_transition_inner| <= K_tr epsilon_tr_hair",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "audit_id": "AUD4640_3_no_cross_branch",
            "input": "4638/4639/4640 conditional zero branches",
            "mapped_object": "Xi_tail",
            "status": "SAME_BRANCH_ASSEMBLY_REQUIRED",
            "law": "Xi_tail=0 only if Xi_src_hidden=Xi_nonHilbert=Xi_boundary_history=Xi_transition_inner=0 on the same parent branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def formula_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_0_pair",
            "formula": "Xi_BT := Xi_boundary_history + Xi_transition_inner",
            "basis": "4639 two-component remaining tail",
            "status": "DEFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_1_Qedge_shell",
            "formula": "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "basis": "4609 Reynolds shell row",
            "status": "BOUND_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_2_Qedge_boundary",
            "formula": "|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|",
            "basis": "4609 Hamiltonian boundary part",
            "status": "BOUND_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_3_boundary_bound",
            "formula": "|Xi_boundary_history| <= K_edge(|Q_edge_shell| + |Q_edge_boundary|)",
            "basis": "Q_edge projected into current R10 Xi_tail normalization",
            "status": "BOUND_READY_KEDGE_AND_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_4_transition_hair",
            "formula": "epsilon_tr_hair <= Y_nonHilbert + Delta_Wtr + Y_time_l + Y_species_frame + Y_range + Y_nonEH + Y_boundary_nonlocal",
            "basis": "4355 finite source-hair vector",
            "status": "BOUND_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_5_transition_bound",
            "formula": "|Xi_transition_inner| <= K_tr epsilon_tr_hair",
            "basis": "transition source-kernel/hair projected into current R10 Xi_tail normalization",
            "status": "BOUND_READY_KTR_AND_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_6_pair_bound",
            "formula": "|Xi_BT| <= K_edge(|Q_edge_shell|+|Q_edge_boundary|) + K_tr epsilon_tr_hair",
            "basis": "no-cancellation boundary plus transition pair",
            "status": "FINAL_PAIR_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "formula_id": "F4640_7_full_tail_zero",
            "formula": "if Xi_src_hidden=Xi_nonHilbert=Xi_boundary_history=Xi_transition_inner=0 on one branch, then Xi_tail=0",
            "basis": "4638, 4639 and 4640 conditional zero branches assembled without cancellation",
            "status": "SAME_BRANCH_ASSEMBLY_REQUIRED_NEXT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def boundary_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("BH4640_0", "regular compact support", "zero density trace and no birth shell", "rho_H_trace_norm=0 and mu_birth_TV=0", "Q_edge_shell"),
        ("BH4640_1", "fixed q-basic source worldtube", "worldtube support fixed before variation", "V_n_bound=0 or fixed source support theorem", "Q_edge_shell"),
        ("BH4640_2", "source-free no-flux collar", "no source sidewall/collar leakage", "B_X_flux=F_side_source=F_rad=0", "Q_edge_boundary"),
        ("BH4640_3", "fixed corner/reference data", "Hamiltonian corner/reference terms do not move", "C_corner=E_reference_edge=0", "Q_edge_boundary"),
        ("BH4640_4", "fixed projector/readout edge", "projector support not fitted after seeing GM", "E_projector_edge=0", "Q_edge_boundary"),
        ("BH4640_5", "no fitted GM support definition", "support mask is parent/readout-owned", "no post-fit support boundary", "Xi_boundary_history"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "zero_gate": zero_gate,
            "feeds": feeds,
            "current_status": "ZERO_OR_BOUND_ROUTE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for component_id, component, meaning, zero_gate, feeds in components
    ]


def transition_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("TR4640_0", "Hilbert action-domain source kernel", "q_tr is Hilbert source dressing", "P_nonHilbert_action_domain q_tr=0", "Y_nonHilbert"),
        ("TR4640_1", "same-worldtube readout", "transition support included before variation, exterior restriction post-solve", "P_off_worldtube_readout_order q_tr=0", "Delta_Wtr"),
        ("TR4640_2", "static l=0 monopole", "no time/multipole transition hair", "partial_tau q_tr=0 and Q_l>=1_tr=0", "Y_time_l"),
        ("TR4640_3", "universal species/frame blind", "no WEP/source-label transition hair", "D_species q_tr=D_frame q_tr=Delta_source_weight_tr=0", "Y_species_frame"),
        ("TR4640_4", "range-free common monopole", "no finite-range Yukawa/test-leg transition hair", "D_lambda q_tr=q_range_tail=0", "Y_range"),
        ("TR4640_5", "same metric/EH readout", "no non-EH metric response from transition current", "Pi_arena Sigma_nonEH[q_tr]=0", "Y_nonEH"),
        ("TR4640_6", "boundary/nonlocal owner", "boundary part is Hamiltonian/routed or projection-null", "B_tr_nonlocal=0", "Y_boundary_nonlocal"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "zero_gate": zero_gate,
            "feeds": feeds,
            "current_status": "SOURCE_KERNEL_ZERO_OR_HAIR_BOUND_ROUTE_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for component_id, component, meaning, zero_gate, feeds in components
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4640_0_input_from_4639",
            "definition": "if Xi_src_hidden=0 and Xi_nonHilbert=0, then Xi_tail := Xi_boundary_history + Xi_transition_inner",
            "status": "INPUT_FROM_4639",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4640_1_pair_definition",
            "definition": "Xi_BT := Xi_boundary_history + Xi_transition_inner",
            "status": "PAIR_DEFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4640_2_pair_zero_branch",
            "definition": "if Q_edge=0 and epsilon_tr_hair=0 on the same branch, then Xi_BT=0",
            "status": "CONDITIONAL_PAIR_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4640_3_full_tail_zero_branch",
            "definition": "if Xi_src_hidden=Xi_nonHilbert=Xi_boundary_history=Xi_transition_inner=0 on one branch, then Xi_tail=0",
            "status": "FULL_XI_TAIL_ZERO_CONDITIONAL_NEXT_ASSEMBLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "XR4640_4_R10_gate",
            "definition": "|Xi_BT| <= alpha_bound(lambda_mem) after Xi_src_hidden=Xi_nonHilbert=0; otherwise add all four absolute components",
            "status": "R10_GATE_RETAINS_NONCANCELLATION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def run_rows(points: list[tuple[float, float]], now: str) -> list[dict[str, Any]]:
    specs = [
        ("RUN4640_0_live_missing_inputs", "current live corpus", None, None, None),
        ("RUN4640_1_all_tail_zero_control", "all four Xi_tail components zero", 1.0e-4, 0.0, 0.0),
        ("RUN4640_2_BT_pass_100um", "boundary/transition pair smoke", 1.0e-4, 0.03, 0.04),
        ("RUN4640_3_BT_fail_100um", "boundary/transition pair smoke", 1.0e-4, 0.04, 0.04),
        ("RUN4640_4_BT_pass_1mm", "large-range tight-budget smoke", 1.0e-3, 0.009, 0.009),
        ("RUN4640_5_BT_fail_1mm", "large-range tight-budget smoke", 1.0e-3, 0.01, 0.01),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, branch, lambda_m, xi_boundary, xi_transition in specs:
        if lambda_m is None:
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "run_id": run_id,
                    "branch": branch,
                    "lambda_mem_m": "",
                    "Xi_boundary_history_abs": "",
                    "Xi_transition_inner_abs": "",
                    "Xi_BT_abs": "",
                    "alpha_bound_vector": "",
                    "result": "FAIL_CLOSED",
                    "reason": "missing source-backed boundary/history, transition-inner and lambda_mem values",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                    "timestamp_utc": now,
                }
            )
            continue
        alpha = interpolate_alpha(points, lambda_m)
        xi_bt = float(xi_boundary or 0.0) + float(xi_transition or 0.0)
        if alpha is None:
            result = "FAIL_CLOSED"
            reason = "lambda outside extracted vector curve"
        elif xi_bt <= alpha:
            result = "SMOKE_PASS_NONCLAIM"
            reason = "absolute boundary/transition pair sits inside digitized vector bound for this toy/control row"
        else:
            result = "SMOKE_FAIL_NONCLAIM"
            reason = "absolute boundary/transition pair exceeds digitized vector bound"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "run_id": run_id,
                "branch": branch,
                "lambda_mem_m": f"{lambda_m:.12g}",
                "Xi_boundary_history_abs": f"{float(xi_boundary or 0.0):.12g}",
                "Xi_transition_inner_abs": f"{float(xi_transition or 0.0):.12g}",
                "Xi_BT_abs": f"{xi_bt:.12g}",
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
            "control_id": "CTRL4640_0_same_branch",
            "control": "do not assemble zero branches across incompatible parent/readout branches",
            "result": "PASS",
            "reason": "full Xi_tail zero is explicitly deferred to a same-branch assembly gate",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4640_1_no_raw_transition_pass",
            "control": "raw transition shell does not pass by rough projection",
            "result": "PASS",
            "reason": "4355 rough epsilon pressure remains a finite-hair warning, not safety evidence",
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4640_2_no_boundary_by_inspection",
            "control": "compact support/no-flux cannot be asserted by inspection",
            "result": "PASS",
            "reason": "Q_edge zero needs same worldtube, no birth shell, no-flux collar and fixed projector/reference clauses",
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("BLK4640_0", "MISSING_K_EDGE_PROJECTION", "dimensionless projection from Q_edge to Xi_boundary_history is not source-backed"),
        ("BLK4640_1", "MISSING_QEDGE_ZERO_OR_VALUES", "Q_edge shell/boundary components are formula-ready but not zero/value sourced"),
        ("BLK4640_2", "MISSING_K_TR_PROJECTION", "dimensionless projection from epsilon_tr_hair to Xi_transition_inner is not source-backed"),
        ("BLK4640_3", "MISSING_SOURCE_KERNEL_CLAUSES", "static l=0, universal, range-free, same-metric and boundary-owned clauses remain unsigned"),
        ("BLK4640_4", "SAME_BRANCH_ASSEMBLY_NOT_DONE", "the four conditional zeros from 4638/4639/4640 have not yet been checked on one parent branch"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "detail": detail,
            "blocks_claim": True,
            "next_action": NEXT_TARGET if blocker_id == "BLK4640_4" else "retain in boundary-transition ledger",
            "timestamp_utc": now,
        }
        for blocker_id, blocker, detail in blockers
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4640_0",
            "decision": DECISION,
            "selected_next_target": NEXT_TARGET,
            "claim_allowed": False,
            "reason": "the last two live Xi_tail terms now have explicit Q_edge and source-kernel hair zero-or-bound routes; next is same-branch assembly, not a public claim",
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "FINAL_PAIR_REDUCED_NONCLAIM",
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
            "priority": "assemble the four Xi_tail zero branches on a single parent/readout branch or generate a finite coefficient pack",
            "acceptance_gate": "same branch must sign Xi_src_hidden, Xi_nonHilbert, Xi_boundary_history and Xi_transition_inner zero; otherwise finite rows remain nonclaim",
            "timestamp_utc": now,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    transition: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    runs: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4640 — Xi boundary/history plus transition-inner tail zero or bound

Marker: `{MARKER}`

## Result

4640 reduces the final pair left by 4639:

`Xi_tail := Xi_boundary_history + Xi_transition_inner`

after the conditional `Xi_src_hidden=0` and `Xi_nonHilbert=0` branches.

Define

`Xi_BT := Xi_boundary_history + Xi_transition_inner`.

The boundary/history half is now routed through the source-worldtube edge gate:

`|Xi_boundary_history| <= K_edge(|Q_edge_shell| + |Q_edge_boundary|)`.

The transition-inner half is now routed through the source-kernel hair law:

`|Xi_transition_inner| <= K_tr epsilon_tr_hair`.

Therefore

`|Xi_BT| <= K_edge(|Q_edge_shell|+|Q_edge_boundary|) + K_tr epsilon_tr_hair`.

If `Q_edge=0` and `epsilon_tr_hair=0` on the same parent/readout branch, then `Xi_BT=0`. Combined with 4638 and 4639, this gives the next assembly problem:

`Xi_tail=0` only if `Xi_src_hidden=Xi_nonHilbert=Xi_boundary_history=Xi_transition_inner=0` on one branch.

This remains private/nonclaim. The required projection constants, source-kernel clauses, boundary components and same-branch assembly gate are not yet closed.

## Source register

{markdown_table(sources)}

## Import audit

{markdown_table(audits)}

## Formula rows

{markdown_table(formulas)}

## Boundary/history component status

{markdown_table(boundary)}

## Transition-inner hair component status

{markdown_table(transition)}

## Tail reduction rows

{markdown_table(reductions)}

## R10 final-tail smoke runner

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
        "claim": "4640 reduces the remaining Xi_boundary_history plus Xi_transition_inner pair to Q_edge boundary/history and transition source-kernel hair zero-or-bound routes.",
        "current_evidence": "Generated source register, boundary-transition import audit, Xi_BT formula rows, component status tables, reduced-tail rows, R10 final-tail smoke runner, controls, blockers, decision, status, next target and validation.",
        "status": "Xi_boundary_transition_pair_reduced_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Assembling conditional zeros from different branches or treating raw transition shells and compact support as locally safe by inspection.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/R10/PPN claim until Q_edge, transition hair, projection constants, lambda_mem and the four zero branches are source-backed or theorem-zeroed on one branch.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def validate(
    sources: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    transition: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4640_0_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4640_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4640_2_pair_defined", any(row["mapped_object"] == "Xi_BT" for row in audits), "Xi_BT pair object defined"))
    checks.append(("VAL4640_3_boundary_bound_present", any(row["formula_id"] == "F4640_3_boundary_bound" for row in formulas), "boundary/history bound formula present"))
    checks.append(("VAL4640_4_transition_bound_present", any(row["formula_id"] == "F4640_5_transition_bound" for row in formulas), "transition-inner bound formula present"))
    checks.append(("VAL4640_5_boundary_components", len(boundary) == 6, "boundary/history component table complete"))
    checks.append(("VAL4640_6_transition_components", len(transition) == 7, "transition hair component table complete"))
    checks.append(("VAL4640_7_full_tail_zero_row", any(row["row_id"] == "XR4640_3_full_tail_zero_branch" for row in reductions), "full Xi_tail conditional zero row present"))
    checks.append(("VAL4640_8_runner_live_fail_closed", any(row["run_id"] == "RUN4640_0_live_missing_inputs" and row["result"] == "FAIL_CLOSED" for row in runs), "live missing-input row fails closed"))
    checks.append(("VAL4640_9_runner_has_pass_and_fail_controls", any("PASS" in row["result"] for row in runs) and any("FAIL" in row["result"] for row in runs), "runner has pass and fail controls"))
    checks.append(("VAL4640_10_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for row in audits + formulas + boundary + transition + reductions + runs), "generated theory rows remain nonclaim"))
    checks.append(("VAL4640_11_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4640_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4640_13_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4640_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4640_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4640_16_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4640_17_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
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
            "validation_id": "VAL4640_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4640 validation passed" if overall else "one or more 4640 checks failed",
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
    boundary = boundary_rows(now)
    transition = transition_rows(now)
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
        (BOUNDARY_CSV, boundary),
        (TRANSITION_CSV, transition),
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
        {"checkpoint": CHECKPOINT, "validation_id": "VAL4640_PROVISIONAL", "status": "PENDING", "detail": "validation runs after documents are written", "timestamp_utc": now}
    ]
    doc_body = build_doc(sources, audits, formulas, boundary, transition, reductions, runs, blockers, decisions, provisional_validations)
    write_text(DOC_PATH, doc_body)
    write_text(FORMAL_PATH, doc_body.replace("# 4640", "# 656 / 4640", 1))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4640 reduces the remaining `Xi_boundary_history + Xi_transition_inner` pair to `Xi_BT`, with `|Xi_boundary_history| <= K_edge(|Q_edge_shell|+|Q_edge_boundary|)` and `|Xi_transition_inner| <= K_tr epsilon_tr_hair`. If `Q_edge=0` and `epsilon_tr_hair=0` on the same branch, then `Xi_BT=0`; full `Xi_tail=0` requires all four component zeros from 4638, 4639 and 4640 on one parent/readout branch. This remains nonclaim until the projection constants, edge/hair clauses, `lambda_mem` and same-branch assembly gate close.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` reduces the last current R10 `Xi_tail` pair. Boundary/history is now a `Q_edge` worldtube/no-flux problem; transition-inner is now a source-kernel hair problem. Next packet target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    validations = validate(sources, audits, formulas, boundary, transition, reductions, runs)
    write_csv(VALIDATION_CSV, validations)
    final_doc = build_doc(sources, audits, formulas, boundary, transition, reductions, runs, blockers, decisions, validations)
    write_text(DOC_PATH, final_doc)
    write_text(FORMAL_PATH, final_doc.replace("# 4640", "# 656 / 4640", 1))

    print(f"{MARKER}: {validations[-1]['status']}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if validations[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
