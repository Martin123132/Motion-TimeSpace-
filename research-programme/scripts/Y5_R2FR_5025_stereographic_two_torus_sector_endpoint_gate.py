from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any, Callable

import mpmath as mp
import numpy as np
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5024 = POST / "scripts" / "Y5_R2FR_5024_physical_propagator_pole_classification_and_coupled_cycle_transport.py"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5024 = load_module("mts_5024_for_5025", SCRIPT_5024)
M5022 = M5024.M5022
M5017 = M5024.M5017
SEGMENTS = ("north", "middle", "south")
GLOBAL_ROOT_LABELS = ("plus_u", "plus_v", "minus_u", "minus_v")
REFERENCE_COSINE = 0.3


def reference_segment_bounds(segment: str, reference_cosine: float) -> tuple[float, float]:
    lower_pinch = (1.0 - reference_cosine) / 2.0
    upper_pinch = (1.0 + reference_cosine) / 2.0
    return {
        "north": (0.0, lower_pinch),
        "middle": (lower_pinch, upper_pinch),
        "south": (upper_pinch, 1.0),
    }[segment]


def clip_polygon(
    polygon: list[np.ndarray],
    value: Callable[[np.ndarray], float],
    tolerance: float = 1.0e-13,
) -> list[np.ndarray]:
    if not polygon:
        return []
    result: list[np.ndarray] = []
    previous = polygon[-1]
    previous_value = value(previous)
    previous_inside = previous_value >= -tolerance
    for current in polygon:
        current_value = value(current)
        current_inside = current_value >= -tolerance
        if current_inside != previous_inside:
            fraction = previous_value / (previous_value - current_value)
            result.append(previous + fraction * (current - previous))
        if current_inside:
            result.append(current)
        previous = current
        previous_value = current_value
        previous_inside = current_inside
    return result


def polygon_area(polygon: list[np.ndarray]) -> float:
    return 0.5 * abs(
        sum(
            polygon[index][0] * polygon[(index + 1) % len(polygon)][1]
            - polygon[(index + 1) % len(polygon)][0] * polygon[index][1]
            for index in range(len(polygon))
        )
    )


def transported_triangles(reference_cosine: float = 0.3) -> list[dict[str, Any]]:
    triangles: list[dict[str, Any]] = []
    unit_square = [
        np.asarray([0.0, 0.0]),
        np.asarray([1.0, 0.0]),
        np.asarray([1.0, 1.0]),
        np.asarray([0.0, 1.0]),
    ]
    for soft_segment in SEGMENTS:
        soft_lower, soft_upper = reference_segment_bounds(
            soft_segment, reference_cosine
        )
        soft_width = soft_upper - soft_lower
        for decay_segment in SEGMENTS:
            decay_lower, decay_upper = reference_segment_bounds(
                decay_segment, reference_cosine
            )
            decay_width = decay_upper - decay_lower

            def coordinates(point: np.ndarray) -> tuple[float, float]:
                return (
                    soft_lower + soft_width * point[0],
                    decay_lower + decay_width * point[1],
                )

            for soft_less in (True, False):
                for sum_less in (True, False):
                    polygon = list(unit_square)
                    polygon = clip_polygon(
                        polygon,
                        lambda point, desired=soft_less: (
                            (coordinates(point)[1] - coordinates(point)[0])
                            if desired
                            else (coordinates(point)[0] - coordinates(point)[1])
                        ),
                    )
                    polygon = clip_polygon(
                        polygon,
                        lambda point, desired=sum_less: (
                            (1.0 - sum(coordinates(point)))
                            if desired
                            else (sum(coordinates(point)) - 1.0)
                        ),
                    )
                    if len(polygon) < 3 or polygon_area(polygon) < 1.0e-14:
                        continue
                    for vertex_index in range(1, len(polygon) - 1):
                        vertices = [
                            polygon[0],
                            polygon[vertex_index],
                            polygon[vertex_index + 1],
                        ]
                        area = polygon_area(vertices)
                        if area < 1.0e-14:
                            continue
                        triangles.append(
                            {
                                "soft_segment": soft_segment,
                                "decay_segment": decay_segment,
                                "soft_less_than_decay": soft_less,
                                "sum_less_than_one": sum_less,
                                "vertices": vertices,
                                "area": area,
                            }
                        )
    return triangles


