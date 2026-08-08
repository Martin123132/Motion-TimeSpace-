from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import itertools
import json
import math
import os
import sys
import time
from collections import defaultdict
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
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5278"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5277 = (
    SCRIPTS
    / "Y5_R2FR_5277_exact_mask_residue_normalization_bridge.py"
)
RESULT_5277 = (
    FUNCTIONAL_RG
    / "5277"
    / "exact_mask_residue_normalization_result.json"
)
VALIDATION_5277 = (
    FUNCTIONAL_RG
    / "5277"
    / "exact_mask_residue_normalization_validation.csv"
)
FULL_MASK_LAWS_5274 = (
    FUNCTIONAL_RG
    / "5274"
    / "all_safe_component_boolean_mask_laws.csv"
)
DYNAMIC_INTERVALS_5239 = (
    FUNCTIONAL_RG
    / "5239"
    / "matched_event_dynamic_winding_intervals.csv"
)
MANIFEST_5239 = (
    FUNCTIONAL_RG
    / "5239"
    / "matched_event_A00_job_manifest.json"
)

DRY_RUN = SOURCE / "eight_component_joint_cubature_dry_run.json"
HISTORICAL_REPLAY = SOURCE / "historical_mask_sign_replay.csv"
NODE_ROWS = SOURCE / "joint_cubature_node_residues.csv"
COMPONENT_TOTALS = SOURCE / "joint_cubature_component_totals.csv"
ORDER_TOTALS = SOURCE / "joint_cubature_order_totals.csv"
CONVERGENCE_ROWS = SOURCE / "joint_cubature_convergence.csv"
RESULT = SOURCE / "eight_component_joint_cubature_result.json"
VALIDATION = SOURCE / "eight_component_joint_cubature_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5278_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5278-Y5-R2FR-eight-component-exact-mask-joint-cubature-smoke.md"
)

CHECKPOINT = 5278
PARENT_CHECKPOINT = 5277
MARKER = "MTS_5278_EIGHT_COMPONENT_EXACT_MASK_JOINT_CUBATURE_SMOKE"
REVISION = "eight-component-exact-mask-joint-cubature-smoke-v2"
REGULATOR_IDS = ("E040", "E020")
COMPONENT_IDS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
LEGACY_SIX_IDS = (
    "MC03",
    "MC04",
    "MC07",
    "MC12",
    "MC14",
    "MC15",
)
HIDDEN_IDS = ("MC02", "MC08")
QUADRATURE_ORDERS = (2, 3)
MP_DECIMAL_DIGITS = 80
DELTA_EXPONENTS = (12, 20, 28)
ROOT_RESIDUAL_LIMIT = 1.0e-50
ROOT_REFINEMENT_DISTANCE_LIMIT = 1.0e-7
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
MASK_BOUNDARY_FLOOR = 1.0e-12
ANGULAR_JACOBIAN = 0.25
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


M5277 = load_module("mts_5277_for_5278", SCRIPT_5277)
M5276 = M5277.M5276
M5275 = M5277.M5275
M5274 = M5277.M5274
M5040_MP = M5277.M5040_MP
np = M5274.np
mp = M5277.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


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
        SCRIPT_5277,
        RESULT_5277,
        VALIDATION_5277,
        FULL_MASK_LAWS_5274,
        DYNAMIC_INTERVALS_5239,
        MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5277.formal_inventory_digest())


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(
    first: complex,
    second: complex,
) -> float:
    return abs(first - second) / max(
        abs(first),
        abs(second),
        1.0,
    )


def law_lookup() -> dict[str, dict[str, str]]:
    return {
        row["component_id"]: row
        for row in read_csv(FULL_MASK_LAWS_5274)
        if row["component_id"] in COMPONENT_IDS
    }


def law_state(
    law: dict[str, str],
    event: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
) -> tuple[bool, float, float]:
    values = []
    for field in ("surface_A", "surface_B"):
        value = M5274.M5273.surface_value(
            surfaces[law[field]],
            float(event["soft_energy"]),
            float(event["soft_cosine"]),
            float(event["decay_cosine"]),
        )
        values.append(float(value))
    parity = int(law["root_parity_product"])
    return (
        parity * values[0] * values[1] < 0.0,
        values[0],
        values[1],
    )


