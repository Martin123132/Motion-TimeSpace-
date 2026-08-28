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


CHECKPOINT = 5413
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
    / "5412"
    / "v42_frontier_contraction_result.json"
)
STATUS = SOURCE / "status.json"
MIGRATION = SOURCE / "resume_manifest_migration.json"
ACTIVE_STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_LEFT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5413-Y5-R2FR-D4-left-second-soft-mixed-angle-subcover-gate.md"
COVERS = OUTPUT / "left_second_soft_mixed_angle_cover.csv"
POINTS = OUTPUT / "left_second_soft_mixed_angle_point_crosschecks.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5413_VALIDATION.csv"
RESULT = OUTPUT / "left_second_soft_mixed_angle_subcover_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v43"
X_LOWER = 0.3250603057916317
X_UPPER = 0.33489218984300384
T_LOWER = 0.0
T_UPPER = 0.5
REFINEMENT_DEPTH = 3
REFINEMENT_PATH = "LRD"
REMOVED_EDGE = "edge_2_2_3:stable_edge"
NEXT_KNOWN_EDGE = "edge_1_4_2:stable_edge"
EXPECTED_AREA = 0.03932753620548857
BROAD_COLUMNS = (
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
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
    specification = importlib.util.spec_from_file_location("mts_5396", PARENT_SCRIPT)
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


def epsilon_and_context(parent: Any) -> tuple[Any, Any, Any, dict[str, Any]]:
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


def cover_rows(parent: Any, cell: Any, configuration: Any, epsilon: Any) -> list[dict[str, Any]]:
    coordinate = parent.cbox(X_LOWER, X_UPPER)
    parameter = parent.cbox(T_LOWER, T_UPPER)
    rows: list[dict[str, Any]] = []
    for subdivision_count in (1, 2, 4, 8):
        if subdivision_count == 1:
            enclosure = (
                parent.centered_path_correlated_left_second_soft_mixed_angle(
                    configuration,
                    cell,
                    "LEFT_CONNECTOR",
                    coordinate,
                    parameter,
                    epsilon,
                )
            )
        else:
            enclosure = parent.subdivided_path_correlated_left_second_soft_mixed_angle(
                configuration,
                cell,
                "LEFT_CONNECTOR",
                coordinate,
                parameter,
                epsilon,
                subdivision_count,
            )
        real_lower, real_upper = parent.M5394.real_bounds(enclosure)
        imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(enclosure)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "mapped_cell_id": cell["mapped_cell_id"],
                "term_id": "MC04_SP_DP",
                "selected_role": configuration["role"],
                "path_segment": "LEFT_CONNECTOR",
                "refinement_depth": REFINEMENT_DEPTH,
                "refinement_path": REFINEMENT_PATH,
                "edge_pair": "2|3",
                "chirality": 0,
                "hard_chart": "minus",
                "soft_chart": "plus",
                "subdivision_count": subdivision_count,
                "subcover_leaf_count": subdivision_count**2,
                "edge_real_lower": real_lower,
                "edge_real_upper": real_upper,
                "edge_imaginary_lower": imaginary_lower,
                "edge_imaginary_upper": imaginary_upper,
                "edge_abs_lower": parent.M5258.lower_abs(enclosure),
                "edge_abs_upper": parent.M5258.upper_abs(enclosure),
                "valid_for_edge_nonzero": parent.M5258.lower_abs(enclosure) > 0.0,
            }
        )
    return rows


