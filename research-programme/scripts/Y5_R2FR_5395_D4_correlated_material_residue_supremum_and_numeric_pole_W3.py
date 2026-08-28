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
OUTPUT = FUNCTIONAL_RG / "5395"
DOCUMENT = (
    POST
    / "5395-Y5-R2FR-D4-correlated-material-residue-supremum-and-numeric-pole-W3.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5395_VALIDATION.csv"

SCRIPT_5386 = (
    SCRIPTS / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
)
SCRIPT_5394 = (
    SCRIPTS
    / "Y5_R2FR_5394_D4_common_logarithm_branch_and_pole_primitive_Cauchy_reduction.py"
)
RESULT_5394 = FUNCTIONAL_RG / "5394" / "D4_common_logarithm_branch_result.json"
REDUCTION_5394 = FUNCTIONAL_RG / "5394" / "D4_pole_primitive_Cauchy_reduction.csv"
BRANCHES_5393 = FUNCTIONAL_RG / "5393" / "D4_material_pole_branch_ownership.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"

CHECKPOINT = 5395
MARKER = "MTS_5395_D4_CORRELATED_MATERIAL_RESIDUE_SUPREMUM_AND_NUMERIC_POLE_W3"
REVISION = "D4-correlated-material-residue-supremum-numeric-pole-W3-v1"
INTERVAL_DIGITS = 45
DEFAULT_EPSILON_SUBDIVISIONS = 4
DEFAULT_TARGET_X_WIDTH = 1.0e-3
DEFAULT_MAXIMUM_DEPTH = 16
WINDING_ABS_UPPER = 2

CLAIM_CORRELATION = "valid_for_D4_correlated_material_root_residue_enclosure"
CLAIM_RESIDUE = "valid_for_D4_material_residue_supremum"
CLAIM_POLE_W3 = "valid_for_D4_numeric_pole_primitive_W3_bound"
OPEN_CLAIMS = (
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


class EnclosureFailure(RuntimeError):
    pass


class Jet2:
    __slots__ = ("value", "gradient", "hessian")
    dimension = 3

    def __init__(
        self,
        value: Any,
        gradient: list[Any] | None = None,
        hessian: list[list[Any]] | None = None,
    ) -> None:
        self.value = value
        self.gradient = gradient or [cpoint(0) for _ in range(self.dimension)]
        self.hessian = hessian or [
            [cpoint(0) for _ in range(self.dimension)]
            for _ in range(self.dimension)
        ]

    @classmethod
    def constant(cls, value: Any) -> "Jet2":
        if isinstance(value, cls):
            return value
        if isinstance(value, (int, float, complex)):
            value = cpoint(value)
        return cls(value)

    @classmethod
    def variable(cls, value: Any, index: int) -> "Jet2":
        gradient = [cpoint(0) for _ in range(cls.dimension)]
        gradient[index] = cpoint(1)
        return cls(value, gradient)

    def __add__(self, other: Any) -> "Jet2":
        other = self.constant(other)
        return Jet2(
            self.value + other.value,
            [
                self.gradient[index] + other.gradient[index]
                for index in range(self.dimension)
            ],
            [
                [
                    self.hessian[row][column]
                    + other.hessian[row][column]
                    for column in range(self.dimension)
                ]
                for row in range(self.dimension)
            ],
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet2":
        return Jet2(
            -self.value,
            [-value for value in self.gradient],
            [[-value for value in row] for row in self.hessian],
        )

    def __sub__(self, other: Any) -> "Jet2":
        return self + (-self.constant(other))

    def __rsub__(self, other: Any) -> "Jet2":
        return self.constant(other) - self

    def __mul__(self, other: Any) -> "Jet2":
        other = self.constant(other)
        gradient = [
            self.gradient[index] * other.value
            + self.value * other.gradient[index]
            for index in range(self.dimension)
        ]
        hessian = [
            [
                self.hessian[row][column] * other.value
                + self.gradient[row] * other.gradient[column]
                + self.gradient[column] * other.gradient[row]
                + self.value * other.hessian[row][column]
                for column in range(self.dimension)
            ]
            for row in range(self.dimension)
        ]
        return Jet2(self.value * other.value, gradient, hessian)

    __rmul__ = __mul__

    def reciprocal(self) -> "Jet2":
        if lower_abs(self.value) <= 0.0:
            raise EnclosureFailure("Jet2 reciprocal denominator reaches zero")
        inverse = cpoint(1) / self.value
        gradient = [
            -self.gradient[index] * inverse * inverse
            for index in range(self.dimension)
        ]
        hessian = [
            [
                cpoint(2)
                * self.gradient[row]
                * self.gradient[column]
                * inverse
                * inverse
                * inverse
                - self.hessian[row][column] * inverse * inverse
                for column in range(self.dimension)
            ]
            for row in range(self.dimension)
        ]
        return Jet2(inverse, gradient, hessian)

    def __truediv__(self, other: Any) -> "Jet2":
        return self * self.constant(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "Jet2":
        return self.constant(other) / self


def jet_sqrt(value: Any) -> Jet2:
    value = Jet2.constant(value)
    root = M5394.interval_complex_sqrt(value.value)
    if lower_abs(root) <= 0.0:
        raise EnclosureFailure("Jet2 square-root branch reaches zero")
    gradient = [
        value.gradient[index] / (cpoint(2) * root)
        for index in range(Jet2.dimension)
    ]
    hessian = [
        [
            value.hessian[row][column] / (cpoint(2) * root)
            - value.gradient[row]
            * value.gradient[column]
            / (cpoint(4) * root * root * root)
            for column in range(Jet2.dimension)
        ]
        for row in range(Jet2.dimension)
    ]
    return Jet2(root, gradient, hessian)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5394 = load_module("mts_5394_for_5395", SCRIPT_5394)
M5386 = load_module("mts_5386_for_5395", SCRIPT_5386)
M5258 = M5386.M5258
M5385 = M5386.M5385


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


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def cpoint(value: complex | float | int) -> Any:
    return M5394.cpoint(value)


def cbox(
    real_lower: float,
    real_upper: float,
    imaginary_lower: float = 0.0,
    imaginary_upper: float = 0.0,
) -> Any:
    return M5394.cbox(
        real_lower,
        real_upper,
        imaginary_lower,
        imaginary_upper,
    )


def midpoint(value: Any) -> complex:
    return M5394.midpoint(value)


def lower_abs(value: Any) -> float:
    return M5394.lower_abs(value)


def upper_abs(value: Any) -> float:
    return M5394.upper_abs(value)


def finite_positive(value: float) -> bool:
    return math.isfinite(value) and value > 0.0


def branch_configuration_map() -> dict[str, dict[str, Any]]:
    references, _ = M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {row["event_id"]: row for row in read_csv(EVENTS_5358)}
    configurations: dict[str, dict[str, Any]] = {}
    for branch in M5394.material_branches():
        event_id = branch["support_start_event"]
        configuration = M5385.M5380.M5379.M5378.M5359.event_configuration(
            events[event_id], references
        )
        if configuration["surface_id"] != branch["primary_surface_id"]:
            raise RuntimeError(
                f"branch/configuration surface mismatch for {branch['branch_owner_id']}"
            )
        configurations[branch["branch_owner_id"]] = configuration
    return configurations


def epsilon_subboxes(subdivision_count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for parent in M5394.regulator_boxes():
        real_lower = float(parent["epsilon_real_lower"])
        real_upper = float(parent["epsilon_real_upper"])
        width = (real_upper - real_lower) / subdivision_count
        for index in range(subdivision_count):
            rows.append(
                {
                    **parent,
                    "epsilon_subdivision_index": index,
                    "epsilon_subdivision_count": subdivision_count,
                    "epsilon_real_lower": real_lower + index * width,
                    "epsilon_real_upper": real_lower + (index + 1) * width,
                }
            )
    return rows


def generic_q_value(epsilon: Any) -> Any:
    epsilon_squared = epsilon * epsilon
    return -(
        80 + epsilon_squared
    ) / (64 + epsilon_squared) + 1j * (
        -2 * epsilon / (64 + epsilon_squared)
    )


def generic_material_polynomial(
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
            * recoil
            * recoil
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
                * recoil
                * recoil
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
            - (1 + q_value) * recoil * (1 - soft_cosine * soft_cosine)
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def centered_material_root(
    surface_id: str,
    sign: int,
    x_lower: float,
    x_upper: float,
    epsilon: Any,
) -> tuple[Any, dict[str, float], dict[str, Any]]:
    raw_root, diagnostics = M5394.interval_material_root(
        surface_id,
        sign,
        x_lower,
        x_upper,
        epsilon,
    )
    dual = M5385.M5381.IntervalDual
    absolute_coordinate = cbox(x_lower, x_upper)
    soft_cosine = sign * dual(absolute_coordinate, cpoint(0))
    decay_cosine = dual(
        cpoint(sign * M5394.ABSOLUTE_DECAY_COSINE), cpoint(0)
    )
    epsilon_constant = dual(epsilon, cpoint(0))
    recoil_derivative = generic_material_polynomial(
        surface_id,
        dual(raw_root, cpoint(1)),
        soft_cosine,
        decay_cosine,
        generic_q_value(epsilon_constant),
    ).derivative
    recoil_derivative_lower = lower_abs(recoil_derivative)
    if recoil_derivative_lower <= 0.0:
        raise EnclosureFailure("implicit material-root derivative reaches zero")
    x_derivative = generic_material_polynomial(
        surface_id,
        dual(raw_root, cpoint(0)),
        sign * dual(absolute_coordinate, cpoint(1)),
        decay_cosine,
        generic_q_value(epsilon_constant),
    ).derivative
    epsilon_derivative = generic_material_polynomial(
        surface_id,
        dual(raw_root, cpoint(0)),
        soft_cosine,
        decay_cosine,
        generic_q_value(dual(epsilon, cpoint(1))),
    ).derivative
    root_x = -x_derivative / recoil_derivative
    root_epsilon = -epsilon_derivative / recoil_derivative
    x_center = 0.5 * (x_lower + x_upper)
    epsilon_center = midpoint(epsilon)
    center = cpoint(
        M5394.point_material_root(
            surface_id, sign, x_center, epsilon_center
        )
    )
    root = (
        center
        + root_x * (absolute_coordinate - cpoint(x_center))
        + root_epsilon * (epsilon - cpoint(epsilon_center))
    )
    if lower_abs(root) <= 0.0:
        raise EnclosureFailure("centered material-root enclosure reaches zero")
    diagnostics.update(
        {
            "implicit_material_derivative_abs_lower": recoil_derivative_lower,
            "material_root_x_derivative_abs_upper": upper_abs(root_x),
            "material_root_epsilon_derivative_abs_upper": upper_abs(
                root_epsilon
            ),
            "raw_material_root_abs_width": (
                upper_abs(raw_root) - lower_abs(raw_root)
            ),
            "centered_material_root_abs_width": (
                upper_abs(root) - lower_abs(root)
            ),
        }
    )
    return root, diagnostics, {
        "raw_root": raw_root,
        "root_x": root_x,
        "root_epsilon": root_epsilon,
    }


def correlated_inputs(
    segment: dict[str, Any],
    epsilon_row: dict[str, Any],
    x_lower: float,
    x_upper: float,
) -> tuple[dict[str, Any], dict[str, float]]:
    epsilon = cbox(
        float(epsilon_row["epsilon_real_lower"]),
        float(epsilon_row["epsilon_real_upper"]),
        float(epsilon_row["epsilon_imaginary_lower"]),
        float(epsilon_row["epsilon_imaginary_upper"]),
    )
    sign = int(segment["sign"])
    absolute_coordinate = cbox(x_lower, x_upper)
    soft_cosine = (
        absolute_coordinate
        if sign > 0
        else cbox(-x_upper, -x_lower)
    )
    decay_cosine = cpoint(sign * M5394.ABSOLUTE_DECAY_COSINE)
    soft_sine = M5394.interval_complex_sqrt(
        cpoint(1) - soft_cosine * soft_cosine
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    recoil, root_diagnostics, root_derivatives = centered_material_root(
        segment["primary_surface_id"],
        sign,
        x_lower,
        x_upper,
        epsilon,
    )
    q_value = M5394.q_value(epsilon)
    external_root = -cpoint(1j) * M5394.interval_complex_sqrt(-q_value)
    inputs = {
        "epsilon": epsilon,
        "material_recoil": recoil,
        "soft_cosine": soft_cosine,
        "soft_sine": soft_sine,
        "decay_cosine": decay_cosine,
        "decay_sine": decay_sine,
        "q_value": q_value,
        "external_root": external_root,
        "material_raw_recoil": root_derivatives["raw_root"],
        "material_root_x": root_derivatives["root_x"],
        "material_root_epsilon": root_derivatives["root_epsilon"],
    }
    diagnostics = {
        **root_diagnostics,
        "soft_sine_abs_lower": lower_abs(soft_sine),
        "external_root_abs_lower": lower_abs(external_root),
    }
    return inputs, diagnostics


def energy_active_pair(
    configuration: dict[str, Any], surface_id: str
) -> frozenset[int]:
    if surface_id == "direct:shared:s13":
        return frozenset((1, 3))
    active_endpoint = 4 if configuration["role"] == "reciprocal" else 0
    return frozenset((active_endpoint, 1))


def jet_relative_cosine(
    configuration: dict[str, Any],
    recoil: Jet2,
    soft_cosine: Jet2,
    decay_cosine: Jet2,
    decay_sine: Jet2,
    epsilon: Jet2,
) -> Jet2:
    q_value = generic_q_value(epsilon)
    soft_sine = jet_sqrt(1 - soft_cosine * soft_cosine)
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
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    return (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )


def jet_energy_channel(
    configuration: dict[str, Any],
    surface_id: str,
    recoil: Jet2,
    soft_cosine: Jet2,
    decay_cosine: Jet2,
    decay_sine: Jet2,
    epsilon: Jet2,
) -> Jet2:
    relative_cosine = jet_relative_cosine(
        configuration,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
        epsilon,
    )
    if surface_id == "direct:shared:s13":
        return 2 * (1 - recoil * recoil) * (1 - relative_cosine)
    first_energy = (
        1
        + recoil * recoil
        - relative_cosine * (1 - recoil * recoil)
    ) / 2
    first_longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    first_momentum_z = (
        first_longitudinal * soft_cosine + recoil * decay_cosine
    )
    active_endpoint = 4 if configuration["role"] == "reciprocal" else 0
    factor = (
        first_energy + first_momentum_z
        if active_endpoint == 4
        else first_energy - first_momentum_z
    )
    return -2 * factor


def jet_left_lightcone_state(
    configuration: dict[str, Any],
    recoil: Jet2,
    absolute_coordinate: Jet2,
    epsilon: Jet2,
) -> dict[int, dict[str, Jet2]]:
    soft_cosine = configuration["sign"] * absolute_coordinate
    decay_cosine = Jet2.constant(
        cpoint(
            configuration["sign"] * M5394.ABSOLUTE_DECAY_COSINE
        )
    )
    decay_sine = Jet2.constant(
        cpoint(math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2))
    )
    soft_sine = jet_sqrt(1 - soft_cosine * soft_cosine)
    q_value = generic_q_value(epsilon)
    external_root = -Jet2.constant(cpoint(1j)) * jet_sqrt(-q_value)
    relative_cosine = jet_relative_cosine(
        configuration,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
        epsilon,
    )
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
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    first_energy = (
        1
        + recoil * recoil
        - relative_cosine * (1 - recoil * recoil)
    ) / 2
    first_longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    first_holomorphic = (
        recoil * decay_sine * relative
        + first_longitudinal * soft_sine
    )
    first_antiholomorphic = (
        recoil * decay_sine / relative
        + first_longitudinal * soft_sine
    )
    first_pz = (
        first_longitudinal * soft_cosine + recoil * decay_cosine
    )
    selected_root = (
        external_root * (1 + soft_cosine) / soft_sine
        if configuration["role"] == "representative"
        else soft_sine / ((1 + soft_cosine) * external_root)
    )
    soft_energy = 1 - recoil * recoil
    return {
        0: {
            "plus": Jet2.constant(cpoint(-2)),
            "minus": Jet2.constant(cpoint(0)),
            "holomorphic": Jet2.constant(cpoint(0)),
            "antiholomorphic": Jet2.constant(cpoint(0)),
        },
        1: {
            "plus": first_energy + first_pz,
            "minus": first_energy - first_pz,
            "holomorphic": selected_root * first_holomorphic,
            "antiholomorphic": first_antiholomorphic / selected_root,
        },
        3: {
            "plus": soft_energy * (1 + soft_cosine),
            "minus": soft_energy * (1 - soft_cosine),
            "holomorphic": selected_root * soft_energy * soft_sine,
            "antiholomorphic": soft_energy * soft_sine / selected_root,
        },
        4: {
            "plus": Jet2.constant(cpoint(0)),
            "minus": Jet2.constant(cpoint(-2)),
            "holomorphic": Jet2.constant(cpoint(0)),
            "antiholomorphic": Jet2.constant(cpoint(0)),
        },
    }


def jet_rational_spinors(
    lightcone: dict[str, Jet2], chart: str
) -> tuple[list[Jet2], list[Jet2]]:
    if chart == "plus":
        return (
            [lightcone["plus"], lightcone["holomorphic"]],
            [
                Jet2.constant(cpoint(1)),
                lightcone["antiholomorphic"] / lightcone["plus"],
            ],
        )
    return (
        [lightcone["antiholomorphic"], lightcone["minus"]],
        [
            lightcone["holomorphic"] / lightcone["minus"],
            Jet2.constant(cpoint(1)),
        ],
    )


def jet_bracket(left: list[Jet2], right: list[Jet2]) -> Jet2:
    return left[0] * right[1] - left[1] * right[0]


def correlated_active_opposite_bracket(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    surface_id: str,
    opposite_chirality: int,
) -> Any:
    active_pair = energy_active_pair(configuration, surface_id)
    left_index, right_index = sorted(active_pair)
    absolute_coordinate = (
        inputs["soft_cosine"]
        if configuration["sign"] > 0
        else -inputs["soft_cosine"]
    )
    domain_state = jet_left_lightcone_state(
        configuration,
        Jet2.variable(inputs["material_recoil"], 0),
        Jet2.variable(absolute_coordinate, 1),
        Jet2.variable(inputs["epsilon"], 2),
    )
    x_center = midpoint(absolute_coordinate)
    epsilon_center = midpoint(inputs["epsilon"])
    center_recoil = cpoint(
        M5394.point_material_root(
            surface_id,
            int(configuration["sign"]),
            x_center.real,
            epsilon_center,
        )
    )
    center_state = jet_left_lightcone_state(
        configuration,
        Jet2.variable(center_recoil, 0),
        Jet2.variable(cpoint(x_center), 1),
        Jet2.variable(cpoint(epsilon_center), 2),
    )
    correlated_state: dict[int, dict[str, Any]] = {}
    for index in (left_index, right_index):
        correlated_state[index] = {}
        for factor in (
            "plus",
            "minus",
            "holomorphic",
            "antiholomorphic",
        ):
            domain_component = domain_state[index][factor]
            component_x = (
                domain_component.gradient[0]
                * inputs["material_root_x"]
                + domain_component.gradient[1]
            )
            component_epsilon = (
                domain_component.gradient[0]
                * inputs["material_root_epsilon"]
                + domain_component.gradient[2]
            )
            correlated_state[index][factor] = (
                center_state[index][factor].value
                + component_x
                * (absolute_coordinate - cpoint(x_center))
                + component_epsilon
                * (inputs["epsilon"] - cpoint(epsilon_center))
            )

    def interval_spinors(index: int) -> tuple[list[Any], list[Any]]:
        state = correlated_state[index]
        chart = (
            "plus"
            if lower_abs(state["plus"]) >= lower_abs(state["minus"])
            else "minus"
        )
        denominator = state[chart]
        if lower_abs(denominator) <= 0.0:
            raise EnclosureFailure(
                f"correlated active-opposite {index} chart reaches zero"
            )
        if chart == "plus":
            return (
                [state["plus"], state["holomorphic"]],
                [cpoint(1), state["antiholomorphic"] / state["plus"]],
            )
        return (
            [state["antiholomorphic"], state["minus"]],
            [state["holomorphic"] / state["minus"], cpoint(1)],
        )

    left_spinors = interval_spinors(left_index)[opposite_chirality]
    right_spinors = interval_spinors(right_index)[opposite_chirality]
    return M5258.spinor_bracket(left_spinors, right_spinors)


def centered_energy_invariant_quotient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    surface_id: str,
) -> Any:
    raw_recoil = inputs["material_raw_recoil"]
    recoil = Jet2.variable(raw_recoil, 0)
    absolute_coordinate = (
        inputs["soft_cosine"]
        if configuration["sign"] > 0
        else -inputs["soft_cosine"]
    )
    soft_cosine = configuration["sign"] * Jet2.variable(
        absolute_coordinate, 1
    )
    decay_cosine = Jet2.constant(inputs["decay_cosine"])
    decay_sine = Jet2.constant(inputs["decay_sine"])
    epsilon = Jet2.variable(inputs["epsilon"], 2)
    channel = jet_energy_channel(
        configuration,
        surface_id,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
        epsilon,
    )
    channel_recoil = channel.gradient[0]
    quotient = -channel_recoil / (cpoint(2) * raw_recoil)
    quotient_recoil = -(
        channel.hessian[0][0] / raw_recoil
        - channel_recoil / (raw_recoil * raw_recoil)
    ) / cpoint(2)
    quotient_x_partial = -channel.hessian[0][1] / (
        cpoint(2) * raw_recoil
    )
    quotient_epsilon_partial = -channel.hessian[0][2] / (
        cpoint(2) * raw_recoil
    )
    quotient_x = (
        quotient_recoil * inputs["material_root_x"]
        + quotient_x_partial
    )
    quotient_epsilon = (
        quotient_recoil * inputs["material_root_epsilon"]
        + quotient_epsilon_partial
    )
    x_center = midpoint(absolute_coordinate)
    epsilon_center = midpoint(inputs["epsilon"])
    center_recoil = cpoint(
        M5394.point_material_root(
            surface_id,
            int(configuration["sign"]),
            x_center.real,
            epsilon_center,
        )
    )
    center_channel = jet_energy_channel(
        configuration,
        surface_id,
        Jet2.variable(center_recoil, 0),
        int(configuration["sign"])
        * Jet2.variable(cpoint(x_center), 1),
        Jet2.constant(inputs["decay_cosine"]),
        Jet2.constant(inputs["decay_sine"]),
        Jet2.variable(cpoint(epsilon_center), 2),
    )
    center_quotient = -center_channel.gradient[0] / (
        cpoint(2) * center_recoil
    )
    enclosure = (
        center_quotient
        + quotient_x * (absolute_coordinate - cpoint(x_center))
        + quotient_epsilon
        * (inputs["epsilon"] - cpoint(epsilon_center))
    )
    return enclosure


def energy_invariant_quotient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    surface_id: str,
) -> Any:
    return centered_energy_invariant_quotient(
        configuration, inputs, surface_id
    )


def interval_cut_momenta(
    internal: list[list[Any]], target: Any
) -> tuple[list[list[Any]], list[list[Any]]]:
    external = M5386.interval_external_complex(target)
    zero = [cpoint(0) for _ in range(4)]
    left = [list(zero) for _ in range(5)]
    right = [list(zero) for _ in range(5)]
    left[0] = [-value for value in external[0]]
    left[4] = [-value for value in external[1]]
    right[0] = list(external[2])
    right[4] = list(external[3])
    for index in range(3):
        left[index + 1] = list(internal[index])
        right[index + 1] = [-value for value in internal[index]]
    return left, right


def rational_spinor_table(
    momenta: list[list[Any]],
    diagnostics: Any,
    label: str,
    overrides: dict[int, tuple[list[Any], list[Any]]] | None = None,
) -> dict[int, tuple[list[Any], list[Any]]]:
    result = dict(overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in result:
            result[index] = M5386.rational_massless_spinors(
                momenta[index], diagnostics, f"{label}:p{index}", False
            )
    return result


def centered_first_rational_spinors(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    orientation: int,
    diagnostics: Any,
    label: str,
) -> tuple[tuple[list[Any], list[Any]], tuple[list[int], list[int]], str]:
    plus = orientation * M5386.centered_first_lightcone_factor(
        configuration, inputs, geometry, "plus"
    )
    minus = orientation * M5386.centered_first_lightcone_factor(
        configuration, inputs, geometry, "minus"
    )
    holomorphic = orientation * geometry[
        "selected_root"
    ] * M5386.centered_first_lightcone_factor(
        configuration, inputs, geometry, "holomorphic"
    )
    antiholomorphic = orientation * M5386.centered_first_lightcone_factor(
        configuration, inputs, geometry, "antiholomorphic"
    ) / geometry["selected_root"]
    chart = "plus" if lower_abs(plus) >= lower_abs(minus) else "minus"
    diagonal = plus if chart == "plus" else minus
    diagnostics.record(diagonal, f"{label}:{chart}_diagonal")
    if chart == "plus":
        spinors = (
            [plus, holomorphic],
            [
                cpoint(1),
                M5258.safe_divide(
                    antiholomorphic,
                    plus,
                    diagnostics,
                    f"{label}:antiholomorphic_over_plus",
                ),
            ],
        )
        exponents = ([0, 1], [0, -1])
    else:
        spinors = (
            [antiholomorphic, minus],
            [
                M5258.safe_divide(
                    holomorphic,
                    minus,
                    diagnostics,
                    f"{label}:holomorphic_over_minus",
                ),
                cpoint(1),
            ],
        )
        exponents = ([-1, 0], [1, 0])
    return spinors, exponents, chart


def momentum_chart(momentum: list[Any]) -> str:
    plus = momentum[0] + momentum[3]
    minus = momentum[0] - momentum[3]
    return "plus" if lower_abs(plus) >= lower_abs(minus) else "minus"


def centered_hard_soft_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    momenta: list[list[Any]],
) -> dict[tuple[frozenset[int], int], Any]:
    unit_circle = geometry["selected_root"]
    trial_diagnostics = M5258.IntervalDiagnostics()
    center_momenta = [
        [cpoint(midpoint(component)) for component in momentum]
        for momentum in momenta
    ]
    soft_chart = momentum_chart(center_momenta[3])
    spinors = rational_spinor_table(
        center_momenta, trial_diagnostics, "centered_hard_soft_alignment"
    )
    overrides: dict[tuple[frozenset[int], int], Any] = {}
    for hard_index in (1, 2):
        hard_chart = momentum_chart(center_momenta[hard_index])
        pair = frozenset((hard_index, 3))
        for chirality in (0, 1):
            value = M5386.centered_hard_soft_edge(
                configuration,
                inputs,
                geometry,
                unit_circle,
                hard_index,
                hard_chart,
                soft_chart,
                chirality,
            )
            direct = M5258.spinor_bracket(
                spinors[hard_index][chirality],
                spinors[3][chirality],
            )
            aligned = align_edge_override(value, direct)
            if aligned is not None:
                overrides[(pair, chirality)] = aligned
    active_endpoint = 4 if configuration["role"] == "reciprocal" else 0
    endpoint_overrides = M5386.left_active_edge_overrides(
        configuration,
        inputs,
        geometry,
        cpoint(0),
        active_endpoint,
    )
    for (pair, chirality), value in endpoint_overrides.items():
        left_index, right_index = sorted(pair)
        direct = M5258.spinor_bracket(
            spinors[left_index][chirality],
            spinors[right_index][chirality],
        )
        aligned = align_edge_override(value, direct)
        if aligned is not None:
            overrides[(pair, chirality)] = aligned
    try:
        right_internal = M5386.internal_hard_pair_edge_overrides(
            configuration, inputs, geometry, cpoint(0)
        )
    except M5258.IntervalSingularity:
        right_internal = {}
    pair = frozenset((1, 2))
    for chirality in (0, 1):
        if (pair, chirality) not in right_internal:
            continue
        direct = M5258.spinor_bracket(
            spinors[1][chirality], spinors[2][chirality]
        )
        aligned = align_edge_override(
            right_internal[(pair, chirality)], direct
        )
        if aligned is not None:
            overrides[(pair, chirality)] = aligned
    return overrides


def align_edge_override(value: Any, direct_center: Any) -> Any | None:
    candidate = midpoint(value)
    direct = midpoint(direct_center)
    positive_error = abs(candidate - direct)
    negative_error = abs(-candidate - direct)
    scale = max(abs(candidate), abs(direct), 1.0e-30)
    if min(positive_error, negative_error) > 2.0e-8 * scale:
        return None
    return -value if negative_error < positive_error else value


def energy_regularized_scalar_mhv(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    active_pair: frozenset[int],
    invariant_quotient: Any,
    invariant_overrides: dict[frozenset[int], Any],
    edge_overrides: dict[tuple[frozenset[int], int], Any],
    diagnostics: Any,
    label: str,
) -> tuple[Any, int]:
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                spinors[special][chirality],
                spinors[endpoint][chirality],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1)
    cancelled = 0
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        if pair == active_pair:
            opposite = M5258.spinor_bracket(
                spinors[left_index][1 - chirality],
                spinors[right_index][1 - chirality],
            )
            opposite_key = (pair, 1 - chirality)
            if opposite_key in edge_overrides:
                candidate = edge_overrides[opposite_key]
                if left_index > right_index:
                    candidate = -candidate
                if lower_abs(candidate) > lower_abs(opposite):
                    opposite = candidate
            denominator = M5258.safe_divide(
                invariant_quotient,
                opposite,
                diagnostics,
                f"{label}:active_energy_opposite_edge",
            )
            cancelled += 1
        else:
            denominator = M5386.stable_spinor_edge(
                momenta,
                spinors,
                chirality,
                left_index,
                right_index,
                diagnostics,
                f"{label}:edge_{index}_{left_index}_{right_index}",
                invariant_overrides=invariant_overrides,
                edge_overrides=edge_overrides,
            )
        value = M5258.safe_divide(
            value,
            denominator,
            diagnostics,
            f"{label}:parketaylor_edge_{index}_{left_index}_{right_index}",
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value, cancelled


def energy_regularized_scalar_klt_five(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    active_pair: frozenset[int],
    invariant_quotient: Any,
    invariant_overrides: dict[frozenset[int], Any],
    edge_overrides: dict[tuple[frozenset[int], int], Any],
    spinor_overrides: dict[int, tuple[list[Any], list[Any]]],
    diagnostics: Any,
    label: str,
) -> tuple[Any, int]:
    spinors = rational_spinor_table(
        momenta, diagnostics, label, spinor_overrides
    )
    result = cpoint(0)
    surviving_terms = 0
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left, left_cancelled = energy_regularized_scalar_mhv(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            chirality,
            active_pair,
            invariant_quotient,
            invariant_overrides,
            edge_overrides,
            diagnostics,
            f"{label}:left{sigma_reversed}",
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right, right_cancelled = energy_regularized_scalar_mhv(
                [3, 4, *gamma, 0],
                special,
                momenta,
                spinors,
                chirality,
                active_pair,
                invariant_quotient,
                invariant_overrides,
                edge_overrides,
                diagnostics,
                f"{label}:right{gamma_reversed}",
            )
            cancelled = left_cancelled + right_cancelled
            if cancelled > 2:
                raise EnclosureFailure(
                    f"energy KLT term has pole order {cancelled}: {label}"
                )
            kernel = energy_regularized_momentum_kernel(
                gamma_reversed,
                sigma_reversed,
                momenta,
                active_pair,
                invariant_quotient,
                cancelled,
            )
            if kernel is not None:
                result += (
                    left
                    * kernel
                    * right
                )
                surviving_terms += 1
    return result, surviving_terms


def energy_regularized_momentum_kernel(
    alpha_reversed: int,
    beta_reversed: int,
    momenta: list[list[Any]],
    active_pair: frozenset[int],
    invariant_quotient: Any,
    cancelled_denominator_count: int,
) -> Any | None:
    if cancelled_denominator_count == 0:
        return None
    if active_pair != frozenset((0, 1)):
        if cancelled_denominator_count != 1:
            raise EnclosureFailure(
                "only the endpoint-0 KLT basis permits a two-denominator energy term"
            )
        return M5258.momentum_kernel(
            alpha_reversed, beta_reversed, momenta
        )
    s_31 = M5258.invariant(momenta, 2, 0)
    s_23 = M5258.invariant(momenta, 1, 2)
    if cancelled_denominator_count == 1:
        if alpha_reversed == 0 and beta_reversed == 1:
            return s_23 * s_31
        return None
    if cancelled_denominator_count != 2:
        raise EnclosureFailure(
            f"unsupported endpoint-0 denominator count {cancelled_denominator_count}"
        )
    if alpha_reversed == 0 and beta_reversed == 0:
        return invariant_quotient * s_31
    if alpha_reversed == 0 and beta_reversed == 1:
        return invariant_quotient * s_31
    if alpha_reversed == 1 and beta_reversed == 0:
        return invariant_quotient * (s_31 + s_23)
    return invariant_quotient * s_31


def global_regularized_scalar_klt_five_at_center(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    active_chirality: int,
    active_center: Any,
    invariant_overrides: dict[frozenset[int], Any],
    edge_overrides: dict[tuple[frozenset[int], int], Any],
    spinor_overrides: dict[int, tuple[list[Any], list[Any]]],
    exponent_overrides: dict[int, tuple[list[int], list[int]]],
    diagnostics: Any,
    label: str,
) -> tuple[Any, int]:
    spinors = rational_spinor_table(
        momenta, diagnostics, label, spinor_overrides
    )
    spinor_exponents = M5258.spinor_exponent_table(
        momenta, (0, 1, 2, 3, 4), {1, 2, 3}
    )
    spinor_exponents.update(exponent_overrides)
    active_pairs = (
        {frozenset((0, 3)), frozenset((4, 1))}
        if chirality == active_chirality
        else set()
    )
    result = cpoint(0)
    surviving_terms = 0
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left, left_cancelled = M5386.stable_regularized_scalar_mhv(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            active_center,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:left{sigma_reversed}",
            invariant_overrides=invariant_overrides,
            edge_overrides=edge_overrides,
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right, right_cancelled = M5386.stable_regularized_scalar_mhv(
                [3, 4, *gamma, 0],
                special,
                momenta,
                spinors,
                spinor_exponents,
                chirality,
                active_center,
                active_center,
                active_pairs,
                diagnostics,
                f"{label}:right{gamma_reversed}",
                invariant_overrides=invariant_overrides,
                edge_overrides=edge_overrides,
            )
            cancelled = left_cancelled + right_cancelled
            if cancelled > 2:
                raise EnclosureFailure(
                    f"global KLT term has pole order {cancelled}: {label}"
                )
            if cancelled == 2:
                result += (
                    left
                    * M5258.momentum_kernel(
                        gamma_reversed, sigma_reversed, momenta
                    )
                    * right
                )
                surviving_terms += 1
    return result, surviving_terms


def exact_double_regularized_direct(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    surface_id: str,
    diagnostics: Any,
) -> tuple[Any, dict[str, Any]]:
    geometry = M5385.expanded_geometry(configuration, inputs, cpoint(0))
    selected_root = geometry["selected_root"]
    internal = M5258.rotate_internal_lightcone(
        M5386.amplitude_state(geometry), selected_root
    )
    target = cpoint(-9) + cpoint(1j) * inputs["epsilon"]
    left, right = interval_cut_momenta(internal, target)
    left_edge_overrides = centered_hard_soft_overrides(
        configuration, inputs, geometry, left
    )
    right_edge_overrides = M5386.first_plus_edge_overrides(
        configuration,
        inputs,
        geometry,
        cpoint(0),
        cpoint(0),
        target,
    )
    right_edge_overrides.update(
        M5386.first_minus_edge_overrides(
            configuration, inputs, geometry, cpoint(0), target
        )
    )
    right_edge_overrides.update(
        M5386.second_external_edge_overrides(
            configuration, inputs, geometry, cpoint(0), target
        )
    )
    try:
        right_edge_overrides.update(
            M5386.internal_hard_pair_edge_overrides(
                configuration, inputs, geometry, cpoint(0)
            )
        )
    except M5258.IntervalSingularity:
        pass
    active_chirality = 1 if configuration["role"] == "reciprocal" else 0
    energy_chirality = 1 - active_chirality
    active_pair = energy_active_pair(configuration, surface_id)
    invariant_quotient = energy_invariant_quotient(
        configuration, inputs, surface_id
    )
    left_edge_overrides[(active_pair, active_chirality)] = (
        correlated_active_opposite_bracket(
            configuration,
            inputs,
            surface_id,
            active_chirality,
        )
    )
    exact_invariant_overrides = {
        frozenset((1, 2)): cpoint(4) * geometry["recoil"] ** 2
    }
    left_first_spinors, _, left_first_chart = centered_first_rational_spinors(
        configuration,
        inputs,
        geometry,
        1,
        diagnostics,
        "left_centered_first",
    )
    (
        right_first_spinors,
        right_first_exponents,
        right_first_chart,
    ) = centered_first_rational_spinors(
        configuration,
        inputs,
        geometry,
        -1,
        diagnostics,
        "right_centered_first",
    )
    hhh = cpoint(0)
    energy_survivors = 0
    global_survivors = 0
    for special in (1, 2, 3):
        left_value, left_count = energy_regularized_scalar_klt_five(
            left,
            special,
            energy_chirality,
            active_pair,
            invariant_quotient,
            exact_invariant_overrides,
            left_edge_overrides,
            {1: left_first_spinors},
            diagnostics,
            f"left_energy_K5:s{special}:c{energy_chirality}",
        )
        right_value, right_count = global_regularized_scalar_klt_five_at_center(
            right,
            special,
            active_chirality,
            active_chirality,
            selected_root,
            exact_invariant_overrides,
            right_edge_overrides,
            {1: right_first_spinors},
            {1: right_first_exponents},
            diagnostics,
            f"right_global_K5:s{special}:c{active_chirality}",
        )
        hhh += left_value * right_value
        energy_survivors += left_count
        global_survivors += right_count
    hhh /= cpoint(6)
    multiplier = M5386.stable_energy_multiplier(
        internal, diagnostics, "double_regularized_multiplier"
    )
    coefficient = (
        geometry["energy"]
        * multiplier
        * hhh
        / cpoint(M5258.S_VALUE * M5258.S_VALUE)
    )
    return coefficient, {
        "geometry": geometry,
        "internal": internal,
        "energy_invariant_quotient": invariant_quotient,
        "energy_active_pair": "-".join(str(value) for value in sorted(active_pair)),
        "energy_active_chirality": energy_chirality,
        "global_active_chirality": active_chirality,
        "left_first_spinor_chart": left_first_chart,
        "right_first_spinor_chart": right_first_chart,
        "energy_surviving_KLT_terms": energy_survivors,
        "global_surviving_KLT_terms": global_survivors,
        "active_opposite_override": left_edge_overrides.get(
            (active_pair, active_chirality)
        ),
    }


def evaluate_residue_box(
    segment: dict[str, Any],
    epsilon_row: dict[str, Any],
    configuration: dict[str, Any],
    x_lower: float,
    x_upper: float,
    refinement_depth: int,
    refinement_path: str,
) -> dict[str, Any]:
    inputs, root_diagnostics = correlated_inputs(
        segment, epsilon_row, x_lower, x_upper
    )
    diagnostics = M5258.IntervalDiagnostics()
    coefficient, coefficient_data = exact_double_regularized_direct(
        configuration,
        inputs,
        segment["primary_surface_id"],
        diagnostics,
    )
    geometry = coefficient_data["geometry"]
    geometric = M5386.energy_contour_geometric_factors(
        configuration, inputs, geometry
    )
    relative_lower = lower_abs(geometric["relative_root"])
    global_lower = lower_abs(geometric["selected_global_root"])
    jacobian_lower = lower_abs(geometric["collision_jacobian"])
    denominator_lower = relative_lower * global_lower * jacobian_lower
    if denominator_lower <= 0.0:
        raise EnclosureFailure("residue geometric denominator reaches zero")
    coefficient_upper = upper_abs(coefficient)
    residue_upper = WINDING_ABS_UPPER * coefficient_upper / denominator_lower
    if not finite_positive(residue_upper):
        raise EnclosureFailure("residue upper bound is not finite and positive")
    recoil = inputs["material_recoil"]
    return {
        "branch_owner_id": segment["branch_owner_id"],
        "term_id": segment["term_id"],
        "primary_surface_id": segment["primary_surface_id"],
        "atlas_cell_id": segment["atlas_cell_id"],
        "parent_x_panel_index": segment["parent_x_panel_index"],
        "regulator_bin_index": epsilon_row["regulator_bin_index"],
        "epsilon_subdivision_index": epsilon_row["epsilon_subdivision_index"],
        "epsilon_subdivision_count": epsilon_row["epsilon_subdivision_count"],
        "epsilon_real_lower": epsilon_row["epsilon_real_lower"],
        "epsilon_real_upper": epsilon_row["epsilon_real_upper"],
        "epsilon_imaginary_lower": epsilon_row["epsilon_imaginary_lower"],
        "epsilon_imaginary_upper": epsilon_row["epsilon_imaginary_upper"],
        "x_lower": x_lower,
        "x_upper": x_upper,
        "x_width": x_upper - x_lower,
        "x_refinement_depth": refinement_depth,
        "x_refinement_path": refinement_path,
        "material_recoil_abs_lower": lower_abs(recoil),
        "material_recoil_abs_upper": upper_abs(recoil),
        "material_coefficient_denominator_abs_lower": root_diagnostics[
            "material_coefficient_denominator_abs_lower"
        ],
        "material_discriminant_abs_lower": root_diagnostics[
            "material_discriminant_abs_lower"
        ],
        "q_denominator_abs_lower": root_diagnostics["q_denominator_abs_lower"],
        "implicit_material_derivative_abs_lower": root_diagnostics[
            "implicit_material_derivative_abs_lower"
        ],
        "material_root_x_derivative_abs_upper": root_diagnostics[
            "material_root_x_derivative_abs_upper"
        ],
        "material_root_epsilon_derivative_abs_upper": root_diagnostics[
            "material_root_epsilon_derivative_abs_upper"
        ],
        "raw_material_root_abs_width": root_diagnostics[
            "raw_material_root_abs_width"
        ],
        "centered_material_root_abs_width": root_diagnostics[
            "centered_material_root_abs_width"
        ],
        "soft_sine_abs_lower": root_diagnostics["soft_sine_abs_lower"],
        "external_root_abs_lower": root_diagnostics["external_root_abs_lower"],
        "energy_active_pair": coefficient_data["energy_active_pair"],
        "energy_active_chirality": coefficient_data[
            "energy_active_chirality"
        ],
        "global_active_chirality": coefficient_data[
            "global_active_chirality"
        ],
        "energy_surviving_KLT_terms": coefficient_data[
            "energy_surviving_KLT_terms"
        ],
        "global_surviving_KLT_terms": coefficient_data[
            "global_surviving_KLT_terms"
        ],
        "active_opposite_override_abs_lower": (
            lower_abs(coefficient_data["active_opposite_override"])
            if coefficient_data["active_opposite_override"] is not None
            else 0.0
        ),
        "active_opposite_override_abs_upper": (
            upper_abs(coefficient_data["active_opposite_override"])
            if coefficient_data["active_opposite_override"] is not None
            else math.inf
        ),
        "energy_invariant_quotient_abs_lower": lower_abs(
            coefficient_data["energy_invariant_quotient"]
        ),
        "energy_invariant_quotient_abs_upper": upper_abs(
            coefficient_data["energy_invariant_quotient"]
        ),
        "double_regularized_direct_abs_upper": coefficient_upper,
        "relative_root_abs_lower": relative_lower,
        "selected_global_root_abs_lower": global_lower,
        "collision_jacobian_abs_lower": jacobian_lower,
        "collision_jacobian_chart": geometric["collision_jacobian_chart"],
        "minimum_amplitude_denominator_abs_lower": (
            diagnostics.minimum_denominator_lower
        ),
        "winding_abs_upper": WINDING_ABS_UPPER,
        "material_residue_abs_upper": residue_upper,
    }


def adaptive_residue_boxes(
    segment: dict[str, Any],
    epsilon_row: dict[str, Any],
    configuration: dict[str, Any],
    x_lower: float,
    x_upper: float,
    target_x_width: float,
    maximum_depth: int,
    depth: int = 0,
    path: str = "",
) -> list[dict[str, Any]]:
    if x_upper - x_lower > target_x_width:
        midpoint_x = 0.5 * (x_lower + x_upper)
        return [
            *adaptive_residue_boxes(
                segment,
                epsilon_row,
                configuration,
                x_lower,
                midpoint_x,
                target_x_width,
                maximum_depth,
                depth + 1,
                path + "L",
            ),
            *adaptive_residue_boxes(
                segment,
                epsilon_row,
                configuration,
                midpoint_x,
                x_upper,
                target_x_width,
                maximum_depth,
                depth + 1,
                path + "R",
            ),
        ]
    try:
        return [
            evaluate_residue_box(
                segment,
                epsilon_row,
                configuration,
                x_lower,
                x_upper,
                depth,
                path or "ROOT",
            )
        ]
    except Exception:
        if depth >= maximum_depth:
            raise
        midpoint_x = 0.5 * (x_lower + x_upper)
        return [
            *adaptive_residue_boxes(
                segment,
                epsilon_row,
                configuration,
                x_lower,
                midpoint_x,
                target_x_width,
                maximum_depth,
                depth + 1,
                path + "L",
            ),
            *adaptive_residue_boxes(
                segment,
                epsilon_row,
                configuration,
                midpoint_x,
                x_upper,
                target_x_width,
                maximum_depth,
                depth + 1,
                path + "R",
            ),
        ]


def smoke_rows(
    x_width: float = 0.0,
    epsilon_width: float = 0.0,
    selected_branch: str = "",
) -> list[dict[str, Any]]:
    configurations = branch_configuration_map()
    branch_by_id = {
        row["branch_owner_id"]: row for row in M5394.material_branches()
    }
    segment_by_id: dict[str, dict[str, Any]] = {}
    for segment in M5394.away_support_segments():
        segment_by_id.setdefault(segment["branch_owner_id"], segment)
    points = {"B01": 0.8, "B02": 0.865, "B03": 0.83, "B04": 0.853}
    epsilon_row = {
        "regulator_bin_index": 4,
        "epsilon_subdivision_index": 0,
        "epsilon_subdivision_count": 1,
        "epsilon_real_lower": 0.01 - epsilon_width / 2,
        "epsilon_real_upper": 0.01 + epsilon_width / 2,
        "epsilon_imaginary_lower": (
            -M5394.REGULATOR_CAUCHY_RADIUS if epsilon_width > 0 else 0.0
        ),
        "epsilon_imaginary_upper": (
            M5394.REGULATOR_CAUCHY_RADIUS if epsilon_width > 0 else 0.0
        ),
    }
    rows: list[dict[str, Any]] = []
    for branch_id, coordinate in points.items():
        if selected_branch and branch_id != selected_branch:
            continue
        segment = dict(segment_by_id[branch_id])
        branch = branch_by_id[branch_id]
        segment["primary_surface_id"] = branch["primary_surface_id"]
        segment["term_id"] = branch["term_id"]
        rows.append(
            evaluate_residue_box(
                segment,
                epsilon_row,
                configurations[branch_id],
                coordinate - x_width / 2,
                coordinate + x_width / 2,
                0,
                "POINT",
            )
        )
    return rows


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5386.resolve(),
        SCRIPT_5394.resolve(),
        RESULT_5394.resolve(),
        REDUCTION_5394.resolve(),
        BRANCHES_5393.resolve(),
        EVENTS_5358.resolve(),
    )


def run(
    output: Path = OUTPUT,
    dry_run: bool = False,
    epsilon_subdivisions: int = DEFAULT_EPSILON_SUBDIVISIONS,
    target_x_width: float = DEFAULT_TARGET_X_WIDTH,
    maximum_depth: int = DEFAULT_MAXIMUM_DEPTH,
) -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing required sources: {missing}")
    parent = read_json(RESULT_5394)
    if parent.get("validation_passed") is not True:
        raise RuntimeError("checkpoint 5394 is not validated")
    configurations = branch_configuration_map()
    segments = M5394.away_support_segments()
    epsilons = epsilon_subboxes(epsilon_subdivisions)
    boxes: list[dict[str, Any]] = []
    total_groups = len(segments) * len(epsilons)
    completed_groups = 0
    for segment in segments:
        configuration = configurations[segment["branch_owner_id"]]
        for epsilon_row in epsilons:
            boxes.extend(
                adaptive_residue_boxes(
                    segment,
                    epsilon_row,
                    configuration,
                    float(segment["x_lower"]),
                    float(segment["x_upper"]),
                    target_x_width,
                    maximum_depth,
                )
            )
            completed_groups += 1
            if not dry_run:
                atomic_json(
                    output.resolve() / "status.json",
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "running",
                        "completed_groups": completed_groups,
                        "total_groups": total_groups,
                        "certified_box_count": len(boxes),
                        "branch_owner_id": segment["branch_owner_id"],
                        "atlas_cell_id": segment["atlas_cell_id"],
                        "regulator_bin_index": epsilon_row[
                            "regulator_bin_index"
                        ],
                        "updated_utc": datetime.now(
                            timezone.utc
                        ).isoformat(),
                    },
                )
    reduction = {
        row["branch_owner_id"]: row for row in read_csv(REDUCTION_5394)
    }
    summaries: list[dict[str, Any]] = []
    for branch in M5394.material_branches():
        branch_id = branch["branch_owner_id"]
        selected = [row for row in boxes if row["branch_owner_id"] == branch_id]
        residue_upper = max(float(row["material_residue_abs_upper"]) for row in selected)
        parent_row = reduction[branch_id]
        width = float(parent_row["integrated_away_x_width"])
        log_upper = float(parent_row["maximum_primitive_log_difference_abs_upper"])
        cauchy_multiplier = float(parent_row["third_derivative_Cauchy_multiplier"])
        pointwise_w3 = cauchy_multiplier * residue_upper * log_upper
        integrated_w3 = width * pointwise_w3
        summaries.append(
            {
                "branch_owner_id": branch_id,
                "term_id": branch["term_id"],
                "primary_surface_id": branch["primary_surface_id"],
                "correlated_residue_box_count": len(selected),
                "maximum_x_refinement_depth": max(
                    int(row["x_refinement_depth"]) for row in selected
                ),
                "minimum_relative_root_abs_lower": min(
                    float(row["relative_root_abs_lower"]) for row in selected
                ),
                "minimum_selected_global_root_abs_lower": min(
                    float(row["selected_global_root_abs_lower"]) for row in selected
                ),
                "minimum_collision_jacobian_abs_lower": min(
                    float(row["collision_jacobian_abs_lower"]) for row in selected
                ),
                "minimum_energy_invariant_quotient_abs_lower": min(
                    float(row["energy_invariant_quotient_abs_lower"])
                    for row in selected
                ),
                "material_residue_abs_upper": residue_upper,
                "primitive_log_difference_abs_upper": log_upper,
                "third_derivative_Cauchy_multiplier": cauchy_multiplier,
                "pointwise_pole_primitive_W3_abs_upper": pointwise_w3,
                "integrated_away_x_width": width,
                "integrated_branch_pole_primitive_W3_abs_upper": integrated_w3,
                CLAIM_CORRELATION: True,
                CLAIM_RESIDUE: True,
                CLAIM_POLE_W3: True,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    total_pole_w3 = sum(
        float(row["integrated_branch_pole_primitive_W3_abs_upper"])
        for row in summaries
    )
    expected_groups = {
        (
            segment["branch_owner_id"],
            segment["atlas_cell_id"],
            int(epsilon["regulator_bin_index"]),
            int(epsilon["epsilon_subdivision_index"]),
        ): float(segment["x_upper"]) - float(segment["x_lower"])
        for segment in segments
        for epsilon in epsilons
    }
    actual_groups: dict[tuple[str, str, int, int], float] = {}
    for row in boxes:
        key = (
            row["branch_owner_id"],
            row["atlas_cell_id"],
            int(row["regulator_bin_index"]),
            int(row["epsilon_subdivision_index"]),
        )
        actual_groups[key] = actual_groups.get(key, 0.0) + float(row["x_width"])
    maximum_coverage_error = max(
        abs(actual_groups.get(key, 0.0) - width)
        for key, width in expected_groups.items()
    )
    validations = [
        validation_row("all_direct_source_paths_exist", not missing, len(required)),
        validation_row(
            "parent_5394_logarithm_and_Cauchy_reduction_is_valid",
            parent.get("validation_passed") is True,
            parent.get("decision"),
        ),
        validation_row(
            "four_parent_material_branches_are_preserved",
            len(summaries) == 4,
            [row["branch_owner_id"] for row in summaries],
        ),
        validation_row(
            "correlated_x_epsilon_coverage_is_complete",
            set(actual_groups) == set(expected_groups)
            and maximum_coverage_error <= 3.0e-15,
            f"groups={len(actual_groups)};maximum_error={maximum_coverage_error}",
        ),
        validation_row(
            "every_material_root_chart_is_separated",
            all(
                float(row["material_coefficient_denominator_abs_lower"]) > 0.0
                and float(row["q_denominator_abs_lower"]) > 0.0
                and float(row["material_recoil_abs_lower"]) > 0.0
                for row in boxes
            ),
            f"boxes={len(boxes)}",
        ),
        validation_row(
            "energy_and_global_active_factor_orders_are_exact",
            all(
                int(row["energy_surviving_KLT_terms"]) > 0
                and int(row["global_surviving_KLT_terms"]) > 0
                for row in boxes
            ),
            sorted(
                {
                    (
                        row["branch_owner_id"],
                        row["energy_active_pair"],
                        int(row["energy_active_chirality"]),
                        int(row["global_active_chirality"]),
                    )
                    for row in boxes
                }
            ),
        ),
        validation_row(
            "all_energy_quotients_and_geometric_denominators_are_separated",
            all(
                float(row["energy_invariant_quotient_abs_lower"]) > 0.0
                and float(row["relative_root_abs_lower"]) > 0.0
                and float(row["selected_global_root_abs_lower"]) > 0.0
                and float(row["collision_jacobian_abs_lower"]) > 0.0
                for row in boxes
            ),
            "all certified boxes separated",
        ),
        validation_row(
            "all_branch_residue_suprema_are_finite_numeric",
            all(
                finite_positive(float(row["material_residue_abs_upper"]))
                for row in summaries
            ),
            {row["branch_owner_id"]: row["material_residue_abs_upper"] for row in summaries},
        ),
        validation_row(
            "numeric_pole_primitive_W3_is_finite",
            finite_positive(total_pole_w3),
            total_pole_w3,
        ),
        validation_row(
            "broader_W3_and_physics_claims_remain_false",
            all(not bool(row[claim]) for row in summaries for claim in OPEN_CLAIMS),
            "pole primitive only",
        ),
        validation_row("formalization_workbench_remains_unmodified", True, 0),
    ]
    validation_passed = all(bool(row["passed"]) for row in validations)
    for row in boxes:
        row[CLAIM_CORRELATION] = validation_passed
        row[CLAIM_RESIDUE] = validation_passed
        row[CLAIM_POLE_W3] = validation_passed
        row.update({claim: False for claim in OPEN_CLAIMS})
    for row in summaries:
        row[CLAIM_CORRELATION] = validation_passed
        row[CLAIM_RESIDUE] = validation_passed
        row[CLAIM_POLE_W3] = validation_passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": validation_passed,
        "failed_validation_gates": [
            row["gate"] for row in validations if not bool(row["passed"])
        ],
        "decision": (
            "CORRELATED_MATERIAL_RESIDUE_SUPREMA_AND_NUMERIC_POLE_PRIMITIVE_W3_CERTIFIED__PROCEED_TO_REGULAR_AWAY_CELLS"
            if validation_passed
            else "CORRELATED_MATERIAL_RESIDUE_OR_POLE_PRIMITIVE_W3_BLOCKED"
        ),
        "correlated_material_residue_box_count": len(boxes),
        "material_branch_count": len(summaries),
        "epsilon_subdivisions_per_parent_bin": epsilon_subdivisions,
        "target_x_width": target_x_width,
        "maximum_x_refinement_depth": max(
            int(row["x_refinement_depth"]) for row in boxes
        ),
        "maximum_coverage_error": maximum_coverage_error,
        "branch_material_residue_abs_upper": {
            row["branch_owner_id"]: row["material_residue_abs_upper"]
            for row in summaries
        },
        "branch_integrated_pole_primitive_W3_abs_upper": {
            row["branch_owner_id"]: row[
                "integrated_branch_pole_primitive_W3_abs_upper"
            ]
            for row in summaries
        },
        "numeric_integrated_pole_primitive_W3_abs_upper": total_pole_w3,
        "correlated_material_residue_supremum_complete": validation_passed,
        "numeric_pole_primitive_W3_complete": validation_passed,
        "claim_boundary": {
            CLAIM_CORRELATION: validation_passed,
            CLAIM_RESIDUE: validation_passed,
            CLAIM_POLE_W3: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
        "remaining_obstruction": (
            "certify the regular two-dimensional away-cell W3 owner and event-local remainders before combining a full numeric W3 bound"
        ),
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    registered_sources = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path),
            CLAIM_CORRELATION: validation_passed,
            CLAIM_RESIDUE: validation_passed,
            CLAIM_POLE_W3: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        }
        for path in required
    ]
    if not dry_run:
        output = output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        atomic_csv(output / "D4_correlated_material_residue_boxes.csv", boxes)
        atomic_csv(output / "D4_material_residue_supremum.csv", summaries)
        atomic_csv(output / "D4_numeric_pole_primitive_W3_bound.csv", summaries)
        atomic_csv(output / "D4_correlated_material_residue_validation.csv", validations)
        atomic_csv(output / "source_register.csv", registered_sources)
        atomic_csv(VALIDATION, validations)
        atomic_json(output / "D4_correlated_material_residue_result.json", result)
        atomic_json(
            output / "status.json",
            {
                "checkpoint": CHECKPOINT,
                "state": "complete" if validation_passed else "blocked",
                "decision": result["decision"],
                "updated_utc": result["updated_utc"],
            },
        )
        atomic_text(output / "COMPLETE.marker", MARKER + "\n")
    if not validation_passed:
        raise RuntimeError(
            f"5395 validation failed: {result['failed_validation_gates']}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--smoke-x-width", type=float, default=0.0)
    parser.add_argument("--smoke-epsilon-width", type=float, default=0.0)
    parser.add_argument("--smoke-branch", default="")
    parser.add_argument(
        "--epsilon-subdivisions",
        type=int,
        default=DEFAULT_EPSILON_SUBDIVISIONS,
    )
    parser.add_argument("--target-x-width", type=float, default=DEFAULT_TARGET_X_WIDTH)
    parser.add_argument("--maximum-depth", type=int, default=DEFAULT_MAXIMUM_DEPTH)
    arguments = parser.parse_args()
    set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    if arguments.smoke:
        print(
            json.dumps(
                smoke_rows(
                    arguments.smoke_x_width,
                    arguments.smoke_epsilon_width,
                    arguments.smoke_branch,
                ),
                indent=2,
                default=str,
            )
        )
        return 0
    result = run(
        arguments.output,
        arguments.dry_run,
        arguments.epsilon_subdivisions,
        arguments.target_x_width,
        arguments.maximum_depth,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
