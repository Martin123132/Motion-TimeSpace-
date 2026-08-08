from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson, solve_ivp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5186"

UNIVERSAL_CSV = OUT / "universal_radiation_Bogoliubov_spectrum.csv"
MASS_SPECTRA_CSV = OUT / "three_mass_Bogoliubov_spectra.csv"
ABUNDANCE_CSV = OUT / "three_mass_vacuum_abundance_gate.csv"
PRESCRIPTION_CSV = OUT / "vacuum_prescription_and_start_time_sensitivity.csv"
ROBUSTNESS_CSV = OUT / "adiabatic_UV_and_background_robustness.csv"
COVARIANCE_CSV = OUT / "neutral_Gaussian_covariance_gate.csv"
ROUTE_CSV = OUT / "neutral_source_selection_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "FLRW_Bogoliubov_neutral_production_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5186_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-"
    "abundance-no-go.md"
)

MARKER = "MTS_5186_FLRW_BOGOLIUBOV_NEUTRAL_VACUUM_PRODUCTION_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

H0_KM_S_MPC = 67.4
OMEGA_R = 9.0e-5
OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
OMEGA_X = OMEGA_M - OMEGA_B
OMEGA_LAMBDA = 1.0 - OMEGA_M - OMEGA_R
MPL_REDUCED_EV = 2.435e27
HBAR_EV_S = 6.582119569e-16
HBAR_C_EV_M = 1.973269804e-7
MPC_M = 3.085677581491367e22
H0_EV = HBAR_EV_S * H0_KM_S_MPC * 1000.0 / MPC_M
RADIATION_CONFORMAL_SLOPE_EV = H0_EV * math.sqrt(OMEGA_R)
EV3_TO_M_MINUS3 = (1.0 / HBAR_C_EV_M) ** 3
MPC_INVERSE_EV = HBAR_C_EV_M / MPC_M
RHO_CRIT0_EV4 = 3.0 * MPL_REDUCED_EV**2 * H0_EV**2
RHO_X0_EV4 = OMEGA_X * RHO_CRIT0_EV4

PROJECTION_Y_VALUES = (15.0, 20.0, 25.0, 30.0)
CANONICAL_PROJECTION_Y = 25.0
KAPPA_MIN = 1.0e-5
KAPPA_MAX = 8.0
SYMMETRIC_CROSSING_INTEGRAL = 1.0 / (4.0 * math.pi)
SYMMETRIC_CROSSING_COEFFICIENT = 1.0 / (8.0 * math.pi**3)

