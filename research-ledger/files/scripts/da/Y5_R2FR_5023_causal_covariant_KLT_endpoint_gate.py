from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5017 = POST / "scripts" / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
SCRIPT_5019 = POST / "scripts" / "Y5_R2FR_5019_hhh_exact_soft_endpoint_and_crossed_pole_theorem.py"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5017 = load_module("mts_5017_for_5023", SCRIPT_5017)
M5019 = load_module("mts_5019_for_5023", SCRIPT_5019)


def minkowski(left: np.ndarray, right: np.ndarray) -> complex:
    return complex(left[0] * right[0] - np.dot(left[1:], right[1:]))


def spinor_bracket(left: np.ndarray, right: np.ndarray) -> complex:
    return complex(left[0] * right[1] - left[1] * right[0])


def bispinor_to_vector(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            (matrix[0, 0] + matrix[1, 1]) / 2.0,
            (matrix[0, 1] + matrix[1, 0]) / 2.0,
            (matrix[1, 0] - matrix[0, 1]) / (2.0j),
            (matrix[0, 0] - matrix[1, 1]) / 2.0,
        ],
        dtype=np.complex128,
    )


def polarization(
    momentum: np.ndarray, reference: np.ndarray, helicity: int
) -> np.ndarray:
    angle_momentum, square_momentum = M5017.massless_spinors(momentum)
    angle_reference, square_reference = M5017.massless_spinors(reference)
    if helicity == 1:
        denominator = spinor_bracket(angle_reference, angle_momentum)
        matrix = (
            math.sqrt(2.0)
            * np.outer(angle_reference, square_momentum)
            / denominator
        )
    elif helicity == -1:
        denominator = spinor_bracket(square_momentum, square_reference)
        matrix = (
            math.sqrt(2.0)
            * np.outer(angle_momentum, square_reference)
            / denominator
        )
    else:
        raise ValueError("helicity must be +1 or -1")
    return bispinor_to_vector(matrix)


def field_strength_contraction(
    left: np.ndarray,
    momentum: np.ndarray,
    polarization_vector: np.ndarray,
    right: np.ndarray,
) -> complex:
    return minkowski(left, momentum) * minkowski(
        polarization_vector, right
    ) - minkowski(left, polarization_vector) * minkowski(momentum, right)


def subtracted_invariant(*momenta: np.ndarray) -> complex:
    total = sum(momenta, np.zeros(4, dtype=np.complex128))
    return minkowski(total, total) - sum(
        minkowski(momentum, momentum) for momentum in momenta
    )


def causal(value: complex, epsilon: float) -> complex:
    return value + 1.0j * epsilon


def canonical_gauge_four(
    momenta: list[np.ndarray],
    polarizations: list[np.ndarray],
    epsilon: float,
) -> complex:
    scalar_left, graviton_two, graviton_three, scalar_right = momenta
    epsilon_two, epsilon_three = polarizations
    s_23 = subtracted_invariant(graviton_two, graviton_three)
    s_12 = subtracted_invariant(scalar_left, graviton_two)
    numerator_23 = 2.0 * minkowski(
        epsilon_two, scalar_left
    ) * minkowski(epsilon_three, graviton_two) - 2.0 * field_strength_contraction(
        epsilon_two,
        graviton_three,
        epsilon_three,
        scalar_left,
    )
    numerator_12 = -2.0 * minkowski(
        epsilon_two, scalar_left
    ) * minkowski(epsilon_three, scalar_right)
    return numerator_23 / causal(s_23, epsilon) + numerator_12 / causal(
        s_12, epsilon
    )


def ordered_shuffles(left: list[int], right: list[int]) -> list[list[int]]:
    if not left:
        return [list(right)]
    if not right:
        return [list(left)]
    return [
        [left[0], *remainder]
        for remainder in ordered_shuffles(left[1:], right)
    ] + [
        [right[0], *remainder]
        for remainder in ordered_shuffles(left, right[1:])
    ]


def gauge_four_ordered(
    order: list[int],
    momenta: np.ndarray,
    polarizations: dict[int, np.ndarray],
    epsilon: float,
) -> complex:
    rotated = list(order)
    scalar_start = rotated.index(0)
    rotated = rotated[scalar_start:] + rotated[:scalar_start]
    scalar_end = rotated.index(4)
    alpha = rotated[1:scalar_end]
    beta = rotated[scalar_end + 1 :]
    result = 0.0j
    for shuffle in ordered_shuffles(alpha, list(reversed(beta))):
        result += canonical_gauge_four(
            [momenta[0], *[momenta[index] for index in shuffle], momenta[4]],
            [polarizations[index] for index in shuffle],
            epsilon,
        )
    return ((-1) ** len(beta)) * result


