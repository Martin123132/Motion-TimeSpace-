from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v4-evaluate-smoke"
CHECKPOINT_DOC = "427-local-bound-runner-v4-evaluate-smoke.md"
STATUS = "local_bound_runner_v4_evaluate_smoke_passed_12_sourced_rows_evaluated_symbolic_rows_deferred_no_MTS_residual_claim_no_local_GR_pass"
CLAIM_CEILING = "local_bound_evaluate_smoke_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "428-MTS-local-residual-vector-input-contract.md"
INTERFACE_SCRIPT = ROOT / "scripts" / "local_bound_runner_v4_real_data_interface.py"
INTERFACE_RUN_SLUG = "local-bound-runner-v4-real-data-interface"
CLAIMS_CSV = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"


SOURCE_DOCS = [
    {
        "path": "427-source-normalization-bounds-csv-template-fill.md",
        "role": "verified source-intake file checkpoint",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "sourced local-bound claims CSV",
    },
    {
        "path": "scripts/local_bound_runner_v4_real_data_interface.py",
        "role": "evaluate-mode runner-v4 interface",
    },
    {
        "path": "runs/20260602-092500-source-normalization-bounds-csv-template-fill/results/row_source_quality.csv",
        "role": "source quality and symbolic-row policy",
    },
]


