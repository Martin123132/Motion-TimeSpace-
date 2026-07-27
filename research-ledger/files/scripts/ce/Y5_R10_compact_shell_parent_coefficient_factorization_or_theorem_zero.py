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

SLUG = "Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero"
DOC_PATH = ROOT / "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_607_SOURCE_REGISTER.csv"
DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_607_PARENT_COEFFICIENT_FACTORIZATION.csv"
EXPONENT_GATE_PATH = RESIDUALS / "P8_Y5_R10_607_EPSILON_EXPONENT_GATE.csv"
THEOREM_ZERO_PATH = RESIDUALS / "P8_Y5_R10_607_THEOREM_ZERO_GATE.csv"
PRESSURE_PATH = RESIDUALS / "P8_Y5_R10_607_COEFFICIENT_PRESSURE_TABLE.csv"
PARENT_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_607_PARENT_INPUT_UPDATE.csv"
MTS_TEMPLATE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_COMPACT_SHELL_FACTOR_BRANCH_TEMPLATE.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_607_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_607_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_607_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_607_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_607_VALIDATION.csv"

PRIOR_606_VALIDATION = RESIDUALS / "P8_Y5_BRR545_606_VALIDATION.csv"
PRIOR_606_LAW = RESIDUALS / "P8_Y5_R10_606_COMPACT_SHELL_ALPHA_LAW_CONTRACT.csv"
PRIOR_606_REQUIREMENTS = RESIDUALS / "P8_Y5_R10_606_PARENT_INPUT_REQUIREMENTS.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"

STATUS = "Y5_R10_compact_shell_alpha_factorization_derived_conditionally_exponent_and_zero_theorem_not_parent_signed"
CLAIM_CEILING = "conditional_factorization_and_pressure_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md"
EPSILON_SHELL = 7.432631961576971e-06

SOURCE_FILES = [
    ("606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md", "immediate 606 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_606_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_606_COMPACT_SHELL_ALPHA_LAW_CONTRACT.csv", "R10 alpha law contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_606_PARENT_INPUT_REQUIREMENTS.csv", "parent inputs to fill"),
    ("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_COMPACT_SHELL_UNIT_MAP_TEMPLATE.csv", "prior symbolic unit-map template"),
    ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "quadratic Green-function product law"),
    ("source-intake/mts_residuals/P8_Y5_R10_578_PRODUCT_COEFFICIENT_DERIVATION.csv", "product coefficient definitions"),
    ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "Hessian/source countermodel and theorem-zero gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_579_THEOREM_ZERO_RETURN_GATE.csv", "zero route status"),
    ("476-double-zero-memory-coupling-origin-or-coefficient-runner.md", "p>=2 double-zero requirement and origin failure"),
    ("475-domain-selector-parent-action-clause-or-coefficient-fill.md", "double-zero parent-action clause"),
    ("572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md", "neutrality versus finite coefficient fork"),
    ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "qbar/source-current universality failure"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor-only non-claim R10 bound rows"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_compact_shell_parent_coefficient_factorization_or_theorem_zero.py", "this checkpoint generator"),
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


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_derivation_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "PCF607_0_parent_quadratic_block",
            "object": "local X exchange mode",
            "derivation": "expand parent action around compact local branch: S_X^(2)=1/2 int sqrt(h)[Z_X |grad X|^2+M_X^2 X^2]-int sqrt(h) X J_X",
            "result": "quadratic operator inherited from 578/579",
            "formula": "(-Z_X Delta + M_X^2)X=J_X",
            "status": "conditional_parent_block",
            "claim_status": "nonclaim",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_1_compact_shell_source_pullout",
            "object": "compact-shell source amplitude",
            "derivation": "if the finite local residual sources X through an activation f(chi_D), write J_X=epsilon_shell^p kappa_X rho_X with p the Taylor order of f at the local branch",
            "result": "epsilon exponent separated from the unknown parent coefficient",
            "formula": "J_X = epsilon_shell^p kappa_X rho_X; p=1 is linear, p>=2 is double-zero",
            "status": "factorization_derived_p_not_parent_owned",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_2_green_solution",
            "object": "exterior profile",
            "derivation": "solve the static exterior Green problem for a compact source with range lambda_X=sqrt(Z_X/M_X^2)",
            "result": "Yukawa profile with compact-shell amplitude as a multiplicative factor",
            "formula": "X(r)=epsilon_shell^p kappa_X Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi Z_X r)",
            "status": "derived_conditionally",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_3_test_potential",
            "object": "ordinary test-body potential",
            "derivation": "couple test body through q_X^T=-delta S_T/dX and compare with V_N=-G_obs M_H m_T/r",
            "result": "R10 alpha is the normalized source-test Green coefficient",
            "formula": "alpha_X=sigma_X epsilon_shell^p kappa_X Q_X^H q_X^T/(4*pi Z_X G_obs M_H m_T)",
            "status": "derived_conditionally",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_4_normalized_product",
            "object": "coefficient product C_X",
            "derivation": "define Qbar_XH=Q_X^H/M_H, qbar_XT=q_X^T/m_T, and C_X=sigma_X kappa_X Qbar_XH qbar_XT/(4*pi Z_X G_obs)",
            "result": "alpha_X(lambda_X)=epsilon_shell^p C_X(lambda_X)",
            "formula": "C_X=sigma_X kappa_X Qbar_XH(lambda_X) qbar_XT/(4*pi Z_X G_obs)",
            "status": "exact_factorization_derived_conditionally",
            "claim_status": "blocked_by_CX_and_p",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_5_606_linear_template_relation",
            "object": "606 alpha law",
            "derivation": "606 is recovered as the conservative p=1 branch after absorbing kappa_X into K_X",
            "result": "606 formula is a special case, not the full parent exponent law",
            "formula": "alpha_X=sigma_X epsilon_shell K_X Qbar_source_X qbar_test_X/(4*pi Z_X G_obs)",
            "status": "p_equals_1_special_case",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PCF607_6_verdict",
            "object": "derivation result",
            "derivation": "the Green-function coefficient product is derived; the parent exponent p, sign, source/test projections, and Hessian normalization are not",
            "result": "derive_factorization_not_numeric_pass",
            "formula": "alpha_X=lambda branch claim only after p, C_X, lambda_X, and alpha_bound(lambda) are real",
            "status": "progress_with_claim_block",
            "claim_status": "no_R10_claim",
            "valid_for_claim": "false",
        },
    ]


