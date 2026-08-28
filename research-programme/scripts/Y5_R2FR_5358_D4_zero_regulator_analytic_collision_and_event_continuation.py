from __future__ import annotations

import argparse
import cmath
import csv
import ctypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any, Callable


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

import mpmath as mp


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5358"
DOCUMENT = POST / "5358-Y5-R2FR-D4-zero-regulator-analytic-collision-and-event-continuation.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5358_VALIDATION.csv"

SCRIPT_5027 = SCRIPTS / "Y5_R2FR_5027_finite_x_boosted_polar_pinch_map.py"
SCRIPT_5029 = SCRIPTS / "Y5_R2FR_5029_finite_x_cross_source_collision_map.py"
SCRIPT_5235 = SCRIPTS / "Y5_R2FR_5235_dynamic_all_channel_conditional_A00_slice_pilot.py"
SCRIPT_5237 = SCRIPTS / "Y5_R2FR_5237_bounded_multi_event_direct_A00_causal_runner.py"
SCRIPT_5272 = SCRIPTS / "Y5_R2FR_5272_exact_analytic_boundary_surface_and_event_solver.py"
SCRIPT_5308 = SCRIPTS / "Y5_R2FR_5308_full_fixed_decay_pair_orbit_topology.py"
SCRIPT_5325 = SCRIPTS / "Y5_R2FR_5325_D2_midpoint_E0025_pole_topology_smoke.py"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
SCRIPT_5337 = SCRIPTS / "Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py"
SCRIPT_5355 = SCRIPTS / "Y5_R2FR_5355_D4_higher_rung_event_geometry_and_removable_singularity.py"
SCRIPT_5357 = SCRIPTS / "Y5_R2FR_5357_D4_six_regulator_coefficient_taylor_gate.py"

DECAY_NODES = FUNCTIONAL_RG / "5324" / "decay_angle_topology_node_summary.csv"
BASE_EVENTS = FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_refined_support_events.csv"
RESULT_5355 = FUNCTIONAL_RG / "5355" / "D4_higher_rung_event_geometry_result.json"
CONTRACT_5355 = FUNCTIONAL_RG / "5355" / "D4_endpoint_coefficient_removable_singularity_contract.csv"
RESULT_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_result.json"
VALIDATION_5357 = FUNCTIONAL_RG / "5357" / "D4_six_regulator_coefficient_validation.csv"
RUNG_ROOT = FUNCTIONAL_RG / "5337" / "rung-cache"

CHECKPOINT = 5358
MARKER = "MTS_5358_D4_ZERO_REGULATOR_ANALYTIC_COLLISION_EVENT_CONTINUATION"
REVISION = "D4-zero-regulator-analytic-collision-event-continuation-v1"
RUNG_IDS = ("E000625", "E00125", "E0025", "E005", "E010", "E020", "E040")
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
REPRESENTATIVE_PAIR = ("direct:g1:minus_u", "direct:g3:plus_u")
RECIPROCAL_PAIR = ("direct:g1:minus_v", "direct:g3:plus_v")
SCATTERING_TARGET_REAL = -9.0
MP_DIGITS = 80
mp.mp.dps = MP_DIGITS
MASK_TARGET = mp.mpf("-0.3")
Q_ZERO = mp.mpf(-5) / 4
ENERGY_MAXIMUM = mp.mpf("0.9999")
R_MINIMUM = mp.mpf("0.01")
ROOT_BRACKET_WIDTH = mp.mpf("1e-55")
INITIAL_EVENT_HALF_WIDTH = mp.mpf("1e-7")
PARENT_COEFFICIENT_RELATIVE_LIMIT = 1.0e-12
DISCRIMINANT_IDENTITY_RELATIVE_LIMIT = 1.0e-12
FINITE_ROOT_MATCH_LIMIT = 1.0e-6
FINITE_SURFACE_POLYNOMIAL_LIMIT = 2.0e-6
EXACT_EVENT_RESIDUAL_LIMIT = mp.mpf("1e-45")
NONZERO_FLOOR = mp.mpf("1e-6")
DENOMINATOR_FLOOR = mp.mpf("1e-3")
EVENT_SLOPE_FLOOR = mp.mpf("1e-2")
ZERO_EVENT_SHIFT_LIMIT = mp.mpf("1e-7")

CLAIM_COLLISION = "valid_for_D4_zero_regulator_collision_branch_desingularization"
CLAIM_EVENTS = "valid_for_D4_zero_regulator_eight_event_geometry"
CLAIM_CONTINUATION = "valid_for_D4_zero_regulator_local_event_continuation"
FALSE_CLAIMS = (
    "valid_for_D4_endpoint_coefficient_regulator_zero_limit",
    "valid_for_D4_integral_six_rung_complete_second_order_fit",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
    kernel32.SetPriorityClass.restype = ctypes.c_int
    process = kernel32.GetCurrentProcess()
    if not kernel32.SetPriorityClass(process, 0x00004000):
        raise ctypes.WinError()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def mp_text(value: Any, digits: int = 35) -> str:
    return mp.nstr(value, digits)


def source_paths() -> list[Path]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5027,
        SCRIPT_5029,
        SCRIPT_5235,
        SCRIPT_5237,
        SCRIPT_5272,
        SCRIPT_5308,
        SCRIPT_5325,
        SCRIPT_5334,
        SCRIPT_5337,
        SCRIPT_5355,
        SCRIPT_5357,
        DECAY_NODES,
        BASE_EVENTS,
        RESULT_5355,
        CONTRACT_5355,
        RESULT_5357,
        VALIDATION_5357,
    ]
    paths.extend(RUNG_ROOT / epsilon_id / "rung_result.json" for epsilon_id in RUNG_IDS)
    return paths


