from __future__ import annotations

import argparse
import csv
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


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5393"
DOCUMENT = POST / "5393-Y5-R2FR-D4-parent-frozen-mapped-away-atlas-and-W3-owner-decomposition.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5393_VALIDATION.csv"

SCRIPT_5308 = SCRIPTS / "Y5_R2FR_5308_full_fixed_decay_pair_orbit_topology.py"
PARENT_PANELS = FUNCTIONAL_RG / "5324" / "decay_angle_topology_soft_panels.csv"
PARENT_CHAMBERS = FUNCTIONAL_RG / "5324" / "decay_angle_energy_chambers.csv"
PARENT_TOPOLOGY_RESULT = (
    FUNCTIONAL_RG
    / "5324"
    / "decay_angle_measure_symmetry_topology_preflight_result.json"
)
PARENT_CONTRACT = (
    FUNCTIONAL_RG
    / "5334"
    / "E0025"
    / "D4_outer_reduced_MC04_cubature_contract.csv"
)
EVENT_CERTIFICATE = (
    FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
)
EVENT_RESULT = (
    FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
)
TUBE_BOXES = (
    FUNCTIONAL_RG / "5379" / "D4_parametric_interval_Newton_boxes.csv"
)
TUBE_RESULT = (
    FUNCTIONAL_RG / "5379" / "D4_parametric_interval_Newton_result.json"
)
ENDPOINT_RESULT = FUNCTIONAL_RG / "5392" / "D4_endpoint_G3_result.json"
REDUCTION_DOCUMENT = (
    POST / "5376-Y5-R2FR-D4-uniform-remainder-decomposition-and-bound-reduction.md"
)
SELECTED_COMPONENTS = (
    FUNCTIONAL_RG / "5376" / "D4_selected_leaf_component_decomposition.csv"
)
REDUCTION_RESULT = (
    FUNCTIONAL_RG / "5376" / "D4_uniform_remainder_reduction_result.json"
)

CHECKPOINT = 5393
MARKER = "MTS_5393_D4_PARENT_FROZEN_MAPPED_AWAY_ATLAS_AND_W3_OWNER_DECOMPOSITION"
REVISION = "D4-parent-frozen-mapped-away-atlas-W3-owner-v1"
DECAY_NODE_ID = "D4_OUTER"
ABSOLUTE_DECAY_COSINE = 0.8568306300360823
EXPECTED_PARENT_PANEL_COUNT = 13
EXPECTED_PARENT_CONTRACT_COUNT = 55
EXPECTED_ACTIVE_CONTRACT_COUNT = 29
EXPECTED_EVENT_COUNT = 8
RUNG_IDS = (
    "E020",
    "E010",
    "E005",
    "E0025",
    "E00125",
    "E000625",
    "E0003125",
)

CLAIM_ATLAS = "valid_for_D4_parent_frozen_mapped_away_atlas"
CLAIM_OWNERS = "valid_for_D4_complete_pole_owner_decomposition"
CLAIM_REDUCTION = "valid_for_D4_finite_W3_owner_reduction"
OPEN_CLAIMS = (
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


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5308 = load_module("mts_5308_for_5393", SCRIPT_5308)
M5308.M5302.EDGE_DECAY_ABSOLUTE = ABSOLUTE_DECAY_COSINE


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def rung_paths(rung_id: str) -> tuple[Path, Path, Path]:
    source = FUNCTIONAL_RG / "5334" / rung_id
    stem = f"D4_outer_event_aligned_{rung_id}"
    return (
        source / f"{stem}_geometric_poles.csv",
        source / f"{stem}_pole_classification.csv",
        source / f"{stem}_result.json",
    )


def source_paths() -> tuple[Path, ...]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5308.resolve(),
        PARENT_PANELS.resolve(),
        PARENT_CHAMBERS.resolve(),
        PARENT_TOPOLOGY_RESULT.resolve(),
        PARENT_CONTRACT.resolve(),
        EVENT_CERTIFICATE.resolve(),
        EVENT_RESULT.resolve(),
        TUBE_BOXES.resolve(),
        TUBE_RESULT.resolve(),
        ENDPOINT_RESULT.resolve(),
        REDUCTION_DOCUMENT.resolve(),
        SELECTED_COMPONENTS.resolve(),
        REDUCTION_RESULT.resolve(),
    ]
    for rung_id in RUNG_IDS:
        paths.extend(path.resolve() for path in rung_paths(rung_id))
    return tuple(paths)


