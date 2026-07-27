from __future__ import annotations

import argparse
import cmath
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment


POST = Path(__file__).resolve().parents[1]
SCRIPT_5029 = (
    POST
    / "scripts"
    / "Y5_R2FR_5029_finite_x_cross_source_collision_map.py"
)
REFERENCE_COSINE = complex(0.3, 0.0)
TARGET_COSINE = complex(1.5, 0.08)
SOFT_ENERGY = 0.37
SOFT_COSINE = 0.23
DECAY_COSINE = -0.31
ENDPOINT_COLLISION_PAIRS = {
    tuple(sorted(("direct:g1:minus_u", "direct:g1:minus_v"))),
    tuple(sorted(("direct:g2:plus_u", "direct:g2:plus_v"))),
}
PROJECTIVE_TRACKING_LIMIT = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5029 = load_module("mts_5029_for_5030", SCRIPT_5029)
M5028 = M5029.M5028


def lifted_log(value: complex, reference: complex) -> complex:
    principal = cmath.log(value)
    turn = round((reference.imag - principal.imag) / (2.0 * math.pi))
    return principal + 2.0j * math.pi * turn


def chordal_distance(first: complex, second: complex) -> float:
    return abs(first - second) / math.sqrt(
        (1.0 + abs(first) ** 2) * (1.0 + abs(second) ** 2)
    )


def homotopy_cosines(
    steps: int, regulator: float, path_kind: str
) -> list[complex]:
    if steps < 2:
        raise ValueError("homotopy requires at least two steps")
    if regulator <= 0.0:
        raise ValueError("Feynman regulator must be positive")
    start = complex(REFERENCE_COSINE.real, regulator)
    if path_kind == "feynman":
        horizontal_steps = steps // 2
        vertical_steps = steps - horizontal_steps
        start_real = REFERENCE_COSINE.real
        target_real = TARGET_COSINE.real
        rows = [
            complex(
                start_real
                + index
                / horizontal_steps
                * (target_real - start_real),
                regulator,
            )
            for index in range(horizontal_steps + 1)
        ]
        rows.extend(
            complex(
                target_real,
                regulator
                + index
                / vertical_steps
                * (TARGET_COSINE.imag - regulator),
            )
            for index in range(1, vertical_steps + 1)
        )
        return rows
    rows: list[complex] = []
    for index in range(steps + 1):
        fraction = index / steps
        if path_kind == "direct":
            value = start + fraction * (TARGET_COSINE - start)
        elif fraction <= 0.5:
            leg_fraction = 2.0 * fraction
            value = complex(
                REFERENCE_COSINE.real,
                regulator
                + leg_fraction * (TARGET_COSINE.imag - regulator),
            )
        else:
            leg_fraction = 2.0 * fraction - 1.0
            value = complex(
                REFERENCE_COSINE.real
                + leg_fraction
                * (TARGET_COSINE.real - REFERENCE_COSINE.real),
                TARGET_COSINE.imag,
            )
        rows.append(value)
    return rows


def physical_chambers() -> tuple[list[dict[str, Any]], list[dict[str, bool]]]:
    boundaries = M5028.physical_relative_boundaries(
        SOFT_ENERGY, SOFT_COSINE, DECAY_COSINE
    )
    if not boundaries:
        boundaries = [
            {
                "angle": 0.0,
                "root": 1.0 + 0.0j,
                "equations": [],
                "synthetic": True,
            }
        ]
    ownerships: list[dict[str, bool]] = []
    for index, boundary in enumerate(boundaries):
        next_index = (index + 1) % len(boundaries)
        start_angle = float(boundary["angle"])
        end_angle = float(boundaries[next_index]["angle"])
        if next_index == 0:
            end_angle += 2.0 * math.pi
        ownerships.append(
            M5028.chamber_ownership(
                SOFT_ENERGY,
                complex(SOFT_COSINE, 0.0),
                complex(DECAY_COSINE, 0.0),
                cmath.exp(0.5j * (start_angle + end_angle)),
            )
        )
    return boundaries, ownerships


def endpoint_log_paths(
    boundaries: list[dict[str, Any]],
    cosines: list[complex],
    tracking_steps: int,
) -> tuple[list[list[complex]], float, float]:
    if not cosines:
        raise ValueError("endpoint transport requires a non-empty path")
    paths: list[list[complex]] = []
    maximum_log_step = 0.0
    maximum_projective_step = 0.0
    for boundary in boundaries:
        reference = complex(0.0, float(boundary["angle"]))
        if boundary.get("synthetic"):
            paths.append([reference for _ in cosines])
            continue
        equation = boundary["equations"][0]
        start_roots = M5028.M5027.relative_azimuth_roots(
            SOFT_ENERGY,
            complex(SOFT_COSINE, 0.0),
            complex(DECAY_COSINE, 0.0),
            equation["external_sign"] * REFERENCE_COSINE,
            equation["hard_sign"],
        )[:2]
        start_eta = (start_roots[0] + start_roots[1]) / 2.0
        current_square_root = complex(boundary["root"] - start_eta)
        current_root = complex(boundary["root"])

        def advance(cosine: complex) -> tuple[complex, float]:
            nonlocal current_square_root, current_root
            roots = M5028.M5027.relative_azimuth_roots(
                SOFT_ENERGY,
                complex(SOFT_COSINE, 0.0),
                complex(DECAY_COSINE, 0.0),
                equation["external_sign"] * cosine,
                equation["hard_sign"],
            )[:2]
            eta = (roots[0] + roots[1]) / 2.0
            principal = complex(np.sqrt(eta * eta - 1.0 + 0.0j))
            current_square_root = min(
                (principal, -principal),
                key=lambda candidate: abs(candidate - current_square_root),
            )
            next_root = complex(eta + current_square_root)
            maximum_candidate = chordal_distance(current_root, next_root)
            current_root = next_root
            return next_root, maximum_candidate

        initial_steps = max(1, tracking_steps)
        for index in range(1, initial_steps + 1):
            fraction = index / initial_steps
            cosine = REFERENCE_COSINE + fraction * (
                cosines[0] - REFERENCE_COSINE
            )
            root, projective_step = advance(cosine)
            value = lifted_log(root, reference)
            maximum_log_step = max(
                maximum_log_step, abs(value - reference)
            )
            maximum_projective_step = max(
                maximum_projective_step, projective_step
            )
            reference = value
        values = [reference]
        for cosine in cosines[1:]:
            root, projective_step = advance(cosine)
            value = lifted_log(root, reference)
            maximum_log_step = max(
                maximum_log_step, abs(value - reference)
            )
            maximum_projective_step = max(
                maximum_projective_step, projective_step
            )
            reference = value
            values.append(reference)
        paths.append(values)
    return paths, maximum_log_step, maximum_projective_step


