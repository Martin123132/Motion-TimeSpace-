from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_delta_beta_source_law_derived_AB_coefficients_required_current_MTS_unfilled_no_beta_or_local_GR_promotion"
CLAIM_CEILING = "delta_beta_source_expansion_law_and_input_requirements_only_no_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md"

DOC_PATH = Path("525-Y5-delta-beta-source-expansion-or-R11-input-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_SOURCE_REGISTER.csv")
DERIVATION_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv")
CASE_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_CASES.csv")
INPUT_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv")
R11_LINK_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_R11_LINK.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_DELTA_BETA_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "selects delta_beta_source as the highest-leverage next residual",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "first-order source-normalization scorecard whose residuals can re-enter beta",
    },
    {
        "source_file": "303-second-order-beta-response-attempt.md",
        "role": "prior beta derivation beta_eff=B/A^2 and beta-zero condition b1=2a1",
    },
    {
        "source_file": "304-epsilon-loc-beta-guard-update.md",
        "role": "conservative beta guard for linear-only epsilon_loc leakage",
    },
    {
        "source_file": "229-second-order-beta-or-boundary-scalar-owner.md",
        "role": "boundary scalar owner route and beta reduction to exterior vacuum-Einstein gate",
    },
    {
        "source_file": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "R11/operator families that can contribute to B but are template-only",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "fixed-point conditions requiring metric PPN readout and double zeros",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "Gamma_eff/K_hat/q_loc action-placement debt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "role": "524 PPN residual vector including delta_beta_source",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
        "role": "524 evaluator input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "523 source-normalization residual scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "R11 status showing operator families lack executable coefficient data",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
        "role": "minimum R11 vector skeleton where beta-relevant coefficients are missing",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local beta/gamma/preferred-frame empirical locks",
    },
    {
        "source_file": "scripts/Y5_delta_beta_source_expansion_or_R11_input_fill.py",
        "role": "this checkpoint generator",
    },
]


DERIVATION_ROWS = [
    {
        "step_id": "DB525_0_define_unmeasured_potential",
        "statement": "Use W for the parent weak-field source potential before measured-GM normalization.",
        "math_form": "g_00=-1+2 A W/c^2 - 2 B W^2/c^4 + O(c^-6)",
        "result": "A is the first-order source amplitude; B is the quadratic source response",
        "current_MTS_status": "A_and_B_not_computed",
    },
    {
        "step_id": "DB525_1_normalize_to_measured_U",
        "statement": "The observed Newtonian potential is the first-order calibrated potential.",
        "math_form": "U = A W, with A != 0 on the tested branch",
        "result": "W=U/A",
        "current_MTS_status": "allowed_as_definition_only_not_a_pass",
    },
    {
        "step_id": "DB525_2_extract_beta",
        "statement": "Rewrite the metric in terms of measured U and compare with PPN form.",
        "math_form": "g_00=-1+2U/c^2-2(B/A^2)U^2/c^4+O(c^-6)",
        "result": "beta_eff = B/A^2",
        "current_MTS_status": "derived_kinematic_law",
    },
    {
        "step_id": "DB525_3_beta_residual",
        "statement": "The source-normalization beta residual is the failure of the quadratic response to square the first-order response.",
        "math_form": "delta_beta_source = B_source/A_source^2 - 1",
        "result": "beta is safe only if B_source=A_source^2 after all source/readout/operator splits",
        "current_MTS_status": "law_derived_coefficients_unfilled",
    },
    {
        "step_id": "DB525_4_linearized_guard",
        "statement": "For A=1+a1 epsilon and B=1+b1 epsilon, the first nonzero beta shift is fixed.",
        "math_form": "beta_eff-1 = (b1-2 a1) epsilon + O(epsilon^2)",
        "result": "linear-only leakage has c_beta=-2a1; GR-like completion requires b1=2a1",
        "current_MTS_status": "matches_303_and_304_guard",
    },
    {
        "step_id": "DB525_5_constant_offset_policy",
        "statement": "A constant first-order mass renormalization is harmless only when the second-order coefficient follows the square.",
        "math_form": "A=constant, B=A^2 => beta_eff=1; A=constant, B!=A^2 => beta_eff!=1",
        "result": "GM absorption alone is not enough; nonlinear completion is required",
        "current_MTS_status": "blocks_simple_absorption_overclaim",
    },
    {
        "step_id": "DB525_6_R11_and_q_loc_split",
        "statement": "The observed beta residual must split source-normalization, non-EH operator, q_loc, boundary/domain, and readout pieces before scoring.",
        "math_form": "beta-1 = delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary + delta_beta_readout",
        "result": "each piece needs theorem-zero or executable coefficient input; no cancellation credit",
        "current_MTS_status": "split_written_inputs_unfilled",
    },
]


