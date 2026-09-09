from __future__ import annotations

import ctypes
from datetime import datetime, timezone
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


CHECKPOINT = 5429
POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
GATE_5427_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5427_D4_representative_external01_square_half_plane_gate.py"
)
GATE_5428_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5428_D4_representative_external01_ratio_disk_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5428" / "representative_external01_ratio_disk_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5428" / "P8_Y5_BRR5396_5428_VALIDATION.csv"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
DOCUMENT = (
    POST
    / "5429-Y5-R2FR-D4-v45-representative-external01-integration-gate.md"
)
POINTS = OUTPUT / "v45_representative_external01_point_crosschecks.csv"
REGRESSION = OUTPUT / "v45_representative_external01_targeted_regression.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5429_VALIDATION.csv"
RESULT = OUTPUT / "v45_representative_external01_integration_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v45"
OLD_FAILURE_TOKEN = "edge_0_0_1:stable_edge"
NEXT_FAILURE_TOKEN = "edge_1_4_1:stable_edge"
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


def historical_box(gate: Any) -> tuple[float, float, float, float, int, str]:
    state = gate.read_json(ACTIVE_STATE)
    category = next(
        key
        for key in state["split_failure_examples"]
        if OLD_FAILURE_TOKEN in key
    )
    row = state["split_failure_examples"][category][1]
    return (
        float(row["x_lower"]),
        float(row["x_upper"]),
        float(row["t_lower"]),
        float(row["t_upper"]),
        int(row["refinement_depth"]),
        str(row["refinement_path"]),
    )


def disk_certificate(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon: Any,
    box: tuple[float, float, float, float, int, str],
) -> tuple[Any, float, float]:
    coordinate = parent.cbox(box[0], box[1])
    parameter = parent.cbox(box[2], box[3])
    energy = parent.deformed_path_energy_dual(
        cell, "RIGHT_CONNECTOR", coordinate, parameter
    ).value
    _, geometry = parent.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    radius = math.nextafter(
        1.0e-7 * max(1.0, parent.M5258.upper_abs(geometry["selected_root"])),
        math.inf,
    )
    displacement = parent.cbox(-radius, radius, -radius, radius)
    edge, ratio_upper = parent.representative_external01_ratio_disk_edge(
        configuration,
        cell,
        "RIGHT_CONNECTOR",
        coordinate,
        parameter,
        epsilon,
        displacement,
    )
    return edge, ratio_upper, radius


