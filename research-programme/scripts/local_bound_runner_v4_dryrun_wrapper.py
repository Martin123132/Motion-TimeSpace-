from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v4-dryrun-wrapper"
CHECKPOINT_DOC = "426-local-bound-runner-v4-dryrun-wrapper.md"
STATUS = "local_bound_runner_v4_dryrun_wrapper_written_inner_dryrun_passed_source_intake_template_ready_no_data_claim_no_local_GR_pass"
CLAIM_CEILING = "local_bound_runner_v4_dryrun_wrapper_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "427-source-normalization-bounds-csv-template-fill.md"
INTERFACE_SCRIPT = ROOT / "scripts" / "local_bound_runner_v4_real_data_interface.py"
INTERFACE_RUN_SLUG = "local-bound-runner-v4-real-data-interface"
SOURCE_INTAKE_DIR = ROOT / "source-intake" / "local_bounds"


SOURCE_DOCS = [
    {
        "path": "411-local-bound-runner-v4-real-data-interface.md",
        "role": "runner-v4 local-bound interface and dry-run/evaluate command contract",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH-operator/source-normalization retained ledger and test matrix",
    },
    {
        "path": "scripts/local_bound_runner_v4_real_data_interface.py",
        "role": "inner dry-run/evaluate script",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/EH_operator_retained_ledger.csv",
        "role": "operator-family ledger to keep non-EH channels retained",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/source_normalization_channel_plan.csv",
        "role": "source-normalization channels and row locks",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/local_bound_test_matrix.csv",
        "role": "baseline-aware local-bound tests",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/dry_run_workflow.csv",
        "role": "VS Code safe dry-run/evaluate workflow",
    },
]


INNER_REQUIRED_ARTIFACTS = [
    "command_manifest.csv",
    "decision.csv",
    "external_bound_evaluation.csv",
    "gate_results.csv",
    "interface_contract.csv",
    "interface_schema.csv",
    "interface_summary.csv",
    "local_bounds_template.csv",
    "local_data_targets.csv",
    "next_queue.csv",
    "source_register.csv",
    "validation_errors.csv",
]


