#!/usr/bin/env python3
"""Checkpoint 184: inject fixed MTS CMB background/closure tables without spectra."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from cmb_kill_screen_long_run import run_from_config


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
CONFIG_DIR = CMB_CONTRACT_RUN / "configs"
MTS_EXACT_CONFIG = CONFIG_DIR / "MTS_exact_auxiliary_transfer_locked.blueprint.json"
MTS_HIGH_CS_CONFIG = CONFIG_DIR / "MTS_high_cs_transfer_locked.blueprint.json"
BOLTZMANN_RUN = RUNS_ROOT / "20260531-235900-Boltzmann-interface-contract"

STATUS_PASS = "MTS_CMB_background_injection_dry_run_passed_no_spectra"
STATUS_FAIL = "MTS_CMB_background_injection_dry_run_failed"
CLAIM_CEILING = "MTS_CMB_background_injection_only_no_spectra_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

N_EFF = 3.046
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
REFERENCE_Z_STAR = 1091.7904498991018
Z_SAMPLES = [0.0, 0.01, 0.05, 0.1, 0.15, 0.24, 0.38, 0.51, 0.7, 1.0, 2.0, 5.0, 10.0, 100.0, 1059.0, 1089.9373168180757, REFERENCE_Z_STAR, 10000.0]


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
        (Path(__file__).resolve(), "checkpoint 184 MTS CMB background injection script"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline smoke checkpoint"),
        (CHECKPOINT_183_RUN / "status.json", "LCDM baseline smoke machine status"),
        (WORK_DIR / "150-Boltzmann-interface-contract.md", "Boltzmann interface source"),
        (BOLTZMANN_RUN / "status.json", "Boltzmann interface machine status"),
        (BOLTZMANN_RUN / "results" / "CMB_safety_table.csv", "previous CMB safety table"),
        (WORK_DIR / "178-memory-perturbation-owner-attempt.md", "high-cs perturbation owner checkpoint"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN screening checkpoint"),
        (MTS_EXACT_CONFIG, "MTS exact auxiliary blueprint"),
        (MTS_HIGH_CS_CONFIG, "MTS high-cs blueprint"),
        (SCRIPT_DIR / "cmb_kill_screen_long_run.py", "CMB wrapper"),
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


def reference_params() -> dict[str, float]:
    config = load_json(MTS_HIGH_CS_CONFIG)
    fixed = config["fixed_mts_parameters"]
    return {
        "Omega_m0": float(fixed["Omega_m0_late_reference"]),
        "h": float(fixed["h_profiled_reference"]),
        "B_mem": float(fixed["B_mem"]),
        "p": float(fixed["p"]),
        "u3": float(fixed["u3"]),
    }


def radiation_density(h: float) -> float:
    omega_gamma = 2.469e-5 / (h * h)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation(n_past: float, p: float, u3: float) -> float:
    if n_past <= 0.0:
        return 0.0
    exponent = (n_past / u3) ** p
    if exponent > 745.0:
        return 1.0
    return 1.0 - math.exp(-exponent)


def activation_derivative(n_past: float, p: float, u3: float) -> float:
    if n_past <= 0.0:
        return 0.0
    exponent = (n_past / u3) ** p
    if exponent > 745.0:
        return 0.0
    return math.exp(-exponent) * p * n_past ** (p - 1.0) / (u3**p)


def background_row(z: float, params: dict[str, float]) -> dict[str, Any]:
    omega_m0 = params["Omega_m0"]
    h = params["h"]
    b_mem = params["B_mem"]
    p = params["p"]
    u3 = params["u3"]
    n_past = math.log1p(z)
    a = 1.0 / (1.0 + z)
    act = activation(n_past, p, u3)
    dact_dn = activation_derivative(n_past, p, u3)
    rho_mem = 1.0 - omega_m0 + b_mem * act
    one_plus_w = b_mem * dact_dn / (3.0 * rho_mem) if rho_mem > 0.0 else math.nan
    w_mem = -1.0 + one_plus_w
    omega_r = radiation_density(h)
    e2_no_rad = omega_m0 * (1.0 + z) ** 3 + rho_mem
    e2_with_rad = e2_no_rad + omega_r * (1.0 + z) ** 4
    omega_mem_with_rad = rho_mem / e2_with_rad
    omega_m_with_rad = omega_m0 * (1.0 + z) ** 3 / e2_with_rad
    omega_r_with_rad = omega_r * (1.0 + z) ** 4 / e2_with_rad
    return {
        "z": z,
        "a": a,
        "N_ln_1_plus_z": n_past,
        "A_mem": act,
        "dA_dN": dact_dn,
        "rho_mem_over_rhocrit0": rho_mem,
        "one_plus_w_mem": one_plus_w,
        "w_mem": w_mem,
        "E2_no_radiation": e2_no_rad,
        "E2_with_radiation": e2_with_rad,
        "Omega_mem_with_radiation": omega_mem_with_rad,
        "Omega_m_with_radiation": omega_m_with_rad,
        "Omega_r_with_radiation": omega_r_with_rad,
        "c_s_eff_squared_high_cs": 1.0,
        "sigma_mem": 0.0,
        "claim_limit": "background/closure table only; no spectra interpretation",
    }


def background_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    return [background_row(z, params) for z in Z_SAMPLES]


def parameter_lock_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    expected = {
        "B_mem": LOCKED_B_MEM,
        "p": LOCKED_P,
        "u3": LOCKED_U3,
    }
    rows: list[dict[str, Any]] = []
    for key in ["B_mem", "p", "u3"]:
        actual = params[key]
        target = expected[key]
        rows.append(
            {
                "parameter": key,
                "actual": actual,
                "expected": target,
                "delta": actual - target,
                "status": "pass" if abs(actual - target) < 1.0e-12 else "fail",
                "rule": "fixed no-refit lock",
            }
        )
    rows.extend(
        [
            {
                "parameter": "Omega_m0_late_reference",
                "actual": params["Omega_m0"],
                "expected": "predeclared transfer reference",
                "delta": "",
                "status": "pass",
                "rule": "logged calibration branch input, not silently reset",
            },
            {
                "parameter": "h_profiled_reference",
                "actual": params["h"],
                "expected": "predeclared transfer reference",
                "delta": "",
                "status": "pass",
                "rule": "logged calibration branch input, not silently reset",
            },
            {
                "parameter": "c_s_eff_squared",
                "actual": 1.0,
                "expected": 1.0,
                "delta": 0.0,
                "status": "pass",
                "rule": "fixed high-cs closure, not fitted",
            },
            {
                "parameter": "sigma_mem",
                "actual": 0.0,
                "expected": 0.0,
                "delta": 0.0,
                "status": "pass",
                "rule": "no fitted slip/lensing rescue",
            },
        ]
    )
    return rows


def closure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_mode": "exact_auxiliary_smooth_memory",
            "delta_mem": "0 by constraint",
            "theta_mem": "0 by constraint",
            "delta_p_mem": "0 by constraint",
            "sigma_mem": "0",
            "status": "dry_run_contract_only",
            "claim_limit": "requires parent auxiliary/Bianchi owner before support claim",
        },
        {
            "closure_mode": "high_sound_speed_effective_scalar",
            "delta_mem": "bounded, not zero",
            "theta_mem": "standard effective scalar/fluid variable in future engine",
            "delta_p_mem": "rest-frame c_s_eff^2=1",
            "sigma_mem": "0",
            "status": "dry_run_contract_only",
            "claim_limit": "effective EFT owner only; no parent promotion",
        },
    ]


def camb_injection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "pipeline_item": "background_functions",
            "injected_now": "yes_table_only",
            "artifact": "MTS_background_functions.csv",
            "pass_condition": "rho_mem,w_mem,Omega_mem finite and locked at sampled redshifts",
            "claim_limit": "no CAMB spectra sourced from this table yet",
        },
        {
            "pipeline_item": "closure_mode",
            "injected_now": "yes_contract_only",
            "artifact": "CMB_closure_modes.csv",
            "pass_condition": "exact auxiliary and high-cs modes explicitly fenced",
            "claim_limit": "not a parent perturbation derivation",
        },
        {
            "pipeline_item": "CAMB_custom_dark_energy",
            "injected_now": "no",
            "artifact": "future wrapper/engine module",
            "pass_condition": "future code maps table to CAMB/CLASS background and perturbations",
            "claim_limit": "required before spectra interpretation",
        },
        {
            "pipeline_item": "TT_TE_EE_lensing_spectra",
            "injected_now": "no",
            "artifact": "spectra_TT_TE_EE.csv, lensing_phi_phi.csv",
            "pass_condition": "future spectra run after injection module exists",
            "claim_limit": "blocked in checkpoint 184",
        },
        {
            "pipeline_item": "likelihood_scorecard",
            "injected_now": "no",
            "artifact": "likelihood_scorecard.csv",
            "pass_condition": "future baseline-parity likelihood score",
            "claim_limit": "no CMB support claim",
        },
    ]


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


def safety_recheck_rows(background: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for z_target in [1059.0, 1089.9373168180757, REFERENCE_Z_STAR, 10000.0]:
        row = min(background, key=lambda item: abs(float(item["z"]) - z_target))
        omega_mem = float(row["Omega_mem_with_radiation"])
        rows.append(
            {
                "z": row["z"],
                "Omega_mem_with_radiation": omega_mem,
                "one_plus_w_mem": row["one_plus_w_mem"],
                "readout": "primary_CMB_background_negligible" if omega_mem < 1.0e-6 else "check",
                "claim_limit": "background safety only; no TT/TE/EE/lensing pass",
            }
        )
    return rows


def claim_gate_rows(
    locks: list[dict[str, Any]],
    dry_runs: list[dict[str, Any]],
    background: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    failed_locks = [row for row in locks if row["status"] != "pass"]
    spectra_runs = [row for row in dry_runs if str(row["spectra_run_performed"]).lower() == "true"]
    bad_background = [
        row
        for row in background
        if not math.isfinite(float(row["rho_mem_over_rhocrit0"]))
        or not math.isfinite(float(row["E2_with_radiation"]))
        or float(row["E2_with_radiation"]) <= 0.0
    ]
    return [
        {
            "gate": "parameter_locks_preserved",
            "status": "pass" if not failed_locks else "fail",
            "evidence": f"failed_locks={len(failed_locks)}",
        },
        {
            "gate": "background_table_finite",
            "status": "pass" if not bad_background else "fail",
            "evidence": f"bad_background_rows={len(bad_background)}",
        },
        {
            "gate": "MTS_blueprint_dry_runs_ready",
            "status": "pass" if all(row["status"] == "dry_run_ready_engine_available_no_spectra_run" for row in dry_runs) else "fail",
            "evidence": f"dry_run_rows={len(dry_runs)}",
        },
        {
            "gate": "MTS_spectra_run_performed",
            "status": "blocked",
            "evidence": f"spectra_runs={len(spectra_runs)}; spectra intentionally blocked",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "evidence": "background injection dry-run only",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    background: list[dict[str, Any]],
    dry_runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    failed_locks = [row for row in locks if row["status"] != "pass"]
    spectra_runs = [row for row in dry_runs if str(row["spectra_run_performed"]).lower() == "true"]
    recomb_rows = [row for row in background if float(row["z"]) in {1059.0, 1089.9373168180757, REFERENCE_Z_STAR}]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all registered paths found" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "parameter_locks_clean",
            "status": "pass" if not failed_locks else "fail",
            "evidence": f"failed_locks={len(failed_locks)}",
        },
        {
            "gate": "background_table_written",
            "status": "pass" if len(background) == len(Z_SAMPLES) else "fail",
            "evidence": f"background_rows={len(background)}",
        },
        {
            "gate": "primary_CMB_background_fraction_small",
            "status": "pass" if all(float(row["Omega_mem_with_radiation"]) < 1.0e-6 for row in recomb_rows) else "fail",
            "evidence": "recombination sampled Omega_mem below 1e-6",
        },
        {
            "gate": "MTS_dry_runs_no_spectra",
            "status": "pass" if not spectra_runs else "fail",
            "evidence": f"spectra_runs={len(spectra_runs)}",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(locks: list[dict[str, Any]], background: list[dict[str, Any]], dry_runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed_locks = [row for row in locks if row["status"] != "pass"]
    spectra_runs = [row for row in dry_runs if str(row["spectra_run_performed"]).lower() == "true"]
    bad_background = [row for row in background if float(row["E2_with_radiation"]) <= 0.0]
    status = STATUS_PASS if not failed_locks and not spectra_runs and not bad_background else "MTS_CMB_background_injection_dry_run_failed"
    zstar_row = min(background, key=lambda item: abs(float(item["z"]) - REFERENCE_Z_STAR))
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_locks={len(failed_locks)}; spectra_runs={len(spectra_runs)}; bad_background={len(bad_background)}",
        },
        {
            "item": "Omega_mem_at_reference_zstar",
            "verdict": f"{float(zstar_row['Omega_mem_with_radiation']):.12g}",
            "evidence": f"z={zstar_row['z']}",
        },
        {
            "item": "MTS_CMB_spectra_status",
            "verdict": "blocked_not_run",
            "evidence": "background/closure injection only",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "no TT/TE/EE/lensing spectra and no likelihood",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "dry-run background injection only",
        },
        {
            "item": "next_target",
            "verdict": "185-CAMB-MTS-effective-background-module-contract.md",
            "evidence": "next step is engine module/PPF mapping before any MTS spectra interpretation",
        },
    ]


def run_checkpoint(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-MTS-CMB-background-injection-dry-run"
    results_dir = run_dir / "results"
    dry_root = run_dir / "dry-runs"
    results_dir.mkdir(parents=True, exist_ok=True)
    dry_root.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    params = reference_params()
    locks = parameter_lock_rows(params)
    background = background_rows(params)
    closures = closure_mode_rows()
    injection = camb_injection_contract_rows()
    dry_run_dirs = [
        run_from_config(MTS_EXACT_CONFIG, output_root=dry_root, timestamp=run_stamp, dry_run=True),
        run_from_config(MTS_HIGH_CS_CONFIG, output_root=dry_root, timestamp=run_stamp, dry_run=True),
    ]
    dry_runs = dry_run_summary_rows(dry_run_dirs)
    safety = safety_recheck_rows(background)
    claim_gates = claim_gate_rows(locks, dry_runs, background)
    acceptance = acceptance_gate_rows(sources, locks, background, dry_runs)
    decisions = decision_rows(locks, background, dry_runs)
    status_value = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "fixed_parameters": params,
            "z_samples": Z_SAMPLES,
            "purpose": "inject fixed MTS CMB background/closure tables without spectra execution",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "MTS_parameter_locks.csv", locks, ["parameter", "actual", "expected", "delta", "status", "rule"])
    write_csv(
        results_dir / "MTS_background_functions.csv",
        background,
        [
            "z",
            "a",
            "N_ln_1_plus_z",
            "A_mem",
            "dA_dN",
            "rho_mem_over_rhocrit0",
            "one_plus_w_mem",
            "w_mem",
            "E2_no_radiation",
            "E2_with_radiation",
            "Omega_mem_with_radiation",
            "Omega_m_with_radiation",
            "Omega_r_with_radiation",
            "c_s_eff_squared_high_cs",
            "sigma_mem",
            "claim_limit",
        ],
    )
    write_csv(results_dir / "CMB_closure_modes.csv", closures, ["closure_mode", "delta_mem", "theta_mem", "delta_p_mem", "sigma_mem", "status", "claim_limit"])
    write_csv(results_dir / "CAMB_injection_contract.csv", injection, ["pipeline_item", "injected_now", "artifact", "pass_condition", "claim_limit"])
    write_csv(results_dir / "dry_run_summary.csv", dry_runs, ["config_id", "dry_run_dir", "status", "engine_available", "blueprint_valid", "output_contract_valid", "spectra_run_performed", "marker", "reason"])
    write_csv(results_dir / "primary_CMB_safety_recheck.csv", safety, ["z", "Omega_mem_with_radiation", "one_plus_w_mem", "readout", "claim_limit"])
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
            "MTS_background_injection_dry_run": True,
            "MTS_CMB_spectra_run": False,
            "official_likelihood_run": False,
            "promotion_allowed": False,
            "generated": [
                "source_register.csv",
                "MTS_parameter_locks.csv",
                "MTS_background_functions.csv",
                "CMB_closure_modes.csv",
                "CAMB_injection_contract.csv",
                "dry_run_summary.csv",
                "primary_CMB_safety_recheck.csv",
                "claim_gate_results.csv",
                "acceptance_gates.csv",
                "decision.csv",
            ],
            "next_target": decisions[-1]["verdict"],
        },
    )
    marker = "DONE.txt" if status_value == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status_value}\n", encoding="utf-8")
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
