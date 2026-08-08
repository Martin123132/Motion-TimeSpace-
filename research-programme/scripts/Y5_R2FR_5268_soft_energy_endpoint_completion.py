from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5267 = FUNCTIONAL_RG / "5267"
SOURCE = FUNCTIONAL_RG / "5268"
WORKERS = SOURCE / "workers"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5267 = (
    SCRIPTS
    / "Y5_R2FR_5267_topology_aware_soft_energy_component_runner.py"
)
RESULT_5267 = SOURCE_5267 / "energy_first_two_regulator_result.json"
VALIDATION_5267 = SOURCE_5267 / "energy_first_validation.csv"
THEOREM_5010 = (
    POST
    / "5010-Y5-R2FR-coupled-three-particle-cut-normalization-and-soft-plus-integrand.md"
)
THEOREM_5019 = (
    POST
    / "5019-Y5-R2FR-hhh-exact-soft-endpoint-and-crossed-pole-theorem.md"
)
THEOREM_5029 = (
    POST
    / "5029-Y5-R2FR-finite-x-pole-transport-and-collision-map.md"
)

RESULT = SOURCE / "soft_energy_endpoint_completion_result.json"
COMBINED_ROWS = SOURCE / "soft_energy_endpoint_completion_convergence.csv"
PHYSICAL_SAMPLES = SOURCE / "soft_energy_endpoint_physical_samples.csv"
STATUS = SOURCE / "status.json"
CHILD_LOG = SOURCE / "E020_worker.log"
VALIDATION = SOURCE / "soft_energy_endpoint_completion_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5268_VALIDATION.csv"
)
DOCUMENT = POST / "5268-Y5-R2FR-soft-energy-endpoint-completion.md"

CHECKPOINT = 5268
PARENT_CHECKPOINT = 5267
MARKER = "MTS_5268_SOFT_ENERGY_ENDPOINT_COMPLETION"
REVISION = "soft-energy-endpoint-completion-v1"
EPSILON_IDS = ("E040", "E020")
TAIL_CUT = 1.0e-4
TOPOLOGY_WITNESS = TAIL_CUT
SURFACE_SCAN_MINIMUM = 1.0e-6
NUMERICAL_FLOORS = (1.0e-7, 3.0e-7, 1.0e-6)
QUADRATURE_ORDERS = (32, 128, 512)
SAMPLE_COORDINATES = tuple(
    sorted(
        {
            *np.geomspace(1.0e-7, TAIL_CUT, 49).tolist(),
            *NUMERICAL_FLOORS,
            *[
                factor * floor
                for floor in NUMERICAL_FLOORS
                for factor in (
                    1.0,
                    1.25,
                    1.5,
                    2.0,
                    2.5,
                    3.0,
                    4.0,
                    5.0,
                    7.5,
                    10.0,
                )
                if factor * floor <= TAIL_CUT
            ],
        }
    )
)
SURFACE_SCAN_COORDINATES = tuple(
    np.geomspace(SURFACE_SCAN_MINIMUM, TAIL_CUT, 49).tolist()
)
POLYNOMIAL_DEGREES = (2, 3, 4)
CENTRAL_POLYNOMIAL_DEGREE = 3
LOW_ORDER_ERROR_LIMIT = 5.0e-3
MID_ORDER_ERROR_LIMIT = 1.0e-3
FLOOR_STABILITY_RELATIVE_LIMIT = 5.0e-4
UNRESOLVED_CAP_RELATIVE_LIMIT = 5.0e-4
ENDPOINT_ENVELOPE_SAFETY_FACTOR = 10.0
BOUNDARY_STATE_CACHES: dict[str, dict[str, Any]] = {}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5267 = load_module("mts_5267_for_5268", SCRIPT_5267)
M5267.SOURCE = SOURCE


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, complex):
        return {"real": value.real, "imaginary": value.imag}
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot serialize {type(value)!r}")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            default=json_default,
        ),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            default=json_default,
        ).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5267,
        RESULT_5267,
        VALIDATION_5267,
        THEOREM_5010,
        THEOREM_5019,
        THEOREM_5029,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def worker_paths(epsilon_id: str) -> dict[str, Path]:
    root = WORKERS / epsilon_id
    return {
        "root": root,
        "result": root / "endpoint_worker_result.json",
        "status": root / "status.json",
        "topology": root / "endpoint_topology_witnesses.csv",
        "surfaces": root / "endpoint_surface_scan.csv",
        "samples": root / "endpoint_integrand_samples.csv",
        "components": root / "endpoint_component_samples.csv",
        "quadrature": root / "endpoint_tail_quadrature.csv",
        "winding_attempts": root / "winding_resolution_attempts.csv",
    }


def interval_contract(
    epsilon_id: str,
) -> tuple[
    dict[tuple[str, str], dict[str, str]],
    list[dict[str, str]],
]:
    path = (
        SOURCE_5267
        / "workers"
        / epsilon_id
        / "dynamic_winding_intervals.csv"
    )
    rows = read_csv(path)
    contract: dict[tuple[str, str], dict[str, str]] = {}
    for component_id in sorted({row["component_id"] for row in rows}):
        component_rows = sorted(
            (
                row
                for row in rows
                if row["component_id"] == component_id
            ),
            key=lambda row: float(row["interval_lower"]),
        )
        contract[(component_id, "low")] = component_rows[0]
        contract[(component_id, "high")] = component_rows[-1]
    return contract, rows


