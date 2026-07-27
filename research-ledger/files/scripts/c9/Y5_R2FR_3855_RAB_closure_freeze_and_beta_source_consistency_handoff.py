from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


CHECKPOINT = "3855"
BRANCH = "MTS_R2FR_Y5_RAB_CLOSURE_FREEZE_AND_BETA_SOURCE_CONSISTENCY_HANDOFF_3855"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3854_BRANCH = OUT / "P8_Y5_R2FR_3854_RAB_BRANCH_DECISION.csv"
CSV_3854_HANDOFF = OUT / "P8_Y5_R2FR_3854_BETA_SOURCE_HANDOFF_QUEUE.csv"
CSV_3854_THEOREM = OUT / "P8_Y5_R2FR_3854_CELL_LOCK_THEOREM_STATUS.csv"
CSV_3854_VALIDATION = OUT / "P8_Y5_BRR545_3854_VALIDATION.csv"
CSV_3843_BETA_LEDGER = OUT / "P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv"
CSV_3843_QUEUE = OUT / "P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv"
CSV_3843_THRESHOLD = OUT / "P8_Y5_R2FR_3843_BETA_THRESHOLD_CONTRACT.csv"
CSV_3844_LOVELOCK = OUT / "P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv"
CSV_3844_EH2 = OUT / "P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv"
CSV_3844_CLAUSES = OUT / "P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3818_GUARDS = OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv"
CSV_3826_KERNEL = OUT / "P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv"
CSV_3832_EM = OUT / "P8_Y5_R2FR_3832_EM_POYNTING_TF_STRESS_ROWS.csv"
CSV_3832_SEP = OUT / "P8_Y5_R2FR_3832_TF_VIRIAL_EM_SEPARATION.csv"
CSV_3851_BUDGET = OUT / "P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3855_SOURCE_REGISTER.csv",
    "freeze": OUT / "P8_Y5_R2FR_3855_RAB_BRANCH_FREEZE.csv",
    "matrix": OUT / "P8_Y5_R2FR_3855_LOCAL_GR_HANDOFF_MATRIX.csv",
    "beta": OUT / "P8_Y5_R2FR_3855_BETA_REENTRY_QUEUE.csv",
    "source": OUT / "P8_Y5_R2FR_3855_SOURCE_NORMALIZATION_REENTRY_QUEUE.csv",
    "em": OUT / "P8_Y5_R2FR_3855_EM_STRESS_REENTRY_QUEUE.csv",
    "gates": OUT / "P8_Y5_R2FR_3855_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3855_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3855_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3855_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3855_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3855_0_3854_branch", CSV_3854_BRANCH, "FREEZE_AS_CONTROL_BRANCH_NOT_DERIVED"),
    ("SRC3855_1_3854_handoff", CSV_3854_HANDOFF, "beta/second-order temporal self-coupling"),
    ("SRC3855_2_3854_theorem", CSV_3854_THEOREM, "CELL_LOCK_NOT_DERIVED_CURRENT_CORPUS"),
    ("SRC3855_3_3854_validation", CSV_3854_VALIDATION, "PASS"),
    ("SRC3855_4_3843_beta_ledger", CSV_3843_BETA_LEDGER, "STRUCTURALLY_COMPLETE_NONCLAIM_BETA_LEDGER"),
    ("SRC3855_5_3843_queue", CSV_3843_QUEUE, "parent EH second-variation / nonlinear self-source proof"),
    ("SRC3855_6_3843_threshold", CSV_3843_THRESHOLD, "MISSING_EXTERNAL_NUMERIC_PPN_BETA_SOURCE"),
    ("SRC3855_7_3844_lovelock", CSV_3844_LOVELOCK, "Lovelock-style uniqueness"),
    ("SRC3855_8_3844_eh2", CSV_3844_EH2, "B_EH2_vertex"),
    ("SRC3855_9_3844_clauses", CSV_3844_CLAUSES, "all Lovelock/EH2 clauses pass simultaneously"),
    ("SRC3855_10_3818_poisson", CSV_3818_POISSON, "nabla^2 Phi=4*pi*G_ref rho_H"),
    ("SRC3855_11_3818_guards", CSV_3818_GUARDS, "GM_orbit/G_ref cannot fill M_H_ref"),
    ("SRC3855_12_3826_kernel", CSV_3826_KERNEL, "R_kernel_total_3826"),
    ("SRC3855_13_3832_em", CSV_3832_EM, "epsilon_EM_Poynting_TF"),
    ("SRC3855_14_3832_sep", CSV_3832_SEP, "Sigma_TF_matter = Sigma_TF_virial + Sigma_TF_EM_Poynting"),
    ("SRC3855_15_3851_budget", CSV_3851_BUDGET, "6.102178699076298e-11"),
]

