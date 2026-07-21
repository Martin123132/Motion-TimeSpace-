from __future__ import annotations

import argparse
import cmath
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np


POST = Path(__file__).resolve().parents[1]
RUNNER = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5040"
RUN = SOURCE / "runs" / "nested_sobol_power1_s4_v1"
OUTPUT_DIRECTORY = SOURCE / "arbitrary_precision_residues"
MARKER = "MTS_5040_ARBITRARY_PRECISION_CROSS_SOURCE_RESIDUE"
S_VALUE = mp.mpf(4)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_mp_residue", RUNNER)
M5036 = M5040.M5036
M5034 = M5036.M5035.M5034
N5030 = M5036.N5030


def mpc(value: complex | float | int | mp.mpf | mp.mpc) -> mp.mpc:
    if isinstance(value, (mp.mpf, mp.mpc)):
        return mp.mpc(value)
    converted = complex(value)
    return mp.mpc(converted.real, converted.imag)


def mp_vector(values: Any) -> list[mp.mpc]:
    return [mpc(value) for value in values]


def mp_matrix(values: Any) -> list[list[mp.mpc]]:
    return [mp_vector(row) for row in values]


def serialized(value: mp.mpc | complex) -> dict[str, str]:
    return {"real": mp.nstr(mp.re(value), 40), "imaginary": mp.nstr(mp.im(value), 40)}


def minkowski(left: list[mp.mpc], right: list[mp.mpc]) -> mp.mpc:
    return left[0] * right[0] - sum(left[index] * right[index] for index in range(1, 4))


def rotate_vector(vector: list[mp.mpc], unit_circle: mp.mpc) -> list[mp.mpc]:
    inverse = 1 / unit_circle
    cosine = (unit_circle + inverse) / 2
    sine = (unit_circle - inverse) / (2j)
    return [
        cosine * vector[0] - sine * vector[1],
        sine * vector[0] + cosine * vector[1],
        vector[2],
    ]


def rotate_internal(
    internal: list[list[mp.mpc]], unit_circle: mp.mpc
) -> list[list[mp.mpc]]:
    result = []
    for momentum in internal:
        spatial = rotate_vector(momentum[1:], unit_circle)
        result.append([momentum[0], *spatial])
    return result


def external(scattering_cosine: mp.mpc) -> list[list[mp.mpc]]:
    transverse = mp.sqrt(1 - scattering_cosine * scattering_cosine)
    return [
        [mp.mpc(1), mp.mpc(0), mp.mpc(0), mp.mpc(1)],
        [mp.mpc(1), mp.mpc(0), mp.mpc(0), mp.mpc(-1)],
        [mp.mpc(1), transverse, mp.mpc(0), scattering_cosine],
        [mp.mpc(1), -transverse, mp.mpc(0), -scattering_cosine],
    ]


def negate(vector: list[mp.mpc]) -> list[mp.mpc]:
    return [-value for value in vector]


def cut_momenta(
    internal: list[list[mp.mpc]], scattering_cosine: mp.mpc
) -> tuple[list[list[mp.mpc]], list[list[mp.mpc]]]:
    ext = external(scattering_cosine)
    zero = [mp.mpc(0) for _ in range(4)]
    left = [zero.copy() for _ in range(5)]
    right = [zero.copy() for _ in range(5)]
    left[0] = negate(ext[0])
    left[4] = negate(ext[1])
    right[0] = ext[2]
    right[4] = ext[3]
    for index in range(3):
        left[index + 1] = internal[index].copy()
        right[index + 1] = negate(internal[index])
    return left, right


