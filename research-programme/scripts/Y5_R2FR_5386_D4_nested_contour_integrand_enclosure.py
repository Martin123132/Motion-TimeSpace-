from __future__ import annotations

import argparse
import cmath
from contextlib import contextmanager
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Iterator

from mpmath import iv


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
SCRIPT_5385 = (
    SCRIPTS
    / "Y5_R2FR_5385_D4_expanded_energy_contour_full_pole_catalog_clearance.py"
)
SCRIPT_5258 = SCRIPTS / "Y5_R2FR_5258_interval_residue_enclosure_pilot.py"

INTERVAL_DIGITS = 50
ENERGY_PHASE_ARC_COUNT = 32
GLOBAL_PHASE_ARC_COUNT = 64
ENERGY_PATH_SUBDIVISIONS = 32
ENERGY_CONTOUR_RELATIVE_RADIUS = "1e-5"
GLOBAL_CONTOUR_RELATIVE_RADIUS = "1e-7"
CAUCHY_ENDPOINT_HALO_BOXES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5387"
    / "D4_Cauchy_endpoint_halo_boxes.csv"
)


def contour_box_rows(include_endpoint_halo: bool = True) -> list[dict[str, str]]:
    rows = M5385.read_csv(M5385.BOXES_5380)
    if include_endpoint_halo and CAUCHY_ENDPOINT_HALO_BOXES.is_file():
        rows.extend(M5385.read_csv(CAUCHY_ENDPOINT_HALO_BOXES))
    return rows


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5385 = load_module("mts_5385_for_5386", SCRIPT_5385)
M5258 = load_module("mts_5258_for_5386", SCRIPT_5258)


def chart_safe_sqrt(value: Any) -> Any:
    candidates = (
        (1, 1),
        (-1, 1j),
        (1j, cmath.exp(0.25j * math.pi)),
        (-1j, cmath.exp(-0.25j * math.pi)),
    )
    phase, phase_root = max(
        candidates,
        key=lambda item: M5385.M5380.real_lower(item[0] * value),
    )
    rotated = phase * value
    if M5385.M5380.real_lower(rotated) <= 0:
        raise M5258.IntervalSingularity(
            "no closed square-root half-plane chart excludes zero"
        )
    real_part = M5385.M5381.interval_real(rotated)
    imaginary_part = M5385.M5381.interval_imaginary(rotated)
    modulus = abs(rotated)
    real_root = iv.sqrt((modulus + real_part) / 2)
    imaginary_root = imaginary_part / (2 * real_root)
    root = iv.mpc(real_root, imaginary_root) / M5258.cpoint(phase_root)
    principal_midpoint = cmath.sqrt(M5385.M5380.complex_midpoint(value))
    if abs(M5258.midpoint(root) - principal_midpoint) > abs(
        -M5258.midpoint(root) - principal_midpoint
    ):
        root = -root
    return root


def chart_safe_massless_spinors(
    momentum: list[Any],
    diagnostics: Any,
    label: str,
    allow_transverse_chart: bool = True,
) -> tuple[list[Any], list[Any]]:
    energy, momentum_x, momentum_y, momentum_z = momentum
    plus = energy + momentum_z
    minus = energy - momentum_z
    transverse_minus = momentum_x - M5258.cpoint(1j) * momentum_y
    transverse_plus = momentum_x + M5258.cpoint(1j) * momentum_y
    diagonal_lowers = (M5258.lower_abs(plus), M5258.lower_abs(minus))
    if max(diagonal_lowers) > 0 or not allow_transverse_chart:
        chart = "plus" if diagonal_lowers[0] >= diagonal_lowers[1] else "minus"
    else:
        transverse_lowers = (
            M5258.lower_abs(transverse_minus),
            M5258.lower_abs(transverse_plus),
        )
        chart = (
            "transverse_minus"
            if transverse_lowers[0] >= transverse_lowers[1]
            else "transverse_plus"
        )
    selected = {
        "plus": plus,
        "minus": minus,
        "transverse_minus": transverse_minus,
        "transverse_plus": transverse_plus,
    }[chart]
    diagnostics.record(selected, f"{label}:spinor_chart")
    root = chart_safe_sqrt(selected)
    diagnostics.record(root, f"{label}:spinor_root")
    if chart == "plus":
        angle = [
            root,
            M5258.safe_divide(
                transverse_plus, root, diagnostics, f"{label}:angle_plus"
            ),
        ]
        square = [
            root,
            M5258.safe_divide(
                transverse_minus, root, diagnostics, f"{label}:square_plus"
            ),
        ]
    elif chart == "minus":
        angle = [
            M5258.safe_divide(
                transverse_minus, root, diagnostics, f"{label}:angle_minus"
            ),
            root,
        ]
        square = [
            M5258.safe_divide(
                transverse_plus, root, diagnostics, f"{label}:square_minus"
            ),
            root,
        ]
    elif chart == "transverse_minus":
        angle = [
            root,
            M5258.safe_divide(
                minus, root, diagnostics, f"{label}:angle_transverse_minus"
            ),
        ]
        square = [
            M5258.safe_divide(
                plus, root, diagnostics, f"{label}:square_transverse_minus"
            ),
            root,
        ]
    else:
        angle = [
            M5258.safe_divide(
                plus, root, diagnostics, f"{label}:angle_transverse_plus"
            ),
            root,
        ]
        square = [
            root,
            M5258.safe_divide(
                minus, root, diagnostics, f"{label}:square_transverse_plus"
            ),
        ]
    return angle, square


def rational_massless_spinors(
    momentum: list[Any],
    diagnostics: Any,
    label: str,
    allow_transverse_chart: bool = True,
) -> tuple[list[Any], list[Any]]:
    energy, momentum_x, momentum_y, momentum_z = momentum
    plus = energy + momentum_z
    minus = energy - momentum_z
    transverse_plus = momentum_x + 1j * momentum_y
    transverse_minus = momentum_x - 1j * momentum_y
    plus_lower = M5258.lower_abs(plus)
    minus_lower = M5258.lower_abs(minus)
    if max(plus_lower, minus_lower) <= 0:
        raise M5258.IntervalSingularity(
            f"no rational diagonal spinor chart survives: {label}"
        )
    if plus_lower >= minus_lower:
        diagnostics.record(plus, f"{label}:rational_plus_chart")
        return (
            [plus, transverse_plus],
            [
                M5258.cpoint(1),
                M5258.safe_divide(
                    transverse_minus,
                    plus,
                    diagnostics,
                    f"{label}:rational_square_plus",
                ),
            ],
        )
    diagnostics.record(minus, f"{label}:rational_minus_chart")
    return (
        [transverse_minus, minus],
        [
            M5258.safe_divide(
                transverse_plus,
                minus,
                diagnostics,
                f"{label}:rational_square_minus",
            ),
            M5258.cpoint(1),
        ],
    )


def interval_external_complex(target: Any) -> list[list[Any]]:
    one = M5258.cpoint(1)
    zero = M5258.cpoint(0)
    transverse = chart_safe_sqrt(one - target * target)
    return [
        [one, zero, zero, one],
        [one, zero, zero, -one],
        [one, transverse, zero, target],
        [one, -transverse, zero, -target],
    ]


def relative_cosine_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
) -> Any:
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    return (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )


def first_channel_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    active_endpoint: int,
) -> Any:
    dual = M5385.M5381.IntervalDual
    recoil = dual.coerce(recoil)
    relative_cosine = relative_cosine_dual(
        configuration,
        epsilon,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
    )
    first_energy = (
        1
        + recoil * recoil
        - relative_cosine * (1 - recoil * recoil)
    ) / 2
    first_longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    first_momentum_z = (
        first_longitudinal * soft_cosine + recoil * decay_cosine
    )
    channel_factor = (
        first_energy + first_momentum_z
        if active_endpoint == 4
        else first_energy - first_momentum_z
    )
    return -2 * channel_factor


def first_lightcone_factor_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    factor: str,
) -> Any:
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    energy = (
        1
        + recoil * recoil
        - relative_cosine * (1 - recoil * recoil)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
    values = {
        "plus": energy + momentum_z,
        "minus": energy - momentum_z,
        "holomorphic": recoil * decay_sine * relative
        + longitudinal * soft_sine,
        "antiholomorphic": recoil * decay_sine / relative
        + longitudinal * soft_sine,
    }
    return values[factor]


def centered_first_lightcone_factor(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    factor: str,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        return first_lightcone_factor_dual(
            configuration,
            values[0],
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            factor,
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value, M5258.cpoint(1 if index == derivative_index else 0)
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def energy_channel_quotient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    energy_displacement: Any,
    active_endpoint: int,
) -> Any:
    material_recoil = inputs["material_recoil"]
    energy_recoil = M5385.M5381.positive_complex_sqrt(
        material_recoil**2 - energy_displacement
    )
    recoil_displacement = energy_recoil - material_recoil
    derivative_integral = iv.mpc(0)
    for index in range(ENERGY_PATH_SUBDIVISIONS):
        path_parameter = iv.mpf(
            [
                index / ENERGY_PATH_SUBDIVISIONS,
                (index + 1) / ENERGY_PATH_SUBDIVISIONS,
            ]
        )
        path_recoil = material_recoil + path_parameter * recoil_displacement
        recoil_dual = M5385.M5381.IntervalDual(path_recoil, iv.mpc(1))
        channel = first_channel_dual(
            configuration,
            inputs["epsilon"],
            recoil_dual,
            inputs["soft_cosine"],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            active_endpoint,
        )
        derivative_integral += (
            -channel.derivative
            / (2 * path_recoil)
            / ENERGY_PATH_SUBDIVISIONS
        )
    return derivative_integral


def shared_channel_quotient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    energy_displacement: Any,
) -> Any:
    material_recoil = inputs["material_recoil"]
    energy_recoil = M5385.M5381.positive_complex_sqrt(
        material_recoil**2 - energy_displacement
    )
    recoil_displacement = energy_recoil - material_recoil
    derivative_integral = iv.mpc(0)
    for index in range(ENERGY_PATH_SUBDIVISIONS):
        path_parameter = iv.mpf(
            [
                index / ENERGY_PATH_SUBDIVISIONS,
                (index + 1) / ENERGY_PATH_SUBDIVISIONS,
            ]
        )
        path_recoil = material_recoil + path_parameter * recoil_displacement
        recoil_dual = M5385.M5381.IntervalDual(path_recoil, iv.mpc(1))
        relative_cosine = relative_cosine_dual(
            configuration,
            inputs["epsilon"],
            recoil_dual,
            inputs["soft_cosine"],
            inputs["decay_cosine"],
            inputs["decay_sine"],
        )
        channel = (
            2
            * (1 - recoil_dual * recoil_dual)
            * (1 - relative_cosine)
        )
        derivative_integral += (
            -channel.derivative
            / (2 * path_recoil)
            / ENERGY_PATH_SUBDIVISIONS
        )
    return derivative_integral


def hard_pair_diagonal_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    first_chart: str,
    second_chart: str,
) -> Any:
    dual = M5385.M5381.IntervalDual
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    relative_cosine = relative_cosine_dual(
        configuration,
        epsilon,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
    )
    first_energy = (
        1
        + recoil * recoil
        - relative_cosine * (1 - recoil * recoil)
    ) / 2
    first_longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    first_pz = (
        first_longitudinal * soft_cosine + recoil * decay_cosine
    )
    second_energy = (
        1
        + recoil * recoil
        + relative_cosine * (1 - recoil * recoil)
    ) / 2
    second_longitudinal = (
        -relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    second_pz = (
        second_longitudinal * soft_cosine - recoil * decay_cosine
    )
    first_diagonal = (
        first_energy + first_pz
        if first_chart == "plus"
        else first_energy - first_pz
    )
    second_diagonal = (
        second_energy + second_pz
        if second_chart == "plus"
        else second_energy - second_pz
    )
    return first_diagonal * second_diagonal


def centered_hard_pair_diagonal(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    first_chart: str,
    second_chart: str,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    center_value = hard_pair_diagonal_dual(
        configuration,
        centers[0],
        centers[1],
        centers[2],
        inputs["decay_cosine"],
        inputs["decay_sine"],
        first_chart,
        second_chart,
    ).value
    enclosure = center_value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value, iv.mpc(1 if index == derivative_index else 0)
            )
            for index, value in enumerate(domains)
        ]
        value = hard_pair_diagonal_dual(
            configuration,
            dual_domains[0],
            dual_domains[1],
            dual_domains[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            first_chart,
            second_chart,
        )
        enclosure += value.derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def hard_soft_edge_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    unit_circle: Any,
    hard_index: int,
    hard_chart: str,
    soft_chart: str,
    chirality: int,
) -> Any:
    dual = M5385.M5381.IntervalDual
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    unit_circle = dual.coerce(unit_circle)
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    relative_cosine = relative_cosine_dual(
        configuration,
        epsilon,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
    )
    epsilon_dual = dual.coerce(epsilon)
    epsilon_squared = epsilon_dual * epsilon_dual
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon_dual / (64 + epsilon_squared))
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    if hard_index == 1:
        energy = (
            1
            + recoil * recoil
            - relative_cosine * (1 - recoil * recoil)
        ) / 2
        longitudinal = (
            relative_cosine * (1 - recoil) * (1 - recoil)
            - (1 - recoil * recoil)
        ) / 2
        holomorphic = (
            recoil * decay_sine * relative
            + longitudinal * soft_sine
        )
        antiholomorphic = (
            recoil * decay_sine / relative
            + longitudinal * soft_sine
        )
        pz = longitudinal * soft_cosine + recoil * decay_cosine
    elif hard_index == 2:
        energy = (
            1
            + recoil * recoil
            + relative_cosine * (1 - recoil * recoil)
        ) / 2
        longitudinal = (
            -relative_cosine * (1 - recoil) * (1 - recoil)
            - (1 - recoil * recoil)
        ) / 2
        holomorphic = (
            -recoil * decay_sine * relative
            + longitudinal * soft_sine
        )
        antiholomorphic = (
            -recoil * decay_sine / relative
            + longitudinal * soft_sine
        )
        pz = longitudinal * soft_cosine - recoil * decay_cosine
    else:
        raise ValueError(f"unsupported hard index {hard_index}")
    soft_energy = 1 - recoil * recoil
    hard = {
        "plus": -(energy + pz),
        "minus": -(energy - pz),
        "holomorphic": -unit_circle * holomorphic,
        "antiholomorphic": -antiholomorphic / unit_circle,
    }
    soft = {
        "plus": -soft_energy * (1 + soft_cosine),
        "minus": -soft_energy * (1 - soft_cosine),
        "holomorphic": -unit_circle * soft_energy * soft_sine,
        "antiholomorphic": -soft_energy * soft_sine / unit_circle,
    }
    if chirality == 0:
        if (hard_chart, soft_chart) == ("plus", "plus"):
            return (
                hard["plus"] * soft["holomorphic"]
                - hard["holomorphic"] * soft["plus"]
            )
        if (hard_chart, soft_chart) == ("minus", "minus"):
            return (
                hard["antiholomorphic"] * soft["minus"]
                - hard["minus"] * soft["antiholomorphic"]
            )
        if (hard_chart, soft_chart) == ("minus", "plus"):
            return (
                hard["antiholomorphic"] * soft["holomorphic"]
                - hard["minus"] * soft["plus"]
            )
        return (
            hard["plus"] * soft["minus"]
            - hard["holomorphic"] * soft["antiholomorphic"]
        )
    if (hard_chart, soft_chart) == ("plus", "plus"):
        return (
            soft["antiholomorphic"] / soft["plus"]
            - hard["antiholomorphic"] / hard["plus"]
        )
    if (hard_chart, soft_chart) == ("minus", "minus"):
        return (
            hard["holomorphic"] / hard["minus"]
            - soft["holomorphic"] / soft["minus"]
        )
    if (hard_chart, soft_chart) == ("minus", "plus"):
        return (
            hard["holomorphic"]
            * soft["antiholomorphic"]
            / (hard["minus"] * soft["plus"])
            - 1
        )
    return 1 - (
        hard["antiholomorphic"]
        * soft["holomorphic"]
        / (hard["plus"] * soft["minus"])
    )


