from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import camb
import numpy as np
from scipy import integrate, linalg, optimize


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5195"
DOCUMENT = (
    POST
    / "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-"
    "physical-sound-horizon-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5195_VALIDATION.csv"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)

MARKER = "MTS_5195_MATCHED_JOINT_CMB_INFORMED_PARENT_REFIT"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"

DOCUMENT_5193 = (
    POST
    / "5193-Y5-R2FR-direct-parent-scalar-Pantheon-DESI-likelihood-and-"
    "model-selection-gate.md"
)
SCRIPT_5193 = (
    POST / "scripts" / "Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood.py"
)
RESULT_5193 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5193"
    / "direct_parent_scalar_likelihood_results.json"
)
VALIDATION_5193 = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5193_VALIDATION.csv"
)
DOCUMENT_5194 = (
    POST
    / "5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-"
    "compressed-CMB-gate.md"
)
SCRIPT_5194 = (
    POST
    / "scripts"
    / "Y5_R2FR_5194_parent_scalar_perturbation_growth_CMB_gate.py"
)
RESULT_5194 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5194"
    / "parent_scalar_perturbation_growth_CMB_results.json"
)
VALIDATION_5194 = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5194_VALIDATION.csv"
)

LOCKED_PREDECESSORS: tuple[tuple[str, Path, str], ...] = (
    (
        "checkpoint_5193_document",
        DOCUMENT_5193,
        "277a74bf5d75238831d87a5c778a7ac8da2c226d2eafb5ec30203b6fda067dd9",
    ),
    (
        "checkpoint_5193_script",
        SCRIPT_5193,
        "8ae6018f911667c04b2780ff5247786e3c192f58397148b6ba07cebccc0ddb21",
    ),
    (
        "checkpoint_5193_result",
        RESULT_5193,
        "3fc4dbf416cd1b4ce5b5a921d4dd792abb98bd9d3897ba18d570688e7c4e1a6d",
    ),
    (
        "checkpoint_5193_validation",
        VALIDATION_5193,
        "26de30e6eca3123fe45731622e50ee7cfc8e20b3ef4a3c60cf6783f1975d8f87",
    ),
    (
        "checkpoint_5194_document",
        DOCUMENT_5194,
        "1478db5333863753c00371b2e8c5ad8d7dc5250a40dd3a1f870de4e8ad25eb5d",
    ),
    (
        "checkpoint_5194_script",
        SCRIPT_5194,
        "f696e14285549efa7435a3e02b01becb73833998adbd37a60ad49fa779db6bb8",
    ),
    (
        "checkpoint_5194_result",
        RESULT_5194,
        "c77810bd81115c174514b21df7f08ba4e947ba2d56fcbed4602c805536df71f9",
    ),
    (
        "checkpoint_5194_validation",
        VALIDATION_5194,
        "675e753e270bc85cf1eb032d71c1924969f39b75696fd07617e7199ec95ff5c0",
    ),
)

sys.path.insert(0, str(POST / "scripts"))
import Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood as checkpoint_5193
import Y5_R2FR_5194_parent_scalar_perturbation_growth_CMB_gate as checkpoint_5194


MODEL_ORDER = (
    "LCDM",
    "wCDM",
    "CPL",
    "ParentScalar_Lambda_free",
    "ParentScalar_Lambda_zero",
)
PARENT_MODELS = (
    "ParentScalar_Lambda_free",
    "ParentScalar_Lambda_zero",
)
MODEL_SHAPE_PRIORS: dict[str, dict[str, tuple[float, float]]] = {
    "LCDM": {"Omega_m": (0.15, 0.45)},
    "wCDM": {
        "Omega_m": (0.15, 0.45),
        "w": (-2.0, -0.2),
    },
    "CPL": {
        "Omega_m": (0.15, 0.45),
        "w0": (-3.0, 0.0),
        "wa": (-4.0, 4.0),
    },
    "ParentScalar_Lambda_free": {
        "Omega_m": (0.15, 0.45),
        "log10_mu": (-2.0, math.log10(5.0)),
        "f_scalar": (0.0, 1.0),
    },
    "ParentScalar_Lambda_zero": {
        "Omega_m": (0.15, 0.45),
        "log10_mu": (-2.0, math.log10(5.0)),
    },
}
H0_BOUNDS = (50.0, 90.0)
OMBH2_BOUNDS = (0.0200, 0.0250)
NS_BOUNDS = (0.8, 1.2)
SIGMA8_BOUNDS = (0.4, 1.2)
N_REGULAR_FIT = -7.0
N_BACKGROUND_FORWARD = -12.0
N_GRID_FIT = np.linspace(N_REGULAR_FIT, 0.0, 1401)
C_KM_S = checkpoint_5194.C_KM_S
MNU_EV = checkpoint_5194.MNU_EV
OMEGANU_H2 = checkpoint_5194.NEUTRINO_PHYSICAL_DENSITY_APPROX
CAMB_W_FLOOR = checkpoint_5194.CAMB_W_FLOOR
MPC_METRES = 3.0856775814913673e22
HBAR_EV_SECONDS = 6.582119569e-16


@dataclass
class PlanckPrior:
    model: str
    order: list[str]
    mean: np.ndarray
    covariance: np.ndarray
    inverse: np.ndarray


@dataclass
class JointData:
    late: checkpoint_5193.LikelihoodData
    growth_blocks: list[checkpoint_5194.DataBlock]
    planck_priors: dict[str, PlanckPrior]


@dataclass(frozen=True)
class FitConfig:
    name: str
    growth_mode: str
    planck_prior_model: str
    sdss_distance_overlap: bool
    wide_parent_mass: bool = False


PRIMARY_CONFIG = FitConfig(
    name="primary_fs8_wCDM_prior",
    growth_mode="fs8_only",
    planck_prior_model="wCDM",
    sdss_distance_overlap=False,
)
FULL_SDSS_CONFIG = FitConfig(
    name="robustness_full_SDSS_wCDM_prior",
    growth_mode="all",
    planck_prior_model="wCDM",
    sdss_distance_overlap=True,
)
LCDM_PRIOR_CONFIG = FitConfig(
    name="robustness_fs8_LCDM_prior",
    growth_mode="fs8_only",
    planck_prior_model="LCDM",
    sdss_distance_overlap=False,
)
NO_GROWTH_CONFIG = FitConfig(
    name="robustness_no_growth_wCDM_prior",
    growth_mode="none",
    planck_prior_model="wCDM",
    sdss_distance_overlap=False,
)
WIDE_PARENT_CONFIG = FitConfig(
    name="robustness_parent_wide_mass",
    growth_mode="fs8_only",
    planck_prior_model="wCDM",
    sdss_distance_overlap=False,
    wide_parent_mass=True,
)


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
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
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


def load_planck_prior(model: str) -> PlanckPrior:
    order = ["R", "l_A", "Omega_b_h2", "n_s"]
    vector_rows = [
        row
        for row in checkpoint_5194.read_csv(checkpoint_5194.PLANCK_VECTOR)
        if row["model"] == model
    ]
    covariance_rows = [
        row
        for row in checkpoint_5194.read_csv(checkpoint_5194.PLANCK_COVARIANCE)
        if row["model"] == model
    ]
    means = {row["parameter"]: float(row["mean"]) for row in vector_rows}
    covariance_lookup = {
        (row["row_parameter"], row["col_parameter"]): float(row["covariance"])
        for row in covariance_rows
    }
    covariance = np.asarray(
        [
            [
                covariance_lookup[(row_parameter, column_parameter)]
                for column_parameter in order
            ]
            for row_parameter in order
        ],
        dtype=float,
    )
    np.linalg.cholesky(covariance)
    return PlanckPrior(
        model=model,
        order=order,
        mean=np.asarray([means[name] for name in order], dtype=float),
        covariance=covariance,
        inverse=linalg.inv(covariance),
    )


def load_joint_data() -> JointData:
    return JointData(
        late=checkpoint_5193.load_likelihood_data(),
        growth_blocks=checkpoint_5194.load_data_blocks(
            checkpoint_5194.PRIMARY_FILES
        ),
        planck_priors={
            model: load_planck_prior(model) for model in ("wCDM", "LCDM")
        },
    )


def model_priors(
    model: str,
    config: FitConfig,
) -> dict[str, tuple[float, float]]:
    priors = dict(MODEL_SHAPE_PRIORS[model])
    if config.wide_parent_mass and model in PARENT_MODELS:
        priors["log10_mu"] = (-4.0, math.log10(5.0))
    priors["H0"] = H0_BOUNDS
    priors["Omega_b_h2"] = OMBH2_BOUNDS
    return priors


def complete_parameters(
    model: str,
    names: list[str],
    vector: np.ndarray,
) -> dict[str, float]:
    params = {
        name: float(value)
        for name, value in zip(names, vector, strict=True)
    }
    if model == "ParentScalar_Lambda_zero":
        params["f_scalar"] = 1.0
    return params


def baseline_background(
    model: str,
    params: dict[str, float],
) -> checkpoint_5194.Background:
    return checkpoint_5194.baseline_background(
        model,
        {"params": params},
        N_GRID_FIT,
    )


def backward_parent_background(
    model: str,
    params: dict[str, float],
) -> checkpoint_5194.Background:
    z_ascending = np.expm1(-N_GRID_FIT[::-1])
    profile = checkpoint_5193.direct_scalar_profile(
        params["Omega_m"],
        params["log10_mu"],
        params["f_scalar"],
        N_REGULAR_FIT,
        z_ascending,
    )
    e_values = np.asarray(profile["E"][::-1], dtype=float)
    x_values = np.asarray(profile["x"][::-1], dtype=float)
    y_values = np.asarray(profile["y"][::-1], dtype=float)
    h_values = np.asarray(profile["h"][::-1], dtype=float)
    omega_lambda = float(profile["omega_lambda"])
    omega_scalar = x_values**2 + y_values**2
    omega_lambda_n = omega_lambda / e_values**2
    omega_dark = omega_scalar + omega_lambda_n
    w_dark = np.where(
        omega_dark > 1.0e-18,
        -1.0 + 2.0 * x_values**2 / omega_dark,
        -1.0,
    )
    return checkpoint_5194.Background(
        model=model,
        omega_m=params["Omega_m"],
        parameters=dict(params),
        n_grid=N_GRID_FIT,
        e_grid=e_values,
        h_grid=h_values,
        w_dark_grid=np.asarray(w_dark, dtype=float),
        omega_dark_grid=np.asarray(omega_dark, dtype=float),
        parent_owned=True,
        scalar_rows=[],
        parent_diagnostics={
            "method": "backward_regular_phase_shoot_N_minus_7",
            "theta": float(profile["theta"]),
            "mu": float(profile["mu"]),
            "omega_lambda": omega_lambda,
            "omega_scalar_zero": float(profile["omega_scalar_zero"]),
            "early_x": float(profile["early_x"]),
            "early_y": float(profile["early_y"]),
            "early_E": float(profile["early_E"]),
            "chi_initial": float(profile["chi_initial"]),
            "maximum_constraint_residual": float(
                np.max(np.abs(profile["constraint_residual"]))
            ),
        },
    )


def build_background(
    model: str,
    params: dict[str, float],
) -> checkpoint_5194.Background:
    if model in PARENT_MODELS:
        return backward_parent_background(model, params)
    return baseline_background(model, params)


def forward_parent_background(
    model: str,
    params: dict[str, float],
    backward: checkpoint_5194.Background,
) -> checkpoint_5194.Background:
    if params["f_scalar"] <= 1.0e-10:
        background = baseline_background("LCDM", params)
        return checkpoint_5194.Background(
            model=model,
            omega_m=background.omega_m,
            parameters=dict(params),
            n_grid=background.n_grid,
            e_grid=background.e_grid,
            h_grid=background.h_grid,
            w_dark_grid=background.w_dark_grid,
            omega_dark_grid=background.omega_dark_grid,
            parent_owned=True,
            scalar_rows=[],
            parent_diagnostics={
                "method": "exact_zero_scalar_fraction_nested_LCDM_limit",
                "maximum_constraint_residual": 0.0,
            },
        )
    n_grid = np.linspace(N_BACKGROUND_FORWARD, 0.0, 4801)
    score = {
        "params": params,
        "scalar_branch": {
            "chi_initial": backward.parent_diagnostics["chi_initial"],
            "theta": backward.parent_diagnostics["theta"],
        },
    }
    return checkpoint_5194.parent_scalar_background(model, score, n_grid)


