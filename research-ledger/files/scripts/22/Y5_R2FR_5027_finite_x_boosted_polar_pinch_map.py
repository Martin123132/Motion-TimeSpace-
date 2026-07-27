from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5026 = (
    POST
    / "scripts"
    / "Y5_R2FR_5026_finite_x_global_pole_transport_smoke.py"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5026 = load_module("mts_5026_for_5027", SCRIPT_5026)
M5017 = M5026.M5017


def boost_coefficients(
    soft_energy: float,
) -> tuple[complex, complex, complex, complex]:
    recoil_root = np.sqrt(1.0 - soft_energy + 0.0j)
    beta = soft_energy / (2.0 - soft_energy)
    gamma = (2.0 - soft_energy) / (2.0 * recoil_root)
    gamma_beta = soft_energy / (2.0 * recoil_root)
    return recoil_root, beta, gamma, gamma_beta


def complex_sequential_three_body(
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
) -> np.ndarray:
    recoil_root, beta, gamma, gamma_beta = boost_coefficients(
        soft_energy
    )
    relative_cosine = sum(
        soft_direction[index] * decay_direction[index]
        for index in range(3)
    )
    internal = np.empty((3, 4), dtype=np.complex128)
    for internal_index, sign in enumerate((1.0, -1.0)):
        internal[internal_index, 0] = (
            gamma
            * recoil_root
            * (1.0 - sign * beta * relative_cosine)
        )
        internal[internal_index, 1:] = recoil_root * (
            sign * decay_direction
            + (
                sign * (gamma - 1.0) * relative_cosine
                - gamma_beta
            )
            * soft_direction
        )
    internal[2, 0] = soft_energy
    internal[2, 1:] = soft_energy * soft_direction
    return internal


def boosted_hard_cosine(
    soft_energy: float,
    soft_cosine: complex,
    decay_cosine: complex,
    relative_cosine: complex,
    sign: int,
) -> complex:
    _, beta, gamma, gamma_beta = boost_coefficients(soft_energy)
    return complex(
        (
            sign * decay_cosine
            + (
                sign * (gamma - 1.0) * relative_cosine
                - gamma_beta
            )
            * soft_cosine
        )
        / (gamma * (1.0 - sign * beta * relative_cosine))
    )


def required_relative_cosine(
    soft_energy: float,
    soft_cosine: complex,
    decay_cosine: complex,
    target_hard_cosine: complex,
    sign: int,
) -> complex:
    _, _, gamma, gamma_beta = boost_coefficients(soft_energy)
    denominator = (
        (gamma - 1.0) * soft_cosine
        + target_hard_cosine * gamma_beta
    )
    return complex(
        (
            sign * target_hard_cosine * gamma
            - decay_cosine
            + sign * gamma_beta * soft_cosine
        )
        / denominator
    )


def relative_azimuth_roots(
    soft_energy: float,
    soft_cosine: complex,
    decay_cosine: complex,
    target_hard_cosine: complex,
    sign: int,
) -> tuple[complex, complex, complex]:
    relative_cosine = required_relative_cosine(
        soft_energy,
        soft_cosine,
        decay_cosine,
        target_hard_cosine,
        sign,
    )
    soft_transverse = np.sqrt(1.0 - soft_cosine**2 + 0.0j)
    decay_transverse = np.sqrt(1.0 - decay_cosine**2 + 0.0j)
    azimuth_cosine = (
        relative_cosine - soft_cosine * decay_cosine
    ) / (soft_transverse * decay_transverse)
    discriminant = np.sqrt(azimuth_cosine**2 - 1.0 + 0.0j)
    return (
        complex(azimuth_cosine + discriminant),
        complex(azimuth_cosine - discriminant),
        complex(relative_cosine),
    )


def direction_pair_from_cosines(
    soft_cosine: complex,
    decay_cosine: complex,
    relative_circle: complex,
) -> tuple[np.ndarray, np.ndarray]:
    soft_transverse = np.sqrt(1.0 - soft_cosine**2 + 0.0j)
    decay_transverse = np.sqrt(1.0 - decay_cosine**2 + 0.0j)
    azimuth_cosine = (relative_circle + 1.0 / relative_circle) / 2.0
    azimuth_sine = (relative_circle - 1.0 / relative_circle) / (2.0j)
    soft_direction = np.asarray(
        [soft_transverse, 0.0, soft_cosine], dtype=np.complex128
    )
    decay_direction = np.asarray(
        [
            decay_transverse * azimuth_cosine,
            decay_transverse * azimuth_sine,
            decay_cosine,
        ],
        dtype=np.complex128,
    )
    return soft_direction, decay_direction


def kinematic_validation(power: int, seed: int) -> dict[str, Any]:
    points = qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
    maximum_momentum_residual = 0.0
    maximum_mass_shell_residual = 0.0
    maximum_cosine_residual = 0.0
    for point in points:
        soft_energy = 0.02 + 0.96 * float(point[0])
        soft_direction = M5017.direction(float(point[1]), 0.0)
        decay_direction = M5017.direction(float(point[2]), float(point[3]))
        reference = M5017.sequential_three_body(
            soft_energy, soft_direction, decay_direction
        ).astype(np.complex128)
        analytic = complex_sequential_three_body(
            soft_energy, soft_direction, decay_direction
        )
        maximum_momentum_residual = max(
            maximum_momentum_residual,
            float(np.max(np.abs(reference - analytic))),
        )
        total = np.sum(analytic, axis=0)
        maximum_momentum_residual = max(
            maximum_momentum_residual,
            float(np.max(np.abs(total - np.asarray([2.0, 0.0, 0.0, 0.0])))),
        )
        for internal_index, sign in enumerate((1, -1)):
            momentum = analytic[internal_index]
            mass_shell = momentum[0] ** 2 - sum(
                momentum[space_index] ** 2 for space_index in (1, 2, 3)
            )
            maximum_mass_shell_residual = max(
                maximum_mass_shell_residual, abs(mass_shell)
            )
            relative_cosine = float(soft_direction @ decay_direction)
            predicted = boosted_hard_cosine(
                soft_energy,
                soft_direction[2],
                decay_direction[2],
                relative_cosine,
                sign,
            )
            maximum_cosine_residual = max(
                maximum_cosine_residual,
                abs(predicted - momentum[3] / momentum[0]),
            )
    return {
        "samples": len(points),
        "maximum_four_momentum_residual": maximum_momentum_residual,
        "maximum_mass_shell_residual": maximum_mass_shell_residual,
        "maximum_hard_cosine_residual": maximum_cosine_residual,
        "passed": max(
            maximum_momentum_residual,
            maximum_mass_shell_residual,
            maximum_cosine_residual,
        )
        < 2.0e-12,
    }


def pinch_validation() -> dict[str, Any]:
    soft_energy = 0.37
    soft_cosine = complex(0.23, 0.0)
    decay_cosine = complex(-0.31, 0.0)
    scattering_cosine = complex(1.5, 0.08)
    rows: list[dict[str, Any]] = []
    maximum_hard_pinch_residual = 0.0
    maximum_reciprocity_residual = 0.0
    for sign in (1, -1):
        for external_sign in (1, -1):
            target = external_sign * scattering_cosine
            first_root, second_root, relative_cosine = relative_azimuth_roots(
                soft_energy,
                soft_cosine,
                decay_cosine,
                target,
                sign,
            )
            root_residuals: list[float] = []
            for root in (first_root, second_root):
                soft_direction, decay_direction = direction_pair_from_cosines(
                    soft_cosine, decay_cosine, root
                )
                internal = complex_sequential_three_body(
                    soft_energy, soft_direction, decay_direction
                )
                hard_cosine = internal[0 if sign == 1 else 1, 3] / internal[
                    0 if sign == 1 else 1, 0
                ]
                residual = abs(hard_cosine - target)
                root_residuals.append(residual)
                maximum_hard_pinch_residual = max(
                    maximum_hard_pinch_residual, residual
                )
            reciprocity_residual = abs(first_root * second_root - 1.0)
            maximum_reciprocity_residual = max(
                maximum_reciprocity_residual, reciprocity_residual
            )
            rows.append(
                {
                    "hard_leg_sign": sign,
                    "external_polar_sign": external_sign,
                    "target_hard_cosine": str(target),
                    "required_soft_decay_cosine": str(relative_cosine),
                    "relative_azimuth_root_1": str(first_root),
                    "relative_azimuth_root_2": str(second_root),
                    "root_product": str(first_root * second_root),
                    "root_residuals": root_residuals,
                }
            )
    return {
        "rows": rows,
        "maximum_hard_pinch_residual": maximum_hard_pinch_residual,
        "maximum_root_reciprocity_residual": maximum_reciprocity_residual,
        "passed": max(
            maximum_hard_pinch_residual,
            maximum_reciprocity_residual,
        )
        < 2.0e-11,
        "polar_pinch_surfaces": [
            "c_soft=+z",
            "c_soft=-z",
            "c_decay=+z",
            "c_decay=-z",
            "c_hard_plus=+z",
            "c_hard_plus=-z",
            "c_hard_minus=+z",
            "c_hard_minus=-z",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=7)
    parser.add_argument("--seed", type=int, default=50271)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = {
        "kinematic_validation": kinematic_validation(
            arguments.power, arguments.seed
        ),
        "pinch_validation": pinch_validation(),
        "boosted_polar_law_derived": True,
        "finite_x_polar_pinch_map_derived": True,
        "relative_cycle_residue_sum_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    serialized = json.dumps(
        result,
        indent=2,
        default=lambda value: value.item()
        if isinstance(value, np.generic)
        else str(value),
    )
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
