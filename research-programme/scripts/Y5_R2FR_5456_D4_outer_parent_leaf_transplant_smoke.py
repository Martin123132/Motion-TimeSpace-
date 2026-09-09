from __future__ import annotations

import argparse
import cmath
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(variable, "1")


POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5456"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5449 = POST / "scripts" / "Y5_R2FR_5449_D4_event_local_finite_enclosure_smoke.py"
RESULT_5449 = FUNCTIONAL_RG / "5449" / "D4_event_local_finite_enclosure_smoke_result.json"
SCRIPT_5450 = POST / "scripts" / "Y5_R2FR_5450_D4_event_endpoint_Cauchy_subtraction_and_correlated_probe.py"
RESULT_5450 = FUNCTIONAL_RG / "5450" / "D4_event_endpoint_Cauchy_subtraction_result.json"
SCRIPT_5451 = POST / "scripts" / "Y5_R2FR_5451_D4_event_endpoint_xt_overlap_geometry_cover.py"
COVER_5451 = FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_cover.csv"
RESULT_5451 = FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_geometry_result.json"
RESULT_5455 = FUNCTIONAL_RG / "5455" / "D4_full_epsilon_connected_superprojection_cover_result.json"
COMPLETE_5455 = FUNCTIONAL_RG / "5455" / "COMPLETE.json"

DOCUMENT = POST / "5456-Y5-R2FR-D4-outer-parent-leaf-transplant-smoke.md"
REPRESENTATIVES = OUTPUT / "D4_outer_parent_leaf_representatives.csv"
SMOKE = OUTPUT / "D4_outer_parent_leaf_smoke.csv"
OWNER_SUMMARY = OUTPUT / "D4_outer_parent_owner_path_smoke_summary.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5449_5456_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_outer_parent_leaf_transplant_smoke_result.json"

