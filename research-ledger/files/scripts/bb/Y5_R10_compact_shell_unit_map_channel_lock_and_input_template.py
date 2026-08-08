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

SLUG = "Y5-R10-compact-shell-unit-map-channel-lock-and-input-template"
DOC_PATH = ROOT / "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_606_SOURCE_REGISTER.csv"
CHANNEL_LOCK_PATH = RESIDUALS / "P8_Y5_R10_606_UNIT_MAP_CHANNEL_LOCK.csv"
ALPHA_LAW_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_606_COMPACT_SHELL_ALPHA_LAW_CONTRACT.csv"
PARENT_INPUT_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_606_PARENT_INPUT_REQUIREMENTS.csv"
MTS_TEMPLATE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_COMPACT_SHELL_UNIT_MAP_TEMPLATE.csv"
BOUND_STATUS_PATH = RESIDUALS / "P8_Y5_R10_606_BOUND_INPUT_STATUS.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_606_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_606_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_606_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_606_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_606_VALIDATION.csv"

PRIOR_605_VALIDATION = RESIDUALS / "P8_Y5_BRR545_605_VALIDATION.csv"
PRIOR_605_CHANNEL = RESIDUALS / "P8_Y5_R10_605_UNIT_MAP_CHANNEL_DECISION.csv"
PRIOR_601_SPEC = RESIDUALS / "P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
LIVE_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
LIVE_MTS = RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv"

STATUS = "Y5_R10_compact_shell_R10_unit_map_locked_input_template_written_claim_blocked"
CLAIM_CEILING = "unit_map_template_and_runner_block_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md", "immediate 605 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_605_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_605_UNIT_MAP_CHANNEL_DECISION.csv", "R10 channel recommendation"),
    ("601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md", "first compact-shell unit-map contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv", "compact-shell proxy and claim gate"),
    ("563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md", "R10 anchor/smoke runner checkpoint"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "source-backed anchor-only non-claim bound rows"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "live claim bound placeholder kept unchanged"),
    ("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv", "live MTS placeholder kept unchanged"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "review-candidate vector curve not promoted"),
    ("559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md", "runner lineage"),
    ("562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md", "lambda and prefactor lineage"),
    ("578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md", "mass-gap/product coefficient target"),
    ("579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md", "parent Hessian/source charge attempt"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_compact_shell_unit_map_channel_lock_and_input_template.py", "this checkpoint generator"),
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


def make_channel_lock_rows() -> list[dict[str, str]]:
    return [
        {
            "channel_id": "UML606_0_R10_alpha_lambda",
            "candidate_channel": "R10 alpha(lambda)",
            "selection": "locked_first_nonclaim_channel",
            "why_selected": "existing runner, source-backed anchor rows, and clear Yukawa alpha convention make this the least ambiguous first unit map",
            "what_is_being_mapped": "compact_shell_proxy_epsilon -> Yukawa alpha_X(lambda_X)",
            "still_forbidden": "treating epsilon_shell itself as alpha without parent coefficient, sign, lambda, and source projection",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UML606_1_PPN_vector",
            "candidate_channel": "PPN residual vector",
            "selection": "deferred",
            "why_selected": "not selected because gamma/beta/preferred-frame/Gdot rows require several more local-GR components",
            "what_is_being_mapped": "compact_shell_proxy_epsilon -> PPN vector",
            "still_forbidden": "using R10 silence as a PPN/local-GR pass",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UML606_2_WEP_source",
            "candidate_channel": "WEP/Eotvos source channel",
            "selection": "deferred",
            "why_selected": "not selected because constant-sector/source-current universality is still open",
            "what_is_being_mapped": "compact_shell_proxy_epsilon -> species/source-dependent acceleration contrast",
            "still_forbidden": "claiming composition universality from a single compact-shell scalar",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UML606_3_clock",
            "candidate_channel": "clock/redshift/fine-structure",
            "selection": "deferred",
            "why_selected": "not selected because no parent coupling to spectral constants has been derived",
            "what_is_being_mapped": "compact_shell_proxy_epsilon -> delta_nu/nu or delta_alpha_EM/alpha_EM",
            "still_forbidden": "turning a gravitational residual into an EM/clock signal by naming only",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "UML606_4_score_policy",
            "candidate_channel": "R10 scoring policy",
            "selection": "claim_gate_closed",
            "why_selected": "channel may be scaffolded only as non-claim until numeric parent coefficients and valid bound curve rows exist",
            "what_is_being_mapped": "template rows and runner failure modes",
            "still_forbidden": "promoting anchor-only or symbolic rows to evidence",
            "valid_for_claim": "false",
        },
    ]


def make_alpha_law_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "law_id": "AL606_0_force_convention",
            "object": "R10 Yukawa convention",
            "contract": "V(r)=-G_obs m1 m2/r * [1 + alpha_X exp(-r/lambda_X)]",
            "needed_for_claim": "state whether alpha_X is the potential alpha used by the bound curve or a force-ratio proxy",
            "current_status": "potential_alpha_convention_selected",
            "claim_status": "nonclaim_convention_only",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_1_compact_shell_proxy",
            "object": "epsilon_shell",
            "contract": f"epsilon_shell={COMPACT_SHELL_PROXY} is dimensionless internal compact-shell pressure/residual proxy",
            "needed_for_claim": "derive why epsilon_shell sources the same scalar/vector mode constrained by R10",
            "current_status": "proxy_recorded_not_observable",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_2_lambda_map",
            "object": "lambda_X",
            "contract": "lambda_X=sqrt(Z_X/M_X^2) after parent units are fixed, or equivalent source-backed mass-gap length",
            "needed_for_claim": "positive numeric lambda in metres with source path and uncertainty/range",
            "current_status": "symbolic",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_3_alpha_map",
            "object": "alpha_X(lambda_X)",
            "contract": "alpha_X = sigma_X * epsilon_shell * K_X * Qbar_source_X * qbar_test_X / (4*pi*Z_X*G_obs)",
            "needed_for_claim": "numeric sigma_X, K_X, source/test projections, Z_X, and G_obs normalization in consistent units",
            "current_status": "factorized_template_only",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_4_sign_rule",
            "object": "sigma_X",
            "contract": "sigma_X must come from the parent Hessian/source-charge sign, not from fitting the bound",
            "needed_for_claim": "derive sign before any alpha comparison; runner uses abs(alpha) only after sign exists",
            "current_status": "missing",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_5_source_profile",
            "object": "profile and source projection",
            "contract": "compact-shell residual must project onto the laboratory source/test configuration, not only a cosmological or abstract domain",
            "needed_for_claim": "composition/source map and geometry/profile integral for the R10 apparatus class",
            "current_status": "missing",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "AL606_6_acceptance_gate",
            "object": "claim promotion",
            "contract": "valid MTS row + valid full bound curve + abs(alpha_predicted)<=alpha_bound + no edge-only dependence",
            "needed_for_claim": "all generated rows must have no missing markers, positive units, source files, and valid_for_claim=true",
            "current_status": "gate_written_closed",
            "claim_status": "no_claim",
            "valid_for_claim": "false",
        },
    ]


