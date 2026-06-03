"""Route gate for an H(z)/radial-expansion stress test after BAO-shape audit."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

WORK_DIR = Path(__file__).resolve().parent.parent
ROOT = WORK_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
DATA_ROOT = ROOT / "formalization-workbench" / "data" / "cosmology" / "cosmic_chronometers"
CC_RECIPE_ROOT = ROOT / "formalization-workbench" / "data" / "CCcovariance"

HZ_32 = DATA_ROOT / "Hz.csv"
SOURCE_METADATA = DATA_ROOT / "source_metadata.json"
COV_BRANCH_DIR = DATA_ROOT / "covariance_branch"
HZ_15 = COV_BRANCH_DIR / "Hz_CC_Moresco15_BC03.csv"
ROW_LOCK = COV_BRANCH_DIR / "row_lock_manifest.json"
COVARIANCE_FILES = {
    "diagonal_total_error": COV_BRANCH_DIR / "covariance_diagonal_total_error.csv",
    "suggested": COV_BRANCH_DIR / "covariance_suggested.csv",
    "conservative": COV_BRANCH_DIR / "covariance_conservative.csv",
    "extra_conservative": COV_BRANCH_DIR / "covariance_extra_conservative.csv",
    "nonstat_systematic_only": COV_BRANCH_DIR / "covariance_nonstat_systematic_only.csv",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        HZ_32,
        SOURCE_METADATA,
        HZ_15,
        ROW_LOCK,
        *COVARIANCE_FILES.values(),
        CC_RECIPE_ROOT / "README.md",
        WORK_DIR / "124-BAO-shape-residual-decomposition.md",
        script_path,
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def read_covariance_matrix(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        if len(header) < 2:
            raise ValueError(f"bad covariance header in {path}")
        rows = []
        for row in reader:
            rows.append([float(value) for value in row[1:]])
    matrix = np.asarray(rows, dtype=float)
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"covariance matrix {path} is not square: {matrix.shape}")
    return matrix


def covariance_diagnostic_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, path in COVARIANCE_FILES.items():
        matrix = read_covariance_matrix(path)
        eigvals = np.linalg.eigvalsh(matrix)
        min_eig = float(np.min(eigvals))
        max_eig = float(np.max(eigvals))
        rows.append(
            {
                "covariance": label,
                "path": str(path),
                "rows": matrix.shape[0],
                "cols": matrix.shape[1],
                "symmetric": bool(np.allclose(matrix, matrix.T, rtol=1.0e-9, atol=1.0e-9)),
                "min_eigenvalue": min_eig,
                "max_eigenvalue": max_eig,
                "condition_number": max_eig / min_eig if min_eig > 0.0 else math.inf,
                "positive_definite": bool(min_eig > 0.0),
                "status": "usable" if min_eig > 0.0 else "not_positive_definite",
            }
        )
    return rows


def data_option_rows() -> list[dict[str, Any]]:
    metadata = read_json(SOURCE_METADATA)
    row_lock = read_json(ROW_LOCK)
    hz32_rows = read_csv_rows(HZ_32)
    hz15_rows = read_csv_rows(HZ_15)
    return [
        {
            "option": "CC_full32_diagonal",
            "data_path": str(HZ_32),
            "rows": len(hz32_rows),
            "covariance": "diagonal_sigma_only",
            "source": metadata.get("source_url", ""),
            "status": "sensitivity_only",
            "claim_ceiling": "diagonal_sanity_check_not_primary_evidence",
            "notes": metadata.get("caveat", ""),
        },
        {
            "option": "CC_15row_covariance_suggested",
            "data_path": str(HZ_15),
            "rows": len(hz15_rows),
            "covariance": str(COVARIANCE_FILES["suggested"]),
            "source": row_lock.get("recipe_source", ""),
            "status": "primary_smoke_candidate",
            "claim_ceiling": "covariance_smoke_only",
            "notes": "15-row Moresco covariance branch prepared locally; use as primary H(z) stress route.",
        },
        {
            "option": "CC_15row_covariance_conservative_sensitivity",
            "data_path": str(HZ_15),
            "rows": len(hz15_rows),
            "covariance": str(COVARIANCE_FILES["conservative"]),
            "source": row_lock.get("recipe_source", ""),
            "status": "sensitivity_candidate",
            "claim_ceiling": "covariance_sensitivity_only",
            "notes": "Checks whether the result depends on covariance prescription.",
        },
    ]


def model_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "H_model": "H(z)=100 h E_LCDM(z;Omega_m0)",
            "free_parameters": "Omega_m0;h",
            "fairness_rule": "same H(z) rows and covariance as MTS",
        },
        {
            "model": "wCDM",
            "role": "flexible_baseline",
            "H_model": "H(z)=100 h E_wCDM(z;Omega_m0,w)",
            "free_parameters": "Omega_m0;h;w",
            "fairness_rule": "same priors/edge reporting as cosmology branch",
        },
        {
            "model": "CPL",
            "role": "flexible_baseline",
            "H_model": "H(z)=100 h E_CPL(z;Omega_m0,w0,wa)",
            "free_parameters": "Omega_m0;h;w0;wa",
            "fairness_rule": "allowed but penalized by AIC/BIC",
        },
        {
            "model": "MTS_locked_2over27",
            "role": "predeclared_locked_branch",
            "H_model": "H(z)=100 h E_MTS(z;Omega_m0,B_mem=2/27,p=3,u3=1/4)",
            "free_parameters": "Omega_m0;h",
            "fairness_rule": "no BAO-shape repair or Omega-map term",
        },
        {
            "model": "MTS_Bmem_zero",
            "role": "negative_control",
            "H_model": "H(z)=100 h E_MTS(z;Omega_m0,B_mem=0,p=3,u3=1/4)",
            "free_parameters": "Omega_m0;h",
            "fairness_rule": "must reproduce LCDM background",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "data_integrity",
            "rule": "source paths, row counts, and covariance dimensions must pass before scoring",
            "status": "required",
        },
        {
            "gate": "covariance_primary",
            "rule": "primary score uses 15-row suggested covariance; full32 diagonal is sensitivity only",
            "status": "required",
        },
        {
            "gate": "baseline_symmetry",
            "rule": "LCDM, wCDM, CPL, MTS_locked, and Bmem_zero use identical H(z) rows/covariance",
            "status": "required",
        },
        {
            "gate": "no_local_H0_prior",
            "rule": "do not add SH0ES/local-H0 calibration pressure in the primary H(z) route",
            "status": "required",
        },
        {
            "gate": "no_rescue_term",
            "rule": "do not add an MTS-only radial correction before a theorem contract exists",
            "status": "locked",
        },
        {
            "gate": "claim_ceiling",
            "rule": "H(z) smoke can support or weaken radial consistency only; it cannot derive CMB/BAO physics",
            "status": "locked",
        },
    ]


def decision_rows(cov_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    usable_primary = any(row["covariance"] == "suggested" and row["positive_definite"] for row in cov_rows)
    return [
        {
            "item": "status",
            "verdict": "Hz_radial_stress_route_ready" if usable_primary else "Hz_route_blocked_covariance",
            "evidence": "local CC data and 15-row covariance branch found" if usable_primary else "primary covariance is not positive definite",
        },
        {
            "item": "primary_data",
            "verdict": "CC_15row_covariance_suggested",
            "evidence": str(HZ_15),
        },
        {
            "item": "sensitivity_data",
            "verdict": "CC_full32_diagonal_and_covariance_variants",
            "evidence": str(DATA_ROOT),
        },
        {
            "item": "next_script",
            "verdict": "Hz_radial_expansion_smoke.py",
            "evidence": "fit H(z)=100 h E(z) symmetrically for baselines and locked MTS",
        },
        {
            "item": "claim_status",
            "verdict": "route_gate_only_no_evidence_claim",
            "evidence": "no likelihood score has been run in this checkpoint",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Hz-radial-stress-route-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    cov_rows = covariance_diagnostic_rows()
    data_rows = data_option_rows()
    model_rows = model_contract_rows()
    gates = acceptance_gate_rows()
    decisions = decision_rows(cov_rows)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_option_audit.csv",
        data_rows,
        ["option", "data_path", "rows", "covariance", "source", "status", "claim_ceiling", "notes"],
    )
    write_csv(
        results_dir / "covariance_diagnostics.csv",
        cov_rows,
        [
            "covariance",
            "path",
            "rows",
            "cols",
            "symmetric",
            "min_eigenvalue",
            "max_eigenvalue",
            "condition_number",
            "positive_definite",
            "status",
        ],
    )
    write_csv(
        results_dir / "model_test_contract.csv",
        model_rows,
        ["model", "role", "H_model", "free_parameters", "fairness_rule"],
    )
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "rule", "status"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": "Hz_radial_stress_route_ready",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "route_gate_not_likelihood_evidence",
        "generated": [
            "source_register.csv",
            "data_option_audit.csv",
            "covariance_diagnostics.csv",
            "model_test_contract.csv",
            "acceptance_gates.csv",
            "decision.csv",
        ],
        "next_target": "126-Hz-radial-expansion-smoke.md plus scripts/Hz_radial_expansion_smoke.py",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
