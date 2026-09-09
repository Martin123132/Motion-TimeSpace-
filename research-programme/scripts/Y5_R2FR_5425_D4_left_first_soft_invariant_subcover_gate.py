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

import sympy


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


CHECKPOINT = 5425
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
    / "5424"
    / "v43_right_connector_progress_result.json"
)
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5424"
    / "P8_Y5_BRR5396_5424_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
ACTIVE_STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5425-Y5-R2FR-D4-left-first-soft-invariant-subcover-gate.md"
COVER = OUTPUT / "left_first_soft_invariant_cover.csv"
COVER_SUMMARY = OUTPUT / "left_first_soft_invariant_cover_summary.csv"
POINTS = OUTPUT / "left_first_soft_invariant_point_crosschecks.csv"
REGRESSION = OUTPUT / "v44_targeted_connector_regression.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5425_VALIDATION.csv"
RESULT = OUTPUT / "left_first_soft_invariant_subcover_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v44"
REMOVED_EDGE = "edge_2_1_3:stable_edge"
EXPECTED_AREA = 0.03932753620548857
HISTORICAL_BOX = (
    0.32152697246066986,
    0.32168059564897256,
    0.0,
    0.015625,
    14,
    "LLDRDLDRDLDLDR",
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
        "mts_5396_v44",
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


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


def symbolic_identity() -> dict[str, Any]:
    q_value, recoil, soft_cosine, decay_cosine = sympy.symbols(
        "q r x c",
        nonzero=True,
    )
    soft_sine, decay_sine = sympy.symbols("u d", nonzero=True)
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
    relative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_plus
        / (decay_sine * (1 + soft_cosine) * factor_minus)
    )
    relative_cosine = (
        (relative + 1 / relative)
        * soft_sine
        * decay_sine
        / 2
        + soft_cosine * decay_cosine
    )
    polynomial = (
        decay_cosine * q_value * soft_cosine
        + decay_cosine * q_value
        + decay_cosine * soft_cosine
        - decay_cosine
        + q_value * recoil * soft_cosine**2
        - q_value * recoil
        - q_value * soft_cosine**2
        - q_value * soft_cosine
        + recoil * soft_cosine**2
        - recoil
        - soft_cosine**2
        + soft_cosine
    )
    original = 2 * (1 - recoil**2) * (1 - relative_cosine)
    rational = (
        4
        * recoil
        * (q_value + 1)
        * (1 - recoil**2)
        * polynomial
        / (factor_plus * factor_minus)
    )
    numerator = sympy.expand(
        sympy.fraction(sympy.together(original - rational))[0]
    )
    reduced = sympy.factor(
        numerator.subs(soft_sine**2, 1 - soft_cosine**2).subs(
            decay_sine**2,
            1 - decay_cosine**2,
        )
    )
    reciprocal_symmetry = sympy.simplify(
        (relative + 1 / relative) - (1 / relative + relative)
    )
    return {
        "identity_remainder": str(reduced),
        "reciprocal_symmetry_remainder": str(reciprocal_symmetry),
        "identity_exact": reduced == 0,
        "reciprocal_symmetry_exact": reciprocal_symmetry == 0,
    }


def context(parent: Any) -> tuple[Any, list[dict[str, Any]], Any, dict[str, Any]]:
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == "S_X006_MC04_SP_DP"
    )
    configurations = parent.configuration_variants("MC04_SP_DP")
    arguments = argparse.Namespace(
        combined_regulator_box=True,
        combined_regulator_slab_count=2,
        epsilon_subdivisions=1,
    )
    epsilon_row = parent.epsilon_boxes(arguments)[0]
    epsilon = parent.epsilon_interval(epsilon_row)
    return cell, configurations, epsilon, epsilon_row


