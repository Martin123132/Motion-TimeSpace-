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
SCRIPT_5019 = POST / "scripts" / "Y5_R2FR_5019_hhh_exact_soft_endpoint_and_crossed_pole_theorem.py"
SCRIPT_5021 = POST / "scripts" / "Y5_R2FR_5021_global_azimuth_feynman_contour_nested_hhh_smoke.py"
START_COSINE = complex(0.3, 0.0)
BRACKET_PAIRS = {
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 1),
    (4, 2),
    (2, 0),
    (1, 0),
    (0, 3),
}
BASE_RADII = np.asarray((0.35, 0.45, 0.58, 0.72, 0.86, 1.16, 1.38, 1.72, 2.2))


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5019 = load_module("mts_5019_for_5022", SCRIPT_5019)
M5021 = load_module("mts_5021_for_5022", SCRIPT_5021)
M5017 = M5021.M5017


def rotate_vector(vector: np.ndarray, unit_circle: complex) -> np.ndarray:
    inverse = 1.0 / unit_circle
    cosine = (unit_circle + inverse) / 2.0
    sine = (unit_circle - inverse) / (2.0j)
    return np.asarray(
        [
            cosine * vector[0] - sine * vector[1],
            sine * vector[0] + cosine * vector[1],
            vector[2],
        ],
        dtype=np.complex128,
    )


def endpoint_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> complex:
    soft_rotated = rotate_vector(soft_direction, unit_circle)
    decay_rotated = rotate_vector(decay_direction, unit_circle)
    internal = np.zeros((3, 4), dtype=np.complex128)
    internal[0, 0] = 1.0
    internal[0, 1:] = decay_rotated
    internal[1, 0] = 1.0
    internal[1, 1:] = -decay_rotated
    left, right = M5017.cut_momenta(
        internal, scattering_cosine, 1.0
    )
    soft_left = np.empty(4, dtype=np.complex128)
    soft_left[0] = 1.0
    soft_left[1:] = soft_rotated
    soft_right = -soft_left
    result = 0.0j
    for special in (1, 2):
        result += (
            M5017.spinor_soft_factor(left, soft_left, 0)
            * M5017.scalar_klt_four(left, special, 0)
            * M5017.spinor_soft_factor(right, soft_right, 1)
            * M5017.scalar_klt_four(right, special, 1)
        )
        result += (
            M5017.spinor_soft_factor(left, soft_left, 1)
            * M5017.scalar_klt_four(left, special, 1)
            * M5017.spinor_soft_factor(right, soft_right, 0)
            * M5017.scalar_klt_four(right, special, 0)
        )
    return complex(result / (2.0 * M5021.S_VALUE * M5021.S_VALUE))


