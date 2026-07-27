from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5028 = (
    POST
    / "scripts"
    / "Y5_R2FR_5028_finite_x_relative_chamber_transport_event.py"
)
ROOT_LABELS = ("plus_u", "plus_v", "minus_u", "minus_v")
REFERENCE_COSINE = complex(0.3, 0.0)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5028 = load_module("mts_5028_for_5029", SCRIPT_5028)
M5027 = M5028.M5027
M5024 = M5028.M5024
Laurent = dict[int, complex]


def laurent_add(left: Laurent, right: Laurent, scale: complex = 1.0) -> Laurent:
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, 0.0j) + scale * coefficient
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if abs(coefficient) > 1.0e-14
    }


def laurent_scale(polynomial: Laurent, scale: complex) -> Laurent:
    return {
        exponent: scale * coefficient
        for exponent, coefficient in polynomial.items()
    }


def laurent_multiply(left: Laurent, right: Laurent) -> Laurent:
    result: Laurent = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, 0.0j)
                + left_coefficient * right_coefficient
            )
    return result


def laurent_value(polynomial: Laurent, value: complex) -> complex:
    return complex(
        sum(
            coefficient * value**exponent
            for exponent, coefficient in polynomial.items()
        )
    )


def source_momenta(
    soft_energy: float, soft_cosine: float, decay_cosine: float
) -> dict[str, tuple[Laurent, Laurent, Laurent, Laurent]]:
    soft_transverse = complex(np.sqrt(1.0 - soft_cosine**2 + 0.0j))
    decay_transverse = complex(np.sqrt(1.0 - decay_cosine**2 + 0.0j))
    recoil_root, beta, gamma, gamma_beta = M5027.boost_coefficients(
        soft_energy
    )
    relative_cosine: Laurent = {
        -1: soft_transverse * decay_transverse / 2.0,
        0: soft_cosine * decay_cosine,
        1: soft_transverse * decay_transverse / 2.0,
    }
    sources: dict[str, tuple[Laurent, Laurent, Laurent, Laurent]] = {}
    for source, sign in (("direct:g1", 1.0), ("direct:g2", -1.0)):
        energy = laurent_scale(
            laurent_add(
                {0: 1.0}, relative_cosine, -sign * beta
            ),
            gamma * recoil_root,
        )
        pz = laurent_scale(relative_cosine, sign * (gamma - 1.0) * soft_cosine)
        pz = laurent_add(
            pz,
            {
                0: sign * decay_cosine - gamma_beta * soft_cosine
            },
        )
        pz = laurent_scale(pz, recoil_root)
        pplus = laurent_scale(
            relative_cosine,
            sign * (gamma - 1.0) * soft_transverse,
        )
        pplus = laurent_add(
            pplus,
            {
                0: -gamma_beta * soft_transverse,
                1: sign * decay_transverse,
            },
        )
        pplus = laurent_scale(pplus, recoil_root)
        pminus = laurent_scale(
            relative_cosine,
            sign * (gamma - 1.0) * soft_transverse,
        )
        pminus = laurent_add(
            pminus,
            {
                -1: sign * decay_transverse,
                0: -gamma_beta * soft_transverse,
            },
        )
        pminus = laurent_scale(pminus, recoil_root)
        sources[source] = (energy, pz, pplus, pminus)
    sources["direct:g3"] = (
        {0: soft_energy},
        {0: soft_energy * soft_cosine},
        {0: soft_energy * soft_transverse},
        {0: soft_energy * soft_transverse},
    )
    sources["subtraction:decay"] = (
        {0: 1.0},
        {0: decay_cosine},
        {1: decay_transverse},
        {-1: decay_transverse},
    )
    return sources


def root_rationals(
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    scattering_cosine: complex,
) -> dict[str, tuple[Laurent, Laurent]]:
    external = complex(
        np.sqrt(
            (1.0 - scattering_cosine) / (1.0 + scattering_cosine)
            + 0.0j
        )
    )
    result: dict[str, tuple[Laurent, Laurent]] = {}
    for source, (energy, pz, pplus, pminus) in source_momenta(
        soft_energy, soft_cosine, decay_cosine
    ).items():
        energy_plus_pz = laurent_add(energy, pz)
        result[f"{source}:plus_u"] = (
            laurent_scale(energy_plus_pz, external),
            pplus,
        )
        result[f"{source}:plus_v"] = (
            pminus,
            laurent_scale(energy_plus_pz, external),
        )
        result[f"{source}:minus_u"] = (
            laurent_scale(energy_plus_pz, -1.0),
            laurent_scale(pplus, external),
        )
        result[f"{source}:minus_v"] = (
            laurent_scale(pminus, -external),
            energy_plus_pz,
        )
    return result


def rational_value(rational: tuple[Laurent, Laurent], value: complex) -> complex:
    return laurent_value(rational[0], value) / laurent_value(
        rational[1], value
    )


