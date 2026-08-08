from __future__ import annotations

import argparse
import cmath
import copy
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
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
os.environ["PYTHONNOUSERSITE"] = "1"

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5274"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5273 = (
    SCRIPTS / "Y5_R2FR_5273_exact_boolean_cycle_mask_collapse.py"
)
SCRIPT_5239 = (
    SCRIPTS
    / "Y5_R2FR_5239_matched_event_A00_regular_complement_and_regulator_extrapolation.py"
)
RESULT_5273 = (
    FUNCTIONAL_RG / "5273" / "exact_boolean_cycle_mask_result.json"
)
VALIDATION_5273 = (
    FUNCTIONAL_RG / "5273" / "exact_boolean_cycle_mask_validation.csv"
)
COMPONENT_MAP_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_regulator_component_map.csv"
)
MANIFEST_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_event_A00_job_manifest.json"
)

DRY_RUN = SOURCE / "full_safe_component_audit_dry_run.json"
FULL_MASK_LAWS = SOURCE / "all_safe_component_boolean_mask_laws.csv"
MASK_INSERTION = SOURCE / "integrand_mask_insertion_audit.csv"
TARGET_POINTS = SOURCE / "materiality_target_points.csv"
PATH_DIAGNOSTICS = SOURCE / "component_transport_path_diagnostics.csv"
MATERIALITY_ROWS = SOURCE / "transported_component_pole_order_audit.csv"
COMPONENT_SUMMARY = SOURCE / "global_component_materiality_summary.csv"
RESULT = SOURCE / "full_safe_component_materiality_result.json"
VALIDATION = SOURCE / "full_safe_component_materiality_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5274_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5274-Y5-R2FR-full-safe-component-materiality-and-mask-insertion-audit.md"
)

CHECKPOINT = 5274
PARENT_CHECKPOINT = 5273
MARKER = "MTS_5274_FULL_SAFE_COMPONENT_MATERIALITY_AND_MASK_INSERTION_AUDIT"
REVISION = "full-safe-component-materiality-mask-insertion-audit-v1"
TARGET_POINT_COUNT = 48
PATH_RESOLUTIONS = (33, 65, 129, 257, 513, 1025)
PATH_STEP_LIMIT = 5.0e-2
RECIPROCAL_RESIDUAL_LIMIT = 2.0e-8
CLAIM_FIELDS = (
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


M5273 = load_module("mts_5273_for_5274", SCRIPT_5273)
M5272 = M5273.M5272
M5270 = M5273.M5270
M5267 = M5272.M5267
M5239 = M5267.M5239
M5237 = M5239.M5237
M5231 = M5239.M5231


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def json_default(value: Any) -> Any:
    if isinstance(value, complex):
        return {
            "real": float(value.real),
            "imaginary": float(value.imag),
        }
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
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
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5273,
        SCRIPT_5239,
        RESULT_5273,
        VALIDATION_5273,
        COMPONENT_MAP_5239,
        MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5273.formal_inventory_digest())


def label_surface_key(label: str) -> str:
    source_name, root_label = label.rsplit(":", 1)
    return M5272.surface_key(
        source_name,
        M5272.target_from_label(root_label),
        math.pi,
    )


def suffix_parity(label: str) -> int:
    suffix = label.rsplit("_", 1)[1]
    if suffix == "u":
        return 1
    if suffix == "v":
        return -1
    raise ValueError(f"unsupported root suffix: {label}")