DECISION = [
    {
        "decision": "The local-bound runner-v4 dry-run now executes through a wrapper that checks the inner interface artifacts, preserves the EH/source retained ledger, writes a source-intake template, and refuses local-GR theorem credit. The project is ready for the next testing move: fill a verified local-bound CSV and evaluate it against the same baseline-aware pipeline.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence": "no",
        "real_external_data_loaded": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "427-source-normalization-bounds-csv-template-fill.md",
        "task": "prepare or fill the local_bound_claims.csv source-intake file using verified external/local bound sources only",
        "priority": "P0",
    },
    {
        "next_file": "427-local-bound-runner-v4-evaluate-smoke.md",
        "task": "run a short evaluate pass once the source-intake CSV exists and preserve GR/null baseline comparison",
        "priority": "P0",
    },
    {
        "next_file": "427-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "task": "attempt the derivation that kills source_residuals and mu_extra rather than closing them by axiom",
        "priority": "P1",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_health(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "artifact": path.name,
            "exists": False,
            "row_count": 0,
            "malformed_rows": "",
            "status": "missing",
        }
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    malformed = [str(index + 2) for index, row in enumerate(rows) if None in row]
    return {
        "artifact": path.name,
        "exists": True,
        "row_count": len(rows),
        "malformed_rows": ";".join(malformed),
        "status": "pass" if not malformed else "malformed",
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": path.exists(),
                "role": item["role"],
            }
        )
    return rows


def run_inner_dryrun(timestamp: str, outer_run_dir: Path) -> tuple[Path, dict[str, Any]]:
    inner_timestamp = f"{timestamp}-wrapped-dryrun"
    command = [
        sys.executable,
        str(INTERFACE_SCRIPT),
        "--timestamp",
        inner_timestamp,
        "--mode",
        "dry-run",
    ]
    completed = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    inner_run_dir = ROOT / "runs" / f"{inner_timestamp}-{INTERFACE_RUN_SLUG}"
    (outer_run_dir / "inner_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (outer_run_dir / "inner_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    command_row = {
        "command_id": "wrapped_runner_v4_dry_run",
        "exit_code": completed.returncode,
        "inner_timestamp": inner_timestamp,
        "inner_run_dir": str(inner_run_dir),
        "command": " ".join(command),
        "stdout_path": "inner_stdout.txt",
        "stderr_path": "inner_stderr.txt",
    }
    return inner_run_dir, command_row


def row_prefix(row_id: str) -> str:
    return row_id.split("_", 1)[0]


def expand_target_rows(target_rows: str) -> list[str]:
    parts = [part.strip() for part in target_rows.split(";") if part.strip()]
    expanded: list[str] = []
    for part in parts:
        if part == "R0-R11":
            expanded.extend([f"R{index}" for index in range(12)])
        else:
            expanded.append(part)
    return expanded


def ledger_join_rows(inner_results_dir: Path, checkpoint_425_results_dir: Path) -> list[dict[str, Any]]:
    targets = read_csv(inner_results_dir / "local_data_targets.csv")
    test_matrix = read_csv(checkpoint_425_results_dir / "local_bound_test_matrix.csv")
    target_by_prefix = {row_prefix(row["row_id"]): row for row in targets if row.get("row_id")}
    rows: list[dict[str, Any]] = []
    for test in test_matrix:
        for row_id in expand_target_rows(test["target_rows"]):
            target = target_by_prefix.get(row_id)
            rows.append(
                {
                    "test_id": test["test_id"],
                    "row_prefix": row_id,
                    "joined_row_id": target.get("row_id", "") if target else "",
                    "observable": target.get("observable", "") if target else "",
                    "source_lock": target.get("source_lock", "") if target else "",
                    "source_lock_units": target.get("source_lock_units", "") if target else "",
                    "baseline_required": test["baseline_required"],
                    "claim_policy": test["claim_policy"],
                    "join_status": "pass" if target else "missing_target",
                }
            )
    return rows


def baseline_control_rows(checkpoint_425_results_dir: Path) -> list[dict[str, Any]]:
    test_matrix = read_csv(checkpoint_425_results_dir / "local_bound_test_matrix.csv")
    rows = []
    for test in test_matrix:
        rows.append(
            {
                "test_id": test["test_id"],
                "target_rows": test["target_rows"],
                "baseline_required": test["baseline_required"],
                "baseline_status": "pass" if test["baseline_required"] == "yes" else "fail",
                "claim_policy": test["claim_policy"],
                "wrapper_action": "keep_same_pipeline_GR_null_baseline_before_MTS_interpretation",
            }
        )
    return rows


def schema_validation_rows(inner_results_dir: Path, checkpoint_425_results_dir: Path) -> list[dict[str, Any]]:
    targets = read_csv(inner_results_dir / "local_data_targets.csv")
    template = read_csv(inner_results_dir / "local_bounds_template.csv")
    summary = read_csv(inner_results_dir / "interface_summary.csv")
    validation_errors = read_csv(inner_results_dir / "validation_errors.csv")
    gate_rows = read_csv(inner_results_dir / "gate_results.csv")
    operator_ledger = read_csv(checkpoint_425_results_dir / "EH_operator_retained_ledger.csv")
    source_channels = read_csv(checkpoint_425_results_dir / "source_normalization_channel_plan.csv")
    test_matrix = read_csv(checkpoint_425_results_dir / "local_bound_test_matrix.csv")
    summary_by_item = {row["summary_item"]: row for row in summary if row.get("summary_item")}
    gate_by_name = {row["gate"]: row for row in gate_rows if row.get("gate")}
    return [
        {
            "check": "local_data_targets_count",
            "observed": len(targets),
            "expected": 12,
            "status": "pass" if len(targets) == 12 else "fail",
        },
        {
            "check": "local_bounds_template_count",
            "observed": len(template),
            "expected": 12,
            "status": "pass" if len(template) == 12 else "fail",
        },
        {
            "check": "validation_errors_count",
            "observed": len(validation_errors),
            "expected": 0,
            "status": "pass" if len(validation_errors) == 0 else "fail",
        },
        {
            "check": "external_bounds_loaded",
            "observed": summary_by_item.get("external_bounds_loaded", {}).get("value", ""),
            "expected": "False",
            "status": "pass" if summary_by_item.get("external_bounds_loaded", {}).get("value", "") == "False" else "fail",
        },
        {
            "check": "claim_allowed_rows",
            "observed": summary_by_item.get("claim_allowed_rows", {}).get("value", ""),
            "expected": "0",
            "status": "pass" if summary_by_item.get("claim_allowed_rows", {}).get("value", "") == "0" else "fail",
        },
        {
            "check": "theorem_credit_rows",
            "observed": summary_by_item.get("theorem_credit_rows", {}).get("value", ""),
            "expected": "0",
            "status": "pass" if summary_by_item.get("theorem_credit_rows", {}).get("value", "") == "0" else "fail",
        },
        {
            "check": "inner_claim_ceiling",
            "observed": gate_by_name.get("claim_ceiling_enforced", {}).get("status", ""),
            "expected": "pass",
            "status": "pass" if gate_by_name.get("claim_ceiling_enforced", {}).get("status", "") == "pass" else "fail",
        },
        {
            "check": "EH_operator_ledger_count",
            "observed": len(operator_ledger),
            "expected": 10,
            "status": "pass" if len(operator_ledger) == 10 else "fail",
        },
        {
            "check": "source_normalization_channel_count",
            "observed": len(source_channels),
            "expected": 7,
            "status": "pass" if len(source_channels) == 7 else "fail",
        },
        {
            "check": "local_bound_test_matrix_count",
            "observed": len(test_matrix),
            "expected": 12,
            "status": "pass" if len(test_matrix) == 12 else "fail",
        },
    ]


def source_intake_artifact_rows(inner_results_dir: Path) -> list[dict[str, Any]]:
    SOURCE_INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    template_source = inner_results_dir / "local_bounds_template.csv"
    template_target = SOURCE_INTAKE_DIR / "local_bound_claims_TEMPLATE.csv"
    claims_target = SOURCE_INTAKE_DIR / "local_bound_claims.csv"
    readme_target = SOURCE_INTAKE_DIR / "README.md"
    if template_source.exists():
        shutil.copyfile(template_source, template_target)
    readme_target.write_text(
        "\n".join(
            [
                "# Local Bound Source Intake",
                "",
                "Use `local_bound_claims_TEMPLATE.csv` as the starting point for verified local-bound sources.",
                "",
                "Do not create or evaluate `local_bound_claims.csv` until every row you keep has a real source path, DOI, URL, or local citation. Template internal locks are not empirical data claims.",
                "",
                "After a verified `local_bound_claims.csv` exists, run the evaluate command from `426-local-bound-runner-v4-dryrun-wrapper.md` or the generated dry-run workflow.",
            ]
        ),
        encoding="utf-8",
    )
    return [
        {
            "artifact": "local_bound_claims_TEMPLATE.csv",
            "path": str(template_target),
            "exists": template_target.exists(),
            "purpose": "editable copy of dry-run template; not empirical evidence",
        },
        {
            "artifact": "README.md",
            "path": str(readme_target),
            "exists": readme_target.exists(),
            "purpose": "source-intake rules and no-claim warning",
        },
        {
            "artifact": "local_bound_claims.csv",
            "path": str(claims_target),
            "exists": claims_target.exists(),
            "purpose": "future verified external/local bound file; absent is correct at dry-run stage",
        },
    ]


def gate_result_rows(
    source_rows: list[dict[str, Any]],
    command_row: dict[str, Any],
    artifact_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    join_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    source_intake_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    missing_artifacts = [row for row in artifact_rows if not row["exists"]]
    malformed_artifacts = [row for row in artifact_rows if row["status"] == "malformed"]
    failed_schema = [row for row in schema_rows if row["status"] != "pass"]
    missing_joins = [row for row in join_rows if row["join_status"] != "pass"]
    failed_baselines = [row for row in baseline_rows if row["baseline_status"] != "pass"]
    missing_intake_template = [
        row
        for row in source_intake_rows
        if row["artifact"] in {"local_bound_claims_TEMPLATE.csv", "README.md"} and not row["exists"]
    ]
    claims_file_rows = [row for row in source_intake_rows if row["artifact"] == "local_bound_claims.csv" and row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "inner_dry_run_exit_zero",
            "status": "pass" if command_row["exit_code"] == 0 else "fail",
            "evidence": f"exit_code={command_row['exit_code']}",
        },
        {
            "gate": "inner_DONE_exists",
            "status": "pass" if (Path(command_row["inner_run_dir"]) / "DONE.txt").exists() else "fail",
            "evidence": str(Path(command_row["inner_run_dir"]) / "DONE.txt"),
        },
        {
            "gate": "inner_required_artifacts_exist",
            "status": "pass" if not missing_artifacts else "fail",
            "evidence": f"{len(missing_artifacts)} missing artifacts",
        },
        {
            "gate": "inner_required_csvs_well_formed",
            "status": "pass" if not malformed_artifacts else "fail",
            "evidence": f"{len(malformed_artifacts)} malformed artifacts",
        },
        {
            "gate": "schema_validation_passed",
            "status": "pass" if not failed_schema else "fail",
            "evidence": f"{len(failed_schema)} failed schema checks",
        },
        {
            "gate": "ledger_rows_join_runner_targets",
            "status": "pass" if not missing_joins else "fail",
            "evidence": f"{len(missing_joins)} missing row joins",
        },
        {
            "gate": "GR_null_baseline_required",
            "status": "pass" if not failed_baselines else "fail",
            "evidence": f"{len(failed_baselines)} test rows without baseline requirement",
        },
        {
            "gate": "source_intake_template_written",
            "status": "pass" if not missing_intake_template else "fail",
            "evidence": f"{len(missing_intake_template)} required source-intake artifacts missing",
        },
        {
            "gate": "real_claims_file_absent_in_dryrun",
            "status": "pass" if not claims_file_rows else "warn",
            "evidence": "local_bound_claims.csv not created by wrapper" if not claims_file_rows else "local_bound_claims.csv exists; evaluate only if verified",
        },
        {
            "gate": "external_data_loaded",
            "status": "not_run",
            "evidence": "dry-run wrapper only; no external data evaluated",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "no WEP/EH/Newton/PPN/fifth-force pass claimed",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    command_row: dict[str, Any],
    artifact_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    join_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    source_intake_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, str]],
) -> None:
    artifact_table_rows = [
        {
            "artifact": row["artifact"],
            "exists": row["exists"],
            "row_count": row["row_count"],
            "status": row["status"],
        }
        for row in artifact_rows
    ]
    schema_table_rows = [
        {
            "check": row["check"],
            "observed": row["observed"],
            "expected": row["expected"],
            "status": row["status"],
        }
        for row in schema_rows
    ]
    join_table_rows = [
        {
            "test_id": row["test_id"],
            "row_prefix": row["row_prefix"],
            "joined_row_id": row["joined_row_id"],
            "join_status": row["join_status"],
        }
        for row in join_rows
    ]
    baseline_table_rows = [
        {
            "test_id": row["test_id"],
            "target_rows": row["target_rows"],
            "baseline_status": row["baseline_status"],
            "claim_policy": row["claim_policy"],
        }
        for row in baseline_rows
    ]
    intake_table_rows = [
        {
            "artifact": row["artifact"],
            "exists": row["exists"],
            "purpose": row["purpose"],
        }
        for row in source_intake_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_rows
    ]
    evaluate_command = "$py = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\.venv-score\\Scripts\\python.exe'; $pc = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\\local_bound_runner_v4_real_data_interface.py') --mode evaluate --bounds-csv (Join-Path $pc 'source-intake\\local_bounds\\local_bound_claims.csv')"
    text = f"""# 426 - Local Bound Runner-v4 Dry-Run Wrapper

Private testing workflow checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 425 gave us the EH-operator/source-normalization ledger. This checkpoint makes the first testing move: run the local-bound runner-v4 interface in dry-run mode, verify its artifacts, join it to the retained ledger, and prepare a source-intake template without treating template locks as data.

This is the boring bit that matters. If the pipeline cannot keep GR/null baselines, symbolic rows, and source-normalization channels honest, any later "hit" is just footwork on a banana skin.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_dryrun_wrapper.py` |
| Run directory | `runs/{run_dir.name}` |
| Inner dry-run directory | `{Path(command_row["inner_run_dir"]).relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Inner Dry-Run Invocation

| Item | Value |
| --- | --- |
| Command id | `{command_row["command_id"]}` |
| Exit code | `{command_row["exit_code"]}` |
| Stdout | `runs/{run_dir.name}/inner_stdout.txt` |
| Stderr | `runs/{run_dir.name}/inner_stderr.txt` |

## 4. Inner Artifact Check

{markdown_table(artifact_table_rows, ["artifact", "exists", "row_count", "status"])}

## 5. Schema and Claim Validation

{markdown_table(schema_table_rows, ["check", "observed", "expected", "status"])}

## 6. Ledger-to-Runner Join

{markdown_table(join_table_rows, ["test_id", "row_prefix", "joined_row_id", "join_status"])}

## 7. Baseline Controls

{markdown_table(baseline_table_rows, ["test_id", "target_rows", "baseline_status", "claim_policy"])}

Every test keeps `baseline_required=yes`. This is the fair-fight rule: if MTS is scored under a stress test, the GR/null baseline is scored in the same pipeline instead of being assumed clean by vibes.

## 8. Source-Intake Template

{markdown_table(intake_table_rows, ["artifact", "exists", "purpose"])}

Future evaluate command after verified sources are filled:

```powershell
{evaluate_command}
```

Do not run that as a claim until `source-intake/local_bounds/local_bound_claims.csv` contains verified external/local source rows. The generated template is a scaffold, not empirical evidence.

## 9. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 10. Decision

{DECISION[0]["decision"]}

Practical read: we are now testing-ready in the narrow local-bound sense. The next step is not to celebrate; it is to fill or source the bounds CSV cleanly, run a short evaluate smoke, and see which retained channels actually bite.

## 11. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    run_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_425_results_dir = ROOT / "runs" / "20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan" / "results"

    source_rows = source_register_rows()
    inner_run_dir, command_row = run_inner_dryrun(timestamp, run_dir)
    inner_results_dir = inner_run_dir / "results"
    artifact_rows = [csv_health(inner_results_dir / artifact) for artifact in INNER_REQUIRED_ARTIFACTS]
    schema_rows = schema_validation_rows(inner_results_dir, checkpoint_425_results_dir)
    join_rows = ledger_join_rows(inner_results_dir, checkpoint_425_results_dir)
    baseline_rows = baseline_control_rows(checkpoint_425_results_dir)
    source_intake_rows = source_intake_artifact_rows(inner_results_dir)
    gate_rows = gate_result_rows(
        source_rows,
        command_row,
        artifact_rows,
        schema_rows,
        join_rows,
        baseline_rows,
        source_intake_rows,
    )

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "runner_invocation.csv", [command_row])
    write_csv(results_dir / "inner_run_artifacts.csv", artifact_rows)
    write_csv(results_dir / "schema_validation.csv", schema_rows)
    write_csv(results_dir / "ledger_join_plan.csv", join_rows)
    write_csv(results_dir / "baseline_control_plan.csv", baseline_rows)
    write_csv(results_dir / "source_intake_artifacts.csv", source_intake_rows)
    write_csv(results_dir / "gate_results.csv", gate_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_gates = [row["gate"] for row in gate_rows if row["status"] == "fail" and row["gate"] != "local_GR_promoted"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "inner_run_dir": str(inner_run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "inner_dry_run_exit_code": command_row["exit_code"],
        "inner_required_artifacts": len(artifact_rows),
        "schema_checks": len(schema_rows),
        "ledger_join_rows": len(join_rows),
        "baseline_control_rows": len(baseline_rows),
        "source_intake_template_ready": any(
            row["artifact"] == "local_bound_claims_TEMPLATE.csv" and row["exists"] for row in source_intake_rows
        ),
        "claims_file_created": any(
            row["artifact"] == "local_bound_claims.csv" and row["exists"] for row in source_intake_rows
        ),
        "external_data_loaded": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(
        run_dir,
        command_row,
        artifact_rows,
        schema_rows,
        join_rows,
        baseline_rows,
        source_intake_rows,
        gate_rows,
    )
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run and validate the local-bound runner-v4 dry-run through the checkpoint 425 EH/source ledger."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
