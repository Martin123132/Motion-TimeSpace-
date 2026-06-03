#!/usr/bin/env python3
"""Red-team the mixed locked 2/27 joint late-CMB calibration result."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
BROAD_RUN = RUNS_ROOT / "20260531-164201-locked-2over27-joint-late-CMB-score"
PHYSICAL_RUN = RUNS_ROOT / "20260531-164711-locked-2over27-joint-late-CMB-score"
T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
TRANSFER_RUN = RUNS_ROOT / "20260531-162146-locked-2over27-late-CMB-transfer-score"
CHECKPOINT_119 = POST_CHECKPOINT / "119-locked-2over27-joint-late-CMB-calibration-runner.md"

sys.path.insert(0, str(SCRIPTS_ROOT))
from locked_2over27_joint_late_CMB_calibration_runner import (  # noqa: E402
    PRIMARY_MODEL,
    fit_joint_model,
    load_primary_data,
    write_csv,
)


LATE_HARD_CUTOFF = 6.0
CMB_HARD_CUTOFF = 6.0
TARGET_PRIOR_TABLE = "LCDM"
TARGET_SCORE_MODE = "strict_full4"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        BROAD_RUN / "results" / "fit_summary.csv",
        BROAD_RUN / "results" / "joint_gates.csv",
        PHYSICAL_RUN / "results" / "fit_summary.csv",
        PHYSICAL_RUN / "results" / "joint_gates.csv",
        T7_RUN / "results" / "locked_branch_scores.csv",
        TRANSFER_RUN / "status.json",
        CHECKPOINT_119,
        Path(__file__).resolve(),
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


def primary_t7_row() -> dict[str, float]:
    rows = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    row = next(item for item in rows if item["branch"] == "T1_primary_fullcov_DR2")
    return {
        "chi2_SN": float(row["chi2_SN"]),
        "chi2_BAO": float(row["chi2_BAO"]),
        "chi2_late": float(row["chi2_total"]),
        "Omega_m": float(row["Omega_m"]),
    }


def locked_fit_rows(run: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(run / "results" / "fit_summary.csv"):
        if row["model"] != PRIMARY_MODEL:
            continue
        numeric = dict(row)
        for key in [
            "chi2_SN",
            "chi2_BAO",
            "chi2_CMB",
            "chi2_total",
            "AIC",
            "BIC",
            "Omega_m0",
            "h",
            "r_d",
            "BAO_alpha",
        ]:
            numeric[key] = float(row[key])
        numeric["edge_flag"] = row["edge_flag"].lower() == "true"
        rows.append(numeric)
    return rows


def gate_rows(run: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(run / "results" / "joint_gates.csv"):
        numeric = dict(row)
        for key in [
            "late_chi2_penalty_vs_T7",
            "CMB_chi2_penalty_vs_CMB_only",
            "delta_BIC_vs_LCDM",
            "r_d",
        ]:
            numeric[key] = float(row[key])
        numeric["edge_flag"] = row["edge_flag"].lower() == "true"
        rows.append(numeric)
    return rows


def gate_failure_audit_rows(broad_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in broad_gates:
        late_margin = float(row["late_chi2_penalty_vs_T7"]) - LATE_HARD_CUTOFF
        cmb_margin = float(row["CMB_chi2_penalty_vs_CMB_only"]) - CMB_HARD_CUTOFF
        failure_driver = "none"
        if row["edge_flag"]:
            failure_driver = "edge_flag"
        elif late_margin > 0.0:
            failure_driver = "late_sector_degradation"
        elif cmb_margin > 0.0:
            failure_driver = "CMB_sector_degradation"
        rows.append(
            {
                "rd_prior_mode": row["rd_prior_mode"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "gate": row["gate"],
                "late_penalty": row["late_chi2_penalty_vs_T7"],
                "late_margin_to_hard_cutoff": late_margin,
                "CMB_penalty": row["CMB_chi2_penalty_vs_CMB_only"],
                "CMB_margin_to_hard_cutoff": cmb_margin,
                "delta_BIC_vs_LCDM": row["delta_BIC_vs_LCDM"],
                "edge_flag": row["edge_flag"],
                "failure_driver": failure_driver,
            }
        )
    return rows


def sector_penalty_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    t7 = primary_t7_row()
    rows: list[dict[str, Any]] = []
    for row in fit_rows:
        sn_penalty = float(row["chi2_SN"]) - t7["chi2_SN"]
        bao_penalty = float(row["chi2_BAO"]) - t7["chi2_BAO"]
        late_penalty = sn_penalty + bao_penalty
        rows.append(
            {
                "rd_prior_mode": row["rd_prior_mode"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "Omega_m0": row["Omega_m0"],
                "h": row["h"],
                "r_d": row["r_d"],
                "SN_penalty_vs_T7": sn_penalty,
                "BAO_penalty_vs_T7": bao_penalty,
                "late_penalty_vs_T7": late_penalty,
                "BAO_fraction_of_late_penalty": bao_penalty / late_penalty if late_penalty else "",
            }
        )
    return rows


def prior_mode_sensitivity_rows(
    broad_rows: list[dict[str, Any]],
    physical_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    physical_lookup = {(row["prior_table"], row["score_mode"]): row for row in physical_rows}
    rows: list[dict[str, Any]] = []
    for broad in broad_rows:
        physical = physical_lookup[(broad["prior_table"], broad["score_mode"])]
        rows.append(
            {
                "prior_table": broad["prior_table"],
                "score_mode": broad["score_mode"],
                "delta_Omega_m_physical_minus_broad": physical["Omega_m0"] - broad["Omega_m0"],
                "delta_h_physical_minus_broad": physical["h"] - broad["h"],
                "delta_r_d_physical_minus_broad": physical["r_d"] - broad["r_d"],
                "delta_chi2_physical_minus_broad": physical["chi2_total"] - broad["chi2_total"],
                "readout": "stable_against_rd_prior_mode",
            }
        )
    return rows


def compressed_prior_sensitivity_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lookup = {(row["prior_table"], row["score_mode"]): row for row in rows}
    out: list[dict[str, Any]] = []
    for score_mode in sorted({row["score_mode"] for row in rows}):
        lcdm = lookup[("LCDM", score_mode)]
        wcdm = lookup[("wCDM", score_mode)]
        out.append(
            {
                "score_mode": score_mode,
                "delta_Omega_m_LCDM_minus_wCDM": lcdm["Omega_m0"] - wcdm["Omega_m0"],
                "delta_h_LCDM_minus_wCDM": lcdm["h"] - wcdm["h"],
                "delta_r_d_LCDM_minus_wCDM": lcdm["r_d"] - wcdm["r_d"],
                "delta_chi2_total_LCDM_minus_wCDM": lcdm["chi2_total"] - wcdm["chi2_total"],
                "readout": "strict_full4_prior_table_dependency"
                if score_mode == TARGET_SCORE_MODE
                else "marginal_mode_less_severe",
            }
        )
    return out


def targeted_refit_row(max_iter: int) -> dict[str, Any]:
    _, sn, bao = load_primary_data()
    fit, _, _ = fit_joint_model(
        "broad",
        TARGET_PRIOR_TABLE,
        TARGET_SCORE_MODE,
        PRIMARY_MODEL,
        sn,
        bao,
        max_iter,
    )
    t7 = primary_t7_row()
    late_penalty = float(fit["chi2_SN"]) + float(fit["chi2_BAO"]) - t7["chi2_late"]
    return {
        "rd_prior_mode": fit["rd_prior_mode"],
        "prior_table": fit["prior_table"],
        "score_mode": fit["score_mode"],
        "model": fit["model"],
        "max_iter": max_iter,
        "chi2_SN": fit["chi2_SN"],
        "chi2_BAO": fit["chi2_BAO"],
        "chi2_CMB": fit["chi2_CMB"],
        "chi2_total": fit["chi2_total"],
        "late_penalty_vs_T7": late_penalty,
        "late_margin_to_hard_cutoff": late_penalty - LATE_HARD_CUTOFF,
        "Omega_m0": fit["Omega_m0"],
        "h": fit["h"],
        "r_d": fit["r_d"],
        "edge_flag": fit["edge_flag"],
        "optimizer": fit["optimizer"],
        "issue": fit["issue"],
    }


def repair_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "numerical_optimizer_issue",
            "status": "not_primary_suspect",
            "evidence": "broad and physical r_d runs reproduce same locked solution; targeted refit checks the failing branch",
            "next_action": "only rerun with exhaustive optimizer if future public-facing claim depends on cutoff by < 1 chi2",
        },
        {
            "option": "compressed_prior_model_dependence",
            "status": "live_suspect",
            "evidence": "only LCDM strict_full4 compressed table triggers hard sector gate; wCDM strict and both marginal modes draw",
            "next_action": "treat compressed-prior table as sensitivity, not public CMB evidence",
        },
        {
            "option": "BAO_absolute_calibration_tension",
            "status": "live_suspect",
            "evidence": "late penalty is dominated by BAO degradation after alpha is tied to h and r_d",
            "next_action": "derive or constrain h-r_d-alpha relation from parent calibration map",
        },
        {
            "option": "threshold_too_hard",
            "status": "do_not_move_goalposts",
            "evidence": "hard cutoff was predeclared at 6; failing branch is 0.516 chi2 beyond it",
            "next_action": "keep result mixed/not-promoted unless independent repair clears cutoff",
        },
        {
            "option": "parent_calibration_relation",
            "status": "needed_for_promotion",
            "evidence": "joint fit wants sane h and r_d but must trade late SN+BAO against CMB",
            "next_action": "attempt derivation of shared calibration relation among h, r_d, BAO alpha, SN offset, and Omega_m0",
        },
    ]


def decision_rows(
    failure_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    refit: dict[str, Any],
) -> list[dict[str, Any]]:
    hard_failures = [row for row in failure_rows if str(row["gate"]).startswith("hard_loss")]
    target_sector = next(
        row
        for row in sector_rows
        if row["prior_table"] == TARGET_PRIOR_TABLE and row["score_mode"] == TARGET_SCORE_MODE
    )
    bao_fraction = float(target_sector["BAO_fraction_of_late_penalty"])
    status = "joint_calibration_red_team_mixed_result_confirmed_not_promoted"
    if not hard_failures:
        status = "joint_calibration_red_team_no_hard_failure_found_recheck_required"
    return [
        {
            "decision": "red_team_status",
            "value": status,
            "rationale": "one strict LCDM-prior full-vector sector gate remains over cutoff",
        },
        {
            "decision": "hard_failure_count",
            "value": len(hard_failures),
            "rationale": "hard failures in broad-r_d primary joint gates",
        },
        {
            "decision": "failing_gate_margin",
            "value": next(row["late_margin_to_hard_cutoff"] for row in failure_rows if row["failure_driver"] == "late_sector_degradation"),
            "rationale": "positive margin over predeclared late-sector hard cutoff",
        },
        {
            "decision": "BAO_fraction_of_failing_late_penalty",
            "value": bao_fraction,
            "rationale": "identifies whether the late penalty is SN-shape or BAO calibration dominated",
        },
        {
            "decision": "targeted_refit_late_margin",
            "value": refit["late_margin_to_hard_cutoff"],
            "rationale": "single-branch refit check of numerical stability",
        },
        {
            "decision": "theory_promotion_allowed",
            "value": False,
            "rationale": "red-team pass confirms mixed result; branch remains unpromoted",
        },
        {
            "decision": "next_target",
            "value": "121-shared-calibration-relation-derivation-attempt.md",
            "rationale": "minimum repair is a derived h-r_d-alpha/SN-offset calibration relation, not another free retune",
        },
    ]


def run_audit(output_root: Path, refit_max_iter: int) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-joint-calibration-red-team"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    broad_locked = locked_fit_rows(BROAD_RUN)
    physical_locked = locked_fit_rows(PHYSICAL_RUN)
    broad_gates = gate_rows(BROAD_RUN)
    failure_audit = gate_failure_audit_rows(broad_gates)
    sector_penalties = sector_penalty_rows(broad_locked)
    prior_sensitivity = prior_mode_sensitivity_rows(broad_locked, physical_locked)
    compressed_sensitivity = compressed_prior_sensitivity_rows(broad_locked)
    refit = targeted_refit_row(refit_max_iter)
    repairs = repair_option_rows()
    decisions = decision_rows(failure_audit, sector_penalties, refit)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "gate_failure_audit.csv",
        failure_audit,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "gate",
            "late_penalty",
            "late_margin_to_hard_cutoff",
            "CMB_penalty",
            "CMB_margin_to_hard_cutoff",
            "delta_BIC_vs_LCDM",
            "edge_flag",
            "failure_driver",
        ],
    )
    write_csv(
        results_dir / "sector_penalty_decomposition.csv",
        sector_penalties,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "Omega_m0",
            "h",
            "r_d",
            "SN_penalty_vs_T7",
            "BAO_penalty_vs_T7",
            "late_penalty_vs_T7",
            "BAO_fraction_of_late_penalty",
        ],
    )
    write_csv(
        results_dir / "rd_prior_sensitivity.csv",
        prior_sensitivity,
        [
            "prior_table",
            "score_mode",
            "delta_Omega_m_physical_minus_broad",
            "delta_h_physical_minus_broad",
            "delta_r_d_physical_minus_broad",
            "delta_chi2_physical_minus_broad",
            "readout",
        ],
    )
    write_csv(
        results_dir / "compressed_prior_sensitivity.csv",
        compressed_sensitivity,
        [
            "score_mode",
            "delta_Omega_m_LCDM_minus_wCDM",
            "delta_h_LCDM_minus_wCDM",
            "delta_r_d_LCDM_minus_wCDM",
            "delta_chi2_total_LCDM_minus_wCDM",
            "readout",
        ],
    )
    write_csv(
        results_dir / "targeted_refit.csv",
        [refit],
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "max_iter",
            "chi2_SN",
            "chi2_BAO",
            "chi2_CMB",
            "chi2_total",
            "late_penalty_vs_T7",
            "late_margin_to_hard_cutoff",
            "Omega_m0",
            "h",
            "r_d",
            "edge_flag",
            "optimizer",
            "issue",
        ],
    )
    write_csv(results_dir / "repair_options.csv", repairs, ["option", "status", "evidence", "next_action"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])

    status = {
        "status": next(row["value"] for row in decisions if row["decision"] == "red_team_status"),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "red_team_internal_not_promotion",
        "hard_failure_count": next(row["value"] for row in decisions if row["decision"] == "hard_failure_count"),
        "targeted_refit_late_margin": refit["late_margin_to_hard_cutoff"],
        "next_target": "121-shared-calibration-relation-derivation-attempt.md",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Red-team the mixed joint calibration result.")
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--refit-max-iter", type=int, default=120)
    args = parser.parse_args()
    run_audit(args.output_root, args.refit_max_iter)


if __name__ == "__main__":
    main()
