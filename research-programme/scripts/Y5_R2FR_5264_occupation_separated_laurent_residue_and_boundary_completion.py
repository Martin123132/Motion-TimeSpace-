from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5260 = FUNCTIONAL_RG / "5260"
SOURCE_5261 = FUNCTIONAL_RG / "5261"
SOURCE_5262 = FUNCTIONAL_RG / "5262"
SOURCE_5263 = FUNCTIONAL_RG / "5263"
SOURCE = FUNCTIONAL_RG / "5264"
NODES = SOURCE / "nodes"

SCRIPT_5263 = (
    SCRIPTS
    / "Y5_R2FR_5263_R96_resolution_repair_and_boundary_completion.py"
)
STATE_5263 = SOURCE_5263 / "boundary_state.json"
REPAIR_RESULT_5263 = (
    SOURCE_5263
    / "G08_I01_T00_R96_repair"
    / "resolution_repair_result.json"
)
FORMAL_INVENTORY = (
    SOURCE_5261 / "formalization_workbench_start_inventory.csv"
)
FAILED_NODE_ID = "G09_I01_T01"
FAILED_NODE_ROOT = SOURCE_5263 / "nodes" / FAILED_NODE_ID
FAILED_NODE_RESULT = FAILED_NODE_ROOT / "node_result.json"
FAILED_NODE_VALIDATION = FAILED_NODE_ROOT / "node_validation.csv"
FAILED_NODE_FITS = FAILED_NODE_ROOT / "corrected_residue_fits.csv"

RUN_CONFIG = SOURCE / "occupation_separated_run_config.json"
DRY_RUN = SOURCE / "occupation_separated_dry_run.json"
STATUS = SOURCE / "status.json"
STATE = SOURCE / "boundary_state.json"
FIT_CANDIDATES = SOURCE / "occupation_separated_fit_candidates.csv"
ALL_NODES = SOURCE / "targeted_boundary_nodes.csv"
FINAL_BRACKETS = SOURCE / "final_topology_transition_brackets.csv"
VALIDATION = SOURCE / "occupation_separated_completion_validation.csv"
RESULT = SOURCE / "occupation_separated_completion_result.json"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"
DOC = (
    POST
    / "5264-Y5-R2FR-occupation-separated-Laurent-residue-and-boundary-completion.md"
)

CHECKPOINT = 5264
PARENT_CHECKPOINT = 5263
MARKER = (
    "MTS_5264_OCCUPATION_SEPARATED_LAURENT_RESIDUE_"
    "AND_BOUNDARY_COMPLETION"
)
REVISION = "occupation-separated-Laurent-residue-v1"
REPAIR_ORDERS = (96, 128, 512)
INNER_ORDERS = (128, 512)
MAXIMUM_GENERATION = 12
MINIMUM_FIT_RADIUS = 2.0e-5
MAXIMUM_REFINEMENTS = 10
MINIMUM_COMPLEX_COVERAGE_RATIO = 1.25
MINIMUM_NESTED_CERTIFYING_FITS = 2
NESTED_RESIDUE_RELATIVE_SPREAD_LIMIT = 5.0e-4
ROOT_NORMALIZED_RESIDUAL_LIMIT = 1.0e-8
DERIVATIVE_RELATIVE_RESIDUAL_LIMIT = 5.0e-5
ROOT_REFINEMENT_SHIFT_RATIO_LIMIT = 1.0e-3
ROOT_REFINEMENT_STEP_LIMIT = 1.0e-14
ROOT_REFINEMENT_MAXIMUM_STEPS = 8
DYNAMIC_PATCH_MARGIN_FACTOR = 0.8
PHYSICAL_REPAIR_RELATIVE_SHIFT_LIMIT = 5.0e-5


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5263 = load_module("mts_5263_for_5264", SCRIPT_5263)
M5261 = M5263.M5261
M5251 = M5263.M5251
M5239 = M5251.M5239
M5237 = M5239.M5237


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
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
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def persist_fit_candidates(rows: list[dict[str, Any]]) -> None:
    existing = read_csv(FIT_CANDIDATES) if FIT_CANDIDATES.exists() else []
    merged: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in [*existing, *rows]:
        key = (
            str(row["job_id"]),
            str(row["pole_id"]),
            str(row["fit_refinement_count"]),
            str(row["fit_method"]),
        )
        merged[key] = row
    write_csv(
        FIT_CANDIDATES,
        sorted(
            merged.values(),
            key=lambda row: (
                str(row["job_id"]),
                str(row["pole_id"]),
                int(row["fit_refinement_count"]),
            ),
        ),
    )


