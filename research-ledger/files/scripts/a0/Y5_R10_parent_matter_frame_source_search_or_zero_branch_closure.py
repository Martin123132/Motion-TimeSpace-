from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "633-Y5-R10-parent-matter-frame-source-search-or-zero-branch-closure.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_parent_matter_frame_source_search_or_zero_branch_closure.py"

STATUS = "Y5_R10_parent_matter_frame_source_hunt_found_conditional_contracts_no_signed_zero_branch"
CLAIM_CEILING = "source_hunt_and_closure_classification_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "634-Y5-R10-zero-branch-parent-clause-draft-or-two-leg-input-fill.md"

PRIOR_632_DOC = ROOT / "632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md"
PRIOR_632_VALIDATION = MTS_DIR / "P8_Y5_BRR545_632_VALIDATION.csv"
PRIOR_632_SELECTOR = MTS_DIR / "P8_Y5_R10_632_PARENT_MATTER_FRAME_SELECTOR_AUDIT.csv"
PRIOR_632_BRANCH = MTS_DIR / "P8_Y5_R10_632_BRANCH_SELECTION_STATUS.csv"
PRIOR_632_ENVELOPE = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_633_SOURCE_REGISTER.csv"
SEARCH_LEDGER = MTS_DIR / "P8_Y5_R10_633_SOURCE_HUNT_LEDGER.csv"
CANDIDATE_CLASSIFICATION = MTS_DIR / "P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv"
ZERO_CLOSURE_GATE = MTS_DIR / "P8_Y5_R10_633_ZERO_BRANCH_CLOSURE_GATE.csv"
FINITE_FALLBACK = MTS_DIR / "P8_Y5_R10_633_FINITE_FALLBACK_STATUS.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_633_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_633_ROUTE_UPDATE.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_633_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_633_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_633_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def text_contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle.lower() in path.read_text(encoding="utf-8", errors="ignore").lower()