def make_parent_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "PRI606_0_lambda_X",
            "required_input": "lambda_X",
            "required_type": "positive numeric metres",
            "parent_source_needed": "mass-gap/Hessian eigenvalue M_X^2 and kinetic normalization Z_X",
            "why_it_matters": "R10 bounds are alpha(lambda); without lambda there is no comparable point",
            "template_value": "3.86e-5 and 5.6e-5 anchor-aligned placeholders only",
            "current_status": "template_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_1_epsilon_shell",
            "required_input": "epsilon_shell",
            "required_type": "dimensionless proxy with provenance",
            "parent_source_needed": "compact-shell residual derivation and domain/projection ownership",
            "why_it_matters": "epsilon_shell may be a proxy, not an observable charge by itself",
            "template_value": COMPACT_SHELL_PROXY,
            "current_status": "available_as_proxy_only",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_2_KX_over_ZX",
            "required_input": "K_X/(4*pi*Z_X*G_obs)",
            "required_type": "numeric dimensionless normalization after unit reduction",
            "parent_source_needed": "quadratic parent action, field normalization, and Newtonian matching",
            "why_it_matters": "this is the main conversion from proxy amplitude to Yukawa alpha",
            "template_value": "MISSING_PARENT_NORMALIZATION",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_3_source_projection",
            "required_input": "Qbar_source_X",
            "required_type": "numeric source charge per gravitational mass or equivalent normalized projection",
            "parent_source_needed": "matter/source pullback and composition map",
            "why_it_matters": "R10 source/test masses are ordinary matter, not abstract cells",
            "template_value": "MISSING_SOURCE_PROJECTION",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_4_test_projection",
            "required_input": "qbar_test_X",
            "required_type": "numeric test charge per gravitational mass or equivalent normalized projection",
            "parent_source_needed": "test-body coupling and WEP/source universality branch",
            "why_it_matters": "alpha depends on both source and test coupling",
            "template_value": "MISSING_TEST_PROJECTION",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_5_sign",
            "required_input": "sigma_X",
            "required_type": "+1 or -1 from parent sign convention",
            "parent_source_needed": "Hessian/source-charge sign derivation",
            "why_it_matters": "sign decides attraction/repulsion even though bounds compare absolute strength",
            "template_value": "MISSING_PARENT_SIGN",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PRI606_6_bound_curve",
            "required_input": "alpha_bound(lambda)",
            "required_type": "dense positive numeric full curve with provenance",
            "parent_source_needed": "not a parent input; external R10 evidence input",
            "why_it_matters": "anchor-only rows cannot support an alpha(lambda) claim",
            "template_value": "anchor-only nonclaim rows available",
            "current_status": "bound_curve_missing",
            "valid_for_claim": "false",
        },
    ]


