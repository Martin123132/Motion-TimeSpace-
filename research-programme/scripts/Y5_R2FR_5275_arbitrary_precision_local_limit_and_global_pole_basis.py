from __future__ import annotations

import argparse
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
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5275"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5274 = (
    SCRIPTS
    / "Y5_R2FR_5274_full_safe_component_materiality_and_mask_insertion_audit.py"
)
SCRIPT_5040_MP = (
    SCRIPTS / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
)
RESULT_5274 = (
    FUNCTIONAL_RG
    / "5274"
    / "full_safe_component_materiality_result.json"
)
VALIDATION_5274 = (
    FUNCTIONAL_RG
    / "5274"
    / "full_safe_component_materiality_validation.csv"
)
TARGET_POINTS_5274 = (
    FUNCTIONAL_RG / "5274" / "materiality_target_points.csv"
)
MATERIALITY_5274 = (
    FUNCTIONAL_RG
    / "5274"
    / "transported_component_pole_order_audit.csv"
)
COMPONENT_MAP_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_regulator_component_map.csv"
)

DRY_RUN = SOURCE / "arbitrary_precision_local_limit_dry_run.json"
TARGET_POINTS = SOURCE / "high_precision_target_points.csv"
PATH_DIAGNOSTICS = SOURCE / "high_precision_transport_diagnostics.csv"
LIMIT_ROWS = SOURCE / "owner_resolved_local_coefficient_limits.csv"
POLE_BASIS = SOURCE / "generic_global_pole_basis.csv"
CLASSIFIER_COMPARISON = (
    SOURCE / "double_precision_classifier_comparison.csv"
)
RESULT = SOURCE / "arbitrary_precision_global_pole_basis_result.json"
VALIDATION = SOURCE / "arbitrary_precision_global_pole_basis_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5275_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5275-Y5-R2FR-arbitrary-precision-local-limit-and-global-pole-basis.md"
)

CHECKPOINT = 5275
PARENT_CHECKPOINT = 5274
MARKER = "MTS_5275_ARBITRARY_PRECISION_LOCAL_LIMIT_AND_GLOBAL_POLE_BASIS"
REVISION = "arbitrary-precision-local-limit-global-pole-basis-v1"
TARGET_POINT_IDS = ("P000", "P001", "P004", "P024", "P046")
REGULATOR_IDS = ("E040", "E020")
MP_DECIMAL_DIGITS = 80
DELTA_EXPONENTS = (8, 16, 24)
ROOT_RESIDUAL_LIMIT = 1.0e-50
ROOT_REFINEMENT_DISTANCE_LIMIT = 1.0e-7
DOUBLE_ORDER_LIMIT = 0.2
SIMPLE_ORDER_MINIMUM = 0.8
SIMPLE_ORDER_MAXIMUM = 1.2
DOUBLE_COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
EXPECTED_DOUBLE_COMPONENTS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
EXPECTED_SIMPLE_COMPONENTS = (
    "MC01",
    "MC05",
    "MC06",
    "MC09",
    "MC10",
    "MC11",
    "MC13",
)
EXPECTED_DIRECT_DOUBLE_COMPONENTS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
)
EXPECTED_SUBTRACTION_DOUBLE_COMPONENTS = ("MC14", "MC15")
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


M5274 = load_module("mts_5274_for_5275", SCRIPT_5274)
M5040_MP = load_module("mts_5040_mp_for_5275", SCRIPT_5040_MP)
mp = M5040_MP.mp


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
        SCRIPT_5274,
        SCRIPT_5040_MP,
        RESULT_5274,
        VALIDATION_5274,
        TARGET_POINTS_5274,
        MATERIALITY_5274,
        COMPONENT_MAP_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5274.formal_inventory_digest())


