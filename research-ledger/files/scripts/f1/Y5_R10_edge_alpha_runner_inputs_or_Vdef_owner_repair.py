from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "585-Y5-R10-edge-alpha-runner-inputs-or-Vdef-owner-repair.md"
RUNNER = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"

PRIOR_584_VALIDATION = RESIDUALS / "P8_Y5_BRR545_584_VALIDATION.csv"
PRIOR_584_SUMMARY = RESIDUALS / "P8_Y5_R10_584_NONCLAIM_SUMMARY.csv"
EDGE_LAW_584 = RESIDUALS / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv"
PRESSURE_584 = RESIDUALS / "P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv"
CLAIM_CONTRACT_584 = RESIDUALS / "P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv"
OWNER_REPAIR_584 = RESIDUALS / "P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv"
LIVE_CLAIM_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_585_SOURCE_REGISTER.csv"
RUNNER_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_585_EDGE_RUNNER_INPUT_SCHEMA.csv"
EDGE_SMOKE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_edge_residual_smoke.csv"
RUNNER_STATUS_PATH = RESIDUALS / "P8_Y5_R10_585_RUNNER_STATUS_SUMMARY.csv"
VDEF_REPAIR_PATH = RESIDUALS / "P8_Y5_R10_585_VDEF_OWNER_REPAIR_PASS.csv"
CLAIM_BLOCKERS_PATH = RESIDUALS / "P8_Y5_R10_585_EDGE_CLAIM_BLOCKER_LEDGER.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_585_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_585_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_585_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_585_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_edge_alpha_runner_inputs_written_runner_blocks_nonclaim_rows_Vdef_owner_repair_open"
CLAIM_CEILING = "edge_runner_input_smoke_and_Vdef_repair_contract_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md"

MTS_REQUIRED_COLUMNS = [
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

SOURCE_FILES = [
    {
        "source_file": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
        "role": "immediate edge-envelope handoff",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_584_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_NONCLAIM_SUMMARY.csv",
        "role": "prior nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
        "role": "edge alpha law",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv",
        "role": "private review-candidate pressure matrix",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
        "role": "missing input contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
        "role": "owner repair options",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live claim curve placeholder",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
        "role": "private review candidate curve",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "existing R10 comparator",
    },
    {
        "source_file": "scripts/Y5_R10_edge_alpha_runner_inputs_or_Vdef_owner_repair.py",
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


def make_runner_schema() -> list[dict[str, object]]:
    return [
        {
            "column": column,
            "purpose": {
                "model_id": "names the theory branch",
                "branch_id": "names the residual/zero route",
                "curve_id": "groups rows into a sampled alpha(lambda) curve",
                "lambda_value": "edge support/range ordinate",
                "lambda_units": "units convertible to meters",
                "alpha_predicted": "numeric alpha for runner validation; symbolic rows must stay nonclaim",
                "alpha_bound": "optional row-level bound annotation; runner interpolates external bound file",
                "alpha_bound_source": "bound provenance",
                "force_law_form": "Yukawa/edge/envelope form",
                "derivation_status": "must distinguish source-backed from smoke/template",
                "formula_reference": "checkpoint formula source",
                "source_file": "local source for coefficients",
                "assumptions": "same-frame and no-double-count assumptions",
                "valid_for_claim": "must be true only after all inputs are numeric/source-backed",
                "notes": "blockers and provenance caveats",
            }.get(column, ""),
            "edge_branch_status": "required",
        }
        for column in MTS_REQUIRED_COLUMNS
    ]


def make_edge_smoke_rows() -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke",
            "branch_id": "edge_only_residual_smoke",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke",
            "lambda_value": "6.080783e-04",
            "lambda_units": "m",
            "alpha_predicted": "0.001",
            "alpha_bound": "0.00234471960478",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv::private_review_candidate",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "numeric_smoke_placeholder_not_source_backed",
            "formula_reference": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "assumptions": "K_edge*Qbar_edge_XH*qbar_XT inserted for schema smoke only; no parent coefficients",
            "valid_for_claim": "false",
            "notes": "nonclaim smoke row below private review candidate ceiling; must remain invalid until coefficients are source-backed",
        },
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke",
            "branch_id": "edge_only_residual_smoke",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke",
            "lambda_value": "1.000000e-04",
            "lambda_units": "m",
            "alpha_predicted": "0.05",
            "alpha_bound": "0.0766587862265",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv::private_review_candidate",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "numeric_smoke_placeholder_not_source_backed",
            "formula_reference": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "assumptions": "K_edge*Qbar_edge_XH*qbar_XT inserted for schema smoke only; no parent coefficients",
            "valid_for_claim": "false",
            "notes": "nonclaim smoke row below private review candidate ceiling; must remain invalid until coefficients are source-backed",
        },
        {
            "model_id": "MTS_edge_residual_nonclaim_smoke",
            "branch_id": "edge_missing_input_guard",
            "curve_id": "R10_alpha_lambda_curve_MTS_edge_residual_smoke",
            "lambda_value": "MISSING_PARENT_EDGE_RANGE_OR_ENVELOPE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_EDGE_QBAR_EDGE_QBAR_XT",
            "alpha_bound": "MISSING_CLAIM_GRADE_BOUND",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
            "force_law_form": "edge_alpha_envelope",
            "derivation_status": "template_invalid_missing_edge_inputs",
            "formula_reference": "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
            "assumptions": "explicit missing-input guard row",
            "valid_for_claim": "false",
            "notes": "runner must reject this row",
        },
    ]