def spinor_tables(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> tuple[np.ndarray, np.ndarray]:
    soft_rotated = rotate_vector(soft_direction, unit_circle)
    decay_rotated = rotate_vector(decay_direction, unit_circle)
    internal = np.zeros((3, 4), dtype=np.complex128)
    internal[0, 0] = 1.0
    internal[0, 1:] = decay_rotated
    internal[1, 0] = 1.0
    internal[1, 1:] = -decay_rotated
    left, right = M5017.cut_momenta(
        internal, scattering_cosine, 1.0
    )
    soft_left = np.empty(4, dtype=np.complex128)
    soft_left[0] = 1.0
    soft_left[1:] = soft_rotated
    left[3] = soft_left
    right[3] = -soft_left
    return M5017.spinor_table(left), M5017.spinor_table(right)


def bracket_roots(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
) -> dict[tuple[str, int, tuple[int, int]], complex]:
    positive = spinor_tables(
        soft_direction, decay_direction, scattering_cosine, 1.0 + 0.0j
    )
    negative = spinor_tables(
        soft_direction, decay_direction, scattering_cosine, -1.0 + 0.0j
    )
    roots: dict[tuple[str, int, tuple[int, int]], complex] = {}
    for side_index, side in enumerate(("left", "right")):
        for chirality in (0, 1):
            for pair in BRACKET_PAIRS:
                positive_value = M5017.bracket(
                    positive[side_index], pair[0], pair[1], chirality
                )
                negative_value = M5017.bracket(
                    negative[side_index], pair[0], pair[1], chirality
                )
                linear = (positive_value - negative_value) / 2.0
                constant = (positive_value + negative_value) / 2.0
                if chirality == 0:
                    if abs(linear) < 1.0e-11:
                        continue
                    root = -constant / linear
                else:
                    if abs(constant) < 1.0e-11:
                        continue
                    root = -linear / constant
                if 1.0e-8 < abs(root) < 1.0e8:
                    roots[(side, chirality, pair)] = complex(root)
    return roots


def root_groups(
    target_roots: dict[tuple[str, int, tuple[int, int]], complex],
    start_roots: dict[tuple[str, int, tuple[int, int]], complex],
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for label, root in target_roots.items():
        group = next(
            (
                candidate
                for candidate in groups
                if abs(root - candidate["root"])
                < 2.0e-7 * max(1.0, abs(root))
            ),
            None,
        )
        if group is None:
            groups.append({"root": root, "roots": [root], "labels": [label]})
        else:
            group["roots"].append(root)
            group["labels"].append(label)
            group["root"] = sum(group["roots"]) / len(group["roots"])
    for group in groups:
        start_inside = [
            abs(start_roots[label]) < 1.0
            for label in group["labels"]
            if label in start_roots
        ]
        if len(set(start_inside)) > 1:
            raise RuntimeError("coincident roots have mixed physical-sheet ownership")
        group["desired_inside"] = start_inside[0] if start_inside else False
    return groups


def circle_integral(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    radius: float,
    nodes: int,
) -> complex:
    return sum(
        endpoint_value(
            soft_direction,
            decay_direction,
            scattering_cosine,
            radius
            * np.exp(2.0j * np.pi * (index + 0.371) / nodes),
        )
        for index in range(nodes)
    ) / nodes


def local_residue(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    root: complex,
    radius: float,
    nodes: int,
) -> complex:
    result = 0.0j
    for index in range(nodes):
        phase = np.exp(2.0j * np.pi * (index + 0.193) / nodes)
        unit_circle = root + radius * phase
        result += (
            endpoint_value(
                soft_direction,
                decay_direction,
                scattering_cosine,
                unit_circle,
            )
            / unit_circle
            * radius
            * phase
        )
    return result / nodes


def select_base_radius(groups: list[dict[str, Any]]) -> float:
    moduli = np.asarray([abs(group["root"]) for group in groups])
    scores = [
        np.min(np.abs(np.log(radius / moduli)))
        - 0.02 * abs(math.log(radius))
        for radius in BASE_RADII
    ]
    return float(BASE_RADII[int(np.argmax(scores))])


def corrected_endpoint_directions(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
    start_cosine: complex = START_COSINE,
) -> complex:
    target_roots = bracket_roots(
        soft_direction, decay_direction, scattering_cosine
    )
    start_roots = bracket_roots(
        soft_direction, decay_direction, start_cosine
    )
    groups = root_groups(target_roots, start_roots)
    base_radius = select_base_radius(groups)
    result = circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_radius,
        base_nodes,
    )
    for group in groups:
        separations = [
            abs(group["root"] - other["root"])
            for other in groups
            if other is not group
        ]
        local_radius = 0.14 * min([abs(group["root"])] + separations)
        residue = local_residue(
            soft_direction,
            decay_direction,
            scattering_cosine,
            group["root"],
            max(local_radius, 1.0e-7),
            residue_nodes,
        )
        currently_inside = abs(group["root"]) < base_radius
        if group["desired_inside"] and not currently_inside:
            result += residue
        elif currently_inside and not group["desired_inside"]:
            result -= residue
    return result


def corrected_endpoint_event(
    point: np.ndarray,
    scattering_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
) -> complex:
    soft_direction, decay_direction, importance_weight = M5021.reduced_directions(
        float(point[0]),
        float(point[1]),
        float(point[2]),
        scattering_cosine,
    )
    return importance_weight * corrected_endpoint_directions(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_nodes,
        residue_nodes,
    )


def rotate_internal(
    internal: np.ndarray, unit_circle: complex
) -> np.ndarray:
    inverse = 1.0 / unit_circle
    cosine = (unit_circle + inverse) / 2.0
    sine = (unit_circle - inverse) / (2.0j)
    result = np.empty((3, 4), dtype=np.complex128)
    result[:, 0] = internal[:, 0]
    result[:, 3] = internal[:, 3]
    result[:, 1] = cosine * internal[:, 1] - sine * internal[:, 2]
    result[:, 2] = sine * internal[:, 1] + cosine * internal[:, 2]
    return result


def finite_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
    soft_energy: float,
) -> complex:
    internal = M5021.SEQUENTIAL_THREE_BODY(
        soft_energy, soft_direction, decay_direction
    )
    inverse_energy_squared_sum = sum(
        1.0 / (internal[index, 0] * internal[index, 0])
        for index in range(3)
    )
    sector_multiplier = (
        3.0
        / (internal[2, 0] * internal[2, 0])
        / inverse_energy_squared_sum
    )
    return complex(
        soft_energy
        * soft_energy
        * sector_multiplier
        * M5021.HHH_REDUCED_PRODUCT(
            rotate_internal(internal, unit_circle),
            scattering_cosine,
            1.0,
        )
        / (M5021.S_VALUE * M5021.S_VALUE)
    )