def interval_safe_margin(
    center: float,
    interval: dict[str, Any],
) -> float:
    lower = float(interval["interval_lower"])
    upper = float(interval["interval_upper"])
    left_uncertainty = float(
        interval.get("left_transition_uncertainty", 0.0)
    )
    right_uncertainty = float(
        interval.get("right_transition_uncertainty", 0.0)
    )
    return min(
        center - lower - left_uncertainty,
        upper - center - right_uncertainty,
    )


def occupied_bare_contribution(
    problem: dict[str, Any],
    coordinate: float,
    occupation_multiplier: float,
) -> complex:
    return occupation_multiplier * M5237.component_contribution(
        problem, coordinate
    )


def owner_channel_derivative(
    problem: dict[str, Any],
    coordinate: complex,
    surface_id: str,
    step: float,
) -> complex:
    value = lambda point: M5239.owner_surface_values(
        problem, point
    )[surface_id]
    return (
        value(coordinate - 2.0 * step)
        - 8.0 * value(coordinate - step)
        + 8.0 * value(coordinate + step)
        - value(coordinate + 2.0 * step)
    ) / (12.0 * step)


def refine_owner_channel_root(
    problem: dict[str, Any],
    initial_pole: complex,
    surface_id: str,
    fit_radius: float,
) -> dict[str, Any]:
    derivative_step = max(
        1.0e-8,
        min(fit_radius * 1.0e-3, 1.0e-5),
    )
    pole = initial_pole
    iteration_count = 0
    final_step = math.inf
    for iteration in range(ROOT_REFINEMENT_MAXIMUM_STEPS):
        channel = M5239.owner_surface_values(
            problem, pole
        )[surface_id]
        derivative = owner_channel_derivative(
            problem,
            pole,
            surface_id,
            derivative_step,
        )
        if abs(derivative) <= 1.0e-30:
            break
        correction = channel / derivative
        pole -= correction
        iteration_count = iteration + 1
        final_step = abs(correction)
        if final_step <= ROOT_REFINEMENT_STEP_LIMIT:
            break
    derivative_coarse = owner_channel_derivative(
        problem,
        pole,
        surface_id,
        derivative_step,
    )
    derivative_fine = owner_channel_derivative(
        problem,
        pole,
        surface_id,
        0.5 * derivative_step,
    )
    derivative_relative_residual = abs(
        derivative_fine - derivative_coarse
    ) / max(abs(derivative_fine), 1.0e-30)
    return {
        "initial_pole": initial_pole,
        "refined_pole": pole,
        "derivative": derivative_fine,
        "derivative_step": derivative_step,
        "derivative_relative_residual": (
            derivative_relative_residual
        ),
        "iteration_count": iteration_count,
        "final_step": final_step,
        "shift": abs(pole - initial_pole),
    }


def fit_candidate(
    problem: dict[str, Any],
    center: float,
    complex_pole: complex,
    surface_id: str,
    derivative: complex,
    occupation_multiplier: float,
    radius: float,
    refinement: int,
) -> dict[str, Any]:
    offsets = radius * np.asarray(
        (-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0)
    )
    contributions: list[complex] = []
    numerators: list[complex] = []
    for offset in offsets:
        coordinate = center + float(offset)
        contribution = occupied_bare_contribution(
            problem,
            coordinate,
            occupation_multiplier,
        )
        channel = M5239.owner_surface_values(
            problem, complex(coordinate)
        )[surface_id]
        contributions.append(contribution)
        numerators.append(channel * contribution)
    coefficients = np.polyfit(
        offsets,
        np.asarray(numerators, dtype=np.complex128),
        3,
    )
    fitted = np.polyval(coefficients, offsets)
    numerator_array = np.asarray(numerators, dtype=np.complex128)
    numerator_scale = max(
        float(np.max(np.abs(numerator_array))),
        1.0e-30,
    )
    fit_residual = float(
        np.max(np.abs(fitted - numerator_array)) / numerator_scale
    )
    numerator_at_pole = complex(
        np.polyval(coefficients, complex_pole - center)
    )
    slopes: dict[str, float] = {}
    for side, sign in (("negative", -1.0), ("positive", 1.0)):
        selected = [
            index
            for index, offset in enumerate(offsets)
            if float(offset) * sign > 0.0
        ]
        slope, _ = np.polyfit(
            np.log(
                [
                    abs(center + float(offsets[index]) - complex_pole)
                    for index in selected
                ]
            ),
            np.log(
                [
                    max(abs(contributions[index]), 1.0e-300)
                    for index in selected
                ]
            ),
            1,
        )
        slopes[side] = float(slope)
    standard_fit_passed = (
        fit_residual <= M5237.NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
        and all(
            abs(slopes[side] + 1.0) <= M5237.SLOPE_TOLERANCE
            for side in ("negative", "positive")
        )
    )
    residue = numerator_at_pole / derivative
    coverage_ratio = radius / max(
        abs(complex_pole - center),
        1.0e-30,
    )
    return {
        "fit_radius": radius,
        "fit_refinement_count": refinement,
        "numerator_scale": numerator_scale,
        "fit_residual": fit_residual,
        "numerator_at_pole": numerator_at_pole,
        "residue": residue,
        "slopes": slopes,
        "standard_fit_passed": standard_fit_passed,
        "complex_pole_coverage_ratio": coverage_ratio,
        "complex_interpolation_covered": (
            coverage_ratio >= MINIMUM_COMPLEX_COVERAGE_RATIO
        ),
    }


