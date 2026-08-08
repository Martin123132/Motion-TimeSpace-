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
import sympy as sp
from scipy.optimize import least_squares


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5272"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5271 = (
    SCRIPTS / "Y5_R2FR_5271_soft_energy_boundary_surface_oracle.py"
)
RESULT_5271 = (
    FUNCTIONAL_RG
    / "5271"
    / "soft_energy_boundary_surface_oracle_result.json"
)
VALIDATION_5271 = (
    FUNCTIONAL_RG
    / "5271"
    / "soft_energy_boundary_surface_oracle_validation.csv"
)
RAW_5271 = (
    FUNCTIONAL_RG / "5271" / "soft_energy_raw_boundaries.csv"
)
EVENTS_5271 = (
    FUNCTIONAL_RG / "5271" / "soft_energy_surface_topology_events.csv"
)
DESCRIPTORS_5270 = (
    FUNCTIONAL_RG / "5270" / "shared_cycle_boundary_descriptors.csv"
)

DRY_RUN = SOURCE / "exact_analytic_surface_dry_run.json"
SURFACES = SOURCE / "analytic_surface_descriptors.csv"
RAW_REPRODUCTION = SOURCE / "raw_boundary_analytic_reproduction.csv"
LADDER_REPRODUCTION = SOURCE / "analytic_ladder_root_reproduction.csv"
FOLD_CANDIDATES = SOURCE / "fold_resultant_candidate_ledger.csv"
ENDPOINT_EVENTS = SOURCE / "exact_endpoint_events.csv"
FOLD_EVENTS = SOURCE / "resultant_isolated_fold_events.csv"
CROSSING_CANDIDATES = SOURCE / "crossing_resultant_candidate_ledger.csv"
CROSSING_EVENTS = SOURCE / "resultant_isolated_surface_crossings.csv"
EVENT_BALANCE = SOURCE / "event_count_balance.csv"
RECONCILIATION = SOURCE / "5271_event_reconciliation.csv"
RESULT = SOURCE / "exact_analytic_boundary_surface_result.json"
VALIDATION = SOURCE / "exact_analytic_boundary_surface_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5272_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5272-Y5-R2FR-exact-analytic-boundary-surface-and-event-solver.md"
)

CHECKPOINT = 5272
PARENT_CHECKPOINT = 5271
MARKER = "MTS_5272_EXACT_ANALYTIC_BOUNDARY_SURFACE_AND_EVENT_SOLVER"
REVISION = "exact-analytic-boundary-surface-and-event-solver-v1"
ROOT_COORDINATE_TOLERANCE = 2.0e-7
RAW_EQUATION_TOLERANCE = 2.0e-7
EVENT_RESIDUAL_TOLERANCE = 2.0e-9
RESULTANT_ROOT_IMAGINARY_TOLERANCE = 2.0e-8
SOLUTION_DEDUPLICATION_TOLERANCE = 2.0e-7
DOMAIN_TOLERANCE = 2.0e-9
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)

U_SYMBOL, Q_SYMBOL = sp.symbols("u q")


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5271 = load_module("mts_5271_for_5272", SCRIPT_5271)
M5270 = M5271.M5270
M5269 = M5271.M5269
M5267 = M5271.M5267


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
        SCRIPT_5271,
        RESULT_5271,
        VALIDATION_5271,
        RAW_5271,
        EVENTS_5271,
        DESCRIPTORS_5270,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5271.formal_inventory_digest())


def target_from_label(root_label: str) -> float:
    reference = float(M5270.M5028.REFERENCE_COSINE.real)
    if root_label.startswith("plus_"):
        return reference
    if root_label.startswith("minus_"):
        return -reference
    raise ValueError(f"unrecognized root label: {root_label}")


def source_sign(source_name: str) -> int | None:
    if source_name == "direct:g1":
        return 1
    if source_name == "direct:g2":
        return -1
    return None


def surface_key(
    source_name: str,
    target: float,
    chamber_midpoint: float,
) -> str:
    return (
        f"{source_name}|t={target:+.12g}|"
        f"phi={chamber_midpoint:.16g}"
    )


