#!/usr/bin/env python3
"""Checkpoint 181: verify CMB engine readiness and dry-run wrapper behavior."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from cmb_kill_screen_long_run import engine_readiness_rows, run_from_config


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CMB_DECISION_RUN = RUNS_ROOT / "20260531-235959-CMB-kill-screen-or-parent-amplitude-owner-decision"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
CONFIG_DIR = CMB_CONTRACT_RUN / "configs"
STATUS_PASS = "CMB_engine_readiness_wrapper_written_dryruns_fail_clean_missing_engine"
CLAIM_CEILING = "engine_readiness_and_dryrun_only_no_spectra_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 181 wrapper readiness script"),
        (WORK_DIR / "180-CMB-kill-screen-or-parent-amplitude-owner-decision.md", "route decision"),
        (CMB_DECISION_RUN / "status.json", "route decision machine status"),
        (WORK_DIR / "151-CMB-kill-screen-runner-contract.md", "CMB kill-screen contract"),
        (CMB_CONTRACT_RUN / "status.json", "CMB kill-screen contract status"),
        (SCRIPT_DIR / "cmb_kill_screen_long_run.py", "new dry-run long-run wrapper"),
        (CONFIG_DIR / "LCDM_baseline_reproduction.blueprint.json", "baseline blueprint"),
        (CONFIG_DIR / "MTS_exact_auxiliary_transfer_locked.blueprint.json", "exact auxiliary blueprint"),
        (CONFIG_DIR / "MTS_high_cs_transfer_locked.blueprint.json", "high-cs blueprint"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def config_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(CONFIG_DIR.glob("*.blueprint.json")):
        config = load_json(path)
        rows.append(
            {
                "config_id": config.get("config_id", path.stem),
                "path": str(path),
                "model": config.get("model", ""),
                "closure_mode": config.get("closure_mode", ""),
                "engine": config.get("engine", ""),
                "claim_ceiling": config.get("claim_ceiling", ""),
                "dry_run_blueprint_only": config.get("dry_run_blueprint_only", ""),
            }
        )
    return rows


def dry_run_summary_rows(dry_run_dirs: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_dir in dry_run_dirs:
        status = load_json(run_dir / "status.json")
        marker = "DONE.txt" if (run_dir / "DONE.txt").exists() else ("FAILED.txt" if (run_dir / "FAILED.txt").exists() else "")
        rows.append(
            {
                "config_id": status.get("config_id", ""),
                "dry_run_dir": str(run_dir),
                "status": status.get("status", ""),
                "engine_available": status.get("engine_available", ""),
                "blueprint_valid": status.get("blueprint_valid", ""),
                "output_contract_valid": status.get("output_contract_valid", ""),
                "spectra_run_performed": status.get("spectra_run_performed", ""),
                "marker": marker,
                "reason": status.get("reason", ""),
            }
        )
    return rows


def lock_audit_summary_rows(dry_run_dirs: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_dir in dry_run_dirs:
        status = load_json(run_dir / "status.json")
        for row in read_csv_rows(run_dir / "results" / "blueprint_lock_audit.csv"):
            rows.append(
                {
                    "config_id": status.get("config_id", ""),
                    "check": row["check"],
                    "status": row["status"],
                    "evidence": row["evidence"],
                }
            )
    return rows


def launch_command_rows(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wrapper = WORK_DIR / "scripts" / "cmb_kill_screen_long_run.py"
    rows: list[dict[str, Any]] = []
    for row in configs:
        rows.append(
            {
                "config_id": row["config_id"],
                "dry_run_command": f'& ".venv-score\\Scripts\\python.exe" "scripts\\cmb_kill_screen_long_run.py" --config "{row["path"]}" --dry-run',
                "long_run_command": f'& ".venv-score\\Scripts\\python.exe" "scripts\\cmb_kill_screen_long_run.py" --config "{row["path"]}"',
                "allowed_now": "dry_run_only",
                "wrapper_path": str(wrapper),
            }
        )
    return rows


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    engines: list[dict[str, Any]],
    dry_runs: list[dict[str, Any]],
    lock_audits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    engine_available = any(row["available"] == "yes" for row in engines if row["engine_or_tool"] in {"camb_python_module", "classy_python_module", "class_executable"})
    spectra_runs = [row for row in dry_runs if str(row["spectra_run_performed"]).lower() == "true"]
    bad_locks = [row for row in lock_audits if row["status"] != "pass"]
    bad_contracts = [row for row in dry_runs if str(row["blueprint_valid"]).lower() != "true" or str(row["output_contract_valid"]).lower() != "true"]
    clean_missing_engine_blocks = [
        row
        for row in dry_runs
        if row["status"] == "dry_run_blocked_missing_engine_no_spectra_run" and row["marker"] == "FAILED.txt"
    ]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all registered paths found" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "wrapper_exists",
            "status": "pass",
            "evidence": str(SCRIPT_DIR / "cmb_kill_screen_long_run.py"),
        },
        {
            "gate": "blueprints_valid_and_locked",
            "status": "pass" if not bad_locks and not bad_contracts else "fail",
            "evidence": f"bad_locks={len(bad_locks)}; bad_contracts={len(bad_contracts)}",
        },
        {
            "gate": "engine_readiness_known",
            "status": "pass",
            "evidence": "engine_available=yes" if engine_available else "engine_available=no",
        },
        {
            "gate": "missing_engine_fails_cleanly",
            "status": "pass" if engine_available or len(clean_missing_engine_blocks) == len(dry_runs) else "fail",
            "evidence": f"clean_missing_engine_blocks={len(clean_missing_engine_blocks)} of {len(dry_runs)}",
        },
        {
            "gate": "no_spectra_run_performed",
            "status": "pass" if not spectra_runs else "fail",
            "evidence": f"spectra_runs={len(spectra_runs)}",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(engines: list[dict[str, Any]], dry_runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    engine_available = any(row["available"] == "yes" for row in engines if row["engine_or_tool"] in {"camb_python_module", "classy_python_module", "class_executable"})
    if engine_available:
        status = "CMB_engine_available_dryruns_ready_no_spectra_run"
        next_target = "182-LCDM-baseline-reproduction-dry-run.md"
        next_evidence = "connect selected engine to baseline reproduction before MTS interpretation"
    else:
        status = STATUS_PASS
        next_target = "182-CMB-engine-install-or-external-run-plan.md"
        next_evidence = "choose/install CLASS or CAMB, then rerun dry-run wrapper"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"dry_runs={len(dry_runs)}; engine_available={engine_available}",
        },
        {
            "item": "wrapper_status",
            "verdict": "written_and_dryrun_tested",
            "evidence": "scripts/cmb_kill_screen_long_run.py",
        },
        {
            "item": "spectra_run_performed",
            "verdict": False,
            "evidence": "readiness/dry-run only",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "no CMB spectra, no baseline reproduction, no likelihood score",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "engine readiness and dry-run only",
        },
        {
            "item": "next_target",
            "verdict": next_target,
            "evidence": next_evidence,
        },
    ]


def run_checkpoint(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-CMB-engine-readiness-and-dryrun-wrapper"
    results_dir = run_dir / "results"
    dry_root = run_dir / "dry-runs"
    results_dir.mkdir(parents=True, exist_ok=True)
    dry_root.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    configs = config_manifest_rows()
    dry_run_dirs = [
        run_from_config(Path(row["path"]), output_root=dry_root, timestamp=run_stamp, dry_run=True)
        for row in configs
    ]
    engines = engine_readiness_rows()
    dry_runs = dry_run_summary_rows(dry_run_dirs)
    lock_audits = lock_audit_summary_rows(dry_run_dirs)
    launch_commands = launch_command_rows(configs)
    gates = acceptance_gate_rows(sources, engines, dry_runs, lock_audits)
    decisions = decision_rows(engines, dry_runs)
    status_value = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "purpose": "verify CMB engine readiness and dry-run wrapper behavior without spectra execution",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "engine_preflight.csv", engines, ["engine_or_tool", "available", "version_or_path", "role"])
    write_csv(
        results_dir / "config_manifest.csv",
        configs,
        ["config_id", "path", "model", "closure_mode", "engine", "claim_ceiling", "dry_run_blueprint_only"],
    )
    write_csv(
        results_dir / "dry_run_summary.csv",
        dry_runs,
        ["config_id", "dry_run_dir", "status", "engine_available", "blueprint_valid", "output_contract_valid", "spectra_run_performed", "marker", "reason"],
    )
    write_csv(results_dir / "lock_audit_summary.csv", lock_audits, ["config_id", "check", "status", "evidence"])
    write_csv(results_dir / "launch_commands.csv", launch_commands, ["config_id", "dry_run_command", "long_run_command", "allowed_now", "wrapper_path"])
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    write_json(
        run_dir / "status.json",
        {
            "status": status_value,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "spectra_run_performed": False,
            "promotion_allowed": False,
            "dry_run_count": len(dry_runs),
            "engine_available": any(row["available"] == "yes" for row in engines if row["engine_or_tool"] in {"camb_python_module", "classy_python_module", "class_executable"}),
            "generated": [
                "source_register.csv",
                "engine_preflight.csv",
                "config_manifest.csv",
                "dry_run_summary.csv",
                "lock_audit_summary.csv",
                "launch_commands.csv",
                "acceptance_gates.csv",
                "decision.csv",
            ],
            "next_target": decisions[-1]["verdict"],
        },
    )
    (run_dir / "DONE.txt").write_text(f"{status_value}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_checkpoint(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