def fit_occupation_separated_residues(
    problem: dict[str, Any],
    poles: list[dict[str, Any]],
    global_centers: list[float],
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    active = [row for row in poles if row["causal_family_active"]]
    rows: list[dict[str, Any]] = []
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
    for pole in active:
        center = float(pole["real_axis_center"])
        nearest = min(
            (
                abs(center - other)
                for other in global_centers
                if abs(center - other) > 1.0e-10
            ),
            default=math.inf,
        )
        cycle_half_width = M5237.local_cycle_half_width(
            problem, center
        )
        maximum_fit_radius = min(
            5.0e-3,
            0.2 * nearest,
            0.2 * cycle_half_width,
            0.2 * (center - lower),
            0.2 * (upper - center),
        )
        if maximum_fit_radius < MINIMUM_FIT_RADIUS:
            raise RuntimeError(
                f"insufficient analytic fit radius at {center}"
            )
        active_interval = M5239.interval_for_coordinate(
            problem,
            center,
            intervals_by_job,
        )
        occupation_multiplier = float(
            active_interval["dynamic_multiplier"]
        )
        safe_margin = interval_safe_margin(center, active_interval)
        surface_id = pole["primary_surface_id"]
        initial_complex_pole = complex(
            float(pole["pole_real"]),
            float(pole["pole_imaginary"]),
        )
        root_refinement = refine_owner_channel_root(
            problem,
            initial_complex_pole,
            surface_id,
            maximum_fit_radius,
        )
        complex_pole = complex(root_refinement["refined_pole"])
        derivative = complex(root_refinement["derivative"])
        root_refinement_shift_ratio = float(
            root_refinement["shift"]
        ) / maximum_fit_radius
        candidates: list[dict[str, Any]] = []
        for refinement in range(MAXIMUM_REFINEMENTS):
            radius = maximum_fit_radius * 0.5**refinement
            if radius < MINIMUM_FIT_RADIUS:
                break
            candidates.append(
                fit_candidate(
                    problem,
                    center,
                    complex_pole,
                    surface_id,
                    derivative,
                    occupation_multiplier,
                    radius,
                    refinement,
                )
            )
        certifying = [
            candidate
            for candidate in candidates
            if candidate["standard_fit_passed"]
            and candidate["complex_interpolation_covered"]
        ]
        selected = (
            certifying[0]
            if certifying
            else min(
                candidates,
                key=lambda candidate: max(
                    candidate["fit_residual"]
                    / M5237.NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT,
                    abs(candidate["slopes"]["negative"] + 1.0)
                    / M5237.SLOPE_TOLERANCE,
                    abs(candidate["slopes"]["positive"] + 1.0)
                    / M5237.SLOPE_TOLERANCE,
                ),
            )
        )
        selected_residue = complex(selected["residue"])
        nested_spread = (
            max(
                abs(complex(candidate["residue"]) - selected_residue)
                for candidate in certifying
            )
            / max(abs(selected_residue), 1.0e-30)
            if certifying
            else math.inf
        )
        root_value = M5239.owner_surface_values(
            problem, complex_pole
        )[surface_id]
        root_normalized_residual = abs(root_value) / max(
            abs(derivative) * float(selected["fit_radius"]),
            1.0e-30,
        )
        derivative_relative_residual = float(
            root_refinement["derivative_relative_residual"]
        )
        numerator_at_pole = complex(selected["numerator_at_pole"])
        numerator_error_scale = (
            float(selected["fit_residual"])
            * float(selected["numerator_scale"])
        )
        numerator_nonzero_margin = (
            abs(numerator_at_pole) - numerator_error_scale
        )
        patch_candidates = [
            candidate
            for candidate in candidates
            if float(candidate["fit_radius"])
            <= DYNAMIC_PATCH_MARGIN_FACTOR * safe_margin
        ]
        patch_radius = (
            float(patch_candidates[0]["fit_radius"])
            if patch_candidates
            else 0.0
        )
        direct_certificate_passed = (
            occupation_multiplier != 0.0
            and finite_complex(selected_residue)
            and len(certifying) >= MINIMUM_NESTED_CERTIFYING_FITS
            and nested_spread
            <= NESTED_RESIDUE_RELATIVE_SPREAD_LIMIT
            and root_normalized_residual
            <= ROOT_NORMALIZED_RESIDUAL_LIMIT
            and derivative_relative_residual
            <= DERIVATIVE_RELATIVE_RESIDUAL_LIMIT
            and root_refinement_shift_ratio
            <= ROOT_REFINEMENT_SHIFT_RATIO_LIMIT
            and float(root_refinement["final_step"])
            <= ROOT_REFINEMENT_STEP_LIMIT
            and numerator_nonzero_margin > 0.0
            and patch_radius >= MINIMUM_FIT_RADIUS
            and patch_radius
            <= DYNAMIC_PATCH_MARGIN_FACTOR * safe_margin
        )
        candidate_rows = []
        for candidate in candidates:
            candidate_rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "job_id": problem["job"]["job_id"],
                    "epsilon_id": problem["job"]["epsilon_id"],
                    "component_id": problem["component_id"],
                    "pole_id": pole["pole_id"],
                    "surface_id": surface_id,
                    "fit_method": (
                        "constant_occupation_bare_Laurent"
                    ),
                    "fit_refinement_count": candidate[
                        "fit_refinement_count"
                    ],
                    "fit_radius": candidate["fit_radius"],
                    "complex_pole_coverage_ratio": candidate[
                        "complex_pole_coverage_ratio"
                    ],
                    "complex_interpolation_covered": candidate[
                        "complex_interpolation_covered"
                    ],
                    "numerator_fit_relative_residual": candidate[
                        "fit_residual"
                    ],
                    "negative_log_log_slope": candidate["slopes"][
                        "negative"
                    ],
                    "positive_log_log_slope": candidate["slopes"][
                        "positive"
                    ],
                    "standard_fit_passed": candidate[
                        "standard_fit_passed"
                    ],
                    "residue_real": complex(
                        candidate["residue"]
                    ).real,
                    "residue_imaginary": complex(
                        candidate["residue"]
                    ).imag,
                    "selected_for_residue": (
                        candidate is selected
                    ),
                    "initial_pole_real": initial_complex_pole.real,
                    "initial_pole_imaginary": (
                        initial_complex_pole.imag
                    ),
                    "refined_pole_real": complex_pole.real,
                    "refined_pole_imaginary": complex_pole.imag,
                    "root_refinement_shift_ratio": (
                        root_refinement_shift_ratio
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        persist_fit_candidates(candidate_rows)
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "epsilon_id": problem["job"]["epsilon_id"],
                "pole_id": pole["pole_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "owner_summand": problem["job"]["owner_summand"],
                "surface_id": surface_id,
                "center": center,
                "pole_real": complex_pole.real,
                "pole_imaginary": complex_pole.imag,
                "initial_pole_real": initial_complex_pole.real,
                "initial_pole_imaginary": initial_complex_pole.imag,
                "root_refinement_iteration_count": root_refinement[
                    "iteration_count"
                ],
                "root_refinement_final_step": root_refinement[
                    "final_step"
                ],
                "root_refinement_shift": root_refinement["shift"],
                "root_refinement_shift_ratio": (
                    root_refinement_shift_ratio
                ),
                "fit_radius": selected["fit_radius"],
                "nearest_event_pole_distance": nearest,
                "local_cycle_half_width": cycle_half_width,
                "patch_half_width": min(
                    M5237.PATCH_HALF_WIDTH,
                    0.8 * cycle_half_width,
                    patch_radius,
                ),
                "fit_refinement_count": selected[
                    "fit_refinement_count"
                ],
                "patch_refinement_count": patch_candidates[0][
                    "fit_refinement_count"
                ]
                if patch_candidates
                else -1,
                "channel_derivative_real": derivative.real,
                "channel_derivative_imaginary": derivative.imag,
                "numerator_at_pole_real": numerator_at_pole.real,
                "numerator_at_pole_imaginary": numerator_at_pole.imag,
                "outer_residue_real": selected_residue.real,
                "outer_residue_imaginary": selected_residue.imag,
                "numerator_fit_relative_residual": selected[
                    "fit_residual"
                ],
                "negative_log_log_slope": selected["slopes"][
                    "negative"
                ],
                "positive_log_log_slope": selected["slopes"][
                    "positive"
                ],
                "fit_method": "constant_occupation_bare_Laurent",
                "dynamic_occupation_multiplier": (
                    occupation_multiplier
                ),
                "dynamic_boundary_safe_margin": safe_margin,
                "complex_pole_coverage_ratio": selected[
                    "complex_pole_coverage_ratio"
                ],
                "certifying_nested_fit_count": len(certifying),
                "nested_residue_relative_spread": nested_spread,
                "root_normalized_residual": (
                    root_normalized_residual
                ),
                "derivative_relative_residual": (
                    derivative_relative_residual
                ),
                "numerator_nonzero_margin": numerator_nonzero_margin,
                "direct_simple_pole_certificate_passed": (
                    direct_certificate_passed
                ),
                "fit_passed": direct_certificate_passed,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def required_sources() -> tuple[Path, ...]:
    return (
        SCRIPT_5263,
        STATE_5263,
        REPAIR_RESULT_5263,
        FORMAL_INVENTORY,
        FAILED_NODE_RESULT,
        FAILED_NODE_VALIDATION,
        FAILED_NODE_FITS,
    )


def parent_failure_is_isolated() -> bool:
    failed = [
        row
        for row in read_csv(FAILED_NODE_VALIDATION)
        if not parse_bool(row["passed"])
    ]
    return (
        len(failed) == 1
        and failed[0]["gate"]
        == f"{FAILED_NODE_ID}_ACTIVE_POLES_HAVE_ONE_ACCEPTED_FIT"
    )


def configure_controller() -> None:
    M5263.configure_5263_controller()
    M5261.SOURCE = SOURCE
    M5261.NODES = NODES
    M5261.STATE = STATE
    M5261.STATUS = STATUS
    M5261.MARKER = MARKER
    M5261.REVISION = REVISION
    M5261.CHECKPOINT = CHECKPOINT
    M5261.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5261.MAXIMUM_GENERATION = MAXIMUM_GENERATION
    M5239.QUADRATURE_ORDERS = REPAIR_ORDERS
    M5239.fit_full_component_residues = (
        fit_occupation_separated_residues
    )


def install_manifest_contract() -> Any:
    original = M5261.generation_manifest

    def contracted_manifest(
        state: dict[str, Any],
        targets: list[dict[str, Any]],
        generation: int,
        formal_digest: str,
        run_signature: str,
    ) -> dict[str, Any]:
        manifest = original(
            state,
            targets,
            generation,
            formal_digest,
            run_signature,
        )
        manifest.pop("manifest_hash", None)
        manifest.update(
            {
                "quadrature_orders": list(REPAIR_ORDERS),
                "low_order_gate_contract": "R96_vs_R512 <= 5e-3",
                "mid_order_gate_contract": "R128_vs_R512 <= 1e-3",
                "residue_fit_contract": (
                    "constant contour occupation times the bare "
                    "analytic component; direct simple-pole theorem"
                ),
                "minimum_complex_coverage_ratio": (
                    MINIMUM_COMPLEX_COVERAGE_RATIO
                ),
                "minimum_nested_certifying_fits": (
                    MINIMUM_NESTED_CERTIFYING_FITS
                ),
                "nested_residue_relative_spread_limit": (
                    NESTED_RESIDUE_RELATIVE_SPREAD_LIMIT
                ),
                "root_refinement_shift_ratio_limit": (
                    ROOT_REFINEMENT_SHIFT_RATIO_LIMIT
                ),
                "dynamic_patch_margin_factor": (
                    DYNAMIC_PATCH_MARGIN_FACTOR
                ),
                "resolution_escalation_source": str(
                    REPAIR_RESULT_5263
                ),
            }
        )
        manifest["manifest_hash"] = serialized_hash(manifest)
        return manifest

    M5261.generation_manifest = contracted_manifest
    return original


def run_configuration(parent_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "marker": f"{MARKER}_RUN_CONFIGURATION",
        "revision": REVISION,
        "parent_completed_generation": parent_state[
            "completed_generation"
        ],
        "parent_state_hash": serialized_hash(parent_state),
        "parent_failure_isolated": parent_failure_is_isolated(),
        "quadrature_orders": list(REPAIR_ORDERS),
        "residue_fit_method": "constant_occupation_bare_Laurent",
        "minimum_complex_coverage_ratio": (
            MINIMUM_COMPLEX_COVERAGE_RATIO
        ),
        "minimum_nested_certifying_fits": (
            MINIMUM_NESTED_CERTIFYING_FITS
        ),
        "nested_residue_relative_spread_limit": (
            NESTED_RESIDUE_RELATIVE_SPREAD_LIMIT
        ),
        "root_normalized_residual_limit": (
            ROOT_NORMALIZED_RESIDUAL_LIMIT
        ),
        "derivative_relative_residual_limit": (
            DERIVATIVE_RELATIVE_RESIDUAL_LIMIT
        ),
        "root_refinement_shift_ratio_limit": (
            ROOT_REFINEMENT_SHIFT_RATIO_LIMIT
        ),
        "dynamic_patch_margin_factor": (
            DYNAMIC_PATCH_MARGIN_FACTOR
        ),
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in required_sources()
        ],
    }


def ensure_configuration(value: dict[str, Any]) -> str:
    signature = serialized_hash(value)
    payload = {**value, "run_signature": signature}
    if RUN_CONFIG.exists():
        existing = json.loads(RUN_CONFIG.read_text(encoding="utf-8"))
        if existing != payload:
            raise RuntimeError("checkpoint-5264 run configuration changed")
    else:
        atomic_json(RUN_CONFIG, payload)
    return signature


def dry_run() -> dict[str, Any]:
    sources = required_sources()
    parent_state = (
        json.loads(STATE_5263.read_text(encoding="utf-8"))
        if STATE_5263.exists()
        else {}
    )
    failed_result = (
        json.loads(FAILED_NODE_RESULT.read_text(encoding="utf-8"))
        if FAILED_NODE_RESULT.exists()
        else {}
    )
    checks = {
        "all_required_sources_exist": all(
            path.exists() for path in sources
        ),
        "parent_completed_generation_is_eight": (
            int(parent_state.get("completed_generation", -1)) == 8
        ),
        "parent_failure_is_isolated_residue_fit_gate": (
            parent_failure_is_isolated()
            if FAILED_NODE_VALIDATION.exists()
            else False
        ),
        "failed_node_integrity_passed": bool(
            failed_result.get("integrity_passed", False)
        ),
        "failed_node_acceptance_remains_false": not bool(
            failed_result.get("acceptance_passed", True)
        ),
        "claim_flags_locked_false": all(
            not bool(failed_result.get(field, True))
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
        "formalization_workbench_exists": FORMAL.exists(),
    }
    result = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "writes_performed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return result


def collect_new_fit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(NODES.glob("G*/corrected_residue_fits.csv")):
        rows.extend(read_csv(path))
    return rows


def collect_parent_and_new_nodes(
    completed_generation: int,
) -> list[dict[str, Any]]:
    prior_5261 = M5263.collect_node_rows(SOURCE_5261, 3, 5)
    prior_5262 = M5263.collect_node_rows(SOURCE_5262, 6, 7)
    prior_5263 = M5263.collect_node_rows(SOURCE_5263, 8, 8)
    new_rows = M5263.collect_node_rows(
        SOURCE,
        9,
        completed_generation,
    )
    return [*prior_5261, *prior_5262, *prior_5263, *new_rows]


def physical_repair_shift() -> float:
    parent = json.loads(FAILED_NODE_RESULT.read_text(encoding="utf-8"))
    repaired_path = NODES / FAILED_NODE_ID / "node_result.json"
    repaired = json.loads(repaired_path.read_text(encoding="utf-8"))
    shifts = []
    for order in INNER_ORDERS:
        parent_value = M5261.result_value(parent, order)
        repaired_value = M5261.result_value(repaired, order)
        shifts.append(
            abs(repaired_value - parent_value)
            / max(abs(parent_value), 1.0e-30)
        )
    return max(shifts)


def write_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5264 — Occupation-separated Laurent residue and boundary completion",
        "",
        "## Purpose",
        "",
        (
            "Checkpoint 5263 reached generation 9 with intact topology, "
            "closure, and R96/R128/R512 convergence, but one E040 "
            "residue row failed the finite-window log-slope gate."
        ),
        (
            "The failure occurred because the dynamic winding boundary "
            "forced the real-axis fit radius below the pole's imaginary "
            "displacement. This checkpoint separates two logically "
            "distinct objects: the analytic Laurent residue of the bare "
            "component and the integer contour-occupation multiplier."
        ),
        "",
        "## Derived local rule",
        "",
        (
            "For an active owner channel `D_X(z)` and component "
            "`F_X(z)`, define `N_X(z)=D_X(z)F_X(z)`. If "
            "`D_X(z_X)=0`, `D'_X(z_X) != 0`, `N_X` is analytic and "
            "`N_X(z_X) != 0`, then the pole is simple and "
            "`Res(F_X,z_X)=N_X(z_X)/D'_X(z_X)`."
        ),
        (
            "The dynamic winding multiplier is held constant while "
            "fitting this analytic local object. It is then used only "
            "as the independently certified contour occupation. The "
            "real integration patch remains capped inside the dynamic "
            "interval, so the continuation does not smear a winding "
            "step across the real contour."
        ),
        "",
        "## Numerical gates",
        "",
        (
            f"- Minimum complex-pole coverage ratio: "
            f"`{MINIMUM_COMPLEX_COVERAGE_RATIO}`."
        ),
        (
            f"- Minimum nested certifying fits: "
            f"`{MINIMUM_NESTED_CERTIFYING_FITS}`."
        ),
        (
            f"- Nested residue relative-spread limit: "
            f"`{NESTED_RESIDUE_RELATIVE_SPREAD_LIMIT}`."
        ),
        (
            f"- Root normalized-residual limit: "
            f"`{ROOT_NORMALIZED_RESIDUAL_LIMIT}`."
        ),
        (
            f"- Derivative relative-residual limit: "
            f"`{DERIVATIVE_RELATIVE_RESIDUAL_LIMIT}`."
        ),
        (
            f"- Root-refinement shift-ratio limit: "
            f"`{ROOT_REFINEMENT_SHIFT_RATIO_LIMIT}`."
        ),
        (
            f"- Dynamic patch margin factor: "
            f"`{DYNAMIC_PATCH_MARGIN_FACTOR}`."
        ),
        "",
        "## Result",
        "",
        f"- Validation passed: `{result['validation_passed']}`.",
        (
            f"- Completed generation: "
            f"`{result['completed_generation']}`."
        ),
        f"- Total certified nodes: `{result['node_count']}`.",
        (
            f"- Maximum parent-to-repaired physical shift: "
            f"`{result['maximum_physical_repair_relative_shift']}`."
        ),
        (
            f"- All boundary stopping gates passed: "
            f"`{result['all_boundary_stopping_gates_passed']}`."
        ),
        (
            "- Formalization-workbench modified files: "
            f"`{result['formalization_workbench_modified_file_count']}`."
        ),
        f"- Decision: `{result['decision']}`.",
        "",
        "## Claim boundary",
        "",
        (
            "This checkpoint certifies the targeted topology-boundary "
            "location budget and the local residue treatment used in "
            "that calculation. It does not by itself establish the "
            "numeric UV coefficient, local GR, or the full MTS theory."
        ),
        "",
    ]
    atomic_text(DOC, "\n".join(lines))


def execute() -> dict[str, Any]:
    dry_result = dry_run()
    if not dry_result["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_result["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5264 dry run failed: {failed}")
    SOURCE.mkdir(parents=True, exist_ok=True)
    atomic_json(DRY_RUN, {**dry_result, "writes_performed": True})
    parent_state = json.loads(STATE_5263.read_text(encoding="utf-8"))
    configuration = run_configuration(parent_state)
    run_signature = ensure_configuration(configuration)
    formal_start_rows = read_csv(FORMAL_INVENTORY)
    formal_digest = M5251.inventory_digest(formal_start_rows)
    configure_controller()
    original_manifest_function = install_manifest_contract()
    try:
        if STATE.exists():
            state = json.loads(STATE.read_text(encoding="utf-8"))
        else:
            state = copy.deepcopy(parent_state)
            state["marker"] = f"{MARKER}_STATE"
            state["revision"] = REVISION
            atomic_json(STATE, state)
        while not all(
            bool(bracket["stopping_gate_passed"])
            for bracket in state["brackets"].values()
        ):
            generation = int(state["completed_generation"]) + 1
            if generation > MAXIMUM_GENERATION:
                raise RuntimeError(
                    "maximum generation reached before stopping"
                )
            state, _ = M5261.execute_generation(
                state,
                generation,
                formal_digest,
                run_signature,
            )
    finally:
        M5261.generation_manifest = original_manifest_function
    all_node_rows = collect_parent_and_new_nodes(
        int(state["completed_generation"])
    )
    final_rows = M5261.final_bracket_rows(state)
    new_fit_rows = collect_new_fit_rows()
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        formal_start_rows,
        formal_after_rows,
    )
    write_csv(FORMAL_DIFF, formal_diff_rows)
    maximum_shift = physical_repair_shift()
    checks = [
        {
            "check_id": "PARENT_FAILURE_IS_ISOLATED_RESIDUE_GATE",
            "passed": parent_failure_is_isolated(),
            "detail": FAILED_NODE_ID,
        },
        {
            "check_id": "ALL_NEW_RESIDUES_USE_OCCUPATION_SEPARATION",
            "passed": bool(new_fit_rows)
            and all(
                row.get("fit_method")
                == "constant_occupation_bare_Laurent"
                for row in new_fit_rows
            ),
            "detail": f"rows={len(new_fit_rows)}",
        },
        {
            "check_id": "ALL_DIRECT_SIMPLE_POLE_CERTIFICATES_PASS",
            "passed": bool(new_fit_rows)
            and all(
                parse_bool(
                    row["direct_simple_pole_certificate_passed"]
                )
                and parse_bool(row["fit_passed"])
                for row in new_fit_rows
            ),
            "detail": (
                f"passed={sum(parse_bool(row['fit_passed']) for row in new_fit_rows)}"
                f"/{len(new_fit_rows)}"
            ),
        },
        {
            "check_id": "REPAIRED_PHYSICS_SHIFT_IS_BOUNDED",
            "passed": maximum_shift
            <= PHYSICAL_REPAIR_RELATIVE_SHIFT_LIMIT,
            "detail": (
                f"shift={maximum_shift}; "
                f"limit={PHYSICAL_REPAIR_RELATIVE_SHIFT_LIMIT}"
            ),
        },
        {
            "check_id": "NODE_ACCOUNTING_MATCHES_SCHEDULE",
            "passed": len(all_node_rows) == 27
            and len(
                {
                    row["order9_node_id"]
                    for row in all_node_rows
                }
            )
            == 27,
            "detail": f"nodes={len(all_node_rows)}; expected=27",
        },
        {
            "check_id": "ALL_EFFECTIVE_NODE_GATES_PASS",
            "passed": all(
                parse_bool(row["integrity_passed"])
                and parse_bool(row["acceptance_passed"])
                for row in all_node_rows
            ),
            "detail": (
                "passed="
                f"{sum(parse_bool(row['integrity_passed']) and parse_bool(row['acceptance_passed']) for row in all_node_rows)}"
                f"/{len(all_node_rows)}"
            ),
        },
        {
            "check_id": "NO_THIRD_OR_AMBIGUOUS_SIGNATURE",
            "passed": int(
                state["third_or_ambiguous_signature_count"]
            )
            == 0,
            "detail": (
                "count="
                f"{state['third_or_ambiguous_signature_count']}"
            ),
        },
        {
            "check_id": "ALL_CERTIFIED_WIDTH_GATES_PASS",
            "passed": all(
                float(row["final_width"])
                <= float(row["certified_target_width"])
                and parse_bool(row["stopping_gate_passed"])
                for row in final_rows
            ),
            "detail": (
                "maximum_width_target_ratio="
                f"{max(float(row['final_width']) / float(row['certified_target_width']) for row in final_rows)}"
            ),
        },
        {
            "check_id": "ALL_BOUNDARY_ERROR_BUDGETS_PASS",
            "passed": all(
                float(row["boundary_location_error_upper"])
                <= float(row["equal_boundary_budget"])
                for row in final_rows
            ),
            "detail": (
                "maximum_error_budget_ratio="
                f"{max(float(row['boundary_location_error_upper']) / float(row['equal_boundary_budget']) for row in final_rows)}"
            ),
        },
        {
            "check_id": "FORMALIZATION_WORKBENCH_UNCHANGED",
            "passed": len(formal_diff_rows) == 0,
            "detail": f"modified_files={len(formal_diff_rows)}",
        },
        {
            "check_id": "CLAIM_SCOPE_STAYS_PRE_COEFFICIENT",
            "passed": all(
                parse_bool(row["valid_for_boundary_error_claim"])
                and not parse_bool(row["valid_for_numeric_UV_claim"])
                and not parse_bool(row["valid_for_local_GR_claim"])
                and not parse_bool(row["valid_for_full_MTS_claim"])
                for row in final_rows
            ),
            "detail": (
                "boundary location only; coefficient and GR "
                "claims remain false"
            ),
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "residue_fit_method": (
            "constant_occupation_bare_Laurent"
        ),
        "quadrature_orders": list(REPAIR_ORDERS),
        "node_count": len(all_node_rows),
        "completed_generation": state["completed_generation"],
        "new_residue_fit_count": len(new_fit_rows),
        "maximum_physical_repair_relative_shift": maximum_shift,
        "all_boundary_stopping_gates_passed": all(
            parse_bool(row["stopping_gate_passed"])
            for row in final_rows
        ),
        "maximum_final_width_to_target_ratio": max(
            float(row["final_width"])
            / float(row["certified_target_width"])
            for row in final_rows
        ),
        "maximum_final_error_to_budget_ratio": max(
            float(row["boundary_location_error_upper"])
            / float(row["equal_boundary_budget"])
            for row in final_rows
        ),
        "formalization_workbench_modified_file_count": len(
            formal_diff_rows
        ),
        "decision": (
            "ADOPT_OCCUPATION_SEPARATED_LAURENT_RESIDUE__"
            "HANDOFF_TO_OUTER_COEFFICIENT_REASSEMBLY"
            if passed
            else "HOLD_OCCUPATION_SEPARATED_BOUNDARY_COMPLETION"
        ),
        "valid_for_boundary_error_claim": passed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(ALL_NODES, all_node_rows)
    write_csv(FINAL_BRACKETS, final_rows)
    write_csv(VALIDATION, checks)
    atomic_json(RESULT, result)
    write_document(result)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "complete" if passed else "validation_failed",
            "completed_generation": state["completed_generation"],
            "node_count": len(all_node_rows),
            "validation_passed": passed,
            "run_signature": run_signature,
        },
    )
    if not passed:
        failed_checks = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"5264 validation failed: {failed_checks}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        result = dry_run()
        print(json.dumps(result, indent=2, sort_keys=True))
        if not result["dry_run_passed"]:
            raise SystemExit(1)
        return
    started = time.perf_counter()
    result = execute()
    print(
        json.dumps(
            {
                **result,
                "elapsed_seconds": time.perf_counter() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