def parent_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    panels = [
        row
        for row in read_csv(PARENT_PANELS)
        if row["decay_node_id"] == DECAY_NODE_ID
    ]
    chambers = [
        row
        for row in read_csv(PARENT_CHAMBERS)
        if row["decay_node_id"] == DECAY_NODE_ID
    ]
    contract = read_csv(PARENT_CONTRACT)
    panels.sort(key=lambda row: int(row["x_panel_index"]))
    chambers.sort(
        key=lambda row: (int(row["x_panel_index"]), int(row["chamber_index"]))
    )
    contract.sort(key=lambda row: int(row["contract_index"]))
    return panels, chambers, contract


def event_tube_rows() -> list[dict[str, Any]]:
    certificates = {row["event_id"]: row for row in read_csv(EVENT_CERTIFICATE)}
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(TUBE_BOXES):
        grouped.setdefault(row["event_id"], []).append(row)
    rows: list[dict[str, Any]] = []
    for event_id in sorted(grouped):
        boxes = grouped[event_id]
        certificate = certificates[event_id]
        lower_values = {float(row["fixed_tube_lower"]) for row in boxes}
        upper_values = {float(row["fixed_tube_upper"]) for row in boxes}
        rows.append(
            {
                "event_id": event_id,
                "event_type": certificate["event_type"],
                "term_id": certificate["term_id"],
                "primary_surface_id": certificate["primary_surface_id"],
                "zero_regulator_coordinate": float(
                    certificate["zero_regulator_absolute_soft_cosine"]
                ),
                "fixed_tube_lower": min(lower_values),
                "fixed_tube_upper": max(upper_values),
                "source_box_count": len(boxes),
                "fixed_bounds_identical_across_boxes": (
                    len(lower_values) == 1 and len(upper_values) == 1
                ),
                "all_real_interval_Newton_boxes_pass": all(
                    parse_bool(row["box_certificate_passes"])
                    and parse_bool(
                        row["valid_for_D4_common_closed_real_interval_event_atlas"]
                    )
                    for row in boxes
                ),
            }
        )
    return rows


def merged_breakpoints(values: list[float], tolerance: float = 1.0e-14) -> list[float]:
    merged: list[float] = []
    for value in sorted(values):
        if not merged or abs(value - merged[-1]) > tolerance:
            merged.append(value)
    return merged


