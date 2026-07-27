from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Callable

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares


sys.dont_write_bytecode = True
getcontext().prec = 80

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5192"
DOCUMENT = (
    POST
    / "5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-"
    "mass-gap-cosmology-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5192_VALIDATION.csv"
)

MARKER = "MTS_5192_PARENT_MOTION_FLRW_BRANCH_MEMORY_SEPARATION"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176 = POST / "source-intake" / "functional_rg" / "5176"

LOCAL_SOURCES: dict[str, str] = {
    "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md":
        "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md":
        "2cf1f25d7cf67ec9bb724381919a9ff6e78d5dabe355ec50178157309b29cce5",
    "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md":
        "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    "4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md":
        "9da47eb0232980ca743c50617645c0d02cfaaeca58793a0d244bc9450418fa9e",
    "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md":
        "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    "source-intake/functional_rg/4957/functional_PX_O4_GR_trajectory_results.json":
        "8d8c7e416706d116492e3539a0541e6e64174c59a460714325251656b1477cc6",
    "source-intake/functional_rg/4957/functional_PX_O4_GR_trajectory.csv":
        "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    "5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-Hessian-gate.md":
        "e4a3427963b4de0b5b40baab67b905e9e7054e8033c72dee768fb8973a258e33",
    "source-intake/functional_rg/5184/stationary_PX_background_results.json":
        "203549387a9c8f22721dfe8925c91aa2614a2adbcb3281f487cefb89d849e63b",
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md":
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674",
    "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-local-tensor-protection-theorem.md":
        "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266",
    "source-intake/functional_rg/5189/motion_ADM_projection_results.json":
        "6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2",
    "5191-Y5-R2FR-O4-FLRW-tensor-nondegeneracy-order-reduction-and-cosmological-safety-theorem.md":
        "4568e2ac3fe467b2fa1e2c294058692a0c62994e53e703405b2b18864742b6fa",
    "source-intake/functional_rg/5191/O4_FLRW_tensor_order_reduction_results.json":
        "e8c3d48469a0e47a5629d30dd43992e1193f20f064f6c582db496514ac08712d",
    "90-cosmo-model-selection-stability-ledger.md":
        "2527dc8fbc4780b806f90b38783822d1634a8ba1fe06a54c097be09333ca2708",
    "91-Bmem-p-u3-parent-ownership-gate.md":
        "bdbeab2c0dc5a1be216ea203c1cb991c0db850be04b1bb40c7f86cb22442fdb0",
    "scripts/cosmo_SN_BAO_closure_runner.py":
        "3ce577f284978b92a16466102cc2672011a8afb4bd54a1b0e7581ec16cc49b26",
}

OMEGA_M = 0.3
OMEGA_R = 9.0e-5
B_MEMORY = 2.0 / 27.0
N_INITIAL = -5.0
N_PAST_MAX = 2.0
P_CLOSURE = 3.0
U_CLOSURE = 0.25
W_O4_ABS_MAX = 3.3225249561681114
H0_KM_S_MPC = 70.0
MPC_METRES = 3.0856775814913673e22
PLANCK_TIME_SECONDS = 5.391247e-44
HBAR_EV_SECONDS = 6.582119569e-16


def source_path(relative: str) -> Path:
    return POST / Path(relative)


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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "valid_for_cosmology_support_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def load_trajectory_rows() -> list[dict[str, str]]:
    path = source_path(
        "source-intake/functional_rg/4957/functional_PX_O4_GR_trajectory.csv"
    )
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def endpoint_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    endpoints: dict[str, dict[str, str]] = {}
    for scheme in ("dynamic_etaN", "reference_etaN0"):
        selected = [
            row
            for row in rows
            if row["scheme"] == scheme and row["polynomial_order"] == "8"
        ]
        if not selected:
            raise RuntimeError(f"missing N=8 trajectory for {scheme}")
        endpoints[scheme] = selected[-1]
    return endpoints


def decimal_polynomial_metrics(
    coefficients: list[Decimal], x_value: Decimal
) -> dict[str, Any]:
    def power(exponent: int) -> Decimal:
        return Decimal(1) if exponent == 0 else x_value**exponent

    p_value = sum(
        coefficient * power(index)
        for index, coefficient in enumerate(coefficients)
    )
    p_x = sum(
        Decimal(index) * coefficients[index] * power(index - 1)
        for index in range(1, len(coefficients))
    )
    p_xx = sum(
        Decimal(index * (index - 1))
        * coefficients[index]
        * power(index - 2)
        for index in range(2, len(coefficients))
    )
    kinetic = p_x + Decimal(2) * x_value * p_xx
    density = p_value - Decimal(2) * x_value * p_x
    pressure = -p_value
    if density:
        equation_of_state = pressure / density
    else:
        equation_of_state = "UNDEFINED_ZERO_DENSITY_VACUUM_ORIGIN"
    if kinetic:
        sound_speed_squared = p_x / kinetic
    else:
        sound_speed_squared = Decimal("NaN")
    return {
        "P_over_k4": p_value,
        "P_X_dimensionless": p_x,
        "kinetic_principal": kinetic,
        "rho_over_k4": density,
        "pressure_over_k4": pressure,
        "w": equation_of_state,
        "c_s_squared": sound_speed_squared,
    }


def functional_germ_rows(
    endpoints: dict[str, dict[str, str]]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, str]] = {}
    x_values = (
        Decimal("-0.1"),
        Decimal("-0.05"),
        Decimal("-0.01"),
        Decimal("-0.001"),
        Decimal("-0.000001"),
        Decimal("0"),
    )
    for scheme, endpoint in endpoints.items():
        coefficients = [Decimal("0"), Decimal("0.5")] + [
            Decimal(endpoint[f"a{index}"]) for index in range(2, 9)
        ]
        finite_metrics: list[dict[str, Decimal]] = []
        for x_value in x_values:
            metrics = decimal_polynomial_metrics(coefficients, x_value)
            if x_value:
                finite_metrics.append(metrics)
            rows.append(
                {
                    "scheme": scheme,
                    "g": endpoint["g"],
                    "x": str(x_value),
                    **{
                        key: str(value)
                        for key, value in metrics.items()
                    },
                    "status": (
                        "TIMELIKE_LOCAL_ANALYTIC_CONTINUATION_DIAGNOSTIC"
                        if x_value < 0
                        else "CANONICAL_ORIGIN"
                    ),
                    "claim_boundary": (
                        "Euclidean FRG germ analytically continued locally; "
                        "not a global Lorentzian fixed-function theorem"
                    ),
                }
            )
        min_px = min(item["P_X_dimensionless"] for item in finite_metrics)
        min_kinetic = min(item["kinetic_principal"] for item in finite_metrics)
        max_w_deviation = max(
            abs(item["w"] - Decimal(1)) for item in finite_metrics
        )
        max_cs_deviation = max(
            abs(item["c_s_squared"] - Decimal(1)) for item in finite_metrics
        )
        summaries[scheme] = {
            "minimum_P_X": str(min_px),
            "minimum_kinetic_principal": str(min_kinetic),
            "maximum_abs_w_minus_1": str(max_w_deviation),
            "maximum_abs_cs2_minus_1": str(max_cs_deviation),
        }
    return tagged(rows), summaries


