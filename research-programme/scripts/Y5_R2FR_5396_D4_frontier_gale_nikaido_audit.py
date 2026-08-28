from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
from types import SimpleNamespace
from typing import Any

from mpmath import iv


POST = Path(__file__).resolve().parents[1]
PRIMARY = POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
OUTPUT = POST / "source-intake" / "functional_rg" / "5396"
STATE = (
    OUTPUT
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X002_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)


def load_primary() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5396_gale_nikaido_primary", PRIMARY
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def closed_arc_displacement(
    module: Any,
    global_radius: float,
    arc_index: int,
    arc_subindex: int,
    arc_subdivision_count: int,
    global_arc_count: int = 4,
) -> Any:
    phase_lower = (
        arc_index + arc_subindex / arc_subdivision_count
    ) * 2 * math.pi / global_arc_count
    phase_upper = (
        arc_index + (arc_subindex + 1) / arc_subdivision_count
    ) * 2 * math.pi / global_arc_count
    phase = module.cbox(phase_lower, phase_upper)
    return module.cpoint(global_radius) * (
        iv.cos(phase) + module.cpoint(1j) * iv.sin(phase)
    )


def interval_sign(bounds: tuple[float, float]) -> int:
    if bounds[0] > 0.0:
        return 1
    if bounds[1] < 0.0:
        return -1
    return 0


def selected_frontier(
    arguments: argparse.Namespace, state: dict[str, Any]
) -> tuple[float, float, float, float, int, str, str]:
    explicit_values = (
        arguments.x_lower,
        arguments.x_upper,
        arguments.t_lower,
        arguments.t_upper,
        arguments.refinement_depth,
        arguments.refinement_path,
    )
    if any(value is not None for value in explicit_values):
        if not all(value is not None for value in explicit_values):
            raise ValueError(
                "explicit frontier requires x/t bounds, depth, and path together"
            )
        return (
            float(arguments.x_lower),
            float(arguments.x_upper),
            float(arguments.t_lower),
            float(arguments.t_upper),
            int(arguments.refinement_depth),
            str(arguments.refinement_path),
            "explicit_cli",
        )
    if not state["stack"]:
        raise RuntimeError("selected frontier state is already empty")
    try:
        frontier = state["stack"][arguments.stack_index]
    except IndexError as error:
        raise ValueError(
            f"stack index {arguments.stack_index} is outside the live frontier"
        ) from error
    return (
        float(frontier[0]),
        float(frontier[1]),
        float(frontier[2]),
        float(frontier[3]),
        int(frontier[4]),
        str(frontier[5]),
        f"state_stack[{arguments.stack_index}]",
    )


