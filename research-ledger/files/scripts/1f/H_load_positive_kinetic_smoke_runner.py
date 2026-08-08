from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
sys.path.insert(0, str(POST / "scripts"))
import H_load_cosmology_smoke_runner as negative_runner  # noqa: E402


BASELINES = negative_runner.BASELINES
POSITIVE_MODELS = ("HLOAD_EXP_POS_KSAFE", "HLOAD_TANH_POS_KSAFE")
MODEL_ORDER = BASELINES + POSITIVE_MODELS
NEGATIVE_KERNEL = {
    "HLOAD_EXP_POS_KSAFE": "HLOAD_EXP_NEG",
    "HLOAD_TANH_POS_KSAFE": "HLOAD_TANH_NEG",
}
Y_RHO_ROOT = {
    "HLOAD_EXP_POS_KSAFE": 1.9038136944403834,
    "HLOAD_TANH_POS_KSAFE": 1.4192231900240135,
}
F_K_MAX = 0.95
Y_SATURATION = {
    "HLOAD_EXP_POS_KSAFE": -math.log(0.01),
    "HLOAD_TANH_POS_KSAFE": math.atanh(0.99),
}
Q_BOUNDS = {
    model: (Y_RHO_ROOT[model] ** (1.0 / 3.0), Y_SATURATION[model] ** (1.0 / 3.0))
    for model in POSITIVE_MODELS
}
POSITIVE_BOUNDS = {
    model: {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
        "f_K": (0.0, F_K_MAX),
        "q_H": Q_BOUNDS[model],
    }
    for model in POSITIVE_MODELS
}


def configure_theory_bounds(fraction_maximum: float, saturation: float) -> None:
    global F_K_MAX, Y_SATURATION, Q_BOUNDS, POSITIVE_BOUNDS
    if not 0.0 < fraction_maximum < 1.0:
        raise ValueError("f_K maximum must lie strictly between zero and one")
    if not 0.9 <= saturation < 1.0:
        raise ValueError("kernel saturation must lie in [0.9,1)")
    F_K_MAX = fraction_maximum
    Y_SATURATION = {
        "HLOAD_EXP_POS_KSAFE": -math.log(1.0 - saturation),
        "HLOAD_TANH_POS_KSAFE": math.atanh(saturation),
    }
    Q_BOUNDS = {
        model: (Y_RHO_ROOT[model] ** (1.0 / 3.0), Y_SATURATION[model] ** (1.0 / 3.0))
        for model in POSITIVE_MODELS
    }
    POSITIVE_BOUNDS = {
        model: {
            "h0": (55.0, 85.0),
            "omega_m0": (0.1, 0.5),
            "rd": (130.0, 170.0),
            "f_K": (0.0, F_K_MAX),
            "q_H": Q_BOUNDS[model],
        }
        for model in POSITIVE_MODELS
    }