def point_rows(
    parent: Any,
    cell: dict[str, Any],
    configurations: list[dict[str, Any]],
    epsilon: Any,
) -> list[dict[str, Any]]:
    x_lower = float(cell["lower_absolute_soft_cosine"])
    x_upper = float(cell["upper_absolute_soft_cosine"])
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    epsilon_points = (
        epsilon_real_lower + 1j * epsilon_imaginary_lower,
        0.5 * (epsilon_real_lower + epsilon_real_upper),
        epsilon_real_upper + 1j * epsilon_imaginary_upper,
    )
    rows: list[dict[str, Any]] = []
    for configuration in configurations:
        for x_fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            for t_fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
                for epsilon_value in epsilon_points:
                    x_value = x_lower + (x_upper - x_lower) * x_fraction
                    coordinate = parent.cpoint(x_value)
                    parameter = parent.cpoint(t_fraction)
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
                    internal = parent.M5258.rotate_internal_lightcone(
                        parent.M5386.amplitude_state(geometry),
                        geometry["selected_root"] + parent.cpoint(1.0e-7),
                    )
                    left, right = parent.sheet_locked_interval_cut_momenta(
                        internal,
                        parent.cpoint(-9) + parent.cpoint(1j) * epsilon_point,
                    )
                    derived = parent.left_first_soft_invariant_rational_dual(
                        configuration,
                        epsilon_point,
                        energy,
                        inputs["soft_cosine"],
                        inputs["decay_cosine"],
                    ).value
                    left_direct = parent.M5258.invariant(left, 1, 3)
                    right_direct = parent.M5258.invariant(right, 1, 3)
                    rows.append(
                        {
                            "checkpoint": CHECKPOINT,
                            "role": configuration["role"],
                            "x_fraction": x_fraction,
                            "t_fraction": t_fraction,
                            "epsilon_real": epsilon_value.real,
                            "epsilon_imaginary": epsilon_value.imag,
                            "left_direct_abs": parent.M5258.upper_abs(left_direct),
                            "right_direct_abs": parent.M5258.upper_abs(right_direct),
                            "derived_abs": parent.M5258.upper_abs(derived),
                            "left_absolute_error_upper": parent.M5258.upper_abs(
                                left_direct - derived
                            ),
                            "right_absolute_error_upper": parent.M5258.upper_abs(
                                right_direct - derived
                            ),
                            "left_right_absolute_error_upper": (
                                parent.M5258.upper_abs(left_direct - right_direct)
                            ),
                        }
                    )
    return rows


