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
OUT = POST / "source-intake" / "functional_rg" / "5206"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5206_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5206-Y5-R2FR-constraint-reduced-zero-Lambda-Jordan-scalar-tensor-"
    "refit-local-Gdot-and-competitive-model-gate.md"
)
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPOSITORY = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

CHECKPOINT = 5206
CHECKED_DATE = "2026-07-24"
MARKER = "MTS_5206_CONSTRAINT_REDUCED_SCALAR_TENSOR_REFIT"
FORMAL_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"
GALAXY_STATUS_LOCK = "21838b41dd2617e2de312ea2620c225022cc2f70d85b4a78d75dcb1cc727ff39"

SOURCE_LOCKS = (
    (
        POST
        / "5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-"
        "physical-sound-horizon-gate.md",
        "217fdc07f94e18a21fe996f7592930f69c21ba16b3fe44b1fd1a2518d9d54737",
    ),
    (
        POST / "scripts" / "Y5_R2FR_5195_joint_CMB_informed_parent_refit.py",
        "c379ecbc04bd94fc469281ab3a3a99f103c304a209bd8ea33db4a10785129cb8",
    ),
    (
        POST
        / "source-intake"
        / "functional_rg"
        / "5195"
        / "joint_CMB_informed_refit_results.json",
        "538078e466c2ee9f02e5204090b9e1c87c8c56b5680c366289336dda4abdf3ad",
    ),
    (
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_BRR545_5195_VALIDATION.csv",
        "9bd11c9d45a76ae25999c155c5f77949221c53421fe80dc466c98416554481c5",
    ),
    (
        POST
        / "5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-"
        "cross-coupling-and-branch-reduction-theorem.md",
        "0c456634e22a3f6e03ce648fe34c28e5557d562a47249b04201a2602b67c8a6b",
    ),
    (
        POST
        / "source-intake"
        / "functional_rg"
        / "5203"
        / "canonical_translation_parent_action_results.json",
        "4199e389c41acf8b7c4414912afd88b616429440e90952e80553a235f528b2fe",
    ),
    (
        POST
        / "5204-Y5-R2FR-curvature-triggered-homogeneous-motion-state-"
        "local-PPN-Gdot-and-preparation-no-overlap-theorem.md",
        "8923d9fac23289f1923659ac3352aa216ad89c1985140c01e1d9ed1907d7c535",
    ),
    (
        POST / "scripts" / "Y5_R2FR_5204_curvature_triggered_motion_state_gate.py",
        "86b2d1161ff907e19aead1b44587342a79c4a6d88e11584c282e2521a394d765",
    ),
    (
        POST
        / "source-intake"
        / "functional_rg"
        / "5204"
        / "curvature_triggered_motion_state_results.json",
        "341abeb003983ab9593137983e792e4007742d1f46c17e95b194a5fb827c382a",
    ),
    (
        POST
        / "5205-Y5-R2FR-normalized-CTP-regular-mode-ensemble-Hamiltonian-"
        "constraint-and-zero-Lambda-second-moment-selection-theorem.md",
        "2563092d1eb5ede72275042bec70d70f79f7f98db371d5a710f681d59a38af50",
    ),
    (
        POST / "scripts" / "Y5_R2FR_5205_normalized_CTP_regular_mode_state_gate.py",
        "819a01a287e2a89b0582789927dd8da28178b97a7650245416025f36f20a2c55",
    ),
    (
        POST
        / "source-intake"
        / "functional_rg"
        / "5205"
        / "normalized_CTP_regular_mode_state_results.json",
        "08bc87ff2feefdf05d35a4df4836e55c9a4dd9eeeb3b7eff72c0960112400537",
    ),
    (
        POST
        / "source-intake"
        / "mts_residuals"
        / "P8_Y5_BRR545_5205_VALIDATION.csv",
        "3926facbb335ef797092895323a70e914832a708bf92564f02e76fbb59c24b42",
    ),
)

sys.path.insert(0, str(POST / "scripts"))
import Y5_R2FR_5195_joint_CMB_informed_parent_refit as checkpoint_5195
import Y5_R2FR_5204_curvature_triggered_motion_state_gate as checkpoint_5204


OMEGA_R = checkpoint_5195.checkpoint_5194.OMEGA_R
C_KM_S = checkpoint_5195.C_KM_S
MPC_METRES = checkpoint_5195.MPC_METRES
SECONDS_PER_JULIAN_YEAR = 365.25 * 86400.0
H0_TO_YEAR_INV = 1000.0 / MPC_METRES * SECONDS_PER_JULIAN_YEAR
N_INITIAL = -18.0
N_OUTPUT = np.linspace(N_INITIAL, 0.0, 3601)
OMEGA_GAMMA_H2 = 2.469e-5
LOCAL_GAMMA_MEAN = 2.1e-5
LOCAL_GAMMA_SIGMA = 2.3e-5
LOCAL_GDOT_MEAN_YR_INV = -5.0e-15
LOCAL_GDOT_SIGMA_YR_INV = 9.6e-15
LOCAL_GAMMA_TWO_SIGMA_ENVELOPE = 6.7e-5
LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV = 2.42e-14
K_MIN_H_MPC = 0.01
PRIMARY_N_COSMOLOGY = 1646
PRIMARY_N_WITH_LOCAL = PRIMARY_N_COSMOLOGY + 2

LOCKED_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5195"
    / "joint_CMB_informed_refit_results.json"
)


@dataclass(frozen=True)
class FitSpec:
    name: str
    zeta_bounds: tuple[float, float]
    starts: tuple[float, ...]


@dataclass
class STSolution:
    background: checkpoint_5195.checkpoint_5194.Background
    phi_grid: np.ndarray
    q_grid: np.ndarray
    geff_grid: np.ndarray
    diagnostics: dict[str, Any]


SIGNED_SPEC = FitSpec(
    name="ParentST_Lambda_zero_signed_zeta",
    zeta_bounds=(-0.002, 0.002),
    starts=(0.0, -5.0e-5, 5.0e-5),
)
POSITIVE_SPEC = FitSpec(
    name="ParentST_Lambda_zero_positive_zeta",
    zeta_bounds=(0.0, 0.002),
    starts=(0.0, 5.0e-5, 1.5e-4),
)

