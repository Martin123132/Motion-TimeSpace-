from __future__ import annotations

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
from scipy import integrate, interpolate, linalg, optimize


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5194"
DOCUMENT = (
    POST
    / "5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-"
    "compressed-CMB-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5194_VALIDATION.csv"
)

MARKER = "MTS_5194_PARENT_CANONICAL_SCALAR_PERTURBATION_GROWTH_CMB"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"

RESULT_5193 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5193"
    / "direct_parent_scalar_likelihood_results.json"
)
BACKGROUND_5193 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5193"
    / "parent_scalar_background.csv"
)
DOCUMENT_5193 = (
    POST
    / "5193-Y5-R2FR-direct-parent-scalar-Pantheon-DESI-likelihood-and-"
    "model-selection-gate.md"
)
SCRIPT_5193 = (
    POST
    / "scripts"
    / "Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood.py"
)
VALIDATION_5193 = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5193_VALIDATION.csv"
)

LOCKED_5193 = (
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
)

GROWTH_ROOT = (
    FORMAL / "data" / "cosmology" / "growth_CMB" / "sdss_eboss_dr16"
)
BAO_PLUS_ROOT = GROWTH_ROOT / "BAO-plus"
FULL_SHAPE_ROOT = GROWTH_ROOT / "Full-shape-only"
PLANCK_ROOT = (
    FORMAL / "data" / "cosmology" / "growth_CMB" / "planck2018_distance_priors"
)
PLANCK_VECTOR = PLANCK_ROOT / "planck2018_distance_prior_vector.csv"
PLANCK_COVARIANCE = PLANCK_ROOT / "planck2018_distance_prior_covariance.csv"
PLANCK_MANIFEST = PLANCK_ROOT / "row_lock_manifest.json"
SDSS_MANIFEST = GROWTH_ROOT / "row_lock_manifest.json"
SDSS_VALIDATION = GROWTH_ROOT / "covariance_validation.csv"
SOURCE_MANIFEST = GROWTH_ROOT.parent / "source_manifest.csv"

PRIMARY_FILES = (
    (
        "MGS",
        BAO_PLUS_ROOT / "sdss_MGS_FSBAO_DVfs8.txt",
        BAO_PLUS_ROOT / "sdss_MGS_FSBAO_DVfs8_covtot.txt",
    ),
    (
        "BOSS_DR12_LRG",
        BAO_PLUS_ROOT / "sdss_DR12_LRG_FSBAO_DMDHfs8.txt",
        BAO_PLUS_ROOT / "sdss_DR12_LRG_FSBAO_DMDHfs8_covtot.txt",
    ),
    (
        "eBOSS_DR16_LRG",
        BAO_PLUS_ROOT / "sdss_DR16_LRG_FSBAO_DMDHfs8.txt",
        BAO_PLUS_ROOT / "sdss_DR16_LRG_FSBAO_DMDHfs8_covtot.txt",
    ),
    (
        "eBOSS_DR16_QSO",
        BAO_PLUS_ROOT / "sdss_DR16_QSO_FSBAO_DMDHfs8.txt",
        BAO_PLUS_ROOT / "sdss_DR16_QSO_FSBAO_DMDHfs8_covtot.txt",
    ),
)

FULL_SHAPE_FILES = (
    (
        "BOSS_DR12_LRG",
        FULL_SHAPE_ROOT / "sdss_DR12_LRG_FS_DMDHfs8.txt",
        FULL_SHAPE_ROOT / "sdss_DR12_LRG_FS_DMDHfs8_covtot.txt",
    ),
    (
        "eBOSS_DR16_LRG",
        FULL_SHAPE_ROOT / "sdss_DR16_LRG_FS_DMDHfs8.txt",
        FULL_SHAPE_ROOT / "sdss_DR16_LRG_FS_DMDHfs8_covtot.txt",
    ),
    (
        "eBOSS_DR16_QSO",
        FULL_SHAPE_ROOT / "sdss_DR16_QSO_FS_DMDHfs8.txt",
        FULL_SHAPE_ROOT / "sdss_DR16_QSO_FS_DMDHfs8_covtot.txt",
    ),
)

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

OMEGA_R = 9.0e-5
N_BACKGROUND_START = -12.0
N_GROWTH_START = -7.0
CAMB_A_MIN = 1.0e-5
CAMB_W_FLOOR = 1.0e-4
CAMB_LMAX = 800
CAMB_KMAX_MPC = 0.3
H0_PRIOR_BOUNDS = (50.0, 90.0)
C_KM_S = 299792.458
OMBH2 = 0.02239
NS = 0.9653
TAU = 0.0544
AS = 2.1e-9
MNU_EV = 0.06
NEUTRINO_PHYSICAL_DENSITY_APPROX = MNU_EV / 93.14
RSD_K_H_VALUES = np.asarray([0.01, 0.02, 0.05, 0.1], dtype=float)
RSD_Z_VALUES = np.asarray([0.0, 0.15, 0.38, 0.51, 0.698, 1.0, 1.48])


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