def side_coordinate(side: str, distance: float) -> float:
    if side == "low":
        return float(distance)
    if side == "high":
        return float(1.0 - distance)
    raise ValueError(f"unknown endpoint side: {side}")


def fixed_multiplier(
    contract: dict[tuple[str, str], dict[str, str]],
    component_id: str,
    side: str,
) -> float:
    return float(contract[(component_id, side)]["dynamic_multiplier"])


def source_locked_5267_boundary_state(
    problem: dict[str, Any], coordinate: float
) -> dict[str, Any]:
    epsilon_id = str(problem["job"]["epsilon_id"])
    if epsilon_id not in BOUNDARY_STATE_CACHES:
        path = (
            SOURCE_5267
            / f"energy_winding_state_cache_{epsilon_id}.json"
        )
        payload = read_json(path)
        if payload.get("revision") != M5267.REVISION:
            raise RuntimeError(
                f"5267 winding cache revision mismatch for {epsilon_id}"
            )
        BOUNDARY_STATE_CACHES[epsilon_id] = payload
    cache = BOUNDARY_STATE_CACHES[epsilon_id]
    key = M5267.winding_state_cache_key(problem, float(coordinate))
    if key not in cache["states"]:
        raise RuntimeError(
            "5267 boundary state is absent for "
            f"{problem['job']['job_id']} at {coordinate:.17g}"
        )
    return dict(cache["states"][key])


def endpoint_component_value(
    problem: dict[str, Any],
    multiplier: float,
    coordinate: float,
) -> complex:
    if multiplier == 0.0:
        return 0.0j
    return multiplier * M5267.M5237.component_contribution(
        problem, float(coordinate)
    )


def gauss_integral(
    function: Callable[[float], complex],
    lower: float,
    upper: float,
    order: int,
) -> complex:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    half_width = 0.5 * (upper - lower)
    midpoint = 0.5 * (upper + lower)
    coordinates = midpoint + half_width * nodes
    values = np.asarray(
        [function(float(coordinate)) for coordinate in coordinates],
        dtype=np.complex128,
    )
    return complex(np.sum(half_width * weights * values))


