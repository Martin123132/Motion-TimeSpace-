from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
from types import SimpleNamespace
from typing import Any

from mpmath import iv


POST = Path(__file__).resolve().parents[1]
PRIMARY = POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
OUTPUT = POST / "source-intake" / "functional_rg" / "5396"
STATE = (
    OUTPUT
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X002_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)


def load_primary() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5396_frontier_primary", PRIMARY
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def closed_arc_displacement(
    module: Any,
    global_radius: float,
    arc_index: int,
    arc_subindex: int,
    arc_subdivision_count: int,
    global_arc_count: int,
) -> Any:
    phase_lower = (
        arc_index + arc_subindex / arc_subdivision_count
    ) * 2 * math.pi / global_arc_count
    phase_upper = (
        arc_index + (arc_subindex + 1) / arc_subdivision_count
    ) * 2 * math.pi / global_arc_count
    phase = module.cbox(phase_lower, phase_upper)
    return module.cpoint(global_radius) * (
        iv.cos(phase) + module.cpoint(1j) * iv.sin(phase)
    )


def selected_frontier(
    arguments: argparse.Namespace, state: dict[str, Any]
) -> tuple[float, float, float, float, int, str, str]:
    explicit_values = (
        arguments.x_lower,
        arguments.x_upper,
        arguments.t_lower,
        arguments.t_upper,
        arguments.refinement_depth,
        arguments.refinement_path,
    )
    if any(value is not None for value in explicit_values):
        if not all(value is not None for value in explicit_values):
            raise ValueError(
                "explicit frontier requires x/t bounds, depth, and path together"
            )
        return (
            float(arguments.x_lower),
            float(arguments.x_upper),
            float(arguments.t_lower),
            float(arguments.t_upper),
            int(arguments.refinement_depth),
            str(arguments.refinement_path),
            "explicit_cli",
        )
    if not state["stack"]:
        raise RuntimeError("selected frontier state is already empty")
    try:
        frontier = state["stack"][arguments.stack_index]
    except IndexError as error:
        raise ValueError(
            f"stack index {arguments.stack_index} is outside the live frontier"
        ) from error
    return (
        float(frontier[0]),
        float(frontier[1]),
        float(frontier[2]),
        float(frontier[3]),
        int(frontier[4]),
        str(frontier[5]),
        f"state_stack[{arguments.stack_index}]",
    )


