from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
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
if os.name == "nt":
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


CHECKPOINT = 5437
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
UTILITY_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5428_D4_representative_external01_ratio_disk_gate.py"
)
ISOTROPIC_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5434_D4_subdivided_representative_ratio_disk_subcover_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5436" / "anisotropic_external01_invariant_result.json"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5437-Y5-R2FR-D4-external01-endpoint-zero-and-pole-order-gate.md"
SAMPLES = OUTPUT / "external01_endpoint_samples.csv"
SUMMARY = OUTPUT / "external01_endpoint_order_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5437_VALIDATION.csv"
RESULT = OUTPUT / "external01_endpoint_zero_and_pole_order_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v47"
PATH_SEGMENT = "RIGHT_CONNECTOR"
T_SAMPLES = (
    0.0,
    1.0e-12,
    1.0e-10,
    1.0e-8,
    1.0e-7,
    1.0e-6,
    1.0e-5,
    1.0e-4,
    1.0e-3,
    1.0 / 128.0,
    2.0 / 128.0,
    4.0 / 128.0,
    7.0 / 128.0,
)
FIT_T_MINIMUM = 1.0e-8
FIT_T_MAXIMUM = 1.0e-4
ENDPOINT_ZERO_TOLERANCE = 1.0e-20
NONZERO_SQUARE_FLOOR = 1.0e-2
NONZERO_INVARIANT_FLOOR = 1.0e-4
NONZERO_ANGLE_FLOOR = 1.0e-3
BROAD_FLAGS = (
    "valid_for_parent_integration",
    "valid_for_right_connector_completion",
    "valid_for_regular_away_W3_claim",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def interval_center(parent: Any, value: Any) -> complex:
    real_lower, real_upper = parent.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(value)
    return complex(
        (real_lower + real_upper) / 2.0,
        (imaginary_lower + imaginary_upper) / 2.0,
    )


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def log_order(rows: list[dict[str, Any]], field: str) -> float:
    points = [
        (math.log(float(row["t"])), math.log(float(row[field])))
        for row in rows
        if FIT_T_MINIMUM <= float(row["t"]) <= FIT_T_MAXIMUM
        and float(row[field]) > 0.0
    ]
    if len(points) < 2:
        return math.nan
    mean_x = sum(point[0] for point in points) / len(points)
    mean_y = sum(point[1] for point in points) / len(points)
    denominator = sum((point[0] - mean_x) ** 2 for point in points)
    if denominator == 0.0:
        return math.nan
    return sum(
        (point[0] - mean_x) * (point[1] - mean_y) for point in points
    ) / denominator


def sample_target(
    parent: Any,
    isotropic: Any,
    cell: dict[str, Any],
    epsilon_box: Any,
    target: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    configuration, _ = isotropic.representative_configuration(
        parent, cell, epsilon_box, target
    )
    epsilon = parent.M5385.complex_midpoint_box(epsilon_box)
    epsilon_center = interval_center(parent, epsilon)
    x_value = (float(target["x_lower"]) + float(target["x_upper"])) / 2.0
    coordinate = parent.cpoint(x_value)
    displacement = parent.cpoint(0)
    rows: list[dict[str, Any]] = []
    for t_value in T_SAMPLES:
        parameter = parent.cpoint(t_value)
        energy_box = parent.deformed_path_energy_dual(
            cell, PATH_SEGMENT, coordinate, parameter
        ).value
        ratio_box = (
            parent.centered_path_correlated_representative_external01_ratio(
                configuration,
                cell,
                PATH_SEGMENT,
                coordinate,
                parameter,
                epsilon,
                displacement,
            )
        )
        square_box = ratio_box - parent.cpoint(1)
        invariant_box = parent.centered_path_correlated_external_first_invariant(
            configuration,
            cell,
            PATH_SEGMENT,
            coordinate,
            parameter,
            epsilon,
            displacement,
            0,
        )
        angle_box = invariant_box / square_box
        energy = interval_center(parent, energy_box)
        ratio = interval_center(parent, ratio_box)
        square = interval_center(parent, square_box)
        invariant = interval_center(parent, invariant_box)
        angle = interval_center(parent, angle_box)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "target_path": target["refinement_path"],
                "role": configuration["role"],
                "soft_sign": configuration["soft_sign"],
                "decay_sign": configuration["decay_sign"],
                "x": x_value,
                "t": t_value,
                "epsilon_real": epsilon_center.real,
                "epsilon_imaginary": epsilon_center.imag,
                "energy_real": energy.real,
                "energy_imaginary": energy.imag,
                "ratio_real": ratio.real,
                "ratio_imaginary": ratio.imag,
                "ratio_abs": abs(ratio),
                "square_real": square.real,
                "square_imaginary": square.imag,
                "square_abs": abs(square),
                "invariant_real": invariant.real,
                "invariant_imaginary": invariant.imag,
                "invariant_abs": abs(invariant),
                "angle_real": angle.real,
                "angle_imaginary": angle.imag,
                "angle_abs": abs(angle),
                "invariant_abs_over_t": (
                    "" if t_value == 0.0 else abs(invariant) / t_value
                ),
                "angle_abs_over_t": (
                    "" if t_value == 0.0 else abs(angle) / t_value
                ),
                **{flag: False for flag in BROAD_FLAGS},
            }
        )
    endpoint = rows[0]
    invariant_order = log_order(rows, "invariant_abs")
    angle_order = log_order(rows, "angle_abs")
    square_order = log_order(rows, "square_abs")
    endpoint_zero = (
        float(endpoint["invariant_abs"]) <= ENDPOINT_ZERO_TOLERANCE
        and float(endpoint["angle_abs"]) <= ENDPOINT_ZERO_TOLERANCE
        and float(endpoint["square_abs"]) >= NONZERO_SQUARE_FLOOR
    )
    linear_zero = (
        0.8 <= invariant_order <= 1.2
        and 0.8 <= angle_order <= 1.2
        and abs(square_order) <= 0.2
    )
    finite_endpoint = (
        float(endpoint["invariant_abs"]) >= NONZERO_INVARIANT_FLOOR
        and float(endpoint["angle_abs"]) >= NONZERO_ANGLE_FLOOR
        and float(endpoint["square_abs"]) >= NONZERO_SQUARE_FLOOR
        and abs(invariant_order) <= 0.2
        and abs(angle_order) <= 0.2
        and abs(square_order) <= 0.2
    )
    summary = {
        "checkpoint": CHECKPOINT,
        "target_path": target["refinement_path"],
        "x": x_value,
        "sample_count": len(rows),
        "endpoint_square_abs": endpoint["square_abs"],
        "endpoint_invariant_abs": endpoint["invariant_abs"],
        "endpoint_angle_abs": endpoint["angle_abs"],
        "invariant_log_order": invariant_order,
        "angle_log_order": angle_order,
        "square_log_order": square_order,
        "pointwise_endpoint_zero_detected": endpoint_zero,
        "pointwise_linear_zero_detected": linear_zero,
        "pointwise_simple_reciprocal_pole_detected": endpoint_zero and linear_zero,
        "pointwise_finite_endpoint_detected": finite_endpoint,
        **{flag: False for flag in BROAD_FLAGS},
    }
    return rows, summary