def middle_branch_layer_breaks(
    scattering_cosine: complex,
) -> list[float]:
    if abs(scattering_cosine) < 1.0e-14:
        return [0.0, 1.0]
    branch_preimages = (
        (scattering_cosine - 1.0) / (2.0 * scattering_cosine),
        (scattering_cosine + 1.0) / (2.0 * scattering_cosine),
    )
    breaks = [0.0, 1.0]
    for preimage in branch_preimages:
        centre = float(preimage.real)
        width = float(abs(preimage.imag))
        if not 0.0 < centre < 1.0 or width < 1.0e-8:
            continue
        for multiple in (-3.0, -1.0, 0.0, 1.0, 3.0):
            candidate = centre + multiple * width
            if 0.0 < candidate < 1.0:
                breaks.append(candidate)
    return sorted(
        value
        for index, value in enumerate(sorted(breaks))
        if index == 0 or abs(value - sorted(breaks)[index - 1]) > 1.0e-12
    )


def branch_layer_refined_triangles(
    triangles: list[dict[str, Any]], scattering_cosine: complex
) -> list[dict[str, Any]]:
    middle_breaks = middle_branch_layer_breaks(scattering_cosine)
    if len(middle_breaks) == 2:
        return triangles
    refined: list[dict[str, Any]] = []
    for parent_index, triangle in enumerate(triangles):
        soft_breaks = (
            middle_breaks
            if triangle["soft_segment"] == "middle"
            else [0.0, 1.0]
        )
        decay_breaks = (
            middle_breaks
            if triangle["decay_segment"] == "middle"
            else [0.0, 1.0]
        )
        for soft_lower, soft_upper in zip(
            soft_breaks[:-1], soft_breaks[1:]
        ):
            for decay_lower, decay_upper in zip(
                decay_breaks[:-1], decay_breaks[1:]
            ):
                polygon = list(triangle["vertices"])
                polygon = clip_polygon(
                    polygon, lambda point: point[0] - soft_lower
                )
                polygon = clip_polygon(
                    polygon, lambda point: soft_upper - point[0]
                )
                polygon = clip_polygon(
                    polygon, lambda point: point[1] - decay_lower
                )
                polygon = clip_polygon(
                    polygon, lambda point: decay_upper - point[1]
                )
                if len(polygon) < 3 or polygon_area(polygon) < 1.0e-14:
                    continue
                for vertex_index in range(1, len(polygon) - 1):
                    vertices = [
                        polygon[0],
                        polygon[vertex_index],
                        polygon[vertex_index + 1],
                    ]
                    area = polygon_area(vertices)
                    if area < 1.0e-14:
                        continue
                    child = dict(triangle)
                    child.update(
                        {
                            "vertices": vertices,
                            "area": area,
                            "parent_triangle_index": parent_index,
                        }
                    )
                    refined.append(child)
    return refined


def triangle_point(
    vertices: list[np.ndarray], first: float, second: float
) -> np.ndarray:
    radial = math.sqrt(first)
    weights = (1.0 - radial, radial * (1.0 - second), radial * second)
    return sum(
        weight * vertex for weight, vertex in zip(weights, vertices)
    )


def relative_roots(
    soft_direction: np.ndarray, decay_direction: np.ndarray
) -> dict[str, complex]:
    soft_holomorphic, _ = M5024.stereographic_pair(soft_direction)
    decay_holomorphic, _ = M5024.stereographic_pair(decay_direction)
    radial_product = soft_holomorphic * decay_holomorphic
    return {
        "plus_soft": soft_holomorphic / decay_holomorphic,
        "plus_decay": decay_holomorphic / soft_holomorphic,
        "minus_product": -radial_product,
        "minus_inverse": -1.0 / radial_product,
    }


def relative_desired_labels(
    soft_less_than_decay: bool, sum_less_than_one: bool
) -> tuple[str, str]:
    return (
        "plus_soft" if soft_less_than_decay else "plus_decay",
        "minus_product" if sum_less_than_one else "minus_inverse",
    )


def global_desired_labels(segment: str) -> set[str]:
    return {
        "plus_v" if segment == "north" else "plus_u",
        "minus_u" if segment == "south" else "minus_v",
    }