BACKGROUND_CACHE: dict[tuple[Any, ...], STSolution] = {}
EARLY_CALIBRATION_CACHE: dict[tuple[Any, ...], dict[str, Any]] = {}
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
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
    status_lines = subprocess.run(
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
    return head, status_lines


def assert_source_locks() -> None:
    for path, expected in SOURCE_LOCKS:
        if not path.exists():
            raise FileNotFoundError(path)
        actual = file_digest(path)
        if actual != expected:
            raise RuntimeError(
                f"source lock failed for {path}: expected {expected}, got {actual}"
            )


def locked_primary_fits() -> dict[str, dict[str, Any]]:
    payload = json.loads(LOCKED_RESULT.read_text(encoding="utf-8"))
    return {
        row["model"]: row
        for row in payload["fits"]
        if row["config"] == checkpoint_5195.PRIMARY_CONFIG.name
    }


def symbolic_equation_rows() -> tuple[list[dict[str, Any]], dict[str, str]]:
    f, f_phi, f_phiphi = sp.symbols("f f_phi f_phiphi", positive=True)
    h, q, q_n, phi, mu, e2, omega_m_n, omega_r_n = sp.symbols(
        "h q q_N phi mu E2 Omega_m_N Omega_r_N", real=True
    )
    zeta = sp.symbols("zeta", real=True)
    f_value = 1 + zeta * phi**2
    f_phi_value = 2 * zeta * phi
    scalar_qn = (
        -(3 + h) * q
        - mu**2 * phi / e2
        + 6 * zeta * phi * (2 + h)
    )
    f_n = f_phi_value * q
    f_nn = 2 * zeta * q**2 + f_phi_value * scalar_qn
    h_closed = -(
        3 * omega_m_n
        + 4 * omega_r_n
        + (1 + 2 * zeta) * q**2
        - 8 * zeta * phi * q
        - 2 * zeta * mu**2 * phi**2 / e2
        + 24 * zeta**2 * phi**2
    ) / (2 * f_value + 12 * zeta**2 * phi**2)
    raychaudhuri_residual = sp.simplify(
        (
            -2 * f_value * h
            - (
                3 * omega_m_n
                + 4 * omega_r_n
                + q**2
                + f_nn
                + (h - 1) * f_n
            )
        ).subs(h, h_closed)
    )
    scalar_residual = sp.simplify(
        (
            q_n
            + (3 + h) * q
            + mu**2 * phi / e2
            - 6 * zeta * phi * (2 + h)
        ).subs(q_n, scalar_qn)
    )
    rows = tagged(
        [
            {
                "equation": "parent_action",
                "formula": (
                    "S=integral sqrt(-g)[F(phi)R/2-M_R^2(partial phi)^2/2"
                    "-M_R^2 m^2 phi^2/2]+S_m[g,Psi]"
                ),
                "derivation": "checkpoint-5203 Jordan-frame branch with Z=1 and Lambda_cal=0",
                "status": "LOCKED_TRUNCATION",
            },
            {
                "equation": "nonminimal_function",
                "formula": "F/M_R^2=f(phi)=1+zeta_c phi^2",
                "derivation": "checkpoint-5204 canonical convention",
                "status": "DERIVED_COORDINATE",
            },
            {
                "equation": "Hamiltonian_constraint",
                "formula": (
                    "E^2[f+f_N-q^2/6]=Omega_m exp(-3N)+Omega_r exp(-4N)"
                    "+mu^2 phi^2/6"
                ),
                "derivation": "00 Jordan metric equation divided by 3 M_R^2 H0^2",
                "status": "EXACT_AT_TESTED_TRUNCATION",
            },
            {
                "equation": "scalar_equation",
                "formula": (
                    "q_N=-(3+h)q-mu^2 phi/E^2+6 zeta_c phi(2+h)"
                ),
                "derivation": "Box chi+m^2 chi-zeta_c R chi=0 with R/H^2=6(2+h)",
                "status": "EXACT_AT_TESTED_TRUNCATION",
            },
            {
                "equation": "Raychaudhuri_solution",
                "formula": str(h_closed),
                "derivation": (
                    "-2F Hdot=rho_m+4rho_r/3+chidot^2+Fddot-H Fdot "
                    "with the scalar equation substituted"
                ),
                "status": "EXACT_ALGEBRAIC_SOLUTION",
            },
            {
                "equation": "Raychaudhuri_substitution_residual",
                "formula": str(raychaudhuri_residual),
                "derivation": "SymPy substitution into the independent ij equation",
                "status": "EXACT_ZERO",
            },
            {
                "equation": "scalar_substitution_residual",
                "formula": str(scalar_residual),
                "derivation": "SymPy substitution into the scalar equation",
                "status": "EXACT_ZERO",
            },
            {
                "equation": "regular_radiation_mode",
                "formula": (
                    "q_i/phi_i=(3/2)zeta_c(Omega_m/Omega_r)a_i"
                    "-mu^2 a_i^4/(5 Omega_r)+O(r_i^2,a_i^5)"
                ),
                "derivation": "regular Frobenius branch; the e^{-N} singular mode is excluded",
                "status": "DERIVED_BOUNDARY_CONDITION",
            },
            {
                "equation": "local_Gdot",
                "formula": (
                    "Gdot/G=H0 q0 d_phi ln{[(2f+4f_phi^2)/(2f+3f_phi^2)]/f}"
                ),
                "derivation": "checkpoint-5204 Cavendish map evaluated on the refitted state",
                "status": "DIRECT_LOCAL_PREDICTION",
            },
        ]
    )
    diagnostics = {
        "raychaudhuri_residual": str(raychaudhuri_residual),
        "scalar_residual": str(scalar_residual),
        "h_closed": str(h_closed),
    }
    return rows, diagnostics


def field_quantities(
    n_value: float,
    phi_value: float,
    q_value: float,
    omega_m: float,
    mu_value: float,
    zeta: float,
) -> dict[str, float]:
    reduced_f = 1.0 + zeta * phi_value**2
    reduced_f_n = 2.0 * zeta * phi_value * q_value
    denominator = reduced_f + reduced_f_n - q_value**2 / 6.0
    numerator = (
        omega_m * math.exp(-3.0 * n_value)
        + OMEGA_R * math.exp(-4.0 * n_value)
        + mu_value**2 * phi_value**2 / 6.0
    )
    if denominator <= 0.0 or numerator <= 0.0 or reduced_f <= 0.0:
        raise ValueError("left the positive-F positive-Hamiltonian branch")
    e_squared = numerator / denominator
    omega_m_n = omega_m * math.exp(-3.0 * n_value) / e_squared
    omega_r_n = OMEGA_R * math.exp(-4.0 * n_value) / e_squared
    h_numerator = (
        3.0 * omega_m_n
        + 4.0 * omega_r_n
        + (1.0 + 2.0 * zeta) * q_value**2
        - 8.0 * zeta * phi_value * q_value
        - 2.0 * zeta * mu_value**2 * phi_value**2 / e_squared
        + 24.0 * zeta**2 * phi_value**2
    )
    h_denominator = 2.0 * reduced_f + 12.0 * zeta**2 * phi_value**2
    h_value = -h_numerator / h_denominator
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
        "hamiltonian_denominator": denominator,
        "Omega_m": omega_m_n,
        "Omega_r": omega_r_n,
    }


def regular_ratio(
    omega_m: float,
    mu_value: float,
    zeta: float,
    n_initial: float,
) -> float:
    scale_factor = math.exp(n_initial)
    matter_to_radiation = omega_m * scale_factor / OMEGA_R
    return (
        1.5 * zeta * matter_to_radiation
        - mu_value**2 * scale_factor**4 / (5.0 * OMEGA_R)
    )


def integrate_from_amplitude(
    amplitude: float,
    omega_m: float,
    mu_value: float,
    zeta: float,
    n_initial: float,
    accuracy: str,
    dense_output: bool,
) -> Any:
    if accuracy == "fit":
        rtol, atol, max_step = 3.0e-8, 3.0e-10, 0.1
    elif accuracy == "exact":
        rtol, atol, max_step = 2.0e-11, 2.0e-13, 0.03
    else:
        raise ValueError(accuracy)
    initial_q = regular_ratio(omega_m, mu_value, zeta, n_initial) * amplitude

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        quantities = field_quantities(
            float(n_value),
            float(state[0]),
            float(state[1]),
            omega_m,
            mu_value,
            zeta,
        )
        return np.asarray([state[1], quantities["qN"]], dtype=float)

    solution = integrate.solve_ivp(
        rhs,
        (n_initial, 0.0),
        np.asarray([amplitude, initial_q], dtype=float),
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=dense_output,
    )
    if not solution.success:
        raise ValueError(solution.message)
    return solution