@dataclass
class Background:
    model: str
    omega_m: float
    parameters: dict[str, float]
    n_grid: np.ndarray
    e_grid: np.ndarray
    h_grid: np.ndarray
    w_dark_grid: np.ndarray
    omega_dark_grid: np.ndarray
    parent_owned: bool
    scalar_rows: list[dict[str, Any]]
    parent_diagnostics: dict[str, Any]

    def values_at_n(
        self,
        n_values: np.ndarray | float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        values = np.asarray(n_values, dtype=float)
        e_values = np.interp(values, self.n_grid, self.e_grid)
        h_values = np.interp(values, self.n_grid, self.h_grid)
        w_values = np.interp(values, self.n_grid, self.w_dark_grid)
        omega_values = np.interp(values, self.n_grid, self.omega_dark_grid)
        return e_values, h_values, w_values, omega_values

    def e_at_z(self, redshift: float | np.ndarray) -> np.ndarray:
        redshifts = np.asarray(redshift, dtype=float)
        n_values = -np.log1p(redshifts)
        return self.values_at_n(n_values)[0]


@dataclass
class DataBlock:
    sample: str
    rows: list[tuple[float, float, str]]
    covariance: np.ndarray
    vector_path: Path
    covariance_path: Path


def load_5193_result() -> dict[str, Any]:
    return json.loads(RESULT_5193.read_text(encoding="utf-8"))


def baseline_background(
    model: str,
    score: dict[str, Any],
    n_grid: np.ndarray,
) -> Background:
    parameters = {
        key: float(value) for key, value in score["params"].items()
    }
    omega_m = parameters["Omega_m"]
    scale_factor = np.exp(n_grid)
    matter = omega_m * scale_factor**-3
    radiation = OMEGA_R * scale_factor**-4
    omega_dark_zero = 1.0 - omega_m - OMEGA_R
    if model == "LCDM":
        dark = np.full_like(n_grid, omega_dark_zero)
        w_dark = np.full_like(n_grid, -1.0)
    elif model == "wCDM":
        w_value = parameters["w"]
        dark = omega_dark_zero * scale_factor ** (-3.0 * (1.0 + w_value))
        w_dark = np.full_like(n_grid, w_value)
    elif model == "CPL":
        w_zero = parameters["w0"]
        w_a = parameters["wa"]
        w_dark = w_zero + w_a * (1.0 - scale_factor)
        dark = omega_dark_zero * scale_factor ** (-3.0 * (1.0 + w_zero + w_a))
        dark *= np.exp(-3.0 * w_a * (1.0 - scale_factor))
    else:
        raise ValueError(f"unsupported baseline model {model}")
    e_squared = matter + radiation + dark
    omega_m_n = matter / e_squared
    omega_r_n = radiation / e_squared
    omega_dark_n = dark / e_squared
    h_grid = (
        -1.5 * omega_m_n
        - 2.0 * omega_r_n
        - 1.5 * (1.0 + w_dark) * omega_dark_n
    )
    return Background(
        model=model,
        omega_m=omega_m,
        parameters=parameters,
        n_grid=n_grid,
        e_grid=np.sqrt(e_squared),
        h_grid=h_grid,
        w_dark_grid=w_dark,
        omega_dark_grid=omega_dark_n,
        parent_owned=False,
        scalar_rows=[],
        parent_diagnostics={},
    )


def parent_scalar_background(
    model: str,
    score: dict[str, Any],
    n_grid: np.ndarray,
) -> Background:
    parameters = {
        key: float(value) for key, value in score["params"].items()
    }
    omega_m = parameters["Omega_m"]
    scalar_fraction = parameters["f_scalar"]
    mu_value = 10.0 ** parameters["log10_mu"]
    dark_density = 1.0 - omega_m - OMEGA_R
    omega_scalar_zero = scalar_fraction * dark_density
    omega_lambda = (1.0 - scalar_fraction) * dark_density

    def e_squared(n_value: float, chi_value: float, x_value: float) -> float:
        numerator = (
            omega_m * math.exp(-3.0 * n_value)
            + OMEGA_R * math.exp(-4.0 * n_value)
            + omega_lambda
            + mu_value**2 * chi_value**2
        )
        denominator = 1.0 - x_value**2
        if denominator <= 0.0:
            raise ValueError("canonical scalar kinetic fraction reached unity")
        return numerator / denominator

    def initial_state(chi_value: float) -> np.ndarray:
        initial_e_squared = e_squared(
            N_BACKGROUND_START,
            chi_value,
            0.0,
        )
        initial_x = (
            -mu_value**2
            * chi_value
            / (5.0 * initial_e_squared)
        )
        return np.asarray([chi_value, initial_x], dtype=float)

    def scalar_rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        chi_value = float(state[0])
        x_value = float(state[1])
        current_e_squared = e_squared(n_value, chi_value, x_value)
        omega_m_n = (
            omega_m * math.exp(-3.0 * n_value) / current_e_squared
        )
        omega_r_n = (
            OMEGA_R * math.exp(-4.0 * n_value) / current_e_squared
        )
        h_value = -1.5 * omega_m_n - 2.0 * omega_r_n - 3.0 * x_value**2
        return np.asarray(
            [
                x_value,
                -(3.0 + h_value) * x_value
                - mu_value**2 * chi_value / current_e_squared,
            ],
            dtype=float,
        )

    def integrate_from_chi(
        chi_value: float,
        dense_output: bool,
    ) -> Any:
        solution = integrate.solve_ivp(
            scalar_rhs,
            (N_BACKGROUND_START, 0.0),
            initial_state(chi_value),
            method="DOP853",
            rtol=2.0e-11,
            atol=2.0e-13,
            max_step=0.025,
            dense_output=dense_output,
        )
        if not solution.success:
            raise ValueError(solution.message)
        return solution

    def present_log_e(chi_value: float) -> float:
        solution = integrate_from_chi(chi_value, dense_output=False)
        present_chi = float(solution.y[0, -1])
        present_x = float(solution.y[1, -1])
        return 0.5 * math.log(e_squared(0.0, present_chi, present_x))

    upper_chi = max(
        2.0,
        4.0 * math.sqrt(max(omega_scalar_zero, 1.0e-14)) / mu_value,
    )
    lower_value = present_log_e(0.0)
    upper_value = present_log_e(upper_chi)
    while lower_value * upper_value >= 0.0 and upper_chi < 100.0:
        upper_chi *= 2.0
        upper_value = present_log_e(upper_chi)
    if lower_value * upper_value >= 0.0:
        raise ValueError("forward scalar amplitude root is not bracketed")
    root = optimize.root_scalar(
        present_log_e,
        bracket=(0.0, upper_chi),
        method="toms748",
        xtol=1.0e-13,
        rtol=1.0e-13,
        maxiter=80,
    )
    if not root.converged:
        raise ValueError("forward scalar amplitude root failed")
    solution = integrate_from_chi(float(root.root), dense_output=True)
    states = solution.sol(n_grid)
    chi_values = np.asarray(states[0], dtype=float)
    x_values = np.asarray(states[1], dtype=float)
    e_values = np.asarray(
        [
            math.sqrt(e_squared(n_value, chi_value, x_value))
            for n_value, chi_value, x_value in zip(
                n_grid,
                chi_values,
                x_values,
                strict=True,
            )
        ],
        dtype=float,
    )
    y_values = mu_value * chi_values / e_values
    scale_factor = np.exp(n_grid)
    omega_m_values = omega_m * scale_factor**-3 / e_values**2
    omega_r_values = OMEGA_R * scale_factor**-4 / e_values**2
    omega_lambda_values = omega_lambda / e_values**2
    omega_scalar_values = x_values**2 + y_values**2
    omega_dark_values = omega_scalar_values + omega_lambda_values
    h_values = (
        -1.5 * omega_m_values
        - 2.0 * omega_r_values
        - 3.0 * x_values**2
    )
    w_dark_values = -1.0 + 2.0 * x_values**2 / omega_dark_values
    constraint = (
        omega_m_values
        + omega_r_values
        + omega_lambda_values
        + omega_scalar_values
        - 1.0
    )
    present_theta = math.atan2(-x_values[-1], y_values[-1])
    old_scalar = score["scalar_branch"]
    old_chi_at_minus_five = float(old_scalar["chi_initial"])
    chi_at_minus_five = float(np.interp(-5.0, n_grid, chi_values))
    diagnostics = {
        "mu": mu_value,
        "omega_lambda": omega_lambda,
        "omega_scalar_zero": omega_scalar_zero,
        "chi_initial_at_N_minus_12": float(root.root),
        "chi_at_N_minus_5": chi_at_minus_five,
        "old_chi_at_N_minus_5": old_chi_at_minus_five,
        "chi_minus5_difference": chi_at_minus_five - old_chi_at_minus_five,
        "present_theta": present_theta,
        "old_present_theta": float(old_scalar["theta"]),
        "theta_difference": present_theta - float(old_scalar["theta"]),
        "present_E": float(e_values[-1]),
        "present_scalar_density": float(omega_scalar_values[-1]),
        "target_present_scalar_density": omega_scalar_zero,
        "maximum_constraint_residual": float(np.max(np.abs(constraint))),
        "minimum_one_plus_w_dark": float(np.min(1.0 + w_dark_values)),
        "maximum_one_plus_w_dark": float(np.max(1.0 + w_dark_values)),
        "root_iterations": int(root.iterations),
        "regular_series": "x_i=-(mu/E_i)^2 chi_i/5 in radiation domination",
    }
    sample_n = np.linspace(N_BACKGROUND_START, 0.0, 121)
    sample_chi, sample_x = solution.sol(sample_n)
    scalar_rows: list[dict[str, Any]] = []
    for n_value, chi_value, x_value in zip(
        sample_n,
        sample_chi,
        sample_x,
        strict=True,
    ):
        current_e = math.sqrt(e_squared(n_value, chi_value, x_value))
        current_y = mu_value * chi_value / current_e
        current_omega_lambda = omega_lambda / current_e**2
        current_omega_scalar = x_value**2 + current_y**2
        current_omega_dark = current_omega_scalar + current_omega_lambda
        current_w_dark = -1.0 + 2.0 * x_value**2 / current_omega_dark
        scalar_rows.append(
            {
                "model": model,
                "N_ln_a": float(n_value),
                "a": math.exp(n_value),
                "z": math.exp(-n_value) - 1.0,
                "E": current_e,
                "chi": float(chi_value),
                "x": float(x_value),
                "y": current_y,
                "Omega_scalar": current_omega_scalar,
                "Omega_Lambda": current_omega_lambda,
                "Omega_dark": current_omega_dark,
                "w_dark": current_w_dark,
                "one_plus_w_dark": 1.0 + current_w_dark,
                "c_s_squared": 1.0,
                "scalar_anisotropic_stress": 0.0,
            }
        )
    return Background(
        model=model,
        omega_m=omega_m,
        parameters=parameters,
        n_grid=n_grid,
        e_grid=e_values,
        h_grid=h_values,
        w_dark_grid=w_dark_values,
        omega_dark_grid=omega_dark_values,
        parent_owned=True,
        scalar_rows=scalar_rows,
        parent_diagnostics=diagnostics,
    )


def build_backgrounds(
    result_5193: dict[str, Any],
) -> dict[str, Background]:
    n_grid = np.linspace(N_BACKGROUND_START, 0.0, 4801)
    backgrounds: dict[str, Background] = {}
    for model in MODEL_ORDER:
        score = result_5193["scores"][model]
        if model in PARENT_MODELS:
            backgrounds[model] = parent_scalar_background(
                model,
                score,
                n_grid,
            )
        else:
            backgrounds[model] = baseline_background(
                model,
                score,
                n_grid,
            )
    return backgrounds


def perturbation_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "item": "parent_action",
            "formula": "S=integral sqrt(-g)[Mpl^2(R-2 Lambda)/2-(partial psi)^2/2-m_gap^2 psi^2/2]+S_m[g,Psi]+S_O4",
            "derivation_status": "PARENT_OWNED_LOW_ENERGY_ACTION",
            "consequence": "Einstein gravity plus one minimally coupled canonical massive scalar at O2",
        },
        {
            "item": "scalar_equation",
            "formula": "Box psi-m_gap^2 psi=0",
            "derivation_status": "EULER_LAGRANGE_EXACT_AT_O2",
            "consequence": "homogeneous equation and perturbation equation share one mass",
        },
        {
            "item": "scalar_stress",
            "formula": "Tmunu_psi=partial_mu psi partial_nu psi-gmunu[(partial psi)^2/2+V]",
            "derivation_status": "METRIC_VARIATION_EXACT_AT_O2",
            "consequence": "Bianchi consistency follows on the scalar equation",
        },
        {
            "item": "newtonian_gauge",
            "formula": "ds^2=a^2[-(1+2 Psi)deta^2+(1-2 Phi)dx^2]",
            "derivation_status": "GAUGE_CONVENTION",
            "consequence": "Phi and Psi are the scalar metric potentials",
        },
        {
            "item": "delta_scalar_equation",
            "formula": "delta_psi''+2Hc delta_psi'+(k^2+a^2 m_gap^2)delta_psi-psi_bar'(Psi'+3 Phi')+2a^2 m_gap^2 psi_bar Psi=0",
            "derivation_status": "LINEARIZED_PARENT_KLEIN_GORDON",
            "consequence": "no phenomenological memory perturbation source is inserted",
        },
        {
            "item": "delta_rho_scalar",
            "formula": "delta_rho_psi=(psi_bar' delta_psi'-psi_bar'^2 Psi)/a^2+m_gap^2 psi_bar delta_psi",
            "derivation_status": "LINEARIZED_PARENT_STRESS",
            "consequence": "scalar clustering enters only through its derived stress",
        },
        {
            "item": "delta_p_scalar",
            "formula": "delta_p_psi=(psi_bar' delta_psi'-psi_bar'^2 Psi)/a^2-m_gap^2 psi_bar delta_psi",
            "derivation_status": "LINEARIZED_PARENT_STRESS",
            "consequence": "rest-frame pressure perturbation is fixed",
        },
        {
            "item": "momentum_scalar",
            "formula": "delta_q_psi=-psi_bar' delta_psi/a^2",
            "derivation_status": "LINEARIZED_PARENT_STRESS",
            "consequence": "no independently fitted velocity closure",
        },
        {
            "item": "principal_symbol",
            "formula": "S2_high_k=(1/2)integral a^2[(delta_psi')^2-(grad delta_psi)^2+lower_derivative_terms]",
            "derivation_status": "QUADRATIC_ACTION_PRINCIPAL_PART",
            "consequence": "no ghost and c_s^2=1",
        },
        {
            "item": "anisotropic_stress",
            "formula": "Pi_psi^i_j|linear_tracefree=0",
            "derivation_status": "EXACT_FOR_ONE_CANONICAL_SCALAR",
            "consequence": "the parent scalar produces no intrinsic gravitational slip",
        },
        {
            "item": "matter_conservation",
            "formula": "nabla_mu T_m^{mu nu}=0",
            "derivation_status": "DIFFEOMORPHISM_IDENTITY_PLUS_MINIMAL_METRIC_COUPLING",
            "consequence": "matter follows metric geodesics and no scalar fifth force is present",
        },
        {
            "item": "combined_scalar_Lambda_fluid",
            "formula": "rho_D=rho_psi+rho_Lambda; p_D=p_psi-rho_Lambda; 1+w_D=dot(psi)^2/rho_D; c_s,rf^2=1",
            "derivation_status": "EXACT_STRESS_SUM_IDENTITY",
            "consequence": "the free-Lambda parent branch is linearly equivalent to one conserved nonphantom c_s^2=1 fluid",
        },
        {
            "item": "late_scalar_slip",
            "formula": "Phi-Psi=0 when other species have negligible anisotropic stress",
            "derivation_status": "EINSTEIN_TRACEFREE_CONSTRAINT",
            "consequence": "standard neutrino or photon slip is not falsely assigned to MTS",
        },
        {
            "item": "subhorizon_growth",
            "formula": "D_NN+[2+d ln H/dN]D_N-(3/2)Omega_m D=O[(aH/k)^2 delta_psi_response]",
            "derivation_status": "DERIVED_QUASISTATIC_LIMIT_THEN_CAMB_CHECKED",
            "consequence": "the smooth growth equation is now an approximation to a derived parent sector, not an axiom",
        },
        {
            "item": "claim_ceiling",
            "formula": "no official CMB likelihood and no derivation of m_gap or the homogeneous state",
            "derivation_status": "NONCLAIM_GUARD",
            "consequence": "growth and compressed-CMB results are internal theory-discipline evidence",
        },
    ]
    return tagged(rows)


