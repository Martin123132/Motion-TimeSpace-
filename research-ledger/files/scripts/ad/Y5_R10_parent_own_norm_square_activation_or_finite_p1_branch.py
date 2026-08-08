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

SLUG = "Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch"
DOC_PATH = ROOT / "609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_609_SOURCE_REGISTER.csv"
AMPLITUDE_PATH = RESIDUALS / "P8_Y5_R10_609_PRIMITIVE_AMPLITUDE_OWNERSHIP.csv"
FIBRE_METRIC_PATH = RESIDUALS / "P8_Y5_R10_609_FIBRE_METRIC_OWNERSHIP.csv"
NO_LINEAR_PATH = RESIDUALS / "P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv"
LOCAL_FLRW_PATH = RESIDUALS / "P8_Y5_R10_609_LOCAL_FLRW_BRANCH_SPLIT_GATE.csv"
P_BRANCH_PATH = RESIDUALS / "P8_Y5_R10_609_P_BRANCH_DECISION.csv"
FINITE_P1_PATH = RESIDUALS / "P8_Y5_R10_609_FINITE_P1_BRANCH_LEDGER.csv"
MTS_TEMPLATE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_P_BRANCH_609_TEMPLATE.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_609_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_609_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_609_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_609_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_609_VALIDATION.csv"

PRIOR_608_VALIDATION = RESIDUALS / "P8_Y5_BRR545_608_VALIDATION.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"

STATUS = "Y5_R10_norm_square_parent_ownership_attempt_partial_marker_counterexample_keeps_p1_finite_branch_legal"
CLAIM_CEILING = "norm_square_parent_ownership_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "610-Y5-R10-finite-p1-branch-coefficient-envelope-or-marker-exclusion-repair.md"
EPSILON_SHELL = 7.432631961576971e-06

SOURCE_FILES = [
    ("608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md", "immediate 608 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_608_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_608_PARENT_INPUT_UPDATE.csv", "norm-square promotion requirements"),
    ("source-intake/mts_residuals/P8_Y5_R10_608_NORMSQUARE_P2_THEOREM_ATTEMPT.csv", "conditional p=2 theorem"),
    ("407-primitive-relational-quotient-action-sketch.md", "primitive quotient action sketch"),
    ("413-no-marker-parent-action-theorem-attempt.md", "marker counterexample classification"),
    ("573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md", "no-marker reduction and generator debts"),
    ("574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md", "generator elimination order"),
    ("601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md", "relative-Hodge/fibre metric ownership blockers"),
    ("603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md", "N_D primitive attempt"),
    ("608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md", "p=2/p=3 theorem target"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor-only non-claim R10 bound rows"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_parent_own_norm_square_activation_or_finite_p1_branch.py", "this checkpoint generator"),
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


def make_amplitude_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PA609_0_candidate_bundle",
            "required_object": "primitive relative-memory/source fibre E_D",
            "attempt": "identify compact-shell amplitude as a_D in E_D, with local trivial branch a_D=0",
            "result": "formal_candidate",
            "why_not_claim": "E_D is still a relative/Hodge/projector contract, not a parent-owned reduced field bundle",
            "surviving_counterexample": "epsilon_shell could be a post-processed scalar A_D or fitted residual, not primitive ||a_D||",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PA609_1_proxy_identification",
            "required_object": "epsilon_shell = ||a_D||",
            "attempt": "map 7.432631961576971e-06 to primitive norm rather than norm-square or pressure scalar",
            "result": "not_derived",
            "why_not_claim": "current provenance only says compact-shell proxy; it does not specify amplitude level",
            "surviving_counterexample": "epsilon_shell=A_D=||a_D||^2 makes p=1 in epsilon notation physically p=2 in primitive amplitude",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PA609_2_parent_variation",
            "required_object": "a_D varied in S_parent before readout",
            "attempt": "treat a_D as parent source coordinate rather than runner/readout coefficient",
            "result": "conditional_no_cheat_rule",
            "why_not_claim": "readout-after-variation is still a contract from 574/575 lineage, not a full parent theorem",
            "surviving_counterexample": "post-readout EFT marker can generate linear source term after closure",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PA609_3_amplitude_verdict",
            "required_object": "parent-owned primitive amplitude",
            "attempt": "combine E_D, epsilon identification, and variation ownership",
            "result": "partial_not_parent_owned",
            "why_not_claim": "all three pieces are plausible but not signed together",
            "surviving_counterexample": "finite p=1 branch remains legal in the observable epsilon variable",
            "valid_for_claim": "false",
        },
    ]


