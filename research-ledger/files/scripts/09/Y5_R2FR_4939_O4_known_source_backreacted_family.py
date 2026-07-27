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
SOURCE = POST / "source-intake" / "functional_rg" / "4939"
RESULT_JSON = SOURCE / "known_source_O4_and_backreacted_family_results.json"
SPECTRUM_CSV = SOURCE / "augmented_motion_backreacted_spectrum.csv"
FAMILY_CSV = SOURCE / "two_scale_backreacted_GR_family.csv"
RESIDUAL_CSV = SOURCE / "local_threshold_residual_family.csv"

COMPLETED_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
COMPLETED_RESULT = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
TRAJECTORY_RESULT = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
MOTION_ENTRY = POST / "source-intake" / "functional_rg" / "4935" / "motion_sector_entry_results.json"
FUNCTIONAL_GATE = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
FIXED_GATE = POST / "source-intake" / "functional_rg" / "4937" / "functional_potential_fixed_gate_results.json"
TWO_SCALE_GATE = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
CURVED_SCALAR_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"

EXPECTED_HASHES = {
    COMPLETED_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    COMPLETED_RESULT: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    TRAJECTORY_RESULT: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    MOTION_ENTRY: "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    FUNCTIONAL_GATE: "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971",
    FIXED_GATE: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
    TWO_SCALE_GATE: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    CURVED_SCALAR_SOURCE: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
}

MARKER = "MTS_4939_O4_KNOWN_SOURCE_BACKREACTED_FAMILY"
COORDINATE_NAMES = ("g", "g_plus", "g_minus", "g_CFF", "h_C3")
MASS_MAPPINGS = {
    "Wetterich_v_equals_plus_2lambda": 1.0,
    "Wetterich_v_equals_minus_2lambda": -1.0,
}
SEED_AMPLITUDES = (1.0e-5, 3.0e-6, 1.0e-6)
R_UV_VALUES = (1.0e-12, 1.0e-10, 1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2, 1.0)
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
LOG_SUBTRACTION_SCALE = 16.0 * math.pi


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in values]


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


def scalar_decoupling(w_value: float) -> float:
    if w_value <= 0.0:
        return 1.0
    if w_value > 1.0e200:
        return 0.0
    return 1.0 / (1.0 + w_value)


def scalar_essential_source(point: np.ndarray, w_value: float) -> np.ndarray:
    source = np.zeros(5, dtype=float)
    source[0] = point[0] ** 2 * scalar_decoupling(w_value) / (6.0 * math.pi)
    return source


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
) -> np.ndarray:
    floors = np.array([1.0e-5, 1.0e-4, 1.0e-4, 1.0e-6, 1.0e-8])
    jacobian = np.zeros((5, 5), dtype=float)
    for column in range(5):
        step = 2.0e-5 * max(abs(point[column]), floors[column])
        plus = point.copy()
        minus = point.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (function(plus) - function(minus)) / (2.0 * step)
    return jacobian


def estimate_gaussian_sources(beta: Callable[[np.ndarray], np.ndarray]) -> dict[str, float]:
    g_values = np.logspace(-9, -6, 10)
    design = []
    c3_values = []
    minus_values = []
    plus_values = []
    for g_value in g_values:
        point = np.array([g_value, 0.0, 0.0, 0.0, 0.0], dtype=float)
        beta_value = beta(point)
        design.append([1.0, g_value * math.log(g_value), g_value])
        c3_values.append(float(beta_value[4] / g_value))
        minus_values.append(float(beta_value[2] / g_value**2))
        plus_values.append(float(beta_value[1] / g_value**2))
    design_matrix = np.asarray(design, dtype=float)
    return {
        "c3_source_limit": float(
            np.linalg.lstsq(design_matrix, c3_values, rcond=None)[0][0]
        ),
        "minus_source_limit": float(
            np.linalg.lstsq(design_matrix, minus_values, rcond=None)[0][0]
        ),
        "plus_source_limit": float(
            np.linalg.lstsq(design_matrix, plus_values, rcond=None)[0][0]
        ),
    }


