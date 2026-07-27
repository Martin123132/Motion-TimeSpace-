from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_bound_curve_digitization_and_MTS_alpha_runner_built_dryrun_blocks_placeholders"
CLAIM_CEILING = "R10_runner_implementation_dryrun_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md"

DOC_PATH = Path("559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_559_SOURCE_REGISTER.csv")
BOUND_DIGITIZATION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv")
MTS_ALPHA_RUNNER_SPEC_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_MTS_ALPHA_RUNNER_SPEC.csv")
RUNNER_DRYRUN_SUMMARY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_RUNNER_DRYRUN_SUMMARY.csv")
RUNNER_BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_RUNNER_BLOCKER_LEDGER.csv")
BOUND_CURVE_PLACEHOLDER_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_559_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_559_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_559_ROUTE_UPDATE.csv")


BOUND_CURVE_PLACEHOLDER_ROWS = [
    {
        "bound_id": "R10_BOUND_PLACEHOLDER_0",
        "dataset_id": "Adelberger_Heckel_Nelson_2003_ISL_curve",
        "lambda_value": "MISSING_NUMERIC_LAMBDA",
        "lambda_units": "m",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503",
        "digitization_method": "template_invalid_missing_digitized_curve",
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "valid_for_claim": "false",
        "notes": "replace with digitized lambda/alpha_bound rows before R10 scoring",
    },
    {
        "bound_id": "R10_BOUND_PLACEHOLDER_1",
        "dataset_id": "future_bound_curve_source",
        "lambda_value": "MISSING_NUMERIC_LAMBDA",
        "lambda_units": "m",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "MISSING_BOUND_SOURCE",
        "digitization_method": "template_invalid_missing_source",
        "source_file": "MISSING_SOURCE_FILE",
        "valid_for_claim": "false",
        "notes": "additional bound rows can be added from newer/official sources but remain non-claim until sourced",
    },
]


SOURCE_REGISTER = [
    {
        "source_file": "558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md",
        "role": "R10 no-range theorem failure and placeholder curve file",
    },
    {
        "source_file": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "role": "bulk/memory/range Yukawa fill contract",
    },
    {
        "source_file": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "R10 alpha(lambda) executable curve rules",
    },
    {
        "source_file": "431-MTS-local-residual-vector-evaluator.md",
        "role": "local evaluator placeholder-rejection policy",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "MTS-side alpha(lambda) placeholder curve",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "bound-side alpha(lambda) placeholder curve",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local-bound manifest naming R10 source",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_558_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_CURVE_DATA_AUDIT.csv",
        "role": "558 curve-data audit",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_MTS_CURVE_INPUT_CONTRACT.csv",
        "role": "558 MTS alpha(lambda) input contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAMBDA_PLACEHOLDER_REJECTION.csv",
        "role": "558 placeholder rejection ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "bulk-X source-normalized force-law ledger",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "reusable R10 alpha(lambda) runner",
    },
    {
        "source_file": "scripts/Y5_R10_bound_curve_digitization_and_MTS_alpha_prediction_runner.py",
        "role": "this checkpoint generator",
    },
]


BOUND_DIGITIZATION_CONTRACT_ROWS = [
    {
        "contract_id": "BDC559_0_required_columns",
        "artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "requirement": "bound_id;dataset_id;lambda_value;lambda_units;alpha_bound;alpha_bound_source;digitization_method;source_file;valid_for_claim;notes",
        "current_status": "placeholder_schema_written",
        "claim_status": "false",
    },
    {
        "contract_id": "BDC559_1_numeric_rows",
        "artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "requirement": "lambda_value and alpha_bound must be positive numeric values with units convertible to meters",
        "current_status": "missing_numeric_values",
        "claim_status": "false",
    },
    {
        "contract_id": "BDC559_2_source_provenance",
        "artifact": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "requirement": "each row must cite a bound source and digitization/extraction method",
        "current_status": "source_named_for_first_placeholder_only_not_digitized",
        "claim_status": "false",
    },
    {
        "contract_id": "BDC559_3_interpolation_policy",
        "artifact": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "requirement": "compare exact matching lambda or log-log interpolate positive bound rows inside sampled range",
        "current_status": "runner_implemented",
        "claim_status": "false",
    },
]