def collision_groups(
    scattering_cosine: complex, ownership: dict[str, bool]
) -> list[dict[str, Any]]:
    rationals = M5029.root_rationals(
        SOFT_ENERGY,
        SOFT_COSINE,
        DECAY_COSINE,
        scattering_cosine,
    )
    keys = sorted(rationals)
    candidates: list[dict[str, Any]] = []
    for first_index, first_key in enumerate(keys):
        for second_key in keys[first_index + 1 :]:
            if ownership[first_key] == ownership[second_key]:
                continue
            for root in M5029.collision_roots(
                rationals[first_key], rationals[second_key]
            ):
                candidates.append(
                    {"root": root, "pairs": [(first_key, second_key)]}
                )
    groups: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda row: abs(row["root"])):
        root = candidate["root"]
        group = next(
            (
                row
                for row in groups
                if abs(root - row["root"])
                < 2.0e-5 * max(1.0, abs(root), abs(row["root"]))
            ),
            None,
        )
        if group is None:
            groups.append(candidate)
        else:
            group["pairs"].extend(candidate["pairs"])
    return groups


def track_collision_groups(
    cosines: list[complex], ownership: dict[str, bool]
) -> tuple[list[dict[str, Any]], float]:
    initial = collision_groups(cosines[0], ownership)
    tracks = [
        {
            "logs": [cmath.log(group["root"])],
            "initial_pairs": group["pairs"],
            "target_pairs": group["pairs"],
        }
        for group in initial
    ]
    maximum_step = 0.0
    for cosine in cosines[1:]:
        groups = collision_groups(cosine, ownership)
        if len(groups) != len(tracks):
            raise RuntimeError(
                f"collision-group count changed {len(tracks)} -> {len(groups)}"
            )
        lifted: list[list[complex]] = []
        costs = np.empty((len(tracks), len(groups)), dtype=float)
        for track_index, track in enumerate(tracks):
            previous = track["logs"][-1]
            row: list[complex] = []
            for group_index, group in enumerate(groups):
                value = lifted_log(group["root"], previous)
                row.append(value)
                costs[track_index, group_index] = abs(value - previous)
            lifted.append(row)
        track_indices, group_indices = linear_sum_assignment(costs)
        assignment = dict(zip(track_indices.tolist(), group_indices.tolist()))
        for track_index, track in enumerate(tracks):
            group_index = assignment[track_index]
            value = lifted[track_index][group_index]
            maximum_step = max(
                maximum_step, abs(value - track["logs"][-1])
            )
            track["logs"].append(value)
            track["target_pairs"] = groups[group_index]["pairs"]
    return tracks, maximum_step


def track_opposite_pair_roots(
    rational_path: list[dict[str, tuple[M5029.Laurent, M5029.Laurent]]],
    ownership: dict[str, bool],
) -> tuple[
    list[dict[str, Any]],
    float,
    float,
    int,
    int,
    dict[str, Any] | None,
    dict[str, Any] | None,
]:
    keys = sorted(rational_path[0])
    tracks: list[dict[str, Any]] = []
    maximum_step = 0.0
    maximum_projective_step = 0.0
    pair_count = 0
    discarded_transient_roots = 0
    maximum_step_detail: dict[str, Any] | None = None
    maximum_projective_detail: dict[str, Any] | None = None
    for first_index, first_key in enumerate(keys):
        for second_key in keys[first_index + 1 :]:
            if ownership[first_key] == ownership[second_key]:
                continue
            pair = (first_key, second_key)
            pair_count += 1
            roots_path = [
                M5029.collision_roots(
                    rationals[first_key], rationals[second_key]
                )
                for rationals in rational_path
            ]
            persistent_count = min(len(roots) for roots in roots_path)
            anchor_index = next(
                index
                for index, roots in enumerate(roots_path)
                if len(roots) == persistent_count
            )
            anchor_logs = [
                cmath.log(root) for root in roots_path[anchor_index]
            ]

            def propagate(
                starting_logs: list[complex],
                root_sequence: list[list[complex]],
                path_indices: list[int],
                direction: str,
            ) -> tuple[
                list[list[complex]],
                float,
                float,
                int,
                dict[str, Any] | None,
                dict[str, Any] | None,
            ]:
                propagated = [[value] for value in starting_logs]
                local_maximum_step = 0.0
                local_maximum_projective_step = 0.0
                local_discarded = 0
                local_detail: dict[str, Any] | None = None
                local_projective_detail: dict[str, Any] | None = None
                previous_path_index = anchor_index
                for roots, path_index in zip(root_sequence, path_indices):
                    if len(roots) < len(propagated):
                        raise RuntimeError(
                            f"persistent pair root disappeared for {pair}: "
                            f"{len(propagated)} -> {len(roots)}"
                        )
                    local_discarded += len(roots) - len(propagated)
                    costs = np.empty(
                        (len(propagated), len(roots)), dtype=float
                    )
                    lifted: list[list[complex]] = []
                    for track_index, track in enumerate(propagated):
                        previous = track[-1]
                        previous_root = cmath.exp(previous)
                        row: list[complex] = []
                        for root_index, root in enumerate(roots):
                            value = lifted_log(root, previous)
                            row.append(value)
                            costs[track_index, root_index] = chordal_distance(
                                previous_root, root
                            )
                        lifted.append(row)
                    track_indices, root_indices = linear_sum_assignment(costs)
                    assignment = dict(
                        zip(track_indices.tolist(), root_indices.tolist())
                    )
                    for track_index, track in enumerate(propagated):
                        root_index = assignment[track_index]
                        value = lifted[track_index][root_index]
                        step_size = abs(value - track[-1])
                        projective_step = chordal_distance(
                            cmath.exp(track[-1]), roots[root_index]
                        )
                        if step_size > local_maximum_step:
                            local_maximum_step = step_size
                            local_detail = {
                                "pair": list(pair),
                                "direction": direction,
                                "from_path_index": previous_path_index,
                                "to_path_index": path_index,
                                "track_index": track_index,
                                "previous_log": str(track[-1]),
                                "next_log": str(value),
                                "step_size": step_size,
                                "root_count": len(roots),
                                "persistent_count": len(propagated),
                            }
                        if projective_step > local_maximum_projective_step:
                            local_maximum_projective_step = projective_step
                            local_projective_detail = {
                                "pair": list(pair),
                                "direction": direction,
                                "from_path_index": previous_path_index,
                                "to_path_index": path_index,
                                "track_index": track_index,
                                "previous_root": str(cmath.exp(track[-1])),
                                "next_root": str(roots[root_index]),
                                "step_size": projective_step,
                                "root_count": len(roots),
                                "persistent_count": len(propagated),
                            }
                        track.append(value)
                    previous_path_index = path_index
                return (
                    propagated,
                    local_maximum_step,
                    local_maximum_projective_step,
                    local_discarded,
                    local_detail,
                    local_projective_detail,
                )

            (
                forward,
                forward_step,
                forward_projective_step,
                forward_discarded,
                forward_detail,
                forward_projective_detail,
            ) = propagate(
                anchor_logs,
                roots_path[anchor_index + 1 :],
                list(range(anchor_index + 1, len(roots_path))),
                "forward",
            )
            (
                backward,
                backward_step,
                backward_projective_step,
                backward_discarded,
                backward_detail,
                backward_projective_detail,
            ) = propagate(
                anchor_logs,
                list(reversed(roots_path[:anchor_index])),
                list(reversed(range(anchor_index))),
                "backward",
            )
            pair_step = max(forward_step, backward_step)
            pair_detail = (
                forward_detail
                if forward_step >= backward_step
                else backward_detail
            )
            if pair_step > maximum_step:
                maximum_step = pair_step
                maximum_step_detail = pair_detail
            pair_projective_step = max(
                forward_projective_step, backward_projective_step
            )
            pair_projective_detail = (
                forward_projective_detail
                if forward_projective_step >= backward_projective_step
                else backward_projective_detail
            )
            if pair_projective_step > maximum_projective_step:
                maximum_projective_step = pair_projective_step
                maximum_projective_detail = pair_projective_detail
            discarded_transient_roots += (
                forward_discarded + backward_discarded
            )
            for track_index in range(persistent_count):
                logs = list(reversed(backward[track_index][1:]))
                logs.extend(forward[track_index])
                tracks.append(
                    {
                        "logs": logs,
                        "initial_pairs": [pair],
                        "target_pairs": [pair],
                    }
                )
    return (
        tracks,
        maximum_step,
        maximum_projective_step,
        pair_count,
        discarded_transient_roots,
        maximum_step_detail,
        maximum_projective_detail,
    )


