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
import numpy as np


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
OUTPUT = FUNCTIONAL_RG / "5380"
DOCUMENT = POST / "5380-Y5-R2FR-D4-complexified-event-neighborhood-certificate.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5380_VALIDATION.csv"

SCRIPT_5379 = SCRIPTS / "Y5_R2FR_5379_D4_parametric_interval_newton_event_atlas.py"
RESULT_5379 = FUNCTIONAL_RG / "5379" / "D4_parametric_interval_Newton_result.json"
VALIDATION_5379 = FUNCTIONAL_RG / "5379" / "D4_parametric_interval_Newton_validation.csv"
BOXES_5379 = FUNCTIONAL_RG / "5379" / "D4_parametric_interval_Newton_boxes.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"

CHECKPOINT = 5380
MARKER = "MTS_5380_D4_COMPLEXIFIED_EVENT_NEIGHBORHOOD_CERTIFICATE"
REVISION = "D4-complexified-event-neighborhood-certificate-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
EPSILON_MINIMUM = 0.0
EPSILON_MAXIMUM = 0.02
EPSILON_BIN_COUNT = 8
EPSILON_IMAGINARY_HALF_WIDTH = 1.0e-6
IMAGINARY_STATE_PADDING_FACTOR = 12.0
STATE_BOX_INFLATION_SAFETY_FACTOR = 1.5
STATE_BOX_INFLATION_MAXIMUM_STEPS = 8
STATE_BOX_INFLATION_ABSOLUTE_BUFFER = 1.0e-14
INTERVAL_DIGITS = 50
MP_DIGITS = 110

CLAIM_COMPLEX = "valid_for_D4_common_closed_complex_event_neighborhood"
OPEN_CLAIMS = (
    "valid_for_D4_endpoint_C_regulator_zero_limit",
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


M5379 = load_module("mts_5379_for_5380", SCRIPT_5379)
mp = M5379.mp


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5379.set_below_normal_priority()


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


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def open_claims() -> dict[str, bool]:
    return {claim: False for claim in OPEN_CLAIMS}


def source_paths() -> tuple[Path, ...]:
    return tuple(
        path.resolve()
        for path in (
            Path(__file__),
            SCRIPT_5379,
            RESULT_5379,
            VALIDATION_5379,
            BOXES_5379,
            EVENTS_5358,
        )
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_COMPLEX: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    result = read_json(RESULT_5379)
    boxes = read_csv(BOXES_5379)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in source_paths()),
        "checkpoint_5379_passes": result.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5379)),
        "real_interval_atlas_is_claimed": result.get("claim_boundary", {}).get(
            M5379.CLAIM_REAL_ATLAS
        )
        is True,
        "all_64_real_boxes_pass": len(boxes) == 64
        and all(parse_bool(row["box_certificate_passes"]) for row in boxes),
        "formal_workbench_inventory_is_unchanged": M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5379.M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def real_interval(lower: Any, upper: Any) -> Any:
    return iv.mpf([str(lower), str(upper)])


def complex_box(
    real_lower: Any,
    real_upper: Any,
    imaginary_lower: Any,
    imaginary_upper: Any,
) -> Any:
    return iv.mpc(
        [str(real_lower), str(real_upper)],
        [str(imaginary_lower), str(imaginary_upper)],
    )


def complex_point(value: complex | float) -> Any:
    value = complex(value)
    return complex_box(value.real, value.real, value.imag, value.imag)


def lower(value: Any) -> float:
    return float(value.a)


def upper(value: Any) -> float:
    return float(value.b)


def real_lower(value: Any) -> float:
    return lower(value.real)


def real_upper(value: Any) -> float:
    return upper(value.real)


def imaginary_lower(value: Any) -> float:
    return lower(value.imag)


def imaginary_upper(value: Any) -> float:
    return upper(value.imag)


def complex_midpoint(value: Any) -> complex:
    return complex(
        0.5 * (real_lower(value) + real_upper(value)),
        0.5 * (imaginary_lower(value) + imaginary_upper(value)),
    )


def complex_sup_abs(value: Any) -> float:
    real_bound = max(abs(real_lower(value)), abs(real_upper(value)))
    imaginary_bound = max(
        abs(imaginary_lower(value)), abs(imaginary_upper(value))
    )
    return math.hypot(real_bound, imaginary_bound)


def complex_interval_text(value: Any) -> str:
    return (
        f"[{real_lower(value):.17g},{real_upper(value):.17g}]"
        f"+i[{imaginary_lower(value):.17g},{imaginary_upper(value):.17g}]"
    )