def jet_boundary_energy(module: Any, owner: str, coordinate: Any) -> Any:
    jet = module.M5395.Jet2
    jet_sqrt = module.M5395.jet_sqrt
    minimum, maximum = module.M5308.energy_limits()
    if owner == "ENERGY_MINIMUM":
        return jet.constant(module.cpoint(minimum))
    if owner == "ENERGY_MAXIMUM":
        return jet.constant(module.cpoint(maximum))
    first_owner = owner.split("|")[0]
    surface_id, branch_id = first_owner.rsplit(":", 1)
    if branch_id not in {"Q01", "Q02"}:
        raise RuntimeError(f"unsupported hard-boundary branch {owner}")
    component, soft_label, decay_label = surface_id.split("_")
    hard_sign = 1 if component == "MC04" else -1
    soft_sign = 1 if soft_label == "SP" else -1
    decay_sign = 1 if decay_label == "DP" else -1
    soft_cosine = coordinate * soft_sign
    decay_cosine = module.cpoint(
        decay_sign * module.M5394.ABSOLUTE_DECAY_COSINE
    )
    soft_sine = jet_sqrt(1 - soft_cosine * soft_cosine)
    decay_sine = module.cpoint(
        math.sqrt(1 - module.M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    relative = soft_cosine * decay_cosine - soft_sine * decay_sine
    coefficient_a = (
        soft_cosine - module.M5394.TARGET_COSINE
    ) * (1 + hard_sign * relative)
    coefficient_b = (
        jet.constant(decay_cosine) - soft_cosine * relative
    ) * (2 * hard_sign)
    coefficient_c = (
        soft_cosine + module.M5394.TARGET_COSINE
    ) * (hard_sign * relative - 1)
    discriminant_root = jet_sqrt(
        coefficient_b * coefficient_b
        - 4 * coefficient_a * coefficient_c
    )
    candidates: list[Any] = []
    if module.M5258.lower_abs(2 * coefficient_a.value) > 0.0:
        candidates.extend(
            (
                (-coefficient_b - discriminant_root)
                / (2 * coefficient_a),
                (-coefficient_b + discriminant_root)
                / (2 * coefficient_a),
            )
        )
    for stable_denominator in (
        coefficient_b - discriminant_root,
        coefficient_b + discriminant_root,
    ):
        if module.M5258.lower_abs(stable_denominator.value) > 0.0:
            candidates.append(-2 * coefficient_c / stable_denominator)
    if not candidates:
        raise RuntimeError(f"no stable jet hard-boundary chart: {owner}")
    coordinate_midpoint = complex(
        module.M5394.midpoint(coordinate.value)
    ).real
    expected_energy = float(
        module.M5308.boundary_energy(owner, coordinate_midpoint)
    )
    expected_recoil = math.sqrt(max(0.0, 1.0 - expected_energy))
    selected_recoil = min(
        candidates,
        key=lambda value: abs(
            complex(module.M5394.midpoint(value.value))
            - expected_recoil
        ),
    )
    return 1 - selected_recoil * selected_recoil


def jet_native_angle(
    module: Any,
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    displacement: Any,
) -> Any:
    jet_sqrt = module.M5395.jet_sqrt
    decay_cosine = module.cpoint(
        configuration["decay_sign"]
        * module.M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = module.cpoint(
        math.sqrt(1 - module.M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * jet_sqrt(-q_value)
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
        / ((1 + soft_cosine) * factor_f2 * decay_sine)
    )
    selected_root = soft_sine / (
        (1 + soft_cosine) * external_root
    )
    unit_circle = selected_root + displacement
    recoil_squared = recoil * recoil
    relative_cosine_constant = soft_cosine * decay_cosine
    relative_cosine_laurent = soft_sine * decay_sine / 2
    first_energy_constant = (1 + recoil_squared) / 2
    first_energy_coefficient = -(1 - recoil_squared) / 2
    longitudinal_constant = -(1 - recoil_squared) / 2
    longitudinal_coefficient = (1 - recoil) * (1 - recoil) / 2
    plus_coefficient = (
        first_energy_coefficient
        + longitudinal_coefficient * soft_cosine
    )
    plus_constant = (
        first_energy_constant
        + longitudinal_constant * soft_cosine
        + recoil * decay_cosine
        + plus_coefficient * relative_cosine_constant
    )
    plus_laurent = plus_coefficient * relative_cosine_laurent
    holomorphic_constant = soft_sine * (
        longitudinal_constant
        + longitudinal_coefficient * relative_cosine_constant
    )
    holomorphic_laurent = (
        soft_sine
        * longitudinal_coefficient
        * relative_cosine_laurent
    )
    target = -9 + 1j * epsilon
    external_transverse = jet_sqrt(1 - target * target)
    polynomial = (
        -external_transverse
        * unit_circle
        * (
            holomorphic_laurent * representative * representative
            + holomorphic_constant * representative
            + holomorphic_laurent
            + recoil * decay_sine
        )
        + (1 - target)
        * (
            plus_laurent * representative * representative
            + plus_constant * representative
            + plus_laurent
        )
    )
    return polynomial / representative


def conjugate_interval(module: Any, value: Any) -> Any:
    real_lower, real_upper = module.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = module.M5394.imaginary_bounds(value)
    return module.cbox(
        real_lower, real_upper, -imaginary_upper, -imaginary_lower
    )


def centered_native_path_derivatives(
    module: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    displacement: Any,
    include_determinant: bool = False,
) -> tuple[Any, Any] | tuple[Any, Any, tuple[float, float]]:
    jet = module.M5395.Jet2
    previous_dimension = jet.dimension
    jet.dimension = 4
    domains = (coordinate, parameter, epsilon, displacement)
    centers = tuple(
        module.M5385.complex_midpoint_box(value) for value in domains
    )

    def evaluate(values: tuple[Any, ...]) -> Any:
        coordinate_jet, parameter_jet, epsilon_jet, displacement_jet = (
            jet.variable(value, index) for index, value in enumerate(values)
        )
        if path_segment == "LEFT_CONNECTOR":
            boundary_owner = cell["lower_energy_boundary"]
        elif path_segment == "RIGHT_CONNECTOR":
            boundary_owner = cell["upper_energy_boundary"]
        else:
            raise ValueError(
                "centred Jacobian audit supports connector paths only"
            )
        energy = jet_boundary_energy(
            module, boundary_owner, coordinate_jet
        ) + 1j * module.DEFAULT_ENERGY_DEFORMATION * parameter_jet
        recoil = module.M5395.jet_sqrt(1 - energy)
        return jet_native_angle(
            module,
            configuration,
            epsilon_jet,
            recoil,
            coordinate_jet * configuration["soft_sign"],
            displacement_jet,
        )

    try:
        center_jet = evaluate(centers)
        box_jet = evaluate(domains)
        derivatives: list[Any] = []
        for derivative_index in (0, 1):
            enclosure = center_jet.gradient[derivative_index]
            for domain_index, domain in enumerate(domains):
                enclosure += box_jet.hessian[derivative_index][
                    domain_index
                ] * (domain - centers[domain_index])
            derivatives.append(enclosure)
        if include_determinant:
            center_product = (
                conjugate_interval(module, center_jet.gradient[0])
                * center_jet.gradient[1]
            )
            determinant_lower, determinant_upper = (
                module.M5394.imaginary_bounds(center_product)
            )
            for domain_index, domain in enumerate(domains):
                domain_delta = domain - centers[domain_index]
                derivative_x_delta = (
                    box_jet.hessian[0][domain_index] * domain_delta
                )
                derivative_t_delta = (
                    box_jet.hessian[1][domain_index] * domain_delta
                )
                contribution = (
                    conjugate_interval(module, derivative_x_delta)
                    * box_jet.gradient[1]
                    + conjugate_interval(module, box_jet.gradient[0])
                    * derivative_t_delta
                )
                contribution_lower, contribution_upper = (
                    module.M5394.imaginary_bounds(contribution)
                )
                determinant_lower = math.nextafter(
                    determinant_lower + contribution_lower, -math.inf
                )
                determinant_upper = math.nextafter(
                    determinant_upper + contribution_upper, math.inf
                )
            return (
                derivatives[0],
                derivatives[1],
                (determinant_lower, determinant_upper),
            )
        return derivatives[0], derivatives[1]
    finally:
        jet.dimension = previous_dimension


def principal_minor_bounds(
    module: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    displacement: Any,
) -> dict[str, Any]:
    derivative_x, derivative_t, determinant = (
        centered_native_path_derivatives(
            module,
            configuration,
            cell,
            path_segment,
            coordinate,
            parameter,
            epsilon,
            displacement,
            True,
        )
    )
    derivative_x_real = module.M5394.real_bounds(derivative_x)
    derivative_x_imaginary = module.M5394.imaginary_bounds(derivative_x)
    derivative_t_real = module.M5394.real_bounds(derivative_t)
    derivative_t_imaginary = module.M5394.imaginary_bounds(derivative_t)
    return {
        "j11": derivative_x_real,
        "j12": derivative_t_real,
        "j21": derivative_x_imaginary,
        "j22": derivative_t_imaginary,
        "determinant": determinant,
    }


def minimum_abs_lower(bounds: tuple[float, float]) -> float:
    sign = interval_sign(bounds)
    if sign > 0:
        return bounds[0]
    if sign < 0:
        return -bounds[1]
    return 0.0


def scaled_interval(
    value: tuple[float, float], coefficient: float
) -> tuple[float, float]:
    products = (coefficient * value[0], coefficient * value[1])
    return (
        math.nextafter(min(products), -math.inf),
        math.nextafter(max(products), math.inf),
    )


def added_intervals(
    left: tuple[float, float], right: tuple[float, float]
) -> tuple[float, float]:
    return (
        math.nextafter(left[0] + right[0], -math.inf),
        math.nextafter(left[1] + right[1], math.inf),
    )


def inverse_midpoint_preconditioner(
    module: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    displacement: Any,
) -> tuple[tuple[float, float], tuple[float, float]]:
    derivative_x, derivative_t = centered_native_path_derivatives(
        module,
        configuration,
        cell,
        path_segment,
        coordinate,
        parameter,
        epsilon,
        displacement,
    )
    derivative_x_value = complex(module.M5394.midpoint(derivative_x))
    derivative_t_value = complex(module.M5394.midpoint(derivative_t))
    j11 = derivative_x_value.real
    j12 = derivative_t_value.real
    j21 = derivative_x_value.imag
    j22 = derivative_t_value.imag
    determinant = j11 * j22 - j12 * j21
    if determinant <= 0.0:
        raise RuntimeError(
            "midpoint Jacobian does not have positive orientation"
        )
    return (
        (j22 / determinant, -j12 / determinant),
        (-j21 / determinant, j11 / determinant),
    )


def run_audit(arguments: argparse.Namespace) -> dict[str, Any]:
    module = load_primary()
    module.set_below_normal_priority()
    iv.dps = module.INTERVAL_DIGITS
    explicit_frontier = any(
        value is not None
        for value in (
            arguments.x_lower,
            arguments.x_upper,
            arguments.t_lower,
            arguments.t_upper,
            arguments.refinement_depth,
            arguments.refinement_path,
        )
    )
    state = {} if explicit_frontier else module.read_json(STATE)
    (
        x_lower,
        x_upper,
        t_lower,
        t_upper,
        depth,
        refinement_path,
        frontier_source,
    ) = selected_frontier(arguments, state)
    mapped_cell_id = str(arguments.mapped_cell_id)
    term_id = str(arguments.term_id)
    path_segment = str(arguments.path_segment)
    cell = next(
        row
        for row in module.away_term_support_cells()
        if row["mapped_cell_id"] == mapped_cell_id
    )
    configuration = module.configuration_variants(term_id)[0]
    epsilon_row = module.epsilon_boxes(
        SimpleNamespace(
            combined_regulator_box=True,
            combined_regulator_slab_count=2,
            epsilon_subdivisions=1,
        )
    )[0]
    epsilon = module.epsilon_interval(epsilon_row)
    coordinate = module.cbox(float(x_lower), float(x_upper))
    parameter = module.cbox(float(t_lower), float(t_upper))
    energy = module.deformed_path_energy_dual(
        cell, path_segment, coordinate, parameter
    ).value
    _, geometry = module.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    global_radius = 1.0e-7 * max(
        1.0, module.M5258.upper_abs(geometry["selected_root"])
    )
    preconditioner = inverse_midpoint_preconditioner(
        module,
        configuration,
        cell,
        path_segment,
        module.cpoint(0.5 * (float(x_lower) + float(x_upper))),
        module.cpoint(0.5 * (float(t_lower) + float(t_upper))),
        module.cpoint(
            0.5
            * (
                float(epsilon_row["epsilon_real_lower"])
                + float(epsilon_row["epsilon_real_upper"])
            )
        ),
        module.cpoint(global_radius),
    )
    preconditioner_determinant = (
        preconditioner[0][0] * preconditioner[1][1]
        - preconditioner[0][1] * preconditioner[1][0]
    )
    univalence_direction = (
        preconditioner[0][0] + preconditioner[1][0],
        preconditioner[0][1] + preconditioner[1][1],
    )
    leaf_rows: list[dict[str, Any]] = []
    scheme_rows: list[dict[str, Any]] = []
    for x_count, t_count, epsilon_real_count, arc_subdivision_count in (
        (1, 1, 1, 1),
        (2, 2, 2, 2),
        (4, 4, 4, 4),
    ):
        started = time.time()
        local_rows: list[dict[str, Any]] = []
        for x_index in range(x_count):
            local_x_lower = float(x_lower) + (
                float(x_upper) - float(x_lower)
            ) * x_index / x_count
            local_x_upper = float(x_lower) + (
                float(x_upper) - float(x_lower)
            ) * (x_index + 1) / x_count
            for t_index in range(t_count):
                local_t_lower = float(t_lower) + (
                    float(t_upper) - float(t_lower)
                ) * t_index / t_count
                local_t_upper = float(t_lower) + (
                    float(t_upper) - float(t_lower)
                ) * (t_index + 1) / t_count
                for epsilon_real_index in range(epsilon_real_count):
                    epsilon_real_lower = float(
                        epsilon_row["epsilon_real_lower"]
                    ) + (
                        float(epsilon_row["epsilon_real_upper"])
                        - float(epsilon_row["epsilon_real_lower"])
                    ) * epsilon_real_index / epsilon_real_count
                    epsilon_real_upper = float(
                        epsilon_row["epsilon_real_lower"]
                    ) + (
                        float(epsilon_row["epsilon_real_upper"])
                        - float(epsilon_row["epsilon_real_lower"])
                    ) * (epsilon_real_index + 1) / epsilon_real_count
                    local_epsilon = module.cbox(
                        epsilon_real_lower,
                        epsilon_real_upper,
                        float(epsilon_row["epsilon_imaginary_lower"]),
                        float(epsilon_row["epsilon_imaginary_upper"]),
                    )
                    for arc_index in range(4):
                        for arc_subindex in range(
                            arc_subdivision_count
                        ):
                            displacement = closed_arc_displacement(
                                module,
                                global_radius,
                                arc_index,
                                arc_subindex,
                                arc_subdivision_count,
                            )
                            bounds = principal_minor_bounds(
                                module,
                                configuration,
                                cell,
                                path_segment,
                                module.cbox(
                                    local_x_lower, local_x_upper
                                ),
                                module.cbox(
                                    local_t_lower, local_t_upper
                                ),
                                local_epsilon,
                                displacement,
                            )
                            transformed = {
                                "j11": added_intervals(
                                    scaled_interval(
                                        bounds["j11"], univalence_direction[0]
                                    ),
                                    scaled_interval(
                                        bounds["j21"], univalence_direction[1]
                                    ),
                                ),
                                "j22": added_intervals(
                                    scaled_interval(
                                        bounds["j12"], univalence_direction[0]
                                    ),
                                    scaled_interval(
                                        bounds["j22"], univalence_direction[1]
                                    ),
                                ),
                                "j12": bounds["j12"],
                                "j21": bounds["j21"],
                            }
                            transformed["determinant"] = scaled_interval(
                                bounds["determinant"],
                                preconditioner_determinant,
                            )
                            row = {
                                "x_subdivision_count": x_count,
                                "t_subdivision_count": t_count,
                                "epsilon_real_subdivision_count": (
                                    epsilon_real_count
                                ),
                                "arc_subdivision_count": (
                                    arc_subdivision_count
                                ),
                                "x_index": x_index,
                                "t_index": t_index,
                                "epsilon_real_index": epsilon_real_index,
                                "arc_index": arc_index,
                                "arc_subindex": arc_subindex,
                                "x_lower": local_x_lower,
                                "x_upper": local_x_upper,
                                "t_lower": local_t_lower,
                                "t_upper": local_t_upper,
                                "epsilon_real_lower": epsilon_real_lower,
                                "epsilon_real_upper": epsilon_real_upper,
                            }
                            for name, interval in transformed.items():
                                row[f"{name}_lower"] = interval[0]
                                row[f"{name}_upper"] = interval[1]
                                row[f"{name}_sign"] = interval_sign(
                                    interval
                                )
                                row[f"{name}_abs_lower"] = (
                                    minimum_abs_lower(interval)
                                )
                            local_rows.append(row)
        leaf_rows.extend(local_rows)
        j11_signs = {int(row["j11_sign"]) for row in local_rows}
        j22_signs = {int(row["j22_sign"]) for row in local_rows}
        determinant_signs = {
            int(row["determinant_sign"]) for row in local_rows
        }
        passed = (
            len(j11_signs) == 1
            and 0 not in j11_signs
            and len(j22_signs) == 1
            and 0 not in j22_signs
            and len(determinant_signs) == 1
            and 0 not in determinant_signs
        )
        scheme_rows.append(
            {
                "x_subdivision_count": x_count,
                "t_subdivision_count": t_count,
                "epsilon_real_subdivision_count": epsilon_real_count,
                "arc_subdivision_count": arc_subdivision_count,
                "leaf_count": len(local_rows),
                "j11_signs": "|".join(
                    str(value) for value in sorted(j11_signs)
                ),
                "j22_signs": "|".join(
                    str(value) for value in sorted(j22_signs)
                ),
                "determinant_signs": "|".join(
                    str(value) for value in sorted(determinant_signs)
                ),
                "minimum_j11_abs_lower": min(
                    float(row["j11_abs_lower"]) for row in local_rows
                ),
                "minimum_j22_abs_lower": min(
                    float(row["j22_abs_lower"]) for row in local_rows
                ),
                "minimum_determinant_abs_lower": min(
                    float(row["determinant_abs_lower"])
                    for row in local_rows
                ),
                "gale_nikaido_principal_minor_cover_passed": passed,
                "runtime_seconds": time.time() - started,
            }
        )
        if passed:
            break

    selected = next(
        (
            row
            for row in scheme_rows
            if row["gale_nikaido_principal_minor_cover_passed"]
        ),
        None,
    )
    payload = {
        "checkpoint": 5396,
        "primary_revision": module.REVISION,
        "theorem": (
            "GALE_NIKAIDO_1965_THEOREM_8II_2D_ONE_SIGNED_OUTPUT_DIRECTION"
        ),
        "theorem_doi": "10.1007/BF01360282",
        "frontier": {
            "mapped_cell_id": mapped_cell_id,
            "term_id": term_id,
            "path_segment": path_segment,
            "x_lower": x_lower,
            "x_upper": x_upper,
            "t_lower": t_lower,
            "t_upper": t_upper,
            "refinement_depth": depth,
            "refinement_path": refinement_path,
            "source": frontier_source,
        },
        "global_radius": global_radius,
        "fixed_output_preconditioner": preconditioner,
        "fixed_output_preconditioner_determinant": (
            preconditioner_determinant
        ),
        "fixed_univalence_direction": univalence_direction,
        "schemes": scheme_rows,
        "selected_scheme": selected,
        "global_univalence_proved": selected is not None,
        "claim_boundary": (
            "This proves injectivity only for the audited external01 path map "
            "on the stated closed frontier box, uniformly over the saved "
            "regulator slab and closed contour-subarc cover."
        ),
    }
    frontier_id = f"d{int(depth):02d}_{refinement_path or 'ROOT'}"
    frontier_scope = f"{mapped_cell_id}_{path_segment}"
    artifact_id = f"{frontier_scope}_{frontier_id}"
    payload["artifact_prefix"] = (
        f"external01_frontier_gale_nikaido_{artifact_id}"
    )
    module.atomic_csv(
        OUTPUT
        / f"external01_frontier_gale_nikaido_{artifact_id}_leaf_audit.csv",
        leaf_rows,
    )
    module.atomic_csv(
        OUTPUT
        / f"external01_frontier_gale_nikaido_{artifact_id}_scheme_audit.csv",
        scheme_rows,
    )
    module.atomic_json(
        OUTPUT / f"external01_frontier_gale_nikaido_{artifact_id}_result.json",
        payload,
    )
    if frontier_source != "explicit_cli":
        module.atomic_csv(
            OUTPUT / "external01_frontier_gale_nikaido_leaf_audit.csv",
            leaf_rows,
        )
        module.atomic_csv(
            OUTPUT / "external01_frontier_gale_nikaido_scheme_audit.csv",
            scheme_rows,
        )
        module.atomic_json(
            OUTPUT / "external01_frontier_gale_nikaido_audit_result.json",
            payload,
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapped-cell-id", default="S_X002_MC04_SP_DM")
    parser.add_argument("--term-id", default="MC04_SP_DM")
    parser.add_argument("--path-segment", default="RIGHT_CONNECTOR")
    parser.add_argument("--stack-index", type=int, default=-1)
    parser.add_argument("--x-lower", type=float)
    parser.add_argument("--x-upper", type=float)
    parser.add_argument("--t-lower", type=float)
    parser.add_argument("--t-upper", type=float)
    parser.add_argument("--refinement-depth", type=int)
    parser.add_argument("--refinement-path")
    print(json.dumps(run_audit(parser.parse_args()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
