from __future__ import annotations

import argparse
import cmath
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
import traceback
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True


CHECKPOINT = 5339
MARKER = "MTS_5339_D4_E08_SUPPORT_EXIT_LOG_SUBTRACTION"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
RESULT = OUT / "D4_E08_support_exit_log_subtraction_result.json"
STATUS = OUT / "status.json"
SOURCE_REGISTER = OUT / "source_register.csv"
STENCIL = OUT / "E08_parent_endpoint_coefficient_stencil.csv"
COEFFICIENTS = OUT / "E08_parent_endpoint_coefficients.csv"
NODE_AUDIT = OUT / "E08_log_subtraction_node_audit.csv"
QUADRATURE = OUT / "E08_log_subtracted_quadrature.csv"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EVENT_ID = "E08"
TARGET_PANEL = "P12S02LLLL"
TARGET_PARENT = "P12S02LLL"
TERM_ID = "MC04_SM_DM"
SURFACE_ID = "direct:shared:s13"
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_ERROR_BUDGET_LIMIT = 1.0e-2
DERIVATIVE_RELATIVE_STABILITY_LIMIT = 2.5e-2
MODEL_ENDPOINT_RELATIVE_RESIDUAL_LIMIT = 5.0e-3
ONE_SIDED_TRACE_RELATIVE_MISMATCH_LIMIT = 1.0e-5
CLAIM_FIELDS = (
    "valid_for_E08_parent_endpoint_coefficients",
    "valid_for_E08_log_subtraction",
    "valid_for_D4_outer_E0025_fixed_decay_integral",
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


M5334 = load_module("mts_5334_for_5339", SCRIPT_5334)
M5326 = M5334.M5326
M5312 = M5326.M5312
M5283 = M5334.M5283


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(first), abs(second), 1.0e-300)


def configure() -> dict[str, Any]:
    M5334.configure_refinement("E0025")
    return M5326.configure_kernel()


def source_paths() -> list[Path]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5334,
        SCRIPTS / "Y5_R2FR_5326_D2_midpoint_event_aligned_E0025_refinement.py",
        SCRIPTS / "Y5_R2FR_5338_D4_E0025_targeted_support_exit_depth4_refinement.py",
        POST / "5338-Y5-R2FR-D4-E0025-targeted-support-exit-depth4-refinement.md",
        POST / "5339-Y5-R2FR-D4-E08-support-exit-log-subtraction.md",
        POST / "source-intake/functional_rg/5338/D4_E0025_targeted_depth4_result.json",
        POST / "source-intake/mts_residuals/P8_Y5_BRR545_5338_VALIDATION.csv",
        M5326.EVENTS,
        M5326.CONTRACT_5325,
        M5326.ADAPTIVE_PANELS,
        M5326.NODE_MANIFEST,
        M5326.RESULT,
        M5326.FINITE_VALUE,
    ]
    return [Path(path) for path in paths]


def write_source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in source_paths():
        rows.append(
            {
                "path": str(path.resolve()),
                "sha256": digest(path) if path.is_file() else "MISSING",
                "exists": path.is_file(),
                **no_claims(),
            }
        )
    write_csv(SOURCE_REGISTER, rows)
    return rows


def event_row() -> dict[str, str]:
    rows = [row for row in read_csv(M5326.EVENTS) if row["event_id"] == EVENT_ID]
    if len(rows) != 1:
        raise RuntimeError(f"expected one {EVENT_ID} row, found {len(rows)}")
    return rows[0]


