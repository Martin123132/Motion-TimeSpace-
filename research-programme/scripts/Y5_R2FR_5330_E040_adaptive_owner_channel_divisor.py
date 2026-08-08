from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5330"
SOURCE_5327 = FUNCTIONAL_RG / "5327" / "E040"

SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
CLASSIFICATIONS_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_pole_classification.csv"
POLES_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_geometric_poles.csv"
DRY_RUN_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_dry_run.json"

DRY_RUN = SOURCE / "E040_adaptive_divisor_dry_run.json"
INPUT_SNAPSHOT = SOURCE / "E040_adaptive_divisor_input.csv"
POLE_SNAPSHOT = SOURCE / "E040_adaptive_divisor_poles.csv"
ROOT_ROWS = SOURCE / "E040_adaptive_divisor_roots.csv"
SAMPLE_ROWS = SOURCE / "E040_adaptive_divisor_samples.csv"
FIT_ROWS = SOURCE / "E040_adaptive_divisor_fits.csv"
CERTIFICATE_ROWS = SOURCE / "E040_adaptive_divisor_certificates.csv"
FAMILY_ROWS = SOURCE / "E040_adaptive_divisor_family_audit.csv"
FAMILY_REFERENCE = SOURCE / "E040_adaptive_divisor_family_history_reference.csv"
PATH_ROWS = SOURCE / "E040_resolvent_path_audit.csv"
RESULT = SOURCE / "E040_adaptive_divisor_result.json"
VALIDATION = SOURCE / "E040_adaptive_divisor_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5330_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5330-Y5-R2FR-E040-adaptive-owner-channel-divisor-theorem.md"

CHECKPOINT = 5330
PARENT_CHECKPOINT = 5329
MARKER = "MTS_5330_E040_ADAPTIVE_OWNER_CHANNEL_DIVISOR_THEOREM"
REVISION = "E040-adaptive-owner-channel-divisor-v1"
EPSILON_ID = "E040"

FIT_SCALES = (0.25, 0.5, 1.0)
SYMMETRIC_FIT_FRACTIONS = (-4.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 4.0)
INTERIOR_FIT_FRACTIONS = (-1.0, -0.75, -0.5, -0.375, -0.25, -0.125, -0.0625, 0.0)
LOCAL_NUMERATOR_FIT_DEGREES = (5, 6)
EXTRAPOLATED_NUMERATOR_FIT_DEGREES = (2, 3)
CHANNEL_CONTINUATION_DEGREES = (5, 6)
MAXIMUM_RADIUS_HALVINGS = 6
ROOT_RESIDUAL_LIMIT = 1.0e-10
ROOT_NORMALIZED_RESIDUAL_LIMIT = 1.0e-5
ROOT_SHIFT_RADIUS_FRACTION_LIMIT = 0.25
DERIVATIVE_CHANGE_LIMIT = 1.0e-3
CHANNEL_CONTINUATION_ROOT_CHANGE_LIMIT = 1.0e-5
CHANNEL_CONTINUATION_ROOT_UNCERTAINTY_CORE_FRACTION_LIMIT = 1.0e-3
INTERIOR_CONTINUATION_RATIO_TRIGGER = 4.0
LOW_ORDER_CONTINUATION_RATIO_TRIGGER = 0.75
INTERIOR_CONTINUATION_MAXIMUM_CORE_SPAN = 8.0
NUMERATOR_FIT_RESIDUAL_LIMIT = 5.0e-5
COEFFICIENT_CHANGE_LIMIT = 1.0e-6
ROOT_EQUATION_RESIDUAL_LIMIT = 1.0e-30
ROOT_REFINEMENT_CHORDAL_LIMIT = 1.0e-6
RESIDUE_STABILITY_LIMIT = 5.0e-4
MATERIAL_RESIDUE_FLOOR = 1.0e-6
REMOVABLE_RESIDUE_CEILING = 1.0e-8

CLAIM_FIELDS = (
    "valid_for_D2_regulator_zero_limit",
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
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for field in leading_fields or []:
        if field not in fields:
            fields.append(field)
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    return abs(second - first) / max(abs(first), abs(second), 1.0e-300)


def target_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return str(row["node_id"]), str(row["term_id"]), str(row["pole_id"])


def family_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(row["term_id"]),
        str(row["pole_id"]),
        str(row["primary_surface_id"]),
    )


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def central_derivative(
    function: Callable[[complex], complex],
    point: complex,
    step: float,
) -> complex:
    return (function(point + step) - function(point - step)) / (2.0 * step)


def base_fit_radius(
    row: dict[str, Any],
    poles: list[dict[str, Any]],
) -> float:
    center = float(row["real_axis_center"])
    lower = float(row["support_energy_lower"])
    upper = float(row["support_energy_upper"])
    separations = [
        abs(center - float(other["real_axis_center"]))
        for other in poles
        if target_key(other) != target_key(row)
        and other["node_id"] == row["node_id"]
        and other["term_id"] == row["term_id"]
        and other["support_id"] == row["support_id"]
    ]
    margin = min(center - lower, upper - center, *(separations or [1.0]))
    if margin <= 0.0:
        raise RuntimeError(f"nonpositive support margin for {target_key(row)}")
    core = max(abs(float(row["pole_imaginary"])), 1.0e-7)
    return min(max(8.0 * core, 2.0e-6), margin / 10.0)


def numerator_sampling_strategy(
    pole: complex,
    initial_radius: float,
) -> tuple[str, float, tuple[float, ...], tuple[int, ...]]:
    core = max(abs(pole.imag), 1.0e-7)
    extrapolation_ratio = abs(pole.imag) / max(initial_radius, 1.0e-300)
    if extrapolation_ratio > INTERIOR_CONTINUATION_RATIO_TRIGGER:
        return (
            "BOUNDARY_INTERIOR_ANALYTIC_CONTINUATION",
            INTERIOR_CONTINUATION_MAXIMUM_CORE_SPAN * core,
            INTERIOR_FIT_FRACTIONS,
            EXTRAPOLATED_NUMERATOR_FIT_DEGREES,
        )
    if extrapolation_ratio > LOW_ORDER_CONTINUATION_RATIO_TRIGGER:
        return (
            "SYMMETRIC_LOW_ORDER_ANALYTIC_CONTINUATION",
            initial_radius,
            SYMMETRIC_FIT_FRACTIONS,
            EXTRAPOLATED_NUMERATOR_FIT_DEGREES,
        )
    return (
        "SYMMETRIC_LOCAL_DIVISOR",
        initial_radius,
        SYMMETRIC_FIT_FRACTIONS,
        LOCAL_NUMERATOR_FIT_DEGREES,
    )