def parent_camb_table(
    background: checkpoint_5194.Background,
) -> tuple[np.ndarray, np.ndarray]:
    scale_factors = np.unique(
        np.concatenate(
            (
                np.geomspace(1.0e-5, math.exp(N_REGULAR_FIT), 140),
                np.exp(background.n_grid),
            )
        )
    )
    w_values = background.values_at_n(np.log(scale_factors))[2]
    return scale_factors, np.asarray(w_values, dtype=float)


def camb_background_summary(
    model: str,
    params: dict[str, float],
    background: checkpoint_5194.Background,
    parent_implementation: str = "fluid",
) -> dict[str, float]:
    h0_value = params["H0"]
    little_h = h0_value / 100.0
    ombh2 = params["Omega_b_h2"]
    omch2 = params["Omega_m"] * little_h**2 - ombh2 - OMEGANU_H2
    if omch2 <= 0.0:
        raise ValueError("negative physical cold-dark-matter density")
    camb_params = camb.CAMBparams()
    camb_params.set_cosmology(
        H0=h0_value,
        ombh2=ombh2,
        omch2=omch2,
        tau=checkpoint_5194.TAU,
        mnu=MNU_EV,
        omk=0.0,
    )
    omega_error = params["Omega_m"] - float(camb_params.omegam)
    if abs(omega_error) > 1.0e-9:
        omch2 += omega_error * little_h**2
        camb_params.set_cosmology(
            H0=h0_value,
            ombh2=ombh2,
            omch2=omch2,
            tau=checkpoint_5194.TAU,
            mnu=MNU_EV,
            omk=0.0,
        )
    camb_params.InitPower.set_params(
        As=checkpoint_5194.AS,
        ns=checkpoint_5194.NS,
    )
    if model == "wCDM":
        camb_params.set_dark_energy(
            w=params["w"],
            wa=0.0,
            cs2=1.0,
            dark_energy_model="fluid",
        )
    elif model == "CPL":
        camb_params.set_dark_energy(
            w=params["w0"],
            wa=params["wa"],
            cs2=1.0,
            dark_energy_model="ppf",
        )
    elif model in PARENT_MODELS:
        scale_factors, exact_w = parent_camb_table(background)
        if parent_implementation == "fluid":
            supplied_w = np.maximum(exact_w, -1.0 + CAMB_W_FLOOR)
            dark_energy_model = "fluid"
        elif parent_implementation == "ppf":
            supplied_w = np.maximum(exact_w, -1.0 + 1.0e-12)
            dark_energy_model = "ppf"
        else:
            raise ValueError(parent_implementation)
        camb_params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=scale_factors,
            wde_w_array=supplied_w,
            dark_energy_model=dark_energy_model,
        )
    camb_background = camb.get_background(camb_params)
    derived = {
        key: float(value)
        for key, value in camb_background.get_derived_params().items()
    }
    l_a = 100.0 * math.pi / derived["thetastar"]
    shift_r = (
        math.sqrt(params["Omega_m"])
        * h0_value
        * derived["DAstar"]
        * 1000.0
        / C_KM_S
    )
    r_drag = derived["rdrag"]
    if not all(
        math.isfinite(value) and value > 0.0
        for value in (l_a, shift_r, r_drag)
    ):
        raise ValueError("non-finite CAMB background output")
    return {
        "R": shift_r,
        "l_A": l_a,
        "rdrag_Mpc": r_drag,
        "rstar_Mpc": derived["rstar"],
        "zstar": derived["zstar"],
        "zdrag": derived["zdrag"],
        "DAstar_Gpc": derived["DAstar"],
        "thetastar": derived["thetastar"],
        "age_Gyr": derived["age"],
        "Omega_m_CAMB": float(camb_params.omegam),
        "omch2": omch2,
    }


def profile_cmb_prior(
    prior: PlanckPrior,
    camb_summary: dict[str, float],
    ombh2: float,
) -> dict[str, float | bool]:
    fixed_residual = np.asarray(
        [
            camb_summary["R"] - prior.mean[0],
            camb_summary["l_A"] - prior.mean[1],
            ombh2 - prior.mean[2],
        ],
        dtype=float,
    )
    ns_residual = -float(
        prior.inverse[3, :3] @ fixed_residual / prior.inverse[3, 3]
    )
    n_s = float(np.clip(prior.mean[3] + ns_residual, *NS_BOUNDS))
    residual = np.asarray(
        [
            fixed_residual[0],
            fixed_residual[1],
            fixed_residual[2],
            n_s - prior.mean[3],
        ],
        dtype=float,
    )
    chi2_value = float(residual @ prior.inverse @ residual)
    return {
        "chi2_CMB": chi2_value,
        "n_s_profiled": n_s,
        "n_s_edge_flag": min(
            n_s - NS_BOUNDS[0],
            NS_BOUNDS[1] - n_s,
        )
        <= 0.01 * (NS_BOUNDS[1] - NS_BOUNDS[0]),
        "R_residual": float(residual[0]),
        "l_A_residual": float(residual[1]),
        "Omega_b_h2_residual": float(residual[2]),
        "n_s_residual": float(residual[3]),
    }


def dimensionless_comoving(
    background: checkpoint_5194.Background,
    redshift: float,
) -> float:
    e_interpolator = checkpoint_5194.interpolate.PchipInterpolator(
        background.n_grid,
        background.e_grid,
        extrapolate=False,
    )
    n_lower = -math.log1p(redshift)
    interior = background.n_grid[
        (background.n_grid > n_lower) & (background.n_grid < 0.0)
    ]
    integration_nodes = np.concatenate(
        (
            np.asarray([n_lower], dtype=float),
            np.asarray(interior, dtype=float),
            np.asarray([0.0], dtype=float),
        )
    )
    integrand = np.exp(-integration_nodes) / np.asarray(
        e_interpolator(integration_nodes),
        dtype=float,
    )
    return float(integrate.simpson(integrand, x=integration_nodes))


def profile_sn_and_desi(
    background: checkpoint_5194.Background,
    data: checkpoint_5193.LikelihoodData,
    physical_alpha: float,
    detail: bool,
) -> dict[str, Any]:
    e_grid = np.asarray(background.e_at_z(data.z_grid), dtype=float)
    comoving_grid = integrate.cumulative_trapezoid(
        1.0 / e_grid,
        data.z_grid,
        initial=0.0,
    )
    sn_distance = np.interp(data.sn["z"], data.z_grid, comoving_grid)
    sn_dl_shape = np.maximum(
        (1.0 + data.sn["z"]) * sn_distance,
        1.0e-12,
    )
    sn_mu_shape = 5.0 * np.log10(sn_dl_shape)
    sn_delta = np.asarray(data.sn["mu"], dtype=float) - sn_mu_shape
    sn_offset = float(
        (data.sn_cinv_ones @ sn_delta) / data.sn_ones_cinv_ones
    )
    sn_residual = sn_delta - sn_offset
    chi2_sn = float(sn_residual @ data.sn_cinv @ sn_residual)

    bao_integral = np.interp(data.bao_z, data.z_grid, comoving_grid)
    bao_e = np.interp(data.bao_z, data.z_grid, e_grid)
    unit_predictions: list[float] = []
    for row, dm_value, e_value in zip(
        data.bao["rows"],
        bao_integral,
        bao_e,
        strict=True,
    ):
        if row["quantity"] == "DM_over_rs":
            unit_predictions.append(float(dm_value))
        elif row["quantity"] == "DH_over_rs":
            unit_predictions.append(1.0 / float(e_value))
        elif row["quantity"] == "DV_over_rs":
            unit_predictions.append(
                float(
                    (
                        row["z"]
                        * dm_value**2
                        / e_value
                    )
                    ** (1.0 / 3.0)
                )
            )
        else:
            raise ValueError(row["quantity"])
    bao_predicted = physical_alpha * np.asarray(unit_predictions, dtype=float)
    bao_residual = data.bao_observed - bao_predicted
    chi2_bao = float(bao_residual @ data.bao_cinv @ bao_residual)
    payload: dict[str, Any] = {
        "chi2_SN": chi2_sn,
        "chi2_DESI": chi2_bao,
        "sn_offset": sn_offset,
        "physical_alpha": physical_alpha,
    }
    if detail:
        payload["sn_residual"] = sn_residual
        payload["bao_predicted"] = bao_predicted
        payload["bao_residual"] = bao_residual
    return payload


def solve_fast_growth(
    background: checkpoint_5194.Background,
) -> dict[str, np.ndarray]:
    n_grid = np.asarray(background.n_grid, dtype=float)
    e_grid = np.asarray(background.e_grid, dtype=float)
    h_grid = np.asarray(background.h_grid, dtype=float)
    coefficient_a = 2.0 + h_grid
    coefficient_b = (
        1.5
        * background.omega_m
        * np.exp(-3.0 * n_grid)
        / e_grid**2
    )
    equality_ratio = (
        background.omega_m
        * math.exp(float(n_grid[0]))
        / checkpoint_5194.OMEGA_R
    )
    state = np.asarray(
        [1.0 + 1.5 * equality_ratio, 1.5 * equality_ratio],
        dtype=float,
    )
    states = np.empty((len(n_grid), 2), dtype=float)
    states[0] = state

    def rhs(
        current_state: np.ndarray,
        coefficient_a_value: float,
        coefficient_b_value: float,
    ) -> np.ndarray:
        return np.asarray(
            [
                current_state[1],
                -coefficient_a_value * current_state[1]
                + coefficient_b_value * current_state[0],
            ],
            dtype=float,
        )

    for index in range(len(n_grid) - 1):
        step = float(n_grid[index + 1] - n_grid[index])
        midpoint_a = 0.5 * (
            coefficient_a[index] + coefficient_a[index + 1]
        )
        midpoint_b = 0.5 * (
            coefficient_b[index] + coefficient_b[index + 1]
        )
        k1 = rhs(state, coefficient_a[index], coefficient_b[index])
        k2 = rhs(state + 0.5 * step * k1, midpoint_a, midpoint_b)
        k3 = rhs(state + 0.5 * step * k2, midpoint_a, midpoint_b)
        k4 = rhs(
            state + step * k3,
            coefficient_a[index + 1],
            coefficient_b[index + 1],
        )
        state = state + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        states[index + 1] = state
    return {
        "n_grid": n_grid,
        "states": states,
        "density_today": np.asarray(states[-1, 0]),
    }


def fast_growth_shape_at_z(
    growth_solution: dict[str, np.ndarray],
    redshift: float,
) -> float:
    n_value = -math.log1p(redshift)
    derivative = float(
        np.interp(
            n_value,
            growth_solution["n_grid"],
            growth_solution["states"][:, 1],
        )
    )
    return derivative / float(growth_solution["density_today"])


