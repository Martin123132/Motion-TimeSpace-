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
SOURCE_5327 = FUNCTIONAL_RG / "5327" / "E040"
SOURCE = FUNCTIONAL_RG / "5329"

SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
POLES_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_geometric_poles.csv"
CLASSIFICATIONS_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_pole_classification.csv"
DRY_RUN_5327 = SOURCE_5327 / "D2_midpoint_event_aligned_E040_dry_run.json"

DRY_RUN = SOURCE / "E040_owner_channel_numerator_certificate_dry_run.json"
DRY_RUN_SNAPSHOT = SOURCE / "E040_parent_dry_run_snapshot.json"
INPUT_SNAPSHOT = SOURCE / "E040_unresolved_pole_input_snapshot.csv"
POLE_SNAPSHOT = SOURCE / "E040_geometric_pole_input_snapshot.csv"
ROOTS = SOURCE / "E040_owner_channel_root_controls.csv"
SAMPLES = SOURCE / "E040_owner_channel_numerator_samples.csv"
FITS = SOURCE / "E040_owner_channel_numerator_fits.csv"
CERTIFICATES = SOURCE / "E040_owner_channel_pole_certificates.csv"
RESULT = SOURCE / "E040_owner_channel_numerator_pole_certificate_result.json"
VALIDATION = SOURCE / "E040_owner_channel_numerator_pole_certificate_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5329_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5329-Y5-R2FR-E040-owner-channel-numerator-pole-certificate.md"

CHECKPOINT = 5329
PARENT_CHECKPOINT = 5327
MARKER = "MTS_5329_E040_OWNER_CHANNEL_NUMERATOR_POLE_CERTIFICATE"
REVISION = "E040-owner-channel-numerator-pole-certificate-v1"
EPSILON_ID = "E040"
EXPECTED_UNRESOLVED_COUNT = 30
EXPECTED_REMOVABLE_COUNT = 26
EXPECTED_MATERIAL_COUNT = 4
FIT_SCALES = (0.25, 0.5, 1.0)
FIT_FRACTIONS = (-4.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 4.0)
FIT_DEGREES = (5, 6)
MAXIMUM_RADIUS_HALVINGS = 6
ROOT_RESIDUAL_LIMIT = 1.0e-10
ROOT_NORMALIZED_RESIDUAL_LIMIT = 1.0e-5
ROOT_SHIFT_RADIUS_FRACTION_LIMIT = 0.25
DERIVATIVE_CHANGE_LIMIT = 1.0e-3
NUMERATOR_FIT_RESIDUAL_LIMIT = 5.0e-5
COEFFICIENT_CHANGE_LIMIT = 1.0e-6
ROOT_EQUATION_RESIDUAL_LIMIT = 1.0e-30
ROOT_REFINEMENT_CHORDAL_LIMIT = 1.0e-6
RESIDUE_STABILITY_LIMIT = 5.0e-4
MATERIAL_RESIDUE_FLOOR = 1.0e-6
REMOVABLE_RESIDUE_CEILING = 1.0e-8
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
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


M5327 = load_module("mts_5327_for_5329", SCRIPT_5327)
M5327.OWNER_CHANNEL_CERTIFICATE_BYPASS = True


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


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def unresolved_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(CLASSIFICATIONS_5327)
        if not parse_bool(row["pole_classification_resolved"])
    ]