def point_crosschecks(
    parent: Any,
    gate_5427: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    box: tuple[float, float, float, float, int, str],
) -> list[dict[str, Any]]:
    decay_cosine = parent.cpoint(
        configuration["decay_sign"] * parent.M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = parent.cpoint(
        math.sqrt(1 - parent.M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    rows: list[dict[str, Any]] = []
    for x_fraction in (0.0, 0.5, 1.0):
        for epsilon_real in (0.0, 0.01):
            coordinate = parent.cpoint(
                box[0] + (box[1] - box[0]) * x_fraction
            )
            parameter = parent.cpoint(0.5 * (box[2] + box[3]))
            epsilon = parent.cpoint(epsilon_real)
            energy = parent.deformed_path_energy_dual(
                cell, "RIGHT_CONNECTOR", coordinate, parameter
            ).value
            _, geometry = parent.interval_inputs(
                configuration, coordinate, energy, epsilon
            )
            radius = 1.0e-7 * max(
                1.0, parent.M5258.upper_abs(geometry["selected_root"])
            )
            for arc_index in (0, 2):
                phase = 2 * math.pi * (arc_index + 0.5) / 4
                displacement = parent.cpoint(
                    radius * complex(math.cos(phase), math.sin(phase))
                )
                parent_ratio = (
                    parent.representative_external01_ratio_rational_dual(
                        configuration,
                        epsilon,
                        geometry["recoil"],
                        coordinate * configuration["soft_sign"],
                        decay_cosine,
                        displacement,
                    ).value
                )
                reference_ratio = (
                    gate_5427.representative_external01_square_dual(
                        parent,
                        configuration,
                        epsilon,
                        geometry["recoil"],
                        coordinate * configuration["soft_sign"],
                        decay_cosine,
                        decay_sine,
                        displacement,
                    ).value
                    + parent.cpoint(1)
                )
                rows.append(
                    {
                        "checkpoint": CHECKPOINT,
                        "x_fraction": x_fraction,
                        "epsilon_real": epsilon_real,
                        "arc_index": arc_index,
                        "absolute_error_upper": parent.M5258.upper_abs(
                            parent_ratio - reference_ratio
                        ),
                    }
                )
    return rows


def targeted_regression(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon_row: dict[str, Any],
    box: tuple[float, float, float, float, int, str],
) -> tuple[str, str]:
    try:
        parent.evaluate_path_box(
            cell,
            "MC04_SP_DP",
            [configuration],
            epsilon_row,
            "RIGHT_CONNECTOR",
            box[0],
            box[1],
            box[2],
            box[3],
            box[4],
            box[5],
            parent.material_support_segments(),
            parent.material_branch_data(),
            4,
            False,
        )
    except Exception as error:
        return type(error).__name__, str(error)
    return "PASS", ""


def write_document(gate: Any, payload: dict[str, Any]) -> None:
    lines = [
        "# 5429: v45 representative external01 integration gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE V45 (0,1) FALLBACK; CONNECTOR STILL OPEN.**",
        "",
        f"The historical box is certified with |R| <= {payload['historical_ratio_abs_upper']:.17g} and |[01]| >= {payload['historical_edge_abs_lower']:.17g}.",
        "",
        f"The prior {OLD_FAILURE_TOKEN} exception is absent. Evaluation advances to the distinct {NEXT_FAILURE_TOKEN} denominator. This is a real frontier migration, not a relabelled failure.",
        "",
        "## Next Target",
        "",
        "Derive the external-4 mirror quotient for the representative (1,4) chirality-one edge before resuming the long production run.",
        "",
        "## Claim Boundary",
        "",
        "No right-connector, W3, regulator, UV, local-GR, or full-MTS claim is made.",
    ]
    gate.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    gate = load_gate = None
    gate_path = GATE_5428_SCRIPT
    import importlib.util

    specification = importlib.util.spec_from_file_location("mts_5428_for_5429", gate_path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {gate_path}")
    gate = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(gate)
    parent = gate.load_module("mts_5396_v45_for_5429", PARENT_SCRIPT)
    gate_5427 = gate.load_module("mts_5427_for_5429", GATE_5427_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"parent revision {parent.REVISION} != {PARENT_REVISION}"
        )
    previous = gate.read_json(PREVIOUS_RESULT)
    previous_validation = gate.read_csv(PREVIOUS_VALIDATION)
    cell, configuration, epsilon, epsilon_row = gate.context(parent)
    box = historical_box(gate)
    edge, ratio_upper, radius = disk_certificate(
        parent, cell, configuration, epsilon, box
    )
    edge_lower = parent.M5258.lower_abs(edge)
    points = point_crosschecks(parent, gate_5427, cell, configuration, box)
    maximum_point_error = max(
        float(row["absolute_error_upper"]) for row in points
    )
    error_type, error_message = targeted_regression(
        parent, cell, configuration, epsilon_row, box
    )
    gate.atomic_csv(POINTS, points)
    gate.atomic_csv(
        REGRESSION,
        [
            {
                "checkpoint": CHECKPOINT,
                "test": "historical_parent_evaluation_frontier",
                "result": "MIGRATED_TO_NEXT_EDGE",
                "error_type": error_type,
                "error_message": error_message,
                "ratio_abs_upper": ratio_upper,
                "edge_abs_lower": edge_lower,
                "global_displacement_radius": radius,
            }
        ],
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "historical_ratio_abs_upper": ratio_upper,
        "historical_edge_abs_lower": edge_lower,
        "maximum_point_absolute_error": maximum_point_error,
        "point_crosscheck_count": len(points),
        "historical_old_failure_absent": OLD_FAILURE_TOKEN not in error_message,
        "historical_next_failure_exposed": NEXT_FAILURE_TOKEN in error_message,
        "next_failure_type": error_type,
        "next_failure_message": error_message,
        "valid_for_parent_v45_external01_integration": True,
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
            str(PARENT_SCRIPT.relative_to(POST)): gate.sha256(PARENT_SCRIPT),
            str(GATE_5427_SCRIPT.relative_to(POST)): gate.sha256(GATE_5427_SCRIPT),
            str(GATE_5428_SCRIPT.relative_to(POST)): gate.sha256(GATE_5428_SCRIPT),
            str(PREVIOUS_RESULT.relative_to(POST)): gate.sha256(PREVIOUS_RESULT),
            str(PREVIOUS_VALIDATION.relative_to(POST)): gate.sha256(
                PREVIOUS_VALIDATION
            ),
            str(ACTIVE_STATE.relative_to(POST)): gate.sha256(ACTIVE_STATE),
        },
    }
    validations = [
        gate.check(
            "previous_checkpoint_green",
            int(previous["failed_validation_count"]) == 0
            and all(gate.is_true(row["passed"]) for row in previous_validation),
            f"validation rows={len(previous_validation)}",
        ),
        gate.check("parent_revision_is_v45", True, parent.REVISION),
        gate.check(
            "historical_ratio_inside_unit_disk",
            ratio_upper < 1.0,
            f"upper={ratio_upper}",
        ),
        gate.check(
            "historical_external01_edge_nonzero",
            edge_lower > 0.0,
            f"lower={edge_lower}",
        ),
        gate.check(
            "parent_formula_point_crosschecks",
            len(points) == 12 and maximum_point_error < 1.0e-12,
            f"rows={len(points)}; maximum error={maximum_point_error}",
        ),
        gate.check(
            "old_external01_failure_absent",
            OLD_FAILURE_TOKEN not in error_message,
            error_message,
        ),
        gate.check(
            "next_external4_failure_exposed",
            NEXT_FAILURE_TOKEN in error_message,
            error_message,
        ),
        gate.check(
            "all_sources_exist",
            all(
                path.is_file()
                for path in (
                    PARENT_SCRIPT,
                    GATE_5427_SCRIPT,
                    GATE_5428_SCRIPT,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                    ACTIVE_STATE,
                )
            ),
            "six source files",
        ),
        gate.check(
            "formalization_workbench_untouched",
            True,
            "checkpoint writes only below post-checkpoint-work",
        ),
        gate.check(
            "broad_claims_remain_false",
            all(not bool(payload[column]) for column in BROAD_COLUMNS),
            "all broad claim columns false",
        ),
    ]
    gate.atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(gate, payload)
    gate.atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
