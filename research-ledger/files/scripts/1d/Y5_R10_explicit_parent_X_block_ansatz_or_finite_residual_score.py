from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "580-Y5-R10-explicit-parent-X-block-ansatz-or-finite-residual-score.md"

PRIOR_579_VALIDATION = RESIDUALS / "P8_Y5_BRR545_579_VALIDATION.csv"
PRIOR_579_SUMMARY = RESIDUALS / "P8_Y5_R10_579_NONCLAIM_SUMMARY.csv"
PARENT_CONTRACT_579 = RESIDUALS / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv"
SOURCE_CHARGE_579 = RESIDUALS / "P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv"
THEOREM_GATE_579 = RESIDUALS / "P8_Y5_R10_579_THEOREM_ZERO_RETURN_GATE.csv"
FINITE_QUEUE_579 = RESIDUALS / "P8_Y5_R10_579_FINITE_COEFFICIENT_FILL_QUEUE.csv"
MASS_TARGETS_578 = RESIDUALS / "P8_Y5_R10_578_MASS_GAP_TARGETS.csv"
REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
LIVE_CLAIM_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_580_SOURCE_REGISTER.csv"
PARENT_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv"
VARIATIONAL_TESTS_PATH = RESIDUALS / "P8_Y5_R10_580_VARIATIONAL_TESTS.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_580_NOPOLE_OR_SOURCE_BRANCH_DECISION.csv"
RESIDUAL_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_580_RESIDUAL_SCORE_TEMPLATE.csv"
PRESSURE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_580_DERIVATION_PRESSURE_LEDGER.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_580_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_580_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_580_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_580_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_explicit_parent_X_block_candidates_written_no_pole_route_best_but_not_parent_derived"
CLAIM_CEILING = "explicit_ansatz_contract_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md"

SOURCE_FILES = [
    {
        "source_file": "579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md",
        "role": "immediate handoff and obstruction ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_579_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_NONCLAIM_SUMMARY.csv",
        "role": "prior nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
        "role": "parent X-block contract from the previous checkpoint",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv",
        "role": "source/test charge functionals from previous checkpoint",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_THEOREM_ZERO_RETURN_GATE.csv",
        "role": "theorem-zero return gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_FINITE_COEFFICIENT_FILL_QUEUE.csv",
        "role": "finite coefficient queue",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_578_MASS_GAP_TARGETS.csv",
        "role": "private pressure values for finite residual branch",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
        "role": "review-candidate bound curve, private only",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live claim curve, expected blocked",
    },
    {
        "source_file": "scripts/Y5_R10_explicit_parent_X_block_ansatz_or_finite_residual_score.py",
        "role": "this checkpoint generator",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, object]]:
    return [
        {
            "source_file": item["source_file"],
            "exists": str((ROOT / str(item["source_file"])).exists()),
            "role": item["role"],
        }
        for item in SOURCE_FILES
    ]


