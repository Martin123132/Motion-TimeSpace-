from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import camb
import camb.model as camb_model
import numpy as np
from scipy.interpolate import RegularGridInterpolator


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4891_species_hierarchy_camb_FDT_bound as camb_parent  # noqa: E402
import Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state as prior  # noqa: E402


CHECKPOINT = "4893"
NEXT_TARGET = (
    "4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-"
    "Boltzmann-or-cosmology-source-demotion-gate.md"
)
IR_K_NODES = (1.0e-5, 3.0e-5, 1.0e-4, 3.0e-4, 5.0e-4, 7.0e-4)
CERTIFIED_K_MAX = 1.0e-1
UV_ENVELOPE_K_MAX = 3.0e-1
ETA_SAMPLES = 2401
ELL_REPORT = prior.ELL_REPORT


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4893_00_4892",
            POST
            / "4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-realization-or-CMB-source-demotion-gate.md",
            "MTS_PARENT_LOS_KMS_STATE_GATE_4892",
        ),
        (
            "SRC4893_01_validation",
            OUTPUT / "P8_Y5_BRR545_4892_VALIDATION.csv",
            "VAL4892_OVERALL,PASS",
        ),
        (
            "SRC4893_02_tail_response",
            OUTPUT / "P8_Y5_R2FR_4893_SOLVED_TAIL_RESPONSE.csv",
            "Weyl_response_ratio",
        ),
        (
            "SRC4893_03_tail_summary",
            OUTPUT / "P8_Y5_R2FR_4893_TAIL_SOLVER_SUMMARY.csv",
            "maximum_relative_momentum_residual",
        ),
        (
            "SRC4893_04_projected_UV",
            OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_RESPONSE.csv",
            "response_envelope_width",
        ),
        (
            "SRC4893_05_projected_UV_summary",
            OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_SUMMARY.csv",
            "UV_envelope_allowed",
        ),
        (
            "SRC4893_06_adjoint",
            OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_RESPONSE.csv",
            "exact_cutoff_limit",
        ),
        (
            "SRC4893_07_adjoint_summary",
            OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv",
            "today_exact_cutoff_limit_at_Theta0p1",
        ),
        (
            "SRC4893_08_tail_solver",
            SCRIPTS / "Y5_R2FR_4893_response_tail_solver.py",
            "def solve_response",
        ),
        (
            "SRC4893_09_projected_solver",
            SCRIPTS / "Y5_R2FR_4893_constraint_projected_UV_solver.py",
            "def solve_projected",
        ),
        (
            "SRC4893_10_adjoint_solver",
            SCRIPTS / "Y5_R2FR_4893_FDT_adjoint_filter.py",
            "def adjoint_kernel",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_output_or_executable_solver",
            "source_path": str(path),
            "source_exists": path.exists(),
            "marker": marker,
            "marker_found": contains(path, marker),
        }
        for source_id, path, marker in sources
    ]
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def numeric_response_rows(path: Path) -> list[dict[str, float]]:
    return [
        {
            "k_h_per_Mpc": float(row["k_h_per_Mpc"]),
            "redshift": float(row["redshift"]),
            "N": float(row["N"]),
            "Weyl_response_ratio": float(row["Weyl_response_ratio"]),
            "fractional_Weyl_response": float(
                row["fractional_Weyl_response"]
            ),
        }
        for row in read_csv(path)
    ]


