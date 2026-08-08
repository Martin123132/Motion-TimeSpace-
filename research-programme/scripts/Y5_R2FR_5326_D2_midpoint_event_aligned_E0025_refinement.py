from __future__ import annotations

import argparse
import cmath
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5326"
SHARDS = SOURCE / "shards"

SCRIPT_5325 = SCRIPTS / "Y5_R2FR_5325_D2_midpoint_E0025_pole_topology_smoke.py"
RESULT_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_pole_topology_smoke_result.json"
VALIDATION_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_pole_topology_smoke_validation.csv"
CONTRACT_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_reduced_MC04_cubature_contract.csv"
PLAN_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_outer_node_plan.csv"
POLES_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_geometric_poles.csv"
CLASSIFICATIONS_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_pole_classification.csv"
PANELS_5325 = FUNCTIONAL_RG / "5325" / "D2_midpoint_E0025_panel_convergence.csv"

EVENT_CANDIDATES = SOURCE / "D2_midpoint_support_event_candidates.csv"
EVENT_CACHE = SOURCE / "D2_midpoint_support_event_state_cache.json"
EVENT_STATES = SOURCE / "D2_midpoint_support_event_state_scan.csv"
EVENTS = SOURCE / "D2_midpoint_refined_support_events.csv"
INITIAL_PLAN = SOURCE / "D2_midpoint_event_aligned_initial_plan.csv"
DRY_RUN = SOURCE / "D2_midpoint_event_aligned_E0025_refinement_dry_run.json"
NODE_MANIFEST = SOURCE / "D2_midpoint_event_aligned_E0025_node_manifest.csv"
ADAPTIVE_PANELS = SOURCE / "D2_midpoint_event_aligned_E0025_adaptive_panels.csv"
OFF_AXIS_POLES = SOURCE / "D2_midpoint_event_aligned_E0025_geometric_poles.csv"
OFF_AXIS_FITS = SOURCE / "D2_midpoint_event_aligned_E0025_pole_residue_fits.csv"
OFF_AXIS_CLASSIFICATIONS = SOURCE / "D2_midpoint_event_aligned_E0025_pole_classification.csv"
CELL_INTEGRALS = SOURCE / "D2_midpoint_event_aligned_E0025_cell_integrals.csv"
ENERGY_REPAIRS = SOURCE / "D2_midpoint_targeted_energy_partition_repairs.csv"
NEAR_SUPPORT_REPAIRS = (
    SOURCE / "D2_midpoint_near_support_pole_subtraction_repairs.csv"
)
NEAR_SUPPORT_FITS = SOURCE / "D2_midpoint_near_support_pole_fits.csv"
NEAR_SUPPORT_IDENTITIES = (
    SOURCE / "D2_midpoint_near_support_masked_identity.csv"
)
FINITE_VALUE = SOURCE / "D2_midpoint_event_aligned_E0025_finite_value.csv"
RESULT = SOURCE / "D2_midpoint_event_aligned_E0025_refinement_result.json"
VALIDATION = SOURCE / "D2_midpoint_event_aligned_E0025_refinement_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5326_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5326-Y5-R2FR-D2-midpoint-event-aligned-E0025-refinement.md"

CHECKPOINT = 5326
PARENT_CHECKPOINT = 5325
MARKER = "MTS_5326_D2_MIDPOINT_EVENT_ALIGNED_E0025_REFINEMENT"
REVISION = "D2-midpoint-event-aligned-E0025-refinement-v1"
NODE_REVISION = "D2-midpoint-event-aligned-E0025-node-v1"
DECAY_NODE_ID = "D2_MID"
EPSILON_ID = "E0025"
EPSILON = 0.0025
EXPECTED_EVENT_COUNT = 7
EXPECTED_TOPOLOGY_PANEL_COUNT = 11
OUTER_ORDERS = (4, 8)
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_ERROR_BUDGET_LIMIT = 1.0e-2
MAXIMUM_ADAPTIVE_DEPTH = 3
EVENT_MARGIN_TOLERANCE = 1.0e-10
EVENT_COORDINATE_ERROR_TOLERANCE = 1.0e-8
EVENT_MAXIMUM_ITERATIONS = 32
BRANCH_DEATH_WIDTH_TOLERANCE = 1.0e-8
DEFAULT_RUNTIME_LIMIT_SECONDS = 2.25 * 3600.0
NEAR_SUPPORT_DISTANCE_CORE_LIMIT = 8.0
NEAR_SUPPORT_FIT_BACKGROUND_DEGREE = 4
NEAR_SUPPORT_FIT_SCALES = (0.75, 1.5)
NEAR_SUPPORT_FIT_UNITS = (
    0.0625,
    0.125,
    0.25,
    0.375,
    0.5,
    0.75,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    4.0,
    5.0,
    6.0,
    7.0,
    8.0,
)
NEAR_SUPPORT_MAXIMUM_POLE_REFINEMENTS = 4
NEAR_SUPPORT_POLE_REFINEMENT_TOLERANCE = 1.0e-11
NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-5
NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT = 1.0e-3
NEAR_SUPPORT_SECOND_ORDER_SUPPRESSION_LIMIT = 1.0e-4
NEAR_SUPPORT_MASKED_IDENTITY_LIMIT = 1.0e-9
NEAR_SUPPORT_REPAIR_REVISION = "active-side-one-sided-laurent-v2"
CLAIM_FIELDS = (
    "valid_for_D2_E0025_fixed_decay_integral",
    "valid_for_D2_regulator_zero_limit",
    "valid_for_decay_angle_integral",
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


M5325 = load_module("mts_5325_for_5326", SCRIPT_5325)
M5312 = M5325.M5312
M5283 = M5325.M5283


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5325.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5325.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5325.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5325.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5325.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5325.complex_fields(prefix, value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5325.validation_gate(gate, passed, detail)


def configure_kernel() -> dict[str, Any]:
    old = M5325.configure_kernel()
    M5312.SHARDS = SHARDS
    M5312.NODE_REVISION = NODE_REVISION
    M5312.CHECKPOINT = CHECKPOINT
    return old


def restore_kernel(old: dict[str, Any]) -> None:
    M5325.restore_kernel(old)


def support_margin(
    pole_real: float, supports: list[dict[str, Any]]
) -> tuple[float, dict[str, Any]]:
    scored: list[tuple[float, dict[str, Any]]] = []
    for support in supports:
        lower = float(support["lower"])
        upper = float(support["upper"])
        if lower <= pole_real <= upper:
            margin = min(pole_real - lower, upper - pole_real)
        elif pole_real < lower:
            margin = pole_real - lower
        else:
            margin = upper - pole_real
        scored.append((margin, support))
    if not scored:
        raise RuntimeError("target term has no reduced support")
    return max(scored, key=lambda item: item[0])


def event_cache_key(
    panel_index: int,
    term_id: str,
    primary_surface_id: str,
    coordinate: float,
) -> str:
    return (
        f"P{panel_index:02d}|{term_id}|{primary_surface_id}|"
        f"{coordinate:.17g}"
    )


def load_event_cache() -> dict[str, Any]:
    contract_sha256 = digest(CONTRACT_5325)
    pole_sha256 = digest(POLES_5325)
    if EVENT_CACHE.exists():
        value = read_json(EVENT_CACHE)
        if (
            value.get("revision") == REVISION
            and value.get("contract_sha256") == contract_sha256
            and value.get("parent_pole_sha256") == pole_sha256
        ):
            for state in value.get("states", {}).values():
                state.setdefault(
                    "branch_exists", state.get("pole_real", "") not in (None, "")
                )
            return value
    return {
        "revision": REVISION,
        "contract_sha256": contract_sha256,
        "parent_pole_sha256": pole_sha256,
        "states": {},
    }


def branch_state(
    panel_index: int,
    term_id: str,
    primary_surface_id: str,
    coordinate: float,
    contract: list[dict[str, str]],
    cache: dict[str, Any],
) -> dict[str, Any]:
    key = event_cache_key(
        panel_index, term_id, primary_surface_id, coordinate
    )
    if key in cache["states"]:
        return dict(cache["states"][key])
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells).get(term_id, [])
    node = {
        "node_id": f"EVENT_SCAN_{len(cache['states']) + 1:04d}",
        "x_panel_index": panel_index,
        "outer_order": 0,
        "absolute_soft_cosine": coordinate,
    }
    poles = M5312.scan_term_poles(node, term_id, supports)
    selected = [
        row
        for row in poles
        if row["primary_surface_id"] == primary_surface_id
    ]
    if len(selected) > 1:
        raise RuntimeError(
            f"expected at most one {term_id} {primary_surface_id} branch at {coordinate}, "
            f"found {len(selected)}"
        )
    if selected:
        pole = selected[0]
        margin, support = support_margin(float(pole["pole_real"]), supports)
        row = {
            "x_panel_index": panel_index,
            "term_id": term_id,
            "primary_surface_id": primary_surface_id,
            "absolute_soft_cosine": coordinate,
            "branch_exists": True,
            "pole_real": float(pole["pole_real"]),
            "pole_imaginary": float(pole["pole_imaginary"]),
            "support_id": support["support_id"],
            "support_energy_lower": float(support["lower"]),
            "support_energy_upper": float(support["upper"]),
            "signed_support_margin": margin,
            "inside_reduced_term_support": margin >= 0.0,
            **{field: False for field in CLAIM_FIELDS},
        }
    else:
        row = {
            "x_panel_index": panel_index,
            "term_id": term_id,
            "primary_surface_id": primary_surface_id,
            "absolute_soft_cosine": coordinate,
            "branch_exists": False,
            "pole_real": "",
            "pole_imaginary": "",
            "support_id": "",
            "support_energy_lower": "",
            "support_energy_upper": "",
            "signed_support_margin": "",
            "inside_reduced_term_support": False,
            **{field: False for field in CLAIM_FIELDS},
        }
    cache["states"][key] = row
    atomic_json(EVENT_CACHE, cache)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "RUNNING",
            "stage": "D2_SUPPORT_EVENT_ROOT_DERIVATION",
            "cached_event_state_count": len(cache["states"]),
        },
    )
    return dict(row)