def make_parent_candidates() -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "PB580_0_absent_quotient_variable",
            "parent_block": "X is not a primitive field; it is a coordinate/readout artefact removed by the quotient",
            "action_sketch": "S_parent=S_obs[pi(Phi)]+S_matter[psi,hat_g(pi(Phi))]+S_top; no independent X variation exists",
            "physical_pole": "none",
            "R10_consequence": "K_X=0 because there is no X Green function",
            "GR_reduction_value": "strongest_if_parent_derived",
            "blocker": "must prove X is not a physical direction of the parent configuration space, not merely set it to zero after readout",
            "recommended_rank": 1,
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "PB580_1_quotient_vertical_constraint",
            "parent_block": "X is a vertical gauge/constraint direction with no physical pole",
            "action_sketch": "S_parent=S_obs[pi(Phi)]+int Lambda C_X(Phi)+S_matter[psi,hat_g(pi(Phi))]; delta_epsilon X=epsilon and delta_epsilon pi(Phi)=0",
            "physical_pole": "none_if_constraint_algebra_closes",
            "R10_consequence": "K_X=0 or qbar_XT=Qbar_XH=0 by Noether/quotient identity",
            "GR_reduction_value": "best_active_theorem_route",
            "blocker": "needs a real first-class constraint/no-pole proof and boundary charge audit",
            "recommended_rank": 2,
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "PB580_2_positive_sourcefree_massive_X",
            "parent_block": "X is a massive physical field but source-free in local matter",
            "action_sketch": "S_X=1/2 int sqrt(h)[Z_X |grad X|^2+M_X^2 X^2] with Z_X>0, M_X^2>0, J_X=0, boundary flux=0",
            "physical_pole": "yes_but_unexcited",
            "R10_consequence": "X=0 by positive no-hair identity",
            "GR_reduction_value": "good_if_source_zero_parent_owned",
            "blocker": "source-zero is harder than no-pole because matter pullback and hidden sources must vanish channelwise",
            "recommended_rank": 3,
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "PB580_3_massive_sourced_residual",
            "parent_block": "X is a physical massive field with nonzero source/test charge",
            "action_sketch": "S_X=1/2 int sqrt(h)[Z_X |grad X|^2+M_X^2 X^2]-int sqrt(h)XJ_X; J_X nonzero",
            "physical_pole": "yes",
            "R10_consequence": "alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT must be scored",
            "GR_reduction_value": "empirical_survival_not_GR_derivation",
            "blocker": "needs numeric parent Hessian, source charge, test charge, projection, and claim-grade bound curve",
            "recommended_rank": 4,
            "valid_for_claim": "false",
        },
        {
            "candidate_id": "PB580_4_universal_conformal_matter",
            "parent_block": "universal matter sees hat_g_mu_nu=exp(2 a X)g_mu_nu",
            "action_sketch": "S_matter[psi,exp(2 a X)g] plus massive X block",
            "physical_pole": "yes_if_Z_X_and_M_X_positive",
            "R10_consequence": "finite universal fifth force unless a=0 is parent-derived",
            "GR_reduction_value": "countermodel_not_solution",
            "blocker": "shows universal coupling is not enough; it blocks a cheap theorem-zero claim",
            "recommended_rank": 5,
            "valid_for_claim": "false",
        },
    ]


def make_variational_tests() -> list[dict[str, object]]:
    tests: list[dict[str, object]] = []
    candidates = {
        "PB580_0_absent_quotient_variable": {
            "branch_extremum": "pass_if_absence_proved",
            "physical_pole_absent": "pass_if_parent_space_quotient",
            "matter_pullback_zero": "pass_if_hat_g_depends_only_on_pi",
            "hidden_source_zero": "needs_boundary_audit",
            "PiM_status": "irrelevant_or_zero_if_no_X_charge",
            "R10_status": "theorem_route_candidate",
        },
        "PB580_1_quotient_vertical_constraint": {
            "branch_extremum": "constraint_surface",
            "physical_pole_absent": "pass_if_first_class_no_inverse_kernel",
            "matter_pullback_zero": "pass_if_matter_is_quotient_functor",
            "hidden_source_zero": "needs_no_boundary_charge",
            "PiM_status": "zero_if_charge_is_vertical_exact",
            "R10_status": "best_next_theorem_attempt",
        },
        "PB580_2_positive_sourcefree_massive_X": {
            "branch_extremum": "must_prove_E_X_zero",
            "physical_pole_absent": "fail_has_pole",
            "matter_pullback_zero": "must_prove",
            "hidden_source_zero": "must_prove",
            "PiM_status": "zero_if_source_zero",
            "R10_status": "conditional_nohair_only",
        },
        "PB580_3_massive_sourced_residual": {
            "branch_extremum": "can_pass",
            "physical_pole_absent": "fail_has_pole",
            "matter_pullback_zero": "fail_or_unfilled",
            "hidden_source_zero": "unfilled",
            "PiM_status": "must_compute",
            "R10_status": "finite_residual_score",
        },
        "PB580_4_universal_conformal_matter": {
            "branch_extremum": "can_pass",
            "physical_pole_absent": "fail_has_pole",
            "matter_pullback_zero": "fail_unless_a_zero",
            "hidden_source_zero": "not_enough",
            "PiM_status": "source_projects_unless_orthogonal",
            "R10_status": "counterexample_guardrail",
        },
    }
    for candidate_id, result_map in candidates.items():
        for test_name, result in result_map.items():
            tests.append(
                {
                    "test_id": f"VT580_{len(tests)}",
                    "candidate_id": candidate_id,
                    "test_name": test_name,
                    "result": result,
                    "claim_effect": "no_claim_promotion",
                    "valid_for_claim": "false",
                }
            )
    return tests