def refine_channel_root(
    row: dict[str, Any],
    poles: list[dict[str, Any]],
    function: Callable[[complex], complex],
) -> tuple[dict[str, Any], complex, complex, float]:
    initial = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
    radius = base_fit_radius(row, poles)
    core = max(abs(initial.imag), 1.0e-7)
    derivative_step = min(1.0e-6, max(1.0e-8, 0.25 * core))
    refinement_mode = "DIRECT_COMPLEX_NEWTON"
    continuation_fit_residual = 0.0
    continuation_root_change = 0.0
    continuation_root_uncertainty = 0.0
    continuation_root_uncertainty_core_fraction = 0.0
    iterations = 0
    try:
        pole = initial
        best = initial
        best_residual = abs(function(initial))
        for iterations in range(1, 17):
            derivative = central_derivative(function, pole, derivative_step)
            if abs(derivative) <= 1.0e-300:
                break
            updated = pole - function(pole) / derivative
            if abs(updated - initial) > max(radius, 1.0e-5):
                break
            pole = updated
            residual = abs(function(pole))
            if residual < best_residual:
                best = pole
                best_residual = residual
            if residual <= 1.0e-14:
                break
        pole = best
        derivative_steps = (
            derivative_step,
            derivative_step / 2.0,
            derivative_step / 4.0,
        )
        derivatives = [
            central_derivative(function, pole, step) for step in derivative_steps
        ]
        derivative = derivatives[-1]
        derivative_change = max(
            relative_complex_change(first, second)
            for first, second in zip(derivatives, derivatives[1:])
        )
        residual = abs(function(pole))
        normalized_residual = residual / max(abs(derivative) * core, 1.0e-300)
        final_derivative_step = derivative_steps[-1]
    except Exception:
        refinement_mode = "REAL_AXIS_ANALYTIC_CONTINUATION"
        fractions = np.asarray(
            (-4.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 4.0),
            dtype=float,
        )
        values = np.asarray(
            [function(complex(initial.real + radius * fraction)) for fraction in fractions],
            dtype=np.complex128,
        )
        target_scaled = (initial - initial.real) / radius
        candidates: list[dict[str, Any]] = []
        for degree in CHANNEL_CONTINUATION_DEGREES:
            matrix = np.column_stack(
                [fractions**power for power in range(degree + 1)]
            )
            coefficients, _, _, _ = np.linalg.lstsq(matrix, values, rcond=None)
            predicted = matrix @ coefficients
            fit_residual = float(
                np.linalg.norm(predicted - values)
                / max(float(np.linalg.norm(values)), 1.0e-300)
            )
            roots = np.roots(coefficients[::-1])
            selected_root = min(roots, key=lambda value: abs(value - target_scaled))
            derivative_value = sum(
                power * coefficients[power] * selected_root ** (power - 1)
                for power in range(1, degree + 1)
            ) / radius
            equation_residual = abs(
                sum(
                    coefficients[power] * selected_root**power
                    for power in range(degree + 1)
                )
            )
            maximum_absolute_fit_error = float(
                np.max(np.abs(predicted - values))
            )
            candidates.append(
                {
                    "degree": degree,
                    "root": complex(initial.real + radius * selected_root),
                    "derivative": complex(derivative_value),
                    "fit_residual": fit_residual,
                    "equation_residual": equation_residual,
                    "maximum_absolute_fit_error": maximum_absolute_fit_error,
                }
            )
        selected = candidates[-1]
        pole = selected["root"]
        derivative = selected["derivative"]
        continuation_fit_residual = max(
            float(candidate["fit_residual"]) for candidate in candidates
        )
        continuation_root_change = relative_complex_change(
            complex(candidates[-2]["root"]),
            pole,
        )
        derivative_change = relative_complex_change(
            complex(candidates[-2]["derivative"]),
            derivative,
        )
        continuation_root_uncertainty = max(
            float(candidate["maximum_absolute_fit_error"])
            for candidate in candidates
        ) / max(
            min(abs(complex(candidate["derivative"])) for candidate in candidates),
            1.0e-300,
        )
        continuation_root_uncertainty_core_fraction = (
            continuation_root_uncertainty / core
        )
        residual = float(selected["equation_residual"])
        normalized_residual = residual / max(abs(derivative) * core, 1.0e-300)
        final_derivative_step = radius
    shift = abs(pole - initial)
    controls_pass = (
        residual <= ROOT_RESIDUAL_LIMIT
        and normalized_residual <= ROOT_NORMALIZED_RESIDUAL_LIMIT
        and abs(derivative) > 1.0e-12
        and derivative_change <= DERIVATIVE_CHANGE_LIMIT
        and shift <= max(ROOT_SHIFT_RADIUS_FRACTION_LIMIT * radius, 1.0e-8)
        and math.isfinite(continuation_fit_residual)
        and continuation_root_change <= CHANNEL_CONTINUATION_ROOT_CHANGE_LIMIT
        and continuation_root_uncertainty_core_fraction
        <= CHANNEL_CONTINUATION_ROOT_UNCERTAINTY_CORE_FRACTION_LIMIT
    )
    result = {
        "node_id": row["node_id"],
        "term_id": row["term_id"],
        "pole_id": row["pole_id"],
        "support_id": row["support_id"],
        "primary_surface_id": row["primary_surface_id"],
        **complex_fields("initial_pole", initial),
        **complex_fields("refined_pole", pole),
        "pole_refinement_shift": shift,
        "channel_root_residual": residual,
        "channel_root_normalized_residual": normalized_residual,
        **complex_fields("channel_derivative", derivative),
        "channel_derivative_relative_change": derivative_change,
        "derivative_step": final_derivative_step,
        "root_refinement_mode": refinement_mode,
        "analytic_continuation_fit_relative_residual": continuation_fit_residual,
        "analytic_continuation_root_relative_change": continuation_root_change,
        "analytic_continuation_root_uncertainty": continuation_root_uncertainty,
        "analytic_continuation_root_uncertainty_core_fraction": (
            continuation_root_uncertainty_core_fraction
        ),
        "newton_iteration_count": iterations,
        "initial_fit_radius": radius,
        "channel_root_controls_pass": controls_pass,
        **{field: False for field in CLAIM_FIELDS},
    }
    return result, pole, derivative, radius