def make_fibre_metric_rows() -> list[dict[str, str]]:
    return [
        {
            "metric_id": "FM609_0_relative_inner_product",
            "required_metric": "<a,b>_D from parent relative complex",
            "attempt": "use the relative-Hodge inner product from 601 as the fibre metric on E_D",
            "result": "formal_if_domain_exists",
            "why_not_claim": "601 left E_rel, boundary conditions, Green operator, and zero-mode routing not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "metric_id": "FM609_1_positive_definiteness",
            "required_metric": "positive norm ||a_D||^2",
            "attempt": "restrict to compact local collar with positive relative-memory source fibre",
            "result": "conditional",
            "why_not_claim": "projector/domain/zero-mode split can leave indefinite or gauge directions unless quotient is fully fixed",
            "valid_for_claim": "false",
        },
        {
            "metric_id": "FM609_2_OED_symmetry",
            "required_metric": "O(E_D) or sign symmetry of parent activation",
            "attempt": "declare parent activation depends on a_D only through ||a_D||^2",
            "result": "would_close_p2_if_parent_clause_accepted",
            "why_not_claim": "this is exactly the new parent clause; not derived from current action skeleton",
            "valid_for_claim": "false",
        },
        {
            "metric_id": "FM609_3_metric_verdict",
            "required_metric": "parent-owned fibre metric sufficient for norm-square activation",
            "attempt": "combine relative inner product, positivity, and O(E_D) symmetry",
            "result": "contract_written_not_derived",
            "why_not_claim": "metric exists as clean future action clause, not current theorem",
            "valid_for_claim": "false",
        },
    ]


def make_no_linear_rows() -> list[dict[str, str]]:
    return [
        {
            "symmetry_id": "NL609_0_fixed_spurion",
            "linear_marker": "fixed active covector ell in E_D*",
            "attempted_block": "strict quotient parent space excludes fixed non-orbit functions",
            "result": "conditional_pass_if_strict_quotient",
            "why_not_full": "407/413 still have parent quotient proof open",
            "p1_status": "not_from_fixed_spurion_if_quotient_signed",
            "valid_for_claim": "false",
        },
        {
            "symmetry_id": "NL609_1_material_marker",
            "linear_marker": "co-moving material/source/domain marker covector ell(m)",
            "attempted_block": "no-natural-marker theorem and invariant algebra triviality",
            "result": "fail_current_corpus",
            "why_not_full": "413, 573, and 574 keep material/domain/species marker generators legal",
            "p1_status": "p1_remains_legal",
            "valid_for_claim": "false",
        },
        {
            "symmetry_id": "NL609_2_domain_class_marker",
            "linear_marker": "relative/domain class scalar selecting sign/direction",
            "attempted_block": "local trivial relative class and parent domain selector",
            "result": "not_derived",
            "why_not_full": "physical domain selection and local class-zero theorem remain conditional",
            "p1_status": "p1_remains_legal",
            "valid_for_claim": "false",
        },
        {
            "symmetry_id": "NL609_3_readout_marker",
            "linear_marker": "post-readout EFT/source marker",
            "attempted_block": "readout is a map on solution space, not an argument of S_parent",
            "result": "conditional_no_cheat_rule",
            "why_not_full": "not fully formalized as parent-domain theorem",
            "p1_status": "p1_remains_legal_if_reduced_EFT_allowed",
            "valid_for_claim": "false",
        },
        {
            "symmetry_id": "NL609_4_no_linear_verdict",
            "linear_marker": "all linear covectors",
            "attempted_block": "O(E_D) invariant norm-square parent clause",
            "result": "closure_or_new_parent_clause_required",
            "why_not_full": "current corpus cannot derive O(E_D) from existing ingredients alone",
            "p1_status": "finite_p1_branch_retained",
            "valid_for_claim": "false",
        },
    ]


def make_local_flrw_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": "LF609_0_local",
            "branch": "stationary compact local domain",
            "needed_statement": "a_D=0 or epsilon_amp=0 by parent-selected local trivial relative class",
            "current_status": "conditional_only",
            "if_true": "p>=2 plus a_D=0 gives exact local source silence",
            "blocker": "domain selector/local trivial class remains theorem target",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "LF609_1_FLRW",
            "branch": "coherent FLRW domain",
            "needed_statement": "a_D != 0 or N_D != 0 with coherent expansion class",
            "current_status": "conditional_supported",
            "if_true": "cosmology branch survives while local branch silences",
            "blocker": "same selector must produce both branches, not hand-picked domains",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "LF609_2_no_overstrong_zero",
            "branch": "global all-domain zero closure",
            "needed_statement": "forbidden as unification route",
            "current_status": "guardrail",
            "if_true": "would kill FLRW/cosmology memory along with local residual",
            "blocker": "not allowed as a serious unified-field reduction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "LF609_3_verdict",
            "branch": "local/FLRW split",
            "needed_statement": "parent-owned norm-square activation plus branch selector",
            "current_status": "not_closed",
            "if_true": "would strongly support local GR reduction route",
            "blocker": "selector and amplitude ownership both remain conditional",
            "valid_for_claim": "false",
        },
    ]