def run_audit(arguments: argparse.Namespace) -> dict[str, Any]:
    module = load_primary()
    module.set_below_normal_priority()
    iv.dps = module.INTERVAL_DIGITS
    explicit_frontier = any(
        value is not None
        for value in (
            arguments.x_lower,
            arguments.x_upper,
            arguments.t_lower,
            arguments.t_upper,
            arguments.refinement_depth,
            arguments.refinement_path,
        )
    )
    state = {} if explicit_frontier else module.read_json(STATE)
    (
        x_lower,
        x_upper,
        t_lower,
        t_upper,
        depth,
        refinement_path,
        frontier_source,
    ) = selected_frontier(arguments, state)
    mapped_cell_id = str(arguments.mapped_cell_id)
    term_id = str(arguments.term_id)
    path_segment = str(arguments.path_segment)
    cell = next(
        row
        for row in module.away_term_support_cells()
        if row["mapped_cell_id"] == mapped_cell_id
    )
    configuration = module.configuration_variants(term_id)[0]
    epsilon_row = module.epsilon_boxes(
        SimpleNamespace(
            combined_regulator_box=True,
            combined_regulator_slab_count=2,
            epsilon_subdivisions=1,
        )
    )[0]
    epsilon = module.epsilon_interval(epsilon_row)
    coordinate = module.cbox(float(x_lower), float(x_upper))
    parameter = module.cbox(float(t_lower), float(t_upper))
    energy = module.deformed_path_energy_dual(
        cell, path_segment, coordinate, parameter
    ).value
    _, geometry = module.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    global_radius = 1.0e-7 * max(
        1.0, module.M5258.upper_abs(geometry["selected_root"])
    )

    point_rows: list[dict[str, Any]] = []
    epsilon_real_values = (
        float(epsilon_row["epsilon_real_lower"]),
        0.5
        * (
            float(epsilon_row["epsilon_real_lower"])
            + float(epsilon_row["epsilon_real_upper"])
        ),
        float(epsilon_row["epsilon_real_upper"]),
    )
    epsilon_imaginary_values = (
        float(epsilon_row["epsilon_imaginary_lower"]),
        0.0,
        float(epsilon_row["epsilon_imaginary_upper"]),
    )
    for coordinate_value in (
        float(x_lower),
        0.5 * (float(x_lower) + float(x_upper)),
        float(x_upper),
    ):
        for parameter_value in (
            float(t_lower),
            0.5 * (float(t_lower) + float(t_upper)),
            float(t_upper),
        ):
            for epsilon_real in epsilon_real_values:
                for epsilon_imaginary in epsilon_imaginary_values:
                    epsilon_point = module.cpoint(
                        complex(epsilon_real, epsilon_imaginary)
                    )
                    for arc_index in range(arguments.global_arc_count):
                        phase = (
                            arc_index + 0.5
                        ) * 2 * math.pi / arguments.global_arc_count
                        displacement = module.cpoint(
                            global_radius
                            * complex(math.cos(phase), math.sin(phase))
                        )
                        angle = module.centered_path_correlated_external4_first_plus_angle_factorized(
                            configuration,
                            cell,
                            path_segment,
                            module.cpoint(coordinate_value),
                            module.cpoint(parameter_value),
                            epsilon_point,
                            displacement,
                        )
                        angle_value = complex(module.M5394.midpoint(angle))
                        point_rows.append(
                            {
                                "absolute_coordinate": coordinate_value,
                                "path_parameter": parameter_value,
                                "epsilon_real": epsilon_real,
                                "epsilon_imaginary": epsilon_imaginary,
                                "arc_index": arc_index,
                                "angle_real": angle_value.real,
                                "angle_imaginary": angle_value.imag,
                                "angle_modulus": abs(angle_value),
                            }
                        )

    cover_rows: list[dict[str, Any]] = []
    for subdivision_count, arc_subdivision_count in (
        (16, 1),
        (16, 2),
        (32, 1),
    ):
        for arc_index in range(arguments.global_arc_count):
            for arc_subindex in range(arc_subdivision_count):
                displacement = closed_arc_displacement(
                    module,
                    global_radius,
                    arc_index,
                    arc_subindex,
                    arc_subdivision_count,
                    arguments.global_arc_count,
                )
                started = time.time()
                angle = module.subdivided_path_external4_first_plus_angle_factorized(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    displacement,
                    subdivision_count,
                )
                real_lower, real_upper = module.M5394.real_bounds(angle)
                imaginary_lower, imaginary_upper = module.M5394.imaginary_bounds(
                    angle
                )
                cover_rows.append(
                    {
                        "subdivision_count": subdivision_count,
                        "arc_subdivision_count": arc_subdivision_count,
                        "arc_index": arc_index,
                        "arc_subindex": arc_subindex,
                        "angle_real_lower": real_lower,
                        "angle_real_upper": real_upper,
                        "angle_imaginary_lower": imaginary_lower,
                        "angle_imaginary_upper": imaginary_upper,
                        "angle_abs_lower": module.M5258.lower_abs(angle),
                        "nonzero_half_plane_passed": (
                            imaginary_lower > 0.0 or imaginary_upper < 0.0
                        ),
                        "runtime_seconds": time.time() - started,
                    }
                )

    scheme_rows: list[dict[str, Any]] = []
    for subdivision_count, arc_subdivision_count in sorted(
        {
            (
                int(row["subdivision_count"]),
                int(row["arc_subdivision_count"]),
            )
            for row in cover_rows
        }
    ):
        rows = [
            row
            for row in cover_rows
            if int(row["subdivision_count"]) == subdivision_count
            and int(row["arc_subdivision_count"])
            == arc_subdivision_count
        ]
        scheme_rows.append(
            {
                "subdivision_count": subdivision_count,
                "arc_subdivision_count": arc_subdivision_count,
                "cover_count": len(rows),
                "minimum_angle_abs_lower": min(
                    float(row["angle_abs_lower"]) for row in rows
                ),
                "minimum_imaginary_lower": min(
                    float(row["angle_imaginary_lower"]) for row in rows
                ),
                "maximum_imaginary_upper": max(
                    float(row["angle_imaginary_upper"]) for row in rows
                ),
                "all_nonzero_half_plane_passed": all(
                    bool(row["nonzero_half_plane_passed"]) for row in rows
                ),
                "runtime_seconds": sum(
                    float(row["runtime_seconds"]) for row in rows
                ),
            }
        )

    payload = {
        "checkpoint": 5396,
        "primary_revision": module.REVISION,
        "frontier": {
            "mapped_cell_id": mapped_cell_id,
            "term_id": term_id,
            "path_segment": path_segment,
            "x_lower": x_lower,
            "x_upper": x_upper,
            "t_lower": t_lower,
            "t_upper": t_upper,
            "refinement_depth": depth,
            "refinement_path": refinement_path,
            "source": frontier_source,
        },
        "global_radius": global_radius,
        "point_count": len(point_rows),
        "minimum_sampled_angle_modulus": min(
            float(row["angle_modulus"]) for row in point_rows
        ),
        "minimum_sampled_angle_imaginary": min(
            float(row["angle_imaginary"]) for row in point_rows
        ),
        "maximum_sampled_angle_imaginary": max(
            float(row["angle_imaginary"]) for row in point_rows
        ),
        "schemes": scheme_rows,
        "selected_scheme": next(
            (
                {
                    "subdivision_count": row["subdivision_count"],
                    "arc_subdivision_count": row[
                        "arc_subdivision_count"
                    ],
                }
                for row in scheme_rows
                if row["all_nonzero_half_plane_passed"]
            ),
            None,
        ),
    }
    frontier_id = f"d{int(depth):02d}_{refinement_path or 'ROOT'}"
    frontier_scope = f"{mapped_cell_id}_{path_segment}"
    artifact_id = f"{frontier_scope}_{frontier_id}"
    payload["artifact_prefix"] = f"external41_frontier_angle_{artifact_id}"
    module.atomic_csv(
        OUTPUT / f"external41_frontier_angle_{artifact_id}_point_audit.csv",
        point_rows,
    )
    module.atomic_csv(
        OUTPUT / f"external41_frontier_angle_{artifact_id}_cover_audit.csv",
        cover_rows,
    )
    module.atomic_csv(
        OUTPUT / f"external41_frontier_angle_{artifact_id}_scheme_audit.csv",
        scheme_rows,
    )
    module.atomic_json(
        OUTPUT / f"external41_frontier_angle_{artifact_id}_audit_result.json",
        payload,
    )
    if frontier_source != "explicit_cli":
        module.atomic_csv(
            OUTPUT / "external41_frontier_angle_point_audit.csv", point_rows
        )
        module.atomic_csv(
            OUTPUT / "external41_frontier_angle_cover_audit.csv", cover_rows
        )
        module.atomic_csv(
            OUTPUT / "external41_frontier_angle_scheme_audit.csv", scheme_rows
        )
        module.atomic_json(
            OUTPUT / "external41_frontier_angle_audit_result.json", payload
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--global-arc-count", type=int, default=4)
    parser.add_argument("--mapped-cell-id", default="S_X002_MC04_SP_DM")
    parser.add_argument("--term-id", default="MC04_SP_DM")
    parser.add_argument("--path-segment", default="RIGHT_CONNECTOR")
    parser.add_argument("--stack-index", type=int, default=-1)
    parser.add_argument("--x-lower", type=float)
    parser.add_argument("--x-upper", type=float)
    parser.add_argument("--t-lower", type=float)
    parser.add_argument("--t-upper", type=float)
    parser.add_argument("--refinement-depth", type=int)
    parser.add_argument("--refinement-path")
    arguments = parser.parse_args()
    print(json.dumps(run_audit(arguments), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
