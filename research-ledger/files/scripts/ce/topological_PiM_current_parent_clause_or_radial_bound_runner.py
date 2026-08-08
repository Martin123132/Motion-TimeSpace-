from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "topological_PiM_current_parent_clause_written_closed_topological_charge_conditional_Hilbert_equality_not_derived_radial_bound_runner_spec_written_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "topological_PiM_clause_only_no_Hilbert_flux_closure_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "501-topological-Hilbert-current-equality-or-radial-bound-runner.md"

DOC_PATH = Path("500-topological-PiM-current-parent-clause-or-radial-bound-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_SOURCE_REGISTER.csv")
CLAUSE_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv")
CLOSURE_CONDITIONS_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv")
FAILURE_ANALYSIS_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_FAILURE_ANALYSIS.csv")
RADIAL_BOUND_SPEC_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_SPEC.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_ROUTE_UPDATE.csv")

PARENT_SOURCE_IDENTITY_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv")
PARENT_SOURCE_RESIDUAL_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv")
PARENT_SOURCE_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv")
PIM_VARIATION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv")
PIM_FLUX_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "selects topological Pi_M as best next route after source-identity decomposition",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "radial epsilon identity that the topological route is trying to zero",
    },
    {
        "source_file": "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
        "role": "topological projector route and Hodge no-go for metric-only local exterior",
    },
    {
        "source_file": "252-topological-projector-parent-action-skeleton.md",
        "role": "wedge/topological parent skeleton with no Hodge star or bulk metric projector stress",
    },
    {
        "source_file": "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
        "role": "same-projector FLRW compatibility gate and B_mem closure warning",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M algebra and H2 mass-charge projector contract",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "topological mass-current route requirements",
    },
    {
        "source_file": "456-PiM-projector-variation-stress-ledger.md",
        "role": "metric-independent topological Pi_M variation route and Hodge stress retained fork",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "calibration warning for conserved charge versus measured orbital GM",
    },
    {
        "source_file": str(PARENT_SOURCE_IDENTITY_PATH),
        "role": "499 machine identity attempt rows",
    },
    {
        "source_file": str(PARENT_SOURCE_RESIDUAL_PATH),
        "role": "499 machine source residual decomposition",
    },
    {
        "source_file": str(PARENT_SOURCE_TEMPLATE_PATH),
        "role": "499 machine radial fallback template",
    },
    {
        "source_file": str(PIM_VARIATION_CONTRACT_PATH),
        "role": "456 machine projector variation contract",
    },
    {
        "source_file": str(PIM_FLUX_CONTRACT_PATH),
        "role": "455 machine flux closure contract",
    },
    {
        "source_file": "scripts/topological_PiM_current_parent_clause_or_radial_bound_runner.py",
        "role": "this checkpoint generator",
    },
]