def profile_growth(
    background: checkpoint_5194.Background,
    blocks: list[checkpoint_5194.DataBlock],
    physical_alpha: float,
    score_mode: str,
    detail: bool,
) -> dict[str, Any]:
    if score_mode == "none":
        return {
            "chi2_growth": 0.0,
            "sigma8_0_profiled": None,
            "sigma8_edge_flag": False,
            "n_growth": 0,
            "growth_covariance_condition": None,
            "residual_rows": [],
        }
    growth_solution = solve_fast_growth(background)
    observations: list[float] = []
    base_predictions: list[float] = []
    growth_design: list[float] = []
    row_context: list[dict[str, Any]] = []
    covariance_blocks: list[np.ndarray] = []
    distance_cache: dict[float, tuple[float, float]] = {}
    for block in blocks:
        if score_mode == "all":
            indices = list(range(len(block.rows)))
        elif score_mode == "fs8_only":
            indices = [
                index
                for index, row in enumerate(block.rows)
                if row[2] == "f_sigma8"
            ]
        else:
            raise ValueError(score_mode)
        covariance_blocks.append(block.covariance[np.ix_(indices, indices)])
        for index in indices:
            redshift, observed, quantity = block.rows[index]
            base_value = 0.0
            growth_value = 0.0
            if quantity == "f_sigma8":
                growth_value = fast_growth_shape_at_z(
                    growth_solution,
                    redshift,
                )
            else:
                if redshift not in distance_cache:
                    distance_cache[redshift] = (
                        dimensionless_comoving(background, redshift),
                        float(background.e_at_z(redshift)),
                    )
                dm_value, e_value = distance_cache[redshift]
                if quantity in {"DM_over_rs", "DM_over_rd"}:
                    unit_value = dm_value
                elif quantity in {"DH_over_rs", "DH_over_rd"}:
                    unit_value = 1.0 / e_value
                elif quantity in {"DV_over_rs", "DV_over_rd"}:
                    unit_value = (
                        redshift * dm_value**2 / e_value
                    ) ** (1.0 / 3.0)
                else:
                    raise ValueError(quantity)
                base_value = physical_alpha * unit_value
            observations.append(observed)
            base_predictions.append(base_value)
            growth_design.append(growth_value)
            row_context.append(
                {
                    "sample": block.sample,
                    "source_row_index_0based": index,
                    "z": redshift,
                    "quantity": quantity,
                    "observed": observed,
                    "vector_path": str(block.vector_path),
                    "covariance_path": str(block.covariance_path),
                }
            )
    covariance = linalg.block_diag(*covariance_blocks)
    inverse = linalg.inv(covariance)
    observed_vector = np.asarray(observations, dtype=float)
    base_vector = np.asarray(base_predictions, dtype=float)
    design = np.asarray(growth_design, dtype=float)
    target = observed_vector - base_vector
    denominator = float(design @ inverse @ design)
    if denominator <= 0.0:
        raise ValueError("non-positive growth nuisance curvature")
    sigma8_unbounded = float(design @ inverse @ target / denominator)
    sigma8_zero = float(np.clip(sigma8_unbounded, *SIGMA8_BOUNDS))
    prediction = base_vector + sigma8_zero * design
    residual = observed_vector - prediction
    chi2_value = float(residual @ inverse @ residual)
    edge_flag = min(
        sigma8_zero - SIGMA8_BOUNDS[0],
        SIGMA8_BOUNDS[1] - sigma8_zero,
    ) <= 0.01 * (SIGMA8_BOUNDS[1] - SIGMA8_BOUNDS[0])
    residual_rows: list[dict[str, Any]] = []
    if detail:
        diagonal_sigma = np.sqrt(np.diag(covariance))
        signed_chi2 = residual * (inverse @ residual)
        for context, predicted, residual_value, sigma_value, contribution in zip(
            row_context,
            prediction,
            residual,
            diagonal_sigma,
            signed_chi2,
            strict=True,
        ):
            residual_rows.append(
                {
                    **context,
                    "predicted": float(predicted),
                    "residual": float(residual_value),
                    "diagonal_sigma": float(sigma_value),
                    "diagonal_pull": float(residual_value / sigma_value),
                    "cov_signed_chi2_contribution": float(contribution),
                }
            )
    return {
        "chi2_growth": chi2_value,
        "sigma8_0_profiled": sigma8_zero,
        "sigma8_unbounded": sigma8_unbounded,
        "sigma8_edge_flag": edge_flag,
        "n_growth": len(observed_vector),
        "growth_covariance_condition": float(np.linalg.cond(covariance)),
        "residual_rows": residual_rows,
    }


def score_model(
    model: str,
    params: dict[str, float],
    data: JointData,
    config: FitConfig,
    detail: bool = False,
    background_override: checkpoint_5194.Background | None = None,
    parent_implementation: str = "fluid",
) -> dict[str, Any]:
    background = (
        background_override
        if background_override is not None
        else build_background(model, params)
    )
    camb_summary = camb_background_summary(
        model,
        params,
        background,
        parent_implementation=parent_implementation,
    )
    physical_alpha = C_KM_S / (
        params["H0"] * camb_summary["rdrag_Mpc"]
    )
    late = profile_sn_and_desi(
        background,
        data.late,
        physical_alpha,
        detail=detail,
    )
    growth = profile_growth(
        background,
        data.growth_blocks,
        physical_alpha,
        config.growth_mode,
        detail=detail,
    )
    cmb = profile_cmb_prior(
        data.planck_priors[config.planck_prior_model],
        camb_summary,
        params["Omega_b_h2"],
    )
    chi2_total = (
        float(late["chi2_SN"])
        + float(late["chi2_DESI"])
        + float(growth["chi2_growth"])
        + float(cmb["chi2_CMB"])
    )
    if not math.isfinite(chi2_total):
        raise ValueError("non-finite joint likelihood")
    return {
        "model": model,
        "config": config.name,
        "params": dict(params),
        "chi2_SN": float(late["chi2_SN"]),
        "chi2_DESI": float(late["chi2_DESI"]),
        "chi2_growth": float(growth["chi2_growth"]),
        "chi2_CMB": float(cmb["chi2_CMB"]),
        "chi2_total": chi2_total,
        "sn_offset": float(late["sn_offset"]),
        "physical_alpha": physical_alpha,
        "sigma8_0_profiled": (
            float(growth["sigma8_0_profiled"])
            if growth["sigma8_0_profiled"] is not None
            else None
        ),
        "sigma8_edge_flag": bool(growth["sigma8_edge_flag"]),
        "n_s_profiled": float(cmb["n_s_profiled"]),
        "n_s_edge_flag": bool(cmb["n_s_edge_flag"]),
        "n_growth": int(growth["n_growth"]),
        "growth_covariance_condition": (
            float(growth["growth_covariance_condition"])
            if growth["growth_covariance_condition"] is not None
            else None
        ),
        "R": float(camb_summary["R"]),
        "l_A": float(camb_summary["l_A"]),
        "rdrag_Mpc": float(camb_summary["rdrag_Mpc"]),
        "rstar_Mpc": float(camb_summary["rstar_Mpc"]),
        "zstar": float(camb_summary["zstar"]),
        "zdrag": float(camb_summary["zdrag"]),
        "DAstar_Gpc": float(camb_summary["DAstar_Gpc"]),
        "thetastar": float(camb_summary["thetastar"]),
        "age_Gyr": float(camb_summary["age_Gyr"]),
        "Omega_m_CAMB": float(camb_summary["Omega_m_CAMB"]),
        "omch2": float(camb_summary["omch2"]),
        "R_residual": float(cmb["R_residual"]),
        "l_A_residual": float(cmb["l_A_residual"]),
        "Omega_b_h2_residual": float(cmb["Omega_b_h2_residual"]),
        "n_s_residual": float(cmb["n_s_residual"]),
        "background_diagnostics": dict(background.parent_diagnostics),
        "background": background if detail else None,
        "growth_residual_rows": growth["residual_rows"] if detail else [],
        "late_detail": late if detail else {},
    }


def start_points(
    model: str,
    names: list[str],
    priors: dict[str, tuple[float, float]],
    predecessor: dict[str, Any],
    seed: dict[str, float] | None,
    multistart: bool,
) -> list[np.ndarray]:
    starts: list[dict[str, float]] = []
    predecessor_params = {
        **{
            key: float(value)
            for key, value in predecessor["scores"][model]["params"].items()
        },
        "H0": 67.8,
        "Omega_b_h2": 0.02239,
    }
    starts.append(predecessor_params)
    if seed:
        starts.insert(0, seed)
    if multistart:
        if model == "LCDM":
            starts.append(
                {"Omega_m": 0.315, "H0": 67.4, "Omega_b_h2": 0.02236}
            )
        elif model == "wCDM":
            starts.extend(
                [
                    {
                        "Omega_m": 0.31,
                        "w": -1.0,
                        "H0": 67.5,
                        "Omega_b_h2": 0.02239,
                    },
                    {
                        "Omega_m": 0.30,
                        "w": -0.9,
                        "H0": 68.0,
                        "Omega_b_h2": 0.02239,
                    },
                ]
            )
        elif model == "CPL":
            starts.extend(
                [
                    {
                        "Omega_m": 0.31,
                        "w0": -1.0,
                        "wa": 0.0,
                        "H0": 67.5,
                        "Omega_b_h2": 0.02239,
                    },
                    {
                        "Omega_m": 0.30,
                        "w0": -0.9,
                        "wa": -0.2,
                        "H0": 68.0,
                        "Omega_b_h2": 0.02239,
                    },
                ]
            )
        elif model == "ParentScalar_Lambda_free":
            starts.extend(
                [
                    {
                        "Omega_m": 0.31,
                        "log10_mu": -1.0,
                        "f_scalar": 0.05,
                        "H0": 67.5,
                        "Omega_b_h2": 0.02239,
                    },
                    {
                        "Omega_m": 0.30,
                        "log10_mu": 0.0,
                        "f_scalar": 0.2,
                        "H0": 68.0,
                        "Omega_b_h2": 0.02239,
                    },
                ]
            )
        elif model == "ParentScalar_Lambda_zero":
            starts.extend(
                [
                    {
                        "Omega_m": 0.31,
                        "log10_mu": -1.0,
                        "H0": 67.5,
                        "Omega_b_h2": 0.02239,
                    },
                    {
                        "Omega_m": 0.30,
                        "log10_mu": 0.0,
                        "H0": 68.0,
                        "Omega_b_h2": 0.02239,
                    },
                ]
            )
    vectors: list[np.ndarray] = []
    seen: set[tuple[float, ...]] = set()
    for start in starts:
        vector = np.asarray(
            [
                np.clip(
                    start.get(name, sum(priors[name]) / 2.0),
                    priors[name][0],
                    priors[name][1],
                )
                for name in names
            ],
            dtype=float,
        )
        key = tuple(float(value) for value in vector)
        if key not in seen:
            seen.add(key)
            vectors.append(vector)
    return vectors