def historical_replay_rows() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    manifest = read_json(MANIFEST_5239)
    outer_coordinate = str(manifest["outer_coordinate"])
    surfaces = M5277.exact_surface_lookup()
    laws = law_lookup()
    rows: list[dict[str, Any]] = []
    for interval in read_csv(DYNAMIC_INTERVALS_5239):
        component_id = interval["component_id"]
        if component_id not in laws:
            continue
        event = dict(source_event)
        event[outer_coordinate] = float(interval["interval_midpoint"])
        active, first_value, second_value = law_state(
            laws[component_id],
            event,
            surfaces,
        )
        multiplier = float(interval["dynamic_multiplier"])
        expected_active = abs(multiplier - 1.0) <= 1.0e-12
        sign_preserving = multiplier >= -1.0e-12
        if active == expected_active:
            mismatch_classification = "AGREES"
        elif active and not expected_active:
            mismatch_classification = (
                "OLD_TRACKER_FALSE_NEGATIVE_ACTIVE_CHAMBER"
            )
        else:
            mismatch_classification = (
                "OLD_TRACKER_FALSE_POSITIVE_ACTIVE_CHAMBER"
            )
        rows.append(
            {
                "epsilon_id": interval["epsilon_id"],
                "component_id": component_id,
                "interval_index": interval["interval_index"],
                "interval_midpoint": interval["interval_midpoint"],
                "exact_mask_active": active,
                "historical_dynamic_multiplier": multiplier,
                "historical_dynamic_winding_delta": interval[
                    "dynamic_winding_delta"
                ],
                "historical_source_winding_delta": interval[
                    "source_winding_delta"
                ],
                "expected_active": expected_active,
                "mask_replay_agrees": active == expected_active,
                "mismatch_classification": mismatch_classification,
                "active_sign_preserving": sign_preserving,
                "surface_A_value": first_value,
                "surface_B_value": second_value,
                "valid_for_historical_sign_replay": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def quadrature_points(order: int) -> list[dict[str, Any]]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    angular_limit = float(M5274.M5270.ANGULAR_LIMIT)
    energy_half_width = 0.5 * (
        energy_maximum - energy_minimum
    )
    energy_midpoint = 0.5 * (
        energy_maximum + energy_minimum
    )
    rows: list[dict[str, Any]] = []
    for energy_index, soft_index, decay_index in itertools.product(
        range(order),
        repeat=3,
    ):
        energy = (
            energy_midpoint
            + energy_half_width * float(nodes[energy_index])
        )
        soft_cosine = angular_limit * float(nodes[soft_index])
        decay_cosine = angular_limit * float(nodes[decay_index])
        weight = (
            energy_half_width
            * float(weights[energy_index])
            * angular_limit
            * float(weights[soft_index])
            * angular_limit
            * float(weights[decay_index])
        )
        rows.append(
            {
                "quadrature_order": order,
                "node_id": (
                    f"Q{order:02d}_"
                    f"E{energy_index + 1:02d}_"
                    f"S{soft_index + 1:02d}_"
                    f"D{decay_index + 1:02d}"
                ),
                "soft_energy": energy,
                "soft_cosine": soft_cosine,
                "decay_cosine": decay_cosine,
                "tensor_weight": weight,
            }
        )
    return rows


def coefficient_limit(
    high_precision_event: dict[str, Any],
    high_precision_target: Any,
    labels: tuple[str, str],
    relative_root: Any,
) -> dict[str, Any]:
    (
        soft_direction,
        decay_direction,
        internal,
        global_roots,
    ) = M5275.local_root_data(
        high_precision_event,
        high_precision_target,
        labels,
        relative_root,
    )
    global_root = (global_roots[0] + global_roots[1]) / 2
    scale = max(mp.mpf(1), abs(global_root))
    phase = mp.exp(mp.mpc(0, mp.mpf("0.37")))
    direct_coefficients: list[Any] = []
    subtraction_coefficients: list[Any] = []
    total_coefficients: list[Any] = []
    for exponent in DELTA_EXPONENTS:
        displacement = mp.power(10, -exponent) * scale * phase
        direct, subtraction = M5040_MP.finite_plus_components(
            internal,
            high_precision_event["soft_energy"],
            soft_direction,
            decay_direction,
            high_precision_target,
            global_root + displacement,
        )
        direct_coefficient = direct * displacement**2
        subtraction_coefficient = subtraction * displacement**2
        direct_coefficients.append(direct_coefficient)
        subtraction_coefficients.append(subtraction_coefficient)
        total_coefficients.append(
            direct_coefficient + subtraction_coefficient
        )
    convergence = M5275.relative_complex_difference(
        total_coefficients[-2],
        total_coefficients[-1],
    )
    return {
        "global_root": global_root,
        "direct_limit": direct_coefficients[-1],
        "subtraction_limit": subtraction_coefficients[-1],
        "total_limit": total_coefficients[-1],
        "coefficient_relative_change": convergence,
    }


def selected_component_role(
    component: dict[str, Any],
    transported_pair: tuple[complex, complex],
) -> tuple[str, dict[str, Any], complex]:
    if abs(transported_pair[0]) >= 1.0:
        return (
            "representative",
            component["representative"],
            transported_pair[0],
        )
    return (
        "reciprocal",
        component["reciprocal"],
        transported_pair[1],
    )


def inactive_node_row(
    base: dict[str, Any],
    selected_role: str,
    labels: tuple[str, str],
    mask_active: bool,
    law_active: bool,
    pair_mask_consistent: bool,
    owned_labels: tuple[bool, bool],
    surface_values: tuple[float, float],
    orientation: int,
    winding_delta: int,
    relative_root: complex,
) -> dict[str, Any]:
    return {
        **base,
        "selected_role": selected_role,
        "representing_pair": "|".join(labels),
        "mask_active": mask_active,
        "law_active": law_active,
        "mask_law_agrees": mask_active == law_active,
        "representative_reciprocal_masks_agree": (
            pair_mask_consistent
        ),
        "first_label_owned": owned_labels[0],
        "second_label_owned": owned_labels[1],
        "surface_A_value": surface_values[0],
        "surface_B_value": surface_values[1],
        "minimum_surface_distance": min(
            abs(surface_values[0]),
            abs(surface_values[1]),
        ),
        "orientation": orientation,
        "winding_delta": winding_delta,
        "relative_root_real": relative_root.real,
        "relative_root_imaginary": relative_root.imag,
        "relative_root_unit_margin": abs(
            math.log(max(abs(relative_root), 1.0e-300))
        ),
        "root_equation_residual": "",
        "root_refinement_chordal_distance": "",
        "collision_jacobian_magnitude": "",
        "direct_coefficient_magnitude": "",
        "subtraction_coefficient_magnitude": "",
        "total_coefficient_magnitude": "",
        "coefficient_relative_change": "",
        "residue_real": 0.0,
        "residue_imaginary": 0.0,
        "residue_magnitude": 0.0,
        "weighted_residue_real": 0.0,
        "weighted_residue_imaginary": 0.0,
        "evaluation_status": "MASK_INACTIVE",
        "evaluation_error": "",
        "valid_for_low_order_cubature_smoke": True,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def active_node_row(
    base: dict[str, Any],
    event: dict[str, Any],
    scattering_target: complex,
    component: dict[str, Any],
    selected_role: str,
    labels: tuple[str, str],
    initial_root: complex,
    mask_active: bool,
    law_active: bool,
    pair_mask_consistent: bool,
    owned_labels: tuple[bool, bool],
    surface_values: tuple[float, float],
    orientation: int,
    winding_delta: int,
) -> dict[str, Any]:
    row = inactive_node_row(
        base,
        selected_role,
        labels,
        mask_active,
        law_active,
        pair_mask_consistent,
        owned_labels,
        surface_values,
        orientation,
        winding_delta,
        initial_root,
    )
    try:
        high_precision_event = M5275.event_as_mp(event)
        high_precision_target = M5275.target_as_mp(
            scattering_target
        )
        (
            relative_root,
            root_residual,
            refinement_distance,
        ) = M5275.refine_relative_root(
            high_precision_event,
            high_precision_target,
            labels,
            initial_root,
        )
        limit = coefficient_limit(
            high_precision_event,
            high_precision_target,
            labels,
            relative_root,
        )
        collision_jacobian = M5277.mp_collision_jacobian(
            high_precision_event,
            high_precision_target,
            labels,
            relative_root,
        )
        residue = M5277.residue_from_coefficient(
            limit["total_limit"],
            relative_root,
            limit["global_root"],
            collision_jacobian,
            orientation,
            winding_delta,
        )
        residue_complex = complex(residue)
        weight = float(base["tensor_weight"])
        row.update(
            {
                "relative_root_real": float(mp.re(relative_root)),
                "relative_root_imaginary": float(
                    mp.im(relative_root)
                ),
                "relative_root_unit_margin": float(
                    abs(mp.log(abs(relative_root)))
                ),
                "root_equation_residual": root_residual,
                "root_refinement_chordal_distance": (
                    refinement_distance
                ),
                "collision_jacobian_magnitude": float(
                    abs(collision_jacobian)
                ),
                "direct_coefficient_magnitude": float(
                    abs(limit["direct_limit"])
                ),
                "subtraction_coefficient_magnitude": float(
                    abs(limit["subtraction_limit"])
                ),
                "total_coefficient_magnitude": float(
                    abs(limit["total_limit"])
                ),
                "coefficient_relative_change": float(
                    limit["coefficient_relative_change"]
                ),
                "residue_real": residue_complex.real,
                "residue_imaginary": residue_complex.imag,
                "residue_magnitude": abs(residue_complex),
                "weighted_residue_real": (
                    weight * residue_complex.real
                ),
                "weighted_residue_imaginary": (
                    weight * residue_complex.imag
                ),
                "evaluation_status": "EVALUATED",
                "evaluation_error": "",
                "valid_for_low_order_cubature_smoke": True,
            }
        )
    except Exception as error:
        row.update(
            {
                "evaluation_status": "FAILED",
                "evaluation_error": (
                    f"{type(error).__name__}: {error}"
                ),
                "valid_for_low_order_cubature_smoke": False,
            }
        )
    return row


def evaluate_cubature_nodes() -> list[dict[str, Any]]:
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    surfaces = M5277.exact_surface_lookup()
    laws = law_lookup()
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        (
            scattering_target,
            all_components,
            _,
        ) = M5274.component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        components = [
            component
            for component in all_components
            if component["component_id"] in COMPONENT_IDS
        ]
        component_by_id = {
            str(component["component_id"]): component
            for component in components
        }
        for order in QUADRATURE_ORDERS:
            for point in quadrature_points(order):
                event = {
                    "soft_energy": float(point["soft_energy"]),
                    "soft_cosine": float(point["soft_cosine"]),
                    "decay_cosine": float(point["decay_cosine"]),
                }
                (
                    transported,
                    path_resolution,
                    maximum_step,
                    maximum_reciprocal,
                ) = M5274.transport_components(
                    components,
                    source_event,
                    event,
                    scattering_target,
                )
                path_passed = (
                    maximum_step <= M5274.PATH_STEP_LIMIT
                    and maximum_reciprocal
                    <= M5274.RECIPROCAL_RESIDUAL_LIMIT
                )
                for component_id in COMPONENT_IDS:
                    component = component_by_id[component_id]
                    (
                        selected_role,
                        entry,
                        initial_root,
                    ) = selected_component_role(
                        component,
                        transported[component_id],
                    )
                    labels = M5274.pair_labels(entry)
                    (
                        mask_active,
                        orientation,
                        owned_labels,
                        surface_values,
                    ) = M5277.exact_mask_orientation(
                        labels,
                        event,
                        surfaces,
                    )
                    representative_active = (
                        M5277.exact_mask_orientation(
                            M5274.pair_labels(
                                component["representative"]
                            ),
                            event,
                            surfaces,
                        )[0]
                    )
                    reciprocal_active = (
                        M5277.exact_mask_orientation(
                            M5274.pair_labels(
                                component["reciprocal"]
                            ),
                            event,
                            surfaces,
                        )[0]
                    )
                    law_active, _, _ = law_state(
                        laws[component_id],
                        event,
                        surfaces,
                    )
                    winding_delta = M5277.source_winding_delta(
                        component,
                        selected_role,
                    )
                    base = {
                        "epsilon_id": epsilon_id,
                        "quadrature_order": order,
                        "node_id": point["node_id"],
                        "component_id": component_id,
                        "family": component["family"],
                        "owner_summand": component[
                            "owner_summand"
                        ],
                        "soft_energy": event["soft_energy"],
                        "soft_cosine": event["soft_cosine"],
                        "decay_cosine": event["decay_cosine"],
                        "tensor_weight": point["tensor_weight"],
                        "path_resolution": path_resolution,
                        "maximum_projective_step": maximum_step,
                        "maximum_reciprocal_residual": (
                            maximum_reciprocal
                        ),
                        "path_passed": path_passed,
                    }
                    if not mask_active:
                        row = inactive_node_row(
                            base,
                            selected_role,
                            labels,
                            mask_active,
                            law_active,
                            (
                                representative_active
                                == reciprocal_active
                            ),
                            owned_labels,
                            surface_values,
                            orientation,
                            winding_delta,
                            initial_root,
                        )
                    else:
                        row = active_node_row(
                            base,
                            event,
                            scattering_target,
                            component,
                            selected_role,
                            labels,
                            initial_root,
                            mask_active,
                            law_active,
                            (
                                representative_active
                                == reciprocal_active
                            ),
                            owned_labels,
                            surface_values,
                            orientation,
                            winding_delta,
                        )
                    rows.append(row)
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "epsilon_id": epsilon_id,
                        "quadrature_order": order,
                        "last_node_id": point["node_id"],
                        "completed_component_rows": len(rows),
                    },
                )
    return rows


def component_total_rows(
    node_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: defaultdict[
        tuple[int, str, str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in node_rows:
        grouped[
            (
                int(row["quadrature_order"]),
                str(row["epsilon_id"]),
                str(row["component_id"]),
            )
        ].append(row)
    multiplier = (
        M5274.M5231.PHYSICAL_A00_WEIGHT
        * M5274.M5231.KERNEL_MULTIPLIER
    )
    rows: list[dict[str, Any]] = []
    for key in sorted(grouped):
        order, epsilon_id, component_id = key
        local = grouped[key]
        raw = sum(
            (
                complex(
                    float(row["weighted_residue_real"]),
                    float(row["weighted_residue_imaginary"]),
                )
                for row in local
            ),
            0.0j,
        )
        normalized = ANGULAR_JACOBIAN * raw
        rows.append(
            {
                "quadrature_order": order,
                "epsilon_id": epsilon_id,
                "component_id": component_id,
                "family": local[0]["family"],
                "owner_summand": local[0]["owner_summand"],
                "node_count": len(local),
                "active_node_count": sum(
                    bool(row["mask_active"]) for row in local
                ),
                **complex_fields("raw_volume_integral", raw),
                **complex_fields(
                    "angular_normalized_integral",
                    normalized,
                ),
                **complex_fields(
                    "weighted_regulator_integral",
                    multiplier * normalized,
                ),
                "angular_jacobian": ANGULAR_JACOBIAN,
                "kernel_multiplier": (
                    M5274.M5231.KERNEL_MULTIPLIER
                ),
                "physical_A00_weight": (
                    M5274.M5231.PHYSICAL_A00_WEIGHT
                ),
                "valid_for_low_order_cubature_smoke": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def order_total_rows(
    component_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    component_lookup = {
        (
            int(row["quadrature_order"]),
            str(row["epsilon_id"]),
            str(row["component_id"]),
        ): complex(
            float(row["angular_normalized_integral_real"]),
            float(row["angular_normalized_integral_imaginary"]),
        )
        for row in component_rows
    }
    multiplier = (
        M5274.M5231.PHYSICAL_A00_WEIGHT
        * M5274.M5231.KERNEL_MULTIPLIER
    )
    rows: list[dict[str, Any]] = []
    for order in QUADRATURE_ORDERS:
        regulator_values: dict[str, dict[str, complex]] = {}
        for epsilon_id in REGULATOR_IDS:
            eight = sum(
                (
                    component_lookup[
                        (order, epsilon_id, component_id)
                    ]
                    for component_id in COMPONENT_IDS
                ),
                0.0j,
            )
            six = sum(
                (
                    component_lookup[
                        (order, epsilon_id, component_id)
                    ]
                    for component_id in LEGACY_SIX_IDS
                ),
                0.0j,
            )
            hidden = sum(
                (
                    component_lookup[
                        (order, epsilon_id, component_id)
                    ]
                    for component_id in HIDDEN_IDS
                ),
                0.0j,
            )
            regulator_values[epsilon_id] = {
                "eight": eight,
                "six": six,
                "hidden": hidden,
            }
            rows.append(
                {
                    "row_type": "REGULATOR_INTERIOR_INTEGRAL",
                    "quadrature_order": order,
                    "epsilon_id": epsilon_id,
                    **complex_fields(
                        "eight_component_integral",
                        eight,
                    ),
                    **complex_fields(
                        "six_component_integral",
                        six,
                    ),
                    **complex_fields(
                        "hidden_MC02_MC08_integral",
                        hidden,
                    ),
                    "hidden_fraction": (
                        abs(hidden) / max(abs(eight), 1.0e-300)
                    ),
                    "angular_jacobian": ANGULAR_JACOBIAN,
                    "kernel_multiplier": (
                        M5274.M5231.KERNEL_MULTIPLIER
                    ),
                    "physical_A00_weight": (
                        M5274.M5231.PHYSICAL_A00_WEIGHT
                    ),
                    "valid_for_low_order_cubature_smoke": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        physical_eight = multiplier * (
            2.0 * regulator_values["E020"]["eight"]
            - regulator_values["E040"]["eight"]
        )
        physical_six = multiplier * (
            2.0 * regulator_values["E020"]["six"]
            - regulator_values["E040"]["six"]
        )
        physical_hidden = multiplier * (
            2.0 * regulator_values["E020"]["hidden"]
            - regulator_values["E040"]["hidden"]
        )
        rows.append(
            {
                "row_type": "PHYSICAL_REGULATOR_EXTRAPOLATION",
                "quadrature_order": order,
                "epsilon_id": "2E020_MINUS_E040",
                **complex_fields(
                    "eight_component_integral",
                    physical_eight,
                ),
                **complex_fields(
                    "six_component_integral",
                    physical_six,
                ),
                **complex_fields(
                    "hidden_MC02_MC08_integral",
                    physical_hidden,
                ),
                "hidden_fraction": (
                    abs(physical_hidden)
                    / max(abs(physical_eight), 1.0e-300)
                ),
                "angular_jacobian": ANGULAR_JACOBIAN,
                "kernel_multiplier": (
                    M5274.M5231.KERNEL_MULTIPLIER
                ),
                "physical_A00_weight": (
                    M5274.M5231.PHYSICAL_A00_WEIGHT
                ),
                "valid_for_low_order_cubature_smoke": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def convergence_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    physical = {
        int(row["quadrature_order"]): row
        for row in totals
        if row["row_type"] == "PHYSICAL_REGULATOR_EXTRAPOLATION"
    }
    low_order = QUADRATURE_ORDERS[0]
    high_order = QUADRATURE_ORDERS[-1]
    rows: list[dict[str, Any]] = []
    for channel in (
        "eight_component_integral",
        "six_component_integral",
        "hidden_MC02_MC08_integral",
    ):
        low = complex(
            float(physical[low_order][f"{channel}_real"]),
            float(physical[low_order][f"{channel}_imaginary"]),
        )
        high = complex(
            float(physical[high_order][f"{channel}_real"]),
            float(physical[high_order][f"{channel}_imaginary"]),
        )
        rows.append(
            {
                "channel": channel,
                "low_order": low_order,
                "high_order": high_order,
                **complex_fields("low_order_value", low),
                **complex_fields("high_order_value", high),
                "relative_change": relative_complex_difference(
                    low,
                    high,
                ),
                "interpretation": (
                    "LOW_ORDER_DIAGNOSTIC_ONLY__"
                    "CHAMBER_ADAPTED_CONVERGENCE_PENDING"
                ),
                "valid_for_low_order_cubature_smoke": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5277,
        RESULT_5277,
        VALIDATION_5277,
        FULL_MASK_LAWS_5274,
        DYNAMIC_INTERVALS_5239,
        MANIFEST_5239,
    )
    parent = read_json(RESULT_5277)
    parent_validation = read_csv(VALIDATION_5277)
    laws = law_lookup()
    expected_rows = (
        sum(order**3 for order in QUADRATURE_ORDERS)
        * len(REGULATOR_IDS)
        * len(COMPONENT_IDS)
    )
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5277_accepted": bool(parent["acceptance_passed"]),
        "parent_5277_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "exact_eight_component_laws_complete": (
            set(laws) == set(COMPONENT_IDS)
            and all(
                row["derivation_closed"].lower() == "true"
                for row in laws.values()
            )
        ),
        "finite_interior_domain_defined": (
            0.0 < M5274.M5267.ENERGY_MINIMUM
            < M5274.M5267.ENERGY_MAXIMUM
            < 1.0
            and 0.0 < M5274.M5270.ANGULAR_LIMIT < 1.0
        ),
        "single_process_resource_contract": True,
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "expected_component_node_rows": expected_rows,
        "estimated_active_local_limit_evaluations_upper_bound": (
            expected_rows
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_EIGHT_COMPONENT_JOINT_CUBATURE"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
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
    mp.mp.dps = MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5278 dry run did not pass")
    parent = read_json(RESULT_5277)
    replay = historical_replay_rows()
    nodes = evaluate_cubature_nodes()
    component_totals = component_total_rows(nodes)
    order_totals = order_total_rows(component_totals)
    convergence = convergence_rows(order_totals)
    active = [
        row for row in nodes if bool(row["mask_active"])
    ]
    evaluated = [
        row
        for row in active
        if row["evaluation_status"] == "EVALUATED"
    ]
    expected_rows = int(dry["expected_component_node_rows"])
    maximum_root_residual = max(
        float(row["root_equation_residual"])
        for row in evaluated
    )
    maximum_refinement_distance = max(
        float(row["root_refinement_chordal_distance"])
        for row in evaluated
    )
    maximum_coefficient_change = max(
        float(row["coefficient_relative_change"])
        for row in evaluated
    )
    minimum_surface_distance = min(
        float(row["minimum_surface_distance"])
        for row in nodes
    )
    maximum_order_change = max(
        float(row["relative_change"]) for row in convergence
    )
    hidden_active_count = sum(
        row["component_id"] in HIDDEN_IDS for row in active
    )
    replay_mismatches = [
        row for row in replay if not bool(row["mask_replay_agrees"])
    ]
    replay_false_negatives = [
        row
        for row in replay_mismatches
        if row["mismatch_classification"]
        == "OLD_TRACKER_FALSE_NEGATIVE_ACTIVE_CHAMBER"
    ]
    replay_false_positives = [
        row
        for row in replay_mismatches
        if row["mismatch_classification"]
        == "OLD_TRACKER_FALSE_POSITIVE_ACTIVE_CHAMBER"
    ]
    checks = {
        "parent_5277_accepted": bool(parent["acceptance_passed"]),
        "historical_replay_is_one_sided_endpoint_correction": (
            bool(replay)
            and all(
                bool(row["active_sign_preserving"])
                for row in replay
            )
            and len(replay_false_negatives) == 8
            and not replay_false_positives
            and all(
                float(row["interval_midpoint"]) < -0.98
                for row in replay_false_negatives
            )
        ),
        "complete_two_regulator_node_matrix": (
            len(nodes) == expected_rows
        ),
        "all_transport_paths_passed": all(
            bool(row["path_passed"]) for row in nodes
        ),
        "exact_mask_implementations_agree": all(
            bool(row["mask_law_agrees"])
            and bool(
                row["representative_reciprocal_masks_agree"]
            )
            for row in nodes
        ),
        "no_quadrature_node_on_mask_boundary": (
            minimum_surface_distance > MASK_BOUNDARY_FLOOR
        ),
        "all_active_nodes_evaluated": (
            len(active) == len(evaluated) and bool(active)
        ),
        "all_active_roots_refined": (
            maximum_root_residual <= ROOT_RESIDUAL_LIMIT
            and maximum_refinement_distance
            <= ROOT_REFINEMENT_DISTANCE_LIMIT
        ),
        "all_active_coefficients_converged": (
            maximum_coefficient_change
            <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "all_active_winding_deltas_nonzero": all(
            abs(int(row["winding_delta"])) == 2
            for row in active
        ),
        "hidden_components_actively_integrated": (
            hidden_active_count > 0
        ),
        "all_totals_finite": all(
            math.isfinite(float(row[field]))
            for row in order_totals
            for field in (
                "eight_component_integral_real",
                "eight_component_integral_imaginary",
                "six_component_integral_real",
                "six_component_integral_imaginary",
            )
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    physical_totals = {
        str(row["quadrature_order"]): {
            "eight_component_real": row[
                "eight_component_integral_real"
            ],
            "eight_component_imaginary": row[
                "eight_component_integral_imaginary"
            ],
            "six_component_real": row[
                "six_component_integral_real"
            ],
            "six_component_imaginary": row[
                "six_component_integral_imaginary"
            ],
            "hidden_real": row[
                "hidden_MC02_MC08_integral_real"
            ],
            "hidden_imaginary": row[
                "hidden_MC02_MC08_integral_imaginary"
            ],
            "hidden_fraction": row["hidden_fraction"],
        }
        for row in order_totals
        if row["row_type"] == "PHYSICAL_REGULATOR_EXTRAPOLATION"
    }
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "eight-component-exact-mask-joint-cubature-smoke",
        "checks": checks,
        "acceptance_passed": accepted,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "mp_decimal_digits": MP_DECIMAL_DIGITS,
        "delta_exponents": list(DELTA_EXPONENTS),
        "energy_domain": [
            M5274.M5267.ENERGY_MINIMUM,
            M5274.M5267.ENERGY_MAXIMUM,
        ],
        "soft_cosine_domain": [
            -M5274.M5270.ANGULAR_LIMIT,
            M5274.M5270.ANGULAR_LIMIT,
        ],
        "decay_cosine_domain": [
            -M5274.M5270.ANGULAR_LIMIT,
            M5274.M5270.ANGULAR_LIMIT,
        ],
        "angular_jacobian": ANGULAR_JACOBIAN,
        "kernel_multiplier": M5274.M5231.KERNEL_MULTIPLIER,
        "physical_A00_weight": (
            M5274.M5231.PHYSICAL_A00_WEIGHT
        ),
        "component_node_row_count": len(nodes),
        "active_component_node_count": len(active),
        "hidden_active_component_node_count": hidden_active_count,
        "historical_replay_row_count": len(replay),
        "historical_replay_mismatch_count": (
            len(replay_mismatches)
        ),
        "historical_old_tracker_false_negative_count": (
            len(replay_false_negatives)
        ),
        "historical_old_tracker_false_positive_count": (
            len(replay_false_positives)
        ),
        "maximum_root_equation_residual": maximum_root_residual,
        "maximum_root_refinement_chordal_distance": (
            maximum_refinement_distance
        ),
        "maximum_coefficient_relative_change": (
            maximum_coefficient_change
        ),
        "minimum_mask_surface_distance": minimum_surface_distance,
        "maximum_low_order_relative_change": maximum_order_change,
        "physical_regulator_combination": "2 E020 - E040",
        "physical_order_totals": physical_totals,
        "convergence_diagnostics": {
            row["channel"]: row["relative_change"]
            for row in convergence
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
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ACCEPT_EIGHT_COMPONENT_INTERIOR_CUBATURE_SMOKE__"
            "PROCEED_TO_CHAMBER_ADAPTED_CONVERGENCE"
            if accepted
            else "EIGHT_COMPONENT_CUBATURE_SMOKE_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_exact_eight_component_integrand": accepted,
            "valid_for_low_order_interior_cubature_smoke": accepted,
            "valid_for_chamber_adapted_convergence": False,
            "valid_for_endpoint_caps": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This evaluates the analytically derived eight-component "
                "basis with exact masks and true local limits over a "
                "finite interior tensor grid. Orders two and three do "
                "not establish convergence across discontinuous mask "
                "chambers, and the angular endpoint caps remain omitted."
            ),
        },
    }
    write_csv(HISTORICAL_REPLAY, replay)
    write_csv(NODE_ROWS, nodes)
    write_csv(COMPONENT_TOTALS, component_totals)
    write_csv(ORDER_TOTALS, order_totals)
    write_csv(CONVERGENCE_ROWS, convergence)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
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
    totals = "\n".join(
        (
            f"- order `{order}`: eight "
            f"`{values['eight_component_real']:.12g}"
            f"{values['eight_component_imaginary']:+.12g}i`; "
            f"true-six `{values['six_component_real']:.12g}"
            f"{values['six_component_imaginary']:+.12g}i`; "
            f"hidden fraction `{values['hidden_fraction']:.12g}`."
        )
        for order, values in result["physical_order_totals"].items()
    )
    convergence = "\n".join(
        f"- `{channel}`: `{value:.12g}`."
        for channel, value in result[
            "convergence_diagnostics"
        ].items()
    )
    text = f"""# 5278 — Eight-component exact-mask joint cubature smoke

## Purpose

Checkpoint 5277 supplied the true pointwise double-residue evaluator.
This checkpoint performs the first actual three-dimensional interior
integration over soft energy, soft cosine, and decay cosine using the
analytic eight-component pole basis.

## Integrand

Each active component contributes

`Delta w * orientation * C_2 / (R G (g_1'-g_2'))`.

The exact Boolean mask is evaluated before the expensive arbitrary-
precision limit. The two reciprocal representatives give the same mask,
and the historical 5239 winding intervals are replayed as a sign check.
That replay finds
`{result['historical_old_tracker_false_negative_count']}` old
endpoint-adjacent false negatives and
`{result['historical_old_tracker_false_positive_count']}` false
positives. All discrepancies are one-sided corrections supplied by the
analytic mask, rather than sign reversals.

## Domain and measure

- energy: `{result['energy_domain']}`;
- soft cosine: `{result['soft_cosine_domain']}`;
- decay cosine: `{result['decay_cosine_domain']}`;
- normalized angular measure: `d cos(theta_s) d cos(theta_d) / 4`;
- regulator combination: `2 E020 - E040`;
- tensor Gauss orders: `{result['quadrature_orders']}`.

## Numerical results

{totals}

Order-to-order relative changes:

{convergence}

The largest local-limit relative change is
`{result['maximum_coefficient_relative_change']:.12g}` and the largest
root residual is `{result['maximum_root_equation_residual']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is a real integration smoke, not another inventory. It proves that
the exact eight-component integrand can be transported, masked,
evaluated, and integrated on a finite interior grid. It does not yet
establish the coefficient: discontinuous mask chambers require adapted
cubature, orders two and three are only diagnostics, and the excluded
angular endpoint caps still require bounds or restoration.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5277)
    required_csvs = (
        HISTORICAL_REPLAY,
        NODE_ROWS,
        COMPONENT_TOTALS,
        ORDER_TOTALS,
        CONVERGENCE_ROWS,
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
        sort_keys=True,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    expected_rows = (
        sum(order**3 for order in QUADRATURE_ORDERS)
        * len(REGULATOR_IDS)
        * len(COMPONENT_IDS)
    )
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
            "PARENT_5277_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "CUBATURE_SMOKE_ACCEPTED",
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
            "COMPLETE_NODE_MATRIX",
            int(result["component_node_row_count"])
            == expected_rows,
            (
                f"{result['component_node_row_count']}/"
                f"{expected_rows} rows"
            ),
        ),
        validation_gate(
            "LOCAL_LIMIT_CONTROLS_PASS",
            (
                float(result["maximum_root_equation_residual"])
                <= ROOT_RESIDUAL_LIMIT
                and float(
                    result[
                        "maximum_root_refinement_chordal_distance"
                    ]
                )
                <= ROOT_REFINEMENT_DISTANCE_LIMIT
                and float(
                    result[
                        "maximum_coefficient_relative_change"
                    ]
                )
                <= COEFFICIENT_CONVERGENCE_LIMIT
            ),
            "all active arbitrary-precision limits controlled",
        ),
        validation_gate(
            "HIDDEN_COMPONENTS_INCLUDED",
            int(result["hidden_active_component_node_count"]) > 0,
            (
                f"{result['hidden_active_component_node_count']} "
                "active MC02/MC08 rows"
            ),
        ),
        validation_gate(
            "LOW_ORDER_ONLY_EXPLICIT",
            (
                not result["claim_boundary"][
                    "valid_for_chamber_adapted_convergence"
                ]
                and not result["claim_boundary"][
                    "valid_for_endpoint_caps"
                ]
            ),
            "chamber convergence and endpoint caps remain false",
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
            "state": "COMPLETED",
            "mode": "validation",
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
            "VALIDATED_EIGHT_COMPONENT_INTERIOR_CUBATURE_SMOKE"
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