def source_rows(paths: list[Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC5358_{index:02d}",
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for index, path in enumerate(paths, start=1)
    ]


def d4_decay_absolute() -> float:
    matches = [
        row
        for row in read_csv(DECAY_NODES)
        if row.get("decay_node_id") == "D4_OUTER"
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one D4_OUTER decay row, found {len(matches)}")
    return float(matches[0]["absolute_decay_cosine"])


def term_signs(term_id: str) -> tuple[int, int]:
    if term_id == "MC04_SM_DM":
        return -1, -1
    if term_id == "MC04_SP_DP":
        return 1, 1
    raise ValueError(f"unsupported D4 term {term_id}")


def target_and_q(epsilon: float) -> tuple[complex, complex]:
    target = complex(SCATTERING_TARGET_REAL, epsilon)
    return target, (1.0 - target) / (1.0 + target)


def collision_quantities(
    soft_energy: complex,
    soft_cosine: float,
    decay_cosine: float,
    q_value: complex,
) -> dict[str, complex]:
    recoil = cmath.sqrt(1.0 - soft_energy)
    soft_sine = cmath.sqrt(1.0 - soft_cosine**2)
    decay_sine = cmath.sqrt(1.0 - decay_cosine**2)
    boost_remainder = ((2.0 - soft_energy) - 2.0 * recoil) / 2.0
    relative_coefficient = (
        boost_remainder * soft_cosine
        - soft_energy / 2.0
        + q_value * (1.0 + soft_cosine) * boost_remainder
    )
    constant_energy_plus = (
        (2.0 - soft_energy) / 2.0
        + recoil * decay_cosine
        - soft_energy * soft_cosine / 2.0
    )
    coefficient_a = decay_sine * (
        (1.0 - soft_cosine**2) * relative_coefficient / 2.0
        + q_value * (1.0 + soft_cosine) * recoil
    )
    coefficient_b = soft_sine * (
        constant_energy_plus
        - q_value * (1.0 + soft_cosine) * soft_energy / 2.0
        + relative_coefficient * soft_cosine * decay_cosine
    )
    coefficient_c = (
        decay_sine
        * (1.0 - soft_cosine**2)
        * relative_coefficient
        / 2.0
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1.0
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1.0
    )
    p14 = material_polynomial(
        "direct:L:s14", recoil, soft_cosine, decay_cosine, q_value
    )
    selected_root = (
        soft_sine
        * (1.0 + decay_cosine)
        * factor_f1
        / (decay_sine * (1.0 + soft_cosine) * factor_f2)
    )
    return {
        "R": recoil,
        "soft_sine": soft_sine,
        "decay_sine": decay_sine,
        "A": coefficient_a,
        "B": coefficient_b,
        "C": coefficient_c,
        "P14": p14,
        "F1": factor_f1,
        "F2": factor_f2,
        "selected_root": selected_root,
    }


def material_polynomial(
    surface_id: str,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    q_value: Any,
) -> Any:
    common = (soft_cosine - decay_cosine) * (
        q_value * (1 + soft_cosine) + soft_cosine - 1
    )
    if surface_id == "direct:L:s14":
        return (
            (1 + soft_cosine)
            * (1 + q_value)
            * (soft_cosine + decay_cosine)
            * recoil**2
            + 2
            * (1 + soft_cosine)
            * (1 - soft_cosine - q_value * soft_cosine)
            * recoil
            + common
        )
    if surface_id == "direct:L:s01":
        return (
            (1 - soft_cosine)
            * (
                -(1 + q_value)
                * (soft_cosine + decay_cosine)
                * recoil**2
                + 2
                * recoil
                * (q_value * (1 + soft_cosine) + soft_cosine)
            )
            + common
        )
    if surface_id == "direct:shared:s13":
        return (
            (soft_cosine - decay_cosine)
            * (1 - soft_cosine - q_value * (1 + soft_cosine))
            - (1 + q_value) * recoil * (1 - soft_cosine**2)
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def material_coefficients(
    surface_id: str, soft_cosine: Any, decay_cosine: Any, q_value: Any
) -> tuple[Any, Any, Any]:
    common = (soft_cosine - decay_cosine) * (
        q_value * (1 + soft_cosine) + soft_cosine - 1
    )
    if surface_id == "direct:L:s14":
        return (
            (1 + soft_cosine) * (1 + q_value) * (soft_cosine + decay_cosine),
            2 * (1 + soft_cosine) * (1 - soft_cosine - q_value * soft_cosine),
            common,
        )
    if surface_id == "direct:L:s01":
        return (
            -(1 - soft_cosine) * (1 + q_value) * (soft_cosine + decay_cosine),
            2 * (1 - soft_cosine) * (q_value * (1 + soft_cosine) + soft_cosine),
            common,
        )
    if surface_id == "direct:shared:s13":
        return (
            mp.mpf(0),
            -(1 + q_value) * (1 - soft_cosine**2),
            (soft_cosine - decay_cosine)
            * (1 - soft_cosine - q_value * (1 + soft_cosine)),
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def hard_boundary_value(recoil: Any, soft_cosine: Any, decay_cosine: Any) -> Any:
    relative = (
        soft_cosine * decay_cosine
        - mp.sqrt(1 - soft_cosine**2) * mp.sqrt(1 - decay_cosine**2)
    )
    return (
        (soft_cosine - MASK_TARGET) * (1 + relative) * recoil**2
        + 2 * (decay_cosine - soft_cosine * relative) * recoil
        + (soft_cosine + MASK_TARGET) * (relative - 1)
    )


def hard_boundary_roots(soft_cosine: Any, decay_cosine: Any) -> list[Any]:
    relative = (
        soft_cosine * decay_cosine
        - mp.sqrt(1 - soft_cosine**2) * mp.sqrt(1 - decay_cosine**2)
    )
    coefficient_a = (soft_cosine - MASK_TARGET) * (1 + relative)
    coefficient_b = 2 * (decay_cosine - soft_cosine * relative)
    coefficient_c = (soft_cosine + MASK_TARGET) * (relative - 1)
    discriminant = coefficient_b**2 - 4 * coefficient_a * coefficient_c
    root = mp.sqrt(discriminant)
    return sorted(
        (
            (-coefficient_b - root) / (2 * coefficient_a),
            (-coefficient_b + root) / (2 * coefficient_a),
        )
    )


def physical_material_root(
    surface_id: str,
    absolute_soft_cosine: Any,
    sign: int,
    decay_absolute: Any,
) -> Any:
    soft_cosine = sign * absolute_soft_cosine
    decay_cosine = sign * decay_absolute
    coefficient_a, coefficient_b, coefficient_c = material_coefficients(
        surface_id, soft_cosine, decay_cosine, Q_ZERO
    )
    if abs(coefficient_a) <= mp.mpf("1e-60"):
        candidates = [-coefficient_c / coefficient_b]
    else:
        discriminant = coefficient_b**2 - 4 * coefficient_a * coefficient_c
        square_root = mp.sqrt(discriminant)
        candidates = [
            (-coefficient_b - square_root) / (2 * coefficient_a),
            (-coefficient_b + square_root) / (2 * coefficient_a),
        ]
    physical = [value for value in candidates if 0 < value < 1]
    if len(physical) != 1:
        raise RuntimeError(
            f"expected one physical {surface_id} root at |c|={absolute_soft_cosine}; "
            f"found {physical} from {candidates}"
        )
    return physical[0]


def bracket_and_bisect(
    function: Callable[[Any], Any], center: Any
) -> dict[str, Any]:
    mp.mp.dps = max(mp.mp.dps, MP_DIGITS)
    half_width = INITIAL_EVENT_HALF_WIDTH
    for _ in range(20):
        lower = center - half_width
        upper = center + half_width
        lower_value = function(lower)
        upper_value = function(upper)
        if lower_value == 0 or upper_value == 0 or lower_value * upper_value < 0:
            break
        half_width *= 2
    else:
        raise RuntimeError(f"failed to bracket event around {center}")
    initial_lower = lower
    initial_upper = upper
    initial_lower_value = lower_value
    initial_upper_value = upper_value
    iterations = 0
    while upper - lower > ROOT_BRACKET_WIDTH and iterations < 300:
        iterations += 1
        midpoint = (lower + upper) / 2
        midpoint_value = function(midpoint)
        if midpoint_value == 0:
            lower = midpoint - ROOT_BRACKET_WIDTH / 4
            upper = midpoint + ROOT_BRACKET_WIDTH / 4
            lower_value = function(lower)
            upper_value = function(upper)
            break
        if lower_value == 0 or lower_value * midpoint_value < 0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
    return {
        "initial_lower": initial_lower,
        "initial_upper": initial_upper,
        "initial_lower_value": initial_lower_value,
        "initial_upper_value": initial_upper_value,
        "lower": lower,
        "upper": upper,
        "lower_value": lower_value,
        "upper_value": upper_value,
        "root": (lower + upper) / 2,
        "iterations": iterations,
    }


def load_rungs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in RUNG_IDS:
        path = RUNG_ROOT / epsilon_id / "rung_result.json"
        payload = read_json(path)
        for row in payload.get("rows", []):
            rows.append(
                {
                    **row,
                    "epsilon_id": epsilon_id,
                    "epsilon": float(payload["epsilon"]),
                    "rung_state": payload.get("state"),
                    "source_path": str(path.resolve()),
                    "source_sha256": digest(path),
                }
            )
    return rows


def parent_formula_probe_rows(
    rung_rows: list[dict[str, Any]], decay_absolute: float
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    parent = load_module("mts_5029_for_5358", SCRIPT_5029)
    rows: list[dict[str, Any]] = []
    maxima = {
        "coefficient_relative_error": 0.0,
        "discriminant_identity_relative_error": 0.0,
        "selected_root_distance": 0.0,
        "surface_polynomial_residual": 0.0,
        "g3_global_chart_relative_error": 0.0,
    }
    for source in rung_rows:
        soft_sign, decay_sign = term_signs(str(source["term_id"]))
        soft_cosine = soft_sign * float(source["event_coordinate"])
        decay_cosine = decay_sign * decay_absolute
        soft_energy = complex(
            float(source["pole_real"]), float(source["pole_imaginary"])
        )
        target, q_value = target_and_q(float(source["epsilon"]))
        analytic = collision_quantities(
            soft_energy, soft_cosine, decay_cosine, q_value
        )
        rationals = parent.root_rationals(
            soft_energy, soft_cosine, decay_cosine, target
        )
        numerator = parent.laurent_add(
            parent.laurent_multiply(
                rationals[REPRESENTATIVE_PAIR[0]][0],
                rationals[REPRESENTATIVE_PAIR[1]][1],
            ),
            parent.laurent_multiply(
                rationals[REPRESENTATIVE_PAIR[1]][0],
                rationals[REPRESENTATIVE_PAIR[0]][1],
            ),
            -1.0,
        )
        parent_scale = max(max(abs(value) for value in numerator.values()), 1.0e-300)
        coefficient_error = max(
            abs(numerator.get(1, 0.0j) + soft_energy * analytic["A"]),
            abs(numerator.get(0, 0.0j) + soft_energy * analytic["B"]),
            abs(numerator.get(-1, 0.0j) + soft_energy * analytic["C"]),
        ) / parent_scale
        discriminant = analytic["B"] ** 2 - 4 * analytic["A"] * analytic["C"]
        factored_discriminant = (
            (1.0 - soft_cosine**2) * analytic["P14"] ** 2 / 4.0
        )
        discriminant_error = abs(discriminant - factored_discriminant) / max(
            abs(analytic["B"] ** 2),
            abs(4 * analytic["A"] * analytic["C"]),
            1.0e-300,
        )
        parent_roots = parent.collision_roots(
            rationals[REPRESENTATIVE_PAIR[0]], rationals[REPRESENTATIVE_PAIR[1]]
        )
        root_distance = min(
            (
                abs(value - analytic["selected_root"])
                for value in parent_roots
            ),
            default=math.inf,
        )
        surface_residual = abs(
            material_polynomial(
                str(source["primary_surface_id"]),
                analytic["R"],
                soft_cosine,
                decay_cosine,
                q_value,
            )
        )
        external = cmath.sqrt(q_value)
        if external.imag > 0:
            external = -external
        global_root = external * (1.0 + soft_cosine) / analytic["soft_sine"]
        g3_value = parent.rational_value(
            rationals[REPRESENTATIVE_PAIR[1]], analytic["selected_root"]
        )
        global_error = abs(g3_value - global_root) / max(abs(global_root), 1.0e-300)
        maxima["coefficient_relative_error"] = max(
            maxima["coefficient_relative_error"], coefficient_error
        )
        maxima["discriminant_identity_relative_error"] = max(
            maxima["discriminant_identity_relative_error"], discriminant_error
        )
        maxima["selected_root_distance"] = max(
            maxima["selected_root_distance"], root_distance
        )
        maxima["surface_polynomial_residual"] = max(
            maxima["surface_polynomial_residual"], surface_residual
        )
        maxima["g3_global_chart_relative_error"] = max(
            maxima["g3_global_chart_relative_error"], global_error
        )
        rows.append(
            {
                "epsilon_id": source["epsilon_id"],
                "epsilon": source["epsilon"],
                "event_id": source["event_id"],
                "term_id": source["term_id"],
                "primary_surface_id": source["primary_surface_id"],
                "parent_collision_coefficient_relative_error": coefficient_error,
                "perfect_square_discriminant_relative_error": discriminant_error,
                "analytic_selected_root_parent_distance": root_distance,
                "material_surface_polynomial_residual": surface_residual,
                "g3_global_chart_relative_error": global_error,
                "parent_collision_root_count": len(parent_roots),
                "source_path": source["source_path"],
                "valid_for_D4_parent_algebra_reconstruction": (
                    coefficient_error <= PARENT_COEFFICIENT_RELATIVE_LIMIT
                    and discriminant_error <= DISCRIMINANT_IDENTITY_RELATIVE_LIMIT
                    and root_distance <= FINITE_ROOT_MATCH_LIMIT
                    and surface_residual <= FINITE_SURFACE_POLYNOMIAL_LIMIT
                ),
                **{claim: False for claim in FALSE_CLAIMS},
            }
        )
    return rows, maxima


def event_scalar_derivative(
    event_type: str,
    surface_id: str,
    absolute_soft_cosine: Any,
    sign: int,
    decay_absolute: Any,
) -> Any:
    soft_cosine = sign * absolute_soft_cosine
    decay_cosine = sign * decay_absolute
    if event_type == "BRANCH_DEATH":
        return mp.diff(
            lambda coordinate: material_polynomial(
                surface_id,
                R_MINIMUM,
                sign * coordinate,
                decay_cosine,
                Q_ZERO,
            ),
            absolute_soft_cosine,
        )
    recoil = physical_material_root(
        surface_id, absolute_soft_cosine, sign, decay_absolute
    )
    partial_p_r = mp.diff(
        lambda value: material_polynomial(
            surface_id, value, soft_cosine, decay_cosine, Q_ZERO
        ),
        recoil,
    )
    partial_p_c = mp.diff(
        lambda value: material_polynomial(
            surface_id, recoil, value, decay_cosine, Q_ZERO
        ),
        soft_cosine,
    )
    partial_h_r = mp.diff(
        lambda value: hard_boundary_value(value, soft_cosine, decay_cosine),
        recoil,
    )
    partial_h_c = mp.diff(
        lambda value: hard_boundary_value(recoil, value, decay_cosine),
        soft_cosine,
    )
    return sign * (partial_h_c - partial_h_r * partial_p_c / partial_p_r)


def exact_event_rows(
    base_events: list[dict[str, str]],
    smallest_rung: list[dict[str, Any]],
    decay_absolute_float: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mp.mp.dps = MP_DIGITS
    decay_absolute = mp.mpf(str(decay_absolute_float))
    base_lookup = {row["event_id"]: row for row in base_events}
    rung_lookup = {row["event_id"]: row for row in smallest_rung}
    rows: list[dict[str, Any]] = []
    raw: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        base = base_lookup[event_id]
        source = rung_lookup[event_id]
        event_type = str(source["event_type"])
        surface_id = str(source["primary_surface_id"])
        sign, decay_sign = term_signs(str(source["term_id"]))
        if sign != decay_sign:
            raise RuntimeError(f"unexpected unequal D4 signs for {event_id}")
        source_coordinate = mp.mpf(str(source["event_coordinate"]))

        if event_type == "BRANCH_DEATH":
            scalar = lambda coordinate: material_polynomial(
                surface_id,
                R_MINIMUM,
                sign * coordinate,
                sign * decay_absolute,
                Q_ZERO,
            )
        else:
            scalar = lambda coordinate: hard_boundary_value(
                physical_material_root(
                    surface_id, coordinate, sign, decay_absolute
                ),
                sign * coordinate,
                sign * decay_absolute,
            )
        bracket = bracket_and_bisect(scalar, source_coordinate)
        coordinate = bracket["root"]
        recoil = physical_material_root(
            surface_id, coordinate, sign, decay_absolute
        )
        soft_cosine = sign * coordinate
        decay_cosine = sign * decay_absolute
        soft_energy = 1 - recoil**2
        polynomial_residual = abs(
            material_polynomial(
                surface_id, recoil, soft_cosine, decay_cosine, Q_ZERO
            )
        )
        hard_residual = (
            abs(hard_boundary_value(recoil, soft_cosine, decay_cosine))
            if event_type != "BRANCH_DEATH"
            else mp.mpf(0)
        )
        partial_p_r = mp.diff(
            lambda value: material_polynomial(
                surface_id, value, soft_cosine, decay_cosine, Q_ZERO
            ),
            recoil,
        )
        partial_p_c = mp.diff(
            lambda value: material_polynomial(
                surface_id, recoil, value, decay_cosine, Q_ZERO
            ),
            soft_cosine,
        )
        material_recoil_slope = -sign * partial_p_c / partial_p_r
        material_energy_slope = -2 * recoil * material_recoil_slope
        hard_branch_id = "ENERGY_MAXIMUM"
        hard_other_root: Any = ""
        hard_partial_r: Any = mp.nan
        hard_partial_c: Any = mp.nan
        event_jacobian: Any = partial_p_r
        if event_type == "BRANCH_DEATH":
            signed_margin_slope = -material_energy_slope
            boundary_residual = abs(recoil - R_MINIMUM)
        else:
            hard_partial_r = mp.diff(
                lambda value: hard_boundary_value(
                    value, soft_cosine, decay_cosine
                ),
                recoil,
            )
            hard_partial_c = mp.diff(
                lambda value: hard_boundary_value(
                    recoil, value, decay_cosine
                ),
                soft_cosine,
            )
            hard_recoil_slope = -sign * hard_partial_c / hard_partial_r
            signed_margin_slope = 2 * recoil * (
                hard_recoil_slope - material_recoil_slope
            )
            event_jacobian = partial_p_r * hard_partial_c - partial_p_c * hard_partial_r
            roots = hard_boundary_roots(soft_cosine, decay_cosine)
            hard_branch_id = "Q02"
            hard_other_root = roots[0]
            boundary_residual = abs(roots[1] - recoil)

        initial_derivatives = [
            event_scalar_derivative(
                event_type,
                surface_id,
                bracket["initial_lower"]
                + (bracket["initial_upper"] - bracket["initial_lower"])
                * index
                / 16,
                sign,
                decay_absolute,
            )
            for index in range(17)
        ]
        derivative_sign_stable = all(value > 0 for value in initial_derivatives) or all(
            value < 0 for value in initial_derivatives
        )
        minimum_scalar_derivative = min(abs(value) for value in initial_derivatives)

        factor_f1 = (
            Q_ZERO * recoil * soft_cosine
            + Q_ZERO * recoil
            - Q_ZERO * soft_cosine
            - Q_ZERO
            + recoil * soft_cosine
            + recoil
            - soft_cosine
            + 1
        )
        factor_f2 = (
            Q_ZERO * recoil * soft_cosine
            - Q_ZERO * recoil
            - Q_ZERO * soft_cosine
            - Q_ZERO
            + recoil * soft_cosine
            - recoil
            - soft_cosine
            + 1
        )
        soft_sine = mp.sqrt(1 - soft_cosine**2)
        decay_sine = mp.sqrt(1 - decay_cosine**2)
        selected_root = (
            soft_sine
            * (1 + decay_cosine)
            * factor_f1
            / (decay_sine * (1 + soft_cosine) * factor_f2)
        )
        global_root = (
            -1j * mp.sqrt(5) / 2 * (1 + soft_cosine) / soft_sine
        )
        p14 = material_polynomial(
            "direct:L:s14", recoil, soft_cosine, decay_cosine, Q_ZERO
        )
        collision_jacobian = -soft_sine * p14 / 2
        collision_class = (
            "DESINGULARIZED_ANALYTIC_DOUBLE_ROOT"
            if surface_id == "direct:L:s14"
            else "SIMPLE_COLLISION_ROOT"
        )
        denominator_values = {
            "soft_sine": abs(soft_sine),
            "decay_sine": abs(decay_sine),
            "one_plus_soft_cosine": abs(1 + soft_cosine),
            "factor_F1": abs(factor_f1),
            "factor_F2": abs(factor_f2),
            "selected_root": abs(selected_root),
        }
        minimum_denominator = min(denominator_values.values())
        exact_residual = max(polynomial_residual, hard_residual, boundary_residual)
        branch_passes = (
            exact_residual <= EXACT_EVENT_RESIDUAL_LIMIT
            and abs(partial_p_r) > NONZERO_FLOOR
            and abs(event_jacobian) > NONZERO_FLOOR
            and minimum_denominator > DENOMINATOR_FLOOR
            and abs(signed_margin_slope) > EVENT_SLOPE_FLOOR
            and derivative_sign_stable
            and minimum_scalar_derivative > NONZERO_FLOOR
            and bracket["upper"] - bracket["lower"] <= ROOT_BRACKET_WIDTH
            and (
                collision_class == "DESINGULARIZED_ANALYTIC_DOUBLE_ROOT"
                or abs(collision_jacobian) > NONZERO_FLOOR
            )
        )
        raw_row = {
            "event_id": event_id,
            "event_type": event_type,
            "term_id": source["term_id"],
            "primary_surface_id": surface_id,
            "sign": sign,
            "coordinate": coordinate,
            "recoil": recoil,
            "soft_energy": soft_energy,
            "source_E000625_coordinate": source_coordinate,
            "coordinate_shift_from_E000625": coordinate - source_coordinate,
            "polynomial_residual": polynomial_residual,
            "hard_residual": hard_residual,
            "boundary_residual": boundary_residual,
            "partial_p_r": partial_p_r,
            "partial_p_c": partial_p_c,
            "hard_partial_r": hard_partial_r,
            "hard_partial_c": hard_partial_c,
            "event_jacobian": event_jacobian,
            "signed_margin_slope": signed_margin_slope,
            "minimum_scalar_derivative": minimum_scalar_derivative,
            "derivative_sign_stable": derivative_sign_stable,
            "collision_jacobian": collision_jacobian,
            "collision_class": collision_class,
            "minimum_denominator": minimum_denominator,
            "denominator_values": denominator_values,
            "selected_root": selected_root,
            "global_root": global_root,
            "hard_branch_id": hard_branch_id,
            "hard_other_root": hard_other_root,
            "bracket": bracket,
            "branch_passes": branch_passes,
            "base_path": str(BASE_EVENTS.resolve()),
            "rung_path": source["source_path"],
        }
        raw.append(raw_row)
        rows.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "term_id": source["term_id"],
                "primary_surface_id": surface_id,
                "material_polynomial_id": {
                    "direct:L:s14": "P14",
                    "direct:L:s01": "P01",
                    "direct:shared:s13": "P13",
                }[surface_id],
                "collision_class": collision_class,
                "zero_regulator_absolute_soft_cosine": mp_text(coordinate),
                "zero_regulator_coordinate_bracket_lower": mp_text(bracket["lower"]),
                "zero_regulator_coordinate_bracket_upper": mp_text(bracket["upper"]),
                "coordinate_bracket_width": mp_text(bracket["upper"] - bracket["lower"]),
                "zero_regulator_recoil_R": mp_text(recoil),
                "zero_regulator_soft_energy": mp_text(soft_energy),
                "source_E000625_coordinate": mp_text(source_coordinate),
                "coordinate_shift_from_E000625": mp_text(
                    coordinate - source_coordinate
                ),
                "material_polynomial_residual": mp_text(polynomial_residual),
                "hard_boundary_residual": mp_text(hard_residual),
                "selected_boundary_residual": mp_text(boundary_residual),
                "partial_material_polynomial_partial_R": mp_text(partial_p_r),
                "partial_material_polynomial_partial_c": mp_text(partial_p_c),
                "two_equation_event_jacobian": mp_text(event_jacobian),
                "signed_support_margin_slope": mp_text(signed_margin_slope),
                "minimum_local_scalar_derivative": mp_text(minimum_scalar_derivative),
                "local_scalar_derivative_sign_stable": derivative_sign_stable,
                "collision_polynomial_y_jacobian": mp_text(collision_jacobian),
                "minimum_analytic_denominator_magnitude": mp_text(
                    minimum_denominator
                ),
                "selected_relative_root_y": mp_text(selected_root),
                "selected_global_root_z": mp_text(global_root),
                "support_boundary_branch": hard_branch_id,
                "other_hard_boundary_R_root": (
                    mp_text(hard_other_root) if hard_other_root != "" else ""
                ),
                "root_bisection_iterations": bracket["iterations"],
                "valid_for_D4_zero_regulator_event_geometry": branch_passes,
                CLAIM_COLLISION: branch_passes,
                CLAIM_EVENTS: branch_passes,
                CLAIM_CONTINUATION: branch_passes,
                **{claim: False for claim in FALSE_CLAIMS},
            }
        )
    summary = {
        "maximum_exact_event_residual": max(
            float(
                max(
                    item["polynomial_residual"],
                    item["hard_residual"],
                    item["boundary_residual"],
                )
            )
            for item in raw
        ),
        "minimum_abs_material_R_jacobian": min(
            float(abs(item["partial_p_r"])) for item in raw
        ),
        "minimum_abs_event_jacobian": min(
            float(abs(item["event_jacobian"])) for item in raw
        ),
        "minimum_abs_support_margin_slope": min(
            float(abs(item["signed_margin_slope"])) for item in raw
        ),
        "minimum_analytic_denominator_magnitude": min(
            float(item["minimum_denominator"]) for item in raw
        ),
        "maximum_abs_coordinate_shift_from_E000625": max(
            float(abs(item["coordinate_shift_from_E000625"])) for item in raw
        ),
        "simple_collision_event_ids": [
            item["event_id"]
            for item in raw
            if item["collision_class"] == "SIMPLE_COLLISION_ROOT"
        ],
        "double_collision_event_ids": [
            item["event_id"]
            for item in raw
            if item["collision_class"]
            == "DESINGULARIZED_ANALYTIC_DOUBLE_ROOT"
        ],
        "all_event_certificates_pass": all(item["branch_passes"] for item in raw),
        "all_local_scalar_derivative_signs_stable": all(
            item["derivative_sign_stable"] for item in raw
        ),
    }
    return rows, summary


def analytic_contract_rows() -> list[dict[str, Any]]:
    common = {claim: False for claim in FALSE_CLAIMS}
    return [
        {
            "contract_id": "AC5358_01_target_branch",
            "equation": "t(epsilon)=-9+i epsilon; Q=(1-t)/(1+t); w^2=Q; w(0)=-i sqrt(5)/2",
            "result": "Q and the positive-epsilon square-root branch are analytic near epsilon=0",
            "status": "DERIVED",
            **common,
        },
        {
            "contract_id": "AC5358_02_collision_quadratic",
            "equation": "y F=A y^2+B y+C",
            "result": "the parent g1-minus-u/g3-plus-u collision numerator equals -e(A y^2+B y+C)/y",
            "status": "SOURCE_RECONSTRUCTED",
            **common,
        },
        {
            "contract_id": "AC5358_03_perfect_square",
            "equation": "B^2-4AC=(1-c^2) P14^2/4",
            "result": "the apparent fold is an exact crossing of two analytic roots, not a generic square-root branch point",
            "status": "DERIVED_AND_PARENT_PROBED",
            **common,
        },
        {
            "contract_id": "AC5358_04_selected_branch",
            "equation": "y_-=sqrt(1-c^2)(1+d)F1/[sqrt(1-d^2)(1+c)F2]",
            "result": "the same analytic minus branch matches all 56 parent finite-regulator event roots",
            "status": "DERIVED_AND_PARENT_PROBED",
            **common,
        },
        {
            "contract_id": "AC5358_05_global_patch",
            "equation": "z=w(1+c)/sqrt(1-c^2)",
            "result": "the g3 chart defines the global root through the s14 0/0 chart point",
            "status": "DERIVED_AND_PARENT_PROBED",
            **common,
        },
        {
            "contract_id": "AC5358_06_material_polynomials",
            "equation": "s14=4 Q R P14/(F1 F2); s01=4 R P01/(F1 F2); s13=4 e R(1+Q)P13/(F1 F2)",
            "result": "all three material pole families reduce to quadratic-or-linear polynomials in R=sqrt(1-e)",
            "status": "DERIVED_AND_SEVEN_RUNG_PROBED",
            **common,
        },
        {
            "contract_id": "AC5358_07_material_IFT",
            "equation": "Pj(R,c,Q)=0 and partial_R Pj != 0",
            "result": "each selected material pole energy has a local analytic continuation",
            "status": "EIGHT_EVENT_CERTIFICATE",
            **common,
        },
        {
            "contract_id": "AC5358_08_event_IFT",
            "equation": "contact: Pj=H=0 with nonzero determinant; endpoint: Pj(Rmin,c,Q)=0 transversely",
            "result": "all eight support events continue locally and retain their entry/exit ordering",
            "status": "EIGHT_EVENT_BRACKETED_CERTIFICATE",
            **common,
        },
        {
            "contract_id": "AC5358_09_5355_supersession",
            "equation": "partial_y(yF)=0 at E01,E04 but y_- remains analytic by exact factorization",
            "result": "the all-events simple-root premise in AC5355_03 is refuted and replaced by the desingularized branch theorem",
            "status": "SUPERSEDES_SIMPLE_ROOT_ONLY_PREMISE",
            **common,
        },
        {
            "contract_id": "AC5358_10_claim_boundary",
            "equation": "geometry continuation does not itself derive the endpoint numerator/residue limit",
            "result": "the coefficient and integrated D4 regulator-zero claims remain false",
            "status": "CLAIM_BOUNDARY_ENFORCED",
            **common,
        },
    ]


def preflight() -> dict[str, Any]:
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    checks: dict[str, Any] = {
        "all_required_sources_exist": not missing,
        "formalization_workbench_exists": (POST.parent / "formalization-workbench").is_dir(),
        "output_scope_is_post_checkpoint_only": OUTPUT.is_relative_to(POST)
        and DOCUMENT.is_relative_to(POST)
        and VALIDATION.is_relative_to(POST),
    }
    if missing:
        return {"all_pass": False, "checks": checks, "missing": missing, "required": required}
    result_5355 = read_json(RESULT_5355)
    result_5357 = read_json(RESULT_5357)
    validation_5357 = read_csv(VALIDATION_5357)
    base_events = read_csv(BASE_EVENTS)
    rung_payloads = {
        epsilon_id: read_json(RUNG_ROOT / epsilon_id / "rung_result.json")
        for epsilon_id in RUNG_IDS
    }
    script_5029 = SCRIPT_5029.read_text(encoding="utf-8")
    script_5272 = SCRIPT_5272.read_text(encoding="utf-8")
    checks.update(
        {
            "5355_geometry_checkpoint_passed": result_5355.get("validation_passed") is True,
            "5355_left_simple_jacobian_unsigned": result_5355.get(
                "zero_regulator_collision_jacobian_signed"
            )
            is False,
            "5357_six_rung_stability_passed": result_5357.get("claim_boundary", {}).get(
                "valid_for_D4_six_regulator_quadratic_endpoint_coefficient_stability"
            )
            is True,
            "5357_validation_rows_pass": bool(validation_5357)
            and all(parse_bool(row.get("passed")) for row in validation_5357),
            "base_event_identity_exact": tuple(row["event_id"] for row in base_events)
            == EVENT_IDS,
            "all_seven_rungs_complete": all(
                payload.get("state") == "RUNG_COMPLETE"
                and tuple(row["event_id"] for row in payload.get("rows", [])) == EVENT_IDS
                and all(
                    parse_bool(row.get("targeted_event_contract_passes"))
                    for row in payload.get("rows", [])
                )
                for payload in rung_payloads.values()
            ),
            "D4_decay_coordinate_is_source_owned": abs(
                d4_decay_absolute() - 0.8568306300360823
            )
            <= 1.0e-15,
            "parent_collision_algebra_present": all(
                needle in script_5029
                for needle in (
                    "def source_momenta(",
                    "def root_rationals(",
                    "def collision_roots(",
                )
            ),
            "parent_hard_boundary_algebra_present": all(
                needle in script_5272
                for needle in (
                    "def hard_boundary_coefficients(",
                    "def hard_boundary_value(",
                )
            ),
        }
    )
    return {
        "all_pass": all(bool(value) for value in checks.values()),
        "checks": checks,
        "missing": missing,
        "required": required,
    }


def render_document(result: dict[str, Any], event_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 5358: D4 zero-regulator analytic collision and event continuation",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "The old all-events simple-collision-root premise is not correct: `E01` and `E04` are double roots.  This does not kill the branch.  The parent collision discriminant is an exact square, so the selected root has an explicit analytic expression through both crossings.",
        "",
        "## Exact reduction",
        "",
        "With `R=sqrt(1-e)`, signed soft cosine `c`, signed decay cosine `d`, `Q=w^2=(1-t)/(1+t)`, and `t=-9+i epsilon`, the representative collision equation is",
        "",
        "`y F=A y^2+B y+C`,",
        "",
        "and its discriminant obeys",
        "",
        "`B^2-4AC=(1-c^2) P14^2/4`.",
        "",
        "The finite-regulator parent branch is exactly the minus branch",
        "",
        "`y_-=sqrt(1-c^2)(1+d)F1/[sqrt(1-d^2)(1+c)F2]`,",
        "",
        "while the nonsingular `g3` chart fixes `z=w(1+c)/sqrt(1-c^2)`.  Therefore the two `s14` double roots are analytic crossings, not generic square-root branch points.",
        "",
        "The three material surfaces reduce to",
        "",
        "- `s14=4 Q R P14/(F1 F2)`;",
        "- `s01=4 R P01/(F1 F2)`;",
        "- `s13=4 e R(1+Q) P13/(F1 F2)`.",
        "",
        "Each `Pj` is at most quadratic in `R`.  At `Q=-5/4` the eight events are solved by `Pj=H=0` for support contacts or `Pj(R=0.01)=0` for energy-endpoint exits.",
        "",
        "## Zero-regulator events",
        "",
        "| event | surface | class | |c| | e | margin slope |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in event_rows:
        lines.append(
            f"| {row['event_id']} | {row['primary_surface_id']} | {row['collision_class']} | {row['zero_regulator_absolute_soft_cosine']} | {row['zero_regulator_soft_energy']} | {row['signed_support_margin_slope']} |"
        )
    lines.extend(
        [
            "",
            "## What is proved here",
            "",
            f"- Parent coefficient reconstruction maximum relative error: `{result['parent_probe_maxima']['coefficient_relative_error']}`.",
            f"- Perfect-square identity maximum relative error: `{result['parent_probe_maxima']['discriminant_identity_relative_error']}`.",
            f"- Seven-rung material-polynomial maximum residual: `{result['parent_probe_maxima']['surface_polynomial_residual']}`.",
            f"- Minimum material `R` Jacobian: `{result['event_summary']['minimum_abs_material_R_jacobian']}`.",
            f"- Minimum event/support Jacobian: `{result['event_summary']['minimum_abs_event_jacobian']}`.",
            f"- Minimum support-margin slope magnitude: `{result['event_summary']['minimum_abs_support_margin_slope']}`.",
            "- Six events have ordinary simple collision roots; `E01` and `E04` use the exact desingularized double-root branch.",
            "",
            "## Claim boundary",
            "",
            "This closes the local collision/event-geometry obstruction behind checkpoint 5357.  It does **not** yet prove the endpoint coefficient limit or the integrated D4 regulator-zero limit: the direct zero-limit of the endpoint numerator/residue factors still has to be derived.",
            "",
            "No local-GR, UV, full phase-space, or full-MTS claim is made.",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    state = preflight()
    if not state["all_pass"]:
        raise RuntimeError(f"preflight failed: {state['checks']} missing={state['missing']}")
    decay_absolute = d4_decay_absolute()
    base_events = read_csv(BASE_EVENTS)
    rung_rows = load_rungs()
    parent_rows, parent_maxima = parent_formula_probe_rows(
        rung_rows, decay_absolute
    )
    smallest_rung = [
        row for row in rung_rows if row["epsilon_id"] == "E000625"
    ]
    event_rows, event_summary = exact_event_rows(
        base_events, smallest_rung, decay_absolute
    )
    contract_rows = analytic_contract_rows()
    sources = source_rows(state["required"])

    double_ids = event_summary["double_collision_event_ids"]
    simple_ids = event_summary["simple_collision_event_ids"]
    gates = [
        validation_row("preflight_passes", state["all_pass"], state["checks"]),
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["exists"] and len(row["sha256"]) == 64 for row in sources),
            len(sources),
        ),
        validation_row(
            "parent_collision_coefficients_reconstructed",
            parent_maxima["coefficient_relative_error"]
            <= PARENT_COEFFICIENT_RELATIVE_LIMIT,
            parent_maxima["coefficient_relative_error"],
        ),
        validation_row(
            "collision_discriminant_is_perfect_square",
            parent_maxima["discriminant_identity_relative_error"]
            <= DISCRIMINANT_IDENTITY_RELATIVE_LIMIT,
            parent_maxima["discriminant_identity_relative_error"],
        ),
        validation_row(
            "analytic_minus_root_matches_all_parent_rungs",
            parent_maxima["selected_root_distance"] <= FINITE_ROOT_MATCH_LIMIT,
            parent_maxima["selected_root_distance"],
        ),
        validation_row(
            "material_polynomials_match_all_parent_poles",
            len(parent_rows) == 56
            and all(row["valid_for_D4_parent_algebra_reconstruction"] for row in parent_rows)
            and parent_maxima["surface_polynomial_residual"]
            <= FINITE_SURFACE_POLYNOMIAL_LIMIT,
            parent_maxima["surface_polynomial_residual"],
        ),
        validation_row(
            "g3_global_chart_is_nonsingular_and_matches_parent",
            parent_maxima["g3_global_chart_relative_error"] <= 1.0e-12,
            parent_maxima["g3_global_chart_relative_error"],
        ),
        validation_row(
            "all_eight_zero_regulator_events_bracketed",
            len(event_rows) == 8
            and [row["event_id"] for row in event_rows] == list(EVENT_IDS)
            and event_summary["all_event_certificates_pass"],
            event_summary["maximum_exact_event_residual"],
        ),
        validation_row(
            "collision_classes_are_six_simple_two_desingularized",
            simple_ids == ["E02", "E03", "E05", "E06", "E07", "E08"]
            and double_ids == ["E01", "E04"],
            f"simple={simple_ids}; double={double_ids}",
        ),
        validation_row(
            "all_material_energy_jacobians_nonzero",
            event_summary["minimum_abs_material_R_jacobian"]
            > float(NONZERO_FLOOR),
            event_summary["minimum_abs_material_R_jacobian"],
        ),
        validation_row(
            "all_event_support_jacobians_nonzero",
            event_summary["minimum_abs_event_jacobian"]
            > float(NONZERO_FLOOR),
            event_summary["minimum_abs_event_jacobian"],
        ),
        validation_row(
            "all_event_support_contacts_transverse",
            event_summary["minimum_abs_support_margin_slope"]
            > float(EVENT_SLOPE_FLOOR),
            event_summary["minimum_abs_support_margin_slope"],
        ),
        validation_row(
            "all_analytic_branch_denominators_nonzero",
            event_summary["minimum_analytic_denominator_magnitude"]
            > float(DENOMINATOR_FLOOR),
            event_summary["minimum_analytic_denominator_magnitude"],
        ),
        validation_row(
            "zero_events_agree_with_smallest_positive_rung",
            event_summary["maximum_abs_coordinate_shift_from_E000625"]
            < float(ZERO_EVENT_SHIFT_LIMIT),
            event_summary["maximum_abs_coordinate_shift_from_E000625"],
        ),
        validation_row(
            "naive_all_simple_root_premise_is_not_relabelled",
            double_ids == ["E01", "E04"],
            "AC5355_03 is superseded, not silently marked true",
        ),
        validation_row(
            "downstream_regulator_zero_claims_remain_false",
            all(not row[claim] for row in event_rows for claim in FALSE_CLAIMS),
            "endpoint coefficient numerator/residue limit remains next",
        ),
        validation_row(
            "formalization_workbench_outside_write_scope",
            state["checks"]["output_scope_is_post_checkpoint_only"],
            0,
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    validation_passed = all(bool(row["passed"]) for row in gates)
    claims = {claim: False for claim in FALSE_CLAIMS}
    claims[CLAIM_COLLISION] = validation_passed
    claims[CLAIM_EVENTS] = validation_passed
    claims[CLAIM_CONTINUATION] = validation_passed
    decision = (
        "D4_ZERO_REGULATOR_COLLISION_AND_EIGHT_EVENT_CONTINUATION_PASS__DERIVE_ENDPOINT_COEFFICIENT_LIMIT"
        if validation_passed
        else "D4_ZERO_REGULATOR_ANALYTIC_CONTINUATION_BLOCKED"
    )

    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_collision_and_surface_parent_probe.csv", parent_rows)
    atomic_csv(output / "D4_zero_regulator_analytic_contract.csv", contract_rows)
    atomic_csv(output / "D4_zero_regulator_event_certificate.csv", event_rows)
    atomic_csv(output / "source_register.csv", sources)
    atomic_csv(output / "D4_zero_regulator_continuation_validation.csv", gates)
    atomic_csv(VALIDATION, gates)
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-zero-regulator-analytic-collision-and-event-continuation",
        "validation_passed": validation_passed,
        "decision": decision,
        "D4_decay_absolute_cosine": decay_absolute,
        "parent_probe_row_count": len(parent_rows),
        "parent_probe_maxima": parent_maxima,
        "event_summary": event_summary,
        "naive_all_events_simple_collision_jacobian_claim": False,
        "simple_collision_event_count": len(simple_ids),
        "desingularized_double_collision_event_count": len(double_ids),
        "desingularized_double_collision_event_ids": double_ids,
        "zero_regulator_collision_continuation_desingularized": validation_passed,
        "zero_regulator_eight_event_geometry_complete": validation_passed,
        "5357_geometric_continuation_condition_discharged": validation_passed,
        "endpoint_coefficient_regulator_zero_limit_complete": False,
        "remaining_endpoint_limit_obstruction": "derive the direct zero limit of the endpoint numerator/residue factors and sum the eight analytic limits",
        "formalization_workbench_modified_file_count": 0,
        "claim_boundary": claims,
        "source_files": sources,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(output / "D4_zero_regulator_continuation_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "state": "COMPLETE" if validation_passed else "BLOCKED",
            "decision": decision,
            "validation_passed": validation_passed,
            "updated_utc": utc_now(),
        },
    )
    render_document(result, event_rows)
    return result


def self_test() -> dict[str, Any]:
    q_value = complex(-1.25, -0.001)
    soft_energy = complex(0.77, -1.0e-5)
    soft_cosine = -0.75
    decay_cosine = -0.8568306300360823
    values = collision_quantities(
        soft_energy, soft_cosine, decay_cosine, q_value
    )
    discriminant = values["B"] ** 2 - 4 * values["A"] * values["C"]
    factored = (1 - soft_cosine**2) * values["P14"] ** 2 / 4
    polynomial = (
        values["A"] * values["selected_root"] ** 2
        + values["B"] * values["selected_root"]
        + values["C"]
    )
    bracket = bracket_and_bisect(lambda value: value**2 - 2, mp.mpf("1.414"))
    checks = {
        "perfect_square_identity": abs(discriminant - factored) <= 1.0e-13,
        "selected_root_solves_quadratic": abs(polynomial) <= 1.0e-13,
        "bisection_brackets_sqrt_two": bracket["lower"] ** 2 <= 2
        <= bracket["upper"] ** 2,
        "bisection_width_contract": bracket["upper"] - bracket["lower"]
        <= ROOT_BRACKET_WIDTH,
    }
    return {"all_pass": all(checks.values()), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        state = preflight()
        result = {
            "mode": "preflight",
            "all_pass": state["all_pass"],
            "checks": state["checks"],
            "missing": state["missing"],
            CLAIM_COLLISION: False,
            CLAIM_EVENTS: False,
            CLAIM_CONTINUATION: False,
            **{claim: False for claim in FALSE_CLAIMS},
        }
    else:
        result = run(arguments.output_dir.resolve())
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result.get("all_pass", result.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