def material_branch_keys() -> set[tuple[int, str, str]]:
    poles = read_csv(POLES_5325)
    classifications = read_csv(CLASSIFICATIONS_5325)
    pole_lookup = {
        (row["node_id"], row["term_id"], row["pole_id"]): row
        for row in poles
    }
    keys: set[tuple[int, str, str]] = set()
    for row in classifications:
        if not parse_bool(row["material_simple_pole"]):
            continue
        pole = pole_lookup[(row["node_id"], row["term_id"], row["pole_id"])]
        keys.add(
            (
                int(pole["x_panel_index"]),
                pole["term_id"],
                pole["primary_surface_id"],
            )
        )
    return keys


def event_candidate_rows() -> list[dict[str, Any]]:
    plan = read_csv(PLAN_5325)
    poles = read_csv(POLES_5325)
    pole_lookup: dict[tuple[str, str, str], dict[str, str]] = {
        (row["node_id"], row["term_id"], row["primary_surface_id"]): row
        for row in poles
    }
    rows: list[dict[str, Any]] = []
    for panel_index, term_id, surface_id in sorted(material_branch_keys()):
        states: dict[float, bool] = {}
        for node in plan:
            if int(node["x_panel_index"]) != panel_index:
                continue
            coordinate = float(node["absolute_soft_cosine"])
            pole = pole_lookup.get((node["node_id"], term_id, surface_id))
            states[coordinate] = bool(
                pole is not None
                and parse_bool(pole["inside_reduced_term_support"])
            )
        ordered = sorted(states.items())
        for (left, left_inside), (right, right_inside) in zip(
            ordered[:-1], ordered[1:]
        ):
            if left_inside == right_inside:
                continue
            rows.append(
                {
                    "candidate_id": f"C{len(rows) + 1:02d}",
                    "x_panel_index": panel_index,
                    "term_id": term_id,
                    "primary_surface_id": surface_id,
                    "left_coordinate": left,
                    "right_coordinate": right,
                    "left_inside_support": left_inside,
                    "right_inside_support": right_inside,
                    "event_type": (
                        "SUPPORT_ENTRY" if not left_inside else "SUPPORT_EXIT"
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    write_csv(
        EVENT_CANDIDATES,
        rows,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return rows


def refine_event(
    candidate: dict[str, Any],
    contract: list[dict[str, str]],
    cache: dict[str, Any],
) -> dict[str, Any]:
    panel_index = int(candidate["x_panel_index"])
    term_id = str(candidate["term_id"])
    surface_id = str(candidate["primary_surface_id"])
    left = float(candidate["left_coordinate"])
    right = float(candidate["right_coordinate"])
    left_state = branch_state(
        panel_index, term_id, surface_id, left, contract, cache
    )
    right_state = branch_state(
        panel_index, term_id, surface_id, right, contract, cache
    )
    initial_left = left
    initial_right = right
    left_exists = parse_bool(left_state["branch_exists"])
    right_exists = parse_bool(right_state["branch_exists"])
    if left_exists != right_exists:
        iteration_count = 0
        while (
            right - left > BRANCH_DEATH_WIDTH_TOLERANCE
            and iteration_count < EVENT_MAXIMUM_ITERATIONS
        ):
            iteration_count += 1
            trial = 0.5 * (left + right)
            middle = branch_state(
                panel_index, term_id, surface_id, trial, contract, cache
            )
            if parse_bool(middle["branch_exists"]) == left_exists:
                left = trial
                left_state = middle
            else:
                right = trial
                right_state = middle
        coordinate = 0.5 * (left + right)
        existing_state = left_state if left_exists else right_state
        coordinate_error = 0.5 * (right - left)
        passes = coordinate_error <= EVENT_COORDINATE_ERROR_TOLERANCE
        return {
            "event_id": f"E{int(candidate['candidate_id'][1:]):02d}",
            "candidate_id": candidate["candidate_id"],
            "event_type": "BRANCH_DEATH",
            "x_panel_index": panel_index,
            "term_id": term_id,
            "primary_surface_id": surface_id,
            "source_bracket_left": initial_left,
            "source_bracket_right": initial_right,
            "event_coordinate": coordinate,
            "event_pole_real": existing_state["pole_real"],
            "event_support_lower": existing_state["support_energy_lower"],
            "event_support_upper": existing_state["support_energy_upper"],
            "event_signed_support_margin": existing_state[
                "signed_support_margin"
            ],
            "source_crossing_slope": "",
            "event_coordinate_error_estimate": coordinate_error,
            "iteration_count": iteration_count,
            "event_contract_passes": passes,
            "contract_sha256": digest(CONTRACT_5325),
            "parent_pole_sha256": digest(POLES_5325),
            **{field: False for field in CLAIM_FIELDS},
        }
    if not left_exists:
        raise RuntimeError(
            f"candidate {candidate['candidate_id']} has no branch at either endpoint"
        )
    initial_left_margin = float(left_state["signed_support_margin"])
    initial_right_margin = float(right_state["signed_support_margin"])
    if initial_left_margin * initial_right_margin > 0.0:
        raise RuntimeError(f"candidate {candidate['candidate_id']} does not bracket zero")
    selected = left_state
    iteration_count = 0
    for iteration_count in range(1, EVENT_MAXIMUM_ITERATIONS + 1):
        left_margin = float(left_state["signed_support_margin"])
        right_margin = float(right_state["signed_support_margin"])
        denominator = right_margin - left_margin
        trial = (
            (left * right_margin - right * left_margin) / denominator
            if denominator != 0.0
            else 0.5 * (left + right)
        )
        guard = 0.05 * (right - left)
        if not left + guard < trial < right - guard:
            trial = 0.5 * (left + right)
        selected = branch_state(
            panel_index, term_id, surface_id, trial, contract, cache
        )
        margin = float(selected["signed_support_margin"])
        if left_margin * margin <= 0.0:
            right = trial
            right_state = selected
        else:
            left = trial
            left_state = selected
        if abs(margin) <= EVENT_MARGIN_TOLERANCE:
            break
    source_width = initial_right - initial_left
    source_slope = (
        (initial_right_margin - initial_left_margin) / source_width
    )
    coordinate_error = abs(float(selected["signed_support_margin"])) / max(
        abs(source_slope), 1.0e-300
    )
    passes = (
        coordinate_error <= EVENT_COORDINATE_ERROR_TOLERANCE
        and abs(float(selected["signed_support_margin"]))
        <= EVENT_MARGIN_TOLERANCE
    )
    return {
        "event_id": f"E{int(candidate['candidate_id'][1:]):02d}",
        "candidate_id": candidate["candidate_id"],
        "event_type": candidate["event_type"],
        "x_panel_index": panel_index,
        "term_id": term_id,
        "primary_surface_id": surface_id,
        "source_bracket_left": initial_left,
        "source_bracket_right": initial_right,
        "event_coordinate": selected["absolute_soft_cosine"],
        "event_pole_real": selected["pole_real"],
        "event_support_lower": selected["support_energy_lower"],
        "event_support_upper": selected["support_energy_upper"],
        "event_signed_support_margin": selected["signed_support_margin"],
        "source_crossing_slope": source_slope,
        "event_coordinate_error_estimate": coordinate_error,
        "iteration_count": iteration_count,
        "event_contract_passes": passes,
        "contract_sha256": digest(CONTRACT_5325),
        "parent_pole_sha256": digest(POLES_5325),
        **{field: False for field in CLAIM_FIELDS},
    }


def event_cache_current() -> bool:
    if not EVENTS.exists():
        return False
    rows = read_csv(EVENTS)
    return (
        len(rows) == EXPECTED_EVENT_COUNT
        and all(parse_bool(row["event_contract_passes"]) for row in rows)
        and all(row["contract_sha256"] == digest(CONTRACT_5325) for row in rows)
        and all(row["parent_pole_sha256"] == digest(POLES_5325) for row in rows)
    )


def derive_events() -> list[dict[str, Any]]:
    candidates = event_candidate_rows()
    if len(candidates) != EXPECTED_EVENT_COUNT:
        raise RuntimeError(
            f"expected {EXPECTED_EVENT_COUNT} event candidates, found {len(candidates)}"
        )
    if event_cache_current():
        return read_csv(EVENTS)
    contract = read_csv(CONTRACT_5325)
    cache = load_event_cache()
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        rows.append(refine_event(candidate, contract, cache))
        write_csv(
            EVENTS,
            rows,
            ["event_id", "x_panel_index", "term_id", "primary_surface_id"],
        )
    states = list(cache["states"].values())
    states.sort(
        key=lambda row: (
            int(row["x_panel_index"]),
            row["term_id"],
            row["primary_surface_id"],
            float(row["absolute_soft_cosine"]),
        )
    )
    write_csv(
        EVENT_STATES,
        states,
        ["x_panel_index", "term_id", "primary_surface_id", "absolute_soft_cosine"],
    )
    return rows


def panel_limits(contract: list[dict[str, str]]) -> dict[int, tuple[float, float]]:
    rows: dict[int, list[dict[str, str]]] = {}
    for row in contract:
        rows.setdefault(int(row["x_panel_index"]), []).append(row)
    return {
        panel: (
            min(float(row["lower_absolute_soft_cosine"]) for row in local),
            max(float(row["upper_absolute_soft_cosine"]) for row in local),
        )
        for panel, local in rows.items()
    }


def clustered_panel_events(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered = sorted(events, key=lambda row: float(row["event_coordinate"]))
    clusters: list[list[dict[str, Any]]] = []
    for event in ordered:
        if not clusters:
            clusters.append([event])
            continue
        previous = clusters[-1]
        previous_coordinate = sum(
            float(row["event_coordinate"]) for row in previous
        ) / len(previous)
        tolerance = max(
            5.0e-10,
            4.0
            * (
                max(
                    float(row["event_coordinate_error_estimate"])
                    for row in previous
                )
                + float(event["event_coordinate_error_estimate"])
            ),
        )
        if abs(float(event["event_coordinate"]) - previous_coordinate) <= tolerance:
            previous.append(event)
        else:
            clusters.append([event])
    return [
        {
            "event_coordinate": sum(
                float(row["event_coordinate"]) for row in cluster
            )
            / len(cluster),
            "event_ids": "|".join(row["event_id"] for row in cluster),
            "event_types": "|".join(
                sorted({str(row["event_type"]) for row in cluster})
            ),
            "event_count": len(cluster),
        }
        for cluster in clusters
    ]


def expected_initial_segment_count(events: list[dict[str, Any]]) -> int:
    by_panel: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        by_panel.setdefault(int(event["x_panel_index"]), []).append(event)
    return sum(
        1 if panel not in by_panel else 2 * len(clustered_panel_events(by_panel[panel]))
        for panel in range(1, EXPECTED_TOPOLOGY_PANEL_COUNT + 1)
    )


def build_initial_plan(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = read_csv(CONTRACT_5325)
    limits = panel_limits(contract)
    by_panel: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        by_panel.setdefault(int(event["x_panel_index"]), []).append(event)
    rows: list[dict[str, Any]] = []
    segment_counter = 0
    for panel_index in sorted(limits):
        lower, upper = limits[panel_index]
        local_events = clustered_panel_events(by_panel.get(panel_index, []))
        if not local_events:
            pieces = [(lower, upper, 0, "", "SMOOTH_TOPOLOGY_PANEL")]
        else:
            pieces: list[tuple[float, float, int, float | str, str]] = []
            first = local_events[0]
            first_coordinate = float(first["event_coordinate"])
            pieces.append(
                (
                    lower,
                    first_coordinate,
                    -1,
                    first_coordinate,
                    str(first["event_types"]),
                )
            )
            for left_event, right_event in zip(local_events[:-1], local_events[1:]):
                left_coordinate = float(left_event["event_coordinate"])
                right_coordinate = float(right_event["event_coordinate"])
                midpoint = 0.5 * (left_coordinate + right_coordinate)
                pieces.extend(
                    [
                        (
                            left_coordinate,
                            midpoint,
                            1,
                            left_coordinate,
                            str(left_event["event_types"]),
                        ),
                        (
                            midpoint,
                            right_coordinate,
                            -1,
                            right_coordinate,
                            str(right_event["event_types"]),
                        ),
                    ]
                )
            last = local_events[-1]
            last_coordinate = float(last["event_coordinate"])
            pieces.append(
                (
                    last_coordinate,
                    upper,
                    1,
                    last_coordinate,
                    str(last["event_types"]),
                )
            )
        for local_index, (left, right, direction, event, event_type) in enumerate(
            pieces, start=1
        ):
            if not left < right:
                raise RuntimeError(f"panel {panel_index} segment is reversed")
            segment_counter += 1
            segment_id = f"P{panel_index:02d}S{local_index:02d}"
            rows.append(
                {
                    "epsilon_id": EPSILON_ID,
                    "epsilon": EPSILON,
                    "x_panel_index": panel_index,
                    "initial_segment_id": segment_id,
                    "adaptive_panel_id": segment_id,
                    "adaptive_depth": 0,
                    "parent_adaptive_panel_id": "",
                    "lower_absolute_soft_cosine": left,
                    "upper_absolute_soft_cosine": right,
                    "segment_width": right - left,
                    "transform_direction": direction,
                    "event_coordinate": event,
                    "event_type": event_type,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    write_csv(
        INITIAL_PLAN,
        rows,
        ["x_panel_index", "initial_segment_id", "adaptive_panel_id"],
    )
    return rows


def plan_sha256(initial: list[dict[str, Any]]) -> str:
    payload = {
        "revision": REVISION,
        "node_revision": NODE_REVISION,
        "contract_sha256": digest(CONTRACT_5325),
        "events_sha256": digest(EVENTS),
        "outer_orders": OUTER_ORDERS,
        "energy_orders": M5312.ENERGY_ORDERS,
        "maximum_adaptive_depth": MAXIMUM_ADAPTIVE_DEPTH,
        "initial_geometry": [
            {
                key: row[key]
                for key in (
                    "x_panel_index",
                    "initial_segment_id",
                    "lower_absolute_soft_cosine",
                    "upper_absolute_soft_cosine",
                    "transform_direction",
                    "event_coordinate",
                )
            }
            for row in initial
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5325,
        RESULT_5325,
        VALIDATION_5325,
        CONTRACT_5325,
        PLAN_5325,
        POLES_5325,
        CLASSIFICATIONS_5325,
        PANELS_5325,
        EVENT_CANDIDATES,
        EVENT_STATES,
        EVENTS,
        INITIAL_PLAN,
        DRY_RUN,
    ]
    if ENERGY_REPAIRS.exists():
        paths.append(ENERGY_REPAIRS)
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    old = configure_kernel()
    try:
        parent = read_json(RESULT_5325)
        parent_validation = read_csv(VALIDATION_5325)
        candidates = event_candidate_rows()
        events = derive_events()
        initial = build_initial_plan(events)
        limits = panel_limits(read_csv(CONTRACT_5325))
        total_width = sum(float(row["segment_width"]) for row in initial)
        event_panels = {int(row["x_panel_index"]) for row in events}
        checks = {
            "parent_5325_diagnostic_accepted": bool(parent["acceptance_passed"])
            and not bool(parent["finite_regulator_fixed_decay_integral_accepted"]),
            "parent_5325_validation_passes": all(
                parse_bool(row["passed"]) for row in parent_validation
            ),
            "seven_material_support_crossings_derived": (
                len(candidates) == len(events) == EXPECTED_EVENT_COUNT
                and all(parse_bool(row["event_contract_passes"]) for row in events)
                and event_panels == {1, 7, 8, 10}
            ),
            "event_aligned_plan_covers_absolute_soft_domain": (
                len(limits) == EXPECTED_TOPOLOGY_PANEL_COUNT
                and len(initial) == expected_initial_segment_count(events)
                and abs(total_width - M5312.M5308.angular_limit()) <= 2.0e-12
                and all(float(row["segment_width"]) > 0.0 for row in initial)
            ),
            "Q4_Q8_adaptive_contract_is_stricter_than_parent_smoke": (
                OUTER_ORDERS == (4, 8)
                and LOCAL_OUTER_CHANGE_LIMIT
                == M5312.OUTER_RELATIVE_CHANGE_LIMIT
            ),
            "formalization_workbench_unchanged": (
                M5283.formal_inventory_digest()
                == parent["formalization_workbench_end_digest"]
            ),
        }
        accepted = all(checks.values())
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "mode": "dry-run",
            "checks": checks,
            "acceptance_passed": accepted,
            "decision": (
                "DRY_RUN_ACCEPTED__RUN_D2_EVENT_ALIGNED_E0025_REFINEMENT"
                if accepted
                else "D2_EVENT_ALIGNED_E0025_REFINEMENT_DRY_RUN_BLOCKED"
            ),
            "event_candidate_count": len(candidates),
            "refined_event_count": len(events),
            "initial_segment_count": len(initial),
            "node_plan_sha256": plan_sha256(initial),
            "runtime_seconds": time.perf_counter() - started,
            **{field: False for field in CLAIM_FIELDS},
        }
        atomic_json(DRY_RUN, result)
        return result
    finally:
        restore_kernel(old)


def load_validated_dry_run() -> dict[str, Any]:
    required = (DRY_RUN, EVENT_CANDIDATES, EVENT_STATES, EVENTS, INITIAL_PLAN)
    if not all(path.exists() for path in required):
        return dry_run()
    cached = read_json(DRY_RUN)
    events = read_csv(EVENTS)
    initial = read_csv(INITIAL_PLAN)
    current = (
        bool(cached.get("acceptance_passed"))
        and cached.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_D2_EVENT_ALIGNED_E0025_REFINEMENT"
        and len(events) == EXPECTED_EVENT_COUNT
        and all(parse_bool(row["event_contract_passes"]) for row in events)
        and len(initial) == expected_initial_segment_count(events)
        and cached.get("node_plan_sha256") == plan_sha256(initial)
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5325))
    )
    return cached if current else dry_run()


def panel_nodes(panel: dict[str, Any]) -> list[dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    direction = int(panel["transform_direction"])
    rows: list[dict[str, Any]] = []
    for order in OUTER_ORDERS:
        nodes, weights = M5312.np.polynomial.legendre.leggauss(order)
        for index, (local_node, weight) in enumerate(zip(nodes, weights), start=1):
            if direction == 0:
                half = 0.5 * (upper - lower)
                midpoint = 0.5 * (upper + lower)
                coordinate = midpoint + half * float(local_node)
                mapped_weight = half * float(weight)
                transform_coordinate = float(local_node)
                transform_jacobian = half
            else:
                event = float(panel["event_coordinate"])
                maximum_t = math.sqrt(upper - lower)
                local_t = 0.5 * maximum_t * (1.0 + float(local_node))
                coordinate = event + direction * local_t**2
                mapped_weight = (
                    0.5 * maximum_t * float(weight) * 2.0 * local_t
                )
                transform_coordinate = local_t
                transform_jacobian = 2.0 * local_t
            rows.append(
                {
                    "node_id": (
                        f"P{int(panel['x_panel_index']):02d}_"
                        f"{panel['adaptive_panel_id']}_Q{order:02d}_N{index:02d}"
                    ),
                    "x_panel_index": int(panel["x_panel_index"]),
                    "outer_order": order,
                    "local_node_index": index,
                    "initial_segment_id": panel["initial_segment_id"],
                    "adaptive_panel_id": panel["adaptive_panel_id"],
                    "adaptive_depth": int(panel["adaptive_depth"]),
                    "event_type": panel["event_type"],
                    "transform_direction": direction,
                    "transform_coordinate": transform_coordinate,
                    "transform_jacobian": transform_jacobian,
                    "absolute_soft_cosine": coordinate,
                    "mapped_outer_weight": mapped_weight,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def split_panel(panel: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    midpoint = 0.5 * (lower + upper)
    direction = int(panel["transform_direction"])
    common = {
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "x_panel_index": int(panel["x_panel_index"]),
        "initial_segment_id": panel["initial_segment_id"],
        "adaptive_depth": int(panel["adaptive_depth"]) + 1,
        "parent_adaptive_panel_id": panel["adaptive_panel_id"],
        "event_type": panel["event_type"],
        **{field: False for field in CLAIM_FIELDS},
    }
    if direction < 0:
        left_direction, right_direction = 0, -1
        left_event, right_event = "", panel["event_coordinate"]
    elif direction > 0:
        left_direction, right_direction = 1, 0
        left_event, right_event = panel["event_coordinate"], ""
    else:
        left_direction = right_direction = 0
        left_event = right_event = ""
    left = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}L",
        "lower_absolute_soft_cosine": lower,
        "upper_absolute_soft_cosine": midpoint,
        "segment_width": midpoint - lower,
        "transform_direction": left_direction,
        "event_coordinate": left_event,
    }
    right = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}R",
        "lower_absolute_soft_cosine": midpoint,
        "upper_absolute_soft_cosine": upper,
        "segment_width": upper - midpoint,
        "transform_direction": right_direction,
        "event_coordinate": right_event,
    }
    return left, right


def near_support_unmasked_evaluator(
    base_context: dict[str, Any],
    term_id: str,
) -> Any:
    specification = M5312.M5308.SURFACE_LOOKUP[term_id]
    component_id = term_id.split("_", 1)[0]
    soft_sign = int(specification["soft_sign"])
    decay_sign = int(specification["decay_sign"])
    cache: dict[tuple[float, float], dict[str, Any]] = {}

    def evaluate(energy: float, coordinate: float) -> dict[str, Any]:
        key = (float(energy), float(coordinate))
        if key in cache:
            return cache[key]
        context = M5312.M5308.M5302.local_context(
            base_context,
            coordinate,
            soft_sign,
            decay_sign,
        )
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        inventory = context["inventories"][M5312.EPSILON_ID]
        target = inventory["target"]
        component = inventory["components"][component_id]
        rationals = M5312.M5280.M5274.M5231.root_rationals(event, target)
        selection = M5312.M5280.M5279.algebraic_component_selector(
            event,
            target,
            component,
            rationals,
        )
        labels = selection["selected_labels"]
        mask_active, orientation, _, _ = (
            M5312.M5280.M5277.exact_mask_orientation(
                labels,
                event,
                context["surfaces"],
            )
        )
        high_precision_event = M5312.M5280.M5275.event_as_mp(event)
        relative_root, root_residual, refinement_distance = (
            M5312.M5280.M5275.refine_relative_root(
                high_precision_event,
                inventory["high_precision_target"],
                labels,
                selection["selected_root"],
            )
        )
        coefficient = M5312.M5280.coefficient_at_exponent(
            high_precision_event,
            inventory["high_precision_target"],
            labels,
            relative_root,
            M5312.M5280.FAST_DELTA_EXPONENT,
        )
        collision_jacobian = M5312.M5280.M5277.mp_collision_jacobian(
            high_precision_event,
            inventory["high_precision_target"],
            labels,
            relative_root,
        )
        winding_delta = M5312.M5280.M5277.source_winding_delta(
            component,
            selection["selected_role"],
        )
        residue = M5312.M5280.M5277.residue_from_coefficient(
            coefficient["total_coefficient"],
            relative_root,
            coefficient["global_root"],
            collision_jacobian,
            orientation,
            winding_delta,
        )
        cache[key] = {
            "value": complex(residue),
            "mask_active": bool(mask_active),
            "orientation": int(orientation),
            "selected_labels": "|".join(labels),
            "selected_role": selection["selected_role"],
            "root_equation_residual": float(root_residual),
            "root_refinement_chordal_distance": float(refinement_distance),
        }
        return cache[key]

    return evaluate


def near_support_pole_side(
    pole: complex,
    lower: float,
    upper: float,
) -> str:
    if pole.real < lower:
        return "BELOW_SUPPORT"
    if pole.real > upper:
        return "ABOVE_SUPPORT"
    return "INSIDE_SUPPORT"


def near_support_boundary_distance(
    pole: complex,
    lower: float,
    upper: float,
) -> float:
    side = near_support_pole_side(pole, lower, upper)
    if side == "BELOW_SUPPORT":
        return lower - pole.real
    if side == "ABOVE_SUPPORT":
        return pole.real - upper
    return min(pole.real - lower, upper - pole.real)


def active_support_fit_geometry(
    pole: complex,
    lower: float,
    upper: float,
) -> tuple[float, int, str]:
    side = near_support_pole_side(pole, lower, upper)
    if side == "BELOW_SUPPORT":
        return lower, 1, "LOWER"
    if side == "ABOVE_SUPPORT":
        return upper, -1, "UPPER"
    if pole.real - lower <= upper - pole.real:
        return lower, 1, "LOWER"
    return upper, -1, "UPPER"


def near_support_fit_radius(
    pole: complex,
    lower: float,
    upper: float,
) -> float:
    distance = near_support_boundary_distance(pole, lower, upper)
    if distance <= 1.0e-12:
        return 0.0
    maximum_sample_unit = max(abs(value) for value in NEAR_SUPPORT_FIT_UNITS)
    support_safe = 0.8 * (upper - lower) / (
        maximum_sample_unit * max(NEAR_SUPPORT_FIT_SCALES)
    )
    return min(distance, support_safe)


def near_support_laurent_fit(
    coordinate: float,
    pole: complex,
    lower: float,
    upper: float,
    fit_scale: float,
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    radius = near_support_fit_radius(pole, lower, upper)
    if radius <= 0.0:
        raise RuntimeError("nonpositive near-support fit radius")
    boundary, direction, _ = active_support_fit_geometry(pole, lower, upper)
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    metadata: list[dict[str, Any]] = []
    for unit in NEAR_SUPPORT_FIT_UNITS:
        offset = unit * fit_scale * radius
        energy = boundary + direction * offset
        if not lower < energy < upper:
            raise RuntimeError("near-support fit sample left active support")
        evaluation = evaluate_unmasked(energy, coordinate)
        background_coordinate = offset / radius
        matrix_rows.append(
            [
                (radius / (energy - pole)) ** 2,
                radius / (energy - pole),
                *[
                    complex(background_coordinate**power)
                    for power in range(
                        NEAR_SUPPORT_FIT_BACKGROUND_DEGREE + 1
                    )
                ],
            ]
        )
        values.append(evaluation["value"])
        metadata.append(evaluation)
    matrix = M5312.np.asarray(matrix_rows, dtype=M5312.np.complex128)
    vector = M5312.np.asarray(values, dtype=M5312.np.complex128)
    coefficients, _, _, _ = M5312.np.linalg.lstsq(
        matrix,
        vector,
        rcond=None,
    )
    predicted = matrix @ coefficients
    residual = float(
        M5312.np.linalg.norm(predicted - vector)
        / max(M5312.np.linalg.norm(vector), 1.0)
    )
    return {
        "fit_scale": fit_scale,
        "fit_radius": radius,
        "fit_sample_count": len(NEAR_SUPPORT_FIT_UNITS),
        "fit_relative_residual": residual,
        "second_order_coefficient": complex(coefficients[0]) * radius**2,
        "simple_residue": complex(coefficients[1]) * radius,
        "all_fit_samples_mask_active": all(
            bool(row["mask_active"]) for row in metadata
        ),
        "fit_mask_state_count": len(
            {bool(row["mask_active"]) for row in metadata}
        ),
        "fit_mask_states": "|".join(
            sorted({str(bool(row["mask_active"])) for row in metadata})
        ),
        "fit_orientation_count": len(
            {int(row["orientation"]) for row in metadata}
        ),
        "fit_label_count": len(
            {str(row["selected_labels"]) for row in metadata}
        ),
        "fit_role_count": len(
            {str(row["selected_role"]) for row in metadata}
        ),
        "maximum_root_equation_residual": max(
            float(row["root_equation_residual"]) for row in metadata
        ),
        "maximum_root_refinement_chordal_distance": max(
            float(row["root_refinement_chordal_distance"])
            for row in metadata
        ),
    }


def refine_near_support_simple_pole(
    coordinate: float,
    source: dict[str, Any],
    evaluate_unmasked: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    lower = float(source["support_energy_lower"])
    upper = float(source["support_energy_upper"])
    geometric = complex(
        float(source["pole_real"]),
        float(source["pole_imaginary"]),
    )
    refined = geometric
    iteration_rows: list[dict[str, Any]] = []
    for iteration in range(1, NEAR_SUPPORT_MAXIMUM_POLE_REFINEMENTS + 1):
        fit = near_support_laurent_fit(
            coordinate,
            refined,
            lower,
            upper,
            1.0,
            evaluate_unmasked,
        )
        residue = fit["simple_residue"]
        correction = (
            fit["second_order_coefficient"] / residue
            if abs(residue) > 0.0
            else complex(math.inf, math.inf)
        )
        iteration_rows.append(
            {
                "fit_row_type": "NEAR_SUPPORT_POLE_REFINEMENT_ITERATION",
                "pole_refinement_iteration": iteration,
                **complex_fields("input_pole", refined),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields("simple_residue_R1", residue),
                **complex_fields("pole_correction_R2_over_R1", correction),
                "fit_relative_residual": fit["fit_relative_residual"],
                "fit_radius": fit["fit_radius"],
            }
        )
        if not math.isfinite(abs(correction)):
            break
        refined += correction
        if abs(correction) <= NEAR_SUPPORT_POLE_REFINEMENT_TOLERANCE:
            break
    final_fits = [
        near_support_laurent_fit(
            coordinate,
            refined,
            lower,
            upper,
            scale,
            evaluate_unmasked,
        )
        for scale in NEAR_SUPPORT_FIT_SCALES
    ]
    first, second = final_fits
    residue_change = M5312.relative_complex_change(
        first["simple_residue"],
        second["simple_residue"],
    )
    second_order_ratio = max(
        abs(row["second_order_coefficient"])
        / max(
            abs(row["simple_residue"])
            * max(abs(refined.imag), row["fit_radius"], 1.0e-9),
            1.0e-300,
        )
        for row in final_fits
    )
    contract_passes = (
        all(
            row["fit_mask_state_count"] == 1
            and row["all_fit_samples_mask_active"]
            and row["fit_orientation_count"] == 1
            and row["fit_label_count"] == 1
            and row["fit_role_count"] == 1
            and row["fit_relative_residual"]
            <= NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT
            for row in final_fits
        )
        and residue_change <= NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT
        and second_order_ratio
        <= NEAR_SUPPORT_SECOND_ORDER_SUPPRESSION_LIMIT
    )
    final_rows: list[dict[str, Any]] = []
    for fit in final_fits:
        final_rows.append(
            {
                "fit_row_type": "NEAR_SUPPORT_FINAL_SIMPLE_POLE_FIT",
                "pole_refinement_iteration": len(iteration_rows),
                "fit_scale": fit["fit_scale"],
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["fit_sample_count"],
                **complex_fields("refined_pole", refined),
                **complex_fields(
                    "geometric_to_refined_pole_shift",
                    refined - geometric,
                ),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields(
                    "simple_residue_R1",
                    fit["simple_residue"],
                ),
                "fit_relative_residual": fit["fit_relative_residual"],
                "fit_mask_state_count": fit["fit_mask_state_count"],
                "fit_mask_states": fit["fit_mask_states"],
                "all_fit_samples_mask_active": fit[
                    "all_fit_samples_mask_active"
                ],
                "fit_orientation_count": fit["fit_orientation_count"],
                "fit_label_count": fit["fit_label_count"],
                "fit_role_count": fit["fit_role_count"],
                "residue_fit_scale_relative_change": residue_change,
                "second_order_suppression_ratio": second_order_ratio,
                "near_support_simple_pole_fit_passes": contract_passes,
            }
        )
    selected = {
        "geometric_pole": geometric,
        "refined_pole": refined,
        "selected_residue": second["simple_residue"],
        "pole_side": near_support_pole_side(refined, lower, upper),
        "active_support_boundary": active_support_fit_geometry(
            refined,
            lower,
            upper,
        )[2],
        "active_support_direction": active_support_fit_geometry(
            refined,
            lower,
            upper,
        )[1],
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        "fit_relative_residual": max(
            row["fit_relative_residual"] for row in final_fits
        ),
        "residue_fit_scale_relative_change": residue_change,
        "second_order_suppression_ratio": second_order_ratio,
        "fit_contract_passes": contract_passes,
    }
    return selected, iteration_rows + final_rows


def near_support_masked_identity_audit(
    coordinate: float,
    term_id: str,
    selected: dict[str, Any],
    evaluate_unmasked: Any,
    evaluate_masked: Any,
) -> tuple[list[dict[str, Any]], bool]:
    lower = float(selected["support_energy_lower"])
    upper = float(selected["support_energy_upper"])
    pole = complex(selected["refined_pole"])
    boundary = (
        lower
        if selected["active_support_boundary"] == "LOWER"
        else upper
    )
    direction = int(selected["active_support_direction"])
    core = max(
        near_support_boundary_distance(pole, lower, upper),
        abs(pole.imag),
        1.0e-7,
    )
    specification = M5312.M5308.SURFACE_LOOKUP[term_id]
    rows: list[dict[str, Any]] = []
    for sample_index, scale in enumerate((0.5, 1.0, 2.0), start=1):
        energy = boundary + direction * scale * core
        energy = max(lower, min(upper, energy))
        unmasked = evaluate_unmasked(energy, coordinate)
        masked_value, active = evaluate_masked(
            M5312.EPSILON_ID,
            energy,
            coordinate,
            "MC04",
            int(specification["soft_sign"]),
            int(specification["decay_sign"]),
        )
        relative_change = M5312.relative_complex_change(
            complex(masked_value),
            complex(unmasked["value"]),
        )
        passed = bool(active) and (
            relative_change <= NEAR_SUPPORT_MASKED_IDENTITY_LIMIT
        )
        rows.append(
            {
                "sample_index": sample_index,
                "sample_scale": scale,
                "energy": energy,
                "masked_term_active": bool(active),
                **complex_fields("masked_value", complex(masked_value)),
                **complex_fields(
                    "unmasked_value",
                    complex(unmasked["value"]),
                ),
                "masked_unmasked_relative_change": relative_change,
                "selected_labels": unmasked["selected_labels"],
                "selected_role": unmasked["selected_role"],
                "identity_passes": passed,
            }
        )
    return rows, all(bool(row["identity_passes"]) for row in rows)


def build_near_support_augmentation(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
) -> dict[str, Any] | None:
    coordinate = float(node["absolute_soft_cosine"])
    panel_index = int(node["x_panel_index"])
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells)
    paths = M5312.shard_paths(str(node["node_id"]))
    if not paths["poles"].exists():
        return None
    existing_classifications = (
        read_csv(paths["classifications"])
        if paths["classifications"].exists()
        else []
    )
    unresolved_keys = {
        (row["term_id"], row["pole_id"])
        for row in existing_classifications
        if not parse_bool(row["pole_classification_resolved"])
    }
    candidates: list[dict[str, Any]] = []
    for row in read_csv(paths["poles"]):
        term_id = row["term_id"]
        if term_id not in supports:
            continue
        pole = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
        local: list[tuple[float, dict[str, Any], str]] = []
        for support in supports[term_id]:
            side = near_support_pole_side(
                pole,
                float(support["lower"]),
                float(support["upper"]),
            )
            local.append(
                (
                    near_support_boundary_distance(
                        pole,
                        float(support["lower"]),
                        float(support["upper"]),
                    ),
                    support,
                    side,
                )
            )
        if not local:
            continue
        distance, support, side = min(local, key=lambda value: value[0])
        core = max(abs(pole.imag), 1.0e-7)
        key = (term_id, row["pole_id"])
        candidate_mode = (
            "UNRESOLVED_IN_SUPPORT"
            if key in unresolved_keys and side == "INSIDE_SUPPORT"
            else "OUTSIDE_NEAR_SUPPORT"
        )
        if key in unresolved_keys or (
            not unresolved_keys
            and side != "INSIDE_SUPPORT"
            and distance / core <= NEAR_SUPPORT_DISTANCE_CORE_LIMIT
        ):
            candidates.append(
                {
                    **row,
                    "support_id": support["support_id"],
                    "support_energy_lower": support["lower"],
                    "support_energy_upper": support["upper"],
                    "support_contract_indices": "|".join(
                        str(value) for value in support["contracts"]
                    ),
                    "near_support_side": side,
                    "near_support_distance": distance,
                    "near_support_distance_in_core_units": distance / core,
                    "near_support_candidate_mode": candidate_mode,
                }
            )
    if len(candidates) != 1:
        return None
    candidate = candidates[0]
    term_id = candidate["term_id"]
    evaluate_unmasked = near_support_unmasked_evaluator(
        base_context,
        term_id,
    )
    selected, local_fit_rows = refine_near_support_simple_pole(
        coordinate,
        candidate,
        evaluate_unmasked,
    )
    identity_rows, identity_passes = near_support_masked_identity_audit(
        coordinate,
        term_id,
        selected,
        evaluate_unmasked,
        M5312.M5305.component_evaluator(base_context),
    )
    contract_passes = bool(selected["fit_contract_passes"]) and identity_passes
    fit_rows = [
        {
            "node_id": node["node_id"],
            "x_panel_index": panel_index,
            "absolute_soft_cosine": coordinate,
            "term_id": term_id,
            "support_id": candidate["support_id"],
            "pole_id": candidate["pole_id"],
            "primary_surface_id": candidate["primary_surface_id"],
            "near_support_side": candidate["near_support_side"],
            "near_support_distance": candidate["near_support_distance"],
            "near_support_distance_in_core_units": candidate[
                "near_support_distance_in_core_units"
            ],
            "near_support_candidate_mode": candidate[
                "near_support_candidate_mode"
            ],
            **row,
            "near_support_masked_identity_passes": identity_passes,
            "near_support_subtraction_contract_passes": contract_passes,
            **{field: False for field in CLAIM_FIELDS},
        }
        for row in local_fit_rows
    ]
    identity_rows = [
        {
            "node_id": node["node_id"],
            "x_panel_index": panel_index,
            "absolute_soft_cosine": coordinate,
            "term_id": term_id,
            "support_id": candidate["support_id"],
            "pole_id": candidate["pole_id"],
            "primary_surface_id": candidate["primary_surface_id"],
            **row,
            **{field: False for field in CLAIM_FIELDS},
        }
        for row in identity_rows
    ]
    refined = complex(selected["refined_pole"])
    residue = complex(selected["selected_residue"])
    classification = {
        "node_id": node["node_id"],
        "x_panel_index": panel_index,
        "outer_order": node["outer_order"],
        "absolute_soft_cosine": coordinate,
        "term_id": term_id,
        "support_id": candidate["support_id"],
        "pole_id": candidate["pole_id"],
        "primary_surface_id": candidate["primary_surface_id"],
        "pole_real": refined.real,
        "pole_imaginary": refined.imag,
        **complex_fields("geometric_pole", complex(
            float(candidate["pole_real"]),
            float(candidate["pole_imaginary"]),
        )),
        **complex_fields("selected_residue", residue),
        "maximum_fit_relative_residual": selected[
            "fit_relative_residual"
        ],
        "fit_residue_relative_change": selected[
            "residue_fit_scale_relative_change"
        ],
        "all_fit_samples_mask_active": contract_passes,
        "near_support_unmasked_fit_used": True,
        "near_support_candidate_mode": candidate[
            "near_support_candidate_mode"
        ],
        "near_support_side": selected["pole_side"],
        "near_support_distance": near_support_boundary_distance(
            refined,
            float(selected["support_energy_lower"]),
            float(selected["support_energy_upper"]),
        ),
        "near_support_masked_identity_passes": identity_passes,
        "material_simple_pole": contract_passes,
        "removable_zero_residue_pole": False,
        "pole_classification_resolved": contract_passes,
        "failure_reason": (
            "" if contract_passes else "NEAR_SUPPORT_SUBTRACTION_GATE_FAILED"
        ),
        "valid_for_pole_subtracted_outer_soft_node": contract_passes,
        **{field: False for field in CLAIM_FIELDS},
    }
    old_fit_rows = read_csv(NEAR_SUPPORT_FITS) if NEAR_SUPPORT_FITS.exists() else []
    old_fit_rows = [
        row for row in old_fit_rows if row["node_id"] != str(node["node_id"])
    ]
    write_csv(
        NEAR_SUPPORT_FITS,
        old_fit_rows + fit_rows,
        ["node_id", "fit_row_type", "fit_scale"],
    )
    old_identity_rows = (
        read_csv(NEAR_SUPPORT_IDENTITIES)
        if NEAR_SUPPORT_IDENTITIES.exists()
        else []
    )
    old_identity_rows = [
        row
        for row in old_identity_rows
        if row["node_id"] != str(node["node_id"])
    ]
    write_csv(
        NEAR_SUPPORT_IDENTITIES,
        old_identity_rows + identity_rows,
        ["node_id", "sample_index"],
    )
    return {
        "candidate": candidate,
        "selected": selected,
        "fit_rows": fit_rows,
        "identity_rows": identity_rows,
        "classification": classification,
        "contract_passes": contract_passes,
    }


def refined_energy_panel_rows(
    node: dict[str, Any],
    cell: dict[str, Any],
    supports: dict[str, list[dict[str, Any]]],
    classifications: list[dict[str, Any]],
    subdivisions: int,
) -> list[dict[str, Any]]:
    lower = float(cell["energy_lower"])
    upper = float(cell["energy_upper"])
    points = {lower, upper}
    points.update(
        lower + index * (upper - lower) / subdivisions
        for index in range(subdivisions + 1)
    )
    for term_id in cell["coefficients"]:
        support = M5312.support_for_cell_term(supports, term_id, cell)
        for row in classifications:
            if row["term_id"] != term_id or row["support_id"] != support["support_id"]:
                continue
            center = float(row["pole_real"])
            if not lower - 1.0e-12 <= center <= upper + 1.0e-12:
                continue
            core = max(abs(float(row["pole_imaginary"])), 1.0e-7)
            for scale in (0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
                points.add(max(lower, min(upper, center - scale * core)))
                points.add(max(lower, min(upper, center + scale * core)))
    coordinates = sorted(points)
    return [
        {
            "node_id": node["node_id"],
            "contract_index": cell["contract_index"],
            "energy_panel_index": panel_index,
            "energy_lower": left,
            "energy_upper": right,
            "panel_width": right - left,
        }
        for panel_index, (left, right) in enumerate(
            zip(coordinates[:-1], coordinates[1:]), start=1
        )
        if right - left > 1.0e-15
    ]


def record_energy_repair(row: dict[str, Any]) -> None:
    rows = read_csv(ENERGY_REPAIRS) if ENERGY_REPAIRS.exists() else []
    rows = [
        existing
        for existing in rows
        if not (
            existing["node_id"] == row["node_id"]
            and int(existing["energy_panel_subdivisions"])
            == int(row["energy_panel_subdivisions"])
        )
    ]
    rows.append(row)
    write_csv(
        ENERGY_REPAIRS,
        rows,
        ["node_id", "energy_panel_subdivisions"],
    )


def record_near_support_repair(row: dict[str, Any]) -> None:
    row = {
        "near_support_repair_revision": NEAR_SUPPORT_REPAIR_REVISION,
        **row,
    }
    rows = read_csv(NEAR_SUPPORT_REPAIRS) if NEAR_SUPPORT_REPAIRS.exists() else []
    rows = [
        existing
        for existing in rows
        if not (
            existing["node_id"] == row["node_id"]
            and (
                existing.get("near_support_repair_revision", "")
                != NEAR_SUPPORT_REPAIR_REVISION
                or int(existing["energy_panel_subdivisions"])
                == int(row["energy_panel_subdivisions"])
            )
        )
    ]
    rows.append(row)
    write_csv(
        NEAR_SUPPORT_REPAIRS,
        rows,
        ["node_id", "energy_panel_subdivisions"],
    )


def repair_node_near_support_subtraction(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    result: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    baseline_change = float(
        result.get(
            "pre_near_support_inner_Q4_Q8_relative_change",
            result["inner_Q4_Q8_relative_change"],
        )
    )
    baseline_budget = float(
        result.get(
            "pre_near_support_inner_energy_error_budget_relative",
            result["inner_energy_error_budget_relative"],
        )
    )
    try:
        augmentation = build_near_support_augmentation(
            node,
            contract,
            base_context,
        )
    except Exception as error:
        record_near_support_repair(
            {
                "node_id": node["node_id"],
                "x_panel_index": node["x_panel_index"],
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "energy_panel_subdivisions": 0,
                "near_support_candidate_found": True,
                "near_support_subtraction_contract_passes": False,
                "failure_reason": f"{type(error).__name__}: {error}",
                "repair_acceptance_passed": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        return result, True
    if augmentation is None:
        return result, False
    selected = augmentation["selected"]
    candidate = augmentation["candidate"]
    if not bool(augmentation["contract_passes"]):
        record_near_support_repair(
            {
                "node_id": node["node_id"],
                "x_panel_index": node["x_panel_index"],
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "energy_panel_subdivisions": 0,
                "near_support_candidate_found": True,
                "term_id": candidate["term_id"],
                "primary_surface_id": candidate["primary_surface_id"],
                "near_support_subtraction_contract_passes": False,
                "failure_reason": "NEAR_SUPPORT_SUBTRACTION_GATE_FAILED",
                "repair_acceptance_passed": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        return result, True
    old_fit_node_poles = M5312.fit_node_poles
    old_energy_panel_rows = M5312.energy_panel_rows
    classification = dict(augmentation["classification"])
    augmentation_fit_rows = list(augmentation["fit_rows"])

    def fit_node_poles_with_near_support(
        local_node: dict[str, Any],
        poles: list[dict[str, Any]],
        evaluate: Any,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        fits, classifications = old_fit_node_poles(local_node, poles, evaluate)
        if str(local_node["node_id"]) == str(node["node_id"]):
            replacement_key = (candidate["term_id"], candidate["pole_id"])
            fits = [
                row
                for row in fits
                if (row["term_id"], row["pole_id"]) != replacement_key
            ]
            classifications = [
                row
                for row in classifications
                if (row["term_id"], row["pole_id"]) != replacement_key
            ]
            fits.extend(augmentation_fit_rows)
            classifications.append(classification)
        return fits, classifications

    final = result
    try:
        M5312.fit_node_poles = fit_node_poles_with_near_support
        for subdivisions in (16, 32, 64):
            M5312.energy_panel_rows = (
                lambda local_node, cell, supports, classifications, count=subdivisions: refined_energy_panel_rows(
                    local_node,
                    cell,
                    supports,
                    classifications,
                    count,
                )
            )
            final = M5312.run_node(
                node,
                contract,
                expected_plan_sha256,
                base_context,
                multiplier,
            )
            integral_rows = read_csv(
                M5312.shard_paths(str(node["node_id"]))["integrals"]
            )
            q8_rows = [
                row for row in integral_rows if int(row["energy_order"]) == 8
            ]
            analytic_total = sum(
                (
                    complex(
                        float(row["analytic_pole_integral_real"]),
                        float(row["analytic_pole_integral_imaginary"]),
                    )
                    for row in q8_rows
                ),
                0.0j,
            )
            final["near_support_pole_subtraction_repair_applied"] = True
            final["near_support_energy_panel_subdivisions"] = subdivisions
            final["near_support_term_id"] = candidate["term_id"]
            final["near_support_primary_surface_id"] = candidate[
                "primary_surface_id"
            ]
            final["near_support_candidate_mode"] = candidate[
                "near_support_candidate_mode"
            ]
            final["near_support_pole_side"] = selected["pole_side"]
            final["near_support_distance"] = candidate[
                "near_support_distance"
            ]
            final["near_support_distance_in_core_units"] = candidate[
                "near_support_distance_in_core_units"
            ]
            final["near_support_fit_relative_residual"] = selected[
                "fit_relative_residual"
            ]
            final["near_support_residue_scale_relative_change"] = selected[
                "residue_fit_scale_relative_change"
            ]
            final["near_support_second_order_suppression_ratio"] = selected[
                "second_order_suppression_ratio"
            ]
            final["near_support_masked_identity_passes"] = all(
                bool(row["identity_passes"])
                for row in augmentation["identity_rows"]
            )
            final["pre_near_support_inner_Q4_Q8_relative_change"] = (
                baseline_change
            )
            final["pre_near_support_inner_energy_error_budget_relative"] = (
                baseline_budget
            )
            final.update(complex_fields("near_support_Q8_analytic_total", analytic_total))
            atomic_json(M5312.shard_paths(str(node["node_id"]))["result"], final)
            record_near_support_repair(
                {
                    "node_id": node["node_id"],
                    "x_panel_index": node["x_panel_index"],
                    "absolute_soft_cosine": node["absolute_soft_cosine"],
                    "energy_panel_subdivisions": subdivisions,
                    "near_support_candidate_found": True,
                    "term_id": candidate["term_id"],
                    "primary_surface_id": candidate["primary_surface_id"],
                    "near_support_candidate_mode": candidate[
                        "near_support_candidate_mode"
                    ],
                    "near_support_side": selected["pole_side"],
                    "near_support_distance": candidate[
                        "near_support_distance"
                    ],
                    "near_support_distance_in_core_units": candidate[
                        "near_support_distance_in_core_units"
                    ],
                    **complex_fields(
                        "refined_pole",
                        complex(selected["refined_pole"]),
                    ),
                    **complex_fields(
                        "selected_residue",
                        complex(selected["selected_residue"]),
                    ),
                    "fit_relative_residual": selected[
                        "fit_relative_residual"
                    ],
                    "residue_fit_scale_relative_change": selected[
                        "residue_fit_scale_relative_change"
                    ],
                    "second_order_suppression_ratio": selected[
                        "second_order_suppression_ratio"
                    ],
                    "near_support_masked_identity_passes": final[
                        "near_support_masked_identity_passes"
                    ],
                    "near_support_subtraction_contract_passes": True,
                    "pre_repair_inner_Q4_Q8_relative_change": baseline_change,
                    "post_repair_inner_Q4_Q8_relative_change": final[
                        "inner_Q4_Q8_relative_change"
                    ],
                    "pre_repair_inner_energy_error_budget_relative": baseline_budget,
                    "post_repair_inner_energy_error_budget_relative": final[
                        "inner_energy_error_budget_relative"
                    ],
                    **complex_fields("Q8_analytic_pole_integral", analytic_total),
                    "failure_reason": "",
                    "repair_acceptance_passed": final["acceptance_passed"],
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            if bool(final["acceptance_passed"]):
                break
    finally:
        M5312.energy_panel_rows = old_energy_panel_rows
        M5312.fit_node_poles = old_fit_node_poles
    return final, True


def repair_node_energy_resolution(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    result: dict[str, Any],
) -> dict[str, Any]:
    if bool(result["acceptance_passed"]):
        return result
    if int(result["inactive_selected_term_count"]) != 0:
        return result
    exact_result, exact_attempted = repair_node_near_support_subtraction(
        node,
        contract,
        expected_plan_sha256,
        base_context,
        multiplier,
        result,
    )
    if exact_attempted:
        return exact_result
    if int(result["unresolved_pole_count"]) != 0:
        return result
    baseline_change = float(result["inner_Q4_Q8_relative_change"])
    baseline_budget = float(result["inner_energy_error_budget_relative"])
    old_energy_panel_rows = M5312.energy_panel_rows
    final = result
    try:
        for subdivisions in (64, 128):
            M5312.energy_panel_rows = (
                lambda local_node, cell, supports, classifications, count=subdivisions: refined_energy_panel_rows(
                    local_node, cell, supports, classifications, count
                )
            )
            final = M5312.run_node(
                node,
                contract,
                expected_plan_sha256,
                base_context,
                multiplier,
            )
            final["targeted_energy_partition_repair_applied"] = True
            final["targeted_energy_panel_subdivisions"] = subdivisions
            final["pre_repair_inner_Q4_Q8_relative_change"] = baseline_change
            final["pre_repair_inner_energy_error_budget_relative"] = baseline_budget
            atomic_json(M5312.shard_paths(node["node_id"])["result"], final)
            record_energy_repair(
                {
                    "node_id": node["node_id"],
                    "x_panel_index": node["x_panel_index"],
                    "absolute_soft_cosine": node["absolute_soft_cosine"],
                    "energy_panel_subdivisions": subdivisions,
                    "pre_repair_inner_Q4_Q8_relative_change": baseline_change,
                    "post_repair_inner_Q4_Q8_relative_change": final[
                        "inner_Q4_Q8_relative_change"
                    ],
                    "pre_repair_inner_energy_error_budget_relative": baseline_budget,
                    "post_repair_inner_energy_error_budget_relative": final[
                        "inner_energy_error_budget_relative"
                    ],
                    "repair_acceptance_passed": final["acceptance_passed"],
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            if bool(final["acceptance_passed"]):
                break
    finally:
        M5312.energy_panel_rows = old_energy_panel_rows
    return final


def evaluate_panel(
    panel: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
    encountered: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    nodes = panel_nodes(panel)
    results: dict[str, dict[str, Any]] = {}
    for node in nodes:
        encountered[node["node_id"]] = node
        if not M5312.shard_is_complete(node, expected_plan_sha256):
            if time.perf_counter() - started >= runtime_limit_seconds:
                return None
            M5312.run_node(
                node, contract, expected_plan_sha256, base_context, multiplier
            )
        result = read_json(M5312.shard_paths(node["node_id"])["result"])
        result = repair_node_energy_resolution(
            node,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
            result,
        )
        results[node["node_id"]] = result
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "D2_EVENT_ALIGNED_Q4_Q8_ADAPTIVE_REFINEMENT",
                "last_completed_node_id": node["node_id"],
                "encountered_node_count": len(encountered),
            },
        )
    selected_energy_order = max(M5312.ENERGY_ORDERS)
    totals = {order: 0.0j for order in OUTER_ORDERS}
    inner_budgets = {order: 0.0 for order in OUTER_ORDERS}
    all_inner_pass = True
    jacobian_errors: list[float] = []
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    for order in OUTER_ORDERS:
        local_nodes = [row for row in nodes if int(row["outer_order"]) == order]
        weight_sum = sum(float(row["mapped_outer_weight"]) for row in local_nodes)
        jacobian_errors.append(
            abs(weight_sum - (upper - lower)) / max(upper - lower, 1.0e-300)
        )
        for node in local_nodes:
            result = results[node["node_id"]]
            value = complex(
                float(result[f"inner_energy_Q{selected_energy_order}_real"]),
                float(result[f"inner_energy_Q{selected_energy_order}_imaginary"]),
            )
            weight = float(node["mapped_outer_weight"])
            totals[order] += weight * value
            inner_budgets[order] += abs(weight) * float(
                result["inner_energy_error_budget_absolute"]
            )
            all_inner_pass = all_inner_pass and bool(result["acceptance_passed"])
    change = M5312.relative_complex_change(totals[4], totals[8])
    outer_error = abs(totals[8] - totals[4])
    return {
        "x_panel_index": int(panel["x_panel_index"]),
        "initial_segment_id": panel["initial_segment_id"],
        "adaptive_panel_id": panel["adaptive_panel_id"],
        "adaptive_depth": int(panel["adaptive_depth"]),
        "parent_adaptive_panel_id": panel["parent_adaptive_panel_id"],
        "lower_absolute_soft_cosine": lower,
        "upper_absolute_soft_cosine": upper,
        "segment_width": upper - lower,
        "transform_direction": int(panel["transform_direction"]),
        "event_coordinate": panel["event_coordinate"],
        "event_type": panel["event_type"],
        "all_inner_nodes_pass": all_inner_pass,
        **complex_fields("outer_Q4_inner_Q8", totals[4]),
        **complex_fields("outer_Q8_inner_Q8", totals[8]),
        "outer_Q4_Q8_absolute_change": outer_error,
        "outer_Q4_Q8_relative_change": change,
        "selected_inner_error_budget_absolute": inner_budgets[8],
        "maximum_jacobian_relative_error": max(jacobian_errors),
        "exact_change_of_variables_gate_passes": max(jacobian_errors) <= 5.0e-13,
        "adaptive_gate_passes": (
            all_inner_pass
            and max(jacobian_errors) <= 5.0e-13
            and change <= LOCAL_OUTER_CHANGE_LIMIT
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def refine_panels(
    initial: list[dict[str, Any]],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    bool,
]:
    all_rows: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []
    encountered: dict[str, dict[str, Any]] = {}
    paused = False

    def visit(panel: dict[str, Any]) -> None:
        nonlocal paused
        if paused:
            return
        result = evaluate_panel(
            panel,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
            encountered,
        )
        if result is None:
            paused = True
            return
        if bool(result["adaptive_gate_passes"]):
            result["adaptive_leaf"] = True
            result["failure_reason"] = ""
            all_rows.append(result)
            leaves.append(result)
            return
        if not bool(result["all_inner_nodes_pass"]):
            result["adaptive_leaf"] = True
            result["failure_reason"] = "INNER_NODE_FAILURE"
            all_rows.append(result)
            leaves.append(result)
            return
        if int(panel["adaptive_depth"]) >= MAXIMUM_ADAPTIVE_DEPTH:
            result["adaptive_leaf"] = True
            result["failure_reason"] = "MAXIMUM_ADAPTIVE_DEPTH"
            all_rows.append(result)
            leaves.append(result)
            return
        result["adaptive_leaf"] = False
        result["failure_reason"] = "REFINED_TO_CHILDREN"
        all_rows.append(result)
        left, right = split_panel(panel)
        visit(left)
        visit(right)

    for panel in initial:
        visit(dict(panel))
        if paused:
            break
    return all_rows, leaves, encountered, paused


def combined_shard_rows(
    encountered: dict[str, dict[str, Any]],
    expected_plan_sha256: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    manifest: list[dict[str, Any]] = []
    poles: list[dict[str, str]] = []
    fits: list[dict[str, str]] = []
    classifications: list[dict[str, str]] = []
    integrals: list[dict[str, str]] = []
    for node_id, node in encountered.items():
        complete = M5312.shard_is_complete(node, expected_plan_sha256)
        result = (
            read_json(M5312.shard_paths(node_id)["result"]) if complete else {}
        )
        manifest.append(
            {
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(result.get("acceptance_passed"))
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "node_acceptance_passed": bool(result.get("acceptance_passed", False)),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(M5312.shard_paths(node_id)["result"]),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        if not complete:
            continue
        paths = M5312.shard_paths(node_id)
        poles.extend(read_csv(paths["poles"]))
        fits.extend(read_csv(paths["fits"]))
        classifications.extend(read_csv(paths["classifications"]))
        integrals.extend(read_csv(paths["integrals"]))
    return manifest, poles, fits, classifications, integrals


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    started = time.perf_counter()
    old = configure_kernel()
    try:
        dry = load_validated_dry_run()
        if not dry["acceptance_passed"]:
            raise RuntimeError("5326 dry run did not pass")
        contract = read_csv(CONTRACT_5325)
        initial = [dict(row) for row in read_csv(INITIAL_PLAN)]
        expected = str(dry["node_plan_sha256"])
        base_context = M5312.M5303.synthetic_context()
        multiplier = M5312.M5309.physical_multiplier()
        panel_rows, leaves, encountered, paused = refine_panels(
            initial,
            contract,
            expected,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
        )
        manifest, poles, fits, classifications, integrals = combined_shard_rows(
            encountered, expected
        )
        write_csv(NODE_MANIFEST, manifest, ["x_panel_index", "node_id"])
        write_csv(
            ADAPTIVE_PANELS,
            panel_rows,
            ["x_panel_index", "initial_segment_id", "adaptive_panel_id"],
        )
        write_csv(OFF_AXIS_POLES, poles, ["x_panel_index", "node_id", "term_id", "pole_id"])
        write_csv(OFF_AXIS_FITS, fits, ["x_panel_index", "node_id", "term_id", "pole_id"])
        write_csv(
            OFF_AXIS_CLASSIFICATIONS,
            classifications,
            ["x_panel_index", "node_id", "term_id", "pole_id"],
        )
        write_csv(
            CELL_INTEGRALS,
            integrals,
            ["x_panel_index", "node_id", "contract_index", "energy_order"],
        )
        complete = not paused and len(leaves) >= len(initial)
        all_leaf_gates = complete and all(
            parse_bool(row["adaptive_gate_passes"]) for row in leaves
        )
        high = (
            sum(
                complex(
                    float(row["outer_Q8_inner_Q8_real"]),
                    float(row["outer_Q8_inner_Q8_imaginary"]),
                )
                for row in leaves
            )
            if complete
            else 0.0j
        )
        outer_error = (
            sum(float(row["outer_Q4_Q8_absolute_change"]) for row in leaves)
            if complete
            else math.inf
        )
        inner_error = (
            sum(float(row["selected_inner_error_budget_absolute"]) for row in leaves)
            if complete
            else math.inf
        )
        total_error = outer_error + inner_error
        relative_error = total_error / max(abs(high), 1.0e-12)
        accepted = (
            complete
            and all_leaf_gates
            and relative_error <= GLOBAL_ERROR_BUDGET_LIMIT
        )
        finite_rows = [
            {
                "decay_node_id": DECAY_NODE_ID,
                "epsilon_id": EPSILON_ID,
                "epsilon": EPSILON,
                "method": "FOUR_SUPPORT_EVENTS_SQUARED_Q4_Q8_ADAPTIVE",
                **complex_fields("fixed_decay_integral", high),
                "outer_error_absolute_conservative": outer_error,
                "inner_error_absolute_conservative": inner_error,
                "total_error_absolute_conservative": total_error,
                "total_error_relative_conservative": relative_error,
                "finite_regulator_fixed_decay_integral_accepted": accepted,
                **{
                    field: accepted
                    if field == "valid_for_D2_E0025_fixed_decay_integral"
                    else False
                    for field in CLAIM_FIELDS
                },
            }
        ]
        write_csv(FINITE_VALUE, finite_rows, ["decay_node_id", "epsilon_id"])
        parent = read_json(RESULT_5325)
        formal_end = M5283.formal_inventory_digest()
        if paused:
            decision = "D2_EVENT_ALIGNED_E0025_REFINEMENT_PAUSED__RESUME_SHARDS"
        elif accepted:
            decision = "D2_EVENT_ALIGNED_E0025_ACCEPTED__BUILD_D2_REGULATOR_LADDER"
        elif complete:
            decision = "D2_EVENT_ALIGNED_E0025_LOCALIZES_REMAINING_REFINEMENT"
        else:
            decision = "D2_EVENT_ALIGNED_E0025_INNER_FAILURES_LOCALIZED"
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "marker": MARKER,
            "revision": REVISION,
            "mode": "D2-midpoint-event-aligned-E0025-refinement",
            "acceptance_passed": accepted,
            "decision": decision,
            "completed_full_run": complete,
            "encountered_node_count": len(encountered),
            "completed_node_count": sum(
                row["shard_state"] != "PENDING" for row in manifest
            ),
            "failed_inner_node_count": sum(
                row["shard_state"] == "COMPLETE_FAIL" for row in manifest
            ),
            "adaptive_panel_count": len(panel_rows),
            "adaptive_leaf_count": len(leaves),
            "all_adaptive_leaf_gates_pass": all_leaf_gates,
            **complex_fields("fixed_decay_integral", high),
            "outer_error_absolute_conservative": outer_error,
            "inner_error_absolute_conservative": inner_error,
            "total_error_absolute_conservative": total_error,
            "total_error_relative_conservative": relative_error,
            "formalization_workbench_reference_digest": parent[
                "formalization_workbench_end_digest"
            ],
            "formalization_workbench_end_digest": formal_end,
            "formalization_workbench_modified_file_count": (
                0
                if formal_end == parent["formalization_workbench_end_digest"]
                else -1
            ),
            "claim_boundary": {
                "valid_for_D2_E0025_fixed_decay_integral": accepted,
                **{
                    field: False
                    for field in CLAIM_FIELDS
                    if field != "valid_for_D2_E0025_fixed_decay_integral"
                },
                "reason": (
                    "This is one event-aligned finite-regulator value at D2_MID. "
                    "The D2 epsilon-zero and decay-angle limits remain separate."
                ),
            },
            "source_files": source_rows(),
            "runtime_seconds": time.perf_counter() - started,
        }
        atomic_json(RESULT, result)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "PAUSED_RESUMABLE" if paused else "COMPLETE_DIAGNOSTIC",
                "decision": decision,
                "encountered_node_count": len(encountered),
                "completed_node_count": result["completed_node_count"],
            },
        )
        return result
    finally:
        restore_kernel(old)


def repair_failed_nodes() -> dict[str, Any]:
    started = time.perf_counter()
    old = configure_kernel()
    try:
        dry = load_validated_dry_run()
        contract = read_csv(CONTRACT_5325)
        expected = str(dry["node_plan_sha256"])
        base_context = M5312.M5303.synthetic_context()
        multiplier = M5312.M5309.physical_multiplier()
        manifest = read_csv(NODE_MANIFEST)
        failed = [row for row in manifest if row["shard_state"] == "COMPLETE_FAIL"]
        repaired: list[dict[str, Any]] = []
        for row in failed:
            node = dict(row)
            result = read_json(M5312.shard_paths(node["node_id"])["result"])
            final = repair_node_energy_resolution(
                node,
                contract,
                expected,
                base_context,
                multiplier,
                result,
            )
            repaired.append(final)
        accepted = bool(failed) and all(
            bool(row["acceptance_passed"]) for row in repaired
        )
        return {
            "checkpoint": CHECKPOINT,
            "mode": "targeted-energy-partition-repair",
            "acceptance_passed": accepted,
            "decision": (
                "D2_TARGETED_ENERGY_PARTITION_REPAIRS_ACCEPTED__RESUME_REFINEMENT"
                if accepted
                else "D2_TARGETED_ENERGY_PARTITION_REPAIRS_REQUIRE_MORE_RESOLUTION"
            ),
            "targeted_node_count": len(failed),
            "runtime_seconds": time.perf_counter() - started,
        }
    finally:
        restore_kernel(old)


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5326 - D2 midpoint event-aligned E0025 refinement",
        "",
        "## Method",
        "",
        "The complete 5325 pole census identifies seven support crossings in",
        "topology panels 1, 7, 8, and 10.  Their coordinates are solved from the",
        "signed pole-to-support margin.  Each crossing is integrated in squared",
        "event coordinates; all other regions use direct coordinates.  Q4/Q8",
        "outer comparison and recursive local refinement replace the coarse Q2/Q4",
        "smoke rule.  A pole lying just outside a moving support endpoint is",
        "subtracted with a one-sided Laurent fit evaluated entirely on the active",
        "support branch; scale stability, pole-order suppression, and masked versus",
        "unmasked identity are all required before its analytic logarithm is used.",
        "",
        "## Result",
        "",
        f"- completed full run: `{result['completed_full_run']}`;",
        f"- encountered nodes: `{result['encountered_node_count']}`;",
        f"- failed inner nodes: `{result['failed_inner_node_count']}`;",
        f"- adaptive leaves: `{result['adaptive_leaf_count']}`;",
        f"- fixed-decay value: `{result['fixed_decay_integral_real']:.12g}` "
        f"`{result['fixed_decay_integral_imaginary']:+.12g} i`;",
        f"- conservative relative error: "
        f"`{result['total_error_relative_conservative']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "A passing result closes only E0025 at D2_MID.  No epsilon-zero, angular",
        "endpoint, full phase-space, UV, local-GR, or full-MTS claim follows.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    old = configure_kernel()
    try:
        result = read_json(RESULT)
        dry = read_json(DRY_RUN)
        events = read_csv(EVENTS)
        manifest = read_csv(NODE_MANIFEST)
        panels = read_csv(ADAPTIVE_PANELS)
        finite = read_csv(FINITE_VALUE)
        leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
        source_current = all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in result["source_files"]
        )
        broad_claims = [
            field
            for field in CLAIM_FIELDS
            if field != "valid_for_D2_E0025_fixed_decay_integral"
        ]
        gates = [
            validation_gate(
                "seven_support_events_resolved",
                bool(dry["acceptance_passed"])
                and len(events) == EXPECTED_EVENT_COUNT
                and all(parse_bool(row["event_contract_passes"]) for row in events),
                f"events={len(events)}",
            ),
            validation_gate(
                "all_encountered_nodes_pass",
                bool(manifest)
                and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
                and int(result["failed_inner_node_count"]) == 0,
                f"nodes={len(manifest)}",
            ),
            validation_gate(
                "all_adaptive_leaves_pass",
                bool(leaves)
                and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
                and bool(result["all_adaptive_leaf_gates_pass"]),
                f"leaves={len(leaves)}",
            ),
            validation_gate(
                "D2_E0025_conservative_budget_passes",
                len(finite) == 1
                and parse_bool(
                    finite[0]["finite_regulator_fixed_decay_integral_accepted"]
                )
                and float(finite[0]["total_error_relative_conservative"])
                <= GLOBAL_ERROR_BUDGET_LIMIT
                and bool(result["acceptance_passed"]),
                str(result["total_error_relative_conservative"]),
            ),
            validation_gate(
                "formal_workbench_unchanged",
                M5283.formal_inventory_digest()
                == result["formalization_workbench_end_digest"]
                == result["formalization_workbench_reference_digest"]
                and int(result["formalization_workbench_modified_file_count"]) == 0,
                result["formalization_workbench_end_digest"],
            ),
            validation_gate(
                "source_paths_and_hashes_current",
                source_current,
                f"rows={len(result['source_files'])}",
            ),
            validation_gate(
                "scripts_cache_absent",
                not (SCRIPTS / "__pycache__").exists(),
                str(SCRIPTS / "__pycache__"),
            ),
            validation_gate(
                "broader_claims_locked_false",
                all(not bool(result["claim_boundary"][field]) for field in broad_claims),
                "D2 epsilon-zero and angular claims remain false",
            ),
        ]
        passed = all(bool(row["passed"]) for row in gates)
        write_csv(VALIDATION, gates, ["gate"])
        write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
        render_document(result, passed)
        return {
            "checkpoint": CHECKPOINT,
            "mode": "validation",
            "acceptance_passed": passed,
            "decision": (
                "VALIDATED_D2_MIDPOINT_EVENT_ALIGNED_E0025_REFINEMENT"
                if passed
                else "D2_MIDPOINT_EVENT_ALIGNED_E0025_REFINEMENT_VALIDATION_FAILED"
            ),
            "runtime_seconds": time.perf_counter() - started,
        }
    finally:
        restore_kernel(old)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "repair-nodes", "run", "validate"),
        required=True,
    )
    parser.add_argument(
        "--max-runtime-hours",
        type=float,
        default=DEFAULT_RUNTIME_LIMIT_SECONDS / 3600.0,
    )
    return parser.parse_args()


def main() -> int:
    M5312.set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "repair-nodes":
        result = repair_failed_nodes()
    elif arguments.mode == "run":
        result = execute(arguments.max_runtime_hours * 3600.0)
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