def relative_cycle_groups(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    start_soft_direction: np.ndarray,
    start_decay_direction: np.ndarray,
    start_scattering_cosine: complex,
    soft_segment: str,
    decay_segment: str,
) -> list[dict[str, Any]]:
    target_direct = relative_roots(soft_direction, decay_direction)
    start_direct = relative_roots(
        start_soft_direction, start_decay_direction
    )
    rows: list[dict[str, Any]] = [
        {
            "root": target_direct[label],
            "labels": [f"direct:{label}"],
            "desired_values": [abs(start_direct[label]) < 1.0],
        }
        for label in target_direct
    ]
    target_soft_roots = M5024.all_factor_roots(
        soft_direction, scattering_cosine
    )
    target_decay_roots = M5024.all_factor_roots(
        decay_direction, scattering_cosine
    )
    start_soft_roots = M5024.all_factor_roots(
        start_soft_direction, start_scattering_cosine
    )
    start_decay_roots = M5024.all_factor_roots(
        start_decay_direction, start_scattering_cosine
    )
    soft_desired = global_desired_labels(soft_segment)
    decay_desired = global_desired_labels(decay_segment)
    for decay_label in GLOBAL_ROOT_LABELS:
        for soft_label in GLOBAL_ROOT_LABELS:
            if (decay_label in decay_desired) == (
                soft_label in soft_desired
            ):
                continue
            target_root = (
                target_decay_roots[decay_label]
                / target_soft_roots[soft_label]
            )
            start_root = (
                start_decay_roots[decay_label]
                / start_soft_roots[soft_label]
            )
            rows.append(
                {
                    "root": target_root,
                    "labels": [
                        f"pinch:{decay_label}/{soft_label}"
                    ],
                    "desired_values": [abs(start_root) < 1.0],
                }
            )
    groups: list[dict[str, Any]] = []
    for row in rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"])
                < 2.0e-7 * max(1.0, abs(row["root"]))
            ),
            None,
        )
        if group is None:
            groups.append(row)
        else:
            group["labels"].extend(row["labels"])
            group["desired_values"].extend(row["desired_values"])
    for group in groups:
        if len(set(group["desired_values"])) != 1:
            raise RuntimeError(
                "coincident relative roots have mixed physical-sheet ownership: "
                + ", ".join(group["labels"])
            )
        group["desired_inside"] = group["desired_values"][0]
    return groups


def relative_rotated_direction(
    decay_direction: np.ndarray, relative_circle: complex
) -> np.ndarray:
    return M5022.rotate_vector(decay_direction, relative_circle)


def global_cycle_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_segment: str,
    decay_segment: str,
    global_nodes: int,
    global_residue_nodes: int,
) -> complex:
    integrand = lambda unit_circle: M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    root_rows: list[dict[str, Any]] = []
    for direction_name, direction, segment in (
        ("soft", soft_direction, soft_segment),
        ("decay", decay_direction, decay_segment),
    ):
        roots = M5024.all_factor_roots(direction, scattering_cosine)
        desired_labels = global_desired_labels(segment)
        for label, root in roots.items():
            root_rows.append(
                {
                    "root": root,
                    "labels": [f"{direction_name}:{label}"],
                    "desired_values": [label in desired_labels],
                }
            )
    groups: list[dict[str, Any]] = []
    for row in root_rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"])
                < 2.0e-7 * max(1.0, abs(row["root"]))
            ),
            None,
        )
        if group is None:
            groups.append(row)
        else:
            group["labels"].extend(row["labels"])
            group["desired_values"].extend(row["desired_values"])
    for group in groups:
        if len(set(group["desired_values"])) != 1:
            raise RuntimeError("coincident global roots have mixed ownership")
    base_radius = 1.0
    result = M5022.circle_integral(
        soft_direction,
        decay_direction,
        scattering_cosine,
        base_radius,
        global_nodes,
    )
    for group in groups:
        root = group["root"]
        desired_inside = group["desired_values"][0]
        currently_inside = abs(root) < base_radius
        if desired_inside == currently_inside:
            continue
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = M5024.local_residue(
            integrand,
            root,
            max(1.0e-7, 0.08 * safe_scale),
            global_residue_nodes,
        )
        if desired_inside and not currently_inside:
            result += residue
        else:
            result -= residue
    return result


def relative_circle_integral(
    evaluator: Callable[[complex], complex], radius: float, nodes: int
) -> complex:
    return complex(
        sum(
            evaluator(
                radius
                * np.exp(2.0j * np.pi * (index + 0.193) / nodes)
            )
            for index in range(nodes)
        )
        / nodes
    )


def relative_local_residue(
    evaluator: Callable[[complex], complex],
    root: complex,
    radius: float,
    nodes: int,
) -> complex:
    result = 0.0j
    for index in range(nodes):
        phase = np.exp(2.0j * np.pi * (index + 0.317) / nodes)
        relative_circle = root + radius * phase
        result += evaluator(relative_circle) / relative_circle * radius * phase
    return complex(result / nodes)


