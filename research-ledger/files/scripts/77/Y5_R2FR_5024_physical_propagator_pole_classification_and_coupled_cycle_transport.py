from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5022 = POST / "scripts" / "Y5_R2FR_5022_rational_azimuth_residue_endpoint_gate.py"
SCRIPT_5023 = POST / "scripts" / "Y5_R2FR_5023_causal_covariant_KLT_endpoint_gate.py"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5022 = load_module("mts_5022_for_5024", SCRIPT_5022)
M5023 = load_module("mts_5023_for_5024", SCRIPT_5023)
M5017 = M5023.M5017


def rotate_internal(internal: np.ndarray, unit_circle: complex) -> np.ndarray:
    rotated = internal.astype(np.complex128).copy()
    for index in range(len(rotated)):
        rotated[index, 1:] = M5022.rotate_vector(
            rotated[index, 1:], unit_circle
        )
    return rotated


def canonical_four_channels(
    gluons: list[int], momenta: np.ndarray
) -> dict[str, complex]:
    first, second = gluons
    return {
        f"s_g{first}g{second}": M5023.subtracted_invariant(
            momenta[first], momenta[second]
        ),
        f"s_P0g{first}": M5023.subtracted_invariant(
            momenta[0], momenta[first]
        ),
    }


def ordered_four_channels(
    order: list[int], momenta: np.ndarray
) -> dict[str, complex]:
    rotated = list(order)
    scalar_start = rotated.index(0)
    rotated = rotated[scalar_start:] + rotated[:scalar_start]
    scalar_end = rotated.index(4)
    alpha = rotated[1:scalar_end]
    beta = rotated[scalar_end + 1 :]
    result: dict[str, complex] = {}
    for shuffle_index, shuffle in enumerate(
        M5023.ordered_shuffles(alpha, list(reversed(beta)))
    ):
        for label, value in canonical_four_channels(shuffle, momenta).items():
            result[f"shuffle{shuffle_index}:{label}"] = value
    return result


def canonical_five_channels(
    gluons: list[int], momenta: np.ndarray
) -> dict[str, complex]:
    first, second, third = gluons
    return {
        f"s_g{first}g{second}": M5023.subtracted_invariant(
            momenta[first], momenta[second]
        ),
        f"s_g{second}g{third}": M5023.subtracted_invariant(
            momenta[second], momenta[third]
        ),
        f"s_g{first}g{second}g{third}": M5023.subtracted_invariant(
            momenta[first], momenta[second], momenta[third]
        ),
        f"s_P0g{first}": M5023.subtracted_invariant(
            momenta[0], momenta[first]
        ),
        f"s_P0g{third}": M5023.subtracted_invariant(
            momenta[0], momenta[third]
        ),
        f"s_g{third}P4": M5023.subtracted_invariant(
            momenta[third], momenta[4]
        ),
    }


def ordered_five_channels(
    order: list[int], momenta: np.ndarray
) -> dict[str, complex]:
    rotated = list(order)
    scalar_start = rotated.index(0)
    rotated = rotated[scalar_start:] + rotated[:scalar_start]
    scalar_end = rotated.index(4)
    alpha = rotated[1:scalar_end]
    beta = rotated[scalar_end + 1 :]
    result: dict[str, complex] = {}
    for shuffle_index, shuffle in enumerate(
        M5023.ordered_shuffles(alpha, list(reversed(beta)))
    ):
        for label, value in canonical_five_channels(shuffle, momenta).items():
            result[f"shuffle{shuffle_index}:{label}"] = value
    return result