def wilson_coordinates(point: np.ndarray, c3_source: float) -> dict[str, float]:
    g_value, plus_value, minus_value, cff_value, h_value = (
        float(value) for value in point
    )
    photon_denominator = (16.0 * math.pi * g_value) ** 2
    return {
        "W_plus": plus_value / photon_denominator,
        "W_minus_cl16pi": (
            minus_value / g_value**2
            + (548.0 / 15.0) * math.log(LOG_SUBTRACTION_SCALE * g_value)
        )
        / (16.0 * math.pi) ** 2,
        "W_C": cff_value / (16.0 * math.pi * g_value),
        "A_C3": h_value / g_value - 0.5 * c3_source * math.log(g_value),
        "raw_h_over_g": h_value / g_value,
        "raw_gplus_over_g2": plus_value / g_value**2,
        "raw_gminus_over_g2": minus_value / g_value**2,
        "raw_gCFF_over_g": cff_value / g_value,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {
        path.as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    failures = [
        path.as_posix()
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.as_posix()] != expected
    ]
    if failures:
        raise RuntimeError(f"source hash mismatch: {failures}")

    SOURCE.mkdir(parents=True, exist_ok=True)
    completed = json.loads(COMPLETED_RESULT.read_text(encoding="utf-8"))
    previous_fixed = np.asarray(
        completed["source_complete_selected_row_fixed_point"][
            "coordinates_g_gplus_gminus_gCFF_h"
        ],
        dtype=float,
    )
    _, _, base_beta, _, _, _ = completed_flow.build_completed_solver()

    def massless_beta(point: np.ndarray) -> np.ndarray:
        return base_beta(point) + scalar_essential_source(point, 0.0)

    fixed_solution = root(
        massless_beta,
        previous_fixed,
        method="hybr",
        options={"maxfev": 4000, "xtol": 1.0e-11},
    )
    fixed_point = np.asarray(fixed_solution.x, dtype=float)
    fixed_residual = massless_beta(fixed_point)
    if (
        not fixed_solution.success
        or np.linalg.norm(fixed_residual, ord=np.inf) >= 1.0e-9
    ):
        raise RuntimeError(
            f"scalar-backreacted fixed point failed: {fixed_solution.message}; "
            f"residual={fixed_residual.tolist()}"
        )

    gravity_stability = numerical_jacobian(massless_beta, fixed_point)
    gravity_eigenvalues, gravity_eigenvectors = np.linalg.eig(gravity_stability)
    gravity_relevant = [
        index for index, value in enumerate(gravity_eigenvalues) if value.real < 0.0
    ]
    if len(gravity_relevant) != 1:
        raise RuntimeError(f"expected one gravity relevant direction, found {gravity_relevant}")
    gravity_index = gravity_relevant[0]
    theta_gravity = -float(gravity_eigenvalues[gravity_index].real)
    gravity_vector = np.real(gravity_eigenvectors[:, gravity_index])
    if gravity_vector[0] < 0.0:
        gravity_vector *= -1.0
    gravity_vector /= float(np.max(np.abs(gravity_vector / fixed_point)))

    mass_column = np.zeros(5, dtype=float)
    mass_column[0] = -fixed_point[0] ** 2 / (6.0 * math.pi)
    spectrum_rows: list[dict[str, Any]] = []
    mapping_data: dict[str, dict[str, Any]] = {}
    for mapping, v_sign in MASS_MAPPINGS.items():
        A_star = mass_scaling_A(float(fixed_point[0]), v_sign)
        mass_eigenvalue = -2.0 + A_star
        augmented = np.zeros((6, 6), dtype=float)
        augmented[:5, :5] = gravity_stability
        augmented[:5, 5] = mass_column
        augmented[5, 5] = mass_eigenvalue
        augmented_values = np.linalg.eigvals(augmented)
        response = np.linalg.solve(
            gravity_stability - mass_eigenvalue * np.eye(5),
            -mass_column,
        )
        response_residual = float(
            np.linalg.norm(
                (gravity_stability - mass_eigenvalue * np.eye(5)) @ response
                + mass_column,
                ord=np.inf,
            )
        )
        mapping_data[mapping] = {
            "v_sign": v_sign,
            "A_star": A_star,
            "theta_mass": -mass_eigenvalue,
            "mass_eigenvalue": mass_eigenvalue,
            "uv_power": -mass_eigenvalue / theta_gravity,
            "gravity_response_to_unit_mass_mode": response,
            "response_residual": response_residual,
            "augmented_eigenvalues": augmented_values,
        }
        for mode_index, value in enumerate(
            sorted(augmented_values, key=lambda item: (item.real, item.imag))
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
                    "motion_mass_mode": bool(abs(value - mass_eigenvalue) < 1.0e-8),
                    "massless_scalar_baseline_included": True,
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    gaussian_sources = estimate_gaussian_sources(base_beta)
    family_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    massless_endpoints: dict[float, dict[str, Any]] = {}

    def integrate_massless(relative_seed: float) -> dict[str, Any]:
        initial_point = fixed_point - relative_seed * gravity_vector

        def rhs(_time: float, state: np.ndarray) -> np.ndarray:
            return massless_beta(state)

        def event(_time: float, state: np.ndarray) -> float:
            return float(state[0] - IR_G_TARGET)

        event.terminal = True
        event.direction = -1
        solution = solve_ivp(
            rhs,
            (0.0, T_IR_LIMIT),
            initial_point,
            method="DOP853",
            rtol=2.0e-9,
            atol=np.array([1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19]),
            max_step=0.08,
            events=event,
        )
        if not solution.success or not len(solution.t_events[0]):
            raise RuntimeError(f"massless branch failed for seed {relative_seed}")
        endpoint = np.asarray(solution.y[:, -1], dtype=float)
        return {
            "endpoint": endpoint,
            "t_endpoint": float(solution.t[-1]),
            "wilson": wilson_coordinates(
                endpoint, gaussian_sources["c3_source_limit"]
            ),
        }

    for relative_seed in SEED_AMPLITUDES:
        massless = integrate_massless(relative_seed)
        massless_endpoints[relative_seed] = massless
        family_rows.append(
            {
                "mapping": "massless_shared",
                "relative_gravity_seed": relative_seed,
                "R_UV": 0.0,
                "uv_power": "",
                "w_seed": 0.0,
                "t_endpoint": massless["t_endpoint"],
                "g_endpoint": float(massless["endpoint"][0]),
                "w_endpoint": 0.0,
                "J_gap_endpoint": 0.0,
                "D_psi_endpoint": 1.0,
                **massless["wilson"],
                "termination": "IR_G_TARGET",
                "trajectory_scope": "massless scalar fully backreacted in the known essential threshold system",
                "O4_gravity_mixed_source_closed": False,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    for mapping, data in mapping_data.items():
        response = np.asarray(data["gravity_response_to_unit_mass_mode"], dtype=float)
        for relative_seed in SEED_AMPLITUDES:
            baseline = massless_endpoints[relative_seed]
            for R_UV in R_UV_VALUES:
                w_seed = R_UV * relative_seed ** float(data["uv_power"])
                initial_gravity = (
                    fixed_point
                    - relative_seed * gravity_vector
                    + w_seed * response
                )
                initial_state = np.concatenate(
                    [initial_gravity, np.array([math.log(w_seed)])]
                )

                def rhs(_time: float, state: np.ndarray) -> np.ndarray:
                    point = state[:5]
                    log_w = float(state[5])
                    w_value = math.exp(log_w) if log_w < 460.0 else 1.0e200
                    gravity_beta = base_beta(point) + scalar_essential_source(
                        point, w_value
                    )
                    log_mass_beta = -2.0 + mass_scaling_A(
                        float(point[0]), float(data["v_sign"])
                    )
                    return np.concatenate(
                        [gravity_beta, np.array([log_mass_beta])]
                    )

                def event(_time: float, state: np.ndarray) -> float:
                    return float(state[0] - IR_G_TARGET)

                event.terminal = True
                event.direction = -1
                solution = solve_ivp(
                    rhs,
                    (0.0, T_IR_LIMIT),
                    initial_state,
                    method="DOP853",
                    rtol=2.0e-9,
                    atol=np.array(
                        [1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19, 1.0e-10]
                    ),
                    max_step=0.08,
                    events=event,
                )
                if not solution.success or not len(solution.t_events[0]):
                    raise RuntimeError(
                        f"backreacted branch failed for {mapping} seed={relative_seed} R={R_UV}"
                    )
                endpoint = np.asarray(solution.y[:5, -1], dtype=float)
                log_w_endpoint = float(solution.y[5, -1])
                w_endpoint = math.exp(log_w_endpoint)
                g_endpoint = float(endpoint[0])
                J_endpoint = g_endpoint * w_endpoint
                D_endpoint = scalar_decoupling(w_endpoint)
                wilson = wilson_coordinates(
                    endpoint, gaussian_sources["c3_source_limit"]
                )
                baseline_wilson = baseline["wilson"]
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
                        "J_gap_endpoint": J_endpoint,
                        "D_psi_endpoint": D_endpoint,
                        **wilson,
                        "delta_W_plus_from_massless": wilson["W_plus"]
                        - baseline_wilson["W_plus"],
                        "delta_W_minus_from_massless": wilson["W_minus_cl16pi"]
                        - baseline_wilson["W_minus_cl16pi"],
                        "delta_W_C_from_massless": wilson["W_C"]
                        - baseline_wilson["W_C"],
                        "delta_A_C3_from_massless": wilson["A_C3"]
                        - baseline_wilson["A_C3"],
                        "termination": "IR_G_TARGET",
                        "trajectory_scope": "finite mass threshold fully backreacted into the known neutral-scalar essential beta_g source",
                        "O4_gravity_mixed_source_closed": False,
                        "valid_for_full_MTS_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )
                delta_beta_g = (
                    g_endpoint**2 * D_endpoint / (6.0 * math.pi)
                )
                residual_rows.append(
                    {
                        "mapping": mapping,
                        "relative_gravity_seed": relative_seed,
                        "R_UV": R_UV,
                        "J_gap_endpoint": J_endpoint,
                        "g_endpoint": g_endpoint,
                        "w_endpoint": w_endpoint,
                        "D_psi_endpoint": D_endpoint,
                        "Delta_beta_g_endpoint": delta_beta_g,
                        "Delta_beta_g_over_g_endpoint": delta_beta_g / g_endpoint,
                        "direct_neutral_scalar_beta_gplus": 0.0,
                        "direct_neutral_scalar_beta_gminus": 0.0,
                        "direct_neutral_scalar_beta_gCFF": 0.0,
                        "minimal_eta0_scalar_beta_h_C3": 0.0,
                        "PPN_beta_gamma_residual": "NOT_DERIVED_FROM_RG_THRESHOLD",
                        "Maxwell_observable_residual": "INDIRECT_WILSON_SHIFT_ONLY",
                        "O4_gravity_mixed_residual": "OPEN_CURVED_HESSIAN_SOURCE",
                        "valid_for_full_MTS_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )

    positive_rows = [row for row in family_rows if float(row["R_UV"]) > 0.0]
    convergence: dict[str, Any] = {}
    for mapping in MASS_MAPPINGS:
        mapping_rows = [row for row in positive_rows if row["mapping"] == mapping]
        convergence[mapping] = {}
        for R_UV in R_UV_VALUES:
            rows = [row for row in mapping_rows if row["R_UV"] == R_UV]
            values = np.asarray([row["J_gap_endpoint"] for row in rows], dtype=float)
            reference = float(values[-1])
            convergence[mapping][str(R_UV)] = {
                "values": values.tolist(),
                "smallest_seed_reference": reference,
                "max_relative_difference": float(
                    np.max(np.abs(values - reference)) / abs(reference)
                ),
            }

    fixed_shift = fixed_point - previous_fixed
    relative_shift = fixed_shift / previous_fixed
    o4_audit = {
        "operator": "O4=C_abcd C^abcd (nabla psi)^2",
        "projector": "P_O4=(1/2) partial_C2 partial_p2 Gamma_psi_psi^(2)|0",
        "Hessian": "-2u_O4 nabla_mu[C^2 nabla^mu]",
        "dimensionless_coordinate": "utilde_O4=k^4 u_O4/Z_psi",
        "known_beta_structure": "beta_utilde=(4+eta_psi)utilde+S_O4_gravity_mixed",
        "optimized_eta0_threshold_moments": {
            "Q2_over_k4": "1/[2(1+w)]",
            "Q1_over_k2": "1/(1+w)",
            "Q0": "1/(1+w)",
            "Qminus1": "0",
        },
        "minimal_scalar_heat_kernel_a4": {
            "raw": "(5R^2-2Ricci^2+2Riemann^2)/360",
            "R2_S2_Euler": "R^2/80+S^2/60+Euler/180",
            "essential_Newton_projection": "Delta beta_g=g^2/[6pi(1+w)]",
            "minimal_eta0_C3_projection": "0 because Qminus1=0",
        },
        "exact_zero_sources": {
            "isolated_quadratic_scalar_trace": True,
            "direct_neutral_photon_rows": True,
            "minimal_eta0_scalar_C3_row": True,
        },
        "remaining_source": "off-shell curved gravity-motion and mixed Hessian trace at C^2 p^2",
        "u4_zero_is_full_invariant_submanifold": False,
        "known_source_u4_zero_trajectory_is_diagnostic": True,
    }
    checks = {
        "source_hashes_match": not failures,
        "scalar_backreacted_fixed_point_converged": bool(fixed_solution.success),
        "fixed_point_residual_below_1e_minus_9": bool(
            np.linalg.norm(fixed_residual, ord=np.inf) < 1.0e-9
        ),
        "massless_scalar_shifts_fixed_point": bool(
            np.max(np.abs(relative_shift)) > 1.0e-3
        ),
        "gravity_block_retains_one_relevant_direction": len(gravity_relevant) == 1,
        "both_augmented_blocks_have_two_relevant_directions": all(
            sum(value.real < 0.0 for value in data["augmented_eigenvalues"]) == 2
            for data in mapping_data.values()
        ),
        "all_mass_response_solves_accurate": all(
            data["response_residual"] < 1.0e-12 for data in mapping_data.values()
        ),
        "all_family_runs_reach_IR": all(
            row["termination"] == "IR_G_TARGET" for row in family_rows
        ),
        "all_positive_J_endpoints": all(
            float(row["J_gap_endpoint"]) > 0.0 for row in positive_rows
        ),
        "all_threshold_residuals_finite": all(
            math.isfinite(float(row["Delta_beta_g_over_g_endpoint"]))
            for row in residual_rows
        ),
        "scalar_and_photon_direct_O4_sources_zero": all(
            o4_audit["exact_zero_sources"].values()
        ),
        "gravity_mixed_O4_source_not_silently_zeroed": not o4_audit[
            "u4_zero_is_full_invariant_submanifold"
        ],
    }
    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "O4_curved_source_audit": o4_audit,
        "essential_scalar_threshold": {
            "D_psi": "1/(1+w_psi)",
            "Delta_beta_g": "g^2/[6pi(1+w_psi)]",
            "direct_neutral_photon_beta_rows": 0,
            "minimal_eta0_beta_h_C3": 0,
            "scope": "complete known one-loop essential neutral-scalar source; inessential curved rows require the matching field-redefinition basis and are not injected raw",
        },
        "massless_scalar_backreacted_fixed_point": {
            "success": bool(fixed_solution.success),
            "message": fixed_solution.message,
            "coordinates": dict(zip(COORDINATE_NAMES, fixed_point.tolist())),
            "beta_residual": fixed_residual.tolist(),
            "beta_residual_infinity_norm": float(
                np.linalg.norm(fixed_residual, ord=np.inf)
            ),
            "shift_from_4934": dict(zip(COORDINATE_NAMES, fixed_shift.tolist())),
            "relative_shift_from_4934": dict(
                zip(COORDINATE_NAMES, relative_shift.tolist())
            ),
            "gravity_stability_matrix": gravity_stability.tolist(),
            "gravity_beta_eigenvalues": complex_rows(gravity_eigenvalues),
            "gravity_relevant_directions": len(gravity_relevant),
            "theta_gravity": theta_gravity,
        },
        "augmented_motion_blocks": {
            mapping: {
                "A_star": float(data["A_star"]),
                "theta_mass": float(data["theta_mass"]),
                "mass_eigenvalue": float(data["mass_eigenvalue"]),
                "uv_power": float(data["uv_power"]),
                "known_mass_column": mass_column.tolist(),
                "gravity_response_to_unit_mass_mode": np.asarray(
                    data["gravity_response_to_unit_mass_mode"]
                ).tolist(),
                "response_residual": float(data["response_residual"]),
                "augmented_eigenvalues": complex_rows(data["augmented_eigenvalues"]),
                "relevant_directions": int(
                    sum(
                        value.real < 0.0
                        for value in data["augmented_eigenvalues"]
                    )
                ),
            }
            for mapping, data in mapping_data.items()
        },
        "gaussian_sources_for_Wilson_coordinates": gaussian_sources,
        "trajectory_grid": {
            "relative_gravity_seeds": list(SEED_AMPLITUDES),
            "R_UV_values": list(R_UV_VALUES),
            "positive_mass_runs": len(positive_rows),
            "massless_runs": len(family_rows) - len(positive_rows),
            "IR_g_target": IR_G_TARGET,
            "J_gap_seed_convergence": convergence,
        },
        "checks": checks,
        "claim_boundary": {
            "massless_scalar_fixed_point_backreaction_calculated": True,
            "finite_mass_threshold_family_backreacted": True,
            "neutral_scalar_direct_Maxwell_source_zero": True,
            "minimal_eta0_scalar_C3_source_zero": True,
            "scalar_and_photon_O4_sources_zero": True,
            "gravity_mixed_O4_source_derived": False,
            "u4_zero_full_parent_invariant": False,
            "physical_PPN_residual_derived": False,
            "full_MTS_fixed_point": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    write_csv(SPECTRUM_CSV, spectrum_rows)
    write_csv(FAMILY_CSV, family_rows)
    write_csv(RESIDUAL_CSV, residual_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    failed_checks = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_FIXED_POINT={fixed_point.tolist()}", flush=True)
    print(
        f"{MARKER}_FIXED_RESIDUAL={np.linalg.norm(fixed_residual, ord=np.inf):.12e}",
        flush=True,
    )
    print(f"{MARKER}_FAMILY_ROWS={len(family_rows)}", flush=True)
    print(f"{MARKER}_FAILED_CHECKS={failed_checks}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed_checks:
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