def chamber_segment_logs(
    endpoint_paths: list[list[complex]], chamber_index: int
) -> tuple[list[complex], list[complex]]:
    start = endpoint_paths[chamber_index]
    next_index = (chamber_index + 1) % len(endpoint_paths)
    end = list(endpoint_paths[next_index])
    if next_index == 0:
        end = [value + 2.0j * math.pi for value in end]
    return start, end


def segment_coordinate(
    point: complex, start: complex, end: complex
) -> complex:
    return (point - start) / (end - start)


def segment_distance(
    point: complex, start: complex, end: complex
) -> tuple[float, float]:
    difference = end - start
    projection = (
        (point.real - start.real) * difference.real
        + (point.imag - start.imag) * difference.imag
    ) / max(abs(difference) ** 2, 1.0e-30)
    clipped = min(1.0, max(0.0, projection))
    closest = start + clipped * difference
    return abs(point - closest), projection


def surface_crossings(
    tracks: list[dict[str, Any]],
    start_logs: list[complex],
    end_logs: list[complex],
) -> tuple[list[dict[str, Any]], int]:
    crossings: list[dict[str, Any]] = []
    radially_excluded_transitions = 0
    for track_index, track in enumerate(tracks):
        for copy_index in range(-2, 3):
            offset = 2.0j * math.pi * copy_index
            coordinates = [
                segment_coordinate(
                    point + offset,
                    start_logs[index],
                    end_logs[index],
                )
                for index, point in enumerate(track["logs"])
            ]
            for step in range(len(coordinates) - 1):
                first_log = track["logs"][step] + offset
                second_log = track["logs"][step + 1] + offset
                contour_reals = (
                    start_logs[step].real,
                    end_logs[step].real,
                    start_logs[step + 1].real,
                    end_logs[step + 1].real,
                )
                safely_outside = (
                    first_log.real > max(contour_reals) + 0.25
                    and second_log.real > max(contour_reals) + 0.25
                )
                safely_inside = (
                    first_log.real < min(contour_reals) - 0.25
                    and second_log.real < min(contour_reals) - 0.25
                )
                if (safely_outside or safely_inside) and chordal_distance(
                    cmath.exp(first_log), cmath.exp(second_log)
                ) < PROJECTIVE_TRACKING_LIMIT:
                    radially_excluded_transitions += 1
                    continue
                first = coordinates[step]
                second = coordinates[step + 1]
                if first.imag * second.imag >= 0.0:
                    continue
                fraction = first.imag / (first.imag - second.imag)
                along = first.real + fraction * (second.real - first.real)
                if not 1.0e-3 < along < 1.0 - 1.0e-3:
                    continue
                winding = 1 if first.imag > 0.0 else -1
                crossings.append(
                    {
                        "track_index": track_index,
                        "copy_index": copy_index,
                        "step_fraction": (step + fraction)
                        / (len(coordinates) - 1),
                        "segment_fraction": along,
                        "winding_correction": winding,
                        "target_root": str(cmath.exp(track["logs"][-1])),
                        "initial_pairs": [
                            list(pair) for pair in track["initial_pairs"]
                        ],
                        "target_pairs": [
                            list(pair) for pair in track["target_pairs"]
                        ],
                    }
                )
    return crossings, radially_excluded_transitions