def centered_hard_soft_edge(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    unit_circle: Any,
    hard_index: int,
    hard_chart: str,
    soft_chart: str,
    chirality: int,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
        unit_circle,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        return hard_soft_edge_dual(
            configuration,
            values[0],
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            values[3],
            hard_index,
            hard_chart,
            soft_chart,
            chirality,
        )

    center_value = evaluate(list(centers)).value
    enclosure = center_value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value, iv.mpc(1 if index == derivative_index else 0)
            )
            for index, value in enumerate(domains)
        ]
        value = evaluate(dual_domains)
        enclosure += value.derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def reciprocal_first_soft_mixed_square_enclosure(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
) -> Any:
    return -(1 + inputs["q_value"])


def first_plus_root_gap(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    energy_displacement: Any,
    label: str,
    use_material_recoil_sheet: bool = False,
) -> Any:
    selected_root = geometry["selected_root"]
    q_value = inputs["q_value"]
    if label == "plus_u" and configuration["role"] == "representative":
        return -(1 + q_value) * selected_root
    if label == "plus_v" and configuration["role"] == "reciprocal":
        return -(1 + q_value) * selected_root / q_value
    companion_label = (
        "plus_v"
        if configuration["role"] == "representative"
        else "plus_u"
    )
    if label != companion_label:
        raise ValueError(f"unsupported first-plus root gap {label}")
    center = M5385.branch_center_gap_certificate(
        configuration,
        inputs,
        gap_sector="g1_companion",
        use_material_recoil_sheet=use_material_recoil_sheet,
    )
    if use_material_recoil_sheet:
        if M5258.upper_abs(energy_displacement) > 0.0:
            raise ValueError(
                "owned material-recoil sheet requires zero energy displacement"
            )
        translated_numerator = center["center_gap_box"]
    else:
        variation = M5385.branch_energy_variation_upper(
            configuration,
            inputs,
            energy_displacement,
            gap_sector="g1_companion",
        )
        translated_numerator = (
            center["center_gap_box"] + variation["energy_variation_box"]
        )
    denominator = geometry["first_factors"][2]
    if configuration["role"] == "representative":
        denominator *= inputs["external_root"]
    return translated_numerator / denominator


def centered_rational_product(
    numerators: tuple[Any, ...], denominators: tuple[Any, ...]
) -> Any | None:
    if any(M5258.lower_abs(value) <= 0 for value in denominators):
        return None

    def product(values: tuple[Any, ...]) -> Any:
        result = M5258.cpoint(1)
        for value in values:
            result *= value
        return result

    numerator_centers = tuple(
        M5258.cpoint(M5258.midpoint(value)) for value in numerators
    )
    denominator_centers = tuple(
        M5258.cpoint(M5258.midpoint(value)) for value in denominators
    )
    result = product(numerator_centers) / product(denominator_centers)
    reciprocals = tuple(M5258.cpoint(1) / value for value in denominators)
    reciprocal_product = product(reciprocals)
    for index, value in enumerate(numerators):
        derivative = product(
            numerators[:index] + numerators[index + 1 :]
        ) * reciprocal_product
        result += derivative * (value - numerator_centers[index])
    full_numerator = product(numerators)
    for index, value in enumerate(denominators):
        derivative = (
            -full_numerator
            * reciprocals[index]
            * reciprocals[index]
            * product(reciprocals[:index] + reciprocals[index + 1 :])
        )
        result += derivative * (value - denominator_centers[index])
    return result


def chart_safe_sqrt_dual(value: Any) -> Any:
    dual_value = M5385.M5381.IntervalDual.coerce(value)
    root = chart_safe_sqrt(dual_value.value)
    return M5385.M5381.IntervalDual(
        root, dual_value.derivative / (2 * root)
    )


def external_first_edge_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
    external_chart: str,
    first_chart: str,
    chirality: int,
) -> Any:
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    global_displacement = dual.coerce(global_displacement)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * chart_safe_sqrt_dual(-q_value)
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    if hard_index == 1:
        first_energy = (
            1
            + recoil * recoil
            - relative_cosine * (1 - recoil * recoil)
        ) / 2
        first_longitudinal = (
            relative_cosine * (1 - recoil) * (1 - recoil)
            - (1 - recoil * recoil)
        ) / 2
        first_holomorphic = (
            recoil * decay_sine * relative
            + first_longitudinal * soft_sine
        )
        first_antiholomorphic = (
            recoil * decay_sine / relative
            + first_longitudinal * soft_sine
        )
        first_pz = (
            first_longitudinal * soft_cosine + recoil * decay_cosine
        )
    elif hard_index == 2:
        first_energy = (
            1
            + recoil * recoil
            + relative_cosine * (1 - recoil * recoil)
        ) / 2
        first_longitudinal = (
            -relative_cosine * (1 - recoil) * (1 - recoil)
            - (1 - recoil * recoil)
        ) / 2
        first_holomorphic = (
            -recoil * decay_sine * relative
            + first_longitudinal * soft_sine
        )
        first_antiholomorphic = (
            -recoil * decay_sine / relative
            + first_longitudinal * soft_sine
        )
        first_pz = (
            first_longitudinal * soft_cosine - recoil * decay_cosine
        )
    else:
        raise ValueError(f"unsupported hard index {hard_index}")
    selected_root = (
        external_root * (1 + soft_cosine) / soft_sine
        if configuration["role"] == "representative"
        else soft_sine / ((1 + soft_cosine) * external_root)
    )
    unit_circle = selected_root + global_displacement
    target = -9 + 1j * epsilon
    transverse = chart_safe_sqrt_dual(1 - target * target)
    if external_endpoint == 0:
        external = {
            "plus": 1 + target,
            "minus": 1 - target,
            "holomorphic": transverse,
            "antiholomorphic": transverse,
        }
    elif external_endpoint == 4:
        external = {
            "plus": 1 - target,
            "minus": 1 + target,
            "holomorphic": -transverse,
            "antiholomorphic": -transverse,
        }
    else:
        raise ValueError(f"unsupported external endpoint {external_endpoint}")
    first = {
        "plus": -(first_energy + first_pz),
        "minus": -(first_energy - first_pz),
        "holomorphic": -unit_circle * first_holomorphic,
        "antiholomorphic": -first_antiholomorphic / unit_circle,
    }
    if chirality == 0:
        if (external_chart, first_chart) == ("plus", "plus"):
            return (
                external["plus"] * first["holomorphic"]
                - external["holomorphic"] * first["plus"]
            )
        if (external_chart, first_chart) == ("minus", "minus"):
            return (
                external["antiholomorphic"] * first["minus"]
                - external["minus"] * first["antiholomorphic"]
            )
        if (external_chart, first_chart) == ("minus", "plus"):
            return (
                external["antiholomorphic"] * first["holomorphic"]
                - external["minus"] * first["plus"]
            )
        return (
            external["plus"] * first["minus"]
            - external["holomorphic"] * first["antiholomorphic"]
        )
    if (external_chart, first_chart) == ("plus", "plus"):
        return (
            first["antiholomorphic"] / first["plus"]
            - external["antiholomorphic"] / external["plus"]
        )
    if (external_chart, first_chart) == ("minus", "minus"):
        return (
            external["holomorphic"] / external["minus"]
            - first["holomorphic"] / first["minus"]
        )
    if (external_chart, first_chart) == ("minus", "plus"):
        return (
            external["holomorphic"]
            * first["antiholomorphic"]
            / (external["minus"] * first["plus"])
            - 1
        )
    return 1 - (
        external["antiholomorphic"]
        * first["holomorphic"]
        / (external["plus"] * first["minus"])
    )


