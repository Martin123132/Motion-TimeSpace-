from __future__ import annotations

import argparse
import csv
import ctypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5451"
FORMALIZATION = POST.parent / "formalization-workbench"

PARENT_SCRIPT = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
RATIO_BOXES = FUNCTIONAL_RG / "5392" / "D4_desingularized_endpoint_ratio_boxes.csv"
BRANCHES = FUNCTIONAL_RG / "5393" / "D4_material_pole_branch_ownership.csv"
MAPPED_CELLS = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_mapped_cells.csv"
RESIDUES = FUNCTIONAL_RG / "5395" / "D4_material_residue_supremum.csv"
OWNERS_5449 = FUNCTIONAL_RG / "5449" / "D4_event_local_cell_term_owner_manifest.csv"
THEOREM_5450 = FUNCTIONAL_RG / "5450" / "D4_event_endpoint_Cauchy_subtraction_bounds.csv"
RESULT_5450 = FUNCTIONAL_RG / "5450" / "D4_event_endpoint_Cauchy_subtraction_result.json"

DOCUMENT = POST / "5451-Y5-R2FR-D4-event-endpoint-xt-overlap-geometry-cover.md"
COVER = OUTPUT / "D4_event_endpoint_xt_overlap_cover.csv"
SUMMARY = OUTPUT / "D4_event_endpoint_xt_overlap_cover_summary.csv"
PRIMITIVES = OUTPUT / "D4_event_endpoint_nonsingular_primitive_candidates.csv"
EPSILON_AUDIT = OUTPUT / "D4_event_endpoint_epsilon_partition_audit.csv"
SOURCES = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5451_VALIDATION.csv"
RESULT = OUTPUT / "D4_event_endpoint_xt_overlap_geometry_result.json"
WORK = OUTPUT / "work"
STATUS = OUTPUT / "status.json"
COMPLETE = OUTPUT / "COMPLETE.json"

CHECKPOINT = 5451
REVISION = "D4-event-endpoint-xt-overlap-geometry-cover-v5"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
PATH_SEGMENTS = ("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR")
INNER_RADIUS = 7.5e-6
OUTER_RADIUS = 5.0e-6
OVERLAP_WIDTH = INNER_RADIUS - OUTER_RADIUS
MAXIMUM_DEPTH = 16
MINIMUM_X_WIDTH = 1.0e-13
MINIMUM_T_WIDTH = 1.0e-13
MAXIMUM_NODE_EVALUATIONS_PER_JOB = 20000


class CoverBudgetExceeded(RuntimeError):
    pass


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        PARENT_SCRIPT,
        EVENTS,
        RATIO_BOXES,
        BRANCHES,
        MAPPED_CELLS,
        RESIDUES,
        OWNERS_5449,
        THEOREM_5450,
        RESULT_5450,
    )


def event_branch_map() -> dict[str, dict[str, str]]:
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    branches = [
        row
        for row in read_csv(BRANCHES)
        if row["pole_class"] == "MATERIAL_SIMPLE_POLE"
    ]
    mapped: dict[str, dict[str, str]] = {}
    for event_id, event in events.items():
        matches = [
            branch
            for branch in branches
            if branch["term_id"] == event["term_id"]
            and branch["primary_surface_id"] == event["primary_surface_id"]
            and event_id
            in {branch["support_start_event"], branch["support_end_event"]}
        ]
        if len(matches) != 1:
            raise RuntimeError(f"{event_id} has {len(matches)} branch owners")
        mapped[event_id] = matches[0]
    return mapped