def make_exponent_rows() -> list[dict[str, str]]:
    return [
        {
            "p_gate": "P607_0_unsuppressed",
            "p": "0",
            "activation": "f(chi_D)=1 or source term independent of compact-shell residual",
            "local_effect": "ordinary finite fifth-force branch with no compact-shell suppression",
            "derivation_status": "not_supported_for_local_silence",
            "claim_impact": "would need small C_X or short lambda; not a GR-reduction theorem",
            "valid_for_claim": "false",
        },
        {
            "p_gate": "P607_1_linear",
            "p": "1",
            "activation": "f(chi_D)=chi_D or source term linear in epsilon_shell",
            "local_effect": "alpha_X=epsilon_shell C_X; empirical suppression exists but selector exchange is not double-zero silent",
            "derivation_status": "606_conservative_template",
            "claim_impact": "could survive R10 for order-one C_X at anchor pressure, but still not local-GR theorem-zero",
            "valid_for_claim": "false",
        },
        {
            "p_gate": "P607_2_quadratic",
            "p": "2",
            "activation": "f(chi_D)=chi_D^2 or norm-square activation",
            "local_effect": "alpha_X=epsilon_shell^2 C_X and f(0)=f_prime(0)=0 if chi_local=0",
            "derivation_status": "sufficient_double_zero_contract_not_parent_derived",
            "claim_impact": "best local-silence route if parent symmetry derives it",
            "valid_for_claim": "false",
        },
        {
            "p_gate": "P607_3_determinant",
            "p": "3",
            "activation": "determinant/coherent-volume current such as J_C~det(Q_coh)",
            "local_effect": "stronger suppression and double-zero if determinant current is parent-owned",
            "derivation_status": "conditional_clue_from_476_not_parent_owned",
            "claim_impact": "promising but would need normalization and FLRW survival proof",
            "valid_for_claim": "false",
        },
        {
            "p_gate": "P607_4_general_double_zero",
            "p": ">=2",
            "activation": "smooth f with Taylor coefficients f(0)=0 and f_prime(0)=0",
            "local_effect": "local memory/source term can be silent only when chi_local=0 is also parent-derived",
            "derivation_status": "derived_as_requirement_not_as_parent_origin",
            "claim_impact": "next derivation target is origin of p>=2 or source neutrality",
            "valid_for_claim": "false",
        },
    ]


