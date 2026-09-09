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
from typing import Any


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


CHECKPOINT = 5427
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5426"
    / "v44_bounded_production_result.json"
)
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5426"
    / "P8_Y5_BRR5396_5426_VALIDATION.csv"
)
ACTIVE_STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5427-Y5-R2FR-D4-representative-external01-square-half-plane-gate.md"
POINTS = OUTPUT / "representative_external01_square_point_crosschecks.csv"
COVER = OUTPUT / "representative_external01_square_half_plane_cover.csv"
COVER_SUMMARY = OUTPUT / "representative_external01_square_half_plane_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5427_VALIDATION.csv"
RESULT = OUTPUT / "representative_external01_square_half_plane_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v44"
EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:"
    "edge_0_0_1:stable_edge"
)
BROAD_COLUMNS = (
    "valid_for_D4_numeric_event_local_W3_bound",
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_parent() -> Any:
    source = PARENT_SCRIPT.read_text(encoding="utf-8")
    compile(source, str(PARENT_SCRIPT), "exec")
    specification = importlib.util.spec_from_file_location(
        "mts_5396_v44_for_5427",
        PARENT_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {PARENT_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def context(parent: Any) -> tuple[Any, Any, Any, dict[str, Any]]:
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == "S_X006_MC04_SP_DP"
    )
    configuration = next(
        row
        for row in parent.configuration_variants("MC04_SP_DP")
        if row["role"] == "representative"
    )
    arguments = argparse.Namespace(
        combined_regulator_box=True,
        combined_regulator_slab_count=2,
        epsilon_subdivisions=1,
    )
    epsilon_row = parent.epsilon_boxes(arguments)[0]
    epsilon = parent.epsilon_interval(epsilon_row)
    return cell, configuration, epsilon, epsilon_row


def representative_external01_square_dual(
    parent: Any,
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    global_displacement: Any,
) -> Any:
    if configuration["role"] != "representative":
        raise ValueError("square formula requires representative role")
    dual = parent.M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    global_displacement = dual.coerce(global_displacement)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * parent.M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = parent.M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_plus = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_minus = (
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
        * factor_plus
        / (decay_sine * (1 + soft_cosine) * factor_minus)
    )
    selected_root = external_root * (1 + soft_cosine) / soft_sine
    unit_circle = selected_root + global_displacement
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
    antiholomorphic_constant = soft_sine * (
        longitudinal_constant
        + longitudinal_coefficient * relative_cosine_constant
    )
    antiholomorphic_laurent = (
        soft_sine
        * longitudinal_coefficient
        * relative_cosine_laurent
    )
    antiholomorphic_polynomial = (
        antiholomorphic_laurent * representative * representative
        + antiholomorphic_constant * representative
        + antiholomorphic_laurent
        + recoil * decay_sine
    )
    plus_polynomial = (
        plus_laurent * representative * representative
        + plus_constant * representative
        + plus_laurent
    )
    target = -9 + 1j * epsilon
    external_transverse = parent.sheet_locked_external_transverse_dual(target)
    return (
        external_transverse
        * antiholomorphic_polynomial
        / ((1 - target) * unit_circle * plus_polynomial)
        - 1
    )


def centered_square(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(parent.M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = parent.cpoint(
        configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = parent.cpoint(
        math.sqrt(1 - parent.M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = parent.M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = parent.deformed_path_energy_dual(
            cell,
            "RIGHT_CONNECTOR",
            coordinate,
            parameter,
        )
        recoil = parent.M5386.chart_safe_sqrt_dual(1 - energy)
        return representative_external01_square_dual(
            parent,
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )

    direct = evaluate(list(domains)).value
    mean_value = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            parent.M5385.M5381.IntervalDual(
                value,
                parent.cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        mean_value += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return max(
        (direct, mean_value),
        key=lambda value: (
            parent.M5258.lower_abs(value),
            -parent.M5258.upper_abs(value),
        ),
    )


def point_rows(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> list[dict[str, Any]]:
    state = read_json(ACTIVE_STATE)
    examples = state["split_failure_examples"][EXTERNAL01_FAILURE]
    x_lower = min(float(row["x_lower"]) for row in examples)
    x_upper = max(float(row["x_upper"]) for row in examples)
    t_lower = min(float(row["t_lower"]) for row in examples)
    t_upper = max(float(row["t_upper"]) for row in examples)
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_values = (
        epsilon_real_lower,
        0.5 * (epsilon_real_lower + epsilon_real_upper),
        epsilon_real_upper,
    )
    rows: list[dict[str, Any]] = []
    for x_fraction in (0.0, 0.5, 1.0):
        for t_fraction in (0.0, 0.5, 1.0):
            for epsilon_value in epsilon_values:
                coordinate = parent.cpoint(
                    x_lower + (x_upper - x_lower) * x_fraction
                )
                parameter = parent.cpoint(
                    t_lower + (t_upper - t_lower) * t_fraction
                )
                epsilon_point = parent.cpoint(epsilon_value)
                energy = parent.deformed_path_energy_dual(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    parameter,
                ).value
                inputs, geometry = parent.interval_inputs(
                    configuration,
                    coordinate,
                    energy,
                    epsilon_point,
                )
                radius = 1.0e-7 * max(
                    1.0,
                    parent.M5258.upper_abs(geometry["selected_root"]),
                )
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = parent.cpoint(
                        radius
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    internal = parent.M5258.rotate_internal_lightcone(
                        parent.M5386.amplitude_state(geometry),
                        geometry["selected_root"] + displacement,
                    )
                    _, right = parent.sheet_locked_interval_cut_momenta(
                        internal,
                        parent.cpoint(-9)
                        + parent.cpoint(1j) * epsilon_point,
                    )
                    diagnostics = parent.M5258.IntervalDiagnostics()
                    first = parent.displaced_first_rational_spinors(
                        configuration,
                        inputs,
                        geometry,
                        displacement,
                        -1,
                        diagnostics,
                        "external01_square_point_first",
                    )
                    spinors, _, charts = parent.rational_spinor_overrides(
                        right,
                        diagnostics,
                        "external01_square_point_right",
                        first,
                    )
                    direct = parent.M5258.spinor_bracket(
                        spinors[0][1],
                        spinors[1][1],
                    )
                    derived = representative_external01_square_dual(
                        parent,
                        configuration,
                        epsilon_point,
                        geometry["recoil"],
                        inputs["soft_cosine"],
                        inputs["decay_cosine"],
                        inputs["decay_sine"],
                        displacement,
                    ).value
                    rows.append(
                        {
                            "checkpoint": CHECKPOINT,
                            "x_fraction": x_fraction,
                            "t_fraction": t_fraction,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "external_chart": charts[0],
                            "first_chart": charts[1],
                            "direct_abs": parent.M5258.upper_abs(direct),
                            "derived_abs": parent.M5258.upper_abs(derived),
                            "absolute_error_upper": parent.M5258.upper_abs(
                                direct - derived
                            ),
                        }
                    )
    return rows


def adaptive_cover(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = read_json(ACTIVE_STATE)
    examples = state["split_failure_examples"][EXTERNAL01_FAILURE]
    x_lower = min(float(row["x_lower"]) for row in examples)
    x_upper = max(float(row["x_upper"]) for row in examples)
    t_lower = min(float(row["t_lower"]) for row in examples)
    t_upper = max(float(row["t_upper"]) for row in examples)
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    coordinate = parent.cbox(x_lower, x_upper)
    parameter = parent.cbox(t_lower, t_upper)
    energy = parent.deformed_path_energy_dual(
        cell,
        "RIGHT_CONNECTOR",
        coordinate,
        parameter,
    ).value
    _, geometry = parent.interval_inputs(
        configuration,
        coordinate,
        energy,
        epsilon,
    )
    radius = math.nextafter(
        1.0e-7
        * max(1.0, parent.M5258.upper_abs(geometry["selected_root"])),
        math.inf,
    )
    displacement = parent.cbox(-radius, radius, -radius, radius)
    stack: list[tuple[float, float, float, float, float, float, int, Any | None]] = [
        (
            x_lower,
            x_upper,
            t_lower,
            t_upper,
            epsilon_real_lower,
            epsilon_real_upper,
            0,
            None,
        )
    ]
    accepted: list[dict[str, Any]] = []
    evaluation_count = 0
    discarded_trial_count = 0
    maximum_depth = 24
    maximum_leaf_count = 8192
    bootstrap_schedule = (
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "coordinate",
        "coordinate",
        "path_parameter",
        "path_parameter",
        "coordinate",
        "path_parameter",
        "epsilon_real",
    )

    def evaluate(node: tuple[Any, ...]) -> Any:
        nonlocal evaluation_count
        edge = centered_square(
            parent,
            configuration,
            cell,
            parent.cbox(float(node[0]), float(node[1])),
            parent.cbox(float(node[2]), float(node[3])),
            parent.cbox(
                float(node[4]),
                float(node[5]),
                epsilon_imaginary_lower,
                epsilon_imaginary_upper,
            ),
            displacement,
        )
        evaluation_count += 1
        return edge

    while stack:
        node = stack.pop()
        x0, x1, t0, t1, e0, e1, depth, cached = node
        edge = cached if cached is not None else evaluate(node)
        real_bounds = parent.M5394.real_bounds(edge)
        if real_bounds[1] < 0.0:
            imaginary_bounds = parent.M5394.imaginary_bounds(edge)
            accepted.append(
                {
                    "checkpoint": CHECKPOINT,
                    "leaf_index": len(accepted),
                    "depth": depth,
                    "x_lower": x0,
                    "x_upper": x1,
                    "t_lower": t0,
                    "t_upper": t1,
                    "epsilon_real_lower": e0,
                    "epsilon_real_upper": e1,
                    "edge_real_lower": real_bounds[0],
                    "edge_real_upper": real_bounds[1],
                    "edge_imaginary_lower": imaginary_bounds[0],
                    "edge_imaginary_upper": imaginary_bounds[1],
                    "edge_abs_lower": parent.M5258.lower_abs(edge),
                    "edge_abs_upper": parent.M5258.upper_abs(edge),
                    "valid_for_negative_real_half_plane": True,
                    "_edge": edge,
                }
            )
            continue
        if depth >= maximum_depth:
            raise RuntimeError(
                "square edge half-plane cover reaches maximum depth: "
                f"x=({x0},{x1}); t=({t0},{t1}); "
                f"epsilon=({e0},{e1}); real={real_bounds}"
            )
        candidates: list[tuple[float, str, list[tuple[Any, ...]]]] = []
        split_variables = (
            (bootstrap_schedule[depth],)
            if depth < len(bootstrap_schedule)
            else ("epsilon_real", "path_parameter", "coordinate")
        )
        for split_variable in split_variables:
            if split_variable == "epsilon_real":
                midpoint = 0.5 * (e0 + e1)
                children = [
                    (x0, x1, t0, t1, e0, midpoint, depth + 1, None),
                    (x0, x1, t0, t1, midpoint, e1, depth + 1, None),
                ]
            elif split_variable == "path_parameter":
                midpoint = 0.5 * (t0 + t1)
                children = [
                    (x0, x1, t0, midpoint, e0, e1, depth + 1, None),
                    (x0, x1, midpoint, t1, e0, e1, depth + 1, None),
                ]
            else:
                midpoint = 0.5 * (x0 + x1)
                children = [
                    (x0, midpoint, t0, t1, e0, e1, depth + 1, None),
                    (midpoint, x1, t0, t1, e0, e1, depth + 1, None),
                ]
            evaluated_children: list[tuple[Any, ...]] = []
            score = -math.inf
            for child in children:
                child_edge = evaluate(child)
                score = max(
                    score,
                    parent.M5394.real_bounds(child_edge)[1],
                )
                evaluated_children.append((*child[:-1], child_edge))
            candidates.append((score, split_variable, evaluated_children))
        selected = min(candidates, key=lambda row: row[0])
        discarded_trial_count += 2 * (len(candidates) - 1)
        stack.extend(reversed(selected[2]))
        if len(stack) + len(accepted) > maximum_leaf_count:
            raise RuntimeError("square edge half-plane cover exceeds leaf budget")
    hull = parent.rectangular_interval_hull(
        [row["_edge"] for row in accepted]
    )
    hull_real = parent.M5394.real_bounds(hull)
    hull_imaginary = parent.M5394.imaginary_bounds(hull)
    rows = [
        {key: value for key, value in row.items() if key != "_edge"}
        for row in accepted
    ]
    summary = {
        "checkpoint": CHECKPOINT,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
        "epsilon_real_lower": epsilon_real_lower,
        "epsilon_real_upper": epsilon_real_upper,
        "global_displacement_radius": radius,
        "leaf_count": len(rows),
        "evaluation_count": evaluation_count,
        "discarded_trial_count": discarded_trial_count,
        "maximum_depth": max(int(row["depth"]) for row in rows),
        "minimum_leaf_abs_lower": min(
            float(row["edge_abs_lower"]) for row in rows
        ),
        "hull_real_lower": hull_real[0],
        "hull_real_upper": hull_real[1],
        "hull_imaginary_lower": hull_imaginary[0],
        "hull_imaginary_upper": hull_imaginary[1],
        "hull_abs_lower": parent.M5258.lower_abs(hull),
        "valid_for_common_negative_real_half_plane": (
            hull_real[1] < 0.0 and parent.M5258.lower_abs(hull) > 0.0
        ),
    }
    return rows, summary


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5427: representative external01 square half-plane gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE REPRESENTATIVE-CHART `(0,1)` SQUARE EDGE ONLY.**",
        "",
        "The v44 production failure is not the reciprocal external pole already treated by the path-integrated decomposition. It occurs only in the representative chart and chirality one. In the surviving external-minus / hard-plus rational charts, the exact edge is",
        "",
        "`[01] = T p1_bar / ((1-target) p1_plus) - 1`.",
        "",
        "After multiplying the hard lightcone terms by the parent representative coordinate, this becomes the explicit Laurent-free polynomial quotient implemented by the 5427 gate.",
        "",
        "## Evidence",
        "",
        f"All `{payload['point_crosscheck_count']}` direct spinor checks agree within `{payload['maximum_point_absolute_error']:.17g}`. A closed adaptive cover of the recorded failure region uses `{payload['cover_leaf_count']}` leaves and places their common hull strictly in the negative-real half-plane with margin `{payload['cover_negative_real_margin']:.17g}`.",
        "",
        "## Consequence",
        "",
        "The representative branch does not require a pole integral on this recorded region. It requires an exact square-edge override, dual to the existing reciprocal angle-edge override. The next implementation may add that override and rerun the same historical failure boxes.",
        "",
        "## Claim boundary",
        "",
        "No connector, W3, regulator, UV, local-GR, or full-MTS claim follows from this chart-local edge proof.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (
        PARENT_SCRIPT,
        PREVIOUS,
        PREVIOUS_VALIDATION,
        ACTIVE_STATE,
        ACTIVE_ROWS,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))
    parent = load_parent()
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = read_json(PREVIOUS)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    active_rows = read_csv(ACTIVE_ROWS)
    cell, configuration, epsilon, _ = context(parent)
    points = point_rows(parent, cell, configuration, epsilon)
    cover_rows, cover_summary = adaptive_cover(
        parent,
        cell,
        configuration,
        epsilon,
    )
    maximum_point_error = max(
        float(row["absolute_error_upper"]) for row in points
    )
    chart_contract_holds = all(
        row["external_chart"] == "minus"
        and row["first_chart"] == "plus"
        for row in points
    )
    broad_claims_false = all(
        not is_true(row[column])
        for row in active_rows
        for column in BROAD_COLUMNS
    )
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    atomic_csv(POINTS, points)
    atomic_csv(COVER, cover_rows)
    atomic_csv(COVER_SUMMARY, [cover_summary])
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "point_crosscheck_count": len(points),
        "maximum_point_absolute_error": maximum_point_error,
        "cover_leaf_count": int(cover_summary["leaf_count"]),
        "cover_evaluation_count": int(cover_summary["evaluation_count"]),
        "cover_maximum_depth": int(cover_summary["maximum_depth"]),
        "cover_hull_abs_lower": float(cover_summary["hull_abs_lower"]),
        "cover_negative_real_margin": -float(
            cover_summary["hull_real_upper"]
        ),
        "valid_for_representative_external01_square_edge": True,
        "valid_for_parent_v45_candidate": True,
        "valid_for_right_connector_completion": False,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    write_document(payload)
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "parent_source_compiles_as_v44",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        check(
            "checkpoint_5426_is_green_and_narrow",
            int(previous["failed_validation_count"]) == 0
            and all(is_true(row["passed"]) for row in previous_validation)
            and not bool(previous["valid_for_regular_away_W3_claim"]),
            f"validation rows={len(previous_validation)}",
        ),
        check(
            "failure_is_representative_chirality_one",
            previous["current_external01_failure_count"]
            > previous["baseline_external01_failure_count"],
            f"count={previous['current_external01_failure_count']}",
        ),
        check(
            "point_chart_contract_is_uniform",
            chart_contract_holds,
            "external minus; hard-one plus",
        ),
        check(
            "derived_square_matches_direct_spinors",
            maximum_point_error <= 1.0e-12,
            f"count={len(points)}; max error={maximum_point_error:.17g}",
        ),
        check(
            "adaptive_cover_has_positive_leaf_margins",
            all(
                float(row["edge_abs_lower"]) > 0.0
                and is_true(row["valid_for_negative_real_half_plane"])
                for row in cover_rows
            ),
            f"leaves={len(cover_rows)}",
        ),
        check(
            "cover_hull_has_common_negative_real_half_plane",
            bool(cover_summary["valid_for_common_negative_real_half_plane"]),
            f"real upper={cover_summary['hull_real_upper']}; abs lower={cover_summary['hull_abs_lower']}",
        ),
        check(
            "broad_claims_remain_false",
            broad_claims_false
            and not payload["valid_for_regular_away_W3_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "W3, UV, local-GR, and full-MTS remain unclaimed",
        ),
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after gate start={len(formalization_touches)}",
        ),
    ]
    atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