def build_x_atlas(
    panels: list[dict[str, str]], tubes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    domain_lower = float(panels[0]["lower_absolute_soft_cosine"])
    domain_upper = float(panels[-1]["upper_absolute_soft_cosine"])
    breakpoints = [domain_lower, domain_upper]
    for panel in panels:
        breakpoints.extend(
            (
                float(panel["lower_absolute_soft_cosine"]),
                float(panel["upper_absolute_soft_cosine"]),
            )
        )
    for tube in tubes:
        breakpoints.extend(
            (
                max(domain_lower, float(tube["fixed_tube_lower"])),
                min(domain_upper, float(tube["fixed_tube_upper"])),
            )
        )
    points = merged_breakpoints(breakpoints)
    rows: list[dict[str, Any]] = []
    for index, (lower, upper) in enumerate(zip(points, points[1:]), 1):
        midpoint = 0.5 * (lower + upper)
        parent_matches = [
            panel
            for panel in panels
            if float(panel["lower_absolute_soft_cosine"]) <= midpoint
            <= float(panel["upper_absolute_soft_cosine"])
        ]
        tube_matches = [
            tube
            for tube in tubes
            if float(tube["fixed_tube_lower"]) < midpoint
            < float(tube["fixed_tube_upper"])
        ]
        if len(parent_matches) != 1:
            raise RuntimeError(
                f"x cell [{lower},{upper}] has {len(parent_matches)} parent panels"
            )
        if len(tube_matches) > 1:
            raise RuntimeError(
                f"x cell [{lower},{upper}] lies in overlapping event tubes"
            )
        panel = parent_matches[0]
        tube = tube_matches[0] if tube_matches else None
        rows.append(
            {
                "atlas_cell_id": f"X{index:03d}",
                "parent_x_panel_index": int(panel["x_panel_index"]),
                "lower_absolute_soft_cosine": lower,
                "upper_absolute_soft_cosine": upper,
                "midpoint_absolute_soft_cosine": midpoint,
                "cell_width": upper - lower,
                "region_class": "EVENT_TUBE" if tube else "AWAY",
                "event_id": tube["event_id"] if tube else "",
                "event_type": tube["event_type"] if tube else "",
                "event_term_id": tube["term_id"] if tube else "",
                "event_primary_surface_id": (
                    tube["primary_surface_id"] if tube else ""
                ),
                "coordinate_owner": (
                    "5391_H_PLUS_5392_G_EVENT_LOCALIZATION"
                    if tube
                    else "PARENT_TOPOLOGY_STABLE_AWAY_CELL"
                ),
                "valid_for_D4_common_parent_frozen_x_atlas": True,
                "valid_for_D4_numeric_W3_bound": False,
            }
        )
    return rows


def boundary_energy(owner: str, coordinate: float) -> float:
    return float(M5308.boundary_energy(owner, coordinate))


def chamber_reproduction(
    chambers: list[dict[str, str]],
) -> tuple[float, float]:
    maximum_error = 0.0
    minimum_width = math.inf
    for row in chambers:
        coordinate = float(row["representative_absolute_soft_cosine"])
        lower = boundary_energy(row["lower_boundary_owners"], coordinate)
        upper = boundary_energy(row["upper_boundary_owners"], coordinate)
        maximum_error = max(
            maximum_error,
            abs(lower - float(row["lower_soft_energy"])),
            abs(upper - float(row["upper_soft_energy"])),
        )
        minimum_width = min(minimum_width, upper - lower)
    return maximum_error, minimum_width


def build_mapped_cells(
    atlas: list[dict[str, Any]],
    contract: list[dict[str, str]],
    chambers: list[dict[str, str]],
) -> list[dict[str, Any]]:
    active = [row for row in contract if not parse_bool(row["algebraically_zero_cell"])]
    chamber_lookup = {
        (int(row["x_panel_index"]), int(row["chamber_index"])): row
        for row in chambers
    }
    rows: list[dict[str, Any]] = []
    for x_row in atlas:
        panel_index = int(x_row["parent_x_panel_index"])
        for contract_row in active:
            if int(contract_row["x_panel_index"]) != panel_index:
                continue
            lower_x = float(x_row["lower_absolute_soft_cosine"])
            upper_x = float(x_row["upper_absolute_soft_cosine"])
            midpoint_x = float(x_row["midpoint_absolute_soft_cosine"])
            lower_owner = contract_row["lower_energy_boundary"]
            upper_owner = contract_row["upper_energy_boundary"]
            lower_energy = boundary_energy(lower_owner, midpoint_x)
            upper_energy = boundary_energy(upper_owner, midpoint_x)
            energy_width = upper_energy - lower_energy
            x_width = upper_x - lower_x
            chamber = chamber_lookup[
                (panel_index, int(contract_row["chamber_index"]))
            ]
            rows.append(
                {
                    "mapped_cell_id": f"U{len(rows) + 1:03d}",
                    "atlas_cell_id": x_row["atlas_cell_id"],
                    "region_class": x_row["region_class"],
                    "event_id": x_row["event_id"],
                    "parent_contract_index": int(contract_row["contract_index"]),
                    "parent_x_panel_index": panel_index,
                    "parent_chamber_index": int(contract_row["chamber_index"]),
                    "lower_absolute_soft_cosine": lower_x,
                    "upper_absolute_soft_cosine": upper_x,
                    "lower_energy_boundary": lower_owner,
                    "upper_energy_boundary": upper_owner,
                    "reduced_MC04_term_ids": contract_row[
                        "reduced_MC04_term_ids"
                    ],
                    "map_domain": "[-1,1]_xi_x_[-1,1]_eta",
                    "x_map": "x=x_mid+(x_hi-x_lo)*xi/2",
                    "energy_map": "E=(E_L(x)+E_U(x))/2+(E_U(x)-E_L(x))*eta/2",
                    "jacobian": "J=(x_hi-x_lo)*(E_U(x)-E_L(x))/4",
                    "midpoint_energy_lower": lower_energy,
                    "midpoint_energy_upper": upper_energy,
                    "midpoint_energy_width": energy_width,
                    "midpoint_jacobian": x_width * energy_width / 4.0,
                    "parent_representative_energy_lower": float(
                        chamber["lower_soft_energy"]
                    ),
                    "parent_representative_energy_upper": float(
                        chamber["upper_soft_energy"]
                    ),
                    "integrand_owner": (
                        "EVENT_LOCAL_DESINGULARIZED_REMAINDER"
                        if x_row["region_class"] == "EVENT_TUBE"
                        else "AWAY_POLE_SUBTRACTED_REGULAR_REMAINDER"
                    ),
                    "valid_for_D4_parent_frozen_mapped_cell": energy_width > 0,
                    "valid_for_D4_numeric_W3_bound": False,
                }
            )
    return rows


def branch_definitions() -> list[dict[str, Any]]:
    return [
        {
            "branch_owner_id": "B01",
            "term_id": "MC04_SM_DM",
            "primary_surface_id": "direct:L:s14",
            "pole_class": "MATERIAL_SIMPLE_POLE",
            "support_start_event": "E01",
            "support_end_event": "E04",
        },
        {
            "branch_owner_id": "B02",
            "term_id": "MC04_SM_DM",
            "primary_surface_id": "direct:shared:s13",
            "pole_class": "MATERIAL_SIMPLE_POLE",
            "support_start_event": "E07",
            "support_end_event": "E08",
        },
        {
            "branch_owner_id": "B03",
            "term_id": "MC04_SP_DP",
            "primary_surface_id": "direct:L:s01",
            "pole_class": "MATERIAL_SIMPLE_POLE",
            "support_start_event": "E02",
            "support_end_event": "E05",
        },
        {
            "branch_owner_id": "B04",
            "term_id": "MC04_SP_DP",
            "primary_surface_id": "direct:shared:s13",
            "pole_class": "MATERIAL_SIMPLE_POLE",
            "support_start_event": "E03",
            "support_end_event": "E06",
        },
        {
            "branch_owner_id": "B05",
            "term_id": "MC04_SM_DM",
            "primary_surface_id": "direct:R:s01",
            "pole_class": "REMOVABLE_ZERO_RESIDUE_POLE",
            "support_start_event": "",
            "support_end_event": "",
        },
        {
            "branch_owner_id": "B06",
            "term_id": "MC04_SP_DM",
            "primary_surface_id": "direct:R:s01",
            "pole_class": "REMOVABLE_ZERO_RESIDUE_POLE",
            "support_start_event": "",
            "support_end_event": "",
        },
    ]


def build_branch_ownership(
    events: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    definitions = branch_definitions()
    definition_lookup = {
        (row["term_id"], row["primary_surface_id"]): row
        for row in definitions
    }
    event_lookup = {row["event_id"]: row for row in events}
    observed: dict[str, dict[str, Any]] = {
        row["branch_owner_id"]: {
            "count": 0,
            "rungs": set(),
            "pole_ids": set(),
            "x_values": [],
            "all_classifications_resolved": True,
            "all_classifications_match_owner": True,
            "all_nodes_pole_subtracted": True,
        }
        for row in definitions
    }
    unmatched: list[str] = []
    missing_classifications: list[str] = []
    total_inside_support = 0
    for rung_id in RUNG_IDS:
        geometric_path, classification_path, _ = rung_paths(rung_id)
        classifications: dict[tuple[str, str, str], list[dict[str, str]]] = {}
        for row in read_csv(classification_path):
            if not parse_bool(row.get("pole_classification_resolved", False)):
                continue
            key = (row["node_id"], row["term_id"], row["pole_id"])
            classifications.setdefault(key, []).append(row)
        for pole in read_csv(geometric_path):
            if not parse_bool(pole["inside_reduced_term_support"]):
                continue
            total_inside_support += 1
            owner = definition_lookup.get(
                (pole["term_id"], pole["primary_surface_id"])
            )
            key = (pole["node_id"], pole["term_id"], pole["pole_id"])
            class_rows = classifications.get(key, [])
            key_text = "|".join((rung_id, *key, pole["primary_surface_id"]))
            if owner is None:
                unmatched.append(key_text)
                continue
            state = observed[owner["branch_owner_id"]]
            state["count"] += 1
            state["rungs"].add(rung_id)
            state["pole_ids"].add(pole["pole_id"])
            state["x_values"].append(float(pole["absolute_soft_cosine"]))
            if not class_rows:
                state["all_classifications_resolved"] = False
                state["all_classifications_match_owner"] = False
                state["all_nodes_pole_subtracted"] = False
                missing_classifications.append(key_text)
                continue
            expected_material = owner["pole_class"] == "MATERIAL_SIMPLE_POLE"
            matching = [
                row
                for row in class_rows
                if parse_bool(row.get("material_simple_pole", False))
                == expected_material
                and parse_bool(row.get("removable_zero_residue_pole", False))
                == (not expected_material)
            ]
            state["all_classifications_match_owner"] &= bool(matching)
            state["all_nodes_pole_subtracted"] &= any(
                parse_bool(row.get("valid_for_pole_subtracted_outer_soft_node", False))
                for row in matching
            )
    rows: list[dict[str, Any]] = []
    for definition in definitions:
        state = observed[definition["branch_owner_id"]]
        start_event = definition["support_start_event"]
        end_event = definition["support_end_event"]
        start_coordinate = (
            event_lookup[start_event]["zero_regulator_coordinate"]
            if start_event
            else ""
        )
        end_coordinate = (
            event_lookup[end_event]["zero_regulator_coordinate"]
            if end_event
            else ""
        )
        material = definition["pole_class"] == "MATERIAL_SIMPLE_POLE"
        rows.append(
            {
                **definition,
                "support_start_coordinate_epsilon_zero": start_coordinate,
                "support_end_coordinate_epsilon_zero": end_coordinate,
                "observed_inside_support_row_count": state["count"],
                "observed_rung_ids": "|".join(sorted(state["rungs"])),
                "observed_pole_labels": "|".join(sorted(state["pole_ids"])),
                "observed_x_minimum": min(state["x_values"]),
                "observed_x_maximum": max(state["x_values"]),
                "subtraction_owner": (
                    "rho_b/(E-p_b); exact primitive rho_b[Log(E_U-p_b)-Log(E_L-p_b)]"
                    if material
                    else "rho_b=0 algebraically; use analytic removable continuation"
                ),
                "all_classifications_resolved": state[
                    "all_classifications_resolved"
                ],
                "all_classifications_match_owner": state[
                    "all_classifications_match_owner"
                ],
                "all_observed_nodes_have_pole_subtraction_contract": state[
                    "all_nodes_pole_subtracted"
                ],
                "valid_for_D4_numeric_W3_bound": False,
            }
        )
    diagnostics = {
        "total_inside_support_geometric_pole_rows": total_inside_support,
        "assigned_inside_support_geometric_pole_rows": sum(
            int(row["observed_inside_support_row_count"]) for row in rows
        ),
        "unmatched_geometric_pole_rows": unmatched,
        "missing_resolved_classification_rows": missing_classifications,
    }
    return rows, diagnostics


def decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "H_EVENT_LOG",
            "sector": "EVENT_TUBES",
            "dimension_after_mapping": 1,
            "exact_term": "sum_e H_e(epsilon) Log(epsilon/epsilon_ref)",
            "third_derivative_status": "CERTIFIED_BY_5391",
            "included_in_W": False,
            "next_action": "none",
        },
        {
            "owner_id": "G_EVENT_NONLOG",
            "sector": "EVENT_TUBES",
            "dimension_after_mapping": 1,
            "exact_term": "sum_e G_e(epsilon)",
            "third_derivative_status": "CERTIFIED_BY_5392",
            "included_in_W": False,
            "next_action": "none",
        },
        {
            "owner_id": "W_AWAY_REGULAR_2D",
            "sector": "AWAY",
            "dimension_after_mapping": 2,
            "exact_term": "sum_U integral_[-1,1]^2 f_reg(Phi_U;epsilon) J_U dxi deta",
            "third_derivative_status": "FINITE_ATLAS_FROZEN__INTERVAL_ENCLOSURE_PENDING",
            "included_in_W": True,
            "next_action": "interval-enclose 4 sup|partial_epsilon^3(f_reg J)| on every away cell",
        },
        {
            "owner_id": "W_AWAY_POLE_PRIMITIVE_1D",
            "sector": "AWAY",
            "dimension_after_mapping": 1,
            "exact_term": "sum_b integral dx rho_b[Log(E_U-p_b)-Log(E_L-p_b)]",
            "third_derivative_status": "EXACT_PRIMITIVE_FROZEN__INTERVAL_ENCLOSURE_PENDING",
            "included_in_W": True,
            "next_action": "enclose 2 sup|partial_epsilon^3(P_b J_x)| with fixed log branches",
        },
        {
            "owner_id": "W_EVENT_LOCAL_REMAINDER",
            "sector": "EVENT_TUBES",
            "dimension_after_mapping": 2,
            "exact_term": "sum_e [I_tube,e-H_e Log(epsilon/epsilon_ref)-G_e]",
            "third_derivative_status": "DESINGULARIZED_COORDINATES_EXIST__REMAINDER_ENCLOSURE_PENDING",
            "included_in_W": True,
            "next_action": "reuse 5392 v=epsilon h boxes to enclose the local analytic remainder",
        },
    ]


