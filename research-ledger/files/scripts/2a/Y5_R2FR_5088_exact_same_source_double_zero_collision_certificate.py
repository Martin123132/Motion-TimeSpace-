from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any, Callable

import numpy as np


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
PILOT_V6 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v6"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5088"
RESULT_JSON = SOURCE / "exact_same_source_double_zero_collision_certificate.json"
GATE_JSON = SOURCE / "E020_A07_primary24_exact_collision_gate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5088_VALIDATION.csv"
)
PREVIOUS_GATE_5087 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5087"
    / "E020_A07_primary24_finer_limit_gate.json"
)
MARKER = "MTS_5088_EXACT_SAME_SOURCE_DOUBLE_ZERO_COLLISION_CERTIFICATE"
REVISION = "local-double-zero-and-zero-owned-residue-extension-v2"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E020_A07"
BASE_ARGUMENT_ID = "A07"
PROFILE = "primary24"
COLLISION_LABELS = ("direct:g2:plus_u", "direct:g2:plus_v")
CAUCHY_RADIUS_FRACTIONS = (0.03, 0.10, 0.25)
CAUCHY_NODES = (48, 96)
RESIDUE_FRACTIONS = (1.0e-3, 5.0e-4, 2.5e-4)
RESIDUE_DIRECTIONS = (
    1.0 + 0.0j,
    0.0 + 1.0j,
    complex(np.exp(0.37j)),
)
RESIDUE_NODES = (96, 192)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def laurent_value(polynomial: dict[int, complex], value: complex) -> complex:
    return complex(
        sum(coefficient * value**exponent for exponent, coefficient in polynomial.items())
    )


def laurent_derivative_value(
    polynomial: dict[int, complex], value: complex
) -> complex:
    return complex(
        sum(
            exponent * coefficient * value ** (exponent - 1)
            for exponent, coefficient in polynomial.items()
        )
    )


def rational_derivative(
    rational: tuple[dict[int, complex], dict[int, complex]], value: complex
) -> complex:
    numerator, denominator = rational
    numerator_value = laurent_value(numerator, value)
    denominator_value = laurent_value(denominator, value)
    return complex(
        (
            laurent_derivative_value(numerator, value) * denominator_value
            - numerator_value * laurent_derivative_value(denominator, value)
        )
        / denominator_value**2
    )


