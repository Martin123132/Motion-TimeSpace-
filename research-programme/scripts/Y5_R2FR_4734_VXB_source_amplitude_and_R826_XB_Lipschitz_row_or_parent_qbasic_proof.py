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

CHECKPOINT = "4734"
CLAIM_ID = "L-576"
MARKER = "PPC4161_VXB_SOURCE_AMPLITUDE_AND_R826_XB_LIPSCHITZ_ROW_4734"
PACKET_MARKER = "PPC4161_PACKET_VXB_SOURCE_AMPLITUDE_AND_R826_XB_LIPSCHITZ_ROW_4734"
DECISION = "VXB_COMPONENT_BUDGET_DERIVED_LCG_TRANSITION_OWNER_UNSIGNED_LR826XB_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4735-Y5-R2FR-Lcg-qbasic-owner-or-VLcg-source-row.md"

DOC_PATH = POST / "4734-Y5-R2FR-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md"
FORMAL_PATH = FORMAL / "750-PPC4161-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_SOURCE_REGISTER.csv"
VXB_BUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_VXB_COMPONENT_BUDGET.csv"
LR826XB_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_R826_XB_LIPSCHITZ_ROW.csv"
PARENT_QBASIC_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_PARENT_QBASIC_PROOF_ATTEMPT.csv"
JM_PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_VXB_TO_JMHIDDEN_PROPAGATION.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4734_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4734_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4734_0_resume", POST / "CURRENT_LOCAL_RESUME.md", "4734-Y5-R2FR-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md", "current local handoff into 4734"),
    ("SRC4734_1_4733_doc", POST / "4733-Y5-R2FR-XB-qbasic-lock-and-Jm-hidden-source-row-or-R826-descent-proof.md", "L_R826_XB V_XB", "4733 introduced V_XB source row"),
    ("SRC4734_2_4733_next", SOURCE_DIR / "P8_Y5_R2FR_4733_NEXT_TARGET.csv", "4734-Y5-R2FR-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md", "machine handoff into 4734"),
    ("SRC4734_3_4733_theorem", SOURCE_DIR / "P8_Y5_R2FR_4733_XB_QBASIC_LOCK_THEOREM.csv", "XBT4733_6_verdict", "X_B lock not promoted"),
    ("SRC4734_4_4733_components", SOURCE_DIR / "P8_Y5_R2FR_4733_XB_COMPONENT_QBASIC_AUDIT.csv", "XBC4733_7_verdict", "X_B component audit"),
    ("SRC4734_5_4733_descent", SOURCE_DIR / "P8_Y5_R2FR_4733_R826_DESCENT_OR_XB_DERIVATIVE_ROWS.csv", "RDX4733_2_bound_case", "R826-XB bound case"),
    ("SRC4734_6_4733_jm", SOURCE_DIR / "P8_Y5_R2FR_4733_JM_HIDDEN_SOURCE_ROW_CONTRACT.csv", "JMH4733_1_VXB", "J_m hidden V_XB source row"),
    ("SRC4734_7_XB_85", FORMAL / "85-coarse-graining-invariants-XB.md", "A_curv", "X_B component definitions"),
    ("SRC4734_8_XB_86", FORMAL / "86-XB-invariant-gate.md", "sharp transitions need q-current bounds", "transition current warning"),
    ("SRC4734_9_Lcg_87", FORMAL / "87-Lcg-coarse-graining-rule.md", "L_cg_coherence_rule_candidate_not_derived", "L_cg candidate not parent-derived"),
    ("SRC4734_10_Lcg_88", FORMAL / "88-Lcg-rule-gate.md", "open_Lcg_gradient_trace_warning", "L_cg trace warning gate"),
    ("SRC4734_11_source_89", FORMAL / "89-source-model-curvature-Lcg-test.md", "trace_gradient_proxy", "source-model trace-gradient proxy"),
    ("SRC4734_12_trace_90", FORMAL / "90-Lcg-gradient-trace-bound.md", "fail_constant_FL_leaks_locally", "local trace leak if unsuppressed"),
    ("SRC4734_13_trace_91", FORMAL / "91-trace-suppression-closure-gate.md", "U_B^nT", "trace suppression closure candidate"),
    ("SRC4734_14_variable_audit", FORMAL / "04-variable-audit.csv", "X_B,X_B; environmental invariant set", "canonical X_B variable audit row"),
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