def make_theorem_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "TZ607_0_no_pole",
            "zero_route": "K_X=0 or no propagating X pole",
            "condition": "constraint algebra removes X before matter/source variation",
            "would_imply": "C_X=0 and alpha_X=0",
            "current_status": "not_derived",
            "blocker": "current branch still uses a finite quadratic X block",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "TZ607_1_source_neutrality",
            "zero_route": "Qbar_XH(lambda_X)=0",
            "condition": "compact source plus boundary/projector/memory/domain source is orthogonal to measured-mass projection",
            "would_imply": "C_X=0 for laboratory source",
            "current_status": "not_derived",
            "blocker": "Pi_M and hidden source channels remain unclosed",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "TZ607_2_test_neutrality",
            "zero_route": "qbar_XT=0",
            "condition": "ordinary matter action and observed coframe are X-blind before variation",
            "would_imply": "C_X=0 for ordinary test bodies and likely helps WEP",
            "current_status": "conditional_only",
            "blocker": "579 conformal countermodel shows current premises allow qbar_XT nonzero",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "TZ607_3_double_zero_exact_local",
            "zero_route": "epsilon_shell=0 with p>=2 and chi_local=0",
            "condition": "parent derives exact local compact-shell zero, not merely small epsilon",
            "would_imply": "alpha_X=0 in exact local vacuum while FLRW branch can remain active",
            "current_status": "not_derived_for_exact_local_branch",
            "blocker": "epsilon_shell is currently finite proxy and p>=2 origin is not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "TZ607_4_positive_nohair",
            "zero_route": "J_X=0 and boundary flux=0",
            "condition": "Z_X>0, M_X^2>0, regular decay, and channelwise source silence",
            "would_imply": "X=0 by positive integral identity",
            "current_status": "certificate_template_unfilled",
            "blocker": "source-zero and boundary-zero premises are not signed",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "TZ607_5_verdict",
            "zero_route": "R10 theorem-zero",
            "condition": "one zero route above must be parent-derived",
            "would_imply": "R10 alpha row can be zero by theorem",
            "current_status": "fail_current_claim",
            "blocker": "factorization derived but no zero factor is parent-signed",
            "valid_for_claim": "false",
        },
    ]


def make_pressure_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    anchors = read_csv(ANCHOR_BOUND)
    if not anchors:
        anchors = [
            {
                "bound_id": "fallback_anchor_38p6um",
                "lambda_value": "3.86e-5",
                "lambda_units": "m",
                "alpha_bound": "1.0",
            }
        ]
    for anchor in anchors:
        alpha_bound = parse_float(anchor.get("alpha_bound", "")) or 1.0
        for p in range(0, 4):
            epsilon_power = EPSILON_SHELL**p
            alpha_if_unit = epsilon_power
            max_c = alpha_bound / epsilon_power if epsilon_power > 0 else math.inf
            rows.append(
                {
                    "pressure_id": f"CP607_{anchor.get('bound_id', 'anchor')}_p{p}",
                    "bound_id": anchor.get("bound_id", ""),
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", ""),
                    "alpha_bound_anchor": f"{alpha_bound:.12g}",
                    "p": str(p),
                    "epsilon_shell_power": f"{epsilon_power:.12e}",
                    "alpha_if_abs_CX_equals_1": f"{alpha_if_unit:.12e}",
                    "max_abs_CX_allowed_by_anchor": f"{max_c:.12e}",
                    "claim_status": "anchor_only_nonclaim_pressure",
                    "valid_for_claim": "false",
                }
            )
    return rows


