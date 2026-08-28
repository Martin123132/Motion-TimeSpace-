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
OUTPUT = FUNCTIONAL_RG / "5379"
DOCUMENT = POST / "5379-Y5-R2FR-D4-parametric-interval-Newton-event-atlas.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5379_VALIDATION.csv"

SCRIPT_5378 = SCRIPTS / "Y5_R2FR_5378_D4_zero_parent_C_derivative_decomposition.py"
RESULT_5378 = FUNCTIONAL_RG / "5378" / "D4_zero_parent_C_derivative_result.json"
VALIDATION_5378 = FUNCTIONAL_RG / "5378" / "D4_zero_parent_C_derivative_validation.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
TUBES_5377 = FUNCTIONAL_RG / "5377" / "D4_sampled_fixed_event_tubes.csv"

CHECKPOINT = 5379
MARKER = "MTS_5379_D4_PARAMETRIC_INTERVAL_NEWTON_EVENT_ATLAS"
REVISION = "D4-parametric-interval-Newton-event-atlas-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
EPSILON_MINIMUM = 0.0
EPSILON_MAXIMUM = 0.02
EPSILON_BIN_COUNT = 8
MP_DIGITS = 110
INTERVAL_DIGITS = 50

CLAIM_REAL_ATLAS = "valid_for_D4_common_closed_real_interval_event_atlas"
CLAIM_PRIOR_ATLAS = "valid_for_D4_common_closed_interval_event_atlas"
OPEN_CLAIMS = (
    "valid_for_D4_common_closed_complex_event_neighborhood",
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


M5378 = load_module("mts_5378_for_5379", SCRIPT_5378)
mp = M5378.mp


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5378.set_below_normal_priority()


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
            SCRIPT_5378,
            RESULT_5378,
            VALIDATION_5378,
            EVENTS_5358,
            TUBES_5377,
            Path(M5378.M5359.M5358.__file__),
        )
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_REAL_ATLAS: False,
            CLAIM_PRIOR_ATLAS: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    result_5378 = read_json(RESULT_5378)
    events = read_csv(EVENTS_5358)
    tubes = read_csv(TUBES_5377)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in source_paths()),
        "checkpoint_5378_passes": result_5378.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5378)),
        "exactly_eight_ordered_events": [row["event_id"] for row in events]
        == list(EVENT_IDS),
        "exactly_eight_fixed_tubes": sorted(row["event_id"] for row in tubes)
        == sorted(EVENT_IDS),
        "fixed_tubes_are_pairwise_disjoint": all(
            float(left["fixed_tube_upper"]) < float(right["fixed_tube_lower"])
            for left, right in zip(
                sorted(tubes, key=lambda row: float(row["fixed_tube_lower"])),
                sorted(tubes, key=lambda row: float(row["fixed_tube_lower"]))[1:],
            )
        ),
        "formal_workbench_inventory_is_unchanged": M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def interval(lower: Any, upper: Any) -> Any:
    return iv.mpf([str(lower), str(upper)])


def lower(value: Any) -> float:
    return float(value.a)


def upper(value: Any) -> float:
    return float(value.b)


def midpoint(value: Any) -> float:
    return 0.5 * (lower(value) + upper(value))


def width(value: Any) -> float:
    return upper(value) - lower(value)


def sup_abs(value: Any) -> float:
    return max(abs(lower(value)), abs(upper(value)))


def interval_text(value: Any) -> str:
    return f"[{lower(value):.17g},{upper(value):.17g}]"


def complex_interval(real_value: Any, imaginary_value: Any) -> Any:
    return iv.mpc(
        [lower(real_value), upper(real_value)],
        [lower(imaginary_value), upper(imaginary_value)],
    )


def q_interval(epsilon_lower: float, epsilon_upper: float) -> Any:
    def real_part(epsilon: float) -> float:
        return -(80 + epsilon**2) / (64 + epsilon**2)

    def imaginary_part(epsilon: float) -> float:
        return -2 * epsilon / (64 + epsilon**2)

    return iv.mpc(
        [real_part(epsilon_lower), real_part(epsilon_upper)],
        [imaginary_part(epsilon_upper), imaginary_part(epsilon_lower)],
    )


