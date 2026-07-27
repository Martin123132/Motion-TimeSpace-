from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_beta_coefficient_runner_and_q_loc_U2_bound_written_missing_AB_inputs_no_beta_or_local_GR_promotion"
CLAIM_CEILING = "beta_coefficient_fill_runner_or_q_loc_U2_bound_only_no_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md"

DOC_PATH = Path("526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_QLOC_SOURCE_REGISTER.csv")
COEFFICIENT_INPUT_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv")
QLOC_U2_BOUND_PATH = Path("source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_QLOC_ACCEPTANCE_GATES.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_QLOC_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_QLOC_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_QLOC_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "525-Y5-delta-beta-source-expansion-or-R11-input-fill.md",
        "role": "exact beta law beta_eff=B/A^2 and required A/B/R11/q_loc inputs",
    },
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "PPN residual vector requiring delta_beta_source and q_loc U2 handling",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "first-order measured-GM/source-normalization precondition",
    },
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc as projected divergence of T_GK and residual-demotion rule",
    },
    {
        "source_file": "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "candidate GK stress action and residual-bound branch",
    },
    {
        "source_file": "303-second-order-beta-response-attempt.md",
        "role": "prior beta law and linearized beta guard",
    },
    {
        "source_file": "304-epsilon-loc-beta-guard-update.md",
        "role": "conservative beta guard for nonzero epsilon_loc leakage",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv",
        "role": "525 input requirements for A_source, B_source, R11, q_loc, boundary, and readout",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_DELTA_BETA_R11_LINK.csv",
        "role": "525 beta-relevant R11 operator family mapping",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "role": "524 PPN residual vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "role": "existing q_loc bound runner spec with compact-shell budget",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
        "role": "triggers for q_loc residual-bound branch",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "R11 status showing operator-vector rows are not executable claim rows",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "official local beta and PPN locks",
    },
    {
        "source_file": "scripts/Y5_beta_coefficient_fill_runner_or_q_loc_U2_bound.py",
        "role": "this checkpoint generator",
    },
]


