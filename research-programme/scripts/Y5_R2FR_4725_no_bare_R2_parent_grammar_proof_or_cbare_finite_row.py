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
PARENT_ACTION_DIR = POST / "source-intake" / "parent-action"

CHECKPOINT = "4725"
CLAIM_ID = "L-567"
MARKER = "PPC4161_NO_BARE_R2_PARENT_GRAMMAR_OR_CBARE_FINITE_ROW_4725"
PACKET_MARKER = "PPC4161_PACKET_NO_BARE_R2_PARENT_GRAMMAR_OR_CBARE_FINITE_ROW_4725"
DECISION = "NO_DIRECT_BARE_R2_SLOT_EXCLUDED_IN_CANDIDATE_GRAMMAR_GLOBAL_CBARE_UNSIGNED_FINITE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md"

DOC_PATH = POST / "4725-Y5-R2FR-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md"
FORMAL_PATH = FORMAL / "741-PPC4161-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_SOURCE_REGISTER.csv"
GRAMMAR_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_NO_BARE_R2_GRAMMAR_AUDIT.csv"
CBARE_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_CBARE_SPLIT_ROWS.csv"
CBARE_FINITE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_CBARE_FINITE_SOURCE_ROW.csv"
PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_CBARE_TO_MU_PROJECTION_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4725_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4725_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4725_0", POST / "CURRENT_LOCAL_RESUME.md", "4725-Y5-R2FR-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md", "4724 handoff target."),
    ("SRC4725_1", POST / "4724-Y5-R2FR-visible-cell-cR2-zero-signature-or-R2-mu-bound-runner.md", "TCZ4724_3_bare_operator_zero", "4724 identifies c_bare as next proof target."),
    ("SRC4725_2", SOURCE_DIR / "P8_Y5_R2FR_4724_CR2_COMPONENT_SIGNATURE_AUDIT.csv", "CR2COMP4724_1_bare", "4724 c_bare component row."),
    ("SRC4725_3", ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "The full action is:", "Core MTS action gives EH plus curvature-exchange potential."),
    ("SRC4725_4", ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "Construct the effective macroscopic action:", "Fundamental action note gives effective MTS-Einstein action."),
    ("SRC4725_5", SOURCE_DIR / "P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv", "DG2485_3_higher_curvature", "2485 retains higher-curvature terms unless forbidden or bounded."),
    ("SRC4725_6", SOURCE_DIR / "P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv", "NF2485_0_parent_action_skeleton", "2485 parent action skeleton includes residual operator sum."),
    ("SRC4725_7", SOURCE_DIR / "P8_Y5_PARENT_NORMAL_FORM_2485_COEFFICIENT_SLOT_LEDGER.csv", "CS2485_2_c_HD", "2485 higher-derivative coefficient slot ledger."),
    ("SRC4725_8", SOURCE_DIR / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv", "G3007_0_total_normal_form", "3007 minimal parent action grammar remains unsigned."),
    ("SRC4725_9", SOURCE_DIR / "P8_Y5_R2FR_3007_OMITTED_SECTOR_DEMOTION_LEDGER.csv", "OMIT3007_0_higher_derivative", "3007 says higher-derivative omission requires zero/topological/bound."),
    ("SRC4725_10", SOURCE_DIR / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv", "INS3890_0_action", "3890 candidate action with grammar insertion and S_R11 residual channel."),
    ("SRC4725_11", SOURCE_DIR / "P8_Y5_R2FR_3890_REMAINING_SOURCE_CHANNELS.csv", "REM3890_5_R11", "3890 leaves R11/non-EH operator factorization alive."),
    ("SRC4725_12", SOURCE_DIR / "P8_Y5_R2FR_4720_PARENT_EH_SIGNATURE_CLAUSES.csv", "EHSC4720_2_two_derivative_IR", "4720 parent EH signature clause for two-derivative IR."),
    ("SRC4725_13", SOURCE_DIR / "P8_Y5_R2FR_4720_NONEH_OPERATOR_COEFFICIENT_MATRIX.csv", "NEH4720_0_R2_fR_scalar", "4720 R2/f(R) non-EH operator coefficient row."),
    ("SRC4725_14", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1589_COEFFICIENT_SOURCE_HUNT.csv", "HUNT1589_2_no_bare_R2", "1589 source hunt found no parent no-bare-R2 clause."),
    ("SRC4725_15", SOURCE_DIR / "P8_Y5_R2FR_4504_FINITE_BOUND_CONTRACT.csv", "FB4504_1_standard_mu_bound", "4504 finite mu bound contract."),
    ("SRC4725_16", SOURCE_DIR / "P8_Y5_R2FR_4504_STANDARD_BOUND_IMPORT.csv", "SB4504_2_combined_range", "4504 standard bound import."),
    ("SRC4725_17", PARENT_ACTION_DIR / "minimal_parent_action_sector_grammar_3007_NOT_SIGNED.csv", "G3007_0_total_normal_form", "Parent-action copy of 3007 grammar, explicitly not signed."),
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


def grammar_audit_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "NBARE4725_0_core_action_shape",
            "Historical core action shape",
            "The older core action writes an effective EH plus curvature-exchange-potential action with no explicit R^2 term.",
            "SRC4725_3",
            "SUPPORTS_NO_DIRECT_BARE_SLOT",
            "It is an effective macroscopic action and does not prove parent grammar exhaustiveness.",
            False,
        ),
        (
            "NBARE4725_1_fundamental_action_shape",
            "Fundamental action note",
            "The fundamental action note also constructs the MTS-Einstein action as EH plus L_Lambda_kappa plus matter.",
            "SRC4725_4",
            "SUPPORTS_NO_DIRECT_BARE_SLOT",
            "It calls the action effective/macroscopic and does not ban all higher-curvature counterterms.",
            False,
        ),
        (
            "NBARE4725_2_2485_derivative_grammar",
            "Parent normal-form derivative grammar",
            "Higher curvature terms are explicitly retained as c_HD unless forbidden, topological, or bounded.",
            "SRC4725_5",
            "BLOCKS_GLOBAL_NO_BARE_PROOF",
            "The derivative grammar is not signed as excluding higher curvature.",
            False,
        ),
        (
            "NBARE4725_3_3007_minimal_grammar",
            "Minimal parent action grammar",
            "3007 writes a useful parent-action contract, but the EH block is a comparator/reference and residual sectors remain explicit.",
            "SRC4725_8",
            "GRAMMAR_CONTRACT_NOT_PARENT_SIGNED",
            "The grammar is selected/staged, not a globally signed parent action.",
            False,
        ),
        (
            "NBARE4725_4_3890_candidate_action",
            "3890 candidate branch",
            "In the 3890 candidate action, the displayed direct action does not introduce a free bare R^2 coefficient outside its residual/R11 channel.",
            "SRC4725_10",
            "CANDIDATE_DIRECT_SLOT_EXCLUDED",
            "This only signs the candidate branch and leaves S_R11/non-EH factorization open.",
            False,
        ),
        (
            "NBARE4725_5_R11_survivor",
            "R11/non-EH channel",
            "3890 explicitly keeps R11/non-EH operator factorization as remaining source channel.",
            "SRC4725_11",
            "RESIDUAL_CURVATURE_SQUARE_SURVIVES",
            "The candidate grammar cannot be used as total c_bare=0 while R11 can carry curvature-square response.",
            False,
        ),
        (
            "NBARE4725_6_4720_selector",
            "Two-derivative selector route",
            "4720 shows R2/f(R) is killed if the two-derivative EH selector is parent-signed.",
            "SRC4725_12",
            "CONDITIONAL_ZERO_ROUTE",
            "The selector clause is still unsigned, so this is not a claim-grade no-bare proof.",
            False,
        ),
        (
            "NBARE4725_7_1589_hunt",
            "Prior coefficient source hunt",
            "1589 already found no parent clause proving the action excludes bare R^2/f(R)/R F(Box) R terms.",
            "SRC4725_14",
            "NO_PARENT_NO_BARE_CLAUSE_FOUND",
            "This blocks global c_bare=0 in current evidence.",
            False,
        ),
        (
            "NBARE4725_8_verdict",
            "No-bare-R2 proof verdict",
            "Direct bare R2 is excluded only inside a candidate grammar branch; global c_bare remains unsigned and must be finite-rowed.",
            "SRC4725_2",
            "DIRECT_ZERO_CANDIDATE_GLOBAL_FINITE_ROW",
            "Do not promote local GR from this split alone.",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "target": target,
            "finding": finding,
            "source_path": source_path(src),
            "verdict": verdict,
            "blocker_or_guardrail": guardrail,
            "claim_allowed": claim,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for audit_id, target, finding, src, verdict, guardrail, claim in specs
    ]


def cbare_split_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CBS4725_0_direct_metric_slot",
            "c_bare_direct",
            "a free explicit sqrt(-g) R^2/f(R) coefficient outside residual sectors",
            "0 in the 3890 candidate grammar branch if that branch is adopted",
            "CANDIDATE_BRANCH_ZERO_NOT_GLOBAL",
            "Candidate action omits the direct bare slot but is not global corpus adoption.",
        ),
        (
            "CBS4725_1_R11_residual_slot",
            "c_R11_curvature_square",
            "curvature-square response carried by S_R11[Sigma_loc(y),g_obs,Psi] or non-EH factorization",
            "MISSING_FACTORISATION_ZERO_OR_NUMERIC_VALUE",
            "LIVE_RESIDUAL_SLOT",
            "3890 says R11/non-EH operator factorization remains open.",
        ),
        (
            "CBS4725_2_counterterm_slot",
            "c_counterterm",
            "renormalized/singular-running R2 residue or separate UV datum",
            "MISSING_NO_COUNTERTERM_PARENT_RULE",
            "LIVE_COUNTERTERM_SLOT",
            "The no-grain theorem explicitly warns that finite residue can survive through singular running/counterterm.",
        ),
        (
            "CBS4725_3_global_cbare",
            "c_bare_global",
            "effective sum of direct metric slot, R11 residual slot and counterterm slot",
            "MISSING_TOTAL_c_bare_ZERO_OR_VALUE",
            "GLOBAL_ZERO_UNSIGNED",
            "Direct candidate zero is not enough to zero the global bare component.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": split_id,
            "quantity": quantity,
            "meaning": meaning,
            "current_value": current_value,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for split_id, quantity, meaning, current_value, status, reason in specs
    ]


def cbare_finite_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CBARE4725_0_direct_candidate_zero",
            "quantity": "c_bare_direct",
            "formula_or_value": "0_IF_3890_CANDIDATE_GRAMMAR_ADOPTED",
            "units": "m^2 after EH/f(R) normalization",
            "source_path": source_path("SRC4725_10"),
            "source_status": "candidate_branch_only_not_global",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "do not use outside candidate branch without global adoption",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CBARE4725_1_R11_residual",
            "quantity": "c_R11_curvature_square",
            "formula_or_value": "MISSING_R11_FACTORISATION_ZERO_OR_NUMERIC_COEFFICIENT",
            "units": "m^2 or declared operator-normalized units",
            "source_path": source_path("SRC4725_11"),
            "source_status": "live_nonEH_residual_channel",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "prove Sigma_loc factorization/double-zero or fill finite coefficient row",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CBARE4725_2_counterterm",
            "quantity": "c_counterterm",
            "formula_or_value": "MISSING_NO_SINGULAR_COUNTERTERM_RULE_OR_VALUE",
            "units": "m^2 or declared operator-normalized units",
            "source_path": source_path("SRC4725_5"),
            "source_status": "higher_curvature_retained_unless_forbidden_or_bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "derive parent no-counterterm/UV datum rule or finite source-backed prior",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CBARE4725_3_global_effective",
            "quantity": "c_bare_global",
            "formula_or_value": "c_bare_direct + c_R11_curvature_square + c_counterterm",
            "units": "m^2 after EH/f(R) normalization",
            "source_path": source_path("SRC4725_2"),
            "source_status": "finite_row_staged_nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "carry as retained c_R2_eff component until all subslots zero or bounded",
            "timestamp_utc": ts,
        },
    ]