CASE_ROWS = [
    {
        "case_id": "CASE525_0_exact_GR_silence",
        "A": "1",
        "B": "1",
        "beta_eff": "1",
        "meaning": "no source-normalization or operator leakage",
        "current_status": "target_only_not_current_MTS_derived",
        "valid_for_local_GR_claim": "false",
    },
    {
        "case_id": "CASE525_1_GR_like_mass_renormalization",
        "A": "1+a epsilon",
        "B": "(1+a epsilon)^2",
        "beta_eff": "1",
        "meaning": "constant mass/coupling renormalization is safe only if the quadratic response comes along as the square",
        "current_status": "conditional_safe_pattern_not_derived",
        "valid_for_local_GR_claim": "false",
    },
    {
        "case_id": "CASE525_2_linear_only_source_leak",
        "A": "1+a epsilon",
        "B": "1",
        "beta_eff": "1-2a epsilon+O(epsilon^2)",
        "meaning": "first-order calibration without nonlinear completion creates beta residual",
        "current_status": "guard_required",
        "valid_for_local_GR_claim": "false",
    },
    {
        "case_id": "CASE525_3_wrong_quadratic_completion",
        "A": "1+a epsilon",
        "B": "1+b epsilon with b != 2a",
        "beta_eff": "1+(b-2a)epsilon+O(epsilon^2)",
        "meaning": "beta residual directly measures mismatch between first and second order source response",
        "current_status": "input_required",
        "valid_for_local_GR_claim": "false",
    },
    {
        "case_id": "CASE525_4_scalar_boundary_owner",
        "A": "monopole/common-mode only",
        "B": "requires exterior vacuum-Einstein response",
        "beta_eff": "safe only if exterior branch gives B=A^2",
        "meaning": "scalar boundary symmetry can help gamma/slip, but beta still needs the nonlinear exterior equation",
        "current_status": "reduced_not_solved_from_229",
        "valid_for_local_GR_claim": "false",
    },
    {
        "case_id": "CASE525_5_R11_template_only",
        "A": "unknown",
        "B": "unknown plus c_nonEH contributions",
        "beta_eff": "not computable",
        "meaning": "symbolic non-EH operator ledger cannot pass beta",
        "current_status": "R11_vector_missing",
        "valid_for_local_GR_claim": "false",
    },
]