def render_document(result: dict[str, Any], branches: list[dict[str, Any]]) -> None:
    branch_lines = [
        (
            f"- `{row['branch_owner_id']}`: `{row['term_id']}` / "
            f"`{row['primary_surface_id']}` -> `{row['pole_class']}`; "
            f"observed rows `{row['observed_inside_support_row_count']}`."
        )
        for row in branches
    ]
    text = "\n".join(
        [
            "# 5393: D4 parent-frozen mapped-away atlas and W3 owner decomposition",
            "",
            "## Decision",
            "",
            f"**{result['decision']}**",
            "",
            "This checkpoint does not claim `W3`. It replaces the seven incompatible",
            "adaptive finite-rung leaf sets by one regulator-independent atlas inherited",
            "from the parent topology contract and the eight fixed 5379 event tubes.",
            "",
            "## Exact common map",
            "",
            "For every frozen x-cell `X=[x_lo,x_hi]` and every active parent energy",
            "chamber `C=[E_L(x),E_U(x)]`, use",
            "",
            "```text",
            "x = x_mid + (x_hi-x_lo) xi/2",
            "E = (E_L(x)+E_U(x))/2 + (E_U(x)-E_L(x)) eta/2",
            "J = (x_hi-x_lo)(E_U(x)-E_L(x))/4",
            "(xi,eta) in [-1,1]^2.",
            "```",
            "",
            "The source topology certificate fixes the ordering of `E_L,E_U` over each",
            "parent panel. Subdivision by fixed event-tube boundaries therefore preserves",
            "the chamber map rather than introducing a regulator-dependent cubature tree.",
            "",
            "## Pole subtraction",
            "",
            "On an away cell the invariant decomposition is",
            "",
            "```text",
            "f = f_reg + sum_b rho_b/(E-p_b),",
            "P_b = rho_b [Log(E_U-p_b)-Log(E_L-p_b)].",
            "```",
            "",
            "The raw real-energy integrand cannot be bounded directly on a complex",
            "epsilon Cauchy circle: a displaced material pole can cross the real path.",
            "The regular term and exact pole primitive must be enclosed separately.",
            "",
            "## Complete owner table",
            "",
            *branch_lines,
            "",
            "Every inside-support geometric pole row across all seven stored regulator",
            "rungs maps to exactly one of these six analytic owners.",
            "",
            "## Counts",
            "",
            f"- parent topology panels: `{result['parent_panel_count']}`;",
            f"- frozen x-cells: `{result['frozen_x_cell_count']}` "
            f"(`{result['away_x_cell_count']}` away, `{result['event_x_cell_count']}` event);",
            f"- mapped active cells: `{result['mapped_active_cell_count']}`;",
            f"- observed inside-support poles assigned: "
            f"`{result['assigned_inside_support_geometric_pole_rows']}` / "
            f"`{result['total_inside_support_geometric_pole_rows']}`;",
            f"- maximum parent boundary reproduction error: "
            f"`{result['maximum_parent_chamber_boundary_reproduction_error']:.12g}`;",
            f"- minimum mapped midpoint energy width: "
            f"`{result['minimum_mapped_midpoint_energy_width']:.12g}`.",
            "",
            "## Remaining calculation",
            "",
            "The next checkpoint must interval-enclose three finite owner families:",
            "`W_AWAY_REGULAR_2D`, `W_AWAY_POLE_PRIMITIVE_1D`, and",
            "`W_EVENT_LOCAL_REMAINDER`. Only their sum supplies a numeric `W3`; only",
            "then may `M_D4=max(H3,G3+W3)/6` be formed.",
            "",
            "No outer-regulator, full-angular, UV, local-GR, or full-MTS claim follows.",
        ]
    )
    DOCUMENT.write_text(text + "\n", encoding="utf-8")


