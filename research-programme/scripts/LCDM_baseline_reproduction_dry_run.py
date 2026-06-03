#!/usr/bin/env python3
"""Checkpoint 183: tiny CAMB LCDM baseline spectra smoke before any MTS CMB read."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import camb
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_182_RUN = RUNS_ROOT / "20260531-235959-CMB-engine-install-or-external-run-plan"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
LCDM_BLUEPRINT = CMB_CONTRACT_RUN / "configs" / "LCDM_baseline_reproduction.blueprint.json"
STATUS_PASS = "LCDM_CAMB_baseline_smoke_passed_no_MTS_CMB_read"
STATUS_FAIL = "LCDM_CAMB_baseline_smoke_failed_no_MTS_CMB_read"
CLAIM_CEILING = "LCDM_baseline_smoke_only_no_MTS_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

BASELINE_PARAMS = {
    "H0": 67.5,
    "ombh2": 0.02237,
    "omch2": 0.1200,
    "tau": 0.0544,
    "As": 2.1e-9,
    "ns": 0.965,
    "mnu": 0.06,
    "omk": 0.0,
}
LMAX = 200
SAMPLE_ELLS = [2, 10, 50, 100, 150, 200]


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


def timestamp_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 183 LCDM baseline smoke script"),
        (WORK_DIR / "182-CMB-engine-install-or-external-run-plan.md", "CAMB engine readiness checkpoint"),
        (CHECKPOINT_182_RUN / "status.json", "CAMB engine readiness machine status"),
        (SCRIPT_DIR / "cmb_kill_screen_long_run.py", "dry-run wrapper"),
        (WORK_DIR / "151-CMB-kill-screen-runner-contract.md", "CMB kill-screen contract"),
        (LCDM_BLUEPRINT, "LCDM baseline blueprint"),
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


def baseline_parameter_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": key,
            "value": value,
            "source": "fixed LCDM CAMB smoke baseline",
            "claim_limit": "pipeline smoke; not an optimized Planck likelihood vector",
        }
        for key, value in BASELINE_PARAMS.items()
    ]


def run_camb_baseline() -> tuple[Any, dict[str, np.ndarray], dict[str, float], float]:
    start = datetime.now(timezone.utc)
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=BASELINE_PARAMS["H0"],
        ombh2=BASELINE_PARAMS["ombh2"],
        omch2=BASELINE_PARAMS["omch2"],
        tau=BASELINE_PARAMS["tau"],
        mnu=BASELINE_PARAMS["mnu"],
        omk=BASELINE_PARAMS["omk"],
    )
    params.InitPower.set_params(As=BASELINE_PARAMS["As"], ns=BASELINE_PARAMS["ns"])
    params.set_for_lmax(LMAX, lens_potential_accuracy=0)
    results = camb.get_results(params)
    powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
    derived = results.get_derived_params()
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    return results, powers, {key: float(value) for key, value in derived.items()}, elapsed


def spectra_rows(powers: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    total = powers["total"]
    rows: list[dict[str, Any]] = []
    for ell in SAMPLE_ELLS:
        rows.append(
            {
                "ell": ell,
                "TT_Dl_uK2": float(total[ell, 0]),
                "EE_Dl_uK2": float(total[ell, 1]),
                "BB_Dl_uK2": float(total[ell, 2]),
                "TE_Dl_uK2": float(total[ell, 3]),
                "source": "CAMB total lensed CMB power spectra",
            }
        )
    return rows


def background_rows(derived: dict[str, float]) -> list[dict[str, Any]]:
    keys = ["age", "zstar", "rstar", "thetastar", "DAstar", "zdrag", "rdrag", "zeq", "keq"]
    return [
        {
            "quantity": key,
            "value": derived.get(key, ""),
            "source": "CAMB derived parameter",
            "claim_limit": "baseline smoke diagnostic",
        }
        for key in keys
    ]


def baseline_reproduction_rows(
    spectra: list[dict[str, Any]],
    derived: dict[str, float],
    elapsed_seconds: float,
) -> list[dict[str, Any]]:
    tt_values = [float(row["TT_Dl_uK2"]) for row in spectra]
    ee_values = [float(row["EE_Dl_uK2"]) for row in spectra]
    finite_spectra = all(math.isfinite(value) for row in spectra for value in [float(row["TT_Dl_uK2"]), float(row["EE_Dl_uK2"]), float(row["TE_Dl_uK2"])])
    positive_tt = all(value > 0.0 for value in tt_values)
    nonnegative_ee = all(value >= 0.0 for value in ee_values)
    zstar_ok = 1000.0 < float(derived.get("zstar", 0.0)) < 1200.0
    rdrag_ok = 130.0 < float(derived.get("rdrag", 0.0)) < 160.0
    age_ok = 12.0 < float(derived.get("age", 0.0)) < 15.0
    return [
        {
            "check": "CAMB_import",
            "status": "pass",
            "value": package_version("camb"),
            "acceptance": "CAMB version detected",
        },
        {
            "check": "runtime_seconds",
            "status": "pass" if elapsed_seconds < 60.0 else "check",
            "value": elapsed_seconds,
            "acceptance": "tiny smoke should finish quickly",
        },
        {
            "check": "finite_sample_spectra",
            "status": "pass" if finite_spectra else "fail",
            "value": finite_spectra,
            "acceptance": "TT/EE/TE sample rows finite",
        },
        {
            "check": "positive_TT",
            "status": "pass" if positive_tt else "fail",
            "value": min(tt_values),
            "acceptance": "sample TT Dl values positive",
        },
        {
            "check": "nonnegative_EE",
            "status": "pass" if nonnegative_ee else "fail",
            "value": min(ee_values),
            "acceptance": "sample EE Dl values nonnegative",
        },
        {
            "check": "zstar_sanity",
            "status": "pass" if zstar_ok else "fail",
            "value": derived.get("zstar", ""),
            "acceptance": "1000 < zstar < 1200",
        },
        {
            "check": "rdrag_sanity",
            "status": "pass" if rdrag_ok else "fail",
            "value": derived.get("rdrag", ""),
            "acceptance": "130 < rdrag < 160 Mpc",
        },
        {
            "check": "age_sanity",
            "status": "pass" if age_ok else "fail",
            "value": derived.get("age", ""),
            "acceptance": "12 < age < 15 Gyr",
        },
    ]


def likelihood_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "likelihood": "not_run",
            "delta_chi2_vs_baseline": "",
            "status": "not_run",
            "claim_limit": "spectra smoke only; no official likelihood",
        },
        {
            "model": "MTS_locked_2over27",
            "likelihood": "blocked_until_LCDM_baseline_likelihood_exists",
            "delta_chi2_vs_baseline": "",
            "status": "blocked",
            "claim_limit": "MTS CMB branches not read in checkpoint 183",
        },
    ]


def claim_gate_rows(baseline_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in baseline_rows if row["status"] == "fail"]
    return [
        {
            "gate": "CAMB_baseline_smoke",
            "status": "pass" if not failed else "fail",
            "evidence": f"failed_baseline_checks={len(failed)}",
        },
        {
            "gate": "LCDM_baseline_before_MTS",
            "status": "pass",
            "evidence": "only LCDM CAMB smoke executed",
        },
        {
            "gate": "MTS_CMB_branch_read",
            "status": "blocked",
            "evidence": "MTS branches intentionally not executed before baseline smoke",
        },
        {
            "gate": "official_likelihood_run",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood used",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "evidence": "baseline smoke only",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    spectra: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    failed_baseline = [row for row in baseline_rows if row["status"] == "fail"]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all registered paths found" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "CAMB_spectra_generated",
            "status": "pass" if len(spectra) == len(SAMPLE_ELLS) else "fail",
            "evidence": f"sample_ells={len(spectra)}",
        },
        {
            "gate": "baseline_sanity_passed",
            "status": "pass" if not failed_baseline else "fail",
            "evidence": f"failed_baseline_checks={len(failed_baseline)}",
        },
        {
            "gate": "MTS_not_executed",
            "status": "pass",
            "evidence": "checkpoint 183 executes LCDM only",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(baseline_rows: list[dict[str, Any]], elapsed_seconds: float) -> list[dict[str, Any]]:
    failed = [row for row in baseline_rows if row["status"] == "fail"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_baseline_checks={len(failed)}; runtime_seconds={elapsed_seconds:.6g}",
        },
        {
            "item": "baseline_pipeline",
            "verdict": "CAMB_LCDM_smoke_passed" if not failed else "CAMB_LCDM_smoke_failed",
            "evidence": "tiny spectra and derived parameters produced",
        },
        {
            "item": "MTS_CMB_branch_status",
            "verdict": "blocked_not_read",
            "evidence": "baseline smoke only",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "no MTS CMB run and no official likelihood",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "LCDM baseline smoke only",
        },
        {
            "item": "next_target",
            "verdict": "184-MTS-CMB-background-injection-dry-run.md" if not failed else "183b-CAMB-baseline-smoke-repair.md",
            "evidence": "only after LCDM smoke passes may the fixed MTS background/closure be injected in dry-run form",
        },
    ]


def run_checkpoint(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-LCDM-baseline-reproduction-dry-run"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.txt"

    def log(message: str) -> None:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{timestamp_now()} {message}\n")

    log("starting LCDM CAMB baseline smoke")
    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    _, powers, derived, elapsed = run_camb_baseline()
    spectra = spectra_rows(powers)
    background = background_rows(derived)
    params = baseline_parameter_rows()
    baseline_checks = baseline_reproduction_rows(spectra, derived, elapsed)
    likelihood = likelihood_scorecard_rows()
    claim_gates = claim_gate_rows(baseline_checks)
    acceptance = acceptance_gate_rows(sources, baseline_checks, spectra)
    decisions = decision_rows(baseline_checks, elapsed)
    status_value = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "engine": "CAMB Python",
            "camb_version": package_version("camb"),
            "lmax": LMAX,
            "sample_ells": SAMPLE_ELLS,
            "baseline_params": BASELINE_PARAMS,
            "purpose": "tiny LCDM baseline spectra smoke before any MTS CMB read",
        },
    )
    write_json(
        run_dir / "engine_version.json",
        {
            "engine": "CAMB Python",
            "camb_version": package_version("camb"),
            "spectra_run_performed": True,
            "MTS_branch_executed": False,
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "baseline_parameter_vector.csv", params, ["parameter", "value", "source", "claim_limit"])
    write_csv(results_dir / "background_functions.csv", background, ["quantity", "value", "source", "claim_limit"])
    write_csv(results_dir / "spectra_TT_TE_EE.csv", spectra, ["ell", "TT_Dl_uK2", "EE_Dl_uK2", "BB_Dl_uK2", "TE_Dl_uK2", "source"])
    write_csv(results_dir / "baseline_reproduction.csv", baseline_checks, ["check", "status", "value", "acceptance"])
    write_csv(results_dir / "likelihood_scorecard.csv", likelihood, ["model", "likelihood", "delta_chi2_vs_baseline", "status", "claim_limit"])
    write_csv(results_dir / "claim_gate_results.csv", claim_gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "acceptance_gates.csv", acceptance, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    write_json(
        run_dir / "status.json",
        {
            "status": status_value,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "engine": "CAMB Python",
            "camb_version": package_version("camb"),
            "runtime_seconds": elapsed,
            "LCDM_baseline_smoke_executed": True,
            "MTS_CMB_branch_executed": False,
            "official_likelihood_run": False,
            "promotion_allowed": False,
            "generated": [
                "source_register.csv",
                "baseline_parameter_vector.csv",
                "background_functions.csv",
                "spectra_TT_TE_EE.csv",
                "baseline_reproduction.csv",
                "likelihood_scorecard.csv",
                "claim_gate_results.csv",
                "acceptance_gates.csv",
                "decision.csv",
            ],
            "next_target": decisions[-1]["verdict"],
        },
    )
    marker = "DONE.txt" if status_value == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status_value}\n", encoding="utf-8")
    log(f"finished status={status_value} runtime_seconds={elapsed:.6g}")
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
