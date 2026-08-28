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
OUTPUT = FUNCTIONAL_RG / "5378"
DOCUMENT = POST / "5378-Y5-R2FR-D4-zero-parent-C-derivative-decomposition.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5378_VALIDATION.csv"

SCRIPT_5359 = SCRIPTS / "Y5_R2FR_5359_D4_zero_regulator_endpoint_coefficient_limit.py"
SCRIPT_5377 = SCRIPTS / "Y5_R2FR_5377_D4_full_endpoint_C_reconstruction_and_fixed_AC_gate.py"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
RESULT_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
VALIDATION_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_validation.csv"
ENDPOINTS_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
RESULT_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
VALIDATION_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
EVENTS_5377 = FUNCTIONAL_RG / "5377" / "D4_full_endpoint_primitive_event_reconstruction.csv"
ATLAS_5377 = FUNCTIONAL_RG / "5377" / "D4_sampled_event_branch_atlas.csv"
RESULT_5377 = FUNCTIONAL_RG / "5377" / "D4_full_endpoint_C_reconstruction_result.json"
VALIDATION_5377 = FUNCTIONAL_RG / "5377" / "D4_full_endpoint_C_reconstruction_validation.csv"

CHECKPOINT = 5378
MARKER = "MTS_5378_D4_ZERO_PARENT_C_DERIVATIVE_DECOMPOSITION"
REVISION = "D4-zero-parent-C-derivative-decomposition-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
MP_DIGITS = 110
ENERGY_LEVELS = 10
ENERGY_ORDER = 5
ENERGY_INITIAL_STEP = "1e-6"
GLOBAL_EXPONENT = 30
GLOBAL_CROSSCHECK_EXPONENT = 24
GLOBAL_PHASE = "0.37"
GLOBAL_CROSSCHECK_PHASE = "1.11"
C1_INITIAL_STEP = "1e-5"
C1_LEVELS = 6
C1_EXTRAPOLATION_ORDER = 4
C0_EPSILON_INITIAL_STEP = "0.000625"
C0_EPSILON_LEVELS = 7
C0_EPSILON_EXTRAPOLATION_ORDER = 5
RADIUS_SAFETY_FACTOR = 8

CLAIM_TRACE = "valid_for_D4_zero_parent_complex_trace_continuation"
CLAIM_C1 = "valid_for_D4_zero_parent_C1_coefficient"
CLAIM_GEOMETRY = "valid_for_D4_zero_parent_geometry_second_derivative"
CLAIM_C_NUMERIC = "valid_for_D4_zero_parent_C_log_numerical_certificate"
STRICT_OPEN_CLAIMS = (
    "valid_for_D4_endpoint_C_regulator_zero_limit",
    "valid_for_D4_common_closed_interval_event_atlas",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
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


M5359 = load_module("mts_5359_for_5378", SCRIPT_5359)
M5377 = load_module("mts_5377_for_5378", SCRIPT_5377)
mp = M5359.mp
AMP = M5359.AMP


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5359.set_below_normal_priority()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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


def complex_from_row(row: dict[str, Any], prefix: str) -> Any:
    return mp.mpc(row[f"{prefix}_real"], row[f"{prefix}_imaginary"])


def relative_difference(first: Any, second: Any) -> float:
    return float(abs(first - second) / max(abs(first), abs(second), mp.mpf("1e-300")))


def finite_complex(value: Any) -> bool:
    return math.isfinite(float(mp.re(value))) and math.isfinite(float(mp.im(value)))


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def strict_open_claims() -> dict[str, bool]:
    return {claim: False for claim in STRICT_OPEN_CLAIMS}


def source_paths() -> tuple[Path, ...]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5359,
        SCRIPT_5377,
        Path(AMP.__file__).resolve(),
        Path(M5359.M5358.__file__).resolve(),
        EVENTS_5358,
        RESULT_5358,
        VALIDATION_5358,
        ENDPOINTS_5359,
        RESULT_5359,
        VALIDATION_5359,
        EVENTS_5377,
        ATLAS_5377,
        RESULT_5377,
        VALIDATION_5377,
        Path(M5377.INPUTS_5373),
        Path(M5377.RESULT_5373),
        Path(M5377.VALIDATION_5373),
    )
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_TRACE: False,
            CLAIM_C1: False,
            CLAIM_GEOMETRY: False,
            CLAIM_C_NUMERIC: False,
            **strict_open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    result_5358 = read_json(RESULT_5358)
    result_5359 = read_json(RESULT_5359)
    result_5377 = read_json(RESULT_5377)
    events = read_csv(EVENTS_5358)
    endpoints = read_csv(ENDPOINTS_5359)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in paths),
        "checkpoint_5358_passes": result_5358.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5358)),
        "checkpoint_5359_passes": result_5359.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5359)),
        "checkpoint_5377_passes": result_5377.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5377)),
        "exactly_eight_ordered_zero_events": [row["event_id"] for row in events]
        == list(EVENT_IDS),
        "exactly_eight_ordered_zero_coefficients": [row["event_id"] for row in endpoints]
        == list(EVENT_IDS),
        "prior_C_limit_stays_open": result_5377.get("claim_boundary", {}).get(
            "valid_for_D4_endpoint_C_regulator_zero_limit"
        )
        is False,
        "formal_workbench_inventory_is_unchanged": M5359.M5342.M5283.formal_inventory_digest()
        == M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def polynomial_intercept_with_radius(
    points: list[tuple[Any, Any, Any]],
) -> tuple[Any, Any]:
    value = mp.mpc(0)
    radius = mp.mpf(0)
    for index, (x_value, y_value, y_radius) in enumerate(points):
        weight = mp.mpf(1)
        for other_index, (other_x, _, _) in enumerate(points):
            if other_index == index:
                continue
            weight *= -other_x / (x_value - other_x)
        value += weight * y_value
        radius += abs(weight) * y_radius
    return value, radius


def target_and_q(epsilon: Any) -> tuple[Any, Any]:
    target = mp.mpc(-9, epsilon)
    return target, (1 - target) / (1 + target)


def material_recoil(configuration: dict[str, Any], epsilon: Any, coordinate: Any) -> Any:
    _, q_value = target_and_q(epsilon)
    coefficient_a, coefficient_b, coefficient_c = M5359.M5358.material_coefficients(
        configuration["surface_id"],
        configuration["sign"] * coordinate,
        configuration["decay_cosine"],
        q_value,
    )
    if abs(coefficient_a) <= mp.mpf("1e-60"):
        return -coefficient_c / coefficient_b
    square_root = mp.sqrt(coefficient_b**2 - 4 * coefficient_a * coefficient_c)
    candidates = (
        (-coefficient_b - square_root) / (2 * coefficient_a),
        (-coefficient_b + square_root) / (2 * coefficient_a),
    )
    return min(candidates, key=lambda value: abs(value - configuration["recoil"]))