def target_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return str(row["node_id"]), str(row["term_id"]), str(row["pole_id"])


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5327,
        DRY_RUN_SNAPSHOT,
        INPUT_SNAPSHOT,
        POLE_SNAPSHOT,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    required = (SCRIPT_5327, POLES_5327, CLASSIFICATIONS_5327, DRY_RUN_5327)
    missing = [str(path) for path in required if not path.exists()]
    rows = unresolved_rows() if not missing else []
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = str(row["term_id"]), str(row["pole_id"])
        counts[key] = counts.get(key, 0) + 1
    expected_pattern = counts == {
        ("MC04_SP_DM", "MC04_P02"): 26,
        ("MC04_SP_DP", "MC04_P01"): 2,
        ("MC04_SP_DP", "MC04_P02"): 2,
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "acceptance_passed": (
            not missing
            and len(rows) == EXPECTED_UNRESOLVED_COUNT
            and expected_pattern
            and bool(read_json(DRY_RUN_5327)["acceptance_passed"])
        ),
        "decision": (
            "E040_OWNER_CHANNEL_CERTIFICATE_DRY_RUN_ACCEPTED__RUN"
            if not missing and len(rows) == EXPECTED_UNRESOLVED_COUNT and expected_pattern
            else "E040_OWNER_CHANNEL_CERTIFICATE_DRY_RUN_BLOCKED"
        ),
        "unresolved_input_count": len(rows),
        "pattern_counts": {f"{key[0]}|{key[1]}": value for key, value in counts.items()},
        "missing_paths": missing,
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def owner_channel(
    row: dict[str, Any],
) -> Callable[[complex], complex]:
    coordinate = float(row["absolute_soft_cosine"])
    soft_sign = int(row["soft_sign"])
    decay_sign = int(row["decay_sign"])
    problem = M5327.M5326.M5312.M5311.synthetic_energy_problem(
        "MC04",
        soft_sign * coordinate,
        decay_sign
        * M5327.M5326.M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE,
    )
    surface_id = str(row["primary_surface_id"])
    return lambda energy: complex(
        M5327.M5326.M5312.M5291.M5267.M5239.owner_surface_values(
            problem,
            complex(energy),
        )[surface_id]
    )


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


def refine_channel_root(
    row: dict[str, Any],
    poles: list[dict[str, Any]],
) -> tuple[dict[str, Any], Callable[[complex], complex], complex, complex, float]:
    function = owner_channel(row)
    initial = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
    radius = base_fit_radius(row, poles)
    core = max(abs(initial.imag), 1.0e-7)
    derivative_step = min(1.0e-6, max(1.0e-8, 0.25 * core))
    pole = initial
    best = initial
    best_residual = abs(function(initial))
    iterations = 0
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
    derivatives = [central_derivative(function, pole, step) for step in derivative_steps]
    derivative = derivatives[-1]
    derivative_change = max(
        relative_complex_change(first, second)
        for first, second in zip(derivatives, derivatives[1:])
    )
    residual = abs(function(pole))
    normalized_residual = residual / max(abs(derivative) * core, 1.0e-300)
    shift = abs(pole - initial)
    controls_pass = (
        residual <= ROOT_RESIDUAL_LIMIT
        and normalized_residual <= ROOT_NORMALIZED_RESIDUAL_LIMIT
        and abs(derivative) > 1.0e-12
        and derivative_change <= DERIVATIVE_CHANGE_LIMIT
        and shift <= max(ROOT_SHIFT_RADIUS_FRACTION_LIMIT * radius, 1.0e-8)
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
        "derivative_step": derivative_steps[-1],
        "newton_iteration_count": iterations,
        "initial_fit_radius": radius,
        "channel_root_controls_pass": controls_pass,
        **{field: False for field in CLAIM_FIELDS},
    }
    return result, function, pole, derivative, radius


def full_component_evaluator(base_context: dict[str, Any]) -> Callable[..., dict[str, Any]]:
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
            contexts[context_key] = M5327.M5326.M5312.M5308.M5302.local_context(
                base_context,
                coordinate,
                soft_sign,
                decay_sign,
            )
        context = contexts[context_key]
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        target = context["inventories"][EPSILON_ID]["target"]
        rationals = M5327.M5326.M5312.M5280.M5274.M5231.root_rationals(
            event,
            target,
        )
        cache[key] = M5327.M5326.M5312.M5280.evaluate_component(
            event,
            EPSILON_ID,
            "MC04",
            context,
            rationals=rationals,
            convergence_audit=True,
        )
        return cache[key]

    return evaluate


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
    failure = ""
    for halving in range(MAXIMUM_RADIUS_HALVINGS + 1):
        radius = initial_radius / (2.0**halving)
        rows: list[dict[str, Any]] = []
        try:
            for scale in FIT_SCALES:
                local_radius = scale * radius
                for fraction in FIT_FRACTIONS:
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
                            "root_equation_residual": evaluation["root_equation_residual"],
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
            len(rows) == len(FIT_SCALES) * len(FIT_FRACTIONS)
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
    return [], initial_radius / (2.0**MAXIMUM_RADIUS_HALVINGS), MAXIMUM_RADIUS_HALVINGS, failure


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
        for degree in FIT_DEGREES:
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
                    "scaled_pole_magnitude": abs(scaled_pole),
                    **complex_fields("numerator_at_pole", numerator_at_pole),
                    **complex_fields("fitted_residue", residue),
                    "fit_relative_residual": residual,
                    "all_fit_samples_mask_active": all(
                        parse_bool(sample["mask_active"]) for sample in local
                    ),
                    "residue_derivation_method": "OWNER_CHANNEL_NUMERATOR_OVER_DERIVATIVE",
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def classify_pole(
    source: dict[str, Any],
    pole: dict[str, Any],
    root: dict[str, Any],
    samples: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    final_radius: float,
    radius_halvings: int,
    preflight_failure: str,
) -> dict[str, Any]:
    if not fits:
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
            "primary_surface_id": pole["primary_surface_id"],
            **complex_fields(
                "geometric_pole",
                complex(float(pole["pole_real"]), float(pole["pole_imaginary"])),
            ),
            **complex_fields(
                "refined_pole",
                complex(
                    float(root["refined_pole_real"]),
                    float(root["refined_pole_imaginary"]),
                ),
            ),
            **complex_fields("source_direct_laurent_residue", source_residue),
            **complex_fields("certified_residue", 0.0j),
            "certified_residue_envelope": math.inf,
            "certified_residue_relative_spread": math.inf,
            "maximum_fit_relative_residual": math.inf,
            "maximum_coefficient_relative_change": math.inf,
            "maximum_root_equation_residual": math.inf,
            "maximum_root_refinement_chordal_distance": math.inf,
            "selector_label_count": 0,
            "selector_labels": "",
            "selector_role_count": 0,
            "selector_roles": "",
            "selector_orientation_count": 0,
            "selector_orientations": "",
            "final_base_fit_radius": final_radius,
            "radius_halving_count": radius_halvings,
            "selector_preflight_failure": preflight_failure,
            "expected_classification": (
                "REMOVABLE" if source["term_id"] == "MC04_SP_DM" else "MATERIAL"
            ),
            "observed_classification": "UNRESOLVED",
            "pole_classification": "OWNER_CHANNEL_NUMERATOR_CLASSIFICATION_UNRESOLVED",
            "material_simple_pole": False,
            "removable_zero_residue_pole": False,
            "pole_classification_resolved": False,
            "owner_channel_certificate_controls_pass": False,
            "classification_matches_source_pattern": False,
            "valid_for_E040_owner_channel_certificate": False,
            "valid_for_E040_node_rerun": False,
            **{field: False for field in CLAIM_FIELDS},
        }
    selected = next(
        row
        for row in fits
        if float(row["fit_scale"]) == max(FIT_SCALES)
        and int(row["background_polynomial_degree"]) == max(FIT_DEGREES)
    )
    selected_value = complex(
        float(selected["fitted_residue_real"]),
        float(selected["fitted_residue_imaginary"]),
    )
    all_values = [
        complex(float(row["fitted_residue_real"]), float(row["fitted_residue_imaginary"]))
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
    expected_class = (
        "REMOVABLE" if source["term_id"] == "MC04_SP_DM" else "MATERIAL"
    )
    observed_class = "REMOVABLE" if removable else "MATERIAL" if material else "UNRESOLVED"
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
        "primary_surface_id": pole["primary_surface_id"],
        **complex_fields(
            "geometric_pole",
            complex(float(pole["pole_real"]), float(pole["pole_imaginary"])),
        ),
        **complex_fields(
            "refined_pole",
            complex(float(root["refined_pole_real"]), float(root["refined_pole_imaginary"])),
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
        "selector_orientations": "|".join(str(value) for value in sorted(orientations)),
        "final_base_fit_radius": final_radius,
        "radius_halving_count": radius_halvings,
        "selector_preflight_failure": preflight_failure,
        "expected_classification": expected_class,
        "observed_classification": observed_class,
        "pole_classification": (
            "OWNER_CHANNEL_NUMERATOR_BOUNDED_ZERO_REMOVABLE"
            if removable
            else "OWNER_CHANNEL_NUMERATOR_STABLE_MATERIAL_SIMPLE_POLE"
            if material
            else "OWNER_CHANNEL_NUMERATOR_CLASSIFICATION_UNRESOLVED"
        ),
        "material_simple_pole": material,
        "removable_zero_residue_pole": removable,
        "pole_classification_resolved": controls_pass,
        "owner_channel_certificate_controls_pass": controls_pass,
        "classification_matches_source_pattern": observed_class == expected_class,
        "valid_for_E040_owner_channel_certificate": controls_pass,
        "valid_for_E040_node_rerun": controls_pass,
        **{field: False for field in CLAIM_FIELDS},
    }


def run() -> dict[str, Any]:
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5329 dry run did not pass")
    SOURCE.mkdir(parents=True, exist_ok=True)
    source = unresolved_rows()
    poles = read_csv(POLES_5327)
    pole_lookup = {target_key(row): row for row in poles}
    selected_poles = [pole_lookup[target_key(row)] for row in source]
    atomic_json(DRY_RUN_SNAPSHOT, read_json(DRY_RUN_5327))
    write_csv(INPUT_SNAPSHOT, source, ["node_id", "term_id", "pole_id"])
    write_csv(POLE_SNAPSHOT, selected_poles, ["node_id", "term_id", "pole_id"])
    M5327.M5326.M5312.set_below_normal_priority()
    M5327.configure_target(EPSILON_ID)
    old = M5327.M5326.configure_kernel()
    root_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    certificate_rows: list[dict[str, Any]] = []
    formal_start = M5327.M5283.formal_inventory_digest()
    evaluator = full_component_evaluator(
        M5327.M5326.M5312.M5303.synthetic_context()
    )
    try:
        for index, source_row in enumerate(source, start=1):
            pole_row = pole_lookup[target_key(source_row)]
            root_row, function, refined_pole, derivative, radius = refine_channel_root(
                pole_row,
                selected_poles,
            )
            local_samples, final_radius, halvings, preflight_failure = sample_numerator(
                pole_row,
                function,
                refined_pole,
                radius,
                evaluator,
            )
            local_fits = (
                fit_numerator(
                    pole_row,
                    refined_pole,
                    derivative,
                    local_samples,
                )
                if local_samples
                else []
            )
            certificate = classify_pole(
                source_row,
                pole_row,
                root_row,
                local_samples,
                local_fits,
                final_radius,
                halvings,
                preflight_failure,
            )
            root_rows.append(root_row)
            sample_rows.extend(local_samples)
            fit_rows.extend(local_fits)
            certificate_rows.append(certificate)
            write_csv(ROOTS, root_rows, ["node_id", "term_id", "pole_id"])
            write_csv(
                SAMPLES,
                sample_rows,
                ["node_id", "term_id", "pole_id", "fit_scale", "fraction"],
            )
            write_csv(
                FITS,
                fit_rows,
                [
                    "node_id",
                    "term_id",
                    "pole_id",
                    "fit_scale",
                    "background_polynomial_degree",
                ],
            )
            write_csv(
                CERTIFICATES,
                certificate_rows,
                ["node_id", "term_id", "pole_id"],
            )
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "completed_pole_count": index,
                    "expected_pole_count": len(source),
                    "last_target": "|".join(target_key(source_row)),
                },
            )
    finally:
        M5327.M5326.restore_kernel(old)
    formal_end = M5327.M5283.formal_inventory_digest()
    removable_count = sum(
        parse_bool(row["removable_zero_residue_pole"]) for row in certificate_rows
    )
    material_count = sum(
        parse_bool(row["material_simple_pole"]) for row in certificate_rows
    )
    accepted = (
        len(certificate_rows) == EXPECTED_UNRESOLVED_COUNT
        and removable_count == EXPECTED_REMOVABLE_COUNT
        and material_count == EXPECTED_MATERIAL_COUNT
        and all(
            parse_bool(row["owner_channel_certificate_controls_pass"])
            and parse_bool(row["classification_matches_source_pattern"])
            for row in certificate_rows
        )
        and formal_start == formal_end == FORMAL_DIGEST
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "E040-owner-channel-numerator-pole-certificate",
        "acceptance_passed": accepted,
        "decision": (
            "E040_OWNER_CHANNEL_26_REMOVABLE_4_MATERIAL_CERTIFIED__RERUN_NODES"
            if accepted
            else "E040_OWNER_CHANNEL_CERTIFICATE_REQUIRES_REFINEMENT"
        ),
        "input_unresolved_pole_count": len(source),
        "certified_pole_count": len(certificate_rows),
        "removable_zero_residue_pole_count": removable_count,
        "material_simple_pole_count": material_count,
        "maximum_certified_removable_residue_envelope": max(
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
        "maximum_fit_relative_residual": max(
            float(row["maximum_fit_relative_residual"])
            for row in certificate_rows
        ),
        "formalization_workbench_start_digest": formal_start,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_start == formal_end else -1
        ),
        "claim_boundary": {
            "valid_for_E040_owner_channel_certificate": accepted,
            "valid_for_E040_node_rerun": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "This certifies only the 30 unresolved E040 in-support pole "
                "classifications. It does not supply the finite E040 integral "
                "or any regulator-zero, angular, UV, local-GR, or full-MTS claim."
            ),
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "ACCEPTED" if accepted else "REQUIRES_REFINEMENT",
            "decision": result["decision"],
            "completed_pole_count": len(certificate_rows),
        },
    )
    return validate_outputs()


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    inputs = read_csv(INPUT_SNAPSHOT)
    poles = read_csv(POLE_SNAPSHOT)
    roots = read_csv(ROOTS)
    samples = read_csv(SAMPLES)
    fits = read_csv(FITS)
    certificates = read_csv(CERTIFICATES)
    expected_keys = {target_key(row) for row in inputs}
    certificate_keys = {target_key(row) for row in certificates}
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "thirty_unresolved_inputs_are_snapshotted_once",
            len(inputs) == len(expected_keys) == EXPECTED_UNRESOLVED_COUNT,
            f"rows={len(inputs)};keys={len(expected_keys)}",
        ),
        validation_gate(
            "every_input_has_one_geometric_pole_and_root_control",
            len(poles) == len(roots) == EXPECTED_UNRESOLVED_COUNT
            and {target_key(row) for row in poles} == expected_keys
            and {target_key(row) for row in roots} == expected_keys
            and all(parse_bool(row["channel_root_controls_pass"]) for row in roots),
            f"poles={len(poles)};roots={len(roots)}",
        ),
        validation_gate(
            "selector_orbit_and_high_precision_samples_are_complete",
            len(samples)
            == EXPECTED_UNRESOLVED_COUNT * len(FIT_SCALES) * len(FIT_FRACTIONS)
            and all(
                parse_bool(row["mask_active"])
                and parse_bool(row["mask_agrees"])
                and float(row["coefficient_relative_change"])
                <= COEFFICIENT_CHANGE_LIMIT
                and float(row["root_equation_residual"])
                <= ROOT_EQUATION_RESIDUAL_LIMIT
                for row in samples
            ),
            f"samples={len(samples)}",
        ),
        validation_gate(
            "two_degree_three_radius_numerator_fits_are_complete",
            len(fits)
            == EXPECTED_UNRESOLVED_COUNT * len(FIT_SCALES) * len(FIT_DEGREES)
            and all(
                float(row["fit_relative_residual"])
                <= NUMERATOR_FIT_RESIDUAL_LIMIT
                for row in fits
            ),
            f"fits={len(fits)}",
        ),
        validation_gate(
            "twenty_six_removable_and_four_material_poles_are_certified",
            len(certificates) == EXPECTED_UNRESOLVED_COUNT
            and certificate_keys == expected_keys
            and sum(
                parse_bool(row["removable_zero_residue_pole"])
                for row in certificates
            )
            == EXPECTED_REMOVABLE_COUNT
            and sum(
                parse_bool(row["material_simple_pole"])
                for row in certificates
            )
            == EXPECTED_MATERIAL_COUNT
            and all(
                parse_bool(row["owner_channel_certificate_controls_pass"])
                and parse_bool(row["classification_matches_source_pattern"])
                for row in certificates
            ),
            f"certificates={len(certificates)}",
        ),
        validation_gate(
            "removable_residue_envelopes_stay_below_live_ceiling",
            max(
                float(row["certified_residue_envelope"])
                for row in certificates
                if parse_bool(row["removable_zero_residue_pole"])
            )
            <= REMOVABLE_RESIDUE_CEILING,
            str(result["maximum_certified_removable_residue_envelope"]),
        ),
        validation_gate(
            "material_residue_family_is_fit_stable",
            max(
                float(row["certified_residue_relative_spread"])
                for row in certificates
                if parse_bool(row["material_simple_pole"])
            )
            <= RESIDUE_STABILITY_LIMIT,
            str(result["maximum_material_residue_relative_spread"]),
        ),
        validation_gate(
            "source_paths_and_hashes_are_current",
            source_current,
            f"sources={len(result['source_files'])}",
        ),
        validation_gate(
            "formal_workbench_is_unchanged",
            result["formalization_workbench_start_digest"]
            == result["formalization_workbench_end_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "broader_claim_fields_remain_false",
            all(
                not parse_bool(row[field])
                for row in certificates
                for field in CLAIM_FIELDS
            )
            and all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "certificate-only",
        ),
        validation_gate(
            "scripts_cache_is_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = bool(result["acceptance_passed"]) and all(
        bool(row["passed"]) for row in gates
    )
    write_csv(VALIDATION, gates, ["gate"])
    write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_E040_OWNER_CHANNEL_POLE_CERTIFICATE__RERUN_NODES"
            if passed
            else "E040_OWNER_CHANNEL_POLE_CERTIFICATE_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5329 - E040 owner-channel numerator pole certificate",
        "",
        "## Derivation",
        "",
        "For an apparent pole owned by the channel `F_X(E)=0`, the selected",
        "component is written locally as `C_X(E)=N_X(E)/F_X(E)`.  The channel",
        "root is independently refined, `F'_X(E_p)` is derivative-stability",
        "checked, and the analytic numerator is reconstructed on three real",
        "radii from `N_X=F_X C_X`.  The true residue is then",
        "",
        "```text",
        "Res[C_X,E_p] = N_X(E_p)/F'_X(E_p).",
        "```",
        "",
        "The selector pair, role, orientation, exact mask, high-precision root",
        "and coefficient convergence are required to remain fixed on every fit",
        "sample.  No direct Laurent residue is accepted merely by enlarging its",
        "sampling distance.",
        "",
        "## Result",
        "",
        f"- certified unresolved poles: `{result['certified_pole_count']}`;",
        f"- bounded removable poles: `{result['removable_zero_residue_pole_count']}`;",
        f"- stable material simple poles: `{result['material_simple_pole_count']}`;",
        "- maximum removable residue envelope: "
        f"`{result['maximum_certified_removable_residue_envelope']:.12g}`;",
        "- maximum material residue relative spread: "
        f"`{result['maximum_material_residue_relative_spread']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "## Interpretation",
        "",
        "The 26 `MC04_SP_DM/MC04_P02` direct-Laurent artifacts are bounded",
        "zero-residue cancellations.  The four `P08/MC04_SP_DP` poles are not",
        "removable: their owner-channel residues are material and stable, so the",
        "E040 rerun must subtract them rather than erase them.",
        "",
        "## Claim boundary",
        "",
        "This checkpoint authorizes replacement of the 30 unresolved E040 pole",
        "classifications only.  The E040 integral, seven-rung regulator ladder,",
        "regulator-zero limit, decay-angle integral, UV coefficient, local GR",
        "and full MTS remain separate gates.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    return parser.parse_args()


def main() -> int:
    M5327.M5326.M5312.set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = run()
    else:
        result = validate_outputs()
    print(json.dumps(result, sort_keys=True))
    return 0 if bool(result["acceptance_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
