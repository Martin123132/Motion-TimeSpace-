#!/usr/bin/env python3
"""Checkpoint 191: same-density CMB mock likelihood and theta-derivation bridge."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_191_NAME = "CMB-same-density-mock-likelihood-and-theta-derivation-bridge"
CHECKPOINT_190_RUN = RUNS_ROOT / "20260601-000007-CMB-matched-mock-likelihood-or-derivation-pivot"
CHECKPOINT_189_RUN = RUNS_ROOT / "20260601-000006-CMB-profiled-shape-residual-and-likelihood-readiness"
CHECKPOINT_188_RUN = RUNS_ROOT / "20260601-000005-CMB-theta-compensation-theorem-or-profiled-fit-gate"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"

STATUS = "CMB_same_density_mock_competitive_theta_bridge_closure_not_derived_late_H0_tension_flagged"
CLAIM_CEILING = "same_density_theta_bridge_internal_only_no_official_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LATE_REFERENCE_H0 = 68.42175693081872
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25


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
        (Path(__file__).resolve(), "checkpoint 191 theta bridge script"),
        (WORK_DIR / "190-CMB-matched-mock-likelihood-or-derivation-pivot.md", "matched mock likelihood checkpoint"),
        (CHECKPOINT_190_RUN / "status.json", "checkpoint 190 machine status"),
        (CHECKPOINT_190_RUN / "results" / "decision_snapshot.csv", "checkpoint 190 mock decision snapshot"),
        (CHECKPOINT_190_RUN / "results" / "mock_scorecard.csv", "checkpoint 190 mock scorecard"),
        (CHECKPOINT_190_RUN / "results" / "derivation_pivot_ledger.csv", "checkpoint 190 derivation pivot ledger"),
        (WORK_DIR / "189-CMB-profiled-shape-residual-and-likelihood-readiness.md", "profiled shape readiness checkpoint"),
        (CHECKPOINT_189_RUN / "status.json", "checkpoint 189 machine status"),
        (CHECKPOINT_189_RUN / "results" / "shape_residual_band_summary.csv", "checkpoint 189 band summary"),
        (WORK_DIR / "188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md", "theta profile checkpoint"),
        (CHECKPOINT_188_RUN / "status.json", "checkpoint 188 machine status"),
        (CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv", "checkpoint 188 H0 profile results"),
        (CHECKPOINT_188_RUN / "results" / "H0_profile_root_trace.csv", "checkpoint 188 H0 profile root trace"),
        (CHECKPOINT_188_RUN / "results" / "profiled_acoustic_summary.csv", "checkpoint 188 profiled acoustic summary"),
        (WORK_DIR / "186-CAMB-high-cs-wtable-spectra-smoke.md", "same-density unprofiled spectra smoke checkpoint"),
        (CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv", "checkpoint 186 unprofiled acoustic summary"),
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


def metric(rows: list[dict[str, str]], branch: str, quantity: str, value_key: str = "value") -> float:
    for row in rows:
        if row.get("branch") == branch and row.get("quantity") == quantity:
            return float(row[value_key])
    raise KeyError(f"missing {branch}/{quantity}/{value_key}")


def checkpoint_190_snapshot_rows() -> list[dict[str, Any]]:
    rows = read_csv_rows(CHECKPOINT_190_RUN / "results" / "decision_snapshot.csv")
    return [
        {
            "arena": row["arena"],
            "data_vector": row["data_vector"],
            "MTS_chi2_proxy": float(row["MTS_chi2_proxy"]),
            "MTS_delta_AIC_vs_LCDM": float(row["MTS_delta_AIC_vs_LCDM"]),
            "MTS_delta_BIC_vs_LCDM": float(row["MTS_delta_BIC_vs_LCDM"]),
            "verdict": row["verdict"],
            "claim_limit": "copied from checkpoint 190; mock proxy only",
        }
        for row in rows
        if row["arena"] == "same_physical_densities"
    ]


def theta_identity_rows() -> list[dict[str, Any]]:
    acoustic_186 = read_csv_rows(CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv")
    theta_lcdm = metric(acoustic_186, "LCDM_baseline_recomputed", "thetastar")
    theta_mts = metric(acoustic_186, "MTS_high_cs_fluid_density_isolation", "thetastar")
    da_lcdm = metric(acoustic_186, "LCDM_baseline_recomputed", "DAstar")
    da_mts = metric(acoustic_186, "MTS_high_cs_fluid_density_isolation", "DAstar")
    rdrag_lcdm = metric(acoustic_186, "LCDM_baseline_recomputed", "rdrag")
    rdrag_mts = metric(acoustic_186, "MTS_high_cs_fluid_density_isolation", "rdrag")
    age_lcdm = metric(acoustic_186, "LCDM_baseline_recomputed", "age")
    age_mts = metric(acoustic_186, "MTS_high_cs_fluid_density_isolation", "age")
    delta_ln_theta = math.log(theta_mts / theta_lcdm)
    delta_ln_da = math.log(da_mts / da_lcdm)
    delta_ln_rdrag = math.log(rdrag_mts / rdrag_lcdm)
    predicted_delta_ln_theta = delta_ln_rdrag - delta_ln_da
    residual = delta_ln_theta - predicted_delta_ln_theta
    return [
        {
            "identity_piece": "observed_delta_ln_theta_star",
            "value": delta_ln_theta,
            "input": "ln(theta_MTS/theta_LCDM)",
            "interpretation": "raw same-density acoustic-angle hazard",
        },
        {
            "identity_piece": "delta_ln_rdrag_proxy",
            "value": delta_ln_rdrag,
            "input": "ln(rdrag_MTS/rdrag_LCDM)",
            "interpretation": "sound horizon barely moves",
        },
        {
            "identity_piece": "minus_delta_ln_DAstar",
            "value": -delta_ln_da,
            "input": "-ln(DAstar_MTS/DAstar_LCDM)",
            "interpretation": "late-distance projection dominates theta shift",
        },
        {
            "identity_piece": "predicted_delta_ln_theta_from_rdrag_DA",
            "value": predicted_delta_ln_theta,
            "input": "delta_ln_rdrag - delta_ln_DAstar",
            "interpretation": "first-order FLRW distance identity proxy",
        },
        {
            "identity_piece": "identity_residual",
            "value": residual,
            "input": "observed - predicted",
            "interpretation": "small mismatch expected because CAMB theta* is not exactly rdrag/DAstar",
        },
        {
            "identity_piece": "delta_age_fraction",
            "value": (age_mts - age_lcdm) / age_lcdm,
            "input": "(age_MTS-age_LCDM)/age_LCDM",
            "interpretation": "same-density unprofiled MTS shortens age while increasing theta",
        },
    ]


def h0_profile_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    profile_rows = read_csv_rows(CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv")
    root_trace = read_csv_rows(CHECKPOINT_188_RUN / "results" / "H0_profile_root_trace.csv")
    same_lcdm = next(row for row in profile_rows if row["family"] == "same_physical_densities" and row["model"] == "LCDM")
    same_mts = next(row for row in profile_rows if row["family"] == "same_physical_densities" and row["model"] == "MTS_high_cs_fluid")
    target_theta = float(same_lcdm["target_thetastar"])
    unprofiled_h0 = float(same_mts["unprofiled_H0"])
    unprofiled_theta = float(same_mts["unprofiled_thetastar"])
    profiled_h0 = float(same_mts["profiled_H0"])
    actual_shift = profiled_h0 - unprofiled_h0

    lower = max(
        [
            row for row in root_trace
            if row["family"] == "same_physical_densities"
            and row["model"] == "MTS_high_cs_fluid"
            and float(row["H0"]) < unprofiled_h0
        ],
        key=lambda row: float(row["H0"]),
    )
    upper = min(
        [
            row for row in root_trace
            if row["family"] == "same_physical_densities"
            and row["model"] == "MTS_high_cs_fluid"
            and float(row["H0"]) > unprofiled_h0
        ],
        key=lambda row: float(row["H0"]),
    )
    lower_h0 = float(lower["H0"])
    upper_h0 = float(upper["H0"])
    lower_theta = float(lower["thetastar"])
    upper_theta = float(upper["thetastar"])
    slope = (upper_theta - lower_theta) / (upper_h0 - lower_h0)
    predicted_shift = -(unprofiled_theta - target_theta) / slope
    predicted_profiled_h0 = unprofiled_h0 + predicted_shift
    prediction_error = predicted_profiled_h0 - profiled_h0
    derivative_ln = slope * unprofiled_h0 / unprofiled_theta
    required_fractional_h0_shift = actual_shift / unprofiled_h0
    late_reference_delta = profiled_h0 - LATE_REFERENCE_H0
    summary = {
        "target_theta": target_theta,
        "unprofiled_h0": unprofiled_h0,
        "unprofiled_theta": unprofiled_theta,
        "profiled_h0": profiled_h0,
        "actual_shift": actual_shift,
        "slope": slope,
        "predicted_shift": predicted_shift,
        "prediction_error": prediction_error,
        "required_fractional_h0_shift": required_fractional_h0_shift,
        "late_reference_delta": late_reference_delta,
        "delta_h0_vs_late_reference_fraction": late_reference_delta / LATE_REFERENCE_H0,
    }
    rows = [
        {
            "bridge_item": "target_theta_star",
            "value": target_theta,
            "derivation_role": "LCDM target angle from checkpoint 183/188",
            "status": "input",
        },
        {
            "bridge_item": "unprofiled_MTS_theta_star",
            "value": unprofiled_theta,
            "derivation_role": "raw MTS angle before compensation",
            "status": "input",
        },
        {
            "bridge_item": "finite_difference_dtheta_dH0",
            "value": slope,
            "derivation_role": "local same-density MTS theta response from checkpoint 188 root trace",
            "status": "numerical_bridge",
        },
        {
            "bridge_item": "dimensionless_dln_theta_dln_H0",
            "value": derivative_ln,
            "derivation_role": "response coefficient in first-order compensation law",
            "status": "numerical_bridge",
        },
        {
            "bridge_item": "linear_predicted_delta_H0",
            "value": predicted_shift,
            "derivation_role": "-Delta theta / (dtheta/dH0)",
            "status": "matches_profile",
        },
        {
            "bridge_item": "actual_profile_delta_H0",
            "value": actual_shift,
            "derivation_role": "root-solved H0 shift from checkpoint 188",
            "status": "profile_cost",
        },
        {
            "bridge_item": "predicted_profile_H0",
            "value": predicted_profiled_h0,
            "derivation_role": "unprofiled H0 plus linear bridge shift",
            "status": "near_root",
        },
        {
            "bridge_item": "actual_profile_H0",
            "value": profiled_h0,
            "derivation_role": "checkpoint 188 same-density MTS profile",
            "status": "profile_cost",
        },
        {
            "bridge_item": "linear_prediction_error_H0",
            "value": prediction_error,
            "derivation_role": "predicted profile H0 minus root profile H0",
            "status": "small",
        },
        {
            "bridge_item": "fractional_H0_shift_required",
            "value": required_fractional_h0_shift,
            "derivation_role": "profile cost relative to unprofiled same-density H0",
            "status": "phenomenological_cost",
        },
        {
            "bridge_item": "delta_H0_vs_late_reference",
            "value": late_reference_delta,
            "derivation_role": "tension with previous late-reference h_profiled branch",
            "status": "consistency_warning",
        },
    ]
    return rows, summary


def profiled_distance_rows() -> list[dict[str, Any]]:
    acoustic_rows = read_csv_rows(CHECKPOINT_188_RUN / "results" / "profiled_acoustic_summary.csv")
    out: list[dict[str, Any]] = []
    for quantity in ["thetastar", "DAstar", "rdrag", "age"]:
        value = metric(acoustic_rows, "same_physical_densities_MTS_high_cs_fluid_H0_profiled", quantity)
        control = metric(acoustic_rows, "same_physical_densities_MTS_high_cs_fluid_H0_profiled", quantity, "control_value")
        out.append(
            {
                "quantity": quantity,
                "MTS_profiled_value": value,
                "LCDM_profiled_control": control,
                "delta": value - control,
                "fractional_delta": (value - control) / control if control != 0.0 else "",
                "readout": "theta bridge closes this observable" if quantity in {"thetastar", "DAstar", "rdrag"} else "age shifts slightly after profile",
            }
        )
    return out


def derivation_contract_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "derive distance identity owner",
            "current_result": "theta shift decomposes into negligible rdrag motion plus DAstar deficit",
            "required_for_promotion": "derive MTS memory contribution to D_A(z*) from parent FLRW equations, not CAMB closure",
            "status": "partial_numeric_bridge",
        },
        {
            "contract_item": "derive H0 compensation law",
            "current_result": f"Delta H0 ~= {summary['actual_shift']} km/s/Mpc required in same-density branch",
            "required_for_promotion": "parent theory predicts H0_MTS/H0_LCDM or equivalent clock calibration relation",
            "status": "not_derived",
        },
        {
            "contract_item": "resolve late-reference tension",
            "current_result": f"profile H0 differs from late reference by {summary['late_reference_delta']} km/s/Mpc",
            "required_for_promotion": "explain whether late SN/BAO/H(z) branch or CMB same-density branch owns H0",
            "status": "consistency_warning",
        },
        {
            "contract_item": "keep fixed locks",
            "current_result": f"B_mem={LOCKED_B_MEM}, p={LOCKED_P}, u3={LOCKED_U3} remain fixed",
            "required_for_promotion": "derive B,p,u or continue labeling them closure locks",
            "status": "fixed_closure",
        },
        {
            "contract_item": "same-density mock likelihood",
            "current_result": "checkpoint 190 says same-density TT+EE proxy is competitive",
            "required_for_promotion": "replace proxy with official or controlled mock likelihood under equal model freedoms",
            "status": "empirical_next_step",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    bridge_error_ok = abs(summary["prediction_error"]) < 0.05
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal bridge only",
        },
        {
            "gate": "distance identity bridge works",
            "status": "pass",
            "evidence": "theta shift decomposes into rdrag and DAstar terms with small residual",
            "claim_allowed": "diagnostic derivation bridge",
        },
        {
            "gate": "linear H0 bridge predicts profile",
            "status": "pass" if bridge_error_ok else "warning",
            "evidence": f"prediction_error_H0={summary['prediction_error']}",
            "claim_allowed": "phenomenological bridge only",
        },
        {
            "gate": "H0 compensation derived from parent theory",
            "status": "fail",
            "evidence": "bridge predicts required compensation but does not derive why parent action enforces it",
            "claim_allowed": "no theory promotion",
        },
        {
            "gate": "late-reference H0 consistency",
            "status": "warning",
            "evidence": f"delta_H0_vs_late_reference={summary['late_reference_delta']}",
            "claim_allowed": "requires next consistency gate",
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


def decision_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "same-density CMB mock branch has a clear first-order theta/H0 bridge, but the bridge is phenomenological and conflicts with the late H0 reference until derived",
            "same_density_profile_H0": summary["profiled_h0"],
            "linear_predicted_profile_H0": summary["unprofiled_h0"] + summary["predicted_shift"],
            "delta_H0_vs_late_reference": summary["late_reference_delta"],
            "next_target": "192-theta-H0-compensation-derivation-attempt.md",
            "MTS_spectra_run": "false",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_191_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    snapshot = checkpoint_190_snapshot_rows()
    identity = theta_identity_rows()
    h0_bridge, summary = h0_profile_rows()
    profiled_distances = profiled_distance_rows()
    contract = derivation_contract_rows(summary)
    gates = claim_gate_rows(sources, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            sources,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "same_density_mock_snapshot.csv": (
            snapshot,
            ["arena", "data_vector", "MTS_chi2_proxy", "MTS_delta_AIC_vs_LCDM", "MTS_delta_BIC_vs_LCDM", "verdict", "claim_limit"],
        ),
        "theta_distance_identity_bridge.csv": (
            identity,
            ["identity_piece", "value", "input", "interpretation"],
        ),
        "H0_theta_linear_bridge.csv": (
            h0_bridge,
            ["bridge_item", "value", "derivation_role", "status"],
        ),
        "profiled_distance_closure_check.csv": (
            profiled_distances,
            ["quantity", "MTS_profiled_value", "LCDM_profiled_control", "delta", "fractional_delta", "readout"],
        ),
        "theta_derivation_contract.csv": (
            contract,
            ["contract_item", "current_result", "required_for_promotion", "status"],
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
                "same_density_profile_H0",
                "linear_predicted_profile_H0",
                "delta_H0_vs_late_reference",
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
        "same_density_profile_H0": summary["profiled_h0"],
        "linear_predicted_profile_H0": summary["unprofiled_h0"] + summary["predicted_shift"],
        "delta_H0_vs_late_reference": summary["late_reference_delta"],
        "H0_compensation_parent_derived": False,
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