def event_geometry(
    soft_energy_value: float,
    soft_cosine_value: complex,
    decay_cosine_value: complex,
    relative_circle: mp.mpc,
) -> tuple[list[mp.mpc], list[mp.mpc], list[list[mp.mpc]]]:
    soft_energy = mp.mpf(str(soft_energy_value))
    soft_cosine = mpc(soft_cosine_value)
    decay_cosine = mpc(decay_cosine_value)
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
    recoil_root = mp.sqrt(1 - soft_energy)
    beta = soft_energy / (2 - soft_energy)
    gamma = (2 - soft_energy) / (2 * recoil_root)
    gamma_beta = soft_energy / (2 * recoil_root)
    internal: list[list[mp.mpc]] = []
    for sign in (1, -1):
        energy = gamma * recoil_root * (1 - sign * beta * relative_cosine)
        spatial = [
            recoil_root
            * (
                sign * decay_direction[index]
                + (
                    sign * (gamma - 1) * relative_cosine - gamma_beta
                )
                * soft_direction[index]
            )
            for index in range(3)
        ]
        internal.append([energy, *spatial])
    internal.append([soft_energy, *[soft_energy * value for value in soft_direction]])
    return soft_direction, decay_direction, internal


def massless_spinors(
    momentum: list[mp.mpc],
) -> tuple[list[mp.mpc], list[mp.mpc]]:
    energy, px, py, pz = momentum
    if abs(energy + pz) > mp.mpf("1e-13"):
        root = mp.sqrt(energy + pz)
        return [root, (px + 1j * py) / root], [root, (px - 1j * py) / root]
    root = mp.sqrt(energy - pz)
    return [(px - 1j * py) / root, root], [(px + 1j * py) / root, root]


def spinor_table(
    momenta: list[list[mp.mpc]], indices: tuple[int, ...] = (0, 1, 2, 3, 4)
) -> dict[int, tuple[list[mp.mpc], list[mp.mpc]]]:
    return {index: massless_spinors(momenta[index]) for index in indices}


def bracket(
    spinors: dict[int, tuple[list[mp.mpc], list[mp.mpc]]],
    left: int,
    right: int,
    chirality: int,
) -> mp.mpc:
    first = spinors[left][chirality]
    second = spinors[right][chirality]
    return first[0] * second[1] - first[1] * second[0]


def scalar_mhv(
    order: tuple[int, ...],
    special: int,
    spinors: dict[int, tuple[list[mp.mpc], list[mp.mpc]]],
    chirality: int,
) -> mp.mpc:
    numerator = bracket(spinors, special, 0, chirality) ** 2
    numerator *= bracket(spinors, special, 4, chirality) ** 2
    denominator = mp.mpc(1)
    for index, left in enumerate(order):
        denominator *= bracket(
            spinors, left, order[(index + 1) % len(order)], chirality
        )
    return numerator / denominator


def invariant(momenta: list[list[mp.mpc]], left: int, right: int) -> mp.mpc:
    return 2 * minkowski(momenta[left], momenta[right])


def momentum_kernel(
    alpha_reversed: int,
    beta_reversed: int,
    momenta: list[list[mp.mpc]],
) -> mp.mpc:
    s21 = invariant(momenta, 1, 0)
    s31 = invariant(momenta, 2, 0)
    s23 = invariant(momenta, 1, 2)
    if alpha_reversed == 0 and beta_reversed == 0:
        return s21 * s31
    if alpha_reversed == 0 and beta_reversed == 1:
        return (s21 + s23) * s31
    if alpha_reversed == 1 and beta_reversed == 0:
        return (s31 + s23) * s21
    return s31 * s21


def scalar_klt_five(
    momenta: list[list[mp.mpc]],
    spinors: dict[int, tuple[list[mp.mpc], list[mp.mpc]]],
    special: int,
    chirality: int,
) -> mp.mpc:
    result = mp.mpc(0)
    for sigma_reversed in range(2):
        sigma_first, sigma_second = ((1, 2) if sigma_reversed == 0 else (2, 1))
        left_order = (0, sigma_first, sigma_second, 3, 4)
        left = scalar_mhv(left_order, special, spinors, chirality)
        for gamma_reversed in range(2):
            gamma_first, gamma_second = (
                (1, 2) if gamma_reversed == 0 else (2, 1)
            )
            right_order = (3, 4, gamma_first, gamma_second, 0)
            result += (
                left
                * momentum_kernel(gamma_reversed, sigma_reversed, momenta)
                * scalar_mhv(right_order, special, spinors, chirality)
            )
    return result


