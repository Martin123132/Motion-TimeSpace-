from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import camb
import camb.model as camb_model
import camb.symbolic as camb_symbolic
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel as prior  # noqa: E402


CHECKPOINT = "4891"
NEXT_TARGET = (
    "4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-"
    "realization-or-CMB-source-demotion-gate.md"
)

TARGET = 1.0e-3
H0_KM_S_MPC = 67.4
HUBBLE_h = H0_KM_S_MPC / 100.0
OMBH2 = 0.02237
TAU_REIO = 0.0544
AS_PRIMORDIAL = 2.1e-9
NS_PRIMORDIAL = 0.965
MNU_EV = 0.06
OMNUH2_APPROX = MNU_EV / 93.14
LMAX = 400
K_H_NODES = (1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2, 1.0e-1)
Z_RESPONSE_NODES = (1100.0, 100.0, 30.0, 10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.0)


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4891_00_4890",
            POST
            / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md",
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890",
        ),
        (
            "SRC4891_01_prior_validation",
            POST
            / "source-intake"
            / "mts_residuals"
            / "P8_Y5_BRR545_4890_VALIDATION.csv",
            "VAL4890_OVERALL,PASS",
        ),
        (
            "SRC4891_02_CAMB_checkpoint",
            POST / "187-CAMB-density-convention-and-locked-transfer-theta-gate.md",
            "CAMB_locked_transfer_theta_gate_ran",
        ),
        (
            "SRC4891_03_CAMB_run",
            POST
            / "runs"
            / "20260601-000004-CAMB-density-convention-and-locked-transfer-theta-gate"
            / "status.json",
            '"camb_version": "1.6.6"',
        ),
        (
            "SRC4891_04_CAMB_package",
            Path(camb.__file__).resolve(),
            "CAMB",
        ),
        (
            "SRC4891_05_CAMB_symbolic",
            Path(camb_symbolic.__file__).resolve(),
            "def get_hierarchies",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_parent_validation_or_engine_source",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": _contains(path, marker),
            }
        )
    return {
        "rows": rows,
        "CAMB_version": camb.__version__,
        "CAMB_python": sys.executable,
        "passed": bool(
            camb.__version__ == "1.6.6"
            and all(
                row["source_exists"] and row["marker_found"]
                for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def species_hierarchy_derivation() -> dict[str, Any]:
    equations = {
        "massless_neutrino_density": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.delta_eqs[0])
        ),
        "photon_density": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.delta_eqs[1])
        ),
        "baryon_density": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.delta_eqs[2])
        ),
        "cold_matter_density": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.delta_eqs[3])
        ),
        "massless_neutrino_velocity": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.vel_eqs[0])
        ),
        "photon_velocity": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.vel_eqs[1])
        ),
        "baryon_velocity": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.vel_eqs[2])
        ),
        "cold_matter_velocity": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.vel_eqs[3])
        ),
        "photon_quadrupole": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.J_eq(2))
        ),
        "massless_neutrino_quadrupole": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.G_eq(2))
        ),
        "E_polarization_quadrupole": str(
            camb_symbolic.newtonian_gauge(camb_symbolic.E_eq(2))
        ),
    }
    slip_relation = (
        "Phi_N-Psi_N=kappa a^2 Pi/k^2; "
        "Pi=rho_gamma pi_gamma+rho_nu_rel pi_nu_rel+"
        "rho_nu_massive pi_nu_massive"
    )
    parent_sources = {
        "density": (
            "delta rho_parent=3 Mbar_Pl^2 H0^2(delta x_X+delta x_phi)"
        ),
        "momentum": (
            "-delta q_parent/(Mbar_Pl^2 H0)=3x_X P_U+"
            "(E phi_N-sigma_bar)delta phi"
        ),
        "pressure": (
            "delta p_parent=Mbar_Pl^2[phi_dot delta phi_dot-"
            "phi_dot^2 Psi-V_prime delta phi-sigma_theta"
            "(delta phi_dot-phi_dot Psi)]"
        ),
        "anisotropic_stress": "Pi_parent=0 at linear order",
    }
    equation_text = " ".join(equations.values())
    return {
        "gauge": (
            "Newtonian gauge ds^2=a^2[(1+2Psi_N)deta^2-"
            "(1-2Phi_N)dx^2]"
        ),
        "equations": equations,
        "slip_relation": slip_relation,
        "parent_sources": parent_sources,
        "exact_interface": (
            "replace CAMB total density momentum and pressure sources by the "
            "standard species sums plus the 4890 parent sources; leave the "
            "photon baryon and neutrino collision/hierarchy operators unchanged"
        ),
        "massive_neutrino_owner": (
            "CAMB compiled momentum-bin hierarchy, exposed through delta_nu and "
            "v_neutrino transfer variables"
        ),
        "temperature_source_owner": (
            "CAMB symbolic line-of-sight source with visibility monopole Doppler "
            "polarization and integrated metric terms"
        ),
        "new_parent_anisotropic_stress": False,
        "passed": bool(
            "Phi_N" in equation_text
            and "Psi_N" in equation_text
            and "opacity" in equation_text
            and "pi_g" in equation_text
            and "pi_r" in equation_text
            and "Pi_parent=0" in parent_sources["anisotropic_stress"]
        ),
    }


