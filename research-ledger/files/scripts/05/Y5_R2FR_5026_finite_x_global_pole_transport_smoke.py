from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5025 = (
    POST
    / "scripts"
    / "Y5_R2FR_5025_stereographic_two_torus_sector_endpoint_gate.py"
)
REFERENCE_COSINE = complex(0.3, 0.0)
ROOT_LABELS = ("plus_u", "plus_v", "minus_u", "minus_v")
ROOT_COINCIDENCE_RELATIVE_TOLERANCE = 5.0e-12
MINIMUM_CONDITIONED_BASE_RADIUS = 2.0e-3
TARGET_5018 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5018"
    / "known_master_without_hhh_and_matched_hhh_target.csv"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5025 = load_module("mts_5025_for_5026", SCRIPT_5025)
M5024 = M5025.M5024
M5022 = M5025.M5022
M5017 = M5025.M5017


def internal_direction(momentum: np.ndarray) -> np.ndarray:
    return np.asarray(momentum[1:] / momentum[0], dtype=np.complex128)


def add_direction_roots(
    rows: list[dict[str, Any]],
    source: str,
    direction: np.ndarray,
    scattering_cosine: complex,
) -> None:
    target = M5024.all_factor_roots(direction, scattering_cosine)
    start = M5024.all_factor_roots(direction, REFERENCE_COSINE)
    for label in ROOT_LABELS:
        rows.append(
            {
                "root": target[label],
                "labels": [f"{source}:{label}"],
                "desired_values": [abs(start[label]) < 1.0],
            }
        )


def finite_plus_root_groups(
    internal: np.ndarray,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for internal_index, momentum in enumerate(internal):
        add_direction_roots(
            rows,
            f"direct:g{internal_index + 1}",
            internal_direction(momentum),
            scattering_cosine,
        )
    add_direction_roots(
        rows, "subtraction:soft", soft_direction, scattering_cosine
    )
    add_direction_roots(
        rows, "subtraction:decay", decay_direction, scattering_cosine
    )
    groups: list[dict[str, Any]] = []
    for row in rows:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(row["root"] - candidate["root"])
                < ROOT_COINCIDENCE_RELATIVE_TOLERANCE
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
                "coincident finite-x roots have mixed physical-sheet ownership: "
                + ", ".join(group["labels"])
            )
        group["desired_inside"] = group["desired_values"][0]
    return groups


