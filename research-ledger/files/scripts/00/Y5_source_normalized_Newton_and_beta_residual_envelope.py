from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_source_normalized_Newton_and_beta_residual_envelope_written_missing_components_no_beta_or_local_GR_promotion"
CLAIM_CEILING = "source_normalized_Newton_and_beta_residual_envelope_only_no_Newton_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md"

DOC_PATH = Path("531-Y5-source-normalized-Newton-and-beta-residual-envelope.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_SOURCE_REGISTER.csv")
COMPONENTS_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_COMPONENTS.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_EVALUATOR.csv")
NEWTON_GATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NEWTON_PRECONDITION_GATE.csv")
INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_INPUT_TEMPLATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_ENVELOPE_ROUTE_UPDATE.csv")

BETA_BOUND_DEFAULT = 7.8e-5


SOURCE_REGISTER = [
    {
        "source_file": "530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md",
        "role": "R11 beta component vector and EH/no-hair theorem target",
    },
    {
        "source_file": "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
        "role": "source-calibrated EH family proof stack",
    },
    {
        "source_file": "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md",
        "role": "EH mass-parameter route to B=A^2",
    },
    {
        "source_file": "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md",
        "role": "beta demotion residual equation and no-cancellation policy",
    },
    {
        "source_file": "526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md",
        "role": "beta evaluator and provisional q_loc U2 budget",
    },
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "PPN vector gate for beta/gamma/alpha_i/xi",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "source-normalized measured-GM precondition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
        "role": "530 component vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv",
        "role": "526 beta evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv",
        "role": "526 q_loc provisional bound and missing conversion rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "523 measured-GM/source residual scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_DEMOTION_RESIDUAL_ROW.csv",
        "role": "527 beta residual row definitions",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local beta/gamma/PPN bound manifest",
    },
    {
        "source_file": "scripts/Y5_source_normalized_Newton_and_beta_residual_envelope.py",
        "role": "this checkpoint generator",
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


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def beta_bound() -> float:
    evaluator = read_csv(Path("source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv"))
    for row in evaluator:
        value = parse_float(row.get("beta_bound"))
        if value is not None:
            return value
    return BETA_BOUND_DEFAULT


def qloc_budget_rows(bound: float) -> tuple[float | None, float | None, float | None]:
    qloc = read_csv(Path("source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv"))
    beta_budget: float | None = None
    beta_ratio: float | None = None
    alpha3_ratio: float | None = None
    for row in qloc:
        if row.get("bound_id") == "QBU526_0_compact_shell_to_beta_if_same_normalization":
            beta_budget = parse_float(row.get("input_value"))
            beta_ratio = parse_float(row.get("bound_ratio"))
        if row.get("bound_id") == "QBU526_1_compact_shell_to_alpha3_warning":
            alpha3_ratio = parse_float(row.get("bound_ratio"))
    if beta_budget is not None and beta_ratio is None:
        beta_ratio = beta_budget / bound
    return beta_budget, beta_ratio, alpha3_ratio


def envelope_components(bound: float) -> list[dict[str, Any]]:
    qloc_budget, qloc_beta_ratio, qloc_alpha3_ratio = qloc_budget_rows(bound)
    return [
        {
            "component_id": "ENV531_0_first_order_Newton_precondition",
            "symbol": "source_normalized_Newton_precondition",
            "formula_or_map": "measured_mu=G0*M_H with zero source/range/time/frame/domain residuals",
            "current_value": "",
            "absolute_value_for_sum": "",
            "status": "fail_523_scorecard_unfilled",
            "claim_effect": "blocks_beta_PPN_even_if_second_order_components_later_fill",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_1_source_AB",
            "symbol": "delta_beta_source",
            "formula_or_map": "B_source/A_source^2 - 1",
            "current_value": "MISSING_A_SOURCE_AND_B_SOURCE",
            "absolute_value_for_sum": "",
            "status": "missing",
            "claim_effect": "blocks_envelope_evaluation",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_2_R11_operator_sum",
            "symbol": "sum_i_abs_delta_beta_R11_i",
            "formula_or_map": "sum over 530 R11 beta component vector absolute values",
            "current_value": "MISSING_R11_COEFFICIENT_VECTOR_OR_EH_NOHAIR",
            "absolute_value_for_sum": "",
            "status": "missing",
            "claim_effect": "blocks_envelope_evaluation",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_3_q_loc",
            "symbol": "delta_beta_q_loc",
            "formula_or_map": "physical U2 projection of P_loc(nabla Gamma_eff - div Khat)",
            "current_value": "" if qloc_budget is None else qloc_budget,
            "absolute_value_for_sum": "" if qloc_budget is None else qloc_budget,
            "status": "provisional_same_normalization_only_not_claimable",
            "claim_effect": "interesting_beta_budget_but_blocks_until_U2_conversion_and_alpha3_projection_are_resolved",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_4_boundary_domain",
            "symbol": "delta_beta_boundary_domain",
            "formula_or_map": "boundary/domain/projector quadratic stress beta projection",
            "current_value": "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "absolute_value_for_sum": "",
            "status": "missing",
            "claim_effect": "blocks_envelope_evaluation",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_5_readout_frame",
            "symbol": "delta_beta_readout",
            "formula_or_map": "second-order mismatch between source metric and observed isotropic PPN readout",
            "current_value": "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "absolute_value_for_sum": "",
            "status": "missing",
            "claim_effect": "blocks_envelope_evaluation",
            "valid_for_claim": "false",
        },
        {
            "component_id": "ENV531_6_q_loc_alpha3_guard",
            "symbol": "q_loc_alpha3_projection_warning",
            "formula_or_map": "same compact q_loc budget compared to alpha3 if it leaks into momentum-flux/preferred-frame rows",
            "current_value": "" if qloc_alpha3_ratio is None else qloc_alpha3_ratio,
            "absolute_value_for_sum": "not_beta_sum_component",
            "status": "severe_warning_if_projection_applies",
            "claim_effect": "blocks_local_GR_even_if_beta_budget_looks_small",
            "valid_for_claim": "false",
        },
    ]


def envelope_evaluator(bound: float) -> list[dict[str, Any]]:
    qloc_budget, qloc_beta_ratio, qloc_alpha3_ratio = qloc_budget_rows(bound)
    missing_components = [
        "source_normalized_Newton_precondition",
        "delta_beta_source",
        "sum_i_abs_delta_beta_R11_i",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "q_loc_U2_conversion_or_Ward_zero",
    ]
    provisional_sum = qloc_budget
    provisional_ratio = qloc_beta_ratio
    return [
        {
            "evaluator_id": "BE531_0_strict_claim_envelope",
            "mode": "strict_claim",
            "included_components": "source_AB;R11_i;q_loc;boundary_domain;readout",
            "missing_components": ";".join(missing_components),
            "total_abs_beta_envelope": "",
            "beta_bound": bound,
            "bound_ratio": "",
            "result": "not_evaluable_missing_components",
            "valid_for_claim": "false",
        },
        {
            "evaluator_id": "BE531_1_provisional_q_loc_only",
            "mode": "diagnostic_not_claim",
            "included_components": "q_loc_compact_shell_if_same_beta_normalization",
            "missing_components": "all_other_components_assumed_zero_only_for_diagnostic",
            "total_abs_beta_envelope": "" if provisional_sum is None else provisional_sum,
            "beta_bound": bound,
            "bound_ratio": "" if provisional_ratio is None else provisional_ratio,
            "result": "below_beta_lock_if_same_normalization" if provisional_ratio is not None and provisional_ratio < 1 else "not_available_or_above",
            "valid_for_claim": "false",
        },
        {
            "evaluator_id": "BE531_2_alpha3_guard",
            "mode": "local_GR_guard_not_beta_sum",
            "included_components": "q_loc_compact_shell_if_same_preferred_frame_projection",
            "missing_components": "physical_projection_map",
            "total_abs_beta_envelope": "not_beta_envelope",
            "beta_bound": "alpha3_bound_4e-20",
            "bound_ratio": "" if qloc_alpha3_ratio is None else qloc_alpha3_ratio,
            "result": "severe_warning_if_projection_applies",
            "valid_for_claim": "false",
        },
        {
            "evaluator_id": "BE531_3_no_cancellation_policy",
            "mode": "policy",
            "included_components": "absolute_values_only",
            "missing_components": "none_can_be_cancelled_by_tuning",
            "total_abs_beta_envelope": "sum_abs_components_required",
            "beta_bound": bound,
            "bound_ratio": "",
            "result": "policy_enforced",
            "valid_for_claim": "false",
        },
    ]


def newton_gate_rows() -> list[dict[str, str]]:
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    unfilled = [row for row in scorecard if row.get("score_status") != "pass" or row.get("valid_for_claim") != "true"]
    return [
        {
            "gate_id": "NG531_0_scorecard_loaded",
            "gate": "source-normalization scorecard exists",
            "current_status": "pass" if scorecard else "fail",
            "detail": f"scorecard_rows={len(scorecard)}",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG531_1_measured_GM_precondition",
            "gate": "all measured-GM/source-normalization residuals are zero or bounded with source paths",
            "current_status": "fail_unfilled",
            "detail": f"unfilled_or_unclaimable_rows={len(unfilled)}",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG531_2_first_order_before_beta",
            "gate": "Newton/source precondition must pass before beta can be promoted",
            "current_status": "fail_current_branch",
            "detail": "beta is second-order PPN; first-order measured-GM chain remains open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG531_3_no_absorption_cheat",
            "gate": "range/time/species/frame/domain dependence cannot be hidden inside measured GM",
            "current_status": "pass_policy_enforced",
            "detail": "dependent source-normalization channels stay explicit",
            "valid_for_claim": "false",
        },
    ]


def input_template_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "IN531_0_A_B",
            "component": "delta_beta_source",
            "required_artifact": "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv with numeric A_source,B_source or theorem B=A^2",
            "acceptance": "source file exists; units/normalization declared; beta_eff computed",
            "priority": "highest",
        },
        {
            "input_id": "IN531_1_R11",
            "component": "sum_i_abs_delta_beta_R11_i",
            "required_artifact": "R11 beta component coefficient vector or EH/no-hair theorem-zero source",
            "acceptance": "every 530 component valid_for_claim=true or theorem-zeroed",
            "priority": "highest",
        },
        {
            "input_id": "IN531_2_q_loc",
            "component": "delta_beta_q_loc",
            "required_artifact": "q_loc physical U2 conversion/profile or Ward-zero through O(U2)",
            "acceptance": "beta map below bound and alpha_i/xi projection separately safe",
            "priority": "high",
        },
        {
            "input_id": "IN531_3_boundary_domain",
            "component": "delta_beta_boundary_domain",
            "required_artifact": "boundary/domain/projector no-flux/no-stress theorem or coefficient map",
            "acceptance": "beta plus alpha3/xi gates pass without cancellation",
            "priority": "high",
        },
        {
            "input_id": "IN531_4_readout",
            "component": "delta_beta_readout",
            "required_artifact": "same observed coframe/readout theorem through O(U2)",
            "acceptance": "source metric and observed PPN metric are identical through beta order",
            "priority": "high",
        },
        {
            "input_id": "IN531_5_Newton_precondition",
            "component": "source_normalized_Newton_precondition",
            "required_artifact": "523 source-normalization scorecard filled or theorem-zeroed",
            "acceptance": "measured_mu=GM and derivative hair zero/bounded",
            "priority": "highest",
        },
    ]