SAMPLES = {
    "HLOAD_EXP_POS_KSAFE": {"h0": 68.5, "omega_m0": 0.3, "rd": 147.0, "f_K": 0.3, "q_H": 1.38},
    "HLOAD_TANH_POS_KSAFE": {"h0": 68.5, "omega_m0": 0.3, "rd": 147.0, "f_K": 0.3, "q_H": 1.25},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def mapped_kernel(model: str) -> str:
    return NEGATIVE_KERNEL[model]


def kernel_values(model: str, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return negative_runner.kernel_values(mapped_kernel(model), y)


def density_shape(model: str, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return negative_runner.density_shape(mapped_kernel(model), y)


def hessian_factor(model: str, q_value: float) -> float:
    y = q_value**3
    _, first, second = kernel_values(model, np.asarray([y]))
    return float((2.0 * q_value * first[0] + 3.0 * q_value**4 * second[0]) / 3.0)


def amplitude_from_fraction(model: str, q_value: float, fraction: float) -> tuple[float, float]:
    factor = hessian_factor(model, q_value)
    if factor >= 0.0:
        raise ValueError("positive-density q branch must have negative G curvature factor")
    maximum = 6.0 / (-27.0 * q_value**2 * factor)
    return fraction * maximum, maximum


def solve_positive_e(
    model: str,
    z: np.ndarray,
    params: dict[str, float],
    *,
    tolerance: float = 2.0e-12,
    max_iterations: int = 100,
) -> tuple[np.ndarray, dict[str, float]]:
    q_value = params["q_H"]
    fraction = params["f_K"]
    lower_q, upper_q = Q_BOUNDS[model]
    if not lower_q <= q_value <= upper_q:
        raise ValueError("q_H outside positive-density branch")
    if not 0.0 <= fraction <= F_K_MAX:
        raise ValueError("f_K outside kinetic-safe branch")
    amplitude, amplitude_maximum = amplitude_from_fraction(model, q_value, fraction)
    omega_m = params["omega_m0"]
    z = np.asarray(z, dtype=float)
    base = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m
    y0 = q_value**3
    response0 = float(density_shape(model, np.asarray([y0]))[0][0])
    e_value = np.sqrt(base)
    e_value[0] = 1.0
    for iteration in range(max_iterations):
        y = (q_value * e_value) ** 3
        response, response_prime = density_shape(model, y)
        residual = e_value**2 - base - amplitude * (response - response0)
        derivative = 2.0 * e_value - amplitude * response_prime * 3.0 * q_value**3 * e_value**2
        if np.any(~np.isfinite(derivative)) or np.any(derivative <= 0.0):
            raise ValueError("positive branch lost implicit derivative")
        trial = e_value - residual / derivative
        if np.any(trial <= 0.0) or np.any(~np.isfinite(trial)):
            trial = 0.5 * (e_value + np.sqrt(base))
        e_value = trial
        e_value[0] = 1.0
        if float(np.max(np.abs(residual))) < tolerance:
            break
    y = (q_value * e_value) ** 3
    response, response_prime = density_shape(model, y)
    residual = e_value**2 - base - amplitude * (response - response0)
    derivative = 2.0 * e_value - amplitude * response_prime * 3.0 * q_value**3 * e_value**2
    maximum_residual = float(np.max(np.abs(residual)))
    if maximum_residual >= 1.0e-9:
        raise ValueError(f"positive implicit solve residual {maximum_residual}")
    factor0 = hessian_factor(model, q_value)
    kinetic0 = 6.0 + 27.0 * amplitude * q_value**2 * factor0
    diagnostics = {
        "A_H": amplitude,
        "A_H_max": amplitude_maximum,
        "f_K": fraction,
        "q_H": q_value,
        "y0": y0,
        "rho_shape0": response0,
        "omega_gamma0": 1.0 - omega_m - amplitude * response0,
        "G_hessian_factor0": factor0,
        "homogeneous_kinetic_bracket0": kinetic0,
        "expected_kinetic_bracket0": 6.0 * (1.0 - fraction),
        "minimum_implicit_derivative": float(np.min(derivative)),
        "maximum_equation_residual": maximum_residual,
        "iterations": float(iteration + 1),
    }
    return e_value, diagnostics


def background_grid(model: str, params: dict[str, float], z_max: float, steps: int) -> dict[str, Any]:
    if model in BASELINES:
        return negative_runner.background_grid(model, params, z_max, steps)
    z = np.linspace(0.0, z_max, steps)
    e_value, diagnostics = solve_positive_e(model, z, params)
    integral = negative_runner.cumulative_trapezoid(z, 1.0 / e_value)
    d_m = (negative_runner.legacy.C_KM_S / params["h0"]) * integral
    return {"z": z, "e": e_value, "d_m": d_m, "diagnostics": diagnostics}


def distance_modulus(model: str, params: dict[str, float], sn: dict[str, Any], steps: int) -> np.ndarray:
    background = background_grid(model, params, float(np.max(sn["z_cosmo"]) * 1.01 + 0.01), steps)
    d_m = np.interp(sn["z_cosmo"], background["z"], background["d_m"])
    d_l = (1.0 + sn["z_hel"]) * d_m
    if np.any(d_l <= 0.0):
        raise ValueError("non-positive luminosity distance")
    return 5.0 * np.log10(d_l) + 25.0


def bao_vector(model: str, params: dict[str, float], bao: dict[str, Any], steps: int) -> np.ndarray:
    background = background_grid(model, params, float(np.max(bao["z"]) * 1.01 + 0.01), steps)
    d_m = np.interp(bao["z"], background["z"], background["d_m"])
    e_value = np.interp(bao["z"], background["z"], background["e"])
    d_h = negative_runner.legacy.C_KM_S / (params["h0"] * e_value)
    d_v = np.cbrt(bao["z"] * d_m * d_m * d_h)
    predicted = []
    for index, quantity in enumerate(bao["quantity"]):
        if quantity == "DM_over_rs":
            predicted.append(d_m[index] / params["rd"])
        elif quantity == "DH_over_rs":
            predicted.append(d_h[index] / params["rd"])
        elif quantity == "DV_over_rs":
            predicted.append(d_v[index] / params["rd"])
        else:
            raise ValueError(quantity)
    return np.asarray(predicted)


def chi2(model: str, params: dict[str, float], sn: dict[str, Any], bao: dict[str, Any], steps: int) -> tuple[float, float, float]:
    if model in BASELINES:
        return negative_runner.chi2_components(model, params, sn, bao, steps)
    mu_model = distance_modulus(model, params, sn, steps)
    residual = sn["mu_obs"] - mu_model
    c_inv = linalg.cho_solve(sn["cho"], residual, check_finite=False)
    offset = float(sn["ones"] @ c_inv / sn["ones_cinv_ones"])
    adjusted = residual - offset * sn["ones"]
    chi_sn = float(adjusted @ linalg.cho_solve(sn["cho"], adjusted, check_finite=False))
    bao_residual = bao["obs"] - bao_vector(model, params, bao, steps)
    chi_bao = float(bao_residual @ linalg.cho_solve(bao["cho"], bao_residual, check_finite=False))
    return chi_sn, chi_bao, offset


def bounds_for(model: str) -> dict[str, tuple[float, float]]:
    if model in BASELINES:
        return negative_runner.PARAM_BOUNDS[model]
    return POSITIVE_BOUNDS[model]


def sample_for(model: str) -> dict[str, float]:
    if model in BASELINES:
        return negative_runner.SAMPLE_PARAMS[model]
    return SAMPLES[model]


def starts_for(model: str, count: int) -> list[dict[str, float]]:
    sample = dict(sample_for(model))
    rows = [sample]
    if model in POSITIVE_MODELS:
        lower_q, upper_q = Q_BOUNDS[model]
        for fraction, q_fraction in ((0.05, 0.25), (0.4, 0.5), (0.8, 0.75), (0.94, 0.5)):
            row = dict(sample)
            row["f_K"] = fraction
            row["q_H"] = lower_q + q_fraction * (upper_q - lower_q)
            rows.append(row)
    elif model == "M2_wCDM":
        for value in (-1.2, -1.0, -0.8):
            row = dict(sample)
            row["w"] = value
            rows.append(row)
    elif model == "M2_CPL":
        for w0, wa in ((-1.0, 0.0), (-0.8, -0.8), (-1.2, 0.8)):
            row = dict(sample)
            row["w0"] = w0
            row["wa"] = wa
            rows.append(row)
    return rows[: max(1, count)]


def fit_model(model: str, sn: dict[str, Any], bao: dict[str, Any], steps: int, maxiter: int, starts: int) -> dict[str, Any]:
    bounds_map = bounds_for(model)
    names = list(bounds_map)
    scipy_bounds = [bounds_map[name] for name in names]

    def objective(vector: np.ndarray) -> float:
        params = {name: float(value) for name, value in zip(names, vector)}
        try:
            chi_sn, chi_bao, _ = chi2(model, params, sn, bao, steps)
            total = chi_sn + chi_bao
            return total if math.isfinite(total) else 1.0e100
        except Exception:
            return 1.0e100

    attempts = []
    for row in starts_for(model, starts):
        vector = np.asarray([np.clip(row[name], *bounds_map[name]) for name in names])
        attempts.append(
            optimize.minimize(
                objective,
                vector,
                method="L-BFGS-B",
                bounds=scipy_bounds,
                options={"maxiter": maxiter, "ftol": 1.0e-8, "maxls": 30},
            )
        )
    best = min(attempts, key=lambda item: float(item.fun))
    params = {name: float(value) for name, value in zip(names, best.x)}
    chi_sn, chi_bao, offset = chi2(model, params, sn, bao, steps)
    diagnostics: dict[str, float] = {}
    if model in POSITIVE_MODELS:
        diagnostics = background_grid(model, params, 2.6, steps)["diagnostics"]
    return {
        "model": model,
        "chi2_sn": chi_sn,
        "chi2_bao": chi_bao,
        "chi2_total": chi_sn + chi_bao,
        "sn_offset": offset,
        "n_params": len(names),
        "success": bool(best.success),
        "message": f"{best.message}; starts={len(attempts)}",
        "params": params,
        "edge_flags": negative_runner.edge_flags(params, bounds_map),
        "diagnostics": diagnostics,
    }


def evaluate(model: str, sn: dict[str, Any], bao: dict[str, Any], steps: int) -> dict[str, Any]:
    params = dict(sample_for(model))
    chi_sn, chi_bao, offset = chi2(model, params, sn, bao, steps)
    diagnostics: dict[str, float] = {}
    if model in POSITIVE_MODELS:
        diagnostics = background_grid(model, params, 2.6, steps)["diagnostics"]
    return {
        "model": model,
        "chi2_sn": chi_sn,
        "chi2_bao": chi_bao,
        "chi2_total": chi_sn + chi_bao,
        "sn_offset": offset,
        "n_params": 0,
        "success": True,
        "message": "sample",
        "params": params,
        "edge_flags": [],
        "diagnostics": diagnostics,
    }


def add_criteria(row: dict[str, Any], n_data: int) -> None:
    row["aic"] = row["chi2_total"] + 2.0 * row["n_params"]
    row["bic"] = row["chi2_total"] + row["n_params"] * math.log(n_data)


def finalize(rows: list[dict[str, Any]]) -> None:
    for branch in sorted({row["branch"] for row in rows}):
        fits = [row for row in rows if row["branch"] == branch and row["mode"] == "fit"]
        m0 = next(row for row in fits if row["model"] == "M0")
        baselines = [row for row in fits if row["model"] in BASELINES]
        best_aic = min(baselines, key=lambda row: row["aic"])
        best_bic = min(baselines, key=lambda row: row["bic"])
        for row in [item for item in rows if item["branch"] == branch]:
            row["delta_chi2_vs_M0"] = row["chi2_total"] - m0["chi2_total"]
            row["delta_aic_vs_best_baseline"] = row["aic"] - best_aic["aic"]
            row["delta_bic_vs_best_baseline"] = row["bic"] - best_bic["bic"]
            row["best_aic_baseline"] = best_aic["model"]
            row["best_bic_baseline"] = best_bic["model"]


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "branch", "model", "mode", "chi2_sn", "chi2_bao", "chi2_total", "n_params", "aic", "bic",
        "delta_chi2_vs_M0", "delta_aic_vs_best_baseline", "delta_bic_vs_best_baseline",
        "best_aic_baseline", "best_bic_baseline", "edge_flags", "success", "message", "params_json",
        "diagnostics_json",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(FORMAL / "configs" / "cosmology_background_R1_current.json"))
    parser.add_argument("--branches", nargs="+", default=["sh0es", "no_sh0es"])
    parser.add_argument("--steps", type=int, default=768)
    parser.add_argument("--maxiter", type=int, default=50)
    parser.add_argument("--starts", type=int, default=3)
    parser.add_argument("--f-k-max", type=float, default=0.95)
    parser.add_argument("--kernel-saturation", type=float, default=0.99)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    configure_theory_bounds(args.f_k_max, args.kernel_saturation)
    config = negative_runner.legacy.load_json(Path(args.config))
    bao = negative_runner.legacy.load_bao(ROOT, negative_runner.legacy.select_dataset(config, "BAO"))
    (args.output_dir / "results").mkdir(parents=True, exist_ok=True)
    status = args.output_dir / "status.json"
    status.write_text(json.dumps({"status": "running", "updated": utc_now()}, indent=2), encoding="utf-8")
    rows: list[dict[str, Any]] = []
    try:
        for branch in args.branches:
            sn = negative_runner.legacy.load_pantheon(
                ROOT,
                negative_runner.legacy.select_dataset(config, "Pantheon"),
                branch=branch,
            )
            n_data = sn["n"] + bao["n"]
            for model in MODEL_ORDER:
                sample = evaluate(model, sn, bao, args.steps)
                add_criteria(sample, n_data)
                sample.update({"branch": branch, "mode": "sample"})
                sample["params_json"] = json.dumps(sample["params"], sort_keys=True)
                sample["diagnostics_json"] = json.dumps(sample["diagnostics"], sort_keys=True)
                rows.append(sample)
                print(f"{branch} {model} sample chi2={sample['chi2_total']:.6f}", flush=True)
                if args.dry_run:
                    continue
                fit = fit_model(model, sn, bao, args.steps, args.maxiter, args.starts)
                add_criteria(fit, n_data)
                fit.update({"branch": branch, "mode": "fit"})
                fit["params_json"] = json.dumps(fit["params"], sort_keys=True)
                fit["diagnostics_json"] = json.dumps(fit["diagnostics"], sort_keys=True)
                fit["edge_flags"] = ";".join(fit["edge_flags"])
                rows.append(fit)
                print(
                    f"{branch} {model} fit chi2={fit['chi2_total']:.6f} success={fit['success']} "
                    f"edges={fit['edge_flags']}",
                    flush=True,
                )
        if not args.dry_run:
            finalize(rows)
        write_rows(args.output_dir / "results" / "H_load_positive_smoke_results.csv", rows)
        metadata = {
            "created_utc": utc_now(),
            "steps": args.steps,
            "maxiter": args.maxiter,
            "starts": args.starts,
            "dry_run": args.dry_run,
            "models": MODEL_ORDER,
            "q_bounds": Q_BOUNDS,
            "f_K_max": F_K_MAX,
            "kernel_saturation": args.kernel_saturation,
            "y_saturation": Y_SATURATION,
        }
        (args.output_dir / "results" / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        status.write_text(json.dumps({"status": "done", "updated": utc_now()}, indent=2), encoding="utf-8")
        (args.output_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
        return 0
    except Exception as error:
        status.write_text(json.dumps({"status": "failed", "updated": utc_now(), "error": str(error)}, indent=2), encoding="utf-8")
        (args.output_dir / "FAILED.txt").write_text(str(error), encoding="utf-8")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
