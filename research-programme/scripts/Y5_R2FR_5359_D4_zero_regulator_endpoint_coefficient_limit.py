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
OUTPUT = FUNCTIONAL_RG / "5359"
DOCUMENT = POST / "5359-Y5-R2FR-D4-zero-regulator-endpoint-coefficient-limit.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5359_VALIDATION.csv"

SCRIPT_5342 = SCRIPTS / "Y5_R2FR_5342_D4_E00125_generic_support_endpoint_normal_form.py"
SCRIPT_5357 = SCRIPTS / "Y5_R2FR_5357_D4_six_regulator_coefficient_taylor_gate.py"
SCRIPT_5358 = SCRIPTS / "Y5_R2FR_5358_D4_zero_regulator_analytic_collision_and_event_continuation.py"
RESULT_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_result.json"
VALIDATION_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_validation.csv"
INPUTS_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_inputs.csv"
ENVELOPE_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_intercept_envelope.csv"
RESULT_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
VALIDATION_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_validation.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
SUPPORT_E000625 = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "support"
    / "D4_E000625_support_endpoint_coefficients.csv"
)
BRANCH_E000625 = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "all-eight"
    / "D4_E000625_one_sided_branch_endpoint_coefficients.csv"
)
LEDGER_E000625 = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "all-eight"
    / "D4_E000625_all_eight_endpoint_coefficient_ledger.csv"
)

CHECKPOINT = 5359
MARKER = "MTS_5359_D4_ZERO_REGULATOR_ENDPOINT_COEFFICIENT_LIMIT"
REVISION = "D4-zero-regulator-endpoint-coefficient-limit-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
MP_DIGITS = 110
Q_ZERO_TEXT = "-1.25"
Q_EPSILON_DERIVATIVE_TEXT = "-0.03125j"
RESIDUE_INITIAL_STEP = "1e-6"
RESIDUE_LEVELS = 10
RESIDUE_INTERPOLATION_ORDER = 5
GLOBAL_COEFFICIENT_EXPONENT = 30
GLOBAL_COEFFICIENT_CROSSCHECK_EXPONENT = 24
GLOBAL_COEFFICIENT_PHASE = "0.37"
GLOBAL_COEFFICIENT_CROSSCHECK_PHASE = "1.11"
RESIDUE_RADIUS_SAFETY_FACTOR = 8
RESIDUE_RELATIVE_RADIUS_LIMIT = 2.0e-7
FINITE_C0_RELATIVE_LIMIT = 5.0e-4
FINITE_A_RELATIVE_LIMIT = 2.0e-3
FINITE_GAP_SLOPE_RELATIVE_LIMIT = 5.0e-4
FINITE_GAP_DERIVATIVE_RELATIVE_LIMIT = 5.0e-4

CLAIM_RESIDUE = "valid_for_D4_zero_regulator_parent_residue_evaluation"
CLAIM_ENDPOINTS = "valid_for_D4_zero_regulator_eight_endpoint_coefficients"
CLAIM_LIMIT = "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
FALSE_CLAIMS = (
    "valid_for_D4_integral_six_rung_complete_second_order_fit",
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
    specification.loader.exec_module(module)
    return module


M5358 = load_module("mts_5358_for_5359", SCRIPT_5358)
M5342 = load_module("mts_5342_for_5359", SCRIPT_5342)
AMP = M5342.M5312.M5280.M5275.M5040_MP
mp = AMP.mp


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def mp_text(value: Any, digits: int = 40) -> str:
    return mp.nstr(value, digits)


def complex_fields(prefix: str, value: Any) -> dict[str, str]:
    return {
        f"{prefix}_real": mp_text(mp.re(value)),
        f"{prefix}_imaginary": mp_text(mp.im(value)),
        f"{prefix}_magnitude": mp_text(abs(value)),
    }


def finite_complex(value: Any) -> bool:
    return math.isfinite(float(mp.re(value))) and math.isfinite(float(mp.im(value)))


def relative_difference(first: Any, second: Any) -> float:
    return float(abs(first - second) / max(abs(first), abs(second), mp.mpf("1e-300")))


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def no_downstream_claims() -> dict[str, bool]:
    return {claim: False for claim in FALSE_CLAIMS}


def source_paths() -> list[Path]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5342,
        SCRIPT_5357,
        SCRIPT_5358,
        Path(M5342.M5312.M5280.__file__).resolve(),
        Path(M5342.M5312.M5280.M5275.__file__).resolve(),
        Path(M5342.M5312.M5280.M5277.__file__).resolve(),
        Path(AMP.__file__).resolve(),
        Path(M5342.M5312.M5309.__file__).resolve(),
        Path(M5342.M5312.M5309.M5301.M5300.M5292.__file__).resolve(),
        Path(M5342.M5312.M5309.M5301.M5300.M5292.M5283.TOTALS_5281).resolve(),
        M5358.DECAY_NODES.resolve(),
        RESULT_5357,
        VALIDATION_5357,
        INPUTS_5357,
        ENVELOPE_5357,
        RESULT_5358,
        VALIDATION_5358,
        EVENTS_5358,
        SUPPORT_E000625,
        BRANCH_E000625,
        LEDGER_E000625,
    ]
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def source_rows(paths: list[Path]) -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "sha256": digest(path),
            "exists": True,
            CLAIM_RESIDUE: False,
            CLAIM_ENDPOINTS: False,
            CLAIM_LIMIT: False,
            **no_downstream_claims(),
        }
        for path in paths
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    missing = [str(path) for path in paths if not path.is_file()]
    result_5357 = read_json(RESULT_5357)
    result_5358 = read_json(RESULT_5358)
    validation_5357 = read_csv(VALIDATION_5357)
    validation_5358 = read_csv(VALIDATION_5358)
    events = read_csv(EVENTS_5358)
    support = read_csv(SUPPORT_E000625)
    branch = read_csv(BRANCH_E000625)
    ledger = read_csv(LEDGER_E000625)
    checks = {
        "all_direct_sources_exist": not missing,
        "checkpoint_5358_validation_passes": result_5358.get("validation_passed") is True
        and all(parse_bool(row.get("passed")) for row in validation_5358),
        "checkpoint_5358_geometry_claims_pass": all(
            result_5358.get("claim_boundary", {}).get(claim) is True
            for claim in (
                M5358.CLAIM_COLLISION,
                M5358.CLAIM_EVENTS,
                M5358.CLAIM_CONTINUATION,
            )
        ),
        "checkpoint_5357_stability_passes_but_limit_is_open": result_5357.get(
            "validation_passed"
        )
        is True
        and result_5357.get("claim_boundary", {}).get(
            "valid_for_D4_six_regulator_quadratic_endpoint_coefficient_stability"
        )
        is True
        and result_5357.get("claim_boundary", {}).get(CLAIM_LIMIT) is False
        and all(parse_bool(row.get("passed")) for row in validation_5357),
        "exactly_eight_ordered_zero_events": [row.get("event_id") for row in events]
        == list(EVENT_IDS),
        "smallest_rung_reference_partition_is_complete": sorted(
            [row.get("event_id") for row in support]
            + [row.get("event_id") for row in branch]
        )
        == sorted(EVENT_IDS),
        "smallest_rung_ledger_is_complete": [row.get("event_id") for row in ledger]
        == list(EVENT_IDS),
        "formal_workbench_inventory_is_unchanged": M5342.M5283.formal_inventory_digest()
        == M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "D4-zero-regulator-endpoint-coefficient-preflight",
        "checks": checks,
        "missing_paths": missing,
        "source_count": len(paths),
        "all_pass": all(checks.values()),
    }


