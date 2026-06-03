#!/usr/bin/env python3
"""Audit the post-checkpoint CMB distance-prior implementation."""

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
from scipy import integrate, linalg


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_likelihood_smoke import C_KM_S, e2_array  # noqa: E402
from growth_CMB_first_scoring_run import (  # noqa: E402
    N_EFF,
    N_S,
    OMEGA_B_H2,
    cmb_data,
    load_background_params,
    z_star,
)


SOURCE_29_STATUS = Path("runs/20260531-001431-growth-CMB-score-readout-and-robustness-gate/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def chi2(residual: np.ndarray, covariance: np.ndarray) -> float:
    cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
    return float(residual @ linalg.cho_solve(cho, residual, check_finite=False))


def cmb_e2_variant(
    physics_model: str,
    z: np.ndarray | float,
    params: dict[str, float],
    include_radiation: bool,
) -> np.ndarray:
    z_arr = np.asarray(z, dtype=float)
    e2 = e2_array(physics_model, z_arr, params)
    if include_radiation:
        h = float(params.get("h0", 70.0)) / 100.0
        omega_gamma = 2.469e-5 / (h * h)
        omega_r = omega_gamma * (1.0 + 0.22710731766 * N_EFF)
        e2 = e2 + omega_r * (1.0 + z_arr) ** 4
    return e2


def cmb_prediction_variant(
    physics_model: str,
    params: dict[str, float],
    sound_method: str,
    sound_z_max: float,
    include_radiation: bool,
    use_quad_dm: bool,
) -> dict[str, float]:
    h0 = float(params.get("h0", 70.0))
    zs = z_star(params, OMEGA_B_H2)
    a_star = 1.0 / (1.0 + zs)

    def inv_e(z: float) -> float:
        return 1.0 / math.sqrt(float(cmb_e2_variant(physics_model, z, params, include_radiation)))

    def inv_a2_e(a: float) -> float:
        z = 1.0 / a - 1.0
        return 1.0 / (a * a * math.sqrt(float(cmb_e2_variant(physics_model, z, params, include_radiation))))

    if sound_method == "scale_factor_quad":
        dm_integral = integrate.quad(inv_a2_e, a_star, 1.0, epsrel=1.0e-8, limit=300)[0]
    elif use_quad_dm:
        dm_integral = integrate.quad(inv_e, 0.0, zs, epsrel=1.0e-8, limit=300)[0]
    else:
        z_low = np.linspace(0.0, zs, 40000)
        dm_integral = float(
            np.trapezoid(1.0 / np.sqrt(cmb_e2_variant(physics_model, z_low, params, include_radiation)), z_low)
        )
    d_m = (C_KM_S / h0) * dm_integral

    def sound_integrand(z: float) -> float:
        r_b = 31500.0 * OMEGA_B_H2 / (1.0 + z)
        c_s = 1.0 / math.sqrt(3.0 * (1.0 + r_b))
        return c_s / math.sqrt(float(cmb_e2_variant(physics_model, z, params, include_radiation)))

    if sound_method == "scale_factor_quad":
        def sound_integrand_a(a: float) -> float:
            r_b = 31500.0 * OMEGA_B_H2 * a
            c_s = 1.0 / math.sqrt(3.0 * (1.0 + r_b))
            return c_s * inv_a2_e(a)

        sound_integral = integrate.quad(sound_integrand_a, 0.0, a_star, epsrel=1.0e-8, limit=300)[0]
    elif sound_method == "quad_to_infinity":
        sound_integral = integrate.quad(sound_integrand, zs, np.inf, epsrel=1.0e-8, limit=300)[0]
    else:
        z_sound = np.geomspace(zs, sound_z_max, 60000)
        sound_integral = float(np.trapezoid([sound_integrand(float(z)) for z in z_sound], z_sound))
    r_s = (C_KM_S / h0) * sound_integral
    shift_r = math.sqrt(float(params["omega_m0"])) * h0 * d_m / C_KM_S
    l_a = math.pi * d_m / r_s
    return {
        "R": shift_r,
        "l_A": l_a,
        "Omega_b_h2": OMEGA_B_H2,
        "n_s": N_S,
        "z_star": zs,
        "r_s_star": r_s,
        "D_M_star": d_m,
    }


def score_prediction(
    prediction: dict[str, float],
    params_order: list[str],
    obs: np.ndarray,
    cov: np.ndarray,
) -> tuple[float, float, float]:
    predicted = np.asarray([prediction[name] for name in params_order], dtype=float)
    residual = obs - predicted
    full = chi2(residual, cov)
    keep_no_l_a = [index for index, name in enumerate(params_order) if name != "l_A"]
    no_l_a = chi2(residual[keep_no_l_a], cov[np.ix_(keep_no_l_a, keep_no_l_a)])
    l_a_index = params_order.index("l_A")
    l_a_sigma = math.sqrt(float(cov[l_a_index, l_a_index]))
    l_a_pull = float(residual[l_a_index] / l_a_sigma)
    return full, no_l_a, l_a_pull


def variant_rows(params_order: list[str], obs: np.ndarray, cov: np.ndarray) -> list[dict[str, Any]]:
    background = load_background_params(MAIN_WORKBENCH)
    variants = [
        {"variant": "legacy_z_trapezoid_zmax_1e5", "sound_method": "finite_grid", "sound_z_max": 1.0e5, "include_radiation": True, "use_quad_dm": False},
        {"variant": "finite_grid_zmax_1e6", "sound_method": "finite_grid", "sound_z_max": 1.0e6, "include_radiation": True, "use_quad_dm": False},
        {"variant": "finite_grid_zmax_1e7", "sound_method": "finite_grid", "sound_z_max": 1.0e7, "include_radiation": True, "use_quad_dm": False},
        {"variant": "quad_sound_to_infinity", "sound_method": "quad_to_infinity", "sound_z_max": np.inf, "include_radiation": True, "use_quad_dm": True},
        {"variant": "scale_factor_quad", "sound_method": "scale_factor_quad", "sound_z_max": np.inf, "include_radiation": True, "use_quad_dm": True},
        {"variant": "no_radiation_control", "sound_method": "finite_grid", "sound_z_max": 1.0e7, "include_radiation": False, "use_quad_dm": False},
    ]
    rows: list[dict[str, Any]] = []
    for model in ["LCDM", "wCDM", "CPL", "MTS_C0_minimal_smooth_memory"]:
        entry = background[model]
        physics_model = entry["physics_model"]
        model_params = {key: float(value) for key, value in entry["params"].items()}
        for variant in variants:
            prediction = cmb_prediction_variant(
                physics_model,
                model_params,
                str(variant["sound_method"]),
                float(variant["sound_z_max"]),
                bool(variant["include_radiation"]),
                bool(variant["use_quad_dm"]),
            )
            full_chi2, no_l_a_chi2, l_a_pull = score_prediction(prediction, params_order, obs, cov)
            rows.append(
                {
                    "model": model,
                    "variant": variant["variant"],
                    "R": prediction["R"],
                    "l_A": prediction["l_A"],
                    "z_star": prediction["z_star"],
                    "r_s_star": prediction["r_s_star"],
                    "D_M_star": prediction["D_M_star"],
                    "chi2_full": full_chi2,
                    "chi2_without_l_A": no_l_a_chi2,
                    "l_A_pull_sigma": l_a_pull,
                }
            )
    return rows


def best_by_variant_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_rows: list[dict[str, Any]] = []
    for variant in sorted({row["variant"] for row in rows}):
        subset = [row for row in rows if row["variant"] == variant]
        best = min(subset, key=lambda row: float(row["chi2_full"]))
        best_rows.append(
            {
                "variant": variant,
                "best_model": best["model"],
                "best_chi2_full": best["chi2_full"],
                "best_chi2_without_l_A": best["chi2_without_l_A"],
                "best_l_A_pull_sigma": best["l_A_pull_sigma"],
                "best_r_s_star": best["r_s_star"],
            }
        )
    return best_rows


def finding_rows(source_29: dict[str, Any], best_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    legacy = next(row for row in best_rows if row["variant"] == "legacy_z_trapezoid_zmax_1e5")
    scale_factor = next(row for row in best_rows if row["variant"] == "scale_factor_quad")
    quad_inf = next(row for row in best_rows if row["variant"] == "quad_sound_to_infinity")
    return [
        {
            "finding": "legacy_sound_horizon_integral",
            "status": "major_implementation_error",
            "detail": f"legacy best chi2={float(legacy['best_chi2_full']):.6f}; scale-factor best chi2={float(scale_factor['best_chi2_full']):.6f}",
            "action": "replace finite z-grid sound-horizon integration with scale-factor or converged-to-infinity integration",
        },
        {
            "finding": "converged_methods_agree",
            "status": "pass" if abs(float(scale_factor["best_chi2_full"]) - float(quad_inf["best_chi2_full"])) < 1.0e-3 else "warn",
            "detail": f"scale-factor={float(scale_factor['best_chi2_full']):.9f}; quad-inf={float(quad_inf['best_chi2_full']):.9f}",
            "action": "use scale_factor_quad in the repaired post-checkpoint score",
        },
        {
            "finding": "source_29_status",
            "status": "demote_current_score",
            "detail": str(source_29.get("readout")),
            "action": "do not interpret the 28/29 CMB penalty until repaired score is run",
        },
        {
            "finding": "distance_prior_model_dependence",
            "status": "caveat",
            "detail": "the local table uses the wCDM compressed prior by default for C0/MTS",
            "action": "keep official CMB likelihood upgrade on the roadmap before any public claim",
        },
    ]


def gate_rows(source_29: dict[str, Any], best_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    legacy = next(row for row in best_rows if row["variant"] == "legacy_z_trapezoid_zmax_1e5")
    scale_factor = next(row for row in best_rows if row["variant"] == "scale_factor_quad")
    return [
        {
            "gate": "source_29_requires_CMB_audit",
            "status": "pass" if source_29.get("CMB_distance_status") == "dominant_tension_audit_required" else "fail",
            "detail": str(source_29.get("CMB_distance_status")),
        },
        {
            "gate": "legacy_reproduces_huge_chi2",
            "status": "pass" if float(legacy["best_chi2_full"]) > 1000.0 else "fail",
            "detail": f"legacy_best_chi2={legacy['best_chi2_full']}",
        },
        {
            "gate": "scale_factor_quad_removes_huge_artifact",
            "status": "pass" if float(scale_factor["best_chi2_full"]) < 100.0 else "fail",
            "detail": f"scale_factor_best_chi2={scale_factor['best_chi2_full']}",
        },
        {
            "gate": "current_score_demoted",
            "status": "pass",
            "detail": "the 28/29 first score is an implementation-stress result, not physics verdict",
        },
        {
            "gate": "support_or_death_claim_allowed",
            "status": "fail",
            "detail": "repair run required first",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-checkpoint CMB distance-prior audit.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_29 = load_json(POST_CHECKPOINT / SOURCE_29_STATUS)
    params_order, obs, cov = cmb_data(MAIN_WORKBENCH)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-CMB-distance-prior-implementation-audit"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    variants = variant_rows(params_order, obs, cov)
    best_rows = best_by_variant_rows(variants)
    findings = finding_rows(source_29, best_rows)
    gates = gate_rows(source_29, best_rows)

    write_csv(results_dir / "CMB_variant_scores.csv", variants, list(variants[0].keys()))
    write_csv(results_dir / "CMB_variant_best_by_method.csv", best_rows, list(best_rows[0].keys()))
    write_csv(results_dir / "CMB_audit_findings.csv", findings, list(findings[0].keys()))
    write_csv(results_dir / "CMB_audit_gate_criteria.csv", gates, list(gates[0].keys()))

    passed = all(row["status"] == "pass" for row in gates if row["gate"] != "support_or_death_claim_allowed")
    scale_factor = next(row for row in best_rows if row["variant"] == "scale_factor_quad")
    legacy = next(row for row in best_rows if row["variant"] == "legacy_z_trapezoid_zmax_1e5")
    readout = "CMB_distance_prior_implementation_error_found_repair_required" if passed else "CMB_distance_prior_audit_inconclusive"
    status = {
        "status": "complete_post_checkpoint_CMB_distance_prior_implementation_audit",
        "readout": readout,
        "recommendation": "run_repaired_CMB_distance_score_next",
        "next_target": "31-repaired-growth-CMB-score.md",
        "legacy_best_chi2": legacy["best_chi2_full"],
        "scale_factor_quad_best_chi2": scale_factor["best_chi2_full"],
        "current_score_demoted": True,
        "public_claim_allowed": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "outputs": {
            "CMB_variant_scores": str(results_dir / "CMB_variant_scores.csv"),
            "CMB_variant_best_by_method": str(results_dir / "CMB_variant_best_by_method.csv"),
            "CMB_audit_findings": str(results_dir / "CMB_audit_findings.csv"),
            "CMB_audit_gate_criteria": str(results_dir / "CMB_audit_gate_criteria.csv"),
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
