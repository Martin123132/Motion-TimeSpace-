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
from typing import Any, Callable

sys.dont_write_bytecode = True

import numpy as np
import sympy as sp
from scipy import integrate, linalg, optimize


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5207"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5207_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5207-Y5-R2FR-Cavendish-normalized-parent-scale-observed-density-map-"
    "and-self-consistent-source-calibrated-refit.md"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPOSITORY = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

CHECKPOINT = 5207
CHECKED_DATE = "2026-07-24"
MARKER = "MTS_5207_CAVENDISH_SOURCE_CALIBRATED_REFIT"
FORMAL_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"
GALAXY_STATUS_LOCK = "21838b41dd2617e2de312ea2620c225022cc2f70d85b4a78d75dcb1cc727ff39"

SOURCE_LOCKS = (
    (
        POST
        / "5206-Y5-R2FR-constraint-reduced-zero-Lambda-Jordan-scalar-tensor-"
        "refit-local-Gdot-and-competitive-model-gate.md",
        "2e573b6e7027840b6289b647fc27c966caf39f507fe20bd3422e3f3ab810258e",
    ),
    (
        POST
        / "scripts"
        / "Y5_R2FR_5206_constraint_reduced_scalar_tensor_refit.py",
        "da79179a8ad55644cc952ca29972e6d3b44f8e8f08e6586675a3170c971ceedc",
    ),
    (
        POST
        / "source-intake"
        / "functional_rg"
        / "5206"
        / "constraint_reduced_scalar_tensor_results.json",
        "aa09f6859f23954551e44b81e672500099649493964fa7cc9b02a27584d8ddd4",
    ),
    (
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_BRR545_5206_VALIDATION.csv",
        "e46b85c24f42415363f1781306c8541a34c2b02d2f9ce4876d40d4f30ab8ff55",
    ),
)

sys.path.insert(0, str(POST / "scripts"))
import Y5_R2FR_5206_constraint_reduced_scalar_tensor_refit as checkpoint_5206


OMEGA_R_OBSERVED = checkpoint_5206.OMEGA_R
C_KM_S = checkpoint_5206.C_KM_S
H0_TO_YEAR_INV = checkpoint_5206.H0_TO_YEAR_INV
N_INITIAL = checkpoint_5206.N_INITIAL
N_OUTPUT = checkpoint_5206.N_OUTPUT
PRIMARY_N_COSMOLOGY = checkpoint_5206.PRIMARY_N_COSMOLOGY
PRIMARY_N_WITH_LOCAL = checkpoint_5206.PRIMARY_N_WITH_LOCAL
SIGNED_MODEL = "ParentST_Lambda_zero_signed_zeta"
CALIBRATED_MODEL = "ParentST_Lambda_zero_Cavendish_calibrated"
RESULT_5206 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5206"
    / "constraint_reduced_scalar_tensor_results.json"
)


@dataclass
class CalibratedSolution:
    solution: checkpoint_5206.STSolution
    scale_ratio: float
    omega_m_bare: float
    omega_r_bare: float


BACKGROUND_CACHE: dict[tuple[Any, ...], CalibratedSolution] = {}
SCORE_CACHE: dict[tuple[Any, ...], dict[str, Any]] = {}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            allow_nan=False,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_cosmology_support_claim": False,
            "valid_for_full_MTS_claim": False,
            **row,
        }
        for row in rows
    ]


def git_state(repository: Path) -> tuple[str, str]:
    head = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={repository}",
            "-C",
            str(repository),
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
            f"safe.directory={repository}",
            "-C",
            str(repository),
            "status",
            "--short",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return head, status


def assert_source_locks() -> None:
    for path, expected in SOURCE_LOCKS:
        if not path.exists():
            raise FileNotFoundError(path)
        actual = file_digest(path)
        if actual != expected:
            raise RuntimeError(
                f"source lock failed for {path}: expected {expected}, got {actual}"
            )


def load_5206() -> dict[str, Any]:
    return json.loads(RESULT_5206.read_text(encoding="utf-8"))


def symbolic_source_map() -> tuple[list[dict[str, Any]], dict[str, str]]:
    g_zero, m_r_squared, m_n_squared, omega_observed, geff = sp.symbols(
        "g0 M_R_squared M_N_squared Omega_observed G_eff",
        positive=True,
    )
    scale_ratio = sp.simplify(g_zero)
    omega_bare = sp.simplify(omega_observed / scale_ratio)
    present_source = sp.simplify(
        omega_bare * geff / omega_observed
    ).subs(geff, g_zero)
    calibration_residual = sp.simplify(
        g_zero / m_r_squared - 1 / m_n_squared
    ).subs(m_r_squared, g_zero * m_n_squared)
    rows = tagged(
        [
            {
                "item": "measured_Newton_scale",
                "formula": "M_N^2=1/(8 pi G_N)",
                "status": "EXTERNAL_DIMENSIONFUL_CALIBRATION",
                "implication": "the numerical magnitude of G_N is not derived here",
            },
            {
                "item": "parent_Cavendish_prediction",
                "formula": (
                    "G_cav,0=[g0/(8 pi M_R^2)]; "
                    "g0=[(2f0+4f_phi0^2)/(2f0+3f_phi0^2)]/f0"
                ),
                "status": "DERIVED_FROM_PARENT_ACTION",
                "implication": "no second independent Newton normalization is inserted",
            },
            {
                "item": "parent_scale_calibration",
                "formula": "s=M_R^2/M_N^2=g0",
                "status": "EXACT_ALGEBRAIC_MAP",
                "implication": "the parent Planck scale is fixed relative to measured G_N",
            },
            {
                "item": "observed_to_bare_density",
                "formula": "Omega_i,bare=Omega_i,observed/s",
                "status": "EXACT_UNIT_CONVERSION",
                "implication": "the Friedmann source uses the action scale rather than an observed-scale shortcut",
            },
            {
                "item": "growth_source",
                "formula": (
                    "(3/2)Omega_m,bare(a^-3/E^2)(G_eff/G_bare)"
                ),
                "status": "DERIVED_QUASISTATIC_SOURCE",
                "implication": "at N=0 it becomes (3/2)Omega_m,observed",
            },
            {
                "item": "present_source_residual",
                "formula": str(sp.simplify(present_source - 1)),
                "status": "EXACT_ZERO",
                "implication": "the present Poisson source is normalized to measured G_N",
            },
            {
                "item": "Cavendish_calibration_residual",
                "formula": str(calibration_residual),
                "status": "EXACT_ZERO",
                "implication": "G_cav,0=G_N after s=g0",
            },
            {
                "item": "local_GR_branch",
                "formula": "phi_local=0 -> g_local=1 -> s=1",
                "status": "CONDITIONAL_BRANCH",
                "implication": "requires a derived local transition if cosmological phi0 is nonzero",
            },
        ]
    )
    return rows, {
        "scale_ratio": str(scale_ratio),
        "omega_bare": str(omega_bare),
        "present_source_residual": str(sp.simplify(present_source - 1)),
        "calibration_residual": str(calibration_residual),
    }


def field_quantities(
    n_value: float,
    phi_value: float,
    q_value: float,
    omega_m_bare: float,
    omega_r_bare: float,
    mu_value: float,
    zeta: float,
) -> dict[str, float]:
    reduced_f = 1.0 + zeta * phi_value**2
    reduced_f_n = 2.0 * zeta * phi_value * q_value
    denominator = reduced_f + reduced_f_n - q_value**2 / 6.0
    numerator = (
        omega_m_bare * math.exp(-3.0 * n_value)
        + omega_r_bare * math.exp(-4.0 * n_value)
        + mu_value**2 * phi_value**2 / 6.0
    )
    if reduced_f <= 0.0 or denominator <= 0.0 or numerator <= 0.0:
        raise ValueError("left the calibrated positive-F Hamiltonian branch")
    e_squared = numerator / denominator
    omega_m_n = (
        omega_m_bare * math.exp(-3.0 * n_value) / e_squared
    )
    omega_r_n = (
        omega_r_bare * math.exp(-4.0 * n_value) / e_squared
    )
    h_value = -(
        3.0 * omega_m_n
        + 4.0 * omega_r_n
        + (1.0 + 2.0 * zeta) * q_value**2
        - 8.0 * zeta * phi_value * q_value
        - 2.0 * zeta * mu_value**2 * phi_value**2 / e_squared
        + 24.0 * zeta**2 * phi_value**2
    ) / (
        2.0 * reduced_f + 12.0 * zeta**2 * phi_value**2
    )
    q_n = (
        -(3.0 + h_value) * q_value
        - mu_value**2 * phi_value / e_squared
        + 6.0 * zeta * phi_value * (2.0 + h_value)
    )
    return {
        "E2": e_squared,
        "h": h_value,
        "qN": q_n,
        "f": reduced_f,
        "fN": reduced_f_n,
        "denominator": denominator,
        "Omega_m": omega_m_n,
        "Omega_r": omega_r_n,
    }