def run(output: Path, dry_run: bool = False) -> dict[str, Any]:
    started = time.perf_counter()
    required = source_paths()
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing sources: " + "; ".join(map(str, missing)))
    panels, chambers, contract = parent_rows()
    active_contract = [
        row for row in contract if not parse_bool(row["algebraically_zero_cell"])
    ]
    tubes = event_tube_rows()
    atlas = build_x_atlas(panels, tubes)
    mapped = build_mapped_cells(atlas, contract, chambers)
    branches, branch_diagnostics = build_branch_ownership(tubes)
    decomposition = decomposition_rows()
    topology_result = read_json(PARENT_TOPOLOGY_RESULT)
    selected_components = read_csv(SELECTED_COMPONENTS)
    reduction_result = read_json(REDUCTION_RESULT)
    tube_result = read_json(TUBE_RESULT)
    endpoint_result = read_json(ENDPOINT_RESULT)
    reproduction_error, parent_minimum_width = chamber_reproduction(chambers)
    domain_lower = float(panels[0]["lower_absolute_soft_cosine"])
    domain_upper = float(panels[-1]["upper_absolute_soft_cosine"])
    atlas_contiguous = (
        abs(float(atlas[0]["lower_absolute_soft_cosine"]) - domain_lower)
        <= 1.0e-15
        and abs(float(atlas[-1]["upper_absolute_soft_cosine"]) - domain_upper)
        <= 1.0e-15
        and all(
            abs(
                float(first["upper_absolute_soft_cosine"])
                - float(second["lower_absolute_soft_cosine"])
            )
            <= 1.0e-15
            for first, second in zip(atlas, atlas[1:])
        )
        and all(float(row["cell_width"]) > 0 for row in atlas)
    )
    tubes_disjoint = all(
        float(first["fixed_tube_upper"]) <= float(second["fixed_tube_lower"])
        for first, second in zip(
            sorted(tubes, key=lambda row: float(row["fixed_tube_lower"])),
            sorted(tubes, key=lambda row: float(row["fixed_tube_lower"]))[1:],
        )
    )
    material_event_pairs_valid = all(
        row["pole_class"] != "MATERIAL_SIMPLE_POLE"
        or (
            row["support_start_event"]
            and row["support_end_event"]
            and float(row["support_start_coordinate_epsilon_zero"])
            < float(row["support_end_coordinate_epsilon_zero"])
        )
        for row in branches
    )
    pole_ownership_complete = (
        not branch_diagnostics["unmatched_geometric_pole_rows"]
        and not branch_diagnostics["missing_resolved_classification_rows"]
        and all(
            int(row["observed_inside_support_row_count"]) > 0
            and row["all_classifications_resolved"] is True
            and row["all_classifications_match_owner"] is True
            and row["all_observed_nodes_have_pole_subtraction_contract"] is True
            for row in branches
        )
    )
    validations = [
        validation_row("all_required_sources_exist", not missing, len(required)),
        validation_row(
            "parent_D4_topology_and_ladder_sources_pass",
            topology_result.get("acceptance_passed") is True
            and reduction_result.get("validation_passed") is True
            and {row["epsilon_id"] for row in selected_components} == set(RUNG_IDS)
            and all(
                parse_bool(row["valid_for_D4_selected_leaf_component_decomposition"])
                and parse_bool(row["valid_for_D4_uniform_remainder_derivative_reduction"])
                for row in selected_components
            ),
            f"topology={topology_result.get('decision')};selected_rungs={len(selected_components)};reduction={reduction_result.get('decision')}",
        ),
        validation_row(
            "parent_panel_and_contract_cardinalities_match",
            len(panels) == EXPECTED_PARENT_PANEL_COUNT
            and len(contract) == EXPECTED_PARENT_CONTRACT_COUNT
            and len(active_contract) == EXPECTED_ACTIVE_CONTRACT_COUNT,
            f"panels={len(panels)};contract={len(contract)};active={len(active_contract)}",
        ),
        validation_row(
            "parent_topology_rows_are_stable_and_reduced",
            all(parse_bool(row["valid_for_topology_stable_x_panel"]) for row in panels)
            and all(
                parse_bool(row["valid_for_topology_stable_energy_chamber"])
                for row in chambers
            )
            and all(
                parse_bool(row["valid_for_MC04_MC12_identity_reduction"])
                for row in contract
            ),
            f"panels={len(panels)};chambers={len(chambers)};contract={len(contract)}",
        ),
        validation_row(
            "parent_boundary_evaluator_reproduces_source_chambers",
            reproduction_error <= 5.0e-12 and parent_minimum_width > 0,
            f"maximum_error={reproduction_error};minimum_width={parent_minimum_width}",
        ),
        validation_row(
            "eight_fixed_event_tubes_are_certified_and_disjoint",
            len(tubes) == EXPECTED_EVENT_COUNT
            and tubes_disjoint
            and all(
                row["fixed_bounds_identical_across_boxes"] is True
                and row["all_real_interval_Newton_boxes_pass"] is True
                for row in tubes
            )
            and tube_result.get("validation_passed") is True,
            f"tubes={len(tubes)};disjoint={tubes_disjoint}",
        ),
        validation_row(
            "parent_frozen_x_atlas_is_contiguous_and_single_owned",
            atlas_contiguous
            and all(row["valid_for_D4_common_parent_frozen_x_atlas"] for row in atlas),
            f"cells={len(atlas)};domain=[{domain_lower},{domain_upper}]",
        ),
        validation_row(
            "every_event_tube_has_at_least_one_frozen_cell",
            {row["event_id"] for row in atlas if row["event_id"]}
            == {row["event_id"] for row in tubes},
            f"represented={sorted({row['event_id'] for row in atlas if row['event_id']})}",
        ),
        validation_row(
            "all_mapped_active_cells_have_positive_width_and_jacobian",
            bool(mapped)
            and all(
                row["valid_for_D4_parent_frozen_mapped_cell"] is True
                and float(row["midpoint_energy_width"]) > 0
                and float(row["midpoint_jacobian"]) > 0
                for row in mapped
            ),
            f"mapped={len(mapped)};minimum_width={min(float(row['midpoint_energy_width']) for row in mapped)}",
        ),
        validation_row(
            "all_observed_geometric_poles_have_one_analytic_owner",
            pole_ownership_complete,
            f"assigned={branch_diagnostics['assigned_inside_support_geometric_pole_rows']}/{branch_diagnostics['total_inside_support_geometric_pole_rows']};unmatched={len(branch_diagnostics['unmatched_geometric_pole_rows'])};missing_classifications={len(branch_diagnostics['missing_resolved_classification_rows'])}",
        ),
        validation_row(
            "material_branch_support_endpoints_are_event_owned",
            material_event_pairs_valid,
            "B01:E01-E04;B02:E07-E08;B03:E02-E05;B04:E03-E06",
        ),
        validation_row(
            "H_and_G_are_closed_but_W3_remains_open",
            endpoint_result.get("validation_passed") is True
            and endpoint_result.get("claim_boundary", {}).get(
                "valid_for_D4_numeric_G3_bound"
            )
            is True
            and endpoint_result.get("claim_boundary", {}).get(
                "valid_for_D4_numeric_W3_bound"
            )
            is False,
            endpoint_result.get("decision"),
        ),
        validation_row(
            "finite_W3_owner_reduction_has_all_three_open_families",
            {
                row["owner_id"]
                for row in decomposition
                if row["included_in_W"] is True
            }
            == {
                "W_AWAY_REGULAR_2D",
                "W_AWAY_POLE_PRIMITIVE_1D",
                "W_EVENT_LOCAL_REMAINDER",
            },
            "regular_2D|pole_primitive_1D|event_local_remainder",
        ),
        validation_row(
            "formalization_workbench_remains_unmodified",
            endpoint_result.get("formalization_workbench_modified_file_count") == 0,
            endpoint_result.get("formalization_workbench_modified_file_count"),
        ),
        validation_row(
            "claim_boundary_keeps_numeric_W3_and_broader_claims_false",
            True,
            "atlas and owner reduction only; no numeric W3 or broader claim",
        ),
    ]
    validation_passed = all(row["passed"] for row in validations)
    for row in (*atlas, *mapped, *branches, *decomposition):
        row[CLAIM_ATLAS] = validation_passed
        row[CLAIM_OWNERS] = validation_passed
        row[CLAIM_REDUCTION] = validation_passed
        for claim in OPEN_CLAIMS:
            row[claim] = False
    registered_sources = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path),
            CLAIM_ATLAS: validation_passed,
            CLAIM_OWNERS: validation_passed,
            CLAIM_REDUCTION: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        }
        for path in required
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": validation_passed,
        "failed_validation_gates": [
            row["gate"] for row in validations if not row["passed"]
        ],
        "decision": (
            "PARENT_FROZEN_MAPPED_ATLAS_AND_W3_OWNER_REDUCTION_CERTIFIED__PROCEED_TO_INTERVAL_ENCLOSURES"
            if validation_passed
            else "PARENT_FROZEN_MAPPED_ATLAS_AND_W3_OWNER_REDUCTION_BLOCKED"
        ),
        "parent_panel_count": len(panels),
        "parent_contract_row_count": len(contract),
        "parent_active_contract_row_count": len(active_contract),
        "frozen_x_cell_count": len(atlas),
        "away_x_cell_count": sum(row["region_class"] == "AWAY" for row in atlas),
        "event_x_cell_count": sum(
            row["region_class"] == "EVENT_TUBE" for row in atlas
        ),
        "mapped_active_cell_count": len(mapped),
        "mapped_away_cell_count": sum(
            row["region_class"] == "AWAY" for row in mapped
        ),
        "mapped_event_cell_count": sum(
            row["region_class"] == "EVENT_TUBE" for row in mapped
        ),
        "maximum_parent_chamber_boundary_reproduction_error": reproduction_error,
        "minimum_parent_representative_energy_width": parent_minimum_width,
        "minimum_mapped_midpoint_energy_width": min(
            float(row["midpoint_energy_width"]) for row in mapped
        ),
        "minimum_mapped_midpoint_jacobian": min(
            float(row["midpoint_jacobian"]) for row in mapped
        ),
        "pole_branch_owner_count": len(branches),
        **branch_diagnostics,
        "open_W3_owner_ids": [
            row["owner_id"]
            for row in decomposition
            if row["included_in_W"] is True
        ],
        "claim_boundary": {
            CLAIM_ATLAS: validation_passed,
            CLAIM_OWNERS: validation_passed,
            CLAIM_REDUCTION: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
        "remaining_obstruction": "interval-enclose the frozen regular 2D cells, exact pole-primitive 1D owners, and desingularized event-local remainders; sum them to obtain numeric W3",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    if not dry_run:
        output = output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        atomic_csv(output / "D4_parent_frozen_x_atlas.csv", atlas)
        atomic_csv(output / "D4_parent_frozen_mapped_cells.csv", mapped)
        atomic_csv(output / "D4_material_pole_branch_ownership.csv", branches)
        atomic_csv(output / "D4_W3_owner_decomposition.csv", decomposition)
        atomic_csv(output / "D4_parent_frozen_atlas_validation.csv", validations)
        atomic_csv(output / "source_register.csv", registered_sources)
        atomic_csv(VALIDATION, validations)
        atomic_json(output / "D4_parent_frozen_atlas_result.json", result)
        atomic_json(
            output / "status.json",
            {
                "checkpoint": CHECKPOINT,
                "state": "complete" if validation_passed else "blocked",
                "decision": result["decision"],
                "updated_utc": result["updated_utc"],
            },
        )
        render_document(result, branches)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    result = run(arguments.output, arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
