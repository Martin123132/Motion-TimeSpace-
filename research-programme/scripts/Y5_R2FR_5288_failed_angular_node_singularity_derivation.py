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
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

from scipy.optimize import least_squares


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
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5288"

SCRIPT_5287 = (
    SCRIPTS / "Y5_R2FR_5287_order2_angular_inner_energy_smoke.py"
)
RESULT_5287 = (
    FUNCTIONAL_RG / "5287" / "order2_angular_inner_energy_result.json"
)
VALIDATION_5287 = (
    FUNCTIONAL_RG / "5287" / "order2_angular_inner_energy_validation.csv"
)
ANGULAR_NODES_5286 = FUNCTIONAL_RG / "5286" / "angular_order2_nodes.csv"
ENERGY_NODES_5287 = (
    FUNCTIONAL_RG / "5287" / "angular_node_energy_component_nodes.csv"
)

DRY_RUN = SOURCE / "failed_angular_node_singularity_dry_run.json"
SYMMETRY_AUDIT = SOURCE / "failed_node_MC03_MC08_symmetry_audit.csv"
SCANNED_POLES = SOURCE / "failed_node_geometric_pole_scan.csv"
CLASSIFIED_POLES = SOURCE / "failed_node_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "failed_node_channel_roots.csv"
POLE_SAMPLES = SOURCE / "failed_node_pole_numerator_samples.csv"
POLE_FITS = SOURCE / "failed_node_pole_residue_fits.csv"
POLE_RESIDUES = SOURCE / "failed_node_selected_pole_residues.csv"
ENDPOINT_FITS = SOURCE / "lower_endpoint_asymptotic_fits.csv"
ENDPOINT_SELECTED = SOURCE / "lower_endpoint_selected_coefficients.csv"
ENDPOINT_PHYSICAL = SOURCE / "lower_endpoint_physical_coefficients.csv"
RESULT = SOURCE / "failed_angular_node_singularity_result.json"
VALIDATION = SOURCE / "failed_angular_node_singularity_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5288_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5288-Y5-R2FR-failed-angular-node-singularity-derivation.md"

CHECKPOINT = 5288
PARENT_CHECKPOINT = 5287
MARKER = "MTS_5288_FAILED_ANGULAR_NODE_SINGULARITY_DERIVATION"
REVISION = "failed-angular-node-singularity-derivation-v1"
REGULATOR_IDS = ("E040", "E020")
POLE_TARGETS = (
    ("A02_S01_D02", "MC03"),
    ("A02_S02_D01", "MC08"),
)
POLE_OWNER_TARGET = POLE_TARGETS[0]
POLE_MIRROR_TARGET = POLE_TARGETS[1]
SYMMETRY_TEST_ENERGIES = (
    2.0e-4,
    2.0e-3,
    1.0e-1,
    5.0e-1,
    9.75e-1,
    9.825e-1,
    9.90e-1,
    9.98e-1,
)
SYMMETRY_RELATIVE_LIMIT = 1.0e-12
EXPECTED_ENDPOINT_PAIRS = {
    "A02_S01_D01": ("MC12", "MC15"),
    "A02_S01_D02": ("MC04", "MC14"),
    "A02_S02_D01": ("MC04", "MC14"),
    "A02_S02_D02": ("MC12", "MC15"),
}
EXPECTED_ENDPOINT_TARGETS = {
    (angular_node_id, component_id)
    for angular_node_id, component_ids in EXPECTED_ENDPOINT_PAIRS.items()
    for component_id in component_ids
}
FIT_FRACTIONS = (
    -1.0,
    -0.5,
    -0.25,
    -0.125,
    0.125,
    0.25,
    0.5,
    1.0,
)
FIT_DEGREES = (3, 4)
DERIVATIVE_STEPS = (1.0e-5, 3.0e-6, 1.0e-6)
ROOT_RESIDUAL_LIMIT = 1.0e-10
ROOT_SHIFT_LIMIT = 5.0e-5
DERIVATIVE_CHANGE_LIMIT = 2.0e-6
NUMERATOR_FIT_RESIDUAL_LIMIT = 1.0e-4
RESIDUE_REFINEMENT_CHANGE_LIMIT = 5.0e-4
RESIDUE_DEGREE_CHANGE_LIMIT = 5.0e-4
COEFFICIENT_CHANGE_LIMIT = 1.0e-6
MATERIAL_RESIDUE_FLOOR = 1.0e-3
REMOVABLE_RESIDUE_CEILING = 1.0e-4
ENDPOINT_UPPERS = (6.0e-4, 1.1e-3)
ENDPOINT_DEGREES = (2, 3)
ENDPOINT_FIT_RESIDUAL_LIMIT = 2.0e-5
ENDPOINT_REFINEMENT_CHANGE_LIMIT = 2.0e-4
ENDPOINT_DEGREE_CHANGE_LIMIT = 2.0e-4
ENDPOINT_EXPONENT_TOLERANCE = 5.0e-2
ENDPOINT_STRENGTH_RATIO_FLOOR = 0.25
ENDPOINT_ABSOLUTE_FLOOR = 1.0e-6
ENDPOINT_CANCELLATION_RELATIVE_LIMIT = 1.0e-8
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


M5287 = load_module("mts_5287_for_5288", SCRIPT_5287)
M5286 = M5287.M5286
M5280 = M5287.M5280
M5283 = M5287.M5283
M5267 = M5287.M5267
np = M5287.np
mp = M5287.mp


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5287,
        RESULT_5287,
        VALIDATION_5287,
        ANGULAR_NODES_5286,
        ENERGY_NODES_5287,
        M5267.MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def angular_node_lookup() -> dict[str, dict[str, str]]:
    return {
        row["angular_node_id"]: row
        for row in read_csv(ANGULAR_NODES_5286)
    }


def manifest_job(
    epsilon_id: str,
    component_id: str,
) -> dict[str, Any]:
    manifest = M5267.read_json(M5267.MANIFEST_5239)
    return next(
        job
        for job in manifest["jobs"]
        if job["epsilon_id"] == epsilon_id
        and job["component_id"] == component_id
    )