def integrate_trial(
    log_amplitude: float,
    log_scale_ratio: float,
    params: dict[str, float],
    zeta: float,
    accuracy: str,
    n_initial: float,
    dense_output: bool,
) -> tuple[Any, dict[str, float]]:
    amplitude = math.exp(log_amplitude)
    scale_ratio = math.exp(log_scale_ratio)
    omega_m_bare = float(params["Omega_m"]) / scale_ratio
    omega_r_bare = OMEGA_R_OBSERVED / scale_ratio
    mu_value = 10.0 ** float(params["log10_mu"])
    scale_factor = math.exp(n_initial)
    regular_ratio = (
        1.5
        * zeta
        * (float(params["Omega_m"]) / OMEGA_R_OBSERVED)
        * scale_factor
        - mu_value**2 * scale_factor**4 / (5.0 * omega_r_bare)
    )
    if accuracy == "fit":
        rtol, atol, max_step = 3.0e-8, 3.0e-10, 0.1
    elif accuracy == "exact":
        rtol, atol, max_step = 2.0e-11, 2.0e-13, 0.03
    else:
        raise ValueError(accuracy)

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        quantities = field_quantities(
            float(n_value),
            float(state[0]),
            float(state[1]),
            omega_m_bare,
            omega_r_bare,
            mu_value,
            zeta,
        )
        return np.asarray([state[1], quantities["qN"]], dtype=float)

    solution = integrate.solve_ivp(
        rhs,
        (n_initial, 0.0),
        np.asarray([amplitude, regular_ratio * amplitude], dtype=float),
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=dense_output,
    )
    if not solution.success:
        raise ValueError(solution.message)
    phi_zero = float(solution.y[0, -1])
    q_zero = float(solution.y[1, -1])
    e_squared = field_quantities(
        0.0,
        phi_zero,
        q_zero,
        omega_m_bare,
        omega_r_bare,
        mu_value,
        zeta,
    )["E2"]
    gcav_ratio = checkpoint_5206.checkpoint_5204.gcav_ratio(
        zeta,
        phi_zero,
    )
    return solution, {
        "amplitude": amplitude,
        "scale_ratio": scale_ratio,
        "omega_m_bare": omega_m_bare,
        "omega_r_bare": omega_r_bare,
        "mu": mu_value,
        "regular_ratio": regular_ratio,
        "phi0": phi_zero,
        "q0": q_zero,
        "E2_0": e_squared,
        "Gcav_over_Gbare_0": gcav_ratio,
        "flatness_log_residual": math.log(e_squared),
        "calibration_log_residual": math.log(scale_ratio / gcav_ratio),
    }


def solve_calibrated_background(
    params: dict[str, float],
    zeta: float,
    accuracy: str = "fit",
    n_initial: float = N_INITIAL,
) -> CalibratedSolution:
    key = (
        round(float(params["Omega_m"]), 10),
        round(float(params["log10_mu"]), 10),
        round(float(params["H0"]), 8),
        round(float(params["Omega_b_h2"]), 10),
        round(float(zeta), 12),
        accuracy,
        float(n_initial),
    )
    if key in BACKGROUND_CACHE:
        return BACKGROUND_CACHE[key]
    uncalibrated = checkpoint_5206.solve_st_background(
        params,
        zeta,
        accuracy=accuracy,
        n_initial=n_initial,
    )
    initial_vector = np.log(
        [
            uncalibrated.diagnostics["initial_phi_amplitude"],
            uncalibrated.diagnostics["Gcav_over_Gbare_0"],
        ]
    )

    def residual(vector: np.ndarray) -> np.ndarray:
        _, diagnostics = integrate_trial(
            float(vector[0]),
            float(vector[1]),
            params,
            zeta,
            accuracy,
            n_initial,
            dense_output=False,
        )
        return np.asarray(
            [
                diagnostics["flatness_log_residual"],
                diagnostics["calibration_log_residual"],
            ],
            dtype=float,
        )

    tolerance = 2.0e-9 if accuracy == "fit" else 2.0e-12
    root = optimize.root(
        residual,
        initial_vector,
        method="hybr",
        tol=tolerance,
    )
    if not root.success or float(np.max(np.abs(root.fun))) > 2.0e-8:
        raise ValueError(
            f"coupled flatness/Cavendish solve failed: {root.message}"
        )
    solution, trial = integrate_trial(
        float(root.x[0]),
        float(root.x[1]),
        params,
        zeta,
        accuracy,
        n_initial,
        dense_output=True,
    )
    n_grid = (
        N_OUTPUT
        if n_initial == N_INITIAL
        else np.linspace(n_initial, 0.0, int(round(-n_initial / 0.005)) + 1)
    )
    states = solution.sol(n_grid)
    phi_grid = np.asarray(states[0], dtype=float)
    q_grid = np.asarray(states[1], dtype=float)
    e_grid = np.empty_like(n_grid)
    h_grid = np.empty_like(n_grid)
    omega_dark_grid = np.empty_like(n_grid)
    w_dark_grid = np.empty_like(n_grid)
    f_grid = np.empty_like(n_grid)
    denominator_grid = np.empty_like(n_grid)
    constraint_grid = np.empty_like(n_grid)
    for index, (n_value, phi_value, q_value) in enumerate(
        zip(n_grid, phi_grid, q_grid, strict=True)
    ):
        quantities = field_quantities(
            float(n_value),
            float(phi_value),
            float(q_value),
            trial["omega_m_bare"],
            trial["omega_r_bare"],
            trial["mu"],
            zeta,
        )
        e_squared = quantities["E2"]
        e_grid[index] = math.sqrt(e_squared)
        h_grid[index] = quantities["h"]
        omega_dark = 1.0 - quantities["Omega_m"] - quantities["Omega_r"]
        omega_dark_grid[index] = omega_dark
        pressure_numerator = (
            -2.0 * quantities["h"]
            - 3.0 * quantities["Omega_m"]
            - 4.0 * quantities["Omega_r"]
        )
        w_dark_grid[index] = (
            -1.0 + pressure_numerator / (3.0 * omega_dark)
            if abs(omega_dark) > 1.0e-12
            else -1.0
        )
        f_grid[index] = quantities["f"]
        denominator_grid[index] = quantities["denominator"]
        left = e_squared * (
            quantities["f"]
            + quantities["fN"]
            - float(q_value) ** 2 / 6.0
        )
        right = (
            trial["omega_m_bare"] * math.exp(-3.0 * float(n_value))
            + trial["omega_r_bare"] * math.exp(-4.0 * float(n_value))
            + trial["mu"] ** 2 * float(phi_value) ** 2 / 6.0
        )
        constraint_grid[index] = (left - right) / max(
            abs(left),
            abs(right),
            1.0,
        )
    geff_grid = np.asarray(
        [
            checkpoint_5206.checkpoint_5204.gcav_ratio(
                zeta,
                float(phi_value),
            )
            for phi_value in phi_grid
        ],
        dtype=float,
    )
    h_numeric = np.gradient(np.log(e_grid), n_grid, edge_order=2)
    phi_zero = float(phi_grid[-1])
    q_zero = float(q_grid[-1])
    gdot = (
        checkpoint_5206.checkpoint_5204.dln_gcav_dphi(zeta, phi_zero)
        * q_zero
        * float(params["H0"])
        * H0_TO_YEAR_INV
    )
    source_normalization = (
        trial["omega_m_bare"]
        * geff_grid[-1]
        / float(params["Omega_m"])
    )
    initial_matter_ratio = (
        float(params["Omega_m"])
        * math.exp(n_initial)
        / OMEGA_R_OBSERVED
    )
    regular_remainder_bound = (
        abs(zeta) * initial_matter_ratio**2
        + trial["mu"] ** 2
        * math.exp(5.0 * n_initial)
        / trial["omega_r_bare"]
    )
    background = checkpoint_5206.checkpoint_5195.checkpoint_5194.Background(
        model="ParentScalar_Lambda_zero",
        omega_m=trial["omega_m_bare"],
        parameters=dict(params),
        n_grid=n_grid,
        e_grid=e_grid,
        h_grid=h_grid,
        w_dark_grid=w_dark_grid,
        omega_dark_grid=omega_dark_grid,
        parent_owned=True,
        scalar_rows=[],
        parent_diagnostics={},
    )
    diagnostics = {
        "method": "coupled_flatness_and_Cavendish_source_calibration_shoot",
        "accuracy": accuracy,
        "n_initial": n_initial,
        "mu": trial["mu"],
        "zeta": zeta,
        "initial_phi_amplitude": trial["amplitude"],
        "initial_regular_q_over_phi": trial["regular_ratio"],
        "regular_series_remainder_bound": regular_remainder_bound,
        "coupled_root_evaluations": int(root.nfev),
        "coupled_root_max_residual": float(np.max(np.abs(root.fun))),
        "scale_ratio_MR2_over_MN2": trial["scale_ratio"],
        "MR_over_MN": math.sqrt(trial["scale_ratio"]),
        "Gbare_over_GN": 1.0 / trial["scale_ratio"],
        "Omega_m_observed": float(params["Omega_m"]),
        "Omega_m_bare": trial["omega_m_bare"],
        "Omega_r_observed": OMEGA_R_OBSERVED,
        "Omega_r_bare": trial["omega_r_bare"],
        "phi0": phi_zero,
        "q0": q_zero,
        "theta0": math.atan2(-q_zero, trial["mu"] * phi_zero),
        "E0": float(e_grid[-1]),
        "h0": float(h_grid[-1]),
        "minimum_f": float(np.min(f_grid)),
        "minimum_Hamiltonian_denominator": float(np.min(denominator_grid)),
        "minimum_Einstein_kinetic": float(
            np.min(
                1.0 / f_grid
                + 1.5 * (2.0 * zeta * phi_grid / f_grid) ** 2
            )
        ),
        "maximum_constraint_residual": float(np.max(np.abs(constraint_grid))),
        "maximum_h_derivative_residual": float(
            np.max(np.abs(h_numeric[2:-2] - h_grid[2:-2]))
        ),
        "alpha_squared_0": (
            checkpoint_5206.checkpoint_5204.alpha_squared(zeta, phi_zero)
        ),
        "gamma_minus_one_0": (
            checkpoint_5206.checkpoint_5204.gamma_minus_one(zeta, phi_zero)
        ),
        "Gcav_over_Gbare_0": float(geff_grid[-1]),
        "Gdot_over_G_yr_inv": gdot,
        "present_Poisson_source_ratio": source_normalization,
        "Geff_over_GN_minimum": float(
            np.min(geff_grid / trial["scale_ratio"])
        ),
        "Geff_over_GN_maximum": float(
            np.max(geff_grid / trial["scale_ratio"])
        ),
    }
    background.parent_diagnostics = dict(diagnostics)
    st_solution = checkpoint_5206.STSolution(
        background=background,
        phi_grid=phi_grid,
        q_grid=q_grid,
        geff_grid=geff_grid,
        diagnostics=diagnostics,
    )
    payload = CalibratedSolution(
        solution=st_solution,
        scale_ratio=trial["scale_ratio"],
        omega_m_bare=trial["omega_m_bare"],
        omega_r_bare=trial["omega_r_bare"],
    )
    BACKGROUND_CACHE[key] = payload
    return payload


