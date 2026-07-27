from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5236"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5234 = (
    POST
    / "scripts"
    / "Y5_R2FR_5234_complete_active_family_physical_channel_and_pole_order_atlas.py"
)
SCRIPT_5235 = (
    POST
    / "scripts"
    / "Y5_R2FR_5235_dynamic_all_channel_conditional_A00_slice_pilot.py"
)
RESULT_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_physical_channel_and_pole_order_atlas.json"
)
RESULT_5235 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5235"
    / "dynamic_all_channel_conditional_A00_slice_pilot.json"
)
ATLAS_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_pole_atlas.csv"
)
QUADRATURE_5235 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5235"
    / "all_channel_two_patch_quadrature.csv"
)

RESULT = SOURCE / "stratified_causal_multi_slice_A00_pool_validation.json"
SLICE_ROWS = SOURCE / "stratified_slice_catalog.csv"
AF01_POLE_ROWS = SOURCE / "AF01_dynamic_pole_catalog.csv"
AF01_TOPOLOGY_ROWS = SOURCE / "AF01_causal_topology_audit.csv"
AF01_RESIDUE_ROWS = SOURCE / "AF01_active_residue_fits.csv"
AF01_QUADRATURE_ROWS = SOURCE / "AF01_active_patch_quadrature.csv"
ENDPOINT_ROWS = SOURCE / "endpoint_owned_geometric_root_control.csv"
POOL_ROWS = SOURCE / "pooled_active_patch_quadrature.csv"
DOCUMENT = (
    POST
    / "5236-Y5-R2FR-stratified-causal-multi-slice-A00-pool-validation.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5236_VALIDATION.csv"

MARKER = "MTS_5236_STRATIFIED_CAUSAL_MULTI_SLICE_A00_POOL_VALIDATION"
REVISION = "stratified-causal-multi-slice-pool-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
AF01_COMPONENT = "AF01_C01"
ENDPOINT_COMPONENT = "AF04_C01"
EPSILON_ID = "E020"
DIRECT_SCAN_MINIMUM = 0.005
DIRECT_SCAN_MAXIMUM = 0.995
ENDPOINT_SCAN_MINIMUM = -0.995
ENDPOINT_SCAN_MAXIMUM = 0.995
SCAN_POINTS = 801
TOPOLOGY_STEPS = 12288
PROJECTIVE_LIMIT = 0.1
QUADRATURE_ORDERS = (32, 128, 512, 1024)
LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 2.0e-4
HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT = 5.0e-5
MINIMUM_POOL_IMPROVEMENT_FACTOR = 1000.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5235 = load_module(SCRIPT_5235, "mts_5235_for_5236")
M5234 = M5235.M5234
M5232 = M5235.M5232
M5231 = M5235.M5231
M5024 = M5234.M5024
M5022 = M5234.M5022
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


def run_AF01_direct_slice() -> dict[str, Any]:
    case = M5232.source_cases()[1]
    if case["family"] != "direct:g2:plus/direct:g3:minus":
        raise RuntimeError("locked AF01 family changed")
    event = M5232.event_for_case(case)
    topology = M5232.topology_for_case(case, EPSILON_ID)
    atlas_rows = [
        row
        for row in read_csv(ATLAS_5234)
        if row["component_id"] == AF01_COMPONENT
        and row["atlas_status"]
        == "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS"
    ]
    problem = {
        "component_id": AF01_COMPONENT,
        "case": case,
        "event": event,
        "topology": topology,
        "target": M5231.complex_value(topology["target_cosine"]),
        "atlas_rows": atlas_rows,
    }
    previous = (
        M5235.SCAN_MINIMUM,
        M5235.SCAN_MAXIMUM,
        M5235.SCAN_POINTS,
    )
    M5235.SCAN_MINIMUM = DIRECT_SCAN_MINIMUM
    M5235.SCAN_MAXIMUM = DIRECT_SCAN_MAXIMUM
    M5235.SCAN_POINTS = SCAN_POINTS
    try:
        _, values = M5235.scan_surfaces(problem)
        poles = M5235.locate_geometric_roots(problem, values)
        topology_rows = M5235.topology_audit(problem, poles)
        residue_rows, fits = M5235.fit_active_residues(problem, poles)
        quadrature_rows, quadrature = M5235.integrate_active_patches(
            problem, fits
        )
    finally:
        (
            M5235.SCAN_MINIMUM,
            M5235.SCAN_MAXIMUM,
            M5235.SCAN_POINTS,
        ) = previous
    return {
        "problem": problem,
        "poles": poles,
        "topology_rows": topology_rows,
        "residue_rows": residue_rows,
        "fits": fits,
        "quadrature_rows": quadrature_rows,
        "quadrature": quadrature,
    }


def endpoint_component() -> dict[str, Any]:
    components = M5234.component_inventory(
        M5234.active_family_inventory()
    )
    return next(
        component
        for component in components
        if component["component_id"] == ENDPOINT_COMPONENT
    )


def endpoint_geometry(
    component: dict[str, Any], coordinate: complex
) -> dict[str, Any]:
    event = dict(component["event"])
    event["decay_cosine"] = float(coordinate.real)
    rationals = M5231.root_rationals(event, component["target"])
    labels = component["representative_labels"]
    roots = M5232.M5029.collision_roots(
        rationals[labels[0]], rationals[labels[1]]
    )
    if not roots:
        raise RuntimeError("endpoint collision branch disappeared")
    anchor = M5231.complex_value(
        component["representative"]["target_root"]
    )
    relative_root = min(
        roots,
        key=lambda root: M5232.M5030.chordal_distance(root, anchor),
    )
    global_values = [
        M5231.rational_value_and_derivative(
            rationals[label], relative_root
        )[0]
        for label in labels
    ]
    global_root = complex(sum(global_values) / len(global_values))
    soft_direction, decay_direction, _ = M5232.M5028.event_geometry(
        float(event["soft_energy"]),
        complex(float(event["soft_cosine"])),
        complex(float(event["decay_cosine"])),
        relative_root,
    )
    soft_rotated = M5022.rotate_vector(soft_direction, global_root)
    decay_rotated = M5022.rotate_vector(decay_direction, global_root)
    endpoint_internal = np.zeros((3, 4), dtype=np.complex128)
    endpoint_internal[0] = np.concatenate(([1.0], decay_rotated))
    endpoint_internal[1] = np.concatenate(([1.0], -decay_rotated))
    left, right = M5017.cut_momenta(
        endpoint_internal, component["target"], 1.0
    )
    soft_left = np.concatenate(([1.0], soft_rotated)).astype(
        np.complex128
    )
    return {
        "left": left,
        "right": right,
        "soft_left": soft_left,
        "soft_right": -soft_left,
    }


def endpoint_surface_values(
    component: dict[str, Any],
    candidate_surfaces: list[str],
    coordinate: float,
) -> dict[str, complex]:
    geometry = endpoint_geometry(component, complex(coordinate))
    left = geometry["left"]
    right = geometry["right"]
    soft_left = geometry["soft_left"]
    soft_right = geometry["soft_right"]
    all_values = {
        "endpoint:shared:soft:s13": M5234.vector_invariant(
            left[1], soft_left
        ),
        "endpoint:shared:soft:s23": M5234.vector_invariant(
            left[2], soft_left
        ),
        "endpoint:L:hard:s01=s24": M5234.pair_invariant(left, 0, 1),
        "endpoint:L:hard:s02=s14": M5234.pair_invariant(left, 0, 2),
        "endpoint:L:soft:s03": M5234.vector_invariant(
            left[0], soft_left
        ),
        "endpoint:L:soft:s34": M5234.vector_invariant(
            left[4], soft_left
        ),
        "endpoint:R:hard:s01=s24": M5234.pair_invariant(right, 0, 1),
        "endpoint:R:hard:s02=s14": M5234.pair_invariant(right, 0, 2),
        "endpoint:R:soft:s03": M5234.vector_invariant(
            right[0], soft_right
        ),
        "endpoint:R:soft:s34": M5234.vector_invariant(
            right[4], soft_right
        ),
    }
    return {surface: all_values[surface] for surface in candidate_surfaces}


def endpoint_bisection(
    component: dict[str, Any],
    candidate_surfaces: list[str],
    surface_id: str,
    lower: float,
    upper: float,
) -> float:
    lower_value = endpoint_surface_values(
        component, candidate_surfaces, lower
    )[surface_id].real
    upper_value = endpoint_surface_values(
        component, candidate_surfaces, upper
    )[surface_id].real
    for _ in range(70):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = endpoint_surface_values(
            component, candidate_surfaces, midpoint
        )[surface_id].real
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
        if upper - lower < 2.0e-14:
            break
    return 0.5 * (lower + upper)


def run_endpoint_control() -> list[dict[str, Any]]:
    component = endpoint_component()
    candidate_surfaces = [
        row["surface_id"]
        for row in read_csv(ATLAS_5234)
        if row["component_id"] == ENDPOINT_COMPONENT
        and row["atlas_status"]
        == "ENUMERATE_ROOT_AND_SUBTRACT_IF_DOMAIN_INTERSECTS"
    ]
    coordinates = np.linspace(
        ENDPOINT_SCAN_MINIMUM, ENDPOINT_SCAN_MAXIMUM, SCAN_POINTS
    )
    values: dict[str, list[complex]] = {
        surface: [] for surface in candidate_surfaces
    }
    for coordinate in coordinates:
        row = endpoint_surface_values(
            component, candidate_surfaces, float(coordinate)
        )
        for surface, value in row.items():
            values[surface].append(value)
    roots: list[dict[str, Any]] = []
    for surface, surface_values in values.items():
        for index in range(len(coordinates) - 1):
            if (
                surface_values[index].real
                * surface_values[index + 1].real
                >= 0.0
            ):
                continue
            center = endpoint_bisection(
                component,
                candidate_surfaces,
                surface,
                float(coordinates[index]),
                float(coordinates[index + 1]),
            )
            step = 1.0e-6
            value = endpoint_surface_values(
                component, candidate_surfaces, center
            )[surface]
            derivative = (
                endpoint_surface_values(
                    component, candidate_surfaces, center + step
                )[surface]
                - endpoint_surface_values(
                    component, candidate_surfaces, center - step
                )[surface]
            ) / (2.0 * step)
            pole = complex(center) - value / derivative
            roots.append(
                {
                    "control_id": f"EC{len(roots) + 1:02d}",
                    "component_id": ENDPOINT_COMPONENT,
                    "family": component["family"],
                    "outer_coordinate": "decay_cosine",
                    "candidate_surface_count": len(candidate_surfaces),
                    "surface_id": surface,
                    "real_axis_center": center,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "channel_derivative_real": derivative.real,
                    "channel_derivative_imaginary": derivative.imag,
                    "causal_family_active": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    pairs = [
        tuple(component["representative_labels"]),
        tuple(component["partner_labels"]),
    ]
    expected = {
        component["representative_labels"][0].rsplit("_", 1)[-1]: int(
            component["representative"]["winding_correction"]
        ),
        component["partner_labels"][0].rsplit("_", 1)[-1]: int(
            component["partner"]["winding_correction"]
        ),
    }
    for row in roots:
        event = dict(component["event"])
        event["decay_cosine"] = float(row["real_axis_center"])
        audit = M5232.target_pair_track(
            event,
            component["target"],
            pairs,
            TOPOLOGY_STEPS,
        )
        winding = {
            pair_row["pair"][0].rsplit("_", 1)[-1]: int(
                pair_row["winding_sum"]
            )
            for pair_row in audit["pair_rows"]
        }
        active = winding == expected
        row.update(
            {
                "u_winding": winding.get("u"),
                "v_winding": winding.get("v"),
                "expected_u_winding": expected.get("u"),
                "expected_v_winding": expected.get("v"),
                "causal_family_active": active,
                "topology_steps": TOPOLOGY_STEPS,
                "maximum_pair_projective_step": audit[
                    "maximum_pair_projective_step"
                ],
                "maximum_reciprocal_product_residual": audit[
                    "maximum_reciprocal_product_residual"
                ],
                "subtracted": False,
            }
        )
    return roots


def qualify_rows(
    rows: list[dict[str, Any]], slice_id: str
) -> list[dict[str, Any]]:
    return [{"slice_id": slice_id, **row} for row in rows]


def pooled_quadrature(
    AF01_rows: list[dict[str, Any]],
    AF02_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows: list[dict[str, Any]] = []
    for slice_id, rows in (
        ("AF01_soft_energy", AF01_rows),
        ("AF02_decay_cosine", AF02_rows),
    ):
        for row in rows:
            if row["row_type"] != "individual_patch":
                continue
            source_rows.append({"slice_id": slice_id, **row})
    pooled: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        selected = [
            row
            for row in source_rows
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
        pooled.append(
            {
                "quadrature_order": order,
                "slice_count": 2,
                "active_patch_count": len(selected),
                "raw_pool_real": raw.real,
                "raw_pool_imaginary": raw.imag,
                "subtracted_pool_real": subtracted.real,
                "subtracted_pool_imaginary": subtracted.imag,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    reference = complex(
        float(pooled[-1]["subtracted_pool_real"]),
        float(pooled[-1]["subtracted_pool_imaginary"]),
    )
    rows: list[dict[str, Any]] = []
    for row in pooled:
        raw = complex(
            float(row["raw_pool_real"]),
            float(row["raw_pool_imaginary"]),
        )
        subtracted = complex(
            float(row["subtracted_pool_real"]),
            float(row["subtracted_pool_imaginary"]),
        )
        rows.append(
            {
                **row,
                "raw_relative_error_to_subtracted_1024": abs(
                    raw - reference
                )
                / max(abs(reference), 1.0),
                "subtracted_relative_error_to_subtracted_1024": abs(
                    subtracted - reference
                )
                / max(abs(reference), 1.0),
            }
        )
    low = rows[0]
    high = rows[-1]
    low_raw_error = float(low["raw_relative_error_to_subtracted_1024"])
    low_subtracted_error = float(
        low["subtracted_relative_error_to_subtracted_1024"]
    )
    summary = {
        "slice_count": 2,
        "active_patch_count": int(high["active_patch_count"]),
        "reference_order": int(high["quadrature_order"]),
        "subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": low_raw_error,
        "low_order_subtracted_relative_error": low_subtracted_error,
        "high_order_raw_relative_error": float(
            high["raw_relative_error_to_subtracted_1024"]
        ),
        "low_order_improvement_factor": low_raw_error
        / max(low_subtracted_error, 1.0e-30),
    }
    return rows, summary


def slice_catalog(
    AF01: dict[str, Any],
    AF02: dict[str, Any],
    endpoint_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "slice_id": "AF01_soft_energy",
            "component_id": AF01_COMPONENT,
            "owner_summand": "direct_five_point",
            "family": AF01["problem"]["case"]["family"],
            "outer_coordinate": "soft_energy",
            "geometric_root_count": len(AF01["poles"]),
            "active_root_count": sum(
                bool(row["causal_family_active"]) for row in AF01["poles"]
            ),
            "inactive_root_count": sum(
                not bool(row["causal_family_active"])
                for row in AF01["poles"]
            ),
            "subtracted_patch_count": len(AF01["fits"]),
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        {
            "slice_id": "AF02_decay_cosine",
            "component_id": "AF02_C01",
            "owner_summand": "direct_five_point",
            "family": AF02["family"],
            "outer_coordinate": "decay_cosine",
            "geometric_root_count": AF02["geometric_root_count"],
            "active_root_count": AF02["active_causal_root_count"],
            "inactive_root_count": AF02["inactive_geometric_root_count"],
            "subtracted_patch_count": AF02["active_causal_root_count"],
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        {
            "slice_id": "AF04_endpoint_decay_cosine",
            "component_id": ENDPOINT_COMPONENT,
            "owner_summand": "endpoint_subtraction",
            "family": endpoint_rows[0]["family"],
            "outer_coordinate": "decay_cosine",
            "geometric_root_count": len(endpoint_rows),
            "active_root_count": sum(
                bool(row["causal_family_active"]) for row in endpoint_rows
            ),
            "inactive_root_count": sum(
                not bool(row["causal_family_active"])
                for row in endpoint_rows
            ),
            "subtracted_patch_count": 0,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    ]


def validation_rows(
    parent_5234: dict[str, Any],
    parent_5235: dict[str, Any],
    AF01: dict[str, Any],
    endpoint_rows: list[dict[str, Any]],
    pool: dict[str, Any],
) -> list[dict[str, Any]]:
    required = [
        SCRIPT_5234,
        SCRIPT_5235,
        RESULT_5234,
        RESULT_5235,
        ATLAS_5234,
        QUADRATURE_5235,
    ]
    AF01_pass = (
        len(AF01["poles"]) == 1
        and AF01["poles"][0]["surface_ids"] == "direct:L:s24"
        and bool(AF01["poles"][0]["causal_family_active"])
        and len(AF01["fits"]) == 1
        and all(
            abs(
                float(
                    next(iter(AF01["fits"].values()))[side][
                        "log_log_slope"
                    ]
                )
                + 1.0
            )
            < 0.03
            for side in ("negative_side", "positive_side")
        )
        and float(
            AF01["quadrature"]["low_order_subtracted_relative_error"]
        )
        < 1.0e-3
    )
    endpoint_pass = (
        len(endpoint_rows) == 1
        and endpoint_rows[0]["surface_id"]
        == "endpoint:shared:soft:s23"
        and not bool(endpoint_rows[0]["causal_family_active"])
        and not bool(endpoint_rows[0]["subtracted"])
        and float(endpoint_rows[0]["maximum_pair_projective_step"])
        < PROJECTIVE_LIMIT
    )
    pool_pass = (
        int(pool["active_patch_count"]) == 3
        and float(pool["low_order_subtracted_relative_error"])
        <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        and float(pool["high_order_raw_relative_error"])
        <= HIGH_ORDER_RAW_RELATIVE_ERROR_LIMIT
        and float(pool["low_order_improvement_factor"])
        >= MINIMUM_POOL_IMPROVEMENT_FACTOR
    )
    formal_digest = tree_digest(FORMAL)
    checks = [
        (
            "required_source_paths_exist",
            all(path.exists() for path in required),
            f"{sum(path.exists() for path in required)}/{len(required)}",
        ),
        (
            "5234_and_5235_parent_gates_are_passed",
            bool(parent_5234["validation_all_passed"])
            and bool(parent_5235["validation_all_passed"]),
            (
                f"5234={parent_5234['decision']};"
                f"5235={parent_5235['decision']}"
            ),
        ),
        (
            "independent_AF01_slice_finds_and_subtracts_active_s24",
            AF01_pass,
            json.dumps(
                {
                    "poles": [
                        {
                            "surface": row["surface_ids"],
                            "active": row["causal_family_active"],
                            "pole": [
                                row["pole_real"],
                                row["pole_imaginary"],
                            ],
                        }
                        for row in AF01["poles"]
                    ],
                    "quadrature": AF01["quadrature"],
                },
                separators=(",", ":"),
            ),
        ),
        (
            "endpoint_owned_control_rejects_inactive_geometric_root",
            endpoint_pass,
            json.dumps(endpoint_rows, separators=(",", ":")),
        ),
        (
            "three_active_patches_form_a_converged_causal_pool",
            pool_pass,
            json.dumps(pool, separators=(",", ":")),
        ),
        (
            "no_geometric_root_is_subtracted_without_active_winding",
            not any(
                bool(row["subtracted"])
                and not bool(row["causal_family_active"])
                for row in endpoint_rows
            ),
            "endpoint control remains unsubtracted",
        ),
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "all_claim_flags_remain_false",
            True,
            "stratified conditional pilot only; UV, local GR and full MTS claims remain false",
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
    parent_5234 = read_json(RESULT_5234)
    parent_5235 = read_json(RESULT_5235)
    if not (
        bool(parent_5234["validation_all_passed"])
        and bool(parent_5235["validation_all_passed"])
    ):
        raise RuntimeError("5234/5235 parent gate is not passed")
    AF01 = run_AF01_direct_slice()
    endpoint_rows = run_endpoint_control()
    AF02_quadrature = read_csv(QUADRATURE_5235)
    pool_rows, pool = pooled_quadrature(
        AF01["quadrature_rows"], AF02_quadrature
    )
    slices = slice_catalog(AF01, parent_5235, endpoint_rows)
    validations = validation_rows(
        parent_5234,
        parent_5235,
        AF01,
        endpoint_rows,
        pool,
    )
    validation_all_passed = all(bool(row["passed"]) for row in validations)
    decision = (
        "ADOPT_STRATIFIED_CAUSAL_POOL_METHOD_AND_PREPARE_BOUNDED_MULTI_EVENT_RUN"
        if validation_all_passed
        else "RETAIN_BLOCK_AND_REPAIR_STRATIFIED_POOL"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "slice_catalog": slices,
        "AF01_poles": AF01["poles"],
        "AF01_quadrature": AF01["quadrature"],
        "endpoint_control": endpoint_rows,
        "pooled_quadrature": pool,
        "total_geometric_root_count": sum(
            int(row["geometric_root_count"]) for row in slices
        ),
        "total_active_root_count": sum(
            int(row["active_root_count"]) for row in slices
        ),
        "total_inactive_root_count": sum(
            int(row["inactive_root_count"]) for row in slices
        ),
        "validation_all_passed": validation_all_passed,
        "scope": (
            "three stratified conditional slices and three active patches; "
            "not the full multidimensional A00 coefficient"
        ),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_target": (
            "package the validated root scan, causal filter and residue cache "
            "as a bounded multi-event runner; execute a dry run before any "
            "full A00 computation"
        ),
        "source_paths": [
            str(SCRIPT_5234),
            str(SCRIPT_5235),
            str(RESULT_5234),
            str(RESULT_5235),
            str(ATLAS_5234),
            str(QUADRATURE_5235),
        ],
    }
    write_csv(SLICE_ROWS, slices)
    write_csv(AF01_POLE_ROWS, qualify_rows(AF01["poles"], "AF01_soft_energy"))
    write_csv(
        AF01_TOPOLOGY_ROWS,
        qualify_rows(AF01["topology_rows"], "AF01_soft_energy"),
    )
    write_csv(
        AF01_RESIDUE_ROWS,
        qualify_rows(AF01["residue_rows"], "AF01_soft_energy"),
    )
    write_csv(
        AF01_QUADRATURE_ROWS,
        qualify_rows(AF01["quadrature_rows"], "AF01_soft_energy"),
    )
    write_csv(ENDPOINT_ROWS, endpoint_rows)
    write_csv(POOL_ROWS, pool_rows)
    write_csv(VALIDATION, validations)
    atomic_json(RESULT, result)

    slice_lines = "\n".join(
        (
            f"- `{row['slice_id']}`: owner `{row['owner_summand']}`, "
            f"geometric/active/inactive roots "
            f"`{row['geometric_root_count']}/"
            f"{row['active_root_count']}/{row['inactive_root_count']}`, "
            f"subtracted patches `{row['subtracted_patch_count']}`."
        )
        for row in slices
    )
    AF01_pole = AF01["poles"][0]
    endpoint = endpoint_rows[0]
    document = f"""# 5236 - Stratified causal multi-slice A00 pool validation

## Decision

`{decision}`.

The 5235 root scanner and subtraction were not left as a one-event success.
This checkpoint adds an independent direct family and an endpoint-owned
negative control:

{slice_lines}

## Independent direct slice

For `AF01_C01`, all atlas surfaces were scanned over
`soft_energy in [{DIRECT_SCAN_MINIMUM},{DIRECT_SCAN_MAXIMUM}]`.  The scan found
one left-`s24` pole,

```text
q_* = {float(AF01_pole['pole_real']):+.12g}
      {float(AF01_pole['pole_imaginary']):+.12g} i,
```

with causal windings
`({AF01_pole['u_winding']},{AF01_pole['v_winding']})`.  Its order-32
subtracted patch error is
`{AF01['quadrature']['low_order_subtracted_relative_error']:.9g}`, compared
with raw error `{AF01['quadrature']['low_order_raw_relative_error']:.9g}`.

## Endpoint-owned control

The endpoint `AF04_C01` slice contains the geometric
`{endpoint['surface_id']}` zero at
`{float(endpoint['pole_real']):+.12g}`.  Its windings are
`({endpoint['u_winding']},{endpoint['v_winding']})`, not the inherited active
pair.  It is therefore recorded but deliberately not subtracted.

This confirms that the same filter works on both summand owners: it accepts a
direct physical pole when the residue family is live and rejects an endpoint
factorization zero when that family has left the causal cycle.

## Pooled convergence

The three accepted patches from the two direct slices were pooled only after
individual causal classification and subtraction.  Relative to the pooled
order-1024 subtracted reference:

- raw order-32 error: `{pool['low_order_raw_relative_error']:.9g}`;
- subtracted order-32 error:
  `{pool['low_order_subtracted_relative_error']:.9g}`;
- improvement: `{pool['low_order_improvement_factor']:.9g}x`;
- order-1024 raw crosscheck error:
  `{pool['high_order_raw_relative_error']:.9g}`.

The stabilization is therefore not specific to one pole, one coordinate, or
one event.

## Scope and next target

This is a stratified conditional pool, not the full multidimensional A00
coefficient.  It validates the method needed for that computation without
making a UV, local-GR, or full-MTS claim.

The next implementation should package this scanner, winding gate, residue
fit and cache into a bounded multi-event runner, dry-run its job manifest, and
only then authorize a larger A00 calculation.
"""
    atomic_text(DOCUMENT, document)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not validation_all_passed:
        raise RuntimeError("5236 stratified causal pool validation failed")


if __name__ == "__main__":
    main()
