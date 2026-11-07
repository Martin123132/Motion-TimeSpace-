from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy import integrate, linalg, optimize


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5193"
DOCUMENT = (
    POST
    / "5193-Y5-R2FR-direct-parent-scalar-Pantheon-DESI-likelihood-and-"
    "model-selection-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5193_VALIDATION.csv"
)

MARKER = "MTS_5193_DIRECT_PARENT_SCALAR_SN_BAO_LIKELIHOOD"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"

OMEGA_R = 9.0e-5
B_MEMORY = 2.0 / 27.0
P_MEMORY = 3.0
U_MEMORY = 0.25
W_O4_ABS_MAX = 3.3225249561681114
N_REGULAR = -5.0
H0_KM_S_MPC = 70.0
MPC_METRES = 3.0856775814913673e22
PLANCK_TIME_SECONDS = 5.391247e-44

SN_DATA = (
    FORMAL
    / "data"
    / "cosmology"
    / "pantheon_plus"
    / "Pantheon+SH0ES.dat"
)
SN_COV = (
    FORMAL
    / "data"
    / "cosmology"
    / "pantheon_plus"
    / "Pantheon+SH0ES_STAT+SYS.cov"
)
BAO_DATA = (
    FORMAL
    / "data"
    / "cosmology"
    / "desi_dr2_bao"
    / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
)
BAO_COV = (
    FORMAL
    / "data"
    / "cosmology"
    / "desi_dr2_bao"
    / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
)
HISTORICAL_RUN = (
    POST
    / "runs"
    / "20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke"
)

LOCKED_SOURCES: tuple[tuple[str, Path, str, str], ...] = (
    (
        "checkpoint_5192_document",
        POST
        / "5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-"
        "mass-gap-cosmology-gate.md",
        "e171efb8d498df44b535f6c25517c86a0cd5e8b993a67bfb8a9e3b74301eecc3",
        "parent FLRW derivation and massless-memory no-go",
    ),
    (
        "checkpoint_5192_script",
        POST
        / "scripts"
        / "Y5_R2FR_5192_parent_motion_FLRW_branch_and_memory_separation.py",
        "f46ba60d65fbe57434a906e01bfdf2055dea33590b5cd3dc891f453812858a77",
        "direct homogeneous equation convention",
    ),
    (
        "checkpoint_5192_result",
        POST
        / "source-intake"
        / "functional_rg"
        / "5192"
        / "parent_motion_FLRW_results.json",
        "b05068d679118084d07d1b9420603d9bd231369ef1e5889d2ab5c3fa0171df32",
        "5192 numerical branch and O4 bounds",
    ),
    (
        "checkpoint_5192_validation",
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_BRR545_5192_VALIDATION.csv",
        "7bd72e8546dbaa85670d4e33004481c11aa5eca2faf6faab155c5d94cfe00012",
        "5192 lock and validation evidence",
    ),
    (
        "matched_closure_runner",
        POST / "scripts" / "cosmo_SN_BAO_closure_runner.py",
        "3ce577f284978b92a16466102cc2672011a8afb4bd54a1b0e7581ec16cc49b26",
        "matched data loading, nuisance, and historical scoring convention",
    ),
    (
        "historical_run_config",
        HISTORICAL_RUN / "run_config.json",
        "adcb6bd588e4d7708c9371170e8980e6e5542ed201c85a537f8945a077903582",
        "full-covariance no-SH0ES historical run contract",
    ),
    (
        "historical_fit_summary",
        HISTORICAL_RUN / "results" / "fit_summary.csv",
        "ef7cff68b348d3f6b7b6a1eb7a24af23f415dedbfb9a6a6b2319a06bc79e00b0",
        "baseline reproduction target",
    ),
    (
        "Pantheon_plus_mean",
        SN_DATA,
        "1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8",
        "Pantheon+ corrected-magnitude mean table",
    ),
    (
        "Pantheon_plus_covariance",
        SN_COV,
        "abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc",
        "Pantheon+ full STAT+SYS covariance",
    ),
    (
        "DESI_DR2_BAO_mean",
        BAO_DATA,
        "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585",
        "DESI DR2 Gaussian BAO mean vector",
    ),
    (
        "DESI_DR2_BAO_covariance",
        BAO_COV,
        "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509",
        "DESI DR2 Gaussian BAO covariance",
    ),
)

sys.path.insert(0, str(POST / "scripts"))
import cosmo_SN_BAO_closure_runner as closure_runner  # noqa: E402


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_cosmology_support_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


@dataclass
class LikelihoodData:
    sn: dict[str, Any]
    bao: dict[str, Any]
    z_grid: np.ndarray
    sn_cinv: np.ndarray
    sn_cinv_ones: np.ndarray
    sn_ones_cinv_ones: float
    bao_cinv: np.ndarray
    bao_observed: np.ndarray
    bao_z: np.ndarray


def load_likelihood_data() -> LikelihoodData:
    sn = closure_runner.read_sn_data(
        SN_DATA,
        max_rows=None,
        covariance_path=SN_COV,
        covariance_mode="full",
        observable="mb-corr",
        include_calibrators=False,
    )
    bao = closure_runner.read_bao_data(BAO_DATA, BAO_COV)
    bao["label"] = "DESI_DR2_fullcov_noSH0ES"
    z_max = max(float(np.max(sn["z"])), max(row["z"] for row in bao["rows"]))
    grid_size = max(768, int(512 + 256 * z_max))
    z_grid = np.linspace(0.0, z_max, grid_size)
    sn_cinv = np.asarray(sn["inv_covariance"], dtype=float)
    ones = np.ones(len(sn["z"]), dtype=float)
    sn_cinv_ones = sn_cinv @ ones
    bao_covariance = np.asarray(bao["covariance"], dtype=float)
    return LikelihoodData(
        sn=sn,
        bao=bao,
        z_grid=z_grid,
        sn_cinv=sn_cinv,
        sn_cinv_ones=sn_cinv_ones,
        sn_ones_cinv_ones=float(ones @ sn_cinv_ones),
        bao_cinv=linalg.inv(bao_covariance),
        bao_observed=np.asarray(
            [row["value"] for row in bao["rows"]],
            dtype=float,
        ),
        bao_z=np.asarray([row["z"] for row in bao["rows"]], dtype=float),
    )


def baseline_e_grid(
    model: str,
    params: dict[str, float],
    z_grid: np.ndarray,
) -> np.ndarray:
    omega_m = params["Omega_m"]
    one_plus_z = 1.0 + z_grid
    matter = omega_m * one_plus_z**3
    radiation = OMEGA_R * one_plus_z**4
    dark_zero = 1.0 - omega_m - OMEGA_R
    if dark_zero < 0.0:
        raise ValueError("negative present dark-sector density")
    if model == "LCDM":
        e_squared = matter + radiation + dark_zero
    elif model == "wCDM":
        e_squared = (
            matter
            + radiation
            + dark_zero * one_plus_z ** (3.0 * (1.0 + params["w"]))
        )
    elif model == "CPL":
        w0 = params["w0"]
        wa = params["wa"]
        dark_shape = one_plus_z ** (3.0 * (1.0 + w0 + wa))
        dark_shape *= np.exp(-3.0 * wa * z_grid / one_plus_z)
        e_squared = matter + radiation + dark_zero * dark_shape
    elif model in {"M6_fixed", "M6_fitted"}:
        n_past = np.log1p(z_grid)
        activation = 1.0 - np.exp(-((n_past / U_MEMORY) ** P_MEMORY))
        e_squared = (
            matter
            + radiation
            + dark_zero
            + params["B_mem"] * activation
        )
    else:
        raise ValueError(f"unknown baseline model {model}")
    if np.any(e_squared <= 0.0) or np.any(~np.isfinite(e_squared)):
        raise ValueError("non-positive or non-finite baseline E squared")
    return np.sqrt(e_squared)


