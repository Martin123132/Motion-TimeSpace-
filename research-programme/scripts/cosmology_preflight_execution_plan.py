#!/usr/bin/env python3
"""Generate a no-execution cosmology preflight command plan."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_23_STATUS = Path("runs/20260530-235043-strict-cosmology-branch-contract/status.json")
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SCRIPTS = {
    "data_source_audit": MAIN_WORKBENCH / "scripts" / "growth_CMB_data_source_audit.py",
    "parser_smoke_no_score": MAIN_WORKBENCH / "scripts" / "growth_CMB_parser_smoke_dry_run.py",
    "likelihood_preflight_no_score": MAIN_WORKBENCH / "scripts" / "growth_CMB_likelihood_preflight.py",
    "first_scoring_run": MAIN_WORKBENCH / "scripts" / "growth_CMB_first_scoring_run.py",
    "cosmology_likelihood_smoke": MAIN_WORKBENCH / "scripts" / "cosmology_likelihood_smoke.py",
}

CONFIGS = {
    "holdout_dry_run_config": MAIN_WORKBENCH
    / "runs"
    / "20260528-225042-growth-CMB-holdout-dry-run-design"
    / "results"
    / "holdout_dry_run_config.json",
}

LEGACY_STATUSES = {
    "parser_162": MAIN_WORKBENCH / "runs" / "20260528-225834-growth-CMB-parser-smoke-dry-run" / "status.json",
    "likelihood_163": MAIN_WORKBENCH / "runs" / "20260528-230239-growth-CMB-likelihood-preflight" / "status.json",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def try_load_readout(path: Path) -> str:
    if not path.exists():
        return "missing"
    try:
        return str(load_json(path).get("readout", "readout_missing"))
    except json.JSONDecodeError:
        return "invalid_json"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def quote_ps(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def source_availability_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SCRIPTS.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "kind": "script",
                "readout_or_note": "callable_by_python_if_dependencies_present",
            }
        )
    for source_id, path in CONFIGS.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "kind": "config",
                "readout_or_note": "required_for_parser_smoke_no_score",
            }
        )
    for source_id, path in LEGACY_STATUSES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "kind": "legacy_status",
                "readout_or_note": try_load_readout(path),
            }
        )
    return rows


def command_plan_rows(out_dir: Path) -> list[dict[str, Any]]:
    run_root = out_dir / "planned-runs"
    data_source_out = run_root / "growth-CMB-data-source-audit"
    parser_out = run_root / "growth-CMB-parser-smoke-dry-run"
    likelihood_out = run_root / "growth-CMB-likelihood-preflight"
    return [
        {
            "sequence": 1,
            "run_id": "data_source_audit",
            "allowed_now": True,
            "executes_score": False,
            "writes_to": str(data_source_out),
            "command": f"python {quote_ps(SCRIPTS['data_source_audit'])} --out-dir {quote_ps(data_source_out)}",
            "blocking_note": "audit only; no fit",
        },
        {
            "sequence": 2,
            "run_id": "parser_smoke_no_score",
            "allowed_now": True,
            "executes_score": False,
            "writes_to": str(parser_out),
            "command": (
                f"python {quote_ps(SCRIPTS['parser_smoke_no_score'])} "
                f"--config {quote_ps(CONFIGS['holdout_dry_run_config'])} "
                f"--out-dir {quote_ps(parser_out)} --no-score"
            ),
            "blocking_note": "requires holdout_dry_run_config.json; no-score flag is mandatory",
        },
        {
            "sequence": 3,
            "run_id": "likelihood_preflight_no_score",
            "allowed_now": "conditional_legacy_dependency",
            "executes_score": False,
            "writes_to": str(likelihood_out),
            "command": f"python {quote_ps(SCRIPTS['likelihood_preflight_no_score'])} --out-dir {quote_ps(likelihood_out)}",
            "blocking_note": "current script reads legacy parser_162 status; use as preflight contract only unless dependency is patched",
        },
        {
            "sequence": 4,
            "run_id": "first_scoring_run",
            "allowed_now": False,
            "executes_score": True,
            "writes_to": "blocked",
            "command": f"python {quote_ps(SCRIPTS['first_scoring_run'])}",
            "blocking_note": "blocked until strict numeric lock and preflight pass",
        },
        {
            "sequence": 5,
            "run_id": "cosmology_likelihood_smoke",
            "allowed_now": False,
            "executes_score": True,
            "writes_to": "blocked",
            "command": f"python {quote_ps(SCRIPTS['cosmology_likelihood_smoke'])}",
            "blocking_note": "blocked until same-test robust matrix is explicitly authorized",
        },
    ]


def strict_numeric_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "b_mem_pre",
            "needed_before_scoring": True,
            "current_action": "lock value/corridor before scoring or exclude strict_memory_predeclared",
            "status": "not_locked_here",
        },
        {
            "item": "F_pre(N)",
            "needed_before_scoring": True,
            "current_action": "lock exact shape before scoring or use strict_C0_frozen_holdout only",
            "status": "not_locked_here",
        },
        {
            "item": "activation_sign_branch",
            "needed_before_scoring": True,
            "current_action": "declare sign-free and sign-constrained branches before any run",
            "status": "not_locked_here",
        },
        {
            "item": "baseline_priors",
            "needed_before_scoring": True,
            "current_action": "copy identical priors/covariance rules for LCDM, wCDM, CPL, and MTS",
            "status": "not_locked_here",
        },
        {
            "item": "output_directory",
            "needed_before_scoring": True,
            "current_action": "all future preflight outputs must write under post-checkpoint planned-runs or a run-specific folder",
            "status": "locked_for_preflight_plan",
        },
    ]


def artifact_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "preflight_command_plan.csv",
            "purpose": "machine-readable command sequence",
            "must_not_contain": "any command marked allowed_now=false being executed",
        },
        {
            "artifact": "safe_preflight_commands.ps1",
            "purpose": "human-readable VS Code command script that prints commands only",
            "must_not_contain": "uncommented execution lines",
        },
        {
            "artifact": "strict_numeric_lock_needed.csv",
            "purpose": "list remaining choices before scoring",
            "must_not_contain": "post-hoc fitted values",
        },
        {
            "artifact": "preflight_gate_criteria.csv",
            "purpose": "pass/fail gate for whether commands may be run later",
            "must_not_contain": "empirical claim language",
        },
    ]


def gate_rows(source_23: dict[str, Any], availability: list[dict[str, Any]], commands: list[dict[str, Any]]) -> list[dict[str, Any]]:
    script_sources_exist = all(
        row["exists"] is True for row in availability if row["kind"] == "script" and row["source_id"] in {
            "data_source_audit",
            "parser_smoke_no_score",
            "likelihood_preflight_no_score",
        }
    )
    config_exists = any(
        row["source_id"] == "holdout_dry_run_config" and row["exists"] is True for row in availability
    )
    blocked_score_commands = all(
        row["allowed_now"] is False for row in commands if row["executes_score"] is True
    )
    return [
        {
            "gate": "source_23_complete",
            "status": "pass" if source_23.get("readout") == "strict_cosmology_branch_contract_locked_no_scoring_yet" else "fail",
            "detail": str(source_23.get("readout")),
        },
        {
            "gate": "preflight_scripts_exist",
            "status": "pass" if script_sources_exist else "fail",
            "detail": "data source audit, parser smoke, and likelihood preflight scripts checked",
        },
        {
            "gate": "parser_config_exists",
            "status": "pass" if config_exists else "fail",
            "detail": str(CONFIGS["holdout_dry_run_config"]),
        },
        {
            "gate": "score_commands_blocked",
            "status": "pass" if blocked_score_commands else "fail",
            "detail": "first scoring and cosmology smoke commands remain blocked",
        },
        {
            "gate": "commands_executed_by_this_stage",
            "status": "pass",
            "detail": "false; this stage writes command plan only",
        },
        {
            "gate": "legacy_dependency_flagged",
            "status": "pass",
            "detail": "likelihood preflight reads legacy parser_162 unless patched",
        },
        {
            "gate": "empirical_claim_allowed_now",
            "status": "fail",
            "detail": "no data scoring has occurred",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "preflight_plan_status",
            "status": "ready_to_review_or_execute_safe_steps",
            "evidence": "safe command plan generated; no scoring commands allowed",
            "next_action": "run data_source_audit and parser_smoke_no_score only if choosing to execute preflight",
        },
        {
            "decision": "likelihood_preflight_status",
            "status": "conditional_legacy_dependency",
            "evidence": "existing script points to legacy parser_162 status in formalization-workbench",
            "next_action": "use as a contract check or create an isolated post-checkpoint wrapper before claiming preflight continuity",
        },
        {
            "decision": "scoring_status",
            "status": "blocked",
            "evidence": "b_mem_pre/F_pre and same-test branch values are not numerically locked here",
            "next_action": "lock numeric branch values before any fit/score run",
        },
    ]


def write_safe_powershell(path: Path, commands: list[dict[str, Any]]) -> None:
    lines = [
        "# Auto-generated dry-run command list.",
        "# This file prints commands only. It does not execute them.",
        "$ErrorActionPreference = 'Stop'",
        "",
    ]
    for command_row in commands:
        lines.append(f"Write-Host ''")
        lines.append(f"Write-Host '--- {command_row['sequence']}: {command_row['run_id']} ---'")
        lines.append(f"Write-Host 'allowed_now={command_row['allowed_now']}; executes_score={command_row['executes_score']}'")
        lines.append(f"Write-Host @'")
        lines.append(str(command_row["command"]))
        lines.append("'@")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cosmology preflight execution plan.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_23 = load_json(POST_CHECKPOINT / SOURCE_23_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-cosmology-preflight-execution-plan"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    availability = source_availability_rows()
    commands = command_plan_rows(out_dir)
    numeric_locks = strict_numeric_lock_rows()
    artifact_contract = artifact_contract_rows()
    gates = gate_rows(source_23, availability, commands)
    decisions = decision_rows()

    write_csv(results_dir / "preflight_source_availability.csv", availability, list(availability[0].keys()))
    write_csv(results_dir / "preflight_command_plan.csv", commands, list(commands[0].keys()))
    write_csv(results_dir / "strict_numeric_lock_needed.csv", numeric_locks, list(numeric_locks[0].keys()))
    write_csv(results_dir / "preflight_artifact_contract.csv", artifact_contract, list(artifact_contract[0].keys()))
    write_csv(results_dir / "preflight_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "preflight_decision.csv", decisions, list(decisions[0].keys()))
    safe_ps1 = results_dir / "safe_preflight_commands.ps1"
    write_safe_powershell(safe_ps1, commands)

    readout = "cosmology_preflight_execution_plan_written_no_commands_executed"
    status = {
        "status": "complete_cosmology_preflight_execution_plan",
        "readout": readout,
        "recommendation": "execute_safe_preflight_steps_or_patch_isolated_likelihood_dependency_next",
        "next_target": "25-cosmology-preflight-safe-run-or-wrapper.md",
        "commands_executed": False,
        "preflight_allowed_now": True,
        "safe_steps_allowed_now": ["data_source_audit", "parser_smoke_no_score"],
        "conditional_step": "likelihood_preflight_no_score_uses_legacy_parser_162",
        "scoring_run_allowed_now": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "L0_control",
        "outputs": {
            "preflight_source_availability": str(results_dir / "preflight_source_availability.csv"),
            "preflight_command_plan": str(results_dir / "preflight_command_plan.csv"),
            "strict_numeric_lock_needed": str(results_dir / "strict_numeric_lock_needed.csv"),
            "preflight_artifact_contract": str(results_dir / "preflight_artifact_contract.csv"),
            "preflight_gate_criteria": str(results_dir / "preflight_gate_criteria.csv"),
            "preflight_decision": str(results_dir / "preflight_decision.csv"),
            "safe_preflight_commands": str(safe_ps1),
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