def count_term_hits(term: str) -> int:
    roots = [ROOT]
    count = 0
    for root in roots:
        for path in root.glob("*.md"):
            if text_contains(path, term):
                count += 1
        residual_dir = MTS_DIR
        for path in residual_dir.glob("*.csv"):
            if text_contains(path, term):
                count += 1
    return count


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_632_DOC, "immediate selector/envelope checkpoint"),
        (PRIOR_632_VALIDATION, "632 validation gate"),
        (PRIOR_632_SELECTOR, "632 parent selector audit"),
        (PRIOR_632_BRANCH, "632 branch selection status"),
        (PRIOR_632_ENVELOPE, "632 two-leg pressure envelope"),
        (ROOT / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "candidate matter-frame action owner contract"),
        (ROOT / "240-universal-coupling-parent-contract-or-local-bound-data-runner.md", "universal coupling parent contract"),
        (ROOT / "241-C-silence-screening-or-parent-selection-theorem.md", "conformal trace-source no-go/screening gate"),
        (ROOT / "360-universal-matter-coupling-theorem-attempt.md", "universal matter coupling theorem attempt"),
        (ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "vertical observation theorem attempt"),
        (ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "primitive quotient/no-marker parent clause attempt"),
        (ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md", "quotient-invariant signature attempt"),
        (ROOT / "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md", "matter-frame variation result"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC633_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def source_hunt_ledger_rows() -> list[dict[str, Any]]:
    terms = [
        ("matter_frame", "matter frame"),
        ("S_matter", "S_matter"),
        ("quotient_descent", "descend"),
        ("Xhat", "Xhat"),
        ("A_g", "A_g"),
        ("c_g", "c_g"),
        ("disformal", "disformal"),
        ("no_marker", "no marker"),
        ("boundary", "boundary"),
    ]
    return [
        {
            "hunt_id": f"HUNT633_{index}",
            "search_family": label,
            "term": term,
            "local_hits_in_top_docs_and_mts_csv": count_term_hits(term),
            "search_scope": "post-checkpoint-work top-level markdown plus source-intake/mts_residuals CSV",
            "interpretation": "hits_found_not_enough_for_parent_signature" if count_term_hits(term) else "no_hits_in_reduced_scope",
            "valid_for_claim": "false",
        }
        for index, (label, term) in enumerate(terms)
    ]


def candidate_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "MFC633_0_204_matter_action",
            "source_path": "204-matter-metric-action-and-ruler-transport-owner-contract.md",
            "evidence_snippet": "S_matter = integral sqrt(-tilde_g)",
            "candidate_signature": "metric matter action and matter-frame conservation route",
            "classification": "conditional_contract",
            "helps_zero_branch": "defines what a matter frame would be",
            "blocking_gap": "does not prove this frame is quotient-only in the R10/Xhat branch",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_1_240_universal_coupling",
            "source_path": "240-universal-coupling-parent-contract-or-local-bound-data-runner.md",
            "evidence_snippet": "S_matter = sum_A S_A[Psi_A, ehat",
            "candidate_signature": "one observed coframe and no direct memory-sector matter argument",
            "classification": "strong_conditional_contract_not_parent_selected",
            "helps_zero_branch": "would make delta S_matter/delta Z_I vanish at fixed observed coframe",
            "blocking_gap": "document itself marks parent selection of universal matter action as fail/open",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_2_241_conformal_no_go",
            "source_path": "241-C-silence-screening-or-parent-selection-theorem.md",
            "evidence_snippet": "unscreened conformal",
            "candidate_signature": "dynamic conformal trace branch is not locally silent",
            "classification": "negative_evidence_against_finite_conformal_silence",
            "helps_zero_branch": "supports strict quotient/zero-mode/screened route over naive conformal route",
            "blocking_gap": "does not prove quotient-only matter; it rejects a lazy conformal shortcut",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_3_360_universal_theorem",
            "source_path": "360-universal-matter-coupling-theorem-attempt.md",
            "evidence_snippet": "no direct MTS matter arguments",
            "candidate_signature": "universal matter coupling theorem attempt",
            "classification": "conditional_theorem_attempt",
            "helps_zero_branch": "states the exact one-coframe/no-direct-argument rule needed",
            "blocking_gap": "universal coupling theorem remains conditional rather than parent-derived",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_4_565_vertical_observation",
            "source_path": "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
            "evidence_snippet": "conditional_proof_valid",
            "candidate_signature": "if X is vertical and matter factors through observed quotient, delta_X S_matter=0",
            "classification": "conditional_zero_lemma",
            "helps_zero_branch": "directly matches the desired c_g zero theorem shape",
            "blocking_gap": "X verticality, factorization, and no-marker independence remain open",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_5_566_no_marker_clause",
            "source_path": "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md",
            "evidence_snippet": "not_derived_current_claim",
            "candidate_signature": "primitive quotient/no-marker parent clause",
            "classification": "sufficient_axiom_candidate_not_derived",
            "helps_zero_branch": "would close vertical X and no marker leakage if adopted",
            "blocking_gap": "requires adding/sourcing a new primitive parent principle",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_6_626_descent_signature",
            "source_path": "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
            "evidence_snippet": "descent criterion",
            "candidate_signature": "quotient-invariant matter-action signature attempt",
            "classification": "immediate_prior_failed_signature",
            "helps_zero_branch": "lists the exact descent signature",
            "blocking_gap": "criterion exists but was not parent-signed",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "MFC633_7_631_variation",
            "source_path": "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md",
            "evidence_snippet": "J_X = sqrt(-g_m) c_g T_m",
            "candidate_signature": "matter-frame variation proves zero iff derivatives vanish; otherwise trace current",
            "classification": "derived_conditional_branch_law",
            "helps_zero_branch": "makes the zero condition exact",
            "blocking_gap": "still needs parent selector to decide actual branch",
            "selected_for_claim": "false",
            "valid_for_claim": "false",
        },
    ]