def make_p_branch_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": "PB609_0_p2_normsquare",
            "candidate": "p=2 norm-square",
            "status": "conditional_theorem_target",
            "why": "mathematically strong if a_D, fibre metric, and no-linear-marker symmetry are parent-owned",
            "claim_action": "do_not_promote",
            "next_action": "write explicit parent clause or keep as labelled closure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "PB609_1_p3_determinant",
            "candidate": "p=3 det(Q_coh)",
            "status": "deferred_theorem_target",
            "why": "requires more ownership gates than p=2 and raw det(Q) is forbidden",
            "claim_action": "do_not_promote",
            "next_action": "defer unless Q_coh/domain route becomes parent-owned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "PB609_2_p1_finite",
            "candidate": "p=1 finite branch",
            "status": "legal_fallback",
            "why": "linear material/domain/readout marker covectors are still legal under current corpus",
            "claim_action": "retain_nonclaim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "branch_id": "PB609_3_verdict",
            "candidate": "p branch decision",
            "status": "p2_not_signed_p1_retained",
            "why": "parent ownership attempt sharpened the missing clause but did not derive it",
            "claim_action": "no_R10_or_local_GR_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_finite_p1_rows() -> list[dict[str, str]]:
    return [
        {
            "ledger_id": "FP609_0_alpha_law",
            "object": "finite p=1 alpha law",
            "formula": "alpha_X=lambda branch = epsilon_shell C_X(lambda_X)",
            "required_inputs": "C_X(lambda_X), lambda_X, sign, source/test projections, claim-grade bound curve",
            "current_status": "symbolic_nonclaim",
            "why_retained": "linear marker covector is not eliminated",
            "valid_for_claim": "false",
        },
        {
            "ledger_id": "FP609_1_pressure_read",
            "object": "p=1 pressure",
            "formula": f"epsilon_shell={EPSILON_SHELL:.12e}; alpha~7.4e-6*C_X",
            "required_inputs": "real alpha_bound(lambda), not anchors only",
            "current_status": "private_pressure_only",
            "why_retained": "order-one C_X is not immediately absurd at anchor-only pressure, but this is not evidence",
            "valid_for_claim": "false",
        },
        {
            "ledger_id": "FP609_2_local_GR_warning",
            "object": "finite p=1 interpretation",
            "formula": "finite small R10 residual != local GR reduction",
            "required_inputs": "PPN/WEP/measured-GM/source-normalization gates",
            "current_status": "guardrail",
            "why_retained": "even a future R10 numerical survival cannot alone prove GR recovery",
            "valid_for_claim": "false",
        },
    ]


def make_mts_template_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    anchors = read_csv(ANCHOR_BOUND)
    for anchor in anchors:
        for branch_id, expression, note in [
            ("R10_p2_normsquare_closure_template", "(epsilon_amp**2)*C_X(lambda_X)", "conditional p=2 closure/theorem target"),
            ("R10_p1_finite_retained_template", "epsilon_shell*C_X(lambda_X)", "legal finite p=1 fallback"),
        ]:
            rows.append(
                {
                    "model_id": "MTS_p_branch_609",
                    "branch_id": branch_id,
                    "curve_id": "R10_alpha_lambda_curve_MTS_P_BRANCH_609_TEMPLATE",
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", "m"),
                    "alpha_predicted": expression,
                    "alpha_bound": anchor.get("alpha_bound", "1.0"),
                    "alpha_bound_source": f"source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::{anchor.get('bound_id', '')}",
                    "force_law_form": "Yukawa_potential_alpha",
                    "derivation_status": "symbolic_p_branch_nonclaim",
                    "formula_reference": "609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md::PB609",
                    "source_file": "609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md",
                    "assumptions": "MISSING_C_X;MISSING_PARENT_OWNERSHIP_OR_VALID_P1_COEFFICIENTS;anchor_bound_only",
                    "valid_for_claim": "false",
                    "notes": f"Template row only: {note}; runner must reject until numeric parent inputs and real bound curve exist.",
                }
            )
    return rows


