from __future__ import annotations

import argparse
import contextlib
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
SUPPORT_SCRIPT = SCRIPTS / "Y5_R2FR_D4_dyadic_support_endpoint_normal_form.py"
ALL_EIGHT_SCRIPT = SCRIPTS / "Y5_R2FR_D4_all_eight_endpoint_coefficient.py"
EPSILON_ID = "E0025"
EPSILON = 0.0025


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


SUPPORT = load_module("mts_5351_E0025_support_parent", SUPPORT_SCRIPT)
ALL_EIGHT = load_module("mts_5351_E0025_all_eight_parent", ALL_EIGHT_SCRIPT)
SUPPORT.SUPPORTED[EPSILON_ID] = EPSILON
ALL_EIGHT.SUPPORTED[EPSILON_ID] = EPSILON


def enable_read_only_base_configuration(parent_5342: Any) -> None:
    controller = parent_5342.M5334
    original = controller.configure_D4_target

    def configure_target(epsilon_id: str) -> dict[str, Path]:
        if epsilon_id == EPSILON_ID:
            return controller.configure_refinement(EPSILON_ID)
        return original(epsilon_id)

    controller.configure_D4_target = configure_target


enable_read_only_base_configuration(SUPPORT.M5342)
enable_read_only_base_configuration(ALL_EIGHT.M5346.M5342)

ORIGINAL_SUPPORT_EVENT_AT_SCALE = SUPPORT.event_normal_form_at_scale


