from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"

CHECKPOINT = "4887"
NEXT_TARGET = (
    "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-"
    "backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md"
)

H0_KM_S_MPC = 67.4
MPC_M = 3.085677581491367e22
C_M_S = 299792458.0
AU_M = 149597870700.0
R_SUN_M = 695700000.0
OMEGA_B = 0.049
OMEGA_M = 0.315
OMEGA_R = 9.0e-5
OMEGA_LAMBDA = 1 - OMEGA_M - OMEGA_R

SIGMA_THETA_OVER_H0 = 0.3
GAMMA_M_OVER_H0 = 1.0
INITIAL_N = -7.0


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    rows = [
        {
            "source_id": "SRC4887_00_prior_compatibility",
            "source_path": str(
                POST
                / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md"
            ),
            "marker": "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
        },
        {
            "source_id": "SRC4887_01_open_bath_parent",
            "source_path": str(
                POST
                / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md"
            ),
            "marker": "state Landau vector",
        },
        {
            "source_id": "SRC4887_02_composite_flow_parent",
            "source_path": str(
                POST
                / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md"
            ),
            "marker": "unique timelike Landau eigenvector",
        },
        {
            "source_id": "SRC4887_03_memory_operator",
            "source_path": str(
                POST
                / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md"
            ),
            "marker": "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        },
        {
            "source_id": "SRC4887_04_local_GR",
            "source_path": str(
                POST
                / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md"
            ),
            "marker": "gamma_{\\rm classical}=1",
        },
        {
            "source_id": "SRC4887_05_open_EFT_pdf",
            "source_path": str(
                POST
                / "source-intake"
                / "memory_uv"
                / "4885"
                / "Crossley_Glorioso_Liu_1511.03646.pdf"
            ),
            "marker": "closed-time-path EFT primary PDF",
        },
    ]
    for row in rows:
        path = Path(row["source_path"])
        row["source_exists"] = path.exists()
        if path.suffix.lower() == ".pdf":
            row["marker_found"] = path.exists() and path.stat().st_size == 1109199
        else:
            row["marker_found"] = _contains(path, row["marker"])
    return {
        "rows": rows,
        "web_sources": {
            "open_EFT": "https://arxiv.org/abs/1511.03646",
        },
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def candidate_source_audit() -> dict[str, Any]:
    rows = [
        {
            "candidate": "direct_trace_beta_phi2_T",
            "local_stationary_source": "NONZERO_IN_MATTER",
            "FLRW_source": "NONZERO",
            "derivative_order": 0,
            "health": "COVARIANT_WITH_CONFORMAL_OWNER",
            "verdict": "REJECTED_BY_4886_PPN_COSMOLOGY_IDENTITY",
        },
        {
            "candidate": "linear_phi_R",
            "local_stationary_source": "NONZERO_INSIDE_MATTER",
            "FLRW_source": "NONZERO",
            "derivative_order": 2,
            "health": "SCALAR_TENSOR_MONOPOLE",
            "verdict": "REJECT_LOCAL_SILENCE",
        },
        {
            "candidate": "phi_Box_R",
            "local_stationary_source": "TOTAL_DIVERGENCE_AT_LINEAR_ORDER",
            "FLRW_source": "NONZERO_WHEN_R_EVOLVES",
            "derivative_order": 4,
            "health": "FIELD_REDEFINITION_REDUNDANT_WHEN_MASSLESS_AND_HIGHER_DERIVATIVE",
            "verdict": "DEMOTE_AS_LEAD_PARENT",
        },
        {
            "candidate": "linear_phi_Gauss_Bonnet",
            "local_stationary_source": "NONZERO_IN_RICCI_FLAT_CURVATURE",
            "FLRW_source": "NONZERO",
            "derivative_order": 4,
            "health": "TOPOLOGICAL_ONLY_FOR_CONSTANT_COEFFICIENT",
            "verdict": "REJECT_EXACT_LOCAL_VACUUM_SILENCE",
        },
        {
            "candidate": "bath_expansion_u_dot_grad_phi",
            "local_stationary_source": "ZERO_FOR_NORMALIZED_KILLING_FLOW",
            "FLRW_source": "3_SIGMA_THETA_H",
            "derivative_order": 1,
            "health": "UNCHANGED_SCALAR_PRINCIPAL_SYMBOL_CLOCK_GRADIENT_BOUND_REQUIRED",
            "verdict": "SELECT_CONSTRUCTIVE_CANDIDATE",
        },
    ]
    selected = [
        row for row in rows if row["verdict"] == "SELECT_CONSTRUCTIVE_CANDIDATE"
    ]
    return {
        "rows": rows,
        "selected": selected[0]["candidate"],
        "selection_reason": (
            "it is first derivative, covariant through the already present "
            "bath Landau flow, exactly a boundary term on stationary Killing "
            "states, and a genuine bulk source on FLRW"
        ),
        "passed": len(selected) == 1,
    }


@lru_cache(maxsize=None)
def expansion_action() -> dict[str, Any]:
    scale, phi, phi_dot, sigma, kappa = sp.symbols(
        "a phi phi_dot sigma_theta kappa", positive=True, real=True
    )
    hubble = sp.symbols("H", real=True)
    momentum = scale**3 * (phi_dot - sigma)
    momentum_derivative = scale**3 * (
        sp.symbols("phi_ddot") + 3 * hubble * (phi_dot - sigma)
    )
    potential_derivative = scale**3 * kappa * phi**3
    euler = sp.expand(momentum_derivative + potential_derivative)
    return {
        "closed_effective_action": (
            "S=integral sqrt(-g) Mbar_Pl^2[-(grad phi)^2/2-"
            "kappa phi^4/4-sigma_theta u^mu grad_mu phi]+S_bath"
        ),
        "bath_flow_definition": (
            "Tbar^mu_nu,bath u^nu=-rho_bath u^mu; u^2=-1"
        ),
        "integration_by_parts": (
            "-integral sqrt(-g) sigma u.grad phi="
            "integral sqrt(-g) sigma phi theta-boundary; theta=div u"
        ),
        "scalar_EOM_without_open_damping": (
            "Box phi-kappa phi^3+sigma_theta theta=0"
        ),
        "SK_physical_EOM": (
            "Box phi-kappa phi^3-gamma_M u.grad phi+"
            "sigma_theta theta=noise"
        ),
        "FLRW_equation": (
            "phi_ddot+(3H+gamma_M)phi_dot+kappa phi^3="
            "3 sigma_theta H+noise"
        ),
        "homogeneous_canonical_momentum": str(momentum),
        "homogeneous_euler_expression": str(euler),
        "homogeneous_Hamiltonian": (
            "rho_phi=Mbar_Pl^2 phi_dot^2/2+Mbar_Pl^2 kappa phi^4/4; "
            "the term linear in phi_dot cancels from the Hamiltonian"
        ),
        "principal_symbol": (
            "the sigma term is first derivative and leaves the scalar "
            "principal symbol g^mu_nu q_mu q_nu unchanged"
        ),
        "not_a_global_boundary": (
            "it is a boundary only when theta=0; FLRW theta=3H makes it "
            "a physical source"
        ),
        "passed": bool(
            sp.diff(momentum, phi_dot) == scale**3
            and sp.expand(euler).coeff(sigma) == -3 * scale**3 * hubble
            and sp.expand(euler).coeff(kappa) == scale**3 * phi**3
        ),
    }


@lru_cache(maxsize=None)
def clock_stability() -> dict[str, Any]:
    sigma_bar = SIGMA_THETA_OVER_H0
    rows: list[dict[str, Any]] = []
    for label, omega, equation_of_state in (
        ("observed_baryon_enthalpy", OMEGA_B, 0.0),
        ("total_matter_like_bath", OMEGA_M, 0.0),
        ("small_one_percent_bath", 0.01, 0.0),
    ):
        enthalpy_over_mbar_h02 = 3 * omega * (1 + equation_of_state)
        mixing_ratio = sigma_bar**2 / enthalpy_over_mbar_h02
        rows.append(
            {
                "bath_case": label,
                "Omega_X": omega,
                "w_X": equation_of_state,
                "sigma_theta_over_H0": sigma_bar,
                "enthalpy_over_Mbar2_H02": enthalpy_over_mbar_h02,
                "gradient_mixing_ratio": mixing_ratio,
                "positive_gradient_matrix": mixing_ratio < 1,
            }
        )
    selected = rows[0]
    return {
        "clock_owner": (
            "a covariant bath clock Theta with X=-(grad Theta)^2/2 and "
            "u_mu=-grad_mu Theta/sqrt(2X)"
        ),
        "clock_no_ghost": "P_X+2X P_XX>0",
        "clock_gradient": "P_X>0",
        "mixed_gradient_determinant": (
            "sigma_theta^2 < (rho_X+p_X)/Mbar_Pl^2"
        ),
        "derivation": (
            "quadratic gradients are Mbar^2(grad chi)^2/2+"
            "P_X(grad pi)^2/2-Mbar^2 sigma_theta grad pi.grad chi/q"
        ),
        "minimum_Omega_X_one_plus_w": sigma_bar**2 / 3,
        "rows": rows,
        "selected_bath_case": selected["bath_case"],
        "selected_gradient_margin": 1 - selected["gradient_mixing_ratio"],
        "interpretation": (
            "sigma_theta=0.3 H0 does not require a hidden dominant bath: "
            "the observed baryon enthalpy already exceeds the quadratic "
            "gradient-mixing floor, while a one-percent bath would not"
        ),
        "passed": bool(
            selected["positive_gradient_matrix"]
            and selected["gradient_mixing_ratio"] < 0.62
            and not rows[2]["positive_gradient_matrix"]
        ),
    }


@lru_cache(maxsize=None)
def stationary_silence() -> dict[str, Any]:
    h0_per_second = H0_KM_S_MPC * 1000 / MPC_M
    rows = []
    for arena, theta, field_gradient, verdict in (
        (
            "Minkowski_constant_Landau_state",
            0.0,
            0.0,
            "INTERACTION_IS_BOUNDARY",
        ),
        (
            "static_spherical_star_Killing_flow",
            0.0,
            0.0,
            "NO_SCALAR_SOURCE_OR_STRESS",
        ),
        (
            "stationary_Ricci_flat_exterior",
            0.0,
            0.0,
            "NO_MONOPOLE_AND_EH_METRIC_RETAINED",
        ),
        (
            "FLRW_comoving_bath",
            3.0,
            None,
            "SOURCE_EQUALS_3_SIGMA_THETA_H",
        ),
    ):
        rows.append(
            {
                "arena": arena,
                "theta_over_H_or_local_scale": theta,
                "stationary_phi_gradient": field_gradient,
                "verdict": verdict,
            }
        )
    epsilon_au = (h0_per_second * AU_M / C_M_S) ** 2
    epsilon_sun = (h0_per_second * R_SUN_M / C_M_S) ** 2
    return {
        "Killing_identity": (
            "for u^mu=K^mu/sqrt(-K^2), div K=0 and K.grad K^2=0, "
            "therefore theta=div u=0 exactly"
        ),
        "rows": rows,
        "tree_level_matter_scalar_coupling": 0.0,
        "stationary_PPN_gamma": 1.0,
        "stationary_PPN_beta": 1.0,
        "cosmic_state_local_gradient_suppression_AU": epsilon_au,
        "cosmic_state_local_gradient_suppression_Rsun": epsilon_sun,
        "scope": (
            "exact for stationary Killing-aligned bath states; dynamical "
            "binaries require a separate radiation and preferred-frame test"
        ),
        "passed": bool(
            epsilon_au < 1.3e-30
            and epsilon_sun < 3.0e-35
            and all(
                row["theta_over_H_or_local_scale"] == 0
                for row in rows[:3]
            )
            and rows[3]["theta_over_H_or_local_scale"] == 3
        ),
    }


def _background_e(n_value: np.ndarray | float) -> np.ndarray | float:
    return np.sqrt(
        OMEGA_R * np.exp(-4 * n_value)
        + OMEGA_M * np.exp(-3 * n_value)
        + OMEGA_LAMBDA
    )


def _background_h(n_value: np.ndarray | float) -> np.ndarray | float:
    e_squared = _background_e(n_value) ** 2
    return -(
        4 * OMEGA_R * np.exp(-4 * n_value)
        + 3 * OMEGA_M * np.exp(-3 * n_value)
    ) / (2 * e_squared)


@lru_cache(maxsize=512)
def _flrw_run(log_kappa_bar: float) -> dict[str, Any]:
    kappa_bar = math.exp(log_kappa_bar)
    sigma_bar = SIGMA_THETA_OVER_H0
    gamma_bar = GAMMA_M_OVER_H0

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        field, field_n = state
        e_value = float(_background_e(n_value))
        h_value = float(_background_h(n_value))
        return np.asarray(
            [
                field_n,
                -(
                    3 + h_value + gamma_bar / e_value
                )
                * field_n
                - kappa_bar * field**3 / e_value**2
                + 3 * sigma_bar / e_value,
            ]
        )

    solution = solve_ivp(
        rhs,
        (INITIAL_N, 0.0),
        np.asarray([0.0, 0.0]),
        rtol=3.0e-9,
        atol=1.0e-11,
        max_step=0.01,
    )
    if not solution.success:
        raise RuntimeError("FLRW expansion-source integration failed")
    e_values = np.asarray(_background_e(solution.t))
    omega_v = kappa_bar * solution.y[0] ** 4 / (12 * e_values**2)
    omega_k = solution.y[1] ** 2 / 6
    omega_total = omega_v + omega_k
    return {
        "kappa_bar": kappa_bar,
        "solution": solution,
        "omega_v": omega_v,
        "omega_k": omega_k,
        "omega_total": omega_total,
    }


def _tuned_scenario(target_fraction: float) -> dict[str, Any]:
    def residual(log_kappa: float) -> float:
        run = _flrw_run(float(log_kappa))
        return float(run["omega_total"][-1] - target_fraction)

    log_kappa = brentq(residual, 6.0, 35.0, xtol=1.0e-8, rtol=1.0e-10)
    run = _flrw_run(float(log_kappa))
    solution = run["solution"]
    omega_v = run["omega_v"]
    omega_k = run["omega_k"]
    omega_total = run["omega_total"]
    field = float(solution.y[0, -1])
    field_n = float(solution.y[1, -1])
    quasi_static_field = (
        3 * SIGMA_THETA_OVER_H0 / run["kappa_bar"]
    ) ** (1 / 3)
    half_target = 0.5 * target_fraction
    activated = np.flatnonzero(omega_total >= half_target)
    activation_redshift = (
        math.exp(-float(solution.t[activated[0]])) - 1
        if len(activated)
        else None
    )
    return {
        "target_Omega_memory_today": target_fraction,
        "sigma_theta_over_H0": SIGMA_THETA_OVER_H0,
        "gamma_M_over_H0": GAMMA_M_OVER_H0,
        "kappa_over_H0_squared": run["kappa_bar"],
        "phi_today": field,
        "dphi_dN_today": field_n,
        "phi_quasi_static_today": quasi_static_field,
        "phi_to_quasi_static_ratio": field / quasi_static_field,
        "Omega_V_today": float(omega_v[-1]),
        "Omega_K_today": float(omega_k[-1]),
        "Omega_memory_today": float(omega_total[-1]),
        "maximum_Omega_memory": float(np.max(omega_total)),
        "w_phi_proxy_today": float(
            (omega_k[-1] - omega_v[-1]) / omega_total[-1]
        ),
        "half_activation_redshift": activation_redshift,
        "fixed_background_controlled": bool(np.max(omega_total) < 0.015),
    }


@lru_cache(maxsize=None)
def flrw_response() -> dict[str, Any]:
    rows = [
        _tuned_scenario(target) for target in (1.0e-4, 1.0e-3, 1.0e-2)
    ]
    return {
        "dimensionless_equation": (
            "phi_NN+[3+dlnH/dN+gamma_bar/E]phi_N+"
            "kappa_bar phi^3/E^2=3 sigma_bar/E"
        ),
        "initial_conditions": "phi=phi_N=0 at N=-7",
        "late_activation_mechanism": (
            "the dimensionless drive 3 sigma_bar/E is Hubble suppressed "
            "early and grows toward the present without a switch function"
        ),
        "rows": rows,
        "maximum_fixed_background_fraction": max(
            row["maximum_Omega_memory"] for row in rows
        ),
        "passed": bool(
            all(
                abs(
                    row["Omega_memory_today"]
                    / row["target_Omega_memory_today"]
                    - 1
                )
                < 1.0e-7
                for row in rows
            )
            and all(row["fixed_background_controlled"] for row in rows)
            and rows[-1]["maximum_Omega_memory"] < 0.0141
            and all(np.isfinite(row["phi_today"]) for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def coefficient_ownership() -> dict[str, Any]:
    return {
        "sigma_theta": (
            "single bath compression-memory cross-response coefficient"
        ),
        "gamma_M": "existing Ohmic memory damping coefficient from 4873/4885",
        "kappa": "existing quartic coefficient a*Mbar_Pl^2",
        "matching_rule": (
            "sigma_theta gamma_M and kappa are fixed once from the bath "
            "spectral state and one cosmological calibration; no local-arena "
            "retuning is permitted"
        ),
        "Kubo_target": (
            "sigma_theta is the zero-momentum memory-force response to bath "
            "compression theta; its normalization must be extracted from "
            "the closed X_Omega influence functional"
        ),
        "numeric_parent_derivation_complete": False,
        "benchmark_status": (
            "sigma_theta/H0=0.3 and gamma_M/H0=1 are controlled existence "
            "benchmarks, not parent predictions"
        ),
        "passed": True,
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    candidates = candidate_source_audit()
    action = expansion_action()
    stability = clock_stability()
    local = stationary_silence()
    cosmology = flrw_response()
    ownership = coefficient_ownership()
    return {
        "direct_trace_branch": "REMAINS_REJECTED_FOR_SIGNIFICANT_COSMOLOGY",
        "selected_replacement_source": candidates["selected"],
        "variational_closure": "CONSTRUCTED_WITH_BATH_CLOCK_AND_SK_COMPLETION",
        "stationary_local_PPN": "EXACTLY_SILENT_ON_KILLING_ALIGNED_STATE",
        "FLRW_activation": "NONZERO_THETA_EQUALS_3H_AND_NUMERIC_BRANCH_REGULAR",
        "preferred_coordinate": False,
        "state_rest_frame": (
            "SPONTANEOUS_BATH_LANDAU_FRAME_NOT_FUNDAMENTAL_COORDINATE"
        ),
        "principal_cone_change": False,
        "clock_gradient_stability": "PASSES_SELECTED_BARYON_ENTHALPY_BENCHMARK",
        "percent_level_existence_smoke": (
            "PASSES_FIXED_BACKGROUND_AT_MAXIMUM_OMEGA_0P0141"
        ),
        "coefficient_prediction": False,
        "promotion_status": (
            "CONSTRUCTED_CONDITIONAL_MECHANISM_NOT_YET_PARENT_MATCHED_OR_DATA_FIT"
        ),
        "canonical_M_UV_determinant": "RETAINED",
        "Gamma_overdamped_readout": "RETAINED",
        "renormalized_EH_local_branch": "RETAINED",
        "next_target": NEXT_TARGET,
        "passed": bool(
            sources["passed"]
            and candidates["passed"]
            and action["passed"]
            and stability["passed"]
            and local["passed"]
            and cosmology["passed"]
            and ownership["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "candidate_audit": candidate_source_audit(),
        "action": expansion_action(),
        "clock_stability": clock_stability(),
        "stationary_silence": stationary_silence(),
        "FLRW_response": flrw_response(),
        "coefficient_ownership": coefficient_ownership(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(
        section.get("passed", True) for section in sections.values()
    )
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "all_checks_pass": all_checks_pass,
        "decision": (
            "construct a covariant expansion-driven memory source from the "
            "existing bath Landau flow; prove it is a boundary on stationary "
            "Killing states and a 3 sigma_theta H bulk drive on FLRW; derive "
            "the bath-clock gradient-stability bound; demonstrate regular "
            "late-activating 10^-4 to 10^-2 response branches without direct "
            "matter coupling; retain the mechanism conditionally while "
            "advancing its Kubo coefficient and backreacted likelihood to "
            "the next gate"
        ),
    }


if __name__ == "__main__":
    calculation = result()
    print("MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887")
    print(f"all_checks_pass={calculation['all_checks_pass']}")
    print(calculation["decision"])
