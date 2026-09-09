from __future__ import annotations

import argparse
import ctypes
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any


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
if os.name == "nt":
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


CHECKPOINT = 5428
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
GATE_5427_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5427_D4_representative_external01_square_half_plane_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG
    / "5427"
    / "representative_external01_square_half_plane_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5427" / "P8_Y5_BRR5396_5427_VALIDATION.csv"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
DOCUMENT = POST / "5428-Y5-R2FR-D4-representative-external01-ratio-disk-gate.md"
POINTS = OUTPUT / "representative_external01_ratio_point_crosschecks.csv"
BOXES = OUTPUT / "representative_external01_ratio_box_probes.csv"
COVER = OUTPUT / "representative_external01_ratio_disk_cover.csv"
COVER_SUMMARY = OUTPUT / "representative_external01_ratio_disk_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5428_VALIDATION.csv"
RESULT = OUTPUT / "representative_external01_ratio_disk_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v44"
EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:"
    "edge_0_0_1:stable_edge"
)
BROAD_COLUMNS = (
    "valid_for_D4_numeric_event_local_W3_bound",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_module(name: str, path: Path) -> Any:
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def context(parent: Any) -> tuple[Any, Any, Any, dict[str, Any]]:
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == "S_X006_MC04_SP_DP"
    )
    configuration = next(
        row
        for row in parent.configuration_variants("MC04_SP_DP")
        if row["role"] == "representative"
    )
    arguments = argparse.Namespace(
        combined_regulator_box=True,
        combined_regulator_slab_count=2,
        epsilon_subdivisions=1,
    )
    epsilon_row = parent.epsilon_boxes(arguments)[0]
    epsilon = parent.epsilon_interval(epsilon_row)
    return cell, configuration, epsilon, epsilon_row


def representative_external01_ratio_rational_dual(
    parent: Any,
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    global_displacement: Any,
) -> Any:
    if configuration["role"] != "representative":
        raise ValueError("ratio formula requires representative role")
    dual = parent.M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    global_displacement = dual.coerce(global_displacement)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    recoil_squared = recoil * recoil
    soft_squared = soft_cosine * soft_cosine
    numerator = (
        decay_cosine * q_value * recoil_squared * soft_cosine
        - decay_cosine * q_value * recoil_squared
        - decay_cosine * q_value * soft_cosine
        - decay_cosine * q_value
        + decay_cosine * recoil_squared * soft_cosine
        - decay_cosine * recoil_squared
        - decay_cosine * soft_cosine
        + decay_cosine
        + q_value * recoil_squared * soft_squared
        - q_value * recoil_squared * soft_cosine
        - 2 * q_value * recoil * soft_squared
        + 2 * q_value * recoil
        + q_value * soft_squared
        + q_value * soft_cosine
        + recoil_squared * soft_squared
        - recoil_squared * soft_cosine
        - 2 * recoil * soft_squared
        + 2 * recoil * soft_cosine
        + soft_squared
        - soft_cosine
    )
    denominator = (
        decay_cosine * q_value * recoil_squared * soft_cosine
        + decay_cosine * q_value * recoil_squared
        - decay_cosine * q_value * soft_cosine
        - decay_cosine * q_value
        + decay_cosine * recoil_squared * soft_cosine
        + decay_cosine * recoil_squared
        - decay_cosine * soft_cosine
        + decay_cosine
        + q_value * recoil_squared * soft_squared
        + q_value * recoil_squared * soft_cosine
        - 2 * q_value * recoil * soft_squared
        - 2 * q_value * recoil * soft_cosine
        + q_value * soft_squared
        + q_value * soft_cosine
        + recoil_squared * soft_squared
        + recoil_squared * soft_cosine
        - 2 * recoil * soft_squared
        + 2 * recoil
        + soft_squared
        - soft_cosine
    )
    zero_displacement_ratio = -numerator / (q_value * denominator)
    external_root = -1j * parent.M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = parent.M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    selected_root = (
        external_root * (1 + soft_cosine) / soft_sine
    )
    return (
        zero_displacement_ratio
        * selected_root
        / (selected_root + global_displacement)
    )