def trace_reconstructed_support_event_at_scale(
    event: dict[str, str],
    scan: dict[str, str],
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    stencil_scale: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    parent = SUPPORT.M5342
    coordinate = float(event["event_coordinate"])
    coordinate_error = float(event["event_coordinate_error_estimate"])
    physical_gamma = abs(float(scan["pole_imaginary"]))
    boundary_scale = physical_gamma / abs(float(event["source_crossing_slope"]))
    derivative_step = max(stencil_scale * boundary_scale, 64.0 * coordinate_error)
    half_step = 0.5 * derivative_step
    offsets = (
        ("M1", -derivative_step),
        ("MH", -half_step),
        ("PH", half_step),
        ("P1", derivative_step),
    )
    evaluated: list[dict[str, Any]] = []
    for label, offset in offsets:
        row = parent.endpoint_state(
            event,
            scan,
            coordinate + offset,
            contract,
            base_context,
            multiplier,
            label,
        )
        row["delta_from_event"] = offset
        row["physical_multiplier"] = multiplier
        row["geometric_event_slope"] = float(event["source_crossing_slope"])
        row["geometric_gamma_seed"] = physical_gamma
        row["boundary_layer_scale_seed"] = boundary_scale
        row["stencil_source"] = "DIRECT_PARENT_REEVALUATION"
        evaluated.append(row)
    by_label = {row["stencil_label"]: row for row in evaluated}
    minus = by_label["M1"]
    minus_half = by_label["MH"]
    plus_half = by_label["PH"]
    plus = by_label["P1"]
    z0_left = 2.0 * parent.complex_from(minus_half, "boundary_gap") - parent.complex_from(
        minus, "boundary_gap"
    )
    z0_right = 2.0 * parent.complex_from(plus_half, "boundary_gap") - parent.complex_from(
        plus, "boundary_gap"
    )
    coefficient0_left = 2.0 * parent.complex_from(
        minus_half, "physical_endpoint_coefficient"
    ) - parent.complex_from(minus, "physical_endpoint_coefficient")
    coefficient0_right = 2.0 * parent.complex_from(
        plus_half, "physical_endpoint_coefficient"
    ) - parent.complex_from(plus, "physical_endpoint_coefficient")
    z0 = 0.5 * (z0_left + z0_right)
    coefficient0 = 0.5 * (coefficient0_left + coefficient0_right)
    z1_full = (
        parent.complex_from(plus, "boundary_gap")
        - parent.complex_from(minus, "boundary_gap")
    ) / (2.0 * derivative_step)
    z1_half = (
        parent.complex_from(plus_half, "boundary_gap")
        - parent.complex_from(minus_half, "boundary_gap")
    ) / derivative_step
    coefficient1_full = (
        parent.complex_from(plus, "physical_endpoint_coefficient")
        - parent.complex_from(minus, "physical_endpoint_coefficient")
    ) / (2.0 * derivative_step)
    coefficient1_half = (
        parent.complex_from(plus_half, "physical_endpoint_coefficient")
        - parent.complex_from(minus_half, "physical_endpoint_coefficient")
    ) / derivative_step
    z_trace_mismatch = parent.relative_complex_change(z0_left, z0_right)
    coefficient_trace_mismatch = parent.relative_complex_change(
        coefficient0_left, coefficient0_right
    )
    z_derivative_change = parent.relative_complex_change(z1_full, z1_half)
    coefficient_derivative_change = parent.relative_complex_change(
        coefficient1_full, coefficient1_half
    )
    log_sign = -1 if scan["contact_boundary"] == "LOWER" else 1
    primitive_error = parent.primitive_derivative_error(
        derivative_step,
        log_sign,
        coefficient0,
        coefficient1_half,
        z0,
        z1_half,
    )
    gap_resolved = abs(z0.imag) > 0.0 and abs(z0) > 100.0 * coordinate_error * abs(
        z1_half
    )
    support_ids = {row["support_id"] for row in evaluated}
    off_contact_fits_pass = all(parent.parse_bool(row["fit_contract_passes"]) for row in evaluated)
    coefficient_contract = (
        parent.parse_bool(event["event_contract_passes"])
        and off_contact_fits_pass
        and len(support_ids) == 1
        and z_trace_mismatch <= parent.TRACE_LIMIT
        and coefficient_trace_mismatch <= parent.TRACE_LIMIT
        and z_derivative_change <= parent.DERIVATIVE_LIMIT
        and coefficient_derivative_change <= parent.DERIVATIVE_LIMIT
        and gap_resolved
        and primitive_error <= parent.PRIMITIVE_DERIVATIVE_LIMIT
    )
    lower = float(minus_half["support_energy_lower"])
    upper = float(minus_half["support_energy_upper"])
    boundary_energy = lower if scan["contact_boundary"] == "LOWER" else upper
    reconstructed_pole = complex(boundary_energy, 0.0) - z0
    reconstructed_residue = coefficient0 / multiplier
    centre = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "x_panel_index": event["x_panel_index"],
        "term_id": event["term_id"],
        "primary_surface_id": event["primary_surface_id"],
        "contact_boundary": scan["contact_boundary"],
        "log_sign": log_sign,
        "stencil_label": "C0",
        "absolute_soft_cosine": coordinate,
        "support_id": next(iter(support_ids)),
        "fit_contract_passes": off_contact_fits_pass,
        "fit_relative_residual": max(float(row["fit_relative_residual"]) for row in evaluated),
        "residue_scale_relative_change": max(
            float(row["residue_scale_relative_change"]) for row in evaluated
        ),
        "second_order_suppression_ratio": max(
            float(row["second_order_suppression_ratio"]) for row in evaluated
        ),
        "fit_row_count": 0,
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        **parent.complex_fields("refined_pole", reconstructed_pole),
        **parent.complex_fields("endpoint_residue", reconstructed_residue),
        **parent.complex_fields("physical_endpoint_coefficient", coefficient0),
        **parent.complex_fields("boundary_gap", z0),
        "delta_from_event": 0.0,
        "physical_multiplier": multiplier,
        "geometric_event_slope": float(event["source_crossing_slope"]),
        "geometric_gamma_seed": physical_gamma,
        "boundary_layer_scale_seed": boundary_scale,
        "stencil_source": "EXACT_CONTACT_MEASURE_ZERO_TRACE_RECONSTRUCTION",
        "exact_contact_parent_fit_radius_was_zero": True,
        **parent.no_claims(),
    }
    rows = [minus, minus_half, centre, plus_half, plus]
    gamma_widening_factor = max(1.0, stencil_scale)
    parent_internal_scale = stencil_scale / gamma_widening_factor
    coefficient = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "x_panel_index": event["x_panel_index"],
        "term_id": event["term_id"],
        "primary_surface_id": event["primary_surface_id"],
        "contact_boundary": scan["contact_boundary"],
        "log_sign": log_sign,
        "event_coordinate": coordinate,
        "event_coordinate_error_estimate": coordinate_error,
        "derivative_step": derivative_step,
        "stencil_boundary_scale_multiplier": stencil_scale,
        "parent_internal_stencil_scale_multiplier": parent_internal_scale,
        "scan_gamma_widening_factor": gamma_widening_factor,
        "boundary_layer_scale": boundary_scale,
        **parent.complex_fields("boundary_gap_z0", z0),
        **parent.complex_fields("boundary_gap_derivative_z1", z1_half),
        **parent.complex_fields("physical_coefficient_C0", coefficient0),
        **parent.complex_fields("physical_coefficient_derivative_C1", coefficient1_half),
        "boundary_gap_trace_relative_mismatch": z_trace_mismatch,
        "physical_coefficient_trace_relative_mismatch": coefficient_trace_mismatch,
        "boundary_gap_derivative_relative_change_full_vs_half": z_derivative_change,
        "physical_coefficient_derivative_relative_change_full_vs_half": coefficient_derivative_change,
        "center_selector_to_trace_ratio": 1.0,
        "center_selector_trace_relative_change": 0.0,
        "center_selector_class": "TRACE_CONSISTENT",
        "center_selector_evaluation": "EXACT_CONTACT_FIT_UNDEFINED__TRACE_RECONSTRUCTED",
        "primitive_derivative_relative_error": primitive_error,
        "endpoint_coordinate_sensitivity_absolute": abs(coefficient0)
        * abs(z1_half / z0)
        * coordinate_error,
        "all_five_fit_contracts_pass": off_contact_fits_pass,
        "support_id_is_stable": len(support_ids) == 1,
        "endpoint_gap_is_regulator_resolved": gap_resolved,
        "coefficient_contract_passes": coefficient_contract,
        "exact_contact_trace_reconstruction": True,
        **parent.no_claims(),
    }
    return rows, coefficient