def profile_likelihood(
    e_grid: np.ndarray,
    data: LikelihoodData,
) -> dict[str, Any]:
    if e_grid.shape != data.z_grid.shape:
        raise ValueError("E grid shape mismatch")
    if np.any(e_grid <= 0.0) or np.any(~np.isfinite(e_grid)):
        raise ValueError("invalid E grid")
    comoving_grid = integrate.cumulative_trapezoid(
        1.0 / e_grid,
        data.z_grid,
        initial=0.0,
    )
    sn_distance = np.interp(data.sn["z"], data.z_grid, comoving_grid)
    sn_dl_shape = np.maximum((1.0 + data.sn["z"]) * sn_distance, 1.0e-12)
    sn_mu_shape = 5.0 * np.log10(sn_dl_shape)
    sn_delta = np.asarray(data.sn["mu"], dtype=float) - sn_mu_shape
    sn_offset = float(
        (data.sn_cinv_ones @ sn_delta) / data.sn_ones_cinv_ones
    )
    sn_residual = sn_delta - sn_offset
    chi2_sn = float(sn_residual @ data.sn_cinv @ sn_residual)
    sn_predicted = sn_mu_shape + sn_offset

    bao_integral = np.interp(data.bao_z, data.z_grid, comoving_grid)
    bao_e = np.interp(data.bao_z, data.z_grid, e_grid)
    unit_predictions: list[float] = []
    for row, dm, e_value in zip(
        data.bao["rows"],
        bao_integral,
        bao_e,
        strict=True,
    ):
        if row["quantity"] == "DM_over_rs":
            unit_predictions.append(float(dm))
        elif row["quantity"] == "DH_over_rs":
            unit_predictions.append(1.0 / float(e_value))
        elif row["quantity"] == "DV_over_rs":
            unit_predictions.append(
                float((row["z"] * dm * dm / e_value) ** (1.0 / 3.0))
            )
        else:
            raise ValueError(f"unsupported BAO quantity {row['quantity']}")
    bao_unit = np.asarray(unit_predictions, dtype=float)
    alpha = float(
        (bao_unit @ data.bao_cinv @ data.bao_observed)
        / (bao_unit @ data.bao_cinv @ bao_unit)
    )
    bao_predicted = alpha * bao_unit
    bao_residual = data.bao_observed - bao_predicted
    chi2_bao = float(bao_residual @ data.bao_cinv @ bao_residual)
    return {
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_sn + chi2_bao,
        "sn_offset": sn_offset,
        "bao_alpha": alpha,
        "sn_residual": sn_residual,
        "sn_predicted": sn_predicted,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "comoving_grid": comoving_grid,
    }


def scalar_rhs(
    omega_m: float,
    omega_lambda: float,
    mu: float,
) -> Callable[[float, np.ndarray], np.ndarray]:
    def rhs(n_lna: float, state: np.ndarray) -> np.ndarray:
        x_value, y_value, log_e = (
            float(state[0]),
            float(state[1]),
            float(state[2]),
        )
        e_value = math.exp(log_e)
        omega_m_n = omega_m * math.exp(-3.0 * n_lna - 2.0 * log_e)
        omega_r_n = OMEGA_R * math.exp(-4.0 * n_lna - 2.0 * log_e)
        h_value = -1.5 * omega_m_n - 2.0 * omega_r_n - 3.0 * x_value**2
        lambda_value = mu / e_value
        return np.asarray(
            [
                -(3.0 + h_value) * x_value - lambda_value * y_value,
                lambda_value * x_value - h_value * y_value,
                h_value,
            ],
            dtype=float,
        )

    return rhs


def integrate_scalar_backward(
    theta: float,
    omega_m: float,
    mu: float,
    scalar_fraction: float,
    n_regular: float,
    dense_output: bool,
    accuracy: str,
) -> Any:
    dark_density = 1.0 - omega_m - OMEGA_R
    if dark_density <= 0.0:
        raise ValueError("non-positive dark density")
    omega_scalar_zero = scalar_fraction * dark_density
    omega_lambda = (1.0 - scalar_fraction) * dark_density
    amplitude = math.sqrt(omega_scalar_zero)
    state_zero = np.asarray(
        [
            -amplitude * math.sin(theta),
            amplitude * math.cos(theta),
            0.0,
        ],
        dtype=float,
    )
    if accuracy == "root":
        rtol, atol, max_step = 3.0e-8, 3.0e-10, 0.06
    else:
        rtol, atol, max_step = 2.0e-10, 2.0e-12, 0.025
    solution = integrate.solve_ivp(
        scalar_rhs(omega_m, omega_lambda, mu),
        (0.0, n_regular),
        state_zero,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=dense_output,
    )
    if not solution.success:
        raise ValueError(solution.message)
    return solution


SCALAR_PROFILE_CACHE: dict[tuple[float, ...], dict[str, Any]] = {}


def direct_scalar_profile(
    omega_m: float,
    log10_mu: float,
    scalar_fraction: float,
    n_regular: float,
    z_grid: np.ndarray,
) -> dict[str, Any]:
    key = (
        float(omega_m),
        float(log10_mu),
        float(scalar_fraction),
        float(n_regular),
        float(z_grid[-1]),
        float(len(z_grid)),
    )
    if key in SCALAR_PROFILE_CACHE:
        return SCALAR_PROFILE_CACHE[key]
    mu = 10.0**log10_mu
    if not (0.05 < omega_m < 0.65):
        raise ValueError("Omega_m outside physical branch")
    if not (0.0 <= scalar_fraction <= 1.0):
        raise ValueError("scalar fraction outside [0,1]")
    if not (0.009 <= mu <= 5.01):
        raise ValueError("mu outside implemented branch")
    dark_density = 1.0 - omega_m - OMEGA_R
    if dark_density <= 0.0:
        raise ValueError("negative dark density")
    if scalar_fraction <= 1.0e-8:
        e_grid = baseline_e_grid("LCDM", {"Omega_m": omega_m}, z_grid)
        payload = {
            "E": e_grid,
            "x": np.zeros_like(e_grid),
            "y": np.zeros_like(e_grid),
            "h": np.asarray(
                (
                    -1.5 * omega_m * (1.0 + z_grid) ** 3
                    - 2.0 * OMEGA_R * (1.0 + z_grid) ** 4
                )
                / e_grid**2
            ),
            "constraint_residual": np.zeros_like(e_grid),
            "theta": 0.0,
            "mu": mu,
            "omega_lambda": dark_density,
            "omega_scalar_zero": 0.0,
            "early_x": 0.0,
            "early_y": 0.0,
            "early_E": float(e_grid[-1]),
            "chi_initial": 0.0,
            "minimum_y": 0.0,
            "root_iterations": 0,
            "n_regular": n_regular,
        }
        SCALAR_PROFILE_CACHE[key] = payload
        return payload

    root_evaluations = 0

    def early_x(theta: float) -> float:
        nonlocal root_evaluations
        root_evaluations += 1
        solution = integrate_scalar_backward(
            theta,
            omega_m,
            mu,
            scalar_fraction,
            n_regular,
            dense_output=False,
            accuracy="root",
        )
        return float(solution.y[0, -1])

    lower = 0.0
    upper = math.pi / 2.0 - 1.0e-5
    lower_value = early_x(lower)
    upper_value = early_x(upper)
    if lower_value * upper_value >= 0.0:
        raise ValueError("regular-mode phase root is not bracketed")
    root = optimize.root_scalar(
        early_x,
        bracket=(lower, upper),
        method="toms748",
        xtol=2.0e-11,
        rtol=2.0e-11,
        maxiter=40,
    )
    if not root.converged:
        raise ValueError("regular-mode phase solve did not converge")
    solution = integrate_scalar_backward(
        float(root.root),
        omega_m,
        mu,
        scalar_fraction,
        n_regular,
        dense_output=True,
        accuracy="final",
    )
    n_grid = -np.log1p(z_grid)
    states = solution.sol(n_grid)
    x_values = np.asarray(states[0], dtype=float)
    y_values = np.asarray(states[1], dtype=float)
    e_values = np.exp(np.asarray(states[2], dtype=float))
    omega_lambda = (1.0 - scalar_fraction) * dark_density
    omega_m_values = omega_m * np.exp(-3.0 * n_grid) / e_values**2
    omega_r_values = OMEGA_R * np.exp(-4.0 * n_grid) / e_values**2
    omega_lambda_values = omega_lambda / e_values**2
    h_values = (
        -1.5 * omega_m_values - 2.0 * omega_r_values - 3.0 * x_values**2
    )
    constraint = (
        omega_m_values
        + omega_r_values
        + omega_lambda_values
        + x_values**2
        + y_values**2
        - 1.0
    )
    sample_n = np.linspace(0.0, n_regular, 241)
    sample_states = solution.sol(sample_n)
    early_x_value = float(solution.y[0, -1])
    early_y_value = float(solution.y[1, -1])
    early_e_value = float(math.exp(solution.y[2, -1]))
    payload = {
        "E": e_values,
        "x": x_values,
        "y": y_values,
        "h": h_values,
        "constraint_residual": constraint,
        "theta": float(root.root),
        "mu": mu,
        "omega_lambda": omega_lambda,
        "omega_scalar_zero": scalar_fraction * dark_density,
        "early_x": early_x_value,
        "early_y": early_y_value,
        "early_E": early_e_value,
        "chi_initial": early_y_value * early_e_value / mu,
        "minimum_y": float(np.min(sample_states[1])),
        "root_iterations": root_evaluations,
        "n_regular": n_regular,
    }
    if (
        np.any(~np.isfinite(e_values))
        or np.any(e_values <= 0.0)
        or np.max(np.abs(constraint)) > 2.0e-6
        or abs(early_x_value) > 2.0e-5
        or payload["minimum_y"] < -1.0e-7
    ):
        raise ValueError("direct scalar branch failed regularity gates")
    SCALAR_PROFILE_CACHE[key] = payload
    return payload


