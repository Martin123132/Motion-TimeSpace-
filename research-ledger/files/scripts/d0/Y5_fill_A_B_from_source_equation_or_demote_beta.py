from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_A_B_source_extraction_theorem_written_current_MTS_missing_premises_beta_demoted_to_residual"
CLAIM_CEILING = "A_B_source_extraction_or_beta_residual_demotion_only_no_beta_PPN_or_local_GR_pass"
NEXT_TARGET = "528-Y5-EH-family-mass-parameter-route-or-beta-residual-fill.md"

DOC_PATH = Path("527-Y5-fill-A-B-from-source-equation-or-demote-beta-to-residual.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_SOURCE_REGISTER.csv")
EXTRACTION_THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_EXTRACTION_THEOREM.csv")
ROUTE_TESTS_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_ROUTE_TESTS.csv")
BETA_DEMOTION_PATH = Path("source-intake/mts_residuals/P8_Y5_BETA_DEMOTION_RESIDUAL_ROW.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_AB_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "526-Y5-beta-coefficient-fill-runner-or-q_loc-U2-bound.md",
        "role": "beta coefficient runner showing A/B are missing and q_loc bound is provisional",
    },
    {
        "source_file": "525-Y5-delta-beta-source-expansion-or-R11-input-fill.md",
        "role": "A/B beta law and coefficient requirements",
    },
    {
        "source_file": "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md",
        "role": "PPN stability gate requiring beta source residual",
    },
    {
        "source_file": "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "role": "measured-GM/source-normalization precondition",
    },
    {
        "source_file": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "second-order EH/R11 metric-operator reduction blockers",
    },
    {
        "source_file": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only local exterior premise ladder",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration blockers",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Poisson/Gauss measured-GM bridge",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv",
        "role": "526 evaluator status with current MTS missing A/B",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv",
        "role": "526 fill input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv",
        "role": "526 q_loc U2 provisional bound rows",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "R11 status showing non-EH operator vector remains template-only",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local beta lock for residual demotion",
    },
    {
        "source_file": "scripts/Y5_fill_A_B_from_source_equation_or_demote_beta.py",
        "role": "this checkpoint generator",
    },
]


EXTRACTION_THEOREM_ROWS = [
    {
        "theorem_id": "AB527_0_EH_mass_parameter_route",
        "statement": "If the local exterior is the EH/Schwarzschild-family solution with measured mass parameter mu=G0 M_H after source calibration, then beta=1 follows automatically.",
        "math_form": "g00=-(1-2mu/(c^2 r)); isotropic/PPN expansion gives g00=-1+2U/c^2-2U^2/c^4+... with U=mu/r",
        "requires": "EH-only exterior; Birkhoff/no-hair or equivalent compact exterior theorem; measured-GM calibration; same readout metric",
        "current_MTS_status": "not_available_EH_and_measured_GM_premises_open",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "AB527_1_constant_GM_absorption_safe_case",
        "statement": "A constant source renormalization is beta-safe only when it is the actual EH mass parameter entering the nonlinear metric family.",
        "math_form": "mu=A W r and g00 family contains -2(mu/r)^2/c^4, so B=A^2",
        "requires": "constant universal A; EH nonlinear family; no extra quadratic source/readout terms",
        "current_MTS_status": "conditional_pattern_not_derived",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "AB527_2_linear_Poisson_not_enough",
        "statement": "A first-order Poisson coefficient fixes A but does not fix B.",
        "math_form": "nabla^2 Phi=4pi G A rho implies A only; beta_eff=B/A^2 remains open",
        "requires": "second-order source equation or EH family",
        "current_MTS_status": "active_guard",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "AB527_3_parent_nonlinear_completion_route",
        "statement": "If the parent source-normalization sector forces the quadratic response to be the square of the first-order response, beta source residual vanishes.",
        "math_form": "B_source=A_source^2 from parent variation => delta_beta_source=0",
        "requires": "explicit second-order parent/source equation and no R11/q_loc/boundary/readout quadratic leakage",
        "current_MTS_status": "not_computed",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "AB527_4_demotion_rule",
        "statement": "If none of the safe routes is derived, beta is a retained residual, not a local-GR closure assumption.",
        "math_form": "delta_beta_total = |B/A^2-1| + |delta_beta_R11| + |delta_beta_q_loc| + |delta_beta_boundary| + |delta_beta_readout|",
        "requires": "componentwise input rows and beta lock comparison",
        "current_MTS_status": "demotion_active",
        "valid_for_claim": "false",
    },
]