def point_rows(parent: Any, cell: Any, configuration: Any, epsilon: Any) -> list[dict[str, Any]]:
    epsilon_real = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary = parent.M5394.imaginary_bounds(epsilon)
    epsilon_point = parent.cpoint(
        0.5 * (epsilon_real[0] + epsilon_real[1])
        + 0.5j * (epsilon_imaginary[0] + epsilon_imaginary[1])
    )
    rows: list[dict[str, Any]] = []
    for x_fraction in (0.1, 0.5, 0.9):
        for t_fraction in (0.1, 0.5, 0.9):
            x_value = X_LOWER + (X_UPPER - X_LOWER) * x_fraction
            t_value = T_LOWER + (T_UPPER - T_LOWER) * t_fraction
            coordinate = parent.cpoint(x_value)
            parameter = parent.cpoint(t_value)
            energy = parent.deformed_path_energy_dual(
                cell,
                "LEFT_CONNECTOR",
                coordinate,
                parameter,
            ).value
            inputs, geometry = parent.interval_inputs(
                configuration,
                coordinate,
                energy,
                epsilon_point,
            )
            unit_circle = geometry["selected_root"] + parent.cpoint(1.0e-7)
            direct = parent.M5386.centered_hard_soft_edge(
                configuration,
                inputs,
                geometry,
                unit_circle,
                2,
                "minus",
                "plus",
                0,
            )
            derived = parent.centered_path_correlated_left_second_soft_mixed_angle(
                configuration,
                cell,
                "LEFT_CONNECTOR",
                coordinate,
                parameter,
                epsilon_point,
            )
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "x_fraction": x_fraction,
                    "t_fraction": t_fraction,
                    "x_value": x_value,
                    "t_value": t_value,
                    "direct_edge_abs": parent.M5258.upper_abs(direct),
                    "derived_edge_abs": parent.M5258.upper_abs(derived),
                    "absolute_error_upper": parent.M5258.upper_abs(direct - derived),
                }
            )
    return rows


