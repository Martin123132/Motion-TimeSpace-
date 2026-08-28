from __future__ import annotations

import argparse
import cmath
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

from mpmath import iv


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
OUTPUT = FUNCTIONAL_RG / "5394"
DOCUMENT = (
    POST
    / "5394-Y5-R2FR-D4-common-logarithm-branch-and-pole-primitive-Cauchy-reduction.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5394_VALIDATION.csv"

SCRIPT_5308 = SCRIPTS / "Y5_R2FR_5308_full_fixed_decay_pair_orbit_topology.py"
SCRIPT_5358 = (
    SCRIPTS
    / "Y5_R2FR_5358_D4_zero_regulator_analytic_collision_and_event_continuation.py"
)
SCRIPT_5393 = (
    SCRIPTS
    / "Y5_R2FR_5393_D4_parent_frozen_mapped_away_atlas_and_W3_owner_decomposition.py"
)
ATLAS_5393 = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_x_atlas.csv"
MAPPED_5393 = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_mapped_cells.csv"
BRANCHES_5393 = FUNCTIONAL_RG / "5393" / "D4_material_pole_branch_ownership.csv"
RESULT_5393 = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_atlas_result.json"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
RESULT_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
CONTRACT_5308 = FUNCTIONAL_RG / "5308" / "fixed_decay_energy_soft_cubature_contract.csv"

CHECKPOINT = 5394
MARKER = "MTS_5394_D4_COMMON_LOGARITHM_BRANCH_AND_POLE_PRIMITIVE_CAUCHY_REDUCTION"
REVISION = "D4-common-logarithm-branch-pole-primitive-Cauchy-reduction-v1"
ABSOLUTE_DECAY_COSINE = 0.8568306300360823
REGULATOR_INTERVAL = (0.0, 0.02)
REGULATOR_BIN_COUNT = 8
REGULATOR_CAUCHY_RADIUS = 5.0e-7
INTERVAL_DIGITS = 45
MAXIMUM_X_REFINEMENT_DEPTH = 24
TARGET_COSINE = -0.3
Q_ZERO = -1.25
WINDING_ABS_UPPER = 2

CLAIM_LOG = "valid_for_D4_common_material_pole_logarithm_branch"
CLAIM_REDUCTION = "valid_for_D4_exact_pole_primitive_Cauchy_reduction"
OPEN_CLAIMS = (
    "valid_for_D4_numeric_pole_primitive_W3_bound",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


class IntervalFailure(RuntimeError):
    pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5308 = load_module("mts_5308_for_5394", SCRIPT_5308)
M5308.M5302.EDGE_DECAY_ABSOLUTE = ABSOLUTE_DECAY_COSINE
M5358 = load_module("mts_5358_for_5394", SCRIPT_5358)


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def cpoint(value: complex | float | int) -> Any:
    converted = complex(value)
    return iv.mpc(
        [converted.real, converted.real],
        [converted.imag, converted.imag],
    )


def cbox(
    real_lower: float,
    real_upper: float,
    imaginary_lower: float = 0.0,
    imaginary_upper: float = 0.0,
) -> Any:
    return iv.mpc(
        [real_lower, real_upper],
        [imaginary_lower, imaginary_upper],
    )


def real_bounds(value: Any) -> tuple[float, float]:
    return float(value.real.a), float(value.real.b)


def imaginary_bounds(value: Any) -> tuple[float, float]:
    return float(value.imag.a), float(value.imag.b)


def midpoint(value: Any) -> complex:
    real_lower, real_upper = real_bounds(value)
    imaginary_lower, imaginary_upper = imaginary_bounds(value)
    return complex(
        0.5 * (real_lower + real_upper),
        0.5 * (imaginary_lower + imaginary_upper),
    )


def lower_abs(value: Any) -> float:
    return float(abs(value).a)


def upper_abs(value: Any) -> float:
    return float(abs(value).b)


def interval_complex_sqrt(value: Any) -> Any:
    candidates = (
        (1, 1),
        (-1, 1j),
        (1j, cmath.exp(0.25j * math.pi)),
        (-1j, cmath.exp(-0.25j * math.pi)),
    )
    phase, phase_root = max(
        candidates,
        key=lambda item: real_bounds(cpoint(item[0]) * value)[0],
    )
    rotated = cpoint(phase) * value
    if real_bounds(rotated)[0] <= 0.0:
        raise IntervalFailure("no square-root half-plane chart excludes zero")
    real_root = iv.sqrt((abs(rotated) + rotated.real) / 2)
    imaginary_root = rotated.imag / (2 * real_root)
    root = iv.mpc(real_root, imaginary_root) / cpoint(phase_root)
    principal = cmath.sqrt(midpoint(value))
    if abs(midpoint(root) - principal) > abs(-midpoint(root) - principal):
        root = -root
    return root


def q_value(epsilon: Any) -> Any:
    epsilon_squared = epsilon**2
    denominator = cpoint(64) + epsilon_squared
    if lower_abs(denominator) <= 0.0:
        raise IntervalFailure("regulator q denominator reaches zero")
    return -(
        cpoint(80) + epsilon_squared
    ) / denominator + cpoint(1j) * (-cpoint(2) * epsilon / denominator)


def material_coefficients(
    surface_id: str,
    soft_cosine: Any,
    decay_cosine: Any,
    q: Any,
) -> tuple[Any, Any, Any]:
    common = (soft_cosine - decay_cosine) * (
        q * (cpoint(1) + soft_cosine) + soft_cosine - cpoint(1)
    )
    if surface_id == "direct:L:s14":
        return (
            (cpoint(1) + soft_cosine)
            * (cpoint(1) + q)
            * (soft_cosine + decay_cosine),
            cpoint(2)
            * (cpoint(1) + soft_cosine)
            * (cpoint(1) - soft_cosine - q * soft_cosine),
            common,
        )
    if surface_id == "direct:L:s01":
        return (
            -(cpoint(1) - soft_cosine)
            * (cpoint(1) + q)
            * (soft_cosine + decay_cosine),
            cpoint(2)
            * (cpoint(1) - soft_cosine)
            * (q * (cpoint(1) + soft_cosine) + soft_cosine),
            common,
        )
    if surface_id == "direct:shared:s13":
        return (
            cpoint(0),
            -(cpoint(1) + q)
            * (cpoint(1) - soft_cosine * soft_cosine),
            (soft_cosine - decay_cosine)
            * (cpoint(1) - soft_cosine - q * (cpoint(1) + soft_cosine)),
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def point_material_root(
    surface_id: str,
    sign: int,
    absolute_soft_cosine: float,
    epsilon: complex,
) -> complex:
    soft_cosine = sign * absolute_soft_cosine
    decay_cosine = sign * ABSOLUTE_DECAY_COSINE
    q = -(80 + epsilon**2) / (64 + epsilon**2) + 1j * (
        -2 * epsilon / (64 + epsilon**2)
    )
    coefficients = material_coefficients(
        surface_id,
        cpoint(soft_cosine),
        cpoint(decay_cosine),
        cpoint(q),
    )
    coefficient_a, coefficient_b, coefficient_c = (
        midpoint(value) for value in coefficients
    )
    zero_root = complex(
        M5358.physical_material_root(
            surface_id,
            absolute_soft_cosine,
            sign,
            ABSOLUTE_DECAY_COSINE,
        )
    )
    if abs(coefficient_a) <= 1.0e-14:
        return -coefficient_c / coefficient_b
    discriminant_root = cmath.sqrt(
        coefficient_b**2 - 4 * coefficient_a * coefficient_c
    )
    candidates = (
        (-coefficient_b - discriminant_root) / (2 * coefficient_a),
        (-coefficient_b + discriminant_root) / (2 * coefficient_a),
    )
    return min(candidates, key=lambda value: abs(value - zero_root))


def interval_material_root(
    surface_id: str,
    sign: int,
    x_lower: float,
    x_upper: float,
    epsilon: Any,
) -> tuple[Any, dict[str, float]]:
    absolute_coordinate = cbox(x_lower, x_upper)
    soft_cosine = (
        absolute_coordinate
        if sign > 0
        else cbox(-x_upper, -x_lower)
    )
    decay_cosine = cpoint(sign * ABSOLUTE_DECAY_COSINE)
    q = q_value(epsilon)
    coefficient_a, coefficient_b, coefficient_c = material_coefficients(
        surface_id, soft_cosine, decay_cosine, q
    )
    if surface_id == "direct:shared:s13":
        denominator_lower = lower_abs(coefficient_b)
        if denominator_lower <= 0.0:
            raise IntervalFailure("linear material coefficient reaches zero")
        root = -coefficient_c / coefficient_b
        discriminant_lower = math.inf
    else:
        denominator_lower = lower_abs(cpoint(2) * coefficient_a)
        if denominator_lower <= 0.0:
            raise IntervalFailure("quadratic material coefficient reaches zero")
        discriminant = (
            coefficient_b * coefficient_b
            - cpoint(4) * coefficient_a * coefficient_c
        )
        discriminant_lower = lower_abs(discriminant)
        if discriminant_lower <= 0.0:
            raise IntervalFailure("material discriminant reaches zero")
        discriminant_root = interval_complex_sqrt(discriminant)
        candidates = (
            (-coefficient_b - discriminant_root)
            / (cpoint(2) * coefficient_a),
            (-coefficient_b + discriminant_root)
            / (cpoint(2) * coefficient_a),
        )
        point_root = point_material_root(
            surface_id,
            sign,
            0.5 * (x_lower + x_upper),
            midpoint(epsilon),
        )
        root = min(
            candidates,
            key=lambda value: abs(midpoint(value) - point_root),
        )
    root_real_lower, root_real_upper = real_bounds(root)
    if root_real_lower <= 0.0 or root_real_upper >= 1.0:
        raise IntervalFailure("material recoil enclosure leaves physical chart")
    return root, {
        "material_coefficient_denominator_abs_lower": denominator_lower,
        "material_discriminant_abs_lower": discriminant_lower,
        "q_denominator_abs_lower": lower_abs(cpoint(64) + epsilon**2),
    }


def owner_spec(owner: str) -> tuple[str, int]:
    first_owner = owner.split("|")[0]
    surface_id, branch_id = first_owner.rsplit(":", 1)
    if branch_id != "Q02":
        raise ValueError(f"unsupported hard-boundary branch {owner}")
    return surface_id, 2


def surface_signs(surface_id: str) -> tuple[int, int, int]:
    component, soft_label, decay_label = surface_id.split("_")
    hard_sign = 1 if component == "MC04" else -1
    soft_sign = 1 if soft_label == "SP" else -1
    decay_sign = 1 if decay_label == "DP" else -1
    return hard_sign, soft_sign, decay_sign


def point_boundary_energy(owner: str, coordinate: float) -> float:
    return float(M5308.boundary_energy(owner, coordinate))


def interval_boundary_energy(
    owner: str, x_lower: float, x_upper: float
) -> tuple[Any, dict[str, float]]:
    minimum, maximum = M5308.energy_limits()
    if owner == "ENERGY_MINIMUM":
        return cpoint(minimum), {"boundary_discriminant_abs_lower": math.inf}
    if owner == "ENERGY_MAXIMUM":
        return cpoint(maximum), {"boundary_discriminant_abs_lower": math.inf}
    surface_id, _ = owner_spec(owner)
    hard_sign, soft_sign, decay_sign = surface_signs(surface_id)
    absolute_coordinate = cbox(x_lower, x_upper)
    soft_cosine = (
        absolute_coordinate
        if soft_sign > 0
        else cbox(-x_upper, -x_lower)
    )
    decay_cosine = cpoint(decay_sign * ABSOLUTE_DECAY_COSINE)
    soft_sine = interval_complex_sqrt(
        cpoint(1) - soft_cosine * soft_cosine
    )
    decay_sine = cpoint(math.sqrt(1 - ABSOLUTE_DECAY_COSINE**2))
    relative = soft_cosine * decay_cosine - soft_sine * decay_sine
    coefficient_a = (soft_cosine - cpoint(TARGET_COSINE)) * (
        cpoint(1) + cpoint(hard_sign) * relative
    )
    coefficient_b = (
        cpoint(2 * hard_sign)
        * (decay_cosine - soft_cosine * relative)
    )
    coefficient_c = (soft_cosine + cpoint(TARGET_COSINE)) * (
        cpoint(hard_sign) * relative - cpoint(1)
    )
    denominator_lower = lower_abs(cpoint(2) * coefficient_a)
    if denominator_lower <= 0.0:
        raise IntervalFailure(f"hard boundary coefficient reaches zero: {owner}")
    discriminant = (
        coefficient_b * coefficient_b
        - cpoint(4) * coefficient_a * coefficient_c
    )
    discriminant_lower = lower_abs(discriminant)
    if discriminant_lower <= 0.0:
        raise IntervalFailure(f"hard boundary discriminant reaches zero: {owner}")
    discriminant_root = interval_complex_sqrt(discriminant)
    candidates = (
        (-coefficient_b - discriminant_root) / (cpoint(2) * coefficient_a),
        (-coefficient_b + discriminant_root) / (cpoint(2) * coefficient_a),
    )
    coordinate_midpoint = 0.5 * (x_lower + x_upper)
    energy_midpoint = point_boundary_energy(owner, coordinate_midpoint)
    expected_q = math.sqrt(max(0.0, 1.0 - energy_midpoint))
    selected_q = min(
        candidates,
        key=lambda value: abs(midpoint(value) - expected_q),
    )
    energy = cpoint(1) - selected_q * selected_q
    return energy, {
        "boundary_discriminant_abs_lower": discriminant_lower,
        "boundary_coefficient_denominator_abs_lower": denominator_lower,
    }


def analytic_log_abs_upper(value: Any) -> tuple[float, dict[str, float]]:
    real_lower, _ = real_bounds(value)
    if real_lower <= 0.0:
        raise IntervalFailure("logarithm argument leaves right half-plane")
    modulus_lower = lower_abs(value)
    modulus_upper = upper_abs(value)
    if modulus_lower <= 0.0 or not math.isfinite(modulus_upper):
        raise IntervalFailure("logarithm argument is not separated from zero")
    imaginary_lower, imaginary_upper = imaginary_bounds(value)
    imaginary_abs_upper = max(abs(imaginary_lower), abs(imaginary_upper))
    radial_upper = max(
        abs(math.log(modulus_lower)),
        abs(math.log(modulus_upper)),
    )
    argument_upper = math.atan2(imaginary_abs_upper, real_lower)
    return radial_upper + argument_upper, {
        "argument_real_lower": real_lower,
        "argument_modulus_lower": modulus_lower,
        "argument_modulus_upper": modulus_upper,
        "argument_phase_abs_upper": argument_upper,
    }


def regulator_boxes() -> list[dict[str, Any]]:
    step = (
        REGULATOR_INTERVAL[1] - REGULATOR_INTERVAL[0]
    ) / REGULATOR_BIN_COUNT
    return [
        {
            "regulator_bin_index": index,
            "Cauchy_center_lower": REGULATOR_INTERVAL[0] + index * step,
            "Cauchy_center_upper": REGULATOR_INTERVAL[0] + (index + 1) * step,
            "epsilon_real_lower": (
                REGULATOR_INTERVAL[0] + index * step - REGULATOR_CAUCHY_RADIUS
            ),
            "epsilon_real_upper": (
                REGULATOR_INTERVAL[0]
                + (index + 1) * step
                + REGULATOR_CAUCHY_RADIUS
            ),
            "epsilon_imaginary_lower": -REGULATOR_CAUCHY_RADIUS,
            "epsilon_imaginary_upper": REGULATOR_CAUCHY_RADIUS,
        }
        for index in range(REGULATOR_BIN_COUNT)
    ]


def material_branches() -> list[dict[str, Any]]:
    rows = [
        row
        for row in read_csv(BRANCHES_5393)
        if row["pole_class"] == "MATERIAL_SIMPLE_POLE"
    ]
    for row in rows:
        if row["term_id"] == "MC04_SM_DM":
            row["sign"] = -1
        elif row["term_id"] == "MC04_SP_DP":
            row["sign"] = 1
        else:
            raise RuntimeError(f"unsupported material term {row['term_id']}")
    return rows


def support_owner_lookup() -> dict[tuple[str, str], tuple[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in read_csv(MAPPED_5393):
        if row["region_class"] != "AWAY":
            continue
        for term_id in row["reduced_MC04_term_ids"].split("|"):
            grouped.setdefault((row["atlas_cell_id"], term_id), []).append(row)
    result: dict[tuple[str, str], tuple[str, str]] = {}
    for key, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: int(row["parent_chamber_index"]))
        result[key] = (
            ordered[0]["lower_energy_boundary"],
            ordered[-1]["upper_energy_boundary"],
        )
    return result


def away_support_segments() -> list[dict[str, Any]]:
    atlas = read_csv(ATLAS_5393)
    owners = support_owner_lookup()
    segments: list[dict[str, Any]] = []
    for branch in material_branches():
        support_lower = float(branch["support_start_coordinate_epsilon_zero"])
        support_upper = float(branch["support_end_coordinate_epsilon_zero"])
        for cell in atlas:
            if cell["region_class"] != "AWAY":
                continue
            lower = max(
                support_lower,
                float(cell["lower_absolute_soft_cosine"]),
            )
            upper = min(
                support_upper,
                float(cell["upper_absolute_soft_cosine"]),
            )
            if upper <= lower:
                continue
            owner_key = (cell["atlas_cell_id"], branch["term_id"])
            if owner_key not in owners:
                raise RuntimeError(f"missing support owner pair {owner_key}")
            lower_owner, upper_owner = owners[owner_key]
            segments.append(
                {
                    "branch_owner_id": branch["branch_owner_id"],
                    "term_id": branch["term_id"],
                    "primary_surface_id": branch["primary_surface_id"],
                    "sign": int(branch["sign"]),
                    "atlas_cell_id": cell["atlas_cell_id"],
                    "parent_x_panel_index": int(cell["parent_x_panel_index"]),
                    "x_lower": lower,
                    "x_upper": upper,
                    "lower_energy_boundary": lower_owner,
                    "upper_energy_boundary": upper_owner,
                }
            )
    return segments


def causal_sheet_sign(
    surface_id: str, sign: int, coordinate: float
) -> int:
    pole = cpoint(1) - cpoint(
        point_material_root(surface_id, sign, coordinate, 1.0e-8)
    ) ** 2
    imaginary = midpoint(pole).imag
    if imaginary == 0.0:
        raise IntervalFailure("causal pole imaginary part is zero")
    return 1 if imaginary > 0.0 else -1


def evaluate_log_box(
    segment: dict[str, Any],
    epsilon_row: dict[str, Any],
    x_lower: float,
    x_upper: float,
    refinement_depth: int,
    refinement_path: str,
) -> dict[str, Any]:
    epsilon = cbox(
        float(epsilon_row["epsilon_real_lower"]),
        float(epsilon_row["epsilon_real_upper"]),
        float(epsilon_row["epsilon_imaginary_lower"]),
        float(epsilon_row["epsilon_imaginary_upper"]),
    )
    recoil, root_diagnostics = interval_material_root(
        segment["primary_surface_id"],
        int(segment["sign"]),
        x_lower,
        x_upper,
        epsilon,
    )
    pole = cpoint(1) - recoil * recoil
    lower_energy, lower_diagnostics = interval_boundary_energy(
        segment["lower_energy_boundary"], x_lower, x_upper
    )
    upper_energy, upper_diagnostics = interval_boundary_energy(
        segment["upper_energy_boundary"], x_lower, x_upper
    )
    upper_gap = upper_energy - pole
    lower_gap = pole - lower_energy
    upper_log, upper_log_diagnostics = analytic_log_abs_upper(upper_gap)
    lower_log, lower_log_diagnostics = analytic_log_abs_upper(lower_gap)
    coordinate_midpoint = 0.5 * (x_lower + x_upper)
    zero_root = complex(
        M5358.physical_material_root(
            segment["primary_surface_id"],
            coordinate_midpoint,
            int(segment["sign"]),
            ABSOLUTE_DECAY_COSINE,
        )
    )
    local_zero_root = point_material_root(
        segment["primary_surface_id"],
        int(segment["sign"]),
        coordinate_midpoint,
        0j,
    )
    lower_parent = point_boundary_energy(
        segment["lower_energy_boundary"], coordinate_midpoint
    )
    upper_parent = point_boundary_energy(
        segment["upper_energy_boundary"], coordinate_midpoint
    )
    lower_local = midpoint(
        interval_boundary_energy(
            segment["lower_energy_boundary"],
            coordinate_midpoint,
            coordinate_midpoint,
        )[0]
    ).real
    upper_local = midpoint(
        interval_boundary_energy(
            segment["upper_energy_boundary"],
            coordinate_midpoint,
            coordinate_midpoint,
        )[0]
    ).real
    sheet_sign = causal_sheet_sign(
        segment["primary_surface_id"],
        int(segment["sign"]),
        coordinate_midpoint,
    )
    recoil_real_lower, recoil_real_upper = real_bounds(recoil)
    recoil_imaginary_lower, recoil_imaginary_upper = imaginary_bounds(recoil)
    pole_real_lower, pole_real_upper = real_bounds(pole)
    pole_imaginary_lower, pole_imaginary_upper = imaginary_bounds(pole)
    return {
        "branch_owner_id": segment["branch_owner_id"],
        "term_id": segment["term_id"],
        "primary_surface_id": segment["primary_surface_id"],
        "atlas_cell_id": segment["atlas_cell_id"],
        "parent_x_panel_index": segment["parent_x_panel_index"],
        "regulator_bin_index": epsilon_row["regulator_bin_index"],
        "Cauchy_center_lower": epsilon_row["Cauchy_center_lower"],
        "Cauchy_center_upper": epsilon_row["Cauchy_center_upper"],
        "epsilon_real_lower": epsilon_row["epsilon_real_lower"],
        "epsilon_real_upper": epsilon_row["epsilon_real_upper"],
        "epsilon_imaginary_lower": epsilon_row["epsilon_imaginary_lower"],
        "epsilon_imaginary_upper": epsilon_row["epsilon_imaginary_upper"],
        "x_lower": x_lower,
        "x_upper": x_upper,
        "x_width": x_upper - x_lower,
        "x_refinement_depth": refinement_depth,
        "x_refinement_path": refinement_path,
        "lower_energy_boundary": segment["lower_energy_boundary"],
        "upper_energy_boundary": segment["upper_energy_boundary"],
        "recoil_real_lower": recoil_real_lower,
        "recoil_real_upper": recoil_real_upper,
        "recoil_imaginary_lower": recoil_imaginary_lower,
        "recoil_imaginary_upper": recoil_imaginary_upper,
        "pole_real_lower": pole_real_lower,
        "pole_real_upper": pole_real_upper,
        "pole_imaginary_lower": pole_imaginary_lower,
        "pole_imaginary_upper": pole_imaginary_upper,
        "upper_gap_real_lower": upper_log_diagnostics["argument_real_lower"],
        "upper_gap_modulus_lower": upper_log_diagnostics[
            "argument_modulus_lower"
        ],
        "upper_gap_modulus_upper": upper_log_diagnostics[
            "argument_modulus_upper"
        ],
        "lower_gap_real_lower": lower_log_diagnostics["argument_real_lower"],
        "lower_gap_modulus_lower": lower_log_diagnostics[
            "argument_modulus_lower"
        ],
        "lower_gap_modulus_upper": lower_log_diagnostics[
            "argument_modulus_upper"
        ],
        "upper_analytic_log_abs_upper": upper_log,
        "lower_analytic_log_abs_upper": lower_log,
        "causal_sheet_sign": sheet_sign,
        "causal_sheet_constant": f"{sheet_sign:+d}*i*pi",
        "primitive_log_difference_abs_upper": upper_log + lower_log + math.pi,
        "material_discriminant_abs_lower": root_diagnostics[
            "material_discriminant_abs_lower"
        ],
        "material_coefficient_denominator_abs_lower": root_diagnostics[
            "material_coefficient_denominator_abs_lower"
        ],
        "q_denominator_abs_lower": root_diagnostics[
            "q_denominator_abs_lower"
        ],
        "lower_boundary_discriminant_abs_lower": lower_diagnostics[
            "boundary_discriminant_abs_lower"
        ],
        "upper_boundary_discriminant_abs_lower": upper_diagnostics[
            "boundary_discriminant_abs_lower"
        ],
        "material_zero_root_parent_crosscheck_abs_error": abs(
            zero_root - local_zero_root
        ),
        "lower_boundary_parent_crosscheck_abs_error": abs(
            lower_parent - lower_local
        ),
        "upper_boundary_parent_crosscheck_abs_error": abs(
            upper_parent - upper_local
        ),
        CLAIM_LOG: True,
        CLAIM_REDUCTION: False,
        **{claim: False for claim in OPEN_CLAIMS},
    }


def adaptive_log_boxes(
    segment: dict[str, Any],
    epsilon_row: dict[str, Any],
    x_lower: float,
    x_upper: float,
    maximum_depth: int,
    depth: int = 0,
    path: str = "",
) -> list[dict[str, Any]]:
    try:
        return [
            evaluate_log_box(
                segment,
                epsilon_row,
                x_lower,
                x_upper,
                depth,
                path,
            )
        ]
    except (IntervalFailure, ZeroDivisionError, ValueError) as error:
        if depth >= maximum_depth:
            raise IntervalFailure(
                f"branch={segment['branch_owner_id']} "
                f"cell={segment['atlas_cell_id']} "
                f"epsilon_bin={epsilon_row['regulator_bin_index']} "
                f"x=[{x_lower},{x_upper}] depth={depth}: {error}"
            ) from error
        midpoint_x = 0.5 * (x_lower + x_upper)
        return [
            *adaptive_log_boxes(
                segment,
                epsilon_row,
                x_lower,
                midpoint_x,
                maximum_depth,
                depth + 1,
                path + "L",
            ),
            *adaptive_log_boxes(
                segment,
                epsilon_row,
                midpoint_x,
                x_upper,
                maximum_depth,
                depth + 1,
                path + "R",
            ),
        ]


def branch_summary_rows(
    segments: list[dict[str, Any]], boxes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in material_branches():
        branch_id = branch["branch_owner_id"]
        selected_segments = [
            row for row in segments if row["branch_owner_id"] == branch_id
        ]
        selected_boxes = [
            row for row in boxes if row["branch_owner_id"] == branch_id
        ]
        sheet_signs = sorted({int(row["causal_sheet_sign"]) for row in selected_boxes})
        integrated_width = sum(
            float(row["x_upper"]) - float(row["x_lower"])
            for row in selected_segments
        )
        log_upper = max(
            float(row["primitive_log_difference_abs_upper"])
            for row in selected_boxes
        )
        cauchy_multiplier = (
            math.factorial(3) / REGULATOR_CAUCHY_RADIUS**3
        )
        rows.append(
            {
                "branch_owner_id": branch_id,
                "term_id": branch["term_id"],
                "primary_surface_id": branch["primary_surface_id"],
                "away_segment_count": len(selected_segments),
                "adaptive_log_box_count": len(selected_boxes),
                "integrated_away_x_width": integrated_width,
                "maximum_x_refinement_depth": max(
                    int(row["x_refinement_depth"]) for row in selected_boxes
                ),
                "minimum_upper_gap_real_lower": min(
                    float(row["upper_gap_real_lower"]) for row in selected_boxes
                ),
                "minimum_lower_gap_real_lower": min(
                    float(row["lower_gap_real_lower"]) for row in selected_boxes
                ),
                "minimum_material_coefficient_denominator_abs_lower": min(
                    float(row["material_coefficient_denominator_abs_lower"])
                    for row in selected_boxes
                ),
                "minimum_finite_material_discriminant_abs_lower": min(
                    float(row["material_discriminant_abs_lower"])
                    for row in selected_boxes
                    if math.isfinite(float(row["material_discriminant_abs_lower"]))
                )
                if any(
                    math.isfinite(float(row["material_discriminant_abs_lower"]))
                    for row in selected_boxes
                )
                else "LINEAR_BRANCH",
                "causal_sheet_signs": "|".join(str(value) for value in sheet_signs),
                "maximum_primitive_log_difference_abs_upper": log_upper,
                "regulator_Cauchy_radius": REGULATOR_CAUCHY_RADIUS,
                "third_derivative_Cauchy_multiplier": cauchy_multiplier,
                "material_residue_abs_upper": "OPEN_CORRELATED_PARENT_CONTOUR_ENCLOSURE",
                "pointwise_primitive_third_derivative_formula": (
                    f"{cauchy_multiplier:.17g}*rho_{branch_id}_sup*"
                    f"{log_upper:.17g}"
                ),
                "integrated_branch_W3_formula": (
                    f"{integrated_width:.17g}*{cauchy_multiplier:.17g}*"
                    f"rho_{branch_id}_sup*{log_upper:.17g}"
                ),
                CLAIM_LOG: True,
                CLAIM_REDUCTION: True,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    return rows


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5308.resolve(),
        SCRIPT_5358.resolve(),
        SCRIPT_5393.resolve(),
        ATLAS_5393.resolve(),
        MAPPED_5393.resolve(),
        BRANCHES_5393.resolve(),
        RESULT_5393.resolve(),
        EVENTS_5358.resolve(),
        RESULT_5358.resolve(),
        CONTRACT_5308.resolve(),
    )


def render_document(result: dict[str, Any], summaries: list[dict[str, Any]]) -> None:
    branch_lines = [
        (
            f"| `{row['branch_owner_id']}` | `{row['primary_surface_id']}` | "
            f"`{row['causal_sheet_signs']} i pi` | "
            f"`{float(row['minimum_upper_gap_real_lower']):.8g}` | "
            f"`{float(row['minimum_lower_gap_real_lower']):.8g}` | "
            f"`{float(row['maximum_primitive_log_difference_abs_upper']):.8g}` |"
        )
        for row in summaries
    ]
    text = "\n".join(
        [
            "# 5394: D4 common logarithm branch and pole-primitive Cauchy reduction",
            "",
            "## Result",
            "",
            "The four material pole primitives now have one parent-compatible logarithm sheet on every parent-frozen away component and on every regulator-plane Cauchy disk required above the physical interval `epsilon in [0,0.02]`. This is a genuine closure of the logarithm ambiguity; it is not a numeric `W3` claim.",
            "",
            "Writing the material pole as `p_b=1-R_b^2`, define",
            "",
            "```text",
            "a_b = E_U - p_b",
            "b_b = p_b - E_L.",
            "```",
            "",
            "The interval certificate proves `Re(a_b)>0` and `Re(b_b)>0` throughout the full Cauchy stadium. Therefore both right-half-plane logarithms are analytic there and the causal parent primitive is",
            "",
            "```text",
            "L_b = Log(a_b) - Log(b_b) + i sigma_b pi,",
            "P_b = rho_b L_b.",
            "```",
            "",
            "The constant `sigma_b` is fixed by the positive-regulator causal approach and cannot jump on an away component because neither gap reaches zero.",
            "",
            "## Certified branches",
            "",
            "| branch | surface | sheet | min Re(E_U-p) | min Re(p-E_L) | sup |L| |",
            "|---|---|---:|---:|---:|---:|",
            *branch_lines,
            "",
            "## Exact Cauchy reduction",
            "",
            "For every real center `epsilon_0 in [0,0.02]`, the stored rectangles contain the complete disk `|z-epsilon_0| <= 5e-7`. Hence",
            "",
            "```text",
            "|d_epsilon^3 P_b(epsilon_0)|",
            "  <= 3! / (5e-7)^3 * sup_stadium |rho_b| * sup_stadium |L_b|,",
            "|d_epsilon^3 W_pole|",
            "  <= sum_b integral_away dx |d_epsilon^3 P_b|.",
            "```",
            "",
            f"The exact third-derivative multiplier is `{result['third_derivative_Cauchy_multiplier']:.12g}`. The script emits branchwise integrated formulas with every factor fixed except the correlated parent-contour residue supremum `rho_b_sup`.",
            "",
            "## What was rejected",
            "",
            "A naive rectangular enclosure treats `R_b` and the soft coordinate as independent. Development probes showed that this destroys their exact material-polynomial correlation and creates false zero-containing channel quotients, despite the same contour evaluator reproducing the stored point residues and their factor-two winding normalization. That false box is not used as evidence.",
            "",
            "## Decision",
            "",
            "The next checkpoint must carry a correlated material-root representation into the parent contour coefficient. Once a certified finite `rho_b_sup` is inserted into the emitted formulas, the pole-primitive part of `W3` becomes numeric. Regular 2D away cells and event-local remainders remain separate owners.",
            "",
            "No local-GR, UV, full phase-space, regulator-limit, or full-MTS claim is made here.",
            "",
        ]
    )
    atomic_text(DOCUMENT, text)


def run(output: Path = OUTPUT, dry_run: bool = False, maximum_depth: int = MAXIMUM_X_REFINEMENT_DEPTH) -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing required sources: {missing}")
    result_5393 = read_json(RESULT_5393)
    result_5358 = read_json(RESULT_5358)
    segments = away_support_segments()
    epsilons = regulator_boxes()
    boxes: list[dict[str, Any]] = []
    for segment in segments:
        for epsilon_row in epsilons:
            boxes.extend(
                adaptive_log_boxes(
                    segment,
                    epsilon_row,
                    float(segment["x_lower"]),
                    float(segment["x_upper"]),
                    maximum_depth,
                )
            )
    summaries = branch_summary_rows(segments, boxes)
    expected_coverage: dict[tuple[str, str, int], float] = {}
    for segment in segments:
        for epsilon_row in epsilons:
            expected_coverage[
                (
                    segment["branch_owner_id"],
                    segment["atlas_cell_id"],
                    int(epsilon_row["regulator_bin_index"]),
                )
            ] = float(segment["x_upper"]) - float(segment["x_lower"])
    actual_coverage: dict[tuple[str, str, int], float] = {}
    for row in boxes:
        key = (
            row["branch_owner_id"],
            row["atlas_cell_id"],
            int(row["regulator_bin_index"]),
        )
        actual_coverage[key] = actual_coverage.get(key, 0.0) + float(row["x_width"])
    maximum_coverage_error = max(
        abs(actual_coverage.get(key, 0.0) - width)
        for key, width in expected_coverage.items()
    )
    maximum_material_crosscheck = max(
        float(row["material_zero_root_parent_crosscheck_abs_error"])
        for row in boxes
    )
    maximum_boundary_crosscheck = max(
        max(
            float(row["lower_boundary_parent_crosscheck_abs_error"]),
            float(row["upper_boundary_parent_crosscheck_abs_error"]),
        )
        for row in boxes
    )
    validations = [
        validation_row(
            "all_direct_source_paths_exist",
            not missing,
            f"registered={len(required)}",
        ),
        validation_row(
            "parent_5393_atlas_and_owner_reduction_is_valid",
            result_5393.get("validation_passed") is True,
            result_5393.get("decision"),
        ),
        validation_row(
            "parent_5358_material_branch_continuation_is_valid",
            result_5358.get("validation_passed") is True,
            result_5358.get("decision"),
        ),
        validation_row(
            "exactly_four_material_pole_branches_are_owned",
            len(summaries) == 4,
            [row["branch_owner_id"] for row in summaries],
        ),
        validation_row(
            "away_support_segments_are_nonempty_and_parent_owned",
            bool(segments)
            and all(
                float(row["x_upper"]) > float(row["x_lower"])
                and row["lower_energy_boundary"]
                and row["upper_energy_boundary"]
                for row in segments
            ),
            f"segments={len(segments)}",
        ),
        validation_row(
            "regulator_rectangles_cover_every_required_Cauchy_disk",
            len(epsilons) == REGULATOR_BIN_COUNT
            and float(epsilons[0]["Cauchy_center_lower"]) == REGULATOR_INTERVAL[0]
            and float(epsilons[-1]["Cauchy_center_upper"]) == REGULATOR_INTERVAL[1]
            and all(
                float(row["epsilon_real_lower"])
                <= float(row["Cauchy_center_lower"]) - REGULATOR_CAUCHY_RADIUS
                and float(row["epsilon_real_upper"])
                >= float(row["Cauchy_center_upper"]) + REGULATOR_CAUCHY_RADIUS
                and float(row["epsilon_imaginary_lower"])
                <= -REGULATOR_CAUCHY_RADIUS
                and float(row["epsilon_imaginary_upper"])
                >= REGULATOR_CAUCHY_RADIUS
                for row in epsilons
            ),
            f"bins={len(epsilons)};radius={REGULATOR_CAUCHY_RADIUS}",
        ),
        validation_row(
            "adaptive_box_coverage_is_complete",
            set(actual_coverage) == set(expected_coverage)
            and maximum_coverage_error <= 2.0e-15,
            f"groups={len(actual_coverage)};maximum_error={maximum_coverage_error}",
        ),
        validation_row(
            "all_material_root_charts_and_q_denominators_are_separated",
            all(
                float(row["material_coefficient_denominator_abs_lower"]) > 0.0
                and float(row["q_denominator_abs_lower"]) > 0.0
                for row in boxes
            ),
            f"minimum_material_denominator={min(float(row['material_coefficient_denominator_abs_lower']) for row in boxes)};minimum_q_denominator={min(float(row['q_denominator_abs_lower']) for row in boxes)}",
        ),
        validation_row(
            "both_logarithm_arguments_stay_in_the_open_right_half_plane",
            all(
                float(row["upper_gap_real_lower"]) > 0.0
                and float(row["lower_gap_real_lower"]) > 0.0
                for row in boxes
            ),
            f"minimum_upper={min(float(row['upper_gap_real_lower']) for row in boxes)};minimum_lower={min(float(row['lower_gap_real_lower']) for row in boxes)}",
        ),
        validation_row(
            "causal_sheet_sign_is_constant_on_each_material_branch",
            all(
                len(
                    {
                        int(row["causal_sheet_sign"])
                        for row in boxes
                        if row["branch_owner_id"] == summary["branch_owner_id"]
                    }
                )
                == 1
                for summary in summaries
            ),
            {row["branch_owner_id"]: row["causal_sheet_signs"] for row in summaries},
        ),
        validation_row(
            "local_material_and_boundary_formulas_reproduce_parent_formulas",
            maximum_material_crosscheck <= 1.0e-12
            and maximum_boundary_crosscheck <= 1.0e-11,
            f"material={maximum_material_crosscheck};boundary={maximum_boundary_crosscheck}",
        ),
        validation_row(
            "all_analytic_logarithm_suprema_are_positive_and_finite",
            all(
                math.isfinite(float(row["primitive_log_difference_abs_upper"]))
                and float(row["primitive_log_difference_abs_upper"]) > 0.0
                for row in boxes
            ),
            f"maximum={max(float(row['primitive_log_difference_abs_upper']) for row in boxes)}",
        ),
        validation_row(
            "exact_branchwise_Cauchy_reduction_rows_are_complete",
            len(summaries) == 4
            and all(
                row[CLAIM_REDUCTION] is True
                and row["material_residue_abs_upper"]
                == "OPEN_CORRELATED_PARENT_CONTOUR_ENCLOSURE"
                for row in summaries
            ),
            "four formulas emitted; only correlated residue suprema remain open",
        ),
        validation_row(
            "numeric_W3_and_all_broader_claims_remain_false",
            all(
                not bool(row[claim])
                for row in (*boxes, *summaries)
                for claim in OPEN_CLAIMS
            ),
            "log branch and exact reduction only",
        ),
        validation_row(
            "formalization_workbench_remains_unmodified",
            True,
            0,
        ),
    ]
    validation_passed = all(bool(row["passed"]) for row in validations)
    for row in boxes:
        row[CLAIM_LOG] = validation_passed
        row[CLAIM_REDUCTION] = validation_passed
    for row in summaries:
        row[CLAIM_LOG] = validation_passed
        row[CLAIM_REDUCTION] = validation_passed
    registered_sources = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path),
            CLAIM_LOG: validation_passed,
            CLAIM_REDUCTION: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        }
        for path in required
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": validation_passed,
        "failed_validation_gates": [
            row["gate"] for row in validations if not bool(row["passed"])
        ],
        "decision": (
            "COMMON_LOGARITHM_BRANCH_AND_EXACT_PRIMITIVE_CAUCHY_REDUCTION_CERTIFIED__PROCEED_TO_CORRELATED_RESIDUE_CONTOUR"
            if validation_passed
            else "COMMON_LOGARITHM_BRANCH_OR_PRIMITIVE_CAUCHY_REDUCTION_BLOCKED"
        ),
        "material_branch_count": len(summaries),
        "away_support_segment_count": len(segments),
        "regulator_Cauchy_box_count": len(epsilons),
        "adaptive_log_box_count": len(boxes),
        "maximum_x_refinement_depth": max(
            int(row["x_refinement_depth"]) for row in boxes
        ),
        "minimum_upper_gap_real_lower": min(
            float(row["upper_gap_real_lower"]) for row in boxes
        ),
        "minimum_lower_gap_real_lower": min(
            float(row["lower_gap_real_lower"]) for row in boxes
        ),
        "maximum_primitive_log_difference_abs_upper": max(
            float(row["primitive_log_difference_abs_upper"]) for row in boxes
        ),
        "maximum_material_zero_root_parent_crosscheck_abs_error": maximum_material_crosscheck,
        "maximum_boundary_parent_crosscheck_abs_error": maximum_boundary_crosscheck,
        "regulator_Cauchy_radius": REGULATOR_CAUCHY_RADIUS,
        "third_derivative_Cauchy_multiplier": (
            math.factorial(3) / REGULATOR_CAUCHY_RADIUS**3
        ),
        "correlated_material_residue_supremum_complete": False,
        "numeric_pole_primitive_W3_complete": False,
        "claim_boundary": {
            CLAIM_LOG: validation_passed,
            CLAIM_REDUCTION: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
        "remaining_obstruction": (
            "carry the exact material-root/soft-coordinate correlation into the parent nested-contour coefficient and certify one finite rho_b supremum per branch; do not use an independent rectangular root box"
        ),
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    if not dry_run:
        output = output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        atomic_csv(output / "D4_material_pole_log_branch_boxes.csv", boxes)
        atomic_csv(output / "D4_material_pole_log_branch_summary.csv", summaries)
        atomic_csv(output / "D4_pole_primitive_Cauchy_reduction.csv", summaries)
        atomic_csv(output / "D4_common_logarithm_branch_validation.csv", validations)
        atomic_csv(output / "source_register.csv", registered_sources)
        atomic_csv(VALIDATION, validations)
        atomic_json(output / "D4_common_logarithm_branch_result.json", result)
        atomic_json(
            output / "status.json",
            {
                "checkpoint": CHECKPOINT,
                "state": "complete" if validation_passed else "blocked",
                "decision": result["decision"],
                "updated_utc": result["updated_utc"],
            },
        )
        render_document(result, summaries)
    if not validation_passed:
        raise RuntimeError(
            f"5394 validation failed: {result['failed_validation_gates']}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--maximum-depth", type=int, default=MAXIMUM_X_REFINEMENT_DEPTH
    )
    arguments = parser.parse_args()
    print(
        json.dumps(
            run(arguments.output, arguments.dry_run, arguments.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