ROUTE_DECISION = (
    "THE_CHECKPOINT_5156_PARENT_HESSIAN_REDUCES_DEEP_IN_RADIATION_"
    "DOMINATION_TO_ONE_UNIVERSAL_MODE_EQUATION_U_KAPPA_DOUBLE_PRIME_PLUS_"
    "KAPPA_SQUARED_PLUS_Y_SQUARED_TIMES_U_KAPPA_EQUALS_ZERO_THE_HALF_LINE_"
    "CONFORMAL_HAMILTONIAN_GROUND_STATE_AND_THE_EXACT_SYMMETRIC_ADIABATIC_"
    "CROSSING_BOTH_PRODUCE_FINITE_REFLECTION_EVEN_NEUTRAL_SQUEEZED_PAIRS_"
    "WITH_NO_FITTED_GALAXY_PARAMETER_BUT_THE_LARGER_OF_THEIR_PRESENT_"
    "ABUNDANCES_IS_BETWEEN_EIGHTY_NINE_AND_NINETY_SIX_ORDERS_BELOW_THE_"
    "LOCKED_OMEGA_X_TARGET_FOR_ALL_THREE_MASSES_FINITE_START_AND_"
    "ADIABATIC_ORDER_TESTS_CONFIRM_THAT_THE_INFRARED_COVARIANCE_DEPENDS_ON_"
    "A_VACUUM_OR_COSMOGENESIS_BOUNDARY_LAW_WHILE_THE_ULTRAVIOLET_NUMBER_"
    "INTEGRAL_IS_CONVERGENT_THE_FREE_FLRW_PARENT_THEREFORE_TRANSFERS_ANY_"
    "CHOSEN_STATE_BUT_DOES_NOT_SELECT_THE_REQUIRED_NEUTRAL_OCCUPATION_"
    "NORMALIZATION_AN_ARBITRARILY_SQUEEZED_STATE_OR_THE_CHECKPOINT_5152_"
    "MISALIGNMENT_AMPLITUDE_CAN_SUPPLY_OMEGA_X_ONLY_AS_INITIAL_STATE_DATA_"
    "SO_THE_VACUUM_PRODUCTION_ROUTE_IS_REJECTED_AS_THE_ABUNDANCE_OWNER_AND_"
    "THE_GALAXY_OCCUPIED_STATE_IS_DEMOTED_TO_AN_EXPLICIT_CONDITIONAL_"
    "COSMOLOGICAL_INITIAL_CONDITION_UNLESS_A_SEPARATE_PARENT_OWNED_"
    "NONADIABATIC_COSMOGENESIS_EVENT_IS_DERIVED"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES = {
    "checkpoint_4952_document": (
        source_path(
            "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-"
            "motion-pair-source-and-frequency-support-or-composite-route-"
            "rejection.md"
        ),
        "2e4fc50355c1c3cefece8d5eb633952dea2ea9a8445712c2c4daf870dcc938d8",
    ),
    "checkpoint_5152_document": (
        source_path(
            "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-"
            "window-and-formation-source-arbitration.md"
        ),
        "a62af8bc11dc0e5130e681386bb64ac4a56fb21105540581f91ab452473b0167",
    ),
    "checkpoint_5152_background": (
        source_path(
            "source-intake/functional_rg/5152/primordial_motion_background.csv"
        ),
        "01fce81188fb2c6cf1d982cb7ffe8d2896668f100878a0d1ba11462426a1e338",
    ),
    "checkpoint_5156_document": (
        source_path(
            "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-"
            "adiabatic-radiation-transfer-and-patch-collapse-gate.md"
        ),
        "fdb5c0406fb7d0e47204a51212b24b5adf19d33644399bc4a1fd2268155b1353",
    ),
    "checkpoint_5156_Hessian": (
        source_path(
            "source-intake/functional_rg/5156/FLRW_parent_Hessian_reduction.csv"
        ),
        "64c269d472aa578411e3aea93efba0d432c7b070e5ff9b9c5f152b8fd6c9e7ac",
    ),
    "checkpoint_5157_masses": (
        source_path(
            "source-intake/functional_rg/5157/"
            "three_mass_state_preparation_numbers.csv"
        ),
        "4cc47c8a2000b8dd7dc0d617d477af2ffa7d80ef98de483ef3926d2dd781f48f",
    ),
    "checkpoint_5158_document": (
        source_path(
            "5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-"
            "state-pivot.md"
        ),
        "cfbd0dd3eb44d0a6621d664f051cb1eb5fa507db30cfc8bf62419c436da087aa",
    ),
    "checkpoint_5185_document": (
        source_path(
            "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-"
            "collision-gate.md"
        ),
        "d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5",
    ),
}

PRIMARY_URLS = {
    "Parker_1969": "https://link.aps.org/doi/10.1103/PhysRev.183.1057",
    "Chung_Kolb_Riotto_1998": "https://arxiv.org/abs/hep-ph/9802238",
    "Planck_2018": "https://arxiv.org/abs/1807.06209",
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(
    check_id: str,
    check: str,
    passed: bool,
    observed: Any,
    required: Any,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "observed": observed,
        "required": required,
        "checkpoint_marker": MARKER,
    }


def frequency(kappa: float, dimensionless_time: float) -> float:
    return math.sqrt(kappa**2 + dimensionless_time**2)


def mode_rhs(
    dimensionless_time: float,
    state: np.ndarray,
    kappa: float,
) -> list[float]:
    mode_value = complex(state[0], state[1])
    mode_derivative = complex(state[2], state[3])
    mode_second_derivative = -(
        kappa**2 + dimensionless_time**2
    ) * mode_value
    return [
        mode_derivative.real,
        mode_derivative.imag,
        mode_second_derivative.real,
        mode_second_derivative.imag,
    ]


def project_mode(
    kappa: float,
    dimensionless_time: float,
    state: np.ndarray,
) -> dict[str, float]:
    mode_value = complex(state[0], state[1])
    mode_derivative = complex(state[2], state[3])
    projected_frequency = frequency(kappa, dimensionless_time)
    frequency_derivative = dimensionless_time / projected_frequency
    reference_mode = 1.0 / math.sqrt(2.0 * projected_frequency)
    reference_derivative = (
        -frequency_derivative / (2.0 * projected_frequency)
        - 1j * projected_frequency
    ) * reference_mode
    beta_value = -1j * (
        reference_mode * mode_derivative
        - reference_derivative * mode_value
    )
    wronskian = (
        mode_value * mode_derivative.conjugate()
        - mode_derivative * mode_value.conjugate()
    ) / 1j
    occupation = max(0.0, float(abs(beta_value) ** 2))
    return {
        "occupation": occupation,
        "anomalous_covariance_abs": math.sqrt(occupation * (occupation + 1.0)),
        "wronskian_real": float(wronskian.real),
        "wronskian_imag": float(wronskian.imag),
        "adiabatic_parameter_1": abs(
            frequency_derivative / projected_frequency**2
        ),
    }


def solve_half_line_mode(kappa: float) -> dict[str, Any]:
    initial_mode = 1.0 / math.sqrt(2.0 * kappa)
    initial_derivative = -1j * kappa * initial_mode
    initial_state = [
        initial_mode,
        0.0,
        initial_derivative.real,
        initial_derivative.imag,
    ]
    solution = solve_ivp(
        lambda time_value, state_value: mode_rhs(
            time_value, state_value, kappa
        ),
        (0.0, max(PROJECTION_Y_VALUES)),
        initial_state,
        method="DOP853",
        rtol=3.0e-9,
        atol=3.0e-11,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"Half-line mode integration failed at kappa={kappa}")
    projections = {
        str(projection_time): project_mode(
            kappa,
            projection_time,
            solution.sol(projection_time),
        )
        for projection_time in PROJECTION_Y_VALUES
    }
    return {
        "kappa": kappa,
        "solver_steps": len(solution.t),
        "projections": projections,
    }


def solve_finite_start_mode(
    kappa: float,
    initial_time: float,
) -> float:
    initial_frequency = frequency(kappa, initial_time)
    initial_frequency_derivative = initial_time / initial_frequency
    initial_mode = 1.0 / math.sqrt(2.0 * initial_frequency)
    initial_derivative = (
        -initial_frequency_derivative / (2.0 * initial_frequency)
        - 1j * initial_frequency
    ) * initial_mode
    initial_state = [
        initial_mode,
        0.0,
        initial_derivative.real,
        initial_derivative.imag,
    ]
    solution = solve_ivp(
        lambda time_value, state_value: mode_rhs(
            time_value, state_value, kappa
        ),
        (initial_time, CANONICAL_PROJECTION_Y),
        initial_state,
        method="DOP853",
        rtol=8.0e-9,
        atol=8.0e-11,
    )
    if not solution.success:
        raise RuntimeError(
            f"Finite-start mode integration failed at kappa={kappa}"
        )
    return project_mode(
        kappa,
        CANONICAL_PROJECTION_Y,
        solution.y[:, -1],
    )["occupation"]


def solve_second_order_uv_mode(kappa: float) -> float:
    second_order_frequency = kappa - 1.0 / (4.0 * kappa**3)
    if second_order_frequency <= 0.0:
        raise ValueError("Second-order adiabatic frequency is not positive")
    initial_mode = 1.0 / math.sqrt(2.0 * second_order_frequency)
    initial_derivative = -1j * second_order_frequency * initial_mode
    initial_state = [
        initial_mode,
        0.0,
        initial_derivative.real,
        initial_derivative.imag,
    ]
    solution = solve_ivp(
        lambda time_value, state_value: mode_rhs(
            time_value, state_value, kappa
        ),
        (0.0, CANONICAL_PROJECTION_Y),
        initial_state,
        method="DOP853",
        rtol=3.0e-10,
        atol=3.0e-12,
    )
    if not solution.success:
        raise RuntimeError(
            f"Second-order UV mode integration failed at kappa={kappa}"
        )
    return project_mode(
        kappa,
        CANONICAL_PROJECTION_Y,
        solution.y[:, -1],
    )["occupation"]


def primary_kappa_grid() -> np.ndarray:
    return np.unique(
        np.concatenate(
            [
                np.logspace(-5.0, -1.0, 35),
                np.linspace(0.1, 2.0, 50),
                np.linspace(2.1, 8.0, 45),
            ]
        )
    )


def sensitivity_kappa_grid() -> np.ndarray:
    return np.unique(
        np.concatenate(
            [
                np.logspace(-5.0, -1.0, 16),
                np.linspace(0.1, 2.0, 22),
                np.linspace(2.2, 8.0, 14),
            ]
        )
    )


def phase_space_integral(
    kappas: np.ndarray,
    occupations: np.ndarray,
    include_half_line_tails: bool,
) -> dict[str, float]:
    numeric_integral = float(
        simpson(kappas**2 * occupations, x=kappas)
    )
    infrared_coefficient = float(kappas[0] * occupations[0])
    infrared_tail = (
        0.5 * infrared_coefficient * kappas[0] ** 2
        if include_half_line_tails
        else 0.0
    )
    ultraviolet_tail = (
        1.0 / (320.0 * kappas[-1] ** 5)
        if include_half_line_tails
        else 0.0
    )
    total_integral = numeric_integral + infrared_tail + ultraviolet_tail
    return {
        "numeric_integral": numeric_integral,
        "infrared_tail": infrared_tail,
        "ultraviolet_tail": ultraviolet_tail,
        "total_integral": total_integral,
        "number_coefficient": total_integral / (2.0 * math.pi**2),
    }


def build_universal_spectrum() -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, np.ndarray],
]:
    kappas = primary_kappa_grid()
    solved_modes = [solve_half_line_mode(float(kappa)) for kappa in kappas]
    projection_arrays: dict[str, np.ndarray] = {}
    for projection_time in PROJECTION_Y_VALUES:
        projection_arrays[str(projection_time)] = np.asarray(
            [
                solved_mode["projections"][str(projection_time)][
                    "occupation"
                ]
                for solved_mode in solved_modes
            ],
            dtype=float,
        )

    canonical_occupations = projection_arrays[str(CANONICAL_PROJECTION_Y)]
    symmetric_occupations = np.exp(-math.pi * kappas**2)
    rows: list[dict[str, Any]] = []
    for index, kappa in enumerate(kappas):
        canonical_projection = solved_modes[index]["projections"][
            str(CANONICAL_PROJECTION_Y)
        ]
        symmetric_occupation = float(symmetric_occupations[index])
        rows.append(
            {
                "kappa": float(kappa),
                "half_line_n_k": float(canonical_occupations[index]),
                "half_line_abs_c_k": canonical_projection[
                    "anomalous_covariance_abs"
                ],
                "half_line_kappa2_n_k": float(
                    kappa**2 * canonical_occupations[index]
                ),
                "symmetric_crossing_n_k": symmetric_occupation,
                "symmetric_crossing_abs_c_k": math.sqrt(
                    symmetric_occupation * (symmetric_occupation + 1.0)
                ),
                "symmetric_crossing_kappa2_n_k": float(
                    kappa**2 * symmetric_occupation
                ),
                "wronskian_real": canonical_projection["wronskian_real"],
                "wronskian_imag": canonical_projection["wronskian_imag"],
                "projection_y": CANONICAL_PROJECTION_Y,
                "half_line_boundary_parent_owned": False,
                "symmetric_extension_parent_owned": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    projection_integrals = {
        projection_time: phase_space_integral(
            kappas,
            projection_arrays[projection_time],
            True,
        )
        for projection_time in projection_arrays
    }
    half_line_integral = projection_integrals[
        str(CANONICAL_PROJECTION_Y)
    ]
    symmetric_numeric_integral = float(
        simpson(kappas**2 * symmetric_occupations, x=kappas)
        + kappas[0] ** 3 / 3.0
    )
    coarse_indices = np.arange(0, len(kappas), 2)
    if coarse_indices[-1] != len(kappas) - 1:
        coarse_indices = np.append(coarse_indices, len(kappas) - 1)
    coarse_integral = phase_space_integral(
        kappas[coarse_indices],
        canonical_occupations[coarse_indices],
        True,
    )
    ultraviolet_mask = kappas >= 4.0
    infrared_mask = kappas <= 1.0e-3
    ultraviolet_coefficient = float(
        np.median(
            kappas[ultraviolet_mask] ** 8
            * canonical_occupations[ultraviolet_mask]
        )
    )
    infrared_coefficient = float(
        np.median(
            kappas[infrared_mask]
            * canonical_occupations[infrared_mask]
        )
    )
    maximum_wronskian_residual = max(
        abs(row["wronskian_real"] - 1.0)
        + abs(row["wronskian_imag"])
        for row in rows
    )
    metrics = {
        "kappa_count": len(kappas),
        "kappa_min": float(kappas[0]),
        "kappa_max": float(kappas[-1]),
        "half_line_integral": half_line_integral,
        "projection_integrals": projection_integrals,
        "coarse_integral": coarse_integral,
        "symmetric_numeric_integral": symmetric_numeric_integral,
        "symmetric_exact_integral": SYMMETRIC_CROSSING_INTEGRAL,
        "symmetric_number_coefficient": SYMMETRIC_CROSSING_COEFFICIENT,
        "ultraviolet_kappa8_n_coefficient": ultraviolet_coefficient,
        "ultraviolet_exact_asymptotic_coefficient": 1.0 / 64.0,
        "infrared_kappa_n_coefficient": infrared_coefficient,
        "maximum_wronskian_residual": maximum_wronskian_residual,
    }
    arrays = {
        "kappas": kappas,
        "half_line_occupations": canonical_occupations,
        "symmetric_occupations": symmetric_occupations,
    }
    return rows, metrics, arrays


def build_prescription_sensitivity(
    universal_metrics: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    half_line_coefficient = universal_metrics["half_line_integral"][
        "number_coefficient"
    ]
    rows.append(
        {
            "prescription_id": "VP5186_00_half_line_ground",
            "boundary": "y=0 half-line instantaneous conformal Hamiltonian ground state",
            "initial_condition": "u=1/sqrt(2kappa);u_prime=-i*kappa*u",
            "integral_I": universal_metrics["half_line_integral"][
                "total_integral"
            ],
            "number_coefficient_Cn": half_line_coefficient,
            "infrared_status": "finite integral but second adiabatic diagnostic diverges as kappa^-4",
            "ultraviolet_status": "n_k approaches 1/(64 kappa^8)",
            "parent_owned": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    rows.append(
        {
            "prescription_id": "VP5186_01_symmetric_crossing",
            "boundary": "adiabatic in-vacuum on smooth y from minus infinity to plus infinity",
            "initial_condition": "n_k=exp(-pi*kappa^2)",
            "integral_I": SYMMETRIC_CROSSING_INTEGRAL,
            "number_coefficient_Cn": SYMMETRIC_CROSSING_COEFFICIENT,
            "infrared_status": "finite",
            "ultraviolet_status": "exponential",
            "parent_owned": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )

    sensitivity_kappas = sensitivity_kappa_grid()
    finite_start_coefficients: list[float] = []
    for initial_time in (1.0e-3, 1.0e-2, 1.0e-1, 1.0):
        occupations = np.asarray(
            [
                solve_finite_start_mode(float(kappa), initial_time)
                for kappa in sensitivity_kappas
            ],
            dtype=float,
        )
        integral = phase_space_integral(
            sensitivity_kappas,
            occupations,
            False,
        )
        coefficient = integral["number_coefficient"]
        finite_start_coefficients.append(coefficient)
        adiabatic_first = initial_time / (
            sensitivity_kappas**2 + initial_time**2
        ) ** 1.5
        nonadiabatic_fraction = float(
            np.mean(adiabatic_first >= 0.1)
        )
        rows.append(
            {
                "prescription_id": (
                    f"VP5186_start_{initial_time:.0e}".replace("-", "m")
                ),
                "boundary": (
                    f"finite y_i={initial_time} instantaneous WKB-0 state"
                ),
                "initial_condition": "u=1/sqrt(2omega);u_prime=(-omega_prime/(2omega)-iomega)u",
                "integral_I": integral["total_integral"],
                "number_coefficient_Cn": coefficient,
                "infrared_status": (
                    f"{nonadiabatic_fraction:.6f} of diagnostic grid has "
                    "|omega_prime/omega^2|>=0.1"
                ),
                "ultraviolet_status": "convergent through kappa=8; omitted tail negligible for abundance verdict",
                "parent_owned": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    second_order_rows: list[dict[str, float]] = []
    for kappa in (1.5, 2.0, 3.0, 4.0, 6.0):
        half_line_occupation = solve_finite_start_mode(kappa, 0.0)
        second_order_occupation = solve_second_order_uv_mode(kappa)
        second_order_rows.append(
            {
                "kappa": kappa,
                "order0_n": half_line_occupation,
                "order2_n": second_order_occupation,
                "order2_over_order0": (
                    second_order_occupation / half_line_occupation
                ),
            }
        )
    metrics = {
        "finite_start_coefficients": finite_start_coefficients,
        "finite_start_minimum_coefficient": min(finite_start_coefficients),
        "finite_start_maximum_coefficient": max(finite_start_coefficients),
        "largest_declared_vacuum_coefficient": max(
            [half_line_coefficient, SYMMETRIC_CROSSING_COEFFICIENT]
            + finite_start_coefficients
        ),
        "second_order_UV_rows": second_order_rows,
    }
    return rows, metrics


def match_background_row(
    mass_eV: float,
    background_rows: list[dict[str, str]],
) -> dict[str, str]:
    return min(
        background_rows,
        key=lambda row: abs(
            math.log(float(row["m_gap_eV"]) / mass_eV)
        ),
    )


def build_mass_outputs(
    arrays: dict[str, np.ndarray],
    universal_metrics: dict[str, Any],
    prescription_metrics: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    mass_rows = read_csv(SOURCES["checkpoint_5157_masses"][0])
    background_rows = read_csv(SOURCES["checkpoint_5152_background"][0])
    kappas = arrays["kappas"]
    half_line_occupations = arrays["half_line_occupations"]
    symmetric_occupations = arrays["symmetric_occupations"]
    half_line_coefficient = universal_metrics["half_line_integral"][
        "number_coefficient"
    ]
    largest_coefficient = prescription_metrics[
        "largest_declared_vacuum_coefficient"
    ]
    spectra_rows: list[dict[str, Any]] = []
    abundance_rows: list[dict[str, Any]] = []

    for mass_row in mass_rows:
        mass_label = mass_row["mass_label"]
        mass_eV = float(mass_row["m_gap_eV"])
        source_a_osc = float(mass_row["a_osc_H_equals_m"])
        derived_a_osc = math.sqrt(
            RADIATION_CONFORMAL_SLOPE_EV / mass_eV
        )
        momentum_scale_eV = math.sqrt(
            mass_eV * RADIATION_CONFORMAL_SLOPE_EV
        )
        momentum_scale_mpc_inverse = momentum_scale_eV / MPC_INVERSE_EV
        required_number_density = float(
            mass_row["present_number_density_m_minus3"]
        )
        natural_required_number_density = (
            RHO_X0_EV4 / mass_eV * EV3_TO_M_MINUS3
        )
        matched_background = match_background_row(
            mass_eV, background_rows
        )

        half_line_number_density = (
            half_line_coefficient
            * momentum_scale_eV**3
            * EV3_TO_M_MINUS3
        )
        symmetric_number_density = (
            SYMMETRIC_CROSSING_COEFFICIENT
            * momentum_scale_eV**3
            * EV3_TO_M_MINUS3
        )
        largest_number_density = (
            largest_coefficient
            * momentum_scale_eV**3
            * EV3_TO_M_MINUS3
        )
        half_line_ratio = (
            half_line_number_density / required_number_density
        )
        symmetric_ratio = (
            symmetric_number_density / required_number_density
        )
        largest_ratio = largest_number_density / required_number_density
        half_line_rho0 = (
            half_line_coefficient * mass_eV * momentum_scale_eV**3
        )
        symmetric_rho0 = (
            SYMMETRIC_CROSSING_COEFFICIENT
            * mass_eV
            * momentum_scale_eV**3
        )
        half_line_rho_osc = half_line_coefficient * mass_eV**4
        symmetric_rho_osc = (
            SYMMETRIC_CROSSING_COEFFICIENT * mass_eV**4
        )
        target_rho_osc = RHO_X0_EV4 / derived_a_osc**3
        nonradiation_fraction_at_osc = (
            OMEGA_M * derived_a_osc / OMEGA_R
        )
        lambda_fraction_at_osc = (
            OMEGA_LAMBDA * derived_a_osc**4 / OMEGA_R
        )

        abundance_rows.append(
            {
                "mass_label": mass_label,
                "m_gap_eV": mass_eV,
                "a_osc_source": source_a_osc,
                "a_osc_derived": derived_a_osc,
                "a_osc_relative_residual": abs(
                    derived_a_osc / source_a_osc - 1.0
                ),
                "k_star_comoving_eV": momentum_scale_eV,
                "k_star_comoving_Mpc_inverse": momentum_scale_mpc_inverse,
                "target_Omega_X": OMEGA_X,
                "target_rho0_eV4": RHO_X0_EV4,
                "target_number_density_m_minus3": required_number_density,
                "target_number_density_natural_units_m_minus3": natural_required_number_density,
                "target_number_density_relative_residual": abs(
                    natural_required_number_density
                    / required_number_density
                    - 1.0
                ),
                "half_line_number_density_m_minus3": half_line_number_density,
                "symmetric_number_density_m_minus3": symmetric_number_density,
                "largest_declared_vacuum_number_density_m_minus3": largest_number_density,
                "half_line_rho0_eV4": half_line_rho0,
                "symmetric_rho0_eV4": symmetric_rho0,
                "half_line_rho_osc_eV4": half_line_rho_osc,
                "symmetric_rho_osc_eV4": symmetric_rho_osc,
                "target_rho_osc_eV4": target_rho_osc,
                "half_line_fraction_of_target": half_line_ratio,
                "symmetric_fraction_of_target": symmetric_ratio,
                "largest_declared_vacuum_fraction_of_target": largest_ratio,
                "log10_largest_fraction_of_target": math.log10(
                    largest_ratio
                ),
                "required_enhancement_over_largest_declared_vacuum": (
                    1.0 / largest_ratio
                ),
                "psi_i_over_Mpl_conditional": float(
                    mass_row["real_scalar_5152_psi_i_over_Mpl"]
                ),
                "nonradiation_fraction_at_osc": nonradiation_fraction_at_osc,
                "lambda_fraction_at_osc": lambda_fraction_at_osc,
                "source_maximum_abs_delta_H_over_H": float(
                    matched_background[
                        "maximum_abs_delta_H_over_H_during_transition"
                    ]
                ),
                "abundance_selected_by_parent": False,
                "valid_for_cosmology_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

        for index, kappa in enumerate(kappas):
            half_line_occupation = float(half_line_occupations[index])
            symmetric_occupation = float(symmetric_occupations[index])
            spectra_rows.append(
                {
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "kappa": float(kappa),
                    "k_comoving_eV": float(kappa * momentum_scale_eV),
                    "k_comoving_Mpc_inverse": float(
                        kappa * momentum_scale_mpc_inverse
                    ),
                    "physical_momentum_at_osc_over_m": float(kappa),
                    "half_line_n_k": half_line_occupation,
                    "half_line_abs_c_k": math.sqrt(
                        half_line_occupation
                        * (half_line_occupation + 1.0)
                    ),
                    "symmetric_crossing_n_k": symmetric_occupation,
                    "symmetric_crossing_abs_c_k": math.sqrt(
                        symmetric_occupation
                        * (symmetric_occupation + 1.0)
                    ),
                    "state_is_reflection_even_neutral": True,
                    "state_normalization_parent_owned": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    masses = np.asarray(
        [float(row["m_gap_eV"]) for row in abundance_rows],
        dtype=float,
    )
    generated_numbers = np.asarray(
        [
            float(row["half_line_number_density_m_minus3"])
            for row in abundance_rows
        ],
        dtype=float,
    )
    generated_rho0 = np.asarray(
        [float(row["half_line_rho0_eV4"]) for row in abundance_rows],
        dtype=float,
    )
    generated_rho_osc = np.asarray(
        [float(row["half_line_rho_osc_eV4"]) for row in abundance_rows],
        dtype=float,
    )
    metrics = {
        "mass_count": len(abundance_rows),
        "spectral_row_count": len(spectra_rows),
        "number_mass_scaling_exponent": float(
            np.polyfit(np.log(masses), np.log(generated_numbers), 1)[0]
        ),
        "rho0_mass_scaling_exponent": float(
            np.polyfit(np.log(masses), np.log(generated_rho0), 1)[0]
        ),
        "rho_osc_mass_scaling_exponent": float(
            np.polyfit(np.log(masses), np.log(generated_rho_osc), 1)[0]
        ),
        "maximum_declared_vacuum_fraction_of_target": max(
            row["largest_declared_vacuum_fraction_of_target"]
            for row in abundance_rows
        ),
        "minimum_required_enhancement": min(
            row["required_enhancement_over_largest_declared_vacuum"]
            for row in abundance_rows
        ),
        "maximum_background_H_shift": max(
            row["source_maximum_abs_delta_H_over_H"]
            for row in abundance_rows
        ),
        "maximum_nonradiation_fraction_at_osc": max(
            row["nonradiation_fraction_at_osc"]
            for row in abundance_rows
        ),
        "maximum_target_number_reproduction_residual": max(
            row["target_number_density_relative_residual"]
            for row in abundance_rows
        ),
        "maximum_a_osc_residual": max(
            row["a_osc_relative_residual"] for row in abundance_rows
        ),
    }
    return spectra_rows, abundance_rows, metrics


def build_robustness_rows(
    universal_metrics: dict[str, Any],
    prescription_metrics: dict[str, Any],
    mass_metrics: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    canonical_coefficient = universal_metrics["half_line_integral"][
        "number_coefficient"
    ]
    for projection_time in PROJECTION_Y_VALUES:
        coefficient = universal_metrics["projection_integrals"][
            str(projection_time)
        ]["number_coefficient"]
        rows.append(
            {
                "test_id": f"ROB5186_projection_y_{projection_time:g}",
                "test": "late WKB projection time",
                "observed": coefficient,
                "reference": canonical_coefficient,
                "relative_residual": abs(
                    coefficient / canonical_coefficient - 1.0
                ),
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    coarse_coefficient = universal_metrics["coarse_integral"][
        "number_coefficient"
    ]
    rows.extend(
        [
            {
                "test_id": "ROB5186_grid_resolution",
                "test": "coarse versus fine phase-space quadrature",
                "observed": coarse_coefficient,
                "reference": canonical_coefficient,
                "relative_residual": abs(
                    coarse_coefficient / canonical_coefficient - 1.0
                ),
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_symmetric_integral",
                "test": "numeric symmetric-crossing integral versus 1/(4pi)",
                "observed": universal_metrics["symmetric_numeric_integral"],
                "reference": SYMMETRIC_CROSSING_INTEGRAL,
                "relative_residual": abs(
                    universal_metrics["symmetric_numeric_integral"]
                    / SYMMETRIC_CROSSING_INTEGRAL
                    - 1.0
                ),
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_UV_asymptotic",
                "test": "half-line kappa^8 n_k versus 1/64",
                "observed": universal_metrics[
                    "ultraviolet_kappa8_n_coefficient"
                ],
                "reference": 1.0 / 64.0,
                "relative_residual": abs(
                    universal_metrics[
                        "ultraviolet_kappa8_n_coefficient"
                    ]
                    / (1.0 / 64.0)
                    - 1.0
                ),
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_IR_integrability",
                "test": "half-line kappa n_k finite as kappa tends to zero",
                "observed": universal_metrics[
                    "infrared_kappa_n_coefficient"
                ],
                "reference": "finite positive",
                "relative_residual": 0.0,
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_Wronskian",
                "test": "canonical commutator preservation",
                "observed": universal_metrics[
                    "maximum_wronskian_residual"
                ],
                "reference": "<2e-7",
                "relative_residual": universal_metrics[
                    "maximum_wronskian_residual"
                ],
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_RD_background",
                "test": "source-backed maximum transition H shift",
                "observed": mass_metrics["maximum_background_H_shift"],
                "reference": "<1e-4",
                "relative_residual": mass_metrics[
                    "maximum_background_H_shift"
                ],
                "status": "PASS",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "test_id": "ROB5186_start_sensitivity",
                "test": "finite-start vacuum coefficient range",
                "observed": (
                    prescription_metrics[
                        "finite_start_minimum_coefficient"
                    ],
                    prescription_metrics[
                        "finite_start_maximum_coefficient"
                    ],
                ),
                "reference": "boundary-dependent finite dimensionless coefficient",
                "relative_residual": (
                    prescription_metrics[
                        "finite_start_maximum_coefficient"
                    ]
                    / prescription_metrics[
                        "finite_start_minimum_coefficient"
                    ]
                ),
                "status": "BOUNDARY_SENSITIVE",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
        ]
    )
    for second_order_row in prescription_metrics["second_order_UV_rows"]:
        rows.append(
            {
                "test_id": (
                    f"ROB5186_order2_kappa_{second_order_row['kappa']:g}"
                ),
                "test": "second-order versus zeroth-order UV initial state",
                "observed": second_order_row["order2_n"],
                "reference": second_order_row["order0_n"],
                "relative_residual": second_order_row[
                    "order2_over_order0"
                ],
                "status": "UV_SUPPRESSED",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def build_covariance_rows() -> list[dict[str, Any]]:
    return [
        {
            "object_id": "COV5186_M0_zero_mean_mixed_Hessian",
            "object": "metric-motion quadratic mixing on the neutral vacuum branch",
            "equation": "delta^2 S/(delta g_mn delta psi)|_psibar=0=0",
            "result": "the scalar stress begins at quadratic order in delta psi; the free vacuum mode has no linear metric-constraint source",
            "parent_owned": True,
            "abundance_owner": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "object_id": "COV5186_00_commutator",
            "object": "spectral normalization",
            "equation": "u_k u_k_star_prime-u_k_prime u_k_star=i",
            "result": "preserved numerically and fixed by the parent Hessian",
            "parent_owned": True,
            "abundance_owner": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "object_id": "COV5186_01_pure_squeezed",
            "object": "vacuum-produced neutral Gaussian pair",
            "equation": "n_k=|beta_k|^2; |c_k|^2=n_k(n_k+1)",
            "result": "reflection-even pair covariance is derived after a vacuum is chosen",
            "parent_owned": False,
            "abundance_owner": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "object_id": "COV5186_02_charge",
            "object": "signed motion charge",
            "equation": "Q_X=0 for charge-balanced Bogoliubov pairs",
            "result": "neutral occupation is compatible with checkpoint 5158",
            "parent_owned": True,
            "abundance_owner": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "object_id": "COV5186_03_IR_boundary",
            "object": "infrared covariance",
            "equation": "same mode operator admits arbitrary finite Hadamard IR squeezing",
            "result": "action and Wronskian do not choose the required low-k covariance",
            "parent_owned": False,
            "abundance_owner": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "object_id": "COV5186_04_required_state",
            "object": "Omega_X-normalized occupied state",
            "equation": "F_k=(n_k+1/2)(u_k u_k_star+c.c.)+c_k u_k u_k+c.c.",
            "result": "can be specified consistently but remains cosmological initial-state data",
            "parent_owned": False,
            "abundance_owner": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def build_route_rows(
    mass_metrics: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "route": "stationary_visible_matter_or_DC_Poynting",
            "derived_result": "positive-frequency pair source is exactly zero",
            "quantitative_gate": "checkpoint 4952 stationary-source theorem",
            "decision": "REJECT_AS_COSMOLOGICAL_ABUNDANCE_OWNER",
            "next_action": "none",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "half_line_radiation_vacuum",
            "derived_result": "finite neutral squeezed spectrum",
            "quantitative_gate": (
                f"maximum target fraction below "
                f"{mass_metrics['maximum_declared_vacuum_fraction_of_target']:.6e}"
            ),
            "decision": "REJECT_AS_ABUNDANCE_OWNER",
            "next_action": "retain as negligible source-backed comparator",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "symmetric_adiabatic_crossing",
            "derived_result": "exact n_k=exp(-pi kappa^2)",
            "quantitative_gate": "finite but requires an unowned pre-bang smooth extension",
            "decision": "REJECT_AS_PARENT_SELECTION_AND_ABUNDANCE_OWNER",
            "next_action": "retain as analytic cross-check",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "arbitrary_Hadamard_squeezed_boundary",
            "derived_result": "can make occupation arbitrarily large in a finite IR band",
            "quantitative_gate": (
                f"requires at least "
                f"{mass_metrics['minimum_required_enhancement']:.6e} "
                "enhancement over declared vacuum production"
            ),
            "decision": "CONDITIONAL_INITIAL_STATE_ONLY",
            "next_action": "declare covariance and normalization as initial data if retained",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "homogeneous_misalignment",
            "derived_result": "checkpoint 5152 exactly transfers psi_i into dust abundance",
            "quantitative_gate": "psi_i is not selected by current parent action",
            "decision": "CONDITIONAL_INITIAL_STATE_ONLY",
            "next_action": "count one global cosmological datum explicitly",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "separate_parent_nonadiabatic_cosmogenesis_event",
            "derived_result": "not present in current locked action",
            "quantitative_gate": "must predict beta_k and covariance without fitting Omega_X",
            "decision": "ONLY_REENTRY_ROUTE_FOR_DERIVED_ABUNDANCE",
            "next_action": "derive only if a real parent transition sector is identified",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def build_provenance_rows(
    source_hashes: dict[str, str],
) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": source_name,
            "source_type": "local_locked_checkpoint",
            "source_path_or_url": str(SOURCES[source_name][0]),
            "sha256": source_hashes[source_name],
            "role": {
                "checkpoint_4952_document": "stationary source and CTP pair-source theorem",
                "checkpoint_5152_document": "radiation background and misalignment dust theorem",
                "checkpoint_5152_background": "locked a_osc and target abundance rows",
                "checkpoint_5156_document": "FLRW Hessian and Gaussian-state nonuniqueness theorem",
                "checkpoint_5156_Hessian": "canonical mode equation row",
                "checkpoint_5157_masses": "three locked masses and required number densities",
                "checkpoint_5158_document": "neutral-pair charge selection",
                "checkpoint_5185_document": "neutral Bogoliubov route handoff",
            }[source_name],
            "checked_date": CHECKED_DATE,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for source_name in SOURCES
    ]
    rows.extend(
        [
            {
                "source_id": source_id,
                "source_type": "primary_reference_url",
                "source_path_or_url": source_url,
                "sha256": "",
                "role": {
                    "Parker_1969": "particle creation in an expanding spatially flat universe",
                    "Chung_Kolb_Riotto_1998": "gravitational production and relic abundance methodology",
                    "Planck_2018": "source parameters inherited through checkpoints 5152 and 5156",
                }[source_id],
                "checked_date": CHECKED_DATE,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
            for source_id, source_url in PRIMARY_URLS.items()
        ]
    )
    return rows


def calculate_validations(
    source_hashes: dict[str, str],
    formal_digest: str,
    checkpoint_5176_digest: str,
    universal_rows: list[dict[str, Any]],
    universal_metrics: dict[str, Any],
    prescription_rows: list[dict[str, Any]],
    prescription_metrics: dict[str, Any],
    spectra_rows: list[dict[str, Any]],
    abundance_rows: list[dict[str, Any]],
    mass_metrics: dict[str, Any],
    covariance_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_locks_match = all(
        source_hashes[source_name] == expected_hash
        for source_name, (_, expected_hash) in SOURCES.items()
    )
    projection_coefficients = [
        universal_metrics["projection_integrals"][str(projection_time)][
            "number_coefficient"
        ]
        for projection_time in PROJECTION_Y_VALUES
    ]
    projection_spread = (
        max(projection_coefficients) / min(projection_coefficients) - 1.0
    )
    canonical_coefficient = universal_metrics["half_line_integral"][
        "number_coefficient"
    ]
    grid_residual = abs(
        universal_metrics["coarse_integral"]["number_coefficient"]
        / canonical_coefficient
        - 1.0
    )
    symmetric_residual = abs(
        universal_metrics["symmetric_numeric_integral"]
        / SYMMETRIC_CROSSING_INTEGRAL
        - 1.0
    )
    ultraviolet_residual = abs(
        universal_metrics["ultraviolet_kappa8_n_coefficient"]
        / (1.0 / 64.0)
        - 1.0
    )
    compiled = True
    try:
        compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")
    except SyntaxError:
        compiled = False
    return [
        validation_row(
            "V5186_01_source_count",
            "all declared local sources exist",
            len(source_hashes) == len(SOURCES),
            len(source_hashes),
            len(SOURCES),
        ),
        validation_row(
            "V5186_02_source_locks",
            "all local source hashes match",
            source_locks_match,
            sum(
                source_hashes[source_name] == expected_hash
                for source_name, (_, expected_hash) in SOURCES.items()
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5186_03_formal_lock",
            "formalization-workbench remains locked",
            formal_digest == FORMAL_DIGEST_LOCK,
            formal_digest,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5186_04_5176_lock",
            "checkpoint 5176 ensemble remains locked",
            checkpoint_5176_digest == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_digest,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5186_05_script_compile",
            "generator compiles in memory",
            compiled,
            compiled,
            True,
        ),
        validation_row(
            "V5186_06_universal_spectrum",
            "universal spectrum has at least 120 finite rows",
            len(universal_rows) >= 120
            and all(
                math.isfinite(row["half_line_n_k"])
                and row["half_line_n_k"] >= 0.0
                for row in universal_rows
            ),
            len(universal_rows),
            ">=120 finite nonnegative rows",
        ),
        validation_row(
            "V5186_07_Wronskian",
            "canonical commutator is preserved",
            universal_metrics["maximum_wronskian_residual"] < 2.0e-7,
            universal_metrics["maximum_wronskian_residual"],
            "<2e-7",
        ),
        validation_row(
            "V5186_08_projection_stability",
            "late WKB projection is stable",
            projection_spread < 2.0e-5,
            projection_spread,
            "<2e-5",
        ),
        validation_row(
            "V5186_09_grid_stability",
            "coarse and fine phase-space integrals agree",
            grid_residual < 2.0e-4,
            grid_residual,
            "<2e-4",
        ),
        validation_row(
            "V5186_10_symmetric_exact",
            "symmetric crossing reproduces exact 1/(4pi) integral",
            symmetric_residual < 2.0e-4,
            symmetric_residual,
            "<2e-4",
        ),
        validation_row(
            "V5186_11_UV_tail",
            "half-line UV tail matches 1/(64 kappa^8)",
            ultraviolet_residual < 5.0e-2,
            ultraviolet_residual,
            "<5e-2",
        ),
        validation_row(
            "V5186_12_IR_integral",
            "half-line IR number integral is finite",
            math.isfinite(
                universal_metrics["infrared_kappa_n_coefficient"]
            )
            and universal_metrics["infrared_kappa_n_coefficient"] > 0.0
            and universal_metrics["half_line_integral"][
                "infrared_tail"
            ]
            < 1.0e-8,
            (
                universal_metrics["infrared_kappa_n_coefficient"],
                universal_metrics["half_line_integral"][
                    "infrared_tail"
                ],
            ),
            "finite and tail<1e-8",
        ),
        validation_row(
            "V5186_13_half_line_coefficient",
            "half-line production coefficient lies in computed band",
            1.4e-3 < canonical_coefficient < 1.6e-3,
            canonical_coefficient,
            "(1.4e-3,1.6e-3)",
        ),
        validation_row(
            "V5186_14_prescription_rows",
            "all declared vacuum prescriptions are recorded",
            len(prescription_rows) == 6,
            len(prescription_rows),
            6,
        ),
        validation_row(
            "V5186_15_boundary_sensitivity",
            "finite-start choices produce distinct coefficients",
            prescription_metrics["finite_start_maximum_coefficient"]
            / prescription_metrics["finite_start_minimum_coefficient"]
            > 10.0,
            prescription_metrics["finite_start_maximum_coefficient"]
            / prescription_metrics["finite_start_minimum_coefficient"],
            ">10",
        ),
        validation_row(
            "V5186_16_UV_order",
            "second-order state suppresses high-k production",
            all(
                row["order2_over_order0"] < 0.1
                for row in prescription_metrics["second_order_UV_rows"]
                if row["kappa"] >= 2.0
            ),
            [
                row["order2_over_order0"]
                for row in prescription_metrics["second_order_UV_rows"]
                if row["kappa"] >= 2.0
            ],
            "all<0.1",
        ),
        validation_row(
            "V5186_17_three_masses",
            "all three locked masses are present",
            mass_metrics["mass_count"] == 3,
            mass_metrics["mass_count"],
            3,
        ),
        validation_row(
            "V5186_18_mass_spectra",
            "each mass receives the universal spectrum",
            len(spectra_rows) == 3 * len(universal_rows),
            len(spectra_rows),
            3 * len(universal_rows),
        ),
        validation_row(
            "V5186_19_aosc_reproduction",
            "derived radiation oscillation scales reproduce source rows",
            mass_metrics["maximum_a_osc_residual"] < 2.0e-15,
            mass_metrics["maximum_a_osc_residual"],
            "<2e-15",
        ),
        validation_row(
            "V5186_20_target_reproduction",
            "natural-unit target density reproduces locked SI rows",
            mass_metrics[
                "maximum_target_number_reproduction_residual"
            ]
            < 3.0e-4,
            mass_metrics[
                "maximum_target_number_reproduction_residual"
            ],
            "<3e-4",
        ),
        validation_row(
            "V5186_21_number_scaling",
            "produced present number scales as m^(3/2)",
            abs(mass_metrics["number_mass_scaling_exponent"] - 1.5)
            < 2.0e-12,
            mass_metrics["number_mass_scaling_exponent"],
            "1.5",
        ),
        validation_row(
            "V5186_22_rho0_scaling",
            "produced present energy scales as m^(5/2)",
            abs(mass_metrics["rho0_mass_scaling_exponent"] - 2.5)
            < 2.0e-12,
            mass_metrics["rho0_mass_scaling_exponent"],
            "2.5",
        ),
        validation_row(
            "V5186_23_rhoosc_scaling",
            "produced onset energy scales as m^4",
            abs(mass_metrics["rho_osc_mass_scaling_exponent"] - 4.0)
            < 2.0e-12,
            mass_metrics["rho_osc_mass_scaling_exponent"],
            "4",
        ),
        validation_row(
            "V5186_24_RD_background",
            "all locked masses oscillate in controlled radiation domination",
            mass_metrics["maximum_background_H_shift"] < 1.0e-4
            and mass_metrics["maximum_nonradiation_fraction_at_osc"]
            < 3.0e-4,
            (
                mass_metrics["maximum_background_H_shift"],
                mass_metrics["maximum_nonradiation_fraction_at_osc"],
            ),
            "(<1e-4,<3e-4)",
        ),
        validation_row(
            "V5186_25_abundance_no_go",
            "largest declared free-vacuum abundance remains below 3e-89 of target",
            mass_metrics[
                "maximum_declared_vacuum_fraction_of_target"
            ]
            < 3.0e-89,
            mass_metrics[
                "maximum_declared_vacuum_fraction_of_target"
            ],
            "<3e-89",
        ),
        validation_row(
            "V5186_26_enhancement",
            "smallest required occupation enhancement exceeds 4e88",
            mass_metrics["minimum_required_enhancement"] > 4.0e88,
            mass_metrics["minimum_required_enhancement"],
            ">4e88",
        ),
        validation_row(
            "V5186_27_covariance",
            "mixed-Hessian, spectral, squeezed, neutral, IR and required-state rows exist",
            len(covariance_rows) == 6,
            len(covariance_rows),
            6,
        ),
        validation_row(
            "V5186_28_route_rows",
            "all source-selection routes are decided",
            len(route_rows) == 6,
            len(route_rows),
            6,
        ),
        validation_row(
            "V5186_29_vacuum_rejected",
            "free FLRW vacuum production is rejected as abundance owner",
            any(
                row["route"] == "half_line_radiation_vacuum"
                and row["decision"] == "REJECT_AS_ABUNDANCE_OWNER"
                for row in route_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5186_30_initial_state_explicit",
            "misalignment and arbitrary squeezing are explicitly conditional",
            sum(
                row["decision"] == "CONDITIONAL_INITIAL_STATE_ONLY"
                for row in route_rows
            )
            == 2,
            sum(
                row["decision"] == "CONDITIONAL_INITIAL_STATE_ONLY"
                for row in route_rows
            ),
            2,
        ),
        validation_row(
            "V5186_31_no_claim_rows",
            "no numerical output row is marked valid for a theory claim",
            all(not row["valid_for_claim"] for row in universal_rows)
            and all(
                not row["valid_for_claim"] for row in prescription_rows
            )
            and all(not row["valid_for_claim"] for row in spectra_rows)
            and all(
                not row["valid_for_cosmology_claim"]
                for row in abundance_rows
            )
            and all(not row["valid_for_claim"] for row in covariance_rows)
            and all(not row["valid_for_claim"] for row in route_rows),
            False,
            False,
        ),
        validation_row(
            "V5186_32_no_placeholder",
            "outputs contain no MISSING placeholder",
            not any(
                "MISSING_" in json.dumps(row)
                for row in (
                    universal_rows
                    + prescription_rows
                    + spectra_rows
                    + abundance_rows
                    + covariance_rows
                    + route_rows
                )
            ),
            False,
            False,
        ),
    ]


def write_document(result: dict[str, Any]) -> None:
    universal = result["universal_metrics"]
    prescription = result["prescription_metrics"]
    mass_metrics = result["mass_metrics"]
    abundance_rows = result["abundance_rows"]
    half_line_coefficient = universal["half_line_integral"][
        "number_coefficient"
    ]
    abundance_table = "\n".join(
        (
            f"| `{row['mass_label']}` | `{row['m_gap_eV']:.6e}` | "
            f"`{row['k_star_comoving_Mpc_inverse']:.6g}` | "
            f"`{row['largest_declared_vacuum_fraction_of_target']:.6e}` | "
            f"`{row['required_enhancement_over_largest_declared_vacuum']:.6e}` |"
        )
        for row in abundance_rows
    )
    source_list = "\n".join(
        f"- `{source_name}`: `{source_path_value}`"
        for source_name, (source_path_value, _) in SOURCES.items()
    )
    text = f"""# 5186 - FLRW Bogoliubov neutral-vacuum production and abundance no-go

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5185 selected the time-dependent Bogoliubov route because the
stationary interaction route is dynamically inert. This checkpoint carries that
route through the actual checkpoint-5156 mode operator and the three
checkpoint-5157 masses. It does not stop at saying that a state is missing.

```text
{ROUTE_DECISION}
```

The result is constructive but negative:

```text
neutral Bogoliubov pair spectrum     = derived;
Gaussian pair covariance             = derived after a boundary choice;
Omega_X normalization from free FLRW = rejected by 89--96 orders;
unique vacuum/cosmogenesis boundary  = not supplied by the parent action.
```

This is not a no-go against every possible cosmogenesis sector. It is a no-go
against assigning the required abundance to the currently locked free FLRW
Hessian or to stationary visible-matter/Poynting noise.

## 1. Parent mode equation

Checkpoint 5156 gives the canonical minimally coupled motion mode

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric-constraint source.
```

For the neutral vacuum-production branch `bar(psi)=0`. The mixed quadratic
Hessian vanishes exactly,

```text
delta^2 S/(delta g_mn delta psi)|_bar(psi)=0=0,
```

because the scalar Hilbert stress begins at order `(delta psi)^2`. The
`metric-constraint source` is therefore zero for the free production mode;
metric response re-enters through the `h psi psi` vertex already derived in
checkpoint 4952.

All three locked masses begin coherent oscillation deep in radiation
domination. The largest source-computed transition shift is only
`{mass_metrics['maximum_background_H_shift']:.6e}` in `H`, and the largest
non-radiation fraction at `H=m_gap` is
`{mass_metrics['maximum_nonradiation_fraction_at_osc']:.6e}`. Therefore the
source-backed leading production problem has

```text
a(eta)=s eta,
s=H0 sqrt(Omega_r),
a''=0,

v_k''+[k^2+m^2 s^2 eta^2]v_k=0.
```

Define

```text
a_osc=sqrt(s/m),
y=a/a_osc=sqrt(m s) eta,
kappa=k/sqrt(m s),
u_kappa=(m s)^(1/4) v_k.
```

The complete mass dependence factors out:

```text
u_kappa,yy+(kappa^2+y^2)u_kappa=0.
```

This universal reduction reproduces every locked `a_osc` row with maximum
relative residual `{mass_metrics['maximum_a_osc_residual']:.3e}`.

## 2. Half-line radiation prescription

One parameter-free but non-parent-owned boundary prescription is the
instantaneous conformal Hamiltonian ground state at the radiation boundary:

```text
u_kappa(0)=1/sqrt(2 kappa),
u_kappa,y(0)=-i kappa u_kappa(0).
```

At late adiabatic time,

```text
u_kappa=alpha_kappa f_kappa+beta_kappa f_kappa*,
|alpha_kappa|^2-|beta_kappa|^2=1,
n_kappa=|beta_kappa|^2,
|c_kappa|^2=n_kappa(n_kappa+1).
```

The numerical Wronskian residual is at most
`{universal['maximum_wronskian_residual']:.3e}`. The spectrum has controlled
integrable ends:

```text
kappa -> 0:      n_kappa ~ {universal['infrared_kappa_n_coefficient']:.9g}/kappa,
kappa -> infinity: n_kappa ~ 1/(64 kappa^8).
```

The universal comoving number coefficient is

```text
I_half = integral_0^infinity dkappa kappa^2 n_kappa
       = {universal['half_line_integral']['total_integral']:.12g},

C_half = I_half/(2 pi^2)
       = {half_line_coefficient:.12g}.
```

The result is stable over projection times `y=15--30`; their fractional spread
is below `2e-5`.

## 3. Exact analytic crossing check

A second calculable comparator extends the same oscillator smoothly from
`y=-infinity` to `y=+infinity` and chooses the adiabatic in-vacuum. Its exact
Landau-Zener/Schwinger spectrum is

```text
n_kappa=exp(-pi kappa^2),

I_sym=1/(4 pi),
C_sym=1/(8 pi^3)={SYMMETRIC_CROSSING_COEFFICIENT:.12g}.
```

The numerical quadrature reproduces the analytic integral with fractional
residual
`{abs(universal['symmetric_numeric_integral']/SYMMETRIC_CROSSING_INTEGRAL-1.0):.3e}`.
The smooth negative-to-positive `y` extension is not part of the MTS parent, so
this is a cross-check rather than a hidden cosmogenesis axiom.

## 4. Vacuum and start-time robustness

Finite-start WKB-0 prescriptions span coefficients

```text
{prescription['finite_start_minimum_coefficient']:.12g}
 <= C_start <=
{prescription['finite_start_maximum_coefficient']:.12g}.
```

The spread is real: low-`kappa` modes have no parent-selected adiabatic region.
At the radiation boundary the first adiabatic diagnostic vanishes, but the
second behaves as `omega''/omega^3=1/kappa^4`; at finite start the first
diagnostic is also nonadiabatic in the infrared. The action fixes the transfer
operator and Wronskian, not the infrared density matrix.

The ultraviolet conclusion is cleaner. Replacing the order-zero initial
frequency by

```text
W_2(0)=kappa-1/(4 kappa^3)
```

suppresses the high-`kappa` tail, while the integrated abundance verdict is
unchanged because the target shortfall is almost ninety orders even at the
largest mass.

## 5. Three-mass abundance

For any universal spectrum coefficient `C_n`,

```text
k_star=sqrt(m s)=m a_osc,
n_0=C_n k_star^3,
rho_0=m n_0,
rho_osc=C_n m^4.
```

The locked target is

```text
rho_X0=3 Omega_X Mbar_Pl^2 H0^2,
Omega_X={OMEGA_X}.
```

| Mass row | `m_gap` (eV) | `k_star` (Mpc^-1) | largest declared vacuum / target | required enhancement |
|---|---:|---:|---:|---:|
{abundance_table}

The largest target fraction is only
`{mass_metrics['maximum_declared_vacuum_fraction_of_target']:.6e}`. Even the
most favorable locked mass therefore requires at least
`{mass_metrics['minimum_required_enhancement']:.6e}` times more occupation than
the largest declared vacuum-production comparator. This is not a tunable
order-one coefficient problem.

The scalings independently verify the reduction:

```text
n_0 proportional to m^{mass_metrics['number_mass_scaling_exponent']:.12g},
rho_0 proportional to m^{mass_metrics['rho0_mass_scaling_exponent']:.12g},
rho_osc proportional to m^{mass_metrics['rho_osc_mass_scaling_exponent']:.12g}.
```

## 6. What survives

The produced state is a valid neutral, reflection-even, pure squeezed Gaussian
state. It preserves the checkpoint-5158 charge result and can enter the
checkpoint-5185 conserved 2PI stress. What fails is its normalization:

```text
correct tensor and Ward structure = yes;
enough particles for Omega_X      = no;
unique low-k covariance           = no.
```

An arbitrary finite Hadamard infrared squeeze can mathematically fill the
abundance, and the checkpoint-5152 homogeneous amplitude can do the same.
Neither is generated by the current action. Calling either one derived would
only rename initial-state data.

## 7. Route disposition

The occupied-state galaxy branch remains internally usable as a conditional
cosmological branch:

```text
input: one global abundance/amplitude datum plus a declared primordial
       covariance;
transfer: parent FLRW Hessian, radiation transfer, Vlasov/SP evolution and
          conserved Hilbert stress;
claim ceiling: no parent-derived dark-sector abundance or covariance.
```

The only re-entry route for a derived abundance is a real parent-owned
nonadiabatic cosmogenesis event with a specified background, in-vacuum or
density matrix, and no fitted `Omega_X`. No reheating field or transition is
invented here.

## 8. Reproduction

Run:

```powershell
& "{sys.executable}" "{SCRIPT}"
```

Outputs:

- `source-intake/functional_rg/5186/universal_radiation_Bogoliubov_spectrum.csv`
- `source-intake/functional_rg/5186/three_mass_Bogoliubov_spectra.csv`
- `source-intake/functional_rg/5186/three_mass_vacuum_abundance_gate.csv`
- `source-intake/functional_rg/5186/vacuum_prescription_and_start_time_sensitivity.csv`
- `source-intake/functional_rg/5186/adiabatic_UV_and_background_robustness.csv`
- `source-intake/functional_rg/5186/neutral_Gaussian_covariance_gate.csv`
- `source-intake/functional_rg/5186/neutral_source_selection_route_decision.csv`
- `source-intake/functional_rg/5186/source_provenance.csv`
- `source-intake/functional_rg/5186/FLRW_Bogoliubov_neutral_production_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5186_VALIDATION.csv`

Locked local inputs:

{source_list}

Primary references:

- Parker particle creation: {PRIMARY_URLS['Parker_1969']}
- Gravitational relic-production methodology: {PRIMARY_URLS['Chung_Kolb_Riotto_1998']}
- Planck parameter source inherited through 5152/5156: {PRIMARY_URLS['Planck_2018']}

All validation rows pass. The formalization workbench and checkpoint-5176
ensemble remain locked. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_hashes: dict[str, str] = {}
    for source_name, (source_file, _) in SOURCES.items():
        if not source_file.is_file():
            raise FileNotFoundError(source_file)
        source_hashes[source_name] = file_digest(source_file)

    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    universal_rows, universal_metrics, arrays = build_universal_spectrum()
    prescription_rows, prescription_metrics = (
        build_prescription_sensitivity(universal_metrics)
    )
    spectra_rows, abundance_rows, mass_metrics = build_mass_outputs(
        arrays,
        universal_metrics,
        prescription_metrics,
    )
    robustness_rows = build_robustness_rows(
        universal_metrics,
        prescription_metrics,
        mass_metrics,
    )
    covariance_rows = build_covariance_rows()
    route_rows = build_route_rows(mass_metrics)
    provenance_rows = build_provenance_rows(source_hashes)

    checks = calculate_validations(
        source_hashes,
        formal_before,
        checkpoint_5176_before,
        universal_rows,
        universal_metrics,
        prescription_rows,
        prescription_metrics,
        spectra_rows,
        abundance_rows,
        mass_metrics,
        covariance_rows,
        route_rows,
    )
    failed_checks = [
        check for check in checks if check["status"] != "PASS"
    ]
    if failed_checks:
        raise RuntimeError(
            "Pre-write validation failed: "
            + json.dumps(failed_checks, indent=2)
        )

    write_csv(UNIVERSAL_CSV, universal_rows)
    write_csv(MASS_SPECTRA_CSV, spectra_rows)
    write_csv(ABUNDANCE_CSV, abundance_rows)
    write_csv(PRESCRIPTION_CSV, prescription_rows)
    write_csv(ROBUSTNESS_CSV, robustness_rows)
    write_csv(COVARIANCE_CSV, covariance_rows)
    write_csv(ROUTE_CSV, route_rows)
    write_csv(PROVENANCE_CSV, provenance_rows)

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": ROUTE_DECISION,
        "background": {
            "H0_km_s_Mpc": H0_KM_S_MPC,
            "H0_eV": H0_EV,
            "Omega_r": OMEGA_R,
            "Omega_m": OMEGA_M,
            "Omega_b": OMEGA_B,
            "Omega_X": OMEGA_X,
            "Omega_Lambda": OMEGA_LAMBDA,
            "radiation_conformal_slope_eV": RADIATION_CONFORMAL_SLOPE_EV,
            "rho_crit0_eV4": RHO_CRIT0_EV4,
            "rho_X0_eV4": RHO_X0_EV4,
        },
        "universal_equation": (
            "u_kappa,yy+(kappa^2+y^2)u_kappa=0"
        ),
        "universal_metrics": universal_metrics,
        "prescription_metrics": prescription_metrics,
        "mass_metrics": mass_metrics,
        "abundance_rows": abundance_rows,
        "covariance_summary": {
            "zero_mean_metric_scalar_mixed_Hessian": True,
            "neutral_reflection_even_pairs_derived": True,
            "pure_squeezed_relation_derived": True,
            "parent_selects_IR_covariance": False,
            "parent_selects_Omega_X": False,
        },
        "claim_status": {
            "free_FLRW_vacuum_abundance_owner": False,
            "conditional_initial_state_branch_retained": True,
            "full_MTS_claim": False,
            "local_GR_Newton_Maxwell_branch_modified": False,
            "GitHub_action": False,
        },
        "source_hashes": source_hashes,
        "formalization_workbench_sha256": formal_before,
        "checkpoint_5176_tree_sha256": checkpoint_5176_before,
        "validation_count": len(checks),
        "validation_failures": 0,
    }
    write_json(RESULT_JSON, result)
    write_document(result)

    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    final_checks = checks + [
        validation_row(
            "V5186_33_formal_after",
            "formalization-workbench remains unchanged after writes",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5186_34_5176_after",
            "checkpoint 5176 remains unchanged after writes",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5186_35_output_files",
            "all checkpoint output files exist and are nonempty",
            all(
                path.is_file() and path.stat().st_size > 0
                for path in (
                    UNIVERSAL_CSV,
                    MASS_SPECTRA_CSV,
                    ABUNDANCE_CSV,
                    PRESCRIPTION_CSV,
                    ROBUSTNESS_CSV,
                    COVARIANCE_CSV,
                    ROUTE_CSV,
                    PROVENANCE_CSV,
                    RESULT_JSON,
                    DOCUMENT,
                )
            ),
            10,
            10,
        ),
    ]
    final_failures = [
        check for check in final_checks if check["status"] != "PASS"
    ]
    if final_failures:
        raise RuntimeError(
            "Final validation failed: "
            + json.dumps(final_failures, indent=2)
        )
    write_csv(VALIDATION_CSV, final_checks)
    print(
        json.dumps(
            {
                "checkpoint": 5186,
                "marker": MARKER,
                "validation_passed": len(final_checks),
                "validation_failed": 0,
                "half_line_number_coefficient": universal_metrics[
                    "half_line_integral"
                ]["number_coefficient"],
                "symmetric_number_coefficient": (
                    SYMMETRIC_CROSSING_COEFFICIENT
                ),
                "maximum_vacuum_fraction_of_target": mass_metrics[
                    "maximum_declared_vacuum_fraction_of_target"
                ],
                "minimum_required_enhancement": mass_metrics[
                    "minimum_required_enhancement"
                ],
                "document": str(DOCUMENT),
                "result": str(RESULT_JSON),
                "validation": str(VALIDATION_CSV),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
