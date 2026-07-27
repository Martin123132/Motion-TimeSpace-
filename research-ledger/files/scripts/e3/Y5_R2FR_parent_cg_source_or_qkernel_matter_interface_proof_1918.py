from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1918"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1918-Y5-R2FR-parent-cg-source-or-qkernel-matter-interface-proof.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1917_doc": ROOT / "1917-Y5-R2FR-single-public-metric-q-kernel-null-certificate-or-first-cg-row.md",
    "1917_validation": OUT / "P8_Y5_BRR545_1917_VALIDATION.csv",
    "1917_spm_audit": OUT / "P8_Y5_PARENT_QLOC_1917_SINGLE_PUBLIC_METRIC_QKERNEL_AUDIT.csv",
    "1917_cg_row": OUT / "P8_Y5_PARENT_QLOC_1917_FIRST_CG_ROW_NONCLAIM.csv",
    "1917_blockers": OUT / "P8_Y5_PARENT_QLOC_1917_CG_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
    "1917_closure_policy": OUT / "P8_Y5_PARENT_QLOC_1917_SPM_CLOSURE_POLICY_NONCLAIM.csv",
    "1917_next": OUT / "P8_Y5_PARENT_QLOC_1917_NEXT_TARGET.csv",
    "1032_doc": ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
    "1032_validation": OUT / "P8_Y5_BRR545_1032_VALIDATION.csv",
    "1032_closure_ledger": OUT / "P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv",
    "1032_acquisition": OUT / "P8_Y5_R10_1032_CG_TAU_ACQUISITION_TEMPLATE.csv",
    "1032_refusal": OUT / "P8_Y5_R10_1032_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "1032_readiness": OUT / "P8_Y5_R10_1032_R10_PPN_READINESS_MAP.csv",
    "1032_claim_gates": OUT / "P8_Y5_R10_1032_CLAIM_GATES.csv",
    "1033_doc": ROOT / "1033-Y5-R10-tau-R10-projection-derivation-or-source-acquisition.md",
    "1033_validation": OUT / "P8_Y5_BRR545_1033_VALIDATION.csv",
    "1033_tau_audit": OUT / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
    "1033_acquisition": OUT / "P8_Y5_R10_1033_R10_ACQUISITION_TEMPLATE.csv",
    "1033_claim_gates": OUT / "P8_Y5_R10_1033_CLAIM_GATES.csv",
    "1915_priority": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1917_doc": ["SPQ1917_6_total_verdict", "NEXT1917_0_primary"],
    "1917_validation": ["VAL1917_OVERALL", "PASS"],
    "1917_spm_audit": ["SPQ1917_6_total_verdict", "NOT_DERIVED_CURRENT_CORPUS_CLOSURE_ONLY"],
    "1917_cg_row": ["CG1917_0_first_cg_row", "MISSING_PARENT_INPUT"],
    "1917_blockers": ["CGBL1917_0_parent_value", "MISSING_PARENT_INPUT_OR_THEOREM"],
    "1917_closure_policy": ["SPMC1917_0_closure_name", "AVAILABLE_AS_CLOSURE_ONLY"],
    "1917_next": ["NEXT1917_0_primary", "1918-Y5-R2FR-parent-cg-source-or-qkernel-matter-interface-proof.md"],
    "1032_doc": ["Single Public Metric is now a formal nonclaim closure branch", "finite `c_g/tau_R10/tau_PPN` branch"],
    "1032_validation": ["V1032_14_formalization_untouched", "pass"],
    "1032_closure_ledger": ["SPML1032_0_branch_definition", "closure branch only"],
    "1032_acquisition": ["ACQ1032_1_finite_cg_value", "MISSING_PARENT_INPUT"],
    "1032_refusal": ["REF1032_1_1_finite_cg_value", "rejected_missing_provenance"],
    "1032_readiness": ["READY1032_3_SPM_closure", "CLOSURE_READY_NONCLAIM"],
    "1032_claim_gates": ["CGATE1032_1_spm_derived", "false"],
    "1033_doc": ["TAUR1033_6_verdict", "R10ACQ1033_4_cg"],
    "1033_validation": ["V1033_14_formalization_untouched", "pass"],
    "1033_tau_audit": ["TAUR1033_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1033_acquisition": ["R10ACQ1033_4_cg", "MISSING_PARENT_INPUT"],
    "1033_claim_gates": ["CGATE1033_4_R10_pass", "false"],
    "1915_priority": ["readout_tau_residual", "DEFER_AFTER_FRAME_TARGET"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1918_SOURCE_REGISTER.csv",
    "parent_cg_source_audit": OUT / "P8_Y5_PARENT_QLOC_1918_PARENT_CG_SOURCE_AUDIT.csv",
    "qkernel_matter_proof": OUT / "P8_Y5_PARENT_QLOC_1918_QKERNEL_MATTER_INTERFACE_PROOF_ATTEMPT.csv",
    "cg_final_status": OUT / "P8_Y5_PARENT_QLOC_1918_CG_FINAL_STATUS_NONCLAIM.csv",
    "closure_demotion": OUT / "P8_Y5_PARENT_QLOC_1918_FRAME_ZERO_CLOSURE_DEMOTION.csv",
    "route_update": OUT / "P8_Y5_PARENT_QLOC_1918_RESIDUAL_ROUTE_UPDATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1918_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1918_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1918_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1918_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1918_VALIDATION.csv",
}


BRANCH_COPIES = {
    "closure_demotion": SOURCE_WEIGHT_DOCS / "FRAME_ZERO_CLOSURE_DEMOTION_1918_NONCLAIM.csv",
    "cg_final_status": MICROSCOPE_RESIDUALS / OUTPUTS["cg_final_status"].name,
    "route_update": QUEUE / "JR1918_RESIDUAL_ROUTE_UPDATE.csv",
    "claim_gate": QUARANTINE / OUTPUTS["claim_gate"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
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
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    rows = []
    for key, path in INPUTS.items():
        needles = SOURCE_NEEDLES[key]
        exists = path.exists()
        text = source_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        status = "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_OR_NEEDLE_FAILED"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1918 parent c_g source or q-kernel/matter-interface proof",
                "needles": ";".join(needles),
                "status": status,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def build_parent_cg_source_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCG1918_0_parent_zero_theorem",
            "target": "c_g=0 from parent theorem",
            "required_evidence": "parent-signed no-extra-frame action slot plus q-kernel/matter-interface proof",
            "current_evidence": "SPQ1917_6 says not derived; CGATE1032_1 rejects SPM as derived theorem",
            "result": "NOT_ACQUIRED",
            "source_path_or_row": "MISSING_PARENT_THEOREM_SOURCE",
            "claim_effect": "cannot set c_g=0 outside explicit closure",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCG1918_1_finite_parent_value",
            "target": "finite numeric c_g",
            "required_evidence": "numeric c_g, units, source path, source row id, uncertainty/prior, derivation status",
            "current_evidence": "CG1917_0_first_cg_row, ACQ1032_1, R10ACQ1033_4 all carry MISSING_PARENT_INPUT",
            "result": "NOT_ACQUIRED",
            "source_path_or_row": "MISSING_PARENT_SOURCE",
            "claim_effect": "finite c_g branch remains unscoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCG1918_2_spm_closure_zero",
            "target": "c_g=0 inside SPM closure",
            "required_evidence": "explicit closure branch ledger and language boundary",
            "current_evidence": "SPML1032_0 and SPMC1917_1 set c_g=0 only inside closure branch",
            "result": "ACQUIRED_AS_NONCLAIM_CLOSURE_ONLY",
            "source_path_or_row": "P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv:SPML1032_1_zero_policy",
            "claim_effect": "allowed only as labelled closure branch, not MTS theorem evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCG1918_3_projection_companions",
            "target": "tau_R10/tau_PPN/K_X/Qbar/source profile companions",
            "required_evidence": "branch-locked arena projection factors before score",
            "current_evidence": "TAUR1033_6 says tau_R10/K_X/Qbar/c_g/bound curve/tail envelope are missing",
            "result": "NOT_ACQUIRED",
            "source_path_or_row": "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv:TAUR1033_6_verdict",
            "claim_effect": "even a finite c_g would still need projection inputs before R10/PPN scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PCG1918_4_verdict",
            "target": "parent c_g source status after 1918",
            "required_evidence": "one of theorem-zero source, finite c_g source, or explicit closure demotion",
            "current_evidence": "theorem and finite source missing; closure ledger exists",
            "result": "CLOSURE_DEMOTION_SELECTED",
            "source_path_or_row": "P8_Y5_PARENT_QLOC_1918_FRAME_ZERO_CLOSURE_DEMOTION.csv",
            "claim_effect": "frame-zero route demoted to closure-only; finite c_g retained unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_qkernel_matter_proof() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QMI1918_0_qkernel_null",
            "claim_piece": "v in ker(Dq) is presymplectic-null/gauge and boundary silent",
            "mathematical_form": "i_v Omega_parent=0 and i_v Theta_parent=dB_v with zero compact local flux",
            "current_evidence": "SPQ1917_4_qkernel_null failed current corpus",
            "current_status": "NOT_PARENT_SIGNED",
            "if_unsigned": "Dq[v]=0 remains insufficient for physical silence",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QMI1918_1_matter_interface",
            "claim_piece": "ordinary matter evaluates only terminal/public coframe before any non-public labels",
            "mathematical_form": "S_A=Sbar_A[Psi_A,e_pub(q),omega[e_pub],theta_A(q)] and not S_A[Psi_A,E_A(q),labels]",
            "current_evidence": "SPQ1917_3 and TPM1031_2 mark this as needed extra premise",
            "current_status": "NOT_PARENT_DERIVED",
            "if_unsigned": "shadow/non-terminal frame can enter before the terminal map",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QMI1918_2_no_extra_Ag_slot",
            "claim_piece": "no independent A_g(Xhat)e_pub matter/source frame slot",
            "mathematical_form": "Allowed[S_matter] excludes A_g(Xhat)e_pub unless A_g factors through q",
            "current_evidence": "SPMC1917_0 closure permits exclusion by assumption; no parent theorem source",
            "current_status": "CLOSURE_ONLY_NOT_THEOREM",
            "if_unsigned": "c_g/b_g finite row stays live",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QMI1918_3_field_rename_guard",
            "claim_piece": "frame dependence cannot be moved into constants/source/readout/boundary terms",
            "mathematical_form": "same parent ledger owns e_pub, theta_A, alpha_EM, G_eff, T_total, tau/readout, and W_source",
            "current_evidence": "SPQ1917_5 required guard not parent-signed",
            "current_status": "NOT_PARENT_SIGNED",
            "if_unsigned": "c_g=0 can reappear as b_A, b_alpha, q_nonH, Delta_tau_n, or Delta_W_support",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QMI1918_4_verdict",
            "claim_piece": "q-kernel plus matter-interface removes A_g",
            "mathematical_form": "QMI1918_0 through QMI1918_3 parent-signed => c_g=0 theorem",
            "current_evidence": "no clause is parent-signed in current corpus",
            "current_status": "PROOF_FAILS_CURRENT_CORPUS",
            "if_unsigned": "demote frame-zero route to closure-only and move to next residual",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_cg_final_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG1918_0_final_cg_status",
            "symbol": "c_g/b_g",
            "zero_theorem_status": "NOT_PARENT_SIGNED",
            "finite_value_status": "MISSING_PARENT_INPUT",
            "closure_status": "ZERO_ONLY_INSIDE_EXPLICIT_SPM_CLOSURE_NONCLAIM",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "uncertainty_or_prior": "MISSING_UNCERTAINTY",
            "normalization": "MISSING_XHAT_NORMALIZATION",
            "arena_projection": "MISSING_ARENA_PROJECTION",
            "retained_as": "FINITE_FRAME_RESIDUAL_OR_CLOSURE_BRANCH_CHOICE",
            "next_allowed_use": "SPM closure branch can set c_g=0 only when labelled closure; finite branch remains unscoreable",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_closure_demotion() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "FZD1918_0_frame_zero_route",
            "route": "frame_or_coframe_residual zero via SPM/q-kernel",
            "previous_status": "promising conditional theorem route",
            "new_status": "CLOSURE_ONLY_UNLESS_NEW_PARENT_SOURCE_APPEARS",
            "reason": "one last narrow pass found no parent-signed q-kernel, matter-interface, no-extra-A_g slot, or finite c_g source",
            "what_survives": "SPM closure branch; finite c_g row; no-cancellation envelope; blockers",
            "what_is_forbidden": "claiming c_g=0, local-GR pass, R10/PPN/WEP/clock/orbital score from this route",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "FZD1918_1_spm_closure",
            "route": "Single Public Metric closure",
            "previous_status": "closure branch available",
            "new_status": "EXPLICIT_MODEL_BRANCH_NONCLAIM",
            "reason": "SPML1032 ledger is internally consistent but not derived from parent action",
            "what_survives": "c_g=0 and b_dis=0 by branch definition inside closure",
            "what_is_forbidden": "using closure-zero as evidence for derived MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "FZD1918_2_finite_branch",
            "route": "finite c_g branch",
            "previous_status": "first row staged",
            "new_status": "RETAINED_UNFILLED_NONCLAIM",
            "reason": "finite c_g, tau_R10, K_X, Qbar_XH, tau_PPN, and projections remain missing",
            "what_survives": "source-ready schema and blocker ledger",
            "what_is_forbidden": "setting tau_R10=1, fitting c_g from bounds, or cancelling unknowns",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_route_update() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_update_id": "RU1918_0_frame_route",
            "residual_component": "frame_or_coframe_residual",
            "priority_rank": 1,
            "status_after_1918": "DEMOTED_TO_CLOSURE_OR_RETAINED_FINITE_NONCLAIM",
            "why": "no parent c_g theorem/source; SPM is closure-only",
            "future_reopen_condition": "new parent action source signs q-kernel/matter-interface/no-extra-frame, or finite c_g source is acquired",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "route_update_id": "RU1918_1_next_residual",
            "residual_component": "readout_tau_residual",
            "priority_rank": 2,
            "status_after_1918": "SELECT_NEXT_ATTACK",
            "why": "1915 priority matrix ranks readout_tau next with five-arena leverage",
            "future_reopen_condition": "prove parent readout-after-variation/tau-source-normal lock or source first tau kernel row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1918_0_parent_cg_zero",
            "claim": "c_g=0 by parent theorem",
            "current_status": "FALSE_NOT_PARENT_SIGNED",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1918_1_finite_cg_value",
            "claim": "finite c_g value is source-backed",
            "current_status": "FALSE_MISSING_PARENT_INPUT",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1918_2_spm_closure",
            "claim": "SPM closure exists as labelled nonclaim branch",
            "current_status": "TRUE_CLOSURE_ONLY_NONCLAIM",
            "gate_pass": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1918_3_frame_route_claim",
            "claim": "frame residual route supports local-GR/WEP/R10/PPN/clock/orbital scoring",
            "current_status": "CLAIM_BLOCKED",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1918_4_next_route",
            "claim": "move to next residual is justified",
            "current_status": "TRUE_READOUT_TAU_SELECTED_NONCLAIM",
            "gate_pass": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1918_0_cg_verdict",
            "decision": "NO_PARENT_CG_SOURCE_OR_ZERO_THEOREM_FOUND",
            "reason": "1917/1032/1033 evidence keeps c_g and tau/projection rows missing and rejects placeholders",
            "consequence": "finite c_g branch remains nonclaim and unscoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1918_1_closure_demotion",
            "decision": "DEMOTE_FRAME_ZERO_ROUTE_TO_CLOSURE_ONLY",
            "reason": "q-kernel plus matter-interface proof does not close in current corpus",
            "consequence": "SPM can be used only as explicit closure/model branch, not derived MTS theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1918_2_next_residual",
            "decision": "MOVE_TO_READOUT_TAU_RESIDUAL",
            "reason": "frame route is now boxed; 1915 ranked readout_tau second with the broadest empirical leverage",
            "consequence": "1919 should attempt parent readout/tau descent or source the first real tau/readout kernel row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1918_0_primary",
            "selection_status": "selected",
            "target_doc": "1919-Y5-R2FR-readout-tau-parent-descent-or-source-kernel-first-row.md",
            "target_script": "scripts/Y5_R2FR_readout_tau_parent_descent_or_source_kernel_first_row_1919.py",
            "objective": "attack the rank-2 readout_tau_residual: prove readout-after-variation and tau/source-normal lock from the parent, or stage the first source-backed tau/readout kernel row as nonclaim",
            "success_condition": "readout_tau_residual gets a parent theorem-zero source path, a finite source-ready first kernel row, or a closure-only demotion with blockers preserved",
            "do_not": "do not reopen SPM/c_g scoring unless new parent source appears; do not absorb readout residuals into calibration or measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_project_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1918_0_gain",
            "area": "frame/c_g route",
            "summary": "1918 finishes the narrow parent c_g pass and prevents the frame-zero route from floating as an unclosed promise.",
            "risk_level": "DEMOTED_BUT_DISCIPLINED",
            "project_meaning": "the coupling bottleneck is now boxed: closure-only, finite unfilled, no fake scores",
            "next_action": "move to readout_tau residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1918_1_truth",
            "area": "local GR bridge",
            "summary": "No local-GR/Newton reduction follows from the frame route yet; SPM is a closure branch only.",
            "risk_level": "CLAIM_BLOCKED",
            "project_meaning": "this is a useful narrowing, not a failure of the whole project",
            "next_action": "derive/source readout and tau kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1918_2_next",
            "area": "residual priority",
            "summary": "readout_tau_residual becomes the next best target because it touches all local arenas and calibration/readout honesty.",
            "risk_level": "NEXT_ATTACK_SELECTED",
            "project_meaning": "we keep moving through the residual vector instead of circling one deadlock",
            "next_action": "1919 readout/tau pass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": build_source_register(),
        "parent_cg_source_audit": build_parent_cg_source_audit(),
        "qkernel_matter_proof": build_qkernel_matter_proof(),
        "cg_final_status": build_cg_final_status(),
        "closure_demotion": build_closure_demotion(),
        "route_update": build_route_update(),
        "claim_gate": build_claim_gate(),
        "decision": build_decision(),
        "next_target": build_next_target(),
        "project_status": build_project_status(),
    }


def copy_branch_artifacts() -> None:
    for key, destination in BRANCH_COPIES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], destination)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    unsafe: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            if "valid_for_claim" in row and bool_string(row["valid_for_claim"]) != "false":
                unsafe.append(f"{path.name}:valid_for_claim")
            if "claim_allowed" in row and bool_string(row["claim_allowed"]) != "false":
                unsafe.append(f"{path.name}:claim_allowed")
    return not unsafe, "claim flags all false" if not unsafe else ";".join(unsafe)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    failures: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:
            failures.append(f"{path.name}:{exc}")
            continue
        if not rows:
            failures.append(f"{path.name}:no_rows")
    return not failures, "all generated CSVs parse with rows" if not failures else ";".join(failures)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1918_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    cg_audit = csv_rows(OUTPUTS["parent_cg_source_audit"])
    checks.append(
        {
            "validation_id": "VAL1918_01_parent_cg_audit",
            "status": "PASS" if any(row["audit_id"] == "PCG1918_4_verdict" and row["result"] == "CLOSURE_DEMOTION_SELECTED" for row in cg_audit) else "FAIL",
            "detail": "parent c_g source audit selects closure demotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    proof_rows = csv_rows(OUTPUTS["qkernel_matter_proof"])
    checks.append(
        {
            "validation_id": "VAL1918_02_qkernel_matter_proof",
            "status": "PASS"
            if any(row["proof_id"] == "QMI1918_4_verdict" and row["current_status"] == "PROOF_FAILS_CURRENT_CORPUS" for row in proof_rows)
            and all(bool_string(row["proof_pass"]) == "false" for row in proof_rows)
            else "FAIL",
            "detail": "q-kernel/matter-interface proof remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    cg_rows = csv_rows(OUTPUTS["cg_final_status"])
    checks.append(
        {
            "validation_id": "VAL1918_03_cg_final_status",
            "status": "PASS"
            if len(cg_rows) == 1
            and cg_rows[0]["closure_status"] == "ZERO_ONLY_INSIDE_EXPLICIT_SPM_CLOSURE_NONCLAIM"
            and bool_string(cg_rows[0]["score_ready"]) == "false"
            else "FAIL",
            "detail": "c_g final row is closure-only/unfilled nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    demotion_rows = csv_rows(OUTPUTS["closure_demotion"])
    checks.append(
        {
            "validation_id": "VAL1918_04_closure_demotion",
            "status": "PASS" if any(row["demotion_id"] == "FZD1918_0_frame_zero_route" and row["new_status"] == "CLOSURE_ONLY_UNLESS_NEW_PARENT_SOURCE_APPEARS" for row in demotion_rows) else "FAIL",
            "detail": "frame-zero route explicitly demoted to closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    route_rows = csv_rows(OUTPUTS["route_update"])
    checks.append(
        {
            "validation_id": "VAL1918_05_route_update",
            "status": "PASS" if any(row["residual_component"] == "readout_tau_residual" and row["status_after_1918"] == "SELECT_NEXT_ATTACK" for row in route_rows) else "FAIL",
            "detail": "readout_tau residual selected next",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1918_06_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1918_3_frame_route_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1918_07_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1918_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1919 readout/tau route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1918_08_claim_flags_safe",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1918_09_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1918_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1918_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1918-Y5-R2FR-parent-cg",
            "P8_Y5_PARENT_QLOC_1918",
            "Y5_R2FR_parent_cg_source_or_qkernel_matter_interface_proof_1918",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append(
        {
            "validation_id": "VAL1918_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1918_artifact_count={len(formalization_hits)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1918_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1918 parent c_g source or q-kernel matter-interface proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1918 - Parent c_g Source Or q-Kernel Matter-Interface Proof

## Purpose

This checkpoint performs the promised narrow 1918 pass: either find a parent source/theorem for `c_g`, prove the q-kernel plus matter-interface route that removes `A_g`, or explicitly demote the frame-zero route to closure-only while preserving the finite branch.

## Result

- No parent theorem-zero source for `c_g` was found.
- No finite numeric/source-backed `c_g` value was found.
- The q-kernel plus matter-interface proof still fails in the current corpus.
- The Single Public Metric route is retained only as an explicit nonclaim closure branch.
- The finite `c_g` row remains unfilled/nonclaim.
- The next residual target is now `readout_tau_residual`.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent c_g Source Audit

{markdown_table(rows_by_name["parent_cg_source_audit"])}

## q-Kernel Matter-Interface Proof Attempt

{markdown_table(rows_by_name["qkernel_matter_proof"])}

## c_g Final Status

{markdown_table(rows_by_name["cg_final_status"])}

## Frame-Zero Closure Demotion

{markdown_table(rows_by_name["closure_demotion"])}

## Residual Route Update

{markdown_table(rows_by_name["route_update"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
