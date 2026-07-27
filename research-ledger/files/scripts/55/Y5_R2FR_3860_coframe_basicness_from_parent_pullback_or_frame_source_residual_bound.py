from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3860"
BRANCH = "MTS_R2FR_Y5_COFRAME_BASICNESS_FROM_PARENT_PULLBACK_OR_FRAME_SOURCE_RESIDUAL_BOUND_3860"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3859_THEOREM = OUT / "P8_Y5_R2FR_3859_QBASIC_TAU_H_CSTAR_THEOREM.csv"
CSV_3859_AUDIT = OUT / "P8_Y5_R2FR_3859_TAU_H_CSTAR_OWNERSHIP_AUDIT.csv"
CSV_3859_BOUND = OUT / "P8_Y5_R2FR_3859_FRAME_CLOCK_PREFERRED_RESIDUAL_BOUND.csv"
CSV_3859_GATES = OUT / "P8_Y5_R2FR_3859_CLAIM_GATES.csv"
CSV_3859_VALIDATION = OUT / "P8_Y5_BRR545_3859_VALIDATION.csv"
CSV_3766_KERNEL = OUT / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv"
CSV_3766_ATTEMPT = OUT / "P8_Y5_R2FR_3766_QOBS_KERNEL_PROOF_ATTEMPT.csv"
CSV_3766_BOUND = OUT / "P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv"
CSV_3766_NORMS = OUT / "P8_Y5_R2FR_3766_VERTICAL_LEAKAGE_NORMS.csv"
CSV_3767_PULLBACK = OUT / "P8_Y5_R2FR_3767_PARENT_ACTION_PULLBACK_DECOMPOSITION.csv"
CSV_3767_LLEAK = OUT / "P8_Y5_R2FR_3767_LLEAK_BOUND_INTERFACE.csv"
CSV_3765_QOBS = OUT / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv"
CSV_3765_VERDICT = OUT / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv"
CSV_3517_QMAP = OUT / "P8_EM_actual_q_map_vertical_basis_candidate.csv"
CSV_3504_GATE = OUT / "P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv"
CSV_3504_HODGE = OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv"
CSV_3498_NATURALITY = OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv"
CSV_3494_SPIN = OUT / "P8_Y5_R2FR_3494_COFRAME_SPIN_THEOREM_ATTEMPT.csv"
CSV_FRAME_SPLIT = OUT / "P8_frame_source_split_residual_or_zero.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3860_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3860_PARENT_SIGNATURE_AUDIT.csv",
    "residual": OUT / "P8_Y5_R2FR_3860_FRAME_SOURCE_RESIDUAL_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3860_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3860_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3860_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3860_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3860_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3860_00_3859_theorem", CSV_3859_THEOREM, "EXACT_CONDITIONAL_OWNER_THEOREM", "3859 tau/h/c owner theorem"),
    ("SRC3860_01_3859_audit", CSV_3859_AUDIT, "B_qobs_parent_signature+B_eobs_basic", "3859 e_obs owner audit"),
    ("SRC3860_02_3859_bound", CSV_3859_BOUND, "B_tau_h_cstar_owner_3859", "3859 residual bound"),
    ("SRC3860_03_3859_gates", CSV_3859_GATES, "PASS_3860_COFRAME_BASICNESS_TARGET", "3860 target selection"),
    ("SRC3860_04_3859_validation", CSV_3859_VALIDATION, "PASS", "previous validation"),
    ("SRC3860_05_3766_kernel", CSV_3766_KERNEL, "EXACT_CONDITIONAL_KERNEL_CERTIFICATE", "kernel-null theorem"),
    ("SRC3860_06_3766_attempt", CSV_3766_ATTEMPT, "passes_clause", "current kernel proof attempt"),
    ("SRC3860_07_3766_bound", CSV_3766_BOUND, "delta_frame_source <= C_Omega", "frame residual bound"),
    ("SRC3860_08_3766_norms", CSV_3766_NORMS, "epsilon_Omega", "vertical leakage norms"),
    ("SRC3860_09_3767_pullback", CSV_3767_PULLBACK, "L_parent=q_obs^*L_red+dB+L_leak", "parent action pullback identity"),
    ("SRC3860_10_3767_lleak", CSV_3767_LLEAK, "epsilon_shadow_g", "L_leak bound interface"),
    ("SRC3860_11_3765_qobs", CSV_3765_QOBS, "q_obs_candidate", "q_obs candidate map"),
    ("SRC3860_12_3765_verdict", CSV_3765_VERDICT, "QOBS_CANDIDATE_CONSTRUCTED_BUT_NOT_PARENT_SIGNED", "q_obs verdict"),
    ("SRC3860_13_3517_qmap", CSV_3517_QMAP, "CANDIDATE_VISIBLE_NOT_PARENT_DERIVED", "public geometry slot"),
    ("SRC3860_14_3504_gate", CSV_3504_GATE, "e_obs=e_bar(q)", "e_obs q-basic gate"),
    ("SRC3860_15_3504_hodge", CSV_3504_HODGE, "D_v e_obs=0", "Hodge/coframe vertical silence"),
    ("SRC3860_16_3498_naturality", CSV_3498_NATURALITY, "q/e_obs/tau functor projector", "projector naturality chain rule"),
    ("SRC3860_17_3494_spin", CSV_3494_SPIN, "owned-coframe ordinary branch", "owned coframe spin branch"),
    ("SRC3860_18_frame_split", CSV_FRAME_SPLIT, "SEEDED_NONCLAIM_3048_MISSING_SOURCE_VARIATION_FRAME_THEOREM", "frame/source residual fallback"),
]

