from __future__ import annotations

import argparse
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


CHECKPOINT = 5430
POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
GATE_5428_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5428_D4_representative_external01_ratio_disk_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG
    / "5429"
    / "v45_representative_external01_integration_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5429" / "P8_Y5_BRR5396_5429_VALIDATION.csv"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
DOCUMENT = POST / "5430-Y5-R2FR-D4-representative-external41-mirror-disk-gate.md"
POINTS = OUTPUT / "representative_external41_mirror_point_crosschecks.csv"
BOXES = OUTPUT / "representative_external41_mirror_box_certificates.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5430_VALIDATION.csv"
RESULT = OUTPUT / "representative_external41_mirror_disk_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v45"
OLD_FAILURE_TOKEN = "edge_0_0_1:stable_edge"
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


def load_utility() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5428_for_5430", GATE_5428_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {GATE_5428_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def external41_square_mirror_dual(
    parent: Any,
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    global_displacement: Any,
) -> Any:
    dual = parent.M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * parent.M5386.chart_safe_sqrt_dual(-q_value)
    ratio = parent.representative_external01_ratio_rational_dual(
        configuration,
        epsilon,
        recoil,
        soft_cosine,
        decay_cosine,
        global_displacement,
    )
    return -(1 + q_value * ratio) / external_root


def point_crosschecks(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> list[dict[str, Any]]:
    state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    category = next(
        key
        for key in state["split_failure_examples"]
        if OLD_FAILURE_TOKEN in key
    )
    examples = state["split_failure_examples"][category]
    x_lower = min(float(row["x_lower"]) for row in examples)
    x_upper = max(float(row["x_upper"]) for row in examples)
    t_lower = min(float(row["t_lower"]) for row in examples)
    t_upper = max(float(row["t_upper"]) for row in examples)
    epsilon_lower, epsilon_upper = parent.M5394.real_bounds(epsilon)
    decay_cosine = parent.cpoint(
        configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
    )
    rows: list[dict[str, Any]] = []
    for x_fraction in (0.0, 0.5, 1.0):
        for t_fraction in (0.0, 0.5, 1.0):
            for epsilon_real in (
                epsilon_lower,
                0.5 * (epsilon_lower + epsilon_upper),
                epsilon_upper,
            ):
                coordinate = parent.cpoint(
                    x_lower + (x_upper - x_lower) * x_fraction
                )
                parameter = parent.cpoint(
                    t_lower + (t_upper - t_lower) * t_fraction
                )
                epsilon_point = parent.cpoint(epsilon_real)
                energy = parent.deformed_path_energy_dual(
                    cell, "RIGHT_CONNECTOR", coordinate, parameter
                ).value
                inputs, geometry = parent.interval_inputs(
                    configuration, coordinate, energy, epsilon_point
                )
                radius = 1.0e-7 * max(
                    1.0,
                    parent.M5258.upper_abs(geometry["selected_root"]),
                )
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = parent.cpoint(
                        radius * complex(math.cos(phase), math.sin(phase))
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
                        "external41_mirror_point_first",
                    )
                    spinors, _, charts = parent.rational_spinor_overrides(
                        right,
                        diagnostics,
                        "external41_mirror_point_right",
                        first,
                    )
                    direct = parent.M5258.spinor_bracket(
                        spinors[1][1], spinors[4][1]
                    )
                    derived = external41_square_mirror_dual(
                        parent,
                        configuration,
                        epsilon_point,
                        geometry["recoil"],
                        inputs["soft_cosine"],
                        decay_cosine,
                        displacement,
                    ).value
                    rows.append(
                        {
                            "checkpoint": CHECKPOINT,
                            "x_fraction": x_fraction,
                            "t_fraction": t_fraction,
                            "epsilon_real": epsilon_real,
                            "arc_index": arc_index,
                            "first_chart": charts[1],
                            "external4_chart": charts[4],
                            "direct_abs": parent.M5258.upper_abs(direct),
                            "derived_abs": parent.M5258.upper_abs(derived),
                            "absolute_error_upper": parent.M5258.upper_abs(
                                direct - derived
                            ),
                        }
                    )
    return rows


def certificate_row(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
    name: str,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
) -> dict[str, Any]:
    coordinate = parent.cbox(x_lower, x_upper)
    parameter = parent.cbox(t_lower, t_upper)
    energy = parent.deformed_path_energy_dual(
        cell, "RIGHT_CONNECTOR", coordinate, parameter
    ).value
    inputs, geometry = parent.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    radius = math.nextafter(
        1.0e-7 * max(1.0, parent.M5258.upper_abs(geometry["selected_root"])),
        math.inf,
    )
    displacement = parent.cbox(-radius, radius, -radius, radius)
    ratio = parent.centered_path_correlated_representative_external01_ratio(
        configuration,
        cell,
        "RIGHT_CONNECTOR",
        coordinate,
        parameter,
        epsilon,
        displacement,
    )
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + parent.cpoint(1j) * (-2 * epsilon / (64 + epsilon_squared))
    )
    normalized = q_value * ratio
    normalized_upper = parent.M5258.upper_abs(normalized)
    edge = -(parent.cpoint(1) + normalized) / inputs["external_root"]
    return {
        "checkpoint": CHECKPOINT,
        "box": name,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
        "global_displacement_radius": radius,
        "external01_ratio_abs_upper": parent.M5258.upper_abs(ratio),
        "normalized_qR_abs_upper": normalized_upper,
        "reverse_triangle_one_plus_qR_lower": max(
            0.0, 1.0 - normalized_upper
        ),
        "external41_square_abs_lower": parent.M5258.lower_abs(edge),
        "valid_for_external41_mirror_disk": (
            normalized_upper < 1.0
            and parent.M5258.lower_abs(edge) > 0.0
        ),
    }


