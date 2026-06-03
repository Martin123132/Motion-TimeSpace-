#!/usr/bin/env python3
"""Dry-run-safe wrapper for future MTS CMB kill-screen runs.

This script deliberately does not fake spectra. In dry-run mode it validates the
blueprint, checks engine readiness, enforces locked MTS parameters, writes the
standard long-run status/log artifacts, and exits cleanly even when execution is
blocked by missing CMB tooling.
"""

from __future__ import annotations

import argparse
import csv
import importlib
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

SCHEMA = "MTS_CMB_KILL_SCREEN_BLUEPRINT_V1"
CLAIM_CEILING = "CMB_kill_screen_wrapper_no_spectra_without_engine_baseline"
EXPECTED_LOCKS = {
    "B_mem": 2.0 / 27.0,
    "p": 3.0,
    "u3": 0.25,
}
EXPECTED_NO_RESCUE_RULES = {
    "do_not_refit_B_mem",
    "do_not_refit_p_or_u3",
    "do_not_fit_c_s_eff",
    "do_not_fit_sigma_mem_or_slip",
    "log_calibration_branch_separately",
}
EXPECTED_LIKELIHOODS = {
    "temperature_TT",
    "polarization_TE_EE",
    "low_l",
    "lensing_phi_phi",
}
REQUIRED_OUTPUTS = [
    "baseline_reproduction.csv",
    "background_functions.csv",
    "spectra_TT_TE_EE.csv",
    "lensing_phi_phi.csv",
    "late_ISW_diagnostics.csv",
    "likelihood_scorecard.csv",
    "claim_gate_results.csv",
]


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


def timestamp_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in value).strip("-") or "unnamed"


def module_version(module_name: str) -> str:
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return ""
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:  # pragma: no cover - defensive runtime detail
        return f"import_error:{exc.__class__.__name__}"
    return str(getattr(module, "__version__", "available_unknown_version"))


def engine_readiness_rows() -> list[dict[str, Any]]:
    class_path = shutil.which("class")
    rows = [
        {
            "engine_or_tool": "camb_python_module",
            "available": "yes" if importlib.util.find_spec("camb") else "no",
            "version_or_path": module_version("camb"),
            "role": "CAMB spectra engine candidate",
        },
        {
            "engine_or_tool": "classy_python_module",
            "available": "yes" if importlib.util.find_spec("classy") else "no",
            "version_or_path": module_version("classy"),
            "role": "CLASS Python wrapper candidate",
        },
        {
            "engine_or_tool": "class_executable",
            "available": "yes" if class_path else "no",
            "version_or_path": class_path or "",
            "role": "standalone CLASS executable candidate",
        },
        {
            "engine_or_tool": "cobaya_python_module",
            "available": "yes" if importlib.util.find_spec("cobaya") else "no",
            "version_or_path": module_version("cobaya"),
            "role": "likelihood plumbing candidate",
        },
        {
            "engine_or_tool": "montepython_python_module",
            "available": "yes" if importlib.util.find_spec("montepython") else "no",
            "version_or_path": module_version("montepython"),
            "role": "CLASS likelihood plumbing candidate",
        },
    ]
    return rows


def engine_available(rows: list[dict[str, Any]]) -> bool:
    engine_names = {"camb_python_module", "classy_python_module", "class_executable"}
    return any(row["engine_or_tool"] in engine_names and row["available"] == "yes" for row in rows)