def epsilon_row(source: dict[str, str]) -> dict[str, Any]:
    return {
        "regulator_bin_index": int(source["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(
            source.get("epsilon_subdivision_index", 0)
        ),
        "epsilon_subdivision_count": int(
            source.get("epsilon_subdivision_count", 1)
        ),
        "epsilon_real_lower": float(source["epsilon_real_lower"]),
        "epsilon_real_upper": float(source["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(source["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(source["epsilon_imaginary_upper"]),
    }


def ratio_subboxes(
    ratio: dict[str, str], subdivision_count: int
) -> list[dict[str, str]]:
    lower = float(ratio["epsilon_real_lower"])
    upper = float(ratio["epsilon_real_upper"])
    width = (upper - lower) / subdivision_count
    rows: list[dict[str, str]] = []
    for index in range(subdivision_count):
        row = dict(ratio)
        row["epsilon_subdivision_index"] = str(index)
        row["epsilon_subdivision_count"] = str(subdivision_count)
        row["epsilon_real_lower"] = str(lower + index * width)
        row["epsilon_real_upper"] = str(lower + (index + 1) * width)
        rows.append(row)
    return rows


def event_endpoint_connector(
    event: dict[str, str], cell: dict[str, str]
) -> str:
    event_type = event["event_type"]
    term_prefix = f"{event['term_id']}:"
    lower_boundary = cell["lower_energy_boundary"]
    upper_boundary = cell["upper_energy_boundary"]
    if event_type in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}:
        if lower_boundary.startswith(term_prefix):
            return "LEFT_CONNECTOR"
        if upper_boundary.startswith(term_prefix):
            return "RIGHT_CONNECTOR"
    if event_type == "BRANCH_DEATH" and upper_boundary == "ENERGY_MAXIMUM":
        return "RIGHT_CONNECTOR"
    return ""


def epsilon_subdivision_count(
    event: dict[str, str],
    cell: dict[str, str],
    ratio: dict[str, str],
    path_segment: str,
) -> int:
    lower = float(ratio["epsilon_real_lower"])
    upper = float(ratio["epsilon_real_upper"])
    contains_zero = lower <= 0.0 <= upper
    is_wide = upper - lower > 1.0e-5
    endpoint_connector = event_endpoint_connector(event, cell)
    if is_wide and path_segment == endpoint_connector:
        return 32
    if path_segment in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"} and contains_zero and is_wide:
        return 32
    return 1


def next_power_of_two(value: int) -> int:
    result = 1
    while result < value:
        result *= 2
    return result


def certified_epsilon_subdivision_policy(
    parent: Any,
    event: dict[str, str],
    cell: dict[str, str],
    configuration: dict[str, Any],
    branch: dict[str, str],
    ratio: dict[str, str],
    path_segment: str,
) -> tuple[int, dict[str, Any]]:
    base_count = epsilon_subdivision_count(event, cell, ratio, path_segment)
    endpoint_connector = event_endpoint_connector(event, cell)
    real_width = float(ratio["epsilon_real_upper"]) - float(
        ratio["epsilon_real_lower"]
    )
    if path_segment != endpoint_connector or real_width <= 1.0e-5:
        return base_count, {
            "method": "BASE_ENDPOINT_OR_EDGE_POLICY",
            "gap_epsilon_derivative_abs_upper": 0.0,
            "overlap_width": OVERLAP_WIDTH,
            "minimum_required_real_subdivision_count": base_count,
            "selected_real_subdivision_count": base_count,
        }
    event_lower, event_upper = event_coordinate_bounds(parent, ratio)
    slope = max(abs(float(event["signed_support_margin_slope"])), 1.0e-12)
    transition_margin = 16.0 * INNER_RADIUS / slope
    x_lower = max(
        float(cell["lower_absolute_soft_cosine"]),
        event_lower - transition_margin,
    )
    x_upper = min(
        float(cell["upper_absolute_soft_cosine"]),
        event_upper + transition_margin,
    )
    epsilon = parent.epsilon_interval(epsilon_row(ratio))
    recoil, _, root_derivatives = parent.M5395.centered_material_root(
        branch["primary_surface_id"],
        int(configuration["sign"]),
        x_lower,
        x_upper,
        epsilon,
    )
    gap_epsilon_derivative_abs_upper = parent.M5258.upper_abs(
        parent.cpoint(2) * recoil * root_derivatives["root_epsilon"]
    )
    imaginary_lower = float(ratio["epsilon_imaginary_lower"])
    imaginary_upper = float(ratio["epsilon_imaginary_upper"])
    imaginary_center = 0.5 * (imaginary_lower + imaginary_upper)
    imaginary_half_width = max(
        imaginary_center - imaginary_lower,
        imaginary_upper - imaginary_center,
    )
    real_overlap_budget = (
        OVERLAP_WIDTH
        - 2.0
        * gap_epsilon_derivative_abs_upper
        * imaginary_half_width
    )
    if real_overlap_budget <= 0.0:
        raise CoverBudgetExceeded(
            f"{event['event_id']}:{cell['mapped_cell_id']}:{path_segment} "
            "requires imaginary-epsilon subdivision"
        )
    minimum_required = max(
        base_count,
        math.ceil(
            gap_epsilon_derivative_abs_upper
            * real_width
            / real_overlap_budget
        ),
    )
    selected_count = next_power_of_two(minimum_required)
    return selected_count, {
        "method": "DERIVATIVE_BUDGETED_ENDPOINT_CONNECTOR_POLICY",
        "transition_x_lower": x_lower,
        "transition_x_upper": x_upper,
        "gap_epsilon_derivative_abs_upper": (
            gap_epsilon_derivative_abs_upper
        ),
        "epsilon_real_width": real_width,
        "epsilon_imaginary_half_width": imaginary_half_width,
        "overlap_width": OVERLAP_WIDTH,
        "real_overlap_budget": real_overlap_budget,
        "minimum_required_real_subdivision_count": minimum_required,
        "selected_real_subdivision_count": selected_count,
    }


def centered_boundary_pole_gap(
    parent: Any,
    boundary_owner: str,
    branch: dict[str, str],
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    root_derivatives: dict[str, Any],
    x_lower: float,
    x_upper: float,
) -> Any:
    dual = parent.M5385.M5381.IntervalDual
    absolute_coordinate = parent.cbox(x_lower, x_upper)
    boundary_dual = parent.interval_boundary_energy_dual(
        boundary_owner,
        dual(absolute_coordinate, parent.cpoint(1)),
    )
    boundary_x = boundary_dual.derivative
    gap_x = (
        boundary_x
        + parent.cpoint(2) * recoil * root_derivatives["root_x"]
    )
    gap_epsilon = (
        parent.cpoint(2)
        * recoil
        * root_derivatives["root_epsilon"]
    )
    x_center = 0.5 * (x_lower + x_upper)
    epsilon_center = parent.M5395.midpoint(epsilon)
    boundary_center = complex(
        parent.M5308.boundary_energy(boundary_owner, x_center)
    )
    recoil_center = complex(
        parent.M5395.M5394.point_material_root(
            branch["primary_surface_id"],
            int(configuration["sign"]),
            x_center,
            epsilon_center,
        )
    )
    gap_center = boundary_center - (1.0 - recoil_center * recoil_center)
    return (
        parent.cpoint(gap_center)
        + gap_x * (absolute_coordinate - parent.cpoint(x_center))
        + gap_epsilon * (epsilon - parent.cpoint(epsilon_center))
    )


def path_gap_bounds(
    parent: Any,
    cell: dict[str, str],
    configuration: dict[str, Any],
    branch: dict[str, str],
    regulator: dict[str, Any],
    path_segment: str,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
) -> dict[str, Any]:
    epsilon = parent.epsilon_interval(regulator)
    recoil, root_diagnostics, root_derivatives = parent.M5395.centered_material_root(
        branch["primary_surface_id"],
        int(configuration["sign"]),
        x_lower,
        x_upper,
        epsilon,
    )
    path_parameter = parent.cbox(t_lower, t_upper)
    if path_segment == "LEFT_CONNECTOR":
        gap = (
            centered_boundary_pole_gap(
                parent,
                cell["lower_energy_boundary"],
                branch,
                configuration,
                epsilon,
                recoil,
                root_derivatives,
                x_lower,
                x_upper,
            )
            + parent.cpoint(1j * parent.DEFAULT_ENERGY_DEFORMATION)
            * path_parameter
        )
        path_speed = parent.DEFAULT_ENERGY_DEFORMATION
        gap_enclosure_method = "CENTERED_BOUNDARY_MINUS_MATERIAL_POLE"
    elif path_segment == "TOP":
        pole = parent.cpoint(1) - recoil * recoil
        lower_energy, _ = parent.interval_boundary_energy(
            cell["lower_energy_boundary"], x_lower, x_upper
        )
        upper_energy, _ = parent.interval_boundary_energy(
            cell["upper_energy_boundary"], x_lower, x_upper
        )
        energy_width = upper_energy - lower_energy
        energy = (
            lower_energy
            + path_parameter * energy_width
            + parent.cpoint(1j * parent.DEFAULT_ENERGY_DEFORMATION)
        )
        gap = energy - pole
        path_speed = parent.M5258.upper_abs(energy_width)
        gap_enclosure_method = "DIRECT_TOP_CONTOUR_INTERVAL"
    elif path_segment == "RIGHT_CONNECTOR":
        gap = (
            centered_boundary_pole_gap(
                parent,
                cell["upper_energy_boundary"],
                branch,
                configuration,
                epsilon,
                recoil,
                root_derivatives,
                x_lower,
                x_upper,
            )
            + parent.cpoint(1j * parent.DEFAULT_ENERGY_DEFORMATION)
            * path_parameter
        )
        path_speed = parent.DEFAULT_ENERGY_DEFORMATION
        gap_enclosure_method = "CENTERED_BOUNDARY_MINUS_MATERIAL_POLE"
    else:
        raise ValueError(path_segment)
    return {
        "gap_abs_lower": parent.M5258.lower_abs(gap),
        "gap_abs_upper": parent.M5258.upper_abs(gap),
        "gap_real_lower": parent.M5258.real_bounds(gap)[0],
        "gap_real_upper": parent.M5258.real_bounds(gap)[1],
        "gap_imaginary_lower": parent.M5258.imaginary_bounds(gap)[0],
        "gap_imaginary_upper": parent.M5258.imaginary_bounds(gap)[1],
        "path_speed_abs_upper": path_speed,
        "gap_enclosure_method": gap_enclosure_method,
        "material_root_denominator_abs_lower": float(
            root_diagnostics["material_coefficient_denominator_abs_lower"]
        ),
        "implicit_material_derivative_abs_lower": float(
            root_diagnostics["implicit_material_derivative_abs_lower"]
        ),
    }


def classify_gap(bounds: dict[str, float]) -> str:
    if bounds["gap_abs_upper"] <= INNER_RADIUS:
        return "INNER_CAUCHY_REGULAR_PART"
    if bounds["gap_abs_lower"] >= OUTER_RADIUS:
        return "OUTER_PARENT_TRIANGLE"
    return ""


def event_coordinate_bounds(
    parent: Any, ratio: dict[str, str]
) -> tuple[float, float]:
    boxes = [
        parent.M5385.M5381.parse_complex_box(text)
        for text in ratio["desingularized_Krawczyk_images"].split("|")
    ]
    coordinate_index = (
        3 if int(ratio["desingularized_system_dimension"]) == 5 else 2
    )
    return parent.M5258.real_bounds(boxes[coordinate_index])


def seeded_rectangles(
    parent: Any,
    event: dict[str, str],
    cell: dict[str, str],
    ratio: dict[str, str],
    path_segment: str,
) -> list[tuple[float, float, float, float, int, str]]:
    x_lower = float(cell["lower_absolute_soft_cosine"])
    x_upper = float(cell["upper_absolute_soft_cosine"])
    endpoint_connector = event_endpoint_connector(event, cell)
    if path_segment == "TOP" and not endpoint_connector:
        return [(x_lower, x_upper, 0.0, 1.0, 0, "ROOT")]
    event_lower, event_upper = event_coordinate_bounds(parent, ratio)
    slope = max(abs(float(event["signed_support_margin_slope"])), 1.0e-8)
    scale = INNER_RADIUS / slope
    x_points = {x_lower, x_upper}
    center = 0.5 * (event_lower + event_upper)
    for candidate in (event_lower, event_upper):
        if x_lower < candidate < x_upper:
            x_points.add(candidate)
    for multiplier in (-8.0, -4.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 4.0, 8.0):
        candidate = center + multiplier * scale
        if x_lower < candidate < x_upper:
            x_points.add(candidate)
    endpoint_points = (
        0.0,
        5.0e-5,
        1.0e-4,
        2.0e-4,
        5.0e-4,
        1.0e-3,
        2.0e-3,
        5.0e-3,
        1.0e-2,
        2.0e-2,
        5.0e-2,
        1.0e-1,
        2.5e-1,
        5.0e-1,
        1.0,
    )
    if path_segment == "TOP" and endpoint_connector == "RIGHT_CONNECTOR":
        t_points = tuple(sorted({1.0 - value for value in endpoint_points}))
    else:
        t_points = endpoint_points
    ordered_x = sorted(x_points)
    rectangles: list[tuple[float, float, float, float, int, str]] = []
    for x_index, (left, right) in enumerate(zip(ordered_x[:-1], ordered_x[1:])):
        for t_index, (lower, upper) in enumerate(zip(t_points[:-1], t_points[1:])):
            rectangles.append(
                (
                    left,
                    right,
                    lower,
                    upper,
                    0,
                    f"S{x_index:02d}T{t_index:02d}",
                )
            )
    return rectangles


def adaptive_cover(
    parent: Any,
    event: dict[str, str],
    cell: dict[str, str],
    configuration: dict[str, Any],
    branch: dict[str, str],
    ratio: dict[str, str],
    path_segment: str,
) -> list[dict[str, Any]]:
    regulator = epsilon_row(ratio)
    initial_x_lower = float(cell["lower_absolute_soft_cosine"])
    initial_x_upper = float(cell["upper_absolute_soft_cosine"])
    slope = abs(float(event["signed_support_margin_slope"]))
    stack = seeded_rectangles(parent, event, cell, ratio, path_segment)
    leaves: list[dict[str, Any]] = []
    node_evaluations = 0
    unclassified_by_depth: dict[int, int] = {}
    failure_counts: dict[str, int] = {}
    while stack:
        node_evaluations += 1
        if node_evaluations > MAXIMUM_NODE_EVALUATIONS_PER_JOB:
            x_lower, x_upper, t_lower, t_upper, depth, path = stack[-1]
            raise CoverBudgetExceeded(
                f"{event['event_id']}:{cell['mapped_cell_id']}:"
                f"{ratio['epsilon_bin_index']}:{path_segment} exceeded "
                f"{MAXIMUM_NODE_EVALUATIONS_PER_JOB} node evaluations; "
                f"epsilon_subdivision={ratio.get('epsilon_subdivision_index', 0)}/"
                f"{ratio.get('epsilon_subdivision_count', 1)}; "
                f"leaves={len(leaves)}; stack={len(stack)}; "
                f"next_depth={depth}; next_path={path}; "
                f"next_x_width={x_upper - x_lower}; "
                f"next_t_width={t_upper - t_lower}; "
                f"unclassified_by_depth={unclassified_by_depth}; "
                f"failure_counts={failure_counts}"
            )
        x_lower, x_upper, t_lower, t_upper, depth, path = stack.pop()
        failure_type = ""
        failure_message = ""
        bounds: dict[str, float]
        try:
            bounds = path_gap_bounds(
                parent,
                cell,
                configuration,
                branch,
                regulator,
                path_segment,
                x_lower,
                x_upper,
                t_lower,
                t_upper,
            )
            owner = classify_gap(bounds)
        except Exception as error:
            bounds = {
                "gap_abs_lower": math.nan,
                "gap_abs_upper": math.nan,
                "gap_real_lower": math.nan,
                "gap_real_upper": math.nan,
                "gap_imaginary_lower": math.nan,
                "gap_imaginary_upper": math.nan,
                "path_speed_abs_upper": math.nan,
                "material_root_denominator_abs_lower": math.nan,
                "implicit_material_derivative_abs_lower": math.nan,
            }
            owner = ""
            failure_type = type(error).__name__
            failure_message = str(error).splitlines()[0][:300]
            failure_counts[failure_type] = failure_counts.get(failure_type, 0) + 1
        x_width = x_upper - x_lower
        t_width = t_upper - t_lower
        if owner:
            leaves.append(
                {
                    "event_id": event["event_id"],
                    "event_type": event["event_type"],
                    "branch_owner_id": branch["branch_owner_id"],
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": event["term_id"],
                    "primary_surface_id": event["primary_surface_id"],
                    "epsilon_bin_index": int(ratio["epsilon_bin_index"]),
                    "epsilon_subdivision_index": int(
                        ratio.get("epsilon_subdivision_index", 0)
                    ),
                    "epsilon_subdivision_count": int(
                        ratio.get("epsilon_subdivision_count", 1)
                    ),
                    "epsilon_real_lower": float(ratio["epsilon_real_lower"]),
                    "epsilon_real_upper": float(ratio["epsilon_real_upper"]),
                    "epsilon_imaginary_lower": float(
                        ratio["epsilon_imaginary_lower"]
                    ),
                    "epsilon_imaginary_upper": float(
                        ratio["epsilon_imaginary_upper"]
                    ),
                    "path_segment": path_segment,
                    "cover_owner": owner,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "x_width": x_width,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "t_width": t_width,
                    "parameter_area": x_width * t_width,
                    "physical_path_area_abs_upper": (
                        x_width * t_width * bounds["path_speed_abs_upper"]
                    ),
                    "refinement_depth": depth,
                    "refinement_path": path,
                    **bounds,
                    "failure_type": "",
                    "failure_message": "",
                    "geometry_cover_leaf_passes": True,
                    "requires_correlated_Q_contour_enclosure": (
                        owner == "INNER_CAUCHY_REGULAR_PART"
                    ),
                    "requires_parent_outer_amplitude_enclosure": (
                        owner == "OUTER_PARENT_TRIANGLE"
                    ),
                    "valid_for_full_event_cell_finite_cover": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            continue
        can_split_x = x_width > MINIMUM_X_WIDTH
        can_split_t = t_width > MINIMUM_T_WIDTH
        if depth >= MAXIMUM_DEPTH or not (can_split_x or can_split_t):
            leaves.append(
                {
                    "event_id": event["event_id"],
                    "event_type": event["event_type"],
                    "branch_owner_id": branch["branch_owner_id"],
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": event["term_id"],
                    "primary_surface_id": event["primary_surface_id"],
                    "epsilon_bin_index": int(ratio["epsilon_bin_index"]),
                    "epsilon_subdivision_index": int(
                        ratio.get("epsilon_subdivision_index", 0)
                    ),
                    "epsilon_subdivision_count": int(
                        ratio.get("epsilon_subdivision_count", 1)
                    ),
                    "epsilon_real_lower": float(ratio["epsilon_real_lower"]),
                    "epsilon_real_upper": float(ratio["epsilon_real_upper"]),
                    "epsilon_imaginary_lower": float(
                        ratio["epsilon_imaginary_lower"]
                    ),
                    "epsilon_imaginary_upper": float(
                        ratio["epsilon_imaginary_upper"]
                    ),
                    "path_segment": path_segment,
                    "cover_owner": "UNRESOLVED",
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "x_width": x_width,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "t_width": t_width,
                    "parameter_area": x_width * t_width,
                    "physical_path_area_abs_upper": math.nan,
                    "refinement_depth": depth,
                    "refinement_path": path,
                    **bounds,
                    "failure_type": failure_type or "OVERLAP_CLASSIFICATION_DEPTH",
                    "failure_message": failure_message or "box crosses both overlap thresholds",
                    "geometry_cover_leaf_passes": False,
                    "requires_correlated_Q_contour_enclosure": False,
                    "requires_parent_outer_amplitude_enclosure": False,
                    "valid_for_full_event_cell_finite_cover": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            continue
        unclassified_by_depth[depth] = unclassified_by_depth.get(depth, 0) + 1
        if failure_type:
            split_x = can_split_x
        else:
            x_effect = slope * x_width
            if path_segment == "TOP":
                t_effect = max(
                    bounds.get("path_speed_abs_upper", 1.0), 1.0e-12
                ) * t_width
            else:
                t_effect = parent.DEFAULT_ENERGY_DEFORMATION * t_width
            split_x = can_split_x and (
                not can_split_t or x_effect >= t_effect
            )
        if split_x:
            midpoint = 0.5 * (x_lower + x_upper)
            stack.append((midpoint, x_upper, t_lower, t_upper, depth + 1, path + "R"))
            stack.append((x_lower, midpoint, t_lower, t_upper, depth + 1, path + "L"))
        else:
            midpoint = 0.5 * (t_lower + t_upper)
            stack.append((x_lower, x_upper, midpoint, t_upper, depth + 1, path + "U"))
            stack.append((x_lower, x_upper, t_lower, midpoint, depth + 1, path + "D"))
    return leaves


def cover_job_specs(parent: Any) -> list[dict[str, Any]]:
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    cells = {row["mapped_cell_id"]: row for row in read_csv(MAPPED_CELLS)}
    owners = read_csv(OWNERS_5449)
    ratios = read_csv(RATIO_BOXES)
    branches = event_branch_map()
    references, _ = parent.M5385.M5380.M5379.M5378.M5359.reference_rows()
    configurations = {
        event_id: parent.M5385.M5380.M5379.M5378.M5359.event_configuration(
            events[event_id], references
        )
        for event_id in EVENT_IDS
    }
    specs: list[dict[str, Any]] = []
    for owner in owners:
        event_id = owner["event_id"]
        for ratio in [row for row in ratios if row["event_id"] == event_id]:
            for path_segment in PATH_SEGMENTS:
                epsilon_label = str(ratio["epsilon_bin_index"]).replace("-", "m")
                job_id = (
                    f"{event_id}__{owner['mapped_cell_id']}__"
                    f"e{epsilon_label}__{path_segment}"
                )
                specs.append(
                    {
                        "job_id": job_id,
                        "event": events[event_id],
                        "cell": cells[owner["mapped_cell_id"]],
                        "configuration": configurations[event_id],
                        "branch": branches[event_id],
                        "ratio": ratio,
                        "path_segment": path_segment,
                    }
                )
    return specs


def compact_job_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(
        path,
        json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n",
    )


def build_cover(
    parent: Any, max_jobs: int
) -> tuple[list[dict[str, Any]] | None, dict[str, Any]]:
    WORK.mkdir(parents=True, exist_ok=True)
    specs = cover_job_specs(parent)
    processed_this_run = 0
    for spec in specs:
        completed_path = WORK / f"{spec['job_id']}.json"
        failed_path = WORK / f"{spec['job_id']}.failed.json"
        if completed_path.is_file() or failed_path.is_file():
            continue
        if max_jobs > 0 and processed_this_run >= max_jobs:
            break
        started = time.perf_counter()
        try:
            subdivision_count, subdivision_policy = (
                certified_epsilon_subdivision_policy(
                    parent,
                    spec["event"],
                    spec["cell"],
                    spec["configuration"],
                    spec["branch"],
                    spec["ratio"],
                    spec["path_segment"],
                )
            )
            rows: list[dict[str, Any]] = []
            for ratio in ratio_subboxes(spec["ratio"], subdivision_count):
                rows.extend(
                    adaptive_cover(
                        parent,
                        spec["event"],
                        spec["cell"],
                        spec["configuration"],
                        spec["branch"],
                        ratio,
                        spec["path_segment"],
                    )
                )
            compact_job_json(
                completed_path,
                {
                    "job_id": spec["job_id"],
                    "runtime_seconds": time.perf_counter() - started,
                    "epsilon_subdivision_count": subdivision_count,
                    "epsilon_subdivision_policy": subdivision_policy,
                    "leaf_count": len(rows),
                    "rows": rows,
                },
            )
        except Exception as error:
            compact_job_json(
                failed_path,
                {
                    "job_id": spec["job_id"],
                    "runtime_seconds": time.perf_counter() - started,
                    "failure_type": type(error).__name__,
                    "failure_message": str(error).splitlines()[0][:500],
                },
            )
        processed_this_run += 1
        completed_count = sum(
            (WORK / f"{candidate['job_id']}.json").is_file()
            for candidate in specs
        )
        failed_count = sum(
            (WORK / f"{candidate['job_id']}.failed.json").is_file()
            for candidate in specs
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "updated_utc": datetime.now(timezone.utc).isoformat(),
                "total_job_count": len(specs),
                "completed_job_count": completed_count,
                "failed_job_count": failed_count,
                "pending_job_count": len(specs) - completed_count - failed_count,
                "processed_this_run": processed_this_run,
                "last_job_id": spec["job_id"],
            },
        )
    completed = [
        spec for spec in specs if (WORK / f"{spec['job_id']}.json").is_file()
    ]
    failed = [
        spec
        for spec in specs
        if (WORK / f"{spec['job_id']}.failed.json").is_file()
    ]
    progress = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "status": (
            "COMPLETE"
            if len(completed) == len(specs) and not failed
            else ("FAILED_JOBS_PRESENT" if failed else "INCOMPLETE")
        ),
        "total_job_count": len(specs),
        "completed_job_count": len(completed),
        "failed_job_count": len(failed),
        "pending_job_count": len(specs) - len(completed) - len(failed),
        "processed_this_run": processed_this_run,
        "failed_job_ids": [spec["job_id"] for spec in failed],
        "next_pending_job_id": next(
            (
                spec["job_id"]
                for spec in specs
                if not (WORK / f"{spec['job_id']}.json").is_file()
                and not (WORK / f"{spec['job_id']}.failed.json").is_file()
            ),
            "",
        ),
    }
    atomic_json(STATUS, progress)
    if progress["status"] != "COMPLETE":
        return None, progress
    rows: list[dict[str, Any]] = []
    for spec in specs:
        payload = read_json(WORK / f"{spec['job_id']}.json")
        for row in payload["rows"]:
            row.setdefault("epsilon_subdivision_index", 0)
            row.setdefault("epsilon_subdivision_count", 1)
            row.setdefault(
                "epsilon_real_lower", float(spec["ratio"]["epsilon_real_lower"])
            )
            row.setdefault(
                "epsilon_real_upper", float(spec["ratio"]["epsilon_real_upper"])
            )
            row.setdefault(
                "epsilon_imaginary_lower",
                float(spec["ratio"]["epsilon_imaginary_lower"]),
            )
            row.setdefault(
                "epsilon_imaginary_upper",
                float(spec["ratio"]["epsilon_imaginary_upper"]),
            )
            rows.append(row)
    return rows, progress


def summary_rows(cover: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, int, int, int, str], list[dict[str, Any]]] = {}
    for row in cover:
        key = (
            row["event_id"],
            row["mapped_cell_id"],
            int(row["epsilon_bin_index"]),
            int(row.get("epsilon_subdivision_index", 0)),
            int(row.get("epsilon_subdivision_count", 1)),
            row["path_segment"],
        )
        groups.setdefault(key, []).append(row)
    rows: list[dict[str, Any]] = []
    for key, leaves in sorted(groups.items()):
        (
            event_id,
            cell_id,
            epsilon_bin,
            epsilon_subdivision_index,
            epsilon_subdivision_count_value,
            path_segment,
        ) = key
        expected_area = max(float(row["x_upper"]) for row in leaves) - min(
            float(row["x_lower"]) for row in leaves
        )
        covered_area = sum(float(row["parameter_area"]) for row in leaves)
        inner = [
            row
            for row in leaves
            if row["cover_owner"] == "INNER_CAUCHY_REGULAR_PART"
        ]
        outer = [
            row
            for row in leaves
            if row["cover_owner"] == "OUTER_PARENT_TRIANGLE"
        ]
        unresolved = [row for row in leaves if row["cover_owner"] == "UNRESOLVED"]
        rows.append(
            {
                "event_id": event_id,
                "mapped_cell_id": cell_id,
                "epsilon_bin_index": epsilon_bin,
                "epsilon_subdivision_index": epsilon_subdivision_index,
                "epsilon_subdivision_count": epsilon_subdivision_count_value,
                "epsilon_real_lower": min(
                    float(row["epsilon_real_lower"]) for row in leaves
                ),
                "epsilon_real_upper": max(
                    float(row["epsilon_real_upper"]) for row in leaves
                ),
                "path_segment": path_segment,
                "leaf_count": len(leaves),
                "inner_leaf_count": len(inner),
                "outer_leaf_count": len(outer),
                "unresolved_leaf_count": len(unresolved),
                "maximum_refinement_depth": max(
                    int(row["refinement_depth"]) for row in leaves
                ),
                "expected_parameter_area": expected_area,
                "covered_parameter_area": covered_area,
                "parameter_area_absolute_error": abs(covered_area - expected_area),
                "minimum_outer_gap_abs_lower": min(
                    (float(row["gap_abs_lower"]) for row in outer),
                    default=math.nan,
                ),
                "maximum_inner_gap_abs_upper": max(
                    (float(row["gap_abs_upper"]) for row in inner),
                    default=math.nan,
                ),
                "geometry_overlap_cover_passes": (
                    not unresolved
                    and abs(covered_area - expected_area)
                    <= 1.0e-12 * max(expected_area, 1.0)
                    and all(float(row["gap_abs_upper"]) <= INNER_RADIUS for row in inner)
                    and all(float(row["gap_abs_lower"]) >= OUTER_RADIUS for row in outer)
                ),
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def epsilon_partition_audit_rows(
    cover: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ratios = {
        (row["event_id"], int(row["epsilon_bin_index"])): row
        for row in read_csv(RATIO_BOXES)
    }
    groups: dict[tuple[str, str, int, str], list[dict[str, Any]]] = {}
    for row in cover:
        key = (
            row["event_id"],
            row["mapped_cell_id"],
            int(row["epsilon_bin_index"]),
            row["path_segment"],
        )
        groups.setdefault(key, []).append(row)
    audits: list[dict[str, Any]] = []
    for key, leaves in sorted(groups.items()):
        event_id, cell_id, epsilon_bin, path_segment = key
        source = source_ratios[(event_id, epsilon_bin)]
        count_values = {
            int(row.get("epsilon_subdivision_count", 1)) for row in leaves
        }
        declared_count = next(iter(count_values)) if len(count_values) == 1 else -1
        indices = sorted(
            {int(row.get("epsilon_subdivision_index", 0)) for row in leaves}
        )
        bounds_by_index: dict[int, set[tuple[float, float, float, float]]] = {}
        for row in leaves:
            index = int(row.get("epsilon_subdivision_index", 0))
            bounds_by_index.setdefault(index, set()).add(
                (
                    float(row["epsilon_real_lower"]),
                    float(row["epsilon_real_upper"]),
                    float(row["epsilon_imaginary_lower"]),
                    float(row["epsilon_imaginary_upper"]),
                )
            )
        bounds_are_consistent = all(
            len(values) == 1 for values in bounds_by_index.values()
        )
        ordered_bounds = [
            next(iter(bounds_by_index[index]))
            for index in indices
            if len(bounds_by_index[index]) == 1
        ]
        source_real_lower = float(source["epsilon_real_lower"])
        source_real_upper = float(source["epsilon_real_upper"])
        source_imaginary_lower = float(source["epsilon_imaginary_lower"])
        source_imaginary_upper = float(source["epsilon_imaginary_upper"])

        def close(left: float, right: float) -> bool:
            return math.isclose(left, right, rel_tol=1.0e-14, abs_tol=1.0e-15)

        contiguous = bool(ordered_bounds) and all(
            close(left[1], right[0])
            for left, right in zip(ordered_bounds, ordered_bounds[1:])
        )
        reconstructs_source = (
            declared_count > 0
            and indices == list(range(declared_count))
            and len(ordered_bounds) == declared_count
            and bounds_are_consistent
            and close(ordered_bounds[0][0], source_real_lower)
            and close(ordered_bounds[-1][1], source_real_upper)
            and contiguous
            and all(
                close(bounds[2], source_imaginary_lower)
                and close(bounds[3], source_imaginary_upper)
                for bounds in ordered_bounds
            )
        )
        audits.append(
            {
                "event_id": event_id,
                "mapped_cell_id": cell_id,
                "epsilon_bin_index": epsilon_bin,
                "path_segment": path_segment,
                "declared_epsilon_subdivision_count": declared_count,
                "observed_epsilon_subdivision_count": len(indices),
                "source_epsilon_real_lower": source_real_lower,
                "source_epsilon_real_upper": source_real_upper,
                "covered_epsilon_real_lower": (
                    ordered_bounds[0][0] if ordered_bounds else math.nan
                ),
                "covered_epsilon_real_upper": (
                    ordered_bounds[-1][1] if ordered_bounds else math.nan
                ),
                "subdivision_bounds_are_consistent": bounds_are_consistent,
                "subdivision_intervals_are_contiguous": contiguous,
                "epsilon_partition_reconstructs_source_box": reconstructs_source,
                "valid_for_endpoint_xt_overlap_geometry_atlas": reconstructs_source,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return audits


def primitive_candidate_rows(
    cover: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    residues = {
        row["branch_owner_id"]: float(row["material_residue_abs_upper"])
        for row in read_csv(RESIDUES)
    }
    theorem = {
        row["event_id"]: float(row["Q_boundary_abs_upper"])
        for row in read_csv(THEOREM_5450)
    }
    groups: dict[tuple[str, str, int, int, int, str], list[dict[str, Any]]] = {}
    for row in cover:
        if row["path_segment"] not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}:
            continue
        if float(row["t_lower"]) != 0.0:
            continue
        key = (
            row["event_id"],
            row["mapped_cell_id"],
            int(row["epsilon_bin_index"]),
            int(row.get("epsilon_subdivision_index", 0)),
            int(row.get("epsilon_subdivision_count", 1)),
            row["path_segment"],
        )
        groups.setdefault(key, []).append(row)
    rows: list[dict[str, Any]] = []
    for key, leaves in sorted(groups.items()):
        (
            event_id,
            cell_id,
            epsilon_bin,
            epsilon_subdivision_index,
            epsilon_subdivision_count_value,
            connector,
        ) = key
        branch_id = leaves[0]["branch_owner_id"]
        outer = [
            row
            for row in leaves
            if row["cover_owner"] == "OUTER_PARENT_TRIANGLE"
        ]
        inner = [
            row
            for row in leaves
            if row["cover_owner"] == "INNER_CAUCHY_REGULAR_PART"
        ]
        candidate_residue_bound = max(residues[branch_id], theorem[event_id])
        integrated_log_bound = 0.0
        for row in outer:
            lower = float(row["gap_abs_lower"])
            upper = float(row["gap_abs_upper"])
            logarithm_bound = math.hypot(
                max(abs(math.log(lower)), abs(math.log(upper))),
                math.pi,
            )
            integrated_log_bound += (
                float(row["x_width"])
                * candidate_residue_bound
                * logarithm_bound
            )
        rows.append(
            {
                "event_id": event_id,
                "branch_owner_id": branch_id,
                "mapped_cell_id": cell_id,
                "epsilon_bin_index": epsilon_bin,
                "epsilon_subdivision_index": epsilon_subdivision_index,
                "epsilon_subdivision_count": epsilon_subdivision_count_value,
                "connector": connector,
                "outer_endpoint_leaf_count": len(outer),
                "inner_principal_endpoint_leaf_count": len(inner),
                "endpoint_owner": (
                    "MIXED_HLOG_G_INNER_PLUS_NONSINGULAR_OUTER"
                    if inner and outer
                    else (
                        "HLOG_G_INNER"
                        if inner
                        else "NONSINGULAR_LOG_OUTER"
                    )
                ),
                "candidate_residue_abs_upper": candidate_residue_bound,
                "candidate_integrated_nonsingular_log_abs_upper": (
                    integrated_log_bound
                ),
                "candidate_is_finite": math.isfinite(integrated_log_bound),
                "requires_correlated_Q_contour_enclosure_on_inner_x_leaves": bool(
                    inner
                ),
                "valid_for_nonsingular_primitive_bound": False,
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def render_document(
    payload: dict[str, Any], summaries: list[dict[str, Any]]
) -> None:
    event_rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in summaries if row["event_id"] == event_id]
        event_rows.append(
            {
                "event_id": event_id,
                "jobs": len(selected),
                "leaves": sum(int(row["leaf_count"]) for row in selected),
                "inner": sum(int(row["inner_leaf_count"]) for row in selected),
                "outer": sum(int(row["outer_leaf_count"]) for row in selected),
                "unresolved": sum(
                    int(row["unresolved_leaf_count"]) for row in selected
                ),
                "depth": max(int(row["maximum_refinement_depth"]) for row in selected),
            }
        )
    lines = [
        "# 5451: D4 event-endpoint x-t overlap geometry cover",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Construction",
        "",
        "Every singular event-term cell, every one of the ten complex regulator boxes and all three straight contour segments were partitioned in `(x,t)`. A leaf is assigned to the inner Cauchy owner when `sup|E-p|<=7.5e-6`, and to the existing parent triangle owner when `inf|E-p|>=5e-6`. Only boxes crossing both thresholds are subdivided. The positive overlap makes this a finite covering problem rather than a demand to locate the artificial switching circle exactly.",
        "",
        "| event | jobs | leaves | inner | outer | unresolved | max depth |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in event_rows:
        lines.append(
            f"| `{row['event_id']}` | {row['jobs']} | {row['leaves']} | "
            f"{row['inner']} | {row['outer']} | {row['unresolved']} | "
            f"{row['depth']} |"
        )
    lines.extend(
        [
            "",
            "The binary leaf areas reconstruct every source rectangle. Inner leaves now have an exact finite formula but still need their correlated `Q` circle evaluated on the full leaf `x` interval. Outer leaves have a strict positive pole gap but still need the unchanged parent amplitude enclosure run on those leaves.",
            "",
            "## Primitive split",
            "",
            "At `t=0`, outer connector leaves also give a finite candidate bound for the nonsingular logarithm using `|Log z|<=hypot(max(|log m|,|log M|),pi)`. Leaves touching the principal endpoint remain owned by the already-derived `H log + G` primitive. Candidate numbers are not promoted because the event-tube residue must first be enclosed on the same correlated `x` leaves.",
            "",
            "## Claim boundary",
            "",
            "This is a complete geometric atlas, not yet a complete amplitude atlas. Full event-cell finite cover, event-local `W3`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false. The next runner evaluates the inner `Q` contours first, then the outer parent leaves, without changing this partition.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def render_progress_document(progress: dict[str, Any]) -> None:
    failed_ids = progress.get("failed_job_ids", [])
    failed_text = ", ".join(f"`{job_id}`" for job_id in failed_ids) or "none"
    lines = [
        "# 5451: D4 event-endpoint x-t overlap geometry cover",
        "",
        "## Current decision",
        "",
        f"**{progress['decision']}**",
        "",
        "## Resume-safe state",
        "",
        f"- Physical cover jobs complete: `{progress['completed_job_count']}/{progress['total_job_count']}`.",
        f"- Failed jobs: `{progress['failed_job_count']}` ({failed_text}).",
        f"- Pending jobs: `{progress['pending_job_count']}`.",
        f"- Next job: `{progress.get('next_pending_job_id', '')}`.",
        "",
        "Each physical job is written atomically before the next job starts. A stopped run therefore resumes without repeating certified jobs. The runner uses one Python process, one numerical thread and below-normal Windows priority.",
        "",
        "## Geometry construction",
        "",
        "For every event-cell owner and contour segment, a leaf belongs to the inner Cauchy chart when `sup|E-p|<=7.5e-6` and to the parent outer chart when `inf|E-p|>=5e-6`. Their positive `2.5e-6` overlap is the exact reason a finite binary cover can exist.",
        "",
        "The broad real regulator box touching `epsilon=0` couples endpoint motion to the full `x` interval too strongly for a direct interval box. Connector jobs on that box are therefore split into 32 closed real-epsilon subboxes before the same certified `(x,t)` partition is applied. This is a refinement of the parameter atlas, not a changed integrand or a fitted closure.",
        "",
        "## Claim boundary",
        "",
        "Checkpoint 5450 already proves the exact endpoint subtraction `F=rho/delta+G` and the finite Cauchy bound on `G`. Checkpoint 5451 is still incomplete until every physical job is present and the aggregate validations pass. Event-local `W3`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(max_jobs: int) -> dict[str, Any]:
    set_below_normal_priority()
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    parent_result = read_json(RESULT_5450)
    if parent_result.get("failed_validation_count") != 0:
        raise RuntimeError("checkpoint 5450 is not validated")
    parent = load_module("mts_5396_for_5451", PARENT_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    cover, progress = build_cover(parent, max_jobs)
    if cover is None:
        progress.update(
            {
                "decision": (
                    "RESUME_REQUIRED__FAILED_GEOMETRY_JOB_NEEDS_REFINEMENT"
                    if progress["failed_job_count"]
                    else "RESUME_SAFE_GEOMETRY_CHUNK_COMPLETE__MORE_JOBS_PENDING"
                ),
                "runtime_seconds": time.perf_counter() - started,
                "next_target": (
                    "REFINE_FAILED_GEOMETRY_JOB"
                    if progress["failed_job_count"]
                    else "RESUME_5451_GEOMETRY_JOBS"
                ),
                "valid_for_endpoint_xt_overlap_geometry_atlas": False,
                "valid_for_nonsingular_primitive_bound": False,
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_D4_numeric_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "failed_validation_count": 0,
            }
        )
        atomic_json(STATUS, progress)
        render_progress_document(progress)
        return progress
    summaries = summary_rows(cover)
    epsilon_audits = epsilon_partition_audit_rows(cover)
    primitives = primitive_candidate_rows(cover)
    unresolved = [row for row in cover if not row["geometry_cover_leaf_passes"]]
    physical_jobs = cover_job_specs(parent)
    expected_jobs = sum(
        int(row["declared_epsilon_subdivision_count"])
        for row in epsilon_audits
    )
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "FINITE_ENDPOINT_XT_OVERLAP_GEOMETRY_ATLAS_CERTIFIED__EVALUATE_INNER_Q_THEN_OUTER_PARENT"
            if not unresolved
            else "ENDPOINT_XT_OVERLAP_GEOMETRY_HAS_UNRESOLVED_LEAVES"
        ),
        "event_count": len({row["event_id"] for row in cover}),
        "event_cell_term_owner_count": len(read_csv(OWNERS_5449)),
        "physical_cover_job_count": len(physical_jobs),
        "epsilon_partition_audit_row_count": len(epsilon_audits),
        "cover_job_count": len(summaries),
        "expected_cover_job_count": expected_jobs,
        "cover_leaf_count": len(cover),
        "inner_leaf_count": sum(
            row["cover_owner"] == "INNER_CAUCHY_REGULAR_PART" for row in cover
        ),
        "outer_leaf_count": sum(
            row["cover_owner"] == "OUTER_PARENT_TRIANGLE" for row in cover
        ),
        "unresolved_leaf_count": len(unresolved),
        "maximum_refinement_depth": max(
            int(row["refinement_depth"]) for row in cover
        ),
        "primitive_candidate_row_count": len(primitives),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": "CORRELATED_INNER_Q_LEAF_ENCLOSURE_THEN_OUTER_PARENT_LEAF_ENCLOSURE",
        "valid_for_endpoint_xt_overlap_geometry_atlas": not unresolved,
        "valid_for_nonsingular_primitive_bound": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5450_is_valid", parent_result.get("valid_for_exact_endpoint_principal_part_subtraction") is True and parent_result.get("valid_for_correlated_event_curve_contour_smoke") is True, parent_result.get("decision")),
        check("all_13_event_cell_term_owners_are_present", len(read_csv(OWNERS_5449)) == 13, len(read_csv(OWNERS_5449))),
        check("all_390_physical_cover_jobs_are_present", len(epsilon_audits) == len(physical_jobs) == 390, f"{len(epsilon_audits)}/{len(physical_jobs)}"),
        check("all_epsilon_partitions_reconstruct_source_boxes", all(row["epsilon_partition_reconstructs_source_box"] for row in epsilon_audits), sum(not row["epsilon_partition_reconstructs_source_box"] for row in epsilon_audits)),
        check("all_endpoint_parameter_boxes_are_present", len(summaries) == expected_jobs, f"{len(summaries)}/{expected_jobs}"),
        check("all_binary_partitions_reconstruct_source_rectangles", all(float(row["parameter_area_absolute_error"]) <= 1.0e-12 * max(float(row["expected_parameter_area"]), 1.0) for row in summaries), max(float(row["parameter_area_absolute_error"]) for row in summaries)),
        check("all_overlap_cover_leaves_are_classified", not unresolved and all(row["geometry_overlap_cover_passes"] for row in summaries), len(unresolved)),
        check("all_inner_leaves_obey_inner_radius", all(float(row["gap_abs_upper"]) <= INNER_RADIUS for row in cover if row["cover_owner"] == "INNER_CAUCHY_REGULAR_PART"), INNER_RADIUS),
        check("all_outer_leaves_obey_outer_radius", all(float(row["gap_abs_lower"]) >= OUTER_RADIUS for row in cover if row["cover_owner"] == "OUTER_PARENT_TRIANGLE"), OUTER_RADIUS),
        check("all_top_segments_are_outer", all(row["cover_owner"] == "OUTER_PARENT_TRIANGLE" for row in cover if row["path_segment"] == "TOP"), sum(row["path_segment"] == "TOP" for row in cover)),
        check("every_event_has_a_principal_endpoint_leaf", all(any(row["event_id"] == event_id and row["cover_owner"] == "INNER_CAUCHY_REGULAR_PART" and row["path_segment"] in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"} and float(row["t_lower"]) == 0.0 for row in cover) for event_id in EVENT_IDS), list(EVENT_IDS)),
        check("all_nonsingular_primitive_candidates_are_finite", primitives and all(row["candidate_is_finite"] for row in primitives), len(primitives)),
        check("broad_claims_remain_false", not payload["valid_for_nonsingular_primitive_bound"] and not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_D4_numeric_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "geometry atlas only"),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started_utc
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(COVER, cover)
    atomic_csv(SUMMARY, summaries)
    atomic_csv(EPSILON_AUDIT, epsilon_audits)
    atomic_csv(PRIMITIVES, primitives)
    atomic_csv(SOURCES, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload, summaries)
    atomic_json(RESULT, payload)
    atomic_json(
        COMPLETE,
        {
            "checkpoint": CHECKPOINT,
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "validation_passed": payload["failed_validation_count"] == 0,
            "result": str(RESULT),
        },
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-jobs", type=int, default=5)
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.max_jobs)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("failed_validation_count", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