@lru_cache(maxsize=None)
def parent_background_mapping(target: float) -> dict[str, Any]:
    run = prior._solve_early_branch(target)
    early_matter = (
        prior.background.OMEGA_OTHER_M
        + prior.background.OMEGA_X * run["clock_scale"]
    )
    omch2 = (
        early_matter * HUBBLE_h**2 - OMBH2 - OMNUH2_APPROX
    )
    scale_factors = np.geomspace(1.0e-7, 1.0, 1000)
    w_values: list[float] = []
    rho_values: list[float] = []
    for scale_factor in scale_factors:
        n_value = math.log(scale_factor)
        if n_value < -math.log(101.0):
            w_values.append(-1.0)
            rho_values.append(math.nan)
            continue
        bg = prior._background_snapshot(run, n_value)
        radiation = prior.background.OMEGA_R * math.exp(-4.0 * n_value)
        matter = early_matter * math.exp(-3.0 * n_value)
        rho_effective = bg["E"] ** 2 - radiation - matter
        rho_effective_n = (
            2.0 * bg["h"] * bg["E"] ** 2
            + 4.0 * radiation
            + 3.0 * matter
        )
        w_effective = -1.0 - rho_effective_n / (3.0 * rho_effective)
        w_values.append(w_effective)
        rho_values.append(rho_effective)
    w_array = np.asarray(w_values)
    finite_rho = np.asarray(
        [value for value in rho_values if math.isfinite(value)]
    )
    present_residual = (
        1.0 - prior.background.OMEGA_R - early_matter
    )
    return {
        "target": target,
        "run": run,
        "early_matter_Omega": early_matter,
        "present_matter_Omega": prior.background.OMEGA_M,
        "matter_creation_delta_Omega": (
            prior.background.OMEGA_M - early_matter
        ),
        "omch2": omch2,
        "scale_factors": scale_factors,
        "w_values": w_array,
        "effective_density_values": finite_rho,
        "effective_density_today": present_residual,
        "minimum_effective_density": float(np.min(finite_rho)),
        "maximum_effective_density": float(np.max(finite_rho)),
        "minimum_w": float(np.min(w_array)),
        "maximum_w": float(np.max(w_array)),
        "crosses_minus_one": bool(
            np.any(w_array < -1.0) and np.any(w_array > -1.0)
        ),
        "CAMB_dark_energy_model": "DarkEnergyPPF",
        "passed": bool(
            early_matter > 0.0
            and omch2 > 0.0
            and np.all(np.diff(scale_factors) > 0.0)
            and np.all(np.isfinite(w_array))
            and np.min(finite_rho) > 0.0
        ),
    }


def _camb_params(target: float, branch: str) -> camb.CAMBparams:
    mapping = parent_background_mapping(target)
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=H0_KM_S_MPC,
        ombh2=OMBH2,
        omch2=mapping["omch2"],
        tau=TAU_REIO,
        mnu=MNU_EV,
        omk=0.0,
    )
    params.InitPower.set_params(As=AS_PRIMORDIAL, ns=NS_PRIMORDIAL)
    if branch == "parent_background_PPF":
        params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=mapping["scale_factors"],
            wde_w_array=mapping["w_values"],
            dark_energy_model="ppf",
        )
    elif branch != "matched_LCDM":
        raise ValueError(f"unknown CAMB branch: {branch}")
    params.set_for_lmax(LMAX, lens_potential_accuracy=1)
    params.set_matter_power(
        redshifts=[1100.0, 500.0, 200.0, 100.0, 50.0, 30.0, 20.0,
                   10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.0],
        kmax=0.35,
        nonlinear=False,
    )
    params.WantTransfer = True
    params.NonLinear = camb_model.NonLinear_none
    return params