CLAUSE_ATTEMPT_ROWS = [
    {
        "clause_id": "TP500_0_topological_data",
        "clause": "absolute mass cohomology data",
        "candidate_form": "choose an oriented compact exterior class [S2] and a metric-independent closed representative omega_M_top with integral_S2 omega_M_top = 1",
        "would_close": "removes Hodge/metric dependence from Pi_M and gives d omega_M_top = 0",
        "current_status": "conditional_from_topological_projector_route",
        "open_debt": "parent domain/topology selector must choose [S2] before readout and without preferred-frame leakage",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_1_closed_topological_charge",
        "clause": "closed topological mass current",
        "candidate_form": "J_M_top = Q_M omega_M_top with dQ_M = 0, hence dJ_M_top = 0",
        "would_close": "constructs a genuinely closed mass-like current with no bulk metric projector stress",
        "current_status": "formal_clause_written_not_identified_with_Hilbert_current",
        "open_debt": "Q_M must be parent-owned and not chosen from measured GM after the fact",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_2_parent_action_skeleton",
        "clause": "wedge-only source clause",
        "candidate_form": "S_topM = int lambda_Q dQ_M + int Lambda_M wedge dJ_M_top + boundary/topological terms, with no Hodge star or sqrt(-g) bulk potential",
        "would_close": "keeps the topological mass current metric-independent in the local exterior",
        "current_status": "conditional_skeleton_legal_as_topological_sector",
        "open_debt": "independent reason for Q_M/lambda_Q/Lambda_M is missing",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_3_Hilbert_equality_gate",
        "clause": "on-shell equality to observed Hilbert mass channel",
        "candidate_form": "Pi_M J_H = J_M_top + dB_zero, with integral_boundary dB_zero = 0",
        "would_close": "would turn the closed topological current into closed Hilbert Pi_M flux",
        "current_status": "not_derived_key_blocker",
        "open_debt": "without equality, the theory has a conserved topological charge but not Newtonian source normalization",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_4_no_extra_projection",
        "clause": "zero extra-current projection",
        "candidate_form": "Pi_M dJ_extra = 0 for boundary, domain, projector, bulk, nonEH, kappa, frame, and species channels",
        "would_close": "kills the projected extra-current term in the 499 identity",
        "current_status": "not_parent_derived",
        "open_debt": "eight residual channels remain unproved or numeric-template-first",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_5_unification_gate",
        "clause": "same topological projector across local and FLRW sectors",
        "candidate_form": "local Pi_M/P_D topological data must be compatible with FLRW memory projector P_D and not be a local-only repair",
        "would_close": "protects the unified-field programme from a local patch",
        "current_status": "conditional_shape_only_Bmem_not_derived",
        "open_debt": "B_mem = 2/27 and FLRW amplitude/rank normalization remain theorem targets",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "TP500_6_calibration_gate",
        "clause": "closed charge to measured orbital GM",
        "candidate_form": "Q_M = M_EH and mu_obs = G_parent Q_M with constant universal G_parent",
        "would_close": "would connect the closed current to Newtonian source normalization",
        "current_status": "not_parent_derived",
        "open_debt": "same-frame Hilbert mass, Poisson/Gauss calibration, constant G, and PPN source stability remain open",
        "valid_for_claim": "false",
    },
]


CLOSURE_CONDITION_ROWS = [
    {
        "condition_id": "TC500_0_metric_independence",
        "condition": "delta_g Pi_M = 0 in the compact local exterior",
        "current_result": "conditional_pass_if_topological_not_Hodge",
        "evidence": "251/252/456 allow wedge/topological route and reject free Hodge projector stress",
        "if_failed": "projector stress becomes R3/R4/R7/R8/R10/R11 residual",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_1_commutator_zero",
        "condition": "[d,Pi_M]J_H = 0",
        "current_result": "conditional_pass_if_PiM_is_fixed_absolute_charge_map",
        "evidence": "topological omega_M_top is closed and metric-independent",
        "if_failed": "499 commutator obstruction remains active",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_2_closed_top_charge",
        "condition": "dJ_M_top = 0",
        "current_result": "formal_clause_pass",
        "evidence": "J_M_top = Q_M omega_M_top with dQ_M=0 and d omega_M_top=0",
        "if_failed": "no topological route remains; use radial template",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_3_Hilbert_equality",
        "condition": "Pi_M J_H = J_M_top plus exact zero-boundary term",
        "current_result": "fail_open",
        "evidence": "no source-current theorem identifies the Hilbert mass channel with the topological charge",
        "if_failed": "closed topological charge is not closed measured mass flux",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_4_no_extra_projection",
        "condition": "Pi_M dJ_extra = 0",
        "current_result": "fail_open",
        "evidence": "499 residual decomposition keeps boundary/domain/bulk/nonEH/kappa/frame/species channels open",
        "if_failed": "epsilon_radial_Meff and mu_extra remain retained or numeric",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_5_no_multiplier_cheat",
        "condition": "no equality multiplier is introduced solely to impose Newtonian source normalization",
        "current_result": "pass_policy_fail_theorem",
        "evidence": "Euler/lambda route remains closure-only unless independently owned",
        "if_failed": "topological clause is demoted to explicit closure axiom",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_6_FLRW_unification",
        "condition": "same topological structure reduces to the FLRW memory projector without retuning",
        "current_result": "conditional_shape_only",
        "evidence": "253 gives shape route but not B_mem amplitude",
        "if_failed": "local topological Pi_M becomes a local repair, not unified field structure",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "TC500_7_calibration",
        "condition": "closed charge is the same-frame Hilbert/Poisson/Gauss/orbital mass with constant universal G",
        "current_result": "fail_open",
        "evidence": "458/498 keep calibration and derivative silence open",
        "if_failed": "Newton/source-normalization remains unpromoted",
        "valid_for_claim": "false",
    },
]


