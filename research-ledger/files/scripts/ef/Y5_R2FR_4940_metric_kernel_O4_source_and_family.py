from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

import Y5_R2FR_4934_completed_combined_flow as completed_flow


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4940"
RESULT_JSON = SOURCE / "metric_kernel_O4_source_and_family_results.json"
SPECTRUM_CSV = SOURCE / "O4_kernel_augmented_spectrum.csv"
FAMILY_CSV = SOURCE / "O4_kernel_GR_family.csv"
SOURCE_CSV = SOURCE / "O4_source_decomposition.csv"
GAUSSIAN_CSV = SOURCE / "gammaC2_gaussian_scaling.csv"

COMPLETED_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
COMPLETED_RESULT = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
RESULT_4939 = POST / "source-intake" / "functional_rg" / "4939" / "known_source_O4_and_backreacted_family_results.json"
CHECKPOINT_4939 = POST / "4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md"
CHECKPOINT_4930 = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
BASIS_4930 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
ESS_CUBIC_SOURCE = POST / "source-intake" / "functional_rg" / "4929" / "src2312" / "ess_cubic.tex"

EXPECTED_HASHES = {
    COMPLETED_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    COMPLETED_RESULT: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    RESULT_4939: "3859aded9146696080bd7c0209f5a2385ef68ee2dac43ee293a5b864305dd041",
    CHECKPOINT_4939: "9da47eb0232980ca743c50617645c0d02cfaaeca58793a0d244bc9450418fa9e",
    CHECKPOINT_4930: "1b987f0040d4288d9057b52f2f792c6484b6a0a8edd0bf817d71f7abf6a03755",
    BASIS_4930: "93d8485ad79cc72ce2e9f6be3d81dc3605c785cb45436431d64041415e951361",
    ESS_CUBIC_SOURCE: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
}

MARKER = "MTS_4940_METRIC_KERNEL_O4_SOURCE_AND_FAMILY"
COORDINATE_NAMES = ("g", "g_plus", "g_minus", "g_CFF", "h_C3", "u_O4")
MASS_MAPPINGS = {
    "Wetterich_v_equals_plus_2lambda": 1.0,
    "Wetterich_v_equals_minus_2lambda": -1.0,
}
SEED_AMPLITUDES = (1.0e-5, 3.0e-6, 1.0e-6)
R_UV_VALUES = (1.0e-12, 1.0e-10, 1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2, 1.0)
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
C2_ROW = 4
RC2_ROW = 7
GAMMA_C2_INDEX = 7


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in values]


def decoupling(w_value: float) -> float:
    if w_value <= 0.0:
        return 1.0
    if w_value > 1.0e200:
        return 0.0
    return 1.0 / (1.0 + w_value)


def mass_scaling_A(g_value: float, v_sign: float) -> float:
    dimensionless_planck = 1.0 / (16.0 * math.pi * g_value)
    v_value = v_sign * 3.0 * g_value / (8.0 * math.pi)
    return 1.0 / (96.0 * math.pi**2 * dimensionless_planck) * (
        20.0 / (1.0 - v_value) ** 2
        + 1.0 / (1.0 - v_value / 4.0) ** 2
    )