def sample_numerator(
    row: dict[str, Any],
    function: Callable[[complex], complex],
    pole: complex,
    initial_radius: float,
    evaluate: Callable[..., dict[str, Any]],
) -> tuple[list[dict[str, Any]], float, int, str]:
    coordinate = float(row["absolute_soft_cosine"])
    soft_sign = int(row["soft_sign"])
    decay_sign = int(row["decay_sign"])
    (
        sampling_mode,
        strategy_radius,
        fit_fractions,
        fit_degrees,
    ) = numerator_sampling_strategy(pole, initial_radius)
    failure = ""
    for halving in range(MAXIMUM_RADIUS_HALVINGS + 1):
        radius = strategy_radius / (2.0**halving)
        rows: list[dict[str, Any]] = []
        try:
            for scale in FIT_SCALES:
                local_radius = scale * radius
                for fraction in fit_fractions:
                    energy = pole.real + local_radius * fraction
                    if not (
                        float(row["support_energy_lower"])
                        < energy
                        < float(row["support_energy_upper"])
                    ):
                        raise RuntimeError("fit sample left active support")
                    evaluation = evaluate(
                        float(energy),
                        coordinate,
                        soft_sign,
                        decay_sign,
                    )
                    contribution = complex(evaluation["residue"])
                    channel_value = function(complex(energy))
                    numerator = channel_value * contribution
                    rows.append(
                        {
                            "node_id": row["node_id"],
                            "term_id": row["term_id"],
                            "pole_id": row["pole_id"],
                            "support_id": row["support_id"],
                            "primary_surface_id": row["primary_surface_id"],
                            "radius_halving_count": halving,
                            "numerator_sampling_mode": sampling_mode,
                            "numerator_fit_degrees": "|".join(
                                str(degree) for degree in fit_degrees
                            ),
                            "pole_to_initial_radius_ratio": (
                                abs(pole.imag) / max(initial_radius, 1.0e-300)
                            ),
                            "fit_scale": scale,
                            "fit_radius": local_radius,
                            "fraction": fraction,
                            "energy": energy,
                            **complex_fields("channel", channel_value),
                            **complex_fields("contribution", contribution),
                            **complex_fields("numerator", numerator),
                            "mask_active": evaluation["mask_active"],
                            "law_active": evaluation["law_active"],
                            "mask_agrees": evaluation["mask_agrees"],
                            "orientation": evaluation["orientation"],
                            "representing_pair": evaluation["representing_pair"],
                            "selected_role": evaluation["selected_role"],
                            "root_equation_residual": evaluation[
                                "root_equation_residual"
                            ],
                            "root_refinement_chordal_distance": evaluation[
                                "root_refinement_chordal_distance"
                            ],
                            "coefficient_relative_change": evaluation[
                                "coefficient_relative_change"
                            ],
                            "evaluation_status": evaluation["evaluation_status"],
                            **{field: False for field in CLAIM_FIELDS},
                        }
                    )
        except Exception as error:
            failure = f"{type(error).__name__}: {error}"
            continue
        labels = {str(local["representing_pair"]) for local in rows}
        roles = {str(local["selected_role"]) for local in rows}
        orientations = {int(local["orientation"]) for local in rows}
        preflight_passes = (
            len(rows) == len(FIT_SCALES) * len(fit_fractions)
            and all(parse_bool(local["mask_active"]) for local in rows)
            and all(parse_bool(local["law_active"]) for local in rows)
            and all(parse_bool(local["mask_agrees"]) for local in rows)
            and all(local["evaluation_status"] == "EVALUATED" for local in rows)
            and len(labels) == 1
            and len(roles) == 1
            and len(orientations) == 1
        )
        if preflight_passes:
            return rows, radius, halving, ""
        failure = (
            f"selector_orbit_preflight_failed:labels={len(labels)};"
            f"roles={len(roles)};orientations={len(orientations)}"
        )
    return (
        [],
        strategy_radius / (2.0**MAXIMUM_RADIUS_HALVINGS),
        MAXIMUM_RADIUS_HALVINGS,
        failure,
    )