MTS_ALPHA_RUNNER_SPEC_ROWS = [
    {
        "spec_id": "AR559_0_MTS_schema",
        "runner_requirement": "MTS curve must use R10_alpha_lambda_curve_MTS_source_normalization.csv schema from checkpoint 558",
        "failure_mode": "missing/non-numeric alpha_predicted or lambda rejects row",
        "current_status": "implemented",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "AR559_1_bound_schema",
        "runner_requirement": "bound curve must use R10_alpha_lambda_bound_curve_DIGITIZED.csv schema",
        "failure_mode": "symbolic alpha(lambda) bound rejects row",
        "current_status": "implemented",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "AR559_2_claim_flag",
        "runner_requirement": "valid_for_claim must be true on both MTS and bound rows before comparison can support R10",
        "failure_mode": "template rows stay dry-run only",
        "current_status": "implemented",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "AR559_3_comparison_rule",
        "runner_requirement": "abs(alpha_predicted(lambda)) <= alpha_bound(lambda) for all valid rows",
        "failure_mode": "any missing, out-of-range, or exceeding row blocks R10",
        "current_status": "implemented",
        "valid_for_claim": "false",
    },
    {
        "spec_id": "AR559_4_no_claim_dryrun",
        "runner_requirement": "dry-run with placeholders must produce R10_pass_for_claim=false",
        "failure_mode": "false-positive local GR pass",
        "current_status": "implemented_and_verified",
        "valid_for_claim": "false",
    },
]