def centered_external_first_edge(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
    external_chart: str,
    first_chart: str,
    chirality: int,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        return external_first_edge_dual(
            configuration,
            values[0],
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            values[3],
            external_endpoint,
            hard_index,
            external_chart,
            first_chart,
            chirality,
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value, iv.mpc(1 if index == derivative_index else 0)
            )
            for index, value in enumerate(domains)
        ]
        value = evaluate(dual_domains)
        enclosure += value.derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def first_plus_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    energy_displacement: Any,
    global_displacement: Any,
    target: Any,
    use_material_recoil_sheet: bool = False,
) -> dict[tuple[frozenset[int], int], Any]:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    external = interval_external_complex(target)
    right = [
        [M5258.cpoint(0) for _ in range(4)] for _ in range(5)
    ]
    right[0] = external[2]
    right[4] = external[3]
    for index in range(3):
        right[index + 1] = M5258.vector_negate(internal[index])
    external_plus = right[0][0] + right[0][3]
    first_plus = right[1][0] + right[1][3]
    external_minus = right[0][0] - right[0][3]
    first_minus = right[1][0] - right[1][3]
    external_holomorphic = right[0][1] + 1j * right[0][2]
    external_antiholomorphic = right[0][1] - 1j * right[0][2]
    first_holomorphic = right[1][1] + 1j * right[1][2]
    first_antiholomorphic = right[1][1] - 1j * right[1][2]
    plus_u_gap = first_plus_root_gap(
        configuration,
        inputs,
        geometry,
        energy_displacement,
        "plus_u",
        use_material_recoil_sheet,
    )
    plus_v_gap = first_plus_root_gap(
        configuration,
        inputs,
        geometry,
        energy_displacement,
        "plus_v",
        use_material_recoil_sheet,
    )
    unit_minus_plus_u = global_displacement - plus_u_gap
    unit_minus_plus_v = global_displacement - plus_v_gap
    plus_u_root = geometry["selected_root"] + plus_u_gap
    plus_v_root = geometry["selected_root"] + plus_v_gap
    angle_candidates: list[Any] = []
    square_candidates: list[Any] = []
    if min(
        M5258.lower_abs(external_plus),
        M5258.lower_abs(first_plus),
    ) > 0:
        external_root = chart_safe_sqrt(external_plus)
        first_root = chart_safe_sqrt(first_plus)
        angle_candidates.extend(
            (
                centered_rational_product(
                    (
                        external_plus,
                        first_holomorphic,
                        unit_minus_plus_u,
                    ),
                    (unit_circle, external_root, first_root),
                ),
                centered_rational_product(
                    (
                        external_holomorphic,
                        first_plus,
                        unit_minus_plus_u,
                    ),
                    (plus_u_root, external_root, first_root),
                ),
            )
        )
        square_candidates.extend(
            (
                centered_rational_product(
                    (
                        -external_antiholomorphic,
                        first_plus,
                        unit_minus_plus_v,
                    ),
                    (unit_circle, external_root, first_root),
                ),
                centered_rational_product(
                    (
                        -external_plus,
                        first_antiholomorphic,
                        unit_minus_plus_v,
                    ),
                    (plus_v_root, external_root, first_root),
                ),
            )
        )
    if min(
        M5258.lower_abs(external_minus),
        M5258.lower_abs(first_minus),
    ) > 0:
        external_root = chart_safe_sqrt(external_minus)
        first_root = chart_safe_sqrt(first_minus)
        angle_candidates.extend(
            (
                centered_rational_product(
                    (
                        external_antiholomorphic,
                        first_minus,
                        unit_minus_plus_u,
                    ),
                    (unit_circle, external_root, first_root),
                ),
                centered_rational_product(
                    (
                        external_minus,
                        first_antiholomorphic,
                        unit_minus_plus_u,
                    ),
                    (plus_u_root, external_root, first_root),
                ),
            )
        )
    external_chart = (
        "plus"
        if M5258.lower_abs(external_plus)
        >= M5258.lower_abs(external_minus)
        else "minus"
    )
    first_chart = (
        "plus"
        if M5258.lower_abs(first_plus) >= M5258.lower_abs(first_minus)
        else "minus"
    )
    if external_chart == "minus" and first_chart == "minus":
        angle_candidates.append(
            centered_rational_product(
                (
                    external_antiholomorphic,
                    first_minus,
                    unit_minus_plus_u,
                ),
                (unit_circle,),
            )
        )
        square_candidates.append(
            centered_rational_product(
                (-external_holomorphic, unit_minus_plus_v),
                (external_minus, plus_v_root),
            )
        )
    elif external_chart == "minus" and first_chart == "plus":
        angle_candidates.append(
            centered_rational_product(
                (
                    external_antiholomorphic,
                    first_holomorphic,
                    unit_minus_plus_u,
                ),
                (unit_circle,),
            )
        )
        square_candidates.append(
            centered_rational_product(
                (-unit_minus_plus_v,),
                (unit_circle,),
            )
        )
    elif external_chart == "plus" and first_chart == "plus":
        angle_candidates.append(
            centered_rational_product(
                (
                    external_plus,
                    first_holomorphic,
                    unit_minus_plus_u,
                ),
                (unit_circle,),
            )
        )
        square_candidates.append(
            centered_rational_product(
                (-external_antiholomorphic, unit_minus_plus_v),
                (unit_circle, external_plus),
            )
        )
        square_candidates.extend(
            (
                centered_rational_product(
                    (
                        -external_minus,
                        first_holomorphic,
                        unit_minus_plus_v,
                    ),
                    (unit_circle, external_root, first_root),
                ),
                centered_rational_product(
                    (
                        -external_holomorphic,
                        first_minus,
                        unit_minus_plus_v,
                    ),
                    (plus_v_root, external_root, first_root),
                ),
            )
        )
    angle_candidates.append(
        centered_external_first_edge(
            configuration,
            inputs,
            geometry,
            global_displacement,
            0,
            1,
            external_chart,
            first_chart,
            0,
        )
    )
    square_candidates.append(
        centered_external_first_edge(
            configuration,
            inputs,
            geometry,
            global_displacement,
            0,
            1,
            external_chart,
            first_chart,
            1,
        )
    )
    angle_reference = angle_candidates[-1]
    square_reference = square_candidates[-1]
    angle_candidates = [
        value for value in angle_candidates if value is not None
    ]
    square_candidates = [
        value for value in square_candidates if value is not None
    ]
    if not angle_candidates or not square_candidates:
        raise M5258.IntervalSingularity(
            "first-plus edge has no nonzero diagonal chart"
        )
    selected: list[Any] = []
    for reference, candidates in (
        (angle_reference, angle_candidates),
        (square_reference, square_candidates),
    ):
        aligned: list[Any] = []
        for candidate in candidates:
            if abs(
                M5258.midpoint(candidate) - M5258.midpoint(reference)
            ) > abs(
                -M5258.midpoint(candidate) - M5258.midpoint(reference)
            ):
                candidate = -candidate
            aligned.append(candidate)
        selected.append(
            max(aligned, key=lambda value: M5258.lower_abs(value))
        )
    FIRST_PLUS_EDGE_PROBES.append(
        {
            "plus_u_gap_lower": M5258.lower_abs(plus_u_gap),
            "plus_v_gap_lower": M5258.lower_abs(plus_v_gap),
            "external_plus_lower": M5258.lower_abs(external_plus),
            "first_plus_lower": M5258.lower_abs(first_plus),
            "external_minus_lower": M5258.lower_abs(external_minus),
            "first_minus_lower": M5258.lower_abs(first_minus),
            "first_holomorphic_lower": M5258.lower_abs(first_holomorphic),
            "first_antiholomorphic_lower": M5258.lower_abs(
                first_antiholomorphic
            ),
            "angle_candidate_bounds": [
                {
                    "lower": M5258.lower_abs(value),
                    "upper": M5258.upper_abs(value),
                }
                for value in angle_candidates
            ],
            "square_candidate_bounds": [
                {
                    "lower": M5258.lower_abs(value),
                    "upper": M5258.upper_abs(value),
                }
                for value in square_candidates
            ],
        }
    )
    return {
        (frozenset((0, 1)), 0): selected[0],
        (frozenset((0, 1)), 1): selected[1],
    }


def first_minus_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    target: Any,
) -> dict[tuple[frozenset[int], int], Any]:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    external = interval_external_complex(target)[3]
    first = M5258.vector_negate(internal[0])

    def chart(momentum: list[Any]) -> str:
        plus = momentum[0] + momentum[3]
        minus = momentum[0] - momentum[3]
        return (
            "plus"
            if M5258.lower_abs(plus) >= M5258.lower_abs(minus)
            else "minus"
        )

    external_chart = chart(external)
    first_chart = chart(first)
    angle_external_first = centered_external_first_edge(
        configuration,
        inputs,
        geometry,
        global_displacement,
        4,
        1,
        external_chart,
        first_chart,
        0,
    )
    square_external_first = centered_external_first_edge(
        configuration,
        inputs,
        geometry,
        global_displacement,
        4,
        1,
        external_chart,
        first_chart,
        1,
    )
    return {
        (frozenset((1, 4)), 0): -angle_external_first,
        (frozenset((1, 4)), 1): -square_external_first,
    }


def second_external_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    target: Any,
) -> dict[tuple[frozenset[int], int], Any]:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    external = interval_external_complex(target)
    second = M5258.vector_negate(internal[1])

    def chart(momentum: list[Any]) -> str:
        plus = momentum[0] + momentum[3]
        minus = momentum[0] - momentum[3]
        return (
            "plus"
            if M5258.lower_abs(plus) >= M5258.lower_abs(minus)
            else "minus"
        )

    second_chart = chart(second)
    overrides: dict[tuple[frozenset[int], int], Any] = {}
    for external_endpoint, external_momentum in (
        (0, external[0]),
        (4, external[3]),
    ):
        external_chart = chart(external_momentum)
        orientation = 1 if external_endpoint == 0 else -1
        for chirality in (0, 1):
            value = centered_external_first_edge(
                configuration,
                inputs,
                geometry,
                global_displacement,
                external_endpoint,
                2,
                external_chart,
                second_chart,
                chirality,
            )
            overrides[(frozenset((external_endpoint, 2)), chirality)] = (
                orientation * value
            )
    return overrides


def left_active_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    active_endpoint: int,
) -> dict[tuple[frozenset[int], int], Any]:
    if active_endpoint not in (0, 4):
        raise ValueError(f"unsupported active endpoint {active_endpoint}")
    first_plus, first_minus, _, _ = geometry["first_factors"]
    one = M5258.cpoint(1)
    return {
        (frozenset((0, 1)), 0): M5258.cpoint(-2) * first_minus,
        (frozenset((0, 1)), 1): one,
        (frozenset((1, 4)), 0): M5258.cpoint(-2) * first_plus,
        (frozenset((1, 4)), 1): one,
    }


def left_first_rational_spinors(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    energy_displacement: Any,
    channel_quotient: Any,
    diagnostics: Any,
) -> tuple[list[Any], list[Any]]:
    unit_circle = geometry["selected_root"] + global_displacement
    first_holomorphic = centered_first_lightcone_factor(
        configuration, inputs, geometry, "holomorphic"
    )
    first_antiholomorphic = centered_first_lightcone_factor(
        configuration, inputs, geometry, "antiholomorphic"
    )
    transverse_plus = unit_circle * first_holomorphic
    transverse_minus = first_antiholomorphic / unit_circle
    active_diagonal = (
        -energy_displacement * channel_quotient / M5258.cpoint(2)
    )
    diagnostics.record(
        active_diagonal, "left_first_rational_spinors:active_diagonal"
    )
    if configuration["role"] == "representative":
        return (
            [transverse_minus, active_diagonal],
            [
                M5258.safe_divide(
                    transverse_plus,
                    active_diagonal,
                    diagnostics,
                    "left_first_rational_spinors:minus_chart",
                ),
                M5258.cpoint(1),
            ],
        )
    return (
        [active_diagonal, transverse_plus],
        [
            M5258.cpoint(1),
            M5258.safe_divide(
                transverse_minus,
                active_diagonal,
                diagnostics,
                "left_first_rational_spinors:plus_chart",
            ),
        ],
    )


def left_soft_rational_spinors(
    geometry: dict[str, Any],
    global_displacement: Any,
    diagnostics: Any,
) -> tuple[
    tuple[list[Any], list[Any]],
    tuple[list[int], list[int]],
    str,
]:
    unit_circle = geometry["selected_root"] + global_displacement
    soft_plus, soft_minus, soft_holomorphic, soft_antiholomorphic = (
        geometry["soft_factors"]
    )
    energy = geometry["energy"]
    plus = energy * soft_plus
    minus = energy * soft_minus
    transverse_plus = energy * unit_circle * soft_holomorphic
    transverse_minus = energy * soft_antiholomorphic / unit_circle
    if M5258.lower_abs(plus) >= M5258.lower_abs(minus):
        diagnostics.record(plus, "left_soft_rational_spinors:plus_chart")
        return (
            (
                [plus, transverse_plus],
                [
                    M5258.cpoint(1),
                    M5258.safe_divide(
                        transverse_minus,
                        plus,
                        diagnostics,
                        "left_soft_rational_spinors:plus_chart",
                    ),
                ],
            ),
            ([0, 1], [0, -1]),
            "plus",
        )
    diagnostics.record(minus, "left_soft_rational_spinors:minus_chart")
    return (
        (
            [transverse_minus, minus],
            [
                M5258.safe_divide(
                    transverse_plus,
                    minus,
                    diagnostics,
                    "left_soft_rational_spinors:minus_chart",
                ),
                M5258.cpoint(1),
            ],
        ),
        ([-1, 0], [1, 0]),
        "minus",
    )


def right_first_custom_gauge_factor(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    diagnostics: Any,
) -> Any:
    unit_circle = geometry["selected_root"] + global_displacement
    if configuration["role"] == "representative":
        default_diagonal = -centered_first_lightcone_factor(
            configuration, inputs, geometry, "plus"
        )
        custom_transverse = centered_first_lightcone_factor(
            configuration, inputs, geometry, "antiholomorphic"
        ) / unit_circle
    else:
        default_diagonal = -centered_first_lightcone_factor(
            configuration, inputs, geometry, "minus"
        )
        custom_transverse = unit_circle * centered_first_lightcone_factor(
            configuration, inputs, geometry, "holomorphic"
        )
    default_root = chart_safe_sqrt(default_diagonal)
    factor = M5258.cpoint(1j) * custom_transverse / default_root
    diagnostics.record(
        default_diagonal, "right_first_custom_gauge:default_diagonal"
    )
    diagnostics.record(factor, "right_first_custom_gauge:factor")
    return factor


def internal_hard_pair_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
) -> dict[tuple[frozenset[int], int], Any]:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    momenta = [
        M5258.vector_negate(internal[index]) for index in (0, 1, 2)
    ]
    charts: list[str] = []
    for index, momentum in enumerate(momenta):
        plus = momentum[0] + momentum[3]
        minus = momentum[0] - momentum[3]
        chart = (
            "plus"
            if M5258.lower_abs(plus) >= M5258.lower_abs(minus)
            else "minus"
        )
        diagonal = plus if chart == "plus" else minus
        charts.append(chart)
    twice_recoil = M5258.cpoint(2) * geometry["recoil"]
    diagonal_product = centered_hard_pair_diagonal(
        configuration,
        inputs,
        geometry,
        charts[0],
        charts[1],
    )
    combined_root = chart_safe_sqrt(diagonal_product)
    angle = centered_rational_product(
        (twice_recoil, combined_root), ()
    )
    square = centered_rational_product(
        (twice_recoil,), (combined_root,)
    )
    if angle is None or square is None:
        raise M5258.IntervalSingularity(
            "hard-pair coherent spinor normalization failed"
        )
    overrides = {
        (frozenset((1, 2)), 0): angle,
        (frozenset((1, 2)), 1): square,
    }
    for hard_position, hard_index, pair in (
        (0, 1, frozenset((1, 3))),
        (1, 2, frozenset((2, 3))),
    ):
        for chirality in (0, 1):
            overrides[(pair, chirality)] = centered_hard_soft_edge(
                configuration,
                inputs,
                geometry,
                unit_circle,
                hard_index,
                charts[hard_position],
                charts[2],
                chirality,
            )
    if (
        configuration["role"] == "reciprocal"
    ):
        overrides[(frozenset((1, 3)), 1)] = (
            reciprocal_first_soft_mixed_square_enclosure(
                configuration, inputs, geometry
            )
        )
    return overrides


