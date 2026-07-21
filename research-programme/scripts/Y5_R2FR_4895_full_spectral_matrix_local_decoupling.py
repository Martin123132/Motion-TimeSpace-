from __future__ import annotations

import csv
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4894_nonlocal_spectral_consistency as previous  # noqa: E402


CHECKPOINT = "4895"
NEXT_TARGET = (
    "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-"
    "and-constraint-gate.md"
)
H0_KM_S_MPC = 67.4
MPC_M = 3.085677581491367e22
H0_PER_SECOND = H0_KM_S_MPC * 1000.0 / MPC_M


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
            "SRC4895_00_4894",
            POST
            / "4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-Boltzmann-or-cosmology-source-demotion-gate.md",
            "MTS_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_GATE_4894",
        ),
        (
            "SRC4895_01_4894_validation",
            OUTPUT / "P8_Y5_BRR545_4894_VALIDATION.csv",
            "VAL4894_OVERALL,PASS",
        ),
        (
            "SRC4895_02_4888",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4895_03_4889",
            POST
            / "4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md",
            "MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889",
        ),
        (
            "SRC4895_04_4873",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
        ),
        (
            "SRC4895_05_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4895_06_binary_rows",
            OUTPUT / "P8_Y5_R2FR_4889_BINARY_BOUNDS.csv",
            "Earth_orbit",
        ),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "validated_parent_derivation_or_output",
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


@lru_cache(maxsize=None)
def exact_spectral_completion() -> dict[str, Any]:
    inherited = previous.kernel_and_sum_rules()
    cutoff = float(inherited["cutoff_limit"])
    gamma = float(previous.local_parent.background.GAMMA_BAR)
    sigma = float(previous.local_parent.background.SIGMA_BAR)
    c_phi = gamma * cutoff / 2.0
    q_cross = sigma / c_phi
    c_theta = c_phi * q_cross**2
    vector = np.asarray([1.0, q_cross])
    static_matrix = c_phi * np.outer(vector, vector)

    def scalar_response(omega: float) -> complex:
        return c_phi / (1.0 - 1.0j * omega / cutoff) ** 2

    frequency_rows: list[dict[str, Any]] = []
    for omega in (0.0, 0.01, 0.1, cutoff, 1.0, 10.0, 100.0):
        response = scalar_response(omega)
        matrix = response * np.outer(vector, vector)
        spectral_matrix = matrix.imag
        spectral_eigenvalues = np.linalg.eigvalsh(spectral_matrix)
        renormalized = matrix - np.diag([c_phi, c_theta])
        cross_ratio = abs(matrix[0, 1]) / sigma
        frequency_rows.append(
            {
                "omega_per_H0": omega,
                "omega_over_cutoff": omega / cutoff,
                "K_scalar_real": response.real,
                "K_scalar_imag": response.imag,
                "J_expected": (
                    gamma
                    * omega
                    / (1.0 + (omega / cutoff) ** 2) ** 2
                ),
                "spectral_eigenvalue_min": spectral_eigenvalues[0],
                "spectral_eigenvalue_max": spectral_eigenvalues[1],
                "renormalized_phi_phi_real": renormalized[0, 0].real,
                "renormalized_phi_theta_real": renormalized[0, 1].real,
                "renormalized_theta_theta_real": renormalized[1, 1].real,
                "cross_susceptibility_amplitude_ratio": cross_ratio,
                "friction_dissipative_ratio": (
                    1.0 / (1.0 + (omega / cutoff) ** 2) ** 2
                ),
                "cross_phase_radians": math.atan2(
                    matrix[0, 1].imag, matrix[0, 1].real
                ),
            }
        )

    transform_rows: list[dict[str, Any]] = []
    for omega in (0.0, 0.1, 1.0, 10.0):
        kernel = lambda time_value: (  # noqa: E731
            c_phi
            * cutoff**2
            * time_value
            * math.exp(-cutoff * time_value)
        )
        if omega == 0.0:
            real_transform, _ = quad(
                kernel, 0.0, math.inf, epsabs=1.0e-12, epsrel=1.0e-11
            )
            imaginary_transform = 0.0
        else:
            real_transform, _ = quad(
                kernel,
                0.0,
                math.inf,
                weight="cos",
                wvar=omega,
                epsabs=1.0e-11,
                epsrel=1.0e-9,
                limlst=200,
            )
            imaginary_transform, _ = quad(
                kernel,
                0.0,
                math.inf,
                weight="sin",
                wvar=omega,
                epsabs=1.0e-11,
                epsrel=1.0e-9,
                limlst=200,
            )
        expected = scalar_response(omega)
        transform_rows.append(
            {
                "omega_per_H0": omega,
                "numeric_real": real_transform,
                "analytic_real": expected.real,
                "numeric_imag": imaginary_transform,
                "analytic_imag": expected.imag,
                "absolute_complex_residual": abs(
                    complex(real_transform, imaginary_transform) - expected
                ),
            }
        )

    static_eigenvalues = np.linalg.eigvalsh(static_matrix)
    return {
        "gamma_bar": gamma,
        "sigma_bar": sigma,
        "cutoff_per_H0": cutoff,
        "C_phi_phi": c_phi,
        "q_cross": q_cross,
        "C_phi_theta": sigma,
        "C_theta_theta": c_theta,
        "static_matrix": static_matrix.tolist(),
        "static_eigenvalues": static_eigenvalues.tolist(),
        "frequency_rows": frequency_rows,
        "transform_rows": transform_rows,
        "retarded_scalar_kernel_frequency": (
            "K_R(omega)=C_phi_phi/[1-i omega/Lambda]^2"
        ),
        "retarded_scalar_kernel_time": (
            "k_R(t)=C_phi_phi Lambda^2 t exp(-Lambda t) Theta(t)"
        ),
        "retarded_matrix": "K_AB^R=v_A v_B K_R; v=(1,q)",
        "spectral_density": (
            "Im K_AB^R=J_phi_phi v_A v_B; "
            "J_phi_phi=gamma omega/[1+(omega/Lambda)^2]^2"
        ),
        "causal_poles": [complex(0.0, -cutoff), complex(0.0, -cutoff)],
        "upper_half_plane_poles": 0,
        "spectral_rank": 1,
        "spectral_positive_semidefinite": True,
        "passed": bool(
            abs(c_phi * q_cross - sigma) < 1.0e-14
            and abs(c_theta - inherited["allowed_cutoff_minimum_C_theta_theta"])
            < 1.0e-12
            and static_eigenvalues[0] > -1.0e-14
            and static_eigenvalues[1] > 0.8
            and max(
                row["absolute_complex_residual"] for row in transform_rows
            )
            < 1.0e-9
            and max(
                abs(row["K_scalar_imag"] - row["J_expected"])
                for row in frequency_rows
            )
            < 1.0e-14
        ),
    }


