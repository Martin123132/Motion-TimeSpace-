from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Any

from mpmath import iv


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "functional_rg" / "5396"
PRIMARY_PATH = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
AUDIT_PATH = SCRIPTS / "Y5_R2FR_5396_D4_frontier_gale_nikaido_audit.py"
STATE_PATH = (
    OUTPUT
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X002_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def relative_error(left: complex, right: complex) -> float:
    return abs(left - right) / max(1.0e-30, abs(left), abs(right))


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


def run_crosscheck(arguments: argparse.Namespace) -> dict[str, Any]:
    primary = load_module("mts_5396_centered_crosscheck_primary", PRIMARY_PATH)
    audit = load_module("mts_5396_centered_crosscheck_audit", AUDIT_PATH)
    primary.set_below_normal_priority()
    iv.dps = primary.INTERVAL_DIGITS
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
    state = {} if explicit_frontier else primary.read_json(STATE_PATH)
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
        for row in primary.away_term_support_cells()
        if row["mapped_cell_id"] == mapped_cell_id
    )
    configuration = primary.configuration_variants(term_id)[0]
    epsilon_row = primary.epsilon_boxes(
        SimpleNamespace(
            combined_regulator_box=True,
            combined_regulator_slab_count=2,
            epsilon_subdivisions=1,
        )
    )[0]
    coordinate_box = primary.cbox(float(x_lower), float(x_upper))
    parameter_box = primary.cbox(float(t_lower), float(t_upper))
    epsilon_box = primary.epsilon_interval(epsilon_row)
    energy = primary.deformed_path_energy_dual(
        cell, path_segment, coordinate_box, parameter_box
    ).value
    _, geometry = primary.interval_inputs(
        configuration, coordinate_box, energy, epsilon_box
    )
    global_radius = 1.0e-7 * max(
        1.0, primary.M5258.upper_abs(geometry["selected_root"])
    )
    rows: list[dict[str, Any]] = []
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
            for epsilon_real in (
                float(epsilon_row["epsilon_real_lower"]),
                0.5
                * (
                    float(epsilon_row["epsilon_real_lower"])
                    + float(epsilon_row["epsilon_real_upper"])
                ),
                float(epsilon_row["epsilon_real_upper"]),
            ):
                for arc_index in range(4):
                    phase = (arc_index + 0.5) * math.pi / 2
                    displacement = primary.cpoint(
                        global_radius
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    coordinate = primary.cpoint(coordinate_value)
                    parameter = primary.cpoint(parameter_value)
                    epsilon = primary.cpoint(epsilon_real)
                    centered_x, centered_t = (
                        audit.centered_native_path_derivatives(
                            primary,
                            configuration,
                            cell,
                            path_segment,
                            coordinate,
                            parameter,
                            epsilon,
                            displacement,
                        )
                    )
                    direct_x, direct_t = (
                        primary.native_external0_first_minus_plus_path_derivatives(
                            configuration,
                            cell,
                            path_segment,
                            coordinate,
                            parameter,
                            epsilon,
                            displacement,
                        )
                    )
                    centered_x_value = complex(
                        primary.M5394.midpoint(centered_x)
                    )
                    centered_t_value = complex(
                        primary.M5394.midpoint(centered_t)
                    )
                    direct_x_value = complex(
                        primary.M5394.midpoint(direct_x)
                    )
                    direct_t_value = complex(
                        primary.M5394.midpoint(direct_t)
                    )
                    rows.append(
                        {
                            "absolute_coordinate": coordinate_value,
                            "path_parameter": parameter_value,
                            "epsilon_real": epsilon_real,
                            "arc_index": arc_index,
                            "centered_x_real": centered_x_value.real,
                            "centered_x_imaginary": centered_x_value.imag,
                            "direct_x_real": direct_x_value.real,
                            "direct_x_imaginary": direct_x_value.imag,
                            "x_relative_error": relative_error(
                                centered_x_value, direct_x_value
                            ),
                            "centered_t_real": centered_t_value.real,
                            "centered_t_imaginary": centered_t_value.imag,
                            "direct_t_real": direct_t_value.real,
                            "direct_t_imaginary": direct_t_value.imag,
                            "t_relative_error": relative_error(
                                centered_t_value, direct_t_value
                            ),
                        }
                    )
    maximum_error = max(
        max(float(row["x_relative_error"]), float(row["t_relative_error"]))
        for row in rows
    )
    payload = {
        "checkpoint": 5396,
        "primary_revision": primary.REVISION,
        "mapped_cell_id": mapped_cell_id,
        "term_id": term_id,
        "path_segment": path_segment,
        "frontier_depth": depth,
        "frontier_path": refinement_path,
        "frontier_source": frontier_source,
        "row_count": len(rows),
        "maximum_centered_to_direct_relative_error": maximum_error,
        "all_identities_passed": maximum_error <= 5.0e-12,
    }
    frontier_id = f"d{int(depth):02d}_{refinement_path or 'ROOT'}"
    frontier_scope = f"{mapped_cell_id}_{path_segment}"
    artifact_id = f"{frontier_scope}_{frontier_id}"
    payload["artifact_prefix"] = f"external01_centered_jacobian_{artifact_id}"
    primary.atomic_csv(
        OUTPUT
        / f"external01_centered_jacobian_{artifact_id}_point_crosschecks.csv",
        rows,
    )
    primary.atomic_json(
        OUTPUT / f"external01_centered_jacobian_{artifact_id}_result.json",
        payload,
    )
    if frontier_source != "explicit_cli":
        primary.atomic_csv(
            OUTPUT / "external01_centered_jacobian_point_crosschecks.csv", rows
        )
        primary.atomic_json(
            OUTPUT / "external01_centered_jacobian_crosscheck_result.json",
            payload,
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
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
    print(json.dumps(run_crosscheck(parser.parse_args()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