def endpoint_state(
    coordinate: float,
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    label: str,
) -> dict[str, Any]:
    panel_index = 12
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells).get(TERM_ID, [])
    node = {
        "node_id": f"E08_ENDPOINT_{label}",
        "x_panel_index": panel_index,
        "outer_order": 0,
        "absolute_soft_cosine": coordinate,
    }
    poles = [
        row
        for row in M5312.scan_term_poles(node, TERM_ID, supports)
        if row["primary_surface_id"] == SURFACE_ID
    ]
    if len(poles) != 1:
        raise RuntimeError(f"expected one endpoint pole at {coordinate}, found {len(poles)}")
    geometric = poles[0]
    _, support = M5326.support_margin(float(geometric["pole_real"]), supports)
    source = {
        **geometric,
        "support_id": support["support_id"],
        "support_energy_lower": support["lower"],
        "support_energy_upper": support["upper"],
        "support_contract_indices": "|".join(
            str(value) for value in support["contracts"]
        ),
    }
    evaluator = M5326.near_support_unmasked_evaluator(base_context, TERM_ID)
    selected, fits = M5326.refine_near_support_simple_pole(
        coordinate, source, evaluator
    )
    pole = complex(selected["refined_pole"])
    residue = complex(selected["selected_residue"])
    coefficient = multiplier * residue
    lower = float(selected["support_energy_lower"])
    upper = float(selected["support_energy_upper"])
    lower_gap = complex(lower, 0.0) - pole
    return {
        "stencil_label": label,
        "absolute_soft_cosine": coordinate,
        "support_id": source["support_id"],
        "term_id": TERM_ID,
        "primary_surface_id": SURFACE_ID,
        "fit_contract_passes": bool(selected["fit_contract_passes"]),
        "fit_relative_residual": float(selected["fit_relative_residual"]),
        "residue_scale_relative_change": float(
            selected["residue_fit_scale_relative_change"]
        ),
        "second_order_suppression_ratio": float(
            selected["second_order_suppression_ratio"]
        ),
        "fit_row_count": len(fits),
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        **complex_fields("refined_pole", pole),
        **complex_fields("endpoint_residue", residue),
        **complex_fields("physical_endpoint_coefficient", coefficient),
        **complex_fields("lower_gap", lower_gap),
        **no_claims(),
    }