CHECKPOINT = 5456
REVISION = "D4-outer-parent-leaf-transplant-smoke-v2"
OUTER_RADIUS = 5.0e-6
GLOBAL_ARC_COUNT = 4
PATH_SEGMENTS = ("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR")
RECOIL_SHEET_METHOD = (
    "SIGN_DEFINITE_MONOTONE_PRINCIPAL_SQRT_RECTANGLE_WITH_PARENT_FALLBACK"
)


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any], compact: bool = False) -> None:
    value = (
        json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n"
        if compact
        else json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n"
    )
    atomic_text(path, value)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields = list(rows[0])
    known = set(fields)
    for row in rows[1:]:
        for field in row:
            if field not in known:
                fields.append(field)
                known.add(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5449,
        RESULT_5449,
        SCRIPT_5450,
        RESULT_5450,
        SCRIPT_5451,
        COVER_5451,
        RESULT_5451,
        RESULT_5455,
        COMPLETE_5455,
    )


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    return {
        str(path): (path.stat().st_mtime_ns, path.stat().st_size)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def leaf_identity(row: dict[str, str]) -> tuple[Any, ...]:
    return (
        row["event_id"],
        row["mapped_cell_id"],
        row["term_id"],
        int(row["epsilon_bin_index"]),
        int(row["epsilon_subdivision_index"]),
        int(row["epsilon_subdivision_count"]),
        row["path_segment"],
        row["x_lower"],
        row["x_upper"],
        row["t_lower"],
        row["t_upper"],
    )


def representative_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], dict[str, dict[str, str]]] = {}
    outer_leaf_count = 0
    with COVER_5451.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["cover_owner"] != "OUTER_PARENT_TRIANGLE":
                continue
            outer_leaf_count += 1
            key = (
                row["event_id"],
                row["mapped_cell_id"],
                row["term_id"],
                row["path_segment"],
            )
            selected = groups.setdefault(key, {})
            current_area = selected.get("MAXIMUM_PHYSICAL_PATH_AREA")
            if current_area is None or float(row["physical_path_area_abs_upper"]) > float(
                current_area["physical_path_area_abs_upper"]
            ):
                selected["MAXIMUM_PHYSICAL_PATH_AREA"] = dict(row)
            current_gap = selected.get("MINIMUM_CERTIFIED_OUTER_GAP")
            if current_gap is None or float(row["gap_abs_lower"]) < float(
                current_gap["gap_abs_lower"]
            ):
                selected["MINIMUM_CERTIFIED_OUTER_GAP"] = dict(row)
    rows: list[dict[str, Any]] = []
    for key, selected in sorted(groups.items()):
        by_identity: dict[tuple[Any, ...], dict[str, Any]] = {}
        for role, source in selected.items():
            identity = leaf_identity(source)
            if identity in by_identity:
                by_identity[identity]["selection_role"] += f"|{role}"
                continue
            job_id = f"{source['event_id']}__{source['mapped_cell_id']}__{source['path_segment']}__{role}"
            by_identity[identity] = {
                "smoke_job_id": job_id,
                "selection_role": role,
                **source,
                "valid_for_outer_parent_leaf_transplant_smoke": False,
                "valid_for_full_outer_parent_leaf_enclosure": False,
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        rows.extend(by_identity.values())
    diagnostics = {
        "outer_geometry_leaf_count": outer_leaf_count,
        "owner_path_group_count": len(groups),
        "representative_job_count": len(rows),
        "owner_cell_term_count": len({key[:3] for key in groups}),
    }
    return rows, diagnostics


def principal_sqrt_components_at(parent: Any, real_value: float, imag_abs: float) -> tuple[Any, Any]:
    real_interval = parent.iv.mpf([real_value, real_value])
    imag_interval = parent.iv.mpf([imag_abs, imag_abs])
    two = parent.iv.mpf([2.0, 2.0])
    radius = parent.iv.sqrt(
        real_interval * real_interval + imag_interval * imag_interval
    )
    if real_value >= 0.0:
        real_component = parent.iv.sqrt((radius + real_interval) / two)
    else:
        real_component = imag_interval / parent.iv.sqrt(
            two * (radius - real_interval)
        )
    if real_value <= 0.0:
        imaginary_component = parent.iv.sqrt((radius - real_interval) / two)
    else:
        imaginary_component = imag_interval / parent.iv.sqrt(
            two * (radius + real_interval)
        )
    return real_component, imaginary_component


def stable_principal_sqrt_nonreal(parent: Any, value: Any) -> Any:
    real_lower, real_upper = parent.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(value)
    if imaginary_lower > 0.0:
        sign = 1.0
        imaginary_abs_lower = imaginary_lower
        imaginary_abs_upper = imaginary_upper
    elif imaginary_upper < 0.0:
        sign = -1.0
        imaginary_abs_lower = -imaginary_upper
        imaginary_abs_upper = -imaginary_lower
    else:
        return parent.M5394.interval_complex_sqrt(value)
    real_minimum, _ = principal_sqrt_components_at(
        parent, real_lower, imaginary_abs_lower
    )
    real_maximum, _ = principal_sqrt_components_at(
        parent, real_upper, imaginary_abs_upper
    )
    _, imaginary_minimum = principal_sqrt_components_at(
        parent, real_upper, imaginary_abs_lower
    )
    _, imaginary_maximum = principal_sqrt_components_at(
        parent, real_lower, imaginary_abs_upper
    )
    root_real_lower = math.nextafter(float(real_minimum.a), -math.inf)
    root_real_upper = math.nextafter(float(real_maximum.b), math.inf)
    root_imaginary_abs_lower = max(
        0.0, math.nextafter(float(imaginary_minimum.a), -math.inf)
    )
    root_imaginary_abs_upper = math.nextafter(
        float(imaginary_maximum.b), math.inf
    )
    if sign > 0.0:
        root_imaginary_lower = root_imaginary_abs_lower
        root_imaginary_upper = root_imaginary_abs_upper
    else:
        root_imaginary_lower = -root_imaginary_abs_upper
        root_imaginary_upper = -root_imaginary_abs_lower
    return parent.cbox(
        root_real_lower,
        root_real_upper,
        root_imaginary_lower,
        root_imaginary_upper,
    )


def install_stable_recoil_sheet(parent: Any) -> None:
    def interval_inputs(
        configuration: dict[str, Any],
        absolute_coordinate: Any,
        energy: Any,
        epsilon: Any,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        soft_cosine = configuration["soft_sign"] * absolute_coordinate
        soft_sine = parent.M5394.interval_complex_sqrt(
            parent.cpoint(1) - soft_cosine**2
        )
        decay_cosine = parent.cpoint(
            configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
        )
        decay_sine = parent.cpoint(
            math.sqrt(1.0 - parent.M5394.ABSOLUTE_DECAY_COSINE**2)
        )
        q_value = parent.M5394.q_value(epsilon)
        external_root = -parent.cpoint(1j) * parent.M5394.interval_complex_sqrt(
            -q_value
        )
        recoil = stable_principal_sqrt_nonreal(
            parent, parent.cpoint(1) - energy
        )
        if parent.M5394.real_bounds(recoil)[0] <= 0.0:
            raise parent.EnclosureFailure(
                "deformed recoil leaves its parent positive-real sheet"
            )
        inputs = {
            "epsilon": epsilon,
            "material_recoil": recoil,
            "soft_cosine": soft_cosine,
            "soft_sine": soft_sine,
            "decay_cosine": decay_cosine,
            "decay_sine": decay_sine,
            "q_value": q_value,
            "external_root": external_root,
        }
        geometry = parent.M5385.expanded_geometry(
            configuration,
            inputs,
            parent.cpoint(0),
            recoil_override=recoil,
        )
        return inputs, geometry

    parent.interval_inputs = interval_inputs


def validate_stable_recoil_sheet(
    parent: Any, representatives: list[dict[str, Any]]
) -> dict[str, Any]:
    tested_box_count = 0
    tested_point_count = 0
    minimum_real_lower = math.inf
    all_points_enclosed = True
    point_failure_count = 0
    point_failure_examples: list[dict[str, float]] = []
    cells = {
        row["mapped_cell_id"]: row for row in parent.read_csv(parent.MAPPED_5393)
    }
    for row in representatives:
        if row["path_segment"] != "TOP":
            continue
        cell = cells[row["mapped_cell_id"]]
        x_lower = float(row["x_lower"])
        x_upper = float(row["x_upper"])
        lower_energy, _ = parent.interval_boundary_energy(
            cell["lower_energy_boundary"], x_lower, x_upper
        )
        upper_energy, _ = parent.interval_boundary_energy(
            cell["upper_energy_boundary"], x_lower, x_upper
        )
        path_parameter = parent.cbox(float(row["t_lower"]), float(row["t_upper"]))
        energy = (
            lower_energy
            + path_parameter * (upper_energy - lower_energy)
            + parent.cpoint(1j * parent.DEFAULT_ENERGY_DEFORMATION)
        )
        argument = parent.cpoint(1) - energy
        root = stable_principal_sqrt_nonreal(parent, argument)
        root_real_lower, root_real_upper = parent.M5394.real_bounds(root)
        root_imaginary_lower, root_imaginary_upper = parent.M5394.imaginary_bounds(root)
        argument_real_lower, argument_real_upper = parent.M5394.real_bounds(argument)
        argument_imaginary_lower, argument_imaginary_upper = (
            parent.M5394.imaginary_bounds(argument)
        )
        minimum_real_lower = min(minimum_real_lower, root_real_lower)
        for real_value in (
            argument_real_lower,
            0.5 * (argument_real_lower + argument_real_upper),
            argument_real_upper,
        ):
            for imaginary_value in (
                argument_imaginary_lower,
                0.5 * (argument_imaginary_lower + argument_imaginary_upper),
                argument_imaginary_upper,
            ):
                point_root = cmath.sqrt(complex(real_value, imaginary_value))
                tested_point_count += 1
                enclosed = (
                    root_real_lower <= point_root.real <= root_real_upper
                    and root_imaginary_lower
                    <= point_root.imag
                    <= root_imaginary_upper
                )
                all_points_enclosed = all_points_enclosed and enclosed
                if not enclosed:
                    point_failure_count += 1
                    if len(point_failure_examples) < 3:
                        point_failure_examples.append(
                            {
                                "argument_real": real_value,
                                "argument_imaginary": imaginary_value,
                                "root_real": point_root.real,
                                "root_imaginary": point_root.imag,
                                "enclosure_real_lower": root_real_lower,
                                "enclosure_real_upper": root_real_upper,
                                "enclosure_imaginary_lower": root_imaginary_lower,
                                "enclosure_imaginary_upper": root_imaginary_upper,
                            }
                        )
        tested_box_count += 1
    return {
        "recoil_sheet_enclosure_method": RECOIL_SHEET_METHOD,
        "recoil_sheet_tested_box_count": tested_box_count,
        "recoil_sheet_tested_point_count": tested_point_count,
        "recoil_sheet_minimum_real_lower": minimum_real_lower,
        "recoil_sheet_point_samples_enclosed": all_points_enclosed,
        "recoil_sheet_point_failure_count": point_failure_count,
        "recoil_sheet_point_failure_examples": point_failure_examples,
        "valid_for_stable_recoil_sheet_enclosure": (
            tested_box_count > 0
            and all_points_enclosed
            and math.isfinite(minimum_real_lower)
            and minimum_real_lower > 0.0
        ),
    }


def evaluate_representative(
    parent: Any,
    cells: dict[str, dict[str, str]],
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    row: dict[str, Any],
) -> dict[str, Any]:
    started = time.perf_counter()
    epsilon_row = {
        "regulator_bin_index": int(row["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(row["epsilon_subdivision_index"]),
        "epsilon_subdivision_count": int(row["epsilon_subdivision_count"]),
        "epsilon_real_lower": float(row["epsilon_real_lower"]),
        "epsilon_real_upper": float(row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
    }
    base = {
        "smoke_job_id": row["smoke_job_id"],
        "selection_role": row["selection_role"],
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "branch_owner_id": row["branch_owner_id"],
        "epsilon_bin_index": int(row["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(row["epsilon_subdivision_index"]),
        "epsilon_subdivision_count": int(row["epsilon_subdivision_count"]),
        "path_segment": row["path_segment"],
        "recoil_sheet_enclosure_method": RECOIL_SHEET_METHOD,
        "x_lower": float(row["x_lower"]),
        "x_upper": float(row["x_upper"]),
        "t_lower": float(row["t_lower"]),
        "t_upper": float(row["t_upper"]),
        "refinement_depth": int(row["refinement_depth"]),
        "refinement_path": row["refinement_path"],
        "geometry_gap_abs_lower": float(row["gap_abs_lower"]),
        "geometry_physical_path_area_abs_upper": float(
            row["physical_path_area_abs_upper"]
        ),
    }
    try:
        result = parent.evaluate_path_box(
            cells[row["mapped_cell_id"]],
            row["term_id"],
            parent.configuration_variants(row["term_id"]),
            epsilon_row,
            row["path_segment"],
            float(row["x_lower"]),
            float(row["x_upper"]),
            float(row["t_lower"]),
            float(row["t_upper"]),
            int(row["refinement_depth"]),
            f"5456:{row['refinement_path']}",
            support_segments,
            branches,
            GLOBAL_ARC_COUNT,
        )
        finite_values = (
            float(result["integrated_regular_path_abs_upper"]),
            float(result["minimum_amplitude_denominator_abs_lower"]),
            float(result["relative_root_abs_lower"]),
            float(result["selected_global_root_abs_lower"]),
            float(result["collision_jacobian_abs_lower"]),
        )
        reconstructed_area = float(result["parameter_area"]) * float(
            result["path_speed_abs_upper"]
        )
        area_error = abs(reconstructed_area - base["geometry_physical_path_area_abs_upper"])
        area_excess = max(
            0.0,
            reconstructed_area - base["geometry_physical_path_area_abs_upper"],
        )
        passed = (
            all(math.isfinite(value) and value > 0.0 for value in finite_values)
            and base["geometry_gap_abs_lower"] >= OUTER_RADIUS
            and area_excess
            <= 1.0e-14
            * max(base["geometry_physical_path_area_abs_upper"], 1.0)
        )
        return {
            **base,
            "probe_passed": passed,
            "failure_type": "",
            "failure_message": "",
            "integrated_regular_path_abs_upper": finite_values[0],
            "minimum_amplitude_denominator_abs_lower": finite_values[1],
            "relative_root_abs_lower": finite_values[2],
            "selected_global_root_abs_lower": finite_values[3],
            "collision_jacobian_abs_lower": finite_values[4],
            "active_material_branch_count": int(result["active_material_branch_count"]),
            "active_material_branch_ids": result["active_material_branch_ids"],
            "path_integral_enclosure_method": result[
                "path_integral_enclosure_method"
            ],
            "reconstructed_physical_path_area_abs_upper": reconstructed_area,
            "physical_path_area_absolute_error": area_error,
            "physical_path_area_excess": area_excess,
            "runtime_seconds": time.perf_counter() - started,
            "event_principal_pole_owned_separately": True,
            "valid_for_outer_parent_leaf_transplant_smoke": passed,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        return {
            **base,
            "probe_passed": False,
            "failure_type": type(error).__name__,
            "failure_message": str(error).splitlines()[0][:600],
            "integrated_regular_path_abs_upper": math.nan,
            "minimum_amplitude_denominator_abs_lower": math.nan,
            "relative_root_abs_lower": math.nan,
            "selected_global_root_abs_lower": math.nan,
            "collision_jacobian_abs_lower": math.nan,
            "active_material_branch_count": -1,
            "active_material_branch_ids": "",
            "path_integral_enclosure_method": "",
            "reconstructed_physical_path_area_abs_upper": math.nan,
            "physical_path_area_absolute_error": math.nan,
            "physical_path_area_excess": math.nan,
            "runtime_seconds": time.perf_counter() - started,
            "event_principal_pole_owned_separately": True,
            "valid_for_outer_parent_leaf_transplant_smoke": False,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }


def adaptive_evaluate_representative(
    parent: Any,
    cells: dict[str, dict[str, str]],
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    row: dict[str, Any],
) -> dict[str, Any]:
    started = time.perf_counter()
    original_x_lower = float(row["x_lower"])
    original_x_upper = float(row["x_upper"])
    original_t_lower = float(row["t_lower"])
    original_t_upper = float(row["t_upper"])
    original_area = (original_x_upper - original_x_lower) * (
        original_t_upper - original_t_lower
    )
    original_physical_area = float(row["physical_path_area_abs_upper"])
    stack = [
        (
            original_x_lower,
            original_x_upper,
            original_t_lower,
            original_t_upper,
            0,
            "R",
        )
    ]
    accepted: list[dict[str, Any]] = []
    refinement_witnesses: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    while stack:
        x_lower, x_upper, t_lower, t_upper, depth, refinement_path = stack.pop()
        local = dict(row)
        local.update(
            {
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "refinement_depth": depth,
                "refinement_path": refinement_path,
                "physical_path_area_abs_upper": original_physical_area
                * (x_upper - x_lower)
                * (t_upper - t_lower)
                / original_area,
            }
        )
        result = evaluate_representative(
            parent, cells, support_segments, branches, local
        )
        if result["probe_passed"]:
            accepted.append(result)
            continue
        refinement_witnesses.append(result)
        x_width = x_upper - x_lower
        t_width = t_upper - t_lower
        if depth >= 12 or (x_width <= 1.0e-12 and t_width <= 1.0e-10):
            unresolved.append(result)
            continue
        x_score = x_width / max(original_x_upper - original_x_lower, 1.0e-15)
        t_score = t_width / max(original_t_upper - original_t_lower, 1.0e-15)
        if x_score >= t_score and x_width > 1.0e-12:
            midpoint = 0.5 * (x_lower + x_upper)
            stack.append(
                (
                    midpoint,
                    x_upper,
                    t_lower,
                    t_upper,
                    depth + 1,
                    refinement_path + "R",
                )
            )
            stack.append(
                (
                    x_lower,
                    midpoint,
                    t_lower,
                    t_upper,
                    depth + 1,
                    refinement_path + "L",
                )
            )
        elif t_width > 1.0e-10:
            midpoint = 0.5 * (t_lower + t_upper)
            stack.append(
                (
                    x_lower,
                    x_upper,
                    midpoint,
                    t_upper,
                    depth + 1,
                    refinement_path + "U",
                )
            )
            stack.append(
                (
                    x_lower,
                    x_upper,
                    t_lower,
                    midpoint,
                    depth + 1,
                    refinement_path + "D",
                )
            )
        else:
            unresolved.append(result)
    base = {
        "smoke_job_id": row["smoke_job_id"],
        "selection_role": row["selection_role"],
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "branch_owner_id": row["branch_owner_id"],
        "epsilon_bin_index": int(row["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(row["epsilon_subdivision_index"]),
        "epsilon_subdivision_count": int(row["epsilon_subdivision_count"]),
        "path_segment": row["path_segment"],
        "x_lower": original_x_lower,
        "x_upper": original_x_upper,
        "t_lower": original_t_lower,
        "t_upper": original_t_upper,
        "geometry_gap_abs_lower": float(row["gap_abs_lower"]),
        "geometry_physical_path_area_abs_upper": original_physical_area,
    }
    passed = bool(accepted) and not unresolved
    reconstructed_area = sum(
        float(result["reconstructed_physical_path_area_abs_upper"])
        for result in accepted
    )
    return {
        **base,
        "probe_passed": passed,
        "failure_type": "" if passed else "AdaptiveOuterParentFailure",
        "failure_message": (
            ""
            if passed
            else "|".join(
                sorted(
                    {
                        f"{result['failure_type']}:{result['failure_message']}"
                        for result in unresolved
                    }
                )
            )[:1000]
        ),
        "integrated_regular_path_abs_upper": sum(
            float(result["integrated_regular_path_abs_upper"])
            for result in accepted
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            (
                float(result["minimum_amplitude_denominator_abs_lower"])
                for result in accepted
            ),
            default=math.nan,
        ),
        "relative_root_abs_lower": min(
            (float(result["relative_root_abs_lower"]) for result in accepted),
            default=math.nan,
        ),
        "selected_global_root_abs_lower": min(
            (
                float(result["selected_global_root_abs_lower"])
                for result in accepted
            ),
            default=math.nan,
        ),
        "collision_jacobian_abs_lower": min(
            (
                float(result["collision_jacobian_abs_lower"])
                for result in accepted
            ),
            default=math.nan,
        ),
        "active_material_branch_count": max(
            (int(result["active_material_branch_count"]) for result in accepted),
            default=-1,
        ),
        "active_material_branch_ids": "|".join(
            sorted(
                {
                    branch_id
                    for result in accepted
                    for branch_id in str(result["active_material_branch_ids"]).split("|")
                    if branch_id
                }
            )
        ),
        "path_integral_enclosure_method": "|".join(
            sorted(
                {
                    str(result["path_integral_enclosure_method"])
                    for result in accepted
                }
            )
        ),
        "reconstructed_physical_path_area_abs_upper": reconstructed_area,
        "physical_path_area_absolute_error": abs(
            reconstructed_area - original_physical_area
        ),
        "physical_path_area_excess": max(
            0.0, reconstructed_area - original_physical_area
        ),
        "adaptive_subleaf_count": len(accepted),
        "refinement_witness_count": len(refinement_witnesses),
        "maximum_refinement_depth": max(
            (
                int(result.get("refinement_depth", 0))
                for result in accepted + unresolved
            ),
            default=0,
        ),
        "unresolved_subleaf_count": len(unresolved),
        "runtime_seconds": time.perf_counter() - started,
        "event_principal_pole_owned_separately": True,
        "valid_for_outer_parent_leaf_transplant_smoke": passed,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    if payload["valid_for_outer_parent_leaf_transplant_smoke"]:
        claim_boundary = (
            "This validates the outer-parent evaluator transplant on broad and "
            "near-switch leaves. It does not yet aggregate all 606,990 outer "
            "geometry leaves or prove the regular-plus-principal combination."
        )
    else:
        claim_boundary = (
            "This is a resumable partial smoke, not a transplant validation. "
            f"It has completed {payload['completed_probe_count']}/"
            f"{payload['representative_job_count']} representatives. The next "
            "broad TOP leaf requires a finite projective-pivot cover; blind "
            "rectangular refinement is not accepted as the solution."
        )
    lines = [
        "# 5456: D4 outer-parent leaf transplant smoke",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Executable seam",
        "",
        "The full inner-Q cover is complete. The outer geometry leaves therefore move to the checkpoint-5396 `evaluate_path_box` regular enclosure, augmented only by the derived stable deformed-recoil sheet chart below. The event principal pole is not reassigned to this evaluator: its exact `rho/delta` subtraction and logarithmic primitive remain owned by checkpoints 5450-5451.",
        "",
        "For the deformed TOP contour, write `z=1-E=a+ib`, with `b` uniformly nonzero. The principal square root is `sqrt(z)=u+iv`, where `u^2=(sqrt(a^2+b^2)+a)/2` and `|v|^2=(sqrt(a^2+b^2)-a)/2`. Here `u` increases with `a` and `|b|`, while `|v|` decreases with `a` and increases with `|b|`. Directed endpoint evaluation therefore gives a rigorous positive-real-sheet rectangle and removes the inherited interval-wrapping false negative without adding a physical assumption.",
        "",
        f"The smoke selects both the maximum physical-path-area leaf and the minimum certified-gap leaf in every owner-cell/path group. It covers `{payload['representative_job_count']}` representatives across `{payload['owner_cell_term_count']}` owner cells and all three contour segments. Passed: `{payload['passed_probe_count']}/{payload['completed_probe_count']}`.",
        "",
        "## Claim boundary",
        "",
        claim_boundary + " Full event-cell coverage, event-local W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(max_jobs: int, status_only: bool = False) -> dict[str, Any]:
    set_below_normal_priority()
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5449 = read_json(RESULT_5449)
    result_5450 = read_json(RESULT_5450)
    result_5451 = read_json(RESULT_5451)
    result_5455 = read_json(RESULT_5455)
    if result_5449.get("valid_for_D4_event_local_interior_smoke") is not True:
        raise RuntimeError("checkpoint 5449 parent evaluator smoke is not valid")
    if result_5450.get("valid_for_exact_endpoint_principal_part_subtraction") is not True:
        raise RuntimeError("checkpoint 5450 principal subtraction is not valid")
    if result_5451.get("valid_for_endpoint_xt_overlap_geometry_atlas") is not True:
        raise RuntimeError("checkpoint 5451 geometry atlas is not valid")
    if result_5455.get("valid_for_correlated_inner_Q_full_cover") is not True:
        raise RuntimeError("checkpoint 5455 inner-Q cover is not complete")
    representatives, diagnostics = representative_rows()
    atomic_csv(REPRESENTATIVES, representatives)
    WORK.mkdir(parents=True, exist_ok=True)
    module_5449 = load_module("mts_5449_for_5456", SCRIPT_5449)
    parent = load_module("mts_5396_for_5456", module_5449.PARENT_SCRIPT)
    parent.set_below_normal_priority()
    cells = {row["mapped_cell_id"]: row for row in parent.read_csv(parent.MAPPED_5393)}
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    recoil_sheet_diagnostics = validate_stable_recoil_sheet(
        parent, representatives
    )
    if not recoil_sheet_diagnostics[
        "valid_for_stable_recoil_sheet_enclosure"
    ]:
        raise RuntimeError(
            "stable deformed-recoil sheet enclosure is not valid: "
            + json.dumps(recoil_sheet_diagnostics, sort_keys=True)
        )
    install_stable_recoil_sheet(parent)
    processed = 0
    for row in representatives:
        path = WORK / f"{row['smoke_job_id']}.json"
        if path.is_file():
            continue
        if status_only:
            break
        if max_jobs > 0 and processed >= max_jobs:
            break
        atomic_json(
            path,
            adaptive_evaluate_representative(
                parent, cells, support_segments, branches, row
            ),
            compact=True,
        )
        processed += 1
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "updated_utc": datetime.now(timezone.utc).isoformat(),
                "processed_this_run": processed,
                "last_job_id": row["smoke_job_id"],
            },
        )
    completed = []
    for row in representatives:
        path = WORK / f"{row['smoke_job_id']}.json"
        if not path.is_file():
            continue
        completed_row = read_json(path)
        completed_row.setdefault(
            "recoil_sheet_enclosure_method",
            "PARENT_INTERVAL_SQRT_FALLBACK",
        )
        completed.append(completed_row)
    passed = [row for row in completed if row["probe_passed"]]
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = {}
    for row in completed:
        key = (
            row["event_id"],
            row["mapped_cell_id"],
            row["term_id"],
            row["path_segment"],
        )
        groups.setdefault(key, []).append(row)
    owner_summaries = [
        {
            "event_id": key[0],
            "mapped_cell_id": key[1],
            "term_id": key[2],
            "path_segment": key[3],
            "probe_count": len(rows),
            "passed_probe_count": sum(row["probe_passed"] for row in rows),
            "minimum_geometry_gap_abs_lower": min(
                float(row["geometry_gap_abs_lower"]) for row in rows
            ),
            "maximum_integrated_regular_path_abs_upper": max(
                (
                    float(row["integrated_regular_path_abs_upper"])
                    for row in rows
                    if row["probe_passed"]
                ),
                default=math.nan,
            ),
            "minimum_amplitude_denominator_abs_lower": min(
                (
                    float(row["minimum_amplitude_denominator_abs_lower"])
                    for row in rows
                    if row["probe_passed"]
                ),
                default=math.nan,
            ),
            "valid_for_outer_parent_leaf_transplant_smoke": all(
                row["probe_passed"] for row in rows
            ),
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for key, rows in sorted(groups.items())
    ]
    if completed:
        atomic_csv(SMOKE, completed)
    if owner_summaries:
        atomic_csv(OWNER_SUMMARY, owner_summaries)
    complete = len(completed) == len(representatives)
    all_pass = complete and len(passed) == len(representatives)
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "OUTER_PARENT_LEAF_TRANSPLANT_PASSES__DERIVE_FULL_REGULAR_PLUS_PRINCIPAL_AGGREGATION"
            if all_pass
            else (
                "OUTER_PARENT_LEAF_TRANSPLANT_EXPOSES_FAILURES"
                if complete
                else "OUTER_PARENT_TRANSPLANT_PARTIAL__TOP_PROJECTIVE_PIVOT_COVER_REQUIRED"
            )
        ),
        **diagnostics,
        **recoil_sheet_diagnostics,
        "completed_probe_count": len(completed),
        "remaining_probe_count": len(representatives) - len(completed),
        "passed_probe_count": len(passed),
        "failed_probe_count": len(completed) - len(passed),
        "processed_this_run": processed,
        "minimum_geometry_gap_abs_lower": min(
            (float(row["geometry_gap_abs_lower"]) for row in completed),
            default=math.nan,
        ),
        "maximum_integrated_regular_path_abs_upper": max(
            (
                float(row["integrated_regular_path_abs_upper"])
                for row in passed
            ),
            default=math.nan,
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            (
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in passed
            ),
            default=math.nan,
        ),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": (
            "FULL_OUTER_REGULAR_PLUS_PRINCIPAL_AGGREGATION_CONTRACT"
            if all_pass
            else "TOP_CONTOUR_FINITE_PROJECTIVE_PIVOT_COVER"
        ),
        "valid_for_outer_parent_leaf_transplant_smoke": all_pass,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5449_parent_smoke_is_valid", result_5449.get("valid_for_D4_event_local_interior_smoke") is True, result_5449.get("decision")),
        check("checkpoint_5450_principal_subtraction_is_valid", result_5450.get("valid_for_exact_endpoint_principal_part_subtraction") is True, result_5450.get("decision")),
        check("checkpoint_5451_geometry_atlas_is_valid", result_5451.get("valid_for_endpoint_xt_overlap_geometry_atlas") is True, result_5451.get("decision")),
        check("checkpoint_5455_inner_Q_cover_is_complete", result_5455.get("valid_for_correlated_inner_Q_full_cover") is True, result_5455.get("decision")),
        check("all_606990_outer_geometry_leaves_are_seen", diagnostics["outer_geometry_leaf_count"] == int(result_5451["outer_leaf_count"]), f"{diagnostics['outer_geometry_leaf_count']}/{result_5451['outer_leaf_count']}"),
        check("all_13_owner_cells_and_39_owner_paths_are_represented", diagnostics["owner_cell_term_count"] == 13 and diagnostics["owner_path_group_count"] == 39, f"{diagnostics['owner_cell_term_count']}/{diagnostics['owner_path_group_count']}"),
        check("stable_deformed_recoil_sheet_enclosure_is_valid", recoil_sheet_diagnostics["valid_for_stable_recoil_sheet_enclosure"], f"boxes={recoil_sheet_diagnostics['recoil_sheet_tested_box_count']};points={recoil_sheet_diagnostics['recoil_sheet_tested_point_count']};minimum_real_lower={recoil_sheet_diagnostics['recoil_sheet_minimum_real_lower']}"),
        check("all_completed_representatives_obey_outer_gap", all(float(row["geometry_gap_abs_lower"]) >= OUTER_RADIUS for row in completed), min((float(row["geometry_gap_abs_lower"]) for row in completed), default=math.nan)),
        check("all_completed_parent_enclosures_pass", len(passed) == len(completed), f"{len(passed)}/{len(completed)}"),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "transplant smoke only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--status-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.max_jobs, arguments.status_only)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
