#!/usr/bin/env python3
"""Late-time to CMB transfer gate for the locked B_mem=2/27 branch."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import optimize


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
CMB_SCORE_RUN = RUNS_ROOT / "20260531-161215-locked-2over27-CMB-distance-score"
CONTRACT_115 = POST_CHECKPOINT / "115-locked-2over27-CMB-parameter-map-contract.md"
CHECKPOINT_116 = POST_CHECKPOINT / "116-locked-2over27-CMB-distance-score.md"

sys.path.insert(0, str(SCRIPTS_ROOT))
from locked_2over27_CMB_distance_score import (  # noqa: E402
    LOCKED_B_MEM,
    LOCKED_DELTA_R,
    LOCKED_P,
    LOCKED_U3,
    MODEL_ORDER,
    PRIMARY_PRIOR_TABLES,
    SCORE_MODES,
    cmb_prediction,
    prior_table_data,
    score_prediction,
    write_csv,
)


H_BOUNDS = (0.45, 0.90)
PRIMARY_LATE_BRANCH = "T1_primary_fullcov_DR2"
TRANSFER_DELTA_CHI2_PASS = 2.0
TRANSFER_DELTA_CHI2_SOFT = 6.0


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_exists_rows() -> list[dict[str, Any]]:
    paths = [
        T7_RUN / "results" / "locked_branch_scores.csv",
        T7_RUN / "results" / "locked_branch_comparisons.csv",
        CMB_SCORE_RUN / "results" / "fit_summary.csv",
        CMB_SCORE_RUN / "results" / "scorecard_gates.csv",
        CONTRACT_115,
        CHECKPOINT_116,
        Path(__file__).resolve(),
    ]
    return [
        {
            "artifact": path.name,
            "path": str(path),
            "exists": path.exists(),
            "kind": "source",
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def late_branch_rows() -> list[dict[str, Any]]:
    raw_rows = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        rows.append(
            {
                "branch": row["branch"],
                "role": row["role"],
                "source_run": row["source_run"],
                "sn_rows": int(row["sn_rows"]),
                "bao_rows": int(row["bao_rows"]),
                "sn_covariance_mode": row["sn_covariance_mode"],
                "sn_observable": row["sn_observable"],
                "bao_label": row["bao_label"],
                "Omega_m_late": float(row["Omega_m"]),
                "B_mem": float(row["B_mem"]),
                "chi2_late_total": float(row["chi2_total"]),
                "AIC_late": float(row["AIC"]),
                "BIC_late": float(row["BIC"]),
                "late_edge_flag": row["Omega_m_edge_flag"],
                "claim_ceiling": row["claim_ceiling"],
            }
        )
    return rows


def cmb_anchor_rows() -> list[dict[str, Any]]:
    raw_rows = read_csv_rows(CMB_SCORE_RUN / "results" / "fit_summary.csv")
    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        if row["model"] != "MTS_locked_2over27":
            continue
        rows.append(
            {
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "model": row["model"],
                "Omega_m_CMB_only": float(row["Omega_m0"]),
                "h_CMB_only": float(row["h"]),
                "chi2_CMB_only": float(row["chi2"]),
                "AIC_CMB_only": float(row["aic"]),
                "BIC_CMB_only": float(row["bic"]),
                "CMB_only_edge_flag": row["edge_flag"],
            }
        )
    return rows


def anchor_lookup(cmb_rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(row["prior_table"], row["score_mode"]): row for row in cmb_rows}


def h_edge_flag(h: float) -> bool:
    span = H_BOUNDS[1] - H_BOUNDS[0]
    return (h - H_BOUNDS[0]) / span <= 0.01 or (H_BOUNDS[1] - h) / span <= 0.01


def profile_h_for_fixed_omega(
    prior_table: str,
    score_mode: str,
    omega_m_late: float,
) -> tuple[float, float, dict[str, float], list[dict[str, Any]]]:
    prior_data = prior_table_data(prior_table)

    def objective(h: float) -> float:
        try:
            values = {"Omega_m0": omega_m_late, "h": float(h)}
            prediction = cmb_prediction("MTS_locked_2over27", values, prior_data["means"])
            chi2, _, _, _ = score_prediction(prediction, prior_data, score_mode)
            return chi2 if math.isfinite(chi2) else 1.0e100
        except Exception:  # noqa: BLE001
            return 1.0e100

    result = optimize.minimize_scalar(
        objective,
        bounds=H_BOUNDS,
        method="bounded",
        options={"xatol": 1.0e-11, "maxiter": 300},
    )
    best_h = float(result.x)
    best_chi2 = float(result.fun)
    values = {"Omega_m0": omega_m_late, "h": best_h}
    prediction = cmb_prediction("MTS_locked_2over27", values, prior_data["means"])
    _, observed, predicted, residual = score_prediction(prediction, prior_data, score_mode)
    residual_rows = []
    for parameter, obs, pred, res in zip(SCORE_MODES[score_mode], observed, predicted, residual, strict=True):
        residual_rows.append(
            {
                "prior_table": prior_table,
                "score_mode": score_mode,
                "parameter": parameter,
                "observed": float(obs),
                "predicted": float(pred),
                "residual_observed_minus_predicted": float(res),
            }
        )
    return best_chi2, best_h, prediction, residual_rows


def transfer_profile_rows(
    late_rows: list[dict[str, Any]],
    cmb_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    anchors = anchor_lookup(cmb_rows)
    transfer_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for late in late_rows:
        for prior_table in PRIMARY_PRIOR_TABLES:
            for score_mode in SCORE_MODES:
                anchor = anchors[(prior_table, score_mode)]
                chi2, h, prediction, residuals = profile_h_for_fixed_omega(
                    prior_table,
                    score_mode,
                    float(late["Omega_m_late"]),
                )
                delta_chi2 = chi2 - float(anchor["chi2_CMB_only"])
                delta_omega = float(late["Omega_m_late"]) - float(anchor["Omega_m_CMB_only"])
                delta_h = h - float(anchor["h_CMB_only"])
                edge = h_edge_flag(h)
                transfer_rows.append(
                    {
                        "branch": late["branch"],
                        "role": late["role"],
                        "prior_table": prior_table,
                        "score_mode": score_mode,
                        "Omega_m_late": late["Omega_m_late"],
                        "h_profiled": h,
                        "chi2_transfer": chi2,
                        "chi2_CMB_only": anchor["chi2_CMB_only"],
                        "delta_chi2_vs_CMB_only": delta_chi2,
                        "Omega_m_CMB_only": anchor["Omega_m_CMB_only"],
                        "delta_Omega_m_late_minus_CMB": delta_omega,
                        "h_CMB_only": anchor["h_CMB_only"],
                        "delta_h_profile_minus_CMB": delta_h,
                        "h_edge_flag": edge,
                        "z_star": prediction["z_star"],
                        "r_s_star": prediction["r_s_star"],
                        "D_M_star": prediction["D_M_star"],
                    }
                )
                for row in residuals:
                    row.update(
                        {
                            "branch": late["branch"],
                            "Omega_m_late": late["Omega_m_late"],
                            "h_profiled": h,
                        }
                    )
                    residual_rows.append(row)
    return transfer_rows, residual_rows


def transfer_gate_label(delta_chi2: float, h_edge: bool) -> str:
    if h_edge:
        return "blocked_h_edge"
    if delta_chi2 <= TRANSFER_DELTA_CHI2_PASS:
        return "pass_geometry_transfer"
    if delta_chi2 <= TRANSFER_DELTA_CHI2_SOFT:
        return "soft_tension"
    return "fail_geometry_transfer"


def transfer_gate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for row in rows:
        gates.append(
            {
                "branch": row["branch"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "gate": transfer_gate_label(
                    float(row["delta_chi2_vs_CMB_only"]),
                    str(row["h_edge_flag"]).lower() == "true",
                ),
                "delta_chi2_vs_CMB_only": row["delta_chi2_vs_CMB_only"],
                "h_profiled": row["h_profiled"],
                "h_edge_flag": row["h_edge_flag"],
                "delta_Omega_m_late_minus_CMB": row["delta_Omega_m_late_minus_CMB"],
                "claim_ceiling": "geometry_transfer_with_h_profiled_not_absolute_calibration",
            }
        )
    gates.append(
        {
            "branch": "all",
            "prior_table": "all",
            "score_mode": "all",
            "gate": "absolute_H0_rd_calibration_blocked",
            "delta_chi2_vs_CMB_only": "",
            "h_profiled": "",
            "h_edge_flag": "",
            "delta_Omega_m_late_minus_CMB": "",
            "claim_ceiling": "late_SN_BAO_shape_plus_BAO_alpha_does_not_fix_absolute_h_or_rd",
        }
    )
    return gates


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = [
        row
        for row in gates
        if row["branch"] == PRIMARY_LATE_BRANCH
        and row["prior_table"] in PRIMARY_PRIOR_TABLES
        and row["score_mode"] in SCORE_MODES
    ]
    pass_count = sum(row["gate"] == "pass_geometry_transfer" for row in primary)
    soft_count = sum(row["gate"] == "soft_tension" for row in primary)
    fail_count = sum(row["gate"] in {"fail_geometry_transfer", "blocked_h_edge"} for row in primary)
    if fail_count:
        status = "locked_2over27_late_to_CMB_transfer_geometry_fail"
    elif soft_count:
        status = "locked_2over27_late_to_CMB_transfer_geometry_soft_tension"
    elif pass_count == len(primary) and primary:
        status = "locked_2over27_late_to_CMB_transfer_geometry_pass_h_free"
    else:
        status = "locked_2over27_late_to_CMB_transfer_geometry_inconclusive"
    return [
        {
            "decision": "transfer_status",
            "value": status,
            "rationale": "primary T1 late Omega_m is transferred to CMB with h profiled, not fitted Omega_m reset",
        },
        {
            "decision": "primary_gate_count",
            "value": len(primary),
            "rationale": "wCDM/LCDM prior tables times strict/marginal score modes",
        },
        {
            "decision": "primary_pass_count",
            "value": pass_count,
            "rationale": "delta chi2 <= 2 and no h edge",
        },
        {
            "decision": "primary_soft_count",
            "value": soft_count,
            "rationale": "2 < delta chi2 <= 6",
        },
        {
            "decision": "primary_fail_count",
            "value": fail_count,
            "rationale": "delta chi2 > 6 or h edge",
        },
        {
            "decision": "absolute_calibration_claim_allowed",
            "value": False,
            "rationale": "late SN+BAO shape branch profiled BAO alpha and did not lock h/r_d",
        },
        {
            "decision": "theory_promotion_allowed",
            "value": False,
            "rationale": "this is a transfer gate, not a parent-action derivation or perturbation CMB test",
        },
        {
            "decision": "next_target",
            "value": "118-locked-2over27-joint-late-CMB-calibration-contract.md",
            "rationale": "next discriminator must tie h, r_d/BAO alpha, SN offset, and CMB distance in one shared calibration map",
        },
    ]


def run_dry_run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-late-CMB-transfer-dryrun"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    source_rows = file_exists_rows()
    late_rows = late_branch_rows()
    cmb_rows = cmb_anchor_rows()
    gates = [
        {
            "gate": "source_artifacts_exist",
            "status": "pass" if all(row["exists"] for row in source_rows) else "fail",
            "evidence": f"missing_count={sum(not row['exists'] for row in source_rows)}",
        },
        {
            "gate": "late_locked_branches_loaded",
            "status": "pass" if len(late_rows) >= 1 else "fail",
            "evidence": f"late_rows={len(late_rows)}",
        },
        {
            "gate": "CMB_anchor_rows_loaded",
            "status": "pass" if len(cmb_rows) == 4 else "fail",
            "evidence": f"cmb_rows={len(cmb_rows)}",
        },
        {
            "gate": "score_allowed",
            "status": "pass",
            "evidence": "late Omega_m transfer with h-profile only; no absolute calibration claim",
        },
    ]
    write_csv(results_dir / "source_register.csv", source_rows, ["artifact", "path", "exists", "kind", "issue"])
    write_csv(
        results_dir / "late_branch_register.csv",
        late_rows,
        [
            "branch",
            "role",
            "source_run",
            "sn_rows",
            "bao_rows",
            "sn_covariance_mode",
            "sn_observable",
            "bao_label",
            "Omega_m_late",
            "B_mem",
            "chi2_late_total",
            "AIC_late",
            "BIC_late",
            "late_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "cmb_anchor_register.csv",
        cmb_rows,
        [
            "prior_table",
            "score_mode",
            "model",
            "Omega_m_CMB_only",
            "h_CMB_only",
            "chi2_CMB_only",
            "AIC_CMB_only",
            "BIC_CMB_only",
            "CMB_only_edge_flag",
        ],
    )
    write_csv(results_dir / "dryrun_gates.csv", gates, ["gate", "status", "evidence"])
    decisions = [
        {
            "decision": "dryrun_status",
            "value": "locked_2over27_late_CMB_transfer_dryrun_pass"
            if all(row["status"] == "pass" for row in gates)
            else "locked_2over27_late_CMB_transfer_dryrun_fail",
            "rationale": "required source artifacts and anchors are available",
        },
        {
            "decision": "score_ran",
            "value": False,
            "rationale": "dry-run only",
        },
    ]
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])
    status = {
        "status": decisions[0]["value"],
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": False,
        "late_rows": len(late_rows),
        "cmb_anchor_rows": len(cmb_rows),
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def run_score(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-late-CMB-transfer-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = file_exists_rows()
    late_rows = late_branch_rows()
    cmb_rows = cmb_anchor_rows()
    profile_rows, residual_rows = transfer_profile_rows(late_rows, cmb_rows)
    gates = transfer_gate_rows(profile_rows)
    decisions = decision_rows(gates)

    write_csv(results_dir / "source_register.csv", source_rows, ["artifact", "path", "exists", "kind", "issue"])
    write_csv(
        results_dir / "late_branch_register.csv",
        late_rows,
        [
            "branch",
            "role",
            "source_run",
            "sn_rows",
            "bao_rows",
            "sn_covariance_mode",
            "sn_observable",
            "bao_label",
            "Omega_m_late",
            "B_mem",
            "chi2_late_total",
            "AIC_late",
            "BIC_late",
            "late_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "cmb_anchor_register.csv",
        cmb_rows,
        [
            "prior_table",
            "score_mode",
            "model",
            "Omega_m_CMB_only",
            "h_CMB_only",
            "chi2_CMB_only",
            "AIC_CMB_only",
            "BIC_CMB_only",
            "CMB_only_edge_flag",
        ],
    )
    write_csv(
        results_dir / "transfer_profile.csv",
        profile_rows,
        [
            "branch",
            "role",
            "prior_table",
            "score_mode",
            "Omega_m_late",
            "h_profiled",
            "chi2_transfer",
            "chi2_CMB_only",
            "delta_chi2_vs_CMB_only",
            "Omega_m_CMB_only",
            "delta_Omega_m_late_minus_CMB",
            "h_CMB_only",
            "delta_h_profile_minus_CMB",
            "h_edge_flag",
            "z_star",
            "r_s_star",
            "D_M_star",
        ],
    )
    write_csv(
        results_dir / "transfer_residuals.csv",
        residual_rows,
        [
            "branch",
            "Omega_m_late",
            "h_profiled",
            "prior_table",
            "score_mode",
            "parameter",
            "observed",
            "predicted",
            "residual_observed_minus_predicted",
        ],
    )
    write_csv(
        results_dir / "transfer_gates.csv",
        gates,
        [
            "branch",
            "prior_table",
            "score_mode",
            "gate",
            "delta_chi2_vs_CMB_only",
            "h_profiled",
            "h_edge_flag",
            "delta_Omega_m_late_minus_CMB",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])

    status = {
        "status": next(row["value"] for row in decisions if row["decision"] == "transfer_status"),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": True,
        "claim_ceiling": "late_to_CMB_geometry_transfer_with_h_profiled_not_absolute_calibration",
        "late_rows": len(late_rows),
        "profile_rows": len(profile_rows),
        "locked_constants": {
            "DeltaR": LOCKED_DELTA_R,
            "B_mem": LOCKED_B_MEM,
            "p": LOCKED_P,
            "u3": LOCKED_U3,
        },
        "primary_branch": PRIMARY_LATE_BRANCH,
        "next_target": "118-locked-2over27-joint-late-CMB-calibration-contract.md",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Late-time to CMB transfer gate for locked 2/27.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--score", action="store_true")
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    args = parser.parse_args()
    if args.dry_run:
        run_dry_run(args.output_root)
    else:
        run_score(args.output_root)


if __name__ == "__main__":
    main()