def collision_roots(
    first: tuple[Laurent, Laurent], second: tuple[Laurent, Laurent]
) -> list[complex]:
    numerator = laurent_add(
        laurent_multiply(first[0], second[1]),
        laurent_multiply(second[0], first[1]),
        -1.0,
    )
    if not numerator:
        return []
    minimum_exponent = min(numerator)
    maximum_exponent = max(numerator)
    coefficients = np.asarray(
        [
            numerator.get(exponent, 0.0j)
            for exponent in range(maximum_exponent, minimum_exponent - 1, -1)
        ],
        dtype=np.complex128,
    )
    scale = max(float(np.max(np.abs(coefficients))), 1.0e-30)
    while len(coefficients) > 1 and abs(coefficients[0]) < 1.0e-11 * scale:
        coefficients = coefficients[1:]
    roots: list[complex] = []
    for root in np.roots(coefficients):
        root = complex(root)
        if not 1.0e-8 < abs(root) < 1.0e8:
            continue
        try:
            first_value = rational_value(first, root)
            second_value = rational_value(second, root)
        except ZeroDivisionError:
            continue
        residual = abs(first_value - second_value) / max(
            abs(first_value), abs(second_value), 1.0
        )
        if residual < 2.0e-6:
            roots.append(root)
    return roots


def all_collision_rows(
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    scattering_cosine: complex,
) -> tuple[dict[str, tuple[Laurent, Laurent]], list[dict[str, Any]]]:
    rationals = root_rationals(
        soft_energy, soft_cosine, decay_cosine, scattering_cosine
    )
    keys = sorted(rationals)
    rows: list[dict[str, Any]] = []
    for first_index, first_key in enumerate(keys):
        for second_key in keys[first_index + 1 :]:
            for root in collision_roots(
                rationals[first_key], rationals[second_key]
            ):
                rows.append(
                    {
                        "root": root,
                        "pair": (first_key, second_key),
                    }
                )
    return rationals, rows


def physical_opposite_ownership_boundaries(
    soft_energy: float, soft_cosine: float, decay_cosine: float
) -> list[dict[str, Any]]:
    rationals, rows = all_collision_rows(
        soft_energy,
        soft_cosine,
        decay_cosine,
        REFERENCE_COSINE,
    )
    unit_rows = [row for row in rows if abs(abs(row["root"]) - 1.0) < 2.0e-6]
    selected: list[dict[str, Any]] = []
    for row in unit_rows:
        angle = math.atan2(row["root"].imag, row["root"].real) % (
            2.0 * math.pi
        )
        probe = np.exp(1.0j * (angle + 2.0e-5))
        first_inside = abs(rational_value(rationals[row["pair"][0]], probe)) < 1.0
        second_inside = abs(rational_value(rationals[row["pair"][1]], probe)) < 1.0
        if first_inside == second_inside:
            continue
        selected.append(
            {
                "angle": angle,
                "root": row["root"],
                "pairs": [row["pair"]],
            }
        )
    selected.sort(key=lambda row: row["angle"])
    groups: list[dict[str, Any]] = []
    for row in selected:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"]) < 2.0e-6
            ),
            None,
        )
        if group is None:
            groups.append(row)
        else:
            group["pairs"].extend(row["pairs"])
    return groups


def track_collision(
    start_root: complex,
    pair: tuple[str, str],
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    target_cosine: complex,
    steps: int,
) -> complex:
    current = start_root
    for step in range(1, steps + 1):
        fraction = step / steps
        cosine = REFERENCE_COSINE + fraction * (
            target_cosine - REFERENCE_COSINE
        )
        rationals = root_rationals(
            soft_energy, soft_cosine, decay_cosine, cosine
        )
        candidates = collision_roots(
            rationals[pair[0]], rationals[pair[1]]
        )
        if not candidates:
            raise RuntimeError(f"collision branch disappeared for {pair}")
        current = min(candidates, key=lambda root: abs(root - current))
    return current


def collision_map(steps: int) -> dict[str, Any]:
    soft_energy = 0.37
    soft_cosine = 0.23
    decay_cosine = -0.31
    target_cosine = complex(1.5, 0.08)
    boundaries = physical_opposite_ownership_boundaries(
        soft_energy, soft_cosine, decay_cosine
    )
    rows: list[dict[str, Any]] = []
    maximum_target_collision_residual = 0.0
    target_rationals = root_rationals(
        soft_energy, soft_cosine, decay_cosine, target_cosine
    )
    for boundary in boundaries:
        pair = boundary["pairs"][0]
        target_root = track_collision(
            boundary["root"],
            pair,
            soft_energy,
            soft_cosine,
            decay_cosine,
            target_cosine,
            steps,
        )
        first_value = rational_value(target_rationals[pair[0]], target_root)
        second_value = rational_value(target_rationals[pair[1]], target_root)
        residual = abs(first_value - second_value) / max(
            abs(first_value), abs(second_value), 1.0
        )
        maximum_target_collision_residual = max(
            maximum_target_collision_residual, residual
        )
        rows.append(
            {
                "physical_angle": boundary["angle"],
                "physical_root": str(boundary["root"]),
                "colliding_pairs": [list(pair_value) for pair_value in boundary["pairs"]],
                "target_root": str(target_root),
                "target_collision_residual": residual,
            }
        )
    self_only = M5028.physical_relative_boundaries(
        soft_energy, soft_cosine, decay_cosine
    )
    return {
        "soft_energy": soft_energy,
        "soft_cosine": soft_cosine,
        "decay_cosine": decay_cosine,
        "self_collision_boundary_count_5028": len(self_only),
        "all_opposite_ownership_boundary_count": len(boundaries),
        "new_cross_source_boundary_count": max(0, len(boundaries) - len(self_only)),
        "rows": rows,
        "maximum_target_collision_residual": maximum_target_collision_residual,
        "collision_map_passed": maximum_target_collision_residual < 2.0e-6,
        "all_cross_source_collision_boundaries_derived": True,
        "relative_chamber_integral_rerun_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking-steps", type=int, default=96)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = collision_map(arguments.tracking_steps)
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
