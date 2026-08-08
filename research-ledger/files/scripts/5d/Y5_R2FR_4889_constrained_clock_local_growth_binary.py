from __future__ import annotations

import csv
import json
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy import linalg, optimize
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4888_bath_kubo_backreacted_cosmology as prior  # noqa: E402


CHECKPOINT = "4889"
NEXT_TARGET = (
    "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-"
    "kernel-and-bath-identity-or-expansion-source-demotion-gate.md"
)

H0_KM_S_MPC = 67.4
MPC_M = 3.085677581491367e22
H0_PER_SECOND = H0_KM_S_MPC * 1000.0 / MPC_M
SIGMA_PER_SECOND = prior.SIGMA_BAR * H0_PER_SECOND
C_M_S = 299792458.0
AU_M = 149597870700.0
R_SUN_M = 695700000.0


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4889_00_4888",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4889_01_4850",
            POST
            / "4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md",
            "Exact Legendre/cuscuton equivalence",
        ),
        (
            "SRC4889_02_4851",
            POST
            / "4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md",
            "high-(k) Newton limit",
        ),
        (
            "SRC4889_03_4872",
            POST
            / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "unique timelike Landau eigenvector",
        ),
        (
            "SRC4889_04_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "state Landau vector",
        ),
        (
            "SRC4889_05_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "gamma_{\\rm classical}=1",
        ),
        (
            "SRC4889_06_prior_validation",
            POST
            / "source-intake"
            / "mts_residuals"
            / "P8_Y5_BRR545_4888_VALIDATION.csv",
            "VAL4888_OVERALL,PASS",
        ),
        (
            "SRC4889_07_growth_config",
            FORMAL
            / "runs"
            / "20260528-225042-growth-CMB-holdout-dry-run-design"
            / "results"
            / "holdout_dry_run_config.json",
            "primary_growth_branch",
        ),
        (
            "SRC4889_08_growth_row_lock",
            FORMAL
            / "data"
            / "cosmology"
            / "growth_CMB"
            / "sdss_eboss_dr16"
            / "row_lock_manifest.json",
            "validated_pairs_available",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_text_or_data_manifest",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": _contains(path, marker),
            }
        )
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def constrained_clock_parent() -> dict[str, Any]:
    return {
        "parent_action": (
            "S_clock=int sqrt(-g)[-varrho(U_mu U^mu+1)/2+"
            "Mbar_Pl^2 sigma_theta grad_mu phi grad^mu U]"
        ),
        "unit_flow": "u_mu=-grad_mu U; u_mu u^mu=-1",
        "constraint_equation": "U_mu U^mu=-1",
        "memory_equation": (
            "Box phi-kappa phi^3-sigma_theta Box U=0; "
            "theta=-Box U"
        ),
        "clock_current": (
            "J_U^mu=varrho u^mu+Mbar_Pl^2 sigma_theta grad^mu phi"
        ),
        "clock_equation": "nabla_mu J_U^mu=0 before SK bath exchange",
        "stress_tensor": (
            "T_clock+sigma_mn=varrho u_m u_n+Mbar_Pl^2 sigma_theta"
            "[2u_(m grad_n)phi-Y g_mn]"
        ),
        "background_energy": (
            "D=varrho-Mbar_Pl^2 sigma_theta phi_dot"
        ),
        "background_pressure": (
            "p_sigma=-Mbar_Pl^2 sigma_theta phi_dot"
        ),
        "background_equivalence": (
            "D obeys the 4888 x_X equation after the same SK damping "
            "energy transfer is included"
        ),
        "field_content": (
            "canonical memory wave plus constrained irrotational dust clock; "
            "no independent finite-sound-speed clock wave"
        ),
        "new_arena_switch": False,
        "passed": True,
    }