def nested_two_torus_value(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    soft_segment: str,
    decay_segment: str,
    soft_less_than_decay: bool,
    sum_less_than_one: bool,
    global_nodes: int,
    global_residue_nodes: int,
    relative_nodes: int,
    relative_residue_nodes: int,
    start_soft_direction: np.ndarray | None = None,
    start_decay_direction: np.ndarray | None = None,
    start_scattering_cosine: complex = complex(REFERENCE_COSINE, 0.0),
) -> complex:
    if start_soft_direction is None:
        start_soft_direction = soft_direction
    if start_decay_direction is None:
        start_decay_direction = decay_direction
    groups = relative_cycle_groups(
        soft_direction,
        decay_direction,
        scattering_cosine,
        start_soft_direction,
        start_decay_direction,
        start_scattering_cosine,
        soft_segment,
        decay_segment,
    )
    base_radius = 1.0

    def evaluator(relative_circle: complex) -> complex:
        return global_cycle_value(
            soft_direction,
            relative_rotated_direction(decay_direction, relative_circle),
            scattering_cosine,
            soft_segment,
            decay_segment,
            global_nodes,
            global_residue_nodes,
        )

    result = relative_circle_integral(evaluator, base_radius, relative_nodes)
    for group in groups:
        root = group["root"]
        desired_inside = group["desired_inside"]
        currently_inside = abs(root) < base_radius
        if desired_inside == currently_inside:
            continue
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = relative_local_residue(
            evaluator,
            root,
            max(1.0e-7, 0.07 * safe_scale),
            relative_residue_nodes,
        )
        if desired_inside and not currently_inside:
            result += residue
        else:
            result -= residue
    return result