def zero_branch_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ZBC633_0_parent_matter_frame",
            "closure_requirement": "explicit parent matter frame is quotient-only",
            "best_candidate": "240/360/565/566 conditional contracts",
            "hunt_result": "candidate_found_not_signed",
            "closure_status": "open",
            "if_unclosed": "finite two-leg branch remains live",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZBC633_1_X_verticality",
            "closure_requirement": "Xhat is vertical to observed quotient geometry",
            "best_candidate": "565/566 vertical observation route",
            "hunt_result": "conditional_theorem_found",
            "closure_status": "open",
            "if_unclosed": "Xhat can be a physical local scalar/residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZBC633_2_constants_no_marker",
            "closure_requirement": "matter constants/masses do not depend on Xhat or material markers",
            "best_candidate": "566 plus no-species/no-marker lineage",
            "hunt_result": "sufficient_clause_candidate_found",
            "closure_status": "open",
            "if_unclosed": "WEP/clock channels re-enter through composition dependence",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZBC633_3_no_conformal_disformal_shadow",
            "closure_requirement": "no A_g/B_g representative shadow frame survives",
            "best_candidate": "241 no-go plus 625/626/631 lineage",
            "hunt_result": "negative_guard_found_no_positive_zero_source",
            "closure_status": "open",
            "if_unclosed": "trace/disformal current remains possible",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZBC633_4_boundary_silence",
            "closure_requirement": "vertical boundary/projector/domain current has no local projection",
            "best_candidate": "566 flux owner plus later boundary rows",
            "hunt_result": "retained_coefficient_or_closure_only",
            "closure_status": "open",
            "if_unclosed": "edge current can fake a finite source leg",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZBC633_5_total",
            "closure_requirement": "all zero gates parent-signed simultaneously",
            "best_candidate": "none",
            "hunt_result": "not_found",
            "closure_status": "not_closed",
            "if_unclosed": "zero branch must be labelled closure-only or future parent-clause target",
            "valid_for_claim": "false",
        },
    ]