def canonical_gauge_five(
    momenta: list[np.ndarray],
    polarizations: list[np.ndarray],
    epsilon: float,
) -> complex:
    scalar_left, k_two, k_three, k_four, scalar_right = momenta
    epsilon_two, epsilon_three, epsilon_four = polarizations

    def dot(left: np.ndarray, right: np.ndarray) -> complex:
        return minkowski(left, right)

    def denominator(value: complex) -> complex:
        return causal(value, epsilon)

    s_23 = subtracted_invariant(k_two, k_three)
    s_34 = subtracted_invariant(k_three, k_four)
    s_234 = subtracted_invariant(k_two, k_three, k_four)
    s_p12 = subtracted_invariant(scalar_left, k_two)
    s_p14 = subtracted_invariant(scalar_left, k_four)
    s_4p5 = subtracted_invariant(k_four, scalar_right)

    eps_p_21 = dot(epsilon_two, scalar_left)
    eps_p_25 = dot(epsilon_two, scalar_right)
    eps_p_31 = dot(epsilon_three, scalar_left)
    eps_p_32 = dot(epsilon_three, k_two)
    eps_p_35 = dot(epsilon_three, scalar_right)
    eps_p_41 = dot(epsilon_four, scalar_left)
    eps_p_45 = dot(epsilon_four, scalar_right)
    eps_k_21 = dot(epsilon_two, scalar_left)
    eps_k_23 = dot(epsilon_two, k_three)
    eps_k_32 = dot(epsilon_three, k_two)
    eps_k_34 = dot(epsilon_three, k_four)
    eps_k_42 = dot(epsilon_four, k_two)
    eps_k_43 = dot(epsilon_four, k_three)
    eps_eps_23 = dot(epsilon_two, epsilon_three)
    eps_eps_24 = dot(epsilon_two, epsilon_four)
    eps_eps_34 = dot(epsilon_three, epsilon_four)
    eps_f_eps_342 = field_strength_contraction(
        epsilon_three, k_four, epsilon_four, epsilon_two
    )
    eps_f_eps_243 = field_strength_contraction(
        epsilon_two, k_four, epsilon_four, epsilon_three
    )

    result = eps_p_21 * (
        eps_eps_34 * s_34
        - 2.0 * eps_k_34 * eps_p_45
        + 2.0 * eps_k_43 * eps_p_35
    ) / (denominator(s_p12) * denominator(s_34))
    result += (
        eps_eps_23 * eps_k_43 * s_23
        - eps_eps_34 * eps_p_21 * s_23
        - eps_eps_23 * eps_p_41 * s_34
        - eps_f_eps_342 * s_23
    ) / (denominator(s_23) * denominator(s_34))
    result += eps_eps_34 * eps_p_21 * s_4p5 / (
        denominator(s_p12) * denominator(s_34)
    )
    result += 2.0 * eps_p_21 * eps_p_45 * (
        eps_p_31 + eps_p_32
    ) / (denominator(s_p12) * denominator(s_4p5))
    result += eps_p_45 * (
        2.0 * eps_k_21 * eps_p_32
        - 2.0 * eps_k_23 * eps_p_31
        - eps_eps_23 * s_23
    ) / (denominator(s_23) * denominator(s_4p5))
    result += (
        s_p12 * eps_f_eps_243
        + eps_eps_23 * eps_k_43 * s_p12
        - eps_eps_34 * eps_p_21 * s_p14
        - eps_eps_34 * eps_p_25 * s_p14
        + eps_eps_34 * eps_p_21 * s_23
    ) / (denominator(s_34) * denominator(s_234))
    result += eps_eps_23 * eps_p_41 * s_34 / (
        denominator(s_23) * denominator(s_234)
    )
    result -= eps_eps_23 * eps_p_45 * s_p12 / (
        denominator(s_23) * denominator(s_4p5)
    )
    result += (
        eps_eps_34 * eps_p_21
        - eps_eps_24 * eps_p_31
        + eps_eps_23 * eps_p_41
    ) / denominator(s_234)
    result += (
        eps_eps_34 * eps_k_23 * s_p14
        - eps_eps_24 * eps_k_32 * s_p14
        + eps_eps_23 * eps_k_42 * s_p14
        - eps_eps_23 * eps_p_41 * s_p12
        - eps_eps_23 * eps_p_45 * s_p12
    ) / (denominator(s_23) * denominator(s_234))

    cubic_34 = (
        eps_p_21 * eps_k_32 * eps_p_45
        + eps_p_25 * eps_p_31 * eps_p_45
        + eps_p_25 * eps_p_31 * eps_k_42
        + eps_p_21 * eps_p_31 * eps_p_45
    )
    cubic_34_swapped = (
        eps_p_25 * eps_k_32 * eps_p_41
        + eps_p_21 * eps_p_35 * eps_p_41
        + eps_p_21 * eps_p_35 * eps_k_42
        + eps_p_25 * eps_p_35 * eps_p_41
    )
    result += 2.0 * (cubic_34 - cubic_34_swapped) / (
        denominator(s_34) * denominator(s_234)
    )

    cubic_23 = (
        eps_k_23 * eps_p_35 * eps_p_41
        + eps_k_32 * eps_p_45 * eps_p_21
    )
    cubic_23_swapped = (
        eps_k_23 * eps_p_31 * eps_p_45
        + eps_k_32 * eps_p_41 * eps_p_25
    )
    result += 2.0 * (cubic_23 - cubic_23_swapped) / (
        denominator(s_23) * denominator(s_234)
    )
    return math.sqrt(2.0) * result