def hhh_reduced_product(
    internal: list[list[mp.mpc]], scattering_cosine: mp.mpc
) -> mp.mpc:
    left, right = cut_momenta(internal, scattering_cosine)
    left_spinors = spinor_table(left)
    right_spinors = spinor_table(right)
    result = mp.mpc(0)
    for special in (1, 2, 3):
        result += scalar_klt_five(left, left_spinors, special, 0) * scalar_klt_five(
            right, right_spinors, special, 1
        )
        result += scalar_klt_five(left, left_spinors, special, 1) * scalar_klt_five(
            right, right_spinors, special, 0
        )
    return result / 6


def scalar_klt_four(
    momenta: list[list[mp.mpc]],
    spinors: dict[int, tuple[list[mp.mpc], list[mp.mpc]]],
    special: int,
    chirality: int,
) -> mp.mpc:
    return -scalar_mhv((0, 1, 2, 4), special, spinors, chirality) * invariant(
        momenta, 0, 1
    ) * scalar_mhv((2, 4, 1, 0), special, spinors, chirality)


def spinor_soft_factor(
    spinors: dict[int, tuple[list[mp.mpc], list[mp.mpc]]], chirality: int
) -> mp.mpc:
    opposite = 1 - chirality
    result = mp.mpc(0)
    for leg in (0, 1, 2, 4):
        result += (
            bracket(spinors, 3, leg, opposite)
            / bracket(spinors, 3, leg, chirality)
            * (bracket(spinors, 0, leg, chirality) / bracket(spinors, 0, 3, chirality))
            ** 2
        )
    return result


def endpoint_value(
    soft_direction: list[mp.mpc],
    decay_direction: list[mp.mpc],
    scattering_cosine: mp.mpc,
    unit_circle: mp.mpc,
) -> mp.mpc:
    soft_rotated = rotate_vector(soft_direction, unit_circle)
    decay_rotated = rotate_vector(decay_direction, unit_circle)
    internal = [
        [mp.mpc(1), *decay_rotated],
        [mp.mpc(1), *negate(decay_rotated)],
        [mp.mpc(0), mp.mpc(0), mp.mpc(0), mp.mpc(0)],
    ]
    left, right = cut_momenta(internal, scattering_cosine)
    soft_left = [mp.mpc(1), *soft_rotated]
    soft_right = negate(soft_left)
    left[3] = soft_left
    right[3] = soft_right
    left_spinors = spinor_table(left)
    right_spinors = spinor_table(right)
    result = mp.mpc(0)
    for special in (1, 2):
        result += spinor_soft_factor(left_spinors, 0) * scalar_klt_four(
            left, left_spinors, special, 0
        ) * spinor_soft_factor(right_spinors, 1) * scalar_klt_four(
            right, right_spinors, special, 1
        )
        result += spinor_soft_factor(left_spinors, 1) * scalar_klt_four(
            left, left_spinors, special, 1
        ) * spinor_soft_factor(right_spinors, 0) * scalar_klt_four(
            right, right_spinors, special, 0
        )
    return result / (2 * S_VALUE * S_VALUE)


def finite_plus_components(
    internal_values: Any,
    soft_energy: float,
    soft_direction_values: Any,
    decay_direction_values: Any,
    scattering_cosine_value: complex,
    unit_circle: mp.mpc,
) -> tuple[mp.mpc, mp.mpc]:
    internal = mp_matrix(internal_values)
    soft_direction = mp_vector(soft_direction_values)
    decay_direction = mp_vector(decay_direction_values)
    scattering_cosine = mpc(scattering_cosine_value)
    rotated = rotate_internal(internal, unit_circle)
    inverse_energy_square_sum = sum(1 / momentum[0] ** 2 for momentum in rotated)
    soft = mp.mpf(str(soft_energy))
    multiplier = 3 / rotated[2][0] ** 2 / inverse_energy_square_sum
    direct = (
        soft**2
        * multiplier
        * hhh_reduced_product(rotated, scattering_cosine)
        / (S_VALUE * S_VALUE)
    )
    subtraction = endpoint_value(
        soft_direction, decay_direction, scattering_cosine, unit_circle
    )
    return direct / soft, -subtraction / soft


