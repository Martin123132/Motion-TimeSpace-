#!/usr/bin/env python3
"""Checkpoint 182: install/use a local CMB engine route or write external handoff."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from cmb_kill_screen_long_run import engine_readiness_rows, run_from_config


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_181_RUN = RUNS_ROOT / "20260531-235959-CMB-engine-readiness-and-dryrun-wrapper"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
CONFIG_DIR = CMB_CONTRACT_RUN / "configs"
STATUS_CAMB_READY = "CMB_CAMB_engine_installed_dryruns_ready_no_spectra_run"
STATUS_EXTERNAL_PLAN = "CMB_engine_missing_external_or_install_plan_written_no_spectra_run"
CLAIM_CEILING = "CMB_engine_install_readiness_no_spectra_no_CMB_claim"
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


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return ""


def package_origin(module_name: str) -> str:
    spec = importlib.util.find_spec(module_name)
    return str(spec.origin) if spec and spec.origin else ""


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 182 engine route script"),
        (WORK_DIR / "181-CMB-engine-readiness-and-dryrun-wrapper.md", "previous readiness checkpoint"),
        (CHECKPOINT_181_RUN / "status.json", "previous readiness machine status"),
        (SCRIPT_DIR / "cmb_kill_screen_long_run.py", "dry-run wrapper"),
        (WORK_DIR / "151-CMB-kill-screen-runner-contract.md", "CMB kill-screen contract"),
        (CMB_CONTRACT_RUN / "status.json", "CMB kill-screen contract status"),
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


def engine_install_manifest_rows() -> list[dict[str, Any]]:
    camb_available = importlib.util.find_spec("camb") is not None
    return [
        {
            "engine_route": "CAMB Python",
            "selected": "yes" if camb_available else "no",
            "package_or_binary": "camb",
            "installed": "yes" if camb_available else "no",
            "version": package_version("camb"),
            "origin_or_path": package_origin("camb"),
            "install_or_handoff_command": "python -m pip install camb",
            "status": "ready_for_dry_run" if camb_available else "missing",
        },
        {
            "engine_route": "CLASS Python wrapper",
            "selected": "no",
            "package_or_binary": "classy",
            "installed": "yes" if importlib.util.find_spec("classy") else "no",
            "version": package_version("classy"),
            "origin_or_path": package_origin("classy"),
            "install_or_handoff_command": "deferred",
            "status": "not_selected",
        },
        {
            "engine_route": "CLASS executable",
            "selected": "no",
            "package_or_binary": "class",
            "installed": "yes" if shutil.which("class") else "no",
            "version": "",
            "origin_or_path": shutil.which("class") or "",
            "install_or_handoff_command": "deferred",
            "status": "not_selected",
        },
        {
            "engine_route": "external machine/handoff",
            "selected": "no" if camb_available else "fallback",
            "package_or_binary": "external CLASS/CAMB",
            "installed": "not_applicable",
            "version": "",
            "origin_or_path": "",
            "install_or_handoff_command": "export configs and run wrapper-compatible command externally",
            "status": "fallback_if_local_engine_unavailable" if not camb_available else "not_needed_now",
        },
    ]


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


def baseline_next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "baseline_engine_smoke",
            "artifact": "183-LCDM-baseline-reproduction-dry-run.md",
            "requirement": "call CAMB on a tiny LCDM spectra calculation and write status/log/results without interpreting MTS",
            "claim_limit": "pipeline smoke only",
        },
        {
            "step": "baseline_reference_choice",
            "artifact": "baseline_reference_contract.csv",
            "requirement": "choose exact baseline parameter vector and reference score target before MTS branch is read",
            "claim_limit": "baseline parity only",
        },
        {
            "step": "MTS_branch_block",
            "artifact": "claim_gate_results.csv",
            "requirement": "MTS branches remain blocked until LCDM baseline smoke passes",
            "claim_limit": "no MTS CMB result yet",
        },
        {
            "step": "long_run_guard",
            "artifact": "status.json plus DONE/FAILED marker",
            "requirement": "any future spectra run must be launched and inspected via files, not watched for hours",
            "claim_limit": "private kill-screen only",
        },
    ]


def launch_command_rows(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in configs:
        rows.append(
            {
                "config_id": row["config_id"],
                "dry_run_command": f'& ".venv-score\\Scripts\\python.exe" "scripts\\cmb_kill_screen_long_run.py" --config "{row["path"]}" --dry-run',
                "future_long_run_command": f'& ".venv-score\\Scripts\\python.exe" "scripts\\cmb_kill_screen_long_run.py" --config "{row["path"]}"',
                "allowed_now": "dry_run_only_until_baseline_reproduction_passes",
            }
        )
    return rows


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    engines: list[dict[str, Any]],
    dry_runs: list[dict[str, Any]],
    locks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    camb_ready = any(row["engine_or_tool"] == "camb_python_module" and row["available"] == "yes" for row in engines)
    dry_run_failures = [row for row in dry_runs if row["status"] != "dry_run_ready_engine_available_no_spectra_run"]
    spectra_runs = [row for row in dry_runs if str(row["spectra_run_performed"]).lower() == "true"]
    bad_locks = [row for row in locks if row["status"] != "pass"]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all registered paths found" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "CAMB_engine_available",
            "status": "pass" if camb_ready else "fail",
            "evidence": "camb import detected" if camb_ready else "camb missing",
        },
        {
            "gate": "all_blueprint_dryruns_ready",
            "status": "pass" if not dry_run_failures else "fail",
            "evidence": f"dry_run_failures={len(dry_run_failures)}",
        },
        {
            "gate": "locks_preserved",
            "status": "pass" if not bad_locks else "fail",
            "evidence": f"bad_locks={len(bad_locks)}",
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
    camb_row = next(row for row in engines if row["engine_or_tool"] == "camb_python_module")
    camb_ready = camb_row["available"] == "yes"
    all_ready = all(row["status"] == "dry_run_ready_engine_available_no_spectra_run" for row in dry_runs)
    status = STATUS_CAMB_READY if camb_ready and all_ready else STATUS_EXTERNAL_PLAN
    next_target = "183-LCDM-baseline-reproduction-dry-run.md" if camb_ready and all_ready else "182b-CMB-external-run-handoff.md"
    next_evidence = "CAMB is importable and all blueprints dry-run ready" if camb_ready and all_ready else "local engine still unavailable or dry-runs failed"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": next_evidence,
        },
        {
            "item": "selected_engine_route",
            "verdict": "CAMB Python" if camb_ready else "external_or_install_required",
            "evidence": f"camb_available={camb_ready}; version={camb_row['version_or_path']}",
        },
        {
            "item": "dry_run_readiness",
            "verdict": all_ready,
            "evidence": f"dry_runs={len(dry_runs)}",
        },
        {
            "item": "spectra_run_performed",
            "verdict": False,
            "evidence": "dry-run readiness only",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "no spectra, no baseline reproduction, no likelihood score",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "engine install/readiness only",
        },
        {
            "item": "next_target",
            "verdict": next_target,
            "evidence": next_evidence,
        },
    ]


def run_checkpoint(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-CMB-engine-install-or-external-run-plan"
    results_dir = run_dir / "results"
    dry_root = run_dir / "dry-runs"
    results_dir.mkdir(parents=True, exist_ok=True)
    dry_root.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    install_manifest = engine_install_manifest_rows()
    configs = config_manifest_rows()
    dry_run_dirs = [
        run_from_config(Path(row["path"]), output_root=dry_root, timestamp=run_stamp, dry_run=True)
        for row in configs
    ]
    engines = engine_readiness_rows()
    dry_runs = dry_run_summary_rows(dry_run_dirs)
    locks = lock_audit_summary_rows(dry_run_dirs)
    baseline_contract = baseline_next_contract_rows()
    launch_commands = launch_command_rows(configs)
    gates = acceptance_gate_rows(sources, engines, dry_runs, locks)
    decisions = decision_rows(engines, dry_runs)
    status_value = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "purpose": "record CMB engine install/use route and rerun dry-run wrapper without spectra",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "engine_install_manifest.csv",
        install_manifest,
        ["engine_route", "selected", "package_or_binary", "installed", "version", "origin_or_path", "install_or_handoff_command", "status"],
    )
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
    write_csv(results_dir / "lock_audit_summary.csv", locks, ["config_id", "check", "status", "evidence"])
    write_csv(results_dir / "baseline_reproduction_next_contract.csv", baseline_contract, ["step", "artifact", "requirement", "claim_limit"])
    write_csv(results_dir / "launch_commands.csv", launch_commands, ["config_id", "dry_run_command", "future_long_run_command", "allowed_now"])
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
            "selected_engine_route": decisions[1]["verdict"],
            "dry_run_count": len(dry_runs),
            "spectra_run_performed": False,
            "promotion_allowed": False,
            "generated": [
                "source_register.csv",
                "engine_install_manifest.csv",
                "engine_preflight.csv",
                "config_manifest.csv",
                "dry_run_summary.csv",
                "lock_audit_summary.csv",
                "baseline_reproduction_next_contract.csv",
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
