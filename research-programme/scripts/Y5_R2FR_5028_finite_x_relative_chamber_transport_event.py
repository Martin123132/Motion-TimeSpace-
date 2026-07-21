from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5027 = (
    POST
    / "scripts"
    / "Y5_R2FR_5027_finite_x_boosted_polar_pinch_map.py"
)
REFERENCE_COSINE = complex(0.3, 0.0)
ROOT_LABELS = ("plus_u", "plus_v", "minus_u", "minus_v")
ROOT_COINCIDENCE_RELATIVE_TOLERANCE = 5.0e-12


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5027 = load_module("mts_5027_for_5028", SCRIPT_5027)
M5026 = M5027.M5026
M5024 = M5026.M5024


def event_geometry(
    soft_energy: float,
    soft_cosine: complex,
    decay_cosine: complex,
    relative_circle: complex,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    soft_direction, decay_direction = M5027.direction_pair_from_cosines(
        soft_cosine, decay_cosine, relative_circle
    )
    internal = M5027.complex_sequential_three_body(
        soft_energy, soft_direction, decay_direction
    )
    return soft_direction, decay_direction, internal


def source_directions(
    internal: np.ndarray,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
) -> dict[str, np.ndarray]:
    return {
        "direct:g1": M5026.internal_direction(internal[0]),
        "direct:g2": M5026.internal_direction(internal[1]),
        "direct:g3": M5026.internal_direction(internal[2]),
        "subtraction:soft": soft_direction,
        "subtraction:decay": decay_direction,
    }


def chamber_ownership(
    soft_energy: float,
    soft_cosine: complex,
    decay_cosine: complex,
    relative_circle: complex,
) -> dict[str, bool]:
    soft_direction, decay_direction, internal = event_geometry(
        soft_energy, soft_cosine, decay_cosine, relative_circle
    )
    ownership: dict[str, bool] = {}
    for source, direction in source_directions(
        internal, soft_direction, decay_direction
    ).items():
        roots = M5024.all_factor_roots(direction, REFERENCE_COSINE)
        for label in ROOT_LABELS:
            ownership[f"{source}:{label}"] = abs(roots[label]) < 1.0
    return ownership


def fixed_ownership_groups(
    internal: np.ndarray,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    ownership: dict[str, bool],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, direction in source_directions(
        internal, soft_direction, decay_direction
    ).items():
        roots = M5024.all_factor_roots(direction, scattering_cosine)
        for label in ROOT_LABELS:
            key = f"{source}:{label}"
            rows.append(
                {
                    "root": roots[label],
                    "labels": [key],
                    "desired_values": [ownership[key]],
                }
            )
    groups: list[dict[str, Any]] = []
    for row in rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"])
                < ROOT_COINCIDENCE_RELATIVE_TOLERANCE
                * max(1.0, abs(row["root"]), abs(candidate["root"]))
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
                "relative chamber crossed an unsectorized global collision: "
                + ", ".join(group["labels"])
            )
        group["desired_inside"] = group["desired_values"][0]
    return groups


def fixed_ownership_global_cycle(
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    internal: np.ndarray,
    scattering_cosine: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    residue_nodes: int,
) -> tuple[complex, int]:
    groups = fixed_ownership_groups(
        internal,
        soft_direction,
        decay_direction,
        scattering_cosine,
        ownership,
    )
    evaluator = lambda unit_circle: M5026.finite_plus_integrand(
        internal,
        soft_energy,
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    base_radius = M5026.conditioned_global_base_radius(groups)
    result = M5026.circle_average(evaluator, global_nodes, base_radius)
    correction_count = 0
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
        residue = M5024.local_residue(
            evaluator,
            root,
            max(1.0e-7, 0.07 * safe_scale),
            residue_nodes,
        )
        result = result + residue if desired_inside else result - residue
        correction_count += 1
    return result, correction_count


def physical_relative_boundaries(
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for hard_sign in (1, -1):
        for external_sign in (1, -1):
            roots = M5027.relative_azimuth_roots(
                soft_energy,
                complex(soft_cosine, 0.0),
                complex(decay_cosine, 0.0),
                external_sign * REFERENCE_COSINE,
                hard_sign,
            )[:2]
            for branch_index, root in enumerate(roots):
                if abs(abs(root) - 1.0) > 2.0e-8:
                    continue
                angle = math.atan2(root.imag, root.real) % (2.0 * math.pi)
                rows.append(
                    {
                        "angle": angle,
                        "root": root,
                        "hard_sign": hard_sign,
                        "external_sign": external_sign,
                        "branch_index": branch_index,
                    }
                )
    rows.sort(key=lambda row: row["angle"])
    grouped: list[dict[str, Any]] = []
    for row in rows:
        if grouped and abs(row["angle"] - grouped[-1]["angle"]) < 2.0e-8:
            grouped[-1]["equations"].append(row)
        else:
            grouped.append(
                {
                    "angle": row["angle"],
                    "root": row["root"],
                    "equations": [row],
                }
            )
    return grouped


def track_boundary_root(
    boundary: dict[str, Any],
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    target_cosine: complex,
    steps: int,
) -> complex:
    equation = boundary["equations"][0]
    start_roots = M5027.relative_azimuth_roots(
        soft_energy,
        complex(soft_cosine, 0.0),
        complex(decay_cosine, 0.0),
        equation["external_sign"] * REFERENCE_COSINE,
        equation["hard_sign"],
    )[:2]
    start_eta = (start_roots[0] + start_roots[1]) / 2.0
    current_square_root = complex(boundary["root"] - start_eta)
    current = complex(boundary["root"])
    for step in range(1, steps + 1):
        fraction = step / steps
        cosine = REFERENCE_COSINE + fraction * (
            target_cosine - REFERENCE_COSINE
        )
        roots = M5027.relative_azimuth_roots(
            soft_energy,
            complex(soft_cosine, 0.0),
            complex(decay_cosine, 0.0),
            equation["external_sign"] * cosine,
            equation["hard_sign"],
        )[:2]
        eta = (roots[0] + roots[1]) / 2.0
        principal_square_root = complex(np.sqrt(eta * eta - 1.0 + 0.0j))
        square_root_candidates = (
            principal_square_root,
            -principal_square_root,
        )
        current_square_root = min(
            square_root_candidates,
            key=lambda candidate: abs(candidate - current_square_root),
        )
        current = eta + current_square_root
    return complex(current)


def unwrapped_log(root: complex, reference_angle: float) -> complex:
    phase = math.atan2(root.imag, root.real)
    phase += 2.0 * math.pi * round(
        (reference_angle - phase) / (2.0 * math.pi)
    )
    return complex(math.log(abs(root)), phase)


def gauss_rule(order: int) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return (nodes + 1.0) / 2.0, weights / 2.0


def transported_relative_chambers(
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    scattering_cosine: complex,
    relative_order: int,
    global_nodes: int,
    residue_nodes: int,
    tracking_steps: int,
) -> dict[str, Any]:
    boundaries = physical_relative_boundaries(
        soft_energy, soft_cosine, decay_cosine
    )
    nodes, weights = gauss_rule(relative_order)
    if not boundaries:
        boundaries = [
            {
                "angle": 0.0,
                "root": 1.0 + 0.0j,
                "equations": [],
                "synthetic": True,
            }
        ]
    target_roots = [
        (
            complex(boundary["root"])
            if boundary.get("synthetic")
            else track_boundary_root(
                boundary,
                soft_energy,
                soft_cosine,
                decay_cosine,
                scattering_cosine,
                tracking_steps,
            )
        )
        for boundary in boundaries
    ]
    total = 0.0j
    total_global_corrections = 0
    arc_rows: list[dict[str, Any]] = []
    for boundary_index, boundary in enumerate(boundaries):
        next_index = (boundary_index + 1) % len(boundaries)
        start_angle = float(boundary["angle"])
        end_angle = float(boundaries[next_index]["angle"])
        if next_index == 0:
            end_angle += 2.0 * math.pi
        midpoint_angle = (start_angle + end_angle) / 2.0
        ownership = chamber_ownership(
            soft_energy,
            complex(soft_cosine, 0.0),
            complex(decay_cosine, 0.0),
            np.exp(1.0j * midpoint_angle),
        )
        if boundary.get("synthetic"):
            start_log = complex(0.0, start_angle)
            end_log = complex(0.0, end_angle)
        else:
            start_log = unwrapped_log(
                target_roots[boundary_index], start_angle
            )
            end_log = unwrapped_log(target_roots[next_index], end_angle)
        log_difference = end_log - start_log
        arc_value = 0.0j
        arc_corrections = 0
        for node, weight in zip(nodes, weights):
            relative_circle = np.exp(start_log + node * log_difference)
            soft_direction, decay_direction, internal = event_geometry(
                soft_energy,
                complex(soft_cosine, 0.0),
                complex(decay_cosine, 0.0),
                complex(relative_circle),
            )
            global_value, correction_count = fixed_ownership_global_cycle(
                soft_energy,
                soft_direction,
                decay_direction,
                internal,
                scattering_cosine,
                ownership,
                global_nodes,
                residue_nodes,
            )
            arc_value += weight * global_value
            arc_corrections += correction_count
        arc_value *= log_difference / (2.0j * math.pi)
        total += arc_value
        total_global_corrections += arc_corrections
        arc_rows.append(
            {
                "start_angle": start_angle,
                "end_angle": end_angle,
                "start_target_root": str(np.exp(start_log)),
                "end_target_root": str(np.exp(end_log)),
                "arc_value": str(arc_value),
                "global_correction_evaluations": arc_corrections,
            }
        )
    return {
        "value": total,
        "boundary_count": len(boundaries),
        "target_boundary_roots": [str(root) for root in target_roots],
        "arc_rows": arc_rows,
        "global_correction_evaluations": total_global_corrections,
    }


def raw_two_azimuth_average(
    soft_energy: float,
    soft_cosine: float,
    decay_cosine: float,
    scattering_cosine: complex,
    relative_nodes: int,
    global_nodes: int,
) -> complex:
    total = 0.0j
    for relative_index in range(relative_nodes):
        relative_circle = np.exp(
            2.0j * math.pi * (relative_index + 0.193) / relative_nodes
        )
        soft_direction, decay_direction, internal = event_geometry(
            soft_energy,
            complex(soft_cosine, 0.0),
            complex(decay_cosine, 0.0),
            complex(relative_circle),
        )
        evaluator = lambda unit_circle: M5026.finite_plus_integrand(
            internal,
            soft_energy,
            soft_direction,
            decay_direction,
            scattering_cosine,
            unit_circle,
        )
        total += M5026.circle_average(evaluator, global_nodes)
    return complex(total / relative_nodes)


def event_gate(
    relative_order: int,
    global_nodes: int,
    residue_nodes: int,
    tracking_steps: int,
) -> dict[str, Any]:
    soft_energy = 0.37
    soft_cosine = 0.23
    decay_cosine = -0.31
    crossed_cosine = complex(1.5, 0.08)
    physical = transported_relative_chambers(
        soft_energy,
        soft_cosine,
        decay_cosine,
        REFERENCE_COSINE,
        relative_order,
        global_nodes,
        residue_nodes,
        tracking_steps,
    )
    physical_reference = raw_two_azimuth_average(
        soft_energy,
        soft_cosine,
        decay_cosine,
        REFERENCE_COSINE,
        96,
        128,
    )
    crossed = transported_relative_chambers(
        soft_energy,
        soft_cosine,
        decay_cosine,
        crossed_cosine,
        relative_order,
        global_nodes,
        residue_nodes,
        tracking_steps,
    )
    crossed_raw = raw_two_azimuth_average(
        soft_energy,
        soft_cosine,
        decay_cosine,
        crossed_cosine,
        48,
        48,
    )
    physical_residual = abs(physical["value"] - physical_reference) / max(
        abs(physical_reference), 1.0e-30
    )
    return {
        "soft_energy": soft_energy,
        "soft_cosine": soft_cosine,
        "decay_cosine": decay_cosine,
        "physical_reference": str(physical_reference),
        "physical_chamber_value": str(physical["value"]),
        "physical_relative_residual": physical_residual,
        "physical_control_passed": physical_residual < 2.0e-4,
        "physical_chambers": physical,
        "crossed_raw_two_azimuth": str(crossed_raw),
        "crossed_transported_chamber_value": str(crossed["value"]),
        "crossed_transport_shift": str(crossed["value"] - crossed_raw),
        "crossed_chambers": crossed,
        "relative_chamber_transport_constructed": True,
        "cross_source_collision_sectorization_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--relative-order", type=int, default=8)
    parser.add_argument("--global-nodes", type=int, default=12)
    parser.add_argument("--residue-nodes", type=int, default=12)
    parser.add_argument("--tracking-steps", type=int, default=64)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = event_gate(
        arguments.relative_order,
        arguments.global_nodes,
        arguments.residue_nodes,
        arguments.tracking_steps,
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
