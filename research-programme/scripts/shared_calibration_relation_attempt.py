"""Quantify whether a shared late/CMB calibration relation can repair the locked branch.

This is an internal derivation-audit script.  It does not add a new fitted
cosmology model; it measures the exact calibration deformation a future parent
action would need to justify.
"""

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

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import locked_2over27_joint_late_CMB_calibration_runner as joint  # noqa: E402

T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
JOINT_RUN = RUNS_ROOT / "20260531-164201-locked-2over27-joint-late-CMB-score"
RED_TEAM_RUN = RUNS_ROOT / "20260531-165759-joint-calibration-red-team"
PRIMARY_BRANCH = "T1_primary_fullcov_DR2"
PRIMARY_MODEL = "MTS_locked_2over27"
LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
        T7_RUN / "results" / "locked_branch_scores.csv",
        JOINT_RUN / "results" / "fit_summary.csv",
        JOINT_RUN / "results" / "joint_gates.csv",
        RED_TEAM_RUN / "results" / "sector_penalty_decomposition.csv",
        WORK_DIR / "118-locked-2over27-joint-late-CMB-calibration-contract.md",
        WORK_DIR / "120-joint-calibration-red-team-and-repair-options.md",
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


def primary_t7_score() -> dict[str, Any]:
    scores = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    matches = [row for row in scores if row["branch"] == PRIMARY_BRANCH]
    if len(matches) != 1:
        raise RuntimeError(f"expected one {PRIMARY_BRANCH} row, found {len(matches)}")
    row = matches[0]
    return {
        "branch": row["branch"],
        "Omega_m0": float(row["Omega_m"]),
        "DeltaR": float(row["DeltaR"]),
        "B_mem": float(row["B_mem"]),
        "p": LOCKED_P,
        "u3": LOCKED_U3,
        "chi2_SN_reported": float(row["chi2_SN"]),
        "chi2_BAO_reported": float(row["chi2_BAO"]),
        "chi2_late_reported": float(row["chi2_total"]),
    }


def locked_params(omega_m0: float) -> dict[str, float]:
    return {
        "Omega_m": float(omega_m0),
        "B_mem": LOCKED_B_MEM,
        "p": LOCKED_P,
        "u3": LOCKED_U3,
    }


def t7_free_alpha_target(sn: dict[str, Any], bao: dict[str, Any]) -> dict[str, Any]:
    t7 = primary_t7_score()
    params = locked_params(t7["Omega_m0"])
    chi2_sn, sn_offset, _, _ = snbao.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
    chi2_bao, alpha_free, _, _ = snbao.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
    return {
        "branch": PRIMARY_BRANCH,
        "Omega_m0": t7["Omega_m0"],
        "DeltaR": LOCKED_DELTA_R,
        "B_mem": LOCKED_B_MEM,
        "p": LOCKED_P,
        "u3": LOCKED_U3,
        "SN_offset": sn_offset,
        "alpha_free": alpha_free,
        "chi2_SN_recomputed": chi2_sn,
        "chi2_BAO_recomputed": chi2_bao,
        "chi2_late_recomputed": chi2_sn + chi2_bao,
        "chi2_SN_reported": t7["chi2_SN_reported"],
        "chi2_BAO_reported": t7["chi2_BAO_reported"],
        "chi2_late_reported": t7["chi2_late_reported"],
        "abs_chi2_late_diff": abs((chi2_sn + chi2_bao) - t7["chi2_late_reported"]),
        "status": "reproduced" if abs((chi2_sn + chi2_bao) - t7["chi2_late_reported"]) < 0.01 else "check_difference",
    }


def joint_gate_lookup() -> dict[tuple[str, str, str, str], dict[str, str]]:
    rows = read_csv_rows(JOINT_RUN / "results" / "joint_gates.csv")
    return {
        (row["rd_prior_mode"], row["prior_table"], row["score_mode"], row["model"]): row
        for row in rows
    }


def mts_joint_rows() -> list[dict[str, str]]:
    rows = read_csv_rows(JOINT_RUN / "results" / "fit_summary.csv")
    return [
        row
        for row in rows
        if row.get("rd_prior_mode") == "broad" and row.get("model") == PRIMARY_MODEL
    ]