def complex_from(row: dict[str, Any], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def endpoint_stencil() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    event = event_row()
    coordinate = float(event["event_coordinate"])
    slope = float(event["source_crossing_slope"])
    geometric_gamma = abs(float(event.get("event_pole_imaginary", 0.0) or 0.0))
    if geometric_gamma == 0.0:
        nearest = read_json(
            M5326.SHARDS
            / "P12_P12S02LLLL_Q08_N01"
            / "result.json"
        )
        geometric_gamma = float(nearest["near_support_distance"]) / float(
            nearest["near_support_distance_in_core_units"]
        )
    boundary_scale = geometric_gamma / abs(slope)
    derivative_step = max(0.25 * boundary_scale, 64.0 * float(event["event_coordinate_error_estimate"]))
    half_step = 0.5 * derivative_step
    offsets = (
        ("M1", -derivative_step),
        ("MH", -half_step),
        ("C0", 0.0),
        ("PH", half_step),
        ("P1", derivative_step),
    )
    contract = read_csv(M5326.CONTRACT_5325)
    base_context = M5312.M5303.synthetic_context()
    multiplier = float(M5312.M5309.physical_multiplier())
    rows = [
        endpoint_state(
            coordinate + offset,
            contract,
            base_context,
            multiplier,
            label,
        )
        for label, offset in offsets
    ]
    for row, (_, offset) in zip(rows, offsets):
        row["delta_from_event"] = offset
        row["physical_multiplier"] = multiplier
        row["geometric_event_slope"] = slope
        row["geometric_gamma_seed"] = geometric_gamma
        row["boundary_layer_scale_seed"] = boundary_scale
    by_label = {row["stencil_label"]: row for row in rows}
    center = by_label["C0"]
    minus = by_label["M1"]
    plus = by_label["P1"]
    minus_half = by_label["MH"]
    plus_half = by_label["PH"]
    center_z0 = complex_from(center, "lower_gap")
    center_coefficient0 = complex_from(center, "physical_endpoint_coefficient")
    z0_left = (
        2.0 * complex_from(minus_half, "lower_gap")
        - complex_from(minus, "lower_gap")
    )
    z0_right = (
        2.0 * complex_from(plus_half, "lower_gap")
        - complex_from(plus, "lower_gap")
    )
    coefficient0_left = (
        2.0 * complex_from(minus_half, "physical_endpoint_coefficient")
        - complex_from(minus, "physical_endpoint_coefficient")
    )
    coefficient0_right = (
        2.0 * complex_from(plus_half, "physical_endpoint_coefficient")
        - complex_from(plus, "physical_endpoint_coefficient")
    )
    z0 = 0.5 * (z0_left + z0_right)
    coefficient0 = 0.5 * (coefficient0_left + coefficient0_right)
    z1_full = (
        complex_from(plus, "lower_gap") - complex_from(minus, "lower_gap")
    ) / (2.0 * derivative_step)
    z1_half = (
        complex_from(plus_half, "lower_gap")
        - complex_from(minus_half, "lower_gap")
    ) / derivative_step
    coefficient1_full = (
        complex_from(plus, "physical_endpoint_coefficient")
        - complex_from(minus, "physical_endpoint_coefficient")
    ) / (2.0 * derivative_step)
    coefficient1_half = (
        complex_from(plus_half, "physical_endpoint_coefficient")
        - complex_from(minus_half, "physical_endpoint_coefficient")
    ) / derivative_step
    z_derivative_change = relative_complex_change(z1_full, z1_half)
    coefficient_derivative_change = relative_complex_change(
        coefficient1_full, coefficient1_half
    )
    z_trace_mismatch = relative_complex_change(z0_left, z0_right)
    coefficient_trace_mismatch = relative_complex_change(
        coefficient0_left, coefficient0_right
    )
    exact_selector_to_trace_ratio = abs(center_coefficient0) / max(
        abs(coefficient0), 1.0e-300
    )
    context = {
        "event": event,
        "event_coordinate": coordinate,
        "derivative_step": derivative_step,
        "physical_multiplier": multiplier,
        "center_z0": center_z0,
        "center_coefficient0": center_coefficient0,
        "z0_left": z0_left,
        "z0_right": z0_right,
        "coefficient0_left": coefficient0_left,
        "coefficient0_right": coefficient0_right,
        "z0": z0,
        "z1": z1_half,
        "coefficient0": coefficient0,
        "coefficient1": coefficient1_half,
        "z_derivative_change": z_derivative_change,
        "coefficient_derivative_change": coefficient_derivative_change,
        "z_trace_mismatch": z_trace_mismatch,
        "coefficient_trace_mismatch": coefficient_trace_mismatch,
        "exact_selector_to_trace_ratio": exact_selector_to_trace_ratio,
        "boundary_layer_scale": abs(z0.imag) / max(abs(z1_half.real), 1.0e-300),
        "stencil_contract_passes": all(
            bool(row["fit_contract_passes"]) for row in rows
        ),
    }
    write_csv(STENCIL, rows)
    coefficient_row = {
        "event_id": EVENT_ID,
        "event_coordinate": coordinate,
        "derivative_step": derivative_step,
        **complex_fields("exact_selector_lower_gap", center_z0),
        **complex_fields("exact_selector_physical_coefficient", center_coefficient0),
        **complex_fields("left_trace_lower_gap_z0", z0_left),
        **complex_fields("right_trace_lower_gap_z0", z0_right),
        **complex_fields("left_trace_physical_coefficient_C0", coefficient0_left),
        **complex_fields("right_trace_physical_coefficient_C0", coefficient0_right),
        **complex_fields("lower_gap_z0", z0),
        **complex_fields("lower_gap_derivative_z1", z1_half),
        **complex_fields("physical_coefficient_C0", coefficient0),
        **complex_fields("physical_coefficient_derivative_C1", coefficient1_half),
        "z_derivative_relative_change_full_vs_half": z_derivative_change,
        "coefficient_derivative_relative_change_full_vs_half": coefficient_derivative_change,
        "lower_gap_trace_relative_mismatch": z_trace_mismatch,
        "physical_coefficient_trace_relative_mismatch": coefficient_trace_mismatch,
        "exact_selector_to_one_sided_trace_ratio": exact_selector_to_trace_ratio,
        "boundary_layer_scale": context["boundary_layer_scale"],
        "all_stencil_fit_contracts_pass": context["stencil_contract_passes"],
        **no_claims(),
    }
    write_csv(COEFFICIENTS, [coefficient_row])
    return rows, context


def linear_log_value(
    delta: float,
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
) -> complex:
    return -(coefficient0 + coefficient1 * delta) * cmath.log(z0 + z1 * delta)


def linear_log_primitive(
    upper: float,
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
) -> complex:
    if abs(z1) <= 1.0e-300:
        raise ZeroDivisionError("endpoint lower-gap derivative vanishes")
    affine_z_coefficient = coefficient1 / z1
    constant_z_coefficient = coefficient0 - affine_z_coefficient * z0

    def primitive_z(z: complex) -> complex:
        return (
            constant_z_coefficient * (z * cmath.log(z) - z)
            + affine_z_coefficient
            * (0.5 * z * z * cmath.log(z) - 0.25 * z * z)
        ) / z1

    return -(primitive_z(z0 + z1 * upper) - primitive_z(z0))


def shard_result(node_id: str) -> dict[str, Any]:
    return read_json(M5326.SHARDS / node_id / "result.json")


def subtraction_test(context: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    panels = read_csv(M5326.ADAPTIVE_PANELS)
    panel = next(row for row in panels if row["adaptive_panel_id"] == TARGET_PANEL)
    manifest = [
        row
        for row in read_csv(M5326.NODE_MANIFEST)
        if row["adaptive_panel_id"] == TARGET_PANEL
    ]
    if len(manifest) != 12:
        raise RuntimeError(f"expected 12 target nodes, found {len(manifest)}")
    x0 = float(context["event_coordinate"])
    coefficient0 = complex(context["coefficient0"])
    coefficient1 = complex(context["coefficient1"])
    z0 = complex(context["z0"])
    z1 = complex(context["z1"])
    rows: list[dict[str, Any]] = []
    totals: dict[int, dict[str, complex]] = {
        4: {"raw": 0.0j, "model": 0.0j, "regular": 0.0j},
        8: {"raw": 0.0j, "model": 0.0j, "regular": 0.0j},
    }
    for node in manifest:
        result = shard_result(node["node_id"])
        coordinate = float(node["absolute_soft_cosine"])
        delta = coordinate - x0
        weight = float(node["mapped_outer_weight"])
        order = int(node["outer_order"])
        raw = complex(
            float(result["inner_energy_Q8_real"]),
            float(result["inner_energy_Q8_imaginary"]),
        )
        model = linear_log_value(
            delta, coefficient0, coefficient1, z0, z1
        )
        regular = raw - model
        totals[order]["raw"] += weight * raw
        totals[order]["model"] += weight * model
        totals[order]["regular"] += weight * regular
        rows.append(
            {
                "node_id": node["node_id"],
                "outer_order": order,
                "absolute_soft_cosine": coordinate,
                "delta_from_event": delta,
                "mapped_outer_weight": weight,
                **complex_fields("raw_inner_Q8", raw),
                **complex_fields("subtracted_log_model", model),
                **complex_fields("regular_remainder", regular),
                **no_claims(),
            }
        )
    width = float(panel["upper_absolute_soft_cosine"]) - float(
        panel["lower_absolute_soft_cosine"]
    )
    exact_model = linear_log_primitive(
        width, coefficient0, coefficient1, z0, z1
    )
    quadrature_rows: list[dict[str, Any]] = []
    reconstructed: dict[int, complex] = {}
    for order in (4, 8):
        reconstructed[order] = totals[order]["regular"] + exact_model
        quadrature_rows.append(
            {
                "outer_order": order,
                "panel_id": TARGET_PANEL,
                "panel_width": width,
                **complex_fields("raw_panel_integral", totals[order]["raw"]),
                **complex_fields("quadrature_log_model", totals[order]["model"]),
                **complex_fields("regular_remainder_integral", totals[order]["regular"]),
                **complex_fields("exact_log_model_integral", exact_model),
                **complex_fields("reconstructed_panel_integral", reconstructed[order]),
                **no_claims(),
            }
        )
    raw_change = relative_complex_change(totals[4]["raw"], totals[8]["raw"])
    regular_change = relative_complex_change(
        totals[4]["regular"], totals[8]["regular"]
    )
    reconstructed_change = relative_complex_change(
        reconstructed[4], reconstructed[8]
    )
    parent_q4 = complex(
        float(panel["outer_Q4_inner_Q8_real"]),
        float(panel["outer_Q4_inner_Q8_imaginary"]),
    )
    parent_q8 = complex(
        float(panel["outer_Q8_inner_Q8_real"]),
        float(panel["outer_Q8_inner_Q8_imaginary"]),
    )
    raw_reproduction_error = max(
        relative_complex_change(parent_q4, totals[4]["raw"]),
        relative_complex_change(parent_q8, totals[8]["raw"]),
    )
    model_q8_error = relative_complex_change(
        totals[8]["model"], exact_model
    )
    result = {
        "panel": panel,
        "width": width,
        "raw_q4": totals[4]["raw"],
        "raw_q8": totals[8]["raw"],
        "regular_q4": totals[4]["regular"],
        "regular_q8": totals[8]["regular"],
        "exact_model": exact_model,
        "reconstructed_q4": reconstructed[4],
        "reconstructed_q8": reconstructed[8],
        "raw_change": raw_change,
        "regular_change": regular_change,
        "reconstructed_change": reconstructed_change,
        "raw_reproduction_error": raw_reproduction_error,
        "model_q8_error": model_q8_error,
    }
    write_csv(NODE_AUDIT, rows)
    write_csv(QUADRATURE, quadrature_rows)
    return rows, quadrature_rows, result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    M5312.set_below_normal_priority()
    M5326.MAXIMUM_ADAPTIVE_DEPTH = 4
    old = configure()
    try:
        sources = write_source_register()
        stencil, context = endpoint_stencil()
        nodes, quadrature, subtraction = subtraction_test(context)
    finally:
        M5326.restore_kernel(old)
    parent_result = read_json(M5326.RESULT)
    parent_validation = read_csv(M5326.VALIDATION)
    parent_5338 = read_json(
        POST / "source-intake/functional_rg/5338/D4_E0025_targeted_depth4_result.json"
    )
    z0 = complex(context["z0"])
    z1 = complex(context["z1"])
    coefficient0 = complex(context["coefficient0"])
    event_coordinate_error = float(context["event"]["event_coordinate_error_estimate"])
    endpoint_coordinate_sensitivity = abs(coefficient0) * abs(z1 / z0) * event_coordinate_error
    reconstructed_local_error = abs(
        subtraction["reconstructed_q8"] - subtraction["reconstructed_q4"]
    )
    corrected_value = complex(
        float(parent_result["fixed_decay_integral_real"]),
        float(parent_result["fixed_decay_integral_imaginary"]),
    ) + (subtraction["reconstructed_q8"] - subtraction["raw_q8"])
    corrected_outer_error = (
        float(parent_result["outer_error_absolute_conservative"])
        - float(subtraction["panel"]["outer_Q4_Q8_absolute_change"])
        + reconstructed_local_error
    )
    corrected_total_error = corrected_outer_error + float(
        parent_result["inner_error_absolute_conservative"]
    ) + endpoint_coordinate_sensitivity
    corrected_relative_error = corrected_total_error / max(abs(corrected_value), 1.0e-300)
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            bool(sources)
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5338_blocker_is_exactly_target_leaf",
            parent_5338.get("validation_passed") is False
            and parent_5338.get("next_action")
            == "DERIVE_P12S02_SUPPORT_EXIT_ENDPOINT_ASYMPTOTIC"
            and sum(not parse_bool(row["passed"]) for row in parent_validation) == 2,
            str(parent_5338.get("decision")),
        ),
        validation_row(
            "E08_parent_event_contract_passes",
            context["event"]["event_id"] == EVENT_ID
            and context["event"]["term_id"] == TERM_ID
            and context["event"]["primary_surface_id"] == SURFACE_ID
            and parse_bool(context["event"]["event_contract_passes"]),
            str(context["event"]["event_coordinate"]),
        ),
        validation_row(
            "all_five_parent_endpoint_fits_pass",
            len(stencil) == 5
            and bool(context["stencil_contract_passes"])
            and all(
                float(row["fit_relative_residual"])
                <= M5326.NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT
                for row in stencil
            ),
            f"rows={len(stencil)}",
        ),
        validation_row(
            "left_and_right_one_sided_endpoint_traces_agree",
            float(context["z_trace_mismatch"])
            <= ONE_SIDED_TRACE_RELATIVE_MISMATCH_LIMIT
            and float(context["coefficient_trace_mismatch"])
            <= ONE_SIDED_TRACE_RELATIVE_MISMATCH_LIMIT,
            (
                f"z={context['z_trace_mismatch']};"
                f"C={context['coefficient_trace_mismatch']}"
            ),
        ),
        validation_row(
            "exact_crossing_selector_is_excluded_as_measure_zero_trace",
            float(context["exact_selector_to_trace_ratio"]) <= 1.0e-8,
            str(context["exact_selector_to_trace_ratio"]),
        ),
        validation_row(
            "lower_gap_derivative_is_stable",
            float(context["z_derivative_change"])
            <= DERIVATIVE_RELATIVE_STABILITY_LIMIT,
            str(context["z_derivative_change"]),
        ),
        validation_row(
            "physical_residue_derivative_is_stable",
            float(context["coefficient_derivative_change"])
            <= DERIVATIVE_RELATIVE_STABILITY_LIMIT,
            str(context["coefficient_derivative_change"]),
        ),
        validation_row(
            "endpoint_gap_is_regulator_resolved_and_nonzero",
            abs(z0.imag) > 0.0
            and abs(z0) > 100.0 * event_coordinate_error * abs(z1),
            f"z0={z0};coordinate_error={event_coordinate_error}",
        ),
        validation_row(
            "existing_raw_panel_is_reproduced_exactly",
            float(subtraction["raw_reproduction_error"]) <= 5.0e-13,
            str(subtraction["raw_reproduction_error"]),
        ),
        validation_row(
            "analytic_model_improves_its_own_Q8_error",
            float(subtraction["model_q8_error"])
            < float(subtraction["raw_change"]),
            f"model={subtraction['model_q8_error']};raw={subtraction['raw_change']}",
        ),
        validation_row(
            "log_subtracted_reconstructed_panel_passes_local_gate",
            float(subtraction["reconstructed_change"])
            <= LOCAL_OUTER_CHANGE_LIMIT,
            str(subtraction["reconstructed_change"]),
        ),
        validation_row(
            "corrected_global_conservative_budget_passes",
            corrected_relative_error <= GLOBAL_ERROR_BUDGET_LIMIT,
            str(corrected_relative_error),
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    method_claims = no_claims()
    coefficient_gates = {
        "E08_parent_event_contract_passes",
        "all_five_parent_endpoint_fits_pass",
        "left_and_right_one_sided_endpoint_traces_agree",
        "exact_crossing_selector_is_excluded_as_measure_zero_trace",
        "lower_gap_derivative_is_stable",
        "physical_residue_derivative_is_stable",
        "endpoint_gap_is_regulator_resolved_and_nonzero",
    }
    method_claims["valid_for_E08_parent_endpoint_coefficients"] = all(
        parse_bool(row["passed"])
        for row in gates
        if row["gate"] in coefficient_gates
    )
    method_claims["valid_for_E08_log_subtraction"] = passed
    write_csv(VALIDATION, gates)
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E08-parent-log-subtraction",
        "validation_passed": passed,
        "decision": (
            "D4_E08_PARENT_LOG_SUBTRACTION_PASSES__INTEGRATE_INTO_E0025_ENGINE"
            if passed
            else "D4_E08_PARENT_LOG_SUBTRACTION_BLOCKED__REFINE_PARENT_NORMAL_FORM"
        ),
        "event_id": EVENT_ID,
        "event_coordinate": context["event_coordinate"],
        "derivative_step": context["derivative_step"],
        "boundary_layer_scale": context["boundary_layer_scale"],
        "lower_gap_trace_relative_mismatch": context["z_trace_mismatch"],
        "physical_coefficient_trace_relative_mismatch": context[
            "coefficient_trace_mismatch"
        ],
        "exact_selector_to_one_sided_trace_ratio": context[
            "exact_selector_to_trace_ratio"
        ],
        **complex_fields("lower_gap_z0", z0),
        **complex_fields("lower_gap_derivative_z1", z1),
        **complex_fields("physical_coefficient_C0", coefficient0),
        **complex_fields("physical_coefficient_derivative_C1", complex(context["coefficient1"])),
        "raw_target_panel_Q4_Q8_relative_change": subtraction["raw_change"],
        "regular_remainder_Q4_Q8_relative_change": subtraction["regular_change"],
        "reconstructed_target_panel_Q4_Q8_relative_change": subtraction[
            "reconstructed_change"
        ],
        "analytic_model_Q8_relative_error": subtraction["model_q8_error"],
        **complex_fields("raw_target_panel_Q8", subtraction["raw_q8"]),
        **complex_fields("exact_log_model_integral", subtraction["exact_model"]),
        **complex_fields("reconstructed_target_panel_Q8", subtraction["reconstructed_q8"]),
        **complex_fields("corrected_fixed_decay_integral", corrected_value),
        "corrected_outer_error_absolute_conservative": corrected_outer_error,
        "endpoint_coordinate_error_absolute_conservative": endpoint_coordinate_sensitivity,
        "corrected_total_error_absolute_conservative": corrected_total_error,
        "corrected_total_error_relative_conservative": corrected_relative_error,
        "claim_boundary": method_claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": (
            "INTEGRATE_E08_LINEAR_LOG_SUBTRACTION_INTO_D4_E0025_PARENT_ENGINE"
            if passed
            else "DERIVE_QUADRATIC_OR_EXACT_SOURCE_COEFFICIENT_ENDPOINT_MODEL"
        ),
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(RESULT, value)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": value["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    arguments = parser.parse_args()
    M5312.set_below_normal_priority()
    try:
        value = execute()
    except Exception as error:
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "state": "FAILED",
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "updated_utc": utc_now(),
            },
        )
        raise
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "mode": arguments.mode,
                "validation_passed": value["validation_passed"],
                "decision": value["decision"],
                "runtime_seconds": value["runtime_seconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if value["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
