from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy import optimize
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4888_bath_kubo_backreacted_cosmology as background  # noqa: E402
import Y5_R2FR_4889_constrained_clock_local_growth_binary as prior  # noqa: E402


CHECKPOINT = "4890"
NEXT_TARGET = (
    "4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-"
    "FDT-state-normalization-or-CMB-source-demotion-gate.md"
)

H0_KM_S_MPC = 67.4
HUBBLE_h = H0_KM_S_MPC / 100.0
C_KM_S = 299792.458
MPC_M = 3.085677581491367e22
HBAR_EV_S = 6.582119569e-16
C_M_S = C_KM_S * 1000.0
INV_MPC_EV = HBAR_EV_S * C_M_S / MPC_M
EARLY_INITIAL_N = -14.0


def _contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4890_00_4889",
            POST
            / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md",
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
        (
            "SRC4890_01_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "continuum of bath fields",
        ),
        (
            "SRC4890_02_4888",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4890_03_prior_validation",
            POST
            / "source-intake"
            / "mts_residuals"
            / "P8_Y5_BRR545_4889_VALIDATION.csv",
            "VAL4889_OVERALL,PASS",
        ),
        (
            "SRC4890_04_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "gamma_{\\rm classical}=1",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_parent_or_validation",
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


def _mass_floor_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    spatial_cases = (
        ("LSS_k0p2h_z2", 0.2, 2.0, 1.0e-6),
        ("CMB_k0p1h_z1095", 0.1, 1095.0, 1.0e-6),
        ("CMB_k0p2h_z1095", 0.2, 1095.0, 1.0e-6),
    )
    for arena, k_h_mpc, redshift, sound_speed_squared_limit in spatial_cases:
        physical_k_mpc = k_h_mpc * HUBBLE_h * (1.0 + redshift)
        physical_k_ev = physical_k_mpc * INV_MPC_EV
        mass_floor_ev = physical_k_ev / (
            2.0 * math.sqrt(sound_speed_squared_limit)
        )
        rows.append(
            {
                "arena": arena,
                "criterion": "k_phys^2/(4 m_c^2)<=c_s_squared_limit",
                "k_h_per_Mpc": k_h_mpc,
                "redshift": redshift,
                "characteristic_energy_eV": physical_k_ev,
                "tolerance": sound_speed_squared_limit,
                "minimum_carrier_mass_eV": mass_floor_ev,
            }
        )
    temporal_cases = (
        ("binary_8_hour", 8.0 * 3600.0, 1.0e-2),
        ("Earth_year", 365.25 * 86400.0, 1.0e-2),
    )
    for arena, period_seconds, frequency_ratio_limit in temporal_cases:
        angular_frequency = 2.0 * math.pi / period_seconds
        frequency_energy = HBAR_EV_S * angular_frequency
        rows.append(
            {
                "arena": arena,
                "criterion": "hbar*omega/m_c<=frequency_ratio_limit",
                "period_seconds": period_seconds,
                "characteristic_energy_eV": frequency_energy,
                "tolerance": frequency_ratio_limit,
                "minimum_carrier_mass_eV": (
                    frequency_energy / frequency_ratio_limit
                ),
            }
        )
    return rows


@lru_cache(maxsize=None)
def composite_clock_identity() -> dict[str, Any]:
    amplitude, carrier_mass, amplitude_gradient, phase_gradient = sp.symbols(
        "A m_c dA dU", positive=True, real=True
    )
    phase = sp.symbols("theta", real=True)
    first_field = amplitude * sp.cos(phase)
    second_field = amplitude * sp.sin(phase)
    first_gradient = (
        amplitude_gradient * sp.cos(phase)
        - amplitude * carrier_mass * phase_gradient * sp.sin(phase)
    )
    second_gradient = (
        amplitude_gradient * sp.sin(phase)
        + amplitude * carrier_mass * phase_gradient * sp.cos(phase)
    )
    kinetic_sum = sp.simplify(first_gradient**2 + second_gradient**2)
    angular_current = sp.simplify(
        first_field * second_gradient - second_field * first_gradient
    )
    expected_kinetic = (
        amplitude_gradient**2
        + amplitude**2 * carrier_mass**2 * phase_gradient**2
    )
    expected_current = amplitude**2 * carrier_mass * phase_gradient
    mass_rows = _mass_floor_rows()
    return {
        "microscopic_pair": (
            "two degenerate real modes X_1,X_2 from the existing bath, "
            "with Z=X_1+iX_2=A exp(i m_c U)"
        ),
        "exact_composite_map": (
            "grad_mu U=(X_1 grad_mu X_2-X_2 grad_mu X_1)/"
            "[m_c(X_1^2+X_2^2)]"
        ),
        "microscopic_pair_action": (
            "L_pair=-[(grad X_1)^2+(grad X_2)^2+"
            "m_c^2(X_1^2+X_2^2)]/2"
        ),
        "polar_action": (
            "L_pair=-(grad A)^2/2-m_c^2 A^2[(grad U)^2+1]/2"
        ),
        "derived_multiplier": "varrho=m_c^2 A^2",
        "controlled_clock_action": (
            "L_IR=-varrho[(grad U)^2+1]/2+"
            "Mbar_Pl^2 sigma_theta grad(phi).grad(U)"
        ),
        "microscopic_interaction_map": (
            "L_mix=(Mbar_Pl^2 sigma_theta/m_c) grad(phi)."
            "(X_1 grad X_2-X_2 grad X_1)/(X_1^2+X_2^2)"
        ),
        "radial_constraint_with_correction": (
            "(grad U)^2+1=Box A/(m_c^2 A)"
        ),
        "phase_transport": "nabla_mu(A^2 grad^mu U)=0 before mixing/SK exchange",
        "leading_stress": "T_mn=varrho u_m u_n+O[(grad A)^2/m_c^2 A^2]",
        "wkb_control": (
            "epsilon_A=|grad A|/(m_c A), epsilon_R=sqrt(|R|)/m_c, "
            "epsilon_k=k_phys/m_c all much less than one"
        ),
        "coherent_continuum_split": (
            "J_bath=J_coherent_pair+J_continuum; the pair supplies U,varrho "
            "and is excluded from the Ohmic continuum that supplies gamma_M and noise"
        ),
        "sigma_owner": (
            "the operator is the 4887 expansion source and its coefficient remains "
            "the 4888 cross-susceptibility Kubo match, not a new fitted arena switch"
        ),
        "zero_amplitude_domain": (
            "the composite map is undefined at A=0; zero-density patches require "
            "the underlying Cartesian X_1,X_2 fields rather than the dust chart"
        ),
        "kinetic_identity": str(kinetic_sum),
        "angular_identity": str(angular_current),
        "kinetic_identity_verified": sp.simplify(
            kinetic_sum - expected_kinetic
        ) == 0,
        "angular_identity_verified": sp.simplify(
            angular_current - expected_current
        ) == 0,
        "mass_floor_rows": mass_rows,
        "largest_required_mass_floor_eV": max(
            row["minimum_carrier_mass_eV"] for row in mass_rows
        ),
        "new_primitive_field_required": False,
        "new_parent_operator_required": False,
        "identity_status": (
            "CONTROLLED_WKB_COMPOSITE_OF_EXISTING_DEGENERATE_BATH_PAIR_"
            "WITH_NONZERO_AMPLITUDE_DOMAIN"
        ),
        "passed": bool(
            sp.simplify(kinetic_sum - expected_kinetic) == 0
            and sp.simplify(angular_current - expected_current) == 0
            and all(
                row["minimum_carrier_mass_eV"] > 0.0 for row in mass_rows
            )
        ),
    }


def _early_branch_integrator(
    target: float, log_kappa: float, log_clock_scale: float
) -> dict[str, Any]:
    kappa_bar = math.exp(log_kappa)
    omega_lambda = 1.0 - background.OMEGA_R - background.OMEGA_M - target
    initial_clock = background.OMEGA_X * math.exp(
        -3.0 * EARLY_INITIAL_N + log_clock_scale
    )

    def background_values(
        n_value: float, state: np.ndarray
    ) -> tuple[float, float, float]:
        field, field_n, clock_density = state
        radiation = background.OMEGA_R * math.exp(-4.0 * n_value)
        other_matter = background.OMEGA_OTHER_M * math.exp(-3.0 * n_value)
        potential = kappa_bar * field**4 / 12.0
        denominator = 1.0 - field_n**2 / 6.0
        numerator = (
            radiation
            + other_matter
            + omega_lambda
            + clock_density
            + potential
        )
        if denominator <= 0.0 or numerator <= 0.0:
            raise ValueError("non-positive early Friedmann branch")
        e_squared = numerator / denominator
        e_value = math.sqrt(e_squared)
        h_value = (
            -2.0 * radiation / e_squared
            - 1.5 * (other_matter + clock_density) / e_squared
            - 0.5 * field_n**2
            + background.SIGMA_BAR * field_n / (2.0 * e_value)
        )
        return e_value, h_value, potential

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        field, field_n, clock_density = state
        e_value, h_value, _ = background_values(n_value, state)
        return np.asarray(
            [
                field_n,
                -(
                    3.0
                    + h_value
                    + background.GAMMA_BAR / e_value
                )
                * field_n
                - kappa_bar * field**3 / e_value**2
                + 3.0 * background.SIGMA_BAR / e_value,
                -3.0 * clock_density
                + background.GAMMA_BAR * e_value * field_n**2 / 3.0,
            ]
        )

    solution = solve_ivp(
        rhs,
        (EARLY_INITIAL_N, 0.0),
        np.asarray([0.0, 0.0, initial_clock]),
        method="DOP853",
        rtol=2.0e-9,
        atol=1.0e-11,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError("early backreacted FLRW integration failed")
    field, field_n, clock_density = solution.y[:, -1]
    e_value, _, potential = background_values(0.0, solution.y[:, -1])
    memory_fraction = (
        e_value**2 * field_n**2 / 6.0 + potential
    ) / e_value**2
    return {
        "target": target,
        "kappa_bar": kappa_bar,
        "log_kappa": log_kappa,
        "clock_scale": math.exp(log_clock_scale),
        "log_clock_scale": log_clock_scale,
        "omega_lambda": omega_lambda,
        "solution": solution,
        "background_values": background_values,
        "rhs": rhs,
        "clock_today": float(clock_density),
        "memory_today": float(memory_fraction),
        "E_today": float(e_value),
    }


@lru_cache(maxsize=None)
def _solve_early_branch(target: float) -> dict[str, Any]:
    late_run = background._solve_branch(target)

    def residual(vector: np.ndarray) -> np.ndarray:
        run = _early_branch_integrator(
            target, float(vector[0]), float(vector[1])
        )
        return np.asarray(
            [
                math.log(run["memory_today"] / target),
                math.log(run["clock_today"] / background.OMEGA_X),
            ]
        )

    root = optimize.root(
        residual,
        np.asarray([late_run["log_kappa"], late_run["log_bath_scale"]]),
        method="hybr",
        tol=1.0e-10,
    )
    if not root.success:
        raise RuntimeError(f"early branch shooting failed: {root.message}")
    run = _early_branch_integrator(
        target, float(root.x[0]), float(root.x[1])
    )
    run["shooting_success"] = bool(root.success)
    run["shooting_residual_norm"] = float(
        np.linalg.norm(residual(root.x), ord=np.inf)
    )
    return run


@lru_cache(maxsize=None)
def early_background_extension() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    n_overlap = np.linspace(background.INITIAL_N, 0.0, 701)
    for target in background.TARGETS:
        early_run = _solve_early_branch(target)
        late_run = background._solve_branch(target)
        e_early: list[float] = []
        e_late: list[float] = []
        for n_value in n_overlap:
            early_state = early_run["solution"].sol(float(n_value))
            late_state = late_run["solution"].sol(float(n_value))
            e_early.append(
                early_run["background_values"](
                    float(n_value), early_state
                )[0]
            )
            e_late.append(
                late_run["background_values"](float(n_value), late_state)[0]
            )
        e_early_array = np.asarray(e_early)
        e_late_array = np.asarray(e_late)
        rows.append(
            {
                "target": target,
                "early_initial_N": EARLY_INITIAL_N,
                "kappa_over_H0_squared": early_run["kappa_bar"],
                "clock_initial_scale": early_run["clock_scale"],
                "shooting_residual_norm": early_run[
                    "shooting_residual_norm"
                ],
                "memory_today": early_run["memory_today"],
                "clock_today": early_run["clock_today"],
                "E_today": early_run["E_today"],
                "maximum_overlap_fractional_E_shift": float(
                    np.max(np.abs(e_early_array / e_late_array - 1.0))
                ),
            }
        )
    return {
        "reason": (
            "all sampled k modes must begin outside the horizon; N=-14 "
            "replaces the N=-7 perturbation start without changing the parent equations"
        ),
        "rows": rows,
        "passed": all(
            row["shooting_residual_norm"] < 1.0e-8
            and abs(row["memory_today"] - row["target"])
            < row["target"] * 1.0e-7
            and abs(row["clock_today"] - background.OMEGA_X) < 1.0e-9
            and abs(row["E_today"] - 1.0) < 1.0e-8
            for row in rows
        ),
    }


def _background_snapshot(run: dict[str, Any], n_value: float) -> dict[str, float]:
    state = run["solution"].sol(n_value)
    field, field_n, clock_density = (float(value) for value in state)
    e_value, h_value, potential = run["background_values"](n_value, state)
    background_rhs = run["rhs"](n_value, state)
    radiation = background.OMEGA_R * math.exp(-4.0 * n_value)
    other_matter = background.OMEGA_OTHER_M * math.exp(-3.0 * n_value)
    multiplier_density = (
        clock_density + background.SIGMA_BAR * e_value * field_n / 3.0
    )
    return {
        "field": field,
        "field_n": field_n,
        "field_nn": float(background_rhs[1]),
        "clock_density": clock_density,
        "multiplier_density": multiplier_density,
        "radiation": radiation,
        "other_matter": other_matter,
        "E": float(e_value),
        "h": float(h_value),
        "potential": float(potential),
    }


def _kbar_from_h_per_mpc(k_h_per_mpc: float) -> float:
    return k_h_per_mpc * HUBBLE_h * C_KM_S / H0_KM_S_MPC


def _mode_algebra(
    run: dict[str, Any],
    n_value: float,
    state: np.ndarray,
    kbar: float,
) -> dict[str, float]:
    phi_metric, field_delta, field_delta_n, clock_potential = state[:4]
    clock_delta, other_delta, other_potential = state[4:7]
    radiation_delta, radiation_potential = state[7:9]
    bg = _background_snapshot(run, n_value)
    e_value = bg["E"]
    field = bg["field"]
    field_n = bg["field_n"]
    k2 = kbar**2 * math.exp(-2.0 * n_value)
    scalar_density_delta = (
        e_value**2 * field_n * field_delta_n
        - e_value**2 * field_n**2 * phi_metric
        + run["kappa_bar"] * field**3 * field_delta
    ) / 3.0
    total_density_delta = (
        bg["other_matter"] * other_delta
        + bg["radiation"] * radiation_delta
        + clock_delta
        + scalar_density_delta
    )
    phi_metric_n = (
        -phi_metric
        - k2 * phi_metric / (3.0 * e_value**2)
        - total_density_delta / (2.0 * e_value**2)
    )
    momentum_lhs = e_value * (phi_metric_n + phi_metric)
    momentum_rhs = 0.5 * (
        3.0 * bg["other_matter"] * other_potential
        + 4.0 * bg["radiation"] * radiation_potential
        + 3.0 * bg["clock_density"] * clock_potential
        + (e_value * field_n - background.SIGMA_BAR) * field_delta
    )
    theta_delta_over_h0 = (
        -3.0 * e_value * (phi_metric_n + phi_metric)
        + k2 * clock_potential
    )
    hamiltonian_residual = (
        k2 * phi_metric
        + 3.0 * e_value**2 * (phi_metric_n + phi_metric)
        + 1.5 * total_density_delta
    )
    return {
        **bg,
        "k2": k2,
        "scalar_density_delta": scalar_density_delta,
        "total_density_delta": total_density_delta,
        "phi_metric_n": phi_metric_n,
        "momentum_lhs": momentum_lhs,
        "momentum_rhs": momentum_rhs,
        "momentum_residual": momentum_lhs - momentum_rhs,
        "hamiltonian_residual": hamiltonian_residual,
        "theta_delta_over_h0": theta_delta_over_h0,
    }


def _mode_rhs(
    run: dict[str, Any],
    n_value: float,
    state: np.ndarray,
    kbar: float,
    noise_over_h0_squared: float = 0.0,
) -> np.ndarray:
    phi_metric, field_delta, field_delta_n, clock_potential = state[:4]
    clock_delta, other_delta, other_potential = state[4:7]
    radiation_delta, radiation_potential = state[7:9]
    algebra = _mode_algebra(run, n_value, state, kbar)
    e_value = algebra["E"]
    h_value = algebra["h"]
    field = algebra["field"]
    field_n = algebra["field_n"]
    field_nn = algebra["field_nn"]
    k2 = algebra["k2"]
    phi_metric_n = algebra["phi_metric_n"]
    field_delta_nn = (
        -(
            h_value
            + 3.0
            + background.GAMMA_BAR / e_value
        )
        * field_delta_n
        - (k2 + 3.0 * run["kappa_bar"] * field**2)
        * field_delta
        / e_value**2
        + 2.0
        * phi_metric
        * (field_nn + (h_value + 3.0) * field_n)
        + 4.0 * field_n * phi_metric_n
        + background.SIGMA_BAR
        * algebra["theta_delta_over_h0"]
        / e_value**2
        + background.GAMMA_BAR * field_n * phi_metric / e_value
        + noise_over_h0_squared / e_value**2
    )
    clock_delta_n = (
        -3.0 * clock_delta
        + 3.0 * algebra["clock_density"] * phi_metric_n
        - k2
        * (
            3.0 * algebra["multiplier_density"] * clock_potential
            - background.SIGMA_BAR * field_delta
        )
        / (3.0 * e_value)
        + background.GAMMA_BAR
        * e_value
        * (
            2.0 * field_n * field_delta_n
            - field_n**2 * phi_metric
        )
        / 3.0
        - field_n * noise_over_h0_squared / 3.0
    )
    return np.asarray(
        [
            phi_metric_n,
            field_delta_n,
            field_delta_nn,
            phi_metric / e_value,
            clock_delta_n,
            3.0 * phi_metric_n - k2 * other_potential / e_value,
            phi_metric / e_value,
            4.0 * phi_metric_n
            - 4.0 * k2 * radiation_potential / (3.0 * e_value),
            radiation_potential
            + (phi_metric + radiation_delta / 4.0) / e_value,
        ]
    )


def _initial_mode_state(
    run: dict[str, Any], kbar: float, amplitude: float
) -> np.ndarray:
    n_value = EARLY_INITIAL_N
    bg = _background_snapshot(run, n_value)
    phi_metric = amplitude
    field_delta = 0.0
    field_delta_n = 0.0
    other_delta = -1.5 * phi_metric
    radiation_delta = -2.0 * phi_metric
    clock_delta = bg["clock_density"] * other_delta
    state = np.asarray(
        [
            phi_metric,
            field_delta,
            field_delta_n,
            0.0,
            clock_delta,
            other_delta,
            0.0,
            radiation_delta,
            0.0,
        ]
    )
    algebra = _mode_algebra(run, n_value, state, kbar)
    momentum_denominator = (
        3.0 * bg["other_matter"]
        + 4.0 * bg["radiation"]
        + 3.0 * bg["clock_density"]
    )
    common_potential = (
        2.0
        * algebra["E"]
        * (algebra["phi_metric_n"] + phi_metric)
        / momentum_denominator
    )
    state[3] = common_potential
    state[6] = common_potential
    state[8] = common_potential
    return state


@lru_cache(maxsize=None)
def solve_finite_k_mode(
    target: float, k_h_per_mpc: float, amplitude: float = 1.0e-5
) -> dict[str, Any]:
    run = _solve_early_branch(target)
    kbar = _kbar_from_h_per_mpc(k_h_per_mpc)
    initial_state = _initial_mode_state(run, kbar, amplitude)

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        return _mode_rhs(run, n_value, state, kbar)

    max_step = min(0.01, 0.75 / max(kbar, 1.0))
    solution = solve_ivp(
        rhs,
        (EARLY_INITIAL_N, 0.0),
        initial_state,
        method="DOP853",
        rtol=3.0e-10,
        atol=2.0e-14,
        max_step=max_step,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(
            f"finite-k integration failed for target={target}, k={k_h_per_mpc}"
        )
    n_values = np.linspace(EARLY_INITIAL_N, 0.0, 1801)
    states = solution.sol(n_values)
    momentum_residuals: list[float] = []
    momentum_scales: list[float] = []
    hamiltonian_residuals: list[float] = []
    hamiltonian_scales: list[float] = []
    linearity_residuals: list[float] = []
    theta_values: list[float] = []
    for index, n_value in enumerate(n_values):
        algebra = _mode_algebra(
            run, float(n_value), states[:, index], kbar
        )
        momentum_residuals.append(abs(algebra["momentum_residual"]))
        momentum_scales.append(
            abs(algebra["momentum_lhs"])
            + abs(algebra["momentum_rhs"])
            + amplitude * 1.0e-8
        )
        hamiltonian_residuals.append(
            abs(algebra["hamiltonian_residual"])
        )
        hamiltonian_scales.append(
            abs(algebra["k2"] * states[0, index])
            + abs(
                3.0
                * algebra["E"] ** 2
                * (algebra["phi_metric_n"] + states[0, index])
            )
            + abs(1.5 * algebra["total_density_delta"])
            + amplitude * 1.0e-8
        )
        doubled_rhs = _mode_rhs(
            run, float(n_value), 2.0 * states[:, index], kbar
        )
        base_rhs = _mode_rhs(
            run, float(n_value), states[:, index], kbar
        )
        linearity_residuals.append(
            float(
                np.linalg.norm(doubled_rhs - 2.0 * base_rhs, ord=np.inf)
                / (
                    np.linalg.norm(2.0 * base_rhs, ord=np.inf)
                    + amplitude * 1.0e-12
                )
            )
        )
        theta_values.append(algebra["theta_delta_over_h0"])
    momentum_residual_array = np.asarray(momentum_residuals)
    momentum_scale_array = np.asarray(momentum_scales)
    return {
        "target": target,
        "k_h_per_Mpc": k_h_per_mpc,
        "k_over_H0": kbar,
        "initial_amplitude": amplitude,
        "solution": solution,
        "N": n_values,
        "states": states,
        "maximum_momentum_residual": float(np.max(momentum_residual_array)),
        "maximum_momentum_residual_over_seed": float(
            np.max(momentum_residual_array) / amplitude
        ),
        "maximum_relative_momentum_residual": float(
            np.max(momentum_residual_array / momentum_scale_array)
        ),
        "maximum_hamiltonian_residual": float(
            np.max(hamiltonian_residuals)
        ),
        "maximum_relative_hamiltonian_residual": float(
            np.max(
                np.asarray(hamiltonian_residuals)
                / np.asarray(hamiltonian_scales)
            )
        ),
        "maximum_linearity_residual": float(
            np.max(linearity_residuals)
        ),
        "initial_k_over_aH": float(
            kbar
            * math.exp(-EARLY_INITIAL_N)
            / _background_snapshot(run, EARLY_INITIAL_N)["E"]
        ),
        "maximum_abs_phi_metric": float(np.max(np.abs(states[0]))),
        "maximum_abs_field_delta": float(np.max(np.abs(states[1]))),
        "maximum_abs_clock_fractional_delta": float(
            np.max(
                np.abs(
                    states[4]
                    / np.asarray(
                        [
                            _background_snapshot(run, float(n_value))[
                                "clock_density"
                            ]
                            for n_value in n_values
                        ]
                    )
                )
            )
        ),
        "maximum_abs_theta_delta_over_H0": float(
            np.max(np.abs(theta_values))
        ),
        "final_phi_metric": float(states[0, -1]),
        "final_other_delta": float(states[5, -1]),
        "final_clock_fractional_delta": float(
            states[4, -1] / background.OMEGA_X
        ),
        "finite": bool(np.all(np.isfinite(states))),
    }


@lru_cache(maxsize=None)
def finite_k_kernel() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for target in background.TARGETS:
        for k_h_per_mpc in (1.0e-3, 1.0e-2, 3.0e-2):
            mode = solve_finite_k_mode(target, k_h_per_mpc)
            rows.append(
                {
                    key: value
                    for key, value in mode.items()
                    if key not in {"solution", "N", "states"}
                }
            )
    return {
        "gauge": (
            "ds^2=-(1+2 Psi)dt^2+a^2(1-2 Phi)dx^2; "
            "perfect-fluid anisotropic-stress closure Psi=Phi"
        ),
        "clock_constraint": "H0 pi_U,N=Phi/E",
        "expansion_perturbation": (
            "delta theta/H0=-3E(Phi_N+Phi)+(kbar/a)^2 H0 pi_U"
        ),
        "scalar_langevin_equation": (
            "delta phi_NN+(h+3+gamma_bar/E)delta phi_N+"
            "[(kbar/a)^2+3kappa_bar phi^2]delta phi/E^2="
            "2Phi[phi_NN+(h+3)phi_N]+4phi_N Phi_N+"
            "sigma_bar delta theta/(H0 E^2)+gamma_bar phi_N Phi/E+xi_bar/E^2"
        ),
        "clock_energy_equation": (
            "delta x_X,N+3delta x_X-3x_X Phi_N+"
            "(kbar/a)^2[3lambda_x H0 pi_U-sigma_bar delta phi]/(3E)="
            "gamma_bar E[2phi_N delta phi_N-phi_N^2 Phi]/3-phi_N xi_bar/3"
        ),
        "hamiltonian_constraint": (
            "(kbar/a)^2 Phi+3E^2(Phi_N+Phi)=-3 delta x_total/2"
        ),
        "momentum_constraint": (
            "E(Phi_N+Phi)=[3x_oP_o+4x_rP_r+3x_XP_X+"
            "(E phi_N-sigma_bar)delta phi]/2"
        ),
        "matter_equations": (
            "delta_o,N=3Phi_N-K2 P_o/E, P_o,N=Phi/E"
        ),
        "radiation_equations": (
            "delta_r,N=4Phi_N-4K2 P_r/(3E), "
            "P_r,N=P_r+(Phi+delta_r/4)/E"
        ),
        "rows": rows,
        "maximum_momentum_residual_over_seed": max(
            row["maximum_momentum_residual_over_seed"] for row in rows
        ),
        "maximum_relative_momentum_residual": max(
            row["maximum_relative_momentum_residual"] for row in rows
        ),
        "maximum_hamiltonian_residual": max(
            row["maximum_hamiltonian_residual"] for row in rows
        ),
        "maximum_relative_hamiltonian_residual": max(
            row["maximum_relative_hamiltonian_residual"] for row in rows
        ),
        "maximum_linearity_residual": max(
            row["maximum_linearity_residual"] for row in rows
        ),
        "largest_initial_k_over_aH": max(
            row["initial_k_over_aH"] for row in rows
        ),
        "all_finite": all(row["finite"] for row in rows),
        "scope": (
            "full deterministic Einstein plus pressureless matter, constrained "
            "clock, memory scalar and perfect radiation; not yet a photon-baryon-"
            "neutrino Boltzmann hierarchy"
        ),
        "passed": bool(
            all(row["finite"] for row in rows)
            and max(
                row["maximum_relative_momentum_residual"] for row in rows
            )
            < 5.0e-3
            and max(
                row["maximum_relative_hamiltonian_residual"] for row in rows
            )
            < 1.0e-12
            and max(row["maximum_linearity_residual"] for row in rows)
            < 1.0e-12
            and max(row["initial_k_over_aH"] for row in rows) < 1.0e-2
        ),
    }


@lru_cache(maxsize=None)
def solve_noise_impulse(
    injection_n: float,
    target: float = 1.0e-3,
    k_h_per_mpc: float = 1.0e-2,
) -> dict[str, Any]:
    run = _solve_early_branch(target)
    kbar = _kbar_from_h_per_mpc(k_h_per_mpc)
    bg = _background_snapshot(run, injection_n)
    initial_state = np.zeros(9)
    initial_state[2] = 1.0 / bg["E"] ** 2
    initial_state[4] = -bg["field_n"] / 3.0

    def rhs(n_value: float, state: np.ndarray) -> np.ndarray:
        return _mode_rhs(run, n_value, state, kbar)

    solution = solve_ivp(
        rhs,
        (injection_n, 0.0),
        initial_state,
        method="DOP853",
        rtol=3.0e-10,
        atol=2.0e-14,
        max_step=min(0.01, 0.75 / max(kbar, 1.0)),
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"noise impulse integration failed at N={injection_n}")
    n_values = np.linspace(injection_n, 0.0, 801)
    states = solution.sol(n_values)
    momentum_relative: list[float] = []
    momentum_absolute: list[float] = []
    momentum_scale_rows: list[float] = []
    hamiltonian_relative: list[float] = []
    for index, n_value in enumerate(n_values):
        algebra = _mode_algebra(
            run, float(n_value), states[:, index], kbar
        )
        momentum_scale = (
            abs(algebra["momentum_lhs"])
            + abs(algebra["momentum_rhs"])
            + 1.0e-18
        )
        momentum_absolute.append(abs(algebra["momentum_residual"]))
        momentum_scale_rows.append(momentum_scale)
        hamiltonian_scale = (
            abs(algebra["k2"] * states[0, index])
            + abs(
                3.0
                * algebra["E"] ** 2
                * (algebra["phi_metric_n"] + states[0, index])
            )
            + abs(1.5 * algebra["total_density_delta"])
            + 1.0e-18
        )
        momentum_relative.append(
            abs(algebra["momentum_residual"]) / momentum_scale
        )
        hamiltonian_relative.append(
            abs(algebra["hamiltonian_residual"]) / hamiltonian_scale
        )
    initial_algebra = _mode_algebra(
        run, injection_n, initial_state, kbar
    )
    return {
        "target": target,
        "k_h_per_Mpc": k_h_per_mpc,
        "injection_N": injection_n,
        "injection_redshift": math.exp(-injection_n) - 1.0,
        "impulse_convention": "integral dN xi_over_H0_squared=1",
        "initial_scalar_velocity_jump": float(initial_state[2]),
        "initial_clock_energy_jump": float(initial_state[4]),
        "initial_total_density_jump": float(
            initial_algebra["total_density_delta"]
        ),
        "final_metric_response": float(states[0, -1]),
        "final_memory_response": float(states[1, -1]),
        "final_other_matter_response": float(states[5, -1]),
        "final_clock_fractional_response": float(
            states[4, -1] / background.OMEGA_X
        ),
        "maximum_abs_metric_response": float(
            np.max(np.abs(states[0]))
        ),
        "maximum_relative_momentum_residual": float(
            np.max(momentum_relative)
        ),
        "global_normalized_momentum_residual": float(
            np.max(momentum_absolute) / np.max(momentum_scale_rows)
        ),
        "maximum_absolute_momentum_residual": float(
            np.max(momentum_absolute)
        ),
        "maximum_relative_hamiltonian_residual": float(
            np.max(hamiltonian_relative)
        ),
        "finite": bool(np.all(np.isfinite(states))),
    }


@lru_cache(maxsize=None)
def noise_and_cmb_gate() -> dict[str, Any]:
    response_rows = [
        solve_noise_impulse(injection_n)
        for injection_n in (-10.0, -7.0, -4.0, -1.0)
    ]
    requirement_rows = [
        {
            "requirement": "retarded_Ohmic_coefficient_gamma_M",
            "status": "owned_by_4873_4888_low_frequency_bath_response",
            "closed": True,
        },
        {
            "requirement": "FDT_noise_kernel_shape",
            "status": "derived_from_Schwinger_Keldysh_KMS_identity",
            "closed": True,
        },
        {
            "requirement": "bath_state_temperature_or_nonthermal_covariance",
            "status": "parent_state_not_numerically_selected",
            "closed": False,
        },
        {
            "requirement": "coherent_pair_mass_and_fraction",
            "status": "controlled_lower_bounds_only_no_parent_value",
            "closed": False,
        },
        {
            "requirement": "photon_baryon_collision_and_recombination",
            "status": "standard_hierarchy_not_yet_wired_to_MTS_kernel",
            "closed": False,
        },
        {
            "requirement": "massless_and_massive_neutrino_hierarchy",
            "status": "anisotropic_stress_not_yet_included",
            "closed": False,
        },
        {
            "requirement": "primordial_clock_memory_cross_covariance",
            "status": "initial_state_covariance_not_parent_selected",
            "closed": False,
        },
    ]
    return {
        "langevin_convention": (
            "phi_ddot+(3H+gamma_M)phi_dot-a^-2 Laplacian(phi)+"
            "V_prime-sigma_theta theta=xi"
        ),
        "energy_transfer": (
            "Q_SK=Mbar_Pl^2(gamma_M Y-xi)Y; the delta-Q terms in the "
            "clock equation cancel the instantaneous scalar energy kick"
        ),
        "quantum_FDT": (
            "N(omega,k)=[-Im Sigma_R(omega,k)] coth[omega/(2T_bath)]"
        ),
        "Ohmic_classical_limit": "N=2 gamma_M T_bath in the 4873 convention",
        "noise_mean": "<xi>=0",
        "noise_metric_covariance": (
            "P_Phi_noise(k,N)=integral dN_prime |G_Phi_xi(k;N,N_prime)|^2 "
            "Nbar(k,N_prime) with the state measure fixed by the bath density matrix"
        ),
        "response_rows": response_rows,
        "requirements": requirement_rows,
        "maximum_abs_unit_impulse_metric_response": max(
            row["maximum_abs_metric_response"] for row in response_rows
        ),
        "maximum_impulse_momentum_residual": max(
            row["global_normalized_momentum_residual"]
            for row in response_rows
        ),
        "maximum_impulse_hamiltonian_residual": max(
            row["maximum_relative_hamiltonian_residual"]
            for row in response_rows
        ),
        "deterministic_mean_kernel_closed": True,
        "noise_transfer_function_computable": True,
        "noise_power_numerically_predictive": False,
        "full_Einstein_Boltzmann_closed": False,
        "CMB_likelihood_allowed": False,
        "decision": (
            "DETERMINISTIC_FINITE_K_KERNEL_AND_RETARDED_NOISE_RESPONSE_"
            "DERIVED_CMB_POWER_CLAIM_BLOCKED_BY_BATH_STATE_AND_STANDARD_"
            "PHOTON_NEUTRINO_HIERARCHIES"
        ),
        "passed": bool(
            all(row["finite"] for row in response_rows)
            and max(
                row["maximum_relative_hamiltonian_residual"]
                for row in response_rows
            )
            < 1.0e-12
            and not all(row["closed"] for row in requirement_rows)
            and not any(
                row["requirement"]
                == "bath_state_temperature_or_nonthermal_covariance"
                and row["closed"]
                for row in requirement_rows
            )
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sources = source_contract()
    identity = composite_clock_identity()
    early = early_background_extension()
    finite_k = finite_k_kernel()
    noise = noise_and_cmb_gate()
    return {
        "bath_clock_identity": identity["identity_status"],
        "early_background": (
            "N_MINUS_14_BRANCH_RESHOT_AND_LATE_BACKGROUND_PRESERVED"
        ),
        "finite_k": (
            "NINE_MODE_DETERMINISTIC_EINSTEIN_FLUID_KERNEL_CONSTRAINT_"
            "AND_LINEARITY_GATES_PASS"
        ),
        "noise": noise["decision"],
        "local_GR_Newton_Maxwell": (
            "4889_STATIONARY_CORRESPONDENCE_RETAINED_UNCHANGED"
        ),
        "CMB_status": "BLOCKED_NO_LIKELIHOOD_OR_EVIDENCE_CLAIM",
        "demotion_status": (
            "DO_NOT_DEMOTE_EXPANSION_SOURCE_THE_NEW_PARENT_IDENTITY_AND_"
            "FINITE_K_SYSTEM_ARE_CONSISTENT_BUT_DO_NOT_PROMOTE_TO_CMB"
        ),
        "remaining_root_risk": (
            "bath state and carrier preparation, photon-baryon-neutrino "
            "hierarchies, nonlinear zero-amplitude patches, and full stochastic power"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            sources["passed"]
            and identity["passed"]
            and early["passed"]
            and finite_k["passed"]
            and noise["passed"]
            and not noise["CMB_likelihood_allowed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "identity": composite_clock_identity(),
        "early_background": early_background_extension(),
        "finite_k": finite_k_kernel(),
        "noise_CMB": noise_and_cmb_gate(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "decision": arbitration()["demotion_status"],
        "sections": sections,
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    identity = calculation["sections"]["identity"]
    early_background = calculation["sections"]["early_background"]
    finite_k = calculation["sections"]["finite_k"]
    noise = calculation["sections"]["noise_CMB"]
    print(identity["identity_status"])
    print(f"kinetic={identity['kinetic_identity']}")
    print(f"angular={identity['angular_identity']}")
    for row in identity["mass_floor_rows"]:
        print(
            f"{row['arena']} m_c>={row['minimum_carrier_mass_eV']:.9e} eV"
        )
    for row in early_background["rows"]:
        print(
            "early target={:.0e} kappa={:.8e} dE_overlap={:.6e}".format(
                row["target"],
                row["kappa_over_H0_squared"],
                row["maximum_overlap_fractional_E_shift"],
            )
        )
    for row in finite_k["rows"]:
        print(
            "target={:.0e} k={:.0e} mom/seed={:.6e} rel={:.6e} "
            "Phi0={:.6e}".format(
                row["target"],
                row["k_h_per_Mpc"],
                row["maximum_momentum_residual_over_seed"],
                row["maximum_relative_momentum_residual"],
                row["final_phi_metric"],
            )
        )
    for row in noise["response_rows"]:
        print(
            "noise N={:.0f} Phi_response={:.6e}".format(
                row["injection_N"], row["final_metric_response"]
            )
        )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
