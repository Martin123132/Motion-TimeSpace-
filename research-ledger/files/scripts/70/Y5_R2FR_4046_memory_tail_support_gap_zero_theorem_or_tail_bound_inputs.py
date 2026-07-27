from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4046-Y5-R2FR-memory-tail-support-gap-zero-theorem-or-tail-bound-inputs.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4046_SOURCE_REGISTER.csv",
    "local_reset_signature": SOURCE_DIR / "P8_Y5_R2FR_4046_LOCAL_RESET_MEMORY_SIGNATURE.csv",
    "tail_zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4046_TAIL_ZERO_THEOREM.csv",
    "fallback_suppression": SOURCE_DIR / "P8_Y5_R2FR_4046_FALLBACK_SUPPRESSION_BOUND.csv",
    "cz_closure": SOURCE_DIR / "P8_Y5_R2FR_4046_CZ_CLOSURE_STATUS.csv",
    "local_gr_gate": SOURCE_DIR / "P8_Y5_R2FR_4046_LOCAL_GR_GATE_UPDATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4046_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4046_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4046_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4046_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4046_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4046_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4046_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for item in rows:
        for key in item:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4046_0", ROOT / "4045-Y5-R2FR-cZ-kernel-wall-zero-theorem-or-first-bound-values.md", "Delta_cZ_selected = A_tail", "4045 reduced cZ to tail-only"),
        ("SRC4046_1", SOURCE_DIR / "P8_Y5_R2FR_4045_TAIL_KERNEL_GATE.csv", "P_loc K_mem vanishes on compact stationary collar", "4045 exact tail gate"),
        ("SRC4046_2", SOURCE_DIR / "P8_Y5_R2FR_3931_HISTORY_NONLOCAL_PARENT_SIGNATURE.csv", "local reset/no-incoming branch", "3931 local reset/no-incoming memory signature"),
        ("SRC4046_3", SOURCE_DIR / "P8_Y5_R2FR_3931_HISTORY_NONLOCAL_ZERO_RESULT.csv", "B_nonlocal_kernel", "3931 zero result rows"),
        ("SRC4046_4", SOURCE_DIR / "P8_Y5_R2FR_3931_HISTORY_SUPPRESSION_BOUND_ROWS.csv", "||X_mem(t)|| <= exp(-gamma_mem Delta t)||X_mem(t0)||", "fallback history suppression law"),
        ("SRC4046_5", SOURCE_DIR / "P8_Y5_R2FR_3893_MEMORY_SILENCE_THEOREM_OR_BOUND.csv", "If X is parent-owned, A^ij>0", "positive memory operator theorem target"),
        ("SRC4046_6", SOURCE_DIR / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "Exact history silence needs no incoming memory data", "history zero condition"),
        ("SRC4046_7", SOURCE_DIR / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "lambda_gap := a_min C_P/L_D^2 + m_min^2", "gap and suppression law"),
        ("SRC4046_8", SOURCE_DIR / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_INPUT_SCHEMA.csv", "incoming memory amplitude", "fallback input schema"),
        ("SRC4046_9", SOURCE_DIR / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv", "Dq memory zero", "memory verticality/readout guard"),
        ("SRC4046_10", SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv", "No local domain preferred-momentum flux is generated.", "projector/domain source closure needed by 3931"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def local_reset_signature_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "signature_id": "LRS4046_0_branch",
            "clause": "local isolated retarded/reset branch",
            "mathematical_statement": "X_mem(t0)=0, J_open+B_lift=0 on the source-free local collar, B_nonlocal_kernel=0, lambda_gap>0, gamma_mem>=0",
            "effect": "local stationary PPN/Newton branch has no incoming homogeneous memory and no open local memory source",
            "branch_value": "adopted_private_selected_branch",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "signature_id": "LRS4046_1_no_incoming",
            "clause": "no incoming homogeneous memory",
            "mathematical_statement": "||X_mem(t0)||=0",
            "effect": "retarded isolated local solution is not seeded by arbitrary past cosmological memory",
            "branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "signature_id": "LRS4046_2_no_open_source",
            "clause": "no open source after local closures",
            "mathematical_statement": "sup||J_open+B_lift||=0 after 4038 boundary and 4043 projector/domain closure",
            "effect": "memory source term vanishes in compact local collar",
            "branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "signature_id": "LRS4046_3_nonlocal_kernel",
            "clause": "compact local kernel silence",
            "mathematical_statement": "B_nonlocal_kernel=0 for local stationary compact branch",
            "effect": "nonlocal tail does not inject compact local force/current",
            "branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "signature_id": "LRS4046_4_gap_guard",
            "clause": "positive/coercive guard",
            "mathematical_statement": "lambda_gap:=a_min C_P/L_D^2 + m_min^2 > 0 or reset branch uses zero-source solution",
            "effect": "prevents unforced memory zero mode from masquerading as local force hair",
            "branch_value": "positive_or_reset_zero_solution",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "signature_id": "LRS4046_5_cosmology_guard",
            "clause": "local reset is not global memory deletion",
            "mathematical_statement": "local compact retarded/no-incoming condition applies only to isolated PPN/Newton collar; FLRW/open systems keep suppression rows",
            "effect": "keeps cosmology/galaxy memory branch alive",
            "branch_value": "guard_active",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def tail_zero_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TZT4046_0_tail_state",
            "premise": "4045 reduced cZ to tail-only",
            "formula": "Delta_cZ_selected=A_tail",
            "result": "only memory/history kernel tail needs closure in selected branch",
            "status": "PREMISE_ACCEPTED_PRIVATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TZT4046_1_zero_amplitude",
            "premise": "local reset/no-incoming signature",
            "formula": "||X_mem(t)|| <= exp(-gamma_mem Delta t)*0 + (1-exp(-gamma_mem Delta t))*0/lambda_gap = 0",
            "result": "X_mem=0 in compact local collar",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TZT4046_2_zero_observable",
            "premise": "X_mem=0 plus compact local kernel silence",
            "formula": "|Delta O_i| <= K_i||X_mem|| + K_i_grad||grad X_mem|| = 0",
            "result": "A_tail=0 and Delta_cZ_selected=0",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TZT4046_3_verticality_guard",
            "premise": "memory variable is local/private and q-basic readout has no direct disformal memory slot",
            "formula": "Dq_parent[partial_Xmem]=0 and DObs_e[partial_Xmem]=0",
            "result": "the zero is not achieved by hiding memory in the observed metric/readout",
            "status": "READOUT_GUARD_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "TZT4046_4_scope_guard",
            "premise": "local reset/no-incoming branch is a boundary-condition branch",
            "formula": "local PPN/Newton branch != FLRW/open-memory branch",
            "result": "no global memory/no-cosmology claim",
            "status": "GLOBAL_MEMORY_NOT_ZEROED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_suppression_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "fallback_id": "FSB4046_0_static",
            "used_if": "no-reset branch or open source is allowed",
            "formula": "||X_mem|| <= (||J_open|| + B_lift)/lambda_gap",
            "required_inputs": "a_min, C_P/L_D^2, m_min^2, ||J_open||, B_lift",
            "claim_status": "NONCLAIM_VALUES_MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "fallback_id": "FSB4046_1_dynamic",
            "used_if": "incoming memory or finite relaxation interval is allowed",
            "formula": "||X_mem(t)|| <= exp(-gamma_mem Delta t)||X_mem(t0)|| + (1-exp(-gamma_mem Delta t))sup||J_open+B_lift||/lambda_gap",
            "required_inputs": "gamma_mem, Delta t, X_mem(t0), source supremum, lambda_gap",
            "claim_status": "NONCLAIM_VALUES_MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "fallback_id": "FSB4046_2_observable",
            "used_if": "tail amplitude is finite not zero",
            "formula": "|Delta O_i| <= K_i||X_mem|| + K_i_grad||grad X_mem||",
            "required_inputs": "arena-specific K_i, K_i_grad, and gradient bound",
            "claim_status": "NONCLAIM_VALUES_MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def cz_closure_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "closure_id": "CZC4046_0_direct_boundary_gamma",
            "component": "J_Z^direct + J_Z^boundary + J_Z^Gamma",
            "status": "ZERO_CARRIED_FROM_4037_4039",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "closure_id": "CZC4046_1_wall",
            "component": "J_Z^selector_wall",
            "status": "ZERO_CARRIED_FROM_4045",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "closure_id": "CZC4046_2_tail",
            "component": "J_Z^history_tail",
            "status": "ZERO_IN_PRIVATE_SELECTED_LOCAL_RESET_BRANCH",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "closure_id": "CZC4046_3_total",
            "component": "Delta_cZ_selected",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "selected_branch_value": "0",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "closure_id": "CZC4046_4_fallback",
            "component": "Delta_cZ_fallback",
            "status": "SUPPRESSION_BOUND_REQUIRED_IF_LOCAL_RESET_BRANCH_REJECTED",
            "selected_branch_value": "not_applicable",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def local_gr_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "LGG4046_0_cZ",
            "gate": "cZ selected-branch local residual",
            "before_4046": "Delta_cZ_tail live",
            "after_4046": "Delta_cZ_selected=0 in private local reset/no-incoming branch",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "LGG4046_1_remaining",
            "gate": "remaining public local-GR blockers",
            "before_4046": "Delta_cZ_tail; Delta_cnorm_envelope; Parent_packet_adoption",
            "after_4046": "Delta_cnorm_envelope; Parent_packet_adoption; cZ fallback if reset branch rejected",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4046_0_selected_reset_branch",
            "verdict": "CZ_TAIL_ZERO_IN_PRIVATE_SELECTED_RESET_BRANCH",
            "result": "With no incoming homogeneous memory, no open local source, compact local kernel silence, and positive/reset gap guard, A_tail=0 and Delta_cZ_selected=0.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4046_1_if_reset_rejected",
            "verdict": "MEMORY_SUPPRESSION_BOUND_ROWS_REQUIRED",
            "result": "If incoming/open memory is allowed, use the 3895/3931 suppression law with explicit source/gap/projection constants.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4046_0_adopt_reset_local",
            "decision": "adopt local reset/no-incoming history branch for private isolated PPN/Newton systems",
            "reason": "this is the local retarded isolated-source analogue of fixed no-incoming radiation/boundary data and does not erase cosmological memory",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4046_1_cZ_closed_private",
            "decision": "close Delta_cZ in the private selected local branch",
            "reason": "4045 wall zero plus 3931 history/nonlocal zero closes both pieces of the 4040 envelope",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4046_2_next",
            "decision": "attack Delta_cnorm_envelope next",
            "reason": "after cZ closes privately, c_norm derivative hair becomes the main live physics envelope before parent action adoption",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4046_0_cZ_private_zero",
            "claim": "Delta_cZ_selected is zero in the private isolated local reset/no-incoming branch",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "private selected local PPN/Newton branch only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4046_1_global_memory_zero",
            "claim": "MTS memory is globally zero",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "false/not claimed; FLRW/open memory branches remain active",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4046_2_full_local_GR",
            "claim": "full public local-GR/PPN pass",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked by c_norm derivative hair and parent packet adoption",
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4046_0_cnorm",
            "symbol": "Delta_cnorm_envelope",
            "residual": "nonconstant source-normalization derivative hair",
            "current_route": "next target: prove D_a ln G_obs, D_a ln M_eff, and D_a ln(1+epsilon_mu) vanish or fill local bounds",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4046_1_parent",
            "symbol": "Parent_packet_adoption",
            "residual": "private selected local packet not yet final parent-action theorem",
            "current_route": "formal parent action variation audit after c_norm derivative hair closes",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4046_2_cZ_fallback",
            "symbol": "Delta_cZ_fallback_if_reset_rejected",
            "residual": "finite memory suppression bound if local reset/no-incoming branch is rejected",
            "current_route": "not active in selected branch; suppression inputs staged",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4046_0",
            "next_doc": "4047-Y5-R2FR-cnorm-derivative-hair-zero-or-local-bound-scorecard.md",
            "next_script": "scripts/Y5_R2FR_4047_cnorm_derivative_hair_zero_or_local_bound_scorecard.py",
            "why": "cZ is now closed in the selected private branch, so c_norm derivative hair is the main live local physics envelope",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4046",
            "status": "CZ_ZERO_PRIVATE_SELECTED_RESET_BRANCH_CNORM_NEXT",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    source_hits = sum(1 for item in sources if item["exists"] and item["needle_found"])
    return "\n".join(
        [
            "# 4046 - Memory Tail Support/Gap Zero Theorem Or Tail Bound Inputs",
            "",
            f"- Timestamp: `{ts}`",
            "- Status: `private_nonclaim_checkpoint`",
            "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
            f"- Source needles found: `{source_hits}/{len(sources)}`.",
            "",
            "## What Actually Moved",
            "",
            "4046 closes the selected-branch `c_Z` tail using the local reset/no-incoming history branch from 3931.",
            "",
            "4045 had reduced the residual to `Delta_cZ_selected = A_tail`. In the isolated local PPN/Newton branch, impose:",
            "",
            "`X_mem(t0)=0`, `J_open+B_lift=0`, `B_nonlocal_kernel=0`, `lambda_gap>0`, and `gamma_mem>=0`.",
            "",
            "Then the suppression law gives:",
            "",
            "`||X_mem(t)|| <= exp(-gamma_mem Delta t)*0 + (1-exp(-gamma_mem Delta t))*0/lambda_gap = 0`.",
            "",
            "Therefore `A_tail=0` and `Delta_cZ_selected=0` in the private selected local branch.",
            "",
            "## What Is Not Being Claimed",
            "",
            "This is not global memory deletion. FLRW, cosmology, galaxies, and open/history-dependent systems retain the suppression branch. If the local reset/no-incoming branch is rejected, the finite tail bound rows remain active.",
            "",
            "## Current Verdict",
            "",
            "- Current evaluator result: `CZ_TAIL_ZERO_IN_PRIVATE_SELECTED_RESET_BRANCH`.",
            "- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4046`.",
            "- Remaining live local residuals: `Delta_cnorm_envelope`, `Parent_packet_adoption`, plus `Delta_cZ_fallback_if_reset_rejected`.",
            "",
            "## Next Target",
            "",
            "- `4047-Y5-R2FR-cnorm-derivative-hair-zero-or-local-bound-scorecard.md`",
            "- `scripts/Y5_R2FR_4047_cnorm_derivative_hair_zero_or_local_bound_scorecard.py`",
            "",
        ]
    )


def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def all_private(*tables: Iterable[Dict[str, object]]) -> bool:
    return all(item.get("valid_for_public_claim") is False for table in tables for item in table)


def validation_rows(
    sources: List[Dict[str, object]],
    signature: List[Dict[str, object]],
    theorem: List[Dict[str, object]],
    fallback: List[Dict[str, object]],
    closure: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH)]
    return [
        row("VAL4046_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4046_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4046_02_signature_count", len(signature) == 6, "six local reset signature clauses present"),
        row("VAL4046_03_no_incoming", any(item["signature_id"] == "LRS4046_1_no_incoming" and item["branch_value"] == "0" for item in signature), "no incoming memory clause present"),
        row("VAL4046_04_no_open_source", any(item["signature_id"] == "LRS4046_2_no_open_source" and item["branch_value"] == "0" for item in signature), "no open source clause present"),
        row("VAL4046_05_nonlocal_kernel_zero", any(item["signature_id"] == "LRS4046_3_nonlocal_kernel" and item["branch_value"] == "0" for item in signature), "nonlocal kernel zero clause present"),
        row("VAL4046_06_cosmology_guard", any(item["signature_id"] == "LRS4046_5_cosmology_guard" for item in signature), "cosmology/open memory guard present"),
        row("VAL4046_07_tail_state", any(item["theorem_id"] == "TZT4046_0_tail_state" for item in theorem), "tail-only premise present"),
        row("VAL4046_08_zero_amplitude", any(item["theorem_id"] == "TZT4046_1_zero_amplitude" and item["status"] == "ZERO_IN_PRIVATE_SELECTED_BRANCH" for item in theorem), "zero amplitude theorem present"),
        row("VAL4046_09_zero_observable", any(item["theorem_id"] == "TZT4046_2_zero_observable" and item["status"] == "ZERO_IN_PRIVATE_SELECTED_BRANCH" for item in theorem), "zero observable theorem present"),
        row("VAL4046_10_verticality_guard", any(item["theorem_id"] == "TZT4046_3_verticality_guard" for item in theorem), "verticality/readout guard present"),
        row("VAL4046_11_fallback_static", any(item["fallback_id"] == "FSB4046_0_static" for item in fallback), "static fallback bound present"),
        row("VAL4046_12_fallback_dynamic", any(item["fallback_id"] == "FSB4046_1_dynamic" for item in fallback), "dynamic fallback bound present"),
        row("VAL4046_13_cZ_total_zero", any(item["closure_id"] == "CZC4046_3_total" and item["selected_branch_value"] == "0" for item in closure), "Delta_cZ selected total zero"),
        row("VAL4046_14_fallback_retained", any(item["closure_id"] == "CZC4046_4_fallback" for item in closure), "cZ fallback retained"),
        row("VAL4046_15_gate_cZ", any(item["gate_id"] == "LGG4046_0_cZ" and "Delta_cZ_selected=0" in item["after_4046"] for item in gates), "cZ gate updated"),
        row("VAL4046_16_evaluator_zero", any(item["verdict"] == "CZ_TAIL_ZERO_IN_PRIVATE_SELECTED_RESET_BRANCH" for item in evaluator), "cZ tail zero evaluator present"),
        row("VAL4046_17_evaluator_fallback", any(item["verdict"] == "MEMORY_SUPPRESSION_BOUND_ROWS_REQUIRED" for item in evaluator), "fallback evaluator present"),
        row("VAL4046_18_decision_next", any(item["decision_id"] == "DEC4046_2_next" for item in decisions), "next decision present"),
        row("VAL4046_19_private_claim_scoped", any(item["claim_id"] == "CLAIM4046_0_cZ_private_zero" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "private cZ zero claim scoped internal"),
        row("VAL4046_20_global_memory_blocked", any(item["claim_id"] == "CLAIM4046_1_global_memory_zero" and item["allowed"] is False for item in claims), "global memory zero blocked"),
        row("VAL4046_21_local_GR_blocked", any(item["claim_id"] == "CLAIM4046_2_full_local_GR" and item["allowed"] is False for item in claims), "full local-GR claim blocked"),
        row("VAL4046_22_remaining_cnorm", any(item["symbol"] == "Delta_cnorm_envelope" for item in remaining), "c_norm remains next"),
        row("VAL4046_23_remaining_parent", any(item["symbol"] == "Parent_packet_adoption" for item in remaining), "parent adoption remains"),
        row("VAL4046_24_next_target", bool(next_target and "4047" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4046_25_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4046_26_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4046_27_script_compiles", compile_ok, "script compiles"),
        row("VAL4046_28_private_guard", all_private(signature, theorem, fallback, closure, gates, evaluator, decisions, remaining), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    signature = local_reset_signature_rows(ts)
    theorem = tail_zero_theorem_rows(ts)
    fallback = fallback_suppression_rows(ts)
    closure = cz_closure_rows(ts)
    gates = local_gr_gate_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    remaining = remaining_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["local_reset_signature"], signature)
    write_csv(OUTPUTS["tail_zero_theorem"], theorem)
    write_csv(OUTPUTS["fallback_suppression"], fallback)
    write_csv(OUTPUTS["cz_closure"], closure)
    write_csv(OUTPUTS["local_gr_gate"], gates)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(
        sources,
        signature,
        theorem,
        fallback,
        closure,
        gates,
        evaluator,
        decisions,
        claims,
        remaining,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4046 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
