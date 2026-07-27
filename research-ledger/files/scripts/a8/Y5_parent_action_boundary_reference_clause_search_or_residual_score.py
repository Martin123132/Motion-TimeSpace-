from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_parent_action_clause_search_done_MAC545_not_owned_BRR545_scorecard_written"
CLAIM_CEILING = "MAC545_ownership_search_and_residual_scorecard_only_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md"

DOC_PATH = Path("546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_546_SOURCE_REGISTER.csv")
CLAUSE_SEARCH_PATH = Path("source-intake/mts_residuals/P8_Y5_MAC545_PARENT_ACTION_CLAUSE_SEARCH.csv")
OWNERSHIP_MATRIX_PATH = Path("source-intake/mts_residuals/P8_Y5_MAC545_OWNERSHIP_MATRIX.csv")
RESIDUAL_SCORECARD_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_SCORECARD.csv")
GAP_REPAIR_QUEUE_PATH = Path("source-intake/mts_residuals/P8_Y5_MAC545_GAP_REPAIR_QUEUE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_546_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_546_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_546_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
        "role": "MAC545 sufficient contract and retained BRR545 residual",
    },
    {
        "source_file": "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md",
        "role": "data/theorem-zero audit for boundary/reference first row",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional Noether mass-charge closure theorem",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure transfer theorem and M_eff residual runner",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "projected source identity and Pi_M/boundary obstruction decomposition",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M projector ownership and radial runner route",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "Gauss/orbital source-normalization scorecard",
    },
    {
        "source_file": "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
        "role": "source-calibrated EH family proof stack",
    },
    {
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "role": "measured-GM source-current closure attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
        "role": "545 MAC545 contract rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "role": "505 conditional Noether theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "role": "510 worldtube source-measure theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "role": "499 source identity residual decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "role": "532 source-current closure theorem attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RESIDUAL_DECOMPOSITION.csv",
        "role": "532 epsilon charge residual decomposition",
    },
    {
        "source_file": "scripts/Y5_parent_action_boundary_reference_clause_search_or_residual_score.py",
        "role": "this checkpoint generator",
    },
]


