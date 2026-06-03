#!/usr/bin/env python3
"""Summarize the no-score cosmology preflight safe run."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_24_STATUS = Path("runs/20260530-235416-cosmology-preflight-execution-plan/status.json")
SAFE_RUN_ROOT = Path("runs/20260530-235530-cosmology-preflight-safe-run")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def status_rows(source_audit: dict[str, Any], parser_smoke: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "stage": "data_source_audit",
            "readout": source_audit.get("readout", ""),
            "data_fit_performed": source_audit.get("data_fit_performed", ""),
            "fit_allowed_now": source_audit.get("fit_allowed_now", ""),
            "claim_allowed": source_audit.get("public_claim_allowed", ""),
            "status_path": source_audit.get("outputs", {}).get("status_json", ""),
        },
        {
            "stage": "parser_smoke_no_score",
            "readout": parser_smoke.get("readout", ""),
            "data_fit_performed": parser_smoke.get("data_fit_performed", ""),
            "fit_allowed_now": parser_smoke.get("fit_allowed_now", ""),
            "claim_allowed": False,
            "status_path": parser_smoke.get("outputs", {}).get("status_json", ""),
        },
    ]


def gate_summary_rows(source_gates: list[dict[str, str]], parser_gates: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gate_row in source_gates:
        rows.append(
            {
                "stage": "data_source_audit",
                "gate": gate_row["criterion"],
                "status": gate_row["status"],
                "detail": gate_row["detail"],
            }
        )
    for gate_row in parser_gates:
        rows.append(
            {
                "stage": "parser_smoke_no_score",
                "gate": gate_row["criterion"],
                "status": gate_row["status"],
                "detail": gate_row["detail"],
            }
        )
    return rows


def parser_summary_rows(parser_smoke: dict[str, Any], covariance_checks: list[dict[str, str]]) -> list[dict[str, Any]]:
    passed_checks = sum(1 for row in covariance_checks if row.get("status") == "pass")
    failed_checks = sum(1 for row in covariance_checks if row.get("status") != "pass")
    return [
        {
            "metric": "inventory_rows",
            "value": parser_smoke.get("inventory_rows", ""),
            "status": "pass" if int(parser_smoke.get("inventory_rows", 0)) > 0 else "fail",
        },
        {
            "metric": "covariance_checks",
            "value": parser_smoke.get("covariance_checks", ""),
            "status": "pass" if failed_checks == 0 and passed_checks > 0 else "fail",
        },
        {
            "metric": "covariance_checks_passed",
            "value": passed_checks,
            "status": "pass",
        },
        {
            "metric": "covariance_checks_failed",
            "value": failed_checks,
            "status": "pass" if failed_checks == 0 else "fail",
        },
        {
            "metric": "forbidden_artifacts_found",
            "value": ";".join(parser_smoke.get("forbidden_artifacts_found", [])),
            "status": "pass" if not parser_smoke.get("forbidden_artifacts_found", []) else "fail",
        },
    ]


def decision_rows(source_audit: dict[str, Any], parser_smoke: dict[str, Any]) -> list[dict[str, Any]]:
    parser_passed = parser_smoke.get("readout") == "growth_CMB_parser_smoke_dry_run_passed_no_score"
    source_safe = source_audit.get("data_fit_performed") is False and source_audit.get("public_claim_allowed") is False
    return [
        {
            "decision": "safe_two_step_preflight",
            "status": "pass" if parser_passed and source_safe else "fail",
            "evidence": "source audit did no fit; parser smoke passed no-score covariance checks",
            "next_action": "do not score yet",
        },
        {
            "decision": "likelihood_preflight_chain",
            "status": "wrapper_needed",
            "evidence": "existing likelihood preflight reads legacy parser_162 rather than this new parser status",
            "next_action": "build isolated post-checkpoint likelihood wrapper or explicitly accept legacy contract check",
        },
        {
            "decision": "scoring_status",
            "status": "blocked",
            "evidence": "strict numeric locks and isolated preflight chain are still incomplete",
            "next_action": "lock branch numbers and dependency chain before first scoring",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cosmology preflight safe-run readout.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_24 = load_json(root / SOURCE_24_STATUS)
    safe_run_root = root / SAFE_RUN_ROOT
    source_audit = load_json(safe_run_root / "data-source-audit" / "status.json")
    parser_smoke = load_json(safe_run_root / "parser-smoke-no-score" / "status.json")
    source_gates = read_csv(safe_run_root / "data-source-audit" / "results" / "source_audit_gate_criteria.csv")
    parser_gates = read_csv(safe_run_root / "parser-smoke-no-score" / "results" / "parser_smoke_gate_criteria.csv")
    covariance_checks = read_csv(safe_run_root / "parser-smoke-no-score" / "results" / "covariance_shape_checks.csv")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-cosmology-preflight-safe-run-readout"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    statuses = status_rows(source_audit, parser_smoke)
    gates = gate_summary_rows(source_gates, parser_gates)
    parser_summary = parser_summary_rows(parser_smoke, covariance_checks)
    decisions = decision_rows(source_audit, parser_smoke)

    write_csv(results_dir / "safe_run_statuses.csv", statuses, list(statuses[0].keys()))
    write_csv(results_dir / "safe_run_gate_summary.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "parser_no_score_summary.csv", parser_summary, list(parser_summary[0].keys()))
    write_csv(results_dir / "safe_run_decision.csv", decisions, list(decisions[0].keys()))

    readout = "cosmology_preflight_safe_run_two_steps_passed_no_score_likelihood_wrapper_needed"
    status = {
        "status": "complete_cosmology_preflight_safe_run_readout",
        "readout": readout,
        "source_24_readout": source_24.get("readout", ""),
        "safe_run_root": str(safe_run_root),
        "data_source_audit_readout": source_audit.get("readout", ""),
        "parser_smoke_readout": parser_smoke.get("readout", ""),
        "commands_executed": ["data_source_audit", "parser_smoke_no_score"],
        "data_fit_performed": False,
        "fit_allowed_now": False,
        "scoring_run_allowed_now": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "L0_control",
        "next_target": "26-isolated-likelihood-preflight-wrapper.md",
        "outputs": {
            "safe_run_statuses": str(results_dir / "safe_run_statuses.csv"),
            "safe_run_gate_summary": str(results_dir / "safe_run_gate_summary.csv"),
            "parser_no_score_summary": str(results_dir / "parser_no_score_summary.csv"),
            "safe_run_decision": str(results_dir / "safe_run_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