def surface_rows() -> list[dict[str, Any]]:
    descriptors = read_csv(DESCRIPTORS_5270)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for descriptor in descriptors:
        target = target_from_label(descriptor["root_label"])
        midpoint = float(descriptor["chamber_midpoint"])
        grouped[
            surface_key(descriptor["source_name"], target, midpoint)
        ].append(descriptor)
    rows: list[dict[str, Any]] = []
    for key, owners in sorted(grouped.items()):
        source_name = owners[0]["source_name"]
        target = target_from_label(owners[0]["root_label"])
        midpoint = float(owners[0]["chamber_midpoint"])
        sign = source_sign(source_name)
        if sign is not None:
            family = "boosted_hard_leg"
            boundary_law = "F_s,t(q,a,d)=0"
        elif source_name == "direct:g3":
            family = "static_soft_direction"
            boundary_law = "a=t"
        elif source_name == "subtraction:decay":
            family = "static_decay_direction"
            boundary_law = "d=t"
        else:
            raise RuntimeError(
                f"unhandled source family: {source_name}"
            )
        rows.append(
            {
                "surface_key": key,
                "source_name": source_name,
                "family": family,
                "hard_leg_sign": "" if sign is None else sign,
                "target_cosine": target,
                "chamber_midpoint": midpoint,
                "relative_azimuth_cosine": math.cos(midpoint),
                "owner_descriptor_count": len(owners),
                "owner_components": "|".join(
                    sorted(
                        {
                            owner["component_id"]
                            for owner in owners
                        }
                    )
                ),
                "owner_roles": "|".join(
                    sorted({owner["role"] for owner in owners})
                ),
                "root_labels": "|".join(
                    sorted(
                        {
                            owner["root_label"]
                            for owner in owners
                        }
                    )
                ),
                "boundary_law": boundary_law,
                "valid_for_exact_boundary_law": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def surface_lookup(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    return {str(row["surface_key"]): row for row in rows}


def relative_cosine(
    soft_cosine: float,
    decay_cosine: float,
    midpoint: float,
) -> float:
    soft_sine = math.sqrt(max(0.0, 1.0 - soft_cosine**2))
    decay_sine = math.sqrt(max(0.0, 1.0 - decay_cosine**2))
    return (
        soft_cosine * decay_cosine
        + soft_sine
        * decay_sine
        * math.cos(midpoint)
    )


def hard_boundary_coefficients(
    soft_cosine: float,
    decay_cosine: float,
    sign: int,
    target: float,
    midpoint: float,
) -> tuple[float, float, float]:
    relative = relative_cosine(
        soft_cosine, decay_cosine, midpoint
    )
    coefficient_q2 = (
        (soft_cosine - target) * (1.0 + sign * relative)
    )
    coefficient_q1 = (
        2.0 * sign * (decay_cosine - soft_cosine * relative)
    )
    coefficient_q0 = (
        (soft_cosine + target) * (sign * relative - 1.0)
    )
    return coefficient_q2, coefficient_q1, coefficient_q0


def hard_boundary_value(
    q_value: float,
    soft_cosine: float,
    decay_cosine: float,
    sign: int,
    target: float,
    midpoint: float,
) -> float:
    coefficient_q2, coefficient_q1, coefficient_q0 = (
        hard_boundary_coefficients(
            soft_cosine,
            decay_cosine,
            sign,
            target,
            midpoint,
        )
    )
    return (
        coefficient_q2 * q_value**2
        + coefficient_q1 * q_value
        + coefficient_q0
    )


def hard_boundary_coordinate_derivative(
    direction: str,
    q_value: float,
    soft_cosine: float,
    decay_cosine: float,
    sign: int,
    target: float,
    midpoint: float,
) -> float:
    soft_sine = math.sqrt(max(1.0e-30, 1.0 - soft_cosine**2))
    decay_sine = math.sqrt(max(1.0e-30, 1.0 - decay_cosine**2))
    cosine_midpoint = math.cos(midpoint)
    relative = (
        soft_cosine * decay_cosine
        + soft_sine * decay_sine * cosine_midpoint
    )
    relative_soft_derivative = (
        decay_cosine
        - soft_cosine
        * decay_sine
        * cosine_midpoint
        / soft_sine
    )
    relative_decay_derivative = (
        soft_cosine
        - decay_cosine
        * soft_sine
        * cosine_midpoint
        / decay_sine
    )
    if direction == "soft_cosine":
        return (
            (
                1.0
                + sign * relative
                + sign
                * (soft_cosine - target)
                * relative_soft_derivative
            )
            * q_value**2
            + 2.0
            * sign
            * (
                -relative
                - soft_cosine * relative_soft_derivative
            )
            * q_value
            + (
                sign * relative
                - 1.0
                + sign
                * (soft_cosine + target)
                * relative_soft_derivative
            )
        )
    if direction == "decay_cosine":
        return (
            sign
            * (soft_cosine - target)
            * relative_decay_derivative
            * q_value**2
            + 2.0
            * sign
            * (
                1.0
                - soft_cosine * relative_decay_derivative
            )
            * q_value
            + sign
            * (soft_cosine + target)
            * relative_decay_derivative
        )
    raise ValueError(f"unsupported direction: {direction}")


def hard_denominator(
    q_value: float,
    soft_cosine: float,
    decay_cosine: float,
    sign: int,
    midpoint: float,
) -> float:
    relative = relative_cosine(
        soft_cosine, decay_cosine, midpoint
    )
    return (
        1.0
        + q_value**2
        - sign * (1.0 - q_value**2) * relative
    )


def quadratic_real_roots(
    coefficient_q2: float,
    coefficient_q1: float,
    coefficient_q0: float,
) -> list[float]:
    scale = max(
        abs(coefficient_q2),
        abs(coefficient_q1),
        abs(coefficient_q0),
        1.0,
    )
    if abs(coefficient_q2) <= 1.0e-14 * scale:
        if abs(coefficient_q1) <= 1.0e-14 * scale:
            return []
        return [-coefficient_q0 / coefficient_q1]
    discriminant = (
        coefficient_q1**2
        - 4.0 * coefficient_q2 * coefficient_q0
    )
    if discriminant < -1.0e-13 * scale**2:
        return []
    discriminant = max(0.0, discriminant)
    square_root = math.sqrt(discriminant)
    roots = [
        (-coefficient_q1 - square_root)
        / (2.0 * coefficient_q2),
        (-coefficient_q1 + square_root)
        / (2.0 * coefficient_q2),
    ]
    return deduplicate_numbers(roots, 1.0e-11)


def deduplicate_numbers(
    values: list[float], tolerance: float
) -> list[float]:
    result: list[float] = []
    for value in sorted(values):
        if not result or abs(value - result[-1]) > tolerance:
            result.append(value)
    return result


def coordinate_pair(
    direction: str,
    coordinate: float,
    fixed_coordinate: float,
) -> tuple[float, float]:
    if direction == "soft_cosine":
        return coordinate, fixed_coordinate
    if direction == "decay_cosine":
        return fixed_coordinate, coordinate
    raise ValueError(f"unsupported direction: {direction}")


def half_angle_from_cosine(cosine: float) -> float:
    return math.sqrt((1.0 - cosine) / (1.0 + cosine))


def cosine_from_half_angle(half_angle: float) -> float:
    return (1.0 - half_angle**2) / (1.0 + half_angle**2)


def exact_rational(value: float) -> sp.Rational:
    return sp.Rational(str(float(value)))


def quartic_expression(
    direction: str,
    fixed_coordinate: float,
    surface: dict[str, Any],
) -> sp.Expr:
    sign = int(surface["hard_leg_sign"])
    target = exact_rational(float(surface["target_cosine"]))
    midpoint = float(surface["chamber_midpoint"])
    if abs(math.cos(midpoint) + 1.0) > 1.0e-14:
        raise RuntimeError(
            "5272 exact quartic currently requires phi=pi"
        )
    denominator = 1 + U_SYMBOL**2
    cosine_numerator = 1 - U_SYMBOL**2
    sine_numerator = 2 * U_SYMBOL
    if direction == "soft_cosine":
        decay = exact_rational(fixed_coordinate)
        decay_sine = sp.sqrt(1 - decay**2)
        soft_numerator = cosine_numerator
        relative_numerator = (
            soft_numerator * decay
            - sine_numerator * decay_sine
        )
        expression = (
            (soft_numerator - target * denominator)
            * (denominator + sign * relative_numerator)
            * Q_SYMBOL**2
            + 2
            * sign
            * (
                decay * denominator**2
                - soft_numerator * relative_numerator
            )
            * Q_SYMBOL
            + (soft_numerator + target * denominator)
            * (sign * relative_numerator - denominator)
        )
    elif direction == "decay_cosine":
        soft = exact_rational(fixed_coordinate)
        soft_sine = sp.sqrt(1 - soft**2)
        decay_numerator = cosine_numerator
        relative_numerator = (
            soft * decay_numerator
            - soft_sine * sine_numerator
        )
        expression = denominator * (
            (soft - target)
            * (denominator + sign * relative_numerator)
            * Q_SYMBOL**2
            + 2
            * sign
            * (decay_numerator - soft * relative_numerator)
            * Q_SYMBOL
            + (soft + target)
            * (sign * relative_numerator - denominator)
        )
    else:
        raise ValueError(f"unsupported direction: {direction}")
    return sp.expand(expression)


def remove_exact_factor(
    polynomial: sp.Poly,
    factor: sp.Poly,
) -> tuple[sp.Poly, int]:
    removed = 0
    while polynomial.degree() >= factor.degree():
        quotient, remainder = sp.div(polynomial, factor)
        if not remainder.is_zero:
            break
        polynomial = quotient
        removed += 1
    return polynomial, removed


def polynomial_real_roots(
    polynomial: sp.Poly,
    imaginary_tolerance: float,
) -> list[float]:
    if polynomial.degree() <= 0:
        return []
    try:
        roots = sp.nroots(
            polynomial.as_expr(),
            n=24,
            maxsteps=1200,
        )
        values = [
            float(sp.re(root))
            for root in roots
            if abs(float(sp.im(root))) <= imaginary_tolerance
        ]
    except Exception:
        coefficients = np.asarray(
            [
                complex(sp.N(coefficient, 30))
                for coefficient in polynomial.all_coeffs()
            ],
            dtype=np.complex128,
        )
        roots = np.roots(coefficients)
        values = [
            float(root.real)
            for root in roots
            if abs(root.imag) <= imaginary_tolerance
        ]
    return deduplicate_numbers(values, 2.0e-9)


def numeric_u_roots(
    expression: sp.Expr,
    q_value: float,
) -> list[complex]:
    polynomial = sp.Poly(
        expression.subs(Q_SYMBOL, sp.Float(q_value, 30)),
        U_SYMBOL,
    )
    coefficients = np.asarray(
        [
            complex(sp.N(coefficient, 30))
            for coefficient in polynomial.all_coeffs()
        ],
        dtype=np.complex128,
    )
    scale = max(float(np.max(np.abs(coefficients))), 1.0)
    first = 0
    while (
        first < len(coefficients) - 1
        and abs(coefficients[first]) <= 1.0e-13 * scale
    ):
        first += 1
    return list(np.roots(coefficients[first:]))


def hard_coordinate_roots(
    expression: sp.Expr,
    q_value: float,
) -> list[float]:
    lower = -float(M5270.ANGULAR_LIMIT)
    upper = float(M5270.ANGULAR_LIMIT)
    u_minimum = half_angle_from_cosine(upper)
    u_maximum = half_angle_from_cosine(lower)
    coordinates: list[float] = []
    for root in numeric_u_roots(expression, q_value):
        if abs(root.imag) > 2.0e-7:
            continue
        half_angle = float(root.real)
        if (
            half_angle < u_minimum - 1.0e-7
            or half_angle > u_maximum + 1.0e-7
        ):
            continue
        coordinate = cosine_from_half_angle(half_angle)
        if lower - 1.0e-7 <= coordinate <= upper + 1.0e-7:
            coordinates.append(coordinate)
    return deduplicate_numbers(
        coordinates, ROOT_COORDINATE_TOLERANCE
    )


def raw_surface_key(
    row: dict[str, str],
) -> str:
    root_label = row["full_label"].rsplit(":", 1)[1]
    return surface_key(
        row["full_label"].rsplit(":", 1)[0],
        target_from_label(root_label),
        float(row["chamber_midpoint"]),
    )


def raw_reproduction_rows(
    surfaces: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw in read_csv(RAW_5271):
        key = raw_surface_key(raw)
        surface = surfaces[key]
        direction = raw["direction"]
        coordinate = float(raw["boundary_coordinate"])
        fixed = float(raw["fixed_coordinate"])
        soft_cosine, decay_cosine = coordinate_pair(
            direction, coordinate, fixed
        )
        energy = float(raw["energy_witness"])
        q_value = math.sqrt(1.0 - energy)
        if surface["family"] == "boosted_hard_leg":
            sign = int(surface["hard_leg_sign"])
            target = float(surface["target_cosine"])
            midpoint = float(surface["chamber_midpoint"])
            equation_residual = abs(
                hard_boundary_value(
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    sign,
                    target,
                    midpoint,
                )
            )
            coefficients = hard_boundary_coefficients(
                soft_cosine,
                decay_cosine,
                sign,
                target,
                midpoint,
            )
            candidate_q = [
                value
                for value in quadratic_real_roots(*coefficients)
                if 0.0 <= value <= 1.0
            ]
            energy_residual = min(
                (
                    abs((1.0 - candidate**2) - energy)
                    for candidate in candidate_q
                ),
                default=math.inf,
            )
            denominator = abs(
                hard_denominator(
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    sign,
                    midpoint,
                )
            )
        elif surface["family"] == "static_soft_direction":
            equation_residual = abs(
                soft_cosine - float(surface["target_cosine"])
            )
            energy_residual = 0.0
            denominator = 1.0
        else:
            equation_residual = abs(
                decay_cosine - float(surface["target_cosine"])
            )
            energy_residual = 0.0
            denominator = 1.0
        rows.append(
            {
                "direction": direction,
                "soft_energy": energy,
                "fixed_coordinate": fixed,
                "surface_key": key,
                "component_id": raw["component_id"],
                "role": raw["role"],
                "full_label": raw["full_label"],
                "boundary_coordinate": coordinate,
                "analytic_equation_residual": equation_residual,
                "nearest_quadratic_energy_residual": energy_residual,
                "hard_leg_denominator_magnitude": denominator,
                "reproduced": (
                    equation_residual <= RAW_EQUATION_TOLERANCE
                    and energy_residual <= RAW_EQUATION_TOLERANCE
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def deduplicate_raw_coordinates(
    values: list[float],
) -> list[float]:
    return deduplicate_numbers(
        values, float(M5270.MERGE_COORDINATE_TOLERANCE)
    )


def ladder_reproduction_rows(
    surface_list: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, float, float, str], list[float]],
]:
    raw_groups: dict[
        tuple[str, float, float, str], list[float]
    ] = defaultdict(list)
    for raw in read_csv(RAW_5271):
        key = (
            raw["direction"],
            float(raw["energy_witness"]),
            float(raw["fixed_coordinate"]),
            raw_surface_key(raw),
        )
        raw_groups[key].append(float(raw["boundary_coordinate"]))
    raw_groups = {
        key: deduplicate_raw_coordinates(values)
        for key, values in raw_groups.items()
    }
    result_5271 = read_json(RESULT_5271)
    energies = tuple(float(value) for value in result_5271["energy_nodes"])
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    rows: list[dict[str, Any]] = []
    analytic_groups: dict[
        tuple[str, float, float, str], list[float]
    ] = {}
    for surface in surface_list:
        key = str(surface["surface_key"])
        for direction, fixed_values in (
            ("soft_cosine", decay_nodes),
            ("decay_cosine", soft_nodes),
        ):
            for fixed in fixed_values:
                expression = (
                    quartic_expression(direction, fixed, surface)
                    if surface["family"] == "boosted_hard_leg"
                    else None
                )
                for energy in energies:
                    group_key = (direction, energy, fixed, key)
                    if expression is not None:
                        analytic = hard_coordinate_roots(
                            expression, math.sqrt(1.0 - energy)
                        )
                    elif (
                        surface["family"]
                        == "static_soft_direction"
                        and direction == "soft_cosine"
                    ):
                        analytic = [
                            float(surface["target_cosine"])
                        ]
                    elif (
                        surface["family"]
                        == "static_decay_direction"
                        and direction == "decay_cosine"
                    ):
                        analytic = [
                            float(surface["target_cosine"])
                        ]
                    else:
                        analytic = []
                    expected = raw_groups.get(group_key, [])
                    analytic_groups[group_key] = analytic
                    coordinate_residual = (
                        max(
                            min(
                                abs(value - candidate)
                                for candidate in analytic
                            )
                            for value in expected
                        )
                        if expected and analytic
                        else (
                            0.0
                            if not expected and not analytic
                            else math.inf
                        )
                    )
                    reverse_residual = (
                        max(
                            min(
                                abs(value - candidate)
                                for candidate in expected
                            )
                            for value in analytic
                        )
                        if expected and analytic
                        else (
                            0.0
                            if not expected and not analytic
                            else math.inf
                        )
                    )
                    reproduced = (
                        len(expected) == len(analytic)
                        and coordinate_residual
                        <= ROOT_COORDINATE_TOLERANCE
                        and reverse_residual
                        <= ROOT_COORDINATE_TOLERANCE
                    )
                    rows.append(
                        {
                            "direction": direction,
                            "soft_energy": energy,
                            "fixed_coordinate": fixed,
                            "surface_key": key,
                            "raw_unique_root_count": len(expected),
                            "analytic_root_count": len(analytic),
                            "raw_coordinates": "|".join(
                                f"{value:.16g}" for value in expected
                            ),
                            "analytic_coordinates": "|".join(
                                f"{value:.16g}" for value in analytic
                            ),
                            "raw_to_analytic_maximum_residual": (
                                coordinate_residual
                            ),
                            "analytic_to_raw_maximum_residual": (
                                reverse_residual
                            ),
                            "reproduced": reproduced,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
    return rows, analytic_groups


def q_domain() -> tuple[float, float]:
    minimum_energy = float(M5267.ENERGY_MINIMUM)
    maximum_energy = float(M5267.ENERGY_MAXIMUM)
    return (
        math.sqrt(1.0 - maximum_energy),
        math.sqrt(1.0 - minimum_energy),
    )


def endpoint_event_rows(
    hard_surfaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    q_minimum, q_maximum = q_domain()
    rows: list[dict[str, Any]] = []
    for surface in hard_surfaces:
        sign = int(surface["hard_leg_sign"])
        target = float(surface["target_cosine"])
        midpoint = float(surface["chamber_midpoint"])
        for direction, fixed_values in (
            ("soft_cosine", decay_nodes),
            ("decay_cosine", soft_nodes),
        ):
            for fixed in fixed_values:
                for endpoint in (
                    -float(M5270.ANGULAR_LIMIT),
                    float(M5270.ANGULAR_LIMIT),
                ):
                    soft_cosine, decay_cosine = coordinate_pair(
                        direction, endpoint, fixed
                    )
                    coefficients = hard_boundary_coefficients(
                        soft_cosine,
                        decay_cosine,
                        sign,
                        target,
                        midpoint,
                    )
                    for q_value in quadratic_real_roots(*coefficients):
                        if (
                            q_value < q_minimum - DOMAIN_TOLERANCE
                            or q_value
                            > q_maximum + DOMAIN_TOLERANCE
                        ):
                            continue
                        energy = 1.0 - q_value**2
                        rows.append(
                            {
                                "event_type": "angular_endpoint_crossing",
                                "direction": direction,
                                "fixed_coordinate": fixed,
                                "surface_key": surface["surface_key"],
                                "endpoint_coordinate": endpoint,
                                "q_value": q_value,
                                "soft_energy": energy,
                                "equation_residual": abs(
                                    hard_boundary_value(
                                        q_value,
                                        soft_cosine,
                                        decay_cosine,
                                        sign,
                                        target,
                                        midpoint,
                                    )
                                ),
                                "hard_leg_denominator_magnitude": abs(
                                    hard_denominator(
                                        q_value,
                                        soft_cosine,
                                        decay_cosine,
                                        sign,
                                        midpoint,
                                    )
                                ),
                                "valid_for_exact_algebraic_location": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
    return sorted(
        rows,
        key=lambda row: (
            row["direction"],
            float(row["fixed_coordinate"]),
            str(row["surface_key"]),
            float(row["soft_energy"]),
        ),
    )


def fold_residual_function(
    direction: str,
    fixed: float,
    surface: dict[str, Any],
) -> Callable[[np.ndarray], np.ndarray]:
    sign = int(surface["hard_leg_sign"])
    target = float(surface["target_cosine"])
    midpoint = float(surface["chamber_midpoint"])

    def residual(values: np.ndarray) -> np.ndarray:
        q_value = float(values[0])
        coordinate = float(values[1])
        soft_cosine, decay_cosine = coordinate_pair(
            direction, coordinate, fixed
        )
        return np.asarray(
            [
                hard_boundary_value(
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    sign,
                    target,
                    midpoint,
                ),
                hard_boundary_coordinate_derivative(
                    direction,
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    sign,
                    target,
                    midpoint,
                ),
            ],
            dtype=float,
        )

    return residual


def crossing_residual_function(
    direction: str,
    fixed: float,
    first: dict[str, Any],
    second: dict[str, Any],
) -> Callable[[np.ndarray], np.ndarray]:
    def residual(values: np.ndarray) -> np.ndarray:
        q_value = float(values[0])
        coordinate = float(values[1])
        soft_cosine, decay_cosine = coordinate_pair(
            direction, coordinate, fixed
        )
        return np.asarray(
            [
                hard_boundary_value(
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    int(first["hard_leg_sign"]),
                    float(first["target_cosine"]),
                    float(first["chamber_midpoint"]),
                ),
                hard_boundary_value(
                    q_value,
                    soft_cosine,
                    decay_cosine,
                    int(second["hard_leg_sign"]),
                    float(second["target_cosine"]),
                    float(second["chamber_midpoint"]),
                ),
            ],
            dtype=float,
        )

    return residual


def solution_seeds(
    first_expression: sp.Expr,
    q_value: float,
    second_expression: sp.Expr | None = None,
) -> list[float]:
    lower = -float(M5270.ANGULAR_LIMIT)
    upper = float(M5270.ANGULAR_LIMIT)
    u_minimum = half_angle_from_cosine(upper)
    u_maximum = half_angle_from_cosine(lower)
    first_roots = numeric_u_roots(first_expression, q_value)
    if second_expression is None:
        candidates = first_roots
    else:
        second_roots = numeric_u_roots(second_expression, q_value)
        candidates = []
        for first_root in first_roots:
            nearest = min(
                second_roots,
                key=lambda value: abs(value - first_root),
                default=None,
            )
            if nearest is not None:
                candidates.append(0.5 * (first_root + nearest))
    coordinates: list[float] = []
    for root in candidates:
        if abs(root.imag) > 2.0e-2:
            continue
        half_angle = float(root.real)
        if (
            half_angle < u_minimum - 0.1
            or half_angle > u_maximum + 0.1
        ):
            continue
        coordinates.append(cosine_from_half_angle(half_angle))
    if not coordinates:
        coordinates = list(
            np.linspace(lower, upper, 17, dtype=float)
        )
    return deduplicate_numbers(coordinates, 1.0e-5)


def solve_bounded_system(
    residual: Callable[[np.ndarray], np.ndarray],
    q_seed: float,
    coordinate_seeds: list[float],
) -> tuple[list[tuple[float, float, float]], float]:
    q_minimum, q_maximum = q_domain()
    lower = -float(M5270.ANGULAR_LIMIT)
    upper = float(M5270.ANGULAR_LIMIT)
    solutions: list[tuple[float, float, float]] = []
    nearest_residual = math.inf
    for coordinate_seed in coordinate_seeds:
        fitted = least_squares(
            residual,
            np.asarray(
                [
                    min(max(q_seed, q_minimum), q_maximum),
                    min(max(coordinate_seed, lower), upper),
                ],
                dtype=float,
            ),
            bounds=(
                np.asarray([q_minimum, lower], dtype=float),
                np.asarray([q_maximum, upper], dtype=float),
            ),
            xtol=1.0e-13,
            ftol=1.0e-13,
            gtol=1.0e-13,
            max_nfev=500,
        )
        norm = float(np.linalg.norm(residual(fitted.x), ord=np.inf))
        nearest_residual = min(nearest_residual, norm)
        if not fitted.success or norm > EVENT_RESIDUAL_TOLERANCE:
            continue
        q_value = float(fitted.x[0])
        coordinate = float(fitted.x[1])
        if (
            coordinate <= lower + 5.0e-7
            or coordinate >= upper - 5.0e-7
        ):
            continue
        candidate = (q_value, coordinate, norm)
        if not any(
            abs(q_value - prior[0])
            <= SOLUTION_DEDUPLICATION_TOLERANCE
            and abs(coordinate - prior[1])
            <= SOLUTION_DEDUPLICATION_TOLERANCE
            for prior in solutions
        ):
            solutions.append(candidate)
    return solutions, nearest_residual


def fold_resultant_rows(
    hard_surfaces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    q_minimum, q_maximum = q_domain()
    candidate_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    for surface in hard_surfaces:
        for direction, fixed_values in (
            ("soft_cosine", decay_nodes),
            ("decay_cosine", soft_nodes),
        ):
            for fixed in fixed_values:
                expression = quartic_expression(
                    direction, fixed, surface
                )
                resultant = sp.Poly(
                    sp.resultant(
                        expression,
                        sp.diff(expression, U_SYMBOL),
                        U_SYMBOL,
                    ),
                    Q_SYMBOL,
                    extension=True,
                )
                resultant, removed_q1 = remove_exact_factor(
                    resultant,
                    sp.Poly(
                        Q_SYMBOL - 1,
                        Q_SYMBOL,
                        extension=True,
                    ),
                )
                q_candidates = polynomial_real_roots(
                    resultant,
                    RESULTANT_ROOT_IMAGINARY_TOLERANCE,
                )
                residual = fold_residual_function(
                    direction, fixed, surface
                )
                for q_candidate in q_candidates:
                    if (
                        q_candidate < q_minimum - DOMAIN_TOLERANCE
                        or q_candidate
                        > q_maximum + DOMAIN_TOLERANCE
                    ):
                        disposition = "outside_soft_energy_domain"
                        solutions: list[
                            tuple[float, float, float]
                        ] = []
                        nearest_residual = ""
                    else:
                        seeds = solution_seeds(
                            expression, q_candidate
                        )
                        solutions, nearest = solve_bounded_system(
                            residual, q_candidate, seeds
                        )
                        nearest_residual = nearest
                        disposition = (
                            "physical_interior_fold"
                            if solutions
                            else "projective_or_outside_angular_domain"
                        )
                    candidate_id = (
                        f"FC{len(candidate_rows) + 1:04d}"
                    )
                    candidate_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "direction": direction,
                            "fixed_coordinate": fixed,
                            "surface_key": surface["surface_key"],
                            "resultant_degree_after_q1_removal": (
                                resultant.degree()
                            ),
                            "removed_q_minus_one_multiplicity": (
                                removed_q1
                            ),
                            "candidate_q": q_candidate,
                            "candidate_soft_energy": (
                                1.0 - q_candidate**2
                            ),
                            "disposition": disposition,
                            "solution_count": len(solutions),
                            "nearest_system_residual": nearest_residual,
                            "classified": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
                    for q_value, coordinate, norm in solutions:
                        soft_cosine, decay_cosine = coordinate_pair(
                            direction, coordinate, fixed
                        )
                        event_rows.append(
                            {
                                "event_type": "interior_fold",
                                "candidate_id": candidate_id,
                                "direction": direction,
                                "fixed_coordinate": fixed,
                                "surface_key": surface["surface_key"],
                                "q_value": q_value,
                                "soft_energy": 1.0 - q_value**2,
                                "boundary_coordinate": coordinate,
                                "equation_and_derivative_residual": norm,
                                "hard_leg_denominator_magnitude": abs(
                                    hard_denominator(
                                        q_value,
                                        soft_cosine,
                                        decay_cosine,
                                        int(
                                            surface["hard_leg_sign"]
                                        ),
                                        float(
                                            surface[
                                                "chamber_midpoint"
                                            ]
                                        ),
                                    )
                                ),
                                "valid_for_resultant_isolated_location": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
    event_rows = deduplicate_event_rows(
        event_rows, ("surface_key", "direction", "fixed_coordinate")
    )
    return candidate_rows, event_rows


def deduplicate_event_rows(
    rows: list[dict[str, Any]],
    identity_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in sorted(
        rows,
        key=lambda value: (
            *(str(value[field]) for field in identity_fields),
            float(value["soft_energy"]),
            float(value.get("boundary_coordinate", 0.0)),
        ),
    ):
        if any(
            all(
                str(prior[field]) == str(row[field])
                for field in identity_fields
            )
            and abs(
                float(prior["soft_energy"])
                - float(row["soft_energy"])
            )
            <= SOLUTION_DEDUPLICATION_TOLERANCE
            and abs(
                float(prior.get("boundary_coordinate", 0.0))
                - float(row.get("boundary_coordinate", 0.0))
            )
            <= SOLUTION_DEDUPLICATION_TOLERANCE
            for prior in result
        ):
            continue
        result.append(row)
    return result


def hard_static_crossing_rows(
    hard_surfaces: list[dict[str, Any]],
    static_surfaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    q_minimum, q_maximum = q_domain()
    rows: list[dict[str, Any]] = []
    for direction, fixed_values in (
        ("soft_cosine", decay_nodes),
        ("decay_cosine", soft_nodes),
    ):
        relevant_static = [
            surface
            for surface in static_surfaces
            if (
                direction == "soft_cosine"
                and surface["family"]
                == "static_soft_direction"
            )
            or (
                direction == "decay_cosine"
                and surface["family"]
                == "static_decay_direction"
            )
        ]
        for fixed in fixed_values:
            for hard in hard_surfaces:
                for static in relevant_static:
                    coordinate = float(static["target_cosine"])
                    soft_cosine, decay_cosine = coordinate_pair(
                        direction, coordinate, fixed
                    )
                    coefficients = hard_boundary_coefficients(
                        soft_cosine,
                        decay_cosine,
                        int(hard["hard_leg_sign"]),
                        float(hard["target_cosine"]),
                        float(hard["chamber_midpoint"]),
                    )
                    for q_value in quadratic_real_roots(*coefficients):
                        if (
                            q_value < q_minimum - DOMAIN_TOLERANCE
                            or q_value
                            > q_maximum + DOMAIN_TOLERANCE
                        ):
                            continue
                        rows.append(
                            {
                                "event_type": "hard_static_crossing",
                                "direction": direction,
                                "fixed_coordinate": fixed,
                                "first_surface_key": hard["surface_key"],
                                "second_surface_key": static[
                                    "surface_key"
                                ],
                                "q_value": q_value,
                                "soft_energy": 1.0 - q_value**2,
                                "boundary_coordinate": coordinate,
                                "simultaneous_equation_residual": abs(
                                    hard_boundary_value(
                                        q_value,
                                        soft_cosine,
                                        decay_cosine,
                                        int(
                                            hard["hard_leg_sign"]
                                        ),
                                        float(
                                            hard["target_cosine"]
                                        ),
                                        float(
                                            hard[
                                                "chamber_midpoint"
                                            ]
                                        ),
                                    )
                                ),
                                "valid_for_resultant_isolated_location": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
    return rows


def hard_hard_crossing_rows(
    hard_surfaces: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    q_minimum, q_maximum = q_domain()
    candidate_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    pairs = [
        (first, second)
        for first in hard_surfaces
        for second in hard_surfaces
        if str(first["source_name"]) < str(second["source_name"])
    ]
    for direction, fixed_values in (
        ("soft_cosine", decay_nodes),
        ("decay_cosine", soft_nodes),
    ):
        for fixed in fixed_values:
            expressions = {
                str(surface["surface_key"]): quartic_expression(
                    direction, fixed, surface
                )
                for surface in hard_surfaces
            }
            for first, second in pairs:
                first_expression = expressions[
                    str(first["surface_key"])
                ]
                second_expression = expressions[
                    str(second["surface_key"])
                ]
                resultant = sp.Poly(
                    sp.resultant(
                        first_expression,
                        second_expression,
                        U_SYMBOL,
                    ),
                    Q_SYMBOL,
                    extension=True,
                )
                resultant, removed_q1 = remove_exact_factor(
                    resultant,
                    sp.Poly(
                        Q_SYMBOL - 1,
                        Q_SYMBOL,
                        extension=True,
                    ),
                )
                q_candidates = polynomial_real_roots(
                    resultant,
                    RESULTANT_ROOT_IMAGINARY_TOLERANCE,
                )
                residual = crossing_residual_function(
                    direction, fixed, first, second
                )
                for q_candidate in q_candidates:
                    if (
                        q_candidate < q_minimum - DOMAIN_TOLERANCE
                        or q_candidate
                        > q_maximum + DOMAIN_TOLERANCE
                    ):
                        disposition = "outside_soft_energy_domain"
                        solutions: list[
                            tuple[float, float, float]
                        ] = []
                        nearest_residual = ""
                    else:
                        seeds = solution_seeds(
                            first_expression,
                            q_candidate,
                            second_expression,
                        )
                        solutions, nearest = solve_bounded_system(
                            residual, q_candidate, seeds
                        )
                        nearest_residual = nearest
                        disposition = (
                            "physical_isolated_crossing"
                            if solutions
                            else "projective_or_outside_angular_domain"
                        )
                    candidate_id = (
                        f"CC{len(candidate_rows) + 1:04d}"
                    )
                    candidate_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "direction": direction,
                            "fixed_coordinate": fixed,
                            "first_surface_key": first["surface_key"],
                            "second_surface_key": second["surface_key"],
                            "resultant_degree_after_q1_removal": (
                                resultant.degree()
                            ),
                            "removed_q_minus_one_multiplicity": (
                                removed_q1
                            ),
                            "candidate_q": q_candidate,
                            "candidate_soft_energy": (
                                1.0 - q_candidate**2
                            ),
                            "disposition": disposition,
                            "solution_count": len(solutions),
                            "nearest_system_residual": nearest_residual,
                            "classified": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
                    for q_value, coordinate, norm in solutions:
                        event_rows.append(
                            {
                                "event_type": "hard_hard_crossing",
                                "candidate_id": candidate_id,
                                "direction": direction,
                                "fixed_coordinate": fixed,
                                "first_surface_key": first[
                                    "surface_key"
                                ],
                                "second_surface_key": second[
                                    "surface_key"
                                ],
                                "q_value": q_value,
                                "soft_energy": 1.0 - q_value**2,
                                "boundary_coordinate": coordinate,
                                "simultaneous_equation_residual": norm,
                                "valid_for_resultant_isolated_location": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
    event_rows = deduplicate_event_rows(
        event_rows,
        (
            "first_surface_key",
            "second_surface_key",
            "direction",
            "fixed_coordinate",
        ),
    )
    return candidate_rows, event_rows


def analytic_root_count(
    expression: sp.Expr,
    energy: float,
) -> int:
    return len(
        hard_coordinate_roots(
            expression, math.sqrt(max(0.0, 1.0 - energy))
        )
    )


def add_event_count_jumps(
    events: list[dict[str, Any]],
    hard_surfaces: dict[str, dict[str, Any]],
) -> None:
    grouped: dict[
        tuple[str, float, str], list[dict[str, Any]]
    ] = defaultdict(list)
    for event in events:
        grouped[
            (
                str(event["direction"]),
                float(event["fixed_coordinate"]),
                str(event["surface_key"]),
            )
        ].append(event)
    energy_minimum = float(M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5267.ENERGY_MAXIMUM)
    for key, local_events in grouped.items():
        direction, fixed, surface_key_value = key
        expression = quartic_expression(
            direction,
            fixed,
            hard_surfaces[surface_key_value],
        )
        energies = sorted(
            {
                float(event["soft_energy"])
                for event in local_events
            }
        )
        groups: list[list[float]] = []
        for energy in energies:
            if (
                not groups
                or abs(energy - groups[-1][-1]) > 2.0e-7
            ):
                groups.append([energy])
            else:
                groups[-1].append(energy)
        centers = [
            sum(group) / len(group) for group in groups
        ]
        for index, center in enumerate(centers):
            left_bound = (
                energy_minimum
                if index == 0
                else centers[index - 1]
            )
            right_bound = (
                energy_maximum
                if index == len(centers) - 1
                else centers[index + 1]
            )
            epsilon = min(
                1.0e-5,
                0.2 * max(center - left_bound, 1.0e-10),
                0.2 * max(right_bound - center, 1.0e-10),
            )
            before_energy = max(
                energy_minimum,
                center - epsilon,
            )
            after_energy = min(
                energy_maximum,
                center + epsilon,
            )
            count_before = analytic_root_count(
                expression, before_energy
            )
            count_after = analytic_root_count(
                expression, after_energy
            )
            group_id = (
                f"{direction}|{fixed:.16g}|"
                f"{surface_key_value}|{center:.16g}"
            )
            for event in local_events:
                if (
                    abs(float(event["soft_energy"]) - center)
                    <= 2.0e-7
                ):
                    event["event_group_id"] = group_id
                    event["group_energy"] = center
                    event["root_count_before_group"] = count_before
                    event["root_count_after_group"] = count_after
                    event["group_root_count_jump"] = (
                        count_after - count_before
                    )


def event_balance_rows(
    hard_surfaces: list[dict[str, Any]],
    analytic_groups: dict[
        tuple[str, float, float, str], list[float]
    ],
    count_events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result_5271 = read_json(RESULT_5271)
    nodes = tuple(float(value) for value in result_5271["energy_nodes"])
    parent_5269 = read_json(M5270.RESULT_5269)
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    event_groups: dict[
        tuple[str, float, str, str], dict[str, Any]
    ] = {}
    for event in count_events:
        group_key = (
            str(event["direction"]),
            float(event["fixed_coordinate"]),
            str(event["surface_key"]),
            str(event["event_group_id"]),
        )
        event_groups[group_key] = event
    rows: list[dict[str, Any]] = []
    for surface in hard_surfaces:
        surface_key_value = str(surface["surface_key"])
        for direction, fixed_values in (
            ("soft_cosine", decay_nodes),
            ("decay_cosine", soft_nodes),
        ):
            for fixed in fixed_values:
                local_groups = [
                    event
                    for (
                        event_direction,
                        event_fixed,
                        event_surface,
                        _,
                    ), event in event_groups.items()
                    if event_direction == direction
                    and event_fixed == fixed
                    and event_surface == surface_key_value
                ]
                for slab_index, (left, right) in enumerate(
                    zip(nodes[:-1], nodes[1:])
                ):
                    left_count = len(
                        analytic_groups[
                            (
                                direction,
                                left,
                                fixed,
                                surface_key_value,
                            )
                        ]
                    )
                    right_count = len(
                        analytic_groups[
                            (
                                direction,
                                right,
                                fixed,
                                surface_key_value,
                            )
                        ]
                    )
                    in_slab = [
                        event
                        for event in local_groups
                        if left
                        < float(event["group_energy"])
                        <= right
                    ]
                    predicted_jump = sum(
                        int(event["group_root_count_jump"])
                        for event in in_slab
                    )
                    observed_jump = right_count - left_count
                    rows.append(
                        {
                            "direction": direction,
                            "fixed_coordinate": fixed,
                            "surface_key": surface_key_value,
                            "slab_index": slab_index,
                            "left_energy": left,
                            "right_energy": right,
                            "left_root_count": left_count,
                            "right_root_count": right_count,
                            "observed_root_count_jump": observed_jump,
                            "exact_event_group_count": len(in_slab),
                            "predicted_root_count_jump": predicted_jump,
                            "jump_residual": (
                                observed_jump - predicted_jump
                            ),
                            "balanced": observed_jump == predicted_jump,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
    return rows


def reconciliation_rows(
    endpoint_events: list[dict[str, Any]],
    fold_events: list[dict[str, Any]],
    crossing_events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    exact_by_type = {
        "angular_endpoint_entry_or_exit": endpoint_events,
        "interior_birth_death_or_merge": fold_events,
        "owner_merge_split_or_order_exchange": crossing_events,
    }
    for coarse in read_csv(EVENTS_5271):
        coarse_type = coarse["event_type"]
        left = (
            float(coarse["left_energy"])
            if coarse["left_energy"]
            else -math.inf
        )
        right = (
            float(coarse["right_energy"])
            if coarse["right_energy"]
            else math.inf
        )
        direction = coarse["direction"]
        fixed = (
            float(coarse["fixed_coordinate"])
            if coarse["fixed_coordinate"]
            else math.nan
        )
        candidates = [
            event
            for event in exact_by_type.get(coarse_type, [])
            if str(event["direction"]) == direction
            and abs(float(event["fixed_coordinate"]) - fixed)
            <= 1.0e-12
            and left - 1.0e-12
            <= float(event["soft_energy"])
            <= right + 1.0e-12
        ]
        nearest = min(
            candidates,
            key=lambda event: abs(
                float(event["soft_energy"])
                - 0.5 * (left + right)
            ),
            default=None,
        )
        rows.append(
            {
                "coarse_event_type": coarse_type,
                "direction": direction,
                "fixed_coordinate": coarse["fixed_coordinate"],
                "left_energy": coarse["left_energy"],
                "right_energy": coarse["right_energy"],
                "coarse_boundary_coordinate": coarse[
                    "boundary_coordinate"
                ],
                "matching_exact_event_count": len(candidates),
                "nearest_exact_energy": (
                    ""
                    if nearest is None
                    else nearest["soft_energy"]
                ),
                "nearest_exact_coordinate": (
                    ""
                    if nearest is None
                    else nearest.get(
                        "boundary_coordinate",
                        nearest.get("endpoint_coordinate", ""),
                    )
                ),
                "coarse_bracket_confirmed": nearest is not None,
                "interpretation": (
                    "confirmed_by_exact_equation"
                    if nearest is not None
                    else "superseded_nearest_coordinate_artifact"
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
        SCRIPT_5271,
        RESULT_5271,
        VALIDATION_5271,
        RAW_5271,
        EVENTS_5271,
        DESCRIPTORS_5270,
    )
    parent = read_json(RESULT_5271)
    parent_validation = read_csv(VALIDATION_5271)
    surfaces = surface_rows()
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5271_accepted": bool(parent["acceptance_passed"]),
        "parent_5271_validation_passed": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "surface_descriptor_count_is_seven": len(surfaces) == 7,
        "hard_surface_count_is_four": sum(
            row["family"] == "boosted_hard_leg"
            for row in surfaces
        )
        == 4,
        "all_midpoints_are_pi": all(
            abs(
                float(row["chamber_midpoint"]) - math.pi
            )
            <= 1.0e-14
            for row in surfaces
        ),
        "raw_boundary_rows_exist": bool(read_csv(RAW_5271)),
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
        "surface_count": len(surfaces),
        "runtime_seconds": 0.0,
        "decision": (
            "DRY_RUN_ACCEPTED__EXECUTE_EXACT_ANALYTIC_SURFACE_SOLVER"
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
        raise RuntimeError("5272 dry run did not pass")
    parent = read_json(RESULT_5271)
    surfaces = surface_rows()
    lookup = surface_lookup(surfaces)
    hard_surfaces = [
        surface
        for surface in surfaces
        if surface["family"] == "boosted_hard_leg"
    ]
    static_surfaces = [
        surface
        for surface in surfaces
        if surface["family"] != "boosted_hard_leg"
    ]
    reproduction = raw_reproduction_rows(lookup)
    ladder_rows, analytic_groups = ladder_reproduction_rows(
        surfaces
    )
    endpoints = endpoint_event_rows(hard_surfaces)
    fold_candidates, folds = fold_resultant_rows(hard_surfaces)
    crossing_candidates, hard_crossings = (
        hard_hard_crossing_rows(hard_surfaces)
    )
    static_crossings = hard_static_crossing_rows(
        hard_surfaces, static_surfaces
    )
    crossings = deduplicate_event_rows(
        [*hard_crossings, *static_crossings],
        (
            "first_surface_key",
            "second_surface_key",
            "direction",
            "fixed_coordinate",
        ),
    )
    count_events = [*endpoints, *folds]
    add_event_count_jumps(
        count_events, surface_lookup(hard_surfaces)
    )
    balance = event_balance_rows(
        hard_surfaces, analytic_groups, count_events
    )
    reconciliation = reconciliation_rows(
        endpoints, folds, crossings
    )
    raw_maximum_equation_residual = max(
        float(row["analytic_equation_residual"])
        for row in reproduction
    )
    raw_maximum_energy_residual = max(
        float(row["nearest_quadratic_energy_residual"])
        for row in reproduction
    )
    finite_ladder_residuals = [
        float(row["raw_to_analytic_maximum_residual"])
        for row in ladder_rows
        if math.isfinite(
            float(row["raw_to_analytic_maximum_residual"])
        )
    ]
    maximum_ladder_residual = max(
        finite_ladder_residuals, default=0.0
    )
    maximum_fold_residual = max(
        (
            float(
                row["equation_and_derivative_residual"]
            )
            for row in folds
        ),
        default=0.0,
    )
    maximum_crossing_residual = max(
        (
            float(row["simultaneous_equation_residual"])
            for row in crossings
        ),
        default=0.0,
    )
    checks = {
        "parent_5271_accepted": bool(parent["acceptance_passed"]),
        "surface_inventory_closed": (
            len(surfaces) == 7
            and len(hard_surfaces) == 4
            and len(static_surfaces) == 3
        ),
        "all_raw_boundaries_reproduced": (
            all(bool(row["reproduced"]) for row in reproduction)
            and raw_maximum_equation_residual
            <= RAW_EQUATION_TOLERANCE
            and raw_maximum_energy_residual
            <= RAW_EQUATION_TOLERANCE
        ),
        "all_ladder_roots_reproduced": (
            all(bool(row["reproduced"]) for row in ladder_rows)
            and maximum_ladder_residual
            <= ROOT_COORDINATE_TOLERANCE
        ),
        "all_fold_candidates_classified": all(
            bool(row["classified"]) for row in fold_candidates
        ),
        "all_crossing_candidates_classified": all(
            bool(row["classified"])
            for row in crossing_candidates
        ),
        "all_fold_residuals_tight": (
            maximum_fold_residual <= EVENT_RESIDUAL_TOLERANCE
        ),
        "all_crossing_residuals_tight": (
            maximum_crossing_residual
            <= EVENT_RESIDUAL_TOLERANCE
        ),
        "event_count_balance_closes": all(
            bool(row["balanced"]) for row in balance
        ),
        "hard_denominators_nonzero": (
            min(
                float(row["hard_leg_denominator_magnitude"])
                for row in reproduction
            )
            > 1.0e-8
            and min(
                (
                    float(
                        row["hard_leg_denominator_magnitude"]
                    )
                    for row in [*endpoints, *folds]
                ),
                default=1.0,
            )
            > 1.0e-8
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    confirmed_coarse = sum(
        bool(row["coarse_bracket_confirmed"])
        for row in reconciliation
    )
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "exact-analytic-boundary-surface-and-event-solver",
        "checks": checks,
        "acceptance_passed": accepted,
        "surface_count": len(surfaces),
        "hard_surface_count": len(hard_surfaces),
        "static_surface_count": len(static_surfaces),
        "raw_boundary_row_count": len(reproduction),
        "ladder_surface_slice_count": len(ladder_rows),
        "endpoint_event_count": len(endpoints),
        "fold_resultant_candidate_count": len(fold_candidates),
        "physical_fold_event_count": len(folds),
        "crossing_resultant_candidate_count": len(
            crossing_candidates
        ),
        "physical_surface_crossing_count": len(crossings),
        "event_balance_row_count": len(balance),
        "coarse_5271_event_count": len(reconciliation),
        "coarse_5271_confirmed_event_count": confirmed_coarse,
        "coarse_5271_superseded_event_count": (
            len(reconciliation) - confirmed_coarse
        ),
        "maximum_raw_equation_residual": (
            raw_maximum_equation_residual
        ),
        "maximum_raw_energy_inversion_residual": (
            raw_maximum_energy_residual
        ),
        "maximum_ladder_coordinate_residual": (
            maximum_ladder_residual
        ),
        "maximum_fold_system_residual": maximum_fold_residual,
        "maximum_crossing_system_residual": (
            maximum_crossing_residual
        ),
        "exact_boundary_law": {
            "soft_energy_coordinate": "q=sqrt(1-x)",
            "relative_cosine": (
                "r=a*d-sqrt(1-a^2)*sqrt(1-d^2)"
            ),
            "hard_leg_equation": (
                "F=(a-t)(1+s*r)q^2+2s(d-a*r)q"
                "+(a+t)(s*r-1)=0"
            ),
            "source_signs": {
                "direct:g1": 1,
                "direct:g2": -1,
            },
            "root_targets": {
                "plus_u_or_plus_v": float(
                    M5270.M5028.REFERENCE_COSINE.real
                ),
                "minus_u_or_minus_v": -float(
                    M5270.M5028.REFERENCE_COSINE.real
                ),
            },
            "static_surfaces": {
                "direct:g3:plus": "a=+0.3",
                "subtraction:decay:plus": "d=+0.3",
                "subtraction:decay:minus": "d=-0.3",
            },
            "half_angle_polynomial": (
                "u=sqrt((1-c)/(1+c)); "
                "(1+u^2)^2 F is quartic in u and quadratic in q"
            ),
            "fold_equation": "P(u,q)=0 and dP/du=0",
            "crossing_equation": "P_i(u,q)=P_j(u,q)=0",
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
            "ADOPT_EXACT_ANALYTIC_BOUNDARY_LAW__"
            "USE_RESULTANT_EVENTS_FOR_JOINT_CUBATURE"
            if accepted
            else "REPAIR_EXACT_ANALYTIC_BOUNDARY_SOLVER"
        ),
        "claim_boundary": {
            "valid_for_exact_shared_boundary_law": accepted,
            "valid_for_direct_soft_energy_inversion": accepted,
            "valid_for_exact_algebraic_endpoint_locations": accepted,
            "valid_for_resultant_isolated_fold_locations": accepted,
            "valid_for_resultant_isolated_crossings": accepted,
            "valid_for_complete_two_angle_continuum_topology": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The sourced phi=pi chamber now has an exact analytic "
                "energy-angle boundary law and resultant-isolated events "
                "on all sampled transverse slices. A continuous second-"
                "angle proof and final cubature remain outstanding."
            ),
        },
    }
    write_csv(SURFACES, surfaces)
    write_csv(RAW_REPRODUCTION, reproduction)
    write_csv(LADDER_REPRODUCTION, ladder_rows)
    write_csv(FOLD_CANDIDATES, fold_candidates)
    write_csv(ENDPOINT_EVENTS, endpoints)
    write_csv(FOLD_EVENTS, folds)
    write_csv(CROSSING_CANDIDATES, crossing_candidates)
    write_csv(CROSSING_EVENTS, crossings)
    write_csv(EVENT_BALANCE, balance)
    write_csv(RECONCILIATION, reconciliation)
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
    text = f"""# 5272 — Exact analytic boundary surface and event solver

## Scope

This checkpoint replaces the nearest-coordinate energy tracking in 5271
with a derived boundary equation. It is private, leaves the formalization
workbench untouched, and makes no UV, local-GR, or full-MTS claim.

## Exact reduction

Let

- `x` be the soft energy;
- `q = sqrt(1-x)`;
- `a` be the soft-direction cosine;
- `d` be the decay-direction cosine;
- `r = a d - sqrt(1-a^2)sqrt(1-d^2)` in the sourced `phi=pi` chamber;
- `s=+1` for `direct:g1` and `s=-1` for `direct:g2`;
- `t=+0.3` for plus roots and `t=-0.3` for minus roots.

The unit-circle root-margin boundary is exactly

`F=(a-t)(1+s r)q^2+2s(d-a r)q+(a+t)(s r-1)=0`.

This is quadratic in `q`, so each angular point has direct algebraic
soft-energy inversion. With the half-angle coordinate
`u=sqrt((1-c)/(1+c))`, `(1+u^2)^2 F` is quartic in the scanned angle.
Interior folds therefore satisfy `P=0` and `dP/du=0`; crossings satisfy
`P_i=P_j=0`. Checkpoint 5272 solves the corresponding resultants.

## Results

- Shared surfaces: **{result['surface_count']}**.
- Raw 5271 boundary rows reproduced: **{result['raw_boundary_row_count']}**.
- Ladder surface slices checked: **{result['ladder_surface_slice_count']}**.
- Exact endpoint events: **{result['endpoint_event_count']}**.
- Physical interior folds: **{result['physical_fold_event_count']}**.
- Physical surface crossings: **{result['physical_surface_crossing_count']}**.
- Maximum raw equation residual: `{result['maximum_raw_equation_residual']:.12g}`.
- Maximum energy inversion residual: `{result['maximum_raw_energy_inversion_residual']:.12g}`.
- Maximum ladder coordinate residual: `{result['maximum_ladder_coordinate_residual']:.12g}`.
- Maximum fold-system residual: `{result['maximum_fold_system_residual']:.12g}`.
- Maximum crossing-system residual: `{result['maximum_crossing_system_residual']:.12g}`.
- 5271 coarse events confirmed: **{result['coarse_5271_confirmed_event_count']}/{result['coarse_5271_event_count']}**.

The unmatched 5271 event rows are not hidden failures. They are explicitly
marked as nearest-coordinate artifacts superseded by the labelled analytic
equations.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

The exact shared boundary law, direct soft-energy inversion, algebraic
endpoint events, and resultant-isolated events on the sampled transverse
slices are accepted if validation passes. This is not yet a proof of the
complete two-angle continuum topology, the final phase-space coefficient,
the UV coefficient, local GR, or the full MTS theory.

## Next target

Use the exact quadratic/quartic law to continue the event curves in the
second angular coordinate, then construct topology-safe joint angular and
soft-energy cubature without an interpolated chamber mask.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5271)
    required_csvs = (
        SURFACES,
        RAW_REPRODUCTION,
        LADDER_REPRODUCTION,
        FOLD_CANDIDATES,
        ENDPOINT_EVENTS,
        FOLD_EVENTS,
        CROSSING_CANDIDATES,
        CROSSING_EVENTS,
        EVENT_BALANCE,
        RECONCILIATION,
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
            "PARENT_5271_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "EXACT_SURFACE_SOLVER_ACCEPTED",
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
            "RAW_BOUNDARIES_REPRODUCED",
            float(result["maximum_raw_equation_residual"])
            <= RAW_EQUATION_TOLERANCE,
            (
                "maximum residual="
                f"{result['maximum_raw_equation_residual']}"
            ),
        ),
        validation_gate(
            "DIRECT_ENERGY_INVERSION_REPRODUCES",
            float(
                result["maximum_raw_energy_inversion_residual"]
            )
            <= RAW_EQUATION_TOLERANCE,
            (
                "maximum residual="
                f"{result['maximum_raw_energy_inversion_residual']}"
            ),
        ),
        validation_gate(
            "ALL_LADDER_ROOTS_REPRODUCED",
            float(result["maximum_ladder_coordinate_residual"])
            <= ROOT_COORDINATE_TOLERANCE,
            (
                "maximum residual="
                f"{result['maximum_ladder_coordinate_residual']}"
            ),
        ),
        validation_gate(
            "RESULTANT_EVENTS_TIGHT",
            (
                float(result["maximum_fold_system_residual"])
                <= EVENT_RESIDUAL_TOLERANCE
                and float(
                    result["maximum_crossing_system_residual"]
                )
                <= EVENT_RESIDUAL_TOLERANCE
            ),
            (
                f"fold={result['maximum_fold_system_residual']}; "
                f"crossing={result['maximum_crossing_system_residual']}"
            ),
        ),
        validation_gate(
            "EVENT_COUNT_BALANCE_CLOSES",
            bool(result["checks"]["event_count_balance_closes"]),
            f"{result['event_balance_row_count']} energy-slab rows",
        ),
        validation_gate(
            "CONTINUUM_CLAIM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_complete_two_angle_continuum_topology"
            ],
            "sampled transverse slices are not promoted to a 2D proof",
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
            "VALIDATED_EXACT_ANALYTIC_BOUNDARY_SURFACE"
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
