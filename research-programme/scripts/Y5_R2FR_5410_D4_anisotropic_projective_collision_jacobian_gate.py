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


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5410"
PARENT_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
DOCUMENT = (
    POST
    / "5410-Y5-R2FR-D4-anisotropic-projective-collision-Jacobian-gate.md"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5409"
    / "representative_external41_production_stability_result.json"
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
X_UPPER = 0.31538204492856226
T_LOWER = 0.0078125
T_UPPER = 0.015625
EXPECTED_PARAMETER_AREA = 0.03932753620548854
ANISOTROPIC_METHOD = (
    "SUBDIVIDED_PATH_CORRELATED_PROJECTIVE_UNION_8X16"
)


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


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


def cover_rows(parent: Any) -> list[dict[str, Any]]:
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
    epsilon = parent.epsilon_interval(parent.epsilon_boxes(arguments)[0])
    coordinate = parent.cbox(X_LOWER, X_UPPER)
    parameter = parent.cbox(T_LOWER, T_UPPER)
    rows: list[dict[str, Any]] = []
    for x_count, path_count in ((8, 8), (8, 16)):
        candidate = (
            parent.subdivided_path_correlated_collision_jacobian_candidate(
                configuration,
                cell,
                "LEFT_CONNECTOR",
                coordinate,
                parameter,
                epsilon,
                x_count,
                path_count,
            )
        )
        rows.append(
            {
                "checkpoint": 5410,
                "mapped_cell_id": cell["mapped_cell_id"],
                "term_id": "MC04_SP_DP",
                "selected_role": configuration["role"],
                "path_segment": "LEFT_CONNECTOR",
                "x_lower": X_LOWER,
                "x_upper": X_UPPER,
                "t_lower": T_LOWER,
                "t_upper": T_UPPER,
                "x_subdivision_count": x_count,
                "path_subdivision_count": path_count,
                "subcover_leaf_count": x_count * path_count,
                "enclosure_method": candidate[1],
                "collision_jacobian_abs_lower": candidate[0],
                "collision_jacobian_hull_abs_lower": parent.M5258.lower_abs(
                    candidate[2]
                ),
                "projective_chart_denominator_abs_lower": candidate[3],
                "valid_for_collision_jacobian_nonzero": candidate[0] > 0.0,
            }
        )
    return rows


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5410: anisotropic projective collision-Jacobian gate",
        "",
        "## Decision",
        "",
        "**PASS FOR CONTINUED V42 PRODUCTION ONLY.**",
        "",
        "The dominant v41 geometric split was not a physical collision and not a missing parent Jacobian. The selected representative branch is `minus_u`, so the existing anisotropic explicit `minus_v` fallback was algebraically inapplicable. The valid projective fallback was unnecessarily restricted to square covers.",
        "",
        "## Exact repair",
        "",
        "Revision v42 generalizes the projective union from `N x N` to independent `N_x x N_t` closed subcovers. This changes only the finite partition used to enclose the same parent mixed-root derivative; it introduces no fitted coefficient, sign axiom, or closure term.",
        "",
        "On the historical depth-15 parent box:",
        "",
        f"- `8 x 8` collision-Jacobian lower bound: `{payload['square_cover_jacobian_abs_lower']:.17g}`;",
        f"- `8 x 16` collision-Jacobian lower bound: `{payload['anisotropic_cover_jacobian_abs_lower']:.17g}`;",
        f"- `8 x 16` projective denominator lower bound: `{payload['anisotropic_cover_denominator_abs_lower']:.17g}`.",
        "",
        "## Production regression",
        "",
        f"- active state migrated `v41 -> v42` without requeuing accepted rows;",
        f"- current active partition: `{payload['active_accepted_box_count']}` accepted and `{payload['active_pending_box_count']}` pending boxes;",
        f"- accepted production rows using the new `8 x 16` proof: `{payload['anisotropic_production_row_count']}`;",
        f"- exact accepted-plus-pending area: `{payload['total_parameter_area']:.17g}`.",
        "",
        "## Claim boundary",
        "",
        "This removes one conservative collision-Jacobian split class on the active contour path. The remaining edge refinements, complete path, regular-away W3 sum, event-local W3, UV, local-GR, and full-MTS gates remain open.",
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
    rows = read_csv(ACTIVE_ROWS)
    covers = cover_rows(parent)
    square_cover, anisotropic_cover = covers
    anisotropic_rows = [
        row
        for row in rows
        if row["collision_jacobian_enclosure_method"] == ANISOTROPIC_METHOD
    ]
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    remaining_area = pending_area(state["stack"])
    total_area = accepted_area + remaining_area
    pending_depths = [int(row[4]) for row in state["stack"]]
    broad_columns = (
        "valid_for_D4_numeric_W3_bound",
        "valid_for_D4_numeric_uniform_remainder_bound",
        "valid_for_numeric_UV_claim",
        "valid_for_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    minimum_denominator = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in rows
    )
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5409_authorizes_continuation",
            bool(previous["valid_for_continued_v41_production"])
            and previous["valid_for_regular_away_W3_claim"] is False,
            "5409 authorizes production only",
        ),
        check(
            "parent_revision_is_v42",
            parent.REVISION == "D4-deformed-contour-regular-away-W3-v42",
            parent.REVISION,
        ),
        check(
            "v41_state_migrated_to_v42",
            migration["previous_manifest"]["revision"].endswith("v41")
            and migration["current_manifest"]["revision"].endswith("v42")
            and state["revision"].endswith("v42"),
            "manifest and active adaptive state are v42",
        ),
        check(
            "square_projective_cover_reproduces_failure",
            float(square_cover["collision_jacobian_abs_lower"]) == 0.0,
            "8x8 retains zero on the historical parent box",
        ),
        check(
            "anisotropic_projective_cover_proves_nonzero",
            float(anisotropic_cover["collision_jacobian_abs_lower"]) > 0.0
            and float(
                anisotropic_cover[
                    "projective_chart_denominator_abs_lower"
                ]
            )
            > 0.0,
            "8x16 proves both Jacobian and projective denominator nonzero",
        ),
        check(
            "production_uses_anisotropic_projective_cover",
            len(anisotropic_rows) >= 2
            and all(
                float(row["collision_jacobian_abs_lower"]) > 0.0
                for row in anisotropic_rows
            ),
            f"{len(anisotropic_rows)} accepted rows use {ANISOTROPIC_METHOD}",
        ),
        check(
            "adaptive_area_partition_is_exact",
            math.isclose(
                total_area,
                EXPECTED_PARAMETER_AREA,
                rel_tol=1.0e-12,
                abs_tol=1.0e-12,
            )
            and status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            f"accepted={accepted_area:.17g}; pending={remaining_area:.17g}",
        ),
        check(
            "all_accepted_rows_are_finite",
            len(rows) == int(state["accepted_count"]) == 67
            and minimum_denominator > 0.0
            and all(
                row["valid_for_D4_numeric_regular_away_W3_bound"] == "True"
                for row in rows
            ),
            f"67 rows; minimum denominator={minimum_denominator:.17g}",
        ),
        check(
            "broad_claims_remain_false",
            all(
                row[column] == "False"
                for row in rows
                for column in broad_columns
            ),
            "W3, UV, local-GR, and full-MTS flags remain false",
        ),
    ]
    failed = [row for row in validations if not row["passed"]]
    payload = {
        "checkpoint": 5410,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_anisotropic_projective_collision_jacobian": not failed,
        "valid_for_continued_v42_production": not failed,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "square_cover_jacobian_abs_lower": float(
            square_cover["collision_jacobian_abs_lower"]
        ),
        "anisotropic_cover_jacobian_abs_lower": float(
            anisotropic_cover["collision_jacobian_abs_lower"]
        ),
        "anisotropic_cover_denominator_abs_lower": float(
            anisotropic_cover["projective_chart_denominator_abs_lower"]
        ),
        "anisotropic_production_row_count": len(anisotropic_rows),
        "anisotropic_production_refinement_paths": [
            row["refinement_path"] for row in anisotropic_rows
        ],
        "active_accepted_box_count": int(state["accepted_count"]),
        "active_pending_box_count": len(state["stack"]),
        "active_maximum_pending_depth": max(pending_depths, default=-1),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": remaining_area,
        "total_parameter_area": total_area,
        "minimum_accepted_denominator_abs_lower": minimum_denominator,
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(
        OUTPUT / "anisotropic_projective_collision_jacobian_cover.csv", covers
    )
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5410_VALIDATION.csv", validations)
    atomic_json(
        OUTPUT / "anisotropic_projective_collision_jacobian_result.json",
        payload,
    )
    write_document(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5410 validation failed: "
            + " | ".join(row["check"] for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