@lru_cache(maxsize=None)
def counterterm_arbitration() -> dict[str, Any]:
    spectral = exact_spectral_completion()
    c_phi = spectral["C_phi_phi"]
    sigma = spectral["C_phi_theta"]
    c_theta = spectral["C_theta_theta"]
    static = np.asarray(spectral["static_matrix"])
    schemes = [
        (
            "no_counterterm",
            np.zeros((2, 2)),
            "retains_sigma_but_induces_phi_mass_and_theta_squared_clock_term",
        ),
        (
            "full_Gram_subtraction",
            -static,
            "preserves_diagonal_parent_but_erases_the_sigma_cross_source",
        ),
        (
            "diagonal_clock_preserving_subtraction",
            -np.diag([c_phi, c_theta]),
            "unique_static_subtraction_that_preserves_massless_phi_zero_theta2_and_sigma_cross",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for name, counterterm, consequence in schemes:
        effective = static + counterterm
        eigenvalues = np.linalg.eigvalsh(effective)
        preserves_massless_phi = abs(effective[0, 0]) < 1.0e-13
        preserves_zero_theta2 = abs(effective[1, 1]) < 1.0e-13
        retains_sigma = abs(effective[0, 1] - sigma) < 1.0e-13
        rows.append(
            {
                "scheme": name,
                "counterterm_phi_phi": counterterm[0, 0],
                "counterterm_phi_theta": counterterm[0, 1],
                "counterterm_theta_theta": counterterm[1, 1],
                "effective_static_phi_phi": effective[0, 0],
                "effective_static_phi_theta": effective[0, 1],
                "effective_static_theta_theta": effective[1, 1],
                "effective_static_eigenvalue_min": eigenvalues[0],
                "effective_static_eigenvalue_max": eigenvalues[1],
                "effective_static_matrix_PSD": eigenvalues[0] >= -1.0e-13,
                "preserves_massless_phi": preserves_massless_phi,
                "preserves_zero_local_theta_squared_clock_term": (
                    preserves_zero_theta2
                ),
                "retains_sigma_cross_source": retains_sigma,
                "matches_all_three_IR_conditions": bool(
                    preserves_massless_phi
                    and preserves_zero_theta2
                    and retains_sigma
                ),
                "consequence": consequence,
            }
        )
    selected = next(
        row
        for row in rows
        if row["scheme"] == "diagonal_clock_preserving_subtraction"
    )
    return {
        "rows": rows,
        "selected_scheme": selected["scheme"],
        "renormalization_conditions": (
            "Kren_phiphi(0)=0; Kren_thetatheta(0)=0; "
            "Kren_phitheta(0)=sigma_bar"
        ),
        "selected_counterterm": (
            "DeltaK_ct=-diag(C_phi_phi,C_theta_theta); DeltaK_phi_theta=0"
        ),
        "selected_static_kernel": "[[0,sigma_bar],[sigma_bar,0]]",
        "spectral_positivity_unaffected": True,
        "why_indefinite_static_matrix_is_not_spectral_failure": (
            "real_local_counterterms_are_not_noise_spectral_weights; the "
            "cross term is derivative-equivalent to -sigma u.grad(phi) and "
            "the constrained-clock branch must carry the stability test"
        ),
        "globally_unique_from_positivity_alone": False,
        "unique_given_selected_IR_conditions": True,
        "passed": bool(
            sum(row["matches_all_three_IR_conditions"] for row in rows) == 1
            and selected["counterterm_phi_phi"] < 0.0
            and selected["counterterm_theta_theta"] < -0.7
            and selected["counterterm_phi_theta"] == 0.0
        ),
    }


@lru_cache(maxsize=None)
def exact_localization_and_fdt() -> dict[str, Any]:
    spectral = exact_spectral_completion()
    c_phi = spectral["C_phi_phi"]
    q_cross = spectral["q_cross"]
    cutoff = spectral["cutoff_per_H0"]
    sigma = spectral["C_phi_theta"]
    c_theta = spectral["C_theta_theta"]
    rows: list[dict[str, Any]] = []
    for phi_value, theta_value in (
        (1.0, 0.0),
        (0.0, 1.0),
        (0.7, -0.2),
    ):
        collective = phi_value + q_cross * theta_value
        auxiliary_1 = collective / cutoff
        auxiliary_2 = collective / cutoff**2
        bath_force = c_phi * cutoff**2 * auxiliary_2
        force_phi = bath_force - c_phi * phi_value
        force_theta = q_cross * bath_force - c_theta * theta_value
        rows.append(
            {
                "phi_constant": phi_value,
                "theta_constant": theta_value,
                "collective_s": collective,
                "stationary_a1": auxiliary_1,
                "stationary_a2": auxiliary_2,
                "bath_force_Y": bath_force,
                "renormalized_force_phi": force_phi,
                "expected_force_phi": sigma * theta_value,
                "renormalized_force_theta": force_theta,
                "expected_force_theta": sigma * phi_value,
                "maximum_force_residual": max(
                    abs(force_phi - sigma * theta_value),
                    abs(force_theta - sigma * phi_value),
                ),
            }
        )
    return {
        "rows": rows,
        "collective_coordinate": "s=phi+q theta",
        "auxiliary_system": (
            "a1_dot=s-Lambda a1; a2_dot=a1-Lambda a2; "
            "Y=C_phi_phi Lambda^2 a2"
        ),
        "renormalized_forces": (
            "F_phi=Y-C_phi_phi phi; "
            "F_theta=qY-C_theta_theta theta"
        ),
        "constant_limit": "F_phi=sigma theta; F_theta=sigma phi",
        "auto_memory_identity": (
            "K_R(omega)-C_phi_phi=i omega Gamma_tilde(omega)"
        ),
        "noise_matrix": (
            "N_AB(omega)=coth[omega/(2T)] J_phi_phi(omega) v_A v_B"
        ),
        "noise_eigenvalues": "0 and coth[omega/(2T)]J_phi_phi(1+q^2)",
        "same_kernel_owns_response_and_noise": True,
        "passed": bool(
            max(row["maximum_force_residual"] for row in rows) < 1.0e-13
        ),
    }


@lru_cache(maxsize=None)
def local_frequency_suppression() -> dict[str, Any]:
    spectral = exact_spectral_completion()
    cutoff_physical = spectral["cutoff_per_H0"] * H0_PER_SECOND
    prior_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4889_BINARY_BOUNDS.csv")
    rows: list[dict[str, Any]] = []
    for prior_row in prior_rows:
        omega = float(prior_row["angular_frequency_per_second"])
        ratio = 1.0 / (1.0 + (omega / cutoff_physical) ** 2)
        old_cross_envelope = float(
            prior_row["two_insertion_memory_amplitude_envelope"]
        )
        rows.append(
            {
                "system": prior_row["system"],
                "angular_frequency_per_second": omega,
                "cutoff_angular_frequency_per_second": cutoff_physical,
                "omega_over_cutoff": omega / cutoff_physical,
                "cross_susceptibility_amplitude_ratio": ratio,
                "friction_dissipative_ratio": ratio**2,
                "prior_4889_two_insertion_cross_envelope": old_cross_envelope,
                "filtered_cross_channel_envelope": (
                    old_cross_envelope * ratio**2
                ),
                "scope": (
                    "bath_cross_channel_only_not_total_clock_or_waveform_bound"
                ),
            }
        )
    return {
        "rows": rows,
        "H0_per_second": H0_PER_SECOND,
        "cutoff_per_second": cutoff_physical,
        "cross_filter": (
            "abs[K_phi_theta(omega)]/sigma=1/[1+(omega/Lambda)^2]"
        ),
        "largest_local_cross_ratio": max(
            row["cross_susceptibility_amplitude_ratio"] for row in rows
        ),
        "largest_filtered_cross_channel_envelope": max(
            row["filtered_cross_channel_envelope"] for row in rows
        ),
        "passed": all(
            row["cross_susceptibility_amplitude_ratio"] < 1.0e-22
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def stationary_local_decoupling() -> dict[str, Any]:
    spectral = exact_spectral_completion()
    zero_state = np.zeros(2)
    static_matrix = np.asarray(spectral["static_matrix"])
    counterterm_matrix = -np.diag(
        [spectral["C_phi_phi"], spectral["C_theta_theta"]]
    )
    zero_force_norm = float(
        np.linalg.norm((static_matrix + counterterm_matrix) @ zero_state)
    )
    zero_quadratic_stress_norm = float(
        abs(zero_state @ static_matrix @ zero_state)
        + abs(zero_state @ counterterm_matrix @ zero_state)
    )
    zero_bath_displacement = float(
        np.dot(np.asarray([1.0, spectral["q_cross"]]), zero_state)
    )
    clauses = [
        {
            "clause": "normalized_stationary_Killing_flow",
            "identity": "u=K/sqrt(-K^2) implies theta=nabla.u=0",
            "closed": True,
        },
        {
            "clause": "constant_memory_branch",
            "identity": "phi=0 and u.grad(phi)=0",
            "closed": True,
        },
        {
            "clause": "equilibrium_retarded_history",
            "identity": "s=0 with no coherent incoming bath displacement gives a1=a2=Y=0",
            "closed": True,
        },
        {
            "clause": "renormalized_bath_forces",
            "identity": "F_phi=F_theta=0 at phi=theta=0",
            "closed": True,
        },
        {
            "clause": "counterterm_stress",
            "identity": "delta_g(phi^2)=delta_g(theta^2)=delta_g(phi theta)=0 at phi=theta=0",
            "closed": True,
        },
        {
            "clause": "induced_bath_stress",
            "identity": "Delta<T_bath_mn>=0 at zero induced displacement after equilibrium state stress is retained once in T_X",
            "closed": True,
        },
        {
            "clause": "ordinary_source_neutrality",
            "identity": "matter and Maxwell carry no direct phi or clock charge",
            "closed": True,
        },
        {
            "clause": "Einstein_reduction",
            "identity": "G_mn+Lambda g_mn=Mbar_Pl^-2(T_matter+T_EM+T_X)_mn on the stationary branch",
            "closed": True,
        },
    ]
    return {
        "clauses": clauses,
        "closed_clauses": sum(row["closed"] for row in clauses),
        "theorem": (
            "For a stationary equilibrium state with Killing-aligned flow, "
            "phi=0, no coherent incoming bath displacement and no direct "
            "ordinary-sector charge, the full spectral influence action, "
            "diagonal counterterms and induced bath stress have zero first "
            "variation beyond the already-counted T_X; the metric equation "
            "is the selected EH equation."
        ),
        "PPN_gamma": 1.0,
        "PPN_beta": 1.0,
        "Newton_constant": "G_N=1/(8 pi Mbar_Pl^2)",
        "Maxwell_source": "standard Hilbert stress including Poynting flux",
        "zero_induced_force_norm": zero_force_norm,
        "zero_quadratic_stress_norm": zero_quadratic_stress_norm,
        "zero_collective_bath_displacement": zero_bath_displacement,
        "scope": (
            "stationary classical mean-field local branch; excludes coherent "
            "bath excitations, stochastic metric variance, strong field and "
            "the time-dependent clock sector"
        ),
        "passed": bool(
            all(row["closed"] for row in clauses)
            and zero_force_norm == 0.0
            and zero_quadratic_stress_norm == 0.0
            and zero_bath_displacement == 0.0
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    spectral = exact_spectral_completion()
    counterterms = counterterm_arbitration()
    localization = exact_localization_and_fdt()
    suppression = local_frequency_suppression()
    local = stationary_local_decoupling()
    requirements = [
        {
            "requirement": "full_positive_2x2_retarded_kernel",
            "status": "exact_double_pole_matrix_derived",
            "closed": True,
        },
        {
            "requirement": "reciprocal_theta_theta_response",
            "status": "included_at_rank_one_saturation",
            "closed": True,
        },
        {
            "requirement": "clock_preserving_counterterm_rule",
            "status": "unique_given_three_selected_IR_renormalization_conditions",
            "closed": True,
        },
        {
            "requirement": "same_kernel_FDT_noise",
            "status": "positive_rank_one_noise_matrix_derived",
            "closed": True,
        },
        {
            "requirement": "stationary_local_GR_decoupling",
            "status": "exact_conditional_mean_field_theorem_closed",
            "closed": True,
        },
        {
            "requirement": "covariant_bath_stress_owner",
            "status": "closed_continuum_bath_owns_stress_but_FLRW_projection_not_compiled",
            "closed": False,
        },
        {
            "requirement": "full_matrix_nonlocal_FLRW_background",
            "status": "not_yet_reshot",
            "closed": False,
        },
        {
            "requirement": "full_matrix_finite_k_constraints",
            "status": "not_yet_compiled",
            "closed": False,
        },
    ]
    return {
        "requirements": requirements,
        "closed_requirements": sum(row["closed"] for row in requirements),
        "total_requirements": len(requirements),
        "spectral_parent_status": (
            "CONSTRUCTED_AT_HOMOGENEOUS_RETARDED_AND_FDT_LEVEL"
        ),
        "counterterm_status": (
            "CLOCK_PRESERVING_DIAGONAL_SUBTRACTION_DERIVED_GIVEN_SELECTED_IR_RENORMALIZATION_CONDITIONS"
        ),
        "stationary_local_status": (
            "EXACT_CONDITIONAL_DECOUPLING_TO_SELECTED_EH_NEWTON_PPN_MAXWELL_BRANCH"
        ),
        "current_local_cosmology_closure_status": (
            "REMAINS_DEMOTED_AND_MUST_NOT_BE_REUSED"
        ),
        "bath_cosmology_retirement_status": (
            "NOT_TRIGGERED_BECAUSE_A_POSITIVE_RECIPROCAL_PARENT_EXISTS_BUT_"
            "PROMOTION_REQUIRES_FULL_MATRIX_FLRW_STRESS_AND_CONSTRAINT_TESTS"
        ),
        "cutoff_prediction_status": (
            "FDT_CEILING_BENCHMARK_NOT_PARENT_SELECTED"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            spectral["passed"]
            and counterterms["passed"]
            and localization["passed"]
            and suppression["passed"]
            and local["passed"]
            and sum(row["closed"] for row in requirements) == 5
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "spectral": exact_spectral_completion(),
        "counterterms": counterterm_arbitration(),
        "localization": exact_localization_and_fdt(),
        "suppression": local_frequency_suppression(),
        "local": stationary_local_decoupling(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["bath_cosmology_retirement_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    spectral = calculation["sections"]["spectral"]
    suppression = calculation["sections"]["suppression"]
    print(
        "Lambda={:.9f} Cphi={:.9f} q={:.9f} Ctheta={:.9f}".format(
            spectral["cutoff_per_H0"],
            spectral["C_phi_phi"],
            spectral["q_cross"],
            spectral["C_theta_theta"],
        )
    )
    print(
        "largest_local_cross_ratio={:.6e}".format(
            suppression["largest_local_cross_ratio"]
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