FAILURE_ANALYSIS_ROWS = [
    {
        "failure_id": "F500_0_conserved_wrong_object",
        "failure_mode": "J_M_top is closed but not equal to Pi_M J_H",
        "why_it_matters": "a conserved topological charge is not the mass source measured by local orbits",
        "repair": "derive on-shell Hilbert equality or use radial bound template",
        "current_status": "main_blocker",
    },
    {
        "failure_id": "F500_1_multiplier_relabel",
        "failure_mode": "equality to Pi_M J_H is imposed by a late multiplier",
        "why_it_matters": "this inserts the desired Newton closure rather than deriving it",
        "repair": "give the multiplier first-class/topological/Ward origin and stress ledger",
        "current_status": "forbidden_as_derivation",
    },
    {
        "failure_id": "F500_2_domain_selector_leak",
        "failure_mode": "the S2 class or domain is selected by local metric/readout data",
        "why_it_matters": "Pi_M becomes a preferred-frame/readout mask and can carry source hair",
        "repair": "parent topological/domain selector before readout",
        "current_status": "not_parent_derived",
    },
    {
        "failure_id": "F500_3_FLRW_split",
        "failure_mode": "local Pi_M topological route does not match cosmology P_D route",
        "why_it_matters": "a local-GR repair alone weakens the unified-field claim",
        "repair": "prove common topological projector/rank law across local and FLRW sectors",
        "current_status": "conditional_shape_only",
    },
    {
        "failure_id": "F500_4_calibration_gap",
        "failure_mode": "closed topological charge has wrong normalization or running G",
        "why_it_matters": "Newton measures GM, not a bare conserved cohomology label",
        "repair": "prove Q_M=M_EH and constant universal G in the same observed frame",
        "current_status": "not_parent_derived",
    },
]