def finite_plus_integrand(
    internal_values: Any,
    soft_energy: float,
    soft_direction_values: Any,
    decay_direction_values: Any,
    scattering_cosine_value: complex,
    unit_circle: mp.mpc,
) -> mp.mpc:
    direct, subtraction = finite_plus_components(
        internal_values,
        soft_energy,
        soft_direction_values,
        decay_direction_values,
        scattering_cosine_value,
        unit_circle,
    )
    return direct + subtraction


def finite_plus_component(
    component: str,
    internal_values: Any,
    soft_energy: float,
    soft_direction_values: Any,
    decay_direction_values: Any,
    scattering_cosine_value: complex,
    unit_circle: mp.mpc,
) -> mp.mpc:
    direct, subtraction = finite_plus_components(
        internal_values,
        soft_energy,
        soft_direction_values,
        decay_direction_values,
        scattering_cosine_value,
        unit_circle,
    )
    if component == "direct":
        return direct
    if component == "subtraction":
        return subtraction
    raise ValueError(f"unknown additive component {component}")


def factor_root(
    direction_values: Any, scattering_cosine_value: complex, label: str
) -> mp.mpc:
    direction = mp_vector(direction_values)
    scattering_cosine = mpc(scattering_cosine_value)
    external_stereographic = mp.sqrt(
        (1 - scattering_cosine) / (1 + scattering_cosine)
    )
    denominator = 1 + direction[2]
    holomorphic = (direction[0] + 1j * direction[1]) / denominator
    antiholomorphic = (direction[0] - 1j * direction[1]) / denominator
    roots = {
        "plus_u": external_stereographic / holomorphic,
        "plus_v": antiholomorphic / external_stereographic,
        "minus_u": -1 / (external_stereographic * holomorphic),
        "minus_v": -external_stereographic * antiholomorphic,
    }
    return roots[label]


def selected_global_data(
    relative_circle: complex,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, complex, float, str, str]:
    soft_direction, decay_direction, internal = N5030.M5028.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        relative_circle,
    )
    groups = N5030.M5028.fixed_ownership_groups(
        internal,
        soft_direction,
        decay_direction,
        N5030.TARGET_COSINE,
        ownership,
    )
    owned_labels = {
        label
        for pair in collision_pairs
        for label in pair
        if ownership[label]
    }
    selected = [
        group for group in groups if owned_labels.intersection(group["labels"])
    ]
    if len(selected) != 1 or len(owned_labels) != 1:
        raise RuntimeError("cross-source evaluator requires one causally owned pole")
    selected_group = selected[0]
    label = next(iter(owned_labels))
    if not label.startswith("direct:g1:"):
        raise RuntimeError(f"unexpected owned label {label}")
    double_root = complex(selected_group["root"])
    separations = [
        abs(double_root - complex(other["root"]))
        for other in groups
        if other is not selected_group
    ]
    safe_scale = min([abs(double_root)] + separations)
    root_label = label.rsplit(":", 1)[1]
    source_component = "direct" if label.startswith("direct:") else "subtraction"
    return (
        soft_direction,
        decay_direction,
        internal,
        double_root,
        safe_scale,
        root_label,
        source_component,
    )