def symbolic_contract() -> dict[str, Any]:
    x = sp.symbols("x", nonzero=True)
    p_function = sp.Function("P")
    p_value = p_function(x)
    p_x = sp.diff(p_value, x)
    p_xx = sp.diff(p_value, x, 2)
    density = p_value - 2 * x * p_x
    pressure = -p_value
    sound_speed_squared = p_x / (p_x + 2 * x * p_xx)
    d_x_d_lna = -6 * x * sound_speed_squared
    continuity_residual = sp.simplify(
        sp.diff(density, x) * d_x_d_lna + 3 * (density + pressure)
    )

    n, u, b = sp.symbols("n u b", positive=True)
    closure = 1 - sp.exp(-((n / u) ** 3))
    closure_prime = sp.diff(closure, n)
    memory_density = b * closure
    enthalpy = sp.simplify(sp.diff(memory_density, n) / 3)
    reconstructed_p = sp.simplify(memory_density - sp.diff(memory_density, n) / 3)
    x_times_q2 = sp.simplify(
        -sp.exp(-6 * n) * enthalpy**2 / 4
    )
    q, q_dot, hubble, hubble_dot, mass = sp.symbols(
        "q q_dot H H_dot m"
    )
    q_ddot = -3 * hubble_dot * q - 3 * hubble * q_dot - mass**2 * q
    o4_direct_shape = q_dot**2 + q * q_ddot + hubble * q * q_dot
    o4_reduced_shape = (
        q_dot**2
        - 3 * hubble_dot * q**2
        - 2 * hubble * q * q_dot
        - mass**2 * q**2
    )
    return {
        "rho": str(density),
        "pressure": str(pressure),
        "c_s_squared": str(sound_speed_squared),
        "dX_dln_a": str(d_x_d_lna),
        "continuity_residual": str(continuity_residual),
        "F_zero": str(sp.simplify(closure.subs(n, 0))),
        "Fprime_zero": str(sp.simplify(closure_prime.subs(n, 0))),
        "F_infinity": str(sp.limit(closure, n, sp.oo)),
        "enthalpy_zero": str(sp.simplify(enthalpy.subs(n, 0))),
        "P_reconstructed_zero": str(sp.simplify(reconstructed_p.subs(n, 0))),
        "P_reconstructed_infinity": str(sp.limit(reconstructed_p, n, sp.oo)),
        "X_times_Q2_zero": str(sp.simplify(x_times_q2.subs(n, 0))),
        "X_times_Q2_infinity": str(sp.limit(x_times_q2, n, sp.oo)),
        "O4_massive_KG_reduction_residual": str(
            sp.simplify(o4_direct_shape - o4_reduced_shape)
        ),
    }


def memory_no_go_rows(symbolic: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "step": "NG5192_00",
            "statement": "M6 closure shape",
            "equation": "F(n)=1-exp[-(n/u)^3], rho_mem=B_mem F(n)",
            "result": "F(0)=0, F'(0)=0, F(infinity)=1",
            "status": "DERIVED",
        },
        {
            "step": "NG5192_01",
            "statement": "conserved-fluid enthalpy",
            "equation": "rho+p=(1/3)d rho/dn",
            "result": "rho+p=0 at n=0",
            "status": "DERIVED",
        },
        {
            "step": "NG5192_02",
            "statement": "healthy analytic P(X) implication",
            "equation": "rho+p=-2 X P_X; P_X(0)=1/2 and P_X>0",
            "result": "X(0)=0",
            "status": "DERIVED",
        },
        {
            "step": "NG5192_03",
            "statement": "shift-current implication",
            "equation": "Q=a^3 P_X sqrt(-X)=constant",
            "result": "Q=0 at n=0; connected healthy branch has X=0 for all n",
            "status": "DERIVED",
        },
        {
            "step": "NG5192_04",
            "statement": "contradiction",
            "equation": "X=0 implies rho_mem=constant while B_mem F varies",
            "result": "nonzero M6 memory is not the source-free analytic P(X) clock",
            "status": "EXACT_NO_GO",
        },
        {
            "step": "NG5192_05",
            "statement": "parametric reconstruction cross-check",
            "equation": "X Q^2=-a^6(rho+p)^2/4; P=-p=rho-rho_n/3",
            "result": (
                "X->0 at both endpoints but P->0 and P->B_mem; "
                "single-valued P(X) fails for B_mem!=0"
            ),
            "status": "EXACT_NO_GO",
        },
        {
            "step": "NG5192_06",
            "statement": "allowed escapes",
            "equation": "source/exchange current, extra field, singular P_X, or disconnected phase",
            "result": (
                "first two require new parent dynamics; singular/degenerate "
                "escapes are outside the 4957/5184 healthy germ"
            ),
            "status": "NOT_ASSUMED",
        },
    ]
    for row in rows:
        row["symbolic_contract"] = json.dumps(symbolic, sort_keys=True)
    return tagged(rows)


def closure_shape(n_past: np.ndarray, p_value: float, u_value: float) -> np.ndarray:
    return 1.0 - np.exp(-((n_past / u_value) ** p_value))


def scalar_auxiliary(
    n_lna: float,
    state: np.ndarray,
    mu: float,
    omega_lambda: float,
) -> tuple[float, float, float]:
    chi, chi_prime = float(state[0]), float(state[1])
    denominator = 1.0 - chi_prime**2
    base = (
        OMEGA_M * math.exp(-3.0 * n_lna)
        + OMEGA_R * math.exp(-4.0 * n_lna)
        + omega_lambda
        + mu**2 * chi**2
    )
    if denominator <= 1.0e-10 or base <= 0.0:
        raise ValueError("non-positive scalar FLRW algebraic branch")
    e_squared = base / denominator
    hdot_h0_squared = (
        -1.5 * OMEGA_M * math.exp(-3.0 * n_lna)
        - 2.0 * OMEGA_R * math.exp(-4.0 * n_lna)
        - 3.0 * e_squared * chi_prime**2
    )
    dln_h_dln_a = hdot_h0_squared / e_squared
    return e_squared, dln_h_dln_a, hdot_h0_squared