def calibration_target_rows(bao: dict[str, Any], t7_target: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gates = joint_gate_lookup()
    alpha_t7 = float(t7_target["alpha_free"])
    chi2_bao_t7 = float(t7_target["chi2_BAO_recomputed"])

    for row in mts_joint_rows():
        omega_m0 = float(row["Omega_m0"])
        h_value = float(row["h"])
        r_d = float(row["r_d"])
        values = {"Omega_m0": omega_m0, "h": h_value, "r_d": r_d}
        physics_model, params = joint.physical_model_and_params(PRIMARY_MODEL, values)
        chi2_tied, alpha_tied, _, _ = joint.bao_physical_chi2(physics_model, params, values, bao)
        chi2_free_same_shape, alpha_free_same_shape, _, _ = snbao.bao_chi2(physics_model, params, bao)
        gate_key = (row["rd_prior_mode"], row["prior_table"], row["score_mode"], row["model"])
        gate = gates.get(gate_key, {})

        h_rd_product = h_value * r_d
        rd_needed_same_shape = joint.C_KM_S / (100.0 * h_value * alpha_free_same_shape)
        rd_needed_t7_alpha = joint.C_KM_S / (100.0 * h_value * alpha_t7)
        xi_same_shape = alpha_free_same_shape / alpha_tied
        xi_to_t7_alpha = alpha_t7 / alpha_tied

        rows.append(
            {
                "rd_prior_mode": row["rd_prior_mode"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "model": row["model"],
                "gate": gate.get("gate", ""),
                "Omega_m0": omega_m0,
                "Omega_m0_shift_vs_T7": omega_m0 - float(t7_target["Omega_m0"]),
                "h": h_value,
                "r_d": r_d,
                "h_r_d": h_rd_product,
                "alpha_tied_c_over_100hrd": alpha_tied,
                "alpha_free_same_shape": alpha_free_same_shape,
                "alpha_free_T7_late": alpha_t7,
                "xi_required_same_shape": xi_same_shape,
                "xi_required_to_T7_alpha": xi_to_t7_alpha,
                "alpha_shift_same_shape_percent": 100.0 * (xi_same_shape - 1.0),
                "alpha_shift_to_T7_percent": 100.0 * (xi_to_t7_alpha - 1.0),
                "r_d_needed_same_shape_alpha": rd_needed_same_shape,
                "r_d_needed_T7_alpha": rd_needed_t7_alpha,
                "r_d_shift_same_shape_Mpc": rd_needed_same_shape - r_d,
                "r_d_shift_T7_alpha_Mpc": rd_needed_t7_alpha - r_d,
                "chi2_BAO_tied": chi2_tied,
                "chi2_BAO_free_same_shape": chi2_free_same_shape,
                "chi2_BAO_T7_free": chi2_bao_t7,
                "BAO_penalty_tied_vs_T7": chi2_tied - chi2_bao_t7,
                "BAO_shape_penalty_free_vs_T7": chi2_free_same_shape - chi2_bao_t7,
                "BAO_calibration_penalty_same_shape": chi2_tied - chi2_free_same_shape,
                "late_gate_penalty": gate.get("late_chi2_penalty_vs_T7", ""),
                "CMB_gate_penalty": gate.get("CMB_chi2_penalty_vs_CMB_only", ""),
            }
        )
    return rows


def aggregate_target_rows(rows: list[dict[str, Any]], t7_target: dict[str, Any]) -> list[dict[str, Any]]:
    if not rows:
        return []

    xi_same = np.asarray([float(row["xi_required_same_shape"]) for row in rows], dtype=float)
    xi_t7 = np.asarray([float(row["xi_required_to_T7_alpha"]) for row in rows], dtype=float)
    calibration_penalty = np.asarray([float(row["BAO_calibration_penalty_same_shape"]) for row in rows], dtype=float)
    shape_penalty = np.asarray([float(row["BAO_shape_penalty_free_vs_T7"]) for row in rows], dtype=float)
    omega_shift = np.asarray([float(row["Omega_m0_shift_vs_T7"]) for row in rows], dtype=float)
    failing = [row for row in rows if row["gate"] == "hard_loss_sector_degradation"]

    output = [
        {
            "quantity": "T7_alpha_free",
            "value": float(t7_target["alpha_free"]),
            "units": "dimensionless_BAO_scale",
            "readout": "late-only free-alpha target for the locked branch",
        },
        {
            "quantity": "same_shape_xi_required_mean",
            "value": float(np.mean(xi_same)),
            "units": "dimensionless",
            "readout": "mean alpha multiplier needed to make tied alpha equal each joint-row free-alpha optimum",
        },
        {
            "quantity": "same_shape_xi_required_max_spread",
            "value": float(np.max(xi_same) - np.min(xi_same)),
            "units": "dimensionless",
            "readout": "scatter of a possible common calibration multiplier across four mandatory gates",
        },
        {
            "quantity": "to_T7_alpha_xi_required_mean",
            "value": float(np.mean(xi_t7)),
            "units": "dimensionless",
            "readout": "mean alpha multiplier needed to force the joint rows onto the T7 late-only alpha",
        },
        {
            "quantity": "BAO_calibration_penalty_same_shape_mean",
            "value": float(np.mean(calibration_penalty)),
            "units": "chi2",
            "readout": "BAO cost from tying alpha instead of using the same-shape free alpha",
        },
        {
            "quantity": "BAO_shape_penalty_free_vs_T7_mean",
            "value": float(np.mean(shape_penalty)),
            "units": "chi2",
            "readout": "BAO cost left after alpha is freed at the joint-row Omega_m0",
        },
        {
            "quantity": "Omega_m0_shift_vs_T7_mean",
            "value": float(np.mean(omega_shift)),
            "units": "dimensionless",
            "readout": "mean upward Omega_m0 shift imposed by the joint CMB bridge relative to the late-only T7 branch",
        },
    ]

    for row in failing:
        output.extend(
            [
                {
                    "quantity": "failing_gate_xi_required_same_shape",
                    "value": float(row["xi_required_same_shape"]),
                    "units": "dimensionless",
                    "readout": f"{row['prior_table']} {row['score_mode']} alpha multiplier needed at fixed joint shape",
                },
                {
                    "quantity": "failing_gate_BAO_calibration_penalty_same_shape",
                    "value": float(row["BAO_calibration_penalty_same_shape"]),
                    "units": "chi2",
                    "readout": f"{row['prior_table']} {row['score_mode']} BAO penalty from the tied-alpha condition",
                },
                {
                    "quantity": "failing_gate_BAO_shape_penalty_free_vs_T7",
                    "value": float(row["BAO_shape_penalty_free_vs_T7"]),
                    "units": "chi2",
                    "readout": f"{row['prior_table']} {row['score_mode']} BAO penalty remaining after freeing alpha at the joint shape",
                },
                {
                    "quantity": "failing_gate_Omega_m0_shift_vs_T7",
                    "value": float(row["Omega_m0_shift_vs_T7"]),
                    "units": "dimensionless",
                    "readout": f"{row['prior_table']} {row['score_mode']} upward Omega_m0 shift relative to the T7 late-only branch",
                },
            ]
        )
    return output


def relation_candidate_rows(target_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failing = [row for row in target_rows if row["gate"] == "hard_loss_sector_degradation"]
    failing_row = failing[0] if failing else {}
    xi_same = float(failing_row.get("xi_required_same_shape", math.nan))
    alpha_shift_percent = float(failing_row.get("alpha_shift_same_shape_percent", math.nan))
    calibration_penalty = float(failing_row.get("BAO_calibration_penalty_same_shape", math.nan))
    shape_penalty = float(failing_row.get("BAO_shape_penalty_free_vs_T7", math.nan))
    omega_shift = float(failing_row.get("Omega_m0_shift_vs_T7", math.nan))

    return [
        {
            "candidate": "pure_metric_shared_calibration",
            "relation": "alpha_BAO = c/(100 h r_d)",
            "effect_on_failed_gate": "already tested",
            "derivation_status": "encoded_contract",
            "verdict": "mixed_result_one_mandatory_gate_fails",
            "notes": "This is the no-extra-freedom relation used in checkpoint 119.",
        },
        {
            "candidate": "common_alpha_multiplier",
            "relation": "alpha_BAO = xi_alpha c/(100 h r_d)",
            "effect_on_failed_gate": f"xi_alpha={xi_same:.12g}; alpha shift={alpha_shift_percent:.6g}%; tied-alpha BAO penalty={calibration_penalty:.6g}",
            "derivation_status": "not_derived",
            "verdict": "does_not_repair_primary_failure",
            "notes": "The tied alpha is already essentially the free-alpha optimum at fixed joint shape, so an alpha multiplier is not the missing mechanism.",
        },
        {
            "candidate": "effective_late_sound_horizon",
            "relation": "r_d_eff = c/(100 h alpha_free_same_shape)",
            "effect_on_failed_gate": f"same algebra as xi_alpha; residual free-alpha BAO shape penalty={shape_penalty:.6g}",
            "derivation_status": "not_derived",
            "verdict": "possible_theorem_target_not_current_evidence",
            "notes": "This requires an early/late ruler-map derivation, not a fit label.",
        },
        {
            "candidate": "Omega_m_bridge_or_CMB_map",
            "relation": "CMB-inferred Omega_m0 must map to the late BAO/SN Omega_m0 or modify the BAO shape prediction",
            "effect_on_failed_gate": f"failed gate raises Omega_m0 by {omega_shift:.6g}; alpha-free BAO shape penalty={shape_penalty:.6g}",
            "derivation_status": "not_derived",
            "verdict": "main_theorem_target",
            "notes": "The live problem is the CMB-driven Omega_m0 shift, not the numerical alpha=c/(100hr_d) identity.",
        },
        {
            "candidate": "SN_offset_H0_lock",
            "relation": "SN offset fixed by h and absolute magnitude",
            "effect_on_failed_gate": "does not directly repair BAO residuals in the no-SH0ES branch",
            "derivation_status": "irrelevant_to_primary_failure",
            "verdict": "not_a_repair_for_this_gate",
            "notes": "The live failure is BAO-dominated; SN offset freedom is already profiled and counted.",
        },
        {
            "candidate": "MTS_specific_BAO_deformation",
            "relation": "BAO ruler deformed by memory sector",
            "effect_on_failed_gate": "could repair if it changes alpha or anisotropic BAO predictions",
            "derivation_status": "forbidden_until_early_sector_derivation",
            "verdict": "do_not_use_as_public_claim",
            "notes": "This would be a new physical claim requiring CMB/acoustic and perturbation derivation.",
        },
    ]


def decision_rows(target_rows: list[dict[str, Any]], aggregate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failing = [row for row in target_rows if row["gate"] == "hard_loss_sector_degradation"]
    failing_row = failing[0] if failing else {}
    xi_same = float(failing_row.get("xi_required_same_shape", math.nan))
    calibration_penalty = float(failing_row.get("BAO_calibration_penalty_same_shape", math.nan))
    shape_penalty = float(failing_row.get("BAO_shape_penalty_free_vs_T7", math.nan))
    omega_shift = float(failing_row.get("Omega_m0_shift_vs_T7", math.nan))
    xi_spread_row = next((row for row in aggregate_rows if row["quantity"] == "same_shape_xi_required_max_spread"), None)
    xi_spread = float(xi_spread_row["value"]) if xi_spread_row else math.nan
    shape_verdict = "shape_dominated_not_alpha_tie" if calibration_penalty < 0.01 and shape_penalty > 1.0 else "mixed_shape_and_calibration"

    return [
        {
            "item": "status",
            "verdict": "shared_calibration_relation_target_quantified_not_derived",
            "evidence": "exact alpha/r_d and Omega_m0 deformation computed for each mandatory joint gate",
        },
        {
            "item": "failed_gate_repair_size",
            "verdict": "alpha_repair_size_nearly_zero",
            "evidence": f"failed gate same-shape xi_alpha={xi_same:.12g}; same-shape BAO calibration penalty={calibration_penalty:.6g}",
        },
        {
            "item": "shape_vs_calibration",
            "verdict": shape_verdict,
            "evidence": f"failed gate residual free-alpha shape penalty={shape_penalty:.6g}; tied-alpha penalty={calibration_penalty:.6g}; Omega_m0 shift={omega_shift:.6g}",
        },
        {
            "item": "single_relation_coherence",
            "verdict": "numerically_coherent_target" if xi_spread < 0.003 else "branch_dependent_target",
            "evidence": f"xi_alpha spread across four gates={xi_spread:.6g}",
        },
        {
            "item": "promotion_allowed",
            "verdict": "false",
            "evidence": "the relation has been quantified, not derived from a parent action",
        },
        {
            "item": "next_target",
            "verdict": "derive_or_demote",
            "evidence": "derive the early-to-late Omega_m0/CMB map or a BAO-shape modification, otherwise keep the bridge closure-only",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-shared-calibration-relation-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    config, sn, bao = joint.load_primary_data()
    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    t7_target = t7_free_alpha_target(sn, bao)
    target_rows = calibration_target_rows(bao, t7_target)
    aggregate_rows = aggregate_target_rows(target_rows, t7_target)
    candidate_rows = relation_candidate_rows(target_rows)
    decisions = decision_rows(target_rows, aggregate_rows)

    write_csv(
        results_dir / "source_register.csv",
        source_rows,
        ["source", "path", "exists", "issue"],
    )
    write_csv(
        results_dir / "t7_free_alpha_target.csv",
        [t7_target],
        [
            "branch",
            "Omega_m0",
            "DeltaR",
            "B_mem",
            "p",
            "u3",
            "SN_offset",
            "alpha_free",
            "chi2_SN_recomputed",
            "chi2_BAO_recomputed",
            "chi2_late_recomputed",
            "chi2_SN_reported",
            "chi2_BAO_reported",
            "chi2_late_reported",
            "abs_chi2_late_diff",
            "status",
        ],
    )
    write_csv(
        results_dir / "calibration_target_rows.csv",
        target_rows,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "gate",
            "Omega_m0",
            "Omega_m0_shift_vs_T7",
            "h",
            "r_d",
            "h_r_d",
            "alpha_tied_c_over_100hrd",
            "alpha_free_same_shape",
            "alpha_free_T7_late",
            "xi_required_same_shape",
            "xi_required_to_T7_alpha",
            "alpha_shift_same_shape_percent",
            "alpha_shift_to_T7_percent",
            "r_d_needed_same_shape_alpha",
            "r_d_needed_T7_alpha",
            "r_d_shift_same_shape_Mpc",
            "r_d_shift_T7_alpha_Mpc",
            "chi2_BAO_tied",
            "chi2_BAO_free_same_shape",
            "chi2_BAO_T7_free",
            "BAO_penalty_tied_vs_T7",
            "BAO_shape_penalty_free_vs_T7",
            "BAO_calibration_penalty_same_shape",
            "late_gate_penalty",
            "CMB_gate_penalty",
        ],
    )
    write_csv(
        results_dir / "aggregate_targets.csv",
        aggregate_rows,
        ["quantity", "value", "units", "readout"],
    )
    write_csv(
        results_dir / "relation_candidate_audit.csv",
        candidate_rows,
        ["candidate", "relation", "effect_on_failed_gate", "derivation_status", "verdict", "notes"],
    )
    write_csv(
        results_dir / "decision.csv",
        decisions,
        ["item", "verdict", "evidence"],
    )

    hard_failures = sum(1 for row in target_rows if row["gate"] == "hard_loss_sector_degradation")
    status = {
        "status": "shared_calibration_relation_target_quantified_not_derived",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "internal_derivation_audit_not_public_evidence",
        "data_rows": {"SN": len(sn["z"]), "BAO": len(bao["rows"])},
        "config_source": str(config.get("run_dir", joint.T1_RUN)),
        "hard_failure_rows": hard_failures,
        "t7_alpha_free": t7_target["alpha_free"],
        "generated": [
            "source_register.csv",
            "t7_free_alpha_target.csv",
            "calibration_target_rows.csv",
            "aggregate_targets.csv",
            "relation_candidate_audit.csv",
            "decision.csv",
        ],
        "next_target": "121-shared-calibration-relation-derivation-attempt.md",
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
    run_dir = run_audit(args.output_root, args.timestamp)
    print(run_dir)


if __name__ == "__main__":
    main()