ROUTE_TEST_ROWS = [
    {
        "route_id": "ABR527_0_EH_family",
        "premise": "local exterior is exactly EH plus harmless Lambda/background subtraction through second order",
        "evidence_needed": "EH-only theorem or executable R11 vector proving no non-EH second-order operator",
        "current_evidence": "R11 template-only; EH-only premise ladder not closed",
        "result": "fail_for_current_claim",
        "next_action": "try EH-family mass-parameter route or fill R11 beta coefficients",
    },
    {
        "route_id": "ABR527_1_measured_GM_calibrated",
        "premise": "first-order U is the measured orbital GM potential and equals the source mass parameter",
        "evidence_needed": "523 scorecard zero/below-bound; Gauss/orbital calibration; mu_extra silence",
        "current_evidence": "523 scorecard unfilled and measured_GM_parent_derived=false",
        "result": "fail_for_current_claim",
        "next_action": "fill/derive source-normalization scorecard",
    },
    {
        "route_id": "ABR527_2_constant_universal_A",
        "premise": "A_source is constant, universal, frame/source/range/domain blind",
        "evidence_needed": "constant G_eff/kappa and no derivative/source hair",
        "current_evidence": "Gdot/source/range/domain residuals retained",
        "result": "fail_for_current_claim",
        "next_action": "derive global coupling/source-charge theorem or fill residual rows",
    },
    {
        "route_id": "ABR527_3_B_equals_A_squared",
        "premise": "second-order coefficient follows B_source=A_source^2",
        "evidence_needed": "source equation expanded to O(U^2), or EH mass-family theorem",
        "current_evidence": "no A/B extraction source equation supplied",
        "result": "fail_for_current_claim",
        "next_action": "extract A/B from source equation or demote beta",
    },
    {
        "route_id": "ABR527_4_q_loc_U2_zero_or_bound",
        "premise": "q_loc has no O(U^2) beta force or has a physical beta-normalized bound",
        "evidence_needed": "Ward-zero through O(U2), or q_loc profile normalized as delta_beta_q_loc",
        "current_evidence": "526 has provisional compact-shell budget but physical U2 normalization not proved",
        "result": "fail_for_claim_but_interesting_provisional_beta_budget",
        "next_action": "derive q_loc U2 conversion or keep explicit residual",
    },
    {
        "route_id": "ABR527_5_total_beta_envelope",
        "premise": "all beta pieces are zero or below beta lock without cancellation",
        "evidence_needed": "numeric/theorem-zero component rows for source, R11, q_loc, boundary, readout",
        "current_evidence": "component inputs missing",
        "result": "not_run",
        "next_action": "fill component rows",
    },
]