ACTIVE_QUOTIENT_PROBES: list[dict[str, Any]] = []
STABLE_EDGE_PROBES: list[dict[str, Any]] = []
FIRST_PLUS_EDGE_PROBES: list[dict[str, Any]] = []


def probing_active_bracket_quotient(
    left_index: int,
    right_index: int,
    selected_spinors: dict[int, list[Any]],
    selected_exponents: dict[int, list[int]],
    unit_circle: Any,
    active_center: Any,
    diagnostics: Any,
    label: str,
) -> Any:
    left = selected_spinors[left_index]
    right = selected_spinors[right_index]
    left_exponents = selected_exponents[left_index]
    right_exponents = selected_exponents[right_index]
    terms = (
        (
            left[0] * right[1],
            left_exponents[0] + right_exponents[1],
        ),
        (
            -left[1] * right[0],
            left_exponents[1] + right_exponents[0],
        ),
    )
    varying = [item for item in terms if item[1] != 0]
    fixed = [item for item in terms if item[1] == 0]
    if len(varying) != 1 or len(fixed) != 1:
        raise M5258.IntervalSingularity(
            f"active spinor factor is not affine Laurent: {label}"
        )
    varying_term, exponent = varying[0]
    fixed_term = fixed[0][0]
    if exponent == 1:
        coefficient = varying_term / unit_circle
        quotient = -fixed_term / active_center
    elif exponent == -1:
        coefficient = varying_term * unit_circle
        quotient = fixed_term / unit_circle
    else:
        raise M5258.IntervalSingularity(
            f"unsupported active Laurent exponent {exponent}: {label}"
        )
    ACTIVE_QUOTIENT_PROBES.append(
        {
            "label": label,
            "left_index": left_index,
            "right_index": right_index,
            "exponent": exponent,
            "varying_term_abs_lower": M5258.lower_abs(varying_term),
            "varying_term_abs_upper": M5258.upper_abs(varying_term),
            "fixed_term_abs_lower": M5258.lower_abs(fixed_term),
            "fixed_term_abs_upper": M5258.upper_abs(fixed_term),
            "coefficient_abs_lower": M5258.lower_abs(coefficient),
            "coefficient_abs_upper": M5258.upper_abs(coefficient),
            "quotient_abs_lower": M5258.lower_abs(quotient),
            "quotient_abs_upper": M5258.upper_abs(quotient),
            "quotient_midpoint_real": M5258.midpoint(quotient).real,
            "quotient_midpoint_imaginary": M5258.midpoint(quotient).imag,
        }
    )
    return quotient


@contextmanager
def amplitude_primitives(probe_active_quotients: bool) -> Iterator[None]:
    original_spinors = M5258.massless_spinors
    original_external = M5258.external_complex
    original_active = M5258.active_bracket_quotient
    M5258.massless_spinors = rational_massless_spinors
    M5258.external_complex = interval_external_complex
    if probe_active_quotients:
        M5258.active_bracket_quotient = probing_active_bracket_quotient
    try:
        yield
    finally:
        M5258.massless_spinors = original_spinors
        M5258.external_complex = original_external
        M5258.active_bracket_quotient = original_active


def centered_rational_pair_edge(
    momenta: list[list[Any]],
    chirality: int,
    left_index: int,
    right_index: int,
) -> Any | None:
    components: list[dict[str, Any]] = []
    charts: list[str] = []
    for index in (left_index, right_index):
        energy, momentum_x, momentum_y, momentum_z = momenta[index]
        component = {
            "plus": energy + momentum_z,
            "minus": energy - momentum_z,
            "holomorphic": momentum_x + 1j * momentum_y,
            "antiholomorphic": momentum_x - 1j * momentum_y,
        }
        components.append(component)
        charts.append(
            "plus"
            if M5258.lower_abs(component["plus"])
            >= M5258.lower_abs(component["minus"])
            else "minus"
        )
    left, right = components
    chart_pair = tuple(charts)
    if chirality == 0:
        if chart_pair == ("plus", "plus"):
            return centered_rational_product(
                (left["plus"], right["holomorphic"]), ()
            ) - centered_rational_product(
                (left["holomorphic"], right["plus"]), ()
            )
        if chart_pair == ("minus", "minus"):
            return centered_rational_product(
                (left["antiholomorphic"], right["minus"]), ()
            ) - centered_rational_product(
                (left["minus"], right["antiholomorphic"]), ()
            )
        if chart_pair == ("minus", "plus"):
            return centered_rational_product(
                (left["antiholomorphic"], right["holomorphic"]), ()
            ) - centered_rational_product(
                (left["minus"], right["plus"]), ()
            )
        return centered_rational_product(
            (left["plus"], right["minus"]), ()
        ) - centered_rational_product(
            (left["holomorphic"], right["antiholomorphic"]), ()
        )
    if chart_pair == ("plus", "plus"):
        first = centered_rational_product(
            (right["antiholomorphic"],), (right["plus"],)
        )
        second = centered_rational_product(
            (left["antiholomorphic"],), (left["plus"],)
        )
        return None if first is None or second is None else first - second
    if chart_pair == ("minus", "minus"):
        first = centered_rational_product(
            (left["holomorphic"],), (left["minus"],)
        )
        second = centered_rational_product(
            (right["holomorphic"],), (right["minus"],)
        )
        return None if first is None or second is None else first - second
    if chart_pair == ("minus", "plus"):
        ratio = centered_rational_product(
            (left["holomorphic"], right["antiholomorphic"]),
            (left["minus"], right["plus"]),
        )
        return None if ratio is None else ratio - M5258.cpoint(1)
    ratio = centered_rational_product(
        (left["antiholomorphic"], right["holomorphic"]),
        (left["plus"], right["minus"]),
    )
    return None if ratio is None else M5258.cpoint(1) - ratio


def stable_spinor_edge(
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    left_index: int,
    right_index: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
) -> Any:
    direct = M5258.spinor_bracket(
        spinors[left_index][chirality],
        spinors[right_index][chirality],
    )
    direct_lower = M5258.lower_abs(direct)
    if direct_lower > 0:
        diagnostics.record(direct, f"{label}:stable_edge")
        return direct
    candidates = [(direct_lower, direct)]
    rational_pair = centered_rational_pair_edge(
        momenta, chirality, left_index, right_index
    )
    if rational_pair is not None:
        candidates.append((M5258.lower_abs(rational_pair), rational_pair))
    edge_key = (frozenset((left_index, right_index)), chirality)
    overridden = None
    if edge_overrides is not None and edge_key in edge_overrides:
        overridden = edge_overrides[edge_key]
        if left_index > right_index:
            overridden = -overridden
        candidates.append((M5258.lower_abs(overridden), overridden))
    rational_bounds: list[dict[str, float]] = []
    left_momentum = momenta[left_index]
    right_momentum = momenta[right_index]
    left_plus = left_momentum[0] + left_momentum[3]
    right_plus = right_momentum[0] + right_momentum[3]
    left_minus = left_momentum[0] - left_momentum[3]
    right_minus = right_momentum[0] - right_momentum[3]
    left_transverse_plus = left_momentum[1] + 1j * left_momentum[2]
    right_transverse_plus = right_momentum[1] + 1j * right_momentum[2]
    left_transverse_minus = left_momentum[1] - 1j * left_momentum[2]
    right_transverse_minus = right_momentum[1] - 1j * right_momentum[2]
    rational_specs = (
        (
            left_plus,
            right_plus,
            (
                left_plus * right_transverse_plus
                - left_transverse_plus * right_plus
                if chirality == 0
                else left_plus * right_transverse_minus
                - left_transverse_minus * right_plus
            ),
        ),
        (
            left_minus,
            right_minus,
            (
                left_transverse_minus * right_minus
                - left_minus * right_transverse_minus
                if chirality == 0
                else left_transverse_plus * right_minus
                - left_minus * right_transverse_plus
            ),
        ),
    )
    for left_diagonal, right_diagonal, numerator in rational_specs:
        if (
            M5258.lower_abs(left_diagonal) <= 0
            or M5258.lower_abs(right_diagonal) <= 0
        ):
            continue
        denominator = chart_safe_sqrt(left_diagonal) * chart_safe_sqrt(
            right_diagonal
        )
        if M5258.lower_abs(denominator) <= 0:
            continue
        rational = numerator / denominator
        if abs(M5258.midpoint(rational) - M5258.midpoint(direct)) > abs(
            -M5258.midpoint(rational) - M5258.midpoint(direct)
        ):
            rational = -rational
        rational_bounds.append(
            {
                "abs_lower": M5258.lower_abs(rational),
                "abs_upper": M5258.upper_abs(rational),
            }
        )
        candidates.append((M5258.lower_abs(rational), rational))
    invariant_value = M5258.invariant(
        momenta, left_index, right_index
    )
    reconstructed = None
    opposite = M5258.spinor_bracket(
        spinors[left_index][1 - chirality],
        spinors[right_index][1 - chirality],
    )
    opposite_key = (
        frozenset((left_index, right_index)),
        1 - chirality,
    )
    if edge_overrides is not None and opposite_key in edge_overrides:
        opposite_override = edge_overrides[opposite_key]
        if left_index > right_index:
            opposite_override = -opposite_override
        if M5258.lower_abs(opposite_override) > M5258.lower_abs(opposite):
            opposite = opposite_override
    if M5258.lower_abs(opposite) > 0:
        pair = frozenset((left_index, right_index))
        invariant_value = (
            invariant_overrides[pair]
            if invariant_overrides is not None
            and pair in invariant_overrides
            else M5258.invariant(momenta, left_index, right_index)
        )
        reconstructed = M5258.safe_divide(
            invariant_value,
            opposite,
            diagnostics,
            f"{label}:opposite_chirality",
        )
        candidates.append((M5258.lower_abs(reconstructed), reconstructed))
    lower, selected = max(candidates, key=lambda item: item[0])
    if M5258.lower_abs(direct) <= 0:
        STABLE_EDGE_PROBES.append(
            {
                "label": label,
                "direct_abs_lower": M5258.lower_abs(direct),
                "direct_abs_upper": M5258.upper_abs(direct),
                "opposite_abs_lower": M5258.lower_abs(opposite),
                "opposite_abs_upper": M5258.upper_abs(opposite),
                "invariant_abs_lower": M5258.lower_abs(invariant_value),
                "invariant_abs_upper": M5258.upper_abs(invariant_value),
                "reconstructed_abs_lower": (
                    M5258.lower_abs(reconstructed)
                    if reconstructed is not None
                    else 0.0
                ),
                "reconstructed_abs_upper": (
                    M5258.upper_abs(reconstructed)
                    if reconstructed is not None
                    else math.inf
                ),
                "rational_bounds": rational_bounds,
                "override_abs_lower": (
                    M5258.lower_abs(overridden)
                    if overridden is not None
                    else 0.0
                ),
                "override_abs_upper": (
                    M5258.upper_abs(overridden)
                    if overridden is not None
                    else math.inf
                ),
            }
        )
    diagnostics.record(selected, f"{label}:stable_edge")
    if lower <= 0:
        raise M5258.IntervalSingularity(
            f"stable spinor edge still reaches zero: {label}"
        )
    return selected