def score_calibrated(
    params: dict[str, float],
    zeta: float,
    data: checkpoint_5206.checkpoint_5195.JointData,
    accuracy: str = "fit",
    detail: bool = False,
) -> dict[str, Any]:
    key = (
        round(float(params["Omega_m"]), 10),
        round(float(params["log10_mu"]), 10),
        round(float(params["H0"]), 8),
        round(float(params["Omega_b_h2"]), 10),
        round(float(zeta), 12),
        accuracy,
    )
    if not detail and key in SCORE_CACHE:
        return SCORE_CACHE[key]
    calibrated = solve_calibrated_background(
        params,
        zeta,
        accuracy=accuracy,
    )
    solution = calibrated.solution
    calibration = checkpoint_5206.scalar_tensor_calibration(
        solution,
        params,
    )
    physical_alpha = C_KM_S / (
        float(params["H0"]) * calibration["rdrag_Mpc"]
    )
    late = checkpoint_5206.checkpoint_5195.profile_sn_and_desi(
        solution.background,
        data.late,
        physical_alpha,
        detail=detail,
    )
    growth = checkpoint_5206.profile_growth_st(
        solution,
        data.growth_blocks,
        detail=detail,
        normalize_to_present_gcav=False,
    )
    cmb = checkpoint_5206.checkpoint_5195.profile_cmb_prior(
        data.planck_priors[
            checkpoint_5206.checkpoint_5195.PRIMARY_CONFIG.planck_prior_model
        ],
        calibration,
        float(params["Omega_b_h2"]),
    )
    local = checkpoint_5206.local_score(solution)
    chi2_cosmology = (
        float(late["chi2_SN"])
        + float(late["chi2_DESI"])
        + float(growth["chi2_growth"])
        + float(cmb["chi2_CMB"])
    )
    chi2_joint = chi2_cosmology + float(local["chi2_local"])
    payload = {
        "params": dict(params),
        "zeta": zeta,
        "chi2_SN": float(late["chi2_SN"]),
        "chi2_DESI": float(late["chi2_DESI"]),
        "chi2_growth": float(growth["chi2_growth"]),
        "chi2_CMB": float(cmb["chi2_CMB"]),
        "chi2_cosmology": chi2_cosmology,
        "chi2_Cassini": float(local["chi2_Cassini"]),
        "chi2_LLR_Gdot": float(local["chi2_LLR_Gdot"]),
        "chi2_local": float(local["chi2_local"]),
        "chi2_joint": chi2_joint,
        "n_s_profiled": float(cmb["n_s_profiled"]),
        "n_s_edge_flag": bool(cmb["n_s_edge_flag"]),
        "sigma8_0_profiled": float(growth["sigma8_0_profiled"]),
        "sigma8_edge_flag": bool(growth["sigma8_edge_flag"]),
        "R": float(calibration["R"]),
        "l_A": float(calibration["l_A"]),
        "rdrag_Mpc": float(calibration["rdrag_Mpc"]),
        "rstar_Mpc": float(calibration["rstar_Mpc"]),
        "background_diagnostics": dict(solution.diagnostics),
        "local": local,
        "calibration": calibration,
        "growth_residual_rows": growth["residual_rows"] if detail else [],
        "solution": solution if detail else None,
    }
    if not math.isfinite(chi2_joint):
        raise ValueError("non-finite calibrated score")
    if not detail:
        SCORE_CACHE[key] = payload
    return payload


def parameter_vector(params: dict[str, float], zeta: float) -> np.ndarray:
    return np.asarray(
        [
            params["Omega_m"],
            params["log10_mu"],
            params["H0"],
            params["Omega_b_h2"],
            zeta,
        ],
        dtype=float,
    )


def vector_parameters(vector: np.ndarray) -> tuple[dict[str, float], float]:
    return (
        {
            "Omega_m": float(vector[0]),
            "log10_mu": float(vector[1]),
            "H0": float(vector[2]),
            "Omega_b_h2": float(vector[3]),
            "f_scalar": 1.0,
        },
        float(vector[4]),
    )