def global_residue(
    relative_circle: mp.mpc,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    nodes: int,
    radius_fraction: float,
) -> mp.mpc:
    (
        soft_direction,
        decay_direction,
        internal,
        double_root,
        safe_scale,
        root_label,
        source_component,
    ) = selected_global_data(complex(relative_circle), collision_pairs, ownership)
    soft_direction, decay_direction, internal = event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        relative_circle,
    )
    direction = [internal[0][index] / internal[0][0] for index in range(1, 4)]
    root = factor_root(direction, N5030.TARGET_COSINE, root_label)
    if abs(complex(root) - double_root) > 1.0e-8 * max(1.0, abs(double_root)):
        raise RuntimeError("arbitrary-precision and transported direct roots disagree")
    radius = mp.mpf(radius_fraction * safe_scale)
    total = mp.mpc(0)
    for index in range(nodes):
        phase = mp.e ** (2j * mp.pi * (mp.mpf(index) + mp.mpf("0.317")) / nodes)
        unit_circle = root + radius * phase
        total += (
            finite_plus_component(
                source_component,
                internal,
                N5030.SOFT_ENERGY,
                soft_direction,
                decay_direction,
                N5030.TARGET_COSINE,
                unit_circle,
            )
            / unit_circle
            * radius
            * phase
        )
    return total / nodes


def relative_residue(
    root: complex,
    safe_scale: float,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    relative_nodes: int,
    global_nodes: int,
    relative_fraction: float,
    global_fraction: float,
) -> mp.mpc:
    radius = mp.mpf(relative_fraction * safe_scale)
    root_mp = mpc(root)
    total = mp.mpc(0)
    for index in range(relative_nodes):
        phase = mp.e ** (
            2j * mp.pi * (mp.mpf(index) + mp.mpf("0.317")) / relative_nodes
        )
        relative_circle_mp = root_mp + radius * phase
        total += (
            global_residue(
                relative_circle_mp,
                collision_pairs,
                ownership,
                global_nodes,
                global_fraction,
            )
            / relative_circle_mp
            * radius
            * phase
        )
    return total / relative_nodes


def load_job(job_key: str) -> tuple[dict[str, Any], dict[str, Any]]:
    job = json.loads((RUN / "jobs" / f"{job_key}.json").read_text(encoding="utf-8"))
    kernel = json.loads(
        (RUN / "kernels" / f"{job_key}.json").read_text(encoding="utf-8")
    )
    return job, kernel


def configure_kernel(kernel: dict[str, Any]) -> None:
    target = complex(
        float(kernel["argument"]["target_cosine"]["real"]),
        float(kernel["argument"]["target_cosine"]["imaginary"]),
    )
    M5034.configure(kernel["event"], target)


def validate_port(job_key: str, dps: int) -> dict[str, Any]:
    _, kernel = load_job(job_key)
    configure_kernel(kernel)
    target = N5030.TARGET_COSINE
    checks = []
    for relative_circle, unit_circle in (
        (complex(0.7, 0.2), complex(0.61, 0.37)),
        (complex(-0.4, 0.8), complex(-0.72, 0.19)),
        (complex(1.2, -0.3), complex(1.31, 0.41)),
    ):
        soft_direction, decay_direction, internal = N5030.M5028.event_geometry(
            N5030.SOFT_ENERGY,
            complex(N5030.SOFT_COSINE, 0.0),
            complex(N5030.DECAY_COSINE, 0.0),
            relative_circle,
        )
        double = N5030.M5028.M5026.finite_plus_integrand(
            internal,
            N5030.SOFT_ENERGY,
            soft_direction,
            decay_direction,
            target,
            unit_circle,
        )
        arbitrary = finite_plus_integrand(
            internal,
            N5030.SOFT_ENERGY,
            soft_direction,
            decay_direction,
            target,
            mpc(unit_circle),
        )
        relative = abs(complex(arbitrary) - double) / max(abs(double), 1.0)
        checks.append(
            {
                "relative_circle": str(relative_circle),
                "unit_circle": str(unit_circle),
                "double": str(double),
                "arbitrary_precision": serialized(arbitrary),
                "relative_difference": relative,
            }
        )
    return {
        "dps": dps,
        "checks": checks,
        "maximum_relative_difference": max(row["relative_difference"] for row in checks),
        "passed": max(row["relative_difference"] for row in checks) < 2.0e-10,
    }