def finite_plus_integrand(
    internal: np.ndarray,
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> complex:
    rotated_internal = M5024.rotate_internal(internal, unit_circle)
    inverse_energy_square_sum = sum(
        1.0 / (momentum[0] * momentum[0])
        for momentum in rotated_internal
    )
    multiplier = (
        3.0
        / (rotated_internal[2, 0] * rotated_internal[2, 0])
        / inverse_energy_square_sum
    )
    direct = (
        soft_energy
        * soft_energy
        * multiplier
        * M5017.hhh_reduced_product(
            rotated_internal, scattering_cosine, 1.0
        )
        / (M5017.S_VALUE * M5017.S_VALUE)
    )
    subtraction = M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    return complex((direct - subtraction) / soft_energy)


def circle_average(
    evaluator: Callable[[complex], complex], nodes: int, radius: float = 1.0
) -> complex:
    return complex(
        sum(
            evaluator(
                radius
                * np.exp(2.0j * np.pi * (index + 0.271) / nodes)
            )
            for index in range(nodes)
        )
        / nodes
    )


def maximal_log_annulus_radius(groups: list[dict[str, Any]]) -> float:
    moduli = sorted(abs(complex(group["root"])) for group in groups)
    unique_moduli: list[float] = []
    for modulus in moduli:
        if modulus <= 0.0:
            continue
        if not unique_moduli or abs(math.log(modulus / unique_moduli[-1])) > 1.0e-12:
            unique_moduli.append(modulus)
    if len(unique_moduli) < 2:
        if not unique_moduli:
            raise RuntimeError("global pole catalogue has no finite nonzero roots")
        return unique_moduli[0]
    lower, upper = max(
        zip(unique_moduli[:-1], unique_moduli[1:]),
        key=lambda pair: math.log(pair[1] / pair[0]),
    )
    return math.sqrt(lower * upper)


def conditioned_global_base_radius(groups: list[dict[str, Any]]) -> float:
    minimum_root_modulus = min(abs(complex(group["root"])) for group in groups)
    subminimum_radius = 0.2 * minimum_root_modulus
    if subminimum_radius >= MINIMUM_CONDITIONED_BASE_RADIUS:
        return subminimum_radius
    return maximal_log_annulus_radius(groups)


def finite_plus_global_cycle(
    internal: np.ndarray,
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    global_nodes: int,
    residue_nodes: int,
) -> tuple[complex, int, list[dict[str, Any]]]:
    groups = finite_plus_root_groups(
        internal,
        soft_direction,
        decay_direction,
        scattering_cosine,
    )
    evaluator = lambda unit_circle: finite_plus_integrand(
        internal,
        soft_energy,
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    base_radius = conditioned_global_base_radius(groups)
    result = circle_average(evaluator, global_nodes, base_radius)
    correction_rows: list[dict[str, Any]] = []
    for group in groups:
        root = group["root"]
        desired_inside = group["desired_inside"]
        currently_inside = abs(root) < base_radius
        if desired_inside == currently_inside:
            continue
        separations = [
            abs(root - other["root"])
            for other in groups
            if other is not group
        ]
        safe_scale = min([abs(root)] + separations) if separations else abs(root)
        radius = max(1.0e-7, 0.07 * safe_scale)
        residue = M5024.local_residue(
            evaluator, root, radius, residue_nodes
        )
        if desired_inside:
            result += residue
            orientation = "add_outside_to_inside"
        else:
            result -= residue
            orientation = "subtract_inside_to_outside"
        correction_rows.append(
            {
                "root": str(root),
                "root_modulus": abs(root),
                "labels": group["labels"],
                "orientation": orientation,
                "residue": str(residue),
                "base_radius": base_radius,
            }
        )
    return result, len(correction_rows), correction_rows


def phase_event(
    point: np.ndarray,
    scattering_cosine: complex,
    global_nodes: int,
    residue_nodes: int,
) -> tuple[complex, int]:
    soft_energy = min(max(float(point[0]), 1.0e-7), 1.0 - 1.0e-7)
    soft_direction = M5024.direction_from_polar_x(
        complex(float(point[1]), 0.0), 0.0
    ).real
    decay_direction = M5024.direction_from_polar_x(
        complex(float(point[2]), 0.0),
        2.0 * math.pi * float(point[3]),
    ).real
    internal = M5017.sequential_three_body(
        soft_energy, soft_direction, decay_direction
    )
    value, correction_count, _ = finite_plus_global_cycle(
        internal,
        soft_energy,
        soft_direction,
        decay_direction,
        scattering_cosine,
        global_nodes,
        residue_nodes,
    )
    return -2.0 * value / math.pi, correction_count


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def pointwise_gate(global_nodes: int, residue_nodes: int) -> dict[str, Any]:
    soft_energy = 0.37
    soft_direction = M5017.direction(0.31, 0.0)
    decay_direction = M5017.direction(0.64, 0.27)
    internal = M5017.sequential_three_body(
        soft_energy, soft_direction, decay_direction
    )
    evaluator = lambda unit_circle: finite_plus_integrand(
        internal,
        soft_energy,
        soft_direction,
        decay_direction,
        REFERENCE_COSINE,
        unit_circle,
    )
    physical_unit = circle_average(evaluator, max(256, global_nodes))
    physical_cycle, physical_corrections, _ = finite_plus_global_cycle(
        internal,
        soft_energy,
        soft_direction,
        decay_direction,
        REFERENCE_COSINE,
        global_nodes,
        residue_nodes,
    )
    crossed_cosine = complex(1.5, 0.08)
    crossed_cycle, crossed_corrections, correction_rows = (
        finite_plus_global_cycle(
            internal,
            soft_energy,
            soft_direction,
            decay_direction,
            crossed_cosine,
            global_nodes,
            residue_nodes,
        )
    )
    return {
        "physical_unit_circle": str(physical_unit),
        "physical_transported_cycle": str(physical_cycle),
        "physical_control_residual": abs(physical_cycle - physical_unit)
        / max(abs(physical_unit), 1.0e-30),
        "physical_correction_count": physical_corrections,
        "crossed_transported_cycle": str(crossed_cycle),
        "crossed_correction_count": crossed_corrections,
        "crossed_corrections": correction_rows,
        "physical_control_passed": (
            abs(physical_cycle - physical_unit)
            / max(abs(physical_unit), 1.0e-30)
            < 1.0e-6
        ),
    }


def integration_smoke(
    power: int,
    seeds: tuple[int, ...],
    configuration_names: tuple[str, ...],
    global_nodes: int,
    residue_nodes: int,
) -> dict[str, Any]:
    configurations = (
        ("physical_z0p3", complex(0.3, 0.0)),
        ("crossed_z1p5", complex(1.5, 0.08)),
    )
    configurations = tuple(
        row for row in configurations if row[0] in configuration_names
    )
    if len(configurations) != len(configuration_names):
        raise ValueError("unknown configuration")
    points = {
        seed: qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    rows: list[dict[str, Any]] = []
    for configuration, scattering_cosine in configurations:
        seed_means: list[complex] = []
        seed_mean_corrections: list[float] = []
        for seed in seeds:
            values_and_counts = [
                phase_event(
                    point,
                    scattering_cosine,
                    global_nodes,
                    residue_nodes,
                )
                for point in points[seed]
            ]
            seed_means.append(
                complex(np.mean([row[0] for row in values_and_counts]))
            )
            seed_mean_corrections.append(
                float(np.mean([row[1] for row in values_and_counts]))
            )
        mean, real_error, imaginary_error = aggregate(seed_means)
        rows.append(
            {
                "configuration": configuration,
                "scattering_cosine": str(scattering_cosine),
                "D_hhh_direct_over_G3": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "mean_correction_count": float(
                    np.mean(seed_mean_corrections)
                ),
                "seed_means": [str(value) for value in seed_means],
                "seed_mean_corrections": seed_mean_corrections,
            }
        )
    return {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "global_nodes": global_nodes,
        "residue_nodes": residue_nodes,
        "rows": rows,
    }


def cyclic_smoke(
    power: int,
    seeds: tuple[int, ...],
    physical_cosines: tuple[float, ...],
    crossed_epsilon: float,
    global_nodes: int,
    residue_nodes: int,
) -> dict[str, Any]:
    crossing_arguments: set[float] = set(physical_cosines)
    crossing_map: dict[float, tuple[float, float, float, float]] = {}
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        crossing_arguments.update((z_t, z_u))
        crossing_map[cosine] = (t_ratio, u_ratio, z_t, z_u)
    ordered_arguments = tuple(sorted(crossing_arguments))
    points = {
        seed: qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }
    samples: dict[int, dict[float, np.ndarray]] = {}
    correction_counts: dict[int, dict[float, float]] = {}
    for seed in seeds:
        samples[seed] = {}
        correction_counts[seed] = {}
        for argument in ordered_arguments:
            target = complex(
                argument,
                crossed_epsilon if abs(argument) > 1.0 else 0.0,
            )
            values_and_counts = [
                phase_event(
                    point, target, global_nodes, residue_nodes
                )
                for point in points[seed]
            ]
            samples[seed][argument] = np.asarray(
                [row[0] for row in values_and_counts],
                dtype=np.complex128,
            )
            correction_counts[seed][argument] = float(
                np.mean([row[1] for row in values_and_counts])
            )
    direct_rows: list[dict[str, Any]] = []
    for argument in ordered_arguments:
        seed_means = [
            complex(np.mean(samples[seed][argument])) for seed in seeds
        ]
        mean, real_error, imaginary_error = aggregate(seed_means)
        direct_rows.append(
            {
                "scattering_cosine": argument,
                "sheet": (
                    f"upper_epsilon_{crossed_epsilon}"
                    if abs(argument) > 1.0
                    else "physical"
                ),
                "D_hhh_direct_over_G3": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "mean_correction_count": float(
                    np.mean(
                        [
                            correction_counts[seed][argument]
                            for seed in seeds
                        ]
                    )
                ),
            }
        )
    cyclic_rows: list[dict[str, Any]] = []
    cyclic_central: list[float] = []
    for cosine in physical_cosines:
        t_ratio, u_ratio, z_t, z_u = crossing_map[cosine]
        seed_means: list[complex] = []
        for seed in seeds:
            correlated = (
                samples[seed][cosine]
                + t_ratio**3 * samples[seed][z_t]
                + u_ratio**3 * samples[seed][z_u]
            )
            seed_means.append(complex(np.mean(correlated)))
        mean, real_error, imaginary_error = aggregate(seed_means)
        cyclic_central.append(mean.real)
        cyclic_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "z_t": z_t,
                "z_u": z_u,
                "cyclic_D_hhh_over_G3": str(mean),
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
            }
        )
    shape = 1.0 - np.asarray(physical_cosines, dtype=float) ** 2
    central = np.asarray(cyclic_central, dtype=float)
    local_coefficient = float(shape @ central / (shape @ shape))
    nonlocal_vector = central - local_coefficient * shape
    with TARGET_5018.open("r", encoding="utf-8", newline="") as handle:
        target_rows = list(csv.DictReader(handle))
    target_by_cosine = {
        round(float(row["physical_s_channel_cosine"]), 12): float(
            row["required_matched_hhh_nonlocal_cyclic_D_over_G3"]
        )
        for row in target_rows
    }
    comparison_rows: list[dict[str, Any]] = []
    differences: list[float] = []
    for cosine, value in zip(physical_cosines, nonlocal_vector):
        target = target_by_cosine[round(cosine, 12)]
        difference = float(value - target)
        differences.append(difference)
        comparison_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "global_pole_nonlocal_component": float(value),
                "required_5018_nonlocal_component": target,
                "difference": difference,
            }
        )
    return {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "crossed_epsilon": crossed_epsilon,
        "global_nodes": global_nodes,
        "residue_nodes": residue_nodes,
        "direct_rows": direct_rows,
        "cyclic_rows": cyclic_rows,
        "best_local_stu_coefficient": local_coefficient,
        "comparison_rows": comparison_rows,
        "RMS_nonlocal_target_difference": float(
            np.sqrt(np.mean(np.asarray(differences) ** 2))
        ),
        "target_fitted": False,
        "remaining_polar_transport_required": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=3)
    parser.add_argument("--seeds", default="50261,50262")
    parser.add_argument(
        "--configurations", default="physical_z0p3,crossed_z1p5"
    )
    parser.add_argument("--global-nodes", type=int, default=16)
    parser.add_argument("--residue-nodes", type=int, default=12)
    parser.add_argument("--cyclic-smoke", action="store_true")
    parser.add_argument("--skip-integration", action="store_true")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--crossed-epsilon", type=float, default=0.08)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = {
        "pointwise_gate": pointwise_gate(
            arguments.global_nodes, arguments.residue_nodes
        ),
        "integration_smoke": None
        if arguments.skip_integration
        else integration_smoke(
            arguments.power,
            tuple(int(value) for value in arguments.seeds.split(",")),
            tuple(arguments.configurations.split(",")),
            arguments.global_nodes,
            arguments.residue_nodes,
        ),
        "cyclic_smoke": cyclic_smoke(
            arguments.power,
            tuple(int(value) for value in arguments.seeds.split(",")),
            tuple(float(value) for value in arguments.physical_cosines.split(",")),
            arguments.crossed_epsilon,
            arguments.global_nodes,
            arguments.residue_nodes,
        )
        if arguments.cyclic_smoke
        else None,
        "finite_x_global_pole_transport_constructed": True,
        "remaining_polar_cycle_transport_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    serialized = json.dumps(result, indent=2)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