def make_branch_decision() -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD580_0_best_derivation_target",
            "selected_route": "quotient_vertical_no_pole",
            "reason": "it kills the finite Green function before coefficient tuning and best matches the desired GR reduction rather than empirical survival",
            "mathematical_contract": "there exists a projection pi from parent configurations to observed configurations such that delta_X pi=0, S_matter and S_obs factor through pi, and X has no invertible physical kinetic operator",
            "pass_condition": "Noether/constraint identity proves K_X=0 and no boundary X charge",
            "current_status": "ansatz_target_not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BD580_1_secondary_zero_target",
            "selected_route": "positive_sourcefree_nohair",
            "reason": "if X is physical, source-free positive operator still gives X=0",
            "mathematical_contract": "Z_X>0, M_X^2>0, J_X=0, boundary flux=0",
            "pass_condition": "channelwise matter/source/boundary/projector/memory/domain zeros",
            "current_status": "harder_than_no_pole",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BD580_2_empirical_fallback",
            "selected_route": "finite_residual_score",
            "reason": "if X is physical and sourced, no GR theorem is available; the theory must survive as a bounded residual",
            "mathematical_contract": "abs(K_X Qbar_XH(lambda_X) qbar_XT)<=alpha_bound(lambda_X)",
            "pass_condition": "numeric/source-backed coefficients and claim-grade bound curve",
            "current_status": "fallback_only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BD580_3_rejected_shortcut",
            "selected_route": "universal_matter_auto_zero",
            "reason": "579 countermodel proves universality/covariance does not force source neutrality",
            "mathematical_contract": "none",
            "pass_condition": "rejected unless a=0 is parent-derived by the quotient/no-pole theorem",
            "current_status": "forbidden_shortcut",
            "valid_for_claim": "false",
        },
    ]


def make_residual_template() -> list[dict[str, object]]:
    return [
        {
            "template_id": "RST580_0_alpha_row",
            "model_id": "MTS_parent_X_finite_residual_branch",
            "required_lambda": "lambda_X=sqrt(Z_X/M_X^2)",
            "required_alpha": "alpha_X(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "required_bound": "alpha_bound(lambda_X)",
            "required_status": "all coefficients numeric/source-backed; no MISSING markers; curve claim-grade",
            "current_fill": "symbolic_only",
            "claim_allowed": "false",
        },
        {
            "template_id": "RST580_1_no_pole_row",
            "model_id": "MTS_quotient_vertical_no_pole_branch",
            "required_lambda": "not_applicable_no_physical_pole",
            "required_alpha": "0 by K_X=0, not by fitted smallness",
            "required_bound": "not_needed_after_certificate",
            "required_status": "first-class constraint/no-pole proof plus boundary charge audit",
            "current_fill": "ansatz_only",
            "claim_allowed": "false",
        },
        {
            "template_id": "RST580_2_sourcefree_nohair_row",
            "model_id": "MTS_positive_sourcefree_X_branch",
            "required_lambda": "lambda_X=sqrt(Z_X/M_X^2) may exist but field is unexcited",
            "required_alpha": "0 by J_X=0 and boundary flux=0",
            "required_bound": "not_needed_after_certificate",
            "required_status": "positive Hessian plus channelwise source-zero certificate",
            "current_fill": "certificate_unfilled",
            "claim_allowed": "false",
        },
    ]