def polynomial_intercept(points: list[tuple[Any, Any]]) -> Any:
    total = mp.mpc(0)
    for index, (x_value, y_value) in enumerate(points):
        weight = mp.mpf(1)
        for other_index, (other_x, _) in enumerate(points):
            if other_index == index:
                continue
            weight *= -other_x / (x_value - other_x)
        total += weight * y_value
    return total


def positive_regulator_global_root(direction: list[Any], label: str) -> Any:
    external_stereographic = -1j * mp.sqrt(5) / 2
    holomorphic = (direction[0] + 1j * direction[1]) / (1 + direction[2])
    antiholomorphic = (direction[0] - 1j * direction[1]) / (1 + direction[2])
    roots = {
        "plus_u": external_stereographic / holomorphic,
        "plus_v": antiholomorphic / external_stereographic,
        "minus_u": -1 / (external_stereographic * holomorphic),
        "minus_v": -external_stereographic * antiholomorphic,
    }
    return roots[label]


def representative_relative_root(energy: Any, soft_cosine: Any, decay_cosine: Any) -> Any:
    q_value = mp.mpf(Q_ZERO_TEXT)
    recoil = mp.sqrt(1 - energy)
    soft_sine = mp.sqrt(1 - soft_cosine**2)
    decay_sine = mp.sqrt(1 - decay_cosine**2)
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    return (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )


def event_configuration(
    event: dict[str, str],
    references: dict[str, dict[str, str]],
) -> dict[str, Any]:
    sign, decay_sign = M5358.term_signs(event["term_id"])
    if sign != decay_sign:
        raise RuntimeError(f"unequal D4 signs at {event['event_id']}")
    reference = references[event["event_id"]]
    reciprocal = event["term_id"] == "MC04_SM_DM"
    role = "reciprocal" if reciprocal else "representative"
    labels = (
        ("direct:g1:minus_v", "direct:g3:plus_v")
        if reciprocal
        else ("direct:g1:minus_u", "direct:g3:plus_u")
    )
    root_labels = tuple(label.rsplit(":", 1)[1] for label in labels)
    return {
        "event": event,
        "reference": reference,
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "term_id": event["term_id"],
        "surface_id": event["primary_surface_id"],
        "sign": sign,
        "soft_cosine": sign * mp.mpf(event["zero_regulator_absolute_soft_cosine"]),
        "decay_cosine": sign * mp.mpf(str(M5358.d4_decay_absolute())),
        "energy": mp.mpf(event["zero_regulator_soft_energy"]),
        "recoil": mp.mpf(event["zero_regulator_recoil_R"]),
        "role": role,
        "labels": labels,
        "root_labels": root_labels,
        "energy_approach_sign": 1 if event["event_type"] != "BRANCH_DEATH" else -1,
        "inside_coordinate_direction_sign": int(
            reference.get("inside_coordinate_direction_sign") or 0
        ),
        "log_sign": int(reference["log_sign"]),
        "contact_boundary": reference["contact_boundary"],
    }


