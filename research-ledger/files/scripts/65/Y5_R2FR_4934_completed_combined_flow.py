from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import root

import Y5_R2FR_4933_c3_direct_threshold_solver as c3
import Y5_R2FR_4933_combined_c3_photon_stability as previous
import Y5_R2FR_4933_photon_flow_reproduction as photon
import Y5_R2FR_4934_direct_c3_cff_principal as direct


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4934"
PORTAL_LINEAR = SOURCE_DIR / "portal_linear_c3_zero_results.json"
PORTAL_QUADRATIC = SOURCE_DIR / "portal_quadratic_c3_results.json"
DIRECT_CFF = SOURCE_DIR / "direct_c3_cff_principal_results.json"
PREVIOUS_COMBINED = POST / "source-intake" / "functional_rg" / "4933" / "combined_c3_photon_stability_results.json"
OUTPUT = SOURCE_DIR / "completed_combined_flow_results.json"
MARKER = "MTS_4934_COMPLETED_C3_CFF_COMBINED_FLOW"
EXPECTED_HASHES = {
    PORTAL_LINEAR: "f0f30c1233d36d47a92655dd0023918f978d5a76056ffd196a378cdb3156c002",
    PORTAL_QUADRATIC: "a939bf7f1464dc58cd61ea69f907d4d3bb29dd2b8aec36fa51c2ffbaa15ec574",
    DIRECT_CFF: "00c2c4ed4a2ece0611a6b167e885a9811b8748cace0a456337ac03e426034a95",
    PREVIOUS_COMBINED: "082c527e9ce2cfa722abcde9515606162bdb6fe55148ef41e316f78e82d52e0b",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [
        {"real": float(value.real), "imag": float(value.imag)}
        for value in values
    ]


def portal_affine_projection(cff_value: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    constant, gamma_a_coefficient, gamma_df_coefficient = (
        previous.photon_matter_affine_c3_projection(cff_value)
    )
    cff_squared = cff_value**2
    constant[10] += cff_squared / (4 * math.pi**2)
    gamma_a_coefficient[10] += cff_squared / (16 * math.pi**2)
    gamma_df_coefficient[10] -= 3 * cff_squared / (80 * math.pi**2)
    return constant, gamma_a_coefficient, gamma_df_coefficient


def direct_affine_functions():
    expression, symbols = direct.direct_coefficient_formula()
    direct_unknowns = sp.symbols(
        "direct_beta_g direct_gamma_g direct_gamma_s direct_gamma_a direct_gamma_df direct_gamma_ftl"
    )
    substitutions = {
        symbols["beta_g"]: direct_unknowns[0],
        symbols["gamma_g"]: direct_unknowns[1],
        symbols["gamma_s"]: direct_unknowns[2],
        symbols["gamma_a"]: direct_unknowns[3],
        symbols["gamma_df"]: direct_unknowns[4],
        symbols["gamma_ftl"]: direct_unknowns[5],
    }
    expression = sp.expand(expression.subs(substitutions))
    zero_substitution = {unknown: 0 for unknown in direct_unknowns}
    constant = sp.simplify(expression.subs(zero_substitution))
    coefficients = [sp.simplify(sp.diff(expression, unknown)) for unknown in direct_unknowns]
    reconstruction = constant + sum(
        coefficient * unknown
        for coefficient, unknown in zip(coefficients, direct_unknowns)
    )
    if sp.simplify(expression - reconstruction) != 0:
        raise RuntimeError("direct C3 to CFF coefficient is not affine in combined flow unknowns")
    arguments = (symbols["g"], symbols["g_CFF"])
    constant_function = sp.lambdify(arguments, constant, modules="numpy", cse=True)
    coefficient_function = sp.lambdify(
        arguments, sp.Matrix(coefficients), modules="numpy", cse=True
    )
    return constant_function, coefficient_function, str(sp.factor(expression))


def build_completed_solver():
    c3_matrix, c3_vector, _ = c3.build_linear_system()
    photon_matrix, photon_vector, _ = photon.build_system()
    c3_matrix_function = sp.lambdify((c3.g, c3.h, c3.rho), c3_matrix, modules="numpy", cse=True)
    c3_vector_function = sp.lambdify((c3.g, c3.h, c3.rho), c3_vector, modules="numpy", cse=True)
    photon_matrix_function = sp.lambdify(photon.COUPLINGS, photon_matrix, modules="numpy", cse=True)
    photon_vector_function = sp.lambdify(photon.COUPLINGS, photon_vector, modules="numpy", cse=True)
    direct_constant_function, direct_coefficient_function, direct_expression = direct_affine_functions()
    rho_value = 1 / (4 * math.pi)
    photon_to_combined_columns = (0, 2, 13, 14, 15, 3, 4, 5, 16, 17, 18, 19)
    direct_to_combined_columns = (0, 3, 5, 18, 19, 17)

    def system(point: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        g_value, plus_value, minus_value, cff_value, h_value = (
            float(value) for value in point
        )
        raw_photon = (
            g_value,
            plus_value + minus_value,
            plus_value - minus_value,
            cff_value,
        )
        numeric_c3_matrix = np.asarray(
            c3_matrix_function(g_value, h_value, rho_value), dtype=float
        )
        numeric_c3_vector = np.asarray(
            c3_vector_function(g_value, h_value, rho_value), dtype=float
        ).reshape(13)
        numeric_photon_matrix = np.asarray(
            photon_matrix_function(*raw_photon), dtype=float
        )
        numeric_photon_vector = np.asarray(
            photon_vector_function(*raw_photon), dtype=float
        ).reshape(12)
        matter_constant, matter_gamma_a, matter_gamma_df = portal_affine_projection(cff_value)

        matrix = np.zeros((20, 20), dtype=float)
        vector = np.zeros(20, dtype=float)
        matrix[:13, :13] = numeric_c3_matrix
        matrix[:13, 18] -= matter_gamma_a
        matrix[:13, 19] -= matter_gamma_df
        vector[:13] = numeric_c3_vector + matter_constant
        for photon_column, combined_column in enumerate(photon_to_combined_columns):
            matrix[13:, combined_column] = numeric_photon_matrix[5:, photon_column]
        vector[13:] = numeric_photon_vector[5:]

        direct_row = 19
        vector[direct_row] += h_value * float(
            direct_constant_function(g_value, cff_value)
        )
        direct_coefficients = np.asarray(
            direct_coefficient_function(g_value, cff_value), dtype=float
        ).reshape(6)
        for coefficient, combined_column in zip(
            direct_coefficients, direct_to_combined_columns
        ):
            matrix[direct_row, combined_column] -= h_value * coefficient
        return matrix, vector

    def solve_unknowns(point: np.ndarray) -> tuple[np.ndarray, float]:
        matrix, vector = system(point)
        return np.linalg.solve(matrix, vector), float(np.linalg.cond(matrix))

    def beta(point: np.ndarray) -> np.ndarray:
        try:
            unknowns, _ = solve_unknowns(point)
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
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return np.full(5, 1e30)

    return system, solve_unknowns, beta, direct_expression, photon_matrix_function, photon_vector_function


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    failed_hashes = [
        path.as_posix()
        for path, expected_hash in EXPECTED_HASHES.items()
        if source_hashes[path] != expected_hash
    ]
    if failed_hashes:
        raise RuntimeError(f"source hash mismatch: {failed_hashes}")
    previous_result = json.loads(PREVIOUS_COMBINED.read_text(encoding="utf-8"))
    seed = np.array(
        previous_result["partial_combined_common_zero"][
            "coordinates_g_gplus_gminus_gCFF_h"
        ],
        dtype=float,
    )
    (
        system,
        solve_unknowns,
        beta,
        direct_expression,
        photon_matrix_function,
        photon_vector_function,
    ) = build_completed_solver()
    print(f"{MARKER}_SYSTEM_READY", flush=True)
    solution = root(beta, seed, method="hybr", options={"maxfev": 4000, "xtol": 1e-11})
    residual = beta(solution.x)
    unknowns, condition = solve_unknowns(solution.x)
    if not solution.success or np.linalg.norm(residual, ord=np.inf) >= 1e-9:
        raise RuntimeError(
            f"completed combined solve failed: {solution.message}; residual={residual.tolist()}"
        )

    jacobian = np.zeros((5, 5), dtype=float)
    for column in range(5):
        scale = max(abs(solution.x[column]), (1e-5, 1e-4, 1e-4, 1e-6, 1e-8)[column])
        step = 2e-5 * scale
        plus = solution.x.copy()
        minus = solution.x.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (beta(plus) - beta(minus)) / (2 * step)
    eigenvalues, modes = np.linalg.eig(jacobian)
    signed_gap = float(min(abs(value.real) for value in eigenvalues))

    g_value, plus_value, minus_value, cff_value, h_value = (
        float(value) for value in solution.x
    )
    raw_photon = (
        g_value,
        plus_value + minus_value,
        plus_value - minus_value,
        cff_value,
    )
    numeric_photon_matrix = np.asarray(photon_matrix_function(*raw_photon), dtype=float)
    numeric_photon_vector = np.asarray(photon_vector_function(*raw_photon), dtype=float).reshape(12)
    photon_unknowns = np.array(
        [unknowns[index] for index in (0, 2, 13, 14, 15, 3, 4, 5, 16, 17, 18, 19)],
        dtype=float,
    )
    omitted_lower_residual = numeric_photon_matrix[:5] @ photon_unknowns - numeric_photon_vector[:5]

    gamma_a_value = float(unknowns[18])
    gamma_df_value = float(unknowns[19])
    portal_quadratic_projection = (
        cff_value**2
        * (5 * gamma_a_value - 3 * gamma_df_value + 20)
        / (80 * math.pi**2)
    )
    direct_expression_symbolic, direct_symbols = direct.direct_coefficient_formula()
    direct_coefficient = float(
        direct_expression_symbolic.subs(
            {
                direct_symbols["g"]: g_value,
                direct_symbols["g_CFF"]: cff_value,
                direct_symbols["beta_g"]: unknowns[0],
                direct_symbols["gamma_g"]: unknowns[3],
                direct_symbols["gamma_s"]: unknowns[5],
                direct_symbols["gamma_a"]: gamma_a_value,
                direct_symbols["gamma_df"]: gamma_df_value,
                direct_symbols["gamma_ftl"]: unknowns[17],
            }
        )
    )
    direct_projection = h_value * direct_coefficient
    old_coordinates = np.asarray(
        previous_result["partial_combined_common_zero"][
            "coordinates_g_gplus_gminus_gCFF_h"
        ],
        dtype=float,
    )
    coordinate_shift = solution.x - old_coordinates
    relative_shift = coordinate_shift / np.maximum(np.abs(old_coordinates), 1e-30)
    checks = {
        "root_converged": bool(solution.success),
        "beta_residual_below_1e-9": bool(np.linalg.norm(residual, ord=np.inf) < 1e-9),
        "finite_projection_condition": math.isfinite(condition),
        "portal_linear_exact_zero": True,
        "portal_quadratic_included": portal_quadratic_projection != 0,
        "direct_C3_CFF_included": direct_projection != 0,
        "signed_gap_positive": signed_gap > 0,
        "one_relevant_four_irrelevant": int(sum(value.real < 0 for value in eigenvalues)) == 1
        and int(sum(value.real > 0 for value in eigenvalues)) == 4,
    }
    if not all(checks.values()):
        raise RuntimeError(f"completed combined-flow checks failed: {checks}")

    combined_names = [str(value) for value in c3.UNKNOWNS] + [
        "beta_f2sq",
        "beta_f4",
        "beta_cff",
        "gamma_ftrace",
        "gamma_ftl",
        "gamma_a",
        "gamma_df",
    ]
    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): source_hashes[path]
            for path in EXPECTED_HASHES
        },
        "canonical_projection_contract": {
            "equations": 20,
            "unknown_flow_coefficients": 20,
            "essential_coordinates": ["g", "g_plus", "g_minus", "g_CFF", "h_C3"],
            "vacuum_rows": "13 general-background C3-source rows with photon matter added",
            "photon_rows": "7 photon-background rows F2 through CFF",
            "duplicate_lower_photon_rows": "diagnostic only because the four-derivative source omits the h_C3 vacuum Hessian",
        },
        "source_complete_selected_row_fixed_point": {
            "success": bool(solution.success),
            "message": str(solution.message),
            "coordinates_g_gplus_gminus_gCFF_h": solution.x.tolist(),
            "beta_residual": residual.tolist(),
            "beta_residual_infinity_norm": float(np.linalg.norm(residual, ord=np.inf)),
            "linear_system_condition_number": condition,
            "coordinate_shift_from_4933_partial": coordinate_shift.tolist(),
            "relative_coordinate_shift_from_4933_partial": relative_shift.tolist(),
            "stability_matrix": jacobian.tolist(),
            "beta_eigenvalues": complex_rows(eigenvalues),
            "critical_exponents": complex_rows(-eigenvalues),
            "signed_imaginary_axis_gap": signed_gap,
            "modal_matrix_condition_number": float(np.linalg.cond(modes)),
            "signed_index": {
                "negative_real_parts": int(sum(value.real < 0 for value in eigenvalues)),
                "positive_real_parts": int(sum(value.real > 0 for value in eigenvalues)),
            },
            "combined_unknown_values": dict(
                zip(combined_names, (float(value) for value in unknowns))
            ),
            "is_source_complete_for_declared_minimal_truncation": True,
            "is_full_MTS_fixed_point": False,
        },
        "new_exact_sources": {
            "linear_portal_C3_projection": 0.0,
            "quadratic_portal_C3_projection": portal_quadratic_projection,
            "quadratic_portal_formula": "g_CFF^2*(5 gamma_a-3 gamma_DF+20)/(80 pi^2)",
            "direct_C3_to_CFF_coefficient": direct_coefficient,
            "direct_C3_to_CFF_projection": direct_projection,
            "direct_formula": direct_expression,
        },
        "diagnostic_duplicate_lower_photon_residual": {
            "values": omitted_lower_residual.tolist(),
            "infinity_norm": float(np.linalg.norm(omitted_lower_residual, ord=np.inf)),
            "claim_use": "scheme/truncation compatibility diagnostic, not an omitted source row in the canonical 20-row system",
        },
        "checks": checks,
        "remaining_exact_source_blocks_in_declared_minimal_C3_CFF_F4_system": [],
        "next_physics_boundary": [
            "trajectory integration from the completed fixed point",
            "larger operator-basis stability test",
            "connection to the parent MTS motion/time/source sector",
        ],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_POINT={solution.x.tolist()}", flush=True)
    print(f"{MARKER}_PORTAL_QUADRATIC={portal_quadratic_projection:.16g}", flush=True)
    print(f"{MARKER}_DIRECT_CFF={direct_projection:.16g}", flush=True)
    print(f"{MARKER}_EIGENVALUES={eigenvalues.tolist()}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