def make_parent_update_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "PUI607_0_p",
            "required_input": "epsilon exponent p",
            "exact_definition": "Taylor order of the parent activation f(chi_D) that sources the finite X mode",
            "derived_status": "requirement_only",
            "acceptable_closure": "parent symmetry/norm-square/topological determinant giving p>=2, or explicit p=1 finite residual branch",
            "next_action": "derive p origin from parent symmetry or demote to finite score",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI607_1_CX",
            "required_input": "C_X(lambda_X)",
            "exact_definition": "sigma_X kappa_X Qbar_XH(lambda_X) qbar_XT/(4*pi Z_X G_obs)",
            "derived_status": "factorized_symbolically",
            "acceptable_closure": "numeric parent coefficients with units/source paths, or theorem-zero factor",
            "next_action": "attack qbar/source neutrality or explicit parent X block",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI607_2_lambda_X",
            "required_input": "lambda_X",
            "exact_definition": "sqrt(Z_X/M_X^2)",
            "derived_status": "conditional_law_only",
            "acceptable_closure": "parent Hessian ratio M_X^2/Z_X with positive signs and units",
            "next_action": "keep mass-gap target in queue",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI607_3_zero_factor",
            "required_input": "K_X=0 or Qbar_XH=0 or qbar_XT=0 or exact epsilon=0 branch",
            "exact_definition": "any parent-owned zero in alpha_X=epsilon_shell^p C_X",
            "derived_status": "not_signed",
            "acceptable_closure": "channelwise theorem-zero, not cancellation",
            "next_action": "try p>=2/exact-local-zero route first because it also supports GR reduction",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI607_4_bound_curve",
            "required_input": "claim-grade alpha_bound(lambda)",
            "exact_definition": "external R10 curve ordinate at derived lambda_X",
            "derived_status": "anchor_only_nonclaim",
            "acceptable_closure": "digitized/source-backed full curve rows",
            "next_action": "defer until coefficient side exists",
            "valid_for_claim": "false",
        },
    ]


def make_mts_template_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    anchors = read_csv(ANCHOR_BOUND)
    for anchor in anchors:
        for p in (1, 2):
            rows.append(
                {
                    "model_id": "MTS_compact_shell_factor_branch",
                    "branch_id": f"R10_symbolic_factor_p{p}",
                    "curve_id": "R10_alpha_lambda_curve_MTS_COMPACT_SHELL_FACTOR_BRANCH_TEMPLATE",
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", "m"),
                    "alpha_predicted": f"(epsilon_shell**{p})*C_X(lambda_X)",
                    "alpha_bound": anchor.get("alpha_bound", "1.0"),
                    "alpha_bound_source": f"source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::{anchor.get('bound_id', '')}",
                    "force_law_form": "Yukawa_potential_alpha",
                    "derivation_status": "symbolic_factorization_nonclaim_p_not_parent_signed",
                    "formula_reference": "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md::PCF607_4_normalized_product",
                    "source_file": "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md",
                    "assumptions": "MISSING_C_X;MISSING_PARENT_EXPONENT_ORIGIN;MISSING_LAMBDA_HESSIAN;anchor_bound_only",
                    "valid_for_claim": "false",
                    "notes": "Template row only; runner must reject because alpha is symbolic and bound anchors are nonclaim.",
                }
            )
    return rows