def parent_relative_residue(
    configuration: dict[str, Any],
    energy: Any,
    component: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
    exponent: int,
    phase_value: Any,
) -> dict[str, Any]:
    soft_cosine = configuration["soft_cosine"]
    decay_cosine = configuration["decay_cosine"]
    representative_root = representative_relative_root(
        energy, soft_cosine, decay_cosine
    )
    relative_root = (
        1 / representative_root
        if configuration["role"] == "reciprocal"
        else representative_root
    )
    root_labels = configuration["root_labels"]

    def collision_roots(varied_relative_root: Any) -> tuple[Any, Any]:
        _, _, local_internal = AMP.event_geometry(
            energy,
            soft_cosine,
            decay_cosine,
            varied_relative_root,
        )
        directions = [
            [local_internal[index][component] / local_internal[index][0] for component in range(1, 4)]
            for index in (0, 2)
        ]
        return (
            positive_regulator_global_root(directions[0], root_labels[0]),
            positive_regulator_global_root(directions[1], root_labels[1]),
        )

    soft_direction, decay_direction, internal = AMP.event_geometry(
        energy,
        soft_cosine,
        decay_cosine,
        relative_root,
    )
    roots = collision_roots(relative_root)
    global_root = (roots[0] + roots[1]) / 2
    collision_jacobian = mp.diff(
        lambda value: collision_roots(value)[0] - collision_roots(value)[1],
        relative_root,
    )
    displacement = (
        mp.power(10, -exponent)
        * max(mp.mpf(1), abs(global_root))
        * mp.exp(1j * phase_value)
    )
    direct, subtraction = AMP.finite_plus_components(
        internal,
        energy,
        soft_direction,
        decay_direction,
        mp.mpc(-9, 0),
        global_root + displacement,
    )
    global_double_pole_coefficient = (direct + subtraction) * displacement**2
    event_point = {
        "soft_energy": float(energy),
        "soft_cosine": float(soft_cosine),
        "decay_cosine": float(decay_cosine),
    }
    mask_active, orientation, _, _ = M5342.M5312.M5280.M5277.exact_mask_orientation(
        configuration["labels"], event_point, surfaces
    )
    winding_delta = M5342.M5312.M5280.M5277.source_winding_delta(
        component, configuration["role"]
    )
    residue = (
        winding_delta
        * orientation
        * global_double_pole_coefficient
        / (relative_root * global_root * collision_jacobian)
    )
    return {
        "relative_root": relative_root,
        "global_root": global_root,
        "root_difference": roots[0] - roots[1],
        "collision_jacobian": collision_jacobian,
        "global_double_pole_coefficient": global_double_pole_coefficient,
        "residue": residue,
        "mask_active": bool(mask_active),
        "orientation": int(orientation),
        "winding_delta": int(winding_delta),
    }