def grouped_surface_crossings(
    crossings: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    groups: list[dict[str, Any]] = []
    consistent = True
    for crossing in sorted(
        crossings,
        key=lambda row: (row["step_fraction"], row["segment_fraction"]),
    ):
        root = complex(crossing["target_root"])
        group = next(
            (
                row
                for row in groups
                if abs(root - complex(row["target_root"]))
                < 2.0e-5
                * max(1.0, abs(root), abs(complex(row["target_root"])))
                and abs(
                    crossing["step_fraction"] - row["step_fraction"]
                )
                < 0.03
                and abs(
                    crossing["segment_fraction"]
                    - row["segment_fraction"]
                )
                < 0.03
            ),
            None,
        )
        if group is None:
            group = dict(crossing)
            group["representing_pairs"] = list(crossing["target_pairs"])
            group["multiplicity"] = 1
            groups.append(group)
            continue
        if group["winding_correction"] != crossing["winding_correction"]:
            consistent = False
        group["representing_pairs"].extend(crossing["target_pairs"])
        group["multiplicity"] += 1
    for group in groups:
        group["representing_pairs"] = [
            list(pair)
            for pair in sorted(
                {tuple(pair) for pair in group["representing_pairs"]}
            )
        ]
        group.pop("initial_pairs", None)
        group.pop("target_pairs", None)
    return groups, consistent


def unique_target_tracks(
    tracks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for track in tracks:
        root = cmath.exp(track["logs"][-1])
        group = next(
            (
                row
                for row in groups
                if abs(root - cmath.exp(row["logs"][-1]))
                < 2.0e-5
                * max(
                    1.0,
                    abs(root),
                    abs(cmath.exp(row["logs"][-1])),
                )
            ),
            None,
        )
        if group is None:
            groups.append(
                {
                    "logs": track["logs"],
                    "target_pairs": list(track["target_pairs"]),
                }
            )
        else:
            group["target_pairs"].extend(track["target_pairs"])
    return groups


def nearest_target_obstacles(
    tracks: list[dict[str, Any]],
    start: complex,
    end: complex,
    limit: int = 12,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for track_index, track in enumerate(tracks):
        for copy_index in range(-2, 3):
            point = track["logs"][-1] + 2.0j * math.pi * copy_index
            distance, projection = segment_distance(point, start, end)
            if not -0.25 < projection < 1.25:
                continue
            rows.append(
                {
                    "track_index": track_index,
                    "copy_index": copy_index,
                    "log_distance": distance,
                    "segment_projection": projection,
                    "target_root": str(cmath.exp(track["logs"][-1])),
                    "target_pairs": [
                        list(pair) for pair in track["target_pairs"]
                    ],
                }
            )
    rows.sort(key=lambda row: row["log_distance"])
    return rows[:limit]


def global_chamber_value(
    relative_circle: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    global_residue_nodes: int,
) -> complex:
    soft_direction, decay_direction, internal = M5028.event_geometry(
        SOFT_ENERGY,
        complex(SOFT_COSINE, 0.0),
        complex(DECAY_COSINE, 0.0),
        relative_circle,
    )
    return M5028.fixed_ownership_global_cycle(
        SOFT_ENERGY,
        soft_direction,
        decay_direction,
        internal,
        TARGET_COSINE,
        ownership,
        global_nodes,
        global_residue_nodes,
    )[0]


def relative_local_residue(
    root: complex,
    radius: float,
    nodes: int,
    ownership: dict[str, bool],
    global_nodes: int,
    global_residue_nodes: int,
) -> complex:
    total = 0.0j
    for index in range(nodes):
        phase = cmath.exp(
            2.0j * math.pi * (index + 0.317) / nodes
        )
        relative_circle = root + radius * phase
        total += (
            global_chamber_value(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            / relative_circle
            * radius
            * phase
        )
    return total / nodes


def collision_local_global_residue(
    relative_circle: complex,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    global_residue_nodes: int,
) -> complex:
    soft_direction, decay_direction, internal = M5028.event_geometry(
        SOFT_ENERGY,
        complex(SOFT_COSINE, 0.0),
        complex(DECAY_COSINE, 0.0),
        relative_circle,
    )
    groups = M5028.fixed_ownership_groups(
        internal,
        soft_direction,
        decay_direction,
        TARGET_COSINE,
        ownership,
    )
    owned_labels = {
        label
        for pair in collision_pairs
        for label in pair
        if ownership[label]
    }
    selected_groups = [
        group
        for group in groups
        if owned_labels.intersection(group["labels"])
    ]
    if not selected_groups or any(
        not group["desired_inside"] for group in selected_groups
    ):
        raise RuntimeError(
            "collision pair does not select a unique causally owned branch"
        )
    evaluator = lambda unit_circle: M5028.M5026.finite_plus_integrand(
        internal,
        SOFT_ENERGY,
        soft_direction,
        decay_direction,
        TARGET_COSINE,
        unit_circle,
    )
    total = 0.0j
    for group in selected_groups:
        root = complex(group["root"])
        separations = [
            abs(root - complex(other["root"]))
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations)
        if safe_scale <= 0.0:
            raise RuntimeError("degenerate local global-residue radius")
        total += M5028.M5024.local_residue(
            evaluator,
            root,
            0.15 * safe_scale,
            max(24, global_residue_nodes),
        )
    return total


def pair_local_relative_residue(
    root: complex,
    radius: float,
    nodes: int,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    global_residue_nodes: int,
) -> complex:
    total = 0.0j
    for index in range(nodes):
        phase = cmath.exp(2.0j * math.pi * (index + 0.317) / nodes)
        relative_circle = root + radius * phase
        total += (
            collision_local_global_residue(
                relative_circle,
                collision_pairs,
                ownership,
                global_residue_nodes,
            )
            / relative_circle
            * radius
            * phase
        )
    return total / nodes


def nearest_log_copy_to_segment(
    root: complex, start: complex, end: complex
) -> tuple[complex, float, float, int]:
    principal = cmath.log(root)
    candidates: list[tuple[float, float, complex, int]] = []
    for copy_index in range(-3, 4):
        value = principal + 2.0j * math.pi * copy_index
        distance, projection = segment_distance(value, start, end)
        candidates.append((distance, projection, value, copy_index))
    distance, projection, value, copy_index = min(
        candidates, key=lambda row: row[0]
    )
    return value, distance, projection, copy_index


def chamber_residue_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    target_groups = collision_groups(TARGET_COSINE, ownership)
    all_roots = [complex(group["root"]) for group in target_groups]
    selected: list[dict[str, Any]] = []
    for group in target_groups:
        root = complex(group["root"])
        log_point, distance, projection, copy_index = (
            nearest_log_copy_to_segment(root, start, end)
        )
        near_path = (
            distance < model_distance
            and -0.25 < projection < 1.25
        )
        required = any(
            abs(root - candidate)
            < 2.0e-5 * max(1.0, abs(root), abs(candidate))
            for candidate in required_roots
        )
        if not near_path and not required:
            continue
        selected.append(
            {
                "root": root,
                "pairs": group["pairs"],
                "log_point": log_point,
                "log_distance": distance,
                "segment_projection": projection,
                "copy_index": copy_index,
                "near_path": near_path,
                "required_for_homotopy": required,
            }
        )
    catalog: list[dict[str, Any]] = []
    all_stable = True
    for row in selected:
        root = row["root"]
        separations = [
            abs(root - other)
            for other in all_roots
            if abs(root - other)
            > 1.0e-7 * max(1.0, abs(root), abs(other))
        ]
        safe_scale = min([abs(root)] + separations)
        def residue_pair(
            outer_fraction: float,
        ) -> tuple[float, complex, complex, float, bool, bool]:
            radius = outer_fraction * safe_scale
            outer_value = pair_local_relative_residue(
                root,
                radius,
                max(32, relative_residue_nodes + 8),
                row["pairs"],
                ownership,
                max(32, global_residue_nodes + 8),
            )
            inner_value = pair_local_relative_residue(
                root,
                radius / 2.0,
                max(48, relative_residue_nodes + 24),
                row["pairs"],
                ownership,
                max(48, global_residue_nodes + 16),
            )
            pair_magnitude = max(abs(inner_value), abs(outer_value))
            pair_stability = abs(inner_value - outer_value) / max(
                pair_magnitude, 1.0e-30
            )
            pair_zero = pair_magnitude < 1.0e-7
            pair_stable = pair_zero or pair_stability < 5.0e-3
            return (
                radius,
                outer_value,
                inner_value,
                pair_stability,
                pair_zero,
                pair_stable,
            )

        (
            outer_radius,
            outer,
            inner,
            stability,
            numerically_zero,
            stable,
        ) = residue_pair(0.1)
        residue_contour_fraction = 0.1
        if not stable:
            (
                outer_radius,
                outer,
                inner,
                stability,
                numerically_zero,
                stable,
            ) = residue_pair(0.2)
            residue_contour_fraction = 0.2
        all_stable = all_stable and stable
        catalog.append(
            {
                **row,
                "outer_radius": outer_radius,
                "residue_method": "pair-local-double-residue-adaptive-v3",
                "residue_contour_fraction": residue_contour_fraction,
                "outer_residue": outer,
                "inner_residue": inner,
                "residue": 0.0j if numerically_zero else inner,
                "residue_stability": stability,
                "numerically_zero": numerically_zero,
                "stable": stable,
                "included_as_pole_model": row["near_path"]
                and not numerically_zero
                and stable,
            }
        )
    return catalog, all_stable


def continuous_straight_log_difference(
    start: complex, end: complex, pole: complex
) -> complex:
    start_vector = start - pole
    end_vector = end - pole
    phase_difference = cmath.phase(end_vector) - cmath.phase(start_vector)
    phase_difference = math.atan2(
        math.sin(phase_difference), math.cos(phase_difference)
    )
    return complex(
        math.log(abs(end_vector) / abs(start_vector)),
        phase_difference,
    )


def regularized_log_segment_integral(
    start: complex,
    end: complex,
    ownership: dict[str, bool],
    catalog: list[dict[str, Any]],
    order: int,
    global_nodes: int,
    global_residue_nodes: int,
) -> tuple[complex, int]:
    models = [row for row in catalog if row["included_as_pole_model"]]
    nodes, weights = M5028.gauss_rule(order)
    difference = end - start
    regularized = 0.0j
    for node, weight in zip(nodes, weights):
        log_point = start + node * difference
        value = global_chamber_value(
            cmath.exp(log_point),
            ownership,
            global_nodes,
            global_residue_nodes,
        )
        for model in models:
            value -= model["residue"] / (
                log_point - model["log_point"]
            )
        regularized += weight * value
    result = difference * regularized / (2.0j * math.pi)
    for model in models:
        result += (
            model["residue"]
            * continuous_straight_log_difference(
                start, end, model["log_point"]
            )
            / (2.0j * math.pi)
        )
    return result, len(models)


def collision_scaled_breakpoints(
    start: complex,
    end: complex,
    catalog: list[dict[str, Any]],
) -> list[float]:
    difference = end - start
    points = [0.0, 1.0]
    for row in catalog:
        projection = float(row["segment_projection"])
        width = float(row["log_distance"]) / max(abs(difference), 1.0e-30)
        for point in (
            projection - 4.0 * width,
            projection - width,
            projection,
            projection + width,
            projection + 4.0 * width,
        ):
            if 0.0 < point < 1.0:
                points.append(point)
    return sorted({round(point, 12) for point in points})


def composite_regularized_log_segment_integral(
    start: complex,
    end: complex,
    ownership: dict[str, bool],
    catalog: list[dict[str, Any]],
    order: int,
    global_nodes: int,
    global_residue_nodes: int,
) -> tuple[complex, int, int, int]:
    models = [row for row in catalog if row["included_as_pole_model"]]
    breakpoints = collision_scaled_breakpoints(start, end, catalog)
    nodes, weights = M5028.gauss_rule(order)
    difference = end - start
    regularized = 0.0j
    evaluation_count = 0
    for lower, upper in zip(breakpoints[:-1], breakpoints[1:]):
        local = 0.0j
        for node, weight in zip(nodes, weights):
            parameter = lower + (upper - lower) * float(node)
            log_point = start + parameter * difference
            value = global_chamber_value(
                cmath.exp(log_point),
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            for model in models:
                value -= model["residue"] / (
                    log_point - model["log_point"]
                )
            local += float(weight) * value
            evaluation_count += 1
        regularized += (upper - lower) * local
    result = difference * regularized / (2.0j * math.pi)
    for model in models:
        result += (
            model["residue"]
            * continuous_straight_log_difference(
                start, end, model["log_point"]
            )
            / (2.0j * math.pi)
        )
    return result, len(models), len(breakpoints) - 1, evaluation_count


def adaptive_collision_scaled_log_segment_integral(
    start: complex,
    end: complex,
    ownership: dict[str, bool],
    catalog: list[dict[str, Any]],
    high_order: int,
    global_nodes: int,
    global_residue_nodes: int,
    relative_tolerance: float,
    maximum_intervals: int,
) -> tuple[complex, int, int, int, float, bool]:
    models = [row for row in catalog if row["included_as_pole_model"]]
    breakpoints = collision_scaled_breakpoints(start, end, catalog)
    difference = end - start
    low_order = max(6, high_order // 2)
    low_nodes, low_weights = M5028.gauss_rule(low_order)
    high_nodes, high_weights = M5028.gauss_rule(high_order)
    evaluation_count = 0

    def regularized_value(parameter: float) -> complex:
        nonlocal evaluation_count
        log_point = start + parameter * difference
        value = global_chamber_value(
            cmath.exp(log_point),
            ownership,
            global_nodes,
            global_residue_nodes,
        )
        for model in models:
            value -= model["residue"] / (
                log_point - model["log_point"]
            )
        evaluation_count += 1
        return value

    def rule(
        lower: float,
        upper: float,
        nodes: np.ndarray,
        weights: np.ndarray,
    ) -> complex:
        local = 0.0j
        for node, weight in zip(nodes, weights):
            parameter = lower + (upper - lower) * float(node)
            local += float(weight) * regularized_value(parameter)
        return (
            difference
            * (upper - lower)
            * local
            / (2.0j * math.pi)
        )

    def segment(lower: float, upper: float, depth: int) -> dict[str, Any]:
        low = rule(lower, upper, low_nodes, low_weights)
        high = rule(lower, upper, high_nodes, high_weights)
        return {
            "lower": lower,
            "upper": upper,
            "depth": depth,
            "value": high,
            "error": abs(high - low),
        }

    segments = [
        segment(lower, upper, 0)
        for lower, upper in zip(breakpoints[:-1], breakpoints[1:])
    ]
    model_contribution = sum(
        (
            model["residue"]
            * continuous_straight_log_difference(
                start, end, model["log_point"]
            )
            / (2.0j * math.pi)
        )
        for model in models
    )

    def totals() -> tuple[complex, float, float]:
        value = sum((row["value"] for row in segments), 0.0j)
        error = sum(float(row["error"]) for row in segments)
        target = 1.0e-9 + relative_tolerance * max(
            abs(value + model_contribution), 1.0
        )
        return value, error, target

    value, error, target = totals()
    while error > target and len(segments) < maximum_intervals:
        candidates = [row for row in segments if row["depth"] < 14]
        if not candidates:
            break
        parent = max(candidates, key=lambda row: row["error"])
        midpoint = 0.5 * (parent["lower"] + parent["upper"])
        segments.remove(parent)
        segments.extend(
            (
                segment(parent["lower"], midpoint, parent["depth"] + 1),
                segment(midpoint, parent["upper"], parent["depth"] + 1),
            )
        )
        value, error, target = totals()
    result = value + model_contribution
    relative_error = error / max(abs(result), 1.0)
    return (
        result,
        len(models),
        len(segments),
        evaluation_count,
        relative_error,
        error <= target,
    )


def serialized_residue_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "root": str(row["root"]),
        "pairs": [list(pair) for pair in row["pairs"]],
        "log_point": str(row["log_point"]),
        "log_distance": row["log_distance"],
        "segment_projection": row["segment_projection"],
        "copy_index": row["copy_index"],
        "near_path": row["near_path"],
        "required_for_homotopy": row["required_for_homotopy"],
        "outer_radius": row["outer_radius"],
        "residue_method": row["residue_method"],
        "residue_contour_fraction": row["residue_contour_fraction"],
        "outer_residue": str(row["outer_residue"]),
        "inner_residue": str(row["inner_residue"]),
        "residue": str(row["residue"]),
        "residue_stability": row["residue_stability"],
        "numerically_zero": row["numerically_zero"],
        "stable": row["stable"],
        "included_as_pole_model": row["included_as_pole_model"],
    }


def fixed_event_integral_gate(
    homotopy: dict[str, Any],
    relative_orders: tuple[int, ...],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
    boundary_tracking_steps: int,
    relative_quadrature_mode: str = "global",
    relative_adaptive_tolerance: float = 5.0e-5,
    relative_adaptive_maximum_intervals: int = 1024,
) -> dict[str, Any]:
    if relative_quadrature_mode not in {
        "global",
        "collision_scaled_composite",
        "collision_scaled_adaptive",
    }:
        raise ValueError(
            f"unknown relative quadrature mode: {relative_quadrature_mode}"
        )
    boundaries, ownerships = physical_chambers()
    endpoint_paths: list[list[complex]] | None = None
    if not all(
        "target_start_log" in row and "target_end_log" in row
        for row in homotopy["chambers"]
    ):
        endpoint_paths, _, _ = endpoint_log_paths(
            boundaries, [TARGET_COSINE], boundary_tracking_steps
        )
    chamber_data: list[dict[str, Any]] = []
    all_residues_stable = True
    correction_total = 0.0j
    for chamber_index, ownership in enumerate(ownerships):
        homotopy_chamber = homotopy["chambers"][chamber_index]
        if "target_start_log" in homotopy_chamber:
            start = complex(homotopy_chamber["target_start_log"])
            end = complex(homotopy_chamber["target_end_log"])
        else:
            assert endpoint_paths is not None
            start = endpoint_paths[chamber_index][0]
            next_index = (chamber_index + 1) % len(boundaries)
            end = endpoint_paths[next_index][0]
            if next_index == 0:
                end += 2.0j * math.pi
        crossing_rows = homotopy["chambers"][chamber_index][
            "surface_crossings"
        ]
        required_roots = [
            complex(row["target_root"]) for row in crossing_rows
        ]
        catalog, residues_stable = chamber_residue_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
        all_residues_stable = all_residues_stable and residues_stable
        correction = 0.0j
        correction_rows: list[dict[str, Any]] = []
        for crossing in crossing_rows:
            root = complex(crossing["target_root"])
            match = min(catalog, key=lambda row: abs(row["root"] - root))
            matching_residual = abs(match["root"] - root) / max(
                1.0, abs(root), abs(match["root"])
            )
            if matching_residual > 2.0e-5:
                raise RuntimeError(
                    f"crossing root not found in residue catalog: {root}"
                )
            contribution = (
                crossing["winding_correction"] * match["residue"]
            )
            correction += contribution
            correction_rows.append(
                {
                    "target_root": str(root),
                    "winding_correction": crossing[
                        "winding_correction"
                    ],
                    "residue": str(match["residue"]),
                    "contribution": str(contribution),
                    "matching_residual": matching_residual,
                }
            )
        correction_total += correction
        chamber_data.append(
            {
                "chamber_index": chamber_index,
                "start_log": str(start),
                "end_log": str(end),
                "residue_catalog_internal": catalog,
                "residue_catalog": [
                    serialized_residue_row(row) for row in catalog
                ],
                "residues_stable": residues_stable,
                "topological_correction": str(correction),
                "correction_rows": correction_rows,
            }
        )
    order_rows: list[dict[str, Any]] = []
    for order in relative_orders:
        naive_total = 0.0j
        chamber_values: list[str] = []
        model_count = 0
        interval_count = 0
        evaluation_count = 0
        estimated_errors: list[float] = []
        adaptive_rows_converged = True
        for chamber_index, ownership in enumerate(ownerships):
            row = chamber_data[chamber_index]
            if relative_quadrature_mode == "global":
                value, count = regularized_log_segment_integral(
                    complex(row["start_log"]),
                    complex(row["end_log"]),
                    ownership,
                    row["residue_catalog_internal"],
                    order,
                    global_nodes,
                    global_residue_nodes,
                )
                intervals = 1
                evaluations = order
            elif relative_quadrature_mode == "collision_scaled_composite":
                value, count, intervals, evaluations = (
                    composite_regularized_log_segment_integral(
                        complex(row["start_log"]),
                        complex(row["end_log"]),
                        ownership,
                        row["residue_catalog_internal"],
                        order,
                        global_nodes,
                        global_residue_nodes,
                    )
                )
            else:
                (
                    value,
                    count,
                    intervals,
                    evaluations,
                    estimated_error,
                    adaptive_converged,
                ) = adaptive_collision_scaled_log_segment_integral(
                    complex(row["start_log"]),
                    complex(row["end_log"]),
                    ownership,
                    row["residue_catalog_internal"],
                    order,
                    global_nodes,
                    global_residue_nodes,
                    relative_adaptive_tolerance,
                    relative_adaptive_maximum_intervals,
                )
                estimated_errors.append(estimated_error)
                adaptive_rows_converged = (
                    adaptive_rows_converged and adaptive_converged
                )
            naive_total += value
            model_count += count
            interval_count += intervals
            evaluation_count += evaluations
            chamber_values.append(str(value))
        order_rows.append(
            {
                "relative_order": order,
                "regularized_naive_value": str(naive_total),
                "topological_correction": str(correction_total),
                "causally_corrected_value": str(
                    naive_total + correction_total
                ),
                "chamber_values": chamber_values,
                "pole_model_count": model_count,
                "composite_interval_count": interval_count,
                "relative_integrand_evaluation_count": evaluation_count,
                "maximum_adaptive_chamber_relative_error": (
                    max(estimated_errors) if estimated_errors else None
                ),
                "adaptive_quadrature_converged": adaptive_rows_converged,
            }
        )
    corrected_values = [
        complex(row["causally_corrected_value"]) for row in order_rows
    ]
    if len(corrected_values) >= 2:
        convergence_residual = abs(
            corrected_values[-1] - corrected_values[-2]
        ) / max(abs(corrected_values[-1]), 1.0)
    elif relative_quadrature_mode == "collision_scaled_adaptive":
        convergence_residual = float(
            order_rows[-1]["maximum_adaptive_chamber_relative_error"]
        )
    else:
        convergence_residual = math.inf
    strict_adaptive_quadrature_converged = bool(
        relative_quadrature_mode != "collision_scaled_adaptive"
        or all(
            bool(row["adaptive_quadrature_converged"])
            and float(row["maximum_adaptive_chamber_relative_error"])
            <= relative_adaptive_tolerance
            for row in order_rows
        )
    )
    for row in chamber_data:
        row.pop("residue_catalog_internal")
    return {
        "relative_orders": list(relative_orders),
        "global_nodes": global_nodes,
        "global_residue_nodes": global_residue_nodes,
        "relative_residue_nodes": relative_residue_nodes,
        "model_distance": model_distance,
        "relative_quadrature_mode": relative_quadrature_mode,
        "relative_quadrature_revision": (
            "collision-scaled-all-collisions-v2"
            if relative_quadrature_mode == "collision_scaled_composite"
            else (
                "collision-scaled-adaptive-v1"
                if relative_quadrature_mode == "collision_scaled_adaptive"
                else "global-v1"
            )
        ),
        "relative_adaptive_tolerance": relative_adaptive_tolerance,
        "relative_adaptive_maximum_intervals": (
            relative_adaptive_maximum_intervals
        ),
        "global_cycle_revision": "conditioned-subminimum-annulus-v5",
        "relative_residue_revision": "pair-local-double-residue-adaptive-v3",
        "chambers": chamber_data,
        "order_rows": order_rows,
        "all_residues_stable": all_residues_stable,
        "topological_correction": str(correction_total),
        "highest_order_value": str(corrected_values[-1]),
        "highest_two_order_relative_residual": convergence_residual,
        "strict_adaptive_quadrature_converged": (
            strict_adaptive_quadrature_converged
        ),
        "fixed_event_crossed_integral_converged": all_residues_stable
        and convergence_residual < 2.0e-3
        and strict_adaptive_quadrature_converged,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def homotopy_gate(
    steps: int,
    regulator: float,
    path_kind: str,
    boundary_tracking_steps: int,
) -> dict[str, Any]:
    cosines = homotopy_cosines(steps, regulator, path_kind)
    boundaries, ownerships = physical_chambers()
    (
        endpoints,
        maximum_boundary_step,
        maximum_boundary_projective_step,
    ) = endpoint_log_paths(
        boundaries, cosines, boundary_tracking_steps
    )
    rational_path = [
        M5029.root_rationals(
            SOFT_ENERGY,
            SOFT_COSINE,
            DECAY_COSINE,
            cosine,
        )
        for cosine in cosines
    ]
    chamber_rows: list[dict[str, Any]] = []
    maximum_assignment_step = 0.0
    maximum_projective_assignment_step = 0.0
    total_crossings = 0
    total_discarded_transient_roots = 0
    total_radially_excluded_transitions = 0
    all_crossing_groups_consistent = True
    maximum_assignment_detail: dict[str, Any] | None = None
    maximum_projective_assignment_detail: dict[str, Any] | None = None
    for chamber_index, ownership in enumerate(ownerships):
        (
            tracks,
            assignment_step,
            projective_assignment_step,
            pair_count,
            discarded_transient_roots,
            assignment_detail,
            projective_assignment_detail,
        ) = track_opposite_pair_roots(rational_path, ownership)
        total_discarded_transient_roots += discarded_transient_roots
        if assignment_step > maximum_assignment_step:
            maximum_assignment_step = assignment_step
            maximum_assignment_detail = (
                {"chamber_index": chamber_index, **assignment_detail}
                if assignment_detail is not None
                else None
            )
        if projective_assignment_step > maximum_projective_assignment_step:
            maximum_projective_assignment_step = projective_assignment_step
            maximum_projective_assignment_detail = (
                {
                    "chamber_index": chamber_index,
                    **projective_assignment_detail,
                }
                if projective_assignment_detail is not None
                else None
            )
        start_logs, end_logs = chamber_segment_logs(endpoints, chamber_index)
        raw_crossings, radially_excluded_transitions = surface_crossings(
            tracks, start_logs, end_logs
        )
        total_radially_excluded_transitions += radially_excluded_transitions
        crossings, crossing_groups_consistent = grouped_surface_crossings(
            raw_crossings
        )
        all_crossing_groups_consistent = (
            all_crossing_groups_consistent and crossing_groups_consistent
        )
        total_crossings += len(crossings)
        target_tracks = unique_target_tracks(tracks)
        chamber_rows.append(
            {
                "chamber_index": chamber_index,
                "start_physical_angle": float(
                    boundaries[chamber_index]["angle"]
                ),
                "end_physical_angle": float(
                    boundaries[(chamber_index + 1) % len(boundaries)][
                        "angle"
                    ]
                    + (2.0 * math.pi if chamber_index + 1 == len(boundaries) else 0.0)
                ),
                "opposite_ownership_pair_count": pair_count,
                "discarded_transient_root_samples": discarded_transient_roots,
                "pair_root_track_count": len(tracks),
                "unique_target_collision_count": len(target_tracks),
                "surface_crossing_count": len(crossings),
                "raw_pair_crossing_count": len(raw_crossings),
                "radially_excluded_transition_count": (
                    radially_excluded_transitions
                ),
                "crossing_groups_consistent": crossing_groups_consistent,
                "surface_crossings": crossings,
                "nearest_target_obstacles": nearest_target_obstacles(
                    target_tracks,
                    start_logs[-1],
                    end_logs[-1],
                ),
                "target_start_root": str(cmath.exp(start_logs[-1])),
                "target_end_root": str(cmath.exp(end_logs[-1])),
                "target_start_log": str(start_logs[-1]),
                "target_end_log": str(end_logs[-1]),
            }
        )
    collision_tracking_passed = (
        maximum_projective_assignment_step < PROJECTIVE_TRACKING_LIMIT
    )
    boundary_tracking_passed = (
        maximum_boundary_projective_step < PROJECTIVE_TRACKING_LIMIT
    )
    return {
        "soft_energy": SOFT_ENERGY,
        "soft_cosine": SOFT_COSINE,
        "decay_cosine": DECAY_COSINE,
        "reference_cosine": str(REFERENCE_COSINE),
        "target_cosine": str(TARGET_COSINE),
        "regulator": regulator,
        "path_kind": path_kind,
        "path_parameterization": (
            "piecewise linear +i0 with projective root tracking"
            if path_kind == "feynman"
            else "piecewise linear"
        ),
        "homotopy_steps": steps,
        "maximum_collision_assignment_log_step": maximum_assignment_step,
        "maximum_collision_assignment_detail": maximum_assignment_detail,
        "maximum_collision_assignment_projective_step": (
            maximum_projective_assignment_step
        ),
        "maximum_collision_assignment_projective_detail": (
            maximum_projective_assignment_detail
        ),
        "maximum_boundary_assignment_log_step": maximum_boundary_step,
        "maximum_boundary_assignment_projective_step": (
            maximum_boundary_projective_step
        ),
        "projective_tracking_limit": PROJECTIVE_TRACKING_LIMIT,
        "collision_assignment_tracking_passed": collision_tracking_passed,
        "boundary_assignment_tracking_passed": boundary_tracking_passed,
        "assignment_tracking_passed": collision_tracking_passed
        and boundary_tracking_passed,
        "total_surface_crossings": total_crossings,
        "discarded_transient_root_samples": total_discarded_transient_roots,
        "radially_excluded_transition_count": (
            total_radially_excluded_transitions
        ),
        "crossing_groups_consistent": all_crossing_groups_consistent,
        "chambers": chamber_rows,
        "full_off_unit_collision_homotopy_enumerated": True,
        "relative_residue_corrections_evaluated": False,
        "fixed_event_crossed_integral_converged": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=96)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument(
        "--path-kind",
        choices=("feynman", "raised", "direct"),
        default="feynman",
    )
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--integral-gate", action="store_true")
    parser.add_argument("--relative-orders", default="12,20,32")
    parser.add_argument("--global-nodes", type=int, default=12)
    parser.add_argument("--global-residue-nodes", type=int, default=12)
    parser.add_argument("--relative-residue-nodes", type=int, default=12)
    parser.add_argument("--model-distance", type=float, default=0.65)
    parser.add_argument(
        "--relative-quadrature-mode",
        choices=(
            "global",
            "collision_scaled_composite",
            "collision_scaled_adaptive",
        ),
        default="global",
    )
    parser.add_argument("--relative-adaptive-tolerance", type=float, default=5.0e-5)
    parser.add_argument(
        "--relative-adaptive-maximum-intervals", type=int, default=1024
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = homotopy_gate(
        arguments.steps,
        arguments.regulator,
        arguments.path_kind,
        arguments.boundary_tracking_steps,
    )
    if arguments.integral_gate:
        integral_result = fixed_event_integral_gate(
            result,
            tuple(
                int(value) for value in arguments.relative_orders.split(",")
            ),
            arguments.global_nodes,
            arguments.global_residue_nodes,
            arguments.relative_residue_nodes,
            arguments.model_distance,
            arguments.boundary_tracking_steps,
            arguments.relative_quadrature_mode,
            arguments.relative_adaptive_tolerance,
            arguments.relative_adaptive_maximum_intervals,
        )
        result["fixed_event_integral_gate"] = integral_result
        result["relative_residue_corrections_evaluated"] = True
        result["fixed_event_crossed_integral_converged"] = integral_result[
            "fixed_event_crossed_integral_converged"
        ]
    serialized = json.dumps(result, indent=2)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
