from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5304"

SCRIPT_5303 = SCRIPTS / (
    "Y5_R2FR_5303_mask_edge_regulator_ladder_and_zero_limit.py"
)
RESULT_5303 = FUNCTIONAL_RG / "5303" / (
    "mask_edge_regulator_zero_limit_result.json"
)
VALIDATION_5303 = FUNCTIONAL_RG / "5303" / (
    "mask_edge_regulator_zero_limit_validation.csv"
)

DRY_RUN = SOURCE / "moving_mask_edge_energy_map_dry_run.json"
ENDPOINTS = SOURCE / "moving_mask_edge_energy_endpoints.csv"
BRANCH_SCAN = SOURCE / "moving_mask_edge_branch_scan.csv"
ENERGY_MAP = SOURCE / "moving_mask_edge_energy_map.csv"
TOPOLOGY = SOURCE / "moving_mask_edge_topology_intervals.csv"
RESULT = SOURCE / "moving_mask_edge_energy_map_result.json"
VALIDATION = SOURCE / "moving_mask_edge_energy_map_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5304_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5304-Y5-R2FR-moving-mask-edge-energy-map.md"

CHECKPOINT = 5304
PARENT_CHECKPOINT = 5303
MARKER = "MTS_5304_MOVING_MASK_EDGE_ENERGY_MAP"
REVISION = "moving-mask-edge-energy-map-v1"
BRANCH_SCAN_COUNT = 513
MAP_ENERGY_COUNT = 33
BOUNDARY_RESIDUAL_LIMIT = 1.0e-12
WITNESS_REPRODUCTION_LIMIT = 1.0e-12
TRANSVERSE_DERIVATIVE_MINIMUM = 1.0e-8
FOLD_DERIVATIVE_RESIDUAL_LIMIT = 1.0e-11
FOLD_SECOND_DERIVATIVE_MINIMUM = 1.0e-3
FOLD_SECOND_DERIVATIVE_CHANGE_LIMIT = 1.0e-4
CLAIM_FIELDS = (
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5303 = load_module("mts_5303_for_5304", SCRIPT_5303)
M5302 = M5303.M5302
M5272 = M5302.M5272
M5280 = M5303.M5280
M5283 = M5303.M5283
M5292 = M5303.M5301.M5300.M5292
np = M5303.np
mp = M5303.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def angular_limit() -> float:
    return float(M5280.M5274.M5270.ANGULAR_LIMIT)


def energy_limits() -> tuple[float, float]:
    return (
        float(M5292.M5267.ENERGY_MINIMUM),
        float(M5292.M5267.ENERGY_MAXIMUM),
    )


def physical_q_roots(absolute_soft_cosine: float) -> list[float]:
    coefficients = M5272.hard_boundary_coefficients(
        -absolute_soft_cosine,
        -M5302.EDGE_DECAY_ABSOLUTE,
        1,
        -0.3,
        math.pi,
    )
    minimum, maximum = energy_limits()
    return [
        float(root)
        for root in M5272.quadratic_real_roots(*coefficients)
        if 0.0 <= root <= 1.0
        and minimum <= 1.0 - root**2 <= maximum
    ]


def energy_from_coordinate(absolute_soft_cosine: float) -> float:
    roots = physical_q_roots(absolute_soft_cosine)
    if len(roots) != 1:
        raise RuntimeError(
            "moving edge is not single-valued at "
            f"s={absolute_soft_cosine}: roots={roots}"
        )
    return 1.0 - roots[0] ** 2


def surface_value(energy: float, absolute_soft_cosine: float) -> float:
    return float(
        M5272.hard_boundary_value(
            math.sqrt(1.0 - energy),
            -absolute_soft_cosine,
            -M5302.EDGE_DECAY_ABSOLUTE,
            1,
            -0.3,
            math.pi,
        )
    )


def differential_row(
    energy: float,
    absolute_soft_cosine: float,
) -> dict[str, float]:
    q_value = math.sqrt(1.0 - energy)
    coefficient_q2, coefficient_q1, _ = (
        M5272.hard_boundary_coefficients(
            -absolute_soft_cosine,
            -M5302.EDGE_DECAY_ABSOLUTE,
            1,
            -0.3,
            math.pi,
        )
    )
    derivative_s = -float(
        M5272.hard_boundary_coordinate_derivative(
            "soft_cosine",
            q_value,
            -absolute_soft_cosine,
            -M5302.EDGE_DECAY_ABSOLUTE,
            1,
            -0.3,
            math.pi,
        )
    )
    derivative_q = 2.0 * coefficient_q2 * q_value + coefficient_q1
    derivative_energy_coordinate = (
        2.0 * q_value * derivative_s / derivative_q
    )
    return {
        "surface_derivative_with_respect_to_absolute_soft_cosine": (
            derivative_s
        ),
        "surface_derivative_with_respect_to_q": derivative_q,
        "energy_derivative_with_respect_to_absolute_soft_cosine": (
            derivative_energy_coordinate
        ),
        "absolute_soft_cosine_derivative_with_respect_to_energy": (
            1.0 / derivative_energy_coordinate
            if derivative_energy_coordinate != 0.0
            else math.inf
        ),
    }


def fold_coordinate() -> float:
    limit = angular_limit()
    previous_coordinate = 0.0
    previous_energy = energy_from_coordinate(previous_coordinate)
    previous_derivative = differential_row(
        previous_energy, previous_coordinate
    )["energy_derivative_with_respect_to_absolute_soft_cosine"]
    brackets: list[tuple[float, float]] = []
    for index in range(1, BRANCH_SCAN_COUNT):
        coordinate = limit * index / (BRANCH_SCAN_COUNT - 1)
        energy = energy_from_coordinate(coordinate)
        derivative = differential_row(energy, coordinate)[
            "energy_derivative_with_respect_to_absolute_soft_cosine"
        ]
        if previous_derivative * derivative < 0.0:
            brackets.append((previous_coordinate, coordinate))
        previous_coordinate = coordinate
        previous_derivative = derivative
    if len(brackets) != 1:
        raise RuntimeError(f"expected one fold bracket, found {brackets}")
    lower, upper = brackets[0]
    lower_derivative = differential_row(
        energy_from_coordinate(lower), lower
    )["energy_derivative_with_respect_to_absolute_soft_cosine"]
    for _ in range(100):
        midpoint = 0.5 * (lower + upper)
        midpoint_derivative = differential_row(
            energy_from_coordinate(midpoint), midpoint
        )["energy_derivative_with_respect_to_absolute_soft_cosine"]
        if lower_derivative * midpoint_derivative <= 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_derivative = midpoint_derivative
    return 0.5 * (lower + upper)


def fold_second_derivative_rows(
    coordinate: float,
) -> list[dict[str, Any]]:
    center = energy_from_coordinate(coordinate)
    rows: list[dict[str, Any]] = []
    previous: float | None = None
    for step in (1.0e-4, 5.0e-5, 2.5e-5):
        second = (
            energy_from_coordinate(coordinate + step)
            - 2.0 * center
            + energy_from_coordinate(coordinate - step)
        ) / step**2
        change = (
            abs(second - previous) / max(abs(second), abs(previous), 1.0e-300)
            if previous is not None
            else ""
        )
        rows.append(
            {
                "finite_difference_step": step,
                "fold_energy_second_derivative": second,
                "successive_relative_change": change,
            }
        )
        previous = second
    return rows


def inverse_coordinate_on_branch(
    energy: float,
    branch_id: str,
    fold: float,
) -> float:
    tolerance = 2.0e-14
    if branch_id == "INNER":
        lower, upper = 0.0, fold
    elif branch_id == "OUTER":
        lower, upper = fold, angular_limit()
    else:
        raise ValueError(f"unknown branch {branch_id}")
    lower_value = energy_from_coordinate(lower) - energy
    upper_value = energy_from_coordinate(upper) - energy
    if abs(lower_value) <= tolerance:
        return lower
    if abs(upper_value) <= tolerance:
        return upper
    if lower_value * upper_value > 0.0:
        raise ValueError(
            f"energy {energy} not bracketed on {branch_id}: "
            f"{lower_value}, {upper_value}"
        )
    for _ in range(100):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = energy_from_coordinate(midpoint) - energy
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_value = midpoint_value
    return 0.5 * (lower + upper)


def event_rows() -> list[dict[str, Any]]:
    fold = fold_coordinate()
    specifications = (
        ("NONDEGENERATE_FOLD", fold, "FOLD_JOIN"),
        ("ANGULAR_CUTOFF_CROSSING", angular_limit(), "OUTER"),
        ("ZERO_COORDINATE_CROSSING", 0.0, "INNER"),
    )
    second_rows = fold_second_derivative_rows(fold)
    fold_second = float(second_rows[-1]["fold_energy_second_derivative"])
    fold_change = float(second_rows[-1]["successive_relative_change"])
    rows: list[dict[str, Any]] = []
    for event_id, coordinate, branch_id in specifications:
        roots = physical_q_roots(coordinate)
        energy = 1.0 - roots[0] ** 2
        differential = differential_row(energy, coordinate)
        is_fold = event_id == "NONDEGENERATE_FOLD"
        derivative_residual = abs(
            differential[
                "energy_derivative_with_respect_to_absolute_soft_cosine"
            ]
        )
        rows.append(
            {
                "event_id": event_id,
                "branch_id": branch_id,
                "soft_energy": energy,
                "q_value": roots[0],
                "absolute_soft_cosine_boundary": coordinate,
                "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
                "physical_q_root_count": len(roots),
                "surface_residual": abs(surface_value(energy, coordinate)),
                **differential,
                "fold_energy_second_derivative": fold_second if is_fold else "",
                "fold_second_derivative_relative_change": (
                    fold_change if is_fold else ""
                ),
                "valid_for_exact_moving_edge_event": (
                    len(roots) == 1
                    and abs(surface_value(energy, coordinate))
                    <= BOUNDARY_RESIDUAL_LIMIT
                    and (
                        not is_fold
                        or (
                            derivative_residual
                            <= FOLD_DERIVATIVE_RESIDUAL_LIMIT
                            and fold_second
                            >= FOLD_SECOND_DERIVATIVE_MINIMUM
                            and fold_change
                            <= FOLD_SECOND_DERIVATIVE_CHANGE_LIMIT
                        )
                    )
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def branch_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    limit = angular_limit()
    fold = fold_coordinate()
    for index in range(BRANCH_SCAN_COUNT):
        coordinate = limit * index / (BRANCH_SCAN_COUNT - 1)
        roots = physical_q_roots(coordinate)
        energy = 1.0 - roots[0] ** 2 if len(roots) == 1 else math.nan
        differential = (
            differential_row(energy, coordinate)
            if math.isfinite(energy)
            else {}
        )
        branch_id = "INNER" if coordinate < fold else "OUTER"
        rows.append(
            {
                "scan_index": index,
                "branch_id": branch_id,
                "absolute_soft_cosine_boundary": coordinate,
                "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
                "physical_q_root_count": len(roots),
                "q_value": roots[0] if len(roots) == 1 else "",
                "soft_energy": energy if math.isfinite(energy) else "",
                "surface_residual": (
                    abs(surface_value(energy, coordinate))
                    if math.isfinite(energy)
                    else ""
                ),
                **differential,
                "valid_for_single_valued_q_of_coordinate_branch": (
                    len(roots) == 1
                    and abs(surface_value(energy, coordinate))
                    <= BOUNDARY_RESIDUAL_LIMIT
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def energy_nodes(
    fold_energy: float,
    upper_energy: float,
    cutoff_energy: float,
) -> list[tuple[str, float]]:
    midpoint = 0.5 * (fold_energy + upper_energy)
    half_width = 0.5 * (upper_energy - fold_energy)
    values: list[tuple[str, float]] = []
    for index in range(MAP_ENERGY_COUNT):
        phase = math.pi * index / (MAP_ENERGY_COUNT - 1)
        energy = midpoint - half_width * math.cos(phase)
        values.append((f"CHEBYSHEV_{index:02d}", energy))
    values.extend(
        (
            ("ANGULAR_CUTOFF_EVENT", cutoff_energy),
            ("5302_WITNESS", float(M5302.EDGE_ENERGY)),
        )
    )
    unique: list[tuple[str, float]] = []
    for node_id, energy in sorted(values, key=lambda item: item[1]):
        if not unique or abs(energy - unique[-1][1]) > 2.0e-14:
            unique.append((node_id, energy))
        elif node_id in {"ANGULAR_CUTOFF_EVENT", "5302_WITNESS"}:
            unique[-1] = (node_id, energy)
    return unique


def energy_map_rows(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    event_lookup = {row["event_id"]: row for row in events}
    fold = float(event_lookup["NONDEGENERATE_FOLD"]["absolute_soft_cosine_boundary"])
    fold_energy = float(event_lookup["NONDEGENERATE_FOLD"]["soft_energy"])
    cutoff_energy = float(event_lookup["ANGULAR_CUTOFF_CROSSING"]["soft_energy"])
    upper_energy = float(event_lookup["ZERO_COORDINATE_CROSSING"]["soft_energy"])
    rows: list[dict[str, Any]] = []
    node_index = 0
    for energy_node_id, energy in energy_nodes(
        fold_energy, upper_energy, cutoff_energy
    ):
        branches = ["INNER"]
        if energy <= cutoff_energy + 2.0e-14:
            branches.append("OUTER")
        if abs(energy - fold_energy) <= 2.0e-14:
            branches = ["FOLD_JOIN"]
        for branch_id in branches:
            solve_branch = "INNER" if branch_id == "FOLD_JOIN" else branch_id
            coordinate = inverse_coordinate_on_branch(
                energy, solve_branch, fold
            )
            roots = physical_q_roots(coordinate)
            residual = abs(surface_value(energy, coordinate))
            differential = differential_row(energy, coordinate)
            is_fold = branch_id == "FOLD_JOIN"
            rows.append(
                {
                    "map_index": node_index,
                    "energy_node_id": energy_node_id,
                    "branch_id": branch_id,
                    "soft_energy": energy,
                    "q_value": math.sqrt(1.0 - energy),
                    "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
                    "absolute_soft_cosine_boundary": coordinate,
                    "physical_q_root_count_at_coordinate": len(roots),
                    "expected_inverse_coordinate_count_at_energy": (
                        1 if is_fold or energy > cutoff_energy else 2
                    ),
                    "surface_residual": residual,
                    **differential,
                    "valid_for_inverse_moving_edge_map": (
                        len(roots) == 1
                        and residual <= BOUNDARY_RESIDUAL_LIMIT
                        and (
                            is_fold
                            or abs(
                                differential[
                                    "surface_derivative_with_respect_to_absolute_soft_cosine"
                                ]
                            )
                            >= TRANSVERSE_DERIVATIVE_MINIMUM
                        )
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            node_index += 1
    return rows


def topology_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lookup = {row["event_id"]: row for row in events}
    fold = float(lookup["NONDEGENERATE_FOLD"]["soft_energy"])
    cutoff = float(lookup["ANGULAR_CUTOFF_CROSSING"]["soft_energy"])
    upper = float(lookup["ZERO_COORDINATE_CROSSING"]["soft_energy"])
    minimum, maximum = energy_limits()
    specifications = (
        ("BELOW_FOLD", minimum, fold, 0, "no in-domain edge"),
        ("FOLD", fold, fold, 1, "double root joins INNER and OUTER"),
        ("TWO_BRANCH", fold, cutoff, 2, "INNER and OUTER roots"),
        ("INNER_ONLY", cutoff, upper, 1, "INNER root"),
        ("ABOVE_ZERO_CROSSING", upper, maximum, 0, "no in-domain edge"),
    )
    return [
        {
            "topology_region": region,
            "lower_soft_energy": lower,
            "upper_soft_energy": high,
            "in_domain_edge_coordinate_count": count,
            "branch_content": content,
            "valid_for_moving_edge_topology_partition": True,
            **{field: False for field in CLAIM_FIELDS},
        }
        for region, lower, high, count, content in specifications
    ]


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5303,
        RESULT_5303,
        VALIDATION_5303,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5303)
    events = event_rows()
    event_lookup = {row["event_id"]: row for row in events}
    fold_energy = float(event_lookup["NONDEGENERATE_FOLD"]["soft_energy"])
    cutoff_energy = float(
        event_lookup["ANGULAR_CUTOFF_CROSSING"]["soft_energy"]
    )
    upper_energy = float(
        event_lookup["ZERO_COORDINATE_CROSSING"]["soft_energy"]
    )
    minimum, maximum = energy_limits()
    checks = {
        "parent_5303_accepted": bool(parent["acceptance_passed"]),
        "parent_5303_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5303)
        ),
        "parent_requests_boundary_aligned_cubature": (
            parent["decision"]
            == (
                "REGULATOR_ZERO_EDGE_SLICE_RESOLVED__"
                "BUILD_BOUNDARY_ALIGNED_ENERGY_ANGLE_CUBATURE"
            )
        ),
        "three_exact_topology_events_resolved": (
            len(events) == 3
            and all(
                bool(row["valid_for_exact_moving_edge_event"])
                for row in events
            )
        ),
        "fold_cutoff_zero_events_strictly_ordered": (
            minimum < fold_energy < cutoff_energy < upper_energy < maximum
        ),
        "witness_inside_moving_edge_interval": (
            cutoff_energy < M5302.EDGE_ENERGY < upper_energy
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "moving_edge_fold_energy": fold_energy,
        "moving_edge_angular_cutoff_energy": cutoff_energy,
        "moving_edge_upper_energy": upper_energy,
        "decision": (
            "DRY_RUN_ACCEPTED__MAP_MOVING_MASK_EDGE"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5304 dry run did not pass")
    parent = read_json(RESULT_5303)
    events = event_rows()
    event_lookup = {row["event_id"]: row for row in events}
    fold_event = event_lookup["NONDEGENERATE_FOLD"]
    cutoff_event = event_lookup["ANGULAR_CUTOFF_CROSSING"]
    upper_event = event_lookup["ZERO_COORDINATE_CROSSING"]
    fold_energy = float(fold_event["soft_energy"])
    cutoff_energy = float(cutoff_event["soft_energy"])
    upper_energy = float(upper_event["soft_energy"])
    branch = branch_scan_rows()
    energy_map = energy_map_rows(events)
    topology = topology_rows(events)
    write_csv(ENDPOINTS, events)
    write_csv(BRANCH_SCAN, branch)
    write_csv(ENERGY_MAP, energy_map)
    write_csv(TOPOLOGY, topology)
    maximum_residual = max(
        float(row["surface_residual"])
        for rows in (events, branch, energy_map)
        for row in rows
    )
    inner_derivatives = [
        float(row["energy_derivative_with_respect_to_absolute_soft_cosine"])
        for row in branch
        if row["branch_id"] == "INNER"
    ]
    outer_derivatives = [
        float(row["energy_derivative_with_respect_to_absolute_soft_cosine"])
        for row in branch
        if row["branch_id"] == "OUTER"
    ]
    minimum_nonfold_transverse_derivative = min(
        abs(
            float(
                row[
                    "surface_derivative_with_respect_to_absolute_soft_cosine"
                ]
            )
        )
        for row in energy_map
        if row["branch_id"] != "FOLD_JOIN"
    )
    witness_rows = [
        row for row in energy_map if row["energy_node_id"] == "5302_WITNESS"
    ]
    witness = next(row for row in witness_rows if row["branch_id"] == "INNER")
    witness_change = abs(
        float(witness["absolute_soft_cosine_boundary"])
        - float(M5302.boundary_coordinate())
    )
    energy_counts: dict[float, int] = {}
    for row in energy_map:
        energy = float(row["soft_energy"])
        energy_counts[energy] = energy_counts.get(energy, 0) + 1
    root_counts_match = all(
        count
        == int(
            next(
                row["expected_inverse_coordinate_count_at_energy"]
                for row in energy_map
                if float(row["soft_energy"]) == energy
            )
        )
        for energy, count in energy_counts.items()
    )
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "moving_edge_topology_events_exact": all(
            bool(row["valid_for_exact_moving_edge_event"])
            for row in events
        ),
        "q_of_coordinate_branch_single_valued": all(
            bool(row["valid_for_single_valued_q_of_coordinate_branch"])
            for row in branch
        ),
        "inner_branch_strictly_decreasing": (
            max(inner_derivatives) < 0.0
        ),
        "outer_branch_strictly_increasing": (
            min(outer_derivatives) > 0.0
        ),
        "fold_is_nondegenerate": (
            abs(
                float(
                    fold_event[
                        "energy_derivative_with_respect_to_absolute_soft_cosine"
                    ]
                )
            )
            <= FOLD_DERIVATIVE_RESIDUAL_LIMIT
            and float(fold_event["fold_energy_second_derivative"])
            >= FOLD_SECOND_DERIVATIVE_MINIMUM
            and float(
                fold_event["fold_second_derivative_relative_change"]
            )
            <= FOLD_SECOND_DERIVATIVE_CHANGE_LIMIT
        ),
        "inverse_map_nonfold_rows_transverse": (
            minimum_nonfold_transverse_derivative
            >= TRANSVERSE_DERIVATIVE_MINIMUM
        ),
        "inverse_energy_map_exact": all(
            bool(row["valid_for_inverse_moving_edge_map"])
            for row in energy_map
        ),
        "inverse_energy_root_counts_match_topology": root_counts_match,
        "five_region_topology_partition_recorded": len(topology) == 5,
        "witness_edge_reproduced": (
            witness_change <= WITNESS_REPRODUCTION_LIMIT
        ),
        "all_boundary_residuals_tight": (
            maximum_residual <= BOUNDARY_RESIDUAL_LIMIT
        ),
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "MOVING_EDGE_FOLD_AND_TWO_BRANCH_TOPOLOGY_DERIVED__"
        "SELECT_TOPOLOGY_SAFE_REGULATOR_LADDERS"
        if accepted
        else "MOVING_EDGE_MAP_REQUIRES_REPAIR"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "moving-mask-edge-energy-map",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
        "angular_limit": angular_limit(),
        "moving_edge_fold_energy": fold_energy,
        "moving_edge_fold_absolute_soft_cosine": float(
            fold_event["absolute_soft_cosine_boundary"]
        ),
        "moving_edge_fold_energy_second_derivative": float(
            fold_event["fold_energy_second_derivative"]
        ),
        "moving_edge_angular_cutoff_energy": cutoff_energy,
        "moving_edge_upper_energy": upper_energy,
        "moving_edge_energy_width": upper_energy - fold_energy,
        "two_branch_energy_width": cutoff_energy - fold_energy,
        "branch_scan_count": len(branch),
        "inverse_energy_map_count": len(energy_map),
        "inverse_energy_node_count": len(energy_counts),
        "maximum_boundary_surface_residual": maximum_residual,
        "maximum_inner_energy_derivative": max(inner_derivatives),
        "minimum_outer_energy_derivative": min(outer_derivatives),
        "minimum_nonfold_absolute_transverse_surface_derivative": (
            minimum_nonfold_transverse_derivative
        ),
        "witness_absolute_soft_cosine": float(
            witness["absolute_soft_cosine_boundary"]
        ),
        "witness_reproduction_absolute_change": witness_change,
        "integration_mp_decimal_digits": mp.mp.dps,
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "claim_boundary": {
            "valid_for_exact_moving_edge_energy_map": accepted,
            "valid_for_selected_energy_regulator_ladders": False,
            "valid_for_boundary_aligned_energy_angle_cubature": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The direct:g1 minus-root mask edge is now partitioned "
                "into a nondegenerate fold, an INNER branch, and a short "
                "OUTER branch at one fixed decay angle. Its regulated "
                "residue has not yet been integrated along those branches "
                "or over the decay coordinate."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": decision,
            "moving_edge_fold_energy": fold_energy,
            "moving_edge_angular_cutoff_energy": cutoff_energy,
            "moving_edge_upper_energy": upper_energy,
        },
    )
    return result


def validation_gate(
    gate: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5304 — Moving mask-edge fold topology and energy map

## Exact topology

At fixed `|d|={result['absolute_decay_cosine']:.12g}`, the 5272 surface

`F_{{+1,-0.3}}(sqrt(1-E),-|s|,-|d|)=0`

has exactly one physical `q=sqrt(1-E)` root for each
`0 <= |s| <= {result['angular_limit']:.12g}`. Implicit differentiation gives

`dE/d|s| = 2 q (partial F/partial |s|)/(partial F/partial q)`.

The derivative vanishes once. This is a nondegenerate minimum of `E(|s|)`,
so the inverse map has two coordinates between the fold and angular-cutoff
energies: an `INNER` branch and a short `OUTER` branch. Above the cutoff
event only the `INNER` branch remains. This fold was hidden by the earlier
tensor grid and invalidates the preliminary global-monotonicity assumption.

## Result

- fold: `E={result['moving_edge_fold_energy']:.15g}` at `|s|={result['moving_edge_fold_absolute_soft_cosine']:.15g}`;
- fold second derivative: `{result['moving_edge_fold_energy_second_derivative']:.15g}`;
- angular-cutoff crossing: `E={result['moving_edge_angular_cutoff_energy']:.15g}`;
- zero-coordinate crossing: `E={result['moving_edge_upper_energy']:.15g}`;
- energy width: `{result['moving_edge_energy_width']:.15g}`;
- two-branch width: `{result['two_branch_energy_width']:.15g}`;
- branch samples: `{result['branch_scan_count']}`;
- inverse energy nodes: `{result['inverse_energy_node_count']}`;
- inverse energy-map rows: `{result['inverse_energy_map_count']}`;
- maximum equation residual: `{result['maximum_boundary_surface_residual']:.12g}`;
- smallest nonfold transverse derivative magnitude: `{result['minimum_nonfold_absolute_transverse_surface_derivative']:.12g}`;
- witness coordinate: `{result['witness_absolute_soft_cosine']:.15g}`;
- witness reproduction change: `{result['witness_reproduction_absolute_change']:.12g}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This derives the fold and both branches of one exact hard-mask surface at one
fixed decay angle. It does not yet integrate the five-regulator residue along
those branches, integrate over the decay angle, establish the full
phase-space coefficient, or imply local GR or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    events = read_csv(ENDPOINTS)
    branch = read_csv(BRANCH_SCAN)
    energy_map = read_csv(ENERGY_MAP)
    topology = read_csv(TOPOLOGY)
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "three_exact_topology_events",
            len(events) == 3
            and all(
                parse_bool(row["valid_for_exact_moving_edge_event"])
                for row in events
            ),
            f"rows={len(events)}",
        ),
        validation_gate(
            "branch_scan_complete_and_single_valued",
            len(branch) == BRANCH_SCAN_COUNT
            and all(
                parse_bool(
                    row["valid_for_single_valued_q_of_coordinate_branch"]
                )
                for row in branch
            ),
            f"rows={len(branch)}",
        ),
        validation_gate(
            "inverse_map_complete_and_exact",
            len(energy_map) == int(result["inverse_energy_map_count"])
            and len(
                {float(row["soft_energy"]) for row in energy_map}
            )
            == int(result["inverse_energy_node_count"])
            and all(
                parse_bool(row["valid_for_inverse_moving_edge_map"])
                for row in energy_map
            ),
            f"rows={len(energy_map)}",
        ),
        validation_gate(
            "five_region_topology_partition",
            len(topology) == 5
            and all(
                parse_bool(
                    row["valid_for_moving_edge_topology_partition"]
                )
                for row in topology
            ),
            f"rows={len(topology)}",
        ),
        validation_gate(
            "witness_reproduced",
            float(result["witness_reproduction_absolute_change"])
            <= WITNESS_REPRODUCTION_LIMIT,
            str(result["witness_reproduction_absolute_change"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == str(result["formalization_workbench_end_digest"]),
            str(result["formalization_workbench_end_digest"]),
        ),
        validation_gate(
            "full_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no phase-space, UV, local-GR, or full-MTS claim",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_MOVING_MASK_EDGE_ENERGY_MAP"
            if passed
            else "MOVING_MASK_EDGE_ENERGY_MAP_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        required=True,
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