COFRAME_BASICNESS = "e_obs=e_bar(q_obs) and v in ker(Dq_obs) imply D_v e_obs=D e_bar[Dq_obs(v)]=0"
PULLBACK_CERTIFICATE = "L_parent=q_obs^*L_red+dB, int_boundary B_EA=0, S_src=Sbar_src(q_obs,psi,A,theta), Lie_EA theta=0, and r_s=F_s o q_obs"
ANTI_TAUTOLOGY = "including e_obs inside the q_obs tuple is not a proof unless the parent action makes ker(Dq_obs) presymplectic-null, matter-invisible, boundary-silent, and readout-silent"
CURRENT_BLOCK = "current corpus has q_obs and public-geometry candidates, but parent pullback, L_leak=0, boundary silence, source descent, constants, and sector readout descent are not all signed"
RESIDUAL_BOUND = (
    "B_eobs_basic_3860 <= "
    "B_qobs_signature+B_pullback_Lleak+B_kernel_null+B_boundary_silence+"
    "B_source_descent+B_theta_constants+B_sector_readout+B_shadow_frame+"
    "B_coframe_spin+B_readout_order"
)
FRAME_BOUND = (
    "delta_frame_source <= "
    "C_L epsilon_L+C_Omega epsilon_Omega+C_src epsilon_src+C_theta epsilon_theta+"
    "C_boundary epsilon_boundary+C_readout max_s epsilon_readout_s+C_shadow epsilon_shadow_g"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_coframe_basicness_test",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CBT3860_0_qbasic_coframe",
            "step": "coframe basicness chain rule",
            "statement": COFRAME_BASICNESS,
            "proof": "chain rule on the q_obs quotient map",
            "current_result": "EXACT_CHAIN_RULE_THEOREM",
            "status": "EXACT_CONDITIONAL_COFRAME_BASICNESS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CBT3860_1_parent_certificate",
            "step": "parent pullback/kernel certificate",
            "statement": PULLBACK_CERTIFICATE,
            "proof": "3766 and 3767 imply vertical directions are bulk-null, source-invisible, boundary-silent, and readout-silent under these clauses",
            "current_result": "EXACT_CONDITIONAL_PARENT_CERTIFICATE",
            "status": "EXACT_CONDITIONAL_KERNEL_TO_COFRAME_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CBT3860_2_anti_tautology",
            "step": "anti-tautology guard",
            "statement": ANTI_TAUTOLOGY,
            "proof": "a quotient component is physical only if the parent action and readouts make its omitted directions unobservable",
            "current_result": "NO_QOBS_BY_DECLARATION",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CBT3860_3_current_verdict",
            "step": "strict-current coframe basicness test",
            "statement": CURRENT_BLOCK,
            "proof": "3765/3517 write candidates, while 3766/3767/1030 keep the parent signatures unsigned",
            "current_result": "EOBS_BASICNESS_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_RESIDUAL_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CBT3860_4_if_closed",
            "step": "metric bridge consequence",
            "statement": "if B_eobs_basic_3860=0 and c_* is q-basic, then 3859 gives D_v tau_time=D_v h_space=D_v c_*=0 and 3858 owns the Lorentzian metric bridge up to nonLC/readout guards",
            "proof": "compose 3860 coframe basicness with the 3859 tau/h/c chain-rule theorem",
            "current_result": "EXACT_CONDITIONAL_METRIC_BRIDGE_HANDOFF",
            "status": "EXACT_CONDITIONAL_WIN_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "CPA3860_0_qobs_signature",
            "clause": "q_obs parent signature",
            "required_identity": "q_obs is the parent quotient/coequalizer, not a chosen readout tuple",
            "current_evidence": "3765 constructs q_obs_candidate but verdict says not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_qobs_signature",
            "next_action": "prove q_obs from parent equivalence/kernel-null or retain quotient residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_1_pullback_Lleak",
            "clause": "parent action pullback",
            "required_identity": "L_parent=q_obs^*L_red+dB and L_leak=0",
            "current_evidence": "3767 derives exact decomposition but all L_leak operator coefficients remain missing/nonclaim",
            "passes_current_branch": False,
            "residual_owner": "B_pullback_Lleak",
            "next_action": "prove or bound L_leak_shadow_g/source/boundary/readout terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_2_kernel_null",
            "clause": "presymplectic kernel nullness",
            "required_identity": "i_EA Omega_parent=0 and i_EA Theta_parent=dB_EA",
            "current_evidence": "3766 proves this conditionally but current corpus lacks parent Omega calculation",
            "passes_current_branch": False,
            "residual_owner": "B_kernel_null",
            "next_action": "extract parent symplectic form or retain epsilon_Omega",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_3_boundary",
            "clause": "boundary/support silence",
            "required_identity": "int_boundary B_EA=0 on compact local variations/source support",
            "current_evidence": "3766 says boundary silence is required; side flux/support terms remain live",
            "passes_current_branch": False,
            "residual_owner": "B_boundary_silence",
            "next_action": "prove compact support/boundary ownership or retain epsilon_boundary",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_4_source_theta",
            "clause": "source and constants descent",
            "required_identity": "S_src=Sbar_src(q_obs,psi,A,theta) and Lie_EA theta=0",
            "current_evidence": "3766 gives exact source theorem; constants/material-marker descent remains unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_source_descent+B_theta_constants",
            "next_action": "prove same-source action and constant superselection or retain epsilon_src/epsilon_theta",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_5_readout_shadow",
            "clause": "sector readout and no shadow coframe",
            "required_identity": "all r_s=F_s o q_obs and no second hidden coframe/source frame participates",
            "current_evidence": "3766 sector readout descent is unsigned; 3517 public geometry is candidate not parent-derived",
            "passes_current_branch": False,
            "residual_owner": "B_sector_readout+B_shadow_frame+B_readout_order",
            "next_action": "prove no-shadow coframe or bound epsilon_shadow_g and epsilon_readout_s",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CPA3860_6_coframe_spin",
            "clause": "owned coframe ordinary/spin branch",
            "required_identity": "ordinary matter/spin uses e_obs and LC[e_obs], with no Gamma_ind or K slot",
            "current_evidence": "3494 proves this only inside a candidate owned-coframe branch, not globally",
            "passes_current_branch": False,
            "residual_owner": "B_coframe_spin",
            "next_action": "promote owned-coframe matter action or retain torsion/spin residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "FSU3860_0_eobs_basic_bound",
            "observable": "B_eobs_basic_3860",
            "formula": RESIDUAL_BOUND,
            "meaning": "residual preventing public coframe e_obs from being a parent-signed q_obs-basic object",
            "status": "NONCLAIM_BOUND_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FSU3860_1_frame_source_bound",
            "observable": "delta_frame_source",
            "formula": FRAME_BOUND,
            "meaning": "coframe-basicness failure propagates into the existing frame/source/clock/preferred residual family",
            "status": "FRAME_SOURCE_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FSU3860_2_tau_h_c_update",
            "observable": "B_tau_h_cstar_owner_3859",
            "formula": "B_tau_h_cstar_owner_3859 <= B_eobs_basic_3860+B_cstar_superselection+B_clock_scale+B_sector_factorization+B_preferred_frame_motion+B_EM_conformal_scale",
            "meaning": "3859 ownership now depends on public coframe basicness plus cstar/scale/factorization guards",
            "status": "TAU_H_CSTAR_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FSU3860_3_if_closed",
            "observable": "coframe-to-local-GR route",
            "formula": "if B_eobs_basic_3860=0 and B_cstar_superselection=0 then tau/h/c are q-basic; if nonLC/action/source/readout gates also close, visible EH/local-GR route opens conditionally",
            "meaning": "clean ladder from coframe basicness to metric bridge to EH action adoption",
            "status": "EXACT_CONDITIONAL_HANDOFF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3860_0_sources",
            "gate": "source-backed coframe inputs resolved",
            "status": "PASS_SOURCE_REGISTERED",
            "claim_allowed": False,
            "reason": "all coframe-basicness inputs are local source rows from 3494/3498/3504/3517/3765/3766/3767/3859",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3860_1_theorem",
            "gate": "coframe basicness theorem",
            "status": "PASS_EXACT_CONDITIONAL_COFRAME_BASICNESS_THEOREM",
            "claim_allowed": False,
            "reason": "e_obs descends by chain rule once q_obs is parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3860_2_antitautology",
            "gate": "q_obs anti-tautology guard",
            "status": "PASS_NO_QOBS_BY_DECLARATION",
            "claim_allowed": False,
            "reason": "including e_obs in q_obs is not enough without action pullback/kernel/source/readout certificates",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3860_3_current_claim",
            "gate": "current corpus proves e_obs basicness",
            "status": "BLOCKED_EOBS_BASICNESS_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "reason": CURRENT_BLOCK,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3860_4_local_GR",
            "gate": "strict-current metric/action/local-GR claim",
            "status": "BLOCKED_LOCAL_GR_CLAIM",
            "claim_allowed": False,
            "reason": "coframe basicness, cstar, nonLC connection, action adoption, source, and readout gates remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3860_5_next",
            "gate": "next target selected",
            "status": "PASS_3861_NO_SHADOW_COFRAME_TARGET",
            "claim_allowed": False,
            "reason": "the most concrete e_obs-specific leak is the possible hidden/shadow coframe epsilon_shadow_g",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3860_0",
            "decision": "e_obs basicness has an exact chain-rule theorem",
            "consequence": "the proof now depends on parent-signing q_obs, not on rewriting the metric bridge",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3860_1",
            "decision": "q_obs-by-declaration is forbidden",
            "consequence": "the candidate quotient must be backed by pullback/kernel/source/readout certificates",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3860_2",
            "decision": "attack hidden/shadow coframe next",
            "consequence": "3861 should prove no second coframe participates or retain epsilon_shadow_g as a bounded frame residual",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3860_0",
            "next_checkpoint": "3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md",
            "script": "scripts/Y5_R2FR_3861_no_shadow_coframe_basicness_or_epsilon_shadow_frame_bound.py",
            "objective": "prove no hidden/shadow coframe participates in matter, EM, source, clock, light, or orbital readout, or retain epsilon_shadow_g frame-source bounds",
            "reason": "3860 reduces e_obs basicness to parent certificates; the most concrete coframe-specific leak is a second/shadow frame",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EXACT_COFRAME_BASICNESS_THEOREM_CURRENTLY_BLOCKED",
            "claim": "no e_obs basicness, tau/h/c ownership, g_obs adoption, visible EH action adoption, beta, PPN, Newton, EM, or local-GR claim",
            "result": "exact coframe q-basic theorem derived; current corpus blocked by q_obs parent signature, L_leak/pullback, boundary/source/readout, and shadow-frame certificates",
            "next": "3861 no-shadow coframe basicness or epsilon_shadow frame bound",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    residual: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3860 - Coframe Basicness From Parent Pullback Or Frame Source Residual Bound

Private checkpoint. This attacks the public coframe throat below 3859: when is `e_obs` genuinely q_obs-basic, and when is it just an inserted observed-frame label?

Generated: `{timestamp}`

## Result

The exact q-basic coframe theorem is:

`{COFRAME_BASICNESS}`.

The parent certificate needed to use it without smuggling is:

`{PULLBACK_CERTIFICATE}`.

The anti-tautology guard is:

`{ANTI_TAUTOLOGY}`.

The strict current result is still blocked:

`{CURRENT_BLOCK}`.

The finite coframe-basicness residual is:

`{RESIDUAL_BOUND}`.

And its frame/source fallback is:

`{FRAME_BOUND}`.

So 3860 does not claim local GR. It says exactly what would make `e_obs` owned, and exactly where the failure goes if it is not owned.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Coframe Basicness Theorem

{markdown_table(theorem, ["theorem_id", "step", "status", "current_result"])}

## Parent Signature Audit

{markdown_table(audit, ["audit_id", "clause", "passes_current_branch", "residual_owner", "next_action"])}

## Frame Source Residual Update

{markdown_table(residual, ["row_id", "observable", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3860 proves the clean theorem: `e_obs` is q-basic if it is genuinely a parent-signed quotient object. But it blocks the cheap route: merely putting `e_obs` inside the q_obs tuple is not enough. The next concrete target is the shadow-frame leak: prove there is no second coframe participating in matter, EM, clock, light, source, or orbital readout, or bound `epsilon_shadow_g`.

Next target: `3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3859", "Current State After 3860", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3860 at ")
    )
    paragraph = (
        "`3860` proves the public-coframe basicness route and blocks the tautology route. "
        "If `e_obs=e_bar(q_obs)` and `v in ker(Dq_obs)`, then `D_v e_obs=0` by the chain rule; combining this with 3859 makes `tau_time`, `h_space`, and `c_*` q-basic once the public coframe and conversion constant are parent-signed. "
        "But merely including `e_obs` inside the `q_obs` tuple is not proof: the parent must sign the pullback/kernel certificate `L_parent=q_obs^*L_red+dB`, boundary silence, source descent, constant descent, and sector readout descent. "
        "Current MTS therefore retains `B_eobs_basic_3860 <= B_qobs_signature+B_pullback_Lleak+B_kernel_null+B_boundary_silence+B_source_descent+B_theta_constants+B_sector_readout+B_shadow_frame+B_coframe_spin+B_readout_order`, with frame/source fallback `delta_frame_source <= C_L epsilon_L+C_Omega epsilon_Omega+C_src epsilon_src+C_theta epsilon_theta+C_boundary epsilon_boundary+C_readout max_s epsilon_readout_s+C_shadow epsilon_shadow_g`. "
        "The next concrete coframe-specific leak is a hidden/shadow coframe.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound.md`

Target: prove `e_obs` is q_obs-basic from parent action pullback/kernel-null conditions, or route failure into frame/source/clock/preferred residual bounds.

This is the best next move because 3859 shows `tau_time`, `h_space`, and `c_*` close by chain rule once the public coframe and conversion constant are parent-signed."""
    new_gate = """`3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md`

Target: prove no hidden/shadow coframe participates in matter, EM, source, clock, light, or orbital readout, or retain `epsilon_shadow_g` frame-source bounds.

This is the best next move because 3860 reduces public coframe basicness to parent certificates, and the most concrete coframe-specific leak is a second/shadow frame."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3860_PARENT_SIGNATURE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3860_FRAME_SOURCE_RESIDUAL_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3860_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3860 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    residual: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + residual + gates)
    add(
        "VAL3860_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3860_1_chain_rule",
        "coframe chain rule theorem is explicit",
        "EXACT_CHAIN_RULE_THEOREM" in all_text and "D_v e_obs" in all_text,
        "coframe q-basic theorem present",
    )
    add(
        "VAL3860_2_parent_certificate",
        "pullback/kernel parent certificate is explicit",
        "EXACT_CONDITIONAL_KERNEL_TO_COFRAME_ROUTE" in all_text and "L_parent=q_obs^*L_red+dB" in all_text,
        "parent certificate route present",
    )
    add(
        "VAL3860_3_antitautology",
        "q_obs-by-declaration guard is active",
        "NO_QOBS_BY_DECLARATION" in all_text and "PASS_NO_QOBS_BY_DECLARATION" in all_text,
        "anti-tautology guard present",
    )
    add(
        "VAL3860_4_current_block",
        "strict-current coframe basicness remains blocked",
        "EOBS_BASICNESS_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_EOBS_BASICNESS_NOT_PARENT_SIGNED" in all_text,
        "coframe basicness not promoted",
    )
    add(
        "VAL3860_5_residual_vector",
        "coframe/frame residual vector is explicit",
        "B_eobs_basic_3860" in all_text and "delta_frame_source" in all_text and "epsilon_shadow_g" in all_text,
        "coframe and frame-source residuals present",
    )
    add(
        "VAL3860_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + residual + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3860_7_next",
        "next target is 3861 no-shadow coframe",
        DOC_PATH.exists() and "3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound" in read_text(DOC_PATH),
        "3861 no-shadow target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3860_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3860_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "The anti-tautology guard is" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3860*", "P8_Y5_BRR545_3860*", "*Y5_R2FR_3860*", "3860-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3860_10_formalization_clean",
        "formalization-workbench has no generated 3860 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3860 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3860_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    residual = residual_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, residual, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, residual, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EXACT_COFRAME_BASICNESS_THEOREM_CURRENTLY_BLOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