def numerical_jacobian(
    function: Callable[[np.ndarray], np.ndarray],
    point: np.ndarray,
    floors: np.ndarray,
) -> np.ndarray:
    jacobian = np.zeros((len(point), len(point)), dtype=float)
    for column in range(len(point)):
        step = 2.0e-5 * max(abs(point[column]), floors[column])
        plus = point.copy()
        minus = point.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (function(plus) - function(minus)) / (2.0 * step)
    return jacobian


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {
        path.as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = [
        path.as_posix()
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.as_posix()] != expected
    ]
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")

    SOURCE.mkdir(parents=True, exist_ok=True)
    previous = json.loads(RESULT_4939.read_text(encoding="utf-8"))
    x_seed = np.asarray(
        list(previous["massless_scalar_backreacted_fixed_point"]["coordinates"].values()),
        dtype=float,
    )
    system, _, _, _, _, _ = completed_flow.build_completed_solver()

    def solve_known_source(
        x_point: np.ndarray,
        u_value: float,
        w_value: float,
    ) -> tuple[np.ndarray, float, np.ndarray, float]:
        matrix, vector = system(x_point)
        D_value = decoupling(w_value)
        delta_beta_g = x_point[0] ** 2 * D_value / (6.0 * math.pi)
        augmented_vector = vector + matrix[:, 0] * delta_beta_g
        augmented_vector[C2_ROW] += (
            -u_value * D_value**2 / (24.0 * math.pi**2)
        )
        augmented_vector[RC2_ROW] += (
            -u_value * D_value**2 / (96.0 * math.pi**2)
        )
        unknowns = np.linalg.solve(matrix, augmented_vector)
        beta_x = np.array(
            [
                unknowns[0],
                (unknowns[13] + unknowns[14]) / 2.0,
                (unknowns[13] - unknowns[14]) / 2.0,
                unknowns[15],
                unknowns[1],
            ],
            dtype=float,
        )
        gamma_c2 = float(unknowns[GAMMA_C2_INDEX])
        beta_u = 4.0 * u_value - 0.5 * gamma_c2
        residual = matrix @ unknowns - augmented_vector
        return (
            beta_x,
            beta_u,
            unknowns,
            float(np.linalg.norm(residual, ord=np.inf)),
        )

    _, _, seed_unknowns, _ = solve_known_source(x_seed, 0.0, 0.0)
    gamma_seed = float(seed_unknowns[GAMMA_C2_INDEX])
    initial_u = gamma_seed / 8.0

    def fixed_beta(state: np.ndarray) -> np.ndarray:
        beta_x, beta_u, _, _ = solve_known_source(state[:5], float(state[5]), 0.0)
        return np.concatenate([beta_x, np.array([beta_u])])

    fixed_solution = root(
        fixed_beta,
        np.concatenate([x_seed, np.array([initial_u])]),
        method="hybr",
        options={"maxfev": 5000, "xtol": 1.0e-11},
    )
    fixed_state = np.asarray(fixed_solution.x, dtype=float)
    fixed_residual = fixed_beta(fixed_state)
    if (
        not fixed_solution.success
        or np.linalg.norm(fixed_residual, ord=np.inf) >= 1.0e-9
    ):
        raise RuntimeError(
            f"O4 fixed point failed: {fixed_solution.message}; "
            f"residual={fixed_residual.tolist()}"
        )
    fixed_x = fixed_state[:5]
    fixed_u = float(fixed_state[5])
    _, _, fixed_unknowns, fixed_linear_residual = solve_known_source(
        fixed_x, fixed_u, 0.0
    )
    fixed_gamma_c2 = float(fixed_unknowns[GAMMA_C2_INDEX])
    kernel_source_at_zero = -0.5 * float(
        solve_known_source(fixed_x, 0.0, 0.0)[2][GAMMA_C2_INDEX]
    )
    direct_trace_required_for_zero = -kernel_source_at_zero

    stability_6 = numerical_jacobian(
        fixed_beta,
        fixed_state,
        np.array([1.0e-5, 1.0e-4, 1.0e-4, 1.0e-6, 1.0e-8, 1.0e-5]),
    )
    values_6, vectors_6 = np.linalg.eig(stability_6)
    gravity_indices = [index for index, value in enumerate(values_6) if value.real < 0.0]
    if len(gravity_indices) != 1:
        raise RuntimeError(f"expected one six-coordinate relevant direction: {values_6}")
    gravity_index = gravity_indices[0]
    theta_gravity = -float(values_6[gravity_index].real)
    gravity_vector_6 = np.real(vectors_6[:, gravity_index])
    if gravity_vector_6[0] < 0.0:
        gravity_vector_6 *= -1.0
    gravity_vector_6 /= float(
        np.max(np.abs(gravity_vector_6[:5] / fixed_x))
    )

    spectrum_rows: list[dict[str, Any]] = []
    mapping_data: dict[str, dict[str, Any]] = {}
    fixed_7 = np.concatenate([fixed_state, np.array([0.0])])
    for mapping, v_sign in MASS_MAPPINGS.items():
        def beta_7(state: np.ndarray) -> np.ndarray:
            x_point = state[:5]
            u_value = float(state[5])
            w_value = float(state[6])
            beta_x, beta_u, _, _ = solve_known_source(
                x_point, u_value, w_value
            )
            beta_w = (
                -2.0 + mass_scaling_A(float(x_point[0]), v_sign)
            ) * w_value
            return np.concatenate([beta_x, np.array([beta_u, beta_w])])

        stability_7 = numerical_jacobian(
            beta_7,
            fixed_7,
            np.array(
                [1.0e-5, 1.0e-4, 1.0e-4, 1.0e-6, 1.0e-8, 1.0e-5, 1.0e-5]
            ),
        )
        values_7, vectors_7 = np.linalg.eig(stability_7)
        relevant_indices = [
            index for index, value in enumerate(values_7) if value.real < 0.0
        ]
        mass_eigenvalue_target = (
            -2.0 + mass_scaling_A(float(fixed_x[0]), v_sign)
        )
        mass_index = int(
            np.argmin(np.abs(values_7 - mass_eigenvalue_target))
        )
        mass_vector_7 = np.real(vectors_7[:, mass_index])
        mass_vector_7 /= float(mass_vector_7[6])
        mapping_data[mapping] = {
            "v_sign": v_sign,
            "stability": stability_7,
            "values": values_7,
            "mass_eigenvalue": float(values_7[mass_index].real),
            "theta_mass": -float(values_7[mass_index].real),
            "uv_power": -float(values_7[mass_index].real) / theta_gravity,
            "mass_vector": mass_vector_7,
            "relevant_count": len(relevant_indices),
        }
        for mode_index, value in enumerate(
            sorted(values_7, key=lambda item: (item.real, item.imag))
        ):
            spectrum_rows.append(
                {
                    "mapping": mapping,
                    "mode_index": mode_index,
                    "beta_eigenvalue_real": float(value.real),
                    "beta_eigenvalue_imag": float(value.imag),
                    "critical_exponent_real": float(-value.real),
                    "critical_exponent_imag": float(-value.imag),
                    "relevant": bool(value.real < 0.0),
                    "O4_mode": bool(abs(value - stability_7[5, 5]) < 1.0e-6),
                    "motion_mass_mode": bool(
                        abs(value - values_7[mass_index]) < 1.0e-8
                    ),
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    gaussian_rows: list[dict[str, Any]] = []
    for g_value in np.logspace(-9, -5, 9):
        point = np.array([g_value, 0.0, 0.0, 0.0, 0.0], dtype=float)
        _, _, unknowns, residual = solve_known_source(point, 0.0, 1.0e100)
        gamma_value = float(unknowns[GAMMA_C2_INDEX])
        gaussian_rows.append(
            {
                "g": g_value,
                "gamma_C2": gamma_value,
                "gamma_C2_over_g2": gamma_value / g_value**2,
                "linear_solve_residual": residual,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    log_g = np.log([row["g"] for row in gaussian_rows])
    log_gamma = np.log([abs(row["gamma_C2"]) for row in gaussian_rows])
    gaussian_power, gaussian_log_coefficient = np.polyfit(log_g, log_gamma, 1)
    gaussian_coefficient = math.exp(float(gaussian_log_coefficient))

    family_rows: list[dict[str, Any]] = []
    massless_endpoints: dict[float, dict[str, Any]] = {}

    def integrate_massless(relative_seed: float) -> dict[str, Any]:
        initial = fixed_state - relative_seed * gravity_vector_6

        def rhs(_time: float, state: np.ndarray) -> np.ndarray:
            beta_x, beta_u, _, _ = solve_known_source(
                state[:5], float(state[5]), 0.0
            )
            return np.concatenate([beta_x, np.array([beta_u])])

        def event(_time: float, state: np.ndarray) -> float:
            return float(state[0] - IR_G_TARGET)

        event.terminal = True
        event.direction = -1
        solution = solve_ivp(
            rhs,
            (0.0, T_IR_LIMIT),
            initial,
            method="DOP853",
            rtol=2.0e-9,
            atol=np.array(
                [1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19, 1.0e-25]
            ),
            max_step=0.08,
            events=event,
        )
        if not solution.success or not len(solution.t_events[0]):
            raise RuntimeError(f"massless O4 branch failed for seed {relative_seed}")
        endpoint = np.asarray(solution.y[:, -1], dtype=float)
        return {
            "endpoint": endpoint,
            "time": float(solution.t[-1]),
        }

    for relative_seed in SEED_AMPLITUDES:
        baseline = integrate_massless(relative_seed)
        massless_endpoints[relative_seed] = baseline
        endpoint = baseline["endpoint"]
        family_rows.append(
            {
                "mapping": "massless_shared",
                "relative_gravity_seed": relative_seed,
                "R_UV": 0.0,
                "w_seed": 0.0,
                "t_endpoint": baseline["time"],
                "g_endpoint": float(endpoint[0]),
                "w_endpoint": 0.0,
                "J_gap_endpoint": 0.0,
                "u_O4_endpoint": float(endpoint[5]),
                "W_O4_equals_u_over_g2": float(endpoint[5] / endpoint[0] ** 2),
                "termination": "IR_G_TARGET",
                "direct_gravity_mixed_O4_trace_included": False,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    for mapping, data in mapping_data.items():
        mass_vector = np.asarray(data["mass_vector"], dtype=float)
        for relative_seed in SEED_AMPLITUDES:
            baseline = massless_endpoints[relative_seed]["endpoint"]
            for R_UV in R_UV_VALUES:
                w_seed = R_UV * relative_seed ** float(data["uv_power"])
                initial_6 = (
                    fixed_state
                    - relative_seed * gravity_vector_6
                    + w_seed * mass_vector[:6]
                )
                initial = np.concatenate(
                    [initial_6, np.array([math.log(w_seed)])]
                )

                def rhs(_time: float, state: np.ndarray) -> np.ndarray:
                    log_w = float(state[6])
                    w_value = math.exp(log_w) if log_w < 460.0 else 1.0e200
                    beta_x, beta_u, _, _ = solve_known_source(
                        state[:5], float(state[5]), w_value
                    )
                    beta_log_w = -2.0 + mass_scaling_A(
                        float(state[0]), float(data["v_sign"])
                    )
                    return np.concatenate(
                        [beta_x, np.array([beta_u, beta_log_w])]
                    )

                def event(_time: float, state: np.ndarray) -> float:
                    return float(state[0] - IR_G_TARGET)

                event.terminal = True
                event.direction = -1
                solution = solve_ivp(
                    rhs,
                    (0.0, T_IR_LIMIT),
                    initial,
                    method="DOP853",
                    rtol=2.0e-9,
                    atol=np.array(
                        [
                            1.0e-13,
                            1.0e-15,
                            1.0e-15,
                            1.0e-16,
                            1.0e-19,
                            1.0e-25,
                            1.0e-10,
                        ]
                    ),
                    max_step=0.08,
                    events=event,
                )
                if not solution.success or not len(solution.t_events[0]):
                    raise RuntimeError(
                        f"O4 family failed for {mapping} seed={relative_seed} R={R_UV}"
                    )
                endpoint_6 = np.asarray(solution.y[:6, -1], dtype=float)
                w_endpoint = math.exp(float(solution.y[6, -1]))
                g_endpoint = float(endpoint_6[0])
                u_endpoint = float(endpoint_6[5])
                family_rows.append(
                    {
                        "mapping": mapping,
                        "relative_gravity_seed": relative_seed,
                        "R_UV": R_UV,
                        "uv_power": float(data["uv_power"]),
                        "w_seed": w_seed,
                        "t_endpoint": float(solution.t[-1]),
                        "g_endpoint": g_endpoint,
                        "w_endpoint": w_endpoint,
                        "J_gap_endpoint": g_endpoint * w_endpoint,
                        "u_O4_endpoint": u_endpoint,
                        "W_O4_equals_u_over_g2": u_endpoint / g_endpoint**2,
                        "delta_W_O4_from_massless": (
                            u_endpoint / g_endpoint**2
                            - float(baseline[5] / baseline[0] ** 2)
                        ),
                        "termination": "IR_G_TARGET",
                        "direct_gravity_mixed_O4_trace_included": False,
                        "valid_for_full_MTS_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )

    positive_rows = [row for row in family_rows if float(row["R_UV"]) > 0.0]
    convergence: dict[str, Any] = {}
    for mapping in MASS_MAPPINGS:
        convergence[mapping] = {}
        for R_UV in R_UV_VALUES:
            rows = [
                row
                for row in positive_rows
                if row["mapping"] == mapping and row["R_UV"] == R_UV
            ]
            values = np.asarray(
                [row["W_O4_equals_u_over_g2"] for row in rows], dtype=float
            )
            reference = float(values[-1])
            convergence[mapping][str(R_UV)] = {
                "values": values.tolist(),
                "smallest_seed_reference": reference,
                "max_relative_difference": float(
                    np.max(np.abs(values - reference))
                    / max(abs(reference), 1.0e-300)
                ),
            }

    gamma_column = system(fixed_x)[0][:13, GAMMA_C2_INDEX]
    source_rows = [
        {
            "source_id": "O4S4940_0_metric_kernel",
            "source": "Psi_g contains gamma_C2 C^2 g_mn",
            "projection": "Psi_g_mn delta S_psi/delta g_mn=(gamma_C2/2) C^2 (nabla psi)^2",
            "beta_contribution": "-gamma_C2/2",
            "fixed_numeric": kernel_source_at_zero,
            "status": "DERIVED_NONZERO_COMPONENT",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "source_id": "O4S4940_1_scalar_C2_feedback",
            "source": "O4 scalar Hessian in the optimized trace",
            "projection": "Delta RHS_C2=-u_O4 D_psi^2/(24pi^2)",
            "beta_contribution": "included through source row 4",
            "fixed_numeric": -fixed_u / (24.0 * math.pi**2),
            "status": "DERIVED_AND_INCLUDED",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "source_id": "O4S4940_2_scalar_RC2_feedback",
            "source": "O4 scalar Hessian times scalar a2=R/6",
            "projection": "Delta RHS_RC2=-u_O4 D_psi^2/(96pi^2)",
            "beta_contribution": "included through source row 7",
            "fixed_numeric": -fixed_u / (96.0 * math.pi**2),
            "status": "DERIVED_AND_INCLUDED",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "source_id": "O4S4940_3_quadratic_scalar_external",
            "source": "two background-scalar derivatives of the quadratic scalar trace",
            "projection": "zero",
            "beta_contribution": "0",
            "fixed_numeric": 0.0,
            "status": "EXACT_ZERO",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "source_id": "O4S4940_4_neutral_photon_external",
            "source": "two background-scalar derivatives of the neutral photon trace",
            "projection": "zero",
            "beta_contribution": "0",
            "fixed_numeric": 0.0,
            "status": "EXACT_ZERO",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "source_id": "O4S4940_5_direct_gravity_mixed",
            "source": "off-shell metric-scalar and mixed Hessian RHS trace at C2p2",
            "projection": "S_O4_direct",
            "beta_contribution": "not included",
            "fixed_numeric": "",
            "status": "OPEN_CANCELLATION_OR_SHIFT_TERM",
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]

    checks = {
        "source_hashes_match": not hash_failures,
        "O4_fixed_point_converged": bool(fixed_solution.success),
        "O4_fixed_residual_below_1e_minus_9": bool(
            np.linalg.norm(fixed_residual, ord=np.inf) < 1.0e-9
        ),
        "linear_system_residual_small": fixed_linear_residual < 1.0e-10,
        "metric_kernel_source_nonzero": abs(kernel_source_at_zero) > 1.0e-5,
        "u_O4_fixed_point_nonzero": abs(fixed_u) > 1.0e-5,
        "gamma_C2_row7_is_dominant": abs(gamma_column[RC2_ROW])
        > 10.0
        * max(
            abs(value)
            for index, value in enumerate(gamma_column)
            if index != RC2_ROW
        ),
        "six_coordinate_block_has_one_relevant": len(gravity_indices) == 1,
        "both_seven_coordinate_blocks_have_two_relevant": all(
            data["relevant_count"] == 2 for data in mapping_data.values()
        ),
        "O4_eigenvalue_irrelevant": all(
            any(
                value.real > 3.5
                for value in data["values"]
            )
            for data in mapping_data.values()
        ),
        "all_family_runs_reach_IR": all(
            row["termination"] == "IR_G_TARGET" for row in family_rows
        ),
        "all_O4_Wilson_endpoints_finite": all(
            math.isfinite(float(row["W_O4_equals_u_over_g2"]))
            for row in family_rows
        ),
        "Gaussian_gammaC2_power_is_quadratic": abs(gaussian_power - 2.0) < 0.05,
        "direct_gravity_mixed_trace_not_silently_zeroed": source_rows[-1]["status"]
        == "OPEN_CANCELLATION_OR_SHIFT_TERM",
    }
    checks = {name: bool(passed) for name, passed in checks.items()}
    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "operator_and_kernel_derivation": {
            "O4": "C_abcd C^abcd (nabla psi)^2",
            "metric_kernel": "Psi_g_mn contains gamma_C2 C^2 g_mn on the Ricci-flat projection",
            "scalar_metric_contraction_general_d": "(d-2) gamma_C2 C^2 (nabla psi)^2/4",
            "d4_contraction": "gamma_C2 O4/2",
            "known_source_beta": "beta_uO4=4u_O4-gamma_C2/2",
            "scalar_feedback_rows": {
                "C2_row_4": "-u_O4 D_psi^2/(24pi^2)",
                "RC2_row_7": "-u_O4 D_psi^2/(96pi^2)",
            },
            "full_beta_contract": "beta_uO4=4u_O4-gamma_C2/2+S_O4_direct_gravity_mixed",
        },
        "O4_completed_known_source_fixed_point": {
            "success": bool(fixed_solution.success),
            "message": fixed_solution.message,
            "coordinates": dict(zip(COORDINATE_NAMES, fixed_state.tolist())),
            "beta_residual": fixed_residual.tolist(),
            "beta_residual_infinity_norm": float(
                np.linalg.norm(fixed_residual, ord=np.inf)
            ),
            "gamma_C2_at_fixed_point": fixed_gamma_c2,
            "metric_kernel_source_at_u_zero": kernel_source_at_zero,
            "direct_trace_required_for_u_zero": direct_trace_required_for_zero,
            "u_zero_invariant_in_known_source_system": False,
            "stability_matrix": stability_6.tolist(),
            "beta_eigenvalues": complex_rows(values_6),
            "relevant_directions": len(gravity_indices),
            "theta_gravity": theta_gravity,
        },
        "mass_augmented_blocks": {
            mapping: {
                "theta_mass": float(data["theta_mass"]),
                "uv_power": float(data["uv_power"]),
                "relevant_directions": int(data["relevant_count"]),
                "mass_eigenvector_x_u_per_unit_w": np.asarray(
                    data["mass_vector"][:6]
                ).tolist(),
                "beta_eigenvalues": complex_rows(data["values"]),
            }
            for mapping, data in mapping_data.items()
        },
        "Gaussian_gammaC2_scaling": {
            "fit_power": float(gaussian_power),
            "fit_abs_coefficient": gaussian_coefficient,
            "interpretation": "gamma_C2 approaches a g^2 source so u_O4/g^2 has a finite Gaussian Wilson limit in the executed scheme",
        },
        "trajectory_grid": {
            "relative_gravity_seeds": list(SEED_AMPLITUDES),
            "R_UV_values": list(R_UV_VALUES),
            "rows": len(family_rows),
            "O4_Wilson_seed_convergence": convergence,
        },
        "direct_trace_cancellation_contract": {
            "fixed_point_equation": "0=4u_star-gamma_C2_star/2+S_direct_star",
            "u_zero_condition": "S_direct_star=gamma_C2(u=0)_star/2",
            "required_numeric": direct_trace_required_for_zero,
            "proportional_comparator": "if S_direct(t)=xi gamma_C2_kernel(t)/2 pointwise and the same fixed trajectory is chosen, the kernel-forced O4 solution scales with 1-xi",
            "xi_zero": "kernel-owned branch executed here",
            "xi_one": "exact u_O4=0 cancellation branch",
        },
        "checks": checks,
        "claim_boundary": {
            "metric_kernel_O4_source_derived": True,
            "scalar_O4_C2_and_RC2_feedback_derived": True,
            "known_source_O4_fixed_point_solved": True,
            "known_source_O4_finite_family_integrated": True,
            "u_O4_zero_invariant_in_known_source_system": False,
            "direct_gravity_mixed_RHS_trace_derived": False,
            "full_O4_parent_fixed_point": False,
            "physical_PPN_Maxwell_residual_derived": False,
            "full_MTS_fixed_point": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    write_csv(SPECTRUM_CSV, spectrum_rows)
    write_csv(FAMILY_CSV, family_rows)
    write_csv(SOURCE_CSV, source_rows)
    write_csv(GAUSSIAN_CSV, gaussian_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    failed_checks = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_FIXED={fixed_state.tolist()}", flush=True)
    print(f"{MARKER}_GAMMA_C2={fixed_gamma_c2:.12e}", flush=True)
    print(f"{MARKER}_KERNEL_SOURCE={kernel_source_at_zero:.12e}", flush=True)
    print(f"{MARKER}_GAUSSIAN_POWER={gaussian_power:.12f}", flush=True)
    print(f"{MARKER}_FAMILY_ROWS={len(family_rows)}", flush=True)
    print(f"{MARKER}_FAILED_CHECKS={failed_checks}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed_checks:
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
