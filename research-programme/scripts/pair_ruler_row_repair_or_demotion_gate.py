#!/usr/bin/env python3
"""Test parent-constrained pair-ruler row-shape repairs before demotion."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import fixed_pair_ruler_branch_smoke as pair_smoke  # noqa: E402


SMOKE_RUN = RUNS_ROOT / "20260531-235959-fixed-pair-ruler-branch-smoke"
SAFETY_RUN = RUNS_ROOT / "20260531-235959-pair-ruler-residual-and-two-point-safety-audit"
NO_CLOCK = pair_smoke.NO_CLOCK_QUARTER

B_MEM = 2.0 / 27.0
U3_QUARTER = 0.25
CLAIM_CEILING = "pair_ruler_row_repair_or_demotion_gate_no_bridge_promotion"
STATUS = "half_kernel_repair_improves_draw_but_no_clock_remains_lead"


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
    if name.startswith("166-") or name.endswith("pair_ruler_row_repair_or_demotion_gate.py"):
        return "current row-repair/demotion gate"
    if name.startswith("165-") or "pair-ruler-residual-and-two-point-safety-audit" in str(path):
        return "row pressure and two-point safety source"
    if name.startswith("164-") or "fixed-pair-ruler-branch-smoke" in str(path):
        return "fixed pair-ruler smoke source"
    if name.startswith("163-"):
        return "effective pair-action owner"
    if name.startswith("161-"):
        return "trace/quadrupole source-law source"
    if name.endswith(".py"):
        return "machine dependency"
    return "supporting source"


def source_register_rows(script_path: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "fixed_pair_ruler_branch_smoke.py",
        SCRIPT_DIR / "pair_ruler_residual_and_two_point_safety_audit.py",
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        WORK_DIR / "163-effective-pair-action-owner-attempt.md",
        WORK_DIR / "164-fixed-pair-ruler-branch-smoke.md",
        WORK_DIR / "165-pair-ruler-residual-and-two-point-safety-audit.md",
        SMOKE_RUN / "status.json",
        SMOKE_RUN / "results" / "sn_bao_fit_summary.csv",
        SMOKE_RUN / "results" / "bao_residuals.csv",
        SAFETY_RUN / "status.json",
        SAFETY_RUN / "results" / "worst_row_pressure.csv",
        SAFETY_RUN / "results" / "two_point_safety_test_matrix.csv",
        Path(config["sn_data"]),
        Path(config["sn_cov"]),
        Path(config["bao_data"]),
        Path(config["bao_cov"]),
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


def activation(load_n: np.ndarray) -> np.ndarray:
    return 1.0 - np.exp(-((load_n / U3_QUARTER) ** 3))


def projection_factors(z_values: np.ndarray, variant: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    z_arr = np.asarray(z_values, dtype=float)
    load_n = np.log1p(z_arr)
    endpoint_balance = 1.0 - 2.0 * np.exp(-load_n)
    one_endpoint = 1.0 - np.exp(-load_n)
    two_endpoint = 1.0 - np.exp(-2.0 * load_n)
    three_endpoint = 1.0 - np.exp(-3.0 * load_n)
    f_value = activation(load_n)

    if variant == "base_161_fixed":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 6.0) * two_endpoint
    elif variant == "pair_action_half_kernel":
        trace = (B_MEM / 8.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 12.0) * two_endpoint
    elif variant == "half_quadrupole_only":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 12.0) * two_endpoint
    elif variant == "one_endpoint_quadrupole":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 6.0) * one_endpoint
    elif variant == "F_gated_quadrupole":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 6.0) * f_value * two_endpoint
    elif variant == "trace_pair_envelope":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance * two_endpoint
        quadrupole = (B_MEM / 6.0) * two_endpoint
    elif variant == "trace_pair_envelope_half_quad":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance * two_endpoint
        quadrupole = (B_MEM / 12.0) * two_endpoint
    elif variant == "three_endpoint_quadrupole":
        trace = (B_MEM / 4.0) * f_value * endpoint_balance
        quadrupole = (B_MEM / 6.0) * three_endpoint
    elif variant == "projection_off_control":
        trace = np.zeros_like(z_arr)
        quadrupole = np.zeros_like(z_arr)
    else:
        raise ValueError(f"unknown repair variant {variant}")
    pi_perp = trace - quadrupole / 3.0
    pi_parallel = trace + 2.0 * quadrupole / 3.0
    return trace, quadrupole, pi_perp, pi_parallel


def variant_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "variant": "projection_off_control",
            "formula": "T=0; S=0",
            "parent_motivation": "no-clock MTS control",
            "status": "control",
            "repair_allowed": "yes_control",
        },
        {
            "variant": "base_161_fixed",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-2N)",
            "parent_motivation": "checkpoint 161 fixed source law",
            "status": "current_branch",
            "repair_allowed": "yes",
        },
        {
            "variant": "pair_action_half_kernel",
            "formula": "T=(B/8)F(1-2e^-N); S=(B/12)(1-e^-2N)",
            "parent_motivation": "normal-ordered symmetric pair action carries a 1/2 kernel weight",
            "status": "best_structural_repair_candidate",
            "repair_allowed": "yes_if_parent_action_owns_half_factor",
        },
        {
            "variant": "half_quadrupole_only",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/12)(1-e^-2N)",
            "parent_motivation": "unordered-pair quadrupole symmetrization only",
            "status": "diagnostic_structural_variant",
            "repair_allowed": "weak",
        },
        {
            "variant": "one_endpoint_quadrupole",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-N)",
            "parent_motivation": "single-endpoint screen average instead of two-endpoint pair saturation",
            "status": "weak_structural_variant",
            "repair_allowed": "weak",
        },
        {
            "variant": "F_gated_quadrupole",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/6)F(1-e^-2N)",
            "parent_motivation": "determinant gate applied to trace and quadrupole",
            "status": "structural_variant",
            "repair_allowed": "yes",
        },
        {
            "variant": "trace_pair_envelope",
            "formula": "T=(B/4)F(1-2e^-N)(1-e^-2N); S=(B/6)(1-e^-2N)",
            "parent_motivation": "connected-pair envelope applied to trace source",
            "status": "structural_variant",
            "repair_allowed": "yes",
        },
        {
            "variant": "trace_pair_envelope_half_quad",
            "formula": "T=(B/4)F(1-2e^-N)(1-e^-2N); S=(B/12)(1-e^-2N)",
            "parent_motivation": "connected trace envelope plus half quadrupole symmetrization",
            "status": "hybrid_structural_variant",
            "repair_allowed": "weak",
        },
        {
            "variant": "three_endpoint_quadrupole",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-3N)",
            "parent_motivation": "three-spatial-endpoint saturation check",
            "status": "diagnostic_variant",
            "repair_allowed": "weak",
        },
    ]


def read_data() -> tuple[dict[str, Any], dict[str, Any]]:
    config = pair_smoke.load_reference_config()
    sn = snbao.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config.get("sn_max_rows"),
        covariance_path=Path(config["sn_cov"]),
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = snbao.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    return sn, bao


def bao_prediction(values: dict[str, float], bao: dict[str, Any], variant: str, alpha: float) -> np.ndarray:
    z_values = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    dm_values = pair_smoke.comoving_integral_branch(NO_CLOCK, z_values, values)
    ez_values = pair_smoke.e_z_branch(NO_CLOCK, z_values, values)
    _, _, pi_perp, pi_parallel = projection_factors(z_values, variant)
    predictions: list[float] = []
    for row, z_value, dm_value, ez_value, perp, parallel in zip(
        bao["rows"], z_values, dm_values, ez_values, pi_perp, pi_parallel, strict=True
    ):
        dm_projected = (1.0 + perp) * dm_value
        dh_projected = (1.0 + parallel) / ez_value
        quantity = row["quantity"]
        if quantity == "DM_over_rs":
            predictions.append(alpha * float(dm_projected))
        elif quantity == "DH_over_rs":
            predictions.append(alpha * float(dh_projected))
        elif quantity == "DV_over_rs":
            predictions.append(alpha * float((z_value * dm_projected * dm_projected * dh_projected) ** (1.0 / 3.0)))
        else:
            raise ValueError(f"unsupported BAO quantity {quantity}")
    return np.asarray(predictions, dtype=float)


def bao_chi2(values: dict[str, float], bao: dict[str, Any], variant: str) -> tuple[float, float, np.ndarray, np.ndarray]:
    observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
    covariance = np.asarray(bao["covariance"], dtype=float)
    inv_cov = linalg.inv(covariance)
    unit_pred = bao_prediction(values, bao, variant, alpha=1.0)
    alpha = float((unit_pred @ inv_cov @ observed) / (unit_pred @ inv_cov @ unit_pred))
    predicted = alpha * unit_pred
    residual = observed - predicted
    chi2 = float(residual @ inv_cov @ residual)
    return chi2, alpha, residual, predicted


def sn_chi2(values: dict[str, float], sn: dict[str, Any]) -> tuple[float, float, np.ndarray]:
    chi2, offset, residual, _ = pair_smoke.sn_chi2_branch(NO_CLOCK, values, sn)
    return chi2, offset, residual


def score_variant(variant: str, sn: dict[str, Any], bao: dict[str, Any], max_iter: int) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    bounds = [(0.05, 0.60)]

    def objective(vector: np.ndarray) -> float:
        values = {"Omega_m": float(vector[0])}
        try:
            chi2_sn, _, _ = sn_chi2(values, sn)
            chi2_bao, _, _, _ = bao_chi2(values, bao, variant)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([value], dtype=float) for value in [0.20, 0.30, 0.40, 0.50]]
    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-9},
        )
        for start in starts
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = {"Omega_m": float(result.x[0])}
    chi2_sn, sn_offset, _ = sn_chi2(values, sn)
    chi2_bao, alpha, bao_residual, bao_predicted = bao_chi2(values, bao, variant)
    chi2_total = chi2_sn + chi2_bao
    n_data = len(sn["z"]) + len(bao["rows"])
    dynamic_k = 3
    row = {
        "variant": variant,
        "success": bool(result.success),
        "Omega_m": values["Omega_m"],
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "AIC": chi2_total + 2.0 * dynamic_k,
        "BIC": chi2_total + dynamic_k * math.log(n_data),
        "bao_alpha": alpha,
        "sn_offset": sn_offset,
        "optimizer_message": str(result.message),
    }
    return row, bao_residual, bao_predicted


def scorecard_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_variant = {row["variant"]: row for row in scores}
    no_clock = by_variant["projection_off_control"]
    base = by_variant["base_161_fixed"]
    lcdm = next(row for row in read_csv_rows(SMOKE_RUN / "results" / "sn_bao_fit_summary.csv") if row["branch"] == "LCDM")
    rows: list[dict[str, Any]] = []
    contracts = {row["variant"]: row for row in variant_contract_rows()}
    for score in scores:
        delta_bic_no = float(score["BIC"]) - float(no_clock["BIC"])
        delta_bic_base = float(score["BIC"]) - float(base["BIC"])
        delta_bic_lcdm = float(score["BIC"]) - float(lcdm["BIC"])
        rows.append(
            {
                **score,
                "formula": contracts[score["variant"]]["formula"],
                "repair_allowed": contracts[score["variant"]]["repair_allowed"],
                "delta_chi2_vs_no_clock": float(score["chi2_total"]) - float(no_clock["chi2_total"]),
                "delta_BIC_vs_no_clock": delta_bic_no,
                "delta_chi2_BAO_vs_no_clock": float(score["chi2_BAO"]) - float(no_clock["chi2_BAO"]),
                "delta_chi2_SN_vs_no_clock": float(score["chi2_SN"]) - float(no_clock["chi2_SN"]),
                "delta_BIC_vs_base_161": delta_bic_base,
                "delta_BIC_vs_LCDM": delta_bic_lcdm,
                "readout_vs_no_clock": "beats_no_clock" if delta_bic_no <= -2.0 else "draw_vs_no_clock" if delta_bic_no < 2.0 else "worse_than_no_clock",
                "readout_vs_base": "improves_base" if delta_bic_base < -0.25 else "roughly_base" if delta_bic_base < 0.25 else "worse_than_base",
                "readout_vs_LCDM": "beats_LCDM" if delta_bic_lcdm <= -2.0 else "draw_vs_LCDM" if delta_bic_lcdm < 2.0 else "worse_than_LCDM",
            }
        )
    return rows


def row_delta_rows(bao: dict[str, Any], scores: list[dict[str, Any]], residuals: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    covariance = np.asarray(bao["covariance"], dtype=float)
    inv_cov = linalg.inv(covariance)
    no_clock_residual = residuals["projection_off_control"]
    rows: list[dict[str, Any]] = []
    for score in scores:
        variant = score["variant"]
        residual = residuals[variant]
        signed = residual * (inv_cov @ residual)
        no_signed = no_clock_residual * (inv_cov @ no_clock_residual)
        _, _, pi_perp, pi_parallel = projection_factors(np.asarray([row["z"] for row in bao["rows"]], dtype=float), variant)
        for index, (bao_row, res, contrib, no_contrib, perp, parallel) in enumerate(
            zip(bao["rows"], residual, signed, no_signed, pi_perp, pi_parallel, strict=True)
        ):
            rows.append(
                {
                    "variant": variant,
                    "row_index": index,
                    "z": bao_row["z"],
                    "observable": bao_row["quantity"],
                    "Pi_perp": perp,
                    "Pi_parallel": parallel,
                    "residual": res,
                    "cov_signed_chi2_contribution": contrib,
                    "delta_cov_signed_chi2_vs_no_clock": contrib - no_contrib,
                    "readout": "row_better" if contrib - no_contrib < 0.0 else "row_worse",
                }
            )
    return rows


def best_variant(rows: list[dict[str, Any]]) -> dict[str, Any]:
    allowed = [row for row in rows if row["repair_allowed"] in {"yes", "yes_if_parent_action_owns_half_factor"} and row["variant"] != "projection_off_control"]
    return min(allowed, key=lambda row: float(row["delta_BIC_vs_no_clock"]))


def gate_rows(score_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best = best_variant(score_rows)
    base = next(row for row in score_rows if row["variant"] == "base_161_fixed")
    beats_no_clock = float(best["delta_BIC_vs_no_clock"]) <= -2.0
    improves_base = float(best["delta_BIC_vs_base_161"]) < -0.25
    return [
        {
            "gate": "candidate_repairs_predeclared_structural",
            "status": "pass_limited",
            "evidence": "tested discrete endpoint/envelope/symmetry variants only; no continuous fitted projection amplitude",
        },
        {
            "gate": "base_161_status",
            "status": "live_but_not_lead",
            "evidence": f"base delta_BIC_vs_no_clock={base['delta_BIC_vs_no_clock']}; delta_BIC_vs_LCDM={base['delta_BIC_vs_LCDM']}",
        },
        {
            "gate": "best_repair_variant",
            "status": "pass_improves_base" if improves_base else "fail_no_improvement",
            "evidence": f"{best['variant']} delta_BIC_vs_no_clock={best['delta_BIC_vs_no_clock']}; delta_BIC_vs_base={best['delta_BIC_vs_base_161']}",
        },
        {
            "gate": "beats_no_clock_control",
            "status": "pass" if beats_no_clock else "fail_draw_only",
            "evidence": f"best allowed repair still delta_BIC_vs_no_clock={best['delta_BIC_vs_no_clock']}",
        },
        {
            "gate": "parent_derivation_required",
            "status": "fail_open",
            "evidence": "half-kernel repair is only allowed if the effective pair action owns the 1/2 factor before data scoring",
        },
        {
            "gate": "demotion_decision",
            "status": "freeze_as_nonleading_side_branch",
            "evidence": "no tested structural repair beats no-clock; no-clock remains lead empirical branch",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(score_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best = best_variant(score_rows)
    base = next(row for row in score_rows if row["variant"] == "base_161_fixed")
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": f"best repair {best['variant']} improves base by {best['delta_BIC_vs_base_161']} but remains {best['delta_BIC_vs_no_clock']} vs no-clock",
        },
        {
            "item": "best_repair_candidate",
            "verdict": best["variant"],
            "evidence": f"formula={best['formula']}; delta_BIC_vs_LCDM={best['delta_BIC_vs_LCDM']}",
        },
        {
            "item": "base_161_result",
            "verdict": "survives_but_not_lead",
            "evidence": f"base delta_BIC_vs_no_clock={base['delta_BIC_vs_no_clock']}; delta_BIC_vs_LCDM={base['delta_BIC_vs_LCDM']}",
        },
        {
            "item": "lead_branch",
            "verdict": "no_clock_MTS_remains_empirical_lead",
            "evidence": "no discrete parent-constrained pair-ruler variant beats the no-clock control",
        },
        {
            "item": "pair_ruler_status",
            "verdict": "freeze_as_nonleading_side_branch_pending_parent_and_two_point_tests",
            "evidence": "pair-ruler remains useful as a theorem target and two-point test branch, not as lead cosmology",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "repair/demotion gate only; no bridge/CMB/local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "167-no-clock-lead-and-pair-sidecar-test-plan.md",
            "evidence": "prioritize no-clock empirical robustness while keeping half-kernel pair branch as sidecar for growth/lensing/CMB safety",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None, max_iter: int) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-pair-ruler-row-repair-or-demotion-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    config = pair_smoke.load_reference_config()
    sources = source_register_rows(Path(__file__).resolve(), config)
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    sn, bao = read_data()
    scores: list[dict[str, Any]] = []
    residuals: dict[str, np.ndarray] = {}
    predictions: dict[str, np.ndarray] = {}
    for variant in [row["variant"] for row in variant_contract_rows()]:
        score, residual, predicted = score_variant(variant, sn, bao, max_iter)
        scores.append(score)
        residuals[variant] = residual
        predictions[variant] = predicted

    scored = scorecard_rows(scores)
    row_deltas = row_delta_rows(bao, scores, residuals)
    gates = gate_rows(scored)
    decisions = decision_rows(scored)
    best = best_variant(scored)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "max_iter": max_iter,
            "variants": variant_contract_rows(),
            "best_variant": best["variant"],
            "sn_rows": len(sn["z"]),
            "bao_rows": len(bao["rows"]),
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "repair_variant_contract.csv",
        variant_contract_rows(),
        ["variant", "formula", "parent_motivation", "status", "repair_allowed"],
    )
    write_csv(
        results_dir / "repair_variant_scorecard.csv",
        scored,
        [
            "variant",
            "success",
            "Omega_m",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "bao_alpha",
            "sn_offset",
            "formula",
            "repair_allowed",
            "delta_chi2_vs_no_clock",
            "delta_BIC_vs_no_clock",
            "delta_chi2_BAO_vs_no_clock",
            "delta_chi2_SN_vs_no_clock",
            "delta_BIC_vs_base_161",
            "delta_BIC_vs_LCDM",
            "readout_vs_no_clock",
            "readout_vs_base",
            "readout_vs_LCDM",
        ],
    )
    write_csv(
        results_dir / "repair_row_delta_vs_no_clock.csv",
        row_deltas,
        [
            "variant",
            "row_index",
            "z",
            "observable",
            "Pi_perp",
            "Pi_parallel",
            "residual",
            "cov_signed_chi2_contribution",
            "delta_cov_signed_chi2_vs_no_clock",
            "readout",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "best_repair_variant": best["variant"],
        "best_delta_BIC_vs_no_clock": float(best["delta_BIC_vs_no_clock"]),
        "best_delta_BIC_vs_base_161": float(best["delta_BIC_vs_base_161"]),
        "generated": [
            "source_register.csv",
            "repair_variant_contract.csv",
            "repair_variant_scorecard.csv",
            "repair_row_delta_vs_no_clock.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "167-no-clock-lead-and-pair-sidecar-test-plan.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
