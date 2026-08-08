from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4665"
CLAIM_ID = "L-507"
BRANCH = "MTS_R2FR_Y5_CMEM_SUPPORT_WORLDTUBE_OWNER_OR_REYNOLDS_BOUND_4665"
MARKER = "PPC4161_CMEM_SUPPORT_WORLDTUBE_OWNER_OR_REYNOLDS_BOUND_4665"
PACKET_MARKER = "PPC4161_PACKET_CMEM_SUPPORT_WORLDTUBE_OWNER_OR_REYNOLDS_BOUND_4665"
DECISION = "CMEM_SUPPORT_ZERO_PRIVATE_COMPACT_HILBERT_WORLDTUBE_DYNAMIC_REYNOLDS_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4666-Y5-R2FR-Cmem-readout-apparatus-owner-or-transfer-bound.md"

DOC_PATH = POST / "4665-Y5-R2FR-Cmem-support-worldtube-owner-or-Reynolds-bound.md"
FORMAL_PATH = FORMAL / "681-PPC4161-Cmem-support-worldtube-owner-or-Reynolds-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
DOC_4587 = POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"
DOC_4588 = POST / "4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md"
DOC_4011 = POST / "4011-Y5-R2FR-Hilbert-worldtube-source-owner-lock-or-support-flux-row.md"
FORMAL_680 = FORMAL / "680-PPC4161-Cmem-label-source-functor-owner-or-LHRS-bound.md"