def configured_problem() -> tuple[Any, dict[str, Any], dict[str, Any], dict[str, Any]]:
    module_5077 = load_module("mts_5077_for_5088", SCRIPT_5077)
    config = json.loads((PILOT_V6 / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5036.M5035.M5034.configure(event, target)
    topology = json.loads(
        (
            PILOT_V6
            / "topologies"
            / f"{EVENT_ID}__{ARGUMENT_ID}.json"
        ).read_text(encoding="utf-8")
    )
    return module_5077, config, topology, argument


def collision_geometry(
    numerical_module: Any, relative_circle: complex
) -> dict[str, Any]:
    soft_direction, decay_direction, internal = numerical_module.M5028.event_geometry(
        numerical_module.SOFT_ENERGY,
        complex(numerical_module.SOFT_COSINE, 0.0),
        complex(numerical_module.DECAY_COSINE, 0.0),
        relative_circle,
    )
    directions = numerical_module.M5028.source_directions(
        internal, soft_direction, decay_direction
    )
    roots_by_source = {
        source: numerical_module.M5028.M5024.all_factor_roots(
            direction, numerical_module.TARGET_COSINE
        )
        for source, direction in directions.items()
    }
    plus_u = complex(roots_by_source["direct:g2"]["plus_u"])
    plus_v = complex(roots_by_source["direct:g2"]["plus_v"])
    collision_root = (plus_u + plus_v) / 2.0
    other_rows = [
        (f"{source}:{label}", complex(root))
        for source, roots in roots_by_source.items()
        for label, root in roots.items()
        if f"{source}:{label}" not in COLLISION_LABELS
    ]
    nearest_distance, nearest_label, nearest_root = min(
        (
            (abs(root - collision_root), label, root)
            for label, root in other_rows
        ),
        key=lambda row: row[0],
    )
    return {
        "soft_direction": soft_direction,
        "decay_direction": decay_direction,
        "internal": internal,
        "directions": directions,
        "roots_by_source": roots_by_source,
        "plus_u": plus_u,
        "plus_v": plus_v,
        "collision_root": collision_root,
        "nearest_other_distance": float(nearest_distance),
        "nearest_other_label": nearest_label,
        "nearest_other_root": nearest_root,
    }


def finite_integrand(
    numerical_module: Any, geometry: dict[str, Any]
) -> Callable[[complex], complex]:
    return lambda unit_circle: numerical_module.M5028.M5026.finite_plus_integrand(
        geometry["internal"],
        numerical_module.SOFT_ENERGY,
        geometry["soft_direction"],
        geometry["decay_direction"],
        numerical_module.TARGET_COSINE,
        unit_circle,
    )


def exact_collision_root_and_split(
    numerical_module: Any,
) -> tuple[complex, dict[str, tuple[dict[int, complex], dict[int, complex]]], complex, complex]:
    rationals = numerical_module.M5029.root_rationals(
        numerical_module.SOFT_ENERGY,
        numerical_module.SOFT_COSINE,
        numerical_module.DECAY_COSINE,
        numerical_module.TARGET_COSINE,
    )
    roots = numerical_module.M5029.collision_roots(
        rationals[COLLISION_LABELS[0]], rationals[COLLISION_LABELS[1]]
    )
    relative_root = min(roots, key=abs)
    plus_u_derivative = rational_derivative(
        rationals[COLLISION_LABELS[0]], relative_root
    )
    plus_v_derivative = rational_derivative(
        rationals[COLLISION_LABELS[1]], relative_root
    )
    return relative_root, rationals, plus_u_derivative, plus_v_derivative


def cauchy_double_zero_audit(
    numerical_module: Any, relative_root: complex
) -> dict[str, Any]:
    geometry = collision_geometry(numerical_module, relative_root)
    evaluator = finite_integrand(numerical_module, geometry)
    plus_u = geometry["plus_u"]
    plus_v = geometry["plus_v"]
    collision_root = geometry["collision_root"]
    rows: list[dict[str, Any]] = []
    quadratic_coefficients: list[complex] = []
    center_values: list[complex] = []
    maximum_constant_ratio = 0.0
    maximum_linear_ratio = 0.0
    maximum_residue_ratio = 0.0
    for radius_fraction in CAUCHY_RADIUS_FRACTIONS:
        radius = radius_fraction * geometry["nearest_other_distance"]
        for nodes in CAUCHY_NODES:
            phases = np.exp(
                2.0j
                * np.pi
                * (np.arange(nodes, dtype=float) + 0.193)
                / nodes
            )
            unit_circles = collision_root + radius * phases
            global_values = np.asarray(
                [evaluator(complex(value)) / value for value in unit_circles],
                dtype=np.complex128,
            )
            regularized = np.asarray(
                [
                    (value - plus_u) * (value - plus_v) * global_value
                    for value, global_value in zip(unit_circles, global_values)
                ],
                dtype=np.complex128,
            )
            coefficients = [
                complex(np.mean(regularized / phases**order) / radius**order)
                for order in (0, 1, 2)
            ]
            center = complex(np.mean(global_values))
            local_residue = complex(np.mean(global_values * radius * phases))
            quadratic_scale = max(abs(coefficients[2]) * radius**2, 1.0e-30)
            constant_ratio = abs(coefficients[0]) / quadratic_scale
            linear_ratio = abs(coefficients[1]) * radius / quadratic_scale
            residue_ratio = abs(local_residue) / max(abs(center) * radius, 1.0e-30)
            maximum_constant_ratio = max(maximum_constant_ratio, constant_ratio)
            maximum_linear_ratio = max(maximum_linear_ratio, linear_ratio)
            maximum_residue_ratio = max(maximum_residue_ratio, residue_ratio)
            quadratic_coefficients.append(coefficients[2])
            center_values.append(center)
            rows.append(
                {
                    "radius_fraction_of_nearest_other_root": radius_fraction,
                    "radius": float(radius),
                    "nodes": int(nodes),
                    "regularized_taylor_coefficients": {
                        "order_0": serialized(coefficients[0]),
                        "order_1": serialized(coefficients[1]),
                        "order_2": serialized(coefficients[2]),
                    },
                    "constant_to_quadratic_circle_ratio": float(constant_ratio),
                    "linear_to_quadratic_circle_ratio": float(linear_ratio),
                    "global_form_cauchy_center": serialized(center),
                    "local_global_form_residue": serialized(local_residue),
                    "local_residue_relative_ratio": float(residue_ratio),
                }
            )
    quadratic_mean = sum(quadratic_coefficients) / len(quadratic_coefficients)
    center_mean = sum(center_values) / len(center_values)
    quadratic_spread = max(
        abs(value - quadratic_mean) for value in quadratic_coefficients
    ) / max(abs(quadratic_mean), 1.0e-30)
    center_spread = max(abs(value - center_mean) for value in center_values) / max(
        abs(center_mean), 1.0e-30
    )
    coefficient_center_match = abs(quadratic_mean - center_mean) / max(
        abs(quadratic_mean), abs(center_mean), 1.0e-30
    )
    passed = bool(
        maximum_constant_ratio < 1.0e-6
        and maximum_linear_ratio < 1.0e-5
        and maximum_residue_ratio < 1.0e-5
        and quadratic_spread < 1.0e-5
        and center_spread < 1.0e-5
        and coefficient_center_match < 1.0e-5
    )
    return {
        "collision_global_root": serialized(collision_root),
        "plus_u": serialized(plus_u),
        "plus_v": serialized(plus_v),
        "pair_separation": float(abs(plus_u - plus_v)),
        "nearest_other_root_distance": geometry["nearest_other_distance"],
        "nearest_other_root_label": geometry["nearest_other_label"],
        "rows": rows,
        "maximum_constant_to_quadratic_circle_ratio": float(
            maximum_constant_ratio
        ),
        "maximum_linear_to_quadratic_circle_ratio": float(maximum_linear_ratio),
        "maximum_local_residue_relative_ratio": float(maximum_residue_ratio),
        "quadratic_coefficient_mean": serialized(quadratic_mean),
        "quadratic_coefficient_relative_spread": float(quadratic_spread),
        "global_form_cauchy_center_mean": serialized(center_mean),
        "global_form_cauchy_center_relative_spread": float(center_spread),
        "quadratic_coefficient_to_center_relative_residual": float(
            coefficient_center_match
        ),
        "interpretation": (
            "H=(w-u)(w-v) I/w has vanishing constant and linear local "
            "coefficients, a stable quadratic coefficient, and zero local "
            "Cauchy residue; the apparent double pole is cancelled at q0"
        ),
        "passed": passed,
    }


def selected_residue_linear_audit(
    numerical_module: Any,
    relative_root: complex,
    ownership: dict[str, bool],
    exact_split_derivative: complex,
) -> dict[str, Any]:
    selected_label = next(
        label for label in COLLISION_LABELS if bool(ownership[label])
    )
    selected_suffix = selected_label.rsplit(":", 1)[1]
    scale = max(abs(relative_root), 1.0e-6)
    rows: list[dict[str, Any]] = []
    coefficients: list[complex] = []
    split_estimates: dict[tuple[int, float], list[complex]] = {}
    maximum_node_residual = 0.0
    maximum_one_sided_split_derivative_residual = 0.0
    contraction_residuals: list[float] = []
    for direction_index, direction in enumerate(RESIDUE_DIRECTIONS):
        for sign in (-1.0, 1.0):
            ray_rows: list[dict[str, Any]] = []
            previous_residue: complex | None = None
            for fraction in RESIDUE_FRACTIONS:
                displacement = sign * fraction * scale * direction
                geometry = collision_geometry(
                    numerical_module, relative_root + displacement
                )
                plus_u = geometry["plus_u"]
                plus_v = geometry["plus_v"]
                pair_separation = abs(plus_u - plus_v)
                selected_root = complex(
                    geometry["roots_by_source"]["direct:g2"][selected_suffix]
                )
                evaluator = finite_integrand(numerical_module, geometry)
                residue_values = [
                    numerical_module.M5028.M5024.local_residue(
                        evaluator,
                        selected_root,
                        0.20 * pair_separation,
                        nodes,
                    )
                    for nodes in RESIDUE_NODES
                ]
                selected_residue = residue_values[-1]
                node_residual = abs(residue_values[-1] - residue_values[-2]) / max(
                    abs(selected_residue), 1.0e-30
                )
                split_derivative = (plus_u - plus_v) / displacement
                split_derivative_residual = abs(
                    split_derivative - exact_split_derivative
                ) / max(abs(exact_split_derivative), 1.0e-30)
                split_estimates.setdefault((direction_index, fraction), []).append(
                    split_derivative
                )
                coefficient = selected_residue / displacement
                coefficients.append(coefficient)
                maximum_node_residual = max(maximum_node_residual, node_residual)
                maximum_one_sided_split_derivative_residual = max(
                    maximum_one_sided_split_derivative_residual,
                    split_derivative_residual,
                )
                contraction_residual = None
                if previous_residue is not None:
                    contraction_residual = abs(
                        abs(selected_residue) / abs(previous_residue) - 0.5
                    )
                    contraction_residuals.append(contraction_residual)
                previous_residue = selected_residue
                row = {
                    "fraction": fraction,
                    "displacement": serialized(displacement),
                    "pair_separation": float(pair_separation),
                    "split_derivative": serialized(split_derivative),
                    "split_derivative_relative_residual": float(
                        split_derivative_residual
                    ),
                    "selected_root": serialized(selected_root),
                    "residue_nodes": list(RESIDUE_NODES),
                    "residue_values": [serialized(value) for value in residue_values],
                    "selected_residue": serialized(selected_residue),
                    "node_relative_residual": float(node_residual),
                    "residue_over_q_displacement": serialized(coefficient),
                    "half_step_contraction_residual": (
                        float(contraction_residual)
                        if contraction_residual is not None
                        else None
                    ),
                }
                ray_rows.append(row)
                rows.append(
                    {
                        "direction": serialized(direction),
                        "sign": int(sign),
                        **row,
                    }
                )
    symmetric_split_rows = []
    for (direction_index, fraction), estimates in sorted(split_estimates.items()):
        if len(estimates) != 2:
            raise RuntimeError("5088 central split derivative lacks both signs")
        central_estimate = sum(estimates) / 2.0
        central_residual = abs(
            central_estimate - exact_split_derivative
        ) / max(abs(exact_split_derivative), 1.0e-30)
        symmetric_split_rows.append(
            {
                "direction": serialized(RESIDUE_DIRECTIONS[direction_index]),
                "fraction": fraction,
                "central_split_derivative": serialized(central_estimate),
                "central_split_derivative_relative_residual": float(
                    central_residual
                ),
            }
        )
    maximum_central_split_derivative_residual = max(
        row["central_split_derivative_relative_residual"]
        for row in symmetric_split_rows
    )
    coefficient_mean = sum(coefficients) / len(coefficients)
    coefficient_spread = max(
        abs(value - coefficient_mean) for value in coefficients
    ) / max(abs(coefficient_mean), 1.0e-30)
    maximum_contraction_residual = max(contraction_residuals)
    passed = bool(
        abs(exact_split_derivative) > 1.0e-6
        and maximum_central_split_derivative_residual < 1.0e-6
        and maximum_node_residual < 1.0e-2
        and coefficient_spread < 1.0e-2
        and maximum_contraction_residual < 2.0e-2
    )
    return {
        "selected_owned_label": selected_label,
        "unowned_label": next(
            label for label in COLLISION_LABELS if label != selected_label
        ),
        "rows": rows,
        "exact_root_split_derivative": serialized(exact_split_derivative),
        "exact_root_split_derivative_magnitude": float(abs(exact_split_derivative)),
        "symmetric_split_derivative_rows": symmetric_split_rows,
        "maximum_one_sided_split_derivative_relative_residual": float(
            maximum_one_sided_split_derivative_residual
        ),
        "maximum_central_split_derivative_relative_residual": float(
            maximum_central_split_derivative_residual
        ),
        "maximum_residue_node_relative_residual": float(maximum_node_residual),
        "linear_residue_coefficient_mean": serialized(coefficient_mean),
        "linear_residue_coefficient_relative_spread": float(coefficient_spread),
        "maximum_half_step_contraction_residual": float(
            maximum_contraction_residual
        ),
        "derived_limit": serialized(0.0j),
        "interpretation": (
            "Res_owned(q)=C(q-q0)+O((q-q0)^2), so the uniquely owned "
            "local contour contribution has the exact collision limit zero"
        ),
        "passed": passed,
    }


def groups_without_silent_pair(
    numerical_module: Any,
    geometry: dict[str, Any],
    ownership: dict[str, bool],
    labels: tuple[str, ...],
) -> list[dict[str, Any]]:
    excluded = set(labels)
    rows: list[dict[str, Any]] = []
    for source, roots in geometry["roots_by_source"].items():
        for suffix in numerical_module.M5028.ROOT_LABELS:
            key = f"{source}:{suffix}"
            if key in excluded:
                continue
            rows.append(
                {
                    "root": complex(roots[suffix]),
                    "labels": [key],
                    "desired_values": [bool(ownership[key])],
                }
            )
    groups: list[dict[str, Any]] = []
    tolerance = numerical_module.M5028.ROOT_COINCIDENCE_RELATIVE_TOLERANCE
    for row in rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"])
                < tolerance
                * max(1.0, abs(row["root"]), abs(candidate["root"]))
            ),
            None,
        )
        if group is None:
            groups.append(row)
        else:
            group["labels"].extend(row["labels"])
            group["desired_values"].extend(row["desired_values"])
    for group in groups:
        if len(set(group["desired_values"])) != 1:
            raise RuntimeError(
                "non-silent mixed ownership remains after 5088 pair removal: "
                + ", ".join(group["labels"])
            )
        group["desired_inside"] = group["desired_values"][0]
    return groups