RAB_CLOSURE_RULE = "R_AB=0 may be used only as explicit closure/control branch, not as strict-current derivation"
RAB_FINITE_RULE = "finite R_AB hair remains only if source-backed B_RAB beats the 3851 Cassini pressure budget"
BETA_FORMULA = "abs(beta-1) <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+B_eps_temporal_order+B_eps_temporal_gauge+B_eps_temporal_domain+B_eps_temporal_nonlinear+B_eps_temporal_multipole_motion+B_eps_temporal_denominator"
POISSON_FORMULA = "nabla^2 Phi = 4*pi*G_ref*rho_H + S_EH + S_source + S_boundary + S_domain + S_nonEH + S_readout"
EM_FORMULA = "epsilon_EM_Poynting_TF <= B_EM_field_TF + B_Poynting_flux_TF + B_parent_EM_mismatch_TF"


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


def budget_value() -> Decimal:
    for row in read_csv_rows(CSV_3851_BUDGET):
        if row.get("budget_id") == "RBC3851_0_near_limb_scalar_budget":
            return Decimal(row["exact_log_bound"])
    raise RuntimeError("3851 R_AB budget row missing")


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
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
                "role": "input_for_RAB_freeze_and_beta_source_EM_handoff",
                "claim_use": "nonclaim_branch_freeze_and_reentry_matrix",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def freeze_rows(timestamp: str) -> list[dict[str, object]]:
    budget = budget_value()
    return [
        {
            "freeze_id": "RBF3855_0_closure_control",
            "branch": "explicit_RAB_zero_closure",
            "allowed_use": "control/local-GR-lane assumption for comparing downstream beta/source requirements",
            "forbidden_use": "do not cite as derived parent theorem; do not use to erase beta/Newton/source/EM residuals",
            "rule": RAB_CLOSURE_RULE,
            "source": rel(CSV_3854_BRANCH),
            "status": "FROZEN_CONTROL_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "freeze_id": "RBF3855_1_finite_hair_bound",
            "branch": "finite_RAB_hair",
            "allowed_use": "source-bound residual branch if Pi_R/J_R/boundary rows are actually sourced",
            "forbidden_use": "no unsourced reciprocal hair; no fitted PPN p; no cancellation against beta/source errors",
            "rule": f"{RAB_FINITE_RULE}: B_RAB <= {budget} before other gamma residuals",
            "source": rel(CSV_3854_BRANCH),
            "status": "FROZEN_SEVERE_BOUND_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "freeze_id": "RBF3855_2_branch_selector",
            "branch": "RAB_branch_label",
            "allowed_use": "every downstream local-GR row must declare closure_control or finite_hair_bound",
            "forbidden_use": "unlabelled use of R_AB=0 or silent assumption of gamma closure",
            "rule": "RAB_branch_label in {explicit_RAB_zero_closure, finite_RAB_hair}",
            "source": rel(CSV_3854_THEOREM),
            "status": "REQUIRED_DOWNSTREAM_METADATA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def matrix_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "matrix_id": "LGM3855_0_gamma_RAB",
            "sector": "gamma/R_AB no-hair",
            "carried_result": "closure branch available; finite branch severely bounded",
            "what_RAB_freeze_solves": "removes the repeated AB=1/gamma throat from the live derivation loop",
            "what_remains_open": "full no-slip/readout and finite-hair source rows remain nonclaim",
            "next_action": "do not revisit unless parent all-subdomain cell charge or sourced B_RAB row appears",
            "status": "FROZEN_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "matrix_id": "LGM3855_1_beta",
            "sector": "PPN beta / second-order temporal self-coupling",
            "carried_result": BETA_FORMULA,
            "what_RAB_freeze_solves": "prevents gamma/R_AB work from being mistaken for beta",
            "what_remains_open": "EH2 vertex, source self-energy, readout/gauge, boundary/domain, scalar/hidden rows",
            "next_action": "return to SFQ3843_0 parent EH second-variation / nonlinear self-source proof under RAB_branch_label",
            "status": "NEXT_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "matrix_id": "LGM3855_2_Newton_source",
            "sector": "Newton/source normalization",
            "carried_result": POISSON_FORMULA,
            "what_RAB_freeze_solves": "none directly; it only fixes one spatial routing branch",
            "what_remains_open": "positive same-frame M_H_ref, Pi_M J_H closure, worldtube selector, anti-circular GM guard",
            "next_action": "keep 3818/3826 source-normalization guards active in beta and Newton rows",
            "status": "OPEN_PARALLEL_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "matrix_id": "LGM3855_3_EM_stress",
            "sector": "Maxwell/EM stress and Poynting",
            "carried_result": EM_FORMULA,
            "what_RAB_freeze_solves": "none directly; EM stress cannot be hidden in R_AB closure",
            "what_remains_open": "EM TF stress, Poynting/radiative flux, parent EM mismatch source bounds",
            "next_action": "keep EM/Poynting in total Hilbert/source ledger before no-slip or beta claims",
            "status": "OPEN_PARALLEL_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "BRE3855_0_EH2_reentry",
            "priority": "P0",
            "target": "parent EH second-variation / nonlinear self-source proof",
            "carry_RAB_branch_label": True,
            "needed_artifact": "second-variation operator identity or explicit residual norm row",
            "source_basis": rel(CSV_3843_QUEUE) + ";" + rel(CSV_3844_LOVELOCK),
            "blockers": "signed parent visible Lagrangian; Lovelock clauses; Hilbert source glue; Newtonian normalization; readout gauge",
            "status": "NEXT_DERIVATION_TARGET_WITH_RAB_LABEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "BRE3855_1_beta_threshold",
            "priority": "P3",
            "target": "source-backed empirical beta threshold",
            "carry_RAB_branch_label": True,
            "needed_artifact": "current PPN beta bound row with source/citation/confidence",
            "source_basis": rel(CSV_3843_THRESHOLD),
            "blockers": "threshold currently symbolic in 3843; no component budgets before source-backed tau_beta",
            "status": "SOURCE_ACQUISITION_AFTER_DERIVATION_TARGET_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "SRE3855_0_same_frame_MHref",
            "target": "positive same-frame M_H_ref",
            "formula": "M_H_ref=H_tau[S_link]-H_ref>0",
            "source_basis": rel(CSV_3818_GUARDS),
            "why_needed": "Newton/source normalization and beta denominator cannot borrow fitted orbital GM",
            "status": "OPEN_BLOCKER_CARRIED_FORWARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SRE3855_1_PiM_JH",
            "target": "Pi_M J_H compact-exterior closure",
            "formula": "d(Pi_M J_H)=0 and [d,Pi_M]J_H=0 or finite obstruction vector",
            "source_basis": rel(CSV_3818_GUARDS) + ";" + rel(CSV_3826_KERNEL),
            "why_needed": "same source charge must feed Poisson, orbital readout, PPN, and clock/source rows",
            "status": "OPEN_BLOCKER_CARRIED_FORWARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SRE3855_2_anti_circular_GM",
            "target": "no orbital-GM denominator laundering",
            "formula": "GM_orbit/G_ref cannot fill M_H_ref unless Poisson/Gauss/orbital bridge is already derived",
            "source_basis": rel(CSV_3818_GUARDS),
            "why_needed": "prevents Newton/local-GR source normalization from becoming a fitted-product trick",
            "status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def em_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "EMR3855_0_EM_TF",
            "target": "EM/Poynting TF stress bound or same-source cancellation",
            "formula": EM_FORMULA,
            "source_basis": rel(CSV_3832_EM) + ";" + rel(CSV_3832_SEP),
            "why_needed": "no-slip/gamma and beta/source conservation need total stress, not matter-only stress",
            "status": "OPEN_BLOCKER_CARRIED_FORWARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "EMR3855_1_total_Hilbert",
            "target": "EM stress included in same Hilbert/source ledger",
            "formula": "Sigma_TF_matter = Sigma_TF_virial + Sigma_TF_EM_Poynting + Sigma_TF_apparatus + Sigma_TF_quad",
            "source_basis": rel(CSV_3832_SEP),
            "why_needed": "preserves Poynting/vector-wave intuition without bypassing local-GR consistency gates",
            "status": "OPEN_PARALLEL_PRIORITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3855_0_RAB_freeze",
            "gate": "R_AB branch labels frozen",
            "status": "PASS_BRANCH_FREEZE_NONCLAIM",
            "claim_allowed": False,
            "reason": "closure and finite-hair branches are explicit and cannot be silently mixed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3855_1_beta_reentry",
            "gate": "beta reentry queue selected",
            "status": "PASS_NEXT_PRIORITY_SELECTED",
            "claim_allowed": False,
            "reason": "3843 P0 EH2/source-self-coupling proof is the next real local-GR gap",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3855_2_no_RAB_overclaim",
            "gate": "R_AB closure not used as beta/Newton/EM proof",
            "status": "PASS_OVERCLAIM_GUARD",
            "claim_allowed": False,
            "reason": "handoff matrix says exactly what R_AB freeze does and does not solve",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3855_3_source_guards",
            "gate": "source-normalization guards carried",
            "status": "PASS_GUARDS_CARRIED_FORWARD",
            "claim_allowed": False,
            "reason": "M_H_ref, Pi_M J_H, worldtube, and anti-circular GM guards remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3855_4_EM_guard",
            "gate": "EM/Poynting stress carried",
            "status": "PASS_EM_STRESS_CARRIED_FORWARD",
            "claim_allowed": False,
            "reason": "EM TF stress/Poynting cannot be hidden inside a matter-only source ledger",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3855_0",
            "decision": "freeze R_AB branch labels and stop revisiting the same origin fork",
            "consequence": "future local-GR work must carry explicit_RAB_zero_closure or finite_RAB_hair metadata",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3855_1",
            "decision": "return to beta through EH2/source-self-coupling rather than another gamma/R_AB loop",
            "consequence": "next target is parent second variation under the branch label",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3855_2",
            "decision": "keep Newton/source and EM/Poynting as live parallel blockers",
            "consequence": "beta work must not borrow fitted GM or ignore total EM stress",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3855_0",
            "next_checkpoint": "3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label.md",
            "script": "scripts/Y5_R2FR_3856_beta_EH2_reentry_under_RAB_branch_label.py",
            "objective": "attack the P0 beta gap: parent EH second variation / nonlinear self-source proof under explicit RAB branch metadata, without using R_AB closure as a beta proof",
            "reason": "3855 freezes the gamma/R_AB fork and the 3843 dashboard identifies EH2/source self-coupling as the highest-leverage beta target",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_RAB_BRANCH_FREEZE_BETA_SOURCE_HANDOFF",
            "claim": "no strict-current R_AB zero, beta, Newton, EM, PPN, or local-GR claim",
            "result": "R_AB branch labels frozen; beta EH2/source-self-coupling selected as next target; Newton/source and EM stress guards carried",
            "next": "3856 beta EH2 reentry under RAB branch label",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    freeze: list[dict[str, object]],
    matrix: list[dict[str, object]],
    beta: list[dict[str, object]],
    source: list[dict[str, object]],
    em: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3855 - R_AB Closure Freeze And Beta Source Consistency Handoff

Private checkpoint. This freezes the `R_AB` branch outcome from 3854 and routes the work back into beta, Newton/source normalization, and EM stress without pretending `R_AB=0` has been derived.

Generated: `{timestamp}`

## Result

The `R_AB` throat is now a labelled branch, not an active loop:

`{RAB_CLOSURE_RULE}`.

`{RAB_FINITE_RULE}`.

Every downstream local-GR row must carry:

`RAB_branch_label in {{explicit_RAB_zero_closure, finite_RAB_hair}}`.

The beta branch is re-opened with the integrated 3843 formula:

`{BETA_FORMULA}`.

The key discipline is this: `R_AB=0` may simplify the gamma/no-hair lane as a control branch, but it does not prove beta, Newtonian source normalization, or EM stress conservation. Those remain separate gates:

`{POISSON_FORMULA}`.

`{EM_FORMULA}`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## R_AB Branch Freeze

{markdown_table(freeze, ["freeze_id", "branch", "status", "allowed_use", "forbidden_use"])}

## Local GR Handoff Matrix

{markdown_table(matrix, ["matrix_id", "sector", "status", "what_RAB_freeze_solves", "what_remains_open"])}

## Beta Reentry Queue

{markdown_table(beta, ["queue_id", "priority", "target", "status", "blockers"])}

## Source Normalization Reentry Queue

{markdown_table(source, ["queue_id", "target", "status", "why_needed"])}

## EM Stress Reentry Queue

{markdown_table(em, ["queue_id", "target", "status", "why_needed"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3855 is the anti-loop checkpoint. The gamma/R_AB fork is disciplined enough for now. The next meaningful derivation target is beta: parent EH second variation / nonlinear self-source proof, while carrying the explicit RAB branch label and keeping source normalization plus EM/Poynting stress guards alive.

Next target: `3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3854", "Current State After 3855", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3855 at ")
    )
    paragraph = (
        "`3855` freezes the R_AB outcome as branch metadata rather than leaving it as a live loop. "
        "`explicit_RAB_zero_closure` may be used only as a local GR-control assumption, not as a strict-current derivation; `finite_RAB_hair` remains only as a source-backed severe-bound branch. "
        "Every downstream local-GR row must now carry `RAB_branch_label in {explicit_RAB_zero_closure, finite_RAB_hair}`. "
        "The handoff matrix reopens the real local-GR blockers: beta via the 3843 integrated ledger and 3844 EH2/Lovelock route, Newton/source normalization via the 3818/3826 M_H_ref/Pi_M/anti-circular-GM guards, and EM/Poynting stress via the 3832 total-stress rows. "
        "The next priority is the parent EH second variation / nonlinear self-source proof under the R_AB branch label.\n\n"
    )
    anchor = "`3854` audits"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3855-Y5-R2FR-RAB-closure-freeze-and-beta-source-consistency-handoff.md`

Target: freeze the R_AB branch labels, carry explicit closure/finite-hair status into the local-GR dashboard, and resume beta/Newton/source/EM consistency without pretending `R_AB=0` is derived.

This is the best next move because 3854 exhausts the current gauge/topology origin routes; the real project now needs beta and calibrated source coupling."""
    new_gate = """`3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label.md`

Target: attack the P0 beta gap: parent EH second variation / nonlinear self-source proof under explicit RAB branch metadata, without using R_AB closure as a beta proof.

This is the best next move because 3855 freezes the gamma/R_AB fork and the 3843 dashboard identifies EH2/source self-coupling as the highest-leverage beta target."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3855_RAB_BRANCH_FREEZE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3855_LOCAL_GR_HANDOFF_MATRIX.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3855_BETA_REENTRY_QUEUE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3855_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3855_RAB_BRANCH_FREEZE.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3855 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    freeze: list[dict[str, object]],
    matrix: list[dict[str, object]],
    beta: list[dict[str, object]],
    source: list[dict[str, object]],
    em: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in freeze + matrix + beta + source + em + gates)
    add(
        "VAL3855_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add("VAL3855_1_freeze", "R_AB branch freeze rows exist", "FROZEN_CONTROL_BRANCH" in all_text and "FROZEN_SEVERE_BOUND_BRANCH" in all_text, "both branches frozen")
    add("VAL3855_2_branch_label", "downstream branch label required", "RAB_branch_label" in all_text and "REQUIRED_DOWNSTREAM_METADATA" in all_text, "branch metadata required")
    add("VAL3855_3_beta_formula", "integrated beta formula carried", "B_EH2_vertex+B_extra_scalar2" in all_text and "NEXT_PRIORITY" in all_text, "beta formula and priority carried")
    add("VAL3855_4_source_guards", "Newton/source guards carried", "M_H_ref" in all_text and "GM_orbit/G_ref cannot fill M_H_ref" in all_text, "source guards carried")
    add("VAL3855_5_em_guards", "EM/Poynting guards carried", "epsilon_EM_Poynting_TF" in all_text and "Poynting" in all_text, "EM/Poynting guards carried")
    add("VAL3855_6_nonclaim", "all 3855 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in freeze + matrix + beta + source + em + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3855_7_next", "next target is 3856", DOC_PATH.exists() and "3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label" in read_text(DOC_PATH), "3856 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3855_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3855_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "anti-loop checkpoint" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3855*", "P8_Y5_BRR545_3855*", "*Y5_R2FR_3855*", "3855-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3855_10_formalization_clean", "formalization-workbench has no generated 3855 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3855 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3855_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    freeze = freeze_rows(timestamp)
    matrix = matrix_rows(timestamp)
    beta = beta_rows(timestamp)
    source = source_rows(timestamp)
    em = em_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["freeze"], freeze)
    write_csv(OUTPUTS["matrix"], matrix)
    write_csv(OUTPUTS["beta"], beta)
    write_csv(OUTPUTS["source"], source)
    write_csv(OUTPUTS["em"], em)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, freeze, matrix, beta, source, em, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, freeze, matrix, beta, source, em, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_RAB_BRANCH_FREEZE_BETA_SOURCE_HANDOFF")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