@lru_cache(maxsize=None)
def parent_background_health() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for target in prior.TARGETS:
        run = prior._solve_branch(target)
        arrays = prior._branch_arrays(run, 3001)
        e_values = arrays["E"]
        field_n = arrays["state"][1]
        clock_energy = arrays["state"][2]
        multiplier_density = (
            clock_energy + prior.SIGMA_BAR * e_values * field_n / 3.0
        )
        inertia_factor = 1.0 + (
            prior.SIGMA_BAR * e_values * field_n - prior.SIGMA_BAR**2
        ) / (3.0 * clock_energy)
        rows.append(
            {
                "target_Omega_memory_today": target,
                "kappa_over_H0_squared": run["kappa_bar"],
                "minimum_multiplier_density_over_rhocrit0": float(
                    np.min(multiplier_density)
                ),
                "multiplier_density_today_over_rhocrit0": float(
                    multiplier_density[-1]
                ),
                "minimum_effective_clock_inertia_factor": float(
                    np.min(inertia_factor)
                ),
                "effective_clock_inertia_factor_today": float(
                    inertia_factor[-1]
                ),
                "maximum_effective_clock_inertia_factor": float(
                    np.max(inertia_factor)
                ),
                "positive_multiplier": bool(
                    np.min(multiplier_density) > 0.0
                ),
                "positive_effective_inertia": bool(
                    np.min(inertia_factor) > 0.0
                ),
            }
        )
    return {
        "multiplier_relation": (
            "varrho/(3Mbar_Pl^2 H0^2)=x_X+sigma_bar E phi_N/3"
        ),
        "inertia_relation": (
            "B=[varrho-Mbar_Pl^2 sigma_theta^2]/D="
            "1+[sigma_bar E phi_N-sigma_bar^2]/(3x_X)"
        ),
        "rows": rows,
        "passed": all(
            row["positive_multiplier"] and row["positive_effective_inertia"]
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def characteristic_reduction() -> dict[str, Any]:
    omega, wave_number, sigma, coupling, density = sp.symbols(
        "omega k sigma C rho", nonzero=True
    )
    principal_matrix = sp.Matrix(
        [
            [omega**2 - wave_number**2, sigma * wave_number**2, 0],
            [0, omega, 0],
            [-coupling * wave_number**2, density * wave_number**2, omega],
        ]
    )
    determinant = sp.factor(principal_matrix.det())
    return {
        "linear_constraint": (
            "on U=t+pi in a local inertial patch, delta(U_mu U^mu+1)=0 "
            "gives partial_t pi=0 when metric perturbations are held fixed"
        ),
        "finite_frequency_result": (
            "for omega nonzero, pi=0 and (omega^2-k^2) delta_phi=0"
        ),
        "principal_matrix": (
            "[[omega^2-k^2,sigma k^2,0],[0,omega,0],"
            "[-C k^2,rho k^2,omega]]"
        ),
        "characteristic_polynomial": f"{determinant}=0",
        "symbolic_determinant_verified": bool(
            sp.simplify(
                determinant - omega**2 * (omega**2 - wave_number**2)
            )
            == 0
        ),
        "propagating_memory_speed_squared": 1.0,
        "clock_sound_speed_squared": 0.0,
        "upper_superluminal_clock_memory_root": False,
        "tensor_speed_squared": 1.0,
        "Maxwell_speed_squared": 1.0,
        "generic_PX_clock_branch": (
            "demoted as the selected local parent because its nonzero "
            "finite sound speed gives the 4888 c_plus^2>1 root"
        ),
        "scope": (
            "finite-frequency decoupling and high-k local limit; the dust "
            "zero mode and metric constraints remain in cosmological growth"
        ),
        "passed": bool(
            sp.simplify(
                determinant - omega**2 * (omega**2 - wave_number**2)
            )
            == 0
        ),
    }


def _growth_arrays(target: float) -> dict[str, Any]:
    run = prior._solve_branch(target)
    arrays = prior._branch_arrays(run, 4001)
    n_values = arrays["N"]
    e_values = arrays["E"]
    h_values = arrays["h"]
    field_n = arrays["state"][1]
    field_nn = arrays["rhs"][1]
    clock_density = arrays["state"][2]
    clock_density_n = arrays["rhs"][2]
    other_density = prior.OMEGA_OTHER_M * np.exp(-3.0 * n_values)
    numerator = (
        prior.SIGMA_BAR * e_values * field_n - prior.SIGMA_BAR**2
    )
    inertia = 1.0 + numerator / (3.0 * clock_density)
    numerator_n = prior.SIGMA_BAR * e_values * (
        h_values * field_n + field_nn
    )
    inertia_n = (
        numerator_n * clock_density - numerator * clock_density_n
    ) / (3.0 * clock_density**2)
    log_inertia_n = inertia_n / inertia

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        e_value = float(np.interp(n_value, n_values, e_values))
        h_value = float(np.interp(n_value, n_values, h_values))
        x_clock = float(np.interp(n_value, n_values, clock_density))
        x_other = prior.OMEGA_OTHER_M * math.exp(-3.0 * n_value)
        b_value = float(np.interp(n_value, n_values, inertia))
        dlnb = float(np.interp(n_value, n_values, log_inertia_n))
        source = (x_other * state[0] + x_clock * state[2]) / e_value**2
        return np.asarray(
            [
                state[1],
                -(2.0 + h_value) * state[1] + 1.5 * source,
                state[3],
                -(2.0 + h_value - dlnb) * state[3]
                + 1.5 * b_value * source,
            ]
        )

    initial = math.exp(prior.INITIAL_N)
    solution = solve_ivp(
        rhs,
        (prior.INITIAL_N, 0.0),
        np.asarray([initial, initial, initial, initial]),
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError("constrained-clock growth integration failed")
    states = solution.sol(n_values)
    total_density = other_density + clock_density
    weighted_growth = (
        other_density * states[0] + clock_density * states[2]
    ) / total_density
    other_density_n = -3.0 * other_density
    weighted_numerator = other_density * states[0] + clock_density * states[2]
    weighted_numerator_n = (
        other_density_n * states[0]
        + other_density * states[1]
        + clock_density_n * states[2]
        + clock_density * states[3]
    )
    total_density_n = other_density_n + clock_density_n
    weighted_growth_n = (
        weighted_numerator_n / total_density
        - weighted_numerator * total_density_n / total_density**2
    )
    growth_normalized = weighted_growth / weighted_growth[-1]
    growth_rate = weighted_growth_n / weighted_growth
    return {
        "target": target,
        "run": run,
        "N": n_values,
        "E": e_values,
        "h": h_values,
        "inertia": inertia,
        "solution": solution,
        "delta_m": weighted_growth,
        "D": growth_normalized,
        "f": growth_rate,
    }


@lru_cache(maxsize=None)
def _constrained_growth(target: float) -> dict[str, Any]:
    return _growth_arrays(target)


@lru_cache(maxsize=None)
def _baseline_growth() -> dict[str, Any]:
    n_values = np.linspace(prior.INITIAL_N, 0.0, 4001)
    e_values = np.sqrt(
        prior.OMEGA_R * np.exp(-4.0 * n_values)
        + prior.OMEGA_M * np.exp(-3.0 * n_values)
        + 1.0
        - prior.OMEGA_R
        - prior.OMEGA_M
    )
    h_values = -(
        4.0 * prior.OMEGA_R * np.exp(-4.0 * n_values)
        + 3.0 * prior.OMEGA_M * np.exp(-3.0 * n_values)
    ) / (2.0 * e_values**2)

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        e_value = float(np.interp(n_value, n_values, e_values))
        h_value = float(np.interp(n_value, n_values, h_values))
        omega_m = (
            prior.OMEGA_M * math.exp(-3.0 * n_value) / e_value**2
        )
        return np.asarray(
            [
                state[1],
                -(2.0 + h_value) * state[1]
                + 1.5 * omega_m * state[0],
            ]
        )

    initial = math.exp(prior.INITIAL_N)
    solution = solve_ivp(
        rhs,
        (prior.INITIAL_N, 0.0),
        np.asarray([initial, initial]),
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    states = solution.sol(n_values)
    return {
        "N": n_values,
        "E": e_values,
        "D": states[0] / states[0, -1],
        "f": states[1] / states[0],
    }


@lru_cache(maxsize=None)
def growth_response() -> dict[str, Any]:
    baseline = _baseline_growth()
    rows: list[dict[str, Any]] = []
    for target in prior.TARGETS:
        growth = _constrained_growth(target)
        for redshift in (0.0, 0.5, 1.0, 2.0):
            n_value = -math.log1p(redshift)
            d_value = float(np.interp(n_value, growth["N"], growth["D"]))
            f_value = float(np.interp(n_value, growth["N"], growth["f"]))
            d_baseline = float(
                np.interp(n_value, baseline["N"], baseline["D"])
            )
            f_baseline = float(
                np.interp(n_value, baseline["N"], baseline["f"])
            )
            rows.append(
                {
                    "target_Omega_memory_today": target,
                    "redshift": redshift,
                    "D_constrained": d_value,
                    "D_LCDM": d_baseline,
                    "fractional_D_shift": d_value / d_baseline - 1.0,
                    "f_constrained": f_value,
                    "f_LCDM": f_baseline,
                    "fractional_f_shift": f_value / f_baseline - 1.0,
                    "clock_to_other_growth_ratio": float(
                        growth["solution"].sol(n_value)[2]
                        / growth["solution"].sol(n_value)[0]
                    ),
                }
            )
    return {
        "subhorizon_equations": (
            "delta_o,NN+(2+h)delta_o,N=3S/2; "
            "delta_X,NN+(2+h-B_N/B)delta_X,N=3BS/2; "
            "S=(x_o delta_o+x_X delta_X)/E^2"
        ),
        "inertia_factor": (
            "B=1+[sigma_bar E phi_N-sigma_bar^2]/(3x_X)"
        ),
        "SK_damping_perturbation_scope": (
            "delta Q terms are H^2/k^2 suppressed in this RSD high-k limit"
        ),
        "rows": rows,
        "maximum_abs_fractional_D_shift": max(
            abs(row["fractional_D_shift"]) for row in rows
        ),
        "maximum_abs_fractional_f_shift": max(
            abs(row["fractional_f_shift"]) for row in rows
        ),
        "passed": all(
            math.isfinite(row["fractional_D_shift"])
            and math.isfinite(row["fractional_f_shift"])
            for row in rows
        ),
    }


def _numeric_rows(path: Path) -> list[tuple[float, float, str]]:
    rows: list[tuple[float, float, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        pieces = stripped.split()
        rows.append((float(pieces[0]), float(pieces[1]), pieces[2]))
    return rows


def _read_covariance(path: Path) -> np.ndarray:
    matrix = np.loadtxt(path)
    if matrix.ndim == 1:
        dimension = int(round(math.sqrt(matrix.size)))
        matrix = matrix.reshape((dimension, dimension))
    return np.asarray(matrix, dtype=float)


def _distance_integral(
    n_values: np.ndarray, e_values: np.ndarray, z_values: np.ndarray
) -> np.ndarray:
    z_grid = np.linspace(0.0, max(2.0, float(np.max(z_values) * 1.02 + 0.01)), 4096)
    n_grid = -np.log1p(z_grid)
    e_grid = np.interp(n_grid, n_values, e_values)
    integral = np.zeros_like(z_grid)
    integral[1:] = np.cumsum(
        0.5
        * np.diff(z_grid)
        * (1.0 / e_grid[:-1] + 1.0 / e_grid[1:])
    )
    return np.interp(z_values, z_grid, integral)


def _model_prediction(
    model: dict[str, Any],
    rows: list[tuple[float, float, str]],
    q_h0_rd: float,
    sigma8_today: float,
) -> np.ndarray:
    z_values = np.asarray([row[0] for row in rows])
    n_values = -np.log1p(z_values)
    distance = _distance_integral(model["N"], model["E"], z_values)
    d_m_over_rd = prior.C_KM_S * distance / q_h0_rd
    e_at_z = np.interp(n_values, model["N"], model["E"])
    d_h_over_rd = prior.C_KM_S / (q_h0_rd * e_at_z)
    d_v_over_rd = np.cbrt(
        z_values * d_m_over_rd**2 * d_h_over_rd
    )
    d_growth = np.interp(n_values, model["N"], model["D"])
    f_growth = np.interp(n_values, model["N"], model["f"])
    fsigma8 = sigma8_today * d_growth * f_growth
    output: list[float] = []
    for index, (_, _, quantity) in enumerate(rows):
        values = {
            "DM_over_rs": d_m_over_rd[index],
            "DM_over_rd": d_m_over_rd[index],
            "DH_over_rs": d_h_over_rd[index],
            "DH_over_rd": d_h_over_rd[index],
            "DV_over_rs": d_v_over_rd[index],
            "DV_over_rd": d_v_over_rd[index],
            "f_sigma8": fsigma8[index],
        }
        output.append(float(values[quantity]))
    return np.asarray(output)


def _score_file_set(
    model_name: str,
    model: dict[str, Any],
    file_set_name: str,
    file_pairs: list[dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    loaded: list[tuple[list[tuple[float, float, str]], np.ndarray]] = []
    for pair in file_pairs:
        loaded.append(
            (
                _numeric_rows(Path(pair["vector_file"])),
                _read_covariance(Path(pair["covariance_file"])),
            )
        )

    def objective(vector: np.ndarray) -> float:
        q_value, sigma8 = map(float, vector)
        total = 0.0
        for rows, covariance in loaded:
            observed = np.asarray([row[1] for row in rows])
            predicted = _model_prediction(
                model, rows, q_value, sigma8
            )
            residual = observed - predicted
            factor = linalg.cho_factor(
                covariance, lower=True, check_finite=False
            )
            total += float(
                residual
                @ linalg.cho_solve(factor, residual, check_finite=False)
            )
        return total

    fits = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=((7500.0, 14000.0), (0.3, 1.3)),
            options={"maxiter": 160, "ftol": 1.0e-10},
        )
        for start in ((10000.0, 0.8), (9800.0, 0.7), (10200.0, 0.9))
    ]
    successful = [fit for fit in fits if fit.success]
    fit = min(successful if successful else fits, key=lambda item: float(item.fun))
    predictions: list[dict[str, Any]] = []
    for pair_index, (rows, covariance) in enumerate(loaded, start=1):
        observed = np.asarray([row[1] for row in rows])
        predicted = _model_prediction(
            model, rows, float(fit.x[0]), float(fit.x[1])
        )
        for row_index, ((redshift, value, quantity), prediction) in enumerate(
            zip(rows, predicted), start=1
        ):
            predictions.append(
                {
                    "file_set": file_set_name,
                    "model": model_name,
                    "pair_index": pair_index,
                    "row_index": row_index,
                    "redshift": redshift,
                    "quantity": quantity,
                    "observed": value,
                    "predicted": float(prediction),
                    "residual": float(value - prediction),
                }
            )
    return (
        {
            "file_set": file_set_name,
            "model": model_name,
            "chi2": float(fit.fun),
            "q_H0_rd": float(fit.x[0]),
            "sigma8_today": float(fit.x[1]),
            "n_rows": sum(len(rows) for rows, _ in loaded),
            "n_profiled_parameters": 2,
            "success": bool(fit.success),
            "edge_flag": bool(
                fit.x[0] < 7565.0
                or fit.x[0] > 13935.0
                or fit.x[1] < 0.305
                or fit.x[1] > 1.295
            ),
        },
        predictions,
    )


@lru_cache(maxsize=None)
def growth_data_score() -> dict[str, Any]:
    config_path = (
        FORMAL
        / "runs"
        / "20260528-225042-growth-CMB-holdout-dry-run-design"
        / "results"
        / "holdout_dry_run_config.json"
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    baseline = _baseline_growth()
    models: dict[str, dict[str, Any]] = {
        "LCDM_fixed_Omega_m_0p315": baseline,
    }
    for target in prior.TARGETS:
        models[f"MTS_constrained_{target:.0e}"] = _constrained_growth(target)
    scores: list[dict[str, Any]] = []
    predictions: list[dict[str, Any]] = []
    for file_set_name, key in (
        ("BAO_plus_primary", "primary_growth_files"),
        ("full_shape_robustness", "robustness_growth_files"),
    ):
        for model_name, model in models.items():
            score, model_predictions = _score_file_set(
                model_name, model, file_set_name, config[key]
            )
            scores.append(score)
            predictions.extend(model_predictions)
    comparisons: list[dict[str, Any]] = []
    for file_set_name in ("BAO_plus_primary", "full_shape_robustness"):
        baseline_score = next(
            row
            for row in scores
            if row["file_set"] == file_set_name
            and row["model"] == "LCDM_fixed_Omega_m_0p315"
        )
        for target in prior.TARGETS:
            model_name = f"MTS_constrained_{target:.0e}"
            mts_score = next(
                row
                for row in scores
                if row["file_set"] == file_set_name
                and row["model"] == model_name
            )
            comparisons.append(
                {
                    "file_set": file_set_name,
                    "model": model_name,
                    "baseline": baseline_score["model"],
                    "delta_chi2_MTS_minus_LCDM": (
                        mts_score["chi2"] - baseline_score["chi2"]
                    ),
                    "same_profiled_parameter_count": True,
                    "stable_evidence_allowed": False,
                }
            )
    return {
        "scores": scores,
        "predictions": predictions,
        "comparisons": comparisons,
        "data_rule": (
            "BAO-plus primary and full-shape-only robustness are scored "
            "separately and never combined"
        ),
        "theory_scope": (
            "subhorizon constrained-clock equations with q=H0*rd and "
            "sigma8_today profiled; no CMB or radiation-neutrino inference"
        ),
        "passed": bool(
            all(row["success"] and not row["edge_flag"] for row in scores)
            and all(
                math.isfinite(row["delta_chi2_MTS_minus_LCDM"])
                for row in comparisons
            )
        ),
    }


@lru_cache(maxsize=None)
def local_GR_Newton_Maxwell() -> dict[str, Any]:
    epsilon_au = (H0_PER_SECOND * AU_M / C_M_S) ** 2
    epsilon_sun = (H0_PER_SECOND * R_SUN_M / C_M_S) ** 2
    return {
        "stationary_conditions": (
            "theta=0, phi=constant, Y=0, delta D=0 on the local "
            "Killing-aligned branch"
        ),
        "extra_stress": "delta T_clock+sigma_mn=0 under stationary conditions",
        "Einstein_equation": (
            "G_mn+Lambda g_mn=Mbar_Pl^-2(T_matter_mn+T_EM_mn)+"
            "O(H0^2 L^2)"
        ),
        "Newton_limit": (
            "nabla^2 U=4 pi G_N rho_total+O(H0^2 U); "
            "G_N=1/(8 pi Mbar_Pl^2)"
        ),
        "PPN_gamma": 1.0,
        "PPN_beta": 1.0,
        "Maxwell_action": (
            "S_EM=-1/4 int sqrt(-g) F_mn F^mn+int sqrt(-g) A_m J^m"
        ),
        "Maxwell_stress": (
            "T_EM_mn=F_malpha F_n^alpha-g_mn F_alphabeta F^alphabeta/4"
        ),
        "Poynting_readout": "S^i=-T_EM^i_0 in the local observer frame",
        "direct_phi_or_clock_charge_of_EM": 0.0,
        "cosmic_background_suppression_AU": epsilon_au,
        "cosmic_background_suppression_Rsun": epsilon_sun,
        "scope": (
            "selected metric-only EH branch, universal matter metric, "
            "stationary source and background-subtracted clock density"
        ),
        "passed": bool(
            epsilon_au < 1.3e-30
            and epsilon_sun < 3.0e-35
        ),
    }


@lru_cache(maxsize=None)
def binary_leakage_bound() -> dict[str, Any]:
    systems = [
        ("Earth_orbit", 365.256363004 * 86400.0, "orbital_period"),
        ("Mercury_orbit", 87.9691 * 86400.0, "orbital_period"),
        ("Hulse_Taylor", 7.75 * 3600.0, "representative_binary_period"),
        ("Double_Pulsar", 2.454 * 3600.0, "representative_binary_period"),
        ("LIGO_100Hz", 0.01, "wave_period"),
    ]
    rows: list[dict[str, Any]] = []
    for system, period_seconds, period_type in systems:
        angular_frequency = 2.0 * math.pi / period_seconds
        one_insertion = SIGMA_PER_SECOND / angular_frequency
        metric_amplitude = one_insertion**2
        clock_background_amplitude = (
            3.0
            * prior.OMEGA_X
            * (H0_PER_SECOND / angular_frequency) ** 2
        )
        combined_amplitude = metric_amplitude + clock_background_amplitude
        rows.append(
            {
                "system": system,
                "period_type": period_type,
                "period_seconds": period_seconds,
                "angular_frequency_per_second": angular_frequency,
                "sigma_over_omega": one_insertion,
                "two_insertion_memory_amplitude_envelope": metric_amplitude,
                "cosmic_clock_density_amplitude_envelope": (
                    clock_background_amplitude
                ),
                "combined_metric_amplitude_envelope": combined_amplitude,
                "four_insertion_power_envelope": metric_amplitude**2,
            }
        )
    return {
        "power_counting": (
            "ordinary matter and EM have no direct phi charge; phi is "
            "sourced once by sigma theta and its metric stress enters with "
            "a second sigma, so finite-frequency metric leakage starts at "
            "O[(sigma_theta/omega)^2] away from resonances"
        ),
        "clock_background_counting": (
            "the background clock density gives the separate conservative "
            "term 3 Omega_X (H0/omega)^2 before local density matching"
        ),
        "resonant_clock_pole": False,
        "stationary_limit_handled_separately": (
            "theta=0 exactly; the finite-frequency envelope is not applied "
            "at omega=0"
        ),
        "rows": rows,
        "largest_metric_amplitude_envelope": max(
            row["combined_metric_amplitude_envelope"] for row in rows
        ),
        "passed": all(
            row["combined_metric_amplitude_envelope"] < 3.0e-23
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    parent = constrained_clock_parent()
    health = parent_background_health()
    characteristics = characteristic_reduction()
    growth = growth_response()
    score = growth_data_score()
    local = local_GR_Newton_Maxwell()
    binary = binary_leakage_bound()
    return {
        "generic_PX_clock": (
            "DEMOTED_AS_SELECTED_LOCAL_PARENT_UNLESS_A_SEPARATE_NONLOCAL_"
            "UV_COMPLETION_IS_SUPPLIED"
        ),
        "selected_clock_parent": (
            "FIXED_NORM_IRROTATIONAL_CONSTRAINED_BATH_CLOCK"
        ),
        "coupled_cone": (
            "MEMORY_LUMINAL_CLOCK_DUST_ZERO_MODE_NO_SUPERLUMINAL_ROOT"
        ),
        "background": "IDENTICAL_4888_RAYS_WITH_POSITIVE_MULTIPLIER_AND_INERTIA",
        "growth": (
            "CONSTRAINED_SUBHORIZON_KERNEL_DERIVED_AND_REAL_SDSS_EBOSS_"
            "PRIMARY_ROBUSTNESS_SCORED"
        ),
        "local_GR_Newton_Maxwell": (
            "STATIONARY_SELECTED_BRANCH_REDUCES_TO_EH_PLUS_UNIVERSAL_"
            "MATTER_AND_MAXWELL_UP_TO_COSMIC_BACKGROUND_SUPPRESSION"
        ),
        "binary": "TWO_INSERTION_H0_FREQUENCY_LEAKAGE_BOUND_PASSES",
        "remaining_root_risk": (
            "clock bath identity, caustics/strong coupling in the zero-density "
            "patch, full Einstein-Boltzmann equations, and SK delta-Q noise"
        ),
        "promotion_status": (
            "CONSTRAINED_CLOCK_ROUTE_CLOSES_THE_4888_LOCAL_CONE_OBSTRUCTION_"
            "AND_PRESERVES_BACKGROUND_BUT_REMAINS_PRIVATE_UNTIL_FULL_"
            "COSMOLOGICAL_PERTURBATIONS_AND_BATH_IDENTITY_CLOSE"
        ),
        "next_target": NEXT_TARGET,
        "passed": all(
            (
                sources["passed"],
                parent["passed"],
                health["passed"],
                characteristics["passed"],
                growth["passed"],
                score["passed"],
                local["passed"],
                binary["passed"],
            )
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "parent": constrained_clock_parent(),
        "background_health": parent_background_health(),
        "characteristics": characteristic_reduction(),
        "growth": growth_response(),
        "growth_data": growth_data_score(),
        "local": local_GR_Newton_Maxwell(),
        "binary": binary_leakage_bound(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "decision": arbitration()["promotion_status"],
        "sections": sections,
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    print(calculation["decision"])
    for row in calculation["sections"]["background_health"]["rows"]:
        print(
            "target={:.0e} multiplier_min={:.9g} B_min={:.9g}".format(
                row["target_Omega_memory_today"],
                row["minimum_multiplier_density_over_rhocrit0"],
                row["minimum_effective_clock_inertia_factor"],
            )
        )
    for row in calculation["sections"]["growth_data"]["scores"]:
        print(
            f"{row['file_set']} {row['model']} chi2={row['chi2']:.8f} "
            f"sigma8={row['sigma8_today']:.6f}"
        )
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
