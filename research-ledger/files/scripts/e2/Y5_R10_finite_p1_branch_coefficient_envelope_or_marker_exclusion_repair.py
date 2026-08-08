from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair"
DOC_PATH = ROOT / "610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_610_SOURCE_REGISTER.csv"
METHOD_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_610_METHOD_SELECTION.csv"
COEFFICIENT_ENVELOPE_PATH = RESIDUALS / "P8_Y5_R10_610_FINITE_P1_COEFFICIENT_ENVELOPE.csv"
PRESSURE_PATH = RESIDUALS / "P8_Y5_R10_610_ALPHA_PRESSURE_ENVELOPE.csv"
COMPONENT_BUDGET_PATH = RESIDUALS / "P8_Y5_R10_610_COMPONENT_BUDGET_SCENARIOS.csv"
MARKER_REPAIR_PATH = RESIDUALS / "P8_Y5_R10_610_MARKER_EXCLUSION_REPAIR_OPTION.csv"
MTS_TEMPLATE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_FINITE_P1_ENVELOPE_TEMPLATE.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_610_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_610_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_610_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_610_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_610_VALIDATION.csv"

PRIOR_609_VALIDATION = RESIDUALS / "P8_Y5_BRR545_609_VALIDATION.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
LIVE_MTS = RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv"
LIVE_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

STATUS = "Y5_R10_best_method_selected_finite_p1_coefficient_envelope_nonclaim_marker_closure_deferred"
CLAIM_CEILING = "finite_p1_envelope_and_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "611-Y5-R10-real-bound-curve-QA-or-CX-component-prior-runner.md"
EPSILON_SHELL = 7.432631961576971e-06

SOURCE_FILES = [
    ("609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md", "immediate 609 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_609_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_609_FINITE_P1_BRANCH_LEDGER.csv", "finite p1 branch trigger"),
    ("source-intake/mts_residuals/P8_Y5_R10_609_P_BRANCH_DECISION.csv", "p branch decision"),
    ("607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md", "alpha=epsilon^p C_X factorization"),
    ("source-intake/mts_residuals/P8_Y5_R10_607_COEFFICIENT_PRESSURE_TABLE.csv", "prior epsilon pressure rows"),
    ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "lambda/product coefficient derivation"),
    ("source-intake/mts_residuals/P8_Y5_R10_578_PRODUCT_COEFFICIENT_DERIVATION.csv", "C_X component definitions"),
    ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "source charge decomposition and countermodel"),
    ("source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv", "source/test/K_X exact expressions"),
    ("608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md", "p2 theorem target kept but not promoted"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor-only non-claim R10 bound rows"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim placeholder kept unchanged"),
    ("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv", "live MTS placeholder kept unchanged"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_finite_p1_branch_coefficient_envelope_or_marker_exclusion_repair.py", "this checkpoint generator"),
]

MTS_TEMPLATE_FIELDS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_method_selection_rows() -> list[dict[str, str]]:
    return [
        {
            "method_id": "MS610_0_finite_p1_envelope",
            "method": "finite p=1 coefficient envelope",
            "selection": "selected_best_method",
            "why_best": "it is testable, does not add an unearned parent axiom, and keeps p2 as a theorem target without pretending it is derived",
            "physics_cost": "finite residual branch is not local-GR theorem-zero",
            "output": "alpha_X=lambda branch = epsilon_shell C_X(lambda_X)",
            "valid_for_claim": "false",
        },
        {
            "method_id": "MS610_1_parent_OED_closure",
            "method": "explicit parent O(E_D) norm-square clause",
            "selection": "deferred_repair_option",
            "why_best": "would close p=2 cleanly only if labelled as new closure/action clause",
            "physics_cost": "closure is less derivation-pure and must be publicly labelled",
            "output": "p=2 theorem target retained but not used as evidence",
            "valid_for_claim": "false",
        },
        {
            "method_id": "MS610_2_p3_determinant",
            "method": "det(Q_coh) p=3 route",
            "selection": "deferred",
            "why_best": "beautiful shape but too many ownership blockers remain",
            "physics_cost": "raw det(Q) shear leak forbids shortcut",
            "output": "theorem target only",
            "valid_for_claim": "false",
        },
    ]