def scan_failed_node_poles() -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str, str], dict[str, Any]],
]:
    nodes = angular_node_lookup()
    rows: list[dict[str, Any]] = []
    problems: dict[tuple[str, str, str], dict[str, Any]] = {}
    angular_node_id, component_id = POLE_OWNER_TARGET
    node = nodes[angular_node_id]
    reusable = []
    if SCANNED_POLES.exists():
        reusable = [
            row
            for row in read_csv(SCANNED_POLES)
            if row["angular_node_id"] == angular_node_id
            and row["component_id"] == component_id
            and not parse_bool(row.get("symmetry_derived", False))
        ]
    for epsilon_id in REGULATOR_IDS:
        key = (angular_node_id, epsilon_id, component_id)
        problem = M5286.angular_problem(
            manifest_job(epsilon_id, component_id),
            float(node["soft_cosine"]),
            float(node["decay_cosine"]),
        )
        problems[key] = problem
        local_reusable = [
            row
            for row in reusable
            if row["epsilon_id"] == epsilon_id
        ]
        if local_reusable:
            rows.extend(local_reusable)
        else:
            _, _, poles, _ = M5267.M5239.scan_problem(problem)
            for source in poles:
                rows.append(
                    {
                        "angular_node_id": angular_node_id,
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        **source,
                        "symmetry_derived": False,
                        "valid_for_failed_node_pole_scan": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "POLE_SCAN",
                "last_completed_key": "|".join(key),
                "scanned_pole_count": len(rows),
            },
        )
    return rows, problems