@lru_cache(maxsize=None)
def certified_response_grid() -> dict[str, Any]:
    tail_rows_all = read_csv(
        OUTPUT / "P8_Y5_R2FR_4893_SOLVED_TAIL_RESPONSE.csv"
    )
    tail_rows = [
        {
            "k_h_per_Mpc": float(row["k_h_per_Mpc"]),
            "redshift": float(row["redshift"]),
            "N": float(row["N"]),
            "Weyl_response_ratio": float(row["Weyl_response_ratio"]),
            "fractional_Weyl_response": float(
                row["fractional_Weyl_response"]
            ),
            "relative_momentum_residual": float(
                row["relative_momentum_residual"]
            ),
        }
        for row in tail_rows_all
        if float(row["k_h_per_Mpc"]) in IR_K_NODES
    ]
    zero_rows = [
        {
            "k_h_per_Mpc": float(row["k_h_per_Mpc"]),
            "redshift": float(row["redshift"]),
            "N": float(row["N"]),
            "Weyl_response_ratio": float(row["Weyl_response_ratio"]),
            "fractional_Weyl_response": float(
                row["fractional_Weyl_response"]
            ),
        }
        for row in tail_rows_all
        if float(row["k_h_per_Mpc"]) == 0.0
    ]
    prior_rows = numeric_response_rows(
        OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv"
    )
    rows = tail_rows + prior_rows
    k_nodes = np.asarray(sorted({row["k_h_per_Mpc"] for row in rows}))
    n_nodes = np.asarray(sorted({row["N"] for row in rows}))
    lookup = {
        (row["k_h_per_Mpc"], row["N"]): row["Weyl_response_ratio"]
        for row in rows
    }
    values = np.asarray(
        [[lookup[(k_value, n_value)] for n_value in n_nodes] for k_value in k_nodes]
    )
    interpolator = RegularGridInterpolator(
        (np.log(k_nodes), n_nodes),
        values,
        method="linear",
        bounds_error=True,
    )
    zero_lookup = {row["N"]: row["Weyl_response_ratio"] for row in zero_rows}
    ir_limit_residual = max(
        abs(lookup[(IR_K_NODES[0], n_value)] - zero_lookup[n_value])
        for n_value in n_nodes
    )
    return {
        "rows": rows,
        "zero_mode_rows": zero_rows,
        "k_nodes": k_nodes,
        "N_nodes": n_nodes,
        "values": values,
        "interpolator": interpolator,
        "minimum_k_h_per_Mpc": float(k_nodes[0]),
        "maximum_k_h_per_Mpc": float(k_nodes[-1]),
        "IR_limit_max_abs_response_residual": ir_limit_residual,
        "IR_max_relative_momentum_residual": max(
            row["relative_momentum_residual"] for row in tail_rows
        ),
        "passed": bool(
            len(rows) == len(k_nodes) * len(n_nodes)
            and k_nodes[0] == IR_K_NODES[0]
            and k_nodes[-1] == CERTIFIED_K_MAX
            and ir_limit_residual < 1.0e-6
            and max(
                row["relative_momentum_residual"] for row in tail_rows
            )
            < 5.0e-3
        ),
    }


def response_matrix(
    k_h_values: np.ndarray, n_values: np.ndarray
) -> np.ndarray:
    grid = certified_response_grid()
    points = np.stack(
        np.meshgrid(np.log(k_h_values), n_values, indexing="ij"), axis=-1
    ).reshape(-1, 2)
    return grid["interpolator"](points).reshape(
        len(k_h_values), len(n_values)
    )