def run_runner(bound_curve: Path, output_dir: Path) -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--mts-curve",
            str(EDGE_SMOKE_PATH),
            "--bound-curve",
            str(bound_curve),
            "--output-dir",
            str(output_dir),
        ],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    status_path = output_dir / "R10_runner_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["stdout"] = completed.stdout.strip()
    status["stderr"] = completed.stderr.strip()
    return status


def make_vdef_repair() -> list[dict[str, object]]:
    return [
        {
            "repair_id": "VOR585_0_parent_action_variation",
            "target": "derive theta_Y and Omega_Y from one parent action",
            "required_equation": "delta L_parent = E_Y delta Y + d theta_Y(delta Y)",
            "success_criterion": "C_X appears from i_vX Omega_Y=delta G_X",
            "current_status": "not_derived",
            "fallback": "edge runner inputs",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "VOR585_1_Vdef_P_owner",
            "target": "derive P[Y] from V_def",
            "required_equation": "P^{mu nu}=partial V_def/partial Z_{mu nu}",
            "success_criterion": "P is not independent and source identity is parent-owned",
            "current_status": "promising_but_unfilled",
            "fallback": "P-owner blocker",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "VOR585_2_J_eff_owner",
            "target": "derive J_eff from same variation",
            "required_equation": "J_eff^nu=S_L^nu+d_rel(P_mem J_rel)^nu from parent Noether/current identity",
            "success_criterion": "C_X=-nabla_mu P^{mu nu}+J_eff^nu is one Noether identity",
            "current_status": "not_derived",
            "fallback": "source residual",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "VOR585_3_boundary_exactness",
            "target": "zero edge charge",
            "required_equation": "B_X=n_mu P^{mu nu}=d_boundary b_X or pure gauge on compact shell",
            "success_criterion": "Q_edge=0 and K_boundary=0",
            "current_status": "not_derived",
            "fallback": "Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "VOR585_4_decision",
            "target": "choose owner repair or numeric edge priors",
            "required_equation": "either owner certificate zeros edge branch or runner inputs become numeric/source-backed",
            "success_criterion": "no-pole certificate or executable alpha_edge curve",
            "current_status": "open",
            "fallback": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_claim_blockers(runner_status_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blockers = [
        {
            "blocker_id": "CB585_0_edge_coefficients",
            "blocker": "K_edge, Qbar_edge_XH, and qbar_XT are not source-backed",
            "required_repair": "derive owner zero or fill numeric/source-backed coefficients",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "CB585_1_edge_support",
            "blocker": "lambda_edge/support envelope is not parent-derived",
            "required_repair": "derive edge kernel support or bounded range grid",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "CB585_2_bound_curve",
            "blocker": "live claim bound curve still has placeholder rows and review curve is nonclaim",
            "required_repair": "QA-promote/supplement alpha_bound(lambda) before public scoring",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "CB585_3_no_double_count",
            "blocker": "bulk-edge source split is not orthogonalized",
            "required_repair": "derive Q_X=Q_bulk+Q_edge decomposition and projection rules",
            "claim_blocked": "true",
        },
    ]
    for row in runner_status_rows:
        blockers.append(
            {
                "blocker_id": f"CB585_runner_{row['runner_id']}",
                "blocker": f"runner claim_allowed={row['claim_allowed']} valid_mts_rows={row['valid_mts_rows']} valid_bound_rows={row['valid_bound_rows']}",
                "required_repair": "all MTS and bound rows must be valid_for_claim=true, numeric, sourced, and non-placeholder",
                "claim_blocked": "true",
            }
        )
    return blockers


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D585_0_runner_inputs_written",
            "decision": "edge runner smoke rows written",
            "meaning": "edge branch now has the exact R10 runner schema",
            "status": "progress_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D585_1_runner_blocks_claim",
            "decision": "existing runner blocks nonclaim edge rows",
            "meaning": "valid_for_claim=false and placeholder/live-bound rows correctly prevent accidental claim",
            "status": "guardrail_pass",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D585_2_Vdef_owner_not_repaired",
            "decision": "V_def owner route remains open but unfilled",
            "meaning": "no parent symplectic/action owner has been supplied yet",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D585_3_next_best_target",
            "decision": "choose numeric edge priors or V_def action sketch",
            "meaning": "next checkpoint should either make edge rows genuinely numeric/source-backed or attempt the V_def parent action skeleton",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU585_0_allowed",
            "allowed_after_585": "use R10_alpha_lambda_curve_MTS_edge_residual_smoke.csv for schema smoke only",
            "forbidden_after_585": "copy smoke rows into live claim files or set valid_for_claim=true",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU585_1_allowed",
            "allowed_after_585": "use runner statuses as guardrails proving the branch remains blocked",
            "forbidden_after_585": "read nonclaim runner smoke as evidence",
            "next_action": "fill numeric/source-backed edge inputs",
        },
        {
            "route_id": "RU585_2_allowed",
            "allowed_after_585": "keep V_def owner as theorem-repair route",
            "forbidden_after_585": "claim no-pole until V_def/Omega/boundary exactness are derived",
            "next_action": "Vdef owner action sketch or edge numeric priors",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    runner_schema: list[dict[str, object]],
    edge_smoke_rows: list[dict[str, object]],
    runner_status_rows: list[dict[str, object]],
    vdef_repair: list[dict[str, object]],
    claim_blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    prior_claim_allowed = any(row.get("claim_allowed") == "true" for row in prior_summary)
    schema_ok = [row["column"] for row in runner_schema] == MTS_REQUIRED_COLUMNS
    smoke_all_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" for row in edge_smoke_rows)
    runner_all_blocked = all(row["claim_allowed"] == "False" or row["claim_allowed"] is False for row in runner_status_rows)
    vdef_all_nonclaim = all(row["valid_for_claim"] == "false" for row in vdef_repair)
    blocker_all_true = all(row["claim_blocked"] == "true" for row in claim_blockers)
    claim_decisions = [row for row in decisions if str(row["status"]).lower() in {"pass", "claim", "claim_allowed"}]

    return [
        {
            "check_id": "V585_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V585_1_prior_584_clean",
            "result": "pass" if not prior_failures and not prior_claim_allowed else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};prior_claim_allowed={prior_claim_allowed}",
        },
        {
            "check_id": "V585_2_runner_schema_complete",
            "result": "pass" if schema_ok else "fail",
            "detail": f"schema_columns={len(runner_schema)}",
        },
        {
            "check_id": "V585_3_edge_smoke_rows_nonclaim",
            "result": "pass" if len(edge_smoke_rows) >= 3 and smoke_all_nonclaim else "fail",
            "detail": f"smoke_rows={len(edge_smoke_rows)};valid_for_claim_true=0",
        },
        {
            "check_id": "V585_4_existing_runner_blocks_claim",
            "result": "pass" if len(runner_status_rows) == 2 and runner_all_blocked else "fail",
            "detail": ";".join(f"{row['runner_id']}:claim_allowed={row['claim_allowed']}" for row in runner_status_rows),
        },
        {
            "check_id": "V585_5_Vdef_repair_not_promoted",
            "result": "pass" if vdef_all_nonclaim else "fail",
            "detail": f"vdef_rows={len(vdef_repair)};claim_rows=0",
        },
        {
            "check_id": "V585_6_claim_blockers_all_true",
            "result": "pass" if blocker_all_true else "fail",
            "detail": f"blocker_rows={len(claim_blockers)}",
        },
        {
            "check_id": "V585_7_no_R10_or_local_GR_claim",
            "result": "pass" if not claim_decisions else "fail",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    source_rows: list[dict[str, object]],
    runner_schema: list[dict[str, object]],
    edge_smoke_rows: list[dict[str, object]],
    runner_status_rows: list[dict[str, object]],
    vdef_repair: list[dict[str, object]],
    claim_blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 585 Y5 R10 edge-alpha runner inputs or Vdef owner repair

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{run_root.relative_to(ROOT)}`

## Verdict
- The edge branch now has runner-shaped input rows at `source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_edge_residual_smoke.csv`.
- The existing R10 comparator was run against the live placeholder bound curve and the private review-candidate curve. Both runs correctly block claim status.
- This is runner plumbing, not physics evidence: `K_edge`, `Qbar_edge_XH`, `qbar_XT`, `lambda_edge`, claim-grade bound rows, and the bulk-edge split are still missing.
- `V_def` owner repair remains open but unfilled.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Edge Runner Schema
{markdown_table(runner_schema, ["column", "purpose", "edge_branch_status"])}

## Edge Smoke Rows
{markdown_table(edge_smoke_rows, MTS_REQUIRED_COLUMNS)}

## Runner Status Summary
{markdown_table(runner_status_rows, ["runner_id", "bound_curve", "output_dir", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed"])}

## Vdef Owner Repair Pass
{markdown_table(vdef_repair, ["repair_id", "target", "required_equation", "success_criterion", "current_status", "fallback", "valid_for_claim"])}

## Claim Blocker Ledger
{markdown_table(claim_blockers, ["blocker_id", "blocker", "required_repair", "claim_blocked"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_585", "forbidden_after_585", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is useful plumbing. We can now pass the edge branch through the same machinery as the bulk fifth-force branch without letting it accidentally become a claim. The next fork is crisp: either give `V_def` enough parent-action meat to kill the edge, or start supplying real numeric priors for `lambda_edge`, `K_edge`, `Qbar_edge_XH`, and `qbar_XT`.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc)
    generated_iso = generated.isoformat()
    stamp = generated.strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-edge-alpha-runner-inputs-or-Vdef-owner-repair"

    source_rows = source_register()
    prior_validation = read_csv(PRIOR_584_VALIDATION)
    prior_summary = read_csv(PRIOR_584_SUMMARY)

    runner_schema = make_runner_schema()
    edge_smoke_rows = make_edge_smoke_rows()
    write_csv(EDGE_SMOKE_PATH, edge_smoke_rows, MTS_REQUIRED_COLUMNS)

    live_status = run_runner(LIVE_CLAIM_CURVE, run_root / "live_placeholder_bound" / "results")
    review_status = run_runner(REVIEW_CURVE, run_root / "review_candidate_bound" / "results")
    runner_status_rows = [
        {
            "runner_id": "R10_EDGE_SMOKE_LIVE_PLACEHOLDER",
            "bound_curve": live_status["bound_curve"],
            "output_dir": live_status["output_dir"],
            "mts_rows": live_status["mts_rows"],
            "valid_mts_rows": live_status["valid_mts_rows"],
            "bound_rows": live_status["bound_rows"],
            "valid_bound_rows": live_status["valid_bound_rows"],
            "comparison_rows": live_status["comparison_rows"],
            "passed_rows": live_status["passed_rows"],
            "blocked_or_failed_rows": live_status["blocked_or_failed_rows"],
            "claim_allowed": str(live_status["claim_allowed"]),
        },
        {
            "runner_id": "R10_EDGE_SMOKE_REVIEW_CANDIDATE",
            "bound_curve": review_status["bound_curve"],
            "output_dir": review_status["output_dir"],
            "mts_rows": review_status["mts_rows"],
            "valid_mts_rows": review_status["valid_mts_rows"],
            "bound_rows": review_status["bound_rows"],
            "valid_bound_rows": review_status["valid_bound_rows"],
            "comparison_rows": review_status["comparison_rows"],
            "passed_rows": review_status["passed_rows"],
            "blocked_or_failed_rows": review_status["blocked_or_failed_rows"],
            "claim_allowed": str(review_status["claim_allowed"]),
        },
    ]

    vdef_repair = make_vdef_repair()
    claim_blockers = make_claim_blockers(runner_status_rows)
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        runner_schema,
        edge_smoke_rows,
        runner_status_rows,
        vdef_repair,
        claim_blockers,
        decisions,
    )

    summary_rows = [
        {
            "summary_id": "S585_0_result",
            "status": STATUS,
            "edge_runner_inputs_written": "true",
            "edge_smoke_path": str(EDGE_SMOKE_PATH.relative_to(ROOT)).replace("\\", "/"),
            "runner_live_claim_allowed": str(live_status["claim_allowed"]),
            "runner_review_claim_allowed": str(review_status["claim_allowed"]),
            "Vdef_owner_derived": "false",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "run_root": str(run_root.relative_to(ROOT)).replace("\\", "/"),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(RUNNER_SCHEMA_PATH, runner_schema, ["column", "purpose", "edge_branch_status"])
    write_csv(
        RUNNER_STATUS_PATH,
        runner_status_rows,
        [
            "runner_id",
            "bound_curve",
            "output_dir",
            "mts_rows",
            "valid_mts_rows",
            "bound_rows",
            "valid_bound_rows",
            "comparison_rows",
            "passed_rows",
            "blocked_or_failed_rows",
            "claim_allowed",
        ],
    )
    write_csv(
        VDEF_REPAIR_PATH,
        vdef_repair,
        ["repair_id", "target", "required_equation", "success_criterion", "current_status", "fallback", "valid_for_claim"],
    )
    write_csv(CLAIM_BLOCKERS_PATH, claim_blockers, ["blocker_id", "blocker", "required_repair", "claim_blocked"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update, ["route_id", "allowed_after_585", "forbidden_after_585", "next_action"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "edge_runner_inputs_written",
            "edge_smoke_path",
            "runner_live_claim_allowed",
            "runner_review_claim_allowed",
            "Vdef_owner_derived",
            "claim_allowed",
            "R10_pass_for_claim",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "run_root",
            "next_target",
        ],
    )

    write_markdown(
        generated_iso,
        run_root,
        source_rows,
        runner_schema,
        edge_smoke_rows,
        runner_status_rows,
        vdef_repair,
        claim_blockers,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated_iso,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "edge_smoke_path": str(EDGE_SMOKE_PATH.relative_to(ROOT)),
                "run_root": str(run_root.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "runner_live_claim_allowed": live_status["claim_allowed"],
                "runner_review_claim_allowed": review_status["claim_allowed"],
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