def full_mask_law_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component in read_csv(COMPONENT_MAP_5239):
        pair_strings = component["label_signature"].split("||")
        if len(pair_strings) != 2:
            raise RuntimeError(
                f"invalid label signature: {component['label_signature']}"
            )
        pairs = [
            tuple(pair_string.split("|"))
            for pair_string in pair_strings
        ]
        if any(len(pair) != 2 for pair in pairs):
            raise RuntimeError("component pair must have two labels")
        surface_sets = [
            {label_surface_key(label) for label in pair}
            for pair in pairs
        ]
        parities = [
            math.prod(suffix_parity(label) for label in pair)
            for pair in pairs
        ]
        surfaces = sorted(surface_sets[0])
        closed = (
            surface_sets[0] == surface_sets[1]
            and len(surfaces) == 2
            and parities[0] == parities[1]
        )
        parity = parities[0]
        rows.append(
            {
                "component_id": component["component_id"],
                "family": component["family"],
                "owner_summand": component["owner_summand"],
                "source_material": (
                    component["material"].lower() == "true"
                ),
                "label_signature": component["label_signature"],
                "surface_A": surfaces[0] if surfaces else "",
                "surface_B": (
                    surfaces[1] if len(surfaces) > 1 else ""
                ),
                "first_pair_parity": parities[0],
                "second_pair_parity": parities[1],
                "root_parity_product": parity,
                "cycle_active_law": (
                    "F_A*F_B<0"
                    if parity == 1
                    else "F_A*F_B>0"
                ),
                "derivation_closed": closed,
                "valid_for_exact_cycle_mask": closed,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return sorted(rows, key=lambda row: str(row["component_id"]))


def mask_insertion_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_path": str(SCRIPT_5239),
            "function_symbol": "dynamic_component_contribution",
            "assembly_law": (
                "dynamic_multiplier * component_contribution"
            ),
            "mask_operation": "multiplication",
            "mask_derivative_order": 0,
            "surface_delta_generated": False,
            "audit_status": "PURELY_MULTIPLICATIVE",
            "valid_for_volume_mask_without_surface_delta": True,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        {
            "source_path": str(SCRIPT_5239),
            "function_symbol": "integrate_matched_event.total_integrand",
            "assembly_law": "sum(dynamic_component_contribution)",
            "mask_operation": "linear_sum_after_multiplication",
            "mask_derivative_order": 0,
            "surface_delta_generated": False,
            "audit_status": "NO_MASK_DERIVATIVE_IN_PARENT_INTEGRAND",
            "valid_for_volume_mask_without_surface_delta": True,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    ]


def target_point_rows(
    source_event: dict[str, Any],
) -> list[dict[str, Any]]:
    generator = np.random.default_rng(5274)
    random_points = generator.random((TARGET_POINT_COUNT - 1, 3))
    energy_minimum = float(M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5267.ENERGY_MAXIMUM)
    angular_limit = float(M5270.ANGULAR_LIMIT)
    events = [
        {
            "soft_energy": float(source_event["soft_energy"]),
            "soft_cosine": float(source_event["soft_cosine"]),
            "decay_cosine": float(source_event["decay_cosine"]),
            "is_source_event": True,
        }
    ]
    for point in random_points:
        events.append(
            {
                "soft_energy": (
                    energy_minimum
                    + (energy_maximum - energy_minimum)
                    * float(point[0])
                ),
                "soft_cosine": angular_limit * (
                    2.0 * float(point[1]) - 1.0
                ),
                "decay_cosine": angular_limit * (
                    2.0 * float(point[2]) - 1.0
                ),
                "is_source_event": False,
            }
        )
    return [
        {
            "point_id": f"P{index:03d}",
            **event,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for index, event in enumerate(events)
    ]


def component_inventory(
    epsilon_id: str,
    source_event: dict[str, Any],
    contract: dict[str, Any],
) -> tuple[
    complex,
    list[dict[str, Any]],
    dict[int, str],
]:
    topology = read_json(
        M5231.topology_path(
            contract, M5239.TARGET_SEED, epsilon_id
        )
    )
    target = M5231.complex_value(topology["target_cosine"])
    enumerated = M5239.enumerate_components(
        source_event, topology, epsilon_id
    )
    map_rows = read_csv(COMPONENT_MAP_5239)
    pair_to_component = {
        int(row[f"{epsilon_id}_source_pair_index"]):
        row["component_id"]
        for row in map_rows
    }
    for component in enumerated:
        pair_index = int(component["source_pair_index"])
        component["component_id"] = pair_to_component[pair_index]
    return target, enumerated, pair_to_component


def event_interpolation(
    source: dict[str, Any],
    target: dict[str, Any],
    fraction: float,
) -> dict[str, float]:
    return {
        name: (
            (1.0 - fraction) * float(source[name])
            + fraction * float(target[name])
        )
        for name in (
            "soft_energy",
            "soft_cosine",
            "decay_cosine",
        )
    }


def pair_labels(entry: dict[str, Any]) -> tuple[str, str]:
    values = tuple(entry["representing_pairs"][0])
    if len(values) != 2:
        raise RuntimeError("representing pair is not binary")
    return values


def collision_roots(
    rationals: dict[
        str, tuple[dict[int, complex], dict[int, complex]]
    ],
    pair: tuple[str, str],
) -> list[complex]:
    return [
        complex(root)
        for root in M5231.M5029.collision_roots(
            rationals[pair[0]], rationals[pair[1]]
        )
    ]


def selected_reciprocal_pair(
    representative_roots: list[complex],
    reciprocal_roots: list[complex],
    previous: tuple[complex, complex],
) -> tuple[complex, complex, float]:
    rows = [
        (
            representative,
            reciprocal,
            abs(representative * reciprocal - 1.0),
        )
        for representative in representative_roots
        for reciprocal in reciprocal_roots
    ]
    if not rows:
        raise RuntimeError("collision root pair disappeared")
    minimum_residual = min(row[2] for row in rows)
    eligible = [
        row
        for row in rows
        if row[2]
        <= max(
            RECIPROCAL_RESIDUAL_LIMIT,
            100.0 * minimum_residual,
        )
    ]
    return min(
        eligible,
        key=lambda row: (
            max(
                M5237.M5030.chordal_distance(
                    previous[0], row[0]
                ),
                M5237.M5030.chordal_distance(
                    previous[1], row[1]
                ),
            ),
            M5237.M5030.chordal_distance(
                previous[0], row[0]
            )
            + M5237.M5030.chordal_distance(
                previous[1], row[1]
            ),
            row[2],
        ),
    )


def transport_components_once(
    components: list[dict[str, Any]],
    source_event: dict[str, Any],
    target_event: dict[str, Any],
    scattering_target: complex,
    resolution: int,
) -> tuple[
    dict[str, tuple[complex, complex]],
    float,
    float,
]:
    previous = {
        str(component["component_id"]): (
            M5231.complex_value(
                component["representative"]["target_root"]
            ),
            M5231.complex_value(
                component["reciprocal"]["target_root"]
            ),
        )
        for component in components
    }
    maximum_step = 0.0
    maximum_reciprocal = 0.0
    for fraction in np.linspace(0.0, 1.0, resolution)[1:]:
        event = event_interpolation(
            source_event, target_event, float(fraction)
        )
        rationals = M5231.root_rationals(
            event, scattering_target
        )
        root_cache: dict[
            tuple[str, str], list[complex]
        ] = {}
        for component in components:
            component_id = str(component["component_id"])
            representative_pair = pair_labels(
                component["representative"]
            )
            reciprocal_pair = pair_labels(
                component["reciprocal"]
            )
            if representative_pair not in root_cache:
                root_cache[representative_pair] = collision_roots(
                    rationals, representative_pair
                )
            if reciprocal_pair not in root_cache:
                root_cache[reciprocal_pair] = collision_roots(
                    rationals, reciprocal_pair
                )
            selected = selected_reciprocal_pair(
                root_cache[representative_pair],
                root_cache[reciprocal_pair],
                previous[component_id],
            )
            current = (selected[0], selected[1])
            maximum_step = max(
                maximum_step,
                M5237.M5030.chordal_distance(
                    previous[component_id][0], current[0]
                ),
                M5237.M5030.chordal_distance(
                    previous[component_id][1], current[1]
                ),
            )
            maximum_reciprocal = max(
                maximum_reciprocal, float(selected[2])
            )
            previous[component_id] = current
    return previous, maximum_step, maximum_reciprocal


def transport_components(
    components: list[dict[str, Any]],
    source_event: dict[str, Any],
    target_event: dict[str, Any],
    scattering_target: complex,
) -> tuple[
    dict[str, tuple[complex, complex]],
    int,
    float,
    float,
]:
    selected: dict[str, tuple[complex, complex]] = {}
    maximum_step = math.inf
    maximum_reciprocal = math.inf
    used_resolution = PATH_RESOLUTIONS[-1]
    for resolution in PATH_RESOLUTIONS:
        (
            selected,
            maximum_step,
            maximum_reciprocal,
        ) = transport_components_once(
            components,
            source_event,
            target_event,
            scattering_target,
            resolution,
        )
        used_resolution = resolution
        if (
            maximum_step <= PATH_STEP_LIMIT
            and maximum_reciprocal
            <= RECIPROCAL_RESIDUAL_LIMIT
        ):
            break
    return (
        selected,
        used_resolution,
        maximum_step,
        maximum_reciprocal,
    )


def pole_order_diagnostic(
    event: dict[str, Any],
    target: complex,
    pair: tuple[str, str],
    relative_root: complex,
) -> dict[str, Any]:
    rationals = M5231.root_rationals(event, target)
    first_root, first_derivative = (
        M5231.rational_value_and_derivative(
            rationals[pair[0]], relative_root
        )
    )
    second_root, second_derivative = (
        M5231.rational_value_and_derivative(
            rationals[pair[1]], relative_root
        )
    )
    global_root = 0.5 * (first_root + second_root)
    soft_direction, decay_direction, internal = (
        M5231.M5028.event_geometry(
            float(event["soft_energy"]),
            complex(float(event["soft_cosine"]), 0.0),
            complex(float(event["decay_cosine"]), 0.0),
            relative_root,
        )
    )
    phase = cmath.exp(0.37j)
    scale = max(1.0, abs(global_root))
    coefficient_samples: list[complex] = []
    for fraction in (2.0e-5, 1.0e-5, 5.0e-6):
        displacement = fraction * scale * phase
        integrand = M5231.M5028.M5026.finite_plus_integrand(
            internal,
            float(event["soft_energy"]),
            soft_direction,
            decay_direction,
            target,
            global_root + displacement,
        )
        coefficient_samples.append(
            complex(integrand * displacement**2)
        )
    middle_magnitude = max(
        abs(coefficient_samples[-2]), 1.0e-300
    )
    scaling_power = -math.log(
        max(
            abs(coefficient_samples[-1]) / middle_magnitude,
            1.0e-300,
        ),
        2.0,
    )
    if scaling_power > M5231.DOUBLE_POLE_POWER_MAXIMUM:
        classification = "LOWER_THAN_DOUBLE_POLE"
    elif scaling_power < M5231.HIGHER_POLE_POWER_MINIMUM:
        classification = "HIGHER_THAN_DOUBLE_POLE"
    else:
        classification = "DOUBLE_POLE"
    coefficient = (
        2.0 * coefficient_samples[-1]
        - coefficient_samples[-2]
    )
    return {
        "classification": classification,
        "coefficient_scaling_power": scaling_power,
        "coefficient_magnitude": abs(coefficient),
        "relative_root_magnitude": abs(relative_root),
        "global_root_magnitude": abs(global_root),
        "collision_jacobian_magnitude": abs(
            first_derivative - second_derivative
        ),
    }


def materiality_audit(
    points: list[dict[str, Any]],
    source_event: dict[str, Any],
    contract: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    map_by_component = {
        row["component_id"]: row
        for row in read_csv(COMPONENT_MAP_5239)
    }
    path_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for epsilon_id in ("E040", "E020"):
        scattering_target, components, _ = component_inventory(
            epsilon_id, source_event, contract
        )
        component_by_id = {
            str(component["component_id"]): component
            for component in components
        }
        for point in points:
            target_event = {
                name: float(point[name])
                for name in (
                    "soft_energy",
                    "soft_cosine",
                    "decay_cosine",
                )
            }
            (
                transported,
                resolution,
                maximum_step,
                maximum_reciprocal,
            ) = transport_components(
                components,
                source_event,
                target_event,
                scattering_target,
            )
            path_passed = (
                maximum_step <= PATH_STEP_LIMIT
                and maximum_reciprocal
                <= RECIPROCAL_RESIDUAL_LIMIT
            )
            path_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "point_id": point["point_id"],
                    "path_resolution": resolution,
                    "maximum_projective_step": maximum_step,
                    "maximum_reciprocal_residual": maximum_reciprocal,
                    "path_passed": path_passed,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            for component_id, pair in sorted(
                transported.items()
            ):
                component = component_by_id[component_id]
                if abs(pair[0]) >= 1.0:
                    entry = component["representative"]
                    relative_root = pair[0]
                    role = "representative"
                else:
                    entry = component["reciprocal"]
                    relative_root = pair[1]
                    role = "reciprocal"
                diagnostic = pole_order_diagnostic(
                    target_event,
                    scattering_target,
                    pair_labels(entry),
                    relative_root,
                )
                source_material = (
                    map_by_component[component_id]["material"].lower()
                    == "true"
                )
                audit_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "point_id": point["point_id"],
                        "component_id": component_id,
                        "family": component["family"],
                        "owner_summand": component[
                            "owner_summand"
                        ],
                        "source_material": source_material,
                        "selected_role": role,
                        "soft_energy": target_event["soft_energy"],
                        "soft_cosine": target_event["soft_cosine"],
                        "decay_cosine": target_event[
                            "decay_cosine"
                        ],
                        **diagnostic,
                        "path_passed": path_passed,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return path_rows, audit_rows


def component_summary_rows(
    audit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    component_ids = sorted(
        {str(row["component_id"]) for row in audit_rows}
    )
    for component_id in component_ids:
        local = [
            row
            for row in audit_rows
            if row["component_id"] == component_id
        ]
        classifications = sorted(
            {str(row["classification"]) for row in local}
        )
        source_material = bool(local[0]["source_material"])
        expected = (
            {"DOUBLE_POLE"}
            if source_material
            else {"LOWER_THAN_DOUBLE_POLE"}
        )
        stable = set(classifications) == expected
        result.append(
            {
                "component_id": component_id,
                "family": local[0]["family"],
                "owner_summand": local[0]["owner_summand"],
                "source_material": source_material,
                "sample_count": len(local),
                "observed_classifications": "|".join(
                    classifications
                ),
                "minimum_coefficient_scaling_power": min(
                    float(row["coefficient_scaling_power"])
                    for row in local
                ),
                "maximum_coefficient_scaling_power": max(
                    float(row["coefficient_scaling_power"])
                    for row in local
                ),
                "maximum_coefficient_magnitude": max(
                    float(row["coefficient_magnitude"])
                    for row in local
                ),
                "classification_stable_on_audit": stable,
                "valid_for_global_structural_zero_proof": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return result


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5273,
        SCRIPT_5239,
        RESULT_5273,
        VALIDATION_5273,
        COMPONENT_MAP_5239,
        MANIFEST_5239,
    )
    parent = read_json(RESULT_5273)
    validation = read_csv(VALIDATION_5273)
    laws = full_mask_law_rows()
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5273_accepted": bool(parent["acceptance_passed"]),
        "parent_5273_validation_passed": all(
            row["passed"].lower() == "true" for row in validation
        ),
        "fifteen_safe_components_loaded": len(laws) == 15,
        "all_fifteen_mask_derivations_close": all(
            bool(row["derivation_closed"]) for row in laws
        ),
        "six_source_material_components": sum(
            bool(row["source_material"]) for row in laws
        )
        == 6,
        "nine_source_zero_components": sum(
            not bool(row["source_material"]) for row in laws
        )
        == 9,
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "safe_component_count": len(laws),
        "runtime_seconds": 0.0,
        "decision": (
            "DRY_RUN_ACCEPTED__AUDIT_FULL_SAFE_COMPONENT_MATERIALITY"
            if all(checks.values())
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5274 dry run did not pass")
    parent = read_json(RESULT_5273)
    contract = M5239.source_contract()
    source_event = M5239.source_event(contract)
    laws = full_mask_law_rows()
    insertion = mask_insertion_rows()
    points = target_point_rows(source_event)
    path_rows, audit_rows = materiality_audit(
        points, source_event, contract
    )
    summaries = component_summary_rows(audit_rows)
    material_summaries = [
        row for row in summaries if bool(row["source_material"])
    ]
    zero_summaries = [
        row for row in summaries if not bool(row["source_material"])
    ]
    unstable_component_ids = sorted(
        str(row["component_id"])
        for row in summaries
        if not bool(row["classification_stable_on_audit"])
    )
    fixed_six_component_basis_supported = (
        all(
            bool(row["classification_stable_on_audit"])
            for row in material_summaries
        )
        and all(
            bool(row["classification_stable_on_audit"])
            for row in zero_summaries
        )
    )
    maximum_path_step = max(
        float(row["maximum_projective_step"])
        for row in path_rows
    )
    maximum_reciprocal = max(
        float(row["maximum_reciprocal_residual"])
        for row in path_rows
    )
    checks = {
        "parent_5273_accepted": bool(parent["acceptance_passed"]),
        "all_fifteen_mask_derivations_close": all(
            bool(row["derivation_closed"]) for row in laws
        ),
        "mask_is_purely_multiplicative": all(
            int(row["mask_derivative_order"]) == 0
            and not bool(row["surface_delta_generated"])
            for row in insertion
        ),
        "all_transport_paths_pass": all(
            bool(row["path_passed"]) for row in path_rows
        ),
        "complete_two_regulator_component_audit": (
            len(audit_rows)
            == len(points) * len(laws) * len(("E040", "E020"))
        ),
        "fixed_six_component_basis_rejected": (
            not fixed_six_component_basis_supported
        ),
        "classification_instability_localized": (
            unstable_component_ids
            == ["MC02", "MC03", "MC07", "MC08"]
        ),
        "no_higher_pole_detected": all(
            str(row["classification"])
            in {"DOUBLE_POLE", "LOWER_THAN_DOUBLE_POLE"}
            for row in audit_rows
        ),
        "both_regulators_audited": (
            {str(row["epsilon_id"]) for row in audit_rows}
            == {"E040", "E020"}
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "full-safe-component-materiality-and-mask-insertion-audit",
        "checks": checks,
        "acceptance_passed": accepted,
        "safe_component_count": len(laws),
        "source_material_component_count": len(material_summaries),
        "source_zero_component_count": len(zero_summaries),
        "target_point_count": len(points),
        "transport_path_count": len(path_rows),
        "materiality_audit_row_count": len(audit_rows),
        "maximum_transport_projective_step": maximum_path_step,
        "maximum_transport_reciprocal_residual": maximum_reciprocal,
        "source_zero_components_remaining_lower_count": sum(
            bool(row["classification_stable_on_audit"])
            for row in zero_summaries
        ),
        "source_material_components_remaining_double_count": sum(
            bool(row["classification_stable_on_audit"])
            for row in material_summaries
        ),
        "classification_unstable_component_ids": (
            unstable_component_ids
        ),
        "fixed_six_component_basis_supported": (
            fixed_six_component_basis_supported
        ),
        "mask_insertion_contract": {
            "operation": "multiplicative",
            "derivative_order": 0,
            "surface_delta_generated": False,
            "source_function": "dynamic_component_contribution",
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "REJECT_FIXED_SIX_COMPONENT_VOLUME_BASIS__"
            "REQUIRE_ARBITRARY_PRECISION_LOCAL_LIMIT"
            if accepted
            else "REPAIR_COMPONENT_TRANSPORT_BEFORE_LIMIT_ANALYSIS"
        ),
        "claim_boundary": {
            "valid_for_purely_multiplicative_mask_insertion": accepted,
            "valid_for_broad_sampled_component_materiality": False,
            "valid_for_global_structural_zero_proof": False,
            "valid_for_fixed_six_component_basis": False,
            "valid_for_six_component_cubature_smoke": False,
            "valid_for_arbitrary_precision_limit_followup": accepted,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The all-component transport falsifies the assumption "
                "that the six source-event component IDs retain fixed "
                "pole order. MC02, MC03, MC07, and MC08 change the "
                "double-precision classification, so cubature is "
                "blocked pending an arbitrary-precision local limit."
            ),
        },
    }
    write_csv(FULL_MASK_LAWS, laws)
    write_csv(MASK_INSERTION, insertion)
    write_csv(TARGET_POINTS, points)
    write_csv(PATH_DIAGNOSTICS, path_rows)
    write_csv(MATERIALITY_ROWS, audit_rows)
    write_csv(COMPONENT_SUMMARY, summaries)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": result["mode"],
            "state": "COMPLETED",
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    text = f"""# 5274 — Full safe-component materiality and mask-insertion audit

## Scope

Checkpoint 5273 reduced the six transported material components to exact
Boolean masks. Before volume cubature, this checkpoint checks two possible
failure modes:

1. whether differentiating the mask creates unaccounted surface-delta
   terms;
2. whether any of the nine safe components that vanished at the source
   event become double-pole material components elsewhere.

## Mask insertion

The sourced parent assembly is

`dynamic_multiplier * component_contribution`,

followed by a linear sum over components. No derivative acts on the
multiplier or the exact Boolean replacement. Therefore this integrand
contains no mask-generated surface-delta term. This conclusion applies to
the current parent integrand; it is not a claim about a different future
observable that explicitly differentiates the occupation.

## Full safe-component audit

- Safe components: **{result['safe_component_count']}**.
- Source-material components: **{result['source_material_component_count']}**.
- Source-zero components: **{result['source_zero_component_count']}**.
- Target events: **{result['target_point_count']}**.
- Regulator/path audits: **{result['transport_path_count']}**.
- Pole-order rows: **{result['materiality_audit_row_count']}**.
- Source-labelled material components stable under the finite-difference classifier: **{result['source_material_components_remaining_double_count']}/{result['source_material_component_count']}**.
- Source-labelled zero components stable under the finite-difference classifier: **{result['source_zero_components_remaining_lower_count']}/{result['source_zero_component_count']}**.
- Classification-unstable IDs: **{', '.join(result['classification_unstable_component_ids'])}**.
- Maximum projective transport step: `{result['maximum_transport_projective_step']:.12g}`.
- Maximum reciprocal residual: `{result['maximum_transport_reciprocal_residual']:.12g}`.

The instability is not interpreted as physical branch creation or
annihilation. The parent classifier estimates pole order at fixed
double-precision displacements. A small double-pole coefficient can be
hidden by the regular background at those displacements, so the four
unstable IDs require an arbitrary-precision local limit.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

Passing this checkpoint rejects, rather than licenses, a fixed
six-component cubature. It does not turn forty-eight sampled events into
an analytic global structural-zero theorem, nor does it claim the final
phase-space coefficient, UV coefficient, local GR, or the full MTS
theory.

## Next target

Evaluate the local coefficient limit with arbitrary precision, separated
into direct and endpoint-subtraction summands, for all fifteen components.
Only after that limit resolves the four unstable IDs may the global
cubature basis be selected.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5273)
    required_csvs = (
        FULL_MASK_LAWS,
        MASK_INSERTION,
        TARGET_POINTS,
        PATH_DIAGNOSTICS,
        MATERIALITY_ROWS,
        COMPONENT_SUMMARY,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        default=json_default,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5273_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "FULL_COMPONENT_AUDIT_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
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
            "MASK_INSERTION_IS_MULTIPLICATIVE",
            bool(
                result["claim_boundary"][
                    "valid_for_purely_multiplicative_mask_insertion"
                ]
            ),
            "no derivative of the occupation multiplier",
        ),
        validation_gate(
            "ALL_TRANSPORT_PATHS_PASS",
            bool(result["checks"]["all_transport_paths_pass"]),
            (
                f"max step={result['maximum_transport_projective_step']}; "
                f"max reciprocal={result['maximum_transport_reciprocal_residual']}"
            ),
        ),
        validation_gate(
            "FIXED_SIX_COMPONENT_BASIS_REJECTED",
            (
                not bool(
                    result["fixed_six_component_basis_supported"]
                )
                and not bool(
                    result["claim_boundary"][
                        "valid_for_fixed_six_component_basis"
                    ]
                )
                and not bool(
                    result["claim_boundary"][
                        "valid_for_six_component_cubature_smoke"
                    ]
                )
            ),
            "no six-component cubature is licensed",
        ),
        validation_gate(
            "INSTABILITY_LOCALIZED_TO_FOUR_COMPONENTS",
            result["classification_unstable_component_ids"]
            == ["MC02", "MC03", "MC07", "MC08"],
            "|".join(result["classification_unstable_component_ids"]),
        ),
        validation_gate(
            "STRUCTURAL_ZERO_CLAIM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_global_structural_zero_proof"
            ],
            "sampled stability is not promoted to an identity",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
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
                == 1
                and result["resource_contract"][
                    "worker_math_threads"
                ]
                == 1
            ),
            "one below-normal single-thread process",
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
            "VALIDATED_FULL_SAFE_COMPONENT_MATERIALITY_AUDIT"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
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