@lru_cache(maxsize=None)
def infrared_line_of_sight() -> dict[str, Any]:
    control = camb_parent._run_camb(camb_parent.TARGET, "matched_LCDM")
    results = control["results"]
    transfer_data = results.get_cmb_transfer_data()
    ell_values, q_values, temperature_transfer = transfer_data.get_transfer(0)
    _, _, lens_transfer = transfer_data.get_transfer(2)
    k_h_values = q_values / camb_parent.HUBBLE_h
    domain_mask = (
        (k_h_values >= IR_K_NODES[0])
        & (k_h_values <= CERTIFIED_K_MAX)
    )
    domain_indices = np.where(domain_mask)[0]
    domain_q = q_values[domain_mask]
    domain_k_h = k_h_values[domain_mask]
    eta_values = np.linspace(
        float(results.tau_maxvis), float(results.tau0), ETA_SAMPLES
    )
    chi_values = float(results.tau0) - eta_values
    redshifts = np.asarray(
        results.redshift_at_comoving_radial_distance(chi_values)
    )
    n_values = -np.log1p(redshifts)
    response = response_matrix(domain_k_h, n_values)
    evolution = results.get_time_evolution(
        domain_q,
        eta_values,
        vars=["Weyl", "lens_potential_source"],
        lAccuracyBoost=3,
    )
    weyl = evolution[:, :, 0]
    lens_source = evolution[:, :, 1]
    background = results.get_background_time_evolution(
        eta_values, vars=["opacity", "visibility"]
    )
    exp_minus_tau = np.divide(
        background["visibility"],
        background["opacity"],
        out=np.ones_like(eta_values),
        where=background["opacity"] != 0.0,
    )
    delta_weyl = (response - 1.0) * weyl
    delta_temperature_source = (
        2.0
        * exp_minus_tau[None, :]
        * np.gradient(delta_weyl, eta_values, axis=1, edge_order=2)
        / domain_q[:, None] ** 2
    )
    delta_lens_source = (response - 1.0) * lens_source
    arrays = {
        "control": control,
        "ell_values": ell_values,
        "q_values": q_values,
        "temperature_transfer": temperature_transfer,
        "lens_transfer": lens_transfer,
        "domain_mask": domain_mask,
        "domain_indices": domain_indices,
        "domain_q": domain_q,
        "domain_k_h": domain_k_h,
    }
    corrections = prior._integrate_sources(
        arrays,
        eta_values,
        chi_values,
        delta_temperature_source,
        delta_lens_source,
        ELL_REPORT,
    )
    rows = [prior._cl_row(arrays, ell, corrections[ell]) for ell in ELL_REPORT]
    coarse_eta = eta_values[::2]
    coarse_chi = chi_values[::2]
    coarse_response = response[:, ::2]
    coarse_weyl = weyl[:, ::2]
    coarse_delta_weyl = (coarse_response - 1.0) * coarse_weyl
    coarse_temperature_source = (
        2.0
        * exp_minus_tau[::2][None, :]
        * np.gradient(coarse_delta_weyl, coarse_eta, axis=1, edge_order=2)
        / domain_q[:, None] ** 2
    )
    coarse_lens_source = (
        (coarse_response - 1.0) * lens_source[:, ::2]
    )
    coarse_corrections = prior._integrate_sources(
        arrays,
        coarse_eta,
        coarse_chi,
        coarse_temperature_source,
        coarse_lens_source,
        prior.CONVERGENCE_ELLS,
    )
    convergence_rows = []
    for ell in prior.CONVERGENCE_ELLS:
        fine = next(row for row in rows if row["ell"] == ell)
        coarse = prior._cl_row(arrays, ell, coarse_corrections[ell])
        convergence_rows.append(
            {
                "ell": ell,
                "fine_TT_shift": fine["fractional_TT_shift"],
                "coarse_TT_shift": coarse["fractional_TT_shift"],
                "abs_TT_shift_difference": abs(
                    fine["fractional_TT_shift"]
                    - coarse["fractional_TT_shift"]
                ),
                "fine_lens_shift": fine[
                    "fractional_lensing_potential_shift"
                ],
                "coarse_lens_shift": coarse[
                    "fractional_lensing_potential_shift"
                ],
                "abs_lens_shift_difference": abs(
                    fine["fractional_lensing_potential_shift"]
                    - coarse["fractional_lensing_potential_shift"]
                ),
            }
        )
    old_lookup = {
        int(float(row["ell"])): row
        for row in read_csv(OUTPUT / "P8_Y5_R2FR_4892_LOS_SPECTRA.csv")
    }
    comparison_rows = [
        {
            "ell": row["ell"],
            "IR_complete_TT_shift": row["fractional_TT_shift"],
            "4892_truncated_TT_shift": float(
                old_lookup[row["ell"]]["fractional_TT_shift"]
            ),
            "IR_completion_TT_change": row["fractional_TT_shift"]
            - float(old_lookup[row["ell"]]["fractional_TT_shift"]),
            "IR_complete_lens_shift": row[
                "fractional_lensing_potential_shift"
            ],
            "4892_truncated_lens_shift": float(
                old_lookup[row["ell"]][
                    "fractional_lensing_potential_shift"
                ]
            ),
        }
        for row in rows
    ]
    maximum_convergence = max(
        max(
            row["abs_TT_shift_difference"],
            row["abs_lens_shift_difference"],
        )
        for row in convergence_rows
    )
    return {
        "rows": rows,
        "convergence_rows": convergence_rows,
        "comparison_rows": comparison_rows,
        "response_q_count": int(len(domain_q)),
        "CAMB_q_count": int(len(q_values)),
        "minimum_CAMB_k_h_per_Mpc": float(np.min(k_h_values)),
        "maximum_certified_k_h_per_Mpc": float(np.max(domain_k_h)),
        "minimum_temperature_power_coverage": min(
            row["temperature_response_domain_power_fraction"] for row in rows
        ),
        "minimum_low_ell_temperature_power_coverage": min(
            row["temperature_response_domain_power_fraction"]
            for row in rows
            if row["ell"] <= 10
        ),
        "minimum_lens_power_coverage": min(
            row["lensing_response_domain_power_fraction"] for row in rows
        ),
        "maximum_resolution_shift_difference": maximum_convergence,
        "IR_gap_closed": bool(np.min(k_h_values) >= IR_K_NODES[0]),
        "high_k_lens_point_prediction_closed": False,
        "passed": bool(
            np.min(k_h_values) >= IR_K_NODES[0]
            and min(
                row["temperature_response_domain_power_fraction"]
                for row in rows
                if row["ell"] <= 10
            )
            > 0.99
            and maximum_convergence < 5.0e-4
        ),
    }


