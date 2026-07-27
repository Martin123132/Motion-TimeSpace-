from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_BRR545_residual_envelope_written_first_local_lock_not_fillable_local_GR_route_closure_only_until_repaired"
CLAIM_CEILING = "BRR545_residual_envelope_and_local_lock_preflight_only_no_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md"

DOC_PATH = Path("551-Y5-BRR545-residual-envelope-and-first-local-lock-fill-or-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_551_SOURCE_REGISTER.csv")
RESIDUAL_ENVELOPE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_RESIDUAL_ENVELOPE.csv")
LOCAL_LOCK_PREFLIGHT_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_PREFLIGHT.csv")
FIRST_LOCK_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_FIRST_LOCAL_LOCK_ATTEMPT.csv")
CLOSURE_DEMOTION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_CLOSURE_DEMOTION_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_551_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_551_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md",
        "role": "projector symplectic silence failure and commutator/projector bound row",
    },
    {
        "source_file": "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
        "role": "boundary cohomology/no-hair failure and boundary flux bound row",
    },
    {
        "source_file": "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
        "role": "reference lock failure and Delta_symp bound row",
    },
    {
        "source_file": "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md",
        "role": "BRR545 input template, dry run, and local lock map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_FIRST_BOUND_FILL_ROW.csv",
        "role": "reference/symplectic first bound row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
        "role": "boundary flux first bound row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
        "role": "commutator/projector first bound row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_INPUT_TEMPLATE.csv",
        "role": "BRR545 original residual input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_EVALUATOR_DRYRUN.csv",
        "role": "BRR545 dry-run evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
        "role": "BRR545 local lock map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_550_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "scripts/Y5_BRR545_residual_envelope_and_first_local_lock_fill_or_demotion.py",
        "role": "this checkpoint generator",
    },
]


RESIDUAL_ENVELOPE_ROWS = [
    {
        "envelope_id": "ENV551_0_reference_symplectic",
        "component": "epsilon_Delta_symp_abs",
        "strict_envelope_term": "abs(Delta_symp_over_MH)",
        "required_fill": "Delta_symp_over_MH;partial_t_epsilon_Delta_symp_abs;partial_r_epsilon_Delta_symp_abs;alpha_lambda_reference_profile;c_Delta_symp_to_gamma",
        "mapped_locks": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "current_status": "unfilled_retained",
        "theorem_zero_status": "reference_lock_certificate_failed_current_claim",
        "valid_for_claim": "false",
    },
    {
        "envelope_id": "ENV551_1_boundary_flux",
        "component": "epsilon_B_flux_abs",
        "strict_envelope_term": "abs(B_zero_flux_over_MH)",
        "required_fill": "B_zero_flux_over_MH;c_B_flux_to_alpha3;c_B_flux_to_xi;c_B_flux_to_beta;partial_t_epsilon_B_flux_abs;partial_r_epsilon_B_flux_abs",
        "mapped_locks": "R7_alpha3;R8_xi;R4_beta;R9_Gdot;R11_EH_operator_ledger",
        "current_status": "unfilled_retained",
        "theorem_zero_status": "boundary_cohomology_nohair_certificate_failed_current_claim",
        "valid_for_claim": "false",
    },
    {
        "envelope_id": "ENV551_2_projector_commutator",
        "component": "epsilon_commutator",
        "strict_envelope_term": "abs(int_A [d,Pi_M]J_H)/M_H_ref",
        "required_fill": "commutator_over_MH;c_projector_to_gamma;c_projector_to_beta;c_projector_to_alpha3;c_projector_to_xi;partial_t_projector_residual;partial_r_projector_residual",
        "mapped_locks": "R3_gamma;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "current_status": "unfilled_retained",
        "theorem_zero_status": "projector_symplectic_silence_certificate_failed_current_claim",
        "valid_for_claim": "false",
    },
    {
        "envelope_id": "ENV551_3_projector_variation",
        "component": "epsilon_projector_variation",
        "strict_envelope_term": "abs(int_S (delta Pi_M)J_H)/M_H_ref",
        "required_fill": "projector_variation_over_MH;c_projector_to_gamma;c_projector_to_beta;c_projector_to_alpha3;c_projector_to_xi;T_PiM_operator_vector",
        "mapped_locks": "R3_gamma;R4_beta;R7_alpha3;R8_xi;R11_EH_operator_ledger",
        "current_status": "unfilled_retained",
        "theorem_zero_status": "projector_symplectic_silence_certificate_failed_current_claim",
        "valid_for_claim": "false",
    },
    {
        "envelope_id": "ENV551_4_denominator_reference",
        "component": "epsilon_MHref_calibration_abs",
        "strict_envelope_term": "abs(G*M_H_ref/GM_orbit - 1) plus time/species/operator derivative terms",
        "required_fill": "M_H_ref>0;GM_orbit=G*M_H_ref;same observed frame;eta_source_from_denominator_mismatch;partial_t ln(G*M_H_ref/GM_orbit);non_EH_source_normalization_operator_vector",
        "mapped_locks": "R1_WEP_source_charge;R9_Gdot;R11_EH_operator_ledger",
        "current_status": "unfilled_retained",
        "theorem_zero_status": "same_frame_measured_GM_denominator_certificate_missing",
        "valid_for_claim": "false",
    },
    {
        "envelope_id": "ENV551_5_total_no_cancellation",
        "component": "epsilon_BRR545_abs_envelope",
        "strict_envelope_term": "sum_abs(ENV551_0..ENV551_4)",
        "required_fill": "each component must be theorem-zero or source-backed below every mapped lock; no cancellation credit",
        "mapped_locks": "R1_WEP_source_charge;R3_gamma;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "current_status": "not_computable",
        "theorem_zero_status": "three_certificate_failures_plus_denominator_missing",
        "valid_for_claim": "false",
    },
]