def solve_smooth_growth(background: Background) -> dict[str, Any]:
    equality_ratio = (
        background.omega_m * math.exp(N_GROWTH_START) / OMEGA_R
    )
    initial_density = 1.0 + 1.5 * equality_ratio
    initial_derivative = 1.5 * equality_ratio

    def growth_rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        e_value, h_value, _, _ = background.values_at_n(n_value)
        omega_m_n = (
            background.omega_m
            * math.exp(-3.0 * n_value)
            / float(e_value) ** 2
        )
        return np.asarray(
            [
                state[1],
                -(2.0 + float(h_value)) * state[1]
                + 1.5 * omega_m_n * state[0],
            ],
            dtype=float,
        )

    solution = integrate.solve_ivp(
        growth_rhs,
        (N_GROWTH_START, 0.0),
        np.asarray([initial_density, initial_derivative], dtype=float),
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.02,
        dense_output=True,
    )
    if not solution.success:
        raise ValueError(solution.message)
    density_today = float(solution.y[0, -1])
    return {
        "solution": solution,
        "density_today": density_today,
        "initial_equality_ratio": equality_ratio,
        "initial_f": initial_derivative / initial_density,
    }


def growth_shape_at_z(
    growth_solution: dict[str, Any],
    redshifts: np.ndarray,
) -> np.ndarray:
    n_values = -np.log1p(redshifts)
    states = growth_solution["solution"].sol(n_values)
    return np.asarray(
        states[1] / growth_solution["density_today"],
        dtype=float,
    )


