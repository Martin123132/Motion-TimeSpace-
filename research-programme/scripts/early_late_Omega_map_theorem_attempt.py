"""Audit candidate early-to-late Omega_m0 maps for the locked 2/27 branch.

This script quantifies whether the CMB-to-late Omega_m0 gap can be explained by
an algebraic memory-sector map, or whether the map remains an empirical closure.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

WORK_DIR = Path(__file__).resolve().parent.parent
RUNS_ROOT = WORK_DIR / "runs"

CMB_RUN = RUNS_ROOT / "20260531-161215-locked-2over27-CMB-distance-score"
JOINT_RUN = RUNS_ROOT / "20260531-164201-locked-2over27-joint-late-CMB-score"
CALIBRATION_RUN = RUNS_ROOT / "20260531-171500-shared-calibration-relation-attempt"

LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_B_DELTA_R = LOCKED_B_MEM * LOCKED_DELTA_R
PRIMARY_MODEL = "MTS_locked_2over27"
ZERO_MODEL = "MTS_Bmem_zero"


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
        CMB_RUN / "results" / "fit_summary.csv",
        JOINT_RUN / "results" / "fit_summary.csv",
        JOINT_RUN / "results" / "joint_gates.csv",
        CALIBRATION_RUN / "results" / "t7_free_alpha_target.csv",
        CALIBRATION_RUN / "results" / "calibration_target_rows.csv",
        WORK_DIR / "121-shared-calibration-relation-derivation-attempt.md",
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


def t7_omega_late() -> float:
    rows = read_csv_rows(CALIBRATION_RUN / "results" / "t7_free_alpha_target.csv")
    if len(rows) != 1:
        raise RuntimeError(f"expected one T7 target row, found {len(rows)}")
    return float(rows[0]["Omega_m0"])


def cmb_fit_lookup() -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["prior_table"], row["score_mode"], row["model"]): row
        for row in read_csv_rows(CMB_RUN / "results" / "fit_summary.csv")
    }


def candidate_value_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "DeltaR",
            "value": LOCKED_DELTA_R,
            "readout": "locked boundary fraction",
        },
        {
            "quantity": "B_mem",
            "value": LOCKED_B_MEM,
            "readout": "locked memory amplitude",
        },
        {
            "quantity": "B_mem_times_DeltaR",
            "value": LOCKED_B_DELTA_R,
            "readout": "tempting common Omega_m0 shift candidate",
        },
        {
            "quantity": "DeltaR_squared_over_3",
            "value": LOCKED_DELTA_R * LOCKED_DELTA_R / 3.0,
            "readout": "same number because B_mem = DeltaR/3",
        },
    ]


def joint_map_rows(omega_late: float) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(CALIBRATION_RUN / "results" / "calibration_target_rows.csv"):
        omega_joint = float(row["Omega_m0"])
        shift_needed = omega_joint - omega_late
        beta_needed = shift_needed / LOCKED_B_MEM
        omega_after_bdr = omega_joint - LOCKED_B_DELTA_R
        residual_after_bdr = omega_after_bdr - omega_late
        rows.append(
            {
                "arena": "joint_late_CMB",
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "model": PRIMARY_MODEL,
                "gate": row["gate"],
                "Omega_source": omega_joint,
                "Omega_late_target": omega_late,
                "shift_needed": shift_needed,
                "beta_needed_shift_over_Bmem": beta_needed,
                "Bmem_DeltaR_shift": LOCKED_B_DELTA_R,
                "Omega_after_Bmem_DeltaR_map": omega_after_bdr,
                "residual_after_Bmem_DeltaR_map": residual_after_bdr,
                "abs_residual_after_Bmem_DeltaR_map": abs(residual_after_bdr),
                "readout": "post-fit joint compromise compared with late-only T7",
            }
        )
    return rows


def cmb_map_rows(omega_late: float) -> list[dict[str, Any]]:
    lookup = cmb_fit_lookup()
    rows = []
    prior_modes = sorted({key[0:2] for key in lookup})
    for prior_table, score_mode in prior_modes:
        locked = lookup[(prior_table, score_mode, PRIMARY_MODEL)]
        zero = lookup[(prior_table, score_mode, ZERO_MODEL)]
        lcdm = lookup[(prior_table, score_mode, "LCDM")]
        omega_locked = float(locked["Omega_m0"])
        omega_zero = float(zero["Omega_m0"])
        omega_lcdm = float(lcdm["Omega_m0"])
        source_rows = [
            (
                PRIMARY_MODEL,
                omega_locked,
                omega_locked - omega_late,
                (omega_locked - omega_late) / LOCKED_B_MEM,
                omega_locked - LOCKED_B_DELTA_R - omega_late,
                "CMB-only locked branch to late-only T7",
            ),
            (
                ZERO_MODEL,
                omega_zero,
                omega_zero - omega_late,
                "",
                omega_zero - omega_late,
                "CMB-only Bmem-zero control to late-only T7",
            ),
            (
                "LCDM",
                omega_lcdm,
                omega_lcdm - omega_late,
                "",
                omega_lcdm - omega_late,
                "CMB-only LCDM baseline to late-only T7",
            ),
        ]
        for model, omega_source, shift_needed, beta_needed, residual_bdr, readout in source_rows:
            rows.append(
                {
                    "arena": "CMB_only",
                    "prior_table": prior_table,
                    "score_mode": score_mode,
                    "model": model,
                    "gate": "CMB_distance_draw",
                    "Omega_source": omega_source,
                    "Omega_late_target": omega_late,
                    "shift_needed": shift_needed,
                    "beta_needed_shift_over_Bmem": beta_needed,
                    "Bmem_DeltaR_shift": LOCKED_B_DELTA_R if model == PRIMARY_MODEL else "",
                    "Omega_after_Bmem_DeltaR_map": omega_source - LOCKED_B_DELTA_R if model == PRIMARY_MODEL else "",
                    "residual_after_Bmem_DeltaR_map": residual_bdr,
                    "abs_residual_after_Bmem_DeltaR_map": abs(residual_bdr),
                    "readout": readout,
                }
            )

        rows.append(
            {
                "arena": "CMB_only_memory_response",
                "prior_table": prior_table,
                "score_mode": score_mode,
                "model": PRIMARY_MODEL,
                "gate": "finite_response",
                "Omega_source": omega_locked,
                "Omega_late_target": omega_zero,
                "shift_needed": omega_locked - omega_zero,
                "beta_needed_shift_over_Bmem": (omega_locked - omega_zero) / LOCKED_B_MEM,
                "Bmem_DeltaR_shift": LOCKED_B_DELTA_R,
                "Omega_after_Bmem_DeltaR_map": omega_locked - LOCKED_B_DELTA_R,
                "residual_after_Bmem_DeltaR_map": omega_locked - LOCKED_B_DELTA_R - omega_zero,
                "abs_residual_after_Bmem_DeltaR_map": abs(omega_locked - LOCKED_B_DELTA_R - omega_zero),
                "readout": "CMB-only locked-vs-zero isolates compressed-prior response to B_mem",
            }
        )
    return rows


def aggregate_map_rows(map_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    joint_rows = [row for row in map_rows if row["arena"] == "joint_late_CMB"]
    cmb_locked_rows = [
        row for row in map_rows if row["arena"] == "CMB_only" and row["model"] == PRIMARY_MODEL
    ]
    response_rows = [row for row in map_rows if row["arena"] == "CMB_only_memory_response"]

    def mean(values: list[float]) -> float:
        return sum(values) / len(values)

    def spread(values: list[float]) -> float:
        return max(values) - min(values)

    return [
        {
            "quantity": "joint_shift_needed_mean",
            "value": mean([float(row["shift_needed"]) for row in joint_rows]),
            "readout": "mean joint compromise shift relative to late-only T7",
        },
        {
            "quantity": "joint_beta_needed_mean",
            "value": mean([float(row["beta_needed_shift_over_Bmem"]) for row in joint_rows]),
            "readout": "mean beta in shift = beta B_mem for joint rows",
        },
        {
            "quantity": "joint_beta_needed_spread",
            "value": spread([float(row["beta_needed_shift_over_Bmem"]) for row in joint_rows]),
            "readout": "branch dependence of beta across joint gates",
        },
        {
            "quantity": "joint_Bmem_DeltaR_residual_mean",
            "value": mean([float(row["residual_after_Bmem_DeltaR_map"]) for row in joint_rows]),
            "readout": "mean residual after subtracting B_mem DeltaR from joint Omega_m0",
        },
        {
            "quantity": "joint_Bmem_DeltaR_abs_residual_max",
            "value": max(float(row["abs_residual_after_Bmem_DeltaR_map"]) for row in joint_rows),
            "readout": "worst joint residual after the B_mem DeltaR map",
        },
        {
            "quantity": "CMB_locked_to_T7_beta_mean",
            "value": mean([float(row["beta_needed_shift_over_Bmem"]) for row in cmb_locked_rows]),
            "readout": "mean beta needed to map CMB-only locked Omega_m0 to late-only T7",
        },
        {
            "quantity": "CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min",
            "value": min(float(row["abs_residual_after_Bmem_DeltaR_map"]) for row in cmb_locked_rows),
            "readout": "best CMB-only residual after the B_mem DeltaR map",
        },
        {
            "quantity": "CMB_locked_vs_zero_response_beta_mean",
            "value": mean([float(row["beta_needed_shift_over_Bmem"]) for row in response_rows]),
            "readout": "compressed-prior response coefficient of Omega_m0 to B_mem",
        },
        {
            "quantity": "Bmem_DeltaR",
            "value": LOCKED_B_DELTA_R,
            "readout": "candidate theorem shift",
        },
    ]


def candidate_audit_rows(aggregate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    agg = {row["quantity"]: float(row["value"]) for row in aggregate_rows}
    return [
        {
            "candidate": "identity_map",
            "relation": "Omega_m0_late = Omega_m0_CMB",
            "support": "required by separately conserved dust in a single-metric background",
            "failure": f"joint mean shift={agg['joint_shift_needed_mean']:.12g}; CMB-only beta to T7={agg['CMB_locked_to_T7_beta_mean']:.12g}",
            "verdict": "fails_empirical_target_but_is_the_conservative_theory_default",
        },
        {
            "candidate": "Bmem_DeltaR_map",
            "relation": "Omega_m0_late = Omega_m0_source - B_mem DeltaR",
            "support": "numerically centers the four joint rows; B_mem DeltaR = DeltaR^2/3",
            "failure": f"joint beta spread={agg['joint_beta_needed_spread']:.12g}; worst joint residual={agg['joint_Bmem_DeltaR_abs_residual_max']:.12g}; CMB-only residual remains >= {agg['CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min']:.12g}",
            "verdict": "interesting_closure_coincidence_not_a_theorem",
        },
        {
            "candidate": "compressed_prior_response_map",
            "relation": "Omega_m0_CMB,locked - Omega_m0_CMB,B0 = beta_CMB B_mem",
            "support": f"mean beta_CMB={agg['CMB_locked_vs_zero_response_beta_mean']:.12g}",
            "failure": "beta is a likelihood-response coefficient, not a covariant field equation",
            "verdict": "diagnostic_only_requires_official_CMB_likelihood",
        },
        {
            "candidate": "interacting_memory_matter_map",
            "relation": "nabla_mu T_m^{mu nu} = Q^nu, nabla_mu T_mem^{mu nu} = -Q^nu",
            "support": "would allow real early-late matter-normalization drift",
            "failure": "Q^nu is not derived and would endanger Bianchi/local-GR/PPN constraints",
            "verdict": "not_allowed_until_parent_action_supplies_Qnu",
        },
        {
            "candidate": "BAO_shape_correction",
            "relation": "F_BAO -> F_BAO + delta F_memory",
            "support": "targets the actual residual identified in checkpoint 121",
            "failure": "requires acoustic/perturbation derivation before scoring",
            "verdict": "possible_future_route_not_current_evidence",
        },
    ]


def theorem_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "conserved_single_metric_dust",
            "condition": "matter stress is separately conserved and all sectors use one FLRW metric",
            "deduction": "Omega_m0 is one physical normalization across early and late epochs",
            "status": "no_go_for_nontrivial_map",
        },
        {
            "route": "inference_map_from_compressed_priors",
            "condition": "Omega_m0_CMB is treated as a compressed-prior inferred parameter, not the physical dust normalization",
            "deduction": "a map may exist, but it is likelihood/model dependent and cannot be proven by background algebra alone",
            "status": "requires_official_CMB_likelihood_or_perturbation_model",
        },
        {
            "route": "memory_matter_exchange",
            "condition": "parent action produces a conserved total stress with nonzero exchange current Q^nu",
            "deduction": "early and late matter normalizations can differ only if Q^nu is derived and locally screened",
            "status": "open_but_high_risk_not_available_now",
        },
        {
            "route": "memory_BAO_shape",
            "condition": "memory field changes the acoustic ruler or late BAO projection shape",
            "deduction": "can target the residual, but demands a perturbation/acoustic calculation",
            "status": "open_future_theorem_target",
        },
    ]


def decision_rows(aggregate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    agg = {row["quantity"]: float(row["value"]) for row in aggregate_rows}
    theorem_like_joint = (
        abs(agg["joint_Bmem_DeltaR_residual_mean"]) < 1.0e-4
        and agg["joint_Bmem_DeltaR_abs_residual_max"] < 0.005
    )
    cmb_unrepaired = agg["CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min"] > 0.005
    return [
        {
            "item": "status",
            "verdict": "Omega_map_theorem_rejected_under_current_assumptions",
            "evidence": "single-metric conserved dust gives identity; nontrivial maps need new Q^nu or CMB inference model",
        },
        {
            "item": "Bmem_DeltaR",
            "verdict": "useful_closure_coincidence" if theorem_like_joint else "weak_closure_candidate",
            "evidence": f"shift={LOCKED_B_DELTA_R:.12g}; joint mean residual={agg['joint_Bmem_DeltaR_residual_mean']:.12g}; worst residual={agg['joint_Bmem_DeltaR_abs_residual_max']:.12g}",
        },
        {
            "item": "CMB_only_transfer",
            "verdict": "not_repaired_by_Bmem_DeltaR" if cmb_unrepaired else "partially_repaired",
            "evidence": f"best CMB-only residual after Bmem DeltaR={agg['CMB_locked_to_T7_Bmem_DeltaR_abs_residual_min']:.12g}",
        },
        {
            "item": "promotion_allowed",
            "verdict": "false",
            "evidence": "the map is not derived and remains model/likelihood dependent",
        },
        {
            "item": "next_target",
            "verdict": "demote_compressed_CMB_bridge_or_build_full_CMB_perturbation_route",
            "evidence": "a background-only Omega map is not enough to promote the joint CMB gate",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-early-late-Omega-map-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    omega_late = t7_omega_late()
    map_rows = joint_map_rows(omega_late) + cmb_map_rows(omega_late)
    aggregate_rows = aggregate_map_rows(map_rows)
    candidates = candidate_audit_rows(aggregate_rows)
    theorem_routes = theorem_route_rows()
    decisions = decision_rows(aggregate_rows)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "candidate_values.csv", candidate_value_rows(), ["quantity", "value", "readout"])
    write_csv(
        results_dir / "map_target_rows.csv",
        map_rows,
        [
            "arena",
            "prior_table",
            "score_mode",
            "model",
            "gate",
            "Omega_source",
            "Omega_late_target",
            "shift_needed",
            "beta_needed_shift_over_Bmem",
            "Bmem_DeltaR_shift",
            "Omega_after_Bmem_DeltaR_map",
            "residual_after_Bmem_DeltaR_map",
            "abs_residual_after_Bmem_DeltaR_map",
            "readout",
        ],
    )
    write_csv(results_dir / "aggregate_map_diagnostics.csv", aggregate_rows, ["quantity", "value", "readout"])
    write_csv(results_dir / "candidate_map_audit.csv", candidates, ["candidate", "relation", "support", "failure", "verdict"])
    write_csv(results_dir / "theorem_route_audit.csv", theorem_routes, ["route", "condition", "deduction", "status"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": "Omega_map_theorem_rejected_under_current_assumptions",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "internal_theorem_attempt_not_public_evidence",
        "locked_constants": {
            "DeltaR": LOCKED_DELTA_R,
            "B_mem": LOCKED_B_MEM,
            "B_mem_times_DeltaR": LOCKED_B_DELTA_R,
        },
        "generated": [
            "source_register.csv",
            "candidate_values.csv",
            "map_target_rows.csv",
            "aggregate_map_diagnostics.csv",
            "candidate_map_audit.csv",
            "theorem_route_audit.csv",
            "decision.csv",
        ],
        "next_target": "123-CMB-bridge-demotion-and-next-test-route.md",
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
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