CLAUSE_SEARCH_ROWS = [
    {
        "search_id": "CS546_0_MAC545_0",
        "clause_id": "MAC545_0_covariant_parent_action",
        "strongest_evidence": "505 and 510 give an Iyer-Wald/Noether-style conditional charge form; 510 defines Delta_symp as the boundary symplectic transfer obstruction",
        "evidence_source": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md;510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "why_not_enough": "the current branch still lacks a fixed parent Lagrangian, fixed boundary term, and explicit Theta/B_ref variation ledger",
        "search_result": "conditional_template_found",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_1_MAC545_1",
        "clause_id": "MAC545_1_exterior_annulus_vacuum",
        "strongest_evidence": "510 supplies the compact worldtube/exterior annulus setup; 505 states the conditional Stokes charge theorem",
        "evidence_source": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md;source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "why_not_enough": "annulus setup is not enough while C_extra, C_projector, C_boundary, frame, and calibration terms remain open",
        "search_result": "partial_setup_found",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_2_MAC545_2",
        "clause_id": "MAC545_2_reference_lock",
        "strongest_evidence": "544 found reference-only zero rows and Hamiltonian calibration contracts",
        "evidence_source": "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md;source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv",
        "why_not_enough": "no row proves the reference subtraction is source/surface/frame/range/time independent for current MTS",
        "search_result": "no_owner_found",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_3_MAC545_3",
        "clause_id": "MAC545_3_boundary_exact_cohomology_zero",
        "strongest_evidence": "505 names zero boundary/improvement flux as a premise; 499 marks boundary improvement flux as fail_open",
        "evidence_source": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md;source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "why_not_enough": "exact/topological wording does not prove compact linking-sphere flux is zero; finite surface charges remain possible",
        "search_result": "premise_found_but_failed_open",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_4_MAC545_4",
        "clause_id": "MAC545_4_boundary_no_vector_tensor_hair",
        "strongest_evidence": "485/486 and 543 identify the scalar/no-flux lemma and its obstruction ledger",
        "evidence_source": "485-boundary-no-flux-and-R11-silence-from-local-zero.md;486-R11-boundary-stress-theorem-or-closure-fill-pack.md;543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
        "why_not_enough": "scalar boundary language does not eliminate vector, trace-free tensor, preferred-frame, or projector-stress hair unless parent-owned",
        "search_result": "conditional_lemma_found",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_5_MAC545_5",
        "clause_id": "MAC545_5_projector_symplectic_silence",
        "strongest_evidence": "499 and 532 isolate [d,Pi_M]J_H, delta Pi_M, and Pi_M equality as exact obstructions",
        "evidence_source": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md;532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "why_not_enough": "Pi_M is still not parent-derived as metric-independent/topological charge data; commutator/symplectic stress remains retained",
        "search_result": "obstruction_exact_but_not_zero",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
    {
        "search_id": "CS546_6_MAC545_6",
        "clause_id": "MAC545_6_positive_measured_denominator",
        "strongest_evidence": "523/529/532 give the source-current, Poisson/Gauss, and source-calibrated EH proof stacks",
        "evidence_source": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md;529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md;532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "why_not_enough": "M_H_ref positivity is easy, but same-frame GM_orbit=G M_H_ref is still a downstream calibration theorem, not a parent-owned result",
        "search_result": "conditional_calibration_stack_found",
        "owned_for_MAC545": "false",
        "valid_for_claim": "false",
    },
]


OWNERSHIP_MATRIX_ROWS = [
    {
        "clause_id": "MAC545_0_covariant_parent_action",
        "evidence_grade": "B_conditional_form",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "write explicit local parent Lagrangian plus boundary term B_ref and compute Theta, Q_tau, Delta_symp",
        "if_unrepaired": "Delta_symp remains a named residual rather than a derived charge",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_1_exterior_annulus_vacuum",
        "evidence_grade": "B_minus_setup_only",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "derive all C-term silence in the annulus or move each open C term into a numeric residual envelope",
        "if_unrepaired": "Stokes/Gauss surface equality cannot be promoted",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_2_reference_lock",
        "evidence_grade": "D_missing",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "derive a universal source-independent Hamiltonian reference normalization from the action",
        "if_unrepaired": "Delta_symp_ref can absorb or mimic source mass shifts",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_3_boundary_exact_cohomology_zero",
        "evidence_grade": "C_premise_open",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "prove B_imp=dC is trivial in the relative cohomology class of linked local spheres",
        "if_unrepaired": "B_zero_flux must be scored as a finite boundary-charge residual",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_4_boundary_no_vector_tensor_hair",
        "evidence_grade": "C_conditional_nohair",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "derive homogeneous scalar marker-free boundary state and show vector/TF projections vanish",
        "if_unrepaired": "alpha_i, xi, Gdot, beta/source-normalization boundary hair remain live",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_5_projector_symplectic_silence",
        "evidence_grade": "C_obstruction_exact",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "derive Pi_M as topological/covariantly constant charge data or bound [d,Pi_M]J_H and delta Pi_M",
        "if_unrepaired": "projector stress can shift Delta_symp and M_H_ref",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_6_positive_measured_denominator",
        "evidence_grade": "C_plus_conditional_calibration",
        "owned_now": "false",
        "can_be_repaired_by_derivation": "true",
        "minimal_repair": "derive same-frame Poisson/Gauss/orbital equality GM_orbit=G M_H_ref",
        "if_unrepaired": "epsilon_BR has a formal denominator but no measured-GM meaning",
        "valid_for_claim": "false",
    },
]


RESIDUAL_SCORECARD_ROWS = [
    {
        "residual_id": "BRR545_0_total_boundary_reference",
        "quantity": "epsilon_boundary_reference_abs",
        "definition": "(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref",
        "decomposition": "epsilon_B_flux_abs + epsilon_Delta_symp_abs",
        "required_input_columns": "system_id;surface_pair;B_zero_flux_over_MH;Delta_symp_over_MH;M_H_ref_source;units;source_file;assumptions;valid_for_claim",
        "observable_lock": "source-measure/Newton precondition; radial GM drift; local PPN downstream",
        "current_status": "scoreable_template_no_values",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BRR545_1_boundary_flux",
        "quantity": "epsilon_B_flux_abs",
        "definition": "abs(B_zero_flux)/M_H_ref",
        "decomposition": "boundary exact/improvement flux plus boundary stress hair",
        "required_input_columns": "B_zero_flux_over_MH or theorem_zero_certificate",
        "observable_lock": "boundary alpha3/xi/Gdot/beta/source-normalization channels",
        "current_status": "missing_value_or_theorem_zero",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BRR545_2_reference_symplectic",
        "quantity": "epsilon_Delta_symp_abs",
        "definition": "abs(Delta_symp)/M_H_ref",
        "decomposition": "reference subtraction plus exterior symplectic/projector flux",
        "required_input_columns": "Delta_symp_over_MH or theorem_zero_certificate",
        "observable_lock": "absolute mass calibration; radial closure; source universality",
        "current_status": "missing_value_or_theorem_zero",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BRR545_3_denominator",
        "quantity": "M_H_ref",
        "definition": "positive same-frame Hilbert/source denominator tied to orbital measured GM",
        "decomposition": "M_H_ref_positive and GM_orbit=G M_H_ref",
        "required_input_columns": "M_H_ref_source;GM_orbit_source;same_frame_certificate",
        "observable_lock": "measured-GM and Newton/Gauss readout",
        "current_status": "formal_denominator_without_measured_GM_promotion",
        "valid_for_claim": "false",
    },
]


GAP_REPAIR_QUEUE_ROWS = [
    {
        "priority": 1,
        "gap_id": "G546_0_reference_lock",
        "target_clause": "MAC545_2",
        "why_first": "without a reference lock Delta_symp can be moved by convention",
        "next_derivation_attempt": "derive B_ref from a universal background subtraction or prove only differences are observable and source-independent",
        "fallback_if_fails": "score epsilon_Delta_symp_abs",
    },
    {
        "priority": 2,
        "gap_id": "G546_1_boundary_cohomology_nohair",
        "target_clause": "MAC545_3;MAC545_4",
        "why_first": "B_zero_flux is the cleanest numerator term to kill if boundary class is genuinely trivial",
        "next_derivation_attempt": "prove relative cohomology triviality plus scalar homogeneous marker-free boundary variation",
        "fallback_if_fails": "score epsilon_B_flux_abs",
    },
    {
        "priority": 3,
        "gap_id": "G546_2_projector_silence",
        "target_clause": "MAC545_5",
        "why_first": "Pi_M stress contaminates both Delta_symp and M_H_ref",
        "next_derivation_attempt": "derive Pi_M as a topological charge projector or provide commutator bound input",
        "fallback_if_fails": "carry epsilon_commutator and epsilon_PiM_equality from 532",
    },
    {
        "priority": 4,
        "gap_id": "G546_3_measured_denominator",
        "target_clause": "MAC545_6",
        "why_first": "needed before any local-GR/Newton claim",
        "next_derivation_attempt": "derive same-frame Poisson/Gauss/orbital equality for GM_orbit=G M_H_ref",
        "fallback_if_fails": "keep formal residual but no measured-GM promotion",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D546_0_no_MAC545_clause_owned",
        "status": "ownership_search_negative_for_claim",
        "meaning": "existing corpus provides conditional theorem scaffolding but owns none of MAC545_0...MAC545_6 for claim use",
        "claim_status": "boundary_reference_zero_not_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D546_1_best_positive_result",
        "status": "conditional_Noether_worldtube_form_is_real",
        "meaning": "505/510 are useful: they show the right charge-theorem shape if the open C/reference/boundary/projector/calibration premises close",
        "claim_status": "conditional_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D546_2_residual_now_scoreable",
        "status": "BRR545_decomposed_into_scoreable_subrows",
        "meaning": "the hidden gap is split into epsilon_B_flux_abs, epsilon_Delta_symp_abs, and M_H_ref calibration requirements",
        "claim_status": "residual_template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D546_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BOUNDARY_REFERENCE_ZERO",
        "previous_status": "minimal_sufficient_contract_written_not_parent_owned",
        "new_status": "MAC545_ownership_search_negative_residual_scorecard_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "blocked_until_MAC545_parent_ownership_or_residual_bound",
        "new_status": "blocked_until_BRR545_inputs_or_theorem_zero",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_by_denominator_and_boundary_reference_contract",
        "new_status": "blocked_by_measured_denominator_and_unfilled_boundary_reference_score",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_but_exact_parent_action_target_identified",
        "new_status": "still_blocked_but_gap_is_now_scoreable",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_545_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    prior_contract = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv"))
    noether_rows = read_csv(Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_THEOREM.csv"))
    worldtube_rows = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"))
    owned_rows = [row for row in OWNERSHIP_MATRIX_ROWS if row["owned_now"] == "true"]
    claim_search_rows = [row for row in CLAUSE_SEARCH_ROWS if row["valid_for_claim"] == "true"]
    claim_score_rows = [row for row in RESIDUAL_SCORECARD_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V546_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V546_1_prior_545_clean",
            "result": "pass" if len(prior_validation) == 8 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V546_2_MAC545_contract_loaded",
            "result": "pass" if len(prior_contract) == 7 else "fail",
            "detail": f"prior_contract_rows={len(prior_contract)}",
        },
        {
            "check_id": "V546_3_conditional_theorem_sources_loaded",
            "result": "pass" if len(noether_rows) >= 3 and len(worldtube_rows) >= 4 else "fail",
            "detail": f"noether_rows={len(noether_rows)};worldtube_rows={len(worldtube_rows)}",
        },
        {
            "check_id": "V546_4_clause_search_complete",
            "result": "pass" if len(CLAUSE_SEARCH_ROWS) == 7 and len(OWNERSHIP_MATRIX_ROWS) == 7 else "fail",
            "detail": f"search_rows={len(CLAUSE_SEARCH_ROWS)};matrix_rows={len(OWNERSHIP_MATRIX_ROWS)}",
        },
        {
            "check_id": "V546_5_no_owned_MAC545_overclaim",
            "result": "pass" if not owned_rows and not claim_search_rows else "fail",
            "detail": f"owned_rows={len(owned_rows)};claim_search_rows={len(claim_search_rows)}",
        },
        {
            "check_id": "V546_6_residual_scorecard_written",
            "result": "pass" if len(RESIDUAL_SCORECARD_ROWS) == 4 and not claim_score_rows else "fail",
            "detail": f"scorecard_rows={len(RESIDUAL_SCORECARD_ROWS)};claim_score_rows={len(claim_score_rows)}",
        },
        {
            "check_id": "V546_7_no_overclaim",
            "result": "pass" if not owned_rows and not claim_search_rows and not claim_score_rows else "fail",
            "detail": "MAC545_owned=false; boundary_reference_zero_derived=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 546 - Y5 Parent Action Boundary Reference Clause Search Or Residual Score

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

We searched the current parent-action corpus against the seven `MAC545` clauses.

The positive result is real but conditional: the Noether/worldtube material has the correct mathematical skeleton for a local charge theorem. The negative result is also clear: none of `MAC545_0...MAC545_6` is owned for claim use yet.

So the gap is not "we have no idea". The gap is:

```text
conditional charge theorem exists
but reference lock + boundary cohomology/no-hair + projector silence + measured denominator are still unproved
```

That moves the branch from fog to a scorecard.

## 2. Clause Search

{markdown_table(CLAUSE_SEARCH_ROWS)}

## 3. Ownership Matrix

{markdown_table(OWNERSHIP_MATRIX_ROWS)}

## 4. Boundary Reference Residual Scorecard

{markdown_table(RESIDUAL_SCORECARD_ROWS)}

## 5. Gap Repair Queue

{markdown_table(GAP_REPAIR_QUEUE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a conditional Noether/worldtube skeleton for the boundary/reference route.
MTS has not parent-owned MAC545_0...MAC545_6.
MTS has converted BRR545 into scoreable residual subrows.
```

Forbidden:

```text
MTS has derived B_zero_flux=Delta_symp=0.
MTS has filled epsilon_boundary_reference_abs with data.
MTS has derived source-measure glue, measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is closer to the goal than yesterday's plateau problem. We now know the strongest path:

```text
Noether/worldtube charge skeleton
-> fixed reference
-> boundary cohomology/no-hair
-> Pi_M symplectic silence
-> measured-GM denominator
```

If any one of those can be parent-derived, it closes a real gap. If not, each has a residual slot and cannot hide inside a verbal "local vacuum" assumption.

## 12. Next Target

`{NEXT_TARGET}`

Next: write the actual residual input template and local-lock map for `epsilon_B_flux_abs`, `epsilon_Delta_symp_abs`, and `M_H_ref`, so we can either fill numbers/theorem certificates or see exactly which theorem to attack first.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-parent-action-boundary-reference-clause-search-or-residual-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (CLAUSE_SEARCH_PATH, CLAUSE_SEARCH_ROWS),
        (OWNERSHIP_MATRIX_PATH, OWNERSHIP_MATRIX_ROWS),
        (RESIDUAL_SCORECARD_PATH, RESIDUAL_SCORECARD_ROWS),
        (GAP_REPAIR_QUEUE_PATH, GAP_REPAIR_QUEUE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "clause_search": str(ROOT / CLAUSE_SEARCH_PATH),
        "ownership_matrix": str(ROOT / OWNERSHIP_MATRIX_PATH),
        "residual_scorecard": str(ROOT / RESIDUAL_SCORECARD_PATH),
        "gap_repair_queue": str(ROOT / GAP_REPAIR_QUEUE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "clause_search_rows": len(CLAUSE_SEARCH_ROWS),
        "ownership_matrix_rows": len(OWNERSHIP_MATRIX_ROWS),
        "residual_scorecard_rows": len(RESIDUAL_SCORECARD_ROWS),
        "gap_repair_rows": len(GAP_REPAIR_QUEUE_ROWS),
        "MAC545_owned_rows": 0,
        "boundary_reference_zero_derived": False,
        "BRR545_scorecard_written": True,
        "source_measure_theorem_derived": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nMAC545_ownership_search_negative_BRR545_scorecard_written_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