def finite_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FF633_0_two_leg_runner",
            "object": "universal_two_leg_conformal",
            "status": "retained_nonclaim",
            "reason": "source hunt did not close quotient-only zero branch",
            "pressure_source": rel(PRIOR_632_ENVELOPE),
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FF633_1_linear_row",
            "object": "linear_compressed_alpha",
            "status": "blocked_until_metadata",
            "reason": "source/test leg ownership remains missing",
            "pressure_source": rel(PRIOR_632_SELECTOR),
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FF633_2_mixed_branch",
            "object": "disformal_or_mass_channel",
            "status": "blocked",
            "reason": "could generate WEP/clock/PPN leakage outside R10-only score",
            "pressure_source": "no finite projection schema yet",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D633_0_main_verdict",
            "decision": STATUS,
            "meaning": "the hunt found useful conditional contracts but no signed parent matter-frame source",
            "status": "source_hunt_progress_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D633_1_zero_branch",
            "decision": "zero_branch_not_closed",
            "meaning": "quotient-only zero route remains the best GR route but is closure-only until parent signed",
            "status": "closure_only_or_future_axiom",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D633_2_finite_branch",
            "decision": "two_leg_fallback_retained",
            "meaning": "finite coupling must remain under two-leg pressure if zero branch is not adopted/proved",
            "status": "nonclaim_pressure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D633_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no local test pass follows from conditional source contracts",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU633_0_allowed",
            "allowed_after_633": "Use 204/240/360/565/566 as conditional support for a drafted parent zero clause.",
            "forbidden_after_633": "Cite any of them as already proving c_g=0.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU633_1_allowed",
            "allowed_after_633": "Demote zero branch to explicit closure-only unless a new parent clause is adopted.",
            "forbidden_after_633": "Leave zero branch implicit while scoring local tests.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU633_2_allowed",
            "allowed_after_633": "Continue two-leg finite branch as private pressure fallback.",
            "forbidden_after_633": "Use R10 envelope as evidence before source/profile inputs are owned.",
            "next_action": NEXT_TARGET,
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC633_0_zero_clause_draft",
            "required_output": "explicit parent clause: ordinary matter is a functor of observed quotient geometry and X-independent constants only",
            "success_condition": "clause closes matter frame, constants/no-marker, no shadow frame, and boundary silence gates",
            "if_success": "zero branch becomes a labelled parent axiom candidate, still requiring consistency review",
            "if_fail": "zero branch remains closure-only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC633_1_source_text_upgrade",
            "required_output": "find original corpus text/docx/notebook source that already states the parent matter frame",
            "success_condition": "source path exists and says quotient-only matter rather than merely conditional contract",
            "if_success": "rerun 633 with candidate promoted to parent_source_candidate",
            "if_fail": "do not pretend the source exists",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC633_2_two_leg_input_fill",
            "required_output": "if zero branch is not adopted, fill beta_source,beta_test,Z_eff,lambda_X,profile_factor",
            "success_condition": "finite branch has owner equations and units",
            "if_success": "private numeric scans can begin",
            "if_fail": "finite branch remains pressure-only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "conditional_contracts_found": "true",
            "signed_parent_matter_frame_found": "false",
            "zero_branch_closed": "false",
            "zero_branch_status": "closure_only_or_future_parent_clause",
            "finite_fallback": "two_leg_envelope_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_632_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    missing_snippets = [
        row
        for row in candidate_rows
        if not text_contains(ROOT / row["source_path"], row["evidence_snippet"])
    ]
    signed_candidates = [row for row in candidate_rows if row.get("selected_for_claim") == "true" or row.get("valid_for_claim") == "true"]
    total_gate = next((row for row in zero_rows if row["gate_id"] == "ZBC633_5_total"), {})
    claim_fallback_rows = [row for row in fallback_rows if row.get("claim_allowed") == "true" or row.get("valid_for_claim") == "true"]
    return [
        {
            "check_id": "V633_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V633_1_prior_632_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V633_2_hunt_ledger_written",
            "result": "pass" if len(hunt_rows) == 9 else "fail",
            "detail": f"hunt_rows={len(hunt_rows)}",
        },
        {
            "check_id": "V633_3_candidate_snippets_verified",
            "result": "pass" if len(candidate_rows) == 8 and not missing_snippets else "fail",
            "detail": f"candidate_rows={len(candidate_rows)};missing_snippets={len(missing_snippets)}",
        },
        {
            "check_id": "V633_4_no_candidate_promoted_to_claim",
            "result": "pass" if not signed_candidates else "fail",
            "detail": f"signed_candidates={len(signed_candidates)}",
        },
        {
            "check_id": "V633_5_zero_branch_not_closed",
            "result": "pass" if len(zero_rows) == 6 and total_gate.get("closure_status") == "not_closed" else "fail",
            "detail": f"zero_rows={len(zero_rows)};total={total_gate.get('closure_status', '')}",
        },
        {
            "check_id": "V633_6_finite_fallback_retained_nonclaim",
            "result": "pass" if len(fallback_rows) == 3 and not claim_fallback_rows else "fail",
            "detail": f"fallback_rows={len(fallback_rows)};claim_rows={len(claim_fallback_rows)}",
        },
        {
            "check_id": "V633_7_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V633_8_no_local_claim",
            "result": "pass",
            "detail": "signed_parent_matter_frame=false;zero_branch_closed=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def build_doc(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 633 Y5 R10 parent matter frame source search or zero branch closure",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- The source hunt found several useful conditional matter-frame contracts.\n"
            "- It did not find a signed parent matter-frame source that closes the quotient-only zero branch.\n"
            "- The best zero-route ingredients are `204`, `240`, `360`, `565`, and `566`, but they remain conditional or sufficient-clause candidates.\n"
            "- Therefore `c_g=0` is not promoted; the zero branch must be explicit closure-only or become a new parent clause.\n"
            "- The finite two-leg envelope remains the honest fallback pressure route.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Source Hunt Ledger\n" + markdown_table(hunt_rows),
            "## Matter-Frame Candidate Classification\n" + markdown_table(candidate_rows),
            "## Zero Branch Closure Gate\n" + markdown_table(zero_rows),
            "## Finite Fallback Status\n" + markdown_table(fallback_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Next Contract\n" + markdown_table(contracts),
            "## Nonclaim Summary\n" + markdown_table(summary),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    hunt_rows = source_hunt_ledger_rows()
    candidate_rows = candidate_classification_rows()
    zero_rows = zero_branch_closure_rows()
    fallback_rows = finite_fallback_rows()
    decisions = decision_rows()
    routes = route_update_rows()
    contracts = next_contract_rows()
    summary = nonclaim_summary_rows()
    validations = validation_rows(source_rows, hunt_rows, candidate_rows, zero_rows, fallback_rows, contracts)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(SEARCH_LEDGER, hunt_rows)
    write_csv(CANDIDATE_CLASSIFICATION, candidate_rows)
    write_csv(ZERO_CLOSURE_GATE, zero_rows)
    write_csv(FINITE_FALLBACK, fallback_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(NEXT_CONTRACT, contracts)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            hunt_rows,
            candidate_rows,
            zero_rows,
            fallback_rows,
            decisions,
            routes,
            contracts,
            summary,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )
    failed = [row for row in validations if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))


if __name__ == "__main__":
    main()