def stable_scalar_mhv(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
) -> Any:
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                spinors[special][chirality],
                spinors[endpoint][chirality],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = M5258.cpoint(1)
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= M5258.cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        denominator = stable_spinor_edge(
            momenta,
            spinors,
            chirality,
            left_index,
            right_index,
            diagnostics,
            f"{label}:edge_{index}_{left_index}_{right_index}",
            invariant_overrides,
            edge_overrides,
        )
        value = M5258.safe_divide(
            value,
            denominator,
            diagnostics,
            f"{label}:parketaylor_edge_{index}_{left_index}_{right_index}",
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value


def stable_regularized_scalar_mhv(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    spinor_exponents: dict[int, tuple[list[int], list[int]]],
    chirality: int,
    unit_circle: Any,
    active_center: Any,
    active_pairs: set[frozenset[int]],
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
) -> tuple[Any, int]:
    selected_spinors = {
        index: spinors[index][chirality] for index in spinors
    }
    selected_exponents = {
        index: spinor_exponents[index][chirality]
        for index in spinor_exponents
    }
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                selected_spinors[special],
                selected_spinors[endpoint],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = M5258.cpoint(1)
    cancelled = 0
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= M5258.cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        if pair in active_pairs:
            denominator = M5258.active_bracket_quotient(
                left_index,
                right_index,
                selected_spinors,
                selected_exponents,
                unit_circle,
                active_center,
                diagnostics,
                f"{label}:active_edge_{index}_{left_index}_{right_index}",
            )
            cancelled += 1
        else:
            denominator = stable_spinor_edge(
                momenta,
                spinors,
                chirality,
                left_index,
                right_index,
                diagnostics,
                f"{label}:edge_{index}_{left_index}_{right_index}",
                invariant_overrides,
                edge_overrides,
            )
        value = M5258.safe_divide(
            value,
            denominator,
            diagnostics,
            f"{label}:parketaylor_edge_{index}_{left_index}_{right_index}",
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value, cancelled


def oriented_regularized_scalar_klt_five(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    hard_index: int,
    active_chirality: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
    spinor_exponent_overrides: (
        dict[int, tuple[list[int], list[int]]] | None
    ) = None,
) -> Any:
    spinors = dict(spinor_overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in spinors:
            spinors[index] = M5258.massless_spinors(
                momenta[index],
                diagnostics,
                f"{label}:p{index}",
                False,
            )
    spinor_exponents = M5258.spinor_exponent_table(
        momenta,
        (0, 1, 2, 3, 4),
        {1, 2, 3},
    )
    spinor_exponents.update(spinor_exponent_overrides or {})
    active_pairs = (
        {
            frozenset((0, 3)),
            frozenset((4, hard_index)),
        }
        if chirality == active_chirality
        else set()
    )
    result = M5258.cpoint(0)
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left, left_cancelled = stable_regularized_scalar_mhv(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:left{sigma_reversed}",
            invariant_overrides,
            edge_overrides,
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right, right_cancelled = stable_regularized_scalar_mhv(
                [3, 4, *gamma, 0],
                special,
                momenta,
                spinors,
                spinor_exponents,
                chirality,
                unit_circle,
                active_center,
                active_pairs,
                diagnostics,
                f"{label}:right{gamma_reversed}",
                invariant_overrides,
                edge_overrides,
            )
            remaining_power = 2 - left_cancelled - right_cancelled
            if remaining_power < 0:
                raise M5258.IntervalSingularity(
                    f"more than two active factors in {label}"
                )
            result += (
                displacement**remaining_power
                * left
                * M5258.momentum_kernel(
                    gamma_reversed,
                    sigma_reversed,
                    momenta,
                )
                * right
            )
    return result


def scalar_klt_five_interval(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
) -> Any:
    spinors = dict(spinor_overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in spinors:
            spinors[index] = M5258.massless_spinors(
                momenta[index],
                diagnostics,
                f"{label}:p{index}",
                False,
            )
    result = M5258.cpoint(0)
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left = stable_scalar_mhv(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            chirality,
            diagnostics,
            f"{label}:left{sigma_reversed}",
            invariant_overrides,
            edge_overrides,
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right = stable_scalar_mhv(
                [3, 4, *gamma, 0],
                special,
                momenta,
                spinors,
                chirality,
                diagnostics,
                f"{label}:right{gamma_reversed}",
                invariant_overrides,
                edge_overrides,
            )
            result += (
                left
                * M5258.momentum_kernel(
                    gamma_reversed,
                    sigma_reversed,
                    momenta,
                )
                * right
            )
    return result


def global_regularized_hhh(
    internal: list[list[Any]],
    target: Any,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    active_chirality: int,
    diagnostics: Any,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
    left_invariant_overrides: dict[frozenset[int], Any] | None = None,
    left_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
    left_spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
    right_spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
    right_spinor_exponent_overrides: (
        dict[int, tuple[list[int], list[int]]] | None
    ) = None,
) -> Any:
    left, right = M5258.cut_momenta(internal, target)
    result = M5258.cpoint(0)
    for special in (1, 2, 3):
        for left_chirality, right_chirality in ((0, 1), (1, 0)):
            left_value = scalar_klt_five_interval(
                left,
                special,
                left_chirality,
                diagnostics,
                f"left_K5:s{special}:c{left_chirality}",
                left_invariant_overrides,
                left_edge_overrides,
                left_spinor_overrides,
            )
            right_value = oriented_regularized_scalar_klt_five(
                right,
                special,
                right_chirality,
                1,
                active_chirality,
                unit_circle,
                active_center,
                displacement,
                diagnostics,
                f"right_K5:s{special}:c{right_chirality}",
                right_invariant_overrides,
                right_edge_overrides,
                right_spinor_overrides,
                right_spinor_exponent_overrides,
            )
            result += left_value * right_value
    return result / M5258.cpoint(6)


def raw_hhh_interval(
    internal: list[list[Any]],
    target: Any,
    diagnostics: Any,
) -> Any:
    left, right = M5258.cut_momenta(internal, target)
    result = M5258.cpoint(0)
    for special in (1, 2, 3):
        for left_chirality, right_chirality in ((0, 1), (1, 0)):
            result += scalar_klt_five_interval(
                left,
                special,
                left_chirality,
                diagnostics,
                f"raw_left_K5:s{special}:c{left_chirality}",
            ) * scalar_klt_five_interval(
                right,
                special,
                right_chirality,
                diagnostics,
                f"raw_right_K5:s{special}:c{right_chirality}",
            )
    return result / M5258.cpoint(6)


def stable_factorized_d_hhh(
    internal: list[list[Any]],
    target: Any,
    hard_index: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    active_chirality: int,
    diagnostics: Any,
    covariant_k4: bool = True,
    active_endpoint: int = 0,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> Any:
    left, right = M5258.cut_momenta(internal, target)
    fixed_references = (
        [M5258.cpoint(1), M5258.cpoint(1), M5258.cpoint(0), M5258.cpoint(0)],
        [M5258.cpoint(1), M5258.cpoint(-1), M5258.cpoint(0), M5258.cpoint(0)],
        [M5258.cpoint(1), M5258.cpoint(0), M5258.cpoint(1), M5258.cpoint(0)],
        [M5258.cpoint(1), M5258.cpoint(0), M5258.cpoint(0), M5258.cpoint(1)],
        [M5258.cpoint(1), M5258.cpoint(0), M5258.cpoint(0), M5258.cpoint(-1)],
    )
    result = M5258.cpoint(0)
    remaining = [index for index in (1, 2, 3) if index != hard_index]
    for special in (1, 2, 3):
        if special == hard_index:
            continue
        special_reduced = 1 if remaining[0] == special else 2
        for chirality in (0, 1):
            helicity_value = M5258.helicity(
                hard_index, special, chirality
            )
            viable_references: list[tuple[float, list[Any]]] = []
            for reference in fixed_references:
                trial_diagnostics = M5258.IntervalDiagnostics()
                try:
                    M5258.polarization(
                        left[hard_index],
                        reference,
                        helicity_value,
                        trial_diagnostics,
                        f"M3_trial:s{special}:c{chirality}",
                    )
                except M5258.IntervalSingularity:
                    continue
                viable_references.append(
                    (
                        trial_diagnostics.minimum_denominator_lower,
                        reference,
                    )
                )
            if not viable_references:
                raise M5258.IntervalSingularity(
                    f"no fixed hard-polarization reference survives: s{special}:c{chirality}"
                )
            fixed_reference = max(viable_references, key=lambda item: item[0])[1]
            hard_polarization = M5258.polarization(
                left[hard_index],
                fixed_reference,
                helicity_value,
                diagnostics,
                f"M3:s{special}:c{chirality}",
            )
            gravity_three = (
                M5258.cpoint(2)
                * M5258.minkowski(
                    hard_polarization, left[active_endpoint]
                )
                ** 2
            )
            if active_endpoint == 0:
                reduced = [
                    M5258.vector_add(left[0], left[hard_index]),
                    left[remaining[0]],
                    left[remaining[1]],
                    [M5258.cpoint(0) for _ in range(4)],
                    left[4],
                ]
            elif active_endpoint == 4:
                reduced = [
                    left[0],
                    left[remaining[0]],
                    left[remaining[1]],
                    [M5258.cpoint(0) for _ in range(4)],
                    M5258.vector_add(left[4], left[hard_index]),
                ]
            else:
                raise ValueError(f"unsupported active endpoint {active_endpoint}")
            reduced_helicities = {
                reduced_index: M5258.helicity(
                    original_index, special, chirality
                )
                for reduced_index, original_index in (
                    (1, remaining[0]),
                    (2, remaining[1]),
                )
            }
            if covariant_k4:
                gravity_four = M5258.covariant_scalar_klt_four(
                    reduced,
                    reduced_helicities,
                    diagnostics,
                    f"K4:s{special}:c{chirality}",
                )
            else:
                gravity_four = M5258.scalar_klt_four(
                    reduced,
                    special_reduced,
                    chirality,
                    diagnostics,
                    f"K4:s{special}:c{chirality}",
                )
            gravity_five = oriented_regularized_scalar_klt_five(
                right,
                special,
                1 - chirality,
                hard_index,
                active_chirality,
                unit_circle,
                active_center,
                displacement,
                diagnostics,
                f"K5:s{special}:c{chirality}",
                right_invariant_overrides,
                right_edge_overrides,
            )
            result += gravity_three * gravity_four * gravity_five
    return result / M5258.cpoint(6)


def lightcone_momentum(factors: tuple[Any, Any, Any, Any]) -> dict[str, Any]:
    return {
        "energy": (factors[0] + factors[1]) / 2,
        "transverse_plus": factors[2],
        "transverse_minus": factors[3],
        "pz": (factors[0] - factors[1]) / 2,
    }


def amplitude_state(geometry: dict[str, Any]) -> list[dict[str, Any]]:
    soft_factors = geometry["soft_factors"]
    soft_energy = geometry["energy"]
    return [
        lightcone_momentum(geometry["first_factors"]),
        lightcone_momentum(geometry["second_factors"]),
        {
            "energy": soft_energy,
            "transverse_plus": soft_energy * soft_factors[2],
            "transverse_minus": soft_energy * soft_factors[3],
            "pz": soft_energy * (soft_factors[0] - soft_factors[1]) / 2,
        },
    ]


def stable_energy_multiplier(
    internal: list[list[Any]],
    diagnostics: Any,
    label: str,
) -> Any:
    first_square = internal[0][0] * internal[0][0]
    second_square = internal[1][0] * internal[1][0]
    soft_square = internal[2][0] * internal[2][0]
    hard_product = first_square * second_square
    denominator = hard_product + soft_square * (
        first_square + second_square
    )
    return M5258.safe_divide(
        M5258.cpoint(3) * hard_product,
        denominator,
        diagnostics,
        label,
    )


def regularized_direct_interval(
    configuration: dict[str, Any],
    geometry: dict[str, Any],
    target: Any,
    global_displacement: Any,
    diagnostics: Any,
    covariant_k4: bool = True,
    active_endpoint: int = 0,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> Any:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    factorized = stable_factorized_d_hhh(
        internal,
        target,
        1,
        unit_circle,
        geometry["selected_root"],
        global_displacement,
        1 if configuration["role"] == "reciprocal" else 0,
        diagnostics,
        covariant_k4,
        active_endpoint,
        right_invariant_overrides,
        right_edge_overrides,
    )
    multiplier = stable_energy_multiplier(
        internal,
        diagnostics,
        "multiplier_common_denominator",
    )
    return (
        geometry["energy"]
        * multiplier
        * factorized
        / M5258.cpoint(M5258.S_VALUE * M5258.S_VALUE)
    )


def nested_regularized_direct_interval(
    configuration: dict[str, Any],
    geometry: dict[str, Any],
    target: Any,
    global_displacement: Any,
    channel_quotient: Any,
    active_endpoint: int,
    diagnostics: Any,
    covariant_k4: bool = True,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> Any:
    channel_regularized = regularized_direct_interval(
        configuration,
        geometry,
        target,
        global_displacement,
        diagnostics,
        covariant_k4,
        active_endpoint,
        right_invariant_overrides,
        right_edge_overrides,
    )
    return M5258.safe_divide(
        channel_regularized,
        channel_quotient,
        diagnostics,
        "energy_channel_quotient",
    )


def global_regularized_direct_interval(
    configuration: dict[str, Any],
    geometry: dict[str, Any],
    target: Any,
    global_displacement: Any,
    diagnostics: Any,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
    left_invariant_overrides: dict[frozenset[int], Any] | None = None,
    left_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
    left_spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
    right_spinor_overrides: (
        dict[int, tuple[list[Any], list[Any]]] | None
    ) = None,
    right_spinor_exponent_overrides: (
        dict[int, tuple[list[int], list[int]]] | None
    ) = None,
) -> Any:
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    regularized_hhh = global_regularized_hhh(
        internal,
        target,
        unit_circle,
        geometry["selected_root"],
        global_displacement,
        1 if configuration["role"] == "reciprocal" else 0,
        diagnostics,
        right_invariant_overrides,
        right_edge_overrides,
        left_invariant_overrides,
        left_edge_overrides,
        left_spinor_overrides,
        right_spinor_overrides,
        right_spinor_exponent_overrides,
    )
    multiplier = stable_energy_multiplier(
        internal,
        diagnostics,
        "global_multiplier_common_denominator",
    )
    return (
        geometry["energy"]
        * multiplier
        * regularized_hhh
        / M5258.cpoint(M5258.S_VALUE * M5258.S_VALUE)
    )


def nested_exact_regularized_direct_interval(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    target: Any,
    energy_displacement: Any,
    global_displacement: Any,
    channel_quotient: Any,
    active_endpoint: int,
    diagnostics: Any,
    right_invariant_overrides: dict[frozenset[int], Any] | None = None,
    right_edge_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> Any:
    internal_indices = frozenset((1, 2, 3))
    exact_right_edge_overrides = dict(right_edge_overrides or {})
    if configuration["event_type"] == "BRANCH_DEATH":
        exact_right_edge_overrides = {
            key: value
            for key, value in exact_right_edge_overrides.items()
            if key[0].isdisjoint((1, 3))
        }
    left_edge_overrides = (
        {
            key: value
            for key, value in exact_right_edge_overrides.items()
            if key[0].issubset(internal_indices)
        }
        if exact_right_edge_overrides
        else None
    )
    if left_edge_overrides is None:
        left_edge_overrides = {}
    left_spinor_overrides = None
    right_spinor_overrides = None
    right_spinor_exponent_overrides = None
    if configuration["event_type"] == "BRANCH_DEATH":
        left_first_spinors = left_first_rational_spinors(
            configuration,
            inputs,
            geometry,
            global_displacement,
            energy_displacement,
            channel_quotient,
            diagnostics,
        )
        (
            left_soft_spinors,
            soft_spinor_exponents,
            soft_spinor_chart,
        ) = left_soft_rational_spinors(
            geometry, global_displacement, diagnostics
        )
        left_spinor_overrides = {
            1: left_first_spinors,
            3: left_soft_spinors,
        }
        imaginary_unit = M5258.cpoint(1j)
        right_spinor_overrides = {
            1: (
                [imaginary_unit * value for value in left_first_spinors[0]],
                [imaginary_unit * value for value in left_first_spinors[1]],
            ),
            3: (
                [imaginary_unit * value for value in left_soft_spinors[0]],
                [imaginary_unit * value for value in left_soft_spinors[1]],
            ),
        }
        unit_circle = geometry["selected_root"] + global_displacement
        first_gauge_factor = right_first_custom_gauge_factor(
            configuration,
            inputs,
            geometry,
            global_displacement,
            diagnostics,
        )
        for key, default_edge in (right_edge_overrides or {}).items():
            pair, chirality = key
            if 1 not in pair or not pair.intersection((0, 4)):
                continue
            exact_right_edge_overrides[key] = (
                default_edge * first_gauge_factor
                if chirality == 0
                else M5258.safe_divide(
                    default_edge,
                    first_gauge_factor,
                    diagnostics,
                    "right_first_external_edge_gauge",
                )
            )
        right_spinor_exponent_overrides = {
            1: (
                ([-1, 0], [1, 0])
                if configuration["role"] == "representative"
                else ([0, 1], [0, -1])
            ),
            3: soft_spinor_exponents,
        }
        first_soft_pair = frozenset((1, 3))
        first_spinor_chart = (
            "minus"
            if configuration["role"] == "representative"
            else "plus"
        )
        for chirality in (0, 1):
            left_first_soft_edge = centered_hard_soft_edge(
                configuration,
                inputs,
                geometry,
                unit_circle,
                1,
                first_spinor_chart,
                soft_spinor_chart,
                chirality,
            )
            if configuration["role"] == "reciprocal" and chirality == 1:
                left_first_soft_edge = (
                    reciprocal_first_soft_mixed_square_enclosure(
                        configuration, inputs, geometry
                    )
                )
            left_edge_overrides[(first_soft_pair, chirality)] = (
                left_first_soft_edge
            )
            exact_right_edge_overrides[(first_soft_pair, chirality)] = (
                -left_first_soft_edge
            )
    left_invariant_overrides = dict(right_invariant_overrides or {})
    left_invariant_overrides[frozenset((active_endpoint, 1))] = (
        energy_displacement * channel_quotient
    )
    return energy_displacement * global_regularized_direct_interval(
        configuration,
        geometry,
        target,
        global_displacement,
        diagnostics,
        right_invariant_overrides,
        exact_right_edge_overrides,
        left_invariant_overrides,
        left_edge_overrides,
        left_spinor_overrides,
        right_spinor_overrides,
        right_spinor_exponent_overrides,
    )


class MixedDual:
    __slots__ = ("value", "relative_derivative", "recoil_derivative", "mixed_derivative")

    def __init__(
        self,
        value: Any,
        relative_derivative: Any = 0,
        recoil_derivative: Any = 0,
        mixed_derivative: Any = 0,
    ) -> None:
        self.value = value
        self.relative_derivative = relative_derivative
        self.recoil_derivative = recoil_derivative
        self.mixed_derivative = mixed_derivative

    @staticmethod
    def coerce(value: Any) -> "MixedDual":
        return value if isinstance(value, MixedDual) else MixedDual(value)

    def __add__(self, other: Any) -> "MixedDual":
        other = self.coerce(other)
        return MixedDual(
            self.value + other.value,
            self.relative_derivative + other.relative_derivative,
            self.recoil_derivative + other.recoil_derivative,
            self.mixed_derivative + other.mixed_derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> "MixedDual":
        return MixedDual(
            -self.value,
            -self.relative_derivative,
            -self.recoil_derivative,
            -self.mixed_derivative,
        )

    def __sub__(self, other: Any) -> "MixedDual":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "MixedDual":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "MixedDual":
        other = self.coerce(other)
        return MixedDual(
            self.value * other.value,
            self.relative_derivative * other.value
            + self.value * other.relative_derivative,
            self.recoil_derivative * other.value
            + self.value * other.recoil_derivative,
            self.mixed_derivative * other.value
            + self.relative_derivative * other.recoil_derivative
            + self.recoil_derivative * other.relative_derivative
            + self.value * other.mixed_derivative,
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "MixedDual":
        inverse = 1 / self.value
        inverse_squared = inverse * inverse
        return MixedDual(
            inverse,
            -self.relative_derivative * inverse_squared,
            -self.recoil_derivative * inverse_squared,
            M5258.cpoint(2)
            * self.relative_derivative
            * self.recoil_derivative
            * inverse_squared
            * inverse
            - self.mixed_derivative * inverse_squared,
        )

    def __truediv__(self, other: Any) -> "MixedDual":
        return self * self.coerce(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "MixedDual":
        return self.coerce(other) * self.reciprocal()


def mixed_positive_sqrt(value: Any) -> MixedDual:
    value = MixedDual.coerce(value)
    root = M5385.M5381.positive_complex_sqrt(value.value)
    first_derivative = 1 / (M5258.cpoint(2) * root)
    second_derivative = -1 / (M5258.cpoint(4) * root * root * root)
    return MixedDual(
        root,
        first_derivative * value.relative_derivative,
        first_derivative * value.recoil_derivative,
        second_derivative
        * value.relative_derivative
        * value.recoil_derivative
        + first_derivative * value.mixed_derivative,
    )


def collision_root_mixed(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    chart: str,
    factor_value_overrides: dict[str, Any] | None = None,
) -> tuple[MixedDual, Any]:
    recoil = MixedDual(recoil, recoil_derivative=M5258.cpoint(1))
    epsilon = MixedDual(epsilon)
    soft_cosine = MixedDual(soft_cosine)
    decay_cosine = MixedDual(decay_cosine)
    decay_sine = MixedDual(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * mixed_positive_sqrt(-q_value)
    soft_sine = mixed_positive_sqrt(
        MixedDual(M5258.cpoint(1)) - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative = MixedDual(
        relative.value,
        relative_derivative=M5258.cpoint(1),
        recoil_derivative=relative.recoil_derivative,
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    recoil_squared = recoil * recoil
    first_energy = (
        1
        + recoil_squared
        - relative_cosine * (1 - recoil_squared)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil_squared)
    ) / 2
    holomorphic = (
        relative * recoil * decay_sine + longitudinal * soft_sine
    )
    antiholomorphic = (
        recoil * decay_sine / relative + longitudinal * soft_sine
    )
    momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
    plus = first_energy + momentum_z
    minus = first_energy - momentum_z
    factors = {
        "plus": plus,
        "minus": minus,
        "holomorphic": holomorphic,
        "antiholomorphic": antiholomorphic,
    }
    for factor_name, factor_value in (factor_value_overrides or {}).items():
        factor = factors[factor_name]
        factors[factor_name] = MixedDual(
            factor_value,
            factor.relative_derivative,
            factor.recoil_derivative,
            factor.mixed_derivative,
        )
    plus = factors["plus"]
    minus = factors["minus"]
    holomorphic = factors["holomorphic"]
    antiholomorphic = factors["antiholomorphic"]
    first_label = configuration["root_labels"][0]
    if first_label == "minus_u" and chart == "primary":
        return -(plus / holomorphic) / external_root, holomorphic.value
    if first_label == "minus_u" and chart == "alternate":
        return -(antiholomorphic / minus) / external_root, minus.value
    if first_label == "minus_v" and chart == "primary":
        return -external_root * (antiholomorphic / plus), plus.value
    if first_label == "minus_v" and chart == "alternate":
        return -external_root * (minus / holomorphic), holomorphic.value
    raise ValueError(f"unsupported collision chart {first_label}:{chart}")


def centered_collision_jacobian(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
) -> tuple[Any, str, float, float]:
    recoil_displacement = geometry["recoil"] - inputs["material_recoil"]
    path_recoil = inputs["material_recoil"] + iv.mpf([0, 1]) * (
        recoil_displacement
    )
    factor_names = ("plus", "minus", "holomorphic", "antiholomorphic")
    parent_geometry = dict(geometry)
    parent_geometry["recoil"] = inputs["material_recoil"]
    path_geometry = dict(geometry)
    path_geometry["recoil"] = path_recoil
    parent_factor_overrides = {
        factor: centered_first_lightcone_factor(
            configuration, inputs, parent_geometry, factor
        )
        for factor in factor_names
    }
    path_factor_overrides = {
        factor: centered_first_lightcone_factor(
            configuration, inputs, path_geometry, factor
        )
        for factor in factor_names
    }
    candidates: list[tuple[float, str, MixedDual, MixedDual]] = []
    for chart in ("primary", "alternate"):
        parent, _ = collision_root_mixed(
            configuration,
            inputs["epsilon"],
            inputs["material_recoil"],
            inputs["soft_cosine"],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            chart,
            parent_factor_overrides,
        )
        path, denominator = collision_root_mixed(
            configuration,
            inputs["epsilon"],
            path_recoil,
            inputs["soft_cosine"],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            chart,
            path_factor_overrides,
        )
        candidates.append(
            (M5258.lower_abs(denominator), chart, parent, path)
        )
    denominator_lower, chart, parent, path = max(
        candidates, key=lambda item: item[0]
    )
    if denominator_lower <= 0:
        raise M5258.IntervalSingularity(
            "collision Jacobian path has no nonzero projective chart"
        )
    enclosure = parent.relative_derivative + (
        path.mixed_derivative * recoil_displacement
    )
    return (
        enclosure,
        chart,
        denominator_lower,
        M5258.upper_abs(path.mixed_derivative),
    )


def energy_contour_geometric_factors(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
) -> dict[str, Any]:
    interval_geometry = M5385.M5381
    relative = {
        "recoil": geometry["recoil"],
        "energy": geometry["energy"],
        "soft_cosine": inputs["soft_cosine"],
        "soft_sine": inputs["soft_sine"],
        "decay_cosine": inputs["decay_cosine"],
        "decay_sine": inputs["decay_sine"],
        "relative_root": geometry["relative"],
    }
    relative_dual = interval_geometry.IntervalDual(
        geometry["relative"], M5258.cpoint(1)
    )
    first_root, second_root, *_ = interval_geometry.reduced_collision_roots(
        relative,
        relative_dual,
        tuple(configuration["root_labels"]),
        inputs["external_root"],
    )
    selected_global_root = geometry["selected_root"]
    (
        collision_jacobian,
        collision_jacobian_chart,
        collision_jacobian_chart_denominator_lower,
        collision_jacobian_recoil_derivative_upper,
    ) = centered_collision_jacobian(configuration, inputs, geometry)
    return {
        "relative_root": geometry["relative"],
        "selected_global_root": selected_global_root,
        "collision_jacobian": collision_jacobian,
        "collision_root_difference": first_root.value - second_root.value,
        "collision_jacobian_chart": collision_jacobian_chart,
        "collision_jacobian_chart_denominator_lower": (
            collision_jacobian_chart_denominator_lower
        ),
        "collision_jacobian_recoil_derivative_upper": (
            collision_jacobian_recoil_derivative_upper
        ),
    }


def cartesian_internal(geometry: dict[str, Any]) -> list[list[complex]]:
    rows: list[list[complex]] = []
    for momentum in amplitude_state(geometry):
        transverse_plus = momentum["transverse_plus"]
        transverse_minus = momentum["transverse_minus"]
        rows.append(
            [
                M5258.midpoint(momentum["energy"]),
                M5258.midpoint(
                    (transverse_plus + transverse_minus) / 2
                ),
                M5258.midpoint(
                    (transverse_plus - transverse_minus) / (2j)
                ),
                M5258.midpoint(momentum["pz"]),
            ]
        )
    return rows


def geometric_smoke(
    event_id: str,
    epsilon_bin_index: int,
    energy_phase_arc_index: int,
    epsilon_subdivision_index: int = 0,
    epsilon_subdivision_count: int = 1,
    energy_phase_arc_count: int = ENERGY_PHASE_ARC_COUNT,
) -> dict[str, Any]:
    iv.dps = INTERVAL_DIGITS
    references, _ = M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {
        row["event_id"]: row for row in M5385.read_csv(M5385.EVENTS_5358)
    }
    source = next(
        row
        for row in contour_box_rows()
        if row["event_id"] == event_id
        and row["epsilon_bin_index"] == str(epsilon_bin_index)
    )
    configuration = M5385.M5380.M5379.M5378.M5359.event_configuration(
        events[event_id], references
    )
    epsilon_real_lower = float(source["epsilon_real_lower"])
    epsilon_real_upper = float(source["epsilon_real_upper"])
    epsilon_step = (
        epsilon_real_upper - epsilon_real_lower
    ) / epsilon_subdivision_count
    epsilon_lower = (
        epsilon_real_lower + epsilon_subdivision_index * epsilon_step
    )
    epsilon_upper = (
        epsilon_real_lower
        + (epsilon_subdivision_index + 1) * epsilon_step
    )
    epsilon = iv.mpc(
        iv.mpf([epsilon_lower, epsilon_upper]),
        iv.mpf(
            [
                source["epsilon_imaginary_lower"],
                source["epsilon_imaginary_upper"],
            ]
        ),
    )
    state_boxes = [
        M5385.M5381.parse_complex_box(text)
        for text in source["complex_Krawczyk_images"].split("|")
    ]
    zero_coordinate = M5385.M5380.mp.mpf(
        events[event_id]["zero_regulator_absolute_soft_cosine"]
    )
    center = M5385.M5380.point_solution(
        configuration,
        0.5 * (epsilon_lower + epsilon_upper),
        zero_coordinate,
    )
    for _ in range(6):
        contraction = M5385.M5380.krawczyk_certificate(
            configuration,
            (epsilon_lower, epsilon_upper),
            state_boxes,
            center,
        )
        if not contraction["passes"]:
            break
        state_boxes = contraction["operator"]
    inputs = M5385.event_inputs(configuration, epsilon, state_boxes)
    energy_phase = (
        2
        * iv.pi
        * iv.mpf(
            [energy_phase_arc_index, energy_phase_arc_index + 1]
        )
        / energy_phase_arc_count
    )
    energy_displacement = iv.mpf(ENERGY_CONTOUR_RELATIVE_RADIUS) * (
        iv.cos(energy_phase) + 1j * iv.sin(energy_phase)
    )
    geometry = M5385.expanded_geometry(
        configuration, inputs, energy_displacement
    )
    factors = energy_contour_geometric_factors(
        configuration, inputs, geometry
    )
    return {
        "event_id": event_id,
        "epsilon_bin_index": epsilon_bin_index,
        "epsilon_subdivision_index": epsilon_subdivision_index,
        "epsilon_subdivision_count": epsilon_subdivision_count,
        "energy_phase_arc_index": energy_phase_arc_index,
        "energy_phase_arc_count": energy_phase_arc_count,
        "relative_root_modulus_lower": M5258.lower_abs(
            factors["relative_root"]
        ),
        "selected_global_root_modulus_lower": M5258.lower_abs(
            factors["selected_global_root"]
        ),
        "collision_jacobian_modulus_lower": M5258.lower_abs(
            factors["collision_jacobian"]
        ),
        "collision_jacobian_chart": factors[
            "collision_jacobian_chart"
        ],
        "collision_jacobian_chart_denominator_lower": factors[
            "collision_jacobian_chart_denominator_lower"
        ],
        "collision_jacobian_recoil_derivative_upper": factors[
            "collision_jacobian_recoil_derivative_upper"
        ],
    }


def smoke(
    event_id: str = "E01",
    epsilon_bin_index: int = 0,
    energy_phase_arc_index: int = 0,
    global_phase_arc_index: int = 0,
    epsilon_subdivision_index: int = 0,
    epsilon_subdivision_count: int = 1,
    energy_phase_arc_count: int = ENERGY_PHASE_ARC_COUNT,
    global_phase_arc_count: int = GLOBAL_PHASE_ARC_COUNT,
    use_physical_center_for_point_witness: bool = False,
) -> dict[str, Any]:
    iv.dps = INTERVAL_DIGITS
    references, _ = M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {
        row["event_id"]: row for row in M5385.read_csv(M5385.EVENTS_5358)
    }
    source = next(
        row
        for row in contour_box_rows()
        if row["event_id"] == event_id
        and row["epsilon_bin_index"] == str(epsilon_bin_index)
    )
    configuration = M5385.M5380.M5379.M5378.M5359.event_configuration(
        events[event_id], references
    )
    epsilon_real_lower = float(source["epsilon_real_lower"])
    epsilon_real_upper = float(source["epsilon_real_upper"])
    epsilon_step = (
        epsilon_real_upper - epsilon_real_lower
    ) / epsilon_subdivision_count
    epsilon_subdivision_lower = (
        epsilon_real_lower + epsilon_subdivision_index * epsilon_step
    )
    epsilon_subdivision_upper = (
        epsilon_real_lower
        + (epsilon_subdivision_index + 1) * epsilon_step
    )
    epsilon = iv.mpc(
        iv.mpf(
            [epsilon_subdivision_lower, epsilon_subdivision_upper]
        ),
        iv.mpf(
            [
                source["epsilon_imaginary_lower"],
                source["epsilon_imaginary_upper"],
            ]
        ),
    )
    state_boxes = [
        M5385.M5381.parse_complex_box(text)
        for text in source["complex_Krawczyk_images"].split("|")
    ]
    zero_coordinate = M5385.M5380.mp.mpf(
        events[event_id]["zero_regulator_absolute_soft_cosine"]
    )
    center = M5385.M5380.point_solution(
        configuration,
        0.5 * (epsilon_subdivision_lower + epsilon_subdivision_upper),
        zero_coordinate,
    )
    for _ in range(6):
        contraction = M5385.M5380.krawczyk_certificate(
            configuration,
            (epsilon_subdivision_lower, epsilon_subdivision_upper),
            state_boxes,
            center,
        )
        if not contraction["passes"]:
            break
        state_boxes = contraction["operator"]
    inputs = M5385.event_inputs(configuration, epsilon, state_boxes)
    energy_phase = (
        2
        * iv.pi
        * iv.mpf(
            [energy_phase_arc_index, energy_phase_arc_index + 1]
        )
        / energy_phase_arc_count
    )
    energy_displacement = iv.mpf(ENERGY_CONTOUR_RELATIVE_RADIUS) * (
        iv.cos(energy_phase) + 1j * iv.sin(energy_phase)
    )
    geometry = M5385.expanded_geometry(
        configuration, inputs, energy_displacement
    )
    global_phase = (
        2
        * iv.pi
        * iv.mpf(
            [global_phase_arc_index, global_phase_arc_index + 1]
        )
        / global_phase_arc_count
    )
    global_radius = float(GLOBAL_CONTOUR_RELATIVE_RADIUS) * max(
        1.0, M5385.M5381.modulus_upper(geometry["selected_root"])
    )
    global_displacement = iv.mpf(str(global_radius)) * (
        iv.cos(global_phase) + 1j * iv.sin(global_phase)
    )
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        amplitude_state(geometry), unit_circle
    )
    target = M5258.cpoint(-9) + 1j * epsilon
    diagnostics = M5258.IntervalDiagnostics()
    active_endpoint = 4 if configuration["role"] == "reciprocal" else 0
    channel_quotient = energy_channel_quotient(
        configuration,
        inputs,
        energy_displacement,
        active_endpoint,
    )
    shared_quotient = None
    right_invariant_overrides = None
    if configuration["surface_id"] == "direct:shared:s13":
        shared_quotient = shared_channel_quotient(
            configuration,
            inputs,
            energy_displacement,
        )
        right_invariant_overrides = {
            frozenset((1, 3)): energy_displacement * shared_quotient
        }
    right_edge_overrides = None
    FIRST_PLUS_EDGE_PROBES.clear()
    if configuration["event_type"] == "BRANCH_DEATH":
        right_edge_overrides = first_plus_edge_overrides(
            configuration,
            inputs,
            geometry,
            energy_displacement,
            global_displacement,
            target,
        )
        right_edge_overrides.update(
            first_minus_edge_overrides(
                configuration,
                inputs,
                geometry,
                global_displacement,
                target,
            )
        )
        right_edge_overrides.update(
            internal_hard_pair_edge_overrides(
                configuration,
                inputs,
                geometry,
                global_displacement,
            )
        )
        right_edge_overrides.update(
            second_external_edge_overrides(
                configuration,
                inputs,
                geometry,
                global_displacement,
                target,
            )
        )
    ACTIVE_QUOTIENT_PROBES.clear()
    STABLE_EDGE_PROBES.clear()
    error = ""
    value = None
    value_upper = math.inf
    event_integrand_upper = math.inf
    geometric_factor_lowers = {
        "relative_root": 0.0,
        "selected_global_root": 0.0,
        "collision_jacobian": 0.0,
    }
    collision_root_difference_upper = math.inf
    geometric_path_diagnostics = {
        "collision_jacobian_chart": "UNSET",
        "collision_jacobian_chart_denominator_lower": 0.0,
        "collision_jacobian_recoil_derivative_upper": math.inf,
    }
    point_witness_values = (
        center
        if use_physical_center_for_point_witness
        else [M5385.complex_midpoint_box(value) for value in state_boxes]
    )
    point_state_values = (
        [M5385.M5380.complex_point(value) for value in center]
        if use_physical_center_for_point_witness
        else point_witness_values
    )
    point_witness_is_in_state_boxes = all(
        M5258.real_bounds(box)[0]
        <= complex(point_value).real
        <= M5258.real_bounds(box)[1]
        and M5258.imaginary_bounds(box)[0]
        <= complex(point_value).imag
        <= M5258.imaginary_bounds(box)[1]
        for point_value, box in zip(point_witness_values, state_boxes, strict=True)
    )
    point_inputs = M5385.event_inputs(
        configuration,
        M5385.complex_midpoint_box(epsilon),
        point_state_values,
    )
    point_geometry = M5385.expanded_geometry(
        configuration,
        point_inputs,
        M5385.complex_midpoint_box(energy_displacement),
    )
    point_energy_displacement = M5385.complex_midpoint_box(
        energy_displacement
    )
    point_channel_quotient = energy_channel_quotient(
        configuration,
        point_inputs,
        point_energy_displacement,
        active_endpoint,
    )
    point_right_invariant_overrides = None
    if configuration["surface_id"] == "direct:shared:s13":
        point_shared_quotient = shared_channel_quotient(
            configuration,
            point_inputs,
            point_energy_displacement,
        )
        point_right_invariant_overrides = {
            frozenset((1, 3)): (
                point_energy_displacement * point_shared_quotient
            )
        }
    point_right_edge_overrides = None
    point_internal = M5258.rotate_internal_lightcone(
        amplitude_state(point_geometry), point_geometry["selected_root"]
    )
    point_target = (
        M5258.cpoint(-9)
        + 1j * M5385.complex_midpoint_box(epsilon)
    )
    active_brackets: dict[str, float] = {}
    candidate_active_minima: dict[str, list[dict[str, Any]]] = {}
    factorization_relative_error = math.inf
    factorization_interval_midpoint = complex(math.nan, math.nan)
    factorization_scalar_k4_midpoint = complex(math.nan, math.nan)
    factorization_parent_value = complex(math.nan, math.nan)
    scalar_k4_relative_error = math.inf
    global_regularization_relative_error = math.inf
    global_regularization_midpoint = complex(math.nan, math.nan)
    internal_global_regularization_relative_error = math.inf
    raw_hhh_parent_relative_error = math.inf
    parent_value_is_in_global_interval = False
    global_interval_relative_width = math.inf
    parent_value_is_in_nested_interval = False
    nested_interval_relative_width = math.inf
    nested_real_bounds = (math.nan, math.nan)
    nested_imaginary_bounds = (math.nan, math.nan)
    with amplitude_primitives(probe_active_quotients=True):
        _, point_right = M5258.cut_momenta(point_internal, point_target)
        point_spinors = M5258.spinor_table(
            point_right,
            (0, 1, 2, 3, 4),
            M5258.IntervalDiagnostics(),
            "point_active",
            False,
        )
        for external_index in (0, 4):
            for internal_index in (1, 2, 3):
                for chirality in (0, 1):
                    bracket = M5258.spinor_bracket(
                        point_spinors[external_index][chirality],
                        point_spinors[internal_index][chirality],
                    )
                    active_brackets[
                        f"p{external_index}_p{internal_index}_chirality_{chirality}"
                    ] = M5258.upper_abs(bracket)
        for left_index, right_index in ((1, 2), (1, 3), (2, 3)):
            for chirality in (0, 1):
                bracket = M5258.spinor_bracket(
                    point_spinors[left_index][chirality],
                    point_spinors[right_index][chirality],
                )
                active_brackets[
                    f"p{left_index}_p{right_index}_chirality_{chirality}"
                ] = M5258.upper_abs(bracket)
        active_center = point_geometry["selected_root"]
        candidate_units = {
            "z": active_center,
            "minus_z": -active_center,
            "inverse_z": 1 / active_center,
            "minus_inverse_z": -1 / active_center,
            "i_z": 1j * active_center,
            "minus_i_z": -1j * active_center,
            "i_inverse_z": 1j / active_center,
            "minus_i_inverse_z": -1j / active_center,
        }
        for candidate_label, candidate_unit in candidate_units.items():
            candidate_internal = M5258.rotate_internal_lightcone(
                amplitude_state(point_geometry), candidate_unit
            )
            _, candidate_right = M5258.cut_momenta(
                candidate_internal, point_target
            )
            candidate_spinors = M5258.spinor_table(
                candidate_right,
                (0, 1, 2, 3, 4),
                M5258.IntervalDiagnostics(),
                f"candidate_{candidate_label}",
                False,
            )
            candidate_values: list[dict[str, Any]] = []
            for left_index in range(5):
                for right_index in range(left_index + 1, 5):
                    for chirality in (0, 1):
                        bracket = M5258.spinor_bracket(
                            candidate_spinors[left_index][chirality],
                            candidate_spinors[right_index][chirality],
                        )
                        candidate_values.append(
                            {
                                "pair": f"p{left_index}_p{right_index}",
                                "chirality": chirality,
                                "abs_upper": M5258.upper_abs(bracket),
                            }
                        )
            candidate_active_minima[candidate_label] = sorted(
                candidate_values, key=lambda row: row["abs_upper"]
            )[:4]
        try:
            value = nested_exact_regularized_direct_interval(
                configuration,
                inputs,
                geometry,
                target,
                energy_displacement,
                global_displacement,
                channel_quotient,
                active_endpoint,
                diagnostics,
                right_invariant_overrides,
                right_edge_overrides,
            )
            value_upper = M5258.upper_abs(value)
            geometric_factors = energy_contour_geometric_factors(
                configuration, inputs, geometry
            )
            geometric_path_diagnostics = {
                key: geometric_factors[key]
                for key in geometric_path_diagnostics
            }
            event_integrand = value
            for factor_name in (
                "relative_root",
                "selected_global_root",
                "collision_jacobian",
            ):
                factor = geometric_factors[factor_name]
                geometric_factor_lowers[factor_name] = M5258.lower_abs(
                    factor
                )
                event_integrand = M5258.safe_divide(
                    event_integrand,
                    factor,
                    diagnostics,
                    f"event_geometric_factor:{factor_name}",
                )
            event_integrand_upper = M5258.upper_abs(event_integrand)
            collision_root_difference_upper = M5258.upper_abs(
                geometric_factors["collision_root_difference"]
            )
        except Exception as caught:
            error = f"{type(caught).__name__}: {caught}"
        point_global_displacement_value = global_radius * cmath.exp(
            2j
            * math.pi
            * (global_phase_arc_index + 0.5)
            / global_phase_arc_count
        )
        point_global_displacement = M5258.cpoint(
            point_global_displacement_value
        )
        point_diagnostics = M5258.IntervalDiagnostics()
        point_regularized = nested_regularized_direct_interval(
            configuration,
            point_geometry,
            point_target,
            point_global_displacement,
            point_channel_quotient,
            active_endpoint,
            point_diagnostics,
            right_invariant_overrides=point_right_invariant_overrides,
            right_edge_overrides=point_right_edge_overrides,
        )
        scalar_point_regularized = nested_regularized_direct_interval(
            configuration,
            point_geometry,
            point_target,
            point_global_displacement,
            point_channel_quotient,
            active_endpoint,
            M5258.IntervalDiagnostics(),
            covariant_k4=False,
            right_invariant_overrides=point_right_invariant_overrides,
            right_edge_overrides=point_right_edge_overrides,
        )
        global_point_regularized = global_regularized_direct_interval(
            configuration,
            point_geometry,
            point_target,
            point_global_displacement,
            M5258.IntervalDiagnostics(),
        )
        point_unit_circle = (
            point_geometry["selected_root"] + point_global_displacement
        )
        point_rotated_internal = M5258.rotate_internal_lightcone(
            amplitude_state(point_geometry), point_unit_circle
        )
        point_regularized_hhh = global_regularized_hhh(
            point_rotated_internal,
            point_target,
            point_unit_circle,
            point_geometry["selected_root"],
            point_global_displacement,
            1 if configuration["role"] == "reciprocal" else 0,
            M5258.IntervalDiagnostics(),
        )
        point_raw_hhh = raw_hhh_interval(
            point_rotated_internal,
            point_target,
            M5258.IntervalDiagnostics(),
        )
        point_raw_regularized_hhh = (
            point_raw_hhh * point_global_displacement**2
        )
        internal_global_regularization_relative_error = abs(
            M5258.midpoint(point_regularized_hhh)
            - M5258.midpoint(point_raw_regularized_hhh)
        ) / max(abs(M5258.midpoint(point_raw_regularized_hhh)), 1.0e-300)
        parent_rotated_internal = (
            M5385.M5383.M5378.AMP.rotate_internal(
                M5385.M5383.M5378.AMP.mp_matrix(
                    cartesian_internal(point_geometry)
                ),
                M5258.midpoint(point_unit_circle),
            )
        )
        parent_hhh = complex(
            M5385.M5383.M5378.AMP.hhh_reduced_product(
                parent_rotated_internal,
                M5258.midpoint(point_target),
            )
        )
        raw_hhh_parent_relative_error = abs(
            M5258.midpoint(point_raw_hhh) - parent_hhh
        ) / max(abs(parent_hhh), 1.0e-300)
        soft_cosine = M5258.midpoint(point_inputs["soft_cosine"])
        soft_sine = M5258.midpoint(point_inputs["soft_sine"])
        decay_cosine = M5258.midpoint(point_inputs["decay_cosine"])
        decay_sine = M5258.midpoint(point_inputs["decay_sine"])
        relative = M5258.midpoint(point_geometry["relative"])
        soft_direction = [soft_sine, 0j, soft_cosine]
        decay_direction = [
            decay_sine * (relative + 1 / relative) / 2,
            decay_sine * (relative - 1 / relative) / (2j),
            decay_cosine,
        ]
        parent_direct, _ = (
            M5385.M5383.M5378.complex_finite_plus_components(
                cartesian_internal(point_geometry),
                M5258.midpoint(point_geometry["energy"]),
                soft_direction,
                decay_direction,
                M5258.midpoint(point_target),
                M5258.midpoint(point_geometry["selected_root"])
                + point_global_displacement_value,
            )
        )
        parent_global_regularized = complex(parent_direct) * (
            point_global_displacement_value**2
        )
        parent_regularized = parent_global_regularized * M5258.midpoint(
            point_energy_displacement
        )
        if value is not None:
            nested_real_bounds = M5258.real_bounds(value)
            nested_imaginary_bounds = M5258.imaginary_bounds(value)
            parent_value_is_in_nested_interval = (
                nested_real_bounds[0]
                <= parent_regularized.real
                <= nested_real_bounds[1]
                and nested_imaginary_bounds[0]
                <= parent_regularized.imag
                <= nested_imaginary_bounds[1]
            )
            nested_interval_relative_width = max(
                nested_real_bounds[1] - nested_real_bounds[0],
                nested_imaginary_bounds[1] - nested_imaginary_bounds[0],
            ) / max(abs(parent_regularized), 1.0e-300)
        global_real_bounds = M5258.real_bounds(global_point_regularized)
        global_imaginary_bounds = M5258.imaginary_bounds(
            global_point_regularized
        )
        parent_value_is_in_global_interval = (
            global_real_bounds[0]
            <= parent_global_regularized.real
            <= global_real_bounds[1]
            and global_imaginary_bounds[0]
            <= parent_global_regularized.imag
            <= global_imaginary_bounds[1]
        )
        global_interval_relative_width = max(
            global_real_bounds[1] - global_real_bounds[0],
            global_imaginary_bounds[1] - global_imaginary_bounds[0],
        ) / max(abs(parent_global_regularized), 1.0e-300)
        interval_midpoint = M5258.midpoint(point_regularized)
        factorization_interval_midpoint = interval_midpoint
        factorization_scalar_k4_midpoint = M5258.midpoint(
            scalar_point_regularized
        )
        global_regularization_midpoint = M5258.midpoint(
            global_point_regularized
        )
        factorization_parent_value = parent_regularized
        factorization_relative_error = abs(
            interval_midpoint - parent_regularized
        ) / max(abs(parent_regularized), 1.0e-300)
        scalar_k4_relative_error = abs(
            factorization_scalar_k4_midpoint - parent_regularized
        ) / max(abs(parent_regularized), 1.0e-300)
        global_regularization_relative_error = abs(
            global_regularization_midpoint - parent_global_regularized
        ) / max(abs(parent_global_regularized), 1.0e-300)
    return {
        "event_id": event_id,
        "epsilon_bin_index": epsilon_bin_index,
        "epsilon_subdivision_index": epsilon_subdivision_index,
        "epsilon_subdivision_count": epsilon_subdivision_count,
        "energy_phase_arc_index": energy_phase_arc_index,
        "energy_phase_arc_count": energy_phase_arc_count,
        "global_phase_arc_index": global_phase_arc_index,
        "global_phase_arc_count": global_phase_arc_count,
        "global_contour_radius": global_radius,
        "value_abs_upper": value_upper,
        "event_integrand_abs_upper_without_physical_multiplier": (
            event_integrand_upper
        ),
        "geometric_factor_modulus_lowers": geometric_factor_lowers,
        "collision_root_difference_modulus_upper": (
            collision_root_difference_upper
        ),
        "geometric_path_diagnostics": geometric_path_diagnostics,
        "minimum_denominator_lower": diagnostics.minimum_denominator_lower,
        "energy_channel_quotient_abs_lower": M5258.lower_abs(
            channel_quotient
        ),
        "shared_channel_quotient_abs_lower": (
            M5258.lower_abs(shared_quotient)
            if shared_quotient is not None
            else None
        ),
        "error": error,
        "point_active_bracket_abs": active_brackets,
        "candidate_active_minima": candidate_active_minima,
        "active_quotient_probes": ACTIVE_QUOTIENT_PROBES,
        "stable_edge_probes": STABLE_EDGE_PROBES,
        "first_plus_edge_probes": FIRST_PLUS_EDGE_PROBES,
        "right_edge_override_bounds": (
            {
                f"{'_'.join(str(index) for index in sorted(pair))}_c{chirality}": {
                    "lower": M5258.lower_abs(value),
                    "upper": M5258.upper_abs(value),
                }
                for (pair, chirality), value in right_edge_overrides.items()
            }
            if right_edge_overrides is not None
            else {}
        ),
        "left_active_edge_override_bounds": {
            f"c{chirality}": {
                "lower": M5258.lower_abs(value),
                "upper": M5258.upper_abs(value),
            }
            for (_, chirality), value in left_active_edge_overrides(
                configuration,
                inputs,
                geometry,
                global_displacement,
                active_endpoint,
            ).items()
        },
        "left_active_invariant_abs_lower": M5258.lower_abs(
            energy_displacement * channel_quotient
        ),
        "factorization_relative_error": factorization_relative_error,
        "factorization_interval_midpoint_real": factorization_interval_midpoint.real,
        "factorization_interval_midpoint_imaginary": factorization_interval_midpoint.imag,
        "factorization_scalar_k4_midpoint_real": factorization_scalar_k4_midpoint.real,
        "factorization_scalar_k4_midpoint_imaginary": factorization_scalar_k4_midpoint.imag,
        "factorization_parent_value_real": factorization_parent_value.real,
        "factorization_parent_value_imaginary": factorization_parent_value.imag,
        "scalar_k4_relative_error": scalar_k4_relative_error,
        "global_regularization_midpoint_real": global_regularization_midpoint.real,
        "global_regularization_midpoint_imaginary": global_regularization_midpoint.imag,
        "global_regularization_relative_error": global_regularization_relative_error,
        "internal_global_regularization_relative_error": internal_global_regularization_relative_error,
        "raw_hhh_parent_relative_error": raw_hhh_parent_relative_error,
        "parent_value_is_in_global_interval": parent_value_is_in_global_interval,
        "global_interval_relative_width": global_interval_relative_width,
        "nested_real_lower": nested_real_bounds[0],
        "nested_real_upper": nested_real_bounds[1],
        "nested_imaginary_lower": nested_imaginary_bounds[0],
        "nested_imaginary_upper": nested_imaginary_bounds[1],
        "parent_value_is_in_nested_interval": parent_value_is_in_nested_interval,
        "nested_interval_relative_width": nested_interval_relative_width,
        "point_witness_mode": (
            "physical_event_center_solution"
            if use_physical_center_for_point_witness
            else "state_box_midpoint"
        ),
        "point_witness_is_in_state_boxes": point_witness_is_in_state_boxes,
        "smoke_passes": error == ""
        and math.isfinite(value_upper)
        and parent_value_is_in_nested_interval
        and point_witness_is_in_state_boxes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--matrix-smoke", action="store_true")
    parser.add_argument("--event", default="E01")
    parser.add_argument("--epsilon-bin", type=int, default=0)
    parser.add_argument("--energy-arc", type=int, default=0)
    parser.add_argument("--global-arc", type=int, default=0)
    parser.add_argument("--epsilon-subdivision", type=int, default=0)
    parser.add_argument("--epsilon-subdivisions", type=int, default=1)
    parser.add_argument(
        "--energy-arcs", type=int, default=ENERGY_PHASE_ARC_COUNT
    )
    parser.add_argument(
        "--global-arcs", type=int, default=GLOBAL_PHASE_ARC_COUNT
    )
    arguments = parser.parse_args()
    if arguments.matrix_smoke:
        rows = [smoke(event_id) for event_id in M5385.EVENT_IDS]
        result = {
            "rows": [
                {
                    "event_id": row["event_id"],
                    "role": "reciprocal"
                    if row["event_id"] in {"E01", "E04", "E07", "E08"}
                    else "representative",
                    "error": row["error"],
                    "value_abs_upper": row["value_abs_upper"],
                    "minimum_denominator_lower": row[
                        "minimum_denominator_lower"
                    ],
                    "energy_channel_quotient_abs_lower": row[
                        "energy_channel_quotient_abs_lower"
                    ],
                    "factorization_relative_error": row[
                        "factorization_relative_error"
                    ],
                    "smoke_passes": row["smoke_passes"],
                }
                for row in rows
            ],
            "matrix_smoke_passes": all(
                row["error"] == "" and math.isfinite(row["value_abs_upper"])
                for row in rows
            ),
        }
    elif arguments.smoke:
        result = smoke(
            arguments.event,
            arguments.epsilon_bin,
            arguments.energy_arc,
            arguments.global_arc,
            arguments.epsilon_subdivision,
            arguments.epsilon_subdivisions,
            arguments.energy_arcs,
            arguments.global_arcs,
        )
    else:
        parser.error("5386 currently requires --smoke or --matrix-smoke")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get(
        "matrix_smoke_passes", result.get("smoke_passes", False)
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
