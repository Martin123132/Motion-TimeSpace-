from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4733"
CLAIM_ID = "L-575"
MARKER = "PPC4161_XB_QBASIC_LOCK_AND_JM_HIDDEN_SOURCE_ROW_4733"
PACKET_MARKER = "PPC4161_PACKET_XB_QBASIC_LOCK_AND_JM_HIDDEN_SOURCE_ROW_4733"
DECISION = "XB_QBASIC_R826_DESCENT_EXACT_CONDITIONAL_XB_PARENT_LOCK_UNSIGNED_VXB_JMHIDDEN_SOURCE_ROW_CREATED_NONCLAIM"
NEXT_TARGET = "4734-Y5-R2FR-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md"

DOC_PATH = POST / "4733-Y5-R2FR-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md"
FORMAL_PATH = FORMAL / "749-PPC4161-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_SOURCE_REGISTER.csv"
XB_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_XB_QBASIC_LOCK_THEOREM.csv"
XB_COMPONENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_XB_COMPONENT_QBASIC_AUDIT.csv"
R826_DESCENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_R826_DESCENT_OR_XB_DERIVATIVE_ROWS.csv"
JM_HIDDEN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_JM_HIDDEN_SOURCE_ROW_CONTRACT.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4733_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4733_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4733_0_resume", POST / "CURRENT_LOCAL_RESUME.md", "4733-Y5-R2FR-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md", "current local handoff into 4733"),
    ("SRC4733_1_4732_doc", POST / "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md", "`X_B` q-basic lock", "4732 handoff names X_B q-basic lock"),
    ("SRC4733_2_4732_next", SOURCE_DIR / "P8_Y5_R2FR_4732_NEXT_TARGET.csv", "4733-Y5-R2FR-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md", "machine handoff into 4733"),
    ("SRC4733_3_4732_gate", SOURCE_DIR / "P8_Y5_R2FR_4732_R826_CONSTRUCTOR_LIST_GATE.csv", "CLG4732_1_XB_lock", "X_B q-basic lock gate"),
    ("SRC4733_4_4732_translation", SOURCE_DIR / "P8_Y5_R2FR_4732_EULER_RESIDUAL_TO_HHIDDEN_TRANSLATION.csv", "EHT4732_2_descent_zero", "R826 descent zero route"),
    ("SRC4733_5_4732_contract", SOURCE_DIR / "P8_Y5_R2FR_4732_CI826_VI_SOURCE_ROW_CONTRACT.csv", "CIVI4732_1_XB", "source row contract for X_B lock"),
    ("SRC4733_6_XB_85", FORMAL / "85-coarse-graining-invariants-XB.md", "X_B = {", "candidate X_B bundle definition"),
    ("SRC4733_7_XB_86", FORMAL / "86-XB-invariant-gate.md", "complete_XB_invariant_gate_first_results", "X_B invariant anti-retuning gate"),
    ("SRC4733_8_XB_summary", FORMAL / "runs" / "XB_invariant_gate_20260527-204233" / "summary.csv", "local_screening_target_conditional_pass", "X_B gate summary"),
    ("SRC4733_9_Lcg_87", FORMAL / "87-Lcg-coarse-graining-rule.md", "L_cg_coherence_rule_candidate_not_derived", "L_cg candidate not parent-derived"),
    ("SRC4733_10_Lcg_88", FORMAL / "88-Lcg-rule-gate.md", "complete_Lcg_rule_gate_first_results", "L_cg gate"),
    ("SRC4733_11_source_89", FORMAL / "89-source-model-curvature-Lcg-test.md", "trace_gradient_proxy", "source-model L_cg trace warning"),
    ("SRC4733_12_trace_90", FORMAL / "90-Lcg-gradient-trace-bound.md", "complete_Lcg_gradient_trace_bound_first_results", "Lcg-gradient trace bound"),
    ("SRC4733_13_trace_91", FORMAL / "91-trace-suppression-closure-gate.md", "complete_trace_suppression_closure_gate_first_results", "trace suppression closure gate"),
    ("SRC4733_14_variable_audit", FORMAL / "04-variable-audit.csv", "X_B,X_B; environmental invariant set", "canonical X_B variable audit row"),
    ("SRC4733_15_4673_slot", SOURCE_DIR / "P8_Y5_R2FR_4673_R826_SLOT_OWNER_AUDIT.csv", "R8264673_1_XB_qbasic", "older R826 owner audit naming X_B lock"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def xb_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("XBT4733_0_target", "X_B q-basic lock", "Prove D_v X_B=0 for v in ker(Dq_obs) on the local branch.", "This is the missing guard for R826 descent.", "TARGET_SHARP", "SRC4733_3_4732_gate"),
        ("XBT4733_1_exact_chain_rule", "R826 q-descent law", "If R_826=Rbar_826(q_obs,X_B) and v is vertical, then D_v R_826 = (partial_XB Rbar_826) D_v X_B.", "So R826 descends iff X_B is q-basic/fixed or the XB derivative coefficient is zero.", "EXACT_DERIVED_CHAIN_RULE", "SRC4733_4_4732_translation"),
        ("XBT4733_2_qbasic_sufficient_clause", "sufficient zero theorem", "If every component of X_B is a scalar functional of q_obs, fixed representation data and a parent-owned L_cg(q_obs), then D_v X_B=0.", "Then J_m_hidden=0, C_I826=0 for the X_B route, and B826 has no hidden value-source slot.", "EXACT_IF_PARENT_QBASIC", "SRC4733_6_XB_85"),
        ("XBT4733_3_current_evidence", "current X_B status", "X_B is a universal candidate bundle with anti-retuning gates and source-model tests.", "It is disciplined and testable, but not parent-derived as q-basic.", "CANDIDATE_GATE_TESTED_NOT_PARENT_DERIVED", "SRC4733_7_XB_86"),
        ("XBT4733_4_Lcg_gap", "L_cg dependency", "X_B includes L_cg and curvature/source coherence ingredients; current L_cg rule is candidate and trace-gradient constrained.", "Without parent L_cg q-basic ownership, D_v X_B can survive through L_cg or support/readout choices.", "LCG_QBASIC_UNSIGNED", "SRC4733_10_Lcg_88"),
        ("XBT4733_5_transition_gap", "transition/source support", "Sharp transition rows are quarantined and source-current gates remain required.", "Local screening direction is supported, but transition q-current silence is not proven.", "TRANSITION_QCURRENT_UNSIGNED", "SRC4733_8_XB_summary"),
        ("XBT4733_6_verdict", "X_B lock verdict", "D_v X_B=0 is an exact conditional theorem, but present evidence does not sign the parent q-basic lock.", "Do not claim R826 descent; build V_XB/J_m_hidden source row.", "XB_LOCK_NOT_PROMOTED_SOURCE_ROW_REQUIRED", "SRC4733_15_4673_slot"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "effect": effect,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, effect, status, source_id in specs
    ]


def xb_component_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("XBC4733_0_A_curv", "A_curv", "curvature/acceleration invariant", "q-basic if curvature norms and L_cg are q_obs-owned", "LCG_AND_CURVATURE_OWNER_UNSIGNED", "SRC4733_6_XB_85"),
        ("XBC4733_1_E_theta", "E_theta", "expansion/shear/theta environment invariant", "q-basic if theta/readout frame is observed/fixed", "THETA_FRAME_OWNER_UNSIGNED", "SRC4733_6_XB_85"),
        ("XBC4733_2_I_mat", "I_mat", "matter participation invariant", "q-basic if density smoothing/floor/source measure is parent-owned", "MATTER_SMOOTHING_FLOOR_UNSIGNED", "SRC4733_14_variable_audit"),
        ("XBC4733_3_I_rot_shear", "I_rot/I_shear", "kinematic structure invariants", "q-basic if computed from observed coframe/flow without sector labels", "FLOW_FRAME_OWNER_UNSIGNED", "SRC4733_14_variable_audit"),
        ("XBC4733_4_I_grad_Bgrad_dotB", "I_grad/I_Bgrad/I_dotB", "gradient and switch-gradient invariants", "q-basic if differentiable support/projector/current gates are signed", "TRANSITION_GRADIENT_GATE_UNSIGNED", "SRC4733_7_XB_86"),
        ("XBC4733_5_Lcg", "L_cg H_bg/c", "coarse-graining scale part of X_B", "q-basic only if L_cg rule is parent-derived or explicitly q_obs-owned", "LCG_PARENT_THEOREM_NOT_DERIVED", "SRC4733_9_Lcg_87"),
        ("XBC4733_6_trace_suppression", "U_B^nT closure", "trace-suppression compatibility law", "helps local trace leakage but remains closure, not a derivation of X_B q-basicity", "TRACE_CLOSURE_NOT_PARENT_DERIVED", "SRC4733_13_trace_91"),
        ("XBC4733_7_verdict", "X_B total", "component audit verdict", "every component has a clear q-basic route, but at least one owner/signature remains unsigned", "V_XB_RETAINED", "SRC4733_11_source_89"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "role": role,
            "qbasic_condition": condition,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for component_id, component, role, condition, status, source_id in specs
    ]


def r826_descent_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("RDX4733_0_descent_formula", "R826 descent derivative", "D_v R_826 = R_q[D_v q] + R_XB[D_v X_B]", "for vertical v, D_v q=0, so D_v R_826 = R_XB[D_v X_B]", "EXACT_CHAIN_RULE", "SRC4733_4_4732_translation"),
        ("RDX4733_1_zero_case", "descent zero", "D_v X_B=0 => D_v R_826=0", "kills J_m_hidden from the X_B route and removes the C_I826/V_XB piece", "EXACT_IF_XB_LOCK_SIGNED", "SRC4733_3_4732_gate"),
        ("RDX4733_2_bound_case", "descent bound", "|D_v R_826| <= L_R826_XB V_XB + C_I826 V_I + H_grad + H_marker + H_rad + H_boundary", "first bound row if X_B lock or no-hidden-target proof fails", "BOUND_FORMULA_DERIVED_VALUES_MISSING", "SRC4733_5_4732_contract"),
        ("RDX4733_3_euler_insert", "Euler residual insert", "|J_m_hidden| <= L_R826_XB V_XB + C_I826 V_I + H_grad + H_marker + H_rad + H_boundary", "feeds the 4674 B826 Euler residual identity", "JM_HIDDEN_INSERT_WRITTEN", "SRC4733_4_4732_translation"),
        ("RDX4733_4_B826_insert", "B826 insert", "|B_826| <= |a_F| L_cg^-2 (|J_m_hidden|+|J_m_other|+|E_m_res|)", "does not claim total Bmem silence", "B826_BOUND_INSERT_NONCLAIM", "SRC4733_5_4732_contract"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "descent_id": descent_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for descent_id, target, formula, meaning, status, source_id in specs
    ]


def jm_hidden_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("JMH4733_0_master", "J_m_hidden", "hidden/XB branch-force residual", "L_R826_XB V_XB + C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary", "R826 derivative / branch-force norm", "MISSING_COMPONENT_VALUES", "SRC4733_5_4732_contract"),
        ("JMH4733_1_VXB", "V_XB", "vertical amplitude of X_B", "sup_{B_loc,||v||=1}|D_v X_B|", "X_B vertical unit", "MISSING_VXB_ZERO_OR_VALUE", "SRC4733_3_4732_gate"),
        ("JMH4733_2_LR826XB", "L_R826_XB", "R826 Lipschitz/sensitivity to X_B", "sup||partial R_826/partial X_B||", "R826 derivative per X_B unit", "MISSING_LR826XB_VALUE", "SRC4733_4_4732_translation"),
        ("JMH4733_3_CI826_VI", "C_I826 V_I", "direct hidden scalar value slot", "sup|partial Coeff_R826/partial I_hid| * sup|D_v I_hid|", "R826 derivative norm", "MISSING_CI826_OR_VI_VALUE", "SRC4733_5_4732_contract"),
        ("JMH4733_4_transition_tail", "H_transition_XB", "source/support/projector transition tail", "gradient/support/readout/domain terms from X_B components", "R826 derivative norm", "MISSING_TRANSITION_TAIL_BOUND", "SRC4733_8_XB_summary"),
        ("JMH4733_5_units_domain", "units_and_domain", "local branch domain and normalization", "B_loc; X_B normalization; L_cg rule; hidden scalar units; source paths", "provenance contract", "MISSING_UNITS_DOMAIN_SOURCE_PATHS", "SRC4733_14_variable_audit"),
        ("JMH4733_6_acceptance", "valid_for_claim", "claim switch", "true only if X_B q-basic proof signs or all J_m_hidden components are source-backed with units", "boolean", "FALSE_NOW", "SRC4733_5_4732_contract"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "role": role,
            "formula": formula,
            "units": units,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, quantity, role, formula, units, status, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4733_0_sources_verified", "All 4733 source paths exist and needles are found.", True, "NONE"),
        ("GATE4733_1_chain_rule_derived", "R826-XB descent derivative law is written.", True, "STRUCTURE_ONLY_NOT_CLAIM"),
        ("GATE4733_2_XB_parent_qbasic_signed", "X_B is parent-signed q-basic/fixed on the local branch.", False, "XB_PARENT_LOCK_UNSIGNED"),
        ("GATE4733_3_Lcg_parent_owned", "L_cg inside X_B is parent-owned q-basic/fixed.", False, "LCG_PARENT_THEOREM_MISSING"),
        ("GATE4733_4_transition_current_closed", "transition/support/q-current tails are zero or bounded.", False, "TRANSITION_CURRENT_UNSIGNED"),
        ("GATE4733_5_Jm_hidden_sourced", "J_m_hidden components have source-backed values or theorem-zero rows.", False, "JMHIDDEN_VALUES_MISSING"),
        ("GATE4733_6_B826_claim_ready", "R826 descent or Euler residual bound is claim-grade.", False, "B826_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4733_0_candidate_not_qbasic", "A disciplined X_B candidate is not a proof that D_v X_B=0."),
        ("FW4733_1_no_local_screening_to_descent", "Pi_B near one in a toy local row does not prove R826 descends."),
        ("FW4733_2_no_Lcg_silence", "Variable L_cg can carry vertical leakage unless parent-owned or bounded."),
        ("FW4733_3_no_transition_hide", "Solar/transition shells remain local PPN/q-current obligations."),
        ("FW4733_4_no_unit_rescale", "Do not shrink V_XB or C_I826 by changing X_B normalization after the fact."),
        ("FW4733_5_no_single_component_victory", "J_m_hidden/B826 is one branch; Bmem_eff and local-GR gates remain broader."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "D_v R_826(q;X_B)=R_XB D_v X_B is derived; X_B q-basicity would close the descent route exactly",
            "nonclaim_result": "X_B is gate-tested but not parent-signed q-basic because L_cg, transition/support and source-current clauses remain unsigned",
            "finite_row_result": "J_m_hidden bound row now includes L_R826_XB V_XB plus hidden scalar/gradient/marker/readout/boundary components",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4733_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4733_1_science_verdict",
            "status": "XB_qbasic_descent_exact_conditional_VXB_Jmhidden_source_row_created",
            "detail": "The proof target is now V_XB=0 or a source-backed V_XB/L_R826_XB row.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4733 reduces R826 descent to V_XB=0 or a finite L_R826_XB V_XB row.",
            "first_task": "Try to prove V_XB=0 from parent q-basic ownership of X_B components, especially L_cg and transition/support inputs.",
            "fallback_task": "Fill L_R826_XB and V_XB with units, branch domain and source paths so J_m_hidden can be bounded.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    theorem: list[dict[str, Any]],
    components: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    jm_hidden: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4733 - XB q-basic Lock and Jm Hidden Source Row or R826 Descent Proof

Generated: `{ts}`

## Purpose

4733 attacks the narrow proof left by 4732: if `X_B` is fixed/q-basic, then `R_826(q;X_B)` descends and the hidden branch force disappears.

## What Actually Moved

- The exact descent law is now explicit: for vertical `v`, `D_v R_826(q;X_B)=R_826,XB D_v X_B`.
- Therefore `R_826` descent is exact if `D_v X_B=0`.
- Existing `X_B` work gives a disciplined, anti-retuning candidate bundle, but not a parent q-basic theorem.
- The fallback is now sharper: `|J_m_hidden| <= L_R826_XB V_XB + C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary`.

## X_B Lock Theorem

{bullets(theorem, "theorem_id", "status")}

## X_B Component Audit

{bullets(components, "component_id", "current_status")}

## R826 Descent Rows

{bullets(descent, "descent_id", "status")}

## Jm Hidden Source Row

{bullets(jm_hidden, "row_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 749 - XB q-basic Lock and Jm Hidden Source Row or R826 Descent Proof

Generated: `{ts}`

## Result

For the q-descent constructor candidate,

`R_826 = Rbar_826(q_obs, X_B)`,

and local vertical `v in ker(Dq_obs)`,

`D_v R_826 = R_826,XB D_v X_B`.

So `R_826` descends only if `D_v X_B=0`, or if the `X_B` sensitivity vanishes.

## Current Status

The existing `X_B` programme supplies a universal candidate bundle and anti-retuning gates, but not a parent q-basic theorem. `L_cg`, transition support, source-current and readout/projector clauses remain unsigned.

## Fallback Contract

`|J_m_hidden| <= L_R826_XB V_XB + C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary`.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: `D_v R_826(q;X_B)=R_826,XB D_v X_B` is the exact descent law for the q-basic constructor branch.
- Current blocker: `X_B` is gate-tested but not parent-signed q-basic; `L_cg`, transition/support and q-current clauses remain unsigned.
- Finite row: `J_m_hidden` now has a source-row contract with `L_R826_XB V_XB` plus hidden scalar/gradient/marker/readout/boundary components.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: reduces R826 q-descent to the single measurable/provable object `V_XB=sup|D_v X_B|`, then inserts it into `J_m_hidden`.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- R826 q-descent is now reduced exactly to `D_v X_B=0`.
- X_B remains gate-tested but not parent-signed q-basic.
- The fallback is now a concrete `J_m_hidden` row with `L_R826_XB V_XB`.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4733 derives the R826-XB descent law and creates the V_XB/J_m_hidden source-row contract; X_B q-basicity remains unsigned, so no local-GR claim is made.",
        "current_evidence": "Generated source register, X_B theorem rows, X_B component audit, R826 descent rows, J_m_hidden source contract, gates, firewalls, decision, status, next target and validation.",
        "status": "XB_qbasic_descent_exact_conditional_Jmhidden_row_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the X_B candidate/gate as a parent q-basic theorem.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "V_XB, L_R826_XB, L_cg q-basicity, transition-current and source/support clauses remain unsourced.",
        "title": "XB q-basic lock and Jm hidden source row or R826 descent proof",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    components: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    jm_hidden: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        XB_THEOREM_CSV,
        XB_COMPONENT_AUDIT_CSV,
        R826_DESCENT_CSV,
        JM_HIDDEN_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    theorem_status = ";".join(row["status"] for row in theorem)
    component_status = ";".join(row["current_status"] for row in components)
    descent_status = ";".join(row["status"] for row in descent)
    jm_status = ";".join(row["current_status"] for row in jm_hidden)
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    checks = [
        ("VAL4733_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4733 source paths exist"),
        ("VAL4733_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4733 source needles found"),
        ("VAL4733_2_chain_rule_written", "EXACT_DERIVED_CHAIN_RULE" in theorem_status and "D_v R_826(q;X_B)" in doc_text, "R826-XB descent chain rule is written"),
        ("VAL4733_3_XB_not_promoted", "XB_LOCK_NOT_PROMOTED_SOURCE_ROW_REQUIRED" in theorem_status and "V_XB_RETAINED" in component_status, "X_B q-basic lock is not promoted"),
        ("VAL4733_4_descent_bound_written", "BOUND_FORMULA_DERIVED_VALUES_MISSING" in descent_status and "JM_HIDDEN_INSERT_WRITTEN" in descent_status, "descent bound and Jm insert are written"),
        ("VAL4733_5_Jmhidden_contract_created", "MISSING_VXB_ZERO_OR_VALUE" in jm_status and "MISSING_LR826XB_VALUE" in jm_status, "J_m_hidden source contract includes V_XB and L_R826_XB"),
        ("VAL4733_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4733_0_sources_verified", "GATE4733_1_chain_rule_derived"}), "all claim gates remain closed except structural nonclaim gates"),
        ("VAL4733_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4733_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4733_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-575"),
        ("VAL4733_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4734 next target"),
        ("VAL4733_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4733 CSV files parse cleanly"),
        ("VAL4733_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4733_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4733 X_B q-basic lock and J_m_hidden source-row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    theorem = xb_theorem_rows(ts)
    components = xb_component_rows(ts)
    descent = r826_descent_rows(ts)
    jm_hidden = jm_hidden_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(XB_THEOREM_CSV, theorem)
    write_csv(XB_COMPONENT_AUDIT_CSV, components)
    write_csv(R826_DESCENT_CSV, descent)
    write_csv(JM_HIDDEN_CSV, jm_hidden)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, components, descent, jm_hidden, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, components, descent, jm_hidden, gates, ts))


if __name__ == "__main__":
    main()