def make_mts_template_rows() -> list[dict[str, str]]:
    formula = "sigma_X*epsilon_shell*K_X*Qbar_source_X*qbar_test_X/(4*pi*Z_X*G_obs)"
    assumptions = (
        f"epsilon_shell={COMPACT_SHELL_PROXY}; "
        "MISSING_PARENT_NORMALIZATION;MISSING_PARENT_SIGN;MISSING_SOURCE_PROJECTION;MISSING_TEST_PROJECTION;bound_anchor_only"
    )
    return [
        {
            "model_id": "MTS_compact_shell_unit_map",
            "branch_id": "R10_compact_shell_symbolic_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_COMPACT_SHELL_UNIT_MAP_TEMPLATE",
            "lambda_value": "3.86e-5",
            "lambda_units": "m",
            "alpha_predicted": formula,
            "alpha_bound": "1.0",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            "force_law_form": "Yukawa_potential_alpha",
            "derivation_status": "compact_shell_unit_map_template_symbolic_nonclaim",
            "formula_reference": "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md::AL606_3_alpha_map",
            "source_file": "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md",
            "assumptions": assumptions,
            "valid_for_claim": "false",
            "notes": "Anchor-aligned template row only; alpha is symbolic and must remain invalid until parent coefficients are numeric and sourced.",
        },
        {
            "model_id": "MTS_compact_shell_unit_map",
            "branch_id": "R10_compact_shell_symbolic_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_COMPACT_SHELL_UNIT_MAP_TEMPLATE",
            "lambda_value": "5.6e-5",
            "lambda_units": "m",
            "alpha_predicted": formula,
            "alpha_bound": "1.0",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM",
            "force_law_form": "Yukawa_potential_alpha",
            "derivation_status": "compact_shell_unit_map_template_symbolic_nonclaim",
            "formula_reference": "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md::AL606_3_alpha_map",
            "source_file": "606-Y5-R10-compact-shell-unit-map-channel-lock-and-input-template.md",
            "assumptions": assumptions,
            "valid_for_claim": "false",
            "notes": "Continuity-anchor template row only; not a physical prediction or claim row.",
        },
    ]


def make_bound_status_rows() -> list[dict[str, str]]:
    anchor_rows = read_csv(ANCHOR_BOUND)
    live_rows = read_csv(LIVE_BOUND)
    vector_candidate = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
    return [
        {
            "bound_file": rel(ANCHOR_BOUND),
            "rows": str(len(anchor_rows)),
            "claim_status": "anchor_only_nonclaim",
            "valid_rows_for_runner": str(sum(1 for row in anchor_rows if is_true(row.get("valid_for_claim", "")))),
            "use_in_606": "schema_and_failure_mode_smoke",
            "promotion_requirement": "full digitized/source-backed curve rows with valid_for_claim=true",
        },
        {
            "bound_file": rel(LIVE_BOUND),
            "rows": str(len(live_rows)),
            "claim_status": "live_placeholder_blocked",
            "valid_rows_for_runner": str(sum(1 for row in live_rows if is_true(row.get("valid_for_claim", "")))),
            "use_in_606": "kept_unchanged",
            "promotion_requirement": "replace placeholders only after real digitization/provenance QA",
        },
        {
            "bound_file": rel(vector_candidate),
            "rows": str(len(read_csv(vector_candidate))),
            "claim_status": "review_candidate_not_promoted",
            "valid_rows_for_runner": "0",
            "use_in_606": "not_used_for_claim",
            "promotion_requirement": "axis calibration, curve identity, independent QA, source provenance",
        },
    ]