def transported_triangle_value(
    triangle: dict[str, Any],
    point: np.ndarray,
    scattering_cosine: complex,
    global_nodes: int,
    global_residue_nodes: int,
    relative_nodes: int,
    relative_residue_nodes: int,
) -> complex:
    local = triangle_point(
        triangle["vertices"], float(point[0]), float(point[1])
    )
    soft_x, soft_jacobian = M5024.polar_segment(
        triangle["soft_segment"], float(local[0]), scattering_cosine
    )
    decay_x, decay_jacobian = M5024.polar_segment(
        triangle["decay_segment"], float(local[1]), scattering_cosine
    )
    soft_direction = M5024.direction_from_polar_x(soft_x, 0.0)
    decay_direction = M5024.direction_from_polar_x(decay_x, 0.0)
    start_soft_x, _ = M5024.polar_segment(
        triangle["soft_segment"], float(local[0]), REFERENCE_COSINE
    )
    start_decay_x, _ = M5024.polar_segment(
        triangle["decay_segment"], float(local[1]), REFERENCE_COSINE
    )
    start_soft_direction = M5024.direction_from_polar_x(
        start_soft_x, 0.0
    )
    start_decay_direction = M5024.direction_from_polar_x(
        start_decay_x, 0.0
    )
    return (
        triangle["area"]
        * soft_jacobian
        * decay_jacobian
        * nested_two_torus_value(
            soft_direction,
            decay_direction,
            scattering_cosine,
            triangle["soft_segment"],
            triangle["decay_segment"],
            triangle["soft_less_than_decay"],
            triangle["sum_less_than_one"],
            global_nodes,
            global_residue_nodes,
            relative_nodes,
            relative_residue_nodes,
            start_soft_direction,
            start_decay_direction,
        )
    )


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def two_torus_gate(
    power: int,
    seeds: tuple[int, ...],
    configuration_names: tuple[str, ...],
    global_nodes: int,
    global_residue_nodes: int,
    relative_nodes: int,
    relative_residue_nodes: int,
    diagnostics: bool = False,
    branch_layer_refinement: bool = False,
) -> dict[str, Any]:
    triangles = transported_triangles()
    area_by_cell: dict[str, float] = {}
    for triangle in triangles:
        key = f"{triangle['soft_segment']}:{triangle['decay_segment']}"
        area_by_cell[key] = area_by_cell.get(key, 0.0) + triangle["area"]
    partition_passed = (
        len(area_by_cell) == 9
        and max(abs(area - 1.0) for area in area_by_cell.values()) < 1.0e-12
    )
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_q1p5", complex(1.5, 0.08)),
    )
    configurations = tuple(
        row for row in configurations if row[0] in configuration_names
    )
    if len(configurations) != len(configuration_names):
        raise ValueError("unknown two-torus configuration")
    points = {
        seed: qmc.Sobol(d=2, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    rows: list[dict[str, Any]] = []
    for configuration, scattering_cosine in configurations:
        integration_triangles = (
            branch_layer_refined_triangles(triangles, scattering_cosine)
            if branch_layer_refinement
            else triangles
        )
        integration_area_by_cell: dict[str, float] = {}
        for triangle in integration_triangles:
            key = f"{triangle['soft_segment']}:{triangle['decay_segment']}"
            integration_area_by_cell[key] = (
                integration_area_by_cell.get(key, 0.0) + triangle["area"]
            )
        seed_means: list[complex] = []
        triangle_seed_means: list[list[complex]] = [
            [] for _ in integration_triangles
        ]
        for seed in seeds:
            triangle_means = [
                complex(
                    np.mean(
                        [
                            transported_triangle_value(
                                triangle,
                                point,
                                scattering_cosine,
                                global_nodes,
                                global_residue_nodes,
                                relative_nodes,
                                relative_residue_nodes,
                            )
                            for point in points[seed]
                        ]
                    )
                )
                for triangle in integration_triangles
            ]
            seed_means.append(complex(sum(triangle_means)))
            for triangle_index, triangle_mean in enumerate(triangle_means):
                triangle_seed_means[triangle_index].append(triangle_mean)
        mean, real_error, imaginary_error = aggregate(seed_means)
        exact = complex(
            M5024.M5023.M5019.endpoint_resolvent(
                mp.mpc(scattering_cosine.real, scattering_cosine.imag), 192
            )[2]
        )
        row: dict[str, Any] = {
            "configuration": configuration,
            "scattering_cosine": str(scattering_cosine),
            "two_torus_sector_endpoint": str(mean),
            "RQMC_real_error": real_error,
            "RQMC_imaginary_error": imaginary_error,
            "exact_resolvent": str(exact),
            "relative_residual": abs(mean - exact) / max(abs(exact), 1.0e-30),
            "seed_means": [str(value) for value in seed_means],
        }
        if diagnostics:
            triangle_rows: list[dict[str, Any]] = []
            for triangle_index, (triangle, values) in enumerate(
                zip(integration_triangles, triangle_seed_means)
            ):
                triangle_mean, triangle_real_error, triangle_imaginary_error = (
                    aggregate(values)
                )
                triangle_rows.append(
                    {
                        "triangle_index": triangle_index,
                        "parent_triangle_index": triangle.get(
                            "parent_triangle_index", triangle_index
                        ),
                        "soft_segment": triangle["soft_segment"],
                        "decay_segment": triangle["decay_segment"],
                        "soft_less_than_decay": triangle[
                            "soft_less_than_decay"
                        ],
                        "sum_less_than_one": triangle["sum_less_than_one"],
                        "reference_area": triangle["area"],
                        "vertices": [
                            vertex.tolist() for vertex in triangle["vertices"]
                        ],
                        "mean": str(triangle_mean),
                        "RQMC_real_error": triangle_real_error,
                        "RQMC_imaginary_error": triangle_imaginary_error,
                        "seed_means": [str(value) for value in values],
                    }
                )
            row["triangle_rows"] = triangle_rows
        row["integration_triangle_count"] = len(integration_triangles)
        row["integration_cell_area_sums"] = integration_area_by_cell
        row["integration_partition_passed"] = (
            len(integration_area_by_cell) == 9
            and max(
                abs(area - 1.0)
                for area in integration_area_by_cell.values()
            )
            < 1.0e-12
        )
        row["middle_branch_layer_breaks"] = (
            middle_branch_layer_breaks(scattering_cosine)
            if branch_layer_refinement
            else [0.0, 1.0]
        )
        rows.append(row)
    return {
        "triangle_count": len(triangles),
        "cell_area_sums": area_by_cell,
        "partition_passed": partition_passed,
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "global_nodes": global_nodes,
        "global_residue_nodes": global_residue_nodes,
        "relative_nodes": relative_nodes,
        "relative_residue_nodes": relative_residue_nodes,
        "branch_layer_refinement": branch_layer_refinement,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=1)
    parser.add_argument("--seeds", default="50251,50252")
    parser.add_argument("--configurations", default="physical,crossed_q1p5")
    parser.add_argument("--global-nodes", type=int, default=16)
    parser.add_argument("--global-residue-nodes", type=int, default=8)
    parser.add_argument("--relative-nodes", type=int, default=16)
    parser.add_argument("--relative-residue-nodes", type=int, default=8)
    parser.add_argument("--diagnostics", action="store_true")
    parser.add_argument("--branch-layer-refinement", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = two_torus_gate(
        arguments.power,
        tuple(int(value) for value in arguments.seeds.split(",")),
        tuple(arguments.configurations.split(",")),
        arguments.global_nodes,
        arguments.global_residue_nodes,
        arguments.relative_nodes,
        arguments.relative_residue_nodes,
        arguments.diagnostics,
        arguments.branch_layer_refinement,
    )
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