def make_coefficient_envelope_rows() -> list[dict[str, str]]:
    return [
        {
            "coefficient_id": "CE610_0_alpha_law",
            "object": "finite p1 alpha law",
            "formula": "alpha_X(lambda_X)=epsilon_shell*C_X(lambda_X)",
            "definition": "C_X=sigma_X*kappa_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "known": f"epsilon_shell={EPSILON_SHELL:.15g}",
            "missing": "C_X(lambda_X), lambda_X, claim-grade alpha_bound(lambda)",
            "claim_status": "symbolic_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "CE610_1_CX",
            "object": "C_X(lambda_X)",
            "formula": "sigma_X*kappa_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "definition": "dimensionless source-test-normalization product in the R10 Yukawa convention",
            "known": "exact factorization from 607/578/579",
            "missing": "numeric sign, Hessian normalization, source projection, test projection",
            "claim_status": "factorized_symbolic",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "CE610_2_lambda",
            "object": "lambda_X",
            "formula": "lambda_X=sqrt(Z_X/M_X^2)",
            "definition": "finite range from parent Hessian ratio",
            "known": "conditional law derived",
            "missing": "numeric positive M_X^2/Z_X with units",
            "claim_status": "symbolic_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "CE610_3_claim_gate",
            "object": "R10 claim promotion",
            "formula": "abs(epsilon_shell*C_X(lambda_X)) <= alpha_bound(lambda_X)",
            "definition": "claim-grade comparison after all rows are numeric/sourced",
            "known": "runner schema exists",
            "missing": "real bound curve plus numeric parent C_X and lambda_X",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
    ]


def make_pressure_rows() -> list[dict[str, str]]:
    anchors = read_csv(ANCHOR_BOUND)
    c_values = [1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 1e5, 1.345418426702e5, 1e6]
    rows: list[dict[str, str]] = []
    for anchor in anchors:
        alpha_bound = parse_float(anchor.get("alpha_bound", "")) or 1.0
        for c_value in c_values:
            alpha_predicted = EPSILON_SHELL * c_value
            ratio = alpha_predicted / alpha_bound if alpha_bound > 0 else math.inf
            rows.append(
                {
                    "pressure_id": f"AP610_{anchor.get('bound_id','anchor')}_C{c_value:.6g}".replace("+", ""),
                    "bound_id": anchor.get("bound_id", ""),
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", "m"),
                    "alpha_bound_anchor": f"{alpha_bound:.12g}",
                    "abs_CX_trial": f"{c_value:.12e}",
                    "epsilon_shell": f"{EPSILON_SHELL:.12e}",
                    "alpha_predicted_p1": f"{alpha_predicted:.12e}",
                    "ratio_to_anchor_bound": f"{ratio:.12e}",
                    "anchor_private_pass": str(alpha_predicted <= alpha_bound),
                    "claim_status": "anchor_only_nonclaim_pressure",
                    "valid_for_claim": "false",
                }
            )
    return rows


def make_component_budget_rows() -> list[dict[str, str]]:
    anchors = read_csv(ANCHOR_BOUND)
    alpha_bound = parse_float(anchors[0].get("alpha_bound", "")) if anchors else 1.0
    alpha_bound = alpha_bound or 1.0
    max_c_anchor = alpha_bound / EPSILON_SHELL
    scenarios = [
        ("unit_source_unit_test", 1.0, 1.0),
        ("weak_test_1e_minus_2", 1.0, 1e-2),
        ("weak_source_1e_minus_2", 1e-2, 1.0),
        ("both_1e_minus_2", 1e-2, 1e-2),
        ("both_1e_minus_3", 1e-3, 1e-3),
        ("source_screened_1e_minus_4_test_unit", 1e-4, 1.0),
    ]
    rows: list[dict[str, str]] = []
    for scenario_id, q_source, q_test in scenarios:
        product = q_source * q_test
        max_norm = max_c_anchor / product if product > 0 else math.inf
        rows.append(
            {
                "scenario_id": f"CB610_{scenario_id}",
                "Qbar_XH_trial": f"{q_source:.12e}",
                "qbar_XT_trial": f"{q_test:.12e}",
                "source_test_product": f"{product:.12e}",
                "max_abs_normalization_factor_anchor_only": f"{max_norm:.12e}",
                "meaning": "allowed |sigma*kappa/(4*pi Z_X G_obs)| under anchor-only alpha_bound=1 pressure",
                "claim_status": "private_pressure_only_not_claim",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_marker_repair_rows() -> list[dict[str, str]]:
    return [
        {
            "repair_id": "MR610_0_explicit_OED_clause",
            "repair_option": "add parent O(E_D) norm-square activation",
            "clause": "S_act depends on compact-shell amplitude only through ||a_D||^2",
            "would_buy": "p=2 by construction and no linear marker",
            "why_not_selected_now": "it is a new parent closure/action clause, not derived from current corpus",
            "status": "labelled_closure_option_only",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "MR610_1_no_marker_repair",
            "repair_option": "prove no natural marker covector exists",
            "clause": "E_D has no parent-owned covectors besides zero after quotienting",
            "would_buy": "p=1 counterexample removed",
            "why_not_selected_now": "573/574 marker generator debts remain open",
            "status": "theorem_target",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "MR610_2_readout_repair",
            "repair_option": "formal readout-after-variation parent theorem",
            "clause": "readout maps Sol(S_parent)->Obs and cannot source reduced parent terms",
            "would_buy": "blocks post-readout linear marker",
            "why_not_selected_now": "not enough by itself; material/domain markers still survive",
            "status": "partial_repair_target",
            "valid_for_claim": "false",
        },
    ]


def make_mts_template_rows() -> list[dict[str, str]]:
    anchors = read_csv(ANCHOR_BOUND)
    rows: list[dict[str, str]] = []
    for anchor in anchors:
        rows.append(
            {
                "model_id": "MTS_finite_p1_envelope",
                "branch_id": "R10_finite_p1_symbolic_CX",
                "curve_id": "R10_alpha_lambda_curve_MTS_FINITE_P1_ENVELOPE_TEMPLATE",
                "lambda_value": anchor.get("lambda_value", ""),
                "lambda_units": anchor.get("lambda_units", "m"),
                "alpha_predicted": "epsilon_shell*C_X(lambda_X)",
                "alpha_bound": anchor.get("alpha_bound", "1.0"),
                "alpha_bound_source": f"source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::{anchor.get('bound_id', '')}",
                "force_law_form": "Yukawa_potential_alpha",
                "derivation_status": "finite_p1_symbolic_envelope_nonclaim",
                "formula_reference": "610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md::CE610_0_alpha_law",
                "source_file": "610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md",
                "assumptions": "MISSING_C_X;MISSING_PARENT_LAMBDA;anchor_bound_only;finite_p1_not_local_GR_theorem",
                "valid_for_claim": "false",
                "notes": "Template row only; runner must reject until C_X, lambda_X, and alpha_bound(lambda) are real.",
            }
        )
    return rows


def make_runner_summary(run_result: dict[str, Any]) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_610_FINITE_P1_TEMPLATE_RECHECK",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "mts_rows": str(status["mts_rows"]),
            "valid_mts_rows": str(status["valid_mts_rows"]),
            "bound_rows": str(status["bound_rows"]),
            "valid_bound_rows": str(status["valid_bound_rows"]),
            "comparison_rows": str(status["comparison_rows"]),
            "passed_rows": str(status["passed_rows"]),
            "blocked_or_failed_rows": str(status["blocked_or_failed_rows"]),
            "R10_pass_for_claim": str(status["R10_pass_for_claim"]),
            "claim_allowed": str(status["claim_allowed"]),
            "notes": "required blocked result: finite p1 template remains symbolic and anchor bounds are nonclaim",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D610_0_method",
            "status": STATUS,
            "decision": "select finite p1 coefficient envelope as best method",
            "meaning": "testable and honest; avoids adding unearned O(E_D) closure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D610_1_pressure",
            "status": "private_pressure_useful",
            "decision": "use anchor-only pressure to size C_X, not as evidence",
            "meaning": "order-one C_X is not immediately absurd, but real bound curve is still mandatory",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D610_2_marker_repair",
            "status": "deferred",
            "decision": "keep marker exclusion repair as labelled closure/theorem target",
            "meaning": "p2 can return only through explicit parent clause or no-marker proof",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D610_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "finite branch is a residual envelope, not GR reduction",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU610_0_data_route",
            "allowed_after_610": "QA real R10 bound curve or acquire official/digitized alpha(lambda) rows",
            "forbidden_after_610": "use anchor-only pressure as claim evidence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU610_1_theory_route",
            "allowed_after_610": "derive or bound C_X components K/Z, Qbar_XH, qbar_XT, lambda_X",
            "forbidden_after_610": "treat symbolic C_X as a prediction",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU610_2_closure_route",
            "allowed_after_610": "write O(E_D) norm-square clause only as labelled closure",
            "forbidden_after_610": "smuggle p2 closure into derived local GR",
            "next_action": "defer unless finite branch fails badly",
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": f"{EPSILON_SHELL:.15g}",
            "selected_method": "finite_p1_coefficient_envelope",
            "marker_closure_selected": "false",
            "finite_p1_numeric": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def count_claim_rows(row_sets: list[list[dict[str, Any]]]) -> int:
    return sum(1 for rows in row_sets for row in rows if is_true(str(row.get("valid_for_claim", ""))))


def make_validation_rows(
    sources: list[dict[str, str]],
    method_rows: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    budget_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_609_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    selected = [row for row in method_rows if row["selection"] == "selected_best_method"]
    pressure_numeric = all(parse_float(row["alpha_predicted_p1"]) is not None for row in pressure_rows)
    pressure_nonclaim = all(row["valid_for_claim"] == "false" for row in pressure_rows)
    budget_numeric = all(parse_float(row["max_abs_normalization_factor_anchor_only"]) is not None for row in budget_rows)
    repair_not_selected = all(row["valid_for_claim"] == "false" for row in repair_rows)
    template_symbolic = all(parse_float(row.get("alpha_predicted", "")) is None for row in mts_rows)
    template_nonclaim = all(row.get("valid_for_claim") == "false" for row in mts_rows)
    live_mts_rows = read_csv(LIVE_MTS)
    live_bound_rows = read_csv(LIVE_BOUND)
    runner = runner_rows[0]
    claim_rows = count_claim_rows(
        [
            method_rows,
            coefficient_rows,
            pressure_rows,
            budget_rows,
            repair_rows,
            mts_rows,
            decision_rows,
            summary_rows,
        ]
    )
    return [
        {
            "check_id": "V610_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V610_1_prior_609_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V610_2_best_method_selected",
            "result": "pass" if len(selected) == 1 and selected[0]["method"] == "finite p=1 coefficient envelope" else "fail",
            "detail": f"selected={selected[0]['method'] if selected else 'none'}",
        },
        {
            "check_id": "V610_3_coefficient_envelope_written",
            "result": "pass" if len(coefficient_rows) >= 4 and all(row["valid_for_claim"] == "false" for row in coefficient_rows) else "fail",
            "detail": f"coefficient_rows={len(coefficient_rows)}",
        },
        {
            "check_id": "V610_4_pressure_numeric_nonclaim",
            "result": "pass" if pressure_rows and pressure_numeric and pressure_nonclaim else "fail",
            "detail": f"pressure_rows={len(pressure_rows)};numeric={pressure_numeric};nonclaim={pressure_nonclaim}",
        },
        {
            "check_id": "V610_5_component_budget_numeric_nonclaim",
            "result": "pass" if budget_rows and budget_numeric and all(row["valid_for_claim"] == "false" for row in budget_rows) else "fail",
            "detail": f"budget_rows={len(budget_rows)};numeric={budget_numeric}",
        },
        {
            "check_id": "V610_6_marker_repair_not_smuggled",
            "result": "pass" if repair_rows and repair_not_selected else "fail",
            "detail": f"repair_rows={len(repair_rows)};claim_rows={count_claim_rows([repair_rows])}",
        },
        {
            "check_id": "V610_7_template_symbolic_nonclaim",
            "result": "pass" if mts_rows and template_symbolic and template_nonclaim else "fail",
            "detail": f"template_rows={len(mts_rows)};symbolic={template_symbolic};nonclaim={template_nonclaim}",
        },
        {
            "check_id": "V610_8_runner_blocks_template",
            "result": "pass"
            if runner["R10_pass_for_claim"] == "False"
            and runner["claim_allowed"] == "False"
            and runner["valid_mts_rows"] == "0"
            and runner["valid_bound_rows"] == "0"
            else "fail",
            "detail": (
                f"valid_mts={runner['valid_mts_rows']};valid_bound={runner['valid_bound_rows']};"
                f"R10_pass={runner['R10_pass_for_claim']};claim_allowed={runner['claim_allowed']}"
            ),
        },
        {
            "check_id": "V610_9_live_files_not_overwritten",
            "result": "pass" if len(live_mts_rows) == 2 and len(live_bound_rows) == 2 else "fail",
            "detail": f"live_mts_rows={len(live_mts_rows)};live_bound_rows={len(live_bound_rows)}",
        },
        {
            "check_id": "V610_10_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V610_11_no_R10_or_local_GR_claim",
            "result": "pass"
            if summary_rows[0]["R10_pass"] == "false"
            and summary_rows[0]["WEP_pass"] == "false"
            and summary_rows[0]["PPN_pass"] == "false"
            and summary_rows[0]["local_GR_pass"] == "false"
            else "fail",
            "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    method_rows: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    budget_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 610 Y5 R10 finite p1 branch coefficient envelope or marker-exclusion repair

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- Best method selected: finite `p=1` coefficient envelope, not an unearned `O(E_D)` closure.
- The working law is `alpha_X(lambda_X)=epsilon_shell*C_X(lambda_X)`.
- Anchor-only pressure says order-one `C_X` is not immediately absurd, but that is private guidance only, not evidence.
- The next executable wall is now precise: real `alpha_bound(lambda)` curve plus numeric/source-backed `C_X(lambda_X)` and `lambda_X`.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Method Selection
{markdown_table(method_rows, ["method_id", "method", "selection", "why_best", "physics_cost", "output", "valid_for_claim"])}

## Finite P1 Coefficient Envelope
{markdown_table(coefficient_rows, ["coefficient_id", "object", "formula", "definition", "known", "missing", "claim_status", "valid_for_claim"])}

## Alpha Pressure Envelope
{markdown_table(pressure_rows, ["pressure_id", "bound_id", "lambda_value", "lambda_units", "alpha_bound_anchor", "abs_CX_trial", "epsilon_shell", "alpha_predicted_p1", "ratio_to_anchor_bound", "anchor_private_pass", "claim_status", "valid_for_claim"])}

## Component Budget Scenarios
{markdown_table(budget_rows, ["scenario_id", "Qbar_XH_trial", "qbar_XT_trial", "source_test_product", "max_abs_normalization_factor_anchor_only", "meaning", "claim_status", "valid_for_claim"])}

## Marker-Exclusion Repair Option
{markdown_table(repair_rows, ["repair_id", "repair_option", "clause", "would_buy", "why_not_selected_now", "status", "valid_for_claim"])}

## MTS Finite P1 Template
{markdown_table(mts_rows, MTS_TEMPLATE_FIELDS)}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_610", "forbidden_after_610", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is the Money Mayweather move: stay in the fight, do not throw a fake knockout punch. We are not claiming local GR from `p=1`; we are making the finite branch measurable. If the real curve and real coefficients let it survive, we have a respectable residual branch. If it fails, we know exactly where to return: marker exclusion or a labelled parent norm-square closure.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"

    sources = make_sources()
    method_rows = make_method_selection_rows()
    coefficient_rows = make_coefficient_envelope_rows()
    pressure_rows = make_pressure_rows()
    budget_rows = make_component_budget_rows()
    repair_rows = make_marker_repair_rows()
    mts_rows = make_mts_template_rows()

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(METHOD_SELECTION_PATH, method_rows, ["method_id", "method", "selection", "why_best", "physics_cost", "output", "valid_for_claim"])
    write_csv(COEFFICIENT_ENVELOPE_PATH, coefficient_rows, ["coefficient_id", "object", "formula", "definition", "known", "missing", "claim_status", "valid_for_claim"])
    write_csv(PRESSURE_PATH, pressure_rows, ["pressure_id", "bound_id", "lambda_value", "lambda_units", "alpha_bound_anchor", "abs_CX_trial", "epsilon_shell", "alpha_predicted_p1", "ratio_to_anchor_bound", "anchor_private_pass", "claim_status", "valid_for_claim"])
    write_csv(COMPONENT_BUDGET_PATH, budget_rows, ["scenario_id", "Qbar_XH_trial", "qbar_XT_trial", "source_test_product", "max_abs_normalization_factor_anchor_only", "meaning", "claim_status", "valid_for_claim"])
    write_csv(MARKER_REPAIR_PATH, repair_rows, ["repair_id", "repair_option", "clause", "would_buy", "why_not_selected_now", "status", "valid_for_claim"])
    write_csv(MTS_TEMPLATE_PATH, mts_rows, MTS_TEMPLATE_FIELDS)

    runner_result = run_runner(MTS_TEMPLATE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result)
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation_rows(
        sources,
        method_rows,
        coefficient_rows,
        pressure_rows,
        budget_rows,
        repair_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_610", "forbidden_after_610", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "epsilon_shell", "selected_method", "marker_closure_selected", "finite_p1_numeric", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_doc(
        generated,
        run_root,
        sources,
        method_rows,
        coefficient_rows,
        pressure_rows,
        budget_rows,
        repair_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        route_rows,
        validation_rows,
    )

    status = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_status": rel(result_dir / "R10_runner_status.json"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