def topology_rows_for_problem(
    problem: dict[str, Any],
    contract: dict[tuple[str, str], dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    topology_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    for side in ("low", "high"):
        expected = contract[(problem["component_id"], side)]
        expected_multiplier = float(expected["dynamic_multiplier"])
        witness_distance = TOPOLOGY_WITNESS
        coordinate = side_coordinate(side, witness_distance)
        state = source_locked_5267_boundary_state(
            problem, coordinate
        )
        topology_rows.append(
            {
                "epsilon_id": problem["job"]["epsilon_id"],
                "job_id": problem["job"]["job_id"],
                "component_id": problem["component_id"],
                "owner_summand": problem["job"]["owner_summand"],
                "side": side,
                "endpoint_distance": witness_distance,
                "coordinate": coordinate,
                "witness_role": (
                    "5267_boundary_state_for_active_tail"
                    if expected_multiplier != 0.0
                    else "5267_boundary_state_for_inactive_tail"
                ),
                "continuation_test": (
                    "5268_surface_scan_to_1e-6_plus_5019_5029_"
                    "endpoint_regularity"
                ),
                "expected_state_u": int(expected["state_u"]),
                "expected_state_v": int(expected["state_v"]),
                "witness_state_u": state["u"],
                "witness_state_v": state["v"],
                "expected_multiplier": expected_multiplier,
                "witness_multiplier": state["multiplier"],
                "state_matches_5267_tail_interval": (
                    int(expected["state_u"]) == int(state["u"])
                    and int(expected["state_v"]) == int(state["v"])
                    and abs(
                        expected_multiplier
                        - float(state["multiplier"])
                    )
                    <= 1.0e-12
                ),
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "base_topology_steps": state["base_topology_steps"],
                "adaptive_topology_steps": state["topology_steps"],
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        values_by_surface: dict[str, list[complex]] = {}
        coordinates = [
            side_coordinate(side, distance)
            for distance in SURFACE_SCAN_COORDINATES
        ]
        for coordinate_value in coordinates:
            values = M5267.M5239.owner_surface_values(
                problem, complex(coordinate_value)
            )
            for surface_id, value in values.items():
                values_by_surface.setdefault(surface_id, []).append(
                    complex(value)
                )
        for surface_id, values in values_by_surface.items():
            magnitudes = np.abs(
                np.asarray(values, dtype=np.complex128)
            )
            real_values = np.real(
                np.asarray(values, dtype=np.complex128)
            )
            surface_rows.append(
                {
                    "epsilon_id": problem["job"]["epsilon_id"],
                    "job_id": problem["job"]["job_id"],
                    "component_id": problem["component_id"],
                    "side": side,
                    "surface_id": surface_id,
                    "scan_distance_minimum": min(
                        SURFACE_SCAN_COORDINATES
                    ),
                    "scan_distance_maximum": max(
                        SURFACE_SCAN_COORDINATES
                    ),
                    "scan_point_count": len(
                        SURFACE_SCAN_COORDINATES
                    ),
                    "minimum_surface_magnitude": float(
                        np.min(magnitudes)
                    ),
                    "median_surface_magnitude": float(
                        np.median(magnitudes)
                    ),
                    "minimum_to_median_ratio": float(
                        np.min(magnitudes)
                        / max(float(np.median(magnitudes)), 1.0e-300)
                    ),
                    "real_sign_change_count": int(
                        sum(
                            real_values[index]
                            * real_values[index + 1]
                            < 0.0
                            for index in range(
                                len(real_values) - 1
                            )
                        )
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return topology_rows, surface_rows


def endpoint_worker(epsilon_id: str) -> dict[str, Any]:
    if epsilon_id not in EPSILON_IDS:
        raise ValueError(f"unsupported epsilon id: {epsilon_id}")
    started = time.perf_counter()
    set_below_normal_priority()
    M5267.WINDING_ATTEMPTS.clear()
    paths = worker_paths(epsilon_id)
    atomic_json(
        paths["status"],
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "state": "RUNNING",
        },
    )
    contract, source_interval_rows = interval_contract(epsilon_id)
    _, problems, track_rows = M5267.build_energy_problems(
        (epsilon_id,)
    )
    topology_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    for problem in problems:
        problem_topology, problem_surfaces = (
            topology_rows_for_problem(problem, contract)
        )
        topology_rows.extend(problem_topology)
        surface_rows.extend(problem_surfaces)
    sample_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    sample_cache: dict[tuple[str, float], complex] = {}

    def total_value(side: str, distance: float) -> complex:
        key = (side, float(distance))
        if key not in sample_cache:
            coordinate = side_coordinate(side, distance)
            values: list[tuple[dict[str, Any], float, complex]] = []
            for problem in problems:
                multiplier = fixed_multiplier(
                    contract, problem["component_id"], side
                )
                value = endpoint_component_value(
                    problem, multiplier, coordinate
                )
                values.append((problem, multiplier, value))
            sample_cache[key] = sum(
                (value for _, _, value in values), 0.0j
            )
        return sample_cache[key]

    for side in ("low", "high"):
        for distance in SAMPLE_COORDINATES:
            coordinate = side_coordinate(side, distance)
            total = 0.0j
            absolute_component_sum = 0.0
            for problem in problems:
                multiplier = fixed_multiplier(
                    contract, problem["component_id"], side
                )
                value = endpoint_component_value(
                    problem, multiplier, coordinate
                )
                total += value
                absolute_component_sum += abs(value)
                component_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "component_id": problem["component_id"],
                        "owner_summand": problem["job"][
                            "owner_summand"
                        ],
                        "side": side,
                        "endpoint_distance": distance,
                        "coordinate": coordinate,
                        "dynamic_multiplier": multiplier,
                        "value_real": value.real,
                        "value_imaginary": value.imag,
                        "value_magnitude": abs(value),
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
            sample_cache[(side, float(distance))] = total
            sample_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "side": side,
                    "endpoint_distance": distance,
                    "coordinate": coordinate,
                    "total_real": total.real,
                    "total_imaginary": total.imag,
                    "total_magnitude": abs(total),
                    "absolute_component_sum": (
                        absolute_component_sum
                    ),
                    "component_cancellation_condition": (
                        absolute_component_sum
                        / max(abs(total), 1.0e-300)
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    quadrature_rows: list[dict[str, Any]] = []
    totals: dict[str, dict[str, dict[str, complex]]] = {
        side: {} for side in ("low", "high")
    }
    for side in ("low", "high"):
        for floor in NUMERICAL_FLOORS:
            floor_key = float(floor).hex()
            totals[side][floor_key] = {}

            def integrand(distance: float) -> complex:
                return total_value(side, float(distance))

            for order in QUADRATURE_ORDERS:
                value = gauss_integral(
                    integrand, floor, TAIL_CUT, order
                )
                totals[side][floor_key][str(order)] = value
                quadrature_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "side": side,
                        "numerical_floor": floor,
                        "tail_cut": TAIL_CUT,
                        "quadrature_order": order,
                        "integral_real": value.real,
                        "integral_imaginary": value.imag,
                        "integral_magnitude": abs(value),
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    topology_matches = all(
        bool(row["state_matches_5267_tail_interval"])
        for row in topology_rows
    )
    maximum_pair_step = max(
        float(row["maximum_pair_projective_step"])
        for row in topology_rows
    )
    maximum_reciprocal_residual = max(
        float(row["maximum_reciprocal_product_residual"])
        for row in topology_rows
    )
    minimum_surface_ratio = min(
        float(row["minimum_to_median_ratio"])
        for row in surface_rows
    )
    maximum_sample_condition = max(
        float(row["component_cancellation_condition"])
        for row in sample_rows
    )
    checks = {
        "six_component_problems_built": len(problems) == 6,
        "all_5267_branch_tracks_pass": all(
            row["pair_set_track_passed"] for row in track_rows
        ),
        "all_tail_boundary_states_match_5267": topology_matches,
        "all_tail_boundary_pair_steps_pass": (
            maximum_pair_step
            <= M5267.PAIR_SET_PROJECTIVE_LIMIT
        ),
        "all_tail_boundary_reciprocal_residuals_pass": (
            maximum_reciprocal_residual
            <= M5267.RECIPROCAL_RESIDUAL_LIMIT
        ),
        "surface_scan_is_finite": (
            all(
                np.isfinite(
                    float(row["minimum_surface_magnitude"])
                )
                for row in surface_rows
            )
            and minimum_surface_ratio > 0.0
        ),
        "sample_values_are_finite": all(
            np.isfinite(float(row["total_real"]))
            and np.isfinite(float(row["total_imaginary"]))
            for row in sample_rows
        ),
        "claims_locked_false": all(
            not row[field]
            for row in sample_rows
            for field in (
                "valid_for_full_phase_space_coefficient",
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "endpoint-worker",
        "epsilon_id": epsilon_id,
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "source_interval_count": len(source_interval_rows),
        "topology_witness_count": len(topology_rows),
        "surface_scan_row_count": len(surface_rows),
        "sample_count": len(sample_rows),
        "component_sample_count": len(component_rows),
        "winding_resolution_attempt_count": len(
            M5267.WINDING_ATTEMPTS
        ),
        "maximum_pair_projective_step": maximum_pair_step,
        "maximum_reciprocal_product_residual": (
            maximum_reciprocal_residual
        ),
        "minimum_surface_to_median_ratio": minimum_surface_ratio,
        "maximum_component_cancellation_condition": (
            maximum_sample_condition
        ),
        "tail_integrals": totals,
        "runtime_seconds": time.perf_counter() - started,
        "valid_for_boundary_anchored_endpoint_topology_handoff": all(
            checks.values()
        ),
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(paths["topology"], topology_rows)
    write_csv(paths["surfaces"], surface_rows)
    write_csv(paths["samples"], sample_rows)
    write_csv(paths["components"], component_rows)
    write_csv(paths["quadrature"], quadrature_rows)
    if M5267.WINDING_ATTEMPTS:
        write_csv(
            paths["winding_attempts"],
            M5267.WINDING_ATTEMPTS,
        )
    atomic_json(paths["result"], result)
    atomic_json(
        paths["status"],
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def complex_value(value: Any) -> complex:
    if isinstance(value, complex):
        return value
    return complex(float(value["real"]), float(value["imaginary"]))


def worker_integral(
    result: dict[str, Any],
    side: str,
    floor: float,
    order: int,
) -> complex:
    return complex_value(
        result["tail_integrals"][side][float(floor).hex()][
            str(order)
        ]
    )


def physical_multiplier() -> float:
    return float(
        M5267.M5239.M5231.PHYSICAL_A00_WEIGHT
        * M5267.M5239.M5231.KERNEL_MULTIPLIER
    )


def combined_sample_rows(
    worker_results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    del worker_results
    samples = {
        epsilon_id: {
            (row["side"], float(row["endpoint_distance"])): row
            for row in read_csv(worker_paths(epsilon_id)["samples"])
        }
        for epsilon_id in EPSILON_IDS
    }
    factor = physical_multiplier()
    rows: list[dict[str, Any]] = []
    for side in ("low", "high"):
        for distance in SAMPLE_COORDINATES:
            E040 = samples["E040"][(side, float(distance))]
            E020 = samples["E020"][(side, float(distance))]
            z040 = complex(
                float(E040["total_real"]),
                float(E040["total_imaginary"]),
            )
            z020 = complex(
                float(E020["total_real"]),
                float(E020["total_imaginary"]),
            )
            value = factor * (2.0 * z020 - z040)
            rows.append(
                {
                    "side": side,
                    "endpoint_distance": distance,
                    "physical_integrand_real": value.real,
                    "physical_integrand_imaginary": value.imag,
                    "physical_integrand_magnitude": abs(value),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def polynomial_endpoint_integrals(
    sample_rows: list[dict[str, Any]],
    side: str,
    floor: float,
) -> dict[str, Any]:
    upper = min(10.0 * floor, TAIL_CUT)
    selected = [
        row
        for row in sample_rows
        if row["side"] == side
        and floor
        <= float(row["endpoint_distance"])
        <= upper
    ]
    if len(selected) < 8:
        raise RuntimeError(
            f"insufficient endpoint witnesses for {side} at {floor}"
        )
    coordinates = np.asarray(
        [
            float(row["endpoint_distance"]) / floor
            for row in selected
        ],
        dtype=float,
    )
    values = np.asarray(
        [
            complex(
                float(row["physical_integrand_real"]),
                float(row["physical_integrand_imaginary"]),
            )
            for row in selected
        ],
        dtype=np.complex128,
    )
    fits: list[dict[str, Any]] = []
    for degree in POLYNOMIAL_DEGREES:
        coefficients = np.polyfit(coordinates, values, degree)
        fitted = np.polyval(coefficients, coordinates)
        residual = float(np.max(np.abs(fitted - values)))
        integral = 0.0j
        for coefficient_index, coefficient in enumerate(
            coefficients
        ):
            power = degree - coefficient_index
            integral += complex(coefficient) / (power + 1)
        integral *= floor
        endpoint_value = complex(np.polyval(coefficients, 0.0))
        fits.append(
            {
                "degree": degree,
                "integral": integral,
                "endpoint_value": endpoint_value,
                "maximum_fit_residual": residual,
            }
        )
    central = next(
        row
        for row in fits
        if row["degree"] == CENTRAL_POLYNOMIAL_DEGREE
    )
    degree_spread = max(
        abs(row["integral"] - central["integral"])
        for row in fits
    )
    fit_residual_cap = (
        max(row["maximum_fit_residual"] for row in fits) * floor
    )
    measured_or_fitted_scale = max(
        max(abs(value) for value in values),
        max(
            abs(row["endpoint_value"]) + row["maximum_fit_residual"]
            for row in fits
        ),
    )
    sample_envelope = (
        ENDPOINT_ENVELOPE_SAFETY_FACTOR * measured_or_fitted_scale
    )
    unresolved_cap = sample_envelope * floor
    return {
        "side": side,
        "floor": floor,
        "fit_upper": upper,
        "sample_count": len(selected),
        "fits": fits,
        "central_integral": central["integral"],
        "central_endpoint_value": central["endpoint_value"],
        "degree_spread": degree_spread,
        "fit_residual_cap": fit_residual_cap,
        "numerical_uncertainty": degree_spread + fit_residual_cap,
        "conditional_endpoint_envelope": sample_envelope,
        "endpoint_envelope_safety_factor": (
            ENDPOINT_ENVELOPE_SAFETY_FACTOR
        ),
        "endpoint_envelope_assumption": (
            "|H(x)| on the unresolved interval does not exceed the "
            "recorded safety factor times the largest measured or fitted "
            "endpoint scale"
        ),
        "unresolved_envelope_cap": unresolved_cap,
    }


def combine_results(
    worker_results: dict[str, dict[str, Any]],
    runtime_seconds: float,
) -> dict[str, Any]:
    parent = read_json(RESULT_5267)
    sample_rows = combined_sample_rows(worker_results)
    write_csv(PHYSICAL_SAMPLES, sample_rows)
    factor = physical_multiplier()
    polynomial_fits = {
        side: {
            float(floor).hex(): polynomial_endpoint_integrals(
                sample_rows, side, floor
            )
            for floor in NUMERICAL_FLOORS
        }
        for side in ("low", "high")
    }
    rows: list[dict[str, Any]] = []
    corrected: dict[float, dict[int, complex]] = {}
    tail_values: dict[float, dict[int, dict[str, complex]]] = {}
    interior_by_order = {
        int(row["quadrature_order"]): complex(
            float(row["subtracted_real"]),
            float(row["subtracted_imaginary"]),
        )
        for row in parent["combined_convergence"]
    }
    for floor in NUMERICAL_FLOORS:
        corrected[floor] = {}
        tail_values[floor] = {}
        floor_key = float(floor).hex()
        for order in QUADRATURE_ORDERS:
            side_values: dict[str, complex] = {}
            for side in ("low", "high"):
                numerical = factor * (
                    2.0
                    * worker_integral(
                        worker_results["E020"],
                        side,
                        floor,
                        order,
                    )
                    - worker_integral(
                        worker_results["E040"],
                        side,
                        floor,
                        order,
                    )
                )
                extrapolated = complex(
                    polynomial_fits[side][floor_key][
                        "central_integral"
                    ]
                )
                side_values[side] = numerical + extrapolated
            tail_values[floor][order] = side_values
            corrected_value = (
                interior_by_order[order]
                + side_values["low"]
                + side_values["high"]
            )
            corrected[floor][order] = corrected_value
    reference_floor = NUMERICAL_FLOORS[0]
    reference = corrected[reference_floor][QUADRATURE_ORDERS[-1]]
    denominator = max(abs(reference), 1.0)
    for floor in NUMERICAL_FLOORS:
        floor_key = float(floor).hex()
        for order in QUADRATURE_ORDERS:
            value = corrected[floor][order]
            low_fit = polynomial_fits["low"][floor_key]
            high_fit = polynomial_fits["high"][floor_key]
            rows.append(
                {
                    "numerical_floor": floor,
                    "quadrature_order": order,
                    "interior_real": interior_by_order[order].real,
                    "interior_imaginary": (
                        interior_by_order[order].imag
                    ),
                    "low_tail_real": tail_values[floor][order][
                        "low"
                    ].real,
                    "low_tail_imaginary": tail_values[floor][order][
                        "low"
                    ].imag,
                    "high_tail_real": tail_values[floor][order][
                        "high"
                    ].real,
                    "high_tail_imaginary": tail_values[floor][order][
                        "high"
                    ].imag,
                    "corrected_real": value.real,
                    "corrected_imaginary": value.imag,
                    "corrected_magnitude": abs(value),
                    "relative_error_to_reference": (
                        abs(value - reference) / denominator
                    ),
                    "low_extrapolation_uncertainty": low_fit[
                        "numerical_uncertainty"
                    ],
                    "high_extrapolation_uncertainty": high_fit[
                        "numerical_uncertainty"
                    ],
                    "low_unresolved_envelope_cap": low_fit[
                        "unresolved_envelope_cap"
                    ],
                    "high_unresolved_envelope_cap": high_fit[
                        "unresolved_envelope_cap"
                    ],
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    write_csv(COMBINED_ROWS, rows)
    reference_rows = [
        row
        for row in rows
        if float(row["numerical_floor"]) == reference_floor
    ]
    low_order_error = next(
        float(row["relative_error_to_reference"])
        for row in reference_rows
        if int(row["quadrature_order"])
        == QUADRATURE_ORDERS[0]
    )
    mid_order_error = next(
        float(row["relative_error_to_reference"])
        for row in reference_rows
        if int(row["quadrature_order"])
        == QUADRATURE_ORDERS[-2]
    )
    floor_references = [
        corrected[floor][QUADRATURE_ORDERS[-1]]
        for floor in NUMERICAL_FLOORS
    ]
    floor_spread = max(
        abs(value - reference) for value in floor_references
    )
    floor_relative_spread = floor_spread / denominator
    selected_low_fit = polynomial_fits["low"][
        float(reference_floor).hex()
    ]
    selected_high_fit = polynomial_fits["high"][
        float(reference_floor).hex()
    ]
    unresolved_cap = (
        float(selected_low_fit["unresolved_envelope_cap"])
        + float(selected_high_fit["unresolved_envelope_cap"])
    )
    unresolved_relative_cap = unresolved_cap / denominator
    endpoint_correction = (
        tail_values[reference_floor][QUADRATURE_ORDERS[-1]][
            "low"
        ]
        + tail_values[reference_floor][QUADRATURE_ORDERS[-1]][
            "high"
        ]
    )
    checks = {
        "both_endpoint_workers_accepted": all(
            bool(worker_results[epsilon_id]["acceptance_passed"])
            for epsilon_id in EPSILON_IDS
        ),
        "low_order_corrected_rule_converged": (
            low_order_error <= LOW_ORDER_ERROR_LIMIT
        ),
        "mid_order_corrected_rule_converged": (
            mid_order_error <= MID_ORDER_ERROR_LIMIT
        ),
        "numerical_floor_stable": (
            floor_relative_spread
            <= FLOOR_STABILITY_RELATIVE_LIMIT
        ),
        "conditional_unresolved_endpoint_envelope_passed": (
            unresolved_relative_cap
            <= UNRESOLVED_CAP_RELATIVE_LIMIT
        ),
        "soft_plus_regularity_theorem_sourced": all(
            path.exists()
            for path in (THEOREM_5010, THEOREM_5019, THEOREM_5029)
        ),
        "claims_locked_false": True,
    }
    formal_reference = str(
        parent["formalization_workbench_end_digest"]
    )
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "soft-energy-endpoint-completion",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "resource_contract": {
            "maximum_task_python_processes": 2,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "soft_plus_regularity_contract": {
            "definition": "H(x)=[g(x)-g(0)]/x",
            "source_5010": str(THEOREM_5010),
            "exact_endpoint_source_5019": str(THEOREM_5019),
            "finite_transport_source_5029": str(THEOREM_5029),
            "interpretation": (
                "the summed transported plus integrand has a finite "
                "fixed-angle endpoint; component labels may separately "
                "be ill-conditioned and are not extrapolated below the "
                "numerical floor"
            ),
        },
        "tail_cut": TAIL_CUT,
        "topology_witness": TOPOLOGY_WITNESS,
        "surface_scan_minimum": SURFACE_SCAN_MINIMUM,
        "topology_bridge": {
            "boundary_state_source": str(SOURCE_5267),
            "boundary_coordinate_low": TAIL_CUT,
            "boundary_coordinate_high": 1.0 - TAIL_CUT,
            "surface_scan_minimum_distance": SURFACE_SCAN_MINIMUM,
            "endpoint_regularization_sources": [
                str(THEOREM_5019),
                str(THEOREM_5029),
            ],
            "direct_numeric_winding_solve_at_x_zero": False,
            "interpretation": (
                "The accepted 5267 boundary state is continued through "
                "a nonzero-surface scan, then joined to the derived finite "
                "soft endpoint. This is a boundary-anchored numerical "
                "continuation, not an interval proof of every sub-floor "
                "winding state."
            ),
        },
        "numerical_floors": list(NUMERICAL_FLOORS),
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "polynomial_degrees": list(POLYNOMIAL_DEGREES),
        "selected_floor": reference_floor,
        "interior_reference": interior_by_order[
            QUADRATURE_ORDERS[-1]
        ],
        "endpoint_correction": endpoint_correction,
        "corrected_fixed_angle_energy_value": reference,
        "low_order_relative_error": low_order_error,
        "mid_order_relative_error": mid_order_error,
        "floor_relative_spread": floor_relative_spread,
        "unresolved_endpoint_envelope_cap": unresolved_cap,
        "unresolved_endpoint_relative_cap": unresolved_relative_cap,
        "unresolved_endpoint_bound_status": {
            "type": "conditional_numerical_envelope",
            "safety_factor": ENDPOINT_ENVELOPE_SAFETY_FACTOR,
            "assumption": (
                "No unresolved sub-floor spike exceeds the safety-factor "
                "envelope; endpoint finiteness is derived, but this "
                "finite-resolution amplitude cap is not interval proof."
            ),
            "valid_for_exact_analytic_bound_claim": False,
        },
        "polynomial_endpoint_fits": polynomial_fits,
        "workers": worker_results,
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": formal_reference,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_reference == formal_end else -1
        ),
        "runtime_seconds": runtime_seconds,
        "decision": (
            "ACCEPT_FIXED_ANGLE_SOFT_ENERGY_ENDPOINT_COMPLETION__PROCEED_TO_ANGULAR_TOPOLOGY"
            if all(checks.values())
            else "REPAIR_SOFT_ENERGY_ENDPOINT_COMPLETION"
        ),
        "claim_boundary": {
            "valid_for_fixed_angle_energy_rule_with_endpoints": all(
                checks.values()
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Both angular integrations and their topology transport "
                "remain pending."
            ),
        },
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": result["mode"],
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "decision": result["decision"],
            "runtime_seconds": runtime_seconds,
        },
    )
    return result


def full_run() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    SOURCE.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-B",
        str(Path(__file__).resolve()),
        "--mode",
        "worker",
        "--epsilon",
        "E020",
    ]
    environment = dict(os.environ)
    with CHILD_LOG.open("w", encoding="utf-8") as child_log:
        child = subprocess.Popen(
            command,
            stdout=child_log,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        E040 = endpoint_worker("E040")
        child_return_code = child.wait()
    E020_path = worker_paths("E020")["result"]
    if child_return_code != 0 and not E020_path.exists():
        raise RuntimeError(
            f"E020 endpoint worker failed with code {child_return_code}"
        )
    E020 = read_json(E020_path)
    return combine_results(
        {"E040": E040, "E020": E020},
        time.perf_counter() - started,
    )


def combine_existing() -> dict[str, Any]:
    previous_runtime = (
        float(read_json(RESULT).get("runtime_seconds", 0.0))
        if RESULT.exists()
        else 0.0
    )
    return combine_results(
        {
            epsilon_id: read_json(
                worker_paths(epsilon_id)["result"]
            )
            for epsilon_id in EPSILON_IDS
        },
        previous_runtime,
    )


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": bool(passed),
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    interior = complex_value(result["interior_reference"])
    correction = complex_value(result["endpoint_correction"])
    corrected = complex_value(
        result["corrected_fixed_angle_energy_value"]
    )
    correction_fraction = abs(correction) / max(abs(corrected), 1.0)
    text = f"""# 5268 - Soft-energy endpoint completion

## Question

Checkpoint 5267 accepted the topology-aware fixed-angle energy integral only on
`{TAIL_CUT:.1e} <= x <= {1.0 - TAIL_CUT:.4f}`. This checkpoint tests and restores
the omitted `x -> 0` and `x -> 1` tails without changing the angular variables.

## Topology bridge

The endpoint branch is not re-solved by an unstable winding calculation at
`x=0`. Instead, each of the six components in both regulators is anchored to
the accepted checkpoint-5267 winding state at `x={TAIL_CUT:.1e}` or
`x={1.0 - TAIL_CUT:.4f}`. The relevant analytic surfaces are scanned down to
endpoint distance `{SURFACE_SCAN_MINIMUM:.1e}`. The remaining approach to the
endpoint uses the exact soft-endpoint and finite pole-coalescence results in
checkpoints 5019 and 5029.

This is a boundary-anchored numerical continuation. It is not an interval proof
of every winding state below the numerical floor.

## Invariant endpoint law

Checkpoint 5010 defines

`H(x) = [g(x)-g(0)]/x`.

For differentiable `g`,

`H(x) = g'(0) + g''(0)x/2 + O(x^2)`.

The separately labelled residue components become ill-conditioned when
reciprocal pole pairs coalesce, while their physical sum remains finite.
Therefore only the invariant regulator combination `2 E020 - E040`, with the
inherited kernel and A00 factor, is extrapolated below the numerical floor.

## Numerical result

The checkpoint-5267 interior value was

`I_interior = {interior.real:.15g} {interior.imag:+.15g} i`.

The completed two-tail correction is

`Delta I_endpoint = {correction.real:.15g} {correction.imag:+.15g} i`,

giving

`I_completed = {corrected.real:.15g} {corrected.imag:+.15g} i`.

The correction is `{correction_fraction:.12g}` of the completed magnitude.
Across numerical floors `{", ".join(f"{value:.1e}" for value in NUMERICAL_FLOORS)}`,
the order-512 result changes by relative fraction
`{float(result['floor_relative_spread']):.12g}`. The corrected order-32 and
order-128 relative errors are `{float(result['low_order_relative_error']):.12g}`
and `{float(result['mid_order_relative_error']):.12g}`.

## Unresolved sub-floor cap

Endpoint finiteness is derived, but the finite-resolution magnitude cap is
conditional rather than an interval proof. The recorded cap assumes no
sub-floor spike exceeds `{ENDPOINT_ENVELOPE_SAFETY_FACTOR:g}` times the largest
measured or fitted endpoint scale. Under that explicit assumption,

`|Delta I_unresolved| <= {float(result['unresolved_endpoint_envelope_cap']):.12g}`,

or `{float(result['unresolved_endpoint_relative_cap']):.12g}` of the completed
fixed-angle magnitude.

## Decision

`{result['decision']}`

Validation passed: `{str(validation_passed).lower()}`.

This accepts a conditional, numerically stable fixed-angle energy rule with both
endpoint tails restored. It does not accept the two angular integrations, the
full phase-space coefficient, a numeric UV fixed point, local GR, or full MTS.

## Next derivation

Restore the two angular integrations while preserving the component topology,
the energy-pole subtraction, and this endpoint rule. The angular Jacobian is
`1/4`; angular chamber transitions and angular endpoint caps must be resolved
before interpreting any coefficient.

## Artifacts

- Runner: `{Path(__file__).resolve()}`
- Result: `{RESULT}`
- Convergence: `{COMBINED_ROWS}`
- Physical endpoint samples: `{PHYSICAL_SAMPLES}`
- E040 worker: `{worker_paths('E040')['result']}`
- E020 worker: `{worker_paths('E020')['result']}`
- Validation: `{VALIDATION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5267)
    workers = {
        epsilon_id: read_json(worker_paths(epsilon_id)["result"])
        for epsilon_id in EPSILON_IDS
    }
    required_csvs = [
        COMBINED_ROWS,
        PHYSICAL_SAMPLES,
        *[
            worker_paths(epsilon_id)[key]
            for epsilon_id in EPSILON_IDS
            for key in (
                "topology",
                "surfaces",
                "samples",
                "components",
                "quadrature",
            )
        ],
    ]
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    topology_rows = [
        row
        for epsilon_id in EPSILON_IDS
        for row in read_csv(worker_paths(epsilon_id)["topology"])
    ]
    surface_rows = [
        row
        for epsilon_id in EPSILON_IDS
        for row in read_csv(worker_paths(epsilon_id)["surfaces"])
    ]
    physical_rows = read_csv(PHYSICAL_SAMPLES)
    convergence_rows = read_csv(COMBINED_ROWS)
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized_outputs = json.dumps(
        {
            "result": result,
            "workers": workers,
            "csvs": csv_rows,
        },
        default=json_default,
    )
    claim_fields = (
        "valid_for_full_phase_space_coefficient",
        "valid_for_numeric_UV_claim",
        "valid_for_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    claim_csv_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in claim_fields)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} recorded source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source digests reproduce",
        ),
        validation_gate(
            "PARENT_5267_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "BOTH_ENDPOINT_WORKERS_ACCEPTED",
            all(
                bool(workers[epsilon_id]["acceptance_passed"])
                for epsilon_id in EPSILON_IDS
            ),
            "E040 and E020 endpoint workers accepted",
        ),
        validation_gate(
            "BOUNDARY_TOPOLOGY_MATCHES_5267",
            (
                len(topology_rows) == 24
                and all(
                    row["state_matches_5267_tail_interval"].lower()
                    == "true"
                    for row in topology_rows
                )
            ),
            f"{len(topology_rows)}/24 boundary topology witnesses",
        ),
        validation_gate(
            "SURFACE_CONTINUATION_FINITE",
            (
                bool(surface_rows)
                and all(
                    math.isfinite(
                        float(row["minimum_surface_magnitude"])
                    )
                    and float(row["minimum_to_median_ratio"]) > 0.0
                    and float(row["scan_distance_minimum"])
                    <= SURFACE_SCAN_MINIMUM
                    for row in surface_rows
                )
            ),
            (
                f"{len(surface_rows)} surface rows through distance "
                f"{SURFACE_SCAN_MINIMUM:.1e}"
            ),
        ),
        validation_gate(
            "PHYSICAL_ENDPOINT_SAMPLES_FINITE",
            (
                len(physical_rows) == 2 * len(SAMPLE_COORDINATES)
                and all(
                    math.isfinite(
                        float(row["physical_integrand_real"])
                    )
                    and math.isfinite(
                        float(row["physical_integrand_imaginary"])
                    )
                    for row in physical_rows
                )
            ),
            f"{len(physical_rows)} finite summed samples",
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "CORRECTED_RULE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "CORRECTED_RULE_CONVERGED",
            (
                len(convergence_rows)
                == len(NUMERICAL_FLOORS) * len(QUADRATURE_ORDERS)
                and float(result["low_order_relative_error"])
                <= LOW_ORDER_ERROR_LIMIT
                and float(result["mid_order_relative_error"])
                <= MID_ORDER_ERROR_LIMIT
                and float(result["floor_relative_spread"])
                <= FLOOR_STABILITY_RELATIVE_LIMIT
            ),
            (
                f"order32={result['low_order_relative_error']}; "
                f"order128={result['mid_order_relative_error']}; "
                f"floor={result['floor_relative_spread']}"
            ),
        ),
        validation_gate(
            "CONDITIONAL_ENVELOPE_EXPLICIT",
            (
                result["unresolved_endpoint_bound_status"]["type"]
                == "conditional_numerical_envelope"
                and not result["unresolved_endpoint_bound_status"][
                    "valid_for_exact_analytic_bound_claim"
                ]
                and float(result["unresolved_endpoint_relative_cap"])
                <= UNRESOLVED_CAP_RELATIVE_LIMIT
            ),
            (
                "conditional relative cap="
                f"{result['unresolved_endpoint_relative_cap']}"
            ),
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized_outputs,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in claim_fields
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_csv_rows
                    for field in claim_fields
                    if field in row
                )
            ),
            "angular, UV, local-GR, and full-MTS claims remain false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 2
                and result["resource_contract"]["worker_math_threads"]
                == 1
                and result["resource_contract"]["windows_priority"]
                == "BelowNormal"
            ),
            "maximum two below-normal single-thread workers",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "validation",
            "state": "COMPLETED",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_FIXED_ANGLE_SOFT_ENERGY_ENDPOINT_COMPLETION"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "formalization_workbench_modified_file_count": (
            0 if current_formal_digest == reference_formal_digest else -1
        ),
        "valid_for_fixed_angle_energy_rule_with_endpoints": passed,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("worker", "full", "combine", "validate"),
        default="full",
    )
    parser.add_argument("--epsilon", choices=EPSILON_IDS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "worker":
        if args.epsilon is None:
            raise RuntimeError("--epsilon is required for worker mode")
        result = endpoint_worker(args.epsilon)
    elif args.mode == "full":
        result = full_run()
    elif args.mode == "combine":
        result = combine_existing()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result.get(
                    "decision",
                    "ENDPOINT_WORKER_COMPLETE",
                ),
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