class MultiDual:
    def __init__(self, value: Any, derivatives: list[Any]) -> None:
        self.value = value
        self.derivatives = derivatives

    @property
    def dimension(self) -> int:
        return len(self.derivatives)

    @classmethod
    def constant(cls, value: Any, dimension: int) -> "MultiDual":
        if not hasattr(value, "real"):
            value = complex_point(value)
        return cls(value, [complex_point(0) for _ in range(dimension)])

    @classmethod
    def variable(cls, value: Any, dimension: int, index: int) -> "MultiDual":
        derivatives = [complex_point(0) for _ in range(dimension)]
        derivatives[index] = complex_point(1)
        return cls(value, derivatives)

    def coerce(self, value: Any) -> "MultiDual":
        return value if isinstance(value, MultiDual) else self.constant(value, self.dimension)

    def __add__(self, other: Any) -> "MultiDual":
        other = self.coerce(other)
        return MultiDual(
            self.value + other.value,
            [
                left + right
                for left, right in zip(self.derivatives, other.derivatives)
            ],
        )

    __radd__ = __add__

    def __neg__(self) -> "MultiDual":
        return MultiDual(-self.value, [-value for value in self.derivatives])

    def __sub__(self, other: Any) -> "MultiDual":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "MultiDual":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "MultiDual":
        other = self.coerce(other)
        return MultiDual(
            self.value * other.value,
            [
                left * other.value + self.value * right
                for left, right in zip(self.derivatives, other.derivatives)
            ],
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "MultiDual":
        other = self.coerce(other)
        return MultiDual(
            self.value / other.value,
            [
                (left * other.value - self.value * right) / other.value**2
                for left, right in zip(self.derivatives, other.derivatives)
            ],
        )

    def __rtruediv__(self, other: Any) -> "MultiDual":
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> "MultiDual":
        return MultiDual(
            self.value**exponent,
            [
                exponent * self.value ** (exponent - 1) * derivative
                for derivative in self.derivatives
            ],
        )


class AlgebraicPair:
    def __init__(self, real: MultiDual, imaginary: MultiDual) -> None:
        self.real = real
        self.imaginary = imaginary

    def coerce(self, value: Any) -> "AlgebraicPair":
        if isinstance(value, AlgebraicPair):
            return value
        scalar = self.real.coerce(value)
        return AlgebraicPair(scalar, MultiDual.constant(0, scalar.dimension))

    def __add__(self, other: Any) -> "AlgebraicPair":
        other = self.coerce(other)
        return AlgebraicPair(
            self.real + other.real, self.imaginary + other.imaginary
        )

    __radd__ = __add__

    def __neg__(self) -> "AlgebraicPair":
        return AlgebraicPair(-self.real, -self.imaginary)

    def __sub__(self, other: Any) -> "AlgebraicPair":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "AlgebraicPair":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "AlgebraicPair":
        other = self.coerce(other)
        return AlgebraicPair(
            self.real * other.real - self.imaginary * other.imaginary,
            self.real * other.imaginary + self.imaginary * other.real,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "AlgebraicPair":
        if exponent == 2:
            return self * self
        raise ValueError("only square powers are required")


def material_pair(
    surface_id: str,
    recoil: AlgebraicPair,
    soft_cosine: MultiDual,
    decay_cosine: Any,
    q_value: AlgebraicPair,
) -> AlgebraicPair:
    cosine = q_value.coerce(soft_cosine)
    decay = q_value.coerce(decay_cosine)
    common = (cosine - decay) * (
        q_value * (1 + cosine) + cosine - 1
    )
    if surface_id == "direct:L:s14":
        return (
            (1 + cosine)
            * (1 + q_value)
            * (cosine + decay)
            * recoil**2
            + 2
            * (1 + cosine)
            * (1 - cosine - q_value * cosine)
            * recoil
            + common
        )
    if surface_id == "direct:L:s01":
        return (
            (1 - cosine)
            * (
                -(1 + q_value)
                * (cosine + decay)
                * recoil**2
                + 2
                * recoil
                * (q_value * (1 + cosine) + cosine)
            )
            + common
        )
    if surface_id == "direct:shared:s13":
        return (
            (cosine - decay)
            * (1 - cosine - q_value * (1 + cosine))
            - (1 + q_value) * recoil * (1 - cosine**2)
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def complexified_system(
    configuration: dict[str, Any], epsilon: Any, variable_boxes: list[Any]
) -> tuple[list[Any], list[list[Any]]]:
    dimension = len(variable_boxes)
    variables = [
        MultiDual.variable(value, dimension, index)
        for index, value in enumerate(variable_boxes)
    ]
    epsilon_squared = epsilon**2
    q_real = -(80 + epsilon_squared) / (64 + epsilon_squared)
    q_imaginary = -2 * epsilon / (64 + epsilon_squared)
    q_pair = AlgebraicPair(
        MultiDual.constant(q_real, dimension),
        MultiDual.constant(q_imaginary, dimension),
    )
    recoil_pair = AlgebraicPair(variables[0], variables[1])
    coordinate = variables[2] if configuration["event_type"] == "BRANCH_DEATH" else variables[3]
    soft_cosine = configuration["sign"] * coordinate
    decay_cosine = complex_point(configuration["decay_cosine"])
    polynomial = material_pair(
        configuration["surface_id"],
        recoil_pair,
        soft_cosine,
        decay_cosine,
        q_pair,
    )
    functions = [polynomial.real, polynomial.imaginary]
    if configuration["event_type"] == "BRANCH_DEATH":
        functions.append(
            variables[0] ** 2
            - variables[1] ** 2
            - M5379.M5378.M5359.M5358.R_MINIMUM**2
        )
    else:
        hard_recoil = variables[2]
        soft_sine = variables[4]
        decay = MultiDual.constant(decay_cosine, dimension)
        decay_sine = MultiDual.constant(
            complex_point(mp.sqrt(1 - configuration["decay_cosine"] ** 2)),
            dimension,
        )
        relative = soft_cosine * decay - soft_sine * decay_sine
        target = MultiDual.constant(complex_point(-0.3), dimension)
        hard_value = (
            (soft_cosine - target) * (1 + relative) * hard_recoil**2
            + 2 * (decay - soft_cosine * relative) * hard_recoil
            + (soft_cosine + target) * (relative - 1)
        )
        functions.extend(
            (
                hard_value,
                hard_recoil**2 - variables[0] ** 2 + variables[1] ** 2,
                soft_sine**2 + soft_cosine**2 - 1,
            )
        )
    return (
        [function.value for function in functions],
        [function.derivatives for function in functions],
    )


def parse_real_interval(text: str) -> tuple[float, float]:
    left, right = text.strip()[1:-1].split(",")
    return float(left), float(right)


def point_solution(
    configuration: dict[str, Any], epsilon: float, zero_coordinate: Any
) -> list[float]:
    values = M5379.point_solution(configuration, epsilon, zero_coordinate)
    if configuration["event_type"] != "BRANCH_DEATH":
        coordinate = values[3]
        soft_cosine = configuration["sign"] * coordinate
        values.append(math.sqrt(1 - soft_cosine**2))
    return values


def complex_state_boxes(
    configuration: dict[str, Any],
    real_source: dict[str, str],
    samples: list[list[float]],
    epsilon_width: float,
) -> list[Any]:
    real_bounds = [
        parse_real_interval(real_source["recoil_real_box"]),
        parse_real_interval(real_source["recoil_imaginary_box"]),
    ]
    if configuration["event_type"] != "BRANCH_DEATH":
        real_bounds.append(parse_real_interval(real_source["hard_recoil_box"]))
    real_bounds.append(parse_real_interval(real_source["event_coordinate_box"]))
    if configuration["event_type"] != "BRANCH_DEATH":
        sine_values = [sample[-1] for sample in samples]
        sine_span = max(sine_values) - min(sine_values)
        sine_padding = max(150 * sine_span, 1.0e-12)
        real_bounds.append(
            (
                min(sine_values) - sine_padding,
                max(sine_values) + sine_padding,
            )
        )
    boxes: list[Any] = []
    for index, (real_lower_bound, real_upper_bound) in enumerate(real_bounds):
        sample_values = [sample[index] for sample in samples]
        slope_bound = max(
            abs(sample_values[1] - sample_values[0]),
            abs(sample_values[2] - sample_values[1]),
            abs(sample_values[2] - sample_values[0]) / 2,
        ) / (epsilon_width / 2)
        imaginary_half_width = max(
            IMAGINARY_STATE_PADDING_FACTOR
            * slope_bound
            * EPSILON_IMAGINARY_HALF_WIDTH,
            5.0e-9,
        )
        boxes.append(
            complex_box(
                real_lower_bound,
                real_upper_bound,
                -imaginary_half_width,
                imaginary_half_width,
            )
        )
    return boxes


def point_jacobian(
    configuration: dict[str, Any], epsilon: float, center: list[float]
) -> np.ndarray:
    epsilon_point = complex_point(epsilon)
    center_boxes = [complex_point(value) for value in center]
    _, jacobian = complexified_system(configuration, epsilon_point, center_boxes)
    return np.asarray(
        [[complex_midpoint(value) for value in row] for row in jacobian],
        dtype=complex,
    )


def krawczyk_certificate(
    configuration: dict[str, Any],
    epsilon_bounds: tuple[float, float],
    state_boxes: list[Any],
    center: list[float],
) -> dict[str, Any]:
    epsilon_midpoint = 0.5 * sum(epsilon_bounds)
    epsilon_box = complex_box(
        epsilon_bounds[0],
        epsilon_bounds[1],
        -EPSILON_IMAGINARY_HALF_WIDTH,
        EPSILON_IMAGINARY_HALF_WIDTH,
    )
    jacobian_point = point_jacobian(configuration, epsilon_midpoint, center)
    inverse = np.linalg.inv(jacobian_point)
    center_boxes = [complex_point(value) for value in center]
    functions, _ = complexified_system(configuration, epsilon_box, center_boxes)
    _, jacobian = complexified_system(configuration, epsilon_box, state_boxes)
    dimension = len(state_boxes)
    operator: list[Any] = []
    matrix_remainder: list[list[Any]] = []
    for row_index in range(dimension):
        correction = complex_point(0)
        for column_index in range(dimension):
            correction += complex_point(inverse[row_index, column_index]) * functions[
                column_index
            ]
        remainder_row: list[Any] = []
        remainder_value = complex_point(0)
        for column_index in range(dimension):
            matrix_value = complex_point(
                1 if row_index == column_index else 0
            )
            for inner_index in range(dimension):
                matrix_value -= (
                    complex_point(inverse[row_index, inner_index])
                    * jacobian[inner_index][column_index]
                )
            remainder_row.append(matrix_value)
            remainder_value += matrix_value * (
                state_boxes[column_index] - center[column_index]
            )
        matrix_remainder.append(remainder_row)
        operator.append(center[row_index] - correction + remainder_value)
    inclusion_margins: list[float] = []
    for state_box, image in zip(state_boxes, operator):
        inclusion_margins.extend(
            (
                real_lower(image) - real_lower(state_box),
                real_upper(state_box) - real_upper(image),
                imaginary_lower(image) - imaginary_lower(state_box),
                imaginary_upper(state_box) - imaginary_upper(image),
            )
        )
    contraction_bound = max(
        sum(complex_sup_abs(value) for value in row)
        for row in matrix_remainder
    )
    return {
        "operator": operator,
        "minimum_inclusion_margin": min(inclusion_margins),
        "contraction_bound": contraction_bound,
        "point_jacobian_condition_number": float(np.linalg.cond(jacobian_point)),
        "passes": min(inclusion_margins) > 0 and contraction_bound < 1,
    }


def inflate_state_box(
    state_boxes: list[Any], operator: list[Any]
) -> list[Any]:
    inflated: list[Any] = []
    for state_box, image in zip(state_boxes, operator):
        state_real_lower = real_lower(state_box)
        state_real_upper = real_upper(state_box)
        state_imaginary_lower = imaginary_lower(state_box)
        state_imaginary_upper = imaginary_upper(state_box)
        real_lower_deficit = max(0.0, state_real_lower - real_lower(image))
        real_upper_deficit = max(0.0, real_upper(image) - state_real_upper)
        imaginary_lower_deficit = max(
            0.0, state_imaginary_lower - imaginary_lower(image)
        )
        imaginary_upper_deficit = max(
            0.0, imaginary_upper(image) - state_imaginary_upper
        )
        inflated.append(
            complex_box(
                state_real_lower
                - STATE_BOX_INFLATION_SAFETY_FACTOR * real_lower_deficit
                - (
                    STATE_BOX_INFLATION_ABSOLUTE_BUFFER
                    if real_lower_deficit > 0
                    else 0
                ),
                state_real_upper
                + STATE_BOX_INFLATION_SAFETY_FACTOR * real_upper_deficit
                + (
                    STATE_BOX_INFLATION_ABSOLUTE_BUFFER
                    if real_upper_deficit > 0
                    else 0
                ),
                state_imaginary_lower
                - STATE_BOX_INFLATION_SAFETY_FACTOR * imaginary_lower_deficit
                - (
                    STATE_BOX_INFLATION_ABSOLUTE_BUFFER
                    if imaginary_lower_deficit > 0
                    else 0
                ),
                state_imaginary_upper
                + STATE_BOX_INFLATION_SAFETY_FACTOR * imaginary_upper_deficit
                + (
                    STATE_BOX_INFLATION_ABSOLUTE_BUFFER
                    if imaginary_upper_deficit > 0
                    else 0
                ),
            )
        )
    return inflated


def construct_certified_state_box(
    configuration: dict[str, Any],
    epsilon_bounds: tuple[float, float],
    initial_state_boxes: list[Any],
    center: list[float],
) -> tuple[list[Any], dict[str, Any], int]:
    state_boxes = initial_state_boxes
    certificate = krawczyk_certificate(
        configuration, epsilon_bounds, state_boxes, center
    )
    inflation_steps = 0
    while (
        not certificate["passes"]
        and certificate["contraction_bound"] < 1
        and inflation_steps < STATE_BOX_INFLATION_MAXIMUM_STEPS
    ):
        state_boxes = inflate_state_box(state_boxes, certificate["operator"])
        inflation_steps += 1
        certificate = krawczyk_certificate(
            configuration, epsilon_bounds, state_boxes, center
        )
    return state_boxes, certificate, inflation_steps


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5380 - D4 complexified event-neighborhood certificate",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Construction",
        "",
        "The real component equations certified in checkpoint 5379 are complexified as analytic algebraic equations. Branch deaths use three complex unknowns. Support contacts use five, with `s^2+c^2=1` replacing the soft-angle square root. This avoids an unsupported complex interval square-root branch.",
        "",
        f"Each real regulator bin is thickened to `|Im epsilon| <= {EPSILON_IMAGINARY_HALF_WIDTH}` and tested by a complex rectangular Krawczyk operator. Failed faces are enlarged only by their measured inclusion deficit, with safety factor `{STATE_BOX_INFLATION_SAFETY_FACTOR}`, and the complete operator is recomputed for at most `{STATE_BOX_INFLATION_MAXIMUM_STEPS}` steps.",
        "",
        f"- certified boxes: `{result['certified_box_count']}/{result['required_box_count']}`;",
        f"- maximum contraction bound: `{result['maximum_contraction_bound']}`;",
        f"- minimum strict real/imaginary inclusion margin: `{result['minimum_inclusion_margin']}`.",
        "",
        "## Scope",
        "",
        "This certifies the analytic event branches on a common closed complex epsilon neighborhood. It does not yet interval-enclose the parent residue and its amplitude denominators there, so the strict endpoint-C theorem, H3, W3, D4 outer limit and broader claims remain open.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    mp.mp.dps = MP_DIGITS
    iv.dps = INTERVAL_DIGITS
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    references, _ = M5379.M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    event_lookup = {row["event_id"]: row for row in events}
    real_boxes = read_csv(BOXES_5379)
    rows: list[dict[str, Any]] = []
    for source in real_boxes:
        event = event_lookup[source["event_id"]]
        configuration = M5379.M5378.M5359.event_configuration(event, references)
        zero_coordinate = mp.mpf(event["zero_regulator_absolute_soft_cosine"])
        epsilon_lower = float(source["epsilon_lower"])
        epsilon_upper = float(source["epsilon_upper"])
        epsilon_midpoint = 0.5 * (epsilon_lower + epsilon_upper)
        samples = [
            point_solution(configuration, epsilon, zero_coordinate)
            for epsilon in (epsilon_lower, epsilon_midpoint, epsilon_upper)
        ]
        initial_state_boxes = complex_state_boxes(
            configuration,
            source,
            samples,
            epsilon_upper - epsilon_lower,
        )
        state_boxes, certificate, inflation_steps = construct_certified_state_box(
            configuration,
            (epsilon_lower, epsilon_upper),
            initial_state_boxes,
            samples[1],
        )
        rows.append(
            {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "epsilon_bin_index": source["epsilon_bin_index"],
                "epsilon_real_lower": epsilon_lower,
                "epsilon_real_upper": epsilon_upper,
                "epsilon_imaginary_lower": -EPSILON_IMAGINARY_HALF_WIDTH,
                "epsilon_imaginary_upper": EPSILON_IMAGINARY_HALF_WIDTH,
                "complex_system_dimension": len(state_boxes),
                "state_box_inflation_iterations": inflation_steps,
                "complex_state_boxes": "|".join(
                    complex_interval_text(value) for value in state_boxes
                ),
                "complex_Krawczyk_images": "|".join(
                    complex_interval_text(value)
                    for value in certificate["operator"]
                ),
                "minimum_strict_inclusion_margin": certificate[
                    "minimum_inclusion_margin"
                ],
                "maximum_contraction_bound": certificate[
                    "contraction_bound"
                ],
                "point_jacobian_condition_number": certificate[
                    "point_jacobian_condition_number"
                ],
                "complex_neighborhood_box_passes": certificate["passes"],
                CLAIM_COMPLEX: False,
                **open_claims(),
            }
        )
    required_count = len(EVENT_IDS) * EPSILON_BIN_COUNT
    certified_count = sum(
        parse_bool(row["complex_neighborhood_box_passes"]) for row in rows
    )
    maximum_contraction = max(float(row["maximum_contraction_bound"]) for row in rows)
    minimum_margin = min(float(row["minimum_strict_inclusion_margin"]) for row in rows)
    maximum_inflation_steps = max(
        int(row["state_box_inflation_iterations"]) for row in rows
    )
    validations = [
        validation_row("preflight_passes", preflight_result["all_pass"], preflight_result["checks"]),
        validation_row("all_required_complex_boxes_are_present", len(rows) == required_count, f"rows={len(rows)};required={required_count}"),
        validation_row("every_complex_parametric_Krawczyk_box_passes", certified_count == required_count, f"certified={certified_count};required={required_count}"),
        validation_row("all_complex_contraction_bounds_are_below_one", maximum_contraction < 1, maximum_contraction),
        validation_row("all_complex_images_are_strictly_internal", minimum_margin > 0, minimum_margin),
        validation_row("all_state_boxes_close_within_inflation_budget", maximum_inflation_steps < STATE_BOX_INFLATION_MAXIMUM_STEPS or certified_count == required_count, f"maximum_steps_used={maximum_inflation_steps};budget={STATE_BOX_INFLATION_MAXIMUM_STEPS}"),
        validation_row("amplitude_H3_and_downstream_claims_remain_false", all(value is False for value in open_claims().values()), open_claims()),
        validation_row("formal_workbench_remains_unchanged", M5379.M5378.M5359.M5342.M5283.formal_inventory_digest() == M5379.M5378.M5359.M5342.FORMAL_DIGEST, M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()),
        validation_row("scripts_cache_remains_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in rows:
        row[CLAIM_COMPLEX] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_COMPLEX] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_COMMON_CLOSED_COMPLEX_EVENT_NEIGHBORHOOD_CERTIFIED__ENCLOSE_PARENT_RESIDUE"
            if passed
            else "D4_COMPLEXIFIED_EVENT_NEIGHBORHOOD_BLOCKED"
        ),
        "epsilon_real_minimum": EPSILON_MINIMUM,
        "epsilon_real_maximum": EPSILON_MAXIMUM,
        "epsilon_imaginary_half_width": EPSILON_IMAGINARY_HALF_WIDTH,
        "epsilon_bin_count": EPSILON_BIN_COUNT,
        "event_count": len(EVENT_IDS),
        "required_box_count": required_count,
        "certified_box_count": certified_count,
        "maximum_contraction_bound": maximum_contraction,
        "minimum_inclusion_margin": minimum_margin,
        "maximum_state_box_inflation_iterations": maximum_inflation_steps,
        "claim_boundary": {CLAIM_COMPLEX: passed, **open_claims()},
        "remaining_obstruction": "interval-enclose the parent relative/global roots, collision Jacobian and finite-plus residue on the certified complex event neighborhood, then use Cauchy or direct derivatives to bound H3",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_complexified_event_neighborhood_boxes.csv", rows)
    atomic_csv(output / "D4_complexified_event_neighborhood_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_complexified_event_neighborhood_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result)
    return result


def self_test() -> dict[str, Any]:
    iv.dps = 30
    dimension = 2
    first = MultiDual.variable(complex_point(2), dimension, 0)
    second = MultiDual.variable(complex_point(3), dimension, 1)
    product = first * second
    checks = {
        "product_value_is_six": abs(complex_midpoint(product.value) - 6) <= 1.0e-14,
        "product_derivative_first_is_three": abs(complex_midpoint(product.derivatives[0]) - 3) <= 1.0e-14,
        "product_derivative_second_is_two": abs(complex_midpoint(product.derivatives[1]) - 2) <= 1.0e-14,
        "complex_box_contains_origin": real_lower(complex_box(-1, 1, -2, 2)) <= 0 <= real_upper(complex_box(-1, 1, -2, 2)),
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