def complex_event_geometry(
    soft_energy: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    relative_circle: Any,
) -> tuple[list[Any], list[Any], list[list[Any]]]:
    energy = mp.mpc(soft_energy)
    soft_cosine = mp.mpc(soft_cosine)
    decay_cosine = mp.mpc(decay_cosine)
    soft_transverse = mp.sqrt(1 - soft_cosine**2)
    decay_transverse = mp.sqrt(1 - decay_cosine**2)
    azimuth_cosine = (relative_circle + 1 / relative_circle) / 2
    azimuth_sine = (relative_circle - 1 / relative_circle) / (2j)
    soft_direction = [soft_transverse, mp.mpc(0), soft_cosine]
    decay_direction = [
        decay_transverse * azimuth_cosine,
        decay_transverse * azimuth_sine,
        decay_cosine,
    ]
    relative_cosine = sum(
        soft_direction[index] * decay_direction[index] for index in range(3)
    )
    recoil = mp.sqrt(1 - energy)
    beta = energy / (2 - energy)
    gamma = (2 - energy) / (2 * recoil)
    gamma_beta = energy / (2 * recoil)
    internal: list[list[Any]] = []
    for sign in (1, -1):
        local_energy = gamma * recoil * (1 - sign * beta * relative_cosine)
        spatial = [
            recoil
            * (
                sign * decay_direction[index]
                + (sign * (gamma - 1) * relative_cosine - gamma_beta)
                * soft_direction[index]
            )
            for index in range(3)
        ]
        internal.append([local_energy, *spatial])
    internal.append([energy, *[energy * value for value in soft_direction]])
    return soft_direction, decay_direction, internal


def complex_finite_plus_components(
    internal_values: Any,
    soft_energy: Any,
    soft_direction_values: Any,
    decay_direction_values: Any,
    scattering_cosine: Any,
    unit_circle: Any,
) -> tuple[Any, Any]:
    internal = AMP.mp_matrix(internal_values)
    soft_direction = AMP.mp_vector(soft_direction_values)
    decay_direction = AMP.mp_vector(decay_direction_values)
    target = mp.mpc(scattering_cosine)
    rotated = AMP.rotate_internal(internal, unit_circle)
    inverse_energy_square_sum = sum(1 / momentum[0] ** 2 for momentum in rotated)
    energy = mp.mpc(soft_energy)
    multiplier = 3 / rotated[2][0] ** 2 / inverse_energy_square_sum
    direct = (
        energy**2
        * multiplier
        * AMP.hhh_reduced_product(rotated, target)
        / (AMP.S_VALUE * AMP.S_VALUE)
    )
    subtraction = AMP.endpoint_value(
        soft_direction, decay_direction, target, unit_circle
    )
    return direct / energy, -subtraction / energy


def representative_relative_root(
    energy: Any, soft_cosine: Any, decay_cosine: Any, q_value: Any
) -> Any:
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


def global_root(direction: list[Any], label: str, external_root: Any) -> Any:
    holomorphic = (direction[0] + 1j * direction[1]) / (1 + direction[2])
    antiholomorphic = (direction[0] - 1j * direction[1]) / (1 + direction[2])
    roots = {
        "plus_u": external_root / holomorphic,
        "plus_v": antiholomorphic / external_root,
        "minus_u": -1 / (external_root * holomorphic),
        "minus_v": -external_root * antiholomorphic,
    }
    return roots[label]


def analytic_parent_relative_residue(
    configuration: dict[str, Any],
    energy: Any,
    epsilon: Any,
    component: dict[str, Any],
    exponent: int,
    phase: Any,
) -> dict[str, Any]:
    target, q_value = target_and_q(epsilon)
    external_root = -1j * mp.sqrt(-q_value)
    soft_cosine = configuration["soft_cosine"]
    decay_cosine = configuration["decay_cosine"]
    representative_root = representative_relative_root(
        energy, soft_cosine, decay_cosine, q_value
    )
    relative_root = (
        1 / representative_root
        if configuration["role"] == "reciprocal"
        else representative_root
    )

    def collision_roots(varied_relative_root: Any) -> tuple[Any, Any]:
        _, _, local_internal = complex_event_geometry(
            energy, soft_cosine, decay_cosine, varied_relative_root
        )
        directions = [
            [
                local_internal[index][component_index]
                / local_internal[index][0]
                for component_index in range(1, 4)
            ]
            for index in (0, 2)
        ]
        return (
            global_root(directions[0], configuration["root_labels"][0], external_root),
            global_root(directions[1], configuration["root_labels"][1], external_root),
        )

    soft_direction, decay_direction, internal = complex_event_geometry(
        energy, soft_cosine, decay_cosine, relative_root
    )
    roots = collision_roots(relative_root)
    selected_global_root = (roots[0] + roots[1]) / 2
    collision_jacobian = mp.diff(
        lambda value: collision_roots(value)[0] - collision_roots(value)[1],
        relative_root,
    )
    displacement = (
        mp.power(10, -exponent)
        * max(mp.mpf(1), abs(selected_global_root))
        * mp.exp(1j * phase)
    )
    direct, subtraction = complex_finite_plus_components(
        internal,
        energy,
        soft_direction,
        decay_direction,
        target,
        selected_global_root + displacement,
    )
    double_pole_coefficient = (direct + subtraction) * displacement**2
    winding = M5359.M5342.M5312.M5280.M5277.source_winding_delta(
        component, configuration["role"]
    )
    residue = (
        winding
        * configuration["trace_orientation"]
        * double_pole_coefficient
        / (relative_root * selected_global_root * collision_jacobian)
    )
    return {
        "residue": residue,
        "root_difference": roots[0] - roots[1],
        "collision_jacobian": collision_jacobian,
        "winding": int(winding),
    }


