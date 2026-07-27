from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3827"
BRANCH = "MTS_R2FR_Y5_LOCAL_KERNEL_SCORECARD_TO_FIRST_SMOKE_TEST_RUNNER_3827"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3826 = PCW / "3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md"
CSV_3826_SCORECARD = OUT / "P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv"
CSV_3826_ARENAS = OUT / "P8_Y5_R2FR_3826_ARENA_CLOSURE_MATRIX.csv"
CSV_3826_RESIDUALS = OUT / "P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv"
CSV_3826_ROADMAP = OUT / "P8_Y5_R2FR_3826_ZERO_OR_SOURCE_ROW_ROADMAP.csv"
CSV_3826_GATES = OUT / "P8_Y5_R2FR_3826_CLAIM_GATES.csv"
CSV_3826_VALIDATION = OUT / "P8_Y5_BRR545_3826_VALIDATION.csv"
CSV_3822_LEDGER = OUT / "P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv"
CSV_3822_TEST = OUT / "P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv"
CSV_3825_FIRST = OUT / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3827_SOURCE_REGISTER.csv",
    "dry_inputs": OUT / "P8_Y5_R2FR_3827_LOCAL_ARENA_DRY_RUN_INPUTS.csv",
    "smoke_results": OUT / "P8_Y5_R2FR_3827_SMOKE_RUN_RESULTS.csv",
    "failures": OUT / "P8_Y5_R2FR_3827_FAILURE_MODE_LEDGER.csv",
    "priority_queue": OUT / "P8_Y5_R2FR_3827_PRIORITY_SOURCE_FILL_QUEUE.csv",
    "ppn_first_rows": OUT / "P8_Y5_R2FR_3827_PPN_READOUT_TAIL_FIRST_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3827_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3827_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3827_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3827_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3827_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3827_0_3826_doc", P_3826, "Compact Exterior Source-Kernel Closure Scorecard"),
    ("SRC3827_1_3826_scorecard", CSV_3826_SCORECARD, "KSC3826_8_compact_exterior_kernel_total"),
    ("SRC3827_2_3826_arena_matrix", CSV_3826_ARENAS, "ARENA3826_2_PPN"),
    ("SRC3827_3_3826_residuals", CSV_3826_RESIDUALS, "R3826_8_kernel_total"),
    ("SRC3827_4_3826_roadmap", CSV_3826_ROADMAP, "ROAD3826_0_dry_run_runner"),
    ("SRC3827_5_3826_gates", CSV_3826_GATES, "GATE3826_3_local_GR_Newton_claim"),
    ("SRC3827_6_3826_validation", CSV_3826_VALIDATION, "VAL3826_5_3827_next"),
    ("SRC3827_7_3822_local_ledger", CSV_3822_LEDGER, "ARENA3822_0_R10_lab"),
    ("SRC3827_8_3822_test_rows", CSV_3822_TEST, "LTR3822_0_R10_alpha_lambda"),
    ("SRC3827_9_3825_first_rows", CSV_3825_FIRST, "FSR3825_0_B_zero_flux"),
]

ARENA_ALIAS = {
    "ARENA3826_0_R10": "R10",
    "ARENA3826_1_WEP": "WEP",
    "ARENA3826_2_PPN": "PPN",
    "ARENA3826_3_clock": "clock",
    "ARENA3826_4_orbital": "orbital",
    "ARENA3826_5_EM": "EM",
}

MODE_BY_STATUS = {
    "DRY_RUN_ONLY": "PASS_SCHEMA_CLAIM_BLOCKED",
    "BOUND_INPUT_REQUIRED": "PASS_SCHEMA_INPUT_BLOCKED",
    "BLOCKED_NEXT_PROOF": "PASS_SCHEMA_PROOF_BLOCKED",
    "SOURCE_ROW_READY_NONCLAIM": "PASS_SCHEMA_SOURCE_ROWS_NONCLAIM",
    "PRODUCT_ONLY_GM_GUARD": "PASS_SCHEMA_ANTI_CIRCULARITY_GUARD",
    "EXTENSION_NONCLAIM": "PASS_SCHEMA_EXTENSION_BLOCKED",
}


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