def parent_energy_residue(
    configuration: dict[str, Any],
    component: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
    physical_multiplier: Any,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    initial_step = mp.mpf(RESIDUE_INITIAL_STEP)
    sequence_rows: list[dict[str, Any]] = []
    points: list[tuple[Any, Any]] = []
    states: list[dict[str, Any]] = []
    for level in range(RESIDUE_LEVELS):
        step = initial_step / mp.power(2, level)
        delta_energy = configuration["energy_approach_sign"] * step
        energy = configuration["energy"] + delta_energy
        state = parent_relative_residue(
            configuration,
            energy,
            component,
            surfaces,
            GLOBAL_COEFFICIENT_EXPONENT,
            mp.mpf(GLOBAL_COEFFICIENT_PHASE),
        )
        estimator = physical_multiplier * delta_energy * state["residue"]
        points.append((step, estimator))
        states.append(state)
        sequence_rows.append(
            {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "evaluation_class": "MAIN_ZERO_REGULATOR_LAURENT_SEQUENCE",
                "level": level,
                "positive_step_h": mp_text(step),
                "signed_energy_displacement": mp_text(delta_energy),
                "sample_energy": mp_text(energy),
                "selected_role": configuration["role"],
                "selected_labels": "|".join(configuration["labels"]),
                "global_coefficient_exponent": GLOBAL_COEFFICIENT_EXPONENT,
                "global_coefficient_phase": GLOBAL_COEFFICIENT_PHASE,
                "mask_active": state["mask_active"],
                "orientation": state["orientation"],
                "winding_delta": state["winding_delta"],
                **complex_fields("relative_root", state["relative_root"]),
                **complex_fields("global_root", state["global_root"]),
                **complex_fields("collision_root_difference", state["root_difference"]),
                **complex_fields("collision_jacobian", state["collision_jacobian"]),
                **complex_fields(
                    "global_double_pole_coefficient",
                    state["global_double_pole_coefficient"],
                ),
                **complex_fields("unscaled_parent_energy_function", state["residue"]),
                **complex_fields("physical_C0_step_estimator", estimator),
            }
        )

    order = RESIDUE_INTERPOLATION_ORDER
    selected = polynomial_intercept(points[-order:])
    previous_window = polynomial_intercept(points[-order - 1 : -1])
    lower_order = polynomial_intercept(points[-(order - 1) :])
    higher_order = polynomial_intercept(points[-(order + 1) :])
    final_step = points[-1][0]
    final_delta = configuration["energy_approach_sign"] * final_step
    final_energy = configuration["energy"] + final_delta
    exponent_state = parent_relative_residue(
        configuration,
        final_energy,
        component,
        surfaces,
        GLOBAL_COEFFICIENT_CROSSCHECK_EXPONENT,
        mp.mpf(GLOBAL_COEFFICIENT_PHASE),
    )
    exponent_estimator = (
        physical_multiplier * final_delta * exponent_state["residue"]
    )
    phase_state = parent_relative_residue(
        configuration,
        final_energy,
        component,
        surfaces,
        GLOBAL_COEFFICIENT_EXPONENT,
        mp.mpf(GLOBAL_COEFFICIENT_CROSSCHECK_PHASE),
    )
    phase_estimator = physical_multiplier * final_delta * phase_state["residue"]
    final_raw = points[-1][1]
    error_components = {
        "successive_window_shift": abs(selected - previous_window),
        "lower_order_shift": abs(selected - lower_order),
        "higher_order_shift": abs(selected - higher_order),
        "global_coefficient_exponent_shift": abs(final_raw - exponent_estimator),
        "global_coefficient_phase_shift": abs(final_raw - phase_estimator),
    }
    radius = RESIDUE_RADIUS_SAFETY_FACTOR * max(
        *error_components.values(),
        mp.mpf("1e-80"),
    )
    sequence_rows.extend(
        [
            {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "evaluation_class": "GLOBAL_COEFFICIENT_EXPONENT_CROSSCHECK",
                "level": RESIDUE_LEVELS - 1,
                "positive_step_h": mp_text(final_step),
                "signed_energy_displacement": mp_text(final_delta),
                "sample_energy": mp_text(final_energy),
                "selected_role": configuration["role"],
                "selected_labels": "|".join(configuration["labels"]),
                "global_coefficient_exponent": GLOBAL_COEFFICIENT_CROSSCHECK_EXPONENT,
                "global_coefficient_phase": GLOBAL_COEFFICIENT_PHASE,
                "mask_active": exponent_state["mask_active"],
                "orientation": exponent_state["orientation"],
                "winding_delta": exponent_state["winding_delta"],
                **complex_fields("physical_C0_step_estimator", exponent_estimator),
            },
            {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "evaluation_class": "GLOBAL_COEFFICIENT_PHASE_CROSSCHECK",
                "level": RESIDUE_LEVELS - 1,
                "positive_step_h": mp_text(final_step),
                "signed_energy_displacement": mp_text(final_delta),
                "sample_energy": mp_text(final_energy),
                "selected_role": configuration["role"],
                "selected_labels": "|".join(configuration["labels"]),
                "global_coefficient_exponent": GLOBAL_COEFFICIENT_EXPONENT,
                "global_coefficient_phase": GLOBAL_COEFFICIENT_CROSSCHECK_PHASE,
                "mask_active": phase_state["mask_active"],
                "orientation": phase_state["orientation"],
                "winding_delta": phase_state["winding_delta"],
                **complex_fields("physical_C0_step_estimator", phase_estimator),
            },
        ]
    )
    return sequence_rows, {
        "C0": selected,
        "C0_radius": radius,
        "C0_relative_radius": float(radius / max(abs(selected), mp.mpf("1e-300"))),
        "selected_intercept": selected,
        "previous_window_intercept": previous_window,
        "lower_order_intercept": lower_order,
        "higher_order_intercept": higher_order,
        "error_components": error_components,
        "minimum_collision_jacobian": min(abs(state["collision_jacobian"]) for state in states),
        "maximum_collision_root_difference": max(abs(state["root_difference"]) for state in states),
        "all_masks_active": all(state["mask_active"] for state in states),
        "orientations": sorted({state["orientation"] for state in states}),
        "windings": sorted({state["winding_delta"] for state in states}),
    }


def local_geometric_factors(configuration: dict[str, Any]) -> dict[str, Any]:
    q_value = mp.mpf(Q_ZERO_TEXT)
    q_epsilon_derivative = -1j / 32
    recoil = configuration["recoil"]
    soft_cosine = configuration["soft_cosine"]
    decay_cosine = configuration["decay_cosine"]
    surface_id = configuration["surface_id"]
    sign = configuration["sign"]
    partial_p_r = mp.diff(
        lambda value: M5358.material_polynomial(
            surface_id, value, soft_cosine, decay_cosine, q_value
        ),
        recoil,
    )
    partial_p_c = mp.diff(
        lambda value: M5358.material_polynomial(
            surface_id, recoil, value, decay_cosine, q_value
        ),
        soft_cosine,
    )
    partial_p_q = mp.diff(
        lambda value: M5358.material_polynomial(
            surface_id, recoil, soft_cosine, decay_cosine, value
        ),
        q_value,
    )
    recoil_epsilon_derivative = -partial_p_q * q_epsilon_derivative / partial_p_r
    boundary_gap_epsilon_derivative = 2 * recoil * recoil_epsilon_derivative
    material_recoil_x_derivative = -sign * partial_p_c / partial_p_r
    material_energy_x_derivative = -2 * recoil * material_recoil_x_derivative
    if configuration["event_type"] == "BRANCH_DEATH":
        boundary_energy_x_derivative = mp.mpf(0)
        boundary_gap_x_derivative = -material_energy_x_derivative
        boundary_gap_parameter_derivative = (
            configuration["inside_coordinate_direction_sign"]
            * boundary_gap_x_derivative
        )
        support_margin_slope = boundary_gap_x_derivative
    else:
        hard_partial_r = mp.diff(
            lambda value: M5358.hard_boundary_value(
                value, soft_cosine, decay_cosine
            ),
            recoil,
        )
        hard_partial_c = mp.diff(
            lambda value: M5358.hard_boundary_value(
                recoil, value, decay_cosine
            ),
            soft_cosine,
        )
        hard_recoil_x_derivative = -sign * hard_partial_c / hard_partial_r
        boundary_energy_x_derivative = -2 * recoil * hard_recoil_x_derivative
        boundary_gap_x_derivative = (
            boundary_energy_x_derivative - material_energy_x_derivative
        )
        boundary_gap_parameter_derivative = boundary_gap_x_derivative
        support_margin_slope = -boundary_gap_x_derivative
    return {
        "partial_p_r": partial_p_r,
        "partial_p_c": partial_p_c,
        "partial_p_q": partial_p_q,
        "q_epsilon_derivative": q_epsilon_derivative,
        "recoil_epsilon_derivative": recoil_epsilon_derivative,
        "boundary_gap_epsilon_derivative": boundary_gap_epsilon_derivative,
        "material_recoil_x_derivative": material_recoil_x_derivative,
        "material_energy_x_derivative": material_energy_x_derivative,
        "boundary_energy_x_derivative": boundary_energy_x_derivative,
        "boundary_gap_x_derivative": boundary_gap_x_derivative,
        "boundary_gap_parameter_derivative": boundary_gap_parameter_derivative,
        "support_margin_slope": support_margin_slope,
    }


def contract_rows() -> list[dict[str, Any]]:
    common = {CLAIM_LIMIT: False, **no_downstream_claims()}
    return [
        {
            "contract_id": "EC5359_01_positive_regulator_branch",
            "source_statement": "t=-9+i*epsilon and q=(1-t)/(1+t)",
            "derived_statement": "q(0)=-5/4, q'(0)=-i/32, and the epsilon>0 square-root continuation is w(0)=-i*sqrt(5)/2",
            "status": "DERIVED",
            **common,
        },
        {
            "contract_id": "EC5359_02_even_real_event_map",
            "source_statement": "the real support event is invariant under epsilon -> -epsilon followed by complex conjugation",
            "derived_statement": "x_e(epsilon)=x_e(0)+O(epsilon^2), so neither the real event coordinate nor real support boundary contributes linearly to z0",
            "status": "DERIVED_BY_CONJUGATION_SYMMETRY",
            **common,
        },
        {
            "contract_id": "EC5359_03_gap_regulator_derivative",
            "source_statement": "P_j(R,c,d,q)=0 and z0=E_boundary-(1-R^2)",
            "derived_statement": "a_e=z0'(0)=2*R*R_epsilon=i*R*P_q/(16*P_R)",
            "status": "DERIVED",
            **common,
        },
        {
            "contract_id": "EC5359_04_gap_coordinate_derivative",
            "source_statement": "z1 is the derivative of boundary energy minus material-pole energy in the endpoint trace coordinate",
            "derived_statement": "support contacts use dz/dx; branch deaths use (dx/dd_in)*dz/dx with the source-owned inward direction",
            "status": "DERIVED",
            **common,
        },
        {
            "contract_id": "EC5359_05_parent_energy_residue",
            "source_statement": "the parent relative-azimuth residue is Delta_w*orientation*K/(y*z*J), where K=lim[(zeta-z)^2(F_direct+F_sub)]",
            "derived_statement": "C0_e=M_phys*Res_{E=E_e}[Delta_w*orientation*K/(y*z*J)] evaluated directly at epsilon=0 on the positive-regulator branch",
            "status": "DERIVED_PARENT_LAURENT_LIMIT",
            **common,
        },
        {
            "contract_id": "EC5359_06_endpoint_coefficient",
            "source_statement": "A_e(epsilon)=-s_e*C0_e(epsilon)*z0_e(epsilon)/(epsilon*z1_e(epsilon))",
            "derived_statement": "A_e(0)=-s_e*C0_e(0)*a_e/z1_e(0)",
            "status": "DERIVED_IF_NUMERIC_LAURENT_CERTIFICATE_PASSES",
            **common,
        },
        {
            "contract_id": "EC5359_07_claim_boundary",
            "source_statement": "the endpoint coefficient is one local term in the fixed-decay D4 outer-regulator asymptotic",
            "derived_statement": "closing A_total(0) does not by itself close the integrated D4 regulator-zero limit or any GR/MTS claim",
            "status": "DOWNSTREAM_CLAIMS_STAY_FALSE",
            **common,
        },
    ]


def reference_rows() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    coefficient_rows = read_csv(SUPPORT_E000625) + read_csv(BRANCH_E000625)
    coefficients = {row["event_id"]: row for row in coefficient_rows}
    ledger = {row["event_id"]: row for row in read_csv(LEDGER_E000625)}
    return coefficients, ledger


def render_document(result: dict[str, Any], endpoint_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 5359 - D4 zero-regulator endpoint coefficient limit",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Exact local reduction",
        "",
        "The positive-regulator target branch has",
        "",
        "`q(0)=-5/4`, `q'(0)=-i/32`, `w(0)=-i sqrt(5)/2`.",
        "",
        "Conjugation symmetry makes the real event map even in the regulator.  For each material polynomial `P_j(R,c,d,q)=0`,",
        "",
        "`a_e = z0'_e(0) = i R_e (partial_q P_j)/(16 partial_R P_j)`.",
        "",
        "The endpoint-coordinate derivative `z1_e(0)` is obtained from the exact hard-boundary and material-pole derivatives proved in checkpoint 5358.  No finite-regulator fit supplies either local factor.",
        "",
        "## Parent residue",
        "",
        "The remaining factor is evaluated as the parent Laurent coefficient",
        "",
        "`C0_e(0)=M_phys Res_{E=E_e}[Delta_w o_e K_e/(y_e z_e J_e)]`,",
        "",
        "with `K_e=lim_(zeta->z_e) (zeta-z_e)^2(F_direct+F_sub)`.  Reciprocal `SM/DM` events use `y=1/y_-` and the `v` labels; representative `SP/DP` events use `y=y_-` and the `u` labels.  This also handles the two desingularized `s14` collision events without reinstating a simple-root axiom.",
        "",
        "## Eight limits",
        "",
        "| event | C0(0) | a=z0'(0) | z1(0) | A_e(0) | radius |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in endpoint_rows:
        lines.append(
            f"| {row['event_id']} | {row['C0_zero_real']} | {row['boundary_gap_epsilon_derivative_imaginary']} i | {row['boundary_gap_parameter_derivative_real']} | {row['A_event_zero_imaginary']} i | {row['A_event_zero_disk_radius']} |"
        )
    lines.extend(
        [
            "",
            "## Sum and independent ladder check",
            "",
            f"- Direct zero-regulator sum: `{result['A_total_zero_real']} + {result['A_total_zero_imaginary']} i`.",
            f"- Direct disk radius: `{result['A_total_zero_disk_radius']}`.",
            f"- Checkpoint 5357 extrapolated intercept: `{result['ladder_intercept_real']} + {result['ladder_intercept_imaginary']} i`.",
            f"- Direct-to-ladder distance: `{result['direct_to_ladder_distance']}` against the frozen ladder envelope `{result['ladder_envelope_radius']}`.",
            "",
            "The direct result is purely imaginary to its numerical certificate.  The small real intercept in the six-rung fit is therefore a finite-rung/extrapolation artifact, not a new parent coefficient.",
            "",
            "## Claim boundary",
            "",
            f"- `{CLAIM_RESIDUE}`: `{result['claim_boundary'][CLAIM_RESIDUE]}`.",
            f"- `{CLAIM_ENDPOINTS}`: `{result['claim_boundary'][CLAIM_ENDPOINTS]}`.",
            f"- `{CLAIM_LIMIT}`: `{result['claim_boundary'][CLAIM_LIMIT]}`.",
            "- Integrated D4, outer-regulator, angular, phase-space, local-GR and full-MTS claims remain false.",
            "",
            "## Next obstruction",
            "",
            "Insert the derived endpoint coefficient into the preregistered integrated D4 asymptotic, perform the endpoint subtraction at each rung, and prove or bound the analytic remainder before fitting the fixed-decay outer-regulator limit.",
            "",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    mp.mp.dps = MP_DIGITS
    AMP.mp.mp.dps = MP_DIGITS
    output = output.resolve()
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    paths = source_paths()
    registered_sources = source_rows(paths)
    references, ledger = reference_rows()
    events = read_csv(EVENTS_5358)
    old_kernel = M5342.configure()
    sequence_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    residue_summaries: list[dict[str, Any]] = []
    try:
        context = M5342.M5312.M5303.synthetic_context()
        epsilon_id = M5342.M5312.EPSILON_ID
        component = context["inventories"][epsilon_id]["components"]["MC04"]
        surfaces = context["surfaces"]
        physical_multiplier = mp.mpf(str(M5342.M5312.M5309.physical_multiplier()))
        for event in events:
            configuration = event_configuration(event, references)
            local_sequence, residue_summary = parent_energy_residue(
                configuration,
                component,
                surfaces,
                physical_multiplier,
            )
            sequence_rows.extend(local_sequence)
            residue_summaries.append(residue_summary)
            geometry = local_geometric_factors(configuration)
            C0 = residue_summary["C0"]
            C0_radius = residue_summary["C0_radius"]
            a_value = geometry["boundary_gap_epsilon_derivative"]
            z1_value = geometry["boundary_gap_parameter_derivative"]
            A_event = -configuration["log_sign"] * C0 * a_value / z1_value
            A_radius = abs(a_value / z1_value) * C0_radius + mp.mpf("1e-70")
            reference = configuration["reference"]
            finite_C0 = mp.mpc(
                reference["physical_coefficient_C0_real"],
                reference["physical_coefficient_C0_imaginary"],
            )
            finite_z0 = mp.mpc(
                reference["boundary_gap_z0_real"],
                reference["boundary_gap_z0_imaginary"],
            )
            finite_z1 = mp.mpc(
                reference["boundary_gap_derivative_z1_real"],
                reference["boundary_gap_derivative_z1_imaginary"],
            )
            finite_A_row = ledger[configuration["event_id"]]
            finite_A = mp.mpc(
                finite_A_row["A_event_real"], finite_A_row["A_event_imaginary"]
            )
            finite_a = finite_z0 / mp.mpf("0.000625")
            source_slope = mp.mpf(event["signed_support_margin_slope"])
            row = {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "term_id": configuration["term_id"],
                "primary_surface_id": configuration["surface_id"],
                "selected_role": configuration["role"],
                "selected_labels": "|".join(configuration["labels"]),
                "zero_regulator_absolute_soft_cosine": event[
                    "zero_regulator_absolute_soft_cosine"
                ],
                "zero_regulator_soft_energy": event["zero_regulator_soft_energy"],
                "positive_regulator_external_root": "-i*sqrt(5)/2",
                "log_sign": configuration["log_sign"],
                "contact_boundary": configuration["contact_boundary"],
                "inside_coordinate_direction_sign": configuration[
                    "inside_coordinate_direction_sign"
                ],
                **complex_fields("C0_zero", C0),
                "C0_zero_disk_radius": mp_text(C0_radius),
                "C0_zero_relative_disk_radius": residue_summary[
                    "C0_relative_radius"
                ],
                **complex_fields("partial_P_partial_R", geometry["partial_p_r"]),
                **complex_fields("partial_P_partial_c", geometry["partial_p_c"]),
                **complex_fields("partial_P_partial_q", geometry["partial_p_q"]),
                **complex_fields(
                    "boundary_gap_epsilon_derivative", a_value
                ),
                **complex_fields("boundary_gap_x_derivative", geometry["boundary_gap_x_derivative"]),
                **complex_fields(
                    "boundary_gap_parameter_derivative", z1_value
                ),
                **complex_fields("A_event_zero", A_event),
                "A_event_zero_disk_radius": mp_text(A_radius),
                "source_5358_support_margin_slope": event[
                    "signed_support_margin_slope"
                ],
                "derived_support_margin_slope": mp_text(
                    geometry["support_margin_slope"]
                ),
                "support_margin_slope_relative_difference": relative_difference(
                    geometry["support_margin_slope"], source_slope
                ),
                "finite_E000625_C0_real": mp_text(mp.re(finite_C0)),
                "finite_E000625_C0_real_relative_difference": relative_difference(
                    C0, mp.re(finite_C0)
                ),
                "finite_E000625_z0_over_epsilon_imaginary": mp_text(mp.im(finite_a)),
                "finite_E000625_gap_derivative_relative_difference": relative_difference(
                    a_value, 1j * mp.im(finite_a)
                ),
                "finite_E000625_z1_real": mp_text(mp.re(finite_z1)),
                "finite_E000625_z1_real_relative_difference": relative_difference(
                    z1_value, mp.re(finite_z1)
                ),
                "finite_E000625_A_imaginary": mp_text(mp.im(finite_A)),
                "finite_E000625_A_imaginary_relative_difference": relative_difference(
                    A_event, 1j * mp.im(finite_A)
                ),
                "minimum_sampled_collision_jacobian_magnitude": mp_text(
                    residue_summary["minimum_collision_jacobian"]
                ),
                "maximum_sampled_collision_root_difference": mp_text(
                    residue_summary["maximum_collision_root_difference"]
                ),
                "all_parent_masks_active": residue_summary["all_masks_active"],
                "parent_orientations": "|".join(
                    str(value) for value in residue_summary["orientations"]
                ),
                "parent_windings": "|".join(
                    str(value) for value in residue_summary["windings"]
                ),
                CLAIM_RESIDUE: False,
                CLAIM_ENDPOINTS: False,
                CLAIM_LIMIT: False,
                **no_downstream_claims(),
            }
            endpoint_rows.append(row)
    finally:
        M5342.M5326.restore_kernel(old_kernel)

    A_values = [
        mp.mpc(row["A_event_zero_real"], row["A_event_zero_imaginary"])
        for row in endpoint_rows
    ]
    A_radii = [mp.mpf(row["A_event_zero_disk_radius"]) for row in endpoint_rows]
    A_total = sum(A_values, mp.mpc(0))
    A_total_radius = sum(A_radii, mp.mpf(0))
    result_5357 = read_json(RESULT_5357)
    ladder_intercept = mp.mpc(
        result_5357["selected_intercept_real"],
        result_5357["selected_intercept_imaginary"],
    )
    ladder_envelope = mp.mpf(
        str(result_5357["conservative_intercept_envelope_radius"])
    )
    direct_to_ladder = abs(A_total - ladder_intercept)
    sum_rows = [
        {
            "comparison_id": "DIRECT_ZERO_REGULATOR_SUM",
            **complex_fields("A_total", A_total),
            "disk_radius": mp_text(A_total_radius),
            "source": str(EVENTS_5358.resolve()),
            CLAIM_LIMIT: False,
            **no_downstream_claims(),
        },
        {
            "comparison_id": "CHECKPOINT_5357_SIX_RUNG_INTERCEPT",
            **complex_fields("A_total", ladder_intercept),
            "disk_radius": mp_text(ladder_envelope),
            "source": str(RESULT_5357.resolve()),
            CLAIM_LIMIT: False,
            **no_downstream_claims(),
        },
        {
            "comparison_id": "DIRECT_TO_LADDER_DIFFERENCE",
            **complex_fields("A_total", A_total - ladder_intercept),
            "disk_radius": mp_text(A_total_radius + ladder_envelope),
            "source": f"{EVENTS_5358.resolve()}|{RESULT_5357.resolve()}",
            CLAIM_LIMIT: False,
            **no_downstream_claims(),
        },
    ]
    max_residue_relative_radius = max(
        summary["C0_relative_radius"] for summary in residue_summaries
    )
    max_C0_imaginary_ratio = max(
        abs(mp.mpf(row["C0_zero_imaginary"]))
        / max(abs(mp.mpf(row["C0_zero_real"])), mp.mpf("1e-300"))
        for row in endpoint_rows
    )
    max_finite_C0_difference = max(
        float(row["finite_E000625_C0_real_relative_difference"])
        for row in endpoint_rows
    )
    max_finite_a_difference = max(
        float(row["finite_E000625_gap_derivative_relative_difference"])
        for row in endpoint_rows
    )
    max_finite_z1_difference = max(
        float(row["finite_E000625_z1_real_relative_difference"])
        for row in endpoint_rows
    )
    max_finite_A_difference = max(
        float(row["finite_E000625_A_imaginary_relative_difference"])
        for row in endpoint_rows
    )
    max_support_slope_difference = max(
        float(row["support_margin_slope_relative_difference"])
        for row in endpoint_rows
    )
    max_root_difference = max(
        mp.mpf(row["maximum_sampled_collision_root_difference"])
        for row in endpoint_rows
    )
    min_partial_p_r = min(
        mp.mpf(row["partial_P_partial_R_magnitude"]) for row in endpoint_rows
    )
    max_A_real = max(abs(mp.mpf(row["A_event_zero_real"])) for row in endpoint_rows)
    validations = [
        validation_row("preflight_passes", preflight_result["all_pass"], preflight_result["checks"]),
        validation_row("exactly_eight_endpoint_rows_are_present", [row["event_id"] for row in endpoint_rows] == list(EVENT_IDS), len(endpoint_rows)),
        validation_row("all_parent_masks_are_active_on_the_physical_energy_side", all(parse_bool(row["all_parent_masks_active"]) for row in endpoint_rows), [row["parent_orientations"] for row in endpoint_rows]),
        validation_row("parent_windings_and_orientations_are_source_owned", all(row["parent_orientations"] == "1" and row["parent_windings"] in {"-2", "2"} for row in endpoint_rows), [(row["event_id"], row["parent_windings"]) for row in endpoint_rows]),
        validation_row("analytic_collision_roots_match_on_every_residue_sample", max_root_difference <= mp.mpf("1e-70"), mp_text(max_root_difference)),
        validation_row("all_material_R_jacobians_are_nonzero", min_partial_p_r >= mp.mpf("1e-3"), mp_text(min_partial_p_r)),
        validation_row("direct_parent_residue_certificates_are_tight", max_residue_relative_radius <= RESIDUE_RELATIVE_RADIUS_LIMIT, max_residue_relative_radius),
        validation_row("zero_regulator_parent_residues_are_real", max_C0_imaginary_ratio <= mp.mpf("1e-20"), mp_text(max_C0_imaginary_ratio)),
        validation_row("direct_C0_limits_match_the_smallest_finite_rung", max_finite_C0_difference <= FINITE_C0_RELATIVE_LIMIT, max_finite_C0_difference),
        validation_row("derived_gap_regulator_derivatives_match_the_smallest_rung", max_finite_a_difference <= FINITE_GAP_DERIVATIVE_RELATIVE_LIMIT, max_finite_a_difference),
        validation_row("derived_gap_coordinate_derivatives_match_the_smallest_rung", max_finite_z1_difference <= FINITE_GAP_SLOPE_RELATIVE_LIMIT, max_finite_z1_difference),
        validation_row("derived_support_margin_slopes_reproduce_checkpoint_5358", max_support_slope_difference <= 1.0e-25, max_support_slope_difference),
        validation_row("direct_event_limits_match_the_smallest_finite_rung", max_finite_A_difference <= FINITE_A_RELATIVE_LIMIT, max_finite_A_difference),
        validation_row("event_limits_are_purely_imaginary_within_the_direct_certificate", max_A_real <= max(A_radii), f"max_real={mp_text(max_A_real)};max_radius={mp_text(max(A_radii))}"),
        validation_row("direct_endpoint_sum_is_nonzero_outside_its_disk", abs(A_total) > A_total_radius, f"magnitude={mp_text(abs(A_total))};radius={mp_text(A_total_radius)}"),
        validation_row("direct_sum_agrees_with_the_frozen_six_rung_envelope", direct_to_ladder <= ladder_envelope + A_total_radius, f"distance={mp_text(direct_to_ladder)};envelope={mp_text(ladder_envelope)}"),
        validation_row("integrated_and_downstream_claims_remain_false", all(value is False for value in no_downstream_claims().values()), no_downstream_claims()),
        validation_row("formal_workbench_remains_unchanged", M5342.M5283.formal_inventory_digest() == M5342.FORMAL_DIGEST, M5342.M5283.formal_inventory_digest()),
        validation_row("scripts_cache_remains_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_RESIDUE: passed,
        CLAIM_ENDPOINTS: passed,
        CLAIM_LIMIT: passed,
        **no_downstream_claims(),
    }
    for row in sequence_rows:
        row[CLAIM_RESIDUE] = passed
        row[CLAIM_ENDPOINTS] = passed
        row[CLAIM_LIMIT] = passed
        row.update(no_downstream_claims())
    for row in endpoint_rows:
        row.update(claims)
    for row in sum_rows:
        row.update(claims)
    contracts = contract_rows()
    for row in contracts:
        row[CLAIM_LIMIT] = passed
    for row in registered_sources:
        row[CLAIM_RESIDUE] = passed
        row[CLAIM_ENDPOINTS] = passed
        row[CLAIM_LIMIT] = passed
    result = {
        "mode": "D4-zero-regulator-endpoint-coefficient-limit",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_ZERO_REGULATOR_EIGHT_ENDPOINT_COEFFICIENT_LIMIT_DERIVED__FIT_INTEGRATED_D4"
            if passed
            else "D4_ZERO_REGULATOR_ENDPOINT_COEFFICIENT_LIMIT_BLOCKED"
        ),
        "event_count": len(endpoint_rows),
        "positive_regulator_branch": "w(0)=-i*sqrt(5)/2",
        "q_zero": -1.25,
        "q_epsilon_derivative": "-i/32",
        "physical_multiplier": float(physical_multiplier),
        "maximum_parent_residue_relative_disk_radius": max_residue_relative_radius,
        "maximum_smallest_rung_C0_relative_difference": max_finite_C0_difference,
        "maximum_smallest_rung_gap_derivative_relative_difference": max_finite_a_difference,
        "maximum_smallest_rung_z1_relative_difference": max_finite_z1_difference,
        "maximum_smallest_rung_A_relative_difference": max_finite_A_difference,
        "A_total_zero_real": float(mp.re(A_total)),
        "A_total_zero_imaginary": float(mp.im(A_total)),
        "A_total_zero_magnitude": float(abs(A_total)),
        "A_total_zero_disk_radius": float(A_total_radius),
        "ladder_intercept_real": float(mp.re(ladder_intercept)),
        "ladder_intercept_imaginary": float(mp.im(ladder_intercept)),
        "ladder_envelope_radius": float(ladder_envelope),
        "direct_to_ladder_distance": float(direct_to_ladder),
        "claim_boundary": claims,
        "remaining_obstruction": "insert the derived endpoint coefficient into the integrated D4 subtraction and prove or bound the analytic remainder before the fixed-decay outer-regulator fit",
        "source_files": registered_sources,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_zero_regulator_endpoint_limit_contract.csv", contracts)
    atomic_csv(output / "D4_zero_regulator_parent_residue_sequence.csv", sequence_rows)
    atomic_csv(output / "D4_zero_regulator_endpoint_coefficients.csv", endpoint_rows)
    atomic_csv(output / "D4_zero_regulator_endpoint_sum_comparison.csv", sum_rows)
    atomic_csv(output / "D4_zero_regulator_endpoint_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_zero_regulator_endpoint_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result, endpoint_rows)
    return result


def self_test() -> dict[str, Any]:
    mp.mp.dps = 70
    q_zero = mp.mpf(Q_ZERO_TEXT)
    w_zero = -1j * mp.sqrt(5) / 2
    points = [
        (mp.mpf(value), 3 + 2 * mp.mpf(value) - 5 * mp.mpf(value) ** 2 + 7 * mp.mpf(value) ** 3)
        for value in ("0.1", "0.05", "0.025", "0.0125")
    ]
    checks = {
        "positive_regulator_root_squares_to_q_zero": abs(w_zero**2 - q_zero)
        <= mp.mpf("1e-60"),
        "target_map_derivative_is_minus_i_over_32": abs(
            mp.diff(
                lambda epsilon: (1 - (-9 + 1j * epsilon))
                / (1 + (-9 + 1j * epsilon)),
                mp.mpf(0),
            )
            + 1j / 32
        )
        <= mp.mpf("1e-60"),
        "polynomial_intercept_recovers_constant": abs(polynomial_intercept(points) - 3)
        <= mp.mpf("1e-60"),
        "event_partition_is_frozen": EVENT_IDS == tuple(f"E{index:02d}" for index in range(1, 9)),
        "integrated_and_downstream_claims_start_false": all(
            value is False for value in no_downstream_claims().values()
        ),
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        payload = self_test()
    elif arguments.dry_run:
        payload = preflight()
    else:
        payload = run(arguments.output_dir)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