def make_runner_summary(run_result: dict[str, Any], run_id: str) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": run_id,
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
            "notes": "required blocked result: symbolic MTS alpha rows and anchor-only bound rows are not claim-valid",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D606_0_checkpoint_status",
            "status": STATUS,
            "decision": "lock R10 alpha(lambda) as the first compact-shell unit-map channel",
            "rationale": "Q_sec/PMTS route is demoted, so the safest next branch is a transparent non-claim unit map with an existing comparator",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D606_1_alpha_law",
            "status": "factorized_template_only",
            "decision": "use alpha_X=sigma_X epsilon_shell K_X Qbar_source_X qbar_test_X/(4*pi Z_X G_obs) as the input contract",
            "rationale": "this isolates exactly which parent coefficients must be derived before scoring",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D606_2_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "do not claim R10, WEP, PPN, or local-GR success",
            "rationale": "lambda, normalization, sign, source/test projections, and full bound curve are not all real",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU606_0_theory_route",
            "allowed_after_606": "derive the parent factorization pieces in AL606_3 and PRI606 rows",
            "forbidden_after_606": "score epsilon_shell directly as alpha",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU606_1_data_route",
            "allowed_after_606": "digitize or source a real R10 alpha(lambda) bound curve",
            "forbidden_after_606": "promote anchor-only threshold rows to a full curve",
            "next_action": "keep separate from parent-coefficient derivation unless needed for runner QA",
        },
        {
            "route_id": "RU606_2_local_GR_route",
            "allowed_after_606": "later compare PPN/WEP through the same no-one-sided-baseline policy",
            "forbidden_after_606": "infer local GR recovery from a blocked R10 unit-map scaffold",
            "next_action": "return only after R10 coefficients or theorem-zero branch are clearer",
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "compact_shell_proxy": COMPACT_SHELL_PROXY,
            "channel_locked": "R10_alpha_lambda_nonclaim",
            "runner_claim_allowed": "false",
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
    channel_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_template_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    runner_summary: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_605_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    selected = [row for row in channel_rows if row["selection"] == "locked_first_nonclaim_channel"]
    template_symbolic = all(parse_float(row.get("alpha_predicted", "")) is None for row in mts_template_rows)
    template_nonclaim = all(not is_true(row.get("valid_for_claim", "")) for row in mts_template_rows)
    template_sources_exist = all(
        (ROOT / row["source_file"]).exists() or row["source_file"] == DOC_PATH.name
        for row in mts_template_rows
    )
    anchor_valid_rows = 0
    if ANCHOR_BOUND.exists():
        anchor_valid_rows = sum(1 for row in read_csv(ANCHOR_BOUND) if is_true(row.get("valid_for_claim", "")))
    runner = runner_summary[0]
    claim_rows = count_claim_rows(
        [
            channel_rows,
            alpha_rows,
            parent_rows,
            mts_template_rows,
            decision_rows,
            summary_rows,
        ]
    )
    live_mts_rows = read_csv(LIVE_MTS)
    live_bound_rows = read_csv(LIVE_BOUND)
    validations = [
        {
            "check_id": "V606_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V606_1_prior_605_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V606_2_R10_channel_locked_nonclaim",
            "result": "pass" if len(selected) == 1 and selected[0]["valid_for_claim"] == "false" else "fail",
            "detail": f"selected={len(selected)};channel={selected[0]['candidate_channel'] if selected else 'none'}",
        },
        {
            "check_id": "V606_3_alpha_law_factorized_not_scored",
            "result": "pass" if len(alpha_rows) >= 6 and all(row["valid_for_claim"] == "false" for row in alpha_rows) else "fail",
            "detail": f"law_rows={len(alpha_rows)};proxy={COMPACT_SHELL_PROXY};claim_rows={count_claim_rows([alpha_rows])}",
        },
        {
            "check_id": "V606_4_input_template_symbolic_nonclaim",
            "result": "pass" if len(mts_template_rows) == 2 and template_symbolic and template_nonclaim and template_sources_exist else "fail",
            "detail": (
                f"template_rows={len(mts_template_rows)};"
                f"symbolic_alpha={template_symbolic};nonclaim={template_nonclaim};sources_exist={template_sources_exist}"
            ),
        },
        {
            "check_id": "V606_5_bound_inputs_nonclaim",
            "result": "pass" if bound_rows and anchor_valid_rows == 0 else "fail",
            "detail": f"bound_status_rows={len(bound_rows)};anchor_valid_rows={anchor_valid_rows}",
        },
        {
            "check_id": "V606_6_runner_blocks_template",
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
            "check_id": "V606_7_live_files_not_overwritten",
            "result": "pass" if len(live_mts_rows) == 2 and len(live_bound_rows) == 2 else "fail",
            "detail": f"live_mts_rows={len(live_mts_rows)};live_bound_rows={len(live_bound_rows)}",
        },
        {
            "check_id": "V606_8_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V606_9_no_R10_or_local_GR_claim",
            "result": "pass"
            if summary_rows[0]["R10_pass"] == "false"
            and summary_rows[0]["WEP_pass"] == "false"
            and summary_rows[0]["PPN_pass"] == "false"
            and summary_rows[0]["local_GR_pass"] == "false"
            else "fail",
            "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]
    return validations


def write_doc(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_template_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 606 Y5 R10 compact-shell unit-map channel lock and input template

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The compact-shell proxy is now routed into exactly one first observable channel: `R10 alpha(lambda)`.
- The locked law is a factorized input contract, not a prediction: `alpha_X = sigma_X epsilon_shell K_X Qbar_source_X qbar_test_X/(4*pi Z_X G_obs)`.
- The runner template deliberately fails claim validation because `alpha_X`, `lambda_X`, sign, source/test projections, and the full bound curve are not all real.
- This is the right discipline: we have made the next missing derivation visible instead of hiding it inside a projector or a fitted number.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Unit-Map Channel Lock
{markdown_table(channel_rows, ["channel_id", "candidate_channel", "selection", "why_selected", "what_is_being_mapped", "still_forbidden", "valid_for_claim"])}

## Compact-Shell Alpha Law Contract
{markdown_table(alpha_rows, ["law_id", "object", "contract", "needed_for_claim", "current_status", "claim_status", "valid_for_claim"])}

## Parent Input Requirements
{markdown_table(parent_rows, ["input_id", "required_input", "required_type", "parent_source_needed", "why_it_matters", "template_value", "current_status", "valid_for_claim"])}

## MTS Input Template
{markdown_table(mts_template_rows, MTS_TEMPLATE_FIELDS)}

## Bound Input Status
{markdown_table(bound_rows, ["bound_file", "rows", "claim_status", "valid_rows_for_runner", "use_in_606", "promotion_requirement"])}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "rationale", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_606", "forbidden_after_606", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a useful narrowing without becoming "just a galaxy/rotation thing". We are not saying the local branch passes; we are giving the compact-shell residual a clean laboratory-language doorway. The next punch is to derive or kill the coefficient product in `AL606_3`. If it derives naturally and lands small enough, R10 becomes a serious local-bound pillar. If it refuses to derive, the route gets demoted cleanly before it wastes us.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"
    sources = make_sources()
    channel_rows = make_channel_lock_rows()
    alpha_rows = make_alpha_law_contract_rows()
    parent_rows = make_parent_requirement_rows()
    mts_template_rows = make_mts_template_rows()
    bound_rows = make_bound_status_rows()
    summary_rows = make_summary_rows()

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(CHANNEL_LOCK_PATH, channel_rows, ["channel_id", "candidate_channel", "selection", "why_selected", "what_is_being_mapped", "still_forbidden", "valid_for_claim"])
    write_csv(ALPHA_LAW_CONTRACT_PATH, alpha_rows, ["law_id", "object", "contract", "needed_for_claim", "current_status", "claim_status", "valid_for_claim"])
    write_csv(PARENT_INPUT_REQUIREMENTS_PATH, parent_rows, ["input_id", "required_input", "required_type", "parent_source_needed", "why_it_matters", "template_value", "current_status", "valid_for_claim"])
    write_csv(MTS_TEMPLATE_PATH, mts_template_rows, MTS_TEMPLATE_FIELDS)
    write_csv(BOUND_STATUS_PATH, bound_rows, ["bound_file", "rows", "claim_status", "valid_rows_for_runner", "use_in_606", "promotion_requirement"])

    runner_result = run_runner(MTS_TEMPLATE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result, "R10_RUNNER_606_COMPACT_SHELL_TEMPLATE_RECHECK")
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    validation_rows = make_validation_rows(
        sources,
        channel_rows,
        alpha_rows,
        parent_rows,
        mts_template_rows,
        bound_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "rationale", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_606", "forbidden_after_606", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "compact_shell_proxy", "channel_locked", "runner_claim_allowed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_doc(
        generated,
        run_root,
        sources,
        channel_rows,
        alpha_rows,
        parent_rows,
        mts_template_rows,
        bound_rows,
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
        "template": rel(MTS_TEMPLATE_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_status": rel(result_dir / "R10_runner_status.json"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