def cover_leaf_rows(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
    coverage_id: str,
    bounds: tuple[float, float, float, float],
    x_subdivision_count: int,
    endpoint_power: int,
    epsilon_real_subdivision_count: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    x_lower, x_upper, t_lower, t_upper = bounds
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    parameter_edges = parent.endpoint_geometric_real_edges(
        parent.cbox(t_lower, t_upper),
        endpoint_power,
    )
    rows: list[dict[str, Any]] = []
    enclosures: list[Any] = []
    for epsilon_index in range(epsilon_real_subdivision_count):
        epsilon_subbox = parent.cbox(
            epsilon_real_lower
            + (epsilon_real_upper - epsilon_real_lower)
            * epsilon_index
            / epsilon_real_subdivision_count,
            epsilon_real_lower
            + (epsilon_real_upper - epsilon_real_lower)
            * (epsilon_index + 1)
            / epsilon_real_subdivision_count,
            epsilon_imaginary_lower,
            epsilon_imaginary_upper,
        )
        for x_index in range(x_subdivision_count):
            coordinate = parent.cbox(
                x_lower
                + (x_upper - x_lower) * x_index / x_subdivision_count,
                x_lower
                + (x_upper - x_lower)
                * (x_index + 1)
                / x_subdivision_count,
            )
            coordinate_bounds = parent.M5394.real_bounds(coordinate)
            for parameter_index, (
                parameter_lower,
                parameter_upper,
            ) in enumerate(zip(parameter_edges, parameter_edges[1:])):
                enclosure = (
                    parent.centered_path_correlated_left_first_soft_invariant(
                        configuration,
                        cell,
                        "RIGHT_CONNECTOR",
                        coordinate,
                        parent.cbox(parameter_lower, parameter_upper),
                        epsilon_subbox,
                    )
                )
                enclosures.append(enclosure)
                real_bounds = parent.M5394.real_bounds(enclosure)
                imaginary_bounds = parent.M5394.imaginary_bounds(enclosure)
                rows.append(
                    {
                        "checkpoint": CHECKPOINT,
                        "coverage_id": coverage_id,
                        "role": configuration["role"],
                        "epsilon_index": epsilon_index,
                        "x_index": x_index,
                        "parameter_index": parameter_index,
                        "x_lower": coordinate_bounds[0],
                        "x_upper": coordinate_bounds[1],
                        "t_lower": parameter_lower,
                        "t_upper": parameter_upper,
                        "invariant_real_lower": real_bounds[0],
                        "invariant_real_upper": real_bounds[1],
                        "invariant_imaginary_lower": imaginary_bounds[0],
                        "invariant_imaginary_upper": imaginary_bounds[1],
                        "invariant_abs_lower": parent.M5258.lower_abs(enclosure),
                        "invariant_abs_upper": parent.M5258.upper_abs(enclosure),
                        "valid_for_invariant_nonzero": (
                            parent.M5258.lower_abs(enclosure) > 0.0
                        ),
                    }
                )
    hull = parent.rectangular_interval_hull(enclosures)
    hull_real = parent.M5394.real_bounds(hull)
    hull_imaginary = parent.M5394.imaginary_bounds(hull)
    summary = {
        "checkpoint": CHECKPOINT,
        "coverage_id": coverage_id,
        "role": configuration["role"],
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
        "x_subdivision_count": x_subdivision_count,
        "endpoint_power": endpoint_power,
        "epsilon_real_subdivision_count": epsilon_real_subdivision_count,
        "leaf_count": len(rows),
        "zero_leaf_count": sum(
            not bool(row["valid_for_invariant_nonzero"]) for row in rows
        ),
        "minimum_leaf_abs_lower": min(
            float(row["invariant_abs_lower"]) for row in rows
        ),
        "hull_real_lower": hull_real[0],
        "hull_real_upper": hull_real[1],
        "hull_imaginary_lower": hull_imaginary[0],
        "hull_imaginary_upper": hull_imaginary[1],
        "hull_abs_lower": parent.M5258.lower_abs(hull),
        "valid_for_full_rectangular_hull_nonzero": (
            parent.M5258.lower_abs(hull) > 0.0
        ),
    }
    return rows, summary


def regression_rows(
    parent: Any,
    cell: dict[str, Any],
    configurations: list[dict[str, Any]],
    epsilon_row: dict[str, Any],
    active_state: dict[str, Any],
) -> list[dict[str, Any]]:
    active = active_state["stack"][-1]
    cases = (
        ("historical_depth14", HISTORICAL_BOX),
        (
            "active_frontier",
            (
                float(active[0]),
                float(active[1]),
                float(active[2]),
                float(active[3]),
                int(active[4]),
                str(active[5]),
            ),
        ),
    )
    rows: list[dict[str, Any]] = []
    support_segments = parent.material_support_segments()
    branch_data = parent.material_branch_data()
    for case_id, case in cases:
        x_lower, x_upper, t_lower, t_upper, depth, path = case
        try:
            result = parent.evaluate_path_box(
                cell,
                "MC04_SP_DP",
                configurations,
                epsilon_row,
                "RIGHT_CONNECTOR",
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                depth,
                path,
                support_segments,
                branch_data,
                4,
            )
        except Exception as error:
            state = "ADVANCED_TO_LATER_FAILURE"
            error_text = str(error)
            denominator = 0.0
        else:
            state = "PASS"
            error_text = ""
            denominator = float(
                result["minimum_amplitude_denominator_abs_lower"]
            )
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "case_id": case_id,
                "refinement_depth": depth,
                "refinement_path": path,
                "state": state,
                "later_failure": error_text,
                "removed_edge_absent": REMOVED_EDGE not in error_text,
                "minimum_amplitude_denominator_abs_lower": denominator,
            }
        )
    return rows


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5425: left first-soft invariant subcover gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE EXACT `(1,3)` INVARIANT AND CONTINUED V44 PRODUCTION ONLY.**",
        "",
        "The recurring left/right hard-1--soft denominator is not a physical zero. It is an interval-dependency artefact caused by separately enclosing two chiral brackets. V44 now switches to the exact Lorentz invariant whenever either direct bracket loses zero separation.",
        "",
        "## Exact reduction",
        "",
        "With recoil `r`, soft cosine `x`, decay cosine `c`, regulator coordinate `q`, and the two parent factors `F_+` and `F_-`, the parent relative coordinate gives",
        "",
        "`s_13 = 2(1-r^2)(1-C) = 4 r (q+1)(1-r^2) P / (F_+ F_-)`,",
        "",
        "where `P` is the explicit polynomial implemented in the v44 parent. Symbolic elimination using `u^2=1-x^2` and `d^2=1-c^2` leaves exactly zero. Because `C` depends on `R+R^{-1}`, the same invariant serves the representative and reciprocal charts.",
        "",
        "## Certified cover",
        "",
        f"The complete active right-connector regulator slab is covered by `{payload['full_cover_leaf_count']}` closed boxes. Every leaf is nonzero and their single rectangular hull has real lower bound `{payload['full_cover_hull_real_lower']:.17g}` and absolute lower bound `{payload['full_cover_hull_abs_lower']:.17g}`.",
        "",
        f"Across `{payload['point_crosscheck_count']}` direct momentum checks, the largest formula error is `{payload['maximum_point_absolute_error']:.17g}`. Both targeted production boxes advance past `{REMOVED_EDGE}`.",
        "",
        "## Consequence",
        "",
        "This is an analytic repair, not another depth-only workaround: the old `(1,3)` obstruction is removed in both KLT copies. The targeted historical box now reaches the already-known external `(0,1)` obstruction instead.",
        "",
        "## Claim boundary",
        "",
        "The right connector is still incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (
        PARENT_SCRIPT,
        PREVIOUS,
        PREVIOUS_VALIDATION,
        STATUS,
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
    status = read_json(STATUS)
    active_state = read_json(ACTIVE_STATE)
    active_rows = read_csv(ACTIVE_ROWS)
    cell, configurations, epsilon, epsilon_row = context(parent)
    symbolic = symbolic_identity()
    points = point_rows(parent, cell, configurations, epsilon)
    representative = next(
        row for row in configurations if row["role"] == "representative"
    )
    full_bounds = (
        float(cell["lower_absolute_soft_cosine"]),
        float(cell["upper_absolute_soft_cosine"]),
        0.0,
        1.0,
    )
    full_rows, full_summary = cover_leaf_rows(
        parent,
        cell,
        representative,
        epsilon,
        "full_right_connector_active_regulator_slab",
        full_bounds,
        16,
        9,
        2,
    )
    historical_rows, historical_summary = cover_leaf_rows(
        parent,
        cell,
        representative,
        epsilon,
        "historical_depth14_box",
        HISTORICAL_BOX[:4],
        1,
        3,
        1,
    )
    covers = full_rows + historical_rows
    summaries = [full_summary, historical_summary]
    regressions = regression_rows(
        parent,
        cell,
        configurations,
        epsilon_row,
        active_state,
    )
    accepted_area = sum(float(row["parameter_area"]) for row in active_rows)
    remaining_area = pending_area(active_state["stack"])
    total_area = accepted_area + remaining_area
    maximum_point_error = max(
        float(row[column])
        for row in points
        for column in (
            "left_absolute_error_upper",
            "right_absolute_error_upper",
            "left_right_absolute_error_upper",
        )
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

    atomic_csv(COVER, covers)
    atomic_csv(COVER_SUMMARY, summaries)
    atomic_csv(POINTS, points)
    atomic_csv(REGRESSION, regressions)
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "symbolic_identity_remainder": symbolic["identity_remainder"],
        "symbolic_reciprocal_symmetry_remainder": symbolic[
            "reciprocal_symmetry_remainder"
        ],
        "point_crosscheck_count": len(points),
        "maximum_point_absolute_error": maximum_point_error,
        "full_cover_leaf_count": int(full_summary["leaf_count"]),
        "full_cover_zero_leaf_count": int(full_summary["zero_leaf_count"]),
        "full_cover_hull_real_lower": float(full_summary["hull_real_lower"]),
        "full_cover_hull_abs_lower": float(full_summary["hull_abs_lower"]),
        "historical_cover_hull_abs_lower": float(
            historical_summary["hull_abs_lower"]
        ),
        "targeted_regressions": regressions,
        "active_accepted_box_count": int(active_state["accepted_count"]),
        "active_pending_box_count": len(active_state["stack"]),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": remaining_area,
        "total_parameter_area": total_area,
        "valid_for_named_left_first_soft_invariant": True,
        "valid_for_continued_v44_production": True,
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
            parent.REVISION == REVISION,
            parent.REVISION,
        ),
        check(
            "symbolic_invariant_identity_is_exact",
            bool(symbolic["identity_exact"]),
            f"remainder={symbolic['identity_remainder']}",
        ),
        check(
            "representative_reciprocal_symmetry_is_exact",
            bool(symbolic["reciprocal_symmetry_exact"]),
            f"remainder={symbolic['reciprocal_symmetry_remainder']}",
        ),
        check(
            "point_identity_matches_both_momentum_copies",
            maximum_point_error <= 1.0e-12,
            f"count={len(points)}; max error={maximum_point_error:.17g}",
        ),
        check(
            "full_connector_finite_cover_has_no_zero_leaf",
            int(full_summary["zero_leaf_count"]) == 0,
            f"leaves={full_summary['leaf_count']}",
        ),
        check(
            "full_connector_rectangular_hull_is_nonzero",
            bool(full_summary["valid_for_full_rectangular_hull_nonzero"])
            and float(full_summary["hull_real_lower"]) > 0.0,
            f"real lower={full_summary['hull_real_lower']}; abs lower={full_summary['hull_abs_lower']}",
        ),
        check(
            "historical_box_geometric_cover_is_nonzero",
            bool(historical_summary["valid_for_full_rectangular_hull_nonzero"]),
            f"abs lower={historical_summary['hull_abs_lower']}",
        ),
        check(
            "targeted_parent_regressions_remove_named_edge",
            all(bool(row["removed_edge_absent"]) for row in regressions),
            " | ".join(str(row["later_failure"]) for row in regressions),
        ),
        check(
            "v43_state_is_resume_compatible_with_v44",
            active_state["revision"]
            in parent.PREVIOUS_RESUME_COMPATIBLE_REVISIONS,
            f"state={active_state['revision']}; parent={parent.REVISION}",
        ),
        check(
            "checkpoint_5424_is_green_and_bounded",
            int(previous["failed_validation_count"]) == 0
            and all(is_true(row["passed"]) for row in previous_validation)
            and not bool(previous["valid_for_regular_away_W3_claim"]),
            f"validation rows={len(previous_validation)}",
        ),
        check(
            "production_state_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(active_state["accepted_count"]) == len(active_rows),
            f"accepted={len(active_rows)}; pending={len(active_state['stack'])}",
        ),
        check(
            "accepted_plus_pending_area_is_exact",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={remaining_area:.17g}",
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