class Dual:
    def __init__(self, value: Any, derivative: Any = 0) -> None:
        self.value = value
        self.derivative = derivative

    @staticmethod
    def coerce(value: Any) -> "Dual":
        return value if isinstance(value, Dual) else Dual(value, 0)

    def __add__(self, other: Any) -> "Dual":
        other = self.coerce(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Dual":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "Dual":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "Dual":
        other = self.coerce(other)
        return Dual(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "Dual":
        other = self.coerce(other)
        return Dual(
            self.value / other.value,
            (
                self.derivative * other.value
                - self.value * other.derivative
            )
            / other.value**2,
        )

    def __rtruediv__(self, other: Any) -> "Dual":
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> "Dual":
        return Dual(
            self.value**exponent,
            exponent * self.value ** (exponent - 1) * self.derivative,
        )


def dual_sqrt(value: Dual) -> Dual:
    root = iv.sqrt(value.value)
    return Dual(root, value.derivative / (2 * root))


def material_polynomial_dual(
    surface_id: str,
    recoil: Dual,
    soft_cosine: Dual,
    decay_cosine: Any,
    q_value: Dual,
) -> Dual:
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


def hard_boundary_dual(
    recoil: Dual, soft_cosine: Dual, decay_cosine: Any
) -> Dual:
    decay = Dual(decay_cosine)
    relative = (
        soft_cosine * decay
        - dual_sqrt(1 - soft_cosine**2)
        * iv.sqrt(1 - decay_cosine**2)
    )
    target = interval(-0.3, -0.3)
    return (
        (soft_cosine - target) * (1 + relative) * recoil**2
        + 2 * (decay - soft_cosine * relative) * recoil
        + (soft_cosine + target) * (relative - 1)
    )


def system_and_jacobian(
    configuration: dict[str, Any], epsilon_bounds: tuple[float, float], box: list[Any]
) -> tuple[list[Any], list[list[Any]]]:
    q_value = q_interval(*epsilon_bounds)
    sign = int(configuration["sign"])
    decay = interval(configuration["decay_cosine"], configuration["decay_cosine"])
    recoil_real = box[0]
    recoil_imaginary = box[1]
    coordinate = box[-1]
    recoil_complex = complex_interval(recoil_real, recoil_imaginary)
    soft_cosine = sign * coordinate
    polynomial = material_polynomial_dual(
        configuration["surface_id"],
        Dual(recoil_complex),
        Dual(soft_cosine),
        decay,
        Dual(q_value),
    ).value
    polynomial_R = material_polynomial_dual(
        configuration["surface_id"],
        Dual(recoil_complex, 1),
        Dual(soft_cosine),
        decay,
        Dual(q_value),
    ).derivative
    polynomial_x = material_polynomial_dual(
        configuration["surface_id"],
        Dual(recoil_complex),
        Dual(soft_cosine, sign),
        decay,
        Dual(q_value),
    ).derivative
    if configuration["event_type"] == "BRANCH_DEATH":
        functions = [
            polynomial.real,
            polynomial.imag,
            recoil_real**2
            - recoil_imaginary**2
            - M5378.M5359.M5358.R_MINIMUM**2,
        ]
        jacobian = [
            [polynomial_R.real, -polynomial_R.imag, polynomial_x.real],
            [polynomial_R.imag, polynomial_R.real, polynomial_x.imag],
            [2 * recoil_real, -2 * recoil_imaginary, interval(0, 0)],
        ]
        return functions, jacobian
    hard_recoil = box[2]
    hard_value = hard_boundary_dual(
        Dual(hard_recoil), Dual(soft_cosine), decay
    ).value
    hard_R = hard_boundary_dual(
        Dual(hard_recoil, 1), Dual(soft_cosine), decay
    ).derivative
    hard_x = hard_boundary_dual(
        Dual(hard_recoil), Dual(soft_cosine, sign), decay
    ).derivative
    functions = [
        polynomial.real,
        polynomial.imag,
        hard_value,
        hard_recoil**2 - recoil_real**2 + recoil_imaginary**2,
    ]
    jacobian = [
        [polynomial_R.real, -polynomial_R.imag, interval(0, 0), polynomial_x.real],
        [polynomial_R.imag, polynomial_R.real, interval(0, 0), polynomial_x.imag],
        [interval(0, 0), interval(0, 0), hard_R, hard_x],
        [-2 * recoil_real, 2 * recoil_imaginary, 2 * hard_recoil, interval(0, 0)],
    ]
    return functions, jacobian


def point_solution(
    configuration: dict[str, Any], epsilon: float, zero_coordinate: Any
) -> list[float]:
    epsilon_mp = mp.mpf(str(epsilon))
    coordinate = M5378.continued_event_coordinate(
        configuration, epsilon_mp, zero_coordinate
    )
    recoil = M5378.material_recoil(configuration, epsilon_mp, coordinate)
    values = [float(mp.re(recoil)), float(mp.im(recoil))]
    if configuration["event_type"] != "BRANCH_DEATH":
        hard_roots = M5378.M5359.M5358.hard_boundary_roots(
            configuration["sign"] * coordinate,
            configuration["decay_cosine"],
        )
        hard_recoil = min(
            hard_roots, key=lambda value: abs(value - configuration["recoil"])
        )
        values.append(float(hard_recoil))
    values.append(float(coordinate))
    return values


def build_box(samples: list[list[float]]) -> list[Any]:
    dimensions = len(samples[0])
    box: list[Any] = []
    for index in range(dimensions):
        values = [sample[index] for sample in samples]
        sample_lower = min(values)
        sample_upper = max(values)
        span = sample_upper - sample_lower
        floor = 1.0e-12
        padding_factor = 3.0 if index == 1 else 35.0
        padding = max(padding_factor * span, floor)
        box.append(interval(sample_lower - padding, sample_upper + padding))
    return box


def point_matrix(
    configuration: dict[str, Any], epsilon: float, center: list[float]
) -> tuple[np.ndarray, np.ndarray]:
    degenerate = [interval(value, value) for value in center]
    functions, jacobian = system_and_jacobian(
        configuration, (epsilon, epsilon), degenerate
    )
    function_values = np.asarray([midpoint(value) for value in functions])
    jacobian_values = np.asarray(
        [[midpoint(value) for value in row] for row in jacobian]
    )
    return function_values, jacobian_values


def krawczyk_certificate(
    configuration: dict[str, Any],
    epsilon_bounds: tuple[float, float],
    box: list[Any],
    center: list[float],
) -> dict[str, Any]:
    epsilon_midpoint = 0.5 * sum(epsilon_bounds)
    _, point_jacobian = point_matrix(
        configuration, epsilon_midpoint, center
    )
    inverse = np.linalg.inv(point_jacobian)
    center_box = [interval(value, value) for value in center]
    functions, _ = system_and_jacobian(
        configuration, epsilon_bounds, center_box
    )
    _, jacobian = system_and_jacobian(configuration, epsilon_bounds, box)
    dimension = len(box)
    operator: list[Any] = []
    matrix_remainder: list[list[Any]] = []
    for row_index in range(dimension):
        correction = interval(0, 0)
        for column_index in range(dimension):
            correction += inverse[row_index, column_index] * functions[column_index]
        remainder_row: list[Any] = []
        remainder_value = interval(0, 0)
        for column_index in range(dimension):
            matrix_value = interval(
                1 if row_index == column_index else 0,
                1 if row_index == column_index else 0,
            )
            for inner_index in range(dimension):
                matrix_value -= (
                    inverse[row_index, inner_index]
                    * jacobian[inner_index][column_index]
                )
            remainder_row.append(matrix_value)
            remainder_value += matrix_value * (
                box[column_index] - center[column_index]
            )
        matrix_remainder.append(remainder_row)
        operator.append(center[row_index] - correction + remainder_value)
    inclusion_margins = [
        min(
            lower(operator[index]) - lower(box[index]),
            upper(box[index]) - upper(operator[index]),
        )
        for index in range(dimension)
    ]
    contraction_bound = max(
        sum(sup_abs(value) for value in row) for row in matrix_remainder
    )
    return {
        "operator": operator,
        "inclusion_margins": inclusion_margins,
        "contraction_bound": contraction_bound,
        "point_jacobian_condition_number": float(np.linalg.cond(point_jacobian)),
        "passes": min(inclusion_margins) > 0 and contraction_bound < 1,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5379 - D4 parametric interval-Newton event atlas",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Certificate",
        "",
        f"The real regulator interval `[{EPSILON_MINIMUM},{EPSILON_MAXIMUM}]` is partitioned into `{EPSILON_BIN_COUNT}` closed bins. For every event and every bin, the real material/event system is enclosed in one box and tested with a parametric Krawczyk operator.",
        "",
        "Branch deaths solve `Re P=0`, `Im P=0`, and `R_r^2-R_i^2=R_min^2`. Support contacts additionally solve the real hard-boundary equation and `R_h^2=R_r^2-R_i^2`. No complex square-root interval branch is assumed.",
        "",
        f"- certified boxes: `{result['certified_box_count']}/{result['required_box_count']}`;",
        f"- largest Krawczyk contraction bound: `{result['maximum_contraction_bound']}`;",
        f"- smallest strict inclusion margin: `{result['minimum_inclusion_margin']}`;",
        f"- largest event-box fraction of its fixed tube: `{result['maximum_coordinate_box_fraction_of_fixed_tube']}`.",
        "",
        "## Scope",
        "",
        "This closes a common closed real-parameter event atlas: each branch exists uniquely, remains in its fixed disjoint tube, and cannot exchange order on the tested interval. It does not yet enclose the parent amplitude on a complex epsilon neighborhood, so the strict endpoint-C theorem, H3, W3, D4 outer limit and broader GR/MTS claims remain open.",
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
    references, _ = M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    tubes = {row["event_id"]: row for row in read_csv(TUBES_5377)}
    rows: list[dict[str, Any]] = []
    bin_width = (EPSILON_MAXIMUM - EPSILON_MINIMUM) / EPSILON_BIN_COUNT
    for event in events:
        configuration = M5378.M5359.event_configuration(event, references)
        zero_coordinate = mp.mpf(event["zero_regulator_absolute_soft_cosine"])
        tube = tubes[configuration["event_id"]]
        for bin_index in range(EPSILON_BIN_COUNT):
            epsilon_lower = EPSILON_MINIMUM + bin_index * bin_width
            epsilon_upper = EPSILON_MINIMUM + (bin_index + 1) * bin_width
            epsilon_midpoint = 0.5 * (epsilon_lower + epsilon_upper)
            samples = [
                point_solution(configuration, epsilon, zero_coordinate)
                for epsilon in (
                    epsilon_lower,
                    epsilon_midpoint,
                    epsilon_upper,
                )
            ]
            box = build_box(samples)
            center = samples[1]
            certificate = krawczyk_certificate(
                configuration,
                (epsilon_lower, epsilon_upper),
                box,
                center,
            )
            coordinate_box = box[-1]
            tube_lower = float(tube["fixed_tube_lower"])
            tube_upper = float(tube["fixed_tube_upper"])
            tube_width = tube_upper - tube_lower
            coordinate_inside_tube = (
                lower(coordinate_box) > tube_lower
                and upper(coordinate_box) < tube_upper
            )
            row_passes = certificate["passes"] and coordinate_inside_tube
            rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "term_id": configuration["term_id"],
                    "primary_surface_id": configuration["surface_id"],
                    "epsilon_bin_index": bin_index,
                    "epsilon_lower": epsilon_lower,
                    "epsilon_upper": epsilon_upper,
                    "system_dimension": len(box),
                    "recoil_real_box": interval_text(box[0]),
                    "recoil_imaginary_box": interval_text(box[1]),
                    "hard_recoil_box": (
                        interval_text(box[2])
                        if configuration["event_type"] != "BRANCH_DEATH"
                        else "NOT_APPLICABLE"
                    ),
                    "event_coordinate_box": interval_text(coordinate_box),
                    "event_coordinate_box_lower": lower(coordinate_box),
                    "event_coordinate_box_upper": upper(coordinate_box),
                    "event_coordinate_box_width": width(coordinate_box),
                    "fixed_tube_lower": tube_lower,
                    "fixed_tube_upper": tube_upper,
                    "coordinate_box_fraction_of_fixed_tube": width(
                        coordinate_box
                    )
                    / tube_width,
                    "coordinate_box_inside_fixed_tube": coordinate_inside_tube,
                    "krawczyk_operator_boxes": "|".join(
                        interval_text(value) for value in certificate["operator"]
                    ),
                    "minimum_strict_inclusion_margin": min(
                        certificate["inclusion_margins"]
                    ),
                    "maximum_contraction_bound": certificate[
                        "contraction_bound"
                    ],
                    "point_jacobian_condition_number": certificate[
                        "point_jacobian_condition_number"
                    ],
                    "parametric_interval_Newton_passes": certificate["passes"],
                    "box_certificate_passes": row_passes,
                    CLAIM_REAL_ATLAS: False,
                    CLAIM_PRIOR_ATLAS: False,
                    **open_claims(),
                }
            )
    certified_count = sum(parse_bool(row["box_certificate_passes"]) for row in rows)
    required_count = len(EVENT_IDS) * EPSILON_BIN_COUNT
    maximum_contraction = max(float(row["maximum_contraction_bound"]) for row in rows)
    minimum_margin = min(float(row["minimum_strict_inclusion_margin"]) for row in rows)
    maximum_tube_fraction = max(
        float(row["coordinate_box_fraction_of_fixed_tube"]) for row in rows
    )
    event_bin_lookup = {
        (row["event_id"], int(row["epsilon_bin_index"])): row for row in rows
    }
    ordering_passes = True
    ordered_tubes = sorted(tubes.values(), key=lambda row: int(row["coordinate_order_index"]))
    for bin_index in range(EPSILON_BIN_COUNT):
        for left_tube, right_tube in zip(ordered_tubes, ordered_tubes[1:]):
            left_row = event_bin_lookup[(left_tube["event_id"], bin_index)]
            right_row = event_bin_lookup[(right_tube["event_id"], bin_index)]
            ordering_passes = ordering_passes and (
                float(left_row["event_coordinate_box_upper"])
                < float(right_row["event_coordinate_box_lower"])
            )
    validations = [
        validation_row("preflight_passes", preflight_result["all_pass"], preflight_result["checks"]),
        validation_row("all_required_parametric_boxes_are_present", len(rows) == required_count, f"rows={len(rows)};required={required_count}"),
        validation_row("every_parametric_Krawczyk_box_passes", certified_count == required_count, f"certified={certified_count};required={required_count}"),
        validation_row("all_contraction_bounds_are_strictly_below_one", maximum_contraction < 1, maximum_contraction),
        validation_row("all_Krawczyk_images_are_strictly_internal", minimum_margin > 0, minimum_margin),
        validation_row("all_event_boxes_remain_inside_fixed_tubes", all(parse_bool(row["coordinate_box_inside_fixed_tube"]) for row in rows), maximum_tube_fraction),
        validation_row("event_order_is_uniform_across_all_bins", ordering_passes, ordering_passes),
        validation_row("complex_neighborhood_and_downstream_claims_remain_false", all(value is False for value in open_claims().values()), open_claims()),
        validation_row("formal_workbench_remains_unchanged", M5378.M5359.M5342.M5283.formal_inventory_digest() == M5378.M5359.M5342.FORMAL_DIGEST, M5378.M5359.M5342.M5283.formal_inventory_digest()),
        validation_row("scripts_cache_remains_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in rows:
        row[CLAIM_REAL_ATLAS] = passed
        row[CLAIM_PRIOR_ATLAS] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_REAL_ATLAS] = passed
        row[CLAIM_PRIOR_ATLAS] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_COMMON_CLOSED_REAL_INTERVAL_EVENT_ATLAS_CERTIFIED__BUILD_COMPLEX_NEIGHBORHOOD"
            if passed
            else "D4_PARAMETRIC_INTERVAL_NEWTON_EVENT_ATLAS_BLOCKED"
        ),
        "epsilon_minimum": EPSILON_MINIMUM,
        "epsilon_maximum": EPSILON_MAXIMUM,
        "epsilon_bin_count": EPSILON_BIN_COUNT,
        "event_count": len(EVENT_IDS),
        "required_box_count": required_count,
        "certified_box_count": certified_count,
        "maximum_contraction_bound": maximum_contraction,
        "minimum_inclusion_margin": minimum_margin,
        "maximum_coordinate_box_fraction_of_fixed_tube": maximum_tube_fraction,
        "uniform_event_ordering_passes": ordering_passes,
        "claim_boundary": {
            CLAIM_REAL_ATLAS: passed,
            CLAIM_PRIOR_ATLAS: passed,
            **open_claims(),
        },
        "remaining_obstruction": "extend the real parametric boxes to a source-controlled complex epsilon neighborhood for the parent residue, then enclose H3 before attacking mapped-away W3",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_parametric_interval_Newton_boxes.csv", rows)
    atomic_csv(output / "D4_parametric_interval_Newton_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_parametric_interval_Newton_result.json", result)
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
    epsilon_q = q_interval(0.0, 0.02)
    value = interval(-0.1, 0.2)
    dual = Dual(value, interval(1, 1))
    square = dual**2
    checks = {
        "q_real_contains_both_endpoints": lower(epsilon_q.real)
        <= -1.25
        <= upper(epsilon_q.real),
        "q_imaginary_contains_zero": lower(epsilon_q.imag)
        <= 0
        <= upper(epsilon_q.imag),
        "dual_square_value_encloses_zero": lower(square.value) <= 0 <= upper(square.value),
        "dual_square_derivative_is_two_x": lower(square.derivative) <= -0.2 + 1.0e-15
        and upper(square.derivative) >= 0.4 - 1.0e-15,
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