def projection_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CBMU4725_0_pure_fR_projection",
            "mu_bare = N_bare_to_fR * c_bare_global",
            "N_bare_to_fR; c_bare_global; sign convention",
            "MISSING_NORMALIZATION_AND_VALUE",
            "standard f(R)=R+mu R^2 branch",
        ),
        (
            "CBMU4725_1_range_projection",
            "lambda_R = sqrt(6 mu_bare)",
            "positive mu_bare in standard convention",
            "MISSING_mu_bare",
            "only meaningful after c_bare_global maps to positive pure f(R) scalar",
        ),
        (
            "CBMU4725_2_alpha_projection",
            "alpha_eff = (1/3) C_body^2 or screened/body-charge value",
            "C_body or source-charge zero/screening theorem",
            "MISSING_C_body_OR_SCREENING",
            "do not use alpha=1/3 as MTS claim unless pure metric branch is sourced",
        ),
        (
            "CBMU4725_3_bound_interface",
            "if mu_bare is owned, compare mu_bare <= 1.443476e15 m^2 or use full alpha(lambda)",
            "claim-grade MTS mu, alpha_eff and bound curve",
            "BOUND_TARGET_READY_INPUTS_MISSING",
            "template threshold only, not a prediction",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "projection_id": projection_id,
            "projection_formula": formula,
            "needed_inputs": inputs,
            "current_status": status,
            "meaning": meaning,
            "source_path": source_path("SRC4725_15") if projection_id != "CBMU4725_3_bound_interface" else source_path("SRC4725_16"),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for projection_id, formula, inputs, status, meaning in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4725_0_sources_verified", "All 4725 sources exist and needles are found.", True, "NONE"),
        ("GATE4725_1_global_no_bare_R2_signed", "Parent grammar globally forbids bare R2/f(R)/R F(Box) R before reduction.", False, "GLOBAL_PARENT_GRAMMAR_UNSIGNED"),
        ("GATE4725_2_candidate_direct_slot_zero", "Direct bare R2 slot is excluded inside a named candidate branch.", True, "CANDIDATE_ONLY_NOT_CLAIM"),
        ("GATE4725_3_R11_residual_zero", "S_R11/non-EH factorization cannot regenerate curvature-square response.", False, "R11_RESIDUAL_CHANNEL_LIVE"),
        ("GATE4725_4_counterterm_zero", "No singular running/counterterm/UV datum can leave c_bare finite.", False, "COUNTERTERM_RULE_MISSING"),
        ("GATE4725_5_cbare_numeric_or_zero", "c_bare_global has exact zero or source-backed numeric value.", False, "MISSING_GLOBAL_CBARE_ZERO_OR_VALUE"),
        ("GATE4725_6_local_GR_R2_channel_closed", "Bare component of c_R2_eff is removed claim-grade.", False, "CBARE_GLOBAL_RETAINED_NONCLAIM"),
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
        ("FW4725_0_effective_action_not_exhaustive", "Do not treat an effective EH-plus-potential action as a global parent no-bare theorem."),
        ("FW4725_1_candidate_branch_scope", "Do not export 3890 candidate-branch direct-slot zero to the whole historical corpus."),
        ("FW4725_2_R11_survivor", "Do not ignore S_R11/non-EH factorization when claiming no curvature-square response."),
        ("FW4725_3_no_counterterm_smuggling", "Do not hide singular running or UV counterterms under visible-cell no-grain suppression."),
        ("FW4725_4_no_bound_backsolve", "Do not infer c_bare from the mu/R10 bound; derive or source it first."),
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
            "derivation_result": "direct bare R2 slot is absent only in candidate grammar; global c_bare remains live through R11/counterterm channels",
            "finite_row_result": "c_bare_global = c_bare_direct + c_R11_curvature_square + c_counterterm staged nonclaim",
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
            "status_id": "STATUS4725_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4725_1_science_verdict",
            "status": "candidate_direct_bare_slot_zero_but_global_cbare_live",
            "detail": "This is a real narrowing: direct bare R2 is not in the adopted candidate grammar, but R11/counterterm routes still keep global c_bare open.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "After direct c_bare is split, the next total-c_R2_eff component is hidden exchange: 1/2 B^T L^-1 B. It is MTS-specific and may be killed by a positivity plus no-linear-vertex theorem, or converted to a finite source/body-charge bound.",
            "first_task": "Try to prove B_hidden=0 on the physical local subspace for memory/fibre response.",
            "fallback_task": "If a vertex survives, stage its finite coefficient and projection to mu/lambda/alpha as nonclaim.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(ts: str, audit: list[dict[str, Any]], split: list[dict[str, Any]], finite: list[dict[str, Any]], gates: list[dict[str, Any]]) -> None:
    doc = f"""# 4725 - No-Bare-R2 Parent Grammar Proof or cBare Finite Row

Generated: `{ts}`

## Purpose

4725 attacks the bare `R^2/f(R)` component of `c_R2_eff_total`. The aim is not to circle the blocker, but to decide whether the parent action language actually forbids a bare curvature-square slot or whether a finite `c_bare` row must survive.

## What Actually Moved

- The older action documents support an EH-plus-MTS-potential effective action with no explicit direct bare `R^2` term.
- The stronger statement is only candidate-branch safe: the 3890 grammar excludes a direct bare slot, but it is not global corpus adoption.
- Global `c_bare` still survives through `S_R11`/non-EH factorization and possible counterterm/singular-running routes.
- Therefore `c_bare` is now split rather than vaguely missing: `c_bare_global = c_bare_direct + c_R11_curvature_square + c_counterterm`.

## Grammar Audit

{bullets(audit, "audit_id", "verdict")}

## cBare Split

{bullets(split, "split_id", "current_value")}

## Finite Rows

{bullets(finite, "row_id", "formula_or_value")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 741 - No-Bare-R2 Parent Grammar Proof or cBare Finite Row

Generated: `{ts}`

## Result

The direct bare curvature-square slot is absent only inside the 3890 candidate grammar. That is useful: `c_bare_direct=0` is a candidate-branch result, not a tuned closure. But it is not enough for total `c_bare=0`, because `S_R11` and counterterm/singular-running routes can still regenerate curvature-square response.

## Current Split

`c_bare_global = c_bare_direct + c_R11_curvature_square + c_counterterm`.

`c_bare_direct=0` is candidate-branch only. `c_R11_curvature_square` and `c_counterterm` remain missing zero/value rows.

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
- Derivation gain: `c_bare` is no longer one vague missing coefficient; the direct bare R2 slot is zero only in the candidate grammar while R11 and counterterm slots remain live.
- Finite row: `c_bare_global = c_bare_direct + c_R11_curvature_square + c_counterterm`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: narrows the bare R2 problem into direct grammar, R11 residual and counterterm subslots, preventing false total-zero promotion.
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

- The direct bare `R^2/f(R)` slot is excluded only inside the 3890 candidate grammar.
- Global `c_bare` was split into direct, R11/non-EH and counterterm/singular-running subslots.
- A finite nonclaim `c_bare_global` row now exists for the surviving bare component of `c_R2_eff_total`.

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
        "claim": "4725 splits the bare R2 component: the direct bare slot is absent only in the 3890 candidate grammar, while global c_bare remains live through R11/non-EH and counterterm channels.",
        "current_evidence": "Generated source register, no-bare grammar audit, c_bare split rows, finite c_bare source rows, c_bare-to-mu projection rows, gates, firewalls, decision, status, next target and validation.",
        "status": "candidate_direct_bare_zero_global_cbare_finite_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating an effective EH action or candidate grammar branch as a global parent no-bare-R2 theorem.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "R11/non-EH residual factorization or counterterms can regenerate curvature-square response.",
        "title": "No-bare-R2 parent grammar proof or cBare finite row",
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
    audit: list[dict[str, Any]],
    split: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        GRAMMAR_AUDIT_CSV,
        CBARE_SPLIT_CSV,
        CBARE_FINITE_CSV,
        PROJECTION_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    statuses = {row["status"] for row in split}
    finite_quantities = {row["quantity"] for row in finite}
    projection_status = ";".join(row["current_status"] for row in projections)
    checks = [
        ("VAL4725_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4725 source paths exist"),
        ("VAL4725_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4725 source needles found"),
        ("VAL4725_2_candidate_direct_zero_split", "CANDIDATE_BRANCH_ZERO_NOT_GLOBAL" in statuses, "candidate direct c_bare zero split written"),
        ("VAL4725_3_R11_counterterm_survive", "LIVE_RESIDUAL_SLOT" in statuses and "LIVE_COUNTERTERM_SLOT" in statuses, "R11 and counterterm c_bare survivors retained"),
        ("VAL4725_4_global_finite_row", "c_bare_global" in finite_quantities, "global c_bare finite row written"),
        ("VAL4725_5_projection_nonclaim", "MISSING_NORMALIZATION_AND_VALUE" in projection_status and all(not bool(row["valid_for_claim"]) for row in projections), "c_bare-to-mu projection rows remain nonclaim"),
        ("VAL4725_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4725_0_sources_verified", "GATE4725_2_candidate_direct_slot_zero"}), "all broad claim gates remain closed; candidate-only gate is not claim"),
        ("VAL4725_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4725_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4725_9_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4726 next target"),
        ("VAL4725_10_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4725 CSV files parse cleanly"),
        ("VAL4725_11_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
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
            "check_id": "VAL4725_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4725 no-bare-R2 parent grammar or c_bare finite-row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    audit = grammar_audit_rows(ts)
    split = cbare_split_rows(ts)
    finite = cbare_finite_rows(ts)
    projections = projection_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(GRAMMAR_AUDIT_CSV, audit)
    write_csv(CBARE_SPLIT_CSV, split)
    write_csv(CBARE_FINITE_CSV, finite)
    write_csv(PROJECTION_CSV, projections)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, audit, split, finite, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, audit, split, finite, projections, gates, ts))


if __name__ == "__main__":
    main()