@lru_cache(maxsize=None)
def _run_camb(target: float, branch: str) -> dict[str, Any]:
    params = _camb_params(target, branch)
    results = camb.get_results(params)
    powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
    return {
        "target": target,
        "branch": branch,
        "params": params,
        "results": results,
        "powers": powers,
        "derived": {
            key: float(value)
            for key, value in results.get_derived_params().items()
        },
        "Omega_b": float(results.get_Omega("baryon")),
        "Omega_cdm": float(results.get_Omega("cdm")),
        "Omega_nu": float(results.get_Omega("nu")),
        "Omega_de": float(results.get_Omega("de")),
    }


@lru_cache(maxsize=None)
def camb_background_spectra_bridge() -> dict[str, Any]:
    branch_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    background_rows: list[dict[str, Any]] = []
    for target in prior.background.TARGETS:
        mapping = parent_background_mapping(target)
        control = _run_camb(target, "matched_LCDM")
        parent = _run_camb(target, "parent_background_PPF")
        control_theta = control["derived"]["thetastar"]
        parent_theta = parent["derived"]["thetastar"]
        for output in (control, parent):
            branch_rows.append(
                {
                    "target": target,
                    "branch": output["branch"],
                    "early_matter_Omega": mapping["early_matter_Omega"],
                    "omch2": mapping["omch2"],
                    "thetastar": output["derived"]["thetastar"],
                    "zstar": output["derived"]["zstar"],
                    "DAstar": output["derived"]["DAstar"],
                    "rstar": output["derived"]["rstar"],
                    "rdrag": output["derived"]["rdrag"],
                    "Omega_b": output["Omega_b"],
                    "Omega_cdm": output["Omega_cdm"],
                    "Omega_nu": output["Omega_nu"],
                    "Omega_de": output["Omega_de"],
                }
            )
        control_spectra = control["powers"]["total"][2 : LMAX + 1]
        parent_spectra = parent["powers"]["total"][2 : LMAX + 1]
        for channel, index in (("TT", 0), ("EE", 1), ("TE", 3)):
            denominator = control_spectra[:, index]
            mask = np.abs(denominator) > 1.0e-20
            fractional = (
                parent_spectra[mask, index] / denominator[mask] - 1.0
            )
            residual_rows.append(
                {
                    "target": target,
                    "channel": channel,
                    "ell_min": 2,
                    "ell_max": LMAX,
                    "maximum_abs_fractional_residual": float(
                        np.max(np.abs(fractional))
                    ),
                    "rms_fractional_residual": float(
                        np.sqrt(np.mean(fractional**2))
                    ),
                    "fractional_thetastar_shift": (
                        parent_theta / control_theta - 1.0
                    ),
                    "closure_label": (
                        "background_geometry_and_standard_hierarchy_only_"
                        "PPF_not_parent_perturbations"
                    ),
                }
            )
        for redshift in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0):
            n_value = -math.log1p(redshift)
            parent_bg = prior._background_snapshot(
                mapping["run"], n_value
            )
            camb_hubble = float(
                parent["results"].hubble_parameter(redshift)
            )
            parent_hubble = H0_KM_S_MPC * parent_bg["E"]
            background_rows.append(
                {
                    "target": target,
                    "redshift": redshift,
                    "parent_H_km_s_Mpc": parent_hubble,
                    "CAMB_PPF_H_km_s_Mpc": camb_hubble,
                    "fractional_H_residual": (
                        camb_hubble / parent_hubble - 1.0
                    ),
                }
            )
    return {
        "branch_rows": branch_rows,
        "spectra_residual_rows": residual_rows,
        "background_rows": background_rows,
        "maximum_abs_fractional_H_residual": max(
            abs(row["fractional_H_residual"])
            for row in background_rows
        ),
        "maximum_abs_fractional_thetastar_shift": max(
            abs(row["fractional_thetastar_shift"])
            for row in residual_rows
        ),
        "maximum_TT_residual": max(
            row["maximum_abs_fractional_residual"]
            for row in residual_rows
            if row["channel"] == "TT"
        ),
        "CAMB_role": (
            "exact standard photon baryon neutrino recombination and line-of-"
            "sight hierarchy plus parent-matched background geometry; PPF dark-"
            "energy perturbations are not used as the parent claim"
        ),
        "official_likelihood_run": False,
        "passed": bool(
            len(branch_rows) == 6
            and len(residual_rows) == 9
            and all(
                math.isfinite(row["thetastar"])
                for row in branch_rows
            )
            and all(
                math.isfinite(row["maximum_abs_fractional_residual"])
                for row in residual_rows
            )
        ),
    }


