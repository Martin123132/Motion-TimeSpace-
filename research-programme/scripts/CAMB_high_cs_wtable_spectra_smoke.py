#!/usr/bin/env python3
"""Checkpoint 186: tiny CAMB spectra smoke for locked high-cs MTS w(a)."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import camb
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_185_RUN = RUNS_ROOT / "20260601-000002-CAMB-MTS-effective-background-module-contract"
CHECKPOINT_184_RUN = RUNS_ROOT / "20260601-000001-MTS-CMB-background-injection-dry-run"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"

W_TABLE = CHECKPOINT_185_RUN / "results" / "MTS_CAMB_w_table.csv"
BASELINE_VECTOR = CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv"

STATUS_PASS_WITH_WARNING = "CAMB_high_cs_wtable_spectra_smoke_ran_no_likelihood_theta_shift_flagged"
STATUS_FAIL = "CAMB_high_cs_wtable_spectra_smoke_failed"
CLAIM_CEILING = "tiny_CAMB_spectra_smoke_only_no_official_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LMAX = 200
SAMPLE_ELLS = [2, 10, 30, 50, 100, 150, 200]
THETA_FRAC_WARNING = 1.0e-3
RELATIVE_FLOOR = 1.0e-30


@dataclass(frozen=True)
class BranchSpec:
    name: str
    dark_energy_model: str
    claim_role: str
    status_rule: str


BRANCHES = [
    BranchSpec(
        name="LCDM_baseline_recomputed",
        dark_energy_model="lcdm",
        claim_role="control branch",
        status_rule="same checkpoint-183 physical-density baseline",
    ),
    BranchSpec(
        name="MTS_high_cs_fluid_density_isolation",
        dark_energy_model="fluid",
        claim_role="first MTS spectra-producing smoke branch",
        status_rule="same baseline physical densities; only dark-energy w(a) shape changed",
    ),
    BranchSpec(
        name="MTS_high_cs_PPF_density_isolation",
        dark_energy_model="ppf",
        claim_role="numerical comparator branch",
        status_rule="same background table through CAMB PPF; not physical evidence by itself",
    ),
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 186 spectra smoke script"),
        (WORK_DIR / "185-CAMB-MTS-effective-background-module-contract.md", "CAMB MTS mapping contract"),
        (CHECKPOINT_185_RUN / "status.json", "checkpoint 185 machine status"),
        (W_TABLE, "locked MTS CAMB w(a) table"),
        (CHECKPOINT_185_RUN / "results" / "module_readiness_gates.csv", "checkpoint 185 readiness gates"),
        (WORK_DIR / "184-MTS-CMB-background-injection-dry-run.md", "MTS CMB background injection checkpoint"),
        (CHECKPOINT_184_RUN / "status.json", "checkpoint 184 machine status"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline checkpoint"),
        (CHECKPOINT_183_RUN / "status.json", "checkpoint 183 machine status"),
        (BASELINE_VECTOR, "checkpoint 183 physical-density baseline vector"),
        (Path(camb.__file__).resolve(), "installed CAMB Python package"),
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


def baseline_params() -> dict[str, float]:
    return {row["parameter"]: float(row["value"]) for row in read_csv_rows(BASELINE_VECTOR)}


def w_table_arrays() -> tuple[np.ndarray, np.ndarray, list[dict[str, str]]]:
    rows = read_csv_rows(W_TABLE)
    scale_factors = np.array([float(row["a"]) for row in rows])
    w_values = np.array([float(row["w_mem"]) for row in rows])
    return scale_factors, w_values, rows


def run_camb_branch(
    branch: BranchSpec,
    params_dict: dict[str, float],
    scale_factors: np.ndarray,
    w_values: np.ndarray,
) -> dict[str, Any]:
    start = datetime.now(timezone.utc)
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=params_dict["H0"],
        ombh2=params_dict["ombh2"],
        omch2=params_dict["omch2"],
        tau=params_dict["tau"],
        mnu=params_dict["mnu"],
        omk=params_dict["omk"],
    )
    params.InitPower.set_params(As=params_dict["As"], ns=params_dict["ns"])
    if branch.dark_energy_model in {"fluid", "ppf"}:
        params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=scale_factors,
            wde_w_array=w_values,
            dark_energy_model=branch.dark_energy_model,
        )
    params.set_for_lmax(LMAX, lens_potential_accuracy=0)
    results = camb.get_results(params)
    powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    derived = {key: float(value) for key, value in results.get_derived_params().items()}
    return {
        "branch": branch,
        "params": params,
        "results": results,
        "powers": powers,
        "derived": derived,
        "elapsed_seconds": elapsed,
        "status": "pass",
        "error": "",
    }


def branch_run_summary_rows(branch_outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in BRANCHES:
        output = branch_outputs.get(spec.name)
        if output is None:
            rows.append(
                {
                    "branch": spec.name,
                    "CAMB_dark_energy_model": spec.dark_energy_model,
                    "status": "missing",
                    "runtime_seconds": "",
                    "claim_role": spec.claim_role,
                    "status_rule": spec.status_rule,
                    "error": "branch output missing",
                }
            )
            continue
        rows.append(
            {
                "branch": spec.name,
                "CAMB_dark_energy_model": spec.dark_energy_model,
                "status": output["status"],
                "runtime_seconds": output.get("elapsed_seconds", ""),
                "claim_role": spec.claim_role,
                "status_rule": spec.status_rule,
                "error": output.get("error", ""),
            }
        )
    return rows


def parameter_context_rows(params_dict: dict[str, float], w_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = [
        {
            "item": key,
            "value": value,
            "source": "checkpoint 183 baseline vector",
            "rule": "held fixed across LCDM/MTS density-isolation smoke",
        }
        for key, value in params_dict.items()
    ]
    w_values = [float(row["w_mem"]) for row in w_rows]
    rows.extend(
        [
            {
                "item": "LMAX",
                "value": LMAX,
                "source": "checkpoint 186 smoke setting",
                "rule": "tiny smoke only",
            },
            {
                "item": "w_table_rows",
                "value": len(w_rows),
                "source": "checkpoint 185 MTS_CAMB_w_table.csv",
                "rule": "locked generated table, no refit",
            },
            {
                "item": "w_mem_min",
                "value": min(w_values),
                "source": "checkpoint 185 MTS_CAMB_w_table.csv",
                "rule": "non-phantom fluid check",
            },
            {
                "item": "w_mem_max",
                "value": max(w_values),
                "source": "checkpoint 185 MTS_CAMB_w_table.csv",
                "rule": "locked activation hump",
            },
        ]
    )
    return rows


def spectra_sample_rows(branch_outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_name, output in branch_outputs.items():
        if output["status"] != "pass":
            continue
        total = output["powers"]["total"]
        for ell in SAMPLE_ELLS:
            rows.append(
                {
                    "branch": branch_name,
                    "ell": ell,
                    "TT_Dl_uK2": float(total[ell, 0]),
                    "EE_Dl_uK2": float(total[ell, 1]),
                    "BB_Dl_uK2": float(total[ell, 2]),
                    "TE_Dl_uK2": float(total[ell, 3]),
                    "source": "CAMB total lensed CMB power spectra",
                }
            )
    return rows


def acoustic_distance_rows(branch_outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    baseline = branch_outputs["LCDM_baseline_recomputed"]["derived"]
    keys = ["age", "zstar", "rstar", "thetastar", "DAstar", "zdrag", "rdrag", "zeq", "keq"]
    rows: list[dict[str, Any]] = []
    for branch_name, output in branch_outputs.items():
        if output["status"] != "pass":
            continue
        derived = output["derived"]
        for key in keys:
            value = float(derived.get(key, math.nan))
            baseline_value = float(baseline.get(key, math.nan))
            delta = value - baseline_value if math.isfinite(value) and math.isfinite(baseline_value) else math.nan
            frac = delta / baseline_value if baseline_value not in {0.0, math.nan} and math.isfinite(delta) else math.nan
            rows.append(
                {
                    "branch": branch_name,
                    "quantity": key,
                    "value": value,
                    "LCDM_baseline_value": baseline_value,
                    "delta_vs_LCDM": delta,
                    "frac_delta_vs_LCDM": frac,
                    "claim_limit": "tiny spectra smoke diagnostic; no official likelihood",
                }
            )
    return rows


def residual_rows(branch_outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    baseline_total = branch_outputs["LCDM_baseline_recomputed"]["powers"]["total"]
    rows: list[dict[str, Any]] = []
    for branch_name, output in branch_outputs.items():
        if branch_name == "LCDM_baseline_recomputed" or output["status"] != "pass":
            continue
        total = output["powers"]["total"]
        for ell in range(2, LMAX + 1):
            lcdm_tt = float(baseline_total[ell, 0])
            lcdm_ee = float(baseline_total[ell, 1])
            lcdm_te = float(baseline_total[ell, 3])
            branch_tt = float(total[ell, 0])
            branch_ee = float(total[ell, 1])
            branch_te = float(total[ell, 3])
            rows.append(
                {
                    "branch": branch_name,
                    "ell": ell,
                    "delta_TT_Dl_uK2": branch_tt - lcdm_tt,
                    "frac_delta_TT": (branch_tt - lcdm_tt) / max(abs(lcdm_tt), RELATIVE_FLOOR),
                    "delta_EE_Dl_uK2": branch_ee - lcdm_ee,
                    "frac_delta_EE": (branch_ee - lcdm_ee) / max(abs(lcdm_ee), RELATIVE_FLOOR),
                    "delta_TE_Dl_uK2": branch_te - lcdm_te,
                    "frac_delta_TE": (branch_te - lcdm_te) / max(abs(lcdm_te), RELATIVE_FLOOR),
                }
            )
    return rows


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values)) if values else math.nan


def residual_summary_rows(residuals: list[dict[str, Any]], acoustic_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    theta_by_branch = {
        row["branch"]: float(row["frac_delta_vs_LCDM"])
        for row in acoustic_rows
        if row["quantity"] == "thetastar" and row["branch"] != "LCDM_baseline_recomputed"
    }
    branch_names = sorted({str(row["branch"]) for row in residuals})
    for branch_name in branch_names:
        branch_rows = [row for row in residuals if row["branch"] == branch_name]
        tt = [float(row["frac_delta_TT"]) for row in branch_rows]
        ee = [float(row["frac_delta_EE"]) for row in branch_rows]
        te = [float(row["frac_delta_TE"]) for row in branch_rows if math.isfinite(float(row["frac_delta_TE"]))]
        max_tt_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_TT"])))
        max_ee_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_EE"])))
        theta_frac = theta_by_branch.get(branch_name, math.nan)
        rows.append(
            {
                "branch": branch_name,
                "max_abs_frac_delta_TT": abs(float(max_tt_row["frac_delta_TT"])),
                "max_abs_frac_delta_TT_ell": max_tt_row["ell"],
                "rms_frac_delta_TT": rms(tt),
                "max_abs_frac_delta_EE": abs(float(max_ee_row["frac_delta_EE"])),
                "max_abs_frac_delta_EE_ell": max_ee_row["ell"],
                "rms_frac_delta_EE": rms(ee),
                "rms_frac_delta_TE": rms(te),
                "frac_delta_thetastar": theta_frac,
                "theta_warning": "yes" if abs(theta_frac) > THETA_FRAC_WARNING else "no",
                "interpretation": "finite spectra, but raw acoustic-scale shift must face a proper likelihood/parameter fit",
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    branch_summary: list[dict[str, Any]],
    residual_summary: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    branches_ok = all(row["status"] == "pass" for row in branch_summary)
    theta_warnings = sum(row["theta_warning"] == "yes" for row in residual_summary)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": f"missing={sum(row['exists'] != 'yes' for row in source_rows)}",
            "claim_allowed": "spectra smoke only",
        },
        {
            "gate": "LCDM baseline recomputed",
            "status": "pass" if any(row["branch"] == "LCDM_baseline_recomputed" and row["status"] == "pass" for row in branch_summary) else "fail",
            "evidence": "checkpoint 183 vector rerun in same script",
            "claim_allowed": "control branch",
        },
        {
            "gate": "MTS high-cs fluid spectra run",
            "status": "pass" if any(row["branch"] == "MTS_high_cs_fluid_density_isolation" and row["status"] == "pass" for row in branch_summary) else "fail",
            "evidence": "DarkEnergyFluid set_w_a_table branch generated spectra",
            "claim_allowed": "pipeline readiness, not support",
        },
        {
            "gate": "MTS PPF comparator spectra run",
            "status": "pass" if any(row["branch"] == "MTS_high_cs_PPF_density_isolation" and row["status"] == "pass" for row in branch_summary) else "fail",
            "evidence": "DarkEnergyPPF set_w_a_table branch generated spectra",
            "claim_allowed": "diagnostic comparator",
        },
        {
            "gate": "theta_star_raw_shift",
            "status": "warning" if theta_warnings else "pass",
            "evidence": f"branches_over_{THETA_FRAC_WARNING}_fractional_shift={theta_warnings}",
            "claim_allowed": "must not be treated as CMB evidence until likelihood/fit branch exists",
        },
        {
            "gate": "exact auxiliary spectra",
            "status": "blocked",
            "evidence": "checkpoint 185 found no built-in CAMB delta=theta=0 primitive",
            "claim_allowed": "no exact auxiliary CMB claim",
        },
        {
            "gate": "official likelihood run",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no CMB support claim",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(gate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hard_failures = [row for row in gate_rows if row["status"] == "fail" and row["gate"] != "support claim allowed"]
    theta_warning = any(row["gate"] == "theta_star_raw_shift" and row["status"] == "warning" for row in gate_rows)
    status = STATUS_FAIL if hard_failures else STATUS_PASS_WITH_WARNING
    next_target = (
        "187-CAMB-density-convention-and-locked-transfer-theta-gate.md"
        if status != STATUS_FAIL
        else "repair 186 high-cs spectra smoke"
    )
    return [
        {
            "decision": status,
            "meaning": "MTS high-cs w(a) produces finite CAMB spectra under a fair same-density smoke, but raw theta* shift is a precision-CMB hazard"
            if theta_warning
            else "MTS high-cs w(a) produces finite CAMB spectra under a fair same-density smoke",
            "next_target": next_target,
            "MTS_spectra_run": "true",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-CAMB-high-cs-wtable-spectra-smoke"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params_dict = baseline_params()
    scale_factors, w_values, w_rows = w_table_arrays()
    source_rows = source_register_rows()

    branch_outputs: dict[str, dict[str, Any]] = {}
    for branch in BRANCHES:
        try:
            branch_outputs[branch.name] = run_camb_branch(branch, params_dict, scale_factors, w_values)
        except Exception as exc:  # pragma: no cover - engine/runtime dependent
            branch_outputs[branch.name] = {
                "branch": branch,
                "status": "fail",
                "error": f"{type(exc).__name__}: {exc}",
                "elapsed_seconds": "",
            }

    branch_summary = branch_run_summary_rows(branch_outputs)
    spectra_samples = spectra_sample_rows(branch_outputs)
    acoustic_rows = acoustic_distance_rows(branch_outputs) if branch_outputs["LCDM_baseline_recomputed"]["status"] == "pass" else []
    residuals = residual_rows(branch_outputs) if branch_outputs["LCDM_baseline_recomputed"]["status"] == "pass" else []
    residual_summary = residual_summary_rows(residuals, acoustic_rows) if residuals else []
    gate_rows = claim_gate_rows(source_rows, branch_summary, residual_summary)
    decision = decision_rows(gate_rows)

    outputs: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "parameter_context.csv": (
            parameter_context_rows(params_dict, w_rows),
            ["item", "value", "source", "rule"],
        ),
        "branch_run_summary.csv": (
            branch_summary,
            ["branch", "CAMB_dark_energy_model", "status", "runtime_seconds", "claim_role", "status_rule", "error"],
        ),
        "spectra_sample_Dl.csv": (
            spectra_samples,
            ["branch", "ell", "TT_Dl_uK2", "EE_Dl_uK2", "BB_Dl_uK2", "TE_Dl_uK2", "source"],
        ),
        "acoustic_distance_summary.csv": (
            acoustic_rows,
            ["branch", "quantity", "value", "LCDM_baseline_value", "delta_vs_LCDM", "frac_delta_vs_LCDM", "claim_limit"],
        ),
        "spectra_residuals_vs_LCDM.csv": (
            residuals,
            ["branch", "ell", "delta_TT_Dl_uK2", "frac_delta_TT", "delta_EE_Dl_uK2", "frac_delta_EE", "delta_TE_Dl_uK2", "frac_delta_TE"],
        ),
        "spectra_residual_summary.csv": (
            residual_summary,
            [
                "branch",
                "max_abs_frac_delta_TT",
                "max_abs_frac_delta_TT_ell",
                "rms_frac_delta_TT",
                "max_abs_frac_delta_EE",
                "max_abs_frac_delta_EE_ell",
                "rms_frac_delta_EE",
                "rms_frac_delta_TE",
                "frac_delta_thetastar",
                "theta_warning",
                "interpretation",
            ],
        ),
        "claim_gate_results.csv": (
            gate_rows,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "next_target", "MTS_spectra_run", "official_likelihood_run", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "camb_version": camb.__version__,
        "generated": list(outputs.keys()),
        "branches": [branch.name for branch in BRANCHES],
        "lmax": LMAX,
        "MTS_spectra_run": True,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "theta_warning": any(row.get("theta_warning") == "yes" for row in residual_summary),
        "exact_auxiliary_branch": "not_run_blocked_requires_custom_module",
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    status_payload = run(args.timestamp)
    print(json.dumps(status_payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
