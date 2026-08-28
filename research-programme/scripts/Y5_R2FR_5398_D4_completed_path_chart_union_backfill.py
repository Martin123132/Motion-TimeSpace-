from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
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


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
PRIMARY_PATH = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
GATE_PATH = SCRIPTS / "Y5_R2FR_5397_D4_selector_transition_chart_union_gate.py"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
INPUT = FUNCTIONAL_RG / "5396"
INPUT_PARTS = INPUT / "partial" / "path_parts"
GATE_RESULT = (
    FUNCTIONAL_RG / "5397" / "selector_transition_chart_union_result.json"
)
OUTPUT = FUNCTIONAL_RG / "5398"
STAGED_PARTS = OUTPUT / "staged_path_parts"
PARTIAL_PARTS = OUTPUT / "partial_path_parts"
ROW_AUDITS = OUTPUT / "row_audits"
STATE_PATH = OUTPUT / "backfill_state.json"
RESULT_PATH = OUTPUT / "completed_path_chart_union_backfill_result.json"
SUMMARY_PATH = OUTPUT / "completed_path_chart_union_backfill_summary.csv"
FAILURE_PATH = OUTPUT / "completed_path_chart_union_backfill_failures.csv"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5398_VALIDATION.csv"
)

CHECKPOINT = 5398
REVISION = "D4-completed-path-chart-union-backfill-v3"
PREVIOUS_RESUME_COMPATIBLE_REVISIONS = {
    "D4-completed-path-chart-union-backfill-v1",
    "D4-completed-path-chart-union-backfill-v2",
}
DEFAULT_RUNTIME_SECONDS = 600.0
DEFAULT_EXTRA_DEPTH = 6
DEFAULT_SAVE_EVERY = 10


class BackfillBudgetReached(RuntimeError):
    pass


def load_primary() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5398_primary", PRIMARY_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Stage closed full-chart-union replacements for completed 5396 "
            "v39 path boxes without modifying the live production files."
        )
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--runtime-seconds", type=float, default=DEFAULT_RUNTIME_SECONDS
    )
    parser.add_argument(
        "--extra-depth", type=int, default=DEFAULT_EXTRA_DEPTH
    )
    parser.add_argument(
        "--save-every", type=int, default=DEFAULT_SAVE_EVERY
    )
    return parser.parse_args()


def source_part_paths() -> list[Path]:
    return sorted(INPUT_PARTS.glob("*.csv"), key=lambda path: path.name)


def relative_path(path: Path) -> str:
    return str(path.relative_to(POST)).replace("\\", "/")


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def expected_chart_count(primary: Any, term_id: str) -> int:
    return len(primary.configuration_variants(term_id))


def source_inventory(primary: Any) -> tuple[list[Path], list[dict[str, Any]]]:
    paths = source_part_paths()
    rows: list[dict[str, Any]] = []
    for path in paths:
        source_rows = primary.read_csv(path)
        if not source_rows:
            raise RuntimeError(f"empty source path file: {path}")
        term_id = source_rows[0]["term_id"]
        expected = expected_chart_count(primary, term_id)
        rows.append(
            {
                "source_path": relative_path(path),
                "source_filename": path.name,
                "term_id": term_id,
                "path_segment": source_rows[0]["path_segment"],
                "source_row_count": len(source_rows),
                "expected_chart_count": expected,
                "source_rows_requiring_backfill": sum(
                    int(row["chart_count"]) < expected for row in source_rows
                ),
                "source_parameter_area": sum(
                    float(row["parameter_area"]) for row in source_rows
                ),
                "source_integrated_upper": sum(
                    float(row["integrated_regular_path_abs_upper"])
                    for row in source_rows
                ),
                "source_sha256": primary.digest(path),
            }
        )
    return paths, rows


def source_register(primary: Any, part_paths: list[Path]) -> list[dict[str, Any]]:
    paths = [
        Path(__file__).resolve(),
        PRIMARY_PATH,
        GATE_PATH,
        GATE_RESULT,
        INPUT / "run_manifest.json",
        INPUT / "status.json",
        *part_paths,
    ]
    return [
        {
            "path": relative_path(path),
            "sha256": primary.digest(path),
            "source_exists": path.is_file(),
        }
        for path in paths
    ]


def initial_state(
    primary: Any,
    inventory: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "state": "READY",
        "source_path_index": 0,
        "source_row_index": 0,
        "completed_source_row_count": 0,
        "certified_output_row_count": 0,
        "source_hashes": {
            row["source_filename"]: row["source_sha256"] for row in inventory
        },
        "latest_failure": None,
        "updated_utc": primary.utc_now(),
    }