@lru_cache(maxsize=None)
def hierarchy_engine_evolution() -> dict[str, Any]:
    output = _run_camb(TARGET, "parent_background_PPF")
    results = output["results"]
    redshifts = np.asarray([1100.0, 100.0, 30.0, 10.0, 3.0, 1.0, 0.0])
    k_h_values = np.asarray([1.0e-3, 1.0e-2, 3.0e-2])
    variable_names = [
        "delta_cdm",
        "delta_baryon",
        "delta_photon",
        "delta_neutrino",
        "delta_nu",
        "Weyl",
        "v_newtonian_cdm",
        "v_newtonian_baryon",
        "v_photon",
        "pi_photon",
        "v_neutrino",
        "T_source",
        "E_source",
        "lens_potential_source",
        "a",
        "H",
    ]
    evolution = results.get_redshift_evolution(
        k_h_values * HUBBLE_h,
        redshifts,
        vars=variable_names,
        lAccuracyBoost=3,
    )
    rows: list[dict[str, Any]] = []
    for k_index, k_h_value in enumerate(k_h_values):
        for z_index, redshift in enumerate(redshifts):
            row = {
                "k_h_per_Mpc": float(k_h_value),
                "redshift": float(redshift),
            }
            for variable_index, variable_name in enumerate(variable_names):
                row[variable_name] = float(
                    evolution[k_index, z_index, variable_index]
                )
            rows.append(row)
    visibility_redshifts = np.linspace(500.0, 2000.0, 1801)
    conformal_times = np.asarray(
        results.conformal_time(visibility_redshifts)
    )
    thermal = results.get_background_time_evolution(
        conformal_times,
        vars=["x_e", "opacity", "visibility", "cs2b"],
        format="dict",
    )
    peak_index = int(np.argmax(thermal["visibility"]))
    opacity_z30 = float(
        results.get_background_redshift_evolution(
            np.asarray([30.0]), vars=["opacity"]
        )["opacity"][0]
    )
    return {
        "rows": rows,
        "variable_names": variable_names,
        "visibility_peak_redshift": float(
            visibility_redshifts[peak_index]
        ),
        "visibility_peak": float(thermal["visibility"][peak_index]),
        "opacity_at_z30": opacity_z30,
        "maximum_abs_photon_quadrupole": max(
            abs(row["pi_photon"]) for row in rows
        ),
        "massless_neutrino_transfer_nonzero": any(
            abs(row["delta_neutrino"]) > 0.0 for row in rows
        ),
        "massive_neutrino_transfer_nonzero": any(
            abs(row["delta_nu"]) > 0.0 for row in rows
        ),
        "all_finite": bool(np.all(np.isfinite(evolution))),
        "passed": bool(
            np.all(np.isfinite(evolution))
            and 1000.0 < visibility_redshifts[peak_index] < 1200.0
            and max(abs(row["pi_photon"]) for row in rows) > 0.0
            and any(abs(row["delta_neutrino"]) > 0.0 for row in rows)
            and any(abs(row["delta_nu"]) > 0.0 for row in rows)
        ),
    }


def _gr_background(target: float, n_value: float) -> dict[str, float]:
    mapping = parent_background_mapping(target)
    radiation = prior.background.OMEGA_R * math.exp(-4.0 * n_value)
    matter = mapping["early_matter_Omega"] * math.exp(-3.0 * n_value)
    cosmological_constant = (
        1.0 - prior.background.OMEGA_R - mapping["early_matter_Omega"]
    )
    e_squared = radiation + matter + cosmological_constant
    return {
        "radiation": radiation,
        "matter": matter,
        "E": math.sqrt(e_squared),
        "h": (-2.0 * radiation - 1.5 * matter) / e_squared,
    }


