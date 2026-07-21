from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq, root

import Y5_R2FR_4933_c3_direct_threshold_solver as c3
import Y5_R2FR_4933_photon_flow_reproduction as photon


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4933"
OUTPUT_JSON = SOURCE_DIR / "combined_c3_photon_stability_results.json"
MARKER = "MTS_4933_COMBINED_C3_PHOTON_STABILITY"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in values]


def photon_fixed_point(
    photon_system: tuple[sp.Matrix, sp.Matrix, dict[str, object]] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    matrix, vector, _ = photon_system if photon_system is not None else photon.build_system()
    solve_raw = photon.numerical_solver(matrix, vector)

    def solve(point: np.ndarray) -> tuple[np.ndarray, float]:
        return solve_raw(photon.essential_to_raw(point))

    def beta(point: np.ndarray) -> np.ndarray:
        try:
            return photon.beta_coordinates(solve(point)[0])
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return np.full(4, 1e30)

    solution = root(beta, photon.FP1, method="hybr", options={"maxfev": 3000, "xtol": 1e-11})
    if not solution.success or np.linalg.norm(beta(solution.x), ord=np.inf) > 1e-8:
        raise RuntimeError(f"photon fixed point failed: {solution.message}")
    unknowns, condition = solve(solution.x)
    stability, exponents = photon.stability(solve, solution.x)
    return solution.x, unknowns, stability, exponents, condition


def photon_matter_curvature_vector(cff_value: float, gamma_a: float, gamma_df: float) -> np.ndarray:
    pi2 = math.pi**2

    def regulator(x_value: float) -> float:
        return 1 - x_value

    def y_factor(x_value: float) -> float:
        return -(1 + gamma_a - gamma_df * x_value) * regulator(x_value) - x_value

    matter_1 = quad(
        lambda value: -value
        * (((-4 - 4 * gamma_a + 3 * gamma_df * value) * regulator(value)) - 4 * value)
        / (16 * pi2)
        - value / (8 * pi2),
        0,
        1,
        epsabs=1e-14,
    )[0]
    matter_r = quad(
        lambda value: (((-2 - 2 * gamma_a + 3 * gamma_df * value) * regulator(value)) - 2 * value)
        / (96 * pi2)
        - 1 / (48 * pi2),
        0,
        1,
        epsabs=1e-14,
    )[0]
    common = lambda value: cff_value * value * (-1 + 2 * cff_value * value**2) * y_factor(value)
    matter_r2 = -1 / (640 * pi2) + (1 + gamma_a) / (1920 * pi2)
    matter_r2 += quad(lambda value: common(value) / (48 * pi2), 0, 1, epsabs=1e-14)[0]
    matter_s2 = -1 / (480 * pi2) + 7 * (1 + gamma_a) / (480 * pi2)
    matter_s2 += quad(lambda value: -common(value) / (4 * pi2), 0, 1, epsabs=1e-14)[0]
    matter_euler = -1 / (1440 * pi2) - 11 * (1 + gamma_a) / (2880 * pi2)
    matter_euler += quad(lambda value: -common(value) / (8 * pi2), 0, 1, epsabs=1e-14)[0]
    vector = np.zeros(13, dtype=float)
    vector[0] = matter_1
    vector[1] = matter_r
    vector[2] = matter_r2 + matter_euler / 6
    vector[3] = matter_s2 - 2 * matter_euler
    vector[4] = matter_euler
    return vector


def frozen_photon_c3_fixed_point(
    photon_point: np.ndarray,
    photon_unknowns: np.ndarray,
    seed_h: float,
    principal_c3_projection: float,
    principal_c3_projection_derivative: float,
    c3_system: tuple[sp.Matrix, sp.Matrix, dict[str, object]] | None = None,
) -> dict[str, object]:
    matrix, vector, _ = c3_system if c3_system is not None else c3.build_linear_system()
    matrix_function = sp.lambdify((c3.g, c3.h, c3.rho), matrix, modules="numpy", cse=True)
    vector_function = sp.lambdify((c3.g, c3.h, c3.rho), vector, modules="numpy", cse=True)
    rho_value = 1 / (4 * math.pi)
    matter = photon_matter_curvature_vector(
        float(photon_point[3]), float(photon_unknowns[10]), float(photon_unknowns[11])
    )
    maxwell_c6 = 1 / (15120 * (4 * math.pi) ** 2)
    maxwell_qminus1_combination = 4 * float(photon_unknowns[10]) + 3 * float(photon_unknowns[11])
    maxwell_minimal_a6_projection = -maxwell_c6 * maxwell_qminus1_combination
    matter[10] = principal_c3_projection + maxwell_minimal_a6_projection

    def solve(point: np.ndarray) -> tuple[np.ndarray, float]:
        g_value, h_value = (float(value) for value in point)
        numeric_matrix = np.asarray(matrix_function(g_value, h_value, rho_value), dtype=float)
        numeric_vector = np.asarray(vector_function(g_value, h_value, rho_value), dtype=float).reshape(13) + matter
        return np.linalg.solve(numeric_matrix, numeric_vector), float(np.linalg.cond(numeric_matrix))

    def beta(point: np.ndarray) -> np.ndarray:
        try:
            return solve(point)[0][:2]
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return np.full(2, 1e30)

    solution = root(beta, np.array([photon_point[0], seed_h]), method="hybr", options={"maxfev": 2000})
    unknowns, condition = solve(solution.x)
    fixed_matrix = np.asarray(matrix_function(float(solution.x[0]), float(solution.x[1]), rho_value), dtype=float)
    projection_to_beta_h = float(np.linalg.inv(fixed_matrix)[1, 10])
    principal_partial_beta_h_partial_cff = projection_to_beta_h * principal_c3_projection_derivative
    jacobian = np.zeros((2, 2), dtype=float)
    for column in range(2):
        step = max(abs(solution.x[column]) * 2e-5, 1e-8 if column == 0 else 1e-11)
        plus = solution.x.copy()
        minus = solution.x.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (beta(plus) - beta(minus)) / (2 * step)
    photon_g = float(photon_point[0])

    def conditional_beta_h(h_value: float) -> float:
        return float(solve(np.array([photon_g, h_value]))[0][1])

    conditional_h = brentq(conditional_beta_h, -1e-4, 1e-4, xtol=1e-16, rtol=1e-14)
    conditional_unknowns, conditional_condition = solve(np.array([photon_g, conditional_h]))
    conditional_h_step = max(abs(conditional_h) * 2e-5, 1e-11)
    conditional_g_step = max(abs(photon_g) * 2e-5, 1e-7)
    conditional_lambda_h = (
        conditional_beta_h(conditional_h + conditional_h_step)
        - conditional_beta_h(conditional_h - conditional_h_step)
    ) / (2 * conditional_h_step)
    conditional_partial_g = (
        solve(np.array([photon_g + conditional_g_step, conditional_h]))[0][1]
        - solve(np.array([photon_g - conditional_g_step, conditional_h]))[0][1]
    ) / (2 * conditional_g_step)
    conditional_matrix = np.asarray(matrix_function(photon_g, conditional_h, rho_value), dtype=float)
    conditional_projection_response = float(np.linalg.inv(conditional_matrix)[1, 10])
    conditional_principal_cff_derivative = conditional_projection_response * principal_c3_projection_derivative
    return {
        "success": bool(solution.success and np.linalg.norm(beta(solution.x), ord=np.inf) < 1e-8),
        "message": str(solution.message),
        "g": float(solution.x[0]),
        "h": float(solution.x[1]),
        "beta_residual": beta(solution.x).tolist(),
        "critical_exponents": complex_rows(-np.linalg.eigvals(jacobian)),
        "stability_matrix": jacobian.tolist(),
        "linear_condition_number": condition,
        "photon_matter_projection_1_R_R2_S2_C2": matter[:5].tolist(),
        "principal_C3_RHS_projection": principal_c3_projection,
        "minimal_Maxwell_a6": {
            "massive_vector_c1": 1 / (10080 * (4 * math.pi) ** 2),
            "minimal_scalar_c1": 1 / (30240 * (4 * math.pi) ** 2),
            "massless_Maxwell_c6_difference": maxwell_c6,
            "Qminus1_kernel_combination": maxwell_qminus1_combination,
            "C3_RHS_projection": maxwell_minimal_a6_projection,
            "formula": "-[1/(15120(4pi)^2)]*(4 gamma_a+3 gamma_DF)",
        },
        "C3_projection_to_beta_h_response": projection_to_beta_h,
        "principal_partial_beta_h_partial_g_CFF": principal_partial_beta_h_partial_cff,
        "photon_coordinates_and_gammas_frozen": True,
        "principal_photon_CFF3_C3_term_included": True,
        "minimal_photon_a6_C3_term_included": True,
        "complete_portal_dependent_photon_a6_C3_term_included": False,
        "reverse_C3_to_photon_block_included": False,
        "conditional_h_at_photon_fixed_g": {
            "g": photon_g,
            "h": conditional_h,
            "beta_g_from_combined_gravity_projection": float(conditional_unknowns[0]),
            "beta_h": float(conditional_unknowns[1]),
            "partial_beta_h_partial_h": float(conditional_lambda_h),
            "partial_beta_h_partial_g": float(conditional_partial_g),
            "principal_partial_beta_h_partial_g_CFF": conditional_principal_cff_derivative,
            "linear_condition_number": conditional_condition,
        },
    }


def c3_vertical_nullcline(
    g_value: float,
    c3_system: tuple[sp.Matrix, sp.Matrix, dict[str, object]] | None = None,
) -> dict[str, object]:
    matrix, vector, _ = c3_system if c3_system is not None else c3.build_linear_system()
    solve = c3.numerical_solver(matrix, vector)
    rho_value = 1 / (4 * math.pi)

    def beta_h(h_value: float) -> float:
        return float(solve(g_value, h_value, rho_value)[0][1])

    h_value = brentq(beta_h, -1e-5, 0.0, xtol=1e-16, rtol=1e-14)
    unknowns, condition = solve(g_value, h_value, rho_value)
    h_step = max(abs(h_value) * 2e-5, 1e-11)
    g_step = max(abs(g_value) * 2e-5, 1e-7)
    lambda_h = (beta_h(h_value + h_step) - beta_h(h_value - h_step)) / (2 * h_step)
    derivative_h_g = (
        solve(g_value + g_step, h_value, rho_value)[0][1]
        - solve(g_value - g_step, h_value, rho_value)[0][1]
    ) / (2 * g_step)
    return {
        "g": g_value,
        "h": h_value,
        "beta_g_from_pure_c3_block": float(unknowns[0]),
        "beta_h": float(unknowns[1]),
        "lambda_h_partial_h": float(lambda_h),
        "partial_beta_h_partial_g": float(derivative_h_g),
        "linear_condition_number": condition,
        "rho": "1/(4*pi)",
    }


def principal_cff_to_c3(cff_value: float) -> dict[str, float | str]:
    quadratic_notebook_coefficient = 1 / (16 * math.pi**2)
    uncalibrated_quadratic_coefficient = 1 / (4 * math.pi**2)
    polarization_calibration = quadratic_notebook_coefficient / uncalibrated_quadratic_coefficient
    beta_h_cubic_coefficient = polarization_calibration * 64 / (16 * math.pi**2 * 5)
    beta_h_term = beta_h_cubic_coefficient * cff_value**3
    derivative = 3 * beta_h_cubic_coefficient * cff_value**2
    return {
        "K_two_form": "I-4*g_CFF*C",
        "notebook_CFF2_coefficient": quadratic_notebook_coefficient,
        "raw_two_form_CFF2_coefficient": uncalibrated_quadratic_coefficient,
        "polarization_calibration": polarization_calibration,
        "principal_C3_RHS_projection_term": beta_h_term,
        "principal_C3_RHS_projection_derivative": derivative,
        "status": "EXACT_WITHIN_CONSTANT_WEYL_PRINCIPAL_SYMBOL_NOT_COMPLETE_A6",
    }


def photon_matter_affine_c3_projection(cff_value: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    constant = photon_matter_curvature_vector(cff_value, 0.0, 0.0)
    gamma_a_coefficient = photon_matter_curvature_vector(cff_value, 1.0, 0.0) - constant
    gamma_df_coefficient = photon_matter_curvature_vector(cff_value, 0.0, 1.0) - constant
    maxwell_c6 = 1 / (15120 * (4 * math.pi) ** 2)
    constant[10] += float(principal_cff_to_c3(cff_value)["principal_C3_RHS_projection_term"])
    gamma_a_coefficient[10] -= 4 * maxwell_c6
    gamma_df_coefficient[10] -= 3 * maxwell_c6
    return constant, gamma_a_coefficient, gamma_df_coefficient


def partial_combined_common_zero(
    c3_system: tuple[sp.Matrix, sp.Matrix, dict[str, object]],
    photon_system: tuple[sp.Matrix, sp.Matrix, dict[str, object]],
    seed: np.ndarray,
) -> dict[str, object]:
    c3_matrix, c3_vector, _ = c3_system
    photon_matrix, photon_vector, _ = photon_system
    c3_matrix_function = sp.lambdify((c3.g, c3.h, c3.rho), c3_matrix, modules="numpy", cse=True)
    c3_vector_function = sp.lambdify((c3.g, c3.h, c3.rho), c3_vector, modules="numpy", cse=True)
    photon_matrix_function = sp.lambdify(photon.COUPLINGS, photon_matrix, modules="numpy", cse=True)
    photon_vector_function = sp.lambdify(photon.COUPLINGS, photon_vector, modules="numpy", cse=True)
    rho_value = 1 / (4 * math.pi)
    photon_to_combined_columns = (0, 2, 13, 14, 15, 3, 4, 5, 16, 17, 18, 19)
    combined_names = [str(value) for value in c3.UNKNOWNS] + [
        "beta_f2sq",
        "beta_f4",
        "beta_cff",
        "gamma_ftrace",
        "gamma_ftl",
        "gamma_a",
        "gamma_df",
    ]

    def system(point: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        g_value, g_plus_value, g_minus_value, cff_value, h_value = (float(value) for value in point)
        raw_photon = (g_value, g_plus_value + g_minus_value, g_plus_value - g_minus_value, cff_value)
        numeric_c3_matrix = np.asarray(c3_matrix_function(g_value, h_value, rho_value), dtype=float)
        numeric_c3_vector = np.asarray(c3_vector_function(g_value, h_value, rho_value), dtype=float).reshape(13)
        numeric_photon_matrix = np.asarray(photon_matrix_function(*raw_photon), dtype=float)
        numeric_photon_vector = np.asarray(photon_vector_function(*raw_photon), dtype=float).reshape(12)
        matter_constant, matter_gamma_a, matter_gamma_df = photon_matter_affine_c3_projection(cff_value)

        matrix = np.zeros((20, 20), dtype=float)
        vector = np.zeros(20, dtype=float)
        matrix[:13, :13] = numeric_c3_matrix
        matrix[:13, 18] -= matter_gamma_a
        matrix[:13, 19] -= matter_gamma_df
        vector[:13] = numeric_c3_vector + matter_constant
        for photon_column, combined_column in enumerate(photon_to_combined_columns):
            matrix[13:, combined_column] = numeric_photon_matrix[5:, photon_column]
        vector[13:] = numeric_photon_vector[5:]
        return matrix, vector

    def solve(point: np.ndarray) -> tuple[np.ndarray, float, np.ndarray]:
        matrix, vector = system(point)
        unknowns = np.linalg.solve(matrix, vector)
        return unknowns, float(np.linalg.cond(matrix)), matrix

    def beta(point: np.ndarray) -> np.ndarray:
        try:
            unknowns = solve(point)[0]
            return beta_from_unknowns(unknowns)
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return np.full(5, 1e30)

    def beta_from_unknowns(unknowns: np.ndarray) -> np.ndarray:
        return np.array(
            [
                unknowns[0],
                (unknowns[13] + unknowns[14]) / 2,
                (unknowns[13] - unknowns[14]) / 2,
                unknowns[15],
                unknowns[1],
            ],
            dtype=float,
        )

    solution = root(beta, seed, method="hybr", options={"maxfev": 4000, "xtol": 1e-11})
    residual = beta(solution.x)
    unknowns, condition, combined_matrix = solve(solution.x)
    jacobian = np.zeros((5, 5), dtype=float)
    for column in range(5):
        scale = max(abs(solution.x[column]), (1e-5, 1e-4, 1e-4, 1e-6, 1e-8)[column])
        step = 2e-5 * scale
        plus = solution.x.copy()
        minus = solution.x.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (beta(plus) - beta(minus)) / (2 * step)

    g_value, g_plus_value, g_minus_value, cff_value, _ = (float(value) for value in solution.x)
    raw_photon = (g_value, g_plus_value + g_minus_value, g_plus_value - g_minus_value, cff_value)
    numeric_photon_matrix = np.asarray(photon_matrix_function(*raw_photon), dtype=float)
    numeric_photon_vector = np.asarray(photon_vector_function(*raw_photon), dtype=float).reshape(12)
    photon_unknowns = np.array([unknowns[index] for index in photon_to_combined_columns], dtype=float)
    omitted_lower_residual = numeric_photon_matrix[:5] @ photon_unknowns - numeric_photon_vector[:5]
    eigenvalues, modes = np.linalg.eig(jacobian)
    inverse_jacobian = np.linalg.inv(jacobian)
    inverse_jacobian_norm = float(np.linalg.norm(inverse_jacobian, ord=2))
    signed_gap = float(min(abs(value.real) for value in eigenvalues))
    coordinate_shift = solution.x - seed
    relative_shift = coordinate_shift / seed

    def source_response(row: int) -> dict[str, object]:
        source = np.zeros(20, dtype=float)
        source[row] = 1.0
        unknown_response = np.linalg.solve(combined_matrix, source)
        beta_response = beta_from_unknowns(unknown_response)
        coordinate_response = -inverse_jacobian @ beta_response
        one_percent_scales = 0.01 * np.abs(solution.x)
        finite_thresholds = [
            one_percent_scales[index] / abs(coordinate_response[index])
            for index in range(5)
            if abs(coordinate_response[index]) > 0
        ]
        return {
            "combined_rhs_row": row,
            "beta_response_per_unit_projection": beta_response.tolist(),
            "fixed_point_coordinate_response_per_unit_projection": coordinate_response.tolist(),
            "linear_projection_magnitude_for_all_coordinate_shifts_below_one_percent": float(
                min(finite_thresholds)
            ),
        }

    photon_projection_names = ("F2", "FDeltaF", "RFF", "SFF", "F2sq", "F4", "CFF")
    direct_photon_responses = {
        name: source_response(13 + index) for index, name in enumerate(photon_projection_names)
    }
    a6_response = source_response(10)
    return {
        "success": bool(solution.success and np.linalg.norm(residual, ord=np.inf) < 1e-8),
        "message": str(solution.message),
        "coordinates_g_gplus_gminus_gCFF_h": solution.x.tolist(),
        "coordinate_shift_from_triangular_seed": coordinate_shift.tolist(),
        "relative_coordinate_shift_from_triangular_seed": relative_shift.tolist(),
        "beta_residual": residual.tolist(),
        "beta_residual_infinity_norm": float(np.linalg.norm(residual, ord=np.inf)),
        "linear_system_condition_number": condition,
        "stability_matrix": jacobian.tolist(),
        "beta_eigenvalues": complex_rows(eigenvalues),
        "critical_exponents": complex_rows(-eigenvalues),
        "signed_imaginary_axis_gap": signed_gap,
        "modal_matrix_condition_number": float(np.linalg.cond(modes)),
        "coordinate_basis_stability_matrix_2norm_gate": signed_gap / float(np.linalg.cond(modes)),
        "inverse_stability_matrix_2norm": inverse_jacobian_norm,
        "negative_inverse_stability_matrix": (-inverse_jacobian).tolist(),
        "linear_open_residual_shift_bound": f"norm(delta x)_2 <= {inverse_jacobian_norm}*norm(r_open)_2 + O(r_open^2)",
        "open_projection_linear_response": {
            "unknown_portal_a6_C3_row": a6_response,
            "direct_C3_Hessian_photon_rows": direct_photon_responses,
            "scope": "first-order source and fixed-point displacement map; not a nonlinear enclosure",
        },
        "signed_index": {
            "negative_real_parts": int(sum(value.real < 0 for value in eigenvalues)),
            "positive_real_parts": int(sum(value.real > 0 for value in eigenvalues)),
        },
        "combined_unknown_values": dict(zip(combined_names, (float(value) for value in unknowns))),
        "omitted_duplicate_photon_lower_projection_residual": omitted_lower_residual.tolist(),
        "omitted_duplicate_photon_lower_projection_infinity_norm": float(
            np.linalg.norm(omitted_lower_residual, ord=np.inf)
        ),
        "included": [
            "shared beta_g beta_Euler gamma_g gamma_R gamma_S",
            "exact C3 source Hessian in all vacuum curvature rows",
            "exact photon source rows F2 through CFF",
            "affine lower-curvature photon traces",
            "minimal Maxwell a6 C3 term",
            "constant-Weyl principal CFF3 C3 term",
        ],
        "omitted": [
            "linear and quadratic CFF-curvature a6 terms in beta_h",
            "direct C3 Hessian terms in the seven photon-background rows",
        ],
        "is_full_combined_fixed_point": False,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    photon_system = photon.build_system()
    c3_system = c3.build_linear_system()
    point, photon_unknowns, photon_matrix, photon_exponents, photon_condition = photon_fixed_point(photon_system)
    principal = principal_cff_to_c3(float(point[3]))
    c3_nullcline = c3_vertical_nullcline(float(point[0]), c3_system)
    frozen_combined = frozen_photon_c3_fixed_point(
        point,
        photon_unknowns,
        float(c3_nullcline["h"]),
        float(principal["principal_C3_RHS_projection_term"]),
        float(principal["principal_C3_RHS_projection_derivative"]),
        c3_system,
    )
    partial_seed = np.array([*point.tolist(), frozen_combined["conditional_h_at_photon_fixed_g"]["h"]])
    partial_combined = partial_combined_common_zero(c3_system, photon_system, partial_seed)

    photon_eigenvalues, photon_modes = np.linalg.eig(photon_matrix)
    inverse_modes = np.linalg.inv(photon_modes)
    conditional_h = frozen_combined["conditional_h_at_photon_fixed_g"]
    lambda_h = float(conditional_h["partial_beta_h_partial_h"])
    signed_gap = min(min(abs(value.real) for value in photon_eigenvalues), abs(lambda_h))

    c_coordinate = np.array(
        [
            float(conditional_h["partial_beta_h_partial_g"]),
            0.0,
            0.0,
            float(conditional_h["principal_partial_beta_h_partial_g_CFF"]),
        ],
        dtype=complex,
    )
    c_modal = c_coordinate @ photon_modes
    principal_modal_norm = float(np.linalg.norm(c_modal))
    triangular_matrix = np.zeros((5, 5), dtype=float)
    triangular_matrix[:4, :4] = photon_matrix
    triangular_matrix[4, :4] = c_coordinate.real
    triangular_matrix[4, 4] = lambda_h
    triangular_eigenvalues = np.linalg.eigvals(triangular_matrix)
    pairwise_reverse_tolerances = []
    for index, (eigenvalue, c_component) in enumerate(zip(photon_eigenvalues, c_modal)):
        tolerance = math.inf if abs(c_component) == 0 else abs(lambda_h * eigenvalue) / abs(c_component)
        pairwise_reverse_tolerances.append(
            {
                "mode": index,
                "photon_beta_eigenvalue": {"real": float(eigenvalue.real), "imag": float(eigenvalue.imag)},
                "cff_to_h_modal_component": {"real": float(c_component.real), "imag": float(c_component.imag)},
                "max_reverse_modal_component_from_product_gate": tolerance,
            }
        )

    result = {
        "marker": MARKER,
        "photon_source": photon.EXTRACTED_INPUT.relative_to(ROOT).as_posix(),
        "photon_source_sha256": digest(photon.EXTRACTED_INPUT),
        "c3_source": c3.EXTRACTED_INPUT.relative_to(ROOT).as_posix(),
        "c3_source_sha256": digest(c3.EXTRACTED_INPUT),
        "photon_block": {
            "coordinates_g_gplus_gminus_gCFF": point.tolist(),
            "linear_condition_number": photon_condition,
            "stability_matrix": photon_matrix.tolist(),
            "beta_eigenvalues": complex_rows(photon_eigenvalues),
            "critical_exponents": complex_rows(photon_exponents),
        },
        "c3_vertical_nullcline": c3_nullcline,
        "frozen_photon_lower_curvature_combined_solve": frozen_combined,
        "triangular_diagnostic_fixed_point": {
            "coordinates_g_gplus_gminus_gCFF_h": [*point.tolist(), conditional_h["h"]],
            "is_full_combined_fixed_point": False,
            "reason": "pure-C3 beta_g mismatch and reverse h-to-photon block are not yet included",
        },
        "partial_combined_common_zero": partial_combined,
        "principal_cff_to_c3": principal,
        "stability_contract": {
            "photon_modal_matrix_condition_number": float(np.linalg.cond(photon_modes)),
            "signed_imaginary_axis_gap": signed_gap,
            "principal_cff_to_h_modal_norm": principal_modal_norm,
            "principal_fraction_of_gap": principal_modal_norm / signed_gap,
            "known_lower_plus_principal_c_to_h_modal_norm": principal_modal_norm,
            "known_lower_plus_principal_fraction_of_gap": principal_modal_norm / signed_gap,
            "unknown_reverse_modal_norm_requirement": f"norm(V^-1 b_h_to_photon)_2 < {signed_gap}",
            "full_cross_gate": "max(norm(V^-1 b)_2,norm(c V)_2)<signed_gap",
            "pairwise_reverse_tolerances": pairwise_reverse_tolerances,
            "principal_chain_alone_preserves_index": bool(principal_modal_norm < signed_gap),
            "full_combined_index_proved": False,
            "triangular_five_coordinate_matrix": triangular_matrix.tolist(),
            "triangular_beta_eigenvalues": complex_rows(triangular_eigenvalues),
            "triangular_signed_index": {
                "negative_real_parts": int(sum(value.real < 0 for value in triangular_eigenvalues)),
                "positive_real_parts": int(sum(value.real > 0 for value in triangular_eigenvalues)),
            },
        },
        "open_exact_terms": [
            "linear and quadratic CFF-curvature a6 contributions to beta_h",
            "direct C3 Hessian contribution to the seven photon-background projection rows",
        ],
    }
    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_PHOTON_POINT={point.tolist()}", flush=True)
    print(f"{MARKER}_C3_PURE_VERTICAL_H={c3_nullcline['h']}", flush=True)
    print(f"{MARKER}_COMBINED_CONDITIONAL_H={conditional_h['h']}", flush=True)
    print(f"{MARKER}_COMBINED_CONDITIONAL_LAMBDA={lambda_h}", flush=True)
    print(
        f"{MARKER}_PARTIAL_COMMON_ZERO={partial_combined['coordinates_g_gplus_gminus_gCFF_h']}",
        flush=True,
    )
    print(f"{MARKER}_PARTIAL_COMMON_GAP={partial_combined['signed_imaginary_axis_gap']}", flush=True)
    print(f"{MARKER}_PRINCIPAL_FRACTION_OF_GATE={principal_modal_norm / signed_gap}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
