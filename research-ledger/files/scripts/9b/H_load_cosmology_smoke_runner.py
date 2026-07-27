from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy import linalg, optimize


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
sys.path.insert(0, str(FORMAL / "scripts"))
import cosmology_likelihood_smoke as legacy  # noqa: E402


BASELINES = ("M0", "M2_wCDM", "M2_CPL")
H_MODELS = ("HLOAD_EXP_NEG", "HLOAD_TANH_NEG")
MODEL_ORDER = BASELINES + H_MODELS
Q_BOUNDS = {
    "HLOAD_EXP_NEG": ((2.0 / 3.0) ** (1.0 / 3.0), 1.9038136944403834 ** (1.0 / 3.0)),
    "HLOAD_TANH_NEG": (0.6114532915782878 ** (1.0 / 3.0), 1.4192231900240135 ** (1.0 / 3.0)),
}
PARAM_BOUNDS = {
    "M0": {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
    },
    "M2_wCDM": {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
        "w": (-1.4, -0.6),
    },
    "M2_CPL": {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
        "w0": (-1.6, -0.4),
        "wa": (-2.0, 2.0),
    },
    "HLOAD_EXP_NEG": {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
        "A_H": (-2.0, 0.0),
        "q_H": Q_BOUNDS["HLOAD_EXP_NEG"],
    },
    "HLOAD_TANH_NEG": {
        "h0": (55.0, 85.0),
        "omega_m0": (0.1, 0.5),
        "rd": (130.0, 170.0),
        "A_H": (-2.0, 0.0),
        "q_H": Q_BOUNDS["HLOAD_TANH_NEG"],
    },
}
SAMPLE_PARAMS = {
    "M0": {"h0": 68.8, "omega_m0": 0.31, "rd": 146.3},
    "M2_wCDM": {"h0": 68.6, "omega_m0": 0.30, "rd": 145.7, "w": -0.91},
    "M2_CPL": {"h0": 67.9, "omega_m0": 0.31, "rd": 147.3, "w0": -0.86, "wa": -0.56},
    "HLOAD_EXP_NEG": {"h0": 68.5, "omega_m0": 0.30, "rd": 147.0, "A_H": -0.2, "q_H": 1.02},
    "HLOAD_TANH_NEG": {"h0": 68.5, "omega_m0": 0.30, "rd": 147.0, "A_H": -0.2, "q_H": 0.98},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def kernel_values(model: str, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if model == "HLOAD_EXP_NEG":
        exponential = np.exp(-y)
        function = -np.expm1(-y)
        first = exponential
        second = -exponential
        return function, first, second
    if model == "HLOAD_TANH_NEG":
        function = np.tanh(y)
        first = 1.0 - function * function
        second = -2.0 * function * first
        return function, first, second
    raise ValueError(f"not an H-load model: {model}")


def density_shape(model: str, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    function, first, second = kernel_values(model, y)
    response = function - 3.0 * y * first
    derivative = -2.0 * first - 3.0 * y * second
    return response, derivative


def solve_hload_e(
    model: str,
    z: np.ndarray,
    params: dict[str, float],
    *,
    tolerance: float = 2.0e-12,
    max_iterations: int = 80,
) -> tuple[np.ndarray, dict[str, float]]:
    omega_m = params["omega_m0"]
    amplitude = params["A_H"]
    q_value = params["q_H"]
    if amplitude > 1.0e-14:
        raise ValueError("negative-window H-load branch requires A_H <= 0")
    lower_q, upper_q = Q_BOUNDS[model]
    if not lower_q <= q_value <= upper_q:
        raise ValueError("q_H lies outside the derived density/convexity window")

    z = np.asarray(z, dtype=float)
    base = omega_m * (1.0 + z) ** 3 + 1.0 - omega_m
    y0 = q_value**3
    response0 = float(density_shape(model, np.asarray([y0]))[0][0])
    e_value = np.sqrt(base)
    e_value[0] = 1.0
    converged = False
    minimum_derivative = math.inf
    for iteration in range(max_iterations):
        y = (q_value * e_value) ** 3
        response, response_prime = density_shape(model, y)
        residual = e_value * e_value - base - amplitude * (response - response0)
        derivative = 2.0 * e_value - amplitude * response_prime * 3.0 * q_value**3 * e_value**2
        minimum_derivative = min(minimum_derivative, float(np.min(derivative)))
        if np.any(~np.isfinite(derivative)) or np.any(derivative <= 0.0):
            raise ValueError("implicit H-load branch lost positive derivative")
        step = residual / derivative
        trial = e_value - step
        if np.any(trial <= 0.0) or np.any(~np.isfinite(trial)):
            trial = 0.5 * (e_value + np.sqrt(base))
        e_value = trial
        e_value[0] = 1.0
        if float(np.max(np.abs(residual))) < tolerance:
            converged = True
            break
    y = (q_value * e_value) ** 3
    response, response_prime = density_shape(model, y)
    residual = e_value * e_value - base - amplitude * (response - response0)
    derivative = 2.0 * e_value - amplitude * response_prime * 3.0 * q_value**3 * e_value**2
    maximum_residual = float(np.max(np.abs(residual)))
    if not converged and maximum_residual >= 1.0e-9:
        raise ValueError(f"implicit H-load solve failed, residual={maximum_residual}")

    _, first0, second0 = kernel_values(model, np.asarray([y0]))
    scalar0 = q_value
    hessian_factor0 = float((2.0 * scalar0 * first0[0] + 3.0 * scalar0**4 * second0[0]) / 3.0)
    homogeneous_bracket0 = 6.0 + 27.0 * amplitude * q_value**2 * hessian_factor0
    omega_gamma0 = 1.0 - omega_m - amplitude * response0
    diagnostics = {
        "iterations": float(iteration + 1),
        "maximum_equation_residual": maximum_residual,
        "minimum_implicit_derivative": float(np.min(derivative)),
        "omega_gamma0": omega_gamma0,
        "y0": y0,
        "rho_shape0": response0,
        "G_hessian_factor0": hessian_factor0,
        "homogeneous_kinetic_bracket0": homogeneous_bracket0,
    }
    return e_value, diagnostics


def cumulative_trapezoid(z: np.ndarray, values: np.ndarray) -> np.ndarray:
    output = np.zeros_like(z)
    output[1:] = np.cumsum(0.5 * np.diff(z) * (values[:-1] + values[1:]))
    return output


def background_grid(model: str, params: dict[str, float], z_max: float, steps: int) -> dict[str, Any]:
    if model in BASELINES:
        background = legacy.background_grid(model, params, z_max, steps)
        background["diagnostics"] = {}
        return background
    z = np.linspace(0.0, float(z_max), int(steps))
    e_value, diagnostics = solve_hload_e(model, z, params)
    integral = cumulative_trapezoid(z, 1.0 / e_value)
    d_m = (legacy.C_KM_S / params["h0"]) * integral
    return {"z": z, "e": e_value, "d_m": d_m, "diagnostics": diagnostics}


def distance_modulus(
    model: str,
    params: dict[str, float],
    z_cosmo: np.ndarray,
    z_hel: np.ndarray,
    steps: int,
) -> np.ndarray:
    background = background_grid(model, params, float(np.max(z_cosmo) * 1.01 + 0.01), steps)
    d_m = np.interp(z_cosmo, background["z"], background["d_m"])
    d_l = (1.0 + z_hel) * d_m
    if np.any(d_l <= 0.0):
        raise ValueError("non-positive luminosity distance")
    return 5.0 * np.log10(d_l) + 25.0


def bao_vector(model: str, params: dict[str, float], bao: dict[str, Any], steps: int) -> np.ndarray:
    z = bao["z"]
    background = background_grid(model, params, float(np.max(z) * 1.01 + 0.01), steps)
    d_m = np.interp(z, background["z"], background["d_m"])
    e_value = np.interp(z, background["z"], background["e"])
    d_h = legacy.C_KM_S / (params["h0"] * e_value)
    d_v = np.cbrt(z * d_m * d_m * d_h)
    predicted = []
    for index, quantity in enumerate(bao["quantity"]):
        if quantity == "DM_over_rs":
            predicted.append(d_m[index] / params["rd"])
        elif quantity == "DH_over_rs":
            predicted.append(d_h[index] / params["rd"])
        elif quantity == "DV_over_rs":
            predicted.append(d_v[index] / params["rd"])
        else:
            raise ValueError(f"unsupported BAO quantity: {quantity}")
    return np.asarray(predicted)


def chi2_components(
    model: str,
    params: dict[str, float],
    sn: dict[str, Any],
    bao: dict[str, Any],
    steps: int,
) -> tuple[float, float, float]:
    mu_model = distance_modulus(model, params, sn["z_cosmo"], sn["z_hel"], steps)
    residual = sn["mu_obs"] - mu_model
    c_inv_residual = linalg.cho_solve(sn["cho"], residual, check_finite=False)
    offset = float(sn["ones"] @ c_inv_residual / sn["ones_cinv_ones"])
    adjusted = residual - offset * sn["ones"]
    chi_sn = float(adjusted @ linalg.cho_solve(sn["cho"], adjusted, check_finite=False))
    bao_residual = bao["obs"] - bao_vector(model, params, bao, steps)
    chi_bao = float(bao_residual @ linalg.cho_solve(bao["cho"], bao_residual, check_finite=False))
    return chi_sn, chi_bao, offset


def edge_flags(params: dict[str, float], bounds: dict[str, tuple[float, float]], tolerance: float = 0.01) -> list[str]:
    flags = []
    for name, (lower, upper) in bounds.items():
        span = upper - lower
        value = params[name]
        if value - lower <= tolerance * span:
            flags.append(f"{name}=LOW")
        if upper - value <= tolerance * span:
            flags.append(f"{name}=HIGH")
    return flags


def start_vectors(model: str, names: list[str], bounds: dict[str, tuple[float, float]], count: int) -> list[np.ndarray]:
    sample = SAMPLE_PARAMS[model]
    candidates = [dict(sample)]
    if model in H_MODELS:
        lower_q, upper_q = bounds["q_H"]
        for fraction, amplitude in ((0.25, -0.08), (0.5, -0.3), (0.75, -0.8), (0.5, -1.5)):
            candidate = dict(sample)
            candidate["q_H"] = lower_q + fraction * (upper_q - lower_q)
            candidate["A_H"] = amplitude
            candidates.append(candidate)
    elif model == "M2_wCDM":
        for w_value in (-1.2, -1.0, -0.8):
            candidate = dict(sample)
            candidate["w"] = w_value
            candidates.append(candidate)
    elif model == "M2_CPL":
        for w0, wa in ((-1.0, 0.0), (-0.8, -0.8), (-1.2, 0.8)):
            candidate = dict(sample)
            candidate["w0"] = w0
            candidate["wa"] = wa
            candidates.append(candidate)
    vectors = []
    for candidate in candidates[: max(1, count)]:
        vectors.append(np.asarray([np.clip(candidate[name], *bounds[name]) for name in names], dtype=float))
    return vectors


def fit_model(
    model: str,
    sn: dict[str, Any],
    bao: dict[str, Any],
    *,
    steps: int,
    maxiter: int,
    starts: int,
) -> dict[str, Any]:
    bounds_map = PARAM_BOUNDS[model]
    names = list(bounds_map)
    bounds = [bounds_map[name] for name in names]

    def objective(vector: np.ndarray) -> float:
        params = {name: float(value) for name, value in zip(names, vector)}
        try:
            chi_sn, chi_bao, _ = chi2_components(model, params, sn, bao, steps)
            total = chi_sn + chi_bao
            return total if math.isfinite(total) else 1.0e100
        except Exception:
            return 1.0e100

    attempts = []
    for initial in start_vectors(model, names, bounds_map, starts):
        attempts.append(
            optimize.minimize(
                objective,
                initial,
                method="L-BFGS-B",
                bounds=bounds,
                options={"maxiter": maxiter, "ftol": 1.0e-8, "maxls": 30},
            )
        )
    best = min(attempts, key=lambda item: float(item.fun))
    params = {name: float(value) for name, value in zip(names, best.x)}
    chi_sn, chi_bao, offset = chi2_components(model, params, sn, bao, steps)
    diagnostics: dict[str, float] = {}
    if model in H_MODELS:
        diagnostics = background_grid(model, params, 2.6, steps)["diagnostics"]
    return {
        "model": model,
        "chi2_sn": chi_sn,
        "chi2_bao": chi_bao,
        "chi2_total": chi_sn + chi_bao,
        "sn_offset": offset,
        "n_params": len(names),
        "success": bool(best.success) and math.isfinite(chi_sn + chi_bao),
        "message": f"{best.message}; starts={len(attempts)}",
        "params": params,
        "edge_flags": edge_flags(params, bounds_map),
        "diagnostics": diagnostics,
    }


def evaluate_sample(model: str, sn: dict[str, Any], bao: dict[str, Any], steps: int) -> dict[str, Any]:
    params = dict(SAMPLE_PARAMS[model])
    chi_sn, chi_bao, offset = chi2_components(model, params, sn, bao, steps)
    diagnostics: dict[str, float] = {}
    if model in H_MODELS:
        diagnostics = background_grid(model, params, 2.6, steps)["diagnostics"]
    return {
        "model": model,
        "chi2_sn": chi_sn,
        "chi2_bao": chi_bao,
        "chi2_total": chi_sn + chi_bao,
        "sn_offset": offset,
        "n_params": 0,
        "success": True,
        "message": "sample evaluation",
        "params": params,
        "edge_flags": [],
        "diagnostics": diagnostics,
    }


def add_criteria(result: dict[str, Any], n_data: int) -> None:
    result["aic"] = result["chi2_total"] + 2.0 * result["n_params"]
    result["bic"] = result["chi2_total"] + result["n_params"] * math.log(n_data)


def create_run_folder(label: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = POST / "runs" / f"{timestamp}-{label}"
    (folder / "results").mkdir(parents=True, exist_ok=False)
    return folder


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "branch",
        "model",
        "mode",
        "chi2_sn",
        "chi2_bao",
        "chi2_total",
        "n_params",
        "aic",
        "bic",
        "delta_chi2_vs_M0",
        "delta_aic_vs_best_baseline",
        "delta_bic_vs_best_baseline",
        "best_aic_baseline",
        "best_bic_baseline",
        "edge_flags",
        "success",
        "message",
        "params_json",
        "diagnostics_json",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def finalize_deltas(rows: list[dict[str, Any]]) -> None:
    for branch in sorted({row["branch"] for row in rows}):
        fit_rows = [row for row in rows if row["branch"] == branch and row["mode"] == "fit" and row["success"]]
        m0 = next(row for row in fit_rows if row["model"] == "M0")
        baseline_rows = [row for row in fit_rows if row["model"] in BASELINES]
        best_aic = min(baseline_rows, key=lambda row: row["aic"])
        best_bic = min(baseline_rows, key=lambda row: row["bic"])
        for row in [item for item in rows if item["branch"] == branch]:
            row["delta_chi2_vs_M0"] = row["chi2_total"] - m0["chi2_total"]
            row["delta_aic_vs_best_baseline"] = row["aic"] - best_aic["aic"]
            row["delta_bic_vs_best_baseline"] = row["bic"] - best_bic["bic"]
            row["best_aic_baseline"] = best_aic["model"]
            row["best_bic_baseline"] = best_bic["model"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(FORMAL / "configs" / "cosmology_background_R1_current.json"))
    parser.add_argument("--branches", nargs="+", default=["sh0es", "no_sh0es"])
    parser.add_argument("--steps", type=int, default=1024)
    parser.add_argument("--maxiter", type=int, default=60)
    parser.add_argument("--starts", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    arguments = parser.parse_args()

    config = legacy.load_json(Path(arguments.config))
    bao = legacy.load_bao(ROOT, legacy.select_dataset(config, "BAO"))
    run_folder = arguments.output_dir or create_run_folder("H-load-cosmology-smoke")
    (run_folder / "results").mkdir(parents=True, exist_ok=True)
    status_path = run_folder / "status.json"
    status_path.write_text(json.dumps({"status": "running", "updated": utc_now()}, indent=2), encoding="utf-8")
    rows: list[dict[str, Any]] = []
    try:
        for branch in arguments.branches:
            sn = legacy.load_pantheon(ROOT, legacy.select_dataset(config, "Pantheon"), branch=branch)
            n_data = sn["n"] + bao["n"]
            for model in MODEL_ORDER:
                sample = evaluate_sample(model, sn, bao, arguments.steps)
                add_criteria(sample, n_data)
                sample.update({"branch": branch, "mode": "sample"})
                sample["params_json"] = json.dumps(sample["params"], sort_keys=True)
                sample["diagnostics_json"] = json.dumps(sample["diagnostics"], sort_keys=True)
                rows.append(sample)
                print(f"{branch} {model} sample chi2={sample['chi2_total']:.6f}", flush=True)
                if arguments.dry_run:
                    continue
                fit = fit_model(
                    model,
                    sn,
                    bao,
                    steps=arguments.steps,
                    maxiter=arguments.maxiter,
                    starts=arguments.starts,
                )
                add_criteria(fit, n_data)
                fit.update({"branch": branch, "mode": "fit"})
                fit["params_json"] = json.dumps(fit["params"], sort_keys=True)
                fit["diagnostics_json"] = json.dumps(fit["diagnostics"], sort_keys=True)
                fit["edge_flags"] = ";".join(fit["edge_flags"])
                rows.append(fit)
                print(
                    f"{branch} {model} fit chi2={fit['chi2_total']:.6f} "
                    f"success={fit['success']} edges={fit['edge_flags']}",
                    flush=True,
                )
        if not arguments.dry_run:
            finalize_deltas(rows)
        write_rows(run_folder / "results" / "H_load_smoke_results.csv", rows)
        metadata = {
            "created_utc": utc_now(),
            "config": str(arguments.config),
            "branches": arguments.branches,
            "steps": arguments.steps,
            "maxiter": arguments.maxiter,
            "starts": arguments.starts,
            "dry_run": arguments.dry_run,
            "models": list(MODEL_ORDER),
            "q_bounds": Q_BOUNDS,
        }
        (run_folder / "results" / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        status_path.write_text(json.dumps({"status": "done", "updated": utc_now()}, indent=2), encoding="utf-8")
        (run_folder / "DONE.txt").write_text("done\n", encoding="utf-8")
        print(f"Run folder: {run_folder}")
        return 0
    except Exception as error:
        status_path.write_text(
            json.dumps({"status": "failed", "updated": utc_now(), "error": str(error)}, indent=2),
            encoding="utf-8",
        )
        (run_folder / "FAILED.txt").write_text(str(error), encoding="utf-8")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
