#!/usr/bin/env python3
"""Fixed-row growth, compressed-CMB, and H(z) retest for the best C2 activation."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy import integrate, linalg


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
POST_SCRIPTS = POST_CHECKPOINT / "scripts"
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(POST_SCRIPTS))
sys.path.insert(0, str(MAIN_SCRIPTS))

from activation_regularity_repair_gate import candidate_specs  # noqa: E402
from cosmology_likelihood_smoke import C_KM_S, e2_array  # noqa: E402
from growth_CMB_first_scoring_run import (  # noqa: E402
    N_EFF,
    N_S,
    OMEGA_B_H2,
    SOURCE_161_CONFIG,
    cmb_data,
    load_background_params,
    numeric_rows,
    read_covariance,
    z_star,
)
from post_checkpoint_CMB_distance_prior_implementation_audit import score_prediction  # noqa: E402


SOURCE_PATHS = {
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "47_status": Path("runs/20260531-014459-C2-activation-background-smoke/status.json"),
    "47_scores": Path("runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_scores.csv"),
}

HZ_TABLE = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/Hz_CC_Moresco15_BC03.csv"
HZ_MANIFEST = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/row_lock_manifest.json"
BEST_C2_CANDIDATE = "weibull_p3_match_N50"
BEST_C2_LABEL = "C2_weibull_p3_match_N50"
ORIGINAL_LABEL = "C0_frozen_original_fractional_weibull"
LOCKED_LABEL = "MTS_C0_minimal_smooth_memory_fixed_no_SH0ES"
BASELINE_LABELS = {"LCDM_fixed_no_SH0ES", "wCDM_fixed_no_SH0ES", "CPL_fixed_no_SH0ES"}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    paths = dict(SOURCE_PATHS)
    paths.update(
        {
            "growth_CMB_config": MAIN_WORKBENCH / SOURCE_161_CONFIG,
            "Hz_table": HZ_TABLE,
            "Hz_manifest": HZ_MANIFEST,
        }
    )
    rows: list[dict[str, Any]] = []
    for key, path in paths.items():
        absolute = POST_CHECKPOINT / path if not path.is_absolute() else path
        rows.append({"source_key": key, "path": str(absolute), "exists": absolute.exists()})
    missing = [row["path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def radiation_density(params: dict[str, float]) -> float:
    h = float(params.get("h0", 70.0)) / 100.0
    omega_gamma = 2.469e-5 / (h * h)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation_lookup(params: dict[str, float]) -> dict[str, Callable[[np.ndarray], np.ndarray]]:
    return {spec["candidate"]: spec["activation_fn"] for spec in candidate_specs(params)}


def e2_model(spec: dict[str, Any], z: np.ndarray | float, include_radiation: bool = False) -> np.ndarray:
    z_arr = np.asarray(z, dtype=float)
    params = spec["params"]
    if spec["physics_model"] == "custom_M6":
        activation = spec["activation_fn"](np.log1p(z_arr))
        omega_m = float(params["omega_m0"])
        e2 = omega_m * (1.0 + z_arr) ** 3 + 1.0 - omega_m + float(params["b_mem"]) * activation
    else:
        e2 = e2_array(spec["physics_model"], z_arr, params)
    if include_radiation:
        e2 = e2 + radiation_density(params) * (1.0 + z_arr) ** 4
    return np.asarray(e2, dtype=float)


def background_grid(spec: dict[str, Any], z_max: float, steps: int = 4096) -> dict[str, np.ndarray]:
    z_grid = np.linspace(0.0, float(z_max), int(steps))
    e2 = e2_model(spec, z_grid, include_radiation=False)
    if np.any(~np.isfinite(e2)) or np.any(e2 <= 0.0):
        raise ValueError(f"{spec['model']} produced non-positive E2")
    e = np.sqrt(e2)
    integral = np.zeros_like(z_grid)
    if len(z_grid) > 1:
        integral[1:] = np.cumsum(0.5 * np.diff(z_grid) * (1.0 / e[:-1] + 1.0 / e[1:]))
    d_m = (C_KM_S / float(spec["params"]["h0"])) * integral
    return {"z": z_grid, "e": e, "d_m": d_m}


def growth_solution(spec: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x0 = math.log(1.0e-3)
    x1 = 0.0

    def e2_at_x(x: float) -> float:
        a = math.exp(x)
        return float(e2_model(spec, np.asarray([1.0 / a - 1.0]), include_radiation=False)[0])

    def deriv(x: float, y: np.ndarray) -> list[float]:
        a = math.exp(x)
        e2 = e2_at_x(x)
        eps = 1.0e-4
        if x + eps > 0.0:
            dlnh_dlna = 0.5 * (math.log(e2) - math.log(e2_at_x(x - eps))) / eps
        else:
            dlnh_dlna = 0.25 * (math.log(e2_at_x(x + eps)) - math.log(e2_at_x(x - eps))) / eps
        omega_m_a = float(spec["params"]["omega_m0"]) * a ** -3 / e2
        return [y[1], -(2.0 + dlnh_dlna) * y[1] + 1.5 * omega_m_a * y[0]]

    y0 = np.asarray([math.exp(x0), math.exp(x0)], dtype=float)
    sol = integrate.solve_ivp(deriv, (x0, x1), y0, rtol=1.0e-6, atol=1.0e-9, dense_output=False, max_step=0.02)
    if not sol.success:
        raise ValueError(sol.message)
    d_norm = sol.y[0] / sol.y[0, -1]
    f_values = sol.y[1] / sol.y[0]
    return sol.t, d_norm, f_values


def growth_shape(spec: dict[str, Any], z_values: np.ndarray, growth_cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    model = str(spec["model"])
    if model not in growth_cache:
        growth_cache[model] = growth_solution(spec)
    x_grid, d_grid, f_grid = growth_cache[model]
    x_values = np.log(1.0 / (1.0 + z_values))
    d_values = np.interp(x_values, x_grid, d_grid)
    f_values = np.interp(x_values, x_grid, f_grid)
    return d_values * f_values


def prediction_components(
    spec: dict[str, Any],
    rows: list[tuple[float, float, str]],
    growth_cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
) -> tuple[np.ndarray, np.ndarray]:
    z_values = np.asarray([row[0] for row in rows], dtype=float)
    background = background_grid(spec, float(np.max(z_values) * 1.01 + 0.01), 4096)
    d_m = np.interp(z_values, background["z"], background["d_m"])
    e_values = np.interp(z_values, background["z"], background["e"])
    h0 = float(spec["params"].get("h0", 70.0))
    rd = float(spec["params"].get("rd", 147.0))
    d_h = C_KM_S / (h0 * e_values)
    d_v = np.cbrt(z_values * d_m * d_m * d_h)
    growth_unit = growth_shape(spec, z_values, growth_cache)
    base: list[float] = []
    sigma_component: list[float] = []
    for index, (_, _, quantity) in enumerate(rows):
        if quantity in {"DM_over_rs", "DM_over_rd"}:
            base.append(float(d_m[index] / rd))
            sigma_component.append(0.0)
        elif quantity in {"DH_over_rs", "DH_over_rd"}:
            base.append(float(d_h[index] / rd))
            sigma_component.append(0.0)
        elif quantity in {"DV_over_rs", "DV_over_rd"}:
            base.append(float(d_v[index] / rd))
            sigma_component.append(0.0)
        elif quantity == "f_sigma8":
            base.append(0.0)
            sigma_component.append(float(growth_unit[index]))
        else:
            raise ValueError(f"unsupported quantity: {quantity}")
    return np.asarray(base, dtype=float), np.asarray(sigma_component, dtype=float)


def fit_sigma8_linear(spec: dict[str, Any], files: list[dict[str, str]], growth_cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]) -> tuple[float, float]:
    numerator = 0.0
    denominator = 0.0
    bundles: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = []
    for pair in files:
        rows = numeric_rows(Path(pair["vector_file"]))
        covariance = read_covariance(Path(pair["covariance_file"]))
        obs = np.asarray([row[1] for row in rows], dtype=float)
        base, component = prediction_components(spec, rows, growth_cache)
        cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
        cinv_component = linalg.cho_solve(cho, component, check_finite=False)
        residual_base = obs - base
        numerator += float(component @ linalg.cho_solve(cho, residual_base, check_finite=False))
        denominator += float(component @ cinv_component)
        bundles.append((obs, base, component, covariance))
    sigma8 = numerator / denominator if denominator > 0.0 else 0.8
    sigma8 = min(1.4, max(0.2, sigma8))
    chi2_total = 0.0
    for obs, base, component, covariance in bundles:
        residual = obs - (base + sigma8 * component)
        cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
        chi2_total += float(residual @ linalg.cho_solve(cho, residual, check_finite=False))
    return float(sigma8), float(chi2_total)


def branch_chi2(
    spec: dict[str, Any],
    files: list[dict[str, str]],
    sigma8: float,
    growth_cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
    predictions: list[dict[str, Any]],
    branch: str,
) -> float:
    total = 0.0
    for pair_index, pair in enumerate(files, start=1):
        rows = numeric_rows(Path(pair["vector_file"]))
        covariance = read_covariance(Path(pair["covariance_file"]))
        obs = np.asarray([row[1] for row in rows], dtype=float)
        base, component = prediction_components(spec, rows, growth_cache)
        pred = base + sigma8 * component
        residual = obs - pred
        cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
        total += float(residual @ linalg.cho_solve(cho, residual, check_finite=False))
        for row_index, ((z, observed, quantity), predicted, residual_value) in enumerate(zip(rows, pred, residual), start=1):
            predictions.append(
                {
                    "model": spec["model"],
                    "branch": branch,
                    "pair_index": pair_index,
                    "row_index": row_index,
                    "z": z,
                    "quantity": quantity,
                    "observed": observed,
                    "predicted": float(predicted),
                    "residual": float(residual_value),
                    "sigma8_0": sigma8,
                }
            )
    return float(total)


def cmb_prediction(spec: dict[str, Any]) -> dict[str, float]:
    h0 = float(spec["params"].get("h0", 70.0))
    zs = z_star(spec["params"], OMEGA_B_H2)
    a_star = 1.0 / (1.0 + zs)

    def inv_a2_e(a: float) -> float:
        z = 1.0 / a - 1.0
        return 1.0 / (a * a * math.sqrt(float(e2_model(spec, np.asarray([z]), include_radiation=True)[0])))

    dm_integral = integrate.quad(inv_a2_e, a_star, 1.0, epsrel=1.0e-8, limit=300)[0]
    d_m = (C_KM_S / h0) * dm_integral

    def sound_integrand_a(a: float) -> float:
        z = 1.0 / a - 1.0
        r_b = 31500.0 * OMEGA_B_H2 * a
        c_s = 1.0 / math.sqrt(3.0 * (1.0 + r_b))
        return c_s / (a * a * math.sqrt(float(e2_model(spec, np.asarray([z]), include_radiation=True)[0])))

    sound_integral = integrate.quad(sound_integrand_a, 0.0, a_star, epsrel=1.0e-8, limit=300)[0]
    r_s = (C_KM_S / h0) * sound_integral
    shift_r = math.sqrt(float(spec["params"]["omega_m0"])) * h0 * d_m / C_KM_S
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


def load_hz_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(HZ_TABLE):
        rows.append({"z": float(row["z"]), "H": float(row["H"]), "sigma": float(row["sigma"]), "reference": row.get("reference", "")})
    return rows


def read_hz_covariance() -> np.ndarray:
    manifest = json.loads(HZ_MANIFEST.read_text(encoding="utf-8"))
    relative = Path(manifest["matrix_paths"]["suggested"])
    path = relative if relative.is_absolute() else MAIN_WORKBENCH / relative
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        matrix = np.asarray([[float(value) for value in row[1:]] for row in reader], dtype=float)
    if matrix.shape[0] + 1 != len(header):
        raise ValueError("H(z) covariance header mismatch")
    return matrix


def hz_chi2(spec: dict[str, Any], hz_rows: list[dict[str, Any]], covariance: np.ndarray) -> float:
    z = np.asarray([row["z"] for row in hz_rows], dtype=float)
    observed = np.asarray([row["H"] for row in hz_rows], dtype=float)
    predicted = float(spec["params"]["h0"]) * np.sqrt(e2_model(spec, z, include_radiation=False))
    residual = predicted - observed
    lower = np.linalg.cholesky(covariance)
    y = np.linalg.solve(lower, residual)
    weighted = np.linalg.solve(lower.T, y)
    return float(residual @ weighted)


def fixed_specs(source_38: dict[str, Any]) -> list[dict[str, Any]]:
    background = load_background_params(MAIN_WORKBENCH)
    specs: list[dict[str, Any]] = []
    mapping = {
        "LCDM": "LCDM_fixed_no_SH0ES",
        "wCDM": "wCDM_fixed_no_SH0ES",
        "CPL": "CPL_fixed_no_SH0ES",
        "MTS_C0_minimal_smooth_memory": LOCKED_LABEL,
    }
    for model, label in mapping.items():
        entry = background[model]
        specs.append(
            {
                "model": label,
                "physics_model": entry["physics_model"],
                "params": {key: float(value) for key, value in entry["params"].items()},
                "activation_candidate": "",
                "parameter_origin": "no_SH0ES_background_locked",
                "claim_limit": "reference_only",
            }
        )
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    lookup = activation_lookup(params)
    specs.append(
        {
            "model": ORIGINAL_LABEL,
            "physics_model": "custom_M6",
            "params": dict(params),
            "activation_candidate": "original_fractional_weibull",
            "activation_fn": lookup["original_fractional_weibull"],
            "parameter_origin": "checkpoint_38_frozen_no_rescue",
            "claim_limit": "closure_guardrail_only",
        }
    )
    specs.append(
        {
            "model": BEST_C2_LABEL,
            "physics_model": "custom_M6",
            "params": dict(params),
            "activation_candidate": BEST_C2_CANDIDATE,
            "activation_fn": lookup[BEST_C2_CANDIDATE],
            "parameter_origin": "checkpoint_38_frozen_with_C2_activation_no_rescue",
            "claim_limit": "regularized_closure_guardrail_only",
        }
    )
    return specs


def score_all(config: dict[str, Any], specs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cmb_params, cmb_obs, cmb_cov = cmb_data(MAIN_WORKBENCH)
    hz_rows = load_hz_rows()
    hz_cov = read_hz_covariance()
    growth_cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    score_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    cmb_rows: list[dict[str, Any]] = []
    for spec in specs:
        sigma8, _ = fit_sigma8_linear(spec, config["primary_growth_files"], growth_cache)
        primary_predictions: list[dict[str, Any]] = []
        primary_chi2 = branch_chi2(spec, config["primary_growth_files"], sigma8, growth_cache, primary_predictions, "primary_BAO_plus")
        prediction_rows.extend(primary_predictions)
        full_predictions: list[dict[str, Any]] = []
        full_chi2 = branch_chi2(spec, config["robustness_growth_files"], sigma8, growth_cache, full_predictions, "robustness_full_shape_only")
        prediction_rows.extend(full_predictions)
        cmb_pred_map = cmb_prediction(spec)
        cmb_chi2, cmb_without_l_a, l_a_pull = score_prediction(cmb_pred_map, cmb_params, cmb_obs, cmb_cov)
        hz_value = hz_chi2(spec, hz_rows, hz_cov)
        for parameter in cmb_params:
            cmb_rows.append(
                {
                    "model": spec["model"],
                    "parameter": parameter,
                    "predicted": cmb_pred_map[parameter],
                    "claim_limit": spec["claim_limit"],
                }
            )
        score_rows.append(
            {
                "model": spec["model"],
                "physics_model": spec["physics_model"],
                "activation_candidate": spec["activation_candidate"],
                "parameter_origin": spec["parameter_origin"],
                "chi2_growth_primary": primary_chi2,
                "chi2_growth_full_shape_only": full_chi2,
                "chi2_CMB_repaired": cmb_chi2,
                "chi2_CMB_without_l_A": cmb_without_l_a,
                "l_A_pull_sigma": l_a_pull,
                "chi2_Hz_suggested": hz_value,
                "chi2_primary_growth_plus_CMB": primary_chi2 + cmb_chi2,
                "chi2_primary_growth_plus_CMB_plus_Hz": primary_chi2 + cmb_chi2 + hz_value,
                "sigma8_0_fit_primary": sigma8,
                "claim_limit": spec["claim_limit"],
                "params_json": json.dumps(spec["params"], sort_keys=True),
            }
        )
    add_deltas(score_rows)
    return score_rows, prediction_rows, cmb_rows


def add_deltas(rows: list[dict[str, Any]]) -> None:
    original = next(row for row in rows if row["model"] == ORIGINAL_LABEL)
    c2 = next(row for row in rows if row["model"] == BEST_C2_LABEL)
    locked = next(row for row in rows if row["model"] == LOCKED_LABEL)
    fixed_baselines = [row for row in rows if row["model"] in BASELINE_LABELS]
    best_growth = min(fixed_baselines, key=lambda row: float(row["chi2_growth_primary"]))
    best_cmb = min(fixed_baselines, key=lambda row: float(row["chi2_CMB_repaired"]))
    best_total = min(fixed_baselines, key=lambda row: float(row["chi2_primary_growth_plus_CMB_plus_Hz"]))
    for row in rows:
        row["delta_growth_primary_vs_original_frozen"] = float(row["chi2_growth_primary"]) - float(original["chi2_growth_primary"])
        row["delta_growth_full_shape_vs_original_frozen"] = float(row["chi2_growth_full_shape_only"]) - float(original["chi2_growth_full_shape_only"])
        row["delta_CMB_vs_original_frozen"] = float(row["chi2_CMB_repaired"]) - float(original["chi2_CMB_repaired"])
        row["delta_Hz_vs_original_frozen"] = float(row["chi2_Hz_suggested"]) - float(original["chi2_Hz_suggested"])
        row["delta_total_vs_original_frozen"] = float(row["chi2_primary_growth_plus_CMB_plus_Hz"]) - float(original["chi2_primary_growth_plus_CMB_plus_Hz"])
        row["delta_growth_primary_vs_locked_C0"] = float(row["chi2_growth_primary"]) - float(locked["chi2_growth_primary"])
        row["delta_total_vs_best_fixed_baseline"] = float(row["chi2_primary_growth_plus_CMB_plus_Hz"]) - float(best_total["chi2_primary_growth_plus_CMB_plus_Hz"])
        row["best_fixed_growth_baseline"] = best_growth["model"]
        row["best_fixed_CMB_baseline"] = best_cmb["model"]
        row["best_fixed_total_baseline"] = best_total["model"]
        row["delta_total_vs_C2"] = float(row["chi2_primary_growth_plus_CMB_plus_Hz"]) - float(c2["chi2_primary_growth_plus_CMB_plus_Hz"])


def gate_rows(source_47: dict[str, Any], scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c2 = next(row for row in scores if row["model"] == BEST_C2_LABEL)
    return [
        {
            "gate": "source_47_complete",
            "status": "pass" if source_47.get("readout") == "C2_activation_background_smoke_retains_best_repair_not_evidence" else "fail",
            "detail": str(source_47.get("readout")),
        },
        {
            "gate": "C2_primary_growth_not_worse_than_original_by_2",
            "status": "pass" if float(c2["delta_growth_primary_vs_original_frozen"]) <= 2.0 else "fail",
            "detail": f"delta={c2['delta_growth_primary_vs_original_frozen']}; threshold=2",
        },
        {
            "gate": "C2_full_shape_growth_not_worse_than_original_by_2",
            "status": "pass" if float(c2["delta_growth_full_shape_vs_original_frozen"]) <= 2.0 else "fail",
            "detail": f"delta={c2['delta_growth_full_shape_vs_original_frozen']}; threshold=2",
        },
        {
            "gate": "C2_CMB_not_worse_than_original_by_5",
            "status": "pass" if float(c2["delta_CMB_vs_original_frozen"]) <= 5.0 else "fail",
            "detail": f"delta={c2['delta_CMB_vs_original_frozen']}; threshold=5",
        },
        {
            "gate": "C2_Hz_not_worse_than_original_by_1",
            "status": "pass" if float(c2["delta_Hz_vs_original_frozen"]) <= 1.0 else "fail",
            "detail": f"delta={c2['delta_Hz_vs_original_frozen']}; threshold=1",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "C2 activation is regularized closure, not parent-derived",
        },
    ]


def decision_rows(scores: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c2 = next(row for row in scores if row["model"] == BEST_C2_LABEL)
    blocking = [row for row in gates if row["gate"].startswith("C2_") and row["status"] == "fail"]
    retained = not blocking
    return [
        {
            "decision": "C2_activation_growth_CMB_status",
            "status": "retained_regularized_closure_candidate" if retained else "demote_C2_regularized_route",
            "evidence": f"blocking_gates={len(blocking)}; delta_total_vs_original={c2['delta_total_vs_original_frozen']}",
            "next_action": "package regularized closure ledger" if retained else "return to parent activation derivation",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "regularized activation is not parent-derived and compressed CMB is not official spectra/lensing",
            "next_action": "closure language only",
        },
        {
            "decision": "recommended_next_target",
            "status": "49-C2-regularized-closure-ledger.md" if retained else "49-parent-activation-derivation-repair.md",
            "evidence": "growth/CMB/H(z) fixed-row guardrail determines whether regularized scalar-action route remains worth carrying",
            "next_action": "write retained/demoted status ledger",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="C2 activation fixed-row growth/CMB/H(z) retest.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json(absolute_source("38_status"))
    source_47 = load_json(absolute_source("47_status"))
    config = load_json(MAIN_WORKBENCH / SOURCE_161_CONFIG)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-C2-activation-growth-CMB-retest"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    specs = fixed_specs(source_38)
    scores, growth_predictions, cmb_predictions = score_all(config, specs)
    gates = gate_rows(source_47, scores)
    decisions = decision_rows(scores, gates)
    c2 = next(row for row in scores if row["model"] == BEST_C2_LABEL)
    retained = next(row for row in decisions if row["decision"] == "C2_activation_growth_CMB_status")["status"] == "retained_regularized_closure_candidate"

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "C2_activation_growth_CMB_scores.csv", scores, list(scores[0].keys()))
    write_csv(results_dir / "C2_growth_predictions.csv", growth_predictions, list(growth_predictions[0].keys()))
    write_csv(results_dir / "C2_CMB_predictions.csv", cmb_predictions, list(cmb_predictions[0].keys()))
    write_csv(results_dir / "C2_activation_growth_CMB_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    readout = (
        "C2_activation_growth_CMB_retest_retains_regularized_closure_not_evidence"
        if retained
        else "C2_activation_growth_CMB_retest_demotes_regularized_route"
    )
    status = {
        "status": "complete_C2_activation_growth_CMB_retest",
        "readout": readout,
        "recommendation": "write_C2_regularized_closure_ledger_next" if retained else "return_to_parent_activation_derivation",
        "next_target": "49-C2-regularized-closure-ledger.md" if retained else "49-parent-activation-derivation-repair.md",
        "best_C2_model": BEST_C2_LABEL,
        "C2_delta_growth_primary_vs_original": c2["delta_growth_primary_vs_original_frozen"],
        "C2_delta_growth_full_shape_vs_original": c2["delta_growth_full_shape_vs_original_frozen"],
        "C2_delta_CMB_vs_original": c2["delta_CMB_vs_original_frozen"],
        "C2_delta_Hz_vs_original": c2["delta_Hz_vs_original_frozen"],
        "C2_delta_total_vs_original": c2["delta_total_vs_original_frozen"],
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "C2_activation_growth_CMB_scores": str(results_dir / "C2_activation_growth_CMB_scores.csv"),
            "C2_growth_predictions": str(results_dir / "C2_growth_predictions.csv"),
            "C2_CMB_predictions": str(results_dir / "C2_CMB_predictions.csv"),
            "C2_activation_growth_CMB_gates": str(results_dir / "C2_activation_growth_CMB_gates.csv"),
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