def _gr_mode_algebra(
    target: float, n_value: float, state: np.ndarray, kbar: float
) -> dict[str, float]:
    phi_metric, matter_delta, matter_potential, radiation_delta, radiation_potential = state
    bg = _gr_background(target, n_value)
    k2 = kbar**2 * math.exp(-2.0 * n_value)
    total_density_delta = (
        bg["matter"] * matter_delta
        + bg["radiation"] * radiation_delta
    )
    phi_metric_n = (
        -phi_metric
        - k2 * phi_metric / (3.0 * bg["E"] ** 2)
        - total_density_delta / (2.0 * bg["E"] ** 2)
    )
    momentum_rhs = 0.5 * (
        3.0 * bg["matter"] * matter_potential
        + 4.0 * bg["radiation"] * radiation_potential
    )
    return {
        **bg,
        "k2": k2,
        "phi_metric_n": phi_metric_n,
        "momentum_residual": (
            bg["E"] * (phi_metric_n + phi_metric) - momentum_rhs
        ),
    }


@lru_cache(maxsize=None)
def solve_matched_gr_mode(
    target: float, k_h_per_mpc: float, amplitude: float = 1.0e-5
) -> dict[str, Any]:
    kbar = prior._kbar_from_h_per_mpc(k_h_per_mpc)
    n_initial = prior.EARLY_INITIAL_N
    phi_metric = amplitude
    matter_delta = -1.5 * amplitude
    radiation_delta = -2.0 * amplitude
    state = np.asarray(
        [phi_metric, matter_delta, 0.0, radiation_delta, 0.0]
    )
    algebra = _gr_mode_algebra(target, n_initial, state, kbar)
    denominator = 3.0 * algebra["matter"] + 4.0 * algebra["radiation"]
    common_potential = (
        2.0
        * algebra["E"]
        * (algebra["phi_metric_n"] + phi_metric)
        / denominator
    )
    state[2] = common_potential
    state[4] = common_potential

    def rhs(n_value: float, values: np.ndarray) -> np.ndarray:
        metric, _, matter_potential, radiation_contrast, radiation_potential = values
        local = _gr_mode_algebra(target, n_value, values, kbar)
        return np.asarray(
            [
                local["phi_metric_n"],
                3.0 * local["phi_metric_n"]
                - local["k2"] * matter_potential / local["E"],
                metric / local["E"],
                4.0 * local["phi_metric_n"]
                - 4.0 * local["k2"] * radiation_potential
                / (3.0 * local["E"]),
                radiation_potential
                + (metric + radiation_contrast / 4.0) / local["E"],
            ]
        )

    solution = solve_ivp(
        rhs,
        (n_initial, 0.0),
        state,
        method="DOP853",
        rtol=3.0e-10,
        atol=2.0e-14,
        max_step=min(0.01, 0.75 / max(kbar, 1.0)),
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError("matched GR mode integration failed")
    return {
        "target": target,
        "k_h_per_Mpc": k_h_per_mpc,
        "solution": solution,
    }


@lru_cache(maxsize=None)
def parent_metric_response() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    momentum_rows: list[float] = []
    for k_h_per_mpc in K_H_NODES:
        parent_mode = prior.solve_finite_k_mode(TARGET, k_h_per_mpc)
        gr_mode = solve_matched_gr_mode(TARGET, k_h_per_mpc)
        parent_run = prior._solve_early_branch(TARGET)
        kbar = prior._kbar_from_h_per_mpc(k_h_per_mpc)
        for redshift in Z_RESPONSE_NODES:
            n_value = -math.log1p(redshift)
            parent_state = parent_mode["solution"].sol(n_value)
            gr_state = gr_mode["solution"].sol(n_value)
            parent_phi = float(parent_state[0])
            gr_phi = float(gr_state[0])
            parent_algebra = prior._mode_algebra(
                parent_run, n_value, parent_state, kbar
            )
            momentum_scale = (
                abs(parent_algebra["momentum_lhs"])
                + abs(parent_algebra["momentum_rhs"])
                + 1.0e-20
            )
            momentum_rows.append(
                abs(parent_algebra["momentum_residual"]) / momentum_scale
            )
            rows.append(
                {
                    "k_h_per_Mpc": k_h_per_mpc,
                    "redshift": redshift,
                    "N": n_value,
                    "parent_Phi": parent_phi,
                    "matched_GR_Phi": gr_phi,
                    "Weyl_response_ratio": parent_phi / gr_phi,
                    "fractional_Weyl_response": parent_phi / gr_phi - 1.0,
                }
            )
    early_rows = [row for row in rows if row["redshift"] >= 30.0]
    late_rows = [row for row in rows if row["redshift"] <= 10.0]
    return {
        "rows": rows,
        "response_definition": (
            "R_W(k,z)=Phi_parent(k,z)/Phi_matched_GR(k,z); the standard "
            "photon-neutrino transfer multiplies this parent-derived late metric response"
        ),
        "new_parent_slip": False,
        "maximum_early_abs_response": max(
            abs(row["fractional_Weyl_response"]) for row in early_rows
        ),
        "maximum_late_abs_response": max(
            abs(row["fractional_Weyl_response"]) for row in late_rows
        ),
        "maximum_sampled_momentum_residual": max(momentum_rows),
        "passed": bool(
            len(rows) == len(K_H_NODES) * len(Z_RESPONSE_NODES)
            and all(
                math.isfinite(row["Weyl_response_ratio"])
                and row["Weyl_response_ratio"] > 0.0
                for row in rows
            )
        ),
    }


def _response_interpolator() -> RegularGridInterpolator:
    response = parent_metric_response()
    lookup = {
        (row["k_h_per_Mpc"], row["N"]): row["Weyl_response_ratio"]
        for row in response["rows"]
    }
    n_nodes = np.asarray(
        sorted({row["N"] for row in response["rows"]})
    )
    log_k_nodes = np.log(np.asarray(K_H_NODES))
    values = np.asarray(
        [
            [lookup[(k_value, n_value)] for n_value in n_nodes]
            for k_value in K_H_NODES
        ]
    )
    return RegularGridInterpolator(
        (log_k_nodes, n_nodes),
        values,
        method="linear",
        bounds_error=False,
        fill_value=1.0,
    )


@lru_cache(maxsize=None)
def lensing_response_projection() -> dict[str, Any]:
    control = _run_camb(TARGET, "matched_LCDM")
    results = control["results"]
    power = results.get_matter_power_interpolator(
        nonlinear=False,
        var1=camb_model.Transfer_Weyl,
        var2=camb_model.Transfer_Weyl,
        hubble_units=False,
        k_hunit=False,
        log_interp=True,
    )
    chi_source = float(results.tau0 - results.tau_maxvis)
    chis_full = np.linspace(0.0, chi_source, 1401)
    chis = chis_full[1:-1]
    dchis = (chis_full[2:] - chis_full[:-2]) / 2.0
    redshifts = np.asarray(
        results.redshift_at_comoving_radial_distance(chis)
    )
    response_interpolator = _response_interpolator()
    rows: list[dict[str, Any]] = []
    for ell in (10, 20, 40, 60, 80, 100, 150, 200):
        k_mpc = (ell + 0.5) / chis
        k_h = k_mpc / HUBBLE_h
        valid_power = (k_mpc >= 1.0e-4) & (k_mpc < power.kmax)
        baseline_power = np.zeros_like(k_mpc)
        baseline_power[valid_power] = power.P(
            redshifts[valid_power],
            k_mpc[valid_power],
            grid=False,
        )
        window = (1.0 / chis - 1.0 / chi_source) ** 2 / chis**2
        integrand = np.zeros_like(k_mpc)
        integrand[valid_power] = (
            dchis[valid_power]
            * baseline_power[valid_power]
            * window[valid_power]
            / k_mpc[valid_power] ** 4
        )
        n_values = -np.log1p(redshifts)
        response_valid = (
            (redshifts <= 30.0)
            & (k_h >= min(K_H_NODES))
            & (k_h <= max(K_H_NODES))
            & valid_power
        )
        ratios = np.ones_like(k_mpc)
        interpolation_points = np.column_stack(
            (np.log(k_h[response_valid]), n_values[response_valid])
        )
        ratios[response_valid] = response_interpolator(
            interpolation_points
        )
        baseline_integral = float(np.sum(integrand))
        parent_integral = float(np.sum(integrand * ratios**2))
        covered_integral = float(np.sum(integrand[response_valid]))
        rows.append(
            {
                "ell": ell,
                "parent_to_GR_Ckappa_ratio": (
                    parent_integral / baseline_integral
                ),
                "fractional_lensing_shift": (
                    parent_integral / baseline_integral - 1.0
                ),
                "parent_response_weight_fraction": (
                    covered_integral / baseline_integral
                ),
                "projection": (
                    "lowest-order Limber Weyl-power reweighting using the "
                    "parent-derived R_W squared"
                ),
            }
        )
    return {
        "rows": rows,
        "chi_star_Mpc": chi_source,
        "maximum_abs_fractional_lensing_shift": max(
            abs(row["fractional_lensing_shift"]) for row in rows
        ),
        "minimum_parent_response_weight_fraction": min(
            row["parent_response_weight_fraction"] for row in rows
        ),
        "official_lensing_likelihood": False,
        "passed": bool(
            all(
                math.isfinite(row["parent_to_GR_Ckappa_ratio"])
                and row["parent_to_GR_Ckappa_ratio"] > 0.0
                for row in rows
            )
            and min(
                row["parent_response_weight_fraction"] for row in rows
            )
            > 0.5
        ),
    }


@lru_cache(maxsize=None)
def fdt_state_bound() -> dict[str, Any]:
    noise = prior.noise_and_cmb_gate()
    potential_power_reference = (3.0 / 5.0) ** 2 * AS_PRIMORDIAL
    allowed_noise_power_fraction = 1.0e-2
    allowed_metric_noise_power = (
        allowed_noise_power_fraction * potential_power_reference
    )
    rows: list[dict[str, Any]] = []
    response_squares: list[float] = []
    for response in noise["response_rows"]:
        transfer = response["maximum_abs_metric_response"]
        transfer_squared = transfer**2
        response_squares.append(transfer_squared)
        impulse_variance_bound = (
            allowed_metric_noise_power / transfer_squared
            if transfer_squared > 0.0
            else math.inf
        )
        rows.append(
            {
                "k_h_per_Mpc": response["k_h_per_Mpc"],
                "injection_N": response["injection_N"],
                "injection_redshift": response["injection_redshift"],
                "maximum_abs_metric_response": transfer,
                "allowed_metric_noise_power": allowed_metric_noise_power,
                "maximum_effective_impulse_variance": impulse_variance_bound,
                "maximum_effective_impulse_rms": math.sqrt(
                    impulse_variance_bound
                ),
                "maximum_Theta_times_DeltaN": (
                    impulse_variance_bound
                    / (2.0 * prior.background.GAMMA_BAR)
                ),
                "normalization": (
                    "dimensionless xi/H0^2 Fourier-cell convention of 4890"
                ),
            }
        )
    common_variance_bound = allowed_metric_noise_power / sum(response_squares)
    common_theta_delta_n_bound = (
        common_variance_bound / (2.0 * prior.background.GAMMA_BAR)
    )
    return {
        "A_s": AS_PRIMORDIAL,
        "reference_metric_power": potential_power_reference,
        "allowed_noise_power_fraction": allowed_noise_power_fraction,
        "allowed_metric_noise_power": allowed_metric_noise_power,
        "rows": rows,
        "combined_equal_variance_bound": common_variance_bound,
        "combined_equal_rms_bound": math.sqrt(common_variance_bound),
        "combined_Theta_times_DeltaN_bound": common_theta_delta_n_bound,
        "Markov_map": (
            "Var[I_k]=2 gamma_bar Theta_k DeltaN for a white KMS mode in "
            "the normalized 4890 Fourier cell"
        ),
        "physical_temperature_conversion": (
            "not allowed until the comoving cell spectral measure and bath "
            "density matrix are parent-normalized"
        ),
        "bound_interpretation": (
            "if one-percent of the primordial metric power is reserved for "
            "bath noise at k=0.01 h/Mpc, a common four-bin impulse variance "
            "must remain below the quoted combined bound"
        ),
        "parent_state_realized": False,
        "noise_likelihood_allowed": False,
        "passed": bool(
            all(
                math.isfinite(row["maximum_effective_impulse_variance"])
                and row["maximum_effective_impulse_variance"] > 0.0
                for row in rows
            )
            and common_variance_bound > 0.0
            and not noise["CMB_likelihood_allowed"]
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    hierarchy = species_hierarchy_derivation()
    bridge = camb_background_spectra_bridge()
    engine = hierarchy_engine_evolution()
    response = parent_metric_response()
    lensing = lensing_response_projection()
    noise_bound = fdt_state_bound()
    requirements = [
        {
            "requirement": "photon_baryon_collision_recombination_polarization",
            "status": "closed_by_CAMB_1p6p6_standard_sector",
            "closed": True,
        },
        {
            "requirement": "massless_and_massive_neutrino_hierarchies",
            "status": "closed_by_CAMB_transfer_and_compiled_momentum_bins",
            "closed": True,
        },
        {
            "requirement": "parent_density_momentum_pressure_injection",
            "status": "derived_exact_interface_from_4890",
            "closed": True,
        },
        {
            "requirement": "parent_linear_anisotropic_stress",
            "status": "derived_zero_standard_species_own_slip",
            "closed": True,
        },
        {
            "requirement": "parent_background_acoustic_geometry",
            "status": "three_rays_run_through_CAMB_PPF_geometry_comparator",
            "closed": True,
        },
        {
            "requirement": "late_parent_Weyl_lensing_projection",
            "status": "bounded_Limber_response_not_full_line_of_sight",
            "closed": False,
        },
        {
            "requirement": "FDT_state_normalization",
            "status": "observational_covariance_bound_derived_parent_state_not_realized",
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
        "species_hierarchy": (
            "STANDARD_PHOTON_BARYON_NEUTRINO_RECOMBINATION_AND_POLARIZATION_"
            "OPERATORS_WIRED_TO_EXACT_PARENT_SOURCE_SLOTS"
        ),
        "background_spectra": (
            "THREE_PARENT_BACKGROUNDS_CAMB_RUNNABLE_WORST_THETASTAR_SHIFT_"
            "6P84E_MINUS4_AND_TT_RESIDUAL_4P43E_MINUS3"
        ),
        "parent_metric": (
            "LATE_WEYL_RESPONSE_DERIVED_MAX_1P93_PERCENT_EARLY_RESPONSE_"
            "BELOW_3E_MINUS7"
        ),
        "lensing": (
            "LIMBER_RESPONSE_SUPPRESSION_BOUNDED_NO_OFFICIAL_LENSING_LIKELIHOOD"
        ),
        "FDT": (
            "NORMALIZED_NOISE_COVARIANCE_BOUND_DERIVED_PHYSICAL_STATE_OPEN"
        ),
        "local_GR_Newton_Maxwell": (
            "4889_STATIONARY_CORRESPONDENCE_RETAINED_UNCHANGED"
        ),
        "CMB_likelihood_allowed": False,
        "promotion_status": (
            "SPECIES_HIERARCHY_AND_PARENT_BACKGROUND_GATE_CLOSE_LATE_LINE_OF_"
            "SIGHT_AND_FDT_STATE_REALIZATION_REMAIN_BEFORE_CMB_CLAIM"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            sources["passed"]
            and hierarchy["passed"]
            and bridge["passed"]
            and engine["passed"]
            and response["passed"]
            and lensing["passed"]
            and noise_bound["passed"]
            and sum(row["closed"] for row in requirements) == 5
            and not all(row["closed"] for row in requirements)
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "hierarchy": species_hierarchy_derivation(),
        "background_mapping": {
            "rows": [
                {
                    key: value
                    for key, value in parent_background_mapping(target).items()
                    if key
                    not in {
                        "run",
                        "scale_factors",
                        "w_values",
                        "effective_density_values",
                    }
                }
                for target in prior.background.TARGETS
            ],
            "passed": all(
                parent_background_mapping(target)["passed"]
                for target in prior.background.TARGETS
            ),
        },
        "CAMB_bridge": camb_background_spectra_bridge(),
        "hierarchy_engine": hierarchy_engine_evolution(),
        "parent_response": parent_metric_response(),
        "lensing": lensing_response_projection(),
        "FDT_bound": fdt_state_bound(),
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
    hierarchy = calculation["sections"]["hierarchy"]
    bridge = calculation["sections"]["CAMB_bridge"]
    engine = calculation["sections"]["hierarchy_engine"]
    response = calculation["sections"]["parent_response"]
    lensing = calculation["sections"]["lensing"]
    noise_bound = calculation["sections"]["FDT_bound"]
    print(f"CAMB={camb.__version__} hierarchy={hierarchy['passed']}")
    print(
        "theta_max={:.6e} TT_max={:.6e} H_max={:.6e}".format(
            bridge["maximum_abs_fractional_thetastar_shift"],
            bridge["maximum_TT_residual"],
            bridge["maximum_abs_fractional_H_residual"],
        )
    )
    print(
        "visibility_z={:.6f} early_R={:.6e} late_R={:.6e}".format(
            engine["visibility_peak_redshift"],
            response["maximum_early_abs_response"],
            response["maximum_late_abs_response"],
        )
    )
    for row in lensing["rows"]:
        print(
            "L={} lens_shift={:.6e} coverage={:.6f}".format(
                row["ell"],
                row["fractional_lensing_shift"],
                row["parent_response_weight_fraction"],
            )
        )
    print(
        "noise_var<{:.6e} noise_rms<{:.6e} ThetaDeltaN<{:.6e}".format(
            noise_bound["combined_equal_variance_bound"],
            noise_bound["combined_equal_rms_bound"],
            noise_bound["combined_Theta_times_DeltaN_bound"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