def solve_st_background(
    params: dict[str, float],
    zeta: float,
    accuracy: str = "fit",
    n_initial: float = N_INITIAL,
) -> STSolution:
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
    omega_m = float(params["Omega_m"])
    mu_value = 10.0 ** float(params["log10_mu"])
    if not (0.05 < omega_m < 0.65):
        raise ValueError("Omega_m outside physical branch")
    if not (0.005 < mu_value < 5.1):
        raise ValueError("mu outside implemented branch")
    if not (-0.01 < zeta < 0.01):
        raise ValueError("zeta outside tested near-minimal branch")

    def present_constraint(amplitude: float) -> float:
        solution = integrate_from_amplitude(
            amplitude,
            omega_m,
            mu_value,
            zeta,
            n_initial,
            accuracy,
            dense_output=False,
        )
        phi_zero = float(solution.y[0, -1])
        q_zero = float(solution.y[1, -1])
        return (
            field_quantities(
                0.0,
                phi_zero,
                q_zero,
                omega_m,
                mu_value,
                zeta,
            )["E2"]
            - 1.0
        )

    lower = 0.0
    lower_value = present_constraint(lower)
    upper = 2.0
    upper_value = math.nan
    while upper < 100.0:
        try:
            upper_value = present_constraint(upper)
        except (ValueError, OverflowError, FloatingPointError):
            upper_value = math.nan
        if math.isfinite(upper_value) and lower_value * upper_value < 0.0:
            break
        upper *= 1.5
    if not math.isfinite(upper_value) or lower_value * upper_value >= 0.0:
        raise ValueError("flatness amplitude root is not bracketed")
    tolerance = 2.0e-8 if accuracy == "fit" else 2.0e-12
    root = optimize.root_scalar(
        present_constraint,
        bracket=(lower, upper),
        method="toms748",
        xtol=tolerance,
        rtol=tolerance,
        maxiter=80,
    )
    if not root.converged:
        raise ValueError("flatness amplitude shoot failed")
    solution = integrate_from_amplitude(
        float(root.root),
        omega_m,
        mu_value,
        zeta,
        n_initial,
        accuracy,
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
            omega_m,
            mu_value,
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
        denominator_grid[index] = quantities["hamiltonian_denominator"]
        constraint_left = e_squared * (
            quantities["f"]
            + quantities["fN"]
            - float(q_value) ** 2 / 6.0
        )
        constraint_right = (
            omega_m * math.exp(-3.0 * float(n_value))
            + OMEGA_R * math.exp(-4.0 * float(n_value))
            + mu_value**2 * float(phi_value) ** 2 / 6.0
        )
        constraint_grid[index] = (
            constraint_left - constraint_right
        ) / max(
            abs(constraint_left),
            abs(constraint_right),
            1.0,
        )
    geff_grid = np.asarray(
        [
            checkpoint_5204.gcav_ratio(zeta, float(phi_value))
            for phi_value in phi_grid
        ],
        dtype=float,
    )
    h_numeric = np.gradient(np.log(e_grid), n_grid, edge_order=2)
    phi_zero = float(phi_grid[-1])
    q_zero = float(q_grid[-1])
    h0_year = float(params["H0"]) * H0_TO_YEAR_INV
    gdot = (
        checkpoint_5204.dln_gcav_dphi(zeta, phi_zero)
        * q_zero
        * h0_year
    )
    theta_zero = math.atan2(-q_zero, mu_value * phi_zero)
    initial_matter_ratio = omega_m * math.exp(n_initial) / OMEGA_R
    regular_remainder_bound = (
        abs(zeta) * initial_matter_ratio**2
        + mu_value**2 * math.exp(5.0 * n_initial) / OMEGA_R
    )
    background = checkpoint_5195.checkpoint_5194.Background(
        model="ParentScalar_Lambda_zero",
        omega_m=omega_m,
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
        "method": "forward_regular_Frobenius_and_flatness_amplitude_shoot",
        "accuracy": accuracy,
        "n_initial": n_initial,
        "mu": mu_value,
        "zeta": zeta,
        "initial_phi_amplitude": float(root.root),
        "initial_chi_over_sqrt6_MR": float(root.root) / math.sqrt(6.0),
        "initial_regular_q_over_phi": regular_ratio(
            omega_m, mu_value, zeta, n_initial
        ),
        "initial_matter_to_radiation": initial_matter_ratio,
        "regular_series_remainder_bound": regular_remainder_bound,
        "flatness_root_iterations": int(root.iterations),
        "phi0": phi_zero,
        "q0": q_zero,
        "theta0": theta_zero,
        "E0": float(e_grid[-1]),
        "h0": float(h_grid[-1]),
        "minimum_f": float(np.min(f_grid)),
        "minimum_Hamiltonian_denominator": float(np.min(denominator_grid)),
        "minimum_Einstein_kinetic": float(
            np.min(
                1.0 / f_grid
                + 1.5
                * (
                    2.0
                    * zeta
                    * phi_grid
                    / f_grid
                )
                ** 2
            )
        ),
        "maximum_constraint_residual": float(np.max(np.abs(constraint_grid))),
        "maximum_h_derivative_residual": float(
            np.max(np.abs(h_numeric[2:-2] - h_grid[2:-2]))
        ),
        "alpha_squared_0": checkpoint_5204.alpha_squared(zeta, phi_zero),
        "gamma_minus_one_0": checkpoint_5204.gamma_minus_one(zeta, phi_zero),
        "Gcav_over_Gbare_0": checkpoint_5204.gcav_ratio(zeta, phi_zero),
        "Gdot_over_G_yr_inv": gdot,
        "geff_minimum": float(np.min(geff_grid)),
        "geff_maximum": float(np.max(geff_grid)),
    }
    background.parent_diagnostics = dict(diagnostics)
    payload = STSolution(
        background=background,
        phi_grid=phi_grid,
        q_grid=q_grid,
        geff_grid=geff_grid,
        diagnostics=diagnostics,
    )
    BACKGROUND_CACHE[key] = payload
    return payload


def minimal_parent_calibration(
    params: dict[str, float],
    accuracy: str,
) -> tuple[dict[str, float], STSolution]:
    key = (
        round(float(params["Omega_m"]), 10),
        round(float(params["log10_mu"]), 10),
        round(float(params["H0"]), 8),
        round(float(params["Omega_b_h2"]), 10),
        accuracy,
    )
    if key in EARLY_CALIBRATION_CACHE:
        cached = EARLY_CALIBRATION_CACHE[key]
        return cached["summary"], cached["solution"]
    minimal_solution = solve_st_background(
        params,
        0.0,
        accuracy=accuracy,
    )
    summary = checkpoint_5195.camb_background_summary(
        "ParentScalar_Lambda_zero",
        params,
        minimal_solution.background,
    )
    EARLY_CALIBRATION_CACHE[key] = {
        "summary": summary,
        "solution": minimal_solution,
    }
    return summary, minimal_solution


def sound_integral(
    e_function: Callable[[np.ndarray], np.ndarray],
    n_lower: float,
    n_upper: float,
    omega_b_h2: float,
) -> float:
    n_nodes = np.linspace(n_lower, n_upper, 1801)
    baryon_loading = 3.0 * omega_b_h2 / (4.0 * OMEGA_GAMMA_H2)
    sound_speed = 1.0 / np.sqrt(
        3.0 * (1.0 + baryon_loading * np.exp(n_nodes))
    )
    e_values = np.asarray(e_function(n_nodes), dtype=float)
    integrand = np.exp(-n_nodes) * sound_speed / e_values
    tail = math.exp(-n_lower) / (
        math.sqrt(3.0) * float(e_values[0])
    )
    return tail + float(integrate.simpson(integrand, x=n_nodes))


def scalar_tensor_calibration(
    solution: STSolution,
    params: dict[str, float],
) -> dict[str, float]:
    base, minimal_solution = minimal_parent_calibration(
        params,
        str(solution.diagnostics["accuracy"]),
    )
    background = solution.background
    omega_m = float(params["Omega_m"])
    e_interpolator = checkpoint_5195.checkpoint_5194.interpolate.PchipInterpolator(
        background.n_grid,
        background.e_grid,
        extrapolate=False,
    )
    minimal_e_interpolator = (
        checkpoint_5195.checkpoint_5194.interpolate.PchipInterpolator(
            minimal_solution.background.n_grid,
            minimal_solution.background.e_grid,
            extrapolate=False,
        )
    )

    def st_e(n_values: np.ndarray) -> np.ndarray:
        return np.asarray(e_interpolator(n_values), dtype=float)

    def comparator_e(n_values: np.ndarray) -> np.ndarray:
        return np.asarray(minimal_e_interpolator(n_values), dtype=float)

    n_drag = -math.log1p(base["zdrag"])
    n_star = -math.log1p(base["zstar"])
    st_drag_integral = sound_integral(
        st_e,
        N_INITIAL,
        n_drag,
        float(params["Omega_b_h2"]),
    )
    comparator_drag_integral = sound_integral(
        comparator_e,
        N_INITIAL,
        n_drag,
        float(params["Omega_b_h2"]),
    )
    st_star_integral = sound_integral(
        st_e,
        N_INITIAL,
        n_star,
        float(params["Omega_b_h2"]),
    )
    comparator_star_integral = sound_integral(
        comparator_e,
        N_INITIAL,
        n_star,
        float(params["Omega_b_h2"]),
    )
    drag_ratio = st_drag_integral / comparator_drag_integral
    star_ratio = st_star_integral / comparator_star_integral
    r_drag = base["rdrag_Mpc"] * drag_ratio
    r_star = base["rstar_Mpc"] * star_ratio
    distance_star = checkpoint_5195.dimensionless_comoving(
        background,
        base["zstar"],
    )
    comparator_distance_star = checkpoint_5195.dimensionless_comoving(
        minimal_solution.background,
        base["zstar"],
    )
    distance_ratio = distance_star / comparator_distance_star
    dm_star_mpc = base["DAstar_Gpc"] * 1000.0 * distance_ratio
    l_a = math.pi * dm_star_mpc / r_star
    shift_r = math.sqrt(omega_m) * float(params["H0"]) * dm_star_mpc / C_KM_S
    age_integrand = 1.0 / background.e_grid
    age_hubble_units = float(
        integrate.simpson(age_integrand, x=background.n_grid)
        + 1.0 / (2.0 * background.e_grid[0])
    )
    comparator_age_nodes = minimal_solution.background.n_grid
    comparator_age_hubble_units = float(
        integrate.simpson(
            1.0 / comparator_e(comparator_age_nodes),
            x=comparator_age_nodes,
        )
        + 1.0 / (2.0 * comparator_e(comparator_age_nodes[:1])[0])
    )
    age_gyr = base["age_Gyr"] * (
        age_hubble_units / comparator_age_hubble_units
    )
    return {
        "R": shift_r,
        "l_A": l_a,
        "rdrag_Mpc": r_drag,
        "rstar_Mpc": r_star,
        "zstar": base["zstar"],
        "zdrag": base["zdrag"],
        "DAstar_Gpc": dm_star_mpc / 1000.0,
        "thetastar": 100.0 * math.pi / l_a,
        "age_Gyr": age_gyr,
        "Omega_m_CAMB": base["Omega_m_CAMB"],
        "omch2": base["omch2"],
        "rdrag_scalar_tensor_ratio": drag_ratio,
        "rstar_scalar_tensor_ratio": star_ratio,
        "distance_scalar_tensor_ratio": distance_ratio,
        "fixed_recombination_redshift_approximation": True,
        "maximum_pre_recombination_H_fractional_shift": float(
            np.max(
                np.abs(
                    background.e_grid[background.n_grid <= n_star]
                    / comparator_e(background.n_grid[background.n_grid <= n_star])
                    - 1.0
                )
            )
        ),
    }


def solve_growth(
    solution: STSolution,
    normalize_to_present_gcav: bool,
) -> dict[str, np.ndarray]:
    background = solution.background
    n_grid = np.asarray(background.n_grid, dtype=float)
    e_grid = np.asarray(background.e_grid, dtype=float)
    h_grid = np.asarray(background.h_grid, dtype=float)
    geff = np.asarray(solution.geff_grid, dtype=float)
    if normalize_to_present_gcav:
        geff = geff / float(geff[-1])
    coefficient_a = 2.0 + h_grid
    coefficient_b = (
        1.5
        * background.omega_m
        * np.exp(-3.0 * n_grid)
        / e_grid**2
        * geff
    )
    equality_ratio = (
        background.omega_m * math.exp(float(n_grid[0])) / OMEGA_R
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
        "geff_normalized_to_present": np.asarray(normalize_to_present_gcav),
    }


def growth_shape_at_z(
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


def profile_growth_st(
    solution: STSolution,
    blocks: list[checkpoint_5195.checkpoint_5194.DataBlock],
    detail: bool,
    normalize_to_present_gcav: bool = False,
) -> dict[str, Any]:
    growth_solution = solve_growth(solution, normalize_to_present_gcav)
    observations: list[float] = []
    design_values: list[float] = []
    covariance_blocks: list[np.ndarray] = []
    contexts: list[dict[str, Any]] = []
    for block in blocks:
        indices = [
            index
            for index, row in enumerate(block.rows)
            if row[2] == "f_sigma8"
        ]
        covariance_blocks.append(block.covariance[np.ix_(indices, indices)])
        for index in indices:
            redshift, observed, quantity = block.rows[index]
            observations.append(float(observed))
            design_values.append(growth_shape_at_z(growth_solution, redshift))
            contexts.append(
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
    design = np.asarray(design_values, dtype=float)
    denominator = float(design @ inverse @ design)
    if denominator <= 0.0:
        raise ValueError("non-positive growth nuisance curvature")
    sigma8_unbounded = float(design @ inverse @ observed_vector / denominator)
    sigma8_zero = float(
        np.clip(sigma8_unbounded, *checkpoint_5195.SIGMA8_BOUNDS)
    )
    prediction = sigma8_zero * design
    residual = observed_vector - prediction
    chi2_value = float(residual @ inverse @ residual)
    edge_flag = min(
        sigma8_zero - checkpoint_5195.SIGMA8_BOUNDS[0],
        checkpoint_5195.SIGMA8_BOUNDS[1] - sigma8_zero,
    ) <= 0.01 * (
        checkpoint_5195.SIGMA8_BOUNDS[1]
        - checkpoint_5195.SIGMA8_BOUNDS[0]
    )
    residual_rows: list[dict[str, Any]] = []
    if detail:
        diagonal_sigma = np.sqrt(np.diag(covariance))
        signed_chi2 = residual * (inverse @ residual)
        for context, predicted, residual_value, sigma_value, contribution in zip(
            contexts,
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
        "normalize_to_present_gcav": normalize_to_present_gcav,
    }


def local_score(solution: STSolution) -> dict[str, float]:
    gamma_value = float(solution.diagnostics["gamma_minus_one_0"])
    gdot_value = float(solution.diagnostics["Gdot_over_G_yr_inv"])
    chi2_gamma = (
        (gamma_value - LOCAL_GAMMA_MEAN) / LOCAL_GAMMA_SIGMA
    ) ** 2
    chi2_gdot = (
        (gdot_value - LOCAL_GDOT_MEAN_YR_INV) / LOCAL_GDOT_SIGMA_YR_INV
    ) ** 2
    return {
        "gamma_minus_one": gamma_value,
        "Gdot_over_G_yr_inv": gdot_value,
        "chi2_Cassini": chi2_gamma,
        "chi2_LLR_Gdot": chi2_gdot,
        "chi2_local": chi2_gamma + chi2_gdot,
        "Cassini_two_sigma_envelope_pass": float(
            abs(gamma_value) <= LOCAL_GAMMA_TWO_SIGMA_ENVELOPE
        ),
        "Gdot_two_sigma_envelope_pass": float(
            abs(gdot_value) <= LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV
        ),
    }


def score_st_model(
    params: dict[str, float],
    zeta: float,
    data: checkpoint_5195.JointData,
    accuracy: str = "fit",
    detail: bool = False,
    normalize_growth_to_present_gcav: bool = False,
) -> dict[str, Any]:
    key = (
        round(float(params["Omega_m"]), 10),
        round(float(params["log10_mu"]), 10),
        round(float(params["H0"]), 8),
        round(float(params["Omega_b_h2"]), 10),
        round(float(zeta), 12),
        accuracy,
        normalize_growth_to_present_gcav,
    )
    if not detail and key in SCORE_CACHE:
        return SCORE_CACHE[key]
    solution = solve_st_background(params, zeta, accuracy=accuracy)
    calibration = scalar_tensor_calibration(solution, params)
    physical_alpha = C_KM_S / (
        float(params["H0"]) * calibration["rdrag_Mpc"]
    )
    late = checkpoint_5195.profile_sn_and_desi(
        solution.background,
        data.late,
        physical_alpha,
        detail=detail,
    )
    growth = profile_growth_st(
        solution,
        data.growth_blocks,
        detail=detail,
        normalize_to_present_gcav=normalize_growth_to_present_gcav,
    )
    cmb = checkpoint_5195.profile_cmb_prior(
        data.planck_priors[checkpoint_5195.PRIMARY_CONFIG.planck_prior_model],
        calibration,
        float(params["Omega_b_h2"]),
    )
    local = local_score(solution)
    chi2_cosmology = (
        float(late["chi2_SN"])
        + float(late["chi2_DESI"])
        + float(growth["chi2_growth"])
        + float(cmb["chi2_CMB"])
    )
    chi2_joint = chi2_cosmology + float(local["chi2_local"])
    if not math.isfinite(chi2_joint):
        raise ValueError("non-finite scalar-tensor score")
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
        "sn_offset": float(late["sn_offset"]),
        "physical_alpha": physical_alpha,
        "sigma8_0_profiled": float(growth["sigma8_0_profiled"]),
        "sigma8_edge_flag": bool(growth["sigma8_edge_flag"]),
        "n_s_profiled": float(cmb["n_s_profiled"]),
        "n_s_edge_flag": bool(cmb["n_s_edge_flag"]),
        "R": float(calibration["R"]),
        "l_A": float(calibration["l_A"]),
        "rdrag_Mpc": float(calibration["rdrag_Mpc"]),
        "rstar_Mpc": float(calibration["rstar_Mpc"]),
        "rdrag_scalar_tensor_ratio": float(
            calibration["rdrag_scalar_tensor_ratio"]
        ),
        "rstar_scalar_tensor_ratio": float(
            calibration["rstar_scalar_tensor_ratio"]
        ),
        "maximum_pre_recombination_H_fractional_shift": float(
            calibration["maximum_pre_recombination_H_fractional_shift"]
        ),
        "background_diagnostics": dict(solution.diagnostics),
        "local": local,
        "growth_normalized_to_present_gcav": normalize_growth_to_present_gcav,
        "growth_residual_rows": growth["residual_rows"] if detail else [],
        "late_detail": late if detail else {},
        "solution": solution if detail else None,
    }
    if not detail:
        SCORE_CACHE[key] = payload
    return payload


def parameter_vector(
    params: dict[str, float],
    zeta: float,
) -> np.ndarray:
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


def fit_st_model(
    spec: FitSpec,
    data: checkpoint_5195.JointData,
    locked_minimal: dict[str, Any],
) -> dict[str, Any]:
    priors = (
        (0.15, 0.45),
        (-2.0, math.log10(5.0)),
        checkpoint_5195.H0_BOUNDS,
        checkpoint_5195.OMBH2_BOUNDS,
        spec.zeta_bounds,
    )
    locked_params = {
        key: float(value)
        for key, value in locked_minimal["params"].items()
    }
    starts = [
        parameter_vector(locked_params, start_zeta)
        for start_zeta in spec.starts
    ]
    objective_cache: dict[tuple[float, ...], float] = {}
    failure_counts: dict[str, int] = {}
    evaluations = 0

    def objective(vector: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        key = tuple(round(float(value), 10) for value in vector)
        if key in objective_cache:
            return objective_cache[key]
        try:
            params, zeta = vector_parameters(vector)
            value = score_st_model(
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
            checkpoint_5195.camb.baseconfig.CAMBError,
        ) as exc:
            failure_name = type(exc).__name__
            failure_counts[failure_name] = failure_counts.get(failure_name, 0) + 1
            value = 1.0e30
        objective_cache[key] = float(value)
        return float(value)

    finite_difference_steps = np.asarray(
        [
            3.0e-5,
            2.7e-4,
            4.0e-3,
            5.0e-7,
            2.0e-7,
        ],
        dtype=float,
    )
    optimizer_results: list[Any] = []
    start_time = time.perf_counter()
    for start in starts:
        result = optimize.minimize(
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
        optimizer_results.append(result)
    finite_results = [
        result
        for result in optimizer_results
        if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e29
    ]
    if not finite_results:
        raise RuntimeError(f"all starts failed for {spec.name}")
    best = min(finite_results, key=lambda result: float(result.fun))
    best_params, best_zeta = vector_parameters(np.asarray(best.x, dtype=float))
    exact_score = score_st_model(
        best_params,
        best_zeta,
        data,
        accuracy="exact",
        detail=True,
    )
    edge_rows: list[dict[str, Any]] = []
    names = ["Omega_m", "log10_mu", "H0", "Omega_b_h2", "zeta_c"]
    values = [
        best_params["Omega_m"],
        best_params["log10_mu"],
        best_params["H0"],
        best_params["Omega_b_h2"],
        best_zeta,
    ]
    for name, value, bounds in zip(names, values, priors, strict=True):
        fractional_distance = min(
            value - bounds[0],
            bounds[1] - value,
        ) / (bounds[1] - bounds[0])
        edge_rows.append(
            {
                "model": spec.name,
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
            exact_score["n_s_profiled"],
            checkpoint_5195.NS_BOUNDS,
            exact_score["n_s_edge_flag"],
        ),
        (
            "sigma8_0",
            exact_score["sigma8_0_profiled"],
            checkpoint_5195.SIGMA8_BOUNDS,
            exact_score["sigma8_edge_flag"],
        ),
    ):
        edge_rows.append(
            {
                "model": spec.name,
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
    start_values = sorted(float(result.fun) for result in finite_results)
    fit = {
        "model": spec.name,
        "params": best_params,
        "zeta": best_zeta,
        "priors": {
            name: list(bounds)
            for name, bounds in zip(names, priors, strict=True)
        },
        **{
            key: value
            for key, value in exact_score.items()
            if key not in {"solution", "growth_residual_rows", "late_detail"}
        },
        "n_cosmology": PRIMARY_N_COSMOLOGY,
        "n_joint": PRIMARY_N_WITH_LOCAL,
        "k": k_count,
        "AIC_cosmology": exact_score["chi2_cosmology"] + 2.0 * k_count,
        "BIC_cosmology": exact_score["chi2_cosmology"]
        + k_count * math.log(PRIMARY_N_COSMOLOGY),
        "AIC_joint": exact_score["chi2_joint"] + 2.0 * k_count,
        "BIC_joint": exact_score["chi2_joint"]
        + k_count * math.log(PRIMARY_N_WITH_LOCAL),
        "convergence": (
            math.isfinite(exact_score["chi2_joint"])
            and abs(float(best.fun) - exact_score["chi2_joint"]) < 0.02
        ),
        "optimizer_success": bool(best.success),
        "optimizer_message": str(best.message),
        "objective_evaluations": evaluations,
        "unique_objective_evaluations": len(objective_cache),
        "successful_start_count": len(start_values),
        "multistart_chi2_span": (
            max(start_values) - min(start_values)
            if len(start_values) > 1
            else 0.0
        ),
        "prior_edge_flag": any(bool(row["edge_flag"]) for row in edge_rows),
        "edge_rows": edge_rows,
        "failure_counts": failure_counts,
        "runtime_seconds": time.perf_counter() - start_time,
        "growth_residual_rows": exact_score["growth_residual_rows"],
        "solution": exact_score["solution"],
    }
    print(
        json.dumps(
            {
                "model": spec.name,
                "chi2_joint": fit["chi2_joint"],
                "chi2_cosmology": fit["chi2_cosmology"],
                "zeta": fit["zeta"],
                "params": best_params,
                "edge": fit["prior_edge_flag"],
                "evaluations": evaluations,
                "runtime_seconds": fit["runtime_seconds"],
            }
        ),
        flush=True,
    )
    return fit


def locked_model_rows(
    locked_fits: dict[str, dict[str, Any]],
    minimal_score: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    baseline_local = (
        (0.0 - LOCAL_GAMMA_MEAN) / LOCAL_GAMMA_SIGMA
    ) ** 2 + (
        (0.0 - LOCAL_GDOT_MEAN_YR_INV) / LOCAL_GDOT_SIGMA_YR_INV
    ) ** 2
    for model in ("LCDM", "wCDM", "CPL"):
        fit = locked_fits[model]
        chi2_cosmology = float(fit["chi2_total"])
        chi2_joint = chi2_cosmology + baseline_local
        k_count = int(fit["k"])
        rows.append(
            {
                "model": model,
                "source": "locked_checkpoint_5195_primary_fit",
                "chi2_SN": fit["chi2_SN"],
                "chi2_DESI": fit["chi2_DESI"],
                "chi2_growth": fit["chi2_growth"],
                "chi2_CMB": fit["chi2_CMB"],
                "chi2_cosmology": chi2_cosmology,
                "chi2_local": baseline_local,
                "chi2_joint": chi2_joint,
                "gamma_minus_one": 0.0,
                "Gdot_over_G_yr_inv": 0.0,
                "k": k_count,
                "AIC_cosmology": chi2_cosmology + 2.0 * k_count,
                "BIC_cosmology": chi2_cosmology
                + k_count * math.log(PRIMARY_N_COSMOLOGY),
                "AIC_joint": chi2_joint + 2.0 * k_count,
                "BIC_joint": chi2_joint
                + k_count * math.log(PRIMARY_N_WITH_LOCAL),
                "prior_edge_flag": fit["prior_edge_flag"],
            }
        )
    minimal_locked = locked_fits["ParentScalar_Lambda_zero"]
    k_count = int(minimal_locked["k"])
    rows.append(
        {
            "model": "ParentScalar_Lambda_zero_minimal_locked",
            "source": "5206 exact zeta=0 rebuild of locked checkpoint-5195 parameters",
            "chi2_SN": minimal_score["chi2_SN"],
            "chi2_DESI": minimal_score["chi2_DESI"],
            "chi2_growth": minimal_score["chi2_growth"],
            "chi2_CMB": minimal_score["chi2_CMB"],
            "chi2_cosmology": minimal_score["chi2_cosmology"],
            "chi2_local": minimal_score["chi2_local"],
            "chi2_joint": minimal_score["chi2_joint"],
            "gamma_minus_one": minimal_score["local"]["gamma_minus_one"],
            "Gdot_over_G_yr_inv": minimal_score["local"][
                "Gdot_over_G_yr_inv"
            ],
            "k": k_count,
            "AIC_cosmology": minimal_score["chi2_cosmology"]
            + 2.0 * k_count,
            "BIC_cosmology": minimal_score["chi2_cosmology"]
            + k_count * math.log(PRIMARY_N_COSMOLOGY),
            "AIC_joint": minimal_score["chi2_joint"] + 2.0 * k_count,
            "BIC_joint": minimal_score["chi2_joint"]
            + k_count * math.log(PRIMARY_N_WITH_LOCAL),
            "prior_edge_flag": False,
        }
    )
    return tagged(rows)


def st_fit_summary_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "model": fit["model"],
                "chi2_SN": fit["chi2_SN"],
                "chi2_DESI": fit["chi2_DESI"],
                "chi2_growth": fit["chi2_growth"],
                "chi2_CMB": fit["chi2_CMB"],
                "chi2_cosmology": fit["chi2_cosmology"],
                "chi2_Cassini": fit["chi2_Cassini"],
                "chi2_LLR_Gdot": fit["chi2_LLR_Gdot"],
                "chi2_local": fit["chi2_local"],
                "chi2_joint": fit["chi2_joint"],
                "k": fit["k"],
                "AIC_cosmology": fit["AIC_cosmology"],
                "BIC_cosmology": fit["BIC_cosmology"],
                "AIC_joint": fit["AIC_joint"],
                "BIC_joint": fit["BIC_joint"],
                "convergence": fit["convergence"],
                "optimizer_success": fit["optimizer_success"],
                "prior_edge_flag": fit["prior_edge_flag"],
                "objective_evaluations": fit["objective_evaluations"],
                "runtime_seconds": fit["runtime_seconds"],
            }
            for fit in fits
        ]
    )


def parameter_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        for name, value in (
            ("Omega_m", fit["params"]["Omega_m"]),
            ("log10_mu", fit["params"]["log10_mu"]),
            ("mu_mgap_over_H0", 10.0 ** fit["params"]["log10_mu"]),
            ("H0", fit["params"]["H0"]),
            ("Omega_b_h2", fit["params"]["Omega_b_h2"]),
            ("zeta_c", fit["zeta"]),
            ("n_s", fit["n_s_profiled"]),
            ("sigma8_0", fit["sigma8_0_profiled"]),
            ("phi0", fit["background_diagnostics"]["phi0"]),
            ("q0_dphi_dN", fit["background_diagnostics"]["q0"]),
            ("theta0", fit["background_diagnostics"]["theta0"]),
            (
                "initial_phi_amplitude_N_minus_18",
                fit["background_diagnostics"]["initial_phi_amplitude"],
            ),
        ):
            rows.append(
                {
                    "model": fit["model"],
                    "parameter": name,
                    "value": value,
                    "status": (
                        "OPTIMIZED"
                        if name
                        in {
                            "Omega_m",
                            "log10_mu",
                            "H0",
                            "Omega_b_h2",
                            "zeta_c",
                        }
                        else "DERIVED_OR_PROFILED"
                    ),
                }
            )
        rows.extend(fit["edge_rows"])
    return tagged(rows)


def local_rows(
    fits: list[dict[str, Any]],
    minimal_score: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    all_models = [
        (
            "ParentScalar_Lambda_zero_minimal_locked",
            minimal_score,
        )
    ] + [(fit["model"], fit) for fit in fits]
    for model, score in all_models:
        diagnostics = score["background_diagnostics"]
        rows.append(
            {
                "model": model,
                "zeta_c": score["zeta"],
                "phi0": diagnostics["phi0"],
                "q0": diagnostics["q0"],
                "alpha_squared_0": diagnostics["alpha_squared_0"],
                "gamma_minus_one": diagnostics["gamma_minus_one_0"],
                "Cassini_mean": LOCAL_GAMMA_MEAN,
                "Cassini_sigma": LOCAL_GAMMA_SIGMA,
                "chi2_Cassini": score["chi2_Cassini"],
                "Gdot_over_G_yr_inv": diagnostics["Gdot_over_G_yr_inv"],
                "LLR_mean_yr_inv": LOCAL_GDOT_MEAN_YR_INV,
                "LLR_sigma_yr_inv": LOCAL_GDOT_SIGMA_YR_INV,
                "chi2_LLR_Gdot": score["chi2_LLR_Gdot"],
                "chi2_local": score["chi2_local"],
                "Cassini_two_sigma_envelope_pass": abs(
                    diagnostics["gamma_minus_one_0"]
                )
                <= LOCAL_GAMMA_TWO_SIGMA_ENVELOPE,
                "Gdot_two_sigma_envelope_pass": abs(
                    diagnostics["Gdot_over_G_yr_inv"]
                )
                <= LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV,
                "Gcav_over_Gbare_0": diagnostics["Gcav_over_Gbare_0"],
                "minimum_f": diagnostics["minimum_f"],
                "minimum_Einstein_kinetic": diagnostics[
                    "minimum_Einstein_kinetic"
                ],
            }
        )
    return tagged(rows)


def comparison_rows(
    locked_rows: list[dict[str, Any]],
    fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {
        row["model"]: row for row in locked_rows
    }
    for fit in fits:
        lookup[fit["model"]] = fit
    rows: list[dict[str, Any]] = []
    baselines = (
        "LCDM",
        "wCDM",
        "CPL",
        "ParentScalar_Lambda_zero_minimal_locked",
    )
    for fit in fits:
        for baseline_name in baselines:
            baseline = lookup[baseline_name]
            rows.append(
                {
                    "model": fit["model"],
                    "baseline": baseline_name,
                    "delta_chi2_cosmology": fit["chi2_cosmology"]
                    - float(baseline["chi2_cosmology"]),
                    "delta_AIC_cosmology": fit["AIC_cosmology"]
                    - float(baseline["AIC_cosmology"]),
                    "delta_BIC_cosmology": fit["BIC_cosmology"]
                    - float(baseline["BIC_cosmology"]),
                    "delta_chi2_joint": fit["chi2_joint"]
                    - float(baseline["chi2_joint"]),
                    "delta_AIC_joint": fit["AIC_joint"]
                    - float(baseline["AIC_joint"]),
                    "delta_BIC_joint": fit["BIC_joint"]
                    - float(baseline["BIC_joint"]),
                    "model_edge_flag": fit["prior_edge_flag"],
                    "baseline_edge_flag": baseline["prior_edge_flag"],
                    "interpretation": (
                        "negative favors the scalar-tensor model; "
                        "abs(delta)<2 is draw-scale"
                    ),
                }
            )
    return tagged(rows)


def regular_validation_rows(
    fits: list[dict[str, Any]],
    minimal_score: dict[str, Any],
    locked_minimal: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    locked_chi = float(locked_minimal["chi2_total"])
    rows.append(
        {
            "model": "ParentScalar_Lambda_zero_minimal_locked",
            "test": "zeta_zero_locked_likelihood_reproduction",
            "value": minimal_score["chi2_cosmology"] - locked_chi,
            "tolerance": 1.0e-4,
            "pass": abs(minimal_score["chi2_cosmology"] - locked_chi) < 1.0e-4,
        }
    )
    for fit in fits:
        diagnostics = fit["background_diagnostics"]
        exact_solution = fit["solution"]
        start_sensitivity = solve_st_background(
            fit["params"],
            fit["zeta"],
            accuracy="exact",
            n_initial=-16.0,
        )
        comparison_n = np.linspace(-12.0, 0.0, 1201)
        exact_e = exact_solution.background.values_at_n(comparison_n)[0]
        short_e = start_sensitivity.background.values_at_n(comparison_n)[0]
        maximum_relative_e = float(
            np.max(np.abs(short_e / exact_e - 1.0))
        )
        for test, value, tolerance, passed in (
            (
                "flatness_constraint",
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
                "initial_surface_sensitivity",
                maximum_relative_e,
                2.0e-6,
                maximum_relative_e < 2.0e-6,
            ),
            (
                "regular_series_remainder",
                diagnostics["regular_series_remainder_bound"],
                1.0e-8,
                diagnostics["regular_series_remainder_bound"] < 1.0e-8,
            ),
        ):
            rows.append(
                {
                    "model": fit["model"],
                    "test": test,
                    "value": value,
                    "tolerance": tolerance,
                    "pass": passed,
                }
            )
    return tagged(rows)


def growth_validation_rows(
    fits: list[dict[str, Any]],
    data: checkpoint_5195.JointData,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        solution = fit["solution"]
        normalized = profile_growth_st(
            solution,
            data.growth_blocks,
            detail=False,
            normalize_to_present_gcav=True,
        )
        mu_value = 10.0 ** fit["params"]["log10_mu"]
        mass_wave_number = (
            mu_value * float(fit["params"]["H0"]) / C_KM_S
        )
        k_min = K_MIN_H_MPC * float(fit["params"]["H0"]) / 100.0
        yukawa_ratio_squared = (mass_wave_number / k_min) ** 2
        rows.extend(
            [
                {
                    "model": fit["model"],
                    "test": "massless_quasistatic_growth_range_error_bound",
                    "value": yukawa_ratio_squared / (1.0 + yukawa_ratio_squared),
                    "pass": yukawa_ratio_squared / (1.0 + yukawa_ratio_squared)
                    < 1.0e-3,
                    "detail": (
                        "maximum correction at k=0.01 h/Mpc; smaller at larger k"
                    ),
                },
                {
                    "model": fit["model"],
                    "test": "bare_vs_present_Gcav_growth_score",
                    "value": normalized["chi2_growth"] - fit["chi2_growth"],
                    "pass": abs(normalized["chi2_growth"] - fit["chi2_growth"])
                    < 0.05,
                    "detail": (
                        "source-normalization sensitivity; primary retains the "
                        "checkpoint-5203 bare-M_R convention"
                    ),
                },
                {
                    "model": fit["model"],
                    "test": "geff_excursion",
                    "value": max(
                        abs(fit["background_diagnostics"]["geff_minimum"] - 1.0),
                        abs(fit["background_diagnostics"]["geff_maximum"] - 1.0),
                    ),
                    "pass": True,
                    "detail": "reported, not used as an independent cut",
                },
            ]
        )
    return tagged(rows)


def zeta_profile_rows(
    fit: dict[str, Any],
    data: checkpoint_5195.JointData,
) -> list[dict[str, Any]]:
    grid = sorted(
        set(
            [
                -3.0e-4,
                -2.0e-4,
                -1.0e-4,
                -5.0e-5,
                0.0,
                5.0e-5,
                1.0e-4,
                2.0e-4,
                3.0e-4,
                float(fit["zeta"]),
            ]
        )
    )
    rows: list[dict[str, Any]] = []
    for zeta in grid:
        score = score_st_model(
            fit["params"],
            zeta,
            data,
            accuracy="fit",
            detail=False,
        )
        rows.append(
            {
                "reference_model": fit["model"],
                "zeta_c": zeta,
                "other_parameters": "fixed_at_signed_joint_optimum",
                "chi2_cosmology": score["chi2_cosmology"],
                "chi2_local": score["chi2_local"],
                "chi2_joint": score["chi2_joint"],
                "delta_chi2_joint": score["chi2_joint"] - fit["chi2_joint"],
                "gamma_minus_one": score["local"]["gamma_minus_one"],
                "Gdot_over_G_yr_inv": score["local"]["Gdot_over_G_yr_inv"],
                "minimum_f": score["background_diagnostics"]["minimum_f"],
            }
        )
    return tagged(rows)


def background_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fit in fits:
        solution = fit["solution"]
        for redshift in (0.0, 0.5, 1.0, 2.0, 10.0, 1100.0):
            n_value = -math.log1p(redshift)
            e_value, h_value, w_value, omega_dark = (
                solution.background.values_at_n(n_value)
            )
            phi_value = float(
                np.interp(
                    n_value,
                    solution.background.n_grid,
                    solution.phi_grid,
                )
            )
            q_value = float(
                np.interp(
                    n_value,
                    solution.background.n_grid,
                    solution.q_grid,
                )
            )
            geff = float(
                np.interp(
                    n_value,
                    solution.background.n_grid,
                    solution.geff_grid,
                )
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
                    "Geff_over_Gbare": geff,
                }
            )
    return tagged(rows)


def provenance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, expected_hash in SOURCE_LOCKS:
        rows.append(
            {
                "source": str(path),
                "sha256": expected_hash,
                "role": (
                    "locked parent action, likelihood, state selection, "
                    "or local-bound predecessor"
                ),
                "exists": path.exists(),
            }
        )
    rows.extend(
        [
            {
                "source": "Cassini Bertotti-Iess-Tortora 2003",
                "sha256": "recorded_by_checkpoint_5204",
                "role": "gamma-1=(2.1+/-2.3)e-5 Gaussian local row",
                "exists": True,
            },
            {
                "source": "LLR Williams-Turyshev-Boggs 2004",
                "sha256": "recorded_by_checkpoint_5204",
                "role": "Gdot/G=(-5.0+/-9.6)e-15 yr^-1 Gaussian local row",
                "exists": True,
            },
        ]
    )
    return tagged(rows)


def clean_fit(fit: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in fit.items()
        if key
        not in {
            "solution",
            "growth_residual_rows",
            "edge_rows",
        }
    }


def build_document(
    symbolic: dict[str, str],
    locked_rows: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    regular_rows: list[dict[str, Any]],
    growth_rows: list[dict[str, Any]],
) -> str:
    fit_lookup = {fit["model"]: fit for fit in fits}
    signed = fit_lookup[SIGNED_SPEC.name]
    positive = fit_lookup[POSITIVE_SPEC.name]
    locked_lookup = {row["model"]: row for row in locked_rows}
    minimal = locked_lookup["ParentScalar_Lambda_zero_minimal_locked"]
    comparison_lookup = {
        (row["model"], row["baseline"]): row for row in comparisons
    }
    signed_vs_minimal = comparison_lookup[
        (SIGNED_SPEC.name, "ParentScalar_Lambda_zero_minimal_locked")
    ]
    signed_vs_lcdm = comparison_lookup[(SIGNED_SPEC.name, "LCDM")]
    signed_vs_cpl = comparison_lookup[(SIGNED_SPEC.name, "CPL")]
    positive_vs_minimal = comparison_lookup[
        (POSITIVE_SPEC.name, "ParentScalar_Lambda_zero_minimal_locked")
    ]
    regular_pass = all(bool(row["pass"]) for row in regular_rows)
    growth_pass = all(bool(row["pass"]) for row in growth_rows)
    signed_local_pass = (
        abs(signed["background_diagnostics"]["gamma_minus_one_0"])
        <= LOCAL_GAMMA_TWO_SIGMA_ENVELOPE
        and abs(signed["background_diagnostics"]["Gdot_over_G_yr_inv"])
        <= LOCAL_GDOT_TWO_SIGMA_ENVELOPE_YR_INV
    )
    selected_route = (
        "DERIVE_COMMON_F_R_V_Z_X2_TRAJECTORY_AND_PRESENT_G_SOURCE_NORMALIZATION"
        if signed_vs_minimal["delta_BIC_joint"] >= 0.0
        else "PROMOTE_TO_FULL_LINEAR_SCALAR_TENSOR_BOLTZMANN_IMPLEMENTATION"
    )
    table_rows = "\n".join(
        (
            f"| `{fit['model']}` | {fit['chi2_cosmology']:.6f} | "
            f"{fit['chi2_local']:.6f} | {fit['chi2_joint']:.6f} | "
            f"{fit['AIC_joint']:.6f} | {fit['BIC_joint']:.6f} | "
            f"{fit['zeta']:.9g} | `{fit['prior_edge_flag']}` |"
        )
        for fit in fits
    )
    baseline_rows = "\n".join(
        (
            f"| `{row['model']}` | {float(row['chi2_cosmology']):.6f} | "
            f"{float(row['chi2_local']):.6f} | "
            f"{float(row['chi2_joint']):.6f} | "
            f"{float(row['AIC_joint']):.6f} | "
            f"{float(row['BIC_joint']):.6f} |"
        )
        for row in locked_rows
    )
    return f"""# 5206 - Constraint-Reduced Zero-Lambda Jordan Scalar-Tensor Refit, Local Gdot and Competitive-Model Gate

Private derivation and empirical robustness checkpoint. This remains an
internal compressed-CMB calculation, not an official cosmology or full-MTS
claim.

Checkpoint marker: `{MARKER}`.

## Executive result

This checkpoint performs the calculation requested by checkpoint 5205 rather
than restating it. The same checkpoint-5203 Jordan action is reduced to

```text
F/M_R^2=1+zeta_c phi^2,
Z=1,
V=M_R^2 m_gap^2 phi^2/2,
Lambda_cal=0.
```

The regular radiation mode is imposed at `N=-18`; its singular partner is
excluded. The sole homogeneous amplitude is then shot until the exact
Hamiltonian constraint gives `E(0)=1`. No scalar fraction or present phase is
fitted. The fitted coordinates are therefore

```text
Omega_m, log10(m_gap/H0), H0, Omega_b h^2, zeta_c,
```

with `n_s` and `sigma8_0` analytically profiled as in checkpoint 5195.

The exact `zeta_c=0` rebuild changes the locked 5195 total cosmology score by
only

```text
{float(minimal['chi2_cosmology']) - 1474.0690807198073:.12g}.
```

That is the compatibility gate: the scalar-tensor implementation reduces
numerically to the already tested minimal parent rather than replacing it
with a new closure.

## 1. Derived FLRW system

With `q=dphi/dN`, `h=d ln H/dN` and `mu=m_gap/H0`, the Hamiltonian equation is

```text
E^2[f+f_N-q^2/6]
 =Omega_m exp(-3N)+Omega_r exp(-4N)+mu^2 phi^2/6.
```

The scalar equation is

```text
q_N=-(3+h)q-mu^2 phi/E^2+6 zeta_c phi(2+h).
```

Eliminating `q_N` from the independent spatial metric equation gives the
closed Raychaudhuri expression recorded in
`source-intake/functional_rg/5206/Jordan_FLRW_equations.csv`. SymPy returns

```text
Raychaudhuri substitution residual = {symbolic['raychaudhuri_residual']},
scalar substitution residual       = {symbolic['scalar_residual']}.
```

The numerical constraint, `d ln E/dN` identity, positive-`F` condition and
Einstein-frame kinetic sign are checked independently.

## 2. State selection is now constraint-reduced

The regular boundary condition is

```text
q_i/phi_i
 =(3/2) zeta_c (Omega_m/Omega_r) a_i
  -mu^2 a_i^4/(5 Omega_r)
  +O(r_i^2,a_i^5).
```

At `N=-18` the explicit remainder bound is below the validation tolerance.
Changing the initial surface to `N=-16` changes the observable background by
less than the recorded start-sensitivity limit. Flatness determines the
initial second moment/amplitude at every likelihood evaluation. Thus the
zero-Lambda parent no longer carries the old fitted `f_scalar` or a fitted
phase.

This is conditional on the declared `Lambda_cal=0` branch. It does not derive
the absolute vacuum-energy origin.

## 3. Physical sound horizon and growth

CAMB supplies standard recombination redshifts and the physical-density
microphysics. The runner then recomputes the sound-horizon integrals using
the scalar-tensor `E(N)` and rescales the CAMB `r_drag` and `r_star`. This
avoids representing the nonminimal background as an invented positive dark
fluid. The small residual approximation is that the recombination redshifts
are held fixed; the maximum pre-recombination `H` shift is reported.

For the five primary `f sigma8` rows the subhorizon equation uses the derived
long-range scalar-tensor coupling

```text
G_eff/G_bare
 =[(2f+4f_phi^2)/(2f+3f_phi^2)]/f.
```

At the lowest observed scale, `k=0.01 h/Mpc`, the omitted Yukawa range
correction is below the machine-recorded `10^-3` gate. A second score
normalizes `G_eff` to its present Cavendish value; its growth-chi-squared
shift is recorded rather than hidden.

## 4. Direct local likelihood

The refitted state predicts both local rows:

```text
gamma-1=-2 alpha_0^2/(1+alpha_0^2),
Gdot/G=H0 q0 d_phi ln G_cav.
```

The runner scores the published Gaussian anchors used by checkpoint 5204:

```text
Cassini gamma-1=(2.1 +/- 2.3)e-5,
LLR Gdot/G=(-5.0 +/- 9.6)e-15 yr^-1.
```

This is stronger and cleaner than imposing a frozen `zeta_c` ceiling from the
old state: every likelihood evaluation recomputes `phi0`, `q0`, `gamma` and
`Gdot`.

## 5. Joint refit

| scalar-tensor model | cosmology chi2 | local chi2 | joint chi2 | joint AIC | joint BIC | zeta_c | edge |
|---|---:|---:|---:|---:|---:|---:|---|
{table_rows}

The signed result has

```text
phi0={signed['background_diagnostics']['phi0']:.10g},
q0={signed['background_diagnostics']['q0']:.10g},
gamma-1={signed['background_diagnostics']['gamma_minus_one_0']:.10g},
Gdot/G={signed['background_diagnostics']['Gdot_over_G_yr_inv']:.10g} yr^-1,
G_cav/G_bare={signed['background_diagnostics']['Gcav_over_Gbare_0']:.10g}.
```

The positive-only branch has `zeta_c={positive['zeta']:.10g}` and differs
from the locked minimal parent by

```text
Delta AIC_joint={float(positive_vs_minimal['delta_AIC_joint']):.9g},
Delta BIC_joint={float(positive_vs_minimal['delta_BIC_joint']):.9g}.
```

An edge-hitting positive-only result is not called evidence for a nonzero
coupling.

## 6. Locked comparators

| model | cosmology chi2 | local chi2 | joint chi2 | joint AIC | joint BIC |
|---|---:|---:|---:|---:|---:|
{baseline_rows}

For the signed scalar-tensor branch:

```text
versus minimal zero-Lambda parent:
  Delta AIC_joint={float(signed_vs_minimal['delta_AIC_joint']):.9g},
  Delta BIC_joint={float(signed_vs_minimal['delta_BIC_joint']):.9g};

versus LCDM:
  Delta AIC_joint={float(signed_vs_lcdm['delta_AIC_joint']):.9g},
  Delta BIC_joint={float(signed_vs_lcdm['delta_BIC_joint']):.9g};

versus CPL:
  Delta AIC_joint={float(signed_vs_cpl['delta_AIC_joint']):.9g},
  Delta BIC_joint={float(signed_vs_cpl['delta_BIC_joint']):.9g}.
```

Negative differences favour the scalar-tensor model; absolute differences
below two are draw-scale. The compressed-CMB caveat remains exactly the same
as checkpoint 5195.

## 7. Decision

```text
full Jordan FLRW equations solved                 = yes;
regular phase derived, not fitted                 = yes;
homogeneous amplitude fixed by flatness           = yes;
finite zeta scored against Cassini and LLR        = yes;
scalar-tensor subhorizon growth inserted          = yes;
physical sound-horizon response inserted          = yes;
regular/numerical validation                      = {str(regular_pass).lower()};
growth approximation validation                   = {str(growth_pass).lower()};
signed local two-sigma envelopes                   = {str(signed_local_pass).lower()};
absolute Lambda_cal=0 origin derived              = no;
common F_R,V,Z,X2 RG trajectory selected          = no;
official CMB likelihood                           = no;
cosmology-support claim                           = false;
full MTS claim                                    = false.
```

Selected next route:

```text
{selected_route}.
```

If the finite coupling is not selected after its parameter penalty, the
result is still constructive: the local-GR corridor and the competitive
minimal cosmology are now connected by one explicitly solved Jordan system,
and the remaining problem is coefficient selection rather than a missing
background equation.

## 8. Evidence products

- `source-intake/functional_rg/5206/Jordan_FLRW_equations.csv`
- `source-intake/functional_rg/5206/regular_shoot_validation.csv`
- `source-intake/functional_rg/5206/locked_comparator_summary.csv`
- `source-intake/functional_rg/5206/scalar_tensor_fit_summary.csv`
- `source-intake/functional_rg/5206/scalar_tensor_fit_parameters.csv`
- `source-intake/functional_rg/5206/local_PPN_Gdot_likelihood.csv`
- `source-intake/functional_rg/5206/growth_effective_G_validation.csv`
- `source-intake/functional_rg/5206/zeta_profile.csv`
- `source-intake/functional_rg/5206/model_comparisons.csv`
- `source-intake/functional_rg/5206/background_samples.csv`
- `source-intake/functional_rg/5206/source_provenance.csv`
- `source-intake/functional_rg/5206/constraint_reduced_scalar_tensor_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5206_VALIDATION.csv`
"""


def validation_rows(
    payload: dict[str, Any],
    output_files: list[str],
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
    add(
        "formal_tree_locked",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "symbolic_Raychaudhuri_residual_zero",
        payload["symbolic"]["raychaudhuri_residual"] == "0",
        payload["symbolic"]["raychaudhuri_residual"],
    )
    add(
        "symbolic_scalar_residual_zero",
        payload["symbolic"]["scalar_residual"] == "0",
        payload["symbolic"]["scalar_residual"],
    )
    add(
        "zeta_zero_reproduces_5195",
        abs(payload["zeta_zero_locked_delta_chi2"]) < 1.0e-4,
        payload["zeta_zero_locked_delta_chi2"],
    )
    for fit in payload["fits"]:
        add(
            f"{fit['model']}::converged",
            bool(fit["convergence"]),
            fit["optimizer_message"],
        )
        add(
            f"{fit['model']}::finite_joint_score",
            math.isfinite(float(fit["chi2_joint"])),
            fit["chi2_joint"],
        )
        add(
            f"{fit['model']}::positive_F",
            float(fit["background_diagnostics"]["minimum_f"]) > 0.0,
            fit["background_diagnostics"]["minimum_f"],
        )
        add(
            f"{fit['model']}::positive_Einstein_kinetic",
            float(fit["background_diagnostics"]["minimum_Einstein_kinetic"])
            > 0.0,
            fit["background_diagnostics"]["minimum_Einstein_kinetic"],
        )
        add(
            f"{fit['model']}::Hamiltonian_constraint",
            abs(
                float(
                    fit["background_diagnostics"]["maximum_constraint_residual"]
                )
            )
            < 1.0e-9,
            fit["background_diagnostics"]["maximum_constraint_residual"],
        )
        add(
            f"{fit['model']}::local_rows_directly_scored",
            math.isfinite(float(fit["chi2_Cassini"]))
            and math.isfinite(float(fit["chi2_LLR_Gdot"])),
            f"{fit['chi2_Cassini']},{fit['chi2_LLR_Gdot']}",
        )
        add(
            f"{fit['model']}::profiled_nuisances_interior",
            not bool(fit["n_s_edge_flag"])
            and not bool(fit["sigma8_edge_flag"]),
            f"ns={fit['n_s_profiled']};sigma8={fit['sigma8_0_profiled']}",
        )
        add(
            f"{fit['model']}::parameter_count",
            int(fit["k"]) == 8,
            f"k={fit['k']}=5 optimized+3 profiled",
        )
    add(
        "regular_validation_all_pass",
        all(bool(row["pass"]) for row in payload["regular_validation"]),
        len(payload["regular_validation"]),
    )
    add(
        "growth_validation_all_pass",
        all(bool(row["pass"]) for row in payload["growth_validation"]),
        len(payload["growth_validation"]),
    )
    add(
        "comparisons_complete",
        len(payload["model_comparisons"]) == 8,
        len(payload["model_comparisons"]),
    )
    add(
        "claim_status_false",
        not payload["claim_status"]["cosmology_support"]
        and not payload["claim_status"]["full_MTS"],
        payload["claim_status"],
    )
    add(
        "absolute_zero_Lambda_not_overclaimed",
        not payload["claim_status"]["absolute_zero_Lambda_origin_derived"],
        payload["claim_status"],
    )
    add(
        "official_CMB_not_overclaimed",
        not payload["claim_status"]["official_CMB_likelihood"],
        payload["claim_status"],
    )
    add(
        "GitHub_action_false",
        not payload["claim_status"]["GitHub_action"],
        payload["claim_status"],
    )
    for name in output_files:
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
    symbolic_rows, symbolic = symbolic_equation_rows()
    if symbolic["raychaudhuri_residual"] != "0":
        raise RuntimeError("Raychaudhuri symbolic residual is nonzero")
    if symbolic["scalar_residual"] != "0":
        raise RuntimeError("scalar symbolic residual is nonzero")
    data = checkpoint_5195.load_joint_data()
    locked = locked_primary_fits()["ParentScalar_Lambda_zero"]
    params = {key: float(value) for key, value in locked["params"].items()}
    score = score_st_model(
        params,
        0.0,
        data,
        accuracy="exact",
        detail=False,
    )
    delta = score["chi2_cosmology"] - float(locked["chi2_total"])
    if abs(delta) >= 1.0e-4:
        raise RuntimeError(f"zeta=0 compatibility failed: {delta}")
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "symbolic_rows": len(symbolic_rows),
                "zeta_zero_delta_chi2": delta,
                "data_rows": PRIMARY_N_COSMOLOGY,
                "formal_tree": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def run_checkpoint() -> None:
    assert_source_locks()
    if tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed before checkpoint 5206")
    symbolic_rows, symbolic = symbolic_equation_rows()
    data = checkpoint_5195.load_joint_data()
    locked_fits = locked_primary_fits()
    locked_minimal = locked_fits["ParentScalar_Lambda_zero"]
    locked_params = {
        key: float(value)
        for key, value in locked_minimal["params"].items()
    }
    minimal_score = score_st_model(
        locked_params,
        0.0,
        data,
        accuracy="exact",
        detail=True,
    )
    zeta_zero_delta = (
        minimal_score["chi2_cosmology"] - float(locked_minimal["chi2_total"])
    )
    if abs(zeta_zero_delta) >= 1.0e-4:
        raise RuntimeError(
            f"zeta=0 compatibility failed before fitting: {zeta_zero_delta}"
        )
    signed_fit = fit_st_model(SIGNED_SPEC, data, locked_minimal)
    positive_fit = fit_st_model(POSITIVE_SPEC, data, locked_minimal)
    fits = [signed_fit, positive_fit]
    locked_rows = locked_model_rows(locked_fits, minimal_score)
    fit_summary = st_fit_summary_rows(fits)
    fit_parameters = parameter_rows(fits)
    local_likelihood = local_rows(fits, minimal_score)
    comparisons = comparison_rows(locked_rows, fits)
    regular_validation = regular_validation_rows(
        fits,
        minimal_score,
        locked_minimal,
    )
    growth_validation = growth_validation_rows(fits, data)
    zeta_profile = zeta_profile_rows(signed_fit, data)
    samples = background_rows(fits)
    provenance = provenance_rows()
    output_payloads: dict[str, list[dict[str, Any]]] = {
        "Jordan_FLRW_equations.csv": symbolic_rows,
        "regular_shoot_validation.csv": regular_validation,
        "locked_comparator_summary.csv": locked_rows,
        "scalar_tensor_fit_summary.csv": fit_summary,
        "scalar_tensor_fit_parameters.csv": fit_parameters,
        "local_PPN_Gdot_likelihood.csv": local_likelihood,
        "growth_effective_G_validation.csv": growth_validation,
        "zeta_profile.csv": zeta_profile,
        "model_comparisons.csv": comparisons,
        "background_samples.csv": samples,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in output_payloads.items():
        write_csv(OUT / name, rows)
    document_text = build_document(
        symbolic,
        locked_rows,
        fits,
        comparisons,
        regular_validation,
        growth_validation,
    )
    DOCUMENT.write_text(document_text, encoding="utf-8")
    comparison_clean = [
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
    regular_clean = [
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
        for row in regular_validation
    ]
    growth_clean = [
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
        for row in growth_validation
    ]
    result_payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "symbolic": symbolic,
        "zeta_zero_locked_delta_chi2": zeta_zero_delta,
        "fits": [clean_fit(fit) for fit in fits],
        "locked_comparators": [
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
            for row in locked_rows
        ],
        "model_comparisons": comparison_clean,
        "regular_validation": regular_clean,
        "growth_validation": growth_clean,
        "claim_status": {
            "Jordan_FLRW_equations_derived": True,
            "regular_phase_derived": True,
            "homogeneous_amplitude_fixed_by_flatness": True,
            "finite_zeta_locally_scored": True,
            "scalar_tensor_growth_scored": True,
            "physical_sound_horizon_response_scored": True,
            "absolute_zero_Lambda_origin_derived": False,
            "common_F_R_V_Z_X2_trajectory_selected": False,
            "official_CMB_likelihood": False,
            "cosmology_support": False,
            "full_MTS": False,
            "GitHub_action": False,
        },
        "selected_next_route": (
            "DERIVE_COMMON_F_R_V_Z_X2_TRAJECTORY_AND_PRESENT_G_SOURCE_NORMALIZATION"
            if next(
                row
                for row in comparison_clean
                if row["model"] == SIGNED_SPEC.name
                and row["baseline"]
                == "ParentScalar_Lambda_zero_minimal_locked"
            )["delta_BIC_joint"]
            >= 0.0
            else "PROMOTE_TO_FULL_LINEAR_SCALAR_TENSOR_BOLTZMANN_IMPLEMENTATION"
        ),
        "official_CMB_likelihood": False,
    }
    result_name = "constraint_reduced_scalar_tensor_results.json"
    write_json(OUT / result_name, result_payload)
    output_names = [*output_payloads, result_name]
    validation = validation_rows(result_payload, output_names)
    write_csv(VALIDATION, validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5206 validation failed: "
            + json.dumps(failed, indent=2, allow_nan=False)
        )
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
        raise RuntimeError(
            "checkpoint 5206 final validation failed: "
            + json.dumps(failed, indent=2, allow_nan=False)
        )
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "signed_zeta": signed_fit["zeta"],
                "signed_chi2_joint": signed_fit["chi2_joint"],
                "positive_zeta": positive_fit["zeta"],
                "positive_chi2_joint": positive_fit["chi2_joint"],
                "zeta_zero_delta_chi2": zeta_zero_delta,
                "selected_next_route": result_payload["selected_next_route"],
                "output_tree_sha256": tree_digest(OUT),
                "formal_tree_sha256": tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    result_path = OUT / "constraint_reduced_scalar_tensor_results.json"
    if not result_path.exists():
        raise FileNotFoundError(result_path)
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    output_names = [
        "Jordan_FLRW_equations.csv",
        "regular_shoot_validation.csv",
        "locked_comparator_summary.csv",
        "scalar_tensor_fit_summary.csv",
        "scalar_tensor_fit_parameters.csv",
        "local_PPN_Gdot_likelihood.csv",
        "growth_effective_G_validation.csv",
        "zeta_profile.csv",
        "model_comparisons.csv",
        "background_samples.csv",
        "source_provenance.csv",
        "constraint_reduced_scalar_tensor_results.json",
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