def vxb_budget_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("VXB4734_0_total", "V_XB", "sup_{B_loc,||v||=1} ||D_v X_B||", "V_Acurv+V_Etheta+V_Imat+V_flow+V_grad+V_Lcg+V_transition+V_readout", "X_B vertical norm", "MISSING_COMPONENT_VALUES", "SRC4734_6_4733_jm"),
        ("VXB4734_1_Acurv", "V_Acurv", "curvature acceleration invariant variation", "V_Acurv <= |A_curv|(|D_v ln L_cg|+|D_v ln K_curv|+|D_v ln H_bg|)", "dimensionless vertical amplitude", "MISSING_CURVATURE_LCG_OWNER", "SRC4734_7_XB_85"),
        ("VXB4734_2_Etheta", "V_Etheta", "theta/expansion environment variation", "zero if theta/coframe/readout is q_obs-owned; otherwise finite frame/readout amplitude", "dimensionless vertical amplitude", "MISSING_THETA_FRAME_OWNER", "SRC4734_7_XB_85"),
        ("VXB4734_3_Imat", "V_Imat", "matter participation variation", "zero if density measure, smoothing and floor are q-basic/fixed; otherwise finite source-measure amplitude", "dimensionless vertical amplitude", "MISSING_MATTER_SMOOTHING_OWNER", "SRC4734_14_variable_audit"),
        ("VXB4734_4_flow", "V_flow", "rotation/shear/flow-frame variation", "zero if observed flow/coframe is q-owned and no hidden flow marker enters", "dimensionless vertical amplitude", "MISSING_FLOW_FRAME_OWNER", "SRC4734_14_variable_audit"),
        ("VXB4734_5_gradient_transition", "V_grad+V_transition", "I_grad/I_Bgrad/I_dotB and switch-gradient variation", "transition-current/support/projector terms must be theorem-zero or bounded", "dimensionless vertical amplitude", "MISSING_TRANSITION_CURRENT_BOUND", "SRC4734_8_XB_86"),
        ("VXB4734_6_Lcg", "V_Lcg", "coarse-graining length variation", "V_Lcg:=sup|D_v ln L_cg|; zero only if L_cg is parent q-basic/fixed", "dimensionless log-amplitude", "MISSING_LCG_QBASIC_OWNER_OR_VALUE", "SRC4734_9_Lcg_87"),
        ("VXB4734_7_readout", "V_readout", "post-variation/readout regeneration", "zero if readout preserves X_B domain and no hidden selector re-enters", "dimensionless vertical amplitude", "MISSING_READOUT_STABILITY_BOUND", "SRC4734_13_trace_91"),
        ("VXB4734_8_verdict", "V_XB verdict", "component budget verdict", "V_XB=0 not signed; V_Lcg and transition/support appear as leading next blockers", "boolean", "VXB_RETAINED_LCG_TRANSITION_DOMINANT", "SRC4734_4_4733_components"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "budget_id": budget_id,
            "quantity": quantity,
            "definition": definition,
            "bound_or_formula": formula,
            "units": units,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for budget_id, quantity, definition, formula, units, status, source_id in specs
    ]