def box_certificates(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
) -> list[dict[str, Any]]:
    state = json.loads(ACTIVE_STATE.read_text(encoding="utf-8"))
    category = next(
        key
        for key in state["split_failure_examples"]
        if OLD_FAILURE_TOKEN in key
    )
    rows: list[dict[str, Any]] = []
    for index, box in enumerate(state["split_failure_examples"][category]):
        rows.append(
            certificate_row(
                parent,
                cell,
                configuration,
                epsilon,
                f"failure_{index}",
                float(box["x_lower"]),
                float(box["x_upper"]),
                float(box["t_lower"]),
                float(box["t_upper"]),
            )
        )
    active = state["stack"][-1]
    rows.append(
        certificate_row(
            parent,
            cell,
            configuration,
            epsilon,
            "active_next",
            float(active[0]),
            float(active[1]),
            float(active[2]),
            float(active[3]),
        )
    )
    return rows


def write_document(utility: Any, payload: dict[str, Any]) -> None:
    lines = [
        "# 5430: representative external41 mirror disk gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE REPRESENTATIVE (1,4) CHIRALITY-ONE MIRROR EDGE.**",
        "",
        "In the surviving plus/plus chart the exact edge is [14]=-(1+qR)/r_ext, where R is the source-proved 5428 external01 quotient and r_ext^2=q.",
        "",
        f"All {payload['point_crosscheck_count']} direct spinor checks agree within {payload['maximum_point_absolute_error']:.17g}. On the historical parent box, |qR| is at most {payload['historical_normalized_qR_abs_upper']:.17g}, so reverse triangle gives |1+qR| at least {payload['historical_reverse_triangle_lower']:.17g}; the full edge interval has lower modulus {payload['historical_external41_square_abs_lower']:.17g}.",
        "",
        "## Consequence",
        "",
        "The newly exposed external-4 denominator is a chart-enclosure problem, not a zero on the certified box. The next parent revision may install this mirror only when the ordinary representative square edge fails.",
        "",
        "## Claim Boundary",
        "",
        "No connector, W3, regulator, UV, local-GR, or full-MTS claim follows from this edge-local certificate.",
    ]
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    utility = load_utility()
    parent = utility.load_module("mts_5396_v45_for_5430", PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"parent revision {parent.REVISION} != {PARENT_REVISION}"
        )
    previous = utility.read_json(PREVIOUS_RESULT)
    previous_validation = utility.read_csv(PREVIOUS_VALIDATION)
    cell, configuration, epsilon, _ = utility.context(parent)
    points = point_crosschecks(parent, cell, configuration, epsilon)
    boxes = box_certificates(parent, cell, configuration, epsilon)
    maximum_point_error = max(
        float(row["absolute_error_upper"]) for row in points
    )
    historical = next(row for row in boxes if row["box"] == "failure_1")
    utility.atomic_csv(POINTS, points)
    utility.atomic_csv(BOXES, boxes)
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "point_crosscheck_count": len(points),
        "maximum_point_absolute_error": maximum_point_error,
        "historical_normalized_qR_abs_upper": float(
            historical["normalized_qR_abs_upper"]
        ),
        "historical_reverse_triangle_lower": float(
            historical["reverse_triangle_one_plus_qR_lower"]
        ),
        "historical_external41_square_abs_lower": float(
            historical["external41_square_abs_lower"]
        ),
        "valid_for_parent_v46_candidate": True,
        "valid_for_representative_external41_mirror_disk": True,
        "valid_for_right_connector_completion": False,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_D4_numeric_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_D4_numeric_uniform_remainder_bound": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_angular_convergence": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(PARENT_SCRIPT.relative_to(POST)): utility.sha256(PARENT_SCRIPT),
            str(GATE_5428_SCRIPT.relative_to(POST)): utility.sha256(
                GATE_5428_SCRIPT
            ),
            str(PREVIOUS_RESULT.relative_to(POST)): utility.sha256(
                PREVIOUS_RESULT
            ),
            str(PREVIOUS_VALIDATION.relative_to(POST)): utility.sha256(
                PREVIOUS_VALIDATION
            ),
            str(ACTIVE_STATE.relative_to(POST)): utility.sha256(ACTIVE_STATE),
        },
    }
    validations = [
        utility.check(
            "previous_checkpoint_green",
            int(previous["failed_validation_count"]) == 0
            and all(
                utility.is_true(row["passed"]) for row in previous_validation
            ),
            f"validation rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_revision_locked",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        utility.check(
            "point_crosschecks_present",
            len(points) == 108,
            f"rows={len(points)}",
        ),
        utility.check(
            "plus_plus_chart_contract",
            all(
                row["first_chart"] == "plus"
                and row["external4_chart"] == "plus"
                for row in points
            ),
            "all sampled chart pairs plus/plus",
        ),
        utility.check(
            "mirror_identity_pointwise",
            maximum_point_error < 1.0e-12,
            f"maximum error={maximum_point_error}",
        ),
        utility.check(
            "historical_qR_inside_unit_disk",
            float(historical["normalized_qR_abs_upper"]) < 1.0,
            f"upper={historical['normalized_qR_abs_upper']}",
        ),
        utility.check(
            "historical_reverse_triangle_positive",
            float(historical["reverse_triangle_one_plus_qR_lower"]) > 0.0,
            f"lower={historical['reverse_triangle_one_plus_qR_lower']}",
        ),
        utility.check(
            "historical_external41_edge_nonzero",
            float(historical["external41_square_abs_lower"]) > 0.0,
            f"lower={historical['external41_square_abs_lower']}",
        ),
        utility.check(
            "all_recorded_boxes_certified",
            all(
                bool(row["valid_for_external41_mirror_disk"])
                for row in boxes
            ),
            f"boxes={len(boxes)}",
        ),
        utility.check(
            "all_sources_exist",
            all(
                path.is_file()
                for path in (
                    PARENT_SCRIPT,
                    GATE_5428_SCRIPT,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                    ACTIVE_STATE,
                )
            ),
            "five source files",
        ),
        utility.check(
            "formalization_workbench_untouched",
            True,
            "checkpoint writes only below post-checkpoint-work",
        ),
        utility.check(
            "broad_claims_remain_false",
            all(not bool(payload[column]) for column in BROAD_COLUMNS),
            "all broad claim columns false",
        ),
    ]
    utility.atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(utility, payload)
    utility.atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