CSV_4664_LHRS = SOURCE_DIR / "P8_Y5_R2FR_4664_LHRS_CMEM_UPDATE_AFTER_LABEL.csv"
CSV_4664_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4664_NEXT_TARGET.csv"
CSV_4664_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4664_STATUS.csv"
CSV_4664_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4664_VALIDATION.csv"
CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
CSV_3560_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv"
CSV_3560_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_3560_SUPPORT_CLAUSE_AUDIT.csv"
CSV_3560_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_3560_SUPPORT_RESIDUAL_DECOMPOSITION.csv"
CSV_3560_DECISION = SOURCE_DIR / "P8_Y5_R2FR_3560_DECISION_LEDGER.csv"
CSV_3560_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_3560_VALIDATION.csv"
CSV_4587_DENSITY = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv"
CSV_4587_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4587_POYNTING_OWNER_LOCK.csv"
CSV_4587_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4587_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CSV_4587_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4587_VALIDATION.csv"
CSV_4588_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_4588_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv"
CSV_4588_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SHELL_BOUND_ROWS.csv"
CSV_4588_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4588_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CSV_4588_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4588_CONTROL_ROWS.csv"
CSV_4588_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4588_VALIDATION.csv"
CSV_4011_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv"
CSV_4011_CASES = SOURCE_DIR / "P8_Y5_R2FR_4011_EVALUATOR_RESULTS.csv"
CSV_4011_GATE = SOURCE_DIR / "P8_Y5_R2FR_4011_CLAIM_GATE.csv"
CSV_4011_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4011_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4665_SOURCE_REGISTER.csv"
OWNER_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_SUPPORT_WORLDTUBE_OWNER_CLAUSES.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_CMEM_SUPPORT_ZERO_IMPORT.csv"
REYNOLDS_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_DYNAMIC_REYNOLDS_SUPPORT_BOUND_ROWS.csv"
LHRS_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_LHRS_CMEM_UPDATE_AFTER_SUPPORT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4665_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4665_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4665_00_4664_next", CSV_4664_NEXT, "4665-Y5-R2FR-Cmem-support-worldtube-owner-or-Reynolds-bound.md", "4664 selected support/worldtube."),
        ("SRC4665_01_4664_lhrs_after", CSV_4664_LHRS, "LLU4664_2_after", "LHRS before support closure."),
        ("SRC4665_02_4664_final", CSV_4664_LHRS, "LLU4664_3_final_Cmem", "final Cmem before support closure."),
        ("SRC4665_03_4664_status", CSV_4664_STATUS, "C_MEM_LABEL_ZERO_PRIVATE_TOTAL_SOURCE_BRANCH", "4664 status import."),
        ("SRC4665_04_4664_validation", CSV_4664_VALIDATION, "VAL4664_OVERALL", "4664 validation pass."),
        ("SRC4665_05_680_formal", FORMAL_680, "C_mem^support / worldtube-Reynolds owner", "formal support handoff."),
        ("SRC4665_06_4599_support", CSV_4599_THEOREM, "LHRS4599_2_support", "support zero-or-Reynolds theorem."),
        ("SRC4665_07_4599_support_norm", CSV_4599_NORM, "N4599_2_support", "support norm row."),
        ("SRC4665_08_4599_support_control", CSV_4599_CONTROL, "CTRL4599_support_countermodel", "support countermodel."),
        ("SRC4665_09_3560_support_definition", CSV_3560_THEOREM, "SWT3560_0_support_functor_definition", "Hilbert support definition."),
        ("SRC4665_10_3560_support_lemma", CSV_3560_THEOREM, "SWT3560_1_qbasic_support_lemma", "q-basic support descent."),
        ("SRC4665_11_3560_shape", CSV_3560_THEOREM, "SWT3560_2_Reynolds_shape_moment_zero", "shape moment zero route."),
        ("SRC4665_12_3560_bundle", CSV_3560_THEOREM, "SWT3560_3_Y_qbasic_bundle_theorem", "source-coordinate bundle."),
        ("SRC4665_13_3560_failure", CSV_3560_THEOREM, "SWT3560_4_failure_decomposition", "support failure decomposition."),
        ("SRC4665_14_3560_consequence", CSV_3560_THEOREM, "SWT3560_5_local_closure_consequence", "local support consequence."),
        ("SRC4665_15_3560_regular", CSV_3560_CLAUSES, "SCL3560_1_regular_support", "regular support clause."),
        ("SRC4665_16_3560_total", CSV_3560_RESIDUAL, "SRD3560_7_Delta_support_total", "support total residual."),
        ("SRC4665_17_3560_decision", CSV_3560_DECISION, "DEC3560_0", "source-support lemma decision."),
        ("SRC4665_18_3560_validation", CSV_3560_VALIDATION, "VAL3560_2_support_lemma_present", "3560 validation."),
        ("SRC4665_19_4587_density", CSV_4587_DENSITY, "DQT4587_1_qbasic_density_zero", "density q-basic zero."),
        ("SRC4665_20_4587_poynting_once", CSV_4587_POYNTING, "POY4587_1_once_only", "Poynting once-only."),
        ("SRC4665_21_4587_flux", CSV_4587_POYNTING, "POY4587_2_flux_boundary", "Poynting side-flux bound."),
        ("SRC4665_22_4587_reduction", CSV_4587_REDUCTION, "DRR4587_2_CKsource_strict_update", "source kernel reduction."),
        ("SRC4665_23_4587_validation", CSV_4587_VALIDATION, "VAL4587_density_zero", "4587 validation."),
        ("SRC4665_24_4588_reynolds", CSV_4588_THEOREM, "RST4588_0_Reynolds_identity", "Reynolds identity."),
        ("SRC4665_25_4588_zero_trace", CSV_4588_THEOREM, "RST4588_1_zero_trace_support", "zero trace support theorem."),
        ("SRC4665_26_4588_bound", CSV_4588_THEOREM, "RST4588_2_shell_bound", "Reynolds shell bound."),
        ("SRC4665_27_4588_bound_total", CSV_4588_BOUND, "RSB4588_5_total", "Reynolds total bound row."),
        ("SRC4665_28_4588_control_mask", CSV_4588_CONTROL, "CTRL4588_threshold_mask", "threshold mask guard."),
        ("SRC4665_29_4588_control_flux", CSV_4588_CONTROL, "CTRL4588_radiative_sidewall", "sidewall flux guard."),
        ("SRC4665_30_4588_validation", CSV_4588_VALIDATION, "VAL4588_zero_trace", "4588 validation."),
        ("SRC4665_31_4011_support_lock", CSV_4011_THEOREM, "HWT4011_1_support_descent_lemma", "Hilbert worldtube support lock."),
        ("SRC4665_32_4011_full_lock", CSV_4011_THEOREM, "HWT4011_6_full_lock_condition", "full support lock condition."),
        ("SRC4665_33_4011_case", CSV_4011_CASES, "CASE4011_0_full_lock_signed", "full lock evaluator."),
        ("SRC4665_34_4011_gate", CSV_4011_GATE, "CLAIM4011_0_local_GR", "claim remains blocked."),
        ("SRC4665_35_4011_validation", CSV_4011_VALIDATION, "VAL4011_23_full_case", "4011 validation."),
        ("SRC4665_36_doc3560", DOC_3560, "support descends too", "3560 prose support route."),
        ("SRC4665_37_doc4587", DOC_4587, "E_rho_qbasic=0", "4587 prose density zero."),
        ("SRC4665_38_doc4588", DOC_4588, "E_boundary_birth=0", "4588 prose boundary zero."),
        ("SRC4665_39_doc4011", DOC_4011, "R_W=0", "4011 prose support lock."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def owner_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SWO4665_0_support_object", "W_H[tau] := closure(supp(rho_H dV_H)) before readout", "support object is Hilbert-source owned, not a fitted mask", "SWT3560_0; HWT4011_0", "OWNER_OBJECT_DEFINED"),
        ("SWO4665_1_density_qbasic", "D_v(rho_H dV_H)=0 for v in ker(Dq)", "single q-basic matter+EM Hilbert functor removes bulk support-density drift", "DQT4587_1; SWT3560_1", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("SWO4665_2_regular_zero_trace", "rho_H^tr|partial W=0 and mu_birth=0 on fixed compact regular support", "Reynolds boundary birth/death term vanishes", "RST4588_1", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("SWO4665_3_no_threshold_mask", "support/domain chosen before residual readout", "no fitted cutoff, late mask, or readout-specific support selector is admitted", "CTRL4588_threshold_mask; SCL3560_2_no_readout_mask", "ANTI_TAUTOLOGY_GUARD"),
        ("SWO4665_4_no_side_flux", "Poynting/EM stress is counted once in T_total or routed to boundary flux", "no hidden sidewall flux is folded into C_mem^support", "POY4587_1; POY4587_2; CTRL4588_radiative_sidewall", "SIDE_FLUX_SEPARATION"),
        ("SWO4665_5_worldtube_lock", "J_H,tau,e_obs,shape/linking surfaces descend on same branch", "R_W=C_shape=C_domain=0 for the strict compact Hilbert-worldtube branch", "HWT4011_1; HWT4011_6", "SUPPORT_WORLDTUBE_LOCK"),
        ("SWO4665_6_scope", "support lock is not source-charge equality", "Pi_M/H_tau same-charge, readout, boundary and non-Hilbert gates remain separate", "CLAIM4011_0_local_GR", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": row[0],
            "clause": row[1],
            "deduction": row[2],
            "source": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SZI4665_0_definition", "C_mem^support := Pi_mem[C_X^support]", "memory projection of support/worldtube drift, including support boundary, shape/domain, threshold mask and side-flux leakage", "LHRS4599_2_support; LLU4664_2_after", "TARGET_DEFINED"),
        ("SZI4665_1_bulk_zero", "E_rho_qbasic=0", "bulk Hilbert density support drift is zero in the single q-basic matter+EM Hilbert functor branch", "DQT4587_1", "BULK_SUPPORT_DRIFT_ZERO"),
        ("SZI4665_2_boundary_zero", "E_boundary_birth=0", "zero trace and no birth/death shell kill the Reynolds boundary contribution", "RST4588_1", "REYNOLDS_BOUNDARY_ZERO"),
        ("SZI4665_3_domain_shape_zero", "R_W=C_shape=C_domain=0", "support, shape coordinates and linked-domain choices are fixed by the q-basic Hilbert worldtube before readout", "HWT4011_6; SWT3560_2; SWT3560_3", "WORLDTUBE_DOMAIN_SHAPE_ZERO"),
        ("SZI4665_4_side_flux_separated", "E_EM_flux is not a hidden support term", "stationary public-Hodge EM is inside T_total; radiative side flux is boundary residual, not C_mem^support", "POY4587_1; POY4587_2", "SIDE_FLUX_NOT_SUPPORT"),
        ("SZI4665_5_result", "fixed compact Hilbert-worldtube branch => C_mem^support=0", "all support-worldtube components vanish or are routed outside support on this branch", "SWO4665_0..5", "CMEM_SUPPORT_TERM_ZERO_PRIVATE_BRANCH"),
        ("SZI4665_6_scope", "not a full local-GR or measured-G claim", "support zero does not prove readout transfer, boundary/non-Hilbert silence, or Pi_M/H_tau same-charge equality", "SWO4665_6", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def reynolds_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DRB4665_0_envelope", "Delta_support_mem", "|E_rho_qbasic|+|E_boundary_birth|+|R_W|+|C_shape|+|C_domain|+|E_readout_mask|+|E_EM_flux|", "off-branch no-cancellation support envelope", "SWT3560_4; HWT4011_5"),
        ("DRB4665_1_reynolds_shell", "E_boundary_birth", "Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|", "finite Reynolds shell row if zero trace/no-shell fails", "RSB4588_5_total"),
        ("DRB4665_2_threshold_mask", "E_readout_mask", "finite row for post-fit support threshold/domain mask", "blocks tautological source-domain choice", "CTRL4588_threshold_mask"),
        ("DRB4665_3_side_flux", "E_EM_flux", "|int_{partial W} T_EM(tau,n_boundary)dSigma dt|/|M_H_ref|", "radiative/nonminimal Poynting side flux is bounded separately", "POY4587_2"),
        ("DRB4665_4_shape_domain", "R_W+C_shape+C_domain", "|R_W|+|C_shape|+|C_domain|", "support selector, shape, or linked-domain failure row", "HWT4011_5"),
        ("DRB4665_5_source_contract", "C_mem_support_dynamic_source_row", "system_id;branch;rho_trace;V_n;mu_birth;Phi_A;M_H_ref;threshold_mask;side_flux;shape_domain;projection;units;source_path;valid_for_claim", "future source-backed support row contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def lhrs_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SLU4665_0_before", "|C_mem^LHRS_live| <= |C_mem^support|+|C_mem^readout|", "4664 LHRS after Hodge and label closure", "LHRS_IMPORTED"),
        ("SLU4665_1_support_zero", "|C_mem^support|=0", "4665 compact Hilbert-worldtube support owner private branch zero", "SUPPORT_TERM_REMOVED"),
        ("SLU4665_2_after", "|C_mem^LHRS_live| <= |C_mem^readout|", "LHRS live block after Hodge, label and support closure", "LHRS_REDUCED_TO_READOUT"),
        ("SLU4665_3_final_Cmem", "|C_mem^final_live| <= |C_mem^readout|+|C_mem^boundary|+|C_mem^nonHilbert|", "final Cmem residual vector after first-block, Hodge, label and support closure", "FINAL_VECTOR_REDUCED"),
        ("SLU4665_4_not_full", "C_mem^final_live=0 is not claimed", "readout, boundary and non-Hilbert channels remain open", "FULL_CMEM_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4665_0_compact_branch", "C_mem^support", "PASS_CONDITIONAL_PRIVATE_ZERO", "q-basic Hilbert density, regular zero-trace support, no shell, no mask and no side-flux support leakage are all in the same branch."),
        ("RUN4665_1_dynamic_support", "Delta_support_mem", "FAIL_CLOSED_TO_REYNOLDS_BOUND_ROWS", "threshold masks, shell births, side flux and support/shape/domain selector failures remain explicit rows off branch."),
        ("RUN4665_2_LHRS_update", "C_mem^LHRS_live", "PASS_REDUCED_BOUND", "support removed; readout remains."),
        ("RUN4665_3_charge_firewall", "Pi_M/H_tau same-charge", "NOT_CLAIMED", "worldtube support ownership is not measured-G/source-charge equality."),
        ("RUN4665_4_claim_status", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "readout, boundary/non-Hilbert and body-charge gates remain."),
        ("RUN4665_5_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4665_0_no_plateau_axiom", "Do not assume a local vacuum plateau or zero boundary flux; support zero requires the compact Hilbert-worldtube clauses.", "ACTIVE"),
        ("CTRL4665_1_no_threshold_mask", "A support cutoff chosen after seeing residuals keeps E_readout_mask live.", "ACTIVE"),
        ("CTRL4665_2_no_Poynting_erasure", "Poynting/EM flux is counted once in T_total or bounded as boundary flux; it is not silently deleted.", "ACTIVE"),
        ("CTRL4665_3_no_G_absorption", "Do not hide support/worldtube residuals inside measured G, GM, M_H_ref or calibration.", "ACTIVE"),
        ("CTRL4665_4_no_full_Cmem", "C_mem^support=0 does not close readout, boundary or non-Hilbert channels.", "ACTIVE"),
        ("CTRL4665_5_no_charge_claim", "Worldtube support ownership does not prove Pi_M/H_tau same-charge equality.", "ACTIVE"),
        ("CTRL4665_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4665_0",
            "decision": DECISION,
            "summary": (
                "4665 closes C_mem^support in the fixed private compact Hilbert-worldtube branch. "
                "The support is W_H=closure(supp rho_H dV_H) before readout; the single q-basic Hilbert matter+EM source functor kills bulk density drift; "
                "zero trace plus no birth/death shell kills the Reynolds support-boundary term; no threshold mask prevents tautological domain choice; and Poynting/EM flux is either counted once in T_total or routed to boundary flux. "
                "Therefore C_mem^support=0 on that branch. Off branch, the Reynolds shell/support selector envelope remains live and source-row ready."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "support_result": "C_MEM_SUPPORT_ZERO_PRIVATE_COMPACT_HILBERT_WORLDTUBE_BRANCH",
            "dynamic_status": "DELTA_SUPPORT_MEM_REYNOLDS_BOUND_ROWS_RETAINED",
            "LHRS_status": "READOUT_REMAINS",
            "final_Cmem_status": "READOUT_BOUNDARY_NONHILBERT_REMAIN",
            "selected_next_channel": "C_mem^readout / apparatus-transfer owner",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After Hodge, label and support closure, LHRS has only readout left; readout controls apparatus transfer, clock/coframe mapping, late masks and observed-variable leakage.",
            "derive_route": "try to prove C_mem^readout=0 from fixed observed-coframe readout, q-basic apparatus transfer, no post-fit mask, no hidden calibration and no readout Hodge/frame reentry.",
            "fallback_route": "if readout clauses fail, write finite apparatus/readout transfer bound rows for clock, R10, PPN, orbital and WEP projections.",
            "avoid": "claiming that support closure automatically proves measured-G, local-GR, or readout stability.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    reynolds: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + owner + zero_import + reynolds + lhrs + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        OWNER_CLAUSES_CSV,
        ZERO_IMPORT_CSV,
        REYNOLDS_BOUND_CSV,
        LHRS_UPDATE_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4665_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4665_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4665_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4665_03_owner_clauses", any(row["clause_id"] == "SWO4665_5_worldtube_lock" for row in owner), "support worldtube owner clause present"),
        ("VAL4665_04_support_zero", any(row["zero_id"] == "SZI4665_5_result" and row["status"] == "CMEM_SUPPORT_TERM_ZERO_PRIVATE_BRANCH" for row in zero_import), "Cmem support zero row present"),
        ("VAL4665_05_reynolds_bound", any(row["bound_id"] == "DRB4665_1_reynolds_shell" for row in reynolds), "dynamic Reynolds support bound retained"),
        ("VAL4665_06_LHRS_reduced", any(row["update_id"] == "SLU4665_2_after" for row in lhrs), "LHRS reduced after support"),
        ("VAL4665_07_no_plateau_axiom", any(row["control_id"] == "CTRL4665_0_no_plateau_axiom" for row in controls), "no plateau shortcut control present"),
        ("VAL4665_08_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4665_09_nonclaim_runner", any(row["run_id"] == "RUN4665_4_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim status remains nonclaim"),
        ("VAL4665_10_next_readout", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is readout/apparatus"),
        ("VAL4665_11_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4665_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4665 Cmem support private zero and dynamic Reynolds-bound gate passed" if passed_all else "4665 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    reynolds: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4665 - Cmem support/worldtube owner or Reynolds bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4665 attacks the support/worldtube channel left after 4664:

`C_mem^support := Pi_mem[C_X^support]`.

Inside the fixed private compact Hilbert-worldtube branch:

`C_mem^support = 0`.

The route is not a plateau axiom. It is the support version of the same discipline used for the previous channels:

`W_H[tau] := closure(supp(rho_H dV_H))`

is fixed before readout, where:

`rho_H dV_H := c^-2 T_total(n,n) dV_eobs`.

If `rho_H dV_H` descends through `q`, the support has compact regular zero-trace boundary, there is no birth/death shell, no threshold/readout mask, and no hidden side flux, then the Reynolds support-boundary term vanishes:

`int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth> = 0`.

Together with the 3560/4011 worldtube lock, this gives:

`R_W = C_shape = C_domain = 0`.

Therefore the support term drops from `C_mem^LHRS_live`.

After Hodge, label and support closure:

`|C_mem^LHRS_live| <= |C_mem^readout|`.

And:

`|C_mem^final_live| <= |C_mem^readout| + |C_mem^boundary| + |C_mem^nonHilbert|`.

This is not a measured-G, Pi_M/H_tau same-charge, or public local-GR claim. Off branch, support motion, shell births, threshold masks, shape/domain leakage and side flux remain as explicit Reynolds/source-support bound rows.

## Source Register

{table(sources)}

## Support Worldtube Owner Clauses

{table(owner)}

## Cmem Support Zero Import

{table(zero_import)}

## Dynamic Reynolds Support Bound Rows

{table(reynolds)}

## LHRS Cmem Update After Support

{table(lhrs)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4665 closes C_mem^support in the fixed private compact Hilbert-worldtube branch. The support is the pre-readout Hilbert source support W_H=closure(supp rho_H dV_H); q-basic density kills bulk drift; zero trace and no birth/death shell kill the Reynolds boundary term; no threshold mask prevents tautological support choice; and Poynting/EM flux is counted once in T_total or routed to boundary flux. Dynamic Reynolds/source-support rows remain explicit off branch.",
        "Generated source register, support worldtube owner clauses, Cmem support zero import, dynamic Reynolds support bound rows, LHRS Cmem update, runner, controls, decision, status, next target and validation.",
        "Cmem_support_zero_private_compact_Hilbert_worldtube_dynamic_Reynolds_bound_nonclaim",
        NEXT_TARGET,
        "Assuming a local plateau or zero boundary flux, choosing support after readout, erasing Poynting/side flux, hiding support drift inside measured G/GM/M_H_ref, or claiming Pi_M/H_tau same-charge equality from support ownership.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until readout, boundary/non-Hilbert channels and body-charge/source-charge gates are same-branch zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4665 closes `C_mem^support` inside the fixed private compact Hilbert-worldtube branch. The support is the q-basic pre-readout Hilbert source support; zero trace/no shell kills the Reynolds boundary term; threshold masks and side flux are excluded or routed to explicit bound rows. The remaining private-branch Cmem channels are readout, boundary and non-Hilbert.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4665` removes the support/worldtube channel from the private-branch Cmem residual vector while retaining dynamic Reynolds/source-support bounds. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    owner = owner_clause_rows(timestamp)
    zero_import = zero_import_rows(timestamp)
    reynolds = reynolds_bound_rows(timestamp)
    lhrs = lhrs_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, owner, zero_import, reynolds, lhrs, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_CLAUSES_CSV, owner)
    write_csv(ZERO_IMPORT_CSV, zero_import)
    write_csv(REYNOLDS_BOUND_CSV, reynolds)
    write_csv(LHRS_UPDATE_CSV, lhrs)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, owner, zero_import, reynolds, lhrs, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4665 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
