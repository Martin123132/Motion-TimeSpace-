#!/usr/bin/env python3
"""Checkpoint 192: derive or bound the same-density theta/H0 compensation law."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_192_NAME = "theta-H0-compensation-derivation-attempt"
CHECKPOINT_191_RUN = RUNS_ROOT / "20260601-000008-CMB-same-density-mock-likelihood-and-theta-derivation-bridge"
CHECKPOINT_190_RUN = RUNS_ROOT / "20260601-000007-CMB-matched-mock-likelihood-or-derivation-pivot"
CHECKPOINT_188_RUN = RUNS_ROOT / "20260601-000005-CMB-theta-compensation-theorem-or-profiled-fit-gate"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"

BASELINE_VECTOR = CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv"

STATUS = "theta_H0_compensation_FLRW_distance_law_partially_derived_parent_owner_still_missing"
CLAIM_CEILING = "FLRW_compensation_law_internal_only_no_parent_derivation_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.469e-5
NEUTRINO_MASS_TO_OMEGA_H2 = 93.14
ZSTAR_REFERENCE = 1089.9373168180757
INTEGRAL_Z_SPLIT = 2.0
LOW_GRID_POINTS = 20001
HIGH_GRID_POINTS = 50000
LATE_REFERENCE_H0 = 68.42175693081872


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
        (Path(__file__).resolve(), "checkpoint 192 compensation derivation script"),
        (WORK_DIR / "191-CMB-same-density-mock-likelihood-and-theta-derivation-bridge.md", "theta bridge checkpoint"),
        (CHECKPOINT_191_RUN / "status.json", "checkpoint 191 machine status"),
        (CHECKPOINT_191_RUN / "results" / "theta_distance_identity_bridge.csv", "checkpoint 191 distance identity bridge"),
        (CHECKPOINT_191_RUN / "results" / "H0_theta_linear_bridge.csv", "checkpoint 191 H0 bridge"),
        (CHECKPOINT_191_RUN / "results" / "theta_derivation_contract.csv", "checkpoint 191 derivation contract"),
        (WORK_DIR / "190-CMB-matched-mock-likelihood-or-derivation-pivot.md", "mock likelihood checkpoint"),
        (CHECKPOINT_190_RUN / "status.json", "checkpoint 190 machine status"),
        (WORK_DIR / "188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md", "theta profile checkpoint"),
        (CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv", "checkpoint 188 H0 profile results"),
        (WORK_DIR / "186-CAMB-high-cs-wtable-spectra-smoke.md", "unprofiled spectra smoke checkpoint"),
        (CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv", "checkpoint 186 acoustic summary"),
        (BASELINE_VECTOR, "checkpoint 183 baseline parameter vector"),
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


def activation(redshift: float) -> float:
    past_efolds = math.log1p(redshift)
    if past_efolds <= 0.0:
        return 0.0
    exponent = (past_efolds / LOCKED_U3) ** LOCKED_P
    if exponent > 745.0:
        return 1.0
    return 1.0 - math.exp(-exponent)


def omega_r_h2() -> float:
    return OMEGA_GAMMA_H2 * (1.0 + 0.22710731766 * N_EFF)


def q2_lcdm_fixed_density(redshift: float, h: float, omega_m_h2: float, omega_rh2: float) -> float:
    return (
        h * h
        + omega_m_h2 * ((1.0 + redshift) ** 3 - 1.0)
        + omega_rh2 * ((1.0 + redshift) ** 4 - 1.0)
    )


def integration_grid() -> np.ndarray:
    low = np.linspace(0.0, INTEGRAL_Z_SPLIT, LOW_GRID_POINTS)
    high = np.geomspace(INTEGRAL_Z_SPLIT + 1.0e-4, ZSTAR_REFERENCE, HIGH_GRID_POINTS)
    return np.r_[low, high]


def trapezoid(values: np.ndarray, grid: np.ndarray) -> float:
    return float(np.trapezoid(values, grid))


def weighted_activation_integrals(params: dict[str, float]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    h = params["H0"] / 100.0
    omega_m_h2 = params["ombh2"] + params["omch2"] + params["mnu"] / NEUTRINO_MASS_TO_OMEGA_H2
    omega_rh2 = omega_r_h2()
    grid = integration_grid()
    q2_values = np.array([q2_lcdm_fixed_density(float(z), h, omega_m_h2, omega_rh2) for z in grid])
    q_values = np.sqrt(q2_values)
    activation_values = np.array([activation(float(z)) for z in grid])
    q_minus_1 = 1.0 / q_values
    q_minus_3 = 1.0 / (q_values**3)
    chi = trapezoid(q_minus_1, grid)
    weighted_a_q1 = trapezoid(activation_values * q_minus_1, grid) / chi
    response_norm = trapezoid(q_minus_3, grid)
    weighted_a_q3 = trapezoid(activation_values * q_minus_3, grid) / response_norm
    predicted_delta_ln_h = -0.5 * LOCKED_B_MEM * weighted_a_q3
    predicted_h0 = params["H0"] * (1.0 + predicted_delta_ln_h)
    rows = [
        {
            "quantity": "omega_m_h2_fixed",
            "value": omega_m_h2,
            "definition": "ombh2+omch2+approx mnu/93.14",
            "role": "fixed physical matter density",
        },
        {
            "quantity": "omega_r_h2_fixed",
            "value": omega_rh2,
            "definition": "omega_gamma h^2 times N_eff correction",
            "role": "fixed radiation density approximation",
        },
        {
            "quantity": "chi_integral_proxy",
            "value": chi,
            "definition": "Integral dz/q(z) to zstar",
            "role": "dimensionless comoving-distance proxy",
        },
        {
            "quantity": "A_eff_chi_weight_qminus1",
            "value": weighted_a_q1,
            "definition": "Integral A/q dz divided by Integral 1/q dz",
            "role": "ordinary distance-weighted activation",
        },
        {
            "quantity": "A_eff_response_weight_qminus3",
            "value": weighted_a_q3,
            "definition": "Integral A/q^3 dz divided by Integral 1/q^3 dz",
            "role": "first-order distance-response activation",
        },
        {
            "quantity": "predicted_delta_ln_h",
            "value": predicted_delta_ln_h,
            "definition": "-B_mem A_eff_response / 2",
            "role": "first-order theta compensation law",
        },
        {
            "quantity": "predicted_H0_from_integral_law",
            "value": predicted_h0,
            "definition": "H0_baseline*(1+predicted_delta_ln_h)",
            "role": "FLRW integral prediction",
        },
    ]
    summary = {
        "h": h,
        "omega_m_h2": omega_m_h2,
        "omega_r_h2": omega_rh2,
        "chi": chi,
        "weighted_a_q1": weighted_a_q1,
        "weighted_a_q3": weighted_a_q3,
        "predicted_delta_ln_h": predicted_delta_ln_h,
        "predicted_h0": predicted_h0,
    }
    return rows, summary


def equation_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "theta_* ~= r_s(z_*) / D_A(z_*)",
            "meaning": "CMB acoustic angle is controlled by early sound horizon and angular-diameter distance",
            "status": "standard_FLRW_identity_proxy",
        },
        {
            "step": 2,
            "equation": "q_LCDM^2(z)=h^2+omega_m[(1+z)^3-1]+omega_r[(1+z)^4-1]",
            "meaning": "fixed-physical-density flat background in H/100 units",
            "status": "derived_for_same_density_branch",
        },
        {
            "step": 3,
            "equation": "q_MTS^2(z)=q_LCDM^2(z)+h^2 B_mem A(z)",
            "meaning": "locked MTS memory adds a late-time positive expansion term",
            "status": "closure_level_from_locked_background",
        },
        {
            "step": 4,
            "equation": "delta chi = -1/2 Integral[delta q^2/q^3] dz",
            "meaning": "first-order distance response to a background perturbation",
            "status": "derived_FLRW_variation",
        },
        {
            "step": 5,
            "equation": "delta ln h ~= -(B_mem/2) <A>_{q^-3}",
            "meaning": "H0 must decrease to cancel the MTS distance deficit",
            "status": "partial_compensation_law",
        },
        {
            "step": 6,
            "equation": "<A>_{q^-3}=Integral[A(z)/q^3 dz]/Integral[1/q^3 dz]",
            "meaning": "only the response-weighted activation matters for first-order compensation",
            "status": "computable_bridge_not_parent_owner",
        },
    ]


def profile_value(rows: list[dict[str, str]], family: str, model: str, key: str) -> float:
    for row in rows:
        if row["family"] == family and row["model"] == model:
            return float(row[key])
    raise KeyError(f"missing profile {family}/{model}/{key}")


def h0_prediction_comparison_rows(params: dict[str, float], integral_summary: dict[str, float]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    profile_rows = read_csv_rows(CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv")
    baseline_h0 = params["H0"]
    actual_profile_h0 = profile_value(profile_rows, "same_physical_densities", "MTS_high_cs_fluid", "profiled_H0")
    actual_delta_ln_h = actual_profile_h0 / baseline_h0 - 1.0
    required_a_eff = -2.0 * actual_delta_ln_h / LOCKED_B_MEM
    integral_pred_h0 = integral_summary["predicted_h0"]
    checkpoint_191 = load_json(CHECKPOINT_191_RUN / "status.json")
    linear_pred_h0 = float(checkpoint_191["linear_predicted_profile_H0"])
    rows = [
        {
            "prediction": "actual_root_profile_H0",
            "H0": actual_profile_h0,
            "delta_H0_vs_baseline": actual_profile_h0 - baseline_h0,
            "delta_ln_h": actual_delta_ln_h,
            "error_vs_actual_H0": 0.0,
            "readout": "full CAMB profile root from checkpoint 188",
        },
        {
            "prediction": "FLRW_integral_first_order",
            "H0": integral_pred_h0,
            "delta_H0_vs_baseline": integral_pred_h0 - baseline_h0,
            "delta_ln_h": integral_summary["predicted_delta_ln_h"],
            "error_vs_actual_H0": integral_pred_h0 - actual_profile_h0,
            "readout": "analytic same-density distance-response law",
        },
        {
            "prediction": "checkpoint_191_finite_difference_bridge",
            "H0": linear_pred_h0,
            "delta_H0_vs_baseline": linear_pred_h0 - baseline_h0,
            "delta_ln_h": linear_pred_h0 / baseline_h0 - 1.0,
            "error_vs_actual_H0": linear_pred_h0 - actual_profile_h0,
            "readout": "local numerical theta derivative bridge",
        },
        {
            "prediction": "late_reference_H0",
            "H0": LATE_REFERENCE_H0,
            "delta_H0_vs_baseline": LATE_REFERENCE_H0 - baseline_h0,
            "delta_ln_h": LATE_REFERENCE_H0 / baseline_h0 - 1.0,
            "error_vs_actual_H0": LATE_REFERENCE_H0 - actual_profile_h0,
            "readout": "previous late-reference branch; tension with CMB same-density profile",
        },
        {
            "prediction": "required_A_eff_from_actual_profile",
            "H0": "",
            "delta_H0_vs_baseline": "",
            "delta_ln_h": "",
            "error_vs_actual_H0": required_a_eff - integral_summary["weighted_a_q3"],
            "readout": f"required A_eff={required_a_eff}; integral A_eff={integral_summary['weighted_a_q3']}",
        },
    ]
    summary = {
        "actual_profile_h0": actual_profile_h0,
        "actual_delta_ln_h": actual_delta_ln_h,
        "required_a_eff": required_a_eff,
        "integral_pred_h0": integral_pred_h0,
        "integral_error_h0": integral_pred_h0 - actual_profile_h0,
        "linear_pred_h0": linear_pred_h0,
        "linear_error_h0": linear_pred_h0 - actual_profile_h0,
        "late_reference_error_h0": LATE_REFERENCE_H0 - actual_profile_h0,
    }
    return rows, summary


def parent_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap": "B_mem amplitude owner",
            "why_it_blocks_derivation": "compensation law depends linearly on B_mem",
            "current_status": "B_mem=2/27 is locked but not parent-derived",
            "needed_next": "derive B_mem from action/boundary normalization or keep as closure",
        },
        {
            "gap": "activation law owner",
            "why_it_blocks_derivation": "response-weighted activation <A> sets the H0 shift magnitude",
            "current_status": "p=3,u3=1/4 are locked regularity/closure parameters",
            "needed_next": "derive A(z) from cell-current or memory production equation",
        },
        {
            "gap": "clock/calibration owner",
            "why_it_blocks_derivation": "same-density profile lowers H0 relative to late-reference H0",
            "current_status": "no parent relation deciding CMB H0 versus late SN/BAO/H(z) H0",
            "needed_next": "derive observer clock map or calibration bridge",
        },
        {
            "gap": "exact perturbation owner",
            "why_it_blocks_derivation": "CMB spectra currently use high-cs effective fluid",
            "current_status": "partial effective owner only",
            "needed_next": "derive exact auxiliary or parent perturbation equations",
        },
        {
            "gap": "local GR owner",
            "why_it_blocks_derivation": "fundamental theory must recover local GR while modifying cosmological distance",
            "current_status": "screened effective branch only",
            "needed_next": "derive local fixed point/q_loc silence from parent action",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], prediction_summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    integral_close = abs(prediction_summary["integral_error_h0"]) < 0.15
    linear_close = abs(prediction_summary["linear_error_h0"]) < 0.05
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation attempt only",
        },
        {
            "gate": "FLRW integral law predicts H0 profile scale",
            "status": "pass" if integral_close else "warning",
            "evidence": f"integral_error_H0={prediction_summary['integral_error_h0']}",
            "claim_allowed": "partial derivation bridge",
        },
        {
            "gate": "local theta derivative predicts H0 profile",
            "status": "pass" if linear_close else "warning",
            "evidence": f"linear_error_H0={prediction_summary['linear_error_h0']}",
            "claim_allowed": "numerical bridge",
        },
        {
            "gate": "parent theory derives compensation",
            "status": "fail",
            "evidence": "B_mem, activation, calibration, perturbations, local GR still lack parent owners",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "late-reference H0 consistency",
            "status": "warning",
            "evidence": f"late_reference_error_H0={prediction_summary['late_reference_error_h0']}",
            "claim_allowed": "requires calibration derivation",
        },
        {
            "gate": "official CMB likelihood",
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


def decision_rows(prediction_summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The same-density H0 compensation law is partially derived from the FLRW distance response: MTS adds h^2 B A(z), lowering H0 cancels the D_A deficit. Parent ownership is still missing.",
            "actual_profile_H0": prediction_summary["actual_profile_h0"],
            "integral_law_H0": prediction_summary["integral_pred_h0"],
            "integral_error_H0": prediction_summary["integral_error_h0"],
            "required_A_eff": prediction_summary["required_a_eff"],
            "next_target": "193-calibration-bridge-H0-owner-or-demotion.md",
            "MTS_spectra_run": "false",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_192_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params = baseline_params()
    source_rows = source_register_rows()
    equation_rows = equation_derivation_rows()
    integral_rows, integral_summary = weighted_activation_integrals(params)
    prediction_rows, prediction_summary = h0_prediction_comparison_rows(params, integral_summary)
    gap_rows = parent_gap_rows()
    gates = claim_gate_rows(source_rows, prediction_summary)
    decision = decision_rows(prediction_summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "equation_derivation_steps.csv": (
            equation_rows,
            ["step", "equation", "meaning", "status"],
        ),
        "weighted_activation_integral.csv": (
            integral_rows,
            ["quantity", "value", "definition", "role"],
        ),
        "H0_prediction_comparison.csv": (
            prediction_rows,
            ["prediction", "H0", "delta_H0_vs_baseline", "delta_ln_h", "error_vs_actual_H0", "readout"],
        ),
        "parent_derivation_gap_ledger.csv": (
            gap_rows,
            ["gap", "why_it_blocks_derivation", "current_status", "needed_next"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "actual_profile_H0",
                "integral_law_H0",
                "integral_error_H0",
                "required_A_eff",
                "next_target",
                "MTS_spectra_run",
                "official_likelihood_run",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "actual_profile_H0": prediction_summary["actual_profile_h0"],
        "integral_law_H0": prediction_summary["integral_pred_h0"],
        "integral_error_H0": prediction_summary["integral_error_h0"],
        "required_A_eff": prediction_summary["required_a_eff"],
        "integral_A_eff": integral_summary["weighted_a_q3"],
        "parent_compensation_derived": False,
        "FLRW_distance_law_partially_derived": True,
        "MTS_spectra_run": False,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