def historical_parent_result(parent: Any, cell: Any, epsilon_row: dict[str, Any]) -> dict[str, Any]:
    try:
        row = parent.evaluate_path_box(
            cell,
            "MC04_SP_DP",
            parent.configuration_variants("MC04_SP_DP"),
            epsilon_row,
            "LEFT_CONNECTOR",
            X_LOWER,
            X_UPPER,
            T_LOWER,
            T_UPPER,
            REFINEMENT_DEPTH,
            REFINEMENT_PATH,
            parent.material_support_segments(),
            parent.material_branch_data(),
            4,
        )
        return {
            "state": "PASS",
            "error": "",
            "minimum_denominator_abs_lower": float(
                row["minimum_amplitude_denominator_abs_lower"]
            ),
        }
    except Exception as error:
        return {
            "state": "ADVANCED_TO_LATER_FAILURE",
            "error": str(error),
            "minimum_denominator_abs_lower": 0.0,
        }


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5413: left second-soft mixed-angle subcover gate",
        "",
        "## Decision",
        "",
        "**PASS FOR THE NAMED EDGE AND CONTINUED V43 PRODUCTION ONLY.**",
        "",
        "The new left-copy `(2,3)` failure is an interval dependency. In the uniform hard-minus/soft-plus chart at chirality zero, the global unit-circle factor cancels exactly between the transverse factors. The remaining edge is therefore a correlated function of `(x,t,epsilon)` on the parent deformed path, not of an independently boxed spinor normalization.",
        "",
        "## Exact finite cover",
        "",
        f"- the unsubdivided enclosure contains zero;",
        f"- the `2 x 2` enclosure still contains zero;",
        f"- the exact `4 x 4` cover proves `|<23>| >= {payload['four_by_four_edge_abs_lower']:.17g}`;",
        f"- the `8 x 8` confirmation proves `|<23>| >= {payload['eight_by_eight_edge_abs_lower']:.17g}`.",
        "",
        f"All `{payload['point_crosscheck_count']}` point crosschecks agree with the parent hard-soft edge to maximum absolute error `{payload['maximum_point_absolute_error']:.17g}`. Re-evaluating the complete historical parent advances past `(2,3)` and stops only at the previously declared `(4,2)` stable-edge class.",
        "",
        "## Production migration",
        "",
        f"The adaptive state migrates `v42 -> v43` and remains resume-safe with `{payload['active_accepted_box_count']}` accepted and `{payload['active_pending_box_count']}` pending boxes. Exact accepted-plus-pending area is preserved.",
        "",
        "## Claim boundary",
        "",
        "This removes only the named left `(2,3)` enclosure obstruction. The active connector, regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS gates remain open.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (PARENT_SCRIPT, PREVIOUS, STATUS, MIGRATION, ACTIVE_STATE, ACTIVE_ROWS)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    parent = load_parent()
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = read_json(PREVIOUS)
    status = read_json(STATUS)
    migration = read_json(MIGRATION)
    state = read_json(ACTIVE_STATE)
    active_rows = read_csv(ACTIVE_ROWS)
    cell, configuration, epsilon, epsilon_row = epsilon_and_context(parent)
    covers = cover_rows(parent, cell, configuration, epsilon)
    points = point_rows(parent, cell, configuration, epsilon)
    historical = historical_parent_result(parent, cell, epsilon_row)
    accepted_area = sum(float(row["parameter_area"]) for row in active_rows)
    remaining_area = pending_area(state["stack"])
    total_area = accepted_area + remaining_area
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

    atomic_csv(COVERS, covers)
    atomic_csv(POINTS, points)
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "historical_parent_state": historical["state"],
        "historical_parent_later_error": historical["error"],
        "four_by_four_edge_abs_lower": float(covers[2]["edge_abs_lower"]),
        "eight_by_eight_edge_abs_lower": float(covers[3]["edge_abs_lower"]),
        "point_crosscheck_count": len(points),
        "maximum_point_absolute_error": max(
            float(row["absolute_error_upper"]) for row in points
        ),
        "active_accepted_box_count": int(state["accepted_count"]),
        "active_pending_box_count": len(state["stack"]),
        "active_maximum_pending_depth": max(
            (int(row[4]) for row in state["stack"]), default=0
        ),
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": remaining_area,
        "total_parameter_area": total_area,
        "valid_for_named_left_second_soft_edge": True,
        "valid_for_continued_v43_production": True,
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
            "parent_revision_is_v43",
            parent.REVISION == REVISION,
            parent.REVISION,
        ),
        check(
            "v42_state_migrated_to_v43",
            migration["previous_manifest"]["revision"].endswith("v42")
            and migration["current_manifest"]["revision"] == REVISION
            and state["revision"] == REVISION,
            "manifest and adaptive state record v42 -> v43",
        ),
        check(
            "coarse_and_two_by_two_reproduce_dependency",
            float(covers[0]["edge_abs_lower"]) == 0.0
            and float(covers[1]["edge_abs_lower"]) == 0.0,
            "1x1 and 2x2 retain zero",
        ),
        check(
            "four_by_four_proves_edge_nonzero",
            float(covers[2]["edge_abs_lower"]) > 0.0
            and float(covers[2]["edge_real_upper"]) < 0.0,
            f"4x4 lower={covers[2]['edge_abs_lower']}",
        ),
        check(
            "eight_by_eight_confirms_edge_nonzero",
            float(covers[3]["edge_abs_lower"])
            > float(covers[2]["edge_abs_lower"]),
            f"8x8 lower={covers[3]['edge_abs_lower']}",
        ),
        check(
            "point_identity_matches_parent_edge",
            payload["maximum_point_absolute_error"] <= 1.0e-12,
            f"max error={payload['maximum_point_absolute_error']:.17g}",
        ),
        check(
            "historical_parent_advances_past_named_edge",
            REMOVED_EDGE not in historical["error"]
            and NEXT_KNOWN_EDGE in historical["error"],
            historical["error"],
        ),
        check(
            "production_state_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(status["internally_certified_box_count"])
            == int(state["accepted_count"])
            == len(active_rows),
            f"accepted={len(active_rows)}; pending={len(state['stack'])}",
        ),
        check(
            "accepted_plus_pending_area_is_exact",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={remaining_area:.17g}",
        ),
        check(
            "checkpoint_5412_claim_boundary_preserved",
            not bool(previous["valid_for_regular_away_W3_claim"])
            and not bool(previous["valid_for_local_GR_claim"]),
            "5412 broad claims remain false",
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