def make_runner_summary(run_result: dict[str, Any]) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_609_P_BRANCH_TEMPLATE_RECHECK",
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
            "notes": "required blocked result: p branch templates remain symbolic and anchor bounds are nonclaim",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D609_0_normsquare_attempt",
            "status": "partial_not_parent_owned",
            "decision": "do not promote p=2 as parent-owned",
            "meaning": "the needed O(E_D)/norm-square clause is clear but not derived from current parent skeleton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D609_1_p1_retained",
            "status": "legal_fallback",
            "decision": "retain finite p=1 branch",
            "meaning": "material/domain/readout marker covectors remain legal counterexamples",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D609_2_best_next",
            "status": "finite_or_repair_fork",
            "decision": "either write an explicit parent norm-square closure clause or start finite p=1 coefficient envelope",
            "meaning": "derivation-first was attempted; the missing axiom is now named exactly",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D609_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "p branch and C_X remain nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU609_0_repair_route",
            "allowed_after_609": "write explicit parent O(E_D) norm-square clause and label it as closure unless derived",
            "forbidden_after_609": "pretend current corpus derives marker exclusion",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU609_1_finite_route",
            "allowed_after_609": "prepare finite p=1 coefficient envelope for R10 scoring",
            "forbidden_after_609": "call finite p=1 survival a local-GR theorem",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU609_2_determinant_route",
            "allowed_after_609": "keep p=3 determinant route as deferred theorem target",
            "forbidden_after_609": "use raw det(Q) or skip Q_coh/domain ownership",
            "next_action": "defer behind p=1 envelope or explicit closure decision",
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": f"{EPSILON_SHELL:.15g}",
            "p2_parent_owned": "false",
            "p1_branch_legal": "true",
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
    amplitude_rows: list[dict[str, str]],
    metric_rows: list[dict[str, str]],
    no_linear_rows: list[dict[str, str]],
    local_flrw_rows: list[dict[str, str]],
    p_branch_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_608_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    p2_verdict = [row for row in p_branch_rows if row["candidate"] == "p=2 norm-square"]
    p1_verdict = [row for row in p_branch_rows if row["candidate"] == "p=1 finite branch"]
    marker_fail = [row for row in no_linear_rows if row["result"] == "fail_current_corpus"]
    template_symbolic = all(parse_float(row.get("alpha_predicted", "")) is None for row in mts_rows)
    template_nonclaim = all(row.get("valid_for_claim") == "false" for row in mts_rows)
    runner = runner_rows[0]
    claim_rows = count_claim_rows(
        [
            amplitude_rows,
            metric_rows,
            no_linear_rows,
            local_flrw_rows,
            p_branch_rows,
            finite_rows,
            mts_rows,
            decision_rows,
            summary_rows,
        ]
    )
    return [
        {
            "check_id": "V609_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V609_1_prior_608_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V609_2_amplitude_not_parent_owned",
            "result": "pass" if amplitude_rows[-1]["result"] == "partial_not_parent_owned" else "fail",
            "detail": amplitude_rows[-1]["surviving_counterexample"],
        },
        {
            "check_id": "V609_3_fibre_metric_contract_only",
            "result": "pass" if metric_rows[-1]["result"] == "contract_written_not_derived" else "fail",
            "detail": metric_rows[-1]["why_not_claim"],
        },
        {
            "check_id": "V609_4_no_linear_marker_not_closed",
            "result": "pass" if marker_fail and no_linear_rows[-1]["p1_status"] == "finite_p1_branch_retained" else "fail",
            "detail": f"marker_fail_rows={len(marker_fail)};verdict={no_linear_rows[-1]['result']}",
        },
        {
            "check_id": "V609_5_p2_not_promoted_p1_retained",
            "result": "pass"
            if p2_verdict and p2_verdict[0]["claim_action"] == "do_not_promote" and p1_verdict and p1_verdict[0]["status"] == "legal_fallback"
            else "fail",
            "detail": f"p2={p2_verdict[0]['status'] if p2_verdict else 'missing'};p1={p1_verdict[0]['status'] if p1_verdict else 'missing'}",
        },
        {
            "check_id": "V609_6_finite_p1_ledger_written",
            "result": "pass" if len(finite_rows) >= 3 and all(row["valid_for_claim"] == "false" for row in finite_rows) else "fail",
            "detail": f"finite_rows={len(finite_rows)}",
        },
        {
            "check_id": "V609_7_template_symbolic_nonclaim",
            "result": "pass" if mts_rows and template_symbolic and template_nonclaim else "fail",
            "detail": f"template_rows={len(mts_rows)};symbolic={template_symbolic};nonclaim={template_nonclaim}",
        },
        {
            "check_id": "V609_8_runner_blocks_template",
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
            "check_id": "V609_9_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V609_10_no_R10_or_local_GR_claim",
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
    amplitude_rows: list[dict[str, str]],
    metric_rows: list[dict[str, str]],
    no_linear_rows: list[dict[str, str]],
    local_flrw_rows: list[dict[str, str]],
    p_branch_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 609 Y5 R10 parent-own norm-square activation or finite p1 branch

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- I tried to parent-own the norm-square route rather than just admire it.
- Result: `p=2` remains the clean theorem target, but current corpus does not derive the required parent-owned primitive amplitude, fibre metric, and no-linear-marker symmetry.
- The killer counterexample is still a material/domain/readout marker covector `ell(a_D)`, which makes a linear source term legal and keeps `p=1` alive.
- So the finite `p=1` branch must remain as a non-claim fallback unless we explicitly add a parent `O(E_D)` norm-square clause as labelled closure.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Primitive Amplitude Ownership
{markdown_table(amplitude_rows, ["gate_id", "required_object", "attempt", "result", "why_not_claim", "surviving_counterexample", "valid_for_claim"])}

## Fibre Metric Ownership
{markdown_table(metric_rows, ["metric_id", "required_metric", "attempt", "result", "why_not_claim", "valid_for_claim"])}

## No-Linear Marker Symmetry Gate
{markdown_table(no_linear_rows, ["symmetry_id", "linear_marker", "attempted_block", "result", "why_not_full", "p1_status", "valid_for_claim"])}

## Local-FLRW Branch Split Gate
{markdown_table(local_flrw_rows, ["branch_id", "branch", "needed_statement", "current_status", "if_true", "blocker", "valid_for_claim"])}

## P-Branch Decision
{markdown_table(p_branch_rows, ["branch_id", "candidate", "status", "why", "claim_action", "next_action", "valid_for_claim"])}

## Finite P1 Branch Ledger
{markdown_table(finite_rows, ["ledger_id", "object", "formula", "required_inputs", "current_status", "why_retained", "valid_for_claim"])}

## MTS P-Branch Template
{markdown_table(mts_rows, MTS_TEMPLATE_FIELDS)}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_609", "forbidden_after_609", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is not the answer we wanted, but it is the answer that keeps the theory honest. The `p=2` route is still beautiful and worth keeping as a theorem target, but without a parent no-marker/O(E_D) clause, a linear marker can walk back in through the side door. That means the next practical move is either: write that parent clause openly as closure, or start the finite `p=1` coefficient envelope and see whether it survives R10 without pretending it is derived local GR.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"

    sources = make_sources()
    amplitude_rows = make_amplitude_rows()
    metric_rows = make_fibre_metric_rows()
    no_linear_rows = make_no_linear_rows()
    local_flrw_rows = make_local_flrw_rows()
    p_branch_rows = make_p_branch_rows()
    finite_rows = make_finite_p1_rows()
    mts_rows = make_mts_template_rows()

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(AMPLITUDE_PATH, amplitude_rows, ["gate_id", "required_object", "attempt", "result", "why_not_claim", "surviving_counterexample", "valid_for_claim"])
    write_csv(FIBRE_METRIC_PATH, metric_rows, ["metric_id", "required_metric", "attempt", "result", "why_not_claim", "valid_for_claim"])
    write_csv(NO_LINEAR_PATH, no_linear_rows, ["symmetry_id", "linear_marker", "attempted_block", "result", "why_not_full", "p1_status", "valid_for_claim"])
    write_csv(LOCAL_FLRW_PATH, local_flrw_rows, ["branch_id", "branch", "needed_statement", "current_status", "if_true", "blocker", "valid_for_claim"])
    write_csv(P_BRANCH_PATH, p_branch_rows, ["branch_id", "candidate", "status", "why", "claim_action", "next_action", "valid_for_claim"])
    write_csv(FINITE_P1_PATH, finite_rows, ["ledger_id", "object", "formula", "required_inputs", "current_status", "why_retained", "valid_for_claim"])
    write_csv(MTS_TEMPLATE_PATH, mts_rows, MTS_TEMPLATE_FIELDS)

    runner_result = run_runner(MTS_TEMPLATE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result)
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation_rows(
        sources,
        amplitude_rows,
        metric_rows,
        no_linear_rows,
        local_flrw_rows,
        p_branch_rows,
        finite_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_609", "forbidden_after_609", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "epsilon_shell", "p2_parent_owned", "p1_branch_legal", "finite_p1_numeric", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_doc(
        generated,
        run_root,
        sources,
        amplitude_rows,
        metric_rows,
        no_linear_rows,
        local_flrw_rows,
        p_branch_rows,
        finite_rows,
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