COEFFICIENT_INPUT_ROWS = [
    {
        "model_id": "MTS_local_GR_branch",
        "branch_id": "Y5_beta_coefficient_fill_runner",
        "row_id": "BETA526_0_source_AB",
        "A_source": "MISSING_A_SOURCE",
        "B_source": "MISSING_B_SOURCE",
        "delta_beta_R11": "MISSING_OR_ZERO_THEOREM",
        "delta_beta_q_loc": "MISSING_OR_ZERO_THEOREM",
        "delta_beta_boundary_domain": "MISSING_OR_ZERO_THEOREM",
        "delta_beta_readout": "MISSING_OR_ZERO_THEOREM",
        "normalization": "g00=-1+2 A W/c^2 - 2 B W^2/c^4; U=A W; beta_eff=B/A^2",
        "source_file": "fill_second_order_source_equation_or_R11_vector",
        "derivation_status": "unfilled_template",
        "valid_for_claim": "false",
    },
    {
        "model_id": "MTS_local_GR_branch",
        "branch_id": "Y5_beta_coefficient_fill_runner",
        "row_id": "BETA526_1_GR_target_reference",
        "A_source": "1",
        "B_source": "1",
        "delta_beta_R11": "0",
        "delta_beta_q_loc": "0",
        "delta_beta_boundary_domain": "0",
        "delta_beta_readout": "0",
        "normalization": "reference-only GR target; not current MTS evidence",
        "source_file": "reference_case_not_claim_evidence",
        "derivation_status": "reference_target_only",
        "valid_for_claim": "false",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "BG526_0_A_B_loaded",
        "pass_condition": "A_source and B_source are numeric or theorem-zero/square-certified from a source equation",
        "current_result": "fail_missing_current_MTS_A_B",
        "claim_effect": "blocks_delta_beta_source_claim",
    },
    {
        "gate_id": "BG526_1_beta_law_evaluated",
        "pass_condition": "delta_beta_source=B_source/A_source^2-1 is computed with source path and units",
        "current_result": "runner_available_but_current_branch_missing_inputs",
        "claim_effect": "no_beta_claim",
    },
    {
        "gate_id": "BG526_2_q_loc_U2_bound_mapped",
        "pass_condition": "q_loc U2 coefficient has same normalization as beta residual or explicit conversion factor",
        "current_result": "provisional_compact_shell_budget_only",
        "claim_effect": "cannot_promote_q_loc_silence",
    },
    {
        "gate_id": "BG526_3_R11_beta_coefficients_supplied",
        "pass_condition": "all beta-relevant R11 operator families have executable coefficient rows or theorem-zero proof",
        "current_result": "fail_R11_template_only",
        "claim_effect": "blocks_beta_and_local_GR",
    },
    {
        "gate_id": "BG526_4_total_no_cancellation_envelope",
        "pass_condition": "total beta envelope is the sum of absolute components and is below beta lock",
        "current_result": "not_run_missing_components",
        "claim_effect": "no_cancellation_credit",
    },
    {
        "gate_id": "BG526_5_first_order_precondition",
        "pass_condition": "523 first-order measured-GM/source-normalization scorecard is zero or scored below locks",
        "current_result": "fail_523_scorecard_unfilled",
        "claim_effect": "blocks_PPN_even_if_beta_runner_fills",
    },
    {
        "gate_id": "BG526_6_no_overclaim",
        "pass_condition": "no beta/PPN/local-GR claim is made from templates, reference rows, or provisional q_loc budget",
        "current_result": "pass_policy_enforced",
        "claim_effect": "safe_private_checkpoint",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D526_0_runner_written",
        "status": "beta_coefficient_runner_written",
        "meaning": "A/B coefficient rows can now be filled and evaluated with beta_eff=B/A^2",
        "claim_status": "runner_only_no_beta_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D526_1_current_inputs_missing",
        "status": "current_MTS_A_B_missing",
        "meaning": "no current source equation supplies A_source and B_source, so delta_beta_source is not evaluated for claim",
        "claim_status": "blocks_PPN_and_local_GR",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D526_2_q_loc_budget_provisional",
        "status": "compact_shell_budget_below_beta_lock_if_same_normalization",
        "meaning": "existing q_loc compact-shell budget is smaller than the beta lock, but normalization to beta U2 is not proven",
        "claim_status": "interesting_not_claimable",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D526_3_alpha3_warning",
        "status": "q_loc_alpha3_projection_still_severe",
        "meaning": "even if beta-normalized q_loc is small, momentum-flux/preferred-frame projection may hit the alpha3 lock and must be separately mapped",
        "claim_status": "blocks_local_GR",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D526_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "all outputs remain private post-checkpoint derivation work",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BETA_COEFFICIENT_FILL_RUNNER",
        "previous_status": "A_source_B_source_required_after_525",
        "new_status": "runner_and_input_template_written_current_inputs_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_U2_BOUND",
        "previous_status": "q_loc_U2_beta_bound_missing",
        "new_status": "compact_shell_budget_checked_as_provisional_beta_bound_same_normalization_not_proved",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_BETA_CHANNELS",
        "previous_status": "beta_relevant_operator_families_mapped_to_missing_coefficients",
        "new_status": "still_template_only_and_blocks_beta_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON_TO_PPN",
        "previous_status": "first_order_scorecard_unfilled",
        "new_status": "still_precondition_for_PPN_even_if_beta_coefficients_are_filled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_A_B_coefficients_R11_vector_and_q_loc_U2_bound_missing",
        "new_status": "still_blocked_current_beta_inputs_missing_q_loc_normalization_not_proved_and_R11_template_only",
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


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.lower() in {"not_loaded", "fill", "symbolic"}:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if math.isfinite(parsed):
        return parsed
    return None


def get_local_bound(row_id: str, observable: str | None = None) -> float | None:
    for row in read_csv(Path("source-intake/local_bounds/local_bound_claims.csv")):
        if row.get("row_id") != row_id:
            continue
        if observable is not None and row.get("observable") != observable:
            continue
        parsed = parse_float(row.get("upper_bound"))
        if parsed is not None:
            return parsed
    return None


def get_q_loc_compact_budget() -> float | None:
    for row in read_csv(Path("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv")):
        if row.get("bound_id") == "QB516_0_compact_shell_budget":
            return parse_float(row.get("current_bound"))
    return None


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def evaluator_rows(beta_bound: float | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in COEFFICIENT_INPUT_ROWS:
        a_source = parse_float(row["A_source"])
        b_source = parse_float(row["B_source"])
        components = {
            "delta_beta_R11": parse_float(row["delta_beta_R11"]),
            "delta_beta_q_loc": parse_float(row["delta_beta_q_loc"]),
            "delta_beta_boundary_domain": parse_float(row["delta_beta_boundary_domain"]),
            "delta_beta_readout": parse_float(row["delta_beta_readout"]),
        }
        missing_components = [name for name, value in components.items() if value is None]
        if a_source is None or b_source is None or a_source == 0:
            beta_eff = ""
            delta_beta_source = ""
            total_envelope = ""
            beta_bound_ratio = ""
            current_status = "not_run_missing_A_or_B"
        else:
            beta_eff_value = b_source / (a_source * a_source)
            delta_beta_source_value = beta_eff_value - 1.0
            beta_eff = f"{beta_eff_value:.16g}"
            delta_beta_source = f"{delta_beta_source_value:.16g}"
            if missing_components:
                total_envelope = ""
                beta_bound_ratio = ""
                current_status = "partial_run_missing_component_splits"
            else:
                total = abs(delta_beta_source_value) + sum(abs(value) for value in components.values() if value is not None)
                total_envelope = f"{total:.16g}"
                beta_bound_ratio = f"{total / beta_bound:.16g}" if beta_bound else ""
                current_status = "below_beta_lock_reference_only" if beta_bound and total <= beta_bound else "above_or_unbounded_beta_lock"
        valid_for_claim = (
            "true"
            if row["valid_for_claim"] == "true"
            and current_status == "below_beta_lock_reference_only"
            and not missing_components
            else "false"
        )
        rows.append(
            {
                "model_id": row["model_id"],
                "row_id": row["row_id"],
                "A_source": row["A_source"],
                "B_source": row["B_source"],
                "beta_eff": beta_eff,
                "delta_beta_source": delta_beta_source,
                "delta_beta_R11": row["delta_beta_R11"],
                "delta_beta_q_loc": row["delta_beta_q_loc"],
                "delta_beta_boundary_domain": row["delta_beta_boundary_domain"],
                "delta_beta_readout": row["delta_beta_readout"],
                "missing_components": ";".join(missing_components),
                "total_abs_beta_envelope": total_envelope,
                "beta_bound": beta_bound if beta_bound is not None else "",
                "beta_bound_ratio": beta_bound_ratio,
                "current_status": current_status,
                "valid_for_claim": valid_for_claim,
                "notes": "reference rows are not current MTS evidence; claim requires real source path and first-order precondition",
            }
        )
    return rows


def q_loc_u2_bound_rows(beta_bound: float | None, alpha3_bound: float | None) -> list[dict[str, Any]]:
    q_loc_budget = get_q_loc_compact_budget()
    beta_ratio = q_loc_budget / beta_bound if q_loc_budget is not None and beta_bound else None
    alpha3_ratio = q_loc_budget / alpha3_bound if q_loc_budget is not None and alpha3_bound else None
    return [
        {
            "bound_id": "QBU526_0_compact_shell_to_beta_if_same_normalization",
            "input_quantity": "compact_shell_q_loc_budget",
            "input_value": q_loc_budget if q_loc_budget is not None else "",
            "target_row": "R4_beta",
            "target_bound": beta_bound if beta_bound is not None else "",
            "mapping_assumption": "q_loc budget is already dimensionless beta-equivalent U2 coefficient",
            "bound_ratio": f"{beta_ratio:.16g}" if beta_ratio is not None else "",
            "provisional_result": "below_beta_lock_if_same_normalization" if beta_ratio is not None and beta_ratio <= 1 else "not_evaluable_or_above",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBU526_1_compact_shell_to_alpha3_warning",
            "input_quantity": "compact_shell_q_loc_budget",
            "input_value": q_loc_budget if q_loc_budget is not None else "",
            "target_row": "R7_alpha3",
            "target_bound": alpha3_bound if alpha3_bound is not None else "",
            "mapping_assumption": "same q_loc leakage projects into alpha3-equivalent momentum-flux coefficient",
            "bound_ratio": f"{alpha3_ratio:.16g}" if alpha3_ratio is not None else "",
            "provisional_result": "alpha3_lock_would_be_extremely_severe_if_this_projection_applies" if alpha3_ratio is not None and alpha3_ratio > 1 else "not_evaluable_or_below",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBU526_2_required_U2_conversion",
            "input_quantity": "q_loc_U2_conversion_factor",
            "input_value": "MISSING_CONVERSION",
            "target_row": "delta_beta_q_loc",
            "target_bound": beta_bound if beta_bound is not None else "",
            "mapping_assumption": "q_loc^i must be written as c_q (U/c^2) grad^i U or directly as delta_beta_q_loc",
            "bound_ratio": "",
            "provisional_result": "conversion_missing_no_claim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBU526_3_required_source_path",
            "input_quantity": "q_loc_profile_or_theorem",
            "input_value": "MISSING_PROFILE_OR_WARD_ZERO",
            "target_row": "PPN524_7_q_loc_second_order_force",
            "target_bound": "derived_zero_or_componentwise_PPN_bounds",
            "mapping_assumption": "Gamma_eff/K_hat sector either proves Ward-zero through O(U2) or supplies a q_loc profile",
            "bound_ratio": "",
            "provisional_result": "not_derived_zero",
            "valid_for_claim": "false",
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    evaluator: list[dict[str, Any]],
    q_loc_bounds: list[dict[str, Any]],
    beta_bound: float | None,
    alpha3_bound: float | None,
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    delta_beta_inputs = read_csv(Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv"))
    ppn_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv"))
    qloc_spec_rows = read_csv(Path("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv"))
    claim_input_rows = [row for row in COEFFICIENT_INPUT_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator if row["valid_for_claim"] == "true"]
    claim_q_rows = [row for row in q_loc_bounds if row["valid_for_claim"] == "true"]
    current_mts_eval = [row for row in evaluator if row["row_id"] == "BETA526_0_source_AB"]
    current_mts_status = current_mts_eval[0]["current_status"] if current_mts_eval else "missing"
    return [
        {
            "check_id": "V526_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V526_1_prior_delta_beta_inputs_loaded",
            "result": "pass" if len(delta_beta_inputs) >= 7 and len(ppn_rows) >= 12 else "fail",
            "detail": f"delta_beta_inputs={len(delta_beta_inputs)};ppn_rows={len(ppn_rows)}",
        },
        {
            "check_id": "V526_2_local_beta_alpha3_locks_loaded",
            "result": "pass" if beta_bound is not None and alpha3_bound is not None else "fail",
            "detail": f"beta_bound={beta_bound};alpha3_bound={alpha3_bound}",
        },
        {
            "check_id": "V526_3_q_loc_spec_loaded",
            "result": "pass" if len(qloc_spec_rows) >= 5 and get_q_loc_compact_budget() is not None else "fail",
            "detail": f"qloc_spec_rows={len(qloc_spec_rows)};compact_budget={get_q_loc_compact_budget()}",
        },
        {
            "check_id": "V526_4_runner_outputs_written",
            "result": "pass" if len(COEFFICIENT_INPUT_ROWS) == 2 and len(evaluator) == 2 and len(q_loc_bounds) == 4 else "fail",
            "detail": f"input_rows={len(COEFFICIENT_INPUT_ROWS)};evaluator_rows={len(evaluator)};q_loc_bound_rows={len(q_loc_bounds)}",
        },
        {
            "check_id": "V526_5_current_MTS_not_claimed",
            "result": "pass" if current_mts_status == "not_run_missing_A_or_B" else "fail",
            "detail": f"current_MTS_status={current_mts_status}",
        },
        {
            "check_id": "V526_6_no_overclaim",
            "result": "pass" if not claim_input_rows and not claim_eval_rows and not claim_q_rows else "fail",
            "detail": "A_source_computed=false; B_source_computed=false; q_loc_U2_claim=false; beta_equals_one_derived=false; local_GR_claim_allowed=false",
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
    evaluator: list[dict[str, Any]],
    q_loc_bounds: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 526 - Y5 Beta Coefficient Fill Runner or q_loc U2 Bound

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The beta problem is now executable.

The runner takes the law from 525:

```text
beta_eff = B_source / A_source^2
delta_beta_source = beta_eff - 1
```

and turns it into a fill/evaluate table. Current MTS still has no `A_source` or `B_source` coefficient extraction, so the current branch does not pass beta.

There is one interesting provisional result: the existing q_loc compact-shell budget is below the beta lock **if** it is already in beta-equivalent U2 normalization. That if is not proved, and alpha3 remains far more severe if q_loc projects into momentum-flux rows.

## 2. Coefficient Fill Input

{markdown_table(COEFFICIENT_INPUT_ROWS)}

## 3. Beta Evaluator

{markdown_table(evaluator)}

## 4. q_loc U2 Bound

{markdown_table(q_loc_bounds)}

## 5. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

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
The beta coefficient evaluator exists.
The current MTS row fails because A_source and B_source are missing.
The q_loc compact-shell budget is provisionally below the beta lock only under an unproved same-normalization assumption.
```

Forbidden:

```text
MTS has computed A_source or B_source.
MTS has derived beta=1.
MTS has proven q_loc is below PPN bounds in the physical U2 normalization.
MTS has promoted PPN or local GR.
```

## 11. Next Target

`{NEXT_TARGET}`

Next, try to extract `A_source` and `B_source` from an actual second-order source equation. If that cannot be done, beta should be demoted to an explicit residual channel with no local-GR promotion.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    beta_bound = get_local_bound("R4_beta", "beta_minus_1")
    alpha3_bound = get_local_bound("R7_alpha3", "alpha3")
    sources = source_rows()
    evaluator = evaluator_rows(beta_bound)
    q_loc_bounds = q_loc_u2_bound_rows(beta_bound, alpha3_bound)
    validations = validation_rows(sources, evaluator, q_loc_bounds, beta_bound, alpha3_bound)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (COEFFICIENT_INPUT_PATH, COEFFICIENT_INPUT_ROWS),
        (EVALUATOR_PATH, evaluator),
        (QLOC_U2_BOUND_PATH, q_loc_bounds),
        (ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, evaluator, q_loc_bounds, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    q_loc_budget = get_q_loc_compact_budget()
    q_loc_beta_ratio = q_loc_budget / beta_bound if q_loc_budget is not None and beta_bound else None
    q_loc_alpha3_ratio = q_loc_budget / alpha3_bound if q_loc_budget is not None and alpha3_bound else None
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "coefficient_input": str(ROOT / COEFFICIENT_INPUT_PATH),
        "evaluator": str(ROOT / EVALUATOR_PATH),
        "q_loc_u2_bound": str(ROOT / QLOC_U2_BOUND_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "input_rows": len(COEFFICIENT_INPUT_ROWS),
        "evaluator_rows": len(evaluator),
        "q_loc_bound_rows": len(q_loc_bounds),
        "failed_validation_rows": len(failed_validations),
        "beta_bound": beta_bound,
        "alpha3_bound": alpha3_bound,
        "q_loc_compact_shell_budget": q_loc_budget,
        "q_loc_beta_bound_ratio_if_same_normalization": q_loc_beta_ratio,
        "q_loc_alpha3_bound_ratio_if_same_projection": q_loc_alpha3_ratio,
        "beta_coefficient_runner_written": True,
        "current_MTS_A_source_loaded": False,
        "current_MTS_B_source_loaded": False,
        "delta_beta_source_evaluated_for_current_MTS": False,
        "q_loc_U2_physical_normalization_proved": False,
        "q_loc_beta_bound_provisional_below_if_same_normalization": bool(q_loc_beta_ratio is not None and q_loc_beta_ratio <= 1),
        "q_loc_alpha3_projection_cleared": False,
        "R11_beta_coefficients_supplied": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