def gauge_five_ordered(
    order: list[int],
    momenta: np.ndarray,
    polarizations: dict[int, np.ndarray],
    epsilon: float,
) -> complex:
    rotated = list(order)
    scalar_start = rotated.index(0)
    rotated = rotated[scalar_start:] + rotated[:scalar_start]
    scalar_end = rotated.index(4)
    alpha = rotated[1:scalar_end]
    beta = rotated[scalar_end + 1 :]
    result = 0.0j
    for shuffle in ordered_shuffles(alpha, list(reversed(beta))):
        result += canonical_gauge_five(
            [momenta[0], *[momenta[index] for index in shuffle], momenta[4]],
            [polarizations[index] for index in shuffle],
            epsilon,
        )
    return ((-1) ** len(beta)) * result


def causal_scalar_klt_four(
    momenta: np.ndarray,
    special: int,
    chirality: int,
    epsilon: float,
) -> complex:
    helicities = {
        index: (
            (-1 if index == special else 1)
            if chirality == 0
            else (1 if index == special else -1)
        )
        for index in (1, 2)
    }
    polarizations = {
        index: polarization(momenta[index], momenta[0], helicities[index])
        for index in (1, 2)
    }
    left = gauge_four_ordered(
        [0, 1, 2, 4], momenta, polarizations, epsilon
    )
    right = gauge_four_ordered(
        [2, 4, 1, 0], momenta, polarizations, epsilon
    )
    kernel = causal(complex(M5017.invariant(momenta, 0, 1)), epsilon)
    return -left * kernel * right


def causal_momentum_kernel(
    alpha_reversed: int,
    beta_reversed: int,
    momenta: np.ndarray,
    epsilon: float,
) -> complex:
    s_21 = complex(M5017.invariant(momenta, 1, 0))
    s_31 = complex(M5017.invariant(momenta, 2, 0))
    s_23 = complex(M5017.invariant(momenta, 1, 2))
    if alpha_reversed == 0 and beta_reversed == 0:
        return causal(s_21, epsilon) * causal(s_31, epsilon)
    if alpha_reversed == 0 and beta_reversed == 1:
        return causal(s_21 + s_23, epsilon) * causal(s_31, epsilon)
    if alpha_reversed == 1 and beta_reversed == 0:
        return causal(s_31 + s_23, epsilon) * causal(s_21, epsilon)
    return causal(s_31, epsilon) * causal(s_21, epsilon)