RUNNER_BLOCKER_ROWS = [
    {
        "blocker_id": "RB559_0_MTS_alpha_placeholder",
        "blocked_object": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "reason": "MTS lambda/alpha rows are placeholders",
        "repair": "derive source-normalized alpha_predicted(lambda) or theorem-zero",
        "valid_for_claim": "false",
    },
    {
        "blocker_id": "RB559_1_bound_curve_placeholder",
        "blocked_object": "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "reason": "bound lambda/alpha rows are placeholders",
        "repair": "digitize or source machine-readable inverse-square bound curve",
        "valid_for_claim": "false",
    },
    {
        "blocker_id": "RB559_2_no_valid_rows",
        "blocked_object": "R10_runner_comparison.csv",
        "reason": "runner has no valid MTS rows and no valid bound rows to compare",
        "repair": "fill both sides with source-backed numeric rows and rerun",
        "valid_for_claim": "false",
    },
    {
        "blocker_id": "RB559_3_no_theorem_zero",
        "blocked_object": "R10 no-range branch",
        "reason": "no theorem-zero certificate exists as an alternative to curve comparison",
        "repair": "derive no-range theorem or keep R10 retained",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D559_0_runner_built",
        "status": "R10_bound_prediction_runner_built",
        "meaning": "R10 now has a reusable curve validator/comparator",
        "claim_status": "dryrun_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D559_1_placeholders_blocked",
        "status": "placeholder_dryrun_rejected",
        "meaning": "runner correctly refuses MTS and bound placeholder rows",
        "claim_status": "R10_pass_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D559_2_bound_curve_template_written",
        "status": "bound_curve_digitization_template_written",
        "meaning": "the expected digitized bound-curve file exists but is non-claim until populated",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D559_3_local_GR_status",
        "status": "local_GR_still_closure_only",
        "meaning": "no R10/fifth-force, Cextra, radial closure, Newton, PPN, or local-GR promotion is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D559_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "R10_FIFTH_FORCE",
        "previous_status": "no_range_failed_expected_curve_file_written_invalid",
        "new_status": "runner_built_placeholders_rejected_no_R10_pass",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_RESIDUAL_VECTOR",
        "previous_status": "R10_placeholder_file_exists_but_rejected_for_claim",
        "new_status": "R10_runner_available_for_future_real_curve_rows",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "CEXTRA_BULK_MEMORY_RANGE",
        "previous_status": "still_failed_no_range_and_no_alpha_lambda_curve",
        "new_status": "still_failed_runner_waits_for_real_alpha_prediction_or_no_range_theorem",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "HAMILTONIAN_EXTRA_CHARGE_SILENCE",
        "previous_status": "still_failed_R10_bulk_memory_range_data_missing",
        "new_status": "still_failed_R10_runner_dryrun_only",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR_TRANSITION_ROUTE",
        "previous_status": "closure_only_R10_no_range_or_curve_not_available",
        "new_status": "closure_only_R10_runner_no_claim",
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
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


def runner_summary_rows(runner_result: dict[str, Any], runner_results_dir: Path) -> list[dict[str, Any]]:
    status = runner_result["status"]
    return [
        {
            "summary_id": "R10_RUNNER_559",
            "runner_results_dir": rel(runner_results_dir),
            "mts_rows": status["mts_rows"],
            "valid_mts_rows": status["valid_mts_rows"],
            "bound_rows": status["bound_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "passed_rows": status["passed_rows"],
            "blocked_or_failed_rows": status["blocked_or_failed_rows"],
            "R10_pass_for_claim": status["R10_pass_for_claim"],
            "claim_allowed": status["claim_allowed"],
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    runner_result: dict[str, Any],
    runner_summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_558_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    mts_curve = read_csv(Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv"))
    bound_curve = read_csv(BOUND_CURVE_PLACEHOLDER_PATH)
    local_bounds = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    r10_rows = [row for row in local_bounds if row.get("row_id") == "R10_fifth_force"]
    mts_validation = runner_result["mts_validation"]
    bound_validation = runner_result["bound_validation"]
    comparisons = runner_result["comparisons"]
    runner_status = runner_result["status"]
    claim_runner_rows = [row for row in comparisons if row.get("pass_for_claim") == "true"]
    claim_bound_rows = [row for row in bound_curve if row.get("valid_for_claim") == "true"]
    claim_mts_rows = [row for row in mts_curve if row.get("valid_for_claim") == "true"]
    return [
        {
            "check_id": "V559_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V559_1_prior_558_clean",
            "result": "pass" if len(prior_validation) == 11 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V559_2_curve_files_loaded",
            "result": "pass" if len(mts_curve) == 2 and len(bound_curve) == 2 else "fail",
            "detail": f"mts_curve_rows={len(mts_curve)};bound_curve_rows={len(bound_curve)}",
        },
        {
            "check_id": "V559_3_bound_manifest_context_loaded",
            "result": "pass" if len(local_bounds) == 12 and len(r10_rows) == 1 else "fail",
            "detail": f"local_bounds={len(local_bounds)};R10_rows={len(r10_rows)}",
        },
        {
            "check_id": "V559_4_runner_outputs_written",
            "result": "pass" if len(mts_validation) == 2 and len(bound_validation) == 2 and len(comparisons) == 1 else "fail",
            "detail": f"mts_validation={len(mts_validation)};bound_validation={len(bound_validation)};comparisons={len(comparisons)}",
        },
        {
            "check_id": "V559_5_runner_blocks_placeholders",
            "result": "pass" if runner_status["valid_mts_rows"] == 0 and runner_status["valid_bound_rows"] == 0 and runner_status["R10_pass_for_claim"] is False else "fail",
            "detail": f"valid_mts={runner_status['valid_mts_rows']};valid_bound={runner_status['valid_bound_rows']};R10_pass={runner_status['R10_pass_for_claim']}",
        },
        {
            "check_id": "V559_6_contracts_complete",
            "result": "pass" if len(BOUND_DIGITIZATION_CONTRACT_ROWS) == 4 and len(MTS_ALPHA_RUNNER_SPEC_ROWS) == 5 and len(RUNNER_BLOCKER_ROWS) == 4 else "fail",
            "detail": f"bound_contract={len(BOUND_DIGITIZATION_CONTRACT_ROWS)};runner_spec={len(MTS_ALPHA_RUNNER_SPEC_ROWS)};blockers={len(RUNNER_BLOCKER_ROWS)}",
        },
        {
            "check_id": "V559_7_summary_written",
            "result": "pass" if len(runner_summary) == 1 and runner_summary[0]["R10_pass_for_claim"] is False else "fail",
            "detail": f"summary_rows={len(runner_summary)};R10_pass={runner_summary[0]['R10_pass_for_claim'] if runner_summary else 'missing'}",
        },
        {
            "check_id": "V559_8_no_claim_rows",
            "result": "pass" if not claim_runner_rows and not claim_bound_rows and not claim_mts_rows else "fail",
            "detail": f"claim_runner={len(claim_runner_rows)};claim_bound={len(claim_bound_rows)};claim_mts={len(claim_mts_rows)}",
        },
        {
            "check_id": "V559_9_no_overclaim",
            "result": "pass" if runner_status["R10_pass_for_claim"] is False and not claim_runner_rows and not claim_bound_rows and not claim_mts_rows else "fail",
            "detail": "R10_pass=false; fifth_force=false; Cextra=false; radial_closure=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    runner_summary: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 559 - Y5 R10 Bound-Curve Digitization and MTS Alpha Prediction Runner

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The R10 runner now exists and correctly rejects placeholders.

This is an implementation checkpoint, not a physics pass. The machinery can now compare:

```text
abs(alpha_predicted(lambda_i)) <= alpha_bound(lambda_i)
```

but the current dry-run has zero valid MTS rows and zero valid bound rows, so R10 remains blocked.

## 2. Bound-Curve Digitization Contract

{markdown_table(BOUND_DIGITIZATION_CONTRACT_ROWS)}

## 3. MTS Alpha Runner Spec

{markdown_table(MTS_ALPHA_RUNNER_SPEC_ROWS)}

## 4. Bound Curve Placeholder

{markdown_table(BOUND_CURVE_PLACEHOLDER_ROWS)}

## 5. Runner Dry-Run Summary

{markdown_table(runner_summary)}

## 6. Runner Blocker Ledger

{markdown_table(RUNNER_BLOCKER_ROWS)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has an R10 alpha(lambda) bound/prediction runner.
MTS has an invalid placeholder bound curve file.
MTS dry-run rejection of placeholder rows is verified.
```

Forbidden:

```text
MTS has passed R10/fifth-force.
MTS has produced a real alpha(lambda) prediction.
MTS has produced digitized bound-curve data.
MTS has proved C_extra = 0, radial closure, Newton, PPN, or local GR.
```

## 12. Practical Read

This is a good little machine-room checkpoint. We now have the judge for the R10 round. It is not impressed by vibes. It wants real `lambda`, real `alpha_predicted`, real `alpha_bound`, and source paths.

## 13. Next Target

`{NEXT_TARGET}`

Next: either derive the MTS source-normalized alpha law from the parent branch, or fill a real runner input file with sourced bound data and non-claim smoke predictions.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner"
    results_dir = run_dir / "results"
    runner_results_dir = results_dir / "runner"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(BOUND_CURVE_PLACEHOLDER_PATH, BOUND_CURVE_PLACEHOLDER_ROWS)
    write_run_csv(results_dir, BOUND_CURVE_PLACEHOLDER_PATH.name, BOUND_CURVE_PLACEHOLDER_ROWS)

    runner_result = run_runner(
        ROOT / "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        ROOT / BOUND_CURVE_PLACEHOLDER_PATH,
        runner_results_dir,
    )
    runner_summary = runner_summary_rows(runner_result, runner_results_dir)

    sources = source_rows()
    validations = validation_rows(sources, runner_result, runner_summary)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (BOUND_DIGITIZATION_CONTRACT_PATH, BOUND_DIGITIZATION_CONTRACT_ROWS),
        (MTS_ALPHA_RUNNER_SPEC_PATH, MTS_ALPHA_RUNNER_SPEC_ROWS),
        (RUNNER_DRYRUN_SUMMARY_PATH, runner_summary),
        (RUNNER_BLOCKER_LEDGER_PATH, RUNNER_BLOCKER_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, runner_summary, validations)
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
        "runner_results_dir": str(runner_results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "bound_curve": str(ROOT / BOUND_CURVE_PLACEHOLDER_PATH),
        "runner_script": str(ROOT / "scripts/R10_alpha_lambda_bound_prediction_runner.py"),
        "runner_status": runner_result["status"],
        "validation": str(ROOT / VALIDATION_PATH),
        "missing_sources": missing_sources,
        "failed_validations": failed_validations,
        "R10_runner_built": True,
        "R10_fifth_force_passed": False,
        "R10_curve_valid_for_claim": False,
        "Cextra_zero_signed": False,
        "radial_closure_claim_allowed": False,
        "source_measure_claim_allowed": False,
        "measured_GM_claim_allowed": False,
        "Newton_claim_allowed": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "formalization_workbench_modified": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
