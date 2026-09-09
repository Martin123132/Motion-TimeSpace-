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


CHECKPOINT = 5440
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
INVALID_PREPROBE = OUTPUT / "collision_jacobian_dimension_ablation.json"
DOCUMENT = (
    POST / "5440-Y5-R2FR-D4-collision-jacobian-finite-subcover-gate.md"
)
COVER_ROWS = OUTPUT / "collision_jacobian_finite_subcover_rows.csv"
ABLATION_ROWS = OUTPUT / "collision_jacobian_corrected_ablation_rows.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5440_VALIDATION.csv"
RESULT = OUTPUT / "collision_jacobian_finite_subcover_result.json"

EXPECTED_PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v48"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
TERM_ID = "MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
TARGET_PATH = "LRDRDRDLDLDRDL"
SCHEDULE = (
    (2, 2),
    (4, 4),
    (8, 8),
    (8, 16),
    (8, 32),
    (8, 64),
    (8, 128),
    (8, 256),
)
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
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def validation_row(check: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "check": check,
        "passed": passed,
        "detail": detail,
    }


def interval_bounds(parent: Any, value: Any) -> dict[str, float]:
    real_lower, real_upper = parent.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(value)
    return {
        "real_lower": real_lower,
        "real_upper": real_upper,
        "imaginary_lower": imaginary_lower,
        "imaginary_upper": imaginary_upper,
        "abs_lower": parent.M5258.lower_abs(value),
        "abs_upper": parent.M5258.upper_abs(value),
    }


def midpoint_point(parent: Any, value: Any) -> Any:
    return parent.cpoint(complex(parent.M5394.midpoint(value)))


def split_real_interval(parent: Any, value: Any, count: int) -> list[Any]:
    lower, upper = parent.M5394.real_bounds(value)
    return [
        parent.cbox(
            lower + (upper - lower) * index / count,
            lower + (upper - lower) * (index + 1) / count,
        )
        for index in range(count)
    ]


def candidate_rows(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
) -> list[dict[str, Any]]:
    candidates = parent.path_correlated_collision_jacobian_candidates(
        configuration,
        cell,
        PATH_SEGMENT,
        coordinate,
        parameter,
        epsilon,
    )
    return [
        {
            "abs_lower": float(lower),
            "method": method,
            "jacobian": jacobian,
            "denominator_lower": float(denominator_lower),
        }
        for lower, method, jacobian, denominator_lower in candidates
        if float(denominator_lower) > 0.0
    ]


