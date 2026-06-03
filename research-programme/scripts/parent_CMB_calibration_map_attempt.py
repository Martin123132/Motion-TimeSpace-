#!/usr/bin/env python3
"""Attempt the parent map for CMB-calibrated H0/Omega_m0/b_mem."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from growth_CMB_first_scoring_run import load_background_params  # noqa: E402


SOURCE_33_RESULTS = Path("runs/20260531-003140-CMB-calibration-freedom-audit/results")
SOURCE_35_STATUS = Path("runs/20260531-004152-early-time-decoupling-or-calibration-derivation/status.json")
LOCKED_BRANCH = "MTS_C0_minimal_smooth_memory"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def c0_calibration_rows() -> list[dict[str, Any]]:
    rows = read_csv(POST_CHECKPOINT / SOURCE_33_RESULTS / "CMB_calibration_freedom_audit.csv")
    out: list[dict[str, Any]] = []
    for row in rows:
        if not row["branch"].startswith("C0"):
            continue
        params = json.loads(row["params_json"])
        out.append(
            {
                "tier": row["tier"],
                "branch": row["branch"],
                "fit_names": row["fit_names"],
                "chi2_CMB": float(row["chi2_CMB"]),
                "delta_aic_vs_best_baseline": float(row["delta_aic_vs_best_baseline"]),
                "edge_flags": row["edge_flags"],
                "h0": float(params["h0"]),
                "omega_m0": float(params["omega_m0"]),
                "b_mem": float(params.get("b_mem", 0.0)),
                "alpha_act": float(params.get("alpha_act", 0.0)),
                "nu_act": float(params.get("nu_act", 0.0)),
            }
        )
    return out


def parameter_shift_rows(locked_params: dict[str, float], calibrated_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in calibrated_rows:
        for parameter in ["h0", "omega_m0", "b_mem", "alpha_act", "nu_act"]:
            locked = float(locked_params.get(parameter, 0.0))
            calibrated = float(row[parameter])
            delta = calibrated - locked
            rows.append(
                {
                    "branch": row["branch"],
                    "tier": row["tier"],
                    "parameter": parameter,
                    "locked_value": locked,
                    "calibrated_value": calibrated,
                    "delta": delta,
                    "fractional_delta": delta / locked if locked != 0.0 else "",
                    "fit_names": row["fit_names"],
                    "edge_flags": row["edge_flags"],
                }
            )
    return rows


def candidate_parent_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "H0",
            "candidate_map": "H0 = c / L_H, or H0^2 = kappa_eff rho_m0 / (3 Omega_m0)",
            "source_status": "algebraic_identity_only",
            "missing_derivation": "parent action does not yet derive L_H, rho_m0, or the normalization selecting the observed present background",
            "promotion_requirement": "derive H0 from a boundary condition or invariant coarse-graining scale, not from a CMB retune",
        },
        {
            "quantity": "Omega_m0",
            "candidate_map": "Omega_m0 = kappa_eff rho_m0 / (3 H0^2)",
            "source_status": "standard_Friedmann_bookkeeping",
            "missing_derivation": "parent theory has not specified whether rho_m0 excludes or absorbs memory-sector energy",
            "promotion_requirement": "derive a single matter-density definition used in SN/BAO/growth/CMB",
        },
        {
            "quantity": "b_mem",
            "candidate_map": "b_mem = a_F DeltaR / [3 (H0 L_cg / c)^2]",
            "source_status": "conditional_parent_route",
            "missing_derivation": "L_cg, a_F, DeltaR, and endpoint ordering remain unpredicted",
            "promotion_requirement": "derive the trace-coupling amplitude and coarse-graining length from the parent invariant bundle",
        },
        {
            "quantity": "alpha_act, nu_act",
            "candidate_map": "u_s = alpha_act ln[(1-Omega_m0)/Omega_m0]/3 and F=1-exp[-(N/u_s)^nu_act]",
            "source_status": "phenomenological_shape_lock",
            "missing_derivation": "transition shape is not generated by a parent memory equation",
            "promotion_requirement": "derive Weibull/survival shape, or predeclare it independently before future data tests",
        },
        {
            "quantity": "shared_parameter_set",
            "candidate_map": "same H0, Omega_m0, b_mem, alpha_act, nu_act must serve SN/BAO, growth, and CMB",
            "source_status": "required_not_satisfied",
            "missing_derivation": "CMB-calibrated rows change parameters relative to locked no-SH0ES background",
            "promotion_requirement": "show one parent map and one parameter row passes background, growth, and CMB gates",
        },
    ]


def amplitude_corridor_rows(locked_params: dict[str, float], calibrated_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eta_values = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    branches = [
        {
            "branch": "locked_no_SH0ES_C0",
            "b_mem": float(locked_params["b_mem"]),
        }
    ]
    for row in calibrated_rows:
        if row["branch"] in {"C0_native_bmem_CMB_calibrated_shape_frozen", "C0_equal_h0_omega_shape_frozen"}:
            branches.append({"branch": row["branch"], "b_mem": float(row["b_mem"])})
    out: list[dict[str, Any]] = []
    for branch in branches:
        for eta in eta_values:
            parent_contrast = 3.0 * float(branch["b_mem"]) * eta * eta
            if parent_contrast < 0.0:
                status = "sign_incompatible_with_positive_trace_route"
            elif parent_contrast <= 1.0:
                status = "inside_order_one_corridor"
            else:
                status = "requires_super_order_one_trace_budget"
            out.append(
                {
                    "branch": branch["branch"],
                    "b_mem": branch["b_mem"],
                    "eta_H0_Lcg_over_c": eta,
                    "required_aF_DeltaR": parent_contrast,
                    "status": status,
                    "identity": "a_F DeltaR = 3 b_mem eta^2",
                }
            )
    return out


def requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "same_parameter_map",
            "must_show": "one parent-derived map fixes H0, Omega_m0, and b_mem across late background, growth, and CMB",
            "current_evidence": "CMB retuning produces different parameter rows",
            "status": "fail",
        },
        {
            "requirement": "no_CMB_only_freedom",
            "must_show": "CMB calibration variables were available by derivation before looking at CMB residuals",
            "current_evidence": "calibration was introduced after fixed CMB-distance tension",
            "status": "fail",
        },
        {
            "requirement": "b_mem_magnitude_prediction",
            "must_show": "parent predicts a_F DeltaR and eta, hence b_mem",
            "current_evidence": "only the corridor identity exists",
            "status": "fail",
        },
        {
            "requirement": "high_z_background_safety",
            "must_show": "direct memory is negligible at recombination",
            "current_evidence": "checkpoint 35 bounded saturated memory fraction at 1.6885841317095195e-10",
            "status": "pass",
        },
        {
            "requirement": "calibrated_branch_edge_safety",
            "must_show": "CMB-calibrated row is not merely an optimizer edge artifact",
            "current_evidence": "checkpoint 33 C0 calibration rows have no edge flags",
            "status": "pass",
        },
    ]


def gate_rows(source_35: dict[str, Any], shifts: list[dict[str, Any]], amplitude_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    native_b_shift = next(
        row for row in shifts
        if row["branch"] == "C0_native_bmem_CMB_calibrated_shape_frozen" and row["parameter"] == "b_mem"
    )
    locked_eta_one = next(
        row for row in amplitude_rows
        if row["branch"] == "locked_no_SH0ES_C0" and float(row["eta_H0_Lcg_over_c"]) == 1.0
    )
    return [
        {
            "gate": "source_35_complete",
            "status": "pass" if source_35.get("readout") == "early_time_memory_bound_passes_CMB_distance_calibration_remains_closure_only" else "fail",
            "detail": str(source_35.get("readout")),
        },
        {
            "gate": "H0_parent_map_derived",
            "status": "fail",
            "detail": "H0 has only algebraic definitions; no parent boundary/scale law selects its value",
        },
        {
            "gate": "Omega_m0_parent_map_derived",
            "status": "fail",
            "detail": "matter definition versus absorbed memory contribution is not fixed by parent theory",
        },
        {
            "gate": "b_mem_parent_magnitude_derived",
            "status": "fail",
            "detail": f"corridor exists, but eta=1 locked branch still requires aF_DeltaR={locked_eta_one['required_aF_DeltaR']}",
        },
        {
            "gate": "native_CMB_retune_small_enough_to_ignore",
            "status": "fail" if abs(float(native_b_shift["fractional_delta"])) > 0.1 else "pass",
            "detail": f"native CMB calibration changes b_mem fractionally by {native_b_shift['fractional_delta']}",
        },
        {
            "gate": "calibrated_CMB_support_claim_allowed",
            "status": "fail",
            "detail": "calibration map is not parent-derived",
        },
        {
            "gate": "next_empirical_stress_allowed",
            "status": "pass",
            "detail": "as a labelled closure-only diagnostic, the CMB-calibrated row can be tested against growth",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "parent_calibration_map_status",
            "status": "not_derived",
            "evidence": "H0/Omega_m0 are bookkeeping identities and b_mem has only a conditional amplitude corridor",
            "next_action": "keep CMB-calibrated branch secondary unless a parent scale/amplitude theorem is supplied",
        },
        {
            "decision": "b_mem_parent_route_status",
            "status": "plausible_corridor_not_prediction",
            "evidence": "b_mem = a_F DeltaR/[3 eta^2] can be natural for eta near unity, but eta/a_F/DeltaR are free",
            "next_action": "derive L_cg/H0 normalization and endpoint trace contrast",
        },
        {
            "decision": "empirical_next_step",
            "status": "run_same_parameter_growth_CMB_stress",
            "evidence": "CMB calibration changes b_mem substantially, so test whether the calibrated row keeps growth near-competitive",
            "next_action": "create 37-CMB-calibrated-joint-growth-stress.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Attempt parent CMB calibration map.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_35 = load_json(POST_CHECKPOINT / SOURCE_35_STATUS)
    background = load_background_params(MAIN_WORKBENCH)
    locked_params = {key: float(value) for key, value in background[LOCKED_BRANCH]["params"].items()}
    calibrated = c0_calibration_rows()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-parent-CMB-calibration-map-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    shifts = parameter_shift_rows(locked_params, calibrated)
    candidate_maps = candidate_parent_map_rows()
    amplitude_corridor = amplitude_corridor_rows(locked_params, calibrated)
    requirements = requirement_rows()
    gates = gate_rows(source_35, shifts, amplitude_corridor)
    decisions = decision_rows()

    write_csv(results_dir / "candidate_parent_map.csv", candidate_maps, list(candidate_maps[0].keys()))
    write_csv(results_dir / "CMB_calibration_parameter_shifts.csv", shifts, list(shifts[0].keys()))
    write_csv(results_dir / "bmem_parent_amplitude_corridor.csv", amplitude_corridor, list(amplitude_corridor[0].keys()))
    write_csv(results_dir / "parent_map_requirements.csv", requirements, list(requirements[0].keys()))
    write_csv(results_dir / "parent_map_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    native_b_shift = next(
        row for row in shifts
        if row["branch"] == "C0_native_bmem_CMB_calibrated_shape_frozen" and row["parameter"] == "b_mem"
    )
    readout = "parent_CMB_calibration_map_not_derived_bmem_corridor_only"
    status = {
        "status": "complete_parent_CMB_calibration_map_attempt",
        "readout": readout,
        "recommendation": "run_CMB_calibrated_same_parameter_growth_stress_next",
        "next_target": "37-CMB-calibrated-joint-growth-stress.md",
        "parent_map_status": "not_derived",
        "bmem_route_status": "conditional_corridor_not_prediction",
        "native_CMB_bmem_fractional_shift": native_b_shift["fractional_delta"],
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "public_claim_allowed": False,
        "closure_diagnostic_allowed": True,
        "outputs": {
            "candidate_parent_map": str(results_dir / "candidate_parent_map.csv"),
            "CMB_calibration_parameter_shifts": str(results_dir / "CMB_calibration_parameter_shifts.csv"),
            "bmem_parent_amplitude_corridor": str(results_dir / "bmem_parent_amplitude_corridor.csv"),
            "parent_map_requirements": str(results_dir / "parent_map_requirements.csv"),
            "parent_map_gate_criteria": str(results_dir / "parent_map_gate_criteria.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
