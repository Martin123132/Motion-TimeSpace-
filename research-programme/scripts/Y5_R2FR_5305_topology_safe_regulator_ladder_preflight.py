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
SOURCE = FUNCTIONAL_RG / "5305"

SCRIPT_5304 = SCRIPTS / "Y5_R2FR_5304_moving_mask_edge_energy_map.py"
RESULT_5304 = FUNCTIONAL_RG / "5304" / "moving_mask_edge_energy_map_result.json"
VALIDATION_5304 = FUNCTIONAL_RG / "5304" / "moving_mask_edge_energy_map_validation.csv"

DRY_RUN = SOURCE / "topology_safe_regulator_ladder_preflight_dry_run.json"
NODES = SOURCE / "selected_topology_safe_energy_nodes.csv"
MASK_AUDIT = SOURCE / "selected_node_mask_support_audit.csv"
SYMMETRY = SOURCE / "selected_node_sign_orbit_symmetry_audit.csv"
PEAK_SCAN = SOURCE / "selected_node_E0025_peak_scan.csv"
PEAKS = SOURCE / "selected_node_E0025_peak_locations.csv"
PANELS = SOURCE / "selected_node_boundary_aligned_panel_plan.csv"
RESULT = SOURCE / "topology_safe_regulator_ladder_preflight_result.json"
VALIDATION = SOURCE / "topology_safe_regulator_ladder_preflight_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5305_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5305-Y5-R2FR-topology-safe-regulator-ladder-preflight.md"

CHECKPOINT = 5305
PARENT_CHECKPOINT = 5304
MARKER = "MTS_5305_TOPOLOGY_SAFE_REGULATOR_LADDER_PREFLIGHT"
REVISION = "topology-safe-regulator-ladder-preflight-v1"
SYMMETRY_EPSILON_IDS = ("E020", "E005")
SYMMETRY_FRACTIONS = (0.05, 0.25, 0.5, 0.75, 0.95)
MASK_FRACTIONS = (0.01, 0.25, 0.5, 0.75, 0.99)
SYMMETRY_RELATIVE_ERROR_LIMIT = 1.0e-9
MAXIMUM_COARSE_PANEL_WIDTH = 2.0e-2
MAXIMUM_PEAK_CORE_PANEL_WIDTH = 2.01e-6
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


M5304 = load_module("mts_5304_for_5305", SCRIPT_5304)
M5303 = M5304.M5303
M5302 = M5304.M5302
M5301 = M5303.M5301
M5280 = M5304.M5280
M5283 = M5304.M5283
np = M5304.np
mp = M5304.mp


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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(second), abs(first), 1.0e-300)


def cancellation_surface_value(energy: float, coordinate: float) -> float:
    return float(
        M5304.M5272.hard_boundary_value(
            math.sqrt(1.0 - energy),
            -coordinate,
            M5302.EDGE_DECAY_ABSOLUTE,
            -1,
            -0.3,
            math.pi,
        )
    )


def cancellation_onset_energy() -> float:
    coefficients = M5304.M5272.hard_boundary_coefficients(
        -M5304.angular_limit(),
        M5302.EDGE_DECAY_ABSOLUTE,
        -1,
        -0.3,
        math.pi,
    )
    roots = [
        float(root)
        for root in M5304.M5272.quadratic_real_roots(*coefficients)
        if 0.0 <= root <= 1.0
    ]
    if len(roots) != 1:
        raise RuntimeError(f"expected one cancellation-onset q root: {roots}")
    return 1.0 - roots[0] ** 2


def cancellation_coordinate(energy: float) -> float | None:
    if energy < cancellation_onset_energy() - 2.0e-14:
        return None
    lower = 0.0
    upper = M5304.angular_limit()
    lower_value = cancellation_surface_value(energy, lower)
    upper_value = cancellation_surface_value(energy, upper)
    if abs(upper_value) <= 1.0e-13:
        return upper
    if lower_value * upper_value >= 0.0:
        raise RuntimeError(
            f"cancellation boundary not bracketed at E={energy}: "
            f"{lower_value}, {upper_value}"
        )
    for _ in range(100):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = cancellation_surface_value(energy, midpoint)
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_value = midpoint_value
    return 0.5 * (lower + upper)