def blueprint_audit_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    fixed = config.get("fixed_mts_parameters", {})
    rules = set(config.get("no_rescue_rules", []))
    likelihoods = set(config.get("likelihood_blocks", []))
    rows: list[dict[str, Any]] = [
        {
            "check": "schema",
            "status": "pass" if config.get("schema") == SCHEMA else "fail",
            "evidence": str(config.get("schema", "")),
        },
        {
            "check": "claim_ceiling",
            "status": "pass" if "no_support_claim" in str(config.get("claim_ceiling", "")) else "fail",
            "evidence": str(config.get("claim_ceiling", "")),
        },
        {
            "check": "model_declared",
            "status": "pass" if config.get("model") else "fail",
            "evidence": str(config.get("model", "")),
        },
        {
            "check": "closure_mode_declared",
            "status": "pass" if config.get("closure_mode") else "fail",
            "evidence": str(config.get("closure_mode", "")),
        },
        {
            "check": "likelihood_blocks_complete",
            "status": "pass" if EXPECTED_LIKELIHOODS.issubset(likelihoods) else "fail",
            "evidence": ";".join(sorted(likelihoods)),
        },
        {
            "check": "no_rescue_rules_complete",
            "status": "pass" if EXPECTED_NO_RESCUE_RULES.issubset(rules) else "fail",
            "evidence": ";".join(sorted(rules)),
        },
    ]
    for key, expected in EXPECTED_LOCKS.items():
        actual = fixed.get(key)
        try:
            delta = abs(float(actual) - expected)
            status = "pass" if delta < 1.0e-12 else "fail"
        except Exception:
            delta = ""
            status = "fail"
        rows.append(
            {
                "check": f"lock_{key}",
                "status": status,
                "evidence": f"actual={actual}; expected={expected}; delta={delta}",
            }
        )
    return rows


def output_contract_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    output_contract = config.get("output_contract", {})
    configured_results = set(output_contract.get("results", []))
    rows = [
        {
            "artifact": "status.json",
            "required": "yes",
            "configured": str(output_contract.get("status_json", "")),
            "status": "pass" if output_contract.get("status_json") == "status.json" else "fail",
        },
        {
            "artifact": "log.txt",
            "required": "yes",
            "configured": str(output_contract.get("log", "")),
            "status": "pass" if output_contract.get("log") == "log.txt" else "fail",
        },
        {
            "artifact": "completion_marker",
            "required": "yes",
            "configured": str(output_contract.get("completion_marker", "")),
            "status": "pass" if output_contract.get("completion_marker") else "fail",
        },
    ]
    for artifact in REQUIRED_OUTPUTS:
        rows.append(
            {
                "artifact": artifact,
                "required": "yes",
                "configured": "yes" if artifact in configured_results else "no",
                "status": "pass" if artifact in configured_results else "fail",
            }
        )
    return rows


def not_run_placeholder_rows(artifact: str, reason: str) -> list[dict[str, Any]]:
    return [
        {
            "artifact": artifact,
            "status": "not_run",
            "reason": reason,
            "claim_allowed": "no",
        }
    ]


def claim_gate_rows(
    dry_run: bool,
    engine_ok: bool,
    blueprint_ok: bool,
    output_contract_ok: bool,
    long_run_requested: bool,
) -> list[dict[str, Any]]:
    return [
        {
            "gate": "dry_run_mode",
            "status": "pass" if dry_run else "fail",
            "evidence": "spectra execution is forbidden unless dry-run and engine/baseline gates are replaced by a real engine stage",
        },
        {
            "gate": "engine_available",
            "status": "pass" if engine_ok else "blocked",
            "evidence": "at least one of camb/classy/class executable is available" if engine_ok else "no camb/classy/class engine detected",
        },
        {
            "gate": "blueprint_valid",
            "status": "pass" if blueprint_ok else "fail",
            "evidence": "schema/locks/no-rescue rules validated",
        },
        {
            "gate": "output_contract_valid",
            "status": "pass" if output_contract_ok else "fail",
            "evidence": "required long-run artifacts declared",
        },
        {
            "gate": "spectra_run_performed",
            "status": "pass" if not long_run_requested else "fail",
            "evidence": "no spectra run was performed" if not long_run_requested else "long run requested before wrapper is connected to engine",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "evidence": "dry-run/readiness wrapper only",
        },
    ]