def has_any_missing_marker(row: dict[str, str]) -> bool:
    text = " ".join(str(value) for value in row.values())
    return "MISSING_" in text or "placeholder" in text.lower() or "not yet" in text.lower()


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
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
                "role": "input_for_local_arena_dry_run_runner",
                "claim_use": "schema_and_failure_mode_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def matching_clause_ids(required_clause: str, scorecard: list[dict[str, str]]) -> list[str]:
    return [row["clause_id"] for row in scorecard if row.get("clause_id", "").startswith(required_clause)]


def split_required_clauses(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(";") if chunk.strip()]


def dry_input_rows(
    arenas: list[dict[str, str]],
    scorecard: list[dict[str, str]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arena in arenas:
        arena_id = arena["arena_id"]
        required = split_required_clauses(arena["required_kernel_clauses"])
        resolved = []
        missing = []
        for clause in required:
            matches = matching_clause_ids(clause, scorecard)
            if matches:
                resolved.extend(matches)
            else:
                missing.append(clause)
        rows.append(
            {
                "dry_input_id": f"DRY3827_{ARENA_ALIAS.get(arena_id, arena_id)}",
                "arena_id": arena_id,
                "arena": arena["arena"],
                "required_kernel_clause_prefixes": ";".join(required),
                "resolved_kernel_clauses": ";".join(resolved),
                "missing_kernel_clause_prefixes": ";".join(missing),
                "kernel_clause_resolution": "PASS" if not missing else "FAIL",
                "input_mode": arena["first_usable_mode"],
                "declared_status": arena["current_status"],
                "declared_claim_allowed": arena["claim_allowed"],
                "blocking_inputs": arena["blocking_inputs"],
                "timestamp_utc": timestamp,
            }
        )
    return rows


def smoke_result_rows(
    arenas: list[dict[str, str]],
    dry_inputs: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    dry_by_arena = {row["arena_id"]: row for row in dry_inputs}
    for arena in arenas:
        arena_id = arena["arena_id"]
        declared_status = arena["current_status"]
        kernel_ok = dry_by_arena[arena_id]["kernel_clause_resolution"] == "PASS"
        expected_claim_block = str(arena["claim_allowed"]).lower() == "false"
        smoke_status = MODE_BY_STATUS.get(declared_status, "FAIL_UNKNOWN_STATUS")
        if not kernel_ok:
            smoke_status = "FAIL_MISSING_KERNEL_CLAUSE"
        elif not expected_claim_block:
            smoke_status = "FAIL_CLAIM_FLAG_OPEN"
        rows.append(
            {
                "smoke_id": f"SMOKE3827_{ARENA_ALIAS.get(arena_id, arena_id)}",
                "arena_id": arena_id,
                "arena": arena["arena"],
                "kernel_input_resolution": dry_by_arena[arena_id]["kernel_clause_resolution"],
                "smoke_status": smoke_status,
                "claim_allowed": False,
                "claim_decision": "BLOCKED_NONCLAIM_DRY_RUN",
                "actionable_result": arena["next_test_action"],
                "blocking_inputs": arena["blocking_inputs"],
                "timestamp_utc": timestamp,
            }
        )
    return rows


def failure_mode_rows(
    smoke_results: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    base_rows = [
        {
            "failure_id": "FAIL3827_0_R10_source_numerator",
            "arena_id": "ARENA3826_0_R10",
            "failure_mode": "numeric MTS alpha numerator is absent or nonclaim",
            "blocks": "R10 alpha(lambda) claim",
            "first_fix": "derive or source K_X Qbar_XH qbar_XT numerator and keep row valid_for_claim=false until provenance exists",
            "severity": "HIGH",
        },
        {
            "failure_id": "FAIL3827_1_boundary_MHref",
            "arena_id": "ARENA3826_0_R10;ARENA3826_3_clock;ARENA3826_5_EM",
            "failure_mode": "boundary/reference lock and M_H_ref denominator rows are source-ready but not claim-valid",
            "blocks": "R10, clock, EM, and local-source normalization claims",
            "first_fix": "fill FSR3825 rows or prove exact boundary/reference zero using the same compact exterior source",
            "severity": "HIGH",
        },
        {
            "failure_id": "FAIL3827_2_PPN_readout_tail",
            "arena_id": "ARENA3826_2_PPN;ARENA3826_4_orbital;ARENA3826_3_clock;ARENA3826_1_WEP",
            "failure_mode": "metric readout descent has no parent-signed gamma/beta/preferred-frame residual vector",
            "blocks": "local GR/Newton recovery claim",
            "first_fix": "derive or bound R_PPN_readout_tail with gamma-1, beta-1, alpha1, alpha2, clock, and orbital subrows",
            "severity": "CRITICAL",
        },
        {
            "failure_id": "FAIL3827_3_GM_smuggling_guard",
            "arena_id": "ARENA3826_4_orbital",
            "failure_mode": "orbital mu=GM remains validation-output product evidence, not independent source normalization",
            "blocks": "Newton constant/source-mass derivation claim",
            "first_fix": "obtain independent M/G split or derive source normalization without using fitted orbital mu as input",
            "severity": "HIGH",
        },
        {
            "failure_id": "FAIL3827_4_WEP_material_stress",
            "arena_id": "ARENA3826_1_WEP",
            "failure_mode": "composition/material stress normalizer is not source-owned",
            "blocks": "WEP composition claim",
            "first_fix": "separate universal compact-kernel terms from material-dependent stress residuals",
            "severity": "MEDIUM",
        },
        {
            "failure_id": "FAIL3827_5_EM_Poynting_flux",
            "arena_id": "ARENA3826_5_EM",
            "failure_mode": "Poynting/vector-wave stress route lacks same-current source ownership and boundary flux row",
            "blocks": "Maxwell/EM stress extension claim",
            "first_fix": "add Poynting flux boundary/source row under the same Pi_M and R_eq kernel",
            "severity": "MEDIUM",
        },
    ]
    smoke_status = {row["arena_id"]: row["smoke_status"] for row in smoke_results}
    rows: list[dict[str, object]] = []
    for row in base_rows:
        related_statuses = []
        for arena_id in str(row["arena_id"]).split(";"):
            related_statuses.append(f"{arena_id}:{smoke_status.get(arena_id, 'not_directly_smoked')}")
        rows.append(
            {
                **row,
                "observed_in_smoke": ";".join(related_statuses),
                "claim_allowed": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def priority_queue_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "queue_id": "QUEUE3827_0_PPN_readout_tail",
            "target": "R_PPN_readout_tail",
            "why_first": "this is the direct local GR/Newton proof edge; without it the compact kernel cannot produce PPN residuals",
            "required_rows": "gamma_minus_one; beta_minus_one; alpha1; alpha2; clock_tau; orbital_mu_guard",
            "acceptable_outcome": "derive zero route or emit finite residual vector with units, source path, and valid_for_claim=false",
            "feeds_next": "3828",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 2,
            "queue_id": "QUEUE3827_1_boundary_MHref",
            "target": "B_zero_flux; Delta_symp; M_H_ref",
            "why_first": "these rows control R10/clock/EM source normalization and prevent hidden denominator tricks",
            "required_rows": "FSR3825 boundary/reference rows with real source values or theorem-zero signatures",
            "acceptable_outcome": "source-backed nonclaim rows before any local pass language",
            "feeds_next": "3828_or_3829",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 3,
            "queue_id": "QUEUE3827_2_independent_source_ledger",
            "target": "independent source mass/scale rows",
            "why_first": "prevents fitted GM and fitted alpha from becoming hidden inputs",
            "required_rows": "M_source, G normalization, apparatus source scale, local units, provenance",
            "acceptable_outcome": "source ledger has numeric provenance while claim gates stay closed",
            "feeds_next": "local_arena_smoke_v2",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 4,
            "queue_id": "QUEUE3827_3_R10_bound_and_MTS_alpha",
            "target": "R10 alpha(lambda)",
            "why_first": "R10 can become the quickest empirical sanity check once parent numerator exists",
            "required_rows": "real bound curve; MTS numerator; lambda map; uncertainty policy",
            "acceptable_outcome": "R10 comparator runs and reports blocked/stable without claiming pass from placeholders",
            "feeds_next": "R10_smoke_v2",
            "timestamp_utc": timestamp,
        },
        {
            "priority": 5,
            "queue_id": "QUEUE3827_4_EM_Poynting_source_stress",
            "target": "EM stress/Poynting boundary row",
            "why_first": "captures Martin's wave/Poynting intuition without letting EM shortcut the local-GR source proof",
            "required_rows": "same-current EM source; Poynting flux boundary term; radiative readout naturality",
            "acceptable_outcome": "EM extension remains tied to the same compact source kernel",
            "feeds_next": "EM_extension_gate",
            "timestamp_utc": timestamp,
        },
    ]


def ppn_first_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "PPN3827_0_gamma_minus_one",
            "observable": "gamma-1",
            "required_parent_object": "metric readout descent coefficient Dg_obs/Dq_X on the compact exterior kernel",
            "symbolic_residual": "delta_gamma_MTS",
            "units": "dimensionless",
            "source_status": "MISSING_PARENT_SIGNED_READOUT",
            "valid_for_claim": False,
            "next_action": "derive zero from readout naturality or emit finite bound row",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3827_1_beta_minus_one",
            "observable": "beta-1",
            "required_parent_object": "second-order metric/source self-coupling readout",
            "symbolic_residual": "delta_beta_MTS",
            "units": "dimensionless",
            "source_status": "MISSING_SECOND_ORDER_SOURCE_COUPLING",
            "valid_for_claim": False,
            "next_action": "derive quadratic source-kernel coefficient or bound it independently",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3827_2_preferred_frame",
            "observable": "alpha1, alpha2 preferred-frame residuals",
            "required_parent_object": "local Lorentz/frame descent and no arena-tuned vector coefficient",
            "symbolic_residual": "delta_alpha1_MTS;delta_alpha2_MTS",
            "units": "dimensionless",
            "source_status": "MISSING_FRAME_DESCENT_SIGNATURE",
            "valid_for_claim": False,
            "next_action": "prove frame terms vanish or emit preferred-frame finite residual vector",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3827_3_clock_tau",
            "observable": "clock redshift/time-transport residual",
            "required_parent_object": "same source-kernel clock readout tau_clock",
            "symbolic_residual": "delta_tau_clock_MTS",
            "units": "dimensionless or seconds/second after normalization",
            "source_status": "MISSING_CLOCK_READOUT_TRANSPORT",
            "valid_for_claim": False,
            "next_action": "link tau_clock to boundary/MHref row rather than independent local-time ansatz",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3827_4_orbital_mu_guard",
            "observable": "orbital mu=GM validation residual",
            "required_parent_object": "independent source normalization separate from fitted mu",
            "symbolic_residual": "delta_mu_orbital_guard_MTS",
            "units": "m^3 s^-2 only as output comparison",
            "source_status": "PRODUCT_ONLY_GM_GUARD",
            "valid_for_claim": False,
            "next_action": "keep mu as output check until independent M/G split exists",
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(smoke_results: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3827_0_runner_executes",
            "gate": "dry-run runner emits one result per local arena",
            "status": "PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": f"{len(smoke_results)} local arena smoke rows emitted",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3827_1_no_claim_pass",
            "gate": "no dry-run result can be interpreted as a physics pass",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "all results are schema, input-blocked, proof-blocked, source-row, guard, or extension modes",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3827_2_local_GR_Newton",
            "gate": "local GR/Newton recovery claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "R_PPN_readout_tail remains missing and is selected as 3828",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3827_3_R10",
            "gate": "R10 alpha(lambda) claim",
            "status": "BLOCKED_DRY_RUN_ONLY",
            "claim_allowed": False,
            "reason": "real MTS numerator and boundary/MHref rows are still absent",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3827_4_EM",
            "gate": "Maxwell/EM stress or Poynting claim",
            "status": "BLOCKED_EXTENSION_NONCLAIM",
            "claim_allowed": False,
            "reason": "Poynting flux/source-current boundary row is not yet parent-owned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3827_5_next_derivation",
            "gate": "next target prioritizes derivation over more passive ledgering",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "3828 targets PPN readout-tail descent or finite residual vector",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3827_0_testing_started",
            "decision": "local testing has started in dry-run mode",
            "basis": "3827 resolves required kernel clauses for six arenas and reports concrete failure modes",
            "consequence": "future work can now distinguish schema failure, missing source inputs, and missing derivation",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3827_1_not_yet_claimable",
            "decision": "no local arena is claimable from the dry run",
            "basis": "all generated claim_allowed flags remain false",
            "consequence": "the project avoids post-hoc local-GR claims while still moving toward tests",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3827_2_next_derivation",
            "decision": "go after R_PPN_readout_tail next",
            "basis": "it is the highest-severity blocker connecting MTS to local GR/Newton and PPN observables",
            "consequence": "3828 should derive zero conditions or emit first finite residual vector rows",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3827_0",
            "next_checkpoint": "3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md",
            "script": "scripts/Y5_R2FR_3828_PPN_readout_tail_descent_or_first_residual_vector_bound.py",
            "objective": "derive or cleanly bound R_PPN_readout_tail for gamma-1, beta-1, preferred-frame, clock, and orbital residuals using the same compact exterior source kernel, without arena-tuned readout coefficients",
            "reason": "3827 shows this is the critical proof edge between the compact source kernel and local Newton/GR recovery",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_LOCAL_DRY_RUN",
            "claim": "no R10/WEP/PPN/clock/orbital/EM/Newton/local-GR claim",
            "summary": "3827 runs the 3826 scorecard as six local dry-run smoke checks, emits concrete failure modes, and selects R_PPN_readout_tail as the next derivation target.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    smoke_results: list[dict[str, object]],
    failures: list[dict[str, object]],
    priority_queue: list[dict[str, object]],
    ppn_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3827 — Local Kernel Scorecard To First Smoke-Test Runner

Private checkpoint. This is the first runnable local-arena dry run from the 3826 compact-exterior source kernel. It deliberately does not claim any physics pass.

Generated: `{timestamp}`

## What Ran

The runner loaded the 3826 kernel scorecard, arena closure matrix, residual bundle, and roadmap, then checked that each local arena resolves its declared kernel clauses. The output is not a fit. It is a schema/failure-mode smoke test.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Smoke Results

{markdown_table(smoke_results, ["smoke_id", "arena", "kernel_input_resolution", "smoke_status", "claim_allowed", "blocking_inputs"])}

## Failure Mode Ledger

{markdown_table(failures, ["failure_id", "severity", "failure_mode", "blocks", "first_fix"])}

## Priority Source-Fill Queue

{markdown_table(priority_queue, ["priority", "queue_id", "target", "why_first", "acceptable_outcome"])}

## PPN Readout-Tail First Rows

{markdown_table(ppn_rows, ["row_id", "observable", "symbolic_residual", "source_status", "valid_for_claim", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3827 moves the project from prose blockers to executable dry-run blockers:

- all six local arenas resolve their 3826 kernel clauses;
- every arena remains nonclaim;
- the local-GR/Newton edge is now sharply identified as `R_PPN_readout_tail`;
- R10 and EM are not discarded, but they are downstream of source numerator/boundary/current rows;
- orbital `mu=GM` remains a guardrail output, not an input.

Next target: `3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3826", "Current State After 3827", 1)
    paragraph = (
        "`3827` runs the 3826 compact-exterior source-kernel scorecard as six local dry-run smoke checks: "
        "R10, WEP, PPN, clock, orbital, and EM all resolve their required kernel clauses, but all remain `claim_allowed=false`. "
        "The dry run converts the open branch from narrative blockers into a priority queue: `R_PPN_readout_tail` is the critical local-GR/Newton edge, "
        "boundary/`M_H_ref` rows and independent source ledger values are the next source-fill blockers, and EM/Poynting stress stays tied to the same compact source kernel.\n\n"
    )
    anchor = "`3826` integrates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md`

Target: run the 3826 compact-exterior source-kernel scorecard as dry-run local arena checks for R10/WEP/PPN/clock/orbital/EM, with explicit `claim_allowed=false` failure modes and a priority source-fill queue.

This is the best next move because testing can now start safely in nonclaim mode: the runner should show which arenas are schema-ready, which fail from missing source rows, and which physics residuals block local Newton/GR recovery."""
    new_gate = """`3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md`

Target: derive or cleanly bound `R_PPN_readout_tail` for `gamma-1`, `beta-1`, preferred-frame, clock, and orbital residuals using the same compact exterior source kernel, without arena-tuned readout coefficients.

This is the best next move because 3827 shows the dry-run machinery is working and the readout tail is the critical proof edge between the compact source kernel and local Newton/GR recovery."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3827_SMOKE_RUN_RESULTS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3827_FAILURE_MODE_LEDGER.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3827_PRIORITY_SOURCE_FILL_QUEUE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3827_PPN_READOUT_TAIL_FIRST_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3827_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3827_SMOKE_RUN_RESULTS.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3827 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3827 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    dry_inputs: list[dict[str, object]],
    smoke_results: list[dict[str, object]],
    failures: list[dict[str, object]],
    priority_queue: list[dict[str, object]],
    ppn_rows: list[dict[str, object]],
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

    add(
        "VAL3827_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    required_arena_ids = set(ARENA_ALIAS)
    result_arena_ids = {str(row["arena_id"]) for row in smoke_results}
    add(
        "VAL3827_1_arena_count",
        "one smoke result per local arena",
        required_arena_ids == result_arena_ids,
        "; ".join(sorted(result_arena_ids)),
    )
    add(
        "VAL3827_2_kernel_resolution",
        "all dry-run inputs resolve declared kernel clauses",
        all(row["kernel_clause_resolution"] == "PASS" for row in dry_inputs),
        "; ".join(f"{row['arena_id']}={row['kernel_clause_resolution']}" for row in dry_inputs),
    )
    add(
        "VAL3827_3_no_claims",
        "all smoke, PPN, and gate rows remain claim-blocked",
        all(not bool(row.get("claim_allowed")) for row in smoke_results + ppn_rows + gates),
        "claim_allowed=false throughout generated claim-bearing rows",
    )
    add(
        "VAL3827_4_no_physics_pass",
        "no smoke status is a physics pass",
        all("CLAIM_PASS" not in str(row["smoke_status"]) and "PHYSICS_PASS" not in str(row["smoke_status"]) for row in smoke_results),
        "; ".join(str(row["smoke_status"]) for row in smoke_results),
    )
    add(
        "VAL3827_5_failure_modes",
        "failure ledger names PPN, boundary/MHref, GM guard, and EM/Poynting blockers",
        all(
            token in " ".join(str(row.values()) for row in failures)
            for token in ["PPN", "boundary", "GM", "Poynting"]
        ),
        f"{len(failures)} failure rows",
    )
    add(
        "VAL3827_6_priority_next",
        "priority queue selects PPN readout tail first",
        bool(priority_queue) and priority_queue[0]["target"] == "R_PPN_readout_tail",
        str(priority_queue[0]["target"]) if priority_queue else "missing queue",
    )
    add(
        "VAL3827_7_ppn_rows",
        "PPN first rows cover gamma, beta, preferred-frame, clock, and orbital guard",
        len(ppn_rows) == 5 and all(not row["valid_for_claim"] for row in ppn_rows),
        f"{len(ppn_rows)} PPN rows",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3827_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3827_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "R_PPN_readout_tail" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = [path for path in FWB.rglob("*3827*") if path.is_file()] if FWB.exists() else []
    add(
        "VAL3827_10_formalization_clean",
        "formalization-workbench has no 3827 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3827 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3827_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    scorecard = read_csv_rows(CSV_3826_SCORECARD)
    arenas = read_csv_rows(CSV_3826_ARENAS)

    dry_inputs = dry_input_rows(arenas, scorecard, timestamp)
    smoke_results = smoke_result_rows(arenas, dry_inputs, timestamp)
    failures = failure_mode_rows(smoke_results, timestamp)
    priority_queue = priority_queue_rows(timestamp)
    ppn_rows = ppn_first_rows(timestamp)
    gates = claim_gate_rows(smoke_results, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["dry_inputs"], dry_inputs)
    write_csv(OUTPUTS["smoke_results"], smoke_results)
    write_csv(OUTPUTS["failures"], failures)
    write_csv(OUTPUTS["priority_queue"], priority_queue)
    write_csv(OUTPUTS["ppn_first_rows"], ppn_rows)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, smoke_results, failures, priority_queue, ppn_rows, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, dry_inputs, smoke_results, failures, priority_queue, ppn_rows, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_LOCAL_DRY_RUN")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