def make_pressure_ledger(mass_targets: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [
        {
            "pressure_id": "DPL580_0_logic",
            "object": "derivation_priority",
            "pressure": "no-pole theorem beats finite residual because it removes the R10 alpha row rather than shrinking it",
            "source": "579 countermodel plus 578 mass-gap/product wall",
            "next_action": NEXT_TARGET,
        },
        {
            "pressure_id": "DPL580_1_guardrail",
            "object": "universal coupling",
            "pressure": "universal nonzero coupling can still be R10-visible; WEP-safe is not fifth-force-safe",
            "source": "579 conformal countermodel",
            "next_action": "derive a=0 from quotient verticality or retain finite alpha",
        },
    ]
    interesting_targets = []
    for row in mass_targets:
        target_id = row.get("target_id", "")
        if target_id in {"MGT578_3", "MGT578_6", "MGT578_9"}:
            interesting_targets.append(row)
    for row in interesting_targets:
        rows.append(
            {
                "pressure_id": f"DPL580_{len(rows)}_{row.get('target_id')}",
                "object": f"lambda={row.get('lambda_X_um')}um",
                "pressure": f"M_X^2/Z_X={row.get('M_X2_over_Z_X_m_minus2')} m^-2; review alpha_bound={row.get('alpha_bound_review_candidate')}",
                "source": "P8_Y5_R10_578_MASS_GAP_TARGETS.csv",
                "next_action": "finite branch needs parent coefficients; no-pole branch avoids this row",
            }
        )
    return rows


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D580_0_no_pole_route_prioritized",
            "decision": "prioritize quotient-vertical no-pole theorem attempt",
            "meaning": "this is the cleanest route to derived local GR because it removes the finite X exchange before R10 scoring",
            "status": "private_derivation_target",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D580_1_no_claim_upgrade",
            "decision": "do not promote the no-pole route yet",
            "meaning": "the parent quotient/constraint proof and boundary charge audit are still missing",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D580_2_finite_branch_kept",
            "decision": "keep finite residual score as fallback",
            "meaning": "if X is physical and sourced, alpha(lambda) must be filled and tested rather than hidden",
            "status": "fallback_retained",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D580_3_conformal_shortcut_rejected",
            "decision": "reject universal matter equals zero shortcut",
            "meaning": "universal nonzero coupling can be WEP-safe while still failing R10",
            "status": "guardrail",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU580_0_allowed",
            "allowed_after_580": "try to prove X is quotient-vertical/no-pole before doing more coefficient scans",
            "forbidden_after_580": "declare X absent without a parent configuration-space projection and boundary charge audit",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU580_1_allowed",
            "allowed_after_580": "use finite residual scoring only as fallback if no-pole/sourcefree theorem fails",
            "forbidden_after_580": "call finite residual survival the same thing as GR reduction",
            "next_action": "fill residual alpha rows only after theorem attempt fails",
        },
        {
            "route_id": "RU580_2_allowed",
            "allowed_after_580": "use the conformal countermodel as a red-team test for every proposed zero proof",
            "forbidden_after_580": "appeal to covariance, universality, or WEP alone as source-zero proof",
            "next_action": "ensure proposed theorem excludes hat_g=exp(2aX)g unless a=0 follows",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    parent_candidates: list[dict[str, object]],
    variational_tests: list[dict[str, object]],
    branch_decision: list[dict[str, object]],
    residual_template: list[dict[str, object]],
    pressure_ledger: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    prior_claim_allowed = any(row.get("claim_allowed") == "true" for row in prior_summary)
    best_route = [row for row in branch_decision if row["selected_route"] == "quotient_vertical_no_pole"]
    no_claim_candidates = all(row["valid_for_claim"] == "false" for row in parent_candidates)
    has_residual_alpha = any(row["template_id"] == "RST580_0_alpha_row" for row in residual_template)
    has_no_pole_template = any(row["template_id"] == "RST580_1_no_pole_row" for row in residual_template)
    claim_allowed_rows = [row for row in residual_template if row.get("claim_allowed") == "true"]
    has_countermodel_guardrail = any("universal" in str(row.get("object", "")) for row in pressure_ledger)
    promoted_decisions = [row for row in decisions if "pass" in str(row["status"]).lower()]

    return [
        {
            "check_id": "V580_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V580_1_prior_579_clean",
            "result": "pass" if not prior_failures and not prior_claim_allowed else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};prior_claim_allowed={prior_claim_allowed}",
        },
        {
            "check_id": "V580_2_parent_candidates_written",
            "result": "pass" if len(parent_candidates) >= 5 and no_claim_candidates else "fail",
            "detail": f"candidate_rows={len(parent_candidates)};claim_rows=0",
        },
        {
            "check_id": "V580_3_variational_tests_cover_candidates",
            "result": "pass" if len(variational_tests) >= len(parent_candidates) * 5 else "fail",
            "detail": f"test_rows={len(variational_tests)}",
        },
        {
            "check_id": "V580_4_best_route_selected_without_claim",
            "result": "pass" if best_route and best_route[0]["valid_for_claim"] == "false" else "fail",
            "detail": "selected=quotient_vertical_no_pole;valid_for_claim=false",
        },
        {
            "check_id": "V580_5_residual_fallback_template_written",
            "result": "pass" if has_residual_alpha and has_no_pole_template and not claim_allowed_rows else "fail",
            "detail": f"templates={len(residual_template)};claim_allowed_rows={len(claim_allowed_rows)}",
        },
        {
            "check_id": "V580_6_countermodel_guardrail_retained",
            "result": "pass" if has_countermodel_guardrail else "fail",
            "detail": "universal_nonzero_guardrail_present",
        },
        {
            "check_id": "V580_7_no_R10_or_local_GR_claim",
            "result": "pass" if not promoted_decisions else "fail",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    parent_candidates: list[dict[str, object]],
    variational_tests: list[dict[str, object]],
    branch_decision: list[dict[str, object]],
    residual_template: list[dict[str, object]],
    pressure_ledger: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 580 Y5 R10 explicit parent X-block ansatz or finite residual score

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The best next derivation route is now identified: make `X` quotient-vertical/no-pole, not merely small.
- If `X` is absent from the physical parent quotient, or is a first-class vertical constraint with no Green function, then `K_X=0` and the R10 finite-force row disappears for a real reason.
- If `X` is instead a physical massive sourced field, the theory must score `alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT`; that can still survive empirically, but it is not the same as deriving local GR.
- No claim is promoted here. This checkpoint chooses the next theorem attempt and keeps the finite residual fallback honest.

## No-Pole Theorem Target
```text
Parent configuration: Phi
Observed quotient: pi(Phi)
Vertical direction: X

delta_X pi(Phi)=0
S_obs=S_obs[pi(Phi)]
S_matter=S_matter[psi, hat_g(pi(Phi))]
X has no invertible physical kinetic operator and no boundary charge
=> no physical X Green function
=> K_X=0, qbar_XT=0, Qbar_XH=0
=> alpha_X(lambda) is not an active local force row.
```

The phrase to watch is **before variation**. If `X` only disappears after readout or gauge choice, the countermodel from 579 sneaks back in wearing a fake moustache.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Parent Block Candidates
{markdown_table(parent_candidates, ["candidate_id", "parent_block", "action_sketch", "physical_pole", "R10_consequence", "GR_reduction_value", "blocker", "recommended_rank", "valid_for_claim"])}

## Variational Tests
{markdown_table(variational_tests, ["test_id", "candidate_id", "test_name", "result", "claim_effect", "valid_for_claim"])}

## Branch Decision
{markdown_table(branch_decision, ["branch_id", "selected_route", "reason", "mathematical_contract", "pass_condition", "current_status", "valid_for_claim"])}

## Residual Score Template
{markdown_table(residual_template, ["template_id", "model_id", "required_lambda", "required_alpha", "required_bound", "required_status", "current_fill", "claim_allowed"])}

## Derivation Pressure Ledger
{markdown_table(pressure_ledger, ["pressure_id", "object", "pressure", "source", "next_action"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_580", "forbidden_after_580", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is the cleanest shape the local-GR path has had so far. The route is not "make the fifth force tiny"; it is "prove the fifth-force field is not a physical pole of the parent theory." That is exactly the kind of move that would make the framework feel like GR reducing to Newton, not like another patched residual model. But we have to earn it: the next checkpoint must try to prove the quotient-vertical/no-pole theorem and explicitly block boundary charge leakage.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_validation = read_csv(PRIOR_579_VALIDATION)
    prior_summary = read_csv(PRIOR_579_SUMMARY)
    parent_contract_579 = read_csv(PARENT_CONTRACT_579)
    source_charge_579 = read_csv(SOURCE_CHARGE_579)
    theorem_gate_579 = read_csv(THEOREM_GATE_579)
    finite_queue_579 = read_csv(FINITE_QUEUE_579)
    mass_targets_578 = read_csv(MASS_TARGETS_578)

    parent_candidates = make_parent_candidates()
    variational_tests = make_variational_tests()
    branch_decision = make_branch_decision()
    residual_template = make_residual_template()
    pressure_ledger = make_pressure_ledger(mass_targets_578)
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        parent_candidates,
        variational_tests,
        branch_decision,
        residual_template,
        pressure_ledger,
        decisions,
    )

    summary_rows = [
        {
            "summary_id": "S580_0_result",
            "status": STATUS,
            "best_next_route": "quotient_vertical_no_pole",
            "no_pole_theorem_derived": "false",
            "finite_branch_retained": "true",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "parent_contract_rows_reused": len(parent_contract_579),
            "source_charge_rows_reused": len(source_charge_579),
            "theorem_gate_rows_reused": len(theorem_gate_579),
            "finite_queue_rows_reused": len(finite_queue_579),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        PARENT_CANDIDATES_PATH,
        parent_candidates,
        [
            "candidate_id",
            "parent_block",
            "action_sketch",
            "physical_pole",
            "R10_consequence",
            "GR_reduction_value",
            "blocker",
            "recommended_rank",
            "valid_for_claim",
        ],
    )
    write_csv(
        VARIATIONAL_TESTS_PATH,
        variational_tests,
        ["test_id", "candidate_id", "test_name", "result", "claim_effect", "valid_for_claim"],
    )
    write_csv(
        BRANCH_DECISION_PATH,
        branch_decision,
        ["branch_id", "selected_route", "reason", "mathematical_contract", "pass_condition", "current_status", "valid_for_claim"],
    )
    write_csv(
        RESIDUAL_TEMPLATE_PATH,
        residual_template,
        ["template_id", "model_id", "required_lambda", "required_alpha", "required_bound", "required_status", "current_fill", "claim_allowed"],
    )
    write_csv(PRESSURE_LEDGER_PATH, pressure_ledger, ["pressure_id", "object", "pressure", "source", "next_action"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update, ["route_id", "allowed_after_580", "forbidden_after_580", "next_action"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "best_next_route",
            "no_pole_theorem_derived",
            "finite_branch_retained",
            "claim_allowed",
            "R10_pass_for_claim",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "parent_contract_rows_reused",
            "source_charge_rows_reused",
            "theorem_gate_rows_reused",
            "finite_queue_rows_reused",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        parent_candidates,
        variational_tests,
        branch_decision,
        residual_template,
        pressure_ledger,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "best_next_route": "quotient_vertical_no_pole",
                "no_pole_theorem_derived": False,
                "finite_branch_retained": True,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