def silent_pair_global_cycle(
    numerical_module: Any,
    relative_circle: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    residue_nodes: int,
    labels: tuple[str, ...],
) -> tuple[complex, dict[str, Any]]:
    geometry = collision_geometry(numerical_module, relative_circle)
    pair_residual = abs(geometry["plus_u"] - geometry["plus_v"]) / max(
        1.0, abs(geometry["collision_root"])
    )
    if pair_residual >= 2.0e-10:
        raise RuntimeError(
            f"5088 silent-pair root residual exceeds scope: {pair_residual}"
        )
    groups = groups_without_silent_pair(
        numerical_module, geometry, ownership, labels
    )
    evaluator = finite_integrand(numerical_module, geometry)
    base_radius = numerical_module.M5028.M5026.conditioned_global_base_radius(
        groups
    )
    result = numerical_module.M5028.M5026.circle_average(
        evaluator, global_nodes, base_radius
    )
    corrections: list[dict[str, Any]] = []
    for group in groups:
        root = complex(group["root"])
        currently_inside = abs(root) < base_radius
        if bool(group["desired_inside"]) == currently_inside:
            continue
        separations = [
            abs(root - complex(other["root"]))
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        residue = numerical_module.M5028.M5024.local_residue(
            evaluator,
            root,
            max(1.0e-7, 0.07 * safe_scale),
            residue_nodes,
        )
        if bool(group["desired_inside"]):
            result += residue
            orientation = "add_outside_to_inside"
        else:
            result -= residue
            orientation = "subtract_inside_to_outside"
        corrections.append(
            {
                "labels": list(group["labels"]),
                "root": serialized(root),
                "residue": serialized(residue),
                "orientation": orientation,
            }
        )
    return result, {
        "relative_circle": serialized(relative_circle),
        "labels_removed_only_after_double_zero_certificate": list(labels),
        "pair_collision_relative_residual": float(pair_residual),
        "pair_owned_residue_limit": serialized(0.0j),
        "nearest_other_root_distance": geometry["nearest_other_distance"],
        "base_radius": float(base_radius),
        "remaining_group_count": len(groups),
        "correction_count": len(corrections),
        "corrections": corrections,
        "returned_value": serialized(result),
    }


class CertifiedDoubleZeroGlobalExtension:
    def __init__(
        self,
        numerical_module: Any,
        original: Callable[[complex, dict[str, bool], int, int], complex],
        module_5085: Any,
        relative_root: complex,
        certified_ownership_digests: set[str],
        certificate_passed: bool,
    ) -> None:
        self.numerical_module = numerical_module
        self.original = original
        self.module_5085 = module_5085
        self.relative_root = relative_root
        self.certified_ownership_digests = certified_ownership_digests
        self.certificate_passed = certificate_passed
        self.calls: list[dict[str, Any]] = []
        self.cache: dict[tuple[Any, ...], complex] = {}

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        try:
            return self.original(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
        except RuntimeError as error:
            labels = self.module_5085.labels_from_error(error)
            if set(labels) != set(COLLISION_LABELS):
                raise
            if not self.certificate_passed:
                raise
            relative_distance = abs(relative_circle - self.relative_root) / max(
                1.0, abs(self.relative_root)
            )
            if relative_distance >= 5.0e-9:
                raise
            current_ownership_digest = ownership_digest(ownership)
            if current_ownership_digest not in self.certified_ownership_digests:
                raise
            key = (
                round(relative_circle.real, 11),
                round(relative_circle.imag, 11),
                int(global_nodes),
                int(global_residue_nodes),
                current_ownership_digest,
            )
            if key in self.cache:
                return self.cache[key]
            value, audit = silent_pair_global_cycle(
                self.numerical_module,
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
                labels,
            )
            audit.update(
                {
                    "checkpoint_marker": MARKER,
                    "revision": REVISION,
                    "original_error": str(error),
                    "distance_from_certified_relative_root": float(relative_distance),
                    "ownership_digest": current_ownership_digest,
                    "valid_for_full_MTS_claim": False,
                }
            )
            self.calls.append(audit)
            self.cache[key] = value
            return value


def main() -> None:
    topology_path = PILOT_V6 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    failed_job_path = (
        PILOT_V6
        / "jobs"
        / f"E020__{EVENT_ID}__{BASE_ARGUMENT_ID}__{PROFILE}.json"
    )
    required = [
        SCRIPT_5077,
        PILOT_V6 / "config.json",
        topology_path,
        failed_job_path,
        PREVIOUS_GATE_5087,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5088 inputs: {missing}")
    module_5077, config, topology, argument = configured_problem()
    numerical_module = module_5077.M5036.N5030
    boundaries, ownerships = numerical_module.physical_chambers()
    previous_gate_5087 = json.loads(
        PREVIOUS_GATE_5087.read_text(encoding="utf-8")
    )
    target_ownership_digest = previous_gate_5087["extension_calls"][0][
        "selected_audit"
    ]["ownership_digest"]
    matching_chamber_indexes = [
        index
        for index, candidate in enumerate(ownerships)
        if ownership_digest(candidate) == target_ownership_digest
    ]
    if not matching_chamber_indexes:
        raise RuntimeError("5088 cannot match the failed 5087 ownership digest")
    ownership = ownerships[matching_chamber_indexes[0]]
    opposite_ownerships = [
        candidate
        for candidate in ownerships
        if bool(candidate[COLLISION_LABELS[0]])
        != bool(candidate[COLLISION_LABELS[1]])
    ]
    certified_ownership_digests = {
        ownership_digest(candidate) for candidate in opposite_ownerships
    }
    relative_root, _, plus_u_derivative, plus_v_derivative = (
        exact_collision_root_and_split(numerical_module)
    )
    geometry = collision_geometry(numerical_module, relative_root)
    collision_relative_residual = abs(
        geometry["plus_u"] - geometry["plus_v"]
    ) / max(1.0, abs(geometry["collision_root"]))
    direction_cosine_residual = abs(
        complex(geometry["directions"]["direct:g2"][2])
        - numerical_module.TARGET_COSINE
    )
    split_derivative = plus_u_derivative - plus_v_derivative
    cauchy_audit = cauchy_double_zero_audit(numerical_module, relative_root)
    residue_audits: dict[str, dict[str, Any]] = {}
    for selected_label in COLLISION_LABELS:
        representative = next(
            candidate
            for candidate in opposite_ownerships
            if bool(candidate[selected_label])
        )
        residue_audits[selected_label] = selected_residue_linear_audit(
            numerical_module,
            relative_root,
            representative,
            split_derivative,
        )
    double_zero_certificate_passed = bool(
        collision_relative_residual < 2.0e-10
        and direction_cosine_residual < 2.0e-8
        and abs(split_derivative) > 1.0e-6
        and bool(ownership[COLLISION_LABELS[0]])
        != bool(ownership[COLLISION_LABELS[1]])
        and cauchy_audit["passed"]
        and all(audit["passed"] for audit in residue_audits.values())
    )
    previous_catalog = numerical_module.chamber_residue_catalog
    previous_global = numerical_module.global_chamber_value
    extension = CertifiedDoubleZeroGlobalExtension(
        numerical_module,
        previous_global,
        module_5077.M5085,
        relative_root,
        certified_ownership_digests,
        double_zero_certificate_passed,
    )
    numerical_module.chamber_residue_catalog = module_5077.certified_primary_catalog
    numerical_module.global_chamber_value = extension
    module_5077.M5036.MREPAIR.CURRENT_JOB = "5088::E020_A07_primary24"
    module_5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    profile = config["tiers"][PROFILE]
    gate = None
    gate_error = None
    try:
        gate = numerical_module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            int(profile["relative_adaptive_maximum_intervals"]),
        )
    except Exception as error:
        gate_error = f"{type(error).__name__}: {error}"
    finally:
        numerical_module.chamber_residue_catalog = previous_catalog
        numerical_module.global_chamber_value = previous_global
    gate_converged = bool(
        gate is not None and gate["fixed_event_crossed_integral_converged"]
    )
    gate_residues_stable = bool(gate is not None and gate["all_residues_stable"])
    gate_result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "profile": PROFILE,
        "converged": gate_converged,
        "all_residues_stable": gate_residues_stable,
        "highest_two_order_relative_residual": (
            float(gate["highest_two_order_relative_residual"])
            if gate is not None
            else None
        ),
        "highest_value": (
            module_5077.M5036.complex_row(
                module_5077.M5036.M5035.M5034.highest_value(gate)
            )
            if gate is not None
            else None
        ),
        "gate_error": gate_error,
        "double_zero_extension_call_count": len(extension.calls),
        "double_zero_extension_calls": extension.calls,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE_JSON, gate_result)
    failed_job = json.loads(failed_job_path.read_text(encoding="utf-8"))
    formal_digest = tree_digest(FORMAL)
    gate_accepted = bool(
        double_zero_certificate_passed
        and gate_converged
        and gate_residues_stable
        and gate_error is None
        and len(extension.calls) > 0
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "profile": PROFILE,
        "target_cosine": argument["target_cosine"],
        "chamber_indexes_with_failed_ownership": matching_chamber_indexes,
        "failed_5087_ownership_digest": target_ownership_digest,
        "certified_physical_ownership_digests": sorted(
            certified_ownership_digests
        ),
        "physical_boundary_count": len(boundaries),
        "collision_labels": list(COLLISION_LABELS),
        "relative_collision_root": serialized(relative_root),
        "global_collision_root": serialized(geometry["collision_root"]),
        "global_collision_relative_residual": float(collision_relative_residual),
        "direction_cosine_collision_residual": float(direction_cosine_residual),
        "opposite_ownership": bool(ownership[COLLISION_LABELS[0]])
        != bool(ownership[COLLISION_LABELS[1]]),
        "ownership": {
            label: bool(ownership[label]) for label in COLLISION_LABELS
        },
        "ownership_digest": ownership_digest(ownership),
        "plus_u_derivative": serialized(plus_u_derivative),
        "plus_v_derivative": serialized(plus_v_derivative),
        "root_split_derivative": serialized(split_derivative),
        "root_split_derivative_magnitude": float(abs(split_derivative)),
        "cauchy_double_zero_audit": cauchy_audit,
        "owned_residue_linear_audits": residue_audits,
        "derived_local_lemma": {
            "definition": "G(q,w)=I(q,w)/w and H(q,w)=(w-u(q))(w-v(q))G(q,w)",
            "certified_hypotheses": [
                "u(q0)=v(q0)=w0",
                "u'(q0)-v'(q0) is nonzero",
                "H(q0,w0)=partial_w H(q0,w0)=0",
                "the owned pole residue is linear in q-q0 with one complex coefficient",
            ],
            "conclusion": (
                "Res_owned G=C(q-q0)+O((q-q0)^2), hence its collision "
                "limit is zero and the remaining global cycle is evaluated "
                "with only this certified silent pair removed"
            ),
            "principal_value_or_half_residue_inserted": False,
        },
        "double_zero_certificate_passed": double_zero_certificate_passed,
        "gate_path": str(GATE_JSON),
        "gate_sha256": digest(GATE_JSON),
        "failed_job_before_repair": failed_job,
        "exact_collision_gate_accepted": gate_accepted,
        "runner_integration_authorized": gate_accepted,
        "pilot_resume_authorized_under_exact_guard": gate_accepted,
        "decision": (
            "ACCEPT_CERTIFIED_ZERO_OWNED_RESIDUE_EXTENSION"
            if gate_accepted
            else "CERTIFICATE_PASSED_BUT_EVENT_GATE_FAILED"
            if double_zero_certificate_passed
            else "REJECT_DOUBLE_ZERO_CLASSIFICATION"
        ),
        "next_route": (
            "integrate the exact guard and resume only the blocked pilot row"
            if gate_accepted
            else "inspect the recorded event-gate failure without changing tolerances"
            if double_zero_certificate_passed
            else "reject this contour topology for the row"
        ),
        "numerical_limit_ladder_revived": False,
        "tolerance_relaxed": False,
        "pilot_result_claimed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all exact-row inputs exist"),
        (
            "old_failure_is_targeted",
            failed_job["status"] == "FAILED"
            and "5085 removable extension did not converge" in failed_job["error"],
            failed_job.get("error", ""),
        ),
        (
            "collision_identity",
            collision_relative_residual < 2.0e-10
            and direction_cosine_residual < 2.0e-8,
            f"root={collision_relative_residual}; direction={direction_cosine_residual}",
        ),
        (
            "simple_root_split",
            abs(split_derivative) > 1.0e-6,
            f"magnitude={abs(split_derivative)}",
        ),
        (
            "cauchy_double_zero",
            cauchy_audit["passed"],
            (
                f"constant={cauchy_audit['maximum_constant_to_quadratic_circle_ratio']}; "
                f"linear={cauchy_audit['maximum_linear_to_quadratic_circle_ratio']}; "
                f"residue={cauchy_audit['maximum_local_residue_relative_ratio']}"
            ),
        ),
        (
            "owned_residue_linear_zero",
            all(audit["passed"] for audit in residue_audits.values()),
            "; ".join(
                f"{label}:spread={audit['linear_residue_coefficient_relative_spread']},"
                f"contraction={audit['maximum_half_step_contraction_residual']}"
                for label, audit in residue_audits.items()
            ),
        ),
        (
            "classification_accepted",
            double_zero_certificate_passed,
            "local lemma hypotheses all pass",
        ),
        (
            "event_gate_outcome_recorded",
            gate_accepted or gate_error is not None or gate is not None,
            gate_error
            or f"converged={gate_converged}; stable={gate_residues_stable}",
        ),
        (
            "integration_authorization_consistent",
            result["runner_integration_authorized"] == gate_accepted,
            result["decision"],
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["pilot_result_claimed"]
            and not result["valid_for_full_MTS_claim"]
            and not result["tolerance_relaxed"]
            and not result["numerical_limit_ladder_revived"],
            "row-level contour certificate is not physical evidence",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5088_{index:02d}_{name}",
                    "passed": bool(passed),
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5088 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
