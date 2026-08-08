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
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5308"

SCRIPT_5307 = (
    SCRIPTS / "Y5_R2FR_5307_N04_secondary_peak_adaptive_refinement.py"
)
RESULT_5307 = (
    FUNCTIONAL_RG / "5307" / "N04_secondary_peak_refinement_result.json"
)
VALIDATION_5307 = (
    FUNCTIONAL_RG / "5307" / "N04_secondary_peak_refinement_validation.csv"
)

DRY_RUN = SOURCE / "full_fixed_decay_pair_topology_dry_run.json"
BRANCH_SCAN = SOURCE / "full_fixed_decay_pair_surface_branch_scan.csv"
EVENTS = SOURCE / "full_fixed_decay_pair_topology_events.csv"
X_PANELS = SOURCE / "full_fixed_decay_pair_x_panels.csv"
CHAMBERS = SOURCE / "full_fixed_decay_pair_energy_chambers.csv"
REDUCTION = SOURCE / "full_fixed_decay_pair_orbit_reduction_audit.csv"
CONTRACT = SOURCE / "fixed_decay_energy_soft_cubature_contract.csv"
RESULT = SOURCE / "full_fixed_decay_pair_topology_result.json"
VALIDATION = SOURCE / "full_fixed_decay_pair_topology_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5308_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5308-Y5-R2FR-full-fixed-decay-pair-orbit-topology.md"