def parent_C0(
    configuration: dict[str, Any],
    epsilon: Any,
    coordinate: Any,
    component: dict[str, Any],
    physical_multiplier: Any,
) -> dict[str, Any]:
    recoil = material_recoil(configuration, epsilon, coordinate)
    pole_energy = 1 - recoil**2
    local_configuration = {
        **configuration,
        "soft_cosine": configuration["sign"] * coordinate,
        "recoil": recoil,
        "energy": pole_energy,
    }
    points: list[tuple[Any, Any, Any]] = []
    states: list[dict[str, Any]] = []
    initial_step = mp.mpf(ENERGY_INITIAL_STEP)
    for level in range(ENERGY_LEVELS):
        step = initial_step / mp.power(2, level)
        displacement = local_configuration["energy_approach_sign"] * step
        state = analytic_parent_relative_residue(
            local_configuration,
            pole_energy + displacement,
            epsilon,
            component,
            GLOBAL_EXPONENT,
            mp.mpf(GLOBAL_PHASE),
        )
        estimator = physical_multiplier * displacement * state["residue"]
        points.append((step, estimator, mp.mpf(0)))
        states.append(state)
    selected, _ = polynomial_intercept_with_radius(points[-ENERGY_ORDER:])
    previous, _ = polynomial_intercept_with_radius(points[-ENERGY_ORDER - 1 : -1])
    lower, _ = polynomial_intercept_with_radius(points[-ENERGY_ORDER + 1 :])
    higher, _ = polynomial_intercept_with_radius(points[-ENERGY_ORDER - 1 :])
    final_step, final_value, _ = points[-1]
    final_displacement = local_configuration["energy_approach_sign"] * final_step
    exponent_state = analytic_parent_relative_residue(
        local_configuration,
        pole_energy + final_displacement,
        epsilon,
        component,
        GLOBAL_CROSSCHECK_EXPONENT,
        mp.mpf(GLOBAL_PHASE),
    )
    exponent_value = physical_multiplier * final_displacement * exponent_state["residue"]
    phase_state = analytic_parent_relative_residue(
        local_configuration,
        pole_energy + final_displacement,
        epsilon,
        component,
        GLOBAL_EXPONENT,
        mp.mpf(GLOBAL_CROSSCHECK_PHASE),
    )
    phase_value = physical_multiplier * final_displacement * phase_state["residue"]
    errors = {
        "successive_window_shift": abs(selected - previous),
        "lower_order_shift": abs(selected - lower),
        "higher_order_shift": abs(selected - higher),
        "exponent_shift": abs(final_value - exponent_value),
        "phase_shift": abs(final_value - phase_value),
    }
    radius = RADIUS_SAFETY_FACTOR * max(*errors.values(), mp.mpf("1e-80"))
    return {
        "C0": selected,
        "radius": radius,
        "pole_energy": pole_energy,
        "recoil": recoil,
        "minimum_collision_jacobian": min(
            abs(state["collision_jacobian"]) for state in states
        ),
        "maximum_root_difference": max(abs(state["root_difference"]) for state in states),
        "winding": states[-1]["winding"],
        "errors": errors,
    }


def extrapolated_value(
    points: list[tuple[Any, Any, Any]], order: int
) -> dict[str, Any]:
    selected, propagated = polynomial_intercept_with_radius(points[-order:])
    previous, previous_radius = polynomial_intercept_with_radius(points[-order - 1 : -1])
    lower, lower_radius = polynomial_intercept_with_radius(points[-order + 1 :])
    higher, higher_radius = polynomial_intercept_with_radius(points[-order - 1 :])
    shifts = (
        abs(selected - previous) + previous_radius,
        abs(selected - lower) + lower_radius,
        abs(selected - higher) + higher_radius,
    )
    radius = RADIUS_SAFETY_FACTOR * max(propagated, *shifts, mp.mpf("1e-70"))
    return {
        "value": selected,
        "radius": radius,
        "propagated_radius": propagated,
        "maximum_window_shift": max(shifts),
    }


def hard_boundary_energy(configuration: dict[str, Any], coordinate: Any) -> Any:
    if configuration["event_type"] == "BRANCH_DEATH":
        return M5359.M5358.ENERGY_MAXIMUM
    roots = M5359.M5358.hard_boundary_roots(
        configuration["sign"] * coordinate,
        configuration["decay_cosine"],
    )
    recoil = min(roots, key=lambda value: abs(value - configuration["recoil"]))
    return 1 - recoil**2


def gap_value(configuration: dict[str, Any], epsilon: Any, coordinate: Any) -> Any:
    recoil = material_recoil(configuration, epsilon, coordinate)
    return hard_boundary_energy(configuration, coordinate) - (1 - recoil**2)


def continued_event_coordinate(
    configuration: dict[str, Any], epsilon: Any, zero_coordinate: Any
) -> Any:
    function = lambda coordinate: mp.re(
        gap_value(configuration, epsilon, coordinate)
    )
    half_width = mp.mpf("1e-6")
    return mp.findroot(
        function,
        (zero_coordinate - half_width, zero_coordinate + half_width),
    )


def geometry_derivatives(configuration: dict[str, Any]) -> dict[str, Any]:
    coordinate = mp.mpf(
        configuration["event"]["zero_regulator_absolute_soft_cosine"]
    )
    sigma = (
        mp.mpf(configuration["inside_coordinate_direction_sign"])
        if configuration["event_type"] == "BRANCH_DEATH"
        else mp.mpf(1)
    )
    z_e = mp.diff(lambda epsilon: gap_value(configuration, epsilon, coordinate), 0)
    z_ee = mp.diff(
        lambda epsilon: gap_value(configuration, epsilon, coordinate), 0, 2
    )
    z_x = mp.diff(
        lambda value: gap_value(configuration, mp.mpf(0), value), coordinate
    )
    z_xe = mp.diff(
        lambda epsilon: mp.diff(
            lambda value: gap_value(configuration, epsilon, value), coordinate
        ),
        0,
    )
    event_coordinate_second_derivative = -mp.re(z_ee) / mp.re(z_x)
    z0_second_derivative = z_ee + z_x * event_coordinate_second_derivative
    z1 = sigma * z_x
    z1_e = sigma * z_xe
    ratio_first_derivative = z_e / z1
    ratio_second_derivative = (
        z0_second_derivative / z1 - 2 * z_e * z1_e / z1**2
    )
    return {
        "sigma": sigma,
        "z_e": z_e,
        "z_ee_fixed_x": z_ee,
        "z_x": z_x,
        "z_xe": z_xe,
        "event_coordinate_second_derivative": event_coordinate_second_derivative,
        "z0_second_derivative": z0_second_derivative,
        "z1": z1,
        "z1_e": z1_e,
        "ratio_first_derivative": ratio_first_derivative,
        "ratio_second_derivative": ratio_second_derivative,
    }


def atlas_curvature(event_id: str, zero_coordinate: Any) -> Any:
    rows = [
        row
        for row in read_csv(ATLAS_5377)
        if row["event_id"] == event_id and mp.mpf(row["epsilon"]) > 0
    ]
    numerator = mp.mpf(0)
    denominator = mp.mpf(0)
    for row in rows:
        epsilon_squared = mp.mpf(row["epsilon"]) ** 2
        displacement = mp.mpf(row["event_coordinate"]) - zero_coordinate
        numerator += epsilon_squared * displacement
        denominator += epsilon_squared**2
    return 2 * numerator / denominator