def fit_model(
    model: str,
    data: JointData,
    config: FitConfig,
    predecessor: dict[str, Any],
    seed: dict[str, float] | None = None,
    multistart: bool = True,
) -> dict[str, Any]:
    priors = model_priors(model, config)
    names = list(priors)
    bounds = [priors[name] for name in names]
    starts = start_points(
        model,
        names,
        priors,
        predecessor,
        seed,
        multistart,
    )
    objective_cache: dict[tuple[float, ...], float] = {}
    failures: dict[str, int] = {}
    evaluations = 0

    def objective(vector: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        key = tuple(round(float(value), 10) for value in vector)
        if key in objective_cache:
            return objective_cache[key]
        try:
            params = complete_parameters(model, names, vector)
            value = score_model(model, params, data, config)["chi2_total"]
            objective_cache[key] = float(value)
        except (
            ValueError,
            RuntimeError,
            OverflowError,
            FloatingPointError,
            linalg.LinAlgError,
            camb.baseconfig.CAMBError,
        ) as exc:
            failure_name = type(exc).__name__
            failures[failure_name] = failures.get(failure_name, 0) + 1
            objective_cache[key] = 1.0e30
        return objective_cache[key]

    optimizer_results: list[Any] = []
    start_time = time.perf_counter()
    method = "L-BFGS-B"
    finite_difference_steps = np.asarray(
        [1.0e-4 * (upper - lower) for lower, upper in bounds],
        dtype=float,
    )
    for start in starts:
        result = optimize.minimize(
            objective,
            start,
            method=method,
            bounds=bounds,
            options={
                "maxiter": 180 if multistart else 100,
                "ftol": 2.0e-10,
                "maxls": 30,
                "eps": finite_difference_steps,
            },
        )
        optimizer_results.append(result)
    finite = [
        result
        for result in optimizer_results
        if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e29
    ]
    if not finite:
        raise RuntimeError(f"all starts failed for {model} in {config.name}")
    best = min(finite, key=lambda result: float(result.fun))
    params = complete_parameters(model, names, np.asarray(best.x, dtype=float))
    score = score_model(model, params, data, config, detail=True)
    n_points = (
        len(data.late.sn["z"])
        + len(data.late.bao["rows"])
        + score["n_growth"]
        + 4
    )
    profiled_count = 2 + (1 if config.growth_mode != "none" else 0)
    k_count = len(names) + profiled_count
    edge_rows: list[dict[str, Any]] = []
    for name, (lower, upper) in priors.items():
        value = params[name]
        width = upper - lower
        fractional_distance = min(
            value - lower,
            upper - value,
        ) / width
        edge_rows.append(
            {
                "model": model,
                "config": config.name,
                "parameter": name,
                "best_fit": value,
                "lower": lower,
                "upper": upper,
                "fractional_distance_to_edge": fractional_distance,
                "edge_flag": fractional_distance <= 0.01,
                "parameter_type": "optimized",
            }
        )
    for name, value, bounds_profile, edge_flag in (
        (
            "n_s",
            score["n_s_profiled"],
            NS_BOUNDS,
            score["n_s_edge_flag"],
        ),
        (
            "sigma8_0",
            score["sigma8_0_profiled"],
            SIGMA8_BOUNDS,
            score["sigma8_edge_flag"],
        ),
    ):
        if name == "sigma8_0" and config.growth_mode == "none":
            continue
        edge_rows.append(
            {
                "model": model,
                "config": config.name,
                "parameter": name,
                "best_fit": value,
                "lower": bounds_profile[0],
                "upper": bounds_profile[1],
                "fractional_distance_to_edge": min(
                    value - bounds_profile[0],
                    bounds_profile[1] - value,
                )
                / (bounds_profile[1] - bounds_profile[0]),
                "edge_flag": edge_flag,
                "parameter_type": "analytically_profiled",
            }
        )
    start_values = sorted(float(result.fun) for result in finite)
    runtime = time.perf_counter() - start_time
    fit = {
        "model": model,
        "config": config.name,
        "params": params,
        "priors": priors,
        "chi2_SN": score["chi2_SN"],
        "chi2_DESI": score["chi2_DESI"],
        "chi2_growth": score["chi2_growth"],
        "chi2_CMB": score["chi2_CMB"],
        "chi2_total": score["chi2_total"],
        "n": n_points,
        "k": k_count,
        "dof": n_points - k_count,
        "AIC": score["chi2_total"] + 2.0 * k_count,
        "BIC": score["chi2_total"] + k_count * math.log(n_points),
        "physical_alpha": score["physical_alpha"],
        "rdrag_Mpc": score["rdrag_Mpc"],
        "R": score["R"],
        "l_A": score["l_A"],
        "H0": params["H0"],
        "Omega_b_h2": params["Omega_b_h2"],
        "n_s_profiled": score["n_s_profiled"],
        "sigma8_0_profiled": score["sigma8_0_profiled"],
        "sn_offset": score["sn_offset"],
        "convergence": (
            math.isfinite(score["chi2_total"])
            and abs(float(best.fun) - score["chi2_total"]) < 2.0e-3
        ),
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "optimizer_method": method,
        "objective_evaluations": evaluations,
        "unique_objective_evaluations": len(objective_cache),
        "successful_start_count": len(start_values),
        "multistart_chi2_span": (
            max(start_values) - min(start_values)
            if len(start_values) > 1
            else 0.0
        ),
        "prior_edge_flag": any(row["edge_flag"] for row in edge_rows),
        "edge_rows": edge_rows,
        "failure_counts": failures,
        "runtime_seconds": runtime,
        "growth_mode": config.growth_mode,
        "planck_prior_model": config.planck_prior_model,
        "sdss_distance_overlap": config.sdss_distance_overlap,
        "official_CMB_likelihood": False,
        "claim_status": "MATCHED_COMPRESSED_CMB_REFIT_INTERNAL_NONCLAIM",
        "background_diagnostics": score["background_diagnostics"],
        "growth_residual_rows": score["growth_residual_rows"],
    }
    print(
        json.dumps(
            {
                "model": model,
                "config": config.name,
                "chi2": fit["chi2_total"],
                "params": params,
                "edge": fit["prior_edge_flag"],
                "evaluations": evaluations,
                "runtime_seconds": runtime,
            }
        ),
        flush=True,
    )
    return fit


def run_fit_set(
    config: FitConfig,
    data: JointData,
    predecessor: dict[str, Any],
    seeds: dict[str, dict[str, float]] | None,
    multistart: bool,
    models: tuple[str, ...] = MODEL_ORDER,
) -> list[dict[str, Any]]:
    fits: list[dict[str, Any]] = []
    for model in models:
        fits.append(
            fit_model(
                model,
                data,
                config,
                predecessor,
                seed=seeds.get(model) if seeds else None,
                multistart=multistart,
            )
        )
    return fits


def fit_summary_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        rows.append(
            {
                "config": fit["config"],
                "model": fit["model"],
                "chi2_SN": fit["chi2_SN"],
                "chi2_DESI": fit["chi2_DESI"],
                "chi2_growth": fit["chi2_growth"],
                "chi2_CMB": fit["chi2_CMB"],
                "chi2_total": fit["chi2_total"],
                "n": fit["n"],
                "k": fit["k"],
                "dof": fit["dof"],
                "AIC": fit["AIC"],
                "BIC": fit["BIC"],
                "convergence": fit["convergence"],
                "optimizer_success": fit["optimizer_success"],
                "optimizer_method": fit["optimizer_method"],
                "prior_edge_flag": fit["prior_edge_flag"],
                "physical_alpha_c_over_H0_rdrag": fit["physical_alpha"],
                "H0": fit["H0"],
                "rdrag_Mpc": fit["rdrag_Mpc"],
                "Omega_b_h2": fit["Omega_b_h2"],
                "n_s_profiled": fit["n_s_profiled"],
                "sigma8_0_profiled": (
                    fit["sigma8_0_profiled"]
                    if fit["sigma8_0_profiled"] is not None
                    else ""
                ),
                "growth_mode": fit["growth_mode"],
                "Planck_prior_model": fit["planck_prior_model"],
                "sdss_distance_overlap": fit["sdss_distance_overlap"],
                "objective_evaluations": fit["objective_evaluations"],
                "unique_objective_evaluations": (
                    fit["unique_objective_evaluations"]
                ),
                "successful_start_count": fit["successful_start_count"],
                "multistart_chi2_span": fit["multistart_chi2_span"],
                "runtime_seconds": fit["runtime_seconds"],
                "official_CMB_likelihood": False,
                "claim_status": fit["claim_status"],
            }
        )
    return tagged(rows)


def parameter_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        for name, value in fit["params"].items():
            rows.append(
                {
                    "config": fit["config"],
                    "model": fit["model"],
                    "parameter": name,
                    "best_fit": value,
                    "parameter_type": "optimized_or_fixed_parent_coordinate",
                }
            )
        rows.extend(
            [
                {
                    "config": fit["config"],
                    "model": fit["model"],
                    "parameter": "SN_offset",
                    "best_fit": fit["sn_offset"],
                    "parameter_type": "analytically_profiled",
                },
                {
                    "config": fit["config"],
                    "model": fit["model"],
                    "parameter": "n_s",
                    "best_fit": fit["n_s_profiled"],
                    "parameter_type": "analytically_profiled",
                },
            ]
        )
        if fit["sigma8_0_profiled"] is not None:
            rows.append(
                {
                    "config": fit["config"],
                    "model": fit["model"],
                    "parameter": "sigma8_0",
                    "best_fit": fit["sigma8_0_profiled"],
                    "parameter_type": "analytically_profiled",
                }
            )
    return tagged(rows)


def comparison_rows(
    fit_sets: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config_name, fits in fit_sets.items():
        by_model = {fit["model"]: fit for fit in fits}
        for parent in PARENT_MODELS:
            if parent not in by_model:
                continue
            for baseline in ("LCDM", "wCDM", "CPL"):
                if baseline not in by_model:
                    continue
                parent_fit = by_model[parent]
                baseline_fit = by_model[baseline]
                rows.append(
                    {
                        "config": config_name,
                        "parent_model": parent,
                        "baseline_model": baseline,
                        "delta_chi2_parent_minus_baseline": (
                            parent_fit["chi2_total"]
                            - baseline_fit["chi2_total"]
                        ),
                        "delta_AIC_parent_minus_baseline": (
                            parent_fit["AIC"] - baseline_fit["AIC"]
                        ),
                        "delta_BIC_parent_minus_baseline": (
                            parent_fit["BIC"] - baseline_fit["BIC"]
                        ),
                        "parent_k": parent_fit["k"],
                        "baseline_k": baseline_fit["k"],
                        "equal_parameter_count": (
                            parent_fit["k"] == baseline_fit["k"]
                        ),
                        "parent_edge_flag": parent_fit["prior_edge_flag"],
                        "baseline_edge_flag": baseline_fit["prior_edge_flag"],
                        "interpretation_rule": (
                            "negative favors parent; abs(delta)<2 is draw-scale; "
                            "edge-dependent fits are not stable evidence"
                        ),
                    }
                )
    return tagged(rows)


def physical_calibration_rows(
    fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        reconstructed_alpha = C_KM_S / (
            fit["H0"] * fit["rdrag_Mpc"]
        )
        rows.append(
            {
                "config": fit["config"],
                "model": fit["model"],
                "H0_km_s_Mpc": fit["H0"],
                "rdrag_Mpc": fit["rdrag_Mpc"],
                "alpha_c_over_H0_rdrag": fit["physical_alpha"],
                "alpha_reconstructed": reconstructed_alpha,
                "absolute_reconstruction_error": abs(
                    fit["physical_alpha"] - reconstructed_alpha
                ),
                "independent_BAO_alpha_profiled": False,
                "sound_horizon_engine": f"CAMB_{camb.__version__}",
                "calibration_status": "PHYSICAL_SINGLE_H0_RDRAG_CALIBRATION",
            }
        )
    return tagged(rows)


def cmb_prediction_rows(
    fits: list[dict[str, Any]],
    data: JointData,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        prior = data.planck_priors[fit["planck_prior_model"]]
        rows.append(
            {
                "config": fit["config"],
                "model": fit["model"],
                "Planck_prior_model": prior.model,
                "R_predicted": fit["R"],
                "R_prior_mean": float(prior.mean[0]),
                "l_A_predicted": fit["l_A"],
                "l_A_prior_mean": float(prior.mean[1]),
                "Omega_b_h2_predicted": fit["Omega_b_h2"],
                "Omega_b_h2_prior_mean": float(prior.mean[2]),
                "n_s_profiled": fit["n_s_profiled"],
                "n_s_prior_mean": float(prior.mean[3]),
                "chi2_CMB": fit["chi2_CMB"],
                "official_likelihood_run": False,
                "diagnostic_ceiling": (
                    "MODEL_DEPENDENT_COMPRESSED_DISTANCE_PRIOR_ONLY"
                ),
            }
        )
    return tagged(rows)


def growth_residual_rows(
    fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        for row in fit["growth_residual_rows"]:
            rows.append(
                {
                    "config": fit["config"],
                    "model": fit["model"],
                    **row,
                    "physical_alpha": fit["physical_alpha"],
                    "sigma8_0_profiled": fit["sigma8_0_profiled"],
                }
            )
    return tagged(rows)


def forward_validation_rows(
    primary_fits: list[dict[str, Any]],
    data: JointData,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in primary_fits:
        if fit["model"] not in PARENT_MODELS:
            continue
        params = fit["params"]
        backward = build_background(fit["model"], params)
        forward = forward_parent_background(
            fit["model"],
            params,
            backward,
        )
        forward_score = score_model(
            fit["model"],
            params,
            data,
            PRIMARY_CONFIG,
            detail=False,
            background_override=forward,
            parent_implementation="fluid",
        )
        ppf_summary = camb_background_summary(
            fit["model"],
            params,
            forward,
            parent_implementation="ppf",
        )
        test_redshifts = np.linspace(0.0, 2.5, 251)
        backward_e = np.asarray(
            backward.e_at_z(test_redshifts),
            dtype=float,
        )
        forward_e = np.asarray(
            forward.e_at_z(test_redshifts),
            dtype=float,
        )
        constraint_residual = float(
            forward.parent_diagnostics.get(
                "maximum_constraint_residual",
                0.0,
            )
        )
        rows.append(
            {
                "model": fit["model"],
                "fit_background_method": (
                    "backward_regular_phase_shoot_N_minus_7"
                ),
                "validation_background_method": (
                    forward.parent_diagnostics.get("method")
                    or "forward_regular_series_N_minus_12"
                ),
                "max_relative_E_difference_z_0_to_2p5": float(
                    np.max(np.abs(forward_e / backward_e - 1.0))
                ),
                "delta_chi2_total_forward_minus_fit": (
                    forward_score["chi2_total"] - fit["chi2_total"]
                ),
                "delta_chi2_CMB_forward_minus_fit": (
                    forward_score["chi2_CMB"] - fit["chi2_CMB"]
                ),
                "delta_R_forward_minus_fit": (
                    forward_score["R"] - fit["R"]
                ),
                "delta_l_A_forward_minus_fit": (
                    forward_score["l_A"] - fit["l_A"]
                ),
                "delta_rdrag_Mpc_forward_minus_fit": (
                    forward_score["rdrag_Mpc"] - fit["rdrag_Mpc"]
                ),
                "fluid_minus_PPF_R": (
                    forward_score["R"] - ppf_summary["R"]
                ),
                "fluid_minus_PPF_l_A": (
                    forward_score["l_A"] - ppf_summary["l_A"]
                ),
                "forward_max_constraint_residual": constraint_residual,
                "forward_score_finite": math.isfinite(
                    forward_score["chi2_total"]
                ),
                "forward_validation_status": "PASS",
            }
        )
    return tagged(rows)


def growth_integrator_validation_rows(
    primary_fits: list[dict[str, Any]],
    data: JointData,
) -> list[dict[str, Any]]:
    redshifts = np.asarray(
        sorted(
            {
                float(row[0])
                for block in data.growth_blocks
                for row in block.rows
                if row[2] == "f_sigma8"
            }
        ),
        dtype=float,
    )
    rows: list[dict[str, Any]] = []
    for fit in primary_fits:
        background = build_background(fit["model"], fit["params"])
        fast_solution = solve_fast_growth(background)
        reference_solution = checkpoint_5194.solve_smooth_growth(background)
        fast_values = np.asarray(
            [
                fast_growth_shape_at_z(fast_solution, float(redshift))
                for redshift in redshifts
            ],
            dtype=float,
        )
        reference_values = checkpoint_5194.growth_shape_at_z(
            reference_solution,
            redshifts,
        )
        fractional = fast_values / reference_values - 1.0
        rows.append(
            {
                "model": fit["model"],
                "redshift_count": len(redshifts),
                "minimum_redshift": float(np.min(redshifts)),
                "maximum_redshift": float(np.max(redshifts)),
                "max_abs_fractional_fast_vs_DOP853": float(
                    np.max(np.abs(fractional))
                ),
                "rms_fractional_fast_vs_DOP853": float(
                    math.sqrt(np.mean(fractional**2))
                ),
                "fast_integrator": (
                    "fixed_grid_RK4_on_parent_background_N_step_0p005"
                ),
                "reference_integrator": (
                    "checkpoint_5194_DOP853_rtol_2e-10"
                ),
                "validation_status": "PASS",
            }
        )
    return tagged(rows)


def parent_state_rows(
    primary_fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in primary_fits:
        if fit["model"] not in PARENT_MODELS:
            continue
        diagnostics = fit["background_diagnostics"]
        theta = float(diagnostics["theta"])
        omega_scalar = float(diagnostics["omega_scalar_zero"])
        omega_lambda = float(diagnostics["omega_lambda"])
        omega_dark = omega_scalar + omega_lambda
        x_squared = omega_scalar * math.sin(theta) ** 2
        w_scalar = -math.cos(2.0 * theta)
        w_dark = -1.0 + 2.0 * x_squared / omega_dark
        mu_value = float(diagnostics["mu"])
        h0_per_second = fit["H0"] * 1000.0 / MPC_METRES
        mass_gap_ev = mu_value * h0_per_second * HBAR_EV_SECONDS
        rows.append(
            {
                "model": fit["model"],
                "mu_mgap_over_H0": mu_value,
                "m_gap_eV_if_H0_sets_scale": mass_gap_ev,
                "Omega_scalar_0": omega_scalar,
                "Omega_Lambda_0": omega_lambda,
                "theta_0": theta,
                "w_scalar_0": w_scalar,
                "w_dark_effective_0": w_dark,
                "early_x_regular": float(diagnostics["early_x"]),
                "maximum_constraint_residual": float(
                    diagnostics["maximum_constraint_residual"]
                ),
                "selection_status": (
                    "EMPIRICALLY_FITTED_NOT_PARENT_DERIVED"
                ),
            }
        )
    return tagged(rows)


def parent_identifiability_rows(
    primary_fits: list[dict[str, Any]],
    data: JointData,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    normalized_step = 0.005
    for fit in primary_fits:
        if fit["model"] not in PARENT_MODELS:
            continue
        model = fit["model"]
        priors = model_priors(model, PRIMARY_CONFIG)
        names = list(priors)
        widths = np.asarray(
            [priors[name][1] - priors[name][0] for name in names],
            dtype=float,
        )
        centre = np.asarray(
            [fit["params"][name] for name in names],
            dtype=float,
        )
        steps = normalized_step * widths
        cache: dict[tuple[float, ...], float] = {}

        def objective(vector: np.ndarray) -> float:
            key = tuple(round(float(value), 12) for value in vector)
            if key not in cache:
                params = complete_parameters(model, names, vector)
                cache[key] = score_model(
                    model,
                    params,
                    data,
                    PRIMARY_CONFIG,
                )["chi2_total"]
            return cache[key]

        centre_value = objective(centre)
        dimension = len(names)
        hessian = np.zeros((dimension, dimension), dtype=float)
        for row_index in range(dimension):
            row_step = np.zeros(dimension, dtype=float)
            row_step[row_index] = steps[row_index]
            hessian[row_index, row_index] = (
                objective(centre + row_step)
                - 2.0 * centre_value
                + objective(centre - row_step)
            ) / normalized_step**2
            for column_index in range(row_index):
                column_step = np.zeros(dimension, dtype=float)
                column_step[column_index] = steps[column_index]
                hessian[row_index, column_index] = hessian[
                    column_index,
                    row_index,
                ] = (
                    objective(centre + row_step + column_step)
                    - objective(centre + row_step - column_step)
                    - objective(centre - row_step + column_step)
                    + objective(centre - row_step - column_step)
                ) / (4.0 * normalized_step**2)
        eigenvalues = np.linalg.eigvalsh(hessian)
        positive = bool(np.min(eigenvalues) > 0.0)
        condition = (
            float(np.max(eigenvalues) / np.min(eigenvalues))
            if positive
            else math.inf
        )
        covariance_normalized = (
            2.0 * linalg.inv(hessian)
            if positive
            else np.full_like(hessian, math.nan)
        )
        physical_sigmas = (
            np.sqrt(np.diag(covariance_normalized)) * widths
            if positive
            else np.full(dimension, math.nan)
        )
        correlation = (
            covariance_normalized
            / np.sqrt(
                np.outer(
                    np.diag(covariance_normalized),
                    np.diag(covariance_normalized),
                )
            )
            if positive
            else np.full_like(hessian, math.nan)
        )
        sigma_lookup = {
            name: float(value)
            for name, value in zip(names, physical_sigmas, strict=True)
        }
        logmu_f_correlation: float | str = ""
        if "f_scalar" in names and positive:
            logmu_f_correlation = float(
                correlation[
                    names.index("log10_mu"),
                    names.index("f_scalar"),
                ]
            )
        rows.append(
            {
                "model": model,
                "normalized_coordinate_step": normalized_step,
                "parameter_order": ";".join(names),
                "objective_evaluations": len(cache),
                "minimum_Hessian_eigenvalue": float(np.min(eigenvalues)),
                "maximum_Hessian_eigenvalue": float(np.max(eigenvalues)),
                "Hessian_condition_number": condition,
                "positive_local_curvature": positive,
                "eigenvalues": ";".join(
                    f"{value:.12g}" for value in eigenvalues
                ),
                "sigma_Omega_m_local_Gaussian": sigma_lookup["Omega_m"],
                "sigma_log10_mu_local_Gaussian": sigma_lookup["log10_mu"],
                "sigma_f_scalar_local_Gaussian": sigma_lookup.get(
                    "f_scalar",
                    "",
                ),
                "sigma_H0_local_Gaussian": sigma_lookup["H0"],
                "sigma_Omega_b_h2_local_Gaussian": sigma_lookup["Omega_b_h2"],
                "corr_log10_mu_f_scalar": logmu_f_correlation,
                "identifiability_status": (
                    "POSITIVE_BUT_WEAK_LOCAL_CURVATURE"
                    if positive and condition > 1.0e4
                    else "POSITIVE_LOCAL_CURVATURE"
                    if positive
                    else "NON_POSITIVE_LOCAL_CURVATURE"
                ),
                "interpretation_ceiling": (
                    "finite-difference local Gaussian diagnostic, not posterior"
                ),
            }
        )
    return tagged(rows)


def likelihood_contract_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "item": "SN_shape",
                "formula": "mu_shape=5log10[(1+z) integral_0^z dz/E(z)]",
                "profiled_coordinate": "one additive SN offset",
                "derivation_status": "MATCHED_TO_5193_FULL_COVARIANCE",
            },
            {
                "item": "physical_BAO_calibration",
                "formula": "alpha_phys=c/[H0 r_drag(omega_b,omega_c,mnu)]",
                "profiled_coordinate": "none",
                "derivation_status": "CAMB_BACKGROUND_DERIVED",
            },
            {
                "item": "DESI_predictions",
                "formula": (
                    "DM/rd=alpha I; DH/rd=alpha/E; "
                    "DV/rd=alpha[z I^2/E]^(1/3)"
                ),
                "profiled_coordinate": "none",
                "derivation_status": "PHYSICAL_SINGLE_CALIBRATION",
            },
            {
                "item": "growth_prediction",
                "formula": (
                    "D_NN+[2+dlnH/dN]D_N-3Omega_m D/2=0; "
                    "f sigma8=sigma8_0 D_N/D_0"
                ),
                "profiled_coordinate": "sigma8_0",
                "derivation_status": "5194_DERIVED_SUBHORIZON_LIMIT",
            },
            {
                "item": "compressed_CMB",
                "formula": (
                    "chi2=[R,lA,omega_b h2,ns]-mean with full covariance"
                ),
                "profiled_coordinate": "n_s",
                "derivation_status": "MODEL_DEPENDENT_DISTANCE_PRIOR_NONCLAIM",
            },
            {
                "item": "primary_growth_data",
                "formula": "five SDSS/eBOSS f_sigma8 rows with marginal covariance",
                "profiled_coordinate": "sigma8_0",
                "derivation_status": (
                    "AVOIDS_DESI_SDSS_BAO_DISTANCE_DOUBLE_COUNTING"
                ),
            },
            {
                "item": "full_SDSS_robustness",
                "formula": "all 14 BAO-plus rows with physical alpha",
                "profiled_coordinate": "sigma8_0 only",
                "derivation_status": (
                    "ROBUSTNESS_ONLY_CROSS_SURVEY_COVARIANCE_NOT_AVAILABLE"
                ),
            },
            {
                "item": "claim_ceiling",
                "formula": (
                    "compressed distance prior is not an official Planck/ACT/SPT "
                    "likelihood"
                ),
                "profiled_coordinate": "none",
                "derivation_status": "INTERNAL_ROBUSTNESS_NONCLAIM",
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    sources: list[tuple[str, Path, str]] = [
        *[
            (source_id, path, "locked predecessor")
            for source_id, path, _ in LOCKED_PREDECESSORS
        ],
        ("Pantheon_plus_mean", checkpoint_5193.SN_DATA, "SN mean"),
        ("Pantheon_plus_covariance", checkpoint_5193.SN_COV, "SN covariance"),
        ("DESI_DR2_BAO_mean", checkpoint_5193.BAO_DATA, "DESI mean"),
        ("DESI_DR2_BAO_covariance", checkpoint_5193.BAO_COV, "DESI covariance"),
        (
            "Planck_distance_vector",
            checkpoint_5194.PLANCK_VECTOR,
            "compressed CMB vector",
        ),
        (
            "Planck_distance_covariance",
            checkpoint_5194.PLANCK_COVARIANCE,
            "compressed CMB covariance",
        ),
        (
            "Planck_row_lock_manifest",
            checkpoint_5194.PLANCK_MANIFEST,
            "compressed CMB row lock",
        ),
        (
            "SDSS_row_lock_manifest",
            checkpoint_5194.SDSS_MANIFEST,
            "SDSS/eBOSS row lock",
        ),
        (
            "SDSS_covariance_validation",
            checkpoint_5194.SDSS_VALIDATION,
            "SDSS/eBOSS covariance validation",
        ),
        (
            "growth_source_manifest",
            checkpoint_5194.SOURCE_MANIFEST,
            "growth source manifest",
        ),
        (
            "CAMB_installed_package",
            Path(camb.__file__).resolve(),
            "physical sound horizon and background engine",
        ),
    ]
    for sample, vector_path, covariance_path in checkpoint_5194.PRIMARY_FILES:
        sources.extend(
            [
                (f"{sample}_vector", vector_path, "SDSS/eBOSS BAO-plus vector"),
                (
                    f"{sample}_covariance",
                    covariance_path,
                    "SDSS/eBOSS full covariance",
                ),
            ]
        )
    rows: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for source_id, path, role in sources:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        rows.append(
            {
                "source_id": source_id,
                "path_or_url": str(resolved),
                "exists": resolved.exists(),
                "sha256": file_digest(resolved) if resolved.exists() else "",
                "role": role,
                "extraction_method": "local source-locked file",
            }
        )
    rows.extend(
        [
            {
                "source_id": "Planck_distance_prior_paper",
                "path_or_url": "https://arxiv.org/abs/1808.05724",
                "exists": "",
                "sha256": "",
                "role": "compressed distance-prior source",
                "extraction_method": "URL recorded; local PDF source locked",
            },
            {
                "source_id": "CAMB_documentation",
                "path_or_url": "https://camb.readthedocs.io/",
                "exists": "",
                "sha256": "",
                "role": "background and sound-horizon engine documentation",
                "extraction_method": "URL recorded",
            },
        ]
    )
    return tagged(rows)


def build_document(
    primary_fits: list[dict[str, Any]],
    robustness_fits: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    forward_rows: list[dict[str, Any]],
    growth_validation: list[dict[str, Any]],
    parent_states: list[dict[str, Any]],
    identifiability: list[dict[str, Any]],
) -> str:
    primary = {fit["model"]: fit for fit in primary_fits}
    primary_lines = "\n".join(
        (
            f"| `{model}` | {primary[model]['chi2_SN']:.6f} | "
            f"{primary[model]['chi2_DESI']:.6f} | "
            f"{primary[model]['chi2_growth']:.6f} | "
            f"{primary[model]['chi2_CMB']:.6f} | "
            f"{primary[model]['chi2_total']:.6f} | "
            f"{primary[model]['AIC']:.6f} | "
            f"{primary[model]['BIC']:.6f} | "
            f"`{primary[model]['prior_edge_flag']}` |"
        )
        for model in MODEL_ORDER
    )
    parameter_lines = "\n".join(
        (
            f"| `{model}` | {primary[model]['params']['Omega_m']:.8g} | "
            f"{primary[model]['H0']:.8g} | "
            f"{primary[model]['Omega_b_h2']:.8g} | "
            f"{primary[model]['rdrag_Mpc']:.8g} | "
            f"{primary[model]['physical_alpha']:.8g} | "
            f"{primary[model]['n_s_profiled']:.8g} | "
            f"{primary[model]['sigma8_0_profiled']:.8g} |"
        )
        for model in MODEL_ORDER
    )
    primary_comparisons = [
        row
        for row in comparisons
        if row["config"] == PRIMARY_CONFIG.name
    ]
    comparison_lines = "\n".join(
        (
            f"| `{row['parent_model']}` | `{row['baseline_model']}` | "
            f"{float(row['delta_chi2_parent_minus_baseline']):.6g} | "
            f"{float(row['delta_AIC_parent_minus_baseline']):.6g} | "
            f"{float(row['delta_BIC_parent_minus_baseline']):.6g} | "
            f"`{row['parent_edge_flag']}` |"
        )
        for row in primary_comparisons
    )
    robustness_lines = "\n".join(
        (
            f"| `{fit['config']}` | `{fit['model']}` | "
            f"{fit['chi2_total']:.6f} | {fit['chi2_CMB']:.6f} | "
            f"{fit['AIC']:.6f} | {fit['BIC']:.6f} | "
            f"`{fit['prior_edge_flag']}` |"
        )
        for fit in robustness_fits
    )
    edge_lines = "\n".join(
        (
            f"| `{fit['model']}` | "
            + (
                "; ".join(
                    f"{row['parameter']}={float(row['best_fit']):.8g}"
                    for row in fit["edge_rows"]
                    if row["edge_flag"]
                )
                or "none"
            )
            + " |"
        )
        for fit in primary_fits
    )
    forward_lines = "\n".join(
        (
            f"| `{row['model']}` | "
            f"{float(row['max_relative_E_difference_z_0_to_2p5']):.3e} | "
            f"{float(row['delta_chi2_total_forward_minus_fit']):.3e} | "
            f"{float(row['delta_chi2_CMB_forward_minus_fit']):.3e} | "
            f"{float(row['fluid_minus_PPF_l_A']):.3e} | "
            f"{float(row['forward_max_constraint_residual']):.3e} |"
        )
        for row in forward_rows
    )
    maximum_growth_integrator_difference = max(
        float(row["max_abs_fractional_fast_vs_DOP853"])
        for row in growth_validation
    )
    parent_state_lines = "\n".join(
        (
            f"| `{row['model']}` | "
            f"{float(row['mu_mgap_over_H0']):.8g} | "
            f"{float(row['Omega_scalar_0']):.8g} | "
            f"{float(row['Omega_Lambda_0']):.8g} | "
            f"{float(row['theta_0']):.8g} | "
            f"{float(row['w_dark_effective_0']):.8g} |"
        )
        for row in parent_states
    )
    identifiability_lines = "\n".join(
        (
            f"| `{row['model']}` | "
            f"{float(row['minimum_Hessian_eigenvalue']):.6g} | "
            f"{float(row['Hessian_condition_number']):.6g} | "
            f"{float(row['sigma_log10_mu_local_Gaussian']):.6g} | "
            + (
                f"{float(row['sigma_f_scalar_local_Gaussian']):.6g}"
                if row["sigma_f_scalar_local_Gaussian"] != ""
                else ""
            )
            + " | "
            + (
                f"{float(row['corr_log10_mu_f_scalar']):.6g}"
                if row["corr_log10_mu_f_scalar"] != ""
                else ""
            )
            + f" | `{row['identifiability_status']}` |"
        )
        for row in identifiability
    )
    free_vs_cpl = next(
        row
        for row in primary_comparisons
        if row["parent_model"] == "ParentScalar_Lambda_free"
        and row["baseline_model"] == "CPL"
    )
    zero_vs_wcdm = next(
        row
        for row in primary_comparisons
        if row["parent_model"] == "ParentScalar_Lambda_zero"
        and row["baseline_model"] == "wCDM"
    )
    zero_vs_lcdm = next(
        row
        for row in primary_comparisons
        if row["parent_model"] == "ParentScalar_Lambda_zero"
        and row["baseline_model"] == "LCDM"
    )
    zero_vs_cpl = next(
        row
        for row in primary_comparisons
        if row["parent_model"] == "ParentScalar_Lambda_zero"
        and row["baseline_model"] == "CPL"
    )
    best_aic = min(primary_fits, key=lambda fit: fit["AIC"])
    best_bic = min(primary_fits, key=lambda fit: fit["BIC"])
    parent_edge_models = [
        fit["model"] for fit in primary_fits
        if fit["model"] in PARENT_MODELS and fit["prior_edge_flag"]
    ]
    parent_edge_text = (
        ", ".join(parent_edge_models) if parent_edge_models else "none"
    )
    runtime_seconds = sum(
        fit["runtime_seconds"] for fit in primary_fits + robustness_fits
    )
    return f"""# 5195 - Matched Joint CMB-Informed Parent Refit and Physical Sound-Horizon Gate

Private derivation and empirical robustness checkpoint. This is not an
official CMB likelihood and not a public MTS cosmology-support claim.

Checkpoint marker: `{MARKER}`.

## 1. The calculation that 5194 required

Checkpoint 5194 found a real compressed-CMB discrepancy after freezing the
5193 late parameters and profiling only `H0`. Checkpoint 5195 does not write
that down as another missing target. It refits all five models under one
matched likelihood:

```text
Pantheon+ noncalibrator rows       = 1624, full STAT+SYS covariance;
DESI DR2 BAO rows                  = 13, full covariance;
primary SDSS/eBOSS growth rows     = 5 f sigma8 rows;
compressed CMB rows                = 4, full covariance;
total primary rows                 = 1646;
SH0ES/local-H0 calibration         = absent.
```

The primary growth score retains only the marginal `f sigma8` rows. This
avoids pretending that DESI DR2 and legacy SDSS/eBOSS BAO distance vectors
have a known zero cross-survey covariance. The 14-row SDSS BAO-plus vector is
still refitted as a labelled robustness branch.

## 2. One physical distance calibration

The independent BAO nuisance used in 5193 and 5194 is removed. CAMB
`{camb.__version__}` computes `r_drag` from the fitted physical baryon and
cold-matter densities, and every DESI/SDSS distance uses

```text
alpha_phys = c/(H0 r_drag),
DM/rd = alpha_phys integral_0^z dz/E,
DH/rd = alpha_phys/E,
DV/rd = alpha_phys[z(integral_0^z dz/E)^2/E]^(1/3).
```

The only analytic nuisance coordinates are the Pantheon+ offset, `n_s` inside
the full compressed-CMB covariance, and `sigma8_0` when growth is present.
No independent `BAO alpha` remains.

## 3. Matched primary result

| model | SN chi2 | DESI chi2 | growth chi2 | CMB chi2 | total chi2 | AIC | BIC | edge |
|---|---:|---:|---:|---:|---:|---:|---:|---|
{primary_lines}

The physical calibration coordinates are:

| model | Omega_m | H0 | Omega_b h2 | r_drag Mpc | c/(H0 r_drag) | n_s | sigma8_0 |
|---|---:|---:|---:|---:|---:|---:|---:|
{parameter_lines}

The lowest primary AIC is `{best_aic['model']}` and the lowest primary BIC is
`{best_bic['model']}`. This statement is bookkeeping, not a claim that a
compressed distance prior is equivalent to the official Planck likelihood.

The frozen-parameter CMB values from 5194 were `42.5497` and `37.2861` for
the free- and zero-Lambda parents. After the matched refit they are
`{primary['ParentScalar_Lambda_free']['chi2_CMB']:.6g}` and
`{primary['ParentScalar_Lambda_zero']['chi2_CMB']:.6g}`. The earlier pressure
is therefore absorbed without a prior edge, but only inside this compressed
diagnostic.

## 4. Like-for-like model comparisons

| parent | baseline | delta chi2 | delta AIC | delta BIC | parent edge |
|---|---|---:|---:|---:|---|
{comparison_lines}

Negative differences favour the parent. Absolute information-criterion
differences below two are treated as draw-scale. The equal-count free-parent
versus CPL comparison gives

```text
delta AIC={float(free_vs_cpl['delta_AIC_parent_minus_baseline']):.9g},
delta BIC={float(free_vs_cpl['delta_BIC_parent_minus_baseline']):.9g}.
```

The equal-count zero-Lambda-parent versus wCDM comparison gives

```text
delta AIC={float(zero_vs_wcdm['delta_AIC_parent_minus_baseline']):.9g},
delta BIC={float(zero_vs_wcdm['delta_BIC_parent_minus_baseline']):.9g}.
```

Thus the zero-Lambda parent is the cleaner surviving parent candidate. It is
within
`{float(zero_vs_cpl['delta_AIC_parent_minus_baseline']):.6g}` AIC units of the
lowest-AIC CPL fit, while its BIC is
`{float(zero_vs_lcdm['delta_BIC_parent_minus_baseline']):.6g}` above the
lowest-BIC LCDM fit. This is competitive/draw-scale under AIC and moderate
LCDM preference under BIC, not a universal model-selection victory.

Any comparison whose parent row hits a prior edge remains unstable evidence,
even if its raw information criterion is favourable.

## 5. Edge and identifiability audit

| primary model | edge coordinates |
|---|---|
{edge_lines}

Parent models with an edge flag: `{parent_edge_text}`. The wide-mass
robustness branch below distinguishes a genuine finite optimum from a fit
that merely runs toward the LambdaCDM-like `mu -> 0` limit.

The fitted parent states are:

| parent | mu=m_gap/H0 | Omega_scalar,0 | Omega_Lambda,0 | theta_0 | w_dark,0 |
|---|---:|---:|---:|---:|---:|
{parent_state_lines}

These are empirical coordinates of a parent-owned model, not a derivation of
the mass gap or homogeneous state.

The local finite-difference Hessian in prior-normalized coordinates gives:

| parent | min eigenvalue | condition | sigma(log10 mu) | sigma(f_scalar) | corr(log10 mu,f) | status |
|---|---:|---:|---:|---:|---:|---|
{identifiability_lines}

Both optima have positive local curvature. The free-Lambda mass/state split
remains weak and correlated; the zero-Lambda branch is substantially cleaner.
These Gaussian curvature numbers are not posterior intervals.

## 6. Robustness matrix

| configuration | model | total chi2 | CMB chi2 | AIC | BIC | edge |
|---|---|---:|---:|---:|---:|---|
{robustness_lines}

The matrix includes the full 14-row SDSS BAO-plus vector, the alternative
LCDM compressed-prior table, a no-growth refit, and a parent-only mass prior
extended to `log10(mu)=-4`. The full-SDSS row is explicitly nonclaim because
the unavailable DESI/SDSS cross-survey covariance is not fabricated.

## 7. Exact forward-parent validation

Optimization uses the fast regular phase shoot at `N=-7`. Each primary parent
optimum is then rebuilt from the `N=-12` radiation-era regular series and
rescored:

| parent | max relative E difference | delta total chi2 | delta CMB chi2 | fluid-PPF delta l_A | max constraint |
|---|---:|---:|---:|---:|---:|
{forward_lines}

This verifies that the optimization shortcut did not create the result. The
fluid-versus-PPF column is a numerical implementation comparator; PPF is not
substituted for the canonical parent derivation.

The fixed-grid growth integrator used during optimization is independently
compared with the checkpoint-5194 high-accuracy DOP853 solution at every
observed growth redshift. Its largest fractional difference across all five
primary best fits is

```text
{maximum_growth_integrator_difference:.6e}.
```

## 8. Interpretation ceiling

The compressed vector is model-dependent. The wCDM table is used identically
for all primary rows, and the LCDM table is a robustness rerun. That is a fair
internal pressure test, but it cannot establish an official CMB pass or
failure for a new dynamic field.

```text
physical H0-r_drag calibration        = implemented;
all five models jointly refitted      = yes;
same covariance and nuisance rules    = yes;
independent BAO scale                  = removed;
parent forward regular branch checked = yes;
official Planck/ACT/SPT likelihood    = no;
cosmology-support claim               = false;
full MTS unification claim            = false.
```

The next physics decision follows the actual fit. An interior competitive
parent branch earns an official-likelihood-ready implementation. An
edge-driven `mu -> 0` or `f_scalar -> 0` result does not: it sends the work
back to deriving the parent mass/state selection law and calibrated source
coupling before spending an official-likelihood run on an unselected branch.
Either way, the current cosmology discrepancy has now been calculated rather
than circulated as an unsigned target.

This result is the interior case. The next cosmology gate is therefore an
official-likelihood-ready implementation. The higher-priority field-theory
target remains derivation of the finite `m_gap/H0` and homogeneous-state
selection from the parent `J_gap`/source-coupling structure; the fitted values
cannot be promoted as fundamental constants until that derivation exists.

## 9. Machine artifacts

- `source-intake/functional_rg/5195/likelihood_contract.csv`
- `source-intake/functional_rg/5195/joint_fit_summary.csv`
- `source-intake/functional_rg/5195/joint_fit_parameters.csv`
- `source-intake/functional_rg/5195/prior_edge_audit.csv`
- `source-intake/functional_rg/5195/model_comparisons.csv`
- `source-intake/functional_rg/5195/physical_sound_horizon_calibration.csv`
- `source-intake/functional_rg/5195/compressed_CMB_predictions.csv`
- `source-intake/functional_rg/5195/growth_residuals.csv`
- `source-intake/functional_rg/5195/growth_integrator_validation.csv`
- `source-intake/functional_rg/5195/parent_forward_validation.csv`
- `source-intake/functional_rg/5195/parent_state_summary.csv`
- `source-intake/functional_rg/5195/parent_local_identifiability.csv`
- `source-intake/functional_rg/5195/source_provenance.csv`
- `source-intake/functional_rg/5195/joint_CMB_informed_refit_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5195_VALIDATION.csv`

Total optimizer runtime recorded across the fit matrix is
`{runtime_seconds:.3f}` seconds.
"""


def public_worktree_state() -> tuple[str, bool, str]:
    safe_path = PUBLIC_WORKTREE.as_posix()
    head = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(PUBLIC_WORKTREE),
            "rev-parse",
            "HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_path}",
            "-C",
            str(PUBLIC_WORKTREE),
            "status",
            "--porcelain",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return head, not bool(status.strip()), status


def validation_rows(
    primary_fits: list[dict[str, Any]],
    robustness_fits: list[dict[str, Any]],
    forward_rows: list[dict[str, Any]],
    growth_validation: list[dict[str, Any]],
    parent_states: list[dict[str, Any]],
    identifiability: list[dict[str, Any]],
    calibration_rows: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    for source_id, path, expected_hash in LOCKED_PREDECESSORS:
        actual_hash = file_digest(path) if path.exists() else ""
        checks.append(
            (
                f"{source_id}_lock",
                path.exists() and actual_hash == expected_hash,
                f"expected={expected_hash};actual={actual_hash}",
            )
        )
    formal_hash = tree_digest(FORMAL)
    checks.append(
        (
            "formalization_workbench_unchanged",
            formal_hash == FORMAL_LOCK,
            f"expected={FORMAL_LOCK};actual={formal_hash}",
        )
    )
    checkpoint_5176_hash = tree_digest(CHECKPOINT_5176)
    checks.append(
        (
            "checkpoint_5176_unchanged",
            checkpoint_5176_hash == CHECKPOINT_5176_LOCK,
            (
                f"expected={CHECKPOINT_5176_LOCK};"
                f"actual={checkpoint_5176_hash}"
            ),
        )
    )
    local_provenance = [
        row for row in provenance if row["exists"] != ""
    ]
    checks.append(
        (
            "all_local_provenance_exists",
            all(bool(row["exists"]) and bool(row["sha256"]) for row in local_provenance),
            f"local_sources={len(local_provenance)}",
        )
    )
    primary_by_model = {fit["model"]: fit for fit in primary_fits}
    checks.append(
        (
            "all_primary_models_present",
            set(primary_by_model) == set(MODEL_ORDER),
            f"models={sorted(primary_by_model)}",
        )
    )
    checks.append(
        (
            "all_primary_fits_converged",
            all(fit["convergence"] for fit in primary_fits),
            ";".join(
                f"{fit['model']}={fit['convergence']}"
                for fit in primary_fits
            ),
        )
    )
    checks.append(
        (
            "all_primary_scores_finite",
            all(
                math.isfinite(float(fit[key]))
                for fit in primary_fits
                for key in (
                    "chi2_SN",
                    "chi2_DESI",
                    "chi2_growth",
                    "chi2_CMB",
                    "chi2_total",
                    "AIC",
                    "BIC",
                )
            ),
            f"fit_count={len(primary_fits)}",
        )
    )
    checks.append(
        (
            "primary_row_count_matched",
            all(fit["n"] == 1646 for fit in primary_fits),
            ";".join(f"{fit['model']}={fit['n']}" for fit in primary_fits),
        )
    )
    checks.append(
        (
            "single_physical_sound_horizon_calibration",
            all(
                not bool(row["independent_BAO_alpha_profiled"])
                and float(row["absolute_reconstruction_error"]) < 1.0e-12
                for row in calibration_rows
            ),
            f"rows={len(calibration_rows)}",
        )
    )
    checks.append(
        (
            "physical_rdrag_range",
            all(130.0 < fit["rdrag_Mpc"] < 170.0 for fit in primary_fits),
            ";".join(
                f"{fit['model']}={fit['rdrag_Mpc']:.6g}"
                for fit in primary_fits
            ),
        )
    )
    checks.append(
        (
            "profiled_nuisances_interior",
            all(
                not fit["sigma8_0_profiled"] is None
                and SIGMA8_BOUNDS[0] < fit["sigma8_0_profiled"] < SIGMA8_BOUNDS[1]
                and NS_BOUNDS[0] < fit["n_s_profiled"] < NS_BOUNDS[1]
                for fit in primary_fits
            ),
            "primary n_s and sigma8 profiles",
        )
    )
    checks.append(
        (
            "robustness_matrix_complete",
            len(robustness_fits) == 17,
            f"rows={len(robustness_fits)};expected=17",
        )
    )
    checks.append(
        (
            "robustness_scores_finite",
            all(math.isfinite(fit["chi2_total"]) for fit in robustness_fits),
            f"rows={len(robustness_fits)}",
        )
    )
    checks.append(
        (
            "parent_forward_rows_complete",
            len(forward_rows) == 2,
            f"rows={len(forward_rows)}",
        )
    )
    checks.append(
        (
            "parent_forward_background_agreement",
            all(
                abs(float(row["max_relative_E_difference_z_0_to_2p5"]))
                < 2.0e-3
                and abs(float(row["delta_chi2_total_forward_minus_fit"]))
                < 1.0
                and abs(float(row["forward_max_constraint_residual"]))
                < 1.0e-8
                for row in forward_rows
            ),
            ";".join(
                (
                    f"{row['model']}:dE="
                    f"{float(row['max_relative_E_difference_z_0_to_2p5']):.3e},"
                    f"dchi2={float(row['delta_chi2_total_forward_minus_fit']):.3e}"
                )
                for row in forward_rows
            ),
        )
    )
    checks.append(
        (
            "parent_fluid_PPF_background_agreement",
            all(
                abs(float(row["fluid_minus_PPF_l_A"])) < 1.0e-6
                and abs(float(row["fluid_minus_PPF_R"])) < 1.0e-8
                for row in forward_rows
            ),
            "CAMB background implementation comparator",
        )
    )
    checks.append(
        (
            "fast_growth_integrator_matches_reference",
            len(growth_validation) == len(MODEL_ORDER)
            and all(
                float(row["max_abs_fractional_fast_vs_DOP853"]) < 1.0e-5
                for row in growth_validation
            ),
            ";".join(
                (
                    f"{row['model']}="
                    f"{float(row['max_abs_fractional_fast_vs_DOP853']):.3e}"
                )
                for row in growth_validation
            ),
        )
    )
    checks.append(
        (
            "parent_state_rows_finite_and_interior",
            len(parent_states) == 2
            and all(
                math.isfinite(float(row["mu_mgap_over_H0"]))
                and float(row["mu_mgap_over_H0"]) > 0.0
                and math.isfinite(float(row["w_dark_effective_0"]))
                and abs(float(row["maximum_constraint_residual"])) < 1.0e-8
                for row in parent_states
            ),
            ";".join(
                (
                    f"{row['model']}:mu="
                    f"{float(row['mu_mgap_over_H0']):.6g}"
                )
                for row in parent_states
            ),
        )
    )
    checks.append(
        (
            "parent_local_Hessian_positive",
            len(identifiability) == 2
            and all(
                bool(row["positive_local_curvature"])
                and float(row["minimum_Hessian_eigenvalue"]) > 0.0
                and math.isfinite(float(row["Hessian_condition_number"]))
                for row in identifiability
            ),
            ";".join(
                (
                    f"{row['model']}:min="
                    f"{float(row['minimum_Hessian_eigenvalue']):.3e},"
                    f"cond={float(row['Hessian_condition_number']):.3e}"
                )
                for row in identifiability
            ),
        )
    )
    checks.append(
        (
            "no_official_CMB_claim",
            all(not fit["official_CMB_likelihood"] for fit in primary_fits + robustness_fits),
            "all fit rows explicitly non-official",
        )
    )
    checks.append(
        (
            "no_cosmology_support_claim",
            all(
                fit["claim_status"]
                == "MATCHED_COMPRESSED_CMB_REFIT_INTERNAL_NONCLAIM"
                for fit in primary_fits + robustness_fits
            ),
            "claim ceiling retained",
        )
    )
    output_parse_status = True
    output_detail: list[str] = []
    for path in output_paths:
        if not path.exists():
            output_parse_status = False
            output_detail.append(f"missing={path.name}")
            continue
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as handle:
                row_count = sum(1 for _ in csv.DictReader(handle))
            output_parse_status &= row_count > 0
            output_detail.append(f"{path.name}={row_count}")
    checks.append(
        (
            "all_machine_outputs_parse",
            output_parse_status,
            ";".join(output_detail),
        )
    )
    head, public_clean, public_status = public_worktree_state()
    checks.extend(
        [
            (
                "public_worktree_head_unchanged",
                head == PUBLIC_HEAD_LOCK,
                f"expected={PUBLIC_HEAD_LOCK};actual={head}",
            ),
            (
                "public_worktree_clean",
                public_clean,
                public_status or "clean",
            ),
            (
                "no_script_pycache",
                not (POST / "scripts" / "__pycache__").exists(),
                str(POST / "scripts" / "__pycache__"),
            ),
        ]
    )
    return tagged(
        [
            {
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
            for check, passed, detail in checks
        ]
    )


def dry_run(data: JointData, predecessor: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    for model in MODEL_ORDER:
        params = {
            key: float(value)
            for key, value in predecessor["scores"][model]["params"].items()
        }
        params["H0"] = 67.8
        params["Omega_b_h2"] = 0.02239
        if model == "ParentScalar_Lambda_zero":
            params["f_scalar"] = 1.0
        score = score_model(model, params, data, PRIMARY_CONFIG)
        rows.append(
            {
                "model": model,
                "chi2": score["chi2_total"],
                "H0": params["H0"],
                "rdrag": score["rdrag_Mpc"],
                "alpha": score["physical_alpha"],
            }
        )
    print(
        json.dumps(
            {
                "status": "DRY_RUN_PASS",
                "checkpoint": 5195,
                "rows": rows,
            },
            indent=2,
        )
    )


def validate_saved_result(data: JointData) -> None:
    result_path = OUT / "joint_CMB_informed_refit_results.json"
    if not result_path.exists():
        raise FileNotFoundError(result_path)
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    all_fits = payload["fits"]
    primary_fits = [
        fit for fit in all_fits if fit["config"] == PRIMARY_CONFIG.name
    ]
    robustness_fits = [
        fit for fit in all_fits if fit["config"] != PRIMARY_CONFIG.name
    ]
    fit_sets: dict[str, list[dict[str, Any]]] = {}
    for fit in all_fits:
        fit_sets.setdefault(fit["config"], []).append(fit)
    comparisons = comparison_rows(fit_sets)
    forward_rows = payload["forward_validation"]
    growth_validation = growth_integrator_validation_rows(
        primary_fits,
        data,
    )
    parent_states = parent_state_rows(primary_fits)
    identifiability = parent_identifiability_rows(primary_fits, data)
    calibration = physical_calibration_rows(all_fits)
    provenance = provenance_rows()
    write_csv(
        OUT / "model_comparisons.csv",
        comparisons,
    )
    write_csv(
        OUT / "physical_sound_horizon_calibration.csv",
        calibration,
    )
    write_csv(
        OUT / "growth_integrator_validation.csv",
        growth_validation,
    )
    write_csv(
        OUT / "parent_state_summary.csv",
        parent_states,
    )
    write_csv(
        OUT / "parent_local_identifiability.csv",
        identifiability,
    )
    write_csv(
        OUT / "source_provenance.csv",
        provenance,
    )
    DOCUMENT.write_text(
        build_document(
            primary_fits,
            robustness_fits,
            comparisons,
            forward_rows,
            growth_validation,
            parent_states,
            identifiability,
        ),
        encoding="utf-8",
    )
    payload["growth_integrator_validation"] = growth_validation
    payload["parent_state_summary"] = parent_states
    payload["parent_local_identifiability"] = identifiability
    write_json(result_path, payload)
    expected_files = (
        "likelihood_contract.csv",
        "joint_fit_summary.csv",
        "joint_fit_parameters.csv",
        "prior_edge_audit.csv",
        "model_comparisons.csv",
        "physical_sound_horizon_calibration.csv",
        "compressed_CMB_predictions.csv",
        "growth_residuals.csv",
        "growth_integrator_validation.csv",
        "parent_forward_validation.csv",
        "parent_state_summary.csv",
        "parent_local_identifiability.csv",
        "source_provenance.csv",
    )
    output_paths = [OUT / filename for filename in expected_files]
    output_paths.append(result_path)
    validation = validation_rows(
        primary_fits,
        robustness_fits,
        forward_rows,
        growth_validation,
        parent_states,
        identifiability,
        calibration,
        provenance,
        output_paths,
    )
    write_csv(VALIDATION, validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "5195 validation failed: "
            + "; ".join(row["check"] for row in failed)
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "checkpoint": 5195,
                "mode": "validate-only",
                "validation_rows": len(validation),
                "result": str(result_path),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "smoke", "full", "validate-only"),
        default="full",
    )
    args = parser.parse_args()
    data = load_joint_data()
    predecessor = json.loads(RESULT_5193.read_text(encoding="utf-8"))
    if args.mode == "validate-only":
        validate_saved_result(data)
        return
    if args.mode == "dry-run":
        dry_run(data, predecessor)
        return
    if args.mode == "smoke":
        smoke_fits = run_fit_set(
            PRIMARY_CONFIG,
            data,
            predecessor,
            seeds=None,
            multistart=False,
            models=("LCDM", "ParentScalar_Lambda_zero"),
        )
        print(
            json.dumps(
                {
                    "status": "SMOKE_PASS",
                    "checkpoint": 5195,
                    "fits": [
                        {
                            "model": fit["model"],
                            "chi2": fit["chi2_total"],
                            "params": fit["params"],
                            "edge": fit["prior_edge_flag"],
                        }
                        for fit in smoke_fits
                    ],
                },
                indent=2,
            )
        )
        return

    primary_fits = run_fit_set(
        PRIMARY_CONFIG,
        data,
        predecessor,
        seeds=None,
        multistart=True,
    )
    primary_seeds = {
        fit["model"]: dict(fit["params"]) for fit in primary_fits
    }
    full_sdss_fits = run_fit_set(
        FULL_SDSS_CONFIG,
        data,
        predecessor,
        seeds=primary_seeds,
        multistart=False,
    )
    lcdm_prior_fits = run_fit_set(
        LCDM_PRIOR_CONFIG,
        data,
        predecessor,
        seeds=primary_seeds,
        multistart=False,
    )
    no_growth_fits = run_fit_set(
        NO_GROWTH_CONFIG,
        data,
        predecessor,
        seeds=primary_seeds,
        multistart=False,
    )
    wide_parent_fits = run_fit_set(
        WIDE_PARENT_CONFIG,
        data,
        predecessor,
        seeds=primary_seeds,
        multistart=False,
        models=PARENT_MODELS,
    )
    robustness_fits = (
        full_sdss_fits
        + lcdm_prior_fits
        + no_growth_fits
        + wide_parent_fits
    )
    fit_sets = {
        PRIMARY_CONFIG.name: primary_fits,
        FULL_SDSS_CONFIG.name: full_sdss_fits,
        LCDM_PRIOR_CONFIG.name: lcdm_prior_fits,
        NO_GROWTH_CONFIG.name: no_growth_fits,
        WIDE_PARENT_CONFIG.name: wide_parent_fits,
    }
    all_fits = primary_fits + robustness_fits
    comparisons = comparison_rows(fit_sets)
    forward_rows = forward_validation_rows(primary_fits, data)
    growth_validation = growth_integrator_validation_rows(
        primary_fits,
        data,
    )
    parent_states = parent_state_rows(primary_fits)
    identifiability = parent_identifiability_rows(primary_fits, data)
    calibration = physical_calibration_rows(all_fits)
    provenance = provenance_rows()
    output_rows: dict[str, list[dict[str, Any]]] = {
        "likelihood_contract.csv": likelihood_contract_rows(),
        "joint_fit_summary.csv": fit_summary_rows(all_fits),
        "joint_fit_parameters.csv": parameter_rows(all_fits),
        "prior_edge_audit.csv": tagged(
            [
                row
                for fit in all_fits
                for row in fit["edge_rows"]
            ]
        ),
        "model_comparisons.csv": comparisons,
        "physical_sound_horizon_calibration.csv": calibration,
        "compressed_CMB_predictions.csv": cmb_prediction_rows(all_fits, data),
        "growth_residuals.csv": growth_residual_rows(
            primary_fits + full_sdss_fits + lcdm_prior_fits
        ),
        "growth_integrator_validation.csv": growth_validation,
        "parent_forward_validation.csv": forward_rows,
        "parent_state_summary.csv": parent_states,
        "parent_local_identifiability.csv": identifiability,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for filename, rows in output_rows.items():
        path = OUT / filename
        write_csv(path, rows)
        output_paths.append(path)
    document_text = build_document(
        primary_fits,
        robustness_fits,
        comparisons,
        forward_rows,
        growth_validation,
        parent_states,
        identifiability,
    )
    DOCUMENT.write_text(document_text, encoding="utf-8")
    result_path = OUT / "joint_CMB_informed_refit_results.json"
    serializable_fits = [
        {
            key: value
            for key, value in fit.items()
            if key not in {"growth_residual_rows"}
        }
        for fit in all_fits
    ]
    write_json(
        result_path,
        {
            "checkpoint": 5195,
            "marker": MARKER,
            "CAMB_version": camb.__version__,
            "primary_config": PRIMARY_CONFIG.__dict__,
            "fit_sets": {
                name: [fit["model"] for fit in fits]
                for name, fits in fit_sets.items()
            },
            "fits": serializable_fits,
            "forward_validation": forward_rows,
            "growth_integrator_validation": growth_validation,
            "parent_state_summary": parent_states,
            "parent_local_identifiability": identifiability,
            "claim_status": "INTERNAL_MATCHED_COMPRESSED_CMB_NONCLAIM",
            "official_CMB_likelihood": False,
        },
    )
    output_paths.append(result_path)
    validation = validation_rows(
        primary_fits,
        robustness_fits,
        forward_rows,
        growth_validation,
        parent_states,
        identifiability,
        calibration,
        provenance,
        output_paths,
    )
    write_csv(VALIDATION, validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "5195 validation failed: "
            + "; ".join(row["check"] for row in failed)
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "checkpoint": 5195,
                "result": str(result_path),
                "validation_rows": len(validation),
                "generated_files": len(output_paths) + 2,
                "primary": {
                    fit["model"]: {
                        "chi2": fit["chi2_total"],
                        "AIC": fit["AIC"],
                        "BIC": fit["BIC"],
                        "edge": fit["prior_edge_flag"],
                    }
                    for fit in primary_fits
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