def MC03_MC08_symmetry_audit(
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    nodes = angular_node_lookup()
    owner_node_id, owner_component_id = POLE_OWNER_TARGET
    mirror_node_id, mirror_component_id = POLE_MIRROR_TARGET
    owner_context = M5287.local_context(
        base_context,
        nodes[owner_node_id],
    )
    mirror_context = M5287.local_context(
        base_context,
        nodes[mirror_node_id],
    )
    owner_cache: dict[tuple[str, float, str], Any] = {}
    mirror_cache: dict[tuple[str, float, str], Any] = {}
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        for energy in SYMMETRY_TEST_ENERGIES:
            owner = M5287.evaluate_component_cached(
                owner_context,
                epsilon_id,
                owner_component_id,
                energy,
                owner_cache,
                convergence_audit=True,
            )
            mirror = M5287.evaluate_component_cached(
                mirror_context,
                epsilon_id,
                mirror_component_id,
                energy,
                mirror_cache,
                convergence_audit=True,
            )
            owner_value = complex(owner["residue"])
            mirror_value = complex(mirror["residue"])
            relative = relative_complex_difference(
                owner_value,
                mirror_value,
            )
            passed = (
                relative <= SYMMETRY_RELATIVE_LIMIT
                and parse_bool(owner["mask_active"])
                == parse_bool(mirror["mask_active"])
            )
            rows.append(
                {
                    "owner_angular_node_id": owner_node_id,
                    "owner_component_id": owner_component_id,
                    "mirror_angular_node_id": mirror_node_id,
                    "mirror_component_id": mirror_component_id,
                    "epsilon_id": epsilon_id,
                    "soft_energy": energy,
                    **complex_fields("owner_residue", owner_value),
                    **complex_fields("mirror_residue", mirror_value),
                    "relative_difference": relative,
                    "owner_mask_active": owner["mask_active"],
                    "mirror_mask_active": mirror["mask_active"],
                    "symmetry_passed": passed,
                    "valid_for_MC03_MC08_symmetry_transport": passed,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def mirror_MC03_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes = angular_node_lookup()
    owner_node_id, owner_component_id = POLE_OWNER_TARGET
    mirror_node_id, mirror_component_id = POLE_MIRROR_TARGET
    mirror_node = nodes[mirror_node_id]
    mirrored: list[dict[str, Any]] = []
    for source in rows:
        row = dict(source)
        row["angular_node_id"] = mirror_node_id
        row["component_id"] = mirror_component_id
        if "soft_cosine" in row:
            row["soft_cosine"] = mirror_node["soft_cosine"]
        if "decay_cosine" in row:
            row["decay_cosine"] = mirror_node["decay_cosine"]
        for field in ("job_id", "pole_id"):
            if field in row:
                row[field] = str(row[field]).replace(
                    owner_component_id,
                    mirror_component_id,
                )
        row["symmetry_derived"] = True
        row["symmetry_source_angular_node_id"] = owner_node_id
        row["symmetry_source_component_id"] = owner_component_id
        mirrored.append(row)
    return mirrored


def classify_exact_masks(
    scanned: list[dict[str, Any]],
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    nodes = angular_node_lookup()
    contexts = {
        node_id: M5287.local_context(base_context, nodes[node_id])
        for node_id, _ in POLE_TARGETS
    }
    rows: list[dict[str, Any]] = []
    for source in scanned:
        angular_node_id = source["angular_node_id"]
        epsilon_id = source["epsilon_id"]
        component_id = source["component_id"]
        context = contexts[angular_node_id]
        event = dict(context["source_event"])
        event["soft_energy"] = float(source["real_axis_center"])
        inventory = context["inventories"][epsilon_id]
        rationals = M5280.M5274.M5231.root_rationals(
            event,
            inventory["target"],
        )
        selection = M5280.M5279.algebraic_component_selector(
            event,
            inventory["target"],
            inventory["components"][component_id],
            rationals,
        )
        (
            exact_active,
            orientation,
            owned_labels,
            surface_values,
        ) = M5280.M5277.exact_mask_orientation(
            selection["selected_labels"],
            event,
            context["surfaces"],
        )
        rows.append(
            {
                "angular_node_id": angular_node_id,
                "soft_cosine": source["soft_cosine"],
                "decay_cosine": source["decay_cosine"],
                "epsilon_id": epsilon_id,
                "component_id": component_id,
                "pole_id": source["pole_id"],
                "primary_surface_id": source["primary_surface_id"],
                "real_axis_center": source["real_axis_center"],
                "pole_real": source["pole_real"],
                "pole_imaginary": source["pole_imaginary"],
                "old_causal_family_active": source[
                    "causal_family_active"
                ],
                "exact_mask_active": exact_active,
                "promoted_by_exact_mask": (
                    exact_active
                    and not parse_bool(source["causal_family_active"])
                ),
                "selected_role": selection["selected_role"],
                "representing_pair": "|".join(
                    selection["selected_labels"]
                ),
                "orientation": orientation,
                "first_label_owned": owned_labels[0],
                "second_label_owned": owned_labels[1],
                "first_surface_value": surface_values[0],
                "second_surface_value": surface_values[1],
                "reciprocal_residual": selection["reciprocal_residual"],
                "valid_for_failed_node_exact_mask_classification": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def channel_function(
    problem: dict[str, Any],
    surface_id: str,
) -> Callable[[complex], complex]:
    return lambda coordinate: complex(
        M5267.M5239.owner_surface_values(
            problem,
            complex(coordinate),
        )[surface_id]
    )


def central_derivative(
    function: Callable[[complex], complex],
    point: complex,
    step: float,
) -> complex:
    return (function(point + step) - function(point - step)) / (
        2.0 * step
    )


def refine_active_channel_roots(
    classified: list[dict[str, Any]],
    problems: dict[tuple[str, str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in classified:
        if not parse_bool(source["exact_mask_active"]):
            continue
        key = (
            source["angular_node_id"],
            source["epsilon_id"],
            source["component_id"],
        )
        surface_id = source["primary_surface_id"]
        channel = channel_function(problems[key], surface_id)
        initial = complex(
            float(source["pole_real"]),
            float(source["pole_imaginary"]),
        )
        initial_residual = abs(channel(initial))
        pole = initial
        best_pole = initial
        best_residual = initial_residual
        iteration = 0
        for iteration in range(1, 13):
            derivative = central_derivative(channel, pole, 1.0e-6)
            if abs(derivative) <= 1.0e-300:
                break
            updated = pole - channel(pole) / derivative
            if abs(updated - initial) > ROOT_SHIFT_LIMIT:
                break
            pole = updated
            residual = abs(channel(pole))
            if residual < best_residual:
                best_pole = pole
                best_residual = residual
            if residual <= ROOT_RESIDUAL_LIMIT:
                break
        pole = best_pole
        derivatives = [
            central_derivative(channel, pole, step)
            for step in DERIVATIVE_STEPS
        ]
        derivative = derivatives[-1]
        derivative_change = relative_complex_difference(
            derivatives[-1],
            derivatives[-2],
        )
        residual = best_residual
        shift = abs(pole - initial)
        passed = (
            residual <= ROOT_RESIDUAL_LIMIT
            and shift <= ROOT_SHIFT_LIMIT
            and derivative_change <= DERIVATIVE_CHANGE_LIMIT
        )
        if not passed:
            pole = initial
            residual = initial_residual
            shift = 0.0
            derivatives = [
                central_derivative(channel, pole, step)
                for step in DERIVATIVE_STEPS
            ]
            derivative = derivatives[-1]
            derivative_change = relative_complex_difference(
                derivatives[-1],
                derivatives[-2],
            )
        derivation_method = (
            "CHANNEL_NUMERATOR_OVER_DERIVATIVE"
            if passed
            else "DIRECT_LAURENT_FALLBACK"
        )
        rows.append(
            {
                "angular_node_id": source["angular_node_id"],
                "soft_cosine": source["soft_cosine"],
                "decay_cosine": source["decay_cosine"],
                "epsilon_id": source["epsilon_id"],
                "component_id": source["component_id"],
                "pole_id": source["pole_id"],
                "surface_id": surface_id,
                "source_center": source["real_axis_center"],
                "initial_pole_real": initial.real,
                "initial_pole_imaginary": initial.imag,
                "initial_channel_root_residual": initial_residual,
                "refined_pole_real": pole.real,
                "refined_pole_imaginary": pole.imag,
                "pole_refinement_shift": shift,
                "channel_root_residual": residual,
                "channel_derivative_real": derivative.real,
                "channel_derivative_imaginary": derivative.imag,
                "channel_derivative_relative_change": derivative_change,
                "newton_iteration_count": iteration,
                "residue_derivation_method": derivation_method,
                "channel_root_controls_pass": passed,
                "direct_laurent_fallback_authorized": not passed,
                "root_or_fallback_route_available": True,
                "valid_for_failed_node_channel_residue": passed,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def pole_fit_radii(
    root: dict[str, Any],
    roots: list[dict[str, Any]],
) -> tuple[float, float]:
    center = float(root["refined_pole_real"])
    minimum = float(M5267.ENERGY_MINIMUM)
    maximum = float(M5267.ENERGY_MAXIMUM)
    if not minimum < center < maximum:
        raise RuntimeError(
            "refined pole left the energy domain: "
            f"{root['angular_node_id']}|{root['epsilon_id']}|"
            f"{root['component_id']}|{root['pole_id']} at {center}"
        )
    neighbors = [
        abs(
            center
            - float(candidate["refined_pole_real"])
        )
        for candidate in roots
        if candidate["angular_node_id"] == root["angular_node_id"]
        and candidate["epsilon_id"] == root["epsilon_id"]
        and candidate["component_id"] == root["component_id"]
        and candidate["pole_id"] != root["pole_id"]
    ]
    separation = min(
        neighbors + [center - minimum, maximum - center]
    )
    coarse = min(4.0e-4, 0.16 * separation)
    return (
        coarse,
        0.5 * coarse,
        0.25 * coarse,
        0.125 * coarse,
    )


def direct_laurent_linear_fit(
    energies: Any,
    fractions: Any,
    values: Any,
    pole: complex,
    degree: int,
) -> tuple[Any, Any, float]:
    matrix = np.column_stack(
        [
            1.0 / (energies - pole),
            *[
                fractions**power
                for power in range(degree + 1)
            ],
        ]
    )
    coefficients, _, _, _ = np.linalg.lstsq(
        matrix,
        values,
        rcond=None,
    )
    predicted = matrix @ coefficients
    residual = float(
        np.max(np.abs(predicted - values))
        / max(float(np.max(np.abs(values))), 1.0e-300)
    )
    return coefficients, predicted, residual


def optimize_direct_laurent_pole(
    energies: Any,
    fractions: Any,
    values: Any,
    center: float,
    radius: float,
    seed: complex,
) -> complex:
    preliminary, _, _ = direct_laurent_linear_fit(
        energies,
        fractions,
        values,
        seed,
        max(FIT_DEGREES),
    )
    if abs(complex(preliminary[0])) <= MATERIAL_RESIDUE_FLOOR:
        return seed
    scaled_seed = np.asarray(
        [
            (seed.real - center) / radius,
            seed.imag / radius,
        ],
        dtype=float,
    )
    if abs(scaled_seed[1]) <= 1.0e-12:
        imaginary_bounds = (-0.5, 0.5)
    else:
        imaginary_bounds = tuple(
            sorted((0.5 * scaled_seed[1], 1.5 * scaled_seed[1]))
        )

    def residuals(parameters: Any) -> Any:
        candidate = complex(
            center + radius * float(parameters[0]),
            radius * float(parameters[1]),
        )
        _, predicted, _ = direct_laurent_linear_fit(
            energies,
            fractions,
            values,
            candidate,
            max(FIT_DEGREES),
        )
        scale = max(float(np.max(np.abs(values))), 1.0e-300)
        difference = (predicted - values) / scale
        return np.concatenate((difference.real, difference.imag))

    result = least_squares(
        residuals,
        scaled_seed,
        bounds=(
            np.asarray([-0.5, imaginary_bounds[0]], dtype=float),
            np.asarray([0.5, imaginary_bounds[1]], dtype=float),
        ),
        xtol=1.0e-14,
        ftol=1.0e-14,
        gtol=1.0e-14,
        max_nfev=500,
    )
    return complex(
        center + radius * float(result.x[0]),
        radius * float(result.x[1]),
    )


def derive_pole_residues(
    roots: list[dict[str, Any]],
    problems: dict[tuple[str, str, str], dict[str, Any]],
    base_context: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    nodes = angular_node_lookup()
    contexts = {
        node_id: M5287.local_context(base_context, nodes[node_id])
        for node_id, _ in POLE_TARGETS
    }
    caches: dict[
        str,
        dict[tuple[str, float, str], Any],
    ] = defaultdict(dict)
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    for root in roots:
        key = (
            root["angular_node_id"],
            root["epsilon_id"],
            root["component_id"],
        )
        channel = channel_function(
            problems[key],
            root["surface_id"],
        )
        pole = complex(
            float(root["refined_pole_real"]),
            float(root["refined_pole_imaginary"]),
        )
        derivative = complex(
            float(root["channel_derivative_real"]),
            float(root["channel_derivative_imaginary"]),
        )
        derivation_method = root["residue_derivation_method"]
        center = pole.real
        radii = pole_fit_radii(root, roots)
        local_fits: dict[tuple[float, int], dict[str, Any]] = {}
        direct_pole_seed = pole
        for radius_index, radius in enumerate(radii, start=1):
            local_samples: list[dict[str, Any]] = []
            for fraction in FIT_FRACTIONS:
                energy = center + radius * fraction
                if not M5267.ENERGY_MINIMUM < energy < M5267.ENERGY_MAXIMUM:
                    raise RuntimeError(
                        "pole-fit sample left energy domain: "
                        f"{key}|{root['pole_id']}|{energy}|{radius}"
                    )
                evaluation = M5287.evaluate_component_cached(
                    contexts[root["angular_node_id"]],
                    root["epsilon_id"],
                    root["component_id"],
                    energy,
                    caches[root["angular_node_id"]],
                    convergence_audit=True,
                )
                contribution = complex(evaluation["residue"])
                channel_value = channel(complex(energy))
                numerator = channel_value * contribution
                sample = {
                    "angular_node_id": root["angular_node_id"],
                    "epsilon_id": root["epsilon_id"],
                    "component_id": root["component_id"],
                    "pole_id": root["pole_id"],
                    "surface_id": root["surface_id"],
                    "residue_derivation_method": derivation_method,
                    "radius_index": radius_index,
                    "radius": radius,
                    "fraction": fraction,
                    "energy": energy,
                    **complex_fields("channel", channel_value),
                    **complex_fields("contribution", contribution),
                    **complex_fields("numerator", numerator),
                    "mask_active": evaluation["mask_active"],
                    "coefficient_relative_change": evaluation[
                        "coefficient_relative_change"
                    ],
                    "valid_for_failed_node_numerator_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                sample_rows.append(sample)
                local_samples.append(sample)
            fractions = np.asarray(
                [
                    complex(float(row["fraction"]))
                    for row in local_samples
                ],
                dtype=np.complex128,
            )
            numerators = np.asarray(
                [
                    complex(
                        float(row["numerator_real"]),
                        float(row["numerator_imaginary"]),
                    )
                    for row in local_samples
                ],
                dtype=np.complex128,
            )
            contributions = np.asarray(
                [
                    complex(
                        float(row["contribution_real"]),
                        float(row["contribution_imaginary"]),
                    )
                    for row in local_samples
                ],
                dtype=np.complex128,
            )
            energies = np.asarray(
                [
                    complex(float(row["energy"]))
                    for row in local_samples
                ],
                dtype=np.complex128,
            )
            scaled_pole = (pole - center) / radius
            fit_pole = pole
            if derivation_method == "DIRECT_LAURENT_FALLBACK":
                fit_pole = optimize_direct_laurent_pole(
                    energies,
                    fractions,
                    contributions,
                    center,
                    radius,
                    direct_pole_seed,
                )
                direct_pole_seed = fit_pole
            for degree in FIT_DEGREES:
                if (
                    derivation_method
                    == "CHANNEL_NUMERATOR_OVER_DERIVATIVE"
                ):
                    matrix = np.column_stack(
                        [
                            fractions**power
                            for power in range(degree + 1)
                        ]
                    )
                    fit_values = numerators
                    coefficients, _, _, _ = np.linalg.lstsq(
                        matrix,
                        fit_values,
                        rcond=None,
                    )
                    predicted = matrix @ coefficients
                    residual = float(
                        np.max(np.abs(predicted - fit_values))
                        / max(
                            float(np.max(np.abs(fit_values))),
                            1.0e-300,
                        )
                    )
                else:
                    (
                        coefficients,
                        predicted,
                        residual,
                    ) = direct_laurent_linear_fit(
                        energies,
                        fractions,
                        contributions,
                        fit_pole,
                        degree,
                    )
                    fit_values = contributions
                if (
                    derivation_method
                    == "CHANNEL_NUMERATOR_OVER_DERIVATIVE"
                ):
                    numerator_at_pole = sum(
                        coefficients[power] * scaled_pole**power
                        for power in range(degree + 1)
                    )
                    residue = numerator_at_pole / derivative
                else:
                    numerator_at_pole = 0.0j
                    residue = complex(coefficients[0])
                fit = {
                    "angular_node_id": root["angular_node_id"],
                    "epsilon_id": root["epsilon_id"],
                    "component_id": root["component_id"],
                    "pole_id": root["pole_id"],
                    "surface_id": root["surface_id"],
                    "residue_derivation_method": derivation_method,
                    "radius_index": radius_index,
                    "radius": radius,
                    "degree": degree,
                    "sample_count": len(local_samples),
                    "scaled_pole_magnitude": abs(scaled_pole),
                    "fitted_pole_real": fit_pole.real,
                    "fitted_pole_imaginary": fit_pole.imag,
                    "fitted_pole_shift_from_source": abs(
                        fit_pole - pole
                    ),
                    **complex_fields(
                        "numerator_at_pole",
                        numerator_at_pole,
                    ),
                    **complex_fields("fitted_residue", residue),
                    "fit_relative_residual": residual,
                    "all_samples_mask_active": all(
                        parse_bool(row["mask_active"])
                        for row in local_samples
                    ),
                    "maximum_coefficient_relative_change": max(
                        float(row["coefficient_relative_change"])
                        for row in local_samples
                    ),
                    "valid_for_failed_node_numerator_fit": True,
                    "valid_for_failed_node_pole_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                fit_rows.append(fit)
                local_fits[(radius, degree)] = fit
        selected = local_fits[(radii[-1], 3)]
        coarse = local_fits[(radii[0], 3)]
        alternate_degree = local_fits[(radii[-1], 4)]
        selected_value = complex(
            selected["fitted_residue_real"],
            selected["fitted_residue_imaginary"],
        )
        coarse_value = complex(
            coarse["fitted_residue_real"],
            coarse["fitted_residue_imaginary"],
        )
        degree_value = complex(
            alternate_degree["fitted_residue_real"],
            alternate_degree["fitted_residue_imaginary"],
        )
        refinement_change = relative_complex_difference(
            selected_value,
            complex(
                local_fits[(radii[-2], 3)]["fitted_residue_real"],
                local_fits[(radii[-2], 3)][
                    "fitted_residue_imaginary"
                ],
            ),
        )
        degree_change = relative_complex_difference(
            selected_value,
            degree_value,
        )
        material = abs(selected_value) > MATERIAL_RESIDUE_FLOOR
        route_controls_pass = (
            parse_bool(root["channel_root_controls_pass"])
            if derivation_method
            == "CHANNEL_NUMERATOR_OVER_DERIVATIVE"
            else parse_bool(
                root["direct_laurent_fallback_authorized"]
            )
        )
        common_controls_pass = (
            route_controls_pass
            and float(selected["fit_relative_residual"])
            <= NUMERATOR_FIT_RESIDUAL_LIMIT
            and parse_bool(selected["all_samples_mask_active"])
            and float(selected["maximum_coefficient_relative_change"])
            <= COEFFICIENT_CHANGE_LIMIT
        )
        material_controls_pass = (
            material
            and common_controls_pass
            and refinement_change
            <= RESIDUE_REFINEMENT_CHANGE_LIMIT
            and degree_change <= RESIDUE_DEGREE_CHANGE_LIMIT
        )
        removable_controls_pass = (
            not material
            and common_controls_pass
            and max(
                abs(selected_value),
                abs(coarse_value),
                abs(degree_value),
            )
            <= REMOVABLE_RESIDUE_CEILING
        )
        controls_pass = (
            material_controls_pass or removable_controls_pass
        )
        selected_rows.append(
            {
                "angular_node_id": root["angular_node_id"],
                "epsilon_id": root["epsilon_id"],
                "component_id": root["component_id"],
                "pole_id": root["pole_id"],
                "surface_id": root["surface_id"],
                "residue_derivation_method": derivation_method,
                "pole_real": selected["fitted_pole_real"],
                "pole_imaginary": selected["fitted_pole_imaginary"],
                "pole_shift_from_source": selected[
                    "fitted_pole_shift_from_source"
                ],
                **complex_fields("true_limit_residue", selected_value),
                "fit_relative_residual": selected[
                    "fit_relative_residual"
                ],
                "refinement_relative_change": refinement_change,
                "degree_relative_change": degree_change,
                "maximum_coefficient_relative_change": selected[
                    "maximum_coefficient_relative_change"
                ],
                "material_pole": material,
                "pole_classification": (
                    "EXACT_ACTIVE_MATERIAL_SIMPLE_POLE"
                    if material
                    else "EXACT_ACTIVE_REMOVABLE_BOUNDED_ZERO_RESIDUE"
                ),
                "material_residue_controls_pass": (
                    material_controls_pass
                ),
                "removable_zero_residue_controls_pass": (
                    removable_controls_pass
                ),
                "pole_residue_controls_pass": controls_pass,
                "valid_for_failed_node_pole_subtraction": (
                    controls_pass and material
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "POLE_RESIDUE_DERIVATION",
                "last_completed_key": "|".join(key),
                "selected_pole_residue_count": len(selected_rows),
            },
        )
    return sample_rows, fit_rows, selected_rows


def endpoint_group_rows() -> dict[
    tuple[str, str, str],
    list[dict[str, str]],
]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, str]],
    ] = defaultdict(list)
    seen: set[tuple[str, str, str, float]] = set()
    for row in read_csv(ENERGY_NODES_5287):
        if int(row["energy_order"]) != max(M5287.ENERGY_ORDERS):
            continue
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        energy = float(row["soft_energy"])
        sample_key = (*key, energy)
        if sample_key in seen:
            continue
        seen.add(sample_key)
        grouped[key].append(row)
    return grouped


def endpoint_asymptotic_fits() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    fit_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    for key, source_rows_local in sorted(endpoint_group_rows().items()):
        local_fits: dict[tuple[float, int], dict[str, Any]] = {}
        for upper in ENDPOINT_UPPERS:
            local = sorted(
                [
                    row
                    for row in source_rows_local
                    if float(row["soft_energy"]) <= upper
                ],
                key=lambda row: float(row["soft_energy"]),
            )
            if len(local) < max(ENDPOINT_DEGREES) + 2:
                raise RuntimeError(
                    f"insufficient endpoint samples for {key} at {upper}"
                )
            energies = np.asarray(
                [float(row["soft_energy"]) for row in local],
                dtype=np.float64,
            )
            contributions = np.asarray(
                [
                    complex(
                        float(row["raw_residue_real"]),
                        float(row["raw_residue_imaginary"]),
                    )
                    for row in local
                ],
                dtype=np.complex128,
            )
            scaled = energies / upper
            transformed = energies * contributions
            for degree in ENDPOINT_DEGREES:
                matrix = np.column_stack(
                    [
                        scaled**power
                        for power in range(degree + 1)
                    ]
                )
                coefficients, _, _, _ = np.linalg.lstsq(
                    matrix,
                    transformed,
                    rcond=None,
                )
                predicted = matrix @ coefficients
                coefficient = complex(coefficients[0])
                residual = float(
                    np.max(np.abs(predicted - transformed))
                    / max(
                        float(np.max(np.abs(transformed))),
                        1.0e-300,
                    )
                )
                strength_ratio = abs(coefficient) / max(
                    float(np.max(np.abs(transformed))),
                    1.0e-300,
                )
                fit = {
                    "angular_node_id": key[0],
                    "epsilon_id": key[1],
                    "component_id": key[2],
                    "upper_energy": upper,
                    "degree": degree,
                    "sample_count": len(local),
                    **complex_fields(
                        "endpoint_log_coefficient",
                        coefficient,
                    ),
                    "fit_relative_residual": residual,
                    "endpoint_strength_ratio": strength_ratio,
                    "all_samples_mask_active": all(
                        parse_bool(row["mask_active"]) for row in local
                    ),
                    "valid_for_endpoint_asymptotic_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                fit_rows.append(fit)
                local_fits[(upper, degree)] = fit
        selected = local_fits[(ENDPOINT_UPPERS[0], 2)]
        coarse = local_fits[(ENDPOINT_UPPERS[1], 2)]
        degree = local_fits[(ENDPOINT_UPPERS[0], 3)]
        selected_value = complex(
            selected["endpoint_log_coefficient_real"],
            selected["endpoint_log_coefficient_imaginary"],
        )
        coarse_value = complex(
            coarse["endpoint_log_coefficient_real"],
            coarse["endpoint_log_coefficient_imaginary"],
        )
        degree_value = complex(
            degree["endpoint_log_coefficient_real"],
            degree["endpoint_log_coefficient_imaginary"],
        )
        refinement_change = relative_complex_difference(
            selected_value,
            coarse_value,
        )
        degree_change = relative_complex_difference(
            selected_value,
            degree_value,
        )
        smallest = sorted(
            source_rows_local,
            key=lambda row: float(row["soft_energy"]),
        )[:2]
        first_energy = float(smallest[0]["soft_energy"])
        second_energy = float(smallest[1]["soft_energy"])
        first_magnitude = float(smallest[0]["raw_residue_magnitude"])
        second_magnitude = float(smallest[1]["raw_residue_magnitude"])
        exponent = (
            math.log(second_magnitude / first_magnitude)
            / math.log(second_energy / first_energy)
            if min(first_magnitude, second_magnitude) > 1.0e-300
            else 0.0
        )
        singular = (
            abs(selected_value) > ENDPOINT_ABSOLUTE_FLOOR
            and float(selected["endpoint_strength_ratio"])
            >= ENDPOINT_STRENGTH_RATIO_FLOOR
            and parse_bool(selected["all_samples_mask_active"])
        )
        controls_pass = (
            float(selected["fit_relative_residual"])
            <= ENDPOINT_FIT_RESIDUAL_LIMIT
            and refinement_change <= ENDPOINT_REFINEMENT_CHANGE_LIMIT
            and degree_change <= ENDPOINT_DEGREE_CHANGE_LIMIT
            and (
                not singular
                or abs(exponent + 1.0)
                <= ENDPOINT_EXPONENT_TOLERANCE
            )
        )
        selected_rows.append(
            {
                "angular_node_id": key[0],
                "epsilon_id": key[1],
                "component_id": key[2],
                **complex_fields(
                    "endpoint_log_coefficient",
                    selected_value,
                ),
                "endpoint_power_exponent": exponent,
                "endpoint_strength_ratio": selected[
                    "endpoint_strength_ratio"
                ],
                "fit_relative_residual": selected[
                    "fit_relative_residual"
                ],
                "refinement_relative_change": refinement_change,
                "degree_relative_change": degree_change,
                "lower_endpoint_log_singular": singular,
                "endpoint_classification": (
                    "ACTIVE_A_OVER_E_LOG_ENDPOINT"
                    if singular
                    else "NO_MATERIAL_A_OVER_E_ENDPOINT"
                ),
                "endpoint_fit_controls_pass": controls_pass,
                "valid_for_lower_endpoint_log_subtraction": (
                    singular and controls_pass
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return fit_rows, selected_rows


def physical_endpoint_rows(
    selected: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    parent_total = next(
        row
        for row in read_csv(M5283.TOTALS_5281)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    multiplier = float(parent_total["kernel_multiplier"]) * float(
        parent_total["physical_A00_weight"]
    )
    lookup = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        ): row
        for row in selected
    }
    rows: list[dict[str, Any]] = []
    for angular_node_id, component_ids in sorted(
        EXPECTED_ENDPOINT_PAIRS.items()
    ):
        regulator_totals: dict[str, complex] = {}
        regulator_scales: dict[str, float] = {}
        controls = True
        for epsilon_id in REGULATOR_IDS:
            local = [
                lookup[(angular_node_id, epsilon_id, component_id)]
                for component_id in component_ids
            ]
            values = [
                complex(
                    row["endpoint_log_coefficient_real"],
                    row["endpoint_log_coefficient_imaginary"],
                )
                for row in local
            ]
            regulator_totals[epsilon_id] = sum(values, 0.0j)
            regulator_scales[epsilon_id] = sum(
                abs(value) for value in values
            )
            controls = controls and all(
                parse_bool(
                    row["valid_for_lower_endpoint_log_subtraction"]
                )
                for row in local
            )
        physical = multiplier * (
            2.0 * regulator_totals["E020"]
            - regulator_totals["E040"]
        )
        physical_scale = multiplier * (
            2.0 * regulator_scales["E020"]
            + regulator_scales["E040"]
        )
        e040_ratio = abs(regulator_totals["E040"]) / max(
            regulator_scales["E040"],
            1.0e-300,
        )
        e020_ratio = abs(regulator_totals["E020"]) / max(
            regulator_scales["E020"],
            1.0e-300,
        )
        physical_ratio = abs(physical) / max(
            physical_scale,
            1.0e-300,
        )
        cancellation_passed = (
            max(e040_ratio, e020_ratio, physical_ratio)
            <= ENDPOINT_CANCELLATION_RELATIVE_LIMIT
        )
        rows.append(
            {
                "angular_node_id": angular_node_id,
                "component_pair": "|".join(component_ids),
                "kernel_and_A00_multiplier": multiplier,
                **complex_fields(
                    "E040_pair_endpoint_log_coefficient",
                    regulator_totals["E040"],
                ),
                "E040_pair_cancellation_relative_residual": e040_ratio,
                **complex_fields(
                    "E020_pair_endpoint_log_coefficient",
                    regulator_totals["E020"],
                ),
                "E020_pair_cancellation_relative_residual": e020_ratio,
                **complex_fields(
                    "physical_pair_endpoint_log_coefficient",
                    physical,
                ),
                "physical_pair_cancellation_relative_residual": (
                    physical_ratio
                ),
                "physical_endpoint_classification": (
                    "PAIRWISE_LOG_ENDPOINT_CANCELLATION"
                    if cancellation_passed
                    else "UNCANCELLED_LOG_ENDPOINT"
                ),
                "pairwise_endpoint_cancellation_passed": (
                    cancellation_passed
                ),
                "valid_for_combined_endpoint_subtraction": (
                    controls and cancellation_passed
                ),
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
        SCRIPT_5287,
        RESULT_5287,
        VALIDATION_5287,
        ANGULAR_NODES_5286,
        ENERGY_NODES_5287,
        M5267.MANIFEST_5239,
    )
    parent = read_json(RESULT_5287)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5287_accepted": bool(parent["acceptance_passed"]),
        "parent_5287_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5287)
        ),
        "parent_smoke_failed_numerical_gate": (
            not bool(parent["inner_energy_smoke_passed"])
        ),
        "two_failed_node_pole_targets_declared": len(POLE_TARGETS) == 2,
        "four_angular_nodes_parse": len(read_csv(ANGULAR_NODES_5286)) == 4,
        "stored_energy_nodes_parse": bool(read_csv(ENERGY_NODES_5287)),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
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
            "DRY_RUN_ACCEPTED__DERIVE_FAILED_NODE_POLES_AND_ENDPOINTS"
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
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5288 dry run did not pass")
    parent = read_json(RESULT_5287)
    base_context = M5280.source_context()
    symmetry_audit = MC03_MC08_symmetry_audit(base_context)
    write_csv(SYMMETRY_AUDIT, symmetry_audit)
    owner_scanned, problems = scan_failed_node_poles()
    write_csv(SCANNED_POLES, owner_scanned)
    owner_classified = classify_exact_masks(
        owner_scanned,
        base_context,
    )
    write_csv(CLASSIFIED_POLES, owner_classified)
    owner_roots = refine_active_channel_roots(
        owner_classified,
        problems,
    )
    write_csv(CHANNEL_ROOTS, owner_roots)
    (
        owner_pole_samples,
        owner_pole_fits,
        owner_selected_poles,
    ) = derive_pole_residues(
        owner_roots,
        problems,
        base_context,
    )
    scanned = owner_scanned + mirror_MC03_rows(owner_scanned)
    classified = owner_classified + mirror_MC03_rows(owner_classified)
    roots = owner_roots + mirror_MC03_rows(owner_roots)
    pole_samples = owner_pole_samples + mirror_MC03_rows(
        owner_pole_samples
    )
    pole_fits = owner_pole_fits + mirror_MC03_rows(owner_pole_fits)
    selected_poles = owner_selected_poles + mirror_MC03_rows(
        owner_selected_poles
    )
    endpoint_fits, endpoint_selected = endpoint_asymptotic_fits()
    endpoint_physical = physical_endpoint_rows(endpoint_selected)
    active = [
        row for row in classified if parse_bool(row["exact_mask_active"])
    ]
    promoted = [
        row for row in active if parse_bool(row["promoted_by_exact_mask"])
    ]
    material = [
        row for row in selected_poles if parse_bool(row["material_pole"])
    ]
    endpoint_material = [
        row
        for row in endpoint_selected
        if parse_bool(row["lower_endpoint_log_singular"])
    ]
    endpoint_target_set = {
        (row["angular_node_id"], row["component_id"])
        for row in endpoint_material
    }
    controlled_roots = [
        row
        for row in roots
        if parse_bool(row["channel_root_controls_pass"])
    ]
    fallback_roots = [
        row
        for row in roots
        if parse_bool(row["direct_laurent_fallback_authorized"])
    ]
    maximum_root_residual = max(
        (
            float(row["channel_root_residual"])
            for row in controlled_roots
        ),
        default=0.0,
    )
    maximum_pole_fit_residual = max(
        float(row["fit_relative_residual"]) for row in selected_poles
    )
    maximum_pole_refinement_change = max(
        float(row["refinement_relative_change"])
        for row in selected_poles
    )
    maximum_pole_degree_change = max(
        float(row["degree_relative_change"]) for row in selected_poles
    )
    maximum_endpoint_fit_residual = max(
        float(row["fit_relative_residual"])
        for row in endpoint_material
    )
    maximum_endpoint_refinement_change = max(
        float(row["refinement_relative_change"])
        for row in endpoint_material
    )
    maximum_endpoint_degree_change = max(
        float(row["degree_relative_change"])
        for row in endpoint_material
    )
    maximum_endpoint_exponent_error = max(
        abs(float(row["endpoint_power_exponent"]) + 1.0)
        for row in endpoint_material
    )
    checks = {
        "four_target_problem_inventories_completed": (
            {
                (
                    row["angular_node_id"],
                    row["epsilon_id"],
                    row["component_id"],
                )
                for row in scanned
            }
            == {
                (node_id, epsilon_id, component_id)
                for node_id, component_id in POLE_TARGETS
                for epsilon_id in REGULATOR_IDS
            }
        ),
        "MC03_MC08_symmetry_transport_certified": (
            len(symmetry_audit)
            == len(REGULATOR_IDS) * len(SYMMETRY_TEST_ENERGIES)
            and all(
                parse_bool(row["symmetry_passed"])
                for row in symmetry_audit
            )
        ),
        "all_scanned_poles_exact_mask_classified": (
            len(classified) == len(scanned)
        ),
        "newly_active_poles_found": bool(promoted),
        "all_active_root_or_fallback_routes_available": (
            len(roots) == len(active)
            and all(
                parse_bool(row["root_or_fallback_route_available"])
                for row in roots
            )
        ),
        "all_active_pole_residues_controlled": (
            len(selected_poles) == len(active)
            and all(
                parse_bool(row["pole_residue_controls_pass"])
                for row in selected_poles
            )
        ),
        "material_active_poles_derived": bool(material),
        "expected_lower_endpoint_targets_recovered": (
            endpoint_target_set == EXPECTED_ENDPOINT_TARGETS
        ),
        "all_material_endpoint_fits_controlled": all(
            parse_bool(row["endpoint_fit_controls_pass"])
            for row in endpoint_material
        ),
        "pairwise_endpoint_logs_cancel": all(
            row["physical_endpoint_classification"]
            == "PAIRWISE_LOG_ENDPOINT_CANCELLATION"
            for row in endpoint_physical
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "failed-angular-node-singularity-derivation",
        "checks": checks,
        "acceptance_passed": accepted,
        "scanned_pole_count": len(scanned),
        "exact_active_pole_count": len(active),
        "promoted_pole_count": len(promoted),
        "material_pole_count": len(material),
        "material_pole_component_ids": sorted(
            {row["component_id"] for row in material}
        ),
        "MC03_MC08_symmetry_sample_count": len(symmetry_audit),
        "maximum_MC03_MC08_symmetry_relative_difference": max(
            float(row["relative_difference"]) for row in symmetry_audit
        ),
        "pole_numerator_sample_count": len(pole_samples),
        "selected_pole_residue_count": len(selected_poles),
        "maximum_channel_root_residual": maximum_root_residual,
        "controlled_channel_root_count": len(controlled_roots),
        "direct_laurent_fallback_count": len(fallback_roots),
        "maximum_selected_pole_fit_residual": (
            maximum_pole_fit_residual
        ),
        "maximum_pole_refinement_relative_change": (
            maximum_pole_refinement_change
        ),
        "maximum_pole_degree_relative_change": (
            maximum_pole_degree_change
        ),
        "material_endpoint_count": len(endpoint_material),
        "material_endpoint_targets": sorted(
            "|".join(key) for key in endpoint_target_set
        ),
        "maximum_endpoint_fit_residual": (
            maximum_endpoint_fit_residual
        ),
        "maximum_endpoint_refinement_relative_change": (
            maximum_endpoint_refinement_change
        ),
        "maximum_endpoint_degree_relative_change": (
            maximum_endpoint_degree_change
        ),
        "maximum_endpoint_exponent_error_from_minus_one": (
            maximum_endpoint_exponent_error
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
            "DERIVE_NEW_ANGULAR_POLES_AND_LOG_ENDPOINTS__"
            "BUILD_COMBINED_SUBTRACTION_RUNNER"
            if accepted
            else "FAILED_NODE_SINGULARITY_DERIVATION_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_failed_node_singularity_inventory": accepted,
            "valid_for_combined_subtraction_runner": accepted,
            "valid_for_converged_angular_integration": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The failed order-two angular nodes contain angularly "
                "promoted simple poles and nonzero lower-endpoint A/E "
                "terms. Their coefficients are now explicit, but they "
                "must be subtracted and the energy rules rerun before "
                "any angular or phase-space coefficient claim."
            ),
        },
    }
    write_csv(SYMMETRY_AUDIT, symmetry_audit)
    write_csv(SCANNED_POLES, scanned)
    write_csv(CLASSIFIED_POLES, classified)
    write_csv(CHANNEL_ROOTS, roots)
    write_csv(POLE_SAMPLES, pole_samples)
    write_csv(POLE_FITS, pole_fits)
    write_csv(POLE_RESIDUES, selected_poles)
    write_csv(ENDPOINT_FITS, endpoint_fits)
    write_csv(ENDPOINT_SELECTED, endpoint_selected)
    write_csv(ENDPOINT_PHYSICAL, endpoint_physical)
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


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    text = f"""# 5288 — Failed angular-node singularity derivation

## Purpose

Checkpoint 5287 completed the first four-node angular smoke calculation,
but its inner-energy convergence failed at three nodes. This checkpoint
does not add quadrature points blindly. It derives the singular objects
that the failed rules were integrating untreated.

## Derived structures

- geometric pole candidates scanned: `{result['scanned_pole_count']}`;
- exact-mask active candidates: `{result['exact_active_pole_count']}`;
- candidates promoted by the angular mask: `{result['promoted_pole_count']}`;
- material simple poles: `{result['material_pole_count']}`;
- material pole components: `{result['material_pole_component_ids']}`;
- material lower endpoints: `{result['material_endpoint_count']}`;
- endpoint targets: `{result['material_endpoint_targets']}`.

The lower endpoint law is

`F_X(E) = A_X / E + O(1)`.

The fitted exponent differs from `-1` by at most
`{result['maximum_endpoint_exponent_error_from_minus_one']:.12g}`.
Each individual component has a nonzero coefficient, but the coefficients
occur in opposing `MC04|MC14` or `MC12|MC15` pairs. Their pair sums vanish
within the fitted error budget. The next runner must subtract and add the
paired terms together so quadrature does not destroy this analytic
infrared cancellation.

For the upper-energy failures, the angular mask promotes geometric poles
that were inactive in the fixed-angle calculation. Their roots are
refined channel zeros and their residues are obtained as

`Res(F_X,E_X) = N_X(E_X) / D'_X(E_X)`.

## Numerical controls

- maximum channel-root residual:
  `{result['maximum_channel_root_residual']:.12g}`;
- maximum selected numerator-fit residual:
  `{result['maximum_selected_pole_fit_residual']:.12g}`;
- maximum pole radius refinement change:
  `{result['maximum_pole_refinement_relative_change']:.12g}`;
- maximum pole degree change:
  `{result['maximum_pole_degree_relative_change']:.12g}`;
- maximum endpoint fit residual:
  `{result['maximum_endpoint_fit_residual']:.12g}`;
- validation passed: `{validation_passed}`.

## Decision

`{result['decision']}`

This is a singularity inventory and subtraction contract. It is not an
angular-convergence, full phase-space, UV, local-GR, or full-MTS claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required_csvs = (
        SYMMETRY_AUDIT,
        SCANNED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        POLE_RESIDUES,
        ENDPOINT_FITS,
        ENDPOINT_SELECTED,
        ENDPOINT_PHYSICAL,
    )
    if not RESULT.exists():
        raise RuntimeError(f"missing result: {RESULT}")
    result = read_json(RESULT)
    csv_rows = {path: read_csv(path) for path in required_csvs}
    serialized = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (*required_csvs, RESULT)
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    source_files = result["source_files"]
    current_formal_digest = M5283.formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
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
            "PARENT_5287_ACCEPTED",
            bool(read_json(RESULT_5287)["acceptance_passed"]),
            str(read_json(RESULT_5287)["decision"]),
        ),
        validation_gate(
            "SINGULARITY_DERIVATION_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs)
            and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "MATERIAL_POLES_AND_ENDPOINTS_FOUND",
            (
                result["material_pole_count"] > 0
                and result["material_endpoint_count"]
                == len(EXPECTED_ENDPOINT_TARGETS) * len(REGULATOR_IDS)
            ),
            (
                f"poles={result['material_pole_count']}; "
                f"endpoints={result['material_endpoint_count']}"
            ),
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
                and result["resource_contract"]["worker_math_threads"] == 1
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
            "VALIDATED_FAILED_ANGULAR_NODE_SINGULARITY_DERIVATION"
            if passed
            else "FAILED_ANGULAR_NODE_SINGULARITY_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
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