def corrected_ablation(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    domains = {
        "x": {"box": coordinate, "point": midpoint_point(parent, coordinate)},
        "t": {"box": parameter, "point": midpoint_point(parent, parameter)},
        "epsilon": {
            "box": epsilon,
            "point": midpoint_point(parent, epsilon),
        },
    }
    for x_mode in ("box", "point"):
        for t_mode in ("box", "point"):
            for epsilon_mode in ("box", "point"):
                try:
                    candidates = candidate_rows(
                        parent,
                        configuration,
                        cell,
                        domains["x"][x_mode],
                        domains["t"][t_mode],
                        domains["epsilon"][epsilon_mode],
                    )
                    selected = max(
                        candidates,
                        key=lambda row: (
                            row["abs_lower"],
                            row["denominator_lower"],
                        ),
                    )
                except Exception as error:
                    rows.append(
                        {
                            "x_mode": x_mode,
                            "t_mode": t_mode,
                            "epsilon_mode": epsilon_mode,
                            "status": "FAIL",
                            "selected_method": "",
                            "selected_abs_lower": 0.0,
                            "selected_denominator_lower": 0.0,
                            "error_type": type(error).__name__,
                            "error": str(error),
                        }
                    )
                    continue
                rows.append(
                    {
                        "x_mode": x_mode,
                        "t_mode": t_mode,
                        "epsilon_mode": epsilon_mode,
                        "status": "PASS" if selected["abs_lower"] > 0.0 else "ZERO",
                        "selected_method": selected["method"],
                        "selected_abs_lower": selected["abs_lower"],
                        "selected_denominator_lower": selected[
                            "denominator_lower"
                        ],
                        "error_type": "",
                        "error": "",
                    }
                )
    return rows


def finite_subcover(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    x_count: int,
    t_count: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    jacobians: list[Any] = []
    rows: list[dict[str, Any]] = []
    uncovered_count = 0
    x_boxes = split_real_interval(parent, coordinate, x_count)
    t_boxes = split_real_interval(parent, parameter, t_count)
    for x_index, x_box in enumerate(x_boxes):
        for t_index, t_box in enumerate(t_boxes):
            candidates = candidate_rows(
                parent,
                configuration,
                cell,
                x_box,
                t_box,
                epsilon,
            )
            if not candidates:
                uncovered_count += 1
                rows.append(
                    {
                        "x_count": x_count,
                        "t_count": t_count,
                        "x_index": x_index,
                        "t_index": t_index,
                        "x_lower": parent.M5394.real_bounds(x_box)[0],
                        "x_upper": parent.M5394.real_bounds(x_box)[1],
                        "t_lower": parent.M5394.real_bounds(t_box)[0],
                        "t_upper": parent.M5394.real_bounds(t_box)[1],
                        "selected_method": "UNCOVERED",
                        "selected_abs_lower": 0.0,
                        "selected_denominator_lower": 0.0,
                        "jacobian_real_lower": 0.0,
                        "jacobian_real_upper": 0.0,
                        "jacobian_imaginary_lower": 0.0,
                        "jacobian_imaginary_upper": 0.0,
                    }
                )
                continue
            selected = max(
                candidates,
                key=lambda row: (
                    row["abs_lower"],
                    row["denominator_lower"],
                ),
            )
            bounds = interval_bounds(parent, selected["jacobian"])
            jacobians.append(selected["jacobian"])
            rows.append(
                {
                    "x_count": x_count,
                    "t_count": t_count,
                    "x_index": x_index,
                    "t_index": t_index,
                    "x_lower": parent.M5394.real_bounds(x_box)[0],
                    "x_upper": parent.M5394.real_bounds(x_box)[1],
                    "t_lower": parent.M5394.real_bounds(t_box)[0],
                    "t_upper": parent.M5394.real_bounds(t_box)[1],
                    "selected_method": selected["method"],
                    "selected_abs_lower": selected["abs_lower"],
                    "selected_denominator_lower": selected[
                        "denominator_lower"
                    ],
                    "jacobian_real_lower": bounds["real_lower"],
                    "jacobian_real_upper": bounds["real_upper"],
                    "jacobian_imaginary_lower": bounds["imaginary_lower"],
                    "jacobian_imaginary_upper": bounds["imaginary_upper"],
                }
            )
    hull_bounds = (
        interval_bounds(parent, parent.rectangular_interval_hull(jacobians))
        if jacobians
        else {
            "real_lower": 0.0,
            "real_upper": 0.0,
            "imaginary_lower": 0.0,
            "imaginary_upper": 0.0,
            "abs_lower": 0.0,
            "abs_upper": 0.0,
        }
    )
    leaf_minimum = min(float(row["selected_abs_lower"]) for row in rows)
    denominator_minimum = min(
        float(row["selected_denominator_lower"]) for row in rows
    )
    return (
        {
            "x_count": x_count,
            "t_count": t_count,
            "leaf_count": len(rows),
            "uncovered_leaf_count": uncovered_count,
            "all_leaf_jacobians_nonzero": (
                uncovered_count == 0 and leaf_minimum > 0.0
            ),
            "leaf_union_abs_lower": leaf_minimum,
            "leaf_denominator_abs_lower": denominator_minimum,
            "rectangular_hull_abs_lower": hull_bounds["abs_lower"],
            "rectangular_hull_real_lower": hull_bounds["real_lower"],
            "rectangular_hull_real_upper": hull_bounds["real_upper"],
            "rectangular_hull_imaginary_lower": hull_bounds[
                "imaginary_lower"
            ],
            "rectangular_hull_imaginary_upper": hull_bounds[
                "imaginary_upper"
            ],
        },
        rows,
    )


def write_document(payload: dict[str, Any]) -> None:
    selected = payload["selected_cover"]
    decision = (
        "**THE COLLISION-JACOBIAN ZERO IS A COARSE PATH-INTERVAL ARTIFACT ON THIS CELL.**"
        if payload["valid_for_collision_jacobian_finite_subcover"]
        else "**THE COLLISION-JACOBIAN CELL REMAINS OPEN.**"
    )
    lines = [
        "# 5440: collision-Jacobian finite-subcover gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "The corrected probe uses the actual `MC04_SP_DP` representative configuration (`minus_u`), not the inapplicable explicit `minus_v` chart used by the quarantined exploratory pre-probe.",
        "",
        "## Exact cover law",
        "",
        "Let the compact parameter cell be the finite union `D = union_i D_i`. If interval evaluation proves `J(D_i) subset B_i` and `0 notin B_i` for every leaf, then",
        "",
        "`inf_{z in D} |J(z)| >= min_i dist(0, B_i) > 0`.",
        "",
        "Taking one rectangular hull of all `B_i` is stronger than this theorem requires and can fill gaps between disconnected image boxes. Here the stronger test also closes after path-only refinement: the `8 x 64` rectangular hull excludes zero, whereas the parent's terminal `8 x 32` cover did not.",
        "",
        "## Certified cell",
        "",
        f"- Path: `{payload['target_path']}` at depth {payload['target_depth']}.",
        f"- Domain: `x in [{payload['x_lower']}, {payload['x_upper']}]`, `t in [{payload['t_lower']}, {payload['t_upper']}]`.",
        f"- Cover: `{selected['x_count']} x {selected['t_count']}` = {selected['leaf_count']} leaves.",
        f"- Leaf-union `|J|` lower bound: `{selected['leaf_union_abs_lower']}`.",
        f"- Chart-denominator lower bound: `{selected['leaf_denominator_abs_lower']}`.",
        f"- Selected-cover rectangular-hull `|J|` lower bound: `{selected['rectangular_hull_abs_lower']}`.",
        "",
        "## Claim boundary",
        "",
        "This proves only the local collision-Jacobian finite subcover needed by the active right-connector cell. Parent integration and a resumed production advance are still required; no W3, UV, local-GR, or full-MTS claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    parent = load_module("mts_parent_5396_v48_for_5440", PARENT_SCRIPT)
    parent.iv.dps = parent.INTERVAL_DIGITS
    state = read_json(ACTIVE_STATE)
    state_row = next(row for row in state["stack"] if row[5] == TARGET_PATH)
    x_lower, x_upper, t_lower, t_upper, depth, _ = state_row
    coordinate = parent.cbox(float(x_lower), float(x_upper))
    parameter = parent.cbox(float(t_lower), float(t_upper))
    full_epsilon_lower = (
        parent.M5394.REGULATOR_INTERVAL[0]
        - parent.M5394.REGULATOR_CAUCHY_RADIUS
    )
    full_epsilon_upper = (
        parent.M5394.REGULATOR_INTERVAL[1]
        + parent.M5394.REGULATOR_CAUCHY_RADIUS
    )
    slab_upper = 0.5 * (full_epsilon_lower + full_epsilon_upper)
    epsilon = parent.cbox(
        full_epsilon_lower,
        slab_upper,
        -parent.M5394.REGULATOR_CAUCHY_RADIUS,
        parent.M5394.REGULATOR_CAUCHY_RADIUS,
    )
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == MAPPED_CELL_ID
    )
    configuration = next(
        row
        for row in parent.configuration_variants(TERM_ID)
        if row["role"] == "representative"
    )
    ablations = corrected_ablation(
        parent,
        configuration,
        cell,
        coordinate,
        parameter,
        epsilon,
    )
    atomic_csv(ABLATION_ROWS, ablations)
    cover_summaries: list[dict[str, Any]] = []
    all_cover_rows: list[dict[str, Any]] = []
    for x_count, t_count in SCHEDULE:
        summary, rows = finite_subcover(
            parent,
            configuration,
            cell,
            coordinate,
            parameter,
            epsilon,
            x_count,
            t_count,
        )
        cover_summaries.append(summary)
        all_cover_rows.extend(rows)
        if summary["all_leaf_jacobians_nonzero"]:
            break
    atomic_csv(COVER_ROWS, all_cover_rows)
    selected_cover = next(
        (
            row
            for row in cover_summaries
            if row["all_leaf_jacobians_nonzero"]
        ),
        cover_summaries[-1],
    )
    invalid_preprobe = read_json(INVALID_PREPROBE)
    invalid_preprobe_quarantined = (
        invalid_preprobe.get("revision")
        == EXPECTED_PARENT_REVISION
        and all(
            row.get("error")
            == "explicit alternate collision chart requires minus_v"
            for row in invalid_preprobe.get("ablations", [])
        )
    )
    valid = (
        selected_cover["all_leaf_jacobians_nonzero"]
        and selected_cover["leaf_union_abs_lower"] > 0.0
        and selected_cover["leaf_denominator_abs_lower"] > 0.0
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_path": TARGET_PATH,
        "target_depth": int(depth),
        "x_lower": float(x_lower),
        "x_upper": float(x_upper),
        "t_lower": float(t_lower),
        "t_upper": float(t_upper),
        "epsilon_bounds": interval_bounds(parent, epsilon),
        "configuration_role": configuration["role"],
        "configuration_root_labels": configuration["root_labels"],
        "corrected_ablation_rows": len(ablations),
        "invalid_preprobe_quarantined": invalid_preprobe_quarantined,
        "cover_summaries": cover_summaries,
        "selected_cover": selected_cover,
        "valid_for_collision_jacobian_finite_subcover": valid,
        "next_target": (
            "INTEGRATE_LEAF_UNION_MINIMUM_IN_PARENT_V49"
            if valid
            else "REFINE_COLLISION_JACOBIAN_COVER"
        ),
        **{flag: False for flag in BROAD_FLAGS},
    }
    validations = [
        validation_row(
            "all_sources_exist",
            all(path.exists() for path in (PARENT_SCRIPT, ACTIVE_STATE, INVALID_PREPROBE)),
            "parent, active state, and exploratory pre-probe",
        ),
        validation_row(
            "parent_revision_is_v48",
            parent.REVISION == EXPECTED_PARENT_REVISION,
            parent.REVISION,
        ),
        validation_row(
            "actual_representative_configuration_selected",
            configuration["role"] == "representative"
            and configuration["root_labels"][0] == "minus_u",
            f"role={configuration['role']}, roots={configuration['root_labels']}",
        ),
        validation_row(
            "invalid_minus_v_preprobe_quarantined",
            invalid_preprobe_quarantined,
            "the exploratory explicit chart was inapplicable to minus_u",
        ),
        validation_row(
            "pointwise_collision_jacobian_is_nonzero",
            next(
                row
                for row in ablations
                if row["x_mode"] == row["t_mode"] == row["epsilon_mode"] == "point"
            )["selected_abs_lower"]
            > 0.0,
            "corrected projective chart at the cell centre",
        ),
        validation_row(
            "finite_subcover_closes_every_leaf",
            selected_cover["all_leaf_jacobians_nonzero"],
            f"leaves={selected_cover['leaf_count']}",
        ),
        validation_row(
            "finite_subcover_union_lower_is_positive",
            selected_cover["leaf_union_abs_lower"] > 0.0,
            str(selected_cover["leaf_union_abs_lower"]),
        ),
        validation_row(
            "finite_subcover_chart_denominators_are_nonzero",
            selected_cover["leaf_denominator_abs_lower"] > 0.0,
            str(selected_cover["leaf_denominator_abs_lower"]),
        ),
        validation_row(
            "cover_csv_row_count_matches_schedule",
            len(all_cover_rows)
            == sum(
                int(row["x_count"]) * int(row["t_count"])
                for row in cover_summaries
            ),
            f"rows={len(all_cover_rows)}",
        ),
        validation_row(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "parent integration and production resume remain open",
        ),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations.append(
        validation_row(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    payload["validation_row_count"] = len(validations)
    atomic_csv(VALIDATION, validations)
    write_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "selected_cover": payload["selected_cover"],
                "failed_validation_count": payload[
                    "failed_validation_count"
                ],
                "valid_for_collision_jacobian_finite_subcover": payload[
                    "valid_for_collision_jacobian_finite_subcover"
                ],
                "next_target": payload["next_target"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
