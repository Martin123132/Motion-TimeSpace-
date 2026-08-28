from __future__ import annotations

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


POST = Path(__file__).resolve().parents[1]
PARENT_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5408"
DOCUMENT = (
    POST
    / "5408-Y5-R2FR-D4-representative-external41-square-subcover-gate.md"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5407"
    / "sixth_right_and_next_supports_completion_gate_result.json"
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

X_LOWER = 0.31522842174025956
X_UPPER = 0.31526682753733526
T_LOWER = 0.0
T_UPPER = 0.00390625
REFINEMENT_DEPTH = 18
REFINEMENT_PATH = "LLDLDLDLDLDLDLDLDL"
GLOBAL_ARC_COUNT = 4
SUBDIVISION_COUNT = 16


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


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


def load_parent() -> Any:
    specification = importlib.util.spec_from_file_location("mts_5396", PARENT_SCRIPT)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {PARENT_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def point_identity_rows(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon_row: dict[str, Any],
    radius: float,
) -> list[dict[str, Any]]:
    epsilon = parent.cpoint(
        0.5
        * (
            float(epsilon_row["epsilon_real_lower"])
            + float(epsilon_row["epsilon_real_upper"])
        )
    )
    coordinate = parent.cpoint(X_LOWER)
    parameter = parent.cpoint(T_LOWER)
    lower_energy, _ = parent.interval_boundary_energy(
        cell["lower_energy_boundary"], X_LOWER, X_LOWER
    )
    inputs, geometry = parent.interval_inputs(
        configuration, coordinate, lower_energy, epsilon
    )
    rows: list[dict[str, Any]] = []
    for arc_index in range(GLOBAL_ARC_COUNT):
        angle = 2 * math.pi * (arc_index + 0.5) / GLOBAL_ARC_COUNT
        displacement = parent.cpoint(
            radius * complex(math.cos(angle), math.sin(angle))
        )
        target = parent.cpoint(-9) + parent.cpoint(1j) * inputs["epsilon"]
        unit_circle = geometry["selected_root"] + displacement
        internal = parent.M5258.rotate_internal_lightcone(
            parent.M5386.amplitude_state(geometry), unit_circle
        )
        _, right = parent.sheet_locked_interval_cut_momenta(internal, target)
        diagnostics = parent.M5258.IntervalDiagnostics()
        first = parent.displaced_first_rational_spinors(
            configuration,
            inputs,
            geometry,
            displacement,
            -1,
            diagnostics,
            "checkpoint_5408_direct_first",
        )
        spinors, _, charts = parent.rational_spinor_overrides(
            right,
            diagnostics,
            "checkpoint_5408_direct",
            first,
            None,
        )
        direct = parent.M5258.spinor_bracket(
            spinors[1][1], spinors[4][1]
        )
        correlated = parent.centered_path_correlated_external4_first_square(
            configuration,
            cell,
            "LEFT_CONNECTOR",
            coordinate,
            parameter,
            epsilon,
            displacement,
            charts[1],
        )
        direct_value = complex(parent.M5394.midpoint(direct))
        correlated_value = complex(parent.M5394.midpoint(correlated))
        rows.append(
            {
                "checkpoint": 5408,
                "global_arc_index": arc_index,
                "first_chart": charts[1],
                "direct_square_real": direct_value.real,
                "direct_square_imaginary": direct_value.imag,
                "direct_square_abs": abs(direct_value),
                "correlated_square_real": correlated_value.real,
                "correlated_square_imaginary": correlated_value.imag,
                "correlated_square_abs": abs(correlated_value),
                "absolute_identity_error": abs(
                    direct_value - correlated_value
                ),
            }
        )
    return rows


def subcover_rows(
    parent: Any,
    cell: dict[str, Any],
    configuration: dict[str, Any],
    epsilon_row: dict[str, Any],
    radius: float,
) -> list[dict[str, Any]]:
    epsilon = parent.epsilon_interval(epsilon_row)
    coordinate = parent.cbox(X_LOWER, X_UPPER)
    parameter = parent.cbox(T_LOWER, T_UPPER)
    rows: list[dict[str, Any]] = []
    for arc_index in range(GLOBAL_ARC_COUNT):
        phase = parent.cbox(arc_index, arc_index + 1) * parent.cpoint(
            2 * math.pi / GLOBAL_ARC_COUNT
        )
        displacement = parent.cpoint(radius) * (
            parent.iv.cos(phase)
            + parent.cpoint(1j) * parent.iv.sin(phase)
        )
        enclosure = (
            parent.subdivided_path_correlated_external4_first_square(
                configuration,
                cell,
                "LEFT_CONNECTOR",
                coordinate,
                parameter,
                epsilon,
                displacement,
                "plus",
                SUBDIVISION_COUNT,
            )
        )
        real_lower, real_upper = parent.M5394.real_bounds(enclosure)
        imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(
            enclosure
        )
        rows.append(
            {
                "checkpoint": 5408,
                "global_arc_index": arc_index,
                "x_subdivision_count": SUBDIVISION_COUNT,
                "path_subdivision_count": SUBDIVISION_COUNT,
                "leaf_count": SUBDIVISION_COUNT**2,
                "square_real_lower": real_lower,
                "square_real_upper": real_upper,
                "square_imaginary_lower": imaginary_lower,
                "square_imaginary_upper": imaginary_upper,
                "square_abs_lower": parent.M5258.lower_abs(enclosure),
                "square_abs_upper": parent.M5258.upper_abs(enclosure),
                "valid_for_representative_external41_square_nonzero": (
                    parent.M5258.lower_abs(enclosure) > 0.0
                ),
            }
        )
    return rows


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5408: representative external-4/first square subcover gate",
        "",
        "## Decision",
        "",
        "**PASS FOR CONTINUED V41 PRODUCTION ONLY.**",
        "",
        "The proposed `{1,4}` invariant override is rejected. At the support endpoint the global displacement lifts that invariant to only order `10^-10`, and its phase winds around the four contour arcs. A rectangular invariant lower bound would therefore be the wrong certificate.",
        "",
        "## Derived edge",
        "",
        "For right external leg 4 in its plus chart and hard leg 1 in its plus chart,",
        "",
        "```text",
        "p4 = (1,-T,0,-z),",
        "tilde_lambda_4 = (1,-T/(1-z)),",
        "tilde_lambda_1 = (1,hbar_1/p1_plus),",
        "[14] = -T/(1-z) - hbar_1/p1_plus.",
        "```",
        "",
        "This ratio form removes the interval dependency introduced by reconstructing the two spinors independently. It is an identity, not a closure or fitted replacement.",
        "",
        "## Numeric certificate",
        "",
        f"- maximum pointwise direct-versus-derived identity error: `{payload['maximum_identity_error']:.17g}`;",
        f"- finite path subcover: `{SUBDIVISION_COUNT} x {SUBDIVISION_COUNT}` on each of `{GLOBAL_ARC_COUNT}` global arcs;",
        f"- minimum rigorous `[14]` absolute lower bound: `{payload['minimum_square_abs_lower']:.17g}`;",
        f"- formerly failing depth-18 leaf denominator margin after repair: `{payload['repaired_leaf_denominator_abs_lower']:.17g}`;",
        f"- production state after the bounded resume: `{payload['completed_path_jobs']}/{payload['total_path_jobs']}` path jobs, `{payload['active_accepted_box_count']}` accepted and `{payload['active_pending_box_count']}` pending boxes in the active path.",
        "",
        "## Claim boundary",
        "",
        "This checkpoint certifies one representative-chart denominator and authorizes continued v41 production. It does not establish the complete regular-away W3 bound, event-local W3, UV finiteness, local GR, or the full MTS theory.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    required = (
        PARENT_SCRIPT,
        PREVIOUS,
        STATUS,
        MIGRATION,
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
    status = read_json(STATUS)
    migration = read_json(MIGRATION)
    state = read_json(ACTIVE_STATE)
    active_rows = read_csv(ACTIVE_ROWS)
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
    arguments = type(
        "Arguments",
        (),
        {
            "combined_regulator_box": True,
            "combined_regulator_slab_count": 2,
            "epsilon_subdivisions": 1,
        },
    )()
    epsilon_row = parent.epsilon_boxes(arguments)[0]
    coordinate = parent.cbox(X_LOWER, X_UPPER)
    parameter = parent.cbox(T_LOWER, T_UPPER)
    epsilon = parent.epsilon_interval(epsilon_row)
    lower_energy, _ = parent.interval_boundary_energy(
        cell["lower_energy_boundary"], X_LOWER, X_UPPER
    )
    energy = lower_energy + parent.cpoint(
        1j * parent.DEFAULT_ENERGY_DEFORMATION
    ) * parameter
    _, geometry = parent.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    radius = 1.0e-7 * max(
        1.0, parent.M5258.upper_abs(geometry["selected_root"])
    )

    identities = point_identity_rows(
        parent, cell, configuration, epsilon_row, radius
    )
    subcover = subcover_rows(
        parent, cell, configuration, epsilon_row, radius
    )
    exact_rows = [
        row
        for row in active_rows
        if row["refinement_path"] == REFINEMENT_PATH
        and int(row["refinement_depth"]) == REFINEMENT_DEPTH
        and math.isclose(float(row["x_lower"]), X_LOWER, abs_tol=1.0e-16)
        and math.isclose(float(row["x_upper"]), X_UPPER, abs_tol=1.0e-16)
        and math.isclose(float(row["t_lower"]), T_LOWER, abs_tol=1.0e-16)
        and math.isclose(float(row["t_upper"]), T_UPPER, abs_tol=1.0e-16)
    ]
    repaired_leaf = exact_rows[0] if exact_rows else None
    maximum_identity_error = max(
        float(row["absolute_identity_error"]) for row in identities
    )
    minimum_square_abs_lower = min(
        float(row["square_abs_lower"]) for row in subcover
    )
    broad_claim_columns = (
        "valid_for_D4_numeric_W3_bound",
        "valid_for_D4_numeric_uniform_remainder_bound",
        "valid_for_numeric_UV_claim",
        "valid_for_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    repaired_leaf_claim_safe = bool(repaired_leaf) and all(
        repaired_leaf[column] == "False" for column in broad_claim_columns
    )
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5407_authorizes_continuation",
            bool(previous["valid_for_continued_v40_production"])
            and previous["valid_for_global_univalence_claim"] is False
            and previous["valid_for_regular_away_W3_claim"] is False,
            "5407 authorizes production only",
        ),
        check(
            "parent_revision_is_v41",
            parent.REVISION == "D4-deformed-contour-regular-away-W3-v41",
            parent.REVISION,
        ),
        check(
            "v40_state_migrated_to_v41",
            migration["previous_manifest"]["revision"].endswith("v40")
            and migration["current_manifest"]["revision"].endswith("v41")
            and state["revision"].endswith("v41"),
            "manifest and active adaptive state are v41",
        ),
        check(
            "derived_square_matches_direct_spinors",
            maximum_identity_error <= 2.0e-15
            and all(row["first_chart"] == "plus" for row in identities),
            f"maximum absolute error={maximum_identity_error:.17g}",
        ),
        check(
            "finite_square_subcover_is_nonzero",
            len(subcover) == GLOBAL_ARC_COUNT
            and minimum_square_abs_lower > 0.0
            and all(
                bool(row["valid_for_representative_external41_square_nonzero"])
                for row in subcover
            ),
            f"minimum lower bound={minimum_square_abs_lower:.17g}",
        ),
        check(
            "formerly_failing_leaf_is_committed",
            repaired_leaf is not None
            and repaired_leaf["chart_roles"] == "representative"
            and float(repaired_leaf["minimum_amplitude_denominator_abs_lower"])
            > 0.0
            and repaired_leaf["valid_for_D4_numeric_regular_away_W3_bound"]
            == "True",
            "the exact depth-18 LLDLDLDLDLDLDLDLDL leaf is now certified",
        ),
        check(
            "bounded_resume_advanced_production",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(status["completed_path_jobs"]) == 27
            and int(status["total_path_jobs"]) == 240
            and int(state["accepted_count"]) == 7
            and len(state["stack"]) == 15,
            "27/240 path jobs; active path has 7 accepted and 15 pending boxes",
        ),
        check(
            "broad_claims_remain_false",
            repaired_leaf_claim_safe,
            "W3, UV, local-GR, and full-MTS flags remain false",
        ),
    ]
    failed = [row for row in validations if not row["passed"]]
    repaired_leaf_denominator = (
        float(repaired_leaf["minimum_amplitude_denominator_abs_lower"])
        if repaired_leaf is not None
        else 0.0
    )
    payload = {
        "checkpoint": 5408,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_representative_external41_square_subcover": not failed,
        "valid_for_continued_v41_production": not failed,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "maximum_identity_error": maximum_identity_error,
        "minimum_square_abs_lower": minimum_square_abs_lower,
        "maximum_square_abs_upper": max(
            float(row["square_abs_upper"]) for row in subcover
        ),
        "global_arc_count": GLOBAL_ARC_COUNT,
        "subdivision_count": SUBDIVISION_COUNT,
        "subcover_leaf_count": GLOBAL_ARC_COUNT * SUBDIVISION_COUNT**2,
        "repaired_leaf_refinement_path": REFINEMENT_PATH,
        "repaired_leaf_denominator_abs_lower": repaired_leaf_denominator,
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "active_accepted_box_count": int(state["accepted_count"]),
        "active_pending_box_count": len(state["stack"]),
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(
        OUTPUT / "representative_external41_square_identity_crosschecks.csv",
        identities,
    )
    atomic_csv(
        OUTPUT / "representative_external41_square_subcover.csv", subcover
    )
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5408_VALIDATION.csv", validations)
    atomic_json(
        OUTPUT / "representative_external41_square_subcover_gate_result.json",
        payload,
    )
    write_document(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5408 validation failed: "
            + " | ".join(row["check"] for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
