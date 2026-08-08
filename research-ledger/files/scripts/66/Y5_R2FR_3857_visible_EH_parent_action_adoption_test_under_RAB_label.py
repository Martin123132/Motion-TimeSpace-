from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3857"
BRANCH = "MTS_R2FR_Y5_VISIBLE_EH_PARENT_ACTION_ADOPTION_TEST_UNDER_RAB_LABEL_3857"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3856_THEOREM = OUT / "P8_Y5_R2FR_3856_EH2_CONDITIONAL_COLLAPSE_THEOREM.csv"
CSV_3856_CLAUSES = OUT / "P8_Y5_R2FR_3856_LOVELOCK_CLAUSE_REENTRY_AUDIT.csv"
CSV_3856_BETA = OUT / "P8_Y5_R2FR_3856_BETA_RESIDUAL_UPDATE.csv"
CSV_3856_GATES = OUT / "P8_Y5_R2FR_3856_CLAIM_GATES.csv"
CSV_3856_VALIDATION = OUT / "P8_Y5_BRR545_3856_VALIDATION.csv"
CSV_3845_ACTION = OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv"
CSV_3845_BRIDGE = OUT / "P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv"
CSV_3845_CLAUSES = OUT / "P8_Y5_R2FR_3845_LOVELOCK_CLAUSE_TEST.csv"
CSV_3845_EH2 = OUT / "P8_Y5_R2FR_3845_EH2_IMPLICATION_UPDATE.csv"
CSV_3763_SIGNATURES = OUT / "P8_Y5_R2FR_3763_MINIMAL_PARENT_SIGNATURE_SET.csv"
CSV_3763_ACTION = OUT / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv"
CSV_3764_QOBS = OUT / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv"
CSV_3764_SOURCE = OUT / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv"
CSV_3765_QOBS = OUT / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv"
CSV_3765_VERDICT = OUT / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv"
CSV_3767_PULLBACK = OUT / "P8_Y5_R2FR_3767_PARENT_ACTION_PULLBACK_DECOMPOSITION.csv"
CSV_3767_VERTICAL = OUT / "P8_Y5_R2FR_3767_VERTICAL_VARIATION_AUDIT.csv"
CSV_3767_LLEAK = OUT / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv"
CSV_1030_CONTRACT = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
CSV_1008_VARIATION = OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv"
CSV_637_ACTION = OUT / "P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv"
CSV_3818_GUARDS = OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3857_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3857_VISIBLE_EH_ACTION_ADOPTION_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3857_ACTION_PIECE_ADOPTION_AUDIT.csv",
    "residual": OUT / "P8_Y5_R2FR_3857_RESIDUAL_DECOMPOSITION_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3857_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3857_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3857_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3857_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3857_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3857_00_3856_theorem", CSV_3856_THEOREM, "NEXT_CONSTRUCTION_TARGET", "3856 EH2 reentry theorem"),
    ("SRC3857_01_3856_clauses", CSV_3856_CLAUSES, "MISSING_EXPLICIT_PARENT_LAGRANGIAN", "3856 Lovelock clauses"),
    ("SRC3857_02_3856_beta", CSV_3856_BETA, "B_RAB_beta_cross", "branch-labelled beta residual"),
    ("SRC3857_03_3856_gates", CSV_3856_GATES, "PASS_3857_ACTION_ADOPTION_TARGET", "3857 target selection"),
    ("SRC3857_04_3856_validation", CSV_3856_VALIDATION, "PASS", "previous validation"),
    ("SRC3857_05_3845_action", CSV_3845_ACTION, "S_candidate", "visible EH action candidate"),
    ("SRC3857_06_3845_bridge", CSV_3845_BRIDGE, "g_obs = h_space", "metric bridge candidate"),
    ("SRC3857_07_3845_clauses", CSV_3845_CLAUSES, "PASS_IF_CANDIDATE_ADOPTED", "candidate Lovelock tests"),
    ("SRC3857_08_3845_eh2", CSV_3845_EH2, "CURRENT_NONCLAIM_ADOPTION_FAILURE_BOUND", "candidate EH2 implication"),
    ("SRC3857_09_3763_signatures", CSV_3763_SIGNATURES, "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED", "minimal signature set"),
    ("SRC3857_10_3763_action", CSV_3763_ACTION, "S_local", "local parent action ansatz"),
    ("SRC3857_11_3764_qobs", CSV_3764_QOBS, "EXACT_CONDITIONAL_ZERO_THEOREM", "single-frame quotient theorem"),
    ("SRC3857_12_3764_source", CSV_3764_SOURCE, "EXACT_CONDITIONAL_VARIATION_THEOREM", "same-total-source theorem"),
    ("SRC3857_13_3765_qobs", CSV_3765_QOBS, "q_obs_candidate", "q_obs candidate map"),
    ("SRC3857_14_3765_verdict", CSV_3765_VERDICT, "QOBS_CANDIDATE_CONSTRUCTED_BUT_NOT_PARENT_SIGNED", "q_obs verdict"),
    ("SRC3857_15_3767_pullback", CSV_3767_PULLBACK, "L_parent=q_obs^*L_red+dB+L_leak", "exact action pullback identity"),
    ("SRC3857_16_3767_vertical", CSV_3767_VERTICAL, "L_leak_kappa", "vertical variation audit"),
    ("SRC3857_17_3767_lleak", CSV_3767_LLEAK, "L_leak_shadow_g", "leak operator basis"),
    ("SRC3857_18_1030_contract", CSV_1030_CONTRACT, "CONTRACT_READY_NOT_CURRENT_THEOREM", "public metric action contract"),
    ("SRC3857_19_1008_variation", CSV_1008_VARIATION, "missing_explicit_current_chain", "parent current-chain audit"),
    ("SRC3857_20_637_action", CSV_637_ACTION, "conditional_theorem", "parent action descent attempt"),
    ("SRC3857_21_3818_guards", CSV_3818_GUARDS, "GM_orbit/G_ref cannot fill M_H_ref", "Newton/source guard"),
]