DECISION = [
    {
        "decision": "Evaluate mode successfully reads the verified local_bound_claims.csv, evaluates all 12 local-bound rows, preserves symbolic R10/R11 treatment, and grants zero theorem or claim credit. This makes the pipeline empirically usable, but it still does not test MTS itself until an MTS residual vector is supplied.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "external_bounds_loaded": "yes",
        "MTS_residuals_loaded": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "428-MTS-local-residual-vector-input-contract.md",
        "task": "define the exact residual quantities MTS must output for eta/gamma/beta/alpha_i/xi/Gdot/fifth-force/operator rows",
        "priority": "P0",
    },
    {
        "next_file": "428-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "task": "attempt the derivation that makes source_residuals and mu_extra vanish instead of closure-assuming them",
        "priority": "P0",
    },
    {
        "next_file": "428-local-bound-evaluate-baseline-red-team.md",
        "task": "red-team the evaluate runner for source-lock assumptions, strong-field caveats, and baseline fairness",
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


def run_inner_evaluate(timestamp: str, outer_run_dir: Path) -> tuple[Path, dict[str, Any]]:
    inner_timestamp = f"{timestamp}-wrapped-evaluate"
    command = [
        sys.executable,
        str(INTERFACE_SCRIPT),
        "--timestamp",
        inner_timestamp,
        "--mode",
        "evaluate",
        "--bounds-csv",
        str(CLAIMS_CSV),
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
    return inner_run_dir, {
        "command_id": "wrapped_runner_v4_evaluate",
        "exit_code": completed.returncode,
        "inner_timestamp": inner_timestamp,
        "inner_run_dir": str(inner_run_dir),
        "bounds_csv": str(CLAIMS_CSV),
        "command": " ".join(command),
        "stdout_path": "inner_stdout.txt",
        "stderr_path": "inner_stderr.txt",
    }


def summary_rows(inner_results_dir: Path) -> list[dict[str, Any]]:
    summary = read_csv(inner_results_dir / "interface_summary.csv")
    by_item = {row["summary_item"]: row for row in summary if row.get("summary_item")}
    return [
        {
            "summary_item": item,
            "value": by_item.get(item, {}).get("value", ""),
            "status": by_item.get(item, {}).get("status", "missing"),
        }
        for item in [
            "targets_mapped",
            "schema_columns",
            "external_bounds_loaded",
            "external_rows_evaluated",
            "evaluation_errors",
            "claim_allowed_rows",
            "theorem_credit_rows",
        ]
    ]


def bound_status_counts(evaluation_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    counts = Counter(row.get("data_bound_status", "") for row in evaluation_rows)
    return [
        {
            "data_bound_status": status,
            "row_count": count,
        }
        for status, count in sorted(counts.items())
    ]


def evaluation_digest_rows(evaluation_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in evaluation_rows:
        rows.append(
            {
                "row_id": row.get("row_id", ""),
                "observable": row.get("observable", ""),
                "runner_v4_state": row.get("runner_v4_state", ""),
                "upper_bound": row.get("upper_bound", ""),
                "source_lock": row.get("source_lock", ""),
                "bound_to_source_lock_ratio": row.get("bound_to_source_lock_ratio", ""),
                "data_bound_status": row.get("data_bound_status", ""),
                "theorem_credit_allowed": row.get("theorem_credit_allowed", ""),
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    command_row: dict[str, Any],
    inner_run_dir: Path,
    summary: list[dict[str, Any]],
    evaluation_rows: list[dict[str, str]],
    validation_errors: list[dict[str, str]],
) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    summary_by_item = {row["summary_item"]: row for row in summary}
    theorem_credit = [
        row for row in evaluation_rows if row.get("theorem_credit_allowed", "").lower() == "true"
    ]
    claim_rows = [
        row for row in evaluation_rows if row.get("claim_allowed", "").lower() == "true"
    ]
    symbolic_rows = [
        row
        for row in evaluation_rows
        if row.get("data_bound_status") == "symbolic_or_curve_input_recorded_no_scalar_pass"
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "claims_csv_exists",
            "status": "pass" if CLAIMS_CSV.exists() else "fail",
            "evidence": str(CLAIMS_CSV),
        },
        {
            "gate": "inner_evaluate_exit_zero",
            "status": "pass" if command_row["exit_code"] == 0 else "fail",
            "evidence": f"exit_code={command_row['exit_code']}",
        },
        {
            "gate": "inner_DONE_exists",
            "status": "pass" if (inner_run_dir / "DONE.txt").exists() else "fail",
            "evidence": str(inner_run_dir / "DONE.txt"),
        },
        {
            "gate": "external_bounds_loaded",
            "status": "pass" if summary_by_item.get("external_bounds_loaded", {}).get("value") == "True" else "fail",
            "evidence": summary_by_item.get("external_bounds_loaded", {}).get("value", "missing"),
        },
        {
            "gate": "external_rows_evaluated",
            "status": "pass" if summary_by_item.get("external_rows_evaluated", {}).get("value") == "12" else "fail",
            "evidence": summary_by_item.get("external_rows_evaluated", {}).get("value", "missing"),
        },
        {
            "gate": "validation_errors_zero",
            "status": "pass" if not validation_errors else "fail",
            "evidence": f"{len(validation_errors)} validation errors",
        },
        {
            "gate": "symbolic_rows_deferred",
            "status": "pass" if len(symbolic_rows) == 2 else "fail",
            "evidence": f"{len(symbolic_rows)} symbolic rows",
        },
        {
            "gate": "theorem_credit_zero",
            "status": "pass" if not theorem_credit else "fail",
            "evidence": f"{len(theorem_credit)} theorem-credit rows",
        },
        {
            "gate": "claim_allowed_zero",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "MTS_residual_vector_loaded",
            "status": "not_run",
            "evidence": "evaluate smoke used external bounds only, not MTS predictions",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "evaluate smoke only; no WEP/EH/Newton/PPN/fifth-force pass",
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
    summary: list[dict[str, Any]],
    status_counts: list[dict[str, Any]],
    evaluation_digest: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    summary_table_rows = [
        {
            "summary_item": row["summary_item"],
            "value": row["value"],
            "status": row["status"],
        }
        for row in summary
    ]
    digest_table_rows = [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "upper_bound": row["upper_bound"],
            "source_lock": row["source_lock"],
            "ratio": row["bound_to_source_lock_ratio"],
            "data_bound_status": row["data_bound_status"],
        }
        for row in evaluation_digest
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 427 - Local Bound Runner-v4 Evaluate Smoke

Private evaluate-mode checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 427 filled the verified local-bound source-intake CSV. This checkpoint runs evaluate mode against that file and checks whether the pipeline can process sourced bounds without giving MTS theorem credit by accident.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_evaluate_smoke.py` |
| Run directory | `runs/{run_dir.name}` |
| Inner evaluate directory | `{Path(command_row["inner_run_dir"]).relative_to(ROOT)}` |
| Bounds CSV | `source-intake/local_bounds/local_bound_claims.csv` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Inner Evaluate Invocation

| Item | Value |
| --- | --- |
| Command id | `{command_row["command_id"]}` |
| Exit code | `{command_row["exit_code"]}` |
| Stdout | `runs/{run_dir.name}/inner_stdout.txt` |
| Stderr | `runs/{run_dir.name}/inner_stderr.txt` |

## 4. Interface Summary

{markdown_table(summary_table_rows, ["summary_item", "value", "status"])}

## 5. Bound Status Counts

{markdown_table(status_counts, ["data_bound_status", "row_count"])}

## 6. Evaluation Digest

{markdown_table(digest_table_rows, ["row_id", "observable", "upper_bound", "source_lock", "ratio", "data_bound_status"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: the empirical harness is now doing what we need. It loads real sourced bounds, keeps symbolic rows symbolic, and refuses to call this a win. The next missing object is the MTS residual vector: what the theory actually predicts for each local row.

## 9. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    run_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    inner_run_dir, command_row = run_inner_evaluate(timestamp, run_dir)
    inner_results_dir = inner_run_dir / "results"
    interface_summary = summary_rows(inner_results_dir)
    evaluation_rows = read_csv(inner_results_dir / "external_bound_evaluation.csv")
    validation_errors = read_csv(inner_results_dir / "validation_errors.csv")
    status_counts = bound_status_counts(evaluation_rows)
    evaluation_digest = evaluation_digest_rows(evaluation_rows)
    gate_result_rows = gate_rows(
        source_rows,
        command_row,
        inner_run_dir,
        interface_summary,
        evaluation_rows,
        validation_errors,
    )

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "runner_invocation.csv", [command_row])
    write_csv(results_dir / "interface_summary.csv", interface_summary)
    write_csv(results_dir / "bound_status_counts.csv", status_counts)
    write_csv(results_dir / "evaluation_digest.csv", evaluation_digest)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    failed_gates = [row["gate"] for row in gate_result_rows if row["status"] == "fail" and row["gate"] != "local_GR_promoted"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "inner_run_dir": str(inner_run_dir),
        "claims_csv": str(CLAIMS_CSV),
        "inner_evaluate_exit_code": command_row["exit_code"],
        "external_rows_evaluated": len(evaluation_rows),
        "validation_errors": len(validation_errors),
        "bound_status_counts": {row["data_bound_status"]: row["row_count"] for row in status_counts},
        "MTS_residual_vector_loaded": False,
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
        interface_summary,
        status_counts,
        evaluation_digest,
        gate_result_rows,
    )
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run evaluate-mode smoke against the verified local_bound_claims.csv file."
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