def numeric_vector_rows(path: Path) -> list[tuple[float, float, str]]:
    rows: list[tuple[float, float, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) >= 3:
            rows.append((float(parts[0]), float(parts[1]), parts[2]))
    return rows


def load_data_blocks(
    file_specs: tuple[tuple[str, Path, Path], ...],
) -> list[DataBlock]:
    blocks: list[DataBlock] = []
    for sample, vector_path, covariance_path in file_specs:
        rows = numeric_vector_rows(vector_path)
        covariance = np.asarray(np.loadtxt(covariance_path), dtype=float)
        if covariance.ndim == 1:
            dimension = int(round(math.sqrt(covariance.size)))
            covariance = covariance.reshape((dimension, dimension))
        if covariance.shape != (len(rows), len(rows)):
            raise ValueError(f"covariance shape mismatch for {sample}")
        np.linalg.cholesky(covariance)
        blocks.append(
            DataBlock(
                sample=sample,
                rows=rows,
                covariance=covariance,
                vector_path=vector_path,
                covariance_path=covariance_path,
            )
        )
    return blocks


def comoving_integral(background: Background, redshift: float) -> float:
    e_interpolator = interpolate.PchipInterpolator(
        background.n_grid,
        background.e_grid,
        extrapolate=False,
    )
    n_lower = -math.log1p(redshift)
    value, _ = integrate.quad(
        lambda n_value: math.exp(-n_value) / float(e_interpolator(n_value)),
        n_lower,
        0.0,
        epsabs=1.0e-10,
        epsrel=1.0e-10,
        limit=100,
    )
    return float(value)


def fit_growth_dataset(
    background: Background,
    growth_solution: dict[str, Any],
    blocks: list[DataBlock],
    file_set: str,
    score_mode: str,
    excluded_sample: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    selected_blocks = [
        block for block in blocks if block.sample != excluded_sample
    ]
    observations: list[float] = []
    design_rows: list[list[float]] = []
    row_context: list[dict[str, Any]] = []
    covariance_blocks: list[np.ndarray] = []
    for block in selected_blocks:
        if score_mode == "all":
            indices = list(range(len(block.rows)))
        elif score_mode == "fs8_only":
            indices = [
                index
                for index, row in enumerate(block.rows)
                if row[2] == "f_sigma8"
            ]
        else:
            raise ValueError(f"unsupported score mode {score_mode}")
        covariance_blocks.append(block.covariance[np.ix_(indices, indices)])
        for index in indices:
            redshift, observed, quantity = block.rows[index]
            distance_coefficient = 0.0
            growth_coefficient = 0.0
            if quantity == "f_sigma8":
                growth_coefficient = float(
                    growth_shape_at_z(
                        growth_solution,
                        np.asarray([redshift]),
                    )[0]
                )
            else:
                integral_value = comoving_integral(background, redshift)
                e_value = float(background.e_at_z(redshift))
                if quantity in {"DM_over_rs", "DM_over_rd"}:
                    distance_coefficient = integral_value
                elif quantity in {"DH_over_rs", "DH_over_rd"}:
                    distance_coefficient = 1.0 / e_value
                elif quantity in {"DV_over_rs", "DV_over_rd"}:
                    distance_coefficient = (
                        redshift
                        * integral_value**2
                        / e_value
                    ) ** (1.0 / 3.0)
                else:
                    raise ValueError(f"unsupported quantity {quantity}")
            observations.append(observed)
            design_rows.append(
                [distance_coefficient, growth_coefficient]
                if score_mode == "all"
                else [growth_coefficient]
            )
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
    observation_vector = np.asarray(observations, dtype=float)
    design = np.asarray(design_rows, dtype=float)
    covariance_inverse = linalg.inv(covariance)
    normal_matrix = design.T @ covariance_inverse @ design
    normal_vector = design.T @ covariance_inverse @ observation_vector
    nuisance = linalg.solve(normal_matrix, normal_vector, assume_a="sym")
    predicted = design @ nuisance
    residual = observation_vector - predicted
    chi2_value = float(residual @ covariance_inverse @ residual)
    nuisance_covariance = linalg.inv(normal_matrix)
    signed_contribution = residual * (covariance_inverse @ residual)
    if score_mode == "all":
        distance_alpha = float(nuisance[0])
        sigma8_zero = float(nuisance[1])
        distance_alpha_sigma = math.sqrt(float(nuisance_covariance[0, 0]))
        sigma8_sigma = math.sqrt(float(nuisance_covariance[1, 1]))
    else:
        distance_alpha = math.nan
        sigma8_zero = float(nuisance[0])
        distance_alpha_sigma = math.nan
        sigma8_sigma = math.sqrt(float(nuisance_covariance[0, 0]))
    edge_flag = not (
        10.0 < distance_alpha < 60.0
        if score_mode == "all"
        else True
    ) or not (0.2 < sigma8_zero < 1.4)
    summary = {
        "model": background.model,
        "file_set": file_set,
        "score_mode": score_mode,
        "excluded_sample": excluded_sample or "",
        "n_data": len(observation_vector),
        "n_profiled_nuisance": len(nuisance),
        "chi2": chi2_value,
        "dof_after_profile": len(observation_vector) - len(nuisance),
        "distance_alpha": distance_alpha if score_mode == "all" else "",
        "distance_alpha_sigma": (
            distance_alpha_sigma if score_mode == "all" else ""
        ),
        "sigma8_0": sigma8_zero,
        "sigma8_0_sigma": sigma8_sigma,
        "nuisance_edge_flag": edge_flag,
        "covariance_condition_number": float(np.linalg.cond(covariance)),
        "fit_status": "PASS" if not edge_flag else "EDGE_WARNING",
        "claim_status": "DIRECT_PARENT_GROWTH_INTERNAL_TEST_NONCLAIM",
    }
    residual_rows = []
    diagonal_sigma = np.sqrt(np.diag(covariance))
    for context, prediction, residual_value, sigma_value, signed_value in zip(
        row_context,
        predicted,
        residual,
        diagonal_sigma,
        signed_contribution,
        strict=True,
    ):
        residual_rows.append(
            {
                "model": background.model,
                "file_set": file_set,
                "score_mode": score_mode,
                "excluded_sample": excluded_sample or "",
                **context,
                "predicted": float(prediction),
                "residual": float(residual_value),
                "diagonal_sigma": float(sigma_value),
                "diagonal_pull": float(residual_value / sigma_value),
                "cov_signed_chi2_contribution": float(signed_value),
                "distance_alpha": (
                    distance_alpha if score_mode == "all" else ""
                ),
                "sigma8_0": sigma8_zero,
            }
        )
    return summary, residual_rows


def growth_scores(
    backgrounds: dict[str, Background],
    growth_solutions: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    primary_blocks = load_data_blocks(PRIMARY_FILES)
    full_shape_blocks = load_data_blocks(FULL_SHAPE_FILES)
    summaries: list[dict[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    jackknife_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    for file_set, blocks in (
        ("primary_BAO_plus", primary_blocks),
        ("robustness_full_shape_only", full_shape_blocks),
    ):
        for block in blocks:
            eigenvalues = np.linalg.eigvalsh(block.covariance)
            schema_rows.append(
                {
                    "file_set": file_set,
                    "sample": block.sample,
                    "vector_rows": len(block.rows),
                    "covariance_rows": block.covariance.shape[0],
                    "covariance_columns": block.covariance.shape[1],
                    "quantities": ";".join(
                        sorted({row[2] for row in block.rows})
                    ),
                    "minimum_covariance_eigenvalue": float(
                        np.min(eigenvalues)
                    ),
                    "maximum_covariance_eigenvalue": float(
                        np.max(eigenvalues)
                    ),
                    "cholesky_pass": True,
                    "vector_sha256": file_digest(block.vector_path),
                    "covariance_sha256": file_digest(block.covariance_path),
                    "vector_path": str(block.vector_path),
                    "covariance_path": str(block.covariance_path),
                }
            )
        for model in MODEL_ORDER:
            for score_mode in ("all", "fs8_only"):
                summary, model_residuals = fit_growth_dataset(
                    backgrounds[model],
                    growth_solutions[model],
                    blocks,
                    file_set,
                    score_mode,
                )
                summaries.append(summary)
                residuals.extend(model_residuals)
    for excluded_sample, _, _ in PRIMARY_FILES:
        for model in MODEL_ORDER:
            summary, _ = fit_growth_dataset(
                backgrounds[model],
                growth_solutions[model],
                primary_blocks,
                "primary_BAO_plus",
                "all",
                excluded_sample=excluded_sample,
            )
            jackknife_rows.append(summary)
    return (
        tagged(summaries),
        tagged(residuals),
        tagged(jackknife_rows),
        tagged(schema_rows),
    )


def growth_comparison_rows(
    growth_summary: list[dict[str, Any]],
    result_5193: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    primary = {
        row["model"]: row
        for row in growth_summary
        if row["file_set"] == "primary_BAO_plus"
        and row["score_mode"] == "all"
        and not row["excluded_sample"]
    }
    comparisons: list[dict[str, Any]] = []
    combined: list[dict[str, Any]] = []
    n_background = int(
        result_5193["data_contract"]["Pantheon_plus_rows"]
        + result_5193["data_contract"]["DESI_DR2_rows"]
    )
    n_growth = int(primary["LCDM"]["n_data"])
    for model in MODEL_ORDER:
        score = result_5193["scores"][model]
        growth = primary[model]
        combined_chi2 = float(score["chi2_total"]) + float(growth["chi2"])
        combined_k = int(score["k"]) + int(growth["n_profiled_nuisance"])
        combined_n = n_background + n_growth
        combined.append(
            {
                "model": model,
                "chi2_SN_DESI": float(score["chi2_total"]),
                "chi2_SDSS_growth_joint": float(growth["chi2"]),
                "chi2_combined": combined_chi2,
                "n_combined": combined_n,
                "k_combined": combined_k,
                "AIC_combined": combined_chi2 + 2.0 * combined_k,
                "BIC_combined": (
                    combined_chi2
                    + combined_k * math.log(combined_n)
                ),
                "overlap_policy": "Pantheon+DESI_DR2 plus alternative SDSS/eBOSS primary compression; full-shape set not added",
                "claim_status": "INTERNAL_COMBINED_SCORE_NOT_GLOBAL_LIKELIHOOD",
            }
        )
    combined_by_model = {row["model"]: row for row in combined}
    for parent_model in PARENT_MODELS:
        for baseline_model in ("LCDM", "wCDM", "CPL"):
            parent_growth = primary[parent_model]
            baseline_growth = primary[baseline_model]
            parent_combined = combined_by_model[parent_model]
            baseline_combined = combined_by_model[baseline_model]
            comparisons.append(
                {
                    "parent_model": parent_model,
                    "baseline_model": baseline_model,
                    "delta_growth_chi2": float(parent_growth["chi2"])
                    - float(baseline_growth["chi2"]),
                    "delta_combined_chi2": float(
                        parent_combined["chi2_combined"]
                    )
                    - float(baseline_combined["chi2_combined"]),
                    "delta_combined_AIC": float(
                        parent_combined["AIC_combined"]
                    )
                    - float(baseline_combined["AIC_combined"]),
                    "delta_combined_BIC": float(
                        parent_combined["BIC_combined"]
                    )
                    - float(baseline_combined["BIC_combined"]),
                    "same_growth_rows": True,
                    "same_growth_covariance": True,
                    "same_growth_nuisance_count": True,
                    "interpretation_rule": "negative favors parent; absolute delta below 2 is a draw-scale result",
                }
            )
    return tagged(comparisons), tagged(combined)


def parent_camb_table(background: Background) -> tuple[np.ndarray, np.ndarray]:
    scale_factors = np.unique(
        np.concatenate(
            (
                np.geomspace(CAMB_A_MIN, 0.01, 180),
                np.linspace(0.01, 1.0, 1200),
            )
        )
    )
    n_values = np.log(scale_factors)
    w_values = background.values_at_n(n_values)[2]
    return scale_factors, np.asarray(w_values, dtype=float)


def make_camb_params(
    background: Background,
    h0_value: float,
    parent_tables: dict[str, tuple[np.ndarray, np.ndarray]],
    parent_implementation: str,
    calculate_transfers: bool,
) -> camb.CAMBparams:
    little_h = h0_value / 100.0
    omch2 = (
        background.omega_m * little_h**2
        - OMBH2
        - NEUTRINO_PHYSICAL_DENSITY_APPROX
    )
    if omch2 <= 0.0:
        raise ValueError("negative cold-dark-matter physical density")
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=h0_value,
        ombh2=OMBH2,
        omch2=omch2,
        tau=TAU,
        mnu=MNU_EV,
        omk=0.0,
    )
    omega_error = background.omega_m - float(params.omegam)
    if abs(omega_error) > 1.0e-9:
        omch2 += omega_error * little_h**2
        params.set_cosmology(
            H0=h0_value,
            ombh2=OMBH2,
            omch2=omch2,
            tau=TAU,
            mnu=MNU_EV,
            omk=0.0,
        )
    params.InitPower.set_params(As=AS, ns=NS)
    if background.model == "wCDM":
        params.set_dark_energy(
            w=background.parameters["w"],
            wa=0.0,
            cs2=1.0,
            dark_energy_model="fluid",
        )
    elif background.model == "CPL":
        params.set_dark_energy(
            w=background.parameters["w0"],
            wa=background.parameters["wa"],
            cs2=1.0,
            dark_energy_model="ppf",
        )
    elif background.model in PARENT_MODELS:
        scale_factors, exact_w = parent_tables[background.model]
        if parent_implementation == "fluid":
            supplied_w = np.maximum(exact_w, -1.0 + CAMB_W_FLOOR)
            dark_energy_model = "fluid"
        elif parent_implementation == "ppf":
            supplied_w = np.maximum(exact_w, -1.0 + 1.0e-12)
            dark_energy_model = "ppf"
        else:
            raise ValueError(
                f"unsupported parent implementation {parent_implementation}"
            )
        params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=scale_factors,
            wde_w_array=supplied_w,
            dark_energy_model=dark_energy_model,
        )
    if calculate_transfers:
        transfer_redshifts = sorted(
            {
                0.0,
                *[float(value) for value in RSD_Z_VALUES],
            },
            reverse=True,
        )
        params.set_matter_power(
            redshifts=transfer_redshifts,
            kmax=1.0,
            nonlinear=False,
            silent=True,
        )
        params.set_for_lmax(CAMB_LMAX, lens_potential_accuracy=0)
    return params


def load_planck_prior() -> tuple[np.ndarray, np.ndarray, list[str]]:
    parameter_order = ["R", "l_A", "Omega_b_h2", "n_s"]
    vector_rows = [
        row
        for row in read_csv(PLANCK_VECTOR)
        if row["model"] == "wCDM"
    ]
    means = {
        row["parameter"]: float(row["mean"]) for row in vector_rows
    }
    covariance_rows = [
        row
        for row in read_csv(PLANCK_COVARIANCE)
        if row["model"] == "wCDM"
    ]
    covariance_lookup = {
        (row["row_parameter"], row["col_parameter"]): float(
            row["covariance"]
        )
        for row in covariance_rows
    }
    covariance = np.asarray(
        [
            [
                covariance_lookup[(row_parameter, column_parameter)]
                for column_parameter in parameter_order
            ]
            for row_parameter in parameter_order
        ],
        dtype=float,
    )
    np.linalg.cholesky(covariance)
    return (
        np.asarray([means[name] for name in parameter_order], dtype=float),
        covariance,
        parameter_order,
    )


def compressed_cmb_fit(
    background: Background,
    parent_tables: dict[str, tuple[np.ndarray, np.ndarray]],
    planck_mean: np.ndarray,
    planck_covariance: np.ndarray,
) -> dict[str, Any]:
    covariance_inverse = linalg.inv(planck_covariance)
    evaluation_cache: dict[float, tuple[float, dict[str, float], np.ndarray]] = {}

    def evaluate(
        h0_value: float,
    ) -> tuple[float, dict[str, float], np.ndarray]:
        cache_key = round(float(h0_value), 8)
        if cache_key in evaluation_cache:
            return evaluation_cache[cache_key]
        params = make_camb_params(
            background,
            float(h0_value),
            parent_tables,
            "fluid",
            calculate_transfers=False,
        )
        camb_background = camb.get_background(params)
        derived = {
            key: float(value)
            for key, value in camb_background.get_derived_params().items()
        }
        l_a = 100.0 * math.pi / derived["thetastar"]
        shift_r = (
            math.sqrt(background.omega_m)
            * float(h0_value)
            * derived["DAstar"]
            * 1000.0
            / C_KM_S
        )
        predicted = np.asarray([shift_r, l_a, OMBH2, NS], dtype=float)
        residual = predicted - planck_mean
        chi2_value = float(
            residual @ covariance_inverse @ residual
        )
        payload = (chi2_value, derived, predicted)
        evaluation_cache[cache_key] = payload
        return payload

    minimization = optimize.minimize_scalar(
        lambda h0_value: evaluate(float(h0_value))[0],
        bounds=H0_PRIOR_BOUNDS,
        method="bounded",
        options={"xatol": 2.0e-4, "maxiter": 80},
    )
    if not minimization.success:
        raise ValueError("compressed CMB H0 profile failed")
    best_h0 = float(minimization.x)
    chi2_value, derived, predicted = evaluate(best_h0)
    distance_to_edge = min(
        best_h0 - H0_PRIOR_BOUNDS[0],
        H0_PRIOR_BOUNDS[1] - best_h0,
    )
    return {
        "model": background.model,
        "H0_profiled": best_h0,
        "chi2_compressed_distance_prior": chi2_value,
        "n_prior_rows": 4,
        "n_profiled_parameters": 1,
        "dof_nominal": 3,
        "H0_edge_flag": distance_to_edge <= 0.5,
        "R_predicted": float(predicted[0]),
        "l_A_predicted": float(predicted[1]),
        "Omega_b_h2_fixed": float(predicted[2]),
        "n_s_fixed": float(predicted[3]),
        "R_prior_mean": float(planck_mean[0]),
        "l_A_prior_mean": float(planck_mean[1]),
        "thetastar": derived["thetastar"],
        "DAstar_Gpc": derived["DAstar"],
        "rstar_Mpc": derived["rstar"],
        "age_Gyr": derived["age"],
        "zstar": derived["zstar"],
        "rdrag_Mpc": derived["rdrag"],
        "diagnostic_status": "COMPRESSED_CMB_CONDITIONAL_DIAGNOSTIC_ONLY",
        "official_likelihood_run": False,
    }


def run_camb_transfers(
    background: Background,
    h0_value: float,
    parent_tables: dict[str, tuple[np.ndarray, np.ndarray]],
    parent_implementation: str,
) -> dict[str, Any]:
    params = make_camb_params(
        background,
        h0_value,
        parent_tables,
        parent_implementation,
        calculate_transfers=True,
    )
    start = time.perf_counter()
    results = camb.get_results(params)
    runtime = time.perf_counter() - start
    powers = results.get_cmb_power_spectra(
        params,
        CMB_unit="muK",
    )["total"]
    redshift_count = int(params.Transfer.PK_num_redshifts)
    transfer_redshifts = np.asarray(
        [
            float(params.Transfer.PK_redshifts[index])
            for index in range(redshift_count)
        ],
        dtype=float,
    )
    fsigma8 = np.asarray(results.get_fsigma8(), dtype=float)
    sigma8_zero = float(results.get_sigma8_0())
    order = np.argsort(transfer_redshifts)
    return {
        "params": params,
        "results": results,
        "powers": powers,
        "transfer_redshifts": transfer_redshifts[order],
        "fsigma8": fsigma8[order],
        "sigma8_0": sigma8_zero,
        "g_fsigma8": fsigma8[order] / sigma8_zero,
        "derived": {
            key: float(value)
            for key, value in results.get_derived_params().items()
        },
        "runtime_seconds": runtime,
        "implementation": parent_implementation,
    }


def camb_analysis(
    backgrounds: dict[str, Background],
    growth_solutions: dict[str, dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    parent_tables = {
        model: parent_camb_table(backgrounds[model])
        for model in PARENT_MODELS
    }
    planck_mean, planck_covariance, parameter_order = load_planck_prior()
    compressed_rows = [
        compressed_cmb_fit(
            backgrounds[model],
            parent_tables,
            planck_mean,
            planck_covariance,
        )
        for model in MODEL_ORDER
    ]
    compressed_by_model = {row["model"]: row for row in compressed_rows}
    camb_runs: dict[str, dict[str, Any]] = {}
    for model in MODEL_ORDER:
        camb_runs[model] = run_camb_transfers(
            backgrounds[model],
            float(compressed_by_model[model]["H0_profiled"]),
            parent_tables,
            "fluid",
        )
    ppf_runs = {
        model: run_camb_transfers(
            backgrounds[model],
            float(compressed_by_model[model]["H0_profiled"]),
            parent_tables,
            "ppf",
        )
        for model in PARENT_MODELS
    }
    branch_rows: list[dict[str, Any]] = []
    for model in MODEL_ORDER:
        run = camb_runs[model]
        params = run["params"]
        branch_rows.append(
            {
                **compressed_by_model[model],
                "CAMB_version": camb.__version__,
                "CAMB_dark_energy_implementation": (
                    "canonical_equivalent_tabulated_fluid_cs2_1"
                    if model in PARENT_MODELS
                    else "standard_CAMB_baseline"
                ),
                "Omega_m_target": backgrounds[model].omega_m,
                "Omega_m_CAMB": float(params.omegam),
                "sigma8_0_As_fixed": run["sigma8_0"],
                "runtime_seconds": run["runtime_seconds"],
                "spectra_lmax": CAMB_LMAX,
                "transfer_status": "PASS",
                "claim_status": "NO_OFFICIAL_CMB_LIKELIHOOD",
            }
        )
    fluid_ppf_rows: list[dict[str, Any]] = []
    for model in PARENT_MODELS:
        fluid_run = camb_runs[model]
        ppf_run = ppf_runs[model]
        common_redshifts = RSD_Z_VALUES
        fluid_growth = np.interp(
            common_redshifts,
            fluid_run["transfer_redshifts"],
            fluid_run["g_fsigma8"],
        )
        ppf_growth = np.interp(
            common_redshifts,
            ppf_run["transfer_redshifts"],
            ppf_run["g_fsigma8"],
        )
        for redshift, fluid_value, ppf_value in zip(
            common_redshifts,
            fluid_growth,
            ppf_growth,
            strict=True,
        ):
            fluid_ppf_rows.append(
                {
                    "model": model,
                    "z": float(redshift),
                    "g_fsigma8_fluid": float(fluid_value),
                    "g_fsigma8_PPF": float(ppf_value),
                    "fractional_difference": float(
                        fluid_value / ppf_value - 1.0
                    ),
                    "sigma8_0_fluid": fluid_run["sigma8_0"],
                    "sigma8_0_PPF": ppf_run["sigma8_0"],
                    "thetastar_fluid": fluid_run["derived"]["thetastar"],
                    "thetastar_PPF": ppf_run["derived"]["thetastar"],
                    "w_floor_fluid": CAMB_W_FLOOR,
                    "interpretation": "numerical regulator convergence comparator; PPF is not the parent derivation",
                }
            )
    smooth_camb_rows: list[dict[str, Any]] = []
    lcdm_run = camb_runs["LCDM"]
    lcdm_camb_growth = np.interp(
        RSD_Z_VALUES,
        lcdm_run["transfer_redshifts"],
        lcdm_run["g_fsigma8"],
    )
    lcdm_smooth_growth = growth_shape_at_z(
        growth_solutions["LCDM"],
        RSD_Z_VALUES,
    )
    for model in MODEL_ORDER:
        run = camb_runs[model]
        camb_growth = np.interp(
            RSD_Z_VALUES,
            run["transfer_redshifts"],
            run["g_fsigma8"],
        )
        smooth_growth = growth_shape_at_z(
            growth_solutions[model],
            RSD_Z_VALUES,
        )
        for index, redshift in enumerate(RSD_Z_VALUES):
            relative_camb = camb_growth[index] / lcdm_camb_growth[index]
            relative_smooth = (
                smooth_growth[index] / lcdm_smooth_growth[index]
            )
            smooth_camb_rows.append(
                {
                    "model": model,
                    "z": float(redshift),
                    "g_fsigma8_CAMB": float(camb_growth[index]),
                    "g_fsigma8_smooth_equation": float(
                        smooth_growth[index]
                    ),
                    "absolute_fractional_difference": float(
                        camb_growth[index] / smooth_growth[index] - 1.0
                    ),
                    "relative_response_vs_LCDM_CAMB": float(relative_camb),
                    "relative_response_vs_LCDM_smooth": float(relative_smooth),
                    "relative_response_mismatch": float(
                        relative_camb / relative_smooth - 1.0
                    ),
                    "interpretation": "relative mismatch isolates parent dark-sector perturbation treatment from common radiation/baryon/neutrino transfer effects",
                }
            )
    clustering_rows: list[dict[str, Any]] = []
    for model in ("LCDM", *PARENT_MODELS):
        run = camb_runs[model]
        little_h = float(compressed_by_model[model]["H0_profiled"]) / 100.0
        q_values = RSD_K_H_VALUES * little_h
        evolution = run["results"].get_redshift_evolution(
            q_values,
            RSD_Z_VALUES,
            vars=["delta_tot", "delta_tot_de", "Weyl", "growth"],
        )
        for k_index, k_h_value in enumerate(RSD_K_H_VALUES):
            for z_index, redshift in enumerate(RSD_Z_VALUES):
                delta_total = float(evolution[k_index, z_index, 0])
                delta_total_de = float(evolution[k_index, z_index, 1])
                clustering_rows.append(
                    {
                        "model": model,
                        "k_h_Mpc_inverse": float(k_h_value),
                        "k_Mpc_inverse": float(q_values[k_index]),
                        "z": float(redshift),
                        "delta_tot": delta_total,
                        "delta_tot_including_dark_energy": delta_total_de,
                        "dark_energy_source_fraction": float(
                            (delta_total_de - delta_total)
                            / delta_total
                        ),
                        "Weyl_transfer": float(
                            evolution[k_index, z_index, 2]
                        ),
                        "CAMB_growth_variable": float(
                            evolution[k_index, z_index, 3]
                        ),
                        "claim_status": "LINEAR_CAMB_TRANSFER_DIAGNOSTIC",
                    }
                )
    spectra_rows: list[dict[str, Any]] = []
    lcdm_powers = camb_runs["LCDM"]["powers"]
    ell_start = 30
    ell_stop = min(CAMB_LMAX, lcdm_powers.shape[0] - 1)
    ell_slice = slice(ell_start, ell_stop + 1)
    for model in MODEL_ORDER:
        powers = camb_runs[model]["powers"]
        for spectrum_name, column in (
            ("TT", 0),
            ("EE", 1),
            ("TE", 3),
        ):
            baseline_values = lcdm_powers[ell_slice, column]
            model_values = powers[ell_slice, column]
            difference = model_values - baseline_values
            baseline_rms = math.sqrt(
                float(np.mean(baseline_values**2))
            )
            rms_difference = math.sqrt(float(np.mean(difference**2)))
            stable_mask = (
                np.abs(baseline_values)
                >= 0.01 * np.max(np.abs(baseline_values))
            )
            stable_fraction = np.abs(
                difference[stable_mask] / baseline_values[stable_mask]
            )
            spectra_rows.append(
                {
                    "model": model,
                    "spectrum": spectrum_name,
                    "ell_min": ell_start,
                    "ell_max": ell_stop,
                    "rms_difference_over_LCDM_rms": (
                        rms_difference / baseline_rms
                        if baseline_rms > 0.0
                        else math.nan
                    ),
                    "max_abs_fractional_difference_stable_ells": (
                        float(np.max(stable_fraction))
                        if stable_fraction.size
                        else math.nan
                    ),
                    "same_As_ns_tau_ombh2": True,
                    "H0_profiled_separately_to_compressed_prior": True,
                    "official_likelihood_run": False,
                }
            )
    diagnostics = {
        "planck_parameter_order": parameter_order,
        "planck_mean": planck_mean.tolist(),
        "planck_covariance": planck_covariance.tolist(),
        "parent_tables": {
            model: {
                "rows": len(parent_tables[model][0]),
                "a_min": float(parent_tables[model][0][0]),
                "a_max": float(parent_tables[model][0][-1]),
                "w_min": float(np.min(parent_tables[model][1])),
                "w_max": float(np.max(parent_tables[model][1])),
            }
            for model in PARENT_MODELS
        },
    }
    return (
        tagged(compressed_rows),
        tagged(branch_rows),
        tagged(fluid_ppf_rows),
        tagged(smooth_camb_rows),
        tagged(clustering_rows),
        tagged(spectra_rows),
        diagnostics,
    )


def o4_envelope_rows() -> list[dict[str, Any]]:
    rows_5193 = read_csv(BACKGROUND_5193)
    maximum_delta_f = max(
        abs(float(row["delta_F_H0_70"]))
        for row in rows_5193
        if row.get("delta_F_H0_70")
    )
    h0_over_c_mpc_inverse = 70.0 / C_KM_S
    derivative_ratio = CAMB_KMAX_MPC / h0_over_c_mpc_inverse
    fourth_derivative_amplification = derivative_ratio**4
    return tagged(
        [
            {
                "input": "maximum_abs_delta_F_H0_70_from_5193",
                "value": maximum_delta_f,
                "units": "dimensionless",
                "source": str(BACKGROUND_5193),
                "role": "order-reduced O4 homogeneous coefficient",
            },
            {
                "input": "CMB_k_max",
                "value": CAMB_KMAX_MPC,
                "units": "Mpc^-1",
                "source": "checkpoint_5194 conservative transfer envelope",
                "role": "maximum derivative scale used for worst-case k^4 amplification",
            },
            {
                "input": "k_over_H0_fourth",
                "value": fourth_derivative_amplification,
                "units": "dimensionless",
                "source": "[(k c)/H0]^4 at H0=70 km/s/Mpc",
                "role": "conservative dimension-eight derivative amplification",
            },
            {
                "input": "O4_perturbation_envelope",
                "value": maximum_delta_f * fourth_derivative_amplification,
                "units": "dimensionless",
                "source": "absolute product without cancellations",
                "role": "upper-order estimate; negligible if perturbative derivative counting applies",
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    local_sources: list[tuple[str, Path, str]] = [
        ("checkpoint_5193_result", RESULT_5193, "late-background fit input"),
        ("checkpoint_5193_background", BACKGROUND_5193, "O4 input"),
        ("checkpoint_5193_document", DOCUMENT_5193, "derivation context"),
        ("checkpoint_5193_script", SCRIPT_5193, "background convention"),
        ("checkpoint_5193_validation", VALIDATION_5193, "upstream lock"),
        ("SDSS_row_lock_manifest", SDSS_MANIFEST, "growth row lock"),
        ("SDSS_covariance_validation", SDSS_VALIDATION, "growth covariance checks"),
        ("growth_source_manifest", SOURCE_MANIFEST, "growth source URLs"),
        ("Planck_distance_vector", PLANCK_VECTOR, "compressed CMB vector"),
        (
            "Planck_distance_covariance",
            PLANCK_COVARIANCE,
            "compressed CMB covariance",
        ),
        ("Planck_row_lock_manifest", PLANCK_MANIFEST, "compressed CMB row lock"),
        (
            "Planck_source_paper",
            PLANCK_ROOT / "source" / "1808.05724.pdf",
            "distance-prior source paper",
        ),
        (
            "CAMB_installed_package",
            Path(camb.__file__).resolve(),
            "linear perturbation and spectra engine",
        ),
    ]
    for _, vector_path, covariance_path in (*PRIMARY_FILES, *FULL_SHAPE_FILES):
        local_sources.append(
            (vector_path.name, vector_path, "growth observable vector")
        )
        local_sources.append(
            (
                covariance_path.name,
                covariance_path,
                "growth observable covariance",
            )
        )
    rows = [
        {
            "source_id": source_id,
            "path_or_url": str(path),
            "exists": path.exists(),
            "sha256": file_digest(path) if path.exists() and path.is_file() else "",
            "role": role,
            "provenance_status": "LOCAL_SOURCE_LOCK",
        }
        for source_id, path, role in local_sources
    ]
    rows.extend(
        [
            {
                "source_id": "Ma_Bertschinger_1995",
                "path_or_url": "https://arxiv.org/abs/astro-ph/9506072",
                "exists": "",
                "sha256": "",
                "role": "conformal Newtonian gauge and linear Einstein-Boltzmann conventions",
                "provenance_status": "PRIMARY_REFERENCE_URL",
            },
            {
                "source_id": "CAMB_dark_energy_documentation",
                "path_or_url": "https://camb.readthedocs.io/en/devel/dark_energy.html",
                "exists": "",
                "sha256": "",
                "role": "DarkEnergyFluid tabulated w(a) and rest-frame sound-speed contract",
                "provenance_status": "OFFICIAL_SOFTWARE_DOCUMENTATION_URL",
            },
            {
                "source_id": "SDSS_eBOSS_DR16_QSO",
                "path_or_url": "https://arxiv.org/abs/2007.08999",
                "exists": "",
                "sha256": "",
                "role": "QSO BAO and f sigma8 source publication",
                "provenance_status": "PRIMARY_REFERENCE_URL",
            },
        ]
    )
    return tagged(rows)


def build_document(
    backgrounds: dict[str, Background],
    growth_summary: list[dict[str, Any]],
    growth_jackknife: list[dict[str, Any]],
    growth_comparisons: list[dict[str, Any]],
    combined_scores: list[dict[str, Any]],
    cmb_branches: list[dict[str, Any]],
    fluid_ppf: list[dict[str, Any]],
    smooth_camb: list[dict[str, Any]],
    clustering: list[dict[str, Any]],
    o4_rows: list[dict[str, Any]],
) -> str:
    primary_growth = {
        row["model"]: row
        for row in growth_summary
        if row["file_set"] == "primary_BAO_plus"
        and row["score_mode"] == "all"
        and not row["excluded_sample"]
    }
    combined_by_model = {row["model"]: row for row in combined_scores}
    cmb_by_model = {row["model"]: row for row in cmb_branches}
    jackknife_lookup = {
        (str(row["excluded_sample"]), str(row["model"])): float(row["chi2"])
        for row in growth_jackknife
        if row["file_set"] == "primary_BAO_plus"
        and row["score_mode"] == "all"
    }
    excluded_samples = sorted(
        {
            str(row["excluded_sample"])
            for row in growth_jackknife
            if row["file_set"] == "primary_BAO_plus"
            and row["score_mode"] == "all"
        }
    )
    jackknife_lines = "\n".join(
        (
            f"| `{sample}` | "
            f"{jackknife_lookup[(sample, 'ParentScalar_Lambda_free')] - jackknife_lookup[(sample, 'wCDM')]:.6g} | "
            f"{jackknife_lookup[(sample, 'ParentScalar_Lambda_free')] - jackknife_lookup[(sample, 'LCDM')]:.6g} |"
        )
        for sample in excluded_samples
    )
    free_minus_wcdm = [
        jackknife_lookup[(sample, "ParentScalar_Lambda_free")]
        - jackknife_lookup[(sample, "wCDM")]
        for sample in excluded_samples
    ]
    free_minus_lcdm = [
        jackknife_lookup[(sample, "ParentScalar_Lambda_free")]
        - jackknife_lookup[(sample, "LCDM")]
        for sample in excluded_samples
    ]
    max_parent_clustering = max(
        abs(float(row["dark_energy_source_fraction"]))
        for row in clustering
        if row["model"] in PARENT_MODELS
        and float(row["k_h_Mpc_inverse"]) >= 0.01
    )
    max_fluid_ppf = max(
        abs(float(row["fractional_difference"])) for row in fluid_ppf
    )
    parent_response_mismatch = max(
        abs(float(row["relative_response_mismatch"]))
        for row in smooth_camb
        if row["model"] in PARENT_MODELS
    )
    o4_envelope = next(
        float(row["value"])
        for row in o4_rows
        if row["input"] == "O4_perturbation_envelope"
    )
    comparison_lines = "\n".join(
        (
            f"| `{row['parent_model']}` | `{row['baseline_model']}` | "
            f"{float(row['delta_growth_chi2']):.6g} | "
            f"{float(row['delta_combined_AIC']):.6g} | "
            f"{float(row['delta_combined_BIC']):.6g} |"
        )
        for row in growth_comparisons
    )
    score_lines = "\n".join(
        (
            f"| `{model}` | {float(primary_growth[model]['chi2']):.9g} | "
            f"{float(primary_growth[model]['distance_alpha']):.9g} | "
            f"{float(primary_growth[model]['sigma8_0']):.9g} | "
            f"{float(combined_by_model[model]['AIC_combined']):.9g} | "
            f"{float(combined_by_model[model]['BIC_combined']):.9g} |"
        )
        for model in MODEL_ORDER
    )
    cmb_lines = "\n".join(
        (
            f"| `{model}` | {float(cmb_by_model[model]['H0_profiled']):.8g} | "
            f"{float(cmb_by_model[model]['chi2_compressed_distance_prior']):.8g} | "
            f"{float(cmb_by_model[model]['R_predicted']):.8g} | "
            f"{float(cmb_by_model[model]['l_A_predicted']):.8g} | "
            f"{float(cmb_by_model[model]['sigma8_0_As_fixed']):.8g} |"
        )
        for model in MODEL_ORDER
    )
    parent_diagnostic_lines = "\n".join(
        (
            f"| `{model}` | "
            f"{backgrounds[model].parent_diagnostics['mu']:.12g} | "
            f"{backgrounds[model].parent_diagnostics['chi_initial_at_N_minus_12']:.12g} | "
            f"{backgrounds[model].parent_diagnostics['present_theta']:.12g} | "
            f"{backgrounds[model].parent_diagnostics['maximum_constraint_residual']:.3e} |"
        )
        for model in PARENT_MODELS
    )
    return f"""# 5194 - Parent Canonical-Scalar Perturbation, Growth, and Compressed-CMB Gate

Private derivation and empirical gate. This is not a public cosmology-support
claim.

Checkpoint marker: `{MARKER}`.

## 1. What changed

Checkpoint 5193 fitted the parent homogeneous scalar but deliberately did not
promote the old smooth-growth proxy. This checkpoint varies the same surviving
low-energy parent action to linear order. The perturbation owner is therefore
no longer missing:

```text
S_O2 = integral sqrt(-g) [
  Mpl^2 (R - 2 Lambda)/2
  - (partial psi)^2/2
  - m_gap^2 psi^2/2
] + S_m[g,Psi].
```

It fixes, rather than fits,

```text
Box psi - m_gap^2 psi = 0,
c_s,rf^2 = 1,
Pi_psi^i_j|TF = 0,
nabla_mu T_m^{{mu nu}} = 0.
```

Thus matter remains metric-geodesic, the scalar has no direct fifth force, and
the scalar contributes no intrinsic linear gravitational slip. Standard
photon/neutrino anisotropic stress is not relabelled as an MTS effect.

## 2. Exact linear scalar equations

With

```text
ds^2=a^2[-(1+2 Psi)deta^2+(1-2 Phi)dx^2],
psi=psi_bar+delta_psi,
```

the parent Klein-Gordon equation gives

```text
delta_psi'' + 2 Hc delta_psi'
+ (k^2+a^2 m_gap^2) delta_psi
- psi_bar'(Psi'+3 Phi')
+ 2 a^2 m_gap^2 psi_bar Psi = 0.
```

The scalar stress perturbations are

```text
delta rho_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  + m_gap^2 psi_bar delta_psi,

delta p_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  - m_gap^2 psi_bar delta_psi,

delta q_psi = -psi_bar' delta_psi/a^2,
Pi_psi = 0.
```

The high-k quadratic action has equal positive time- and space-gradient
coefficients. Therefore the scalar is ghost-free at this order and its
rest-frame sound speed is exactly one. The free-`Lambda` branch can be treated
as one conserved fluid because adding a cosmological constant changes neither
the total momentum nor rest-frame perturbations:

```text
rho_D=rho_psi+rho_Lambda,
p_D=p_psi-rho_Lambda,
1+w_D=dot(psi)^2/rho_D,
c_s,rf^2=1.
```

## 3. Stable early branch

The 5193 backward solution is excellent to `N=-5`, but extending a backwards
shoot to CMB times can amplify its numerically decaying mode. Checkpoint 5194
therefore starts at `N=-12` with the regular radiation-era series

```text
x_i = -(mu/E_i)^2 chi_i / 5
```

and integrates forward, solving `E(0)=1` for `chi_i`. It reproduces the 5193
present branch:

| branch | `mu` | `chi(-12)` | present `theta` | max Friedmann residual |
|---|---:|---:|---:|---:|
{parent_diagnostic_lines}

No closure activation function is used.

## 4. Real SDSS/eBOSS growth test

The primary test uses the source-locked SDSS/eBOSS DR16 `BAO-plus` vectors and
their full per-sample covariance blocks. It contains 14 rows, including five
`f sigma8` measurements. For every model the same two nuisances are solved
analytically in one generalized least-squares system:

```text
alpha_RSD = c/(H0 r_d),
sigma8_0.
```

The smooth subhorizon equation is now the derived canonical-scalar limit,
not a declaration:

```text
D_NN + [2 + d ln H/dN] D_N - 3 Omega_m D/2
  = O[(aH/k)^2].
```

| model | primary chi2 | `alpha_RSD` | `sigma8_0` | combined AIC | combined BIC |
|---|---:|---:|---:|---:|---:|
{score_lines}

The combined columns add this independent primary SDSS/eBOSS compression to
the checkpoint-5193 Pantheon+ and DESI DR2 score. The alternative
`Full-shape-only` compression is a robustness branch and is not double-counted.

Every model is subjected to the same leave-one-sample-out calculation:

| excluded sample | parent-free minus wCDM chi2 | parent-free minus LCDM chi2 |
|---|---:|---:|
{jackknife_lines}

All four reruns keep both profiled nuisances interior. Across these matched
jackknifes the free parent differs from wCDM by
`[{min(free_minus_wcdm):.6g}, {max(free_minus_wcdm):.6g}]` in chi2 and from
LCDM by `[{min(free_minus_lcdm):.6g}, {max(free_minus_lcdm):.6g}]`. This is a
fair baseline stress test: no failure rule is applied only to MTS.

| parent | baseline | delta growth chi2 | delta combined AIC | delta combined BIC |
|---|---|---:|---:|---:|
{comparison_lines}

Negative differences favour the parent row. Absolute information-criterion
differences below about two are treated as draw-scale, not as a knockout.

## 5. Full linear-transfer check

CAMB `{camb.__version__}` evolves the tabulated parent `w(a)` with
`c_s^2=1`. A forward regular background removes the false early kinetic mode
that appeared when a finite-precision backwards solution was extrapolated.
The fluid integrator uses only a numerical floor
`1+w >= {CAMB_W_FLOOR:g}` where the dark fraction is early and negligible.
An exact-table PPF comparator changes normalized `f sigma8` by at most

```text
{max_fluid_ppf:.6e}.
```

Across the tested RSD redshifts, the largest mismatch between the
parent-to-LCDM growth response from CAMB and from the derived subhorizon
equation is

```text
{parent_response_mismatch:.6e}.
```

The largest CAMB difference between total transfer density with and without
dark-energy perturbations on `k >= 0.01 h/Mpc` is

```text
{max_parent_clustering:.6e}.
```

This is a measured transfer diagnostic, not a hand-inserted suppression
factor.

## 6. Compressed CMB gate

The source-locked Planck-2018 distance-prior vector and full covariance are
used only as a conditional diagnostic. `Omega_m` and the late branch stay at
their 5193 values; `Omega_b h^2` and `n_s` are held at the prior means; only
`H0` is profiled. No Planck, ACT, or SPT official likelihood is run.

| model | profiled `H0` | compressed chi2 | `R` | `l_A` | fixed-`A_s` sigma8 |
|---|---:|---:|---:|---:|---:|
{cmb_lines}

CAMB spectra through `ell={CAMB_LMAX}` and transfer functions are finite for
both parent branches. Their spectra residuals are machine outputs for the next
likelihood step, not support evidence.

The compressed diagnostic is adverse to the parent late-only fits:
LCDM gives chi2
`{float(cmb_by_model['LCDM']['chi2_compressed_distance_prior']):.6g}`,
whereas the free-`Lambda` and zero-`Lambda` parent branches give
`{float(cmb_by_model['ParentScalar_Lambda_free']['chi2_compressed_distance_prior']):.6g}`
and
`{float(cmb_by_model['ParentScalar_Lambda_zero']['chi2_compressed_distance_prior']):.6g}`.
This is not an official rejection because the late parameters are frozen and
only `H0` is refitted, but it is real pressure. The next CMB pass must refit
every baseline and parent branch under the same CMB information rather than
explaining this discrepancy away.

## 7. O4 handoff

The largest checkpoint-5193 homogeneous `delta_F` is multiplied by the
deliberately conservative `[(k c)/H0]^4` envelope at
`k={CAMB_KMAX_MPC} Mpc^-1`. The result is

```text
{o4_envelope:.6e}.
```

It remains negligible on this low-energy branch. This does not replace the
all-scale UV-completion boundary.

## 8. Decision

```text
canonical scalar perturbation owner       = derived at O2;
no-ghost principal sign                   = passed;
rest-frame sound speed                    = c_s^2=1 exactly;
intrinsic scalar anisotropic stress       = zero exactly;
direct scalar force on matter             = absent by minimal coupling;
forward regular CMB-time background       = constructed and 5193-matched;
SDSS/eBOSS full-covariance growth test     = executed;
CAMB linear transfer/spectra smoke        = executed;
official CMB likelihood                   = not run;
mass-gap value from parent                = not derived;
homogeneous state selection from parent   = not derived;
full MTS cosmology/unification claim      = false.
```

The correct next target is an official-likelihood-ready parent scalar module
or a parent selection law for `m_gap/H0` and the homogeneous state. The growth
perturbation gap itself is no longer merely listed as missing.

## 9. Machine artifacts

- `source-intake/functional_rg/5194/perturbation_contract.csv`
- `source-intake/functional_rg/5194/parent_scalar_forward_background.csv`
- `source-intake/functional_rg/5194/parent_forward_diagnostics.csv`
- `source-intake/functional_rg/5194/growth_data_schema.csv`
- `source-intake/functional_rg/5194/growth_fit_summary.csv`
- `source-intake/functional_rg/5194/growth_residuals.csv`
- `source-intake/functional_rg/5194/growth_jackknife.csv`
- `source-intake/functional_rg/5194/growth_baseline_comparison.csv`
- `source-intake/functional_rg/5194/combined_SN_DESI_SDSS_scores.csv`
- `source-intake/functional_rg/5194/compressed_CMB_profile.csv`
- `source-intake/functional_rg/5194/CAMB_branch_summary.csv`
- `source-intake/functional_rg/5194/CAMB_fluid_PPF_convergence.csv`
- `source-intake/functional_rg/5194/CAMB_vs_smooth_growth.csv`
- `source-intake/functional_rg/5194/CAMB_dark_energy_clustering.csv`
- `source-intake/functional_rg/5194/CAMB_spectra_residual_summary.csv`
- `source-intake/functional_rg/5194/O4_perturbation_envelope.csv`
- `source-intake/functional_rg/5194/source_provenance.csv`
- `source-intake/functional_rg/5194/parent_scalar_perturbation_growth_CMB_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5194_VALIDATION.csv`
"""


def validation_rows(
    backgrounds: dict[str, Background],
    growth_summary: list[dict[str, Any]],
    growth_comparisons: list[dict[str, Any]],
    compressed_cmb: list[dict[str, Any]],
    camb_branches: list[dict[str, Any]],
    fluid_ppf: list[dict[str, Any]],
    smooth_camb: list[dict[str, Any]],
    clustering: list[dict[str, Any]],
    spectra: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    o4_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    for source_id, path, expected_hash in LOCKED_5193:
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
            f"expected={CHECKPOINT_5176_LOCK};actual={checkpoint_5176_hash}",
        )
    )
    checks.append(
        (
            "all_local_sources_exist",
            all(
                bool(row["exists"])
                for row in provenance
                if row["provenance_status"] == "LOCAL_SOURCE_LOCK"
            ),
            "all local provenance rows must exist",
        )
    )
    checks.append(
        (
            "parent_forward_profiles_present",
            all(model in backgrounds for model in PARENT_MODELS),
            ";".join(PARENT_MODELS),
        )
    )
    for model in PARENT_MODELS:
        diagnostics = backgrounds[model].parent_diagnostics
        checks.extend(
            [
                (
                    f"{model}_present_flatness",
                    abs(float(diagnostics["present_E"]) - 1.0) < 1.0e-10,
                    str(diagnostics["present_E"]),
                ),
                (
                    f"{model}_density_match",
                    abs(
                        float(diagnostics["present_scalar_density"])
                        - float(
                            diagnostics["target_present_scalar_density"]
                        )
                    )
                    < 1.0e-10,
                    (
                        f"actual={diagnostics['present_scalar_density']};"
                        f"target={diagnostics['target_present_scalar_density']}"
                    ),
                ),
                (
                    f"{model}_theta_matches_5193",
                    abs(float(diagnostics["theta_difference"])) < 1.0e-7,
                    str(diagnostics["theta_difference"]),
                ),
                (
                    f"{model}_Friedmann_constraint",
                    float(diagnostics["maximum_constraint_residual"])
                    < 1.0e-12,
                    str(diagnostics["maximum_constraint_residual"]),
                ),
                (
                    f"{model}_nonphantom",
                    float(diagnostics["minimum_one_plus_w_dark"])
                    >= -1.0e-12,
                    str(diagnostics["minimum_one_plus_w_dark"]),
                ),
            ]
        )
    checks.append(
        (
            "growth_all_models_primary",
            len(
                [
                    row
                    for row in growth_summary
                    if row["file_set"] == "primary_BAO_plus"
                    and row["score_mode"] == "all"
                ]
            )
            == len(MODEL_ORDER),
            f"rows={len(growth_summary)}",
        )
    )
    checks.append(
        (
            "growth_no_nuisance_edges",
            not any(bool(row["nuisance_edge_flag"]) for row in growth_summary),
            "all alpha and sigma8 profiles interior",
        )
    )
    checks.append(
        (
            "growth_scores_finite",
            all(math.isfinite(float(row["chi2"])) for row in growth_summary),
            f"rows={len(growth_summary)}",
        )
    )
    checks.append(
        (
            "growth_comparisons_complete",
            len(growth_comparisons) == 6,
            f"rows={len(growth_comparisons)}",
        )
    )
    checks.append(
        (
            "compressed_CMB_all_models",
            len(compressed_cmb) == len(MODEL_ORDER),
            f"rows={len(compressed_cmb)}",
        )
    )
    checks.append(
        (
            "compressed_CMB_no_H0_edges",
            not any(bool(row["H0_edge_flag"]) for row in compressed_cmb),
            "all H0 profiles interior",
        )
    )
    checks.append(
        (
            "CAMB_all_transfers_pass",
            len(camb_branches) == len(MODEL_ORDER)
            and all(row["transfer_status"] == "PASS" for row in camb_branches),
            f"CAMB={camb.__version__};rows={len(camb_branches)}",
        )
    )
    max_fluid_ppf = max(
        abs(float(row["fractional_difference"])) for row in fluid_ppf
    )
    checks.append(
        (
            "parent_fluid_PPF_convergence",
            max_fluid_ppf < 1.0e-5,
            f"max_fractional_difference={max_fluid_ppf}",
        )
    )
    max_response_mismatch = max(
        abs(float(row["relative_response_mismatch"]))
        for row in smooth_camb
        if row["model"] in PARENT_MODELS
    )
    checks.append(
        (
            "parent_smooth_growth_relative_response",
            max_response_mismatch < 5.0e-3,
            f"max_relative_response_mismatch={max_response_mismatch}",
        )
    )
    max_clustering = max(
        abs(float(row["dark_energy_source_fraction"]))
        for row in clustering
        if row["model"] in PARENT_MODELS
        and float(row["k_h_Mpc_inverse"]) >= 0.01
    )
    checks.append(
        (
            "parent_dark_energy_clustering_subhorizon",
            max_clustering < 5.0e-3,
            f"max_source_fraction={max_clustering}",
        )
    )
    checks.append(
        (
            "spectra_generated",
            len(spectra) == len(MODEL_ORDER) * 3,
            f"rows={len(spectra)}",
        )
    )
    o4_envelope = next(
        float(row["value"])
        for row in o4_rows
        if row["input"] == "O4_perturbation_envelope"
    )
    checks.append(
        (
            "O4_perturbation_envelope_negligible",
            o4_envelope < 1.0e-200,
            f"envelope={o4_envelope}",
        )
    )
    checks.append(
        (
            "official_CMB_claim_blocked",
            all(not bool(row["official_likelihood_run"]) for row in compressed_cmb),
            "no official Planck/ACT/SPT likelihood was called",
        )
    )
    checks.append(
        (
            "full_MTS_claim_blocked",
            all(
                not bool(row["valid_for_full_MTS_claim"])
                for row in [
                    *growth_summary,
                    *compressed_cmb,
                    *camb_branches,
                ]
            ),
            "checkpoint remains internal and conditional",
        )
    )
    public_worktree = (
        Path.home()
        / "OneDrive"
        / "Documents"
        / "Motion-TimeSpace-public-update-2026-07-22"
    )
    if public_worktree.exists():
        status = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={public_worktree.as_posix()}",
                "status",
                "--porcelain",
            ],
            cwd=public_worktree,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        checks.append(
            (
                "public_worktree_clean",
                status == "",
                status or "clean",
            )
        )
    checks.append(
        (
            "no_script_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            str(POST / "scripts" / "__pycache__"),
        )
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result_5193 = load_5193_result()
    backgrounds = build_backgrounds(result_5193)
    perturbation_rows = perturbation_contract_rows()
    growth_solutions = {
        model: solve_smooth_growth(backgrounds[model])
        for model in MODEL_ORDER
    }
    (
        growth_summary,
        growth_residuals,
        growth_jackknife,
        growth_schema,
    ) = growth_scores(backgrounds, growth_solutions)
    growth_comparisons, combined_scores = growth_comparison_rows(
        growth_summary,
        result_5193,
    )
    (
        compressed_cmb,
        camb_branches,
        fluid_ppf,
        smooth_camb,
        clustering,
        spectra,
        camb_diagnostics,
    ) = camb_analysis(backgrounds, growth_solutions)
    o4_rows = o4_envelope_rows()
    provenance = source_provenance_rows()
    scalar_rows = tagged(
        [
            row
            for model in PARENT_MODELS
            for row in backgrounds[model].scalar_rows
        ]
    )
    parent_diagnostics = tagged(
        [
            {
                "model": model,
                **backgrounds[model].parent_diagnostics,
            }
            for model in PARENT_MODELS
        ]
    )

    outputs = {
        "perturbation_contract.csv": perturbation_rows,
        "parent_scalar_forward_background.csv": scalar_rows,
        "parent_forward_diagnostics.csv": parent_diagnostics,
        "growth_data_schema.csv": growth_schema,
        "growth_fit_summary.csv": growth_summary,
        "growth_residuals.csv": growth_residuals,
        "growth_jackknife.csv": growth_jackknife,
        "growth_baseline_comparison.csv": growth_comparisons,
        "combined_SN_DESI_SDSS_scores.csv": combined_scores,
        "compressed_CMB_profile.csv": compressed_cmb,
        "CAMB_branch_summary.csv": camb_branches,
        "CAMB_fluid_PPF_convergence.csv": fluid_ppf,
        "CAMB_vs_smooth_growth.csv": smooth_camb,
        "CAMB_dark_energy_clustering.csv": clustering,
        "CAMB_spectra_residual_summary.csv": spectra,
        "O4_perturbation_envelope.csv": o4_rows,
        "source_provenance.csv": provenance,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    document_text = build_document(
        backgrounds,
        growth_summary,
        growth_jackknife,
        growth_comparisons,
        combined_scores,
        camb_branches,
        fluid_ppf,
        smooth_camb,
        clustering,
        o4_rows,
    )
    DOCUMENT.write_text(document_text, encoding="utf-8")

    validation = validation_rows(
        backgrounds,
        growth_summary,
        growth_comparisons,
        compressed_cmb,
        camb_branches,
        fluid_ppf,
        smooth_camb,
        clustering,
        spectra,
        provenance,
        o4_rows,
    )
    write_csv(VALIDATION, validation)
    failed_checks = [
        row for row in validation if row["status"] != "PASS"
    ]
    result_payload = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "theorem": "THE_SURVIVING_O2_PARENT_CANONICAL_SCALAR_FIXES_THE_LINEAR_PERTURBATION_OWNER_WITH_CS2_ONE_ZERO_INTRINSIC_ANISOTROPIC_STRESS_AND_MINIMAL_METRIC_MATTER_COUPLING_SO_THE_SDSS_GROWTH_LIMIT_CAN_BE_TESTED_WITHOUT_A_MEMORY_CLOSURE_AXIOM",
        "claim_guard": "NO_OFFICIAL_CMB_LIKELIHOOD_NO_DERIVATION_OF_MASS_GAP_NO_DERIVATION_OF_HOMOGENEOUS_STATE_NO_FULL_MTS_COSMOLOGY_OR_UNIFICATION_CLAIM",
        "formalization_workbench_sha256": tree_digest(FORMAL),
        "checkpoint_5176_tree_sha256": tree_digest(CHECKPOINT_5176),
        "CAMB_version": camb.__version__,
        "models": list(MODEL_ORDER),
        "parent_models": list(PARENT_MODELS),
        "parent_diagnostics": {
            model: backgrounds[model].parent_diagnostics
            for model in PARENT_MODELS
        },
        "primary_growth": {
            row["model"]: {
                key: row[key]
                for key in (
                    "chi2",
                    "n_data",
                    "distance_alpha",
                    "sigma8_0",
                    "nuisance_edge_flag",
                )
            }
            for row in growth_summary
            if row["file_set"] == "primary_BAO_plus"
            and row["score_mode"] == "all"
        },
        "combined_scores": {
            row["model"]: {
                key: row[key]
                for key in (
                    "chi2_combined",
                    "k_combined",
                    "AIC_combined",
                    "BIC_combined",
                )
            }
            for row in combined_scores
        },
        "compressed_CMB": {
            row["model"]: {
                key: row[key]
                for key in (
                    "H0_profiled",
                    "chi2_compressed_distance_prior",
                    "R_predicted",
                    "l_A_predicted",
                )
            }
            for row in camb_branches
        },
        "CAMB_diagnostics": camb_diagnostics,
        "validation_passed": len(failed_checks) == 0,
        "validation_failures": [
            {
                "check": row["check"],
                "detail": row["detail"],
            }
            for row in failed_checks
        ],
        "generated": sorted(
            [
                *outputs.keys(),
                DOCUMENT.name,
                VALIDATION.name,
            ]
        ),
        "next_target": "5195 parent mass-state selection law or official-likelihood-ready scalar implementation with fair baseline refits",
    }
    result_path = OUT / "parent_scalar_perturbation_growth_CMB_results.json"
    write_json(result_path, result_payload)
    if failed_checks:
        raise SystemExit(
            "5194 validation failed: "
            + "; ".join(
                f"{row['check']}={row['detail']}" for row in failed_checks
            )
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "checkpoint": 5194,
                "result": str(result_path),
                "validation_rows": len(validation),
                "generated_files": len(outputs) + 3,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