def fit_calibrated(
    data: checkpoint_5206.checkpoint_5195.JointData,
    source_fit: dict[str, Any],
) -> dict[str, Any]:
    priors = (
        (0.15, 0.45),
        (-2.0, math.log10(5.0)),
        checkpoint_5206.checkpoint_5195.H0_BOUNDS,
        checkpoint_5206.checkpoint_5195.OMBH2_BOUNDS,
        (-0.002, 0.002),
    )
    source_params = {
        key: float(value) for key, value in source_fit["params"].items()
    }
    starts = (
        parameter_vector(source_params, float(source_fit["zeta"])),
        parameter_vector(source_params, 0.0),
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
            params, zeta = vector_parameters(vector)
            value = score_calibrated(
                params,
                zeta,
                data,
                accuracy="fit",
                detail=False,
            )["chi2_joint"]
        except (
            ValueError,
            RuntimeError,
            OverflowError,
            FloatingPointError,
            linalg.LinAlgError,
            checkpoint_5206.checkpoint_5195.camb.baseconfig.CAMBError,
        ) as exc:
            name = type(exc).__name__
            failures[name] = failures.get(name, 0) + 1
            value = 1.0e30
        objective_cache[key] = float(value)
        return float(value)

    finite_difference_steps = np.asarray(
        [3.0e-5, 2.7e-4, 4.0e-3, 5.0e-7, 2.0e-7],
        dtype=float,
    )
    results: list[Any] = []
    start_time = time.perf_counter()
    for start in starts:
        results.append(
            optimize.minimize(
                objective,
                start,
                method="L-BFGS-B",
                bounds=priors,
                options={
                    "maxiter": 120,
                    "ftol": 2.0e-10,
                    "maxls": 35,
                    "eps": finite_difference_steps,
                },
            )
        )
    finite = [
        result
        for result in results
        if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e29
    ]
    if not finite:
        raise RuntimeError("all calibrated-fit starts failed")
    best = min(finite, key=lambda result: float(result.fun))
    params, zeta = vector_parameters(np.asarray(best.x, dtype=float))
    exact = score_calibrated(
        params,
        zeta,
        data,
        accuracy="exact",
        detail=True,
    )
    names = ["Omega_m", "log10_mu", "H0", "Omega_b_h2", "zeta_c"]
    values = [
        params["Omega_m"],
        params["log10_mu"],
        params["H0"],
        params["Omega_b_h2"],
        zeta,
    ]
    edge_rows: list[dict[str, Any]] = []
    for name, value, bounds in zip(names, values, priors, strict=True):
        fractional_distance = min(
            value - bounds[0],
            bounds[1] - value,
        ) / (bounds[1] - bounds[0])
        edge_rows.append(
            {
                "model": CALIBRATED_MODEL,
                "parameter": name,
                "best_fit": value,
                "lower": bounds[0],
                "upper": bounds[1],
                "fractional_distance_to_edge": fractional_distance,
                "edge_flag": fractional_distance <= 0.01,
                "parameter_type": "optimized",
            }
        )
    for name, value, bounds, edge_flag in (
        (
            "n_s",
            exact["n_s_profiled"],
            checkpoint_5206.checkpoint_5195.NS_BOUNDS,
            exact["n_s_edge_flag"],
        ),
        (
            "sigma8_0",
            exact["sigma8_0_profiled"],
            checkpoint_5206.checkpoint_5195.SIGMA8_BOUNDS,
            exact["sigma8_edge_flag"],
        ),
    ):
        edge_rows.append(
            {
                "model": CALIBRATED_MODEL,
                "parameter": name,
                "best_fit": value,
                "lower": bounds[0],
                "upper": bounds[1],
                "fractional_distance_to_edge": min(
                    value - bounds[0],
                    bounds[1] - value,
                )
                / (bounds[1] - bounds[0]),
                "edge_flag": edge_flag,
                "parameter_type": "analytically_profiled",
            }
        )
    k_count = 8
    fit = {
        "model": CALIBRATED_MODEL,
        "params": params,
        "zeta": zeta,
        **{
            key: value
            for key, value in exact.items()
            if key not in {"solution", "growth_residual_rows"}
        },
        "k": k_count,
        "AIC_cosmology": exact["chi2_cosmology"] + 2.0 * k_count,
        "BIC_cosmology": exact["chi2_cosmology"]
        + k_count * math.log(PRIMARY_N_COSMOLOGY),
        "AIC_joint": exact["chi2_joint"] + 2.0 * k_count,
        "BIC_joint": exact["chi2_joint"]
        + k_count * math.log(PRIMARY_N_WITH_LOCAL),
        "convergence": (
            math.isfinite(exact["chi2_joint"])
            and abs(float(best.fun) - exact["chi2_joint"]) < 0.02
        ),
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "objective_evaluations": evaluations,
        "unique_objective_evaluations": len(objective_cache),
        "successful_start_count": len(finite),
        "multistart_chi2_span": (
            max(float(result.fun) for result in finite)
            - min(float(result.fun) for result in finite)
        ),
        "prior_edge_flag": any(bool(row["edge_flag"]) for row in edge_rows),
        "edge_rows": edge_rows,
        "failure_counts": failures,
        "runtime_seconds": time.perf_counter() - start_time,
        "growth_residual_rows": exact["growth_residual_rows"],
        "solution": exact["solution"],
    }
    print(
        json.dumps(
            {
                "model": CALIBRATED_MODEL,
                "chi2_joint": fit["chi2_joint"],
                "zeta": fit["zeta"],
                "scale_ratio": fit["background_diagnostics"][
                    "scale_ratio_MR2_over_MN2"
                ],
                "params": params,
                "edge": fit["prior_edge_flag"],
                "evaluations": evaluations,
                "runtime_seconds": fit["runtime_seconds"],
            }
        ),
        flush=True,
    )
    return fit


def calibration_rows(
    source_fit: dict[str, Any],
    no_refit_score: dict[str, Any],
    calibrated_fit: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model, score, status in (
        (
            "5206_signed_uncalibrated",
            source_fit,
            "BARE_MR_CONVENTION",
        ),
        (
            "5206_signed_Cavendish_calibrated_without_refit",
            no_refit_score,
            "EXACT_SOURCE_MAP_FIXED_PARAMETERS",
        ),
        (
            CALIBRATED_MODEL,
            calibrated_fit,
            "EXACT_SOURCE_MAP_REFITTED",
        ),
    ):
        diagnostics = score["background_diagnostics"]
        scale_ratio = float(
            diagnostics.get(
                "scale_ratio_MR2_over_MN2",
                diagnostics.get("Gcav_over_Gbare_0", 1.0),
            )
        )
        rows.append(
            {
                "model": model,
                "status": status,
                "zeta_c": score["zeta"],
                "phi0": diagnostics["phi0"],
                "q0": diagnostics["q0"],
                "MR2_over_MN2": scale_ratio,
                "MR_over_MN": math.sqrt(scale_ratio),
                "Gbare_over_GN": 1.0 / scale_ratio,
                "Omega_m_observed": score["params"]["Omega_m"],
                "Omega_m_bare": diagnostics.get(
                    "Omega_m_bare",
                    score["params"]["Omega_m"],
                ),
                "present_Poisson_source_ratio": diagnostics.get(
                    "present_Poisson_source_ratio",
                    diagnostics.get("Gcav_over_Gbare_0", 1.0),
                ),
                "chi2_cosmology": score["chi2_cosmology"],
                "chi2_local": score["chi2_local"],
                "chi2_joint": score["chi2_joint"],
            }
        )
    rows.extend(
        [
            {
                "model": "conditional_exact_local_GR_phi_zero",
                "status": "CONDITIONAL_BRANCH_NOT_DYNAMICAL_TRANSITION",
                "zeta_c": calibrated_fit["zeta"],
                "phi0": 0.0,
                "q0": 0.0,
                "MR2_over_MN2": 1.0,
                "MR_over_MN": 1.0,
                "Gbare_over_GN": 1.0,
                "Omega_m_observed": calibrated_fit["params"]["Omega_m"],
                "Omega_m_bare": calibrated_fit["params"]["Omega_m"],
                "present_Poisson_source_ratio": 1.0,
                "chi2_cosmology": "",
                "chi2_local": "",
                "chi2_joint": "",
            },
            {
                "model": "absolute_Newton_scale",
                "status": "NOT_DERIVED",
                "zeta_c": "",
                "phi0": "",
                "q0": "",
                "MR2_over_MN2": "dimensionless ratio derived",
                "MR_over_MN": "dimensionless ratio derived",
                "Gbare_over_GN": "dimensionless ratio derived",
                "Omega_m_observed": "",
                "Omega_m_bare": "",
                "present_Poisson_source_ratio": "",
                "chi2_cosmology": "",
                "chi2_local": "",
                "chi2_joint": "",
            },
        ]
    )
    return tagged(rows)


def comparison_rows(
    result_5206: dict[str, Any],
    source_fit: dict[str, Any],
    no_refit_score: dict[str, Any],
    calibrated_fit: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    no_refit_k = 8
    no_refit = {
        **no_refit_score,
        "k": no_refit_k,
        "AIC_joint": no_refit_score["chi2_joint"] + 2.0 * no_refit_k,
        "BIC_joint": no_refit_score["chi2_joint"]
        + no_refit_k * math.log(PRIMARY_N_WITH_LOCAL),
    }
    comparators: dict[str, dict[str, Any]] = {
        source_fit["model"]: source_fit,
        "5206_signed_Cavendish_calibrated_without_refit": no_refit,
    }
    for row in result_5206["locked_comparators"]:
        comparators[row["model"]] = row
    for name, comparator in comparators.items():
        rows.append(
            {
                "model": CALIBRATED_MODEL,
                "baseline": name,
                "delta_chi2_joint": calibrated_fit["chi2_joint"]
                - float(comparator["chi2_joint"]),
                "delta_AIC_joint": calibrated_fit["AIC_joint"]
                - float(comparator["AIC_joint"]),
                "delta_BIC_joint": calibrated_fit["BIC_joint"]
                - float(comparator["BIC_joint"]),
                "model_k": calibrated_fit["k"],
                "baseline_k": comparator["k"],
                "model_edge_flag": calibrated_fit["prior_edge_flag"],
                "baseline_edge_flag": comparator.get("prior_edge_flag", False),
            }
        )
    return tagged(rows)


def sensitivity_rows(
    source_fit: dict[str, Any],
    no_refit_score: dict[str, Any],
    calibrated_fit: dict[str, Any],
) -> list[dict[str, Any]]:
    calibrated_solution = calibrated_fit["solution"]
    uncalibrated_at_refit = checkpoint_5206.solve_st_background(
        calibrated_fit["params"],
        calibrated_fit["zeta"],
        accuracy="exact",
    )
    nodes = np.linspace(-12.0, 0.0, 1201)
    calibrated_e = calibrated_solution.background.values_at_n(nodes)[0]
    uncalibrated_e = uncalibrated_at_refit.background.values_at_n(nodes)[0]
    maximum_relative_e = float(
        np.max(np.abs(calibrated_e / uncalibrated_e - 1.0))
    )
    diagnostics = calibrated_fit["background_diagnostics"]
    return tagged(
        [
            {
                "test": "fixed_5206_parameters_source_calibration",
                "value": no_refit_score["chi2_joint"] - source_fit["chi2_joint"],
                "metric": "Delta chi2_joint",
                "status": "CALCULATED",
            },
            {
                "test": "refit_after_source_calibration",
                "value": calibrated_fit["chi2_joint"] - source_fit["chi2_joint"],
                "metric": "Delta chi2_joint versus 5206 signed",
                "status": "CALCULATED",
            },
            {
                "test": "maximum_background_change",
                "value": maximum_relative_e,
                "metric": "max abs(E_cal/E_bare-1), -12<=N<=0",
                "status": "CALCULATED",
            },
            {
                "test": "present_source_normalization",
                "value": diagnostics["present_Poisson_source_ratio"] - 1.0,
                "metric": "Omega_m,bare Geff0/Omega_m,observed - 1",
                "status": "EXACT_NUMERIC_ZERO",
            },
            {
                "test": "parent_scale_shift",
                "value": diagnostics["scale_ratio_MR2_over_MN2"] - 1.0,
                "metric": "M_R^2/M_N^2 - 1",
                "status": "DERIVED_DIMENSIONLESS_SHIFT",
            },
            {
                "test": "absolute_GN",
                "value": "",
                "metric": "dimensionful magnitude",
                "status": "NOT_DERIVED_REQUIRES_PARENT_SCALE_SELECTION",
            },
        ]
    )


def parameter_rows(fit: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics = fit["background_diagnostics"]
    rows: list[dict[str, Any]] = []
    for name, value, status in (
        ("Omega_m_observed", fit["params"]["Omega_m"], "OPTIMIZED"),
        ("Omega_m_bare", diagnostics["Omega_m_bare"], "DERIVED"),
        ("log10_mu", fit["params"]["log10_mu"], "OPTIMIZED"),
        ("mu_mgap_over_H0", 10.0 ** fit["params"]["log10_mu"], "DERIVED"),
        ("H0", fit["params"]["H0"], "OPTIMIZED"),
        ("Omega_b_h2", fit["params"]["Omega_b_h2"], "OPTIMIZED"),
        ("zeta_c", fit["zeta"], "OPTIMIZED"),
        ("n_s", fit["n_s_profiled"], "PROFILED"),
        ("sigma8_0", fit["sigma8_0_profiled"], "PROFILED"),
        ("phi0", diagnostics["phi0"], "DERIVED"),
        ("q0", diagnostics["q0"], "DERIVED"),
        (
            "scale_ratio_MR2_over_MN2",
            diagnostics["scale_ratio_MR2_over_MN2"],
            "DERIVED_BY_CAVENDISH_CALIBRATION",
        ),
        ("MR_over_MN", diagnostics["MR_over_MN"], "DERIVED"),
        ("Gbare_over_GN", diagnostics["Gbare_over_GN"], "DERIVED"),
    ):
        rows.append(
            {
                "model": fit["model"],
                "parameter": name,
                "value": value,
                "status": status,
            }
        )
    rows.extend(fit["edge_rows"])
    return tagged(rows)


def background_rows(fit: dict[str, Any]) -> list[dict[str, Any]]:
    solution = fit["solution"]
    scale_ratio = fit["background_diagnostics"]["scale_ratio_MR2_over_MN2"]
    rows: list[dict[str, Any]] = []
    for redshift in (0.0, 0.5, 1.0, 2.0, 10.0, 1100.0):
        n_value = -math.log1p(redshift)
        e_value, h_value, w_value, omega_dark = (
            solution.background.values_at_n(n_value)
        )
        phi_value = float(
            np.interp(n_value, solution.background.n_grid, solution.phi_grid)
        )
        q_value = float(
            np.interp(n_value, solution.background.n_grid, solution.q_grid)
        )
        geff_bare = float(
            np.interp(n_value, solution.background.n_grid, solution.geff_grid)
        )
        rows.append(
            {
                "model": fit["model"],
                "z": redshift,
                "N_ln_a": n_value,
                "E": float(e_value),
                "h_dlnH_dN": float(h_value),
                "phi": phi_value,
                "q_dphi_dN": q_value,
                "Omega_dark_effective": float(omega_dark),
                "w_dark_effective": float(w_value),
                "Geff_over_Gbare": geff_bare,
                "Geff_over_GN": geff_bare / scale_ratio,
            }
        )
    return tagged(rows)


def regular_rows(
    calibrated_fit: dict[str, Any],
) -> list[dict[str, Any]]:
    diagnostics = calibrated_fit["background_diagnostics"]
    short = solve_calibrated_background(
        calibrated_fit["params"],
        calibrated_fit["zeta"],
        accuracy="exact",
        n_initial=-16.0,
    )
    nodes = np.linspace(-12.0, 0.0, 1201)
    long_e = calibrated_fit["solution"].background.values_at_n(nodes)[0]
    short_e = short.solution.background.values_at_n(nodes)[0]
    start_sensitivity = float(np.max(np.abs(short_e / long_e - 1.0)))
    tests = (
        (
            "coupled_root",
            diagnostics["coupled_root_max_residual"],
            1.0e-9,
            diagnostics["coupled_root_max_residual"] < 1.0e-9,
        ),
        (
            "Hamiltonian_constraint",
            diagnostics["maximum_constraint_residual"],
            1.0e-9,
            diagnostics["maximum_constraint_residual"] < 1.0e-9,
        ),
        (
            "h_derivative_identity",
            diagnostics["maximum_h_derivative_residual"],
            2.0e-4,
            diagnostics["maximum_h_derivative_residual"] < 2.0e-4,
        ),
        (
            "positive_F",
            diagnostics["minimum_f"],
            0.0,
            diagnostics["minimum_f"] > 0.0,
        ),
        (
            "positive_Einstein_kinetic",
            diagnostics["minimum_Einstein_kinetic"],
            0.0,
            diagnostics["minimum_Einstein_kinetic"] > 0.0,
        ),
        (
            "present_source_normalization",
            abs(diagnostics["present_Poisson_source_ratio"] - 1.0),
            1.0e-10,
            abs(diagnostics["present_Poisson_source_ratio"] - 1.0) < 1.0e-10,
        ),
        (
            "initial_surface_sensitivity",
            start_sensitivity,
            2.0e-6,
            start_sensitivity < 2.0e-6,
        ),
        (
            "regular_series_remainder",
            diagnostics["regular_series_remainder_bound"],
            1.0e-8,
            diagnostics["regular_series_remainder_bound"] < 1.0e-8,
        ),
    )
    return tagged(
        [
            {
                "model": calibrated_fit["model"],
                "test": name,
                "value": value,
                "tolerance": tolerance,
                "pass": passed,
            }
            for name, value, tolerance, passed in tests
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source": str(path),
            "sha256": expected,
            "role": "locked checkpoint-5206 parent equations, fit and validation",
            "exists": path.exists(),
        }
        for path, expected in SOURCE_LOCKS
    ]
    rows.extend(
        [
            {
                "source": "checkpoint-5204 Cassini and LLR anchors",
                "sha256": "transitively locked by checkpoint 5206",
                "role": "local gamma and Gdot likelihood",
                "exists": True,
            },
            {
                "source": "measured G_N",
                "sha256": "dimensionful calibration symbol only",
                "role": "defines M_N^2=1/(8 pi G_N); no numerical value required",
                "exists": True,
            },
        ]
    )
    return tagged(rows)


def clean_fit(fit: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in fit.items()
        if key not in {"solution", "growth_residual_rows", "edge_rows"}
    }


def build_document(
    symbolic: dict[str, str],
    source_fit: dict[str, Any],
    no_refit_score: dict[str, Any],
    calibrated_fit: dict[str, Any],
    comparisons: list[dict[str, Any]],
    regular: list[dict[str, Any]],
) -> str:
    comparison_lookup = {row["baseline"]: row for row in comparisons}
    vs_source = comparison_lookup[SIGNED_MODEL]
    vs_minimal = comparison_lookup[
        "ParentScalar_Lambda_zero_minimal_locked"
    ]
    vs_lcdm = comparison_lookup["LCDM"]
    diagnostics = calibrated_fit["background_diagnostics"]
    local_pass = (
        abs(diagnostics["gamma_minus_one_0"])
        <= checkpoint_5206.LOCAL_GAMMA_TWO_SIGMA_ENVELOPE
        and abs(diagnostics["Gdot_over_G_yr_inv"])
        <= checkpoint_5206.LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV
    )
    selected_route = (
        "DERIVE_COMMON_F_R_V_Z_X2_RUNNING_AND_ABSOLUTE_PARENT_SCALE_SELECTION"
    )
    return f"""# 5207 - Cavendish-Normalized Parent Scale, Observed-Density Map and Self-Consistent Source-Calibrated Refit

Private derivation and empirical robustness checkpoint. No GitHub action and
no public cosmology or full-MTS claim.

Checkpoint marker: `{MARKER}`.

## Executive result

Checkpoint 5206 solved the finite-`zeta_c` Jordan background but deliberately
retained the action-scale density convention. Checkpoint 5207 removes that
last source-normalization convention.

Define the measured reduced Newton scale by

```text
M_N^2=1/(8 pi G_N).
```

The same parent action predicts

```text
G_cav,0
 =1/(8 pi M_R^2)
   [(2f0+4f_phi0^2)/(2f0+3f_phi0^2)]/f0
 =g0/(8 pi M_R^2).
```

Requiring `G_cav,0=G_N` gives the exact relation

```text
s=M_R^2/M_N^2=g0.
```

This derives the ratio of the parent and measured gravitational scales. It
does not derive the absolute dimensionful magnitude of `G_N`.

## 1. Coupled boundary-value problem

Observed density parameters and action-scale density parameters obey

```text
Omega_i,bare=Omega_i,observed/s.
```

At every likelihood evaluation the runner simultaneously solves

```text
ln E(0)^2=0,
ln[s/g(phi0)]=0,
```

for the regular-mode amplitude and `s`. The field phase remains derived from
the `N=-18` regular Frobenius boundary condition. No source coefficient,
scalar fraction or phase is fitted.

The symbolic calibration residual is

```text
{symbolic['calibration_residual']},
```

and the present Poisson-source residual is

```text
{symbolic['present_source_residual']}.
```

Numerically,

```text
Omega_m,bare (G_eff,0/G_bare)/Omega_m,observed
 ={diagnostics['present_Poisson_source_ratio']:.16g}.
```

Thus the Newtonian source coefficient at the present epoch is normalized to
measured `G_N` by the parent relation itself.

## 2. Fixed-parameter calibration test

Applying the exact map to the checkpoint-5206 signed optimum without
refitting gives

```text
Delta chi2_joint
 ={no_refit_score['chi2_joint'] - source_fit['chi2_joint']:.12g}.
```

This is the direct size of the convention correction before the likelihood
is allowed to readjust.

## 3. Calibrated refit

The source-calibrated optimum is

```text
zeta_c                    ={calibrated_fit['zeta']:.12g};
Omega_m,observed           ={calibrated_fit['params']['Omega_m']:.12g};
Omega_m,bare               ={diagnostics['Omega_m_bare']:.12g};
mu=m_gap/H0                ={10.0 ** calibrated_fit['params']['log10_mu']:.12g};
H0                         ={calibrated_fit['params']['H0']:.12g} km/s/Mpc;
phi0                       ={diagnostics['phi0']:.12g};
q0                         ={diagnostics['q0']:.12g};
M_R^2/M_N^2                ={diagnostics['scale_ratio_MR2_over_MN2']:.12g};
M_R/M_N                    ={diagnostics['MR_over_MN']:.12g};
G_bare/G_N                 ={diagnostics['Gbare_over_GN']:.12g};
gamma-1                    ={diagnostics['gamma_minus_one_0']:.12g};
Gdot/G                     ={diagnostics['Gdot_over_G_yr_inv']:.12g} yr^-1;
chi2_cosmology             ={calibrated_fit['chi2_cosmology']:.12g};
chi2_local                 ={calibrated_fit['chi2_local']:.12g};
chi2_joint                 ={calibrated_fit['chi2_joint']:.12g}.
```

Relative to the uncalibrated checkpoint-5206 signed fit:

```text
Delta chi2_joint={float(vs_source['delta_chi2_joint']):.12g};
Delta AIC_joint ={float(vs_source['delta_AIC_joint']):.12g};
Delta BIC_joint ={float(vs_source['delta_BIC_joint']):.12g}.
```

Both models have the same parameter count, so this is a pure calibration
sensitivity comparison.

Relative to the locked minimal zero-Lambda parent:

```text
Delta AIC_joint={float(vs_minimal['delta_AIC_joint']):.12g};
Delta BIC_joint={float(vs_minimal['delta_BIC_joint']):.12g}.
```

Relative to fitted LCDM:

```text
Delta AIC_joint={float(vs_lcdm['delta_AIC_joint']):.12g};
Delta BIC_joint={float(vs_lcdm['delta_BIC_joint']):.12g}.
```

The finite signed coupling remains an allowed near-GR coordinate only if it
is interior and locally bounded. It is not promoted merely because the
source calibration is numerically small.

## 4. Local-GR branch distinction

The calculation above is the unscreened long-range branch used by checkpoint
5204: the local field inherits the cosmological `phi0`. On a separate exact
local branch with

```text
phi_local=0,
q_local=0,
```

one instead has `g_local=1` and `M_R=M_N`. No local transition or screening
mechanism between the cosmological state and that exact local branch has
been derived, so the two calibrations are recorded separately rather than
blended.

## 5. Decision

```text
Cavendish parent-scale ratio derived              = yes;
observed-to-bare density map derived              = yes;
flatness and source calibration solved together  = yes;
present Newtonian source residual                 ={diagnostics['present_Poisson_source_ratio'] - 1.0:.3e};
regular/numerical gates                            ={str(all(bool(row['pass']) for row in regular)).lower()};
signed local two-sigma envelopes                   ={str(local_pass).lower()};
absolute numerical G_N derived                    = no;
local transition phi_cosmology -> 0 derived       = no;
common F_R,V,Z,X2 trajectory selected             = no;
official CMB likelihood                           = no;
cosmology-support claim                           = false;
full MTS claim                                    = false.
```

Selected next route:

```text
{selected_route}.
```

The source-coupling normalization is no longer a free gap. What remains is
genuinely upstream: select the running coefficients and the absolute parent
scale from the parent theory, or show that they must remain measured inputs.

## 6. Evidence products

- `source-intake/functional_rg/5207/Cavendish_source_map.csv`
- `source-intake/functional_rg/5207/calibrated_fit_summary.csv`
- `source-intake/functional_rg/5207/calibrated_fit_parameters.csv`
- `source-intake/functional_rg/5207/calibration_branch_comparison.csv`
- `source-intake/functional_rg/5207/calibration_sensitivity.csv`
- `source-intake/functional_rg/5207/model_comparisons.csv`
- `source-intake/functional_rg/5207/regular_and_source_validation.csv`
- `source-intake/functional_rg/5207/calibrated_background_samples.csv`
- `source-intake/functional_rg/5207/source_provenance.csv`
- `source-intake/functional_rg/5207/Cavendish_source_calibrated_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5207_VALIDATION.csv`
"""


def validation_rows(
    payload: dict[str, Any],
    output_names: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check: str, passed: bool, detail: Any) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "checked_date": CHECKED_DATE,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    add(
        "script_compiles",
        bool(compile(Path(__file__).read_text(encoding="utf-8"), str(__file__), "exec")),
        str(Path(__file__)),
    )
    add("document_exists", DOCUMENT.exists(), str(DOCUMENT))
    for path, expected in SOURCE_LOCKS:
        add(f"source_exists::{path.name}", path.exists(), str(path))
        add(
            f"source_hash::{path.name}",
            path.exists() and file_digest(path) == expected,
            file_digest(path) if path.exists() else "MISSING",
        )
    formal_hash = tree_digest(FORMAL)
    add("formal_tree_locked", formal_hash == FORMAL_LOCK, formal_hash)
    add(
        "symbolic_calibration_residual_zero",
        payload["symbolic"]["calibration_residual"] == "0",
        payload["symbolic"]["calibration_residual"],
    )
    add(
        "symbolic_present_source_residual_zero",
        payload["symbolic"]["present_source_residual"] == "0",
        payload["symbolic"]["present_source_residual"],
    )
    fit = payload["fit"]
    diagnostics = fit["background_diagnostics"]
    add("calibrated_fit_converged", bool(fit["convergence"]), fit["optimizer_message"])
    add(
        "calibrated_fit_interior",
        not bool(fit["prior_edge_flag"]),
        fit["prior_edge_flag"],
    )
    add(
        "coupled_root_closed",
        float(diagnostics["coupled_root_max_residual"]) < 1.0e-9,
        diagnostics["coupled_root_max_residual"],
    )
    add(
        "present_source_normalized",
        abs(float(diagnostics["present_Poisson_source_ratio"]) - 1.0) < 1.0e-10,
        diagnostics["present_Poisson_source_ratio"],
    )
    add(
        "scale_ratio_matches_Gcav",
        abs(
            float(diagnostics["scale_ratio_MR2_over_MN2"])
            - float(diagnostics["Gcav_over_Gbare_0"])
        )
        < 1.0e-10,
        (
            diagnostics["scale_ratio_MR2_over_MN2"],
            diagnostics["Gcav_over_Gbare_0"],
        ),
    )
    add(
        "positive_F",
        float(diagnostics["minimum_f"]) > 0.0,
        diagnostics["minimum_f"],
    )
    add(
        "positive_Einstein_kinetic",
        float(diagnostics["minimum_Einstein_kinetic"]) > 0.0,
        diagnostics["minimum_Einstein_kinetic"],
    )
    add(
        "Hamiltonian_constraint",
        float(diagnostics["maximum_constraint_residual"]) < 1.0e-9,
        diagnostics["maximum_constraint_residual"],
    )
    add(
        "local_Cassini_envelope",
        abs(float(diagnostics["gamma_minus_one_0"]))
        <= checkpoint_5206.LOCAL_GAMMA_TWO_SIGMA_ENVELOPE,
        diagnostics["gamma_minus_one_0"],
    )
    add(
        "local_Gdot_envelope",
        abs(float(diagnostics["Gdot_over_G_yr_inv"]))
        <= checkpoint_5206.LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV,
        diagnostics["Gdot_over_G_yr_inv"],
    )
    add(
        "regular_validation_all_pass",
        all(bool(row["pass"]) for row in payload["regular_validation"]),
        len(payload["regular_validation"]),
    )
    add(
        "parameter_count",
        int(fit["k"]) == 8,
        f"k={fit['k']}=5 optimized+3 profiled",
    )
    add(
        "model_comparisons_complete",
        len(payload["model_comparisons"]) == 6,
        len(payload["model_comparisons"]),
    )
    add(
        "absolute_GN_not_overclaimed",
        not payload["claim_status"]["absolute_GN_derived"],
        payload["claim_status"],
    )
    add(
        "local_transition_not_overclaimed",
        not payload["claim_status"]["local_transition_derived"],
        payload["claim_status"],
    )
    add(
        "claim_status_false",
        not payload["claim_status"]["cosmology_support"]
        and not payload["claim_status"]["full_MTS"],
        payload["claim_status"],
    )
    add(
        "GitHub_action_false",
        not payload["claim_status"]["GitHub_action"],
        payload["claim_status"],
    )
    for name in output_names:
        path = OUT / name
        add(f"output_exists::{name}", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            add(
                f"output_nonempty::{name}",
                len(read_csv(path)) > 0,
                len(read_csv(path)),
            )
    pycache = list((POST / "scripts").rglob("__pycache__"))
    add("no_script_pycache", len(pycache) == 0, len(pycache))
    public_head, public_status = git_state(PUBLIC_WORKTREE)
    add("public_head_locked", public_head == PUBLIC_HEAD_LOCK, public_head)
    add("public_worktree_clean", public_status == "", public_status)
    galaxy_head, galaxy_status = git_state(GALAXY_REPOSITORY)
    add("galaxy_head_locked", galaxy_head == GALAXY_HEAD_LOCK, galaxy_head)
    add(
        "galaxy_status_unchanged",
        text_digest(galaxy_status) == GALAXY_STATUS_LOCK,
        text_digest(galaxy_status),
    )
    return rows


def run_dry() -> None:
    assert_source_locks()
    _, symbolic = symbolic_source_map()
    if symbolic["calibration_residual"] != "0":
        raise RuntimeError("symbolic Cavendish residual is nonzero")
    if symbolic["present_source_residual"] != "0":
        raise RuntimeError("symbolic source residual is nonzero")
    result_5206 = load_5206()
    source_fit = next(
        fit for fit in result_5206["fits"] if fit["model"] == SIGNED_MODEL
    )
    params = {key: float(value) for key, value in source_fit["params"].items()}
    calibrated = solve_calibrated_background(
        params,
        float(source_fit["zeta"]),
        accuracy="exact",
    )
    diagnostics = calibrated.solution.diagnostics
    if abs(diagnostics["present_Poisson_source_ratio"] - 1.0) >= 1.0e-10:
        raise RuntimeError("present source normalization failed")
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "scale_ratio_MR2_over_MN2": diagnostics[
                    "scale_ratio_MR2_over_MN2"
                ],
                "present_source_ratio": diagnostics[
                    "present_Poisson_source_ratio"
                ],
                "coupled_root_residual": diagnostics[
                    "coupled_root_max_residual"
                ],
                "formal_tree": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def run_checkpoint() -> None:
    assert_source_locks()
    if tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed before checkpoint 5207")
    source_rows, symbolic = symbolic_source_map()
    result_5206 = load_5206()
    source_fit = next(
        fit for fit in result_5206["fits"] if fit["model"] == SIGNED_MODEL
    )
    source_params = {
        key: float(value) for key, value in source_fit["params"].items()
    }
    data = checkpoint_5206.checkpoint_5195.load_joint_data()
    no_refit_score = score_calibrated(
        source_params,
        float(source_fit["zeta"]),
        data,
        accuracy="exact",
        detail=True,
    )
    calibrated_fit = fit_calibrated(data, source_fit)
    calibration_branch = calibration_rows(
        source_fit,
        no_refit_score,
        calibrated_fit,
    )
    comparisons = comparison_rows(
        result_5206,
        source_fit,
        no_refit_score,
        calibrated_fit,
    )
    sensitivity = sensitivity_rows(
        source_fit,
        no_refit_score,
        calibrated_fit,
    )
    parameters = parameter_rows(calibrated_fit)
    regular = regular_rows(calibrated_fit)
    background = background_rows(calibrated_fit)
    provenance = provenance_rows()
    fit_summary = tagged(
        [
            {
                "model": calibrated_fit["model"],
                "chi2_SN": calibrated_fit["chi2_SN"],
                "chi2_DESI": calibrated_fit["chi2_DESI"],
                "chi2_growth": calibrated_fit["chi2_growth"],
                "chi2_CMB": calibrated_fit["chi2_CMB"],
                "chi2_cosmology": calibrated_fit["chi2_cosmology"],
                "chi2_Cassini": calibrated_fit["chi2_Cassini"],
                "chi2_LLR_Gdot": calibrated_fit["chi2_LLR_Gdot"],
                "chi2_local": calibrated_fit["chi2_local"],
                "chi2_joint": calibrated_fit["chi2_joint"],
                "k": calibrated_fit["k"],
                "AIC_joint": calibrated_fit["AIC_joint"],
                "BIC_joint": calibrated_fit["BIC_joint"],
                "convergence": calibrated_fit["convergence"],
                "prior_edge_flag": calibrated_fit["prior_edge_flag"],
                "runtime_seconds": calibrated_fit["runtime_seconds"],
            }
        ]
    )
    output_payloads: dict[str, list[dict[str, Any]]] = {
        "Cavendish_source_map.csv": source_rows,
        "calibrated_fit_summary.csv": fit_summary,
        "calibrated_fit_parameters.csv": parameters,
        "calibration_branch_comparison.csv": calibration_branch,
        "calibration_sensitivity.csv": sensitivity,
        "model_comparisons.csv": comparisons,
        "regular_and_source_validation.csv": regular,
        "calibrated_background_samples.csv": background,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in output_payloads.items():
        write_csv(OUT / name, rows)
    DOCUMENT.write_text(
        build_document(
            symbolic,
            source_fit,
            no_refit_score,
            calibrated_fit,
            comparisons,
            regular,
        ),
        encoding="utf-8",
    )
    clean_comparisons = [
        {
            key: value
            for key, value in row.items()
            if key
            not in {
                "checkpoint",
                "marker",
                "checked_date",
                "valid_for_cosmology_support_claim",
                "valid_for_full_MTS_claim",
            }
        }
        for row in comparisons
    ]
    clean_regular = [
        {
            key: value
            for key, value in row.items()
            if key
            not in {
                "checkpoint",
                "marker",
                "checked_date",
                "valid_for_cosmology_support_claim",
                "valid_for_full_MTS_claim",
            }
        }
        for row in regular
    ]
    result_payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "symbolic": symbolic,
        "source_fit_5206": source_fit,
        "fixed_parameter_calibrated_score": {
            key: value
            for key, value in no_refit_score.items()
            if key not in {"solution", "growth_residual_rows"}
        },
        "fit": clean_fit(calibrated_fit),
        "model_comparisons": clean_comparisons,
        "regular_validation": clean_regular,
        "claim_status": {
            "Cavendish_parent_scale_ratio_derived": True,
            "observed_to_bare_density_map_derived": True,
            "flatness_and_source_calibration_solved_together": True,
            "present_Newtonian_source_normalized": True,
            "absolute_GN_derived": False,
            "local_transition_derived": False,
            "common_F_R_V_Z_X2_trajectory_selected": False,
            "official_CMB_likelihood": False,
            "cosmology_support": False,
            "full_MTS": False,
            "GitHub_action": False,
        },
        "selected_next_route": (
            "DERIVE_COMMON_F_R_V_Z_X2_RUNNING_AND_ABSOLUTE_PARENT_SCALE_SELECTION"
        ),
    }
    result_name = "Cavendish_source_calibrated_results.json"
    write_json(OUT / result_name, result_payload)
    output_names = [*output_payloads, result_name]
    validation = validation_rows(result_payload, output_names)
    write_csv(VALIDATION, validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(json.dumps(failed, indent=2, allow_nan=False))
    result_payload["validation"] = {
        "passed": len(validation),
        "failed": 0,
        "validation_path": str(VALIDATION),
        "formal_tree_sha256": tree_digest(FORMAL),
        "output_tree_sha256": tree_digest(OUT),
    }
    write_json(OUT / result_name, result_payload)
    validation = validation_rows(result_payload, output_names)
    write_csv(VALIDATION, validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(json.dumps(failed, indent=2, allow_nan=False))
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "zeta": calibrated_fit["zeta"],
                "scale_ratio_MR2_over_MN2": calibrated_fit[
                    "background_diagnostics"
                ]["scale_ratio_MR2_over_MN2"],
                "present_source_ratio": calibrated_fit[
                    "background_diagnostics"
                ]["present_Poisson_source_ratio"],
                "chi2_joint": calibrated_fit["chi2_joint"],
                "delta_chi2_vs_5206": calibrated_fit["chi2_joint"]
                - source_fit["chi2_joint"],
                "selected_next_route": result_payload["selected_next_route"],
                "output_tree_sha256": tree_digest(OUT),
                "formal_tree_sha256": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    result_path = OUT / "Cavendish_source_calibrated_results.json"
    if not result_path.exists():
        raise FileNotFoundError(result_path)
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    output_names = [
        "Cavendish_source_map.csv",
        "calibrated_fit_summary.csv",
        "calibrated_fit_parameters.csv",
        "calibration_branch_comparison.csv",
        "calibration_sensitivity.csv",
        "model_comparisons.csv",
        "regular_and_source_validation.csv",
        "calibrated_background_samples.csv",
        "source_provenance.csv",
        "Cavendish_source_calibrated_results.json",
    ]
    rows = validation_rows(payload, output_names)
    failed = [row for row in rows if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(json.dumps(failed, indent=2))
    print(
        json.dumps(
            {
                "saved_validation": f"{len(rows)}/{len(rows)} PASS",
                "output_tree_sha256": tree_digest(OUT),
                "formal_tree_sha256": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        run_dry()
    elif args.validate_saved:
        validate_saved()
    else:
        run_checkpoint()


if __name__ == "__main__":
    main()