def selected_nodes() -> list[dict[str, Any]]:
    result = read_json(RESULT_5304)
    fold_energy = float(result["moving_edge_fold_energy"])
    cutoff_energy = float(result["moving_edge_angular_cutoff_energy"])
    witness_energy = float(M5302.EDGE_ENERGY)
    upper_energy = float(result["moving_edge_upper_energy"])
    fold_coordinate = float(result["moving_edge_fold_absolute_soft_cosine"])
    specifications = (
        (
            "N01_TWO_BRANCH_MID",
            0.5 * (fold_energy + cutoff_energy),
            "TWO_BRANCH",
        ),
        ("N02_ANGULAR_CUTOFF", cutoff_energy, "CUTOFF_EVENT"),
        ("N03_5302_WITNESS", witness_energy, "INNER_ONLY"),
        (
            "N04_INNER_HIGH_MID",
            0.5 * (witness_energy + upper_energy),
            "INNER_ONLY",
        ),
    )
    rows: list[dict[str, Any]] = []
    for node_id, energy, region in specifications:
        inner = M5304.inverse_coordinate_on_branch(
            energy, "INNER", fold_coordinate
        )
        activation_outer = (
            M5304.inverse_coordinate_on_branch(
                energy, "OUTER", fold_coordinate
            )
            if energy <= cutoff_energy + 2.0e-14
                else M5304.angular_limit()
        )
        cancellation = cancellation_coordinate(energy)
        outer = (
            min(activation_outer, cancellation)
            if cancellation is not None
            else activation_outer
        )
        rows.append(
            {
                "energy_node_id": node_id,
                "topology_region": region,
                "soft_energy": energy,
                "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
                "inner_boundary_absolute_soft_cosine": inner,
                "outer_boundary_absolute_soft_cosine": outer,
                "activation_outer_boundary_absolute_soft_cosine": (
                    activation_outer
                ),
                "cancellation_boundary_absolute_soft_cosine": (
                    cancellation if cancellation is not None else ""
                ),
                "cancellation_onset_soft_energy": cancellation_onset_energy(),
                "active_support_width": outer - inner,
                "outer_boundary_type": (
                    "EXACT_G2_CANCELLATION_EDGE"
                    if cancellation is not None
                    else (
                        "EXACT_G1_OUTER_EDGE"
                        if energy < cutoff_energy - 2.0e-14
                        else (
                            "EXACT_G1_EDGE_AT_ANGULAR_CUTOFF"
                            if energy <= cutoff_energy + 2.0e-14
                            else "ANGULAR_DOMAIN_LIMIT"
                        )
                    )
                ),
                "valid_for_topology_safe_ladder_node": (
                    0.0 <= inner < outer <= M5304.angular_limit()
                    and abs(M5304.surface_value(energy, inner)) <= 1.0e-12
                    and (
                        cancellation is None
                        or abs(cancellation_surface_value(energy, outer))
                        <= 1.0e-12
                    )
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def component_evaluator(base_context: dict[str, Any]) -> Any:
    cache: dict[tuple[str, float, float, str, int, int], tuple[complex, bool]] = {}

    def evaluate(
        epsilon_id: str,
        energy: float,
        absolute_soft_cosine: float,
        component_id: str,
        soft_sign: int,
        decay_sign: int,
    ) -> tuple[complex, bool]:
        key = (
            epsilon_id,
            float(energy),
            float(absolute_soft_cosine),
            component_id,
            soft_sign,
            decay_sign,
        )
        if key in cache:
            return cache[key]
        context = M5302.local_context(
            base_context,
            absolute_soft_cosine,
            soft_sign,
            decay_sign,
        )
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        target = context["inventories"][epsilon_id]["target"]
        rationals = M5280.M5274.M5231.root_rationals(event, target)
        evaluation = M5280.evaluate_component(
            event,
            epsilon_id,
            component_id,
            context,
            rationals=rationals,
            convergence_audit=False,
        )
        value = complex(evaluation["residue"])
        active = bool(evaluation["mask_active"])
        cache[key] = (value, active)
        return cache[key]

    return evaluate


def edge_component(
    evaluate: Any,
    epsilon_id: str,
    energy: float,
    coordinate: float,
) -> tuple[complex, bool]:
    return evaluate(
        epsilon_id,
        energy,
        coordinate,
        M5302.EDGE_COMPONENT,
        M5302.EDGE_SOFT_SIGN,
        M5302.EDGE_DECAY_SIGN,
    )


def pair_orbit(
    evaluate: Any,
    epsilon_id: str,
    energy: float,
    coordinate: float,
) -> complex:
    return sum(
        (
            evaluate(
                epsilon_id,
                energy,
                coordinate,
                component_id,
                soft_sign,
                decay_sign,
            )[0]
            for soft_sign in (-1, 1)
            for decay_sign in (-1, 1)
            for component_id in M5302.PAIR_COMPONENTS
        ),
        0.0j,
    )


def mask_audit_rows(nodes: list[dict[str, Any]], evaluate: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in nodes:
        energy = float(node["soft_energy"])
        lower = float(node["inner_boundary_absolute_soft_cosine"])
        upper = float(node["outer_boundary_absolute_soft_cosine"])
        width = upper - lower
        probes: list[tuple[str, float, bool]] = []
        outside_step = min(1.0e-5, 0.01 * width)
        if lower > 0.0:
            probes.append(("BELOW_INNER", max(0.0, lower - outside_step), False))
        for fraction in MASK_FRACTIONS:
            probes.append(
                (f"INSIDE_{fraction:.2f}", lower + fraction * width, True)
            )
        if upper < M5304.angular_limit():
            probes.append(
                (
                    "ABOVE_OUTER",
                    min(M5304.angular_limit(), upper + outside_step),
                    False,
                )
            )
        for probe_id, coordinate, expected in probes:
            edge, active = edge_component(
                evaluate, "E020", energy, coordinate
            )
            orbit = pair_orbit(evaluate, "E020", energy, coordinate)
            if expected:
                support_error = relative_complex_change(edge, orbit)
                matches = (
                    active
                    and support_error <= SYMMETRY_RELATIVE_ERROR_LIMIT
                )
            else:
                support_error = abs(orbit) / max(abs(edge), 1.0)
                matches = support_error <= SYMMETRY_RELATIVE_ERROR_LIMIT
            rows.append(
                {
                    "energy_node_id": node["energy_node_id"],
                    "probe_id": probe_id,
                    "soft_energy": energy,
                    "absolute_soft_cosine": coordinate,
                    "expected_net_orbit_support_active": expected,
                    "observed_edge_mask_active": active,
                    **complex_fields("edge_component", edge),
                    **complex_fields("pair_sign_orbit", orbit),
                    "net_orbit_support_relative_error": support_error,
                    "net_orbit_state_matches_exact_support": matches,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def symmetry_rows(nodes: list[dict[str, Any]], evaluate: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in nodes:
        energy = float(node["soft_energy"])
        lower = float(node["inner_boundary_absolute_soft_cosine"])
        upper = float(node["outer_boundary_absolute_soft_cosine"])
        for epsilon_id in SYMMETRY_EPSILON_IDS:
            for fraction in SYMMETRY_FRACTIONS:
                coordinate = lower + fraction * (upper - lower)
                edge, active = edge_component(
                    evaluate, epsilon_id, energy, coordinate
                )
                orbit = pair_orbit(
                    evaluate, epsilon_id, energy, coordinate
                )
                change = relative_complex_change(edge, orbit)
                rows.append(
                    {
                        "energy_node_id": node["energy_node_id"],
                        "epsilon_id": epsilon_id,
                        "support_fraction": fraction,
                        "soft_energy": energy,
                        "absolute_soft_cosine": coordinate,
                        "edge_component_mask_active": active,
                        **complex_fields("edge_component", edge),
                        **complex_fields("pair_sign_orbit", orbit),
                        "symmetry_relative_error": change,
                        "valid_for_single_component_orbit_reduction": (
                            active
                            and change <= SYMMETRY_RELATIVE_ERROR_LIMIT
                        ),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def unique_coordinates(values: list[float], lower: float, upper: float) -> list[float]:
    clipped = sorted(max(lower, min(upper, value)) for value in values)
    unique: list[float] = []
    for value in clipped:
        if not unique or abs(value - unique[-1]) > 2.0e-13:
            unique.append(value)
    return unique


def initial_peak_coordinates(lower: float, upper: float) -> list[float]:
    width = upper - lower
    values = [lower + fraction * width for fraction in np.linspace(0.001, 0.999, 25)]
    maximum_offset = min(0.03, 0.999 * width)
    if maximum_offset > 1.0e-7:
        values.extend(
            lower + float(offset)
            for offset in np.geomspace(1.0e-7, maximum_offset, 36)
        )
    local_maximum = min(0.02, 0.999 * width)
    values.extend(
        lower + float(offset)
        for offset in np.linspace(1.0e-7, local_maximum, 101)
    )
    return unique_coordinates(values, lower + 1.0e-9 * width, upper - 1.0e-9 * width)


def peak_scan_rows(
    nodes: list[dict[str, Any]],
    evaluate: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    peaks: list[dict[str, Any]] = []
    for node in nodes:
        node_id = str(node["energy_node_id"])
        energy = float(node["soft_energy"])
        lower = float(node["inner_boundary_absolute_soft_cosine"])
        upper = float(node["outer_boundary_absolute_soft_cosine"])
        width = upper - lower
        stage_coordinates = initial_peak_coordinates(lower, upper)
        evaluated: dict[float, tuple[complex, bool, str]] = {}
        for stage in ("COARSE", "REFINE_1", "REFINE_2"):
            for coordinate in stage_coordinates:
                if coordinate in evaluated:
                    continue
                value, active = edge_component(
                    evaluate, "E0025", energy, coordinate
                )
                evaluated[coordinate] = (value, active, stage)
            active_items = [
                (coordinate, value)
                for coordinate, (value, active, _) in evaluated.items()
                if active
            ]
            peak_coordinate, peak_value = max(
                active_items, key=lambda item: abs(item[1])
            )
            if stage == "COARSE":
                span = min(4.0e-4, 0.05 * width)
            else:
                span = min(4.0e-5, 0.005 * width)
            stage_coordinates = unique_coordinates(
                [
                    peak_coordinate + float(offset)
                    for offset in np.linspace(-span, span, 81)
                ],
                lower + 1.0e-9 * width,
                upper - 1.0e-9 * width,
            )
        for coordinate, (value, active, stage) in sorted(evaluated.items()):
            rows.append(
                {
                    "energy_node_id": node_id,
                    "scan_stage": stage,
                    "soft_energy": energy,
                    "absolute_soft_cosine": coordinate,
                    "offset_from_inner_boundary": coordinate - lower,
                    "edge_mask_active": active,
                    **complex_fields("E0025_edge_component", value),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        active_rows = [
            row
            for row in rows
            if row["energy_node_id"] == node_id and row["edge_mask_active"]
        ]
        peak = max(
            active_rows,
            key=lambda row: float(row["E0025_edge_component_magnitude"]),
        )
        peaks.append(
            {
                "energy_node_id": node_id,
                "soft_energy": energy,
                "inner_boundary_absolute_soft_cosine": lower,
                "outer_boundary_absolute_soft_cosine": upper,
                "peak_absolute_soft_cosine": float(peak["absolute_soft_cosine"]),
                "peak_offset_from_inner_boundary": float(
                    peak["offset_from_inner_boundary"]
                ),
                "peak_magnitude": float(peak["E0025_edge_component_magnitude"]),
                "peak_scan_row_count": len(active_rows),
                "valid_for_boundary_aligned_peak_localization": (
                    lower < float(peak["absolute_soft_cosine"]) < upper
                    and math.isfinite(
                        float(peak["E0025_edge_component_magnitude"])
                    )
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "PEAK_SCAN",
                "last_completed_energy_node_id": node_id,
                "completed_peak_count": len(peaks),
                "planned_peak_count": len(nodes),
            },
        )
    return rows, peaks


def panel_rows(
    nodes: list[dict[str, Any]],
    peaks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    peak_lookup = {row["energy_node_id"]: row for row in peaks}
    rows: list[dict[str, Any]] = []
    for node in nodes:
        node_id = str(node["energy_node_id"])
        lower = float(node["inner_boundary_absolute_soft_cosine"])
        upper = float(node["outer_boundary_absolute_soft_cosine"])
        width = upper - lower
        peak = float(peak_lookup[node_id]["peak_absolute_soft_cosine"])
        values = [lower, upper]
        values.extend(
            lower + fraction * width for fraction in np.linspace(0.0, 1.0, 65)
        )
        values.extend(
            lower + offset
            for offset in M5303.panel_offsets()
            if 0.0 <= offset <= width
        )
        values.extend(
            peak + offset
            for offset in np.arange(-1.0e-3, 1.0e-3 + 0.5e-5, 1.0e-5)
        )
        values.extend(
            peak + offset
            for offset in np.arange(-1.0e-4, 1.0e-4 + 1.0e-6, 2.0e-6)
        )
        coordinates = unique_coordinates(values, lower, upper)
        for panel_index, (left, right) in enumerate(
            zip(coordinates[:-1], coordinates[1:]), start=1
        ):
            intersects_peak_core = (
                left >= peak - 1.0001e-4 and right <= peak + 1.0001e-4
            )
            rows.append(
                {
                    "energy_node_id": node_id,
                    "panel_index": panel_index,
                    "left_absolute_soft_cosine": left,
                    "right_absolute_soft_cosine": right,
                    "panel_width": right - left,
                    "intersects_peak_core": intersects_peak_core,
                    "valid_for_boundary_aligned_panel_plan": (
                        lower <= left < right <= upper
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5304,
        RESULT_5304,
        VALIDATION_5304,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5304)
    nodes = selected_nodes()
    checks = {
        "parent_5304_accepted": bool(parent["acceptance_passed"]),
        "parent_5304_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5304)
        ),
        "parent_requests_topology_safe_ladders": (
            parent["decision"]
            == (
                "MOVING_EDGE_FOLD_AND_TWO_BRANCH_TOPOLOGY_DERIVED__"
                "SELECT_TOPOLOGY_SAFE_REGULATOR_LADDERS"
            )
        ),
        "four_topology_safe_nodes_selected": (
            len(nodes) == 4
            and all(
                bool(row["valid_for_topology_safe_ladder_node"])
                for row in nodes
            )
        ),
        "selection_spans_two_branch_cutoff_and_inner_regions": (
            {row["topology_region"] for row in nodes}
            == {"TWO_BRANCH", "CUTOFF_EVENT", "INNER_ONLY"}
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
        "selected_energy_node_count": len(nodes),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_TOPOLOGY_SAFE_LADDER_PREFLIGHT"
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
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5305 dry run did not pass")
    parent = read_json(RESULT_5304)
    nodes = selected_nodes()
    context = M5303.synthetic_context()
    evaluate = component_evaluator(context)
    mask_rows = mask_audit_rows(nodes, evaluate)
    symmetry = symmetry_rows(nodes, evaluate)
    scans, peaks = peak_scan_rows(nodes, evaluate)
    panels = panel_rows(nodes, peaks)
    write_csv(NODES, nodes)
    write_csv(MASK_AUDIT, mask_rows)
    write_csv(SYMMETRY, symmetry)
    write_csv(PEAK_SCAN, scans)
    write_csv(PEAKS, peaks)
    write_csv(PANELS, panels)
    maximum_symmetry_error = max(
        float(row["symmetry_relative_error"]) for row in symmetry
    )
    maximum_panel_width = max(float(row["panel_width"]) for row in panels)
    maximum_peak_core_panel_width = max(
        float(row["panel_width"])
        for row in panels
        if parse_bool(row["intersects_peak_core"])
    )
    node_panel_counts = {
        str(node["energy_node_id"]): sum(
            row["energy_node_id"] == node["energy_node_id"] for row in panels
        )
        for node in nodes
    }
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "exact_net_orbit_support_resolved": all(
            bool(row["net_orbit_state_matches_exact_support"])
            for row in mask_rows
        ),
        "single_component_sign_orbit_reduction_holds": (
            maximum_symmetry_error <= SYMMETRY_RELATIVE_ERROR_LIMIT
            and all(
                bool(row["valid_for_single_component_orbit_reduction"])
                for row in symmetry
            )
        ),
        "all_E0025_peaks_localized": all(
            bool(row["valid_for_boundary_aligned_peak_localization"])
            for row in peaks
        ),
        "all_panel_plans_cover_exact_support": all(
            bool(row["valid_for_boundary_aligned_panel_plan"])
            for row in panels
        ),
        "coarse_panels_bounded": (
            maximum_panel_width <= MAXIMUM_COARSE_PANEL_WIDTH
        ),
        "peak_core_panels_ultrafine": (
            maximum_peak_core_panel_width
            <= MAXIMUM_PEAK_CORE_PANEL_WIDTH
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
        "TOPOLOGY_SAFE_NODES_SYMMETRY_AND_PEAK_PANELS_RESOLVED__"
        "RUN_FIVE_REGULATOR_LADDERS"
        if accepted
        else "TOPOLOGY_SAFE_LADDER_PREFLIGHT_REQUIRES_REPAIR"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "topology-safe-regulator-ladder-preflight",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "selected_energy_node_count": len(nodes),
        "mask_support_audit_row_count": len(mask_rows),
        "symmetry_audit_row_count": len(symmetry),
        "peak_scan_row_count": len(scans),
        "panel_plan_row_count": len(panels),
        "node_panel_counts": node_panel_counts,
        "maximum_sign_orbit_symmetry_relative_error": maximum_symmetry_error,
        "maximum_panel_width": maximum_panel_width,
        "maximum_peak_core_panel_width": maximum_peak_core_panel_width,
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
            "valid_for_topology_safe_energy_node_selection": accepted,
            "valid_for_single_component_orbit_reduction_at_selected_nodes": accepted,
            "valid_for_boundary_aligned_panel_plan": accepted,
            "valid_for_five_regulator_selected_node_integrals": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The selected-node activation/cancellation support, orbit "
                "reduction, E0025 peaks, "
                "and panel plans are preflight results. No finite-regulator "
                "or regulator-zero selected-node integrals have yet run."
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
            "selected_energy_node_count": len(nodes),
            "node_panel_counts": node_panel_counts,
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5305 — Topology-safe regulator-ladder preflight

## Result

Four fixed-decay energy nodes now cover the narrow two-branch region, the
angular-cutoff event, the validated 5302 witness, and the upper INNER branch.
The lower `g1` activation edge and the later `g2` cancellation edge were
checked directly against the transported `MC04+MC12` sign orbit. Above the
`g2` edge the newly active `MC12(-,+)` term cancels `MC04(-,-)` exactly.

The full `MC04+MC12` four-sign orbit reproduces the single `MC04(-,-)` edge
component at the selected support probes with maximum relative error
`{result['maximum_sign_orbit_symmetry_relative_error']:.12g}`. This licenses
the cheaper one-component integrand for the next selected-node ladders only.

- selected energy nodes: `{result['selected_energy_node_count']}`;
- mask probes: `{result['mask_support_audit_row_count']}`;
- sign-orbit probes: `{result['symmetry_audit_row_count']}`;
- E0025 peak-scan rows: `{result['peak_scan_row_count']}`;
- planned angular panels: `{result['panel_plan_row_count']}`;
- widest panel: `{result['maximum_panel_width']:.12g}`;
- widest peak-core panel: `{result['maximum_peak_core_panel_width']:.12g}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This is a topology, symmetry, peak-localization, and panel-construction
preflight. It is not a finite-regulator integral, regulator-zero result,
energy-angle cubature, phase-space coefficient, local-GR result, or full-MTS
claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    nodes = read_csv(NODES)
    masks = read_csv(MASK_AUDIT)
    symmetry = read_csv(SYMMETRY)
    peaks = read_csv(PEAKS)
    panels = read_csv(PANELS)
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "four_selected_nodes_complete",
            len(nodes) == 4
            and all(
                parse_bool(row["valid_for_topology_safe_ladder_node"])
                for row in nodes
            ),
            f"rows={len(nodes)}",
        ),
        validation_gate(
            "net_orbit_support_audit_passes",
            len(masks) >= 20
            and all(
                parse_bool(row["net_orbit_state_matches_exact_support"])
                for row in masks
            ),
            f"rows={len(masks)}",
        ),
        validation_gate(
            "sign_orbit_reduction_passes",
            len(symmetry)
            == len(nodes) * len(SYMMETRY_EPSILON_IDS) * len(SYMMETRY_FRACTIONS)
            and all(
                parse_bool(row["valid_for_single_component_orbit_reduction"])
                for row in symmetry
            ),
            f"rows={len(symmetry)}",
        ),
        validation_gate(
            "all_peaks_and_panel_plans_complete",
            len(peaks) == len(nodes)
            and len(panels) == int(result["panel_plan_row_count"])
            and all(
                parse_bool(row["valid_for_boundary_aligned_panel_plan"])
                for row in panels
            ),
            f"peaks={len(peaks)}; panels={len(panels)}",
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
            "no angular, phase-space, UV, local-GR, or full-MTS claim",
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
            "VALIDATED_TOPOLOGY_SAFE_REGULATOR_LADDER_PREFLIGHT"
            if passed
            else "TOPOLOGY_SAFE_REGULATOR_LADDER_PREFLIGHT_VALIDATION_FAILED"
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