def causal_scalar_klt_five(
    momenta: np.ndarray,
    special: int,
    chirality: int,
    epsilon: float,
) -> complex:
    helicities = {
        index: (
            (-1 if index == special else 1)
            if chirality == 0
            else (1 if index == special else -1)
        )
        for index in (1, 2, 3)
    }
    polarizations = {
        index: polarization(momenta[index], momenta[0], helicities[index])
        for index in (1, 2, 3)
    }
    result = 0.0j
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left = gauge_five_ordered(
            [0, *sigma, 3, 4], momenta, polarizations, epsilon
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right = gauge_five_ordered(
                [3, 4, *gamma, 0], momenta, polarizations, epsilon
            )
            result += (
                left
                * causal_momentum_kernel(
                    gamma_reversed, sigma_reversed, momenta, epsilon
                )
                * right
            )
    return result


def causal_hhh_reduced_product(
    internal: np.ndarray,
    scattering_cosine: complex,
    left_epsilon: float,
    right_epsilon: float,
) -> complex:
    left, right = M5017.cut_momenta(internal, scattering_cosine, 1.0)
    result = 0.0j
    for special in (1, 2, 3):
        result += causal_scalar_klt_five(
            left, special, 0, left_epsilon
        ) * causal_scalar_klt_five(right, special, 1, right_epsilon)
        result += causal_scalar_klt_five(
            left, special, 1, left_epsilon
        ) * causal_scalar_klt_five(right, special, 0, right_epsilon)
    return result / 6.0


def causal_soft_factor(
    hard_momenta: np.ndarray,
    soft_momentum: np.ndarray,
    chirality: int,
    epsilon: float,
) -> complex:
    helicity = 1 if chirality == 0 else -1
    epsilon_soft = polarization(
        soft_momentum, hard_momenta[0], helicity
    )
    result = 0.0j
    for leg in (0, 1, 2, 4):
        numerator = minkowski(epsilon_soft, hard_momenta[leg]) ** 2
        denominator = causal(
            minkowski(soft_momentum, hard_momenta[leg]), epsilon
        )
        result += numerator / denominator
    return result


def causal_endpoint_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    left_epsilon: float,
    right_epsilon: float,
) -> complex:
    internal = np.zeros((3, 4), dtype=np.complex128)
    internal[0, 0] = 1.0
    internal[0, 1:] = decay_direction
    internal[1, 0] = 1.0
    internal[1, 1:] = -decay_direction
    left, right = M5017.cut_momenta(internal, scattering_cosine, 1.0)
    soft_left = np.empty(4, dtype=np.complex128)
    soft_left[0] = 1.0
    soft_left[1:] = soft_direction
    soft_right = -soft_left
    result = 0.0j
    for special in (1, 2):
        result += (
            causal_soft_factor(left, soft_left, 0, left_epsilon)
            * causal_scalar_klt_four(left, special, 0, left_epsilon)
            * causal_soft_factor(right, soft_right, 1, right_epsilon)
            * causal_scalar_klt_four(right, special, 1, right_epsilon)
        )
        result += (
            causal_soft_factor(left, soft_left, 1, left_epsilon)
            * causal_scalar_klt_four(left, special, 1, left_epsilon)
            * causal_soft_factor(right, soft_right, 0, right_epsilon)
            * causal_scalar_klt_four(right, special, 0, right_epsilon)
        )
    return result / 32.0