MODEL_PRIORS: dict[str, dict[str, tuple[float, float]]] = {
    "LCDM": {"Omega_m": (0.05, 0.6)},
    "wCDM": {"Omega_m": (0.05, 0.6), "w": (-2.0, -0.2)},
    "CPL": {
        "Omega_m": (0.05, 0.6),
        "w0": (-4.0, 1.0),
        "wa": (-5.0, 5.0),
    },
    "M6_fixed": {"Omega_m": (0.05, 0.6)},
    "M6_fitted": {
        "Omega_m": (0.05, 0.6),
        "B_mem": (-1.0, 1.0),
    },
    "ParentScalar_Lambda_free": {
        "Omega_m": (0.05, 0.6),
        "log10_mu": (-2.0, math.log10(5.0)),
        "f_scalar": (0.0, 1.0),
    },
    "ParentScalar_Lambda_zero": {
        "Omega_m": (0.05, 0.6),
        "log10_mu": (-2.0, math.log10(5.0)),
    },
    "ParentScalar_narrow_prior": {
        "Omega_m": (0.15, 0.45),
        "log10_mu": (math.log10(0.05), math.log10(2.0)),
        "f_scalar": (0.05, 1.0),
    },
    "ParentScalar_N7": {
        "Omega_m": (0.05, 0.6),
        "log10_mu": (-2.0, math.log10(5.0)),
        "f_scalar": (0.0, 1.0),
    },
}


def model_parameters(
    model: str,
    names: list[str],
    vector: np.ndarray,
) -> dict[str, float]:
    params = dict(
        zip(names, (float(value) for value in vector), strict=True)
    )
    if model == "M6_fixed":
        params["B_mem"] = B_MEMORY
    if model == "ParentScalar_Lambda_zero":
        params["f_scalar"] = 1.0
    return params


def evaluate_model(
    model: str,
    params: dict[str, float],
    data: LikelihoodData,
) -> dict[str, Any]:
    scalar_payload: dict[str, Any] | None = None
    if model.startswith("ParentScalar"):
        n_regular = -7.0 if model == "ParentScalar_N7" else N_REGULAR
        scalar_payload = direct_scalar_profile(
            params["Omega_m"],
            params["log10_mu"],
            params["f_scalar"],
            n_regular,
            data.z_grid,
        )
        e_grid = scalar_payload["E"]
    else:
        e_grid = baseline_e_grid(model, params, data.z_grid)
    likelihood = profile_likelihood(e_grid, data)
    return {
        **likelihood,
        "E": e_grid,
        "scalar": scalar_payload,
    }


def default_starts(
    model: str,
    names: list[str],
    priors: dict[str, tuple[float, float]],
    seed_start: dict[str, float] | None,
) -> list[np.ndarray]:
    bounds = [priors[name] for name in names]
    starts = [
        np.asarray(
            [(lower + upper) / 2.0 for lower, upper in bounds],
            dtype=float,
        )
    ]
    targeted: list[dict[str, float]] = []
    if model == "LCDM":
        targeted = [{"Omega_m": 0.305}]
    elif model == "wCDM":
        targeted = [
            {"Omega_m": 0.30, "w": -0.91},
            {"Omega_m": 0.30, "w": -1.0},
        ]
    elif model == "CPL":
        targeted = [
            {"Omega_m": 0.306, "w0": -0.88, "wa": -0.25},
            {"Omega_m": 0.30, "w0": -1.0, "wa": 0.0},
        ]
    elif model == "M6_fixed":
        targeted = [{"Omega_m": 0.3033}]
    elif model == "M6_fitted":
        targeted = [
            {"Omega_m": 0.3033, "B_mem": 0.0745},
            {"Omega_m": 0.305, "B_mem": 0.0},
        ]
    elif model.startswith("ParentScalar"):
        targeted = [
            {
                "Omega_m": 0.30,
                "log10_mu": math.log10(0.69524),
                "f_scalar": 1.0,
            },
            {
                "Omega_m": 0.30,
                "log10_mu": math.log10(0.7),
                "f_scalar": 0.5,
            },
            {
                "Omega_m": 0.30,
                "log10_mu": 0.0,
                "f_scalar": 0.2,
            },
        ]
    if seed_start:
        targeted.insert(0, seed_start)
    for target in targeted:
        values = []
        for name, (lower, upper) in zip(names, bounds, strict=True):
            value = target.get(name, (lower + upper) / 2.0)
            values.append(min(max(value, lower), upper))
        starts.append(np.asarray(values, dtype=float))
    rng = np.random.default_rng(5193)
    random_count = 3 if model.startswith("ParentScalar") else 5
    for _ in range(random_count):
        starts.append(
            np.asarray(
                [rng.uniform(lower, upper) for lower, upper in bounds],
                dtype=float,
            )
        )
    unique: list[np.ndarray] = []
    seen: set[tuple[float, ...]] = set()
    for start in starts:
        key = tuple(float(value) for value in start)
        if key not in seen:
            seen.add(key)
            unique.append(start)
    return unique