def endpoint_channels(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> dict[str, complex]:
    soft_rotated = M5022.rotate_vector(soft_direction, unit_circle)
    decay_rotated = M5022.rotate_vector(decay_direction, unit_circle)
    internal = np.zeros((3, 4), dtype=np.complex128)
    internal[0] = np.concatenate(([1.0], decay_rotated))
    internal[1] = np.concatenate(([1.0], -decay_rotated))
    left, right = M5017.cut_momenta(internal, scattering_cosine, 1.0)
    soft_left = np.concatenate(([1.0], soft_rotated)).astype(np.complex128)
    soft_right = -soft_left
    result: dict[str, complex] = {}
    orders = ([0, 1, 2, 4], [2, 4, 1, 0])
    for side_name, momenta, soft in (
        ("left", left, soft_left),
        ("right", right, soft_right),
    ):
        for leg in (0, 1, 2, 4):
            result[f"{side_name}:soft:kdotp{leg}"] = M5023.minkowski(
                soft, momenta[leg]
            )
        for order_index, order in enumerate(orders):
            for label, value in ordered_four_channels(order, momenta).items():
                result[f"{side_name}:gauge{order_index}:{label}"] = value
    return result


def finite_channels(
    internal: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> dict[str, complex]:
    rotated = rotate_internal(internal, unit_circle)
    left, right = M5017.cut_momenta(rotated, scattering_cosine, 1.0)
    result: dict[str, complex] = {}
    orders = (
        [0, 1, 2, 3, 4],
        [0, 2, 1, 3, 4],
        [3, 4, 1, 2, 0],
        [3, 4, 2, 1, 0],
    )
    for side_name, momenta in (("left", left), ("right", right)):
        for order_index, order in enumerate(orders):
            for label, value in ordered_five_channels(order, momenta).items():
                result[f"{side_name}:gauge{order_index}:{label}"] = value
    return result


def laurent_roots(
    evaluator: Callable[[complex], complex], nodes: int = 16
) -> tuple[list[complex], float, tuple[complex, complex, complex]]:
    phases = np.exp(
        2.0j * np.pi * (np.arange(nodes, dtype=float) + 0.173) / nodes
    )
    values = np.asarray([evaluator(complex(phase)) for phase in phases])
    matrix = np.column_stack((1.0 / phases, np.ones(nodes), phases))
    coefficients, *_ = np.linalg.lstsq(matrix, values, rcond=None)
    reconstructed = matrix @ coefficients
    residual = float(
        np.max(np.abs(values - reconstructed))
        / max(float(np.max(np.abs(values))), 1.0e-30)
    )
    minus_one, zero, plus_one = coefficients
    scale = max(abs(minus_one), abs(zero), abs(plus_one), 1.0e-30)
    polynomial = np.asarray([plus_one, zero, minus_one], dtype=np.complex128)
    while len(polynomial) > 1 and abs(polynomial[0]) < 1.0e-11 * scale:
        polynomial = polynomial[1:]
    roots = [
        complex(root)
        for root in np.roots(polynomial)
        if 1.0e-9 < abs(root) < 1.0e9
    ]
    return roots, residual, (complex(minus_one), complex(zero), complex(plus_one))


def channel_root_rows(
    channel_function: Callable[[complex], dict[str, complex]]
) -> tuple[list[dict[str, Any]], float]:
    labels = sorted(channel_function(1.0 + 0.0j))
    rows: list[dict[str, Any]] = []
    maximum_residual = 0.0
    for label in labels:
        roots, residual, coefficients = laurent_roots(
            lambda unit_circle, channel_label=label: channel_function(
                unit_circle
            )[channel_label]
        )
        maximum_residual = max(maximum_residual, residual)
        for root_index, root in enumerate(roots):
            rows.append(
                {
                    "channel": label,
                    "root_index": root_index,
                    "root": root,
                    "root_modulus": abs(root),
                    "laurent_coefficients": coefficients,
                    "laurent_fit_relative_residual": residual,
                }
            )
    return rows, maximum_residual


def group_roots(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for row in rows:
        root = row["root"]
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
            groups.append({"root": root, "roots": [root], "channels": [row["channel"]]})
        else:
            group["roots"].append(root)
            group["channels"].append(row["channel"])
            group["root"] = sum(group["roots"]) / len(group["roots"])
    return groups


def track_channel_roots(
    label: str,
    channel_at: Callable[[complex, complex], dict[str, complex]],
    start_cosine: complex,
    target_cosine: complex,
    steps: int = 401,
) -> list[dict[str, Any]]:
    path = [
        start_cosine
        + (target_cosine - start_cosine) * step_index / (steps - 1)
        for step_index in range(steps)
    ]

    def roots_at(scattering_cosine: complex) -> list[complex]:
        roots, _, _ = laurent_roots(
            lambda unit_circle: channel_at(
                scattering_cosine, unit_circle
            )[label]
        )
        if len(roots) != 2:
            raise RuntimeError(f"expected two roots for {label}, found {len(roots)}")
        return roots

    initial = roots_at(path[0])
    branches = [[initial[0]], [initial[1]]]
    minimum_unit_distance = [abs(abs(initial[0]) - 1.0), abs(abs(initial[1]) - 1.0)]
    minimum_unit_step = [0, 0]
    for step_index, scattering_cosine in enumerate(path[1:], start=1):
        candidates = roots_at(scattering_cosine)
        direct = abs(branches[0][-1] - candidates[0]) + abs(
            branches[1][-1] - candidates[1]
        )
        exchanged = abs(branches[0][-1] - candidates[1]) + abs(
            branches[1][-1] - candidates[0]
        )
        if exchanged < direct:
            candidates = [candidates[1], candidates[0]]
        for branch_index, root in enumerate(candidates):
            branches[branch_index].append(root)
            unit_distance = abs(abs(root) - 1.0)
            if unit_distance < minimum_unit_distance[branch_index]:
                minimum_unit_distance[branch_index] = unit_distance
                minimum_unit_step[branch_index] = step_index
    return [
        {
            "channel": label,
            "branch": branch_index,
            "start_root": str(branch[0]),
            "start_modulus": abs(branch[0]),
            "target_root": str(branch[-1]),
            "target_modulus": abs(branch[-1]),
            "desired_inside_from_start": abs(branch[0]) < 1.0,
            "currently_inside_at_target": abs(branch[-1]) < 1.0,
            "ownership_changed": (abs(branch[0]) < 1.0)
            != (abs(branch[-1]) < 1.0),
            "minimum_distance_to_unit_circle": minimum_unit_distance[
                branch_index
            ],
            "minimum_distance_path_fraction": minimum_unit_step[branch_index]
            / (steps - 1),
            "minimum_distance_cosine": str(path[minimum_unit_step[branch_index]]),
        }
        for branch_index, branch in enumerate(branches)
    ]


def select_base_radius(groups: list[dict[str, Any]]) -> float:
    moduli = np.asarray([abs(group["root"]) for group in groups])
    scores = [
        np.min(np.abs(np.log(radius / moduli))) - 0.02 * abs(math.log(radius))
        for radius in M5022.BASE_RADII
    ]
    return float(M5022.BASE_RADII[int(np.argmax(scores))])


def transported_endpoint_directions(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    start_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
    tracking_steps: int,
) -> complex:
    channel_at = lambda cosine, unit_circle: endpoint_channels(
        soft_direction, decay_direction, cosine, unit_circle
    )
    target_function = lambda unit_circle: channel_at(
        scattering_cosine, unit_circle
    )
    rows, _ = channel_root_rows(target_function)
    groups = group_roots(rows)
    tracks: list[dict[str, Any]] = []
    for label in sorted(set(row["channel"] for row in rows)):
        tracks.extend(
            track_channel_roots(
                label,
                channel_at,
                start_cosine,
                scattering_cosine,
                steps=tracking_steps,
            )
        )
    integrand = lambda unit_circle: M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    base_radius = select_base_radius(groups)
    result = M5022.circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_radius,
        base_nodes,
    )
    for group in groups:
        root = group["root"]
        matching = [
            track
            for track in tracks
            if track["channel"] in group["channels"]
            and abs(complex(track["target_root"]) - root)
            < 5.0e-6 * max(1.0, abs(root))
        ]
        desired_values = set(
            track["desired_inside_from_start"] for track in matching
        )
        if len(desired_values) != 1:
            raise RuntimeError("physical propagator root ownership is ambiguous")
        desired_inside = desired_values.pop()
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = local_residue(
            integrand,
            root,
            max(1.0e-7, 0.08 * safe_scale),
            residue_nodes,
        )
        currently_inside = abs(root) < base_radius
        if desired_inside and not currently_inside:
            result += residue
        elif currently_inside and not desired_inside:
            result -= residue
    return result


def transported_endpoint_event(
    point: np.ndarray,
    scattering_cosine: complex,
    start_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
    tracking_steps: int,
) -> complex:
    soft_direction, decay_direction, importance_weight = M5022.M5021.reduced_directions(
        float(point[0]),
        float(point[1]),
        float(point[2]),
        scattering_cosine,
    )
    return importance_weight * start_sheet_cycle_endpoint_directions(
        soft_direction,
        decay_direction,
        scattering_cosine,
        start_cosine,
        base_nodes,
        residue_nodes,
    )


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def transported_endpoint_smoke(
    power: int,
    seeds: tuple[int, ...],
    base_nodes: int,
    residue_nodes: int,
    tracking_steps: int,
) -> dict[str, Any]:
    scattering_cosine = complex(1.5, 0.08)
    exact = complex(
        M5023.M5019.endpoint_resolvent(
            M5023.mp.mpc(scattering_cosine.real, scattering_cosine.imag), 192
        )[2]
    )
    points = {
        seed: qmc.Sobol(d=3, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    rows: list[dict[str, Any]] = []
    for start_cosine in (complex(-0.3, 0.0), complex(0.0, 0.0), complex(0.3, 0.0)):
        seed_means: list[complex] = []
        for seed in seeds:
            seed_means.append(
                complex(
                    np.mean(
                        [
                            transported_endpoint_event(
                                point,
                                scattering_cosine,
                                start_cosine,
                                base_nodes,
                                residue_nodes,
                                tracking_steps,
                            )
                            for point in points[seed]
                        ]
                    )
                )
            )
        mean, real_error, imaginary_error = aggregate(seed_means)
        rows.append(
            {
                "start_cosine": str(start_cosine),
                "transported_endpoint": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "exact_resolvent": str(exact),
                "relative_residual": abs(mean - exact) / max(abs(exact), 1.0e-30),
                "seed_means": [str(value) for value in seed_means],
            }
        )
    spread = max(
        abs(complex(left["transported_endpoint"]) - complex(right["transported_endpoint"]))
        for left in rows
        for right in rows
    )
    maximum_pair_error = max(
        math.hypot(row["RQMC_real_error"], row["RQMC_imaginary_error"])
        for row in rows
    )
    return {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "base_nodes": base_nodes,
        "residue_nodes": residue_nodes,
        "tracking_steps": tracking_steps,
        "rows": rows,
        "start_cosine_spread": spread,
        "maximum_complex_RQMC_error": maximum_pair_error,
        "start_dependence_resolved": spread < 4.0 * maximum_pair_error,
        "polar_cycle_required": spread >= 4.0 * maximum_pair_error,
    }


def polar_segment(
    segment: str, fraction: float, scattering_cosine: complex
) -> tuple[complex, complex]:
    lower_pinch = (1.0 - scattering_cosine) / 2.0
    upper_pinch = (1.0 + scattering_cosine) / 2.0
    if segment == "north":
        return lower_pinch * fraction, lower_pinch
    if segment == "middle":
        return (
            lower_pinch
            + (upper_pinch - lower_pinch) * fraction,
            upper_pinch - lower_pinch,
        )
    if segment == "south":
        return (
            upper_pinch + (1.0 - upper_pinch) * fraction,
            1.0 - upper_pinch,
        )
    raise ValueError(f"unknown polar segment {segment}")


def direction_from_polar_x(polar_x: complex, azimuth: float) -> np.ndarray:
    transverse = 2.0 * np.sqrt(polar_x * (1.0 - polar_x) + 0.0j)
    return np.asarray(
        [
            transverse * math.cos(azimuth),
            transverse * math.sin(azimuth),
            1.0 - 2.0 * polar_x,
        ],
        dtype=np.complex128,
    )


def stereographic_pair(direction: np.ndarray) -> tuple[complex, complex]:
    denominator = 1.0 + direction[2]
    return (
        complex((direction[0] + 1.0j * direction[1]) / denominator),
        complex((direction[0] - 1.0j * direction[1]) / denominator),
    )


def desired_factor_roots(
    direction: np.ndarray,
    scattering_cosine: complex,
    segment: str,
) -> tuple[complex, complex]:
    external_stereographic = complex(
        np.sqrt(
            (1.0 - scattering_cosine) / (1.0 + scattering_cosine)
            + 0.0j
        )
    )
    holomorphic, antiholomorphic = stereographic_pair(direction)
    plus_root = (
        antiholomorphic / external_stereographic
        if segment == "north"
        else external_stereographic / holomorphic
    )
    minus_root = (
        -1.0 / (external_stereographic * holomorphic)
        if segment == "south"
        else -external_stereographic * antiholomorphic
    )
    return plus_root, minus_root


def all_factor_roots(
    direction: np.ndarray, scattering_cosine: complex
) -> dict[str, complex]:
    external_stereographic = complex(
        np.sqrt(
            (1.0 - scattering_cosine) / (1.0 + scattering_cosine)
            + 0.0j
        )
    )
    holomorphic, antiholomorphic = stereographic_pair(direction)
    return {
        "plus_u": external_stereographic / holomorphic,
        "plus_v": antiholomorphic / external_stereographic,
        "minus_u": -1.0 / (external_stereographic * holomorphic),
        "minus_v": -external_stereographic * antiholomorphic,
    }


def start_owned_factor_roots(
    direction: np.ndarray,
    target_cosine: complex,
    start_cosine: complex,
) -> tuple[complex, complex]:
    target = all_factor_roots(direction, target_cosine)
    start = all_factor_roots(direction, start_cosine)
    plus_label = min(
        ("plus_u", "plus_v"), key=lambda label: abs(start[label])
    )
    minus_label = min(
        ("minus_u", "minus_v"), key=lambda label: abs(start[label])
    )
    return target[plus_label], target[minus_label]


def channel_desired_root(
    channel: str,
    soft_roots: tuple[complex, complex],
    decay_roots: tuple[complex, complex],
) -> complex:
    if channel.endswith("s_P0g1"):
        return decay_roots[0]
    if channel.endswith("s_P0g2"):
        return decay_roots[1]
    if channel.endswith("soft:kdotp0"):
        return soft_roots[0]
    if channel.endswith("soft:kdotp4"):
        return soft_roots[1]
    raise RuntimeError(f"no stereographic ownership rule for {channel}")


def start_sheet_cycle_endpoint_directions(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    start_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
) -> complex:
    channel_function = lambda unit_circle: endpoint_channels(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    rows, _ = channel_root_rows(channel_function)
    groups = group_roots(rows)
    integrand = lambda unit_circle: M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    soft_roots = start_owned_factor_roots(
        soft_direction, scattering_cosine, start_cosine
    )
    decay_roots = start_owned_factor_roots(
        decay_direction, scattering_cosine, start_cosine
    )
    base_radius = select_base_radius(groups)
    result = M5022.circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_radius,
        base_nodes,
    )
    for group in groups:
        root = group["root"]
        desired_matches = [
            abs(
                channel_desired_root(channel, soft_roots, decay_roots) - root
            )
            < 5.0e-6 * max(1.0, abs(root))
            for channel in set(group["channels"])
        ]
        if len(set(desired_matches)) != 1:
            raise RuntimeError("start-sheet channel ownership disagreement")
        desired_inside = desired_matches[0]
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = local_residue(
            integrand,
            root,
            max(1.0e-7, 0.08 * safe_scale),
            residue_nodes,
        )
        currently_inside = abs(root) < base_radius
        if desired_inside and not currently_inside:
            result += residue
        elif currently_inside and not desired_inside:
            result -= residue
    return result


def canonical_cycle_endpoint_directions(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_segment: str,
    decay_segment: str,
    base_nodes: int,
    residue_nodes: int,
) -> complex:
    channel_function = lambda unit_circle: endpoint_channels(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    rows, _ = channel_root_rows(channel_function)
    groups = group_roots(rows)
    integrand = lambda unit_circle: M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    soft_roots = desired_factor_roots(
        soft_direction, scattering_cosine, soft_segment
    )
    decay_roots = desired_factor_roots(
        decay_direction, scattering_cosine, decay_segment
    )
    base_radius = select_base_radius(groups)
    result = M5022.circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_radius,
        base_nodes,
    )
    for group in groups:
        root = group["root"]
        desired_matches = [
            abs(
                channel_desired_root(channel, soft_roots, decay_roots) - root
            )
            < 5.0e-6 * max(1.0, abs(root))
            for channel in set(group["channels"])
        ]
        if len(set(desired_matches)) != 1:
            raise RuntimeError("coincident channels disagree on stereographic ownership")
        desired_inside = desired_matches[0]
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = local_residue(
            integrand,
            root,
            max(1.0e-7, 0.08 * safe_scale),
            residue_nodes,
        )
        currently_inside = abs(root) < base_radius
        if desired_inside and not currently_inside:
            result += residue
        elif currently_inside and not desired_inside:
            result -= residue
    return result


def coupled_sector_endpoint_event(
    point: np.ndarray,
    scattering_cosine: complex,
    base_nodes: int,
    residue_nodes: int,
) -> complex:
    result = 0.0j
    relative_azimuth = 2.0 * math.pi * float(point[2])
    for soft_segment in ("north", "middle", "south"):
        soft_x, soft_jacobian = polar_segment(
            soft_segment, float(point[0]), scattering_cosine
        )
        soft_direction = direction_from_polar_x(soft_x, 0.0)
        for decay_segment in ("north", "middle", "south"):
            decay_x, decay_jacobian = polar_segment(
                decay_segment, float(point[1]), scattering_cosine
            )
            decay_direction = direction_from_polar_x(
                decay_x, relative_azimuth
            )
            result += (
                soft_jacobian
                * decay_jacobian
                * canonical_cycle_endpoint_directions(
                    soft_direction,
                    decay_direction,
                    scattering_cosine,
                    soft_segment,
                    decay_segment,
                    base_nodes,
                    residue_nodes,
                )
            )
    return result


def coupled_sector_endpoint_gate(
    power: int,
    seeds: tuple[int, ...],
    base_nodes: int,
    residue_nodes: int,
) -> dict[str, Any]:
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_q1p5", complex(1.5, 0.08)),
    )
    rows: list[dict[str, Any]] = []
    points = {
        seed: qmc.Sobol(d=3, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    for configuration, scattering_cosine in configurations:
        seed_means: list[complex] = []
        for seed in seeds:
            seed_means.append(
                complex(
                    np.mean(
                        [
                            coupled_sector_endpoint_event(
                                point,
                                scattering_cosine,
                                base_nodes,
                                residue_nodes,
                            )
                            for point in points[seed]
                        ]
                    )
                )
            )
        mean, real_error, imaginary_error = aggregate(seed_means)
        exact = complex(
            M5023.M5019.endpoint_resolvent(
                M5023.mp.mpc(
                    scattering_cosine.real, scattering_cosine.imag
                ),
                192,
            )[2]
        )
        rows.append(
            {
                "configuration": configuration,
                "scattering_cosine": str(scattering_cosine),
                "coupled_sector_endpoint": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "exact_resolvent": str(exact),
                "relative_residual": abs(mean - exact) / max(abs(exact), 1.0e-30),
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
    }


def soft_shape(value: complex) -> complex:
    return complex(
        (1.0 - value) * np.log(1.0 - value + 0.0j)
        + (1.0 + value) * np.log(1.0 + value + 0.0j)
    )


def soft_averaged_endpoint_integrand(
    polar_x: complex,
    scattering_cosine: complex,
    unit_circle: complex,
) -> complex:
    cosine_a = 1.0 - 2.0 * polar_x
    rho = 2.0 * np.sqrt(polar_x * (1.0 - polar_x) + 0.0j)
    transverse = np.sqrt(1.0 - scattering_cosine**2 + 0.0j)
    cosine_phi = (unit_circle + 1.0 / unit_circle) / 2.0
    sine_phi = (unit_circle - 1.0 / unit_circle) / (2.0j)
    cosine_b = (
        scattering_cosine * cosine_a + transverse * rho * cosine_phi
    )
    q_plus = (
        -scattering_cosine * rho
        + transverse * cosine_a * cosine_phi
        + 1.0j * transverse * sine_phi
    )
    q_minus = (
        -scattering_cosine * rho
        + transverse * cosine_a * cosine_phi
        - 1.0j * transverse * sine_phi
    )
    hard_factor = rho**2 / 16.0 * (
        q_plus**3 / q_minus + q_minus**3 / q_plus
    )
    soft_bracket = (
        soft_shape(scattering_cosine)
        - soft_shape(cosine_a)
        - soft_shape(cosine_b)
        + 2.0 * math.log(2.0)
    )
    return complex(hard_factor * soft_bracket)


def sector_azimuth_radius(
    polar_x: complex, scattering_cosine: complex, segment: str
) -> tuple[float, dict[str, complex]]:
    external_stereographic = complex(
        np.sqrt(
            (1.0 - scattering_cosine) / (1.0 + scattering_cosine)
            + 0.0j
        )
    )
    radial = complex(np.sqrt(polar_x / (1.0 - polar_x) + 0.0j))
    roots = {
        "plus_u": external_stereographic / radial,
        "plus_v": radial / external_stereographic,
        "minus_u": -1.0 / (external_stereographic * radial),
        "minus_v": -external_stereographic * radial,
    }
    desired_labels = {
        "north": ("plus_v", "minus_v"),
        "middle": ("plus_u", "minus_v"),
        "south": ("plus_u", "minus_u"),
    }[segment]
    unwanted_labels = tuple(
        label for label in roots if label not in desired_labels
    )
    desired_maximum = max(abs(roots[label]) for label in desired_labels)
    unwanted_minimum = min(abs(roots[label]) for label in unwanted_labels)
    if desired_maximum >= unwanted_minimum:
        raise RuntimeError(
            f"no separating azimuth circle in {segment}: "
            f"desired={desired_maximum}, unwanted={unwanted_minimum}"
        )
    radius = math.sqrt(desired_maximum * unwanted_minimum)
    return radius, roots


def soft_averaged_sector_event(
    fraction: float,
    scattering_cosine: complex,
    azimuth_nodes: int,
) -> complex:
    result = 0.0j
    for segment in ("north", "middle", "south"):
        polar_x, jacobian = polar_segment(
            segment, fraction, scattering_cosine
        )
        radius, _ = sector_azimuth_radius(
            polar_x, scattering_cosine, segment
        )
        azimuth_average = sum(
            soft_averaged_endpoint_integrand(
                polar_x,
                scattering_cosine,
                radius
                * np.exp(
                    2.0j * np.pi * (node_index + 0.271) / azimuth_nodes
                ),
            )
            for node_index in range(azimuth_nodes)
        ) / azimuth_nodes
        result += jacobian * azimuth_average
    return result


def soft_averaged_sector_gate(
    power: int,
    seeds: tuple[int, ...],
    azimuth_nodes: int,
) -> dict[str, Any]:
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_q1p5", complex(1.5, 0.08)),
        ("crossed_q3", complex(3.0, 0.08)),
    )
    rows: list[dict[str, Any]] = []
    points = {
        seed: qmc.Sobol(d=1, scramble=True, seed=seed).random_base2(power)[:, 0]
        for seed in seeds
    }
    for configuration, scattering_cosine in configurations:
        seed_means: list[complex] = []
        failure: str | None = None
        try:
            for seed in seeds:
                seed_means.append(
                    complex(
                        np.mean(
                            [
                                soft_averaged_sector_event(
                                    float(fraction),
                                    scattering_cosine,
                                    azimuth_nodes,
                                )
                                for fraction in points[seed]
                            ]
                        )
                    )
                )
        except RuntimeError as error:
            failure = str(error)
        exact = complex(
            M5023.M5019.endpoint_resolvent(
                M5023.mp.mpc(
                    scattering_cosine.real, scattering_cosine.imag
                ),
                192,
            )[2]
        )
        if failure is None:
            mean, real_error, imaginary_error = aggregate(seed_means)
            relative_residual = abs(mean - exact) / max(abs(exact), 1.0e-30)
        else:
            mean = complex(float("nan"), float("nan"))
            real_error = float("nan")
            imaginary_error = float("nan")
            relative_residual = float("nan")
        rows.append(
            {
                "configuration": configuration,
                "scattering_cosine": str(scattering_cosine),
                "soft_averaged_sector_endpoint": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "exact_resolvent": str(exact),
                "relative_residual": relative_residual,
                "failure": failure,
                "seed_means": [str(value) for value in seed_means],
            }
        )
    return {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "azimuth_nodes": azimuth_nodes,
        "rows": rows,
    }


def attach_ownership(
    classified: list[dict[str, Any]], tracks: list[dict[str, Any]]
) -> None:
    for group in classified:
        root = complex(group["root"])
        matching = [
            track
            for track in tracks
            if track["channel"] in group["channels"]
            and abs(complex(track["target_root"]) - root)
            < 5.0e-6 * max(1.0, abs(root))
        ]
        group["tracked_branches"] = matching
        group["desired_inside_values"] = sorted(
            set(track["desired_inside_from_start"] for track in matching)
        )
        group["ownership_change"] = any(
            track["ownership_changed"] for track in matching
        )


def local_residue(
    integrand: Callable[[complex], complex],
    root: complex,
    radius: float,
    nodes: int,
) -> complex:
    result = 0.0j
    for index in range(nodes):
        phase = np.exp(2.0j * np.pi * (index + 0.317) / nodes)
        unit_circle = root + radius * phase
        result += integrand(unit_circle) / unit_circle * radius * phase
    return complex(result / nodes)


def classify_groups(
    groups: list[dict[str, Any]],
    integrand: Callable[[complex], complex],
    residue_nodes: int,
) -> list[dict[str, Any]]:
    classified: list[dict[str, Any]] = []
    for group in groups:
        root = group["root"]
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        outer_radius = max(1.0e-7, 0.08 * safe_scale)
        inner_radius = outer_radius / 2.0
        outer = local_residue(integrand, root, outer_radius, residue_nodes)
        inner = local_residue(integrand, root, inner_radius, residue_nodes)
        stability = abs(inner - outer) / max(abs(inner), abs(outer), 1.0e-30)
        classified.append(
            {
                "root": str(root),
                "root_modulus": abs(root),
                "channels": sorted(set(group["channels"])),
                "channel_count": len(set(group["channels"])),
                "residue_outer": str(outer),
                "residue_inner": str(inner),
                "residue_stability": stability,
                "nonzero_residue": max(abs(inner), abs(outer)) > 1.0e-8,
            }
        )
    return classified


def endpoint_classification(residue_nodes: int) -> dict[str, Any]:
    soft_direction = M5017.direction(0.43, 0.18)
    decay_direction = M5017.direction(0.71, 0.59)
    scattering_cosine = complex(1.5, 0.08)
    channel_function = lambda unit_circle: endpoint_channels(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    rows, maximum_fit_residual = channel_root_rows(channel_function)
    groups = group_roots(rows)
    integrand = lambda unit_circle: M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    classified = classify_groups(groups, integrand, residue_nodes)
    channel_at = lambda cosine, unit_circle: endpoint_channels(
        soft_direction, decay_direction, cosine, unit_circle
    )
    tracks: list[dict[str, Any]] = []
    for label in sorted(set(row["channel"] for row in rows)):
        tracks.extend(
            track_channel_roots(
                label,
                channel_at,
                complex(0.3, 0.0),
                scattering_cosine,
            )
        )
    attach_ownership(classified, tracks)
    bracket_roots = M5022.bracket_roots(
        soft_direction, decay_direction, scattering_cosine
    )
    nonzero = [row for row in classified if row["nonzero_residue"]]
    uncovered = [
        row
        for row in nonzero
        if not any(
            abs(complex(row["root"]) - root)
            < 5.0e-6 * max(1.0, abs(root))
            for root in bracket_roots.values()
        )
    ]
    return {
        "scattering_cosine": str(scattering_cosine),
        "soft_direction": soft_direction.tolist(),
        "decay_direction": decay_direction.tolist(),
        "candidate_channel_roots": len(rows),
        "coincident_root_groups": len(groups),
        "maximum_laurent_fit_relative_residual": maximum_fit_residual,
        "classified_groups": classified,
        "channel_root_tracks": tracks,
        "ownership_changing_branch_count": sum(
            track["ownership_changed"] for track in tracks
        ),
        "ownership_changing_nonzero_group_count": sum(
            row["nonzero_residue"] and row["ownership_change"]
            for row in classified
        ),
        "nonzero_residue_group_count": len(nonzero),
        "nonzero_residue_roots_not_present_in_spinor_root_set": len(uncovered),
    }


def finite_classification(residue_nodes: int) -> dict[str, Any]:
    internal = M5017.sequential_three_body(
        0.37,
        M5017.direction(0.31, 0.73),
        M5017.direction(0.64, 0.27),
    )
    scattering_cosine = complex(1.5, 0.08)
    channel_function = lambda unit_circle: finite_channels(
        internal, scattering_cosine, unit_circle
    )
    rows, maximum_fit_residual = channel_root_rows(channel_function)
    groups = group_roots(rows)
    integrand = lambda unit_circle: M5023.causal_hhh_reduced_product(
        rotate_internal(internal, unit_circle),
        scattering_cosine,
        0.0,
        0.0,
    )
    classified = classify_groups(groups, integrand, residue_nodes)
    return {
        "scattering_cosine": str(scattering_cosine),
        "soft_energy": 0.37,
        "candidate_channel_roots": len(rows),
        "coincident_root_groups": len(groups),
        "maximum_laurent_fit_relative_residual": maximum_fit_residual,
        "classified_groups": classified,
        "nonzero_residue_group_count": sum(
            row["nonzero_residue"] for row in classified
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residue-nodes", type=int, default=96)
    parser.add_argument(
        "--sector", choices=("none", "endpoint", "finite", "both"), default="endpoint"
    )
    parser.add_argument("--transport-smoke", action="store_true")
    parser.add_argument("--coupled-sector-gate", action="store_true")
    parser.add_argument("--soft-averaged-sector-gate", action="store_true")
    parser.add_argument("--power", type=int, default=3)
    parser.add_argument("--seeds", default="50241,50242")
    parser.add_argument("--base-nodes", type=int, default=64)
    parser.add_argument("--azimuth-nodes", type=int, default=128)
    parser.add_argument("--tracking-steps", type=int, default=41)
    arguments = parser.parse_args()
    result: dict[str, Any] = {}
    if arguments.sector in {"endpoint", "both"}:
        result["endpoint"] = endpoint_classification(arguments.residue_nodes)
    if arguments.sector in {"finite", "both"}:
        result["finite_x"] = finite_classification(arguments.residue_nodes)
    if arguments.transport_smoke:
        result["transported_endpoint_smoke"] = transported_endpoint_smoke(
            arguments.power,
            tuple(int(value) for value in arguments.seeds.split(",")),
            arguments.base_nodes,
            arguments.residue_nodes,
            arguments.tracking_steps,
        )
    if arguments.coupled_sector_gate:
        result["coupled_sector_endpoint_gate"] = coupled_sector_endpoint_gate(
            arguments.power,
            tuple(int(value) for value in arguments.seeds.split(",")),
            arguments.base_nodes,
            arguments.residue_nodes,
        )
    if arguments.soft_averaged_sector_gate:
        result["soft_averaged_sector_gate"] = soft_averaged_sector_gate(
            arguments.power,
            tuple(int(value) for value in arguments.seeds.split(",")),
            arguments.azimuth_nodes,
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