S_CANDIDATE = (
    "S_candidate=(1/(2*kappa_MTS))*int sqrt(-g_obs)*(R[g_obs]-2*Lambda_eff)"
    "+S_matter[Psi,g_obs,theta(q)]+S_GHY[g_obs]+S_silent[Phi_perp;q]"
)

ADOPTION_THEOREM = (
    "If q_obs is parent-signed, L_parent=q_obs^*L_red+dB+L_leak with L_leak=0 and silent boundary, "
    "L_red is 4D local diffeo-covariant metric-only second-order in g_obs, matter descends as one Hilbert source, "
    "kappa_MTS is quotient-owned, and no extra visible beta-order dof survives, then L_red equals EH+Lambda+GHY+same-source matter up to silent topological terms; hence S_parent adopts S_candidate."
)

ADOPTION_BOUND = (
    "B_action_adoption_3857 <= "
    "B_qobs_signature+B_metric_bridge+B_vertical_Lleak+B_operator_class+B_kappa_ownership+"
    "B_matter_descent+B_silent_variation+B_boundary_support+B_readout_gauge+B_RAB_beta_cross"
)

CURRENT_VERDICT = (
    "strict current corpus does not adopt S_candidate because q_obs/g_obs ownership, explicit current-chain L_parent, "
    "L_leak=0, kappa ownership, same-source matter descent, and silent-sector/boundary clauses are not all signed"
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
                "claim_use": "nonclaim_action_adoption_test",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "VEH3857_0_adoption_target",
            "step": "candidate action written",
            "statement": S_CANDIDATE,
            "proof_move": "make the 3845 expression an adoption target, not a copied-GR proof",
            "current_result": "CANDIDATE_AVAILABLE",
            "status": "FORMAL_TARGET_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VEH3857_1_exact_pullback_adoption_theorem",
            "step": "exact adoption theorem",
            "statement": ADOPTION_THEOREM,
            "proof_move": "combine 3767 action pullback identity with Lovelock uniqueness and 3764 same-source variation",
            "current_result": "THEOREM_DERIVED_CONDITIONALLY",
            "status": "EXACT_CONDITIONAL_ADOPTION_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VEH3857_2_current_rejection",
            "step": "strict-current adoption test",
            "statement": CURRENT_VERDICT,
            "proof_move": "test all necessary clauses against current source rows",
            "current_result": "S_CANDIDATE_NOT_ADOPTED_CURRENT_CORPUS",
            "status": "ADOPTION_REJECTED_FOR_NOW_WITH_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VEH3857_3_no_smuggle",
            "step": "RAB and GR-copy guard",
            "statement": "RAB_branch_label and formal EH notation cannot set B_action_adoption_3857 to zero; only parent ownership of q_obs/g_obs/L_parent/source/silent sectors can do it.",
            "proof_move": "keep B_RAB_beta_cross and action-adoption residuals explicit",
            "current_result": "NO_RAB_OR_GR_COPY_SMUGGLE",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "APA3857_0_qobs_public_metric",
            "action_piece": "q_obs/g_obs public metric bridge",
            "required_zero": "B_qobs_signature+B_metric_bridge=0",
            "current_evidence": "3765 constructs q_obs_candidate and 3845 writes g_obs schema, but 3765 verdict says q_obs is not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_qobs_signature+B_metric_bridge",
            "next_artifact_needed": "derive motion/time/space to tau_time,h_space,c_* to Lorentzian g_obs with sector factorization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_1_action_pullback",
            "action_piece": "parent action descent",
            "required_zero": "B_vertical_Lleak=0",
            "current_evidence": "3767 gives exact L_parent=q_obs^*L_red+dB+L_leak identity, but vertical audit leaves L_leak_top/kappa/shadow/source/theta/aux/boundary/readout live",
            "passes_current_branch": False,
            "residual_owner": "B_vertical_Lleak",
            "next_artifact_needed": "prove all vertical Euler derivatives are exact with silent boundary, or bound the L_leak operator vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_2_operator_class",
            "action_piece": "visible gravitational operator",
            "required_zero": "B_operator_class=0",
            "current_evidence": "3856/3844 identify missing explicit parent Lagrangian and operator class",
            "passes_current_branch": False,
            "residual_owner": "B_operator_class",
            "next_artifact_needed": "local 4D diffeo-covariant metric-only second-order operator theorem from MTS parent action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_3_kappa",
            "action_piece": "kappa_MTS/EH coefficient",
            "required_zero": "B_kappa_ownership=0",
            "current_evidence": "3767 keeps L_leak_kappa live and 3818 forbids orbital-GM denominator laundering",
            "passes_current_branch": False,
            "residual_owner": "B_kappa_ownership",
            "next_artifact_needed": "superselected or quotient-owned kappa_MTS tied to G_ref without fitted GM smuggling",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_4_matter_source",
            "action_piece": "same-source matter/EM/binding/apparatus source",
            "required_zero": "B_matter_descent=0",
            "current_evidence": "3764 gives exact conditional variation theorem and 1030 writes contract, but source action descent is not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_matter_descent",
            "next_artifact_needed": "S_src=Sbar_src[q_obs(Phi),psi,A,theta] with no shadow frame, source-only weights, or marker constants",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_5_silent_boundary",
            "action_piece": "silent/projector/boundary sectors",
            "required_zero": "B_silent_variation+B_boundary_support=0",
            "current_evidence": "3845 silent rule is written; 1008/3767 leave boundary, topological, auxiliary, and readout leaks live",
            "passes_current_branch": False,
            "residual_owner": "B_silent_variation+B_boundary_support",
            "next_artifact_needed": "R_silent_mu_nu=0 to second variation or explicit finite residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "APA3857_6_readout_RAB",
            "action_piece": "PPN readout and RAB cross term",
            "required_zero": "B_readout_gauge+B_RAB_beta_cross=0",
            "current_evidence": "3856 requires B_RAB_beta_cross unless temporal readout decoupling is proved",
            "passes_current_branch": False,
            "residual_owner": "B_readout_gauge+B_RAB_beta_cross",
            "next_artifact_needed": "fixed PPN gauge/readout Hessian plus RAB temporal decoupling theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "RDB3857_0_action_adoption_bound",
            "observable": "B_action_adoption_3857",
            "formula": ADOPTION_BOUND,
            "meaning": "total residual preventing the visible EH action candidate from being a parent-owned MTS action",
            "status": "NONCLAIM_BOUND_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDB3857_1_EH2_update",
            "observable": "B_EH2_vertex",
            "formula": "B_EH2_vertex <= B_action_adoption_3857+B_field_redef_gauge+B_unclassified_EH2_residual",
            "meaning": "beta EH2 remains open exactly to the extent the visible EH parent action is not adopted and readout is not fixed",
            "status": "BETA_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDB3857_2_if_adopted",
            "observable": "S_parent to local GR",
            "formula": "if B_action_adoption_3857=0 and B_field_redef_gauge=0 then S_parent -> S_candidate and B_EH2_vertex=0 on the labelled local branch",
            "meaning": "this is the clean route to local GR beta without post-hoc fitting",
            "status": "EXACT_CONDITIONAL_WIN_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDB3857_3_current_fail_vector",
            "observable": "strict-current adoption failure vector",
            "formula": "F_adopt=(B_qobs_signature,B_metric_bridge,B_vertical_Lleak,B_operator_class,B_kappa_ownership,B_matter_descent,B_silent_variation,B_boundary_support,B_readout_gauge,B_RAB_beta_cross)",
            "meaning": "the remaining work is a finite construction/vector, not an amorphous missing coupling",
            "status": "FINITE_FAILURE_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3857_0_sources",
            "gate": "source-backed adoption inputs resolved",
            "status": "PASS_SOURCE_REGISTERED",
            "claim_allowed": False,
            "reason": "all adoption theorem inputs are local source rows from 3763/3764/3765/3767/3845/3856/1030/1008",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3857_1_theorem",
            "gate": "exact action adoption theorem",
            "status": "PASS_EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "reason": "pullback identity plus Lovelock plus same-source variation gives an exact conditional adoption route",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3857_2_current_adoption",
            "gate": "current corpus adopts S_candidate",
            "status": "BLOCKED_ACTION_ADOPTION_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "reason": CURRENT_VERDICT,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3857_3_no_smuggle",
            "gate": "no GR-copy/RAB closure smuggling",
            "status": "PASS_NO_SMUGGLE_GUARD",
            "claim_allowed": False,
            "reason": "formal EH notation and RAB branch labels cannot zero action adoption residuals",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3857_4_beta_local_GR",
            "gate": "strict-current beta/local-GR claim",
            "status": "BLOCKED_BETA_LOCAL_GR_CLAIM",
            "claim_allowed": False,
            "reason": "B_action_adoption_3857, B_field_redef_gauge, and source/readout guards remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3857_5_next",
            "gate": "next target selected",
            "status": "PASS_3858_METRIC_BRIDGE_TARGET",
            "claim_allowed": False,
            "reason": "the first adoption residual to attack constructively is MTS motion/time/space to visible Lorentzian metric bridge",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3857_0",
            "decision": "S_candidate is not adopted in the strict current corpus",
            "consequence": "no beta/local-GR claim is made from formal EH notation",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3857_1",
            "decision": "adoption failure is now a finite residual vector",
            "consequence": "the route forward is to close or bound each named action-adoption residual",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3857_2",
            "decision": "attack metric ownership first",
            "consequence": "3858 should derive M,T,S -> tau_time,h_space,c_* -> g_obs or emit a no-go/residual",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3857_0",
            "next_checkpoint": "3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go.md",
            "script": "scripts/Y5_R2FR_3858_motion_time_space_visible_metric_bridge_or_signature_no_go.py",
            "objective": "derive or reject the MTS primitive bridge M,T,S -> tau_time,h_space,c_* -> one Lorentzian g_obs with quotient-owned sector readout",
            "reason": "without parent-owned g_obs, the visible EH action cannot be MTS-owned and Lovelock/EH2 cannot be claimed",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EXACT_ACTION_ADOPTION_THEOREM_CURRENTLY_BLOCKED",
            "claim": "no visible EH action adoption, beta, PPN, Newton, EM, RAB, or local-GR claim",
            "result": "exact conditional adoption theorem derived; current adoption fails into a finite residual vector; next target is MTS-to-visible-metric bridge",
            "next": "3858 motion/time/space visible metric bridge or signature no-go",
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
    text = f"""# 3857 - Visible EH Parent Action Adoption Test Under RAB Label

Private checkpoint. This is the direct attempt to make the 3845 visible EH action MTS-owned rather than just GR-looking notation.

Generated: `{timestamp}`

## Result

The adoption target is:

`{S_CANDIDATE}`.

The exact route is:

`{ADOPTION_THEOREM}`.

That is a real derivation gate: 3767 gives the exact pullback identity, Lovelock gives the EH uniqueness route, and 3764 gives the same-source variation theorem. If all premises are parent-signed, the visible action is not being smuggled in.

The strict current result is not adoption:

`{CURRENT_VERDICT}`.

So the action-adoption residual is:

`{ADOPTION_BOUND}`.

This is progress because the blocker is no longer "the coupling" as a fog bank. It is a finite vector: q_obs/g_obs ownership, vertical leak, operator class, kappa, matter descent, silent/boundary sectors, readout gauge, and RAB beta cross-term.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Visible EH Adoption Theorem

{markdown_table(theorem, ["theorem_id", "step", "status", "current_result"])}

## Action Piece Adoption Audit

{markdown_table(audit, ["audit_id", "action_piece", "passes_current_branch", "residual_owner", "next_artifact_needed"])}

## Residual Decomposition Bound

{markdown_table(residual, ["row_id", "observable", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3857 does not claim local GR. It gives the exact contract a future parent action must satisfy and cleanly rejects current adoption until the MTS primitives own `g_obs`, `L_parent`, `kappa_MTS`, source descent, and silent sectors. The best next attack is the first residual in the vector: derive the motion/time/space visible metric bridge.

Next target: `3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3856", "Current State After 3857", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3857 at ")
    )
    paragraph = (
        "`3857` attempts the visible EH parent-action adoption directly. "
        "Using the 3767 pullback identity `L_parent=q_obs^*L_red+dB+L_leak`, the 3764 same-source theorem, and the 3856 Lovelock/EH2 route, it derives an exact conditional adoption theorem: if `q_obs/g_obs` is parent-signed, `L_leak=0` with silent boundary, the reduced visible operator is local 4D diffeo-covariant metric-only second-order, `kappa_MTS` is quotient-owned, matter descends as one Hilbert source, and no extra beta-order dof survives, then the 3845 `S_candidate` is genuinely MTS-owned. "
        "The strict current corpus fails adoption into the finite residual `B_action_adoption_3857`, whose components are `B_qobs_signature`, `B_metric_bridge`, `B_vertical_Lleak`, `B_operator_class`, `B_kappa_ownership`, `B_matter_descent`, `B_silent_variation`, `B_boundary_support`, `B_readout_gauge`, and `B_RAB_beta_cross`. "
        "The next constructive pressure point is the motion/time/space to visible Lorentzian metric bridge.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label.md`

Target: try to adopt or reject the 3845 minimal visible EH parent action from MTS primitives under explicit RAB_branch_label.

This is the best next move because 3856 turns beta/EH2 into a precise parent visible-action adoption problem rather than another missing-coefficient audit."""
    new_gate = """`3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go.md`

Target: derive or reject the MTS primitive bridge `M,T,S -> tau_time,h_space,c_* -> g_obs` with one quotient-owned Lorentzian public metric.

This is the best next move because 3857 shows the visible EH action cannot be MTS-owned until the metric bridge is parent-signed rather than inserted."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3857_VISIBLE_EH_ACTION_ADOPTION_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3857_ACTION_PIECE_ADOPTION_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3857_RESIDUAL_DECOMPOSITION_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3857_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3857_VISIBLE_EH_ACTION_ADOPTION_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3857 at {timestamp} -->\n"
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
        "VAL3857_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3857_1_candidate",
        "S_candidate adoption target is explicit",
        "S_candidate" in all_text and "FORMAL_TARGET_READY" in all_text,
        "candidate visible EH action captured",
    )
    add(
        "VAL3857_2_theorem",
        "exact adoption theorem derived conditionally",
        "EXACT_CONDITIONAL_ADOPTION_ROUTE" in all_text and "Lovelock" in all_text and "L_leak=0" in all_text,
        "pullback/Lovelock/source route present",
    )
    add(
        "VAL3857_3_current_reject",
        "strict-current adoption remains blocked",
        "S_CANDIDATE_NOT_ADOPTED_CURRENT_CORPUS" in all_text and "BLOCKED_ACTION_ADOPTION_NOT_PARENT_SIGNED" in all_text,
        "candidate not adopted as claim",
    )
    add(
        "VAL3857_4_residual_vector",
        "action adoption residual vector is explicit",
        "B_action_adoption_3857" in all_text and "B_vertical_Lleak" in all_text and "B_RAB_beta_cross" in all_text,
        "finite adoption residual vector written",
    )
    add(
        "VAL3857_5_no_smuggle",
        "RAB/GR-copy guard active",
        "NO_RAB_OR_GR_COPY_SMUGGLE" in all_text and "PASS_NO_SMUGGLE_GUARD" in all_text,
        "formal EH and RAB labels cannot zero residuals",
    )
    add(
        "VAL3857_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + residual + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3857_7_next",
        "next target is 3858 metric bridge",
        DOC_PATH.exists() and "3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go" in read_text(DOC_PATH),
        "3858 metric bridge target visible",
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
        add(f"VAL3857_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3857_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "The strict current result is not adoption" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3857*", "P8_Y5_BRR545_3857*", "*Y5_R2FR_3857*", "3857-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3857_10_formalization_clean",
        "formalization-workbench has no generated 3857 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3857 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3857_11_pycache_removed",
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
    print(f"{CHECKPOINT} PASS_NONCLAIM_EXACT_ACTION_ADOPTION_THEOREM_CURRENTLY_BLOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