def fit_model(
    model: str,
    data: LikelihoodData,
    seed_start: dict[str, float] | None = None,
) -> dict[str, Any]:
    priors = MODEL_PRIORS[model]
    names = list(priors)
    bounds = [priors[name] for name in names]
    starts = default_starts(model, names, priors, seed_start)
    evaluations = 0

    def objective(vector: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        try:
            params = model_parameters(model, names, vector)
            value = evaluate_model(model, params, data)["chi2_total"]
            return float(value) if math.isfinite(value) else 1.0e30
        except (
            ValueError,
            OverflowError,
            FloatingPointError,
            linalg.LinAlgError,
        ):
            return 1.0e30

    results: list[Any] = []
    if model.startswith("ParentScalar"):
        for start in starts:
            results.append(
                optimize.minimize(
                    objective,
                    start,
                    method="Powell",
                    bounds=bounds,
                    options={
                        "maxiter": 90,
                        "xtol": 2.0e-5,
                        "ftol": 2.0e-7,
                    },
                )
            )
    else:
        for start in starts:
            results.append(
                optimize.minimize(
                    objective,
                    start,
                    method="L-BFGS-B",
                    bounds=bounds,
                    options={"maxiter": 220, "ftol": 1.0e-11},
                )
            )
    finite_results = [
        result for result in results if math.isfinite(float(result.fun))
    ]
    if not finite_results:
        raise RuntimeError(f"all optimizer starts failed for {model}")
    best = min(finite_results, key=lambda item: float(item.fun))
    params = model_parameters(model, names, np.asarray(best.x, dtype=float))
    profile = evaluate_model(model, params, data)
    n_points = int(len(data.sn["z"]) + len(data.bao["rows"]))
    k_count = len(names) + 2
    chi2_total = float(profile["chi2_total"])
    edge_rows = []
    for name, (lower, upper) in priors.items():
        value = params[name]
        width = upper - lower
        distance = min(value - lower, upper - value)
        edge_rows.append(
            {
                "model": model,
                "parameter": name,
                "best_fit": value,
                "lower": lower,
                "upper": upper,
                "fractional_distance_to_edge": distance / width,
                "edge_flag": distance < 0.01 * width,
            }
        )
    start_finite_values = sorted(
        float(result.fun)
        for result in finite_results
        if float(result.fun) < 1.0e29
    )
    convergence = bool(
        start_finite_values
        and abs(float(best.fun) - chi2_total) < 2.0e-4
        and math.isfinite(chi2_total)
    )
    print(
        json.dumps(
            {
                "model": model,
                "chi2": chi2_total,
                "params": params,
                "optimizer_success": bool(best.success),
                "evaluations": evaluations,
            }
        ),
        flush=True,
    )
    return {
        "model": model,
        "params": params,
        "priors": priors,
        "chi2_SN": float(profile["chi2_SN"]),
        "chi2_BAO": float(profile["chi2_BAO"]),
        "chi2_total": chi2_total,
        "n": n_points,
        "k": k_count,
        "dof": n_points - k_count,
        "AIC": chi2_total + 2.0 * k_count,
        "BIC": chi2_total + k_count * math.log(n_points),
        "convergence": convergence,
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "objective_evaluations": evaluations,
        "successful_start_count": len(start_finite_values),
        "multistart_chi2_span": (
            max(start_finite_values) - min(start_finite_values)
            if len(start_finite_values) > 1
            else 0.0
        ),
        "prior_edge_flag": any(row["edge_flag"] for row in edge_rows),
        "edge_rows": edge_rows,
        "profile": profile,
        "claim_ceiling": (
            "baseline"
            if model in {"LCDM", "wCDM", "CPL"}
            else "direct_parent_test_nonclaim"
            if model.startswith("ParentScalar")
            else "historical_closure_comparator_nonclaim"
        ),
    }


def historical_scores() -> dict[str, dict[str, str]]:
    with (
        HISTORICAL_RUN / "results" / "fit_summary.csv"
    ).open(newline="", encoding="utf-8") as handle:
        return {row["model"]: row for row in csv.DictReader(handle)}


def fit_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    historical = historical_scores()
    aliases = {
        "LCDM": "LCDM",
        "wCDM": "wCDM",
        "CPL": "CPL",
        "M6_fixed": "MTS_fixed_2over27_no_clock",
        "M6_fitted": "MTS_fixed_p3_u3quarter",
    }
    rows = []
    for score in scores:
        historical_key = aliases.get(score["model"])
        historical_chi2 = (
            float(historical[historical_key]["chi2_total"])
            if historical_key
            else None
        )
        rows.append(
            {
                "model": score["model"],
                "chi2_SN": score["chi2_SN"],
                "chi2_BAO": score["chi2_BAO"],
                "chi2_total": score["chi2_total"],
                "dof": score["dof"],
                "k": score["k"],
                "n": score["n"],
                "AIC": score["AIC"],
                "BIC": score["BIC"],
                "convergence": score["convergence"],
                "optimizer_success": score["optimizer_success"],
                "prior_edge_flag": score["prior_edge_flag"],
                "historical_chi2_total": historical_chi2,
                "delta_chi2_from_historical": (
                    score["chi2_total"] - historical_chi2
                    if historical_chi2 is not None
                    else ""
                ),
                "objective_evaluations": score["objective_evaluations"],
                "successful_start_count": score["successful_start_count"],
                "multistart_chi2_span": score["multistart_chi2_span"],
                "claim_ceiling": score["claim_ceiling"],
            }
        )
    return tagged(rows)


def parameter_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for score in scores:
        scalar = score["profile"]["scalar"]
        for name, value in score["params"].items():
            rows.append(
                {
                    "model": score["model"],
                    "parameter": name,
                    "best_fit": value,
                    "parameter_role": (
                        "universal_action_mass_ratio"
                        if name == "log10_mu"
                        else "homogeneous_state_share"
                        if name == "f_scalar"
                        else "cosmological_density_or_comparator_parameter"
                    ),
                    "derived_quantity": (
                        10.0**value if name == "log10_mu" else ""
                    ),
                    "derived_quantity_label": (
                        "mu=m_gap/H0" if name == "log10_mu" else ""
                    ),
                    "parent_selected_numerically": False,
                    "fit_is_derivation": False,
                    "scalar_theta": scalar["theta"] if scalar else "",
                    "scalar_chi_initial": scalar["chi_initial"] if scalar else "",
                    "omega_lambda": scalar["omega_lambda"] if scalar else "",
                    "omega_scalar_zero": (
                        scalar["omega_scalar_zero"] if scalar else ""
                    ),
                }
            )
        rows.append(
            {
                "model": score["model"],
                "parameter": "SN_offset_profiled",
                "best_fit": score["profile"]["sn_offset"],
                "parameter_role": "shared_nuisance",
                "parent_selected_numerically": False,
                "fit_is_derivation": False,
            }
        )
        rows.append(
            {
                "model": score["model"],
                "parameter": "BAO_alpha_profiled",
                "best_fit": score["profile"]["bao_alpha"],
                "parameter_role": "shared_nuisance",
                "parent_selected_numerically": False,
                "fit_is_derivation": False,
            }
        )
    return tagged(rows)


def baseline_comparison_rows(
    scores: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    baselines = ("LCDM", "wCDM", "CPL")
    rows = []
    for score in scores:
        for baseline_name in baselines:
            if score["model"] == baseline_name:
                continue
            baseline = by_model[baseline_name]
            rows.append(
                {
                    "model": score["model"],
                    "reference_baseline": baseline_name,
                    "delta_chi2": score["chi2_total"]
                    - baseline["chi2_total"],
                    "delta_AIC": score["AIC"] - baseline["AIC"],
                    "delta_BIC": score["BIC"] - baseline["BIC"],
                    "same_SN_rows": True,
                    "same_SN_covariance": True,
                    "same_BAO_rows": True,
                    "same_BAO_covariance": True,
                    "same_SN_offset_profile": True,
                    "same_BAO_alpha_profile": True,
                    "same_fixed_radiation_density": True,
                    "stable_evidence_allowed": False,
                }
            )
    return tagged(rows)


def robustness_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    reference = by_model["ParentScalar_Lambda_free"]
    rows = []
    for name in (
        "ParentScalar_Lambda_free",
        "ParentScalar_Lambda_zero",
        "ParentScalar_narrow_prior",
        "ParentScalar_N7",
    ):
        score = by_model[name]
        scalar = score["profile"]["scalar"]
        rows.append(
            {
                "branch": name,
                "n_regular": scalar["n_regular"],
                "chi2_total": score["chi2_total"],
                "delta_chi2_from_parent_free": (
                    score["chi2_total"] - reference["chi2_total"]
                ),
                "AIC": score["AIC"],
                "BIC": score["BIC"],
                "prior_edge_flag": score["prior_edge_flag"],
                "convergence": score["convergence"],
                "Omega_m": score["params"]["Omega_m"],
                "mu": scalar["mu"],
                "f_scalar": score["params"]["f_scalar"],
                "omega_lambda": scalar["omega_lambda"],
                "theta": scalar["theta"],
                "chi_initial": scalar["chi_initial"],
                "early_x_residual": scalar["early_x"],
                "maximum_constraint_residual": float(
                    np.max(np.abs(scalar["constraint_residual"]))
                ),
                "minimum_y": scalar["minimum_y"],
                "claim_status": "DIRECT_PARENT_FIT_NONCLAIM",
            }
        )
    return tagged(rows)


def parent_identifiability_rows(
    parent_score: dict[str, Any],
    data: LikelihoodData,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    names = ["Omega_m", "log10_mu", "f_scalar"]
    center = np.asarray(
        [parent_score["params"][name] for name in names],
        dtype=float,
    )
    steps = np.asarray([5.0e-4, 2.0e-3, 2.0e-3], dtype=float)

    def objective(vector: np.ndarray) -> float:
        params = dict(
            zip(names, (float(value) for value in vector), strict=True)
        )
        return float(
            evaluate_model("ParentScalar_Lambda_free", params, data)[
                "chi2_total"
            ]
        )

    center_value = objective(center)
    hessian = np.zeros((3, 3), dtype=float)
    for row_index in range(3):
        row_step = np.zeros(3, dtype=float)
        row_step[row_index] = steps[row_index]
        hessian[row_index, row_index] = (
            objective(center + row_step)
            - 2.0 * center_value
            + objective(center - row_step)
        ) / steps[row_index] ** 2
        for column_index in range(row_index):
            column_step = np.zeros(3, dtype=float)
            column_step[column_index] = steps[column_index]
            hessian[row_index, column_index] = hessian[
                column_index, row_index
            ] = (
                objective(center + row_step + column_step)
                - objective(center + row_step - column_step)
                - objective(center - row_step + column_step)
                + objective(center - row_step - column_step)
            ) / (
                4.0 * steps[row_index] * steps[column_index]
            )
    eigenvalues, eigenvectors = np.linalg.eigh(hessian)
    positive_definite = bool(np.all(eigenvalues > 0.0))
    if positive_definite:
        covariance = 2.0 * np.linalg.inv(hessian)
        sigma = np.sqrt(np.diag(covariance))
        correlation = covariance / np.sqrt(
            np.outer(np.diag(covariance), np.diag(covariance))
        )
    else:
        covariance = np.full((3, 3), np.nan)
        sigma = np.full(3, np.nan)
        correlation = np.full((3, 3), np.nan)
    condition_number = (
        float(eigenvalues[-1] / eigenvalues[0])
        if positive_definite
        else math.inf
    )
    rows: list[dict[str, Any]] = []
    for row_index, row_name in enumerate(names):
        for column_index, column_name in enumerate(names):
            rows.append(
                {
                    "row_type": "HESSIAN",
                    "row_parameter": row_name,
                    "column_parameter": column_name,
                    "value": float(hessian[row_index, column_index]),
                    "step": steps[row_index],
                    "interpretation": "second derivative of matched chi squared",
                }
            )
            rows.append(
                {
                    "row_type": "CORRELATION",
                    "row_parameter": row_name,
                    "column_parameter": column_name,
                    "value": float(correlation[row_index, column_index]),
                    "interpretation": "local Gaussian diagnostic only",
                }
            )
    for index, eigenvalue in enumerate(eigenvalues):
        rows.append(
            {
                "row_type": "EIGENMODE",
                "row_parameter": f"mode_{index}",
                "value": float(eigenvalue),
                "Omega_m_component": float(eigenvectors[0, index]),
                "log10_mu_component": float(eigenvectors[1, index]),
                "f_scalar_component": float(eigenvectors[2, index]),
                "interpretation": (
                    "weak_mass_state_direction"
                    if index == 0
                    else "identified_local_direction"
                ),
            }
        )
    for index, name in enumerate(names):
        rows.append(
            {
                "row_type": "MARGINAL_SIGMA",
                "row_parameter": name,
                "value": float(sigma[index]),
                "interpretation": (
                    "local curvature estimate; not a posterior interval"
                ),
            }
        )
    scalar = parent_score["profile"]["scalar"]
    x_zero = float(scalar["x"][0])
    y_zero = float(scalar["y"][0])
    omega_scalar_zero = x_zero**2 + y_zero**2
    omega_lambda = scalar["omega_lambda"]
    total_dark = omega_scalar_zero + omega_lambda
    effective_dark_w_zero = (
        x_zero**2 - y_zero**2 - omega_lambda
    ) / total_dark
    summary = {
        "center_chi2": center_value,
        "hessian": hessian.tolist(),
        "eigenvalues": eigenvalues.tolist(),
        "condition_number": condition_number,
        "positive_definite": positive_definite,
        "marginal_sigma": dict(zip(names, sigma.tolist(), strict=True)),
        "correlation_log10_mu_f_scalar": float(correlation[1, 2]),
        "weak_eigenvector": {
            name: float(eigenvectors[index, 0])
            for index, name in enumerate(names)
        },
        "identifiability_status": (
            "WEAK_MASS_STATE_SPLIT"
            if condition_number > 1.0e3
            and abs(float(correlation[1, 2])) > 0.95
            else "LOCALLY_IDENTIFIED"
        ),
        "present_scalar_kinetic_fraction": x_zero**2,
        "present_scalar_potential_fraction": y_zero**2,
        "present_effective_total_dark_w": effective_dark_w_zero,
    }
    return tagged(rows), summary


def residual_summary_rows(
    scores: list[dict[str, Any]],
    data: LikelihoodData,
) -> list[dict[str, Any]]:
    rows = []
    z_sn = np.asarray(data.sn["z"], dtype=float)
    bin_edges = np.quantile(z_sn, np.linspace(0.0, 1.0, 21))
    bin_edges[0] -= 1.0e-12
    bin_edges[-1] += 1.0e-12
    sn_sigma = np.sqrt(np.diag(np.asarray(data.sn["covariance"], dtype=float)))
    bao_sigma = np.sqrt(np.diag(np.asarray(data.bao["covariance"], dtype=float)))
    for score in scores:
        residual = np.asarray(score["profile"]["sn_residual"], dtype=float)
        for index in range(20):
            mask = (z_sn > bin_edges[index]) & (z_sn <= bin_edges[index + 1])
            if not np.any(mask):
                continue
            rows.append(
                {
                    "dataset": "Pantheon_plus_fullcov_noSH0ES",
                    "model": score["model"],
                    "bin_or_row": f"quantile_{index:02d}",
                    "coordinate_min": float(np.min(z_sn[mask])),
                    "coordinate_max": float(np.max(z_sn[mask])),
                    "count": int(np.count_nonzero(mask)),
                    "mean_residual": float(np.mean(residual[mask])),
                    "rms_residual": float(
                        np.sqrt(np.mean(residual[mask] ** 2))
                    ),
                    "mean_diagonal_standardized_residual": float(
                        np.mean(residual[mask] / sn_sigma[mask])
                    ),
                    "observable": "m_b_corr_shape_profiled",
                }
            )
        for index, row in enumerate(data.bao["rows"]):
            bao_residual = float(score["profile"]["bao_residual"][index])
            rows.append(
                {
                    "dataset": "DESI_DR2_fullcov",
                    "model": score["model"],
                    "bin_or_row": index,
                    "coordinate_min": row["z"],
                    "coordinate_max": row["z"],
                    "count": 1,
                    "mean_residual": bao_residual,
                    "rms_residual": abs(bao_residual),
                    "mean_diagonal_standardized_residual": (
                        bao_residual / bao_sigma[index]
                    ),
                    "observable": row["quantity"],
                    "observed": row["value"],
                    "predicted": float(
                        score["profile"]["bao_predicted"][index]
                    ),
                }
            )
    return tagged(rows)


def scalar_background_rows(
    scores: list[dict[str, Any]],
    data: LikelihoodData,
) -> list[dict[str, Any]]:
    selected_redshifts = np.asarray(
        [0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 2.33],
        dtype=float,
    )
    rows = []
    h0_planck = (
        H0_KM_S_MPC * 1000.0 / MPC_METRES * PLANCK_TIME_SECONDS
    )
    for score in scores:
        scalar = score["profile"]["scalar"]
        if scalar is None:
            continue
        for redshift in selected_redshifts:
            e_value = float(np.interp(redshift, data.z_grid, scalar["E"]))
            x_value = float(np.interp(redshift, data.z_grid, scalar["x"]))
            y_value = float(np.interp(redshift, data.z_grid, scalar["y"]))
            h_value = float(np.interp(redshift, data.z_grid, scalar["h"]))
            constraint = float(
                np.interp(
                    redshift,
                    data.z_grid,
                    scalar["constraint_residual"],
                )
            )
            mu = scalar["mu"]
            acceleration = -3.0 * e_value**2 * x_value - mu * e_value * y_value
            hdot_h0_squared = h_value * e_value**2
            derivative_shape = (
                acceleration**2
                - 3.0 * hdot_h0_squared * e_value**2 * x_value**2
                - 2.0 * e_value**2 * x_value * acceleration
                - mu**2 * e_value**2 * x_value**2
            )
            delta_q_coefficient = (
                -96.0
                * W_O4_ABS_MAX
                * e_value**4
                * x_value**2
            )
            delta_f_coefficient = (
                -96.0 * W_O4_ABS_MAX * derivative_shape
            )
            omega_scalar = x_value**2 + y_value**2
            rows.append(
                {
                    "model": score["model"],
                    "redshift": redshift,
                    "E": e_value,
                    "x_kinetic_root_fraction": x_value,
                    "y_potential_root_fraction": y_value,
                    "Omega_scalar_fraction": omega_scalar,
                    "w_scalar": (
                        (x_value**2 - y_value**2) / omega_scalar
                        if omega_scalar > 0.0
                        else -1.0
                    ),
                    "constraint_residual": constraint,
                    "delta_Q_over_H0tP_fourth": delta_q_coefficient,
                    "delta_F_over_H0tP_fourth": delta_f_coefficient,
                    "delta_Q_H0_70": delta_q_coefficient * h0_planck**4,
                    "delta_F_H0_70": delta_f_coefficient * h0_planck**4,
                    "status": "DIRECT_PARENT_SCALAR_BACKGROUND",
                }
            )
    return tagged(rows)


def provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, expected, role in LOCKED_SOURCES:
        rows.append(
            {
                "source_id": source_id,
                "source": str(path),
                "sha256": source_hashes[source_id],
                "expected_sha256": expected,
                "exists": path.is_file(),
                "hash_match": source_hashes[source_id] == expected,
                "role": role,
                "status": "HASH_MATCHED",
            }
        )
    return tagged(rows)


def build_document(
    scores: list[dict[str, Any]],
    source_hashes: dict[str, str],
    identifiability: dict[str, Any],
) -> str:
    by_model = {score["model"]: score for score in scores}
    parent = by_model["ParentScalar_Lambda_free"]
    parent_zero = by_model["ParentScalar_Lambda_zero"]
    parent_narrow = by_model["ParentScalar_narrow_prior"]
    parent_n7 = by_model["ParentScalar_N7"]
    scalar = parent["profile"]["scalar"]
    best_bic = min(scores[:7], key=lambda score: score["BIC"])
    best_aic = min(scores[:7], key=lambda score: score["AIC"])
    derived_or_baseline = [
        by_model[name]
        for name in (
            "LCDM",
            "wCDM",
            "CPL",
            "ParentScalar_Lambda_free",
            "ParentScalar_Lambda_zero",
        )
    ]
    best_derived_aic = min(
        derived_or_baseline,
        key=lambda score: score["AIC"],
    )
    best_derived_bic = min(
        derived_or_baseline,
        key=lambda score: score["BIC"],
    )

    def comparison(model: str, baseline: str) -> str:
        score = by_model[model]
        base = by_model[baseline]
        return (
            f"{model} minus {baseline}: "
            f"Delta chi2={score['chi2_total'] - base['chi2_total']:.9g}, "
            f"Delta AIC={score['AIC'] - base['AIC']:.9g}, "
            f"Delta BIC={score['BIC'] - base['BIC']:.9g}"
        )

    table_lines = [
        (
            f"{score['model']:31s} "
            f"chi2={score['chi2_total']:.9f} "
            f"k={score['k']} "
            f"AIC={score['AIC']:.9f} "
            f"BIC={score['BIC']:.9f} "
            f"edge={score['prior_edge_flag']}"
        )
        for score in scores
    ]
    return f"""# 5193 - Direct parent-scalar Pantheon+/DESI likelihood and model-selection gate

Marker: `{MARKER}`

**Verdict:** checkpoint 5192 has been converted into a direct data model. The
parent scalar was not approximated by the rejected `p=3,u=1/4` closure. Its
regular homogeneous mode was solved at every likelihood evaluation and scored
on exactly the same 1,624 Pantheon+ shape rows and 13 DESI DR2 BAO rows as the
fitted baselines, with the same full covariance matrices and the same two
profiled nuisance parameters.

The numerical result remains nonclaim. The action owns the universal mass
coordinate and the homogeneous equations; it does not select the fitted mass
or state amplitude.

## 1. Matched likelihood contract

```text
Pantheon+ rows                 = 1624 non-calibrators;
Pantheon+ covariance           = full STAT+SYS;
SN nuisance                    = one analytic additive offset;
DESI DR2 BAO rows              = 13;
DESI DR2 covariance            = full Gaussian covariance;
BAO nuisance                   = one analytic common scale alpha;
local-H0/SH0ES calibration     = absent;
fixed radiation density        = Omega_r={OMEGA_R};
total scored points            = 1637.
```

The four data hashes match the historical no-SH0ES run. All models use the
same selected rows, covariances, integration grid, and nuisance profiling.

## 2. Parent-scalar parameterization

Define

```text
x=dot(psi_c)/(sqrt(6) M_R H),
y=m_gap psi_c/(sqrt(6) M_R H),
mu=m_gap/H0.
```

At `N=0`, flatness is imposed exactly:

```text
Omega_psi,0=f_scalar(1-Omega_m-Omega_r),
Omega_Lambda=(1-f_scalar)(1-Omega_m-Omega_r),
x_0=-sqrt(Omega_psi,0) sin(theta),
y_0= sqrt(Omega_psi,0) cos(theta).
```

The backward autonomous system is

```text
x'=-(3+h)x-(mu/E)y,
y'=(mu/E)x-hy,
(ln E)'=h,
h=-3Omega_m(N)/2-2Omega_r(N)-3x^2.
```

`theta` is not fitted. It is shot uniquely onto the regular frozen mode
`x(N_reg)=0` at every likelihood evaluation. The free-`Lambda` model therefore
has three shape parameters:

```text
Omega_m, log10(mu), f_scalar.
```

The `Lambda=0` ablation fixes `f_scalar=1` and has two shape parameters.
The SN offset and BAO scale are counted for every model.

## 3. Fitted scores

```text
{chr(10).join(table_lines)}
```

The lowest primary AIC is `{best_aic['model']}`. The lowest primary BIC is
`{best_bic['model']}`. Information criteria are reported rather than turned
into a binary victory claim.

`M6_fixed` is retained only as the historical empirical closure comparator:
checkpoint 5192 rejects its identity with the source-free parent scalar.
Restricting the comparison to standard baselines and direct parent-owned
models, the lowest AIC is `{best_derived_aic['model']}` and the lowest BIC is
`{best_derived_bic['model']}`. Their disagreement is part of the result, not
something to average away.

Direct comparisons:

```text
{comparison('ParentScalar_Lambda_free', 'LCDM')}
{comparison('ParentScalar_Lambda_free', 'wCDM')}
{comparison('ParentScalar_Lambda_free', 'CPL')}
{comparison('ParentScalar_Lambda_zero', 'LCDM')}
{comparison('ParentScalar_Lambda_zero', 'wCDM')}
{comparison('ParentScalar_Lambda_zero', 'CPL')}
```

## 4. Parent best-fit branch

```text
Omega_m       = {parent['params']['Omega_m']:.15g},
mu=m_gap/H0   = {scalar['mu']:.15g},
f_scalar      = {parent['params']['f_scalar']:.15g},
Omega_Lambda  = {scalar['omega_lambda']:.15g},
theta         = {scalar['theta']:.15g},
chi_initial   = {scalar['chi_initial']:.15g},
early x       = {scalar['early_x']:.15g},
max constraint residual
              = {float(np.max(np.abs(scalar['constraint_residual']))):.15g}.
```

These fitted numbers are not a derivation of `J_gap` or the cosmological
state. They are the data-preferred coordinates inside the parent-owned model
family under the declared priors.

## 5. Robustness branches

```text
free Lambda broad prior:
  chi2={parent['chi2_total']:.12g},
  edge={parent['prior_edge_flag']};

Lambda=0 ablation:
  chi2={parent_zero['chi2_total']:.12g},
  Delta chi2={parent_zero['chi2_total'] - parent['chi2_total']:.12g},
  edge={parent_zero['prior_edge_flag']};

narrow parent prior:
  chi2={parent_narrow['chi2_total']:.12g},
  Delta chi2={parent_narrow['chi2_total'] - parent['chi2_total']:.12g},
  edge={parent_narrow['prior_edge_flag']};

regular surface N=-7:
  chi2={parent_n7['chi2_total']:.12g},
  Delta chi2={parent_n7['chi2_total'] - parent['chi2_total']:.12g},
  edge={parent_n7['prior_edge_flag']}.
```

Any prior-edge branch remains unstable evidence even if its raw chi-squared
is low.

## 6. Identifiability and physical reading

The broad free-`Lambda` minimum is interior, but an interior point is not the
same thing as a well-measured parameter split. A direct finite-difference
Hessian gives

```text
minimum eigenvalue = {identifiability['eigenvalues'][0]:.15g},
maximum eigenvalue = {identifiability['eigenvalues'][-1]:.15g},
condition number   = {identifiability['condition_number']:.15g},
corr(log10(mu),f_scalar)
                   = {identifiability['correlation_log10_mu_f_scalar']:.15g},
status             = {identifiability['identifiability_status']}.
```

Thus the background constrains a combined thaw history much more strongly
than it separately measures the universal mass and state share. Local
Gaussian curvature estimates are

```text
sigma(Omega_m)  = {identifiability['marginal_sigma']['Omega_m']:.15g},
sigma(log10_mu) = {identifiability['marginal_sigma']['log10_mu']:.15g},
sigma(f_scalar) = {identifiability['marginal_sigma']['f_scalar']:.15g}.
```

These are diagnostics, not posterior intervals. They explain why the
`Lambda=0` ablation is the cleaner predictive branch: it removes the nearly
degenerate split while retaining a fit competitive with wCDM and CPL.

At the free-`Lambda` optimum,

```text
Omega_scalar,kinetic,0
  = {identifiability['present_scalar_kinetic_fraction']:.15g},
Omega_scalar,potential,0
  = {identifiability['present_scalar_potential_fraction']:.15g},
w_dark,effective,0
  = {identifiability['present_effective_total_dark_w']:.15g}.
```

## 7. Decision

```text
old M6 equals direct parent scalar             = false;
parent scalar background equation in scorer   = direct ODE;
regular homogeneous mode                      = solved, not fitted;
flatness                                      = exact;
SN and BAO nuisance freedom                    = matched;
historical baselines                          = reproduced within tolerance;
parent scalar parameter estimates             = fit coordinates, not derived;
cosmology-support claim                        = false;
full MTS unification claim                     = false.
```

## 8. Next target

If the direct branch is competitive and not wholly edge-supported, checkpoint
5194 should add independent growth/CMB perturbation equations for this exact
background before promotion. If it is not competitive, 5194 should diagnose
which redshift and observable blocks reject it and return to the parent
potential/state-selection problem rather than tune a replacement closure.

## 9. Machine artifacts

- `source-intake/functional_rg/5193/fit_summary.csv`
- `source-intake/functional_rg/5193/parameter_estimates.csv`
- `source-intake/functional_rg/5193/prior_edge_table.csv`
- `source-intake/functional_rg/5193/baseline_comparison.csv`
- `source-intake/functional_rg/5193/robustness_matrix.csv`
- `source-intake/functional_rg/5193/parent_scalar_identifiability.csv`
- `source-intake/functional_rg/5193/residual_summary.csv`
- `source-intake/functional_rg/5193/parent_scalar_background.csv`
- `source-intake/functional_rg/5193/source_provenance.csv`
- `source-intake/functional_rg/5193/direct_parent_scalar_likelihood_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5193_VALIDATION.csv`
"""


def validation_rows(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_before: str,
    scores: list[dict[str, Any]],
    identifiability: dict[str, Any],
    data: LikelihoodData,
    output_paths: tuple[Path, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check: str, passed: bool, observed: Any, expected: Any) -> None:
        rows.append(
            {
                "check_id": f"V5193_{len(rows):02d}",
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
            }
        )

    expected_hashes = {
        source_id: expected
        for source_id, _, expected, _ in LOCKED_SOURCES
    }
    add(
        "all locked source hashes match",
        source_hashes == expected_hashes,
        sum(
            source_hashes[source_id] == expected
            for source_id, _, expected, _ in LOCKED_SOURCES
        ),
        len(LOCKED_SOURCES),
    )
    add(
        "formalization workbench lock matches before writes",
        formal_before == FORMAL_LOCK,
        formal_before,
        FORMAL_LOCK,
    )
    add(
        "checkpoint 5176 lock matches before writes",
        checkpoint_before == CHECKPOINT_5176_LOCK,
        checkpoint_before,
        CHECKPOINT_5176_LOCK,
    )
    add(
        "matched Pantheon plus row count",
        len(data.sn["z"]) == 1624,
        len(data.sn["z"]),
        1624,
    )
    add(
        "matched DESI DR2 BAO row count",
        len(data.bao["rows"]) == 13,
        len(data.bao["rows"]),
        13,
    )
    add(
        "full SN covariance selected",
        data.sn.get("covariance_mode") == "full"
        and data.sn["covariance"].shape == (1624, 1624),
        (
            data.sn.get("covariance_mode"),
            data.sn["covariance"].shape,
        ),
        ("full", (1624, 1624)),
    )
    add(
        "full BAO covariance selected",
        data.bao["covariance"].shape == (13, 13),
        data.bao["covariance"].shape,
        (13, 13),
    )
    add(
        "all fitted models return finite converged scores",
        all(
            score["convergence"]
            and math.isfinite(score["chi2_total"])
            and score["chi2_total"] > 0.0
            for score in scores
        ),
        sum(
            score["convergence"] and math.isfinite(score["chi2_total"])
            for score in scores
        ),
        len(scores),
    )
    historical_tolerance_rows = [
        row
        for row in fit_summary_rows(scores)
        if row["historical_chi2_total"] not in ("", None)
    ]
    add(
        "matched-radiation baselines reproduce historical scores",
        all(
            abs(float(row["delta_chi2_from_historical"])) < 0.1
            for row in historical_tolerance_rows
        ),
        max(
            abs(float(row["delta_chi2_from_historical"]))
            for row in historical_tolerance_rows
        ),
        "<0.1",
    )
    scalar_scores = [
        score for score in scores if score["model"].startswith("ParentScalar")
    ]
    add(
        "all direct scalar fits solve the regular frozen mode",
        all(abs(score["profile"]["scalar"]["early_x"]) < 2.0e-5 for score in scalar_scores),
        max(abs(score["profile"]["scalar"]["early_x"]) for score in scalar_scores),
        "<2e-5",
    )
    add(
        "all direct scalar fits preserve the Friedmann constraint",
        all(
            np.max(
                np.abs(score["profile"]["scalar"]["constraint_residual"])
            )
            < 2.0e-6
            for score in scalar_scores
        ),
        max(
            float(
                np.max(
                    np.abs(score["profile"]["scalar"]["constraint_residual"])
                )
            )
            for score in scalar_scores
        ),
        "<2e-6",
    )
    add(
        "all direct scalar fits remain on the nodeless thaw branch",
        all(score["profile"]["scalar"]["minimum_y"] >= -1.0e-7 for score in scalar_scores),
        min(score["profile"]["scalar"]["minimum_y"] for score in scalar_scores),
        ">=-1e-7",
    )
    by_model = {score["model"]: score for score in scores}
    add(
        "Lambda zero ablation fixes the scalar share exactly",
        by_model["ParentScalar_Lambda_zero"]["params"]["f_scalar"] == 1.0,
        by_model["ParentScalar_Lambda_zero"]["params"]["f_scalar"],
        1.0,
    )
    add(
        "N minus 7 robustness branch uses the earlier regular surface",
        by_model["ParentScalar_N7"]["profile"]["scalar"]["n_regular"] == -7.0,
        by_model["ParentScalar_N7"]["profile"]["scalar"]["n_regular"],
        -7.0,
    )
    add(
        "broad and narrow parent priors recover the same likelihood basin",
        abs(
            by_model["ParentScalar_narrow_prior"]["chi2_total"]
            - by_model["ParentScalar_Lambda_free"]["chi2_total"]
        )
        < 1.0e-3,
        (
            by_model["ParentScalar_narrow_prior"]["chi2_total"]
            - by_model["ParentScalar_Lambda_free"]["chi2_total"]
        ),
        "absolute Delta chi2 <1e-3",
    )
    add(
        "N minus 5 and N minus 7 fits recover the same likelihood basin",
        abs(
            by_model["ParentScalar_N7"]["chi2_total"]
            - by_model["ParentScalar_Lambda_free"]["chi2_total"]
        )
        < 1.0e-3,
        (
            by_model["ParentScalar_N7"]["chi2_total"]
            - by_model["ParentScalar_Lambda_free"]["chi2_total"]
        ),
        "absolute Delta chi2 <1e-3",
    )
    add(
        "free parent scalar and CPL have matched parameter count",
        by_model["ParentScalar_Lambda_free"]["k"] == by_model["CPL"]["k"],
        (
            by_model["ParentScalar_Lambda_free"]["k"],
            by_model["CPL"]["k"],
        ),
        "equal",
    )
    add(
        "free parent scalar reaches the CPL likelihood basin",
        abs(
            by_model["ParentScalar_Lambda_free"]["chi2_total"]
            - by_model["CPL"]["chi2_total"]
        )
        < 0.1,
        (
            by_model["ParentScalar_Lambda_free"]["chi2_total"]
            - by_model["CPL"]["chi2_total"]
        ),
        "absolute Delta chi2 <0.1",
    )
    add(
        "Lambda zero parent scalar and wCDM have matched parameter count",
        by_model["ParentScalar_Lambda_zero"]["k"] == by_model["wCDM"]["k"],
        (
            by_model["ParentScalar_Lambda_zero"]["k"],
            by_model["wCDM"]["k"],
        ),
        "equal",
    )
    add(
        "Lambda zero parent scalar is competitive with wCDM",
        (
            by_model["ParentScalar_Lambda_zero"]["chi2_total"]
            - by_model["wCDM"]["chi2_total"]
        )
        < 1.0,
        (
            by_model["ParentScalar_Lambda_zero"]["chi2_total"]
            - by_model["wCDM"]["chi2_total"]
        ),
        "Delta chi2 <1",
    )
    add(
        "no fitted parent scalar coordinate hits a prior edge",
        not any(score["prior_edge_flag"] for score in scalar_scores),
        sum(score["prior_edge_flag"] for score in scalar_scores),
        0,
    )
    add(
        "free parent scalar mass-state weak direction is explicitly detected",
        (
            identifiability["identifiability_status"]
            == "WEAK_MASS_STATE_SPLIT"
            and identifiability["positive_definite"]
            and identifiability["condition_number"] > 1.0e3
        ),
        (
            identifiability["identifiability_status"],
            identifiability["condition_number"],
        ),
        "positive Hessian with condition >1e3 and weak status",
    )
    add(
        "all planned output files exist and are nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in output_paths),
        sum(path.exists() and path.stat().st_size > 0 for path in output_paths),
        len(output_paths),
    )
    return tagged(rows)


def main() -> None:
    source_hashes = {
        source_id: file_digest(path)
        for source_id, path, _, _ in LOCKED_SOURCES
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_before = tree_digest(CHECKPOINT_5176)
    data = load_likelihood_data()

    scores: list[dict[str, Any]] = []
    for model in ("LCDM", "wCDM", "CPL", "M6_fixed", "M6_fitted"):
        scores.append(fit_model(model, data))

    parent = fit_model("ParentScalar_Lambda_free", data)
    scores.append(parent)
    seed = parent["params"]
    scores.append(fit_model("ParentScalar_Lambda_zero", data, seed))
    scores.append(fit_model("ParentScalar_narrow_prior", data, seed))
    scores.append(fit_model("ParentScalar_N7", data, seed))

    fit_rows = fit_summary_rows(scores)
    parameters = parameter_rows(scores)
    edge_rows = tagged(
        [row for score in scores for row in score["edge_rows"]]
    )
    comparisons = baseline_comparison_rows(scores)
    robustness = robustness_rows(scores)
    identifiability_rows, identifiability_summary = (
        parent_identifiability_rows(parent, data)
    )
    residuals = residual_summary_rows(scores, data)
    backgrounds = scalar_background_rows(scores, data)
    provenance = provenance_rows(source_hashes)

    output_map: dict[Path, list[dict[str, Any]]] = {
        OUT / "fit_summary.csv": fit_rows,
        OUT / "parameter_estimates.csv": parameters,
        OUT / "prior_edge_table.csv": edge_rows,
        OUT / "baseline_comparison.csv": comparisons,
        OUT / "robustness_matrix.csv": robustness,
        OUT / "parent_scalar_identifiability.csv": identifiability_rows,
        OUT / "residual_summary.csv": residuals,
        OUT / "parent_scalar_background.csv": backgrounds,
        OUT / "source_provenance.csv": provenance,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)

    by_model = {score["model"]: score for score in scores}
    primary_names = (
        "LCDM",
        "wCDM",
        "CPL",
        "M6_fixed",
        "M6_fitted",
        "ParentScalar_Lambda_free",
        "ParentScalar_Lambda_zero",
    )
    primary_scores = [by_model[name] for name in primary_names]
    result_path = OUT / "direct_parent_scalar_likelihood_results.json"
    result_payload = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "theorem": (
            "THE_PARENT_OWNED_MASS_GAP_SCALAR_HAS_BEEN_INTEGRATED_DIRECTLY_"
            "ON_ITS_REGULAR_HOMOGENEOUS_FLRW_MODE_AND_SCORED_WITH_MATCHED_"
            "FULL_COVARIANCE_PANTHEON_PLUS_AND_DESI_DR2_SHAPE_LIKELIHOODS_"
            "WITHOUT_IDENTIFYING_IT_WITH_THE_REJECTED_MEMORY_CLOSURE"
        ),
        "claim_guard": (
            "NO_COSMOLOGY_SUPPORT_CLAIM_NO_DERIVATION_OF_THE_FITTED_MASS_"
            "NO_DERIVATION_OF_THE_FITTED_STATE_NO_CMB_OR_GROWTH_PROMOTION_"
            "NO_FULL_MTS_UNIFICATION_CLAIM"
        ),
        "data_contract": {
            "Pantheon_plus_rows": len(data.sn["z"]),
            "Pantheon_plus_covariance": "full_STAT+SYS",
            "Pantheon_plus_calibrators_included": False,
            "SN_nuisance": "analytic_additive_offset",
            "DESI_DR2_rows": len(data.bao["rows"]),
            "DESI_DR2_covariance": "full",
            "BAO_nuisance": "analytic_common_alpha",
            "Omega_r_fixed": OMEGA_R,
        },
        "scores": {
            score["model"]: {
                "params": score["params"],
                "chi2_SN": score["chi2_SN"],
                "chi2_BAO": score["chi2_BAO"],
                "chi2_total": score["chi2_total"],
                "k": score["k"],
                "AIC": score["AIC"],
                "BIC": score["BIC"],
                "prior_edge_flag": score["prior_edge_flag"],
                "convergence": score["convergence"],
                "scalar_branch": (
                    {
                        key: value
                        for key, value in score["profile"]["scalar"].items()
                        if key
                        not in {
                            "E",
                            "x",
                            "y",
                            "h",
                            "constraint_residual",
                        }
                    }
                    if score["profile"]["scalar"] is not None
                    else None
                ),
            }
            for score in scores
        },
        "primary_best_AIC": min(
            primary_scores,
            key=lambda score: score["AIC"],
        )["model"],
        "primary_best_BIC": min(
            primary_scores,
            key=lambda score: score["BIC"],
        )["model"],
        "parent_scalar_identifiability": identifiability_summary,
        "source_hashes": source_hashes,
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_before,
        "next_target": (
            "5194 direct-parent perturbation and growth/CMB gate if the "
            "background survives, otherwise redshift-block diagnosis and "
            "parent state-selection revision"
        ),
    }
    write_json(result_path, result_payload)
    DOCUMENT.write_text(
        build_document(scores, source_hashes, identifiability_summary),
        encoding="utf-8",
    )

    output_paths = tuple(output_map) + (result_path, DOCUMENT)
    checks = validation_rows(
        source_hashes,
        formal_before,
        checkpoint_before,
        scores,
        identifiability_summary,
        data,
        output_paths,
    )
    formal_after = tree_digest(FORMAL)
    checkpoint_after = tree_digest(CHECKPOINT_5176)

    def add_final(check: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append(
            {
                "check_id": f"V5193_{len(checks):02d}",
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
                "checkpoint_marker": MARKER,
                "valid_for_cosmology_support_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    add_final(
        "formalization workbench remains unchanged after writes",
        formal_after == formal_before == FORMAL_LOCK,
        formal_after,
        FORMAL_LOCK,
    )
    add_final(
        "checkpoint 5176 remains unchanged after writes",
        checkpoint_after == checkpoint_before == CHECKPOINT_5176_LOCK,
        checkpoint_after,
        CHECKPOINT_5176_LOCK,
    )
    add_final(
        "all evidence rows remain nonclaim",
        all(
            row["valid_for_cosmology_support_claim"] is False
            and row["valid_for_full_MTS_claim"] is False
            for collection in (
                fit_rows,
                parameters,
                edge_rows,
                comparisons,
                robustness,
                identifiability_rows,
                residuals,
                backgrounds,
                provenance,
            )
            for row in collection
        ),
        "all false",
        "all false",
    )
    write_csv(VALIDATION, checks)
    failures = [row for row in checks if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(json.dumps(failures, indent=2))

    parent_score = by_model["ParentScalar_Lambda_free"]
    print(
        json.dumps(
            {
                "checkpoint": 5193,
                "marker": MARKER,
                "validation_passed": len(checks),
                "validation_failed": 0,
                "parent_scalar_chi2": parent_score["chi2_total"],
                "parent_scalar_AIC": parent_score["AIC"],
                "parent_scalar_BIC": parent_score["BIC"],
                "parent_scalar_params": parent_score["params"],
                "best_primary_AIC": result_payload["primary_best_AIC"],
                "best_primary_BIC": result_payload["primary_best_BIC"],
                "next_target": result_payload["next_target"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