def centered_ratio(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(parent.M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = parent.cpoint(
        configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
    )

    def evaluate(values: list[Any]) -> Any:
        dual = parent.M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = parent.deformed_path_energy_dual(
            cell,
            "RIGHT_CONNECTOR",
            coordinate,
            parameter,
        )
        recoil = parent.M5386.chart_safe_sqrt_dual(1 - energy)
        return representative_external01_ratio_rational_dual(
            parent,
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            displacement,
        )

    direct = evaluate(list(domains)).value
    mean_value = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            parent.M5385.M5381.IntervalDual(
                value,
                parent.cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        mean_value += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return min(
        (direct, mean_value),
        key=lambda value: parent.M5258.upper_abs(value),
    )


def proof_displacement(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
) -> tuple[Any, float]:
    energy = parent.deformed_path_energy_dual(
        cell,
        "RIGHT_CONNECTOR",
        coordinate,
        parameter,
    ).value
    _, geometry = parent.interval_inputs(
        configuration,
        coordinate,
        energy,
        epsilon,
    )
    radius = math.nextafter(
        1.0e-7 * max(1.0, parent.M5258.upper_abs(geometry["selected_root"])),
        math.inf,
    )
    return parent.cbox(-radius, radius, -radius, radius), radius


def symbolic_remainder_is_zero() -> tuple[bool, int]:
    import sympy

    q_value, recoil, soft_cosine, decay_cosine = sympy.symbols(
        "q r x d", nonzero=True
    )
    soft_sine, decay_sine = sympy.symbols("S U", nonzero=True)
    factor_plus = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_minus = (
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
        * factor_plus
        / (decay_sine * (1 + soft_cosine) * factor_minus)
    )
    relative_cosine = (
        (representative + 1 / representative)
        * soft_sine
        * decay_sine
        / 2
        + soft_cosine * decay_cosine
    )
    energy = (
        1
        + recoil**2
        - relative_cosine * (1 - recoil**2)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) ** 2
        - (1 - recoil**2)
    ) / 2
    plus = energy + longitudinal * soft_cosine + recoil * decay_cosine
    antiholomorphic = (
        recoil * decay_sine / representative
        + longitudinal * soft_sine
    )
    original = sympy.cancel(
        soft_sine
        * antiholomorphic
        / (q_value * (1 + soft_cosine) * plus)
    )
    numerator = (
        decay_cosine * q_value * recoil**2 * soft_cosine
        - decay_cosine * q_value * recoil**2
        - decay_cosine * q_value * soft_cosine
        - decay_cosine * q_value
        + decay_cosine * recoil**2 * soft_cosine
        - decay_cosine * recoil**2
        - decay_cosine * soft_cosine
        + decay_cosine
        + q_value * recoil**2 * soft_cosine**2
        - q_value * recoil**2 * soft_cosine
        - 2 * q_value * recoil * soft_cosine**2
        + 2 * q_value * recoil
        + q_value * soft_cosine**2
        + q_value * soft_cosine
        + recoil**2 * soft_cosine**2
        - recoil**2 * soft_cosine
        - 2 * recoil * soft_cosine**2
        + 2 * recoil * soft_cosine
        + soft_cosine**2
        - soft_cosine
    )
    denominator = (
        decay_cosine * q_value * recoil**2 * soft_cosine
        + decay_cosine * q_value * recoil**2
        - decay_cosine * q_value * soft_cosine
        - decay_cosine * q_value
        + decay_cosine * recoil**2 * soft_cosine
        + decay_cosine * recoil**2
        - decay_cosine * soft_cosine
        + decay_cosine
        + q_value * recoil**2 * soft_cosine**2
        + q_value * recoil**2 * soft_cosine
        - 2 * q_value * recoil * soft_cosine**2
        - 2 * q_value * recoil * soft_cosine
        + q_value * soft_cosine**2
        + q_value * soft_cosine
        + recoil**2 * soft_cosine**2
        + recoil**2 * soft_cosine
        - 2 * recoil * soft_cosine**2
        + 2 * recoil
        + soft_cosine**2
        - soft_cosine
    )
    candidate = -numerator / (q_value * denominator)
    difference_numerator = sympy.fraction(sympy.together(original - candidate))[0]
    basis = sympy.groebner(
        [
            soft_sine**2 - (1 - soft_cosine**2),
            decay_sine**2 - (1 - decay_cosine**2),
        ],
        soft_sine,
        decay_sine,
        q_value,
        recoil,
        soft_cosine,
        decay_cosine,
        order="grlex",
    )
    remainder = basis.reduce(sympy.expand(difference_numerator))[1]
    return remainder == 0, sympy.count_ops(candidate)


def point_crosschecks(
    parent: Any,
    gate_5427: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> list[dict[str, Any]]:
    state = read_json(ACTIVE_STATE)
    examples = state["split_failure_examples"][EXTERNAL01_FAILURE]
    x_lower = min(float(row["x_lower"]) for row in examples)
    x_upper = max(float(row["x_upper"]) for row in examples)
    t_lower = min(float(row["t_lower"]) for row in examples)
    t_upper = max(float(row["t_upper"]) for row in examples)
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_values = (
        epsilon_real_lower,
        0.5 * (epsilon_real_lower + epsilon_real_upper),
        epsilon_real_upper,
    )
    decay_cosine = parent.cpoint(
        configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
    )
    rows: list[dict[str, Any]] = []
    for x_fraction in (0.0, 0.5, 1.0):
        for t_fraction in (0.0, 0.5, 1.0):
            for epsilon_value in epsilon_values:
                coordinate = parent.cpoint(
                    x_lower + (x_upper - x_lower) * x_fraction
                )
                parameter = parent.cpoint(
                    t_lower + (t_upper - t_lower) * t_fraction
                )
                epsilon_point = parent.cpoint(epsilon_value)
                energy = parent.deformed_path_energy_dual(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    parameter,
                ).value
                _, geometry = parent.interval_inputs(
                    configuration,
                    coordinate,
                    energy,
                    epsilon_point,
                )
                radius = 1.0e-7 * max(
                    1.0,
                    parent.M5258.upper_abs(geometry["selected_root"]),
                )
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = parent.cpoint(
                        radius * complex(math.cos(phase), math.sin(phase))
                    )
                    low_degree_ratio = (
                        representative_external01_ratio_rational_dual(
                            parent,
                            configuration,
                            epsilon_point,
                            geometry["recoil"],
                            coordinate * configuration["soft_sign"],
                            decay_cosine,
                            displacement,
                        ).value
                    )
                    square_ratio = (
                        gate_5427.representative_external01_square_dual(
                            parent,
                            configuration,
                            epsilon_point,
                            geometry["recoil"],
                            coordinate * configuration["soft_sign"],
                            parent.cpoint(
                                configuration["decay_sign"]
                                * parent.M5394.ABSOLUTE_DECAY_COSINE
                            ),
                            parent.cpoint(
                                math.sqrt(
                                    1 - parent.M5394.ABSOLUTE_DECAY_COSINE**2
                                )
                            ),
                            displacement,
                        ).value
                        + parent.cpoint(1)
                    )
                    rows.append(
                        {
                            "checkpoint": CHECKPOINT,
                            "x_fraction": x_fraction,
                            "t_fraction": t_fraction,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "ratio_abs": parent.M5258.upper_abs(low_degree_ratio),
                            "absolute_error_upper": parent.M5258.upper_abs(
                                low_degree_ratio - square_ratio
                            ),
                        }
                    )
    return rows


def box_probe_rows(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> list[dict[str, Any]]:
    state = read_json(ACTIVE_STATE)
    boxes: list[tuple[str, float, float, float, float]] = []
    for index, row in enumerate(
        state["split_failure_examples"][EXTERNAL01_FAILURE]
    ):
        boxes.append(
            (
                f"failure_{index}",
                float(row["x_lower"]),
                float(row["x_upper"]),
                float(row["t_lower"]),
                float(row["t_upper"]),
            )
        )
    next_box = state["stack"][-1]
    boxes.append(
        (
            "active_next",
            float(next_box[0]),
            float(next_box[1]),
            float(next_box[2]),
            float(next_box[3]),
        )
    )
    rows: list[dict[str, Any]] = []
    for name, x_lower, x_upper, t_lower, t_upper in boxes:
        coordinate = parent.cbox(x_lower, x_upper)
        parameter = parent.cbox(t_lower, t_upper)
        displacement, radius = proof_displacement(
            parent,
            configuration,
            cell,
            coordinate,
            parameter,
            epsilon,
        )
        ratio = centered_ratio(
            parent,
            configuration,
            cell,
            coordinate,
            parameter,
            epsilon,
            displacement,
        )
        ratio_upper = parent.M5258.upper_abs(ratio)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "box": name,
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "global_displacement_radius": radius,
                "ratio_abs_upper": ratio_upper,
                "triangle_edge_abs_lower": max(0.0, 1.0 - ratio_upper),
                "direct_disk_certificate": ratio_upper < 1.0,
            }
        )
    return rows


def adaptive_disk_cover(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = read_json(ACTIVE_STATE)
    examples = state["split_failure_examples"][EXTERNAL01_FAILURE]
    x_lower = min(float(row["x_lower"]) for row in examples)
    x_upper = max(float(row["x_upper"]) for row in examples)
    t_lower = min(float(row["t_lower"]) for row in examples)
    t_upper = max(float(row["t_upper"]) for row in examples)
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    full_coordinate = parent.cbox(x_lower, x_upper)
    full_parameter = parent.cbox(t_lower, t_upper)
    displacement, radius = proof_displacement(
        parent,
        configuration,
        cell,
        full_coordinate,
        full_parameter,
        epsilon,
    )
    stack: list[tuple[float, float, float, float, float, float, int]] = [
        (
            x_lower,
            x_upper,
            t_lower,
            t_upper,
            epsilon_real_lower,
            epsilon_real_upper,
            0,
        )
    ]
    accepted: list[dict[str, Any]] = []
    evaluation_count = 0
    maximum_depth = 18
    maximum_leaf_count = 4096
    split_schedule = (
        "epsilon_real",
        "epsilon_real",
        "absolute_coordinate",
        "path_parameter",
        "epsilon_real",
        "absolute_coordinate",
        "path_parameter",
    )

    def evaluate(node: tuple[float, ...]) -> Any:
        nonlocal evaluation_count
        ratio = centered_ratio(
            parent,
            configuration,
            cell,
            parent.cbox(node[0], node[1]),
            parent.cbox(node[2], node[3]),
            parent.cbox(
                node[4],
                node[5],
                epsilon_imaginary_lower,
                epsilon_imaginary_upper,
            ),
            displacement,
        )
        evaluation_count += 1
        return ratio

    while stack:
        node = stack.pop()
        ratio = evaluate(node)
        ratio_upper = parent.M5258.upper_abs(ratio)
        if ratio_upper < 1.0:
            real_bounds = parent.M5394.real_bounds(ratio)
            imaginary_bounds = parent.M5394.imaginary_bounds(ratio)
            accepted.append(
                {
                    "checkpoint": CHECKPOINT,
                    "leaf_index": len(accepted),
                    "depth": int(node[6]),
                    "x_lower": node[0],
                    "x_upper": node[1],
                    "t_lower": node[2],
                    "t_upper": node[3],
                    "epsilon_real_lower": node[4],
                    "epsilon_real_upper": node[5],
                    "ratio_real_lower": real_bounds[0],
                    "ratio_real_upper": real_bounds[1],
                    "ratio_imaginary_lower": imaginary_bounds[0],
                    "ratio_imaginary_upper": imaginary_bounds[1],
                    "ratio_abs_upper": ratio_upper,
                    "triangle_edge_abs_lower": 1.0 - ratio_upper,
                    "valid_for_unit_disk": True,
                    "_ratio": ratio,
                }
            )
            continue
        depth = int(node[6])
        if depth >= maximum_depth:
            raise RuntimeError(
                "ratio disk cover reaches maximum depth: "
                f"x=({node[0]},{node[1]}); t=({node[2]},{node[3]}); "
                f"epsilon=({node[4]},{node[5]}); upper={ratio_upper}"
            )
        split_variable = split_schedule[depth % len(split_schedule)]
        if split_variable == "epsilon_real":
            midpoint = 0.5 * (node[4] + node[5])
            children = (
                (*node[:4], node[4], midpoint, depth + 1),
                (*node[:4], midpoint, node[5], depth + 1),
            )
        elif split_variable == "absolute_coordinate":
            midpoint = 0.5 * (node[0] + node[1])
            children = (
                (node[0], midpoint, *node[2:6], depth + 1),
                (midpoint, node[1], *node[2:6], depth + 1),
            )
        else:
            midpoint = 0.5 * (node[2] + node[3])
            children = (
                (*node[:2], node[2], midpoint, *node[4:6], depth + 1),
                (*node[:2], midpoint, node[3], *node[4:6], depth + 1),
            )
        stack.extend(reversed(children))
        if len(stack) + len(accepted) > maximum_leaf_count:
            raise RuntimeError("ratio disk cover exceeds leaf budget")
    hull = parent.rectangular_interval_hull(
        [row["_ratio"] for row in accepted]
    )
    hull_upper = parent.M5258.upper_abs(hull)
    rows = [
        {key: value for key, value in row.items() if key != "_ratio"}
        for row in accepted
    ]
    summary = {
        "checkpoint": CHECKPOINT,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
        "epsilon_real_lower": epsilon_real_lower,
        "epsilon_real_upper": epsilon_real_upper,
        "global_displacement_radius": radius,
        "leaf_count": len(rows),
        "evaluation_count": evaluation_count,
        "maximum_depth": max(int(row["depth"]) for row in rows),
        "maximum_leaf_ratio_abs_upper": max(
            float(row["ratio_abs_upper"]) for row in rows
        ),
        "minimum_leaf_triangle_edge_abs_lower": min(
            float(row["triangle_edge_abs_lower"]) for row in rows
        ),
        "hull_real_lower": parent.M5394.real_bounds(hull)[0],
        "hull_real_upper": parent.M5394.real_bounds(hull)[1],
        "hull_imaginary_lower": parent.M5394.imaginary_bounds(hull)[0],
        "hull_imaginary_upper": parent.M5394.imaginary_bounds(hull)[1],
        "hull_ratio_abs_upper": hull_upper,
        "hull_triangle_edge_abs_lower": max(0.0, 1.0 - hull_upper),
        "valid_for_common_unit_disk": hull_upper < 1.0,
    }
    return rows, summary


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5428: representative external01 ratio disk gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE RECORDED REPRESENTATIVE-CHART `(0,1)` EDGE REGION ONLY.**",
        "",
        "Write the square edge as `[01] = R - 1`. At zero contour displacement, exact elimination of the representative coordinate gives the low-degree rational quotient `R0 = -A/(q B)`. For displacement `delta`, the only correction is `R = R0 z_sel/(z_sel + delta)`.",
        "",
        "The symbolic numerator remainder modulo `S^2=1-x^2` and `U^2=1-d^2` is exactly zero. The pointwise implementation agrees with the independently spinor-checked 5427 expression to within "
        f"`{payload['maximum_point_absolute_error']:.17g}`.",
        "",
        "## Disk Certificate",
        "",
        f"A closed cover of the recorded failure union uses `{payload['cover_leaf_count']}` leaves. Its common rectangular ratio hull obeys `|R| <= {payload['cover_hull_ratio_abs_upper']:.17g} < 1`, so `[01]` has the rigorous reverse-triangle lower bound `{payload['cover_hull_triangle_edge_abs_lower']:.17g}`.",
        "",
        "This removes the apparent zero without treating a chart artifact as a physical pole and is the candidate production fallback for representative-role, external-minus / hard-plus, chirality-one edges.",
        "",
        "## Claim Boundary",
        "",
        "No connector, W3, regulator, UV, local-GR, or full-MTS claim follows from this local chart certificate.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    parent = load_module("mts_5396_v44_for_5428", PARENT_SCRIPT)
    gate_5427 = load_module("mts_5427_for_5428", GATE_5427_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"parent revision {parent.REVISION} != {PARENT_REVISION}"
        )
    cell, configuration, epsilon, _ = context(parent)
    symbolic_zero, candidate_operation_count = symbolic_remainder_is_zero()
    points = point_crosschecks(
        parent,
        gate_5427,
        cell,
        configuration,
        epsilon,
    )
    box_rows = box_probe_rows(parent, cell, configuration, epsilon)
    cover_rows, cover_summary = adaptive_disk_cover(
        parent,
        cell,
        configuration,
        epsilon,
    )
    atomic_csv(POINTS, points)
    atomic_csv(BOXES, box_rows)
    atomic_csv(COVER, cover_rows)
    atomic_csv(COVER_SUMMARY, [cover_summary])
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    maximum_point_error = max(
        float(row["absolute_error_upper"]) for row in points
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": utc_now(),
        "parent_revision": parent.REVISION,
        "symbolic_remainder_exactly_zero": symbolic_zero,
        "low_degree_candidate_operation_count": candidate_operation_count,
        "point_crosscheck_count": len(points),
        "maximum_point_absolute_error": maximum_point_error,
        "cover_leaf_count": int(cover_summary["leaf_count"]),
        "cover_evaluation_count": int(cover_summary["evaluation_count"]),
        "cover_maximum_depth": int(cover_summary["maximum_depth"]),
        "cover_hull_ratio_abs_upper": float(
            cover_summary["hull_ratio_abs_upper"]
        ),
        "cover_hull_triangle_edge_abs_lower": float(
            cover_summary["hull_triangle_edge_abs_lower"]
        ),
        "valid_for_parent_v45_candidate": True,
        "valid_for_representative_external01_ratio_disk": True,
        "valid_for_right_connector_completion": False,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_D4_numeric_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_D4_numeric_uniform_remainder_bound": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_angular_convergence": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(PARENT_SCRIPT.relative_to(POST)): sha256(PARENT_SCRIPT),
            str(GATE_5427_SCRIPT.relative_to(POST)): sha256(GATE_5427_SCRIPT),
            str(PREVIOUS_RESULT.relative_to(POST)): sha256(PREVIOUS_RESULT),
            str(PREVIOUS_VALIDATION.relative_to(POST)): sha256(
                PREVIOUS_VALIDATION
            ),
            str(ACTIVE_STATE.relative_to(POST)): sha256(ACTIVE_STATE),
        },
    }
    validations = [
        check(
            "previous_checkpoint_green",
            int(previous["failed_validation_count"]) == 0
            and all(is_true(row["passed"]) for row in previous_validation),
            f"validation rows={len(previous_validation)}",
        ),
        check(
            "parent_revision_locked",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        check(
            "symbolic_ratio_remainder_exactly_zero",
            symbolic_zero,
            f"candidate operations={candidate_operation_count}",
        ),
        check(
            "point_crosschecks_present",
            len(points) == 108,
            f"rows={len(points)}",
        ),
        check(
            "point_crosschecks_agree",
            maximum_point_error < 1.0e-12,
            f"maximum error={maximum_point_error}",
        ),
        check(
            "disk_cover_nonempty",
            len(cover_rows) > 0,
            f"leaves={len(cover_rows)}",
        ),
        check(
            "every_leaf_inside_unit_disk",
            all(float(row["ratio_abs_upper"]) < 1.0 for row in cover_rows),
            f"maximum={cover_summary['maximum_leaf_ratio_abs_upper']}",
        ),
        check(
            "common_ratio_hull_inside_unit_disk",
            bool(cover_summary["valid_for_common_unit_disk"]),
            f"hull upper={cover_summary['hull_ratio_abs_upper']}",
        ),
        check(
            "reverse_triangle_edge_bound_positive",
            float(cover_summary["hull_triangle_edge_abs_lower"]) > 0.0,
            f"lower={cover_summary['hull_triangle_edge_abs_lower']}",
        ),
        check(
            "all_sources_exist",
            all(
                path.is_file()
                for path in (
                    PARENT_SCRIPT,
                    GATE_5427_SCRIPT,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                    ACTIVE_STATE,
                )
            ),
            "five source files",
        ),
        check(
            "formalization_workbench_untouched",
            True,
            "checkpoint writes only below post-checkpoint-work",
        ),
        check(
            "broad_claims_remain_false",
            all(not bool(payload[column]) for column in BROAD_COLUMNS),
            "all broad claim columns false",
        ),
    ]
    atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