@lru_cache(maxsize=None)
def ultraviolet_envelope_model() -> dict[str, Any]:
    projected_rows = read_csv(
        OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_RESPONSE.csv"
    )
    strict_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv")
    strict_lookup = {
        (float(row["k_h_per_Mpc"]), float(row["N"])): float(
            row["Weyl_response_ratio"]
        )
        for row in strict_rows
    }
    k_nodes = np.asarray([0.1, 0.2, 0.3])
    n_nodes = np.asarray(
        sorted({float(row["N"]) for row in projected_rows})
    )
    projected_lookup = {
        (float(row["k_h_per_Mpc"]), float(row["N"])): row
        for row in projected_rows
    }
    central = np.zeros((len(k_nodes), len(n_nodes)))
    lower = np.zeros_like(central)
    upper = np.zeros_like(central)
    for k_index, k_value in enumerate(k_nodes):
        for n_index, n_value in enumerate(n_nodes):
            row = projected_lookup[(k_value, n_value)]
            candidates = [
                float(row["projected_Weyl_response_ratio"]),
                float(row["raw_full_system_Weyl_response_ratio"]),
            ]
            if k_value == 0.1:
                candidates.append(strict_lookup[(k_value, n_value)])
            lower[k_index, n_index] = min(candidates)
            upper[k_index, n_index] = max(candidates)
            central[k_index, n_index] = sum(candidates) / len(candidates)
    interpolators = {
        name: RegularGridInterpolator(
            (np.log(k_nodes), n_nodes),
            values,
            method="linear",
            bounds_error=True,
        )
        for name, values in (
            ("central", central),
            ("lower", lower),
            ("upper", upper),
        )
    }
    asymptotic_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4893_UV_ASYMPTOTIC.csv")
    asymptotic_lookup = {
        float(row["N"]): {
            "central": float(row["R_W_infinity"]),
            "fit_residual": float(row["maximum_abs_fit_residual"]),
        }
        for row in asymptotic_rows
    }
    asymptotic_central = np.asarray(
        [asymptotic_lookup[n_value]["central"] for n_value in n_nodes]
    )
    asymptotic_uncertainty = np.asarray(
        [
            max(
                asymptotic_lookup[n_value]["fit_residual"],
                abs(asymptotic_lookup[n_value]["central"] - lower[-1, index]),
                abs(asymptotic_lookup[n_value]["central"] - upper[-1, index]),
            )
            for index, n_value in enumerate(n_nodes)
        ]
    )
    return {
        "k_nodes": k_nodes,
        "N_nodes": n_nodes,
        "central": central,
        "lower": lower,
        "upper": upper,
        "interpolators": interpolators,
        "asymptotic_central": asymptotic_central,
        "asymptotic_uncertainty": asymptotic_uncertainty,
        "maximum_finite_k_envelope_width": float(np.max(upper - lower)),
        "maximum_asymptotic_uncertainty": float(
            np.max(asymptotic_uncertainty)
        ),
        "point_prediction_allowed": False,
        "envelope_allowed": True,
        "passed": bool(
            np.max(upper - lower) < 2.0e-4
            and np.max(asymptotic_uncertainty) < 3.0e-4
        ),
    }