def run_from_config(
    config_path: Path,
    output_root: Path = RUNS_ROOT,
    timestamp: str | None = None,
    dry_run: bool = True,
) -> Path:
    config_path = config_path.resolve()
    config = load_json(config_path)
    config_id = safe_name(str(config.get("config_id", config_path.stem)))
    stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = "dry-run" if dry_run else "long-run-request"
    run_dir = output_root / f"{stamp}-cmb-kill-screen-{config_id}-{suffix}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.txt"

    def log(message: str) -> None:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{timestamp_now()} {message}\n")

    log(f"starting wrapper config={config_path} dry_run={dry_run}")

    engines = engine_readiness_rows()
    blueprint = blueprint_audit_rows(config)
    output_contract = output_contract_rows(config)
    engine_ok = engine_available(engines)
    blueprint_ok = all(row["status"] == "pass" for row in blueprint)
    output_contract_ok = all(row["status"] == "pass" for row in output_contract)
    long_run_requested = not dry_run
    reason = "blocked_missing_CMB_engine" if not engine_ok else "dry_run_only_no_spectra"
    if not dry_run:
        reason = "long_run_refused_wrapper_not_connected_to_engine"
    if not blueprint_ok:
        reason = "invalid_blueprint"
    if not output_contract_ok:
        reason = "invalid_output_contract"

    if dry_run and engine_ok and blueprint_ok and output_contract_ok:
        status_value = "dry_run_ready_engine_available_no_spectra_run"
        marker = "DONE.txt"
    elif dry_run and blueprint_ok and output_contract_ok:
        status_value = "dry_run_blocked_missing_engine_no_spectra_run"
        marker = "FAILED.txt"
    else:
        status_value = "dry_run_failed_contract_or_long_run_refused_no_spectra"
        marker = "FAILED.txt"

    write_json(
        run_dir / "run_config.json",
        {
            "config_path": str(config_path),
            "config": config,
            "dry_run": dry_run,
            "claim_ceiling": CLAIM_CEILING,
            "spectra_run_performed": False,
            "created_at_utc": timestamp_now(),
        },
    )
    write_csv(results_dir / "engine_readiness.csv", engines, ["engine_or_tool", "available", "version_or_path", "role"])
    write_csv(results_dir / "blueprint_lock_audit.csv", blueprint, ["check", "status", "evidence"])
    write_csv(results_dir / "output_contract_audit.csv", output_contract, ["artifact", "required", "configured", "status"])

    for artifact in REQUIRED_OUTPUTS:
        rows = not_run_placeholder_rows(artifact, reason)
        if artifact == "claim_gate_results.csv":
            rows = claim_gate_rows(dry_run, engine_ok, blueprint_ok, output_contract_ok, long_run_requested)
            write_csv(results_dir / artifact, rows, ["gate", "status", "evidence"])
        else:
            write_csv(results_dir / artifact, rows, ["artifact", "status", "reason", "claim_allowed"])

    write_json(
        run_dir / "engine_version.json",
        {
            "engines": engines,
            "engine_available": engine_ok,
            "spectra_engine_selected": "",
            "spectra_run_performed": False,
        },
    )
    write_json(
        run_dir / "status.json",
        {
            "status": status_value,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "config_path": str(config_path),
            "config_id": config_id,
            "dry_run": dry_run,
            "engine_available": engine_ok,
            "blueprint_valid": blueprint_ok,
            "output_contract_valid": output_contract_ok,
            "spectra_run_performed": False,
            "claim_ceiling": CLAIM_CEILING,
            "reason": reason,
            "promotion_allowed": False,
            "next_action": "install_or_configure_CLASS_or_CAMB_then_rerun_dry_run" if not engine_ok else "connect_engine_and_baseline_reproduction_before_long_run",
        },
    )
    (run_dir / marker).write_text(f"{status_value}\n", encoding="utf-8")
    log(f"finished status={status_value} reason={reason}")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_from_config(args.config, args.output_root, args.timestamp, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