def integrate_scalar(
    mu: float,
    chi_initial: float,
    omega_lambda: float,
    dense_output: bool = False,
    n_initial: float = N_INITIAL,
) -> tuple[Any, float, float, float]:
    def rhs(n_lna: float, state: np.ndarray) -> np.ndarray:
        e_squared, dln_h, _ = scalar_auxiliary(
            n_lna, state, mu, omega_lambda
        )
        return np.array(
            [
                state[1],
                -(3.0 + dln_h) * state[1] - mu**2 * state[0] / e_squared,
            ],
            dtype=float,
        )

    solution = solve_ivp(
        rhs,
        (n_initial, 0.0),
        np.array([chi_initial, 0.0], dtype=float),
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.02,
        dense_output=dense_output,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    chi_zero, derivative_zero = solution.y[:, -1]
    e_squared_zero, _, _ = scalar_auxiliary(
        0.0,
        np.array([chi_zero, derivative_zero]),
        mu,
        omega_lambda,
    )
    omega_scalar_zero = (
        e_squared_zero * derivative_zero**2 + mu**2 * chi_zero**2
    )
    omega_scalar_initial = mu**2 * chi_initial**2
    return (
        solution,
        float(e_squared_zero),
        float(omega_scalar_zero),
        float(omega_scalar_initial),
    )


def solve_fixed_step(
    mu: float,
    target_step: float,
    initial_guess: np.ndarray | None = None,
) -> tuple[dict[str, Any] | None, np.ndarray]:
    if initial_guess is None:
        initial_guess = np.array(
            [math.log(max(math.sqrt(target_step) / max(mu, 0.1), 1.0e-4)), 0.5]
        )

    def residual(parameters: np.ndarray) -> np.ndarray:
        chi_initial = math.exp(float(parameters[0]))
        omega_lambda = float(parameters[1])
        try:
            _, e_squared_zero, omega_zero, omega_initial = integrate_scalar(
                mu, chi_initial, omega_lambda
            )
        except (RuntimeError, ValueError, FloatingPointError):
            return np.array([10.0, 10.0])
        return np.array(
            [
                e_squared_zero - 1.0,
                omega_initial - omega_zero - target_step,
            ]
        )

    fit = least_squares(
        residual,
        initial_guess,
        bounds=(
            np.array([math.log(1.0e-8), 0.0]),
            np.array([math.log(1.0e4), 1.0]),
        ),
        xtol=1.0e-11,
        ftol=1.0e-11,
        gtol=1.0e-11,
        max_nfev=100,
    )
    errors = residual(fit.x)
    if np.max(np.abs(errors)) > 2.0e-7:
        return None, fit.x
    chi_initial = math.exp(float(fit.x[0]))
    omega_lambda = float(fit.x[1])
    solution, e_zero, omega_zero, omega_initial = integrate_scalar(
        mu, chi_initial, omega_lambda, dense_output=True
    )
    return (
        {
            "mu": mu,
            "chi_initial": chi_initial,
            "omega_lambda": omega_lambda,
            "solution": solution,
            "E0_squared": e_zero,
            "omega_scalar_zero": omega_zero,
            "omega_scalar_initial": omega_initial,
            "step": omega_initial - omega_zero,
            "residual_infinity": float(np.max(np.abs(errors))),
        },
        fit.x,
    )


def solve_zero_lambda_boundary(
    target_step: float,
    n_initial: float = N_INITIAL,
) -> dict[str, Any]:
    def residual(log_parameters: np.ndarray) -> np.ndarray:
        mu, chi_initial = np.exp(log_parameters)
        try:
            _, e_zero, omega_zero, omega_initial = integrate_scalar(
                float(mu),
                float(chi_initial),
                0.0,
                n_initial=n_initial,
            )
        except (RuntimeError, ValueError, FloatingPointError):
            return np.array([10.0, 10.0])
        return np.array(
            [
                e_zero - 1.0,
                omega_initial - omega_zero - target_step,
            ]
        )

    fit = least_squares(
        residual,
        np.log(np.array([0.7, 1.25])),
        xtol=1.0e-12,
        ftol=1.0e-12,
        gtol=1.0e-12,
        max_nfev=120,
    )
    mu, chi_initial = np.exp(fit.x)
    solution, e_zero, omega_zero, omega_initial = integrate_scalar(
        float(mu),
        float(chi_initial),
        0.0,
        dense_output=True,
        n_initial=n_initial,
    )
    return {
        "mu": float(mu),
        "N_initial": n_initial,
        "chi_initial": float(chi_initial),
        "omega_lambda": 0.0,
        "solution": solution,
        "E0_squared": e_zero,
        "omega_scalar_zero": omega_zero,
        "omega_scalar_initial": omega_initial,
        "step": omega_initial - omega_zero,
        "residual_infinity": float(np.max(np.abs(residual(fit.x)))),
    }


def evaluate_scalar_shape(
    branch: dict[str, Any],
    n_past: np.ndarray,
) -> dict[str, Any]:
    n_lna = -n_past
    states = branch["solution"].sol(n_lna)
    omega_values: list[float] = []
    e_values: list[float] = []
    hdot_values: list[float] = []
    delta_q_coefficients: list[float] = []
    delta_f_coefficients: list[float] = []
    for n_value, chi, derivative in zip(
        n_lna, states[0], states[1], strict=True
    ):
        e_squared, _, hdot_h0_squared = scalar_auxiliary(
            float(n_value),
            np.array([chi, derivative]),
            branch["mu"],
            branch["omega_lambda"],
        )
        omega_scalar = (
            e_squared * derivative**2 + branch["mu"] ** 2 * chi**2
        )
        acceleration = (
            -3.0 * e_squared * derivative - branch["mu"] ** 2 * chi
        )
        derivative_shape = (
            acceleration**2
            - 3.0 * hdot_h0_squared * e_squared * derivative**2
            - 2.0 * e_squared * derivative * acceleration
            - branch["mu"] ** 2 * e_squared * derivative**2
        )
        delta_q_coefficients.append(
            -96.0 * W_O4_ABS_MAX * e_squared**2 * derivative**2
        )
        delta_f_coefficients.append(
            -96.0 * W_O4_ABS_MAX * derivative_shape
        )
        omega_values.append(float(omega_scalar))
        e_values.append(math.sqrt(e_squared))
        hdot_values.append(float(hdot_h0_squared))
    omega_array = np.asarray(omega_values)
    normalized_shape = (
        omega_array - branch["omega_scalar_zero"]
    ) / branch["step"]
    target_shape = closure_shape(n_past, P_CLOSURE, U_CLOSURE)
    return {
        "n_past": n_past,
        "chi": states[0],
        "chi_prime": states[1],
        "E": np.asarray(e_values),
        "Hdot_over_H0_squared": np.asarray(hdot_values),
        "omega_scalar": omega_array,
        "shape": normalized_shape,
        "target": target_shape,
        "rms_vs_fixed_closure": float(
            np.sqrt(np.mean((normalized_shape - target_shape) ** 2))
        ),
        "max_abs_vs_fixed_closure": float(
            np.max(np.abs(normalized_shape - target_shape))
        ),
        "delta_Q_over_H0tP_fourth": np.asarray(delta_q_coefficients),
        "delta_F_over_H0tP_fourth": np.asarray(delta_f_coefficients),
    }


def fit_stretched_exponential(
    n_past: np.ndarray,
    shape: np.ndarray,
) -> dict[str, float]:
    mask = n_past <= 1.5

    def residual(log_parameters: np.ndarray) -> np.ndarray:
        p_value, u_value = np.exp(log_parameters)
        return (
            closure_shape(n_past[mask], float(p_value), float(u_value))
            - shape[mask]
        )

    fit = least_squares(
        residual,
        np.log(np.array([1.0, 0.4])),
        bounds=(
            np.log(np.array([0.2, 0.02])),
            np.log(np.array([10.0, 3.0])),
        ),
        xtol=1.0e-12,
        ftol=1.0e-12,
        gtol=1.0e-12,
    )
    p_value, u_value = np.exp(fit.x)
    return {
        "p_effective": float(p_value),
        "u_effective": float(u_value),
        "rms": float(np.sqrt(np.mean(fit.fun**2))),
    }


def scalar_scan() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    n_past = np.linspace(0.0, N_PAST_MAX, 201)
    scan_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    tensor_rows: list[dict[str, Any]] = []
    guess: np.ndarray | None = None
    successful: list[tuple[dict[str, Any], dict[str, Any]]] = []
    mu_grid = sorted(
        set(
            np.geomspace(0.55, 10.0, 32).tolist()
            + [
                math.sqrt(
                    OMEGA_M * math.exp(3.0 * U_CLOSURE)
                    + OMEGA_R * math.exp(4.0 * U_CLOSURE)
                    + 1.0
                    - OMEGA_M
                    - OMEGA_R
                ),
                3.0
                * math.sqrt(
                    OMEGA_M * math.exp(3.0 * U_CLOSURE)
                    + OMEGA_R * math.exp(4.0 * U_CLOSURE)
                    + 1.0
                    - OMEGA_M
                    - OMEGA_R
                ),
            ]
        )
    )
    for mu in mu_grid:
        branch, guess = solve_fixed_step(mu, B_MEMORY, guess)
        if branch is None:
            scan_rows.append(
                {
                    "branch": "quadratic_1PI_fixed_step",
                    "mu_m_over_H0": mu,
                    "target_B_mem": B_MEMORY,
                    "status": "NO_NONNEGATIVE_LAMBDA_FLAT_SOLUTION",
                }
            )
            continue
        evaluated = evaluate_scalar_shape(branch, n_past)
        successful.append((branch, evaluated))
        scan_rows.append(
            {
                "branch": "quadratic_1PI_fixed_step",
                "mu_m_over_H0": mu,
                "target_B_mem": B_MEMORY,
                "J_gap_for_H0_70": (
                    mu * (H0_KM_S_MPC * 1000.0 / MPC_METRES)
                    * PLANCK_TIME_SECONDS
                )
                ** 2,
                "mass_eV_for_H0_70": (
                    mu
                    * (H0_KM_S_MPC * 1000.0 / MPC_METRES)
                    * HBAR_EV_SECONDS
                ),
                "chi_initial": branch["chi_initial"],
                "omega_lambda": branch["omega_lambda"],
                "omega_scalar_zero": branch["omega_scalar_zero"],
                "omega_scalar_initial": branch["omega_scalar_initial"],
                "step": branch["step"],
                "flat_step_residual_infinity": branch["residual_infinity"],
                "rms_vs_fixed_p3_u3quarter": evaluated[
                    "rms_vs_fixed_closure"
                ],
                "max_abs_vs_fixed_p3_u3quarter": evaluated[
                    "max_abs_vs_fixed_closure"
                ],
                "status": "PHYSICAL_NONNEGATIVE_LAMBDA_SOLUTION",
            }
        )

    boundary = solve_zero_lambda_boundary(B_MEMORY)
    boundary_evaluated = evaluate_scalar_shape(boundary, n_past)
    start_sensitivity_pairs = [(boundary, boundary_evaluated)]
    for n_initial in (-6.0, -7.0):
        sensitivity_branch = solve_zero_lambda_boundary(
            B_MEMORY,
            n_initial=n_initial,
        )
        start_sensitivity_pairs.append(
            (
                sensitivity_branch,
                evaluate_scalar_shape(sensitivity_branch, n_past),
            )
        )
    start_sensitivity_rows = [
        {
            "N_initial": candidate["N_initial"],
            "mu": candidate["mu"],
            "chi_initial": candidate["chi_initial"],
            "omega_scalar_initial": candidate["omega_scalar_initial"],
            "omega_scalar_zero": candidate["omega_scalar_zero"],
            "step": candidate["step"],
            "residual_infinity": candidate["residual_infinity"],
            "delta_mu_from_N_minus_5": candidate["mu"] - boundary["mu"],
            "shape_rms_from_N_minus_5": float(
                np.sqrt(
                    np.mean(
                        (
                            candidate_evaluated["shape"]
                            - boundary_evaluated["shape"]
                        )
                        ** 2
                    )
                )
            ),
        }
        for candidate, candidate_evaluated in start_sensitivity_pairs
    ]
    effective_fit = fit_stretched_exponential(
        n_past, boundary_evaluated["shape"]
    )
    best_branch, best_evaluated = min(
        successful + [(boundary, boundary_evaluated)],
        key=lambda item: item[1]["rms_vs_fixed_closure"],
    )

    selected_indices = sorted(
        set(
            [
                0,
                *(
                    int(index)
                    for index in np.linspace(0, len(n_past) - 1, 41)
                ),
            ]
        )
    )
    for index in selected_indices:
        comparison_rows.append(
            {
                "branch": "zero_Lambda_boundary_parent_scalar",
                "n_past": float(n_past[index]),
                "redshift": float(math.exp(n_past[index]) - 1.0),
                "parent_scalar_shape": float(
                    boundary_evaluated["shape"][index]
                ),
                "fixed_p3_u3quarter_shape": float(
                    boundary_evaluated["target"][index]
                ),
                "residual": float(
                    boundary_evaluated["shape"][index]
                    - boundary_evaluated["target"][index]
                ),
                "omega_scalar": float(
                    boundary_evaluated["omega_scalar"][index]
                ),
                "E": float(boundary_evaluated["E"][index]),
                "chi": float(boundary_evaluated["chi"][index]),
                "dchi_dln_a": float(
                    boundary_evaluated["chi_prime"][index]
                ),
                "status": "DIRECT_PARENT_SCALAR_ODE_NOT_CLOSURE_FIT",
            }
        )
        tensor_rows.append(
            {
                "branch": "zero_Lambda_boundary_parent_scalar",
                "n_past": float(n_past[index]),
                "redshift": float(math.exp(n_past[index]) - 1.0),
                "delta_Q_over_H0tP_fourth": float(
                    boundary_evaluated[
                        "delta_Q_over_H0tP_fourth"
                    ][index]
                ),
                "delta_F_over_H0tP_fourth": float(
                    boundary_evaluated[
                        "delta_F_over_H0tP_fourth"
                    ][index]
                ),
                "delta_Q_H0_70": float(
                    boundary_evaluated[
                        "delta_Q_over_H0tP_fourth"
                    ][index]
                    * (
                        H0_KM_S_MPC
                        * 1000.0
                        / MPC_METRES
                        * PLANCK_TIME_SECONDS
                    )
                    ** 4
                ),
                "delta_F_H0_70": float(
                    boundary_evaluated[
                        "delta_F_over_H0tP_fourth"
                    ][index]
                    * (
                        H0_KM_S_MPC
                        * 1000.0
                        / MPC_METRES
                        * PLANCK_TIME_SECONDS
                    )
                    ** 4
                ),
                "status": "ORDER_REDUCED_O4_PARENT_SCALAR_PREDICTION",
            }
        )

    summary = {
        "target_memory_amplitude": B_MEMORY,
        "closure_p": P_CLOSURE,
        "closure_u": U_CLOSURE,
        "successful_nonnegative_lambda_scan_rows": len(successful),
        "zero_lambda_boundary": {
            key: value
            for key, value in boundary.items()
            if key != "solution"
        },
        "zero_lambda_shape": {
            "rms_vs_fixed_closure": boundary_evaluated[
                "rms_vs_fixed_closure"
            ],
            "max_abs_vs_fixed_closure": boundary_evaluated[
                "max_abs_vs_fixed_closure"
            ],
            "minimum_shape": float(np.min(boundary_evaluated["shape"])),
            "maximum_shape": float(np.max(boundary_evaluated["shape"])),
            "minimum_forward_shape_increment": float(
                np.min(np.diff(boundary_evaluated["shape"]))
            ),
            "maximum_abs_chi_prime": float(
                np.max(np.abs(boundary_evaluated["chi_prime"]))
            ),
            "minimum_E": float(np.min(boundary_evaluated["E"])),
            **effective_fit,
        },
        "finite_start_sensitivity": {
            "rows": start_sensitivity_rows,
            "maximum_abs_delta_mu_from_N_minus_5": max(
                abs(row["delta_mu_from_N_minus_5"])
                for row in start_sensitivity_rows
            ),
            "maximum_shape_rms_from_N_minus_5": max(
                row["shape_rms_from_N_minus_5"]
                for row in start_sensitivity_rows
            ),
        },
        "best_nonnegative_lambda_or_boundary": {
            "mu": best_branch["mu"],
            "omega_lambda": best_branch["omega_lambda"],
            "rms_vs_fixed_closure": best_evaluated[
                "rms_vs_fixed_closure"
            ],
            "max_abs_vs_fixed_closure": best_evaluated[
                "max_abs_vs_fixed_closure"
            ],
        },
        "tensor_maximum": {
            "max_abs_delta_Q_over_H0tP_fourth": float(
                np.max(
                    np.abs(
                        boundary_evaluated[
                            "delta_Q_over_H0tP_fourth"
                        ]
                    )
                )
            ),
            "max_abs_delta_F_over_H0tP_fourth": float(
                np.max(
                    np.abs(
                        boundary_evaluated[
                            "delta_F_over_H0tP_fourth"
                        ]
                    )
                )
            ),
            "max_abs_delta_Q_H0_70": float(
                np.max(
                    np.abs(
                        boundary_evaluated[
                            "delta_Q_over_H0tP_fourth"
                        ]
                    )
                )
                * (
                    H0_KM_S_MPC
                    * 1000.0
                    / MPC_METRES
                    * PLANCK_TIME_SECONDS
                )
                ** 4
            ),
            "max_abs_delta_F_H0_70": float(
                np.max(
                    np.abs(
                        boundary_evaluated[
                            "delta_F_over_H0tP_fourth"
                        ]
                    )
                )
                * (
                    H0_KM_S_MPC
                    * 1000.0
                    / MPC_METRES
                    * PLANCK_TIME_SECONDS
                )
                ** 4
            ),
        },
    }
    scan_rows.append(
        {
            "branch": "zero_Lambda_boundary_parent_scalar",
            "mu_m_over_H0": boundary["mu"],
            "target_B_mem": B_MEMORY,
            "J_gap_for_H0_70": (
                boundary["mu"]
                * (H0_KM_S_MPC * 1000.0 / MPC_METRES)
                * PLANCK_TIME_SECONDS
            )
            ** 2,
            "mass_eV_for_H0_70": (
                boundary["mu"]
                * (H0_KM_S_MPC * 1000.0 / MPC_METRES)
                * HBAR_EV_SECONDS
            ),
            "chi_initial": boundary["chi_initial"],
            "omega_lambda": 0.0,
            "omega_scalar_zero": boundary["omega_scalar_zero"],
            "omega_scalar_initial": boundary["omega_scalar_initial"],
            "step": boundary["step"],
            "flat_step_residual_infinity": boundary["residual_infinity"],
            "rms_vs_fixed_p3_u3quarter": boundary_evaluated[
                "rms_vs_fixed_closure"
            ],
            "max_abs_vs_fixed_p3_u3quarter": boundary_evaluated[
                "max_abs_vs_fixed_closure"
            ],
            "effective_p": effective_fit["p_effective"],
            "effective_u": effective_fit["u_effective"],
            "effective_shape_rms": effective_fit["rms"],
            "status": "PHYSICAL_BOUNDARY_SOLUTION",
        }
    )
    for candidate, candidate_evaluated in start_sensitivity_pairs[1:]:
        scan_rows.append(
            {
                "branch": "zero_Lambda_finite_start_sensitivity",
                "mu_m_over_H0": candidate["mu"],
                "target_B_mem": B_MEMORY,
                "N_initial": candidate["N_initial"],
                "chi_initial": candidate["chi_initial"],
                "omega_lambda": 0.0,
                "omega_scalar_zero": candidate["omega_scalar_zero"],
                "omega_scalar_initial": candidate["omega_scalar_initial"],
                "step": candidate["step"],
                "flat_step_residual_infinity": candidate[
                    "residual_infinity"
                ],
                "shape_rms_from_N_minus_5": float(
                    np.sqrt(
                        np.mean(
                            (
                                candidate_evaluated["shape"]
                                - boundary_evaluated["shape"]
                            )
                            ** 2
                        )
                    )
                ),
                "status": "FINITE_START_SENSITIVITY_SOLUTION",
            }
        )
    return (
        tagged(scan_rows),
        tagged(comparison_rows),
        tagged(tensor_rows),
        summary,
    )


def parent_contract_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "sector": "functional_kinetic",
                "parent_equation": (
                    "P_k(X_c)=k^4 p_k(x), x=X_c/k^4, "
                    "p=x/2+sum_(n>=2) a_n x^n"
                ),
                "derived_FLRW_equation": (
                    "rho=P+V-2XP_X; pressure=-(P+V)"
                ),
                "ownership": "4957 trajectory",
                "status": "PARENT_OWNED_LOCAL_GERM",
            },
            {
                "sector": "scalar_equation",
                "parent_equation": "L=-P(X)-V(psi)",
                "derived_FLRW_equation": (
                    "(P_X+2XP_XX)ddot(psi)+3H P_X dot(psi)+V_psi/2=0"
                ),
                "ownership": "4935+5184 convention",
                "status": "DERIVED",
            },
            {
                "sector": "massless_current",
                "parent_equation": "V_psi=0",
                "derived_FLRW_equation": (
                    "a^3 P_X dot(psi)=Q; "
                    "dln|X|/dlna=-6c_s^2"
                ),
                "ownership": "shift-symmetric subbranch",
                "status": "DERIVED_ONE_STATE_CONSTANT",
            },
            {
                "sector": "massive_1PI",
                "parent_equation": "V=m_gap^2 psi_c^2/2",
                "derived_FLRW_equation": (
                    "ddot(psi_c)+3Hdot(psi_c)+m_gap^2 psi_c=0 "
                    "at leading canonical order"
                ),
                "ownership": "4935 renormalized 1PI entry",
                "status": "DERIVED_TWO_SCALE_BRANCH",
            },
            {
                "sector": "motion_scale",
                "parent_equation": "J_gap=m_gap^2 G_N",
                "derived_FLRW_equation": (
                    "mu=m_gap/H0=sqrt(J_gap)/(H0 sqrt(G_N))"
                ),
                "ownership": "4938 universal essential scale",
                "status": "ACTION_PARAMETER_NOT_SELECTED",
            },
            {
                "sector": "initial_state",
                "parent_equation": "early regular mode dchi/dlna=0",
                "derived_FLRW_equation": (
                    "one homogeneous amplitude remains after decaying-mode removal"
                ),
                "ownership": "cosmological state data",
                "status": "STATE_PARAMETER_NOT_ACTION_COUPLING",
            },
            {
                "sector": "microscopic_fractional_potential",
                "parent_equation": "V=(3/4)g_psi |psi|^(4/3)",
                "derived_FLRW_equation": "not used as closed low-energy potential",
                "ownership": "4935 microscopic input",
                "status": "NOT_RG_CLOSED_BY_4937",
            },
        ]
    )