def evaluate_job(arguments: argparse.Namespace) -> dict[str, Any]:
    job, kernel = load_job(arguments.job_key)
    configure_kernel(kernel)
    unstable = [
        (int(chamber["chamber_index"]), row)
        for chamber in kernel["fixed_event_integral_gate"]["chambers"]
        for row in chamber["residue_catalog"]
        if not row["stable"]
    ]
    if len(unstable) != 1:
        raise RuntimeError(f"expected one unstable residue, found {len(unstable)}")
    chamber_index, row = unstable[0]
    ownership = N5030.physical_chambers()[1][chamber_index]
    root = complex(row["root"])
    safe_scale = float(row["outer_radius"]) / float(row["residue_contour_fraction"])
    collision_pairs = [tuple(pair) for pair in row["pairs"]]
    pair_components = {
        "direct" if label.startswith("direct:") else "subtraction"
        for pair in collision_pairs
        for label in pair
    }
    if pair_components != {"direct", "subtraction"}:
        raise RuntimeError("the source-separated evaluator requires a cross-source pair")
    values = []
    for relative_fraction in arguments.relative_fractions:
        for global_fraction in arguments.global_fractions:
            value = relative_residue(
                root,
                safe_scale,
                collision_pairs,
                ownership,
                arguments.relative_nodes,
                arguments.global_nodes,
                relative_fraction,
                global_fraction,
            )
            values.append(
                {
                    "relative_fraction": relative_fraction,
                    "global_fraction": global_fraction,
                    "value": serialized(value),
                    "magnitude": float(abs(value)),
                }
            )
    complex_values = [
        complex(float(row["value"]["real"]), float(row["value"]["imaginary"]))
        for row in values
    ]
    mean = sum(complex_values) / len(complex_values)
    spread = max(abs(value - mean) for value in complex_values)
    result = {
        "checkpoint_marker": MARKER,
        "job_key": job["job_key"],
        "dps": arguments.dps,
        "relative_nodes": arguments.relative_nodes,
        "global_nodes": arguments.global_nodes,
        "relative_fractions": arguments.relative_fractions,
        "global_fractions": arguments.global_fractions,
        "port_validation": validate_port(arguments.job_key, arguments.dps),
        "collision_pairs": [list(pair) for pair in collision_pairs],
        "source_separation": {
            "components": sorted(pair_components),
            "rule": "retain_the_component_that_owns_the_local_global_pole",
            "discarded_component_local_residue": "exactly_zero_by_Cauchy_analyticity",
            "guard": "local_radius_is_smaller_than_every_other_global_pole_separation",
        },
        "root": str(root),
        "safe_scale": safe_scale,
        "values": values,
        "mean": {"real": mean.real, "imaginary": mean.imag},
        "maximum_spread": spread,
        "relative_spread": spread / max(abs(mean), 1.0e-30),
        "accepted": False,
        "promoted": False,
        "valid_for_production_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    M5036.atomic_json(OUTPUT_DIRECTORY / f"{job['job_key']}.json", result)
    return result


def parse_floats(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--job-key", default="E040__S503403_N0001__A14__primary24"
    )
    parser.add_argument("--dps", type=int, default=60)
    parser.add_argument("--relative-nodes", type=int, default=24)
    parser.add_argument("--global-nodes", type=int, default=24)
    parser.add_argument("--relative-fractions", type=parse_floats, default=[0.1, 0.05])
    parser.add_argument("--global-fractions", type=parse_floats, default=[0.15, 0.3])
    parser.add_argument("--validate-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.dps < 40 or arguments.relative_nodes < 8 or arguments.global_nodes < 8:
        raise ValueError("precision floors are too small")
    mp.mp.dps = arguments.dps
    if arguments.validate_only:
        result = validate_port(arguments.job_key, arguments.dps)
    else:
        result = evaluate_job(arguments)
    print(json.dumps(result, indent=2, allow_nan=False))
    passed = result["passed"] if arguments.validate_only else result["port_validation"]["passed"]
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