def make_runner_summary(run_result: dict[str, Any]) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_607_FACTOR_TEMPLATE_RECHECK",
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
            "notes": "required blocked result: p/C_X templates are symbolic and anchor bounds are nonclaim",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D607_0_factorization_derived",
            "status": "conditional_derivation_progress",
            "decision": "accept alpha_X=lambda branch factorization alpha_X=epsilon_shell^p C_X(lambda_X)",
            "meaning": "the coefficient problem is now p plus C_X plus lambda_X, not an undefined residual",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D607_1_p_not_signed",
            "status": "blocked_for_claim",
            "decision": "do not assume p=2 or p=3 even though they are attractive",
            "meaning": "476 gives p>=2 as a requirement for local silence, not as a parent theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D607_2_theorem_zero_not_closed",
            "status": "zero_certificate_unfilled",
            "decision": "do not claim R10 theorem-zero",
            "meaning": "no pole/source/test/exact-local-zero route is parent-signed yet",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D607_3_pressure_read",
            "status": "nonclaim_pressure_useful",
            "decision": "use epsilon powers as private pressure guidance only",
            "meaning": "order-one C_X would be mild at anchor pressure for p>=1, but anchors are not a claim curve",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU607_0_best_derivation_route",
            "allowed_after_607": "derive p>=2 from parent symmetry, norm-square, determinant, or topological pairing",
            "forbidden_after_607": "silently choosing p=2 because it makes bounds comfortable",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU607_1_source_neutrality_route",
            "allowed_after_607": "try Qbar_XH=0 or qbar_XT=0 as channelwise theorem-zero",
            "forbidden_after_607": "claiming matter neutrality despite 579 conformal countermodel",
            "next_action": "use only if p-origin route fails",
        },
        {
            "route_id": "RU607_2_finite_score_route",
            "allowed_after_607": "retain alpha_X=epsilon_shell^p C_X for future numeric residual scoring",
            "forbidden_after_607": "calling a finite small alpha a GR reduction without PPN/WEP gates",
            "next_action": "defer scoring until p,C_X,lambda_X and full bound curve exist",
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": f"{EPSILON_SHELL:.15g}",
            "derived_factorization": "alpha_X=epsilon_shell^p*C_X(lambda_X)",
            "p_parent_signed": "false",
            "C_X_numeric": "false",
            "theorem_zero_signed": "false",
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
    derivation_rows: list[dict[str, str]],
    exponent_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_606_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    factor_row = [row for row in derivation_rows if row["step_id"] == "PCF607_4_normalized_product"]
    p_double_rows = [row for row in exponent_rows if row["p"] in {"2", "3", ">=2"}]
    zero_claim_rows = [row for row in theorem_rows if is_true(row.get("valid_for_claim", ""))]
    template_symbolic = all(parse_float(row.get("alpha_predicted", "")) is None for row in mts_rows)
    template_nonclaim = all(row.get("valid_for_claim") == "false" for row in mts_rows)
    runner = runner_rows[0]
    claim_rows = count_claim_rows(
        [
            derivation_rows,
            exponent_rows,
            theorem_rows,
            pressure_rows,
            parent_rows,
            mts_rows,
            decision_rows,
            summary_rows,
        ]
    )
    return [
        {
            "check_id": "V607_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V607_1_prior_606_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V607_2_factorization_derived_conditionally",
            "result": "pass"
            if factor_row
            and factor_row[0]["result"] == "alpha_X(lambda_X)=epsilon_shell^p C_X(lambda_X)"
            and "Qbar_XH" in factor_row[0]["formula"]
            else "fail",
            "detail": f"{factor_row[0]['result']};{factor_row[0]['formula']}" if factor_row else "missing_factor_row",
        },
        {
            "check_id": "V607_3_exponent_gate_keeps_p_unpromoted",
            "result": "pass" if len(p_double_rows) == 3 and all(row["valid_for_claim"] == "false" for row in exponent_rows) else "fail",
            "detail": f"exponent_rows={len(exponent_rows)};double_zero_rows={len(p_double_rows)};claim_rows={count_claim_rows([exponent_rows])}",
        },
        {
            "check_id": "V607_4_theorem_zero_not_overclaimed",
            "result": "pass" if not zero_claim_rows and theorem_rows[-1]["current_status"] == "fail_current_claim" else "fail",
            "detail": f"zero_claim_rows={len(zero_claim_rows)};verdict={theorem_rows[-1]['current_status']}",
        },
        {
            "check_id": "V607_5_pressure_rows_numeric_nonclaim",
            "result": "pass" if pressure_rows and all(parse_float(row["epsilon_shell_power"]) is not None for row in pressure_rows) and all(row["valid_for_claim"] == "false" for row in pressure_rows) else "fail",
            "detail": f"pressure_rows={len(pressure_rows)};epsilon={EPSILON_SHELL:.12e}",
        },
        {
            "check_id": "V607_6_template_symbolic_nonclaim",
            "result": "pass" if mts_rows and template_symbolic and template_nonclaim else "fail",
            "detail": f"template_rows={len(mts_rows)};symbolic={template_symbolic};nonclaim={template_nonclaim}",
        },
        {
            "check_id": "V607_7_runner_blocks_template",
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
            "check_id": "V607_8_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V607_9_no_R10_or_local_GR_claim",
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
    derivation_rows: list[dict[str, str]],
    exponent_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 607 Y5 R10 compact-shell parent coefficient factorization or theorem-zero

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The coefficient product can be derived structurally: `alpha_X(lambda_X)=epsilon_shell^p C_X(lambda_X)`.
- The derived coefficient is `C_X=sigma_X kappa_X Qbar_XH(lambda_X) qbar_XT/(4*pi Z_X G_obs)`.
- The exponent `p` is now the key local-GR lock: `p=1` is the conservative finite branch; `p>=2` is the double-zero route, but its parent origin is not yet signed.
- No theorem-zero is promoted: `K_X=0`, `Qbar_XH=0`, `qbar_XT=0`, or exact local `epsilon_shell=0` are still target theorems.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Parent Coefficient Factorization
{markdown_table(derivation_rows, ["step_id", "object", "derivation", "result", "formula", "status", "claim_status", "valid_for_claim"])}

## Epsilon Exponent Gate
{markdown_table(exponent_rows, ["p_gate", "p", "activation", "local_effect", "derivation_status", "claim_impact", "valid_for_claim"])}

## Theorem-Zero Gate
{markdown_table(theorem_rows, ["zero_id", "zero_route", "condition", "would_imply", "current_status", "blocker", "valid_for_claim"])}

## Coefficient Pressure Table
{markdown_table(pressure_rows, ["pressure_id", "bound_id", "lambda_value", "lambda_units", "alpha_bound_anchor", "p", "epsilon_shell_power", "alpha_if_abs_CX_equals_1", "max_abs_CX_allowed_by_anchor", "claim_status", "valid_for_claim"])}

## Parent Input Update
{markdown_table(parent_rows, ["input_id", "required_input", "exact_definition", "derived_status", "acceptable_closure", "next_action", "valid_for_claim"])}

## MTS Factor Template
{markdown_table(mts_rows, MTS_TEMPLATE_FIELDS)}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_607", "forbidden_after_607", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is progress, but not a victory lap. We have converted the fuzzy compact-shell residual into a precise coefficient theorem target. If the parent action gives `p>=2` naturally, the local branch starts looking much healthier because the same double-zero condition also helps GR reduction. If the parent only gives `p=1`, the branch is still potentially scoreable, but it is an empirical residual rather than a derived local-GR silence theorem. Next best punch: derive the origin of `p>=2`, or prove source/test neutrality.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"

    sources = make_sources()
    derivation_rows = make_derivation_rows()
    exponent_rows = make_exponent_rows()
    theorem_rows = make_theorem_zero_rows()
    pressure_rows = make_pressure_rows()
    parent_rows = make_parent_update_rows()
    mts_rows = make_mts_template_rows()

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(DERIVATION_PATH, derivation_rows, ["step_id", "object", "derivation", "result", "formula", "status", "claim_status", "valid_for_claim"])
    write_csv(EXPONENT_GATE_PATH, exponent_rows, ["p_gate", "p", "activation", "local_effect", "derivation_status", "claim_impact", "valid_for_claim"])
    write_csv(THEOREM_ZERO_PATH, theorem_rows, ["zero_id", "zero_route", "condition", "would_imply", "current_status", "blocker", "valid_for_claim"])
    write_csv(PRESSURE_PATH, pressure_rows, ["pressure_id", "bound_id", "lambda_value", "lambda_units", "alpha_bound_anchor", "p", "epsilon_shell_power", "alpha_if_abs_CX_equals_1", "max_abs_CX_allowed_by_anchor", "claim_status", "valid_for_claim"])
    write_csv(PARENT_UPDATE_PATH, parent_rows, ["input_id", "required_input", "exact_definition", "derived_status", "acceptable_closure", "next_action", "valid_for_claim"])
    write_csv(MTS_TEMPLATE_PATH, mts_rows, MTS_TEMPLATE_FIELDS)

    runner_result = run_runner(MTS_TEMPLATE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result)
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation_rows(
        sources,
        derivation_rows,
        exponent_rows,
        theorem_rows,
        pressure_rows,
        parent_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_607", "forbidden_after_607", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "epsilon_shell", "derived_factorization", "p_parent_signed", "C_X_numeric", "theorem_zero_signed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_doc(
        generated,
        run_root,
        sources,
        derivation_rows,
        exponent_rows,
        theorem_rows,
        pressure_rows,
        parent_rows,
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