def branch_decision_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    boundary = summary["zero_lambda_boundary"]
    shape = summary["zero_lambda_shape"]
    return tagged(
        [
            {
                "branch": "massless_Q_zero",
                "result": "X=0, rho_psi=0 up to separately calibrated Lambda",
                "decision": "RETAIN_LOCAL_AND_COSMOLOGICAL_VACUUM",
                "next_action": "none for O4; it is exactly silent",
            },
            {
                "branch": "massless_Q_nonzero",
                "result": "analytic low-X branch is stiff and carries one current state datum",
                "decision": "RETAIN_AS_BOUNDED_STATE_NOT_MEMORY",
                "next_action": "constrain abundance with early-universe data if populated",
            },
            {
                "branch": "M6_as_source_free_PX",
                "result": "exact current and endpoint reconstruction contradiction",
                "decision": "REJECT_IDENTITY",
                "next_action": "do not relabel fitted B_mem as the P(X) clock",
            },
            {
                "branch": "massive_quadratic_parent_scalar",
                "result": (
                    f"physical thaw branch exists; zero-Lambda boundary "
                    f"mu={boundary['mu']:.12g}"
                ),
                "decision": "RETAIN_AS_DIRECT_TEST_MODEL",
                "next_action": (
                    "score the direct ODE against LCDM, wCDM, CPL and old M6"
                ),
            },
            {
                "branch": "fixed_p3_u3quarter_identity",
                "result": (
                    f"direct scalar RMS={shape['rms_vs_fixed_closure']:.6g}, "
                    f"max residual={shape['max_abs_vs_fixed_closure']:.6g}"
                ),
                "decision": "REJECT_EXACT_PARENT_SHAPE_IDENTITY",
                "next_action": (
                    f"use direct ODE; its best stretched-exponential diagnostic "
                    f"is p={shape['p_effective']:.6g}, u={shape['u_effective']:.6g}"
                ),
            },
            {
                "branch": "O4_on_massive_thaw",
                "result": (
                    "direct derivative prediction remains Planck-suppressed "
                    "through the executed branch"
                ),
                "decision": "RETAIN_ORDER_REDUCED_EFT",
                "next_action": "carry direct delta_Q and delta_F in CMB/GW scorer",
            },
            {
                "branch": "full_cosmology_claim",
                "result": (
                    "J_gap and one state amplitude remain unselected and the "
                    "direct scalar likelihood has not yet been run"
                ),
                "decision": "BLOCKED_FROM_PROMOTION",
                "next_action": "checkpoint 5193 direct parent-scalar likelihood",
            },
        ]
    )