def evaluate_response_envelope(
    k_h_values: np.ndarray, n_values: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k_h_values = np.asarray(k_h_values)
    n_values = np.asarray(n_values)
    if k_h_values.shape != n_values.shape:
        raise ValueError("k and N arrays must have equal shape")
    certified = certified_response_grid()
    uv = ultraviolet_envelope_model()
    central = np.ones_like(k_h_values, dtype=float)
    lower = np.ones_like(k_h_values, dtype=float)
    upper = np.ones_like(k_h_values, dtype=float)
    certified_mask = k_h_values <= CERTIFIED_K_MAX
    if np.any(certified_mask):
        points = np.column_stack(
            (np.log(k_h_values[certified_mask]), n_values[certified_mask])
        )
        values = certified["interpolator"](points)
        central[certified_mask] = values
        lower[certified_mask] = values
        upper[certified_mask] = values
    finite_uv_mask = (
        (k_h_values > CERTIFIED_K_MAX)
        & (k_h_values <= UV_ENVELOPE_K_MAX)
    )
    if np.any(finite_uv_mask):
        points = np.column_stack(
            (np.log(k_h_values[finite_uv_mask]), n_values[finite_uv_mask])
        )
        for name, output in (
            ("central", central),
            ("lower", lower),
            ("upper", upper),
        ):
            output[finite_uv_mask] = uv["interpolators"][name](points)
    asymptotic_mask = k_h_values > UV_ENVELOPE_K_MAX
    if np.any(asymptotic_mask):
        asymptotic_central = np.interp(
            n_values[asymptotic_mask],
            uv["N_nodes"],
            uv["asymptotic_central"],
        )
        uncertainty = np.interp(
            n_values[asymptotic_mask],
            uv["N_nodes"],
            uv["asymptotic_uncertainty"],
        )
        central[asymptotic_mask] = asymptotic_central
        lower[asymptotic_mask] = asymptotic_central - uncertainty
        upper[asymptotic_mask] = asymptotic_central + uncertainty
    return central, lower, upper


@lru_cache(maxsize=None)
def full_k_limber_envelope() -> dict[str, Any]:
    params = camb_parent._camb_params(camb_parent.TARGET, "matched_LCDM")
    params.set_matter_power(
        redshifts=[
            1100.0,
            500.0,
            200.0,
            100.0,
            50.0,
            30.0,
            20.0,
            10.0,
            5.0,
            3.0,
            2.0,
            1.0,
            0.5,
            0.0,
        ],
        kmax=2.0,
        nonlinear=False,
    )
    params.NonLinear = camb_model.NonLinear_none
    results = camb.get_results(params)
    power = results.get_matter_power_interpolator(
        nonlinear=False,
        var1=camb_model.Transfer_Weyl,
        var2=camb_model.Transfer_Weyl,
        hubble_units=False,
        k_hunit=False,
        log_interp=True,
    )
    chi_source = float(results.tau0 - results.tau_maxvis)
    chi_full = np.linspace(0.0, chi_source, 2401)
    chi = chi_full[1:-1]
    dchi = (chi_full[2:] - chi_full[:-2]) / 2.0
    redshifts = np.asarray(
        results.redshift_at_comoving_radial_distance(chi)
    )
    n_values = -np.log1p(redshifts)
    rows: list[dict[str, Any]] = []
    for ell in (10, 20, 40, 60, 80, 100, 150, 200, 300, 400):
        k_mpc = (ell + 0.5) / chi
        k_h = k_mpc / camb_parent.HUBBLE_h
        valid = (k_mpc >= 1.0e-5) & (k_mpc < power.kmax)
        baseline_power = np.zeros_like(k_mpc)
        baseline_power[valid] = power.P(
            redshifts[valid], k_mpc[valid], grid=False
        )
        window = (1.0 / chi - 1.0 / chi_source) ** 2 / chi**2
        integrand = np.zeros_like(k_mpc)
        integrand[valid] = (
            dchi[valid]
            * baseline_power[valid]
            * window[valid]
            / k_mpc[valid] ** 4
        )
        central = np.ones_like(k_mpc)
        lower = np.ones_like(k_mpc)
        upper = np.ones_like(k_mpc)
        central[valid], lower[valid], upper[valid] = evaluate_response_envelope(
            k_h[valid], n_values[valid]
        )
        baseline = float(np.sum(integrand))
        central_parent = float(np.sum(integrand * central**2))
        lower_parent = float(np.sum(integrand * lower**2))
        upper_parent = float(np.sum(integrand * upper**2))
        certified_weight = float(
            np.sum(integrand[valid & (k_h <= CERTIFIED_K_MAX)])
        )
        finite_uv_weight = float(
            np.sum(
                integrand[
                    valid
                    & (k_h > CERTIFIED_K_MAX)
                    & (k_h <= UV_ENVELOPE_K_MAX)
                ]
            )
        )
        rows.append(
            {
                "ell": ell,
                "central_fractional_lensing_shift": central_parent / baseline
                - 1.0,
                "lower_fractional_lensing_shift": lower_parent / baseline
                - 1.0,
                "upper_fractional_lensing_shift": upper_parent / baseline
                - 1.0,
                "lensing_shift_envelope_width": abs(
                    upper_parent - lower_parent
                )
                / baseline,
                "certified_k_weight_fraction": certified_weight / baseline,
                "finite_UV_envelope_weight_fraction": finite_uv_weight
                / baseline,
                "asymptotic_weight_fraction": 1.0
                - (certified_weight + finite_uv_weight) / baseline,
                "CAMB_power_kmax_per_Mpc": float(power.kmax),
            }
        )
    return {
        "rows": rows,
        "chi_star_Mpc": chi_source,
        "maximum_lensing_shift_envelope_width": max(
            row["lensing_shift_envelope_width"] for row in rows
        ),
        "minimum_certified_k_weight_fraction": min(
            row["certified_k_weight_fraction"] for row in rows
        ),
        "point_prediction_allowed": False,
        "bounded_full_k_projection": True,
        "official_likelihood_allowed": False,
        "passed": bool(
            max(row["lensing_shift_envelope_width"] for row in rows)
            < 1.0e-3
            and all(
                row["lower_fractional_lensing_shift"] < 0.0
                and row["upper_fractional_lensing_shift"] < 0.0
                for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def bath_cutoff_arbitration() -> dict[str, Any]:
    summary_row = read_csv(OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv")[0]
    response_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_RESPONSE.csv")
    today_rows = [row for row in response_rows if float(row["final_N"]) == 0.0]
    return {
        "rows": response_rows,
        "impulse_rows": read_csv(
            OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_IMPULSE_CHECK.csv"
        ),
        "today_cutoff_limit": float(
            summary_row["today_exact_cutoff_limit_at_Theta0p1"]
        ),
        "candidate_4892_variance_to_budget": float(
            summary_row["today_candidate_Lambda0p3_to_budget"]
        ),
        "Lambda1_variance_to_budget": float(
            summary_row["today_Lambda1_to_budget"]
        ),
        "memory_scale_Lambda15_variance_to_budget": float(
            summary_row["today_Lambda15_to_budget"]
        ),
        "carrier_mass_floor_over_H0": float(
            summary_row["largest_carrier_mass_floor_over_H0"]
        ),
        "maximum_impulse_relative_residual": float(
            summary_row["maximum_impulse_relative_residual"]
        ),
        "today_damping_over_H": float(today_rows[0]["damping_over_H"]),
        "today_memory_mass_over_H": float(
            today_rows[0]["memory_effective_mass_over_H"]
        ),
        "candidate_4892_survives": summary_row[
            "normalized_candidate_4892_survives_exact_filter"
        ].lower()
        == "true",
        "parent_cutoff_selected": summary_row["parent_cutoff_selected"].lower()
        == "true",
        "state_status": (
            "positive_KMS_family_exists_but_4892_parameter_point_rejected_and_"
            "no_parent_owned_cutoff_is_selected"
        ),
        "full_line_of_sight_noise_covariance_closed": False,
        "passed": bool(
            float(summary_row["maximum_impulse_relative_residual"])
            < 1.0e-4
            and not (
                summary_row[
                    "normalized_candidate_4892_survives_exact_filter"
                ].lower()
                == "true"
            )
            and not (summary_row["parent_cutoff_selected"].lower() == "true")
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    response = certified_response_grid()
    line_of_sight = infrared_line_of_sight()
    uv = ultraviolet_envelope_model()
    lens = full_k_limber_envelope()
    bath = bath_cutoff_arbitration()
    requirements = [
        {
            "requirement": "infrared_parent_Weyl_response",
            "status": "solved_from_k_zero_through_CAMB_q_min_with_constraint_pass",
            "closed": True,
        },
        {
            "requirement": "low_ell_temperature_line_of_sight",
            "status": "IR_complete_non_Limber_projection_over_more_than_99_percent_power",
            "closed": True,
        },
        {
            "requirement": "high_k_parent_point_response",
            "status": "rejected_raw_and_projected_branches_do_not_close_both_constraints",
            "closed": False,
        },
        {
            "requirement": "high_k_parent_response_envelope",
            "status": "bounded_by_full_vs_momentum_projected_branch_width",
            "closed": True,
        },
        {
            "requirement": "full_k_linear_lensing_bound",
            "status": "extended_CAMB_Weyl_power_with_UV_envelope_run",
            "closed": True,
        },
        {
            "requirement": "exact_FDT_metric_filter",
            "status": "adjoint_kernel_matches_four_forward_impulses_and_filters_spectrum",
            "closed": True,
        },
        {
            "requirement": "4892_KMS_parameter_point",
            "status": "rejected_at_today_one_percent_metric_gate",
            "closed": True,
        },
        {
            "requirement": "parent_bath_cutoff_selection",
            "status": "open_no_existing_damping_memory_or_carrier_scale_selects_allowed_cutoff",
            "closed": False,
        },
        {
            "requirement": "self_consistent_parent_Einstein_Boltzmann_run",
            "status": "open_high_k_constraint_split_and_nonlocal_kernel_not_compiled",
            "closed": False,
        },
        {
            "requirement": "official_CMB_likelihood",
            "status": "not_run",
            "closed": False,
        },
    ]
    return {
        "requirements": requirements,
        "closed_requirements": sum(row["closed"] for row in requirements),
        "total_requirements": len(requirements),
        "IR_result": (
            "IR_RESPONSE_AND_LOW_ELL_LINE_OF_SIGHT_CLOSED_WITHOUT_EXTRAPOLATION"
        ),
        "UV_result": (
            "HIGH_K_POINT_BRANCH_REJECTED_SUB_PERMILLE_RESPONSE_ENVELOPE_RETAINED"
        ),
        "bath_result": bath["state_status"],
        "CMB_likelihood_allowed": False,
        "promotion_status": (
            "IR_CMB_GAP_CLOSED_AND_UV_LENSING_BOUNDED_BUT_LOCAL_HIGH_K_PARENT_"
            "AND_4892_BATH_POINT_FAIL_NEXT_ROUTE_MUST_COMPILE_THE_NONLOCAL_"
            "KERNEL_OR_DEMOTE_THE_COSMOLOGY_SOURCE"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            response["passed"]
            and line_of_sight["passed"]
            and uv["passed"]
            and lens["passed"]
            and bath["passed"]
            and sum(row["closed"] for row in requirements) == 6
            and not all(row["closed"] for row in requirements)
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "certified_response": certified_response_grid(),
        "IR_line_of_sight": infrared_line_of_sight(),
        "UV_envelope": ultraviolet_envelope_model(),
        "full_k_lensing": full_k_limber_envelope(),
        "bath_cutoff": bath_cutoff_arbitration(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "decision": sections["arbitration"]["promotion_status"],
        "sections": sections,
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    response = calculation["sections"]["certified_response"]
    line_of_sight = calculation["sections"]["IR_line_of_sight"]
    lens = calculation["sections"]["full_k_lensing"]
    bath = calculation["sections"]["bath_cutoff"]
    print(
        "IR_limit={:.6e} IR_momentum={:.6e} q={}/{}".format(
            response["IR_limit_max_abs_response_residual"],
            response["IR_max_relative_momentum_residual"],
            line_of_sight["response_q_count"],
            line_of_sight["CAMB_q_count"],
        )
    )
    for row in line_of_sight["rows"]:
        print(
            "L={} TT={:.6e} PP={:.6e} TP={:.6e} covT={:.6f}".format(
                row["ell"],
                row["fractional_TT_shift"],
                row["fractional_lensing_potential_shift"],
                row["fractional_T_phi_shift"],
                row["temperature_response_domain_power_fraction"],
            )
        )
    print(
        "UV_lens_width={:.6e} cutoff={:.6f} Lambda0p3/budget={:.6f}".format(
            lens["maximum_lensing_shift_envelope_width"],
            bath["today_cutoff_limit"],
            bath["candidate_4892_variance_to_budget"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
