#!/usr/bin/env python3
"""Audit whether the CMB bridge should pursue a BAO-shape owner or Q^nu owner."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"

BAO_SHAPE_RUN = RUNS_ROOT / "20260531-173800-BAO-shape-residual-decomposition"
BAO_SHAPE_RESULTS = BAO_SHAPE_RUN / "results"
BAO_ROW_RESIDUALS = BAO_SHAPE_RESULTS / "bao_row_residuals.csv"
BAO_BY_OBSERVABLE = BAO_SHAPE_RESULTS / "mts_delta_vs_T7_by_observable.csv"
BAO_BY_REDSHIFT = BAO_SHAPE_RESULTS / "mts_delta_vs_T7_by_redshift.csv"
BAO_DECISION = BAO_SHAPE_RESULTS / "decision.csv"

CALIBRATION_RUN = RUNS_ROOT / "20260531-235955-calibration-bridge-no-go-owner-contract"
CALIBRATION_RESULTS = CALIBRATION_RUN / "results"
CALIBRATION_STATUS = CALIBRATION_RUN / "status.json"
CALIBRATION_EVIDENCE = CALIBRATION_RESULTS / "calibration_evidence_table.csv"
CALIBRATION_OWNER_MATRIX = CALIBRATION_RESULTS / "owner_candidate_matrix.csv"

HZ_RUN = RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout"
HZ_DECISION = HZ_RUN / "results" / "decision.csv"
HZ_COMPARISONS = HZ_RUN / "results" / "baseline_comparisons.csv"

CLAIM_CEILING = "BAO_shape_or_Qnu_owner_contract_no_bridge_promotion"
FAILED_BRANCH_ID = "joint_tied_alpha__LCDM__strict_full4__MTS_locked_2over27"
T7_BRANCH_ID = "late_T7_locked_2over27_free_alpha__MTS_locked_2over27"


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("124-"):
        return "BAO shape residual decomposition checkpoint"
    if name.startswith("125-"):
        return "radial H(z) route gate"
    if name.startswith("145-"):
        return "fresh source-locked H(z) holdout"
    if name.startswith("152-"):
        return "calibration bridge no-go checkpoint"
    if name == "08-long-run-workflow.md":
        return "long-run workflow"
    if name.endswith(".csv") or name == "status.json":
        return "machine source output"
    return "script"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "124-BAO-shape-residual-decomposition.md",
        WORK_DIR / "125-BAO-shape-theorem-target-or-non-CMB-stress-route.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        WORK_DIR / "152-calibration-bridge-no-go-owner-contract.md",
        BAO_SHAPE_RUN / "status.json",
        BAO_ROW_RESIDUALS,
        BAO_BY_OBSERVABLE,
        BAO_BY_REDSHIFT,
        BAO_DECISION,
        CALIBRATION_STATUS,
        CALIBRATION_EVIDENCE,
        CALIBRATION_OWNER_MATRIX,
        HZ_DECISION,
        HZ_COMPARISONS,
        FORMALIZATION_WORKBENCH / "08-long-run-workflow.md",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def paired_target_rows() -> list[dict[str, Any]]:
    rows = read_csv_rows(BAO_ROW_RESIDUALS)
    branch_rows = [row for row in rows if row["branch_id"] == FAILED_BRANCH_ID]
    t7_by_index = {
        row["row_index"]: row for row in rows if row["branch_id"] == T7_BRANCH_ID
    }
    paired = []
    for row in branch_rows:
        t7 = t7_by_index[row["row_index"]]
        branch_pred = float(row["predicted"])
        t7_pred = float(t7["predicted"])
        branch_residual = float(row["residual"])
        t7_residual = float(t7["residual"])
        prediction_shift_to_T7 = branch_residual - t7_residual
        fractional_prediction_shift = prediction_shift_to_T7 / branch_pred
        observable = row["observable"]
        if observable == "DH_over_rs":
            inferred_delta_H_over_H = -fractional_prediction_shift
            owner_readout = "radial_H_target"
        elif observable == "DM_over_rs":
            inferred_delta_H_over_H = ""
            owner_readout = "transverse_integral_target"
        else:
            inferred_delta_H_over_H = ""
            owner_readout = "DV_mixed_target"
        paired.append(
            {
                "row_index": row["row_index"],
                "z": row["z"],
                "observable": observable,
                "observed": row["observed"],
                "failed_branch_predicted": branch_pred,
                "T7_predicted": t7_pred,
                "failed_branch_residual": branch_residual,
                "T7_residual": t7_residual,
                "prediction_shift_to_T7": prediction_shift_to_T7,
                "fractional_prediction_shift_to_T7": fractional_prediction_shift,
                "inferred_delta_H_over_H_if_DH": inferred_delta_H_over_H,
                "delta_chi2_contribution_vs_T7": float(row["cov_signed_chi2_contribution"]) - float(t7["cov_signed_chi2_contribution"]),
                "owner_readout": owner_readout,
            }
        )
    return paired


def selected_observable_summary() -> list[dict[str, Any]]:
    return [
        row
        for row in read_csv_rows(BAO_BY_OBSERVABLE)
        if row["branch_id"] == FAILED_BRANCH_ID
    ]


def selected_redshift_summary() -> list[dict[str, Any]]:
    return [
        row
        for row in read_csv_rows(BAO_BY_REDSHIFT)
        if row["branch_id"] == FAILED_BRANCH_ID
    ]


def pure_metric_consistency_rows(target_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dh_rows = [row for row in target_rows if row["observable"] == "DH_over_rs"]
    dm_rows = [row for row in target_rows if row["observable"] == "DM_over_rs"]
    dh_need_lower_h = [
        row
        for row in dh_rows
        if isinstance(row["inferred_delta_H_over_H_if_DH"], float)
        and row["inferred_delta_H_over_H_if_DH"] < 0.0
    ]
    dm_need_lower_distance = [
        row
        for row in dm_rows
        if float(row["fractional_prediction_shift_to_T7"]) < 0.0
    ]
    high_z_dh = [
        row
        for row in dh_need_lower_h
        if float(row["z"]) >= 0.7
    ]
    max_abs_dh_h = max(abs(float(row["inferred_delta_H_over_H_if_DH"])) for row in dh_rows)
    max_abs_dm = max(abs(float(row["fractional_prediction_shift_to_T7"])) for row in dm_rows)
    return [
        {
            "test": "DH_radial_target",
            "result": f"{len(dh_need_lower_h)}/{len(dh_rows)} DH rows require lower H than the failed joint branch",
            "readout": "radial correction pressure is real",
            "risk": "lower H also tends to raise DM in a single-metric distance integral",
        },
        {
            "test": "high_z_DH_radial_target",
            "result": f"{len(high_z_dh)} DH rows at z>=0.7 require lower H; max |deltaH/H|={max_abs_dh_h:.6g}",
            "readout": "radial pressure strengthens at high z",
            "risk": "looks like a smooth shape/inference correction, not a scalar alpha shift",
        },
        {
            "test": "DM_integral_sign",
            "result": f"{len(dm_need_lower_distance)}/{len(dm_rows)} DM rows require lower DM than the failed joint branch; max |deltaDM/DM|={max_abs_dm:.6g}",
            "readout": "pure lower-H correction conflicts with most transverse targets",
            "risk": "single scalar H(z) repair is not enough",
        },
        {
            "test": "single_metric_pure_H_owner",
            "result": "fails_as_complete_owner",
            "readout": "DH wants lower H while most DM rows want lower distance; an owner must be anisotropic/projective or inference-level",
            "risk": "do not claim a BAO-shape theorem from radial residuals alone",
        },
    ]


def owner_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "scalar_alpha_or_rd",
            "status": "rejected",
            "why": "checkpoint 152 shows tied alpha is already same-shape optimum to O(1e-8)",
            "owner_needed": "none; not the lever",
            "local_GR_risk": "low",
            "next_action": "do not pursue",
        },
        {
            "route": "pure_single_metric_Hz_shape",
            "status": "insufficient",
            "why": "DH rows require lower H, but most DM rows require lower transverse distance",
            "owner_needed": "a radial pressure law plus proof of transverse integral consistency",
            "local_GR_risk": "medium",
            "next_action": "only pursue if a projection term also appears",
        },
        {
            "route": "anisotropic_BAO_projection_owner",
            "status": "best_shape_route",
            "why": "can in principle alter radial DH and transverse DM differently without matter exchange",
            "owner_needed": "parent redshift/ruler projection tensor with zero-memory identity limit",
            "local_GR_risk": "medium",
            "next_action": "derive a projection tensor or demote",
        },
        {
            "route": "screened_Qnu_matter_memory_exchange",
            "status": "high_risk_fallback",
            "why": "can move Omega_m0 early-to-late but threatens local GR, growth, and conservation",
            "owner_needed": "covariant Q^nu with Q^nu->0 locally and no fitted growth fudge",
            "local_GR_risk": "high",
            "next_action": "avoid until shape/projection route fails",
        },
        {
            "route": "full_Boltzmann_inference_map",
            "status": "needed_eventually",
            "why": "compressed priors may misrepresent the actual CMB response",
            "owner_needed": "CMB kill-screen engine/wrapper from checkpoint 151",
            "local_GR_risk": "low",
            "next_action": "run after engine exists or after projection theorem is written",
        },
    ]


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "zero_memory_identity",
            "condition": "B_mem -> 0 implies delta_BAO_shape -> 0 and Q^nu -> 0",
            "status": "mandatory",
            "failure_if_missing": "baseline parity violation",
        },
        {
            "gate": "radial_transverse_consistency",
            "condition": "derive DH, DM, and DV corrections together; no row-by-row residual fitting",
            "status": "missing",
            "failure_if_missing": "BAO-shape patch only",
        },
        {
            "gate": "covariant_owner",
            "condition": "projection tensor or exchange current follows from parent action/constraint",
            "status": "missing",
            "failure_if_missing": "closure-only",
        },
        {
            "gate": "H_z_holdout_compatibility",
            "condition": "independent CC H(z) remains draw/preferred after any radial correction",
            "status": "not_tested_for_new_owner",
            "failure_if_missing": "BAO repair breaks H(z)",
        },
        {
            "gate": "growth_and_local_silence",
            "condition": "no fitted mu/sigma8 rescue; Q^nu/projection vanishes in local/PPN regimes",
            "status": "mandatory",
            "failure_if_missing": "field-theory promotion fails",
        },
        {
            "gate": "CMB_spectra_kill_screen",
            "condition": "survive TT/TE/EE/lensing under same owner and same locks",
            "status": "not_run",
            "failure_if_missing": "no CMB claim",
        },
    ]


def gate_rows(target_rows: list[dict[str, Any]], consistency: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dh_rows = [row for row in target_rows if row["observable"] == "DH_over_rs"]
    max_dh_h = max(abs(float(row["inferred_delta_H_over_H_if_DH"])) for row in dh_rows)
    dm_lower = sum(
        1
        for row in target_rows
        if row["observable"] == "DM_over_rs" and float(row["fractional_prediction_shift_to_T7"]) < 0.0
    )
    dm_total = sum(1 for row in target_rows if row["observable"] == "DM_over_rs")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited BAO/calibration/H(z) artifacts exist",
        },
        {
            "gate": "BAO_shape_target_localized",
            "status": "pass",
            "evidence": "checkpoint 124 localizes failed gate to BAO shape residuals",
        },
        {
            "gate": "radial_DH_target",
            "status": "pass_target_defined",
            "evidence": f"max inferred |deltaH/H| from DH rows={max_dh_h:.6g}",
        },
        {
            "gate": "pure_Hz_shape_owner",
            "status": "fail_as_complete_owner",
            "evidence": f"{dm_lower}/{dm_total} DM rows require lower transverse distance while DH repair generally lowers H",
        },
        {
            "gate": "anisotropic_projection_owner",
            "status": "live_theorem_target",
            "evidence": "only route that can separate radial and transverse BAO shape without immediate Q^nu exchange",
        },
        {
            "gate": "Qnu_owner",
            "status": "defer_high_risk",
            "evidence": "Q^nu could move Omega but risks local GR/growth unless screened",
        },
        {
            "gate": "bridge_promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "BAO_shape_owner_route_sharpened_pure_Hz_repair_rejected_Qnu_deferred",
            "evidence": "radial DH target exists, but pure H(z) correction conflicts with transverse DM targets; anisotropic projection is live",
        },
        {
            "item": "best_next_target",
            "verdict": "154-anisotropic-BAO-projection-owner-attempt.md",
            "evidence": "derive or reject a parent projection tensor before risking Q^nu exchange",
        },
        {
            "item": "Qnu_status",
            "verdict": "fallback_only",
            "evidence": "Q^nu remains possible but threatens local-GR and growth constraints",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no BAO-shape correction, no Q^nu map, no CMB bridge promotion",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-BAO-shape-or-Qnu-bridge-owner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    target_rows = paired_target_rows()
    observable_rows = selected_observable_summary()
    redshift_rows = selected_redshift_summary()
    consistency = pure_metric_consistency_rows(target_rows)
    owners = owner_route_rows()
    theorem_contract = theorem_contract_rows()
    gates = gate_rows(target_rows, consistency)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "failed_gate_shape_target_rows.csv",
        target_rows,
        [
            "row_index",
            "z",
            "observable",
            "observed",
            "failed_branch_predicted",
            "T7_predicted",
            "failed_branch_residual",
            "T7_residual",
            "prediction_shift_to_T7",
            "fractional_prediction_shift_to_T7",
            "inferred_delta_H_over_H_if_DH",
            "delta_chi2_contribution_vs_T7",
            "owner_readout",
        ],
    )
    write_csv(
        results_dir / "observable_shape_summary.csv",
        observable_rows,
        [
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "observable",
            "rows",
            "delta_signed_chi2_sum_vs_T7",
            "positive_delta_sum",
            "negative_delta_sum",
            "abs_delta_sum",
        ],
    )
    write_csv(
        results_dir / "redshift_shape_summary.csv",
        redshift_rows,
        [
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "z",
            "rows",
            "delta_signed_chi2_sum_vs_T7",
            "positive_delta_sum",
            "negative_delta_sum",
            "abs_delta_sum",
        ],
    )
    write_csv(results_dir / "pure_metric_consistency.csv", consistency, ["test", "result", "readout", "risk"])
    write_csv(results_dir / "owner_route_matrix.csv", owners, ["route", "status", "why", "owner_needed", "local_GR_risk", "next_action"])
    write_csv(results_dir / "theorem_contract.csv", theorem_contract, ["gate", "condition", "status", "failure_if_missing"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    dh_rows = [row for row in target_rows if row["observable"] == "DH_over_rs"]
    max_dh_h = max(abs(float(row["inferred_delta_H_over_H_if_DH"])) for row in dh_rows)
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "failed_branch_id": FAILED_BRANCH_ID,
        "comparison_branch_id": T7_BRANCH_ID,
        "max_inferred_abs_delta_H_over_H_from_DH": max_dh_h,
        "generated": [
            "source_register.csv",
            "failed_gate_shape_target_rows.csv",
            "observable_shape_summary.csv",
            "redshift_shape_summary.csv",
            "pure_metric_consistency.csv",
            "owner_route_matrix.csv",
            "theorem_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "154-anisotropic-BAO-projection-owner-attempt.md",
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
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