def remainder_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
    soft_energy: float,
) -> complex:
    return (
        finite_value(
            soft_direction,
            decay_direction,
            scattering_cosine,
            unit_circle,
            soft_energy,
        )
        - endpoint_value(
            soft_direction,
            decay_direction,
            scattering_cosine,
            unit_circle,
        )
    ) / soft_energy


def finite_spinor_tables(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
    soft_energy: float,
) -> tuple[np.ndarray, np.ndarray]:
    internal = M5021.SEQUENTIAL_THREE_BODY(
        soft_energy, soft_direction, decay_direction
    )
    left, right = M5017.cut_momenta(
        rotate_internal(internal, unit_circle),
        scattering_cosine,
        1.0,
    )
    return M5017.spinor_table(left), M5017.spinor_table(right)


def finite_bracket_roots(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_energy: float,
) -> dict[tuple[str, int, tuple[int, int]], complex]:
    positive = finite_spinor_tables(
        soft_direction,
        decay_direction,
        scattering_cosine,
        1.0 + 0.0j,
        soft_energy,
    )
    negative = finite_spinor_tables(
        soft_direction,
        decay_direction,
        scattering_cosine,
        -1.0 + 0.0j,
        soft_energy,
    )
    roots: dict[tuple[str, int, tuple[int, int]], complex] = {}
    for side_index, side in enumerate(("left", "right")):
        for chirality in (0, 1):
            for pair in BRACKET_PAIRS:
                positive_value = M5017.bracket(
                    positive[side_index], pair[0], pair[1], chirality
                )
                negative_value = M5017.bracket(
                    negative[side_index], pair[0], pair[1], chirality
                )
                linear = (positive_value - negative_value) / 2.0
                constant = (positive_value + negative_value) / 2.0
                if chirality == 0:
                    if abs(linear) < 1.0e-11:
                        continue
                    root = -constant / linear
                else:
                    if abs(constant) < 1.0e-11:
                        continue
                    root = -linear / constant
                if 1.0e-8 < abs(root) < 1.0e8:
                    roots[(side, chirality, pair)] = complex(root)
    return roots


def remainder_roots(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_energy: float,
) -> dict[tuple[str, str, int, tuple[int, int]], complex]:
    result = {
        ("finite", *label): root
        for label, root in finite_bracket_roots(
            soft_direction,
            decay_direction,
            scattering_cosine,
            soft_energy,
        ).items()
    }
    result.update(
        {
            ("endpoint", *label): root
            for label, root in bracket_roots(
                soft_direction, decay_direction, scattering_cosine
            ).items()
        }
    )
    return result


