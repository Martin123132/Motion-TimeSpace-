from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3014"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3014-Y5-R2FR-parent-source-current-owner-for-R10-kernel-or-rank-zero-local-closure-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3014_00_3013_doc": ROOT / "3013-Y5-R2FR-R10-q_loc-to-Yukawa-projection-kernel-or-calibrated-curve-import-under-AX1090.md",
    "SRC3014_01_3013_next": RESIDUALS / "P8_Y5_R2FR_3013_NEXT_TARGET.csv",
    "SRC3014_02_3013_kernel": RESIDUALS / "P8_Y5_R2FR_3013_R10_KERNEL_DERIVATION.csv",
    "SRC3014_03_3013_contract": RESIDUALS / "P8_Y5_R2FR_3013_PARENT_ACTION_CONTRACT.csv",
    "SRC3014_04_3013_blockers": RESIDUALS / "P8_Y5_R2FR_3013_BLOCKER_LEDGER.csv",
    "SRC3014_05_2641_rankzero": LOCAL_BOUNDS / "R10_2641_READOUT_TAIL_AWARE_ZAB_RANKZERO_NONCLAIM.csv",
    "SRC3014_06_2642_source_current_residual": LOCAL_BOUNDS / "R10_2642_RANK_ZERO_SOURCE_CURRENT_RESIDUAL_NONCLAIM.csv",
    "SRC3014_07_2968_rankzero_envelope": LOCAL_BOUNDS / "rank_zero_residual_envelope_2968_NONCLAIM.csv",
    "SRC3014_08_3006_current_sectors": LOCAL_BOUNDS / "Hamiltonian_current_sector_charge_rows_3006_NONCLAIM.csv",
    "SRC3014_09_3007_action_grammar": LOCAL_BOUNDS / "theta_Qtau_feed_rows_3007_NONCLAIM.csv",
    "SRC3014_10_3008_residual_split": LOCAL_BOUNDS / "q_loc_explicit_residual_split_3008_NONCLAIM.csv",
    "SRC3014_11_3009_residual_interface": LOCAL_BOUNDS / "q_loc_coupling_source_ready_residual_interface_3009_NONCLAIM.csv",
    "SRC3014_12_3010_bound_interface": LOCAL_BOUNDS / "q_loc_coupling_bound_interface_3010_NONCLAIM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3014_SOURCE_REGISTER.csv",
    "route_audit": RESIDUALS / "P8_Y5_R2FR_3014_SOURCE_CURRENT_ROUTE_AUDIT.csv",
    "rankzero_gate": RESIDUALS / "P8_Y5_R2FR_3014_RANK_ZERO_CLOSURE_GATE.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_3014_R10_FINITE_RANGE_DEMOTION_LEDGER.csv",
    "closure_envelope": RESIDUALS / "P8_Y5_R2FR_3014_LOCAL_CLOSURE_RESIDUAL_ENVELOPE.csv",
    "ppn_handoff": RESIDUALS / "P8_Y5_R2FR_3014_PPN_HANDOFF_FROM_R10_DEMOTION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3014_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3014_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3014_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3014_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3014_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "route_audit_copy": LOCAL_BOUNDS / "R10_source_current_route_audit_3014_NONCLAIM.csv",
    "demotion_copy": LOCAL_BOUNDS / "R10_finite_range_demoted_to_local_closure_3014_NONCLAIM.csv",
    "closure_copy": LOCAL_BOUNDS / "local_closure_residual_envelope_3014_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3014_PPN_KERNEL_AFTER_R10_SOURCE_MAP_BLOCK_NEXT.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": {
                "SRC3014_00_3013_doc": "previous checkpoint verdict and source-current blocker",
                "SRC3014_01_3013_next": "3014 target definition",
                "SRC3014_02_3013_kernel": "R10 kernel and q_loc bridge contract",
                "SRC3014_03_3013_contract": "parent action clauses still missing",
                "SRC3014_04_3013_blockers": "precise active blockers",
                "SRC3014_05_2641_rankzero": "rank-zero closure normal form",
                "SRC3014_06_2642_source_current_residual": "rank-zero source-current residual envelope",
                "SRC3014_07_2968_rankzero_envelope": "local residual envelope projection rows",
                "SRC3014_08_3006_current_sectors": "Hamiltonian current sector audit",
                "SRC3014_09_3007_action_grammar": "theta/Qtau parent-action grammar",
                "SRC3014_10_3008_residual_split": "explicit q_loc residual split",
                "SRC3014_11_3009_residual_interface": "q_loc/coupling residual interface",
                "SRC3014_12_3010_bound_interface": "q_loc/Delta_K/coupling bound interface",
            }[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

route_audit = [
    base(
        {
            "route_id": "ROUTE3014_0_finite_range_parent_current",
            "route": "derive J_i from a parent finite-range action",
            "candidate_formula": "S_X=1/2 int(Z_AB dX^A dX^B + M_AB X^A X^B) - int J_A X^A; J_i=v_i^A J_A",
            "evidence_found": "3013/2210 give the correct form; no parent-signed Z_AB, M_AB, J_A, v_i or domain certificate is present",
            "status": "ROUTE_BLOCKED_NOT_SIGNED",
            "blocks_claim_because": "lambda_i, K_i and the source charge are not owned by the parent theory",
            "next_if_revived": "source-sign the quadratic X block and current J_A from the parent action",
        }
    ),
    base(
        {
            "route_id": "ROUTE3014_1_inverse_divergence_bridge",
            "route": "derive C_i[I_div^{-1}(q_loc)]",
            "candidate_formula": "J_i=C_i[I_div^{-1}(q_loc)] with domain, boundary conditions, units and no scalar proxy",
            "evidence_found": "3013 writes the bridge contract; no inverse-divergence operator, kernel C_i, or boundary condition is parent-owned",
            "status": "ROUTE_BLOCKED_NOT_SIGNED",
            "blocks_claim_because": "q_loc^nu remains a projected vector/divergence residual, not a scalar Yukawa source",
            "next_if_revived": "derive I_div from the parent elliptic complex or abandon R10 source-map scoring",
        }
    ),
    base(
        {
            "route_id": "ROUTE3014_2_Hamiltonian_Noether_current",
            "route": "derive source current from theta/Qtau/Htau",
            "candidate_formula": "J_tau=theta_MTS(Phi,L_tau Phi)-i_tau L_parent; H_tau=int_S(delta Q_tau-i_tau theta)",
            "evidence_found": "3006/3007 give grammar only; EH core is conditional baseline, total non-EH sectors are not promoted",
            "status": "ROUTE_BLOCKED_GRAMMAR_ONLY",
            "blocks_claim_because": "total MTS Hamiltonian current is not signed across matter, boundary, GK, selector, Pi_M and memory sectors",
            "next_if_revived": "sign each retained non-EH theta/Q_tau piece or keep explicit residuals",
        }
    ),
    base(
        {
            "route_id": "ROUTE3014_3_rank_zero_closure",
            "route": "demote finite-range R10 to local closure residual",
            "candidate_formula": "if Z_AB=0 on the physical quotient then M_AB Z^B=J_H,A+J_NH,A+B_A+J_readout,A+CDB_A+R_projector,A",
            "evidence_found": "2641/2642/2968 provide exact rank-zero source-current residual envelopes, but rank/sign/units and component values are missing",
            "status": "DEMOTION_ROUTE_AVAILABLE_NOT_PROOF",
            "blocks_claim_because": "closure residual can be bounded later, but it is not a Yukawa alpha source and not a local-GR proof yet",
            "next_if_revived": "fill component bounds or theorem-zero rows for the closure envelope",
        }
    ),
    base(
        {
            "route_id": "ROUTE3014_4_acceleration_profile",
            "route": "treat R10 as same-frame acceleration residual only",
            "candidate_formula": "alpha_q(lambda;r)=a_q/a_N exp(r/lambda)/(1+r/lambda)",
            "evidence_found": "2701 supplies the response formula, but q_loc profile/force-density-to-acceleration map/source frame are missing",
            "status": "ROUTE_BLOCKED_PROFILE_MISSING",
            "blocks_claim_because": "no numeric or theorem-zero q_loc profile exists",
            "next_if_revived": "derive q_loc radial acceleration profile from the closure envelope",
        }
    ),
]

rankzero_gate = [
    base(
        {
            "gate_id": "RZG3014_0_rank_certificate",
            "clause": "Z_AB=0 on the strict physical quotient or finite-range X branch absent",
            "current_status": "MISSING_RANK_CERTIFICATE",
            "effect": "cannot claim rank-zero proof",
            "demotion_effect": "finite-range R10 is not live unless future Z_AB/M_AB/J_A are supplied",
        }
    ),
    base(
        {
            "gate_id": "RZG3014_1_algebraic_operator",
            "clause": "M_AB has sign, units and inverse/norm owner on the same quotient domain",
            "current_status": "MISSING_M_AB_SIGN_UNITS_NORM",
            "effect": "closure envelope cannot become numeric",
            "demotion_effect": "rank-zero remains a residual bookkeeping branch",
        }
    ),
    base(
        {
            "gate_id": "RZG3014_2_Hilbert_source",
            "clause": "P_Z[J_H]=0 or universal Hilbert source descent from one source-blind matter action",
            "current_status": "PARTIAL_CONDITIONAL_THEOREM_ONLY",
            "effect": "ordinary matter can still source the eliminated coordinate",
            "demotion_effect": "carry eps_JH_Z_abs in closure envelope",
        }
    ),
    base(
        {
            "gate_id": "RZG3014_3_nonHilbert_boundary_readout",
            "clause": "J_NH, boundary, readout, CDB and observed descent terms are zero or bounded",
            "current_status": "COMPONENT_VALUES_MISSING",
            "effect": "no local-GR/Newton proof",
            "demotion_effect": "carry additive absolute source-current residuals with no cancellation",
        }
    ),
    base(
        {
            "gate_id": "RZG3014_4_R10_projection",
            "clause": "Pi_R10 maps closure residual to alpha/acceleration with source/test normalization",
            "current_status": "MISSING_R10_PROJECTION_VALUES",
            "effect": "R10 cannot score the closure residual",
            "demotion_effect": "R10 remains a blocked diagnostic, not an empirical claim",
        }
    ),
]

demotion = [
    base(
        {
            "demotion_id": "DEM3014_0_live_verdict",
            "object": "R10 finite-range Yukawa source branch",
            "verdict": "DEMOTED_TO_LOCAL_CLOSURE_ONLY",
            "reason": "No parent-signed source-current owner J_i, inverse-divergence map, Z/M eigenmode, source/test charges or tau_R10 exists in the current corpus.",
            "what_survives": "the R10 kernel contract and source acquisition records survive as future-ready nonclaim infrastructure",
            "what_is_forbidden": "no alpha(lambda) pass, no direct q_loc scalar source, no anchor-only curve claim",
        }
    ),
    base(
        {
            "demotion_id": "DEM3014_1_revival_conditions",
            "object": "future R10 revival",
            "verdict": "REVIVABLE_ONLY_WITH_PARENT_INPUTS",
            "reason": "A future parent action may re-open the finite-range branch by supplying Z_AB/M_AB/J_A/v_i or a calibrated acceleration profile.",
            "what_survives": "3013 kernel contract gives the required row shape",
            "what_is_forbidden": "do not use empirical R10 data to define the missing theory coefficients",
        }
    ),
    base(
        {
            "demotion_id": "DEM3014_2_current_work_priority",
            "object": "local GR/Newton programme",
            "verdict": "MOVE_TO_PPN_KERNEL_AFTER_R10_BLOCK",
            "reason": "PPN is the direct local-GR guardrail and does not require pretending q_loc is a scalar Yukawa source.",
            "what_survives": "closure residual envelope can feed a PPN projection kernel",
            "what_is_forbidden": "no PPN pass until source frame, measured-GM convention and response kernels are explicit",
        }
    ),
]

closure_envelope = [
    base(
        {
            "envelope_id": "CENV3014_0_master",
            "quantity": "Delta_rankzero_source_abs_A",
            "formula": "Delta_A <= ||L_A M^-1||*(eps_JH_Z_abs + eps_JNH_abs + eps_B_abs + Delta_readout_abs_A + Q_cdb_abs + eps_projector_abs) + E_DqZ_A",
            "status": "FORMULA_READY_VALUES_MISSING",
            "feeds": "R10_closure; PPN; clocks; WEP; orbital; local_GR",
            "required_next": "M_AB norm/sign/units plus all component zeros or numeric source rows",
        }
    ),
    base(
        {
            "envelope_id": "CENV3014_1_R10_projection",
            "quantity": "alpha_R10_closure_abs",
            "formula": "|alpha_R10| <= Pi_R10[Delta_rankzero_source_abs_A] with no finite-range alpha claim",
            "status": "PROJECTION_VALUES_MISSING",
            "feeds": "R10 diagnostic only",
            "required_next": "Pi_R10 operator, source/test normalization, q_loc acceleration map and valid bound curve",
        }
    ),
    base(
        {
            "envelope_id": "CENV3014_2_PPN_projection",
            "quantity": "PPN_residual_vector_abs",
            "formula": "||delta gamma, delta beta, alpha_i, zeta_i, xi|| <= Pi_PPN[Delta_rankzero_source_abs_A]",
            "status": "PPN_KERNEL_MISSING",
            "feeds": "next local-GR guardrail",
            "required_next": "weak-field response kernel, source frame, measured-GM guard and no-cancellation vector",
        }
    ),
    base(
        {
            "envelope_id": "CENV3014_3_total_no_cancellation",
            "quantity": "local_closure_total_abs",
            "formula": "sum of absolute Hilbert, non-Hilbert, boundary, readout, CDB, projector and observed descent pieces",
            "status": "GUARD_ACTIVE_VALUES_MISSING",
            "feeds": "local_GR/Newton proof discipline",
            "required_next": "each component theorem-zero or source-backed numeric, no cancellation credit",
        }
    ),
]

ppn_handoff = [
    base(
        {
            "handoff_id": "PPN3014_0_reason",
            "ppn_target": "PPN kernel from closure residual",
            "why_now": "R10 finite-range source branch is blocked; PPN is the direct test of whether local GR/Newton recovery survives.",
            "needed_inputs": "K_PPN; weak-field gauge; source frame; measured-GM guard; closure residual vector; comparator rows",
            "status": "NEXT_BEST_ROUTE_NONCLAIM",
        }
    ),
    base(
        {
            "handoff_id": "PPN3014_1_no_shortcut",
            "ppn_target": "fixed measured-GM convention",
            "why_now": "PPN must not hide source-current residuals inside fitted GM or beta/gamma post-calibration.",
            "needed_inputs": "2513 measured-GM no-absorb guard; PPN comparator rows; source normalization",
            "status": "GUARD_REQUIRED",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3014_0_sources_exist",
            "gate": "all cited local source paths exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "3014 only cites current local ledgers",
        }
    ),
    base(
        {
            "gate_id": "GATE3014_1_source_current_owner",
            "gate": "parent source-current owner is signed",
            "result": False,
            "notes": "all live routes are blocked or grammar-only",
        }
    ),
    base(
        {
            "gate_id": "GATE3014_2_rank_zero_proof",
            "gate": "rank-zero closure proof is complete",
            "result": False,
            "notes": "rank certificate and component zero/bound values are missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3014_3_R10_finite_range_live",
            "gate": "R10 finite-range Yukawa alpha branch remains live",
            "result": False,
            "notes": "demoted to local closure only until parent Z/M/J or acceleration profile exists",
        }
    ),
    base(
        {
            "gate_id": "GATE3014_4_no_scalarization",
            "gate": "direct scalarization rho_X := q_loc is forbidden",
            "result": True,
            "notes": "q_loc remains vector/divergence residual unless current owner/inverse divergence map is supplied",
        }
    ),
    base(
        {
            "gate_id": "GATE3014_5_R10_claim",
            "gate": "R10 pass claim allowed",
            "result": False,
            "notes": "source-current owner, rank-zero proof, curve and projection values are missing",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3014_0_status",
            "decision": "The R10 finite-range Yukawa source branch is demoted to local-closure-only for the current corpus.",
            "rationale": "No parent-owned source current or inverse-divergence map exists, and rank-zero closure is not proven; the honest object is an explicit residual envelope.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3014_1_no_failure_claim",
            "decision": "This is not a physics failure of MTS; it is a claim-control decision.",
            "rationale": "The theory can still recover local GR if closure residuals are zero/bounded, but R10 cannot be used as a finite-range alpha claim yet.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3014_2_next_route",
            "decision": "Move to PPN kernel construction from the closure residual envelope.",
            "rationale": "PPN is closer to the central GR/Newton reduction target and avoids the scalar Yukawa source-current trap.",
            "claim_allowed_after_decision": False,
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3014_0_3015",
            "priority": "selected_primary",
            "target_doc": "3015-Y5-R2FR-PPN-kernel-from-local-closure-residual-envelope-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_PPN_kernel_from_local_closure_residual_envelope_under_AX1090_3015.py",
            "mission": "Build the PPN response-kernel contract from the rank-zero/local-closure residual envelope, with fixed measured-GM and no-cancellation guards.",
            "success_condition": "PPN residual vector row exists with required source frame, weak-field gauge, K_PPN placeholders, comparator links and explicit blockers; no PPN/local-GR claim.",
            "fallback_if_fail": "write the missing PPN kernel/source-frame owner as the next blocker and keep closure envelope nonclaim",
            "guardrails": "no PPN pass; no fitted-GM absorption; no hidden cancellation; no formalization-workbench edits; no GitHub action",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["route_audit"], route_audit)
write_csv(OUTPUTS["rankzero_gate"], rankzero_gate)
write_csv(OUTPUTS["demotion"], demotion)
write_csv(OUTPUTS["closure_envelope"], closure_envelope)
write_csv(OUTPUTS["ppn_handoff"], ppn_handoff)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("route_audit_copy", "route_audit"),
    ("demotion_copy", "demotion"),
    ("closure_copy", "closure_envelope"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3014_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_register
    + route_audit
    + rankzero_gate
    + demotion
    + closure_envelope
    + ppn_handoff
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3014_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3014_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3014_02_source_current_not_signed",
        "passed": any(row["gate_id"] == "GATE3014_1_source_current_owner" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "source-current owner remains unsigned",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3014_03_rank_zero_not_claimed",
        "passed": any(row["gate_id"] == "GATE3014_2_rank_zero_proof" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "rank-zero closure is not claimed as proven",
        "evidence": OUTPUTS["rankzero_gate"].name,
    },
    {
        "validation_id": "VAL3014_04_R10_demoted",
        "passed": any(row["verdict"] == "DEMOTED_TO_LOCAL_CLOSURE_ONLY" for row in demotion)
        and any(row["gate_id"] == "GATE3014_3_R10_finite_range_live" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "R10 finite-range branch is demoted, not promoted",
        "evidence": OUTPUTS["demotion"].name,
    },
    {
        "validation_id": "VAL3014_05_no_scalarization",
        "passed": any(row["gate_id"] == "GATE3014_4_no_scalarization" and boolish(row["result"]) for row in promotion_gates),
        "requirement": "direct scalarization of q_loc remains forbidden",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3014_06_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and any(row["gate_id"] == "GATE3014_5_R10_claim" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "R10/local claims remain blocked",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3014_07_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3014 generated ledgers",
    },
    {
        "validation_id": "VAL3014_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3014_09_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3014_10_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3015-Y5-R2FR-PPN-kernel"),
        "requirement": "next target selects PPN kernel from local closure envelope",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3014_99_overall",
        "passed": overall_pass,
        "requirement": "all 3014 validation checks pass",
        "evidence": "aggregate of VAL3014_00 through VAL3014_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3014 — Parent Source-Current Owner for R10 Kernel or Rank-Zero Local Closure under AX1090

Status: `Y5_R2FR_3014_R10_finite_range_demoted_to_local_closure_PPN_next`

## Verdict

3014 does **not** find a parent-signed R10 source-current owner.

The finite-range R10 Yukawa branch is therefore demoted to **local-closure-only** for the current corpus. That is not a defeat of the theory; it is a discipline move. R10 remains useful as a future diagnostic, but it is not allowed to act like a live `alpha(lambda)` prediction until a parent action supplies `Z/M/J`, an inverse-divergence bridge, or a calibrated acceleration profile.

The live object is now the closure residual envelope:

`Delta_A <= ||L_A M^-1||*(eps_JH_Z_abs + eps_JNH_abs + eps_B_abs + Delta_readout_abs_A + Q_cdb_abs + eps_projector_abs) + E_DqZ_A`.

This points us back toward the main goal: local GR/Newton recovery. The next best route is PPN, because PPN tests whether the closure residual can be made small in the weak-field limit without hiding anything inside fitted `GM`.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Source-Current Route Audit

{md_table(route_audit, ["route_id", "route", "status", "blocks_claim_because"])}

## Rank-Zero Closure Gate

{md_table(rankzero_gate, ["gate_id", "clause", "current_status", "demotion_effect"])}

## R10 Demotion Ledger

{md_table(demotion, ["demotion_id", "object", "verdict", "what_is_forbidden"])}

## Local Closure Residual Envelope

{md_table(closure_envelope, ["envelope_id", "quantity", "status", "feeds", "required_next"])}

## PPN Handoff

{md_table(ppn_handoff, ["handoff_id", "ppn_target", "why_now", "status"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["route_audit"]}`
- `{OUTPUTS["rankzero_gate"]}`
- `{OUTPUTS["demotion"]}`
- `{OUTPUTS["closure_envelope"]}`
- `{OUTPUTS["ppn_handoff"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["route_audit_copy"]}`
- `{BRANCH_OUTPUTS["demotion_copy"]}`
- `{BRANCH_OUTPUTS["closure_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No R10 pass claim.
- No rank-zero proof claim.
- No direct scalarization of `q_loc`.
- No fitted-`GM` absorption.
- No hidden-cancellation closure.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