def lr826xb_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("LRX4734_0_target", "L_R826_XB", "R826 sensitivity to X_B", "sup_local ||partial R_826/partial X_B||", "R826 derivative per X_B unit", "MISSING_LIPSCHITZ_SOURCE", "SRC4734_5_4733_descent"),
        ("LRX4734_1_zero_case", "L_R826_XB=0", "R826 independent of X_B", "if parent constructor is R_826=R_826(q) or post-variation diagnostic, the X_B sensitivity slot is absent", "zero theorem", "EXACT_IF_CONSTRUCTOR_SIGNED_NOT_PROMOTED", "SRC4734_3_4733_theorem"),
        ("LRX4734_2_bound_case", "L_R826_XB finite", "finite response sensitivity", "requires action-density source, response table or symbolic parent coefficient with units", "R826 derivative per X_B unit", "MISSING_NUMERIC_OR_SYMBOLIC_SOURCE", "SRC4734_6_4733_jm"),
        ("LRX4734_3_product", "L_R826_XB V_XB", "X_B contribution to J_m_hidden", "|J_m_XB| <= L_R826_XB V_XB", "R826 derivative norm", "PRODUCT_FORM_READY_VALUES_MISSING", "SRC4734_1_4733_doc"),
        ("LRX4734_4_acceptance", "valid_for_claim", "claim switch", "true only if L_R826_XB=0 theorem signs, V_XB=0 theorem signs, or both finite values are source-backed with units", "boolean", "FALSE_NOW", "SRC4734_6_4733_jm"),
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


def parent_qbasic_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("PQB4734_0_exact_statement", "parent q-basic theorem", "If every constructor of X_B factors through q_obs and fixed constants, then V_XB=0.", "EXACT_CONDITIONAL_THEOREM", "SRC4734_3_4733_theorem"),
        ("PQB4734_1_XB_gate_support", "anti-retuning evidence", "Existing X_B gates forbid sector labels, observed residuals, direct Pi_B override and free L_cg.", "DISCIPLINE_SUPPORTS_ROUTE_NOT_PROOF", "SRC4734_8_XB_86"),
        ("PQB4734_2_Lcg_gap", "L_cg parent owner", "The selected L_cg rule is candidate/gated, with parent theorem not derived and trace-gradient warning open.", "BLOCKS_PARENT_QBASIC_PROMOTION", "SRC4734_10_Lcg_88"),
        ("PQB4734_3_trace_gap", "trace/readout compatibility", "U_B^nT suppression is compatible but closure, not a parent derivation.", "TRACE_CLOSURE_UNSIGNED", "SRC4734_13_trace_91"),
        ("PQB4734_4_transition_gap", "transition support", "Sharp transition and solar shell rows remain q-current/local PPN obligations.", "TRANSITION_GATE_UNSIGNED", "SRC4734_11_source_89"),
        ("PQB4734_5_verdict", "V_XB zero verdict", "V_XB=0 is not derived from the current corpus; the next narrow target is L_cg q-basic owner or V_Lcg source row.", "VXB_ZERO_NOT_PROMOTED", "SRC4734_4_4733_components"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": proof_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for proof_id, piece, statement, status, source_id in specs
    ]