def remainder_circle_integral(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_energy: float,
    radius: float,
    nodes: int,
) -> complex:
    return sum(
        remainder_value(
            soft_direction,
            decay_direction,
            scattering_cosine,
            radius
            * np.exp(2.0j * np.pi * (index + 0.371) / nodes),
            soft_energy,
        )
        for index in range(nodes)
    ) / nodes


def remainder_local_residue(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_energy: float,
    root: complex,
    radius: float,
    nodes: int,
) -> complex:
    result = 0.0j
    for index in range(nodes):
        phase = np.exp(2.0j * np.pi * (index + 0.193) / nodes)
        unit_circle = root + radius * phase
        result += (
            remainder_value(
                soft_direction,
                decay_direction,
                scattering_cosine,
                unit_circle,
                soft_energy,
            )
            / unit_circle
            * radius
            * phase
        )
    return result / nodes


def corrected_remainder_directions(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_energy: float,
    start_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
) -> complex:
    target_roots = remainder_roots(
        soft_direction,
        decay_direction,
        scattering_cosine,
        soft_energy,
    )
    start_roots = remainder_roots(
        soft_direction,
        decay_direction,
        start_cosine,
        soft_energy,
    )
    groups = root_groups(target_roots, start_roots)
    base_radius = select_base_radius(groups)
    result = remainder_circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        soft_energy,
        base_radius,
        base_nodes,
    )
    for group in groups:
        separations = [
            abs(group["root"] - other["root"])
            for other in groups
            if other is not group
        ]
        local_radius = 0.12 * min([abs(group["root"])] + separations)
        residue = remainder_local_residue(
            soft_direction,
            decay_direction,
            scattering_cosine,
            soft_energy,
            group["root"],
            max(local_radius, 1.0e-8),
            residue_nodes,
        )
        currently_inside = abs(group["root"]) < base_radius
        if group["desired_inside"] and not currently_inside:
            result += residue
        elif currently_inside and not group["desired_inside"]:
            result -= residue
    return result


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def endpoint_gate(
    power: int,
    seeds: tuple[int, ...],
    base_nodes: int,
    residue_nodes: int,
) -> dict[str, Any]:
    mp.mp.dps = 50
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_q1p5", complex(1.5, 0.08)),
        ("crossed_q3", complex(3.0, 0.08)),
    )
    rows: list[dict[str, Any]] = []
    for configuration, scattering_cosine in configurations:
        seed_means: list[complex] = []
        for seed in seeds:
            points = qmc.Sobol(
                d=3, scramble=True, seed=seed + 50220
            ).random_base2(power)
            seed_means.append(
                complex(
                    np.mean(
                        [
                            corrected_endpoint_event(
                                point,
                                scattering_cosine,
                                base_nodes,
                                residue_nodes,
                            )
                            for point in points
                        ]
                    )
                )
            )
        mean, real_error, imaginary_error = aggregate(seed_means)
        exact = complex(
            M5019.endpoint_resolvent(
                mp.mpc(scattering_cosine.real, scattering_cosine.imag), 192
            )[2]
        )
        residual = abs(mean - exact)
        relative = residual / max(abs(exact), 1.0e-30)
        rows.append(
            {
                "configuration": configuration,
                "scattering_cosine": str(scattering_cosine),
                "residue_continuation": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "exact_resolvent": str(exact),
                "absolute_residual": residual,
                "relative_residual": relative,
                "status": "PASS" if relative < 0.15 else "FAIL",
                "seed_means": [str(value) for value in seed_means],
            }
        )
    return {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "base_nodes": base_nodes,
        "residue_nodes": residue_nodes,
        "rows": rows,
        "all_passed": all(row["status"] == "PASS" for row in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=4)
    parser.add_argument("--seeds", default="50221,50222,50223,50224")
    parser.add_argument("--base-nodes", type=int, default=192)
    parser.add_argument("--residue-nodes", type=int, default=96)
    arguments = parser.parse_args()
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    if arguments.power < 3 or len(seeds) < 2:
        raise ValueError("power >= 3 and at least two seeds are required")
    result = endpoint_gate(
        arguments.power,
        seeds,
        arguments.base_nodes,
        arguments.residue_nodes,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
