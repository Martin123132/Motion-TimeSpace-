from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import camb
import camb.symbolic as camb_symbolic
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import brentq
from scipy.special import spherical_jn


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4891_species_hierarchy_camb_FDT_bound as prior  # noqa: E402


CHECKPOINT = "4892"
NEXT_TARGET = (
    "4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-"
    "cutoff-selection-or-CMB-likelihood-demotion-gate.md"
)
ETA_SAMPLES = 2401
ELL_REPORT = (2, 3, 4, 5, 10, 19, 40, 60, 80, 110, 150, 200, 300, 400)
CONVERGENCE_ELLS = (2, 10, 40, 200)
BATH_DELTA_N = 1.0
BATH_CANDIDATE_CUTOFF = 0.3
BATH_CANDIDATE_TEMPERATURE = 0.1


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4892_00_4891",
            POST
            / "4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-FDT-state-normalization-or-CMB-source-demotion-gate.md",
            "MTS_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891",
        ),
        (
            "SRC4892_01_validation",
            OUTPUT / "P8_Y5_BRR545_4891_VALIDATION.csv",
            "VAL4891_OVERALL,PASS",
        ),
        (
            "SRC4892_02_parent_response",
            OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv",
            "Weyl_response_ratio",
        ),
        (
            "SRC4892_03_limber_response",
            OUTPUT / "P8_Y5_R2FR_4891_LENSING_RESPONSE.csv",
            "fractional_lensing_shift",
        ),
        (
            "SRC4892_04_FDT_bound",
            OUTPUT / "P8_Y5_R2FR_4891_FDT_SUMMARY.csv",
            "combined_equal_variance_bound",
        ),
        (
            "SRC4892_05_CAMB",
            Path(camb.__file__).resolve(),
            "CAMB",
        ),
        (
            "SRC4892_06_symbolic",
            Path(camb_symbolic.__file__).resolve(),
            "ISW = 2 * diff(phi, t) * exptau",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_output_or_engine_source",
            "source_path": str(path),
            "source_exists": path.exists(),
            "marker": marker,
            "marker_found": _contains(path, marker),
        }
        for source_id, path, marker in sources
    ]
    return {
        "rows": rows,
        "CAMB_version": camb.__version__,
        "passed": bool(
            camb.__version__ == "1.6.6"
            and all(
                row["source_exists"] and row["marker_found"] for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def response_grid() -> dict[str, Any]:
    path = OUTPUT / "P8_Y5_R2FR_4891_PARENT_RESPONSE.csv"
    source_rows = _read_csv(path)
    rows = [
        {
            "k_h_per_Mpc": float(row["k_h_per_Mpc"]),
            "redshift": float(row["redshift"]),
            "N": float(row["N"]),
            "Weyl_response_ratio": float(row["Weyl_response_ratio"]),
        }
        for row in source_rows
    ]
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
    return {
        "rows": rows,
        "k_nodes": k_nodes,
        "N_nodes": n_nodes,
        "values": values,
        "interpolator": interpolator,
        "minimum_k_h_per_Mpc": float(k_nodes[0]),
        "maximum_k_h_per_Mpc": float(k_nodes[-1]),
        "minimum_N": float(n_nodes[0]),
        "maximum_N": float(n_nodes[-1]),
        "passed": bool(
            len(rows) == len(k_nodes) * len(n_nodes)
            and np.all(np.isfinite(values))
            and np.all(values > 0.0)
        ),
    }


@lru_cache(maxsize=None)
def transfer_normalization() -> dict[str, Any]:
    control = prior._run_camb(prior.TARGET, "matched_LCDM")
    params = control["params"]
    results = control["results"]
    transfer_data = results.get_cmb_transfer_data()
    ell_values, q_values, temperature_transfer = transfer_data.get_transfer(0)
    _, _, lens_transfer = transfer_data.get_transfer(2)
    primordial_power = params.scalar_power(q_values)
    log_q = np.log(q_values)
    raw_temperature = results.get_unlensed_scalar_cls(
        lmax=prior.LMAX, CMB_unit=None, raw_cl=True
    )
    raw_lens = results.get_lens_potential_cls(
        lmax=prior.LMAX, CMB_unit=None, raw_cl=True
    )
    rows: list[dict[str, Any]] = []
    errors: list[float] = []
    for source, transfer, reference, column in (
        ("temperature", temperature_transfer, raw_temperature, 0),
        ("lensing_potential", lens_transfer, raw_lens, 0),
    ):
        for ell in ELL_REPORT:
            ell_index = int(np.where(ell_values == ell)[0][0])
            calculated = float(
                4.0
                * math.pi
                * np.trapezoid(
                    primordial_power * transfer[ell_index] ** 2,
                    x=log_q,
                )
            )
            expected = float(reference[ell, column])
            relative_error = calculated / expected - 1.0
            errors.append(abs(relative_error))
            rows.append(
                {
                    "source": source,
                    "ell": ell,
                    "calculated_raw_Cl": calculated,
                    "CAMB_raw_Cl": expected,
                    "fractional_normalization_residual": relative_error,
                }
            )
    return {
        "rows": rows,
        "NumSources": int(transfer_data.NumSources),
        "q_count": int(len(q_values)),
        "ell_count": int(len(ell_values)),
        "normalization": "C_l=4 pi integral dln(k) P_R(k) Delta_l(k)^2",
        "maximum_abs_fractional_residual": max(errors),
        "passed": bool(
            transfer_data.NumSources == 3
            and max(errors) < 2.0e-3
        ),
    }


def _source_arrays() -> dict[str, Any]:
    control = prior._run_camb(prior.TARGET, "matched_LCDM")
    results = control["results"]
    transfer_data = results.get_cmb_transfer_data()
    ell_values, q_values, temperature_transfer = transfer_data.get_transfer(0)
    _, _, lens_transfer = transfer_data.get_transfer(2)
    grid = response_grid()
    k_h_values = q_values / prior.HUBBLE_h
    domain_mask = (
        (k_h_values >= grid["minimum_k_h_per_Mpc"])
        & (k_h_values <= grid["maximum_k_h_per_Mpc"])
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
    interpolation_points = np.stack(
        np.meshgrid(np.log(domain_k_h), n_values, indexing="ij"), axis=-1
    ).reshape(-1, 2)
    response = grid["interpolator"](interpolation_points).reshape(
        len(domain_q), len(eta_values)
    )
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
    return {
        "control": control,
        "results": results,
        "ell_values": ell_values,
        "q_values": q_values,
        "temperature_transfer": temperature_transfer,
        "lens_transfer": lens_transfer,
        "domain_mask": domain_mask,
        "domain_indices": domain_indices,
        "domain_q": domain_q,
        "domain_k_h": domain_k_h,
        "eta_values": eta_values,
        "chi_values": chi_values,
        "redshifts": redshifts,
        "N_values": n_values,
        "response": response,
        "weyl": weyl,
        "lens_source": lens_source,
        "exp_minus_tau": exp_minus_tau,
        "delta_temperature_source": delta_temperature_source,
        "delta_lens_source": delta_lens_source,
    }


def _integrate_sources(
    arrays: dict[str, Any],
    eta_values: np.ndarray,
    chi_values: np.ndarray,
    delta_temperature_source: np.ndarray,
    delta_lens_source: np.ndarray,
    ell_subset: tuple[int, ...],
) -> dict[int, dict[str, np.ndarray]]:
    q_values = arrays["domain_q"]
    arguments = q_values[:, None] * chi_values[None, :]
    output: dict[int, dict[str, np.ndarray]] = {}
    for ell in ell_subset:
        bessel = spherical_jn(ell, arguments)
        output[ell] = {
            "delta_temperature_transfer": np.trapezoid(
                delta_temperature_source * bessel,
                x=eta_values,
                axis=1,
            ),
            "delta_lens_transfer": np.trapezoid(
                delta_lens_source * bessel,
                x=eta_values,
                axis=1,
            ),
        }
    return output


def _cl_row(
    arrays: dict[str, Any],
    ell: int,
    corrections: dict[str, np.ndarray],
) -> dict[str, Any]:
    params = arrays["control"]["params"]
    q_values = arrays["q_values"]
    log_q = np.log(q_values)
    primordial_power = params.scalar_power(q_values)
    ell_index = int(np.where(arrays["ell_values"] == ell)[0][0])
    baseline_temperature = arrays["temperature_transfer"][ell_index]
    baseline_lens = arrays["lens_transfer"][ell_index]
    parent_temperature = baseline_temperature.copy()
    parent_lens = baseline_lens.copy()
    parent_temperature[arrays["domain_indices"]] += corrections[
        "delta_temperature_transfer"
    ]
    parent_lens[arrays["domain_indices"]] += corrections[
        "delta_lens_transfer"
    ]

    def integral(first: np.ndarray, second: np.ndarray) -> float:
        return float(
            4.0
            * math.pi
            * np.trapezoid(
                primordial_power * first * second,
                x=log_q,
            )
        )

    baseline_tt = integral(baseline_temperature, baseline_temperature)
    parent_tt = integral(parent_temperature, parent_temperature)
    baseline_pp = integral(baseline_lens, baseline_lens)
    parent_pp = integral(parent_lens, parent_lens)
    baseline_tp = integral(baseline_temperature, baseline_lens)
    parent_tp = integral(parent_temperature, parent_lens)
    mask = arrays["domain_mask"]
    domain_log_q = log_q[mask]
    domain_power = primordial_power[mask]
    tt_domain = float(
        4.0
        * math.pi
        * np.trapezoid(
            domain_power * baseline_temperature[mask] ** 2,
            x=domain_log_q,
        )
    )
    pp_domain = float(
        4.0
        * math.pi
        * np.trapezoid(
            domain_power * baseline_lens[mask] ** 2,
            x=domain_log_q,
        )
    )
    cosmic_variance = math.sqrt(2.0 / (2.0 * ell + 1.0))
    tt_shift = parent_tt / baseline_tt - 1.0
    return {
        "ell": ell,
        "fractional_TT_shift": tt_shift,
        "fractional_lensing_potential_shift": parent_pp / baseline_pp - 1.0,
        "fractional_T_phi_shift": parent_tp / baseline_tp - 1.0,
        "temperature_response_domain_power_fraction": tt_domain / baseline_tt,
        "lensing_response_domain_power_fraction": pp_domain / baseline_pp,
        "temperature_cosmic_variance_fraction": cosmic_variance,
        "TT_shift_over_cosmic_variance": tt_shift / cosmic_variance,
        "baseline_TT_raw_Cl": baseline_tt,
        "parent_TT_raw_Cl": parent_tt,
        "baseline_phi_phi_raw_Cl": baseline_pp,
        "parent_phi_phi_raw_Cl": parent_pp,
    }


@lru_cache(maxsize=None)
def line_of_sight_projection() -> dict[str, Any]:
    arrays = _source_arrays()
    fine_corrections = _integrate_sources(
        arrays,
        arrays["eta_values"],
        arrays["chi_values"],
        arrays["delta_temperature_source"],
        arrays["delta_lens_source"],
        ELL_REPORT,
    )
    rows = [
        _cl_row(arrays, ell, fine_corrections[ell]) for ell in ELL_REPORT
    ]
    coarse_eta = arrays["eta_values"][::2]
    coarse_chi = arrays["chi_values"][::2]
    coarse_response = arrays["response"][:, ::2]
    coarse_weyl = arrays["weyl"][:, ::2]
    coarse_exp_minus_tau = arrays["exp_minus_tau"][::2]
    coarse_delta_weyl = (coarse_response - 1.0) * coarse_weyl
    coarse_temperature_source = (
        2.0
        * coarse_exp_minus_tau[None, :]
        * np.gradient(coarse_delta_weyl, coarse_eta, axis=1, edge_order=2)
        / arrays["domain_q"][:, None] ** 2
    )
    coarse_lens_source = (
        (coarse_response - 1.0) * arrays["lens_source"][:, ::2]
    )
    coarse_corrections = _integrate_sources(
        arrays,
        coarse_eta,
        coarse_chi,
        coarse_temperature_source,
        coarse_lens_source,
        CONVERGENCE_ELLS,
    )
    convergence_rows: list[dict[str, Any]] = []
    for ell in CONVERGENCE_ELLS:
        fine_row = next(row for row in rows if row["ell"] == ell)
        coarse_row = _cl_row(arrays, ell, coarse_corrections[ell])
        convergence_rows.append(
            {
                "ell": ell,
                "fine_fractional_TT_shift": fine_row["fractional_TT_shift"],
                "coarse_fractional_TT_shift": coarse_row["fractional_TT_shift"],
                "abs_TT_shift_difference": abs(
                    fine_row["fractional_TT_shift"]
                    - coarse_row["fractional_TT_shift"]
                ),
                "fine_fractional_lensing_shift": fine_row[
                    "fractional_lensing_potential_shift"
                ],
                "coarse_fractional_lensing_shift": coarse_row[
                    "fractional_lensing_potential_shift"
                ],
                "abs_lensing_shift_difference": abs(
                    fine_row["fractional_lensing_potential_shift"]
                    - coarse_row["fractional_lensing_potential_shift"]
                ),
            }
        )
    lens_reconstruction_rows: list[dict[str, Any]] = []
    for target_k_h, ell_set in (
        (0.01, (2, 10, 40)),
        (0.1, (10, 40, 200, 400)),
    ):
        q_index = int(np.argmin(np.abs(arrays["domain_k_h"] - target_k_h)))
        q_value = arrays["domain_q"][q_index]
        argument = q_value * arrays["chi_values"]
        for ell in ell_set:
            ell_index = int(np.where(arrays["ell_values"] == ell)[0][0])
            reconstructed = float(
                np.trapezoid(
                    arrays["lens_source"][q_index]
                    * spherical_jn(ell, argument),
                    x=arrays["eta_values"],
                )
            )
            expected = float(
                arrays["lens_transfer"][
                    ell_index, arrays["domain_indices"][q_index]
                ]
            )
            lens_reconstruction_rows.append(
                {
                    "target_k_h_per_Mpc": target_k_h,
                    "actual_k_h_per_Mpc": float(arrays["domain_k_h"][q_index]),
                    "ell": ell,
                    "reconstructed_transfer": reconstructed,
                    "CAMB_transfer": expected,
                    "fractional_residual": reconstructed / expected - 1.0,
                }
            )
    limber_lookup = {
        int(float(row["ell"])): float(row["fractional_lensing_shift"])
        for row in _read_csv(
            OUTPUT / "P8_Y5_R2FR_4891_LENSING_RESPONSE.csv"
        )
    }
    limber_comparison_rows = []
    for row in rows:
        ell = row["ell"]
        if ell in limber_lookup:
            non_limber = row["fractional_lensing_potential_shift"]
            limber = limber_lookup[ell]
            limber_comparison_rows.append(
                {
                    "ell": ell,
                    "non_Limber_fractional_shift": non_limber,
                    "Limber_fractional_shift_4891": limber,
                    "absolute_shift_difference": abs(non_limber - limber),
                }
            )
    maximum_reconstruction_residual = max(
        abs(row["fractional_residual"]) for row in lens_reconstruction_rows
    )
    maximum_convergence_difference = max(
        max(
            row["abs_TT_shift_difference"],
            row["abs_lensing_shift_difference"],
        )
        for row in convergence_rows
    )
    return {
        "rows": rows,
        "convergence_rows": convergence_rows,
        "lens_reconstruction_rows": lens_reconstruction_rows,
        "limber_comparison_rows": limber_comparison_rows,
        "temperature_source_identity": (
            "delta S_T^ISW=2 exp(-tau) d_eta[(R_W-1)W_CAMB/k^2]"
        ),
        "lensing_source_identity": (
            "delta S_phi=(R_W-1) S_phi_CAMB"
        ),
        "Weyl_normalization": "W_CAMB=k^2 Phi_Weyl",
        "eta_samples": ETA_SAMPLES,
        "coarse_eta_samples": (ETA_SAMPLES + 1) // 2,
        "response_q_count": int(len(arrays["domain_q"])),
        "response_k_min_h_per_Mpc": float(np.min(arrays["domain_k_h"])),
        "response_k_max_h_per_Mpc": float(np.max(arrays["domain_k_h"])),
        "maximum_abs_lens_reconstruction_residual": (
            maximum_reconstruction_residual
        ),
        "maximum_abs_resolution_shift_difference": (
            maximum_convergence_difference
        ),
        "maximum_abs_Limber_non_Limber_shift_difference": max(
            row["absolute_shift_difference"]
            for row in limber_comparison_rows
        ),
        "minimum_temperature_domain_power_fraction": min(
            row["temperature_response_domain_power_fraction"] for row in rows
        ),
        "minimum_lensing_domain_power_fraction": min(
            row["lensing_response_domain_power_fraction"] for row in rows
        ),
        "IR_temperature_incomplete_below_ell_10": True,
        "high_k_lensing_incomplete_above_ell_200": True,
        "official_likelihood_allowed": False,
        "passed": bool(
            maximum_reconstruction_residual < 5.0e-3
            and maximum_convergence_difference < 5.0e-4
            and all(
                math.isfinite(row["fractional_TT_shift"])
                and math.isfinite(row["fractional_lensing_potential_shift"])
                for row in rows
            )
        ),
    }


def _bath_variance(cutoff: float, temperature: float, delta_n: float) -> float:
    gamma_bar = prior.prior.background.GAMMA_BAR

    def integrand(omega: float) -> float:
        if omega == 0.0:
            return 0.0
        spectral_density = (
            gamma_bar
            * omega
            / (1.0 + (omega / cutoff) ** 2) ** 2
        )
        if temperature == 0.0:
            thermal_factor = 1.0
        else:
            argument = omega / (2.0 * temperature)
            thermal_factor = (
                1.0 if argument > 30.0 else 1.0 / math.tanh(argument)
            )
        window = math.sin(omega * delta_n / 2.0) ** 2 / omega**2
        return 4.0 * spectral_density * thermal_factor * window / math.pi

    value, _ = quad(
        integrand,
        0.0,
        math.inf,
        epsabs=1.0e-11,
        epsrel=2.0e-8,
        limit=500,
    )
    return float(value)


@lru_cache(maxsize=None)
def bath_state_realization() -> dict[str, Any]:
    fdt_summary = _read_csv(
        OUTPUT / "P8_Y5_R2FR_4891_FDT_SUMMARY.csv"
    )[0]
    variance_bound = float(fdt_summary["combined_equal_variance_bound"])
    cutoff_rows: list[dict[str, Any]] = []
    for cutoff in (0.1, 0.3, 1.0, 3.0):
        vacuum_variance = _bath_variance(cutoff, 0.0, BATH_DELTA_N)
        if vacuum_variance < variance_bound:
            upper_temperature = 0.1
            while (
                _bath_variance(cutoff, upper_temperature, BATH_DELTA_N)
                < variance_bound
            ):
                upper_temperature *= 2.0
            maximum_temperature = brentq(
                lambda temperature: _bath_variance(
                    cutoff, temperature, BATH_DELTA_N
                )
                - variance_bound,
                0.0,
                upper_temperature,
            )
        else:
            maximum_temperature = math.nan
        cutoff_rows.append(
            {
                "cutoff_per_efold": cutoff,
                "window_DeltaN": BATH_DELTA_N,
                "vacuum_impulse_variance": vacuum_variance,
                "variance_bound_4891": variance_bound,
                "vacuum_to_bound_ratio": vacuum_variance / variance_bound,
                "maximum_KMS_temperature_if_allowed": maximum_temperature,
                "vacuum_allowed": vacuum_variance <= variance_bound,
                "broad_Markov_over_window": cutoff * BATH_DELTA_N >= 3.0,
            }
        )
    candidate_variance = _bath_variance(
        BATH_CANDIDATE_CUTOFF,
        BATH_CANDIDATE_TEMPERATURE,
        BATH_DELTA_N,
    )
    vacuum_cutoff_limit = brentq(
        lambda cutoff: _bath_variance(cutoff, 0.0, BATH_DELTA_N)
        - variance_bound,
        0.3,
        1.0,
    )
    return {
        "rows": cutoff_rows,
        "state": (
            "rho_B=Z^-1 exp[-integral_0^infinity domega omega "
            "b_omega^dagger b_omega/Theta_B]"
        ),
        "spectral_density": (
            "J(omega)=gamma_bar omega/[1+(omega/Lambda_bar)^2]^2"
        ),
        "noise_spectrum": (
            "N(omega)=J(abs(omega)) coth[abs(omega)/(2 Theta_B)]"
        ),
        "retarded_completion": (
            "-Im Sigma_R(omega)=J(omega) for omega>0; Re Sigma_R is the "
            "once-subtracted Kramers-Kronig transform"
        ),
        "filtered_variance": (
            "Var[I_DeltaN]=(4/pi) integral_0^infinity domega J(omega) "
            "coth[omega/(2Theta_B)] sin^2(omega DeltaN/2)/omega^2"
        ),
        "low_frequency_Ohmic_limit": (
            "lim_omega_to_0 J(omega)/omega=gamma_bar=1"
        ),
        "candidate_cutoff_per_efold": BATH_CANDIDATE_CUTOFF,
        "candidate_temperature_per_efold": BATH_CANDIDATE_TEMPERATURE,
        "candidate_window_DeltaN": BATH_DELTA_N,
        "candidate_impulse_variance": candidate_variance,
        "variance_bound_4891": variance_bound,
        "candidate_to_bound_ratio": candidate_variance / variance_bound,
        "vacuum_cutoff_limit_times_DeltaN": (
            vacuum_cutoff_limit * BATH_DELTA_N
        ),
        "candidate_positive_KMS_state_exists": candidate_variance < variance_bound,
        "candidate_local_Markov_valid": (
            BATH_CANDIDATE_CUTOFF * BATH_DELTA_N >= 3.0
        ),
        "broad_Markov_vacuum_allowed": next(
            row["vacuum_allowed"]
            for row in cutoff_rows
            if row["cutoff_per_efold"] == 3.0
        ),
        "state_existence_closed": True,
        "parent_selects_cutoff_temperature_or_cell_measure": False,
        "physical_temperature_conversion_allowed": False,
        "noise_likelihood_allowed": False,
        "decision": (
            "A_POSITIVE_KMS_SUPER_DRUDE_STATE_EXISTS_INSIDE_THE_4891_"
            "NORMALIZED_BOUND_BUT_ONLY_IN_A_NON_MARKOV_REGIME_PARENT_CUTOFF_"
            "TEMPERATURE_AND_CELL_MEASURE_REMAIN_UNSELECTED"
        ),
        "passed": bool(
            candidate_variance < variance_bound
            and vacuum_cutoff_limit * BATH_DELTA_N < 1.0
            and not (
                BATH_CANDIDATE_CUTOFF * BATH_DELTA_N >= 3.0
            )
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    normalization = transfer_normalization()
    projection = line_of_sight_projection()
    bath = bath_state_realization()
    requirements = [
        {
            "requirement": "CAMB_transfer_to_Cl_normalization",
            "status": "closed_temperature_and_lensing_sources_below_0p2_percent",
            "closed": True,
        },
        {
            "requirement": "late_ISW_parent_source",
            "status": "derived_from_exact_CAMB_ISW_identity_and_parent_R_W",
            "closed": True,
        },
        {
            "requirement": "lensing_parent_source",
            "status": "derived_and_direct_source_reconstruction_validated",
            "closed": True,
        },
        {
            "requirement": "non_Limber_fixed_background_projection",
            "status": "run_TT_phi_phi_and_T_phi_with_resolution_check",
            "closed": True,
        },
        {
            "requirement": "infrared_parent_Weyl_response",
            "status": "open_below_0p001_h_per_Mpc_low_ell_TT_incomplete",
            "closed": False,
        },
        {
            "requirement": "high_k_parent_Weyl_response",
            "status": "open_above_0p1_h_per_Mpc_high_ell_lensing_incomplete",
            "closed": False,
        },
        {
            "requirement": "positive_FDT_bath_state_existence",
            "status": "closed_by_normalized_super_Drude_KMS_constructive_example",
            "closed": True,
        },
        {
            "requirement": "parent_bath_state_selection",
            "status": "open_cutoff_temperature_and_cell_measure_not_parent_owned",
            "closed": False,
        },
        {
            "requirement": "self_consistent_parent_Einstein_Boltzmann_run",
            "status": "open_fixed_background_response_insertion_only",
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
        "transfer_normalization": (
            "CAMB_TEMPERATURE_AND_LENS_POTENTIAL_TRANSFER_NORMALIZATION_CLOSED"
        ),
        "late_line_of_sight": (
            "NON_LIMBER_FIXED_BACKGROUND_ISW_LENSING_AND_TPHI_PROJECTION_RUN"
        ),
        "bath_state": bath["decision"],
        "CMB_likelihood_allowed": False,
        "promotion_status": (
            "LATE_LINE_OF_SIGHT_AND_BATH_STATE_EXISTENCE_ADVANCED_IR_HIGH_K_"
            "PARENT_RESPONSE_AND_PARENT_BATH_SELECTION_REMAIN_BEFORE_CMB_CLAIM"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            normalization["passed"]
            and projection["passed"]
            and bath["passed"]
            and sum(row["closed"] for row in requirements) == 5
            and not all(row["closed"] for row in requirements)
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "response_grid": response_grid(),
        "transfer_normalization": transfer_normalization(),
        "line_of_sight": line_of_sight_projection(),
        "bath_state": bath_state_realization(),
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
    normalization = calculation["sections"]["transfer_normalization"]
    projection = calculation["sections"]["line_of_sight"]
    bath = calculation["sections"]["bath_state"]
    print(
        "transfer_norm_max={:.6e} lens_reconstruction_max={:.6e}".format(
            normalization["maximum_abs_fractional_residual"],
            projection["maximum_abs_lens_reconstruction_residual"],
        )
    )
    for row in projection["rows"]:
        print(
            "L={} TT={:.6e} PP={:.6e} TP={:.6e} covT={:.4f} covP={:.4f}".format(
                row["ell"],
                row["fractional_TT_shift"],
                row["fractional_lensing_potential_shift"],
                row["fractional_T_phi_shift"],
                row["temperature_response_domain_power_fraction"],
                row["lensing_response_domain_power_fraction"],
            )
        )
    print(
        "bath_candidate_var={:.6e} bound={:.6e} vacuum_cutoff_DeltaN={:.6f}".format(
            bath["candidate_impulse_variance"],
            bath["variance_bound_4891"],
            bath["vacuum_cutoff_limit_times_DeltaN"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