CHECKPOINT = 5308
PARENT_CHECKPOINT = 5307
MARKER = "MTS_5308_FULL_FIXED_DECAY_PAIR_ORBIT_TOPOLOGY"
REVISION = "full-fixed-decay-pair-orbit-topology-v1"
SCAN_COUNT = 2049
ROOT_RESIDUAL_LIMIT = 1.0e-11
EVENT_MERGE_TOLERANCE = 2.0e-9
BOUNDARY_MERGE_TOLERANCE = 2.0e-10
SIGNATURE_RELATIVE_ERROR_LIMIT = 1.0e-9
CLAIM_FIELDS = (
    "valid_for_boundary_aligned_energy_angle_cubature",
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


M5307 = load_module("mts_5307_for_5308", SCRIPT_5307)
M5305 = M5307.M5305
M5304 = M5305.M5304
M5303 = M5307.M5303
M5302 = M5305.M5302
M5301 = M5307.M5301
M5280 = M5307.M5280
M5283 = M5307.M5283
M5272 = M5304.M5272
np = M5307.np
mp = M5307.mp


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


def energy_limits() -> tuple[float, float]:
    return M5304.energy_limits()


def q_limits() -> tuple[float, float]:
    minimum, maximum = energy_limits()
    return math.sqrt(1.0 - maximum), math.sqrt(1.0 - minimum)


def angular_limit() -> float:
    return M5304.angular_limit()


def surface_specs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component_id, hard_leg_sign in (("MC04", 1), ("MC12", -1)):
        for soft_sign in (-1, 1):
            for decay_sign in (-1, 1):
                rows.append(
                    {
                        "surface_id": (
                            f"{component_id}_S"
                            f"{'P' if soft_sign > 0 else 'M'}_D"
                            f"{'P' if decay_sign > 0 else 'M'}"
                        ),
                        "component_id": component_id,
                        "hard_leg_sign": hard_leg_sign,
                        "soft_sign": soft_sign,
                        "decay_sign": decay_sign,
                        "target_cosine": -0.3,
                    }
                )
    return rows


SURFACES = surface_specs()
SURFACE_LOOKUP = {row["surface_id"]: row for row in SURFACES}


def coefficients(spec: dict[str, Any], coordinate: float) -> tuple[float, ...]:
    return M5272.hard_boundary_coefficients(
        int(spec["soft_sign"]) * coordinate,
        int(spec["decay_sign"]) * M5302.EDGE_DECAY_ABSOLUTE,
        int(spec["hard_leg_sign"]),
        float(spec["target_cosine"]),
        math.pi,
    )


def discriminant(spec: dict[str, Any], coordinate: float) -> float:
    coefficient_q2, coefficient_q1, coefficient_q0 = coefficients(
        spec, coordinate
    )
    return coefficient_q1**2 - 4.0 * coefficient_q2 * coefficient_q0


def all_real_roots(spec: dict[str, Any], coordinate: float) -> list[float]:
    return sorted(float(root) for root in M5272.quadratic_real_roots(
        *coefficients(spec, coordinate)
    ))


def physical_branches(
    spec: dict[str, Any], coordinate: float
) -> list[dict[str, Any]]:
    q_minimum, q_maximum = q_limits()
    rows: list[dict[str, Any]] = []
    for root_index, q_value in enumerate(all_real_roots(spec, coordinate), 1):
        if q_minimum - 1.0e-12 <= q_value <= q_maximum + 1.0e-12:
            energy = 1.0 - q_value**2
            rows.append(
                {
                    "surface_id": spec["surface_id"],
                    "component_id": spec["component_id"],
                    "hard_leg_sign": spec["hard_leg_sign"],
                    "soft_sign": spec["soft_sign"],
                    "decay_sign": spec["decay_sign"],
                    "branch_id": f"Q{root_index:02d}",
                    "absolute_soft_cosine": coordinate,
                    "q_value": q_value,
                    "soft_energy": energy,
                    "equation_residual": abs(
                        M5272.hard_boundary_value(
                            q_value,
                            int(spec["soft_sign"]) * coordinate,
                            int(spec["decay_sign"])
                            * M5302.EDGE_DECAY_ABSOLUTE,
                            int(spec["hard_leg_sign"]),
                            float(spec["target_cosine"]),
                            math.pi,
                        )
                    ),
                }
            )
    return rows


def branch_value(
    spec: dict[str, Any], branch_id: str, coordinate: float
) -> float | None:
    root_index = int(branch_id[1:]) - 1
    roots = all_real_roots(spec, coordinate)
    if root_index >= len(roots):
        return None
    q_value = roots[root_index]
    q_minimum, q_maximum = q_limits()
    if not q_minimum - 1.0e-12 <= q_value <= q_maximum + 1.0e-12:
        return None
    return 1.0 - q_value**2


def unique_numbers(values: list[float], tolerance: float) -> list[float]:
    result: list[float] = []
    for value in sorted(values):
        if not result or abs(value - result[-1]) > tolerance:
            result.append(value)
    return result


def bisect_scalar(
    function: Callable[[float], float | None],
    lower: float,
    upper: float,
) -> float:
    lower_value = function(lower)
    upper_value = function(upper)
    if lower_value is None or upper_value is None:
        return 0.5 * (lower + upper)
    for _ in range(80):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = function(midpoint)
        if midpoint_value is None:
            return midpoint
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
    return 0.5 * (lower + upper)


def scan_scalar_roots(
    function: Callable[[float], float | None],
    grid: list[float],
    zero_tolerance: float = 1.0e-11,
) -> list[float]:
    roots: list[float] = []
    previous_coordinate: float | None = None
    previous_value: float | None = None
    for coordinate in grid:
        value = function(coordinate)
        if value is None or not math.isfinite(value):
            previous_coordinate = None
            previous_value = None
            continue
        if abs(value) <= zero_tolerance:
            roots.append(coordinate)
        if (
            previous_coordinate is not None
            and previous_value is not None
            and previous_value * value < 0.0
        ):
            roots.append(
                bisect_scalar(function, previous_coordinate, coordinate)
            )
        previous_coordinate = coordinate
        previous_value = value
    return unique_numbers(roots, EVENT_MERGE_TOLERANCE)


def branch_scan_rows(grid: list[float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for coordinate in grid:
        for spec in SURFACES:
            for row in physical_branches(spec, coordinate):
                rows.append(
                    {
                        **row,
                        "valid_for_full_fixed_decay_surface_branch": (
                            row["equation_residual"] <= ROOT_RESIDUAL_LIMIT
                        ),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def topology_event_rows(grid: list[float]) -> list[dict[str, Any]]:
    raw: list[dict[str, Any]] = [
        {
            "event_type": "ANGULAR_ENDPOINT",
            "owner": "LOWER_ENDPOINT",
            "absolute_soft_cosine": 0.0,
        },
        {
            "event_type": "STATIC_G3_CROSSING",
            "owner": "soft_cosine=+0.3",
            "absolute_soft_cosine": 0.3,
        },
        {
            "event_type": "ANGULAR_ENDPOINT",
            "owner": "UPPER_ENDPOINT",
            "absolute_soft_cosine": angular_limit(),
        },
    ]
    q_minimum, q_maximum = q_limits()
    for spec in SURFACES:
        for coordinate in scan_scalar_roots(
            lambda value, local=spec: discriminant(local, value), grid
        ):
            raw.append(
                {
                    "event_type": "SURFACE_FOLD",
                    "owner": spec["surface_id"],
                    "absolute_soft_cosine": coordinate,
                }
            )
        for label, q_value in (
            ("ENERGY_MAXIMUM_CROSSING", q_minimum),
            ("ENERGY_MINIMUM_CROSSING", q_maximum),
        ):
            for coordinate in scan_scalar_roots(
                lambda value, local=spec, q=q_value: (
                    M5272.hard_boundary_value(
                        q,
                        int(local["soft_sign"]) * value,
                        int(local["decay_sign"])
                        * M5302.EDGE_DECAY_ABSOLUTE,
                        int(local["hard_leg_sign"]),
                        float(local["target_cosine"]),
                        math.pi,
                    )
                ),
                grid,
            ):
                raw.append(
                    {
                        "event_type": label,
                        "owner": spec["surface_id"],
                        "absolute_soft_cosine": coordinate,
                    }
                )
    branch_keys = [
        (spec["surface_id"], branch_id)
        for spec in SURFACES
        for branch_id in ("Q01", "Q02")
    ]
    for first_index, first_key in enumerate(branch_keys):
        first_spec = SURFACE_LOOKUP[first_key[0]]
        for second_key in branch_keys[first_index + 1 :]:
            second_spec = SURFACE_LOOKUP[second_key[0]]
            differences = []
            for coordinate in grid[::64]:
                first = branch_value(first_spec, first_key[1], coordinate)
                second = branch_value(second_spec, second_key[1], coordinate)
                if first is not None and second is not None:
                    differences.append(first - second)
            if differences and max(abs(value) for value in differences) <= 1.0e-10:
                continue
            function = lambda value, a=first_spec, ak=first_key[1], b=second_spec, bk=second_key[1]: (
                None
                if branch_value(a, ak, value) is None
                or branch_value(b, bk, value) is None
                else branch_value(a, ak, value) - branch_value(b, bk, value)
            )
            for coordinate in scan_scalar_roots(function, grid):
                raw.append(
                    {
                        "event_type": "SURFACE_CROSSING",
                        "owner": (
                            f"{first_key[0]}:{first_key[1]}|"
                            f"{second_key[0]}:{second_key[1]}"
                        ),
                        "absolute_soft_cosine": coordinate,
                    }
                )
    coordinates = unique_numbers(
        [float(row["absolute_soft_cosine"]) for row in raw],
        EVENT_MERGE_TOLERANCE,
    )
    rows: list[dict[str, Any]] = []
    for event_index, coordinate in enumerate(coordinates):
        matches = [
            row for row in raw
            if abs(float(row["absolute_soft_cosine"]) - coordinate)
            <= EVENT_MERGE_TOLERANCE
        ]
        rows.append(
            {
                "event_index": event_index,
                "absolute_soft_cosine": coordinate,
                "event_types": "|".join(sorted({row["event_type"] for row in matches})),
                "owners": "|".join(sorted({row["owner"] for row in matches})),
                "valid_for_fixed_decay_topology_event": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def analytic_active_terms(energy: float, coordinate: float) -> tuple[str, ...]:
    q_value = math.sqrt(1.0 - energy)
    active: list[str] = []
    for spec in SURFACES:
        signed_soft = int(spec["soft_sign"]) * coordinate
        signed_decay = (
            int(spec["decay_sign"]) * M5302.EDGE_DECAY_ABSOLUTE
        )
        hard_value = M5272.hard_boundary_value(
            q_value,
            signed_soft,
            signed_decay,
            int(spec["hard_leg_sign"]),
            float(spec["target_cosine"]),
            math.pi,
        )
        g3_value = signed_soft - 0.3
        if hard_value * g3_value < 0.0:
            active.append(spec["surface_id"])
    return tuple(sorted(active))


def boundary_groups(coordinate: float) -> list[dict[str, Any]]:
    roots = [
        row
        for spec in SURFACES
        for row in physical_branches(spec, coordinate)
    ]
    roots.sort(key=lambda row: float(row["soft_energy"]))
    groups: list[list[dict[str, Any]]] = []
    for row in roots:
        if (
            not groups
            or abs(
                float(row["soft_energy"])
                - float(groups[-1][0]["soft_energy"])
            )
            > BOUNDARY_MERGE_TOLERANCE
        ):
            groups.append([row])
        else:
            groups[-1].append(row)
    return [
        {
            "soft_energy": sum(float(row["soft_energy"]) for row in group)
            / len(group),
            "owners": "|".join(
                sorted(
                    f"{row['surface_id']}:{row['branch_id']}"
                    for row in group
                )
            ),
        }
        for group in groups
    ]


def chamber_templates(coordinate: float) -> list[dict[str, Any]]:
    minimum, maximum = energy_limits()
    groups = boundary_groups(coordinate)
    boundaries = [
        {"soft_energy": minimum, "owners": "ENERGY_MINIMUM"},
        *groups,
        {"soft_energy": maximum, "owners": "ENERGY_MAXIMUM"},
    ]
    rows: list[dict[str, Any]] = []
    for chamber_index, (lower, upper) in enumerate(
        zip(boundaries[:-1], boundaries[1:]), start=1
    ):
        lower_energy = float(lower["soft_energy"])
        upper_energy = float(upper["soft_energy"])
        if upper_energy - lower_energy <= 1.0e-12:
            continue
        midpoint = 0.5 * (lower_energy + upper_energy)
        active = analytic_active_terms(midpoint, coordinate)
        rows.append(
            {
                "chamber_index": chamber_index,
                "representative_absolute_soft_cosine": coordinate,
                "lower_soft_energy": lower_energy,
                "upper_soft_energy": upper_energy,
                "lower_boundary_owners": lower["owners"],
                "upper_boundary_owners": upper["owners"],
                "active_term_ids": "|".join(active),
                "active_term_count": len(active),
            }
        )
    return rows


def topology_fingerprint(coordinate: float) -> tuple[Any, ...]:
    return tuple(
        (
            row["lower_boundary_owners"],
            row["upper_boundary_owners"],
            row["active_term_ids"],
        )
        for row in chamber_templates(coordinate)
    )


def x_panel_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    coordinates = [float(row["absolute_soft_cosine"]) for row in events]
    rows: list[dict[str, Any]] = []
    for panel_index, (lower, upper) in enumerate(
        zip(coordinates[:-1], coordinates[1:]), start=1
    ):
        fractions = (0.2, 0.5, 0.8)
        fingerprints = [
            topology_fingerprint(lower + fraction * (upper - lower))
            for fraction in fractions
        ]
        stable = fingerprints[0] == fingerprints[1] == fingerprints[2]
        rows.append(
            {
                "x_panel_index": panel_index,
                "lower_absolute_soft_cosine": lower,
                "upper_absolute_soft_cosine": upper,
                "representative_absolute_soft_cosine": 0.5 * (lower + upper),
                "topology_fingerprint": json.dumps(fingerprints[1]),
                "fingerprint_probe_count": len(fingerprints),
                "valid_for_topology_stable_x_panel": stable,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def boundary_energy(owner: str, coordinate: float) -> float:
    minimum, maximum = energy_limits()
    if owner == "ENERGY_MINIMUM":
        return minimum
    if owner == "ENERGY_MAXIMUM":
        return maximum
    first_owner = owner.split("|")[0]
    surface_id, branch_id = first_owner.rsplit(":", 1)
    value = branch_value(SURFACE_LOOKUP[surface_id], branch_id, coordinate)
    if value is None:
        raise RuntimeError(
            f"boundary {first_owner} absent at |s|={coordinate}"
        )
    return value


def term_values(
    evaluate: Any,
    epsilon_id: str,
    energy: float,
    coordinate: float,
) -> tuple[dict[str, complex], dict[str, bool]]:
    values: dict[str, complex] = {}
    masks: dict[str, bool] = {}
    for spec in SURFACES:
        value, active = evaluate(
            epsilon_id,
            energy,
            coordinate,
            spec["component_id"],
            int(spec["soft_sign"]),
            int(spec["decay_sign"]),
        )
        values[spec["surface_id"]] = value
        masks[spec["surface_id"]] = active
    return values, masks


def cancellation_remainder(values: dict[str, complex]) -> tuple[str, ...]:
    remaining = sorted(
        term_id for term_id, value in values.items() if abs(value) > 0.0
    )
    while True:
        best: tuple[float, int, int] | None = None
        for first_index, first_id in enumerate(remaining):
            for second_index in range(first_index + 1, len(remaining)):
                second_id = remaining[second_index]
                change = relative_complex_change(
                    values[first_id], -values[second_id]
                )
                if change <= SIGNATURE_RELATIVE_ERROR_LIMIT and (
                    best is None or change < best[0]
                ):
                    best = (change, first_index, second_index)
        if best is None:
            break
        _, first_index, second_index = best
        remaining.pop(second_index)
        remaining.pop(first_index)
    return tuple(remaining)


def chamber_rows(
    panels: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for panel in panels:
        coordinate = float(panel["representative_absolute_soft_cosine"])
        for local in chamber_templates(coordinate):
            rows.append(
                {
                    "x_panel_index": panel["x_panel_index"],
                    "chamber_index": local["chamber_index"],
                    "lower_absolute_soft_cosine": panel[
                        "lower_absolute_soft_cosine"
                    ],
                    "upper_absolute_soft_cosine": panel[
                        "upper_absolute_soft_cosine"
                    ],
                    **local,
                    "valid_for_topology_stable_energy_chamber": parse_bool(
                        panel["valid_for_topology_stable_x_panel"]
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def reduction_rows(
    chambers: list[dict[str, Any]],
    evaluate: Any,
) -> tuple[list[dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    summaries: dict[tuple[int, int], dict[str, Any]] = {}
    probe_fractions = (
        (0.23, 0.23),
        (0.50, 0.50),
        (0.77, 0.77),
        (0.23, 0.77),
    )
    for chamber_counter, chamber in enumerate(chambers, start=1):
        x_lower = float(chamber["lower_absolute_soft_cosine"])
        x_upper = float(chamber["upper_absolute_soft_cosine"])
        active_ids = tuple(
            value for value in str(chamber["active_term_ids"]).split("|")
            if value
        )
        probe_payloads: list[dict[str, Any]] = []
        candidate_ids: tuple[str, ...] | None = None
        for probe_index, (x_fraction, energy_fraction) in enumerate(
            probe_fractions, start=1
        ):
            coordinate = x_lower + x_fraction * (x_upper - x_lower)
            energy_lower = boundary_energy(
                str(chamber["lower_boundary_owners"]), coordinate
            )
            energy_upper = boundary_energy(
                str(chamber["upper_boundary_owners"]), coordinate
            )
            if energy_upper <= energy_lower:
                raise RuntimeError(
                    f"reversed chamber at panel {chamber['x_panel_index']} "
                    f"chamber {chamber['chamber_index']}"
                )
            energy = energy_lower + energy_fraction * (
                energy_upper - energy_lower
            )
            values, masks = term_values(evaluate, "E020", energy, coordinate)
            analytic = set(analytic_active_terms(energy, coordinate))
            observed = {term_id for term_id, active in masks.items() if active}
            if candidate_ids is None:
                candidate_ids = cancellation_remainder(values)
            full_orbit = sum(values.values(), 0.0j)
            candidate_orbit = sum(
                (values[term_id] for term_id in candidate_ids), 0.0j
            )
            candidate_change = relative_complex_change(
                full_orbit, candidate_orbit
            )
            probe_payloads.append(
                {
                    "probe_index": probe_index,
                    "absolute_soft_cosine": coordinate,
                    "soft_energy": energy,
                    "analytic_active_term_ids": "|".join(sorted(analytic)),
                    "observed_active_term_ids": "|".join(sorted(observed)),
                    "mask_signature_agrees": analytic == observed,
                    "candidate_term_ids": "|".join(candidate_ids),
                    **complex_fields("full_pair_orbit", full_orbit),
                    **complex_fields("candidate_reduced_orbit", candidate_orbit),
                    "candidate_reduction_relative_change": candidate_change,
                }
            )
        candidate_valid = all(
            row["mask_signature_agrees"]
            and float(row["candidate_reduction_relative_change"])
            <= SIGNATURE_RELATIVE_ERROR_LIMIT
            for row in probe_payloads
        )
        final_ids = candidate_ids if candidate_valid else active_ids
        reduction_type = (
            "EXACT_NUMERIC_CANCELLATION_REDUCTION"
            if candidate_valid and len(final_ids) < len(active_ids)
            else (
                "ACTIVE_SIGNATURE_ALREADY_MINIMAL"
                if candidate_valid
                else "FULL_ACTIVE_ORBIT_FALLBACK"
            )
        )
        maximum_final_change = 0.0
        for payload in probe_payloads:
            coordinate = float(payload["absolute_soft_cosine"])
            energy = float(payload["soft_energy"])
            values, _ = term_values(evaluate, "E020", energy, coordinate)
            full_orbit = sum(values.values(), 0.0j)
            final_orbit = sum(
                (values[term_id] for term_id in final_ids), 0.0j
            )
            final_change = relative_complex_change(full_orbit, final_orbit)
            maximum_final_change = max(maximum_final_change, final_change)
            rows.append(
                {
                    "x_panel_index": chamber["x_panel_index"],
                    "chamber_index": chamber["chamber_index"],
                    **payload,
                    "final_evaluation_term_ids": "|".join(final_ids),
                    "reduction_type": reduction_type,
                    **complex_fields("final_reduced_orbit", final_orbit),
                    "final_reduction_relative_change": final_change,
                    "valid_for_pair_orbit_reduction": (
                        payload["mask_signature_agrees"]
                        and final_change <= SIGNATURE_RELATIVE_ERROR_LIMIT
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        summaries[
            (int(chamber["x_panel_index"]), int(chamber["chamber_index"]))
        ] = {
            "evaluation_term_ids": "|".join(final_ids),
            "evaluation_term_count": len(final_ids),
            "reduction_type": reduction_type,
            "maximum_reduction_relative_change": maximum_final_change,
            "valid_for_pair_orbit_reduction": (
                maximum_final_change <= SIGNATURE_RELATIVE_ERROR_LIMIT
                and all(row["mask_signature_agrees"] for row in probe_payloads)
            ),
        }
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "PAIR_ORBIT_REDUCTION_AUDIT",
                "completed_chamber_count": chamber_counter,
                "planned_chamber_count": len(chambers),
            },
        )
    return rows, summaries


def contract_rows(
    chambers: list[dict[str, Any]],
    reductions: dict[tuple[int, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for contract_index, chamber in enumerate(chambers, start=1):
        key = (
            int(chamber["x_panel_index"]),
            int(chamber["chamber_index"]),
        )
        reduction = reductions[key]
        rows.append(
            {
                "contract_index": contract_index,
                "x_panel_index": chamber["x_panel_index"],
                "chamber_index": chamber["chamber_index"],
                "lower_absolute_soft_cosine": chamber[
                    "lower_absolute_soft_cosine"
                ],
                "upper_absolute_soft_cosine": chamber[
                    "upper_absolute_soft_cosine"
                ],
                "lower_energy_boundary": chamber["lower_boundary_owners"],
                "upper_energy_boundary": chamber["upper_boundary_owners"],
                "unit_square_map": (
                    "|s|=s_lo+(s_hi-s_lo)u; "
                    "E=E_lo(|s|)+(E_hi(|s|)-E_lo(|s|))v"
                ),
                "jacobian": (
                    "(s_hi-s_lo)*(E_hi(|s|)-E_lo(|s|))"
                ),
                "active_term_ids": chamber["active_term_ids"],
                **reduction,
                "valid_for_chamber_aligned_cubature_contract": (
                    parse_bool(
                        chamber[
                            "valid_for_topology_stable_energy_chamber"
                        ]
                    )
                    and parse_bool(
                        reduction["valid_for_pair_orbit_reduction"]
                    )
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5307,
        RESULT_5307,
        VALIDATION_5307,
        FUNCTIONAL_RG / "5304" / "moving_mask_edge_energy_map_result.json",
        FUNCTIONAL_RG / "5272" / "analytic_surface_descriptors.csv",
        FUNCTIONAL_RG / "5274" / "all_safe_component_boolean_mask_laws.csv",
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5307)
    validation = read_csv(VALIDATION_5307)
    minimum, maximum = energy_limits()
    checks = {
        "parent_5307_accepted": bool(parent["acceptance_passed"]),
        "parent_5307_validation_passes": all(
            parse_bool(row["passed"]) for row in validation
        ),
        "all_eight_pair_terms_declared": len(SURFACES) == 8,
        "fixed_decay_inside_angular_domain": (
            0.0 < M5302.EDGE_DECAY_ABSOLUTE < angular_limit()
        ),
        "full_energy_domain_nonempty": 0.0 < minimum < maximum < 1.0,
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
            "DRY_RUN_ACCEPTED__DERIVE_FULL_FIXED_DECAY_PAIR_TOPOLOGY"
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
        raise RuntimeError("5308 dry run did not pass")
    grid = [float(value) for value in np.linspace(0.0, angular_limit(), SCAN_COUNT)]
    branches = branch_scan_rows(grid)
    events = topology_event_rows(grid)
    panels = x_panel_rows(events)
    chambers = chamber_rows(panels)
    context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(context)
    reduction, summaries = reduction_rows(chambers, evaluate)
    contract = contract_rows(chambers, summaries)
    formal_end = M5283.formal_inventory_digest()
    parent = read_json(RESULT_5307)
    activation_zero = float(
        read_json(M5304.RESULT)["moving_edge_upper_energy"]
    )
    high_energy_active = [
        row for row in chambers
        if float(row["upper_soft_energy"]) > activation_zero
        and int(row["active_term_count"]) > 0
    ]
    checks = {
        "all_surface_branches_satisfy_exact_equations": all(
            parse_bool(row["valid_for_full_fixed_decay_surface_branch"])
            for row in branches
        ),
        "topology_events_span_full_soft_domain": (
            abs(float(events[0]["absolute_soft_cosine"])) <= 1.0e-14
            and abs(
                float(events[-1]["absolute_soft_cosine"])
                - angular_limit()
            )
            <= 1.0e-14
        ),
        "all_x_panels_have_stable_topology_fingerprints": all(
            parse_bool(row["valid_for_topology_stable_x_panel"])
            for row in panels
        ),
        "all_chamber_masks_and_reductions_validate": all(
            parse_bool(row["valid_for_pair_orbit_reduction"])
            for row in reduction
        ),
        "all_cubature_contract_rows_are_topology_safe": all(
            parse_bool(row["valid_for_chamber_aligned_cubature_contract"])
            for row in contract
        ),
        "static_g3_surface_is_explicit": any(
            "STATIC_G3_CROSSING" in row["event_types"] for row in events
        ),
        "support_continues_above_old_g1_zero_crossing": bool(
            high_energy_active
        ),
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end == parent["formalization_workbench_end_digest"]
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "FULL_FIXED_DECAY_PAIR_ORBIT_TOPOLOGY_DERIVED__"
        "RUN_CHAMBER_ALIGNED_ENERGY_SOFT_CUBATURE"
        if accepted
        else "FULL_FIXED_DECAY_PAIR_TOPOLOGY_REQUIRES_REPAIR"
    )
    write_csv(BRANCH_SCAN, branches)
    write_csv(EVENTS, events)
    write_csv(X_PANELS, panels)
    write_csv(CHAMBERS, chambers)
    write_csv(REDUCTION, reduction)
    write_csv(CONTRACT, contract)
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "full-fixed-decay-pair-orbit-topology",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "absolute_decay_cosine": M5302.EDGE_DECAY_ABSOLUTE,
        "energy_minimum": energy_limits()[0],
        "energy_maximum": energy_limits()[1],
        "surface_branch_scan_row_count": len(branches),
        "topology_event_count": len(events),
        "topology_stable_x_panel_count": len(panels),
        "energy_chamber_count": len(chambers),
        "reduction_probe_count": len(reduction),
        "cubature_contract_row_count": len(contract),
        "high_energy_active_chamber_count": len(high_energy_active),
        "maximum_surface_equation_residual": max(
            float(row["equation_residual"]) for row in branches
        ),
        "maximum_pair_reduction_relative_change": max(
            float(row["final_reduction_relative_change"])
            for row in reduction
        ),
        "full_active_orbit_fallback_count": sum(
            row["reduction_type"] == "FULL_ACTIVE_ORBIT_FALLBACK"
            for row in contract
        ),
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
            "valid_for_full_fixed_decay_pair_orbit_topology": accepted,
            "valid_for_chamber_aligned_cubature_contract": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The full fixed-decay mask chamber arrangement is derived, "
                "but its finite-regulator volume integral and the decay-angle "
                "integral have not yet been run."
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
            "topology_event_count": len(events),
            "energy_chamber_count": len(chambers),
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5308 — Full fixed-decay pair-orbit topology

## Derivation

The earlier moving `g1` edge is not the end of the pair-orbit support.
Both `MC04` and `MC12` obey a product mask with the shared static
`g3` surface `a=+0.3`.  The complete fixed-`|d|` arrangement therefore
contains all signed `g1`, `g2`, and `g3` chambers.  This checkpoint derives
those chambers over the full sourced energy interval rather than extending
the four selected slices by assumption.

- fixed `|d|`: `{result['absolute_decay_cosine']:.15g}`;
- surface branch rows: `{result['surface_branch_scan_row_count']}`;
- topology events: `{result['topology_event_count']}`;
- topology-stable `|s|` panels: `{result['topology_stable_x_panel_count']}`;
- energy chambers: `{result['energy_chamber_count']}`;
- reduction probes: `{result['reduction_probe_count']}`;
- chamber-aligned cubature cells: `{result['cubature_contract_row_count']}`;
- chambers active above the old `g1` zero crossing:
  `{result['high_energy_active_chamber_count']}`;
- maximum surface residual:
  `{result['maximum_surface_equation_residual']:.12g}`;
- maximum pair-reduction change:
  `{result['maximum_pair_reduction_relative_change']:.12g}`;
- full-orbit fallbacks: `{result['full_active_orbit_fallback_count']}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Consequence

The next numerical step has an explicit unit-square map for every fixed-decay
energy/soft-angle chamber.  It must integrate finite regulators on those
cells and take the regulator limit after integration.  It must not truncate
the energy domain at the old `g1` zero crossing.

## Claim boundary

This is a complete topology and cubature-coordinate result at one fixed
decay angle.  It is not yet the finite-regulator volume integral, the
decay-angle integral, a full phase-space coefficient, local GR, or the full
MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    branches = read_csv(BRANCH_SCAN)
    events = read_csv(EVENTS)
    panels = read_csv(X_PANELS)
    chambers = read_csv(CHAMBERS)
    reductions = read_csv(REDUCTION)
    contract = read_csv(CONTRACT)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "surface_branch_rows_exact",
            len(branches) == int(result["surface_branch_scan_row_count"])
            and all(
                parse_bool(
                    row["valid_for_full_fixed_decay_surface_branch"]
                )
                for row in branches
            ),
            f"rows={len(branches)}",
        ),
        validation_gate(
            "topology_partition_complete",
            len(events) == int(result["topology_event_count"])
            and len(panels)
            == int(result["topology_stable_x_panel_count"])
            and all(
                parse_bool(row["valid_for_topology_stable_x_panel"])
                for row in panels
            ),
            f"events={len(events)}; panels={len(panels)}",
        ),
        validation_gate(
            "energy_chambers_and_reductions_complete",
            len(chambers) == int(result["energy_chamber_count"])
            and len(reductions) == int(result["reduction_probe_count"])
            and all(
                parse_bool(row["valid_for_pair_orbit_reduction"])
                for row in reductions
            ),
            f"chambers={len(chambers)}; probes={len(reductions)}",
        ),
        validation_gate(
            "cubature_contract_complete",
            len(contract) == int(result["cubature_contract_row_count"])
            and all(
                parse_bool(
                    row["valid_for_chamber_aligned_cubature_contract"]
                )
                for row in contract
            ),
            f"rows={len(contract)}",
        ),
        validation_gate(
            "high_energy_support_not_truncated",
            int(result["high_energy_active_chamber_count"]) > 0,
            str(result["high_energy_active_chamber_count"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"],
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "recorded_source_paths_and_hashes_current",
            source_files_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "full_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no cubature, phase-space, UV, local-GR, or full-MTS claim",
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
            "VALIDATED_FULL_FIXED_DECAY_PAIR_ORBIT_TOPOLOGY"
            if passed
            else "FULL_FIXED_DECAY_PAIR_TOPOLOGY_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
    return parser.parse_args()


def main() -> int:
    set_below_normal_priority()
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