def robust_finite_C1_reference(event_id: str) -> Any:
    rows = [
        row
        for row in read_csv(EVENTS_5377)
        if row["event_id"] == event_id and mp.mpf(row["epsilon"]) >= mp.mpf("0.0025")
    ]
    values = sorted(mp.re(complex_from_row(row, "C1")) for row in rows)
    return (values[(len(values) - 1) // 2] + values[len(values) // 2]) / 2


def contract_rows(claims: dict[str, bool]) -> list[dict[str, Any]]:
    common = {**claims, **strict_open_claims()}
    return [
        {
            "contract_id": "EC5378_01_unmasked_trace",
            "premises": "the support selector changes orientation at a contact, but C1 differentiates the unmasked analytic residue trace",
            "derived_statement": "freeze the zero-event source orientation while retaining the source winding and analytic parent pole",
            "status": "DERIVED_TRACE_CONTINUATION",
            **common,
        },
        {
            "contract_id": "EC5378_02_event_motion",
            "premises": "Re z(epsilon,x(epsilon))=0, z(0,x0)=0, and conjugation symmetry gives x'(0)=0",
            "derived_statement": "x''(0)=-Re(z_ee)/Re(z_x)",
            "status": "EXACT_IMPLICIT_DERIVATIVE",
            **common,
        },
        {
            "contract_id": "EC5378_03_ratio_derivative",
            "premises": "r=z0/z1, z0(0)=0, z1=sigma*z_x",
            "derived_statement": "r'=z_e/z1 and r''=(z_ee+z_x*x'')/z1-2*z_e*z1_e/z1^2",
            "status": "EXACT_ALGEBRA",
            **common,
        },
        {
            "contract_id": "EC5378_04_parent_C_derivative",
            "premises": "H=-s[C0*r-(C1/2)r^2]",
            "derived_statement": "C_log,e=-s[C0_e*r'+(C0/2)r''-(C1/2)(r')^2] at epsilon=0",
            "status": "DIRECT_PARENT_DECOMPOSITION",
            **common,
        },
        {
            "contract_id": "EC5378_05_claim_boundary",
            "premises": "high-precision derivative sequences are not interval enclosures on a common closed complex neighborhood",
            "derived_statement": "the parent numerical C certificate may pass while the strict regulator-zero theorem, H3, W3 and D4 outer limit remain open",
            "status": "NO_BROAD_CLAIM",
            **common,
        },
    ]


def render_document(result: dict[str, Any], decomposition: list[dict[str, Any]]) -> None:
    lines = [
        "# 5378 - D4 zero-parent C derivative decomposition",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Derived identities",
        "",
        "The event continuation is fixed by `Re z(epsilon,x(epsilon))=0`. Conjugation symmetry gives `x'(0)=0`, hence",
        "",
        "`x''(0)=-Re(z_ee)/Re(z_x)`.",
        "",
        "With `r=z0/z1` and `z1=sigma z_x`,",
        "",
        "`r'=z_e/z1`,",
        "",
        "`r''=(z_ee+z_x x'')/z1-2 z_e z1_e/z1^2`.",
        "",
        "The full endpoint primitive therefore has the event coefficient",
        "",
        "`C_log,e=-s[C0_e r'+(C0/2)r''-(C1/2)(r')^2]`.",
        "",
        "## Eight-event result",
        "",
        "| event | C0_e(0) | C1(0) | C_log,e |",
        "|---|---:|---:|---:|",
    ]
    for row in decomposition:
        lines.append(
            f"| {row['event_id']} | {row['C0_e_zero_real']} {float(row['C0_e_zero_imaginary']):+g} i | {row['C1_zero_real']} {float(row['C1_zero_imaginary']):+g} i | {row['C_log_event_real']} {float(row['C_log_event_imaginary']):+g} i |"
        )
    lines.extend(
        [
            "",
            "## Sum",
            "",
            f"- Direct parent result: `{result['C_log_zero_parent_real']} {float(result['C_log_zero_parent_imaginary']):+g} i`.",
            f"- Diagnostic derivative radius: `{result['C_log_zero_parent_diagnostic_radius']}`.",
            f"- Independent checkpoint-5377 candidate: `{result['C_log_5377_candidate_real']} {result['C_log_5377_candidate_imaginary']:+} i`.",
            f"- Direct-to-candidate distance: `{result['direct_to_5377_candidate_distance']}` against candidate disk `{result['C_log_5377_candidate_disk']}`.",
            f"- Continued-root quotient result: `{result['C_log_continued_quotient_real']} {float(result['C_log_continued_quotient_imaginary']):+g} i`.",
            f"- Formula-to-quotient distance: `{result['formula_to_continued_quotient_distance']}`.",
            f"- Corrected fixed-A,C relative intercept envelope: `{result['corrected_fixed_A_C_relative_intercept_envelope']}`.",
            "",
            "## What closed",
            "",
            "The omitted `C1` term is now evaluated directly on all eight zero-regulator parent traces. The event-motion curvature and `r''` terms come from implicit differentiation, not a finite-rung event fit. The explicit parent regulator derivative `C0_e` comes from the physical one-sided analytic continuation and is independently checked against the smallest finite normal forms.",
            "",
            "## What remains open",
            "",
            "The earlier finite-rung C candidate is retained as a historical diagnostic, not promoted over the direct parent result: its event coordinates were adequate for topology but not for a second derivative quotient. This is still a high-precision source-backed numerical derivative certificate, not an interval theorem on one common closed complex neighborhood. The strict endpoint-C limit, common interval atlas, H3, mapped-away W3, D4 outer limit and all GR/MTS claims remain false until that enclosure is supplied.",
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
    registered_sources = source_rows()
    references, _ = M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    zero_rows = {row["event_id"]: row for row in read_csv(ENDPOINTS_5359)}
    finite_rows = {
        (row["epsilon_id"], row["event_id"]): row for row in read_csv(EVENTS_5377)
    }
    c1_sequence: list[dict[str, Any]] = []
    c0_epsilon_sequence: list[dict[str, Any]] = []
    continued_quotient_sequence: list[dict[str, Any]] = []
    geometry_rows: list[dict[str, Any]] = []
    decomposition_rows: list[dict[str, Any]] = []
    old_kernel = M5359.M5342.configure()
    try:
        context = M5359.M5342.M5312.M5303.synthetic_context()
        epsilon_id = M5359.M5342.M5312.EPSILON_ID
        component = context["inventories"][epsilon_id]["components"]["MC04"]
        physical_multiplier = mp.mpf(
            str(M5359.M5342.M5312.M5309.physical_multiplier())
        )
        for event in events:
            configuration = M5359.event_configuration(event, references)
            zero_source = zero_rows[configuration["event_id"]]
            orientation_values = [
                int(value)
                for value in zero_source["parent_orientations"].split("|")
                if value
            ]
            if orientation_values != [1]:
                raise RuntimeError(
                    f"unexpected zero trace orientation at {configuration['event_id']}: {orientation_values}"
                )
            configuration["trace_orientation"] = orientation_values[0]
            coordinate = mp.mpf(event["zero_regulator_absolute_soft_cosine"])
            sigma = (
                mp.mpf(configuration["inside_coordinate_direction_sign"])
                if configuration["event_type"] == "BRANCH_DEATH"
                else mp.mpf(1)
            )
            center = parent_C0(
                configuration,
                mp.mpf(0),
                coordinate,
                component,
                physical_multiplier,
            )
            c1_points: list[tuple[Any, Any, Any]] = []
            for level in range(C1_LEVELS):
                step = mp.mpf(C1_INITIAL_STEP) / mp.power(2, level)
                minus = parent_C0(
                    configuration,
                    mp.mpf(0),
                    coordinate - step,
                    component,
                    physical_multiplier,
                )
                plus = parent_C0(
                    configuration,
                    mp.mpf(0),
                    coordinate + step,
                    component,
                    physical_multiplier,
                )
                derivative = sigma * (plus["C0"] - minus["C0"]) / (2 * step)
                derivative_radius = (plus["radius"] + minus["radius"]) / (2 * step)
                c1_points.append((step**2, derivative, derivative_radius))
                c1_sequence.append(
                    {
                        "event_id": configuration["event_id"],
                        "level": level,
                        "coordinate_half_step": mp_text(step),
                        "extrapolation_coordinate": mp_text(step**2),
                        "trace_orientation": configuration["trace_orientation"],
                        "integration_coordinate_direction_sigma": mp_text(sigma),
                        **complex_fields("C0_minus", minus["C0"]),
                        "C0_minus_radius": mp_text(minus["radius"]),
                        **complex_fields("C0_plus", plus["C0"]),
                        "C0_plus_radius": mp_text(plus["radius"]),
                        **complex_fields("C1_estimator", derivative),
                        "C1_estimator_radius": mp_text(derivative_radius),
                    }
                )
            c1_result = extrapolated_value(c1_points, C1_EXTRAPOLATION_ORDER)
            c0_e_points: list[tuple[Any, Any, Any]] = []
            finite_crosscheck_difference = mp.nan
            for level in range(C0_EPSILON_LEVELS):
                epsilon = mp.mpf(C0_EPSILON_INITIAL_STEP) / mp.power(2, level)
                positive = parent_C0(
                    configuration,
                    epsilon,
                    coordinate,
                    component,
                    physical_multiplier,
                )
                derivative = (positive["C0"] - center["C0"]) / epsilon
                derivative_radius = (positive["radius"] + center["radius"]) / epsilon
                c0_e_points.append((epsilon, derivative, derivative_radius))
                finite_crosscheck = finite_rows[("E000625", configuration["event_id"])]
                finite_value = complex_from_row(finite_crosscheck, "C0")
                if level == 0:
                    finite_crosscheck_difference = relative_difference(
                        positive["C0"], finite_value
                    )
                c0_epsilon_sequence.append(
                    {
                        "event_id": configuration["event_id"],
                        "level": level,
                        "positive_epsilon": mp_text(epsilon),
                        **complex_fields("C0_positive", positive["C0"]),
                        "C0_positive_radius": mp_text(positive["radius"]),
                        **complex_fields("C0_e_estimator", derivative),
                        "C0_e_estimator_radius": mp_text(derivative_radius),
                        "maximum_collision_root_difference": mp_text(
                            positive["maximum_root_difference"]
                        ),
                        "minimum_collision_jacobian": mp_text(
                            positive["minimum_collision_jacobian"]
                        ),
                    }
                )
            c0_e_result = extrapolated_value(
                c0_e_points, C0_EPSILON_EXTRAPOLATION_ORDER
            )
            geometry = geometry_derivatives(configuration)
            source_z_e = complex_from_row(
                zero_source, "boundary_gap_epsilon_derivative"
            )
            source_z1 = complex_from_row(
                zero_source, "boundary_gap_parameter_derivative"
            )
            sampled_curvature = atlas_curvature(
                configuration["event_id"], coordinate
            )
            geometry_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "integration_coordinate_direction_sigma": mp_text(
                        geometry["sigma"]
                    ),
                    **complex_fields("z_e", geometry["z_e"]),
                    **complex_fields("z_ee_fixed_x", geometry["z_ee_fixed_x"]),
                    **complex_fields("z_x", geometry["z_x"]),
                    **complex_fields("z_xe", geometry["z_xe"]),
                    "event_coordinate_second_derivative": mp_text(
                        geometry["event_coordinate_second_derivative"]
                    ),
                    "sampled_atlas_event_coordinate_second_derivative": mp_text(
                        sampled_curvature
                    ),
                    "event_curvature_relative_difference": relative_difference(
                        geometry["event_coordinate_second_derivative"],
                        sampled_curvature,
                    ),
                    **complex_fields(
                        "z0_second_derivative", geometry["z0_second_derivative"]
                    ),
                    **complex_fields("z1", geometry["z1"]),
                    **complex_fields("z1_e", geometry["z1_e"]),
                    **complex_fields(
                        "ratio_first_derivative",
                        geometry["ratio_first_derivative"],
                    ),
                    **complex_fields(
                        "ratio_second_derivative",
                        geometry["ratio_second_derivative"],
                    ),
                    "source_z_e_relative_difference": relative_difference(
                        geometry["z_e"], source_z_e
                    ),
                    "source_z1_relative_difference": relative_difference(
                        geometry["z1"], source_z1
                    ),
                }
            )
            c0 = center["C0"]
            c0_e = c0_e_result["value"]
            c1 = c1_result["value"]
            ratio_first = geometry["ratio_first_derivative"]
            ratio_second = geometry["ratio_second_derivative"]
            log_sign = mp.mpf(configuration["log_sign"])
            c0_e_term = -log_sign * c0_e * ratio_first
            geometry_term = -log_sign * c0 * ratio_second / 2
            c1_term = log_sign * c1 * ratio_first**2 / 2
            c_log_event = c0_e_term + geometry_term + c1_term
            c_log_radius = (
                abs(ratio_first) * c0_e_result["radius"]
                + abs(ratio_second) * center["radius"] / 2
                + abs(ratio_first**2) * c1_result["radius"] / 2
            )
            source_A = complex_from_row(zero_source, "A_event_zero")
            source_A_radius = mp.mpf(zero_source["A_event_zero_disk_radius"])
            quotient_points: list[tuple[Any, Any, Any]] = []
            for level in range(C0_EPSILON_LEVELS):
                epsilon = mp.mpf(C0_EPSILON_INITIAL_STEP) / mp.power(2, level)
                continued_coordinate = continued_event_coordinate(
                    configuration, epsilon, coordinate
                )
                continued_C0 = parent_C0(
                    configuration,
                    epsilon,
                    continued_coordinate,
                    component,
                    physical_multiplier,
                )
                continued_gap = gap_value(
                    configuration, epsilon, continued_coordinate
                )
                continued_z1 = sigma * mp.diff(
                    lambda value: gap_value(configuration, epsilon, value),
                    continued_coordinate,
                )
                continued_ratio = continued_gap / continued_z1
                continued_H = -log_sign * (
                    continued_C0["C0"] * continued_ratio
                    - c1 * continued_ratio**2 / 2
                )
                continued_K = continued_H / epsilon
                quotient_estimator = (continued_K - source_A) / epsilon
                quotient_radius = (
                    abs(continued_ratio) * continued_C0["radius"]
                    + abs(continued_ratio**2) * c1_result["radius"] / 2
                ) / epsilon**2 + source_A_radius / epsilon
                quotient_points.append(
                    (epsilon, quotient_estimator, quotient_radius)
                )
                source_coordinate: Any = ""
                source_coordinate_disk: Any = ""
                source_coordinate_distance: Any = ""
                source_coordinate_normalized_distance: Any = ""
                if level == 0:
                    atlas_source = next(
                        row
                        for row in read_csv(ATLAS_5377)
                        if row["event_id"] == configuration["event_id"]
                        and row["epsilon_id"] == "E000625"
                    )
                    source_coordinate = atlas_source["event_coordinate"]
                    source_coordinate_disk = atlas_source["coordinate_disk_radius"]
                    source_coordinate_distance = abs(
                        continued_coordinate - mp.mpf(source_coordinate)
                    )
                    source_coordinate_normalized_distance = (
                        source_coordinate_distance
                        / mp.mpf(source_coordinate_disk)
                    )
                continued_quotient_sequence.append(
                    {
                        "event_id": configuration["event_id"],
                        "level": level,
                        "positive_epsilon": mp_text(epsilon),
                        "continued_event_coordinate": mp_text(
                            continued_coordinate
                        ),
                        "historical_source_coordinate": source_coordinate,
                        "historical_source_coordinate_disk": source_coordinate_disk,
                        "historical_coordinate_distance": (
                            mp_text(source_coordinate_distance)
                            if source_coordinate_distance != ""
                            else ""
                        ),
                        "historical_coordinate_normalized_distance": (
                            mp_text(source_coordinate_normalized_distance)
                            if source_coordinate_normalized_distance != ""
                            else ""
                        ),
                        **complex_fields("continued_gap", continued_gap),
                        **complex_fields("continued_z1", continued_z1),
                        **complex_fields("continued_ratio", continued_ratio),
                        **complex_fields("continued_C0", continued_C0["C0"]),
                        "continued_C0_radius": mp_text(continued_C0["radius"]),
                        **complex_fields("continued_H", continued_H),
                        **complex_fields("continued_K", continued_K),
                        **complex_fields("C_log_quotient_estimator", quotient_estimator),
                        "C_log_quotient_estimator_radius": mp_text(
                            quotient_radius
                        ),
                    }
                )
            quotient_result = extrapolated_value(
                quotient_points, C0_EPSILON_EXTRAPOLATION_ORDER
            )
            finite_c1_reference = robust_finite_C1_reference(
                configuration["event_id"]
            )
            decomposition_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "term_id": configuration["term_id"],
                    "primary_surface_id": configuration["surface_id"],
                    "log_sign": configuration["log_sign"],
                    "trace_orientation": configuration["trace_orientation"],
                    "source_winding": center["winding"],
                    **complex_fields("C0_zero", c0),
                    "C0_zero_radius": mp_text(center["radius"]),
                    "C0_zero_source_relative_difference": relative_difference(
                        c0, complex_from_row(zero_source, "C0_zero")
                    ),
                    **complex_fields("C0_e_zero", c0_e),
                    "C0_e_zero_radius": mp_text(c0_e_result["radius"]),
                    "C0_e_maximum_window_shift": mp_text(
                        c0_e_result["maximum_window_shift"]
                    ),
                    "E000625_parent_to_finite_C0_relative_difference": finite_crosscheck_difference,
                    **complex_fields("C1_zero", c1),
                    "C1_zero_radius": mp_text(c1_result["radius"]),
                    "C1_zero_maximum_window_shift": mp_text(
                        c1_result["maximum_window_shift"]
                    ),
                    "robust_finite_rung_C1_real_reference": mp_text(
                        finite_c1_reference
                    ),
                    "C1_to_finite_reference_relative_difference": relative_difference(
                        mp.re(c1), finite_c1_reference
                    ),
                    **complex_fields(
                        "ratio_first_derivative",
                        geometry["ratio_first_derivative"],
                    ),
                    **complex_fields(
                        "ratio_second_derivative",
                        geometry["ratio_second_derivative"],
                    ),
                    **complex_fields("C_log_C0_e_term", c0_e_term),
                    **complex_fields("C_log_geometry_term", geometry_term),
                    **complex_fields("C_log_C1_term", c1_term),
                    **complex_fields("C_log_event", c_log_event),
                    "C_log_event_diagnostic_radius": mp_text(c_log_radius),
                    **complex_fields(
                        "C_log_continued_quotient", quotient_result["value"]
                    ),
                    "C_log_continued_quotient_radius": mp_text(
                        quotient_result["radius"]
                    ),
                    "formula_to_continued_quotient_distance": mp_text(
                        abs(c_log_event - quotient_result["value"])
                    ),
                    "formula_and_continued_quotient_disks_overlap": (
                        abs(c_log_event - quotient_result["value"])
                        <= c_log_radius + quotient_result["radius"]
                    ),
                }
            )
    finally:
        M5359.M5342.M5326.restore_kernel(old_kernel)

    c_log_total = sum(
        (complex_from_row(row, "C_log_event") for row in decomposition_rows),
        mp.mpc(0),
    )
    c_log_radius = sum(
        (mp.mpf(row["C_log_event_diagnostic_radius"]) for row in decomposition_rows),
        mp.mpf(0),
    )
    total_quotient_points: list[tuple[Any, Any, Any]] = []
    for level in range(C0_EPSILON_LEVELS):
        local_rows = [
            row
            for row in continued_quotient_sequence
            if row["event_id"] != "TOTAL" and int(row["level"]) == level
        ]
        epsilon = mp.mpf(local_rows[0]["positive_epsilon"])
        total_estimator = sum(
            (
                complex_from_row(row, "C_log_quotient_estimator")
                for row in local_rows
            ),
            mp.mpc(0),
        )
        total_radius = sum(
            (
                mp.mpf(row["C_log_quotient_estimator_radius"])
                for row in local_rows
            ),
            mp.mpf(0),
        )
        total_quotient_points.append((epsilon, total_estimator, total_radius))
        continued_quotient_sequence.append(
            {
                "event_id": "TOTAL",
                "level": level,
                "positive_epsilon": mp_text(epsilon),
                **complex_fields("C_log_quotient_estimator", total_estimator),
                "C_log_quotient_estimator_radius": mp_text(total_radius),
            }
        )
    total_quotient_result = extrapolated_value(
        total_quotient_points, C0_EPSILON_EXTRAPOLATION_ORDER
    )
    formula_to_quotient_distance = abs(
        c_log_total - total_quotient_result["value"]
    )
    result_5377 = read_json(RESULT_5377)
    c_candidate = mp.mpc(
        result_5377["C_log_candidate_real"],
        result_5377["C_log_candidate_imaginary"],
    )
    c_candidate_disk = mp.mpf(str(result_5377["C_log_candidate_diagnostic_disk"]))
    direct_distance = abs(c_log_total - c_candidate)
    result_5359 = read_json(RESULT_5359)
    source_A = complex(
        float(result_5359["A_total_zero_real"]),
        float(result_5359["A_total_zero_imaginary"]),
    )
    source_A_radius = float(result_5359["A_total_zero_disk_radius"])
    corrected_inputs = M5377.M5373.load_inputs()
    corrected_AC = M5377.fixed_AC_fit(
        corrected_inputs,
        source_A,
        source_A_radius,
        complex(float(mp.re(c_log_total)), float(mp.im(c_log_total))),
        float(c_log_radius),
    )
    corrected_fit_rows = [
        {
            "fit_id": "FIXED_DERIVED_A_DIRECT_PARENT_C",
            **complex_fields("A_fixed", source_A),
            "A_fixed_radius": source_A_radius,
            **complex_fields("C_fixed", c_log_total),
            "C_fixed_radius": mp_text(c_log_radius),
            **complex_fields("intercept", corrected_AC["intercept"]),
            "input_disk": corrected_AC["input_disk"],
            "correlated_A_disk": corrected_AC["a_disk"],
            "correlated_C_disk": corrected_AC["c_disk"],
            "leave_one_out_spread": corrected_AC["loo_spread"],
            "weighted_to_unweighted_shift": corrected_AC["weight_shift"],
            "maximum_residual": corrected_AC["maximum_residual"],
            "maximum_normalized_residual": corrected_AC[
                "maximum_normalized_residual"
            ],
            "intercept_envelope": corrected_AC["envelope"],
            "relative_intercept_envelope": corrected_AC["relative_envelope"],
        }
    ]
    corrected_residual_rows = [
        {
            "epsilon_id": source["epsilon_id"],
            "epsilon": source["epsilon"],
            **complex_fields("observed", source["value"]),
            **complex_fields("predicted", prediction),
            **complex_fields("residual", residual),
            "input_radius": source["radius"],
            "normalized_residual": abs(residual) / source["radius"],
        }
        for source, prediction, residual in zip(
            corrected_inputs,
            corrected_AC["predictions"],
            corrected_AC["residuals"],
        )
    ]
    max_zero_C0_difference = max(
        row["C0_zero_source_relative_difference"] for row in decomposition_rows
    )
    max_finite_C0_difference = max(
        row["E000625_parent_to_finite_C0_relative_difference"]
        for row in decomposition_rows
    )
    max_C1_reference_difference = max(
        row["C1_to_finite_reference_relative_difference"]
        for row in decomposition_rows
    )
    max_z_e_difference = max(
        row["source_z_e_relative_difference"] for row in geometry_rows
    )
    max_z1_difference = max(
        row["source_z1_relative_difference"] for row in geometry_rows
    )
    max_curvature_difference = max(
        row["event_curvature_relative_difference"] for row in geometry_rows
    )
    maximum_historical_coordinate_normalized_distance = max(
        mp.mpf(row["historical_coordinate_normalized_distance"])
        for row in continued_quotient_sequence
        if row.get("historical_coordinate_normalized_distance") not in (None, "")
    )
    max_c0_e_real_ratio = max(
        abs(mp.mpf(row["C0_e_zero_real"]))
        / max(abs(mp.mpf(row["C0_e_zero_imaginary"])), mp.mpf("1e-300"))
        for row in decomposition_rows
    )
    max_c1_imaginary_ratio = max(
        abs(mp.mpf(row["C1_zero_imaginary"]))
        / max(abs(mp.mpf(row["C1_zero_real"])), mp.mpf("1e-300"))
        for row in decomposition_rows
    )
    validations = [
        validation_row("preflight_passes", preflight_result["all_pass"], preflight_result["checks"]),
        validation_row("all_eight_event_decompositions_are_present", [row["event_id"] for row in decomposition_rows] == list(EVENT_IDS), len(decomposition_rows)),
        validation_row("complex_trace_extension_reproduces_zero_parent_C0", max_zero_C0_difference <= 1.0e-18, max_zero_C0_difference),
        validation_row("complex_trace_extension_matches_smallest_finite_normal_forms", max_finite_C0_difference <= 5.0e-4, max_finite_C0_difference),
        validation_row("zero_C1_matches_robust_finite_rung_references", max_C1_reference_difference <= 5.0e-3, max_C1_reference_difference),
        validation_row("zero_C1_is_real_within_numerical_sequences", max_c1_imaginary_ratio <= mp.mpf("1e-18"), mp_text(max_c1_imaginary_ratio)),
        validation_row("zero_C0_e_is_imaginary_within_numerical_sequences", max_c0_e_real_ratio <= mp.mpf("1e-8"), mp_text(max_c0_e_real_ratio)),
        validation_row("implicit_geometry_reproduces_source_z_e", max_z_e_difference <= 1.0e-25, max_z_e_difference),
        validation_row("implicit_geometry_reproduces_source_z1", max_z1_difference <= 1.0e-25, max_z1_difference),
        validation_row("sampled_atlas_is_recorded_as_topology_grade_not_second_derivative_grade", maximum_historical_coordinate_normalized_distance > 1, f"maximum_E000625_coordinate_distance_over_historical_disk={mp_text(maximum_historical_coordinate_normalized_distance)};curvature_difference={max_curvature_difference}"),
        validation_row("all_parent_C_log_events_are_finite", all(finite_complex(complex_from_row(row, "C_log_event")) for row in decomposition_rows), [row["event_id"] for row in decomposition_rows]),
        validation_row("each_parent_derivative_formula_agrees_with_its_continued_root_quotient", all(parse_bool(row["formula_and_continued_quotient_disks_overlap"]) for row in decomposition_rows), [(row["event_id"], row["formula_to_continued_quotient_distance"], row["C_log_continued_quotient_radius"]) for row in decomposition_rows]),
        validation_row("summed_parent_derivative_formula_agrees_with_continued_root_quotient", formula_to_quotient_distance <= c_log_radius + total_quotient_result["radius"], f"distance={mp_text(formula_to_quotient_distance)};combined_radius={mp_text(c_log_radius + total_quotient_result['radius'])}"),
        validation_row("corrected_fixed_A_C_fit_remains_inside_one_percent_envelope", corrected_AC["relative_envelope"] <= 0.01, corrected_AC["relative_envelope"]),
        validation_row("historical_5377_candidate_is_not_used_as_a_zero_derivative_gate", direct_distance > c_candidate_disk + c_log_radius, f"historical_distance={mp_text(direct_distance)};historical_combined_radius={mp_text(c_candidate_disk + c_log_radius)}"),
        validation_row("strict_limit_and_downstream_claims_remain_false", all(value is False for value in strict_open_claims().values()), strict_open_claims()),
        validation_row("formal_workbench_remains_unchanged", M5359.M5342.M5283.formal_inventory_digest() == M5359.M5342.FORMAL_DIGEST, M5359.M5342.M5283.formal_inventory_digest()),
        validation_row("scripts_cache_remains_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_TRACE: passed,
        CLAIM_C1: passed,
        CLAIM_GEOMETRY: passed,
        CLAIM_C_NUMERIC: passed,
    }
    for rows in (
        c1_sequence,
        c0_epsilon_sequence,
        continued_quotient_sequence,
        geometry_rows,
        decomposition_rows,
        corrected_fit_rows,
        corrected_residual_rows,
        registered_sources,
    ):
        for row in rows:
            row.update(claims)
            row.update(strict_open_claims())
    contracts = contract_rows(claims)
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_ZERO_PARENT_C_DERIVATIVE_NUMERICALLY_DERIVED__BUILD_COMMON_INTERVAL_ENCLOSURE"
            if passed
            else "D4_ZERO_PARENT_C_DERIVATIVE_DECOMPOSITION_BLOCKED"
        ),
        "event_count": len(decomposition_rows),
        **{key: value for key, value in complex_fields("C_log_zero_parent", c_log_total).items()},
        "C_log_zero_parent_diagnostic_radius": float(c_log_radius),
        "C_log_5377_candidate_real": float(mp.re(c_candidate)),
        "C_log_5377_candidate_imaginary": float(mp.im(c_candidate)),
        "C_log_5377_candidate_disk": float(c_candidate_disk),
        "direct_to_5377_candidate_distance": float(direct_distance),
        **{
            key: value
            for key, value in complex_fields(
                "C_log_continued_quotient", total_quotient_result["value"]
            ).items()
        },
        "C_log_continued_quotient_radius": float(
            total_quotient_result["radius"]
        ),
        "formula_to_continued_quotient_distance": float(
            formula_to_quotient_distance
        ),
        "corrected_fixed_A_C_intercept_real": float(
            corrected_AC["intercept"].real
        ),
        "corrected_fixed_A_C_intercept_imaginary": float(
            corrected_AC["intercept"].imag
        ),
        "corrected_fixed_A_C_maximum_normalized_residual": corrected_AC[
            "maximum_normalized_residual"
        ],
        "corrected_fixed_A_C_relative_intercept_envelope": corrected_AC[
            "relative_envelope"
        ],
        "maximum_zero_C0_source_relative_difference": max_zero_C0_difference,
        "maximum_E000625_parent_to_finite_C0_relative_difference": max_finite_C0_difference,
        "maximum_C1_to_finite_reference_relative_difference": max_C1_reference_difference,
        "maximum_source_z_e_relative_difference": max_z_e_difference,
        "maximum_source_z1_relative_difference": max_z1_difference,
        "maximum_event_curvature_relative_difference": max_curvature_difference,
        "maximum_historical_coordinate_normalized_distance": float(
            maximum_historical_coordinate_normalized_distance
        ),
        "claim_boundary": {**claims, **strict_open_claims()},
        "remaining_obstruction": "replace convergent derivative disks by interval enclosures on one common closed complex event neighborhood, then use them in H3 before bounding mapped-away W3",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_zero_parent_C_derivative_contract.csv", contracts)
    atomic_csv(output / "D4_zero_parent_C1_trace_sequence.csv", c1_sequence)
    atomic_csv(output / "D4_zero_parent_C0_epsilon_sequence.csv", c0_epsilon_sequence)
    atomic_csv(output / "D4_zero_parent_continued_root_quotient.csv", continued_quotient_sequence)
    atomic_csv(output / "D4_zero_parent_geometry_derivatives.csv", geometry_rows)
    atomic_csv(output / "D4_zero_parent_C_log_event_decomposition.csv", decomposition_rows)
    atomic_csv(output / "D4_corrected_fixed_A_C_fit.csv", corrected_fit_rows)
    atomic_csv(output / "D4_corrected_fixed_A_C_residuals.csv", corrected_residual_rows)
    atomic_csv(output / "D4_zero_parent_C_derivative_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_zero_parent_C_derivative_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result, decomposition_rows)
    return result


def self_test() -> dict[str, Any]:
    mp.mp.dps = 70
    target, q_value = target_and_q(mp.mpf(0))
    q_first = mp.diff(lambda epsilon: target_and_q(epsilon)[1], 0)
    q_second = mp.diff(lambda epsilon: target_and_q(epsilon)[1], 0, 2)
    points = [
        (mp.mpf(value), 3 + 2 * mp.mpf(value) - 5 * mp.mpf(value) ** 2, mp.mpf("1e-40"))
        for value in ("0.1", "0.05", "0.025")
    ]
    intercept, radius = polynomial_intercept_with_radius(points)
    checks = {
        "target_zero_is_minus_nine": target == -9,
        "q_zero_is_minus_five_over_four": q_value == -mp.mpf(5) / 4,
        "q_first_is_minus_i_over_32": abs(q_first + 1j / 32) <= mp.mpf("1e-60"),
        "q_second_is_one_over_128": abs(q_second - mp.mpf(1) / 128) <= mp.mpf("1e-60"),
        "polynomial_intercept_is_exact": abs(intercept - 3) <= mp.mpf("1e-60"),
        "radius_propagates": radius > 0,
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        result = preflight()
    else:
        result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("all_pass", result.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