def pointwise_checks() -> dict[str, Any]:
    soft_direction = M5017.direction(0.43, 0.18)
    decay_direction = M5017.direction(0.71, 0.59)
    internal = np.zeros((3, 4), dtype=np.complex128)
    internal[0] = np.concatenate(([1.0], decay_direction))
    internal[1] = np.concatenate(([1.0], -decay_direction))
    left, right = M5017.cut_momenta(internal, 0.27, 1.0)
    four_residuals: list[float] = []
    for momenta in (left, right):
        for special in (1, 2):
            for chirality in (0, 1):
                causal_value = causal_scalar_klt_four(
                    momenta, special, chirality, 0.0
                )
                reference = complex(
                    M5017.scalar_klt_four(momenta, special, chirality)
                )
                four_residuals.append(
                    abs(causal_value - reference) / max(abs(reference), 1.0e-30)
                )
    endpoint = causal_endpoint_value(
        soft_direction, decay_direction, 0.27, 0.0, 0.0
    )
    endpoint_reference = complex(
        M5017.exact_hhh_g0(
            soft_direction, decay_direction, 0.27, 1.0
        )
    )
    finite_internal = M5017.sequential_three_body(
        0.37,
        M5017.direction(0.31, 0.73),
        M5017.direction(0.64, 0.27),
    )
    finite_left, finite_right = M5017.cut_momenta(
        finite_internal, 0.27, 1.0
    )
    five_residuals: list[float] = []
    five_ratios: list[complex] = []
    for momenta in (finite_left, finite_right):
        spinors = M5017.spinor_table(momenta)
        for sigma_reversed in range(2):
            sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
            orders = (
                [0, *sigma, 3, 4],
                [3, 4, *sigma, 0],
            )
            for order in orders:
                for special in (1, 2, 3):
                    for chirality in (0, 1):
                        helicities = {
                            index: (
                                (-1 if index == special else 1)
                                if chirality == 0
                                else (1 if index == special else -1)
                            )
                            for index in (1, 2, 3)
                        }
                        polarizations = {
                            index: polarization(
                                momenta[index], momenta[0], helicities[index]
                            )
                            for index in (1, 2, 3)
                        }
                        covariant_value = gauge_five_ordered(
                            order, momenta, polarizations, 0.0
                        )
                        reference_value = complex(
                            M5017.scalar_mhv(
                                np.asarray(order, dtype=np.int64),
                                special,
                                spinors,
                                chirality,
                            )
                        )
                        expected_sign = -1.0 if chirality == 0 else 1.0
                        five_residuals.append(
                            abs(covariant_value - expected_sign * reference_value)
                            / max(abs(reference_value), 1.0e-30)
                        )
                        five_ratios.append(
                            covariant_value / reference_value
                        )
    five_klt_residuals: list[float] = []
    for momenta in (finite_left, finite_right):
        for special in (1, 2, 3):
            for chirality in (0, 1):
                covariant_value = causal_scalar_klt_five(
                    momenta, special, chirality, 0.0
                )
                reference_value = complex(
                    M5017.scalar_klt_five(momenta, special, chirality)
                )
                five_klt_residuals.append(
                    abs(covariant_value - reference_value)
                    / max(abs(reference_value), 1.0e-30)
                )
    full_cut_covariant = causal_hhh_reduced_product(
        finite_internal, 0.27, 0.0, 0.0
    )
    full_cut_reference = complex(
        M5017.hhh_reduced_product(finite_internal, 0.27, 1.0)
    )
    return {
        "maximum_four_point_KLT_relative_residual": max(four_residuals),
        "endpoint_relative_residual": abs(endpoint - endpoint_reference)
        / max(abs(endpoint_reference), 1.0e-30),
        "endpoint_covariant": str(endpoint),
        "endpoint_spinor_reference": str(endpoint_reference),
        "maximum_five_point_gauge_relative_residual": max(five_residuals),
        "five_point_ratio_real_range": [
            min(value.real for value in five_ratios),
            max(value.real for value in five_ratios),
        ],
        "five_point_ratio_imaginary_maximum": max(
            abs(value.imag) for value in five_ratios
        ),
        "maximum_five_point_KLT_relative_residual": max(
            five_klt_residuals
        ),
        "finite_x_hhh_cut_relative_residual": abs(
            full_cut_covariant - full_cut_reference
        )
        / max(abs(full_cut_reference), 1.0e-30),
        "finite_x_hhh_cut_covariant": str(full_cut_covariant),
        "finite_x_hhh_cut_spinor_reference": str(full_cut_reference),
    }


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def endpoint_scan(
    power: int,
    seeds: tuple[int, ...],
    epsilon_values: tuple[float, ...],
    configuration_names: tuple[str, ...],
    prescription_names: tuple[str, ...],
) -> list[dict[str, Any]]:
    mp.mp.dps = 40
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_q1p5", complex(1.5, 0.08)),
        ("crossed_q3", complex(3.0, 0.08)),
    )
    prescriptions = (
        ("same_positive", 1.0, 1.0),
        ("amplitude_conjugate", 1.0, -1.0),
        ("conjugate_amplitude", -1.0, 1.0),
        ("same_negative", -1.0, -1.0),
    )
    configurations = tuple(
        row for row in configurations if row[0] in configuration_names
    )
    prescriptions = tuple(
        row for row in prescriptions if row[0] in prescription_names
    )
    if len(configurations) != len(configuration_names):
        raise ValueError("unknown endpoint configuration")
    if len(prescriptions) != len(prescription_names):
        raise ValueError("unknown causal prescription")
    rows: list[dict[str, Any]] = []
    points = {
        seed: qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    for configuration, scattering_cosine in configurations:
        exact = complex(
            M5019.endpoint_resolvent(
                mp.mpc(scattering_cosine.real, scattering_cosine.imag), 128
            )[2]
        )
        for prescription, left_sign, right_sign in prescriptions:
            for epsilon in epsilon_values:
                seed_means: list[complex] = []
                for seed in seeds:
                    values = [
                        causal_endpoint_value(
                            M5017.direction(point[0], point[1]),
                            M5017.direction(point[2], point[3]),
                            scattering_cosine,
                            left_sign * epsilon,
                            right_sign * epsilon,
                        )
                        for point in points[seed]
                    ]
                    seed_means.append(complex(np.mean(values)))
                mean, real_error, imaginary_error = aggregate(seed_means)
                rows.append(
                    {
                        "configuration": configuration,
                        "scattering_cosine": str(scattering_cosine),
                        "prescription": prescription,
                        "epsilon": epsilon,
                        "mean": str(mean),
                        "RQMC_real_error": real_error,
                        "RQMC_imaginary_error": imaginary_error,
                        "exact_resolvent": str(exact),
                        "relative_residual": abs(mean - exact)
                        / max(abs(exact), 1.0e-30),
                    }
                )
    return rows


def build_verdict(result: dict[str, Any]) -> dict[str, Any]:
    checks = result["pointwise_checks"]
    representation_residuals = (
        checks["maximum_four_point_KLT_relative_residual"],
        checks["endpoint_relative_residual"],
        checks["maximum_five_point_gauge_relative_residual"],
        checks["maximum_five_point_KLT_relative_residual"],
        checks["finite_x_hhh_cut_relative_residual"],
    )
    rows = result.get("endpoint_scan", [])
    physical = sorted(
        (
            row
            for row in rows
            if row["configuration"] == "physical"
            and row["prescription"] == "same_positive"
        ),
        key=lambda row: row["epsilon"],
        reverse=True,
    )
    crossed = [
        row
        for row in rows
        if row["configuration"] == "crossed_q1p5"
    ]
    smallest_physical = physical[-1] if physical else None
    smallest_crossed_epsilon = (
        min(row["epsilon"] for row in crossed) if crossed else None
    )
    smallest_crossed = [
        row
        for row in crossed
        if row["epsilon"] == smallest_crossed_epsilon
    ]
    physical_control_passed = bool(
        smallest_physical
        and abs(
            complex(smallest_physical["mean"])
            - complex(smallest_physical["exact_resolvent"])
        )
        < 3.0e-3
        and all(
            abs(complex(physical[index + 1]["mean"]).imag)
            <= abs(complex(physical[index]["mean"]).imag)
            for index in range(len(physical) - 1)
        )
    )
    crossed_rejected = bool(
        smallest_crossed
        and all(row["relative_residual"] > 0.3 for row in smallest_crossed)
    )
    return {
        "explicit_covariant_four_and_five_point_representation_passed": max(
            representation_residuals
        )
        < 1.0e-9,
        "maximum_pointwise_representation_relative_residual": max(
            representation_residuals
        ),
        "physical_causal_control_passed": physical_control_passed,
        "undeformed_real_sphere_crossed_causal_continuation_rejected": crossed_rejected,
        "smallest_crossed_epsilon": smallest_crossed_epsilon,
        "smallest_epsilon_crossed_relative_residuals": {
            row["prescription"]: row["relative_residual"]
            for row in smallest_crossed
        },
        "full_covariant_finite_x_hhh_integrand_constructed": True,
        "full_coupled_cut_bridge_complete": False,
        "reason": (
            "explicit propagator i0 prescriptions on the undeformed real sphere "
            "converge to the wrong crossed-sheet boundary value; physical-propagator "
            "root tracking and a coupled azimuth/polar contour are still required"
        ),
        "next_target": (
            "classify the nonzero global-azimuth residues by physical propagator, "
            "then transport the coupled azimuth/polar integration cycle"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=5)
    parser.add_argument("--seeds", default="50231,50232")
    parser.add_argument("--epsilons", default="0.03,0.01")
    parser.add_argument(
        "--configurations", default="physical,crossed_q1p5,crossed_q3"
    )
    parser.add_argument(
        "--prescriptions",
        default="same_positive,amplitude_conjugate,conjugate_amplitude,same_negative",
    )
    parser.add_argument("--pointwise-only", action="store_true")
    parser.add_argument("--output")
    arguments = parser.parse_args()
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    epsilon_values = tuple(
        float(value) for value in arguments.epsilons.split(",")
    )
    configuration_names = tuple(arguments.configurations.split(","))
    prescription_names = tuple(arguments.prescriptions.split(","))
    result: dict[str, Any] = {"pointwise_checks": pointwise_checks()}
    if not arguments.pointwise_only:
        result["endpoint_scan"] = endpoint_scan(
            arguments.power,
            seeds,
            epsilon_values,
            configuration_names,
            prescription_names,
        )
    result["verdict"] = build_verdict(result)
    serialized = json.dumps(result, indent=2)
    if arguments.output:
        output = Path(arguments.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