def load_state(primary: Any, inventory: list[dict[str, Any]]) -> dict[str, Any]:
    state = (
        primary.read_json(STATE_PATH)
        if STATE_PATH.is_file()
        else initial_state(primary, inventory)
    )
    if (
        state.get("revision") != REVISION
        and state.get("revision") not in PREVIOUS_RESUME_COMPATIBLE_REVISIONS
    ):
        raise RuntimeError(
            f"incompatible backfill revision: {state.get('revision')}"
        )
    state["revision"] = REVISION
    expected_hashes = {
        row["source_filename"]: row["source_sha256"] for row in inventory
    }
    if state.get("source_hashes") != expected_hashes:
        raise RuntimeError(
            "live 5396 path inputs changed after the 5398 backfill started"
        )
    return state


def state_save(primary: Any, state: dict[str, Any], status: str) -> None:
    state["state"] = status
    state["updated_utc"] = primary.utc_now()
    primary.atomic_json(STATE_PATH, state)


def epsilon_row_from_source(row: dict[str, str]) -> dict[str, Any]:
    return {
        "regulator_bin_index": int(row["regulator_bin_index"]),
        "epsilon_subdivision_index": int(row["epsilon_subdivision_index"]),
        "epsilon_subdivision_count": int(row["epsilon_subdivision_count"]),
        "epsilon_real_lower": float(row["epsilon_real_lower"]),
        "epsilon_real_upper": float(row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
    }


def split_box(
    box: tuple[float, float, float, float, int, str],
    target_x_width: float,
    target_t_width: float,
) -> tuple[
    tuple[float, float, float, float, int, str],
    tuple[float, float, float, float, int, str],
]:
    x_lower, x_upper, t_lower, t_upper, depth, path = box
    x_width = x_upper - x_lower
    t_width = t_upper - t_lower
    x_score = x_width / max(target_x_width, 1.0e-15)
    t_score = t_width / max(target_t_width, 1.0e-15)
    if x_score >= t_score and x_width > 1.0e-14:
        midpoint = 0.5 * (x_lower + x_upper)
        return (
            (x_lower, midpoint, t_lower, t_upper, depth + 1, path + "L"),
            (midpoint, x_upper, t_lower, t_upper, depth + 1, path + "R"),
        )
    if t_width > 1.0e-14:
        midpoint = 0.5 * (t_lower + t_upper)
        return (
            (x_lower, x_upper, t_lower, midpoint, depth + 1, path + "D"),
            (x_lower, x_upper, midpoint, t_upper, depth + 1, path + "U"),
        )
    raise RuntimeError("no splittable interval remains in chart-union backfill")


def combine_source_and_missing_chart_bounds(
    primary: Any,
    source_row: dict[str, str],
    missing_row: dict[str, Any],
) -> dict[str, Any]:
    source_roles = [
        role for role in source_row["chart_roles"].split("|") if role
    ]
    missing_roles = [
        role for role in str(missing_row["chart_roles"]).split("|") if role
    ]
    roles = list(dict.fromkeys([*source_roles, *missing_roles]))
    source_orientations = [
        value for value in source_row["trace_orientation"].split("|") if value
    ]
    missing_orientations = [
        value
        for value in str(missing_row["trace_orientation"]).split("|")
        if value
    ]
    source_windings = [
        value for value in source_row["winding_delta"].split("|") if value
    ]
    missing_windings = [
        value
        for value in str(missing_row["winding_delta"]).split("|")
        if value
    ]
    result = dict(missing_row)
    result.update(
        {
            "selected_role": "CHART_UNION",
            "chart_roles": "|".join(roles),
            "chart_count": len(roles),
            "trace_orientation": "|".join(
                [*source_orientations, *missing_orientations]
            ),
            "winding_delta": "|".join(
                [*source_windings, *missing_windings]
            ),
            "backfill_combination_method": (
                "V39_SOURCE_SUPREMUM_PLUS_MISSING_CHART_CERTIFICATE"
            ),
            "path_integral_enclosure_method": (
                "CONSERVATIVE_SUM_OF_CERTIFIED_CHART_BOUNDS"
            ),
        }
    )
    for field in (
        "raw_integrand_abs_upper",
        "pole_correction_abs_upper",
        "regular_integrand_abs_upper",
    ):
        result[field] = float(source_row[field]) + float(missing_row[field])
    source_child_integrated_upper = (
        float(missing_row["parameter_area"])
        * float(source_row["path_speed_abs_upper"])
        * float(source_row["regular_integrand_abs_upper"])
    )
    result["integrated_regular_path_abs_upper"] = (
        source_child_integrated_upper
        + float(missing_row["integrated_regular_path_abs_upper"])
    )
    for field in (
        "lower_boundary_discriminant_abs_lower",
        "upper_boundary_discriminant_abs_lower",
        "pole_gap_abs_lower",
        "material_root_coefficient_abs_lower",
        "material_root_discriminant_abs_lower",
        "material_root_implicit_derivative_abs_lower",
        "minimum_amplitude_denominator_abs_lower",
        "relative_root_abs_lower",
        "selected_global_root_abs_lower",
        "collision_jacobian_abs_lower",
    ):
        result[field] = min(float(source_row[field]), float(missing_row[field]))
    result["path_speed_abs_upper"] = max(
        float(source_row["path_speed_abs_upper"]),
        float(missing_row["path_speed_abs_upper"]),
    )
    result["global_contour_radius"] = max(
        float(source_row["global_contour_radius"]),
        float(missing_row["global_contour_radius"]),
    )
    result["global_arc_count"] = max(
        int(source_row["global_arc_count"]),
        int(missing_row["global_arc_count"]),
    )
    result["global_regularized_coefficient_abs_upper"] = max(
        float(source_row["global_regularized_coefficient_abs_upper"]),
        float(missing_row["global_regularized_coefficient_abs_upper"]),
    )
    result["collision_jacobian_enclosure_method"] = (
        "V39_SOURCE_PARENT_BOX|"
        + str(missing_row.get("collision_jacobian_enclosure_method", "CURRENT"))
    )
    result[primary.CLAIM_DEFORMATION] = True
    result[primary.CLAIM_AWAY] = True
    result.update({claim: False for claim in primary.OPEN_CLAIMS})
    return result


def selector_margin_path_energy(
    primary: Any,
    cell: dict[str, Any],
    source_row: dict[str, str],
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
) -> tuple[Any, Any]:
    absolute_coordinate = primary.cbox(x_lower, x_upper)
    path_parameter = primary.cbox(t_lower, t_upper)
    lower_energy, _ = primary.interval_boundary_energy(
        cell["lower_energy_boundary"], x_lower, x_upper
    )
    upper_energy, _ = primary.interval_boundary_energy(
        cell["upper_energy_boundary"], x_lower, x_upper
    )
    energy_width = upper_energy - lower_energy
    if source_row["path_segment"] == "LEFT_CONNECTOR":
        energy = lower_energy + primary.cpoint(
            1j * primary.DEFAULT_ENERGY_DEFORMATION
        ) * path_parameter
    elif source_row["path_segment"] == "TOP":
        energy = (
            lower_energy
            + path_parameter * energy_width
            + primary.cpoint(1j * primary.DEFAULT_ENERGY_DEFORMATION)
        )
    elif source_row["path_segment"] == "RIGHT_CONNECTOR":
        energy = upper_energy + primary.cpoint(
            1j * primary.DEFAULT_ENERGY_DEFORMATION
        ) * path_parameter
    else:
        raise ValueError(
            f"unsupported path segment {source_row['path_segment']}"
        )
    return absolute_coordinate, energy


def certify_closed_selector_role_margin(
    primary: Any,
    source_row: dict[str, str],
    cell: dict[str, Any],
    target_x_width: float,
    target_t_width: float,
    extra_depth: int,
) -> dict[str, Any]:
    source_roles = [
        role for role in source_row["chart_roles"].split("|") if role
    ]
    if len(source_roles) != 1:
        return {
            "passed": False,
            "failure": "source row does not contain exactly one chart role",
        }
    source_role = source_roles[0]
    representative_configurations = [
        configuration
        for configuration in primary.configuration_variants(
            source_row["term_id"]
        )
        if configuration["role"] == "representative"
    ]
    if len(representative_configurations) != 1:
        return {
            "passed": False,
            "failure": "term has no unique representative selector chart",
        }
    configuration = representative_configurations[0]
    initial_depth = int(source_row["refinement_depth"])
    maximum_depth = initial_depth + extra_depth
    stack = [
        (
            float(source_row["x_lower"]),
            float(source_row["x_upper"]),
            float(source_row["t_lower"]),
            float(source_row["t_upper"]),
            initial_depth,
            source_row["refinement_path"],
        )
    ]
    margins: list[float] = []
    failure_categories: list[str] = []
    split_count = 0
    maximum_observed_depth = initial_depth
    while stack:
        box = stack.pop()
        x_lower, x_upper, t_lower, t_upper, depth, _ = box
        maximum_observed_depth = max(maximum_observed_depth, depth)
        classified_role = "AMBIGUOUS"
        lower_modulus = 0.0
        upper_modulus = math.inf
        try:
            absolute_coordinate, energy = selector_margin_path_energy(
                primary,
                cell,
                source_row,
                x_lower,
                x_upper,
                t_lower,
                t_upper,
            )
            _, geometry = primary.interval_inputs(
                configuration,
                absolute_coordinate,
                energy,
                primary.epsilon_interval(
                    epsilon_row_from_source(source_row)
                ),
            )
            representative = geometry["relative"]
            lower_modulus = primary.M5258.lower_abs(representative)
            upper_modulus = primary.M5258.upper_abs(representative)
            if upper_modulus < 1.0:
                classified_role = "reciprocal"
                margin = 1.0 - upper_modulus
            elif lower_modulus > 1.0:
                classified_role = "representative"
                margin = lower_modulus - 1.0
            else:
                margin = 0.0
        except Exception as error:
            failure_categories.append(
                primary.enclosure_failure_category(error)
            )
            margin = 0.0
        if classified_role == source_role and margin > 0.0:
            margins.append(margin)
            continue
        if classified_role not in {"AMBIGUOUS", source_role}:
            return {
                "passed": False,
                "failure": "closed child selects the opposite chart role",
                "source_role": source_role,
                "opposite_role": classified_role,
                "representative_modulus_lower": lower_modulus,
                "representative_modulus_upper": upper_modulus,
                "leaf_count": len(margins),
                "split_count": split_count,
                "maximum_depth": maximum_observed_depth,
                "failure_categories": "|".join(
                    sorted(set(failure_categories))
                ),
            }
        if depth >= maximum_depth:
            return {
                "passed": False,
                "failure": "unit-circle margin remains unresolved",
                "source_role": source_role,
                "representative_modulus_lower": lower_modulus,
                "representative_modulus_upper": upper_modulus,
                "leaf_count": len(margins),
                "split_count": split_count,
                "maximum_depth": maximum_observed_depth,
                "failure_categories": "|".join(
                    sorted(set(failure_categories))
                ),
            }
        first, second = split_box(box, target_x_width, target_t_width)
        stack.extend((second, first))
        split_count += 1
    return {
        "passed": bool(margins),
        "source_role": source_role,
        "selector_rule": (
            "representative iff |R_rep|>=1; reciprocal iff |R_rep|<1"
        ),
        "minimum_unit_margin": min(margins),
        "leaf_count": len(margins),
        "split_count": split_count,
        "maximum_depth": maximum_observed_depth,
        "failure_categories": "|".join(
            sorted(set(failure_categories))
        ),
    }


def selector_margin_staged_row(
    source_row: dict[str, str], proof: dict[str, Any]
) -> dict[str, Any]:
    return {
        **source_row,
        "selector_ownership_method": (
            "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
        ),
        "selector_margin_source_role": proof["source_role"],
        "selector_role_margin_lower": proof["minimum_unit_margin"],
        "selector_margin_leaf_count": proof["leaf_count"],
        "selector_margin_split_count": proof["split_count"],
        "selector_margin_maximum_depth": proof["maximum_depth"],
        "selector_margin_failure_categories": proof[
            "failure_categories"
        ],
    }


def selector_margin_audit(
    source_path: Path,
    row_index: int,
    source_row: dict[str, str],
    proof: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_filename": source_path.name,
        "source_row_index": row_index,
        "mapped_cell_id": source_row["mapped_cell_id"],
        "term_id": source_row["term_id"],
        "path_segment": source_row["path_segment"],
        "source_refinement_depth": int(source_row["refinement_depth"]),
        "source_refinement_path": source_row["refinement_path"],
        "source_chart_count": int(source_row["chart_count"]),
        "certified_chart_count": int(source_row["chart_count"]),
        "certified_child_row_count": 1,
        "source_parameter_area": float(source_row["parameter_area"]),
        "certified_parameter_area": float(source_row["parameter_area"]),
        "area_relative_error": 0.0,
        "source_integrated_upper": float(
            source_row["integrated_regular_path_abs_upper"]
        ),
        "certified_integrated_upper": float(
            source_row["integrated_regular_path_abs_upper"]
        ),
        "certified_to_source_upper_ratio": 1.0,
        "minimum_certified_amplitude_denominator": float(
            source_row["minimum_amplitude_denominator_abs_lower"]
        ),
        "minimum_certified_collision_jacobian": float(
            source_row["collision_jacobian_abs_lower"]
        ),
        "additional_split_failure_count": int(proof["split_count"]),
        "additional_split_failure_categories": proof[
            "failure_categories"
        ],
        "backfill_combination_method": (
            "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
        ),
        "selector_margin_source_role": proof["source_role"],
        "selector_role_margin_lower": proof["minimum_unit_margin"],
        "selector_margin_leaf_count": proof["leaf_count"],
        "selector_margin_maximum_depth": proof["maximum_depth"],
        "closed_chart_union_row_passed": True,
    }


def certify_source_row(
    primary: Any,
    source_row: dict[str, str],
    cell: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    target_x_width: float,
    target_t_width: float,
    extra_depth: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    term_id = source_row["term_id"]
    configurations = primary.configuration_variants(term_id)
    source_roles = set(source_row["chart_roles"].split("|"))
    missing_configurations = [
        configuration
        for configuration in configurations
        if configuration["role"] not in source_roles
    ]
    if not missing_configurations:
        return [dict(source_row)], []
    initial_depth = int(source_row["refinement_depth"])
    maximum_depth = initial_depth + extra_depth
    stack = [
        (
            float(source_row["x_lower"]),
            float(source_row["x_upper"]),
            float(source_row["t_lower"]),
            float(source_row["t_upper"]),
            initial_depth,
            source_row["refinement_path"],
        )
    ]
    accepted: list[dict[str, Any]] = []
    failure_categories: list[str] = []
    while stack:
        box = stack.pop()
        x_lower, x_upper, t_lower, t_upper, depth, path = box
        try:
            accepted.append(
                primary.evaluate_path_box(
                    cell,
                    term_id,
                    missing_configurations,
                    epsilon_row_from_source(source_row),
                    source_row["path_segment"],
                    x_lower,
                    x_upper,
                    t_lower,
                    t_upper,
                    depth,
                    path,
                    support_segments,
                    branches,
                    int(source_row["global_arc_count"]),
                )
            )
            accepted[-1] = combine_source_and_missing_chart_bounds(
                primary, source_row, accepted[-1]
            )
        except Exception as error:
            failure_categories.append(primary.enclosure_failure_category(error))
            if depth >= maximum_depth:
                raise RuntimeError(
                    "closed chart-union backfill exhausted at "
                    f"depth {depth}: {type(error).__name__}: {error}"
                ) from error
            first, second = split_box(box, target_x_width, target_t_width)
            stack.extend((second, first))
    return accepted, failure_categories


def partial_paths(source_path: Path) -> tuple[Path, Path]:
    return (
        PARTIAL_PARTS / f"{source_path.stem}.partial.csv",
        ROW_AUDITS / f"{source_path.stem}.partial.audit.csv",
    )


def completed_audit_path(source_path: Path) -> Path:
    return ROW_AUDITS / f"{source_path.stem}.audit.csv"


def save_partial(
    primary: Any,
    source_path: Path,
    staged_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
) -> None:
    staged_partial, audit_partial = partial_paths(source_path)
    if staged_rows:
        primary.atomic_csv(staged_partial, staged_rows)
    if audit_rows:
        primary.atomic_csv(audit_partial, audit_rows)


def load_partial(
    primary: Any, source_path: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    staged_partial, audit_partial = partial_paths(source_path)
    staged_rows = (
        [dict(row) for row in primary.read_csv(staged_partial)]
        if staged_partial.is_file()
        else []
    )
    audit_rows = (
        [dict(row) for row in primary.read_csv(audit_partial)]
        if audit_partial.is_file()
        else []
    )
    return staged_rows, audit_rows


def finalize_path(
    primary: Any,
    source_path: Path,
    staged_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
) -> None:
    staged_target = STAGED_PARTS / source_path.name
    audit_target = completed_audit_path(source_path)
    primary.atomic_csv(staged_target, staged_rows)
    primary.atomic_csv(audit_target, audit_rows)
    staged_partial, audit_partial = partial_paths(source_path)
    for partial in (staged_partial, audit_partial):
        if partial.is_file():
            partial.unlink()


def source_row_audit(
    primary: Any,
    source_path: Path,
    row_index: int,
    source_row: dict[str, str],
    certified_rows: list[dict[str, Any]],
    failure_categories: list[str],
) -> dict[str, Any]:
    source_area = float(source_row["parameter_area"])
    certified_area = sum(float(row["parameter_area"]) for row in certified_rows)
    source_upper = float(source_row["integrated_regular_path_abs_upper"])
    certified_upper = sum(
        float(row["integrated_regular_path_abs_upper"])
        for row in certified_rows
    )
    expected_count = int(certified_rows[0]["chart_count"])
    return {
        "source_filename": source_path.name,
        "source_row_index": row_index,
        "mapped_cell_id": source_row["mapped_cell_id"],
        "term_id": source_row["term_id"],
        "path_segment": source_row["path_segment"],
        "source_refinement_depth": int(source_row["refinement_depth"]),
        "source_refinement_path": source_row["refinement_path"],
        "source_chart_count": int(source_row["chart_count"]),
        "certified_chart_count": expected_count,
        "certified_child_row_count": len(certified_rows),
        "source_parameter_area": source_area,
        "certified_parameter_area": certified_area,
        "area_relative_error": abs(certified_area - source_area)
        / max(source_area, 1.0e-300),
        "source_integrated_upper": source_upper,
        "certified_integrated_upper": certified_upper,
        "certified_to_source_upper_ratio": certified_upper
        / max(source_upper, 1.0e-300),
        "minimum_certified_amplitude_denominator": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in certified_rows
        ),
        "minimum_certified_collision_jacobian": min(
            float(row["collision_jacobian_abs_lower"])
            for row in certified_rows
        ),
        "additional_split_failure_count": len(failure_categories),
        "additional_split_failure_categories": "|".join(
            sorted(set(failure_categories))
        ),
        "backfill_combination_method": certified_rows[0].get(
            "backfill_combination_method", "FULL_CHART_UNION_RECOMPUTE"
        ),
        "closed_chart_union_row_passed": (
            expected_count >= int(source_row["chart_count"])
            and all(
                int(row["chart_count"]) == expected_count
                and row["selected_role"] == "CHART_UNION"
                and as_bool(row[primary.CLAIM_DEFORMATION])
                and as_bool(row[primary.CLAIM_AWAY])
                and all(not as_bool(row[claim]) for claim in primary.OPEN_CLAIMS)
                for row in certified_rows
            )
            and abs(certified_area - source_area)
            <= 1.0e-12 * max(1.0, source_area)
        ),
    }


def path_summaries(
    primary: Any, inventory: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for source in inventory:
        staged_path = STAGED_PARTS / source["source_filename"]
        if not staged_path.is_file():
            summaries.append(
                {
                    **source,
                    "staged_path": relative_path(staged_path),
                    "staged_complete": False,
                    "staged_row_count": 0,
                    "staged_parameter_area": 0.0,
                    "staged_integrated_upper": 0.0,
                    "all_staged_rows_have_expected_chart_count": False,
                    "all_claims_remain_locked": True,
                }
            )
            continue
        rows = primary.read_csv(staged_path)
        expected = int(source["expected_chart_count"])
        closed_rows = [
            (
                int(row["chart_count"]) == expected
                and row["selected_role"] == "CHART_UNION"
            )
            or (
                row.get("selector_ownership_method")
                == "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
                and float(row.get("selector_role_margin_lower", 0.0)) > 0.0
                and row.get("selector_margin_source_role")
                in row["chart_roles"].split("|")
            )
            for row in rows
        ]
        summaries.append(
            {
                **source,
                "staged_path": relative_path(staged_path),
                "staged_complete": True,
                "staged_row_count": len(rows),
                "staged_parameter_area": sum(
                    float(row["parameter_area"]) for row in rows
                ),
                "staged_integrated_upper": sum(
                    float(row["integrated_regular_path_abs_upper"])
                    for row in rows
                ),
                "all_staged_rows_have_expected_chart_count": all(
                    int(row["chart_count"]) == expected for row in rows
                ),
                "closed_selector_margin_row_count": sum(
                    row.get("selector_ownership_method")
                    == "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
                    for row in rows
                ),
                "minimum_closed_selector_margin": min(
                    (
                        float(row["selector_role_margin_lower"])
                        for row in rows
                        if row.get("selector_ownership_method")
                        == "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
                    ),
                    default=math.inf,
                ),
                "all_staged_rows_closed_by_union_or_selector_margin": all(
                    closed_rows
                ),
                "all_claims_remain_locked": all(
                    as_bool(row[primary.CLAIM_DEFORMATION])
                    and as_bool(row[primary.CLAIM_AWAY])
                    and all(not as_bool(row[claim]) for claim in primary.OPEN_CLAIMS)
                    for row in rows
                ),
            }
        )
    return summaries


def validation_row(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def write_result(
    primary: Any,
    inventory: list[dict[str, Any]],
    state: dict[str, Any],
    runtime_seconds: float,
    failure_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    summaries = path_summaries(primary, inventory)
    primary.atomic_csv(SUMMARY_PATH, summaries)
    if failure_rows:
        primary.atomic_csv(FAILURE_PATH, failure_rows)
    elif FAILURE_PATH.is_file():
        FAILURE_PATH.unlink()
    completed = sum(bool(row["staged_complete"]) for row in summaries)
    all_complete = completed == len(summaries)
    live_hashes_unchanged = all(
        primary.digest(INPUT_PARTS / row["source_filename"])
        == row["source_sha256"]
        for row in inventory
    )
    area_closed = all(
        not row["staged_complete"]
        or abs(
            float(row["staged_parameter_area"])
            - float(row["source_parameter_area"])
        )
        <= 1.0e-12 * max(1.0, float(row["source_parameter_area"]))
        for row in summaries
    )
    completed_rows_valid = all(
        not row["staged_complete"]
        or (
            bool(row["all_staged_rows_closed_by_union_or_selector_margin"])
            and bool(row["all_claims_remain_locked"])
        )
        for row in summaries
    )
    valid_for_staged_migration = (
        all_complete
        and live_hashes_unchanged
        and area_closed
        and completed_rows_valid
        and not failure_rows
    )
    validations = [
        validation_row(
            "5397_chart_union_algorithm_gate_passed",
            bool(primary.read_json(GATE_RESULT)[
                "valid_for_selector_transition_chart_union_algorithm"
            ]),
            relative_path(GATE_RESULT),
        ),
        validation_row(
            "live_5396_path_inputs_remain_byte_identical",
            live_hashes_unchanged,
            len(inventory),
        ),
        validation_row(
            "every_completed_staged_path_preserves_parameter_area",
            area_closed,
            completed,
        ),
        validation_row(
            "every_completed_staged_row_has_union_or_closed_selector_margin",
            completed_rows_valid,
            completed,
        ),
        validation_row(
            "live_atlas_migration_remains_blocked_until_staging_completes",
            not valid_for_staged_migration or all_complete,
            f"completed={completed}/{len(inventory)}",
        ),
    ]
    primary.atomic_csv(VALIDATION, validations)
    payload = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": 5397,
        "revision": REVISION,
        "state": state["state"],
        "runtime_seconds": runtime_seconds,
        "source_path_count": len(inventory),
        "source_row_count": sum(
            int(row["source_row_count"]) for row in inventory
        ),
        "source_rows_requiring_backfill": sum(
            int(row["source_rows_requiring_backfill"]) for row in inventory
        ),
        "completed_source_row_count": int(
            state["completed_source_row_count"]
        ),
        "certified_output_row_count": int(
            state["certified_output_row_count"]
        ),
        "completed_staged_path_count": completed,
        "completed_closed_selector_margin_row_count": sum(
            int(row.get("closed_selector_margin_row_count", 0))
            for row in summaries
            if row["staged_complete"]
        ),
        "all_staged_paths_complete": all_complete,
        "live_5396_inputs_unchanged": live_hashes_unchanged,
        "valid_for_closed_v39_chart_union_backfill": (
            valid_for_staged_migration
        ),
        "valid_for_staged_atlas_migration": valid_for_staged_migration,
        "valid_for_live_atlas_migration": False,
        "claim_boundary": (
            "A completed staged backfill licenses a separate atomic migration "
            "step only. This runner never overwrites 5396, never promotes the "
            "event-local or UV claims, and does not close the remaining atlas."
        ),
    }
    primary.atomic_json(RESULT_PATH, payload)
    return payload


def dry_run(primary: Any) -> dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    paths, inventory = source_inventory(primary)
    sources = source_register(primary, paths)
    primary.atomic_csv(OUTPUT / "source_register.csv", sources)
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "mode": "strict_dry_run",
        "source_path_count": len(paths),
        "source_row_count": sum(
            int(row["source_row_count"]) for row in inventory
        ),
        "source_rows_requiring_backfill": sum(
            int(row["source_rows_requiring_backfill"]) for row in inventory
        ),
        "single_chart_passthrough_rows": sum(
            int(row["source_row_count"])
            - int(row["source_rows_requiring_backfill"])
            for row in inventory
        ),
        "all_sources_exist_and_are_hashed": all(
            row["source_exists"] and row["sha256"] for row in sources
        ),
        "5397_algorithm_gate_passed": bool(
            primary.read_json(GATE_RESULT)[
                "valid_for_selector_transition_chart_union_algorithm"
            ]
        ),
        "writes_live_5396_files": False,
        "valid_for_live_atlas_migration": False,
    }
    primary.atomic_json(OUTPUT / "dry_run_result.json", payload)
    return payload


def run(arguments: argparse.Namespace, primary: Any) -> dict[str, Any]:
    started = time.time()
    deadline = started + max(1.0, arguments.runtime_seconds)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    STAGED_PARTS.mkdir(parents=True, exist_ok=True)
    PARTIAL_PARTS.mkdir(parents=True, exist_ok=True)
    ROW_AUDITS.mkdir(parents=True, exist_ok=True)
    paths, inventory = source_inventory(primary)
    primary.atomic_csv(OUTPUT / "source_register.csv", source_register(primary, paths))
    state = load_state(primary, inventory)
    state["latest_failure"] = None
    manifest = primary.read_json(INPUT / "run_manifest.json")
    cells = {
        row["mapped_cell_id"]: row for row in primary.away_term_support_cells()
    }
    support_segments = primary.material_support_segments()
    branches = primary.material_branch_data()
    failure_rows: list[dict[str, Any]] = []
    try:
        for path_index in range(int(state["source_path_index"]), len(paths)):
            source_path = paths[path_index]
            source_rows = primary.read_csv(source_path)
            term_id = source_rows[0]["term_id"]
            expected = expected_chart_count(primary, term_id)
            cell = cells[source_rows[0]["mapped_cell_id"]]
            state["source_path_index"] = path_index
            if expected == 1:
                passthrough_audits = [
                    {
                        "source_filename": source_path.name,
                        "source_row_index": row_index,
                        "mapped_cell_id": row["mapped_cell_id"],
                        "term_id": term_id,
                        "path_segment": row["path_segment"],
                        "source_refinement_depth": int(row["refinement_depth"]),
                        "source_refinement_path": row["refinement_path"],
                        "source_chart_count": 1,
                        "certified_chart_count": 1,
                        "certified_child_row_count": 1,
                        "source_parameter_area": float(row["parameter_area"]),
                        "certified_parameter_area": float(row["parameter_area"]),
                        "area_relative_error": 0.0,
                        "source_integrated_upper": float(
                            row["integrated_regular_path_abs_upper"]
                        ),
                        "certified_integrated_upper": float(
                            row["integrated_regular_path_abs_upper"]
                        ),
                        "certified_to_source_upper_ratio": 1.0,
                        "minimum_certified_amplitude_denominator": float(
                            row["minimum_amplitude_denominator_abs_lower"]
                        ),
                        "minimum_certified_collision_jacobian": float(
                            row["collision_jacobian_abs_lower"]
                        ),
                        "additional_split_failure_count": 0,
                        "additional_split_failure_categories": "",
                        "closed_chart_union_row_passed": True,
                    }
                    for row_index, row in enumerate(source_rows)
                ]
                finalize_path(
                    primary,
                    source_path,
                    [dict(row) for row in source_rows],
                    passthrough_audits,
                )
                state["completed_source_row_count"] += len(source_rows)
                state["certified_output_row_count"] += len(source_rows)
                state["source_path_index"] = path_index + 1
                state["source_row_index"] = 0
                state_save(primary, state, "RUNNING")
                if time.time() >= deadline:
                    raise BackfillBudgetReached
                continue
            staged_rows, audit_rows = load_partial(primary, source_path)
            row_start = int(state["source_row_index"])
            for row_index in range(row_start, len(source_rows)):
                source_row = source_rows[row_index]
                selector_proof = certify_closed_selector_role_margin(
                    primary,
                    source_row,
                    cell,
                    float(manifest["target_x_width"]),
                    float(manifest["target_path_width"]),
                    arguments.extra_depth,
                )
                if selector_proof["passed"]:
                    certified_rows = [
                        selector_margin_staged_row(source_row, selector_proof)
                    ]
                    audit = selector_margin_audit(
                        source_path,
                        row_index,
                        source_row,
                        selector_proof,
                    )
                else:
                    certified_rows, failure_categories = certify_source_row(
                        primary,
                        source_row,
                        cell,
                        support_segments,
                        branches,
                        float(manifest["target_x_width"]),
                        float(manifest["target_path_width"]),
                        arguments.extra_depth,
                    )
                    audit = source_row_audit(
                        primary,
                        source_path,
                        row_index,
                        source_row,
                        certified_rows,
                        failure_categories,
                    )
                    audit["selector_margin_fallback_reason"] = (
                        selector_proof.get("failure", "UNKNOWN")
                    )
                if not audit["closed_chart_union_row_passed"]:
                    raise RuntimeError(
                        f"closed chart-union audit failed for {source_path.name} "
                        f"row {row_index}"
                    )
                staged_rows.extend(certified_rows)
                audit_rows.append(audit)
                state["source_row_index"] = row_index + 1
                state["completed_source_row_count"] += 1
                state["certified_output_row_count"] += len(certified_rows)
                if (
                    (row_index + 1) % max(1, arguments.save_every) == 0
                    or time.time() >= deadline
                ):
                    save_partial(primary, source_path, staged_rows, audit_rows)
                    state_save(primary, state, "RUNNING")
                if time.time() >= deadline:
                    raise BackfillBudgetReached
            finalize_path(primary, source_path, staged_rows, audit_rows)
            state["source_path_index"] = path_index + 1
            state["source_row_index"] = 0
            state_save(primary, state, "RUNNING")
        state_save(primary, state, "STAGED_BACKFILL_COMPLETE")
    except BackfillBudgetReached:
        state_save(primary, state, "PAUSED_AT_RUNTIME_BUDGET")
    except Exception as error:
        failure = {
            "source_path_index": int(state["source_path_index"]),
            "source_row_index": int(state["source_row_index"]),
            "source_filename": paths[int(state["source_path_index"])].name
            if int(state["source_path_index"]) < len(paths)
            else "COMPLETE",
            "error_type": type(error).__name__,
            "error": str(error),
            "valid_for_claim": False,
        }
        failure_rows.append(failure)
        state["latest_failure"] = failure
        state_save(primary, state, "BLOCKED_ON_CLOSED_BOX")
    return write_result(
        primary,
        inventory,
        state,
        time.time() - started,
        failure_rows,
    )


def main() -> int:
    arguments = parse_arguments()
    primary = load_primary()
    primary.set_below_normal_priority()
    payload = dry_run(primary) if arguments.dry_run else run(arguments, primary)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