def provenance_rows(source_hashes: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for index, (relative, expected) in enumerate(LOCAL_SOURCES.items()):
        rows.append(
            {
                "source_id": f"SRC5192_{index:02d}",
                "source_type": "local_hash_locked",
                "source": str(source_path(relative)),
                "sha256": source_hashes[relative],
                "expected_sha256": expected,
                "role": "parent action, functional trajectory, O4 theorem, or closure comparator",
                "status": "HASH_MATCHED",
            }
        )
    return tagged(rows)


def build_document(
    symbolic: dict[str, Any],
    germ_summary: dict[str, dict[str, str]],
    scalar_summary: dict[str, Any],
) -> str:
    boundary = scalar_summary["zero_lambda_boundary"]
    shape = scalar_summary["zero_lambda_shape"]
    start_sensitivity = scalar_summary["finite_start_sensitivity"]
    tensor = scalar_summary["tensor_maximum"]
    dynamic = germ_summary["dynamic_etaN"]
    reference = germ_summary["reference_etaN0"]
    return f"""# 5192 - Parent motion FLRW branch, memory separation, and mass-gap cosmology gate

Marker: `{MARKER}`

**Verdict:** the actual MTS motion sector does not turn the fitted direct-memory
closure into a derived homogeneous `P(X)` solution. The source-free analytic
massless branch obeys an exact shift-current theorem which rejects that
identification. The parent nevertheless already contains a distinct and
constructive cosmological route: its universal renormalized motion gap
`J_gap=m_gap^2 G_N` gives a massive homogeneous scalar that can freeze and
thaw. This route has now been integrated directly.

The direct parent scalar is not the old fixed `p=3,u=1/4` closure. Across the
nonnegative-`Lambda` fixed-step scan the closest admissible branch remains a
substantial shape mismatch. The zero-`Lambda` physical boundary has

```text
m_gap/H0 = {boundary['mu']:.15g},
Omega_psi,0 = {boundary['omega_scalar_zero']:.15g},
Omega_psi,early = {boundary['omega_scalar_initial']:.15g},
Delta Omega_psi = {boundary['step']:.15g},
RMS versus fixed p=3,u=1/4 = {shape['rms_vs_fixed_closure']:.15g},
maximum absolute shape residual = {shape['max_abs_vs_fixed_closure']:.15g}.
```

Its shape is accurately summarized only as a diagnostic by

```text
p_eff = {shape['p_effective']:.15g},
u_eff = {shape['u_effective']:.15g},
RMS of diagnostic summary = {shape['rms']:.15g}.
```

The next empirical model must therefore integrate the parent scalar ODE
itself rather than fit or rename the old memory ansatz.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Full parent background equations

Write the local kinetic function in the 4957 convention as

```text
P_k(X_c)=k^4 p_k(x),
x=X_c/k^4,
p_k(x)=x/2+sum_(n>=2) a_n(k)x^n.
```

With physical Lorentzian density convention `L=-P-V`, a homogeneous field
has

```text
rho_psi=P+V-2X P_X,
p_psi=-(P+V),
rho_psi+p_psi=-2X P_X.
```

The exact scalar equation is

```text
(P_X+2X P_XX)ddot(psi)
 +3H P_X dot(psi)+V_psi/2=0.
```

For `V_psi=0`,

```text
a^3 P_X dot(psi)=Q,
c_s^2=P_X/(P_X+2X P_XX),
dln|X|/dlna=-6c_s^2.
```

The symbolic continuity residual is exactly

```text
{symbolic['continuity_residual']}.
```

For the canonical germ, `X proportional a^-6`, so the nonzero massless state
is stiff. `Q` is a cosmological state constant; the action does not select it.

The complete current parent is not exactly shift symmetric. Checkpoint 4935
owns a microscopic fractional potential, but 4937 proves that it is not a
closed regular fixed-function eigenoperator. The low-energy 1PI coordinate is
instead the regular mass gap

```text
V_1PI=m_gap^2 psi_c^2/2,
J_gap=m_gap^2 G_N.
```

Checkpoint 4938 proves that `J_gap` is one universal essential action
parameter but does not predict its value.

## 2. Local functional-germ check

The order-eight `g=10^-10` endpoints were evaluated at
`-0.1<=x<=0` with 80-digit arithmetic. This is a local timelike analytic
continuation diagnostic, not a global Lorentzian fixed-function theorem.

```text
dynamic eta_N:
  min P_X                 = {dynamic['minimum_P_X']}
  min(P_X+2xP_XX)         = {dynamic['minimum_kinetic_principal']}
  max|w-1|                = {dynamic['maximum_abs_w_minus_1']}
  max|c_s^2-1|            = {dynamic['maximum_abs_cs2_minus_1']}

reference eta_N=0:
  min P_X                 = {reference['minimum_P_X']}
  min(P_X+2xP_XX)         = {reference['minimum_kinetic_principal']}
  max|w-1|                = {reference['maximum_abs_w_minus_1']}
  max|c_s^2-1|            = {reference['maximum_abs_cs2_minus_1']}
```

The infrared functional branch is therefore numerically canonical throughout
this local chart. It does not generate a late vacuum-like memory plateau.

## 3. Exact no-go for identifying M6 with the massless clock

The tested closure is

```text
F(n)=1-exp[-(n/u)^3],
rho_mem=B_mem F(n),
n=ln(1+z).
```

It has

```text
F(0)=0,
F'(0)=0,
F(infinity)=1.
```

Conservation gives

```text
rho+p=(1/3)d rho/dn.
```

At the present endpoint the enthalpy is zero. On the healthy analytic
`P_X>0` branch,

```text
rho+p=-2X P_X=0  =>  X=0.
```

The current is then

```text
Q=a^3P_X sqrt(-X)=0.
```

Since `Q` is conserved, a connected healthy branch has `X=0` at every time
and cannot produce nonzero `B_mem F(n)`.

There is an independent endpoint check. For any finite nonzero `Q`, a
barotropic reconstruction gives

```text
X Q^2=-a^6(rho+p)^2/4,
P=-p=rho-(1/3)d rho/dn.
```

The closure sends `X->0` at both endpoints but requires `P->0` at one and
`P->B_mem` at the other. It is not a single-valued analytic `P(X)`.
Source/exchange dynamics or an extra field may evade this theorem; silently
calling the closure the massless clock may not.

## 4. Direct massive parent branch

Set

```text
chi=psi_c/(sqrt(6)M_R),
mu=m_gap/H0,
N=ln a.
```

At leading canonical order the exact flat-background system used here is

```text
E^2=[Omega_m e^(-3N)+Omega_r e^(-4N)+Omega_Lambda
     +mu^2 chi^2]/[1-(chi')^2],

chi''+[3+dlnH/dN]chi'+mu^2 chi/E^2=0,

dlnH/dN=[
 -3 Omega_m e^(-3N)/2
 -2 Omega_r e^(-4N)
 -3E^2(chi')^2]/E^2.
```

The finite-start frozen-mode condition is `chi'(N=-5)=0`. For each `mu`,
flatness and the nonclaim comparator `Delta Omega_psi=2/27` solve for the
early amplitude and nonnegative `Omega_Lambda`. No closure shape is inserted
into this ODE. Repeating the zero-`Lambda` solve from `N=-6` and `N=-7`
changes `mu` by at most
`{start_sensitivity['maximum_abs_delta_mu_from_N_minus_5']:.6g}` and changes
the normalized branch shape by RMS at most
`{start_sensitivity['maximum_shape_rms_from_N_minus_5']:.6g}`. The finite
start is therefore numerically converged for this checkpoint.

The smallest admissible nonnegative-`Lambda` solution is the zero-`Lambda`
boundary quoted above. For `H0=70 km/s/Mpc`, it corresponds to

```text
m_gap = {boundary['mu'] * (H0_KM_S_MPC * 1000.0 / MPC_METRES) * HBAR_EV_SECONDS:.15g} eV,
J_gap = {(boundary['mu'] * (H0_KM_S_MPC * 1000.0 / MPC_METRES) * PLANCK_TIME_SECONDS) ** 2:.15g}.
```

These are conditional translations of the comparator transition, not parent
predictions. They show that a late thaw requires the already-owned universal
gap to lie near the Hubble scale.

## 5. Why the old fixed shape is not derived

The direct ODE rises too broadly in `n=ln(1+z)`:

```text
direct scalar best diagnostic: p={shape['p_effective']:.9g},
                               u={shape['u_effective']:.9g};
old closure:                    p=3,
                               u=1/4.
```

The direct scalar is a viable model family, but it is not mathematically the
same model. This is useful progress: the previously fitted `B_mem,p,u3`
furniture can now be replaced by one universal action mass, one homogeneous
state amplitude, and the separately declared `Lambda_cal`, then penalized
fairly against `Lambda`CDM, `w`CDM and CPL.

## 6. O4 prediction on the massive branch

For `B=-c_O4 dot(psi_c)^2`, the 5191 order-reduced coefficients were
evaluated directly, including the potential-sourced time derivatives rather
than using the massless shift-current shape law. Differentiating the massive
Klein-Gordon equation gives

```text
psi'''=-3 dot(H) dot(psi)-3H ddot(psi)-m_gap^2 dot(psi),

[ddot(B)+Hdot(B)]/(-2c_O4)
 =ddot(psi)^2-3dot(H)dot(psi)^2
  -2Hdot(psi)ddot(psi)-m_gap^2dot(psi)^2.
```

The symbolic reduction residual is exactly
`{symbolic['O4_massive_KG_reduction_residual']}`. Over
`0<=z<=exp(2)-1`,

```text
max|delta_Q/(H0 t_P)^4|
  = {tensor['max_abs_delta_Q_over_H0tP_fourth']:.15g},

max|delta_F/(H0 t_P)^4|
  = {tensor['max_abs_delta_F_over_H0tP_fourth']:.15g}.
```

At the displayed `H0` calibration this is

```text
max|delta_Q| = {tensor['max_abs_delta_Q_H0_70']:.15g},
max|delta_F| = {tensor['max_abs_delta_F_H0_70']:.15g}.
```

Thus the massive thaw route does not endanger low-energy tensor propagation.
The all-scale UV completion boundary from 5191 remains unchanged.

## 7. Decision

```text
parent FLRW stress and scalar equation         = derived;
massless shift-current branch                  = derived;
massless nonzero branch state selection        = not supplied;
M6 equals source-free analytic P(X)             = rejected exactly;
universal massive parent-scalar route           = retained;
J_gap numerical value                           = not selected;
homogeneous amplitude                           = state datum;
fixed p=3,u=1/4 parent identity                 = rejected numerically;
direct parent-scalar likelihood                 = next calculation;
O4 massive-branch tensor safety                 = passed conditionally;
full cosmology or unified-theory claim          = false.
```

## 8. Next target

Checkpoint 5193 should add a direct ODE likelihood model, not another closure
ledger. It should score:

```text
LambdaCDM,
wCDM,
CPL,
old fixed M6 comparator,
parent scalar with Lambda_cal free,
parent scalar with Lambda_cal=0 ablation.
```

The parent scalar must use one universal `J_gap`, one homogeneous state
amplitude, the same Pantheon+/DESI DR2 covariance treatment, explicit
parameter penalties, prior-edge diagnostics, and order-reduced
`delta_Q,delta_F` outputs. A fit may estimate the universal mass and state; it
may not be relabelled as their derivation.

## 9. Machine artifacts

- `source-intake/functional_rg/5192/parent_motion_FLRW_contract.csv`
- `source-intake/functional_rg/5192/functional_PX_timelike_IR_germ.csv`
- `source-intake/functional_rg/5192/memory_PX_exact_no_go.csv`
- `source-intake/functional_rg/5192/massive_parent_scalar_scan.csv`
- `source-intake/functional_rg/5192/closure_vs_parent_scalar_shape.csv`
- `source-intake/functional_rg/5192/O4_massive_branch_tensor_prediction.csv`
- `source-intake/functional_rg/5192/branch_decision.csv`
- `source-intake/functional_rg/5192/source_provenance.csv`
- `source-intake/functional_rg/5192/parent_motion_FLRW_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5192_VALIDATION.csv`
"""


def validation_rows(
    source_hashes: dict[str, str],
    formal_before: str,
    checkpoint_before: str,
    symbolic: dict[str, Any],
    germ_summary: dict[str, dict[str, str]],
    scan_rows: list[dict[str, Any]],
    scalar_summary: dict[str, Any],
    output_paths: tuple[Path, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check: str, passed: bool, observed: Any, expected: Any) -> None:
        rows.append(
            {
                "check_id": f"V5192_{len(rows):02d}",
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
            }
        )

    add(
        "all locked local source hashes match",
        source_hashes == LOCAL_SOURCES,
        sum(source_hashes[key] == value for key, value in LOCAL_SOURCES.items()),
        len(LOCAL_SOURCES),
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
        "P(X) continuity residual vanishes",
        symbolic["continuity_residual"] == "0",
        symbolic["continuity_residual"],
        "0",
    )
    add("closure F(0) is zero", symbolic["F_zero"] == "0", symbolic["F_zero"], "0")
    add(
        "closure F prime at zero is zero",
        symbolic["Fprime_zero"] == "0",
        symbolic["Fprime_zero"],
        "0",
    )
    add(
        "closure high-past endpoint is one",
        symbolic["F_infinity"] == "1",
        symbolic["F_infinity"],
        "1",
    )
    add(
        "reconstructed P has distinct endpoints",
        (
            symbolic["P_reconstructed_zero"] == "0"
            and symbolic["P_reconstructed_infinity"] == "b"
        ),
        (
            symbolic["P_reconstructed_zero"],
            symbolic["P_reconstructed_infinity"],
        ),
        ("0", "b"),
    )
    add(
        "reconstructed X returns to zero at both endpoints",
        (
            symbolic["X_times_Q2_zero"] == "0"
            and symbolic["X_times_Q2_infinity"] == "0"
        ),
        (
            symbolic["X_times_Q2_zero"],
            symbolic["X_times_Q2_infinity"],
        ),
        ("0", "0"),
    )
    for scheme, summary in germ_summary.items():
        add(
            f"{scheme} timelike diagnostic P_X positive",
            Decimal(summary["minimum_P_X"]) > 0,
            summary["minimum_P_X"],
            ">0",
        )
        add(
            f"{scheme} timelike diagnostic principal kinetic positive",
            Decimal(summary["minimum_kinetic_principal"]) > 0,
            summary["minimum_kinetic_principal"],
            ">0",
        )
        add(
            f"{scheme} infrared equation of state is locally canonical",
            Decimal(summary["maximum_abs_w_minus_1"]) < Decimal("1e-15"),
            summary["maximum_abs_w_minus_1"],
            "<1e-15",
        )
        add(
            f"{scheme} infrared sound speed is locally canonical",
            Decimal(summary["maximum_abs_cs2_minus_1"]) < Decimal("1e-15"),
            summary["maximum_abs_cs2_minus_1"],
            "<1e-15",
        )
    boundary = scalar_summary["zero_lambda_boundary"]
    shape = scalar_summary["zero_lambda_shape"]
    start_sensitivity = scalar_summary["finite_start_sensitivity"]
    tensor = scalar_summary["tensor_maximum"]
    physical_scan_rows = [
        row
        for row in scan_rows
        if row["status"] == "PHYSICAL_NONNEGATIVE_LAMBDA_SOLUTION"
    ]
    add(
        "successful fixed-step scan row count matches the summary",
        (
            len(physical_scan_rows)
            == scalar_summary["successful_nonnegative_lambda_scan_rows"]
            and len(physical_scan_rows) > 0
        ),
        len(physical_scan_rows),
        scalar_summary["successful_nonnegative_lambda_scan_rows"],
    )
    add(
        "all successful fixed-step scan rows expose the comparator target",
        all(
            abs(float(row["target_B_mem"]) - B_MEMORY) < 1.0e-14
            for row in physical_scan_rows
        ),
        len(
            [
                row
                for row in physical_scan_rows
                if abs(float(row["target_B_mem"]) - B_MEMORY) < 1.0e-14
            ]
        ),
        len(physical_scan_rows),
    )
    add(
        "all successful fixed-step scan rows close flatness and step",
        all(
            float(row["flat_step_residual_infinity"]) < 2.0e-7
            and abs(float(row["step"]) - B_MEMORY) < 2.0e-7
            for row in physical_scan_rows
        ),
        len(
            [
                row
                for row in physical_scan_rows
                if float(row["flat_step_residual_infinity"]) < 2.0e-7
                and abs(float(row["step"]) - B_MEMORY) < 2.0e-7
            ]
        ),
        len(physical_scan_rows),
    )
    add(
        "all successful fixed-step scan rows retain nonnegative Lambda",
        all(float(row["omega_lambda"]) >= 0.0 for row in physical_scan_rows),
        (
            min(float(row["omega_lambda"]) for row in physical_scan_rows)
            if physical_scan_rows
            else "NO_ROWS"
        ),
        ">=0",
    )
    add(
        "zero-Lambda boundary solve closes flatness and step",
        boundary["residual_infinity"] < 1.0e-8,
        boundary["residual_infinity"],
        "<1e-8",
    )
    add(
        "zero-Lambda boundary has positive mass ratio",
        boundary["mu"] > 0,
        boundary["mu"],
        ">0",
    )
    add(
        "zero-Lambda boundary reproduces comparator step",
        abs(boundary["step"] - B_MEMORY) < 1.0e-8,
        boundary["step"],
        B_MEMORY,
    )
    add(
        "direct scalar is not numerically identical to fixed closure",
        shape["rms_vs_fixed_closure"] > 0.1,
        shape["rms_vs_fixed_closure"],
        ">0.1",
    )
    add(
        "direct scalar has a compact diagnostic stretched-exponential summary",
        shape["rms"] < 0.01,
        shape["rms"],
        "<0.01",
    )
    add(
        "direct scalar effective p is not fixed p=3",
        abs(shape["p_effective"] - 3.0) > 1.0,
        shape["p_effective"],
        "distance from 3 >1",
    )
    add(
        "direct scalar trajectory is monotone over the scored redshift window",
        shape["minimum_forward_shape_increment"] >= -1.0e-10,
        shape["minimum_forward_shape_increment"],
        ">=-1e-10",
    )
    add(
        "direct scalar trajectory stays on the regular Friedmann branch",
        shape["minimum_E"] > 0.0 and shape["maximum_abs_chi_prime"] < 1.0,
        (shape["minimum_E"], shape["maximum_abs_chi_prime"]),
        "E>0 and max|chi_prime|<1",
    )
    add(
        "finite-start frozen-mode boundary is converged",
        (
            start_sensitivity["maximum_abs_delta_mu_from_N_minus_5"]
            < 1.0e-4
            and start_sensitivity["maximum_shape_rms_from_N_minus_5"]
            < 1.0e-4
        ),
        (
            start_sensitivity["maximum_abs_delta_mu_from_N_minus_5"],
            start_sensitivity["maximum_shape_rms_from_N_minus_5"],
        ),
        "both <1e-4",
    )
    add(
        "massive Klein-Gordon equation exactly reduces the O4 derivative shape",
        symbolic["O4_massive_KG_reduction_residual"] == "0",
        symbolic["O4_massive_KG_reduction_residual"],
        "0",
    )
    add(
        "O4 massive-branch delta Q is negligible at H0 benchmark",
        tensor["max_abs_delta_Q_H0_70"] < 1.0e-100,
        tensor["max_abs_delta_Q_H0_70"],
        "<1e-100",
    )
    add(
        "O4 massive-branch delta F is negligible at H0 benchmark",
        tensor["max_abs_delta_F_H0_70"] < 1.0e-100,
        tensor["max_abs_delta_F_H0_70"],
        "<1e-100",
    )
    add(
        "all planned machine outputs exist and are nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in output_paths),
        sum(path.exists() and path.stat().st_size > 0 for path in output_paths),
        len(output_paths),
    )
    return tagged(rows)


def main() -> None:
    source_hashes = {
        relative: file_digest(source_path(relative)) for relative in LOCAL_SOURCES
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_before = tree_digest(CHECKPOINT_5176)

    trajectory = load_trajectory_rows()
    endpoints = endpoint_rows(trajectory)
    germ_rows, germ_summary = functional_germ_rows(endpoints)
    symbolic = symbolic_contract()
    no_go_rows = memory_no_go_rows(symbolic)
    scan_rows, comparison_rows, tensor_rows, scalar_summary = scalar_scan()
    contract_rows = parent_contract_rows()
    decision_rows = branch_decision_rows(scalar_summary)
    source_rows = provenance_rows(source_hashes)

    output_map: dict[Path, list[dict[str, Any]]] = {
        OUT / "parent_motion_FLRW_contract.csv": contract_rows,
        OUT / "functional_PX_timelike_IR_germ.csv": germ_rows,
        OUT / "memory_PX_exact_no_go.csv": no_go_rows,
        OUT / "massive_parent_scalar_scan.csv": scan_rows,
        OUT / "closure_vs_parent_scalar_shape.csv": comparison_rows,
        OUT / "O4_massive_branch_tensor_prediction.csv": tensor_rows,
        OUT / "branch_decision.csv": decision_rows,
        OUT / "source_provenance.csv": source_rows,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)

    result_path = OUT / "parent_motion_FLRW_results.json"
    document_text = build_document(symbolic, germ_summary, scalar_summary)
    result_payload = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "theorem": (
            "THE_SOURCE_FREE_ANALYTIC_MASSLESS_PARENT_PX_CLOCK_CANNOT_"
            "REALIZE_THE_NONZERO_FIXED_P3_U3QUARTER_MEMORY_STEP_BECAUSE_"
            "ZERO_PRESENT_ENTHALPY_FORCES_ZERO_X_AND_ZERO_CONSERVED_"
            "SHIFT_CURRENT_WHILE_THE_PARAMETRIC_RECONSTRUCTION_RETURNS_"
            "TO_X_ZERO_WITH_TWO_DIFFERENT_P_VALUES_THE_PARENT_OWNED_"
            "UNIVERSAL_MASS_GAP_INSTEAD_DEFINES_A_DIRECT_MASSIVE_FLRW_"
            "SCALAR_ROUTE_WITH_ONE_ACTION_MASS_AND_ONE_STATE_AMPLITUDE_"
            "THE_EXECUTED_THAW_BRANCH_IS_NOT_THE_OLD_FIXED_MEMORY_SHAPE_"
            "AND_MUST_BE_SCORED_DIRECTLY_WHILE_ITS_O4_TENSOR_CORRECTIONS_"
            "REMAIN_PLANCK_SUPPRESSED"
        ),
        "claim_guard": (
            "NO_COSMOLOGY_SUPPORT_CLAIM_NO_DERIVATION_OF_J_GAP_VALUE_NO_"
            "DERIVATION_OF_THE_HOMOGENEOUS_STATE_AMPLITUDE_NO_IDENTITY_"
            "BETWEEN_THE_DIRECT_SCALAR_AND_THE_OLD_MEMORY_CLOSURE_NO_"
            "FULL_MTS_UNIFICATION_CLAIM"
        ),
        "symbolic_contract": symbolic,
        "functional_germ_summary": germ_summary,
        "scalar_summary": scalar_summary,
        "source_hashes": source_hashes,
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_before,
        "next_target": (
            "5193 direct parent-scalar Pantheon+ DESI-DR2 likelihood "
            "against LCDM wCDM CPL and old M6 comparator"
        ),
    }
    write_json(result_path, result_payload)
    DOCUMENT.write_text(document_text, encoding="utf-8")

    output_paths = tuple(output_map) + (result_path, DOCUMENT)
    checks = validation_rows(
        source_hashes,
        formal_before,
        checkpoint_before,
        symbolic,
        germ_summary,
        scan_rows,
        scalar_summary,
        output_paths,
    )

    formal_after = tree_digest(FORMAL)
    checkpoint_after = tree_digest(CHECKPOINT_5176)

    def add_final(check: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append(
            {
                "check_id": f"V5192_{len(checks):02d}",
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "expected": expected,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "valid_for_cosmology_support_claim": False,
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
            not bool(row["valid_for_full_MTS_claim"])
            and not bool(row["valid_for_cosmology_support_claim"])
            for collection in (
                contract_rows,
                germ_rows,
                no_go_rows,
                scan_rows,
                comparison_rows,
                tensor_rows,
                decision_rows,
                source_rows,
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
    print(
        json.dumps(
            {
                "checkpoint": 5192,
                "marker": MARKER,
                "validation_passed": len(checks),
                "validation_failed": 0,
                "massless_memory_identity": False,
                "zero_lambda_mu": scalar_summary["zero_lambda_boundary"]["mu"],
                "direct_scalar_rms_vs_fixed_closure": scalar_summary[
                    "zero_lambda_shape"
                ]["rms_vs_fixed_closure"],
                "direct_scalar_effective_p": scalar_summary[
                    "zero_lambda_shape"
                ]["p_effective"],
                "direct_scalar_effective_u": scalar_summary[
                    "zero_lambda_shape"
                ]["u_effective"],
                "next_target": result_payload["next_target"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