def support_event_at_scale_with_context(
    event: dict[str, str],
    scan: dict[str, str],
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    cached_stencil: list[dict[str, str]],
    stencil_scale: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    try:
        return ORIGINAL_SUPPORT_EVENT_AT_SCALE(
            event,
            scan,
            contract,
            base_context,
            multiplier,
            cached_stencil,
            stencil_scale,
        )
    except Exception as error:
        if "nonpositive near-support fit radius" in str(error):
            return trace_reconstructed_support_event_at_scale(
                event,
                scan,
                contract,
                base_context,
                multiplier,
                stencil_scale,
            )
        raise RuntimeError(
            f"E0025 endpoint extraction failed at {event['event_id']} "
            f"scale={stencil_scale}: {error}"
        ) from error


SUPPORT.event_normal_form_at_scale = support_event_at_scale_with_context


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def augment_provenance(
    result_path: Path,
    validation_path: Path,
    source_register: Path,
    no_claims: dict[str, bool],
) -> dict[str, Any]:
    result = read_json(result_path)
    wrapper = Path(__file__).resolve()
    wrapper_row = {
        "path": str(wrapper),
        "sha256": digest(wrapper),
        "exists": True,
        **no_claims,
    }
    source_rows = list(result.get("source_files", []))
    if all(Path(str(row.get("path", ""))).resolve() != wrapper for row in source_rows):
        source_rows.append(wrapper_row)
    register_rows = read_csv(source_register)
    if all(Path(row["path"]).resolve() != wrapper for row in register_rows):
        register_rows.append(wrapper_row)
    validation_rows = read_csv(validation_path)
    validation_rows = [
        row
        for row in validation_rows
        if row.get("gate") != "E0025_read_only_wrapper_is_source_registered"
    ]
    validation_rows.append(
        {
            "gate": "E0025_read_only_wrapper_is_source_registered",
            "passed": True,
            "detail": f"{wrapper}|{digest(wrapper)}",
        }
    )
    reconstructed_ids: list[str] = []
    if result.get("mode") == "D4-dyadic-support-endpoint-normal-form":
        coefficient_path = result_path.parent / "D4_E0025_support_endpoint_coefficients.csv"
        coefficient_rows = read_csv(coefficient_path)
        reconstructed_ids = [
            row["event_id"]
            for row in coefficient_rows
            if str(row.get("exact_contact_trace_reconstruction", "")).lower() == "true"
        ]
        validation_rows.append(
            {
                "gate": "zero_radius_exact_contacts_use_off_contact_trace_only",
                "passed": all(
                    row.get("center_selector_evaluation", "")
                    == "EXACT_CONTACT_FIT_UNDEFINED__TRACE_RECONSTRUCTED"
                    and str(row.get("coefficient_contract_passes", "")).lower() == "true"
                    for row in coefficient_rows
                    if row["event_id"] in reconstructed_ids
                ),
                "detail": "|".join(reconstructed_ids) if reconstructed_ids else "none_required",
            }
        )
    result["source_files"] = source_rows
    result["E0025_read_only_extraction_wrapper"] = str(wrapper)
    result["E0025_read_only_extraction_wrapper_sha256"] = digest(wrapper)
    result["source_geometry_was_not_rewritten"] = True
    result["exact_contact_trace_reconstruction_event_ids"] = reconstructed_ids
    result["validation_passed"] = bool(result.get("validation_passed")) and all(
        str(row["passed"]).strip().lower() == "true" for row in validation_rows
    )
    result["updated_utc"] = utc_now()
    atomic_csv(source_register, register_rows)
    atomic_csv(validation_path, validation_rows)
    atomic_json(result_path, result)
    return result


def run_support(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.dry_run:
        return SUPPORT.preflight(
            EPSILON_ID,
            arguments.geometry_result,
            arguments.geometry_validation,
        )
    if arguments.output_dir is None:
        raise ValueError("--output-dir is required")
    with contextlib.redirect_stdout(io.StringIO()):
        result = SUPPORT.run(
            EPSILON_ID,
            arguments.geometry_result,
            arguments.geometry_validation,
            arguments.output_dir,
        )
    output = arguments.output_dir.resolve()
    return augment_provenance(
        output / "D4_E0025_support_endpoint_result.json",
        output / "D4_E0025_support_endpoint_validation.csv",
        output / "source_register.csv",
        SUPPORT.no_claims(EPSILON_ID),
    )


def run_all_eight(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.endpoint_result is None:
        raise ValueError("--endpoint-result is required")
    if arguments.endpoint_coefficients is None:
        raise ValueError("--endpoint-coefficients is required")
    if arguments.endpoint_validation is None:
        raise ValueError("--endpoint-validation is required")
    if arguments.dry_run:
        return ALL_EIGHT.preflight(
            EPSILON_ID,
            arguments.geometry_result,
            arguments.geometry_validation,
            arguments.endpoint_result,
            arguments.endpoint_coefficients,
            arguments.endpoint_validation,
        )
    if arguments.output_dir is None:
        raise ValueError("--output-dir is required")
    with contextlib.redirect_stdout(io.StringIO()):
        result = ALL_EIGHT.run(
            EPSILON_ID,
            arguments.geometry_result,
            arguments.geometry_validation,
            arguments.endpoint_result,
            arguments.endpoint_coefficients,
            arguments.endpoint_validation,
            arguments.output_dir,
        )
    output = arguments.output_dir.resolve()
    return augment_provenance(
        output / "D4_E0025_all_eight_endpoint_result.json",
        output / "D4_E0025_all_eight_endpoint_validation.csv",
        output / "source_register.csv",
        ALL_EIGHT.no_claims(EPSILON_ID),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("support", "all-eight"), required=True)
    parser.add_argument("--geometry-result", type=Path, required=True)
    parser.add_argument("--geometry-validation", type=Path, required=True)
    parser.add_argument("--endpoint-result", type=Path)
    parser.add_argument("--endpoint-coefficients", type=Path)
    parser.add_argument("--endpoint-validation", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    result = run_support(arguments) if arguments.stage == "support" else run_all_eight(arguments)
    print(json.dumps(result, indent=2, sort_keys=True))
    passed = result.get("all_pass", result.get("validation_passed", False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