def fit_numerator(
    row: dict[str, Any],
    pole: complex,
    derivative: complex,
    samples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scale in FIT_SCALES:
        local = [sample for sample in samples if float(sample["fit_scale"]) == scale]
        fractions = np.asarray([float(sample["fraction"]) for sample in local])
        values = np.asarray(
            [
                complex(
                    float(sample["numerator_real"]),
                    float(sample["numerator_imaginary"]),
                )
                for sample in local
            ],
            dtype=np.complex128,
        )
        radius = float(local[0]["fit_radius"])
        scaled_pole = (pole - pole.real) / radius
        fit_degrees = tuple(
            int(value)
            for value in str(local[0]["numerator_fit_degrees"]).split("|")
        )
        for degree in fit_degrees:
            matrix = np.column_stack(
                [fractions**power for power in range(degree + 1)]
            )
            coefficients, _, _, _ = np.linalg.lstsq(matrix, values, rcond=None)
            predicted = matrix @ coefficients
            residual = float(
                np.linalg.norm(predicted - values)
                / max(float(np.linalg.norm(values)), 1.0e-300)
            )
            numerator_at_pole = sum(
                coefficients[power] * scaled_pole**power
                for power in range(degree + 1)
            )
            residue = numerator_at_pole / derivative
            rows.append(
                {
                    "node_id": row["node_id"],
                    "term_id": row["term_id"],
                    "pole_id": row["pole_id"],
                    "support_id": row["support_id"],
                    "primary_surface_id": row["primary_surface_id"],
                    "fit_scale": scale,
                    "fit_radius": radius,
                    "fit_sample_count": len(local),
                    "background_polynomial_degree": degree,
                    "numerator_sampling_mode": local[0][
                        "numerator_sampling_mode"
                    ],
                    "scaled_pole_magnitude": abs(scaled_pole),
                    **complex_fields("numerator_at_pole", numerator_at_pole),
                    **complex_fields("fitted_residue", residue),
                    "fit_relative_residual": residual,
                    "all_fit_samples_mask_active": all(
                        parse_bool(sample["mask_active"]) for sample in local
                    ),
                    "residue_derivation_method": (
                        "ADAPTIVE_OWNER_CHANNEL_ANALYTIC_DIVISOR"
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def classify_pole(
    source: dict[str, Any],
    pole_row: dict[str, Any],
    root: dict[str, Any],
    samples: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    final_radius: float,
    radius_halvings: int,
    preflight_failure: str,
) -> dict[str, Any]:
    selected_value = 0.0j
    all_values: list[complex] = []
    if fits:
        maximum_scale = max(float(row["fit_scale"]) for row in fits)
        maximum_degree = max(
            int(row["background_polynomial_degree"]) for row in fits
        )
        selected = next(
            row
            for row in fits
            if float(row["fit_scale"]) == maximum_scale
            and int(row["background_polynomial_degree"]) == maximum_degree
        )
        selected_value = complex(
            float(selected["fitted_residue_real"]),
            float(selected["fitted_residue_imaginary"]),
        )
        all_values = [
            complex(
                float(row["fitted_residue_real"]),
                float(row["fitted_residue_imaginary"]),
            )
            for row in fits
        ]
    residue_envelope = max((abs(value) for value in all_values), default=math.inf)
    residue_spread = max(
        (relative_complex_change(selected_value, value) for value in all_values),
        default=math.inf,
    )
    maximum_fit_residual = max(
        (float(row["fit_relative_residual"]) for row in fits),
        default=math.inf,
    )
    labels = {str(row["representing_pair"]) for row in samples}
    roles = {str(row["selected_role"]) for row in samples}
    orientations = {int(row["orientation"]) for row in samples}
    maximum_coefficient_change = max(
        (float(row["coefficient_relative_change"]) for row in samples),
        default=math.inf,
    )
    maximum_root_residual = max(
        (float(row["root_equation_residual"]) for row in samples),
        default=math.inf,
    )
    maximum_root_refinement = max(
        (float(row["root_refinement_chordal_distance"]) for row in samples),
        default=math.inf,
    )
    sample_controls = (
        bool(samples)
        and not preflight_failure
        and len(labels) == 1
        and len(roles) == 1
        and len(orientations) == 1
        and all(parse_bool(row["mask_active"]) for row in samples)
        and all(parse_bool(row["mask_agrees"]) for row in samples)
        and maximum_coefficient_change <= COEFFICIENT_CHANGE_LIMIT
        and maximum_root_residual <= ROOT_EQUATION_RESIDUAL_LIMIT
        and maximum_root_refinement <= ROOT_REFINEMENT_CHORDAL_LIMIT
    )
    common_controls = (
        parse_bool(root["channel_root_controls_pass"])
        and sample_controls
        and bool(fits)
        and maximum_fit_residual <= NUMERATOR_FIT_RESIDUAL_LIMIT
        and all(parse_bool(row["all_fit_samples_mask_active"]) for row in fits)
    )
    removable = common_controls and residue_envelope <= REMOVABLE_RESIDUE_CEILING
    material = (
        common_controls
        and min((abs(value) for value in all_values), default=0.0)
        >= MATERIAL_RESIDUE_FLOOR
        and residue_spread <= RESIDUE_STABILITY_LIMIT
    )
    controls_pass = removable or material
    observed_class = (
        "REMOVABLE" if removable else "MATERIAL" if material else "UNRESOLVED"
    )
    source_residue = complex(
        float(source["selected_residue_real"]),
        float(source["selected_residue_imaginary"]),
    )
    return {
        "node_id": source["node_id"],
        "x_panel_index": source["x_panel_index"],
        "outer_order": source["outer_order"],
        "absolute_soft_cosine": source["absolute_soft_cosine"],
        "term_id": source["term_id"],
        "support_id": source["support_id"],
        "pole_id": source["pole_id"],
        "primary_surface_id": pole_row["primary_surface_id"],
        **complex_fields(
            "geometric_pole",
            complex(float(pole_row["pole_real"]), float(pole_row["pole_imaginary"])),
        ),
        **complex_fields(
            "refined_pole",
            complex(
                float(root["refined_pole_real"]),
                float(root["refined_pole_imaginary"]),
            ),
        ),
        **complex_fields("source_direct_laurent_residue", source_residue),
        **complex_fields("certified_residue", selected_value),
        "certified_residue_envelope": residue_envelope,
        "certified_residue_relative_spread": residue_spread,
        "maximum_fit_relative_residual": maximum_fit_residual,
        "maximum_coefficient_relative_change": maximum_coefficient_change,
        "maximum_root_equation_residual": maximum_root_residual,
        "maximum_root_refinement_chordal_distance": maximum_root_refinement,
        "selector_label_count": len(labels),
        "selector_labels": "||".join(sorted(labels)),
        "selector_role_count": len(roles),
        "selector_roles": "|".join(sorted(roles)),
        "selector_orientation_count": len(orientations),
        "selector_orientations": "|".join(
            str(value) for value in sorted(orientations)
        ),
        "final_base_fit_radius": final_radius,
        "radius_halving_count": radius_halvings,
        "selector_preflight_failure": preflight_failure,
        "observed_classification": observed_class,
        "pole_classification": (
            "ADAPTIVE_DIVISOR_BOUNDED_ZERO_REMOVABLE"
            if removable
            else "ADAPTIVE_DIVISOR_STABLE_MATERIAL_SIMPLE_POLE"
            if material
            else "ADAPTIVE_DIVISOR_CLASSIFICATION_UNRESOLVED"
        ),
        "material_simple_pole": material,
        "removable_zero_residue_pole": removable,
        "pole_classification_resolved": controls_pass,
        "adaptive_divisor_controls_pass": controls_pass,
        "valid_for_E040_adaptive_divisor_certificate": controls_pass,
        "valid_for_E040_node_rerun": controls_pass,
        **{field: False for field in CLAIM_FIELDS},
    }


def classify_adaptive_pole(
    source: dict[str, Any],
    pole_row: dict[str, Any],
    poles: list[dict[str, Any]],
    owner_function: Callable[[complex], complex],
    evaluate: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    root, refined_pole, derivative, initial_radius = refine_channel_root(
        pole_row,
        poles,
        owner_function,
    )
    samples, final_radius, halvings, failure = sample_numerator(
        pole_row,
        owner_function,
        refined_pole,
        initial_radius,
        evaluate,
    )
    fits = (
        fit_numerator(pole_row, refined_pole, derivative, samples)
        if samples
        else []
    )
    certificate = classify_pole(
        source,
        pole_row,
        root,
        samples,
        fits,
        final_radius,
        halvings,
        failure,
    )
    return {
        "root": root,
        "samples": samples,
        "fits": fits,
        "certificate": certificate,
    }


def source_path_audit() -> list[dict[str, Any]]:
    return [
        {
            "object": "owner denominator F_X",
            "source_path": str(
                SCRIPTS
                / "Y5_R2FR_5235_dynamic_all_channel_conditional_A00_slice_pilot.py"
            ),
            "source_symbol": "surface_value",
            "construction": "scalar physical pair invariant",
            "matrix_inverse_present": False,
            "resolvent_mapping_valid": False,
        },
        {
            "object": "selected response C_X",
            "source_path": str(
                SCRIPTS
                / "Y5_R2FR_5231_local_double_residue_identity_and_pooled_A00_tail_decomposition.py"
            ),
            "source_symbol": "safe_family_contributions",
            "construction": "winding-weighted collision residue",
            "matrix_inverse_present": False,
            "resolvent_mapping_valid": False,
        },
        {
            "object": "collision coefficient",
            "source_path": str(
                SCRIPTS / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
            ),
            "source_symbol": "finite_plus_components",
            "construction": "KLT direct plus soft endpoint subtraction",
            "matrix_inverse_present": False,
            "resolvent_mapping_valid": False,
        },
    ]


def full_component_evaluator(module: Any, base_context: dict[str, Any]) -> Callable[..., dict[str, Any]]:
    cache: dict[tuple[float, float, int, int], dict[str, Any]] = {}
    contexts: dict[tuple[float, int, int], dict[str, Any]] = {}

    def evaluate(
        energy: float,
        coordinate: float,
        soft_sign: int,
        decay_sign: int,
    ) -> dict[str, Any]:
        key = (float(energy), float(coordinate), soft_sign, decay_sign)
        if key in cache:
            return cache[key]
        context_key = (float(coordinate), soft_sign, decay_sign)
        if context_key not in contexts:
            contexts[context_key] = module.M5326.M5312.M5308.M5302.local_context(
                base_context,
                coordinate,
                soft_sign,
                decay_sign,
            )
        context = contexts[context_key]
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        target = context["inventories"][EPSILON_ID]["target"]
        rationals = module.M5326.M5312.M5280.M5274.M5231.root_rationals(
            event,
            target,
        )
        cache[key] = module.M5326.M5312.M5280.evaluate_component(
            event,
            EPSILON_ID,
            "MC04",
            context,
            rationals=rationals,
            convergence_audit=True,
        )
        return cache[key]

    return evaluate


def owner_channel_function(
    module: Any,
    row: dict[str, Any],
) -> Callable[[complex], complex]:
    coordinate = float(row["absolute_soft_cosine"])
    soft_sign = int(row["soft_sign"])
    decay_sign = int(row["decay_sign"])
    problem = module.M5326.M5312.M5311.synthetic_energy_problem(
        "MC04",
        soft_sign * coordinate,
        decay_sign * module.M5326.M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE,
    )
    surface_id = str(row["primary_surface_id"])
    return lambda energy: complex(
        module.M5326.M5312.M5291.M5267.M5239.owner_surface_values(
            problem,
            complex(energy),
        )[surface_id]
    )


def unresolved_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(CLASSIFICATIONS_5327)
        if not parse_bool(row["pole_classification_resolved"])
    ]


EXPECTED_PATTERN_COUNTS = {
    ("MC04_SP_DM", "MC04_P02"): 21,
    ("MC04_SM_DM", "MC04_P01"): 4,
    ("MC04_SP_DP", "MC04_P01"): 5,
}


def unresolved_pattern_counts(
    rows: list[dict[str, Any]],
) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = str(row["term_id"]), str(row["pole_id"])
        counts[key] = counts.get(key, 0) + 1
    return counts


def frozen_seed_bundle() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    return (
        read_csv(INPUT_SNAPSHOT),
        read_csv(POLE_SNAPSHOT),
        read_csv(FAMILY_REFERENCE),
    )


def frozen_seed_is_valid() -> bool:
    if not all(path.exists() for path in (INPUT_SNAPSHOT, POLE_SNAPSHOT, FAMILY_REFERENCE)):
        return False
    source, poles, families = frozen_seed_bundle()
    source_keys = {target_key(row) for row in source}
    family_expectations = {
        ("MC04_SP_DM", "MC04_P02", "direct:R:s01"): "REMOVABLE",
        ("MC04_SM_DM", "MC04_P01", "direct:L:s14"): "MATERIAL",
        ("MC04_SP_DP", "MC04_P01", "direct:shared:s13"): "MATERIAL",
    }
    return (
        len(source) == 30
        and unresolved_pattern_counts(source) == EXPECTED_PATTERN_COUNTS
        and len(poles) == 30
        and {target_key(row) for row in poles} == source_keys
        and len(families) == 3
        and {
            family_key(row): str(row["historical_classes"])
            for row in families
        }
        == family_expectations
        and all(parse_bool(row["agrees_with_resolved_family"]) for row in families)
    )


def adaptive_seed_bundle() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    str,
]:
    live_source = unresolved_rows()
    live_poles = read_csv(POLES_5327)
    live_lookup = {target_key(row): row for row in live_poles}
    if (
        len(live_source) == 30
        and unresolved_pattern_counts(live_source) == EXPECTED_PATTERN_COUNTS
        and all(target_key(row) in live_lookup for row in live_source)
    ):
        return live_source, live_poles, "LIVE_CONTROLLER_AGGREGATE"
    if frozen_seed_is_valid():
        frozen_source, frozen_poles, _ = frozen_seed_bundle()
        return frozen_source, frozen_poles, "IMMUTABLE_5330_SEED"
    return [], [], "UNAVAILABLE"


def family_audit_from_reference(
    certificates: list[dict[str, Any]],
    references: list[dict[str, str]],
) -> list[dict[str, Any]]:
    reference_lookup = {family_key(row): row for row in references}
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in certificates:
        grouped.setdefault(family_key(row), []).append(row)
    rows: list[dict[str, Any]] = []
    for key, values in sorted(grouped.items()):
        reference = reference_lookup.get(key, {})
        observed = {str(row["observed_classification"]) for row in values}
        historical = {
            value
            for value in str(reference.get("historical_classes", "")).split("|")
            if value
        }
        coordinates = [float(row["absolute_soft_cosine"]) for row in values]
        rows.append(
            {
                "term_id": key[0],
                "pole_id": key[1],
                "primary_surface_id": key[2],
                "adaptive_certificate_count": len(values),
                "coordinate_minimum": min(coordinates),
                "coordinate_maximum": max(coordinates),
                "adaptive_classes": "|".join(sorted(observed)),
                "historical_resolved_count": int(reference.get("historical_resolved_count", 0)),
                "historical_classes": "|".join(sorted(historical)),
                "single_adaptive_class": len(observed) == 1,
                "agrees_with_resolved_family": bool(historical) and observed == historical,
                "valid_for_future_coordinate_without_fresh_divisor_test": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def family_audit_rows(
    certificates: list[dict[str, Any]],
    all_classifications: list[dict[str, str]],
    all_poles: list[dict[str, str]],
) -> list[dict[str, Any]]:
    pole_lookup = {target_key(row): row for row in all_poles}
    historical: dict[tuple[str, str, str], set[str]] = {}
    historical_counts: dict[tuple[str, str, str], int] = {}
    for row in all_classifications:
        if not parse_bool(row["pole_classification_resolved"]):
            continue
        pole = pole_lookup[target_key(row)]
        key = family_key(pole)
        observed = (
            "REMOVABLE"
            if parse_bool(row["removable_zero_residue_pole"])
            else "MATERIAL"
            if parse_bool(row["material_simple_pole"])
            else "UNRESOLVED"
        )
        historical.setdefault(key, set()).add(observed)
        historical_counts[key] = historical_counts.get(key, 0) + 1
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in certificates:
        grouped.setdefault(family_key(row), []).append(row)
    rows: list[dict[str, Any]] = []
    for key, values in sorted(grouped.items()):
        observed = {str(row["observed_classification"]) for row in values}
        prior = historical.get(key, set())
        coordinates = [float(row["absolute_soft_cosine"]) for row in values]
        rows.append(
            {
                "term_id": key[0],
                "pole_id": key[1],
                "primary_surface_id": key[2],
                "adaptive_certificate_count": len(values),
                "coordinate_minimum": min(coordinates),
                "coordinate_maximum": max(coordinates),
                "adaptive_classes": "|".join(sorted(observed)),
                "historical_resolved_count": historical_counts.get(key, 0),
                "historical_classes": "|".join(sorted(prior)),
                "single_adaptive_class": len(observed) == 1,
                "agrees_with_resolved_family": bool(prior) and observed == prior,
                "valid_for_future_coordinate_without_fresh_divisor_test": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    required = (SCRIPT_5327, CLASSIFICATIONS_5327, POLES_5327, DRY_RUN_5327)
    missing = [str(path) for path in required if not path.exists()]
    source, _, input_mode = adaptive_seed_bundle() if not missing else ([], [], "UNAVAILABLE")
    counts = unresolved_pattern_counts(source)
    accepted = (
        not missing
        and len(source) == 30
        and counts == EXPECTED_PATTERN_COUNTS
        and input_mode in {"LIVE_CONTROLLER_AGGREGATE", "IMMUTABLE_5330_SEED"}
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "acceptance_passed": accepted,
        "decision": (
            "E040_ADAPTIVE_DIVISOR_DRY_RUN_ACCEPTED__RUN"
            if accepted
            else "E040_ADAPTIVE_DIVISOR_DRY_RUN_BLOCKED"
        ),
        "unresolved_input_count": len(source),
        "input_source_mode": input_mode,
        "pattern_counts": {f"{key[0]}|{key[1]}": value for key, value in counts.items()},
        "missing_paths": missing,
    }
    atomic_json(DRY_RUN, result)
    return result


def run() -> dict[str, Any]:
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5330 dry run did not pass")
    module = load_module("mts_5327_for_5330", SCRIPT_5327)
    module.OWNER_CHANNEL_CERTIFICATE_BYPASS = True
    module.M5326.M5312.set_below_normal_priority()
    module.configure_target(EPSILON_ID)
    source, poles, input_mode = adaptive_seed_bundle()
    pole_lookup = {target_key(row): row for row in poles}
    selected_poles = [pole_lookup[target_key(row)] for row in source]
    if input_mode == "LIVE_CONTROLLER_AGGREGATE":
        write_csv(INPUT_SNAPSHOT, source, ["node_id", "term_id", "pole_id"])
        write_csv(POLE_SNAPSHOT, selected_poles, ["node_id", "term_id", "pole_id"])
    path_rows = source_path_audit()
    for row in path_rows:
        path = Path(row["source_path"])
        row["source_exists"] = path.exists()
        row["source_sha256"] = digest(path) if path.exists() else ""
    write_csv(PATH_ROWS, path_rows)
    base_context = module.M5326.M5312.M5303.synthetic_context()
    evaluate = full_component_evaluator(module, base_context)
    old = module.M5326.configure_kernel()
    root_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    certificate_rows: list[dict[str, Any]] = []
    formal_start = module.M5283.formal_inventory_digest()
    atomic_json(
        STATUS,
        {
            "state": "RUNNING",
            "stage": "ADAPTIVE_OWNER_CHANNEL_DIVISOR",
            "completed": 0,
            "total": len(source),
        },
    )
    try:
        for index, source_row in enumerate(source, start=1):
            pole_row = pole_lookup[target_key(source_row)]
            outcome = classify_adaptive_pole(
                source_row,
                pole_row,
                poles,
                owner_channel_function(module, pole_row),
                evaluate,
            )
            root_rows.append(outcome["root"])
            sample_rows.extend(outcome["samples"])
            fit_rows.extend(outcome["fits"])
            certificate_rows.append(outcome["certificate"])
            atomic_json(
                STATUS,
                {
                    "state": "RUNNING",
                    "stage": "ADAPTIVE_OWNER_CHANNEL_DIVISOR",
                    "completed": index,
                    "total": len(source),
                    "last_key": target_key(source_row),
                },
            )
    finally:
        module.M5326.restore_kernel(old)
    formal_end = module.M5283.formal_inventory_digest()
    family_rows = (
        family_audit_rows(
            certificate_rows,
            read_csv(CLASSIFICATIONS_5327),
            poles,
        )
        if input_mode == "LIVE_CONTROLLER_AGGREGATE"
        else family_audit_from_reference(
            certificate_rows,
            read_csv(FAMILY_REFERENCE),
        )
    )
    removable_count = sum(
        parse_bool(row["removable_zero_residue_pole"])
        for row in certificate_rows
    )
    material_count = sum(
        parse_bool(row["material_simple_pole"])
        for row in certificate_rows
    )
    accepted = (
        len(certificate_rows) == len(source)
        and all(parse_bool(row["adaptive_divisor_controls_pass"]) for row in certificate_rows)
        and removable_count == 21
        and material_count == 9
        and all(parse_bool(row["agrees_with_resolved_family"]) for row in family_rows)
        and formal_start == formal_end
    )
    source_paths = (
        (Path(__file__).resolve(), SCRIPT_5327, CLASSIFICATIONS_5327, POLES_5327)
        if input_mode == "LIVE_CONTROLLER_AGGREGATE"
        else (Path(__file__).resolve(), SCRIPT_5327, INPUT_SNAPSHOT, POLE_SNAPSHOT, FAMILY_REFERENCE)
    )
    source_files = [
        {"path": str(path), "sha256": digest(path)}
        for path in source_paths
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "adaptive-owner-channel-divisor",
        "acceptance_passed": accepted,
        "decision": (
            "E040_RESOLVENT_MAPPING_REJECTED__ANALYTIC_DIVISOR_30_OF_30_CERTIFIED"
            if accepted
            else "E040_ADAPTIVE_DIVISOR_REQUIRES_REFINEMENT"
        ),
        "resolvent_mapping_valid": False,
        "replacement_theorem": "JOINT_ANALYTIC_WEIERSTRASS_DIVISOR_REMAINDER",
        "input_unresolved_count": len(source),
        "input_source_mode": input_mode,
        "certified_count": len(certificate_rows),
        "removable_count": removable_count,
        "material_count": material_count,
        "maximum_removable_residue_envelope": max(
            (
                float(row["certified_residue_envelope"])
                for row in certificate_rows
                if parse_bool(row["removable_zero_residue_pole"])
            ),
            default=math.inf,
        ),
        "maximum_material_residue_relative_spread": max(
            (
                float(row["certified_residue_relative_spread"])
                for row in certificate_rows
                if parse_bool(row["material_simple_pole"])
            ),
            default=math.inf,
        ),
        "family_count": len(family_rows),
        "all_families_agree_with_resolved_history": all(
            parse_bool(row["agrees_with_resolved_family"]) for row in family_rows
        ),
        "future_coordinate_requires_fresh_divisor_test": True,
        "formal_digest_before": formal_start,
        "formal_digest_after": formal_end,
        "formal_modified_file_count": 0 if formal_start == formal_end else -1,
        "runtime_seconds": time.perf_counter() - started,
        "source_files": source_files,
        "claim_boundary": {
            "valid_for_adaptive_E040_pole_classification": accepted,
            **{field: False for field in CLAIM_FIELDS},
        },
    }
    write_csv(ROOT_ROWS, root_rows)
    write_csv(SAMPLE_ROWS, sample_rows)
    write_csv(FIT_ROWS, fit_rows)
    write_csv(CERTIFICATE_ROWS, certificate_rows)
    write_csv(FAMILY_ROWS, family_rows)
    atomic_json(RESULT, result)
    validations = validate(result)
    write_csv(VALIDATION, validations)
    write_csv(RESIDUAL_VALIDATION, validations)
    passed = bool(validations) and all(parse_bool(row["passed"]) for row in validations)
    render_document(result, family_rows, passed)
    atomic_json(
        STATUS,
        {
            "state": "COMPLETE" if passed else "FAILED",
            "stage": "VALIDATED",
            "completed": len(certificate_rows),
            "total": len(source),
            "acceptance_passed": passed,
        },
    )
    if not passed:
        raise RuntimeError("5330 adaptive divisor validation failed")
    return result


def validate(result: dict[str, Any]) -> list[dict[str, Any]]:
    roots = read_csv(ROOT_ROWS)
    samples = read_csv(SAMPLE_ROWS)
    fits = read_csv(FIT_ROWS)
    certificates = read_csv(CERTIFICATE_ROWS)
    families = read_csv(FAMILY_ROWS)
    paths = read_csv(PATH_ROWS)
    expected_keys = {target_key(row) for row in read_csv(INPUT_SNAPSHOT)}
    validations = [
        validation_gate(
            "actual_response_path_rejects_matrix_resolvent",
            len(paths) == 3
            and all(parse_bool(row["source_exists"]) for row in paths)
            and all(not parse_bool(row["resolvent_mapping_valid"]) for row in paths),
            f"rows={len(paths)}",
        ),
        validation_gate(
            "all_certification_seed_keys_are_snapshotted",
            len(expected_keys) == 30
            and {target_key(row) for row in read_csv(POLE_SNAPSHOT)} == expected_keys,
            f"keys={len(expected_keys)}",
        ),
        validation_gate(
            "every_owner_root_is_simple_and_refined",
            len(roots) == 30
            and {target_key(row) for row in roots} == expected_keys
            and all(parse_bool(row["channel_root_controls_pass"]) for row in roots),
            f"roots={len(roots)}",
        ),
        validation_gate(
            "selector_orbit_samples_are_complete",
            len(SYMMETRIC_FIT_FRACTIONS) == len(INTERIOR_FIT_FRACTIONS)
            and len(samples)
            == 30 * len(FIT_SCALES) * len(SYMMETRIC_FIT_FRACTIONS)
            and all(parse_bool(row["mask_active"]) for row in samples)
            and all(parse_bool(row["mask_agrees"]) for row in samples),
            f"samples={len(samples)}",
        ),
        validation_gate(
            "analytic_numerator_fits_are_complete",
            len(LOCAL_NUMERATOR_FIT_DEGREES)
            == len(EXTRAPOLATED_NUMERATOR_FIT_DEGREES)
            and len(fits)
            == 30 * len(FIT_SCALES) * len(LOCAL_NUMERATOR_FIT_DEGREES)
            and all(
                float(row["fit_relative_residual"]) <= NUMERATOR_FIT_RESIDUAL_LIMIT
                for row in fits
            ),
            f"fits={len(fits)}",
        ),
        validation_gate(
            "all_adaptive_descendants_are_classified",
            len(certificates) == 30
            and {target_key(row) for row in certificates} == expected_keys
            and all(parse_bool(row["adaptive_divisor_controls_pass"]) for row in certificates),
            f"certificates={len(certificates)}",
        ),
        validation_gate(
            "observed_classes_are_21_removable_and_9_material",
            sum(parse_bool(row["removable_zero_residue_pole"]) for row in certificates)
            == 21
            and sum(parse_bool(row["material_simple_pole"]) for row in certificates)
            == 9,
            f"removable={result['removable_count']};material={result['material_count']}",
        ),
        validation_gate(
            "adaptive_classes_match_independent_resolved_family_history",
            len(families) == 3
            and all(parse_bool(row["agrees_with_resolved_family"]) for row in families)
            and all(
                not parse_bool(row["valid_for_future_coordinate_without_fresh_divisor_test"])
                for row in families
            ),
            f"families={len(families)}",
        ),
        validation_gate(
            "claim_boundary_remains_local_to_pole_classification",
            bool(result["claim_boundary"]["valid_for_adaptive_E040_pole_classification"])
            and all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            json.dumps(result["claim_boundary"], sort_keys=True),
        ),
        validation_gate(
            "formalization_tree_is_unchanged",
            result["formal_digest_before"] == result["formal_digest_after"]
            and int(result["formal_modified_file_count"]) == 0,
            str(result["formal_digest_after"]),
        ),
        validation_gate(
            "source_paths_and_hashes_are_current",
            all(
                Path(row["path"]).exists()
                and digest(Path(row["path"])) == row["sha256"]
                for row in result["source_files"]
            ),
            f"sources={len(result['source_files'])}",
        ),
    ]
    return validations


def render_document(
    result: dict[str, Any],
    families: list[dict[str, Any]],
    passed: bool,
) -> None:
    family_lines = "\n".join(
        (
            f"- `{row['term_id']} / {row['pole_id']} / "
            f"{row['primary_surface_id']}`: `{row['adaptive_certificate_count']}` "
            f"adaptive rows, class `{row['adaptive_classes']}`, "
            f"resolved-history agreement `{row['agrees_with_resolved_family']}`."
        )
        for row in families
    )
    text = f"""# 5330 - E040 adaptive owner-channel divisor theorem

## Resolvent route

The proposed transfer-function shortcut is rejected for the actual E040
object.  The owner denominator `F_X` is a scalar physical pair invariant, and
the selected response `C_X` is a winding-weighted KLT/soft-subtracted collision
residue.  The implementation does not construct `C_X=c^dagger M^-1 b`, so a
left/right zero-mode overlap would be an invented representation rather than a
derivation.

## Correct theorem

Let `F(E,x)` and `N(E,x)` be jointly analytic near a simple owner branch
`F(E_p(x),x)=0`, with `partial_E F != 0`.  The implicit-function theorem makes
`E_p(x)` analytic.  Local analytic division gives

```text
N(E,x) = F(E,x) Q(E,x) + r(x),
r(x)   = N(E_p(x),x).
```

Therefore

```text
C(E,x) = Q(E,x) + r(x)/F(E,x),
Res[C(E,x) dE, E_p(x)] = r(x)/partial_E F(E_p(x),x).
```

The pole is removable exactly when `r(x)=0`; it is material when `r(x)!=0`.
Under any nonsingular analytic energy coordinate `E=phi(xi,x)`, the residue of
the one-form is invariant and the zero/nonzero classification is unchanged.
This is the coordinate-transfer statement that the adaptive controller needs.

The theorem does not license extrapolation from finitely many coordinates.
Until an exact identity `r(x)=0` is derived for a whole family, every newly
encountered adaptive coordinate must execute the same divisor test.  The
classifier is therefore algorithmic and transferable, not a node exception
list.

## Live adaptive test

- current unresolved descendants: `{result['input_unresolved_count']}`;
- certified: `{result['certified_count']}`;
- removable bounded-zero: `{result['removable_count']}`;
- stable material: `{result['material_count']}`;
- maximum removable residue envelope:
  `{result['maximum_removable_residue_envelope']:.12g}`;
- maximum material residue relative spread:
  `{result['maximum_material_residue_relative_spread']:.12g}`.

{family_lines}

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

Checkpoint 5330 certifies the preserved 30-pole E040 seed and provides the
reusable local divisor algorithm.  Evolving controller aggregates do not mutate
that source-bound seed, while every unseen coordinate still executes the full
divisor test.  It does not yet complete the
E040 integral, the seven-rung regulator-zero limit, the decay-angle integral,
the UV coefficient, local GR, or full MTS.  No future coordinate is classified
without running the divisor controls unless a separate exact family identity
is proved.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), default="dry-run")
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    if arguments.mode == "dry-run":
        value = dry_run()
    elif arguments.mode == "run":
        value = run()
    else:
        value = read_json(RESULT)
        validations = validate(value)
        write_csv(VALIDATION, validations)
        write_csv(RESIDUAL_VALIDATION, validations)
        value = {
            **value,
            "validation_all_passed": all(
                parse_bool(row["passed"]) for row in validations
            ),
        }
    print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
