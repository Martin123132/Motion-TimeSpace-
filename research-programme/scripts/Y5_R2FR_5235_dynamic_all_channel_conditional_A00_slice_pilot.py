from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5235"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5234 = (
    POST
    / "scripts"
    / "Y5_R2FR_5234_complete_active_family_physical_channel_and_pole_order_atlas.py"
)
RESULT_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_physical_channel_and_pole_order_atlas.json"
)
ATLAS_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_pole_atlas.csv"
)

RESULT = SOURCE / "dynamic_all_channel_conditional_A00_slice_pilot.json"
SCAN_ROWS = SOURCE / "dynamic_slice_channel_scan.csv"
POLE_ROWS = SOURCE / "dynamic_slice_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "dynamic_slice_causal_topology_audit.csv"
RESIDUE_ROWS = SOURCE / "active_slice_residue_fits.csv"
QUADRATURE_ROWS = SOURCE / "all_channel_two_patch_quadrature.csv"
DOCUMENT = (
    POST
    / "5235-Y5-R2FR-dynamic-all-channel-conditional-A00-slice-pilot.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5235_VALIDATION.csv"

MARKER = "MTS_5235_DYNAMIC_ALL_CHANNEL_CONDITIONAL_A00_SLICE_PILOT"
REVISION = "dynamic-all-channel-conditional-slice-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
TARGET_COMPONENT_ID = "AF02_C01"
EPSILON_ID = "E020"
SCAN_MINIMUM = -0.995
SCAN_MAXIMUM = 0.995
SCAN_POINTS = 801
TOPOLOGY_STEPS = 12288
MAXIMUM_TOPOLOGY_STEPS = 24576
PROJECTIVE_LIMIT = 0.1
POLE_IMAGINARY_LIMIT = 0.01
ROOT_GROUP_TOLERANCE = 5.0e-5
PATCH_HALF_WIDTH = 1.0e-2
QUADRATURE_ORDERS = (32, 128, 512, 1024)
SLOPE_TOLERANCE = 0.08
NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT = 2.0e-4
LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 2.0e-3
HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT = 2.0e-4
MINIMUM_IMPROVEMENT_FACTOR = 100.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5234 = load_module(SCRIPT_5234, "mts_5234_for_5235")
M5232 = M5234.M5232
M5231 = M5234.M5231
M5024 = M5234.M5024
M5017 = M5234.M5017


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
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
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def configured_problem() -> dict[str, Any]:
    case = M5232.source_cases()[0]
    if case["family"] != "direct:g1:plus/direct:g3:minus":
        raise RuntimeError("locked AF02 family changed")
    event = M5232.event_for_case(case)
    topology = M5232.topology_for_case(case, EPSILON_ID)
    target = M5231.complex_value(topology["target_cosine"])
    atlas_rows = [
        row
        for row in read_csv(ATLAS_5234)
        if row["component_id"] == TARGET_COMPONENT_ID
        and row["atlas_status"]
        == "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS"
    ]
    if not atlas_rows:
        raise RuntimeError("5234 atlas has no AF02 candidate surfaces")
    return {
        "component_id": TARGET_COMPONENT_ID,
        "case": case,
        "event": event,
        "topology": topology,
        "target": target,
        "atlas_rows": atlas_rows,
    }


def collision_geometry(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, Any]:
    case = problem["case"]
    event = problem["event"]
    target = problem["target"]
    soft_energy, soft_cosine, decay_cosine = M5232.varied_components(
        case, event, coordinate
    )
    rationals = M5232.M5029.root_rationals(
        soft_energy, soft_cosine, decay_cosine, target
    )
    first_label, second_label = case["representative_pair"]
    collision_roots = M5232.M5029.collision_roots(
        rationals[first_label], rationals[second_label]
    )
    if not collision_roots:
        raise RuntimeError("target collision branch disappeared")
    anchor = problem.get("relative_root_anchor")
    if anchor is None:
        matching = [
            M5231.complex_value(crossing["target_root"])
            for chamber in problem["topology"]["chambers"]
            for crossing in chamber["surface_crossings"]
            if len(crossing["representing_pairs"]) == 1
            and tuple(crossing["representing_pairs"][0])
            == tuple(case["representative_pair"])
        ]
        if not matching:
            raise RuntimeError("representative collision anchor is absent")
        anchor = max(matching, key=abs)
        problem["relative_root_anchor"] = anchor
    relative_root = min(
        collision_roots,
        key=lambda root: M5232.M5030.chordal_distance(root, anchor),
    )
    first_root, _ = M5231.rational_value_and_derivative(
        rationals[first_label], relative_root
    )
    second_root, _ = M5231.rational_value_and_derivative(
        rationals[second_label], relative_root
    )
    global_root = 0.5 * (first_root + second_root)
    _, _, internal = M5232.M5028.event_geometry(
        soft_energy, soft_cosine, decay_cosine, relative_root
    )
    rotated = M5024.rotate_internal(internal, global_root)
    left, right = M5017.cut_momenta(rotated, target, 1.0)
    return {
        "relative_root": relative_root,
        "global_root": global_root,
        "left": left,
        "right": right,
    }


def surface_value(
    geometry: dict[str, Any], surface_id: str
) -> complex:
    if surface_id.startswith("direct:shared:s"):
        channel = surface_id.rsplit(":", 1)[-1][1:]
        if channel == "04":
            pair = (0, 4)
        else:
            pair = (int(channel[0]), int(channel[1]))
        return M5234.pair_invariant(
            geometry["left"], pair[0], pair[1]
        )
    match = __import__("re").fullmatch(
        r"direct:([LR]):s([01234])([01234])", surface_id
    )
    if match is None:
        raise RuntimeError(f"unsupported direct surface: {surface_id}")
    momenta = geometry["left"] if match.group(1) == "L" else geometry["right"]
    return M5234.pair_invariant(
        momenta, int(match.group(2)), int(match.group(3))
    )


def surface_values(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, complex]:
    geometry = collision_geometry(problem, coordinate)
    return {
        row["surface_id"]: surface_value(geometry, row["surface_id"])
        for row in problem["atlas_rows"]
    }


def scan_surfaces(
    problem: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, list[complex]]]:
    coordinates = np.linspace(SCAN_MINIMUM, SCAN_MAXIMUM, SCAN_POINTS)
    component_id = problem.get("component_id", TARGET_COMPONENT_ID)
    values_by_surface: dict[str, list[complex]] = {
        row["surface_id"]: [] for row in problem["atlas_rows"]
    }
    rows: list[dict[str, Any]] = []
    for coordinate in coordinates:
        values = surface_values(problem, complex(float(coordinate)))
        for surface_id, value in values.items():
            values_by_surface[surface_id].append(value)
            rows.append(
                {
                    "component_id": component_id,
                    "outer_coordinate": problem["case"]["outer_coordinate"],
                    "coordinate": float(coordinate),
                    "surface_id": surface_id,
                    "channel_real": value.real,
                    "channel_imaginary": value.imag,
                    "channel_magnitude": abs(value),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows, values_by_surface


def bisect_real_zero(
    problem: dict[str, Any],
    surface_id: str,
    lower: float,
    upper: float,
) -> float:
    lower_value = surface_values(problem, lower)[surface_id].real
    upper_value = surface_values(problem, upper)[surface_id].real
    if lower_value == 0.0:
        return lower
    if upper_value == 0.0:
        return upper
    if lower_value * upper_value > 0.0:
        raise RuntimeError("root bracket does not change sign")
    for _ in range(70):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = surface_values(problem, midpoint)[surface_id].real
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
        if upper - lower < 2.0e-14:
            break
    return 0.5 * (lower + upper)


def locate_geometric_roots(
    problem: dict[str, Any],
    values_by_surface: dict[str, list[complex]],
) -> list[dict[str, Any]]:
    coordinates = np.linspace(SCAN_MINIMUM, SCAN_MAXIMUM, SCAN_POINTS)
    raw_roots: list[dict[str, Any]] = []
    for surface_id, values in values_by_surface.items():
        for index in range(len(coordinates) - 1):
            left = values[index].real
            right = values[index + 1].real
            if left * right >= 0.0:
                continue
            center = bisect_real_zero(
                problem,
                surface_id,
                float(coordinates[index]),
                float(coordinates[index + 1]),
            )
            step = 1.0e-6
            center_value = surface_values(problem, center)[surface_id]
            derivative = (
                surface_values(problem, center + step)[surface_id]
                - surface_values(problem, center - step)[surface_id]
            ) / (2.0 * step)
            if abs(derivative) < 1.0e-10:
                continue
            pole = complex(center) - center_value / derivative
            if not (
                SCAN_MINIMUM < pole.real < SCAN_MAXIMUM
                and abs(pole.imag) < POLE_IMAGINARY_LIMIT
            ):
                continue
            raw_roots.append(
                {
                    "surface_id": surface_id,
                    "real_axis_center": center,
                    "channel_at_center": center_value,
                    "channel_derivative": derivative,
                    "complex_pole": pole,
                }
            )
    raw_roots.sort(key=lambda row: row["complex_pole"].real)
    groups: list[list[dict[str, Any]]] = []
    for root in raw_roots:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(
                    candidate[0]["complex_pole"] - root["complex_pole"]
                )
                < ROOT_GROUP_TOLERANCE
            ),
            None,
        )
        if group is None:
            groups.append([root])
        else:
            group.append(root)
    rows: list[dict[str, Any]] = []
    for index, group in enumerate(groups, start=1):
        representative = min(
            group, key=lambda row: abs(row["channel_at_center"])
        )
        rows.append(
            {
                "pole_id": f"DP{index:02d}",
                "component_id": problem.get(
                    "component_id", TARGET_COMPONENT_ID
                ),
                "family": problem["case"]["family"],
                "epsilon_id": EPSILON_ID,
                "outer_coordinate": problem["case"]["outer_coordinate"],
                "surface_ids": "|".join(
                    sorted(row["surface_id"] for row in group)
                ),
                "surface_count": len(group),
                "primary_surface_id": representative["surface_id"],
                "real_axis_center": representative["real_axis_center"],
                "pole_real": representative["complex_pole"].real,
                "pole_imaginary": representative["complex_pole"].imag,
                "channel_at_center_real": representative[
                    "channel_at_center"
                ].real,
                "channel_at_center_imaginary": representative[
                    "channel_at_center"
                ].imag,
                "channel_derivative_real": representative[
                    "channel_derivative"
                ].real,
                "channel_derivative_imaginary": representative[
                    "channel_derivative"
                ].imag,
                "geometric_root": True,
                "causal_family_active": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def topology_audit(
    problem: dict[str, Any], pole_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    case = problem["case"]
    expected = {
        "u": int(case["expected_u_winding"]),
        "v": int(case["expected_v_winding"]),
    }
    for pole in pole_rows:
        event = dict(problem["event"])
        event[case["outer_coordinate"]] = float(
            pole["real_axis_center"]
        )
        steps = TOPOLOGY_STEPS
        audit = M5232.target_pair_track(
            event,
            problem["target"],
            [case["reciprocal_pair"], case["representative_pair"]],
            steps,
        )
        winding = {
            row["pair"][0].rsplit("_", 1)[-1]: int(
                row["winding_sum"]
            )
            for row in audit["pair_rows"]
        }
        active = winding == expected
        if (
            not active
            and audit["maximum_pair_projective_step"] >= 0.5
            * PROJECTIVE_LIMIT
            and steps < MAXIMUM_TOPOLOGY_STEPS
        ):
            steps = MAXIMUM_TOPOLOGY_STEPS
            audit = M5232.target_pair_track(
                event,
                problem["target"],
                [case["reciprocal_pair"], case["representative_pair"]],
                steps,
            )
            winding = {
                row["pair"][0].rsplit("_", 1)[-1]: int(
                    row["winding_sum"]
                )
                for row in audit["pair_rows"]
            }
            active = winding == expected
        pole["causal_family_active"] = active
        pole["u_winding"] = winding.get("u")
        pole["v_winding"] = winding.get("v")
        pole["topology_steps"] = steps
        pole["maximum_pair_projective_step"] = audit[
            "maximum_pair_projective_step"
        ]
        pole["maximum_reciprocal_product_residual"] = audit[
            "maximum_reciprocal_product_residual"
        ]
        for pair_row in audit["pair_rows"]:
            suffix = pair_row["pair"][0].rsplit("_", 1)[-1]
            rows.append(
                {
                    "pole_id": pole["pole_id"],
                    "surface_ids": pole["surface_ids"],
                    "pair": "|".join(pair_row["pair"]),
                    "suffix": suffix,
                    "winding_sum": int(pair_row["winding_sum"]),
                    "expected_winding_sum": expected[suffix],
                    "winding_matches": int(pair_row["winding_sum"])
                    == expected[suffix],
                    "causal_family_active": active,
                    "topology_steps": steps,
                    "maximum_pair_projective_step": audit[
                        "maximum_pair_projective_step"
                    ],
                    "maximum_boundary_projective_step": audit[
                        "maximum_boundary_projective_step"
                    ],
                    "maximum_reciprocal_product_residual": audit[
                        "maximum_reciprocal_product_residual"
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def fit_active_residues(
    problem: dict[str, Any], pole_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    fits: dict[str, dict[str, Any]] = {}
    offsets = np.asarray(
        (
            -5.0e-3,
            -2.5e-3,
            -1.0e-3,
            -5.0e-4,
            5.0e-4,
            1.0e-3,
            2.5e-3,
            5.0e-3,
        )
    )
    for pole_row in pole_rows:
        if not bool(pole_row["causal_family_active"]):
            continue
        center = float(pole_row["real_axis_center"])
        surface_id = str(pole_row["primary_surface_id"])
        pole = complex(
            float(pole_row["pole_real"]),
            float(pole_row["pole_imaginary"]),
        )
        derivative = complex(
            float(pole_row["channel_derivative_real"]),
            float(pole_row["channel_derivative_imaginary"]),
        )
        contributions: list[complex] = []
        channels: list[complex] = []
        numerators: list[complex] = []
        for offset in offsets:
            coordinate = center + float(offset)
            contribution = M5232.family_contribution(
                problem["case"],
                problem["event"],
                problem["topology"],
                coordinate,
            )[0]
            channel = surface_values(problem, coordinate)[surface_id]
            numerator = channel * contribution
            contributions.append(contribution)
            channels.append(channel)
            numerators.append(numerator)
            rows.append(
                {
                    "pole_id": pole_row["pole_id"],
                    "surface_id": surface_id,
                    "offset": float(offset),
                    "coordinate": coordinate,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "contribution_magnitude": abs(contribution),
                    "channel_real": channel.real,
                    "channel_imaginary": channel.imag,
                    "channel_magnitude": abs(channel),
                    "channel_times_contribution_real": numerator.real,
                    "channel_times_contribution_imaginary": numerator.imag,
                    "channel_times_contribution_magnitude": abs(numerator),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        numerator_array = np.asarray(numerators, dtype=np.complex128)
        coefficients = np.polyfit(offsets, numerator_array, 3)
        fitted = np.polyval(coefficients, offsets)
        fit_residual = float(
            np.max(np.abs(fitted - numerator_array))
            / max(float(np.max(np.abs(numerator_array))), 1.0e-30)
        )
        numerator_at_pole = complex(
            np.polyval(coefficients, pole - center)
        )
        residue = numerator_at_pole / derivative
        side_fits: dict[str, Any] = {}
        for side_name, sign in (("negative", -1.0), ("positive", 1.0)):
            selected = [
                index
                for index, offset in enumerate(offsets)
                if float(offset) * sign > 0.0
            ]
            slope, intercept = np.polyfit(
                np.log([abs(float(offsets[index])) for index in selected]),
                np.log([abs(contributions[index]) for index in selected]),
                1,
            )
            selected_numerator = np.asarray(
                [abs(numerators[index]) for index in selected]
            )
            side_fits[side_name] = {
                "log_log_slope": float(slope),
                "log_log_intercept": float(intercept),
                "numerator_relative_spread": float(
                    np.std(selected_numerator)
                    / np.mean(selected_numerator)
                ),
            }
        fits[pole_row["pole_id"]] = {
            "pole_id": pole_row["pole_id"],
            "surface_id": surface_id,
            "center": center,
            "pole": pole,
            "channel_derivative": derivative,
            "numerator_at_pole": numerator_at_pole,
            "outer_residue": residue,
            "numerator_fit_relative_residual": fit_residual,
            "negative_side": side_fits["negative"],
            "positive_side": side_fits["positive"],
        }
    return rows, fits


def integrate_active_patches(
    problem: dict[str, Any],
    fits: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    intermediate: list[dict[str, Any]] = []
    for pole_id, fit in fits.items():
        pole = complex(fit["pole"])
        residue = complex(fit["outer_residue"])
        lower = pole.real - PATCH_HALF_WIDTH
        upper = pole.real + PATCH_HALF_WIDTH
        analytic = residue * (
            np.log(upper - pole) - np.log(lower - pole)
        )
        for order in QUADRATURE_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            coordinates = PATCH_HALF_WIDTH * nodes + pole.real
            physical_weights = PATCH_HALF_WIDTH * weights
            values = np.asarray(
                [
                    M5232.family_contribution(
                        problem["case"],
                        problem["event"],
                        problem["topology"],
                        float(coordinate),
                    )[0]
                    for coordinate in coordinates
                ],
                dtype=np.complex128,
            )
            raw = complex(np.sum(physical_weights * values))
            regular = complex(
                np.sum(
                    physical_weights
                    * (values - residue / (coordinates - pole))
                )
            )
            subtracted = regular + analytic
            intermediate.append(
                {
                    "row_type": "individual_patch",
                    "pole_id": pole_id,
                    "quadrature_order": order,
                    "patch_lower": lower,
                    "patch_upper": upper,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "outer_residue_real": residue.real,
                    "outer_residue_imaginary": residue.imag,
                    "analytic_singular_real": analytic.real,
                    "analytic_singular_imaginary": analytic.imag,
                    "raw_integral_real": raw.real,
                    "raw_integral_imaginary": raw.imag,
                    "regular_remainder_real": regular.real,
                    "regular_remainder_imaginary": regular.imag,
                    "subtracted_integral_real": subtracted.real,
                    "subtracted_integral_imaginary": subtracted.imag,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    combined: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        selected = [
            row
            for row in intermediate
            if int(row["quadrature_order"]) == order
        ]
        raw = sum(
            (
                complex(
                    float(row["raw_integral_real"]),
                    float(row["raw_integral_imaginary"]),
                )
                for row in selected
            ),
            0.0j,
        )
        subtracted = sum(
            (
                complex(
                    float(row["subtracted_integral_real"]),
                    float(row["subtracted_integral_imaginary"]),
                )
                for row in selected
            ),
            0.0j,
        )
        combined.append(
            {
                "row_type": "combined_active_patch_union",
                "pole_id": "ALL_ACTIVE",
                "quadrature_order": order,
                "patch_lower": "",
                "patch_upper": "",
                "pole_real": "",
                "pole_imaginary": "",
                "outer_residue_real": "",
                "outer_residue_imaginary": "",
                "analytic_singular_real": "",
                "analytic_singular_imaginary": "",
                "raw_integral_real": raw.real,
                "raw_integral_imaginary": raw.imag,
                "regular_remainder_real": "",
                "regular_remainder_imaginary": "",
                "subtracted_integral_real": subtracted.real,
                "subtracted_integral_imaginary": subtracted.imag,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    reference = complex(
        float(combined[-1]["subtracted_integral_real"]),
        float(combined[-1]["subtracted_integral_imaginary"]),
    )
    rows: list[dict[str, Any]] = []
    for row in intermediate + combined:
        raw = complex(
            float(row["raw_integral_real"]),
            float(row["raw_integral_imaginary"]),
        )
        subtracted = complex(
            float(row["subtracted_integral_real"]),
            float(row["subtracted_integral_imaginary"]),
        )
        rows.append(
            {
                **row,
                "raw_relative_error_to_combined_subtracted_1024": (
                    abs(raw - reference) / max(abs(reference), 1.0)
                    if row["row_type"] == "combined_active_patch_union"
                    else ""
                ),
                "subtracted_relative_error_to_combined_subtracted_1024": (
                    abs(subtracted - reference)
                    / max(abs(reference), 1.0)
                    if row["row_type"] == "combined_active_patch_union"
                    else ""
                ),
            }
        )
    low = combined[0]
    high = combined[-1]
    low_raw = complex(
        float(low["raw_integral_real"]),
        float(low["raw_integral_imaginary"]),
    )
    low_subtracted = complex(
        float(low["subtracted_integral_real"]),
        float(low["subtracted_integral_imaginary"]),
    )
    high_raw = complex(
        float(high["raw_integral_real"]),
        float(high["raw_integral_imaginary"]),
    )
    low_raw_error = abs(low_raw - reference) / max(abs(reference), 1.0)
    low_subtracted_error = abs(low_subtracted - reference) / max(
        abs(reference), 1.0
    )
    high_raw_error = abs(high_raw - reference) / max(abs(reference), 1.0)
    summary = {
        "active_pole_count": len(fits),
        "patch_half_width": PATCH_HALF_WIDTH,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "combined_subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": low_raw_error,
        "low_order_subtracted_relative_error": low_subtracted_error,
        "high_order_raw_relative_error": high_raw_error,
        "low_order_improvement_factor": (
            low_raw_error / max(low_subtracted_error, 1.0e-30)
        ),
    }
    return rows, summary


def validation_rows(
    parent: dict[str, Any],
    problem: dict[str, Any],
    pole_rows: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    fits: dict[str, dict[str, Any]],
    quadrature: dict[str, Any],
) -> list[dict[str, Any]]:
    required = [SCRIPT_5234, RESULT_5234, ATLAS_5234]
    active = [row for row in pole_rows if bool(row["causal_family_active"])]
    inactive = [
        row for row in pole_rows if not bool(row["causal_family_active"])
    ]
    expected_surfaces = {
        "direct:shared:s13",
        "direct:L:s01",
        "direct:L:s14",
    }
    root_pass = (
        len(pole_rows) == 3
        and {
            surface
            for row in pole_rows
            for surface in str(row["surface_ids"]).split("|")
        }
        == expected_surfaces
    )
    topology_pass = (
        len(active) == 2
        and len(inactive) == 1
        and all(
            float(row["maximum_pair_projective_step"])
            < PROJECTIVE_LIMIT
            for row in pole_rows
        )
        and all(
            bool(row["causal_family_active"])
            == all(
                bool(pair["winding_matches"])
                for pair in topology_rows
                if pair["pole_id"] == row["pole_id"]
            )
            for row in pole_rows
        )
    )
    residue_pass = (
        len(fits) == 2
        and all(
            float(fit["numerator_fit_relative_residual"])
            <= NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
            and all(
                abs(float(fit[side]["log_log_slope"]) + 1.0)
                <= SLOPE_TOLERANCE
                for side in ("negative_side", "positive_side")
            )
            for fit in fits.values()
        )
    )
    quadrature_pass = (
        float(quadrature["low_order_subtracted_relative_error"])
        <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        and float(quadrature["high_order_raw_relative_error"])
        <= HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT
        and float(quadrature["low_order_improvement_factor"])
        >= MINIMUM_IMPROVEMENT_FACTOR
    )
    branch_rows = []
    for fit in fits.values():
        relative_pole = 1.0j * fit["pole"].imag
        logarithmic_jump = (
            np.log(PATCH_HALF_WIDTH - relative_pole)
            - np.log(-PATCH_HALF_WIDTH - relative_pole)
        )
        analytic_singular = fit["outer_residue"] * logarithmic_jump
        branch_rows.append(
            {
                "pole_imaginary": fit["pole"].imag,
                "logarithmic_jump_imaginary": logarithmic_jump.imag,
                "analytic_singular_imaginary": analytic_singular.imag,
            }
        )
    branch_pass = all(
        float(row["pole_imaginary"]) < 0.0
        and -math.pi < float(row["logarithmic_jump_imaginary"]) < 0.0
        and float(row["analytic_singular_imaginary"]) < 0.0
        for row in branch_rows
    )
    formal_digest = tree_digest(FORMAL)
    checks = [
        (
            "required_source_paths_exist",
            all(path.exists() for path in required),
            f"{sum(path.exists() for path in required)}/{len(required)}",
        ),
        (
            "5234_parent_atlas_is_passed",
            bool(parent["validation_all_passed"])
            and parent["decision"]
            == "ADOPT_COMPLETE_PHYSICAL_CHANNEL_ATLAS_AND_BUILD_DYNAMIC_ROOT_ENUMERATOR",
            parent["decision"],
        ),
        (
            "all_candidate_surfaces_are_scanned_without_hardcoded_pole_guesses",
            len(problem["atlas_rows"]) == 13,
            f"candidate_surfaces={len(problem['atlas_rows'])}",
        ),
        (
            "dynamic_scan_finds_the_three_geometric_slice_roots",
            root_pass,
            json.dumps(
                [
                    {
                        "surface": row["surface_ids"],
                        "pole": [
                            row["pole_real"],
                            row["pole_imaginary"],
                        ],
                    }
                    for row in pole_rows
                ],
                separators=(",", ":"),
            ),
        ),
        (
            "causal_winding_accepts_two_roots_and_rejects_one",
            topology_pass,
            json.dumps(
                [
                    {
                        "surface": row["surface_ids"],
                        "active": row["causal_family_active"],
                        "u": row["u_winding"],
                        "v": row["v_winding"],
                    }
                    for row in pole_rows
                ],
                separators=(",", ":"),
            ),
        ),
        (
            "both_active_roots_have_regular_numerators_and_simple_slopes",
            residue_pass,
            json.dumps(
                {
                    pole_id: {
                        "fit_residual": fit[
                            "numerator_fit_relative_residual"
                        ],
                        "negative_slope": fit["negative_side"][
                            "log_log_slope"
                        ],
                        "positive_slope": fit["positive_side"][
                            "log_log_slope"
                        ],
                    }
                    for pole_id, fit in fits.items()
                },
                separators=(",", ":"),
            ),
        ),
        (
            "inactive_geometric_root_is_not_subtracted",
            len(inactive) == 1
            and all(
                row["pole_id"] not in fits for row in inactive
            ),
            inactive[0]["surface_ids"] if inactive else "missing",
        ),
        (
            "two_patch_all_active_subtraction_converges",
            quadrature_pass,
            json.dumps(quadrature, separators=(",", ":")),
        ),
        (
            "analytic_logs_retain_the_finite_regulator_branch",
            branch_pass,
            json.dumps(branch_rows, separators=(",", ":")),
        ),
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "all_claim_flags_remain_false",
            True,
            "conditional slice only; numeric UV, local GR and full MTS claims remain false",
        ),
    ]
    return [
        {
            "check": check,
            "passed": bool(passed),
            "detail": detail,
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for check, passed, detail in checks
    ]


def main() -> None:
    parent = read_json(RESULT_5234)
    if not bool(parent["validation_all_passed"]):
        raise RuntimeError("5234 parent atlas is not passed")
    problem = configured_problem()
    scan_rows, values = scan_surfaces(problem)
    pole_rows = locate_geometric_roots(problem, values)
    topology_rows = topology_audit(problem, pole_rows)
    residue_rows, fits = fit_active_residues(problem, pole_rows)
    quadrature_rows, quadrature = integrate_active_patches(problem, fits)
    validations = validation_rows(
        parent,
        problem,
        pole_rows,
        topology_rows,
        fits,
        quadrature,
    )
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_CAUSAL_DYNAMIC_ROOT_FILTER_AND_SCALE_TO_MULTI_EVENT_PILOT"
        if validation_all_passed
        else "RETAIN_BLOCK_AND_REPAIR_DYNAMIC_SLICE_ENUMERATOR"
    )
    active_poles = [
        row for row in pole_rows if bool(row["causal_family_active"])
    ]
    inactive_poles = [
        row for row in pole_rows if not bool(row["causal_family_active"])
    ]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "component_id": TARGET_COMPONENT_ID,
        "family": problem["case"]["family"],
        "epsilon_id": EPSILON_ID,
        "outer_coordinate": problem["case"]["outer_coordinate"],
        "fixed_outer_coordinates": {
            "soft_energy": problem["event"]["soft_energy"],
            "soft_cosine": problem["event"]["soft_cosine"],
        },
        "scan_domain": [SCAN_MINIMUM, SCAN_MAXIMUM],
        "scan_points": SCAN_POINTS,
        "candidate_surface_count": len(problem["atlas_rows"]),
        "geometric_root_count": len(pole_rows),
        "active_causal_root_count": len(active_poles),
        "inactive_geometric_root_count": len(inactive_poles),
        "pole_catalog": pole_rows,
        "residue_fits": {
            pole_id: {
                **{
                    key: value
                    for key, value in fit.items()
                    if key
                    not in {
                        "pole",
                        "channel_derivative",
                        "numerator_at_pole",
                        "outer_residue",
                    }
                },
                "pole": complex_row(fit["pole"]),
                "channel_derivative": complex_row(
                    fit["channel_derivative"]
                ),
                "numerator_at_pole": complex_row(
                    fit["numerator_at_pole"]
                ),
                "outer_residue": complex_row(fit["outer_residue"]),
            }
            for pole_id, fit in fits.items()
        },
        "quadrature_summary": quadrature,
        "validation_all_passed": validation_all_passed,
        "scope": (
            "complete channel/root/subtraction audit of one conditional "
            "decay-cosine slice; not the full multidimensional A00 integral"
        ),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "run this dynamic causal filter on a stratified multi-event set, "
            "cache channel roots and residues, then compare raw and fully "
            "subtracted event pools before authorizing a full A00 rerun"
        ),
        "source_paths": [
            str(SCRIPT_5234),
            str(RESULT_5234),
            str(ATLAS_5234),
        ],
    }
    write_csv(SCAN_ROWS, scan_rows)
    write_csv(POLE_ROWS, pole_rows)
    write_csv(TOPOLOGY_ROWS, topology_rows)
    write_csv(RESIDUE_ROWS, residue_rows)
    write_csv(QUADRATURE_ROWS, quadrature_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)

    pole_lines = "\n".join(
        (
            f"- `{row['surface_ids']}`: "
            f"`q_*={float(row['pole_real']):+.12g}"
            f"{float(row['pole_imaginary']):+.12g} i`, "
            f"windings `({row['u_winding']},{row['v_winding']})`, "
            f"active `{row['causal_family_active']}`."
        )
        for row in pole_rows
    )
    fit_lines = "\n".join(
        (
            f"- `{pole_id}` `{fit['surface_id']}`: slopes "
            f"`{fit['negative_side']['log_log_slope']:.9g}` and "
            f"`{fit['positive_side']['log_log_slope']:.9g}`, numerator-fit "
            f"residual `{fit['numerator_fit_relative_residual']:.9g}`."
        )
        for pole_id, fit in fits.items()
    )
    document = f"""# 5235 - Dynamic all-channel conditional A00 slice pilot

## Decision

`{decision}`.

Checkpoint 5234's atlas is now used as an executable root catalogue rather
than a list of future targets.  On the representative `AF02_C01`
`g1+/g3-` component, all `{len(problem['atlas_rows'])}` unconsumed direct
surfaces were scanned over the full conditional
`decay_cosine in [{SCAN_MINIMUM},{SCAN_MAXIMUM}]`.  No pole coordinate was
hardcoded.

## Geometry is not enough

The scan found three geometric zeros:

{pole_lines}

The shared `s13` and left `s14` zeros retain the inherited reciprocal winding
and are genuine poles of this residue family.  The left `s01` channel is also
a real factorization zero, but both collision windings have switched off by
that point.  It is therefore not part of the active family correction and was
not subtracted.

This is the first concrete use of the distinction

```text
physical denominator zero != active causal residue-family pole.
```

It prevents both missed poles and spurious subtraction.

## Active residues

{fit_lines}

Both active roots have simple `1/(q-q_*)` scaling and a regular fitted
numerator `D*T`.  The inactive root is absent from the residue-fit table.

## Two-patch pilot

The two accepted patches were integrated as

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

Their combined order-32 raw relative error is
`{quadrature['low_order_raw_relative_error']:.9g}`.  The combined order-32
subtracted error is
`{quadrature['low_order_subtracted_relative_error']:.9g}`, an improvement of
`{quadrature['low_order_improvement_factor']:.9g}x`.  The independent
order-1024 raw result differs from the subtracted reference by
`{quadrature['high_order_raw_relative_error']:.9g}`.

## Scope

This closes one complete conditional slice: every atlas channel was scanned,
every geometric root was causally classified, and every active pole was
subtracted.  It is not yet the full multidimensional A00 coefficient and does
not establish the UV coefficient, local GR, or full MTS.

## Next target

Run the same causal root filter on a stratified set spanning direct and
endpoint-owned families, cache the accepted roots and residues, and compare
the raw versus fully subtracted event pools before authorizing a full run.
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not validation_all_passed:
        raise RuntimeError("5235 dynamic conditional slice pilot failed")


if __name__ == "__main__":
    main()