DECISION_ROWS = [
    {
        "decision_id": "D531_0_envelope_written",
        "status": "strict_no_cancellation_beta_envelope_written",
        "meaning": "the beta pass condition is now an explicit absolute-sum envelope rather than a hidden closure",
        "claim_status": "not_evaluable_missing_components",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D531_1_q_loc_interesting_but_not_claim",
        "status": "q_loc_below_beta_if_same_normalization_but_alpha3_guard_severe",
        "meaning": "q_loc is not automatically fatal for beta, but it cannot be counted until physical U2 and preferred-frame projections are derived",
        "claim_status": "diagnostic_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D531_2_source_Newton_blocks_PPN",
        "status": "measured_GM_precondition_unfilled",
        "meaning": "beta cannot promote local GR while first-order source-normalized Newton is still unearned",
        "claim_status": "Newton_PPN_local_GR_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D531_3_next_target",
        "status": "attack_measured_GM_source_current_closure",
        "meaning": "the fastest derivable route is now to close or fill the measured-GM/source-current chain before trying to score beta",
        "claim_status": "active_private_research",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D531_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BETA_ENVELOPE",
        "previous_status": "ready_for_no_cancellation_envelope_after_component_inputs",
        "new_status": "strict_envelope_written_missing_components_not_evaluable",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_U2",
        "previous_status": "explicit_beta_component_retained_until_physical_U2_map_or_Ward_zero",
        "new_status": "diagnostic_beta_budget_retained_alpha3_guard_blocks_promotion",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "central_blocker_in_EH_family_stack",
        "new_status": "first_order_precondition_for_beta_and_local_GR",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_BETA_VECTOR",
        "previous_status": "component_vector_written_all_rows_unfilled_or_template_only",
        "new_status": "feeds_strict_envelope_but_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_R11_beta_components_unfilled_and_EH_nohair_not_derived",
        "new_status": "still_blocked_Newton_precondition_and_beta_envelope_missing_components",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def validation_rows(sources: list[dict[str, Any]], components: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    beta_component_vector = read_csv(Path("source-intake/mts_residuals/P8_Y5_R11_BETA_COMPONENT_VECTOR.csv"))
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    qloc = read_csv(Path("source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv"))
    claim_rows = [row for row in components if row["valid_for_claim"] == "true"]
    strict_rows = [row for row in evaluator if row["evaluator_id"] == "BE531_0_strict_claim_envelope"]
    return [
        {
            "check_id": "V531_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V531_1_prior_component_vector_loaded",
            "result": "pass" if len(beta_component_vector) == 12 else "fail",
            "detail": f"component_vector_rows={len(beta_component_vector)}",
        },
        {
            "check_id": "V531_2_scorecard_and_q_loc_loaded",
            "result": "pass" if len(scorecard) >= 12 and len(qloc) >= 4 else "fail",
            "detail": f"scorecard_rows={len(scorecard)};q_loc_rows={len(qloc)}",
        },
        {
            "check_id": "V531_3_components_written",
            "result": "pass" if len(components) == 7 else "fail",
            "detail": f"component_rows={len(components)}",
        },
        {
            "check_id": "V531_4_evaluator_written",
            "result": "pass" if len(evaluator) == 4 else "fail",
            "detail": f"evaluator_rows={len(evaluator)}",
        },
        {
            "check_id": "V531_5_strict_envelope_not_claimable",
            "result": "pass" if strict_rows and strict_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": strict_rows[0]["result"] if strict_rows else "missing_strict_row",
        },
        {
            "check_id": "V531_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V531_7_no_overclaim",
            "result": "pass" if not claim_rows else "fail",
            "detail": "source_Newton_derived=false; beta_envelope_passed=false; beta_equals_one_derived=false; local_GR_claim_allowed=false",
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
    components: list[dict[str, Any]],
    evaluator: list[dict[str, Any]],
    newton_gates: list[dict[str, str]],
    inputs: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 531 - Y5 Source-Normalized Newton and Beta Residual Envelope

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The beta problem is now in the right shape:

```text
Delta_beta_total_abs
= |delta_beta_source|
+ sum_i |delta_beta_R11_i|
+ |delta_beta_q_loc|
+ |delta_beta_boundary_domain|
+ |delta_beta_readout|.
```

Current MTS cannot evaluate the strict envelope yet because source A/B, R11 beta components, boundary/domain, readout, and physical q_loc U2 normalization are still missing. Also, source-normalized Newton remains a first-order precondition for any PPN/local-GR claim.

The useful positive hint survives only as a diagnostic: the existing q_loc compact-shell budget is below the beta lock if it is already beta-normalized. That is not claim credit, and the alpha3 guard remains brutal if the same leakage projects into preferred-frame momentum flux.

## 2. Envelope Components

{markdown_table(components)}

## 3. Envelope Evaluator

{markdown_table(evaluator)}

## 4. Source-Normalized Newton Gate

{markdown_table(newton_gates)}

## 5. Required Inputs

{markdown_table(inputs)}

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
The strict beta no-cancellation envelope is explicit.
The q_loc compact-shell result is only a diagnostic below-beta hint under unproved normalization.
Source-normalized Newton is a required precondition for beta/PPN/local-GR promotion.
```

Forbidden:

```text
MTS has passed source-normalized Newton.
MTS has evaluated or passed the strict beta envelope.
MTS has derived beta=1, PPN, or local GR.
```

## 11. Practical Read

This is not a collapse; it is a narrowing. The work now knows where the fight really is: measured GM/source-current closure first, then componentwise beta. If source-normalized Newton closes, the EH mass-family route becomes much more serious. If it does not, the branch stays a testable residual theory instead of pretending to be GR.

## 12. Next Target

`{NEXT_TARGET}`

Next: attack the measured-GM/source-current closure. We either derive the source charge that orbital systems measure, or we fill the first residual inputs and stop letting first-order Newton hide inside notation.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-source-normalized-Newton-and-beta-residual-envelope"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    bound = beta_bound()
    sources = source_rows()
    components = envelope_components(bound)
    evaluator = envelope_evaluator(bound)
    newton_gates = newton_gate_rows()
    inputs = input_template_rows()
    validations = validation_rows(sources, components, evaluator)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (COMPONENTS_PATH, components),
        (EVALUATOR_PATH, evaluator),
        (NEWTON_GATE_PATH, newton_gates),
        (INPUT_TEMPLATE_PATH, inputs),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, components, evaluator, newton_gates, inputs, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    qloc_budget, qloc_beta_ratio, qloc_alpha3_ratio = qloc_budget_rows(bound)
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "components": str(ROOT / COMPONENTS_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "newton_gate": str(ROOT / NEWTON_GATE_PATH),
        "input_template": str(ROOT / INPUT_TEMPLATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "component_rows": len(components),
        "evaluator_rows": len(evaluator),
        "newton_gate_rows": len(newton_gates),
        "beta_bound": bound,
        "q_loc_compact_shell_budget": qloc_budget,
        "q_loc_beta_ratio_if_same_normalization": qloc_beta_ratio,
        "q_loc_alpha3_ratio_if_same_projection": qloc_alpha3_ratio,
        "strict_beta_envelope_written": True,
        "strict_beta_envelope_evaluable": False,
        "source_normalized_Newton_derived": False,
        "beta_envelope_passed": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nno_Newton_beta_PPN_or_local_GR_promotion\n", encoding="utf-8"
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