def validation_row(check: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "check": check,
        "passed": passed,
        "detail": detail,
    }


def write_document(payload: dict[str, Any], summaries: list[dict[str, Any]]) -> None:
    if payload["pointwise_simple_reciprocal_pole_detected"]:
        decision = "**POINTWISE SIMPLE ENDPOINT ZERO DETECTED; NONZERO-EDGE ROUTE REJECTED.**"
        interpretation = (
            "At both representative broad-chart centres, `s01` and `<01>` vanish "
            "linearly as `t -> 0`, while `[01]` remains finite and nonzero. The "
            "new c0 failure is therefore not cured by finer interval subdivision. "
            "The next admissible route is an amplitude-level pole cancellation or "
            "integrated endpoint bound; this checkpoint alone is not a global proof."
        )
    elif payload["pointwise_finite_endpoint_detected"]:
        decision = "**POINTWISE FINITE ENDPOINT DETECTED; PHYSICAL-POLE ROUTE REJECTED.**"
        interpretation = (
            "At both representative broad-chart centres, `s01`, `[01]`, and "
            "`<01> = s01/[01]` approach finite nonzero constants as `t -> 0`. "
            "Their fitted log orders are zero. The 5436 zero enclosure is therefore "
            "an interval-width dependency, not evidence for a physical collinear "
            "pole. The next route is a finer endpoint `t` subcover."
        )
    else:
        decision = "**POINTWISE ENDPOINT ORDER REMAINS UNRESOLVED.**"
        interpretation = (
            "The samples do not establish the expected finite-square, linear-angle "
            "endpoint law. No parent integration is allowed."
        )
    lines = [
        "# 5437: external01 endpoint zero and pole-order gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Pointwise order table",
        "",
        "| target | |[01](0)| | |s01(0)| | |<01>(0)| | ord(s01) | ord(<01>) | ord([01]) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            "| {target_path} | {endpoint_square_abs:.12g} | "
            "{endpoint_invariant_abs:.12g} | {endpoint_angle_abs:.12g} | "
            "{invariant_log_order:.8f} | {angle_log_order:.8f} | "
            "{square_log_order:.8f} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "- This is a reproducible pointwise order diagnostic at the LR/R broad-chart centres and the regulator midpoint.",
            "- It distinguishes a finite endpoint from a simple endpoint zero before any full-cover calculation.",
            "- It does not prove the order uniformly in `x`, regulator, displacement, or chart selector.",
            "- All parent, right-connector, UV, and local-GR claim flags remain false.",
            "",
            "## Next derivation",
            "",
            (
                "Derive the complete K5 amplitude numerator order at `t=0` before any v48 parent edit."
                if payload["pointwise_simple_reciprocal_pole_detected"]
                else "Build the anisotropic endpoint `t` negative-real subcover before any v48 parent edit."
            ),
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    parent = load_module("mts_5396_v47_for_5437", PARENT_SCRIPT)
    utility = load_module("mts_5428_for_5437", UTILITY_SCRIPT)
    isotropic = load_module("mts_5434_for_5437", ISOTROPIC_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    state_before = ACTIVE_STATE.read_bytes()
    rows_before = ACTIVE_ROWS.read_bytes()
    cell, epsilon_row = isotropic.epsilon_and_cell(parent)
    epsilon_box = parent.epsilon_interval(epsilon_row)
    all_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for target in isotropic.targets(utility):
        rows, summary = sample_target(
            parent, isotropic, cell, epsilon_box, target
        )
        all_rows.extend(rows)
        summaries.append(summary)
    all_finite = all(
        all(
            math.isfinite(float(row[field]))
            for field in (
                "energy_real",
                "energy_imaginary",
                "ratio_abs",
                "square_abs",
                "invariant_abs",
                "angle_abs",
            )
        )
        for row in all_rows
    )
    simple_pole = len(summaries) == 2 and all(
        bool(row["pointwise_simple_reciprocal_pole_detected"])
        for row in summaries
    )
    finite_endpoint = len(summaries) == 2 and all(
        bool(row["pointwise_finite_endpoint_detected"])
        for row in summaries
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_count": len(summaries),
        "sample_count": len(all_rows),
        "pointwise_simple_reciprocal_pole_detected": simple_pole,
        "pointwise_finite_endpoint_detected": finite_endpoint,
        "nonzero_edge_subdivision_route_rejected": simple_pole,
        "next_target": (
            "K5_AMPLITUDE_NUMERATOR_ENDPOINT_ORDER"
            if simple_pole
            else (
                "ANISOTROPIC_ENDPOINT_T_NEGATIVE_REAL_SUBCOVER"
                if finite_endpoint
                else "SHARPER_CORRELATED_ENDPOINT_DIAGNOSTIC"
            )
        ),
        **{flag: False for flag in BROAD_FLAGS},
    }
    state_unchanged = (
        ACTIVE_STATE.read_bytes() == state_before
        and ACTIVE_ROWS.read_bytes() == rows_before
    )
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        validation_row(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    UTILITY_SCRIPT,
                    ISOTROPIC_SCRIPT,
                    PREVIOUS_RESULT,
                    ACTIVE_STATE,
                    ACTIVE_ROWS,
                )
            ),
            "six local inputs",
        ),
        validation_row(
            "parent_revision_is_v47",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        validation_row(
            "5436_failure_is_real_input",
            int(previous["failed_cell_count"]) == 1344
            and not bool(
                previous["valid_for_anisotropic_external01_invariant_subcover"]
            ),
            f"failed cells={previous['failed_cell_count']}",
        ),
        validation_row(
            "two_targets_and_all_samples_present",
            len(summaries) == 2
            and len(all_rows) == 2 * len(T_SAMPLES),
            f"targets={len(summaries)}, samples={len(all_rows)}",
        ),
        validation_row(
            "all_samples_are_finite",
            all_finite,
            f"samples={len(all_rows)}",
        ),
        validation_row(
            "endpoint_route_classified",
            simple_pole or finite_endpoint,
            (
                "simple pole at both broad-chart centres"
                if simple_pole
                else (
                    "finite nonzero endpoint at both broad-chart centres"
                    if finite_endpoint
                    else "pointwise order unresolved"
                )
            ),
        ),
        validation_row(
            "active_parent_state_unchanged",
            state_unchanged,
            str(ACTIVE_STATE),
        ),
        validation_row(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"touches={len(formalization_touches)}",
        ),
        validation_row(
            "broad_claim_flags_false",
            not any(bool(payload[flag]) for flag in BROAD_FLAGS),
            "all broad flags false",
        ),
    ]
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    payload["elapsed_seconds"] = (
        datetime.now(timezone.utc) - started
    ).total_seconds()
    atomic_csv(SAMPLES, all_rows)
    atomic_csv(SUMMARY, summaries)
    atomic_csv(VALIDATION, validations)
    atomic_json(RESULT, payload)
    write_document(payload, summaries)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    result = run_gate()
    raise SystemExit(0 if result["failed_validation_count"] == 0 else 1)