RADIAL_BOUND_SPEC_ROWS = [
    {
        "spec_id": "RB500_0_runner_input",
        "object": "parent_identity_integral_table",
        "columns": "system_id;r1;r2;channel;I_channel;I_commutator;I_anomaly;c_M;M_eff_ref;units;source_file;assumptions",
        "purpose": "make the 499 radial numerator executable if theorem route fails",
        "status": "spec_written_not_filled",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "RB500_1_bound_output",
        "object": "epsilon_radial_Meff_bound",
        "columns": "system_id;r1;r2;epsilon_radial_Meff;dln_mu_dlnr;affected_rows;bound_source;pass_fail;notes",
        "purpose": "map source-current residuals to radial measured-GM/source-normalization bounds",
        "status": "spec_written_not_run",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "RB500_2_no_cancellation_policy",
        "object": "channelwise_no_cancellation",
        "columns": "channel;epsilon_channel;bound;source_file;valid_for_claim",
        "purpose": "do not hide a large open row behind cancellation with another open row",
        "status": "policy_written",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "RB500_3_acceptance",
        "object": "radial_row_acceptance",
        "columns": "all_units_declared;all_channels_source_backed;no_claim_rows_open;local_bound_comparison;decision",
        "purpose": "only allow numeric scoring after every residual input has units/source path",
        "status": "gate_written",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D500_0_clause",
        "status": "conditional_clause_written",
        "meaning": "a metric-independent topological Pi_M current clause can be written and would close its own topological current",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D500_1_Hilbert_equality",
        "status": "not_derived",
        "meaning": "the closed topological current has not been proved equal to the observed Hilbert Pi_M source current",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D500_2_radial_bound",
        "status": "runner_spec_written_not_executed",
        "meaning": "if the equality theorem fails, the radial bound runner now has explicit input/output schema",
        "next_action": "build and fill only with sourced residual inputs",
    },
    {
        "decision_id": "D500_3_promotion",
        "status": "forbidden",
        "meaning": "no closed Hilbert flux, mu_extra zero, Newtonian recovery, PPN pass, or local-GR pass is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "TOPOLOGICAL_PIM",
        "previous_status": "best_next_derivation_target_for_commutator_zero_and_stress_silence",
        "new_status": "conditional_topological_current_clause_written_Hilbert_equality_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PARENT_SOURCE_IDENTITY",
        "previous_status": "identity_decomposed_total_conservation_not_Hilbert_closure",
        "new_status": "topological_clause_can_close_JMtop_not_PiM_JH_yet",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RADIAL_BOUND_FALLBACK",
        "previous_status": "radial_numerator_split_into_extra_current_commutator_anomaly",
        "new_status": "bound_runner_schema_written_not_filled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_extra_current_commutator_calibration_and_PPN_source_stability",
        "new_status": "still_blocked_by_Hilbert_equality_extra_projection_calibration_and_PPN_source_stability",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        source_file = row["source_file"]
        rows.append(
            {
                **row,
                "exists": str((ROOT / source_file).exists()),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    identity_rows = read_csv(PARENT_SOURCE_IDENTITY_PATH)
    residual_rows = read_csv(PARENT_SOURCE_RESIDUAL_PATH)
    radial_template_rows = read_csv(PARENT_SOURCE_TEMPLATE_PATH)
    variation_rows = read_csv(PIM_VARIATION_CONTRACT_PATH)
    flux_rows = read_csv(PIM_FLUX_CONTRACT_PATH)

    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_clause_rows = [row for row in CLAUSE_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_condition_rows = [row for row in CLOSURE_CONDITION_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in RADIAL_BOUND_SPEC_ROWS if row["valid_for_claim"] == "true"]
    required_conditions = {
        "TC500_0_metric_independence",
        "TC500_1_commutator_zero",
        "TC500_2_closed_top_charge",
        "TC500_3_Hilbert_equality",
        "TC500_4_no_extra_projection",
        "TC500_5_no_multiplier_cheat",
        "TC500_6_FLRW_unification",
        "TC500_7_calibration",
    }
    condition_ids = {row["condition_id"] for row in CLOSURE_CONDITION_ROWS}

    return [
        {
            "rule_id": "V500_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V500_1_prior_identity_loaded",
            "rule": "499 identity/residual/template rows and PiM contracts are loaded",
            "result": "pass" if identity_rows and residual_rows and radial_template_rows and variation_rows and flux_rows else "fail",
            "evidence": f"identity={len(identity_rows)};residual={len(residual_rows)};template={len(radial_template_rows)};PV={len(variation_rows)};FC={len(flux_rows)}",
            "claim_effect": "500 tied to 499 and PiM gates",
        },
        {
            "rule_id": "V500_2_clause_written",
            "rule": "topological PiM parent clause attempt includes data, closed current, skeleton, Hilbert equality, extra projection, unification, and calibration rows",
            "result": "pass" if len(CLAUSE_ATTEMPT_ROWS) == 7 else "fail",
            "evidence": f"clause_rows={len(CLAUSE_ATTEMPT_ROWS)}",
            "claim_effect": "topological route concrete",
        },
        {
            "rule_id": "V500_3_condition_coverage",
            "rule": "closure conditions cover metric independence, commutator, closed charge, Hilbert equality, extra projection, multiplier, FLRW, and calibration",
            "result": "pass" if required_conditions.issubset(condition_ids) else "fail",
            "evidence": ";".join(sorted(condition_ids)),
            "claim_effect": "no hidden promotion condition",
        },
        {
            "rule_id": "V500_4_bound_runner_spec",
            "rule": "radial bound fallback has input, output, no-cancellation, and acceptance rows",
            "result": "pass" if len(RADIAL_BOUND_SPEC_ROWS) == 4 else "fail",
            "evidence": f"bound_spec_rows={len(RADIAL_BOUND_SPEC_ROWS)}",
            "claim_effect": "test branch explicit but unfilled",
        },
        {
            "rule_id": "V500_5_no_false_claims",
            "rule": "no clause, condition, or bound row is claim-valid",
            "result": "pass" if not claim_clause_rows and not claim_condition_rows and not claim_bound_rows else "fail",
            "evidence": f"clause_claims={len(claim_clause_rows)};condition_claims={len(claim_condition_rows)};bound_claims={len(claim_bound_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 500 - Topological PiM Current Parent Clause Or Radial Bound Runner

Private source-normalization/topological-projector checkpoint. This is not a public closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `499` showed:

```text
d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.
```

The best remaining derivation route is to make `Pi_M` a metric-independent topological mass-current object, not a Hodge/readout projector.

Short answer:

```text
A conditional topological Pi_M clause can be written.
It can close its own topological current J_M_top.
It can kill the Hodge/projector commutator route if Pi_M is genuinely metric-independent.

But it does not yet prove Pi_M J_H = J_M_top.

So the conserved object is not yet the observed Hilbert/measured mass channel.
The radial bound runner schema is written as the fallback.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/topological_PiM_current_parent_clause_or_radial_bound_runner.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Parent Clause Attempt

The usable topological clause is:

```text
J_M_top = Q_M omega_M_top
dQ_M = 0
d omega_M_top = 0
delta_g omega_M_top = 0
```

This closes `J_M_top`. It does not, by itself, prove that the observed Hilbert mass current equals `J_M_top`.

{markdown_table(CLAUSE_ATTEMPT_ROWS)}

## 5. Closure Conditions

{markdown_table(CLOSURE_CONDITION_ROWS)}

## 6. Failure Analysis

{markdown_table(FAILURE_ANALYSIS_ROWS)}

## 7. Radial Bound Runner Spec

If the Hilbert-equality theorem does not land, the next honest path is a bound runner:

{markdown_table(RADIAL_BOUND_SPEC_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
A conditional metric-independent topological Pi_M current clause has been written.
The clause can close J_M_top if Q_M and omega_M_top are parent-owned.
The key remaining theorem is equality between J_M_top and Pi_M J_H.
```

Forbidden:

```text
MTS has derived d(Pi_M J_H)=0.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | the next exact theorem is whether the closed topological current is actually the observed Hilbert Pi_M mass current |
| 2 | radial bound runner implementation | if equality fails, implement the runner spec and fill only sourced residual inputs |
| 3 | calibration lock | even equality still needs measured-GM/Poisson/Gauss and constant universal G |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-topological-PiM-current-parent-clause-or-radial-bound-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (CLAUSE_ATTEMPT_PATH, CLAUSE_ATTEMPT_ROWS),
        (CLOSURE_CONDITIONS_PATH, CLOSURE_CONDITION_ROWS),
        (FAILURE_ANALYSIS_PATH, FAILURE_ANALYSIS_ROWS),
        (RADIAL_BOUND_SPEC_PATH, RADIAL_BOUND_SPEC_ROWS),
        (VALIDATION_PATH, validations),
        (DECISION_PATH, DECISION_ROWS),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
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
        "clause_attempt": str(ROOT / CLAUSE_ATTEMPT_PATH),
        "closure_conditions": str(ROOT / CLOSURE_CONDITIONS_PATH),
        "failure_analysis": str(ROOT / FAILURE_ANALYSIS_PATH),
        "radial_bound_spec": str(ROOT / RADIAL_BOUND_SPEC_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "clause_rows": len(CLAUSE_ATTEMPT_ROWS),
        "condition_rows": len(CLOSURE_CONDITION_ROWS),
        "failure_rows": len(FAILURE_ANALYSIS_ROWS),
        "radial_bound_spec_rows": len(RADIAL_BOUND_SPEC_ROWS),
        "failed_validation_rows": len(failed_validations),
        "topological_PiM_clause_written": True,
        "closed_topological_charge_constructed_conditionally": True,
        "Hilbert_topological_current_equality_derived": False,
        "projected_extra_current_zero_derived": False,
        "calibration_lock_derived": False,
        "radial_bound_runner_spec_written": True,
        "radial_bound_runner_executed": False,
        "Hilbert_PiM_flux_closed_parent_derived": False,
        "epsilon_radial_Meff_zero_derived": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