LOCAL_LOCK_PREFLIGHT_ROWS = [
    {
        "lock_id": "LLP551_0_R7_alpha3",
        "local_row_id": "R7_alpha3",
        "required_test": "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs) and abs(c_projector_to_alpha3*epsilon_projector_symplectic_abs) each below 4e-20 or theorem-zero",
        "missing_items": "epsilon_B_flux_abs;c_B_flux_to_alpha3;epsilon_projector_symplectic_abs;c_projector_to_alpha3;alpha3 theorem-zero certificates",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_1_R8_xi",
        "local_row_id": "R8_xi",
        "required_test": "boundary and projector preferred-location terms each below xi lock or theorem-zero",
        "missing_items": "epsilon_B_flux_abs;c_B_flux_to_xi;epsilon_projector_symplectic_abs;c_projector_to_xi;domain/homology theorem",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_2_R4_beta",
        "local_row_id": "R4_beta",
        "required_test": "boundary and projector second-order scalar/metric terms each below beta lock or theorem-zero",
        "missing_items": "epsilon_B_flux_abs;c_B_flux_to_beta;epsilon_projector_symplectic_abs;c_projector_to_beta;second-order coefficient map",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_3_R3_gamma",
        "local_row_id": "R3_gamma",
        "required_test": "reference and projector linear metric terms each below gamma lock or theorem-zero",
        "missing_items": "epsilon_Delta_symp_abs;c_Delta_symp_to_gamma;epsilon_projector_symplectic_abs;c_projector_to_gamma",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_4_R9_Gdot",
        "local_row_id": "R9_Gdot",
        "required_test": "all time derivatives of reference, boundary, projector, and denominator residuals below Gdot/G or derivative-zero",
        "missing_items": "partial_t_epsilon_Delta_symp_abs;partial_t_epsilon_B_flux_abs;partial_t_projector_residual;partial_t ln denominator",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_5_R10_fifth_force",
        "local_row_id": "R10_fifth_force",
        "required_test": "range/radial profiles for reference and projector residuals below fifth-force curve or radial-zero theorem",
        "missing_items": "alpha_lambda_reference_profile;partial_r_epsilon_Delta_symp_abs;partial_r_projector_residual;radial-zero theorem",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_6_R1_WEP_source_charge",
        "local_row_id": "R1_WEP_source_charge",
        "required_test": "same-source denominator and charge measure produce no species/source-dependent eta above WEP lock",
        "missing_items": "same-frame measured-GM denominator certificate;eta_source_from_denominator_mismatch;source-measure glue",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
    {
        "lock_id": "LLP551_7_R11_operator_ledger",
        "local_row_id": "R11_EH_operator_ledger",
        "required_test": "non-EH boundary/reference/projector/source-normalization operators are theorem-zero or coefficient-mapped",
        "missing_items": "non_EH_source_normalization_operator_vector;T_PiM_operator_vector;boundary/reference operator coefficient maps",
        "current_status": "cannot_fill",
        "accepted_for_claim": "false",
    },
]


FIRST_LOCK_ATTEMPT_ROWS = [
    {
        "attempt_id": "FL551_0_first_lock_R7_alpha3",
        "chosen_lock": "R7_alpha3",
        "why_first": "alpha3 is the tightest local preferred-frame gate in the current BRR545 map and is hit by both boundary flux and projector symplectic residuals",
        "required_inequality": "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs) <= 4e-20 and abs(c_projector_to_alpha3*epsilon_projector_symplectic_abs) <= 4e-20, or theorem-zero for each term",
        "current_result": "cannot_fill",
        "blocking_missing_items": "B_zero_flux_over_MH;c_B_flux_to_alpha3;commutator_over_MH;projector_variation_over_MH;c_projector_to_alpha3;theorem-zero certificates",
        "decision": "demote_local_GR_route_to_closure_only_until_repaired",
        "accepted_for_claim": "false",
    }
]


CLOSURE_DEMOTION_ROWS = [
    {
        "decision_id": "CD551_0_BRR545_not_passed",
        "status": "not_passed",
        "meaning": "reference, boundary, projector, and denominator components are all explicit but unfilled",
        "claim_status": "BRR545_not_claimable",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "CD551_1_local_GR_route_closure_only",
        "status": "closure_only_until_repaired",
        "meaning": "the current local-GR transition route can be used as a labelled closure/residual branch, not as a derivation from the parent action",
        "claim_status": "local_GR_not_allowed",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "CD551_2_not_a_physical_failure",
        "status": "derivation_gap_not_data_rejection",
        "meaning": "this does not show MTS is empirically false; it shows the current local proof cannot omit these residuals",
        "claim_status": "private_repair_route_open",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "CD551_3_repair_priority",
        "status": "parent_action_zero_theorem_needed",
        "meaning": "the next productive move is a parent action contract that kills or owns reference, boundary, projector, and denominator terms together",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "CD551_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BRR545_RESIDUAL_ENVELOPE",
        "previous_status": "component_rows_scattered_across_548_549_550",
        "new_status": "strict_no_cancellation_envelope_written_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_FIRST_LOCAL_LOCK",
        "previous_status": "local_lock_map_written_not_attempted",
        "new_status": "R7_alpha3_attempted_cannot_fill_missing_values_coefficients_and_theorem_zero",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "blocked_no_reference_boundary_projector_zero_or_bound_values",
        "new_status": "closure_only_until_parent_action_zero_theorem_or_numeric_bound_fill",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_projector_symplectic_silence_failed_current_claim",
        "new_status": "still_blocked_BRR545_envelope_unfilled_and_denominator_missing",
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
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_550_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    reference_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_FIRST_BOUND_FILL_ROW.csv"))
    boundary_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv"))
    projector_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv"))
    input_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_INPUT_TEMPLATE.csv"))
    dryrun_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_EVALUATOR_DRYRUN.csv"))
    local_lock_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"))
    claim_envelope_rows = [row for row in RESIDUAL_ENVELOPE_ROWS if row["valid_for_claim"] == "true"]
    claim_lock_rows = [row for row in LOCAL_LOCK_PREFLIGHT_ROWS if row["accepted_for_claim"] == "true"]
    claim_first_lock_rows = [row for row in FIRST_LOCK_ATTEMPT_ROWS if row["accepted_for_claim"] == "true"]
    return [
        {
            "check_id": "V551_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V551_1_prior_550_clean",
            "result": "pass" if len(prior_validation) == 9 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V551_2_component_bound_rows_loaded",
            "result": "pass" if len(reference_rows) == 1 and len(boundary_rows) == 1 and len(projector_rows) == 1 else "fail",
            "detail": f"reference_rows={len(reference_rows)};boundary_rows={len(boundary_rows)};projector_rows={len(projector_rows)}",
        },
        {
            "check_id": "V551_3_original_BRR545_templates_loaded",
            "result": "pass" if len(input_rows) == 4 and len(dryrun_rows) == 4 and len(local_lock_rows) == 10 else "fail",
            "detail": f"input_rows={len(input_rows)};dryrun_rows={len(dryrun_rows)};local_lock_rows={len(local_lock_rows)}",
        },
        {
            "check_id": "V551_4_envelope_complete",
            "result": "pass" if len(RESIDUAL_ENVELOPE_ROWS) == 6 else "fail",
            "detail": f"envelope_rows={len(RESIDUAL_ENVELOPE_ROWS)}",
        },
        {
            "check_id": "V551_5_local_lock_preflight_complete",
            "result": "pass" if len(LOCAL_LOCK_PREFLIGHT_ROWS) == 8 and len(FIRST_LOCK_ATTEMPT_ROWS) == 1 else "fail",
            "detail": f"lock_preflight_rows={len(LOCAL_LOCK_PREFLIGHT_ROWS)};first_lock_rows={len(FIRST_LOCK_ATTEMPT_ROWS)}",
        },
        {
            "check_id": "V551_6_no_claim_rows",
            "result": "pass" if not claim_envelope_rows and not claim_lock_rows and not claim_first_lock_rows else "fail",
            "detail": f"claim_envelope={len(claim_envelope_rows)};claim_lock={len(claim_lock_rows)};claim_first_lock={len(claim_first_lock_rows)}",
        },
        {
            "check_id": "V551_7_demote_not_overclaim",
            "result": "pass" if not claim_envelope_rows and not claim_lock_rows and not claim_first_lock_rows else "fail",
            "detail": "BRR545_filled=false; first_local_lock_passed=false; local_GR_claim_allowed=false; closure_only_label_active=true",
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
    return f"""# 551 - Y5 BRR545 Residual Envelope and First Local Lock Fill or Demotion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The BRR545 local transition branch is now an explicit residual envelope, not a hidden assumption.

The first local lock cannot be filled honestly. The tightest immediate gate is `R7_alpha3`, and it needs boundary/projector amplitudes, coefficients, or theorem-zero certificates that do not yet exist.

So this route is demoted to closure-only until repaired. That is not a physical disproof of MTS. It is a proof-discipline label: the current branch cannot be advertised as derived local GR.

## 2. Strict BRR545 Residual Envelope

{markdown_table(RESIDUAL_ENVELOPE_ROWS)}

## 3. Local Lock Preflight

{markdown_table(LOCAL_LOCK_PREFLIGHT_ROWS)}

## 4. First Local Lock Attempt

{markdown_table(FIRST_LOCK_ATTEMPT_ROWS)}

## 5. Closure Demotion Decision

{markdown_table(CLOSURE_DEMOTION_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
MTS has an explicit BRR545 residual envelope.
MTS has attempted the first local lock preflight and found it unfillable with current rows.
MTS has labelled the current local-GR transition route closure-only until repaired.
```

Forbidden:

```text
MTS has passed BRR545.
MTS has filled a local PPN/source lock.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 10. Practical Read

This is the kind of ugly-looking checkpoint that actually makes the framework stronger. We have stopped the proof from sneaking a quiet boundary/projector/reference term through the back door. The next repair has to be structural: a parent action theorem that makes the whole BRR545 envelope vanish or owns every residual as an observable coefficient.

## 11. Next Target

`{NEXT_TARGET}`

Next: write the exact parent-action contract that would turn the closure-only branch back into a derivation route.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-BRR545-residual-envelope-and-first-local-lock-fill-or-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (RESIDUAL_ENVELOPE_PATH, RESIDUAL_ENVELOPE_ROWS),
        (LOCAL_LOCK_PREFLIGHT_PATH, LOCAL_LOCK_PREFLIGHT_ROWS),
        (FIRST_LOCK_ATTEMPT_PATH, FIRST_LOCK_ATTEMPT_ROWS),
        (CLOSURE_DEMOTION_PATH, CLOSURE_DEMOTION_ROWS),
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
        "residual_envelope": str(ROOT / RESIDUAL_ENVELOPE_PATH),
        "local_lock_preflight": str(ROOT / LOCAL_LOCK_PREFLIGHT_PATH),
        "first_lock_attempt": str(ROOT / FIRST_LOCK_ATTEMPT_PATH),
        "closure_demotion": str(ROOT / CLOSURE_DEMOTION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "residual_envelope_rows": len(RESIDUAL_ENVELOPE_ROWS),
        "local_lock_preflight_rows": len(LOCAL_LOCK_PREFLIGHT_ROWS),
        "first_local_lock_attempt_rows": len(FIRST_LOCK_ATTEMPT_ROWS),
        "BRR545_values_filled": False,
        "first_local_lock_passed": False,
        "closure_only_label_active": True,
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
        "done\nprivate_no_github\nBRR545_residual_envelope_written_first_local_lock_not_fillable_local_GR_route_closure_only_until_repaired_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