def selected_target_points() -> list[dict[str, Any]]:
    by_id = {
        row["point_id"]: row for row in read_csv(TARGET_POINTS_5274)
    }
    return [
        {
            "point_id": point_id,
            "soft_energy": by_id[point_id]["soft_energy"],
            "soft_cosine": by_id[point_id]["soft_cosine"],
            "decay_cosine": by_id[point_id]["decay_cosine"],
            "is_source_event": by_id[point_id]["is_source_event"],
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for point_id in TARGET_POINT_IDS
    ]


def event_as_float(point: dict[str, Any]) -> dict[str, float]:
    return {
        coordinate: float(point[coordinate])
        for coordinate in (
            "soft_energy",
            "soft_cosine",
            "decay_cosine",
        )
    }


def event_as_mp(point: dict[str, Any]) -> dict[str, Any]:
    return {
        coordinate: mp.mpf(str(point[coordinate]))
        for coordinate in (
            "soft_energy",
            "soft_cosine",
            "decay_cosine",
        )
    }


def source_direction(
    source_name: str,
    soft_direction: list[Any],
    decay_direction: list[Any],
    internal: list[list[Any]],
) -> list[Any]:
    if source_name.startswith("direct:g"):
        internal_index = int(source_name.rsplit("g", 1)[1]) - 1
        return [
            internal[internal_index][component]
            / internal[internal_index][0]
            for component in range(1, 4)
        ]
    if source_name == "subtraction:soft":
        return soft_direction
    if source_name == "subtraction:decay":
        return decay_direction
    raise ValueError(f"unsupported source name: {source_name}")


def target_as_mp(target: complex) -> Any:
    return mp.mpc(
        mp.mpf(repr(float(target.real))),
        mp.mpf(repr(float(target.imag))),
    )


def local_root_data(
    event: dict[str, Any],
    target: Any,
    labels: tuple[str, str],
    relative_root: Any,
) -> tuple[
    list[Any],
    list[Any],
    list[list[Any]],
    tuple[Any, Any],
]:
    soft_direction, decay_direction, internal = (
        M5040_MP.event_geometry(
            event["soft_energy"],
            event["soft_cosine"],
            event["decay_cosine"],
            relative_root,
        )
    )
    global_roots: list[Any] = []
    for label in labels:
        source_name, root_label = label.rsplit(":", 1)
        direction = source_direction(
            source_name,
            soft_direction,
            decay_direction,
            internal,
        )
        global_roots.append(
            M5040_MP.factor_root(
                direction,
                target,
                root_label,
            )
        )
    return (
        soft_direction,
        decay_direction,
        internal,
        (global_roots[0], global_roots[1]),
    )


def refine_relative_root(
    event: dict[str, Any],
    target: Any,
    labels: tuple[str, str],
    initial_root: complex,
) -> tuple[Any, float, float]:
    initial = mp.mpc(
        mp.mpf(repr(float(initial_root.real))),
        mp.mpf(repr(float(initial_root.imag))),
    )

    def collision_equation(relative_root: Any) -> Any:
        *_, roots = local_root_data(
            event,
            target,
            labels,
            relative_root,
        )
        return roots[0] - roots[1]

    perturbation = mp.mpf("1e-10")
    refined = mp.findroot(
        collision_equation,
        (
            initial * (1 - perturbation),
            initial * (1 + perturbation),
        ),
        tol=mp.mpf("1e-60"),
        maxsteps=100,
    )
    residual = abs(collision_equation(refined))
    distance = M5274.M5237.M5030.chordal_distance(
        complex(initial_root),
        complex(refined),
    )
    return refined, float(residual), float(distance)


def coefficient_order(
    first_magnitude: Any,
    last_magnitude: Any,
) -> float:
    floor = mp.mpf("1e-300")
    first = max(abs(first_magnitude), floor)
    last = max(abs(last_magnitude), floor)
    exponent_span = DELTA_EXPONENTS[-1] - DELTA_EXPONENTS[0]
    return float(-mp.log10(last / first) / exponent_span)


def classify_coefficient_order(order: float) -> str:
    if abs(order) <= DOUBLE_ORDER_LIMIT:
        return "DOUBLE_POLE"
    if SIMPLE_ORDER_MINIMUM <= order <= SIMPLE_ORDER_MAXIMUM:
        return "SIMPLE_POLE"
    if 1.8 <= order <= 2.2:
        return "FINITE"
    return "UNRESOLVED"


def relative_complex_difference(first: Any, second: Any) -> float:
    return float(
        abs(first - second)
        / max(abs(first), abs(second), mp.mpf("1e-100"))
    )


def coefficient_limit_row(
    epsilon_id: str,
    point: dict[str, Any],
    component: dict[str, Any],
    transported_pair: tuple[complex, complex],
    scattering_target: complex,
    source_material: bool,
    double_precision_classification: str,
    path_passed: bool,
) -> dict[str, Any]:
    if abs(transported_pair[0]) >= 1.0:
        entry = component["representative"]
        initial_root = transported_pair[0]
        selected_role = "representative"
    else:
        entry = component["reciprocal"]
        initial_root = transported_pair[1]
        selected_role = "reciprocal"
    labels = M5274.pair_labels(entry)
    high_precision_event = event_as_mp(point)
    high_precision_target = target_as_mp(scattering_target)
    relative_root, root_residual, refinement_distance = (
        refine_relative_root(
            high_precision_event,
            high_precision_target,
            labels,
            initial_root,
        )
    )
    (
        soft_direction,
        decay_direction,
        internal,
        global_roots,
    ) = local_root_data(
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
    direct_order = coefficient_order(
        abs(direct_coefficients[0]),
        abs(direct_coefficients[-1]),
    )
    subtraction_order = coefficient_order(
        abs(subtraction_coefficients[0]),
        abs(subtraction_coefficients[-1]),
    )
    total_order = coefficient_order(
        abs(total_coefficients[0]),
        abs(total_coefficients[-1]),
    )
    direct_classification = classify_coefficient_order(direct_order)
    subtraction_classification = classify_coefficient_order(
        subtraction_order
    )
    total_classification = classify_coefficient_order(total_order)
    if total_classification != "DOUBLE_POLE":
        double_pole_owner = "none"
    elif (
        direct_classification == "DOUBLE_POLE"
        and subtraction_classification != "DOUBLE_POLE"
    ):
        double_pole_owner = "direct"
    elif (
        subtraction_classification == "DOUBLE_POLE"
        and direct_classification != "DOUBLE_POLE"
    ):
        double_pole_owner = "endpoint_subtraction"
    else:
        double_pole_owner = "mixed"
    total_convergence = relative_complex_difference(
        total_coefficients[-2],
        total_coefficients[-1],
    )
    return {
        "epsilon_id": epsilon_id,
        "point_id": point["point_id"],
        "component_id": component["component_id"],
        "family": component["family"],
        "owner_summand": component["owner_summand"],
        "source_material": source_material,
        "selected_role": selected_role,
        "representing_pair": "|".join(labels),
        "path_passed": path_passed,
        "mp_decimal_digits": MP_DECIMAL_DIGITS,
        "delta_exponents": "|".join(
            str(value) for value in DELTA_EXPONENTS
        ),
        "relative_root_real": mp.nstr(mp.re(relative_root), 32),
        "relative_root_imaginary": mp.nstr(mp.im(relative_root), 32),
        "global_root_real": mp.nstr(mp.re(global_root), 32),
        "global_root_imaginary": mp.nstr(mp.im(global_root), 32),
        "root_equation_residual": root_residual,
        "root_refinement_chordal_distance": refinement_distance,
        "direct_coefficient_order": direct_order,
        "subtraction_coefficient_order": subtraction_order,
        "total_coefficient_order": total_order,
        "direct_classification": direct_classification,
        "subtraction_classification": subtraction_classification,
        "total_classification": total_classification,
        "double_pole_owner": double_pole_owner,
        "direct_limit_real": mp.nstr(
            mp.re(direct_coefficients[-1]), 32
        ),
        "direct_limit_imaginary": mp.nstr(
            mp.im(direct_coefficients[-1]), 32
        ),
        "direct_limit_magnitude": float(
            abs(direct_coefficients[-1])
        ),
        "subtraction_limit_real": mp.nstr(
            mp.re(subtraction_coefficients[-1]), 32
        ),
        "subtraction_limit_imaginary": mp.nstr(
            mp.im(subtraction_coefficients[-1]), 32
        ),
        "subtraction_limit_magnitude": float(
            abs(subtraction_coefficients[-1])
        ),
        "total_limit_real": mp.nstr(
            mp.re(total_coefficients[-1]), 32
        ),
        "total_limit_imaginary": mp.nstr(
            mp.im(total_coefficients[-1]), 32
        ),
        "total_limit_magnitude": float(
            abs(total_coefficients[-1])
        ),
        "total_limit_relative_change": total_convergence,
        "double_precision_classification": (
            double_precision_classification
        ),
        "classifier_disagrees": (
            (
                double_precision_classification
                == "LOWER_THAN_DOUBLE_POLE"
            )
            != (total_classification != "DOUBLE_POLE")
        ),
        "valid_for_generic_pole_basis": True,
        "valid_for_global_pointwise_pole_theorem": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def pole_basis_rows(
    limit_rows: list[dict[str, Any]],
    component_map: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    component_ids = sorted(
        {str(row["component_id"]) for row in limit_rows}
    )
    for component_id in component_ids:
        local = [
            row
            for row in limit_rows
            if row["component_id"] == component_id
        ]
        classifications = sorted(
            {str(row["total_classification"]) for row in local}
        )
        owners = sorted(
            {str(row["double_pole_owner"]) for row in local}
        )
        stable = len(classifications) == 1
        generic_classification = (
            classifications[0] if stable else "UNRESOLVED"
        )
        source_material = (
            component_map[component_id]["material"].lower() == "true"
        )
        rows.append(
            {
                "component_id": component_id,
                "family": local[0]["family"],
                "owner_summand": local[0]["owner_summand"],
                "source_material": source_material,
                "sample_count": len(local),
                "generic_classification": generic_classification,
                "observed_classifications": "|".join(classifications),
                "double_pole_owners": "|".join(owners),
                "classification_stable": stable,
                "minimum_total_limit_magnitude": min(
                    float(row["total_limit_magnitude"])
                    for row in local
                ),
                "maximum_total_limit_magnitude": max(
                    float(row["total_limit_magnitude"])
                    for row in local
                ),
                "maximum_double_coefficient_relative_change": max(
                    float(row["total_limit_relative_change"])
                    for row in local
                    if row["total_classification"]
                    == "DOUBLE_POLE"
                )
                if generic_classification == "DOUBLE_POLE"
                else "",
                "hidden_by_5239_source_material_floor": (
                    not source_material
                    and generic_classification == "DOUBLE_POLE"
                ),
                "retain_in_generic_cubature_basis": (
                    generic_classification == "DOUBLE_POLE"
                ),
                "valid_for_generic_pole_basis": stable,
                "valid_for_global_pointwise_pole_theorem": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def classifier_comparison_rows(
    limit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "epsilon_id": row["epsilon_id"],
            "point_id": row["point_id"],
            "component_id": row["component_id"],
            "source_material": row["source_material"],
            "double_precision_classification": row[
                "double_precision_classification"
            ],
            "arbitrary_precision_classification": row[
                "total_classification"
            ],
            "classifier_disagrees": row["classifier_disagrees"],
            "total_limit_magnitude": row["total_limit_magnitude"],
            "total_coefficient_order": row["total_coefficient_order"],
            "conclusion": (
                "FIXED_DISPLACEMENT_MISCLASSIFIED_SMALL_DOUBLE_COEFFICIENT"
                if row["classifier_disagrees"]
                else "CLASSIFIERS_AGREE"
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for row in limit_rows
    ]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5274,
        SCRIPT_5040_MP,
        RESULT_5274,
        VALIDATION_5274,
        TARGET_POINTS_5274,
        MATERIALITY_5274,
        COMPONENT_MAP_5239,
    )
    parent = read_json(RESULT_5274)
    parent_validation = read_csv(VALIDATION_5274)
    points = selected_target_points()
    components = read_csv(COMPONENT_MAP_5239)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5274_accepted": bool(parent["acceptance_passed"]),
        "parent_5274_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "parent_rejected_fixed_six_basis": (
            not bool(parent["fixed_six_component_basis_supported"])
        ),
        "five_target_points_loaded": len(points) == 5,
        "fifteen_components_loaded": len(components) == 15,
        "mpmath_precision_available": hasattr(mp, "findroot"),
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
        "decision": (
            "DRY_RUN_ACCEPTED__EVALUATE_OWNER_RESOLVED_LOCAL_LIMITS"
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
        raise RuntimeError("5275 dry run did not pass")
    parent = read_json(RESULT_5274)
    contract = M5274.M5239.source_contract()
    source_event = M5274.M5239.source_event(contract)
    points = selected_target_points()
    component_map = {
        row["component_id"]: row
        for row in read_csv(COMPONENT_MAP_5239)
    }
    old_classifier = {
        (
            row["epsilon_id"],
            row["point_id"],
            row["component_id"],
        ): row["classification"]
        for row in read_csv(MATERIALITY_5274)
    }
    path_rows: list[dict[str, Any]] = []
    limit_rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        (
            scattering_target,
            components,
            _,
        ) = M5274.component_inventory(
            epsilon_id,
            source_event,
            contract,
        )
        for point in points:
            target_event = event_as_float(point)
            (
                transported,
                resolution,
                maximum_step,
                maximum_reciprocal,
            ) = M5274.transport_components(
                components,
                source_event,
                target_event,
                scattering_target,
            )
            path_passed = (
                maximum_step <= M5274.PATH_STEP_LIMIT
                and maximum_reciprocal
                <= M5274.RECIPROCAL_RESIDUAL_LIMIT
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
            for component in sorted(
                components,
                key=lambda row: str(row["component_id"]),
            ):
                component_id = str(component["component_id"])
                map_row = component_map[component_id]
                limit_rows.append(
                    coefficient_limit_row(
                        epsilon_id=epsilon_id,
                        point=point,
                        component=component,
                        transported_pair=transported[component_id],
                        scattering_target=scattering_target,
                        source_material=(
                            map_row["material"].lower() == "true"
                        ),
                        double_precision_classification=old_classifier[
                            (
                                epsilon_id,
                                point["point_id"],
                                component_id,
                            )
                        ],
                        path_passed=path_passed,
                    )
                )
    basis_rows = pole_basis_rows(limit_rows, component_map)
    comparison_rows = classifier_comparison_rows(limit_rows)
    double_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["generic_classification"] == "DOUBLE_POLE"
    )
    simple_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["generic_classification"] == "SIMPLE_POLE"
    )
    direct_double_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["double_pole_owners"] == "direct"
    )
    subtraction_double_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["double_pole_owners"] == "endpoint_subtraction"
    )
    hidden_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if bool(row["hidden_by_5239_source_material_floor"])
    )
    maximum_root_residual = max(
        float(row["root_equation_residual"]) for row in limit_rows
    )
    maximum_refinement_distance = max(
        float(row["root_refinement_chordal_distance"])
        for row in limit_rows
    )
    maximum_double_convergence = max(
        float(row["total_limit_relative_change"])
        for row in limit_rows
        if row["total_classification"] == "DOUBLE_POLE"
    )
    checks = {
        "parent_5274_accepted": bool(parent["acceptance_passed"]),
        "all_transport_paths_pass": all(
            bool(row["path_passed"]) for row in path_rows
        ),
        "all_roots_refined": (
            maximum_root_residual <= ROOT_RESIDUAL_LIMIT
            and maximum_refinement_distance
            <= ROOT_REFINEMENT_DISTANCE_LIMIT
        ),
        "complete_limit_matrix": (
            len(limit_rows)
            == len(REGULATOR_IDS) * len(points) * len(component_map)
        ),
        "all_component_classifications_stable": all(
            bool(row["classification_stable"])
            for row in basis_rows
        ),
        "eight_generic_double_components": (
            double_ids == list(EXPECTED_DOUBLE_COMPONENTS)
        ),
        "seven_generic_simple_components": (
            simple_ids == list(EXPECTED_SIMPLE_COMPONENTS)
        ),
        "direct_double_owner_set_closes": (
            direct_double_ids
            == list(EXPECTED_DIRECT_DOUBLE_COMPONENTS)
        ),
        "subtraction_double_owner_set_closes": (
            subtraction_double_ids
            == list(EXPECTED_SUBTRACTION_DOUBLE_COMPONENTS)
        ),
        "hidden_source_components_identified": (
            hidden_ids == ["MC02", "MC08"]
        ),
        "double_coefficients_converge": (
            maximum_double_convergence
            <= DOUBLE_COEFFICIENT_CONVERGENCE_LIMIT
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
        "mode": "arbitrary-precision-owner-resolved-local-limit",
        "checks": checks,
        "acceptance_passed": accepted,
        "mp_decimal_digits": MP_DECIMAL_DIGITS,
        "delta_exponents": list(DELTA_EXPONENTS),
        "target_point_ids": list(TARGET_POINT_IDS),
        "regulator_ids": list(REGULATOR_IDS),
        "component_count": len(component_map),
        "limit_row_count": len(limit_rows),
        "generic_double_component_count": len(double_ids),
        "generic_double_component_ids": double_ids,
        "generic_simple_component_count": len(simple_ids),
        "generic_simple_component_ids": simple_ids,
        "direct_double_component_ids": direct_double_ids,
        "subtraction_double_component_ids": subtraction_double_ids,
        "hidden_source_double_component_ids": hidden_ids,
        "double_precision_disagreement_count": sum(
            bool(row["classifier_disagrees"])
            for row in comparison_rows
        ),
        "maximum_root_equation_residual": maximum_root_residual,
        "maximum_root_refinement_chordal_distance": (
            maximum_refinement_distance
        ),
        "maximum_double_coefficient_relative_change": (
            maximum_double_convergence
        ),
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
            "REPLACE_SOURCE_SIX_WITH_GENERIC_EIGHT_COMPONENT_POLE_BASIS__"
            "PROCEED_TO_DENOMINATOR_INCIDENCE_PROOF"
            if accepted
            else "ARBITRARY_PRECISION_POLE_BASIS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_fixed_six_component_basis": False,
            "valid_for_generic_eight_component_pole_basis": accepted,
            "valid_for_eight_component_cubature_smoke": accepted,
            "valid_for_global_pointwise_pole_order_theorem": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The arbitrary-precision local limit resolves two "
                "small direct-sector double coefficients hidden by "
                "the 5239 fixed-displacement classifier. The "
                "eight-component basis is generic and sampled across "
                "five events and two regulators; a denominator-incidence "
                "proof is still required for a global theorem."
            ),
        },
    }
    write_csv(TARGET_POINTS, points)
    write_csv(PATH_DIAGNOSTICS, path_rows)
    write_csv(LIMIT_ROWS, limit_rows)
    write_csv(POLE_BASIS, basis_rows)
    write_csv(CLASSIFIER_COMPARISON, comparison_rows)
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
    text = f"""# 5275 — Arbitrary-precision local limit and global pole basis

## Question

Checkpoint 5274 showed that the fixed-displacement double-precision pole
classifier changed its answer for MC02, MC03, MC07, and MC08. This
checkpoint evaluates the defining local coefficient directly:

`C_2 = lim_(delta -> 0) delta^2 I(z_0 + delta)`.

The limit is evaluated at `{MP_DECIMAL_DIGITS}` decimal digits and at
three displacement scales, with direct and endpoint-subtraction
summands kept separate.

## Result

The apparent component exchange was numerical, not topological.

- Generic double-pole basis ({result['generic_double_component_count']}):
  `{', '.join(result['generic_double_component_ids'])}`.
- Generic simple-pole complement ({result['generic_simple_component_count']}):
  `{', '.join(result['generic_simple_component_ids'])}`.
- Direct-owned doubles:
  `{', '.join(result['direct_double_component_ids'])}`.
- Endpoint-subtraction-owned doubles:
  `{', '.join(result['subtraction_double_component_ids'])}`.
- Hidden by the 5239 source-event material floor:
  `{', '.join(result['hidden_source_double_component_ids'])}`.
- Double-precision disagreements:
  **{result['double_precision_disagreement_count']}** of
  **{result['limit_row_count']}** local limits.

MC02 and MC08 have small but nonzero direct-sector double coefficients.
The regular background dominates at the old fixed displacement, causing
the old scaling estimate to report a lower pole. The arbitrary-precision
coefficient stabilizes as the displacement is reduced.

## Numerical controls

- Events: `{', '.join(result['target_point_ids'])}`.
- Regulators: `{', '.join(result['regulator_ids'])}`.
- Maximum refined collision residual:
  `{result['maximum_root_equation_residual']:.12g}`.
- Maximum root-refinement chordal displacement:
  `{result['maximum_root_refinement_chordal_distance']:.12g}`.
- Maximum double-coefficient relative change:
  `{result['maximum_double_coefficient_relative_change']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This replaces the source-event six-component list with an
eight-component *generic* pole basis and licenses only an
eight-component cubature smoke. Five events and two regulators do not
constitute a global pointwise theorem. No final phase-space coefficient,
UV coefficient, local-GR result, or full-MTS claim follows.

## Next derivation

Build the denominator-incidence proof. Show term by term that the seven
complement components cannot contain two simultaneous denominator
factors, while the six direct-owned and two subtraction-owned basis
components possess a generically nonzero double coefficient. This turns
the sampled generic basis into an analytic almost-everywhere statement.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5274)
    required_csvs = (
        TARGET_POINTS,
        PATH_DIAGNOSTICS,
        LIMIT_ROWS,
        POLE_BASIS,
        CLASSIFIER_COMPARISON,
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
            "PARENT_5274_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "ARBITRARY_PRECISION_AUDIT_ACCEPTED",
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
            "COMPLETE_LIMIT_MATRIX",
            int(result["limit_row_count"])
            == len(REGULATOR_IDS)
            * len(TARGET_POINT_IDS)
            * 15,
            f"{result['limit_row_count']} local limits",
        ),
        validation_gate(
            "EIGHT_COMPONENT_BASIS",
            result["generic_double_component_ids"]
            == list(EXPECTED_DOUBLE_COMPONENTS),
            "|".join(result["generic_double_component_ids"]),
        ),
        validation_gate(
            "SEVEN_COMPONENT_SIMPLE_COMPLEMENT",
            result["generic_simple_component_ids"]
            == list(EXPECTED_SIMPLE_COMPONENTS),
            "|".join(result["generic_simple_component_ids"]),
        ),
        validation_gate(
            "OWNER_DECOMPOSITION_CLOSES",
            (
                result["direct_double_component_ids"]
                == list(EXPECTED_DIRECT_DOUBLE_COMPONENTS)
                and result["subtraction_double_component_ids"]
                == list(EXPECTED_SUBTRACTION_DOUBLE_COMPONENTS)
            ),
            "six direct plus two endpoint-subtraction doubles",
        ),
        validation_gate(
            "HIDDEN_SOURCE_DOUBLES_IDENTIFIED",
            result["hidden_source_double_component_ids"]
            == ["MC02", "MC08"],
            "|".join(result["hidden_source_double_component_ids"]),
        ),
        validation_gate(
            "ROOT_AND_LIMIT_CONTROLS_PASS",
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
                        "maximum_double_coefficient_relative_change"
                    ]
                )
                <= DOUBLE_COEFFICIENT_CONVERGENCE_LIMIT
            ),
            "root residual, branch distance, and limit convergence",
        ),
        validation_gate(
            "SIX_COMPONENT_BASIS_REMAINS_FALSE",
            (
                not result["claim_boundary"][
                    "valid_for_fixed_six_component_basis"
                ]
                and result["claim_boundary"][
                    "valid_for_generic_eight_component_pole_basis"
                ]
            ),
            "six rejected; generic eight retained",
        ),
        validation_gate(
            "GLOBAL_THEOREM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_global_pointwise_pole_order_theorem"
            ],
            "sampled generic basis is not a pointwise theorem",
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
            "VALIDATED_ARBITRARY_PRECISION_EIGHT_COMPONENT_POLE_BASIS"
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