INPUT_REQUIREMENT_ROWS = [
    {
        "input_id": "BI525_0_A_source",
        "coefficient": "A_source",
        "definition": "first-order g00 source amplitude before measured-GM normalization",
        "required_evidence": "weak-field expansion or theorem showing A_source and its source/range/frame dependence",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_1_B_source",
        "coefficient": "B_source",
        "definition": "quadratic g00 source coefficient from source-normalization sector",
        "required_evidence": "second-order parent/source equation or coefficient extraction",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_2_delta_beta_source",
        "coefficient": "delta_beta_source",
        "definition": "B_source/A_source^2 - 1",
        "required_evidence": "computed from A_source and B_source, then compared to beta_minus_1 lock",
        "current_status": "formula_available_inputs_missing",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_3_delta_beta_R11",
        "coefficient": "delta_beta_R11",
        "definition": "beta contribution from retained non-EH operator families",
        "required_evidence": "R11 executable vector or EH-only theorem",
        "current_status": "R11_template_only",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_4_delta_beta_q_loc",
        "coefficient": "delta_beta_q_loc",
        "definition": "O(U^2) beta-channel projection of q_loc^nu",
        "required_evidence": "parent Ward-zero derivation or q_loc U^2 coefficient/bound",
        "current_status": "not_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_5_delta_beta_boundary_domain",
        "coefficient": "delta_beta_boundary_domain",
        "definition": "quadratic beta leak from boundary/domain/projector stress",
        "required_evidence": "scalar/topological no-flux theorem or coefficient map",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "BI525_6_delta_beta_readout",
        "coefficient": "delta_beta_readout",
        "definition": "second-order mismatch between observed/source/readout metric potentials",
        "required_evidence": "same observed metric/coframe theorem through O(U^2)",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
]


R11_LINK_ROWS = [
    {
        "operator_family": "R2_fR_scalar_mode",
        "beta_channel": "delta_beta_R11_scalar",
        "required_coefficient": "c_R2_or_c_fR plus scalar mass/coupling",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "beta_channel": "delta_beta_R11_higher_curvature",
        "required_coefficient": "c_Ricci_or_c_Weyl with weak-field map",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "beta_channel": "delta_beta_R11_scalar_tensor",
        "required_coefficient": "F_phi_C_or_c_scalar and local solution/source coupling",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "boundary_topological_terms",
        "beta_channel": "delta_beta_boundary",
        "required_coefficient": "boundary coefficient or scalar/topological no-flux theorem",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "source_normalization_operator",
        "beta_channel": "delta_beta_source",
        "required_coefficient": "A_source and B_source or theorem B=A^2",
        "current_status": "missing_A_B_coefficients",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "projector_domain_stress",
        "beta_channel": "delta_beta_projector_domain",
        "required_coefficient": "projector/domain stress coefficient and beta map",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "beta_channel": "delta_beta_nonlocal_memory",
        "required_coefficient": "kernel norm/form or compact-local silence proof",
        "current_status": "missing_numeric_or_derived_zero",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D525_0_beta_law_derived",
        "status": "exact_AB_beta_law_written",
        "meaning": "the correct source-normalization beta test is beta_eff=B/A^2, not whether the first-order Newton coefficient can be fitted",
        "claim_status": "formula_only_no_beta_pass",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D525_1_coefficients_missing",
        "status": "A_and_B_not_current_MTS_computed",
        "meaning": "current MTS has not supplied the first- and second-order source coefficients needed to evaluate delta_beta_source",
        "claim_status": "blocks_PPN_and_local_GR",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D525_2_absorption_not_enough",
        "status": "constant_GM_absorption_guarded",
        "meaning": "a constant first-order mass/coupling offset is safe only if the quadratic coefficient is the square of the first-order coefficient",
        "claim_status": "prevents_false_beta_pass",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D525_3_R11_or_q_loc_fill_required",
        "status": "beta_split_inputs_unfilled",
        "meaning": "delta_beta_source must be separated from R11, q_loc, boundary/domain, and readout contributions before scoring",
        "claim_status": "no_cancellation_no_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D525_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "this is private derivation discipline, not a public/local-GR update",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "DELTA_BETA_SOURCE",
        "previous_status": "selected_as_hard_residual_after_524",
        "new_status": "exact_AB_law_derived_coefficients_missing_no_beta_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZATION_AB_COEFFICIENTS",
        "previous_status": "not_explicitly_extracted",
        "new_status": "A_source_B_source_now_required_for_beta_stability",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_EH_OPERATOR",
        "previous_status": "template_only_PPN_blocker",
        "new_status": "beta_relevant_operator_families_mapped_to_missing_coefficients",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_GAMMA_KHAT",
        "previous_status": "needs_O_U2_silence_or_bound",
        "new_status": "delta_beta_q_loc_added_as_required_input",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_PPN_vector_inputs_unfilled_and_R11_template_only",
        "new_status": "still_blocked_A_B_coefficients_R11_vector_and_q_loc_U2_bound_missing",
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
    ppn_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv"))
    source_score_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    r11_status_rows = read_csv(Path("source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv"))
    local_bound_rows = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    beta_rows = [row for row in local_bound_rows if row.get("row_id", "") == "R4_beta"]
    claim_rows = [
        *[row for row in CASE_ROWS if row["valid_for_local_GR_claim"] == "true"],
        *[row for row in INPUT_REQUIREMENT_ROWS if row["valid_for_claim"] == "true"],
        *[row for row in R11_LINK_ROWS if row["valid_for_claim"] == "true"],
    ]
    derivation_ids = {row["step_id"] for row in DERIVATION_ROWS}
    required_derivations = {"DB525_2_extract_beta", "DB525_3_beta_residual", "DB525_4_linearized_guard"}
    return [
        {
            "check_id": "V525_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V525_1_prior_PPN_and_source_scorecards_loaded",
            "result": "pass" if len(ppn_rows) == 12 and len(source_score_rows) == 12 else "fail",
            "detail": f"ppn_rows={len(ppn_rows)};source_score_rows={len(source_score_rows)}",
        },
        {
            "check_id": "V525_2_R11_status_loaded",
            "result": "pass" if len(r11_status_rows) >= 10 else "fail",
            "detail": f"r11_status_rows={len(r11_status_rows)}",
        },
        {
            "check_id": "V525_3_beta_bound_available",
            "result": "pass" if beta_rows else "fail",
            "detail": f"R4_beta_rows={len(beta_rows)}",
        },
        {
            "check_id": "V525_4_AB_law_derived",
            "result": "pass" if required_derivations.issubset(derivation_ids) else "fail",
            "detail": "beta_eff=B/A^2; delta_beta_source=B_source/A_source^2-1; linearized=(b1-2a1)epsilon",
        },
        {
            "check_id": "V525_5_inputs_visible_unfilled",
            "result": "pass" if len(INPUT_REQUIREMENT_ROWS) == 7 and len(R11_LINK_ROWS) == 7 else "fail",
            "detail": f"input_rows={len(INPUT_REQUIREMENT_ROWS)};r11_link_rows={len(R11_LINK_ROWS)}",
        },
        {
            "check_id": "V525_6_no_overclaim",
            "result": "pass" if not claim_rows else "fail",
            "detail": "delta_beta_source_derived_for_MTS=false; beta_equals_one_derived=false; PPN_promoted=false; local_GR_claim_allowed=false",
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
    return f"""# 525 - Y5 Delta-Beta Source Expansion or R11 Input Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This checkpoint gets one real derivation on the board.

For any local branch whose weak-field metric can be written

```text
g_00 = -1 + 2 A W/c^2 - 2 B W^2/c^4 + ...
```

and whose measured Newtonian potential is `U=A W`, the PPN beta coefficient is:

```text
beta_eff = B/A^2.
```

So the source-normalization beta obstruction is not vague:

```text
delta_beta_source = B_source/A_source^2 - 1.
```

Current MTS has the law, but not the required `A_source` and `B_source` coefficients. Therefore beta/local GR is not promoted.

## 2. Derivation

{markdown_table(DERIVATION_ROWS)}

## 3. Cases

{markdown_table(CASE_ROWS)}

## 4. Input Requirements

{markdown_table(INPUT_REQUIREMENT_ROWS)}

## 5. R11 Link

{markdown_table(R11_LINK_ROWS)}

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
The exact beta law beta_eff=B/A^2 is written.
The source-normalization beta residual is delta_beta_source=B_source/A_source^2-1.
The required A/B/R11/q_loc/boundary/readout inputs are now explicit.
```

Forbidden:

```text
MTS has computed A_source or B_source.
MTS has derived B_source=A_source^2.
MTS has derived beta=1.
MTS has promoted PPN or local GR.
```

## 11. Next Target

`{NEXT_TARGET}`

Next, either fill `A_source` and `B_source` from an actual second-order source equation, or bound/demote the beta channel explicitly. No more hiding beta inside first-order GM absorption.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-delta-beta-source-expansion-or-R11-input-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (DERIVATION_PATH, DERIVATION_ROWS),
        (CASE_PATH, CASE_ROWS),
        (INPUT_REQUIREMENTS_PATH, INPUT_REQUIREMENT_ROWS),
        (R11_LINK_PATH, R11_LINK_ROWS),
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
        "derivation": str(ROOT / DERIVATION_PATH),
        "cases": str(ROOT / CASE_PATH),
        "input_requirements": str(ROOT / INPUT_REQUIREMENTS_PATH),
        "r11_link": str(ROOT / R11_LINK_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "derivation_rows": len(DERIVATION_ROWS),
        "case_rows": len(CASE_ROWS),
        "input_requirement_rows": len(INPUT_REQUIREMENT_ROWS),
        "r11_link_rows": len(R11_LINK_ROWS),
        "failed_validation_rows": len(failed_validations),
        "beta_eff_AB_law_derived": True,
        "delta_beta_source_formula_written": True,
        "A_source_computed": False,
        "B_source_computed": False,
        "B_equals_A_squared_derived_for_MTS": False,
        "delta_beta_source_derived_for_MTS": False,
        "beta_equals_one_derived": False,
        "R11_beta_coefficients_supplied": False,
        "q_loc_U2_beta_bound_supplied": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