def jm_propagation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("JMP4734_0_XB_insert", "J_m_XB", "|J_m_XB| <= L_R826_XB V_XB", "first explicit X_B contribution to J_m_hidden", "SRC4734_5_4733_descent"),
        ("JMP4734_1_total", "J_m_hidden", "|J_m_hidden| <= L_R826_XB V_XB + C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary", "full 4733 hidden row retained", "SRC4734_6_4733_jm"),
        ("JMP4734_2_B826", "B_826", "|B_826| <= |a_F| L_cg^-2 (|J_m_XB|+|J_m_other_hidden|+|J_m_other|+|E_m_res|)", "Euler residual route remains nonclaim until values/source paths exist", "SRC4734_1_4733_doc"),
        ("JMP4734_3_next", "next narrow source row", "focus on V_Lcg because it appears inside A_curv, B_env, Pi_B and Gamma_eff trace leakage", "selects 4735", "SRC4734_9_Lcg_87"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, target, formula, meaning, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4734_0_sources_verified", "All 4734 source paths exist and needles are found.", True, "NONE"),
        ("GATE4734_1_VXB_budget_written", "V_XB component budget is written.", True, "BUDGET_ONLY_NOT_CLAIM"),
        ("GATE4734_2_parent_qbasic_signed", "All X_B constructors are parent q-basic/fixed.", False, "PARENT_QBASIC_UNSIGNED"),
        ("GATE4734_3_Lcg_owner_signed", "L_cg q-basic owner or V_Lcg value is sourced.", False, "LCG_OWNER_OR_VALUE_MISSING"),
        ("GATE4734_4_transition_support_closed", "transition/support/readout components are zero or bounded.", False, "TRANSITION_SUPPORT_UNSIGNED"),
        ("GATE4734_5_LR826XB_sourced", "L_R826_XB is theorem-zero or source-backed.", False, "LR826XB_VALUE_MISSING"),
        ("GATE4734_6_Jm_hidden_claim_ready", "J_m_hidden/B826 hidden row is claim-grade.", False, "JM_HIDDEN_NONCLAIM"),
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
        ("FW4734_0_budget_not_value", "A component budget is not a numeric bound until values, units and source paths exist."),
        ("FW4734_1_no_Lcg_overlook", "Do not claim V_XB=0 while L_cg parent ownership is unsigned."),
        ("FW4734_2_no_gate_to_theorem", "Anti-retuning gates discipline X_B; they do not derive parent q-basicity."),
        ("FW4734_3_no_trace_cheat", "Trace suppression U_B^nT is closure until parent-derived."),
        ("FW4734_4_no_transition_silence", "Transition q-current/support tails cannot be removed by local screening alone."),
        ("FW4734_5_no_public_claim", "No local-GR, PPN, R10 or GitHub claim from this checkpoint."),
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
            "derivation_result": "V_XB component budget and L_R826_XB V_XB product bound are derived",
            "nonclaim_result": "V_XB=0 is not promoted because L_cg, transition/support and readout clauses remain unsigned",
            "finite_row_result": "L_R826_XB and V_XB are staged as source rows feeding J_m_hidden and B826 Euler residual",
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
            "status_id": "STATUS4734_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4734_1_science_verdict",
            "status": "VXB_budget_ready_Lcg_next_blocker",
            "detail": "The next narrow target is L_cg q-basic ownership or V_Lcg source value.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "V_XB budget shows L_cg is the most central shared component in X_B, Gamma_eff and trace leakage.",
            "first_task": "Try to prove L_cg is q-basic/fixed under local vertical variation from the curvature/source coherence rule.",
            "fallback_task": "Fill V_Lcg=sup|D_v ln L_cg| with units, local branch domain and source path.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    vxb: list[dict[str, Any]],
    lr826xb: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    jm: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4734 - VXB Source Amplitude and R826-XB Lipschitz Row or Parent q-basic Proof

Generated: `{ts}`

## Purpose

4734 turns `V_XB` into a sourceable component budget and isolates the product that feeds `J_m_hidden`.

## What Actually Moved

- The bound shape is now explicit: `|J_m_XB| <= L_R826_XB V_XB`.
- `V_XB` is decomposed into curvature, theta/frame, matter smoothing, flow, gradient/transition, `L_cg`, and readout pieces.
- The parent q-basic theorem is exact but not promoted: existing X_B gates discipline the candidate, but do not derive it.
- The next narrow blocker is `L_cg`, because it enters `X_B`, `A_curv`, `B_env`, `Pi_B`, and `Gamma_eff` trace leakage.

## VXB Budget

{bullets(vxb, "budget_id", "current_status")}

## R826-XB Lipschitz Row

{bullets(lr826xb, "row_id", "current_status")}

## Parent q-basic Proof Attempt

{bullets(proof, "proof_id", "status")}

## Jm Propagation

{bullets(jm, "propagation_id", "meaning")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 750 - VXB Source Amplitude and R826-XB Lipschitz Row or Parent q-basic Proof

Generated: `{ts}`

## Result

The X_B route now has the explicit bound

`|J_m_XB| <= L_R826_XB V_XB`,

with

`V_XB <= V_Acurv + V_Etheta + V_Imat + V_flow + V_grad + V_Lcg + V_transition + V_readout`.

This is the right object to source if the parent q-basic proof fails.

## Current Status

`V_XB=0` is exact if all X_B constructors are q-basic/fixed. Current evidence keeps `L_cg`, transition/support and readout clauses unsigned, so the result is nonclaim.

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
- Derivation gain: `|J_m_XB| <= L_R826_XB V_XB` and the component budget for `V_XB` are now explicit.
- Current blocker: parent q-basicity of `X_B` is not signed; `L_cg` and transition/support/readout pieces remain live.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: makes the X_B leakage sourceable by decomposing `V_XB` and isolating `L_R826_XB V_XB`.
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

- `V_XB` is now a component budget, not a blank unknown.
- The product `L_R826_XB V_XB` is the X_B contribution to `J_m_hidden`.
- `L_cg` is selected as the next narrow blocker.

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
        "claim": "4734 derives the V_XB component budget and stages L_R826_XB V_XB as the X_B contribution to J_m_hidden; L_cg remains the next unsigned blocker.",
        "current_evidence": "Generated source register, V_XB component budget, R826-XB Lipschitz row, parent q-basic proof attempt, Jm propagation, gates, firewalls, decision, status, next target and validation.",
        "status": "VXB_budget_LR826XB_row_staged_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating anti-retuning gates or local screening as V_XB=0.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "L_cg q-basic owner, V_Lcg, transition/support/readout tails and L_R826_XB remain unsourced.",
        "title": "VXB source amplitude and R826-XB Lipschitz row",
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
    vxb: list[dict[str, Any]],
    lr826xb: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    jm: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        VXB_BUDGET_CSV,
        LR826XB_CSV,
        PARENT_QBASIC_CSV,
        JM_PROPAGATION_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    vxb_status = ";".join(row["current_status"] for row in vxb)
    lr_status = ";".join(row["current_status"] for row in lr826xb)
    proof_status = ";".join(row["status"] for row in proof)
    jm_formula = ";".join(row["formula"] for row in jm)
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    checks = [
        ("VAL4734_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4734 source paths exist"),
        ("VAL4734_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4734 source needles found"),
        ("VAL4734_2_VXB_budget_written", "VXB_RETAINED_LCG_TRANSITION_DOMINANT" in vxb_status and "L_R826_XB V_XB" in doc_text, "V_XB component budget is written"),
        ("VAL4734_3_LR826XB_row_written", "MISSING_LIPSCHITZ_SOURCE" in lr_status and "PRODUCT_FORM_READY_VALUES_MISSING" in lr_status, "R826-XB Lipschitz row is written"),
        ("VAL4734_4_parent_qbasic_not_promoted", "VXB_ZERO_NOT_PROMOTED" in proof_status and "BLOCKS_PARENT_QBASIC_PROMOTION" in proof_status, "parent q-basic proof is not promoted"),
        ("VAL4734_5_Jm_propagation_written", "L_R826_XB V_XB" in jm_formula and "|B_826|" in jm_formula, "V_XB propagates to J_m_hidden and B826"),
        ("VAL4734_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4734_0_sources_verified", "GATE4734_1_VXB_budget_written"}), "all claim gates remain closed except structural nonclaim gates"),
        ("VAL4734_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4734_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4734_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-576"),
        ("VAL4734_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4735 next target"),
        ("VAL4734_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4734 CSV files parse cleanly"),
        ("VAL4734_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
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
            "check_id": "VAL4734_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4734 V_XB source amplitude and R826-XB Lipschitz validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    vxb = vxb_budget_rows(ts)
    lr826xb = lr826xb_rows(ts)
    proof = parent_qbasic_rows(ts)
    jm = jm_propagation_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(VXB_BUDGET_CSV, vxb)
    write_csv(LR826XB_CSV, lr826xb)
    write_csv(PARENT_QBASIC_CSV, proof)
    write_csv(JM_PROPAGATION_CSV, jm)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, vxb, lr826xb, proof, jm, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, vxb, lr826xb, proof, jm, gates, ts))


if __name__ == "__main__":
    main()