BETA_DEMOTION_ROWS = [
    {
        "residual_id": "BD527_0_delta_beta_source",
        "symbol": "delta_beta_source",
        "formula": "B_source/A_source^2 - 1",
        "required_input": "A_source;B_source;source equation path",
        "bound_or_target": "beta_minus_1<=7.8e-5 or derived zero",
        "current_status": "retained_missing_A_B",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BD527_1_delta_beta_R11",
        "symbol": "delta_beta_R11",
        "formula": "beta projection of non-EH operator coefficient vector",
        "required_input": "R11 executable vector or EH-only theorem",
        "bound_or_target": "operator contribution below beta/gamma/preferred-frame locks",
        "current_status": "retained_R11_template_only",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BD527_2_delta_beta_q_loc",
        "symbol": "delta_beta_q_loc",
        "formula": "beta-equivalent O(U2) projection of q_loc force/source residual",
        "required_input": "q_loc Ward-zero or U2 conversion/profile",
        "bound_or_target": "below beta lock and separately checked against alpha_i/xi locks",
        "current_status": "retained_provisional_budget_only",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BD527_3_delta_beta_boundary_domain",
        "symbol": "delta_beta_boundary_domain",
        "formula": "quadratic beta leak from boundary/domain/projector stress",
        "required_input": "scalar/topological no-flux theorem or coefficient map",
        "bound_or_target": "below beta and alpha3/xi locks",
        "current_status": "retained_unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BD527_4_delta_beta_readout",
        "symbol": "delta_beta_readout",
        "formula": "second-order mismatch between source metric and orbital/clock readout metric",
        "required_input": "same observed coframe/readout theorem through O(U2)",
        "bound_or_target": "WEP/clock/gamma/beta locks",
        "current_status": "retained_unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "BD527_5_total_beta_envelope",
        "symbol": "Delta_beta_total_abs",
        "formula": "sum_i |BD527_i| with no cancellation credit",
        "required_input": "all beta component rows filled or theorem-zero",
        "bound_or_target": "Delta_beta_total_abs <= 7.8e-5",
        "current_status": "not_run_components_missing",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D527_0_safe_route_identified",
        "status": "EH_mass_parameter_route_is_clean",
        "meaning": "the cleanest way to get beta=1 is to derive the EH local exterior family with measured mass parameter mu, which gives B=A^2 automatically",
        "claim_status": "conditional_not_current_MTS_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D527_1_current_source_equation_missing",
        "status": "A_B_not_extractable_from_current_rows",
        "meaning": "the current corpus has not supplied a second-order source equation that yields A_source and B_source",
        "claim_status": "beta_demoted_to_residual",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D527_2_linear_Newton_not_enough",
        "status": "first_order_fit_cannot_pay_beta_debt",
        "meaning": "a Newton/Gauss source coefficient can determine A, but beta still needs B=A^2 or a residual bound",
        "claim_status": "overclaim_blocked",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D527_3_demoted_beta_row_written",
        "status": "beta_component_residual_rows_active",
        "meaning": "source, R11, q_loc, boundary/domain, and readout beta pieces are retained with no-cancellation policy",
        "claim_status": "no_PPN_or_local_GR_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D527_4_private_no_push",
        "status": "private_no_github_no_promotion",
        "meaning": "this checkpoint stays private and does not push or publish anything",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "A_B_SOURCE_EXTRACTION",
        "previous_status": "runner_written_current_inputs_missing",
        "new_status": "safe_routes_written_current_A_B_source_equation_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BETA_DEMOTION",
        "previous_status": "beta_channel_unfilled",
        "new_status": "explicit_component_residual_rows_active",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "EH_MASS_PARAMETER_ROUTE",
        "previous_status": "implicit_possible_route",
        "new_status": "identified_as_cleanest_path_to_B_equals_A_squared",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Q_LOC_U2_BOUND",
        "previous_status": "provisional_compact_shell_beta_budget_same_normalization_not_proved",
        "new_status": "retained_beta_component_until_U2_conversion_or_Ward_zero_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_current_beta_inputs_missing_q_loc_normalization_not_proved_and_R11_template_only",
        "new_status": "still_blocked_beta_demoted_to_residual_and_EH_mass_family_not_derived",
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
    evaluator_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv"))
    qloc_bound_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_QLOC_U2_BOUND.csv"))
    beta_bound_rows = [
        row
        for row in read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
        if row.get("row_id") == "R4_beta"
    ]
    theorem_claim_rows = [row for row in EXTRACTION_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    demotion_claim_rows = [row for row in BETA_DEMOTION_ROWS if row["valid_for_claim"] == "true"]
    route_pass_rows = [row for row in ROUTE_TEST_ROWS if row["result"] == "pass_for_current_claim"]
    return [
        {
            "check_id": "V527_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V527_1_526_runner_loaded",
            "result": "pass" if len(evaluator_rows) >= 2 and len(qloc_bound_rows) >= 4 else "fail",
            "detail": f"evaluator_rows={len(evaluator_rows)};qloc_bound_rows={len(qloc_bound_rows)}",
        },
        {
            "check_id": "V527_2_beta_bound_available",
            "result": "pass" if beta_bound_rows else "fail",
            "detail": f"R4_beta_rows={len(beta_bound_rows)}",
        },
        {
            "check_id": "V527_3_safe_routes_written",
            "result": "pass" if len(EXTRACTION_THEOREM_ROWS) == 5 and len(ROUTE_TEST_ROWS) == 6 else "fail",
            "detail": f"theorem_rows={len(EXTRACTION_THEOREM_ROWS)};route_tests={len(ROUTE_TEST_ROWS)}",
        },
        {
            "check_id": "V527_4_beta_demotion_rows_written",
            "result": "pass" if len(BETA_DEMOTION_ROWS) == 6 else "fail",
            "detail": f"demotion_rows={len(BETA_DEMOTION_ROWS)}",
        },
        {
            "check_id": "V527_5_current_routes_do_not_pass",
            "result": "pass" if not route_pass_rows else "fail",
            "detail": f"pass_for_current_claim_rows={len(route_pass_rows)}",
        },
        {
            "check_id": "V527_6_no_overclaim",
            "result": "pass" if not theorem_claim_rows and not demotion_claim_rows else "fail",
            "detail": "A_B_extracted=false; B_equals_A_squared_derived=false; beta_equals_one_derived=false; local_GR_claim_allowed=false",
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
    return f"""# 527 - Y5 Fill A/B from Source Equation or Demote Beta to Residual

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The clean beta route is now identified:

```text
derive an EH local exterior family with measured mass parameter mu,
then B = A^2 and beta = 1 follows.
```

That route is not yet available for current MTS, because EH-only exterior, measured-GM calibration, R11 silence, and q_loc U2 silence are still open.

So beta is demoted to explicit residual rows. This is not grim; it is disciplined. The theory now knows exactly what it must derive or fill before local GR can be claimed.

## 2. A/B Extraction Theorem

{markdown_table(EXTRACTION_THEOREM_ROWS)}

## 3. Route Tests

{markdown_table(ROUTE_TEST_ROWS)}

## 4. Beta Demotion Residual Row

{markdown_table(BETA_DEMOTION_ROWS)}

## 5. Decision

{markdown_table(DECISION_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
The EH mass-parameter route to B=A^2 is now explicit.
The current MTS branch does not yet satisfy that route.
Beta is demoted to source/R11/q_loc/boundary/readout residual components.
```

Forbidden:

```text
MTS has extracted A_source and B_source from a source equation.
MTS has derived B_source=A_source^2.
MTS has derived beta=1 or local GR.
```

## 10. Next Target

`{NEXT_TARGET}`

Next, attack the cleanest route: can the local branch be shown to be an EH mass-parameter family after source calibration? If yes, beta becomes derivable. If no, fill the beta residual row and stop treating beta as a hidden closure.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-fill-A-B-from-source-equation-or-demote-beta"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (EXTRACTION_THEOREM_PATH, EXTRACTION_THEOREM_ROWS),
        (ROUTE_TESTS_PATH, ROUTE_TEST_ROWS),
        (BETA_DEMOTION_PATH, BETA_DEMOTION_ROWS),
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
        "extraction_theorem": str(ROOT / EXTRACTION_THEOREM_PATH),
        "route_tests": str(ROOT / ROUTE_TESTS_PATH),
        "beta_demotion": str(ROOT / BETA_DEMOTION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "extraction_theorem_rows": len(EXTRACTION_THEOREM_ROWS),
        "route_test_rows": len(ROUTE_TEST_ROWS),
        "beta_demotion_rows": len(BETA_DEMOTION_ROWS),
        "failed_validation_rows": len(failed_validations),
        "EH_mass_parameter_route_written": True,
        "EH_mass_parameter_route_derived_for_MTS": False,
        "A_B_source_equation_extracted": False,
        "B_equals_A_squared_derived_for_MTS": False,
        "beta_demoted_to_residual": True,
        "delta_beta_residual_components_written": True,
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
